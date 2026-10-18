"""Per-part comparison against reference CAD meshes (`reference_cad` in the spec), used for dimensions only, never copied.

Spec: {"reference_cad": {"dir": "path/to/stls" (relative to the spec), "parts": [
    {"part": "<our part id>", "file": "<ref>.STL", "mode": "shape" | "envelope" (bought-in: dims+volume only),
     "tol_mm": 0.5, "tol_vol_frac": 0.15, "hole_tol_mm": 0.3, "at": [x, y, z] (optional expected bbox centre), "at_tol": 1.0,
     "note": "why"}]}}
Shape-intrinsic fingerprints (independent of pose): oriented-box extents (sorted), volume, genus (through-holes) and, for
plate-like parts, the holes cut through the mid-plane as (diameter, distance from the outline centroid): bores, bolt
circles and pockets. Findings:
  reference_cad.dims / .volume / .holes / .placement   each within tolerance (WARNING when off)
  reference_cad.copied (BLOCKER)  the model mesh is near-identical to the reference mesh (same triangle structure and
                                  ~0 Hausdorff after alignment): geometry must come from our parametric code, not an import.
  reference_cad.unusable          file missing/unreadable or part missing -> NOT CHECKED, never a pass.
"""

from __future__ import annotations

from pathlib import Path

import numpy as np

from ..finding import BLOCKER, WARNING, fail, ok

G = "reference"


def _cfg(spec):
    c = (spec.raw or {}).get("reference_cad") or {}
    return c if isinstance(c, dict) else {"parts": list(c)}


def fingerprint(m):
    """Pose-independent fingerprint of a trimesh mesh."""
    obb = m.bounding_box_oriented.primitive
    ext = np.asarray(obb.extents, float)
    comps = m.body_count if hasattr(m, "body_count") else 1
    genus = int(round((2 * comps - m.euler_number) / 2))
    fp = {"ext": sorted(ext.tolist(), reverse=True), "vol_cc": abs(float(m.volume)) / 1000.0, "genus": genus,
          "faces": int(len(m.faces)), "holes": None}
    if ext.min() < 0.35 * np.median(ext):
        try:
            fp["holes"] = plate_holes(m, obb)
        except Exception:  # noqa: BLE001 - optional feature
            fp["holes"] = None
    return fp


def plate_holes(m, obb=None):
    """Holes through a plate's mid-plane: sorted [(diameter mm, distance from outline centroid mm)]."""
    import trimesh
    from shapely.geometry import LineString, Polygon
    from shapely.ops import polygonize, unary_union

    obb = obb or m.bounding_box_oriented.primitive
    T, ext = obb.transform, obb.extents
    ax = int(np.argmin(ext))
    n, c = T[:3, ax], T[:3, 3]
    u, v = T[:3, (ax + 1) % 3], T[:3, (ax + 2) % 3]
    segs = trimesh.intersections.mesh_plane(m, n, c)
    q = lambda p: (round(float((p - c) @ u), 3), round(float((p - c) @ v), 3))  # noqa: E731 - snap so loops close
    lines = [LineString([q(a), q(b)]) for a, b in segs if q(a) != q(b)]
    polys = sorted(polygonize(unary_union([ln for ln in lines if ln.length > 1e-9])), key=lambda p: -Polygon(p.exterior).area)  # outline = largest shell, not largest face
    if not polys:
        return []
    outer = polys[0]
    oc = np.array(outer.centroid.coords[0])
    out = []
    for ring in outer.interiors:
        hp = Polygon(ring)
        if hp.area < 0.2:
            continue
        out.append((round(2 * float(np.sqrt(hp.area / np.pi)), 2),
                    round(float(np.linalg.norm(np.array(hp.centroid.coords[0]) - oc)), 2)))
    return sorted(out)


def match_holes(a, b, tol):
    """Greedy match of (d, r) lists. Returns (unmatched in a, unmatched in b)."""
    b = list(b)
    miss = []
    for d, r in a:
        j = next((k for k, (d2, r2) in enumerate(b) if abs(d - d2) <= tol and abs(r - r2) <= max(tol, 0.5)), None)
        if j is None:
            miss.append((d, r))
        else:
            b.pop(j)
    return miss, b


def _aligned(m):
    """Vertices in the principal frame (centroid at 0, axes by decreasing variance)."""
    V = np.asarray(m.vertices, float)
    V = V - V.mean(0)
    w, E = np.linalg.eigh(np.cov(V.T))
    return V @ E[:, np.argsort(w)[::-1]]


def is_copy(ma, mb, rel=0.002):
    """Near-identical meshes: same triangle structure (face count within 1%) and Hausdorff ~0 after principal alignment."""
    from scipy.spatial import cKDTree

    fa, fb = len(ma.faces), len(mb.faces)
    if abs(fa - fb) > 0.01 * max(fa, fb):
        return False, None
    A, B = _aligned(ma), _aligned(mb)
    diag = float(np.linalg.norm(B.max(0) - B.min(0))) or 1.0
    tb = cKDTree(B)
    best = None
    for sx in (1, -1):
        for sy in (1, -1):
            for sz in (1, -1):
                As = A * (sx, sy, sz)
                h = max(tb.query(As)[0].max(), cKDTree(As).query(B)[0].max())
                best = h if best is None else min(best, h)
    return best < rel * diag, best


def run(ctx):
    spec = ctx.r.spec
    cfg = _cfg(spec)
    items = cfg.get("parts") or []
    if not items:
        return []
    import trimesh

    base = Path(getattr(spec, "base_dir", ".") or ".")
    rdir = base / (cfg.get("dir") or ".")
    out = []
    for e in items:
        pid, fn = e.get("part"), e.get("file")
        b = ctx.world.body(pid) if pid else None
        path = rdir / (fn or "")
        if b is None or not fn or not path.is_file():
            why = f"part `{pid}` not in the model" if b is None else f"reference file `{path}` not found"
            out.append(fail("reference_cad.unusable", G, WARNING, "Reference CAD comparison not possible", why))
            ctx.not_checked.append(f"Reference CAD `{fn}` vs `{pid}`")
            continue
        try:
            ref = trimesh.load(path, force="mesh")
            mod = b.mesh
            fr, fm = fingerprint(ref), fingerprint(mod)
        except Exception as ex:  # noqa: BLE001 - fail closed
            out.append(fail("reference_cad.unusable", G, WARNING, "Reference CAD comparison crashed", f"`{pid}` vs `{fn}`: {ex}"))
            ctx.not_checked.append(f"Reference CAD `{fn}` vs `{pid}`")
            continue
        ctx.metrics[f"reference_cad.{pid}"] = {"ref": fr, "model": fm}
        copied, h = is_copy(mod, ref)
        if copied:
            out.append(fail("reference_cad.copied", G, BLOCKER, "Part geometry is a copy of the reference CAD",
                            f"`{pid}` matches `{fn}` triangle for triangle (Hausdorff {h:.4f} mm after alignment).")
                       .on(pid).fix("Reference CAD is for measurement only. Build the part from parametric code."))
            continue
        tol = float(e.get("tol_mm", 0.5))
        de = [round(a - r, 2) for a, r in zip(fm["ext"], fr["ext"])]
        msg = f"`{pid}` vs `{fn}`: extents {np.round(fm['ext'], 2).tolist()} vs {np.round(fr['ext'], 2).tolist()} mm"
        out.append((ok if max(map(abs, de)) <= tol else lambda *a: fail(*a[:2], WARNING, *a[2:]))(
            "reference_cad.dims", G, "Part size matches the reference CAD" if max(map(abs, de)) <= tol else "Part size differs from the reference CAD",
            msg + f" (diff {de}, tol {tol})").on(pid))
        tv = float(e.get("tol_vol_frac", 0.15))
        rv = fm["vol_cc"] / fr["vol_cc"] - 1 if fr["vol_cc"] > 0 else 0.0
        vmsg = f"`{pid}` volume {fm['vol_cc']:.3f} vs {fr['vol_cc']:.3f} cm3 ({rv:+.0%}, tol ±{tv:.0%})"
        out.append(ok("reference_cad.volume", G, "Part volume matches", vmsg).on(pid) if abs(rv) <= tv else
                   fail("reference_cad.volume", G, WARNING, "Part volume differs from the reference CAD", vmsg).on(pid)
                   .fix("Match wall thickness, pockets and lightening holes to the reference."))
        if e.get("mode", "shape") == "shape":
            ht = float(e.get("hole_tol_mm", 0.3))
            if fr["holes"] is not None:
                if fm["holes"] is None:
                    miss, extra = fr["holes"], []
                else:
                    miss, extra = match_holes(fr["holes"], fm["holes"], ht)
                hmsg = (f"`{pid}`: reference has {len(fr['holes'])} holes (d, r from centre) {fr['holes']}; model "
                        f"{len(fm['holes'] or [])}. Missing {miss}; extra {extra}.")
                out.append(ok("reference_cad.holes", G, "Holes, bores and bolt circles match", hmsg).on(pid) if not miss and not extra else
                           fail("reference_cad.holes", G, WARNING, "Holes differ from the reference CAD", hmsg).on(pid)
                           .fix("Add/move the missing holes (bolt circle radius, bore diameter)."))
            elif fm["genus"] != fr["genus"]:
                out.append(fail("reference_cad.holes", G, WARNING, "Through-hole count differs from the reference CAD",
                                f"`{pid}` has {fm['genus']} through-holes, `{fn}` has {fr['genus']}.").on(pid))
            else:
                out.append(ok("reference_cad.holes", G, "Through-hole count matches", f"`{pid}`: {fm['genus']} through-holes.").on(pid))
        if e.get("at") is not None:
            lo, hi = b.aabb
            c = (np.asarray(lo) + np.asarray(hi)) / 2
            d = float(np.linalg.norm(c - np.asarray(e["at"], float)))
            at_tol = float(e.get("at_tol", 1.0))
            pmsg = f"`{pid}` centre {np.round(c, 1).tolist()} vs expected {e['at']} ({d:.1f} mm, tol {at_tol})"
            out.append(ok("reference_cad.placement", G, "Part placed as in the reference", pmsg).on(pid) if d <= at_tol else
                       fail("reference_cad.placement", G, WARNING, "Part placed differently from the reference", pmsg).on(pid))
    return out
