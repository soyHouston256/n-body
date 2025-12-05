import os

# Configuration
cpu_counts = [1, 2, 4, 8, 16, 32]
base_template = """#!/bin/bash
#SBATCH --job-name=nbody-{n}
#SBATCH --output=nbody_{n}_%j.out
#SBATCH --error=nbody_{n}_%j.err
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task={n}
#SBATCH --time=00:10:00

# Load modules
module purge
module load gnu9/9.4.0
module load openmpi4/4.1.1

# No compilation here (assumes make cpu-4th was run on login node)

# Run
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
echo "Running with {n} CPUs"

mpirun -n 1 --bind-to none ./cpu-4th < phi-GPU4.cfg
"""

submit_script_lines = ["#!/bin/bash"]

for n in cpu_counts:
    filename = f"../run_{n}.slurm"
    with open(filename, "w") as f:
        f.write(base_template.format(n=n))
    print(f"Created {filename}")
    submit_script_lines.append(f"sbatch run_{n}.slurm")

with open("../submit_all.sh", "w") as f:
    f.write("\n".join(submit_script_lines))
    f.write("\n")

print("Created submit_all.sh. Upload these files to the cluster and run 'bash submit_all.sh'.")
