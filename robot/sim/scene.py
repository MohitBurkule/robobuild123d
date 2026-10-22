"""Scene description: static and dynamic props plus robot placements. Plain dataclasses, engine independent."""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class Prop:
    name: str
    shape: str  # box | sphere | cylinder
    size: tuple  # box: half extents; sphere: (r,); cylinder: (r, half height)   (m)
    pos: tuple
    euler_deg: tuple = (0.0, 0.0, 0.0)
    mass: float | None = None  # None = static
    friction: float = 0.8
    rgba: tuple = (0.6, 0.6, 0.65, 1.0)


@dataclass
class Placement:
    name: str
    xy: tuple = (0.0, 0.0)
    yaw_deg: float = 0.0
    z_clear: float = 0.0005  # gap above the ground at spawn (m)


@dataclass
class Scene:
    gravity: float = 9.81
    floor_friction: float = 0.8
    arena_half: float = 0.6  # square arena half side (m); 0 = infinite plane only
    wall_height: float = 0.1
    props: list = field(default_factory=list)

    def box(self, name, size, pos, mass=None, **kw):
        self.props.append(Prop(name, "box", tuple(size), tuple(pos), mass=mass, **kw))
        return self

    def sphere(self, name, r, pos, mass=None, **kw):
        self.props.append(Prop(name, "sphere", (r,), tuple(pos), mass=mass, **kw))
        return self

    def ramp(self, name, length, width, angle_deg, x, y=0.0, thick=0.004):
        """Static incline rising along +y from ground level at its low edge."""
        import math

        a = math.radians(angle_deg)
        zc = length / 2 * math.sin(a) - thick / 2 * math.cos(a)
        yc = y + length / 2 * math.cos(a)
        self.props.append(Prop(name, "box", (width / 2, length / 2, thick / 2), (x, yc, zc), (angle_deg, 0, 0)))
        return self
