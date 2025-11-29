#!/bin/bash
#SBATCH --job-name=nbody-4
#SBATCH --output=nbody_4_%j.out
#SBATCH --error=nbody_4_%j.err
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --time=00:10:00

# Load modules
module purge
module load gnu9/9.4.0
module load openmpi4/4.1.1

# No compilation here (assumes make cpu-4th was run on login node)

# Run
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK
echo "Running with 4 CPUs"

mpirun -n 1 --bind-to none ./cpu-4th < phi-GPU4.cfg
