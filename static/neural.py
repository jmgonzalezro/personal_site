#!/usr/bin/env python3
"""neural.py — entrena una red neuronal y la dibuja en ASCII.

Una MLP (2 -> h -> 1, tanh + sigmoid, entropía cruzada, Adam) aprende a
separar una espiral de dos brazos. Cada pocas épocas se renderiza un
frame del dashboard: la frontera de decisión sobre el plano, la curva de
loss y las métricas del entrenamiento. Sale un "vídeo" de 10 s.

Solo stdlib, sin dependencias. Dos salidas:

  * Terminal (modo por defecto), en vivo con ANSI y color truecolor:

        curl -fsSL https://<dominio>/static/neural.py | python3

    Entrena (~2-3 s) y reproduce el resultado en bucle. Ctrl+C para salir.

  * Web: pregenera los frames y los escribe en JSON comprimido
    (zlib + base64) para que /cv-terminal los reproduzca:

        python3 neural.py --size 76x24 --web static/data/neural-desktop.json
        python3 neural.py --size 44x36 --web static/data/neural-mobile.json

La frontera de decisión se muestrea con celdas cuadradas (rows ≈ 0.6 *
cols / alto_de_carácter) para que la espiral no salga deformada.
"""

from __future__ import annotations

import argparse
import base64
import json
import math
import os
import random
import shutil
import sys
import time
import zlib

RAMP = " .:-=+*#%@"
DOMAIN = 1.15      # el plano visible es [-DOMAIN, DOMAIN]^2


# ------------------------------------------------------------------ datos
def make_spiral(n_per_class: int, noise: float, rng: random.Random):
    """Espiral de dos brazos entrelazados, normalizada y con ruido."""
    pts, labels = [], []
    for k in range(2):
        for i in range(n_per_class):
            t = i / n_per_class
            r = 0.06 + 0.92 * t
            ang = t * 2.6 * math.pi + k * math.pi
            x = r * math.cos(ang) + rng.gauss(0, noise)
            y = r * math.sin(ang) + rng.gauss(0, noise)
            pts.append([x / 1.15, y / 1.15])
            labels.append(k)
    return pts, labels


# -------------------------------------------------------------------- red
def sigmoid(z: float) -> float:
    if z >= 0:
        return 1.0 / (1.0 + math.exp(-z))
    e = math.exp(z)
    return e / (1.0 + e)


class MLP:
    """Red densa mínima con backprop y Adam. Pesos como listas anidadas."""

    def __init__(self, sizes, rng: random.Random, lr: float):
        self.sizes = sizes
        self.L = len(sizes) - 1
        self.lr = lr
        self.W, self.b = [], []
        for l in range(self.L):
            fan_in, fan_out = sizes[l], sizes[l + 1]
            scale = math.sqrt(2.0 / fan_in)  # He
            self.W.append([[rng.gauss(0.0, scale) for _ in range(fan_in)]
                           for _ in range(fan_out)])
            self.b.append([0.0] * fan_out)
        # estado de Adam
        self.mW = [[[0.0] * sizes[l] for _ in range(sizes[l + 1])]
                   for l in range(self.L)]
        self.vW = [[[0.0] * sizes[l] for _ in range(sizes[l + 1])]
                   for l in range(self.L)]
        self.mb = [[0.0] * sizes[l + 1] for l in range(self.L)]
        self.vb = [[0.0] * sizes[l + 1] for l in range(self.L)]
        self.t = 0

    def forward(self, x):
        acts = [x]
        for l in range(self.L):
            prev = acts[-1]
            z = [self.b[l][j] + sum(w * a for w, a in zip(row, prev))
                 for j, row in enumerate(self.W[l])]
            acts.append([math.tanh(v) for v in z] if l < self.L - 1
                        else [sigmoid(v) for v in z])
        return acts

    def predict(self, x, y) -> float:
        return self.forward([x, y])[-1][0]

    def train_epoch(self, X, Y) -> float:
        n = len(X)
        gW = [[[0.0] * len(row) for row in layer] for layer in self.W]
        gb = [[0.0] * len(bias) for bias in self.b]
        loss = 0.0

        for x, target in zip(X, Y):
            acts = self.forward(x)
            out = acts[-1][0]
            eps = 1e-9
            loss -= target * math.log(out + eps) + (1 - target) * math.log(1 - out + eps)

            # sigmoid + BCE: delta de salida = out - target
            delta = [out - target]
            for l in range(self.L - 1, -1, -1):
                prev = acts[l]
                for j, d in enumerate(delta):
                    gb[l][j] += d
                    row = gW[l][j]
                    for k, a in enumerate(prev):
                        row[k] += d * a
                if l > 0:
                    W = self.W[l]
                    nxt = [0.0] * len(prev)
                    for j, row in enumerate(W):
                        d = delta[j]
                        for k, w in enumerate(row):
                            nxt[k] += d * w
                    delta = [nxt[k] * (1.0 - prev[k] * prev[k])
                             for k in range(len(prev))]

        # Adam con gradiente medio
        self.t += 1
        b1, b2, eps = 0.9, 0.999, 1e-8
        c1 = 1.0 - b1 ** self.t
        c2 = 1.0 - b2 ** self.t
        for l in range(self.L):
            for j in range(len(self.W[l])):
                for k in range(len(self.W[l][j])):
                    g = gW[l][j][k] / n
                    self.mW[l][j][k] = b1 * self.mW[l][j][k] + (1 - b1) * g
                    self.vW[l][j][k] = b2 * self.vW[l][j][k] + (1 - b2) * g * g
                    self.W[l][j][k] -= self.lr * (self.mW[l][j][k] / c1) / (
                        math.sqrt(self.vW[l][j][k] / c2) + eps)
                g = gb[l][j] / n
                self.mb[l][j] = b1 * self.mb[l][j] + (1 - b1) * g
                self.vb[l][j] = b2 * self.vb[l][j] + (1 - b2) * g * g
                self.b[l][j] -= self.lr * (self.mb[l][j] / c1) / (
                    math.sqrt(self.vb[l][j] / c2) + eps)
        return loss / n

    def accuracy(self, X, Y) -> float:
        hits = 0
        for x, t in zip(X, Y):
            hits += (self.predict(x[0], x[1]) >= 0.5) == bool(t)
        return hits / len(X)

    def n_params(self) -> int:
        return sum(len(r) + 1 for layer in self.W for r in layer)


# ----------------------------------------------------------------- render
def frontier(net: MLP, pts, labels, cols: int, rows: int):
    """Mapa de decisión + puntos del dataset, celdas cuadradas."""
    dist = []
    for ry in range(rows):
        y = DOMAIN - (ry + 0.5) * 2 * DOMAIN / rows
        dist.append([
            abs(2 * net.predict(-DOMAIN + (rx + 0.5) * 2 * DOMAIN / cols, y) - 1)
            for rx in range(cols)])

    # Brillo = cercanía a la frontera (p = 0.5), normalizado al rango del
    # propio frame: si no, al principio la red no se separa de 0.5 y el
    # plano entero sale encendido. Normalizado, las primeras épocas se ven
    # como un degradado ancho que se va cerrando en una línea al converger.
    top = max(max(r) for r in dist) or 1.0
    grid = [[RAMP[max(0, min(9, int(9 * (1.0 - d / top) ** 3)))]
             for d in row] for row in dist]

    # Los puntos mandan sobre el fondo, pero no sobre el trazo de la curva:
    # así la frontera queda continua y se lee de un vistazo.
    for (x, y), lab in zip(pts, labels):
        rx = int((x + DOMAIN) / (2 * DOMAIN) * cols)
        ry = int((DOMAIN - y) / (2 * DOMAIN) * rows)
        if 0 <= rx < cols and 0 <= ry < rows and grid[ry][rx] in " .":
            grid[ry][rx] = "o" if lab == 0 else "x"
    return ["".join(r) for r in grid]


def loss_plot(hist, width: int, height: int):
    """Mini-gráfico ASCII del histórico de loss, escalado a su máximo."""
    lines = [[" "] * width for _ in range(height)]
    top = max(hist) or 1.0
    # cada columna resume un tramo del histórico
    for cx in range(width):
        a = cx * len(hist) // width
        b = max(a + 1, (cx + 1) * len(hist) // width)
        v = sum(hist[a:b]) / (b - a)
        row = min(height - 1, int((1.0 - v / top) * (height - 1)))
        lines[row][cx] = "*"
    return ["".join(r) for r in lines]


def bar(value: float, width: int) -> str:
    filled = int(round(value * width))
    return "[" + "#" * filled + "." * (width - filled) + "]"


def compose(frontier_rows, *, epoch, epochs, loss, acc, arch, params,
            hist, lr, points, cols: int, rows: int):
    """Dashboard: frontera a la izquierda (o arriba) y métricas al lado."""
    fcols = len(frontier_rows[0])
    frows = len(frontier_rows)
    out = []

    if cols >= 60:
        # layout lateral: frontera | panel de métricas
        pw = cols - fcols - 2
        plot_w = max(8, pw - 4)
        plot_h = min(10, frows - 12)
        head = [
            "mlp :: spiral",
            "",
            f"loss  {loss:.4f}",
        ]
        plot = loss_plot(hist, plot_w, plot_h) if plot_h >= 3 else []
        tail = [
            "",
            f"acc   {acc * 100:.1f}%",
            bar(acc, max(6, min(18, pw - 8))),
            "",
            f"epoch {epoch}/{epochs}",
            f"arch  2-{arch}-1",
            f"params {params}",
            f"lr    {lr:.2f} adam",
            f"data  {points} pts",
        ]
        panel = head + plot + tail
        for i in range(max(len(panel), frows)):
            left = frontier_rows[i] if i < frows else " " * fcols
            right = panel[i] if i < len(panel) else ""
            out.append(left + " | " + right)
    else:
        # layout apilado: frontera centrada, curva de loss debajo y estado
        pad = " " * max(0, (cols - fcols) // 2)
        plot_h = max(3, min(6, rows - frows - 6))
        out.extend(pad + r for r in frontier_rows)
        out.append("")
        out.append(f"loss {loss:.4f}")
        out.extend(pad + r for r in loss_plot(hist, fcols, plot_h))
        out.append("")
        out.append(f"epoch {epoch}/{epochs}  acc {acc * 100:.1f}%")
        out.append(bar(acc, cols - 9) + f" 2-{arch}-1")
    return "\n".join(out)


def train(cols, rows, char_h, *, epochs, frames, fps, seed, hidden, lr,
          noise, points):
    rng = random.Random(seed)
    X, Y = make_spiral(points, noise, rng)
    net = MLP([2, hidden, 1], rng, lr)

    # geometría de la frontera: celdas cuadradas
    if cols >= 60:
        # lateral: frontera + " | " + panel de métricas (>= 33 cols)
        fcols = min(cols - 36, int((rows - 1) * char_h / 0.6))
        fcols = max(10, fcols)
        frows = int(fcols * 0.6 / char_h)
    else:
        # apilado: frontera a todo el ancho + curva + estado (8 filas)
        fcols = min(cols, 44)
        frows = int(fcols * 0.6 / char_h)
        while frows > rows - 10:
            fcols -= 2
            frows = int(fcols * 0.6 / char_h)
    if fcols < 8 or frows < 6:
        raise SystemExit(f"rejilla demasiado pequeña para el dashboard ({cols}x{rows})")

    hist = []
    out = []
    # Las primeras épocas la red aún no ha salido del 0.5 (el mapa sería
    # un bloque macizo), así que la animación empieza unas cuantas después:
    # el primer frame ya muestra una frontera deforme que se va afinando.
    first = max(1, int(epochs * 0.04))
    every = max(1, (epochs - first) / frames)
    next_at = first
    for epoch in range(1, epochs + 1):
        loss = net.train_epoch(X, Y)
        hist.append(loss)
        if epoch >= next_at or epoch == epochs:
            acc = net.accuracy(X, Y)
            fr = frontier(net, X, Y, fcols, frows)
            out.append(compose(
                fr, epoch=epoch, epochs=epochs, loss=loss, acc=acc,
                arch=hidden, params=net.n_params(), hist=hist, lr=lr,
                points=len(X), cols=cols, rows=rows))
            next_at += every
    return out


# ------------------------------------------------------------------- web
def pack_web(frames, fps) -> str:
    # cols/rows reales del arte (las filas del panel pueden ser menos que
    # las de la rejilla pedida); la web los usa para escalar el <pre>.
    cols = max(max(len(line) for line in f.split("\n")) for f in frames)
    rows = max(len(f.split("\n")) for f in frames)
    doc = {
        "v": 1,
        "cols": cols,
        "rows": rows,
        "fps": fps,
        "count": len(frames),
        "data": base64.b64encode(
            zlib.compress(json.dumps(frames).encode(), 9)
        ).decode(),
    }
    return json.dumps(doc, separators=(",", ":"))


# -------------------------------------------------------------- terminal
CLASS_COLORS = {"o": "\x1b[38;2;80;255;150m", "x": "\x1b[38;2;255;178;102m"}


def level_colors():
    out = ["\x1b[0m"]
    for i in range(1, 10):
        t = i / 9
        out.append(f"\x1b[38;2;{int(20 + 150 * t)};"
                   f"{int(70 + 185 * t)};{int(35 + 110 * t)}m")
    return out


def drive(frames, fps):
    colors = level_colors()
    lvl = {c: i for i, c in enumerate(RAMP)}
    for ch, code in CLASS_COLORS.items():
        colors.append(code)
        lvl[ch] = len(colors) - 1
    period = 1.0 / fps
    sys.stdout.write("\x1b[?25l\x1b[2J")
    sys.stdout.flush()
    try:
        while True:
            t_next = time.perf_counter()
            for frame in frames:
                out = ["\x1b[H"]
                cur = 0
                for line in frame.split("\n"):
                    for ch in line:
                        lv = lvl.get(ch, 0)  # 'o' y 'x' no están en la rampa
                        if lv != cur:
                            out.append(colors[lv])
                            cur = lv
                        out.append(ch)
                    out.append("\x1b[0m\r\n")
                sys.stdout.write("".join(out))
                sys.stdout.flush()
                t_next += period
                wait = t_next - time.perf_counter()
                if wait > 0:
                    time.sleep(wait)
                else:
                    t_next = time.perf_counter()
            return
    finally:
        sys.stdout.write("\x1b[0m\x1b[?25h\n")
        sys.stdout.flush()


# ------------------------------------------------------------------ main
def parse_size(s: str):
    try:
        w, h = s.lower().split("x")
        return int(w), int(h)
    except ValueError:
        raise SystemExit(f"--size debe ser anchoxalto, p.ej. 76x24 (recibido: {s})")


def main():
    p = argparse.ArgumentParser(
        description="entrena una MLP y la dibuja en ASCII (terminal o web)")
    p.add_argument("--size", metavar="WxH", help="rejilla (por defecto: terminal)")
    p.add_argument("--epochs", type=int, default=300)
    p.add_argument("--frames", type=int, default=120)
    p.add_argument("--fps", type=int, default=12)
    p.add_argument("--hidden", type=int, default=16, help="neuronas ocultas")
    p.add_argument("--lr", type=float, default=0.04)
    p.add_argument("--seed", type=int, default=7)
    p.add_argument("--noise", type=float, default=0.045)
    p.add_argument("--points", type=int, default=30,
                   help="puntos por clase de la espiral")
    p.add_argument("--char-height", type=float, default=None,
                   help="alto de línea en unidades de ancho de char "
                        "(1.0 = web con line-height 1, 1.2 = terminal típico)")
    p.add_argument("--web", nargs="?", const="-", metavar="RUTA",
                   help="genera el replay JSON ('-' = stdout) en vez de reproducir")
    p.add_argument("--preview", type=int, metavar="N",
                   help="imprime el frame N y sale")
    args = p.parse_args()

    is_web = args.web is not None or args.preview is not None
    if args.size:
        cols, rows = parse_size(args.size)
    elif is_web:
        cols, rows = 76, 24
    else:
        cols, rows = shutil.get_terminal_size()
        cols, rows = cols - 1, rows - 1
    if cols < 20 or rows < 8:
        sys.exit(f"rejilla demasiado pequeña ({cols}x{rows}); mínimo 20x8")
    char_h = args.char_height if args.char_height is not None else (
        1.0 if is_web else 1.2)

    kw = dict(epochs=args.epochs, frames=args.frames, fps=args.fps,
              seed=args.seed, hidden=args.hidden, lr=args.lr,
              noise=args.noise, points=args.points)

    if args.preview is not None:
        frames = train(cols, rows, char_h, **kw)
        print(frames[min(args.preview, len(frames) - 1)])
        return

    if args.web is not None:
        frames = train(cols, rows, char_h, **kw)
        doc = pack_web(frames, args.fps)
        if args.web == "-":
            sys.stdout.write(doc + "\n")
        else:
            with open(args.web, "w") as fh:
                fh.write(doc + "\n")
            print(f"{args.web}: {cols}x{rows}, {len(frames)} frames "
                  f"@ {args.fps}fps, {len(doc):,} bytes", file=sys.stderr)
        return

    # modo terminal: entrena y reproduce en bucle hasta Ctrl+C
    last = None
    try:
        while True:
            if (cols, rows) != last:
                print(f"# entrenando mlp {2}-{args.hidden}-1 "
                      f"({args.epochs} epocas)…", file=sys.stderr)
                frames = train(cols, rows, char_h, **kw)
                last = (cols, rows)
            drive(frames, args.fps)
            cols, rows = shutil.get_terminal_size()
            cols, rows = cols - 1, rows - 1
    except KeyboardInterrupt:
        return
    except BrokenPipeError:
        # el visitante cortó la salida (p. ej. `| head`): ni rastro de error
        os.dup2(os.open(os.devnull, os.O_WRONLY), sys.stdout.fileno())
        return


if __name__ == "__main__":
    main()
