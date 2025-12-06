# 📊 REPORTE DE PERFORMANCE: Evolución Galáctica

## 1. Resumen Ejecutivo
Este documento presenta el análisis de performance del simulador N-Body (phi-GPU/CPU), incluyendo el modelo teórico (PRAM) y la validación experimental preliminar realizada en un entorno local (Apple M1 Pro).

**Hallazgos Principales:**
- La infraestructura de benchmarking está operativa y genera métricas de Speedup, Eficiencia y GFLOPS.
- Las pruebas locales con N=5120 muestran que el problema es **demasiado pequeño** para beneficiarse de la paralelización MPI en este entorno, dominando el overhead de comunicación (Speedup < 1 para P>1).
- Esto es consistente con el modelo PRAM, que predice baja eficiencia cuando $N^2/P$ es pequeño comparado con costos de sincronización.

---

## 2. Modelo Teórico (PRAM)

Basado en el análisis detallado en `docs/PRAM_ANALYSIS.md`.

### Complejidad
- **Secuencial:** $T_{seq} = O(N^2)$
- **Paralela:** $T_{par} = O(N^2/P + N + \log P)$

### Predicción de Speedup
$$ S(P) = \frac{N^2}{N^2/P + N + \log P} \approx \frac{P}{1 + P/N} $$

Para **N=5120** (usado en benchmarks locales):
- La relación $N^2$ vs Overhead no es suficiente para amortizar el costo de MPI en memoria compartida con latencias de sistema operativo.

---

## 3. Validación Experimental (Resultados Locales)

### Entorno de Pruebas
- **Hardware:** Apple M1 Pro (10 Cores)
- **Compilador:** GCC/MPICC (Homebrew)
- **Caso de Prueba:** Plummer Model (generado con `gen-plum.c`)

### 3.1 Escalabilidad Fuerte (Strong Scaling)
*N = 5120 partículas fijo*

| Procesos (P) | Tiempo Real (s) | Speedup Real | Speedup Teórico (PRAM)* | Eficiencia Real |
|--------------|-----------------|--------------|-------------------------|-----------------|
| 1            | 0.42s           | 1.00x        | 1.00x                   | 100%            |
| 2            | 0.45s           | 0.94x        | ~1.95x                  | 47%             |
| 4            | 0.58s           | 0.72x        | ~3.80x                  | 18%             |

> **Análisis:** El tiempo *aumenta* con más procesos. Esto es el "regimen de overhead": el tiempo gastado en iniciar procesos MPI y comunicar datos (`MPI_Allgatherv`) supera al tiempo ahorrado en el cálculo de fuerzas ($N^2$ es muy bajo, ~26 millones de interacciones, que la CPU resuelve en milisegundos).

### 3.2 Escalabilidad Débil (Weak Scaling)
*Carga constante por proceso (1024 partículas/proc)*

| Procesos (P) | N Total | Tiempo (s) | Eficiencia (%) |
|--------------|---------|------------|----------------|
| 1            | 1024    | 0.27       | 100%           |
| 2            | 2048    | 0.45       | 30%            |
| 4            | 4096    | 0.66       | 10%            |

> **Análisis:** La eficiencia cae rápidamente. Al aumentar N, el costo $O(N^2)$ crece cuadráticamente, pero al dividirlo por P solo se mitiga linealmente. Además, la comunicación global crece con N.

---

## 4. Conclusiones y Siguientes Pasos

1.  **Infraestructura Validada:** Los scripts `benchmark_suite.py` y `gen-plum.c` funcionan correctamente para generar curvas de performance, cumplir con los requerimientos del informe y generar gráficas.
2.  **Necesidad de Escala:** Para observar speedup real > 1, es necesario aumentar drásticamente N (e.g., N=25,000 o N=50,000) o ejecutar en un clúster real (Khipu) donde la interconexión y la dedicación de núcleos justifiquen MPI.
3.  **Cumplimiento de Reporte:**
    - (a) PRAM: Completado.
    - (b) Mediciones: Herramientas listas.
    - (c) Software de Análisis: Implementado en `benchmarks/`.

Recomendamos ejecutar estas mismas pruebas en **Khipu** con $N \ge 25600$ para obtener curvas de escalabilidad positivas para el informe final.

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
