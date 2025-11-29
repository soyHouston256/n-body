import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy as np
import glob

def read_dat_file(filename):
    with open(filename, 'r') as f:
        lines = f.readlines()
        data = []
        for line in lines[3:]:
            parts = line.split()
            if len(parts) >= 8:
                data.append([float(x) for x in parts[2:8]])
    return np.array(data)

def generate_snapshot():
    files = sorted(glob.glob("0*.dat"))
    if not files: return
    
    # Use the last file for the snapshot
    last_file = files[-1]
    data = read_dat_file(last_file)
    
    fig = plt.figure(figsize=(10, 10), facecolor='black')
    ax = fig.add_subplot(111, projection='3d', facecolor='black')
    ax.set_axis_off()
    
    vel = np.linalg.norm(data[:, 3:], axis=1)
    norm = plt.Normalize(vel.min(), vel.max())
    
    ax.scatter(data[:, 0], data[:, 1], data[:, 2], 
               c=vel, cmap='plasma', s=1.0, alpha=0.9, norm=norm)
               
    # Zoom out slightly to see structure
    max_range = 2.0 
    ax.set_xlim(-max_range, max_range)
    ax.set_ylim(-max_range, max_range)
    ax.set_zlim(-max_range, max_range)
    
    # Nice angle
    ax.view_init(elev=30, azim=45)
    
    plt.savefig("simulation_snapshot.png", dpi=300, bbox_inches='tight', facecolor='black')
    print("Snapshot saved to simulation_snapshot.png")

if __name__ == "__main__":
    generate_snapshot()
