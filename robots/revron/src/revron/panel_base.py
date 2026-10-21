"""RV26 base panel, built in its own SolidWorks part frame (feature order of the RV26 Base Panel dump):
Sketch1 outline -> Boss-Extrude1 (panel thickness) -> Chamfer1 (the five countersinks) -> Sketch3 + Boss-Extrude2 (N10 preload
pads, mirrored one side) -> Fillet1 (pad corners) -> Chamfer2 (pad top edges).
Part frame = reference transform: origin on the outline centre at the inner face, z pointing out through the panel (turned
180 deg about Y from the robot frame). It is placed on the tub by the `hole_0` joint (assembly_rig), not by coordinates."""
import build123d as b
from robot.cad.holes import hole_tool
from .variants import variant
from .params_chassis import BASE_OUT, BASE_Z0, BASE_T, BASE_CSK_CLEAR, BASE_CSK_CLEAR_STEP, INS, PRELOAD_PAD

YC = (BASE_OUT["y0"] + BASE_OUT["y1"]) / 2                 # outline centre Y: the part origin
FRAME = b.Location((0, YC, BASE_Z0 + BASE_T), (0, 180, 0))  # part frame -> robot world (reference transform)
PAD_CHAMFER = 0.25                                           # Chamfer2: the pad's whole height


def to_local(frame, p):
    """Robot-world point -> part-frame point."""
    q = (frame.inverse() * b.Pos(*p)).position
    return (round(q.X, 6) + 0.0, round(q.Y, 6) + 0.0, round(q.Z, 6) + 0.0)


def outline(grow=0.0):
    """Sketch1: the RV26 rounded rectangle; `grow` offsets it for the chassis rabbet."""
    return b.RectangleRounded(2 * (BASE_OUT["x"] + grow), BASE_OUT["y1"] - BASE_OUT["y0"] + 2 * grow, BASE_OUT["r"])


def rabbet(grow, z0, z1):
    """Robot-frame prism of the grown outline between world Z z0..z1 (the chassis seat the panel sits in)."""
    return b.Pos(0, YC, z0) * b.extrude(outline(grow), z1 - z0)


def seat(i, local=True):
    """(cutter, FastenerRecord) of countersink i: the M2 CSK of the bolt, head side, 4.4 head in a seat cone parallel to it."""
    x, y = INS[i]
    at, axis = ((*to_local(FRAME, (x, y, BASE_Z0))[:2], BASE_T), (0, 0, -1)) if local else ((x, y, BASE_Z0), (0, 0, 1))
    return hole_tool(at, axis, "M2x6", head="csk", into="through", side="head", grip=BASE_T, csk_clear=BASE_CSK_CLEAR if variant("base_csk_fit") else BASE_CSK_CLEAR_STEP)   # original RV26 seat unless the base_csk_fit variant


def pad(sx):
    """Sketch3 + Fillet1 + Chamfer2: one preload pad (square, rounded corners, chamfered top), standing on the inner face (z < 0)."""
    cx, cy = PRELOAD_PAD["c"]
    h = PRELOAD_PAD["h"]
    sk = b.Pos(sx * cx, cy - YC) * b.Rectangle(PRELOAD_PAD["s"], PRELOAD_PAD["s"])
    sk = b.fillet(sk.vertices(), PRELOAD_PAD["r"])
    solid = b.Pos(0, 0, PRELOAD_PAD["sink"]) * b.extrude(sk, h + PRELOAD_PAD["sink"], dir=(0, 0, -1))
    return b.chamfer(solid.edges().filter_by_position(b.Axis.Z, -h - 1e-3, -h + 1e-3), PAD_CHAMFER)


def base_panel():
    body = b.extrude(outline(), BASE_T)
    for sx in (1, -1):
        body += pad(sx)
    return body - [seat(i)[0] for i in range(len(INS))]
