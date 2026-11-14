"""Limpet XXT parts, one function per manufactured part. UNTESTED: written without running anything.

Manufacture (as the photos suggest, see REFERENCE.md):
  tub            FDM print (PLA), open top, M2 heat-set inserts
  lid (x2)       2D-cut 1.5 mm polycarbonate, decal underneath; left one = mirror of the right
  side plate (x2) 2D-cut 2 mm polycarbonate hexagon; left = mirror of the right
  flipper        2D-cut 2 mm polycarbonate, chamfered front corners
  hinge block    FDM print: centre hinge knuckle + flipper seat + tail lever with the servo-pin slot
  horn           FDM print (or the servo's own horn) with a drive pin
  wheels (x4)    printed hub + tyre (PR #68 robot.modules.wheel when present, same relations otherwise)
Catalogue parts (motors, servo, battery, ESC, switch) are placed, never redrawn.
"""
import build123d as bd

from robot import catalog
from robot.cad import bay as bay_lib

from .params import *  # noqa: F401,F403
from .params import hw

EPS = bay_lib.CUT_OVERSHOOT   # booleans pass the faces they open


# ------------------------------------------------------------------------------------------------------- helpers
def screw_hole(length, d=SCREW_CLEAR_D):
    """Through hole along Z, centred on the origin."""
    return bd.Cylinder(d / 2, length + 2 * EPS)


def insert_bore(depth):
    """Heat-set bore going down from Z = 0 (the boss top)."""
    return bd.Pos(0, 0, -depth / 2 + EPS) * bd.Cylinder(INSERT_OD / 2 - CLEAR / 2, depth + EPS)


def y_cyl(r, length):
    """Cylinder with its axis on Y, centred on the origin."""
    return bd.Rot(90, 0, 0) * bd.Cylinder(r, length)


def catalog_solid(cid):
    """A catalogue part's own solid (reused through revron hw: one cached conversion per id)."""
    return hw._solid(cid)


def mirror_y(part):
    """Left-hand copy of a right-hand (-Y) part."""
    return bd.mirror(part, bd.Plane.XZ)


# --------------------------------------------------------------------------------------------------------- tub
def _bays():
    """Battery (centre channel, rear) and ESC (left side zone) bays from robot/cad/bay.py, drop-in from the top."""
    bat = bay_lib.derive_bay(catalog.find(BATTERY_ID), wall=WALL, insert_dir="-z",
                             placement=bd.Pos(BAT_X, 0, TUB_Z0 + WALL + BAT_H / 2))
    esc = bay_lib.derive_bay(catalog.find(ESC_ID), wall=WALL, insert_dir="-z",
                             placement=bd.Pos(ESC_X, SIDE_ZONE_Y, TUB_Z0 + WALL + ESC_H / 2))
    return bat, esc


def motor_pose(front, left):
    """Catalogue gearmotor frame (+X = shaft) -> robot: shaft points outboard along +-Y, root on the wall face."""
    x = AXLES_X[0] if front else AXLES_X[1]
    s = 1 if left else -1
    root = bd.Pos(x, s * MOTOR_ROOT_Y, AXLE_Z) * bd.Rot(0, 0, 90 * s)
    return root * bd.Pos(-MOTOR_SHAFT["at"][0], 0, 0)


def servo_pose():
    """Servo on its side in the centre channel: catalogue Z (output axis) -> robot +Y."""
    return bd.Pos(SERVO_X, 0, SERVO_OUT_Z) * bd.Rot(-90, 0, 0)


def tub():
    outer = bd.Pos(TUB_XC, 0, TUB_Z0 + TUB_H / 2) * bd.Box(TUB_L, TUB_W, TUB_H)
    inner = bd.Pos(TUB_XC, 0, TUB_Z0 + WALL + TUB_H / 2) * bd.Box(TUB_L - 2 * WALL, TUB_W - 2 * WALL, TUB_H)
    body = outer - inner

    # standoff columns to the side plates (mirror pattern), insert bores in their outer ends
    for x in PLATE_SCREWS_X:
        for z in PLATE_SCREWS_Z:
            col = bd.Pos(x, -(TUB_W / 2 + SPACER_L / 2), z) * y_cyl(STANDOFF_D / 2, SPACER_L + WALL)
            bore = bd.Pos(x, -(TUB_W / 2 + SPACER_L), z) * bd.Rot(-90, 0, 0) * insert_bore(INSERT_L)
            body = body + col + mirror_y(col) - bore - mirror_y(bore)

    # lid inserts: corner bosses on the wall tops (4 per lid, mirror pattern)
    for x in LID_SCREWS_X:
        y = -(TUB_W / 2 - LID_SCREW_INSET)
        boss = bd.Pos(x, y, TUB_Z1 - INSERT_L / 2) * bd.Cylinder(INSERT_OD / 2 + WALL, INSERT_L)
        bore = bd.Pos(x, y, TUB_Z1) * insert_bore(INSERT_L)
        body = body + boss + mirror_y(boss) - bore - mirror_y(bore)

    # outer hinge knuckles on the front top edge (the flipper's centre knuckle sits between them)
    knuckle_w = FLIP_W / HINGE_KNUCKLES
    for s in (-1, 1):
        k = bd.Pos(HINGE_X, s * knuckle_w, HINGE_Z) * y_cyl(HINGE_BOSS_D / 2, knuckle_w - 2 * CLEAR)
        body = body + k - bd.Pos(HINGE_X, s * knuckle_w, HINGE_Z) * y_cyl(HINGE_PIN_D / 2, knuckle_w + EPS)

    # motor pockets: catalogue envelope grown by the fit clearance, swept up through the open top; shaft holes
    for front in (True, False):
        for left in (True, False):
            env = catalog_solid(DRIVE_MOTOR_ID)
            bb = env.bounding_box()
            z_lo = -bb.size.Z / 2 - CLEAR                        # motor frame: axis at z = 0
            z_hi = TUB_Z1 - AXLE_Z + EPS                         # swept up through the open top (drop-in)
            pocket = bd.Pos(bb.center().X, 0, (z_lo + z_hi) / 2) * bd.Box(bb.size.X + 2 * CLEAR, bb.size.Y + 2 * CLEAR,
                                                                          z_hi - z_lo)
            body = body - motor_pose(front, left) * pocket

    # servo pocket (lying on its side, open to the top for the horn and tail)
    sl, sw, sh = SERVO_L + 2 * CLEAR, SERVO_H + 2 * CLEAR, SERVO_W + 2 * CLEAR
    body = body - bd.Pos(SERVO_X, 0, TUB_Z0 + WALL + TUB_H / 2) * bd.Box(sl, sw, TUB_H + EPS)
    # servo retention: on its side the ear holes run along Y with no wall to screw into, so the pocket is a snug
    # drop-in and the lids hold it down (GUESS; SERVO_HOLES kept for a future printed ear post)

    # electronics bays (bay.py cut solids), switch slot through the right lid zone
    for b in _bays():
        body = body - b.cut_solid()
    sw_l, sw_w, sw_h = hw.size(SWITCH_ID)
    body = body - bd.Pos(ESC_X, -SIDE_ZONE_Y, TUB_Z1 - sw_h / 2) * bd.Box(sw_l + 2 * CLEAR, sw_w + 2 * CLEAR, sw_h + EPS)
    return body


# --------------------------------------------------------------------------------------------------------- lids
def lid_right():
    """Right lid: tub wall to the centre channel edge; the slot between the two lids shows the tail and battery."""
    w = TUB_W / 2 - CHANNEL_HALF_W
    plate = bd.Pos(TUB_XC, -(CHANNEL_HALF_W + w / 2), TUB_Z1 + LID_T / 2) * bd.Box(TUB_L, w, LID_T)
    for x in LID_SCREWS_X:
        plate = plate - bd.Pos(x, -(TUB_W / 2 - LID_SCREW_INSET), TUB_Z1 + LID_T / 2) * screw_hole(LID_T)
    sw_l, sw_w, _ = hw.size(SWITCH_ID)
    plate = plate - bd.Pos(ESC_X, -SIDE_ZONE_Y, TUB_Z1 + LID_T / 2) * bd.Box(sw_l, sw_w, LID_T + 2 * EPS)
    return plate


def lid_left():
    """Left lid: the right lid's mirror image without the switch cut-out (the switch is on the right only)."""
    w = TUB_W / 2 - CHANNEL_HALF_W
    plate = bd.Pos(TUB_XC, CHANNEL_HALF_W + w / 2, TUB_Z1 + LID_T / 2) * bd.Box(TUB_L, w, LID_T)
    for x in LID_SCREWS_X:
        plate = plate - bd.Pos(x, TUB_W / 2 - LID_SCREW_INSET, TUB_Z1 + LID_T / 2) * screw_hole(LID_T)
    return plate


# --------------------------------------------------------------------------------------------------- side plates
def side_plate_right():
    """Hexagonal PC plate (chamfered corners, photos), XZ outline extruded SHEET_T outboard of the right wheels."""
    c = PLATE_CHAMFER
    x0, x1, z0, z1 = BODY_X0, BODY_X1, PLATE_Z0, PLATE_Z0 + PLATE_H
    pts = [(x0 + c, z0), (x1 - c, z0), (x1, z0 + c), (x1, z1 - c), (x1 - c, z1), (x0 + c, z1), (x0, z1 - c), (x0, z0 + c)]
    with bd.BuildPart() as p:
        with bd.BuildSketch(bd.Plane.XZ.offset(SIDE_Y - SHEET_T / 2)):
            bd.Polygon(*pts, align=None)
        bd.extrude(amount=SHEET_T)
        for x in PLATE_SCREWS_X:
            for z in PLATE_SCREWS_Z:
                bd.add(bd.Pos(x, -SIDE_Y, z) * bd.Rot(90, 0, 0) * screw_hole(SHEET_T), mode=bd.Mode.SUBTRACT)
    return p.part   # Plane.XZ normal is -Y: offset SIDE_Y lands the plate on the right (-Y) side


def side_plate_left():
    return mirror_y(side_plate_right())


# ------------------------------------------------------------------------------------------------------ flipper
def flipper():
    """Flipper plate in its hinge frame: hinge axis = Y through the origin, plate along +X, top face Z = 0."""
    c = FLIP_CHAMFER
    h, L = FLIP_W / 2, FLIP_LEN
    pts = [(HINGE_BOSS_D / 2, -h), (L - c, -h), (L, -h + c), (L, h - c), (L - c, h), (HINGE_BOSS_D / 2, h)]
    plate = bd.extrude(bd.Polygon(*pts, align=None), amount=-SHEET_T)
    # hinge block screws: a row of two across the centre knuckle (mirror pattern)
    for y in (-HINGE_BOSS_D, HINGE_BOSS_D):
        plate = plate - bd.Pos(HINGE_BOSS_D + HEAD_D, y, -SHEET_T / 2) * screw_hole(SHEET_T)
    return plate


def hinge_block():
    """Printed centre knuckle + flipper seat + tail lever (hinge frame as flipper())."""
    knuckle_w = FLIP_W / HINGE_KNUCKLES
    knuckle = y_cyl(HINGE_BOSS_D / 2, knuckle_w - 2 * CLEAR) - y_cyl(HINGE_PIN_D / 2, knuckle_w)
    seat_l = 2 * (HINGE_BOSS_D + HEAD_D)
    seat = bd.Pos(seat_l / 2, 0, -SHEET_T - WALL / 2) * bd.Box(seat_l, knuckle_w - 2 * CLEAR, WALL)
    for y in (-HINGE_BOSS_D, HINGE_BOSS_D):
        seat = seat - bd.Pos(HINGE_BOSS_D + HEAD_D, y, -SHEET_T - WALL / 2) * screw_hole(WALL, SCREW_TAP_D)
    tail = bd.Pos(-TAIL_L / 2, 0, 0) * bd.Box(TAIL_L, TAIL_W, HINGE_BOSS_D)
    slot = bd.Pos(-(TAIL_L - HORN_R), 0, 0) * bd.Box(TAIL_SLOT_L + HINGE_PIN_D, HINGE_PIN_D + CLEAR, HINGE_BOSS_D + 2 * EPS)
    return knuckle + seat + tail - slot


def horn():
    """Servo horn: arm of reach HORN_R in the servo's XZ plane, drive pin along Y at the tip (servo output frame)."""
    arm = bd.Pos(HORN_R / 2, 0, 0) * bd.Box(HORN_R + HINGE_BOSS_D, WALL, HINGE_BOSS_D)
    pin = bd.Pos(HORN_R, 0, 0) * y_cyl(HINGE_PIN_D / 2, TAIL_W + 2 * WALL)
    return arm + pin


# ------------------------------------------------------------------------------------------------------- wheels
def wheel():
    """Wheel in its axle frame (axle along +X, origin at centre). PR #68 Wheel module when importable."""
    try:
        from robot.modules.wheel import Wheel   # draft PR #68; not on dev at the time of writing
        res = Wheel(wheel_id=None, motor_id=DRIVE_MOTOR_ID, diameter_mm=WHEEL_D, width_mm=WHEEL_W).build()
        return res.parts["hub"] + res.parts["tyre"]
    except ImportError:   # same relation as the module: solid printed wheel, bore = shaft + fit clearance
        x_cyl = lambda r, l: bd.Rot(0, 90, 0) * bd.Cylinder(r, l)
        return x_cyl(WHEEL_D / 2, WHEEL_W) - x_cyl(MOTOR_SHAFT["dia"] / 2 + CLEAR / 3, WHEEL_W + EPS)


# --------------------------------------------------------------------------------------------------------- mass
def mass_g(made):
    """Catalogue masses + printed / sheet part volumes (densities from robot.catalog.MATERIALS)."""
    cat_ids = [DRIVE_MOTOR_ID] * 4 + [SERVO_ID, BATTERY_ID, ESC_ID, SWITCH_ID]
    m = sum(catalog.find(c).mass_g for c in cat_ids)
    rho = {"print": catalog.density(PRINT_MAT), "sheet": catalog.density(SHEET_MAT), "tyre": catalog.density("tpu")}
    for name, (solid, kind) in made.items():
        m += solid.volume / 1000.0 * rho[kind]
    return m
