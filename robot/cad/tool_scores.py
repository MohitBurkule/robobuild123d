"""Score blend_finder / sketch_extract against the SolidWorks dumps. The dump is read HERE only, to grade the tools;
the tools themselves see nothing but the reference solid.

    python -m robot.cad.tool_scores "RV01 Chassis" RV01_Chassis_1 [out.json]

blend recall : dump fillet / chamfer faces (own + pattern copies) that the reference solid shows, matched by a found
               blend face of the same kind and size (|size - dumped| <= RES) within 0.05 mm.
radius recall: distinct dumped (kind, size) values found anywhere on the part.
dim recall   : dumped sketch dims (mm, or deg for angles) of every sketch used by a solid feature, found (+-0.01 mm /
               0.05 deg) among the dims of the sections the extractor proposes with the sketch's normal.
dims_oracle_plane: the same, sectioning at the dumped sketch plane (scores the extractor apart from plane choice).
chance       : the same dim recall for the dumped values shifted by +0.37 (an estimate of accidental matches).
"""
from __future__ import annotations

import json
import math
import sys
from pathlib import Path

import numpy as np

from ..checks import sldprt_dump as sd
from ..checks.asm_dump import DEFAULT_FILE
from . import blend_finder as bf
from . import sketch_extract as se

STEP = "/mnt/project-files/robot-cad/research/rvrn_step/rvrn_2.0.step"
INDEX = "/mnt/project-files/robot-cad/research/rvrn_step/INDEX.txt"
STL_DIR = "/mnt/project-files/robot-cad/research/rvrn_step/parts"


def ref_solid(stem):
    from build123d import import_step
    names = [l.split()[0] for l in Path(INDEX).read_text().splitlines() if l.strip()]
    return import_step(STEP).solids()[names.index(stem)]


def part_to_asm(name, stem):
    import trimesh
    dump, faces = sd._load(sd.DEFAULT_ROOT, name)
    refm = trimesh.load(f"{STL_DIR}/{stem}.stl", force="mesh")
    A, rms = sd.register(sd.part_vertices(faces), refm, sd.asm_starts(DEFAULT_FILE, name, f"{stem}.stl"))
    return dump, faces, A, rms


def dumped_blends(dump, faces):
    size = {}
    for f in dump["features"]:
        if f["suppressed"]:
            continue
        if f["type"] == "Fillet" and (f.get("fillet") or {}).get("r"):
            size[f["name"]] = ("fillet", f["fillet"]["r"] * 1e3)
        elif f["type"] == "Chamfer":
            d = [v for k, v in f["dims"].items() if k.startswith("D1@")]
            if d: size[f["name"]] = ("chamfer", d[0] * 1e3)
    out = []
    for f, fc in faces:
        if f["suppressed"]:
            continue
        src = f["name"] if f["name"] in size else next((p for p in f["parents"] if p in size), None) if f["type"] in ("CirPattern", "LPattern", "MirrorPattern") else None
        if src is None:
            continue
        kind, s = size[src]
        if kind == "fillet" and (fc["type"] not in ("cyl", "torus") or (fc["type"] == "cyl" and abs(fc["r"] * 1e3 - s) > 1e-3)):
            continue
        if kind == "chamfer" and fc["type"] not in ("plane", "cone"):
            continue
        out.append((src, kind, s, fc))
    return out


def _dist(face, p):
    from OCP.BRepBuilderAPI import BRepBuilderAPI_MakeVertex
    from OCP.BRepExtrema import BRepExtrema_DistShapeShape
    from OCP.gp import gp_Pnt
    d = BRepExtrema_DistShapeShape(BRepBuilderAPI_MakeVertex(gp_Pnt(*map(float, p))).Vertex(), face.wrapped)
    return d.Value() if d.IsDone() else math.inf


def score_blends(solid, blends, dump, faces, A):
    X = lambda p: np.atleast_2d(p) @ A[:3, :3].T + A[:3, 3]
    want = dumped_blends(dump, faces)
    found = [(b.kind, b.size, f) for b in blends for f in b.faces]
    hit = shown = 0
    misses = []
    for src, kind, s, fc in want:
        sp = sd.face_samples(fc)
        if sp is None:
            continue
        p = X(sp).mean(0) if fc["type"] == "plane" else X(sp)[0]
        if _dist(solid, p) > 0.05:
            continue
        shown += 1
        near = [(k, z) for k, z, f in found if _dist(f, p) < 0.05]
        ok = any(k == kind and abs(z - s) <= bf.RES + 1e-6 for k, z in near)
        hit += ok
        if not ok:
            misses.append(dict(feature=src, kind=kind, size=round(s, 3), at=np.round(p, 2).tolist(), found=[(k, z) for k, z in near]))
    want_sizes = {(k, round(s, 2)) for _s, k, s, _f in want}
    got_sizes = {(b.kind, round(b.size, 2)) for b in blends}
    return dict(faces_shown=shown, faces_hit=hit, recall=round(hit / max(shown, 1), 3),
                sizes_dumped=sorted(want_sizes), sizes_found=sorted(got_sizes),
                size_recall=round(len(want_sizes & got_sizes) / max(len(want_sizes), 1), 3), misses=misses)


def dumped_sketch_dims(dump, A):
    """[(sketch, dim, value mm|deg, normal in asm frame)] for sketches used by solid features."""
    by = {f["name"]: f for f in dump["features"]}
    used = {p for f in dump["features"] if not f["suppressed"] and f["type"] not in ("ProfileFeature",) for p in f["parents"]}
    out = []
    for name in used:
        f = by.get(name)
        if not f or f["type"] != "ProfileFeature" or not f.get("sketch", {}).get("xf"):
            continue
        n = A[:3, :3] @ np.array(f["sketch"]["xf"][6:9])
        o = A[:3, :3] @ (np.array(f["sketch"]["xf"][9:12]) * 1e3) + A[:3, 3]
        for k, v in f["dims"].items():
            if k.split("@")[1:2] != [name] or abs(v) < 1e-9:   # a zero dim matches anything: not scored
                continue
            ang = abs(v) > 0.2          # SW stores lengths in m (parts < 0.2 m) and angles in rad
            out.append((name, k, math.degrees(v) if ang else v * 1e3, n, ang, float(o @ n)))
    return out


def score_dims(solid, dump, A, shift=0.0, tol=1e-3, tol_deg=0.01, oracle=False):
    """Each dumped dim is looked up in the four proposed sections (same normal) nearest its sketch plane, two each side."""
    want = dumped_sketch_dims(dump, A)
    planes = se.section_planes(solid, max_levels=1000, skin=0.02)
    cache, hit, rows = {}, 0, []
    for sk, k, v, n, ang, lvl in want:
        nn = n / np.linalg.norm(n)
        cand = [(float(o @ nn), o, m) for o, m in planes if abs(abs(m @ nn) - 1) < 1e-4]
        if oracle:   # extractor quality alone: section at the dumped sketch plane (+-0.02, +-0.5 into the feature)
            cand = [(lvl + d, nn * (lvl + d), nn) for d in (-0.5, -0.02, 0.02, 0.5)]
        below = sorted((c for c in cand if c[0] <= lvl), key=lambda c: -c[0])[:2]
        above = sorted((c for c in cand if c[0] > lvl), key=lambda c: c[0])[:2]
        vals = []
        for c in below + above:
            if c is None:
                continue
            key = (round(c[0], 4), tuple(np.round(c[2], 4)))
            if key not in cache:
                try:
                    cache[key] = list(se.extract(solid, c[1], c[2]).dims.values())
                except Exception:
                    cache[key] = []
            vals += cache[key]
        vals = np.array(vals)
        t = v + shift
        alt = [t, 180 - t, 90 - t] if ang else [t]
        ok = bool(len(vals)) and any(np.any(np.abs(vals - x) <= (tol_deg if ang else tol)) for x in alt)
        hit += ok
        rows.append(dict(sketch=sk, dim=k.split("@")[0], value=round(v, 4), angle=ang, found=ok, n_candidates=len(vals)))
    return dict(dims=len(want), hit=hit, recall=round(hit / max(len(want), 1), 3), rows=rows)


def _near_sections(solid, planes, n, lvl, cache):
    nn = n / np.linalg.norm(n)
    cand = [(float(o @ nn), o, m) for o, m in planes if abs(abs(m @ nn) - 1) < 1e-4]
    pick = sorted((c for c in cand if c[0] <= lvl), key=lambda c: -c[0])[:2] + sorted((c for c in cand if c[0] > lvl), key=lambda c: c[0])[:2]
    out = []
    for c in pick:
        key = (round(c[0], 4), tuple(np.round(c[2], 4)))
        if key not in cache:
            try:
                cache[key] = se.extract(solid, c[1], c[2])
            except Exception:
                cache[key] = None
        if cache[key] is not None:
            out.append(cache[key])
    return out


def score_entities(solid, dump, A, tol=1e-3):
    """Sketch lines / arcs that survive on the reference surface, matched by an extracted entity of the same kind and
    length / radius in the sections nearest the sketch plane (the extractor's geometric recall, independent of how
    the designer dimensioned it)."""
    from build123d import Compound, Vector
    skin = Compound(solid.faces())
    planes = se.section_planes(solid, max_levels=1000, skin=0.02)
    by = {f["name"]: f for f in dump["features"]}
    used = {p for f in dump["features"] if not f["suppressed"] and f["type"] != "ProfileFeature" for p in f["parents"]}
    cache, total, hit, miss = {}, 0, 0, []
    for name in sorted(used):
        f = by.get(name)
        if not f or f["type"] != "ProfileFeature" or not f.get("sketch", {}).get("xf"):
            continue
        xf = np.array(f["sketch"]["xf"]); R = xf[0:9].reshape(3, 3); t = xf[9:12] * 1e3
        X = lambda q: A[:3, :3] @ (np.asarray(q) * 1e3 @ R + t) + A[:3, 3]
        n = A[:3, :3] @ R[2]
        lvl = float(X((0, 0, 0)) @ (n / np.linalg.norm(n)))
        secs = None
        for sg in f["sketch"]["segs"]:
            if sg.get("constr") or sg.get("type") not in (0, 1) or "p0" not in sg:
                continue
            p0, p1 = np.array(sg["p0"]), np.array(sg["p1"])
            mid = (p0 + p1) / 2 if sg["type"] == 0 else (p0 if np.allclose(p0, p1) else None)
            if mid is None:
                c = np.array(sg["c"]); w = (p0 + p1) / 2 - c
                mid = c + w / max(np.linalg.norm(w), 1e-12) * sg["r"] * (1 if np.linalg.norm(w) > 1e-9 else 0)
            probe = [mid] + ([p0 * 0.8 + p1 * 0.2, p0 * 0.2 + p1 * 0.8] if sg["type"] == 0 else [])
            if any(skin.distance_to(Vector(*X(q))) > 0.01 for q in probe):
                continue                                   # (partly) consumed by a later feature
            total += 1
            secs = secs if secs is not None else _near_sections(solid, planes, n, lvl, cache)
            if sg["type"] == 0:
                L = float(np.linalg.norm(p1 - p0)) * 1e3
                ok = any(abs(v - L) <= tol for S in secs for k, v in S.dims.items() if k.endswith((".len", ".len_sharp", ".span")))
            else:
                ok = any(abs(a[1] - sg["r"] * 1e3) <= tol for S in secs for a in S.arcs.values())
            hit += ok
            if not ok:
                miss.append(dict(sketch=name, seg=sg["id"], kind="line" if sg["type"] == 0 else "arc",
                                 size=round(L if sg["type"] == 0 else sg["r"] * 1e3, 4), at=np.round(X(mid), 2).tolist(), sections=len(secs)))
    return dict(entities_surviving=total, hit=hit, recall=round(hit / max(total, 1), 3), misses=miss)


def run(name, stem, out=None):
    solid = ref_solid(stem)
    dump, faces, A, rms = part_to_asm(name, stem)
    blends = bf.find(solid)
    res = dict(part=name, reg_gap_mm=round(rms, 4), blends=score_blends(solid, blends, dump, faces, A),
               dims=score_dims(solid, dump, A), chance=score_dims(solid, dump, A, shift=0.37)["recall"],
               dims_oracle_plane=score_dims(solid, dump, A, oracle=True), entities=score_entities(solid, dump, A))
    if out:
        Path(out).write_text(json.dumps(res, indent=1, default=float))
    return res


if __name__ == "__main__":
    r = run(*sys.argv[1:4])
    b, d = r["blends"], r["dims"]
    print(f"{r['part']}: blend faces {b['faces_hit']}/{b['faces_shown']} ({b['recall']}), sizes {b['size_recall']}; "
          f"dims {d['hit']}/{d['dims']} ({d['recall']}), chance {r['chance']}; at the sketch plane {r['dims_oracle_plane']['recall']}; surviving sketch entities {r['entities']['hit']}/{r['entities']['entities_surviving']} ({r['entities']['recall']})")
