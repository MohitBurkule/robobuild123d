"""Expandabot Classic CAD part builders (build123d).

Each part is built in its own local frame and placed in spec.json by at/rot.
"""
import math

import build123d as bd

from robot import catalog
from robot.cad import bay as bay_lib

from .params import *  # noqa: F401,F403

_CAT_CACHE = {}


def catalog_solid(cid):
    if cid not in _CAT_CACHE:
        _CAT_CACHE[cid] = hw._solid(cid)
    return _CAT_CACHE[cid]


def mirror_x(shape):
    return shape.mirror(bd.Plane.YZ)


def x_cyl(r, h):
    return bd.Cylinder(r, h, rotation=(0, 90, 0))


def screw_hole(t):
    return bd.Cylinder(SCREW_CLEAR_D / 2, t + 2 * EPS)


def _fillet_edges(solid, r, pred):
    edges = pred(solid)
    return bd.fillet(edges, radius=r) if edges else solid


# --------------------------------------------------------------------------------------------------------- poses
def motor_pose(left):
    s = 1 if left else -1
    yaw = 0.0 if left else 180.0
    return bd.Pos(s * (MOTOR_ROOT_X - MOTOR_SHAFT["at"][0]), WHEEL_Y, AXLE_Z) * bd.Rot(0, 0, yaw)


def servo_pose():
    # Servo lying on its side (+Z output along +Y/forward, body tucked under top_panel)
    return bd.Pos(SERVO_X, SERVO_Y, SERVO_Z) * bd.Rot(90, 0, 0)


def switch_pose():
    return bd.Pos(SWITCH_X, SWITCH_Y, SWITCH_Z) * bd.Rot(0, 0, 90)


# ---------------------------------------------------------------------------------------------------------- tub
def tub():
    """Black 3D-printed chassis tub with front bulkhead, rear wheel cutouts, closed-top N10 motor pockets,
    internal bays, lid pads, side-plate insert bosses, and front corner wing hinge clevises."""
    outer = bd.Pos(0, (BODY_Y0 + BODY_Y1) / 2, TUB_Z0 + TUB_H / 2) * bd.Box(TUB_W, BODY_L, TUB_H)
    # Hollow interior leaving floor WALL, side walls WALL, rear wall WALL, front bulkhead 2*WALL
    in_w = TUB_W - 2 * WALL
    in_y0 = BODY_Y0 + WALL
    in_y1 = BODY_Y1 - 2 * WALL
    cavity = bd.Pos(0, (in_y0 + in_y1) / 2, TUB_Z0 + WALL + TUB_H / 2) * bd.Box(in_w, in_y1 - in_y0, TUB_H)
    cavity = _fillet_edges(cavity, CHAMFER_R, lambda b: b.edges().filter_by(bd.Axis.Z))
    body = outer - cavity

    # Cut open rear wheel wells on +X and -X
    for s in (-1, 1):
        wx0 = s * (WHEEL_X - WHEEL_W / 2 - RUN_CLEAR - RUN_CLEAR / 2)
        wx1 = s * (TUB_W / 2 + CHAMFER_R + RUN_CLEAR)
        well = bd.Pos((wx0 + wx1) / 2, WHEEL_Y, TUB_Z0 + TUB_H / 2) * \
            bd.Box(abs(wx1 - wx0), WHEEL_D + 2 * RUN_CLEAR + RUN_CLEAR / 2, TUB_H + 2 * EPS)
        well = _fillet_edges(well, CHAMFER_R, lambda b: b.edges().filter_by(bd.Axis.Z))
        body = body - well

    # Closed-top N10 motor pockets on +X and -X
    for left in (True, False):
        s = 1 if left else -1
        # Carve motor pocket (U-channel open on +Z for top-down drop-in, covered by top_panel)
        bx0 = s * MOTOR_INNER_X
        bx1 = s * (WHEEL_X - WHEEL_W / 2 - RUN_CLEAR)
        m_blk_h = AXLE_Z - TUB_Z0 + MOTOR_ENV_Z
        m_blk = bd.Pos((bx0 + bx1) / 2, WHEEL_Y, TUB_Z0 + m_blk_h / 2) * \
            bd.Box(abs(bx1 - bx0), 2 * (MOTOR_ENV_Y + WALL), m_blk_h)
        body = body + m_blk
        mx0 = s * (MOTOR_INNER_X - MOTOR_FIT)
        mx1 = s * (MOTOR_ROOT_X - MOTOR_FIT)
        m_cav = bd.Pos((mx0 + mx1) / 2, WHEEL_Y, AXLE_Z + MOTOR_ENV_Z / 2) * \
            bd.Box(abs(mx1 - mx0), 2 * (MOTOR_ENV_Y + MOTOR_FIT), 3 * MOTOR_ENV_Z)
        body = body - m_cav
        wire_slot = bd.Pos(s * (MOTOR_INNER_X - WALL / 2), WHEEL_Y, TUB_Z0 + WALL + WIRE_SLOT_H / 2) * \
            bd.Box(WALL + TUB_Z0, WIRE_SLOT_W, WIRE_SLOT_H)
        body = body - wire_slot
        shaft_r = MOTOR_SHAFT["dia"] / 2 + RUN_CLEAR / 2
        shaft_bore = bd.Pos(s * (WHEEL_X - WHEEL_W / 2 - RUN_CLEAR), WHEEL_Y, AXLE_Z) * x_cyl(shaft_r, WIRE_SLOT_H)
        shaft_slot = bd.Pos(s * (WHEEL_X - WHEEL_W / 2 - RUN_CLEAR), WHEEL_Y, (AXLE_Z + TUB_Z1) / 2) * \
            bd.Box(WIRE_SLOT_H, 2 * shaft_r - CLEAR, TUB_Z1 - AXLE_Z + EPS)
        body = body - shaft_bore - shaft_slot

    # Internal bay divider wall on -X (separates ESC/battery from open front-right bay)
    div_y0 = TOP_BAY_Y0 - CLEVIS_Z_GAP
    div_r = bd.Pos(-TOP_TONGUE_HALF_X - WALL / 2, (div_y0 + BODY_Y1 - WALL) / 2, TUB_Z0 + TUB_H / 2) * \
        bd.Box(WALL, BODY_Y1 - WALL - div_y0, TUB_H)
    body = body + div_r

    # Lid screw pads with heat-set bores (front pads tapered underneath for support-free printing)
    for px, py in TOP_SCREWS_XY:
        if py > 0:
            pad_h = PAD_FRONT_H
            pad_zc = TUB_Z1 - pad_h / 2
            pad = bd.Pos(px, py, pad_zc) * bd.Cylinder(PAD_R, pad_h)
            taper = bd.Pos(px, py, TUB_Z1 - pad_h - PAD_R / 2) * bd.Cone(EPS, PAD_R, PAD_R)
            bridge = bd.Pos(px, (py + BODY_Y1 - WALL) / 2, pad_zc) * bd.Box(2 * PAD_R, abs(BODY_Y1 - WALL - py) + WALL, pad_h)
            pad = pad + taper + bridge
        else:
            pad = bd.Pos(px, py, TUB_Z0 + TUB_H / 2) * bd.Cylinder(PAD_R, TUB_H)
        bore = bd.Pos(px, py, TUB_Z1 - INSERT_HALF_L) * bd.Cylinder((INSERT_OD - CLEAR) / 2, INSERT_L + RUN_CLEAR)
        body = body + pad - bore

    # Side-plate insert bosses
    for s in (-1, 1):
        for sy in SIDE_SCREW_YS:
            boss = bd.Pos(s * (TUB_W / 2 - SIDE_BOSS_L / 2), sy, SIDE_SCREW_Z) * x_cyl(SIDE_BOSS_R, SIDE_BOSS_L)
            bore = bd.Pos(s * (TUB_W / 2 - INSERT_HALF_L), sy, SIDE_SCREW_Z) * x_cyl((INSERT_OD - CLEAR) / 2, INSERT_L + RUN_CLEAR)
            body = body + boss - bore

    # Switch tray under -X deck
    sw_tray = bd.Pos(SWITCH_X, SWITCH_Y, SWITCH_Z - SW_TRAY_DZ) * bd.Box(SW_TRAY_W, SW_TRAY_L, SW_TRAY_H)
    sw_cut = bd.Pos(SWITCH_X, SWITCH_Y, SWITCH_Z) * bd.Box(SW_CUT_W, SW_CUT_L, SW_CUT_H)
    body = body + sw_tray - sw_cut

    # Front corner wing hinge clevises (top & bottom ears bridged to tub front wall)
    for s in (-1, 1):
        px, py = s * WING_PIVOT_X, WING_PIVOT_Y
        for ez in (WING_PIVOT_Z - BRACKET_H / 2 - CLEVIS_Z_GAP, WING_PIVOT_Z + BRACKET_H / 2 + CLEVIS_Z_GAP):
            ear = bd.Pos(px, py, ez) * bd.Cylinder(CLEVIS_R, CLEVIS_T)
            bridge = bd.Pos((px + s * (TUB_W / 2 - RUN_CLEAR)) / 2, py - WALL, ez) * \
                bd.Box(abs(px - s * (TUB_W / 2 - RUN_CLEAR)) + WALL, CLEVIS_R, CLEVIS_T)
            body = body + ear + bridge
        pin_hole = bd.Pos(px, py, WING_PIVOT_Z) * bd.Cylinder(WING_PIN_D / 2 - CLEAR / 2, WING_PIN_LEN + WALL)
        body = body - pin_hole

    # Front skid pads for stable floor support polygon
    for s in (-1, 1):
        skid = bd.Pos(s * SKID_X, SKID_Y, TUB_Z0 - SKID_H / 2) * bd.Box(SKID_W, SKID_L, SKID_H)
        body = body + skid

    # Nose stud bore on front bulkhead
    body = body - bd.Pos(0, BODY_Y1 - WALL, NOSE_PIN_Z) * bd.Cylinder(NOSE_PIN_D / 2 - CLEAR / 4, PAD_FRONT_H, rotation=(90, 0, 0))
    return body


# ---------------------------------------------------------------------------------------------------- top_panel
def top_panel():
    """One-piece 1.5 mm CF T-shaped top plate with rear wheel cutouts, rear centre notch,
    open front corner bays, and elongated switch travel slot."""
    cx, cy = 0.0, (TOP_REAR_Y0 + TOP_FRONT_Y1) / 2
    pts = [
        (-TOP_X_MAX - cx, TOP_REAR_Y0 - cy),
        (-TOP_REAR_NOTCH_HALF_X - cx, TOP_REAR_Y0 - cy),
        (-TOP_REAR_NOTCH_HALF_X - cx, TOP_REAR_NOTCH_Y1 - cy),
        (TOP_REAR_NOTCH_HALF_X - cx, TOP_REAR_NOTCH_Y1 - cy),
        (TOP_REAR_NOTCH_HALF_X - cx, TOP_REAR_Y0 - cy),
        (TOP_X_MAX - cx, TOP_REAR_Y0 - cy),
        (TOP_X_MAX - cx, TOP_BAY_Y0 - cy),
        (TOP_TONGUE_HALF_X - cx, TOP_BAY_Y0 - cy),
        (TOP_TONGUE_HALF_X - cx, TOP_FRONT_Y1 - cy),
        (-TOP_TONGUE_HALF_X - cx, TOP_FRONT_Y1 - cy),
        (-TOP_TONGUE_HALF_X - cx, TOP_BAY_Y0 - cy),
        (-TOP_X_MAX - cx, TOP_BAY_Y0 - cy),
    ]
    plate = bd.Pos(0, 0, -TOP_T / 2) * bd.extrude(bd.Polygon(*pts, align=None), amount=TOP_T)

    # Rear wheel cutouts
    w_cx = (TOP_WHEEL_SLOT_X0 + TOP_WHEEL_SLOT_X1) / 2
    w_cy = (TOP_WHEEL_SLOT_Y0 + TOP_WHEEL_SLOT_Y1) / 2
    w_sx = TOP_WHEEL_SLOT_X1 - TOP_WHEEL_SLOT_X0
    w_sy = TOP_WHEEL_SLOT_Y1 - TOP_WHEEL_SLOT_Y0
    for s in (-1, 1):
        plate = plate - bd.Pos(s * w_cx - cx, w_cy - cy, 0) * bd.Box(w_sx, w_sy, TOP_T + 2 * EPS)

    # Elongated switch travel slot on -X
    top_bb = (catalog_solid(SWITCH_ID).moved(switch_pose()) &
              bd.Pos(0, 0, TOP_Z1) * bd.Box(120, 120, 2 * TOP_T)).bounding_box()
    kx = (top_bb.min.X + top_bb.max.X) / 2
    y_min = top_bb.min.Y - SW_LEVER_TRAVEL - 0.5
    y_max = top_bb.max.Y + 0.5
    ky = (y_min + y_max) / 2
    kw = (top_bb.max.X - top_bb.min.X) + 2 * CLEAR
    kl = y_max - y_min
    plate = plate - bd.Pos(kx - cx, ky - cy, 0) * bd.Box(kw, kl, TOP_T + 2 * EPS)

    # Fillet all vertical corners >= laser kerf
    plate = _fillet_edges(plate, SLOT_R, lambda p: [e for e in p.edges() if abs(e.center().Z) < SHELL_TOL])

    for px, py in TOP_SCREWS_XY:
        plate = plate - bd.Pos(px - cx, py - cy, 0) * screw_hole(TOP_T)
    return plate


def top_panel_at():
    return (0.0, (TOP_REAR_Y0 + TOP_FRONT_Y1) / 2, TUB_Z1 + TOP_T / 2)


# --------------------------------------------------------------------------------------------------- side_plates
def _side_base():
    y0, y1, z0, z1 = SIDE_Y0, SIDE_Y1, SIDE_Z0, SIDE_Z1
    yc, zc = (y0 + y1) / 2, (z0 + z1) / 2
    plate = bd.Pos(0, 0, 0) * bd.Box(SHEET_T, y1 - y0, z1 - z0)
    plate = _fillet_edges(plate, SIDE_R, lambda p: [e for e in p.edges() if abs(e.center().X) < SHELL_TOL and e.center().Y < 0])
    for sy in SIDE_SCREW_YS:
        plate = plate - bd.Pos(0, sy - yc, SIDE_SCREW_Z - zc) * x_cyl(SCREW_CLEAR_D / 2, SHEET_T + 2 * EPS)
    return plate


def side_left():
    return _side_base()


def side_right():
    return mirror_x(_side_base())


def side_at(side):
    return (side * SIDE_X, (SIDE_Y0 + SIDE_Y1) / 2, (SIDE_Z0 + SIDE_Z1) / 2)


# -------------------------------------------------------------------------------------------------------- wedge
def wedge():
    """Black 3D-printed forked front wedge with central window."""
    slope_dy = WEDGE_Y1 - WEDGE_Y0
    slope_dz = WEDGE_Z1 - WEDGE_Z0
    L = math.hypot(slope_dy, slope_dz)
    pts = [
        (-WEDGE_W0 / 2, 0.0),
        (WEDGE_W0 / 2, 0.0),
        (WEDGE_TIP_X_OUT, L),
        (WEDGE_TIP_X_IN, L),
        (0.0, WEDGE_V_Y - WEDGE_Y0),
        (-WEDGE_TIP_X_IN, L),
        (-WEDGE_TIP_X_OUT, L),
    ]
    plate = bd.Pos(0, 0, -WEDGE_T / 2) * bd.extrude(bd.Polygon(*pts, align=None), amount=WEDGE_T)
    win = bd.Pos(0, (WEDGE_WIN_Y0 + WEDGE_WIN_Y1) / 2 - WEDGE_Y0, 0) * \
        bd.Box(2 * WEDGE_WIN_X, WEDGE_WIN_Y1 - WEDGE_WIN_Y0, WEDGE_T + 2 * EPS)
    plate = plate - win
    plate = _fillet_edges(plate, 0.5, lambda p: [e for e in p.edges() if abs(e.center().Z) < SHELL_TOL and abs(e.center().X) < WEDGE_WIN_X + 0.5 and (WEDGE_WIN_Y0 - WEDGE_Y0 - 0.5) < e.center().Y < (WEDGE_WIN_Y1 - WEDGE_Y0 + 0.5)])
    cb_y = (CROSSBAR_Y - WEDGE_Y0) / math.cos(math.atan2(-slope_dz, slope_dy))
    for s in (-1, 1):
        plate = plate + bd.Pos(s * (WEDGE_WIN_X + WEDGE_BOSS_D / 2), cb_y, 0) * x_cyl(WEDGE_BOSS_D / 2, WEDGE_BOSS_D)
    plate = plate - bd.Pos(0, cb_y, 0) * x_cyl(CROSSBAR_D / 2 + 0.1, 2 * WEDGE_WIN_X + 4.0)
    return plate


def crossbar():
    """Brushed steel crossbar spanning the wedge window."""
    return x_cyl(CROSSBAR_D / 2, 2 * WEDGE_WIN_X + 2.0)


# ----------------------------------------------------------------------------------------------- wings & brackets
def bracket_left():
    """Dark-grey printed corner hinge bracket in hinge frame (pivot at (0,0,0), arm along +Y)."""
    arm = bd.Pos(0, BRACKET_L / 2, 0) * bd.Box(BRACKET_W, BRACKET_L, BRACKET_H)
    hub = bd.Cylinder(BRACKET_W / 2, BRACKET_H)
    blk = arm + hub
    blk = blk - bd.Cylinder(WING_PIN_D / 2 + 0.2, BRACKET_H + 2 * EPS)
    for dy in WING_SCREW_DYS:
        blk = blk - bd.Pos(0, dy, 0) * x_cyl((INSERT_OD - CLEAR) / 2, BRACKET_W + 2 * EPS)
    return blk


def bracket_right():
    return mirror_x(bracket_left())


def wing_left():
    """Pale-mint G10/PC expanding wing bolted to bracket_left (hinge frame)."""
    pts = [
        (WING_ROOT_Y, 0.0),
        (WING_LEN, 0.0),
        (WING_LEN - WING_TIP_CHAMFER, -WING_H),
        (WING_ROOT_Y, -WING_H),
    ]
    # Plane.YZ * Polygon extrudes in -X, so start at BRACKET_W / 2 + WING_GAP + WING_T
    blade = bd.Pos(BRACKET_W / 2 + WING_GAP + WING_T, 0, WING_H / 2) * \
        bd.extrude(bd.Plane.YZ * bd.Polygon(*pts, align=None), amount=WING_T)
    for dy in WING_SCREW_DYS:
        blade = blade - bd.Pos(BRACKET_W / 2 + WING_GAP + WING_T / 2, dy, 0) * x_cyl(SCREW_CLEAR_D / 2, WING_T + 2 * EPS)
    return blade


def wing_right():
    return mirror_x(wing_left())


def hinge_pin():
    return bd.Cylinder(WING_PIN_D / 2, WING_PIN_LEN)


def horn():
    """White printed servo horn extending forward into open front-left bay."""
    hub = bd.Cylinder(3.5, HORN_T)
    arm = bd.Pos(0, HORN_LEN / 2, 0) * bd.Box(HORN_W, HORN_LEN, HORN_T)
    return hub + arm


def nose_pin():
    """White front bulkhead nose stud."""
    return bd.Cylinder(NOSE_PIN_D / 2, NOSE_PIN_L, rotation=(90, 0, 0))


# ------------------------------------------------------------------------------------------------------- wheels
def _wheel_base():
    """Grooved grey TPU rear wheel with 12 radial tread notches and N10 D-bore."""
    w = bd.Cylinder(WHEEL_D / 2, WHEEL_W, rotation=(0, 90, 0))
    for i in range(WHEEL_NOTCHES):
        a = 2 * math.pi * i / WHEEL_NOTCHES
        ny = (WHEEL_D / 2) * math.cos(a)
        nz = (WHEEL_D / 2) * math.sin(a)
        notch = bd.Pos(0, ny, nz) * bd.Rot(math.degrees(a), 0, 0) * bd.Box(WHEEL_W + 2 * EPS, 2 * WHEEL_NOTCH_D, WHEEL_NOTCH_W)
        w = w - notch
    bore = x_cyl(MOTOR_SHAFT["dia"] / 2 + 0.25, WHEEL_W + 2 * EPS)
    return w - bore


def wheel_left():
    return _wheel_base()


def wheel_right():
    return mirror_x(_wheel_base())


def mass_g(made):
    cat_ids = [DRIVE_MOTOR_ID] * 2 + [SERVO_ID, BATTERY_ID, ESC_ID, SWITCH_ID]
    m = sum(catalog.find(c).mass_g for c in cat_ids)
    rho = {"print": catalog.density(PRINT_MAT), "sheet": catalog.density(SHEET_MAT),
           "cf": catalog.density(TOP_MAT) or 1.55, "tyre": catalog.density("tpu"), "steel": 7.85}
    for _name, (solid, kind) in made.items():
        m += solid.volume / 1000.0 * rho[kind]
    return m
