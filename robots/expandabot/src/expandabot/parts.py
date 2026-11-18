"""Expandabot manufactured parts, one function per fabricated part.

Each part is built in its OWN local frame (the spec places it with at/rot):
  tub                     world frame (origin on the centre line, mid overall length)
  lid                     plate centre
  side_l / side_r         plate centre
  clamp_l / clamp_r       clamp frame (origin at (±CLAMP_X, HINGE_Y, HINGE_Z), arm along +Y, top face z = 0)
  flipper, hinge_block    hinge frame (origin at (0, HINGE_Y, HINGE_Z), plate along +Y, top face z = 0)
  horn, drive_pin         servo output frame (origin on the output axis, arm along +Y)
  wheel_l / wheel_r       axle frame (origin at the wheel centre, axis along X)
  hinge_pin               on the hinge axis, along X
"""
import math

import build123d as bd

from robot import catalog
from robot.cad import bay as bay_lib

from .params import *  # noqa: F401,F403
from .params import hw

EPS = bay_lib.CUT_OVERSHOOT


# ------------------------------------------------------------------------------------------------------- helpers
def screw_hole(length, d=SCREW_CLEAR_D):
    """Through hole along Z, centred on the origin."""
    return bd.Cylinder(d / 2, length + 2 * EPS)


def y_cyl(r, length):
    """Cylinder with its axis on Y, centred on the origin."""
    return bd.Rot(90, 0, 0) * bd.Cylinder(r, length)


def x_cyl(r, length):
    """Cylinder with its axis on X, centred on the origin."""
    return bd.Rot(0, 90, 0) * bd.Cylinder(r, length)


def catalog_solid(cid):
    """A catalogue part's own solid (cached conversion per id)."""
    return hw._solid(cid)


def mirror_x(part):
    """Right-hand (-X) mirror copy of a left-hand (+X) part across the YZ plane."""
    return bd.mirror(part, bd.Plane.YZ)


def _fillet_edges(part, r, cand):
    """Fillet the edges selected by `cand(part)` at radius r, falling back to per-edge filtering if needed."""
    edges = cand(part)
    if not edges:
        return part
    try:
        return part.fillet(r, edges)
    except Exception:  # noqa: BLE001
        pass

    def key(e):
        c = e.center()
        return (round(c.X, 2), round(c.Y, 2), round(c.Z, 2))

    good = set()
    for e in edges:
        try:
            part.fillet(r, [e])
            good.add(key(e))
        except Exception:  # noqa: BLE001
            pass
    if good:
        try:
            return part.fillet(r, [e for e in cand(part) if key(e) in good])
        except Exception:  # noqa: BLE001
            pass
    return part


def _fillet_near(part, r, plane_xs, yz_centers, tol=PAD_MOUTH_R, plane_ys=()):
    """Fillet sharp rim edges whose centre sits on `plane_xs` and within `r + tol` of `yz_centers`."""
    def cand(p):
        return [e for e in p.edges()
                if (not plane_xs or any(abs(e.center().X - px) < RIM_TOL for px in plane_xs))
                and (not plane_ys or any(abs(e.center().Y - py) < RIM_TOL for py in plane_ys))
                and any(math.hypot(e.center().Y - cy, e.center().Z - cz) < r + tol for cy, cz in yz_centers)]
    return _fillet_edges(part, r, cand)


# --------------------------------------------------------------------------------------------------------- tub
def _bays():
    """Battery (centre channel, rear) and ESC (left side zone) bays from robot/cad/bay.py, drop-in from the top."""
    bat = bay_lib.derive_bay(catalog.find(BATTERY_ID), wall=WALL, insert_dir="-z",
                             placement=bd.Pos(0, BAT_Y, TUB_Z0 + WALL + BAT_H / 2) * bd.Rot(0, 0, 90))
    esc = bay_lib.derive_bay(catalog.find(ESC_ID), wall=WALL, insert_dir="-z",
                             placement=bd.Pos(SIDE_ZONE_X, ESC_Y, TUB_Z0 + WALL + ESC_H / 2) * bd.Rot(0, 0, 90))
    return bat, esc


def switch_z():
    """Switch centre height: knob pokes SWITCH_POKE_Z through the right lid slot."""
    bb = catalog_solid(SWITCH_ID).bounding_box()
    return LID_Z1 + SWITCH_POKE_Z - bb.max.Z


def switch_pose():
    """Switch in the right side zone (-X), knob through the right lid slot."""
    return bd.Pos(-SIDE_ZONE_X, SW_Y, switch_z()) * bd.Rot(0, 0, 90)


def _switch_tray():
    """Printed pillar from the floor up to the switch bottom, rotated so long side runs along Y."""
    sw_l, sw_w, _ = hw.size(SWITCH_ID)
    bb = catalog_solid(SWITCH_ID).bounding_box()
    z_bot = switch_z() + bb.min.Z
    return bd.Pos(-SIDE_ZONE_X, SW_Y, (TUB_Z0 + WALL + z_bot) / 2) * \
        bd.Box(sw_w + 2 * CLEAR, sw_l + 2 * CLEAR, z_bot - TUB_Z0 - WALL)


def motor_pose(left):
    """Catalogue gearmotor frame (+X = shaft) -> robot: shaft points outboard along +-X at the rear axle."""
    s = 1 if left else -1
    root = bd.Pos(s * MOTOR_ROOT_X, WHEEL_Y, AXLE_Z) * bd.Rot(0, 0, 90 * (1 - s))
    return root * bd.Pos(-MOTOR_SHAFT["at"][0], 0, 0)


def servo_pose():
    """Servo on its side in the centre channel: catalogue +Z (output axis) -> robot +X, catalogue +X -> robot +Y."""
    return bd.Pos(0, SERVO_Y, SERVO_OUT_Z) * bd.Rot(0, 0, 90) * bd.Rot(90, 0, 0)


def _clamp_mount(side):
    """Sloped front mounting block on the tub for the left (+1) or right (-1) horizontal clamping arm.
    Sits flat on the print bed at Z = TUB_Z0, merges into the front wall at Y = BODY_Y1, and is planed
    at z = -SHEET_T in the clamp frame with three blind M2 heat-set bores perpendicular to the slope."""
    s = side
    w = CLAMP_SEAT_OUTER_X - CLAMP_INNER_X
    y1 = HINGE_Y + CLAMP_MOUNT_Y1
    raw = bd.Pos(s * CLAMP_X, (CLAMP_SEAT_Y0 + y1) / 2, TUB_Z0 + TUB_H / 2) * \
        bd.Box(w, y1 - CLAMP_SEAT_Y0, TUB_H)
    cframe = bd.Pos(s * CLAMP_X, HINGE_Y, HINGE_Z) * bd.Rot(-CLAMP_REST_DEG, 0, 0)
    cutter = cframe * bd.Pos(0, 0, CLAMP_CUT_H / 2 - SHEET_T) * bd.Box(CLAMP_CUT_W, CLAMP_CUT_W, CLAMP_CUT_H)
    mount = raw - cutter
    for dx, by in CLAMP_BOLTS_XY:
        bore = cframe * bd.Pos(dx, by, -SHEET_T - CLAMP_BORE_DEPTH / 2 + EPS) * \
            bd.Cylinder(SEAT_HOLE_D / 2, CLAMP_BORE_DEPTH + 2 * EPS)
        mount = mount - bore
    return mount


def tub():
    outer = bd.Pos(0, TUB_YC, TUB_Z0 + TUB_H / 2) * bd.Box(TUB_W, TUB_L, TUB_H)
    inner = bd.Pos(0, TUB_YC, TUB_Z0 + WALL + TUB_H / 2) * bd.Box(TUB_W - 2 * WALL, TUB_L - 2 * WALL, TUB_H)
    body = outer - inner

    # servo tray: open-top U-channel in the front of the centre channel, horn slot on +X wall, lead slot on -Y wall
    tray_cy = SERVO_Y + SERVO_Y_OFF
    tray = bd.Pos(0, tray_cy, (TUB_Z0 + WALL + TRAY_TOP_Z) / 2) * \
        bd.Box(2 * TRAY_HALF_X, SERVO_LEN + 2 * TRAY_WALL, TRAY_TOP_Z - TUB_Z0 - WALL)
    cav = bd.Pos(0, tray_cy, (TUB_Z0 + WALL - EPS + TRAY_TOP_Z + EPS) / 2) * \
        bd.Box(2 * (SERVO_FACE_X + SERVO_CAV_FIT), SERVO_LEN + 2 * SERVO_CAV_FIT, TRAY_TOP_Z + EPS - (TUB_Z0 + WALL - EPS))
    slot = bd.Pos(TRAY_HALF_X - TRAY_WALL / 2, (HORN_SLOT_Y0 + HORN_SLOT_Y1) / 2,
                  (HORN_SLOT_Z0 + TRAY_TOP_Z + EPS) / 2) * \
        bd.Box(TRAY_WALL + 2 * HORN_SLOT_MARGIN, HORN_SLOT_Y1 - HORN_SLOT_Y0, TRAY_TOP_Z + EPS - HORN_SLOT_Z0)
    lead = bd.Pos(0, tray_cy - SERVO_LEN / 2 - TRAY_WALL / 2 + EPS, (LEAD_SLOT_Z0 + LEAD_SLOT_Z1) / 2) * \
        bd.Box(2 * LEAD_SLOT_HALF_X, TRAY_WALL + 2 * EPS, LEAD_SLOT_Z1 - LEAD_SLOT_Z0)
    body = body + (tray - cav - slot - lead)

    # switch tray in the right (-X) side zone
    body = body + _switch_tray()

    # two rear motor housing blocks (added before lid pads so rear lid pad bores stay open)
    mx0 = MOTOR_INNER_X + WALL
    mx1 = TUB_W / 2
    my0 = WHEEL_Y - MOTOR_ENV_Y - WALL
    my1 = WHEEL_Y + MOTOR_ENV_Y + WALL
    for s in (-1, 1):
        m_wall = bd.Pos(s * (mx0 + mx1) / 2, (my0 + my1) / 2, TUB_Z0 + TUB_H / 2) * \
            bd.Box(mx1 - mx0, my1 - my0, TUB_H)
        body = body + m_wall

    # lid pads on left (+X) and right (-X) walls with blind M2 heat-set bores
    bz0 = TUB_Z1 - LID_PAD_H + LID_PAD_BORE_FLOOR
    for s in (1, -1):
        for y, pw in LID_PADS:
            pad = bd.Pos(s * LID_PAD_X, y, TUB_Z1 - LID_PAD_H / 2) * bd.Box(LID_PAD_D, pw, LID_PAD_H)
            bore = bd.Pos(s * LID_PAD_X, y, (bz0 + TUB_Z1 + EPS) / 2) * \
                bd.Cylinder(INSERT_OD / 2 - CLEAR / 2, TUB_Z1 + EPS - bz0)
            body = body + pad - bore

    # standoff columns to the left and right side guard plates (overlapping the wall by WALL so union is manifold)
    for s in (-1, 1):
        for y in STANDOFF_YS:
            for z in PLATE_SCREWS_Z:
                col = bd.Pos(s * (TUB_W / 2 + (SPACER_L - WALL) / 2), y, z) * x_cyl(STANDOFF_D / 2, SPACER_L + WALL)
                bore = bd.Pos(s * (TUB_W / 2 + SPACER_L / 2), y, z) * x_cyl(INSERT_OD / 2 - CLEAR / 2, SPACER_L + 2 * EPS)
                body = body + col - bore

    # sloped front clamp mounts (left +1, right -1)
    for s in (-1, 1):
        body = body + _clamp_mount(s)

    # outer hinge knuckles on the front top edge for the central flipper pin
    for s in (-1, 1):
        k = bd.Pos(s * TUB_KNUCKLE_X, HINGE_Y, HINGE_Z) * x_cyl(HINGE_BOSS_D / 2, TUB_KNUCKLE_W - 2 * CLEAR)
        bore = bd.Pos(s * TUB_KNUCKLE_X, HINGE_Y, HINGE_Z) * x_cyl(PIN_TUB_BORE_R, TUB_KNUCKLE_W + 2 * EPS)
        body = body + k - bore
    notch = bd.Pos(0, (RELIEF_Y0 + RELIEF_Y1) / 2, (RELIEF_Z0 + TUB_Z1 + EPS) / 2) * \
        bd.Box(2 * RELIEF_HALF_X, RELIEF_Y1 - RELIEF_Y0, TUB_Z1 + EPS - RELIEF_Z0)
    body = body - notch

    # two rear motor pocket cuts (closed top, open outboard wall for axial motor insertion, shaft hole into wheel well)
    for s in (-1, 1):
        pocket = bd.Pos(s * (MOTOR_INNER_X - MOTOR_FIT + TUB_W / 2 + POCKET_OUT) / 2, WHEEL_Y, AXLE_Z) * \
            bd.Box(TUB_W / 2 + POCKET_OUT - MOTOR_INNER_X + MOTOR_FIT,
                   2 * (MOTOR_ENV_Y + MOTOR_FIT),
                   2 * (MOTOR_ENV_Z + MOTOR_FIT))
        shaft_hole = bd.Pos(s * (MOTOR_ROOT_X - SHAFT_HOLE_IN + (SHAFT_HOLE_IN + SHAFT_HOLE_OUT) / 2), WHEEL_Y, AXLE_Z) * \
            x_cyl(MOTOR_SHAFT["dia"] / 2 + SHAFT_HOLE_FIT, SHAFT_HOLE_IN + SHAFT_HOLE_OUT)
        body = body - pocket - shaft_hole

    # electronics bays (battery and ESC cut solids)
    for b in _bays():
        body = body - b.cut_solid()

    return body


# --------------------------------------------------------------------------------------------------------- lid
def lid():
    """One-piece 1.5 mm PC top lid in its own centred frame, with symmetric front U-notch for hinge_block,
    narrow slot for the servo horn + drive_pin passage, and elongated slot for full switch lever travel."""
    x0, x1 = -TUB_W / 2, TUB_W / 2
    cx, cy = (x0 + x1) / 2, (BODY_Y0 + LID_Y1) / 2
    pts = [
        (x0 - cx, BODY_Y0 - cy),
        (x1 - cx, BODY_Y0 - cy),
        (x1 - cx, LID_Y1 - cy),
        (LID_SLOT_HALF_X - cx, LID_Y1 - cy),
        (LID_SLOT_HALF_X - cx, LID_SLOT_Y0 - cy),
        (-LID_SLOT_HALF_X - cx, LID_SLOT_Y0 - cy),
        (-LID_SLOT_HALF_X - cx, LID_Y1 - cy),
        (x0 - cx, LID_Y1 - cy),
    ]
    plate = bd.Pos(0, 0, -LID_T / 2) * bd.extrude(bd.Polygon(*pts, align=None), amount=LID_T)
    notch_corners = [
        (-LID_SLOT_HALF_X - cx, LID_SLOT_Y0 - cy),
        (LID_SLOT_HALF_X - cx, LID_SLOT_Y0 - cy),
    ]

    def _notch_edges(p):
        return [e for e in p.edges()
                if abs(e.center().Z) < SHELL_TOL
                and any(abs(e.center().X - nx) < SHELL_TOL and abs(e.center().Y - ny) < SHELL_TOL
                        for nx, ny in notch_corners)]
    plate = _fillet_edges(plate, LID_SLOT_R, _notch_edges)
    # Horn slot + narrow drive_pin passage (so lid lifts clear along +Z without trapping drive_pin)
    hx0 = HORN_X - (HORN_HALF_X + HORN_LID_MARGIN)
    hx1 = LID_HORN_NOTCH_X1
    hcx, hcy = (hx0 + hx1) / 2 - cx, (HORN_LID_Y0 + HORN_LID_Y1) / 2 - cy
    hw_x, hl_y = hx1 - hx0, HORN_LID_Y1 - HORN_LID_Y0
    plate = plate - bd.Pos(hcx, hcy, 0) * bd.Box(hw_x, hl_y, LID_T + 2 * EPS)
    pin_slot_w = hx0 - LID_SLOT_HALF_X + 0.4
    pin_slot_y = HINGE_PIN_D + 2 * 0.45
    plate = plate - bd.Pos((LID_SLOT_HALF_X + hx0) / 2 - cx, PIN_Y - cy, 0) * bd.Box(pin_slot_w, pin_slot_y, LID_T + 2 * EPS)

    def _hslot_edges(p):
        return [e for e in p.edges()
                if abs(e.center().Z) < SHELL_TOL
                and LID_SLOT_HALF_X - 0.5 < e.center().X + cx < hx1 + 0.5
                and HORN_LID_Y0 - 0.5 < e.center().Y + cy < HORN_LID_Y1 + 0.5]
    plate = _fillet_edges(plate, LID_SLOT_R, _hslot_edges)
    for s, ys in ((1, LID_SCREWS_Y_L), (-1, LID_SCREWS_Y_R)):
        for y in ys:
            plate = plate - bd.Pos(s * LID_PAD_X - cx, y - cy, 0) * screw_hole(LID_T)
    top_bb = (catalog_solid(SWITCH_ID).moved(switch_pose()) &
              bd.Pos(0, 0, LID_Z1) * bd.Box(OVERALL_W, OVERALL_L, 2 * LID_T)).bounding_box()
    kx = (top_bb.min.X + top_bb.max.X) / 2
    y_min = top_bb.min.Y - SW_LEVER_TRAVEL - LID_SW_TRAVEL_MARGIN
    y_max = top_bb.max.Y + LID_SW_TRAVEL_MARGIN
    ky = (y_min + y_max) / 2
    kw = (top_bb.max.X - top_bb.min.X) + 2 * CLEAR
    kl = y_max - y_min
    slot = bd.Pos(kx - cx, ky - cy, 0) * bd.Box(kw, kl, LID_T + 2 * EPS)
    plate = plate - slot
    scx, scy = kx - cx, ky - cy

    def _slot_edges(p):
        return [e for e in p.edges()
                if abs(e.center().Z) < SHELL_TOL
                and abs(e.center().X - scx) < kw / 2 + LID_SLOT_MARGIN
                and abs(e.center().Y - scy) < kl / 2 + LID_SLOT_MARGIN]
    return _fillet_edges(plate, LID_SLOT_R, _slot_edges)


def lid_at():
    return (0.0, (BODY_Y0 + LID_Y1) / 2, TUB_Z1 + LID_T / 2)


# --------------------------------------------------------------------------------------------------- side plates
def _side_base():
    """Left (+X) hexagonal 2 mm PC side guard plate in its own centred frame."""
    c = PLATE_CHAMFER
    y0, y1, z0, z1 = BODY_Y0, BODY_Y1, PLATE_Z0, PLATE_Z0 + PLATE_H
    pts = [(y0 + c, z0), (y1 - c, z0), (y1, z0 + c), (y1, z1 - c),
           (y1 - c, z1), (y0 + c, z1), (y0, z1 - c), (y0, z0 + c)]
    plate = bd.extrude(bd.Plane.YZ * bd.Polygon(*pts, align=None), amount=SHEET_T)
    for y in STANDOFF_YS:
        for z in PLATE_SCREWS_Z:
            plate = plate - bd.Pos(SHEET_T / 2, y, z) * x_cyl(PLATE_HOLE_D / 2, SHEET_T + 2 * EPS)
    bb = plate.bounding_box()
    return plate.moved(bd.Pos(-(bb.min.X + bb.max.X) / 2, -(bb.min.Y + bb.max.Y) / 2, -(bb.min.Z + bb.max.Z) / 2))


def side_plate_left():
    return _side_base()


def side_plate_right():
    return mirror_x(_side_base())


def side_at(side):
    return (side * SIDE_X, (BODY_Y0 + BODY_Y1) / 2, PLATE_Z0 + PLATE_H / 2)


# --------------------------------------------------------------------------------------------- clamping arms
def clamp_left():
    """Left (+X) lobster-claw clamping arm in its local clamp frame (origin at (+CLAMP_X, HINGE_Y, HINGE_Z),
    arm extending along +Y, top face at z = 0, bottom face at z = -SHEET_T)."""
    x_in = CLAMP_INNER_X - CLAMP_X
    x_out0 = CLAMP_OUTER_X - CLAMP_X
    x_out1 = CLAMP_TIP_OUTER_X - CLAMP_X
    y0 = HINGE_BOSS_D / 2
    y1 = CLAMP_LEN
    c = FLIP_CHAMFER
    pts = [
        (x_in, y0),
        (x_out0, y0),
        (x_out0, CLAMP_MOUNT_Y1),
        (x_out1, y1 - c),
        (x_out1 - c, y1),
        (x_in, y1),
    ]
    plate = bd.extrude(bd.Polygon(*pts, align=None), amount=-SHEET_T)
    for dx, by in CLAMP_BOLTS_XY:
        plate = plate - bd.Pos(dx, by, -SHEET_T / 2) * screw_hole(SHEET_T)
    return plate


def clamp_right():
    """Right (-X) lobster-claw clamping arm: exact mirror of the left arm across YZ."""
    return mirror_x(clamp_left())


# ------------------------------------------------------------------------------------------------------ flipper
def flipper():
    """Central flipper plate in the hinge frame: hinge axis = X through origin, plate along +Y, top face z = 0."""
    c = FLIP_CHAMFER
    h, L = FLIP_W / 2, FLIP_LEN
    pts = [(-h, HINGE_BOSS_D / 2), (h, HINGE_BOSS_D / 2), (h, L - c),
           (h - c, L), (-h + c, L), (-h, L - c)]
    plate = bd.extrude(bd.Polygon(*pts, align=None), amount=-SHEET_T)
    for x in (-HINGE_BOLT_X, HINGE_BOLT_X):
        plate = plate - bd.Pos(x, BOLT_HB_Y, -SHEET_T / 2) * screw_hole(SHEET_T)
    return plate


def hinge_block():
    """Printed centre knuckle + flipper seat + tail lever, in the hinge frame (child of the flipper)."""
    knuckle_w = BLOCK_KNUCKLE_W - 2 * CLEAR
    knuckle = x_cyl(HINGE_BOSS_D / 2, knuckle_w)

    def _rims(p):
        return [e for e in p.edges()
                if abs(abs(e.center().X) - knuckle_w / 2) < RIM_TOL
                and math.hypot(e.center().Y, e.center().Z) > HINGE_BOSS_D / 2 - BORE_GUARD]
    knuckle = _fillet_edges(knuckle, KNUCKLE_RIM_FILLET_R, _rims)
    seat = bd.Pos(0, SEAT_Y0 + SEAT_L / 2, -SHEET_T - SEAT_H / 2) * bd.Box(SEAT_W, SEAT_L, SEAT_H)
    for x in (-HINGE_BOLT_X, HINGE_BOLT_X):
        seat = seat - bd.Pos(x, BOLT_HB_Y, -SHEET_T - SEAT_H / 2) * bd.Cylinder(SEAT_HOLE_D / 2, SEAT_H + 2 * EPS)
    web = bd.Pos(0, (SEAT_WEB_Y0 + SEAT_WEB_Y1) / 2, -SHEET_T - SEAT_WEB_H / 2) * \
        bd.Box(knuckle_w, SEAT_WEB_Y1 - SEAT_WEB_Y0, SEAT_WEB_H)
    block = knuckle + web + seat
    tail = bd.Pos(0, -TAIL_L / 2, 0) * bd.Box(TAIL_W, TAIL_L, TAIL_H)
    skirt_l = TAIL_L - TAIL_SKIRT_INSET
    skirt = bd.Pos(0, -skirt_l / 2, -TAIL_DROP / 2) * bd.Box(TAIL_W, skirt_l, TAIL_H + TAIL_DROP)
    block = block + tail + skirt
    block = block - x_cyl(KNUCKLE_BORE_R, BLOCK_KNUCKLE_W + 2 * EPS)

    def _seams(p):
        return [e for e in p.edges()
                if abs(e.center().X) < RIM_TOL
                and SEAT_WEB_Y0 - RIM_TOL <= e.center().Y <= HINGE_BOSS_D / 2
                and -SHEET_T - SEAM_DZ < e.center().Z < -SHEET_T + SEAM_DZ_TOP]
    block = _fillet_edges(block, SEAT_WEB_FILLET_R, _seams)
    return block


def horn():
    """Servo horn in the servo output frame: hub on X axis, arm along +Y out to the pin tab."""
    hub = x_cyl(HORN_HUB_R, 2 * HORN_HALF_X)
    arm = bd.Pos(0, HORN_R / 2 - HORN_ARM_OFF, 0) * bd.Box(2 * HORN_HALF_X, HORN_R + HORN_ARM_EXTRA, HORN_ARM_W)
    tab = bd.Pos(0, HORN_R, 0) * bd.Box(2 * HORN_HALF_X, HORN_TAB[0], HORN_TAB[1])
    bore = bd.Pos(0, HORN_R, 0) * x_cyl(HORN_PIN_BORE_R, 2 * HORN_HALF_X + 2 * EPS)
    return hub + arm + tab - bore


def drive_pin():
    """M2 drive pin through the horn tab bore, inner end in the tail's angular shadow (horn frame)."""
    return bd.Pos((PIN_X0 + PIN_X1) / 2, HORN_R, 0) * x_cyl(HINGE_PIN_D / 2, PIN_X1 - PIN_X0)


def hinge_pin():
    """M2 hinge pin through all knuckles, along X centred on the hinge axis."""
    return x_cyl(HINGE_PIN_D / 2, HINGE_PIN_LEN)


# ------------------------------------------------------------------------------------------------------- wheels
def _wheel_base():
    """Left (+X) wheel in the axle frame (axis along X): printed hub + TPU tyre with D-bore matching N10 shaft."""
    bore = x_cyl(BORE_R, WHEEL_W + 2 * EPS) & \
        bd.Pos(0, 0, BORE_FLAT_Z - BORE_BOX_Z_OFF) * bd.Box(WHEEL_W + 2 * EPS, BORE_FLAT_W, BORE_BOX_H)
    return x_cyl(WHEEL_D / 2, WHEEL_W) - bore


def wheel_left():
    return _wheel_base()


def wheel_right():
    return mirror_x(_wheel_base())


# --------------------------------------------------------------------------------------------------------- mass
def mass_g(made):
    """Catalogue masses + printed / sheet part volumes (densities from robot.catalog.MATERIALS)."""
    cat_ids = [DRIVE_MOTOR_ID] * 2 + [SERVO_ID, BATTERY_ID, ESC_ID, SWITCH_ID]
    m = sum(catalog.find(c).mass_g for c in cat_ids)
    rho = {"print": catalog.density(PRINT_MAT), "sheet": catalog.density(SHEET_MAT), "tyre": catalog.density("tpu")}
    for _name, (solid, kind) in made.items():
        m += solid.volume / 1000.0 * rho[kind]
    return m
