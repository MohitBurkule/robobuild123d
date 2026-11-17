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

DOME_H = P.MIN_GROUND_CLR + P.SKID_H   # mm proud of the top panel


def _z_cyl(r, h):
    return bd.Cylinder(r, h, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


ARM_CLR_FLOOR = 1.1    # mm: arm underside above the floor (profile ground clearance 1.0 + margin)
ARM_CLR_BAR = 1.1      # mm: arm top under the bar underside (kin.rub_gap wants 1.0 mm for a weapon)
ARM_W = 10.0           # mm strip width = puck diameter; bar-bolt driver path (x 5.65 .. 9.35 at PCD 15) stays clear
ARM_RISER_Y = (-54.0, -46.0)   # mm: behind the bar sweep (rearmost sweep y = axis - r = -42.5); sits on the pod floor underside
BEARING_OD_R = 4.0     # mm MR85 outer radius (bearing seat in the puck)
BEARING_W = 2.5        # mm MR85 width
SHAFT_R = P.SHAFT_D / 2


def foot():
    """Skid arm (kind structure, FDM nylon, world frame): a 2.8 mm strip along the centre line from the pod floor underside
    (a riser behind the bar sweep) forward UNDER the whole sweep disc to a round puck on the weapon axis. The bar passes over it
    with a 1.1 mm gap; the puck's bore holds the MR85 bearing whose inner race rides the 5 mm weapon shaft. This is the only
    way a static part can reach the axis below the bar: it comes in under the sweep, not through it."""
    z0, z1 = ARM_CLR_FLOOR, P.BAR_Z0 - ARM_CLR_BAR
    y0 = ARM_RISER_Y[0]
    strip = bd.Pos(0, (y0 + P.WPN_AXIS_Y) / 2, z0) * bd.Box(ARM_W, P.WPN_AXIS_Y - y0, z1 - z0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    puck = bd.Pos(0, P.WPN_AXIS_Y, z0) * _z_cyl(ARM_W / 2, z1 - z0)
    riser = bd.Pos(0, sum(ARM_RISER_Y) / 2, z0) * bd.Box(ARM_W, ARM_RISER_Y[1] - ARM_RISER_Y[0], P.tub_floor_z() - z0,
                                                       align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))
    arm = strip + puck + riser
    bore = bd.Pos(0, P.WPN_AXIS_Y, z0 - 1) * _z_cyl(BEARING_OD_R, z1 - z0 + 2)
    return arm - bore


def bearing():
    """World frame: MR85 5 x 8 x 2.5 (robot.catalog.BEARINGS 'mr85'), centred in the arm's puck bore."""
    z0, z1 = ARM_CLR_FLOOR, P.BAR_Z0 - ARM_CLR_BAR
    z = z0 + (z1 - z0 - BEARING_W) / 2
    return bd.Pos(0, P.WPN_AXIS_Y, z) * (_z_cyl(BEARING_OD_R, BEARING_W) - _z_cyl(SHAFT_R, BEARING_W))


def shaft_top_z():
    """Shaft top: inside the stator bore, 1.1 mm under the stator base's top face (the motor's own bearings carry it there)."""
    return P.wpn_motor_z() + 10.4 - 1.1


def shaft():
    """World frame: the 5 mm weapon shaft on the axis, from the arm underside up through the bearing, the bar bore, the hub
    and the bell into the stator bore (the motor's own shaft extended: motor-as-hub on the top side)."""
    return bd.Pos(0, P.WPN_AXIS_Y, ARM_CLR_FLOOR) * _z_cyl(SHAFT_R, shaft_top_z() - ARM_CLR_FLOOR)


DOME_STEM_R = 1.45     # mm: the dome's stem plugs into a 3 mm hole in the top panel (snap; no screw, the axis is the shaft's)


def dome():
    """Turned POM button on the top panel over the weapon axis (inverted front contact), plugged into a 3 mm panel hole."""
    button = _z_cyl(P.SKID_D / 2, DOME_H)
    stem = bd.Pos(0, 0, -P.TOP_PANEL_T) * _z_cyl(DOME_STEM_R, P.TOP_PANEL_T)
    return bd.Pos(0, P.WPN_AXIS_Y, P.TUB_TOP_Z) * (button + stem)


def lock_pin():
    """Rule 5f lock: a steel pin dropped down through the bar's lock hole into the tub floor's underside (removable,
    tethered; pulled before a fight). It sits off the axis, so the hub and shaft are not involved."""
    from . import tub
    return bd.Pos(P.LOCK_PIN_R, P.WPN_AXIS_Y, 0) * _z_cyl(P.LOCK_PIN_D / 2, tub.z0())


def parts():
    return {"skid_arm": foot(), "bearing_caster": bearing(), "weapon_shaft": shaft(), "skid_dome": dome(), "lock_pin": lock_pin()}
