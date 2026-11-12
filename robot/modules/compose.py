"""Compose a robot from module configs (UNTESTED: written without running).

config = {
  "name": "ant",
  "pods":   {"type": "drive_pod", "kwargs": {...}, "at": [x, y, z], "mirror": True},
  "weapon": {"type": "weapon", "kwargs": {...}, "at": [x, y, z]},
  "electronics": {"type": "electronics_bay", "kwargs": {...}, "at": [x, y, z]},
  "tub":    {"type": "tub", "kwargs": {...}, "wall_mm": 3.0, "clearance_mm": 1.0},
}
The tub is sized last, from the union bbox of the placed module envelopes (+ clearance + wall), unless the
tub kwargs already give a size. Pods with mirror=True are placed at (x, y) and (x, -y), the copy rotated 180 deg.
"""
from __future__ import annotations

from build123d import Compound, Location

from . import make
from .base import ModuleResult, place


def _loc(at, rot_z: float = 0.0) -> Location:
    x, y, z = (list(at or [0, 0, 0]) + [0, 0, 0])[:3]
    return Location((x, y, z), (0, 0, rot_z))


def _bbox(results: list[ModuleResult]):
    lo, hi = [1e9] * 3, [-1e9] * 3
    for r in results:
        shapes = [r.envelope] if r.envelope is not None else list(r.parts.values())
        for s in shapes:
            b = s.bounding_box()
            for i, (a, c) in enumerate(((b.min.X, b.max.X), (b.min.Y, b.max.Y), (b.min.Z, b.max.Z))):
                lo[i], hi[i] = min(lo[i], a), max(hi[i], c)
    return lo, hi


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
        kw = dict(tub_cfg.get("kwargs", {}))
        if not {"length", "width", "height"} & set(kw):
            inner = [r for k, r in placed.items() if k != "weapon" or tub_cfg.get("enclose_weapon")]
            lo, hi = _bbox(inner) if inner else ([0] * 3, [0] * 3)
            pad = tub_cfg.get("clearance_mm", 1.0) + tub_cfg.get("wall_mm", 3.0)
            kw.update(length=hi[0] - lo[0] + 2 * pad, width=hi[1] - lo[1] + 2 * pad,
                      height=hi[2] - lo[2] + pad, wall=tub_cfg.get("wall_mm", 3.0))
            centre = [(lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, lo[2] - tub_cfg.get("wall_mm", 3.0)]
        else:
            centre = tub_cfg.get("at", [0, 0, 0])
        placed["tub"] = _build_one({"type": tub_cfg.get("type", "tub"), "kwargs": kw}, centre)

    solids = [p for r in placed.values() for p in r.parts.values()]
    return {
        "name": config.get("name", "modular"),
        "assembly": Compound(children=solids) if solids else None,
        "modules": placed,
        "bom": [b for r in placed.values() for b in r.bom],
        "mass_g": sum(r.mass_g for r in placed.values()),
    }
