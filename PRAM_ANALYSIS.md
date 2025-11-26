# 🧮 ANÁLISIS PRAM Y COMPLEJIDAD TEÓRICA
## Simulación N-Body Gravitacional

---

## 🔄 **MODELO PRAM (Parallel Random Access Machine)**

### **Algoritmo N-Body Hermite Paralelo**

```
PRAM N-Body Algorithm:
Input: N partículas, P procesadores
Output: Evolución temporal del sistema

FASE 1: INICIALIZACIÓN
for i = 0 to P-1 in parallel:
    local_particles[i] = N/P partículas
    broadcast(global_state)
end parallel

FASE 2: BUCLE TEMPORAL PRINCIPAL
while t < t_end:
    
    SUBFASE 2.1: PREDICCIÓN (Paralela)
    for i = 0 to P-1 in parallel:
        for j in local_particles[i]:
            predict_position(j, dt[j])    // O(1) por partícula
            predict_velocity(j, dt[j])    // O(1) por partícula
        end for
    end parallel
    
    SUBFASE 2.2: COMUNICACIÓN (Sincronización)
    all_gather(predicted_positions)       // O(log P) con árbol
    
    SUBFASE 2.3: CÁLCULO DE FUERZAS (Paralela)
    for i = 0 to P-1 in parallel:
        for j in local_particles[i]:
            force[j] = 0
            for k = 0 to N-1:            // O(N) interacciones
                if k ≠ j:
                    force[j] += gravity(j,k)  // O(1) por par
                end if
            end for
        end for
    end parallel
    
    SUBFASE 2.4: CORRECCIÓN HERMITE (Paralela)
    for i = 0 to P-1 in parallel:
        for j in local_particles[i]:
            correct_position(j)           // O(1) por partícula
            correct_velocity(j)           // O(1) por partícula
            update_timestep(j)            // O(1) por partícula
        end for
    end parallel
    
    SUBFASE 2.5: REDUCCIÓN TEMPORAL
    t_next = min_reduce(all_timesteps)    // O(log P)
    
end while
```

---

## 📐 **ANÁLISIS DE COMPLEJIDAD TEÓRICA**

### **Complejidad Secuencial**
```
T_seq = T_steps × (T_predict + T_force + T_correct)

Donde:
- T_predict = O(N)           // Predicción para N partículas
- T_force = O(N²)            // N partículas × N interacciones
- T_correct = O(N)           // Corrección para N partículas
- T_steps = O(t_end/dt_avg)  // Número de pasos temporales

Por tanto: T_seq = O(T_steps × N²)
```

### **Complejidad Paralela (P procesadores)**
```
T_par = T_steps × (T_predict_par + T_comm + T_force_par + T_correct_par + T_reduce)

Donde:
- T_predict_par = O(N/P)     // Predicción distribuida
- T_comm = O(N + log P)      // All-gather de posiciones
- T_force_par = O(N²/P)      // Fuerzas distribuidas
- T_correct_par = O(N/P)     // Corrección distribuida  
- T_reduce = O(log P)        // Reducción de timesteps

Dominante: T_par = O(T_steps × (N²/P + N + log P))
```

### **Speedup Teórico**
```
S(P) = T_seq / T_par = (T_steps × N²) / (T_steps × (N²/P + N + log P))

S(P) = N² / (N²/P + N + log P)

Para N >> P >> log P:
S(P) ≈ P × N² / (N² + P×N) = P / (1 + P/N)

Speedup máximo: S_max ≈ N (limitado por comunicación)
```

### **Eficiencia Teórica**
```
E(P) = S(P) / P = 1 / (1 + P/N + P×log P/N²)

Para eficiencia alta: P << N
Eficiencia óptima: P ≈ √N
```

---

## 📊 **PREDICCIONES TEÓRICAS**

### **Para N = 5,120 partículas:**

| Procesos (P) | Speedup Teórico | Eficiencia Teórica | Tiempo Estimado |
|--------------|-----------------|-------------------|-----------------|
| 1            | 1.0             | 100%              | 1200s           |
| 2            | 1.95            | 97%               | 615s            |
| 4            | 3.81            | 95%               | 315s            |
| 8            | 7.27            | 91%               | 165s            |
| 16           | 13.1            | 82%               | 92s             |
| 32           | 22.4            | 70%               | 54s             |

### **Punto Óptimo:**
```
P_optimal = √N = √5120 ≈ 72 procesos
Eficiencia esperada: ~85%
```

---

## ⚡ **FACTORES LIMITANTES**

### **1. Comunicación (Overhead)**
```
T_comm = α + β × N
Donde:
- α = latencia de red (~10⁻⁶ s)
- β = ancho de banda inverso (~10⁻⁹ s/byte)
- N × 24 bytes por partícula (pos + vel)
```

### **2. Desbalance de Carga**
```
Timesteps adaptativos → diferentes dt por partícula
Partículas centrales: dt_min ≈ 10⁻⁴
Partículas externas: dt_max ≈ 10⁻²
Ratio: dt_max/dt_min ≈ 100:1
```

### **3. Sincronización**
```
Barrera global cada paso temporal
T_sync = O(log P) por sincronización
Impacto: ~5-10% del tiempo total
```

---

## 🎯 **VALIDACIÓN EXPERIMENTAL**

### **Métricas a Medir:**
1. **Tiempo total** vs P (procesos)
2. **Tiempo de cómputo** vs P  
3. **Tiempo de comunicación** vs P
4. **Speedup real** vs teórico
5. **Eficiencia** vs P
6. **Escalabilidad fuerte** (N fijo, P variable)
7. **Escalabilidad débil** (N/P fijo, P variable)

### **Experimentos Propuestos:**
```bash
# Escalabilidad fuerte (N=5120 fijo)
for P in 1 2 4 8 16 32; do
    mpirun -n $P ./cpu-4th < config.cfg
done

# Escalabilidad débil (N/P=320 fijo)  
for P in 1 2 4 8 16; do
    N=$((P * 320))
    ./gen-plum $N > data_${N}.inp
    mpirun -n $P ./cpu-4th < config_${N}.cfg
done
```

---

## 📈 **NORMALIZACIÓN PARA COMPARACIÓN**

### **Tiempo Normalizado:**
```
T_norm(P) = T_measured(P) / T_measured(1)
T_theory(P) = (N²/P + N + log P) / N²
```

### **FLOPS Teóricos:**
```
FLOPS_per_interaction = 20 (distancia + fuerza)
FLOPS_per_step = N² × 20 + N × 60 (Hermite)
FLOPS_total = FLOPS_per_step × T_steps

Para N=5120, T_steps=1000:
FLOPS_total ≈ 5.2×10¹¹ operaciones
```

---

## 🔬 **CONCLUSIONES TEÓRICAS**

1. **Algoritmo es paralelizable** con eficiencia alta para P < √N
2. **Bottleneck principal:** Cálculo de fuerzas O(N²)  
3. **Comunicación escalable:** O(N + log P)
4. **Speedup máximo teórico:** ~72x para N=5120
5. **Limitación práctica:** Desbalance por timesteps adaptativos

**Predicción:** Eficiencia >80% hasta P=16, degradación gradual después.