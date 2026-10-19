"""The build plan every external generator writes into: chassis features per half, parts, screws, wires.

The chassis is a printed clamshell split at the wheel axis plane (z = 0): `bottom` (belly .. 0) and `top` (0 .. roof).
Generators add solids (`add`) and cuts (`cut`) to either half, add parts and fasteners, and register pockets; `shell`
turns the plan into the two printed halves at the end.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Frame:
    outline: list  # outer XY outline, counter-clockwise
    zb: float  # belly (underside of the bottom half)
    zt: float  # roof (top of the top half)
    wall: float = 1.6
    floor: float = 1.0
    split: float = 0.0
    spline: bool = False  # outline drawn as a closed B-spline (organic shell)

    @property
    def x0(self):
        return min(p[0] for p in self.outline)

    @property
    def x1(self):
        return max(p[0] for p in self.outline)

    @property
    def y0(self):
        return min(p[1] for p in self.outline)

    @property
    def y1(self):
        return max(p[1] for p in self.outline)


@dataclass
class Pocket:
    """A cavity for one component, with a housing wall around it. z0..z1 is the cavity height."""

    id: str
    x0: float
    x1: float
    y0: float
    y1: float
    z0: float
    z1: float
    housing: float = 1.4  # wall thickness of the housing; 0 = no housing
    halves: tuple = ("bottom", "top")
    notches: list = field(default_factory=list)  # [(x0, x1, y0, y1, z0, z1)] wire exits at the ports
    wire_through: bool = False  # the channel band under the part is empty (switch slot): its own wires may cross it

    def outer(self) -> tuple:
        """XY extent of cavity + notches + housing wall."""
        xs = [self.x0, self.x1] + [v for n in self.notches for v in n[:2]]
        ys = [self.y0, self.y1] + [v for n in self.notches for v in n[2:4]]
        h = self.housing
        return (min(xs) - h, max(xs) + h, min(ys) - h, max(ys) + h)


@dataclass
class Plan:
    hyp: object
    frame: Frame
    name: str = "generated"
    robot_type: str = "wedge"
    archetype: str | None = None
    pockets: list = field(default_factory=list)
    adds: dict = field(default_factory=lambda: {"bottom": [], "top": []})
    cuts: dict = field(default_factory=lambda: {"bottom": [], "top": []})
    late_cuts: dict = field(default_factory=lambda: {"bottom": [], "top": []})  # applied after pockets (bolt holes)
    parts: list = field(default_factory=list)
    fasteners: list = field(default_factory=list)
    wires: list = field(default_factory=list)
    connections: list = field(default_factory=list)
    allow_overlap: list = field(default_factory=list)
    claims: list = field(default_factory=list)
    keepouts: list = field(default_factory=list)  # (id, x0, x1, y0, y1) for the layout solver
    anchors: dict = field(default_factory=dict)  # wire anchor name -> (x, y, z)
    electronics: dict = field(default_factory=dict)
    extra: dict = field(default_factory=dict)  # top-level spec keys (archetype, reference, ...)
    notes: list = field(default_factory=list)
    placements: dict = field(default_factory=dict)  # component id -> (x, y, z, rot_z) from the layout

    def add(self, half, *shapes):
        self.adds[half].extend(s for s in shapes if s is not None)

    def cut(self, half, *shapes):
        self.cuts[half].extend(s for s in shapes if s is not None)

    def cut_both(self, *shapes):
        self.cut("bottom", *shapes)
        self.cut("top", *shapes)

    def part(self, **p):
        p.setdefault("at", [0.0, 0.0, 0.0])
        p.setdefault("rot", [0.0, 0.0, 0.0])
        self.parts.append(p)
        return p

    def get(self, pid):
        return next((p for p in self.parts if p["id"] == pid), None)

    def connect(self, a, b, method, reason, **kw):
        self.connections.append({"a": a, "b": b, "method": method, "reason": reason, **kw})

    def screw(self, **f):
        f.setdefault("tool", "hex1.5")
        f.setdefault("removable", True)
        f.setdefault("head", "socket")
        self.fasteners.append(f)
        return f
