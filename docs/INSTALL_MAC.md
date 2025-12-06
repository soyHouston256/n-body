# Guía de Instalación - Mac M1/M2/M3

Esta guía te muestra cómo configurar todo lo necesario para compilar, ejecutar y visualizar simulaciones N-Body en Mac con procesadores Apple Silicon (M1/M2/M3).

## ✅ Resumen de lo que necesitas

### 1. Compilación
- ✅ **Open MPI** (instalado) - Paralelización distribuida
- ✅ **libomp** (instalado) - Soporte OpenMP para Clang
- ✅ **Compilador C++** (incluido en Xcode) - Apple Clang

### 2. Visualización
- ✅ **Python 3** (ya instalado) - Python 3.9.6
- ✅ **NumPy** (instalado) - Cálculos numéricos
- ✅ **Matplotlib** (instalado) - Gráficos y visualización 3D

---

## 📦 Instalación Completa (ya hecha)

```bash
# 1. Instalar Open MPI
brew install open-mpi

# 2. Instalar soporte OpenMP
brew install libomp

# 3. Instalar bibliotecas Python para visualización
pip3 install numpy matplotlib
```

---

## 🔨 Compilación

```bash
cd N-Body-CPU

# Compilar todas las versiones (4to, 6to, 8vo orden)
make all

# O compilar individualmente
make cpu-4th   # 4to orden - Más rápido
make cpu-6th   # 6to orden - Balance
make cpu-8th   # 8vo orden - Más preciso
```

---

## 🚀 Ejecución

### Ejecución Simple (un solo proceso)
```bash
./cpu-4th < phi-GPU4.cfg
./cpu-6th < phi-GPU6.cfg
./cpu-8th < phi-GPU8.cfg
```

### Ejecución con MPI (múltiples procesos)
```bash
# 4 procesos MPI
mpirun -n 4 ./cpu-4th < phi-GPU4.cfg

# 8 procesos MPI
mpirun -n 8 ./cpu-6th < phi-GPU6.cfg
```

### Optimización para Mac M1

Para mejor rendimiento, ajusta el número de hilos OpenMP:

```bash
# Usar todos los cores (ejemplo: M1 tiene 8 cores)
export OMP_NUM_THREADS=8
./cpu-4th < phi-GPU4.cfg

# O distribuir entre procesos MPI
# Ejemplo: M1 con 8 cores → 4 procesos × 2 hilos cada uno
export OMP_NUM_THREADS=2
mpirun -n 4 ./cpu-4th < phi-GPU4.cfg
```

**Detecta cuántos cores tienes:**
```bash
sysctl -n hw.ncpu  # Muestra el número total de cores
```

---

## 📊 Visualización de Resultados

El script `visualize.py` te permite ver los resultados de la simulación.

### Ver un snapshot específico
```bash
python3 visualize.py snapshot 0000.dat
```

Esto abre una ventana con una visualización 3D de las 5120 partículas en el tiempo t=0.

### Generar imágenes de todos los snapshots
```bash
python3 visualize.py all
```

Crea archivos PNG:
- `snapshot_0000.png` - Estado inicial (t=0)
- `snapshot_0001.png` - Estado final (t=1)
- etc.

### Graficar conservación de energía
```bash
python3 visualize.py energy
```

Genera `energy_conservation.png` mostrando el error de energía ΔE vs tiempo.

---

## 📁 Archivos Generados

Después de ejecutar la simulación, encontrarás:

```
N-Body-CPU/
├── 0000.dat, 0001.dat, ...  [Snapshots de partículas]
├── contr.dat                [Conservación de energía/momento]
├── data.con                 [Checkpoint del estado actual]
├── snapshot_*.png           [Visualizaciones 3D (si usas visualize.py)]
└── energy_conservation.png  [Gráfico de error de energía]
```

### Formato de archivos .dat

```
0000                    # ID del snapshot
5120                    # Número de partículas
0.00000000E+00          # Tiempo actual
# Luego: id, masa, x, y, z, vx, vy, vz (una línea por partícula)
000000  1.95E-04  -0.144  0.151  0.064  -0.073 -0.688 -1.093
000001  1.95E-04   0.566  1.019 -1.432  -0.044 -0.570 -0.283
...
```

---

## ⚙️ Configuración

Edita los archivos `.cfg` para ajustar la simulación:

```bash
# phi-GPU4.cfg (ejemplo)
eps         1.0E-04      # Parámetro de suavizado gravitacional
t_end       1.0          # Tiempo final de simulación
dt_disk     1.0          # Intervalo entre snapshots
dt_contr    0.125        # Intervalo de salida de energía
eta         0.15         # Parámetro de timestep adaptivo
```

**Parámetros clave:**
- `eps`: Suavizado gravitacional (evita singularidades cuando partículas están muy cerca)
- `t_end`: Duración total de la simulación
- `dt_disk`: Frecuencia de guardado de snapshots (menor = más archivos .dat)
- `eta`: Control de precisión del timestep adaptivo (menor = más preciso pero más lento)

---

## 🧪 Ejemplo de Uso Completo

```bash
# 1. Compilar
make cpu-4th

# 2. Ejecutar simulación (usando 4 cores)
export OMP_NUM_THREADS=4
./cpu-4th < phi-GPU4.cfg

# 3. Visualizar resultados
python3 visualize.py all          # Crear imágenes de todas las snapshots
python3 visualize.py energy       # Graficar conservación de energía
open snapshot_0000.png            # Ver resultado inicial
open snapshot_0001.png            # Ver resultado final
open energy_conservation.png      # Ver error de energía
```

---

## 🔍 Verificar Instalación

Para verificar que todo esté instalado correctamente:

```bash
# Verificar compiladores y MPI
which mpicxx           # Debe mostrar: /opt/homebrew/bin/mpicxx
mpicxx --version       # Debe mostrar: Apple clang version...

# Verificar OpenMP
brew list libomp       # Debe mostrar archivos instalados

# Verificar Python y bibliotecas
python3 --version      # Debe mostrar: Python 3.x.x
python3 -c "import numpy, matplotlib; print('OK')"  # Debe imprimir: OK

# Probar compilación
make cpu-4th           # Debe compilar sin errores
```

---

## 📈 Rendimiento Esperado

En un Mac M1 (8 cores):

| Versión | Partículas | Tiempo (seg) | GFLOPS |
|---------|-----------|--------------|---------|
| cpu-4th | 5,120     | ~18 seg      | ~90     |
| cpu-6th | 5,120     | ~25 seg      | ~75     |
| cpu-8th | 5,120     | ~35 seg      | ~65     |

**Nota:** El rendimiento depende del número de cores y de la configuración `OMP_NUM_THREADS`.

---

## 🐛 Solución de Problemas

### Error: "mpicxx: command not found"
```bash
brew install open-mpi
```

### Error: "unsupported option '-fopenmp'"
```bash
brew install libomp
# Luego el Makefile debería detectar automáticamente la ubicación
```

### Error: "No module named 'matplotlib'"
```bash
pip3 install matplotlib numpy
```

### Las visualizaciones no se abren
```bash
# En Mac, usa 'open' para abrir imágenes
open snapshot_0000.png
open energy_conservation.png
```

### Advertencia: "sprintf is deprecated"
Esto es solo una advertencia de seguridad y no afecta la ejecución. El código funciona correctamente.

---

## 📚 Recursos Adicionales

- **Manual de Open MPI**: https://www.open-mpi.org/doc/
- **Matplotlib Docs**: https://matplotlib.org/stable/gallery/index.html
- **Hermite Integration**: Método numérico de alta precisión para N-Body

---

## 💡 Tips

1. **Usa el 4to orden** para pruebas rápidas y el 8vo orden para resultados publicables
2. **Ajusta `dt_disk`** para controlar cuántos snapshots se guardan
3. **Monitora `contr.dat`** para verificar que la energía se conserve (ΔE ≈ 0)
4. **Para muchas partículas** (>50k), considera usar múltiples procesos MPI
5. **Rota las visualizaciones 3D** en modo interactivo cambiando `save=False` en el script

---

## ✨ Todo está listo!

Tu entorno está completamente configurado. Ejecuta:

```bash
make cpu-4th && ./cpu-4th < phi-GPU4.cfg && python3 visualize.py all
```

Y en ~20 segundos tendrás una simulación completa con visualizaciones! 🎉

---
<br>

### 🏫 Información Académica

**Universidad de Ingeniería y Tecnología - UTEC**  
*Maestría en Ciencia de Datos e Inteligencia Artificial*

**Curso:** Applied High Performance Computing  
**Profesor:** Jose Antonio Fiestas Iquira  

**👥 Integrantes:**
- Morocho Caballero, Rodolfo
- Ramirez Martel, Max Houston
- Velasquez Santos, Alberto Valentin
