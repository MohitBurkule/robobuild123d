"""Elevron Red printed parts, built from the masters in params.py.

build(part=...) is the spec's `model` entry point. Right-hand (+x) parts are built once and mirrored; the lifter
module (housing, cover, arm, horn) is drawn housing-left and mirrored so the housing sits on +x (robot right, photo).
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from build123d import (Axis, Box, Cylinder, Plane, Polygon, Pos, RegularPolygon, Rot, chamfer, extrude, fillet,  # noqa: E402
                       mirror)

import params as P  # noqa: E402

# build constants (not robot dimensions): overlaps that make booleans clean, and cut lengths
EPS = 0.01               # coplanar-face nudge
LAP = 0.3                # a post / boss reaches this far into the plate it hangs from
FAR = 60.0               # half-length of a cut that must pass through everything
SQ2 = 2 ** 0.5
# feature sizes read off the photos / the catalog parts (mm)
SHAFT_SLOT_R = 2.0       # N10 shaft clearance (3 mm shaft, 0.5 mm play)
LEAD_HALF = 3.0          # servo lead chimney half-width
LEAD_BACK, LEAD_FWD = 1.0, 3.5   # chimney reach behind / ahead of the lead exit
LEAD_UP = 3.0            # chimney top above the lead exit
SPLINE_R = 2.6           # servo output boss clearance
EAR_OFF, EAR_T = 6.9, 2.5   # CS07 ear plate: offset from the body centre along the output axis, thickness
BAT_WIN_IN, BAT_WIN_END = 1.0, 3.0   # battery lead window: depth into the wall, margin from the pack ends
ESC_LIP = 1.0            # ESC side walls stop this far below the board top
ESC_GAP, ESC_SLOT_IN = 2.5, 1.0   # ESC end openings: margin from the corners, depth
ESC_SLOT_Z = 0.6         # ESC end openings start this far above the floor
MOTOR_PAD = (8.0, 4.0, 4.0)   # lid pad over a motor: reach behind / ahead of the motor origin, half-width
BAT_POST_DY, ESC_POST_DY, POST_R = 7.0, 6.0, 2.5   # lid posts on the battery and the ESC
SW_POST_IN, SW_POST_OUT, SW_POST_HW = 1.4, 0.2, 1.5   # lid posts on the switch ends
LUG_RISE = 4.0           # lug top runs this far ahead of the boss
LUG_DROP = 1.0           # lug top sits this far under the housing top
LUG_SLOPE = 0.6          # rear lug edge rise per boss radius
KNEE_FWD = 2.0           # arm knee ahead of the chassis front
KNEE_RUN = 10.0          # arm underside flat behind the knee
NOSE_RUN = 6.0           # arm top nose ahead of the knee
BOSS_DROP = 0.9          # arm underside under the boss, fraction of ARM_DEPTH
ARM_CH_BACK = 8.0        # arm underside channel stops this far behind the chassis front
ARM_CH_GAP = 2.0         # channel starts this far ahead of the boss
TIP_LIFT = 0.6           # arm blade tip above the floor
HORN_TAPER = 0.35        # horn half-width at its tip, fraction of HORN_W
HORN_PIN_R = 0.8         # link pin hole in the horn tip
HUB_BORE_R = 1.55        # D-bore radius on the 3 mm shaft
HUB_BITE_EXTRA = 0.5
POD_REAR_CHAMFER, POD_REAR_RUN = 3.0, 6.0   # side plan rear corner chamfer (x, y)
FORK_ROOT_F = 0.75       # fork plan root, fraction of FORK_W_ROOT
FORK_KNEE = 10.0         # fork plan straight run past the pod nose
INNER_STEP, INNER_RUN = 1.5, 6.0   # front pod inner relief
SAW_BACK, SAW_HI, SAW_LO = 12.0, 6.0, 4.6   # fork saw-tooth step: distance from the tip, top heights above the sole
SOLE = 0.5               # side panel sole above the floor
POD_TOP_RUN, POD_TOP_DROP = 4.0, 9.0   # front pod top ends ahead / rear pod top starts behind the axle
REAR_TAIL = 4.0          # rear pod tail chamfer
REAR_HOLLOW_IN = 6.0
FRONT_HOLLOW_BACK = 3.0
FORK_HOLLOW_END = 14.0   # fork hollow stops this far behind the tip (before the saw-tooth)
VENT_LOW, VENT_TOP = 3.0, 2.5   # vent grooves: above the sole, below the pod top
VENT_REAR_END, VENT_FRONT_START, VENT_FRONT_END = 2.0, 2.0, 4.0
REAR_VENTS, FRONT_VENTS = 3, 5


def _box(x0, x1, y0, y1, z0, z1):
    x0, x1 = sorted((x0, x1)); y0, y1 = sorted((y0, y1)); z0, z1 = sorted((z0, z1))
    return Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * Box(x1 - x0, y1 - y0, z1 - z0)


def _cyl_x(r, x0, x1, y, z):
    return Pos((x0 + x1) / 2, y, z) * Rot(0, 90, 0) * Cylinder(r, x1 - x0)


def _cyl_z(r, x, y, z0, z1):
    return Pos(x, y, (z0 + z1) / 2) * Cylinder(r, z1 - z0)


def _plan(pts, z0, z1):
    """outline in (x, y) extruded from z0 to z1"""
    return Pos(0, 0, z0) * extrude(Polygon(*pts, align=None), z1 - z0, dir=(0, 0, 1))


def _side(pts, x0, x1):
    """outline in (y, z) extruded across x0..x1"""
    face = Plane.YZ.offset(x0) * Polygon(*pts, align=None)
    return extrude(face, x1 - x0, dir=(1, 0, 0))


def _mx(s, sx):
    return s if sx > 0 else mirror(s, Plane.YZ)


def _motor_env(side, y, grow):
    """N10 envelope (body only) at one wheel station, grown by `grow` per side"""
    xo = P.motor_origin_x()
    x0, x1 = xo - P.MOTOR_BACK - grow, xo + P.MOTOR_GB + grow
    return _mx(_box(x0, x1, y - P.MOTOR_W / 2 - grow, y + P.MOTOR_W / 2 + grow, -P.MOTOR_H / 2 - grow, P.MOTOR_H / 2 + grow), side)


def _stations():
    return [(sx, sy * P.AXLE_Y) for sx in (1, -1) for sy in (1, -1)]


# ---------------------------------------------------------------- chassis tub + lid
def _well(sx, y):
    """wheel well cut, its two inner vertical corners rounded"""
    w = _box(P.well_x(), P.CH_W, y - P.well_half(), y + P.well_half(), P.ch_z0() - 1, P.ch_top() + 1)
    try:
        w = fillet(w.edges().filter_by(Axis.Z).sort_by(Axis.X)[:2], P.WELL_R)
    except Exception:
        pass
    return _mx(w, sx)


def _outer():
    """chassis block with the ramp chamfer and the wheel wells"""
    hw = P.CH_W / 2
    body = _box(-hw, hw, P.CH_REAR, P.CH_FRONT, P.ch_z0(), P.ch_top())
    body = chamfer(body.edges().filter_by(Axis.X).group_by(Axis.Z)[-1].sort_by(Axis.Y)[-1], P.RAMP, P.RAMP)
    for sx, y in _stations():
        body -= _well(sx, y)
    return body


def _lid_zone(y1):
    """everything above the lid underside behind y1: the lid's share of the block"""
    return _box(-P.CH_W, P.CH_W, P.CH_REAR - 1, y1, P.lid_z0(), P.ch_top() + 1)


def _key_slot(sx):
    """slot in the chassis flank that takes the side panel's web tongue"""
    ky = P.mid_half_y() - P.KEY_TRIM
    return _mx(_box(P.CH_W / 2 - P.TAB - P.FIT, P.CH_W / 2 + 1, -ky - P.FIT, ky + P.FIT, P.WEB_Z0 - P.FIT, P.SP_LOW + P.FIT), sx)


def _tub():
    z0, z1 = P.ch_z0(), P.ch_top()
    body = _outer()
    outer = body
    ch = P.cavity_half_w()
    g = P.FIT + P.WALL
    # hollow: one cavity, walls WALL, the ramp keeps its skin
    cav = _box(-ch, ch, P.CH_REAR + P.WALL, P.CH_FRONT - P.WALL, P.floor_top(), z1 - P.WALL)
    skin = (P.RAMP + 2 * P.WALL) * SQ2
    body -= cav - Pos(0, P.CH_FRONT, z1) * Rot(45, 0, 0) * Box(P.CH_W, skin, skin)
    xo = P.motor_origin_x()
    # motor cradles: solid round each motor, reaching the cavity wall
    for sx, y in _stations():
        reach = _box(xo - P.MOTOR_BACK, ch + EPS, y - P.MOTOR_W / 2 - g, y + P.MOTOR_W / 2 + g, P.floor_top() - EPS, z1 - P.WALL + EPS)
        body += (_motor_env(sx, y, g) + _mx(reach, sx)) & outer
    # lid screw columns, floor to the lid
    for x, y in P.LID_SCREWS:
        body += _cyl_z(P.COL_R, x, y, P.floor_top() - EPS, P.lid_z0()) & outer
    # side panel screw blocks on the flanks between the wheels
    for sx in (1, -1):
        for sy in (1, -1):
            body += _mx(_box(P.CH_W / 2 - P.FIT, P.SB_X1, sy * P.SB_Y - P.SB_HALF, sy * P.SB_Y + P.SB_HALF, P.SB_Z0,
                             P.SP_LOW - P.WEB_PLATE), sx)
        body -= _key_slot(sx)
    # pilot holes started in the columns and blocks (the screws go in from above)
    for x, y in P.LID_SCREWS:
        body -= _cyl_z(P.PILOT_R, x, y, P.lid_z0() - P.PILOT_PRE, P.lid_z0() + 1)
    for sx in (1, -1):
        for sy in (1, -1):
            body -= _cyl_z(P.PILOT_R, sx * P.SIDE_SCREW_X, sy * P.SB_Y, P.SP_LOW - P.WEB_PLATE - P.PILOT_PRE, P.SP_LOW)
    # the top comes off as the lid (and the ramp's top edge with it, so no knife edge is left)
    body -= _lid_zone(P.CH_FRONT - P.RAMP + P.LID_T)
    # behind the ramp the skin's inner face would run out to a knife edge at the lid plane: stop it square
    body -= _box(-P.CH_W, P.CH_W, P.CH_FRONT - P.RAMP - 2 * P.WALL - 1, P.CH_FRONT - P.RAMP, P.ch_top() - 2 * P.WALL, P.ch_top() + 1)
    for sx, y in _stations():
        # motor drops in from above: pocket and shaft slot open to the top
        body -= _mx(_box(xo - P.MOTOR_BACK - P.FIT, xo + P.MOTOR_GB + P.FIT, y - P.MOTOR_W / 2 - P.FIT, y + P.MOTOR_W / 2 + P.FIT,
                         -P.MOTOR_H / 2 - P.FIT, P.CH_H), sx)
        body -= _mx(_box(xo - P.MOTOR_BACK - g - EPS, xo - P.MOTOR_BACK, y - P.MOTOR_W / 2 + 1, y + P.MOTOR_W / 2 - 1,
                         -P.MOTOR_H / 2 + 1, P.MOTOR_H / 2 - 1), sx)   # terminal end open to the cavity
        body -= _mx(_cyl_x(SHAFT_SLOT_R, xo, P.CH_W, y, 0) + _box(xo, P.CH_W, y - SHAFT_SLOT_R, y + SHAFT_SLOT_R, 0, P.CH_H), sx)
        body -= _well(sx, y)   # cradles stop at the wheel wells
    # switch cradle on the floor, open on top (the lid posts hold it), worked through a slot in the belly
    sw = (-P.SW_L / 2 - P.FIT, P.SW_L / 2 + P.FIT, P.SW_Y - P.SW_W / 2 - P.FIT, P.SW_Y + P.SW_W / 2 + P.FIT)
    body += _box(sw[0] - P.WALL, sw[1] + P.WALL, sw[2] - P.WALL, sw[3] + P.WALL, P.floor_top() - EPS, P.floor_top() + P.SW_H)
    body -= _box(*sw, P.floor_top(), z1)
    lips = _box(-P.SW_LIP_L / 2, P.SW_LIP_L / 2, sw[2], sw[3], z0 - 1, P.floor_top() + EPS) - _box(
        -P.SW_LIP_L / 2 - 1, P.SW_LIP_L / 2 + 1, sw[2] + P.FIT + P.SW_LIP_W, sw[3] - P.FIT - P.SW_LIP_W, z0 - 2, P.floor_top() + 1)
    body -= _box(*sw, z0 - 1, P.floor_top() + EPS) - lips   # lips under the middle of the body; the corners stay open to a finger
    # battery: cradle walls round the pack, open on top (the lid posts hold it), window on the lead face
    bx, by, bz = P.bat_center()
    bl, bw = P.BAT_W, P.BAT_L  # turned lengthwise: x extent, y extent
    body += _box(bx - bl / 2 - g, bx + bl / 2 + g, by - bw / 2 - g, by + bw / 2 + g, P.floor_top() - EPS, bz + P.BAT_H / 2)
    body -= _box(bx - bl / 2 - P.FIT, bx + bl / 2 + P.FIT, by - bw / 2 - P.FIT, by + bw / 2 + P.FIT, P.floor_top(), z1)
    body -= _box(bx + bl / 2 - BAT_WIN_IN, bx + bl / 2 + g + 1, by - bw / 2 + BAT_WIN_END, by + bw / 2 - BAT_WIN_END, P.floor_top() + 1, z1)
    # ESC: side walls and corner stops, ends open for the leads
    ex, ey, ez = P.esc_center()
    el, ew = P.ESC_W, P.ESC_L
    body += _box(ex - el / 2 - g, ex + el / 2 + g, ey - ew / 2 - g, ey + ew / 2 + g, P.floor_top() - EPS, ez + P.ESC_H / 2 - ESC_LIP)
    body -= _box(ex - el / 2 - P.FIT, ex + el / 2 + P.FIT, ey - ew / 2 - P.FIT, ey + ew / 2 + P.FIT, P.floor_top(), z1)
    for sy in (1, -1):
        body -= _box(ex - el / 2 + ESC_GAP, ex + el / 2 - ESC_GAP, ey + sy * (ew / 2 - ESC_SLOT_IN), ey + sy * (ew / 2 + g + 1),
                     P.floor_top() + ESC_SLOT_Z, z1)
    return body


def chassis():
    return _tub()


def _post(x, y, z0, r):
    """a lid post from z0 up into the lid plate"""
    return _cyl_z(r, x, y, z0, P.lid_z0() + LAP)


def lid():
    """black top plate screwed onto the tub; the red housing is printed on it (second colour, `fused_with`).
    Posts on its underside close the open-top cradles of the motors, the battery, the ESC and the switch."""
    lid = _outer() & _lid_zone(P.CH_FRONT - P.RAMP)
    for x, y in P.LID_SCREWS:
        lid += _cyl_z(P.LID_BOSS_R, x, y, P.ch_top() - LAP, P.ch_top() + P.LID_BOSS_H)
    xo = P.motor_origin_x()
    back, fwd, hw = MOTOR_PAD
    for sx, y in _stations():
        lid += _mx(_box(xo - back, xo + fwd, y - hw, y + hw, P.MOTOR_H / 2 + P.FIT, P.lid_z0() + LAP), sx)
    bx, by, bz = P.bat_center()
    ex, ey, ez = P.esc_center()
    for sy in (1, -1):
        lid += _post(bx, by + sy * BAT_POST_DY, bz + P.BAT_H / 2 + P.FIT, POST_R)
        lid += _post(ex, ey + sy * ESC_POST_DY, ez + P.ESC_H / 2 + P.FIT, POST_R)
    s = _box(P.SW_L / 2 - SW_POST_IN, P.SW_L / 2 + SW_POST_OUT, P.SW_Y - SW_POST_HW, P.SW_Y + SW_POST_HW,
             P.floor_top() + P.SW_H + P.FIT, P.lid_z0() + LAP)
    lid += s + mirror(s, Plane.YZ)
    lx, ly, _ = P.servo_lead()
    lid -= _box(P.world_x(lx) - LEAD_HALF, P.world_x(lx) + LEAD_HALF, ly - LEAD_BACK, ly + LEAD_FWD, P.lid_z0() - 1, P.ch_top() + 1)
    return lid


# ---------------------------------------------------------------- lifter module (drawn housing-left, see _module)
def servo_env(grow=0.0):
    """CS07 envelope at its spec pose (body + ear plate), grown by `grow`"""
    sx, sy, sz = P.servo_box()
    cx, cy, cz = P.servo_center()
    body = _box(cx - sx / 2 - grow, cx + sx / 2 + grow, cy - sy / 2 - grow, cy + sy / 2 + grow, cz - sz / 2 - grow, cz + sz / 2 + grow)
    ear_x = cx + EAR_OFF
    ears = _box(ear_x - EAR_T / 2 - grow, ear_x + EAR_T / 2 + grow, cy - P.SERVO_EAR_L / 2 - grow, cy + P.SERVO_EAR_L / 2 + grow,
                cz - sz / 2 - grow, cz + sz / 2 + grow)
    return body + ears


def _housing_shell(x0, x1, y0, y1, z0, z1, inset=0.0):
    """the housing block: 45 degree chamfers along the top sides and a sloped nose; `inset` > 0 gives the inner
    surface one wall in (its chamfers shrink so the slopes stay parallel to the outside)"""
    shrink = inset * (2 - SQ2)
    h = _box(x0, x1, y0, y1, z0, z1)
    h = chamfer(h.edges().group_by(Axis.Z)[-1].filter_by(Axis.Y), P.HOUSING_CHAMFER - shrink)
    nose = min(P.HOUSING_NOSE, P.housing_top() - P.ch_top() - P.HOUSING_CHAMFER - 1) - shrink
    return chamfer(h.edges().group_by(Axis.Z)[-1].filter_by(Axis.X).sort_by(Axis.Y)[-1], nose)


def _lug():
    """pivot lug on the arm side of the housing, rear end"""
    x1 = P.housing_x1()
    z0, z1 = P.ch_top(), P.housing_top()
    y0 = P.CH_REAR
    px, py, pz = P.pivot()
    r = P.ARM_BOSS_R
    lug = _side([(y0, z1 - LUG_DROP), (py + r + LUG_RISE, z1 - LUG_DROP), (py + r, pz), (py - r, pz + r * LUG_SLOPE), (y0, pz)],
                x1 - P.LUG_T, x1)
    return lug + _cyl_x(r, x1 - P.LUG_T, x1, py, pz) + _box(x1 - P.LUG_T, x1, y0, py + r + LUG_RISE, z0 - P.WALL, z1)


def _housing_solid():
    """the housing block before the split: shell, cover screw columns, pivot lug"""
    x0, x1 = P.HOUSING_X0, P.housing_x1()
    z0, z1 = P.ch_top(), P.housing_top()
    y0, y1 = P.CH_REAR, P.HOUSING_FRONT
    w = P.WALL
    outer = _housing_shell(x0, x1, y0, y1, z0 - w, z1)
    h = outer - (_housing_shell(x0 + w, x1 - w, y0 + w, y1 - w, z0, z1 - w, inset=w) - servo_env(P.FIT + w))
    for x, y in P.COVER_COLS:
        h += _cyl_z(P.COVER_COL_R, x, y, z0, z1) & outer
        h -= _cyl_z(P.PILOT_R, x, y, P.z_split() - P.PILOT_PRE, P.z_split())
    return h + _lug()


def _cover_zone():
    """the cover: everything above the servo top, from the rear to just ahead of the cover screws"""
    return _box(P.HOUSING_X0 - 1, P.housing_x1() + 1, P.CH_REAR - 1, P.COVER_Y1, P.z_split(), FAR)


def _servo_cuts():
    px, py, pz = P.pivot()
    cut = servo_env(P.FIT)
    cut += (Pos(0, 0, LAP) * cut) & _box(-FAR, FAR, -FAR, FAR, 0, P.z_split())   # open up to the split: the servo lifts out
    lx, ly, lz = P.servo_lead()  # lead chimney down into the lid
    cut += _box(lx - LEAD_HALF, lx + LEAD_HALF, ly - LEAD_BACK, ly + LEAD_FWD, P.lid_z0() - 1, lz + LEAD_UP)
    # output spline through the arm-side wall: a U-slot open to the split so the servo lifts out
    ox, oy, oz = P.servo_out()
    x0, x1 = P.housing_x1() - P.WALL - 1, P.housing_x1() + 1
    cut += _cyl_x(SPLINE_R, x0, x1, oy, oz) + _box(x0, x1, oy - SPLINE_R, oy + SPLINE_R, oz, P.z_split() + EPS)
    # pivot screw hole and a hex pocket for its nut on the lug's outer face
    lx0 = P.housing_x1() - P.LUG_T
    cut += _cyl_x(P.PIVOT_D / 2 + P.FIT / 2, lx0 - 1, P.housing_x1() + 1, py, pz)
    nut = Pos(lx0 + P.NUT_T / 2 - EPS, py, pz) * Rot(0, 90, 0) * extrude(RegularPolygon(P.NUT_AF / 3 ** 0.5 + P.FIT / 2, 6), P.NUT_T,
                                                                          both=True)
    return cut + nut


def housing():
    """red servo housing on the lid, open on top over the servo; the cover closes it"""
    return (_housing_solid() - _cover_zone()) - _servo_cuts()


def cover():
    """red servo cover with the pivot lug, screwed down into the housing columns ("01" on top); a pad on its
    underside comes down to SERVO_HOLD over the servo so it cannot lift"""
    sx, sy, sz = P.servo_box()
    cx, cy, cz = P.servo_center()
    pad = _box(cx - sx / 2 + P.WALL, cx + sx / 2 - P.WALL, cy - sy / 2 + P.WALL, cy + sy / 2 - P.WALL, cz + sz / 2 + P.SERVO_HOLD, P.z_split() + EPS)
    return ((_housing_solid() & _cover_zone()) - _servo_cuts()) + pad


def arm_profile():
    """(y, z) outline of the arm plate: boss at the pivot, top raked down to a blade tip at the floor"""
    px, py, pz = P.pivot()
    r = P.ARM_BOSS_R
    zb = P.ch_top() + P.CLEAR
    g = P.ground_z() + TIP_LIFT
    knee = P.CH_FRONT + KNEE_FWD
    tip = (P.ARM_TIP_Y, g + P.FORK_TIP_H)
    top0 = (py, pz + r)
    # top edge: a rake from the boss to the blade tip with one step down part way (photo)
    a = (knee + NOSE_RUN, zb + P.ARM_NOSE)
    t = P.ARM_STEP_AT
    s = (top0[0] + (a[0] - top0[0]) * t, top0[1] + (a[1] - top0[1]) * t)
    return [(py, pz - r), (py + 2 * r, pz - P.ARM_DEPTH * BOSS_DROP), (knee - KNEE_RUN, zb), (knee, zb), (P.ARM_TIP_Y, g), tip,
            a, (s[0] + P.ARM_STEP, s[1] - P.ARM_STEP), s, top0]


def _plate():
    return _side(arm_profile(), P.arm_x0(), P.arm_x1())


def _rail(depth=None, blade=None):
    """red top band of the plate (`depth` deep, forward of the boss) plus the blade tip (`blade` long)"""
    depth = P.ARM_RAIL if depth is None else depth
    blade = P.ARM_BLADE if blade is None else blade
    plate = _plate()
    px, py, pz = P.pivot()
    band = (plate - Pos(0, 0, -depth) * plate) & _box(P.arm_x0() - 1, P.arm_x1() + 1, py + P.ARM_BOSS_R, P.ARM_TIP_Y + 1, -FAR, FAR)
    return band + (plate & _box(P.arm_x0() - 1, P.arm_x1() + 1, P.ARM_TIP_Y - blade, P.ARM_TIP_Y + 1, -FAR, FAR))


def arm():
    """black plate; it keeps FUSE_LAP under the rail so the two colours print as one body"""
    px, py, pz = P.pivot()
    plate = _plate()
    s = plate + _cyl_x(P.ARM_BOSS_R, P.arm_x0(), P.arm_x1(), py, pz)
    s -= _rail(P.ARM_RAIL - P.FUSE_LAP, P.ARM_BLADE - P.FUSE_LAP)
    # layered arm: two black side plates under the red top, open underneath between the boss and the knee
    s -= (Pos(0, 0, -P.ARM_RAIL - P.WALL) * plate) & _box(P.arm_x0() + P.WALL, P.arm_x1() - P.WALL, py + P.ARM_BOSS_R + ARM_CH_GAP,
                                                         P.CH_FRONT - ARM_CH_BACK, -FAR, FAR)
    return s - _cyl_x(P.PIVOT_D / 2 + P.FIT / 2, P.arm_x0() - 1, P.arm_x1() + 1, py, pz)  # pivot screw


def pivot_cap():
    """red washer under the pivot screw head (photo: red cap on the arm boss)"""
    px, py, pz = P.pivot()
    x0 = P.arm_x1()
    return _cyl_x(P.CAP_R, x0, x0 + P.CAP_T, py, pz) - _cyl_x(P.PIVOT_D / 2 + P.FIT / 2, x0 - 1, x0 + P.CAP_T + 1, py, pz)


def arm_rail():
    """printed with the arm (second colour)"""
    return _rail()


def horn():
    """white servo horn on the output spline, standing up in the gap between the housing and the arm"""
    ox, oy, oz = P.servo_out()
    x0, x1 = ox + P.HORN_GAP, ox + P.ARM_GAP - P.HORN_GAP
    hw, tw = P.HORN_W / 2, P.HORN_W * HORN_TAPER
    lever = _side([(oy - hw, oz), (oy + hw, oz), (oy + tw, oz + P.HORN_L), (oy - tw, oz + P.HORN_L)], x0, x1)
    tip = _cyl_x(tw, x0, x1, oy, oz + P.HORN_L)
    return _cyl_x(P.HORN_HUB_R, x0, x1, oy, oz) + lever + tip - _cyl_x(HORN_PIN_R, x0 - 1, x1 + 1, oy, oz + P.HORN_L)


# ---------------------------------------------------------------- side panels (+x built, -x mirrored)
def side_plan():
    xi, xo = P.pod_inner_x(), P.SP_OUT
    my = P.mid_half_y()
    xc = P.CH_W / 2 - P.TAB
    fy = P.pod_front_y() + P.POD_NOSE
    return [(xi, P.SP_REAR), (xo - POD_REAR_CHAMFER, P.SP_REAR), (xo, P.SP_REAR + POD_REAR_RUN), (xo, fy),
            (xi + P.FORK_W_ROOT * FORK_ROOT_F, fy + FORK_KNEE), (xi + P.FORK_W_TIP, P.FORK_TIP_Y), (xi, P.FORK_TIP_Y),
            (xi - INNER_STEP, P.pod_front_y() + INNER_RUN), (xi - INNER_STEP, P.pod_front_y()), (xi, P.pod_front_y() - 1),
            (xi, my), (xc, my), (xc, -my), (xi, -my)]


def side_profile():
    g = P.ground_z() + SOLE
    t, lo = P.SP_TOP, P.SP_LOW
    tip = P.FORK_TIP_Y
    return [(P.SP_REAR - 1, g), (tip + 1, g), (tip + 1, g + P.FORK_TIP_H), (tip - SAW_BACK, g + SAW_HI), (tip - SAW_BACK, g + SAW_LO),
            (P.pod_front_y() + P.POD_NOSE, t), (P.AXLE_Y - POD_TOP_RUN, t), (P.AXLE_Y - POD_TOP_DROP, lo), (P.SP_REAR + REAR_TAIL, lo),
            (P.SP_REAR - 1, g + REAR_TAIL)]


def _fork_out_x(y):
    """outer plan edge of the fork at y (straight taper from the knee to the tip)"""
    y0 = P.pod_front_y() + P.POD_NOSE + FORK_KNEE
    x0 = P.pod_inner_x() + P.FORK_W_ROOT * FORK_ROOT_F
    x1 = P.pod_inner_x() + P.FORK_W_TIP
    return x0 + (y - y0) * (x1 - x0) / (P.FORK_TIP_Y - y0)


def side_panel():
    prof = _side(side_profile(), 0, P.SP_OUT + 2)
    s = _plan(side_plan(), P.ground_z(), P.SP_TOP + 1) & prof
    # round the pods along the outer top edge (photo)
    try:
        s = fillet([e for e in s.edges() if e.center().X > P.SP_OUT - EPS * 10 and e.center().Z > P.SP_LOW - EPS * 10], P.POD_ROUND)
    except Exception:
        pass
    # hollow the pods (open underneath, printed top down)
    xi, xo = P.pod_inner_x(), P.SP_OUT
    sk = P.POD_SKIN
    fy = P.pod_front_y() + P.POD_NOSE
    s -= _box(xi + sk, xo - sk, P.SP_REAR + REAR_HOLLOW_IN, P.AXLE_Y - POD_TOP_DROP - sk, P.ground_z(), P.SP_LOW - sk)
    s -= _box(xi + sk, xo - sk, P.AXLE_Y - FRONT_HOLLOW_BACK, fy - sk, P.ground_z(), P.SP_TOP - sk)
    # fork hollow from underneath (skin POD_SKIN on top and sides), stops before the saw-tooth step
    y1 = P.FORK_TIP_Y - FORK_HOLLOW_END
    yk = fy + FORK_KNEE
    hp = _plan([(xi + sk, fy - sk), (xo - sk, fy - sk), (xo - sk, fy), (_fork_out_x(yk) - sk, yk), (_fork_out_x(y1) - sk, y1), (xi + sk, y1)],
               P.ground_z() - 1, P.SP_TOP)
    s -= hp & (Pos(0, 0, -sk) * prof)
    # web between the wheels only from the axle up; its tongue keys into the chassis flank slot
    my = P.mid_half_y()
    s -= _box(P.CH_W / 2 - P.TAB - 1, xi + sk, -my - 1, my + 1, P.ground_z() - 1, P.WEB_Z0)
    # the tongue stops short of the wheel wells and under the lid
    ky = my - P.KEY_TRIM
    for sy in (1, -1):
        s -= _box(P.CH_W / 2 - P.TAB - 1, P.CH_W / 2 + P.FIT, sy * ky, sy * (my + 1), P.WEB_Z0 - 1, P.SP_TOP + 1)
    s -= _box(P.CH_W / 2 - P.TAB - 1, P.CH_W / 2 + P.FIT, -my, my, P.lid_z0() - P.FIT, P.SP_TOP + 1)
    # web: a top plate over the gap between the wheels, screwed down onto the chassis flank blocks
    s -= _box(P.CH_W / 2 + P.FIT, xi + sk, -my + sk, my - sk, P.WEB_Z0 - 1, P.SP_LOW - P.WEB_PLATE)
    # vent grooves on the outer face of each pod (photo: III on the rear pod, IIIII on the front pod)
    for y0, y1, top, n in ((P.SP_REAR + REAR_HOLLOW_IN, -my - VENT_REAR_END, P.SP_LOW, REAR_VENTS),
                           (P.AXLE_Y - VENT_FRONT_START, fy - VENT_FRONT_END, P.SP_TOP, FRONT_VENTS)):
        pitch = (y1 - y0) / n
        for i in range(n):
            yc = y0 + pitch * (i + 0.5)
            s -= _box(xo - P.VENT_D, xo + 1, yc - P.VENT_W / 2, yc + P.VENT_W / 2, P.ground_z() + VENT_LOW, top - VENT_TOP)
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
    h = _cyl_x(P.HUB_R, x0, x1, y, 0) - _cyl_x(HUB_BORE_R, x0 - 1, x0 + P.SHAFT_BITE + HUB_BITE_EXTRA, y, 0)
    return _mx(h, sx)


def _module(fn):
    def f():
        s = fn()
        return mirror(s, Plane.YZ) if P.MODULE_SIDE < 0 else s
    return f


PARTS = {"chassis": chassis, "lid": lid, "housing": _module(housing), "cover": _module(cover), "pivot_cap": _module(pivot_cap),
         "arm": _module(arm), "arm_rail": _module(arm_rail), "horn": _module(horn), "side_l": side_panel, "side_r": side_panel_r}


def build(part, sx=1, sy=1):
    if part == "tyre":
        return tyre(sx, sy)
    if part == "hub":
        return hub(sx, sy)
    return PARTS[part]()
