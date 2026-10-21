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
