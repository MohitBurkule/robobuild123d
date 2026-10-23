"""Every screwed joint once: the head-side holes the part builders cut and the spec `fasteners[]` records both come
from this table (robot.cad.holes), so a hole and its record cannot disagree. STEP frame; `records()` lifts to world.

The thread side is the chassis' own dump features (2.9 heat-set column bores, the side-boss nut pockets, the tab
holes), the motor's tapped base, the standoff's thread."""
from dataclasses import dataclass, field

from robot.cad.holes import hole_tool
from robot.cad import fastener_catalog as fc
from .params_chassis import (HX, IN_X, WALL, CH_H, AXLE_Y, AXLE_Z, POSTS, END_POSTS, BOSS_PITCH, HY, TAB_HOLE_DY, TAB_HOLE_Z,
                             TAB_X_OUT, TAB_W, TAB_PITCH, BOSS_IN)
from .params_drive import FLOOR_LIFT, WY, WZ, UP_IN, UP_T
from .params_hw import BASE_T, BACK_T, M2, M3
from .params_side import PLATE_X
from .params_vert import DECK_TOP, POST_CB_Z, MOTOR_HOLES, PRONG

import math

INSERT_LEN = 4.0
NUT_FACE_X = IN_X - BOSS_IN + fc.nut(M3, "thin")[1]   # head-side face of the boss nut (it sits on the pocket floor from inside)
CSK_SINK = 0.1                 # the dump's Chamfer5 seat (R3.1) is a hair under the DIN 7991 head (R3.0 + clearance): head sits 0.1 deep
SCREW_MATERIAL = "aluminium"   # 7075 screws throughout, as Revron (mass)
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

    def tool_and_record(self):
        """Head-side cutter and record (Revron convention: the head side is cut and recorded; the thread side is the
        host's own feature: a heat-set bore, nut pocket, tapped standoff or the motor's tapped base)."""
        return hole_tool(self.at, self.axis, self.fastener, head=self.head, into="through", grip=self.grip, side="head",
                         head_clear=self.head_clear, cbore=None if self.head == "csk" else 0.0, sink=self.sink)   # heads seat on the face, no counterbore


def joints():
    out = []
    for i, (x, y) in enumerate(list(POSTS) + list(END_POSTS)):   # base panel into the bottom column heat-sets
        out.append(Joint(f"bolt_b{i}", f"M{M2:g}x5", "button", (x, y, WALL - BASE_T), (0, 0, 1), "base_panel", BASE_T, "insert", f"insert_b{i}", ["base_panel"]))
    for i, (x, y) in enumerate(POSTS):                            # vert_mod frame into the top column heat-sets
        out.append(Joint(f"bolt_t{i}", f"M{M2:g}x6", "button", (x, y, POST_CB_Z), (0, 0, -1), "vert_mod", POST_CB_Z - DECK_TOP, "insert", f"insert_t{i}", ["vert_mod"]))
    for s, n in ((-1, "l"), (1, "r")):
        for k, y in enumerate((-BOSS_PITCH / 2, BOSS_PITCH / 2)):   # side pod plate into the captive boss nuts
            out.append(Joint(f"bolt_s{n}{k}", f"M{M3:g}x10", "csk", (s * PLATE_X[1], y, AXLE_Z), (-s, 0, 0), f"side_{n}", PLATE_X[1] - NUT_FACE_X, "nut",
                             f"nut_s{n}{k}", [f"side_{n}", "chassis"], "hex2"))
        out.append(Joint(f"bolt_a{n}", f"M{M3:g}x12", "cap", (s * (IN_X - BACK_T), -AXLE_Y, AXLE_Z), (s, 0, 0), None, BACK_T, "tapped",   # front axle stack
                         f"so_{n}", [f"bplate_{n}", "chassis", f"fplate_{n}"], "hex2.5"))
        x_in = TAB_X_OUT - TAB_PITCH - TAB_W                     # inner tab's inner face: the head seats on its lead-in (Chamfer5)
        out.append(Joint(f"bolt_x{n}", f"M{M3:g}x12", "button", (s * x_in, HY + TAB_HOLE_DY, TAB_HOLE_Z), (s, 0, 0), None,
                         PRONG[0] - x_in, "nut", f"nut_x{n}", ["chassis", "vert_mod", f"side_{n}"], "hex2",
                         {"reason": "rear cross bolt, driven from between the inner tabs: through the inner tab into the thin nut captive in the "
                                    "module prong, its shank on through the pod tongue as a shear pin (the tongue sits in the tab gap); the 4 M2 "
                                    "into the columns clamp the deck face"}, OPEN))
    for i, (dy, dz) in enumerate(MOTOR_HOLES):                   # BE1806 base through the left upright, heads in its counterbores
        out.append(Joint(f"bolt_m{i}", f"M{M2:g}x6", "cap", (-(UP_IN + UP_T), WY + dy, WZ + dz), (1, 0, 0),
                         "vert_mod", UP_T, "tapped", "weapon_motor_stator", ["vert_mod"]))
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
