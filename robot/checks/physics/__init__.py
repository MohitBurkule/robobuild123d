"""Group `physics`: closed-form weapon / drive / power checks from geometry metrics + catalogue (no sim).

Runs after `power`, `dynamics` and `combat` and reuses their metrics (weapon_rpm, weapon_energy_j, peak_current_a, mass_total_g).
Every missing input goes to NOT CHECKED, never a silent pass. UNTESTED: written without running.
"""

from __future__ import annotations

import math

from ...finding import BLOCKER, WARNING, fail, ok
from . import formulas as F
from .limits import limit

G = "physics"
GCM_TO_NM = 9.80665e-5  # catalog `stall_torque_gcm` (g cm) -> N m


def _props(rp):
    return rp.cat.props if rp is not None and getattr(rp, "cat", None) is not None else {}


def _parts(r, kind):
    return [rp for rp in r.parts if rp.part.kind == kind]


def _wheel_geometry(ctx, m):
    """track_mm / wheel_d_mm from the world's wheel bodies (same method as dynamics._turn_rate); nothing if there are none."""
    try:
        wheels = [b for b in ctx.world.bodies if b.kind == "wheel" and not b.fastener]
    except Exception:  # noqa: BLE001 - no world / unexpected body shape: leave the metrics unset (NOT CHECKED)
        return
    if not wheels:
        return
    if "wheel_d_mm" not in m:
        m["wheel_d_mm"] = max(float(b.aabb[1][2] - b.aabb[0][2]) for b in wheels)
    xs = [float(b.center[0]) for b in wheels]
    if "track_mm" not in m and len(wheels) >= 2 and max(xs) - min(xs) >= 5.0:
        m["track_mm"] = max(xs) - min(xs)


def run(ctx):
    r, m = ctx.r, ctx.metrics
    prof = getattr(r, "profile", None)
    out = []
    mass_kg = float(m.get("mass_g", m.get("mass_total_g", 150.0))) / 1000.0
    _wheel_geometry(ctx, m)
    out += _weapon(ctx, r, m, prof, mass_kg)
    out += _power(ctx, r, m, prof)
    out += _drive(ctx, r, m, prof, mass_kg)
    out += _invert(ctx, r, m)
    return out


def _weapon(ctx, r, m, prof, mass_kg):
    out = []
    rpm, e = m.get("weapon_rpm"), m.get("weapon_energy_j")
    if rpm is None or e is None:
        ctx.not_checked.append("physics weapon: power group gave no weapon_rpm / weapon_energy_j")
        return out
    fight = rpm * limit(prof, "weapon_fight_rpm_share")
    w = fight * 2 * math.pi / 60.0
    inertia = 2.0 * e / (w * w) if w > 0 else 0.0  # back out J from power's real-geometry energy
    m["weapon_inertia_kgm2"] = inertia
    wp = next((rp for rp in r.parts if rp.part.kind == "weapon" and rp.part.weapon is not None), None)
    wd = wp.part.weapon if wp else None
    motor = next((q for q in r.parts if wd is not None and q.part.id == wd.motor), None)
    mp = _props(motor)
    kv, stall = mp.get("kv"), mp.get("stall_current_a", mp.get("max_current_a"))
    red = float(getattr(wd, "reduction", None) or 1.0)
    if kv and stall:
        t = F.spinup_time_s(inertia, fight, rpm, F.motor_torque_stall_nm(float(stall), float(kv)), red)
        m["weapon_spinup_s"] = t
        lim = limit(prof, "max_spinup_s")
        out.append(fail("physics.spinup", G, WARNING, "Weapon spins up slowly",
                        f"{t:.2f} s to {fight:.0f} rpm; limit {lim:.1f} s. Slow spin-up loses the first hit.")
                   .expect(f"<= {lim}", f"{t:.2f}").fix("Higher-current motor, lower inertia, or a reduction.")
                   if t > lim else ok("physics.spinup", G, "Spin-up fast enough", f"{t:.2f} s to {fight:.0f} rpm."))
    else:
        ctx.not_checked.append("physics.spinup: weapon motor lacks kv or stall/max current")
    teeth = int(getattr(wd, "teeth", None) or 2)
    b = F.bite_m(limit(prof, "closing_speed_ms"), fight, teeth) * 1000.0
    m["weapon_bite_mm"] = b
    blim = limit(prof, "min_bite_mm")
    out.append(fail("physics.bite", G, WARNING, "Weapon bite is shallow",
                    f"{b:.1f} mm per tooth at {limit(prof, 'closing_speed_ms'):.1f} m/s closing with {teeth} teeth; below {blim} mm it skips off wedges.")
               .fix("Fewer teeth or lower rpm.") if b < blim else ok("physics.bite", G, "Bite ok", f"{b:.1f} mm per tooth."))
    track = m.get("track_mm")
    if track:
        om = F.gyro_turn_rate_limit(inertia, fight, mass_kg, float(track) / 1000.0)
        m["gyro_turn_limit_rad_s"] = om
        glim = limit(prof, "min_gyro_turn_rad_s")
        out.append(fail("physics.gyro", G, WARNING, "Gyro lifts a wheel when turning",
                        f"Wheels lift above {om:.1f} rad/s yaw (need {glim}). Horizontal spinner will hop on turns.")
                   .fix("Wider track, lower weapon inertia, or vertical spin axis.") if om < glim
                   else ok("physics.gyro", G, "Gyro ok", f"Turn limit {om:.1f} rad/s."))
    else:
        ctx.not_checked.append("physics.gyro: no track_mm metric")
    return out


def _power(ctx, r, m, prof):
    out = []
    bat = next(iter(_parts(r, "battery")), None)
    bp = _props(bat)
    peak = m.get("peak_current_a")
    mah, c = bp.get("capacity_mah"), bp.get("c_rating")
    if peak is None or not mah:
        ctx.not_checked.append("physics.runtime: no peak current or battery capacity")
    else:
        avg = float(peak) * limit(prof, "avg_current_share")
        t = F.runtime_s(float(mah), avg)
        m["runtime_s"] = t
        lim = limit(prof, "min_runtime_s")
        out.append(fail("physics.runtime", G, BLOCKER, "Battery dies before the fight ends",
                        f"~{t:.0f} s at ~{avg:.1f} A average from {mah} mAh; a fight is {lim:.0f} s.")
                   .fix("Bigger pack or less current.") if t < lim else ok("physics.runtime", G, "Runtime ok", f"~{t:.0f} s."))
        if c:
            cmax = F.battery_max_a(float(mah), float(c))
            out.append(fail("physics.c_rating", G, WARNING, "Peak exceeds battery C rating",
                            f"Peak {peak:.1f} A vs {cmax:.1f} A ({mah} mAh x {c} C).").fix("Higher-C pack.")
                       if peak > cmax else ok("physics.c_rating", G, "C rating ok", f"{peak:.1f} / {cmax:.1f} A."))
    margin = limit(prof, "esc_margin")
    for esc in _parts(r, "esc"):
        ep = _props(esc)
        cont = ep.get("cont_current_a", ep.get("continuous_a", ep.get("max_current_a")))
        load = ep.get("load_a")
        for tgt in (getattr(esc.part, "drives", None) or []):
            q = next((x for x in r.parts if x.part.id == tgt), None)
            qp = _props(q)
            load = (load or 0.0) + float(qp.get("max_current_a", qp.get("stall_current_a", 0.0)) or 0.0)
        if cont is None or not load:
            ctx.not_checked.append(f"physics.esc_margin `{esc.part.id}`: no ESC rating or load")
            continue
        out.append(fail("physics.esc_margin", G, WARNING, "ESC current margin too small",
                        f"`{esc.part.id}` {cont} A vs {load:.1f} A load; need x{margin}.").on(esc.part.id)
                   if float(cont) < load * margin else ok("physics.esc_margin", G, "ESC margin ok", f"`{esc.part.id}` {cont}/{load:.1f} A."))
    return out


def _drive(ctx, r, m, prof, mass_kg):
    out = []
    motors = _parts(r, "motor")
    wheel_d = m.get("wheel_d_mm")
    if not motors or not wheel_d:
        ctx.not_checked.append("physics drive: no drive motors or wheel_d_mm metric")
        return out
    mp = _props(motors[0])
    rpm = mp.get("rpm_nominal", mp.get("no_load_rpm", mp.get("rpm")))
    stall_t = mp.get("stall_torque_nm")
    if stall_t is None and mp.get("stall_torque_gcm"):
        stall_t = float(mp["stall_torque_gcm"]) * GCM_TO_NM
    if stall_t is None and mp.get("stall_torque_kgcm"):
        stall_t = float(mp["stall_torque_kgcm"]) * 1000.0 * GCM_TO_NM
    red = float(getattr(motors[0].part, "reduction", None) or 1.0)
    d = float(wheel_d) / 1000.0
    if rpm:
        v = F.drive_top_speed_ms(float(rpm), d, red)
        m["drive_speed_ms"] = v
        lo, hi = limit(prof, "min_drive_speed_ms"), limit(prof, "max_drive_speed_ms")
        out.append(fail("physics.drive_speed", G, WARNING, "Drive speed out of range",
                        f"~{v:.1f} m/s top speed; want {lo} to {hi} m/s for control in a 1.2 m arena.")
                   if not lo <= v <= hi else ok("physics.drive_speed", G, "Drive speed ok", f"~{v:.1f} m/s."))
    else:
        ctx.not_checked.append("physics.drive_speed: motor no-load rpm unknown")
    if stall_t:
        push = F.push_force_n(float(stall_t), len(motors), d, red)
        share = float(m.get("driven_weight_share", 0.5))
        trac = F.traction_force_n(mass_kg, share, limit(prof, "mu_tyre"))
        m["push_force_n"], m["traction_n"] = push, trac
        out.append(fail("physics.push", G, WARNING, "Motors can't break traction",
                        f"Stall push {push:.1f} N < traction {trac:.1f} N; robot stalls in a shove, drawing stall current.")
                   .fix("More torque (gear down) or less driven weight.") if push < trac
                   else ok("physics.push", G, "Pushing traction-limited", f"push {push:.1f} N >= traction {trac:.1f} N."))
    else:
        ctx.not_checked.append("physics.push: motor stall torque unknown")
    return out


def _invert(ctx, r, m):
    # dynamics writes `invert_wheel_shortfall_mm` (0 = every wheel stands proud of the top); the spec flag is `can_run_inverted`
    short = m.get("invert_wheel_shortfall_mm")
    inv = None if short is None else float(short) <= 0.0
    srt = bool(getattr(r.spec, "can_run_inverted", False) or getattr(r.spec, "self_right", False))
    if inv is None and not srt:
        ctx.not_checked.append("physics.invert: no invert_wheel_shortfall_mm metric (dynamics did not run) and no self-righting declared")
        return []
    if inv or srt:
        return [ok("physics.invert", G, "Drives inverted or self-rights", "Robot can fight upside down or right itself.")]
    return [fail("physics.invert", G, WARNING, "Dead when flipped",
                 "Wheels don't touch the floor inverted and no self-righting declared.")
            .fix("Wheels proud of both faces, or a self-righting mechanism.")]
