"""[fix-B-vers] The weapon motor as ONE catalog setting: everything the weapon fits to the motor is read here from that
one catalog entry (robot/catalog.py, robot/cots_alts.py), never from GR1507 constants.

A motor entry either names its rotating half (`rotor_part`: gr1507 -> gr1507_can, gr1507_step -> gr1507_step_can) or
is a one-piece outrunner that declares its mounting geometry (props body_x, bell_len), which the catalog splits into a
fixed half and a bell (catalog.split_outrunner: `<id>__fixed` / `<id>__bell`). Either way the robot gets the same two
parts (weapon_motor_stator / weapon_motor_can), and these features, all in the catalog frame (+X = bell top):

  back_x       stator base back face (it sits on the motor back spacer)
  cap_x        bell cap face (the spider sits on it)
  bell_r       bell outer radius (drisk spacer bore)
  base_h       base flange thickness (the stator screws bite into it)
  base_hub_r   hub / rear boss radius behind the base (back spacer bore)
  base_holes   [(r, local deg, screw d)] stator screws (RV03 counterbores, back spacer holes)
  top_holes    [(r, local deg, screw d)] bell-top screws (spider)
  shaft_r      motor shaft radius (spider bore, RV03 bore, outboard bearing)
  thread_len   threaded length of the shaft's free end (0 = plain)
  core_r       solid rotor core radius the drawn shaft passes through (STEP-simplified bell), else 0
"""
import math

from robot import catalog as C


class WeaponMotorError(ValueError):
    """The selected weapon motor cannot be fitted: a clear reason, raised at spec generation."""


def _holes(rows, what, cid):
    out = []
    for row in rows or []:
        if len(row) < 3:
            raise WeaponMotorError(f"weapon motor `{cid}`: {what} row {row} is not [pitch circle d, count, screw d, phase]")
        pcd, n, d = float(row[0]), int(row[1]), float(row[2])
        ph = float(row[3]) if len(row) > 3 else 45.0          # robot.cots_alts.bolt_circle default phase
        out += [(pcd / 2, ph + 360.0 * k / n, d) for k in range(n)]
    return out


def describe(cid: str) -> dict:
    """Fitting features of weapon motor `cid` (see the module doc). Raises WeaponMotorError with the reason when the
    entry is unknown, not a weapon motor, or does not declare what the weapon needs."""
    e = C.find(cid)
    if e is None:
        raise WeaponMotorError(f"weapon motor `{cid}` is not in the catalog")
    if e.kind != "weapon_motor" or (e.props or {}).get("half_of"):
        raise WeaponMotorError(f"`{cid}` is not a weapon motor entry (kind {e.kind!r})")
    pr = e.props or {}
    if pr.get("rotor_part"):
        stator, can = e.id, pr["rotor_part"]
    else:
        halves = C.split_outrunner(e)
        if not halves:
            raise WeaponMotorError(f"weapon motor `{cid}` is one piece and declares no mounting geometry (props body_x, bell_len, "
                                   f"mount_holes, top_holes): its fixed half and bell cannot be told apart")
        stator, can = halves[0].id, halves[1].id
    miss = [k for k in ("body_x", "bell_r", "mount_holes", "top_holes") if not pr.get(k)]
    if miss:
        raise WeaponMotorError(f"weapon motor `{cid}` does not declare {', '.join(miss)}: the mounts and the spider cannot be drilled for it")
    if not e.shaft:
        raise WeaponMotorError(f"weapon motor `{cid}` has no shaft entry")
    tops = _holes(pr["top_holes"], "top_holes", cid)
    if len({(round(r, 6), d) for r, _, d in tops}) != 1:
        raise WeaponMotorError(f"weapon motor `{cid}`: the spider takes one bell-top screw circle, the entry has {pr['top_holes']}")
    can_e = C.find(can)
    return dict(id=e.id, stator=stator, can=can, back_x=float(pr["body_x"][0]), cap_x=float(pr["body_x"][1]),
                bell_r=float(pr["bell_r"]), base_h=float(pr.get("base_h", 2.0)), base_hub_r=float(pr.get("base_hub_r", e.shaft["dia"] / 2 + 1.0)),
                base_holes=_holes(pr["mount_holes"], "mount_holes", cid), top_holes=tops, shaft_r=float(e.shaft["dia"]) / 2,
                thread_len=float(pr.get("shaft_thread_mm", 0.0)), core_r=float(((can_e.props or {}) if can_e else {}).get("solid_core_r", 0.0)))


def world_holes(holes):
    """[(dY, dZ, d)] of catalog-frame holes about the weapon axis in the chassis side view: the motor sits in the
    weapon frame turned half a turn about Z (MOTOR_FLIP), so local (y, z) -> (-y, z). Sorted by pattern circle, then
    by angle from 0 deg, so a pattern reads the same whichever way the catalog clocks it."""
    out = []
    for r, a, d in holes:
        dy, dz = -r * math.cos(math.radians(a)), r * math.sin(math.radians(a))
        dy, dz = (0.0 if abs(dy) < 1e-9 else round(dy, 9)), (0.0 if abs(dz) < 1e-9 else round(dz, 9))
        out.append((round(r, 6), round(math.degrees(math.atan2(dz, dy)) % 360.0, 6) % 360.0, dy, dz, d))
    return [(dy, dz, d) for _, _, dy, dz, d in sorted(out)]


def pick_bearing(shaft_d, bearings=None):
    """Outboard bearing for a shaft of diameter shaft_d: the catalog bearing with that bore and the smallest OD (MR85
    for the 5 mm GR1507). Raises WeaponMotorError when the catalog has none."""
    bearings = bearings or C.BEARINGS
    fit = sorted((od, w, name) for name, (bore, od, w) in bearings.items() if abs(bore - shaft_d) < 1e-6 and not name.startswith(("mf", "f")))
    if not fit:
        raise WeaponMotorError(f"no outboard bearing in robot.catalog.BEARINGS for a {shaft_d:g} mm weapon shaft")
    return "mr85" if abs(shaft_d - 5.0) < 1e-6 and "mr85" in bearings else fit[0][2]
