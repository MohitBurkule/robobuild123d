"""Ripsaw forks: Revron's fork_5 laser part (1.5 mm Ti sheet) reused unchanged, hinged on an M3 pin through each
weapon plate's outer face, free to swing so the tip rests on the floor (self-levelling). Same part both sides, no
mirror (as Revron).
Adversarial intent: forks get under wedges/forks first and feed the opponent up into the disc; a bent fork
is a two-screw swap. Start config: tips forward on the floor, inside the size limit (tip ahead of pin by FK_TIP[0],
the disc still leads)."""
import build123d as bd

from . import params as P
from ._reuse import revron_fork


def _fork_mod():
    fork, pd = revron_fork()
    return fork, pd


def pin_point(side):
    """M3 hinge pin axis point on the plate outer face; pin height puts the fork tip FORK_TIP_GAP above the floor."""
    _, pd = _fork_mod()
    x_face = P.RAIL_R_X[1] if side > 0 else P.RAIL_L_X[0]
    x = x_face + side * P.FORK_SIDE_CLR + (pd.FK_T if side > 0 else 0.0)   # sheet extrudes toward -X (w), see seat_plane
    return (x, P.Y_AX, P.FORK_TIP_GAP + pd.FK_TIP[1])


def seat_plane(side):
    """Fork frame: u back along the blade = robot -Y, v up, w = robot -X (Revron convention, same part both sides)."""
    return bd.Plane(origin=pin_point(side), x_dir=(0, -1, 0), z_dir=(-1, 0, 0))


def fork(side):
    fork_mod, _ = _fork_mod()
    s = fork_mod.fork_local()                         # reused: revron/fork.py fork_local (laser outline, FK_T sheet)
    s = s.moved(bd.Location(seat_plane(side)))
    s.label = f"fork_{'r' if side > 0 else 'l'}"
    return s


def pin(side):
    """The M3 hinge pin part: through the plate and the fork sheet, press fit in the plate."""
    x_face = P.RAIL_R_X[1] if side > 0 else P.RAIL_L_X[0]
    x_out = x_face + side * (P.FORK_SIDE_CLR + 1.5 + 1.0)   # through the fork sheet (1.5) plus a grip land
    x_in = x_face - side * 1.0
    lo, hi = sorted((x_out, x_in))
    s = bd.Pos((lo + hi) / 2, P.Y_AX, pin_point(side)[2]) * bd.Rot(0, 90, 0) * bd.Cylinder(P.FORK_PIN / 2, hi - lo)
    s.label = f"fork_pin_{'r' if side > 0 else 'l'}"
    return s
