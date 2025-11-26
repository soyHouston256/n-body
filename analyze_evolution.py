#!/usr/bin/env python3
"""
Análisis de Evolución del Cúmulo N-Body
Muestra cómo cambian las propiedades físicas con el tiempo
"""

import numpy as np
import matplotlib.pyplot as plt
import glob

def read_snapshot(filename):
    """Lee un snapshot y retorna datos de partículas"""
    with open(filename, 'r') as f:
        lines = f.readlines()

    snapshot_id = int(lines[0].strip())
    n_particles = int(lines[1].strip())
    time = float(lines[2].strip())

    particles = []
    for i in range(3, len(lines)):
        data = lines[i].split()
        if len(data) >= 8:
            particles.append([
                int(data[0]),      # id
                float(data[1]),    # mass
                float(data[2]),    # x
                float(data[3]),    # y
                float(data[4]),    # z
                float(data[5]),    # vx
                float(data[6]),    # vy
                float(data[7])     # vz
            ])

    return snapshot_id, n_particles, time, np.array(particles)

def analyze_cluster(particles):
    """
    Calcula propiedades físicas del cúmulo:
    - Radio del núcleo (core radius)
    - Radio medio
    - Radio de marea (tidal radius)
    - Dispersión de velocidades
    - Densidad central
    """
    # Posiciones y velocidades
    pos = particles[:, 2:5]
    vel = particles[:, 5:8]

    # Distancias desde el centro
    r = np.sqrt(np.sum(pos**2, axis=1))

    # Velocidades
    v = np.sqrt(np.sum(vel**2, axis=1))

    # Radio que contiene el 10% de las partículas (core radius)
    r_sorted = np.sort(r)
    n_10 = int(0.1 * len(r))
    r_core = r_sorted[n_10]

    # Radio medio (half-mass radius)
    n_50 = int(0.5 * len(r))
    r_half = r_sorted[n_50]

    # Radio que contiene el 90% (tidal radius aproximado)
    n_90 = int(0.9 * len(r))
    r_tidal = r_sorted[n_90]

    # Dispersión de velocidades
    v_mean = np.mean(v)
    v_std = np.std(v)

    # Densidad central (partículas dentro de r_core)
    n_core = np.sum(r < r_core)
    volume_core = (4/3) * np.pi * r_core**3
    density_core = n_core / volume_core if volume_core > 0 else 0

    return {
        'r_core': r_core,
        'r_half': r_half,
        'r_tidal': r_tidal,
        'v_mean': v_mean,
        'v_std': v_std,
        'density_core': density_core,
        'r_max': r.max(),
        'r_mean': r.mean()
    }

def plot_evolution():
    """
    Grafica la evolución temporal del cúmulo
    """
    snapshot_files = sorted(glob.glob('[0-9][0-9][0-9][0-9].dat'))

    if len(snapshot_files) < 2:
        print("Se necesitan al menos 2 snapshots para ver evolución")
        return

    print(f"Analizando {len(snapshot_files)} snapshots...")

    # Arrays para almacenar evolución temporal
    times = []
    r_cores = []
    r_halfs = []
    r_tidals = []
    v_stds = []
    densities = []
    n_particles = []

    for filename in snapshot_files:
        snap_id, n_parts, time, particles = read_snapshot(filename)
        props = analyze_cluster(particles)

        times.append(time)
        r_cores.append(props['r_core'])
        r_halfs.append(props['r_half'])
        r_tidals.append(props['r_tidal'])
        v_stds.append(props['v_std'])
        densities.append(props['density_core'])
        n_particles.append(n_parts)

        print(f"t={time:.2f}: r_core={props['r_core']:.3f}, "
              f"r_half={props['r_half']:.3f}, σ_v={props['v_std']:.3f}")

    times = np.array(times)
    r_cores = np.array(r_cores)
    r_halfs = np.array(r_halfs)
    r_tidals = np.array(r_tidals)
    v_stds = np.array(v_stds)
    densities = np.array(densities)

    # Crear gráficos
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    # 1. Evolución de radios
    ax = axes[0, 0]
    ax.plot(times, r_cores, 'b-', linewidth=2, label='Radio del núcleo (10%)')
    ax.plot(times, r_halfs, 'g-', linewidth=2, label='Radio medio (50%)')
    ax.plot(times, r_tidals, 'r-', linewidth=2, label='Radio externo (90%)')
    ax.set_xlabel('Tiempo', fontsize=12)
    ax.set_ylabel('Radio', fontsize=12)
    ax.set_title('Evolución de la Estructura del Cúmulo', fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)

    # 2. Densidad central
    ax = axes[0, 1]
    ax.plot(times, densities / densities[0], 'purple', linewidth=2)
    ax.set_xlabel('Tiempo', fontsize=12)
    ax.set_ylabel('Densidad Central (normalizada)', fontsize=12)
    ax.set_title('Concentración del Núcleo', fontsize=14)
    ax.grid(True, alpha=0.3)

    # 3. Dispersión de velocidades
    ax = axes[1, 0]
    ax.plot(times, v_stds, 'orange', linewidth=2)
    ax.set_xlabel('Tiempo', fontsize=12)
    ax.set_ylabel('Dispersión de Velocidades σ_v', fontsize=12)
    ax.set_title('Temperatura del Cúmulo', fontsize=14)
    ax.grid(True, alpha=0.3)

    # 4. Razón de concentración (core collapse indicator)
    ax = axes[1, 1]
    concentration = r_halfs / r_cores
    ax.plot(times, concentration, 'darkred', linewidth=2)
    ax.set_xlabel('Tiempo', fontsize=12)
    ax.set_ylabel('r_half / r_core', fontsize=12)
    ax.set_title('Razón de Concentración (Core Collapse)', fontsize=14)
    ax.axhline(y=concentration[0], color='gray', linestyle='--', alpha=0.5, label='Inicial')
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.savefig('cluster_evolution.png', dpi=150, bbox_inches='tight')
    print("\n✅ Gráfico guardado: cluster_evolution.png")
    plt.show()

    # Resumen de cambios
    print("\n" + "="*60)
    print("RESUMEN DE EVOLUCIÓN")
    print("="*60)
    print(f"Tiempo simulado: {times[0]:.2f} → {times[-1]:.2f}")
    print(f"\nRadio del núcleo:")
    print(f"  Inicial: {r_cores[0]:.4f}")
    print(f"  Final:   {r_cores[-1]:.4f}")
    print(f"  Cambio:  {(r_cores[-1]/r_cores[0] - 1)*100:+.2f}%")

    print(f"\nRadio medio:")
    print(f"  Inicial: {r_halfs[0]:.4f}")
    print(f"  Final:   {r_halfs[-1]:.4f}")
    print(f"  Cambio:  {(r_halfs[-1]/r_halfs[0] - 1)*100:+.2f}%")

    print(f"\nDensidad central:")
    print(f"  Inicial: {densities[0]:.4f}")
    print(f"  Final:   {densities[-1]:.4f}")
    print(f"  Cambio:  {(densities[-1]/densities[0] - 1)*100:+.2f}%")

    print(f"\nConcentración (r_half/r_core):")
    print(f"  Inicial: {concentration[0]:.4f}")
    print(f"  Final:   {concentration[-1]:.4f}")
    print(f"  Cambio:  {(concentration[-1]/concentration[0] - 1)*100:+.2f}%")
    print("="*60)

    # Interpretación
    print("\n📊 INTERPRETACIÓN:")
    if concentration[-1] > concentration[0] * 1.2:
        print("⚠️  El cúmulo está experimentando CORE COLLAPSE")
        print("   El núcleo se contrae mientras el halo se expande")
    elif r_cores[-1] < r_cores[0] * 0.9:
        print("📉 El núcleo se está contrayendo (segregación de masas)")
    elif r_tidals[-1] > r_tidals[0] * 1.1:
        print("📈 El cúmulo se está expandiendo (evaporación)")
    else:
        print("✅ El cúmulo permanece en equilibrio virial")

if __name__ == '__main__':
    plot_evolution()
