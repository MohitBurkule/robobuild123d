"""TubShell: chassis tub sized from its contents (UNTESTED: written without running).

Interior = union bounding box of the content envelopes passed in (electronics bay, drive pods, weapon), shell =
interior grown by `wall` on the sides and `floor` below, open on top. Every content envelope is cut out; pods are
mirrored left/right about Y=0. The front (+X) gets a wedge whose length derives from shell height and `wedge_angle_deg`.
Mounts are emitted at each pod envelope centre (both sides). No raw numbers: all from masters / envelopes.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

from build123d import Box, Location, Part, Plane, Pos, Wedge, mirror

from robot.cad.bay import DEFAULT_WALL, CUT_OVERSHOOT
from robot.modules.base import ModuleResult, Mount


def _bbox(solids):
    bbs = [s.bounding_box() for s in solids]
    lo = tuple(min(getattr(b.min, a) for b in bbs) for a in "XYZ")
    hi = tuple(max(getattr(b.max, a) for b in bbs) for a in "XYZ")
    return lo, hi


@dataclass
class TubShell:
    name: str = "tub"
    wall: float = DEFAULT_WALL                     # side wall master
    floor: float = DEFAULT_WALL                    # floor master
    wedge_angle_deg: float = 30.0                  # master: front wedge rake from horizontal
    bay_cuts: list = field(default_factory=list)   # solids to subtract (e.g. ElectronicsBay parts["cut_*"])
    pod_envelopes: list = field(default_factory=list)   # right-side (+Y) drive pod keep-ins; mirrored to -Y
    weapon_envelopes: list = field(default_factory=list)
    mirror_pods: bool = True                       # False when both pods are already passed in

    def _all_cuts(self):
        pods = list(self.pod_envelopes)
        if self.mirror_pods:
            pods += [mirror(p, Plane.XZ) for p in self.pod_envelopes]
        return list(self.bay_cuts), pods, list(self.weapon_envelopes)

    def build(self) -> ModuleResult:
        bays, pods, weapons = self._all_cuts()
        contents = bays + pods + weapons
        if not contents:
            raise ValueError("TubShell needs at least one content envelope")
        lo, hi = _bbox(contents)
        size = [h - l for l, h in zip(lo, hi)]
        outer = (size[0] + 2 * self.wall, size[1] + 2 * self.wall, size[2] + self.floor)
        centre = ((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, lo[2] - self.floor + outer[2] / 2)
        shell: Part = Pos(*centre) * Box(*outer)

        # wedge: a ramp ahead of the front face, run = height / tan(angle)
        height = outer[2]
        run = height / math.tan(math.radians(self.wedge_angle_deg))
        front_x = centre[0] + outer[0] / 2
        base_z = centre[2] - outer[2] / 2
        # Wedge(xsize, ysize, zsize, xmin, zmin, xmax, zmax): taper to a line at the leading edge
        wedge = Pos(front_x + run / 2, centre[1], base_z + height / 2) * Wedge(
            run, outer[1], height, -run / 2, -height / 2, -run / 2, -height / 2)
        shell = shell + wedge   # UNTESTED: Wedge axis convention (taper face at y=ysize) may need a Rot to align

        # open top: interior pocket swept up past the rim
        interior = Pos((lo[0] + hi[0]) / 2, (lo[1] + hi[1]) / 2, (lo[2] + hi[2]) / 2 + CUT_OVERSHOOT) * Box(
            size[0], size[1], size[2] + 2 * CUT_OVERSHOOT)
        for c in contents:
            shell = shell - c
        shell = shell - interior

        res = ModuleResult(self.name, parts={"tub": shell})
        for i, p in enumerate(pods):
            c = p.bounding_box().center   # BoundBox.center is a property, not a method
            side = "right" if c.Y >= centre[1] else "left"
            res.mounts[f"pod_{side}_{i}"] = Mount(f"pod_{side}_{i}", Location((c.X, c.Y, c.Z)))
        res.envelope = Pos(*centre) * Box(*outer)
        return res
