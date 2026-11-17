"""Per-robot fight description: what the sim needs to know about a robot beyond its CAD.

Read from the spec's optional `sim` block, with derived defaults (each default is reported, so the `sim` check group can
say what a robot still has to declare). Robot frame: the verifier's (mm in the spec, m here), +z up.

spec "sim" block (all optional; see robot/docs/FIGHT.md):
  forward      [x, y]  robot-frame driving direction (default [0, 1])
  drive        {"max_rad_s": 230, "torque_Nm": 0.05}                   wheel motor speed + torque cap
  weapon       {"rpm": 15000, "torque_Nm": 0.12, "spin": 1}          spinner target speed, motor torque, sign
  lifter       {"group": "flipper", "up_rad": 1.2, "down_rad": 0, "torque_Nm": 0.25, "lock": ["horn"]}
  danger       [{"deg": 0, "half_deg": 60, "reach_mm": 80}]           arcs (robot frame, 0 = forward) opponents avoid
  breakable    {"part_id": break_N | {"break_N": .., "material": ..}}  override of the fastener-derived weld limits
  strategy     "spinner" | "lifter" | "pusher" | "flanker"             which brain drives it
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

BREAKABLE_KINDS = ("armor", "wedge", "fork", "plate")
SPINNER_TYPES = ("vertical_spinner", "horizontal_spinner", "drum", "spinner", "undercutter", "eggbeater", "drisk", "bar")
LIFTER_TYPES = ("flipper", "lifter")

# Per-fastener pull-out / shear limit (N) when the part is held by screws. Hand values, to be replaced by the OpenRadioss
# table (robot/fight/data/impact_table.json): M2 thread-forming in PLA ~150 N, M2 into brass heat-set ~250 N,
# M3 heat-set ~400 N, through-bolt with nut ~ bolt shear (M2 Al ~400 N, M3 steel ~1500 N).
FASTENER_N = {"M2": 220.0, "M2.5": 300.0, "M3": 400.0, "M4": 700.0}
UNFASTENED_N = 120.0  # glued / clipped / press-fit plate with no fastener through it


@dataclass
class Profile:
    name: str
    robot_type: str
    forward: np.ndarray
    strategy: str
    drive_max: float = 230.0
    drive_torque: float = 0.05
    weapon_omega: float = 0.0
    weapon_torque: float = 0.12
    lifter: dict | None = None
    danger: list = field(default_factory=list)  # [(center rad, half width rad, reach m)] robot frame, 0 = forward
    breakable: dict = field(default_factory=dict)  # part id -> break force N
    can_run_inverted: bool = False
    defaults: list = field(default_factory=list)  # fields filled by a default (reported by the sim check)
    materials: dict = field(default_factory=dict)  # part id -> (material, kind) from the spec
    raw: dict = field(default_factory=dict)  # the spec's sim block as written (motors, battery, wobble)

    @property
    def heading0(self) -> float:
        return math.atan2(self.forward[1], self.forward[0])


def _fastener_limits(spec):
    out = {}
    for f in spec.raw.get("fasteners") or []:
        des = str(f.get("designation") or "M2")
        size = des.split("x")[0]
        n = FASTENER_N.get(size, 250.0)
        for pid in f.get("through") or []:
            out[pid] = out.get(pid, 0.0) + n
    return out


def build(spec, model=None) -> Profile:
    sim = dict(spec.raw.get("sim") or {})
    dflt = []

    def get(k, v):
        if k in sim:
            return sim[k]
        dflt.append(k)
        return v

    rt = spec.robot_type
    fwd = np.asarray(get("forward", [0.0, 1.0]), float)
    fwd = fwd / (np.linalg.norm(fwd) or 1.0)
    strategy = get("strategy", "spinner" if rt in SPINNER_TYPES else "lifter" if rt in LIFTER_TYPES else "pusher")
    drive = get("drive", {})
    p = Profile(spec.name or "robot", rt, fwd, strategy, float(drive.get("max_rad_s", 230.0)),
                float(drive.get("torque_Nm", 0.05)), can_run_inverted=bool(spec.can_run_inverted))
    if rt in SPINNER_TYPES:
        w = get("weapon", {})
        p.weapon_omega = float(w.get("rpm", 15000.0)) * 2 * math.pi / 60 * float(w.get("spin", 1))
        p.weapon_torque = float(w.get("torque_Nm", 0.12))
    if rt in LIFTER_TYPES:
        lf = dict(get("lifter", {}))
        lf.setdefault("group", "flipper")
        lf.setdefault("up_rad", 1.2)
        lf.setdefault("down_rad", 0.0)
        lf.setdefault("torque_Nm", 0.25)
        lf.setdefault("lock", [])
        p.lifter = lf
    dz = get("danger", None)
    if dz is None:
        half = {"spinner": 70, "lifter": 40, "pusher": 30}.get(strategy, 40)
        reach = {"spinner": 0.09, "lifter": 0.07}.get(strategy, 0.05)
        dz = [{"deg": 0.0, "half_deg": half, "reach_mm": reach * 1000}]
    p.danger = [(math.radians(d.get("deg", 0.0)), math.radians(d.get("half_deg", 45.0)), d.get("reach_mm", 80.0) / 1000)
                for d in dz]
    lim = _fastener_limits(spec)
    over = sim.get("breakable") or {}
    if "breakable" not in sim:
        dflt.append("breakable")
    for part in spec.parts:
        if part.kind in BREAKABLE_KINDS or part.id in over:
            o = over.get(part.id)
            if isinstance(o, dict):
                o = o.get("break_N")
            p.breakable[part.id] = float(o if o is not None else lim.get(part.id, UNFASTENED_N))
    p.defaults = dflt
    p.raw = sim
    p.materials = {pt.id: ((pt.raw.get("material") if hasattr(pt, "raw") else getattr(pt, "material", None)), pt.kind)
                   for pt in spec.parts}
    return p


def requirements(spec) -> list:
    """[(field, problem)] for things a fight sim cannot run without or must not guess. Used by checks/sim.py."""
    sim = spec.raw.get("sim")
    if sim is None:
        return [("sim", "no `sim` block: forward, drive, weapon/lifter and danger arcs are all guessed")]
    out = []
    rt = spec.robot_type
    if "forward" not in sim:
        out.append(("sim.forward", "driving direction not declared"))
    if rt in SPINNER_TYPES and not (sim.get("weapon") or {}).get("rpm"):
        out.append(("sim.weapon.rpm", "spinner without a target weapon speed"))
    if rt in LIFTER_TYPES:
        lf = sim.get("lifter") or {}
        for k in ("group", "up_rad"):
            if k not in lf:
                out.append((f"sim.lifter.{k}", "lifter group / stroke not declared"))
        g = lf.get("group")
        if g and not any(pp.rotates_with == g for pp in spec.parts):
            out.append(("sim.lifter.group", f"no part rotates_with '{g}'"))
    for pid in (sim.get("breakable") or {}):
        if spec.part(pid) is None:
            out.append((f"sim.breakable.{pid}", "unknown part id"))
    for k, v in (sim.get("breakable") or {}).items():
        n = v.get("break_N") if isinstance(v, dict) else v
        if not isinstance(n, (int, float)) or n <= 0:
            out.append((f"sim.breakable.{k}", "break_N must be a positive number"))
    return out
