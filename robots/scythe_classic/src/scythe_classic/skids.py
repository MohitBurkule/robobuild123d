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


FOOT_R_OUT = 5.0       # mm caster puck outer radius (1.0 mm wall; 0.6 failed the uhmw thin-wall rule)
BEARING_OD_R = 4.0     # mm MR85 outer radius (bearing seat in the puck)
BEARING_W = 2.5        # mm MR85 width
SHAFT_R = P.SHAFT_D / 2


def foot():
    """World frame: a caster puck on the weapon axis (kind caster), bottom FOOT_CLR_FLOOR above the floor and top
    FOOT_CLR_BAR under the bar underside. Its bore holds an MR85 bearing (outer ring pressed in the puck); the inner
    ring rides the 5 mm weapon shaft, so the puck stays put on touch and the shaft turns in it. Not part of the rotor."""
    h = P.BAR_Z0 - FOOT_CLR_BAR - FOOT_CLR_FLOOR
    ring = _z_cyl(FOOT_R_OUT, h) - _z_cyl(BEARING_OD_R, h)
    return bd.Pos(0, P.WPN_AXIS_Y, FOOT_CLR_FLOOR) * ring


def bearing():
    """World frame: MR85 5 x 8 x 2.5 (robot.catalog.BEARINGS 'mr85'), centred in the caster puck bore."""
    h = P.BAR_Z0 - FOOT_CLR_BAR - FOOT_CLR_FLOOR
    z = FOOT_CLR_FLOOR + (h - BEARING_W) / 2
    return bd.Pos(0, P.WPN_AXIS_Y, z) * (_z_cyl(BEARING_OD_R, BEARING_W) - _z_cyl(SHAFT_R, BEARING_W))


def shaft():
    """World frame: the 5 mm weapon shaft on the axis, from the puck's bottom up to the hub top. It runs through the
    bar bore, the hub bore and the bearing; the GR1507 can (rotor) sits on the hub top."""
    top = P.bar_top_z() + P.HUB_GAP + P.HUB_H
    return bd.Pos(0, P.WPN_AXIS_Y, FOOT_CLR_FLOOR) * _z_cyl(SHAFT_R, top - FOOT_CLR_FLOOR)


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
    return {"skid_foot": foot(), "bearing_caster": bearing(), "weapon_shaft": shaft(), "skid_dome": dome(), "lock_pin": lock_pin()}
