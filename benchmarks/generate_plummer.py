import numpy as np
import sys

def generate_plummer(n_particles, seed=42):
    """
    Generates a Plummer sphere model.
    Based on Aarseth et al. (1974) recipe.
    """
    np.random.seed(seed)
    
    # Mass of each particle (total mass = 1)
    mass = 1.0 / n_particles
    
    # Radii
    X1 = np.random.random(n_particles)
    r = (X1**(-2.0/3.0) - 1.0)**(-0.5)
    
    # Positions
    X2 = np.random.random(n_particles)
    X3 = np.random.random(n_particles)
    z = (1.0 - 2.0*X2) * r
    x = (r**2 - z**2)**0.5 * np.cos(2.0*np.pi*X3)
    y = (r**2 - z**2)**0.5 * np.sin(2.0*np.pi*X3)
    
    # Velocities
    # Escape velocity at r: v_esc = sqrt(2 * phi(r)) = sqrt(2) * (1 + r^2)^(-1/4)
    # q = v / v_esc
    # Distribution of q: g(q) = q^2 * (1 - q^2)^(3.5)
    
    X4 = np.random.random(n_particles)
    X5 = np.random.random(n_particles)
    
    # Rejection sampling for velocity magnitude
    # Max of g(q) is at q = sqrt(2/9) approx 0.47
    # We can use a simple rejection method
    
    q = np.zeros(n_particles)
    for i in range(n_particles):
        while True:
            qi = np.random.random()
            fi = qi**2 * (1.0 - qi**2)**3.5
            # Max value of f(q) is approx 0.1
            if np.random.random() * 0.1 < fi:
                q[i] = qi
                break
                
    v_esc = np.sqrt(2.0) * (1.0 + r**2)**(-0.25)
    v = q * v_esc
    
    X6 = np.random.random(n_particles)
    X7 = np.random.random(n_particles)
    
    vz = (1.0 - 2.0*X6) * v
    vx = (v**2 - vz**2)**0.5 * np.cos(2.0*np.pi*X7)
    vy = (v**2 - vz**2)**0.5 * np.sin(2.0*np.pi*X7)
    
    return mass, x, y, z, vx, vy, vz

def write_input_file(filename, n_particles):
    mass, x, y, z, vx, vy, vz = generate_plummer(n_particles)
    
    with open(filename, 'w') as f:
        # Header: diskstep, nbody, time
        f.write(f"0\n{n_particles}\n0.0\n")
        
        for i in range(n_particles):
            # Format: id mass x y z vx vy vz
            # Using scientific notation for precision
            f.write(f"{i} {mass:.8E} {x[i]:.8E} {y[i]:.8E} {z[i]:.8E} {vx[i]:.8E} {vy[i]:.8E} {vz[i]:.8E}\n")

if __name__ == "__main__":
    N = 25600
    FILENAME = "../data_m15.inp"
    print(f"Generating Plummer sphere with N={N} particles...")
    write_input_file(FILENAME, N)
    print(f"File {FILENAME} created successfully.")
