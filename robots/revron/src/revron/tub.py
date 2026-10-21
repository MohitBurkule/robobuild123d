"""[fix-S] Chassis tub and its panels: chassis, base_panel, top_panel, esc_tray, inserts / panel seats."""
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403
from . import tub_shell, tub_lobes, tub_lugs, tub_front
from .tub_util import rect
from robot.cad.holes import hole_tool   # the repo root is on the import path (params.py)

SW_PAD_ENGAGE = 3.0   # pad material above the switch screw head seat (M2x3 thread-forming into the 1.7 pilot)
SW_PAD = dict(x=(22.5, 27.5), y=(-15.6, 4.4), r=1.5, z0=16.5, fillet=1.5, over=0.5, up=0.1)   # switch pad under the deck (STEP): X / Y span (the +X end is the wall), free corner R, bottom Z, wall fillet R, reach into the wall, reach up into the deck


def _switch_hole(yy):
    """robot.cad.holes record for a switch screw: M2x3 button thread-forming up into the 1.7 pilot of the deck pad (3.0 mm of pad above its 16.0 head seat)."""
    return hole_tool((SWX, yy, SW_BOLT_Z), (0, 0, 1), "M2x3", head="button", into="tapped", side="thread", engage=SW_PAD_ENGAGE)


# ------------------------------------------------------------------------------------------------------------ chassis
def switch_pad(c):
    """Pad under the deck that the switch ears bear on (STEP); +X side only."""
    from shapely.geometry import Point
    P = SW_PAD
    (x0, x1), (y0, y1), f = P["x"], P["y"], P["fillet"]
    plan = _round(rect(x0, x1 + P["over"], y0, y1), r_out=P["r"])
    for yw, d in ((y0, -1), (y1, 1)):   # concave fillet where the pad ends meet the side wall
        q = rect(x1 - f, x1, *sorted((yw, yw + d * f)))
        plan = plan.union(q.difference(Point(x1 - f, yw + d * f).buffer(f, SEG)))
    return _ext(plan, "xy", P["z0"], c["deck"] + P["up"])


def chassis():
    """RV01 printed chassis: a closed-top box printed deck-down, open underneath for the base panel. Composed from the
    per-feature modules: shell (box, columns, deck pockets, base seat), lobes (side lobes with the captive M3 nut),
    lugs (front tabs and standoff lugs), front (corner flanges, rear lattice, wire hole, wall pockets)."""
    c = CH
    adds = tub_shell.additions(c) + tub_lobes.additions(c) + tub_lugs.additions(c) + tub_front.additions(c) + [switch_pad(c)]
    cuts = tub_shell.cuts(c) + tub_lobes.cuts(c) + tub_lugs.cuts(c) + tub_front.cuts(c)
    body = _U(tub_shell.shell(c), *adds)
    tub = _S(tub_lobes.root_fillet(body, c), *cuts)
    assert len(tub.solids()) == 1 and tub.volume > CHASSIS_MIN_VOL, f"chassis boolean collapsed: {len(tub.solids())} solids, {tub.volume:.0f} mm3"
    return tub


def esc_tray():
    """TPU tray glued to the base panel under the weapon ESC (not in the STEP, where kapton alone holds it): two rails carry
    the board 0.1 mm off, 1 mm lips 0.1 mm off its -x / +x / +y sides (leads leave above the lips at the board mid-plane).
    Lips on all four sides (the cage rib no longer exists) and the Malenki above it +z, so the ESC cannot rattle inverted; base panel off, it lifts out."""
    (wx0, wx1), (wy0, wy1), wz0 = WE_X, WE_Y, WE_Z[0]
    T = ESC_TRAY
    g, w, e = T["gap"], T["wall"], T["fuse"]
    z0, top = BASE_Z0 + BASE_T, wz0 + T["lip"]   # sits on the base panel top face; lips rise 1 mm past the board underside
    zw = z0 + w - e
    parts = [_box(wx0 - g - w, wx1 + g + w, wy0 - g - w, wy1 + g + w, z0, z0 + w)]
    parts += [_box(xa, xa + w, wy0 + T["rail_end"], wy1 - T["rail_end"], zw, wz0 - g) for xa in (wx0 + T["rail_x"][0], wx1 - T["rail_x"][1])]
    parts += [_box(wx0 - g - w, wx0 - g, wy0, wy1 + g + w, zw, top), _box(wx1 + g, wx1 + g + w, wy0, wy1 + g + w, zw, top),
              _box(wx0 - g - w, wx1 + g + w, wy1 + g, wy1 + g + w, zw, top),
              _box(wx0 - g - w, wx1 + g + w, wy0 - g - w, wy0 - g, zw, top)]   # closing -y lip: the removed cage rib no longer holds that side
    return _U(*parts)
