// Implementação do cálculo do conjunto de Mandelbrot em C.
// Estratégia:
//   Para cada pixel (px, py), mapeamos para o plano complexo (cx, cy).
//   Iteramos z_{n+1} = z_n^2 + c até |z|^2 > 4.0 ou atingir max_iter.
//   out_buffer o número de iterações realizadas.
#include <math.h>
#include <stddef.h>
#include "mandelbrot.h"

int mandelbrot(
    int width, int height,
    double xmin, double ymin, double xmax, double ymax,
    int max_iter,
    int *out_buffer
) {
    if (width <= 0 || height <= 0 || max_iter <= 0 || out_buffer == NULL) {
        return 1; // parâmetros inválidos
    }
    if (xmax <= xmin || ymax <= ymin) {
        return 2; // janela inválida
    }

    const double dx = (xmax - xmin) / (double)width;
    const double dy = (ymax - ymin) / (double)height;

    for (int py = 0; py < height; ++py) {
        double cy = ymin + (double)py * dy;
        for (int px = 0; px < width; ++px) {
            double cx = xmin + (double)px * dx;

            double zx = 0.0;
            double zy = 0.0;
            int iter = 0;

            // loop principal
            while (iter < max_iter) {
                // z^2 = (zx + i*zy)^2 = (zx*zx - zy*zy) + i*(2*zx*zy)
                double zx2 = zx * zx - zy * zy + cx;
                double zy2 = 2.0 * zx * zy + cy;

                zx = zx2;
                zy = zy2;

                if ((zx * zx + zy * zy) > 4.0) {
                    break;
                }
                iter++;
            }

            out_buffer[py * width + px] = iter;
        }
    }

    return 0;
}
