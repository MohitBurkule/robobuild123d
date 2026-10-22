"""The robot description an LLM (or a person) writes: parts, fasteners, wires, connections and claims.

The JSON schema is the same as the Rust `cadcraft-robot` crate, so specs move between the two tools unchanged.
Everything is read into light attribute objects with defaults; unknown keys are kept but ignored.
"""

from __future__ import annotations

import json
import math
from pathlib import Path

ELECTRONIC = {"motor", "weapon_motor", "battery", "esc", "receiver", "servo", "switch"}
STRUCTURAL = {"structure", "armor", "wedge", "plate"}
PART_KINDS = {
    "structure", "armor", "wedge", "motor", "weapon_motor", "wheel", "battery", "esc", "receiver", "servo", "switch",
    "connector", "weapon", "locking_bar", "insert", "nut", "bearing", "plate", "fork", "tyre", "pulley", "belt",
    "shaft", "pin", "spring", "other", "wedgelet", "skirt",
}
ROBOT_TYPES = {"wedge", "horizontal_spinner", "vertical_spinner", "drum", "lifter", "flipper", "other"}
SPINNER_TYPES = {"horizontal_spinner", "vertical_spinner", "drum"}


class Obj:
    """Attribute access over a dict with defaults."""

    def __init__(self, data: dict | None, defaults: dict):
        data = dict(data or {})
        for k, v in defaults.items():
            val = data.get(k, None)
            if val is None:
                val = v() if callable(v) else v
            setattr(self, k, val)
        self._extra = {k: v for k, v in data.items() if k not in defaults}

    def to_dict(self) -> dict:
        out = {}
        for k, v in self.__dict__.items():
            if k == "_extra":
                continue
            out[k] = _plain(v)
        out.update(self._extra)
        return out


def _plain(v):
    if isinstance(v, Obj):
        return v.to_dict()
    if isinstance(v, list):
        return [_plain(x) for x in v]
    if isinstance(v, dict):
        return {k: _plain(x) for k, x in v.items()}
    return v


def _obj(defaults):
    return lambda d: None if d is None else Obj(d, defaults)


Joint = _obj({"kind": "revolute", "axis": [1.0, 0.0, 0.0], "pivot": [0.0, 0.0, 0.0], "min": 0.0, "max": 0.0, "default": 0.0})
Tensioner = _obj({"kind": "none", "adjustable": False, "anchors": list})
Belt = _obj({"pulleys": list, "kind": "o_ring", "length_mm": None, "width_mm": 0.0, "thickness_mm": 0.0})
Weapon = _obj({
    "kind": "none", "motor": None, "cells": None, "reduction": None, "spin_axis": None,
    "supported_both_ends": False, "locking_bar": None,
    "spin_dir": None,  # "cw"/"ccw" (or -1/+1) about spin_axis by the right-hand rule: ccw/+1 = positive rotation
})

PART_DEFAULTS = {
    "id": "", "kind": "structure", "catalog": None, "material": None, "process": None, "shape": None,
    # New in the build123d port: a Python model file (relative to the spec) whose `build(**params)` returns a build123d solid.
    "model": None, "params": dict,
    "at": lambda: [0.0, 0.0, 0.0], "rot": lambda: [0.0, 0.0, 0.0], "parent": None, "joint": None,
    "mass_g": None, "slicer_mass_g": None, "scale_mass_g": None, "solid_fraction": None, "color": None, "label": None,
    "marked": False, "tool_free": False, "sharp": False, "cover": None, "retained": None, "fused_with": None,
    "weapon": None, "tensioner": None, "belt": None, "tyre_of": None, "no_tyre_reason": None, "actuation": None,
    "tethered": False, "actuated_by": None, "ports": dict,
    # Motion group (kinematics checks): `rotates_with` names a rotating group (any label, usually the jointed part id);
    # `fixed: true` declares the part static. Both inferred when absent.
    "rotates_with": None, "fixed": None,
}


def Part(d: dict) -> Obj:
    p = Obj(d, PART_DEFAULTS)
    p.joint = Joint(p.joint) if isinstance(p.joint, dict) else p.joint
    p.tensioner = Tensioner(p.tensioner) if isinstance(p.tensioner, dict) else p.tensioner
    p.belt = Belt(p.belt) if isinstance(p.belt, dict) else p.belt
    p.weapon = Weapon(p.weapon) if isinstance(p.weapon, dict) else p.weapon
    return p


Fastener = _obj({
    "id": "", "designation": "", "at": lambda: [0.0, 0.0, 0.0], "dir": lambda: [0.0, 0.0, -1.0], "through": list,
    "threads_into": None, "tool": None, "removable": False, "head": None,
    "waive": dict,  # {"<check id or prefix>": "<reason citing RVRN/RVnn/FSn>"}: see checks/waiver.py
})
Wire = _obj({"id": "", "from": "", "to": "", "awg": None, "kind": "signal", "slack_mm": None, "via": list})   # via: waypoints [[x,y,z],...] the route passes in order
Electronics = _obj({"failsafe": False, "weapon_remote_disable": False, "radio": None, "cells": None})
Connection = _obj({"a": "", "b": "", "method": "", "reason": "", "interference_mm": None, "mechanical_key": False})
AllowOverlap = _obj({"a": "", "b": "", "max_depth_mm": None, "reason": ""})
Claim = _obj({"id": "", "text": "", "metric": "", "op": "<=", "value": 0.0})


class Spec:
    def __init__(self, d: dict, base_dir: str | Path | None = None):
        d = dict(d or {})
        if d.get("overlay"):  # declarative settings overlay (robot/overlay.py): a variant robot without code edits
            from . import overlay as _ov

            d = _ov.apply(d, d["overlay"], base_dir=base_dir)
        if any(isinstance(p, dict) and p.get("mate") for p in (d.get("parts") or [])):
            from .cad import mates  # parts placed by constraints (robot/cad/mates.py)

            d = mates.apply(d)
        self.raw = d
        self.base_dir = Path(base_dir) if base_dir else Path.cwd()
        self.name = d.get("name") or ""
        self.profile = d.get("profile") or ""
        self.robot_type = d.get("robot_type") or "wedge"
        self.locomotion = d.get("locomotion") or "roller"
        self.parts = [Part(p) for p in (d.get("parts") or [])]
        self.fasteners = [Fastener(f) for f in (d.get("fasteners") or [])]
        self.wires = [Wire(w) for w in (d.get("wires") or [])]
        self.electronics = Electronics(d.get("electronics") or {})
        self.can_run_inverted = bool(d.get("can_run_inverted") or False)
        self.allow_overlap = [AllowOverlap(a) for a in (d.get("allow_overlap") or [])]
        self.connections = [Connection(c) for c in (d.get("connections") or [])]
        self.claims = [Claim(c) for c in (d.get("claims") or [])]
        self.start_pose = dict(d.get("start_pose") or {})
        self.ground_z = d.get("ground_z")
        self.calibration = dict(d.get("calibration") or {})
        # declared teardown moves: [{"parts": [ids], "dir": [x, y, z], "reason": ...}] - parts that come off together
        # (a fork pinned in a wedgelet slot) in the real service order; the assembly check tries them as one move
        self.teardown = [dict(t) for t in (d.get("teardown") or [])]

    def part(self, pid):
        for p in self.parts:
            if p.id == pid:
                return p
        return None

    @property
    def is_spinner(self) -> bool:
        return self.robot_type in SPINNER_TYPES

    def to_dict(self) -> dict:
        return {
            "name": self.name, "profile": self.profile, "robot_type": self.robot_type, "locomotion": self.locomotion,
            "parts": [p.to_dict() for p in self.parts], "fasteners": [f.to_dict() for f in self.fasteners],
            "wires": [w.to_dict() for w in self.wires], "electronics": self.electronics.to_dict(),
            "can_run_inverted": self.can_run_inverted, "allow_overlap": [a.to_dict() for a in self.allow_overlap],
            "connections": [c.to_dict() for c in self.connections], "claims": [c.to_dict() for c in self.claims],
            "start_pose": self.start_pose, "ground_z": self.ground_z, "calibration": self.calibration,
            **({"teardown": self.teardown} if self.teardown else {}),
        }

    def copy(self) -> "Spec":
        return Spec(json.loads(json.dumps(self.to_dict())), self.base_dir)


def load(path: str | Path) -> Spec:
    path = Path(path)
    try:
        data = json.loads(path.read_text())
    except (OSError, ValueError) as e:
        raise ValueError(f"{path} is not a valid spec: {e}") from e
    if not isinstance(data, dict):
        raise ValueError(f"{path} is not a JSON object")
    return Spec(data, path.parent)


def finite(v) -> bool:
    try:
        return all(math.isfinite(float(x)) for x in v)
    except (TypeError, ValueError):
        return False
