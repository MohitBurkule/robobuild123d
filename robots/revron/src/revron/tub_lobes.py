"""Side nut lobe and everything that mates with it: N10 keyholes, captive M3 nut pocket, lobe-tail trim for the
side panel / weapon mounts, motor stop wall rounding. Every feature is built for +X and mirrored (`_both`)."""
import math
from shapely.geometry import Point, Polygon
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403

# ---- lobe (relations off CH / LOBE)
LOBE_SINK = 0.1                       # lobe starts this far inside the wall face (fuses with the wall)
LOBE_PROUD = 3.0                      # lobe stands this proud of the wall's outer face
LOBE_OUT = CH_HALF_W + LOBE_PROUD      # outer face of the lobe, |X|
LOBE_NUT_R, LOBE_CAP, LOBE_CAP_R, LOBE_SEG = 4.5, (0.5, 6.9), 2.0, 64   # organic STEP lobe: R4.5 round the nut hulled with an R2 end cap (Y, Z)
LOBE = Point(NUT[0], NUT[1]).buffer(LOBE_NUT_R, LOBE_SEG).union(Point(*LOBE_CAP).buffer(LOBE_CAP_R, LOBE_SEG)).convex_hull
LOBE_ROOT_R = PANEL_IN - CH_HALF_W + 0.05    # STEP Fillet3 is R2; 1.95 here (1.9 and 1.99 make OCC fail): its tangent line on the lobe stops 0.05 short of the side panel inner face (|X| 31.5), so it never grazes the panel plane (non-manifold edge / 0.11 mm tub-side overlap at the lobe end)
LOBE_ROOT_TOL = 0.05                  # edge-on-wall-plane tolerance when picking the root edges
# ---- N10 keyhole (U-slot to the floor)
KH_SEAT_R, KH_NECK_DZ, KH_NECK_R = 2.5, 5.15, 0.85   # round seat for the gearbox boss, neck below it (STEP keyhole)
KH_NECK_Z = RZ - KH_NECK_DZ
KH_BOSS_R, KH_SLOT_CLR = 2.0, 0.05    # 4 dia gearbox boss, slot clearance each side
KH_SLOT_HALF = KH_BOSS_R + KH_SLOT_CLR   # slot half width
KH_SEG, KH_SEG_NECK = 64, 24
# ---- captive M3 nut
NUT_BORE_R = 1.6                      # M3 clearance
CUT_BELOW = 1.0                       # slot cutter reaches this far below the floor
CUT_OVER = 0.5                        # cutters overshoot the faces they open through
NUT_BORE_IN, NUT_BORE_OUT = 1.5, CUT_OVER  # bore starts this far inside the inner wall face, ends this far past the lobe
HEX_N = 6
HEX_PHASE = 360 / HEX_N / 2           # flats parallel to the Z axis
POCKET_RU, POCKET_RV = 3.12, 3.13     # hex pocket radii along Y / Z: ~0.05 under the 5.5 AF / 6.35 corner thin M3 nut (pressed in); STEP-fitted, not re-derived
POCKET_IN = CUT_OVER                  # pocket starts this far inside the inner wall face, ends at the outer wall face
RELIEF_OUT = 1.5
FLOOR_RELIEF_DEPTH = 3.0              # the root fillet must not hang below the floor plane
# param: organic nut detail relief measured on the STEP (Y, Z), sits beside the nut
NUT_DETAIL = [(-7.14, 6.85), (-3.45, 7.05), (-3.45, 7.95), (-6.9, 8.9)]
# param: end
NUT_DETAIL_R = 0.25
# ---- motor stop wall lower inner edge R4.5 (STEP)
STOP_ROUND_R = 4.5
STOP_ROUND_X = 22.2                   # arc centre |X| (STEP)
STOP_ROUND_C = (STOP_ROUND_X, CH_Z0 + CH_WALL + STOP_ROUND_R)   # arc (X, Z) rests on the floor panel's top face
STOP_WALL_Y = (KEY_SPAN[1] - CH_WALL, KEY_SPAN[1])   # wall as thick as the chassis wall, ending at the key tab's front
STOP_OVER = 0.1                       # cutter reaches this far past the wall/arc: no skin left under the R0.9 corner fillet
STOP_THRU = 1.0                       # cutter length behind the wall
# ---- lobe tail: panel/lobe overlap slab removed with the side panel
TAIL_LEN, TAIL_MARGIN = 12.0, 2.0
TAIL_OUT = LOBE_PROUD + 1.0          # slab reaches 1 mm past the lobe's outer face


def _both(s):
    return [s, _mirror_x(s)]


def _rect(u0, u1, v0, v1):
    return _poly([(u0, v0), (u1, v0), (u1, v1), (u0, v1)])


# ------------------------------------------------------------------------------------------------------------ additions
def lobe_body(c):
    return _ext(LOBE, "yz", c["x"] - LOBE_SINK, LOBE_OUT)


def root_fillet(solid, c):
    """True R-LOBE_ROOT_R fillet round the closed loop where each lobe meets the wall's outer face (build123d fillet)."""
    y0, z0, y1, z1 = LOBE.bounds   # (Y, Z)
    m = LOBE_ROOT_R + 0.5

    def on_root(e):
        bb = e.bounding_box()
        return (abs(abs(bb.min.X) - c["x"]) < LOBE_ROOT_TOL and abs(bb.max.X - bb.min.X) < LOBE_ROOT_TOL
                and bb.min.Y > y0 - m and bb.max.Y < y1 + m and bb.min.Z > z0 - m and bb.max.Z < z1 + m)
    return _b().fillet([e for e in solid.edges() if on_root(e)], LOBE_ROOT_R)


def additions(c):
    out = []
    for s in (lobe_body(c),):
        out += _both(s)
    return out


# ---------------------------------------------------------------------------------------------------------------- cuts
def keyhole(c):
    """Round seat for the gearbox shaft boss narrowing to the floor, opened into a U-slot so the boss drops in from below."""
    seat = Point(RY, RZ).buffer(KH_SEAT_R, KH_SEG).union(Point(RY, KH_NECK_Z).buffer(KH_NECK_R, KH_SEG_NECK)).convex_hull
    slot = _rect(RY - KH_SLOT_HALF, RY + KH_SLOT_HALF, c["z0"] - CUT_BELOW, RZ)
    return _ext(seat.union(slot), "yz", c["x"] - c["wall"] - CUT_OVER, c["x"] + CUT_OVER)


def nut_bore(c):
    return _cyl(NUT_BORE_R, c["x"] - c["wall"] - NUT_BORE_IN, LOBE_OUT + NUT_BORE_OUT, NUT)


def floor_relief(c):
    y0, z0, y1, z1 = LOBE.bounds   # outline is in (Y, Z)
    return _box(c["x"] - CUT_OVER, LOBE_OUT + RELIEF_OUT, y0 - LOBE_ROOT_R - CUT_BELOW, y1 + LOBE_ROOT_R + CUT_BELOW,
                c["z0"] - FLOOR_RELIEF_DEPTH, c["z0"])


def hex_pocket(c):
    hexp = Polygon([(NUT[0] + POCKET_RU * math.cos(math.radians(HEX_PHASE + 360 / HEX_N * i)),
                     NUT[1] + POCKET_RV * math.sin(math.radians(HEX_PHASE + 360 / HEX_N * i))) for i in range(HEX_N)])
    return _ext(hexp, "yz", c["x"] - c["wall"] - POCKET_IN, c["x"])


def nut_detail(c):
    return _ext(_round(Polygon(NUT_DETAIL), r_out=NUT_DETAIL_R), "yz", c["x"] - CUT_OVER, LOBE_OUT + CUT_OVER)


def stop_wall_round(c):
    cx, cz = STOP_ROUND_C
    r = STOP_ROUND_R
    fil = _rect(cx - r - STOP_OVER, cx, cz - r - STOP_OVER, cz).difference(Point(cx, cz).buffer(r, KH_SEG))
    return _ext(fil, "xz", STOP_WALL_Y[0] - STOP_OVER, STOP_WALL_Y[1] + STOP_THRU)


def lobe_tail(c):
    """Whole overlapping slab of the lobe tail (rounded inside corner) goes with the side panel cut."""
    y1 = NUT_RELIEF_END_Y
    tail = _rect(PANEL_IN, c["x"] + TAIL_OUT, y1 - TAIL_LEN, y1).buffer(-NUT_STEP_R).buffer(NUT_STEP_R)
    return _ext(tail, "xy", LOBE.bounds[1] - TAIL_MARGIN, LOBE.bounds[3] + TAIL_MARGIN)


def panel_mating():
    """The weapon mounts and side panels seat on the chassis: their solids are cut out of it."""
    from .weapon import weapon_mount
    from .side import side_panel
    return [weapon_mount("l"), weapon_mount("r"), side_panel(1), side_panel(-1)]


def cuts(c):
    out = []
    for f in (keyhole, nut_bore, floor_relief, hex_pocket, nut_detail, lobe_tail):
        out += _both(f(c))
    return out + panel_mating()
