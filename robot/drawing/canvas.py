"""[drawing] Display list in sheet millimetres (origin bottom-left, y up): polylines with a line style, filled
regions (build123d sketch faces: arrow heads, dimension text) and plain text. Groups carry attributes, so a
dimension keeps its label and model probe in the SVG for the checker."""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

# ISO 128 line types, widths in mm on the sheet; dash arrays in mm
STYLES = {
    "visible": dict(width=0.35, dash=None, color="#000000"),
    "hidden": dict(width=0.13, dash=(1.6, 0.9), color="#5a5a5a"),
    "center": dict(width=0.13, dash=(8.0, 1.5, 1.0, 1.5), color="#000000"),
    "thin": dict(width=0.18, dash=None, color="#000000"),
    "frame": dict(width=0.7, dash=None, color="#000000"),
    "grid": dict(width=0.25, dash=None, color="#000000"),
}


def fmt(v):
    """Dimension text: 2 decimals when they hold the value to 0.0005 mm, else 3 (a 1.995 chamfer never reads 2.00)."""
    v = float(v)
    s2 = f"{v:.2f}"
    return s2 if abs(float(s2) - v) < 5e-4 else f"{v:.3f}"


@dataclass
class Item:
    kind: str                       # poly | fill | text | group
    pts: object = None              # poly: (k,2); fill: list of rings
    style: str = "thin"
    closed: bool = False
    text: str = ""
    size: float = 3.5
    anchor: str = "start"           # start | middle | end
    angle: float = 0.0
    attrs: dict = field(default_factory=dict)
    children: list = field(default_factory=list)


class Canvas:
    def __init__(self, width, height):
        self.width, self.height = width, height
        self.items: list[Item] = []
        self._stack = [self.items]

    def _add(self, it):
        self._stack[-1].append(it)
        return it

    def poly(self, pts, style="thin", closed=False):
        return self._add(Item("poly", np.asarray(pts, float), style, closed))

    def line(self, a, b, style="thin"):
        return self.poly([a, b], style)

    def rect(self, x0, y0, x1, y1, style="thin"):
        return self.poly([(x0, y0), (x1, y0), (x1, y1), (x0, y1)], style, closed=True)

    def fill(self, rings, style="thin"):
        return self._add(Item("fill", [np.asarray(r, float) for r in rings], style))

    def text(self, xy, s, size=3.5, anchor="start", angle=0.0, attrs=None):
        return self._add(Item("text", np.asarray(xy, float), text=s, size=size, anchor=anchor, angle=angle, attrs=attrs or {}))

    def group(self, **attrs):
        g = Item("group", attrs=attrs)
        self._add(g)
        canvas = self

        class _G:
            def __enter__(self_):
                canvas._stack.append(g.children)
                return g

            def __exit__(self_, *a):
                canvas._stack.pop()
        return _G()

    def sketch(self, sk, style="thin"):
        """Add a build123d Sketch (faces) as filled rings."""
        for f in sk.faces():
            rings = [wire_ring(f.outer_wire())] + [wire_ring(w) for w in f.inner_wires()]
            self.fill(rings, style)

    def walk(self, items=None):
        for it in self.items if items is None else items:
            yield it
            if it.kind == "group":
                yield from self.walk(it.children)


def wire_ring(w, tol=0.03):
    n = int(max(8, min(600, w.length / tol)))
    pts = w.positions([i / n for i in range(n)])
    return np.array([[p.X, p.Y] for p in pts])
