"""Assembly relations shared by every robot package: named frames (build123d RigidJoint) on a datum part, every placed
part mated to one, and the mated pose as the spec's (at, rot). Moved from revron/joints.py; a robot passes the frames
of parts drawn in their own CAD part frame (part frame -> robot world)."""
import math
import build123d as b

DIGITS = 6   # spec precision: micron / micro-degree, JSON free of float noise


class Rig:
    def __init__(self, frames=None):
        self.parts = {}
        self._mates = []
        self.frames = dict(frames or {})   # parts drawn in their own CAD part frame: frame -> robot world; joints are declared in robot coordinates

    def _host(self, name):
        if name not in self.parts:
            h = b.Compound(children=[b.Box(1, 1, 1)])
            h.label = name
            h.location = self.frames.get(name, b.Location())
            self.parts[name] = h
        return self.parts[name]

    def joint(self, part, label, at, rot=(0, 0, 0)):
        """Frame `label` on `part`, at `at` with orientation `rot` (degrees about X, Y, Z), given in robot coordinates (build123d re-expresses it in the host's frame: the host of a part with a reference frame is created at that frame)."""
        b.RigidJoint(label, self._host(part), b.Location(tuple(at), tuple(rot)))

    def joint_in(self, part, label, frame, world):
        """Frame `label` on `part` at the robot-world Location `world`, written in the part's own frame `frame` (part frame -> world)."""
        b.RigidJoint(label, self._host(part), frame.inverse() * world)

    def hole(self, part, label, at, direction):
        """Screw hole `label` on `part`: frame on the head seat, z along the screw's insertion direction."""
        b.RigidJoint(label, self._host(part), b.Location(b.Plane(tuple(at), z_dir=tuple(direction))))

    def seat(self, fastener):
        """Spec `at`/`dir` of a fastener mated into its hole: head point and insertion direction (the frame's z)."""
        loc = self.parts[fastener].location
        z = loc.wrapped.Transformation().HVectorialPart().Column(3)
        return {"at": self.pose(fastener)[0], "dir": [round(v, DIGITS) + 0.0 for v in (z.X(), z.Y(), z.Z())]}

    def axis(self, part, label, at, direction=(1, 0, 0)):
        """Spin axis `label` on `part` (build123d RevoluteJoint): a bearing bore or a shaft the mating part turns on."""
        b.RevoluteJoint(label, self._host(part), b.Axis(tuple(at), tuple(direction)))

    def revolute(self, part, label, span=(0, 360), frame=None):
        """Spec `joint` dict of a spin axis in world: pivot on the axis, sense normalised to + (an axle's sense is a
        convention, a mirrored motor still turns its hub about +X)."""
        ax = self.parts[part].joints[label].relative_axis.located(self.parts[part].location)
        if frame is not None:   # in `frame` part's frame (a spec joint pivot is in the part's parent frame)
            ax = ax.located(self.parts[frame].location.inverse())
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
        t = loc.wrapped.Transformation()
        R = [[t.Value(i, j) for j in (1, 2, 3)] for i in (1, 2, 3)]
        ry = -math.asin(max(-1.0, min(1.0, R[2][0])))   # the spec's Euler angles are R = Rz * Ry * Rx (robot.xform), not build123d's intrinsic XYZ
        rx, rz = (math.atan2(R[2][1], R[2][2]), math.atan2(R[1][0], R[0][0])) if abs(R[2][0]) < 1 - 1e-9 else (math.atan2(-R[1][2], R[1][1]), 0.0)
        at = loc.position
        return [round(v, DIGITS) + 0.0 for v in (at.X, at.Y, at.Z)], [round(math.degrees(v), DIGITS) + 0.0 for v in (rx, ry, rz)]
