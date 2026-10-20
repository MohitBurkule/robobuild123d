"""[fix-B] Drisk: spider, floating Hardox discs, spacer."""
import json, math, os, sys
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403


# ------------------------------------------------------------------------------------------------------------ drisk
def _disc_local(u, v):
    """Drisk-local (u, v) -> world (Y, Z): STEP Drisk_V4 rotation about the axis, then the ref -> world map."""
    a = math.radians(DR_ROT)
    xr = u * math.cos(a) - v * math.sin(a) - WY
    yr = u * math.sin(a) + v * math.cos(a) + WZ
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
