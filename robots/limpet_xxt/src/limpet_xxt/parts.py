"""Limpet XXT parts, one function per manufactured part.

Each part is built in its OWN local frame (the spec places it with at/rot):
  tub            world frame (origin on the centre line, mid wheelbase)
  lid / side     plate centre
  flipper, hinge_block   hinge frame (origin on the hinge axis, plate along +X, top face at z=0)
  horn, drive_pin        servo output frame (origin on the output axis, arm along +X)
  wheel          axle frame (origin at the wheel centre, axis along +X)
  hinge_pin      on the hinge axis, along Y

Manufacture (as the photos suggest, see REFERENCE.md):
  tub            FDM print (PLA), open top, M2 heat-set inserts in wall pads and standoff columns
  lid (x2)       2D-cut 1.5 mm polycarbonate, left = mirror of the right (minus the switch slot)
  side plate (x2) 2D-cut 2 mm polycarbonate hexagon; left = mirror of the right
  flipper        2D-cut 2 mm polycarbonate, chamfered front corners, screwed to the hinge block
  hinge block    FDM print: centre knuckle + flipper seat + tail lever (the tail end face is the drive face)
  horn           FDM print: hub + arm + pin tab (union of overlapping boxes, manifold), drive pin in the tab bore
  wheels (x4)    printed hub + tyre, D-bore on the motor shaft
Catalogue parts (motors, servo, battery, ESC, switch) are placed, never redrawn.
"""
import math

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


def y_cyl(r, length):
    """Cylinder with its axis on Y, centred on the origin."""
    return bd.Rot(90, 0, 0) * bd.Cylinder(r, length)


def x_cyl(r, length):
    """Cylinder with its axis on X, centred on the origin."""
    return bd.Rot(0, 90, 0) * bd.Cylinder(r, length)


def catalog_solid(cid):
    """A catalogue part's own solid (reused through revron hw: one cached conversion per id)."""
    return hw._solid(cid)


def mirror_y(part):
    """Left-hand copy of a right-hand (-Y) part."""
    return bd.mirror(part, bd.Plane.XZ)


def _fillet_edges(part, r, cand):
    """Fillet the edges selected by `cand(part)` at radius r. Tries one batch; on failure, trials each
    edge alone on the original shape, then batches the ones that work (so one bad edge does not leave
    the whole seam sharp)."""
    edges = cand(part)
    if not edges:
        return part
    try:
        return part.fillet(r, edges)
    except Exception:  # noqa: BLE001
        pass
    def key(e):
        c = e.center()
        return (round(c.X, 3), round(c.Y, 3), round(c.Z, 3))
    good, bad = set(), []
    for e in edges[:24]:
        try:
            part.fillet(r, [e])
            good.add(key(e))
        except Exception:  # noqa: BLE001
            bad.append(key(e))
    if bad:
        print(f"fillet rejected {len(bad)} edge(s), e.g. {bad[:3]}")
    if good:
        try:
            return part.fillet(r, [e for e in cand(part) if key(e) in good])
        except Exception:  # noqa: BLE001
            pass
    if not good:
        print(f"fillet skipped ({len(edges)} edges)")
    return part


def _fillet_near(part, r, plane_ys, xz_centers, tol=1.5, plane_xs=()):
    """Fillet the sharp rim edges whose centre sits within RIM_TOL of any y in `plane_ys` (all y when empty)
    and any x in `plane_xs` (when given) and within r+tol of any (x, z) in `xz_centers` (the seams where
    knuckles / columns / pads cross the wall faces)."""
    def cand(p):
        return [e for e in p.edges()
                if (not plane_ys or any(abs(e.center().Y - py) < RIM_TOL for py in plane_ys))
                and (not plane_xs or any(abs(e.center().X - px) < RIM_TOL for px in plane_xs))
                and any(math.hypot(e.center().X - cx, e.center().Z - cz) < r + tol for cx, cz in xz_centers)]
    return _fillet_edges(part, r, cand)


# --------------------------------------------------------------------------------------------------------- tub
def _bays():
    """Battery (centre channel, rear) and ESC (left side zone) bays from robot/cad/bay.py, drop-in from the top."""
    bat = bay_lib.derive_bay(catalog.find(BATTERY_ID), wall=WALL, insert_dir="-z",
                             placement=bd.Pos(BAT_X, 0, TUB_Z0 + WALL + BAT_H / 2))
    esc = bay_lib.derive_bay(catalog.find(ESC_ID), wall=WALL, insert_dir="-z",
                             placement=bd.Pos(ESC_X, SIDE_ZONE_Y, TUB_Z0 + WALL + ESC_H / 2))
    return bat, esc


def switch_z():
    """Switch centre height: knob pokes 0.5 mm through the lid slot."""
    bb = catalog_solid(SWITCH_ID).bounding_box()
    return LID_Z1 + 0.5 - bb.max.Z


def switch_pose():
    """Switch in the right zone, high on its tray, knob through the lid slot."""
    return bd.Pos(SW_X, -SIDE_ZONE_Y, switch_z())


def _switch_tray():
    """Printed pillar from the floor up to the switch, snug cavity, so the switch is captured floor-to-lid.
    The switch stands upright (long side along X), so the tray is long in X and narrow in Y."""
    sw_l, sw_w, _ = hw.size(SWITCH_ID)
    bb = catalog_solid(SWITCH_ID).bounding_box()
    z_bot = switch_z() + bb.min.Z                       # switch bottom in world
    z_top = switch_z() + bb.max.Z
    tray = bd.Pos(SW_X, -SIDE_ZONE_Y, (TUB_Z0 + WALL + z_bot) / 2) * \
        bd.Box(sw_l + 2 * CLEAR, sw_w + 2 * CLEAR, z_bot - TUB_Z0 - WALL)
    cav = bd.Pos(SW_X, -SIDE_ZONE_Y, (z_bot - EPS + z_top + EPS) / 2) * \
        bd.Box(sw_l + 2 * CAV_FIT, sw_w + 2 * CAV_FIT, z_top - z_bot + 2 * EPS)
    return tray - cav


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
    inner = inner.fillet(1.2, [e for e in inner.edges()
                               if e.bounding_box().size.X < 1e-6 and e.bounding_box().size.Y < 1e-6])
    body = outer - inner

    # servo tray: block filling the channel around the servo, snug cavity OPEN AT THE TOP (the servo lifts out
    # +z once the lids are off), horn slot piercing the +Y wall, lead slot in the -X wall for the servo wire
    tray_cx = SERVO_X + SERVO_X_OFF
    tray = bd.Pos(tray_cx, 0, (TUB_Z0 + WALL + TRAY_TOP_Z) / 2) * \
        bd.Box(SERVO_LEN + 2 * TRAY_WALL, 2 * TRAY_HALF_Y, TRAY_TOP_Z - TUB_Z0 - WALL)
    cav = bd.Pos(tray_cx, 0, (TUB_Z0 + WALL - EPS + TRAY_TOP_Z + EPS) / 2) * \
        bd.Box(SERVO_LEN + 2 * SERVO_CAV_FIT, 2 * (SERVO_FACE_Y + SERVO_CAV_FIT), TRAY_TOP_Z + EPS - (TUB_Z0 + WALL - EPS))
    slot = bd.Pos((HORN_SLOT_X0 + HORN_SLOT_X1) / 2, TRAY_HALF_Y - TRAY_WALL / 2,
                  (HORN_SLOT_Z0 + TRAY_TOP_Z + EPS) / 2) * \
        bd.Box(HORN_SLOT_X1 - HORN_SLOT_X0, TRAY_WALL + 2 * HORN_SLOT_MARGIN, TRAY_TOP_Z + EPS - HORN_SLOT_Z0)
    lead = bd.Pos(tray_cx - SERVO_LEN / 2 - TRAY_WALL / 2 + EPS, 0, (LEAD_SLOT_Z0 + LEAD_SLOT_Z1) / 2) * \
        bd.Box(TRAY_WALL + 2 * EPS, 2 * LEAD_SLOT_HALF_Y, LEAD_SLOT_Z1 - LEAD_SLOT_Z0)
    body = body + (tray - cav - slot - lead)

    # switch tray (right zone)
    body = body + _switch_tray()

    # lid pads: wall-thickening pads with blind insert bores open at the wall top; each bore mouth is
    # filleted right after the pad is added, while the shape is still simple (the pad/wall seams are
    # left to the end-of-body fillets — post-union seam fillets here segfault OCCT)
    bz0 = TUB_Z1 - LID_PAD_H + LID_PAD_BORE_FLOOR
    for s in (1, -1):
        for x, pw in LID_PADS:
            pad = bd.Pos(x, s * LID_PAD_Y, TUB_Z1 - LID_PAD_H / 2) * bd.Box(pw, LID_PAD_D, LID_PAD_H)
            bore = bd.Pos(x, s * LID_PAD_Y, (bz0 + TUB_Z1 + EPS) / 2) * \
                bd.Cylinder(INSERT_OD / 2 - CLEAR / 2, TUB_Z1 + EPS - bz0)
            body = body + pad - bore

            def _mouths(p, x=x, s=s):
                return [e for e in p.edges()
                        if e.geom_type == bd.GeomType.CIRCLE
                        and (abs(e.center().Z - TUB_Z1) < RIM_TOL or abs(e.center().Z - bz0) < RIM_TOL)
                        and math.hypot(e.center().X - x, e.center().Y - s * LID_PAD_Y) < 1.5]
            body = _fillet_edges(body, 1.0, _mouths)

            def _pad_seams(p, x=x, s=s, pw=pw):
                return [e for e in p.edges()
                        if abs(e.center().Y - s * (TUB_W / 2 - WALL)) < RIM_TOL
                        and abs(e.center().X - x) < pw / 2 + 0.5]
            body = _fillet_edges(body, 1.0, _pad_seams)

    # standoff columns to the side plates (mirror pattern), insert bores through the full column
    for s in (-1, 1):
        for x in STANDOFF_XS:
            for z in PLATE_SCREWS_Z:
                col = bd.Pos(x, s * (TUB_W / 2 + SPACER_L / 2), z) * y_cyl(STANDOFF_D / 2, SPACER_L)
                bore = bd.Pos(x, s * (TUB_W / 2 + SPACER_L / 2), z) * y_cyl(INSERT_OD / 2 - CLEAR / 2, SPACER_L + 2 * EPS)
                body = body + col - bore

    # outer hinge knuckles on the front top edge (the block's centre knuckle sits between them, 4 mm clear);
    # the wall's front-top corner is notched away over the whole hinge-block swing envelope
    for s in (-1, 1):
        k = bd.Pos(HINGE_X, s * TUB_KNUCKLE_Y, HINGE_Z) * y_cyl(HINGE_BOSS_D / 2, TUB_KNUCKLE_W - 2 * CLEAR)
        bore = bd.Pos(HINGE_X, s * TUB_KNUCKLE_Y, HINGE_Z) * y_cyl(PIN_TUB_BORE_R, TUB_KNUCKLE_W + 2 * EPS)
        body = body + k - bore
    notch = bd.Pos((RELIEF_X0 + RELIEF_X1) / 2, 0, (RELIEF_Z0 + TUB_Z1 + EPS) / 2) * \
        bd.Box(RELIEF_X1 - RELIEF_X0, 2 * RELIEF_HALF_Y, TUB_Z1 + EPS - RELIEF_Z0)
    body = body - notch

    # motor pockets: snug (MOTOR_FIT per side), closed top (wall above captures the motor), through the outer wall;
    # the shaft hole passes the wall into the wheel well. Motors slide in axially before the wheels go on.
    for front in (True, False):
        x = AXLES_X[0] if front else AXLES_X[1]
        for s in (-1, 1):
            pocket = bd.Pos(x, s * (MOTOR_INNER_Y - MOTOR_FIT + MOTOR_ROOT_Y + POCKET_OUT) / 2, AXLE_Z) * \
                bd.Box(2 * (MOTOR_ENV_X + MOTOR_FIT), MOTOR_ROOT_Y + POCKET_OUT - MOTOR_INNER_Y + MOTOR_FIT,
                       2 * (MOTOR_ENV_Z + MOTOR_FIT))
            shaft_hole = bd.Pos(x, s * (MOTOR_ROOT_Y - SHAFT_HOLE_IN + (SHAFT_HOLE_IN + SHAFT_HOLE_OUT) / 2), AXLE_Z) * \
                y_cyl(MOTOR_SHAFT["dia"] / 2 + SHAFT_HOLE_FIT, SHAFT_HOLE_IN + SHAFT_HOLE_OUT)
            body = body - pocket - shaft_hole

    # electronics bays (bay.py cut solids)
    for b in _bays():
        body = body - b.cut_solid()

    # rim fillets LAST: a fillet applied before a later boolean gets sliced by it, and the trimmed
    # tangent patches tessellate with T-junctions (non-watertight mesh). On the finished body every
    # fillet terminates transversally and the mesh stays closed.
    def _shell(p):
        return [e for e in p.edges()
                if (TUB_XC - TUB_L / 2 + WALL - SELECT_TOL <= e.center().X <= TUB_XC + TUB_L / 2 - WALL + SELECT_TOL
                    and abs(e.center().Y) <= TUB_W / 2 - WALL + SELECT_TOL
                    and TUB_Z0 + WALL - SELECT_TOL <= e.center().Z <= TUB_Z1 + SELECT_TOL)
                ]
    def _notch(p):
        return [e for e in p.edges()
                if RELIEF_X0 - SELECT_TOL <= e.center().X <= RELIEF_X1 + SELECT_TOL
                and abs(e.center().Y) <= RELIEF_HALF_Y + SELECT_TOL
                and RELIEF_Z0 - SELECT_TOL <= e.center().Z <= TUB_Z1 + SELECT_TOL]
    body = _fillet_edges(body, 1.0, _notch)
    rim_centers = [(HINGE_X, HINGE_Z)] * 2 + [(x, z) for x in STANDOFF_XS for z in PLATE_SCREWS_Z]
    body = _fillet_near(body, 1.0, (TUB_W / 2 - WALL, TUB_W / 2), rim_centers)
    body = _fillet_edges(body, 1.0, _shell)

    return body


# --------------------------------------------------------------------------------------------------------- lids
def _lid(side):
    """Lid plate in its own frame (centred), covering tub wall to centre channel edge on one side."""
    s = side
    w = TUB_W / 2 - CHANNEL_HALF_W
    plate = bd.Box(LID_X1 - BODY_X0, w, LID_T)
    cx, cy = (BODY_X0 + LID_X1) / 2, s * (CHANNEL_HALF_W + w / 2)
    # armour deck shutting the centre channel from above (motors, servo, battery and ESC otherwise
    # have line of sight out through the open channel); ends at LID_DECK_X1 clear of the
    # tail-lever sweep (lever crosses the lid plane at x 7.57..37.63)
    deck = bd.Pos((BODY_X0 + LID_DECK_X1) / 2 - cx, s * CHANNEL_HALF_W / 2 - cy, 0) * \
        bd.Box(LID_DECK_X1 - BODY_X0, CHANNEL_HALF_W, LID_T)
    if s > 0:
        notch = bd.Pos((LID_DECK_NOTCH_X0 + LID_X1) / 2 - cx,
                       (LID_DECK_SLOT_Y0 + CHANNEL_HALF_W + CLEAR) / 2 - cy, 0) * \
            bd.Box(LID_X1 - LID_DECK_NOTCH_X0 + 2 * CLEAR, CHANNEL_HALF_W + CLEAR - LID_DECK_SLOT_Y0,
                   LID_T + 2 * EPS)
        deck = deck - notch
    plate = plate + deck
    deck_corners = [(LID_DECK_X1, -CHANNEL_HALF_W)] if s < 0 else \
        [(LID_DECK_NOTCH_X0, LID_DECK_SLOT_Y0), (LID_DECK_NOTCH_X0, CHANNEL_HALF_W)]
    try:
        edges = [e for e in plate.edges()
                 if abs(e.center().Z) < 0.1
                 and any(math.hypot(e.center().X - (px - cx), e.center().Y - (py - cy)) < 1.0
                         for px, py in deck_corners)]
        if edges:
            plate = plate.fillet(LID_SLOT_R, edges)
    except Exception as e:  # noqa: BLE001
        print(f"lid deck corner fillet skipped: {type(e).__name__}: {e}")
    for x in (LID_SCREWS_X_L if s > 0 else LID_SCREWS_X_R):
        plate = plate - bd.Pos(x - cx, s * LID_PAD_Y - cy, 0) * screw_hole(LID_T)
    if s < 0:   # switch slot in the right lid (switch stands upright: slot long in X), corners rounded to the kerf
        sw_l, sw_w, _ = hw.size(SWITCH_ID)
        slot = bd.Pos(SW_X - cx, -SIDE_ZONE_Y - cy, 0) * bd.Box(sw_l + 2 * CLEAR, sw_w + 2 * CLEAR, LID_T + 2 * EPS)
        plate = plate - slot
        try:
            scx, scy = SW_X - cx, -SIDE_ZONE_Y - cy
            edges = [e for e in plate.edges()
                     if abs(e.center().Z) < 0.1
                     and abs(e.center().X - scx) < sw_l / 2 + 0.6
                     and abs(e.center().Y - scy) < sw_w / 2 + 0.6]
            if edges:
                plate = plate.fillet(LID_SLOT_R, edges)
        except Exception as e:  # noqa: BLE001
            print(f"lid slot fillet skipped: {type(e).__name__}: {e}")
    return plate, (cx, cy, TUB_Z1 + LID_T / 2)


def lid_right():
    return _lid(-1)[0]


def lid_left():
    return _lid(1)[0]


def lid_at(side):
    w = TUB_W / 2 - CHANNEL_HALF_W
    return ((BODY_X0 + LID_X1) / 2, side * (CHANNEL_HALF_W + w / 2), TUB_Z1 + LID_T / 2)


# --------------------------------------------------------------------------------------------------- side plates
def _side_plate(side):
    """Hexagonal PC plate (chamfered corners, photos) in its own frame, centred on the plate."""
    c = PLATE_CHAMFER
    x0, x1, z0, z1 = BODY_X0, BODY_X1, PLATE_Z0, PLATE_Z0 + PLATE_H
    pts = [(x0 + c, z0), (x1 - c, z0), (x1, z0 + c), (x1, z1 - c), (x1 - c, z1), (x0 + c, z1), (x0, z1 - c), (x0, z0 + c)]
    plate = bd.Rot(90, 0, 0) * bd.extrude(bd.Polygon(*pts, align=None), amount=SHEET_T)   # XZ outline, Y thickness
    cx, cz = (x0 + x1) / 2, (z0 + z1) / 2
    for x in STANDOFF_XS:
        for z in PLATE_SCREWS_Z:
            plate = plate - bd.Pos(x, -SHEET_T / 2, z) * y_cyl(PLATE_HOLE_D / 2, SHEET_T + 2 * EPS)
    bb = plate.bounding_box()
    plate = plate.moved(bd.Pos(-(bb.min.X + bb.max.X) / 2, -(bb.min.Y + bb.max.Y) / 2, -(bb.min.Z + bb.max.Z) / 2))
    return plate


def side_plate_right():
    return _side_plate(-1)


def side_plate_left():
    return _side_plate(1)


def side_at(side):
    x0, x1, z0, z1 = BODY_X0, BODY_X1, PLATE_Z0, PLATE_Z0 + PLATE_H
    return ((x0 + x1) / 2, side * SIDE_Y, (z0 + z1) / 2)


# ------------------------------------------------------------------------------------------------------ flipper
def flipper():
    """Flipper plate in the hinge frame: hinge axis = Y through the origin, plate along +X, top face z = 0."""
    c = FLIP_CHAMFER
    h, L = FLIP_W / 2, FLIP_LEN
    pts = [(HINGE_BOSS_D / 2, -h), (L - c, -h), (L, -h + c), (L, h - c), (L - c, h), (HINGE_BOSS_D / 2, h)]
    plate = bd.extrude(bd.Polygon(*pts, align=None), amount=-SHEET_T)
    for y in (-HINGE_BOLT_Y, HINGE_BOLT_Y):
        plate = plate - bd.Pos(BOLT_HB_X, y, -SHEET_T / 2) * screw_hole(SHEET_T)
    return plate


def hinge_block():
    """Printed centre knuckle + flipper seat + tail lever, in the hinge frame (child of the flipper)."""
    knuckle_w = BLOCK_KNUCKLE_W - 2 * CLEAR
    knuckle = y_cyl(HINGE_BOSS_D / 2, knuckle_w)
    def _rims(p):    # round the knuckle's OUTER end rims only (load zone of the hinge pin; bore cut after union)
        return [e for e in p.edges()
                if abs(abs(e.center().Y) - knuckle_w / 2) < RIM_TOL
                and math.hypot(e.center().X, e.center().Z) > HINGE_BOSS_D / 2 - BORE_GUARD]
    knuckle = _fillet_edges(knuckle, KNUCKLE_RIM_FILLET_R, _rims)
    seat = bd.Pos(SEAT_X0 + SEAT_L / 2, 0, -SHEET_T - SEAT_H / 2) * bd.Box(SEAT_L, SEAT_W, SEAT_H)
    for y in (-HINGE_BOLT_Y, HINGE_BOLT_Y):
        seat = seat - bd.Pos(BOLT_HB_X, y, -SHEET_T - SEAT_H / 2) * bd.Cylinder(SEAT_HOLE_D / 2, SEAT_H + 2 * EPS)

    def _top(p):    # round the seat's top rim: perimeter edges and insert-bore mouths (bolt load zone)
        return [e for e in p.edges() if abs(e.center().Z + SHEET_T) < RIM_TOL]
    seat = _fillet_edges(seat, SEAT_TOP_FILLET_R, _top)
    # web: the knuckle circle (r 2.6) curves away below z=-2.0, so the seat (top at -SHEET_T) never reaches it;
    # this thin web at the seat's top rim fuses knuckle and seat while staying clear of the servo tray
    web = bd.Pos((SEAT_WEB_X0 + SEAT_WEB_X1) / 2, 0, -SHEET_T - SEAT_WEB_H / 2) * \
        bd.Box(SEAT_WEB_X1 - SEAT_WEB_X0, SEAT_W, SEAT_WEB_H)
    block = knuckle + web + seat
    tail = bd.Pos(-TAIL_L / 2, 0, 0) * bd.Box(TAIL_L, TAIL_W, TAIL_H)
    block = block + tail
    block = block - y_cyl(KNUCKLE_BORE_R, BLOCK_KNUCKLE_W + 2 * EPS)   # pin bore through the whole block
    def _seams(p):    # round the concave web seams (knuckle and seat)
        return [e for e in p.edges()
                if SEAT_WEB_X0 - RIM_TOL <= e.center().X <= HINGE_BOSS_D / 2
                and -SHEET_T - SEAM_DZ < e.center().Z < -SHEET_T + SEAM_DZ_TOP]
    block = _fillet_edges(block, SEAT_WEB_FILLET_R, _seams)
    return block


def horn():
    """Servo horn in the servo output frame: hub on the axis, arm out to the pin tab (overlapping boxes, manifold)."""
    hub = y_cyl(3.0, 2 * HORN_HALF_Y)
    arm = bd.Pos(HORN_R / 2 - 1.5, 0, 0) * bd.Box(HORN_R + 3.0, 2 * HORN_HALF_Y, HORN_ARM_W)
    tab = bd.Pos(HORN_R, 0, 0) * bd.Box(HORN_TAB[0], 2 * HORN_HALF_Y, HORN_TAB[1])
    bore = bd.Pos(HORN_R, 0, 0) * y_cyl(HORN_PIN_BORE_R, 2 * HORN_HALF_Y + 2 * EPS)
    return hub + arm + tab - bore


def drive_pin():
    """M2 drive pin through the horn tab bore, inner end bearing on the tail end face (horn frame)."""
    return bd.Pos(HORN_R, (PIN_Y0 + PIN_Y1) / 2, 0) * y_cyl(HINGE_PIN_D / 2, PIN_Y1 - PIN_Y0)


def hinge_pin():
    """M2 hinge pin through all knuckles, along Y centred on the hinge axis."""
    return y_cyl(HINGE_PIN_D / 2, FLIP_W + 2.0)


# ------------------------------------------------------------------------------------------------------- wheels
def wheel(front, left):
    """Wheel in the axle frame: printed hub + tyre with a D-bore matching the N10 shaft flat."""
    bore = x_cyl(BORE_R, WHEEL_W + 2 * EPS) & bd.Pos(0, 0, BORE_FLAT_Z - 1.5) * bd.Box(WHEEL_W + 2 * EPS, BORE_FLAT_W, 3.0)
    return x_cyl(WHEEL_D / 2, WHEEL_W) - bore


# --------------------------------------------------------------------------------------------------------- mass
def mass_g(made):
    """Catalogue masses + printed / sheet part volumes (densities from robot.catalog.MATERIALS)."""
    cat_ids = [DRIVE_MOTOR_ID] * 4 + [SERVO_ID, BATTERY_ID, ESC_ID, SWITCH_ID]
    m = sum(catalog.find(c).mass_g for c in cat_ids)
    rho = {"print": catalog.density(PRINT_MAT), "sheet": catalog.density(SHEET_MAT), "tyre": catalog.density("tpu")}
    for name, (solid, kind) in made.items():
        m += solid.volume / 1000.0 * rho[kind]
    return m
