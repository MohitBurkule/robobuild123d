"""Ripsaw tub: printed nylon unibody (wall ring + rear shelf + motor cradles + front-wall pads), open top and bottom
closed by panels. Print orientation: +Z.

The battery lies on the rear shelf behind the N10 cradles; the ESCs sit high on the walls; the weapon plates bolt to
the front-wall pads (heat-set inserts along Y); the panels screw to the side-wall bosses."""
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
    """Shelf the battery sits on and the motor cradle roots in. Main span between the wheel wells (the wells only
    cut |x| > 28.4), plus rear wings out to the side walls behind the well band, so it fuses with the tub everywhere."""
    out = []
    out.append(bd.Pos(0, (P.TUB_Y0 + P.WALL + P.SHELF_Y1) / 2, P.TUB_FLOOR_Z + P.SHELF_T / 2)
               * bd.Box(2 * (P.WHEEL_X - P.WHEEL_W / 2 - 1.0), P.SHELF_Y1 - (P.TUB_Y0 + P.WALL), P.SHELF_T))
    x_in = P.WHEEL_X - P.WHEEL_W / 2 - 1.0          # well cut inner edge
    x_out = P.TUB_W / 2 - P.WALL + 0.8              # into the side wall
    y_back = P.WHEEL_Y - P.WHEEL_OD / 2 - P.WHEEL_GAP   # behind the well band
    for sx in (1, -1):
        out.append(bd.Pos(sx * (x_in + x_out) / 2, (P.TUB_Y0 + P.WALL + y_back) / 2, P.TUB_FLOOR_Z + P.SHELF_T / 2)
                   * bd.Box(x_out - x_in, y_back - (P.TUB_Y0 + P.WALL), P.SHELF_T))
    return out


def motor_cradle():
    """Walls, bridge ribs and axial stops capturing both N10s (insert from below with the base panel off)."""
    x0, x1 = -(P.WHEEL_X - P.WHEEL_W / 2 - 1.0), P.WHEEL_X - P.WHEEL_W / 2 - 1.0
    out = []
    for y0, y1 in ((P.CRADLE_Y0, P.CRADLE_Y0 + P.CRADLE_WALL_T), (P.CRADLE_Y1 - P.CRADLE_WALL_T, P.CRADLE_Y1)):
        out.append(bd.Pos((x0 + x1) / 2, (y0 + y1) / 2, (P.TUB_FLOOR_Z + P.CRADLE_TOP_Z) / 2)
                   * bd.Box(x1 - x0, y1 - y0, P.CRADLE_TOP_Z - P.TUB_FLOOR_Z))
    for bx in (x0 + 8.0, 0.0, x1 - 8.0):   # bridge ribs over the motors: 0.2 capture gap
        out.append(bd.Pos(bx, (P.CRADLE_Y0 + P.CRADLE_Y1) / 2, (P.MOTOR_BRIDGE_Z0 + P.CRADLE_TOP_Z) / 2)
                   * bd.Box(4.0, P.CRADLE_Y1 - P.CRADLE_Y0, P.CRADLE_TOP_Z - P.MOTOR_BRIDGE_Z0))
    gb_face = (P.WHEEL_X - P.WHEEL_W / 2 - P.DM_L / 2) + 11.25   # gearbox front face x (catalogue bbox)
    for sx in (1, -1):
        out.append(bd.Pos(sx * (gb_face + P.MOTOR_STOP_T / 2), (P.CRADLE_Y0 + P.CRADLE_Y1) / 2, 15.0)
                   * bd.Box(P.MOTOR_STOP_T, P.CRADLE_Y1 - P.CRADLE_Y0, 10.0))
    out.append(bd.Pos(0.0, (P.CRADLE_Y0 + P.CRADLE_Y1) / 2, 15.0)
               * bd.Box(0.3, P.CRADLE_Y1 - P.CRADLE_Y0, 10.0))   # central stop between the two can backs
    return out


def front_pads():
    """Pads thickening the front wall where the weapon plates bolt on (heat-set inserts along Y)."""
    out = []
    for cx in ((P.RAIL_L_X[0] + P.RAIL_L_X[1]) / 2, (P.RAIL_R_X[0] + P.RAIL_R_X[1]) / 2):
        out.append(bd.Pos(cx, P.TUB_Y1 - P.WALL - P.PAD_T / 2, (P.TUB_FLOOR_Z + P.TUB_TOP_Z) / 2)
                   * bd.Box(P.RAIL_L_X[1] - P.RAIL_L_X[0] + 2 * P.WALL + 2.0, P.PAD_T, P.TUB_TOP_Z - P.TUB_FLOOR_Z))
    return out


def side_bosses():
    """Bosses thickening the side walls where the panels screw on (heat-set inserts along Z)."""
    out = []
    for sx in (1, -1):
        for sy in (1, -1):
            out.append(bd.Pos(sx * (P.TUB_W / 2 - P.WALL - P.PANEL_BOSS_T / 2), sy * P.PANEL_SCREW_Y,
                              (P.TUB_FLOOR_Z + P.TUB_TOP_Z) / 2)
                       * bd.Box(P.PANEL_BOSS_T, 2 * (P.INSERT_D / 2 + P.WALL), P.TUB_TOP_Z - P.TUB_FLOOR_Z))
    return out


def cuts():
    """Disc slot through the front wall, wheel wells, insert bores, plate-screw clearance through the wall."""
    out = []
    out.append(bd.Pos(0, P.Y_AX, P.Z_AX) * bd.Rot(0, 90, 0) *
               bd.Cylinder(P.DISC_R + 4 * P.MOVING_CLR, P.DISC_T + 2 * P.MOVING_CLR))   # disc slot through the tub
    out.extend(drive.wells())
    for cx in ((P.RAIL_L_X[0] + P.RAIL_L_X[1]) / 2, (P.RAIL_R_X[0] + P.RAIL_R_X[1]) / 2):
        for z in P.PLATE_SCREW_Z:   # plate screw clearance through the wall into the pad inserts
            out.append(bd.Pos(cx, P.TUB_Y1, z) * bd.Rot(90, 0, 0) * bd.Cylinder(P.PLATE_SCREW_CLR / 2, P.WALL * 3))
    for side in (1, -1):           # pedestal slots through the cradle root strip (the base-panel pads rise in)
        mx = side * (P.WHEEL_X - P.WHEEL_W / 2 - P.DM_L / 2)
        out.append(bd.Pos(mx - 5.25, P.WHEEL_Y, 4.25) * bd.Box(11.0, 11.0, 3.5))   # under the can pad
        out.append(bd.Pos(mx + 6.75, P.WHEEL_Y, 4.25) * bd.Box(9.0, 11.0, 3.5))    # under the gearbox pad
    out.append(bd.Pos(-14.5, P.TUB_Y1 - 1.0, 26.0) * bd.Box(4.2, 3.0, 3.0))   # phase-lead cable notch, wall top (left pad)
    for sx in (1, -1):              # panel insert bores in the side-wall bosses (top and bottom)
        for sy in (1, -1):
            for z0 in (P.TUB_FLOOR_Z, P.TUB_TOP_Z - P.INSERT_L):
                out.append(bd.Pos(sx * (P.TUB_W / 2 - P.WALL - P.PANEL_BOSS_T / 2), sy * P.PANEL_SCREW_Y,
                                  z0 + P.INSERT_L / 2) * bd.Cylinder(P.INSERT_D / 2, P.INSERT_L))
    for cx in ((P.RAIL_L_X[0] + P.RAIL_L_X[1]) / 2, (P.RAIL_R_X[0] + P.RAIL_R_X[1]) / 2):
        for z in P.PLATE_SCREW_Z:   # pad insert bores (mouth at the wall outer face)
            out.append(bd.Pos(cx, P.TUB_Y1 - P.WALL - P.PAD_T + P.INSERT_L / 2, z)
                       * bd.Rot(90, 0, 0) * bd.Cylinder(P.INSERT_D / 2, P.INSERT_L))
    return out


def tub():
    s = shell()
    for c in rear_shelf() + motor_cradle() + front_pads() + side_bosses():
        s = s + c
    for c in cuts():
        s = s - c
    s.label = "tub"
    bd.RigidJoint("origin", s, bd.Location())
    bd.RigidJoint("motor", s, weapon_mount.motor_frame())
    bd.RevoluteJoint("axle", s, axis=bd.Axis((0, P.Y_AX, P.Z_AX), (1, 0, 0)))
    return s
