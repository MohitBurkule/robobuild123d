"""Electrical and weapon numbers: tip speed, stored energy, ESC and battery limits (port of power.rs)."""

from __future__ import annotations

import math

import numpy as np

from .. import catalog, geom, xform
from ..finding import BLOCKER, WARNING, fail, ok

G = "power"


def spin_axis(w, r, i):
    """(origin, unit axis) of a weapon body in the world: its placement origin and `weapon.spin_axis` (default local Z)."""
    b = w.bodies[i]
    if b.part_idx is None:
        return None
    wd = r.parts[b.part_idx].part.weapon
    if wd is None:
        return None
    local = np.asarray(wd.spin_axis if wd.spin_axis is not None else [0.0, 0.0, 1.0], float)
    return b.M[:3, 3].copy(), xform.norm(xform.apply_dir(b.M, local))


def rim_radius(body, origin, axis) -> float:
    q = body.mesh.vertices - origin
    perp = q - np.outer(q @ axis, axis)
    return float(np.linalg.norm(perp, axis=1).max()) if len(q) else 0.0


def run(ctx):
    r, w = ctx.r, ctx.world
    out = []
    cells = r.spec.electronics.cells
    if cells is None:
        cells = next((rp.cat.props.get("cells") for rp in r.parts if rp.cat is not None and rp.cat.kind == "battery"
                      and rp.cat.props.get("cells") is not None), None)
    cells = float(cells if cells is not None else 2.0)
    weapon_current = 0.0
    spinups = []  # (part id, stored energy J at fighting speed, typical current A) per weapon, for the runtime estimate
    missing_current = []  # motors whose current draw is unknown: the peak is then a lower bound, never a pass
    for rp in r.parts:
        if rp.part.kind != "weapon" or rp.part.weapon is None:
            continue
        pid, wd = rp.part.id, rp.part.weapon
        i = w.index(pid)
        if i is None:
            ctx.not_checked.append(f"Weapon `{pid}` tip speed and energy: it has no body in the world")
            continue
        motor = next((m for m in r.parts if wd.motor is not None and m.part.id == wd.motor), None)
        kv = motor.cat.props.get("kv") if motor is not None and motor.cat is not None else None
        if kv is None:
            out.append(fail("power.weapon_motor", G, BLOCKER, "Weapon has no motor with a known kV",
                            f"`{pid}` names motor {wd.motor!r}; it must be a catalog brushless motor so speed can be computed.")
                       .on(pid).fix("Set `weapon.motor` to a `weapon_motor` part that uses a catalog entry with kV."))
            continue
        mc = motor.cat.props.get("max_current_a")
        if mc is None:
            missing_current.append(motor.part.id)
        else:
            weapon_current += float(mc)
        ratio = max(float(wd.reduction if wd.reduction is not None else 1.0), 0.01)
        wcells = float(wd.cells if wd.cells is not None else cells)
        rpm = r.profile.max_cell_v * wcells * float(kv) / ratio  # AWS 5e: no-load speed
        sa = spin_axis(w, r, i)
        if sa is None:
            ctx.not_checked.append(f"Weapon `{pid}` tip speed: no spin axis")
            continue
        origin, axis = sa
        rmax = rim_radius(w.bodies[i], origin, axis)
        tip = rpm * (2.0 * rmax) * math.pi * 60.0 / 1_609_344.0
        ctx.metrics["tip_speed_mph"] = tip
        ctx.metrics["weapon_rpm"] = rpm
        limit = r.profile.max_tip_speed_mph
        if tip > limit:
            out.append(fail("power.tip_speed", G, BLOCKER, "Weapon tip is too fast",
                            f"{rpm:.0f} rpm at {2 * rmax:.0f} mm diameter gives {tip:.0f} mph at the tip; the limit is {limit:.0f} mph.")
                       .on(pid).expect(f"<= {limit:.0f} mph", f"{tip:.0f} mph")
                       .fix("Add a reduction (`weapon.reduction` above 1), fit a lower kV motor, use fewer cells or a smaller disc."))
        else:
            out.append(ok("power.tip_speed", G, "Tip speed is legal", f"{rpm:.0f} rpm at {2 * rmax:.0f} mm diameter is {tip:.0f} mph (limit {limit:.0f})."))
        dens = catalog.density(rp.part.material)
        if dens is None:
            ctx.not_checked.append(f"Weapon `{pid}` stored energy: no material density")
            continue
        b = w.bodies[i]
        iner = geom.axial_inertia(b.geom, b.M, origin, axis) * dens * 1e-3 * 1e-9  # kg m2
        # the rest of the rotating stack (second disc, spacer, hub, shaft, rotor nuts) stores energy too
        from .archetype import rotor_set
        for oid in sorted(rotor_set(r.spec, pid) - {pid}):
            ob, orp = w.body(oid), next((q for q in r.parts if q.part.id == oid), None)
            if ob is None or orp is None or ob.fastener:
                continue
            od = catalog.density(orp.part.material) if orp.part.material else None
            if od is None:
                continue
            sf = float(orp.part.solid_fraction) if orp.part.solid_fraction else 1.0
            iner += geom.axial_inertia(ob.geom, ob.M, origin, axis) * od * sf * 1e-3 * 1e-9
        omega = rpm * 0.85 * 2.0 * math.pi / 60.0
        energy = 0.5 * iner * omega * omega
        ctx.metrics["weapon_energy_j"] = energy
        spinups.append((pid, energy, motor.cat.props.get("typ_current_a", mc)))
        if energy < 3.0:
            out.append(fail("power.weapon_energy", G, WARNING, "Weapon stores very little energy",
                            f"About {energy:.1f} J at 85% of no-load speed; competitive ant spinners store 10 to 50 J. It will bounce off armour.")
                       .on(pid).fix("Make the weapon heavier toward the rim, larger, or spin it faster (within the tip speed limit)."))
        else:
            out.append(ok("power.weapon_energy", G, "Weapon stores useful energy", f"About {energy:.1f} J at 85% of no-load speed."))
    bat_rp = next((rp for rp in r.parts if rp.part.kind == "battery"), None)
    if bat_rp is not None and bat_rp.cat is None:
        ctx.not_checked.append(f"Battery `{bat_rp.part.id}` current rating: not a catalog battery")
    if bat_rp is not None and bat_rp.cat is not None:
        bp = bat_rp.cat.props
        mah, c = float(bp.get("capacity_mah", 0.0) or 0.0), float(bp.get("c_rating", 0.0) or 0.0)
        max_a = mah / 1000.0 * c
        # Peak = every drive motor stalled (pushing match, wheels blocked) plus the weapon at its rated maximum.
        drive = 0.0
        for rp in r.parts:
            if rp.part.kind != "motor":
                continue
            sc = rp.cat.props.get("stall_current_a") if rp.cat is not None else None
            if sc is None:
                missing_current.append(rp.part.id)
            else:
                drive += float(sc)
        peak = drive + weapon_current
        ctx.metrics["peak_current_a"] = peak
        if missing_current:
            ids = ", ".join(f"`{x}`" for x in missing_current)
            out.append(fail("power.current_unknown", G, WARNING, "Motor current draw unknown",
                            f"{ids} {'has' if len(missing_current) == 1 else 'have'} no stall or maximum current in the catalog; "
                            f"the {peak:.1f} A peak leaves {'it' if len(missing_current) == 1 else 'them'} out.")
                       .on(*missing_current).fix("Use catalog motors with a stall current (drive) or max current (weapon)."))
            ctx.not_checked.append(f"Battery peak current: no current data for {', '.join(missing_current)}")
        if max_a > 0 and peak > max_a:
            out.append(fail("power.battery", G, WARNING, "Battery may sag under peak load",
                            f"Estimated peak {peak:.1f} A against a {max_a:.1f} A rating ({_n(mah)} mAh x {_n(c)} C); the voltage will collapse in a hit.")
                       .fix("Use a bigger or higher-C pack, or a motor that draws less."))
        elif max_a > 0 and not missing_current:
            out.append(ok("power.battery", G, "Battery covers peak current", f"Peak {peak:.1f} A within the {max_a:.1f} A rating."))
        elif max_a <= 0:
            ctx.not_checked.append(f"Battery `{bat_rp.part.id}` current rating: catalog has no capacity or C rating")
    out += runtime(ctx, bat_rp, cells, spinups)
    for esc in r.parts:
        if esc.part.kind != "esc" or esc.cat is None:
            continue
        cont = float(esc.cat.props.get("cont_current_a", 0.0) or 0.0)
        if cont > 0 and weapon_current > cont * 1.6 and "brushless" in esc.cat.id:
            out.append(fail("power.esc", G, WARNING, "ESC is small for this motor",
                            f"`{esc.part.id}` is rated {cont:.0f} A continuous but the weapon motor can draw {weapon_current:.0f} A.")
                       .on(esc.part.id).fix("Use a bigger ESC or a weaker motor."))
    return out


# Match duty cycle (per motor) for the runtime estimate. Drive: pushing or stalled 15% of the time, cruising at about a
# third of stall current 50%, idle the rest. Weapon: one full spin-up from rest every SPINUP_EVERY_S (each big hit or
# flip dumps most of the stored energy), held at speed against windage and bearing drag at HOLD_FRAC of its typical
# current while powered, coasting with the throttle off WEAPON_COAST of the match. Spin-up charge comes from the stored
# energy, not a current guess: Q = E / (eta * V).
# Calibrated against a real fighting robot (2026-10 reference audit): RVRN/Revron, 150 g BE1806 drisk + 2x N10, wins
# 3 min UK antweight fights on a 2S 180 mAh pack. The old weapon hold (40% of the motor's 8 A typical current, throttle on
# 80% of the match) alone came to ~130 mAh, which said that robot cannot finish a fight. Measured antweight practice: a
# 1806-class outrunner holding a ~30 g rotor at speed draws ~1.5 A (windage + bearings, = 20% of typical current), and
# drivers have the weapon off or coasting about half the match (after self-hits, while repositioning, pinned, between
# exchanges). Drive and spin-up terms were already in line with logged antweight packs and are kept.
DRIVE_PUSH, DRIVE_CRUISE, DRIVE_CRUISE_FRAC = 0.15, 0.50, 0.35
SPINUP_EVERY_S, SPINUP_EFF, HOLD_FRAC, WEAPON_COAST = 10.0, 0.6, 0.2, 0.5
ELEC_A = 0.1  # receiver, ESC logic, LED
USABLE = 0.8  # never run a LiPo below about 20% left


def runtime(ctx, bat_rp, cells, spinups):
    r = ctx.r
    fight = float(r.profile.fight_s)
    need = fight * float(r.profile.runtime_margin)
    if bat_rp is None:
        ctx.not_checked.append("Battery runtime: no battery part")
        return []
    mah = float((bat_rp.cat.props.get("capacity_mah") if bat_rp.cat is not None else None) or 0.0)
    if mah <= 0:
        ctx.not_checked.append(f"Battery runtime: `{bat_rp.part.id}` has no catalog capacity")
        return [fail("power.runtime", G, WARNING, "Not checked: battery runtime", f"`{bat_rp.part.id}` has no capacity (mAh) in the catalog.")
                .on(bat_rp.part.id).fix("Use a catalog battery with `capacity_mah`.")]
    v = 3.7 * cells
    unknown = []
    drive_a = 0.0
    for rp in r.parts:
        if rp.part.kind != "motor":
            continue
        pr = rp.cat.props if rp.cat is not None else {}
        sc = pr.get("stall_current_a")
        if sc is None:
            unknown.append(rp.part.id)
            continue
        nl = float(pr.get("no_load_current_a") or 0.0)
        drive_a += DRIVE_PUSH * float(sc) + DRIVE_CRUISE * max(DRIVE_CRUISE_FRAC * float(sc), nl)
    weapon_c = 0.0  # coulombs per fight
    for pid, energy, typ in spinups:
        if typ is None:
            unknown.append(pid)
            continue
        weapon_c += (fight / SPINUP_EVERY_S) * energy / (SPINUP_EFF * v)
        weapon_c += HOLD_FRAC * float(typ) * fight * (1.0 - WEAPON_COAST)
    for rp in r.parts:  # a weapon whose energy could not be computed is not in spinups
        if rp.part.kind == "weapon" and rp.part.weapon is not None and rp.part.weapon.kind in ("spinner", "drum", "disc", "bar") \
                and rp.part.id not in {s[0] for s in spinups} and rp.part.id not in unknown:
            unknown.append(rp.part.id)
    if unknown:
        ctx.not_checked.append(f"Battery runtime: no current or energy data for {', '.join(unknown)}")
        return [fail("power.runtime", G, WARNING, "Not checked: battery runtime",
                     f"No current or stored-energy figure for {', '.join(f'`{x}`' for x in unknown)}, so the match draw is unknown.")
                .on(bat_rp.part.id, *unknown).fix("Use catalog motors with stall/typical current and give the weapon a material.")]
    used_c = drive_a * fight + weapon_c + ELEC_A * fight
    usable_c = mah / 1000.0 * 3600.0 * USABLE
    run_s = usable_c / used_c * fight
    ctx.metrics["runtime_min"] = run_s / 60.0
    used_mah = used_c / 3.6
    detail = (f"{_n(mah)} mAh x {USABLE:.0%} usable lasts about {run_s / 60:.1f} min of fighting "
              f"(per {fight / 60:g} min fight: drive {drive_a * fight / 3.6:.0f} mAh, weapon spin-ups and hold {weapon_c / 3.6:.0f} mAh, "
              f"electronics {ELEC_A * fight / 3.6:.0f} mAh = {used_mah:.0f} mAh).")
    if run_s < need:
        return [fail("power.runtime", G, BLOCKER, "Battery does not last the fight",
                     detail + f" A fight is {fight / 60:g} min and the pack must cover it with {r.profile.runtime_margin - 1:.0%} margin.")
                .on(bat_rp.part.id).expect(f">= {need / 60:.2f} min", f"{run_s / 60:.2f} min")
                .fix(f"Fit a pack of at least {used_mah * r.profile.runtime_margin / USABLE:.0f} mAh, or lower the load (smaller weapon, lower kV).")]
    return [ok("power.runtime", G, "Battery lasts the fight", detail)]


def _n(x):
    """Rust's f64 Display: integers print without a decimal point."""
    return str(int(x)) if float(x).is_integer() else repr(float(x))
