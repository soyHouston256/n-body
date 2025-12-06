#!/bin/bash
#SBATCH --job-name=nbody-weak
#SBATCH --output=../outputs/weak_%j.out
#SBATCH --error=../outputs/weak_%j.err
#SBATCH --partition=standard
#SBATCH --nodes=1
#SBATCH --ntasks=32
#SBATCH --cpus-per-task=1
#SBATCH --time=04:00:00

# Load modules
module purge
module load gnu9/9.4.0
module load openmpi4/4.1.1

# Go to root
cd ..

# Ensure executables exist
if [ ! -f "./cpu-4th" ] || [ ! -f "./gen-plum" ]; then
    echo "❌ Missing ./cpu-4th or ./gen-plum"
    echo "Please compile both on Khipu before running this script."
    exit 1
fi

echo "🚀 Starting Weak Scaling Benchmark (Base N=4096)"
echo "------------------------------------------------"

# Base particles per processor
BASE_N=4096

for P in 1 2 4 8 16 32; do
    # Calculate N = BASE_N * P
    N=$((BASE_N * P))
    
    echo "▶️ Preparing P=$P, N=$N..."
    
    # 1. Generate Input Data
    DATA_FILE="dat/weak_N${N}.inp"
    if [ ! -f "$DATA_FILE" ]; then
        ./gen-plum $N > $DATA_FILE
    fi
    
    # 2. Create Config
    CONFIG_FILE="phi-weak-P${P}.cfg"
    # t_end=0.2 is enough for performance check
    echo "1.0E-04   0.2   10.0   0.01   0.15   0.15   $DATA_FILE" > $CONFIG_FILE
    
    # 3. Run Benchmark
    echo "   Running MPI..."
    start_time=$(date +%s)
    mpirun -n $P --bind-to core ./cpu-4th $CONFIG_FILE > outputs/weak_P${P}_N${N}.log 2>&1
    end_time=$(date +%s)
    
    duration=$((end_time - start_time))
    echo "✅ P=$P (N=$N) completed in ${duration}s"
    
    # Cleanup config but keep data for reference if needed? No, maybe clean to save space
    rm $CONFIG_FILE
    # rm $DATA_FILE # Optional: keep execution clean
done

echo "🎉 Weak Scaling benchmark complete."
