# N-Body Simulation - CPU-Only Version
# Simplified Makefile without CUDA/GPU dependencies

CXX = mpicxx
CXXFLAGS = -O3 -Wall

# Detect OS and set OpenMP flags accordingly
UNAME_S := $(shell uname -s)
ifeq ($(UNAME_S),Darwin)
    # macOS: use libomp from Homebrew
    LIBOMP_PREFIX = $(shell brew --prefix libomp 2>/dev/null || echo "/opt/homebrew/opt/libomp")
    CXXFLAGS += -Xpreprocessor -fopenmp -I$(LIBOMP_PREFIX)/include
    LDFLAGS = -L$(LIBOMP_PREFIX)/lib -lomp
else
    # Linux: use standard OpenMP
    CXXFLAGS += -fopenmp
    LDFLAGS =
endif

# Default target: build all CPU versions
all: cpu-4th cpu-6th cpu-8th

# Individual targets
cpu-4th: phi-GPU.cpp hermite4.h vector3.h taylor.h
	$(CXX) $(CXXFLAGS) -DFOURTH -o $@ phi-GPU.cpp $(LDFLAGS)

cpu-6th: phi-GPU.cpp hermite6.h vector3.h taylor.h
	$(CXX) $(CXXFLAGS) -DSIXTH -o $@ phi-GPU.cpp $(LDFLAGS)

cpu-8th: phi-GPU.cpp hermite8.h vector3.h taylor.h
	$(CXX) $(CXXFLAGS) -DEIGHTH -o $@ phi-GPU.cpp $(LDFLAGS)

# Clean build artifacts
clean:
	rm -f cpu-4th cpu-6th cpu-8th *.o

# Run targets with default config
run-4th: cpu-4th
	./cpu-4th < phi-GPU4.cfg

run-6th: cpu-6th
	./cpu-6th < phi-GPU6.cfg

run-8th: cpu-8th
	./cpu-8th < phi-GPU8.cfg

# Run with MPI (adjust -n for number of processes)
run-mpi-4th: cpu-4th
	mpirun -n 4 ./cpu-4th < phi-GPU4.cfg

.PHONY: all clean run-4th run-6th run-8th run-mpi-4th
