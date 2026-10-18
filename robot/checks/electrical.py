"""Electrical system: voltages and currents against component ratings, wire gauge, connectors, switch, receiver supply,
failsafe, indicator, battery protection and service, wire routing near moving parts, power path and runtime.

Same structure as `archetype`: `facts(ctx)` gathers numbers (None = unknown), each rule is a pure function
`(facts) -> (passed True/False/'warn'/None, message)`. Ratings come from the catalog entry's props, overridden by a part's
own `ratings` table in the spec (e.g. `"ratings": {"current_a": 15}` on a switch). Unknown data is a WARNING plus a
NOT CHECKED line, never a pass.
"""

from __future__ import annotations

import math
import re

import numpy as np

from .. import measure
from ..finding import BLOCKER, WARNING, fail, ok
from .power import rim_radius, spin_axis

G = "electrical"
MAX_CELL_V = 4.2
# Continuous amps for short silicone-insulated runs inside a robot (conservative chassis-wiring values).
AMPACITY = {30: 2.5, 28: 3.5, 26: 5.0, 24: 8.0, 22: 12.0, 20: 17.0, 18: 24.0, 16: 33.0, 14: 45.0}
CONNECTOR_A = {"xt30": 30.0, "xt60": 60.0, "xt90": 90.0, "mr30": 30.0, "mr60": 60.0, "xt20": 20.0, "ph2": 2.0, "jst_ph": 2.0,
               "jst": 5.0, "jst_rcy": 5.0, "bec": 5.0, "deans": 40.0, "t_plug": 40.0, "ec2": 20.0, "ec3": 60.0, "a30": 30.0,
               "mx": 3.0, "molex": 3.0, "bullet2": 20.0, "bullet1": 10.0}
MIN_RUNTIME_MIN = 3.0
CLEAR = ("pc", "polycarbonate", "clear_pc", "acrylic", "petg_clear")
ROTATING = ("weapon", "wheel", "pulley", "belt", "hub")


def awg_amps(awg):
    if awg is None:
        return None
    a = int(round(float(awg)))
    if a in AMPACITY:
        return AMPACITY[a]
    ks = sorted(AMPACITY)
    if a > ks[-1]:
        return AMPACITY[ks[-1]] * 0.5 ** ((a - ks[-1]) / 3)  # thinner than tabulated
    return AMPACITY[ks[0]]


def ratings(rp):
    p = dict(rp.cat.props) if rp.cat is not None else {}
    p.update(rp.part._extra.get("ratings") or {})
    return p


def _parse(cid, pat):
    m = re.search(pat, (cid or "").lower())
    return float(m.group(1)) if m else None


def _end(s):
    s = s or ""
    return s.split(".", 1) if "." in s else (s, "")


# ------------------------------------------------------------------------------------------------------------- rules


def r_drive_motor_voltage(F):
    v, ms = F.get("v_nom"), F.get("drive_motors")
    if not ms:
        return None, "no drive motors"
    if v is None:
        return None, "battery voltage unknown"
    unk = [m for m, d in ms.items() if d.get("nominal_v") is None]
    if unk:
        return None, f"no nominal voltage for {', '.join(unk)}"
    worst = max(ms.items(), key=lambda kv: v / kv[1]["nominal_v"])
    ratio = v / worst[1]["nominal_v"]
    if ratio > 2.0:
        return False, f"{v:.1f} V pack on `{worst[0]}` rated {worst[1]['nominal_v']:.1f} V ({ratio:.1f}x): it will burn out."
    if ratio > 1.5:
        return "warn", f"{v:.1f} V pack on `{worst[0]}` rated {worst[1]['nominal_v']:.1f} V ({ratio:.1f}x): short brush life."
    return True, f"Pack {v:.1f} V nominal is within 1.5x of every drive motor's rating (worst {ratio:.2f}x)."


def r_weapon_motor_voltage(F):
    cells, wm = F.get("cells"), F.get("weapon_motors")
    if not wm:
        return True, "No weapon motor."
    if cells is None:
        return None, "battery cell count unknown"
    unk = [m for m, d in wm.items() if d.get("max_cells") is None]
    if unk:
        return None, f"no max_cells rating for {', '.join(unk)}"
    bad = [m for m, d in wm.items() if d["max_cells"] < cells]
    return not bad, f"{cells:g}S pack; weapon motor max cells: " + ", ".join(f"`{m}` {d['max_cells']:g}S" for m, d in wm.items()) + "."


def r_esc_voltage(F):
    cells, escs = F.get("cells"), F.get("escs")
    if not escs:
        return None, "no ESC"
    if cells is None:
        return None, "battery cell count unknown"
    unk = [e for e, d in escs.items() if d.get("max_cells") is None]
    if unk:
        return None, f"no cell rating for {', '.join(unk)}"
    bad = [e for e, d in escs.items() if d["max_cells"] < cells]
    return not bad, f"{cells:g}S pack; ESC ratings: " + ", ".join(f"`{e}` {d['max_cells']:g}S" for e, d in escs.items()) + "."


def _esc_current(F, weapon):
    escs = F.get("escs")
    if not escs:
        return None, "no ESC"
    msgs, worst = [], True
    seen = False
    for e, d in escs.items():
        loads = d["loads_weapon"] if weapon else d["loads_drive"]
        if not loads:
            continue
        seen = True
        per = max(loads.values()) if not weapon else sum(loads.values())
        if any(v is None for v in loads.values()):
            return None, f"motor current unknown for loads of `{e}`"
        cont, burst = d.get("cont_a"), d.get("burst_a")
        if cont is None and burst is None:
            return None, f"`{e}` has no current rating"
        lim = burst if burst is not None else cont
        msgs.append(f"`{e}` {'burst' if burst is not None else 'continuous'} {lim:.1f} A vs {'stall' if not weapon else 'max'} {per:.1f} A per channel")
        if per > 2.0 * lim:
            worst = False
        elif per > lim and worst is True:
            worst = "warn"
    if not seen:
        return True, f"No ESC drives a {'weapon' if weapon else 'drive'} motor."
    return worst, "; ".join(msgs) + "."


def r_esc_drive_current(F):
    return _esc_current(F, False)


def r_esc_weapon_current(F):
    return _esc_current(F, True)


def r_wire_ampacity(F):
    ws = F.get("wire_currents")
    if ws is None:
        return None, "no wires"
    unk = [w for w, (a, i) in ws.items() if a is None or i is None]
    if unk:
        return None, f"gauge or current unknown for {', '.join(unk)}"
    bad = [(w, a, i) for w, (a, i) in ws.items() if i > awg_amps(a)]
    if bad:
        return False, "Over capacity: " + "; ".join(f"`{w}` {a:g} AWG carries {i:.1f} A (rated {awg_amps(a):.1f} A)" for w, a, i in bad) + "."
    return True, f"All {len(ws)} wires within their gauge's continuous rating."


def r_connector_rating(F):
    c = F.get("connector")
    if c is None:
        return None, "no battery connector port or load current"
    name, amps, need = c
    if amps is None:
        return None, f"connector `{name}` has no known rating"
    return need <= amps, f"Battery connector `{name}` rated {amps:.0f} A; peak load {need:.1f} A."


def r_switch_rating(F):
    s = F.get("switch")
    if s is None:
        return None, "no switch"
    sid, amps, need = s
    if amps is None:
        return None, f"switch `{sid}` has no current rating (add `ratings.current_a`)"
    if need is None:
        return None, "load current unknown"
    return need <= amps, f"Switch `{sid}` rated {amps:.1f} A; continuous load {need:.1f} A."


def r_receiver_supply(F):
    v = F.get("receiver")
    if v is None:
        return False, "No receiver: no part of kind `receiver` and no combined ESC/receiver."
    rid, powered = v
    return powered, f"Receiver `{rid}` " + ("is powered (wired to an ESC/BEC or integrated)." if powered else "has no wire to an ESC/BEC or battery.")


def r_failsafe(F):
    fs, unlinked = F.get("failsafe"), F.get("escs_unlinked")
    if not fs:
        return False, "`electronics.failsafe` is not declared."
    if unlinked:
        return False, "ESC(s) not driven from the receiver, so its failsafe cannot stop them: " + ", ".join(unlinked) + "."
    return True, "Failsafe declared and every ESC takes its signal from the receiver."


def r_indicator(F):
    v = F.get("indicator")
    if v is None:
        return False, "No power indicator LED (a part with `led` in its id/label or `electronics.indicator`)."
    lid, visible = v
    if visible is None:
        return True, f"Indicator `{lid}` declared (not a modelled part, visibility not judged)."
    return visible, f"Indicator `{lid}` " + ("can be seen from outside." if visible else "is hidden behind opaque parts.")


def r_battery_weapon_gap(F):
    v = F.get("battery_weapon_gap_mm")
    if v is None:
        return True if F.get("no_weapon") else None, "No spinning weapon." if F.get("no_weapon") else "battery or weapon not modelled"
    return v >= 3.0, f"Battery is {v:.1f} mm from the weapon's swept volume (need >= 3 mm plus a wall)."


def r_battery_shielded(F):
    v = F.get("battery_shielded")
    if v is None:
        return True if F.get("no_weapon") else None, "No spinning weapon." if F.get("no_weapon") else "battery or weapon not modelled"
    return v, "A structural wall " + ("sits" if v else "does NOT sit") + " between the battery and the weapon."


def r_battery_floor(F):
    v = F.get("battery_floor")
    if v is None:
        return None, "battery not modelled"
    gap, covered = v
    return covered and gap >= 0.5, f"Battery underside is {gap:.1f} mm above the floor and {'is' if covered else 'is NOT'} covered by structure below."


def r_battery_removable(F):
    v = F.get("battery_removal")
    if v is None:
        return None, "battery not modelled"
    good, why = v
    return good, why


def r_wire_bend_radius(F):
    v = F.get("bends")
    if v is None:
        return None, "no wire routes (run deep)"
    if not v:
        return True, "No routed wire bends tighter than 2x its diameter."
    return "warn", "Tight bends: " + "; ".join(f"`{w}` {rr:.1f} mm radius (min {m:.1f})" for w, rr, m in v) + "."


def r_wire_rotating_clearance(F):
    v = F.get("wire_rotating")
    if v is None:
        return None, "no wire routes (run deep)"
    if not v:
        return True, "Every routed wire stays >= 2 mm from rotating parts."
    return False, "Wires near rotating parts: " + "; ".join(f"`{w}` {d:.1f} mm from `{b}`" for w, b, d in v) + "."


def r_strain_relief(F):
    v = F.get("strain")
    if v is None:
        return None, "no wires"
    if not v:
        return True, "Wires at the ESC/battery have slack and the parts are retained."
    return "warn", "Missing strain relief: " + "; ".join(v) + "."


def r_cells_consistent(F):
    v = F.get("cells_sources")
    if not v:
        return None, "no cell count anywhere"
    vals = set(v.values())
    return len(vals) == 1, "Cell counts: " + ", ".join(f"{k} {x:g}S" for k, x in v.items()) + "."


def r_switch_in_series(F):
    v = F.get("bypass")
    if v is None:
        return None, "no battery or no power wires"
    if v:
        return False, "Loads reach the battery without passing the switch: " + ", ".join(v) + "."
    return True, "Every ESC is powered through the switch."


def r_power_path(F):
    v = F.get("unpowered")
    if v is None:
        return None, "no wires"
    if v:
        return False, "Not connected: " + "; ".join(v) + "."
    return True, "Every ESC has battery power and every motor is wired to an ESC."


def r_battery_c_rating(F):
    v = F.get("battery_cont")
    if v is None:
        return None, "battery capacity/C rating or load current unknown"
    max_a, need = v
    return need <= max_a, f"Continuous load {need:.1f} A against {max_a:.1f} A (capacity x C)."


def r_runtime(F):
    v = F.get("runtime_min")
    if v is None:
        return None, "battery capacity or load current unknown"
    return v >= MIN_RUNTIME_MIN, f"Estimated runtime {v:.1f} min at match duty (need >= {MIN_RUNTIME_MIN:g} min)."


def r_wire_gauge_declared(F):
    v = F.get("no_awg")
    if v is None:
        return None, "no wires"
    return not v, ("Power/motor wires without `awg`: " + ", ".join(v) + ".") if v else "Every power and motor wire declares its gauge."


def r_parts_retained(F):
    v = F.get("loose")
    if v is None:
        return None, "no electronics"
    return ("warn" if v else True), ("Not retained: " + ", ".join(v) + ".") if v else "Battery, ESCs and receiver declare how they are held."


def r_weapon_disable(F):
    if not F.get("armed"):
        return True, "No active weapon."
    return bool(F.get("weapon_remote_disable")), "Weapon remote disable " + ("declared." if F.get("weapon_remote_disable") else "NOT declared.")


RULES = {
    "drive_motor_voltage": (BLOCKER, "Drive motors suit the pack voltage", "Use fewer cells or motors rated for the pack.", r_drive_motor_voltage),
    "weapon_motor_voltage": (BLOCKER, "Weapon motor suits the pack voltage", "Use a motor rated for the cell count (or add `ratings.max_cells`).", r_weapon_motor_voltage),
    "esc_voltage": (BLOCKER, "ESCs rated for the pack voltage", "Use ESCs rated for the cell count.", r_esc_voltage),
    "esc_drive_current": (BLOCKER, "Drive ESC covers motor stall", "Use an ESC whose burst rating covers the drive motor stall current.", r_esc_drive_current),
    "esc_weapon_current": (BLOCKER, "Weapon ESC covers motor current", "Use a bigger weapon ESC or a weaker motor.", r_esc_weapon_current),
    "wire_ampacity": (WARNING, "Wire gauge carries the current", "Use a thicker wire (lower AWG).", r_wire_ampacity),
    "connector_rating": (WARNING, "Battery connector rating", "Use a connector rated for the peak current.", r_connector_rating),
    "switch_rating": (WARNING, "Switch rating", "Use a switch rated for the load (e.g. a 15 A robot switch).", r_switch_rating),
    "receiver_supply": (BLOCKER, "Receiver is powered", "Wire the receiver to an ESC with a BEC.", r_receiver_supply),
    "failsafe": (WARNING, "Failsafe covers every ESC", "Declare failsafe and drive every ESC from the receiver.", r_failsafe),
    "indicator": (WARNING, "Power light visible", "Add an LED that shows power, visible from outside.", r_indicator),
    "battery_weapon_gap": (BLOCKER, "Battery clear of the weapon", "Move the battery >= 3 mm from the swept volume.", r_battery_weapon_gap),
    "battery_shielded": (WARNING, "Wall between battery and weapon", "Put a structural wall between them.", r_battery_shielded),
    "battery_floor": (WARNING, "Battery protected from below", "Put floor structure under the battery, >= 0.5 mm above the ground.", r_battery_floor),
    "battery_removable": (WARNING, "Battery comes out without the weapon", "Give the battery a lid that does not carry weapon parts.", r_battery_removable),
    "wire_bend_radius": (WARNING, "Wire bend radius", "Give the wires room to bend (>= 2x diameter).", r_wire_bend_radius),
    "wire_rotating_clearance": (BLOCKER, "Wires clear of rotating parts", "Route wires >= 2 mm from wheels, pulleys, belts and the weapon.", r_wire_rotating_clearance),
    "strain_relief": (WARNING, "Strain relief at ESC and battery", "Give wires slack (`slack_mm` >= 3) and retain the parts.", r_strain_relief),
    "cells_consistent": (BLOCKER, "Cell count consistent", "Make electronics.cells, the battery and weapon.cells agree.", r_cells_consistent),
    "switch_in_series": (BLOCKER, "Switch cuts all power", "Route every power wire through the switch.", r_switch_in_series),
    "power_path": (BLOCKER, "Power path complete", "Wire every ESC to power and every motor to an ESC.", r_power_path),
    "battery_c_rating": (WARNING, "Battery continuous rating", "Use a bigger or higher-C pack.", r_battery_c_rating),
    "runtime": (WARNING, "Runtime covers a match", "Use a bigger pack or lower the load.", r_runtime),
    "wire_gauge_declared": (WARNING, "Wire gauges declared", "Give every power/motor wire an `awg`.", r_wire_gauge_declared),
    "parts_retained": (WARNING, "Electronics retained", "Declare `retained` for the battery, ESCs and receiver.", r_parts_retained),
    "weapon_disable": (BLOCKER, "Weapon can be disabled remotely", "Declare `electronics.weapon_remote_disable` with a weapon ESC on the receiver.", r_weapon_disable),
}


def evaluate(F):
    return [(rid, *RULES[rid][3](F)) for rid in RULES]


# ------------------------------------------------------------------------------------------------------------- facts


def _is_receiver(rp):
    if rp.part.kind == "receiver":
        return True
    text = " ".join(str(x or "") for x in (rp.part.catalog, rp.part.label, rp.cat.name if rp.cat else "")).lower()
    return rp.part.kind == "esc" and ("receiver" in text or "rx" in rp.part.id)


def facts(ctx) -> dict:
    r, w = ctx.r, ctx.world
    spec = r.spec
    F = {}
    parts = {rp.part.id: rp for rp in r.parts}
    bats = [rp for rp in r.parts if rp.part.kind == "battery"]
    bat = bats[0] if bats else None
    cells = cap = crate = None
    srcs = {}
    if bat is not None:
        p = ratings(bat)
        cid = (bat.part.catalog or "") + " " + (bat.cat.name if bat.cat else "")
        cells = p.get("cells") or _parse(cid, r"(?<![a-z0-9])(\d)s(?:\b|_)")
        cap = p.get("capacity_mah") or _parse(cid, r"(\d+)\s*_?mah")
        crate = p.get("c_rating") or _parse(cid, r"(\d+)\s*c\b")
        if cells is not None:
            srcs["battery"] = float(cells)
    if spec.electronics.cells is not None:
        srcs["electronics.cells"] = float(spec.electronics.cells)
        cells = cells if cells is not None else float(spec.electronics.cells)
    for rp in r.parts:
        if rp.part.weapon is not None and rp.part.weapon.cells is not None:
            srcs[f"{rp.part.id}.weapon.cells"] = float(rp.part.weapon.cells)
    F["cells_sources"] = srcs
    F["cells"] = float(cells) if cells is not None else None
    F["v_nom"] = 3.7 * F["cells"] if cells is not None else None
    drive = {rp.part.id: {"nominal_v": ratings(rp).get("nominal_v"), "i": ratings(rp).get("stall_current_a")}
             for rp in r.parts if rp.part.kind == "motor"}
    wpn = {rp.part.id: {"max_cells": ratings(rp).get("max_cells"), "i": ratings(rp).get("max_current_a"),
                        "typ": ratings(rp).get("typ_current_a", ratings(rp).get("max_current_a"))}
           for rp in r.parts if rp.part.kind == "weapon_motor"}
    F["drive_motors"], F["weapon_motors"] = drive, wpn
    # graph from wires
    wires = list(spec.wires)
    adj = {}
    for wi in wires:
        a, b = _end(wi.__dict__.get("from", ""))[0], _end(wi.to)[0]
        adj.setdefault(a, set()).add(b)
        adj.setdefault(b, set()).add(a)
    escs = {}
    for rp in r.parts:
        if rp.part.kind != "esc":
            continue
        p = ratings(rp)
        nb = adj.get(rp.part.id, set())
        escs[rp.part.id] = {
            "max_cells": p.get("max_cells", p.get("cells")), "cont_a": p.get("cont_current_a"), "burst_a": p.get("burst_current_a"),
            "loads_drive": {m: drive[m]["i"] for m in nb if m in drive},
            "loads_weapon": {m: wpn[m]["i"] for m in nb if m in wpn}}
    F["escs"] = escs

    def esc_load(e, cont=True):
        d = escs[e]
        vals = list(d["loads_drive"].values()) + [wpn[m]["typ" if cont else "i"] for m in d["loads_weapon"]]
        return None if any(v is None for v in vals) else sum(vals)

    loads = [esc_load(e) for e in escs]
    total_cont = None if any(v is None for v in loads) else sum(loads) + 0.2
    peaks = [esc_load(e, False) for e in escs]
    total_peak = None if any(v is None for v in peaks) else sum(peaks) + 0.2
    # wire currents
    wc, no_awg = {}, []
    for wi in wires:
        a, b = _end(wi.__dict__.get("from", ""))[0], _end(wi.to)[0]
        if wi.kind in ("power", "motor") and wi.awg is None:
            no_awg.append(wi.id)
        if wi.kind == "signal":
            i = 0.1
        elif wi.kind == "motor":
            m = a if a in drive or a in wpn else b
            i = drive[m]["i"] if m in drive else (wpn[m]["typ"] if m in wpn else None)
        else:
            e = a if a in escs else (b if b in escs else None)
            i = esc_load(e) if e is not None else total_cont
        wc[wi.id] = (wi.awg, i)
    if wires:
        F["wire_currents"] = wc
        F["no_awg"] = no_awg
    # connector
    if bat is not None and total_peak is not None:
        ports = list((bat.cat.ports if bat.cat else {}) or {}) + list(bat.part.ports or {})
        if ports:
            name = ports[0]
            F["connector"] = (name, ratings(bat).get("connector_a", CONNECTOR_A.get(name.lower())), total_peak)
    sw = next((rp for rp in r.parts if rp.part.kind == "switch"), None)
    if sw is not None:
        F["switch"] = (sw.part.id, ratings(sw).get("current_a"), total_cont)
    # receiver
    rx = next((rp for rp in r.parts if _is_receiver(rp)), None)
    if rx is not None:
        supply = ({bat.part.id} if bat else set()) | ({sw.part.id} if sw else set())
        nb = adj.get(rx.part.id, set())
        powered = bool(nb & supply) if rx.part.kind == "esc" else bool(nb & (set(escs) | supply))
        F["receiver"] = (rx.part.id, bool(powered))
        F["escs_unlinked"] = [e for e in escs if e != rx.part.id and rx.part.id not in adj.get(e, set())]
    else:
        F["escs_unlinked"] = list(escs)
    F["failsafe"] = bool(spec.electronics.failsafe)
    F["armed"] = any(p.kind == "weapon" and p.weapon is not None and p.weapon.kind not in ("none", "wedge") for p in spec.parts)
    F["weapon_remote_disable"] = bool(spec.electronics.weapon_remote_disable)
    # power path
    if wires:
        un = []
        pw = {}
        for wi in wires:
            if wi.kind == "power":
                a, b = _end(wi.__dict__.get("from", ""))[0], _end(wi.to)[0]
                pw.setdefault(a, set()).add(b)
                pw.setdefault(b, set()).add(a)
        if bat is not None:
            reach, todo = {bat.part.id}, [bat.part.id]
            while todo:
                c = todo.pop()
                for n in pw.get(c, ()):
                    if n not in reach:
                        reach.add(n)
                        todo.append(n)
            un += [f"ESC `{e}` has no power wire path to the battery" for e in escs if e not in reach]
            if sw is not None:
                reach2, todo = {bat.part.id}, [bat.part.id]
                while todo:
                    c = todo.pop()
                    for n in pw.get(c, ()):
                        if n not in reach2 and n != sw.part.id:
                            reach2.add(n)
                            todo.append(n)
                F["bypass"] = [f"`{e}`" for e in escs if e in reach2]
            else:
                F["bypass"] = ["no switch part at all"]
        else:
            un.append("no battery")
        for m in list(drive) + list(wpn):
            if not (adj.get(m, set()) & set(escs)):
                un.append(f"motor `{m}` has no wire to an ESC")
        F["unpowered"] = un
    # battery capacity
    if cap and crate and total_cont is not None:
        F["battery_cont"] = (cap / 1000.0 * crate, total_cont)
    if cap and drive is not None:
        di = [d["i"] for d in drive.values()]
        wi_ = [d["typ"] for d in wpn.values()]
        if all(v is not None for v in di + wi_):
            avg = 0.3 * sum(di) + 0.5 * sum(wi_) + 0.1
            F["runtime_min"] = cap / 1000.0 * 0.8 / avg * 60.0
    # strain relief and retention
    if wires:
        st = []
        for wi in wires:
            ends = {_end(wi.__dict__.get("from", ""))[0], _end(wi.to)[0]}
            if ends & (set(escs) | ({bat.part.id} if bat else set())) and (wi.slack_mm is None or wi.slack_mm < 3.0):
                st.append(f"`{wi.id}` slack {wi.slack_mm if wi.slack_mm is not None else 'undeclared'}")
        F["strain"] = st
    elec = [rp for rp in r.parts if rp.part.kind in ("battery", "esc", "receiver")]
    if elec:
        F["loose"] = [rp.part.id for rp in elec if rp.part.retained is None and rp.part.parent is None]
    # indicator
    led = next((rp for rp in r.parts if "led" in rp.part.id.lower() or "led" in str(rp.part.label or "").lower().split()), None)
    if led is not None:
        b = w.body(led.part.id)
        F["indicator"] = (led.part.id, _visible(r, w, b) if b is not None else None)
    elif spec.electronics._extra.get("indicator"):
        F["indicator"] = (str(spec.electronics._extra["indicator"]), None)
    # geometry: battery vs weapon / floor / removal
    _battery_geom(ctx, F, bat)
    _routes(ctx, F)
    return F


def _visible(r, w, b):
    """Seen from outside along some axis: nothing in the way, or only clear (polycarbonate) parts."""
    others = [x for x in w.bodies if x is not b and not x.is_wire]
    clear = {rp.part.id for rp in r.parts if str(rp.part.material or "").lower() in CLEAR}
    sc = measure.Scene([x for x in others if x.id not in clear])
    for d in np.vstack([np.eye(3), -np.eye(3)]):
        dist, _ = sc.first_hit(b.center[None], d[None])
        if np.isinf(dist[0]):
            return True
    return False


def _weapon(ctx):
    w, r = ctx.world, ctx.r
    for i, b in enumerate(w.bodies):
        if b.part_idx is not None and b.kind == "weapon":
            sa = spin_axis(w, r, i)
            if sa is not None:
                o, a = sa
                return b, o, a, rim_radius(b, o, a), float(np.abs((b.mesh.vertices - o) @ a).max())
    return None


def _battery_geom(ctx, F, bat):
    w, r = ctx.world, ctx.r
    wp = _weapon(ctx)
    if wp is None:
        F["no_weapon"] = True
    if bat is None:
        return
    bb = w.body(bat.part.id)
    if bb is None:
        return
    lo, hi = bb.aabb
    if wp is not None:
        wb, o, a, R, half = wp
        P = bb.surface(1.0)[0]
        q = P - o
        ax = np.abs(q @ a)
        rad = np.linalg.norm(q - np.outer(q @ a, a), axis=1)
        dr, da = rad - R, ax - half
        d = np.where((dr > 0) & (da > 0), np.hypot(dr, da), np.maximum(dr, da))
        F["battery_weapon_gap_mm"] = float(d.min())
        walls = [b for b in w.bodies if b.kind in ("structure", "armor", "plate", "fork") and not b.fastener and b is not wb]
        sc = measure.Scene(walls)
        dvec = o - bb.center
        L = float(np.linalg.norm(dvec))
        dist, _ = sc.first_hit(bb.center[None], (dvec / max(L, 1e-9))[None])
        F["battery_shielded"] = bool(dist[0] < max(L - R, 0.0))
    floor = ctx.metrics.get("ground_z")
    if floor is None:
        zs = [float(b.aabb[0][2]) for b in w.bodies if not b.fastener and not b.is_wire]
        floor = min(zs)
    if r.spec.ground_z is not None:
        floor = float(r.spec.ground_z)
    below = [b for b in w.bodies if b.kind in ("structure", "armor", "plate") and not b.fastener]
    sc = measure.Scene(below)
    c = bb.center
    O = np.array([[x, y, lo[2] + 0.01] for x in (lo[0] + 1, c[0], hi[0] - 1) for y in (lo[1] + 1, c[1], hi[1] - 1)])
    dist, _ = sc.first_hit(O, np.tile([0, 0, -1.0], (len(O), 1)))
    F["battery_floor"] = (float(lo[2] - floor), bool(np.isfinite(dist).all()))
    # removal: up or down path must not pass weapon assembly parts
    from .archetype import _ancestors, _descendants, rotor_set
    spec = r.spec
    asm = set()
    if wp is not None:
        wid = wp[0].id
        asm = rotor_set(spec, wid) | set(_ancestors(spec, wid))
        for x in list(asm):
            asm |= _descendants(spec, x)
        wpart = spec.part(wid)
        if wpart.weapon and wpart.weapon.motor:
            asm.add(wpart.weapon.motor)
        asm.add(wid)
    others = [b for b in w.bodies if b is not bb and not b.is_wire and not b.fastener]
    res = []
    for d in ([0, 0, 1.0], [0, 0, -1.0]):
        hits = set()
        for b in others:
            blo, bhi = b.aabb
            if d[2] > 0 and blo[2] < hi[2] - 0.1:
                continue
            if d[2] < 0 and bhi[2] > lo[2] + 0.1:
                continue
            if blo[0] < hi[0] - 0.5 and bhi[0] > lo[0] + 0.5 and blo[1] < hi[1] - 0.5 and bhi[1] > lo[1] + 0.5:
                hits.add(b.id)
        bad = sorted(hits & asm)
        res.append((not bad, "up" if d[2] > 0 else "down", sorted(hits), bad))
    good = [x for x in res if x[0]]
    if good:
        g = good[0]
        F["battery_removal"] = (True, f"Battery comes out {g[1]} past {', '.join(f'`{h}`' for h in g[2]) or 'nothing'}; no weapon part in the way.")
    else:
        F["battery_removal"] = (False, "Both ways out of the battery bay pass weapon parts: " + "; ".join(f"{x[1]}: {', '.join(x[3])}" for x in res) + ".")


def _routes(ctx, F):
    routes = ctx.routes
    if not routes:
        if ctx.r.spec.wires:
            return
        F["bends"], F["wire_rotating"] = [], []
        return
    bends = []
    for rt in routes:
        P = np.asarray(rt.points, float)
        if len(P) < 3:
            continue
        seg = np.linalg.norm(np.diff(P, axis=0), axis=1)
        s = np.concatenate([[0], np.cumsum(seg)])
        L = s[-1]
        step = max(3.0, 2.5 * rt.od_mm)
        if L < 2 * step:
            continue
        ts = np.arange(0, L + 1e-9, step / 2)
        Q = np.array([[np.interp(t, s, P[:, k]) for k in range(3)] for t in ts])
        worst = math.inf
        for k in range(2, len(Q) - 2):
            a, b, c = Q[k - 2], Q[k], Q[k + 2]
            ab, bc, ca = np.linalg.norm(b - a), np.linalg.norm(c - b), np.linalg.norm(a - c)
            area = np.linalg.norm(np.cross(b - a, c - a)) / 2
            if area > 1e-6:
                worst = min(worst, ab * bc * ca / (4 * area))
        lim = 2.0 * rt.od_mm
        if worst < lim:
            bends.append((rt.id, worst, lim))
    F["bends"] = bends
    w = ctx.world
    rot = [b for b in w.bodies if b.kind in ROTATING and not b.fastener]
    near = []
    wp = _weapon(ctx)
    for rt in routes:
        P = np.asarray(rt.points, float)
        if len(P) == 0:
            continue
        rr = rt.od_mm / 2
        for b in rot:
            if b.kind == "weapon" and wp is not None and b is wp[0]:
                _, o, a, R, half = wp
                q = P - o
                ax = np.abs(q @ a)
                rad = np.linalg.norm(q - np.outer(q @ a, a), axis=1)
                dr, da = rad - R, ax - half
                d = float(np.where((dr > 0) & (da > 0), np.hypot(dr, da), np.maximum(dr, da)).min()) - rr
            else:
                lo, hi = b.aabb
                if not (np.all(P.max(0) >= lo - 3) and np.all(P.min(0) <= hi + 3)):
                    continue
                m = np.all((P >= lo - 3) & (P <= hi + 3), axis=1)
                if not m.any():
                    continue
                d = float(b.distance(P[m]).min()) - rr
            if d < 2.0:
                near.append((rt.id, b.id, d))
    F["wire_rotating"] = near


# ------------------------------------------------------------------------------------------------------------- run


def run(ctx):
    F = facts(ctx)
    out = []
    for rid, passed, msg in evaluate(F):
        sev, title, hint, _ = RULES[rid]
        fid = f"electrical.{rid}"
        if passed is None:
            ctx.not_checked.append(f"Electrical `{rid}`: {msg}")
            out.append(fail(fid, G, WARNING, f"Not checked: {title}", f"Could not evaluate ({msg}).")
                       .fix("Add the rating to the catalog entry or a `ratings` table on the part."))
        elif not isinstance(passed, str) and bool(passed):
            out.append(ok(fid, G, title, msg))
        else:
            out.append(fail(fid, G, WARNING if passed == "warn" else sev, title, msg).fix(hint))
    for k in ("runtime_min", "battery_weapon_gap_mm"):
        if F.get(k) is not None:
            ctx.metrics[f"electrical.{k}"] = float(F[k])
    return out
