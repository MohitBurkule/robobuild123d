"""Assembler: hypothesis + layout -> complete spec.json, then the verifier gate (`gate.py`) repairs or rejects it.

Pipeline (each step one small function writing into a `Plan`):
  frame -> drive -> clamshell screw sites -> internal layout (CSP) -> component pockets + switch -> front interface
  -> weapon module -> wiring -> shell halves -> electronics/claims -> spec dict.
"""

from __future__ import annotations

import copy
import json
from pathlib import Path

from . import hypothesis as hyp_mod
from .external import drive, electronics, fasteners, front, pockets, shell, switch, weapon, wiring
from .external.plan import Frame, Plan
from .layout import Component, Keepout, LayoutInputs, Link, solve

ROBOT_TYPE = {"none_pusher": "wedge", "wedge": "wedge", "lifter": "lifter", "hspin_bar": "horizontal_spinner",
              "vspin_drisk": "vertical_spinner"}


class BuildError(ValueError):
    pass


# ---------------------------------------------------------------- frame
def frame_params(h, user: dict | None = None) -> dict:
    """Default body box for a hypothesis (user `outline`/`height` override)."""
    user = user or {}
    R = h.wheel_dia / 2
    zb = -max(7.7, R - 4.0)
    zt = min(10.0, R - 1.5) if h.invertible else 10.0
    p = {"axle_y": -16.0, "y0": -40.0, "y1": 36.0, "zb": zb, "zt": zt, "floor_z": -R}
    if h.weapon == "hspin_bar":
        p.update(axle_y=-14.0, y0=-48.0, y1=44.0, floor=1.1)
    if h.weapon == "vspin_drisk":
        p.update(axle_y=-14.0, y0=-36.0, y1=44.0, floor=1.1)
    if h.weapon == "lifter":
        p.update(axle_y=-18.0, y0=-42.0, y1=30.0)
    p.update({k: v for k, v in user.items() if k in p})
    if "y0" not in user:  # room behind the wheels for the rear clamshell screws
        p["y0"] = min(p["y0"], p["axle_y"] - R - 16.5)
    return p


def default_outline(half_w, y0, y1, chamfer=4.0) -> list:
    return [[-half_w, y1], [-half_w, y0 + chamfer], [-half_w + chamfer, y0], [half_w - chamfer, y0], [half_w, y0 + chamfer],
            [half_w, y1]][::-1]


def make_plan(h, user=None) -> tuple:
    fp = frame_params(h, user)
    g = drive.geom_for(h, fp["axle_y"])
    W = round(g.half_width, 2)
    outline = (user or {}).get("outline") or default_outline(W, fp["y0"], fp["y1"])
    fr = Frame(outline=[list(map(float, p)) for p in outline], zb=fp["zb"], zt=fp["zt"], floor=fp.get("floor", 1.5))
    plan = Plan(hyp=h, frame=fr, name=(user or {}).get("name") or f"gen {h.weapon}",
                robot_type=ROBOT_TYPE.get(h.weapon, "other"))
    plan.extra["_floor_z"] = fp["floor_z"]
    return plan, g


# ---------------------------------------------------------------- layout
def layout_inputs(plan, h, user=None) -> LayoutInputs:
    comps = []
    for c in electronics.components(h):
        size = electronics.size_of(c["catalog"])
        fixed = ((user or {}).get("fixed") or {}).get(c["id"])
        comps.append(Component(c["id"], c["kind"], size, electronics.mass_of(c["catalog"]), c["catalog"],
                               fixed_at=tuple(fixed) if fixed else None, ports=electronics.ports_of(c["catalog"]),
                               min_front_mm=c.get("min_front_mm", 0.0), min_side_mm=c.get("min_side_mm", 0.0),
                               port_room=pockets.PORT_ROOM + pockets.GAP,
                               rot_choices=(0.0, 90.0, 180.0, 270.0) if c["kind"] == "battery" else (0.0, 90.0)))
    comps.append(Component("power_switch", "switch", switch.SIZE, 0.5, "switch_slide_12x4", on_wall=True,
                           rot_choices=(0.0, 90.0), ports={"in": (-4, 0, 0), "out": (4, 0, 0)}))
    links = [Link(a.split(".")[0] if a.split(".")[0] in {c.id for c in comps} else a,
                  b.split(".")[0] if b.split(".")[0] in {c.id for c in comps} else b)
             for _, a, b, _, _ in electronics.harness(h, plan.extra.get("weapon_motor"), plan.extra.get("servo"))]
    anchors = {k: (v[0], v[1]) for k, v in plan.anchors.items()}
    fixed_mass = [(p_mass(p), p["at"][0], p["at"][1]) for p in plan.parts]
    keep = [Keepout(*k) for k in plan.keepouts]
    f = plan.frame
    return LayoutInputs(outline=f.outline, height=f.zt - f.zb, wall=f.wall + 0.2, components=comps, keepouts=keep,
                        links=links, anchors=anchors, fixed_mass=fixed_mass,
                        cog_target=(0.0, plan.extra.get("cog_y", plan.extra.get("axle_y", 0.0) + 6.0)),
                        seed=(user or {}).get("seed", 0))


def p_mass(p) -> float:
    from .. import catalog
    if p.get("mass_g"):
        return float(p["mass_g"])
    if p.get("catalog"):
        return float(catalog.find(p["catalog"]).mass_g)
    return 2.0


def place_components(plan, h, lay):
    for c in electronics.components(h):
        pl = lay.placements[c["id"]]
        size = electronics.size_of(c["catalog"])
        z = component_z(plan, size[2])
        extra = {"ports": electronics.ports_of(c["catalog"])} if c["catalog"] in electronics.PORTS else {}
        pockets.add_component(plan, c["id"], c["kind"], c["catalog"], size, pl.x, pl.y, z, pl.rot_z, **extra)
        plan.placements[c["id"]] = (pl.x, pl.y, z, pl.rot_z)
    sw = lay.placements["power_switch"]
    z = switch.add_switch(plan, sw.x, sw.y, sw.rot_z)
    plan.placements["power_switch"] = (sw.x, sw.y, z, sw.rot_z)


def component_z(plan, height) -> float:
    f = plan.frame
    lo, hi = f.zb + f.floor + 0.4 + height / 2, f.zt - f.floor - 0.4 - height / 2
    return round(min(max(0.0, lo), hi), 2)


# ---------------------------------------------------------------- wiring
def add_wiring(plan, h):
    for wid, a, b, kind, awg in electronics.harness(h, plan.extra.get("weapon_motor"), plan.extra.get("servo")):
        ends = {a.split(".")[0], b.split(".")[0]}
        avoid = {"drive_mid"}
        avoid |= set(plan.extra.get("wire_avoid_ok", ()))
        wiring.add_wire(plan, wid, a, b, kind, awg=awg, slack=8.0 if kind == "power" else 6.0, avoid=avoid)


# ---------------------------------------------------------------- spec
def to_spec(plan, h) -> dict:
    weaponed = plan.extra.get("weapon_motor") or plan.extra.get("servo")
    cells = 1 if h.battery == "lipo_1s_300" else 2
    spec = {
        "name": plan.name, "profile": "aws2025", "robot_type": plan.robot_type, "locomotion": "roller",
        "parts": plan.parts, "fasteners": plan.fasteners, "wires": plan.wires,
        "electronics": {"failsafe": True, "weapon_remote_disable": bool(weaponed), "radio": "2.4 GHz", "cells": cells,
                        **plan.electronics},
        "can_run_inverted": bool(h.invertible), "allow_overlap": plan.allow_overlap, "connections": plan.connections,
        "claims": [{"id": "c_mass", "text": "weighs 150 g or less", "metric": "mass_total_g", "op": "<=", "value": 150.0},
                   {"id": "c_fit", "text": "fits the 150 mm square", "metric": "footprint_mm", "op": "<=", "value": 150.0}]
        + plan.claims,
        "generator": {"hypothesis": h.to_dict(), "slug": h.slug, "notes": plan.notes,
                      "layout": {k: list(v) for k, v in plan.placements.items()}},
    }
    if plan.archetype:
        spec["archetype"] = plan.archetype
    spec.update({k: v for k, v in plan.extra.items() if k in ("start_pose", "weapon_lock")})
    return spec


def _base(h, user):
    plan, g = make_plan(h, user)
    plan.extra["axle_y"] = g.axle_y
    drive.add_drive(plan, g)
    weapon.prepare(plan, h, g)
    fasteners.add_clamshell_screws(plan, fasteners.clamshell_sites(plan))
    return plan, g


def _finish(plan, g, h, lay):
    place_components(plan, h, lay)
    add_front(plan, h)
    weapon.add(plan, h, g)
    add_wiring(plan, h)
    shell.add_shell(plan)
    return to_spec(plan, h)


def layouts(h, user=None, k=5):
    plan, _ = _base(h, user)
    return solve(layout_inputs(plan, h, user), k=k)


def build(h, user: dict | None = None, layout_index: int = 0, k: int = 5) -> dict:
    """Spec dict for hypothesis `h`: the `layout_index`-th best layout whose wires can all be channelled
    (layouts that cannot be wired are skipped)."""
    if isinstance(h, dict):
        h = hyp_mod.Hypothesis.from_dict(h)
    if not hyp_mod.buildable(h):
        raise BuildError(f"no assembler for {h.slug} yet (buildable: {sorted(hyp_mod.BUILDABLE)})")
    lays = layouts(h, user, k=max(k, layout_index + 1) * 2)
    errors, usable = [], 0
    for lay in lays:
        plan, g = _base(h, user)
        try:
            spec = _finish(plan, g, h, lay)
        except ValueError as e:
            errors.append(str(e))
            continue
        if usable == layout_index:
            return spec
        usable += 1
    raise BuildError(f"{h.slug}: no wireable layout ({'; '.join(errors[:3])})")


def add_front(plan, h):
    if h.front == "wedge":
        front.add_wedge(plan, length=plan.extra.get("wedge_len", 46.0))
    elif h.front in ("forks", "wedgelets") and h.weapon == "vspin_drisk":
        pass  # the drisk module adds its own fork tines
    elif h.front in ("forks", "wedgelets", "skirt", "plow"):
        front.add_front(plan, h.front)


def write(spec: dict, out_dir: str | Path, slug: str | None = None) -> Path:
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    path = out / f"{slug or 'spec'}.json"
    path.write_text(json.dumps(copy.deepcopy(spec), indent=1))
    return path
