"""[drawing] View placement in third-angle projection with automatic scale, and the occupancy map used to keep
annotation text from overlapping.

Grid (third angle):      top
                  left  front  right
                        bottom
Views in a row share the front view's v (sheet y) alignment, views in the column share its u (sheet x) alignment."""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np

SCALES = (10.0, 5.0, 4.0, 3.0, 2.5, 2.0, 1.5, 1.0, 0.5, 0.2, 0.1)   # enlargement / reduction factors tried, largest first


def scale_label(s):
    return f"{s:g}:1" if s >= 1 else f"1:{1 / s:g}"


@dataclass
class Placement:
    scale: float
    origin: dict          # view name -> sheet xy of the view's model (0,0) point

    def to_sheet(self, view, p2d):
        return self.origin[view] + self.scale * np.asarray(p2d, float)


def _ext(view):
    lo, hi = view.bbox()
    return lo, hi


def place_views(views, region, margins, gap=8.0):
    """views: name -> View (with projected lines). region: (x0, y0, x1, y1) sheet area for the view grid.
    margins: name -> dict(l, r, b, t) sheet mm reserved around each view for its dimensions.
    Returns the Placement with the largest scale in SCALES that fits, centred in the region."""
    ext = {k: _ext(v) for k, v in views.items()}
    size = {k: hi - lo for k, (lo, hi) in ext.items()}
    m = {k: margins.get(k, dict(l=0, r=0, b=0, t=0)) for k in views}
    rx0, ry0, rx1, ry1 = region

    def need(s):
        # widths of the middle row, heights of the middle column (each cell = view size*s + its margins + gap)
        def cw(k):
            return 0 if k not in views else size[k][0] * s + m[k]["l"] + m[k]["r"] + gap

        def ch(k):
            return 0 if k not in views else size[k][1] * s + m[k]["b"] + m[k]["t"] + gap
        return cw("left") + cw("front") + cw("right"), ch("top") + ch("front") + ch("bottom")

    W, H = rx1 - rx0, ry1 - ry0
    s = next((s for s in SCALES if need(s)[0] <= W and need(s)[1] <= H), SCALES[-1])
    tw, th = need(s)
    # front view cell origin so the whole grid is centred
    fl = rx0 + (W - tw) / 2 + (0 if "left" not in views else size["left"][0] * s + m["left"]["l"] + m["left"]["r"] + gap)
    fb = ry0 + (H - th) / 2 + (0 if "bottom" not in views else size["bottom"][1] * s + m["bottom"]["b"] + m["bottom"]["t"] + gap)
    fx = fl + m["front"]["l"] + gap / 2       # sheet x of the front view's left edge
    fy = fb + m["front"]["b"] + gap / 2       # sheet y of its bottom edge
    lo_f, hi_f = ext["front"]
    origin = {"front": np.array([fx, fy]) - s * lo_f}
    # alignment: views in the row share sheet y of the projected model v; left/right views: v == front v (model Y)
    for k in ("left", "right"):
        if k in views:
            lo, hi = ext[k]
            if k == "left":
                x = fx - m["front"]["l"] - gap - m["left"]["r"] - s * hi[0]
            else:
                x = fx + s * size["front"][0] + m["front"]["r"] + gap + m["right"]["l"] - s * lo[0]
            origin[k] = np.array([x, origin["front"][1]])
    for k in ("top", "bottom"):
        if k in views:
            lo, hi = ext[k]
            if k == "top":
                y = fy + s * size["front"][1] + m["front"]["t"] + gap + m["top"]["b"] - s * lo[1]
            else:
                y = fy - m["front"]["b"] - gap - m["bottom"]["t"] - s * hi[1]
            origin[k] = np.array([origin["front"][0], y])
    return Placement(s, origin)


class Occupancy:
    """Axis-aligned boxes already taken on the sheet; text and leaders are placed where they hit none."""

    def __init__(self):
        self.boxes = []

    def add(self, box, tag=""):
        self.boxes.append((tuple(box), tag))

    @staticmethod
    def overlap(a, b, pad=0.0):
        return not (a[2] + pad <= b[0] or b[2] + pad <= a[0] or a[3] + pad <= b[1] or b[3] + pad <= a[1])

    def free(self, box, pad=0.8, ignore=()):
        return all(not self.overlap(box, b, pad) for b, t in self.boxes if t not in ignore)

    def segment_free(self, a, b, ignore=(), shrink=0.3):
        """True if segment a-b crosses no text box (view outlines are allowed: leaders go into the part)."""
        for box, t in self.boxes:
            if t in ignore or not t.startswith("text"):
                continue
            if _seg_box(a, b, (box[0] + shrink, box[1] + shrink, box[2] - shrink, box[3] - shrink)):
                return False
        return True


def _seg_box(a, b, box):
    """Liang-Barsky segment / box intersection."""
    (x0, y0), (x1, y1) = a, b
    dx, dy = x1 - x0, y1 - y0
    t0, t1 = 0.0, 1.0
    for p, q in ((-dx, x0 - box[0]), (dx, box[2] - x0), (-dy, y0 - box[1]), (dy, box[3] - y0)):
        if abs(p) < 1e-12:
            if q < 0:
                return False
        else:
            r = q / p
            if p < 0:
                t0 = max(t0, r)
            else:
                t1 = min(t1, r)
            if t0 > t1:
                return False
    return True
