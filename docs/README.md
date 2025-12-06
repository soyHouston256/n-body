# N-Body Simulation - Versión CPU-Only

Esta carpeta contiene solo los archivos necesarios para ejecutar el simulador N-Body usando **CPU únicamente** (sin GPU/CUDA).

## 📖 Guías de Instalación

- **[Mac M1/M2/M3](INSTALL_MAC.md)** - Guía completa para Mac con Apple Silicon (✅ Instalado y funcionando)
- **Linux** - Usa el Makefile directamente (requiere `mpicxx` y `libomp`)

## 📊 Visualización

Incluye `visualize.py` - Script Python para visualizar resultados:
```bash
python3 visualize.py snapshot 0000.dat   # Ver snapshot específico
python3 visualize.py all                 # Generar todas las imágenes
python3 visualize.py energy              # Graficar conservación de energía
```

## Archivos Incluidos

### Código Fuente
- `phi-GPU.cpp` - Motor principal de simulación
- `hermite4.h` - Integrador Hermite de 4to orden (CPU)
- `hermite6.h` - Integrador Hermite de 6to orden (CPU)
- `hermite8.h` - Integrador Hermite de 8vo orden (CPU)
- `vector3.h` - Matemáticas de vectores 3D
- `taylor.h` - Expansión de series de Taylor

### Configuración y Datos
- `phi-GPU4.cfg` - Configuración para 4to orden
- `phi-GPU6.cfg` - Configuración para 6to orden
- `phi-GPU8.cfg` - Configuración para 8vo orden
- `data.inp` - Datos de entrada (5120 partículas del modelo Plummer)

### Sistema de Compilación
- `Makefile` - Compilación simplificada para CPU

## Dependencias

Solo necesitas:
- **MPI** (Message Passing Interface) - Para paralelización distribuida
- **Compilador C++** compatible con C++11 o superior
- **OpenMP** - Para paralelización multi-hilo (incluido en GCC/Clang moderno)

**NO necesitas:**
- ❌ CUDA toolkit
- ❌ GPU NVIDIA
- ❌ Drivers de GPU

## Compilación

```bash
# Compilar todas las versiones
make all

# O compilar individualmente
make cpu-4th   # 4to orden (más rápido, menos preciso)
make cpu-6th   # 6to orden (balance)
make cpu-8th   # 8vo orden (más lento, más preciso)
```

## Ejecución

### Ejecución Simple (un solo proceso)
```bash
./cpu-4th < phi-GPU4.cfg
```

### Ejecución con MPI (múltiples procesos)
```bash
# Usar 4 procesos MPI
mpirun -n 4 ./cpu-4th < phi-GPU4.cfg

# Usar 8 procesos MPI
mpirun -n 8 ./cpu-6th < phi-GPU6.cfg
```

### Ejecución con Make
```bash
make run-4th        # Ejecutar versión 4to orden
make run-mpi-4th    # Ejecutar con MPI (4 procesos)
```

## Configuración

Edita los archivos `phi-GPU*.cfg` para ajustar:

```
eps         1.0E-04      # Parámetro de suavizado
t_end       1.0          # Tiempo final de simulación
dt_disk     1.0          # Intervalo de snapshots
dt_contr    0.125        # Intervalo de salida de energía
eta         0.15         # Parámetro de timestep adaptivo
```

## Salidas

El simulador genera:
- `0000.dat, 0001.dat, ...` - Snapshots de partículas (cada dt_disk)
- `contr.dat` - Conservación de energía/momento
- `data.con` - Checkpoint del estado actual

## Rendimiento

### Comparación de Órdenes de Integración

| Orden | FLOPS/partícula | Precisión | Velocidad |
|-------|-----------------|-----------|-----------|
| 4to   | 60             | O(h⁴)     | ⚡⚡⚡     |
| 6to   | 97             | O(h⁶)     | ⚡⚡       |
| 8vo   | 144            | O(h⁸)     | ⚡         |

### Paralelización

El código usa:
- **MPI**: Paralelización entre nodos/procesos
- **OpenMP**: Paralelización multi-hilo en cada proceso

Para mejor rendimiento:
```bash
# Ejemplo: máquina con 8 cores
export OMP_NUM_THREADS=8
mpirun -n 1 ./cpu-4th < phi-GPU4.cfg

# O distribuir en 2 procesos con 4 hilos cada uno
export OMP_NUM_THREADS=4
mpirun -n 2 ./cpu-4th < phi-GPU4.cfg
```

## Características del Simulador

- **Integrador Hermite**: Alta precisión para dinámica gravitacional
- **Timesteps adaptativos**: Cada partícula tiene su propio paso de tiempo
- **Integración individual**: Partículas rápidas usan pasos más pequeños
- **Conservación de energía**: Monitoreo automático de errores numéricos
- **Escalable**: Hasta ~1 millón de partículas

## Notas

- El archivo `phi-GPU.cpp` contiene código tanto CPU como GPU, pero cuando se compila sin `-DGPU`, solo se usa el código CPU
- Las versiones CPU usan precisión doble, mientras que las GPU usan precisión simple con acumulación float2
- Los timesteps adaptativos son clave para el rendimiento: partículas cercanas tienen pasos pequeños, partículas lejanas tienen pasos grandes


#comando usado 
rsync -avz max.ramirez@khipu.utec.edu.pe:~/n-body/outputs/ /Users/maxhoustonramirezmartel/code/utec/hpc/N-Body-CPU/outputs/


#ignoramos git porque es algo que no queremos correr 
rsync -avz --exclude='.git' --exclude='.DS_Store' /Users/maxhoustonramirezmartel/code/utec/hpc/N-Body-CPU/ max.ramirez@khipu.utec.edu.pe:/home/max.ramirez/n-body/



rsync -avz max.ramirez@khipu.utec.edu.pe:~/n-body/outputs/ /Users/maxhoustonramirezmartel/code/utec/hpc/N-Body-CPU/outputs/

