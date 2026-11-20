"""Export robots for the browser fight game (web/fight): rigid groups with true mass/inertia/hulls + fight profile.

    python -m robot.fight.webexport robots/revron/spec.json ... --out web/fight/robots

Masses: wheels/tyres the catalogue gives no mass get 3 g; every non-weapon group is then scaled so the total is the
150 g class limit (the CAD model omits electronics/wiring mass). Weapon mass stays as modelled.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path

import numpy as np

from .. import spec as spec_mod
from ..sim import model as model_mod
from . import hazards, materials, physics, profile, wobble
from .arena import _prep, sector_pieces

TOTAL_KG = 0.150
FAST = False


def export(spec_path, out_dir):
    sp = spec_mod.load(spec_path)
    m = model_mod.load(spec_path, fast=FAST)
    prof = profile.build(sp, m)
    m = _prep(m, prof)
    if prof.lifter:
        prof.lifter = dict(prof.lifter, lock=list(prof.lifter.get('lock', [])))
    for g in m.groups:  # massless wheels get 3 g
        if g.kind == "wheel" and g.mass < 1e-3:
            for p in g.parts:
                p.mass = 3e-3 / len(g.parts)
    wm = sum(g.mass for g in m.groups if g.kind == "weapon")
    rest = sum(g.mass for g in m.groups if g.kind != "weapon")
    k = max(0.2, (TOTAL_KG - wm) / rest) if rest > 0 else 1.0
    groups = []
    for g in m.groups:
        s = k if g.kind != "weapon" else 1.0
        com, I = g.com, g.inertia * s
        pieces = []
        for p in g.parts:
            ps = [p]
            if g.kind == "weapon":
                ps = sector_pieces(p, g.pivot, g.axis)
            mname, pkind = prof.materials.get(p.id, (None, p.kind))
            mu, e = materials.props(mname, pkind)
            for q in ps:
                pieces.append({"id": q.id, "part": p.id, "kind": q.kind, "mu": mu, "e": e, "com": np.round(p.com, 5).tolist(), "verts": np.round(q.verts, 5).ravel().tolist()})
        groups.append({"name": g.name, "kind": g.kind, "mass": g.mass * s, "com": com.round(6).tolist(),
                       "inertia": [I[0, 0], I[1, 1], I[2, 2], I[0, 1], I[0, 2], I[1, 2]],
                       "pivot": None if g.pivot is None else np.asarray(g.pivot).round(6).tolist(),
                       "axis": None if g.axis is None else np.asarray(g.axis).round(6).tolist(),
                       "parts": pieces, "break_N": prof.breakable.get(g.name) if g.kind == "loose" else None})
    lo, hi = m.bounds()
    raw = prof.raw or {}
    motors = {}
    for g in m.groups:
        if g.kind == "wheel":
            mo = physics.drive_motor(raw, g.name)
        elif g.kind == "weapon":
            mo = physics.weapon_motor(raw, g.name)
        else:
            continue
        motors[g.name] = {"ke": mo.ke, "r20": mo.r20, "i_max": mo.i_max, "c_th": mo.c_th, "r_th": mo.r_th, "t_cut": mo.t_cut}
    bat = physics.battery(raw)
    wob, _ = wobble.params(sp)
    coms = {p.id: p.com for g in m.groups for p in g.parts}
    kinds = {p.id: p.kind for g in m.groups for p in g.parts}
    wires = []
    for w in sp.raw.get("wires") or []:
        a, b = str(w.get("from", "")).split(".")[0], str(w.get("to", "")).split(".")[0]
        if a in coms and b in coms:
            pts = [coms[a]] + [np.asarray(v, float) * 1e-3 for v in (w.get("via") or [])] + [coms[b]]
            wires.append({"id": w.get("id"), "ends": [a, b], "kinds": [kinds.get(a, ""), kinds.get(b, "")],
                          "pts": np.round(np.asarray(pts), 5).tolist()})
    hz = hazards.params(prof)
    name = Path(spec_path).parent.name
    doc = {"id": name, "name": (sp.name or name).split(" (")[0], "robot_type": prof.robot_type,
           "forward": [float(v) for v in prof.forward], "strategy": prof.strategy,
           "drive": {"max_rad_s": prof.drive_max, "torque_Nm": prof.drive_torque},
           "weapon": {"omega": prof.weapon_omega, "torque_Nm": prof.weapon_torque} if prof.weapon_omega else None,
           "lifter": prof.lifter, "can_run_inverted": prof.can_run_inverted,
           "bounds": [lo.round(5).tolist(), hi.round(5).tolist()], "groups": groups,
           "motors": motors, "battery": {"cells": bat.cells, "mah": bat.mah, "r_int": bat.r_int},
           "wobble": wob, "blade_tc": float((raw.get("weapon") or {}).get("blade_tc", 4e-4)),
           "danger": [list(map(float, d)) for d in prof.danger], "hazards": hz, "wires": wires,
           "switches": {pid: np.round(coms[pid], 5).tolist() for pid, k in kinds.items() if k == "switch"},
           "part_kinds": kinds, "part_coms": {k: np.round(v, 5).tolist() for k, v in coms.items()},
           "mass_g": round(sum(g["mass"] for g in groups) * 1000, 1)}
    out = Path(out_dir) / f"{name}.json"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(doc, separators=(",", ":")))
    return out, doc


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("specs", nargs="+")
    ap.add_argument("--out", default="web/fight/robots")
    a = ap.parse_args()
    for s in a.specs:
        try:
            o, d = export(s, a.out)
            print(o, d["mass_g"], "g", [(g["name"], g["kind"], len(g["parts"])) for g in d["groups"]], o.stat().st_size // 1024, "KB")
        except Exception as e:  # noqa: BLE001
            print(s, "FAILED", type(e).__name__, str(e)[:200])
