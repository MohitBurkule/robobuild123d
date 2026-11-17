"""Buzzkill parametric build123d solid builders.

Every function returns a build123d Solid in its own local frame (or world frame for tub/lid/hoop when placed at [0,0,0]).
"""

from __future__ import annotations

import math
import os
import sys

_SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if _SRC not in sys.path:
    sys.path.insert(0, _SRC)

import build123d as bd

from robot import catalog as C
from robot.cad.bay import derive_bay

from buzzkill import params as P


def _poly_face(pts, z=0.0):
    from shapely.geometry import Polygon

    p = Polygon(pts)
    coords = list(p.exterior.coords)[:-1]
    if p.exterior.is_ccw is False:
        coords = coords[::-1]
    wire = bd.Wire.make_polygon([bd.Vector(x, y, z) for x, y in coords] + [bd.Vector(coords[0][0], coords[0][1], z)])
    f = bd.Face(wire)
    if f.normal_at().Z < 0:
        f = bd.Face(wire.reversed())
    return f


def _inset_poly(pts, d):
    """Inset a CCW 2D polygon by d using shapely (exact offset, clean corners)."""
    from shapely.geometry import Polygon

    poly = Polygon(pts).buffer(-d, join_style=2)  # mitre join
    coords = list(poly.exterior.coords)[:-1]
    if poly.exterior.is_ccw is False:
        coords = coords[::-1]
    return [(float(x), float(y)) for x, y in coords]


def tub():
    """Printed nylon faceted stealth tub with integral outboard weapon upright, wheel wells, and COTS bays."""
    # 1. Outer faceted hull
    f_bot = _poly_face(P.OUTER_POLY, P.TUB_FLOOR_Z)
    hull_lower = bd.extrude(f_bot, P.TUB_TOP_Z - P.TUB_FLOOR_Z, dir=(0, 0, 1))
    body = hull_lower

    # 2. Inner cavity (open top, leaves floor of TUB_FLOOR_T and perimeter WALL)
    inner_pts = _inset_poly(P.OUTER_POLY, P.WALL)
    f_in = _poly_face(inner_pts, P.TUB_FLOOR_Z + P.TUB_FLOOR_T)
    cavity = bd.extrude(f_in, P.TUB_TOP_Z - (P.TUB_FLOOR_Z + P.TUB_FLOOR_T) + 2.0, dir=(0, 0, 1))
    body = body - cavity

    # 3. Screw boss columns inside perimeter for LID_SCREWS (keeps walls thin elsewhere)
    for sx, sy in P.LID_SCREWS:
        boss = bd.Pos(sx, sy, (P.TUB_FLOOR_Z + P.TUB_TOP_Z) / 2.0) * bd.Cylinder(3.0, P.TUB_TOP_Z - P.TUB_FLOOR_Z)
        body = body + (boss & hull_lower)
        hole = bd.Pos(sx, sy, P.TUB_TOP_Z - 2.5) * bd.Cylinder(P.INSERT_D / 2.0, 5.2)
        body = body - hole

    # 4. Upright mounting insert holes (outboard at X=-35.25, inboard at X=-4.0) + driver access holes
    for uy in (2.0, 10.0):
        body = body - (bd.Pos(P.UPRIGHT_X0 - 1.5, uy, -5.0) * bd.Rot(0, 90, 0) * bd.Cylinder(P.INSERT_D / 2.0, 4.0))
    for uz in (-5.0, 5.0):
        uboss = bd.Pos(-2.5, 0.5, uz) * bd.Rot(0, 90, 0) * bd.Cylinder(2.6, 3.2)
        body = body + uboss
        body = body - (bd.Pos(-2.5, 0.5, uz) * bd.Rot(0, 90, 0) * bd.Cylinder(P.INSERT_D / 2.0, 3.6))
    for k in range(4):
        ang = math.radians(45.0 + 90.0 * k)
        dy, dz = 4.5 * math.cos(ang), 4.5 * math.sin(ang)
        body = body - (bd.Pos(-3.2, P.Y_AX + dy, P.Z_AX + dz) * bd.Rot(0, 90, 0) * bd.Cylinder(1.8, 4.0))

    # 5. Mechanical retaining rails on tub floor for battery, drive_esc, and weapon_esc (0.4-0.5 mm clearance)
    z_rail = P.TUB_FLOOR_Z + P.TUB_FLOOR_T + 0.75
    # Battery at [11.0, 12.9] (17 x 61 mm -> X=2.5..19.5, Y=-17.6..43.4): left, right, & rear rails (0.3 mm gap)
    z_brail = P.TUB_FLOOR_Z + P.TUB_FLOOR_T + 2.25
    body = body + (bd.Pos(1.7, 12.9, z_brail) * bd.Box(1.0, 30.0, 4.5))
    body = body + (bd.Pos(20.3, 12.9, z_brail) * bd.Box(1.0, 40.0, 4.5))
    body = body + (bd.Pos(11.0, -18.4, z_rail) * bd.Box(14.0, 1.0, 1.5))
    # Drive ESC at [40.0, 0.0] (32 x 19 mm -> X=24.0..56.0, Y=-9.5..9.5): -X, +X, -Y, +Y rails
    body = body + (bd.Pos(23.0, 0.0, z_rail) * bd.Box(1.0, 14.0, 1.5))
    body = body + (bd.Pos(57.0, 0.0, z_rail) * bd.Box(1.0, 14.0, 1.5))
    body = body + (bd.Pos(40.0, -10.5, z_rail) * bd.Box(24.0, 1.0, 1.5))
    body = body + (bd.Pos(40.0, 10.5, z_rail) * bd.Box(24.0, 1.0, 1.5))
    # Weapon ESC at [-24.0, -22.0] (12 x 23 mm -> X=-30.0..-18.0, Y=-33.5..-10.5): -X, +X, +Y rails
    body = body + (bd.Pos(-31.0, -22.0, z_rail) * bd.Box(1.0, 16.0, 1.5))
    body = body + (bd.Pos(-17.0, -22.0, z_rail) * bd.Box(1.0, 16.0, 1.5))
    body = body + (bd.Pos(-24.0, -9.5, z_rail) * bd.Box(10.0, 1.0, 1.5))

    # 7. Wheel wells & N10 drive motor pockets (both sides)
    for s in (-1.0, 1.0):
        # Wheel well open to bottom
        ww = bd.Pos(s * P.WHEEL_X, P.DRIVE_Y, P.DRIVE_Z) * bd.Rot(0, 90, 0) * bd.Cylinder(P.WHEEL_R + 1.8, P.WHEEL_W + 2.6)
        ww_drop = bd.Pos(s * P.WHEEL_X, P.DRIVE_Y, P.TUB_FLOOR_Z) * bd.Box(P.WHEEL_W + 2.6, 2 * (P.WHEEL_R + 1.8), 10.0)
        body = body - ww - ww_drop
        # N10 motor pocket (open to +Z for drop-in assembly) + shaft bore
        mp = bd.Pos(s * P.MOTOR_X, P.DRIVE_Y, (-5.5 + P.TUB_TOP_Z + 1.0) / 2.0) * bd.Box(26.0, 13.0, P.TUB_TOP_Z + 1.0 - (-5.5))
        sb = bd.Pos(s * (P.MOTOR_X + 12.0), P.DRIVE_Y, P.DRIVE_Z) * bd.Rot(0, 90, 0) * bd.Cylinder(2.2, 16.0)
        body = body - mp - sb

    # 8. Switch pocket (thin shelf at Z=4.8..6.0 bridged to +X wall, clear of drive_esc) & hoop side-mount bosses
    sw_pad = bd.Pos(52.5, P.SW_AT[1], 5.4) * bd.Box(23.0, 17.0, 1.2)
    body = body + sw_pad
    sw_loc = bd.Location(tuple(P.SW_AT), tuple(P.SW_ROT))
    sw_bay = derive_bay(C.find(P.SWITCH), placement=sw_loc, insert_dir="-z")
    body = body - sw_bay.cut_solid()

    # Hoop side-mount insert holes (at X = +-58.0, Y = HOOP_Y, Z = 4.0)
    for s in (-1.0, 1.0):
        body = body - (bd.Pos(s * (P.BODY_HALF_W - 2.0), P.HOOP_Y, P.HOOP_Z_BASE) * bd.Rot(0, 90, 0) * bd.Cylinder(P.INSERT_D / 2.0, 4.5))

    # 9. Front fork mount pockets & insert holes (ceiling at Z = -10.8 flush with fork top)
    for fx, fy0 in ((P.FORK_L_X, P.FORK_L_Y0), (P.FORK_R_X, P.FORK_R_Y0)):
        fpocket = bd.Pos(fx, (fy0 + 49.0) / 2.0, -11.525) * bd.Box(6.6, 51.0 - fy0, 1.45)
        body = body - fpocket
        for fy in (fy0 + 3.0, fy0 + 9.0):
            fboss = bd.Pos(fx, fy, P.TUB_FLOOR_Z + 3.1) * bd.Cylinder(2.6, 4.2)
            body = body + fboss
            body = body - (bd.Pos(fx, fy, P.TUB_FLOOR_Z + 2.9) * bd.Cylinder(P.INSERT_D / 2.0, 4.4))

    return body


def lid():
    """Printed nylon top lid with Buzzkill's signature slotted ribs and triangular recessed pockets."""
    pts = _inset_poly(P.OUTER_POLY, P.CHAMFER_TOP_INSET)
    f_lid = _poly_face(pts, P.TUB_TOP_Z)
    plate = bd.extrude(f_lid, P.LID_T, dir=(0, 0, 1))

    # Cut clearance around outboard upright (-35.25..-33.25) and inboard disc-screw driver access (-6..+4, Y=19..33)
    plate = plate - (bd.Pos(-34.25, 6.0, P.TUB_TOP_Z + P.LID_T / 2.0) * bd.Box(2.6, 20.0, P.LID_T + 1.0))
    plate = plate - (bd.Pos(-1.0, 26.0, P.TUB_TOP_Z + P.LID_T / 2.0) * bd.Box(10.5, 14.0, P.LID_T + 1.0))

    # Recessed decorative grooves (0.4 mm deep, NOT through-holes so electronics stay shielded!)
    z_top = P.TUB_TOP_Z + P.LID_T
    for gy in (-24.0, -14.0, -4.0, 6.0, 16.0, 26.0):
        groove = bd.Pos(10.0, gy, z_top - 0.2) * bd.Box(86.0, 1.4, 0.5)
        plate = plate - (groove & plate)

    # Triangular recessed pockets in center (0.4 mm deep, matching image.png)
    for ty in (-10.0, 2.0, 14.0):
        tri = bd.Polygon((-8.0, ty - 3.5), (6.0, ty), (-8.0, ty + 3.5), align=None)
        plate = plate - bd.extrude(bd.Plane.XY.offset(z_top - 0.4) * tri, 0.6, dir=(0, 0, 1))

    # Switch toggle cutout over SW_AT
    sw_cut = bd.Pos(P.SW_AT[0], P.SW_AT[1], z_top - 0.75) * bd.Box(7.0, 11.0, 2.5)
    plate = plate - sw_cut

    # Clearance holes + counterbores for LID_SCREWS
    for sx, sy in P.LID_SCREWS:
        plate = plate - (bd.Pos(sx, sy, z_top - P.LID_T / 2.0) * bd.Cylinder(1.15, P.LID_T + 1.0))

    # Battery hold-down pads on underside of lid (battery top Z=3.7, pad bottom Z=4.05 -> 0.35 mm gap)
    for py in (-10.0, 30.0):
        plate = plate + (bd.Pos(11.0, py, (4.05 + P.TUB_TOP_Z + 0.1) / 2.0) * bd.Box(6.0, 2.0, P.TUB_TOP_Z + 0.1 - 4.05))

    return plate


def disc():
    """CNC-milled 7075 aluminium vertical drisk spinner wrapping around the BE1806 bell.

    Local frame relative to weapon_motor_bell at [X_MOT, Y_AX, Z_AX]:
    spin axis = +X, centered at (0, 0) in YZ.
    """
    R = P.DISC_R
    pts = []
    n_seg = 72
    for i in range(n_seg):
        a = 2.0 * math.pi * i / n_seg
        deg = (math.degrees(a)) % 180.0
        if deg < 10.0:
            r = R - 2.25 - 2.75 * (0.5 - 0.5 * math.cos(math.pi * deg / 10.0))
        elif deg < 22.0:
            r = R - 5.0 * (0.5 + 0.5 * math.cos(math.pi * (deg - 10.0) / 12.0))
        else:
            r = R - 2.25 * ((deg - 22.0) / 158.0)
        pts.append((r * math.cos(a), r * math.sin(a)))

    # Ring wrapping around bell (local X = DISC_RING_X0 - X_MOT .. DISC_RING_X1 - X_MOT)
    ring_x0 = P.DISC_RING_X0 - P.X_MOT
    ring_w = P.DISC_RING_X1 - P.DISC_RING_X0
    ring_face = bd.Face(bd.Wire([bd.Edge.make_spline([bd.Vector(ring_x0, y, z) for y, z in pts], periodic=True)]))
    ring_solid = bd.extrude(ring_face, ring_w, dir=(1, 0, 0))
    bell_bore = bd.Pos(ring_x0 + ring_w / 2.0, 0, 0) * bd.Rot(0, 90, 0) * bd.Cylinder(
        P.DISC_RING_ID / 2.0, ring_w + 1.0
    )
    ring_solid = ring_solid - bell_bore

    # Inboard web (local X = DISC_WEB_X0 - X_MOT .. DISC_WEB_X1 - X_MOT) bolted to bell top face
    web_x0 = P.DISC_WEB_X0 - P.X_MOT
    web_w = P.DISC_WEB_X1 - P.DISC_WEB_X0
    web_cx = web_x0 + web_w / 2.0
    web_solid = bd.Pos(web_cx, 0, 0) * bd.Rot(0, 90, 0) * bd.Cylinder(
        P.DISC_RING_ID / 2.0 + 1.5, web_w
    )
    solid = ring_solid + web_solid

    # Center 4 mm shaft bore + 4x M2 bell mounting holes (9 mm circle at 45 deg)
    solid = solid - (bd.Pos(web_cx, 0, 0) * bd.Rot(0, 90, 0) * bd.Cylinder(2.15, web_w + 2.0))
    for k in range(4):
        ang = math.radians(45.0 + 90.0 * k)
        dy, dz = 4.5 * math.cos(ang), 4.5 * math.sin(ang)
        solid = solid - (bd.Pos(web_cx, dy, dz) * bd.Rot(0, 90, 0) * bd.Cylinder(1.1, web_w + 2.0))

    return solid


def hoop():
    """Self-righting arch spanning over the top of the chassis from -X to +X."""
    z_arch = P.HOOP_Z_BASE + 5.0
    pts = [
        bd.Vector(-P.BODY_HALF_W - 1.6, P.HOOP_Y, z_arch),
        bd.Vector(-P.HOOP_X_SPAN, P.HOOP_Y, z_arch + 12.0),
        bd.Vector(-36.0, P.HOOP_Y, P.HOOP_Z_PEAK - 8.0),
        bd.Vector(0.0, P.HOOP_Y, P.HOOP_Z_PEAK),
        bd.Vector(36.0, P.HOOP_Y, P.HOOP_Z_PEAK - 8.0),
        bd.Vector(P.HOOP_X_SPAN, P.HOOP_Y, z_arch + 12.0),
        bd.Vector(P.BODY_HALF_W + 1.6, P.HOOP_Y, z_arch),
    ]
    spine = bd.Edge.make_spline(pts)
    profile = bd.Plane(origin=pts[0], z_dir=spine % 0) * bd.Circle(P.HOOP_R_TUBE)
    arch = bd.sweep(profile, spine)

    # Vertical mounting tabs on both ends for M2 screws into the tub sides
    for s in (-1.0, 1.0):
        pad = bd.Pos(s * (P.BODY_HALF_W + 1.3), P.HOOP_Y, P.HOOP_Z_BASE + 2.3) * bd.Box(2.6, 6.0, 10.6)
        hole = bd.Pos(s * (P.BODY_HALF_W + 1.3), P.HOOP_Y, P.HOOP_Z_BASE) * bd.Rot(0, 90, 0) * bd.Cylinder(1.2, 5.0)
        arch = arch + pad - hole

    return arch


def fork(side_x: float, y0: float):
    """1.5 mm laser-cut titanium front wedgelet/fork at X = side_x (6 mm wide, tapered tip)."""
    pts = [
        (side_x - 3.0, y0),
        (side_x + 3.0, y0),
        (side_x + 1.8, P.FORK_Y1),
        (side_x - 1.8, P.FORK_Y1),
    ]
    z0 = P.TUB_FLOOR_Z - 1.0
    s = bd.extrude(bd.Plane.XY.offset(z0) * bd.Polygon(*pts, align=None), P.FORK_T)
    for fy in (y0 + 3.0, y0 + 9.0):
        s = s - (bd.Pos(side_x, fy, z0 + P.FORK_T / 2.0) * bd.Cylinder(1.15, P.FORK_T + 1.0))
        s = s - (bd.Pos(side_x, fy, z0 + 0.6) * bd.Cone(2.25, 1.15, 1.2))
    return s


def wshaft():
    """2 mm steel through-shaft from outboard upright through bell & disc into inboard MR52 bearing."""
    L = P.SHAFT_X1 - P.SHAFT_X0
    cx = (P.SHAFT_X0 + P.SHAFT_X1) / 2.0 - P.X_MOT
    return bd.Pos(cx, 0, 0) * bd.Rot(0, 90, 0) * bd.Cylinder(P.SHAFT_R, L)


def wbearing():
    """MR52 bearing (2 mm ID, 5 mm OD, 2.5 mm wide) in inboard chassis wall."""
    cx = (P.BEARING_X0 + P.BEARING_X1) / 2.0
    outer = bd.Pos(cx, 0, 0) * bd.Rot(0, 90, 0) * bd.Cylinder(P.BEARING_OD / 2.0, P.BEARING_W)
    inner = bd.Pos(cx, 0, 0) * bd.Rot(0, 90, 0) * bd.Cylinder(P.BEARING_ID / 2.0, P.BEARING_W + 1.0)
    return outer - inner


def locking_bar():
    """3 mm titanium weapon locking pin."""
    return bd.Pos(-26.0, P.Y_AX - 14.0, P.Z_AX + 4.0) * bd.Rot(0, 90, 0) * bd.Cylinder(1.5, 22.0)


def upright_outboard():
    """2.0 mm laser-cut titanium outboard weapon motor upright bolted to tub."""
    u_thick = P.UPRIGHT_X1 - P.UPRIGHT_X0
    u_cx = (P.UPRIGHT_X0 + P.UPRIGHT_X1) / 2.0
    u_pts = [
        (P.NOTCH_Y0, P.TUB_FLOOR_Z),
        (P.Y_AX + P.UPRIGHT_BOSS_R, P.TUB_FLOOR_Z),
        (P.Y_AX + P.UPRIGHT_BOSS_R, P.Z_AX),
        (P.Y_AX, P.Z_AX + P.UPRIGHT_BOSS_R),
        (P.NOTCH_Y0 + 6.0, P.TUB_TOP_Z),
        (P.NOTCH_Y0, P.TUB_TOP_Z),
    ]
    u_face = bd.Plane.YZ * bd.Polygon(*u_pts, align=None)
    plate = bd.Pos(P.UPRIGHT_X0, 0, 0) * bd.extrude(u_face, u_thick, dir=(1, 0, 0))
    u_boss = bd.Pos(u_cx, P.Y_AX, P.Z_AX) * bd.Rot(0, 90, 0) * bd.Cylinder(P.UPRIGHT_BOSS_R, u_thick)
    plate = plate + u_boss
    plate = bd.fillet(plate.edges().filter_by(bd.Axis.X), 0.5)
    # 4x M2 motor base holes
    for dy, dz in ((6.0, 0.0), (-6.0, 0.0), (0.0, 8.0), (0.0, -8.0)):
        plate = plate - (bd.Pos(u_cx, P.Y_AX + dy, P.Z_AX + dz) * bd.Rot(0, 90, 0) * bd.Cylinder(1.15, u_thick + 2.0))
    # Shaft hole, locking bar hole, 2x tub mounting holes, and weight-relief cutouts
    plate = plate - (bd.Pos(u_cx, P.Y_AX, P.Z_AX) * bd.Rot(0, 90, 0) * bd.Cylinder(P.SHAFT_R + 0.05, u_thick + 2.0))
    plate = plate - (bd.Pos(u_cx, P.Y_AX - 14.0, P.Z_AX + 4.0) * bd.Rot(0, 90, 0) * bd.Cylinder(1.6, u_thick + 2.0))
    for uy in (2.0, 10.0):
        plate = plate - (bd.Pos(u_cx, uy, -5.0) * bd.Rot(0, 90, 0) * bd.Cylinder(1.15, u_thick + 2.0))
    plate = plate - (bd.Pos(u_cx, 25.0, -3.0) * bd.Rot(0, 90, 0) * bd.Cylinder(4.5, u_thick + 2.0))
    plate = plate - (bd.Pos(u_cx, 11.0, 4.0) * bd.Rot(0, 90, 0) * bd.Cylinder(4.0, u_thick + 2.0))
    return plate


def upright_inboard():
    """2.0 mm CNC-milled aluminium inboard bearing plate bolted to tub."""
    u_thick = 2.0
    u_cx = -5.0
    u_pts = [
        (P.NOTCH_Y0, P.TUB_FLOOR_Z),
        (5.0, P.TUB_FLOOR_Z),
        (P.Y_AX + 6.5, P.Z_AX - 6.5),
        (P.Y_AX + 6.5, P.Z_AX + 6.5),
        (P.Y_AX - 6.5, P.Z_AX + 6.5),
        (P.NOTCH_Y0 + 5.0, P.TUB_TOP_Z - 2.0),
        (P.NOTCH_Y0, P.TUB_TOP_Z - 2.0),
    ]
    u_face = bd.Plane.YZ * bd.Polygon(*u_pts, align=None)
    plate = bd.Pos(-6.0, 0, 0) * bd.extrude(u_face, u_thick, dir=(1, 0, 0))
    plate = bd.fillet(plate.edges().filter_by(bd.Axis.X), 1.1)
    # Through-bore for MR83 bearing (8.0 mm OD)
    plate = plate - (bd.Pos(u_cx, P.Y_AX, P.Z_AX) * bd.Rot(0, 90, 0) * bd.Cylinder(P.BEARING_OD / 2.0 + 0.02, u_thick + 2.0))
    # 2x tub mounting holes (front tab, clear of disc) + lightening cutout
    for uz in (-5.0, 5.0):
        plate = plate - (bd.Pos(u_cx, 0.5, uz) * bd.Rot(0, 90, 0) * bd.Cylinder(1.15, u_thick + 2.0))
    plate = plate - (bd.Pos(u_cx, 12.0, 2.0) * bd.Rot(0, 90, 0) * bd.Cylinder(4.0, u_thick + 2.0))
    return plate


PARTS = {
    "tub": tub,
    "lid": lid,
    "disc": disc,
    "hoop": hoop,
    "upright_outboard": upright_outboard,
    "upright_inboard": upright_inboard,
    "fork_l": lambda: fork(P.FORK_L_X, P.FORK_L_Y0),
    "fork_r": lambda: fork(P.FORK_R_X, P.FORK_R_Y0),
    "wshaft": wshaft,
    "wbearing": wbearing,
    "locking_bar": locking_bar,
}


def build(part: str, origin=None):
    s = PARTS[part]()
    if origin:
        s = s.moved(bd.Location(tuple(-float(v) for v in origin)))
    return s
