"""Visual-review gates (`visual` group): shape checks that a CAD reviewer sees at a glance and the older numeric checks
averaged away. Every check is OPT-OUT: it scans every part mapped in `reference_cad` (and, for leads, every catalog
part), always RELATIVE to the reference mesh at the same place, so the original design is never flagged for being
itself (a corner the reference also has sharp, a sliver the reference also has, a facet the reference also has).

Checks (ids):
  visual.silhouette  five views (front Y, top Z, side X, iso (1,-1,1), iso_back (-1,1,1)) of part vs reference placed
                     in our frame: IoU >= iou_min (0.96) per view, no outline difference blob (XOR after a 0.3 mm
                     opening) >= blob_mm2 (2), and no depth-map difference (the nearest surface along the view, so a
                     slab INSIDE the outline counts) deeper than depth_tol_mm (0.5) over >= depth_mm2 (4). Catches an
                     extra slab, a missing spur, a ledge. Shape parts BLOCKER, envelope (bought-in) parts WARNING.
  visual.holes       every hole the reference has along X, Y or Z (sections at 25 heights per axis, not one mid-plane),
                     and every hole ours has: position (centre within 0.8 mm), kind along its axis (plain / csk /
                     cbore / blind) and minimum diameter. Missing, extra or different-kind holes are BLOCKERs.
  visual.faceting    polygonised curves: edges whose dihedral is between facet_lo_deg (6) and facet_hi_deg (25) are
                     the seams of a faceted arc (a smooth CAD surface tessellates far finer; the RVRN STEP meshes have
                     ~0 mm of such edges). A cluster of >= facet_min_mm (4) mm of them where the reference has less
                     than half as much within 2 mm is a polygon / stair-step standing in for a curved surface.
  visual.fillet_ref  every concave edge of ours: local radius vs the reference's at the same spot (sharp_corner's
                     section method). Flagged where the reference is rounder by > max(0.3 mm, 30 %) over a region of
                     >= 3 samples. BLOCKER on structure / printed load parts when the reference radius >= 1 mm.
  visual.sliver      degenerate B-rep faces (coplanar triangle groups bounded only by real edges > 20 deg): area <
                     sliver_area_mm2 (0.02) or width < sliver_w_mm (0.05). Only where the reference has no sliver
                     within 1 mm (the RVRN STEP has its own).
  visual.lead        every lead / terminal port of a bought-in electrical part (phases, terminals, motor, bat, ...)
                     must be the end of a declared wire, and when routes were computed (wiring group) the route must
                     start within lead_tol_mm (1.5) of the port: a lead stub with no wire is a dangling feature.
Exemptions (each needs a reason that cites the reference: RVnn / RVRN / STEP / the reference file name / FSn):
  region   the entry's `deviations` [{near, r, reason}] (shared with reference_cad.diff) cover findings at that point;
  part     entry `visual_ok: {"<check>": "reason"}` (check = silhouette | holes | faceting | fillet_ref | sliver).
  An uncited reason is a BLOCKER (visual.exempt_reason) and exempts nothing. Thresholds: spec `visual` {..., reason}.
"""

from __future__ import annotations

import math
import re
from pathlib import Path

import numpy as np

from ..finding import BLOCKER, INFO, WARNING, fail, note, ok

G = "visual"
DEFAULTS = {"iou_min": 0.96, "blob_mm2": 2.0, "depth_mm2": 4.0, "depth_tol_mm": 0.5, "res_mm": 0.1, "depth_res_mm": 0.2,
            "facet_lo_deg": 6.0, "facet_hi_deg": 25.0, "facet_min_mm": 4.0, "fillet_tol_mm": 0.3, "fillet_frac": 0.3,
            "fillet_load_r_mm": 1.0, "fillet_grid_mm": 1.5, "sliver_area_mm2": 0.02, "sliver_w_mm": 0.05,
            "hole_tol_mm": 0.8, "lead_tol_mm": 1.5}
BOUNDS = {"iou_min": (0.9, 1.0), "blob_mm2": (0.5, 6.0), "depth_mm2": (1.0, 10.0), "depth_tol_mm": (0.2, 1.0),
          "res_mm": (0.05, 0.2), "depth_res_mm": (0.1, 0.4), "facet_lo_deg": (3.0, 10.0), "facet_hi_deg": (15.0, 40.0),
          "facet_min_mm": (2.0, 10.0), "fillet_tol_mm": (0.1, 0.5), "fillet_frac": (0.1, 0.5),
          "fillet_load_r_mm": (0.5, 2.0), "fillet_grid_mm": (0.5, 3.0), "sliver_area_mm2": (0.005, 0.1),
          "sliver_w_mm": (0.02, 0.2), "hole_tol_mm": (0.3, 1.5), "lead_tol_mm": (0.5, 3.0)}
VIEWS = {"front": (0, 1, 0), "top": (0, 0, 1), "side": (1, 0, 0), "iso": (1, -1, 1), "iso_back": (-1, 1, 1)}
from ._review import BOUNDS as _RB
_RB.setdefault("visual", BOUNDS)
CHECKS = ("silhouette", "holes", "faceting", "fillet_ref", "sliver")
CITE = re.compile(r"(RV\d|RVRN|STEP|\.stl|FS\d|reference)", re.I)
LEAD_PORTS = ("phases", "terminals", "motor", "bat", "m1", "m2", "wpn", "rx", "in", "out", "jst", "xt30", "lead")
LOAD_KINDS = ("structure",)


def cites(reason) -> bool:
    return isinstance(reason, str) and len(reason.strip()) >= 12 and bool(CITE.search(reason))


# ------------------------------------------------------------------------------------------------ silhouettes (pure)
def basis(d):
    d = np.asarray(d, float)
    d = d / np.linalg.norm(d)
    t = np.array([0, 0, 1.0]) if abs(d[2]) < 0.9 else np.array([0, 1.0, 0])
    u = np.cross(t, d)
    u /= np.linalg.norm(u)
    return u, np.cross(d, u), d


def _masks(ms, d, res):
    from PIL import Image, ImageDraw

    u, v, _ = basis(d)
    P = [np.c_[m.vertices @ u, m.vertices @ v] for m in ms]
    lo = np.min([p.min(0) for p in P], 0) - 0.5
    hi = np.max([p.max(0) for p in P], 0) + 0.5
    sh = tuple((np.ceil((hi - lo) / res) + 1).astype(int))
    out = []
    for m, p in zip(ms, P):
        img = Image.new("1", sh, 0)
        dr = ImageDraw.Draw(img)
        for t in ((p - lo) / res)[np.asarray(m.faces)]:
            dr.polygon([tuple(q) for q in t], fill=1, outline=1)
        out.append(np.asarray(img, bool).T)
    return out, lo


def _depth(ms, d, res, dens=40.0):
    """Nearest-surface depth per pixel along -d (the surface a viewer looking down -d sees), by dense surface samples."""
    import trimesh
    from scipy import ndimage

    u, v, w = basis(d)
    P = []
    for m in ms:
        n = int(min(max(m.area * dens, 20000), 600000))
        p, _ = trimesh.sample.sample_surface(m, n, seed=1)
        p = np.vstack([p, m.vertices])
        P.append(np.c_[p @ u, p @ v, p @ w])
    lo = np.min([p[:, :2].min(0) for p in P], 0) - 1
    hi = np.max([p[:, :2].max(0) for p in P], 0) + 1
    sh = tuple((np.ceil((hi - lo) / res) + 1).astype(int))
    out = []
    for p in P:
        D = np.full(sh, -1e9)
        ij = ((p[:, :2] - lo) / res).astype(int)
        np.maximum.at(D, (ij[:, 0], ij[:, 1]), p[:, 2])
        out.append(ndimage.grey_dilation(D, size=3))
    return out, lo, (u, v, w)


def view_diff(model, ref, d, prm=DEFAULTS):
    """(iou, blobs) for one view; blobs: [{kind, area_mm2, at (3D, on the surface that differs), depth_mm}]."""
    from scipy import ndimage

    res, dres = prm["res_mm"], prm["depth_res_mm"]
    (A, B), lo = _masks([model, ref], d, res)
    iou = float((A & B).sum() / max((A | B).sum(), 1))
    u, v, w = basis(d)
    cm = (np.vstack([model.vertices, ref.vertices]) @ w).mean()
    blobs = []
    k = max(int(round(0.3 / res)), 1)
    for kind, X in (("extra outline", A & ~B), ("missing outline", B & ~A)):
        lab, n = ndimage.label(ndimage.binary_opening(X, iterations=k))
        for i in range(1, n + 1):
            xs, ys = np.nonzero(lab == i)
            a = len(xs) * res * res
            if a >= prm["blob_mm2"]:
                uv = lo + np.array([xs.mean(), ys.mean()]) * res
                blobs.append({"kind": kind, "area_mm2": round(a, 2), "at": (uv[0] * u + uv[1] * v + cm * w).round(2).tolist(),
                              "uv": uv.tolist(), "depth_mm": None})
    (DA, DB), lo2, _ = _depth([model, ref], d, dres)
    both = (DA > -1e8) & (DB > -1e8)
    # only where both surfaces are near-continuous (skip the rim of a through-opening seen from the side)
    for kind, X in (("proud", both & (DA - DB > prm["depth_tol_mm"])), ("sunk", both & (DB - DA > prm["depth_tol_mm"]))):
        lab, n = ndimage.label(ndimage.binary_opening(X, iterations=2))
        for i in range(1, n + 1):
            xs, ys = np.nonzero(lab == i)
            a = len(xs) * dres * dres
            if a < prm["depth_mm2"]:
                continue
            dd = np.abs(DA - DB)[xs, ys]
            uv = lo2 + np.array([xs.mean(), ys.mean()]) * dres
            z = float(np.median((DA if kind == "proud" else DB)[xs, ys]))
            blobs.append({"kind": kind + " surface", "area_mm2": round(a, 1), "at": (uv[0] * u + uv[1] * v + z * w).round(2).tolist(),
                          "uv": uv.tolist(), "depth_mm": round(float(np.median(dd)), 2)})
    return iou, blobs


# ------------------------------------------------------------------------------------------------ holes (pure)
def hole_list(m, ref_bounds, n=25):
    """[(axis, centre (u, v), d)] of every hole cut by sections at n heights along each axis (deduplicated)."""
    from .ref_features import holes, section

    out = []
    lo, hi = ref_bounds
    for ax in range(3):
        for f in np.linspace(0.02, 0.98, n):
            h = float(lo[ax] + (hi[ax] - lo[ax]) * f)
            for c, d, _ in holes(section(m, ax, h)):
                if any(a == ax and math.dist(c, cc) < 0.8 for a, cc, _ in out):
                    continue
                out.append((ax, tuple(float(x) for x in c), float(d)))
    return out


def hole_diffs(model, ref, tol=0.8):
    """Feature differences per hole: [{kind, axis, at (3D), msg}] with kind missing / extra / kind / size."""
    from .ref_features import hole_kind, hole_profile

    lo = np.minimum(model.bounds[0], ref.bounds[0])
    hi = np.maximum(model.bounds[1], ref.bounds[1])
    hr, hm = hole_list(ref, (lo, hi)), hole_list(model, (lo, hi))
    out = []

    def p3(ax, c, prof):
        a, b = [i for i in range(3) if i != ax]
        ts = np.linspace(0.04, 0.96, len(prof))
        hs = [lo[ax] + (hi[ax] - lo[ax]) * t for t, d in zip(ts, prof) if d]
        p = [0.0] * 3
        p[a], p[b], p[ax] = c[0], c[1], float(np.mean(hs)) if hs else float((lo[ax] + hi[ax]) / 2)
        return [round(x, 2) for x in p]

    used = set()
    for ax, c, d in hr:
        j = next((k for k, (a2, c2, _) in enumerate(hm) if a2 == ax and k not in used and math.dist(c, c2) <= tol), None)
        pr = hole_profile(ref, ax, c, lo[ax], hi[ax], n=15)
        at = p3(ax, c, pr)
        if j is None:
            out.append({"kind": "missing", "axis": "XYZ"[ax], "at": at, "msg": f"reference hole d{d:.2f} along {'XYZ'[ax]} at {at} has no counterpart"})
            continue
        used.add(j)
        pm = hole_profile(model, ax, hm[j][1], lo[ax], hi[ax], n=15)
        kr, km = hole_kind(pr), hole_kind(pm)
        if kr != km:
            out.append({"kind": "kind", "axis": "XYZ"[ax], "at": at, "msg": f"hole along {'XYZ'[ax]} at {at}: reference {kr}, ours {km}"})
        vr, vm = [x for x in pr if x], [x for x in pm if x]
        if vr and vm and abs(min(vr) - min(vm)) > max(0.4, 0.12 * min(vr)):
            out.append({"kind": "size", "axis": "XYZ"[ax], "at": at, "msg": f"hole along {'XYZ'[ax]} at {at}: min d {min(vm):.2f} vs reference {min(vr):.2f}"})
    for k, (ax, c, d) in enumerate(hm):
        if k in used:
            continue
        at = p3(ax, c, hole_profile(model, ax, c, lo[ax], hi[ax], n=15))
        out.append({"kind": "extra", "axis": "XYZ"[ax], "at": at, "msg": f"hole d{d:.2f} along {'XYZ'[ax]} at {at} is not in the reference"})
    return out


# ------------------------------------------------------------------------------------------------ faceting (pure)
def facet_edge_samples(m, lo_deg, hi_deg, step=0.5):
    """Points every `step` mm along edges whose dihedral is in [lo_deg, hi_deg) and the length each stands for."""
    ang = np.degrees(m.face_adjacency_angles)
    k = (ang >= lo_deg) & (ang < hi_deg)
    E = m.face_adjacency_edges[k]
    a, b = m.vertices[E[:, 0]], m.vertices[E[:, 1]]
    L = np.linalg.norm(b - a, axis=1)
    pts, w = [], []
    for p, q, l in zip(a, b, L):
        n = max(int(l / step), 1)
        for s in (np.arange(n) + 0.5) / n:
            pts.append(p + s * (q - p))
            w.append(l / n)
    return np.asarray(pts, float).reshape(-1, 3), np.asarray(w, float)


def faceted_regions(model, ref, lo_deg=6.0, hi_deg=25.0, min_mm=4.0, link=3.5, ratio=0.5):
    """[{at, len_mm, ref_len_mm, lo, hi}] clusters of faceting seams on `model` that the reference does not have."""
    from scipy.spatial import cKDTree

    from .sharp_corner import regions

    pm, wm = facet_edge_samples(model, lo_deg, hi_deg)
    if not len(pm):
        return []
    pr, wr = facet_edge_samples(ref, lo_deg, hi_deg)
    tr = cKDTree(pr) if len(pr) else None
    out = []
    for g in regions([(p, None, w, 0.0) for p, w in zip(pm, wm)], link):
        P = np.array([h[0] for h in g])
        L = float(sum(h[2] for h in g))
        if L < min_mm:
            continue
        Lr = 0.0
        if tr is not None:
            idx = sorted({j for lst in tr.query_ball_point(P, link) for j in lst})
            Lr = float(wr[idx].sum()) if idx else 0.0
        if Lr < ratio * L:
            out.append({"at": P.mean(0).round(2).tolist(), "len_mm": round(L, 1), "ref_len_mm": round(Lr, 1),
                        "lo": P.min(0).round(1).tolist(), "hi": P.max(0).round(1).tolist()})
    return sorted(out, key=lambda x: -x["len_mm"])


def face_mix(m, lo_deg=6.0):
    """(planar share of area, faceting seam length mm): planar = triangles in coplanar groups over 1 mm2."""
    import networkx as nx

    ang = np.degrees(m.face_adjacency_angles)
    g = nx.Graph()
    g.add_nodes_from(range(len(m.faces)))
    g.add_edges_from(m.face_adjacency[ang < 0.5])
    A = m.area_faces
    planar = sum(A[list(c)].sum() for c in nx.connected_components(g) if A[list(c)].sum() >= 1.0)
    _, w = facet_edge_samples(m, lo_deg, 25.0)
    return float(planar / max(A.sum(), 1e-9)), float(w.sum())


# ------------------------------------------------------------------------------------------------ fillets (pure)
def fillet_diffs(model, ref, grid=1.5, min_turn=30.0, tol=0.3, frac=0.3, snap=1.2):
    """[(point, r_ours, r_ref)] on model concave edges where the reference at the same spot is rounder."""
    import trimesh

    from . import sharp_corner as sc

    bm, br = sc.tri_boxes(model), sc.tri_boxes(ref)
    out = []
    for p, t in sc.concave_samples(model, grid):
        a = sc.local_radius(model, p, t, 4.0, bm)
        if a is None or a[1] < min_turn:
            continue
        q, d, _ = trimesh.proximity.closest_point(ref, [p])
        if d[0] > snap:
            continue
        b = sc.local_radius(ref, q[0], t, 4.0, br)
        if b is None or b[1] < 0.5 * min_turn:
            continue
        if b[0] - a[0] > max(tol, frac * b[0]):
            out.append((np.asarray(p, float), float(a[0]), float(b[0])))
    return out


# ------------------------------------------------------------------------------------------------ slivers (pure)
def slivers(m, area=0.02, width=0.05, sharp=20.0):
    """[(centre, area mm2, width mm)] of B-rep-like faces (coplanar triangle groups whose every boundary edge is a real
    edge > `sharp` deg, so not a tessellation strip of a curved face) that are tiny or needle-thin."""
    import networkx as nx

    ang = np.degrees(m.face_adjacency_angles)
    adj = m.face_adjacency
    g = nx.Graph()
    g.add_nodes_from(range(len(m.faces)))
    g.add_edges_from(adj[ang < 0.5])
    comp = np.empty(len(m.faces), int)
    for i, c in enumerate(nx.connected_components(g)):
        comp[list(c)] = i
    n = int(comp.max()) + 1 if len(comp) else 0
    A = np.bincount(comp, m.area_faces, n)
    ca, cb = comp[adj[:, 0]], comp[adj[:, 1]]
    cross = ca != cb
    soft = np.zeros(n, bool)
    soft[ca[cross & (ang < sharp)]] = True
    soft[cb[cross & (ang < sharp)]] = True
    out = []
    for c in np.nonzero(~soft & (A < 1.0))[0]:
        f = np.nonzero(comp == c)[0]
        pts = m.triangles[f].reshape(-1, 3)
        L = float(np.ptp(pts, axis=0).max())
        w = float(A[c] / max(L, 1e-9))
        if A[c] < area or w < width:
            out.append((pts.mean(0), float(A[c]), w))
    return out


# ------------------------------------------------------------------------------------------------ spec helpers
def params(raw):
    from ._review import resolve

    return {k: float(v) for k, v in resolve((raw or {}).get("visual"), DEFAULTS, BOUNDS)[0].items()}


def _entries(ctx):
    from .reference_cad import _cfg, _cfg_has_frame

    cfg = _cfg(ctx.r.spec)
    base = Path(getattr(ctx.r.spec, "base_dir", ".") or ".")
    rdir = base / (cfg.get("dir") or ".")
    return [(e, cfg, rdir / (e.get("file") or "")) for e in cfg.get("parts") or [] if _cfg_has_frame(e, cfg)]


def _model_mesh(ctx, e):
    import trimesh

    b = ctx.world.body(e.get("part"))
    if b is None or b.mesh is None:
        return None
    ms = [b.mesh] + [ctx.world.body(x).mesh for x in e.get("with_parts") or [] if ctx.world.body(x) is not None]
    return ms[0] if len(ms) == 1 else trimesh.util.concatenate(ms)


def covered(e, at):
    """Reason of a valid entry `deviation` covering 3D point `at` (citing the reference), else None."""
    for d in e.get("deviations") or []:
        if not cites(d.get("reason")) or d.get("near") is None or float(d.get("r", 3.0)) > 5.0:
            continue
        if np.linalg.norm(np.asarray(at, float) - np.asarray(d["near"], float)) <= float(d.get("r", 3.0)):
            return d["reason"]
    return None


def _part_ok(e, check, out, pid):
    """Reason when the entry exempts `check` with a cited reason; an uncited one is a BLOCKER and exempts nothing."""
    v = (e.get("visual_ok") or {}).get(check)
    if v is None:
        return None
    if cites(v):
        return v
    out.append(fail("visual.exempt_reason", G, BLOCKER, "Visual-check exemption does not cite the reference",
                    f"`{pid}` visual_ok.{check} = {v!r}: an exemption must say why, citing the reference (RVnn / RVRN / "
                    f"STEP / file name); it exempts nothing.").on(pid))
    return None


def _split(e, items):
    """(open, waived[(item, reason)]) by the entry's deviations at each item's `at`."""
    op, wv = [], []
    for it in items:
        why = covered(e, it["at"])
        (wv if why else op).append((it, why) if why else it)
    return op, wv


def _report(out, cid, pid, sev, title, items, waived, fmt, fix, ok_msg):
    if items:
        txt = "; ".join(fmt(x) for x in items[:8]) + (f" (+{len(items) - 8} more)" if len(items) > 8 else "")
        out.append(fail(cid, G, sev, title, f"`{pid}`: {len(items)} difference(s) from the reference: {txt}.")
                   .on(pid).here(items[0]["at"]).fix(fix))
    if waived:
        txt = "; ".join(f"{fmt(x)} [{why[:90]}]" for x, why in waived[:6])
        out.append(note(cid, G, title + " (reasoned deviations)", f"`{pid}`: {len(waived)} covered by `deviations`: {txt}.").on(pid))
    if not items:
        out.append(ok(cid, G, ok_msg, f"`{pid}` matches the reference" + (f" ({len(waived)} reasoned deviations)" if waived else "") + ".").on(pid))


# ------------------------------------------------------------------------------------------------ group
def run(ctx):
    import trimesh

    from ._review import override_findings
    from .reference_cad import ref_in_world
    from .ref_diff import clean

    raw = ctx.r.spec.raw or {}
    prm = params(raw)
    out = override_findings(raw.get("visual"), DEFAULTS, "visual", "visual.params", G) if "visual" in raw else []
    rows = {}
    parts = {rp.part.id: rp for rp in ctx.r.parts}
    for e, cfg, path in _entries(ctx):
        pid = e.get("part")
        shape = e.get("mode", "shape") == "shape"
        mod = _model_mesh(ctx, e)
        if mod is None or not path.is_file():
            out.append(fail("visual.unusable", G, BLOCKER if mod is None else WARNING, "Visual comparison not possible",
                            f"`{pid}`: {'no model mesh' if mod is None else f'reference {path} not found'}").on(pid))
            ctx.not_checked.append(f"visual checks of `{pid}`")
            continue
        try:
            ref = clean(ref_in_world(trimesh.load(path, force="mesh"), e, cfg))
        except Exception as ex:  # noqa: BLE001 - fail closed
            out.append(fail("visual.unusable", G, WARNING, "Reference could not be loaded", f"`{pid}`: {ex}").on(pid))
            ctx.not_checked.append(f"visual checks of `{pid}`")
            continue
        rp = parts.get(pid)
        kind = getattr(rp.part, "kind", None) if rp else None
        printed = rp is not None and rp.part.catalog is None
        row = rows.setdefault(pid, {})
        sev_shape = BLOCKER if shape else WARNING
        for check in CHECKS:
            if check in ("holes", "fillet_ref", "sliver") and not shape:
                continue
            why = _part_ok(e, check, out, pid)
            if why:
                out.append(note(f"visual.{check}", G, "Exempt", f"`{pid}` visual_ok.{check}: {why}").on(pid))
                continue
            try:
                if check == "silhouette":
                    items, ious = [], {}
                    for name, d in VIEWS.items():
                        iou, blobs = view_diff(mod, ref, d, prm)
                        ious[name] = round(iou, 3)
                        if iou < prm["iou_min"]:
                            items.append({"at": [round(x, 2) for x in (mod.bounds[0] + mod.bounds[1]) / 2], "msg": f"{name} IoU {iou:.3f} < {prm['iou_min']}"})
                        items += [{"at": b["at"], "msg": f"{name}: {b['kind']} {b['area_mm2']} mm2" + (f" x {b['depth_mm']} mm" if b["depth_mm"] else "") + f" at {b['at']}"} for b in blobs]
                    row["iou"] = ious
                    op, wv = _split(e, items)
                    _report(out, "visual.silhouette", pid, sev_shape, "Part looks different from the reference in a view", op, wv,
                            lambda x: x["msg"], "Remove the extra slab / ledge or add the missing feature seen in that view, or list it "
                            "in the entry's `deviations` with a reason citing the reference.", f"All five views match (IoU {min(ious.values()):.3f}+)")
                elif check == "holes":
                    items = hole_diffs(mod, ref, prm["hole_tol_mm"])
                    row["holes"] = len(items)
                    op, wv = _split(e, items)
                    _report(out, "visual.holes", pid, BLOCKER, "Hole features differ from the reference", op, wv, lambda x: x["msg"],
                            "Match every hole's position and kind (countersink / counterbore / plain) to the reference.",
                            "Every hole matches the reference (position, kind, size) on all three axes")
                elif check == "faceting":
                    regs = faceted_regions(mod, ref, prm["facet_lo_deg"], prm["facet_hi_deg"], prm["facet_min_mm"])
                    pm_, lm = face_mix(mod, prm["facet_lo_deg"])
                    pr_, lr = face_mix(ref, prm["facet_lo_deg"])
                    row["face_mix"] = {"planar_share": round(pm_, 3), "ref_planar_share": round(pr_, 3), "facet_mm": round(lm, 1), "ref_facet_mm": round(lr, 1)}
                    items = [dict(x, msg=f"{x['len_mm']} mm of {prm['facet_lo_deg']:g}-{prm['facet_hi_deg']:g} deg seams (reference {x['ref_len_mm']} mm) round {x['at']}") for x in regs]
                    op, wv = _split(e, items)
                    _report(out, "visual.faceting", pid, sev_shape, "Curved surface modelled as polygon / blocks", op, wv, lambda x: x["msg"],
                            f"Model the arc as a true arc (more segments or a revolve); planar share {pm_:.0%} vs reference {pr_:.0%}.",
                            "No polygonised curves")
                elif check == "fillet_ref":
                    from .sharp_corner import regions

                    hits = fillet_diffs(mod, ref, prm["fillet_grid_mm"], tol=prm["fillet_tol_mm"], frac=prm["fillet_frac"])
                    items = []
                    for g in regions([(p, None, a, b) for p, a, b in hits], 2.5):
                        if len(g) < 3:
                            continue
                        w = max(g, key=lambda h: h[3] - h[2])
                        items.append({"at": np.round(w[0], 2).tolist(), "r": round(w[2], 2), "r_ref": round(w[3], 2), "n": len(g),
                                      "msg": f"{np.round(w[0], 1).tolist()} r {w[2]:.2f} vs reference r {w[3]:.2f} ({len(g)} samples)"})
                    row["fillet_ref"] = len(items)
                    op, wv = _split(e, items)
                    load = (kind in LOAD_KINDS or printed)
                    hard = [x for x in op if load and x["r_ref"] >= prm["fillet_load_r_mm"]]
                    soft = [x for x in op if x not in hard]
                    _report(out, "visual.fillet_ref", pid, BLOCKER, "Inside corner sharper than the reference", hard, wv, lambda x: x["msg"],
                            "Fillet the concave root to the reference radius (a sharp root is a crack start under a hit).",
                            "Every concave corner is at least as round as the reference")
                    if soft:
                        out.append(fail("visual.fillet_ref", G, WARNING, "Inside corner sharper than the reference (small radius)",
                                        f"`{pid}`: " + "; ".join(x["msg"] for x in soft[:8])).on(pid).here(soft[0]["at"]))
                elif check == "sliver":
                    from scipy.spatial import cKDTree

                    sm = slivers(mod, prm["sliver_area_mm2"], prm["sliver_w_mm"])
                    sr = slivers(ref, prm["sliver_area_mm2"], prm["sliver_w_mm"])
                    tr = cKDTree(np.array([s[0] for s in sr])) if sr else None
                    new = [s for s in sm if tr is None or tr.query(s[0])[0] > 1.0]
                    row["sliver"] = {"ours": len(sm), "ref": len(sr), "new": len(new)}
                    items = [{"at": np.round(c, 2).tolist(), "msg": f"{np.round(c, 2).tolist()} area {a:.4f} mm2 width {w:.3f} mm"} for c, a, w in new]
                    op, wv = _split(e, items)
                    _report(out, "visual.sliver", pid, sev_shape, "Sliver / degenerate faces the reference does not have", op, wv,
                            lambda x: x["msg"], "Snap the near-coincident edges (a boolean left a hair-thin face); they print as specks "
                            "and break offsets.", f"No sliver faces beyond the reference's own ({len(sr)})")
            except Exception as ex:  # noqa: BLE001 - fail closed
                out.append(fail(f"visual.{check}", G, BLOCKER, "Visual check crashed", f"`{pid}`: {type(ex).__name__}: {ex}").on(pid))
                ctx.not_checked.append(f"visual.{check} of `{pid}`")
    ctx.metrics["visual"] = rows
    out += leads(ctx, prm)
    return out


def leads(ctx, prm):
    """visual.lead: every lead port of a bought-in electrical part ends a wire, and the wire's route starts at it."""
    from .wiring import _from

    r, w = ctx.r, ctx.world
    spec = r.spec
    ends = {}
    for wr in spec.wires or []:
        ends.setdefault(_from(wr), []).append(wr.id)
        ends.setdefault(wr.to, []).append(wr.id)
    routes = {rt.id: rt for rt in (getattr(ctx, "routes", None) or [])}
    out, bad, n = [], [], 0
    for rp in r.parts:
        cat = getattr(rp, "cat", None)
        if cat is None or not getattr(cat, "ports", None):
            continue
        for pname in cat.ports:
            if not any(pname.startswith(k) for k in LEAD_PORTS):
                continue
            full = f"{rp.part.id}.{pname}"
            p = w.port(r, full)
            n += 1
            ws = ends.get(full)
            if not ws:
                ok_reason = ((getattr(rp.part, "_extra", None) or {}).get("unused_ports") or {}).get(pname)
                if cites(ok_reason) or (isinstance(ok_reason, str) and len(ok_reason.strip()) >= 12):
                    continue
                bad.append((full, p, "no wire ends at it (a lead stub with no route)"))
                continue
            for wid in ws:
                rt = routes.get(wid)
                if rt is None or p is None or len(rt.points) < 2:
                    continue
                dmin = min(np.linalg.norm(np.asarray(rt.points[0], float) - p), np.linalg.norm(np.asarray(rt.points[-1], float) - p))
                if dmin > prm["lead_tol_mm"]:
                    bad.append((full, p, f"route `{wid}` ends {dmin:.1f} mm from the lead"))
    if bad:
        out.append(fail("visual.lead", G, BLOCKER, "Dangling lead: a bought-in part's lead has no wire route",
                        "; ".join(f"`{f}` at {None if p is None else np.round(p, 1).tolist()}: {why}" for f, p, why in bad[:8]))
                   .on(*sorted({f.split('.')[0] for f, _, _ in bad})).here(bad[0][1])
                   .fix("Declare the wire from the lead to its ESC / switch port, or list the port in the part's "
                        "`unused_ports: {port: reason}`."))
    elif n:
        out.append(ok("visual.lead", G, "Every lead ends a wire", f"{n} lead / terminal port(s) all end a declared wire"
                      + (" whose route starts at the lead" if routes else " (routes not computed in this run)") + "."))
    if not routes and spec.wires:
        ctx.not_checked.append("visual.lead: wire routes not computed (run the wiring group) - only declared ends checked")
    return out
