"""[tub2] Small build123d helpers shared by the tub2 feature files: sketch prisms, concave fillet fillers, half-model mirroring."""
from build123d import Align, BuildSketch, Circle, Locations, Mode, Part, Plane, Pos, Rectangle, extrude


def prism(sketch, z0, z1):
    """Extrude a BuildSketch drawn on the XY plane from z0 to z1."""
    return Pos(0, 0, z0) * extrude(sketch.sketch, z1 - z0)


def box_xy(x0, x1, y0, y1, z0, z1):
    """Axis-aligned block between the given coordinates (a rectangle sketch extruded)."""
    with BuildSketch() as sk:
        with Locations((x0, y0)):
            Rectangle(x1 - x0, y1 - y0, align=(Align.MIN, Align.MIN))
    return prism(sk, z0, z1)


def concave_filler(corner, quadrant, r):
    """Material of a fillet R r in the concave corner `corner` whose free space lies in `quadrant` (sx, sy): the
    r x r square minus the tangent circle (what a SolidWorks fillet adds in the sketch)."""
    (px, py), (sx, sy) = corner, quadrant
    ax = Align.MIN if sx > 0 else Align.MAX
    ay = Align.MIN if sy > 0 else Align.MAX
    with BuildSketch() as sk:
        with Locations((px, py)):
            Rectangle(r, r, align=(ax, ay))
        with Locations((px + sx * r, py + sy * r)):
            Circle(r, mode=Mode.SUBTRACT)
    return sk


def mirrored(part):
    """The part plus its image across the X = 0 (Right) plane: the designer's Mirror feature."""
    return part + part.mirror(Plane.YZ)


def round_floor_pocket(face, y_floor, y_open, r):
    """Cutter of a pocket in the XZ plane whose plan corners and floor edges are all rounded R r with the pocket only r deep (SolidWorks
    sketch corner R = floor Fillet R = depth, so the floor corners are spheres): the plan face shrunk by r, swept by a ball of radius r.
    `face` is the plan Face drawn on the default XY sketch plane (sketch x = world X, sketch y = world Z); the floor lies at world y_floor, the pocket opens
    towards y_open."""
    from build123d import Cylinder, Kind, Sphere, add, offset
    s = 1 if y_open > y_floor else -1
    yc = y_floor + s * r
    with BuildSketch(Plane.XZ.offset(-y_floor)) as e:
        add(face)
        offset(amount=-r, kind=Kind.INTERSECTION)
    with BuildSketch(Plane.XZ.offset(-yc)) as w:
        add(face)
        offset(amount=-r, kind=Kind.INTERSECTION)
        offset(amount=r, kind=Kind.ARC)
    out = extrude(e.sketch, -s * abs(y_open - y_floor)) + extrude(w.sketch, -s * abs(y_open - yc))
    for ed in e.sketch.edges():
        p, q = ed.start_point(), ed.end_point()
        d = q - p
        out += Plane(origin=(p.X, yc, p.Z), z_dir=(d.X, 0, d.Z)) * Cylinder(r, d.length, align=(Align.CENTER, Align.CENTER, Align.MIN))
        out += Pos(p.X, yc, p.Z) * Sphere(r)
    return out


def fit_radius(pts, i, r, rounded=()):
    """Largest corner radius <= r that fits at vertex i of the closed polygon `pts`: the tangent length r / tan(half the corner angle)
    must fit the shorter adjacent edge, half of it where the neighbour at its other end is rounded too (`rounded` = vertex indices)."""
    from math import atan2, hypot, tan
    n = len(pts)
    p, a, b = pts[i], pts[i - 1], pts[(i + 1) % n]
    va, vb = (a[0] - p[0], a[1] - p[1]), (b[0] - p[0], b[1] - p[1])
    la, lb = hypot(*va), hypot(*vb)
    theta = abs(atan2(va[0] * vb[1] - va[1] * vb[0], va[0] * vb[0] + va[1] * vb[1]))   # interior angle
    room = min(la / (2 if (i - 1) % n in rounded else 1), lb / (2 if (i + 1) % n in rounded else 1))
    return min(r, 0.98 * room * tan(theta / 2))
