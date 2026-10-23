"""Side_Panel_alt_sm (TPU): the body is built from relations in `sp_geom`; this adds the hardware: the two countersunk
boss screws (fastener table) and the cross bolt's tapping pilot through the tongue (STEP: 2.6). Right-hand part in the STEP frame;
the left panel is its mirror."""
import build123d as bd

from robocad.geom import _S, _cyl, _mirror_x, _solid
from .params_chassis import HY, TAB_HOLE_DY, TAB_HOLE_Z
from .params_side import TONGUE_X, TONGUE_PILOT
from .sp_geom import sp


def side_panel(side=1):
    from .fasteners import cutters
    pin = _cyl(TONGUE_PILOT / 2, TONGUE_X[0] - 1, TONGUE_X[1] + 1, (HY + TAB_HOLE_DY, TAB_HOLE_Z), "x")   # the cross bolt threads into the tongue
    s = _solid(_S(sp(), cutters("side_r"), pin))
    return s if side > 0 else _solid(_mirror_x(s))


def side_panel_r():
    return side_panel(1)


def side_panel_ref_frame():
    """The right panel in the right STEP solid's frame (that solid sits 0.25 mm inboard of the left one's mirror)."""
    return side_panel(1).moved(bd.Location((-0.25, 0, 0)))
