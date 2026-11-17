"""Two low-friction skids: the front support for each way up. UNTESTED.

2WD with the wheels behind the sweep and the weapon motor ahead of the axle puts the CoM ahead of the wheels, so the
front needs a third contact. Nothing fixed may cross the bar plane inside the sweep, so:
  foot  - turned POM cap on the M5 shaft end under the bar, on the axis (it spins with the bar; at r = FOOT_R the
          rubbing torque is tiny). Upright front contact; sets BAR_Z0 exactly (floor -> foot -> bar underside).
  dome  - turned POM button screwed to the top panel over the weapon axis. Inverted front contact; keeps the
          (now overhead) bar plane BAR_Z0 + ... clear of the floor and the top panel off it.
Adversarial intent: both are on the axis, so a hit cannot lever them off; a lost foot drops the bar onto the floor
(risk listed in BRIEF.md) - the foot is captured by the shaft nut, not glued.
"""
import build123d as bd

from . import params as P

FOOT_R = P.SHAFT_D / 2   # mm: the shaft-end radius; M3 bar-bolt heads at r 5.5 clear it (a wider foot would not)
DOME_H = P.MIN_GROUND_CLR + P.SKID_H   # mm proud of the top panel


def _z_cyl(r, h):
    return bd.Cylinder(r, h, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


FOOT_CLR_FLOOR = 0.5   # mm: the caster puck rests this far above the floor when level
FOOT_CLR_BAR = 0.5     # mm: and stays this far under the bar underside (bar spins over it)


def foot():
    """World frame: a caster puck on the weapon axis (kind caster), bottom FOOT_CLR_FLOOR above the floor and top
    FOOT_CLR_BAR under the bar underside. It rides the shaft end on a small bearing (bore on the shaft), so its outer
    ring can stop turning when it touches the floor; it is not part of the rotor."""
    h = P.BAR_Z0 - FOOT_CLR_BAR - FOOT_CLR_FLOOR
    return bd.Pos(0, P.WPN_AXIS_Y, FOOT_CLR_FLOOR) * _z_cyl(FOOT_R, h)


def dome():
    """Turned POM button on the top panel over the weapon axis, with the M2 dome-screw clearance through it."""
    button = _z_cyl(P.SKID_D / 2, DOME_H)
    return bd.Pos(0, P.WPN_AXIS_Y, P.TUB_TOP_Z) * (button - _z_cyl(P.DOME_SCREW_CLR_D / 2, DOME_H))


def lock_pin():
    """Rule 5f lock: a steel pin dropped down through the bar's lock hole into the tub floor's underside (removable,
    tethered; pulled before a fight). It sits off the axis, so the hub and shaft are not involved."""
    from . import tub
    return bd.Pos(P.LOCK_PIN_R, P.WPN_AXIS_Y, 0) * _z_cyl(P.LOCK_PIN_D / 2, tub.z0())


def parts():
    return {"skid_foot": foot(), "skid_dome": dome(), "lock_pin": lock_pin()}
