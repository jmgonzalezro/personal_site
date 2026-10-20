#!/usr/bin/env python3
"""orbits.py — n-cuerpos en ASCII: física simulada y renderizada en texto.

Simula N cuerpos atrayéndose gravitatoriamente (softening + velocity
Verlet) sobre una rejilla ASCII. El campo de brillo decae
exponencialmente entre frames, así que cada cuerpo deja una estela que se
apaga poco a poco. Los últimos frames se desvanecen a negro para que el
bucle del replay no se note.

Solo stdlib, sin dependencias. Dos salidas de la misma simulación:

  * Terminal (modo por defecto), en vivo con ANSI y color truecolor:

        curl -fsSL https://<dominio>/static/orbits.py | python3

  * Web: pregenera los frames y los escribe en JSON comprimido
    (zlib + base64) para que /cv-terminal los reproduzca en bucle:

        python3 orbits.py --size 76x24 --web static/data/orbits-desktop.json
        python3 orbits.py --size 44x20 --web static/data/orbits-mobile.json

El aspecto se corrige con --char-height (alto real de una línea en
unidades de ancho de carácter): la web usa 1.0 (line-height: 1 en el
<pre>), los terminales típicos 1.2. Así los círculos salen circulares.
"""

from __future__ import annotations

import argparse
import base64
import json
import math
import random
import shutil
import sys
import time
import zlib

# Niveles de brillo de menor a mayor. El 0 (espacio) no pinta nada.
RAMP = " .:-=+*#%@"

G = 1.0            # constante gravitatoria (unidades arbitrarias)
M_SUN = 1.0        # masa del cuerpo central
SOFT = 0.012       # softening: evita la singularidad en r -> 0
DT = 0.0009        # paso de integración (el cometa pasa muy pegado al sol)
STEPS_PER_FRAME = 22   # 22 * 0.0009 ≈ 0.02 t por frame
FADE_FRAMES = 12   # desvanecido final para que el bucle no se note
R_SYS = 0.58       # radio efectivo del sistema (órbita exterior + margen)

BRIGHT_SUN = 1.0
BRIGHT_BODY = 0.92   # suficiente para saturar a '@' y verse nítido


def make_bodies(seed: int):
    """Estado inicial: sol + 4 planetas casi circulares + 1 cometa.

    Un par de % de perturbación en las velocidades y masas apreciables
    (más grandes que las reales) para que las órbitas se deformen en los
    pocos segundos del replay sin llegar a volar.
    """
    rng = random.Random(seed)
    bodies = [[0.0, 0.0, 0.0, 0.0, M_SUN]]

    # (radio, ángulo, masa). Masas pequeñas frente al sol: las órbitas
    # se deforman con las interacciones pero no se desestabilizan en el
    # corto tiempo del replay.
    for r, ang, m in (
        (0.24, 0.0, 0.008),
        (0.34, 2.1, 0.012),
        (0.44, 4.0, 0.006),
        (0.53, 0.9, 0.010),
    ):
        v = math.sqrt(G * M_SUN / r) * (1 + rng.uniform(-0.02, 0.02))
        bodies.append([
            r * math.cos(ang),
            r * math.sin(ang),
            -v * math.sin(ang),
            v * math.cos(ang),
            m,
        ])

    # Cometa: órbita interior al planeta más cercano (aphelio < 0.24)
    # para que nunca cruce su trayectoria: los encuentros cercanos a
    # planetas dan slingshots que expulsan cuerpos del sistema.
    peri, ecc = 0.085, 0.27
    a = peri / (1 - ecc)
    v_peri = math.sqrt(G * M_SUN / a * (1 + ecc) / (1 - ecc))
    ang = 5.4  # dirección del perihelio
    bodies.append([
        peri * math.cos(ang),
        peri * math.sin(ang),
        -v_peri * math.sin(ang),
        v_peri * math.cos(ang),
        0.004,
    ])
    return bodies


def accel(bodies):
    n = len(bodies)
    ax = [0.0] * n
    ay = [0.0] * n
    soft2 = SOFT * SOFT
    for i in range(n):
        xi, yi = bodies[i][0], bodies[i][1]
        for j in range(n):
            if i == j:
                continue
            dx = bodies[j][0] - xi
            dy = bodies[j][1] - yi
            inv = 1.0 / ((dx * dx + dy * dy + soft2) ** 1.5)
            ax[i] += G * bodies[j][4] * dx * inv
            ay[i] += G * bodies[j][4] * dy * inv
    return ax, ay


def simulate(cols: int, rows: int, char_h: float, n_frames: int,
             fps: int, decay: float, seed: int) -> list:
    """Devuelve la lista de frames (strings de rows líneas de cols chars)."""
    bodies = make_bodies(seed)
    n = len(bodies)
    # Semiancho del encuadre derivado de la rejilla: el sistema ocupa
    # ~el alto y el ancho disponibles en proporción (0.6 = ancho típico
    # de un carácter monoespaciado en em). Así se ve igual de lleno en
    # escritorio, móvil o terminal grande.
    world_w = R_SYS * 0.6 * cols / (rows * char_h)
    world_h = world_w * rows * char_h / (0.6 * cols)

    # Campo de estela: brillo acumulado que decae cada frame.
    field = [[0.0] * cols for _ in range(rows)]
    ax, ay = accel(bodies)
    frames = []
    bright = [BRIGHT_SUN] + [BRIGHT_BODY] * (n - 1)

    for f in range(n_frames):
        # velocity Verlet
        for _ in range(STEPS_PER_FRAME):
            for i in range(n):
                b = bodies[i]
                b[0] += b[2] * DT + 0.5 * ax[i] * DT * DT
                b[1] += b[3] * DT + 0.5 * ay[i] * DT * DT
            ax2, ay2 = accel(bodies)
            for i in range(n):
                b = bodies[i]
                b[2] += 0.5 * (ax[i] + ax2[i]) * DT
                b[3] += 0.5 * (ay[i] + ay2[i]) * DT
            ax, ay = ax2, ay2

        # los cuerpos brillan siempre en su celda actual
        for i, b in enumerate(bodies):
            cx = int((b[0] + world_w) / (2 * world_w) * (cols - 1))
            cy = int((b[1] + world_h) / (2 * world_h) * (rows - 1))
            if 0 <= cx < cols and 0 <= cy < rows:
                field[cy][cx] += bright[i]

        lines = []
        for row in field:
            lines.append("".join(
                RAMP[min(9, int(v * 10))] for v in row
            ))
        frames.append("\n".join(lines))

        # decaimiento hacia el siguiente frame; al final, fade extra
        fdec = decay * (0.7 if f >= n_frames - FADE_FRAMES else 1.0)
        for r in field:
            for c in range(cols):
                r[c] *= fdec

    return frames


# ------------------------------------------------------------------ web
def pack_web(frames: list, cols: int, rows: int, fps: int) -> str:
    """JSON compacto: meta al claro + frames en zlib+base64.

    La web lo abre con DecompressionStream('deflate') (~10 líneas de JS).
    """
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


# ------------------------------------------------------------- terminal
def level_colors() -> list:
    """Rampa de fósforo verde: nivel 0 (apagado) .. 9 (cuerpo)."""
    out = ["\x1b[0m"]
    for i in range(1, 10):
        t = i / 9
        r = int(20 + 150 * t)
        g = int(70 + 185 * t)
        b = int(35 + 110 * t)
        out.append(f"\x1b[38;2;{r};{g};{b}m")
    return out


def drive(frames: list, fps: int, cols: int, rows: int):
    """Reproduce el replay en la terminal actual (vuelve tras un bucle)."""
    colors = level_colors()
    lvl = {c: i for i, c in enumerate(RAMP)}
    period = 1.0 / fps
    sys.stdout.write("\x1b[?25l")  # ocultar cursor
    sys.stdout.flush()
    try:
        while True:
            t_next = time.perf_counter()
            for frame in frames:
                out = ["\x1b[H"]
                cur = 0
                for line in frame.split("\n"):
                    for ch in line:
                        lv = lvl[ch]
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
            return  # bucle completo: momento de comprobar el tamaño
    finally:
        sys.stdout.write("\x1b[0m\x1b[?25h\n")
        sys.stdout.flush()


def terminal_dims(size: str | None):
    if size:
        cols, rows = parse_size(size)
    else:
        cols, rows = shutil.get_terminal_size()
        cols -= 1  # la última columna exacta provoca wrap+scroll
        rows -= 1
    if cols < 20 or rows < 6:
        sys.exit(f"terminal demasiado pequeño ({cols}x{rows}); mínimo 20x6")
    return cols, rows


def parse_size(s: str) -> tuple:
    try:
        w, h = s.lower().split("x")
        return int(w), int(h)
    except ValueError:
        raise SystemExit(f"--size debe ser anchoxalto, p.ej. 76x24 (recibido: {s})")


def main() -> None:
    p = argparse.ArgumentParser(
        description="n-cuerpos ASCII: replay en terminal o JSON para la web"
    )
    p.add_argument("--size", metavar="WxH",
                   help="rejilla, p.ej. 76x24 (por defecto: tamaño del terminal)")
    p.add_argument("--frames", type=int, default=150, help="frames del replay")
    p.add_argument("--fps", type=int, default=15, help="frames por segundo")
    p.add_argument("--seed", type=int, default=3, help="semilla de la simulación")
    p.add_argument("--decay", type=float, default=0.965,
                   help="decaimiento de estela por frame (0-1)")
    p.add_argument("--char-height", type=float, default=None,
                   help="alto de línea en unidades de ancho de char "
                        "(1.0 = web con line-height 1, 1.2 = terminal típico)")
    p.add_argument("--web", nargs="?", const="-", metavar="RUTA",
                   help="genera el replay JSON ( '-' = stdout ) en vez de reproducir")
    p.add_argument("--preview", type=int, metavar="N",
                   help="imprime el frame N como texto plano y sale")
    args = p.parse_args()

    # --web y --preview usan los defaults de la web si no se indica tamaño
    is_web = args.web is not None or args.preview is not None
    cols, rows = parse_size(args.size) if args.size else (
        (76, 24) if is_web else terminal_dims(None)
    )
    char_h = args.char_height if args.char_height is not None else (1.0 if is_web else 1.2)

    if args.preview is not None:
        frames = simulate(cols, rows, char_h, max(args.preview + 1, args.frames),
                          args.fps, args.decay, args.seed)
        print(frames[args.preview])
        return

    if args.web is not None:
        frames = simulate(cols, rows, char_h, args.frames, args.fps,
                          args.decay, args.seed)
        doc = pack_web(frames, cols, rows, args.fps)
        if args.web == "-":
            sys.stdout.write(doc + "\n")
        else:
            with open(args.web, "w") as fh:
                fh.write(doc + "\n")
            print(f"{args.web}: {cols}x{rows}, {args.frames} frames "
                  f"@ {args.fps}fps, {len(doc):,} bytes", file=sys.stderr)
        return

    # modo terminal: regenera si cambia el tamaño de la ventana
    last = None
    while True:
        cols, rows = terminal_dims(args.size)
        if (cols, rows) != last:
            frames = simulate(cols, rows, char_h, args.frames, args.fps,
                              args.decay, args.seed)
            last = (cols, rows)
        try:
            drive(frames, args.fps, cols, rows)
        except KeyboardInterrupt:
            return


if __name__ == "__main__":
    main()
