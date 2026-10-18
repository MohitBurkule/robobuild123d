"""Data model of the layout problem: an outline, keep-out zones, components to place and the solved layouts."""

from __future__ import annotations

import json
from dataclasses import asdict, dataclass, field


@dataclass
class Component:
    """One internal component. `size` is (x, y, z) in its own frame; `rot_z` choices are tried by the solver."""

    id: str
    kind: str = "other"  # battery, esc, receiver, switch, servo, weapon_esc, other
    size: tuple = (10.0, 10.0, 5.0)
    mass_g: float = 1.0
    catalog: str | None = None
    fixed_at: tuple | None = None  # (x, y) or (x, y, z): pinned by the user
    rot_choices: tuple = (0.0, 90.0)
    on_wall: bool = False  # must sit in the outer wall, reachable from outside (power switch)
    ports: dict = field(default_factory=dict)  # name -> (x, y, z) local
    min_front_mm: float = 0.0  # distance kept from the front edge
    min_side_mm: float = 0.0  # distance kept from each side edge
    compartment: bool = False  # wants its own walled compartment
    wall_faces: tuple = ("rear", "left", "right")  # which outer walls an on_wall component may sit against

    port_room: float = 0.0  # free space kept around each port (wire exit), grows the cavity on that side only

    def footprint(self, rot_z: float) -> tuple:
        sx, sy = self.size[0], self.size[1]
        return (sy, sx) if int(round(rot_z)) % 180 == 90 else (sx, sy)

    def extent(self, rot_z: float) -> tuple:
        """(x0, x1, y0, y1) about the centre in world axes: the body plus room around every port."""
        import math

        fx, fy = self.footprint(rot_z)
        x0, x1, y0, y1 = -fx / 2, fx / 2, -fy / 2, fy / 2
        if self.port_room > 0:
            a = math.radians(rot_z)
            for q in self.ports.values():
                px, py = q[0] * math.cos(a) - q[1] * math.sin(a), q[0] * math.sin(a) + q[1] * math.cos(a)
                x0, x1 = min(x0, px - self.port_room), max(x1, px + self.port_room)
                y0, y1 = min(y0, py - self.port_room), max(y1, py + self.port_room)
        return (x0, x1, y0, y1)


@dataclass
class Keepout:
    """An axis-aligned rectangle no component may use (motors, wheel pockets, bosses, weapon module)."""

    id: str
    x0: float
    x1: float
    y0: float
    y1: float


@dataclass
class Link:
    """A wire between two component ports (or a fixed point named `@x,y`)."""

    a: str
    b: str
    weight: float = 1.0


@dataclass
class LayoutInputs:
    outline: list  # [[x, y], ...] counter-clockwise, the outer chassis outline
    height: float = 20.0
    wall: float = 1.6  # outer wall thickness
    gap: float = 0.4  # printing gap around each component
    pocket_wall: float = 1.2  # wall kept between neighbouring cavities
    components: list = field(default_factory=list)
    keepouts: list = field(default_factory=list)
    links: list = field(default_factory=list)
    anchors: dict = field(default_factory=dict)  # name -> (x, y): fixed wire ends (motor terminals, weapon motor)
    holes: list = field(default_factory=list)  # [(x, y, r)] screw holes / bosses the cavities must clear
    cog_target: tuple = (0.0, 0.0)
    fixed_mass: list = field(default_factory=list)  # [(mass_g, x, y)] for parts not placed by the solver
    grid: float = 2.0
    seed: int = 0
    max_nodes: int = 20000

    @classmethod
    def from_dict(cls, d: dict) -> "LayoutInputs":
        d = dict(d)
        d["components"] = [c if isinstance(c, Component) else Component(**_tuplify(c)) for c in d.get("components", [])]
        d["keepouts"] = [k if isinstance(k, Keepout) else Keepout(**k) for k in d.get("keepouts", [])]
        d["links"] = [l if isinstance(l, Link) else Link(**l) for l in d.get("links", [])]
        keep = {f for f in cls.__dataclass_fields__}
        return cls(**{k: v for k, v in d.items() if k in keep})


def _tuplify(c: dict) -> dict:
    c = dict(c)
    for k in ("size", "fixed_at", "rot_choices", "wall_faces"):
        if c.get(k) is not None:
            c[k] = tuple(c[k])
    return c


@dataclass
class Placement:
    id: str
    x: float
    y: float
    z: float
    rot_z: float
    footprint: tuple  # (fx, fy) world-axis footprint without gap
    extent: tuple | None = None  # (x0, x1, y0, y1) about the centre incl. port room; None = the footprint

    def rect(self, pad: float = 0.0) -> tuple:
        if self.extent is None:
            fx, fy = self.footprint
            e = (-fx / 2, fx / 2, -fy / 2, fy / 2)
        else:
            e = self.extent
        return (self.x + e[0] - pad, self.x + e[1] + pad, self.y + e[2] - pad, self.y + e[3] + pad)


@dataclass
class Layout:
    placements: dict  # id -> Placement
    score: float
    terms: dict  # objective name -> value

    def to_dict(self) -> dict:
        return {"score": round(self.score, 3), "terms": {k: round(v, 3) for k, v in self.terms.items()},
                "placements": {k: asdict(p) for k, p in self.placements.items()}}

    def to_json(self) -> str:
        return json.dumps(self.to_dict(), indent=2)
