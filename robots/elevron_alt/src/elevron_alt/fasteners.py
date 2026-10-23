"""Every screwed joint once: the head-side holes the part builders cut and the spec `fasteners[]` records both come
from this table (robot.cad.holes), so a hole and its record cannot disagree. STEP frame; `records()` lifts to world.

The thread side is the chassis' own dump features (2.9 heat-set column bores, the side-boss nut pockets, the tab
holes), the motor's tapped base, the standoff's thread."""
from dataclasses import dataclass, field

from robot.cad.holes import hole_tool
from robot.cad import fastener_catalog as fc
from .params_chassis import (HX, IN_X, WALL, CH_H, AXLE_Y, AXLE_Z, POSTS, END_POSTS, BOSS_PITCH, HY, TAB_HOLE_DY, TAB_HOLE_Z,
                             TAB_X_OUT, TAB_W, TAB_PITCH, BOSS_IN, HOLE_D, TAB_LEAD)
from .params_drive import FLOOR_LIFT, WY, WZ, UP_IN, UP_T
from .params_hw import BASE_T, BACK_T, M2, M3
from .params_side import PLATE_X, PLATE_CSK_SINK, TONGUE_X
from .params_vert import DECK_TOP, POST_CB_Z, MOTOR_HOLES, PRONG

import math

from .variants import variant

INSERT_LEN = 4.0
NUT_FACE_X = IN_X - BOSS_IN + fc.nut(M3, "thin")[1]   # head-side face of the boss nut (it sits on the pocket floor from inside)
_DK, _K = fc.CSK[M3]
_RIM = _K - (_DK - M3) / 2      # the catalog head's cylindrical rim above its 90 deg cone
CSK_SINK = (HOLE_D / 2 + TAB_LEAD - _DK / 2) - _RIM   # head seated on the Chamfer5 cone (R3.1 at the face): its rim stands proud
SCREW_MATERIAL = "aluminium"   # 7075 screws throughout, as Revron (mass)
PROBE_RING = 0.8       # fastener_seat probes the face on a ring this far outside the head
OPEN = 1e3   # head clearance that opens the head recess right through the part (a driver path)


@dataclass
class Joint:
    id: str
    fastener: str
    head: str
    at: tuple            # head bearing point, STEP frame
    axis: tuple          # head -> tip
    head_part: str       # part that gets the head-side hole cut (None: hole already drawn)
    grip: float
    into: str            # insert | nut | tapped | through
    threads_into: str
    through: list
    tool: str = "hex1.5"
    extra: dict = field(default_factory=dict)
    head_clear: float = 10.0
    sink: float = 0.0
    cbore: float = 0.0   # counterbore depth from the host's face to the head seat
    fit: str = "close"   # clearance class of the head-side hole (the STEP draws M3 3.2, M2 2.2 throughout)

    def tool_and_record(self):
        """Head-side cutter and record (Revron convention: the head side is cut and recorded; the thread side is the
        host's own feature: a heat-set bore, nut pocket, tapped standoff or the motor's tapped base)."""
        return hole_tool(self.at, self.axis, self.fastener, head=self.head, into="through", grip=self.grip, side="head",
                         head_clear=self.head_clear, cbore=None if self.head == "csk" else self.cbore, sink=self.sink,
                         fit=self.fit)


def _seen_face(y, z, n=12):
    """|x| of the left upright's outer face as seen round a motor-screw head (the ring the seat probe walks: head radius
    plus PROBE_RING): the taper face, less the ring points that fall in the axis bore or the screw counterbores."""
    from .vm_geom import taper_x
    from .params_vert import AXIS_HOLE_R, MOTOR_HOLES, MOTOR_CB_R
    r = fc.head(M2, "cap")[0] / 2 + PROBE_RING
    pts = [(y + r * math.cos(2 * math.pi * i / n), z + r * math.sin(2 * math.pi * i / n)) for i in range(n)]
    holes = [((WY, WZ), AXIS_HOLE_R)] + [((WY + a, WZ + b), MOTOR_CB_R) for a, b in MOTOR_HOLES]
    xs = sorted(taper_x(py) for py, pz in pts if all(math.hypot(py - c[0], pz - c[1]) > hr for c, hr in holes))
    return xs[len(xs) - n // 2] if len(xs) >= n // 2 else taper_x(y)   # half the ring in material


def joints():
    out = []
    for i, (x, y) in enumerate(list(POSTS) + list(END_POSTS)):   # base panel into the bottom column heat-sets
        out.append(Joint(f"bolt_b{i}", f"M{M2:g}x5", "button", (x, y, WALL - BASE_T), (0, 0, 1), "base_panel", BASE_T, "insert", f"insert_b{i}", ["base_panel"]))
    for i, (x, y) in enumerate(POSTS):                            # vert_mod frame into the top column heat-sets
        out.append(Joint(f"bolt_t{i}", f"M{M2:g}x6", "button", (x, y, POST_CB_Z), (0, 0, -1), "vert_mod", POST_CB_Z - DECK_TOP, "insert", f"insert_t{i}", ["vert_mod"]))
    for s, n in ((-1, "l"), (1, "r")):
        for k, y in enumerate((-BOSS_PITCH / 2, BOSS_PITCH / 2)):   # side pod plate into the captive boss nuts
            face = PLATE_X[1] + PLATE_CSK_SINK                    # the head sits PLATE_CSK_SINK down its bore through the plate flank
            out.append(Joint(f"bolt_s{n}{k}", f"M{M3:g}x10", "csk", (s * face, y, AXLE_Z), (-s, 0, 0), f"side_{n}", face - NUT_FACE_X, "nut",
                             f"nut_s{n}{k}", [f"side_{n}", "chassis"], "hex2", sink=PLATE_CSK_SINK))
        out.append(Joint(f"bolt_a{n}", f"M{M3:g}x12", "cap", (s * (IN_X - BACK_T), -AXLE_Y, AXLE_Z), (s, 0, 0), None, BACK_T, "tapped",   # front axle stack
                         f"so_{n}", [f"bplate_{n}", "chassis", f"fplate_{n}"], "hex2.5"))
        x_in = TAB_X_OUT - TAB_PITCH - TAB_W                     # inner tab's inner face: its lead-in (Chamfer5) is the countersink
        if variant("step_cross_bolt"):
            out.append(Joint(f"bolt_x{n}", f"M{M3:g}x12", "csk", (s * x_in, HY + TAB_HOLE_DY, TAB_HOLE_Z), (s, 0, 0), None,
                             TONGUE_X[0] - x_in, "tapped", f"side_{n}", ["chassis", "vert_mod", f"side_{n}"], "hex2",
                             {"reason": "rear cross bolt as in the RVRN_revdev STEP, driven from between the inner tabs: clear through the inner tab and "
                                        "the module prong, threaded into the TPU pod tongue (2.6 pilot); the 4 M2 into the columns clamp the deck face"}, OPEN, sink=CSK_SINK))
        else:
            out.append(Joint(f"bolt_x{n}", f"M{M3:g}x10", "csk", (s * x_in, HY + TAB_HOLE_DY, TAB_HOLE_Z), (s, 0, 0), None,
                             PRONG[0] - x_in, "nut", f"nut_x{n}", ["chassis", "vert_mod", f"side_{n}"], "hex2",
                             {"reason": "rear cross bolt, driven from between the inner tabs: through the inner tab into the thin nut captive in the "
                                        "module prong, its shank on through the pod tongue as a shear pin (the tongue sits in the tab gap); the 4 M2 "
                                        "into the columns clamp the deck face"}, OPEN, sink=CSK_SINK))
    for i, (dy, dz) in enumerate(MOTOR_HOLES):                   # BE1806 base through the left upright, heads in its counterbores
        from .vm_geom import taper_x
        face = _seen_face(WY + dy, WZ + dz)                     # the upright's outer face round the head; the heads sit UP_T off the motor
        out.append(Joint(f"bolt_m{i}", f"M{M2:g}x6", "cap", (-face, WY + dy, WZ + dz), (1, 0, 0),
                         "vert_mod", face - UP_IN, "tapped", "weapon_motor_stator", ["vert_mod"], cbore=face - (UP_IN + UP_T)))
    return out


def cutters(part, only=None):
    """Union of the head-side hole tools this part carries (optionally only the joints whose id starts with `only`)."""
    t = [j.tool_and_record()[0] for j in joints() if j.head_part == part and (only is None or j.id.startswith(only))]
    out = t[0] if t else None
    for x in t[1:]:
        out = out + x
    return out


def records():
    M = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, FLOOR_LIFT], [0, 0, 0, 1]]
    out = []
    for j in joints():
        rec = j.tool_and_record()[1]
        out.append(rec.to_spec(j.id, through=j.through, threads_into=j.threads_into, tool=j.tool, M=M, removable=True, material=SCREW_MATERIAL, **j.extra))
    return out
