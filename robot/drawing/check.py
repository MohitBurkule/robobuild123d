"""[drawing] Check: every dimension text on the drawing re-measured on the model (fresh feature recognition, fresh
bounding box) within 0.01 mm, plus the part's named-param cross-checks. Reads the SVG, not the planner's memory, so a
stale or mistyped drawing fails."""
from __future__ import annotations

import json
import re
import xml.etree.ElementTree as ET
from dataclasses import dataclass

import numpy as np

from . import features as F

TOL = 0.01
NUM = re.compile(r"\d+(?:\.\d+)?")


@dataclass
class Result:
    label: str
    expected: list
    shown: list
    ok: bool
    why: str = ""


class Model:
    """Fresh measurements of the shape, independent of the drawing pipeline's cached features."""

    def __init__(self, shape):
        self.shape = shape
        bb = shape.bounding_box()
        self.bmin = np.array([bb.min.X, bb.min.Y, bb.min.Z])
        self.bmax = np.array([bb.max.X, bb.max.Y, bb.max.Z])
        self.holes = F.holes(shape)
        self.fil = F.fillets(shape, hole_list=self.holes)
        self.chs = F.chamfers(shape)

    def hole_at(self, pt, axis):
        pt, axis = np.asarray(pt, float), np.asarray(axis, float)
        for h in self.holes:
            if abs(abs(h.axis @ axis) - 1) > 1e-6:
                continue
            for end in (h.centre, h.centre - h.depth * h.axis):
                if np.linalg.norm(end - pt) < 1e-3:
                    return h
        raise LookupError(f"no hole at {pt}")

    def coord(self, ref, axis):
        axis = np.asarray(axis, float)
        if "bbox" in ref:
            i = ref["i"]
            return (self.bmin if ref["bbox"] == "min" else self.bmax)[i] * axis[i]
        h = self.hole_at(ref["hole"], ref["axis"])
        return float(h.centre @ axis)

    def radius_at(self, pt):
        from build123d import Vector
        best = min(self.fil, key=lambda f: f.face.distance_to(Vector(*pt)))
        if best.face.distance_to(Vector(*pt)) > 1e-3:
            raise LookupError(f"no fillet face at {pt}")
        return best.r

    def chamfer_at(self, pt):
        c = min(self.chs, key=lambda c: np.linalg.norm(c.centre - np.asarray(pt)))
        if np.linalg.norm(c.centre - np.asarray(pt)) > 1e-3:
            raise LookupError(f"no chamfer at {pt}")
        return c

    def probe(self, p):
        k = p["k"]
        if k == "extent":
            return [self.bmax[p["i"]] - self.bmin[p["i"]]]
        if k == "dist":
            return [abs(self.coord(p["b"], p["axis"]) - self.coord(p["a"], p["axis"]))]
        if k == "hole_d":
            h = self.hole_at(p["at"], p["axis"])
            n = sum(1 for g in self.holes if abs(abs(g.axis @ h.axis) - 1) < 1e-6 and abs(g.d - h.d) < 1e-3 and abs(g.depth - h.depth) < 1e-3)
            return ([float(n)] if p.get("n", 1) > 1 else []) + [h.d]
        if k == "hole_depth":
            return [self.hole_at(p["at"], p["axis"]).depth]
        if k == "radius":
            return [self.radius_at(p["at"])]
        if k == "chamfer":
            c = self.chamfer_at(p["at"])
            return [c.leg, c.angle_deg]
        if k == "bbox":
            return [(self.bmin if p["which"] == "min" else self.bmax)[p["i"]]]
        if k == "chamfer_max":
            return [max(c.leg for c in self.chs)]
        if k == "hole_d_near":
            return [self.hole_xy(xy, p["axis"]).d for xy in p["pts"]]
        if k == "hole_xy":
            h = self.hole_xy(p["xy"], p["axis"])
            return list(h.centre[:2])
        raise ValueError(k)

    def hole_xy(self, xy, axis):
        for h in self.holes:
            if abs(abs(h.axis @ np.asarray(axis, float)) - 1) < 1e-6 and np.linalg.norm(h.centre[:2] - np.asarray(xy)) < 0.05:
                return h
        raise LookupError(f"no hole at xy {xy}")


def _numbers(label):
    return [float(x) for x in NUM.findall(label.replace("TYP", ""))]


def check_svg(svg_text, shape, model=None):
    m = model or Model(shape)
    root = ET.fromstring(svg_text)
    out = []
    for g in root.iter("{http://www.w3.org/2000/svg}g"):
        cls = g.get("class")
        if cls not in ("dim", "callout"):
            continue
        label = g.get("data-label")
        probes = json.loads(g.get("data-probe"))
        probes = probes if isinstance(probes, list) else [probes]
        shown = _numbers(label)
        try:
            exp = [v for p in probes for v in m.probe(p)]
        except LookupError as e:
            out.append(Result(label, [], shown, False, str(e)))
            continue
        ok = len(exp) == len(shown) and all(abs(a - b) <= TOL + 1e-9 for a, b in zip(exp, shown))
        out.append(Result(label, [round(x, 4) for x in exp], shown, ok, "" if ok else "text does not match the model"))
    return out


def check_params(info, model):
    out = []
    for name, expected, probe in info.params:
        try:
            got = model.probe(probe)
        except LookupError as e:
            out.append(Result(name, [], [], False, str(e)))
            continue
        exp = list(expected) if isinstance(expected, (tuple, list)) else [expected] * len(got)
        ok = len(exp) == len(got) and all(abs(a - b) <= TOL for a, b in zip(exp, got))
        out.append(Result(name, [round(x, 4) for x in got], exp, ok, "" if ok else "model differs from the named param"))
    return out


def report(results, title):
    bad = [r for r in results if not r.ok]
    lines = [f"{title}: {len(results) - len(bad)}/{len(results)} ok"]
    for r in results:
        lines.append(f"  [{'ok' if r.ok else 'FAIL'}] {r.label}: shown {r.shown} model {r.expected} {r.why}")
    return "\n".join(lines), not bad


# ------------------------------------------------------------------------------------------------ design checks
def check_insert_bores(info, model, undersize=(0.1, 0.4)):
    """Heat-set bores against the insert catalogue: bore = insert OD minus a melt-in interference in `undersize` (mm on dia)."""
    out = []
    for cid, od, pts, axis in info.insert_bores:
        for xy in pts:
            try:
                h = model.hole_xy(xy, axis)
            except LookupError as e:
                out.append(Result(f"{cid} bore at {xy}", [], [], False, str(e)))
                continue
            u = od - h.d
            ok = undersize[0] - 1e-9 <= u <= undersize[1] + 1e-9
            out.append(Result(f"{cid} bore at {xy}", [round(h.d, 4)], [od], ok,
                              "" if ok else f"bore ⌀{h.d:.2f} is {u:.2f} under the {od:.2f} insert OD (want {undersize[0]}..{undersize[1]})"))
    return out


def load_reference(path, matrix=None):
    from build123d import Matrix, import_brep, import_step
    shp = import_brep(str(path)) if str(path).lower().endswith(".brep") else import_step(str(path))
    if matrix is not None:
        shp = shp.transform_geometry(Matrix([list(r) for r in matrix]))
    return shp


def compare_reference(model, ref, tol=TOL, pos_tol=0.05):
    """Our model against the reference (STEP) part: every reference hole present with the same ⌀ / depth, no extra holes;
    fillet face count per (radius, axis) equal; chamfer legs equal."""
    from collections import Counter
    out = []

    def find(h, holes):
        for g in holes:
            if abs(abs(g.axis @ h.axis) - 1) < 1e-6:
                for e1 in (g.centre, g.centre - g.depth * g.axis):
                    for e2 in (h.centre, h.centre - h.depth * h.axis):
                        if np.linalg.norm(e1 - e2) < pos_tol:
                            return g
        return None
    for h in ref.holes:
        g = find(h, model.holes)
        lab = f"hole at {np.round(h.centre, 2).tolist()}"
        if g is None:
            out.append(Result(lab, [round(h.d, 4)], [], False, "missing in our model"))
            continue
        ok = abs(g.d - h.d) <= tol and abs(g.depth - h.depth) <= tol
        out.append(Result(lab, [round(h.d, 4), round(h.depth, 4)], [round(g.d, 4), round(g.depth, 4)], ok, "" if ok else "⌀ / depth differ from the STEP"))
    for g in model.holes:
        if find(g, ref.holes) is None:
            out.append(Result(f"hole at {np.round(g.centre, 2).tolist()}", [], [round(g.d, 4)], False, "not in the STEP"))

    def key(f):
        i = int(np.argmax(np.abs(f.axis)))
        return (round(f.r, 2), "XYZ"[i] if abs(f.axis[i]) > 0.999 else "oblique")
    cr, cm = Counter(key(f) for f in ref.fil), Counter(key(f) for f in model.fil)
    for k in sorted(set(cr) | set(cm), key=lambda k: (k[1], k[0])):
        ok = cr[k] == cm[k]
        out.append(Result(f"fillet R{k[0]:.2f} axis {k[1]} faces", [cr[k]], [cm[k]], ok, "" if ok else "count differs from the STEP"))
    lr = Counter(round(c.leg, 2) for c in ref.chs)
    lm = Counter(round(c.leg, 2) for c in model.chs)
    for k in sorted(set(lr) | set(lm)):
        ok = lr[k] == lm[k]
        out.append(Result(f"chamfer {k:.2f} x 45°", [lr[k]], [lm[k]], ok, "" if ok else "count differs from the STEP"))
    return out
