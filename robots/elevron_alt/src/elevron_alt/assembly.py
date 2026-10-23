"""Part table and the model-file entry point build(). Custom parts are drawn in the STEP frame and lifted by
FLOOR_LIFT into the robot world (floor at z 0). Revron parts that are the same bought or printed part in the Alt
(RV21 hub, RV22 tyre, Drisk_floating_3 disc, the spider) come from the revron package unchanged and are only
re-placed here."""
import os
import sys

import build123d as bd

from robocad.geom import _cyl, _S, _U, _I, _box, _solid
from . import chassis as ch, side_panel as sp, vert_mod as vm
from .fasteners import cutters
from .params_chassis import HX, CORNER_R, REBATE, POSTS, END_POSTS, TAP_D, WALL, AXLE_Z, AXLE_Y, IN_X, KEY_R, HOLE_D
from .params_drive import DISC_PHASE, FLOOR_LIFT, HUB_X0, TYRE_X0, WY, WZ, DISC_X, SPIDER_X, PROP_X0, PROP_LEN, PROP_FLANGE_X1, SHAFT_D, MOTOR_BASE_X, BASE_SKIN, BRG, BRG_X0, UP_IN, UP_T, HUB_LEN
from .params_hw import BASE_T, BASE_CSK_D, SO_LEN, SO_D, PLATE_W, PLATE_H, BACK_T, FRONT_T, PROP_D, FH_CLR, FRONT_HUB_TRIM

_REVRON_SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "..", "revron", "src"))
if _REVRON_SRC not in sys.path:
    sys.path.insert(0, _REVRON_SRC)


def _lift(s):
    """STEP frame -> robot world."""
    return s.moved(bd.Location((0, 0, FLOOR_LIFT)))


def base_panel():
    """1 mm panel in the chassis rebate, an M2 clearance hole under every screw column (fasteners table)."""
    p = _box(-(HX - REBATE), HX - REBATE, -(ch.HY - REBATE), ch.HY - REBATE, WALL - BASE_T, WALL)
    for sx in (-1, 1):   # front corners round with the rebate's (concentric with Fillet1)
        cx, cy = sx * (HX - CORNER_R), -(ch.HY - CORNER_R)
        p = _S(p, _S(_box(cx, cx + sx * CORNER_R, cy, cy - CORNER_R, WALL - BASE_T - 1, WALL + 1), _cyl(CORNER_R - REBATE, WALL - BASE_T - 1, WALL + 1, (cx, cy), "z")))
    return _S(p, cutters("base_panel"))


def _revron_wheel(kind):
    from revron import hubs
    return {"hub": hubs.rear_hub, "tyre": hubs.rear_tyre}[kind]()


def wheel_part(kind, sx, y):
    """RV21 hub / RV22 tyre (Revron frame: axis +X, inner face x = 0) on the axle line y, side sx (STEP frame).
    Front hubs idle on the 10 mm standoff: the D-bore is opened round it."""
    s = _revron_wheel("hub" if kind != "tyre" else "tyre")
    if kind == "front_hub":   # an idler: no grub (its nut slot and bore filled), bore opened round the standoff, inner end trimmed clear of the FRONT_PLATE
        from revron import hubs
        s = _U(s, _I(hubs._spin(hubs._rear_profile()), _U(hubs._nut_slot(), hubs._grub())))
        s = _S(s, _cyl(SO_D / 2 + FH_CLR, -1, HUB_LEN + 1, (0, 0), "x"), _cyl(HUB_LEN, -1, FRONT_HUB_TRIM, (0, 0), "x"))
    x0 = HUB_X0 if kind != "tyre" else TYRE_X0
    s = s.moved(bd.Location((x0, y, AXLE_Z)))
    return s if sx > 0 else s.mirror(bd.Plane.YZ)


def _weapon_plate(name, x_span):
    """Revron Drisk plate (drawn on the Revron spin axis) moved onto the Alt axis at x_span."""
    from revron import drisk
    from revron.params import DR_X, WY as R_WY, WZ as R_WZ
    s = drisk.disc(name) if name.startswith("disc") else drisk.spider()
    s = s.moved(bd.Location((x_span[0] - min(DR_X[name]), WY - R_WY, WZ - R_WZ)))
    return s.rotate(bd.Axis((0, WY, WZ), (1, 0, 0)), DISC_PHASE)   # the tooth where the STEP has it (the joint's 0)


def prop_mount():
    """RV07 prop mount: flange from the spider to the MF85 flange, bored for the shaft."""
    return _S(_cyl(PROP_D / 2, PROP_X0, PROP_FLANGE_X1, (WY, WZ), "x"), _cyl(SHAFT_D / 2, PROP_X0 - 1, BRG_X0 + 1, (WY, WZ), "x"))


def wshaft():
    """BE1806 shaft from the bell face through disc, spider and prop mount into the MF85 inner race."""
    return _cyl(SHAFT_D / 2, MOTOR_BASE_X + BASE_SKIN, BRG_X0 + BRG[2], (WY, WZ), "x")   # from inside the stator base (its bearings) to the MF85


def bearing():
    return _S(_cyl(BRG[1] / 2, BRG_X0, BRG_X0 + BRG[2], (WY, WZ), "x"), _cyl(BRG[0] / 2, BRG_X0 - 1, BRG_X0 + BRG[2] + 1, (WY, WZ), "x"))


def standoff(sx):
    """10 mm M3 aluminium standoff: the front axle, clamped against the outer wall face through the keyhole."""
    x0 = HX + FRONT_T
    s = _S(_cyl(SO_D / 2, x0, x0 + SO_LEN, (-AXLE_Y, AXLE_Z), "x"), _cyl(TAP_D / 2, x0 - 1, x0 + SO_LEN + 1, (-AXLE_Y, AXLE_Z), "x"))
    return s if sx > 0 else s.mirror(bd.Plane.YZ)


def axle_plate(sx, which):
    """BACKING_PLATE (inside the wall) / FRONT_PLATE (outside): square plates clamping the standoff across the keyhole."""
    x0, x1 = (IN_X - BACK_T, IN_X) if which == "back" else (HX, HX + FRONT_T)
    h = PLATE_H if which == "back" else PLATE_W
    s = _S(_box(x0, x1, -AXLE_Y - PLATE_W / 2, -AXLE_Y + PLATE_W / 2, AXLE_Z - h / 2, AXLE_Z + h / 2), _cyl(HOLE_D / 2, x0 - 1, x1 + 1, (-AXLE_Y, AXLE_Z), "x"))
    return s if sx > 0 else s.mirror(bd.Plane.YZ)


PARTS = {
    "chassis": ch.chassis, "base_panel": base_panel, "vert_mod": vm.vert_mod,
    "side_r": lambda: sp.side_panel(1), "side_l": lambda: sp.side_panel(-1),
    "disc": lambda: _weapon_plate("disc_a", DISC_X), "spider": lambda: _weapon_plate("spider", SPIDER_X),
    "prop_mount": prop_mount, "wshaft": wshaft, "bearing": bearing,
    "so_l": lambda: standoff(-1), "so_r": lambda: standoff(1),
    "bplate_l": lambda: axle_plate(-1, "back"), "bplate_r": lambda: axle_plate(1, "back"),
    "fplate_l": lambda: axle_plate(-1, "front"), "fplate_r": lambda: axle_plate(1, "front"),
}
for _n, _sx in (("l", -1), ("r", 1)):
    PARTS[f"whub_r{_n}"] = (lambda sx: lambda: wheel_part("rear_hub", sx, AXLE_Y))(_sx)
    PARTS[f"wheel_r{_n}"] = (lambda sx: lambda: wheel_part("tyre", sx, AXLE_Y))(_sx)
    PARTS[f"whub_f{_n}"] = (lambda sx: lambda: wheel_part("front_hub", sx, -AXLE_Y))(_sx)
    PARTS[f"wheel_f{_n}"] = (lambda sx: lambda: wheel_part("tyre", sx, -AXLE_Y))(_sx)


def build(part, origin=None):
    """Model-file entry point: one part in robot-world coordinates (or relative to `origin`, for rotating parts)."""
    s = _lift(_solid(PARTS[part]()))
    if origin:
        s = s.moved(bd.Location(tuple(-float(v) for v in origin)))
    return s
