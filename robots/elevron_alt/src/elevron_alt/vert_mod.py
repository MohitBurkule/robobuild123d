"""vert_mod: printed weapon module on the Alt chassis deck. The body is built from relations in `vm_geom` (ramp top,
planform, hollow, uprights, shroud, prongs, cuts); this adds the head-side fastener cutters. STEP frame."""
from robocad.geom import _S, _solid
from .vm_geom import vm


def vert_mod():
    from .fasteners import cutters
    return _solid(_S(vm(), cutters("vert_mod")))
