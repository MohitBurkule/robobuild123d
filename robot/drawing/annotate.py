"""[drawing] Annotation planning (model space) and rendering (sheet space).

Planning picks, per view, from features recognised on the B-rep:
  * overall extents (from the projected outline, cross-checked against the shape's bounding box),
  * hole callouts "Nx ⌀d ↧depth" grouped by size, and hole centre positions from the view datum (lower-left corner),
  * fillet radii "R r" (cylinders / tori whose axis is the view direction, seen as true arcs on a visible line),
  * chamfers "leg x 45°" (faces seen edge-on),
  * centre marks / centre lines on holes and large arcs.
Rendering uses build123d's drafting objects: ExtensionLine for linear dimensions, ArrowHead + Text for leaders.
Each annotation keeps a probe (what to re-measure on the model), written into the SVG for robot.drawing.check."""
from __future__ import annotations

import json
import math
from dataclasses import dataclass, field

import numpy as np

from . import features as F
from .canvas import fmt

FONT = "DejaVu Sans"
TEXT = 3.5          # sheet mm
STEP = 7.0          # spacing of stacked dimension lines
BASE = 9.0          # first dimension line from the view outline
MAX_RADII = 6       # radius callouts per view
MAX_POS = 6         # hole position dims per direction per view


@dataclass
class LinDim:
    view: str
    a: np.ndarray        # view 2D model coords
    b: np.ndarray
    dirn: str            # "u" (horizontal) or "v" (vertical)
    side: str            # "b", "t", "l", "r"
    level: int
    value: float
    probe: dict
    from_feature: tuple = (False, False)   # draw a thin extension from a / b (inside the view) to the outline


@dataclass
class Callout:
    view: str
    anchor: np.ndarray   # view 2D model coords: arrow tip
    centre: np.ndarray   # arc / hole centre (2D) or None
    text: str
    probes: list
    kind: str


@dataclass
class Mark:
    view: str
    kind: str            # "cross" or "axis"
    a: np.ndarray
    b: np.ndarray = None
    r: float = 0.0


@dataclass
class Plan:
    dims: list = field(default_factory=list)
    callouts: list = field(default_factory=list)
    marks: list = field(default_factory=list)

    def levels(self, view, side):
        return max([d.level + 1 for d in self.dims if d.view == view and d.side == side], default=0)


# ------------------------------------------------------------------------------------------------ visibility helpers
class Lines2D:
    """All visible segments of a view, for 'is this point on a visible line' queries."""

    def __init__(self, polylines):
        segs = [np.stack([p[:-1], p[1:]], 1) for p in polylines if len(p) > 1]
        self.s = np.concatenate(segs) if segs else np.zeros((0, 2, 2))

    def dist(self, p):
        if not len(self.s):
            return np.inf
        a, b = self.s[:, 0], self.s[:, 1]
        ab = b - a
        L = (ab ** 2).sum(1)
        t = np.clip(((p - a) * ab).sum(1) / np.where(L > 0, L, 1), 0, 1)
        q = a + ab * t[:, None]
        return float(np.sqrt(((q - p) ** 2).sum(1)).min())


def _parallel(a, b, tol=1e-3):
    return abs(abs(float(np.dot(a, b))) - 1) < tol


def _circle_edges(face, r):
    from build123d import GeomType
    return [e for e in face.edges() if e.geom_type == GeomType.CIRCLE and abs(e.radius - r) < 1e-4]


# ------------------------------------------------------------------------------------------------ planning
def plan(shape, views, holes=None, fil=None, chs=None, vis_tol=0.02, hole_roles=()):
    """hole_roles: [(d, axis, role)] names a hole size on its callout (role text has no digits, the checker reads numbers)."""
    holes = F.holes(shape) if holes is None else holes
    fil = F.fillets(shape, hole_list=holes) if fil is None else fil
    chs = F.chamfers(shape) if chs is None else chs
    P = Plan()
    bb = shape.bounding_box()
    bmin = np.array([bb.min.X, bb.min.Y, bb.min.Z])
    bmax = np.array([bb.max.X, bb.max.Y, bb.max.Z])
    for name, V in views.items():
        L = Lines2D(V.visible)
        lo, hi = V.bbox()

        def axis3(k):           # model axis of the view's u / v
            return V.u if k == "u" else V.v

        def bb_ref(k, which):   # probe ref of the view outline edge = model bbox min/max along that axis
            ax = axis3(k)
            i = int(np.argmax(np.abs(ax)))
            sgn = ax[i] > 0
            return {"bbox": ("min" if (which == "lo") == sgn else "max"), "i": i}

        # ---- holes seen as circles
        vh = []
        for h in holes:
            if not _parallel(h.axis, V.n):
                continue
            end = h.centre if np.dot(h.axis, V.n) > 0 else h.centre - h.depth * h.axis
            c2 = V.to2d(end)
            rims = [c2 + h.r * np.array([math.cos(t), math.sin(t)]) for t in np.linspace(0, 2 * math.pi, 12, endpoint=False)]
            vis = sum(L.dist(p) < vis_tol for p in rims) >= 6
            P.marks.append(Mark(name, "cross", c2, r=h.r))
            if vis:
                vh.append((h, c2, end))
        # side-on holes: centre line along the axis
        for h in holes:
            if abs(np.dot(h.axis, V.n)) < 1e-3:
                a = V.to2d(h.centre + 1.0 * h.axis)
                b = V.to2d(h.centre - (h.depth + 1.0) * h.axis)
                P.marks.append(Mark(name, "axis", a, b))
        # hole callouts: group visible holes by (d, depth); count all holes of that size / axis in the part
        groups = {}
        for h, c2, end in vh:
            groups.setdefault((round(h.d, 4), round(h.depth, 4)), []).append((h, c2, end))
        for (d, dep), g in sorted(groups.items()):
            n = sum(1 for h in holes if _parallel(h.axis, V.n) and abs(h.d - d) < 1e-3 and abs(h.depth - dep) < 1e-3)
            g.sort(key=lambda x: min(x[1][0] - lo[0], hi[0] - x[1][0], x[1][1] - lo[1], hi[1] - x[1][1]))
            h, c2, end = g[0]
            dirn = np.array([1.0, 1.0]) / math.sqrt(2)
            txt = (f"{n}x " if n > 1 else "") + f"⌀{fmt(h.d)} ↧{fmt(h.depth)}"
            role = next((ro for dd, ax, ro in hole_roles if abs(dd - h.d) < 1e-3 and _parallel(np.asarray(ax, float), h.axis)), None)
            if role:
                assert not any(ch.isdigit() for ch in role), role
                txt += " " + role
            P.callouts.append(Callout(name, c2 + h.r * dirn, c2, txt,
                                      [{"k": "hole_d", "at": end.tolist(), "axis": h.axis.tolist(), "n": n},
                                       {"k": "hole_depth", "at": end.tolist(), "axis": h.axis.tolist()}], "hole"))
        # ---- hole positions from the datum (outline lower-left corner)
        if vh:
            for k, side in (("u", "b"), ("v", "l")):
                j = 0 if k == "u" else 1
                vals = sorted({round(float(c2[j] - lo[j]), 4): (h, c2, end) for h, c2, end in vh}.items())
                vals = [(v, x) for v, x in vals if v > 1e-3][:MAX_POS]
                for lvl, (v, (h, c2, end)) in enumerate(vals):
                    a = lo.copy()
                    b = lo.copy()
                    b[j] = c2[j]
                    if k == "u":
                        a[1] = b[1] = lo[1]
                    else:
                        a[0] = b[0] = lo[0]
                    P.dims.append(LinDim(name, a, b, k, side, lvl, v,
                                         {"k": "dist", "axis": axis3(k).tolist(), "a": bb_ref(k, "lo"),
                                          "b": {"hole": end.tolist(), "axis": h.axis.tolist()}}, (False, True)))
        # ---- fillet radii seen as arcs
        cand = {}
        for f in fil:
            if not _parallel(f.axis, V.n) or f.r < 0.25:
                continue
            best = None
            for e in _circle_edges(f.face, f.r):
                pm = V.to2d(np.array(tuple(e.position_at(0.5))))
                if L.dist(pm) < vis_tol:
                    c2 = V.to2d(np.array(tuple(e.arc_center)))
                    edge_d = min(pm[0] - lo[0], hi[0] - pm[0], pm[1] - lo[1], hi[1] - pm[1])
                    if best is None or edge_d < best[0]:
                        best = (edge_d, pm, c2, np.array(tuple(e.position_at(0.5))))
            if best:
                cand.setdefault(fmt(f.r), []).append((best, f))
        ranked = sorted(cand.items(), key=lambda kv: (-len(kv[1]), -float(kv[0])))[:MAX_RADII]
        for rs, lst in sorted(ranked, key=lambda kv: float(kv[0])):
            lst.sort(key=lambda x: x[0][0])
            (ed, pm, c2, p3), f = lst[0]
            txt = f"R{rs}" + (" TYP" if len(lst) > 1 else "")
            P.callouts.append(Callout(name, pm, c2, txt, [{"k": "radius", "at": p3.tolist(), "axis": f.axis.tolist()}], "radius"))
            if f.r >= 3.0:
                P.marks.append(Mark(name, "cross", c2, r=f.r * 0.6))
        # ---- chamfers seen edge-on
        cg = {}
        for c in chs:
            if abs(np.dot(c.normal, V.n)) > 1e-3:
                continue
            from build123d import GeomType
            lng = max((e for e in c.face.edges() if e.geom_type == GeomType.LINE), key=lambda e: e.length)
            if not _parallel(np.array(tuple(lng.tangent_at(0))), V.n):
                continue
            p2 = V.to2d(c.centre)
            if L.dist(p2) < vis_tol:
                cg.setdefault(fmt(c.leg), []).append((p2, c))
        for ls, lst in sorted(cg.items()):
            lst.sort(key=lambda x: min(x[0][0] - lo[0], hi[0] - x[0][0], x[0][1] - lo[1], hi[1] - x[0][1]))
            p2, c = lst[0]
            n2 = V.to2d(c.normal)
            txt = f"{ls} x 45°" + (" TYP" if len(lst) > 1 else "")
            P.callouts.append(Callout(name, p2, p2 - n2, txt, [{"k": "chamfer", "at": c.centre.tolist()}], "chamfer"))
    # ---- a mirror view (right vs left, bottom vs top) repeats its partner's callouts and dims: keep them on one only
    for a, b in (("left", "right"), ("top", "bottom")):
        if a in views and b in views:
            ka = sorted(c.text for c in P.callouts if c.view == a) + sorted(fmt(d.value) for d in P.dims if d.view == a)
            kb = sorted(c.text for c in P.callouts if c.view == b) + sorted(fmt(d.value) for d in P.dims if d.view == b)
            if set(kb) <= set(ka):
                P.callouts = [c for c in P.callouts if c.view != b]
                P.dims = [d for d in P.dims if d.view != b]
    # ---- overall extents: width + length in the front view, height in the left (or first side) view
    def overall(view, k, side):
        V = views[view]
        lo, hi = V.bbox()
        j = 0 if k == "u" else 1
        a, b = lo.copy(), lo.copy()
        b[j] = hi[j]
        ax = V.u if k == "u" else V.v
        i = int(np.argmax(np.abs(ax)))
        lvl = P.levels(view, side)
        P.dims.append(LinDim(view, a, b, k, side, lvl, float(hi[j] - lo[j]), {"k": "extent", "i": i}))
    if "front" in views:
        overall("front", "u", "b")
        overall("front", "v", "l")
    side = "left" if "left" in views else ("right" if "right" in views else None)
    if side:
        overall(side, "u", "b")
        if "front" not in views:
            overall(side, "v", "l")
    return P


def margins(P, views):
    """Sheet mm needed around each view for its stacked dimension lines (callouts are placed later, in the gaps)."""
    out = {}
    for v in views:
        out[v] = {s: (BASE + STEP * (P.levels(v, s) - 1) + TEXT + 3 if P.levels(v, s) else 6.0) for s in "lrbt"}
        for s in "lrbt":
            out[v][s] = max(out[v][s], 14.0)   # room for leader text
    return out


# ------------------------------------------------------------------------------------------------ rendering
def _draft():
    from build123d import Draft
    return Draft(font_size=TEXT, font=FONT, arrow_length=2.8, line_width=0.18, pad_around_text=1.0,
                 extension_gap=1.0, decimal_precision=2, display_units=False)


def view_box(pl, V):
    lo, hi = V.bbox()
    a, b = pl.to_sheet(V.name, lo), pl.to_sheet(V.name, hi)
    return (min(a[0], b[0]), min(a[1], b[1]), max(a[0], b[0]), max(a[1], b[1]))


def render_dims(canvas, P, views, pl, occ):
    from build123d import ExtensionLine
    draft = _draft()
    for d in P.dims:
        V = views[d.view]
        box = view_box(pl, V)
        A, B = pl.to_sheet(d.view, d.a), pl.to_sheet(d.view, d.b)
        dist = BASE + STEP * d.level
        if d.side == "b":
            y = box[1]
            pa, pb, off = (A[0], y), (B[0], y), (0, -dist)
        elif d.side == "t":
            y = box[3]
            pa, pb, off = (A[0], y), (B[0], y), (0, dist)
        elif d.side == "l":
            x = box[0]
            pa, pb, off = (x, A[1]), (x, B[1]), (-dist, 0)
        else:
            x = box[2]
            pa, pb, off = (x, A[1]), (x, B[1]), (dist, 0)
        label = fmt(d.value)
        ext = ExtensionLine([pa, pb], offset=off, draft=draft, label=label)
        assert abs(ext.dimension - d.value * pl.scale) < 1e-6, (d, ext.dimension)
        with canvas.group(cls="dim", label=label, value=f"{d.value:.6f}", probe=json.dumps(d.probe), view=d.view):
            canvas.sketch(ext)
            for flag, P0, pe in ((d.from_feature[0], A, pa), (d.from_feature[1], B, pb)):
                if flag:
                    v = np.asarray(pe) - P0
                    n = np.linalg.norm(v)
                    if n > 1.5:
                        canvas.line(P0 + v / n * 1.0, np.asarray(pe) + v / n * 1.0, "thin")
        bb = ext.bounding_box()
        occ.add((bb.min.X, bb.min.Y, bb.max.X, bb.max.Y), "text-dim")


def render_marks(canvas, P, views, pl):
    for m in P.marks:
        s = pl.scale
        if m.kind == "cross":
            c = pl.to_sheet(m.view, m.a)
            e = m.r * s + 2.0
            canvas.line((c[0] - e, c[1]), (c[0] + e, c[1]), "center")
            canvas.line((c[0], c[1] - e), (c[0], c[1] + e), "center")
        else:
            canvas.line(pl.to_sheet(m.view, m.a), pl.to_sheet(m.view, m.b), "center")


def _text_sketch(s):
    from build123d import Align, Text
    return Text(s, TEXT, font=FONT, align=(Align.MIN, Align.CENTER))


def render_callouts(canvas, P, views, pl, occ):
    """Leader + text; the text goes on the first free spot along the radial direction, then the compass rose."""
    from build123d import ArrowHead, HeadType, Pos, Rot
    placed, skipped, leaders = [], [], []
    for co in P.callouts:
        V = views[co.view]
        box = view_box(pl, V)
        A = pl.to_sheet(co.view, co.anchor)
        C = pl.to_sheet(co.view, co.centre) if co.centre is not None else None
        sk = _text_sketch(co.text)
        bb = sk.bounding_box()
        w, h = bb.size.X, bb.size.Y
        dirs = []
        if C is not None and np.linalg.norm(A - C) > 1e-6:
            r = (A - C) / np.linalg.norm(A - C)
            dirs += [r, -r]
        for ang in range(0, 360, 30):
            dirs.append(np.array([math.cos(math.radians(ang)), math.sin(math.radians(ang))]))
        choice = None
        for k, dv in enumerate(dirs):
            exit_d = _exit(A, dv, box)
            for extra in (4.0, 8.0, 13.0, 19.0, 26.0, 34.0):
                T = A + dv * (exit_d + extra)
                right = dv[0] >= -1e-9
                tb = (T[0] + 1.0, T[1] - h / 2 - 0.6, T[0] + 1.0 + w, T[1] + h / 2 + 0.6) if right else \
                     (T[0] - 1.0 - w, T[1] - h / 2 - 0.6, T[0] - 1.0, T[1] + h / 2 + 0.6)
                if not (occ.free(tb) and occ.segment_free(A, T) and not any(_seg_cross(A, T, a, b) for a, b in leaders)):
                    continue
                # cost: leader length, the part of it drawn over the view counts double, non-radial leaders pay a little
                cost = exit_d + extra + exit_d + (0.0 if k < 2 else 4.0)
                if choice is None or cost < choice[3]:
                    choice = (T, tb, right, cost)
                break
        if not choice:
            skipped.append(co)
            continue
        T, tb, right, _ = choice
        occ.add(tb, "text-callout")
        leaders.append((A, T))
        attrs = dict(cls="callout", label=co.text, probe=json.dumps(co.probes), view=co.view, kind=co.kind)
        with canvas.group(**attrs):
            canvas.line(A, T, "thin")
            shoulder = (T[0] + (1.0 if right else -1.0), T[1])
            canvas.line(T, shoulder, "thin")
            ang = math.degrees(math.atan2(A[1] - T[1], A[0] - T[0]))
            canvas.sketch(Pos(A[0], A[1]) * Rot(0, 0, ang) * ArrowHead(2.8, HeadType.CURVED))
            x = tb[0]
            canvas.sketch(Pos(x, T[1]) * sk)
        placed.append(co)
    return placed, skipped


def _exit(A, d, box):
    """Distance along d from A to leave the box (0 if A is outside it)."""
    ts = []
    for i, (lo, hi) in enumerate(((box[0], box[2]), (box[1], box[3]))):
        if abs(d[i]) > 1e-12:
            ts.append(((hi if d[i] > 0 else lo) - A[i]) / d[i])
    t = min(ts) if ts else 0.0
    return max(t, 0.0)


def _seg_cross(p1, p2, q1, q2):
    """Proper intersection of two segments (shared end points do not count)."""
    def orient(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])
    d1, d2 = orient(q1, q2, p1), orient(q1, q2, p2)
    d3, d4 = orient(p1, p2, q1), orient(p1, p2, q2)
    return d1 * d2 < -1e-9 and d3 * d4 < -1e-9
