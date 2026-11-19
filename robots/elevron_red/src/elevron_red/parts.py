"""Elevron Red printed parts, built from the masters in params.py.

build(part=...) is the spec's `model` entry point. Left-hand (+x) parts are built once and mirrored.
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Axis, Box, Cylinder, Plane, Polygon, Pos, Rot, chamfer, extrude, mirror)  # noqa: E402

import params as P  # noqa: E402


def _box(x0, x1, y0, y1, z0, z1):
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _cyl_x(r, x0, x1, y, z):
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, x1 - x0)


def _plan(pts, z0, z1):
    """outline in (x, y) extruded from z0 to z1"""
    return Pos(0, 0, z0) * extrude(Polygon(*pts, align=None), z1 - z0, dir=(0, 0, 1))


def _side(pts, x0, x1):
    """outline in (y, z) extruded across x0..x1"""
    face = Plane.YZ.offset(x0) * Polygon(*pts, align=None)
    return extrude(face, x1 - x0, dir=(1, 0, 0))


def _both(fn):
    """a +x feature and its mirror"""
    s = fn()
    return s + mirror(s, Plane.YZ)


def _motor_env(side, y, grow):
    """N10 envelope (body only) at one wheel station, grown by `grow` per side"""
    xo = P.motor_origin_x()
    x0, x1 = xo - P.MOTOR_BACK - grow, xo + P.MOTOR_GB + grow
    s = _box(x0, x1, y - P.MOTOR_W / 2 - grow, y + P.MOTOR_W / 2 + grow, -P.MOTOR_H / 2 - grow, P.MOTOR_H / 2 + grow)
    return s if side > 0 else mirror(s, Plane.YZ)


def _stations():
    return [(sx, sy * P.AXLE_Y) for sx in (1, -1) for sy in (1, -1)]


# ---------------------------------------------------------------- chassis
def chassis():
    z0, z1 = P.ch_z0(), P.ch_top()
    hw = P.CH_W / 2
    body = _box(-hw, hw, P.CH_REAR, P.CH_FRONT, z0, z1)
    body = chamfer(body.edges().filter_by(Axis.X).group_by(Axis.Z)[-1].sort_by(Axis.Y)[-1], P.RAMP, P.RAMP)
    outer = body
    # wheel wells
    for sx, y in _stations():
        w = _box(P.well_x(), hw + 1, y - P.well_half(), y + P.well_half(), z0 - 1, z1 + 1)
        body -= w if sx > 0 else mirror(w, Plane.YZ)
    # hollow: one cavity, walls WALL, the ramp keeps its skin
    ch = P.cavity_half_w()
    cav = _box(-ch, ch, P.CH_REAR + P.WALL, P.CH_FRONT - P.WALL, P.floor_top(), z1 - P.WALL)
    ramp_cut = Pos(0, P.CH_FRONT, z1) * Rot(45, 0, 0) * Box(P.CH_W, P.RAMP * 1.42 + 2 * P.WALL * 1.42, P.RAMP * 1.42 + 2 * P.WALL * 1.42)
    body -= cav - ramp_cut
    # motor cradles: solid round each motor, open toward the cavity at the terminal end
    for sx, y in _stations():
        cr = _motor_env(sx, y, P.FIT + P.WALL)
        xo = P.motor_origin_x()
        reach = _box(xo - P.MOTOR_BACK, ch + 0.01, y - P.MOTOR_W / 2 - P.FIT - P.WALL, y + P.MOTOR_W / 2 + P.FIT + P.WALL,
                     P.floor_top() - 0.01, z1 - P.WALL + 0.01)
        body += (cr + (reach if sx > 0 else mirror(reach, Plane.YZ))) & outer
    for sx, y in _stations():
        body -= _motor_env(sx, y, P.FIT)
        # open the terminal end into the cavity
        xo = P.motor_origin_x()
        t = _box(xo - P.MOTOR_BACK - P.FIT - P.WALL - 1, xo - P.MOTOR_BACK, y - P.MOTOR_W / 2 + 1, y + P.MOTOR_W / 2 - 1,
                 -P.MOTOR_H / 2 + 1, P.MOTOR_H / 2 - 1)
        body -= t if sx > 0 else mirror(t, Plane.YZ)
        sh = _cyl_x(2.0, xo, P.CH_W, y, 0)
        body -= sh if sx > 0 else mirror(sh, Plane.YZ)
    # switch cradle on the floor, reached through a slot in the belly
    for sx, y in _stations():  # cradles stop at the wheel wells
        w = _box(P.well_x(), P.CH_W, y - P.well_half(), y + P.well_half(), z0 - 1, z1 + 1)
        body -= w if sx > 0 else mirror(w, Plane.YZ)
    g = P.FIT + P.WALL
    sw = _box(-P.SW_L / 2 - g, P.SW_L / 2 + g, P.SW_Y - P.SW_W / 2 - g, P.SW_Y + P.SW_W / 2 + g,
              P.floor_top() - 0.01, P.floor_top() + P.SW_H + g)
    body += sw
    body -= _box(-P.SW_L / 2 - P.FIT, P.SW_L / 2 + P.FIT, P.SW_Y - P.SW_W / 2 - P.FIT, P.SW_Y + P.SW_W / 2 + P.FIT,
                 P.floor_top(), P.floor_top() + P.SW_H + P.FIT)
    # lead window in the cap over the solder pins; the cap edges either side still hold the body down
    body -= _box(-P.SW_L / 2 + 0.5, P.SW_L / 2 - 0.5, P.SW_Y - P.SW_LEAD_W / 2, P.SW_Y + P.SW_LEAD_W / 2,
                 P.floor_top() + P.SW_H, P.floor_top() + P.SW_H + g + 1)
    slot = _box(-P.SW_L / 2 - P.FIT, P.SW_L / 2 + P.FIT, P.SW_Y - P.SW_W / 2 - P.FIT, P.SW_Y + P.SW_W / 2 + P.FIT, z0 - 1, P.floor_top() + 0.01)
    lips = _box(-P.SW_LIP_L / 2, P.SW_LIP_L / 2, P.SW_Y - P.SW_W / 2 - P.FIT, P.SW_Y + P.SW_W / 2 + P.FIT, z0 - 1, P.floor_top() + 0.01) - _box(
        -P.SW_LIP_L / 2 - 1, P.SW_LIP_L / 2 + 1, P.SW_Y - P.SW_W / 2 + P.SW_LIP_W, P.SW_Y + P.SW_W / 2 - P.SW_LIP_W, z0 - 2, P.floor_top() + 1)
    body -= slot - lips  # lips under the middle of the body hold it; the corners stay open to a finger
    # battery: closed cradle floor to roof, window on the lead face (+y)
    bx, by, bz = P.bat_center()
    g = P.FIT + P.WALL
    bl, bw = P.BAT_W, P.BAT_L  # turned lengthwise: x extent, y extent
    body += _box(bx - bl / 2 - g, bx + bl / 2 + g, by - bw / 2 - g, by + bw / 2 + g, P.floor_top() - 0.01, bz + P.BAT_H / 2 + g)
    body -= _box(bx - bl / 2 - P.FIT, bx + bl / 2 + P.FIT, by - bw / 2 - P.FIT, by + bw / 2 + P.FIT,
                 P.floor_top(), bz + P.BAT_H / 2 + P.FIT)
    # lead window on the inboard face (the catalog lead leaves the pack's +y face, -x once turned)
    body -= _box(bx + bl / 2 - 1, bx + bl / 2 + g + 1, by - bw / 2 + 3, by + bw / 2 - 3,
                 P.floor_top() + 1, bz + P.BAT_H / 2 - 1)
    # side panel key slots between the wheels
    for sx in (1, -1):
        k = _box(P.CH_W / 2 - P.TAB - P.FIT, P.CH_W / 2 + 1, -P.mid_half_y() - P.FIT, P.mid_half_y() + P.FIT,
                 P.WEB_Z0 - P.FIT, P.SP_LOW + P.FIT)
        body -= k if sx > 0 else mirror(k, Plane.YZ)
    # servo lead hole into the housing
    lx, ly, _ = P.servo_lead()
    lx = P.world_x(lx)
    body -= _box(lx - 3, lx + 3, ly - 1, ly + 5, z1 - P.WALL - 1, z1 + 1)
    return body


def servo_env(grow=0.0):
    """CS07 envelope at its spec pose (body + ear plate), grown by `grow`"""
    sx, sy, sz = P.servo_box()
    cx, cy, cz = P.servo_center()
    body = _box(cx - sx / 2 - grow, cx + sx / 2 + grow, cy - sy / 2 - grow, cy + sy / 2 + grow, cz - sz / 2 - grow, cz + sz / 2 + grow)
    ear_x = cx + 6.9
    ears = _box(ear_x - 1.25 - grow, ear_x + 1.25 + grow, cy - P.SERVO_EAR_L / 2 - grow, cy + P.SERVO_EAR_L / 2 + grow,
                cz - sz / 2 - grow, cz + sz / 2 + grow)
    return body + ears


def _housing_shell(x0, x1, y0, y1, z0, z1):
    """the housing block: 45 degree chamfers along the top sides and a sloped nose"""
    h = _box(x0, x1, y0, y1, z0, z1)
    top = h.edges().group_by(Axis.Z)[-1]
    h = chamfer(top.filter_by(Axis.Y), P.HOUSING_CHAMFER)
    nose = min(P.HOUSING_NOSE, P.housing_top() - P.ch_top() - P.HOUSING_CHAMFER - 1)
    return chamfer(h.edges().group_by(Axis.Z)[-1].filter_by(Axis.X).sort_by(Axis.Y)[-1], nose)


def housing():
    """red servo housing on the chassis top, beside the arm (printed with the chassis: it sinks one wall into the roof)"""
    x0, x1 = P.HOUSING_X0, P.housing_x1()
    z0, z1 = P.ch_top(), P.housing_top()
    y0, y1 = P.CH_REAR, P.HOUSING_FRONT
    w = P.WALL
    h = _housing_shell(x0, x1, y0, y1, z0 - w, z1)
    # hollow: same block shrunk by one wall, open onto the chassis roof
    h -= _housing_shell(x0 + w, x1 - w, y0 + w, y1 - w, z0, z1 - w) - servo_env(P.FIT + w)
    # pivot lug at the rear, carrying the arm pin
    px, py, pz = P.pivot()
    r = P.ARM_BOSS_R
    lug = _side([(y0, z1 - 1), (py + r + 4, z1 - 1), (py + r, pz), (py - r, pz + r * 0.6), (y0, pz)], x1 - P.LUG_T, x1)
    h += lug + _cyl_x(r, x1 - P.LUG_T, x1, py, pz) + _box(x1 - P.LUG_T, x1, y0, py + r + 4, z0 - w, z1)
    h -= _cyl_x(1.6, x1 - P.LUG_T - 1, x1 + 1, py, pz)
    h -= servo_env(P.FIT)
    lx, ly, lz = P.servo_lead()  # lead chimney down into the chassis
    h -= _box(lx - 3, lx + 3, ly - 1, ly + 5, z0 - P.WALL - 1, lz + 3)
    # output spline through the arm-side wall
    ox, oy, oz = P.servo_out()
    h -= _cyl_x(2.6, x1 - P.WALL - 1, x1 + 1, oy, oz)
    return h


def arm_profile():
    """(y, z) outline of the arm plate: boss at the pivot, top raked down to a blade tip at the floor"""
    px, py, pz = P.pivot()
    r = P.ARM_BOSS_R
    zb = P.ch_top() + P.CLEAR
    g = P.ground_z() + 0.6
    knee = P.CH_FRONT + 2.0
    tip = (P.ARM_TIP_Y, g + P.FORK_TIP_H)
    top0 = (py, pz + r)
    # top edge: one straight rake from the boss to the blade tip
    return [(py, pz - r), (py + 2 * r, pz - P.ARM_DEPTH * 0.9), (knee - 10, zb), (knee, zb), (P.ARM_TIP_Y, g), tip,
            (knee + 6, zb + P.ARM_NOSE), top0]


def _arm_plate():
    s = _side(arm_profile(), P.arm_x0(), P.arm_x1())
    px, py, pz = P.pivot()
    return s + _cyl_x(P.ARM_BOSS_R, P.arm_x0(), P.arm_x1(), py, pz)


def _rail(depth=None, blade=None):
    """red top band of the plate (`depth` deep, forward of the boss) plus the blade tip (`blade` long)"""
    depth = P.ARM_RAIL if depth is None else depth
    blade = P.ARM_BLADE if blade is None else blade
    plate = _side(arm_profile(), P.arm_x0(), P.arm_x1())
    px, py, pz = P.pivot()
    band = plate - Pos(0, 0, -depth) * plate
    band &= _box(P.arm_x0() - 1, P.arm_x1() + 1, py + P.ARM_BOSS_R, P.ARM_TIP_Y + 1, -50, 50)
    tip = plate & _box(P.arm_x0() - 1, P.arm_x1() + 1, P.ARM_TIP_Y - blade, P.ARM_TIP_Y + 1, -50, 50)
    return band + tip


def arm():
    """black plate; it keeps FUSE_LAP under the rail so the two colours print as one body"""
    px, py, pz = P.pivot()
    s = _arm_plate() - _rail(P.ARM_RAIL - P.FUSE_LAP, P.ARM_BLADE - P.FUSE_LAP)
    # layered arm: two black side plates under the red top, open underneath between the boss and the blade
    plate = _side(arm_profile(), P.arm_x0(), P.arm_x1())
    inner = (Pos(0, 0, -P.ARM_RAIL - P.WALL) * plate) & _box(P.arm_x0() + P.WALL, P.arm_x1() - P.WALL, py + P.ARM_BOSS_R + 2,
                                                     P.CH_FRONT - 8.0, -50, 50)  # stops before the knee
    s -= inner
    return s - _cyl_x(1.6, P.arm_x0() - 1, P.arm_x1() + 1, py, pz)  # horn screw / spline seat


def arm_rail():
    """printed with the arm (second colour)"""
    return _rail()


def horn():
    """white servo horn on the output spline, standing up in the gap between the housing and the arm"""
    ox, oy, oz = P.servo_out()
    x0, x1 = ox + P.HORN_GAP, ox + P.ARM_GAP - P.HORN_GAP
    hub = _cyl_x(P.HORN_HUB_R, x0, x1, oy, oz)
    lever = _side([(oy - P.HORN_W / 2, oz), (oy + P.HORN_W / 2, oz), (oy + P.HORN_W * 0.35, oz + P.HORN_L),
                   (oy - P.HORN_W * 0.35, oz + P.HORN_L)], x0, x1)
    tip = _cyl_x(P.HORN_W * 0.35, x0, x1, oy, oz + P.HORN_L)
    return hub + lever + tip - _cyl_x(0.8, x0 - 1, x1 + 1, oy, oz + P.HORN_L)


# ---------------------------------------------------------------- side panels (+x built, -x mirrored)
def side_plan():
    xi, xo = P.pod_inner_x(), P.SP_OUT
    my = P.mid_half_y()
    xc = P.CH_W / 2 - P.TAB
    fy = P.pod_front_y()
    tip = P.FORK_TIP_Y
    return [(xi, P.SP_REAR), (xo - 3, P.SP_REAR), (xo, P.SP_REAR + 6), (xo, fy + P.POD_NOSE), (xi + P.FORK_W_ROOT * 0.75, fy + P.POD_NOSE + 10),
            (xi + P.FORK_W_TIP, tip), (xi, tip), (xi - 1.5, fy + 6), (xi - 1.5, fy), (xi, fy - 1),
            (xi, my), (xc, my), (xc, -my), (xi, -my)]


def side_profile():
    g = P.ground_z() + 0.5
    t, lo = P.SP_TOP, P.SP_LOW
    fy = P.pod_front_y()
    tip = P.FORK_TIP_Y
    return [(P.SP_REAR - 1, g), (tip + 1, g), (tip + 1, g + P.FORK_TIP_H), (tip - 12, g + 6.0), (tip - 12, g + 4.6),
            (fy + P.POD_NOSE, t), (P.AXLE_Y - 4, t), (P.AXLE_Y - 9, lo), (P.SP_REAR + 4, lo), (P.SP_REAR - 1, g + 4)]


def side_panel():
    plan = _plan(side_plan(), P.ground_z(), P.SP_TOP + 1)
    prof = _side(side_profile(), 0, P.SP_OUT + 2)
    s = plan & prof
    # hollow the pods (open underneath, printed top down)
    xi, xo = P.pod_inner_x(), P.SP_OUT
    sk = P.POD_SKIN
    fy = P.pod_front_y()
    s -= _box(xi + sk, xo - sk, P.SP_REAR + 6, P.AXLE_Y - 9 - sk, P.ground_z(), P.SP_LOW - sk)
    s -= _box(xi + sk, xo - sk, P.AXLE_Y - 3, fy + P.POD_NOSE - sk, P.ground_z(), P.SP_TOP - sk)
    # web between the wheels only from the axle up
    s -= _box(P.CH_W / 2 - P.TAB - 1, xi + sk, -P.mid_half_y() - 1, P.mid_half_y() + 1, P.ground_z() - 1, P.WEB_Z0)
    # web: a top plate over the gap between the wheels, keyed into the chassis wall by its inner edge
    s -= _box(P.CH_W / 2 + P.FIT, xi + sk, -P.mid_half_y() + sk, P.mid_half_y() - sk, P.WEB_Z0 - 1, P.SP_LOW - P.WEB_PLATE)
    # vent grooves on the outer face of each pod (photo: III on the rear pod, IIIII on the front pod)
    for y0, y1, top, n in ((P.SP_REAR + 6, -P.mid_half_y() - 2, P.SP_LOW, 3), (P.AXLE_Y - 2, fy + P.POD_NOSE - 4, P.SP_TOP, 5)):
        pitch = (y1 - y0) / n
        for i in range(n):
            yc = y0 + pitch * (i + 0.5)
            s -= _box(xo - P.VENT_D, xo + 1, yc - P.VENT_W / 2, yc + P.VENT_W / 2, P.ground_z() + 3, top - 2.5)
    return s


def side_panel_r():
    return mirror(side_panel(), Plane.YZ)


# ---------------------------------------------------------------- wheels
def tyre(sx=1, sy=1):
    x, y = sx * P.TRACK_X, sy * P.AXLE_Y
    return _cyl_x(P.WHEEL_R, x - P.WHEEL_W / 2, x + P.WHEEL_W / 2, y, 0) - _cyl_x(P.HUB_R, x - P.WHEEL_W, x + P.WHEEL_W, y, 0)


def hub(sx=1, sy=1):
    x0, x1 = P.tyre_x0(), P.tyre_x0() + P.WHEEL_W
    y = sy * P.AXLE_Y
    h = _cyl_x(P.HUB_R, x0, x1, y, 0)
    h -= _cyl_x(1.55, x0 - 1, x0 + P.SHAFT_BITE + 0.5, y, 0)
    return h if sx > 0 else mirror(h, Plane.YZ)


def _module(fn):
    def f():
        s = fn()
        return mirror(s, Plane.YZ) if P.MODULE_SIDE < 0 else s
    return f


PARTS = {"chassis": chassis, "housing": _module(housing), "arm": _module(arm), "arm_rail": _module(arm_rail), "horn": _module(horn),
         "side_l": side_panel, "side_r": side_panel_r}


def build(part, sx=1, sy=1):
    if part == "tyre":
        return tyre(sx, sy)
    if part == "hub":
        return hub(sx, sy)
    return PARTS[part]()
