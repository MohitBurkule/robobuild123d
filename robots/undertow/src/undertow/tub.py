"""Printed nylon tub: a hollow shell with spine ribs, printed bolt columns, skirt pads and the front pivot cheeks.

One quadrant's features (wheel notch, motor rib, lead slot, columns, pads, cheek) are built and mirrored. The wheel
pockets are notched through the side walls so the wheels slide out sideways once a plate is off; the motors and
electronics lift out the top. The shell + ribs + columns + pads + cheeks print as ONE solid in +z (no supports:
every feature is a through or top-open cut).
"""
import build123d as bd

from robot.cad.holes import hole_tool

from . import drive
from .params import (HALF_W_TUB, HALF_L_TUB, CORNER_R, Z_TUB0, TUB_H, WALL, WALL_FDM_MIN, BOLT_SITES, COLUMN_R,
                     TAP_D, TAP_OVERTURN, MOTOR_RIB_X0, MOTOR_RIB_Y0, MOTOR_RIB_Y1, LEAD_SLOT,
                     RAIL_T, RAIL_Y_IN, RAIL_Z0, RAIL_Z1, BULKHEAD_X0, BULKHEAD_X1, SHAFT_HOLE_R,
                     SKIRT_PAD_EMBED, SKIRT_PAD_T, SKIRT_PAD_W, SKIRT_PAD_Z0, SKIRT_PAD_Z1, SKIRT_PAD_Y, REAR_PAD_X,
                     CHEEK_T, CHEEK_HALF_X, CHEEK_REACH, PIN_Y, PIN_Z, PIN_CLEAR, EYE_R,
                     NUT_BOSS_R, NUT_BOSS_T, PIN_SCREW, X_MOTOR_BACK, Y_AXLE, Z_AXLE,
                     WELL, NOTCH_X1, MOTOR_FIT, MOTOR_CAN_W, MOTOR_CAN_H, RAIL_NOTCHES,
                     ESC, ESC_AT, ESC_Z, SWITCH, SWITCH_AT,
                     SW_POCKET_FIT, SW_POCKET_T, SW_POCKET_Z1, SW_POCKET_MERGE,
                     ESC_SHELF_T, ESC_SHELF_X0, ESC_SHELF_X_OVER, ESC_SHELF_Y_OVER, ESC_SHELF_MERGE,
                     ESC_CAP_FIT, ESC_CAP_T, ESC_CAP_RISE, ESC_CAP_SINK,
                     CUT_OVER, NOTCH_GAP, FIN_TIP_BACK)


def _switch_pocket():
    """Capture walls for the switch: it can't be screwed down (base_plate is 1 mm carbon, nothing to tap), so the
    tub clamps it on +y and +x; the -y inner rail (no notch there any more) and the motor rib close the other sides.
    Walls rise past the switch top so it stays captured inverted."""
    z0, z1 = RAIL_Z0, SW_POCKET_Z1
    y_in = SWITCH_AT[1] + SWITCH["body"][0] / 2 + SW_POCKET_FIT     # wall inner face: body +y face + fit
    x_in = SWITCH_AT[0] + SWITCH["body"][1] / 2 + SW_POCKET_FIT     # ... body +x face + fit
    y_hi = RAIL_Y_IN - RAIL_T + SW_POCKET_MERGE                     # +x wall root merges into the +y rail
    y_wall = bd.Pos((X_MOTOR_BACK + x_in + SW_POCKET_T) / 2, y_in + SW_POCKET_T / 2, (z0 + z1) / 2) * \
        bd.Box(x_in + SW_POCKET_T - X_MOTOR_BACK, SW_POCKET_T, z1 - z0)
    x_wall = bd.Pos(x_in + SW_POCKET_T / 2, (y_in + y_hi) / 2, (z0 + z1) / 2) * \
        bd.Box(SW_POCKET_T, y_hi - y_in, z1 - z0)
    return y_wall + x_wall


def _esc_shelf():
    """Printed shelf carrying the ESC over the pack lane: top face at the ESC bottom, merges into the +y rail.
    Capture walls on +y/-y (fit gap, rising past the ESC top) hold it like the switch pocket - the ESC case takes
    no adhesive and has no mounting holes."""
    z1 = ESC_Z - ESC["h"] / 2
    z0 = z1 - ESC_SHELF_T
    x1 = ESC_AT[0] + ESC["l"] / 2 + ESC_SHELF_X_OVER
    y_lo = -(ESC_AT[1] + ESC["w"] / 2 + ESC_CAP_FIT + ESC_CAP_T + ESC_SHELF_Y_OVER)
    y_hi = RAIL_Y_IN - RAIL_T + ESC_SHELF_MERGE
    plate = bd.Pos((ESC_SHELF_X0 + x1) / 2, (y_lo + y_hi) / 2, (z0 + z1) / 2) * \
        bd.Box(x1 - ESC_SHELF_X0, y_hi - y_lo, ESC_SHELF_T)
    wz0, wz1 = z1 - ESC_CAP_SINK, ESC_Z + ESC["h"] / 2 + ESC_CAP_RISE
    wy = bd.Pos((X_MOTOR_BACK + ESC_AT[0] + ESC["l"] / 2) / 2, ESC_AT[1] + ESC["w"] / 2 + ESC_CAP_FIT + ESC_CAP_T / 2,
                (wz0 + wz1) / 2) * bd.Box(ESC_AT[0] + ESC["l"] / 2 - X_MOTOR_BACK, ESC_CAP_T, wz1 - wz0)
    return plate + wy + wy.mirror(bd.Plane.XZ)


def outline(half_w=None, half_l=None, corner=None):
    """Plan outline, centred: a rounded rectangle."""
    return bd.RectangleRounded(2 * (half_w or HALF_W_TUB), 2 * (half_l or HALF_L_TUB), corner or CORNER_R)


def _shell():
    """Outer wall ring: outline extruded, inner cavity removed (inset WALL, corner radius reduced)."""
    outer = bd.Pos(0, 0, Z_TUB0) * bd.extrude(outline(), TUB_H)
    inner = bd.Pos(0, 0, Z_TUB0 - 0.1) * bd.extrude(
        outline(HALF_W_TUB - WALL, HALF_L_TUB - WALL, max(CORNER_R - WALL, 0.5)), TUB_H + 0.2)
    return outer - inner


def _ribs():
    """Motor back ribs: one per quadrant, from the spine out into the front / rear wall (one solid with the shell)."""
    x0, x1 = MOTOR_RIB_X0, X_MOTOR_BACK
    r = bd.Pos((x0 + x1) / 2, (MOTOR_RIB_Y0 + MOTOR_RIB_Y1) / 2, Z_TUB0 + TUB_H / 2) * bd.Box(
        x1 - x0, MOTOR_RIB_Y1 - MOTOR_RIB_Y0, TUB_H)
    r = r + r.mirror(bd.Plane.YZ)
    return r + r.mirror(bd.Plane.XZ)


def _rails():
    """Motor side rails: clamp the can from +-y (x rib..bulkhead, z over the motor)."""
    x0, x1 = MOTOR_RIB_X0, BULKHEAD_X1
    r = None
    for y0 in (RAIL_Y_IN - RAIL_T, RAIL_Y_IN + 12.0):
        blk = bd.Pos((x0 + x1) / 2, y0 + RAIL_T / 2, (RAIL_Z0 + RAIL_Z1) / 2) * bd.Box(
            x1 - x0, RAIL_T, RAIL_Z1 - RAIL_Z0)
        r = blk if r is None else r + blk
    r = r + r.mirror(bd.Plane.YZ)
    r = r + r.mirror(bd.Plane.XZ)
    # lane reliefs in the -y inner rail: the pack and the switch cross it, so the rail is interrupted there
    # (the pack presses the can, the stubs + outer rail + ribs keep the clamp)
    for cx, w in RAIL_NOTCHES:
        r = r - bd.Pos(cx, -(RAIL_Y_IN - RAIL_T / 2), (RAIL_Z0 + RAIL_Z1) / 2) * bd.Box(
            w, RAIL_T + 0.6, RAIL_Z1 - RAIL_Z0 + 2)
    return r


def _bulkhead():
    """Printed bulkhead outboard of the gearbox face: clamps the motors against the ribs from +x and shields the
    electronics from the wheels. Shaft clearance holes at each motor axis."""
    b = bd.Pos((BULKHEAD_X0 + BULKHEAD_X1) / 2, 0, Z_TUB0 + TUB_H / 2) * bd.Box(
        BULKHEAD_X1 - BULKHEAD_X0, 2 * HALF_L_TUB, TUB_H)
    b = b + b.mirror(bd.Plane.YZ)
    for sy in (1, -1):
        b = b - bd.Pos(0, sy * Y_AXLE, Z_AXLE) * bd.Rot(0, 90, 0) * \
            bd.Cylinder(SHAFT_HOLE_R, 2 * BULKHEAD_X1 + 2)
    # motor U-slot per motor, through the whole bulkhead (can footprint + fit, from under the can to past the
    # top): the motor lifts out the top as the docstring promises, shaft sliding up the slot (scythe's axle_holes
    # pattern); the rail clamp +-y and the rib clamp -x hold it in place.
    for sy in (1, -1):
        for sx in (1, -1):
            z_lo = Z_AXLE - MOTOR_CAN_H / 2 - MOTOR_FIT
            z_top = Z_TUB0 + TUB_H + 0.1
            b = b - bd.Pos(sx * (BULKHEAD_X0 + BULKHEAD_X1) / 2, sy * Y_AXLE, (z_lo + z_top) / 2) * bd.Box(
                BULKHEAD_X1 - BULKHEAD_X0 + 0.2, MOTOR_CAN_W + 2 * MOTOR_FIT, z_top - z_lo)
    return b


def _notches():
    """Wheel pockets notched through the side walls (aligned with the plate windows): once a plate is off, the
    wheels slide out sideways through the notch. The notch ends flush with the front / rear wall inner faces; the
    corner fin that still connects each wall to the side wall tapers to a knife edge at the outer corner radius, so
    the tip is cut back to where the fin is WALL_FDM_MIN thick."""
    x0, x1 = BULKHEAD_X1 + NOTCH_GAP, NOTCH_X1
    n = bd.Pos((x0 + x1) / 2, (WELL["y0"] + WELL["y1"]) / 2, Z_TUB0 + TUB_H / 2) * bd.Box(
        x1 - x0, WELL["y1"] - WELL["y0"], TUB_H + CUT_OVER)
    n = n + n.mirror(bd.Plane.YZ)
    n = n + n.mirror(bd.Plane.XZ)
    y_notch = HALF_L_TUB - WALL                                       # notch end face = wall inner face
    fin_tip = (HALF_W_TUB - CORNER_R) - (CORNER_R ** 2 - (CORNER_R - WALL + WALL_FDM_MIN) ** 2) ** 0.5
    x_lo = fin_tip - FIN_TIP_BACK
    x_hi = HALF_W_TUB + CUT_OVER
    for sx in (1, -1):
        for sy in (1, -1):
            n = n + bd.Pos(sx * (x_lo + x_hi) / 2, sy * (y_notch + HALF_L_TUB + CUT_OVER) / 2, Z_TUB0 + TUB_H / 2) * \
                bd.Box(x_hi - x_lo, HALF_L_TUB + CUT_OVER - y_notch, TUB_H + CUT_OVER)
    return n


def _lead_slots():
    """Wire slots through the ribs at each motor's terminals port (x = X_MOTOR_BACK, y = +-Y_AXLE, z = Z_AXLE).
    The slot spans the rib thickness plus a little either side so the wire passes clean into the bay."""
    w, h = LEAD_SLOT["w"], LEAD_SLOT["h"]
    x0, x1 = MOTOR_RIB_X0 - 0.2, X_MOTOR_BACK + 0.2
    s = bd.Pos((x0 + x1) / 2, Y_AXLE, Z_AXLE) * bd.Box(x1 - x0, w, h)
    s = s + s.mirror(bd.Plane.YZ)
    return s + s.mirror(bd.Plane.XZ)


def _columns():
    """Printed bolt columns (M2 tap) at the plate-bolt sites; they merge with the wall they sit in."""
    cols = [bd.Pos(x, y, Z_TUB0 - 0.1) * bd.Cylinder(COLUMN_R, TUB_H + 0.2,
                                                     align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
            for x, y in BOLT_SITES]
    out = cols[0]
    for c in cols[1:]:
        out = out + c
    return out


def _column_taps():
    """M2 tap drills through the columns (cut from the tub)."""
    cuts = []
    for x, y in BOLT_SITES:
        cuts.append(bd.Pos(x, y, Z_TUB0 - 0.1) * bd.Cylinder(TAP_D / 2, TUB_H + 0.2,
                                                              align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)))
    out = cuts[0]
    for c in cuts[1:]:
        out = out + c
    return out


def _pads():
    """Skirt pads: printed shelves on the side flanks (y = +-SKIRT_PAD_Y) and the rear flank (x = +-REAR_PAD_X).
    The side shelves run from the bulkhead out past the wall (the wheel notch isolates the mid-span wall strip,
    so the shelf roots on the bulkhead to stay one solid with the shell); the rear pads embed SKIRT_PAD_EMBED
    into the rear wall."""
    t = SKIRT_PAD_T
    x_out = HALF_W_TUB - SKIRT_PAD_EMBED + t   # pad outer face: the skirt seats flush on it
    x_in = BULKHEAD_X1 - 0.2                    # pad root, merged into the bulkhead
    side = bd.Pos((x_in + x_out) / 2, SKIRT_PAD_Y, (SKIRT_PAD_Z0 + SKIRT_PAD_Z1) / 2) * bd.Box(
        x_out - x_in, SKIRT_PAD_W, SKIRT_PAD_Z1 - SKIRT_PAD_Z0)
    side = side + side.mirror(bd.Plane.XZ) + side.mirror(bd.Plane.YZ) + side.mirror(bd.Plane.YZ).mirror(bd.Plane.XZ)
    y_face = -HALF_L_TUB                      # rear wall outer face
    rear = bd.Pos(REAR_PAD_X, y_face + SKIRT_PAD_EMBED - t / 2, (SKIRT_PAD_Z0 + SKIRT_PAD_Z1) / 2) * bd.Box(
        SKIRT_PAD_W, t, SKIRT_PAD_Z1 - SKIRT_PAD_Z0)
    rear = rear + rear.mirror(bd.Plane.YZ)
    return side + rear


def _pad_taps():
    """M2 tap drills in the pads, along the screw axis (X for the side pads, Y for the rear pads), both flanks.
    Each drill spans from just inside the pad's inner face to past its outer face, so it covers the whole screw."""
    zc = (SKIRT_PAD_Z0 + SKIRT_PAD_Z1) / 2
    x_in = HALF_W_TUB - SKIRT_PAD_EMBED                       # side pad inner face
    x_lo = HALF_W_TUB - WALL - TAP_OVERTURN                   # drill pierces the wall inner face: no end ligament
    x_hi = x_in + SKIRT_PAD_T + 1.5
    side = [bd.Pos((x_lo + x_hi) / 2, sy * SKIRT_PAD_Y, zc) * bd.Rot(0, 90, 0)
            * bd.Cylinder(TAP_D / 2, x_hi - x_lo) for sy in (1, -1)]
    side = side + [c.mirror(bd.Plane.YZ) for c in side]
    y_in = -HALF_L_TUB + SKIRT_PAD_EMBED                       # rear pad inner face
    y_lo = -(HALF_L_TUB - SKIRT_PAD_EMBED + SKIRT_PAD_T) - 1.5
    y_hi = -HALF_L_TUB + WALL + TAP_OVERTURN                   # drill pierces the wall inner face: no end ligament
    rear = [bd.Pos(sx * REAR_PAD_X, (y_lo + y_hi) / 2, zc) * bd.Rot(90, 0, 0)
            * bd.Cylinder(TAP_D / 2, y_hi - y_lo) for sx in (1, -1)]
    out = side[0] + rear[0]
    for c in side[1:] + rear[1:]:
        out = out + c
    return out


def cheeks():
    """The shared front-mount interface: two printed cheeks on the front wall carrying the pivot pin, plus the
    nyloc boss (hex pocket) on the +X cheek outer face."""
    prof = bd.Rectangle(CHEEK_REACH + EYE_R + 0.5, 2 * EYE_R, align=(bd.Align.MIN, bd.Align.CENTER))
    c = []
    for sx in (1, -1):
        blk = bd.extrude(bd.Plane.YZ.offset(sx * CHEEK_HALF_X - CHEEK_T / 2)
                         * bd.Pos(HALF_L_TUB - 0.5, PIN_Z) * prof, CHEEK_T)
        bore = bd.Pos(sx * CHEEK_HALF_X, PIN_Y, PIN_Z) * bd.Rot(0, 90, 0) * bd.Cylinder(PIN_CLEAR / 2, CHEEK_T + 1)
        c.append(blk - bore)
    cheek = c[0] + c[1]
    # nyloc boss on the +X cheek outer face; pin bore + cap-head counterbore + press-fit hex pocket are all cut by
    # the pivot fastener's own hole tool, so the geometry and the spec record can never drift apart
    boss = bd.Pos(CHEEK_HALF_X + CHEEK_T / 2, PIN_Y, PIN_Z) * bd.Rot(0, 90, 0) * bd.Cylinder(NUT_BOSS_R, NUT_BOSS_T)
    cut, _rec = hole_tool(at=(-(CHEEK_HALF_X + CHEEK_T / 2), PIN_Y, PIN_Z), axis=(1, 0, 0),
                          fastener=PIN_SCREW, head="cap", into="nut", side="thread", nut_fit="press",
                          nut_entry="radial", nut_offset=2 * CHEEK_HALF_X + CHEEK_T + NUT_BOSS_T)
    return cheek + boss - cut


def tub():
    body = _shell() + _ribs() + _rails() + _bulkhead() + _columns() + _pads() + cheeks() + _esc_shelf() + _switch_pocket()
    return body - _lead_slots() - _column_taps() - _pad_taps() - _notches()
