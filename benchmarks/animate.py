import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation
import glob
import os

def read_snapshot(filename):
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
                float(data[2]),    # x
                float(data[3]),    # y
                float(data[4]),    # z
                float(data[5]),    # vx
                float(data[6]),    # vy
                float(data[7])     # vz
            ])

    return snapshot_id, n_particles, time, np.array(particles)

def update_graph(num, data_files, scatter, title_text):
    filename = data_files[num]
    snap_id, n_parts, time, particles = read_snapshot(filename)
    print(f"Frame {num}: {filename}, n={n_parts}, p_shape={particles.shape}")
    
    # Update scatter plot
    scatter._offsets3d = (particles[:, 0], particles[:, 1], particles[:, 2])
    
    # Update title
    title_text.set_text(f'N-Body Simulation (t={time:.3f})')
    
    # Optional: Rotate camera
    ax.view_init(elev=30, azim=num * 0.5)
    
    return scatter, title_text

# Get all .dat files
all_files = sorted(glob.glob('../outputs/*.dat'))
if not all_files:
    print("No .dat files found in current directory.")
    exit()

# Filter valid files
data_files = []
expected_n = None

for f in all_files:
    try:
        sid, n, t, p = read_snapshot(f)
        if expected_n is None:
            expected_n = n
        
        if n != expected_n:
            print(f"Skipping {f}: Particle count mismatch ({n} vs {expected_n})")
            continue
            
        if len(p) != n:
            print(f"Skipping {f}: Incomplete data ({len(p)} vs {n})")
            continue
            
        data_files.append(f)
    except Exception as e:
        print(f"Skipping {f}: Error reading file ({e})")
        continue

if not data_files:
    print("No valid data files found.")
    exit()

print(f"Found {len(data_files)} valid snapshots out of {len(all_files)} files.")

# Setup plot
fig = plt.figure(figsize=(10, 10), facecolor='black')
ax = fig.add_subplot(111, projection='3d', facecolor='black')

# Initial data
snap_id, n_parts, time, particles = read_snapshot(data_files[0])

# Plot settings
x = particles[:, 0]
y = particles[:, 1]
z = particles[:, 2]

# Color by radius
r = np.sqrt(x**2 + y**2 + z**2)
scatter = ax.scatter(x, y, z, c=r, cmap='magma', s=0.5, alpha=0.8)

# Axis settings
ax.set_axis_off() # Hide axes for better look
# Or keep them but make them white
# ax.xaxis.label.set_color('white')
# ax.yaxis.label.set_color('white')
# ax.zaxis.label.set_color('white')
# ax.tick_params(axis='x', colors='white')
# ax.tick_params(axis='y', colors='white')
# ax.tick_params(axis='z', colors='white')

# Set limits (fixed to avoid jumping)
max_range = 2.0 # Assuming normalized coordinates roughly -1 to 1
ax.set_xlim(-max_range, max_range)
ax.set_ylim(-max_range, max_range)
ax.set_zlim(-max_range, max_range)

title_text = ax.set_title(f'N-Body Simulation (t={time:.3f})', color='white')

# Create animation
ani = animation.FuncAnimation(
    fig, update_graph, frames=len(data_files), 
    fargs=(data_files, scatter, title_text),
    interval=50, blit=False
)

# Save animation
try:
    print("Saving animation to ../visualizations/simulation.mp4...")
    ani.save('../visualizations/simulation.mp4', writer='ffmpeg', fps=30, dpi=150)
    print("Done!")
except Exception as e:
    print(f"Could not save mp4 (ffmpeg might be missing): {e}")
    print("Trying to save as gif...")
    try:
        ani.save('../visualizations/simulation.gif', writer='pillow', fps=30)
        print("Done!")
    except Exception as e2:
        print(f"Could not save gif: {e2}")

plt.close()
