import matplotlib.pyplot as plt
import numpy as np

# Data from informe.tex
cpus = np.array([1, 2, 4, 8, 16, 32])
speedup_real = np.array([1.00, 1.10, 2.09, 4.02, 7.08, 11.64])
speedup_ideal = cpus

plt.figure(figsize=(10, 6))
plt.plot(cpus, speedup_ideal, 'k--', label='Ideal Speedup (Linear)', linewidth=2)
plt.plot(cpus, speedup_real, 'bo-', label='Real Speedup (Khipu)', linewidth=2, markersize=8)

plt.xlabel('Number of CPUs', fontsize=12)
plt.ylabel('Speedup', fontsize=12)
plt.title('Speedup: Ideal vs. Real', fontsize=14)
plt.legend(fontsize=12)
plt.grid(True, linestyle='--', alpha=0.7)
plt.xticks(cpus)
plt.yticks(np.arange(0, 33, 4))

# Annotate points
for i, txt in enumerate(speedup_real):
    plt.annotate(f'{txt}', (cpus[i], speedup_real[i]), textcoords="offset points", xytext=(0,10), ha='center')

plt.tight_layout()
plt.savefig('../visualizations/speedup_ideal_vs_real.png', dpi=300)
print("Graph saved to ../visualizations/speedup_ideal_vs_real.png")
