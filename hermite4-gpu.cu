#include "hermite4-gpu.h"
#include <cuda_runtime.h>
#include <stdio.h>

// Error checking macro
#define cudaCheckError(ans)                                                    \
  {                                                                            \
    gpuAssert((ans), __FILE__, __LINE__);                                      \
  }
inline void gpuAssert(cudaError_t code, const char *file, int line,
                      bool abort = true) {
  if (code != cudaSuccess) {
    fprintf(stderr, "GPUassert: %s %s %d\n", cudaGetErrorString(code), file,
            line);
    if (abort)
      exit(code);
  }
}

// GPU Data Structures (Internal to this file)
struct GParticle {
  float3 pos;
  float mass;
  float3 vel;
  float pad;
};

struct GForce {
  float3 acc;
  float pot;
  float3 jrk;
  float pad;
};

// CUDA Kernel
__global__ void calc_force_kernel(int ni, int nj, float eps2,
                                  const GParticle *ipred,
                                  const GParticle *jpred, GForce *force) {
  int i = blockIdx.x * blockDim.x + threadIdx.x;
  if (i >= ni)
    return;

  float3 ipos = ipred[i].pos;
  float3 ivel = ipred[i].vel;

  float3 acc = {0.0f, 0.0f, 0.0f};
  float3 jrk = {0.0f, 0.0f, 0.0f};
  float pot = 0.0f;

  for (int j = 0; j < nj; j++) {
    float3 jpos = jpred[j].pos;
    float3 jvel = jpred[j].vel;
    float mass = jpred[j].mass;

    float dx = jpos.x - ipos.x;
    float dy = jpos.y - ipos.y;
    float dz = jpos.z - ipos.z;
    float dvx = jvel.x - ivel.x;
    float dvy = jvel.y - ivel.y;
    float dvz = jvel.z - ivel.z;

    float r2 = eps2 + dx * dx + dy * dy + dz * dz;

    // Simple check for self-interaction
    if (r2 == eps2)
      continue;

    float rinv2 = 1.0f / r2;
    float rinv1 = sqrtf(rinv2);
    float rv = dx * dvx + dy * dvy + dz * dvz;
    rv *= -3.0f * rinv2;
    rinv1 *= mass;
    float rinv3 = rinv1 * rinv2;

    pot -= rinv1;
    acc.x += rinv3 * dx;
    acc.y += rinv3 * dy;
    acc.z += rinv3 * dz;
    jrk.x += rinv3 * (dvx + rv * dx);
    jrk.y += rinv3 * (dvy + rv * dy);
    jrk.z += rinv3 * (dvz + rv * dz);
  }

  force[i].acc = acc;
  force[i].jrk = jrk;
  force[i].pot = pot;
}

// Global pointers for GPU memory
static GParticle *d_ipred = nullptr;
static GParticle *d_jpred = nullptr;
static GForce *d_force = nullptr;
static int d_n_max = 0;

void CUDA_MPI_Init(int rank) {
  int devCount;
  cudaGetDeviceCount(&devCount);
  if (devCount > 0) {
    cudaSetDevice(rank % devCount);
  }
}

extern double wtime(); // Defined in phi-GPU.cpp (or main)

void calc_force(int ni, int nj, double eps2, Predictor ipred[],
                Predictor jpred[], Force force[], double &t1, double &t_isend,
                double &t_recv) {

  t1 = wtime(); // Start timer

  // Allocate GPU memory if needed
  if (d_n_max < std::max(ni, nj)) {
    if (d_ipred)
      cudaFree(d_ipred);
    if (d_jpred)
      cudaFree(d_jpred);
    if (d_force)
      cudaFree(d_force);

    d_n_max = std::max(ni, nj) * 1.2; // Buffer
    cudaCheckError(cudaMalloc(&d_ipred, d_n_max * sizeof(GParticle)));
    cudaCheckError(cudaMalloc(&d_jpred, d_n_max * sizeof(GParticle)));
    cudaCheckError(cudaMalloc(&d_force, d_n_max * sizeof(GForce)));
  }

  // Temporary host buffers (could be optimized)
  static GParticle *h_ipred_buf = nullptr;
  static GParticle *h_jpred_buf = nullptr;
  static GForce *h_force_buf = nullptr;
  static int h_buf_size = 0;

  if (h_buf_size < d_n_max) {
    delete[] h_ipred_buf;
    delete[] h_jpred_buf;
    delete[] h_force_buf;
    h_buf_size = d_n_max;
    h_ipred_buf = new GParticle[h_buf_size];
    h_jpred_buf = new GParticle[h_buf_size];
    h_force_buf = new GForce[h_buf_size];
  }

// Convert Host -> Host Buffer
#pragma omp parallel for
  for (int i = 0; i < ni; i++) {
    h_ipred_buf[i].pos = make_float3(
        (float)ipred[i].pos.x, (float)ipred[i].pos.y, (float)ipred[i].pos.z);
    h_ipred_buf[i].vel = make_float3(
        (float)ipred[i].vel.x, (float)ipred[i].vel.y, (float)ipred[i].vel.z);
    h_ipred_buf[i].mass = (float)ipred[i].mass;
  }
#pragma omp parallel for
  for (int j = 0; j < nj; j++) {
    h_jpred_buf[j].pos = make_float3(
        (float)jpred[j].pos.x, (float)jpred[j].pos.y, (float)jpred[j].pos.z);
    h_jpred_buf[j].vel = make_float3(
        (float)jpred[j].vel.x, (float)jpred[j].vel.y, (float)jpred[j].vel.z);
    h_jpred_buf[j].mass = (float)jpred[j].mass;
  }

  t_isend = wtime();

  cudaCheckError(cudaMemcpy(d_ipred, h_ipred_buf, ni * sizeof(GParticle),
                            cudaMemcpyHostToDevice));
  cudaCheckError(cudaMemcpy(d_jpred, h_jpred_buf, nj * sizeof(GParticle),
                            cudaMemcpyHostToDevice));

  // Launch Kernel
  int blockSize = 128;
  int numBlocks = (ni + blockSize - 1) / blockSize;
  calc_force_kernel<<<numBlocks, blockSize>>>(ni, nj, (float)eps2, d_ipred,
                                              d_jpred, d_force);
  cudaCheckError(cudaGetLastError());

  // Copy back
  cudaCheckError(cudaMemcpy(h_force_buf, d_force, ni * sizeof(GForce),
                            cudaMemcpyDeviceToHost));

  t_recv = wtime();

// Convert back
#pragma omp parallel for
  for (int i = 0; i < ni; i++) {
    force[i].acc.x = h_force_buf[i].acc.x;
    force[i].acc.y = h_force_buf[i].acc.y;
    force[i].acc.z = h_force_buf[i].acc.z;
    force[i].jrk.x = h_force_buf[i].jrk.x;
    force[i].jrk.y = h_force_buf[i].jrk.y;
    force[i].jrk.z = h_force_buf[i].jrk.z;
    force[i].pot = h_force_buf[i].pot;
  }
}
