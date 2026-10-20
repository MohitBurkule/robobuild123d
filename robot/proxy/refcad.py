"""Fast proxy for `reference_cad`: the exact fingerprint checks, then sliced section outlines instead of the boolean diff.

Stands in for reference_cad.diff / .features / .silhouette (each a mesh boolean, a dense surface sampling or a 0.1 mm
raster per part). Both meshes are cut at SLICES planes per axis, spread across the reference's span; any slice where
the outlines differ by more than SECTION_DIFF_MM2 (after removing the discs of the entry's `deviations` spheres), or a
bbox face that moved more than the entry's `dev_tol_mm`, flags the part as `proxy.reference_cad`. The reference side
(sections of the placed STL) is cached to JSON once per file + frame, so a run only slices the model.
Conservative by design: any difference the boolean diff would report crosses at least one slice or moves a bbox face.
"""

from __future__ import annotations

import hashlib
import json
import math
from pathlib import Path

import numpy as np

from shapely import wkb

from ..checks import ref_diff, reference_cad as rc
from ..finding import BLOCKER, fail, ok

G = "proxy"
SLICES = 24  # planes per axis across the reference span
SECTION_DIFF_MM2 = 0.5  # outline difference allowed per slice, after the skin erosion below
DEFAULT_MIN_THICK_MM = 0.3  # reference_cad's diff_min_thick_mm: thinner difference skins are not blobs
DEFAULT_DEV_TOL_MM = 0.5  # same default as reference_cad's dev_tol_mm
CACHE_VERSION = "2"
MIN_RING_MM2 = 1e-4  # ref_features.section drops rings smaller than this


def fast_section(m, ax, h):
    """ref_features.section with the segment geometry built in one vectorised call (same rings, same result)."""
    import shapely
    import trimesh
    from shapely.geometry import Polygon
    from shapely.ops import linemerge, unary_union

    n = np.zeros(3)
    n[ax] = 1.0
    segs = trimesh.intersections.mesh_plane(m, n, n * h)
    if not len(segs):
        return None
    a, b = [i for i in range(3) if i != ax]
    q = np.round(np.asarray(segs, float)[:, :, [a, b]], 3)
    q = q[np.any(q[:, 0] != q[:, 1], axis=1)]
    if not len(q):
        return None
    mg = linemerge(unary_union(shapely.linestrings(q)))
    rings = [g for g in getattr(mg, "geoms", [mg]) if g.is_ring and len(g.coords) > 3]
    out = None
    for p in sorted((Polygon(g).buffer(0) for g in rings), key=lambda p: -p.area):
        if p.area < MIN_RING_MM2:
            continue
        out = p if out is None else out.symmetric_difference(p)
    return out


def model_sections(mod, ax, hs):
    """Sections of the model at heights `hs`, memoised on the mesh content (an unchanged part costs nothing)."""
    from .. import cache

    key = ("proxy_sections", CACHE_VERSION, np.asarray(mod.vertices), np.asarray(mod.faces), ax, np.asarray(hs))
    return [None if x is None else wkb.loads(x) for x in
            cache.memo("proxy_sections", key, lambda: [None if p is None else p.wkb for p in (fast_section(mod, ax, h) for h in hs)])]


def heights(lo, hi, n=SLICES):
    """n plane offsets strictly inside [lo, hi] (cell centres, so no plane sits on a face)."""
    return [lo + (hi - lo) * (k + 0.5) / n for k in range(n)]


def slice_all(mesh, bounds, n=SLICES):
    """{axis: [polygon or None per height]} for the planes spread over `bounds` (2x3)."""
    return {ax: [fast_section(mesh, ax, h) for h in heights(bounds[0][ax], bounds[1][ax], n)] for ax in range(3)}


def _key(path, e, cfg):
    h = hashlib.sha1(Path(path).read_bytes()).hexdigest()
    frame = json.dumps([e.get("ref_to_world", cfg.get("ref_to_world")), e.get("mirror_x"), e.get("ref_shift")], default=str)
    return hashlib.sha1(f"{CACHE_VERSION}|{h}|{frame}|{SLICES}".encode()).hexdigest()[:20]


def ref_signature(path, ref_world, e, cfg, cache_dir):
    """Cached {bounds, sections} of the placed reference; sections as WKB hex (None for an empty cut)."""
    f = Path(cache_dir) / f"refcad_{_key(path, e, cfg)}.json"
    if f.is_file():
        d = json.loads(f.read_text())
    else:
        b = np.asarray(ref_world.bounds, float)
        secs = slice_all(ref_world, b)
        d = {"bounds": b.tolist(), "sections": {str(ax): [p.wkb_hex if p is not None else None for p in v] for ax, v in secs.items()}}
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_text(json.dumps(d))
    return {"bounds": np.asarray(d["bounds"], float),
            "sections": {int(ax): [wkb.loads(x, hex=True) if x else None for x in v] for ax, v in d["sections"].items()}}


def deviation_discs(e, ax, h):
    """The entry's `deviations` spheres cut by plane axis=h: shapely discs in that plane's (a, b) coordinates."""
    from shapely.geometry import Point

    a, b = [i for i in range(3) if i != ax]
    out = []
    for d in e.get("deviations") or []:
        if d.get("near") is None:
            continue
        c, r = np.asarray(d["near"], float), float(d.get("r", 3.0))
        rr = r * r - (c[ax] - h) ** 2
        if rr > 0:
            out.append(Point(c[a], c[b]).buffer(math.sqrt(rr)))
    return out


def section_diff(pm, pr, holes=(), skin=0.0):
    """Area (mm2) of the outline difference of two sections, outside the `holes` (exempt discs), after eroding it by
    `skin` (half the thinnest difference the full diff reports, so tessellation skins drop out)."""
    from shapely.geometry import Polygon

    empty = Polygon()
    d = (pm if pm is not None else empty).symmetric_difference(pr if pr is not None else empty)
    for x in holes:
        d = d.difference(x)
    if skin > 0 and not d.is_empty:
        d = d.buffer(-skin)
    return float(d.area), (d.centroid.coords[0] if not d.is_empty else None)


def compare(mod, sig, e):
    """Differences of the model against a reference signature: [(message, world point)]."""
    out = []
    tol = float(e.get("dev_tol_mm", DEFAULT_DEV_TOL_MM))
    skin = min(tol, float(e.get("diff_min_thick_mm", DEFAULT_MIN_THICK_MM))) / 2
    mb = np.asarray(mod.bounds, float)
    dev = np.abs(mb - sig["bounds"])
    if dev.max() > tol:
        i, ax = np.unravel_index(int(dev.argmax()), dev.shape)
        p = (mb[0] + mb[1]) / 2
        p[ax] = mb[i][ax]
        if not rc._covered(p, e):
            out.append((f"bbox {'min' if i == 0 else 'max'} {'XYZ'[ax]} off by {dev.max():.2f} mm (> {tol})", p.tolist()))
    b = sig["bounds"]
    for ax in range(3):
        hs = heights(b[0][ax], b[1][ax])
        for h, pr, pm in zip(hs, sig["sections"][ax], model_sections(mod, ax, hs)):
            area, c = section_diff(pm, pr, deviation_discs(e, ax, h), skin)
            if area > SECTION_DIFF_MM2:
                out.append((f"section {'XYZ'[ax]}={h:.2f} differs by {area:.2f} mm2", rc._pt3("XYZ"[ax], h, c)))
    return out


def frame_proxy(cache_dir):
    """A `frame_checks` callable for reference_cad.check_entries that runs the cheap proxy."""
    def frame(ctx, e, cfg, pid, fn, mod, ref):
        rw = ref_diff.clean(rc.ref_in_world(ref, e, cfg))
        out = rc.step_placement(e, cfg, pid, mod, rw)
        if e.get("mode", "shape") != "shape":
            return out
        path = Path(getattr(ctx.r.spec, "base_dir", ".") or ".") / (cfg.get("dir") or ".") / fn
        diffs = compare(mod, ref_signature(path, rw, e, cfg, cache_dir), e)
        if diffs:
            msg, at = diffs[0]
            out.append(fail("proxy.reference_cad", G, BLOCKER, "Part likely differs from the reference CAD",
                            f"`{pid}` vs `{fn}`: {len(diffs)} slice/bbox differences, first: {msg}. "
                            f"Others: {[m for m, _ in diffs[1:6]]}").on(pid).here(at)
                       .fix("Run the full `reference_cad` group to see the blobs, or list the change in `deviations`."))
        else:
            out.append(ok("proxy.reference_cad", G, "Sections match the reference CAD",
                          f"`{pid}`: {3 * SLICES} sections and the bbox within tolerance").on(pid))
        return out
    return frame


def run(ctx, parts=None, cache_dir=None):
    from ..geom import cache_dir as default_cache

    cd = Path(cache_dir) if cache_dir else default_cache() / "proxy"
    return rc.check_entries(ctx, frame_proxy(cd), exact=False, parts=parts)
