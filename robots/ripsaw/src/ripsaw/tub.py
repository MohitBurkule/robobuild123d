"""Ripsaw tub: printed nylon unibody (wall ring + rear shelf + motor cradles + front-wall pads + ESC ledge +
battery strap posts), open top and bottom closed by panels. Print orientation: +Z.

The battery lies on the rear shelf between the wheel wells with the rx board on top (one strap over both through
the printed posts); the weapon ESC sits on a printed ledge against the left wall; the weapon plates bolt to the
front-wall pads (M2 from inside, tapped into the plate heels); the panels screw to the side-wall bosses."""
import build123d as bd

from . import params as P
from . import drive, weapon_mount


def _outline(grow=0.0):
    f = bd.Rectangle(P.TUB_W + 2 * grow, P.TUB_BODY_L + 2 * grow)
    return plate_round_corners(f.faces()[0], r_out=P.CORNER_R + grow)


def plate_round_corners(face, r_out):
    from ._reuse import plate as _plate
    return _plate.round_corners(face, r_out=r_out)


def shell():
    outer = bd.extrude(bd.Plane.XY.offset(P.TUB_FLOOR_Z) * _outline(), P.TUB_H)
    inner = bd.extrude(bd.Plane.XY.offset(P.TUB_FLOOR_Z - 1) * _outline(-P.WALL), P.TUB_H + 2)
    return outer - inner


def rear_shelf():
    """Shelf the battery / rx stack lies on and the motor cradle roots in. Main span between the wheel wells
    (the wells only cut |x| > WHEEL_X - W/2 - 1), plus rear wings out to the side walls behind the well band."""
    out = []
    x_in = P.WHEEL_X - P.WHEEL_W / 2 - 1.0          # well cut inner edge
    out.append(bd.Pos(0, (P.TUB_Y0 + P.WALL + P.SHELF_Y1) / 2, P.TUB_FLOOR_Z + P.SHELF_T / 2)
               * bd.Box(2 * x_in, P.SHELF_Y1 - (P.TUB_Y0 + P.WALL), P.SHELF_T))
    x_out = P.TUB_W / 2 - P.WALL + 0.8              # into the side wall
    y_back = P.WHEEL_Y - P.WHEEL_OD / 2 - P.WHEEL_GAP   # behind the well band
    for sx in (1, -1):
        out.append(bd.Pos(sx * (x_in + x_out) / 2, (P.TUB_Y0 + P.WALL + y_back) / 2, P.TUB_FLOOR_Z + P.SHELF_T / 2)
                   * bd.Box(x_out - x_in, y_back - (P.TUB_Y0 + P.WALL), P.SHELF_T))
    return out


def motor_cradle():
    """Walls, capture ribs and axial stops holding both N10s (insert from below with the base panel off,
    resting on the panel's pedestals)."""
    x0, x1 = -(P.WHEEL_X - P.WHEEL_W / 2 - 1.0), P.WHEEL_X - P.WHEEL_W / 2 - 1.0
    cy0, cy1 = P.CRADLE_Y0, P.CRADLE_Y1
    out = []
    for y0, y1 in ((cy0, cy0 + P.CRADLE_WALL_T), (cy1 - P.CRADLE_WALL_T, cy1)):
        out.append(bd.Pos((x0 + x1) / 2, (y0 + y1) / 2, (P.TUB_FLOOR_Z + P.CRADLE_TOP_Z) / 2)
                   * bd.Box(x1 - x0, y1 - y0, P.CRADLE_TOP_Z - P.TUB_FLOOR_Z))
    for bx in (x0 + P.RIB_INSET, 0.0, x1 - P.RIB_INSET):   # capture ribs over the motors: 0.2 gap over the can top
        out.append(bd.Pos(bx, (cy0 + cy1) / 2, P.MOTOR_BRIDGE_Z0 + P.RIB_H / 2)
                   * bd.Box(P.RIB_W, cy1 - cy0, P.RIB_H))
    gb_face = P.WHEEL_X - P.WHEEL_W / 2 - P.DM_L / 2 + P.GB_FACE_OFF   # gearbox front face x (catalogue frame)
    stop_top = P.STOP_Z0 + P.STOP_H
    for sx in (1, -1):
        out.append(bd.Pos(sx * (gb_face + P.MOTOR_STOP_GAP + P.MOTOR_STOP_T / 2), (cy0 + cy1) / 2,
                          (P.TUB_FLOOR_Z + P.SHELF_T + stop_top) / 2)
                   * bd.Box(P.MOTOR_STOP_T, cy1 - cy0, stop_top - (P.TUB_FLOOR_Z + P.SHELF_T)))
    out.append(bd.Pos(0.0, (cy0 + cy1) / 2, (P.TUB_FLOOR_Z + P.SHELF_T + stop_top) / 2)
               * bd.Box(P.CENTRAL_STOP_T, cy1 - cy0, stop_top - (P.TUB_FLOOR_Z + P.SHELF_T)))   # between the can backs
    return out


def front_pads():
    """Pads thickening the front wall band where the weapon plates bolt on: the M2 screws come from inside,
    through the pad clearance hole, into tapped holes in the plate heels."""
    out = []
    for cx in ((P.RAIL_L_X[0] + P.RAIL_L_X[1]) / 2, (P.RAIL_R_X[0] + P.RAIL_R_X[1]) / 2):
        out.append(bd.Pos(cx, P.TUB_Y1 - P.PAD_T / 2, (P.TUB_FLOOR_Z + P.TUB_TOP_Z) / 2)
                   * bd.Box(P.RAIL_L_X[1] - P.RAIL_L_X[0] + 2 * P.WALL + 2.0, P.PAD_T, P.TUB_TOP_Z - P.TUB_FLOOR_Z))
    return out


def side_bosses():
    """Bosses thickening the side walls where the panels screw on (heat-set inserts along Z)."""
    out = []
    for sx in (1, -1):
        for sy in P.PANEL_SCREW_Y:
            out.append(bd.Pos(sx * (P.TUB_W / 2 - P.WALL - P.PANEL_BOSS_T / 2), sy,
                              (P.TUB_FLOOR_Z + P.TUB_TOP_Z) / 2)
                       * bd.Box(P.PANEL_BOSS_T, 2 * (P.INSERT_D / 2 + P.WALL), P.TUB_TOP_Z - P.TUB_FLOOR_Z))
    return out


def esc_ledge():
    """Printed ledge on the left wall the weapon ESC sits on (bottom-face contact for the velcro)."""
    return [bd.Pos((P.ESC_LEDGE_X0 + P.ESC_LEDGE_X1) / 2, (P.ESC_LEDGE_Y0 + P.ESC_LEDGE_Y1) / 2,
                   P.ESC_LEDGE_TOP_Z - P.ESC_LEDGE_Z / 2)
            * bd.Box(P.ESC_LEDGE_X1 - P.ESC_LEDGE_X0, P.ESC_LEDGE_Y1 - P.ESC_LEDGE_Y0, P.ESC_LEDGE_Z)]


def strap_posts():
    """Four posts the battery strap loops through, at the pack's y edges (the strap runs over the pack + rx board)."""
    out = []
    for py in (P.STRAP_POST_Y0, P.STRAP_POST_Y1):
        for sx in (1, -1):
            out.append(bd.Pos(sx * P.STRAP_POST_X, py, P.TUB_FLOOR_Z + P.SHELF_T + P.STRAP_POST_H / 2)
                       * bd.Box(P.STRAP_POST_W, P.STRAP_POST_T, P.STRAP_POST_H))
    return out


def cuts():
    """Disc slot, wheel wells, pedestal slots, plate-screw clearance, cable notch, panel insert bores."""
    out = []
    import math
    sweep_r = P.DISC_R + 1.0                       # weapon sweep + rub clearance at the wall band
    z_half = math.sqrt(sweep_r ** 2 - (P.Y_AX - P.TUB_Y1) ** 2)
    out.append(bd.Pos(0, P.TUB_Y1 - P.WALL / 2, P.Z_AX) *
               bd.Box(2 * P.DISC_SLOT_HALF, P.WALL + 1.4, 2 * z_half))   # disc slot through the front wall band
    out.extend(drive.wells())
    for side in (1, -1):           # one pedestal slot per motor: the base-panel pads rise through the shelf
        mx = side * (P.WHEEL_X - P.WHEEL_W / 2 - P.DM_L / 2)
        out.append(bd.Pos(mx - side * P.PED_SLOT_X_OFF, P.WHEEL_Y, P.PED_SLOT_Z) * bd.Box(P.PED_SLOT_L, P.PED_SLOT_W, P.PED_SLOT_T))
    out.append(bd.Pos(P.NOTCH_X, P.TUB_Y1 - P.PAD_T / 2, P.Z_AX + 1.5)
               * bd.Box(P.NOTCH_W, P.PAD_T + P.NOTCH_EXIT, P.NOTCH_H))   # phase-lead cable notch through the wall band
    for cx in ((P.RAIL_L_X[0] + P.RAIL_L_X[1]) / 2, (P.RAIL_R_X[0] + P.RAIL_R_X[1]) / 2):
        for z in P.PLATE_SCREW_Z:   # plate screw clearance: pad inner face through the wall band, out the far side
            out.append(bd.Pos(cx, P.TUB_Y1 - P.PAD_T / 2, z) * bd.Rot(90, 0, 0)
                       * bd.Cylinder(P.PLATE_SCREW_CLR / 2, P.PAD_T + 1.0))
    for sx in (1, -1):              # panel insert bores in the side-wall bosses (top and bottom)
        for sy in P.PANEL_SCREW_Y:
            for z0 in (P.TUB_FLOOR_Z, P.TUB_TOP_Z - P.INSERT_L):
                out.append(bd.Pos(sx * (P.TUB_W / 2 - P.WALL - P.PANEL_BOSS_T / 2), sy,
                                  z0 + P.INSERT_L / 2) * bd.Cylinder(P.INSERT_D / 2, P.INSERT_L))
    for sx in (1, -1):              # shaft channel through the outboard axial stops: open at the bottom, so the
        gb_face = (P.WHEEL_X - P.WHEEL_W / 2 - P.DM_L / 2) + P.GB_FACE_OFF   # motor + wheel drop out -Z as one unit
        chan_top = P.WHEEL_Z + P.DM_SHAFT["dia"] / 2 + P.STOP_SHAFT_CLR
        out.append(bd.Pos(sx * (gb_face + P.MOTOR_STOP_GAP + P.MOTOR_STOP_T / 2), P.WHEEL_Y,
                          (P.TUB_FLOOR_Z - 1.0 + chan_top) / 2)
                   * bd.Box(P.MOTOR_STOP_T + 2.0, 2 * (P.DM_SHAFT["dia"] / 2 + P.STOP_SHAFT_CLR),
                             chan_top - (P.TUB_FLOOR_Z - 1.0)))
    return out


def tub():
    s = shell()
    for c in (rear_shelf() + motor_cradle() + front_pads() + side_bosses() + esc_ledge() + strap_posts()):
        s = s + c
    for c in cuts():
        s = s - c
    s.label = "tub"
    bd.RigidJoint("origin", s, bd.Location())
    bd.RigidJoint("motor", s, weapon_mount.motor_frame())
    bd.RevoluteJoint("axle", s, axis=bd.Axis((0, P.Y_AX, P.Z_AX), (1, 0, 0)))
    return s
