"""Compose a robot from module configs (UNTESTED: written without running).

config = {
  "name": "ant",
  "pods":   {"type": "drive_pod", "kwargs": {...}, "at": [x, y, z], "mirror": True},
  "weapon": {"type": "weapon", "kwargs": {...}, "at": [x, y, z]},
  "electronics": {"type": "electronics_bay", "kwargs": {...}, "at": [x, y, z]},
  "tub":    {"type": "tub", "kwargs": {"wall": 3.0, ...}},
}
The tub is a TubShell sized last from the placed modules (electronics cuts, pod clamps, weapon envelope), unless the
config has no tub. Pods with mirror=True are placed at (x, y) and (x, -y), the copy rotated 180 deg.
"""
from __future__ import annotations

from build123d import Compound, Location

from . import make
from .base import ModuleResult, place


def _loc(at, rot_z: float = 0.0) -> Location:
    x, y, z = (list(at or [0, 0, 0]) + [0, 0, 0])[:3]
    return Location((x, y, z), (0, 0, rot_z))


def _build_one(entry: dict, at=None, rot_z: float = 0.0) -> ModuleResult:
    mod = make(entry["type"], **entry.get("kwargs", {}))
    return place(mod.build(), _loc(at if at is not None else entry.get("at"), rot_z))


def compose(config: dict) -> dict:
    """Return {"assembly": Compound, "modules": {name: ModuleResult}, "bom": [...], "mass_g": float}."""
    placed: dict[str, ModuleResult] = {}
    pods = config.get("pods")
    if pods:
        x, y, z = (list(pods.get("at", [0, 30, 0])) + [0, 0, 0])[:3]
        placed["pod_left"] = _build_one(pods, [x, y, z])
        if pods.get("mirror", True):
            placed["pod_right"] = _build_one(pods, [x, -y, z], 180.0)
    for key in ("weapon", "electronics"):
        if config.get(key):
            placed[key] = _build_one(config[key])
    for i, extra in enumerate(config.get("extra", [])):
        placed[extra.get("name", f"extra{i}")] = _build_one(extra)

    tub_cfg = config.get("tub")
    if tub_cfg:
        from .tub import TubShell
        kw = dict(tub_cfg.get("kwargs", {}))
        kw.setdefault("wall", tub_cfg.get("wall_mm", 3.0))
        cuts = [p for k, r in placed.items() if k.startswith("pod_") for n, p in r.parts.items() if n == "clamp"]
        cuts += [p for n, p in placed.get("electronics", ModuleResult("none")).parts.items() if n.startswith("cut_")]
        weapons = [placed["weapon"].envelope] if "weapon" in placed and placed["weapon"].envelope is not None else []
        tub = TubShell(bay_cuts=cuts, weapon_envelopes=weapons, **kw)
        placed["tub"] = tub.build()    # built directly in the host frame from the placed contents: not moved again

    solids = [p for r in placed.values() for p in r.parts.values()]
    return {
        "name": config.get("name", "modular"),
        "assembly": Compound(children=solids) if solids else None,
        "modules": placed,
        "bom": [b for r in placed.values() for b in r.bom],
        "mass_g": sum(r.mass_g for r in placed.values()),
    }
