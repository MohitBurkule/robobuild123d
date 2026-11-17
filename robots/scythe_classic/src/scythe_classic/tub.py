"""Printed nylon tub: a sloped-side cone over the bar, with a vertical-walled rear pod that carries the N10s.

Made as: FDM nylon, printed floor-down (+Z build). The cone (round, tapering up) is the old Scythe look; its walls
slope TUB_SLOPE_DEG inward going up so a vertical hit glances off. The rear pod is a rectangular arm behind the disc
that carries the two N10 drive motors, battery, ESC, receiver and switch. Its walls are vertical: a motor body at
the wheel height sits inside the walls, and a sloped wall there would cut through it.
Weapon boss: a ring from the floor to the top panel round the bell, with the stator's base screw holes (catalogue
base_holes, weapon_motor.describe). The screws take the stator into the top panel, so a bar hit's torque goes
stator -> boss -> top panel and walls (the top panel is the tension skin).
"""
import math

import build123d as bd

from . import params as P
from ._reuse import hw, weapon_motor


POD_FRONT_PROUD = 1.9   # mm the pod's front corners stand outside the cone's base circle
SKIRT_INSET = 1.0   # mm the base circle sits inside TUB_R: gives the pod front corners an edge long enough to take the fillet
SLOPE_STEPS = 6   # ruled-loft sections up the sloped wall (each step turns the wall by well under the 45 deg sharp-corner threshold)
JOINT_R = 1.2   # mm inside radius where the pod front face meets the cone (outside) and at the top panel plan
CAVITY_EXTRA = 6.0   # mm the offset body is taller than the tub
SKIRT_H = 2.0   # mm vertical band at the cone base: a sloped wall running into the floor underside leaves a knife edge
TOP_BAND_H = 2.0   # mm vertical band at the cone top: the sloped wall meeting the flat rim face leaves an acute inside corner


def _slope_inset(h):
    """Radial inset of the cone at height h above the floor underside: the slope runs between the vertical skirt and the
    vertical top band, and stays constant in the bands."""
    run = min(h, height() - TOP_BAND_H) - SKIRT_H
    return max(run, 0.0) * math.tan(math.radians(P.TUB_SLOPE_DEG))


def z0():
    return P.tub_floor_z()


def height():
    return P.TUB_TOP_Z - P.TOP_PANEL_T - z0()


def pod_front_y():
    """Y of the pod's front face: its outer corners stand POD_FRONT_PROUD outside the disc's circle, so the face runs the full height
and meets the cone in one clean concave edge (corners exactly on the circle make that edge start at a point)."""
    return P.WPN_AXIS_Y - math.sqrt(P.TUB_R ** 2 - (P.POD_W / 2) ** 2) - POD_FRONT_PROUD


def pod_rear_y():
    """Rear edge: POD_L behind the wheel axle line."""
    return P.wheel_y() - P.POD_L / 2


def pod_len():
    return pod_front_y() - pod_rear_y()


def pod_cy():
    return (pod_front_y() + pod_rear_y()) / 2


def disc_face(grow=0.0):
    """Cone plan outline (circle) at the floor, grown or shrunk by `grow`, on the weapon axis."""
    return bd.Pos(0, P.WPN_AXIS_Y) * bd.Circle(P.TUB_R + grow)


def pod_box(grow=0.0, z_lo=0.0, h=None):
    """Vertical rear pod prism, grown or shrunk on all four sides by `grow`."""
    h = height() if h is None else h
    return bd.Pos(0, pod_cy(), z_lo) * bd.Box(P.POD_W + 2 * grow, pod_len() + 2 * grow, h,
                                              align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def top_outline(inset):
    """Plan outline at a given inset: the cone's circle shrunk by `inset`, joined to the pod's full-width rectangle, with the
    two concave corners where the pod front meets the circle rounded (JOINT_R)."""
    disc = bd.Pos(0, P.WPN_AXIS_Y) * bd.Circle(P.TUB_R - inset)
    pod = bd.Pos(0, pod_cy()) * bd.Rectangle(P.POD_W, pod_len())
    outline = (disc + pod).clean()
    corners = [v for v in outline.vertices() if abs(v.Y - pod_front_y()) < 0.05 and abs(v.X) < P.POD_W / 2 - 1.0]
    return bd.fillet(corners, JOINT_R)


def cone_loft(grow_lo, grow_hi, z_lo, z_hi):
    """Sloped cone solid: the circle grown by grow_lo at z_lo, grown by grow_hi at z_hi (the slope sets grow_hi)."""
    lo = bd.Plane.XY.offset(z_lo)
    hi = bd.Plane.XY.offset(z_hi)
    return bd.loft([lo * disc_face(grow_lo).faces()[0], hi * disc_face(grow_hi).faces()[0]])


def _levels(extra=0.0):
    """[(z, inset)] plan sections of the outer wall: vertical skirt, SLOPE_STEPS up the sloped wall, vertical top band (taller by
    `extra`)."""
    h = height() + extra
    z_cone_top = z0() + height() - TOP_BAND_H
    z_skirt = z0() + SKIRT_H
    top_inset = _slope_inset(height())
    levels = [(z0(), SKIRT_INSET), (z_skirt, SKIRT_INSET)]
    for i in range(1, SLOPE_STEPS + 1):
        levels.append((z_skirt + (z_cone_top - z_skirt) * i / SLOPE_STEPS, SKIRT_INSET + (top_inset - SKIRT_INSET) * i / SLOPE_STEPS))
    levels.append((z0() + h, top_inset))
    return levels


def _stack(sections):
    """Ruled lofts between successive plan faces (z-placed), fused."""
    body = None
    for a, b in zip(sections, sections[1:]):
        seg = bd.loft([a, b], ruled=True)
        body = seg if body is None else body + seg
    return body.clean()


def outer_body(extra=0.0):
    """The solid tub outside: a stack of ruled lofts between plan outlines (disc + pod, joint corners rounded) up a vertical
    skirt, the sloped wall and a vertical top band. `extra` makes it taller."""
    return _stack([bd.Plane.XY.offset(z) * top_outline(inset).faces()[0] for z, inset in _levels(extra)])


def _inset_at(levels, z):
    """Plan inset of the outer wall at height z (linear between the loft sections)."""
    for (za, ia), (zb, ib) in zip(levels, levels[1:]):
        if za - 1e-9 <= z <= zb + 1e-9:
            return ia if zb == za else ia + (ib - ia) * (z - za) / (zb - za)
    return levels[-1][1]


def cavity():
    """What is hollowed out: the same stack of plan outlines, each offset inward by the wall (taken square to the sloped wall, so
    the wall is the same thickness everywhere), from the floor up and out through the open top (the top panel closes it). The floor
    edge is rounded (FILLET_R) by three ruled steps of a quarter circle. Built from the sections, not by offsetting the solid: an
    offset of the faceted solid leaves sliver faces."""
    slope = math.radians(P.TUB_SLOPE_DEG)
    levels = _levels(CAVITY_EXTRA)
    z_floor = z0() + P.TUB_FLOOR_T
    r = FILLET_R
    secs = []   # (z, inset, wall offset)
    for deg in (0, 30, 60, 90):
        a = math.radians(deg)
        z = z_floor + r * (1 - math.cos(a))
        secs.append((z, _inset_at(levels, z), P.TUB_WALL + r * (1 - math.sin(a))))
    for k, (z, inset) in enumerate(levels):
        if z > z_floor + r + 1e-6:
            sloped = z0() + SKIRT_H + 1e-6 < z <= z0() + height() - TOP_BAND_H + 1e-6
            secs.append((z, inset, P.TUB_WALL / (math.cos(slope) if sloped else 1.0)))
    faces = [bd.Plane.XY.offset(z) * bd.offset(top_outline(inset).faces()[0], amount=-w, kind=bd.Kind.ARC).faces()[0] for z, inset, w in secs]
    return _stack(faces)


def shell():
    return outer_body() - cavity()


def weapon_boss():
    """Printed ring from the floor to the top panel: the stator's base screws go down through it. Its inner wall is
    the bell clearance, and the motor solid is cut out so the cross base and stator sit clear of it."""
    m = weapon_motor.describe(P.WEAPON_MOTOR)
    top = P.TUB_TOP_Z - P.TOP_PANEL_T
    z_lo = z0() + P.TUB_FLOOR_T
    r_out = max(r for r, _, _ in m["base_holes"]) + 2 * P.TUB_WALL
    r_in = m["bell_r"] + P.MOTOR_BELL_CLR
    ring = bd.Pos(0, P.WPN_AXIS_Y, z_lo) * (bd.Cylinder(r_out, top - z_lo, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
                                           - bd.Cylinder(r_in, top - z_lo, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)))
    for r, deg, d in m["base_holes"]:
        ring -= bd.Pos(r * math.cos(math.radians(deg)), P.WPN_AXIS_Y + r * math.sin(math.radians(deg)), z_lo) * bd.Cylinder(
            d / 2, top - z_lo, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    return ring - weapon_motor_placed()


def weapon_motor_placed():
    """The weapon motor solid at its assembly pose (shaft down), as the assembly places it."""
    return hw.placed(P.WEAPON_MOTOR, (0.0, P.WPN_AXIS_Y, P.wpn_motor_z()), (0.0, 90.0, 0.0))


def bell_bore():
    m = weapon_motor.describe(P.WEAPON_MOTOR)
    return bd.Pos(0, P.WPN_AXIS_Y, z0() - 1) * bd.Cylinder(m["bell_r"] + P.MOTOR_BELL_CLR, P.TUB_FLOOR_T + 2,
                                                          align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


RING_LEN = 1.8      # mm the axle ring stands off the pod wall: its end stays 0.5 mm clear of the tyre's inboard face (the wheel's swept band)
GUARD_W = 2.4       # mm (y) of the wheel-guard post at each rear pod corner
RING_OUT_R = 6.0    # mm axle ring outer radius
RING_BORE_R = P.WHEEL_HUB_R + 0.2   # mm the wheel hub boss turns in the ring bore (0.2 running clearance)
AXLE_SLOT_R = 2.3   # mm half width of the axle slot (shaft collar 2 mm radius, shaft 1.5 mm)
RIB_T = 1.2         # mm cradle rib thickness (nozzle multiple)
RIB_GAP = 0.45       # mm print clearance between the N10 flats and the ribs
PAD_GAP = 0.45       # mm between the motor shaft-side face and the pad that stops it
STOP_W = 2.4        # mm the rear stops reach in from each rib (they leave the solder-tab corridor free)
MOTOR_HALF_W = 6.0  # mm half width of the N10 body (catalogue box 9 x 12 x 10)
MOTOR_HALF_H = 5.0  # mm half height of the N10 body


FILLET_R = 1.0   # mm minimum inside radius on printed concave corners (mfg.sharp_internal_corner)
CORNER_R = 1.5   # mm radius of the cradle's vertical concave corners (larger than the base fillet, or the two blends degenerate to a point)
SLAB_MARGIN = 2.0   # mm the cradle's base slab runs out beyond the cradle outline: room for the base fillet


def _concave_vertices(face):
    """Vertices of a plan face whose interior angle is reflex (more than half the surrounding disc is inside the face)."""
    out = []
    for v in face.vertices():
        n = 0
        for k in range(8):
            a = math.radians(22.5 + 45 * k)
            q = bd.Vector(v.X + 0.05 * math.cos(a), v.Y + 0.05 * math.sin(a), 0)
            n += face.is_inside(q)
        if n > 4:
            out.append(v)
    return out


def cradle():
    """Per side: the N10's cradle, one printed piece with its base fillets. Two ribs along the motor, a pad in front of its
    shaft-side face (it stops the motor in x) and a rear stop on each rib (not across the middle: the solder tabs and their wires
    leave there). The motor drops in from the top, panel off. Made as a plan outline (concave corners rounded) standing on a slab
    the thickness of the floor, so the base edges take a fillet; the slab is cut back to just inside the pod's walls (0.4 mm into them)."""
    z_lo = z0() + P.TUB_FLOOR_T
    z_hi = P.WHEEL_CZ + MOTOR_HALF_H
    wall_i = P.POD_W / 2 - P.TUB_WALL
    face = P.motor_x() + P.DRIVE_MOTOR_FACE_X          # motor shaft-side face
    rear = P.motor_x() + P.DRIVE_MOTOR_REAR_X          # motor rear face (solder tabs)
    y0 = P.wheel_y()
    half = MOTOR_HALF_W + RIB_GAP + RIB_T
    rect = lambda x0, x1, y_a, y_b: bd.Pos((x0 + x1) / 2, (y_a + y_b) / 2) * bd.Rectangle(x1 - x0, y_b - y_a)
    plan = rect(face + PAD_GAP, wall_i + 0.2, y0 - half, y0 + half)                       # pad
    for sy in (1, -1):
        a, b = sorted((y0 + sy * (MOTOR_HALF_W + RIB_GAP), y0 + sy * half))
        plan += rect(rear - PAD_GAP - RIB_T, face + PAD_GAP, a, b)                          # rib
        a2, b2 = sorted((y0 + sy * (MOTOR_HALF_W + RIB_GAP), y0 + sy * (MOTOR_HALF_W + RIB_GAP - STOP_W)))
        plan += rect(rear - PAD_GAP - RIB_T, rear - PAD_GAP, a2, b2)                         # rear stop
    plan = plan.clean()
    plan = bd.fillet(_concave_vertices(plan.faces()[0]), CORNER_R)
    stand = bd.Pos(0, 0, z_lo) * bd.extrude(plan.faces()[0], z_hi - z_lo)
    slab_face = bd.offset(plan.faces()[0], amount=SLAB_MARGIN, kind=bd.Kind.ARC).faces()[0]
    slab = bd.Pos(0, 0, z0()) * bd.extrude(slab_face, P.TUB_FLOOR_T)
    slab = slab & (bd.Pos(0, pod_cy(), z0()) * bd.Box(2 * wall_i + 0.8, pod_len() - 2 * P.TUB_WALL + 0.8, P.TUB_FLOOR_T, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)))
    body = stand + slab
    edges = [e for e in body.edges() if e.center().X < wall_i - 0.01 and abs(e.bounding_box().min.Z - z_lo) < 1e-3 and abs(e.bounding_box().max.Z - z_lo) < 1e-3
             and min(e.distance_to(bd.Pos(0, 0, z_lo) * w) for w in plan.faces()[0].wires()) < 1e-3]
    return bd.fillet(edges, FILLET_R)


def drive_bays():
    """Per side: the N10's cradle (see cradle) and the wheel's axle ring.
    Axle ring: stands off the wall's outer face round the wheel hub boss; its end holds the shaft's 3 mm grip inside the chassis
    hull (contain.electronics_exposed) and its lips keep the wheel and motor from lifting out. A slot, open at the top, takes
    the shaft up and out when the motor is lifted (the wheel leaves sideways first). A post at the rear pod corner carries the
    hull out over the shaft tip."""
    wall_o = P.POD_W / 2
    y0 = P.wheel_y()
    box = lambda x0, x1, y_a, y_b, z_a, z_b: bd.Pos((x0 + x1) / 2, (y_a + y_b) / 2, z_a) * bd.Box(
        x1 - x0, y_b - y_a, z_b - z_a, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    out = cradle()
    out += bd.Pos(wall_o - 0.2, y0, P.WHEEL_CZ) * bd.Rot(0, 90, 0) * bd.Cylinder(RING_OUT_R, RING_LEN + 0.2, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    out += box(wall_o - 0.4, wall_o + RING_LEN, pod_rear_y(), pod_rear_y() + GUARD_W, z0(), z0() + height())
    return out + bd.mirror(out, bd.Plane.YZ)


def axle_holes():
    """What the axle cuts: the bore for the wheel hub boss in each ring, and the shaft slot (2.3 mm radius at the axle line and
    straight up out of the top) through the ring, the pod wall and the pad. The shaft leaves through the slot, so the motor
    lifts out; the hub boss is wider than the slot, so the ring lips keep the wheel from lifting."""
    z_top = z0() + height() + CAVITY_EXTRA
    wall_o = P.POD_W / 2
    x_a = P.motor_x() + P.DRIVE_MOTOR_FACE_X
    x_b = wall_o + RING_LEN + 1.0
    cyl = lambda r, xa, xb: bd.Pos(xa, P.wheel_y(), P.WHEEL_CZ) * bd.Rot(0, 90, 0) * bd.Cylinder(r, xb - xa, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    one = cyl(AXLE_SLOT_R, x_a, x_b) + cyl(RING_BORE_R, wall_o, x_b)
    one += bd.Pos((x_a + x_b) / 2, P.wheel_y(), (P.WHEEL_CZ + z_top) / 2) * bd.Box(x_b - x_a, 2 * AXLE_SLOT_R, z_top - P.WHEEL_CZ)
    return one + bd.mirror(one, bd.Plane.YZ)


def arm_holes():
    """M2 clearance (2.2) through the pod floor for the skid-arm screws (heads in the pod cavity, threads in the arm riser)."""
    from . import skids
    out = None
    for sx, sy in skids.ARM_SCREWS:
        h = bd.Pos(sx, sy, z0() - 0.5) * bd.Cylinder(1.1, P.TUB_FLOOR_T + 1.0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        out = h if out is None else out + h
    return out


def tub():
    return shell() + weapon_boss() + drive_bays() - bell_bore() - axle_holes() - arm_holes()
