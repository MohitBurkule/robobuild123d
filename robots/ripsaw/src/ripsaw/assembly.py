"""Ripsaw assembly: parts placed by joints/frames from params relations. UNTESTED.
`build(part)` is the single geometry entry point used by spec.json model parts (mirrors revron/assembly.build)."""
import build123d as bd

from . import params as P
from . import tub as T, disc as D, weapon_mount as WMt, forks as F, panels as PN, drive as DR
from ._reuse import hw


def _tub():
    s = T.tub()
    for h in F.pin_holes():
        s = s - h
    return s


def disc_placed():
    """Disc on the axle: its own frame moved to weapon_mount.disc_frame (the tub's `axle` joint is the spin axis)."""
    return D.disc().moved(WMt.disc_frame())


PARTS = {
    "tub": _tub,
    "disc": D.disc,                 # own frame (spec places it on the axle with rotates_with = weapon)
    "disc_placed": disc_placed,
    "fork_r": lambda: F.fork(1),
    "fork_l": lambda: F.fork(-1),
    "panel_base": PN.base_panel,
    "panel_top": PN.top_panel,
}


def build(part, origin=None):
    s = PARTS[part]()
    if origin:
        s = s.moved(bd.Location(tuple(-float(v) for v in origin)))
    return s


def assembly():
    parts = [build(k) for k in ("tub", "disc_placed", "fork_r", "fork_l", "panel_base", "panel_top")]
    cots = [hw.placed(P.WEAPON_MOTOR, tuple(WMt.motor_frame().position), (0, 0, 0))]
    for side in (1, -1):
        loc = DR.motor_at(side)
        cots.append(hw.placed(P.DRIVE_MOTOR, tuple(loc.position), tuple(loc.orientation)))
    for cid, loc in T.bay_locations().items():
        cots.append(hw.placed(cid, tuple(loc.position), tuple(loc.orientation)))
    return bd.Compound(children=parts + cots)
