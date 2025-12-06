import matplotlib.pyplot as plt
import numpy as np
import os

# Khipu Weak Scaling Data
# P = Processors
# N = Particles (scaled P * 4096)
P = np.array([1, 2, 4, 8, 16, 32])
N = np.array([4096, 8192, 16384, 32768, 65536, 131072])

# Extracted from logs
Time = np.array([3.1688, 7.0380, 14.754, 33.359, 79.616, 278.78])
GFLOPS = np.array([10.496, 20.196, 40.423, 78.258, 141.676, 176.382])

# Ideal Time (Linear Scaling for O(N^2))
# Work ~ N^2. Power ~ P. N_new = P*N_base.
# Time ~ (P*N)^2 / P = P * N^2 = P * Time_base
Time_Ideal = Time[0] * P

output_dir = "informe"
os.makedirs(output_dir, exist_ok=True)

# ---------------------------------------------------------
# Plot 1: Weak Scaling GFLOPS
# ---------------------------------------------------------
plt.figure(figsize=(10, 6))
plt.plot(P, GFLOPS, 'o-', color='#8e44ad', linewidth=2, markersize=8, label='Real Performance')

# Add labels
for i, txt in enumerate(GFLOPS):
    plt.annotate(f"{txt:.0f}", (P[i], GFLOPS[i]), 
                 textcoords="offset points", xytext=(0,10), ha='center',
                 fontsize=9, fontweight='bold')

plt.title('Weak Scaling Performance (Khipu)\n(N Scaled linearly: 4k $\to$ 131k)', fontsize=14, fontweight='bold')
plt.xlabel('CPUs (P)', fontsize=12)
plt.ylabel('GFLOPS', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(P)
plt.fill_between(P, 0, GFLOPS, color='#8e44ad', alpha=0.1)
plt.ylim(0, max(GFLOPS)*1.15)

output_path_1 = os.path.join(output_dir, "weak_scaling_gflops.png")
plt.savefig(output_path_1, dpi=300, bbox_inches='tight')
print(f"Generated: {output_path_1}")
plt.close()

# ---------------------------------------------------------
# Plot 2: Weak Scaling Time Trend
# ---------------------------------------------------------
plt.figure(figsize=(10, 6))
plt.plot(P, Time, 'rs-', linewidth=2, markersize=8, label='Tiempo Real')
plt.plot(P, Time_Ideal, 'k--', linewidth=2, label='Predicción O($N^2$) ($T \propto P$)')

plt.title('Weak Scaling Time Analysis\n¿Por qué sube el tiempo?', fontsize=14, fontweight='bold')
plt.xlabel('CPUs (P) / Escala del Problema ($N \propto P$)', fontsize=12)
plt.ylabel('Tiempo de Ejecución (s)', fontsize=12)
plt.legend(fontsize=11)
plt.grid(True, linestyle='--', alpha=0.6)
plt.xticks(P)
plt.yscale('log') # Log scale to handle the range better

output_path_2 = os.path.join(output_dir, "weak_scaling_time.png")
plt.savefig(output_path_2, dpi=300, bbox_inches='tight')
print(f"Generated: {output_path_2}")
plt.close()
