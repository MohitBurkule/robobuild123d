"""Hit reaction and gyroscopic wheel-lift (`impact.*`, F1).

WHY: a fast turn with a spinning weapon stores gyroscopic stiffness: turning the
robot at yaw rate `Omega` needs a torque `I_w * omega * Omega * sin(tilt)` where
tilt is the angle between the spin axis and vertical: the gyro moment is the cross
torque `Omega x L`, which vanishes when a weapon spins about the vertical (a flat
bar spinner yaws about the same axis it spins about) and is full for a horizontal
spin axis (a drum). When it exceeds the gravity restoring torque `m g (track/2)`
the inside wheels lift and the robot rolls. And when a vertical spinner lands a
hit, some of its energy throws the robot itself off the floor (hop), while a
horizontal spinner yaws the robot (spin-out). Closed-form estimates from the
power group's metrics.

Omega_lift = m g (track/2) / (I_w omega sin(tilt)): the yaw rate at which the
robot lifts. Warn when the design's assumed turn rate is over half of it, block
over 0.75. Hop: h = k E / (m g) with k = 0.25 (a low hit throws the robot, most
energy stays in the target); warn over 20 mm. Yaw: omega_yaw = I_w omega / I_yaw
with I_yaw ~ m (footprint/2)^2 (a disc of the footprint radius); warn over 720 deg/s.
"""

from __future__ import annotations

import math

import numpy as np

from ..finding import BLOCKER, WARNING, fail, ok
from .. import xform

G = "impact"
TURN_RATE_RAD_S = 15.0  # a hard antweight pivot (same default as dynamics.GYRO_TURN_RAD_S_DEFAULT)
LIFT_WARN_X, LIFT_BLOCK_X = 0.5, 0.75  # turn rate as a fraction of Omega_lift
HOP_WARN_MM = 30.0
HOP_ENERGY_FRAC = 0.005  # fraction of the hit energy that throws the robot itself (most stays in the target)
YAW_WARN_DEG_S = 720.0


def weapon_inertia(ctx):
    """(I [kg m2], omega [rad/s]) from the power group's energy + rpm metrics, or (None, None)."""
    e = ctx.metrics.get("weapon_energy_j")
    rpm = ctx.metrics.get("weapon_rpm")
    if not e or not rpm:
        return None, None
    omega = float(rpm) * 2 * math.pi / 60.0
    if omega <= 0:
        return None, None
    return 2.0 * float(e) / omega ** 2, omega


def spin_tilt(ctx):
    """|cos| of the angle between the weapon's spin axis and world vertical (1 = vertical axis), or None when unknown.

    The gyro moment of a turn is Omega x L: a vertical spin axis is parallel to the yaw axis, so turning cannot
    roll the robot no matter how fast the weapon spins. Only the tilt's sine couples yaw into roll.
    """
    if ctx.r is None:
        return None
    for rp in ctx.r.parts:
        if rp.part.kind != "weapon" or rp.part.weapon is None:
            continue
        b = ctx.world.body(rp.part.id)
        if b is None or getattr(b, "M", None) is None:
            continue
        wd = rp.part.weapon
        local = np.asarray(wd.spin_axis if wd.spin_axis is not None else [0.0, 0.0, 1.0], float)
        a = xform.apply_dir(b.M, local)
        n = float(np.linalg.norm(a))
        return abs(float(a[2])) / n if n > 0 else None
    return None


def wheel_track(ctx):
    """Track (mm) across the wheel contact centres, or None."""
    wheels = [b for b in ctx.world.bodies if getattr(b, "kind", "") == "wheel" and not getattr(b, "fastener", False)]
    xs = []
    for b in wheels:
        M = getattr(b, "M", None)
        if M is not None:
            xs.append(float(M[0, 3]))
    return (max(xs) - min(xs)) if len(xs) >= 2 else None


def run(ctx):
    out = []
    m_kg = (ctx.metrics.get("mass_total_g") or 0.0) / 1000.0
    i_w, omega = weapon_inertia(ctx)
    if i_w is None or m_kg <= 0:
        ctx.not_checked.append("Impact/gyro: no weapon energy + rpm + mass (run the power and mass groups first)")
        return out
    track = wheel_track(ctx)
    judged = []
    omega_lift = None
    vert = spin_tilt(ctx)
    gyro = 1.0 if vert is None else math.sqrt(max(0.0, 1.0 - vert * vert))  # sin of the axis tilt
    if track and gyro < 1e-3:
        out.append(ok("impact.gyro_lift", G, "No gyroscopic wheel-lift from yaw",
                      f"The weapon spins about the vertical (axis tilt cos {vert:.3f}): a yaw rate is parallel to the "
                      "spin angular momentum, so turning produces no gyroscopic roll (M = Omega x L)."))
        judged.append(True)
    elif track:
        omega_lift = m_kg * 9.81 * (track / 2000.0 / 2) / (i_w * omega * gyro)
        frac = TURN_RATE_RAD_S / omega_lift if omega_lift > 0 else float("inf")
        ctx.metrics["gyro_lift_yaw_rad_s"] = round(omega_lift, 2)
        if frac >= LIFT_BLOCK_X:
            out.append(fail("impact.gyro_lift", G, BLOCKER, "A hard turn lifts the wheels (gyroscopic roll)",
                            f"Turning at {TURN_RATE_RAD_S:.0f} rad/s needs {frac:.2f}x the {omega_lift:.1f} rad/s "
                            f"lift threshold (track {track:.0f} mm, weapon I {i_w * 1000:.1f} g*m2 at {omega:.0f} rad/s, "
                            f"spin axis {math.degrees(math.asin(min(gyro, 1.0))):.0f} deg off vertical).")
                       .fix("Slow the turn, widen the track, or store less energy in the weapon "
                            "(lighter disc / lower rpm)."))
        elif frac >= LIFT_WARN_X:
            out.append(fail("impact.gyro_lift_margin", G, WARNING, "Little margin to gyroscopic wheel-lift",
                            f"Turn rate is {frac:.2f}x of the {omega_lift:.1f} rad/s lift threshold "
                            f"(warn over {LIFT_WARN_X:.2f}).")
                       .fix("Widen the track or trim the weapon energy for margin."))
        else:
            judged.append(True)
    else:
        ctx.not_checked.append("Gyro wheel-lift: no two wheels to measure a track from")
    kind = ctx.metrics.get("weapon_orientation") or ""
    hop_mm = HOP_ENERGY_FRAC * ctx.metrics.get("weapon_energy_j", 0.0) / (m_kg * 9.81) * 1000.0
    ctx.metrics["hit_hop_mm"] = round(hop_mm, 1)
    if "v" in str(kind).lower() or not kind:
        if hop_mm > HOP_WARN_MM:
            out.append(fail("impact.hop", G, WARNING, "A solid hit throws the robot off the floor",
                            f"About {hop_mm:.0f} mm of hop ({HOP_ENERGY_FRAC:.2f}x of "
                            f"{ctx.metrics.get('weapon_energy_j', 0.0):.1f} J into {m_kg * 1000:.0f} g); "
                            f"warn over {HOP_WARN_MM:.0f} mm - the wheels lose drive and steering mid-exchange.")
                       .fix("Trade weapon energy for mass low in the chassis, or accept and design the wedge for it."))
        else:
            judged.append(True)
    if kind and "h" in str(kind).lower():
        fp = ctx.metrics.get("footprint_mm")
        if fp:
            i_yaw = m_kg * (fp / 2000.0) ** 2
            yaw = i_w * omega / i_yaw
            ctx.metrics["hit_yaw_deg_s"] = round(math.degrees(yaw), 0)
            if math.degrees(yaw) > YAW_WARN_DEG_S:
                out.append(fail("impact.yaw", G, WARNING, "A hit spins the robot around",
                                f"Yaw rate about {math.degrees(yaw):.0f} deg/s (warn over {YAW_WARN_DEG_S:.0f}) "
                                "from equal-and-opposite momentum on the weapon axis.")
                           .fix("More yaw inertia (wider footprint) or less angular momentum in the weapon."))
            else:
                judged.append(True)
    if len(judged) >= 1 and not any(not f.passed for f in out):
        extra = f", lift margin {TURN_RATE_RAD_S / omega_lift:.2f}x" if omega_lift else ""
        out.append(ok("impact.ok", G, "Hit reaction within margins", f"hop {hop_mm:.0f} mm{extra}"))
    return out
