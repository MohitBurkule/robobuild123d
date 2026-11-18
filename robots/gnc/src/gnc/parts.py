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
    """Left (+X) pod shell: side profile extruded across the pod, hollowed with an open top under the lid, plus front plow bumper."""
    outer = yz_prism([(POD_Y0, BELLY_Z), (POD_Y1, BELLY_Z), (PLOW_Y1, PLOW_TIP_Z0), (PLOW_Y1, PLOW_TIP_Z1),
                      (PLOW_STEP_Y, PLOW_STEP_Z), (POD_Y1, PLOW_STEP_Z), (POD_Y1, NOSE_Z), (NOSE_Y0, TUB_Z1), (POD_Y0, TUB_Z1)],
                     POD_XI, POD_XO)
    ys = CAV_FRONT_Y                         # solid nose block ahead of here (fork seat)
    y_roof = NOSE_Y0 - WALL                  # keep >= 2.0 mm solid top rim behind the nose slope corner
    cav = yz_prism([(POD_Y0 + WALL, FLOOR_Z), (ys, FLOOR_Z), (ys, _inner_slope_z(ys)),
                    (y_roof, _inner_slope_z(NOSE_Y0)), (y_roof, TUB_Z1 + EPS), (POD_Y0 + WALL, TUB_Z1 + EPS)],
                   POD_IN_XI, POD_IN_XO)
    return outer - cav


def _housing(side, y):
    """Motor housing block with a closed top, open outboard face, open wire tunnel below Z = 6.95 on the inner side, and a lead slot."""
    s = side
    x_step = HOUSE_X0 + HOUSE_UNDER_W
    block_main = box_between(s * x_step, s * POD_IN_XO, y - HOUSE_HALF_Y, y + HOUSE_HALF_Y, FLOOR_Z - EPS, TUB_Z1)
    block_inner = box_between(s * HOUSE_X0, s * (x_step + EPS), y - HOUSE_HALF_Y, y + HOUSE_HALF_Y,
                              AXLE_Z - POCKET_HALF_Z, TUB_Z1)
    pocket = box_between(s * (MOTOR_INNER_X - MOTOR_FIT), s * (POD_XO + EPS), y - POCKET_HALF_Y, y + POCKET_HALF_Y,
                         AXLE_Z - POCKET_HALF_Z, AXLE_Z + POCKET_HALF_Z)
    slot = box_between(s * (HOUSE_X0 - EPS), s * (MOTOR_INNER_X + WALL), y - TERM_SLOT_W / 2, y + TERM_SLOT_W / 2,
                       AXLE_Z - POCKET_HALF_Z - EPS, AXLE_Z + TERM_SLOT_H / 2)
    return block_main + block_inner, pocket + slot


def _lid_pads(side):
    pads, bores = [], []
    bore_d = INSERT_L + LID_BORE_EXTRA
    for y in LID_SCREWS_Y:
        pads.append(box_between(side * (POD_IN_XI - EPS), side * (LID_PAD_X + LID_PAD_D / 2),
                                y - LID_PAD_D / 2, y + LID_PAD_D / 2, TUB_Z1 - LID_PAD_H, TUB_Z1))
        bores.append(bd.Pos(side * LID_PAD_X, y, TUB_Z1 - bore_d / 2 + EPS / 2) *
                     bd.Cylinder(INSERT_OD / 2 - CLEAR / 2, bore_d + EPS))
    return pads, bores


def _fork_seat_cuts(side):
    """Enclosed slot in the outer-lower corner of the nose plow for the tine, blind heat-set bores, driver counterbores, and two plow face recesses."""
    f = fork_frame()
    if side < 0:
        f = bd.Pos(-2 * FORK_X, 0, 0) * f
    # slot for the tine + deep counterbores straight above the two M2 button heads so a hex driver and heat-set insert have full access
    chan = f * bd.Pos(0, FORK_LEN / 2, FORK_CHAN_Z_OFF) * bd.Box(FORK_W + 2 * CLEAR, FORK_LEN + FORK_CHAN_EXTRA_L, FORK_CHAN_H)
    head_pockets = [f * bd.Pos(0, s, FORK_CBORE_Z) * bd.Cylinder(FORK_CBORE_R, FORK_CBORE_H) for s in FORK_BOLT_S]
    bores = [f * bd.Pos(0, s, -FORK_T - FORK_BORE_DEPTH / 2 + EPS) * bd.Cylinder(INSERT_OD / 2 - CLEAR / 2, FORK_BORE_DEPTH)
             for s in FORK_BOLT_S]
    # two rectangular bolt-access pockets on the sloped front plow face (visible in ref.png)
    pockets = [
        box_between(side * (POD_XC + dx - PLOW_POCKET_HW), side * (POD_XC + dx + PLOW_POCKET_HW),
                    PLOW_POCKET_Y0, PLOW_POCKET_Y1, PLOW_POCKET_Z0, PLOW_POCKET_Z1)
        for dx in PLOW_POCKET_DX
    ]
    return chan, head_pockets + bores + pockets


def _bridge():
    """Floor plate between the pods, the hollow rear cross member and the servo cradle end walls."""
    floor = box_between(-POD_XI - EPS, POD_XI + EPS, BRIDGE_Y0, BRIDGE_Y1, BELLY_Z, FLOOR_Z)
    xbar = box_between(-POD_XI - EPS, POD_XI + EPS, POD_Y0, XBAR_Y1, BELLY_Z, XBAR_Z1)
    chan = box_between(-POD_IN_XO + WALL, POD_IN_XO - WALL, POD_Y0 + WALL + CHAN_Y_INSET, POD_Y0 + WALL + CHAN_Y_INSET + CHAN_W,
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
    return box_between(SW_X - SW_W / 2, SW_X + SW_W / 2, SW_Y - SW_TRAY_HALF_Y, SW_Y + SW_TRAY_HALF_Y,
                       FLOOR_Z - EPS, z_bot)


def _bay_walls(x, y, l_y, w_x):
    """Low locating rim round a flat pack lying on the pod floor (open at the rear -Y end for the XT30 wire lead)."""
    o = box_between(POD_IN_XI - EPS, x + w_x / 2 + BAY_FIT + WALL, y - l_y / 2 + BAT_RIM_REAR_TRIM,
                    y + l_y / 2 + BAY_FIT + WALL, FLOOR_Z - EPS, FLOOR_Z + BAY_WALL_H)
    i = box_between(POD_IN_XI, x + w_x / 2 + BAY_FIT, y - l_y / 2 + BAT_RIM_REAR_TRIM - EPS,
                    y + l_y / 2 + BAY_FIT, FLOOR_Z - EPS, FLOOR_Z + BAY_WALL_H + EPS)
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
    adds += [bo]
    cuts += [bi, chan, lead]
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
    slot_2d = bd.Pos(SW_X - cx, SW_Y - cy) * bd.RectangleRounded(SW_W + 2 * CLEAR, SW_L + 2 * CLEAR, LID_SLOT_R)
    slot = bd.extrude(slot_2d, amount=LID_T / 2 + EPS, both=True)
    return plate - slot


def lid_at(side):
    return (side * POD_XC, (LID_Y0 + LID_Y1) / 2, TUB_Z1 + LID_T / 2)


# --------------------------------------------------------------------------------------------------------- forks
def fork():
    """Tine in its fork frame: narrow strip along +Y with an upturned beveled front wedge tip, top face z = 0, two bolt holes."""
    shaft_l = FORK_LEN - FORK_TIP_L
    h = FORK_W / 2
    plate = box_between(-h, h, 0, FORK_LEN, -FORK_T, 0)
    # upturned triangular wedge fin on the front tip (matching the angled tip wedge in ref.png)
    tip_wedge = yz_prism([(shaft_l, 0), (FORK_LEN, 0), (shaft_l + FORK_TIP_PEAK_DY, FORK_TIP_PEAK_Z)], -h, h)
    plate = plate + tip_wedge
    for s in FORK_BOLT_S:
        plate = plate - bd.Pos(0, s, -FORK_T / 2) * bd.Cylinder(SCREW_CLEAR_D / 2, FORK_T + 2 * EPS)
    return plate


# ----------------------------------------------------------------------------------------------------------- arm
def _ring_face():
    """Hook ring profile in the local YZ plane (y along the arm), centred at (0, 0) relative to (ARM_L, HEAD_DZ)."""
    ring = bd.Circle(HEAD_RO) - bd.Circle(HEAD_RI)
    a0, a1 = (math.radians(a) for a in HEAD_GAP_DEG)
    big = 3 * HEAD_RO
    mid = (a0 + a1) / 2
    wedge = bd.Polygon(
        (0, 0),
        (big * math.cos(a0), big * math.sin(a0)),
        (big * math.cos(mid), big * math.sin(mid)),
        (big * math.cos(a1), big * math.sin(a1)),
        align=None,
    )
    face = ring - wedge
    # smooth S-curved lower-rear tail + crossbar hub base at the bottom-rear of the ring
    a_t0, a_t1 = math.radians(TAIL_ANG0), math.radians(TAIL_ANG1)
    tail = bd.Polygon(
        (HEAD_RO * math.cos(a_t0), HEAD_RO * math.sin(a_t0)),
        *TAIL_PTS,
        (HEAD_RI * math.cos(a_t1), HEAD_RI * math.sin(a_t1)),
        (HEAD_RI * math.cos(a_t0), HEAD_RI * math.sin(a_t0)),
        align=None,
    )
    return face + tail


def arm():
    """Arm + rake head in the pivot frame (rest pose applied by the spec rotation)."""
    prof = bd.Plane.YZ * bd.Pos(ARM_L, HEAD_DZ) * _ring_face()
    head = bd.extrude(prof, amount=HEAD_W / 2, both=True)
    # slots between the 5 tines: cut everything EXCEPT the horizontal crossbar where the straight arm bar meets the tine bases
    pitch = (HEAD_W - TINE_T) / (TINES - 1)
    slot_w = pitch - TINE_T
    big = 4 * HEAD_RO
    spine_y0 = ARM_L + SPINE_DY0
    spine_y1 = ARM_L + SPINE_DY1
    spine_z0 = HEAD_DZ + SPINE_DZ0
    spine_z1 = HEAD_DZ + SPINE_DZ1
    for i in range(TINES - 1):
        xc = SPINE_X0 + TINE_T + slot_w / 2 + i * pitch
        slot_all = box_between(xc - slot_w / 2, xc + slot_w / 2, ARM_L - big, ARM_L + big, -big, big)
        spine_keep = box_between(xc - slot_w / 2 - EPS, xc + slot_w / 2 + EPS, spine_y0, spine_y1, spine_z0, spine_z1)
        head = head - (slot_all - spine_keep)
    # central arm bar from pivot hub straight along +Y up to the spine crossbar (spanning X in [HUB_X0, ARM_BAR_X1])
    bar_y1 = spine_y1
    arm_prof = bd.Plane.YZ * bd.Polygon(
        (0, -ARM_ROOT_W / 2),
        (0, ARM_ROOT_W / 2),
        (bar_y1, spine_z1),
        (bar_y1, spine_z0),
        align=None,
    )
    bar_w = ARM_BAR_X1 - HUB_X0
    bar = bd.Pos((HUB_X0 + ARM_BAR_X1) / 2, 0, 0) * bd.extrude(arm_prof, amount=bar_w / 2, both=True)
    hub = bd.Pos(ARM_X, 0, 0) * x_cyl(HUB_R_ARM, ARM_T)
    spline = bd.Pos(ARM_X, 0, 0) * x_cyl(HUB_R_ARM / 2, ARM_T + 2 * EPS)
    return (head + bar + hub) - spline


# ------------------------------------------------------------------------------------------------------- wheels
def wheel():
    """Left wheel in the axle frame: knurled tread ring + 3-spoke web + hub with the N10 D-bore."""
    ro, ri = WHEEL_D / 2, WHEEL_D / 2 - TYRE_T
    tyre = x_cyl(ro, WHEEL_W) - x_cyl(ri, WHEEL_W + 2 * EPS)
    for i in range(KNURL_N):
        a = 360.0 * i / KNURL_N
        tyre = tyre - bd.Rot(a, 0, 0) * bd.Pos(0, 0, ro) * bd.Box(WHEEL_W + 2 * EPS, KNURL_W, 2 * KNURL_D)
    web = x_cyl(ri + EPS, WEB_T)
    # 3 sector/triangular window cutouts in the wheel face matching ref.png
    w_in = HUB_R + WHEEL_WIN_IN_PAD
    w_out = ri - WHEEL_WIN_OUT_PAD
    ai, ao = math.radians(WHEEL_WIN_ANG_IN), math.radians(WHEEL_WIN_ANG_OUT)
    window_2d = bd.Polygon(
        (w_in * math.cos(-ai), w_in * math.sin(-ai)),
        (w_out * math.cos(-ao), w_out * math.sin(-ao)),
        (w_out, 0),
        (w_out * math.cos(ao), w_out * math.sin(ao)),
        (w_in * math.cos(ai), w_in * math.sin(ai)),
        align=None,
    )
    win_solid = bd.extrude(bd.Plane.YZ * window_2d, amount=WEB_T + 2 * EPS, both=True)
    for i in range(WHEEL_SPOKES):
        web = web - bd.Rot(360.0 * i / WHEEL_SPOKES + WHEEL_SPOKE_PHASE, 0, 0) * win_solid
    hub = x_cyl(HUB_R, WHEEL_W)
    bore_r = MOTOR_SHAFT["dia"] / 2 + CLEAR / 3
    bore = x_cyl(bore_r, WHEEL_W + 2 * EPS) & \
        bd.Pos(0, 0, BORE_FLAT_Z - BORE_BOX_Z_OFF) * bd.Box(WHEEL_W + 2 * EPS, BORE_FLAT_W, BORE_BOX_H)
    return tyre + web + hub - bore


def wheel_right():
    return mirror_x(wheel())
