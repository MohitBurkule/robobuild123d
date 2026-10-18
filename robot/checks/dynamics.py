"""Rigid-body behaviour: centre-of-mass height and static tip-over angles, driving upside down, weight on the driven wheels,
weapon balance at speed and gyroscopic load on the weapon bearings during a turn."""

from __future__ import annotations

import math

import numpy as np

from .. import catalog, geom
from ..finding import BLOCKER, WARNING, fail, note, ok
from . import _physics as ph
from .ground import hull

G = "dynamics"
CONTACT_MM = 2.0  # (same as ground.stance) a non-wheel point this close to the floor carries load
MIN_TIP_DEG = 20.0
MIN_DRIVEN_SHARE = 0.6
INVERT_TOL_MM = 0.5
IMBALANCE_WARN_X, IMBALANCE_BLOCK_X = 5.0, 20.0  # rotating imbalance force over the robot weight
GYRO_TURN_RAD_S_DEFAULT = 15.0  # a hard pivot of an antweight when the drive speed is unknown


def run(ctx):
    w = ctx.world
    out = []
    wheels = [b for b in w.bodies if b.kind == "wheel" and not b.fastener]
    if "com_x" not in ctx.metrics:
        ctx.not_checked.append("Dynamics: no centre of mass from the mass group; tip, traction and invert not judged")
        out.append(fail("dynamics.no_com", G, WARNING, "No centre of mass", "The mass group gave no centre of mass."))
    elif not wheels:
        ctx.not_checked.append("Dynamics: no wheels, so tip, traction and invert are not judged")
    else:
        floor = ph.floor_z(ctx)
        com = np.array([ctx.metrics["com_x"], ctx.metrics["com_y"], ctx.metrics["com_z"]])
        out += tipping(ctx, wheels, floor, com)
        out += invertible(ctx, wheels)
    out += balance_and_gyro(ctx)
    return out


def _contacts(ctx, wheels, floor):
    pts, other = [], []
    for b in wheels:
        v = b.mesh.vertices
        low = v[v[:, 2] <= floor + CONTACT_MM]
        if len(low):
            pts.append((b, low))
    for b in ph.solids(ctx.world):
        if b.kind in ("wheel", "tyre") or b.fastener:
            continue
        v = b.mesh.vertices
        low = v[v[:, 2] <= floor + CONTACT_MM]
        if len(low):
            other.append((b, low))
    return pts, other


def tipping(ctx, wheels, floor, com):
    out = []
    h = float(com[2]) - floor
    ctx.metrics["cog_height_mm"] = h
    wpts, opts = _contacts(ctx, wheels, floor)
    P = [p[:2] for _, v in wpts + opts for p in v]
    hl = hull(P) if P else []
    if len(hl) < 3 or h <= 0:
        ctx.not_checked.append("Tip-over angles: the floor contacts do not form a support polygon")
    else:
        c = (float(com[0]), float(com[1]))
        worst = {}
        for i, a in enumerate(hl):
            b = hl[(i + 1) % len(hl)]
            ex, ey = b[0] - a[0], b[1] - a[1]
            ln = math.hypot(ex, ey)
            d = ((ex) * (c[1] - a[1]) - (ey) * (c[0] - a[0])) / ln
            nx, ny = ey / ln, -ex / ln  # outward normal of a CCW hull
            ang = math.degrees(math.atan2(d, h))
            side = ("front" if ny > 0 else "back") if abs(ny) >= abs(nx) else ("right" if nx > 0 else "left")
            worst[side] = min(worst.get(side, 1e9), ang)
        for s, a in worst.items():
            ctx.metrics[f"tip_angle_{s}_deg"] = a
        s_min = min(worst, key=worst.get)
        a_min = worst[s_min]
        msg = ", ".join(f"{s} {a:.0f}°" for s, a in sorted(worst.items()))
        if a_min < MIN_TIP_DEG:
            out.append(fail("dynamics.tip_angle", G, WARNING, "Tips over easily",
                            f"Centre of mass is {h:.1f} mm up; static tip angles {msg}. Towards the {s_min} it goes over at {a_min:.0f}° "
                            f"(need {MIN_TIP_DEG:.0f}°): a ramp, a wall bump or a hit flips it.")
                       .expect(f">= {MIN_TIP_DEG:.0f}°", f"{a_min:.0f}° ({s_min})").fix("Lower the battery and heavy parts, or widen the stance."))
        else:
            out.append(ok("dynamics.tip_angle", G, "Stable against tipping", f"Centre of mass {h:.1f} mm up; static tip angles {msg}."))

    # Weight on the driven wheels: two-line static split between the wheel contacts and the other floor contacts.
    wy = float(np.mean([v[:, 1].mean() for _, v in wpts])) if wpts else None
    driven = [b for b, _ in wpts if (ph.part(ctx, b) is None or ph.part(ctx, b)._extra.get("driven", True))]
    if wy is None or not driven:
        ctx.not_checked.append("Traction: no driven wheel touches the floor")
        return out
    share = 1.0
    from .ground import margin

    whull = hull([p[:2] for _, v in wpts for p in v])
    # If the wheels alone surround the centre of mass they can carry it all; otherwise the contacts on the far side of
    # the axle from the centre of mass take the rest (two-line lever).
    side = [v for _, v in opts if (v[:, 1].mean() - wy) * (float(com[1]) - wy) > 0]
    if margin(whull, (float(com[0]), float(com[1]))) <= 0 and side:
        oy = float(np.mean(np.concatenate([v[:, 1] for v in side])))
        if abs(oy - wy) > 1.0:
            share = min(max(1.0 - (float(com[1]) - wy) / (oy - wy), 0.0), 1.0)
    ctx.metrics["driven_weight_share"] = share
    others = ", ".join(f"`{b.id}`" for b, _ in opts[:4])
    if share < MIN_DRIVEN_SHARE:
        out.append(fail("dynamics.traction", G, WARNING, "Little weight on the driven wheels",
                        f"About {share * 100:.0f}% of the weight is on the driven wheels; the rest rests on {others}. The robot will "
                        "spin its wheels when pushing.").expect(f">= {MIN_DRIVEN_SHARE * 100:.0f}%", f"{share * 100:.0f}%")
                   .fix("Move mass over the axle, or lift the skid or wedge so it only touches when pitched."))
    else:
        out.append(ok("dynamics.traction", G, "Weight is on the driven wheels",
                      f"About {share * 100:.0f}% of the weight is on the driven wheels" + (f" (rest on {others})." if opts else ".")))
    return out


def invertible(ctx, wheels):
    """Upside down (rolled 180° about the length axis) the wheels must still be the lowest points."""
    out = []
    S = [b for b in ph.solids(ctx.world) if not b.fastener]
    top = max(float(b.aabb[1][2]) for b in S)
    tops = {b.id: float(b.aabb[1][2]) for b in wheels}
    short = {k: top - v for k, v in tops.items() if top - v > INVERT_TOL_MM}
    above = sorted({b.id for b in S if b.kind not in ("wheel", "tyre") and float(b.aabb[1][2]) > max(tops.values()) + INVERT_TOL_MM})
    ctx.metrics["invert_wheel_shortfall_mm"] = max(short.values()) if short else 0.0
    declared = ctx.r.spec.can_run_inverted
    if not short:
        out.append(ok("dynamics.invertible", G, "Drives upside down", "Every wheel stands proud of the top, so it drives inverted."))
    else:
        msg = (f"Inverted, {', '.join(f'`{k}` is {v:.1f} mm short' for k, v in short.items())} of the floor; "
               f"{', '.join(f'`{a}`' for a in above[:5])} stick out above the wheels.")
        if declared:
            out.append(fail("dynamics.invertible", G, BLOCKER, "Cannot drive upside down", msg + " The spec claims it can run inverted.")
                       .on(*above[:5]).fix("Use bigger wheels or lower the top so the tyres stand proud."))
        else:
            out.append(fail("dynamics.invertible", G, WARNING, "Cannot drive upside down",
                            msg + " Once flipped it is stuck unless it can self-right.").on(*above[:5])
                       .fix("Make the wheels stand proud of the top, or add a self-righting feature."))
    return out


def _turn_rate(ctx):
    r = ctx.r
    wheels = [b for b in ctx.world.bodies if b.kind == "wheel" and not b.fastener]
    rpms = [rp.cat.props.get("rpm_nominal") * 1.0 for rp in r.parts if rp.cat is not None and rp.part.kind == "motor"
            and rp.cat.props.get("rpm_nominal")]
    if len(wheels) < 2 or not rpms:
        return GYRO_TURN_RAD_S_DEFAULT, "assumed"
    rad = max((float(b.aabb[1][2] - b.aabb[0][2]) / 2 for b in wheels))
    xs = [float(b.center[0]) for b in wheels]
    track = max(xs) - min(xs)
    if track < 5:
        return GYRO_TURN_RAD_S_DEFAULT, "assumed"
    cells = r.spec.electronics.cells or 2
    nominal = next((rp.cat.props.get("nominal_v") for rp in r.parts if rp.cat is not None and rp.part.kind == "motor"), None) or 6.0
    v = max(rpms) * min(cells * 3.7 / nominal, 1.5) * 2 * math.pi / 60 * rad  # mm/s
    return 2 * v / track, "drive"


def balance_and_gyro(ctx):
    out = []
    ws = ph.weapons(ctx)
    if not ws:
        return out
    rpm = ctx.metrics.get("weapon_rpm")
    for p, wb, origin, axis in ws:
        m = ph.mass_g(ctx, wb)
        if rpm is None or m is None:
            ctx.not_checked.append(f"Weapon `{p.id}` balance and gyro: no weapon rpm or mass")
            out.append(fail("dynamics.balance", G, WARNING, "Weapon balance not judged",
                            f"`{p.id}`: weapon speed or mass unknown, so imbalance and gyro loads were not computed.").on(p.id))
            continue
        omega = rpm * 2 * math.pi / 60
        c = wb.M[:3, :3] @ wb.geom.centroid + wb.M[:3, 3]
        e = float(ph.perp_radius([c], origin, axis)[0])
        grade = e * omega
        force = m * 1e-3 * e * 1e-3 * omega ** 2
        ctx.metrics[f"weapon_imbalance_mm.{p.id}"] = e
        ctx.metrics[f"weapon_balance_grade.{p.id}"] = grade
        ctx.metrics[f"weapon_imbalance_n.{p.id}"] = force
        msg = (f"`{p.id}` mass centre is {e:.3f} mm off the spin axis: grade G{grade:.1f} at {rpm:.0f} rpm, a {force:.0f} N rotating "
               "load on the bearings and frame.")
        weight = ph.robot_mass_g(ctx) * 1e-3 * ph.G0
        x = force / weight
        ctx.metrics[f"weapon_imbalance_x_weight.{p.id}"] = x
        msg += f" That is {x:.1f}x the robot's weight."
        if x > IMBALANCE_WARN_X:
            sev = BLOCKER if x > IMBALANCE_BLOCK_X else WARNING
            out.append(fail("dynamics.balance", G, sev, "Weapon is out of balance", msg + " It will shake the robot and the bearings apart.")
                       .on(p.id).here(c).expect(f"<= {IMBALANCE_WARN_X:.0f}x weight", f"{x:.1f}x (G{grade:.0f})")
                       .fix("Make the weapon symmetric about its axis, add a counterweight, or drill the heavy side."))
        else:
            out.append(ok("dynamics.balance", G, "Weapon is balanced", msg))

        dens = catalog.density(p.material)
        if dens is None:
            ctx.not_checked.append(f"Gyro load of `{p.id}`: unknown weapon material density")
            continue
        I = geom.axial_inertia(wb.geom, wb.M, origin, axis) * dens * 1e-3 * 1e-9  # kg m^2
        turn, src = _turn_rate(ctx)
        # Turning about the vertical: the precession couple is I * omega * Omega * |axis x up|.
        tau = I * omega * turn * float(np.linalg.norm(np.cross(axis, [0, 0, 1.0])))  # N m
        lay = ph.shaft_layout(ctx, wb, origin, axis)
        ctx.metrics[f"weapon_gyro_torque_nm.{p.id}"] = tau
        if lay is None or len(lay["sides"]) < 2:
            ctx.not_checked.append(f"Gyro bearing load of `{p.id}`: no shaft supported on both sides")
            continue
        span = abs(lay["sides"][1.0][0] - lay["sides"][-1.0][0])
        load = tau * 1e3 / max(span, 1e-6)
        ctx.metrics[f"weapon_gyro_bearing_n.{p.id}"] = load
        worst = None
        for s, (_, b) in lay["sides"].items():
            if b.kind != "bearing":
                continue
            od = 2 * float(ph.perp_radius(b.mesh.vertices, origin, axis).max())
            rt = ph.bearing_rating(lay["d"], od)
            if rt is None:
                ctx.not_checked.append(f"Gyro load on `{b.id}`: bearing {lay['d']:.1f}x{od:.1f} mm not in the rating table")
                continue
            if worst is None or rt[2] < worst[1][2]:
                worst = (b, rt)
        basis = f"turn rate {turn:.1f} rad/s ({src})"
        if worst is None:
            out.append(note("dynamics.gyro", G, "Gyro load computed",
                            f"`{p.id}`: {tau:.2f} N m precession couple at {basis}, {load:.0f} N on supports {span:.1f} mm apart."))
        elif load > worst[1][2]:
            out.append(fail("dynamics.gyro", G, WARNING, "Gyro load exceeds the bearing rating",
                            f"`{p.id}`: turning at {basis} gives a {tau:.2f} N m couple, {load:.0f} N on bearings {span:.1f} mm apart; "
                            f"`{worst[0].id}` ({worst[1][0]}) is rated {worst[1][2]} N static.").on(p.id, worst[0].id)
                       .expect(f"<= {worst[1][2]} N", f"{load:.0f} N").fix("Space the bearings further apart or use bigger bearings."))
        else:
            out.append(ok("dynamics.gyro", G, "Bearings take the gyro load",
                          f"`{p.id}`: {tau:.2f} N m at {basis} puts {load:.0f} N on bearings {span:.1f} mm apart "
                          f"(`{worst[0].id}` {worst[1][0]} rated {worst[1][2]} N static)."))
    return out
