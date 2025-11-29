#!/bin/bash
#SBATCH --job-name=nbody-cpu
#SBATCH --output=nbody_%j.out
#SBATCH --error=nbody_%j.err
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=32
#SBATCH --time=01:00:00

# Load necessary modules
# Purge first to ensure a clean environment
module purge

# Load GCC and OpenMPI (Using gnu9 as it is stable)
module load gnu9/9.4.0
module load openmpi4/4.1.1

# Compile is done manually on login node to avoid header issues on compute nodes
# make clean
# make cpu-4th

# Run
# OMP_NUM_THREADS should match cpus-per-task
export OMP_NUM_THREADS=$SLURM_CPUS_PER_TASK

echo "Starting simulation on $(hostname)"
echo "CPUs available: $SLURM_CPUS_PER_TASK"

# Run with 1 MPI process (hybrid MPI+OpenMP)
mpirun -n 1 --bind-to none ./cpu-4th < phi-GPU4.cfg

echo "Simulation complete"
