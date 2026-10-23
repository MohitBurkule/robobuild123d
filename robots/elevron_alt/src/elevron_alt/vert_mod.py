"""vert_mod: printed weapon module on the Alt chassis deck. The body is built from relations in `vm_geom` (ramp top,
planform, hollow, uprights, shroud, prongs, cuts); this adds the hardware seats: the cross-bolt nut pockets in the prongs
and the head-side fastener cutters. STEP frame."""
import math

from shapely.geometry import Polygon

from robocad.geom import _S, _ext, _mirror_x, _solid
from robot.cad import fastener_catalog as fc
from .params_chassis import HY, TAB_HOLE_DY, TAB_HOLE_Z, HEX, HEX_PHASE, M3
from .params_side import NUT_FIT
from .params_vert import PRONG
from .vm_geom import vm


def prong_nuts():
    """Thin M3 nut pocket in each prong's inner face: the inner chassis tab closes it once the module is down."""
    af, m = fc.nut(M3, "thin")
    r = (af + NUT_FIT) / math.sqrt(3)
    y, z = HY + TAB_HOLE_DY, TAB_HOLE_Z
    hexp = Polygon([(y + r * math.cos(math.radians(a)), z + r * math.sin(math.radians(a))) for a in range(HEX_PHASE, 360 + HEX_PHASE, 360 // HEX)])
    p = _ext(hexp, "yz", PRONG[0] - 1, PRONG[0] + m)
    return p.fuse(_mirror_x(p))


def vert_mod():
    from .fasteners import cutters
    return _solid(_S(vm(), prong_nuts(), cutters("vert_mod")))
