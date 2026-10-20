"""[fix-S] Weapon module: mounts, spider, discs, spacers, motor back spacer, stator / stack holes."""
import json, math, os, sys
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403


def _mount_clip():
    """Region above the line from the notch top to the nose (the battered boss) as a polygon."""
    return Polygon_([(TAB["y0"], MNT_TOP_Z), (BOSS_NOSE_Y, BOSS_Z), (BIG, BOSS_Z), (BIG, BIG), (0, BIG), (0, MNT_TOP_Z)])


def _mount_profile(side):
    """Weapon mount side profile (Y, Z): a teardrop round the weapon axis (R top_r) running down to the standoffs,
    with the notch that drops over the chassis tab (open to the rear)."""
    m, t = MNT_SIDE[side], TAB
    c = (WY, WZ)
    t0 = _tangent_line_circle((m["notch_y"], MNT_TOP_Z), c, m["top_r"], upper=True)
    a0 = math.degrees(math.atan2(t0[1] - c[1], t0[0] - c[0]))
    rim = _arc(c, m["top_r"], a0, m["rim_end"], WSEG_ARC)
    nose = _arc(SB, NOSE_R, NOSE_A0, -90.0, WSEG_ARC_S)
    zt = t["z0"] + t["h"]
    heel = [(t["y0"] + MNT_HEEL["step"], MNT_HEEL["z"]), (t["y0"] - MNT_HEEL["back"], MNT_HEEL["z_hook"]), (t["y0"] - MNT_HEEL["back"], MNT_HEEL["z_lip"]), (t["y0"], MNT_HEEL["z_lip"])]
    # notch front face on the lug (0 gap): the lug bears a hit before the screws
    notch = [(t["y0"], t["z0"]), (t["y1"] - t["cham"], t["z0"]), (t["y1"], t["z0"] + t["cham"]), (t["y1"], zt - t["cham"]), (t["y1"] - t["cham"], zt), (t["y0"], zt),
             (t["y0"], MNT_TOP_Z - MNT_NOTCH_UP), (t["y0"] - MNT_NOTCH_UP, MNT_TOP_Z), (m["notch_y"], MNT_TOP_Z)]
    p = _poly(rim + [nose[0]] + nose[1:] + heel + notch)
    # the nose CSK (DIN 7991 cone) is wider than the STEP's nose arc and left a 0 mm knife edge there: a local pad
    # (CSK radius + printed wall), kept above the nose underside, wraps the countersink
    from shapely.geometry import Point, box as _sbox
    p = p.union(Point(SB).buffer(NOSE_PAD_R, WSEG_HI).intersection(_sbox(0, MNT_HEEL["z"], BIG + 20, BIG - 20)))
    return _round(p, r_out=0.0, r_in=MNT_RELIEF_R)


def weapon_mount(side):
    """RV02 (left, shaft end) / RV03 (right, stator): 8 mm printed XALT HD plates. A 4 mm slab carries the full
    profile; the outer 4 mm is a boss above the standoff line whose outer face is battered (leans in 7.7 deg) so side
    hits glance off. The rear notch drops over the chassis tab: the tab, not the screws, takes fore/aft load."""
    m = MNT_SIDE[side]
    s = 1 if side == "r" else -1
    prof = _mount_profile(side)
    xi, xm, xo = s * MNT_IN, s * MNT_SLAB, s * MNT_OUT
    eps = m["slab_eps"]                          # RV03's STEP slab face sits just inside the slab plane, RV02's on it
    slab = _ext(prof, "yz", xi, xm - s * eps)
    bp = prof.intersection(_mount_clip())         # boss: the profile above the line from the notch top to the nose
    boss = _ext(bp, "yz", xm - s * eps, xo + s * BOSS_OVER)
    a_, kz, ky = m["face"]                        # outer battered face (STEP): one plane leaning in with height and towards the nose
    bb = _b()
    boss = _one(boss).split(bb.Plane(origin=(s * a_, 0.0, 0.0), z_dir=(s * 1.0, ky, kz)), keep=bb.Keep.BOTTOM)
    body = _U(slab, boss)
    cuts = []
    axis = (WY, WZ)
    if side == "r":
        cuts.append(_cyl(SHAFT_D / 2 + SHAFT_CLR, -BIG / 2, BIG / 2, axis))          # shaft end clearance
        for dy, dz in _polar(STATOR_PCD / 2, 4, 0.0):                                # GR1507 stator M2 on its bolt circle
            cuts.append(_stator_hole(s, dy, dz)[0])
    else:
        cuts.append(_cyl(BRG_SEAT_R, -BIG / 2, BIG / 2, axis))                        # outboard bearing seat
        cuts.append(_cyl(NUT_RECESS_R, xm, xo + s, axis))                             # shaft nut recess
    for (y, z), fastener in zip((SA, SB), MNT_SCREW):                                 # M3 CSK into the standoffs, flush inside
        cuts.append(_mount_csk(s, y, z, fastener)[0])
    return _S(body, *cuts)


def _mount_csk(s, y, z, fastener):
    """robot.cad.holes cutter + record for a mount-to-standoff M3 CSK (bolt_u*): head flush in the inner face, DIN 7991
    countersink (dk 6.0 head in the STEP's 6.2 mm cone) and ISO 273 normal 3.4
    clearance through the 4 mm slab, so the notch, not the shank, takes fore/aft load."""
    _repo = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
    if _repo not in sys.path:
        sys.path.insert(0, _repo)
    from robot.cad.holes import hole_tool
    return hole_tool((s * MNT_IN, y, z), (s, 0, 0), fastener, head="csk", into="through", side="head", grip=MNT_SLAB - MNT_IN, fit="normal", csk_clear=0.2)


def _stator_hole(s, dy, dz):
    """robot.cad.holes cutter + record for one RV03 stator screw (bolt_wm*): M2x8 button, head on the counterbore floor."""
    _repo = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
    if _repo not in sys.path:
        sys.path.insert(0, _repo)
    from robot.cad.holes import hole_tool
    from robot.cad import fastener_catalog as fc
    y, z = WY + dy, WZ + dz
    a_, kz, ky = MNT_SIDE["r"]["face"]
    face = a_ - kz * z - ky * y + HOLE_FACE_RISE * math.hypot(kz, ky)   # RV03 battered outer face |X| (STEP plane, see weapon_mount)
    depth = face - CB_CONE_X[1]                     # counterbore down to the STEP floor
    cut, rec = hole_tool((s * face, y, z), (-s, 0, 0), "M2x8", head="button", into="through", side="head",
                         grip=face - MNT_IN, cbore=depth, cbore_clear=2 * CB_R - fc.head(2.0, "button")[0], fit="normal")
    return _one(cut.solids()[0] if hasattr(cut, "solids") and len(cut.solids()) == 1 else cut), rec


def _stack_hole(fastener, x, y, z, sx, grip):
    """robot.cad.holes record of an M2 button screw on the weapon axis direction sx: clearance through `grip` mm, tapped beyond."""
    _m2()   # puts the repo on sys.path
    from robot.cad.holes import hole_tool
    return hole_tool((x, y, z), (sx, 0, 0), fastener, head="button", into="tapped", side="both", grip=grip, fit="close")[1]


def motor_back_spacer():
    """1.5 mm printed spacer between the GR1507 stator base and RV03: clears the motor's rear bearing boss and wires."""
    from shapely.geometry import Point
    c, b = (WY, WZ), BSP
    p = Point(c).buffer(b["r"], WSEG_HI).difference(Point(c).buffer(b["bore_r"], WSEG_MID))
    p = _ring_windows(p, c, b["win_in"], b["win_out"], b["half_deg"], b["phase"], b["win_round"])   # STEP windows (measured)
    for dy, dz in _polar(STATOR_PCD / 2, 4, 0.0):
        p = p.difference(Point(WY + dy, WZ + dz).buffer(b["hole_r"], WSEG_LO))
    return _ext(p, "yz", *BSP_X)


# ------------------------------------------------------------------------------------------------------------ drisk
def _disc_local(u, v):
    """Drisk-local (u, v) -> world (Y, Z): STEP Drisk_V4 rotation about the axis, then the ref -> world map."""
    a = math.radians(DR_ROT)
    xr = u * math.cos(a) - v * math.sin(a) - 38.5
    yr = u * math.sin(a) + v * math.cos(a) + 23.5
    return (-xr, yr)


def _to_world_poly(p):
    from shapely.geometry import Polygon
    ext = [_disc_local(u, v) for u, v in list(p.exterior.coords)]
    ints = [[_disc_local(u, v) for u, v in list(i.coords)] for i in p.interiors]
    return Polygon(ext, ints).buffer(0)


def disc_outline():
    """Single-tooth eccentric disc (local frame): rim R16.5 centred 0.5 mm off towards -40 deg so the rim mass
    balances the tooth; the tooth leaves the rim with a straight leading flank to R23 at 134.8 deg, and its back face
    drops back to the rim; the root is filleted."""
    from shapely.geometry import Point, Polygon
    ea = math.radians(DISC_ECC_A)
    rim = Point(DISC_ECC * math.cos(ea), DISC_ECC * math.sin(ea)).buffer(DISC_R, WSEG_MAX)
    ta = math.radians(TOOTH_A)
    tip = (TOOTH_R * math.cos(ta), TOOTH_R * math.sin(ta))
    tooth = Polygon([tip] + TOOTH_PTS)
    return _round(rim.union(tooth), **DISC_ROUND)


def floating_disc():
    from shapely.geometry import MultiPoint, Point, Polygon
    p = disc_outline()
    d = DOG

    def r_bore(a):   # bore with 4 ramped drive dogs
        t = a % (360.0 / N_STACK)
        return d["r"] + (d["rise"] * (t - d["t0"]) / (d["t1"] - d["t0"]) if d["t0"] <= t < d["t1"] else d["rise"] * (d["t2"] - t) / (d["t2"] - d["t1"]) if d["t1"] <= t < d["t2"] else 0.0)
    steps = DISC_BORE_RES * 360
    bore = Polygon([(r_bore(a / DISC_BORE_RES) * math.cos(math.radians(a / DISC_BORE_RES)), r_bore(a / DISC_BORE_RES) * math.sin(math.radians(a / DISC_BORE_RES))) for a in range(steps)])
    bore = _round(bore, r_out=DISC_BORE_ROUND, r_in=DISC_BORE_ROUND)
    p = p.difference(bore)
    for c in _polar(BOLT_R):
        p = p.difference(Point(*c).buffer(_m2()[1], WSEG_FINE))
    # balance window by the tooth (STEP): a rounded triangle, the hull of three corner radii
    p = p.difference(MultiPoint(DISC_BAL_PTS).buffer(DISC_HOLE_R_WIN, WSEG_FINE).convex_hull)
    return p


def disc(which):
    x0, x1 = DR_X[which]
    return _ext(_to_world_poly(floating_disc()), "yz", x0, x1)


def spider():
    """3 mm aluminium spider on the GR1507 bell: bore on the shaft collar, 4 M2 on r4.5 into the bell, 4 lobes
    with the r14 stack bolts, 4 quarter windows."""
    from shapely.geometry import Point, Polygon
    sp = SPIDER
    p = Point(0, 0).buffer(sp["r"], WSEG_MAX)
    for c in _polar(BOLT_R):
        p = p.union(Point(*c).buffer(sp["lobe_r"], WSEG_MID))
    p = _round(p, r_in=sp["round_in"])
    o, f = sp["win_off"], sp["win_far"]
    for sx in (1, -1):
        for sy in (1, -1):
            q = Point(0, 0).buffer(sp["win_r"], WSEG_FN).intersection(Polygon([(sx * o, sy * o), (sx * f, sy * o), (sx * f, sy * f), (sx * o, sy * f)]))
            q = q.difference(Point(0, 0).buffer(sp["hub_r"], WSEG_HI))   # hub ring round the 4 bell screws
            p = p.difference(_round(q, r_out=sp["win_round"]))
    p = p.difference(Point(0, 0).buffer(sp["bore_r"], WSEG_MID))
    tap_r, clr_r, _ = _m2()
    for r, hr in ((HUB_R, clr_r), (BOLT_R, tap_r)):   # r14: M2 tap drill (the stack screws thread in), r4.5: clearance
        for c in _polar(r):
            p = p.difference(Point(*c).buffer(hr, WSEG_FINE))
    return _ext(_to_world_poly(p), "yz", *DR_X["spider"])


def drisk_spacer():
    """6 mm printed spacer between the discs: bore round the bell, 4 bolt holes, 4 arc windows (STEP, measured)."""
    from shapely.geometry import Point
    sp, c = SPACER, (0, 0)
    p = Point(c).buffer(sp["r"], WSEG_MAX).difference(Point(c).buffer(sp["bore_r"], WSEG_FN))
    p = _ring_windows(p, c, sp["win_in"], sp["win_out"], sp["half_deg"], sp["phase"], sp["win_round"], WSEG_MAX)
    for pt in _polar(BOLT_R):
        p = p.difference(Point(*pt).buffer(_m2()[1], WSEG_FINE))
    return _ext(_to_world_poly(p), "yz", *DR_X["spacer"])
