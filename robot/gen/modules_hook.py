"""Adapter: let robot/gen ask for a module-built robot instead of CSG boxes (UNTESTED: written without running).

Usage mirrors robot.gen.build.build(h, user): pass user={"modular": True, "modules": {...compose config...}}.
`build(h, user)` returns a spec-like dict with the same top-level "generator" key build.py fills, plus
"modular" holding the compose() result. Falls back to the CSG builder when modular is not requested.
"""
from __future__ import annotations

from . import build as csg


def config_from_hypothesis(h, user: dict | None = None) -> dict:
    """Derive a compose() config from a hypothesis (loose: reads attrs if present)."""
    user = user or {}
    if "modules" in user:
        return user["modules"]
    get = (lambda k, d=None: h.get(k, d)) if isinstance(h, dict) else (lambda k, d=None: getattr(h, k, d))
    weapon = str(get("weapon", "vertical_spinner"))
    return {
        "name": str(get("slug", "modular")),
        "pods": {"type": "drive_pod", "kwargs": {}, "at": [-10, 35, 0], "mirror": True},
        "weapon": {"type": "weapon", "kwargs": {"kind": weapon}, "at": [45, 0, 15]},
        "electronics": {"type": "electronics_bay", "kwargs": {}, "at": [-5, 0, 5]},
        "tub": {"type": "tub", "kwargs": {}, "wall_mm": 3.0, "clearance_mm": 1.0},
    }


def build(h, user: dict | None = None, layout_index: int = 0, k: int = 5) -> dict:
    if not (user or {}).get("modular"):
        return csg.build(h, user, layout_index=layout_index, k=k)
    from robot.modules.compose import compose
    cfg = config_from_hypothesis(h, user)
    try:
        res = compose(cfg)
    except Exception as e:  # noqa: BLE001
        raise csg.BuildError(f"modular build failed: {e}") from e
    return {
        "generator": {"kind": "modules", "config": cfg},
        "bom": res["bom"],
        "mass_g": res["mass_g"],
        "modular": res,
    }
