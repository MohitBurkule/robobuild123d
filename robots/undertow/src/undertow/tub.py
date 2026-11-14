"""TPU tub: the shock-absorbing unibody. One quadrant is not needed for the outline (a rounded rectangle is already
symmetric); the wheel wells, motor bays and bolt columns are built for one corner and mirrored.
UNTESTED: never built, run, rendered or verified.

Printed open-top / open-bottom (print orientation +Z, no supports: every pocket is swept to the top face by derive_bay).
Load paths: a front push goes pin -> cheeks -> tub front wall -> motor plate stacks (pocket walls) -> wheels -> floor.
A side hit goes skirt -> flank V-face -> outer wall -> the wheel-well side walls and the M2 standoffs into both plates
(the plates are the stiff skin, the TPU between them is the spring). The battery, ESC, receiver, switch and every wire
are inside the wall line and under the plates: no attack reaches them without first going through 2.4 mm TPU + a plate.
"""
import build123d as bd

from robot import catalog
from robot.cad.bay import derive_bay

from revron.plate import round_corners   # robots/revron/src/revron/plate.py: 2D corner fillets of a sketch face

from . import drive
from .params import (HALF_W_TUB, HALF_L_TUB, CORNER_R, Z_TUB0, TUB_H, WELL, BOLT_SITES_Q, BOLT_SITES_MID, STANDOFF_D,
                     BATTERY_ID, ESC_ID, RX_ID, SWITCH_ID, BAT_Y, ESC_Y, RX_X, SWITCH_X, SWITCH_Y, Z_BAY, FLANK_DEG, WALL,
                     SKIRT_PIN_Z, SKIRT_PIN_D, CHEEK_T, CHEEK_HALF_X, CHEEK_REACH, PIN_Y, PIN_Z, EYE_R, PIN_CLEAR)
import math


def outline():
    """Plan outline, centred: a rounded rectangle (convex corners CORNER_R)."""
    return bd.RectangleRounded(2 * HALF_W_TUB, 2 * HALF_L_TUB, CORNER_R)


def _body():
    return bd.Pos(0, 0, Z_TUB0) * bd.extrude(outline(), TUB_H)


def _flank_cut():
    """The V flank on the sides and rear: the faces above and below the skirt hinge lean FLANK_DEG in, so a skirt
    swung in rests sloped outward on whichever face is down (and a spinner tooth meets a slope, not a step)."""
    inset = (TUB_H / 2) * math.tan(math.radians(FLANK_DEG))
    dz = SKIRT_PIN_Z - Z_TUB0
    # side profile in XZ, extruded along Y over the whole tub; mirrored to -X
    tri = [(HALF_W_TUB + 0.1, Z_TUB0 - 0.1), (HALF_W_TUB - inset, Z_TUB0 - 0.1), (HALF_W_TUB + 0.1, Z_TUB0 + dz)]
    lo = bd.extrude(bd.Plane.XZ * bd.Polygon(*tri, align=None), HALF_L_TUB, both=True)
    hi = lo.mirror(bd.Plane.XY.offset(SKIRT_PIN_Z))
    side = lo + hi
    return side + side.mirror(bd.Plane.YZ)


def _hinge_bore():
    """Skirt hinge-pin bore along Y in each side wall at the mid-plane (pin inside the wall: the knuckles sit in slots)."""
    x = HALF_W_TUB - WALL / 2
    c = bd.Pos(x, 0, SKIRT_PIN_Z) * bd.Rot(90, 0, 0) * bd.Cylinder(SKIRT_PIN_D / 2 + 0.1, 2 * HALF_L_TUB)
    return c + c.mirror(bd.Plane.YZ)


def _wells():
    """Wheel wells, one corner then mirrored: open through the full height (tyres stand proud of both plates)."""
    w = bd.Pos((WELL["x0"] + WELL["x1"]) / 2, (WELL["y0"] + WELL["y1"]) / 2, Z_TUB0 + TUB_H / 2) * bd.Box(
        WELL["x1"] - WELL["x0"], WELL["y1"] - WELL["y0"], TUB_H + 1)
    w = w + w.mirror(bd.Plane.YZ)
    return w + w.mirror(bd.Plane.XZ)


def _bays():
    """Every COTS pocket from robot/cad/bay.py:derive_bay, dropped in from the top face (insert -z)."""
    cuts = [drive.motor_bay(sx, sy).cut_solid() for sx, sy in drive.QUADRANTS]
    for cid, at in ((BATTERY_ID, (0, BAT_Y, Z_BAY)), (ESC_ID, (0, ESC_Y, Z_BAY)), (RX_ID, (RX_X, ESC_Y, Z_BAY)),
                    (SWITCH_ID, (SWITCH_X, SWITCH_Y, Z_BAY))):
        if cid is None:
            continue
        cuts.append(derive_bay(catalog.find(cid), placement=bd.Pos(*at), insert_dir="-z").cut_solid())
    out = cuts[0]
    for c in cuts[1:]:
        out = out + c
    return out


def _standoff_bores():
    """Columns for the M2 aluminium standoffs: GridLocations-free because the sites are mirrored relations, not a grid."""
    pts = [(sx * x, sy * y) for x, y in BOLT_SITES_Q for sx in (1, -1) for sy in (1, -1)]
    pts += [(sx * x, y) for x, y in BOLT_SITES_MID for sx in (1, -1)]
    cols = [bd.Pos(x, y, Z_TUB0 - 0.1) * bd.Cylinder(STANDOFF_D / 2 + 0.1, TUB_H + 0.2, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
            for x, y in pts]
    out = cols[0]
    for c in cols[1:]:
        out = out + c
    return out, pts


def cheeks():
    """The shared front-mount interface: two TPU cheeks on the front wall carrying the pivot pin (front_mount.py)."""
    c = []
    for sx in (1, -1):
        prof = bd.Pos(0, 0, 0) * bd.Rectangle(CHEEK_REACH + EYE_R, 2 * EYE_R, align=(bd.Align.MIN, bd.Align.CENTER))
        blk = bd.extrude(bd.Plane.YZ.offset(sx * CHEEK_HALF_X - CHEEK_T / 2) * bd.Pos(HALF_L_TUB - 0.5, PIN_Z) * prof, CHEEK_T)
        bore = bd.Pos(sx * CHEEK_HALF_X, PIN_Y, PIN_Z) * bd.Rot(0, 90, 0) * bd.Cylinder(PIN_CLEAR / 2, CHEEK_T + 1)
        c.append(blk - bore)
    return c[0] + c[1]


def tub():
    body = _body() - _flank_cut() - _wells() - _bays() - _standoff_bores()[0] - _hinge_bore()
    return body + cheeks()
