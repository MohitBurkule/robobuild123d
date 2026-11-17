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


def foot():
    """World frame: floor z = 0 up to the bar underside, on the weapon axis."""
    return bd.Pos(0, P.WPN_AXIS_Y, 0) * _z_cyl(FOOT_R, P.BAR_Z0)


def dome():
    """Turned POM button on the top panel over the weapon axis, with the M2 dome-screw clearance through it."""
    button = _z_cyl(P.SKID_D / 2, DOME_H)
    return bd.Pos(0, P.WPN_AXIS_Y, P.TUB_TOP_Z) * (button - _z_cyl(P.DOME_SCREW_CLR_D / 2, DOME_H))


CASTER_Y = P.WPN_AXIS_Y + P.TUB_R - 8.0   # mm: under the tub front, ahead of the CoM (tub front edge at WPN_AXIS_Y + TUB_R)
CASTER_R = 4.0                            # mm: ball radius (8 mm ball caster)
CASTER_TOP_Z = 5.0                        # mm: top of the caster housing, below the tub floor (tub_floor_z)


def caster():
    """Ball-caster button under the tub front: a ball of radius CASTER_R cut flat at CASTER_TOP_Z, so the bottom is the
    floor contact and the top stays clear of the tub floor."""
    ball = bd.Pos(0, CASTER_Y, CASTER_R) * bd.Sphere(CASTER_R)
    return ball & bd.Pos(0, CASTER_Y, 0) * _z_cyl(CASTER_R + 1, CASTER_TOP_Z)


def parts():
    return {"skid_foot": foot(), "skid_dome": dome(), "caster": caster()}
