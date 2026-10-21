"""[drawing] Canvas -> SVG (mm units, y flipped to SVG's downward axis)."""
from __future__ import annotations

from xml.sax.saxutils import escape, quoteattr

from .canvas import STYLES

FONT = "DejaVu Sans, Arial, Helvetica, sans-serif"


def _path(pts, h, closed):
    d = "M" + " L".join(f"{x:.3f},{h - y:.3f}" for x, y in pts)
    return d + (" Z" if closed else "")


def _stroke(style):
    s = STYLES[style]
    a = f'stroke="{s["color"]}" stroke-width="{s["width"]}" fill="none" stroke-linecap="round" stroke-linejoin="round"'
    if s["dash"]:
        a += f' stroke-dasharray="{",".join(str(x) for x in s["dash"])}"'
    return a


def _item(it, h, out):
    if it.kind == "poly":
        out.append(f'<path d="{_path(it.pts, h, it.closed)}" {_stroke(it.style)}/>')
    elif it.kind == "fill":
        d = " ".join(_path(r, h, True) for r in it.pts)
        out.append(f'<path d="{d}" fill="#000" fill-rule="evenodd" stroke="none"/>')
    elif it.kind == "text":
        x, y = it.pts
        tr = f' transform="rotate({-it.angle:.2f} {x:.3f} {h - y:.3f})"' if it.angle else ""
        extra = "".join(f" data-{k}={quoteattr(str(v))}" for k, v in it.attrs.items())
        out.append(f'<text x="{x:.3f}" y="{h - y:.3f}" font-size="{it.size}" font-family="{FONT}" '
                   f'text-anchor="{it.anchor}"{tr}{extra}>{escape(it.text)}</text>')
    elif it.kind == "group":
        attrs = "".join(f" data-{k}={quoteattr(str(v))}" for k, v in it.attrs.items() if k != "cls")
        cls = f' class="{it.attrs["cls"]}"' if "cls" in it.attrs else ""
        out.append(f"<g{cls}{attrs}>")
        for c in it.children:
            _item(c, h, out)
        out.append("</g>")


def to_svg(canvas, title="drawing"):
    w, h = canvas.width, canvas.height
    out = [f'<?xml version="1.0" encoding="UTF-8"?>',
           f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}mm" height="{h}mm" viewBox="0 0 {w} {h}">',
           f"<title>{escape(title)}</title>",
           f'<rect x="0" y="0" width="{w}" height="{h}" fill="#ffffff"/>']
    for it in canvas.items:
        _item(it, h, out)
    out.append("</svg>")
    return "\n".join(out)
