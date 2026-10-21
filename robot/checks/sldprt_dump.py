"""Parity of our parts with the SolidWorks macro dumps (`research/sldprt/dumps_v2/<part>.dump.txt`, faces per feature;
`dumps/` when v2 is absent): exact reference radii, holes and extrude depths, checked at code / geometry level
(point-to-surface queries on our mesh, no slicing). Format: research/sldprt/dumps/FORMAT.md.

Spec: a `reference_cad` entry is matched to a dump by `dump` (file stem, e.g. "RV17 Wedgelet LH") or, failing that, by
its STL name with the instance suffix dropped (RV17_Wedgelet_LH_1.stl -> "RV17 Wedgelet LH"). `sldprt_dumps` (top level
of the spec, default DEFAULT_ROOT) holds `dumps_v2/` / `dumps/`.
The dump's part frame is registered onto the reference STL (which is in the STEP = SolidWorks assembly frame): rigid ICP
of exact surface points of the dump's faces, started from the asmdump component transforms of that part (asm_dump), or
from the 48 signed axis permutations when none fits. An 80th-percentile point gap over REG_RMS_MM means the dump is a
different revision of the part (e.g. RV23 vs the STEP's) and the entry is NOT CHECKED. `dump_to_ref` (4x4, mm) on the
entry overrides the fit. Then, in our world frame (reference_cad.ref_in_world):
  dump.fillet (BLOCKER)  every fillet / chamfer face of the reference (exact radius from the dump, its face from the v2
                         dump, pattern copies included) has our surface within TOL_MM (+ the reference STL's own
                         tessellation error at that point) at sample points on the face: same place, same radius.
  dump.hole (BLOCKER)    every closed sketch circle of a boss / cut extrude (centre, diameter, end condition, depth):
                         points on its wall over the extruded depth that the reference STL still shows lie on our surface.
  dump.extrude (BLOCKER) every blind extrude whose end cap face survives in the reference: the cap lies at the dumped
                         depth on our part.
A sample the reference STL itself does not show (a later feature or pattern changed it) is not compared.
Opt-out: a miss is excused only by the entry's `deviations` (near/path + reason citing the reference), as for
reference_cad.diff. Parts without a usable dump are listed as NOT CHECKED (never a pass).
Also feeds exact values to the estimators: exact_for() -> visual.fillet_ref (reference radius snapped to the dumped
radius) and reference_cad.features (reference hole diameter snapped to the dumped circle).
"""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

import numpy as np

from ..finding import BLOCKER, WARNING, fail, note, ok

G = "reference"
TOL_MM = 0.05
REG_RMS_MM = 0.15     # 80 % of the dump's surface points must lie this close to the reference STL (its chord sag included)
DEFAULT_ROOT = "/mnt/project-files/robot-cad/research/sldprt"
# SolidWorks swEndConditions_e
END = {0: "blind", 1: "through_all", 2: "up_to_next", 3: "up_to_vertex", 4: "up_to_surface", 5: "offset_from_surface",
       6: "mid_plane", 7: "up_to_body", 9: "through_all_both"}

_F = re.compile(r"^FEATURE (-?\d+) \| (.*) \| (\w+) \| id=(-?\d+) \| suppressed=(\w+)")
_KV = re.compile(r"(\w+)=(\([^)]*\)|\S+)")


def _vec(s):
    return [float(x) for x in s.strip("()").split(",")]


def _num(v):
    if v.startswith("("):
        return _vec(v)
    if v in ("True", "False"):
        return v == "True"
    try:
        return float(v) if any(c in v for c in ".eE") else int(v)
    except ValueError:
        return v


# ------------------------------------------------------------------------------------------------ parsing (pure)
def parse_face(rest):
    """A v2 `FACE` line (after the keyword) -> {type, box (6, m), area, ...} in metres: plane {n, o}; cyl {o, ax, r};
    cone {o, ax, r, half} (positional); torus {o, ax, R, r}; sphere / surf: box only."""
    t, _, body = rest.partition(" ")
    box = re.search(r"box=([^ ]+)", body)
    if not box:
        return None
    f = {"type": t, "box": np.asarray([float(x) for x in box[1].split(",") if x], float)}
    kv = dict(_KV.findall(body))
    if "area" in kv:
        f["area"] = float(kv["area"].rstrip(","))
    if t == "plane":
        f["n"], f["o"] = np.asarray(_vec(kv["n"])), np.asarray(_vec(kv["o"]))
    elif t == "cyl":
        f["o"], f["ax"], f["r"] = np.asarray(_vec(kv["o"])), np.asarray(_vec(kv["ax"])), float(kv["r"])
    elif t in ("cone", "torus"):
        v = [float(x) for x in body.split(" box=")[0].split(",") if x.strip()]
        if len(v) >= 8:
            f["o"], f["ax"] = np.asarray(v[:3]), np.asarray(v[3:6])
            f.update({"r": v[6], "half": v[7]} if t == "cone" else {"R": v[6], "r": v[7]})
    return f


def parse(text):
    """{'part', 'features': [{n, name, type, id, suppressed, dims{}, parents[], extrude{}, fillet{}, sketch{}}]} from a
    dump. Units stay as dumped (metres, radians). Lines of a nested `FEATURE -1` block (a copy of the feature's sketch)
    are skipped: the sketch is read where it is defined."""
    part, feats, cur, nested = None, [], None, False
    for raw in text.splitlines():
        line = raw.strip()
        if raw.startswith("PART "):
            part = raw[5:].strip()
            continue
        m = _F.match(line)
        if m:
            if raw.startswith("FEATURE"):
                cur = {"n": int(m[1]), "name": m[2], "type": m[3], "id": int(m[4]), "suppressed": m[5] == "True",
                       "dims": {}, "parents": []}
                feats.append(cur)
                nested = False
            else:
                nested = True
            continue
        if cur is None or nested or not line:
            continue
        key, _, rest = line.partition(" ")
        if key == "DIM":
            k, _, v = rest.rpartition(" = ")
            cur["dims"][k.split("@")[0] + "@" + k.split("@")[1] if "@" in k else k] = float(v)
        elif key == "PARENT":
            cur["parents"].append(rest.split(" | ")[0])
        elif key in ("EXTRUDE", "FILLET"):
            cur[key.lower()] = {k: _num(v) for k, v in _KV.findall(rest)}
        elif key == "SKETCH_TO_MODEL":
            cur.setdefault("sketch", {"pts": {}, "segs": [], "contours": []})["xf"] = [float(x) for x in rest.split(",") if x]
        elif key == "PT":
            pid, _, v = rest.partition(" ")
            cur.setdefault("sketch", {"pts": {}, "segs": [], "contours": []})["pts"][pid] = _vec(v)
        elif key == "SEG":
            sid, _, kv = rest.partition(" ")
            d = {k: _num(v) for k, v in _KV.findall(kv)}
            d["id"] = sid
            cur.setdefault("sketch", {"pts": {}, "segs": [], "contours": []})["segs"].append(d)
        elif key == "CONTOUR":
            kv = dict(_KV.findall(rest))
            cur.setdefault("sketch", {"pts": {}, "segs": [], "contours": []})["contours"].append(
                {"closed": kv.get("closed") == "True", "segs": rest.split("segs=", 1)[1].split()})
        elif key == "FACES":
            cur["n_faces"] = int(rest)
        elif key == "FACE":
            f = parse_face(rest)
            if f is not None:
                cur.setdefault("faces", []).append(f)
    return {"part": part, "features": feats}


def sketch_xf(xf):
    """4x4 (metres) sketch -> part from a SKETCH_TO_MODEL MathTransform array (rows of the 3x3 are the images of the
    sketch X, Y, Z axes; then translation, scale)."""
    R = np.asarray(xf[:9], float).reshape(3, 3)
    T = np.eye(4)
    T[:3, :3] = R.T * (xf[12] if len(xf) > 12 and xf[12] else 1.0)
    T[:3, 3] = xf[9:12]
    return T


def radii(dump):
    """Exact fillet radii and chamfer distances (mm) of the unsuppressed features: {'fillet': [...], 'chamfer': [...]}."""
    out = {"fillet": [], "chamfer": []}
    for f in dump["features"]:
        if f["suppressed"]:
            continue
        if f["type"] == "Fillet" and f.get("fillet") and f["fillet"].get("r"):
            out["fillet"].append(round(f["fillet"]["r"] * 1e3, 4))
        elif f["type"] == "Chamfer":
            d = [v for k, v in f["dims"].items() if k.startswith("D1@")]
            if d:
                out["chamfer"].append(round(d[0] * 1e3, 4))
    return out


def circles(dump):
    """[{feature, kind ('cut'|'boss'), centre (part, mm), normal, d (mm), end, depth (mm), depth2, reverse, both}] for
    every closed single-circle contour of an unsuppressed boss / cut extrude's sketch."""
    sk = {f["name"]: f for f in dump["features"] if f.get("sketch")}
    out = []
    for f in dump["features"]:
        if f["suppressed"] or f["type"] not in ("Extrusion", "ICE") or not f.get("extrude"):
            continue
        s = next((sk[p] for p in f["parents"] if p in sk), None)
        if s is None or "xf" not in s["sketch"]:
            continue
        T = sketch_xf(s["sketch"]["xf"])
        segs = {g["id"]: g for g in s["sketch"]["segs"] if not g.get("constr")}
        ex = f["extrude"]
        for c in s["sketch"]["contours"]:
            if not c["closed"] or len(c["segs"]) != 1 or c["segs"][0] not in segs:
                continue
            g = segs[c["segs"][0]]
            if g.get("type") != 1 or "c" not in g or not np.allclose(g["p0"], g["p1"]):
                continue
            ctr = (T @ np.r_[g["c"], 1.0])[:3] * 1e3
            out.append({"feature": f["name"], "kind": "cut" if f["type"] == "ICE" else "boss", "centre": ctr,
                        "normal": T[:3, 2] / np.linalg.norm(T[:3, 2]), "d": round(2e3 * g["r"], 4),
                        "end": END.get(int(ex.get("end1", 0)), str(ex.get("end1"))), "depth": float(ex.get("d1", 0)) * 1e3,
                        "depth2": float(ex.get("d2", 0)) * 1e3, "both": bool(ex.get("both")), "reverse": bool(ex.get("reverse")),
                        "sketch_origin": T[:3, 3] * 1e3})
    return out


def extrudes(dump):
    """[{feature, id, end, depth (mm), depth2, both, reverse, origin (mm), normal}] of unsuppressed boss / cut extrudes."""
    sk = {f["name"]: f for f in dump["features"] if f.get("sketch")}
    out = []
    for f in dump["features"]:
        if f["suppressed"] or f["type"] not in ("Extrusion", "ICE") or not f.get("extrude"):
            continue
        s = next((sk[p] for p in f["parents"] if p in sk), None)
        if s is None or "xf" not in s["sketch"]:
            continue
        T = sketch_xf(s["sketch"]["xf"])
        ex = f["extrude"]
        out.append({"feature": f["name"], "id": f["id"], "kind": "cut" if f["type"] == "ICE" else "boss",
                    "end": END.get(int(ex.get("end1", 0)), str(ex.get("end1"))), "depth": float(ex.get("d1", 0)) * 1e3,
                    "depth2": float(ex.get("d2", 0)) * 1e3, "both": bool(ex.get("both")), "reverse": bool(ex.get("reverse")),
                    "origin": T[:3, 3] * 1e3, "normal": T[:3, 2] / np.linalg.norm(T[:3, 2])})
    return out


# ------------------------------------------------------------------------------------------------ faces (pure)
def _frame(ax):
    a = np.asarray(ax, float) / np.linalg.norm(ax)
    x = np.cross(a, [1.0, 0, 0]) if abs(a[0]) < 0.9 else np.cross(a, [0, 1.0, 0])
    x /= np.linalg.norm(x)
    return a, x, np.cross(a, x)


def face_samples(f, n=9):
    """Up to n points (mm, part frame) on a v2 dump face, kept inside the face's box: plane -> a grid over the box on
    the plane; cyl -> a ring of angles at three heights; cone -> both senses of the half angle (the box picks one).
    Points that fall in a hole of the face are dropped later (they are not on the reference surface). None if unusable."""
    lo, hi = f["box"][:3] * 1e3, f["box"][3:6] * 1e3
    eps = 1e-3 + 1e-3 * float(np.max(hi - lo))
    t = f["type"]
    if t == "plane":
        g = np.stack(np.meshgrid(*[np.linspace(lo[i], hi[i], 5)[1:-1] if hi[i] - lo[i] > 1e-6 else [lo[i]] for i in range(3)]), -1).reshape(-1, 3)
        nn, o = f["n"] / np.linalg.norm(f["n"]), f["o"] * 1e3
        P = g - np.outer((g - o) @ nn, nn)
    elif t == "cyl" or (t == "cone" and "half" in f):
        a, x, y = _frame(f["ax"])
        o = f["o"] * 1e3
        corners = np.array([[lo[0], lo[1], lo[2]], [hi[0], hi[1], hi[2]]])
        h0, h1 = sorted(((corners - o) @ a).tolist())
        hs = np.linspace(h0, h1, 5)[1:-1] if h1 - h0 > 1e-6 else [h0]
        if t == "cyl":   # the box's extent along the axis, around the box centre
            hc = float(((lo + hi) / 2 - o) @ a)
            hh = float((hi - lo) @ np.abs(a)) / 2
            hs = hc + np.linspace(-hh, hh, 5)[1:-1]
        th = np.linspace(0, 2 * np.pi, 144, endpoint=False)
        ring = np.outer(np.cos(th), x) + np.outer(np.sin(th), y)
        P = []
        for sgn in ((0.0,) if t == "cyl" else (1.0, -1.0)):
            hm = float(np.median(hs))
            r0 = f["r"] * 1e3 + (sgn * hm * np.tan(f["half"]) if t == "cone" else 0.0)
            if r0 <= 0:
                continue
            q = o + hm * a + r0 * ring
            inside = np.all((q >= lo - eps) & (q <= hi + eps), axis=1)
            if not inside.any():
                continue
            if inside.all():
                idx = np.arange(0, 144, 144 // 8)
            else:   # the face's angular run: the longest circular run of in-box angles; sample its inner 20..80 %
                k0 = int(np.argmin(inside))
                rolled = np.roll(inside, -k0)
                runs, cur = [], None
                for i, v in enumerate(rolled):
                    if v and cur is None:
                        cur = i
                    if not v and cur is not None:
                        runs.append((cur, i - 1))
                        cur = None
                if cur is not None:
                    runs.append((cur, len(rolled) - 1))
                i0, i1 = max(runs, key=lambda r: r[1] - r[0])
                idx = (k0 + np.round(np.linspace(i0 + 0.2 * (i1 - i0), i0 + 0.8 * (i1 - i0), 3)).astype(int)) % 144
            for h in hs:
                r = f["r"] * 1e3 + (sgn * h * np.tan(f["half"]) if t == "cone" else 0.0)
                if r > 0:
                    P.append(o + h * a + r * ring[idx])
        P = np.vstack(P) if P else np.zeros((0, 3))
    else:
        return None
    P = P[np.all((P >= lo - eps) & (P <= hi + eps), axis=1)]
    if not len(P):
        return None
    return P[np.linspace(0, len(P) - 1, min(n, len(P))).astype(int)]


# ------------------------------------------------------------------------------------------------ registration (pure)
def _perms():
    import itertools

    for p in itertools.permutations(range(3)):
        for s in itertools.product((1, -1), repeat=3):
            R = np.zeros((3, 3))
            for i in range(3):
                R[i, p[i]] = s[i]
            yield R


def icp(pts, ref, T, iters=15, trim=0.8):
    """Rigid point-to-surface ICP (Kabsch on closest points, worst 20 % trimmed) from 4x4 T; returns (T, 80th-percentile gap mm)."""
    import trimesh

    pq = trimesh.proximity.ProximityQuery(ref)
    T = np.asarray(T, float).copy()
    for it in range(iters + 1):
        q = pts @ T[:3, :3].T + T[:3, 3]
        cp, d, _i = pq.on_surface(q)
        if it == iters:
            break
        k = d <= np.quantile(d, trim) + 1e-9
        A, B = q[k], cp[k]
        ca, cb = A.mean(0), B.mean(0)
        U, _s, Vt = np.linalg.svd((A - ca).T @ (B - cb))
        D = np.diag([1, 1, np.sign(np.linalg.det(Vt.T @ U.T))])
        R = Vt.T @ D @ U.T
        step = np.eye(4)
        step[:3, :3], step[:3, 3] = R, cb - R @ ca
        T = step @ T
    return T, float(np.quantile(d, 0.8))


def _sub(pts, n):
    pts = np.asarray(pts, float)
    return pts[np.linspace(0, len(pts) - 1, min(len(pts), n)).astype(int)]


def register(pts, ref, starts=(), iters=15):
    """4x4 (mm) mapping part-frame points `pts` (exact B-rep vertices) onto mesh `ref`, and the 80th-percentile
    vertex gap (mm): a later revision may move a feature, which then just does not show on the reference.
    Rigid ICP from each decoded assembly placement in `starts`; when none fits, also from the best 6 of the 48 signed
    axis permutations aligned by bbox centre. The best fit is kept."""
    import trimesh

    pts = np.asarray(pts, float)
    if len(pts) < 4:
        return np.eye(4), float("inf")
    P = _sub(pts, 400)
    best = min((icp(P, ref, T, iters) for T in starts), key=lambda x: x[1], default=None)
    if best is not None and best[1] <= REG_RMS_MM:
        return best
    pq = trimesh.proximity.ProximityQuery(ref)
    rc = (ref.bounds[0] + ref.bounds[1]) / 2
    few = _sub(pts, 80)
    scored = []
    for R in _perms():
        q = few @ R.T
        T = np.eye(4)
        T[:3, :3], T[:3, 3] = R, rc - (q.min(0) + q.max(0)) / 2
        d = pq.on_surface(few @ T[:3, :3].T + T[:3, 3])[1]
        scored.append((float(np.median(d)), len(scored), T))
    cands = [x[2] for x in sorted(scored, key=lambda x: x[:2])[:6]]
    return min([best] * (best is not None) + [icp(P, ref, T, iters) for T in cands], key=lambda x: x[1])


def asm_starts(asm_file, name, stl):
    """Placements (4x4, mm) of the assembly components named like dump `name` (from the asmdump XFORMs): the one
    numbered like STL `<stem>_<n>` first (STEP and SolidWorks number copies differently, so all are candidates)."""
    from . import asm_dump

    if not asm_file or not Path(asm_file).is_file():
        return []
    m = re.search(r"_(\d+)$", Path(stl).stem)
    want = f"{name}-{m[1] if m else 1}"
    out = []
    for c, v in asm_dump.load(str(asm_file))["comps"].items():
        if "T" in v and _norm(asm_dump.base(c)) == _norm(name):
            out.insert(0, v["T"]) if _norm(c.split("/")[-1]) == _norm(want) else out.append(v["T"])
    return out


# ------------------------------------------------------------------------------------------------ geometry tests (pure)
def surface_gap(mesh, pts, near=None):
    """Distance (mm) from each point to the mesh surface. With `near` (mm): exact only for points that may be within
    `near` of the surface (a KD-tree of surface samples rules the rest out); those get a lower bound > near."""
    import trimesh
    from scipy.spatial import cKDTree

    pts = np.asarray(pts, float)
    out = np.full(len(pts), np.inf)
    sel = np.ones(len(pts), bool)
    if near is not None and len(pts) > 200:
        n = int(min(400000, max(2000, mesh.area / 0.09)))
        smp = trimesh.sample.sample_surface(mesh, n, seed=1)[0]
        h = 3.0 * float(np.sqrt(mesh.area / len(smp)))   # random samples: a generous gap bound
        ds = cKDTree(smp).query(pts)[0]
        sel = ds - h <= near
        out[~sel] = ds[~sel] - h
    if sel.any():
        out[sel] = trimesh.proximity.ProximityQuery(mesh).on_surface(pts[sel])[1]
    return out


def hole_wall(centre, normal, d, lo, hi, n_ang=8, n_ax=5):
    """Points on a sketch circle's cylindrical wall between axial offsets lo..hi (mm) from the sketch plane."""
    a = np.asarray(normal, float) / np.linalg.norm(normal)
    x = np.cross(a, [1.0, 0, 0]) if abs(a[0]) < 0.9 else np.cross(a, [0, 1.0, 0])
    x /= np.linalg.norm(x)
    y = np.cross(a, x)
    th = np.linspace(0, 2 * np.pi, n_ang, endpoint=False)
    ring = d / 2 * (np.outer(np.cos(th), x) + np.outer(np.sin(th), y))
    return [np.asarray(centre) + h * a + ring for h in np.linspace(lo, hi, n_ax + 2)[1:-1]]


def depth_span(c):
    """(lo, hi) axial offsets (mm) from the sketch plane swept by an extrude: blind / mid-plane from the dumped depth;
    through-all / up-to: None (the reference decides)."""
    s = -1.0 if c["reverse"] else 1.0
    if c["end"] == "blind":
        d1 = c["depth"]
        lo, hi = (0.0, s * d1) if not c["both"] else (-c["depth2"] * s, s * d1)
        return min(lo, hi), max(lo, hi)
    if c["end"] == "mid_plane":
        return -c["depth"] / 2, c["depth"] / 2
    return None


def compare(model, ref, feats, tol=TOL_MM):
    """Run the three parities in one frame (all mm). `feats` = {'fillets': [(feature, r, pts)], 'circles': [...],
    'caps': [(feature, depth, pts)]} with points already in the frame. Returns rows
    {kind, feature, at, ok, msg, ref_ok} - ref_ok False = the reference STL itself does not show it (superseded by a
    later feature / pattern): not compared. Two batched point-to-surface queries (reference, ours)."""
    groups = [("fillet", feat, r, p) for feat, r, p in feats.get("fillets", [])]
    groups += [("hole", c, None, ring) for c in feats.get("circles", []) for ring in c["rings"]]
    groups += [("extrude", feat, d, p) for feat, d, p in feats.get("caps", [])]
    if not groups:
        return []
    allp = np.vstack([g[3] for g in groups])
    idx = np.cumsum([0] + [len(g[3]) for g in groups])
    GR = surface_gap(ref, allp, near=1.0)
    live = GR <= 1.0
    GM = np.full(len(allp), np.inf)
    GM[live] = surface_gap(model, allp[live], near=1.0)
    rows = []
    holes = {}
    for k, (kind, feat, val, pts) in enumerate(groups):
        gr, gm = GR[idx[k]:idx[k + 1]], GM[idx[k]:idx[k + 1]]
        if kind == "hole":
            holes.setdefault(id(feat), (feat, []))[1].append((pts, gr, gm))
            continue
        keep = gr <= (max(tol, 0.25 * val) + 0.02 if kind == "fillet" else tol + 0.02)
        need = max(1, len(pts) // 2) if kind == "fillet" else min(3, len(pts))
        if keep.sum() < need:
            rows.append({"kind": kind, "feature": feat, "at": pts.mean(0), "ok": None, "ref_ok": False})
            continue
        lim = tol + gr[keep]
        bad = gm[keep] > lim
        at = pts[keep][int(np.argmax(gm[keep] - lim))] if bad.any() else pts[keep].mean(0)
        msg = (f"{feat} r{val:g}: our surface {float(gm[keep].max()):.3f} mm off the reference face (tol {tol} + ref tessellation {float(gr[keep].max()):.3f})"
               if kind == "fillet" else f"{feat} depth {val:g} mm: end cap {float(gm[keep].max()):.3f} mm from our surface")
        rows.append({"kind": kind, "feature": feat, "at": at, "ok": not bad.any(), "ref_ok": True, "r": val, "msg": msg})
    for c, levels in holes.values():
        live = [(p, gr, gm) for p, gr, gm in levels if (gr <= tol + 0.03).mean() >= 0.75]
        if not live:
            rows.append({"kind": "hole", "feature": c["feature"], "at": c["centre_w"], "ok": None, "ref_ok": False})
            continue
        worst, bad = 0.0, False
        for p, gr, gm in live:
            lim = tol + gr
            worst = max(worst, float((gm - lim).max()))
            bad |= bool((gm > lim).sum() > 1)
        dep = "" if c.get("span_world") is None else " " + format(c["depth"], "g") + " mm"
        rows.append({"kind": "hole", "feature": c["feature"], "at": c["centre_w"], "ok": not bad, "ref_ok": True,
                     "msg": f"{c['feature']} {c['kind']} circle d{c['d']:g} ({c['end']}{dep}) at {np.round(c['centre_w'], 2).tolist()}: wall "
                            f"{'off by ' + format(worst + tol, '.3f') + ' mm' if bad else 'matches'} on {len(live)}/{len(levels)} depth levels the reference shows"})
    return rows


# ------------------------------------------------------------------------------------------------ files
def _norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def dumps_dir(root):
    """`dumps_v2` (faces per feature) when present, else `dumps`."""
    for d in ("dumps_v2", "dumps"):
        if (Path(root) / d).is_dir():
            return Path(root) / d
    return Path(root) / "dumps"


@lru_cache(maxsize=64)
def _load(root, name):
    """(parsed dump, all faces [(feature, face)])."""
    dump = parse((dumps_dir(root) / f"{name}.dump.txt").read_text(errors="replace"))
    return dump, [(f, fc) for f in dump["features"] for fc in f.get("faces") or []]


def find_dump(root, e):
    """Dump stem for a reference_cad entry (`dump`, else the STL stem without its `_<n>` instance suffix), or None."""
    d = dumps_dir(root)
    if not d.is_dir():
        return None
    if e.get("dump"):
        return e["dump"] if (d / f"{e['dump']}.dump.txt").is_file() else None
    stem = re.sub(r"_\d+$", "", Path(e.get("file") or "").stem)
    hit = [p.name[:-len(".dump.txt")] for p in d.glob("*.dump.txt") if _norm(p.name[:-len(".dump.txt")]) == _norm(stem)]
    return hit[0] if len(hit) == 1 else None


def exact_for(spec, e):
    """{'fillet': [mm], 'chamfer': [mm], 'hole_d': [mm]} for a reference_cad entry from its dump, or None."""
    root = (spec.raw or {}).get("sldprt_dumps") or DEFAULT_ROOT
    name = find_dump(root, e)
    if not name:
        return None
    dump, _ = _load(str(root), name)
    r = radii(dump)
    r["hole_d"] = sorted({c["d"] for c in circles(dump)})
    return r


def snap(v, exact, rel=0.35, absol=0.3):
    """The exact value nearest an estimate `v`, when within max(absol, rel * exact); else v."""
    if not exact:
        return v
    x = min(exact, key=lambda q: abs(q - v))
    return float(x) if abs(x - v) <= max(absol, rel * x) else v


def features_in_frame(dump, faces, T, part_pts=None):
    """Fillet / chamfer face samples, hole rings and extrude cap samples of a dump mapped by 4x4 T (part mm -> frame).
    Fillet faces: the cyl / cone / plane faces listed under the Fillet / Chamfer feature, plus the same-radius cyl faces
    under a pattern / mirror of it (the copies)."""
    def X(p):
        p = np.atleast_2d(p)
        return p @ T[:3, :3].T + T[:3, 3]

    fr = {}
    for f in dump["features"]:
        if f["suppressed"]:
            continue
        if f["type"] == "Fillet" and f.get("fillet") and f["fillet"].get("r"):
            fr[f["name"]] = f["fillet"]["r"] * 1e3
        elif f["type"] == "Chamfer":
            d = [v for k, v in f["dims"].items() if k.startswith("D1@")]
            if d:
                fr[f["name"]] = d[0] * 1e3
    out = {"fillets": [], "circles": [], "caps": []}
    for f, fc in faces:
        if f["suppressed"]:
            continue
        if f["name"] in fr:
            name, r = f["name"], fr[f["name"]]
            if fc["type"] == "cyl" and abs(fc["r"] * 1e3 - r) > 1e-3:
                continue   # a cylinder of the fillet feature with another radius is not its blend face
            if fc["type"] not in ("cyl", "cone", "plane"):
                continue
        elif f["type"] in ("CirPattern", "LPattern", "MirrorPattern") and fc["type"] == "cyl":
            src = [p for p in f["parents"] if p in fr and abs(fc["r"] * 1e3 - fr[p]) <= 1e-3]
            if not src:
                continue
            name, r = src[0], fr[src[0]]
        else:
            continue
        sp = face_samples(fc)
        if sp is not None:
            out["fillets"].append((name, r, X(sp)))
    for c in circles(dump):
        sp = depth_span(c)
        if sp:
            lo, hi, n = sp[0], sp[1], 5
        else:   # through / up-to: every 0.75 mm over the part's extent along the axis (the reference decides where)
            ok_ = part_pts is not None and len(part_pts)
            ext = float(np.ptp(part_pts @ c["normal"])) if ok_ else 80.0
            o = float((part_pts.mean(0) - c["centre"]) @ c["normal"]) if ok_ else 0.0
            lo, hi = o - ext / 2 - 0.5, o + ext / 2 + 0.5
            n = int(min(40, max(5, (hi - lo) / 0.75)))
        rings = hole_wall(c["centre"], c["normal"], c["d"], lo, hi, n_ax=n)
        out["circles"].append(dict(c, rings=[X(r) for r in rings], centre_w=X(c["centre"])[0], span_world=sp))
    for x in extrudes(dump):
        sp = depth_span(x)
        if sp is None or x["end"] != "blind" or x["both"]:
            continue
        cap = x["origin"] + (sp[1] if not x["reverse"] else sp[0]) * x["normal"]
        for f, fc in faces:
            if f["name"] != x["feature"] or fc["type"] != "plane":
                continue
            nrm = fc["n"] / np.linalg.norm(fc["n"])
            if abs(abs(nrm @ x["normal"]) - 1) > 1e-6 or abs((fc["o"] * 1e3 - cap) @ x["normal"]) > 1e-3:
                continue
            smp = face_samples(fc, n=9)
            if smp is not None:
                out["caps"].append((x["feature"], x["depth"], X(smp)))
    return out


def part_vertices(faces):
    """Exact surface points (mm, part frame) of every plane / cyl / cone face: the registration point set."""
    pts = [face_samples(fc, n=8) for _f, fc in faces]
    pts = [p for p in pts if p is not None]
    return np.vstack(pts) if pts else np.zeros((0, 3))


def dump_to_world(spec, e, cfg, name, faces, refm):
    """(4x4 dump part frame (mm) -> our world, 80 % registration gap mm) for a reference_cad entry."""
    from .. import cache
    from .asm_dump import DEFAULT_FILE, world_of

    raw = spec.raw or {}
    if e.get("dump_to_ref") is not None:
        A, rms = np.asarray(e["dump_to_ref"], float), 0.0
    else:
        st = asm_starts(((raw.get("asm_dump") or {}).get("file")) or DEFAULT_FILE, name, e["file"])
        A, rms = cache.memo("dump_register", (cache.source_hash(__file__), name, np.asarray(refm.vertices), len(st), *st),
                            lambda: register(part_vertices(faces), refm, st))
    return world_of(e, cfg) @ A, rms


def fillet_sites(spec, e, cfg, refm):
    """[(lo, hi, r)] world boxes (mm) of the reference's fillet faces (cyl faces of Fillet features and their pattern
    copies) for a reference_cad entry whose dump registers; None when there is no usable dump. visual.fillet_ref uses
    them: a reference arc counts only on a dumped fillet face, never a neighbouring feature's arc."""
    root = (spec.raw or {}).get("sldprt_dumps") or DEFAULT_ROOT
    name = find_dump(root, e)
    if not name:
        return None
    dump, faces = _load(str(root), name)
    M, rms = dump_to_world(spec, e, cfg, name, faces, refm)
    if rms > REG_RMS_MM:
        return None
    fr = {f["name"]: f["fillet"]["r"] * 1e3 for f in dump["features"] if not f["suppressed"] and f["type"] == "Fillet" and (f.get("fillet") or {}).get("r")}
    out = []
    for f, fc in faces:
        if fc["type"] != "cyl" or f["suppressed"]:
            continue
        r = fc["r"] * 1e3
        own = f["name"] in fr and abs(fr[f["name"]] - r) <= 1e-3
        copy = f["type"] in ("CirPattern", "LPattern", "MirrorPattern") and any(abs(fr.get(p, -1) - r) <= 1e-3 for p in f["parents"])
        if not (own or copy):
            continue
        lo, hi = fc["box"][:3] * 1e3, fc["box"][3:6] * 1e3
        c = np.array([[x, y, z, 1.0] for x in (lo[0], hi[0]) for y in (lo[1], hi[1]) for z in (lo[2], hi[2])]) @ M.T
        out.append((c[:, :3].min(0), c[:, :3].max(0), r))
    return out


# ------------------------------------------------------------------------------------------------ group
def run(ctx):
    import trimesh

    from .reference_cad import _cfg, _cfg_has_frame, _covered
    from .ref_diff import clean

    spec = ctx.r.spec
    raw = spec.raw or {}
    cfg = _cfg(spec)
    root = raw.get("sldprt_dumps") or DEFAULT_ROOT
    if not dumps_dir(root).is_dir():
        return []
    base = Path(getattr(spec, "base_dir", ".") or ".")
    rdir = base / (cfg.get("dir") or ".")
    out, skipped = [], []
    for e in cfg.get("parts") or []:
        pid = e.get("part")
        if e.get("mode", "shape") != "shape" or not _cfg_has_frame(e, cfg):
            continue
        name = find_dump(root, e)
        b = ctx.world.body(pid)
        if name is None or b is None or b.mesh is None:
            skipped.append(f"`{pid}` ({'no dump for ' + str(e.get('file')) if name is None else 'no model mesh'})")
            continue
        try:
            dump, faces = _load(str(root), name)
            refm = trimesh.load(rdir / e["file"], force="mesh")
            M, rms = dump_to_world(spec, e, cfg, name, faces, refm)
            if rms > REG_RMS_MM:
                skipped.append(f"`{pid}` (dump `{name}` does not fit `{e['file']}`: 80 % vertex gap {rms:.3f} mm - a different revision)")
                continue
            from .reference_cad import ref_in_world

            ref = clean(ref_in_world(refm, e, cfg))
            rows = compare(b.mesh, ref, features_in_frame(dump, faces, M, part_vertices(faces)))
        except Exception as ex:  # noqa: BLE001 - fail closed
            out.append(fail("dump.unusable", G, WARNING, "SolidWorks dump comparison crashed", f"`{pid}` vs `{name}`: {ex}").on(pid))
            ctx.not_checked.append(f"SolidWorks dump parity of `{pid}`")
            continue
        stats = {}
        for kind, cid, title, fix in (
                ("fillet", "dump.fillet", "Fillet / chamfer differs from the reference (exact radius and place)",
                 "Fillet / chamfer that edge to the dumped radius, or list it in `deviations` with a reason citing the reference."),
                ("hole", "dump.hole", "Sketch circle (hole / bore / boss) differs from the reference",
                 "Cut the hole at the dumped centre, diameter and depth, or list it in `deviations` with a reason citing the reference."),
                ("extrude", "dump.extrude", "Extrude depth differs from the reference",
                 "Extrude to the dumped depth, or list it in `deviations` with a reason citing the reference.")):
            rs = [x for x in rows if x["kind"] == kind]
            live = [x for x in rs if x["ref_ok"]]
            bad, waived = [], []
            for x in live:
                if x["ok"]:
                    continue
                why = _covered(np.asarray(x["at"], float), e)
                (waived if why else bad).append(x)
            stats[kind] = {"ref": len(rs), "compared": len(live), "hit": len(live) - len(bad) - len(waived), "waived": len(waived), "miss": len(bad)}
            msg = (f"`{pid}` vs dump `{name}`: {stats[kind]['hit']}/{len(live)} match"
                   + (f", {len(waived)} reasoned deviations" if waived else "")
                   + (f", {len(rs) - len(live)} not shown by the reference STL (pattern / later feature)" if len(rs) > len(live) else ""))
            if bad:
                worst = {}
                for x in bad:
                    worst.setdefault(x["feature"], []).append(x)
                f = fail(cid, G, BLOCKER, title, msg + ". " + "; ".join(
                    f"{v[0]['msg']}" + (f" (+{len(v) - 1} more samples / faces)" if len(v) > 1 else "") for v in list(worst.values())[:10])).on(pid).here(
                    np.round(bad[0]["at"], 2).tolist()).fix(fix)
            else:
                f = ok(cid, G, title.split(" differs")[0] + " matches the reference", msg + ".").on(pid)
            out.append(f)
        ctx.metrics[f"dump.{pid}"] = {"dump": name, "reg_rms_mm": round(rms, 4), **stats}
    if skipped:
        out.append(note("dump.coverage", G, "Parts not checked against a SolidWorks dump", "; ".join(skipped)))
        ctx.not_checked.extend(f"SolidWorks dump parity of {s}" for s in skipped)
    return out
