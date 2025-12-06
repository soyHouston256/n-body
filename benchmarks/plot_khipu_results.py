import matplotlib.pyplot as plt
import numpy as np
import os

# Data from Khipu (N=25600)
# Processors
P = np.array([1, 2, 4, 8, 16, 32])

# Performance Metrics
Time = np.array([505.50, 266.59, 133.83, 69.89, 39.80, 24.46])
Speedup_Real = np.array([1.00, 1.90, 3.78, 7.23, 12.70, 20.67])
GFLOPS = np.array([10.68, 20.26, 40.35, 77.27, 135.68, 220.74])

# Ideal Speedup (Linear)
Speedup_Ideal = P

# Output directory for plots (target the 'informe' folder directly)
output_dir = "informe"
os.makedirs(output_dir, exist_ok=True)

# ---------------------------------------------------------
# Plot 1: Performance Scaling (GFLOPS)
# ---------------------------------------------------------
plt.figure(figsize=(10, 6))
bars = plt.bar(range(len(P)), GFLOPS, color='#2ecc71', alpha=0.8, edgecolor='black', linewidth=1)

# Add value labels on top of bars
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height + 5,
             f'{height:.1f}',
             ha='center', va='bottom', fontsize=10, fontweight='bold')

plt.title('Strong Scaling Performance (Khipu, N=25,600)', fontsize=14, fontweight='bold')
plt.xlabel('Number of CPUs (P)', fontsize=12)
plt.ylabel('Performance (GFLOPS)', fontsize=12)
plt.xticks(range(len(P)), P)
plt.grid(axis='y', linestyle='--', alpha=0.6)
plt.ylim(0, max(GFLOPS) * 1.15) # Add 15% padding for labels

output_path_1 = os.path.join(output_dir, "performance_scaling.png")
plt.savefig(output_path_1, dpi=300, bbox_inches='tight')
print(f"Generated: {output_path_1}")
plt.close()

# ---------------------------------------------------------
# Plot 2: Speedup Ideal vs Real
# ---------------------------------------------------------
plt.figure(figsize=(10, 6))

# Plot Ideal
plt.plot(P, Speedup_Ideal, 'k--', label='Ideal Speedup (Linear)', linewidth=2)

# Plot Real
plt.plot(P, Speedup_Real, 'o-', color='#3498db', label='Real Speedup', linewidth=2, markersize=8)

# Add value labels for Real Speedup
for i, txt in enumerate(Speedup_Real):
    plt.annotate(f"{txt:.1f}x", (P[i], Speedup_Real[i]), 
                 textcoords="offset points", xytext=(0,10), ha='center',
                 fontsize=9, fontweight='bold', color='#2980b9')

plt.title('Strong Scaling: Ideal vs. Real Speedup', fontsize=14, fontweight='bold')
plt.xlabel('Number of CPUs (P)', fontsize=12)
plt.ylabel('Speedup (S)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)
plt.legend(fontsize=11)
plt.xticks(P)
plt.xlim(0.5, 33)
plt.ylim(0, 34)

# Add efficiency annotations for P=1, 8, 32
efficiencies = [100.0, 90.4, 64.6]
indices = [0, 3, 5]
for idx in indices:
    proc = P[idx]
    spd = Speedup_Real[idx]
    eff = efficiencies[indices.index(idx)]
    plt.text(proc + 0.5, spd - 2, f"Eff: {eff:.1f}%", fontsize=9, style='italic', color='#555')

output_path_2 = os.path.join(output_dir, "speedup_ideal_vs_real.png")
plt.savefig(output_path_2, dpi=300, bbox_inches='tight')
print(f"Generated: {output_path_2}")
plt.close()
