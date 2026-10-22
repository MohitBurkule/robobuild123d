"""Per-part comparison against reference CAD meshes (`reference_cad` in the spec), used for dimensions only, never copied.

Spec: {"reference_cad": {"dir": "path/to/stls" (relative to the spec), "parts": [
    {"part": "<our part id>", "file": "<ref>.STL", "mode": "shape" | "envelope" (bought-in: dims+volume only),
     "tol_mm": 0.5, "tol_vol_frac": 0.15, "hole_tol_mm": 0.3, "at": [x, y, z] (optional expected bbox centre), "at_tol": 1.0,
     "note": "why"}]}}
Shape-intrinsic fingerprints (independent of pose): oriented-box extents (sorted), volume, genus (through-holes) and, for
plate-like parts, the holes cut through the mid-plane as (diameter, distance from the outline centroid): bores, bolt
circles and pockets. Findings:
  reference_cad.dims / .volume / .holes / .placement   each within tolerance (WARNING when off)
  reference_cad.silhouette (BLOCKER)  for "shape" parts when a `ref_to_world` 4x4 is given (config or entry; plus
                                  `mirror_x` for the opposite hand, `ref_shift` for a second copy, `outline_only` to
                                  fill holes first): the reference is placed in our world frame and the
                                  silhouettes along X, Y and Z must each reach IoU >= `iou_min` (default 0.9). This
                                  catches a wrong outline, missing cut-outs, wrong heights and wrong placement.
  `with_parts` [+ `clip_to_ref`]: compare the union of this part and the listed parts (clipped to the reference's span),
                                  for a bought-in part modelled as more than one body.
  reference_cad.copied (BLOCKER)  the model mesh is near-identical to the reference mesh (same triangle structure and
                                  ~0 Hausdorff after alignment): geometry must come from our parametric code, not an import.
  reference_cad.unusable          file missing/unreadable or part missing -> NOT CHECKED, never a pass.
With a frame (the reference placed in our world frame) every entry also gets:
  reference_cad.step_placement (BLOCKER)  part bbox centre vs the reference's, in the STEP assembly frame
                                  (`placement_tol_mm`, default 0.5).
  reference_cad.diff (BLOCKER, shape parts)  boolean diff (ref_diff.boolean_diff): every blob of extra (model - ref) or
                                  missing (ref - model) material over `diff_min_mm3` (2) and `diff_min_thick_mm` (0.3)
                                  is one feature difference and must be fixed or listed in the entry's `deviations`
                                  [{"near": [x, y, z], "r": 3, "reason": "..."}]; surface deviation max / p95 both ways
                                  is reported, and every cluster of surface points deviating more than `dev_tol_mm`
                                  (0.5) either way is a difference too. `diff_render_dir`: write a deviation heat map per part.
  reference_cad.features (BLOCKER, shape parts)  ref_features.compare_sections: sections at 25/50/75 % on all three
                                  axes; hole count and shape (round / D / hex / slot) matched by centroid, hole
                                  profile along the thin axis (plain / countersink / counterbore / blind). A missing,
                                  extra or differently shaped hole, or a countersink the other side lacks, fails
                                  unless listed in `deviations`. Section area / IoU and fillet-vs-sharp corner
                                  differences are reported as warnings.
"""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np

from ..finding import BLOCKER, WARNING, fail, note, ok

G = "reference"


def _cfg(spec):
    c = (spec.raw or {}).get("reference_cad") or {}
    return c if isinstance(c, dict) else {"parts": list(c)}


def fingerprint(m):
    """Pose-independent fingerprint of a trimesh mesh (memoised on the mesh content and this file in the run cache)."""
    from .. import cache

    return cache.memo("ref_fingerprint", (cache.source_hash(__file__), np.asarray(m.vertices), np.asarray(m.faces)),
                      lambda: _fingerprint(m))


def _fingerprint(m):
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


RASTER_SNAP_DP = 4   # vertices snap to 1e-4 mm before rasterising: STL float noise must not flip a pixel edge


def _raster(meshes, ax, lo, res, shape):
    """Silhouette of meshes projected along world axis `ax` on a grid (origin lo, pixel res mm)."""
    from PIL import Image, ImageDraw

    a, b = [i for i in range(3) if i != ax]
    img = Image.new("1", shape, 0)
    d = ImageDraw.Draw(img)
    for m in meshes:
        T = np.round(np.asarray(m.vertices, float), RASTER_SNAP_DP)[np.asarray(m.faces)][:, :, [a, b]]   # 0.89999962 is 0.9
        T = np.round((T - np.round(np.asarray(lo, float), RASTER_SNAP_DP)[[a, b]]) / res, 6)
        for t in T:
            d.polygon([tuple(p) for p in t], fill=1, outline=1)
    return np.asarray(img, bool)


def silhouette_iou(ma, mb, res=0.1, fill_holes=False):
    """IoU of the silhouettes of two meshes (already in one frame) projected along X, Y and Z: [iou_x, iou_y, iou_z].
    fill_holes: compare outlines only (holes inside a silhouette filled), for a part that shares the reference's outline
    but not its cut-outs."""
    lo = np.minimum(ma.bounds[0], mb.bounds[0]) - 1.0
    hi = np.maximum(ma.bounds[1], mb.bounds[1]) + 1.0
    out = []
    for ax in range(3):
        a, b = [i for i in range(3) if i != ax]
        shape = (int(np.ceil((hi[a] - lo[a]) / res)) + 1, int(np.ceil((hi[b] - lo[b]) / res)) + 1)
        A, B = _raster([ma], ax, lo, res, shape), _raster([mb], ax, lo, res, shape)
        if fill_holes:
            from scipy.ndimage import binary_fill_holes
            A, B = binary_fill_holes(A), binary_fill_holes(B)
        u = np.logical_or(A, B).sum()
        out.append(float(np.logical_and(A, B).sum() / u) if u else 1.0)
    return out


def ref_in_world(ref, e, cfg):
    """Reference mesh moved into the model's world frame: the entry's (or the config's) `ref_to_world` 4x4, then an
    optional mirror across X = 0 (`mirror_x`, for the opposite-hand copy of a handed part) and shift (`ref_shift`,
    for a second copy of the same part elsewhere)."""
    T = e.get("ref_to_world", cfg.get("ref_to_world"))
    m = ref.copy()
    if T is not None:
        m.apply_transform(np.asarray(T, float))
    if e.get("mirror_x"):
        m.apply_transform(np.diag([-1.0, 1, 1, 1]))
    if e.get("ref_shift") is not None:
        m.apply_translation(np.asarray(e["ref_shift"], float))
    return m


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
    if min(fa, fb) < 100:  # a primitive (a 12-triangle box) carries no copyable detail: equal boxes are not an import
        return False, None
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


MESH_READ = re.compile(r"""(trimesh\.load|load_mesh|read_stl|stl\.mesh|import_step|importStep|STEPControl_Reader|read_step|"""
                       r"""cq\.importers|np\.load\(|numpy\.load\(|open\([^)]*\.(stl|step|stp|obj|ply)\b)""", re.I)
TABLE_MIN_PTS = 20      # a coordinate table this long is an imported outline, not a design sketch
SAME_TESS_MM = 1e-3     # vertices that coincide this closely (with equal face counts) are the reference's own tessellation


def copy_evidence(spec, mod, ref, h):
    """Provenance evidence that a near-identical part was imported rather than rebuilt: the build code reads mesh / STEP
    data, carries a large coordinate table, or the mesh has the reference's own tessellation (equal face count and
    vertices coinciding to SAME_TESS_MM). A small Hausdorff alone is what a faithful parametric rebuild of a simple part
    should achieve, so it is not evidence."""
    ev = []
    if h is not None and h < SAME_TESS_MM and len(mod.faces) == len(ref.faces):
        ev.append(f"same tessellation ({len(mod.faces)} faces, vertices within {h:.1e} mm)")
    try:
        from .param_lint import sources
        from .practice import point_tables
        paths = sources(spec) if spec is not None else []
    except Exception:  # noqa: BLE001
        paths = []
    for path in paths:
        try:
            text = Path(path).read_text()
        except OSError:
            continue
        for i, ln in enumerate(text.splitlines(), 1):
            if MESH_READ.search(ln) and not ln.lstrip().startswith("#"):
                ev.append(f"{Path(path).name}:{i} reads mesh/STEP data")
        try:
            ev += [f"{Path(path).name}:{ln} `{nm}` table of {n} points" for ln, nm, n in point_tables(text) if n >= TABLE_MIN_PTS]
        except SyntaxError:
            pass
    return ev


def _clip_box(m, lo, hi):
    """Mesh clipped to an axis-aligned box (capped)."""
    import trimesh

    for ax in range(3):
        n = np.zeros(3)
        n[ax] = 1.0
        m = trimesh.intersections.slice_mesh_plane(m, n, n * lo[ax], cap=True)
        if m is None or not len(m.faces):
            return None
        m = trimesh.intersections.slice_mesh_plane(m, -n, n * hi[ax], cap=True)
        if m is None or not len(m.faces):
            return None
    return m


def _cfg_has_frame(e, cfg):
    return e.get("ref_to_world", cfg.get("ref_to_world")) is not None


def run(ctx):
    return check_entries(ctx, _frame_checks)


def check_entries(ctx, frame_checks, exact=True, parts=None):
    """Every `reference_cad` entry: fingerprint checks, then `frame_checks(ctx, e, cfg, pid, fn, mod, ref)` for entries
    placed in our world frame. exact=False (the fast proxy, robot/proxy/refcad.py) skips the copy test and the
    rasterised silhouette, which `frame_checks` then stands in for; `parts` limits the entries checked."""
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
        if parts is not None and pid not in parts:
            continue
        b = ctx.world.body(pid) if pid else None
        path = rdir / (fn or "")
        if b is None or not fn or not path.is_file():
            # a part id that is not in the model is a typo that silently disables BLOCKER checks: fail closed
            why = f"part `{pid}` not in the model" if b is None else f"reference file `{path}` not found"
            out.append(fail("reference_cad.unusable", G, BLOCKER if b is None else WARNING, "Reference CAD comparison not possible", why))
            ctx.not_checked.append(f"Reference CAD `{fn}` vs `{pid}`")
            continue
        try:
            ref = trimesh.load(path, force="mesh")
            mod = b.mesh
            if e.get("with_parts"):
                # a bought-in part modelled as several bodies (e.g. a prop-mount flange plus its spigot inside a shaft
                # body): compare their union, clipped to the reference's span when `clip_to_ref` (in the world frame)
                extra = [ctx.world.body(x) for x in e["with_parts"]]
                if any(x is None for x in extra):
                    raise ValueError(f"with_parts {e['with_parts']} not all in the model")
                ms = [mod] + [x.mesh for x in extra]
                if e.get("clip_to_ref") and _cfg_has_frame(e, cfg):
                    rw = ref_in_world(ref, e, cfg)
                    ms = [_clip_box(m, rw.bounds[0] - 0.05, rw.bounds[1] + 0.05) for m in ms]
                mod = trimesh.util.concatenate([m for m in ms if m is not None and len(m.faces)])
            fr, fm = fingerprint(ref), fingerprint(mod)
        except Exception as ex:  # noqa: BLE001 - fail closed
            out.append(fail("reference_cad.unusable", G, WARNING, "Reference CAD comparison crashed", f"`{pid}` vs `{fn}`: {ex}"))
            ctx.not_checked.append(f"Reference CAD `{fn}` vs `{pid}`")
            continue
        ctx.metrics[f"reference_cad.{pid}"] = {"ref": fr, "model": fm}
        copied, h = is_copy(mod, ref) if exact else (False, None)
        ev = copy_evidence(spec, mod, ref, h) if copied else []
        if copied and not ev:
            out.append(note("reference_cad.faithful", G, "Faithful parametric rebuild",
                            f"`{pid}` is within {h:.4f} mm of `{fn}` but the build code shows no import (no mesh/STEP read, "
                            f"no coordinate table >= {TABLE_MIN_PTS} points, its own tessellation).").on(pid))
        elif copied:
            out.append(fail("reference_cad.copied", G, BLOCKER, "Part geometry is a copy of the reference CAD",
                            f"`{pid}` matches `{fn}` (Hausdorff {h:.4f} mm after alignment) and: {'; '.join(ev[:4])}.")
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
        if exact and (e.get("mode", "shape") == "shape" or e.get("outline_only")) and _cfg_has_frame(e, cfg):
            need = float(e.get("iou_min", cfg.get("iou_min", 0.9)))
            try:
                ious = silhouette_iou(mod, ref_in_world(ref, e, cfg), float(cfg.get("iou_res_mm", 0.1)), bool(e.get("outline_only")))
            except Exception as ex:  # noqa: BLE001 - fail closed
                ious = None
                out.append(fail("reference_cad.silhouette", G, BLOCKER, "Silhouette comparison crashed", f"`{pid}` vs `{fn}`: {ex}").on(pid))
                ctx.not_checked.append(f"Silhouette of `{pid}` vs `{fn}`")
            if ious is not None:
                ctx.metrics.setdefault(f"reference_cad.{pid}", {})["iou"] = ious
                smsg = (f"`{pid}` vs `{fn}` {'outline' if e.get('outline_only') else 'silhouette'} IoU along X/Y/Z "
                        f"{[round(v, 3) for v in ious]} (need >= {need} on every axis, reference placed in our world frame)")
                out.append(ok("reference_cad.silhouette", G, "Part shape matches the reference in all three views", smsg).on(pid)
                           if min(ious) >= need else
                           fail("reference_cad.silhouette", G, BLOCKER, "Part shape differs from the reference CAD", smsg).on(pid)
                           .fix("Match the outline seen along the worst axis: outline, cut-outs, heights and placement."))
        if _cfg_has_frame(e, cfg):
            out += frame_checks(ctx, e, cfg, pid, fn, mod, ref)
        if e.get("at") is not None:
            lo, hi = b.aabb
            c = (np.asarray(lo) + np.asarray(hi)) / 2
            d = float(np.linalg.norm(c - np.asarray(e["at"], float)))
            at_tol = float(e.get("at_tol", 1.0))
            pmsg = f"`{pid}` centre {np.round(c, 1).tolist()} vs expected {e['at']} ({d:.1f} mm, tol {at_tol})"
            out.append(ok("reference_cad.placement", G, "Part placed as in the reference", pmsg).on(pid) if d <= at_tol else
                       fail("reference_cad.placement", G, WARNING, "Part placed differently from the reference", pmsg).on(pid))
    return out


DEV_R_MAX = 5.0   # mm: a deviation waiver is a local note, not a region of the part
PATH_R_MAX = 3.0        # mm: a path (capsule) waiver's radius
PATH_MM3_MAX = 600.0    # mm3: hard cap on the volume one path waiver may excuse (its `max_mm3` must be <= this)
PATH_CITE = re.compile(r"(RV\d|RVRN|STEP|\.stl|FS\d|reference|datasheet|design[- ]intent|intent)", re.I)


def path_dist(P, path):
    """Distance from points P (k,3) to the polyline `path` (the capsule axis)."""
    from ._review import polyline_dist

    return polyline_dist(path, P)


def _path_valid(d):
    path = d.get("path")
    if not isinstance(path, (list, tuple)) or len(path) < 2 or any(len(q) != 3 for q in path):
        return "`path` needs >= 2 [x, y, z] points"
    if float(d.get("r", 0) or 0) <= 0 or float(d.get("r")) > PATH_R_MAX:
        return f"path r {d.get('r')} mm must be in (0, {PATH_R_MAX}]"
    if d.get("max_mm3") is None or not (0 < float(d["max_mm3"]) <= PATH_MM3_MAX):
        return f"path `max_mm3` must be set and <= {PATH_MM3_MAX:g}"
    if not PATH_CITE.search(str(d.get("reason") or "")) or len(str(d.get("reason")).strip()) < 20:
        return "path reason must say why and cite the reference, a datasheet or the design intent"
    return None


def _dev_valid(d):
    """None when the waiver is usable, else why not (no reason, no centre, radius over the cap). A path waiver
    {"path": [[x,y,z], ...], "r" <= 3, "max_mm3" <= 600, "reason"} is a capsule round a polyline (a groove or a
    channel): the whole blob must lie inside it and its volume must not exceed max_mm3."""
    if not str(d.get("reason") or "").strip():
        return "no reason"
    if d.get("path") is not None:
        return _path_valid(d)
    if d.get("near") is None:
        return "no `near` point"
    if float(d.get("r", 3.0)) > DEV_R_MAX:
        return f"r {d.get('r')} mm > cap {DEV_R_MAX} mm"
    return None


def split_waivers(e):
    """{id(d): why} for sphere waivers that dodge DEV_R_MAX by splitting: spheres of one entry with the same reason
    (one feature) that overlap or touch form a group, and the sphere enclosing the group must stay within the cap.
    Every member of an over-cap group waives nothing (two r 4.5 spheres 5 mm apart are one r 7 region)."""
    ds = [d for d in (e.get("deviations") or []) if d.get("path") is None and d.get("near") is not None and not _dev_valid(d)]
    n = len(ds)
    par = list(range(n))

    def root(i):
        while par[i] != i:
            par[i] = par[par[i]]
            i = par[i]
        return i

    C = [np.asarray(d["near"], float) for d in ds]
    R = [float(d.get("r", 3.0)) for d in ds]
    for i in range(n):
        for j in range(i + 1, n):
            if str(ds[i]["reason"]).strip() == str(ds[j]["reason"]).strip() and np.linalg.norm(C[i] - C[j]) <= R[i] + R[j]:
                par[root(i)] = root(j)
    groups = {}
    for i in range(n):
        groups.setdefault(root(i), []).append(i)
    out = {}
    for g in groups.values():
        if len(g) < 2:
            continue
        span = max([R[i] for i in g] + [(np.linalg.norm(C[i] - C[j]) + R[i] + R[j]) / 2 for i in g for j in g if i < j])
        if span > DEV_R_MAX + 1e-9:
            for i in g:
                out[id(ds[i])] = (f"{len(g)} overlapping spheres with the same reason span r {span:.1f} mm > cap {DEV_R_MAX} mm "
                                  "(one feature: split spheres are capped as their union)")
    return out


def _covers(d, pt, bbox=None, pts=None, vol=None):
    """True when the single valid waiver `d` covers a blob at pt (whole bbox / points inside it, path volume cap)."""
    if _dev_valid(d):
        return False
    if d.get("path") is not None:
        path, r = np.asarray(d["path"], float), float(d["r"])
        if vol is not None and float(vol) > float(d["max_mm3"]):
            return False
        Q = np.asarray(pts, float) if pts is not None and len(pts) else (
            np.array([[bbox[i][k] for k, i in enumerate(ix)] for ix in np.ndindex(2, 2, 2)], float) if bbox is not None else
            np.atleast_2d(np.asarray(pt, float)))
        return float(path_dist(Q, path).max()) <= r
    c, r = np.asarray(d["near"], float), float(d.get("r", 3.0))
    if np.linalg.norm(np.asarray(pt, float) - c) > r:
        return False
    if bbox is not None:
        lo, hi = np.asarray(bbox[0], float), np.asarray(bbox[1], float)
        if np.linalg.norm(np.maximum(np.abs(lo - c), np.abs(hi - c))) > r:
            return False
    return True


def _anchor(d):
    return np.asarray(d["near"], float) if d.get("near") is not None else np.asarray(d["path"], float).mean(0)


def claim(items, e):
    """practice.waiver_bounds: each waiver explains at most ONE item of each kind (a blob / cluster dict with "centroid"
    or "at", optional "kind", "bbox", "pts", "volume_mm3"): the covered item nearest its centre (a changed feature is
    one extra and / or one missing blob). Other items inside the same sphere are still differences. Returns ({item index: reason}, [(index, reason)] of items a waiver's sphere held but did not
    claim)."""
    got, held = {}, []
    split = split_waivers(e)
    devs = [d for d in (e.get("deviations") or []) if not _dev_valid(d) and id(d) not in split]
    for d in devs:
        cand = []
        for i, b in enumerate(items):
            if i in got:
                continue
            c = b.get("centroid", b.get("at"))
            if _covers(d, c, b.get("bbox"), b.get("pts"), b.get("volume_mm3")):
                cand.append((float(np.linalg.norm(np.asarray(c, float) - _anchor(d))), i))
        taken = set()
        for _, i in sorted(cand):
            k = items[i].get("kind")
            if k in taken:
                held.append((i, d["reason"]))
                continue
            taken.add(k)
            got[i] = d["reason"]
    held = [(i, w) for i, w in held if i not in got]
    return got, held


def _covered(pt, e, bbox=None, pts=None, vol=None):
    """A diff at `pt` (3D) explained by one of the entry's valid `deviations` -> its reason, else None. With `bbox`
    (the blob's [lo, hi]) the whole box must fit inside the waiver sphere, not just the centroid. A path waiver covers
    a blob only when every blob point (`pts`, else the bbox corners) is within r of its polyline and `vol` <= max_mm3."""
    split = split_waivers(e)
    for d in e.get("deviations") or []:
        if _dev_valid(d) or id(d) in split:
            continue
        if d.get("path") is not None:
            path, r = np.asarray(d["path"], float), float(d["r"])
            if vol is not None and float(vol) > float(d["max_mm3"]):
                continue
            Q = np.asarray(pts, float) if pts is not None and len(pts) else (
                np.array([[bbox[i][k] for k, i in enumerate(ix)] for ix in np.ndindex(2, 2, 2)], float) if bbox is not None else
                np.atleast_2d(np.asarray(pt, float)))
            if float(path_dist(Q, path).max()) <= r:
                return d["reason"]
            continue
        c, r = np.asarray(d["near"], float), float(d.get("r", 3.0))
        if np.linalg.norm(np.asarray(pt, float) - c) > r:
            continue
        if bbox is not None:
            lo, hi = np.asarray(bbox[0], float), np.asarray(bbox[1], float)
            far = np.maximum(np.abs(lo - c), np.abs(hi - c))   # farthest bbox corner from the centre
            if np.linalg.norm(far) > r:
                continue
        return d["reason"]
    return None


def deviation_findings(e, pid):
    """BLOCKER for each waiver with no reason, no centre or an oversized radius (such a waiver waives nothing)."""
    out = []
    split = split_waivers(e)
    for d in e.get("deviations") or []:
        why = _dev_valid(d) or split.get(id(d))
        if why:
            out.append(fail("reference_cad.deviation", G, BLOCKER, "Invalid reference deviation waiver",
                            f"`{pid}` deviation at {d.get('near')} (r {d.get('r', 3.0)}): {why}; it waives nothing.").on(pid)
                       .fix(f"Give each deviation a `reason` and r <= {DEV_R_MAX} mm; a region larger than that is a real deviation to fix (overlapping spheres of one feature count as their union)."))
    return out


def _pt3(ax_name, h, uv):
    ax = "XYZ".index(ax_name)
    a, b = [i for i in range(3) if i != ax]
    p = [0.0, 0.0, 0.0]
    p[ax], p[a], p[b] = h, uv[0], uv[1]
    return p


def step_placement(e, cfg, pid, mod, rw):
    """reference_cad.step_placement: part bbox centre vs the reference's in the STEP frame (shared with the proxy)."""
    cm = (mod.bounds[0] + mod.bounds[1]) / 2
    cr = (rw.bounds[0] + rw.bounds[1]) / 2
    d = float(np.linalg.norm(cm - cr))
    out = []
    tol = float(e.get("placement_tol_mm", cfg.get("placement_tol_mm", 0.5)))
    msg = f"`{pid}` bbox centre {np.round(cm, 2).tolist()} vs STEP {np.round(cr, 2).tolist()} ({d:.2f} mm, tol {tol})"
    out.append(ok("reference_cad.step_placement", G, "Part sits where the STEP assembly puts it", msg).on(pid) if d <= tol else
               fail("reference_cad.step_placement", G, BLOCKER, "Part placed differently from the STEP assembly", msg).on(pid)
               .fix("Move the part (or its features) to the STEP placement."))
    return out


def _frame_checks(ctx, e, cfg, pid, fn, mod, ref):
    from . import ref_diff, ref_features

    rw = ref_diff.clean(ref_in_world(ref, e, cfg))
    out = step_placement(e, cfg, pid, mod, rw)
    if e.get("mode", "shape") != "shape":
        return out
    try:
        bd = ref_diff.boolean_diff(mod, rw, float(e.get("diff_min_mm3", cfg.get("diff_min_mm3", 2.0))),
                                   float(e.get("diff_min_thick_mm", cfg.get("diff_min_thick_mm", 0.3))))
        dev = ref_diff.surface_deviation(mod, rw, 8000)
    except Exception as ex:  # noqa: BLE001 - fail closed
        out.append(fail("reference_cad.diff", G, BLOCKER, "Geometric diff crashed", f"`{pid}` vs `{fn}`: {ex}").on(pid))
        return out
    rdir = e.get("diff_render_dir", cfg.get("diff_render_dir"))
    if rdir:
        try:
            Path(rdir).mkdir(parents=True, exist_ok=True)
            ref_diff.render_deviation(dev, str(Path(rdir) / f"{pid}.png"), pid)
        except Exception:  # noqa: BLE001 - render is optional
            pass
    open_, expl = [], []
    out += deviation_findings(e, pid)
    waived = 0.0
    items = [dict(b, kind=kind) for kind in ("extra", "missing") for b in bd[kind]]
    got, held = claim(items, e)
    for i, b in enumerate(items):
        why = got.get(i)
        waived += float(b["volume_mm3"]) if why else 0.0
        (expl if why else open_).append(f"{b['kind']} {b['volume_mm3']} mm3 (t {b['thick_mm']}) at {b['centroid']}" + (f" [{why}]" if why else ""))
    dtol = float(e.get("dev_tol_mm", cfg.get("dev_tol_mm", 0.5)))
    cl = ref_diff.deviation_clusters(dev, dtol, min_pts=int(e.get("dev_min_pts", cfg.get("dev_min_pts", 2))))
    cgot, chold = claim(cl, e)
    for i, c in enumerate(cl):
        why = cgot.get(i)
        (expl if why else open_).append(f"{c['kind']} surface {c['max_mm']} mm (> {dtol}, {c['n']} pts) at {c['centroid']}" + (f" [{why}]" if why else ""))
    held_n = len(held) + len(chold)
    ctx.metrics.setdefault(f"reference_cad.{pid}", {})["diff"] = {k: bd[k] for k in ("method", "extra_mm3", "missing_mm3")} | {
        "blobs_open": len(open_), "blobs_explained": len(expl), "waived_mm3": round(waived, 2), "held_not_claimed": held_n,
        "dev": {k: v for k, v in dev.items() if not k.startswith("_")}}
    dmsg = (f"`{pid}` vs `{fn}` ({bd['method']}): extra {bd['extra_mm3']} mm3, missing {bd['missing_mm3']} mm3; surface deviation "
            f"model->ref max {dev['model_to_ref']['max']} / p95 {dev['model_to_ref']['p95']} mm, ref->model max {dev['ref_to_model']['max']} / "
            f"p95 {dev['ref_to_model']['p95']} mm. Unexplained blobs: {open_[:12]}{' ...' if len(open_) > 12 else ''}. Explained: {len(expl)} ({waived:.1f} mm3 waived).")
    out.append(ok("reference_cad.diff", G, "Every geometric difference from the reference is fixed or reasoned", dmsg).on(pid) if not open_ else
               fail("reference_cad.diff", G, BLOCKER, "Unexplained geometric differences from the reference", dmsg).on(pid)
               .fix("Each blob is one feature difference: fix it, or list it in the entry's `deviations` with the reason."))
    out += local_findings(e, cfg, pid, fn, mod, rw, ctx)
    try:
        from .sldprt_dump import exact_for

        try:
            ex = exact_for(ctx.r.spec, e)
        except Exception:  # noqa: BLE001 - estimates only
            ex = None
        fd, st = ref_features.compare_sections(mod, rw, exact_d=(ex or {}).get("hole_d"))
    except Exception as ex:  # noqa: BLE001
        out.append(fail("reference_cad.features", G, BLOCKER, "Feature comparison crashed", f"`{pid}`: {ex}").on(pid))
        return out
    hard = [x for x in fd if x["severity"] == "blocker" and not _covered(_pt3(x["axis"], x["h"], x["at"]), e)]
    soft = [x for x in fd if x["severity"] != "blocker"]
    ncorner = sum(1 for x in soft if x["kind"] == "corner")
    ctx.metrics.setdefault(f"reference_cad.{pid}", {})["features"] = {"stats": st, "blockers": len(hard), "warnings": len(soft), "corner_diffs": ncorner}
    fmsg = (f"`{pid}`: {st['sections']} sections, {st['holes_ref']} reference / {st['holes_model']} model hole cuts. "
            + (f"Feature differences: {[x['msg'] for x in hard][:10]}" if hard else "Holes, hole shapes and countersinks match."))
    out.append(ok("reference_cad.features", G, "Holes, hole shapes and countersinks match the reference", fmsg).on(pid) if not hard else
               fail("reference_cad.features", G, BLOCKER, "Hole / countersink features differ from the reference", fmsg).on(pid)
               .fix("Match the hole (count, round / D / hex / slot, countersink) or list it in `deviations` with the reason."))
    if soft:
        out.append(fail("reference_cad.sections", G, WARNING, "Cross-sections differ from the reference",
                        f"`{pid}`: {len(soft) - ncorner} section area/IoU/hole-size differences, {ncorner} corner (fillet/chamfer) differences: "
                        f"{[x['msg'] for x in soft if x['kind'] != 'corner'][:6]}").on(pid))
    else:
        out.append(ok("reference_cad.sections", G, "Cross-sections match the reference", f"`{pid}`: all sections within tolerance").on(pid))
    return out


LOCAL_TOL_MM = 0.1      # local surface tolerance: a fillet 0.5 off, a pocket 0.15 off, a boss outline 0.18 off
LOCAL_MIN_MM2 = 2.0     # smallest blob reported (area of surface off by more than LOCAL_TOL_MM)


def local_findings(e, cfg, pid, fn, mod, rw, ctx=None):
    """reference_cad.local and reference_cad.radii (BLOCKER, shape parts with a frame): the dump-free, feature-level
    comparison. local: every blob of surface > `local_tol_mm` (0.1) off the reference (either way, clustered; a surface
    standing off shows as one "moved" blob) of >= `local_min_mm2` (2) is one difference, wherever it is (mirrored and
    patterned copies included: the whole surface is sampled, not a seed). radii: blend radius per edge sample on both
    meshes (ref_radii), a difference over 0.1 mm (sharp vs R1, R1.5 vs R1, a chamfer the reference lacks) is one
    finding per edge run. A waiver claims one item per kind (claim: the nearest it covers); the rest of its sphere is
    still checked. `local: false` on an entry skips both (a part whose reference is a different revision)."""
    from . import ref_local, ref_radii

    out = []
    if e.get("local") is False:
        return out
    tol = float(e.get("local_tol_mm", cfg.get("local_tol_mm", LOCAL_TOL_MM)))
    amin = float(e.get("local_min_mm2", cfg.get("local_min_mm2", LOCAL_MIN_MM2)))
    try:
        bl = ref_local.local_blobs(mod, rw, tol, amin)
        rd = ref_radii.radius_diffs(ref_radii.radius_pairs(mod, rw))
    except Exception as ex:  # noqa: BLE001 - fail closed
        return [fail("reference_cad.local", G, BLOCKER, "Local comparison crashed", f"`{pid}` vs `{fn}`: {ex}").on(pid)]
    for name, items, fmt, title, fix in (
            ("local", bl, lambda b: f"{b['kind']} {b['area_mm2']} mm2 up to {b['max_mm']} mm at {b['centroid']}",
             "Surface differs locally from the reference", "Each blob is one feature drawn differently: match its section (or waive that feature)."),
            ("radii", [dict(c, kind="radius") for c in rd],
             lambda c: f"R{c['r_ours']} vs reference R{c['r_ref']} ({c['turn']} deg corner, {c['n']} samples) at {c['at']}",
             "Blend radius differs from the reference", "Measure the reference's blend at that edge and use it (0 = sharp).")):
        got, held = claim(items, e)
        opn = [items[i] for i in range(len(items)) if i not in got]
        heldi = {i for i, _ in held}
        msg = (f"`{pid}` vs `{fn}` (tol {tol} mm, >= {amin} mm2): {len(opn)} open, {len(got)} waived"
               + (f" ({len(heldi)} of the open ones lie inside a waiver that already claimed its own feature)" if heldi else "")
               + (": " + "; ".join(fmt(x) for x in opn[:12]) + (" ..." if len(opn) > 12 else "") if opn else "."))
        if ctx is not None:
            ctx.metrics.setdefault(f"reference_cad.{pid}", {})[name] = {"open": len(opn), "waived": len(got), "held": len(heldi),
                                                                       "items": [{k: v for k, v in x.items() if k != "pts"} for x in opn[:40]]}
        out.append(fail(f"reference_cad.{name}", G, BLOCKER, title, msg).on(pid).fix(fix) if opn else
                   ok(f"reference_cad.{name}", G, title.replace("differs", "matches"), msg).on(pid))
    return out
