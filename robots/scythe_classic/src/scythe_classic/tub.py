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


SKIRT_INSET = 2.0   # mm the base circle sits inside TUB_R: gives the pod front corners an edge long enough to take the fillet
SLOPE_STEPS = 6   # ruled-loft sections up the sloped wall (each step turns the wall by well under the 45 deg sharp-corner threshold)
POD_CORNER_R = P.TUB_WALL + 1.1   # mm pod plan corner radius: the cavity corner (wall inside it) is then 1.3 mm
JOINT_R = 1.3   # mm inside radius where the pod front face meets the cone (outside) and at the top panel plan
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
    """Y of the pod's front edge: on the weapon axis, so it lies inside the cone's disc at every height and the pod's side walls run
    into the cone in one gentle concave edge (a front face outside the disc leaves an acute notch that cannot be rounded)."""
    return P.WPN_AXIS_Y


def pod_rear_y():
    """Rear edge: POD_L behind the wheel axle line."""
    return P.wheel_y() - P.POD_L / 2


def pod_len():
    return pod_front_y() - pod_rear_y()


def pod_cy():
    return (pod_front_y() + pod_rear_y()) / 2


RIM_EDGE_D = 4.6   # mm rim screw centre in from the outline (arch.edge_distance wants 1.5 x the 2 mm screw)
RIM_RIB_LEN = 14.0   # mm a rib's cut-out reaches out from its post (past the wall)
RIM_BOSS_R = 3.2   # mm radius of the post that carries a rim screw (its inner face is RIM_EDGE_D from the screw)
RIM_RIB_H = 8.0   # mm the posts and their ribs to the wall reach down from the top
RIM_POD_Y = (-15.0, -33.0)   # mm y of the rim screws on each pod wall (beside the receiver and the battery, clear of the wheel axle slots)


def rim_positions():
    """The six rim screws, each RIM_EDGE_D inside the top outline and clear of the electronics below: two on the cone's far side
    (45 and 135 deg), four on the pod walls (y = RIM_POD_Y)."""
    r = P.TUB_R - _slope_inset(height()) - RIM_EDGE_D
    cone = [(r * math.cos(math.radians(a)), P.WPN_AXIS_Y + r * math.sin(math.radians(a))) for a in (45, 135)]
    pod = [(sx * (P.POD_W / 2 - RIM_EDGE_D), y) for sx in (1, -1) for y in RIM_POD_Y]
    return cone + pod


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
    side = [v for v in outline.vertices() if abs(abs(v.X) - P.POD_W / 2) < 0.05]
    joint = [v for v in side if v.Y > pod_rear_y() + 1.0]
    corners = [v for v in side if v.Y <= pod_rear_y() + 1.0]
    outline = bd.fillet(joint, JOINT_R)
    return bd.fillet(bd.Sketch(outline).vertices().filter_by(lambda v: abs(abs(v.X) - P.POD_W / 2) < 0.05 and v.Y <= pod_rear_y() + 1.0), POD_CORNER_R)


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
    if h > height() - TOP_BAND_H + 1e-9:
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


def rim_posts():
    """[(x, y, ux, uy)]: each rim screw's centre and the outward direction its rib runs (radial on the cone, along x on the pod)."""
    out = []
    for x, y in rim_positions():
        if y < P.WPN_AXIS_Y - 10.0:
            out.append((x, y, math.copysign(1.0, x), 0.0))
        else:
            d = math.hypot(x, y - P.WPN_AXIS_Y)
            out.append((x, y, x / d, (y - P.WPN_AXIS_Y) / d))
    return out


def _cavity_face(inset, wall, ribs=False):
    """Cavity plan at one level: the outline offset in by the wall; with `ribs`, less the rim screws' posts, each a round post
    with a rib out to the wall (their joins to the wall rounded)."""
    face = bd.offset(top_outline(inset).faces()[0], amount=-wall, kind=bd.Kind.ARC).faces()[0]
    if not ribs:
        return face
    for x, y, ux, uy in rim_posts():
        ang = math.degrees(math.atan2(uy, ux))
        rib = bd.Pos(x + ux * RIM_RIB_LEN / 2, y + uy * RIM_RIB_LEN / 2) * bd.Rot(0, 0, ang) * bd.Rectangle(RIM_RIB_LEN, 2 * RIM_BOSS_R)
        face = face - rib - bd.Pos(x, y) * bd.Circle(RIM_BOSS_R)
    posts = rim_positions()
    joins = [(v.X, v.Y) for v in _corner_vertices(face, False) if any(math.hypot(v.X - x, v.Y - y) < RIM_RIB_LEN for x, y in posts)]
    for jx, jy in joins:   # one at a time: the face is rebuilt after each, so the vertex is found again by position
        v = min(face.vertices(), key=lambda q: math.hypot(q.X - jx, q.Y - jy))
        face = face.fillet_2d(FILLET_R, [v])
    return face


def cavity():
    """What is hollowed out: the same stack of plan outlines, each offset inward by the wall (taken square to the sloped wall, so
    the wall is the same thickness everywhere), from the floor up and out through the open top (the top panel closes it). The floor
    edge is rounded (FILLET_R) by four ruled steps of a quarter circle. The upper RIM_RIB_H of the wall carries the rim screws'
    posts: they are left standing in the cavity (a separate loft stack above, so the posts have one topology all the way up).
    Built from the sections, not by offsetting the solid: an offset of the faceted solid leaves sliver faces."""
    slope = math.radians(P.TUB_SLOPE_DEG)
    levels = _levels(CAVITY_EXTRA)
    z_floor = z0() + P.TUB_FLOOR_T
    z_split = z0() + height() - RIM_RIB_H
    z_skirt, z_cone_top = z0() + SKIRT_H, z0() + height() - TOP_BAND_H

    def wall_at(z):
        return P.TUB_WALL / math.cos(slope) if z_skirt + 1e-6 < z <= z_cone_top + 1e-6 else P.TUB_WALL

    r = FILLET_R
    low = []   # (z, inset, wall offset)
    for deg in (0, 22.5, 45, 67.5, 90):
        a = math.radians(deg)
        z = z_floor + r * (1 - math.cos(a))
        low.append((z, _inset_at(levels, z), P.TUB_WALL + r * (1 - math.sin(a))))
    for z in sorted({z for z, _ in levels if z_floor + r + 1e-6 < z < z_split - 1e-6} | {z_split}):
        low.append((z, _inset_at(levels, z), wall_at(z)))
    high = [(z, _inset_at(levels, z), wall_at(z)) for z in sorted({z for z, _ in levels if z > z_split + 1e-6} | {z_split})]
    lower = _stack([bd.Plane.XY.offset(z) * _cavity_face(inset, w) for z, inset, w in low])
    upper = _stack([bd.Plane.XY.offset(z) * _cavity_face(inset, w, ribs=True) for z, inset, w in high])
    return (lower + upper).clean()


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
GUARD_TAPER = 8.0   # mm the wheel-guard wing at each rear pod corner tapers back along the wall (a 13 deg turn, not a sharp corner)
RING_FLARE_R = 1.2  # mm fillet radius where the axle ring meets the wall
RING_OUT_R = 6.0    # mm axle ring outer radius
RING_BORE_R = P.WHEEL_HUB_R + 0.2   # mm the wheel hub boss turns in the ring bore (0.2 running clearance)
AXLE_SLOT_R = 2.3   # mm half width of the axle slot (shaft collar 2 mm radius, shaft 1.5 mm)
RIB_T = 1.2         # mm cradle rib thickness (nozzle multiple)
RIB_GAP = 0.45       # mm print clearance between the N10 flats and the ribs
PAD_GAP = 0.45       # mm between the motor shaft-side face and the pad that stops it
STOP_W = 2.4        # mm the rear stops reach in from each rib (they leave the solder-tab corridor free)
MOTOR_HALF_W = 6.0  # mm half width of the N10 body (catalogue box 9 x 12 x 10)
MOTOR_HALF_H = 5.0  # mm half height of the N10 body


FILLET_R = 1.2   # mm inside radius on printed concave corners (the sharp-corner check wants >= 1.0 measured on the facets)
CONVEX_R = 0.5   # mm rounding of the cradle's convex plan corners (the base fillet wraps cleanly round them)
CORNER_R = 1.8   # mm radius of the cradle's vertical concave corners (larger than the base fillet, or the two blends degenerate to a point)
SLAB_MARGIN = 2.0   # mm the cradle's base slab runs out beyond the cradle outline: room for the base fillet


def _corner_vertices(face, concave):
    """Vertices of a plan face that are true corners: reflex (concave) or convex, not the tangent joins between a line and an arc
    (about half the surrounding disc inside the face)."""
    out = []
    for v in face.vertices():
        n = 0
        for k in range(8):
            a = math.radians(22.5 + 45 * k)
            n += face.is_inside(bd.Vector(v.X + 0.05 * math.cos(a), v.Y + 0.05 * math.sin(a), 0))
        if (n > 4) if concave else (n < 4):
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
    plan = bd.fillet(_corner_vertices(plan.faces()[0], True), CORNER_R)
    plan = bd.fillet(_corner_vertices(plan.faces()[0], False), CONVEX_R)
    stand = bd.Pos(0, 0, z_lo) * bd.extrude(plan.faces()[0], z_hi - z_lo)
    slab_face = bd.offset(plan.faces()[0], amount=SLAB_MARGIN, kind=bd.Kind.ARC).faces()[0]
    slab = bd.Pos(0, 0, z0()) * bd.extrude(slab_face, P.TUB_FLOOR_T)
    slab = slab & (bd.Pos(0, pod_cy(), z0()) * bd.Box(2 * wall_i + 0.8, pod_len() - 2 * P.TUB_WALL + 0.8, P.TUB_FLOOR_T, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)))
    body = stand + slab
    edges = [e for e in body.edges() if e.center().X < wall_i - 0.01 and abs(e.bounding_box().min.Z - z_lo) < 1e-3 and abs(e.bounding_box().max.Z - z_lo) < 1e-3
             and min(e.distance_to(bd.Pos(0, 0, z_lo) * w) for w in plan.faces()[0].wires()) < 1e-3]
    return bd.fillet(edges, FILLET_R)


def axle_ring():
    """One axle ring, x-axis frame at the wall's outer face: a cylinder RING_OUT_R out to RING_LEN (and 0.2 into the wall) with a
    RING_FLARE_R fillet at its foot, made as a revolved profile."""
    f, R, L = RING_FLARE_R, RING_OUT_R, RING_LEN
    c = (f, R + f)
    mid = (c[0] - f * math.cos(math.radians(45)), c[1] - f * math.sin(math.radians(45)))
    with bd.BuildSketch(bd.Plane.XY) as sk:
        with bd.BuildLine():
            bd.Polyline((-0.2, 0), (-0.2, R + f), (0, R + f))
            bd.ThreePointArc((0, R + f), mid, (f, R))
            bd.Polyline((f, R), (L, R), (L, 0), (-0.2, 0))
        bd.make_face()
    return bd.revolve(sk.sketch, bd.Axis.X)


def guard_wing():
    """The wheel-guard wing at the rear pod corner: fills the rounded corner out to the wheel's inboard side (it carries the chassis
    hull out over the shaft tip), tapering back to the wall over GUARD_TAPER."""
    wall_o = P.POD_W / 2
    r = pod_rear_y()
    poly = bd.Polygon((wall_o - 3.0, r), (wall_o + RING_LEN, r), (wall_o, r + GUARD_TAPER), (wall_o - 3.0, r + GUARD_TAPER), align=None)
    plan = poly.faces()[0] - top_outline(SKIRT_INSET).faces()[0]
    return bd.Pos(0, 0, z0()) * bd.extrude(plan.faces()[0], height())


def drive_bays():
    """Per side: the N10's cradle (see cradle), the wheel's axle ring and a guard wing at the rear corner.
    Axle ring: stands off the wall's outer face round the wheel hub boss; its end holds the shaft's 3 mm grip inside the chassis
    hull (contain.electronics_exposed) and its lips keep the wheel and motor from lifting out. A slot, open at the top, takes
    the shaft up and out when the motor is lifted (the wheel leaves sideways first). The wing at the rear pod corner carries the
    hull out over the shaft tip."""
    wall_o = P.POD_W / 2
    out = cradle()
    out += bd.Pos(wall_o, P.wheel_y(), P.WHEEL_CZ) * axle_ring()
    out += guard_wing()
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


PILOT_R = 0.85      # mm M2 thread-forming pilot in printed nylon (1.7 drill, as Revron TOP_SCREW_WEB)
RIM_SCREW_L = 6.0   # mm M2x6 rim screw (make_spec fasteners)


def rim_pilots():
    """Pilot holes in the rim posts for the M2x6 top-panel screws: screw length less the panel, plus 0.5 mm tip room."""
    top = P.TUB_TOP_Z - P.TOP_PANEL_T
    depth = RIM_SCREW_L - P.TOP_PANEL_T + 0.5
    out = None
    for x, y in rim_positions():
        h = bd.Pos(x, y, top - depth) * bd.Cylinder(PILOT_R, depth + 0.1, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
        out = h if out is None else out + h
    return out


def tub():
    return shell() + weapon_boss() + drive_bays() - bell_bore() - axle_holes() - arm_holes() - rim_pilots()
