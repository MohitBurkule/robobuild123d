"""Write the manufacturing pack. UNTESTED.

  python -m robot mfg <spec.json> <out_dir>   (wire into robot/cli.py later; other thread owns cli.py)
"""

from __future__ import annotations

import csv
import io
import json
from pathlib import Path

import numpy as np

from . import guide
from .bom import bom, buy_list, fastener_counts
from .budget import mass_budget
from .cutlist import SHEET_PROCESSES, cut_list
from .printing import print_settings
from .steps import assembly_steps
from ._util import x

UP = {"+x": [1, 0, 0], "-x": [-1, 0, 0], "+y": [0, 1, 0], "-y": [0, -1, 0], "+z": [0, 0, 1], "-z": [0, 0, -1]}


def bed_matrix(up):
    """4x4 rotating part-frame `up` axis onto +Z (bed normal)."""
    a = np.array(UP.get(up, UP["+z"]), float)
    z = np.array([0, 0, 1.0])
    v, c = np.cross(a, z), float(a @ z)
    if np.allclose(v, 0):
        R = np.eye(3) if c > 0 else np.diag([1.0, -1.0, -1.0])
    else:
        k = np.array([[0, -v[2], v[1]], [v[2], 0, -v[0]], [-v[1], v[0], 0]])
        R = np.eye(3) + k + k @ k / (1 + c)
    M = np.eye(4)
    M[:3, :3] = R
    return M


def collect(spec, world=None, report=None, metrics=None):
    return {"bom": bom(spec), "buy": buy_list(spec), "fasteners": fastener_counts(spec),
            "mass": mass_budget(spec, report), "print": print_settings(spec, metrics),
            "cut": cut_list(spec, world), "steps": assembly_steps(spec)}


def _bom_csv(rows):
    s = io.StringIO()
    w = csv.DictWriter(s, fieldnames=list(rows[0].keys()) if rows else ["id"])
    w.writeheader()
    w.writerows(rows)
    return s.getvalue()


def write(spec, out_dir, world=None, report=None, metrics=None, step=True):
    root = Path(out_dir)
    for d in ("print", "cut", "step"):
        (root / d).mkdir(parents=True, exist_ok=True)
    files = []

    def put(rel, data):
        (root / rel).write_bytes(data if isinstance(data, bytes) else data.encode())
        files.append(rel)

    if world is None:
        from .. import checks, render
        world, report, _ = render.world_for(spec, checks.Options())
    for p in spec.parts:
        b = world.body(p.id)
        if b is None or x(p, "catalog"):
            continue
        proc = (x(p, "process") or "").lower()
        if proc in ("fdm", "resin"):
            mesh = b.geom.mesh.copy()  # part frame
            mesh.apply_transform(bed_matrix((x(p, "print_orientation") or "+z").lower()))
            mesh.apply_translation([0, 0, -mesh.bounds[0][2]])  # sit on bed
            put(f"print/{p.id}.stl", mesh.export(file_type="stl"))
            if step and b.geom.solid is not None:
                try:
                    import build123d as bd
                    from .. import shapes
                    bd.export_step(b.geom.solid.moved(shapes.location(bed_matrix(x(p, "print_orientation") or "+z"))),
                                   str(root / "print" / f"{p.id}.step"))
                    files.append(f"print/{p.id}.step")
                except Exception:  # noqa: BLE001
                    pass
    if any((x(p, "process") or "").lower() in SHEET_PROCESSES for p in spec.parts):
        from .. import world as world_mod
        from ..checks import process as process_check
        dxf, _fails = process_check.export_dxf(world_mod.resolve(spec, fast=True), root / "cut")
        files += [f"cut/{f}" for f in dxf]
    data = collect(spec, world, report, metrics)
    for s in data["cut"]["rows"]:
        s["dxf"] = "cut/" + s["dxf"]
    md = guide.markdown(spec.name or "robot", data)
    put("BUILD.md", md)
    put("BUILD.html", guide.to_html(spec.name or "robot", md))
    put("bom.csv", _bom_csv(data["bom"]))
    put("pack.json", json.dumps(data, indent=2, default=str))
    return data, files


def main(argv=None):
    import argparse
    from .. import spec as spec_mod
    ap = argparse.ArgumentParser("robot.mfg")
    ap.add_argument("spec")
    ap.add_argument("out")
    ap.add_argument("--no-step", action="store_true")
    a = ap.parse_args(argv)
    _, files = write(spec_mod.load(a.spec), a.out, step=not a.no_step)
    print("\n".join(files))


if __name__ == "__main__":
    main()
