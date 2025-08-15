// Interface do módulo C que realiza o cálculo do conjunto de Mandelbrot.
// A função 'mandelbrot' preenche um buffer de inteiros (out_buffer) com o
// número de iterações para cada pixel. Valores iguais a max_iter indicam
// que o ponto pertence (provavelmente) ao conjunto.
//
// Compilação como biblioteca compartilhada (Linux/macOS):
//   gcc -fPIC -O2 -shared mandelbrot.c -o mandelbrot.so
//
// No Windows (MinGW):
//   gcc -O2 -shared -o mandelbrot.dll mandelbrot.c
#ifndef MANDELBROT_H
#define MANDELBROT_H

#ifdef _WIN32
  #define EXPORT __declspec(dllexport)
#else
  #define EXPORT
#endif

#ifdef __cplusplus
extern "C" {
#endif

// Calcula o conjunto de Mandelbrot em um retângulo da tela.
// Parâmetros:
//   width, height: dimensões da imagem em pixels
//   xmin, ymin, xmax, ymax: janela de visualização no plano complexo
//   max_iter: máximo de iterações
//   out_buffer: ponteiro para buffer de inteiros (tamanho width*height)
// Retorno: 0 em sucesso, diferente de 0 em erro de parâmetros.
EXPORT int mandelbrot(
    int width, int height,
    double xmin, double ymin, double xmax, double ymax,
    int max_iter,
    int *out_buffer
);

#ifdef __cplusplus
}
#endif

#endif // MANDELBROT_H
