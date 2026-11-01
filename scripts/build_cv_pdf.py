#!/usr/bin/env python3
"""Genera static/cv.pdf a partir de la página /cv.

La fuente de verdad del CV es templates/cv.html: el PDF se renderiza desde esa
misma página con WeasyPrint, así que no hay dos versiones que mantener. El
servidor de producción no genera nada: sirve el PDF ya commiteado.

Uso:
    ./venv/bin/python scripts/build_cv_pdf.py

WeasyPrint es dependencia solo de desarrollo (está en ./venv, no en
PythonAnywhere).
"""

import sys
import threading
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

from werkzeug.serving import make_server  # noqa: E402
from weasyprint import HTML  # noqa: E402

from app import app  # noqa: E402

OUTPUT = ROOT / "static" / "cv.pdf"


def main() -> int:
    # Puerto efímero en loopback: solo lo usa WeasyPrint para pedir la página,
    # las CSS y las fuentes como lo haría un navegador.
    server = make_server("127.0.0.1", 0, app, threaded=True)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()

    url = f"http://127.0.0.1:{server.server_port}/cv"
    try:
        document = HTML(url).render()
        document.write_pdf(str(OUTPUT))
    finally:
        server.shutdown()
        thread.join(timeout=5)

    pages = len(document.pages)
    size_kb = OUTPUT.stat().st_size / 1024
    print(f"{OUTPUT.relative_to(ROOT)}: {pages} páginas, {size_kb:.0f} KB")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
