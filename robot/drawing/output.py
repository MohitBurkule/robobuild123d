"""[drawing] SVG -> PDF / PNG. Tries cairosvg, then rsvg-convert, then a matplotlib replay of the canvas."""
from __future__ import annotations

import shutil
import subprocess
from pathlib import Path


def _cairosvg(svg_path, out, fmt, dpi):
    import cairosvg
    if fmt == "pdf":
        cairosvg.svg2pdf(url=str(svg_path), write_to=str(out))
    else:
        cairosvg.svg2png(url=str(svg_path), write_to=str(out), dpi=dpi, background_color="white")


def _rsvg(svg_path, out, fmt, dpi):
    exe = shutil.which("rsvg-convert")
    if not exe:
        raise RuntimeError("rsvg-convert not found")
    subprocess.run([exe, "-f", fmt, "-d", str(dpi), "-p", str(dpi), "-b", "white", "-o", str(out), str(svg_path)], check=True)


def _matplotlib(canvas, out, fmt, dpi):
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt
    from matplotlib.patches import PathPatch
    from matplotlib.path import Path as MPath
    from .canvas import STYLES
    fig = plt.figure(figsize=(canvas.width / 25.4, canvas.height / 25.4))
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, canvas.width)
    ax.set_ylim(0, canvas.height)
    ax.axis("off")
    pt = 72 / 25.4
    for it in canvas.walk():
        if it.kind == "poly":
            s = STYLES[it.style]
            p = list(it.pts) + ([it.pts[0]] if it.closed else [])
            ls = (0, tuple(d / s["width"] for d in s["dash"])) if s["dash"] else "-"
            ax.plot([q[0] for q in p], [q[1] for q in p], color=s["color"], lw=s["width"] * pt, ls=ls)
        elif it.kind == "fill":
            verts, codes = [], []
            for r in it.pts:
                verts += list(r) + [r[0]]
                codes += [MPath.MOVETO] + [MPath.LINETO] * (len(r) - 1) + [MPath.CLOSEPOLY]
            ax.add_patch(PathPatch(MPath(verts, codes), fc="black", ec="none"))
        elif it.kind == "text":
            ax.text(it.pts[0], it.pts[1], it.text, fontsize=it.size * pt / 0.75 * 0.75, ha={"start": "left", "middle": "center", "end": "right"}[it.anchor],
                    va="baseline", rotation=it.angle)
    fig.savefig(out, dpi=dpi, format=fmt)
    plt.close(fig)


def convert(svg_path, out, canvas=None, dpi=150):
    """Write out (.pdf or .png) from svg_path; returns the converter name used."""
    fmt = Path(out).suffix.lower().lstrip(".")
    errors = []
    for name, fn in (("cairosvg", _cairosvg), ("rsvg-convert", _rsvg)):
        try:
            fn(svg_path, out, fmt, dpi)
            return name
        except Exception as e:      # noqa: BLE001 - try the next converter
            errors.append(f"{name}: {e}")
    if canvas is not None:
        _matplotlib(canvas, out, fmt, dpi)
        return "matplotlib"
    raise RuntimeError("no SVG converter worked: " + "; ".join(errors))
