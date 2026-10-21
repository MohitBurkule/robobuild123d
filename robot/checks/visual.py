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
                     >= 2 samples (1.5 mm grid). BLOCKER on structure / printed load parts when the reference radius >= 1 mm.
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
    import trimesh

    for kind, X, src in (("extra outline", A & ~B, model), ("missing outline", B & ~A, ref)):
        lab, n = ndimage.label(ndimage.binary_opening(X, iterations=k))
        if not n:
            continue
        # where the differing outline IS in 3D: surface samples of the mesh that has it, projecting into the blob
        P, _ = trimesh.sample.sample_surface(src, int(min(max(src.area * 20, 20000), 300000)), seed=2)
        ij = np.floor((np.c_[P @ u, P @ v] - lo) / res).astype(int)
        okp = (ij[:, 0] >= 0) & (ij[:, 1] >= 0) & (ij[:, 0] < lab.shape[0]) & (ij[:, 1] < lab.shape[1])
        lp = np.zeros(len(P), int)
        lp[okp] = lab[ij[okp, 0], ij[okp, 1]]
        for i in range(1, n + 1):
            xs, ys = np.nonzero(lab == i)
            a = len(xs) * res * res
            if a >= prm["blob_mm2"]:
                uv = lo + np.array([xs.mean(), ys.mean()]) * res
                hit = P[lp == i]
                at = hit.mean(0) if len(hit) else uv[0] * u + uv[1] * v + cm * w
                blobs.append({"kind": kind, "area_mm2": round(a, 2), "at": np.round(at, 2).tolist(),
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
def hole_list(m, ref_bounds, n=25, with_h=False):
    """[(axis, centre (u, v), d)] of every hole cut by sections at n heights along each axis (deduplicated);
    with_h: (axis, centre, d, h) with the section height the centre was measured at (a slanted hole or groove moves
    across sections, so its centre is only true at that height)."""
    from .ref_features import holes, section

    out = []
    lo, hi = ref_bounds
    for ax in range(3):
        for f in np.linspace(0.02, 0.98, n):
            h = float(lo[ax] + (hi[ax] - lo[ax]) * f)
            for c, d, _ in holes(section(m, ax, h)):
                if any(a == ax and math.dist(c, cc) < 0.8 for a, cc, *_r in out):
                    continue
                out.append((ax, tuple(float(x) for x in c), float(d), h))
    return out if with_h else [x[:3] for x in out]


def hole_diffs(model, ref, tol=0.8):
    """Feature differences per hole: [{kind, axis, at (3D), msg}] with kind missing / extra / kind / size."""
    from .ref_features import hole_kind, hole_profile

    lo = np.minimum(model.bounds[0], ref.bounds[0])
    hi = np.maximum(model.bounds[1], ref.bounds[1])
    hr, hm = hole_list(ref, (lo, hi), with_h=True), hole_list(model, (lo, hi), with_h=True)
    out = []

    def at_h(ax, c, h):
        p = [0.0] * 3
        a, b = [i for i in range(3) if i != ax]
        p[a], p[b], p[ax] = c[0], c[1], float(h)
        return [round(x, 2) for x in p]

    def runs(ax, c, prof):
        """[(3D centre, (h_lo, h_hi))] of every contiguous run of heights where the hole exists at c (two coaxial holes
        at the two ends of a part are two features, not one at their average height)."""
        a, b = [i for i in range(3) if i != ax]
        hs = [lo[ax] + (hi[ax] - lo[ax]) * t for t in np.linspace(0.04, 0.96, len(prof))]
        out_, cur = [], []
        for h, d in zip(hs, prof):
            if d:
                cur.append(h)
            elif cur:
                out_.append(cur)
                cur = []
        if cur:
            out_.append(cur)
        res = []
        for run in out_:
            p = [0.0] * 3
            p[a], p[b], p[ax] = c[0], c[1], float(np.mean(run))
            res.append(([round(x, 2) for x in p], (min(run), max(run))))
        return res, (hs[1] - hs[0] if len(hs) > 1 else 1.0)

    def places(ax, c, h, prof):
        """Where the hole is: its measured spot (c at the section height h) first - a run's mid-height would put a
        slanted hole or groove off its own centreline - then every other coaxial run of the profile at c."""
        rs, step = runs(ax, c, prof)
        return [at_h(ax, c, h)] + [q for q, (r0, r1) in rs if not (r0 - step <= h <= r1 + step)]

    used = set()
    for ax, c, d, h0 in hr:
        j = next((k for k, (a2, c2, _, _h) in enumerate(hm) if a2 == ax and k not in used and math.dist(c, c2) <= tol), None)
        pr = hole_profile(ref, ax, c, lo[ax], hi[ax], n=15)
        at = at_h(ax, c, h0)
        if j is None:
            for at_ in places(ax, c, h0, pr):
                out.append({"kind": "missing", "axis": "XYZ"[ax], "at": at_, "msg": f"reference hole d{d:.2f} along {'XYZ'[ax]} at {at_} has no counterpart"})
            continue
        used.add(j)
        pm = hole_profile(model, ax, hm[j][1], lo[ax], hi[ax], n=15)
        kr, km = hole_kind(pr), hole_kind(pm)
        if kr != km:
            out.append({"kind": "kind", "axis": "XYZ"[ax], "at": at, "msg": f"hole along {'XYZ'[ax]} at {at}: reference {kr}, ours {km}"})
        vr, vm = [x for x in pr if x], [x for x in pm if x]
        if vr and vm and abs(min(vr) - min(vm)) > max(0.4, 0.12 * min(vr)):
            out.append({"kind": "size", "axis": "XYZ"[ax], "at": at, "msg": f"hole along {'XYZ'[ax]} at {at}: min d {min(vm):.2f} vs reference {min(vr):.2f}"})
    for k, (ax, c, d, h0) in enumerate(hm):
        if k in used:
            continue
        at = at_h(ax, c, h0)
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
SITE_MM = 0.3           # a reference spot is on a dumped fillet face when within this of its box
TURN_MATCH_DEG = 15.0   # the reference corner compared must turn as much as ours (else it is a different corner)


def fillet_diffs(model, ref, grid=1.5, min_turn=30.0, tol=0.3, frac=0.3, snap=1.2, exact=None, sites=None):
    """[(point, r_ours, r_ref)] on model concave edges where the reference at the same spot is rounder.
    The reference is measured with section windows of 2, 4 and 6 mm and only a measurement whose turn matches ours
    within TURN_MATCH_DEG counts (the closest match): a 4 mm window that reaches the next corner, a slot (turn ~180) or a
    shallow 20 deg bend is a different feature, not a rounder version of ours. No matching corner -> not compared.
    `exact`: the reference's exact fillet radii (SolidWorks dump, sldprt_dump.exact_for): the estimate is snapped to the
    nearest one when within 35 % / 0.3 mm (the place comes from the estimate, the radius from the dump).
    `sites`: world boxes (lo, hi, r) of the reference's dumped fillet faces (sldprt_dump.fillet_sites). With them the
    reference is rounder only where the measured spot lies on one (within SITE_MM), and its radius is that face's:
    an estimate picking up a neighbouring feature's arc on a sharp reference edge is not a fillet."""
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
        cands = [x for x in (sc.local_radius(ref, q[0], t, wdw, br) for wdw in (2.0, 4.0, 6.0)) if x is not None]
        cands = [x for x in cands if abs(x[1] - a[1]) <= TURN_MATCH_DEG]
        if not cands:
            continue
        b = min(cands, key=lambda x: abs(x[1] - a[1]))
        if sites is not None:
            on = [r for lo, hi, r in sites if float(np.linalg.norm(np.clip(q[0], lo, hi) - q[0])) <= SITE_MM]
            if not on:
                continue   # the reference is sharp here (no fillet face of its own)
            b = (min(on, key=lambda r: abs(r - b[0])),) + tuple(b[1:])
        elif exact:
            from .sldprt_dump import snap as _snap

            b = (_snap(b[0], exact),) + tuple(b[1:])
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
    from .reference_cad import _dev_valid, path_dist

    for d in e.get("deviations") or []:
        if d.get("path") is not None:   # capsule waiver (validated by reference_cad._dev_valid)
            if _dev_valid(d) is None and float(path_dist(np.atleast_2d(np.asarray(at, float)), np.asarray(d["path"], float))[0]) <= float(d["r"]):
                return d["reason"]
            continue
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

                    from .sldprt_dump import exact_for, fillet_sites

                    try:
                        ex = exact_for(ctx.r.spec, e)
                        sites = fillet_sites(ctx.r.spec, e, cfg, trimesh.load(path, force="mesh"))
                    except Exception:  # noqa: BLE001 - estimates only
                        ex, sites = None, None
                    hits = fillet_diffs(mod, ref, prm["fillet_grid_mm"], tol=prm["fillet_tol_mm"], frac=prm["fillet_frac"],
                                        exact=(ex or {}).get("fillet"), sites=sites)
                    items = []
                    for g in regions([(p, None, a, b) for p, a, b in hits], 2.5):
                        if len(g) < 2:   # 2 samples on the 1.5 mm grid = a >= 1.5 mm run of edge
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
    out += rev2_findings(ctx, prm)
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


# ================================================================================================ review rev2 gates
# visual.shaft_mate   every catalog shaft (cat.shaft at/dir/len): at sections along its span inside another body's bore,
#                     the shaft's profile (round / D / hex) must equal the bore's. A round shaft in a D-bore (or the
#                     reverse) is a BLOCKER: the parts cannot both be right.
# visual.ligament     every printed part, sections at 30 heights on X, Y and Z: the wall round every closed bore (ring
#                     to the outline or the next ring) >= ligament_mm (0.8). Where the reference ring is just as thin at
#                     the same place it is INFO; where the reference has a closed ring and ours is open (a bore broken
#                     through the wall: an open C) it is a BLOCKER.
# visual.deviation_claim  a deviation note that states an extent ("x -26.5..-25, y 43-50") is held to it: the material
#                     the reference has and we removed inside that box must be filled by the part it seats (another
#                     body) for >= claim_fill (0.8, i.e. cut volume <= seated volume x 1.25); the rest of the box is
#                     over-cut (a "1.5 mm seat" cut through the full cheek height).
# visual.terminal     every lead / terminal port of a catalog motor or ESC lies on the part's own solid (within
#                     terminal_tol_mm 0.2): the tab or lead the wire solders to exists in the model.
DEFAULTS.update({"ligament_mm": 0.8, "claim_fill": 0.8, "terminal_tol_mm": 0.2})
BOUNDS.update({"ligament_mm": (0.4, 2.0), "claim_fill": (0.5, 1.0), "terminal_tol_mm": (0.05, 1.0)})
TERMINAL_PORTS = ("terminals", "phases")


def _align(d):
    """4x4 rotation taking unit vector d to +Z."""
    import trimesh

    d = np.asarray(d, float) / np.linalg.norm(d)
    return trimesh.geometry.align_vectors(d, [0, 0, 1.0])


def profile_at(m, T, h, uv, want="solid", geom=False):
    """Shape of the region at (u, v) in section z=h of mesh m moved by T: want='solid' -> the polygon containing the
    point (a shaft), 'hole' -> the interior ring containing it (a bore). None when there is none. geom=True returns
    (shape, shapely geometry)."""
    from shapely.geometry import Point, Polygon

    from .ref_features import hole_shape, section

    mm = m.copy()
    mm.apply_transform(T)
    g = section(mm, 2, h)
    if g is None or g.is_empty:
        return None
    pt = Point(uv)
    for p in getattr(g, "geoms", [g]):
        if want == "solid" and p.contains(pt):
            sh = hole_shape(p.exterior, densify=True)
            return (sh, Polygon(p.exterior)) if geom else sh
        if want == "hole":
            for ring in p.interiors:
                if Polygon(ring).contains(pt):
                    sh = hole_shape(ring, densify=True)
                    return (sh, Polygon(ring)) if geom else sh
    return None


BORE_FLAT_MM = 1.0    # most a bore wall may stand off the shaft (a D flat on a round shaft) and still be its bore
BORE_TOUCH_MM = 0.3   # a bore drives / locates the shaft only when its wall is this close to the shaft outline


def shaft_mate(shaft_mesh, bore_mesh, at, d, span, n=5, touch=BORE_TOUCH_MM):
    """[(t, shaft shape, bore shape)] at n sections over the shaft span where the bore mesh has a bore round the axis
    whose wall touches the shaft (within `touch` mm of its outline). A wider ring round the axis - a tyre stretched
    over the hub, a housing - has another body between it and the shaft and is not the shaft's bore."""
    T = _align(d)
    out = []
    for t in np.linspace(0.15, 0.85, n):
        p = np.asarray(at, float) + np.asarray(d, float) / np.linalg.norm(d) * span * t
        q = (T[:3, :3] @ p)
        b = profile_at(bore_mesh, T, q[2], q[:2], "hole", geom=True)
        if b is None:
            continue
        s_ = profile_at(shaft_mesh, T, q[2], q[:2], "solid", geom=True)
        if s_ is None:
            continue
        if b[1].exterior.distance(s_[1].exterior) > touch:   # nearest wall point must touch the shaft
            continue
        # the bore wall must hug the shaft all round: max gap from the bore ring to the shaft outline <= touch + flat
        if _ring_gap(b[1], s_[1]) > touch + BORE_FLAT_MM:
            continue
        out.append((round(float(t), 2), s_[0], b[0]))
    return out


def _ring_gap(bore_poly, shaft_poly):
    """Largest distance from a point of the bore ring to the shaft outline (a bore round a D shaft with a round hole
    shows the flat's depth here; a tyre round the hub shows the hub wall)."""
    from shapely.geometry import Point

    ring = bore_poly.exterior
    pts = [ring.interpolate(f, normalized=True) for f in np.linspace(0, 1, 72, endpoint=False)]
    return max(shaft_poly.exterior.distance(Point(q.x, q.y)) for q in pts)


def shaft_findings(ctx):
    from .. import xform

    out, n = [], 0
    r, w = ctx.r, ctx.world
    for rp in r.parts:
        cat = getattr(rp, "cat", None)
        sh = getattr(cat, "shaft", None) if cat is not None else None
        b = w.body(rp.part.id)
        if not sh or b is None or b.mesh is None:
            continue
        at = xform.apply(b.M, sh["at"])
        d = np.asarray(b.M)[:3, :3] @ np.asarray(sh.get("dir") or [1, 0, 0], float)
        L = float(sh.get("len") or 0)
        end = at + d / np.linalg.norm(d) * L
        for o in w.bodies:
            if o.id == b.id or o.is_wire or o.mesh is None or getattr(o, "fastener", None):
                continue
            lo, hi = o.aabb
            mid = (at + end) / 2
            if np.any(mid < np.asarray(lo) - 0.5) or np.any(mid > np.asarray(hi) + 0.5):
                if not any(np.all(p >= np.asarray(lo) - 0.5) and np.all(p <= np.asarray(hi) + 0.5) for p in (at, end)):
                    continue
            rows = shaft_mate(b.mesh, o.mesh, at, d, L)
            if not rows:
                continue
            n += 1
            bad = [x for x in rows if x[1] != x[2] and "other" not in (x[1], x[2])]
            if bad:
                out.append(fail("visual.shaft_mate", G, BLOCKER, "Shaft profile does not match the bore it drives",
                                f"`{rp.part.id}` shaft ({cat.id}) in `{o.id}`: shaft {bad[0][1]} vs bore {bad[0][2]} at "
                                f"{len(bad)}/{len(rows)} sections along the shaft.").on(rp.part.id, o.id).here(mid)
                           .fix("Give the catalog shaft its real profile (e.g. the N10's 3 mm D-flat) or the bore the shaft's; "
                                "a round shaft in a D-bore (or the reverse) cannot both be right."))
    if n and not out:
        out.append(ok("visual.shaft_mate", G, "Shafts match their bores", f"{n} shaft/bore pair(s) have the same profile."))
    return out


def _rings_at(m, ax, h):
    """[(centre (u, v), ring d, ligament mm)] of the closed hole rings in the section {axis = h}."""
    from shapely.geometry import LinearRing, Polygon

    from .ref_features import section

    g = section(m, ax, h)
    if g is None or g.is_empty:
        return []
    out = []
    for p in getattr(g, "geoms", [g]):
        rings = list(p.interiors)
        for i, ring in enumerate(rings):
            lr = LinearRing(ring)
            d = lr.distance(p.exterior)
            for j, o in enumerate(rings):
                if j != i:
                    d = min(d, lr.distance(LinearRing(o)))
            pc = Polygon(ring)
            out.append(((pc.centroid.x, pc.centroid.y), 2 * math.sqrt(pc.area / math.pi), float(d)))
    return out


def ring_lig(m, ax, h, c):
    """Ligament of the ring centred near c in section {axis = h} of m, or None when there is no ring there."""
    got = [x for x in _rings_at(m, ax, h) if math.dist(x[0], c) < 0.8]
    return min((x[2] for x in got), default=None)


def ligaments(m, n=30):
    """[(axis, h, centre (u, v), ring d, ligament mm)] for every closed hole ring in sections on all three axes."""
    out = []
    for ax in range(3):
        lo, hi = m.bounds[0][ax], m.bounds[1][ax]
        for f in np.linspace(0.02, 0.98, n):
            h = float(lo + (hi - lo) * f)
            out += [(ax, h, c, d, lig) for c, d, lig in _rings_at(m, ax, h)]
    return out


def face_graze(m, ax, h, c, lim, step=0.25):
    """True when a thin ring at height h is only the last slice before the bore leaves a face: one step outward
    the ring is gone (or the section is), one step inward the wall is >= lim."""
    a, b = ring_lig(m, ax, h - step, c), ring_lig(m, ax, h + step, c)
    return (a is None and b is not None and b >= lim) or (b is None and a is not None and a >= lim)


def ligament_diffs(model, ref, lim=0.8, tol=0.1):
    """[{kind: thin | open, at, msg, ref}] - thin: our ring's wall < lim (ref_lig set when the reference is as thin);
    open: the reference has a closed ring (d >= 2) whose centre is not inside a closed ring of ours at that height."""
    from shapely.geometry import Point

    from .ref_features import section

    lm = ligaments(model)
    lr = ligaments(ref) if ref is not None else []
    out = []

    def p3(ax, h, c):
        a, b = [i for i in range(3) if i != ax]
        p = [0.0] * 3
        p[ax], p[a], p[b] = h, c[0], c[1]
        return [round(x, 2) for x in p]

    for ax, h, c, d, lig in lm:
        if lig >= lim or d < 0.8:
            continue
        # the reference measured at the SAME height (not at its own sample heights: a face graze is one thin slice)
        rl = ring_lig(ref, ax, h, c) if ref is not None else None
        if rl is None and ref is not None:
            same = [x for x in lr if x[0] == ax and abs(x[1] - h) < 0.6 and math.dist(x[2], c) < 0.8]
            rl = min((x[4] for x in same), default=None)
        graze = face_graze(model, ax, h, c, lim)
        out.append({"kind": "graze" if graze else "thin", "at": p3(ax, h, c), "lig": round(lig, 2), "ref": None if rl is None else round(rl, 2),
                    "matches": graze or (rl is not None and lig >= rl - tol),
                    "msg": f"bore d{d:.1f} at {p3(ax, h, c)}: wall {lig:.2f} mm" + ("" if rl is None else f" (reference {rl:.2f})")})
    for ax, h, c, d, lig in lr:
        if d < 2.0:
            continue
        if any(x[0] == ax and abs(x[1] - h) < 0.6 and math.dist(x[2], c) < 0.8 for x in lm):
            continue
        g = section(model, ax, h)
        if g is None or g.is_empty:
            continue
        # open C: our section has material right round where the reference ring's wall is, but no closed ring
        ring_pt = Point(c[0] + d / 2 + lig / 2, c[1])
        if g.buffer(0.05).contains(ring_pt) and not g.contains(Point(c)):
            out.append({"kind": "open", "at": p3(ax, h, c), "lig": 0.0, "ref": round(lig, 2), "matches": False,
                        "msg": f"bore d{d:.1f} at {p3(ax, h, c)} is closed in the reference (wall {lig:.2f} mm) but open in ours"})
    return out


CLAIM_RE = re.compile(r"\b([xyz])\s*(-?\d+(?:\.\d+)?)\s*(?:\.\.|to|–|-)\s*(-?\d+(?:\.\d+)?)", re.I)


def claim_box(text, bounds):
    """(lo, hi) box from 'x a..b, y c-d' ranges in a deviation note (unnamed axes span `bounds`), or None."""
    got = {}
    for ax, a, b in CLAIM_RE.findall(text or ""):
        got["xyz".index(ax.lower())] = sorted((float(a), float(b)))
    if not got:
        return None
    lo, hi = np.array(bounds[0], float), np.array(bounds[1], float)
    for k, (a, b) in got.items():
        lo[k], hi[k] = a, b
    return lo, hi


def claim_fill(model, ref, others, box, step=0.2):
    """(cut mm3, filled fraction): material in the box the reference has and we do not, and the share of it that
    another body (the part the cut seats) occupies."""
    from ..world import _contains

    lo, hi = box
    ax = [np.arange(lo[i] + step / 2, hi[i], step) for i in range(3)]
    if any(len(a) == 0 for a in ax):
        return 0.0, 1.0
    g = np.stack(np.meshgrid(*ax, indexing="ij"), -1).reshape(-1, 3)
    if len(g) > 60000:
        g = g[np.random.default_rng(0).choice(len(g), 60000, replace=False)]
        step3 = float(np.prod(hi - lo)) / len(g)
    else:
        step3 = step ** 3
    cut = g[_contains(ref, g) & ~_contains(model, g)]
    if not len(cut):
        return 0.0, 1.0
    fill = np.zeros(len(cut), bool)
    for o in others:
        olo, ohi = o.bounds
        k = np.all((cut >= olo) & (cut <= ohi), axis=1)
        if k.any():
            fill[np.nonzero(k)[0]] |= _contains(o, cut[k])
    return len(cut) * step3, float(fill.mean())


def rev2_findings(ctx, prm):
    import trimesh

    from .reference_cad import ref_in_world
    from .ref_diff import clean

    out = shaft_findings(ctx)
    refs = {e.get("part"): (e, cfg, path) for e, cfg, path in _entries(ctx)}
    nlig = 0
    for rp in ctx.r.parts:
        p = rp.part
        if p.catalog is not None or str(p.process or "").lower() not in ("fdm", "sla", "molded", "cast", "resin"):
            continue
        b = ctx.world.body(p.id)
        if b is None or b.mesh is None or not len(b.mesh.faces):
            continue
        ref, e = None, {}
        if p.id in refs:
            e, cfg, path = refs[p.id]
            try:
                ref = clean(ref_in_world(trimesh.load(path, force="mesh"), e, cfg)) if path.is_file() else None
            except Exception:  # noqa: BLE001
                ref = None
        try:
            items = ligament_diffs(b.mesh, ref, prm["ligament_mm"])
        except Exception as ex:  # noqa: BLE001 - fail closed
            out.append(fail("visual.ligament", G, BLOCKER, "Bore-wall check crashed", f"`{p.id}`: {ex}").on(p.id))
            continue
        nlig += 1
        same = [x for x in items if x["matches"]]
        op, wv = _split(e, [x for x in items if not x["matches"]])
        if op:
            out.append(fail("visual.ligament", G, BLOCKER, "Wall round a bore too thin or broken through",
                            f"`{p.id}`: " + "; ".join(x["msg"] for x in op[:8]) + (f" (+{len(op) - 8})" if len(op) > 8 else ""))
                       .on(p.id).here(op[0]["at"]).fix(f"Keep >= {prm['ligament_mm']:g} mm of wall round every bore (move or shrink the bore, or thicken the wall)."))
        if same or wv:
            out.append(note("visual.ligament", G, "Thin bore walls the reference has too",
                            f"`{p.id}`: {len(same)} as thin in the reference or a face graze (thin only in the last slice before a face)" + (f", {len(wv)} reasoned deviations" if wv else "") + "."))
        # deviation claims with a stated extent
        notes = [(str(p._extra.get("deviation") or ""), None)] + [(str(d.get("reason") or ""), d) for d in e.get("deviations") or []]
        seen = set()
        for text, _ in notes:
            box = claim_box(text, b.mesh.bounds)
            if ref is None or box is None or text in seen:
                continue
            seen.add(text)
            others = [o.mesh for o in ctx.world.bodies if o.id != p.id and not o.is_wire and o.mesh is not None
                      and np.all(np.asarray(o.aabb[0]) <= box[1]) and np.all(np.asarray(o.aabb[1]) >= box[0])]
            vol, fill = claim_fill(b.mesh, ref, others, box)
            if vol > 1.0 and fill < prm["claim_fill"]:
                out.append(fail("visual.deviation_claim", G, BLOCKER, "Cut is bigger than its deviation note says",
                                f"`{p.id}`: the note \"{text[:140]}\" covers x/y/z {np.round(box[0], 1).tolist()}..{np.round(box[1], 1).tolist()}; "
                                f"{vol:.1f} mm3 of reference material is cut there but only {fill:.0%} of it is filled by the part it seats "
                                f"(need >= {prm['claim_fill']:.0%}).").on(p.id).here((box[0] + box[1]) / 2)
                           .fix("Cut only what the seated part occupies (e.g. a 1.5 mm seat, not a slot through the full height), or "
                                "correct the note to the real extent and reason."))
            elif vol > 1.0:
                out.append(ok("visual.deviation_claim", G, "Cut matches its deviation note", f"`{p.id}`: {vol:.1f} mm3, {fill:.0%} filled by the seated part.").on(p.id))
    if nlig:
        out.append(ok("visual.ligament.scan", G, "Bore walls scanned", f"{nlig} printed part(s) scanned for bore walls on all three axes."))
    out += terminal_findings(ctx, prm)
    return out


def terminal_findings(ctx, prm):
    """visual.terminal: a lead / terminal port must sit on the part's own solid (its tab or lead exists)."""
    r, w = ctx.r, ctx.world
    out, bad, n = [], [], 0
    for rp in r.parts:
        cat = getattr(rp, "cat", None)
        if cat is None or not getattr(cat, "ports", None) or cat.kind not in ("motor", "weapon_motor", "esc"):
            continue
        b = w.body(rp.part.id)
        if b is None or b.mesh is None:
            continue
        for pname in cat.ports:
            if pname not in TERMINAL_PORTS:
                continue
            p = w.port(r, f"{rp.part.id}.{pname}")
            if p is None:
                continue
            n += 1
            d = float(np.abs(b.mesh.nearest.signed_distance([p])[0]))
            inside = bool(b.inside([p])[0]) if hasattr(b, "inside") else False
            if not inside and d > prm["terminal_tol_mm"]:
                bad.append(f"`{rp.part.id}.{pname}` ({cat.id}) is {d:.2f} mm off the part: no tab or lead where the wire solders")
    if bad:
        out.append(fail("visual.terminal", G, BLOCKER, "Motor / ESC terminal feature missing", "; ".join(bad[:8]))
                   .fix("Model the terminal tabs (brushed gearmotor) or phase leads in the catalog shape, ending at the port."))
    elif n:
        out.append(ok("visual.terminal", G, "Terminals modelled", f"{n} terminal / lead port(s) sit on their part's tab or lead."))
    return out
