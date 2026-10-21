"""Top Panel, built in its own SolidWorks part frame (feature order of the Top Panel dump): Sketch1 outline -> Boss-Extrude1 ->
Fillet1 (R10 arcs into the ears) -> Fillet3 -> Sketch2 + Boss-Extrude2 (front tab) -> Fillet4 -> Chamfer1 (hole chamfers).
Laser-cut Ti sheet, one thickness level: the dump's 0.1 deep recess (Cut-Extrude3) is not modelled.
Part frame = reference transform: origin on the bolt-pattern centre at the top face, z pointing down through the sheet."""
import build123d as b
from robot.cad.holes import hole_tool
from .params_chassis import TOP_XY, TOP_Z0, TOP_T, TOP_X, TOP_NOTCH_X, TOP_SHOULDER_Y, TOP_TAB_Y
from .panel_base import to_local

YC = sum(y for _, y in TOP_XY) / len(TOP_XY)
FRAME = b.Location((0, YC, TOP_Z0 + TOP_T), (0, 180, 0))
BOLT = [to_local(FRAME, (x, y, 0))[:2] for x, y in TOP_XY]          # bolt pattern in the part frame (shared with the tub's rim bores)
DX, DY = 2 * max(abs(x) for x, _ in BOLT), 2 * max(abs(y) for _, y in BOLT)
EAR_R, HOLE_D, CHAMFER = 2.5, 2.2, 0.75                             # ear radius, clearance hole, Chamfer1
EDGE_Y = DY / 2 + EAR_R                                             # front / rear edge tangent to the ears
FILL_R, FILL_YT = 10.0, 6.395                                       # Fillet1: R10 arc, tangent to the |X| TOP_X edge at Y = FILL_YT
FILLET = 1.0                                                        # Fillet3 / Fillet4
SHOULDER, TAB_Y = TOP_SHOULDER_Y - YC, TOP_TAB_Y - YC               # notch floor, tab front edge (Boss-Extrude2 reaches TAB_Y)
NOTCH_X0, NOTCH_X1 = TOP_NOTCH_X                                    # tab half width, notch half width


def seat(i):
    """FastenerRecord of bolt i (world): M2 button head bearing flat on the sheet, plain clearance hole."""
    x, y = TOP_XY[i]
    return hole_tool((x, y, TOP_Z0 + TOP_T), (0, 0, -1), "M2x5", head="button", into="through", side="head", grip=TOP_T, cbore=0)


def outline():
    ears = [b.Pos(l.position.X, l.position.Y) * b.Circle(EAR_R) for l in b.GridLocations(DX, DY, 2, 2).locations]
    sk = b.Rectangle(2 * TOP_X, 2 * EDGE_Y)
    for sx in (1, -1):
        for sy in (1, -1):   # concave R10 arc from the side edge into the ear, mirrored to the four ears
            arc = b.Pos(sx * (TOP_X + FILL_R), sy * FILL_YT) * b.Circle(FILL_R)
            xe, ye = TOP_X + (DX / 2 - TOP_X + EAR_R) / 2, (FILL_YT + DY / 2) / 2
            wedge = b.Pos(sx * xe, sy * ye) * b.Rectangle(DX / 2 - TOP_X + EAR_R, DY / 2 - FILL_YT) - arc
            strip = b.Pos(sx * (TOP_X + DX / 2) / 2, sy * (DY / 2 + EDGE_Y) / 2) * b.Rectangle(DX / 2 - TOP_X, EDGE_Y - DY / 2)
            sk += wedge + strip
    sk += ears
    sk -= b.Pos(0, (SHOULDER + EDGE_Y) / 2) * b.Rectangle(2 * NOTCH_X1, EDGE_Y - SHOULDER)           # front notch
    sk += b.Pos(0, (SHOULDER + TAB_Y) / 2) * b.Rectangle(2 * NOTCH_X0, TAB_Y - SHOULDER)             # Boss-Extrude2 tab
    corners = [(sx * x, y) for sx in (1, -1) for x, y in ((NOTCH_X1, SHOULDER), (NOTCH_X0, SHOULDER), (NOTCH_X0, TAB_Y), (NOTCH_X1, EDGE_Y))]
    near = lambda p: min(sk.vertices(), key=lambda v: (v.X - p[0]) ** 2 + (v.Y - p[1]) ** 2)
    return b.fillet([near(p) for p in corners], FILLET)


def top_panel():
    body = b.extrude(outline(), TOP_T)
    for x, y in BOLT:
        body -= b.Pos(x, y, 0) * b.Cylinder(HOLE_D / 2, 2 * TOP_T)
    holes = body.edges().filter_by(b.GeomType.CIRCLE).filter_by_position(b.Axis.Z, TOP_T - 1e-3, TOP_T + 1e-3)
    return b.chamfer([e for e in holes if abs(e.radius - HOLE_D / 2) < 1e-3], CHAMFER)
