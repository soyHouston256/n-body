import matplotlib.pyplot as plt
import numpy as np
import os

# Configuration
input_file = "outputs/nbody_m15_25889.out"
output_dir = "informe"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "energy_conservation.png")

times = []
energies = []

print(f"Reading {input_file}...")

with open(input_file, 'r') as f:
    for line in f:
        # Filter relevant lines (data lines start with a number)
        parts = line.split()
        if len(parts) >= 8:
            try:
                t = float(parts[0])
                e = float(parts[3])
                
                # Check bounds (Time 0 to 50)
                if 0 <= t <= 50.1:
                    times.append(t)
                    energies.append(e)
            except ValueError:
                continue

print(f"Found {len(times)} data points.")

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(times, energies, linewidth=2, color='#e74c3c', label='Total Energy')

# Formatting
plt.title('Conservación de Energía (Validación Científica)', fontsize=14, fontweight='bold')
plt.xlabel('Tiempo de Simulación (Unidades N-Body)', fontsize=12)
plt.ylabel('Energía Total (E)', fontsize=12)
plt.grid(True, linestyle='--', alpha=0.6)

# Calculate stats for annotation
e0 = energies[0]
end = energies[-1]
err = abs(end - e0) / abs(e0) * 100
mean_e = np.mean(energies)

# Dynamic Y-axis limits to show the variation (don't zoom too much if it's flat)
plt.ylim(min(energies)*1.005, max(energies)*0.995) 

# Add text box with statistics
textstr = '\n'.join((
    r'$E_{inicial}=%.4f$' % (e0, ),
    r'$E_{final}=%.4f$' % (end, ),
    r'Error Relativo=%.2f%%' % (err, )))

props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
plt.gca().text(0.05, 0.95, textstr, transform=plt.gca().transAxes, fontsize=10,
        verticalalignment='top', bbox=props)

plt.legend()
plt.tight_layout()

plt.savefig(output_path, dpi=300)
print(f"Generated plot: {output_path}")
print(textstr)
