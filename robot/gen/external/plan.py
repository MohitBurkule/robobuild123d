"""The build plan every external generator writes into: chassis features per half, parts, screws, wires.

The chassis is a printed clamshell split at the wheel axis plane (z = 0): `bottom` (belly .. 0) and `top` (0 .. roof).
Generators add solids (`add`) and cuts (`cut`) to either half, add parts and fasteners, and register pockets; `shell`
turns the plan into the two printed halves at the end.
"""

from __future__ import annotations

import os
import sys
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
    intent: dict | None = None  # why the pocket (and its housing wall) exists

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
    features: list = field(default_factory=list)  # every feature + its design intent (see robot/gen/intent.py)

    def feature(self, op, intent, target=None, half=None):
        """Record one feature and why it exists (`intent` from intent.I). The source line is kept for the check."""
        fr = sys._getframe(1)
        while fr is not None and os.path.basename(fr.f_code.co_filename) == "plan.py":
            fr = fr.f_back
        src = f"{os.path.basename(fr.f_code.co_filename)}:{fr.f_lineno}" if fr is not None else "?"
        self.features.append({"id": f"{op}{len(self.features)}", "op": op, "target": target, "half": half,
                              "intent": intent, "src": src})

    def add(self, half, *shapes, intent=None):
        shapes = [s for s in shapes if s is not None]
        self.adds[half].extend(shapes)
        if shapes:
            self.feature("add", intent, half=half)

    def cut(self, half, *shapes, intent=None):
        shapes = [s for s in shapes if s is not None]
        self.cuts[half].extend(shapes)
        if shapes:
            self.feature("cut", intent, half=half)

    def cut_both(self, *shapes, intent=None):
        self.cut("bottom", *shapes, intent=intent)
        self.cut("top", *shapes, intent=intent)

    def late_cut(self, half, *shapes, intent=None):
        """Cuts applied after pockets (bolt bores, counterbores)."""
        shapes = [s for s in shapes if s is not None]
        self.late_cuts[half].extend(shapes)
        if shapes:
            self.feature("late_cut", intent, half=half)

    def pocket(self, pk, intent=None):
        pk.intent = intent if intent is not None else pk.intent
        self.pockets.append(pk)
        self.feature("pocket", pk.intent, target=pk.id)
        return pk

    def wire(self, w: dict, intent=None):
        self.wires.append(w)
        self.feature("wire", intent, target=w["id"])
        return w

    def part(self, intent=None, **p):
        p.setdefault("at", [0.0, 0.0, 0.0])
        p.setdefault("rot", [0.0, 0.0, 0.0])
        self.parts.append(p)
        self.feature("part", intent, target=p["id"])
        return p

    def get(self, pid):
        return next((p for p in self.parts if p["id"] == pid), None)

    def connect(self, a, b, method, reason, intent=None, **kw):
        """A joint between two parts. Its reason is its intent; the purpose follows from the method unless given."""
        self.connections.append({"a": a, "b": b, "method": method, "reason": reason, **kw})
        if intent is None and reason:
            purpose = {"shaft": "load_path", "pin": "load_path", "belt": "load_path", "glue": "retention", "velcro": "retention",
                       "tape": "retention", "snap": "assembly", "interlock": "retention"}.get(method, "assembly")
            lim = ", ".join(f"{k}={v}" for k, v in kw.items() if k in ("interference_mm", "mechanical_key")) or "geometry"
            intent = {"purpose": purpose, "reason": reason, "load_or_constraint": f"{method}; {lim}"}
        self.feature("connect", intent, target=f"{a}~{b}")

    def screw(self, intent=None, **f):
        f.setdefault("tool", "hex1.5")
        f.setdefault("removable", True)
        f.setdefault("head", "socket")
        self.fasteners.append(f)
        self.feature("fastener", intent, target=f["id"])
        return f
