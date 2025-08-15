Gustavo Raymundi Nygaard

T1 - CONCEITOS DE LINGUAGENS DE PROGRAMAÇÃO

Implementação com visualização gráfica e duas linguagens de programação


# Mandelbrot – Integração C (cálculo) + Python/Tkinter (GUI)

Projeto demonstrando o uso conjunto de duas linguagens com vocação distinta:
- **C**: realiza o cálculo numérico do conjunto de Mandelbrot.
- **Python (Tkinter)**: provê a interface gráfica e exibe a imagem, chamando a biblioteca C via ctypes.

--> O foco é a integração entre as linguagens (carregamento de biblioteca compartilhada, passagem de parâmetros e buffers).

## Como compilar e executar

### Pré-requisitos
- **gcc** (ou clang) para compilar a biblioteca C.
- **Python 3** (Tkinter já vem na biblioteca padrão).
  - Linux/WSL: se necessário, instale `sudo apt install python3-tk`.

### Passos
1. Compilar a biblioteca compartilhada:
   ```bash
   make
   ```
   Isso gerará **`mandelbrot.so`** (Linux), **`mandelbrot.dylib`** (macOS) ou **`mandelbrot.dll`** (Windows).

2. Executar a interface gráfica:
   ```bash
   make run
   ```
   Ou diretamente:
   ```bash
   python3 src/interface.py
   ```

## Como usar a GUI
- Ajuste **largura, altura, iterações** e os limites **xmin, xmax, ymin, ymax**.
- Clique **Renderizar** para recalcular.
- Use **Zoom +/−** e as setas para navegar.
- Clique na imagem para dar **zoom** na posição clicada.
- **Salvar PNG**: salva em **PPM** (padrão do Tk). Converta para PNG com `pnmtopng` ou `convert` (ImageMagick).

## Integração entre as linguagens
- O código C é compilado como **biblioteca dinâmica**.
- O Python carrega essa biblioteca com `ctypes.CDLL(...)`.
- O buffer de saída é um array C de `int` com **width×height** posições. O Python aloca e passa o ponteiro para C.
- A função C preenche o buffer com o **número de iterações** até divergência (ou `max_iter` se não divergiu).
- A GUI converte cada valor em uma **cor** (gradiente HSV→RGB) e desenha a imagem usando `PhotoImage.put`.

Assinatura da função C:
```c
int mandelbrot(int width, int height,
               double xmin, double ymin, double xmax, double ymax,
               int max_iter,
               int *out_buffer);
```
