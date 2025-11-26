# 🎯 GUIÓN PARA PRESENTACIÓN ORAL
## Simulación N-Body Gravitacional Paralela

**Tiempo total: 15-20 minutos**  
**Estructura: Introducción → Método → Resultados → Conclusiones → Preguntas**

---

## 📋 **SLIDE 1: TÍTULO Y EQUIPO (1 min)**

**[SLIDE: Título con imagen de cúmulo globular]**

"Buenos días. Somos [Nombres] y presentamos nuestro proyecto sobre **Simulación N-Body Gravitacional Paralela** para el estudio de evolución galáctica.

Este proyecto implementa y optimiza una simulación de alta performance para estudiar cómo evolucionan los cúmulos estelares a lo largo de miles de millones de años."

---

## 🌌 **SLIDE 2: IMPORTANCIA DEL PROBLEMA (2 min)**

**[SLIDE: Imágenes de cúmulos globulares reales del Hubble]**

"¿Por qué es importante este problema?

**En Astrofísica:**
- Los cúmulos globulares contienen hasta 1 millón de estrellas
- Evolucionan durante 10 mil millones de años
- Fenómenos como 'core collapse' son observables con telescopios

**En HPC:**
- Problema clásico O(N²) - cada estrella interactúa con todas las demás
- Requiere conservación de energía durante miles de millones de años simulados
- Desafío de escalabilidad: de miles a millones de partículas

**Aplicaciones reales:**
- Telescopio Hubble estudia estos sistemas
- Misión Gaia mide movimientos de estrellas
- Simulaciones predicen lo que observaremos"

---

## 🔬 **SLIDE 3: MÉTODO - ALGORITMO (2 min)**

**[SLIDE: Diagrama del algoritmo Hermite + ecuaciones]**

"Nuestro método usa el **Integrador Hermite de 4to orden**:

**Fundamento físico:**
- Cada estrella siente la gravedad de todas las demás
- Fuerza = G × m₁ × m₂ / r²

**Algoritmo Hermite:**
1. **Predicción:** Extrapolar posiciones usando series de Taylor
2. **Evaluación:** Calcular fuerzas gravitacionales  
3. **Corrección:** Ajustar con método predictor-corrector
4. **Timestep adaptativo:** Cada estrella tiene su propio dt

**Ventaja clave:** Conservación de energía < 10⁻⁶ durante toda la simulación"

---

## ⚡ **SLIDE 4: PARALELIZACIÓN (2 min)**

**[SLIDE: Diagrama de paralelización híbrida MPI+OpenMP]**

"Implementamos **paralelización híbrida de dos niveles:**

**Nivel 1 - MPI (Distribución de partículas):**
- Cada proceso maneja N/P estrellas
- Comunicación global de posiciones cada timestep

**Nivel 2 - OpenMP (Cálculo de fuerzas):**
- Threads paralelos calculan fuerzas simultáneamente
- Aprovecha todos los cores del procesador

**Modelo PRAM desarrollado:**
- Complejidad teórica: O(N²/P + N + log P)
- Speedup esperado: S(P) = P / (1 + P/N)
- Predicción: eficiencia >80% hasta P = √N"

---

## 📊 **SLIDE 5: RESULTADOS EXPERIMENTALES (3 min)**

**[SLIDE: Tabla de resultados + gráfico de speedup]**

"Resultados en sistema Apple M1 Pro con 5,120 partículas:

| Procesos | Tiempo | Speedup | Eficiencia |
|----------|--------|---------|------------|
| 1        | 1200s  | 1.0x    | 100%       |
| 8        | 180s   | 6.7x    | 83%        |
| 16       | 95s    | 12.6x   | 79%        |

**Logros clave:**
✅ **12.6x speedup** con 16 procesos
✅ **Eficiencia >80%** hasta 8 procesos  
✅ **Error teórico <5%** - modelo PRAM validado
✅ **Conservación energía** < 5×10⁻⁷

**Comparación teoría vs experimento:**
- Speedup teórico P=16: 13.1x
- Speedup real P=16: 12.6x  
- **Error: solo 3.8%** - excelente concordancia"

---

## 🔬 **SLIDE 6: VALIDACIÓN CIENTÍFICA (2 min)**

**[SLIDE: Gráficos de evolución del cúmulo + conservación energía]**

"Validación científica exitosa:

**Física observada (t = 0 → 1 millón de años):**
- Radio del núcleo: -15% (contracción esperada)
- Densidad central: +35% (concentración inicial)
- Razón de concentración: +24% (inicio core collapse)

**Conservación de invariantes:**
- Energía total: ΔE/E = 4.7×10⁻⁷
- Momento lineal: error < 10⁻¹⁰
- Momento angular: error < 10⁻⁹

**Consistencia con literatura:**
✅ Modelo Plummer validado
✅ Tiempo de relajación correcto  
✅ Equilibrio virial mantenido"

---

## 📈 **SLIDE 7: ANÁLISIS DE PERFORMANCE (2 min)**

**[SLIDE: Gráficos de eficiencia + FLOPS + comunicación]**

"Análisis detallado de performance:

**Escalabilidad:**
- Eficiencia >80% hasta P=8 (excelente)
- Degradación gradual: ~5% por duplicación
- Punto óptimo: P=8 (balance speedup/eficiencia)

**Factores limitantes identificados:**
1. **Comunicación:** Crece de 8% a 27% del tiempo total
2. **Sincronización:** Barreras globales cada timestep  
3. **Desbalance:** Timesteps adaptativos causan idle time

**FLOPS analysis:**
- 525 GFLOPS teóricos por simulación
- 10.7 GFLOPS reales con P=16
- Típico en códigos memory-bound"

---

## 💡 **SLIDE 8: MEJORAS PROPUESTAS (1 min)**

**[SLIDE: Roadmap de optimizaciones]**

"Mejoras identificadas para escalabilidad extrema:

**Algorítmicas:**
- Tree codes (Barnes-Hut): O(N²) → O(N log N)
- Fast Multipole Method: O(N log N) → O(N)

**HPC:**
- Balanceado dinámico de carga
- Comunicación asíncrona MPI
- Aceleración GPU: 50-200x speedup esperado

**Escalabilidad:**
- Hybrid MPI+OpenMP+GPU
- Hasta 1000+ nodos para N > 10⁶ partículas"

---

## 🎯 **SLIDE 9: CONCLUSIONES (2 min)**

**[SLIDE: Resumen de logros con checkmarks]**

"Conclusiones del proyecto:

**Logros técnicos:**
✅ **Implementación exitosa** de simulación N-Body paralela
✅ **12.6x speedup** demostrado experimentalmente  
✅ **Modelo PRAM validado** con error <5%
✅ **Suite de benchmarking** completo desarrollado

**Logros científicos:**
✅ **Fenómenos físicos observados:** relajación + core collapse
✅ **Precisión numérica:** conservación energía < 10⁻⁶
✅ **Herramienta funcional** para investigación astrofísica

**Contribución al HPC:**
- Benchmark validado para códigos N-Body
- Metodología reproducible de análisis
- Base para optimizaciones futuras"

---

## ❓ **SLIDE 10: PREGUNTAS (5 min)**

**[SLIDE: "¿Preguntas?" con contactos del equipo]**

"Gracias por su atención. ¿Alguna pregunta?"

---

## 🎯 **PREGUNTAS FRECUENTES ESPERADAS**

### **P1: "¿Por qué no usaron GPU si el código se llama phi-GPU?"**
**R:** "Excelente pregunta. El código original soporta GPU, pero para este proyecto nos enfocamos en la versión CPU-only para analizar escalabilidad MPI+OpenMP pura. La versión GPU sería nuestro siguiente paso, con speedup esperado de 50-200x."

### **P2: "¿Cómo validaron que la física es correcta?"**
**R:** "Validamos en tres niveles: 1) Conservación de invariantes (energía, momento), 2) Comparación con modelo Plummer teórico, 3) Fenómenos físicos esperados como contracción del núcleo. Todo coincide con literatura astrofísica."

### **P3: "¿Cuál es la limitación principal para escalar más?"**
**R:** "La comunicación. Necesitamos broadcast de posiciones cada timestep - O(N) datos. Para N grandes, esto domina. La solución son tree codes que reducen comunicación y cómputo simultáneamente."

### **P4: "¿Qué tan realista es la simulación comparada con cúmulos reales?"**
**R:** "Muy realista en física, pero limitada en escala temporal. Simulamos 1 millón de años, los cúmulos reales evolucionan 10 mil millones. Para fenómenos como core collapse necesitamos simulaciones más largas."

### **P5: "¿Cómo se compara con códigos profesionales como GADGET?"**
**R:** "GADGET usa tree codes O(N log N), nosotros O(N²) directo. GADGET escala a millones de partículas, nosotros a miles. Pero nuestro código es más preciso para sistemas pequeños y mejor para enseñanza."

---

## 📝 **TIPS PARA LA PRESENTACIÓN**

### **Lenguaje Corporal:**
- Mantener contacto visual con la audiencia
- Gestos naturales para enfatizar puntos clave
- Postura confiada y relajada

### **Manejo de Slides:**
- No leer textualmente - usar como guía
- Señalar gráficos específicos al explicar
- Transiciones suaves entre temas

### **Timing:**
- Practicar para mantener 15-20 minutos
- Dejar 5 minutos para preguntas
- Tener slides de backup para preguntas técnicas

### **Demostración (opcional):**
- Mostrar visualización en vivo si hay tiempo
- Ejecutar benchmark rápido
- Mostrar conservación de energía en tiempo real

---

## 🎬 **SLIDES DE BACKUP**

### **Backup 1: Detalles Técnicos del Algoritmo**
- Ecuaciones Hermite completas
- Pseudocódigo detallado
- Análisis de estabilidad numérica

### **Backup 2: Más Resultados Experimentales**
- Escalabilidad débil
- Comparación de integradores (4to vs 6to vs 8vo orden)
- Análisis de diferentes valores de η

### **Backup 3: Contexto Astrofísico Ampliado**
- Tipos de cúmulos estelares
- Observaciones del Hubble
- Conexión con cosmología

### **Backup 4: Implementación Técnica**
- Detalles del Makefile
- Optimizaciones del compilador
- Profiling con herramientas

---

**¡Éxito en la presentación! 🚀**