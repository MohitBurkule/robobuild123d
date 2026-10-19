"""Servo lifter: a printed U-shaped lifting scoop pivoting about a lateral axis near the front.

The servo lies inside the chassis against the right side wall with its output along +x; the scoop's right cheek
carries a hub that passes through a hole in the wall onto the servo spline (the joint is parented to the servo). The
left cheek turns on an M2 pivot screw on the same axis, into an insert in the left wall. The scoop plate sits in front
of the chassis, its lip just off the floor; raising it turns the front edge up and away from the body.
"""

from __future__ import annotations

import math

from shapely.geometry import MultiPoint

from . import sh
from .plan import Pocket
from .pockets import GAP, HOUSING
from .weapon import module

SERVO = "servo_cs07"
SERVO_SIZE = (22.0, 11.5, 20.0)  # catalog box (x, y, z); output along local z
PIVOT_BACK = 14.5  # pivot behind the chassis front
CHEEK_T = 3.0
HUB_R = 2.2
SCOOP_T = 2.5
SCOOP_LEN = 22.0
LIP_GAP = 0.5
LIP_T = 0.8
RANGE_DEG = 35.0


def _circle(c, r, n=20):
    import math
    return [(c[0] + r * math.cos(2 * math.pi * i / n), c[1] + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


@module("lifter")
class Lifter:
    @staticmethod
    def geometry(plan):
        f = plan.frame
        floor = plan.extra["_floor_z"]
        yp = f.y1 - PIVOT_BACK
        zp = f.zb + f.floor + GAP + SERVO_SIZE[1] / 2 + 0.1  # servo resting on the floor
        x_face = f.x1 + 0.3  # servo output face flush with the outside of the right wall (it sits in a wall window)
        return yp, zp, x_face, floor

    @classmethod
    def prepare(cls, plan, h, g):
        plan.extra["servo"] = "servo"
        plan.robot_type = "lifter"
        plan.archetype = "lifter"
        yp, zp, x_face, _ = cls.geometry(plan)
        sx, sy, sz = SERVO_SIZE
        x0 = x_face - sz
        plan.keepouts.append(("servo", x0 - GAP - HOUSING, plan.frame.x1, yp - sx / 2 - GAP - HOUSING, yp + sx / 2 + GAP + HOUSING))
        plan.keepouts.append(("boss_pivot", -plan.frame.x1, -plan.frame.x1 + 6.5, yp - 3.5, yp + 3.5))
        plan.anchors["servo.signal"] = ((x0 + x_face) / 2, yp - sx / 2, zp)
        plan.extra.setdefault("approach", {})["servo.signal"] = ((x0 + x_face) / 2, yp - sx / 2 - GAP - HOUSING - 1.5)

    @classmethod
    def add(cls, plan, h, g):
        f = plan.frame
        yp, zp, x_face, floor = cls.geometry(plan)
        sx, sy, sz = SERVO_SIZE
        W = f.x1
        xc = x_face - sz / 2
        # servo: local z (output) -> world +x, local x -> world y, local y -> world z
        plan.part(id="servo", kind="servo", catalog=SERVO, at=[xc, yp, zp], rot=[90.0, 0.0, 90.0], retained="captive",
                  ports={"signal": [-sx / 2, 0.0, 0.0]},
                  label="CS07 micro servo on its side, output through the right wall (BEC 5 V from the receiver lead)")
        pk = Pocket("servo", xc - sz / 2 - GAP, W - f.wall, yp - sx / 2 - GAP, yp + sx / 2 + GAP,
                    zp - sy / 2 - GAP, zp + sy / 2 + GAP, HOUSING)
        sig_y = yp - sx / 2
        pk.notches.append((xc - 1.6, xc + 1.6, sig_y - 2.0, sig_y + 0.5, min(zp - 1.6, -1.0), max(zp + 1.6, 1.0)))
        plan.pockets.append(pk)
        # window in the right wall for the servo: its output face sits just outside, in the cheek's plane, so nothing
        # of the scoop has to pass through the wall
        win = sh.boxr(W - f.wall - 0.5, W + 0.5, yp - sx / 2 - GAP, yp + sx / 2 + GAP, zp - sy / 2 - GAP, zp + sy / 2 + GAP)
        plan.cut("bottom", win)
        plan.cut("top", win)
        plan.add("bottom", sh.cyl_axis(3.0, -W, -W + 6.0, "x", yp, zp))
        plan.late_cuts["bottom"].append(sh.cyl_axis(1.0, -W - 0.2, -W + 4.6, "x", yp, zp))
        # the scoop: two cheeks outside the side walls + the plate in front of the chassis
        xo = W + 0.4 + CHEEK_T
        # the plate's back edge clears the front wall over the whole lift (it swings up about the pivot)
        y_back = yp + (f.y1 + 0.8 - yp) / math.cos(math.radians(RANGE_DEG + 5.0))
        y_tip = f.y1 + SCOOP_LEN
        z_tip = floor + LIP_GAP
        top_back = (y_back, zp + 1.0)
        top_tip = (y_tip, z_tip + 1.0)
        plate = [(y_back, top_back[1] - SCOOP_T - 2.0), top_back, top_tip, (y_tip, z_tip)]
        cheek = list(MultiPoint(_circle((yp, zp), 5.0) + [top_back, (y_back + 3.0, top_back[1]),
                                                          (y_back + 3.0, top_back[1] - SCOOP_T - 2.0),
                                                          (y_back, top_back[1] - SCOOP_T - 2.0)]).convex_hull.exterior.coords)[:-1]
        body = sh.U(sh.side_prism(plate, -xo, xo), sh.side_prism(cheek, W + 0.4, xo), sh.side_prism(cheek, -xo, -W - 0.4))
        cuts = [sh.cyl_axis(1.1, -xo - 0.5, -W - 0.3, "x", yp, zp)]
        # arm frame: origin on the pivot so the joint is a plain rotation about x
        arm = sh.place(sh.S(body, *cuts), (0.0, -yp, -zp))
        # the arm hangs on the servo (parent); the servo's frame is rotated, so give its pose relative to it
        plan.part(id="lifter", kind="other", material="nylon", process="fdm", print_orientation="+y",
                  shape=arm, at=[0.0, yp, zp], rot=[0.0, 0.0, 0.0],
                  joint={"kind": "revolute", "axis": [1, 0, 0], "pivot": [x_face, yp, zp],
                         "min": 0, "max": RANGE_DEG, "default": 0},
                  actuated_by="servo", rotates_with="lifter", color="#c0392b",
                  label="printed lifting scoop: cheeks outside the side walls, lip on the floor, servo-driven")
        # pivot pin on the left: a 2 mm steel dowel pressed into the wall boss, the cheek turns on it
        plan.part(id="pivot_pin", kind="pin", material="steel", process="cots", stock="2 mm hardened dowel",
                  shape=sh.cyl_axis(1.0, -xo - 0.3, -W + 4.4, "x", yp, zp), rotates_with="fixed", color="#777777",
                  label="2 mm steel dowel: the scoop's left pivot")
        plan.connect("pivot_pin", "chassis_bottom", "press_fit", "Pressed into the left wall boss", interference_mm=0.03,
                     mechanical_key=True)
        plan.connect("lifter", "pivot_pin", "shaft", "Left cheek turns on the dowel, e-clip outboard")
        plan.connect("lifter", "servo", "shaft", "Hub keyed on the servo's 25T spline, M2 horn screw on the axis",
                     mechanical_key=True)
