"""`robot doctor`: is this machine ready to build + verify robots? UNTESTED (written without running).

Reports python, required/optional deps with versions, cache dir + free disk, bundled data files
(guide, catalogue, rules, templates) with a fix hint per problem. Exit 0 = all required ok, 1 = something required missing.
"""

from __future__ import annotations

import importlib
import json
import os
import shutil
import sys
from pathlib import Path

HERE = Path(__file__).parent
EXTRA = "pip install -e '.[robot]'  (from the robobuild123d checkout)"

# (import name, pip name, required?, what needs it)
DEPS = (
    ("build123d", "build123d", True, "all CAD"),
    ("OCP", "cadquery-ocp-novtk", True, "CAD kernel"),
    ("numpy", "numpy", True, "everything"),
    ("scipy", "scipy", True, "measure, sim"),
    ("trimesh", "trimesh", True, "meshes, checks"),
    ("manifold3d", "manifold3d", True, "mesh booleans (trimesh backend)"),
    ("shapely", "shapely", True, "2D sections, footprint"),
    ("rtree", "rtree", True, "trimesh proximity queries"),
    ("networkx", "networkx", True, "trimesh graph ops, assembly order"),
    ("PIL", "pillow", True, "renders"),
    ("mujoco", "mujoco", False, "robot.sim physics (extra [sim])"),
    ("pytest", "pytest", False, "running robot/tests (extra [robot-dev])"),
)

DATA = (
    ("GUIDE.md", "builder guide (`robot guide`)"),
    ("catalog_data/components.json", "COTS catalogue (`robot catalog`)"),
    ("rules", "competition rules profiles"),
    ("templates", "robot templates (`robot templates`)"),
)

MIN_FREE_GB = 2.0


def check_dep(mod, pip, required, why):
    try:
        m = importlib.import_module(mod)
        ver = getattr(m, "__version__", None)
        if ver is None:
            try:
                from importlib.metadata import version
                ver = version(pip)
            except Exception:  # noqa: BLE001
                ver = "?"
        return {"name": pip, "ok": True, "version": str(ver), "required": required, "why": why}
    except Exception as e:  # noqa: BLE001 - broken installs raise more than ImportError
        fix = f"pip install {pip}" if not required else f"{EXTRA}  or  pip install {pip}"
        return {"name": pip, "ok": False, "required": required, "why": why, "error": f"{type(e).__name__}: {e}", "fix": fix}


def check_cache():
    d = Path(os.environ.get("ROBOT_CACHE") or Path.home() / ".cache" / "robot")
    row = {"name": "cache", "path": str(d), "required": True, "disabled": bool(os.environ.get("ROBOT_NO_CACHE"))}
    try:
        d.mkdir(parents=True, exist_ok=True)
        probe = d / ".doctor_probe"
        probe.write_text("x")
        probe.unlink()
        free = shutil.disk_usage(d).free / 1e9
        used = sum(f.stat().st_size for f in d.rglob("*") if f.is_file()) / 1e9
        row.update(ok=free >= MIN_FREE_GB, free_gb=round(free, 2), used_gb=round(used, 2))
        if not row["ok"]:
            row["fix"] = f"free disk (< {MIN_FREE_GB} GB left): delete old files in {d}, or set ROBOT_CACHE to a bigger disk"
    except OSError as e:
        row.update(ok=False, error=str(e), fix="set ROBOT_CACHE to a writable dir, or ROBOT_NO_CACHE=1")
    return row


def check_data():
    rows = []
    for rel, why in DATA:
        p = HERE / rel
        ok = p.is_file() or (p.is_dir() and any(p.iterdir()))
        r = {"name": rel, "ok": ok, "required": True, "why": why, "path": str(p)}
        if ok and p.suffix == ".json":
            try:
                json.loads(p.read_text())
            except ValueError as e:
                r.update(ok=False, error=f"bad json: {e}")
        if not r["ok"]:
            r["fix"] = ("reinstall: package data missing (non-editable wheel built without package-data?) "
                        f"-> {EXTRA}")
        rows.append(r)
    return rows


def run():
    py_ok = sys.version_info >= (3, 11)
    rows = [{"name": "python", "ok": py_ok, "required": True, "version": sys.version.split()[0],
             **({} if py_ok else {"fix": "use python >= 3.11"})}]
    rows += [check_dep(*d) for d in DEPS]
    rows.append(check_cache())
    rows += check_data()
    ok = all(r["ok"] for r in rows if r["required"])
    return {"ok": ok, "rows": rows}


def cli(a):
    res = run()
    if getattr(a, "json", False):
        print(json.dumps(res, indent=1))
    else:
        for r in res["rows"]:
            tag = "ok  " if r["ok"] else ("MISS" if r["required"] else "opt ")
            extra = r.get("version") or (f"{r.get('free_gb')} GB free, {r.get('used_gb')} GB used at {r['path']}"
                                         if r["name"] == "cache" and "free_gb" in r else "")
            print(f"[{tag}] {r['name']:<30} {extra}")
            if not r["ok"]:
                if r.get("error"):
                    print(f"       {r['error']}")
                print(f"       fix: {r.get('fix')}")
        print("doctor: READY" if res["ok"] else "doctor: NOT READY (fix the MISS rows)")
    return 0 if res["ok"] else 1


def add_cli(sub):
    p = sub.add_parser("doctor", help="check deps, cache dir/disk and bundled data; prints fixes")
    p.add_argument("--json", action="store_true")
    p.set_defaults(func=cli)
