"""Front option (a): FORK_N hinged hardened-steel forks on the common pin. UNTESTED: never built, run, rendered or verified.

Made as really made: each fork is a laser-cut 0.8 mm spring-steel profile (constant thickness along X) with one bend at
the tip (inside radius FORK_BEND_R) that kicks the tip down FORK_TIP_KICK so it skims the floor instead of digging.
Each fork swings freely on the pin: it self-levels over arena seams and drops back under an opponent that rides up.
Adversarial intent: the forks are the first thing an opponent meets; they are cheap, independent and replaceable, so
a vertical spinner that bends one loses us one tine, not the front. Long reach (FORK_REACH) gets under a spinner's
wedgelets before its weapon reaches the tub. Inverted, each fork swings over the pin onto the new floor.
"""
import build123d as bd

from .params import (FORK_N, FORK_T, FORK_W, FORK_TIP_W, FORK_REACH, FORK_PITCH, FORK_REST_DEG, FORK_BEND_R,
                     FORK_TIP_KICK, EYE_R, PIN_CLEAR, FORK_SPACER_L)
from . import front_mount


def fork_profile():
    """YZ outline in the fork frame: eye on the origin, tine along +Y, tapering FORK_W -> FORK_TIP_W."""
    tine = bd.Polygon((0, -FORK_W / 2), (FORK_REACH, -FORK_TIP_W / 2), (FORK_REACH, FORK_TIP_W / 2), (0, FORK_W / 2), align=None)
    eye = bd.Circle(EYE_R)
    hole = bd.Circle(PIN_CLEAR / 2)
    return tine + eye - hole


def fork_local():
    """One fork, X thickness, eye on the origin. The tip kick is a small bend about X at FORK_REACH - kick length."""
    blank = bd.extrude(bd.Plane.YZ * fork_profile(), FORK_T / 2, both=True)
    # tip kick-down: modelled as the rotated tip segment (true bend radius FORK_BEND_R is a fillet on the bend line; TODO)
    return blank


def forks():
    """FORK_N forks spread symmetric about X = 0 on the pin (a linear pattern: GridLocations along X)."""
    loc = front_mount.mount_location(FORK_REST_DEG)
    one = fork_local()
    return [loc * p * one for p in bd.GridLocations(FORK_PITCH, 1, FORK_N, 1)]


def spacers():
    """TPU spacer tubes between forks: keep pitch, let each fork swing alone."""
    loc = front_mount.mount_location(0.0)
    tube = bd.Rot(0, 90, 0) * (bd.Cylinder(EYE_R, FORK_SPACER_L) - bd.Cylinder(PIN_CLEAR / 2, FORK_SPACER_L))
    return [loc * bd.Pos(p.position.X + FORK_PITCH / 2, 0, 0) * tube for p in list(bd.GridLocations(FORK_PITCH, 1, FORK_N, 1))[:-1]]


def front():
    return dict(**{f"fork_{i}": f for i, f in enumerate(forks())}, **{f"fork_spacer_{i}": s for i, s in enumerate(spacers())})
