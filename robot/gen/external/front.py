"""Front ground interface: full wedge, forks, wedgelets, skirt. Each bolts onto the front face of the chassis.

A wedge is a printed sloped plate (lip 0.6 mm off the floor, ribs underneath, a mounting web against the front wall)
printed standing on its mounting face (+y up) so the layers run along the slope. Forks and wedgelets are laser-cut
sheet tines (stock gauge) bolted through a printed fork bar.
"""

from __future__ import annotations

import math

from ..intent import I
from . import fasteners, sh

LIP_GAP = 0.6
WEDGE_T = 2.0
WEB_T = 2.4


def wedge_profile(y_root, z_root, y_tip, z_floor, t=WEDGE_T):
    """Parallelogram side profile (y, z) of the sloped plate: underside lip LIP_GAP above the floor."""
    b0, b1 = (y_root - 0.5, z_root - t), (y_tip, z_floor + LIP_GAP)
    ang = math.atan2(b0[1] - b1[1], b1[0] - b0[0])
    nx, nz = math.sin(ang) * t, math.cos(ang) * t
    return [b0, (b0[0] + nx, b0[1] + nz), (b1[0] + nx, b1[1] + nz), b1], math.degrees(ang)


def rib_profile(y_root, z_root, y_tip, z_floor, z_low, frac=0.55):
    """Triangular gusset under the plate from the root down to z_low, ending `frac` of the way to the tip."""
    yb = y_root + (y_tip - y_root) * frac
    zb = z_root - WEDGE_T + (z_floor + LIP_GAP - z_root + WEDGE_T) * frac
    return [(y_root - 0.5, z_root - WEDGE_T + 0.2), (yb, zb), (yb, z_low), (y_root, z_low)]


def add_wedge(plan, length=46.0, material="petg_cf", pid="wedge"):
    f = plan.frame
    yf, W = f.y1, f.x1
    z_floor = plan.extra.get("_floor_z")
    y_tip = yf + length
    prof, ang = wedge_profile(yf, 0.13, y_tip, z_floor)
    width = 2 * W - 2.0
    items = [sh.side_prism(prof, -width / 2, width / 2),
             sh.box(width, WEB_T, f.zt - f.zb - 0.35, (0, yf + WEB_T / 2, (f.zt + f.zb) / 2 - 0.175))]
    rib = rib_profile(yf, 0.13, y_tip, z_floor, f.zb)
    for x in _rib_xs(W):
        items.append(sh.place(sh.side_prism(rib, -0.6, 0.6), (x, 0, 0)))
    xs = [round(s * W * k, 1) for k in (0.4, 0.8) for s in (1, -1)]
    z_ins = round(f.zt * 0.6, 2)
    holes = [sh.cyl_axis(1.1, yf, yf + WEB_T + 1.6, "y", x, z_ins) for x in xs]
    trim = sh.box(width + 20, 10.0, 40.0, (0, yf - 5.0, 0))
    shape = sh.S(sh.U(*items), *holes, trim)
    plan.part(id=pid, kind="wedge", material=material, process="fdm", shape=shape, color="#ff6a1a",
              print_orientation="+y", label=f"printed wedge, {ang:.0f} deg ramp, lip {LIP_GAP} mm off the floor",
              intent=I("ground_game", "gets under the opponent first and lifts it off its wheels; ribs carry the "
                       "lip load back to the mounting web, printed on its web so layers run along the slope",
                       f"lip {LIP_GAP} mm off the floor (clears arena seams), {ang:.0f} deg, {WEDGE_T} mm plate, 7 ribs"))
    fasteners.add_front_inserts(plan, xs, z_ins, pid, plate_t=WEB_T)
    return y_tip, ang


def _rib_xs(W):
    n = 7
    return [round(-W + 1.0 + i * (2 * W - 2.0) / (n - 1), 2) for i in range(n)]


def add_skirt(plan, length=30.0, pid="skirt", t=2.0):
    """Flexible printed TPU skirt: a thin ramp that drags 0.3 mm off the floor (it flexes over bumps instead of
    lifting the robot), on a vertical flange screwed to the front wall like the wedge web. No ribs: it must flex."""
    f = plan.frame
    yf, W = f.y1, f.x1
    z_floor = plan.extra.get("_floor_z")
    y_tip = yf + length
    b0, b1 = (yf - 0.5, f.zb + 2.0), (y_tip, z_floor + 0.3)
    ang = math.atan2(b0[1] - b1[1], b1[0] - b0[0])
    nx, nz = math.sin(ang) * t, math.cos(ang) * t
    prof = [b0, (b0[0] + nx, b0[1] + nz), (b1[0] + nx, b1[1] + nz), b1]
    width = 2 * W - 2.0
    flange_z0 = f.zb + 0.2
    items = [sh.side_prism(prof, -width / 2, width / 2),
             sh.boxr(-width / 2, width / 2, yf, yf + WEB_T, flange_z0, f.zt * 0.8)]
    xs = [round(s * W * k, 1) for k in (0.4, 0.8) for s in (1, -1)]
    z_ins = round(f.zt * 0.45, 2)
    holes = [sh.cyl_axis(1.1, yf - 0.5, yf + WEB_T + 1.6, "y", x, z_ins) for x in xs]
    trim = sh.box(width + 20, 10.0, 40.0, (0, yf - 5.0, 0))
    plan.part(id=pid, kind="skirt", material="tpu", process="fdm", shape=sh.S(sh.U(*items), *holes, trim),
              color="#e0a020", print_orientation="+y",
              label=f"printed TPU skirt, {math.degrees(ang):.0f} deg, {t:g} mm, lip 0.3 mm off the floor",
              intent=I("ground_game", "a flexible skirt drags on the floor and bends over seams instead of lifting the "
                       "robot, so it wins the ground game against wedges", f"TPU {t} mm, lip 0.3 mm, no ribs (must flex)"))
    fasteners.add_front_inserts(plan, xs, z_ins, pid, plate_t=WEB_T)
    return y_tip, math.degrees(ang)


def add_plow(plan, length=30.0, pid="plow"):
    """Printed V plow: a wedge whose leading edge is swept back 25 deg either side of the centre line (deflects
    opponents sideways instead of only lifting them)."""
    f = plan.frame
    y_tip, ang = add_wedge(plan, length=length, pid=pid)
    part = next(p for p in plan.parts if p["id"] == pid)
    W = f.x1
    sweep = math.radians(25.0)
    dy = W * math.tan(sweep)
    for s in (1, -1):
        cut = sh.prism([(0, y_tip + 1.0), (s * (W + 2.0), y_tip + 1.0), (s * (W + 2.0), y_tip - dy)], 60.0, (0, 0, 0))
        part["shape"] = sh.S(part["shape"], cut)
    part["label"] = f"printed V plow, {ang:.0f} deg ramp, nose swept back 25 deg"
    plan.features[-1 - next(i for i, f in enumerate(reversed(plan.features)) if f["target"] == pid)]["intent"] = I(
        "ground_game", "the V nose deflects opponents to the side as well as lifting them, so a pusher can steer them "
        "into the wall", f"wedge {ang:.0f} deg with the edge swept back 25 deg")
    return y_tip, ang


def add_front(plan, kind):
    if kind == "skirt":
        return add_skirt(plan)
    if kind == "plow":
        return add_plow(plan)
    raise NotImplementedError(f"front interface {kind}")
