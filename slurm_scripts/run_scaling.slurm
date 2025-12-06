#!/bin/bash
#SBATCH --job-name=nbody-scaling
#SBATCH --output=../outputs/scaling_%j.out
#SBATCH --error=../outputs/scaling_%j.err
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --ntasks=32
#SBATCH --cpus-per-task=1
#SBATCH --time=02:00:00

# Load modules
module purge
module load gnu9/9.4.0
module load openmpi4/4.1.1

# Go to root
cd ..

# Ensure executable exists
if [ ! -f "./cpu-4th" ]; then
    echo "❌ Missing ./cpu-4th"
    exit 1
fi

echo "🚀 Starting Strong Scaling Benchmark (N=25600)"
echo "------------------------------------------------"

# Create a temporary config file for BENCHMARKING (Short duration)
# t_end = 1.0 (Enough to measure GFLOPS/Speedup, instead of 50.0)
TEMP_CONFIG="phi-scaling.cfg"
# Format: eps t_end dt_disk dt_eval eta eta_bh input
echo "1.0E-04   1.0   2.5   0.5   0.15   0.15   dat/data_m15.inp" > $TEMP_CONFIG

echo "📝 Created temporary config: $TEMP_CONFIG (t_end=1.0)"

for P in 1 2 4 8 16 32; do
    echo "▶️ Running with P=$P..."
    start_time=$(date +%s)
    
    # Run MPI
    mpirun -n $P --bind-to core ./cpu-4th $TEMP_CONFIG > outputs/scaling_P${P}.log 2>&1
    
    end_time=$(date +%s)
    duration=$((end_time - start_time))
    echo "✅ P=$P completed in ${duration}s"
done

# Cleanup
rm $TEMP_CONFIG

echo "🎉 Scaling benchmark complete."
