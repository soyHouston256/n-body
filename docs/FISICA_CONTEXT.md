# 🌌 Contexto Físico: Simulación N-Body Gravitacional

## ¿Qué Estás Simulando?

Estás simulando la **evolución dinámica de un cúmulo estelar** bajo la influencia de la gravedad mutua entre todas las partículas. Cada partícula representa una **estrella** o un grupo de estrellas.

---

## 🔭 Aplicaciones Astronómicas

### Cúmulos Globulares
Los sistemas más estudiados con este código:

| Cúmulo Real | Estrellas | Edad (años) | Masa Solar |
|-------------|-----------|-------------|------------|
| **M13** (Hércules) | 300,000 | 11 mil millones | ~600,000 M☉ |
| **47 Tucanae** | 1,000,000 | 12 mil millones | ~700,000 M☉ |
| **Omega Centauri** | 10,000,000 | 12 mil millones | ~4 millones M☉ |
| **M15** | 100,000 | 12 mil millones | ~500,000 M☉ |

Tu simulación (5,120 partículas) = **cúmulo pequeño** o **región de un cúmulo grande**

### Otros Sistemas
- **Cúmulos abiertos** (Pléyades, Híades)
- **Núcleos galácticos**
- **Cúmulos de galaxias** (escala cosmológica)
- **Discos galácticos**

---

## 📐 Modelo Plummer

Tu condición inicial es un **modelo Plummer (1911)**:

```
ρ(r) = (3M/4πa³) × (1 + r²/a²)^(-5/2)
```

**Características:**
- Distribución esférica simétrica
- Densidad máxima en el centro
- Caída suave hacia el exterior (no tiene borde definido)
- Sistema en **equilibrio virial**: 2K + U = 0 (K=cinética, U=potencial)

**Ventajas:**
- Matemáticamente simple
- Aproxima bien cúmulos globulares observados
- Estable durante tiempos largos

---

## ⏱️ Escalas de Tiempo

### Unidades N-Body → Físicas

Para un cúmulo típico:
```
1 unidad de tiempo = 1 Myr (millón de años)
1 unidad de longitud = 1 pc (parsec ≈ 3.26 años luz)
1 unidad de velocidad = 1 km/s
1 unidad de masa = 10⁵ masas solares
```

**Tu simulación actual:**
- t=0 → t=1.0 = **1 millón de años**
- ¡Muy corto! Los cúmulos viven 10 mil millones de años

### Tiempos Característicos

| Tiempo | Símbolo | Valor (N=5120) | Fenómeno |
|--------|---------|----------------|----------|
| **Tiempo de cruce** | t_cross = R/v | ~0.1 | Una estrella cruza el cúmulo |
| **Tiempo de relajación** | t_relax ≈ N/10ln(N) | ~60 | Sistema "termaliza" |
| **Tiempo de core collapse** | t_cc ≈ 15 t_relax | ~900 | Núcleo colapsa |
| **Tiempo de evaporación** | t_evap ≈ 100 t_relax | ~6000 | Cúmulo se disuelve |

**¡Por eso solo viste cambios pequeños con t=1!**

---

## 🔬 Fenómenos Físicos Observables

### 1. Relajación Gravitacional (t ~ 10-100)

**¿Qué es?**
Las estrellas intercambian energía mediante encuentros gravitacionales:
- Inicialmente: distribución artificial (modelo Plummer perfecto)
- Gradualmente: el sistema "olvida" condiciones iniciales
- Eventualmente: estado de "cuasi-equilibrio" térmico

**Análogo:** Gas de partículas, pero con gravedad de largo alcance

**Observable:**
- Dispersión de velocidades se uniformiza
- Partículas con alta energía migran al exterior
- Partículas con baja energía caen al centro

### 2. Segregación de Masas (t ~ 50-200)

**Si hubiera diferentes masas:**
- **Equipartición de energía**: ½m₁v₁² = ½m₂v₂²
- Objetos masivos se mueven **más lento** pero tienen más energía
- Objetos masivos **caen al centro** (hunden hacia el núcleo)
- Objetos ligeros son **expulsados** hacia el exterior

**En cúmulos reales:**
- Centro: gigantes rojas, estrellas de neutrones, agujeros negros
- Periferia: enanas rojas, enanas blancas

**Tu simulación:** Todas las masas iguales → no verás esto (pero sí el proceso general)

### 3. Core Collapse (t ~ 100-1000)

**El fenómeno más dramático:**

```
Estado inicial:  ●●●●●○○○○
                  ↓
Relajación:      ●●●●●●○○○
                  ↓
Core collapse:   ●●●●●●●●○    (núcleo muy denso)
                  ↓
Post-collapse:   ●●●○○○○○○○  (halo expandido)
```

**Proceso:**
1. Encuentros gravitacionales transfieren energía hacia fuera
2. Núcleo pierde energía → **se contrae** (gravedad colapsa)
3. Densidad central aumenta exponencialmente
4. Formación de **binarias duras** (estrellas dobles muy ligadas)
5. Binarias inyectan energía → **detienen el colapso**

**Observable:**
- Radio del núcleo (r_core) disminuye
- Densidad central aumenta 10-100x
- Razón de concentración (r_half/r_core) aumenta de ~5 a ~20+

**En cúmulos reales:**
- M15, M30 ya experimentaron core collapse
- Observable: núcleo muy brillante y compacto

### 4. Evaporación (t ~ 500+)

**¿Por qué se evapora un cúmulo?**
- Algunos encuentros dan energía suficiente para **escapar**
- Partículas con v > v_escape se pierden
- El cúmulo gradualmente pierde masa
- Radio de marea disminuye con la masa → más evaporación

**Observable:**
- Número de partículas disminuye
- Radio externo (r_tidal) aumenta
- Halo difuso alrededor del núcleo
- Eventualmente: disolución completa

**En cúmulos reales:**
- Cúmulos cerca del centro galáctico se evaporan más rápido
- Fuerza de marea de la galaxia acelera evaporación

### 5. Formación de Binarias

**Encuentros de 3 cuerpos:**
```
   A  +  B  +  C  →  (AB binaria ligada)  +  C_escape
```

- Una estrella escapa con alta velocidad
- Dos estrellas quedan ligadas (binaria)
- Binaria se contrae al intercambiar energía con otras estrellas
- **Fuente de energía** que calienta el cúmulo

**Importancia:**
- Detienen el core collapse
- Permiten que el cúmulo sobreviva ~10 Gyr
- Dominan la dinámica del núcleo post-collapse

---

## 📊 Qué Medir en la Simulación

### 1. **Radio del Núcleo (r_core)**
Radio que contiene el 10% de las partículas más centrales
- **Disminuye** durante core collapse
- **Aumenta** si hay calentamiento (binarias)

### 2. **Radio Medio (r_half)**
Radio que contiene el 50% de la masa
- Indicador de tamaño global del cúmulo
- Relativamente constante en equilibrio
- Aumenta durante evaporación

### 3. **Radio de Marea (r_tidal)**
Radio que contiene el 90% de las partículas
- Marca el límite del cúmulo
- Aumenta cuando hay evaporación

### 4. **Razón de Concentración (c = r_half / r_core)**
- **c < 10**: Cúmulo normal
- **c ~ 10-20**: Pre-core-collapse
- **c > 20**: Post-core-collapse (núcleo muy denso)

### 5. **Dispersión de Velocidades (σ_v)**
- Indica "temperatura" del cúmulo
- σ_v² ∝ energía cinética promedio
- Aumenta si hay calentamiento

### 6. **Densidad Central (ρ_c)**
- Aumenta exponencialmente durante core collapse
- Puede aumentar 100-1000x

---

## 🧪 Experimentos Recomendados

### Experimento 1: Evolución a Largo Plazo
```bash
./cpu-4th < phi-long-evolution.cfg
python3 analyze_evolution.py
```
- Simula t=0 → t=50 (~50 millones de años)
- Genera 20 snapshots
- Analiza evolución de radios, densidad, velocidades
- **Tiempo:** ~15-20 minutos

**Qué esperar:**
- Relajación inicial (t<10)
- Inicio de contracción del núcleo (t~20-40)
- Posible inicio de core collapse (t>40)

### Experimento 2: Comparar Integradores
```bash
make cpu-4th cpu-6th cpu-8th

time ./cpu-4th < phi-long-evolution.cfg
time ./cpu-6th < phi-long-evolution.cfg
time ./cpu-8th < phi-long-evolution.cfg

python3 visualize.py energy
```
- Compara conservación de energía
- Compara velocidad de ejecución
- 8vo orden debería tener mejor conservación pero ser más lento

### Experimento 3: Dependencia del Parámetro η
```bash
# Editar phi-long-evolution.cfg con diferentes η:
# η = 0.05 (muy preciso, lento)
# η = 0.10 (preciso, moderado)
# η = 0.15 (rápido, menos preciso)
# η = 0.30 (muy rápido, impreciso)
```
- η controla el tamaño del timestep
- η pequeño → pasos pequeños → más preciso → más lento
- η grande → pasos grandes → menos preciso → más rápido

---

## 📚 Referencias Científicas

### Papers Clásicos
1. **Plummer (1911)** - "On the problem of distribution..."
2. **Aarseth (1963)** - Primera simulación N-Body por computadora
3. **Hénon (1971)** - Teoría de core collapse
4. **Spitzer & Hart (1971)** - Evaporación de cúmulos

### Libros
- **Binney & Tremaine (2008)** - "Galactic Dynamics"
- **Heggie & Hut (2003)** - "The Gravitational Million-Body Problem"

### Observaciones
- Telescopio Hubble: imágenes de cúmulos globulares
- Gaia: mediciones de movimientos propios de estrellas

---

## 💡 Interpretación de Resultados

### Estado Estable (Equilibrio Virial)
```
✅ r_core, r_half, r_tidal ~ constantes
✅ ΔE/E < 10⁻⁶ (buena conservación de energía)
✅ Concentración c ~ constante
```

### Pre-Core-Collapse
```
⚠️ r_core disminuyendo lentamente
⚠️ Densidad central aumentando
⚠️ Concentración c aumentando
```

### Core Collapse
```
🚨 r_core disminuye exponencialmente
🚨 Densidad central aumenta >10x
🚨 Concentración c > 20
```

### Post-Collapse / Evaporación
```
📉 Número de partículas disminuye
📉 r_tidal aumenta (halo)
📉 r_half aumenta lentamente
```

---

## 🎯 Próximo Paso: Ejecutar Simulación Larga

Para ver fenómenos reales, ejecuta:

```bash
# Simulación larga (t=50, ~15-20 minutos)
./cpu-4th < phi-long-evolution.cfg

# Análisis de evolución
python3 analyze_evolution.py

# Ver snapshots individuales
python3 visualize.py snapshot 0000.dat
python3 visualize.py snapshot 0010.dat
python3 visualize.py snapshot 0019.dat
```

¡Esto te mostrará la física real de la evolución dinámica! 🌌

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
