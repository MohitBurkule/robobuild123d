"""Ripsaw top and base panels: printed nylon sheets on M2 screws into the tub's side-wall bosses.
The base panel carries the N10 cradle pedestals (the motors drop in from below with the panel off) and clears the
wheels; the top panel has a keyway over the switch (tool-free access, AWS), a slot clearing the weapon sweep and a
notch for the phase leads. Both are windowed out over the battery bay to hold the mass budget."""
import build123d as bd

from . import params as P
from . import tub as T
from ._reuse import plate

PANEL_HOLE_R = 1.3   # M2 clearance in the 1 mm sheet, wide enough for the countersink mouth
CSK_MOUTH_R = 2.0    # chamfer mouth under the base-panel screw heads (head rim dk 3.8 bears on the chamfer ring)
CSK_HOLE_R = 1.85     # clearance hole past the head cone: the head drops in and seats rim-flush with the bottom face
CSK_T = 0.1           # chamfer depth
WIN_EDGE = 29.0      # window edge in x: clear of the wheel wells (31.8) and the screw bosses (35.8)
WIN_BAY_Y0, WIN_BAY_Y1 = -8.0, 8.0     # battery-bay window split around the strap-post centreline
WIN_FRONT_Y1 = 30.0  # front window edge in y: clear of the front-wall pads and the switch
WIN_SWITCH_X1 = 17.0   # front window edge in x: clear of the switch (x 19.35..32.05)
_BAY_Y0 = P.TUB_Y0 + P.WALL
_BAY_Y1 = P.WHEEL_Y - P.WHEEL_OD / 2 - P.WHEEL_GAP
_CRADLE_FRONT = P.CRADLE_Y1 + 1.0
_BASE_WIN = ((-WIN_EDGE, WIN_BAY_Y0, _BAY_Y0, _BAY_Y1),
             (WIN_BAY_Y1, WIN_EDGE, _BAY_Y0, _BAY_Y1),
             (-WIN_EDGE, WIN_SWITCH_X1, _CRADLE_FRONT, WIN_FRONT_Y1))
_TOP_WIN = ((-WIN_EDGE, WIN_EDGE, _BAY_Y0, _CRADLE_FRONT),
            (WIN_BAY_Y1, WIN_SWITCH_X1, _CRADLE_FRONT, WIN_FRONT_Y1))


def _screw_axes():
    return [(sx * (P.TUB_W / 2 - P.WALL - P.PANEL_BOSS_T / 2), sy) for sx in (1, -1) for sy in P.PANEL_SCREW_Y]


def _sheet(t, z0):
    s = bd.extrude(bd.Plane.XY.offset(z0) * T._outline(), t)
    for x, y in _screw_axes():
        s = s - bd.Pos(x, y, z0 + t / 2) * bd.Cylinder(PANEL_HOLE_R, 2 * t)
    return s


def _windows(s, z0, spans):
    for x0, x1, y0, y1 in spans:
        s = s - bd.Pos((x0 + x1) / 2, (y0 + y1) / 2, z0 + 0.5) * bd.Box(x1 - x0, y1 - y0, 2.0)
    return s


def motor_pedestals():
    """Pads on the base panel the N10s rest on: can and gearbox pads, rising through the tub's pedestal slots."""
    out = []
    for side in (1, -1):
        mx = side * (P.WHEEL_X - P.WHEEL_W / 2 - P.DM_L / 2)
        can0, can1 = sorted((mx - side * P.CAN_X0_OFF, mx + side * P.CAN_X1_OFF))   # can span (mirrored)
        gb0, gb1 = sorted((mx + side * P.CAN_X1_OFF, mx + side * P.GB_FACE_OFF))    # gearbox span (mirrored)
        top = P.WHEEL_Z - P.DM_H / 2               # the motor's underside (can bottom)
        h = top - P.TUB_FLOOR_Z
        out.append(bd.Pos((can0 + can1) / 2, P.WHEEL_Y, P.TUB_FLOOR_Z + h / 2)
                   * bd.Box(can1 - can0 - P.CAN_PAD_TRIM, P.PED_PAD_W, h))
        out.append(bd.Pos((gb0 + gb1) / 2, P.WHEEL_Y, P.TUB_FLOOR_Z + h / 2)
                   * bd.Box(gb1 - gb0 - P.GB_PAD_TRIM, P.PED_PAD_W, h))
    return out


def base_panel():
    s = _sheet(P.PANEL_T_BASE, P.TUB_FLOOR_Z - P.PANEL_T_BASE)
    for w in drive_wells():
        s = s - w
    for x, y in _screw_axes():   # csk seat: a short chamfer the head rim bears on + a clearance hole past the head
        z0 = P.TUB_FLOOR_Z - P.PANEL_T_BASE
        s = s - bd.Pos(x, y, z0 + CSK_T / 2) * bd.Cone(CSK_MOUTH_R, CSK_HOLE_R, CSK_T)
        s = s - bd.Pos(x, y, z0 + P.PANEL_T_BASE / 2) * bd.Cylinder(CSK_HOLE_R, 2 * P.PANEL_T_BASE)
    s = _windows(s, P.TUB_FLOOR_Z - P.PANEL_T_BASE, _BASE_WIN)
    for p in motor_pedestals():
        s = s + p
    s.label = "panel_base"
    return s


def drive_wells():
    """Clearance for the tyres through the base panel (the wheels stand through it to the floor)."""
    import build123d as bd
    out = []
    for side in (1, -1):
        out.append(bd.Pos(side * P.WHEEL_X, P.WHEEL_Y, P.WHEEL_Z)
                   * bd.Box(P.WHEEL_W + 2 * P.WHEEL_GAP, P.WHEEL_OD + 2 * P.WHEEL_GAP, P.WHEEL_OD + 2 * P.WHEEL_GAP))
    return out


def top_panel():
    s = _sheet(P.PANEL_T_TOP, P.TUB_TOP_Z)
    sw = P.SW_AT
    s = s - bd.Pos(sw[0], sw[1], P.TUB_TOP_Z + P.PANEL_T_TOP / 2) * bd.Cylinder(P.SW_W / 3, 3 * P.PANEL_T_TOP)
    sweep = bd.Pos(0, P.TUB_Y1 - P.SWEEP_SLOT_Y / 2, P.TUB_TOP_Z + P.PANEL_T_TOP / 2) \
        * bd.Box(2 * P.DISC_SLOT_HALF, P.SWEEP_SLOT_Y, 2 * P.PANEL_T_TOP)
    s = s - sweep
    s = s - bd.Pos(P.NOTCH_X, P.TUB_Y1 - P.PAD_T / 2, P.TUB_TOP_Z + P.PANEL_T_TOP / 2) \
        * bd.Box(P.NOTCH_W, P.PAD_T + P.NOTCH_EXIT, 2 * P.PANEL_T_TOP + P.NOTCH_EXIT)   # phase-lead cable notch, matches the tub wall notch
    s = _windows(s, P.TUB_TOP_Z, _TOP_WIN)
    s.label = "panel_top"
    return s
