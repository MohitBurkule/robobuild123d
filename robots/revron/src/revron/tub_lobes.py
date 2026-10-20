"""Side nut lobe and everything that mates with it: N10 keyholes, captive M3 nut pocket, lobe-tail trim for the
side panel / weapon mounts, motor stop wall rounding. Every feature is built for +X and mirrored (`_both`)."""
import math
from shapely.geometry import Point, Polygon
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403

# ---- lobe (relations off CH / NUT_LOBE)
LOBE_SINK = 0.1                       # lobe starts this far inside the wall face (fuses with the wall)
LOBE_OUT = CH["x"] + 3.0              # outer face of the lobe, |X|
LOBE_ROOT_R, LOBE_ROOT_BANDS = 1.95, 12   # STEP root fillet where the lobe leaves the wall, as one ruled loft of 12 bands
# ---- N10 keyhole (U-slot to the floor)
KH_SEAT_R, KH_NECK_DZ, KH_NECK_R = 2.5, 5.15, 0.85   # round seat for the gearbox boss, neck below it (STEP keyhole)
KH_NECK_Z = RZ - KH_NECK_DZ
KH_SLOT_HALF = 2.05                   # slot half width: 4 dia gearbox boss + 0.05 each side
KH_SEG, KH_SEG_NECK = 64, 24
# ---- captive M3 nut
NUT_BORE_R = 1.6                      # M3 clearance
NUT_BORE_IN, NUT_BORE_OUT = 1.5, 0.5  # bore starts this far inside the inner wall face, ends this far past the lobe
POCKET_RU, POCKET_RV = 3.12, 3.13     # hex pocket radii along Y / Z: 0.05 under the 5.5 AF / 6.35 corner thin M3 nut (pressed in)
POCKET_IN = 0.5                       # pocket starts this far inside the inner wall face, ends at the outer wall face
HEX_N = 6
HEX_PHASE = 360 / HEX_N / 2           # flats parallel to the Z axis
RELIEF_OUT = 1.5
FLOOR_RELIEF_DEPTH = 3.0              # the root fillet must not hang below the floor plane
# param: organic nut detail relief measured on the STEP (Y, Z), sits beside the nut
NUT_DETAIL = [(-7.14, 6.85), (-3.45, 7.05), (-3.45, 7.95), (-6.9, 8.9)]
NUT_DETAIL_R = 0.25
# ---- motor stop wall lower inner edge R4.5 (STEP)
STOP_ROUND_R = 4.5
STOP_ROUND_C = (22.2, 9.0)            # arc centre (X, Z)
STOP_WALL_Y = (-25.4, -23.4)
STOP_OVER = 0.1                       # cutter reaches this far past the wall/arc: no skin left under the R0.9 corner fillet
STOP_THRU = 1.0                       # cutter length behind the wall
# ---- lobe tail: panel/lobe overlap slab removed with the side panel
TAIL_LEN, TAIL_OUT, TAIL_MARGIN = 12.0, 4.0, 2.0


def _both(s):
    return [s, _mirror_x(s)]


def _rect(u0, u1, v0, v1):
    return _poly([(u0, v0), (u1, v0), (u1, v1), (u0, v1)])


# ------------------------------------------------------------------------------------------------------------ additions
def _root_offset(h):
    """Outward offset of the lobe outline at height h above the wall face on a quarter round of radius LOBE_ROOT_R."""
    return LOBE_ROOT_R - math.sqrt(LOBE_ROOT_R ** 2 - (LOBE_ROOT_R - h) ** 2)


def lobe_body(c):
    return _ext(NUT_LOBE, "yz", c["x"] - LOBE_SINK, LOBE_OUT)


def lobe_root_fillet(c):
    x0 = c["x"] - LOBE_SINK
    heights = [LOBE_ROOT_R * k / LOBE_ROOT_BANDS for k in range(LOBE_ROOT_BANDS + 1)]
    return _loft_yz_n([(NUT_LOBE.buffer(_root_offset(h), join_style=1), x0 + h) for h in heights])


def additions(c):
    out = []
    for s in (lobe_body(c), lobe_root_fillet(c)):
        out += _both(s)
    return out


# ---------------------------------------------------------------------------------------------------------------- cuts
def keyhole(c):
    """Round seat for the gearbox shaft boss narrowing to the floor, opened into a U-slot so the boss drops in from below."""
    seat = Point(RY, RZ).buffer(KH_SEAT_R, KH_SEG).union(Point(RY, KH_NECK_Z).buffer(KH_NECK_R, KH_SEG_NECK)).convex_hull
    slot = _rect(RY - KH_SLOT_HALF, RY + KH_SLOT_HALF, c["z0"] - 1.0, RZ)
    return _ext(seat.union(slot), "yz", c["x"] - c["wall"] - 0.5, c["x"] + 0.5)


def nut_bore(c):
    return _cyl(NUT_BORE_R, c["x"] - c["wall"] - NUT_BORE_IN, LOBE_OUT + NUT_BORE_OUT, NUT)


def floor_relief(c):
    y0, z0, y1, z1 = NUT_LOBE.bounds   # outline is in (Y, Z)
    return _box(c["x"] - 0.5, LOBE_OUT + RELIEF_OUT, y0 - LOBE_ROOT_R - 1.0, y1 + LOBE_ROOT_R + 1.0,
                c["z0"] - FLOOR_RELIEF_DEPTH, c["z0"])


def hex_pocket(c):
    hexp = Polygon([(NUT[0] + POCKET_RU * math.cos(math.radians(HEX_PHASE + 360 / HEX_N * i)),
                     NUT[1] + POCKET_RV * math.sin(math.radians(HEX_PHASE + 360 / HEX_N * i))) for i in range(HEX_N)])
    return _ext(hexp, "yz", c["x"] - c["wall"] - POCKET_IN, c["x"])


def nut_detail(c):
    return _ext(_round(Polygon(NUT_DETAIL), r_out=NUT_DETAIL_R), "yz", c["x"] - 0.5, LOBE_OUT + 0.5)


def stop_wall_round(c):
    cx, cz = STOP_ROUND_C
    r = STOP_ROUND_R
    fil = _rect(cx - r - STOP_OVER, cx, cz - r - STOP_OVER, cz).difference(Point(cx, cz).buffer(r, KH_SEG))
    return _ext(fil, "xz", STOP_WALL_Y[0] - STOP_OVER, STOP_WALL_Y[1] + STOP_THRU)


def lobe_tail(c):
    """Whole overlapping slab of the lobe tail (rounded inside corner) goes with the side panel cut."""
    y1 = NUT_RELIEF_Y0
    tail = _rect(PANEL_IN, c["x"] + TAIL_OUT, y1 - TAIL_LEN, y1).buffer(-NUT_STEP_R).buffer(NUT_STEP_R)
    return _ext(tail, "xy", NUT_LOBE.bounds[1] - TAIL_MARGIN, NUT_LOBE.bounds[3] + TAIL_MARGIN)


def panel_mating():
    """The weapon mounts and side panels seat on the chassis: their solids are cut out of it."""
    from .weapon import weapon_mount
    from .side import side_panel
    return [weapon_mount("l"), weapon_mount("r"), side_panel(1), side_panel(-1)]


def cuts(c):
    out = []
    for f in (keyhole, nut_bore, floor_relief, hex_pocket, nut_detail, stop_wall_round, lobe_tail):
        out += _both(f(c))
    return out + panel_mating()
