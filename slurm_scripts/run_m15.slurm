#!/bin/bash
#SBATCH --job-name=nbody-m15
#SBATCH --output=../outputs/nbody_m15_%j.out
#SBATCH --error=../outputs/nbody_m15_%j.err
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --time=01:00:00

# Load necessary modules
module purge
module load gnu9/9.4.0
module load openmpi4/4.1.1

# Run
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

echo "Starting M15 simulation (N=25600) on $(hostname)"
echo "CPUs available: $SLURM_CPUS_PER_TASK"

# Run with 1 MPI process (hybrid MPI+OpenMP)
# Assuming sbatch was run from slurm_scripts/
cd .. 

echo "Current directory: $(pwd)"
if [ ! -f "./cpu-4th" ]; then
    echo "❌ ERROR: Executable ./cpu-4th NOT found!"
    echo "Contents of $(pwd):"
    ls -l
    exit 1
fi

mpirun -n 1 --bind-to none ./cpu-4th slurm_scripts/phi-M15.cfg

echo "Simulation complete"
