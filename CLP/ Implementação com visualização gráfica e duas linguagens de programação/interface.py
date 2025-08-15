# src/interface.py
# GUI em Python (Tkinter) que chama a biblioteca C via ctypes para calcular
# o conjunto de Mandelbrot e exibir a imagem.
# Dependências: apenas Python 3 (Tkinter faz parte da biblioteca padrão).
#
# Execução:
#   1) Compile a lib C (make all)
#   2) Rode: python3 src/interface.py  (ou `make run`)
#
import os
import sys
import ctypes
import math
import tkinter as tk
from tkinter import ttk, messagebox, filedialog

# Tenta carregar a biblioteca compartilhada com nomes típicos por SO.
def load_mandelbrot_lib():
    here = os.path.dirname(os.path.abspath(__file__))
    root = os.path.dirname(here)
    candidates = [
        os.path.join(root, "mandelbrot.so"),        # Linux/macOS
        os.path.join(root, "mandelbrot.dylib"),     # macOS (alternativo)
        os.path.join(root, "mandelbrot.dll"),       # Windows
        os.path.join(here, "mandelbrot.so"),
        os.path.join(here, "mandelbrot.dylib"),
        os.path.join(here, "mandelbrot.dll"),
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ctypes.CDLL(path)
            except OSError:
                pass
    raise FileNotFoundError("Não foi possível encontrar/abrir a biblioteca C (mandelbrot.so/.dll). Compile com `make`.")

lib = load_mandelbrot_lib()
# Define a assinatura da função C
lib.mandelbrot.argtypes = [
    ctypes.c_int, ctypes.c_int,
    ctypes.c_double, ctypes.c_double, ctypes.c_double, ctypes.c_double,
    ctypes.c_int,
    ctypes.POINTER(ctypes.c_int),
]
lib.mandelbrot.restype = ctypes.c_int

class MandelbrotApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Mandelbrot: C + Python (Tkinter)")
        self.geometry("980x700")
        self.resizable(True, True)

        # Parâmetros padrão
        self.width = tk.IntVar(value=800)
        self.height = tk.IntVar(value=600)
        self.max_iter = tk.IntVar(value=500)
        self.xmin = tk.DoubleVar(value=-2.5)
        self.xmax = tk.DoubleVar(value=1.0)
        self.ymin = tk.DoubleVar(value=-1.25)
        self.ymax = tk.DoubleVar(value=1.25)

        self._build_ui()

        # Render inicial
        self.render_image()

    def _build_ui(self):
        # Painel de controle
        controls = ttk.Frame(self, padding=8)
        controls.pack(side=tk.TOP, fill=tk.X)

        def add_labeled(entry_parent, label_text, var, width=8):
            frame = ttk.Frame(entry_parent)
            ttk.Label(frame, text=label_text).pack(side=tk.LEFT)
            if isinstance(var, tk.IntVar):
                ent = ttk.Entry(frame, textvariable=var, width=width)
            else:
                ent = ttk.Entry(frame, textvariable=var, width=width)
            ent.pack(side=tk.LEFT, padx=(4, 12))
            frame.pack(side=tk.LEFT)
            return ent

        add_labeled(controls, "Largura:", self.width, 6)
        add_labeled(controls, "Altura:", self.height, 6)
        add_labeled(controls, "Iterações:", self.max_iter, 6)
        add_labeled(controls, "xmin:", self.xmin, 8)
        add_labeled(controls, "xmax:", self.xmax, 8)
        add_labeled(controls, "ymin:", self.ymin, 8)
        add_labeled(controls, "ymax:", self.ymax, 8)

        ttk.Button(controls, text="Renderizar", command=self.render_image).pack(side=tk.LEFT, padx=6)
        ttk.Button(controls, text="Zoom +", command=lambda: self.zoom(0.5)).pack(side=tk.LEFT, padx=2)
        ttk.Button(controls, text="Zoom -", command=lambda: self.zoom(2.0)).pack(side=tk.LEFT, padx=2)
        ttk.Button(controls, text="←", command=lambda: self.pan(-0.2, 0.0)).pack(side=tk.LEFT, padx=2)
        ttk.Button(controls, text="→", command=lambda: self.pan(0.2, 0.0)).pack(side=tk.LEFT, padx=2)
        ttk.Button(controls, text="↑", command=lambda: self.pan(0.0, -0.2)).pack(side=tk.LEFT, padx=2)
        ttk.Button(controls, text="↓", command=lambda: self.pan(0.0, 0.2)).pack(side=tk.LEFT, padx=2)
        ttk.Button(controls, text="Salvar PNG", command=self.save_png).pack(side=tk.LEFT, padx=6)

        # Canvas para a imagem
        self.canvas_frame = ttk.Frame(self, padding=8)
        self.canvas_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
        self.canvas = tk.Canvas(self.canvas_frame, width=self.width.get(), height=self.height.get(), bg="black")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # click para zoom
        self.canvas.bind("<Button-1>", self.on_click_zoom)

    def on_click_zoom(self, event):
        # recentra na posição clicada e dá zoom
        w = self.width.get()
        h = self.height.get()
        x = self.xmin.get() + (self.xmax.get() - self.xmin.get()) * (event.x / max(1, self.canvas.winfo_width()))
        y = self.ymin.get() + (self.ymax.get() - self.ymin.get()) * (event.y / max(1, self.canvas.winfo_height()))
        cx = (self.xmin.get() + self.xmax.get())/2.0
        cy = (self.ymin.get() + self.ymax.get())/2.0
        dx = (self.xmax.get() - self.xmin.get())
        dy = (self.ymax.get() - self.ymin.get())
        # Recentrar na posição clicada
        self.xmin.set(x - dx/4.0); self.xmax.set(x + dx/4.0)
        self.ymin.set(y - dy/4.0); self.ymax.set(y + dy/4.0)
        self.render_image()

    def pan(self, fx, fy):
        # desloca a janela em frações do tamanho atual
        dx = (self.xmax.get() - self.xmin.get()) * fx
        dy = (self.ymax.get() - self.ymin.get()) * fy
        self.xmin.set(self.xmin.get() + dx)
        self.xmax.set(self.xmax.get() + dx)
        self.ymin.set(self.ymin.get() + dy)
        self.ymax.set(self.ymax.get() + dy)
        self.render_image()

    def zoom(self, factor):
        # zoom em torno do centro
        cx = (self.xmin.get() + self.xmax.get())/2.0
        cy = (self.ymin.get() + self.ymax.get())/2.0
        half_w = (self.xmax.get() - self.xmin.get())/2.0 * factor
        half_h = (self.ymax.get() - self.ymin.get())/2.0 * factor
        self.xmin.set(cx - half_w)
        self.xmax.set(cx + half_w)
        self.ymin.set(cy - half_h)
        self.ymax.set(cy + half_h)
        self.render_image()

    def _compute(self, w, h, xmin, ymin, xmax, ymax, max_iter):
        # buffer de inteiros
        buf = (ctypes.c_int * (w * h))()
        rc = lib.mandelbrot(w, h, xmin, ymin, xmax, ymax, max_iter, buf)
        if rc != 0:
            raise RuntimeError(f"mandelbrot() retornou erro {rc}")
        return buf

    def _palette(self, max_iter):
        # Gera uma paleta simples (gradiente HSV -> RGB), mas sem dependências externas.
        # Retorna lista de strings "#RRGGBB".
        palette = []
        for i in range(max_iter + 1):
            t = i / max_iter if max_iter > 0 else 0.0
            # HSV a RGB (h = 360*t, s=1, v=1)
            h = 6.0 * t
            c = 1.0
            x = c * (1.0 - abs((h % 2) - 1.0))
            if   0 <= h < 1: r, g, b = c, x, 0
            elif 1 <= h < 2: r, g, b = x, c, 0
            elif 2 <= h < 3: r, g, b = 0, c, x
            elif 3 <= h < 4: r, g, b = 0, x, c
            elif 4 <= h < 5: r, g, b = x, 0, c
            else:            r, g, b = c, 0, x
            # aplica valor (v=1)
            R = int(r * 255); G = int(g * 255); B = int(b * 255)
            palette.append(f"#{R:02x}{G:02x}{B:02x}")
        # cor para pontos "dentro" (iter == max_iter): preto
        palette[-1] = "#000000"
        return palette

    def _buffer_to_photoimage(self, buf, w, h, max_iter):
        # Converte o buffer de iterações para uma PhotoImage via 'put' por linha.
        img = tk.PhotoImage(width=w, height=h)
        pal = self._palette(max_iter)
        idx = 0
        for y in range(h):
            # Constrói a linha como lista de cores para eficiência
            row_colors = []
            base = y * w
            for x in range(w):
                it = buf[base + x]
                if it < 0: it = 0
                if it > max_iter: it = max_iter
                row_colors.append(pal[it])
            # Tkinter aceita: {#rrggbb #rrggbb ...}
            img.put("{" + " ".join(row_colors) + "}", to=(0, y))
        return img

    def render_image(self):
        try:
            w = max(50, int(self.width.get()))
            h = max(50, int(self.height.get()))
            max_it = max(10, int(self.max_iter.get()))
            xmin = float(self.xmin.get())
            xmax = float(self.xmax.get())
            ymin = float(self.ymin.get())
            ymax = float(self.ymax.get())

            self.canvas.config(width=w, height=h)
            buf = self._compute(w, h, xmin, ymin, xmax, ymax, max_it)
            img = self._buffer_to_photoimage(buf, w, h, max_it)

            # Exibe no canvas
            self.canvas.delete("all")
            self.image_for_canvas = img  # manter referência
            self.canvas.create_image(0, 0, anchor=tk.NW, image=img)
        except Exception as e:
            messagebox.showerror("Erro", str(e))

    def save_png(self):
        try:
            # Exporta como PPM (nativo do Tk) e, se possível, converte para PNG com 'pnmtopng' se instalado.
            w = self.canvas.winfo_width()
            h = self.canvas.winfo_height()
            if w <= 1 or h <= 1:
                w = self.width.get()
                h = self.height.get()
            # Renderiza novamente para garantir o tamanho correto
            self.render_image()

            fpath = filedialog.asksaveasfilename(defaultextension=".ppm", filetypes=[("PPM", "*.ppm"), ("All files", "*.*")])
            if not fpath:
                return
            # PhotoImage permite escrever em PPM via 'write'
            self.image_for_canvas.write(fpath, format="ppm")
            messagebox.showinfo("Salvo", f"Imagem salva em {fpath}\nVocê pode converter PPM→PNG com ferramentas como ImageMagick (convert) ou pnmtopng.")
        except Exception as e:
            messagebox.showerror("Erro ao salvar", str(e))

if __name__ == "__main__":
    app = MandelbrotApp()
    app.mainloop()
