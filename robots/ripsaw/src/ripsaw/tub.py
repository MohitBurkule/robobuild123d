"""Ripsaw tub: printed nylon unibody (walls + weapon rails), open top and bottom closed by panels. UNTESTED.
Print orientation: +Z (rails stand up, no support under the bearing boss bridge except the 6 mm seat).

Pockets for COTS parts come from robot.cad.bay.derive_bay (catalogue envelopes), so swapping a catalogue part moves
its pocket. Battery lies across the body behind the disc slot; ESCs/switch beside it; all inside the walls."""
import build123d as bd

from robot import catalog as C
from robot.cad.bay import derive_bay

from . import params as P
from . import weapon_mount, drive
from ._reuse import plate

# placements of the electronics in the body (relations: behind the disc slot, centred, on the floor ring)
_SLOT_REAR = P.Y_AX - P.DISC_R - 2 * P.MOVING_CLR


def _outline(grow=0.0):
    f = bd.Rectangle(P.TUB_W + 2 * grow, P.TUB_BODY_L + 2 * grow)
    return plate.round_corners(f.faces()[0], r_out=P.CORNER_R + grow)


def shell():
    outer = bd.extrude(bd.Plane.XY.offset(P.TUB_FLOOR_Z) * _outline(), P.TUB_H)
    inner = bd.extrude(bd.Plane.XY.offset(P.TUB_FLOOR_Z - 1) * _outline(-P.WALL), P.TUB_H + 2)
    return outer - inner


def bay_locations():
    """World placements (part frames) of the bay parts: id -> Location."""
    bat_y = (P.TUB_Y0 + P.WALL + _SLOT_REAR) / 2
    return {
        P.BATTERY: bd.Location((0, bat_y, P.TUB_FLOOR_Z + P.PANEL_T_BASE + P.BAT_H / 2)),
        P.WEAPON_ESC: bd.Location((-(P.TUB_W / 2 - P.WALL - P.WESC_W), P.TUB_Y1 - P.WESC_L, P.TUB_TOP_Z - P.WESC_H)),
        P.DRIVE_ESC: bd.Location((0, bat_y, P.TUB_TOP_Z - P.PANEL_T_TOP - P.DESC_H)),
        P.SWITCH: bd.Location((P.TUB_W / 2 - P.WALL - P.SW_W, P.TUB_Y1 - P.SW_L, P.TUB_TOP_Z - P.SW_H)),  # under a top-panel hole
    }


def bays():
    return {cid: derive_bay(C.find(cid), placement=loc, insert_dir="-z" if cid != P.BATTERY else "+z")
            for cid, loc in bay_locations().items()}


def insert_points():
    """Heat-set insert axes for the panels: one side by GridLocations, mirrored."""
    x = P.TUB_W / 2 - P.PANEL_SCREW_INSET
    pitch = (P.TUB_BODY_L - 2 * P.PANEL_SCREW_INSET) / (P.PANEL_SCREW_N_SIDE - 1)
    pts = [(x, loc.position.Y) for loc in bd.GridLocations(0, pitch, 1, P.PANEL_SCREW_N_SIDE)]
    return pts + [(-px, py) for px, py in pts]


def tub():
    s = shell() + weapon_mount.rails()
    for c in weapon_mount.cuts() + drive.wells_and_pockets():
        s = s - c
    for b in bays().values():
        s = s - b.cut_solid()
    for x, y in insert_points():   # inserts from top and bottom into the wall
        for z0 in (P.TUB_FLOOR_Z, P.TUB_TOP_Z - P.INSERT_L):
            s = s - bd.Pos(x, y, z0 + P.INSERT_L / 2) * bd.Cylinder(P.INSERT_D / 2, P.INSERT_L)
    s.label = "tub"
    bd.RigidJoint("origin", s, bd.Location())
    bd.RigidJoint("motor", s, weapon_mount.motor_frame())
    bd.RevoluteJoint("axle", s, axis=bd.Axis((0, P.Y_AX, P.Z_AX), (1, 0, 0)))
    return s
