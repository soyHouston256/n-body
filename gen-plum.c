/*
 * gen-plum.c - Generador de Modelo de Plummer
 * Para Proyecto HPC 2025-I
 *
 * Compilar: gcc -O3 -o gen-plum gen-plum.c -lm
 * Uso: ./gen-plum <N_particles> > data.inp
 */

#include <math.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

#define PI 3.14159265358979323846

double rand_val() { return (double)rand() / (double)RAND_MAX; }

int main(int argc, char *argv[]) {
  if (argc < 2) {
    fprintf(stderr, "Uso: %s <N_particles>\n", argv[0]);
    return 1;
  }

  int n = atoi(argv[1]);
  int seed = time(NULL);
  srand(seed);

  double t_cur = 0.0;

  // Encabezado para phi-GPU (Formato compatible)
  // diskstep nbody time_cur
  printf("%d\n", 0);
  printf("%d\n", n);
  printf("%.1lf\n", t_cur);

  // MUnits (Mass Units) = 1.0 / N
  double mass = 1.0 / (double)n;
  double rsc = 9.0 * PI / 16.0;

  for (int i = 0; i < n; i++) {
    double r = 1.0 / sqrt(pow(rand_val(), -2.0 / 3.0) - 1.0);
    double z = (1.0 - 2.0 * rand_val()) * r;
    double x = sqrt(r * r - z * z) * cos(2.0 * PI * rand_val());
    double y = sqrt(r * r - z * z) * sin(2.0 * PI * rand_val());

    double v = sqrt(2.0) * pow(1.0 + r * r, -0.25);
    double ve =
        v *
        sqrt(pow(rand_val(),
                 2.0 / 3.0)); // Correct distribution? Simplifying for Plummer

    // Velocity (simplified plummer rejection sampling or von neumann is better,
    // but using standard approximate formula for assignment purposes)
    // Better implementation:
    double x1, x2, x3, x4, x5, x6, x7;
    double radius, velocity;

    // Position
    x1 = rand_val();
    radius = 1.0 / sqrt(pow(x1, -2.0 / 3.0) - 1.0);

    x2 = rand_val();
    x3 = rand_val();
    z = (1.0 - 2.0 * x2) * radius;
    x = sqrt(radius * radius - z * z) * cos(2.0 * PI * x3);
    y = sqrt(radius * radius - z * z) * sin(2.0 * PI * x3);

    // Velocity (Von Neumann rejection)
    double q, g;
    do {
      q = rand_val();
      g = rand_val() * 0.1;
    } while (g > q * q * pow(1.0 - q * q, 3.5));

    velocity = q * sqrt(2.0) * pow(1.0 + radius * radius, -0.25);

    x4 = rand_val();
    x5 = rand_val();
    double vz = (1.0 - 2.0 * x4) * velocity;
    double vx = sqrt(velocity * velocity - vz * vz) * cos(2.0 * PI * x5);
    double vy = sqrt(velocity * velocity - vz * vz) * sin(2.0 * PI * x5);

    // Scale
    // x *= rsc; y *= rsc; z *= rsc;
    // vx /= sqrt(rsc); vy /= sqrt(rsc); vz /= sqrt(rsc);

    // Format: id mass x y z vx vy vz
    printf("%d %.8E %.8E %.8E %.8E %.8E %.8E %.8E\n", i, mass, x, y, z, vx, vy,
           vz);
  }

  return 0;
}
