"""Servo lifter: a printed U-shaped lifting scoop pivoting about a lateral axis near the front.

The servo lies against the right side wall with its output along +x, in a window through the wall so its output face
sits just outside it; the scoop's right cheek fits straight onto the spline (joint declared in the servo's frame). The
left cheek turns on an M2 pivot screw on the same axis, into an insert in the left wall. The scoop plate sits in front
of the chassis, its lip just off the floor; raising it turns the front edge up and away from the body.
"""

from __future__ import annotations

import math

from shapely.geometry import MultiPoint

from ..intent import I
from . import sh
from .plan import Pocket
from .pockets import GAP, HOUSING
from .weapon import module

SERVO = "servo_cs07"
SERVO_SIZE = (23.0, 12.0, 22.7)  # catalog body box (x, y, z); output along local z; ears 32 over, local x +-16, z 5.65..8.15
EAR_REACH = 16.0  # the mounting ears reach this far from the centre along local x (world y here)
EAR_X_BAND = (5.35, 8.45)  # the ear plates in world x (local z 5.65..8.15 + 0.3 clearance)
PIVOT_BACK = 14.0  # pivot behind the chassis front: rear ear (yp-16) clears the wheel sweep, and yp-13.3 (servo
                   # keepout) keeps the wire corridor to the rx open; the front ear passes through the front wall
                   # in its ear slot (tip 2 mm proud of the skin, between the wall and the scoop plate's back edge)
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
        xc = x_face - sz / 2
        # the ears reach further along y but only in their narrow x band (the signal approach at x = xc stays routable)
        plan.keepouts.append(("servo_ears", xc + EAR_X_BAND[0] - GAP, xc + EAR_X_BAND[1] + GAP,
                              yp - EAR_REACH - GAP - HOUSING, yp + EAR_REACH + GAP + HOUSING))
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
                  label="CS07 micro servo on its side, output through the right wall (BEC 5 V from the receiver lead)",
                  intent=I("load_path", "the servo drives the scoop directly on its spline: no linkage to wear or jam",
                           f"CS07: torque to lift at the {SCOOP_LEN:g} mm lip", threats=["under_front", "under_side", "reaction_gyro"]))
        pk = Pocket("servo", xc - sz / 2 - GAP, W - f.wall, yp - sx / 2 - GAP, yp + sx / 2 + GAP,
                    zp - sy / 2 - GAP, zp + sy / 2 + GAP, HOUSING,
                    intent=I("retention", "servo pocket: holds the servo against the scoop's reaction torque on all faces",
                             f"servo box + {GAP} mm", threats=["reaction_gyro", "wall_slam"]))
        sig_y = yp - sx / 2
        pk.notches.append((xc - 1.6, xc + 1.6, sig_y - 2.0, sig_y + 0.5, min(zp - 1.6, -1.0), max(zp + 1.6, 1.0)))
        for s in (-1.0, 1.0):  # ear slots: the mounting ears pass through the pocket walls (M2 screws thread them)
            ya, yb = sorted((yp + s * 10.0, yp + s * (EAR_REACH + 1.0)))
            pk.notches.append((xc + EAR_X_BAND[0], xc + EAR_X_BAND[1], ya, yb,
                               zp - sy / 2 - 0.5, zp + sy / 2 + 0.5))
        plan.pocket(pk)
        # window in the right wall for the servo: its output face sits just outside, in the cheek's plane, so nothing
        # of the scoop has to pass through the wall
        win = sh.boxr(W - f.wall - 0.5, W + 0.5, yp - sx / 2 - GAP, yp + sx / 2 + GAP, zp - sy / 2 - GAP, zp + sy / 2 + GAP)
        wi = I("load_path", "window in the right wall: the servo's output face sits in the cheek's plane, so the scoop "
               "never passes through the wall", f"servo cross-section + {GAP} mm", threats=["vspin_side", "reaction_gyro"])
        plan.cut("bottom", win, intent=wi)
        plan.cut("top", win, intent=wi)
        plan.add("bottom", sh.cyl_axis(3.0, -W, -W + 6.0, "x", yp, zp),
                 intent=I("load_path", "boss for the left pivot dowel: the scoop's load on that side goes into 6 mm of solid",
                          "r 3 round a 2 mm dowel", threats=["reaction_gyro", "under_front"]))
        plan.late_cut("bottom", sh.cyl_axis(1.0, -W - 0.2, -W + 4.6, "x", yp, zp),
                      intent=I("retention", "press bore for the dowel", "2 mm - 0.03 interference", threats=["reaction_gyro"]))
        # the scoop: two cheeks outside the side walls + the plate in front of the chassis
        xo = W + 0.4 + CHEEK_T
        # the plate's back edge clears the front wall over the whole lift (it swings up about the pivot)
        y_back = yp + (f.y1 + 0.8 - yp) / math.cos(math.radians(RANGE_DEG + 5.0))
        y_tip = f.y1 + SCOOP_LEN
        z_tip = floor + LIP_GAP
        top_back = (y_back, zp + 1.0)
        top_tip = (y_tip, z_tip + 1.0)
        # the 2 mm ledge at the top-back keeps every plate corner >= 90 deg: an acute corner there reads as a
        # zero-thickness sliver in the wall check (its inward ray leaves through the adjacent face)
        plate = [(y_back, top_back[1] - SCOOP_T - 2.0), top_back, (y_back + 2.0, top_back[1]), top_tip, (y_tip, z_tip)]
        # sweep relief in the top half's front lip: the plate's back edge swings up through it as the scoop lifts
        # (annulus sector of the plate's swept band about the pivot: the plate's material all sits r >= the back edge,
        # so the relief never reaches the pivot or cuts into the bay floor)
        r_in = math.hypot(y_back - yp, top_back[1] - zp) - 0.6
        r_out = max(math.hypot(yv - yp, zv - zp) for yv, zv in plate) + 1.0
        a0 = math.degrees(math.atan2(top_back[1] - zp, y_back - yp)) - 2.0
        a1 = a0 + RANGE_DEG + 4.0
        n = 14
        sec = [(yp + r_in * math.cos(math.radians(a0 + (a1 - a0) * i / n)),
                zp + r_in * math.sin(math.radians(a0 + (a1 - a0) * i / n))) for i in range(n + 1)]
        sec += [(yp + r_out * math.cos(math.radians(a1 - (a1 - a0) * i / n)),
                 zp + r_out * math.sin(math.radians(a1 - (a1 - a0) * i / n))) for i in range(n + 1)]
        plan.cut("top", sh.side_prism(sec, -xo, xo),
                 intent=I("load_path", "sweep relief: the scoop's plate swings up through this opening in the top "
                          "half's front lip as it lifts; the lip above the slot still carries wall loads",
                          f"annulus sector r {r_in:.1f}-{r_out:.1f} mm about the pivot, {a0:.0f}-{a1:.0f} deg",
                          threats=["reaction_gyro", "wall_slam"]))
        cheek = list(MultiPoint(_circle((yp, zp), 5.0) + [top_back, (y_back + 3.0, top_back[1]),
                                                          (y_back + 3.0, top_back[1] - SCOOP_T - 2.0),
                                                          (y_back, top_back[1] - SCOOP_T - 2.0)]).convex_hull.exterior.coords)[:-1]
        body = sh.U(sh.side_prism(plate, -xo, xo), sh.side_prism(cheek, W + 0.4, xo), sh.side_prism(cheek, -xo, -W - 0.4))
        cuts = [sh.cyl_axis(1.1, -xo - 0.5, -W - 0.3, "x", yp, zp)]
        # arm frame: origin on the pivot so the joint is a plain rotation about x
        arm = sh.place(sh.S(body, *cuts), (0.0, -yp, -zp))
        # the arm hangs on the servo (parent); the servo's frame is rotated, so give its pose relative to it
        plan.part(id="lifter", kind="other", material="nylon", process="fdm", print_orientation="+y",
                  shape=arm, parent="servo", at=[0.0, 0.0, -xc], rot=[-90.0, -90.0, 0.0],
                  # joint in the servo's frame: its local z is world +x, the output face is at local z = sz / 2
                  joint={"kind": "revolute", "axis": [0, 0, 1], "pivot": [0.0, 0.0, x_face - xc],
                         "min": 0, "max": RANGE_DEG, "default": 0},
                  actuated_by="servo", rotates_with="lifter", color="#c0392b",
                  label="printed lifting scoop: cheeks outside the side walls, lip on the floor, servo-driven",
                  intent=I("ground_game", "scoop gets under the opponent and lifts it off its wheels; cheeks outside the "
                           "walls so it turns clear of the body", f"lip {LIP_GAP} mm off the floor, lift {RANGE_DEG:g} deg", threats=["under_front", "under_side"]))
        # pivot pin on the left: a 2 mm steel dowel pressed into the wall boss, the cheek turns on it
        plan.part(id="pivot_pin", kind="pin", material="steel", process="cots", stock="2 mm hardened dowel",
                  shape=sh.cyl_axis(1.0, -xo - 0.3, -W + 4.4, "x", yp, zp), rotates_with="fixed", color="#777777",
                  label="2 mm steel dowel: the scoop's left pivot",
                  intent=I("load_path", "second pivot on the scoop axis: the scoop is carried both sides, the servo "
                           "spline only drives it", "2 mm hardened dowel", threats=["reaction_gyro", "under_front"]))
        plan.connect("pivot_pin", "chassis_bottom", "press_fit", "Pressed into the left wall boss", interference_mm=0.03,
                     mechanical_key=True)
        plan.connect("lifter", "pivot_pin", "shaft", "Left cheek turns on the dowel, e-clip outboard")
        plan.connect("lifter", "servo", "shaft", "Hub keyed on the servo's 25T spline, M2 horn screw on the axis",
                     mechanical_key=True)
