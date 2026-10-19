"""Combat failure modes (`threat.CF-*`): how an opponent, the arena or the robot's own weapon breaks the robot.

The catalogue is research/combat_failure_modes.json (copied here as `modes.json`): 61 modes, each with a mechanism (the
WHY), a measurement, a threshold, a severity and a fix. Every mode is one finding `threat.<id>`; a failing finding names
the weak point, explains why it matters and carries the catalogue fix. Most are warnings; CF-GD08 (wire near the
weapon's swept volume) and CF-OW01 (weapon strikes the floor at 5 deg pitch) are blockers.

Layout: `attack.py` (who hits where: attack directions/heights per weapon type, reference energies, debris sizes, the
z-buffer visibility and thickness helpers), `facts.py` (measure once), `rules.py` (one small pure function per mode).
"""

from __future__ import annotations

import json
from pathlib import Path

from ...finding import BLOCKER, INFO, WARNING, fail, ok
from . import facts as facts_mod
from .rules import NA, RULES, SKIP, WARN

G = "threat"
MODES = {m["id"]: m for m in json.loads((Path(__file__).with_name("modes.json")).read_text())}
FALLBACK_FIX = {
    "CF-WL05": "Make the robot drive inverted or add a self-righting mechanism.",
    "CF-AR02": "Keep push and top speed balanced; avoid long front overhangs near the pit.",
    "CF-OW02": "Widen the track or reduce the weapon's angular momentum.",
    "CF-OW05": "Strap or pocket the battery so it cannot move when the robot is upside down.",
}


def judge(mid, T):
    """(severity, status, message, expected, actual) of one mode on facts T."""
    m = MODES[mid]
    try:
        st, msg, exp, act = RULES[mid](T)
    except Exception as e:  # noqa: BLE001 - one bad rule must not hide the others
        st, msg, exp, act = None, f"rule raised {type(e).__name__}: {e}", None, None
    sev = {"blocker": BLOCKER, "warning": WARNING}.get(m["severity"], INFO)
    if st == WARN:
        sev, st = WARNING, False
    return sev, st, msg, exp, act


def run(ctx):
    T = facts_mod.facts(ctx)
    out = []
    for name, err in T.get("_errors", {}).items():
        ctx.not_checked.append(f"threat facts `{name}` failed: {err}")
    if "floor" not in T.get("cg", {}):
        ctx.not_checked.append("Combat failure modes: no solid parts")
        return [fail("threat.no_geometry", G, WARNING, "No geometry", "No solid parts to judge combat failure modes on.")]
    for mid, m in MODES.items():
        if mid not in RULES:
            continue
        fid = f"threat.{mid}"
        title = m["name"]
        sev, st, msg, exp, act = judge(mid, T)
        why = m.get("mechanism", "")
        fix = (m.get("fix") or FALLBACK_FIX.get(mid) or "See research/combat_failure_modes.md.").strip()
        ref = f" (extends {m['extends']})" if m.get("extends") else ""
        if st == NA:
            continue
        if st == SKIP:
            ctx.not_checked.append(f"{fid} {title}: {msg}")
            continue
        if st is None:
            ctx.not_checked.append(f"{fid} {title}: {msg}")
            out.append(fail(fid, G, WARNING if sev != INFO else INFO, f"{title} (not measured)", msg).fix("Supply the missing data (mass, material, wiring routes)."))
        elif st:
            out.append(ok(fid, G, title, msg))
        else:
            f = fail(fid, G, sev, title, f"Weak point: {msg} WHY: {why} FIX: {fix}{ref}").fix(fix)
            if exp is not None:
                f.expect(exp, act)
            out.append(f)
    from .rules_ext import EXT
    for mid, (title, fn, why, fix) in EXT.items():
        fid = f"threat.{mid}"
        try:
            st, msg, exp, act = fn(T)
        except Exception as e:  # noqa: BLE001
            st, msg, exp, act = None, f"rule raised {type(e).__name__}: {e}", None, None
        if st == NA:
            continue
        if st == SKIP or st is None:
            ctx.not_checked.append(f"{fid} {title}: {msg}")
            continue
        if st:
            out.append(ok(fid, G, title, msg))
        else:
            out.append(fail(fid, G, WARNING, title, f"Weak point: {msg} WHY: {why} FIX: {fix}").fix(fix).expect(exp, act))
    return out
