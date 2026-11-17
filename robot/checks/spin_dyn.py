"""Spinner-in-motion checks (run from the dynamics group): what the weapon does to the robot while it drives.

1. dynamics.brake_dive   - braking/accelerating shifts the effective centre of mass; the robot must not pitch onto the
                           spinning weapon (same first-contact test as ground.pitch_rest, gravity + mu * g).
2. dynamics.spinup_kick  - motor reaction torque at spin-up: yaws the robot (vertical axis) or lifts a side (horizontal).
3. dynamics.gyro_lift    - precession couple of a horizontal-axis spinner during a hard turn lifts a wheel.
4. dynamics.floor_margin - a low weapon (undercutter) still clears the floor with squashed tyres and a tilted floor.
5. dynamics.invert_weapon- upside down, a low weapon must not be the part that rests on the floor.
All numbers are measured from the spec (mass, centre of mass, contacts, weapon inertia, motor kv/stall); the fix line
says what to change and by how much.
"""

from __future__ import annotations

import math

import numpy as np

from .. import catalog, geom
from ..finding import BLOCKER, WARNING, fail, note, ok
from . import _physics as ph
from .ground import SPINNING_KINDS, first_contact

G = "dynamics"
MU_TYRE = 1.0  # rubber/silicone on steel arena floor: braking/accel up to ~1 g
TYRE_SQUASH_MM = 0.5  # tyre compression under a hit or landing
FLOOR_TILT_DEG = 3.0  # arena floor seam / plate edge
DEFAULT_PHASE_A = 30.0  # weapon motor current at spin-up when the ESC rating is unknown (A)
YAW_KICK_DEG = 30.0  # yaw the robot may turn while the weapon spins up before it is a problem
GYRO_TURN_RAD_S = 15.0


def _wheel_lows(ctx, floor):
    out = []
    for b in ctx.world.bodies:
        if b.kind == "wheel" and not b.fastener:
            v = b.mesh.vertices
            z = v[:, 2].min()
            sel = v[v[:, 2] <= z + 1e-3]
            out.append((b, np.array([sel[:, 0].mean(), sel[:, 1].mean(), z])))
    return out


def _bodies(ctx):
    return [b for b in ctx.world.bodies if not b.is_wire and not b.fastener and b.kind not in ("wheel", "tyre")]


def brake_dive(ctx, floor, com):
    """Braking at mu*g moves the effective centre of mass forward by h*mu (and back when accelerating)."""
    out = []
    lows = _wheel_lows(ctx, floor)
    if len(lows) < 2:
        return out
    h = float(com[2]) - floor
    ys = [float(p[1]) for _, p in lows]
    for name, sgn in (("braking", 1.0), ("accelerating", -1.0)):
        # forward = +y; braking throws mass forward
        c = (float(com[0]), float(com[1]) + sgn * h * MU_TYRE)
        if min(ys) - 1.0 <= c[1] <= max(ys) + 1.0 and len(lows) >= 3:
            continue  # still over the wheels
        fc = first_contact(lows, floor, c, _bodies(ctx))
        if fc is None:
            continue
        b, ang, sd = fc
        ctx.metrics[f"{name}_rest_part"] = b.id
        if b.kind in SPINNING_KINDS:
            out.append(fail("dynamics.brake_dive", G, BLOCKER, f"Weapon hits the floor when {name}",
                            f"{name.capitalize()} at {MU_TYRE:.1f} g throws the centre of mass {h * MU_TYRE:.1f} mm "
                            f"{'forward' if sgn > 0 else 'back'} (it is {h:.1f} mm up); the robot pitches {ang:.1f} deg onto "
                            f"`{b.id}`, which grinds the floor.").on(b.id)
                       .fix(f"Add a skid/caster (kind `skid`/`caster`) that lands first: at s mm from the wheel line its "
                            f"bottom <= s x {math.tan(math.radians(ang)):.3f} mm; or lower the centre of mass."))
    if not out:
        out.append(ok("dynamics.brake_dive", G, "Weapon stays off the floor when braking",
                      "Full braking and acceleration pitch the robot onto a skid, wedge or wheel, not the weapon."))
    return out


def _motor_torque_nm(ctx, wpart):
    """Peak weapon motor torque: Kt * I with Kt = 60 / (2 pi kv), I from the ESC rating (or 30 A)."""
    r = ctx.r
    kv = None
    wd = wpart.weapon
    mid = getattr(wd, "motor", None)
    for rp in r.parts:
        if rp.cat is not None and (rp.part.id == mid or rp.part.kind == "weapon_motor") and rp.cat.props.get("kv"):
            kv = float(rp.cat.props["kv"])
            break
    if kv is None:
        return None, None
    amps = DEFAULT_PHASE_A
    for rp in r.parts:
        if rp.part.kind == "esc" and rp.cat is not None:
            amps = float(rp.cat.props.get("cont_a") or rp.cat.props.get("current_a") or amps)
            break
    return 60.0 / (2 * math.pi * kv) * amps, amps


def _robot_yaw_inertia(ctx):
    bs = [b.aabb for b in ctx.world.bodies if not b.is_wire]
    m = ph.robot_mass_g(ctx) * 1e-3
    if not bs:
        L = W = 0.1
    else:
        lo = np.min([a[0] for a in bs], axis=0)
        hi = np.max([a[1] for a in bs], axis=0)
        L, W = float(hi[1] - lo[1]) * 1e-3, float(hi[0] - lo[0]) * 1e-3
    return m * (L * L + W * W) / 12.0


def spinup_kick(ctx, floor, com):
    out = []
    for p, wb, origin, axis in ph.weapons(ctx):
        tau, amps = _motor_torque_nm(ctx, p)
        if tau is None:
            ctx.not_checked.append(f"Spin-up kick of `{p.id}`: weapon motor kv unknown")
            continue
        m = ph.robot_mass_g(ctx) * 1e-3
        weight = m * ph.G0
        ctx.metrics[f"weapon_spinup_torque_nm.{p.id}"] = tau
        vertical_axis = abs(float(axis[2])) > 0.7
        lows = _wheel_lows(ctx, floor)
        if vertical_axis:
            # wheels resist yaw by friction at their track radius
            xs = [float(q[0]) for _, q in lows] or [0.0]
            half_track = max((max(xs) - min(xs)) / 2 * 1e-3, 1e-3)
            resist = MU_TYRE * weight * half_track
            if tau > resist:
                Iz = _robot_yaw_inertia(ctx)
                dens = catalog.density(p.material) or 7.8
                Iw = geom.axial_inertia(wb.geom, wb.M, origin, axis) * dens * 1e-12
                rpm = ctx.metrics.get("weapon_rpm")
                if rpm:
                    Lw = Iw * rpm * 2 * math.pi / 60  # weapon angular momentum at full speed
                    t = Lw / tau  # spin-up time at full torque
                    # during spin-up the body gets (tau - grip); after it the grip brakes the body to a stop
                    a1 = (tau - resist) / max(Iz, 1e-9)
                    w1 = a1 * t
                    yaw = math.degrees(0.5 * a1 * t * t + w1 * w1 / (2 * resist / max(Iz, 1e-9)))
                    how = (f"about {yaw:.0f} deg over a {t:.2f} s full-throttle spin-up (an ESC ramp or current limit "
                           "below the grip torque removes it)")
                    sev = WARNING  # a driving fix (ramp), not a design blocker
                else:
                    how, sev = "by an amount not judged (weapon rpm unknown)", WARNING
                out.append(fail("dynamics.spinup_kick", G, sev, "Robot spins when the weapon spins up",
                                f"`{p.id}` spin-up torque {tau:.2f} N m ({amps:.0f} A) beats tyre grip {resist:.2f} N m: the robot "
                                f"yaws the other way while the weapon gets to speed, {how}.").on(p.id)
                           .fix("Ramp the weapon throttle (ESC ramp/current limit), widen the track, or add weight on the wheels."))
            else:
                out.append(ok("dynamics.spinup_kick", G, "Tyres hold the spin-up torque",
                              f"`{p.id}` {tau:.2f} N m < grip {resist:.2f} N m."))
        else:
            # reaction about a horizontal axis tries to roll/pitch the body: resisted by weight x lever
            lever = 1e9
            if lows:
                pts = np.array([[float(q[0]), float(q[1])] for _, q in lows])
                tilt = np.cross(axis, [0, 0, 1.0])[:2]
                tilt = tilt / max(np.linalg.norm(tilt), 1e-9)
                lever = float(np.abs((pts - np.array(com[:2])) @ tilt).min()) * 1e-3
            if tau > weight * lever:
                out.append(fail("dynamics.spinup_kick", G, WARNING, "Weapon spin-up lifts the robot",
                                f"`{p.id}` spin-up torque {tau:.2f} N m beats the weight moment {weight * lever:.2f} N m "
                                f"({lever * 1e3:.1f} mm lever): the robot rocks onto one side when the weapon starts.").on(p.id)
                           .fix("Ramp the weapon throttle, or put the wheels further from the centre of mass."))
    return out


def gyro_lift(ctx, floor, com):
    """A horizontal-axis spinner turning at Omega produces I w Omega about the third axis: it lifts a wheel when that
    beats weight x lever (vertical-axis spinners give no couple in a flat turn)."""
    out = []
    for p, wb, origin, axis in ph.weapons(ctx):
        k = float(np.linalg.norm(np.cross(axis, [0, 0, 1.0])))
        if k < 0.3:
            continue
        rpm = ctx.metrics.get("weapon_rpm")
        dens = catalog.density(p.material)
        if not rpm or dens is None:
            ctx.not_checked.append(f"Gyro lift of `{p.id}`: weapon rpm or material unknown")
            continue
        I = geom.axial_inertia(wb.geom, wb.M, origin, axis) * dens * 1e-12
        tau = I * rpm * 2 * math.pi / 60 * GYRO_TURN_RAD_S * k
        m = ph.robot_mass_g(ctx) * 1e-3 * ph.G0
        lows = _wheel_lows(ctx, floor)
        if not lows:
            continue
        # couple axis = axis x up: it tips the robot about that direction; lever = distance of com to the contacts
        # measured across that axis
        ax = np.cross(axis, [0, 0, 1.0])[:2]
        ax = ax / max(np.linalg.norm(ax), 1e-9)
        nrm = np.array([-ax[1], ax[0]])
        pts = np.array([[float(q[0]), float(q[1])] for _, q in lows])
        lever = float(np.abs((pts - np.array(com[:2])) @ nrm).min()) * 1e-3
        ctx.metrics[f"weapon_gyro_lift_ratio.{p.id}"] = tau / max(m * lever, 1e-9)
        if tau > m * lever:
            out.append(fail("dynamics.gyro_lift", G, WARNING, "Robot lifts a side when it turns",
                            f"`{p.id}` precession {tau:.2f} N m in a {GYRO_TURN_RAD_S:.0f} rad/s turn beats the weight moment "
                            f"{m * lever:.2f} N m ({lever * 1e3:.1f} mm lever): the robot hops onto one wheel and loses steering.")
                       .on(p.id).fix("Lower the weapon rpm or inertia, widen the stance across the spin axis, or drive slower turns."))
        else:
            out.append(ok("dynamics.gyro_lift", G, "Stays flat in turns",
                          f"`{p.id}` precession {tau:.2f} N m < weight moment {m * lever:.2f} N m."))
    return out


def floor_margin(ctx, floor):
    """A low weapon (rim within 10 mm of the floor) must clear it with squashed tyres and a 3 deg floor tilt."""
    out = []
    for p, wb, origin, axis in ph.weapons(ctx):
        v = wb.mesh.vertices
        low = float(v[:, 2].min()) - floor
        if low > 10.0:
            continue
        reach = float(ph.perp_radius(v, origin, axis).max())
        drop = TYRE_SQUASH_MM + reach * math.sin(math.radians(FLOOR_TILT_DEG))
        ctx.metrics[f"weapon_floor_margin_mm.{p.id}"] = low - drop
        if low < TYRE_SQUASH_MM:
            sev = BLOCKER
        elif low < drop:
            sev = WARNING
        else:
            out.append(ok("dynamics.floor_margin", G, "Weapon clears the floor",
                          f"`{p.id}` is {low:.1f} mm up; worst case drop {drop:.1f} mm."))
            continue
        out.append(fail("dynamics.floor_margin", G, sev, "Weapon can hit the floor",
                        f"`{p.id}` is {low:.1f} mm above the floor; squashed tyres ({TYRE_SQUASH_MM} mm) and a {FLOOR_TILT_DEG:.0f} deg "
                        f"floor seam drop its {reach:.0f} mm tip by {drop:.1f} mm.").on(p.id)
                   .expect(f">= {drop:.1f} mm", f"{low:.1f} mm")
                   .fix(f"Raise the weapon {drop - low + 0.2:.1f} mm, or shorten it."))
    return out


def invert_weapon(ctx):
    """Upside down the highest point becomes the floor: a low (undercutter) weapon must not be that point."""
    out = []
    if not ctx.r.spec.can_run_inverted:
        return out
    bodies = [b for b in ctx.world.bodies if not b.is_wire and not b.fastener]
    if not bodies:
        return out
    top = max(float(b.aabb[1][2]) for b in bodies)
    for p, wb, origin, axis in ph.weapons(ctx):
        gap = top - float(wb.aabb[1][2])
        ctx.metrics[f"weapon_inverted_gap_mm.{p.id}"] = gap
        if gap < TYRE_SQUASH_MM:
            out.append(fail("dynamics.invert_weapon", G, BLOCKER, "Weapon touches the floor upside down",
                            f"Inverted, `{p.id}` is {gap:.1f} mm from the floor plane: it rests on the spinning weapon.")
                       .on(p.id).fix("Make the wheels or a skid stand proud of the weapon on the top side by >= 0.5 mm."))
    return out


HIT_SIDE_FRACTION = 0.3  # share of the impact force that lands out of the spin plane (glancing / floor / wall hit)
BEARING_TILT_DEG = 0.3  # shaft tilt from bearing play and frame give under that hit
WOBBLE_MARGIN_MM = 0.5


def blade_wobble(ctx, floor):
    """A hit on a wall, floor or opponent pushes the blade out of its spin plane: it bends as a cantilever from the hub
    and the shaft tilts in its bearings. The tip then moves `delta` along the spin axis; the swept band must stay
    clear of the floor and of every other part by delta + margin."""
    out = []
    F = ph.impact_n(ctx) * HIT_SIDE_FRACTION
    for p, wb, origin, axis in ph.weapons(ctx):
        v = wb.mesh.vertices
        rad = ph.perp_radius(v, origin, axis)
        R = float(rad.max())
        ax = (v - origin) @ axis
        t = float(ax.max() - ax.min())  # blade thickness along the spin axis
        mech = catalog.mech(p.material)
        if mech is None or t <= 0 or R <= 0:
            ctx.not_checked.append(f"Blade wobble of `{p.id}`: material modulus or geometry unknown")
            continue
        E = mech[2] * 1e3  # N/mm^2
        hub = R * 0.25  # clamp radius ~ hub/spider (a quarter of the reach when not modelled)
        L = max(R - hub, 1.0)
        width = max(wb.geom.volume / max(t * 2 * R, 1e-6), 2.0)  # mean blade width (volume / (t x full length))
        I = width * t ** 3 / 12.0
        flex = F * L ** 3 / (3 * E * I)
        tilt = R * math.sin(math.radians(BEARING_TILT_DEG))
        delta = flex + tilt
        ctx.metrics[f"weapon_wobble_mm.{p.id}"] = delta
        # clearance along the spin axis: floor (when the axis is near vertical) and parts inside the swept radius
        gaps = []
        if abs(float(axis[2])) > 0.7:
            gaps.append(("floor", float(v[:, 2].min()) - floor))
        a0, a1 = float(ax.min()), float(ax.max())
        from .archetype import rotor_set
        try:
            rotor = set(rotor_set(ctx.r.spec, p.id))
        except Exception:  # noqa: BLE001
            rotor = {p.id}
        rotor |= {q.id for q in ctx.r.spec.parts if q.parent in rotor}  # bodies carried by the rotor spin with it
        for b in ctx.world.bodies:
            if b is wb or b.id in rotor or b.is_wire or b.fastener or b.kind in SPINNING_KINDS or b.kind == "bearing":
                continue
            bv = b.mesh.vertices
            br = ph.perp_radius(bv, origin, axis)
            k = (br <= R) & (br >= hub)  # under the hub nothing wobbles: only the free span sweeps out of plane
            if not k.any():
                continue
            ba = (bv[k] - origin) @ axis
            above = ba[ba >= a1]
            below = ba[ba <= a0]
            cand = ([float(above.min() - a1)] if len(above) else []) + ([float(a0 - below.max())] if len(below) else [])
            if not cand:
                continue  # the part overlaps the blade band itself: interference checks own that
            g = min(cand)
            if g < 50:
                gaps.append((b.id, g))
        if not gaps:
            continue
        who, g = min(gaps, key=lambda q: q[1])
        need = delta + WOBBLE_MARGIN_MM
        msg = (f"A {F:.0f} N out-of-plane hit bends `{p.id}` ({p.material}, {t:.1f} mm thick, ~{width:.0f} mm wide, {L:.0f} mm "
               f"free span) {flex:.2f} mm, and {BEARING_TILT_DEG} deg of shaft tilt adds {tilt:.2f} mm at the {R:.0f} mm tip: "
               f"the tip wobbles {delta:.2f} mm along the spin axis. Nearest thing along that axis: `{who}` at {g:.2f} mm.")
        if g < need:
            sev = BLOCKER if g < delta else WARNING
            out.append(fail("dynamics.blade_wobble", G, sev, "Blade can wobble into the robot or floor", msg).on(p.id, *([who] if who != "floor" else []))
                       .expect(f">= {need:.2f} mm", f"{g:.2f} mm")
                       .fix(f"Open the gap to `{who}` by {need - g:.2f} mm, or stiffen the blade (thicker / wider root / "
                            "smaller free span), or support the shaft both sides closer to the blade."))
        else:
            out.append(ok("dynamics.blade_wobble", G, "Blade wobble stays clear", msg))
    return out


def run_all(ctx, floor, com):
    out = []
    for f in (lambda: brake_dive(ctx, floor, com), lambda: spinup_kick(ctx, floor, com),
              lambda: gyro_lift(ctx, floor, com), lambda: floor_margin(ctx, floor), lambda: invert_weapon(ctx),
              lambda: blade_wobble(ctx, floor)):
        try:
            out += f()
        except Exception as e:  # noqa: BLE001 - one broken estimate must not hide the others
            ctx.not_checked.append(f"spinner dynamics: {e}")
    return out
