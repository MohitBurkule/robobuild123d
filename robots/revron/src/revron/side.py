"""[fix-S] Side groups: side panels, wedgelets, forks, standoffs, hubs, wheels / tyres."""
import json, math, os, sys
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403


def _fork_outline(s):
    """fork_5: 1.5 mm Ti fork. It hangs on the 15 mm nose standoff (5.2 hole) between the wedgelet cheeks, a pin hole
    in its tail stops it rotating; a triangular window lightens the blade, which tapers to a 1.5 mm tip."""
    from shapely.geometry import Point, Polygon
    x0, x1 = FK_X[1 if s > 0 else -1]
    outline = Point(*FK_EYE).buffer(FK_EYE_R, FK_RES).union(Polygon(FK_BLADE))
    outline = _round(outline, r_out=FK_ROUND[0], r_in=FK_ROUND[1]).union(Polygon(FK_TIP)).buffer(FK_TIP_R, FK_RES_BUF).buffer(-FK_TIP_R, FK_RES_BUF)   # sharp tip, r0.15 (> kerf) where it joins
    p = outline.difference(Point(SB[0], SB[1]).buffer(FK_SB_R, FK_RES)).difference(Point(*FK_EYE).buffer(FK_PIN_R, FK_RES_PIN))
    p = p.difference(_round(Polygon(FK_WIN), r_out=FK_WIN_R))   # lightening window
    # laser kerf / min web: the knife tip cannot be cut sharp; keep the full length but end it in a 0.45 mm land
    p = p.union(Polygon(FK_LAND)).buffer(0)
    if s < 0:   # the STEP hangs the left fork 1.1 deg nose-down about its standoff (pin-hole play in the cheek)
        from shapely import affinity
        p = affinity.rotate(p, FK_TILT, origin=SB)
    return p, x0, x1


def fork(s):
    p, x0, x1 = _fork_outline(s)
    return _ext(p, "yz", x0, x1)


def _fork_slot(s):
    """Seat for the fork tine in the wedgelet nose: the tine outline (window filled) swept straight up out of the
    ramp ahead of Y 42, so the slit is open to the top (the tine drops in) and no TPU film is left over the tine."""
    from shapely.geometry import Polygon
    from shapely import affinity
    p, x0, x1 = _fork_outline(s)
    solid = Polygon(p.exterior)
    up = solid
    for k in range(1, FKS_STEPS + 1):
        up = up.union(affinity.translate(solid, 0, FKS_DY * k))
    up = up.intersection(Polygon([(FKS_CLIP[0], FKS_CLIP[1]), (FKS_CLIP[2], FKS_CLIP[1]), (FKS_CLIP[2], FKS_CLIP[3]), (FKS_CLIP[0], FKS_CLIP[3])])).union(solid)
    return _ext(up.buffer(0), "yz", x0, x1)


def rear_hub(s):
    """RV21 printed rear hub (16 x 12): blind D-bore on the N10 3 mm D-shaft (the flat drives, the blind end stops it
    axially), O-ring groove inboard between 8 mm flanges, a 14 mm tyre seat with a raised 7 mm crown that holds the F1
    tyre, a 6.5 mm outer lip; M2 grub into a captive nut slot on the flat."""
    from shapely.geometry import Point, Polygon
    # STEP RV21, except: groove flanges 0.7 thick (STEP 0.5, under the 0.63 printable floor) with the groove narrowed
    # symmetrically to 1.1 (the 1.0 O-ring still seats, centre unchanged), and a 0.4 flat on the outer lip (the STEP
    # lip runs out to a knife edge that prints as a ragged single line)
    prof = RH_PROF
    if s < 0:
        prof = [(-x, r) for x, r in prof]
    body = _revolve_x(prof, s * HUB_X0, (RY, RZ))
    # D outline: R1.6 arc under a flat 0.9 above the axis; the flat carries vertices every 0.1 mm so it stays a facet
    # strip (a two-vertex chord reads as round to section probes); a 0.02 crown keeps the facets from being merged
    fa = math.degrees(math.asin(RH_FLAT / RH_DR))
    hx = RH_DR * math.cos(math.radians(fa))
    n1 = RH_NARC - 1
    arc = [(RY + RH_DR * math.cos(math.radians(180.0 - fa + (180.0 + 2 * fa) * k / n1)),
            RZ + RH_DR * math.sin(math.radians(180.0 - fa + (180.0 + 2 * fa) * k / n1))) for k in range(RH_NARC)]
    d = Polygon(arc + [(RY + hx - 2 * hx * k / RH_NFLAT, RZ + RH_FLAT - RH_CROWN * math.sin(math.pi * k / RH_NFLAT)) for k in range(1, RH_NFLAT - 1)])   # 0.02 crown: no face merge
    # blind D-bore (flat 0.9 above the axis); an M2 nut slot open at the inner face (STEP: 4.1 x 2, AF 4 nut + 0.1);
    # the M2 grub threads the nut down onto the flat. Its hole is cut by robot.cad.holes as a tapped (1.6) bore so it
    # stays inside the 1.9 mm tyre-seat flat (a 2.4 clearance hole breaks into both 45 deg ramps as knife edges);
    # the grub is a set screw, so it gets no spec fastener (no head to seat)
    from robot.cad.holes import hole_tool
    top = RH_SEAT_R   # tyre-seat radius at the grub
    grub, _rec = hole_tool((s * RH_GRUB_X, RY, RZ + top), RH_GRUB_DIR, RH_GRUB, head="cap", into="tapped", side="thread", engage=top - RH_FLAT)   # tip 0.4 past the flat: breaks cleanly into the bore (STEP: through)
    slot = _box(s * RH_X_IN, s * RH_X_OUT, RY - RH_SLOT_HW, RY + RH_SLOT_HW, RZ + RH_SLOT_Z[0], RZ + RH_SLOT_Z[1])
    return _S(body, _ext(d, "yz", s * RH_X_IN, s * RH_X_OUT), slot, grub)


def front_hub(s):
    """RV19 micro hub (9 x 9) running on the 25 mm standoff: 6 mm tyre seat between two 9 mm flanges, an O-ring
    groove inboard."""
    # STEP RV19, except all three flanges 0.7 thick (STEP 0.5): the groove flanges grow into the groove (1.1 wide, centre
    # unchanged) and the outer flange stays inside the STEP's X 39.0 (seat 0.2 shorter, parity with the reference gap to the side panel)
    prof = FH_PROF
    if s < 0:
        prof = [(-x, r) for x, r in prof]
    return _revolve_x(prof, s * HUB_X0, SA)


def tyre(od, idd, x0, x1, c, shoulder=0.0):
    """Rubber tyre envelope; `shoulder` rounds the tread corners (the F1 tyre's moulded R1.2 shoulders, STEP RV22)."""
    if shoulder <= 0:
        return _S(_cyl(od / 2, x0, x1, c), _cyl(idd / 2, x0 - 1, x1 + 1, c))
    R, rs = od / 2, shoulder
    prof = [(0.0, idd / 2)] + [(rs - rs * math.cos(math.radians(a)), R - rs + rs * math.sin(math.radians(a))) for a in range(0, 91, 10)]
    prof += [(x1 - x0 - rs + rs * math.cos(math.radians(a)), R - rs + rs * math.sin(math.radians(a))) for a in range(90, -1, -10)]
    prof += [(x1 - x0, idd / 2)]
    return _revolve_x(prof, x0, c)


def standoff(L_x, c):
    return _S(_cyl(SO_R, *L_x, c), _cyl(1.25, L_x[0] - 1, L_x[1] + 1, c))
def wedgelet(s):
    """RV17/18 TPU wedgelet (left built, right mirrored), slabs along X measured on the STEP sections:
    an outer block round the 15 mm standoff end (X 36.5..38.5), a ring step (35.5..36.5), a 2.3 mm ramp skin over a
    hollow whose top edge is capped by a raked plane (29..35.5), the cheek round both standoffs with the fork-tail
    kidney slot (21.5..29) and the 2.5 mm fork slot through it, and a nose tab (17.5..21.5). Ramp face 50 deg:
    Z = 1 + 1.187 (50.1 - Y)."""
    from shapely.geometry import LineString, Point, Polygon
    P = lambda pts: Polygon(pts).buffer(0)  # noqa: E731
    s1 = Point(*SB).buffer(3.5, 64).union(P([(40.5, 1.0), (50.1, 1.0), (42.54, 10.0), (39.55, 10.0), (40.23, 8.0)]))
    s2 = Point(*SB).buffer(3.0, 64).union(P([(40.4, 7.5), (39.55, 10.0), (41.92, 10.0), (42.29, 10.31), (50.1, 1.0), (46.68, 1.0), (44.96, 1.5), (40.5, 1.5)]))
    skin = P([(50.1, 1.0), (47.57, 1.0), (46.8, 1.36), (40.79, 8.52), (40.22, 8.04), (37.65, 15.92)])
    cheek = P([(38.05, 15.36), (50.1, 1.0), (26.55, 1.0), (26.59, 6.09), (26.94, 7.22), (27.48, 8.04), (28.7, 9.02), (30.78, 9.78), (32.43, 10.71),
               (36.62, 14.17), (37.1, 12.78), (38.6, 12.78), (37.79, 15.15)])
    in_slot = P([(38.69, 10.9), (39.12, 11.26), (37.79, 15.15), (38.05, 15.36), (50.1, 1.0), (43.75, 1.0), (43.73, 4.82), (43.37, 6.03), (42.91, 6.68),
                 (41.0, 8.6), (40.03, 8.6), (39.52, 10.07)]).union(Point(*SA).buffer(3.5, 64))
    tab = P([(42.78, 6.82), (44.32, 6.1), (44.69, 7.44), (50.1, 1.0), (43.75, 1.0), (43.71, 4.98), (43.37, 6.03)])
    # the nose tab bears on the weapon mount's nose: take the mount's boss outline (its side profile above the
    # notch-to-nose line) out of the tab in 2D and drop any sliver thinner than a TPU wall, so no film is left
    mprof = _mount_profile("l" if s < 0 else "r").intersection(_mount_clip())
    tab = tab.difference(mprof.buffer(0.1, 32)).buffer(-0.6, join_style=2).buffer(0.6, join_style=2)
    bb = _b()
    sk = _one(_ext(skin, "yz", -35.5, -29.0)).split(bb.Plane(origin=(-34.0, 41.66, 11.06), z_dir=(-1.24, -0.75, 1.0)), keep=bb.Keep.BOTTOM)
    body = _U(_ext(s1, "yz", -38.5, -36.5), _ext(s2, "yz", -36.5, -35.5), sk, _ext(cheek, "yz", -29.0, -21.5), _ext(tab, "yz", -21.5, -17.5) if not tab.is_empty else None)
    kid = LineString([(36.05, 5.15), (36.95, 7.45)]).buffer(0.95, 24)
    cuts = [_ext(cheek.difference(in_slot), "yz", -27.0, -24.5),                  # 2.5 mm fork slot through the cheek
            _cyl(2.6, -39.0, -17.0, SA), _cyl(1.6, -39.0, -17.0, SB), _cyl(2.5, -36.5, -17.0, SB), _ext(kid, "yz", -29.5, -21.0)]
    # TPU cannot print the ramp's knife toe: keep the 50.1 reach but stand the toe on a 0.85 mm land (2 perimeters),
    # the ramp face running parallel to the measured one from there
    toe = P([(48.6, 1.0), (50.1, 1.0), (50.1, 1.0 + WEDGE_TOE_H), (48.6, 1.0 + 1.5 * 1.187)])
    body = _U(body, _I(_ext(toe, "yz", -38.5, -17.5), _ext(s1.union(cheek).union(tab).buffer(0.01), "yz", -38.5, -17.5)))
    sh = _S(body, *cuts)
    sh = sh if s < 0 else _mirror_x(sh)
    # the STEP leaves the fork tine and the mount boss inside the TPU nose; cut their seats (the tine slides into a
    # 1.5 mm slit, the TPU nose tab bears on the mount)
    # the nose tab grazes the chassis lug by 0.1 mm: take the chassis out of it (a printed TPU nose conforms)
    return _S(sh, _fork_slot(s), weapon_mount("l" if s < 0 else "r"), chassis())


def _sp_path(z):
    """Inner face path (X, Y) of the side wall at height z."""
    ks = sorted(SW_X)
    sw = [_interp(z, ks, [SW_X[k][i] for k in ks]) for i in range(len(SW_Y))]
    return SP_IN[:9] + list(zip(sw, SW_Y))


def _sp_w(y, z):
    r, m, w = (_interp(z, SP_W_Z, t) for t in (SP_W_REAR, SP_W_MID, SP_W_SWING))
    # STEP RV23: the outer face swells 0.7 mm round the nut lobe (Y -11..1) at Z 4..12 (outer X -35.3 at Y -5 vs -34.5 at Y 5, Z 7.5)
    bump = SPW_BUMP * max(0.0, 1.0 - abs(y - SPW_BUMP_YC) / SPW_BUMP_YH) * max(0.0, 1.0 - abs(z - SPW_BUMP_ZC) / SPW_BUMP_ZH)
    return _interp(y, SPW_Y, (r, m, m, w)) + bump


def side_panel(s):
    """RV23/24 TPU side panel: an S-wall that hugs the chassis side, swings out round the rear wheel and the front
    wheel; its outer face is battered (5 mm at the floor, 2 mm at the top) so side hits ride up; the nose block
    takes the standoff ends (M3x8 CSK, flush)."""
    from shapely.geometry import LineString, Point, Polygon
    b = _b()
    # the battered, leaning wall is one smooth (non-ruled) loft through six band sections floor -> top: the inner face
    # path leans out in the front swing and the thickness thins with height (outer face battered), all as smooth
    # functions of Z so the outer surface has no steps.
    secs = []
    # the floor section is repeated SP_FOOT_LAND higher: the wall rises straight for that height before it leans, so
    # the leaning outer face meets the floor in a printable 0.85 mm land, not a knife edge
    for zw, z in [(SP_W_Z[0], SP_W_Z[0]), (SP_W_Z[0], SP_W_Z[0] + SP_FOOT_LAND)] + [(q, q) for q in SP_W_Z[1:]]:
        path = _resample(_pchip_open(_sp_path(zw), 400), 240)
        out = _offset_var(path, [_sp_w(y, zw) for _, y in path])
        ring = path + _end_cap(path[-1], out[-1], path[-2]) + out[::-1] + _end_cap(out[0], path[0], path[1])
        # drop the little loops a variable offset makes inside tight bends, round what is left (r 0.6), then
        # resample the outline to 480 points from the inner rear corner so every section's points correspond
        poly = Polygon(ring).buffer(0)
        poly = max(getattr(poly, "geoms", [poly]), key=lambda g: g.area).buffer(0.6, 16).buffer(-0.6, 16)
        rg = list(poly.exterior.coords)[:-1]
        if not poly.exterior.is_ccw:
            rg = rg[::-1]
        k = min(range(len(rg)), key=lambda i: math.dist(rg[i], path[0]))
        rg = rg[k:] + rg[:k] + [rg[k]]
        pts = _resample(rg, 481)[:-1]
        # (dense polygon sections: one ruling per matched point pair, adjacent facets meet at a fraction of a degree)
        secs.append(b.Wire.make_polygon([b.Vector(x, y, z) for x, y in pts], close=True))
    wall = _U(b.Solid.make_loft(secs[:2], ruled=True), b.Solid.make_loft(secs[1:], ruled=False))
    side = _round(Polygon([(-32.9, 1.0), (-32.9, 16.0), (-6.7, 16.0), (14.6, 12.0), (19.3, 11.0), (24.0, 10.0), (42.0, 10.0), (50.1, 1.0)]), r_out=1.5)
    side = side.union(Point(-32.2, 9.7).buffer(8.2, 64))                           # rear end a full round over the wheel
    foot = _ext(_poly([(-31.6, -12.0), (-42.0, -11.9), (-40.6, -2.1), (-40.8, 3.3), (-42.9, 13.3), (-31.6, 13.3)]), "xy", 1.0, 2.0)   # 1 mm wide foot under the chassis lobe
    wall = _I(wall, _ext(side, "yz", -60.0, -20.0))
    SIDE_WALL_DEBUG.append(wall)
    nose_plan = _round(Polygon([(-52.1, 26.5), (-51.7, 39.7), (-50.5, 43.0), (-48.4, 45.7), (-45.6, 47.9), (-42.0, 49.6), (-40.0, 50.1), (-38.5, 50.1),
                                (-38.5, 37.6), (-41.6, 37.6), (-42.4, 37.3), (-42.3, 34.9), (-40.5, 34.5), (-40.5, 26.5)]), r_out=0.5)
    batter = _ext(_poly([(-52.06, 1.0), (-52.06 + 0.84 * 15, 16.0), (0.0, 16.0), (0.0, 1.0), (-52.06, -5.0)]), "xz", 0.0, 60.0)   # outer face leans in 38 deg
    nose = _I(_I(_ext(nose_plan, "xy", 1.0, 10.0), _ext(side, "yz", -60.0, -20.0)), batter)
    # the nose top continues the wedgelet's 50 deg ramp (Z = 1 + 1.187 (50.1 - Y)) so a wedge rides up both as one face
    nose = _one(nose).split(b.Plane(origin=(0.0, 50.1, 1.0), z_dir=(0.0, 1.187, 1.0)), keep=b.Keep.BOTTOM)
    # like the wedgelet, the ramp's knife toe stands on a 0.85 mm land at full reach (printable TPU)
    toe = _poly([(47.0, 1.0), (50.1, 1.0), (50.1, 1.0 + WEDGE_TOE_H), (47.0, 1.0 + 3.1 * 1.187)])
    nose = _U(nose, _I(_I(_ext(nose_plan, "xy", 1.0, 10.0), _ext(toe, "yz", -60.0, -20.0)), batter))
    # the nose's front-outer corner is chamfered back (a plane leaning ~55 deg in and ~57 deg back) so a wedge or
    # spinner tooth coming in from the front quarter glances off instead of catching the corner
    nose = _one(nose).split(b.Plane(origin=(-120.0, 0.0, 0.0), z_dir=(1.0, -1.525, -1.4725)), keep=b.Keep.TOP)
    nose = _S(nose, _ext(_poly([(26.5, 3.0), (37.0, 3.0), (37.7, 6.6), (39.0, 10.5), (26.5, 10.5)]), "yz", -42.0, -38.4))   # hollow behind the nose wall (its front face leans back with the wall)
    boss = _I(_cyl(3.0, -42.5, -39.5, SA), _ext(side, "yz", -60.0, -20.0))         # standoff end boss
    body = _U(wall, nose, foot, boss)
    # M3 CSK seats (ISO 10642 head 6.6, +0.1 clearance) with a 12 mm head bore out through the battered outer face, so a
    # driver reaches the head and the screw backs straight out
    cuts = [_csk(3.3, 6.7, (-46.26, SA[0], SA[1]), "x", 1, 8.0, 12.0), _csk(3.3, 6.7, (-41.76, SB[0], SB[1]), "x", 1, 8.0, 12.0),
            _csk(3.3, 6.7, (-35.26, NUT[0], NUT[1]), "x", 1, 8.0, 12.0),
            _cyl(2.55, -42.55, -38.0, SA),
            _box(-45.0, -43.4, -38.7, -24.8, 5.5, 14.5),                          # rear tyre relief on the inner face
            _ext(_poly([(-11.7, 3.8), (0.5, 4.7), (2.3, 5.7), (2.3, 8.3), (0.5, 9.3), (-3.5, 11.0), (-9.5, 13.0), (-11.7, 13.8)]), "yz", -32.5, -31.4)]    # 1 mm relief round the chassis nut lobe: STEP RV23 diamond (Y -11.7..2.3, Z 3.8..13.8, sloping top-right edge)
    for y0 in (-11.0, -4.5, 2.0):     # diagonal vent slots (TPU wall flexes, keeps the ESC cool)
        sl = LineString([(y0, 5.0), (y0 + 5.0, 11.0)]).buffer(1.0, cap_style=1)
        cuts.append(_ext(sl, "yz", -50.0, -36.5))
    sh = _S(body, *cuts)
    sh = sh if s < 0 else _mirror_x(sh)
    # RVRN 2.0 parity: the STEP side panel has a plain inner face (no belt channel); the O-ring grazes it
    return sh
