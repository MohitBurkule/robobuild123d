"""Printed nylon tub: sloped-side disc over the bar + rear drive pod with vertical walls.

Made as: FDM PA12 / PA-CF, printed floor-down (+Z build). The DISC sides slope TUB_SLOPE_DEG inward going up (a
vertical disc or drum hitting the nose glances up and off); the POD walls stay vertical: the boxy N10 gearmotors
sit against them at axle height and a slope would swallow them, and the pod hides behind the weapon sweep anyway.
Weapon motor mount: a printed housing tube rises from the floor round the spinning bell (the floor's centre bore is
the tube's bore, so the motor hangs through the floor with the bar below it), and a boss ring on the tube's top
carries the stator: 4x M2 come down through the top panel and the boss into the stator's base-flange taps, so the
stator is bolted to the tension skin and the motor's own bearings carry the rotor (the shaft extends down through
bar and hub; the M3 nut under the bar clamps the stack up against the bell cap face). A 45-deg slot through the
boss ring (between the tap circle) lets the phase leads turn up out of the pocket over the flange.
Drive cradles: printed pads and side ribs under and beside each N10; the gearbox face bears on the pod wall and
the wheel boss on the shaft clamps the wall between them, so the motors cannot walk inboard.
Panel posts: short printed posts (merged into the disc wall / pod walls) that the top-panel M2 screws bite into;
the wall tops are too thin (1.5 mm) to take a screw directly.
"""
import math

import build123d as bd

from . import params as P


def _slope_inset(h):
    return h * math.tan(math.radians(P.TUB_SLOPE_DEG))


def z0():
    return P.tub_floor_z()


def floor_top():
    return z0() + P.TUB_FLOOR_T


def height():
    return P.TUB_TOP_Z - P.TOP_PANEL_T - z0()


def pod_rear_y():
    """Rear face of the pod (vertical walls, so this is the interior face minus the wall)."""
    return P.wheel_y() - P.POD_REAR


def pod_outline(grow=0.0):
    """The rear pod rectangle: full width at the floor AND at the top (vertical walls)."""
    return bd.Pos(0, (pod_rear_y() + P.WPN_AXIS_Y) / 2) * bd.Rectangle(P.POD_W + 2 * grow, P.WPN_AXIS_Y - pod_rear_y())


def disc_outline(grow=0.0):
    return bd.Pos(0, P.WPN_AXIS_Y) * bd.Circle(P.TUB_R + grow)


def outline(grow=0.0):
    """Plan outline at the floor (widest section), the disc + pod, in world XY."""
    return (disc_outline(grow) + pod_outline(grow)).clean()


def top_outline(grow=0.0):
    """Plan outline at the top: the disc shrunk by the slope inset, the pod at full width (vertical walls)."""
    inset = _slope_inset(height())
    return (bd.Pos(0, P.WPN_AXIS_Y) * bd.Circle(P.TUB_R - inset + grow) + pod_outline(grow)).clean()


def shell():
    """Lofted body: sloped disc + vertical-walled pod, minus the same lofts offset by the wall."""
    h = height()
    lo = bd.Plane.XY.offset(z0())
    hi = bd.Plane.XY.offset(z0() + h)
    outer = bd.loft([lo * outline().faces()[0], hi * top_outline().faces()[0]])
    inner = bd.loft([lo.offset(P.TUB_FLOOR_T) * outline(-P.TUB_WALL).faces()[0],
                     hi.offset(0.01) * top_outline(-P.TUB_WALL).faces()[0]])
    return outer - inner


def motor_housing():
    """Printed tube round the spinning bell: floor to boss, ties the motor mount into the floor. The tube's wall
    overlaps the floor's material (the floor bore IS the tube bore), so it merges with the shell in one solid."""
    return bd.Pos(0, P.WPN_AXIS_Y, z0()) * bd.Cylinder(P.housing_out_r(), P.boss_bottom_z() + 0.6 - z0(),
                                                       align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)) - \
        bd.Pos(0, P.WPN_AXIS_Y, z0() - 1) * bd.Cylinder(P.housing_in_r(), P.boss_bottom_z() + 1.6 - z0(),
                                                        align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def weapon_boss():
    """Ring on the housing top up to the top panel: the stator's M2 screws pass through it into the flange taps.
    Its inner pocket (BOSS_ID_R) leaves the phase leads a channel over the flange face; the 45-deg slot lets them
    turn out (between the tap circle)."""
    top = P.TUB_TOP_Z - P.TOP_PANEL_T
    z = P.boss_bottom_z()
    boss = bd.Pos(0, P.WPN_AXIS_Y, z) * bd.Cylinder(P.BOSS_OD_R, top - z,
                                                    align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)) - \
        bd.Pos(0, P.WPN_AXIS_Y, z - 1) * bd.Cylinder(P.BOSS_ID_R, top - z + 2,
                                                     align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    for k in range(4):
        a = math.radians(90.0 * k)
        boss -= bd.Pos(P.BL_SCREW_PCD / 2 * math.cos(a), P.WPN_AXIS_Y + P.BL_SCREW_PCD / 2 * math.sin(a), z) * bd.Cylinder(
            1.1, top - z + 1, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    r_mid = (P.BOSS_ID_R - 1.0 + P.BOSS_OD_R + 2.0) / 2
    slot = bd.Pos(r_mid * math.cos(math.radians(45.0)), P.WPN_AXIS_Y + r_mid * math.sin(math.radians(45.0)), z - 0.2) * bd.Rot(
        0, 0, 45.0) * bd.Box(P.BOSS_OD_R + 2.0 - (P.BOSS_ID_R - 1.0), P.WIRE_SLOT_W, top - z + 1.2,
                             align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    return boss - slot


def motor_bore():
    """The motor hangs through the floor: the bore clears the spinning bell (bore = the housing tube's bore)."""
    return bd.Pos(0, P.WPN_AXIS_Y, z0() - 1) * bd.Cylinder(P.housing_in_r(), P.TUB_FLOOR_T + 2,
                                                           align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def lock_holes():
    """The weapon-lock pin drops through the floor (and the panel, drilled there) into the bar's lock hole; its tip
    rests on the floor slab, so the bar cannot turn past it. Made safe outside the robot."""
    return bd.Pos(P.BAR_LOCK_X, P.WPN_AXIS_Y, z0() - 1) * bd.Cylinder(P.BAR_LOCK_D / 2 + 0.2, P.TUB_FLOOR_T + 2,
                                                                      align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def axle_holes():
    """N10 output shaft exits through the pod walls; one side built, mirrored."""
    one = bd.Pos(P.POD_W / 2, P.wheel_y(), P.WHEEL_CZ) * bd.Rot(0, 90, 0) * bd.Cylinder(2.0, 2 * P.TUB_WALL + 2)
    return one + bd.mirror(one, bd.Plane.YZ)


def _cradle(side):
    """Pad + front/rear ribs locating one N10 body against the pod wall (side +1 right, -1 left)."""
    x_in = abs(P.POD_W / 2 - P.TUB_WALL + P.N10_BODY_IN)
    x_out = P.POD_W / 2 - P.TUB_WALL
    lo, hi = sorted((side * x_in, side * x_out))
    floor = floor_top()
    pad = bd.Pos((lo + hi) / 2, P.wheel_y(), floor - 0.5) * bd.Box(hi - lo, 2 * (P.N10_HALF_Y - P.CRADLE_CLR),
                                                                  P.CRADLE_PAD_TOP - floor + 0.5,
                                                                  align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    for sgn in (-1, 1):
        pad += bd.Pos((lo + hi) / 2, P.wheel_y() + sgn * (P.N10_HALF_Y + P.CRADLE_CLR + P.CRADLE_RIB_T / 2), floor - 0.5) * bd.Box(
            hi - lo, P.CRADLE_RIB_T, P.CRADLE_RIB_H - floor + 0.5, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    return pad


def disc_post_angles():
    """Angles on the disc rim wall that are not swallowed by the pod rectangle.
    # param: organic four-way symmetry of the disc rim: the angles dodge the pod seam and the slope's high points."""
    return [40.0, 75.0, 105.0, 140.0]


def post_xy():
    """World (x, y) of every panel-screw post: 4 on the disc rim wall + 2 on each pod wall."""
    inset = _slope_inset(height())
    r = P.TUB_R - inset - P.DISC_POST_IN
    pts = [(r * math.cos(math.radians(a)), P.WPN_AXIS_Y + r * math.sin(math.radians(a))) for a in disc_post_angles()]
    for dy in P.POD_POST_Y:
        y = P.wheel_y() + dy
        pts.append((P.POD_W / 2 - P.TUB_WALL - P.POST_R / 2, y))
        pts.append((-(P.POD_W / 2 - P.TUB_WALL - P.POST_R / 2), y))
    return pts


def posts():
    """Short printed posts the panel screws thread into (merged with the walls)."""
    out = None
    for x, y in post_xy():
        p = bd.Pos(x, y, P.POST_Z0) * bd.Cylinder(P.POST_R, P.TUB_TOP_Z - P.TOP_PANEL_T - P.POST_Z0,
                                                  align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        out = p if out is None else out + p
    return out


def tub():
    return (shell() + motor_housing() + weapon_boss() + posts() + _cradle(1) + _cradle(-1)
            - motor_bore() - lock_holes() - axle_holes())
