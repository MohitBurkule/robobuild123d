"""[fix-S] Chassis tub and its panels: chassis, base_panel, top_panel, esc_tray, inserts / panel seats."""
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403
from robot.cad.holes import hole_tool   # the repo root is on the import path (params.py)

SW_PAD_ENGAGE = 3.0   # pad material above the switch screw head seat (M2x3 thread-forming into the 1.7 pilot)


def _switch_hole(yy):
    """robot.cad.holes record for a switch screw: M2x3 button thread-forming up into the 1.7 pilot of the deck pad (3.0 mm of pad above its 16.0 head seat)."""
    return hole_tool((SWX, yy, SW_BOLT_Z), (0, 0, 1), "M2x3", head="button", into="tapped", side="thread", engage=SW_PAD_ENGAGE)


def chassis():
    """RV01 printed chassis, built as the designer's feature tree (see tub2.py)."""
    from .tub2 import chassis2
    return chassis2()


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


def bat_pad():
    """Double-sided foam tape pad between the base panel skin and the pack underside (STEP pack floats 2 mm above the panel):
    it carries the pack and keeps it from sliding on the panel."""
    P = BAT_PAD
    return _box(*P["x"], *P["y"], BASE_Z0 + BASE_T, BAT_Z - BAT_BELOW)
