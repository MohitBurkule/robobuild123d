"""Assembly relations: named frames (build123d RigidJoint) on a datum part, and every placed part is mated to one.

The tub is the datum (world frame). Its joints are the places other parts attach to (heat-set bores, the switch slot wall,
the N10 seats); each attached part carries the matching joint on itself (insert bottom, switch side face, motor origin).
`pose(part)` is the mated location as the (at, rot) pair the spec uses, so a part's position is the result of a mate, not
a coordinate typed beside the part."""
import build123d as b
from .params import *  # noqa: F401,F403

DIGITS = 6   # spec precision: micron / micro-degree, JSON free of float noise


class Rig:
    def __init__(self):
        self.parts = {}
        self._mates = []

    def _host(self, name):
        if name not in self.parts:
            h = b.Compound(children=[b.Box(1, 1, 1)])
            h.label = name
            self.parts[name] = h
        return self.parts[name]

    def joint(self, part, label, at, rot=(0, 0, 0)):
        """Frame `label` on `part`, at `at` with orientation `rot` (degrees about X, Y, Z), in the part's own frame."""
        b.RigidJoint(label, self._host(part), b.Location(tuple(at), tuple(rot)))

    def axis(self, part, label, at, direction=(1, 0, 0)):
        """Spin axis `label` on `part` (build123d RevoluteJoint): a bearing bore or a shaft the mating part turns on."""
        b.RevoluteJoint(label, self._host(part), b.Axis(tuple(at), tuple(direction)))

    def revolute(self, part, label, span=(0, 360)):
        """Spec `joint` dict of a spin axis in world: pivot on the axis, sense normalised to + (an axle's sense is a
        convention, a mirrored motor still turns its hub about +X)."""
        ax = self.parts[part].joints[label].relative_axis.located(self.parts[part].location)
        d = [ax.direction.X, ax.direction.Y, ax.direction.Z]
        d = [-v for v in d] if max(d, key=abs) < 0 else d
        p = ax.position
        return {"kind": "revolute", "axis": [round(v, DIGITS) + 0.0 for v in d], "pivot": [round(v, DIGITS) + 0.0 for v in (p.X, p.Y, p.Z)],
                "min": span[0], "max": span[1], "default": span[0]}

    def mate(self, parent, plabel, child, clabel):
        """Place `child` so its joint `clabel` coincides with the parent's `plabel` (applied by solve(), in the order given: a
        joint added to an already placed part is taken relative to the world, so every joint is declared first)."""
        self._mates.append((parent, plabel, child, clabel))

    def solve(self):
        for parent, plabel, child, clabel in self._mates:
            pp, cp = self.parts[parent], self.parts[child]
            cp.location = pp.location * pp.joints[plabel].relative_location * cp.joints[clabel].relative_location.inverse()

    def pose(self, part, frame=None):
        """(at, rot) of the mated part (in `frame` part's frame, else world), rounded to the spec's precision."""
        loc = self.parts[part].location
        if frame is not None:
            loc = self.parts[frame].location.inverse() * loc
        at, rot = loc.position, loc.orientation
        return [round(v, DIGITS) + 0.0 for v in (at.X, at.Y, at.Z)], [round(v, DIGITS) + 0.0 for v in (rot.X, rot.Y, rot.Z)]


def tub_rig(r=None, solve=True):
    """Rig of the parts that mate to the tub: heat-set inserts (floor and rim), the power switch, the N10 motors."""
    r = r or Rig()
    for i, (x, y) in enumerate(INS):                 # floor bores: the insert rests on the bore floor
        r.joint("tub", f"bore_b{i}", (x, y, INS_Z[0]))
        r.joint(f"insert_b{i}", "bottom", (0, 0, -INS_LEN / 2))
        r.mate("tub", f"bore_b{i}", f"insert_b{i}", "bottom")
    for i, (x, y) in enumerate(TOP_XY):              # rim bores: the insert top is flush with the rim the top panel sits on
        r.joint("tub", f"bore_t{i}", (x, y, CH["z1"]))
        r.joint(f"insert_t{i}", "top", (0, 0, INS_LEN / 2))
        r.mate("tub", f"bore_t{i}", f"insert_t{i}", "top")
    r.joint("tub", "switch_wall", (CH["x"] - CH["wall"], ELEC["switch_yz"][0], ELEC["switch_yz"][1]), (0, 0, 90))   # inner face of the +X wall at the switch (switch turned 90 about Z)
    r.joint("power_switch", "side", (0, -(SW_HALF + SW_WALL_CLEAR), 0))                                       # its side face, the clearance off the wall
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
        r.joint("tub", f"screw_t{i}", (x, y, TOP_BOLT_Z))
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
