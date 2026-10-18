"""Drive train: gearmotors in clamshell pockets, printed D-bore wheels in open wheel slots (slide on from outside).

Geometry follows the verified reference wedge (robots/wedge_2wd): motors back to back on the axle line, gearbox face
against the wall between motor pocket and wheel slot, shaft through a 4 mm hole, wheel 2.45 mm outboard of the face.
"""

from __future__ import annotations

from dataclasses import dataclass

from . import sh

MOTORS = {
    # catalog id, body length (can + gearbox), body height, flats, shaft length
    "n10": dict(cat="n10_2200rpm_6v", L=21.1, h=12.0, flats=10.0, shaft=9.0),
    "n20": dict(cat="n20_1000rpm_6v", L=24.0, h=12.0, flats=10.0, shaft=10.0),
}
MOTOR_INNER_X = 5.85  # inner end of each motor (the 11.7 mm between them carries the wire channel)
FACE_TO_WHEEL = 2.45  # gearbox face to the inner face of the wheel
SIDE_MARGIN = 2.6  # outer face of the wheel to the outline


@dataclass
class DriveGeom:
    motor: str
    wheel_dia: float
    wheel_w: float
    axle_y: float

    @property
    def m(self):
        return MOTORS[self.motor]

    @property
    def motor_cx(self):
        return MOTOR_INNER_X + self.m["L"] / 2

    @property
    def face_x(self):
        return MOTOR_INNER_X + self.m["L"]

    @property
    def wheel_cx(self):
        return self.face_x + FACE_TO_WHEEL + self.wheel_w / 2

    @property
    def half_width(self):
        return self.wheel_cx + self.wheel_w / 2 + SIDE_MARGIN

    @property
    def radius(self):
        return self.wheel_dia / 2


def wheel_width(dia: float) -> float:
    return 10.0 if dia >= 25 else 8.0


def geom_for(h, axle_y: float) -> DriveGeom:
    return DriveGeom(h.drive_motor, float(h.wheel_dia), wheel_width(h.wheel_dia), axle_y)


def wheel_shape(dia: float, width: float) -> dict:
    """Printed hub with a 3 mm D-bore (flat 1.0 mm from the axis) inside a tyre ring; axis along x."""
    rt = dia / 2
    rim = sh.S(sh.cyl(rt, width, rot=(0, 90, 0)), sh.cyl(rt - 5.0, width + 2, rot=(0, 90, 0)))
    d_bore = {"type": "intersect", "items": [sh.cyl(1.5, width + 2, rot=(0, 90, 0)), sh.box(width + 2, 3.2, 2.6, (0, 0, -0.3))]}
    hub = sh.S(sh.cyl(rt - 4.5, width, rot=(0, 90, 0)), d_bore)
    return sh.U(rim, hub)


def add_drive(plan, g: DriveGeom):
    """Two motors + two wheels on one axle; pockets, slots, shaft holes; keep-outs and wire anchors for the layout."""
    zb, zt = plan.frame.zb, plan.frame.zt
    W = plan.frame.x1
    m = g.m
    for side, sgn in (("l", 1), ("r", -1)):
        mid, wid = f"motor_{side}", f"wheel_{side}"
        plan.part(id=mid, kind="motor", catalog=m["cat"], at=[sgn * g.motor_cx, g.axle_y, 0.0],
                  rot=[0.0, 0.0, 0.0 if sgn > 0 else 180.0], label=f"{'left' if sgn > 0 else 'right'} drive")
        plan.part(id=wid, kind="wheel", material="pla", process="fdm", shape=wheel_shape(g.wheel_dia, g.wheel_w),
                  at=[sgn * g.wheel_cx, g.axle_y, 0.0], print_orientation="+x",
                  mass_g=round(0.0045 * g.wheel_dia ** 2, 1),
                  label=f"{g.wheel_dia:g} x {g.wheel_w:g} mm wheel, printed hub with 3 mm D-bore, silicone tyre")
        reason = ("Printed hub with a D-bore matching the flat of the 3 mm gearmotor D-shaft: the flat carries drive "
                  "torque, the 0.1 mm interference only stops the hub walking off axially")
        plan.connect(mid, wid, "press_fit", reason, interference_mm=0.1, mechanical_key=True)
        plan.allow_overlap.append({"a": mid, "b": wid, "max_depth_mm": 0.6, "reason": (
            "The catalog shaft is modelled round; the real shaft has a D-flat 1.0 mm from the axis that the wheel's "
            "D-bore keys onto, so the flat of the bore overlaps the round stand-in by up to 0.5 mm")})
        # motor housing + cavity
        hx = sgn * (g.motor_cx + 0.2)
        housing = (m["L"] + 4.1, m["flats"] + 4.5)
        for half, zc in (("bottom", zb / 2), ("top", zt / 2)):
            hz = abs(zc * 2)
            plan.add(half, sh.box(housing[0], housing[1], hz, (hx, g.axle_y, zc)))
            plan.add(half, sh.box(g.wheel_w + 5.0, g.wheel_dia + 5.8, hz, (sgn * g.wheel_cx, g.axle_y, zc)))
        cav_h = m["h"] + 1.3
        plan.cut_both(sh.box(m["L"] + 0.3, m["flats"] + 0.3, cav_h, (sgn * g.motor_cx, g.axle_y, 0.0)))
        plan.cut_both(sh.box(3.3, 5.0, 3.5, (sgn * (MOTOR_INNER_X - 1.7), g.axle_y, 0.0)))  # terminal tab exit
        plan.cut_both(sh.cyl(2.0, 3.0, (sgn * (g.face_x + 1.15), g.axle_y, 0.0), (0, 90, 0)))  # shaft hole
        slot_h = max(-zb, zt) + 0.5
        plan.cut("bottom", sh.box(g.wheel_w + 2.0, g.wheel_dia + 3.0, slot_h, (sgn * g.wheel_cx, g.axle_y, zb + slot_h / 2 - 0.25)))
        plan.cut("top", sh.box(g.wheel_w + 2.0, g.wheel_dia + 3.0, slot_h, (sgn * g.wheel_cx, g.axle_y, zt - slot_h / 2 + 0.25)))
        side_x = sgn * (W - 0.35)
        plan.cut_both(sh.box(3.7, g.wheel_dia + 1.0, 2 * slot_h + 1, (side_x, g.axle_y, 0.0)))  # slide-on opening
        # keep-outs = the real housings: motor block and wheel block
        mx0, mx1 = sorted((hx - housing[0] / 2, hx + housing[0] / 2))
        plan.keepouts.append((f"drive_{side}", mx0, mx1, g.axle_y - housing[1] / 2, g.axle_y + housing[1] / 2))
        wx0, wx1 = sorted((sgn * (g.wheel_cx - (g.wheel_w + 5.0) / 2), sgn * (W + 0.5)))
        dy = (g.wheel_dia + 5.8) / 2
        plan.keepouts.append((f"wheel_{side}", wx0, wx1, g.axle_y - dy, g.axle_y + dy))
        plan.anchors[f"{mid}.terminals"] = (sgn * (MOTOR_INNER_X - 0.3), g.axle_y, 0.0)
        plan.extra.setdefault("approach", {})[f"{mid}.terminals"] = (sgn * 1.5, g.axle_y)
    # a transverse wire lane in front of the motors: every pocket can reach the motor terminals through it
    hy = (g.m["flats"] + 4.5) / 2
    plan.keepouts.append(("lane_drive", -plan.frame.x1, plan.frame.x1, g.axle_y + hy, g.axle_y + hy + 3.0))
    plan.keepouts.append(("drive_mid", -MOTOR_INNER_X, MOTOR_INNER_X, g.axle_y - 3.0, g.axle_y + 3.0))
