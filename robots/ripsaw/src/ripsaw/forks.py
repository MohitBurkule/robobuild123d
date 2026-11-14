"""Ripsaw forks: Revron's fork_5 laser part (1.5 mm Ti sheet) reused unchanged, hinged on an M3 pin on each rail's
outer face, free to swing so the tip rests on the floor (self-levelling). Same part both sides, no mirror (as Revron).
UNTESTED. Adversarial intent: forks get under wedges/forks first and feed the opponent up into the disc; a bent fork
is a two-screw swap. Start config: tips forward on the floor, inside the 4 inch cube (tip ahead of pin by FK_TIP[0],
the disc still leads). If a re-sized fork overhangs the cube, it may be hinged up for the size check (allowed: start
configuration), and drops on its own when the robot moves."""
import build123d as bd

from . import params as P
from ._reuse import revron_fork


def _fork_mod():
    fork, pd = revron_fork()
    return fork, pd


def pin_point(side):
    """M3 hinge pin axis point on the rail outer face; pin height puts the fork tip FORK_TIP_GAP above the floor."""
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


def pin_holes():
    _, pd = _fork_mod()
    return [bd.Pos(*pin_point(s)) * bd.Rot(0, 90, 0) * bd.Cylinder(P.FORK_PIN / 2, 3 * P.RAIL_T) for s in (1, -1)]
