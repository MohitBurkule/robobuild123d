"""Feature-by-feature diagnosis of a hand-built part against the designer's SolidWorks feature tree (v2 dump).

    python -m robot.cad.dump_misses tub "RV01 Chassis" RV01_Chassis_1.stl robots/revron/step/tub.step out.json

The dump is ground truth for DIAGNOSIS only: nothing here builds geometry for the model. For every solid feature
(boss, cut, revolve, fillet, chamfer, pattern, mirror) the faces it owns in the final body (dump v2 FACE lines) are
sampled, mapped into our world frame (asmdump placement + ICP, as robot.checks.sldprt_dump does) and measured against
  ref   the reference STL (a sample the STL does not show was changed by a later feature: not compared), and
  ours  our part's surface.
Each feature gets a status (present / wrong / missing) with the numbers, a cause category, whether our existing checks
(dump.fillet / dump.hole / dump.extrude, reference_cad.diff at the entry's tol_mm and deviations) flag it, and the
process fix that would let a designer without the dump get it right. Our surface far from any reference surface is
reported as extra geometry (invented / patch). Pure measurement; the categories are heuristics, read the numbers.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

from ..checks import sldprt_dump as sd
from ..checks.asm_dump import DEFAULT_FILE, world_of

TOL = 0.05          # mm: surface counts as matching
NEAR = 1.0          # mm: beyond this the feature is not there at all
SHARP = np.sqrt(2) - 1   # gap at the middle of a fillet face when the edge was left sharp, per mm of radius
SOLID = {"Extrusion", "ICE", "Cut", "Revolution", "RevCut", "Fillet", "Chamfer", "CirPattern", "LPattern",
         "MirrorPattern", "Boss", "Thicken"}

FIX = {
    "fillet skipped": "tool: fillet/chamfer radius finder on STEP sections (fit arcs at every concave/convex corner, "
                      "report r and the edge chain); check: dump-free `visual.fillet_ref` must list every arc it finds",
    "fillet wrong radius": "tool: same radius finder, snapped to catalog radii (0.5/1/1.5/2/3/5/8); guide: read r from "
                           "a section perpendicular to the edge, never from the outline",
    "chamfer wrong size": "tool: chamfer finder reporting both legs (D1, angle) from STEP sections; check: dump-free "
                          "bevel-width parity in sections",
    "chamfer skipped": "tool: chamfer finder (45 deg facets in STEP sections); check: sharp convex edge where the "
                       "reference has a planar bevel",
    "wrong depth / end condition": "guide: dimension depths from the face the designer stops at (up-to surface, "
                                   "mid-plane) not from a measured Z; check: per-face plane offset vs the reference "
                                   "(planar-face histogram) at tol 0.05",
    "misread section": "tool: sketch extractor that slices the STEP normal to each extrude axis and fits lines/arcs "
                       "with relations; guide: build each profile from its own section, one feature per region",
    "wrong place": "guide: place features from datums (wall faces, axes) with named relations, not mesh coordinates; "
                   "check: per-feature face offset map (not one global IoU)",
    "feature missing": "check: per-region missing-volume clusters at 0.1 mm3 instead of tol 1.0 mm / 25 % volume; "
                       "guide: enumerate every face of the reference before modelling",
    "pattern copy missing": "guide: model patterns/mirrors as patterns of the seed feature (one call), never as copies",
    "waived": "review the deviation: a waiver hides the miss from every check",
}


def _mesh_of(path):
    import trimesh
    if str(path).lower().endswith((".step", ".stp")):
        import tempfile
        from build123d import export_stl, import_step
        tmp = Path(tempfile.mkdtemp()) / "m.stl"
        export_stl(import_step(str(path)), str(tmp), tolerance=0.01, angular_tolerance=0.1)
        path = tmp
    return trimesh.load(str(path), force="mesh")


def frame(name, stl, e, cfg, root=sd.DEFAULT_ROOT):
    """(dump, faces, 4x4 part mm -> world, registration gap mm, reference mesh in world)."""
    import trimesh
    from ..checks.reference_cad import ref_in_world
    dump, faces = sd._load(str(root), name)
    refm = trimesh.load(str(Path(cfg["dir"]) / stl), force="mesh")
    A, rms = sd.register(sd.part_vertices(faces), refm, sd.asm_starts(DEFAULT_FILE, name, stl))
    return dump, faces, world_of(e, cfg) @ A, rms, ref_in_world(refm, e, cfg)


def blend_size(f):
    if f["type"] == "Fillet" and f.get("fillet"):
        return f["fillet"].get("r", 0) * 1e3
    d = [v for k, v in f["dims"].items() if k.startswith("D1@")]
    return d[0] * 1e3 if d else None


def classify(f, faces, gr, gm, size=None):
    """status, category, numbers for one feature from per-face sample gaps (lists of arrays)."""
    shown = [(fc, a[a <= TOL + 0.03], b[a <= TOL + 0.03]) for fc, a, b in zip(faces, gr, gm)]
    shown = [(fc, a, b) for fc, a, b in shown if len(b)]
    if not shown:
        return "not shown", None, "reference STL does not show its faces (later feature)"
    allm = np.concatenate([b for _, _, b in shown])
    med, mx = float(np.median(allm)), float(allm.max())
    num = f"ours median {med:.3f} / max {mx:.3f} mm on {len(shown)}/{len(faces)} faces"
    if mx <= TOL + 0.03 or np.quantile(allm, 0.9) <= TOL:
        return "present", None, num
    t = f["type"]
    if t in ("Fillet", "Chamfer") and size:
        rel = med / size
        if t == "Chamfer":
            cat = "chamfer skipped" if med > 0.2 * size else "chamfer wrong size"
        else:
            cat = "fillet skipped" if abs(rel - SHARP) < 0.15 or med > 0.3 * size else "fillet wrong radius"
        return ("missing" if cat.endswith("skipped") else "wrong"), cat, num + f" (r {size:g}; sharp edge gives {SHARP * size:.3f})"
    if t in ("CirPattern", "LPattern", "MirrorPattern"):
        return ("missing" if med > NEAR else "wrong"), "pattern copy missing" if med > NEAR else "wrong place", num
    if med > NEAR:
        return "missing", "feature missing", num
    caps, sides = [], []
    nrm = feature_normal(f)
    for fc, _a, b in shown:
        is_cap = nrm is not None and fc["type"] == "plane" and abs(abs(fc["n"] @ nrm) / np.linalg.norm(fc["n"]) - 1) < 1e-4
        (caps if is_cap else sides).append(float(np.median(b)))
    if caps and max(caps) > TOL and (not sides or max(sides) <= max(caps)):
        return "wrong", "wrong depth / end condition", num + f"; worst cap off {max(caps):.3f}"
    if sides and max(sides) > 0.3:
        return "wrong", "misread section", num + f"; worst side wall off {max(sides):.3f}"
    return "wrong", "wrong place", num


SKETCHES = {}


def feature_normal(f):
    sk = SKETCHES.get(f["name"])
    if sk is None:
        return None
    xf = sk["xf"]
    return np.array(xf[6:9], float)


def analyse(dump, faces, M, ref, ours, e, root=sd.DEFAULT_ROOT):
    from ..checks.reference_cad import _covered
    by = {f["name"]: f for f in dump["features"]}
    SKETCHES.clear()
    for f in dump["features"]:
        for p in f["parents"]:
            if by.get(p, {}).get("sketch", {}).get("xf"):
                SKETCHES.setdefault(f["name"], by[p]["sketch"])
    X = lambda p: np.atleast_2d(p) @ M[:3, :3].T + M[:3, 3]
    groups = []
    for f in dump["features"]:
        if f["suppressed"] or f["type"] not in SOLID or f["n"] < 0:
            continue
        fcs, pts = [], []
        for fc in f.get("faces") or []:
            sp = sd.face_samples(fc)
            if sp is not None:
                fcs.append(fc); pts.append(X(sp))
        groups.append((f, fcs, pts))
    allp = np.vstack([p for _, _, ps in groups for p in ps]) if groups else np.zeros((0, 3))
    GR = sd.surface_gap(ref, allp, near=2.0)
    GM = sd.surface_gap(ours, allp, near=5.0)
    dumprows = sd.compare(ours, ref, sd.features_in_frame(dump, faces, M, sd.part_vertices(faces)))
    flagged = {}
    for r in dumprows:
        if r.get("ok") is False:
            flagged.setdefault(r["feature"] if isinstance(r["feature"], str) else r["feature"].get("feature"), set()).add("dump." + r["kind"])
    rows, k = [], 0
    tol = float(e.get("tol_mm", 0.5))
    for f, fcs, pts in groups:
        gr, gm = [], []
        for p in pts:
            gr.append(GR[k:k + len(p)]); gm.append(GM[k:k + len(p)]); k += len(p)
        size = blend_size(f) if f["type"] in ("Fillet", "Chamfer") else None
        st, cat, num = classify(f, fcs, gr, gm, size)
        at = None
        if pts:
            P = np.vstack(pts); G = np.concatenate(gm); live = np.concatenate(gr) <= TOL + 0.03
            if live.any():
                at = P[live][int(np.argmax(G[live]))]
        caught = sorted(flagged.get(f["name"], set()))
        why = _covered(at, e) if at is not None and st in ("wrong", "missing") else None
        if why:
            cat = "waived"
        if st in ("wrong", "missing") and at is not None and not why:
            worst = float(np.concatenate(gm)[np.concatenate(gr) <= TOL + 0.03].max())
            if worst > tol:
                caught.append(f"reference_cad.diff(>{tol:g})")
        dims = {k2.split("@")[0]: round(v * 1e3, 3) if "D" in k2 else v for k2, v in f["dims"].items() if k2.split("@")[1:2] == [f["name"]]}
        rows.append(dict(feature=f["name"], type=f["type"], dims=dims, status=st, category=cat, numbers=num,
                         at=None if at is None else np.round(at, 2).tolist(), caught=caught, waiver=why,
                         fix=FIX.get(cat) if cat else None))
    return rows


def extra_geometry(ours, ref, M, faces, e=None, n=40000, gap=0.3):
    """Clusters of our surface farther than `gap` from the reference: (centroid, bbox, area mm2, max gap)."""
    import trimesh
    from scipy.sparse.csgraph import connected_components
    from scipy.spatial import cKDTree
    P, _ = trimesh.sample.sample_surface(ours, n, seed=2)
    d = sd.surface_gap(ref, P, near=gap)
    far = d > gap
    Q, dq = P[far], d[far]
    if not len(Q):
        return []
    A = cKDTree(Q).sparse_distance_matrix(cKDTree(Q), 1.5)
    nc, lab = connected_components(A, directed=False)
    da = ours.area / n
    out = []
    for c in range(nc):
        m = lab == c
        if m.sum() < 5:
            continue
        q = Q[m]
        from ..checks.reference_cad import _covered
        why = _covered(q.mean(0), e, (q.min(0), q.max(0))) if e else None
        cc = q.mean(0)
        dd = [(float(np.min(np.linalg.norm((np.atleast_2d(sp) @ M[:3, :3].T + M[:3, 3]) - cc, axis=1))), f["name"])
              for f, fc in faces if not f["suppressed"] for sp in [sd.face_samples(fc)] if sp is not None]
        out.append(dict(waiver=why, near_feature=min(dd)[1] if dd else None, centroid=np.round(q.mean(0), 2).tolist(), lo=np.round(q.min(0), 2).tolist(),
                        hi=np.round(q.max(0), 2).tolist(), area_mm2=round(float(m.sum() * da), 2),
                        max_gap=round(float(dq[m].max()), 3)))
    return sorted(out, key=lambda x: -x["area_mm2"])


def run(pid, name, stl, ours_path, spec_path="robots/revron/spec.json", out=None):
    spec = json.loads(Path(spec_path).read_text())
    cfg = spec["reference_cad"]
    e = next((x for x in cfg["parts"] if x.get("part") == pid), None) or {"part": pid, "file": stl}
    e = dict(e, file=stl)
    dump, faces, M, rms, ref = frame(name, stl, e, cfg)
    ours = _mesh_of(ours_path)
    res = dict(part=pid, dump=name, stl=stl, reg_gap_mm=round(rms, 4), tol_mm=e.get("tol_mm"),
               vol_ours=round(float(ours.volume), 1), vol_ref=round(float(ref.volume), 1),
               rows=analyse(dump, faces, M, ref, ours, e), extra=extra_geometry(ours, ref, M, faces, e))
    if out:
        Path(out).write_text(json.dumps(res, indent=1, default=float))
    return res


if __name__ == "__main__":
    a = sys.argv[1:]
    r = run(a[0], a[1], a[2], a[3], out=a[4] if len(a) > 4 else None)
    for x in r["rows"]:
        print(f"{x['feature']:<18} {x['type']:<13} {x['status']:<9} {str(x['category']):<28} {x['numbers']} {x['caught']}")
    print("extra:", r["extra"][:12])
