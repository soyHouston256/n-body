import matplotlib.pyplot as plt
import matplotlib.animation as animation
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import glob
import os

def read_dat_file(filename):
    """Reads a .dat file and returns particle positions and velocities."""
    with open(filename, 'r') as f:
        lines = f.readlines()
        # Skip header (3 lines)
        data = []
        for line in lines[3:]:
            parts = line.split()
            if len(parts) >= 8:
                # ID, Mass, X, Y, Z, VX, VY, VZ
                data.append([float(x) for x in parts[2:8]])
    return np.array(data)

def generate_animation():
    print("Generating 3D Animation...")
    files = sorted(glob.glob("0*.dat"))
    if not files:
        print("No .dat files found!")
        return

    all_data = []
    for f in files:
        print(f"Reading {f}...")
        all_data.append(read_dat_file(f))

    fig = plt.figure(figsize=(10, 10), facecolor='black')
    ax = fig.add_subplot(111, projection='3d', facecolor='black')
    
    # Hide axes
    ax.set_axis_off()
    
    # Initial plot
    data = all_data[0]
    # Color by velocity magnitude
    vel = np.linalg.norm(data[:, 3:], axis=1)
    # Normalize velocity for color map
    norm = plt.Normalize(vel.min(), vel.max())
    
    scatter = ax.scatter(data[:, 0], data[:, 1], data[:, 2], 
                        c=vel, cmap='plasma', s=0.5, alpha=0.8, norm=norm)

    # Set limits based on all data to keep scale constant
    all_pos = np.vstack([d[:, :3] for d in all_data])
    max_range = np.abs(all_pos).max() * 0.6 # Zoom in a bit
    
    ax.set_xlim(-max_range, max_range)
    ax.set_ylim(-max_range, max_range)
    ax.set_zlim(-max_range, max_range)

    def update(frame):
        data = all_data[frame]
        scatter._offsets3d = (data[:, 0], data[:, 1], data[:, 2])
        
        # Update colors
        vel = np.linalg.norm(data[:, 3:], axis=1)
        scatter.set_array(vel)
        
        # Rotate view
        ax.view_init(elev=30, azim=frame * 2)
        
        ax.set_title(f"Time Step: {frame}", color='white')
        return scatter,

    ani = animation.FuncAnimation(fig, update, frames=len(all_data), interval=100, blit=False)
    
    # Save as GIF
    writer = animation.PillowWriter(fps=10)
    ani.save("nbody_simulation.gif", writer=writer)
    print("Animation saved to nbody_simulation.gif")

def generate_performance_chart():
    print("Generating Performance Chart...")
    
    # Data from benchmarks
    cpus = [1, 2, 4, 8, 16, 32]
    gflops = [9.56, 10.53, 19.95, 38.47, 67.66, 111.26]
    
    plt.style.use('dark_background')
    fig, ax = plt.subplots(figsize=(10, 6))
    
    bars = ax.bar(range(len(cpus)), gflops, color='#00ff00', alpha=0.7)
    
    # Add value labels
    for bar in bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{height:.1f}',
                ha='center', va='bottom', color='white', fontweight='bold')

    ax.set_xticks(range(len(cpus)))
    ax.set_xticklabels([str(c) for c in cpus])
    
    ax.set_xlabel('CPUs (OpenMP Threads)', fontsize=12, color='white')
    ax.set_ylabel('Performance (GFlops)', fontsize=12, color='white')
    ax.set_title('N-Body Simulation Scaling on Khipu (32 Cores)', fontsize=14, color='white', fontweight='bold')
    
    # Add a trend line (ideal scaling based on 1 CPU)
    # ideal = [gflops[0] * c for c in cpus]
    # ax.plot(range(len(cpus)), ideal, 'r--', label='Ideal Linear Scaling', alpha=0.5)
    # ax.legend()

    plt.tight_layout()
    plt.savefig("performance_scaling.png", dpi=300)
    print("Chart saved to performance_scaling.png")

if __name__ == "__main__":
    generate_animation()
    generate_performance_chart()
