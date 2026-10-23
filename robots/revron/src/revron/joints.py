"""Assembly relations: named frames (build123d RigidJoint) on a datum part, and every placed part is mated to one.

The tub is the datum (world frame). Its joints are the places other parts attach to (heat-set bores, the switch slot wall,
the N10 seats); each attached part carries the matching joint on itself (insert bottom, switch side face, motor origin).
`pose(part)` is the mated location as the (at, rot) pair the spec uses, so a part's position is the result of a mate, not
a coordinate typed beside the part."""
import math
import build123d as b
from .params import *  # noqa: F401,F403
from .variants import variant
from robocad.rig import Rig as _Rig, DIGITS  # noqa: F401

TUB_FRAME = b.Location((0, 0, (CH_Z0 + CH_Z1) / 2), (0, 180, 0))   # RV01 part frame -> robot world: turned half a turn about Y (x, z flipped) about the mid-height


class Rig(_Rig):
    """The shared robocad Rig with the RV01 tub as the one part drawn in its own SolidWorks frame."""
    def __init__(self):
        super().__init__({"tub": TUB_FRAME})


def tub_rig(r=None, solve=True):
    """Rig of the parts that mate to the tub: heat-set inserts (floor and rim), the power switch, the N10 motors."""
    r = r or Rig()
    for i, (x, y) in enumerate(INS):                 # floor bores: the insert rests on the bore floor
        r.joint("tub", f"bore_b{i}", (x, y, INS_Z[0]))
        r.joint(f"insert_b{i}", "bottom", (0, 0, -INS_LEN / 2))
        r.mate("tub", f"bore_b{i}", f"insert_b{i}", "bottom")
    r.joint("tub", "switch_wall", (CH["x"] - CH["wall"], ELEC["switch_yz"][0], ELEC["switch_yz"][1]), (0, 0, 90))   # inner face of the +X wall at the switch (switch turned 90 about Z)
    r.joint("power_switch", "side", (0, -(SW_HALF_W + SW_CLR), 0))                                       # its side face, the clearance off the wall
    r.mate("tub", "switch_wall", "power_switch", "side")
    for s, n in ((1, "r"), (-1, "l")):               # N10 seats: the gearbox origin sits MOTX out from the chassis centre on the rear axle line
        r.joint("tub", f"n10_{n}", (s * MOTX, RY, RZ), (0, 0, 0 if s > 0 else 180))
        r.joint(f"motor_{n}", "origin", (0, 0, 0))
        r.mate("tub", f"n10_{n}", f"motor_{n}", "origin")
    for i, (x, y) in enumerate(INS):                 # base-panel screws: head plane on the panel underside, axis on the bore
        r.joint("tub", f"screw_b{i}", (x, y, BASE_BOLT_Z))
        r.joint(f"bolt_b{i}", "head", (0, 0, 0))
        r.mate("tub", f"screw_b{i}", f"bolt_b{i}", "head")
    for i, (x, y) in enumerate(TOP_XY):              # top-panel screws: head plane on the panel top face
        r.hole("tub", f"screw_t{i}", (x, y, TOP_BOLT_Z), (0, 0, -1))   # driven down through the panel
        if TOP_SCREW_WEB:
            r.joint(f"bolt_t{i}", "head", (0, 0, 0))
            r.mate("tub", f"screw_t{i}", f"bolt_t{i}", "head")
    for i, sg in enumerate((1, -1)):                 # switch screws: through the ear holes (SW_PITCH apart along its length) at the body top
        r.joint("power_switch", f"ear{i}", (sg * SW_PITCH / 2, 0, SW_BODY_H / 2))
        r.joint(f"bolt_sw{i}", "head", (0, 0, 0))
        r.mate("power_switch", f"ear{i}", f"bolt_sw{i}", "head")
    if solve:
        r.solve()
    return r


def _rig():
    from .assembly_rig import assembly_rig   # the rest of the chain (weapon, drive, armour, electronics)
    return assembly_rig()


RIG = _rig()


def place_at(part):
    return RIG.pose(part)[0]


def place_rot(part):
    return RIG.pose(part)[1]


def place(part, frame=None):
    """Spec `at`/`rot` of a mated part in its spec parent's frame."""
    at, rot = RIG.pose(part, frame)
    return {"at": at, "rot": rot}


def seat(fastener):
    return RIG.seat(fastener)
