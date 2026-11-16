"""Two low-friction skids: the front support for each way up.

2WD with the wheels behind the sweep and the weapon motor ahead of the axle puts the CoM ahead of the wheels, so the
front needs a third contact. Nothing fixed may cross the bar plane inside the sweep, so:
  foot  - turned POM cap threaded M5 onto the weapon shaft end under the bar, on the axis (it spins with the bar; at
          r = FOOT_OD/2 the rubbing torque is tiny). Upright front contact; sets BAR_Z0 exactly (floor -> foot ->
          bar underside). The shaft thread and the tapped POM capture it: no glue, and it unscrews for service.
  dome  - turned POM button screwed to the top panel over the weapon axis. Inverted front contact; keeps the
          (now overhead) bar plane clear of the floor and the top panel off it.
Adversarial intent: both are on the axis, so a hit cannot lever them off; a lost foot drops the bar onto the floor
(risk listed in BRIEF.md) - the foot is captured by the shaft thread, not glued.
"""
import build123d as bd

from . import params as P

DOME_H = P.MIN_GROUND_CLR + P.SKID_H   # mm proud of the top panel


def _z_cyl(r, h):
    return bd.Cylinder(r, h, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def foot():
    """World frame: floor z = 0 up to the bar underside, on the weapon axis; M5 tap bore for the shaft thread."""
    cap = bd.Pos(0, P.WPN_AXIS_Y, 0) * _z_cyl(P.FOOT_OD / 2, P.BAR_Z0)
    return cap - bd.Pos(0, P.WPN_AXIS_Y, -0.5) * _z_cyl(P.FOOT_BORE_R, P.BAR_Z0 + 1)


def dome():
    return bd.Pos(0, P.WPN_AXIS_Y, P.TUB_TOP_Z) * _z_cyl(P.SKID_D / 2, DOME_H)


def parts():
    return {"skid_foot": foot(), "skid_dome": dome()}
