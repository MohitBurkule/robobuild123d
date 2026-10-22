"""`python3 -m robot measure-ref <stl|step> [--part NAME] [--fit] [--md]`: numbers to type into params, never geometry.

WHY: modelling from a reference went wrong two ways: guessing dimensions from renders (wrong hole sizes, missing
countersinks, wrong wall thickness), or importing the mesh (a copy, which `reference_cad.copied` rejects). This tool
prints only measurements: bounding box, section dimensions at N heights per axis, holes (diameter, shape round/D/
hex/slot, axis, countersink angle + diameter, counterbore), wall thickness statistics and fillet radius estimates.
With --fit it adds low-DOF B-spline sketches (<= 8 control points) of the top/side/front outlines and of chosen
sections, plus straight/arc segment lists, for robot.cad.smooth to loft. No polygons, no meshes, no vertex lists.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np

AXES = "xyz"


def load_mesh(path, part=None):
    import trimesh

    path = Path(path)
    if path.suffix.lower() in (".step", ".stp"):
        import build123d as bd

        from ..geom import FINE, tessellate

        shp = bd.import_step(str(path))
        if part:
            hits = [c for c in getattr(shp, "children", []) or [] if (getattr(c, "label", "") or "") == part]
            if not hits:
                hits = [s for s in shp.solids() if (getattr(s, "label", "") or "") == part]
            if not hits:
                raise SystemExit(f"no part labelled `{part}` in {path}")
            shp = hits[0]
        V, F = tessellate(shp, FINE)
        return trimesh.Trimesh(V, F)
    m = trimesh.load(str(path), force="mesh")
    return m


def _r(x, n=2):
    return round(float(x), n)


def sections(m, n=3):
    from ..checks.ref_features import holes, section

    out = {}
    lo, hi = m.bounds
    for ax in range(3):
        rows = []
        u, v = [AXES[i] for i in range(3) if i != ax]
        for k in range(1, n + 1):
            h = lo[ax] + (hi[ax] - lo[ax]) * k / (n + 1)
            g = section(m, ax, h)
            if g is None or g.is_empty:
                rows.append({"at": _r(h), "empty": True})
                continue
            b = g.bounds
            hs = holes(g)
            rows.append({"at": _r(h), f"{u}_min": _r(b[0]), f"{u}_max": _r(b[2]), f"{v}_min": _r(b[1]), f"{v}_max": _r(b[3]),
                         f"size_{u}": _r(b[2] - b[0]), f"size_{v}": _r(b[3] - b[1]), "area_mm2": _r(g.area, 1),
                         "regions": len(getattr(g, "geoms", [g])), "holes": len(hs)})
        out[AXES[ax]] = rows
    return out


def _csk_from_profile(heights, dias):
    """(angle deg, max dia, depth) from a falling diameter profile; None if not tapered."""
    H = np.array([h for h, d in zip(heights, dias) if d])
    D = np.array([d for d in dias if d])
    if len(D) < 3:
        return None
    big = D > D.min() * 1.15
    if big.sum() < 2:
        return None
    hh, dd = H[big], D[big]
    slope = abs(np.polyfit(hh, dd, 1)[0])  # d(diameter)/dh
    ang = 2 * math.degrees(math.atan(slope / 2))
    depth = abs(hh.max() - hh.min()) + abs(H[1] - H[0])
    return _r(ang, 1), _r(D.max()), _r(depth)


def find_holes(m, per_axis=5):
    """Holes seen in sections along each axis, de-duplicated by centre; profile along the axis gives csk/cbore."""
    from ..checks.ref_features import hole_kind, holes, section

    lo, hi = m.bounds
    found = []
    for ax in range(3):
        a, b = [i for i in range(3) if i != ax]
        seen = []
        for k in range(1, per_axis + 1):
            h = lo[ax] + (hi[ax] - lo[ax]) * k / (per_axis + 1)
            for c, dia, shape in holes(section(m, ax, h)):
                hit = next((s for s in seen if math.dist(c, s[0]) < max(0.5, 0.3 * min(dia, s[1]))), None)
                if hit is not None:
                    hit[3].add(shape)
                    continue
                seen.append((c, dia, shape, {shape}))
        for c, dia, shape, shapes in seen:
            hs = np.linspace(lo[ax] + 0.05, hi[ax] - 0.05, 25)
            prof = []
            for h in hs:
                d = None
                for c2, d2, _ in holes(section(m, ax, h)):
                    if math.dist(c, c2) < max(0.6, 0.3 * dia):
                        d = d2
                        break
                prof.append(d)
            ext = [h for h, d in zip(hs, prof) if d]
            centre = [0.0, 0.0, 0.0]
            centre[a], centre[b] = c
            centre[ax] = (min(ext) + max(ext)) / 2 if ext else 0.0
            row = {"axis": AXES[ax], "centre": [_r(x) for x in centre], "diameter": _r(min(d for d in prof if d) if ext else dia),
                   "shape": shape, "depth": _r(max(ext) - min(ext) + (hs[1] - hs[0])) if ext else None,
                   "through": bool(ext and min(ext) <= hs[1] and max(ext) >= hs[-2])}
            if len(shapes) > 1:
                row["shapes_along_axis"] = sorted(shapes)  # e.g. round bore + hex nut pocket
            kind = hole_kind(prof)
            row["profile"] = kind
            if kind == "csk":
                ck = _csk_from_profile(hs, prof)
                if ck:
                    row["csk_angle_deg"], row["csk_dia"], row["csk_depth"] = ck
            elif kind == "cbore":
                ds = [d for d in prof if d]
                row["cbore_dia"] = _r(max(ds))
                row["cbore_depth"] = _r(sum(1 for d in ds if d > min(ds) * 1.2) * (hs[1] - hs[0]))
            found.append(row)
    return found


def wall_thickness(m, n=1500, seed=0):
    """Inward ray thickness from surface samples: min, p5, median, p95 (mm)."""
    import trimesh

    pts, fi = trimesh.sample.sample_surface(m, n, seed=seed)
    nrm = m.face_normals[fi]
    origins = pts - nrm * 1e-3
    loc, ri, _ = m.ray.intersects_location(origins, -nrm, multiple_hits=False)
    if not len(ri):
        return {}
    t = np.linalg.norm(loc - origins[ri], axis=1)
    t = t[t > 0.05]
    if not len(t):
        return {}
    return {"samples": int(len(t)), "min": _r(t.min()), "p5": _r(np.percentile(t, 5)), "median": _r(np.median(t)),
            "p95": _r(np.percentile(t, 95))}


def fillets(m):
    """Fillet radius estimates from the outlines of mid sections on each axis (arcs between two straight runs)."""
    from ..checks.ref_features import section
    from .fit import fillet_radii

    lo, hi = m.bounds
    out = {}
    for ax in range(3):
        g = section(m, ax, (lo[ax] + hi[ax]) / 2)
        rs = []
        for p in getattr(g, "geoms", [g]) if g is not None else []:
            if hasattr(p, "exterior"):
                rs += fillet_radii(np.array(p.exterior.coords))
        out[AXES[ax]] = sorted({_r(r, 1) for r in rs if 0.2 < r < 50})
    return out


def _outline(m, ax):
    """Silhouette along an axis as a shapely polygon (largest piece)."""
    from shapely.geometry import Polygon
    from shapely.ops import unary_union

    a, b = [i for i in range(3) if i != ax]
    tris = m.triangles[:, :, [a, b]]
    polys = [Polygon(t) for t in tris if abs((t[1, 0] - t[0, 0]) * (t[2, 1] - t[0, 1]) - (t[1, 1] - t[0, 1]) * (t[2, 0] - t[0, 0])) > 1e-9]
    u = unary_union([p.buffer(1e-4) for p in polys])
    return max(getattr(u, "geoms", [u]), key=lambda p: p.area)


def fit_profiles(m, stations=None, max_ctrl=8, rms_target=0.3):
    """Low-DOF B-spline sketches of the three view outlines and of the given section stations."""
    from ..checks.ref_features import section
    from .fit import fit_bspline, segments

    def sketch(poly):
        P = np.array(poly.exterior.coords)
        f = fit_bspline(P, True, max_ctrl, rms_target)
        segs = segments(P)
        return {"ctrl": f["ctrl"], "n_ctrl": f["n_ctrl"], "rms": f["rms"], "max_err": f["max_err"],
                "segments": [{k: v for k, v in s.items() if k != "center"} for s in segs][:24]}

    out = {"views": {}, "sections": []}
    for name, ax in (("top", 2), ("front", 1), ("side", 0)):
        out["views"][name] = sketch(_outline(m, ax))
    for ax_name, h in stations or []:
        ax = AXES.index(ax_name)
        g = section(m, ax, h)
        if g is None or g.is_empty:
            out["sections"].append({"axis": ax_name, "at": h, "empty": True})
            continue
        p = max(getattr(g, "geoms", [g]), key=lambda q: q.area)
        out["sections"].append({"axis": ax_name, "at": h, **sketch(p)})
    return out


def measure(path, part=None, n_sections=3, fit=False, stations=None) -> dict:
    m = load_mesh(path, part)
    lo, hi = m.bounds
    out = {"file": Path(path).name, "part": part, "units": "mm",
           "bbox": {"min": [_r(x) for x in lo], "max": [_r(x) for x in hi], "size": [_r(x) for x in hi - lo]},
           "volume_mm3": _r(abs(m.volume), 1) if m.is_watertight else None,
           "sections": sections(m, n_sections), "holes": find_holes(m), "wall_thickness": wall_thickness(m),
           "fillet_radii": fillets(m)}
    if fit:
        out["fit"] = fit_profiles(m, stations)
    return out


def to_markdown(d) -> str:
    L = [f"# {d['file']}" + (f" / {d['part']}" if d.get("part") else ""), "",
         f"bbox size {d['bbox']['size']} (min {d['bbox']['min']}, max {d['bbox']['max']}), volume {d['volume_mm3']} mm3", ""]
    for ax, rows in d["sections"].items():
        L.append(f"## sections along {ax}")
        for r in rows:
            L.append("- " + ", ".join(f"{k} {v}" for k, v in r.items()))
        L.append("")
    L.append("## holes")
    for h in d["holes"]:
        L.append("- " + ", ".join(f"{k} {v}" for k, v in h.items()))
    L += ["", f"## wall thickness {d['wall_thickness']}", f"## fillet radii {d['fillet_radii']}"]
    if "fit" in d:
        L.append("## fitted sketches (B-spline control points, <= 8 per outline)")
        for k, v in d["fit"]["views"].items():
            L.append(f"- {k}: ctrl {v['ctrl']} (rms {v['rms']}, max {v['max_err']})")
        for s in d["fit"]["sections"]:
            L.append(f"- section {s['axis']}={s['at']}: " + (f"ctrl {s['ctrl']} (rms {s['rms']})" if "ctrl" in s else "empty"))
    return "\n".join(L)


def check_no_geometry(d, max_list=8) -> None:
    """Guard: the output must hold no point list longer than `max_list` (no polygons or meshes)."""
    def walk(x, path):
        if isinstance(x, list):
            if len(x) > max_list and x and isinstance(x[0], list) and x[0] and isinstance(x[0][0], (int, float)):
                raise AssertionError(f"{path} is a point list of {len(x)}: measure-ref must not output geometry")
            for i, y in enumerate(x):
                walk(y, f"{path}[{i}]")
        elif isinstance(x, dict):
            for k, y in x.items():
                walk(y, f"{path}.{k}")
    walk(d, "$")


def cli(a):
    st = []
    for s in (a.stations or "").split(";"):
        if ":" in s:
            ax, hs = s.split(":", 1)
            st += [(ax.strip(), float(h)) for h in hs.split(",") if h.strip()]
    d = measure(a.file, a.part, a.sections, a.fit or bool(st), st)
    check_no_geometry(d)
    print(to_markdown(d) if a.md else json.dumps(d, indent=1))
    return 0


def add_cli(sub):
    p = sub.add_parser("measure-ref", help="measure a reference STL/STEP: numbers only (bbox, sections, holes, walls, fillets)")
    p.add_argument("file")
    p.add_argument("--part", help="STEP: the labelled child to measure")
    p.add_argument("--sections", type=int, default=3, help="sections per axis (default 3)")
    p.add_argument("--fit", action="store_true", help="add low-DOF B-spline sketches of view outlines and stations")
    p.add_argument("--stations", help='section stations to fit, e.g. "z:2,5,8;x:0"')
    p.add_argument("--md", action="store_true", help="markdown instead of JSON")
    p.set_defaults(func=cli)
