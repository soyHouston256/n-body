#!/usr/bin/env python3
"""
🚀 SUITE DE BENCHMARKING N-BODY
Análisis completo de performance para proyecto HPC
"""

import subprocess
import time
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import json
from datetime import datetime

class NBenchmark:
    def __init__(self):
        self.results = []
        self.system_info = self.get_system_info()
        
    def get_system_info(self):
        """Obtiene información del sistema"""
        try:
            cpu_info = subprocess.check_output("sysctl -n machdep.cpu.brand_string", shell=True).decode().strip()
            cpu_cores = subprocess.check_output("sysctl -n hw.ncpu", shell=True).decode().strip()
        except:
            cpu_info = "Unknown CPU"
            cpu_cores = "Unknown"
            
        return {
            'cpu': cpu_info,
            'cores': cpu_cores,
            'timestamp': datetime.now().isoformat()
        }
    
    def run_single_benchmark(self, processes, config_file, label=""):
        """Ejecuta un benchmark individual"""
        print(f"🔄 Ejecutando: P={processes}, Config={config_file}")
        
        # Comando MPI
        if processes == 1:
            cmd = f"./cpu-4th < {config_file}"
        else:
            cmd = f"mpirun -n {processes} ./cpu-4th < {config_file}"
        
        # Medir tiempo
        start_time = time.time()
        
        try:
            result = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=3600)
            end_time = time.time()
            
            if result.returncode != 0:
                print(f"❌ Error en ejecución: {result.stderr}")
                return None
                
            wall_time = end_time - start_time
            
            # Parsear salida para obtener métricas
            metrics = self.parse_output(result.stdout, result.stderr)
            metrics.update({
                'processes': processes,
                'wall_time': wall_time,
                'config': config_file,
                'label': label,
                'success': True
            })
            
            print(f"✅ Completado en {wall_time:.2f}s")
            return metrics
            
        except subprocess.TimeoutExpired:
            print(f"⏰ Timeout después de 1 hora")
            return None
        except Exception as e:
            print(f"❌ Error: {e}")
            return None
    
    def parse_output(self, stdout, stderr):
        """Extrae métricas de la salida del programa"""
        lines = stdout.split('\n')
        
        # Buscar líneas con métricas de tiempo y energía
        cpu_time = 0
        energy_error = 0
        timesteps = 0
        
        for line in lines:
            if 'CPU_time_user' in line or len(line.split()) >= 8:
                try:
                    parts = line.split()
                    if len(parts) >= 8:
                        cpu_time = float(parts[-1])  # Último campo suele ser CPU time
                        energy_error = abs(float(parts[6]))  # Error de energía
                        timesteps = float(parts[1])
                        break
                except:
                    continue
        
        return {
            'cpu_time': cpu_time,
            'energy_error': energy_error,
            'timesteps': timesteps
        }
    
    def strong_scaling_benchmark(self, process_list=[1, 2, 4, 8, 16], config="phi-GPU4.cfg"):
        """Benchmark de escalabilidad fuerte (N fijo, P variable)"""
        print("🔥 BENCHMARK DE ESCALABILIDAD FUERTE")
        print("="*50)
        
        results = []
        
        for p in process_list:
            result = self.run_single_benchmark(p, config, f"Strong_P{p}")
            if result:
                results.append(result)
                self.results.append(result)
        
        return results
    
    def weak_scaling_benchmark(self, base_particles=1280, process_list=[1, 2, 4, 8]):
        """Benchmark de escalabilidad débil (N/P fijo, P variable)"""
        print("🔥 BENCHMARK DE ESCALABILIDAD DÉBIL")
        print("="*50)
        
        results = []
        
        for p in process_list:
            n_particles = base_particles * p
            
            # Generar datos de entrada
            print(f"📊 Generando {n_particles} partículas...")
            self.generate_plummer_data(n_particles, f"data_{n_particles}.inp")
            
            # Crear configuración
            config_file = f"config_weak_{p}.cfg"
            self.create_config(config_file, f"data_{n_particles}.inp")
            
            result = self.run_single_benchmark(p, config_file, f"Weak_P{p}_N{n_particles}")
            if result:
                result['particles'] = n_particles
                result['particles_per_process'] = n_particles // p
                results.append(result)
                self.results.append(result)
        
        return results
    
    def generate_plummer_data(self, n_particles, output_file):
        """Genera datos Plummer usando gen-plum.c"""
        # Modificar gen-plum.c para usar N partículas
        with open('gen-plum.c', 'r') as f:
            content = f.read()
        
        # Reemplazar N en el código
        content = content.replace('#define N 5120', f'#define N {n_particles}')
        
        with open('gen-plum-temp.c', 'w') as f:
            f.write(content)
        
        # Compilar y ejecutar
        subprocess.run("gcc -o gen-plum-temp gen-plum-temp.c -lm", shell=True)
        subprocess.run(f"./gen-plum-temp > {output_file}", shell=True)
        
        # Limpiar
        os.remove('gen-plum-temp.c')
        os.remove('gen-plum-temp')
    
    def create_config(self, config_file, data_file, t_end=1.0):
        """Crea archivo de configuración"""
        config_content = f"""1.0E-04   {t_end}   0.25   0.125   0.15   0.15   {data_file}"""
        
        with open(config_file, 'w') as f:
            f.write(config_content)
    
    def calculate_metrics(self, results):
        """Calcula métricas de performance"""
        if not results:
            return {}
        
        # Tiempo base (P=1)
        base_time = None
        for r in results:
            if r['processes'] == 1:
                base_time = r['wall_time']
                break
        
        if base_time is None:
            base_time = results[0]['wall_time']
        
        # Calcular speedup y eficiencia
        for r in results:
            r['speedup'] = base_time / r['wall_time']
            r['efficiency'] = r['speedup'] / r['processes'] * 100
            
            # FLOPS estimados (20 FLOPS por interacción)
            n_particles = r.get('particles', 5120)
            flops_per_step = n_particles**2 * 20 + n_particles * 60
            total_flops = flops_per_step * r.get('timesteps', 1000)
            r['gflops'] = total_flops / (r['wall_time'] * 1e9)
        
        return results
    
    def plot_results(self, results, title_prefix=""):
        """Genera gráficos de resultados"""
        if not results:
            print("❌ No hay resultados para graficar")
            return
        
        df = pd.DataFrame(results)
        
        # Crear figura con subplots
        fig, axes = plt.subplots(2, 2, figsize=(15, 12))
        fig.suptitle(f'{title_prefix} - Análisis de Performance N-Body', fontsize=16)
        
        # 1. Tiempo vs Procesos
        ax = axes[0, 0]
        ax.plot(df['processes'], df['wall_time'], 'bo-', linewidth=2, markersize=8)
        ax.set_xlabel('Número de Procesos')
        ax.set_ylabel('Tiempo (segundos)')
        ax.set_title('Tiempo de Ejecución')
        ax.grid(True, alpha=0.3)
        ax.set_yscale('log')
        
        # 2. Speedup vs Procesos
        ax = axes[0, 1]
        ax.plot(df['processes'], df['speedup'], 'ro-', linewidth=2, markersize=8, label='Speedup Real')
        ax.plot(df['processes'], df['processes'], 'k--', alpha=0.5, label='Speedup Ideal')
        ax.set_xlabel('Número de Procesos')
        ax.set_ylabel('Speedup')
        ax.set_title('Speedup')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # 3. Eficiencia vs Procesos
        ax = axes[1, 0]
        ax.plot(df['processes'], df['efficiency'], 'go-', linewidth=2, markersize=8)
        ax.axhline(y=80, color='r', linestyle='--', alpha=0.5, label='80% Eficiencia')
        ax.set_xlabel('Número de Procesos')
        ax.set_ylabel('Eficiencia (%)')
        ax.set_title('Eficiencia Paralela')
        ax.legend()
        ax.grid(True, alpha=0.3)
        
        # 4. GFLOPS vs Procesos
        ax = axes[1, 1]
        ax.plot(df['processes'], df['gflops'], 'mo-', linewidth=2, markersize=8)
        ax.set_xlabel('Número de Procesos')
        ax.set_ylabel('GFLOPS')
        ax.set_title('Rendimiento Computacional')
        ax.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        # Guardar gráfico
        filename = f"{title_prefix.lower().replace(' ', '_')}_performance.png"
        plt.savefig(filename, dpi=300, bbox_inches='tight')
        print(f"📊 Gráfico guardado: {filename}")
        plt.show()
    
    def generate_report(self, results, report_name="performance_report"):
        """Genera reporte completo"""
        if not results:
            print("❌ No hay resultados para el reporte")
            return
        
        df = pd.DataFrame(results)
        
        # Crear reporte en markdown
        report = f"""# 📊 REPORTE DE PERFORMANCE N-BODY
## {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

### 🖥️ Información del Sistema
- **CPU:** {self.system_info['cpu']}
- **Cores:** {self.system_info['cores']}
- **Timestamp:** {self.system_info['timestamp']}

### 📈 Resultados de Benchmarking

| Procesos | Tiempo (s) | Speedup | Eficiencia (%) | GFLOPS | Error Energía |
|----------|------------|---------|----------------|--------|---------------|
"""
        
        for _, row in df.iterrows():
            report += f"| {row['processes']} | {row['wall_time']:.2f} | {row['speedup']:.2f} | {row['efficiency']:.1f} | {row['gflops']:.2f} | {row['energy_error']:.2e} |\n"
        
        # Análisis
        best_efficiency = df.loc[df['efficiency'].idxmax()]
        best_speedup = df.loc[df['speedup'].idxmax()]
        
        report += f"""
### 🎯 Análisis de Resultados

**Mejor Eficiencia:**
- Procesos: {best_efficiency['processes']}
- Eficiencia: {best_efficiency['efficiency']:.1f}%
- Speedup: {best_efficiency['speedup']:.2f}x

**Mejor Speedup:**
- Procesos: {best_speedup['processes']}
- Speedup: {best_speedup['speedup']:.2f}x
- Eficiencia: {best_speedup['efficiency']:.1f}%

**Escalabilidad:**
- Eficiencia >80%: Hasta {df[df['efficiency'] >= 80]['processes'].max() if not df[df['efficiency'] >= 80].empty else 'N/A'} procesos
- Speedup máximo: {df['speedup'].max():.2f}x con {best_speedup['processes']} procesos

### 🔬 Conclusiones

1. **Escalabilidad fuerte:** {'Excelente' if best_efficiency['efficiency'] > 80 else 'Buena' if best_efficiency['efficiency'] > 60 else 'Regular'}
2. **Overhead de comunicación:** {'Bajo' if best_efficiency['efficiency'] > 85 else 'Moderado' if best_efficiency['efficiency'] > 70 else 'Alto'}
3. **Punto óptimo:** {best_efficiency['processes']} procesos para mejor balance eficiencia/speedup
"""
        
        # Guardar reporte
        with open(f"{report_name}.md", 'w') as f:
            f.write(report)
        
        # Guardar datos en JSON
        with open(f"{report_name}.json", 'w') as f:
            json.dump(results, f, indent=2)
        
        print(f"📄 Reporte guardado: {report_name}.md")
        print(f"💾 Datos guardados: {report_name}.json")
    
    def run_complete_benchmark(self):
        """Ejecuta suite completo de benchmarks"""
        print("🚀 INICIANDO SUITE COMPLETO DE BENCHMARKING")
        print("="*60)
        
        # 1. Escalabilidad fuerte
        strong_results = self.strong_scaling_benchmark([1, 2, 4, 8, 16])
        strong_results = self.calculate_metrics(strong_results)
        
        if strong_results:
            self.plot_results(strong_results, "Escalabilidad Fuerte")
            self.generate_report(strong_results, "strong_scaling_report")
        
        # 2. Escalabilidad débil (opcional, toma más tiempo)
        print("\n¿Ejecutar escalabilidad débil? (toma más tiempo) [y/N]: ", end="")
        if input().lower().startswith('y'):
            weak_results = self.weak_scaling_benchmark([1, 2, 4, 8])
            weak_results = self.calculate_metrics(weak_results)
            
            if weak_results:
                self.plot_results(weak_results, "Escalabilidad Débil")
                self.generate_report(weak_results, "weak_scaling_report")
        
        print("\n🎉 BENCHMARKING COMPLETADO")
        print("📊 Revisa los archivos generados para el análisis completo")

def main():
    """Función principal"""
    print("🔬 SUITE DE BENCHMARKING N-BODY HPC")
    print("Proyecto: Evolución Galáctica")
    print("="*50)
    
    # Verificar que el ejecutable existe
    if not os.path.exists('./cpu-4th'):
        print("❌ Error: ./cpu-4th no encontrado")
        print("Ejecuta: make cpu-4th")
        return
    
    benchmark = NBenchmark()
    benchmark.run_complete_benchmark()

if __name__ == "__main__":
    main()