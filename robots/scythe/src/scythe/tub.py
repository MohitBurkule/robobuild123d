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
    Its bore (BOSS_ID_R) is the MR83ZZ press seat (the bearing sits directly on the flange face)."""
    top = P.TUB_TOP_Z - P.TOP_PANEL_T
    z = P.boss_bottom_z()
    boss = bd.Pos(0, P.WPN_AXIS_Y, z) * bd.Cylinder(P.BOSS_OD_R, top - z,
                                                    align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)) - \
        bd.Pos(0, P.WPN_AXIS_Y, z - 1) * bd.Cylinder(P.BOSS_ID_R, top - z + 2,
                                                     align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    for a in P.SCREW_ANGLES:
        r = math.radians(a)
        boss -= bd.Pos(P.BL_SCREW_PCD / 2 * math.cos(r), P.WPN_AXIS_Y + P.BL_SCREW_PCD / 2 * math.sin(r), z) * bd.Cylinder(
            P.BL_SCREW_CLR_R, top - z + 1, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    return boss


def wire_slot():
    """The SLOT_ANGLE_DEG phase-lead channel, cut from the whole tub, in two steps: (1) an internal channel down the
    housing-tube wall (WIRE_SLOT_TUBE_Z0 up to the boss), outer radius just past the tube wall so it stays inside the
    disc wall - this is how the phase wire gets from the pod-side annulus into the tube's wall; (2) the boss notch from
    inside the bore out past the disc wall (WIRE_SLOT_OUT_R), between the flange tap circle - the phase leads turn up
    out of the pocket over the flange face and leave the boss sideways through this wall notch."""
    top = P.TUB_TOP_Z - P.TOP_PANEL_T
    z = P.boss_bottom_z()
    a = math.radians(P.SLOT_ANGLE_DEG)
    r_out = P.WIRE_SLOT_OUT_R
    r_mid = (P.WIRE_SLOT_IN_R + r_out) / 2
    boss_notch = bd.Pos(r_mid * math.cos(a), P.WPN_AXIS_Y + r_mid * math.sin(a), z - 0.2) * bd.Rot(
        0, 0, P.SLOT_ANGLE_DEG) * bd.Box(r_out - P.WIRE_SLOT_IN_R, P.WIRE_SLOT_W, top - z + 1.2,
                                         align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    r_tube_out = P.housing_out_r() + 0.2
    r_mid2 = (P.WIRE_SLOT_IN_R + r_tube_out) / 2
    tube_channel = bd.Pos(r_mid2 * math.cos(a), P.WPN_AXIS_Y + r_mid2 * math.sin(a), P.WIRE_SLOT_TUBE_Z0) * bd.Rot(
        0, 0, P.SLOT_ANGLE_DEG) * bd.Box(r_tube_out - P.WIRE_SLOT_IN_R, P.WIRE_SLOT_W, z + 0.7 - P.WIRE_SLOT_TUBE_Z0,
                                         align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    slot = boss_notch + tube_channel
    # the same channel at the other three diagonals (between the flange taps, symmetric): the motor-relief sector
    # edges land inside these cuts, so no bare wall strip is left between the two cuts
    out = slot
    for k in (1, 2, 3):
        out = out + bd.Pos(0, P.WPN_AXIS_Y, 0) * bd.Rot(0, 0, 90 * k) * slot
    return out


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
    """N10 output shaft exits through the pod walls; one side built, mirrored. The hole is a U-slot open at the top
    of the wall, so the gearmotor drops into its cradle from above (shaft entering the slot) and lifts back out."""
    one = bd.Pos(P.POD_W / 2, P.wheel_y(), P.WHEEL_CZ) * bd.Rot(0, 90, 0) * bd.Cylinder(2.0, 2 * P.TUB_WALL + 2)
    slot = bd.Pos(P.POD_W / 2, P.wheel_y(), P.WHEEL_CZ) * bd.Box(
        2 * P.TUB_WALL + 2, 4.1, P.TUB_TOP_Z - P.WHEEL_CZ, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    return one + slot + bd.mirror(one + slot, bd.Plane.YZ)


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
    return [20.0, 75.0, 105.0, 140.0]
    # param: end


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


def skid_pads():
    """Rear skid pads printed with the tub (one solid), behind the weapon sweep: the rear corners of the stance
    polygon - with the wheels alone the COM at rest sits outside the wheel contact hull. The pads bottom at
    SKID_PAD_Z0 so the wheels, not the pads, carry the robot on the floor."""
    y = pod_rear_y() + P.TUB_WALL + P.SKID_PAD_BAY
    out = None
    for sx in (-P.SKID_PAD_X, P.SKID_PAD_X):
        p = bd.Pos(sx, y, P.SKID_PAD_Z0) * bd.Cylinder(P.SKID_PAD_R, P.tub_floor_z() + 0.2 - P.SKID_PAD_Z0,
                                                         align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        out = p if out is None else out + p
    return out


def _motor_clearance(side):
    """Annular-sector relief in the housing-tube wall and boss ring for one N10 body's inboard corner (side +1
    faces +X), up to the boss top so the motor lifts straight out +z. The sector's inner arc sits just inside the
    housing bore and its outer arc is the tube wall / boss OD, so the cut merges into the bore on one side and
    opens the wall square on the other - no straight box edge grazing the bore circle, which would leave a
    sub-0.1 mm feather (mfg.thin_wall). Cradle ribs (r > 21), the pod walls and the disc wall are all outside the
    sector radii."""
    a0 = 0.0 if side > 0 else 180.0
    half = 51.0   # sector edges (at +-51 deg, 129/231) land inside the diagonal wire-slot cuts, so no bare wall strip is left between relief and slot
    z0 = P.CRADLE_PAD_TOP
    r_out1 = P.housing_out_r() + 0.02
    r_in1 = P.housing_in_r() - 0.5
    r_in2 = 11.0
    r_out2 = P.BOSS_OD_R + 0.02
    out = None
    for za, zb, ri, ro in ((z0, P.boss_bottom_z() + 0.6, r_in1, r_out1),
                           (P.boss_bottom_z(), P.boss_bottom_z() + P.BOSS_T + 0.2, r_in2, r_out2)):
        ring = bd.Pos(0, P.WPN_AXIS_Y, za) * (
            bd.Cylinder(ro, zb - za, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
            - bd.Cylinder(ri, zb - za + 2, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)))
        # wedge box sized so its corners sit on the ring's outer arc at +-half (no poke inside the ring):
        # cut edge lands at a0 +- half on the tube wall, inside the diagonal wire-slot cuts
        x0 = ro * math.cos(math.radians(half))
        x1 = ro + 0.5
        y1 = ro * math.sin(math.radians(half)) + 0.5
        wedge = (bd.Pos(0, P.WPN_AXIS_Y, za) * bd.Rot(0, 0, a0) * bd.Pos((x0 + x1) / 2, 0, 0)
                 * bd.Box(x1 - x0, 2 * y1, zb - za, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)))
        sec = ring & wedge
        out = sec if out is None else out + sec
    return out


def tub():
    return (shell() + motor_housing() + weapon_boss() + posts() + _cradle(1) + _cradle(-1) + skid_pads()
            - motor_bore() - lock_holes() - axle_holes() - wire_slot()
            - _motor_clearance(1) - _motor_clearance(-1))
