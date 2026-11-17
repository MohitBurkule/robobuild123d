"""GNC manufactured parts, one function per part, each in its own local frame (the spec places it with at/rot).

  tub          world frame: both drive pods, the centre bridge (servo cradle + rear cross member), nose fork seats
  lid_l/lid_r  plate centre
  fork_l/_r    fork frame (origin at the tine root on its top face, tine along +Y, top face z = 0)
  arm          pivot frame (origin on the servo output axis at x = 0, arm along +Y, rotated to rest by the spec)
  wheel_*      axle frame (axis along X)
"""
import math

import build123d as bd

from robot import catalog

from .params import *  # noqa: F401,F403
from .params import hw


# ------------------------------------------------------------------------------------------------------- helpers
def x_cyl(r, length):
    return bd.Rot(0, 90, 0) * bd.Cylinder(r, length)


def box_between(x0, x1, y0, y1, z0, z1):
    """Axis-aligned box from two corners."""
    return bd.Pos((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2) * bd.Box(abs(x1 - x0), abs(y1 - y0), abs(z1 - z0))


def yz_prism(points, x0, x1):
    """Polygon drawn in the YZ plane (as (y, z) pairs) extruded from x0 to x1."""
    face = bd.Plane.YZ * bd.Polygon(*points, align=None)
    return bd.Pos(x0, 0, 0) * bd.extrude(face, amount=x1 - x0)


def mirror_x(part):
    return bd.mirror(part, bd.Plane.YZ)


def fork_frame():
    """World Location of the fork frame for the left (+X) tine."""
    return bd.Pos(FORK_X, FORK_ROOT_Y, FORK_ROOT_Z) * bd.Rot(-FORK_DEG, 0, 0)


def motor_pose(side, y):
    return bd.Pos(side * MOTOR_ROOT_X, y, AXLE_Z) * bd.Rot(0, 0, 90 * (1 - side)) * bd.Pos(-MOTOR_SHAFT["at"][0], 0, 0)


def servo_pose():
    return bd.Pos(SERVO_X, SERVO_Y, SERVO_Z) * bd.Rot(0, 0, 90) * bd.Rot(90, 0, 0)


# --------------------------------------------------------------------------------------------------------- tub
def _inner_slope_z(y):
    """Underside of the sloped nose skin at y."""
    return TUB_Z1 - NOSE_WALL_DY - (y - NOSE_Y0) * NOSE_DROP / NOSE_RUN


def _pod_left():
    """Left (+X) pod shell: side profile extruded across the pod, hollowed with an open top under the lid."""
    outer = yz_prism([(POD_Y0, BELLY_Z), (POD_Y1, BELLY_Z), (POD_Y1, NOSE_Z), (NOSE_Y0, TUB_Z1), (POD_Y0, TUB_Z1)],
                     POD_XI, POD_XO)
    ys = FORK_ROOT_Y - WALL                  # solid nose block ahead of here (fork seat)
    cav = yz_prism([(POD_Y0 + WALL, FLOOR_Z), (ys, FLOOR_Z), (ys, _inner_slope_z(ys)),
                    (NOSE_Y0, _inner_slope_z(NOSE_Y0)), (NOSE_Y0, TUB_Z1 + EPS), (POD_Y0 + WALL, TUB_Z1 + EPS)],
                   POD_IN_XI, POD_IN_XO)
    return outer - cav


def _housing(side, y):
    """Motor housing block with a closed top, open outboard face and a lead slot in the inner end wall."""
    s = side
    block = box_between(s * HOUSE_X0, s * POD_IN_XO, y - HOUSE_HALF_Y, y + HOUSE_HALF_Y, FLOOR_Z - EPS, TUB_Z1)
    pocket = box_between(s * (MOTOR_INNER_X - MOTOR_FIT), s * (POD_XO + EPS), y - POCKET_HALF_Y, y + POCKET_HALF_Y,
                         AXLE_Z - POCKET_HALF_Z, AXLE_Z + POCKET_HALF_Z)
    slot = box_between(s * (HOUSE_X0 - EPS), s * MOTOR_INNER_X, y - TERM_SLOT_W / 2, y + TERM_SLOT_W / 2,
                       AXLE_Z - TERM_SLOT_H / 2, AXLE_Z + TERM_SLOT_H / 2)
    return block, pocket + slot


def _lid_pads(side):
    pads, bores = [], []
    for y in LID_SCREWS_Y:
        pads.append(box_between(side * (LID_PAD_X - LID_PAD_D / 2), side * POD_IN_XO + side * EPS,
                                y - LID_PAD_D / 2, y + LID_PAD_D / 2, TUB_Z1 - LID_PAD_H, TUB_Z1))
        bores.append(bd.Pos(side * LID_PAD_X, y, TUB_Z1 - INSERT_L / 2 - EPS / 2) *
                     bd.Cylinder(INSERT_OD / 2 - CLEAR / 2, INSERT_L + EPS))
    return pads, bores


def _fork_seat_cuts(side):
    """Channel in the nose for the tine (walls locate it) and the two blind heat-set bores under it."""
    f = fork_frame()
    if side < 0:
        f = bd.Pos(-2 * FORK_X, 0, 0) * f
    chan = f * bd.Pos(0, FORK_LEN / 2, NOSE_DROP) * bd.Box(FORK_W + 2 * CLEAR, FORK_LEN, 2 * NOSE_DROP)
    bores = [f * bd.Pos(0, s, -FORK_BORE_DEPTH / 2 + EPS) * bd.Cylinder(INSERT_OD / 2 - CLEAR / 2, FORK_BORE_DEPTH)
             for s in FORK_BOLT_S]
    return chan, bores


def _bridge():
    """Floor plate between the pods, the hollow rear cross member and the servo cradle end walls."""
    floor = box_between(-POD_XI - EPS, POD_XI + EPS, BRIDGE_Y0, BRIDGE_Y1, BELLY_Z, FLOOR_Z)
    xbar = box_between(-POD_XI - EPS, POD_XI + EPS, POD_Y0, XBAR_Y1, BELLY_Z, XBAR_Z1)
    chan = box_between(-POD_IN_XO + WALL, POD_IN_XO - WALL, POD_Y0 + WALL + 1.0, POD_Y0 + WALL + 1.0 + CHAN_W,
                       CHAN_Z0, CHAN_Z0 + CHAN_H)
    yb0 = SERVO_Y - SERVO_BODY_L / 2 - CLEAR
    yb1 = SERVO_Y + SERVO_BODY_L / 2 + CLEAR
    walls = (box_between(-POD_XI - EPS, CRADLE_X1, yb0 - CRADLE_WALL, yb0, FLOOR_Z - EPS, CRADLE_Z1) +
             box_between(-POD_XI - EPS, CRADLE_X1, yb1, yb1 + CRADLE_WALL, FLOOR_Z - EPS, CRADLE_Z1))
    # lead slot for the servo cable through the right pod inner wall, beside the cradle
    lead = box_between(-POD_IN_XI - EPS, -POD_XI + EPS, SERVO_Y - SERVO_BODY_L / 2 - CHAN_W, SERVO_Y - SERVO_BODY_L / 2,
                       SERVO_Z - CHAN_H / 2, SERVO_Z + CHAN_H / 2)
    return floor + xbar + walls, chan, lead


def _switch_tray():
    z_bot = SW_Z + SW_BB.min.Z
    return box_between(SW_X - SW_W / 2 - CLEAR, SW_X + SW_W / 2 + CLEAR, SW_Y - SW_L / 2, SW_Y + SW_L / 2,
                       FLOOR_Z - EPS, z_bot)


def _bay_walls(x, y, l_y, w_x):
    """Low locating rim round a flat pack lying on the pod floor (a pack l_y long in Y, w_x wide in X)."""
    o = box_between(x - w_x / 2 - BAY_FIT - WALL, x + w_x / 2 + BAY_FIT + WALL, y - l_y / 2 - BAY_FIT - WALL,
                    y + l_y / 2 + BAY_FIT + WALL, FLOOR_Z - EPS, FLOOR_Z + BAY_WALL_H)
    i = box_between(x - w_x / 2 - BAY_FIT, x + w_x / 2 + BAY_FIT, y - l_y / 2 - BAY_FIT, y + l_y / 2 + BAY_FIT,
                    FLOOR_Z - EPS, FLOOR_Z + BAY_WALL_H + EPS)
    return o, i


def tub():
    left = _pod_left()
    body = left + mirror_x(left)
    adds, cuts = [], []
    for s in (1, -1):
        for y in (WHEEL_YR, WHEEL_YF):
            b, c = _housing(s, y)
            adds.append(b)
            cuts.append(c)
        pads, bores = _lid_pads(s)
        adds += pads
        cuts += bores
        chan, fbores = _fork_seat_cuts(s)
        cuts += [chan] + fbores
    bridge, chan, lead = _bridge()
    adds.append(bridge)
    adds.append(_switch_tray())
    bo, bi = _bay_walls(BAT_X, BAT_Y, BAT_L, BAT_W)
    eo, ei = _bay_walls(ESC_X, ESC_Y, ESC_L, ESC_W)
    eo = eo - box_between(-POD_IN_XI, -POD_XO, ESC_Y - ESC_L, ESC_Y + ESC_L, FLOOR_Z, TUB_Z1) * 0 if False else eo
    adds += [bo, eo]
    cuts += [bi, ei, chan, lead]
    for a in adds:
        body = body + a
    for c in cuts:
        body = body - c
    return body


# --------------------------------------------------------------------------------------------------------- lids
def lid_left():
    plate = bd.Box(POD_W, LID_Y1 - LID_Y0, LID_T)
    cx, cy = POD_XC, (LID_Y0 + LID_Y1) / 2
    for y in LID_SCREWS_Y:
        plate = plate - bd.Pos(LID_PAD_X - cx, y - cy, 0) * bd.Cylinder(SCREW_CLEAR_D / 2, LID_T + 2 * EPS)
    return plate


def lid_right():
    plate = mirror_x(lid_left())
    cx, cy = -POD_XC, (LID_Y0 + LID_Y1) / 2
    slot = bd.Pos(SW_X - cx, SW_Y - cy, 0) * bd.Box(SW_W + 2 * CLEAR, SW_L + 2 * CLEAR, LID_T + 2 * EPS)
    return plate - slot


def lid_at(side):
    return (side * POD_XC, (LID_Y0 + LID_Y1) / 2, TUB_Z1 + LID_T / 2)


# --------------------------------------------------------------------------------------------------------- forks
def fork():
    """FR4 tine in its fork frame: strip along +Y with an arrowhead tip, top face z = 0, two bolt holes."""
    shaft_l = FORK_LEN - FORK_TIP_L
    h, H = FORK_W / 2, FORK_TIP_W / 2
    pts = [(-h, 0), (h, 0), (h, shaft_l), (H, shaft_l), (0, FORK_LEN), (-H, shaft_l), (-h, shaft_l)]
    plate = bd.extrude(bd.Polygon(*pts, align=None), amount=-FORK_T)
    for s in FORK_BOLT_S:
        plate = plate - bd.Pos(0, s, -FORK_T / 2) * bd.Cylinder(SCREW_CLEAR_D / 2, FORK_T + 2 * EPS)
    return plate


# ----------------------------------------------------------------------------------------------------------- arm
def _ring_face():
    """Hook ring profile in the local YZ plane (y along the arm), centred at (ARM_L, 0)."""
    ring = bd.Circle(HEAD_RO) - bd.Circle(HEAD_RI)
    a0, a1 = (math.radians(a) for a in HEAD_GAP_DEG)
    big = 3 * HEAD_RO
    wedge = bd.Polygon((0, 0), (big * math.cos(a0), big * math.sin(a0)), (big * math.cos((a0 + a1) / 2) * 1.5,
                       big * math.sin((a0 + a1) / 2) * 1.5), (big * math.cos(a1), big * math.sin(a1)), align=None)
    face = ring - wedge
    # pointed tail running on from the ring end at a0, tangent to the ring
    rm = (HEAD_RO + HEAD_RI) / 2
    t = (math.sin(a0), -math.cos(a0))                 # tangent pointing away from the ring (clockwise)
    p_o = (HEAD_RO * math.cos(a0), HEAD_RO * math.sin(a0))
    p_i = (HEAD_RI * math.cos(a0), HEAD_RI * math.sin(a0))
    tip = (rm * math.cos(a0) + TAIL_L * t[0], rm * math.sin(a0) + TAIL_L * t[1])
    tail = bd.Polygon(p_o, tip, p_i, align=None)
    return face + tail


def arm():
    """Arm + rake head in the pivot frame (rest pose applied by the spec rotation)."""
    prof = bd.Plane.YZ * bd.Pos(ARM_L, 0) * _ring_face()
    head = bd.extrude(prof, amount=HEAD_W / 2, both=True)
    # slots between the tines leave a spine on the arm side of the ring
    pitch = (HEAD_W - TINE_T) / (TINES - 1)
    slot_w = pitch - TINE_T
    y0 = ARM_L - HEAD_RI + SPINE_DEPTH
    big = 4 * HEAD_RO
    for i in range(TINES - 1):
        xc = SPINE_X0 + TINE_T + slot_w / 2 + i * pitch
        head = head - box_between(xc - slot_w / 2, xc + slot_w / 2, y0, ARM_L + big, -big, big)
    bar = box_between(HUB_X0, HUB_X1, 0, ARM_L - HEAD_RI + (HEAD_RO - HEAD_RI) / 2, -ARM_W / 2, ARM_W / 2)
    hub = bd.Pos(ARM_X, 0, 0) * x_cyl(HUB_R_ARM, ARM_T)
    spline = bd.Pos(ARM_X, 0, 0) * x_cyl(HUB_R_ARM / 2, ARM_T + 2 * EPS)
    return head + bar + hub - spline


# ------------------------------------------------------------------------------------------------------- wheels
def wheel():
    """Left wheel in the axle frame: knurled tread ring + web + hub with the N10 D-bore."""
    ro, ri = WHEEL_D / 2, WHEEL_D / 2 - TYRE_T
    tyre = x_cyl(ro, WHEEL_W) - x_cyl(ri, WHEEL_W + 2 * EPS)
    for i in range(KNURL_N):
        a = 360.0 * i / KNURL_N
        tyre = tyre - bd.Rot(a, 0, 0) * bd.Pos(0, 0, ro) * bd.Box(WHEEL_W + 2 * EPS, KNURL_W, 2 * KNURL_D)
    web = x_cyl(ri + EPS, WEB_T)
    for i in range(3):
        a = 360.0 * i / 3 + 30.0
        web = web - bd.Rot(a, 0, 0) * bd.Pos(0, 0, (ri + HUB_R) / 2) * x_cyl((ri - HUB_R) * 0.36, WEB_T + 2 * EPS)
    hub = x_cyl(HUB_R, WHEEL_W)
    bore_r = MOTOR_SHAFT["dia"] / 2 + CLEAR / 3
    bore = x_cyl(bore_r, WHEEL_W + 2 * EPS) & \
        bd.Pos(0, 0, BORE_FLAT_Z - BORE_BOX_Z_OFF) * bd.Box(WHEEL_W + 2 * EPS, BORE_FLAT_W, BORE_BOX_H)
    return tyre + web + hub - bore


def wheel_right():
    return mirror_x(wheel())
