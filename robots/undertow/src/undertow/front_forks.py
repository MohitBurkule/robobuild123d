"""Front option (a): FORK_N hinged hardened-steel forks on the common pin.

Each fork is a laser-cut 0.8 mm spring-steel profile (constant thickness along X) with the eye on the pin. Each swings
freely on the pin: it self-levels over arena seams and drops back under an opponent that rides up. Inverted, the forks
swing over the pin onto the new floor. The rest angle is solved so the tine's lower tip corner sits FRONT_TIP_GAP over
the floor (rules wedge_gap 0.2..1.5) and inside the rules wedge-angle band.
"""
import build123d as bd

from .params import (FORK_N, FORK_T, FORK_W, FORK_TIP_W, FORK_REACH, FORK_PITCH, FORK_SPAN, FORK_REST_DEG, EYE_R, PIN_CLEAR)
from . import front_mount


def fork_profile():
    """YZ outline in the fork frame: eye on the origin, tine along +Y, tapering FORK_W -> FORK_TIP_W."""
    tine = bd.Polygon((0, -FORK_W / 2), (FORK_REACH, -FORK_TIP_W / 2), (FORK_REACH, FORK_TIP_W / 2), (0, FORK_W / 2), align=None)
    eye = bd.Circle(EYE_R)
    hole = bd.Circle(PIN_CLEAR / 2)
    return tine + eye - hole


def fork_local():
    """One fork, X thickness, eye on the origin; the tine root corners are radiused >= the laser kerf."""
    blank = bd.extrude(bd.Plane.YZ * fork_profile(), FORK_T / 2, both=True)
    root = [e for e in blank.edges().filter_by(bd.Axis.X) if e.center().Y < FORK_W / 2]
    return blank.fillet(0.5, root) if root else blank


def fork_xs():
    """X positions of the FORK_N forks, symmetric about X = 0."""
    if FORK_N == 1:
        return [0.0]
    return [(-FORK_SPAN / 2 + i * FORK_PITCH) for i in range(FORK_N)]


def forks():
    """FORK_N forks spread symmetric about X = 0 on the pin, tipped to their resting angle."""
    loc = front_mount.mount_location(FORK_REST_DEG)
    one = fork_local()
    return [loc * bd.Pos(x, 0, 0) * one for x in fork_xs()]


def front():
    return {f"fork_{i}": f for i, f in enumerate(forks())}
