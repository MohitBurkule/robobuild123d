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

FOOT_R = P.SHAFT_D       # mm: covers the M5 nut across flats (8 mm) with a lip; see BRIEF unsure list
DOME_H = P.MIN_GROUND_CLR + P.SKID_H   # mm proud of the top panel


def _z_cyl(r, h):
    return bd.Cylinder(r, h, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def foot():
    """World frame: floor z = 0 up to the bar underside, on the weapon axis."""
    return bd.Pos(0, P.WPN_AXIS_Y, 0) * _z_cyl(FOOT_R, P.BAR_Z0)


def dome():
    return bd.Pos(0, P.WPN_AXIS_Y, P.TUB_TOP_Z) * _z_cyl(P.SKID_D / 2, DOME_H)


def parts():
    return {"skid_foot": foot(), "skid_dome": dome()}
