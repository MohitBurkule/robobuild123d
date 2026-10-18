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
        weapon_current += float(motor.cat.props.get("max_current_a", 0.0) or 0.0)
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
        omega = rpm * 0.85 * 2.0 * math.pi / 60.0
        energy = 0.5 * iner * omega * omega
        ctx.metrics["weapon_energy_j"] = energy
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
        drive = sum(float(rp.cat.props["stall_current_a"]) for rp in r.parts
                    if rp.part.kind == "motor" and rp.cat is not None and rp.cat.props.get("stall_current_a") is not None)
        peak = drive * 0.5 + weapon_current
        ctx.metrics["peak_current_a"] = peak
        if max_a > 0 and peak > max_a:
            out.append(fail("power.battery", G, WARNING, "Battery may sag under peak load",
                            f"Estimated peak {peak:.1f} A against a {max_a:.1f} A rating ({_n(mah)} mAh x {_n(c)} C); the voltage will collapse in a hit.")
                       .fix("Use a bigger or higher-C pack, or a motor that draws less."))
        elif max_a > 0:
            out.append(ok("power.battery", G, "Battery covers peak current", f"Peak {peak:.1f} A within the {max_a:.1f} A rating."))
        else:
            ctx.not_checked.append(f"Battery `{bat_rp.part.id}` current rating: catalog has no capacity or C rating")
    for esc in r.parts:
        if esc.part.kind != "esc" or esc.cat is None:
            continue
        cont = float(esc.cat.props.get("cont_current_a", 0.0) or 0.0)
        if cont > 0 and weapon_current > cont * 1.6 and "brushless" in esc.cat.id:
            out.append(fail("power.esc", G, WARNING, "ESC is small for this motor",
                            f"`{esc.part.id}` is rated {cont:.0f} A continuous but the weapon motor can draw {weapon_current:.0f} A.")
                       .on(esc.part.id).fix("Use a bigger ESC or a weaker motor."))
    return out


def _n(x):
    """Rust's f64 Display: integers print without a decimal point."""
    return str(int(x)) if float(x).is_integer() else repr(float(x))
