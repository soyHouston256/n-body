#!/usr/bin/env python3
"""
N-Body Simulation Visualizer
Reads .dat files and creates 3D visualizations
"""

import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import glob
import sys

def read_snapshot(filename):
    """
    Read a snapshot file (.dat format)
    Returns: snapshot_id, n_particles, time, particle_data
    """
    with open(filename, 'r') as f:
        lines = f.readlines()

    snapshot_id = int(lines[0].strip())
    n_particles = int(lines[1].strip())
    time = float(lines[2].strip())

    # Read particle data: id, mass, x, y, z, vx, vy, vz
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

def plot_snapshot_3d(filename, save=False):
    """
    Create a 3D scatter plot of particle positions
    """
    snap_id, n_parts, time, particles = read_snapshot(filename)

    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(111, projection='3d')

    # Extract positions
    x = particles[:, 2]  # x position
    y = particles[:, 3]  # y position
    z = particles[:, 4]  # z position

    # Color by distance from center
    r = np.sqrt(x**2 + y**2 + z**2)

    scatter = ax.scatter(x, y, z, c=r, cmap='viridis', s=1, alpha=0.6)

    ax.set_xlabel('X', fontsize=12)
    ax.set_ylabel('Y', fontsize=12)
    ax.set_zlabel('Z', fontsize=12)
    ax.set_title(f'N-Body Simulation (N={n_parts}, t={time:.3f})', fontsize=14)

    plt.colorbar(scatter, ax=ax, label='Distance from center')

    # Set equal aspect ratio
    max_range = np.array([x.max()-x.min(), y.max()-y.min(), z.max()-z.min()]).max() / 2.0
    mid_x = (x.max()+x.min()) * 0.5
    mid_y = (y.max()+y.min()) * 0.5
    mid_z = (z.max()+z.min()) * 0.5
    ax.set_xlim(mid_x - max_range, mid_x + max_range)
    ax.set_ylim(mid_y - max_range, mid_y + max_range)
    ax.set_zlim(mid_z - max_range, mid_z + max_range)

    if save:
        plt.savefig(f'../visualizations/snapshot_{snap_id:04d}.png', dpi=150, bbox_inches='tight')
        print(f"Saved ../visualizations/snapshot_{snap_id:04d}.png")
    else:
        plt.show()

    plt.close()

def plot_energy_conservation(filename='../outputs/contr.dat'):
    """
    Plot energy conservation from contr.dat
    """
    try:
        # Read contr.dat: time, steps, interactions, E_total, E_kin, E_pot, dE, elapsed_time
        data = np.loadtxt(filename)

        time = data[:, 0]
        energy_error = data[:, 6]  # dE column

        fig, ax = plt.subplots(figsize=(10, 6))
        ax.plot(time, energy_error, 'b-', linewidth=2)
        ax.axhline(y=0, color='r', linestyle='--', alpha=0.5)
        ax.set_xlabel('Time', fontsize=12)
        ax.set_ylabel('Energy Error ΔE', fontsize=12)
        ax.set_title('Energy Conservation', fontsize=14)
        ax.grid(True, alpha=0.3)

        plt.tight_layout()
        plt.savefig('../visualizations/energy_conservation.png', dpi=150, bbox_inches='tight')
        print("Saved ../visualizations/energy_conservation.png")
        plt.show()

    except FileNotFoundError:
        print(f"File {filename} not found")
    except Exception as e:
        print(f"Error reading {filename}: {e}")

def plot_all_snapshots():
    """
    Create plots for all snapshot files
    """
    snapshot_files = sorted(glob.glob('../outputs/[0-9][0-9][0-9][0-9].dat'))

    if not snapshot_files:
        print("No snapshot files found (pattern: 0000.dat, 0001.dat, ...)")
        return

    print(f"Found {len(snapshot_files)} snapshots")

    for filename in snapshot_files:
        print(f"Processing {filename}...")
        plot_snapshot_3d(filename, save=True)

    print(f"\nCreated {len(snapshot_files)} images")

def main():
    """
    Main function
    """
    if len(sys.argv) < 2:
        print("N-Body Simulation Visualizer")
        print("\nUsage:")
        print("  python visualize.py <command> [options]")
        print("\nCommands:")
        print("  snapshot <file>  - Visualize a single snapshot (e.g., 0000.dat)")
        print("  all              - Create images for all snapshots")
        print("  energy           - Plot energy conservation from contr.dat")
        print("\nExamples:")
        print("  python visualize.py snapshot 0000.dat")
        print("  python visualize.py all")
        print("  python visualize.py energy")
        sys.exit(1)

    command = sys.argv[1]

    if command == 'snapshot':
        if len(sys.argv) < 3:
            print("Error: Please specify a snapshot file")
            print("Example: python visualize.py snapshot 0000.dat")
            sys.exit(1)
        filename = sys.argv[2]
        plot_snapshot_3d(filename, save=False)

    elif command == 'all':
        plot_all_snapshots()

    elif command == 'energy':
        plot_energy_conservation()

    else:
        print(f"Unknown command: {command}")
        print("Available commands: snapshot, all, energy")
        sys.exit(1)

if __name__ == '__main__':
    main()
