"""Spec generation for the Elevron 3.0 Alt (robots/elevron_alt/spec.json). Run `python3 build_elevron_alt.py`.

Placements: custom parts are model shapes already in robot-world coordinates; bought parts are placed from the same
params (relations to the chassis, axle and weapon axis). Fasteners come from fasteners.py (one table for the holes and
the records). Where the STEP is silent (battery, ESCs, switch, wiring) the layout is ours (REFERENCE.md)."""
import json
import os

from robot.cad import fastener_catalog as fc
from robocad.rig import DIGITS
from .fasteners import records, INSERT_LEN
from .params_chassis import (WIRE_SLOT_X, DECK_Z, REBATE, IN_X, CH_H, WALL, AXLE_Y, AXLE_Z, POSTS, END_POSTS, BOSS_PITCH, BOSS_IN, COL_R, HY, TAB_HOLE_DY, TAB_HOLE_Z,
                             TAB_X_OUT, TAB_W, TAB_PITCH, SW_SLOT, SW_SLOT_IN, SW_PITCH, POST_PITCH)
from .params_drive import FLOOR_LIFT, N10_X, DRIVE_MOTOR, WY, WZ, MOTOR_AT_X, HUB_X0, HUB_LEN, DISC_X
from .params_hw import INSERT_CAT, M3
from .params_vert import DECK_TOP, LEAD_SLOT, BULK_Y, PRONG
from .params_drive import LEAD_Y

HERE = os.path.dirname(os.path.abspath(__file__))
L = FLOOR_LIFT
SIDES = ((-1, "l"), (1, "r"))
PLA = dict(material="pla", process="fdm", solid_fraction=0.8)   # Revron SOLID tub/mount values
TPU = dict(material="tpu", process="fdm", solid_fraction=0.9)
STATOR, CAN = "be1806_stator", "be1806_can"
BATTERY, RXESC, WESC, SWITCH = "lipo_2s_180_turnabot", "malenki_nano_rvrn2", "bbb_ant_esc_rvrn2", "switch_bbb_ant_rvrn2"
SW_LEVER_TOP = 5.45                    # switch catalog: lever top above its origin (set flush with the deck top)
WIRE = {"power": (24, 8), "motor": (26, 8), "signal": (28, 8), "phase": (22, 10)}   # AWG and slack (mm) per wire kind
PRESS = {"bearing": 0.05, "pack": 0.1, "tyre": 0.5}   # press-fit interference (mm)
NUT_HALF = fc.nut(M3, "thin")[1] / 2   # thin M3 nut: its centre sits half a thickness into its seat
INSERT_MELT = 0.35                     # heat-set OD over the 2.9 dump bore (radial)
SHAFT_RACE = 0.3                       # shaft-in-race overlap of the one-solid bearing
# electronics bay (STEP has none): battery left of centre and Malenki right of centre on the base panel between the
# column rows, the weapon ESC on the Malenki; the switch pressed into the deck slot
BAT_SIZE, RX_SIZE, WE_SIZE = (36.0, 18.0, 11.0), (32.0, 20.0, 4.4), (23.5, 12.0, 5.0)
BAY_GAP = 0.5
LEADS_FORWARD = [-90, 0, 0]             # BE1806 turned about its axis so the phase leads point forward into the upright's lead slot
SHAFT_MASS_SHARE = 0.05                # the shaft's mass is in the motor's catalog mass (Revron convention)
LEAD_RISE = 2.0                        # phase-lead waypoints: this far off the deck faces / the lead tip
MOTOR_LIFT = 0.6                       # N10 play up to the deck underside (STEP 0.5)
MOTOR_SLIDE = 2.0                      # N10 inboard play in the keyhole before the hub meets the wall


def _w(x, y, z):
    """STEP frame -> robot world, rounded to the micron."""
    return [round(x, DIGITS), round(y, DIGITS), round(z + L, DIGITS)]


def _structure(P, M):
    P(id="chassis", kind="structure", print_orientation="-z", rotates_with="fixed", color="#2a2c30", shape=M("chassis"), **PLA,
      thin_wall_deviation="matches ELVRN3.0 Alt chassis: Chamfer1 meets the Cut-Extrude15 boss window top at the pad face (z 12), as in the dump",
      sharp_corners_ok="ELVRN3.0 Alt chassis: the dump rounds only the listed edges (Fillet1..15, Chamfer1..5); the remaining concave edges are sharp in the original too",
      label="ELVRN3.0 Alt chassis: open-bottom block, 2 mm walls and deck, X-lattice deck pockets, N10 / standoff keyholes, side bosses with captive M3 nuts, rear cross-bolt tabs")
    P(id="base_panel", kind="structure", print_orientation="+z", rotates_with="fixed", color="#2a2c30", shape=M("base_panel"), **PLA,
      label="1 mm printed base panel in the chassis rebate, 6 M2 button heads into the column heat-sets")
    P(id="vert_mod", kind="structure", print_orientation="+x", rotates_with="fixed", color="#30343a", shape=M("vert_mod"), **PLA,
      thin_wall_deviation="RVRN_revdev vert_mod as drawn: the four BE1806 screw counterbores break into the axis bore on the motor side",
      sharp_corners_ok="vert_mod from the RVRN_revdev STEP solid's faces (ELVRN, no dump): the shell, bulkhead and uprights meet square as in the STEP solid",
      label="vert_mod weapon module: hollow ramp shell on the deck (4 M2 into the column heat-sets), bulkhead, uprights carrying the BE1806 and the MF85, motor shroud, prongs on the cross bolts")
    for s, n in SIDES:
        P(id=f"side_{n}", kind="armor", print_orientation="+z", rotates_with="fixed", color="#3c4048", shape=M(f"side_{n}"), **TPU,
          thin_wall_deviation="RVRN Side_Panel_alt_sm as drawn: the front boss screw's head bore runs 0.7 mm over the raked underside",
          deviation="ELVRN3.0 Alt STEP: the Side_Panel_alt_sm fork prongs lead the disc (tips at y 98.6, ahead of the disc's swept front): the forks are the ground game in front of the vertical disc, kept for parity",
          label="Side_Panel_alt_sm TPU pod: plate on the side boss (2 M3 CSK into captive nuts), drafted guard round both wheels, tongue on the rear cross bolt, crossbar round the outer tab, fork prong past the weapon")


def _weapon(P, M, pivot):
    """Rotor frame: on the spin axis in the disc mid-plane (the spin checks take the weapon part's origin as the centre)."""
    P(id="weapon_motor_stator", kind="weapon_motor", catalog=STATOR, at=_w(MOTOR_AT_X, WY, WZ), rot=LEADS_FORWARD, rotates_with="fixed",
      exposed=True, exposed_reason="vertical spinner: the BE1806 sits between the uprights behind the disc, shielded by the disc and the uprights",
      label="BBB BE1806 2300 kV (RV08), fixed half: base flat on the left upright, 4 x M2 from outside")
    joint = {"kind": "revolute", "axis": [1, 0, 0], "pivot": pivot, "min": 0, "max": 360, "default": 0}   # pivot in the disc plane, on the shaft
    P(id="wshaft", kind="shaft", material="steel", process="turned", stock="BE1806 5 mm shaft (part of the motor), run on into the MF85", rotates_with="weapon",
      shaft_of="weapon_motor_can", shape=M("wshaft", pivot), parent="disc", at=[0, 0, 0], color="#777777", solid_fraction=SHAFT_MASS_SHARE,
      label="5 mm shaft from the bell face through disc, spider and prop mount into the MF85 in the right upright")
    P(id="weapon_motor_can", kind="other", role="rotor", catalog=CAN, parent="disc", at=[MOTOR_AT_X - pivot[0], 0, 0], rot=LEADS_FORWARD, rotates_with="weapon", exposed=True,
      exposed_reason="vertical spinner: the BE1806 can spins between the uprights behind the disc",
      label="BBB BE1806 can: spins with the shaft round the fixed stator")
    P(id="prop_mount", kind="other", role="hub", material="aluminium", process="turned", stock="RV07 prop mount (aluminium, part of the motor kit)", rotates_with="weapon", parent="disc",
      shape=M("prop_mount", pivot), at=[0, 0, 0], color="#9aa0a6", retained="press_fit", label="RV07 prop mount: flange clamping the spider and disc onto the bell")
    P(id="spider", kind="other", role="hub", material="aluminium", process="waterjet", stock="3 mm 7075 plate", parent="disc", rotates_with="weapon",
      min_web_mm=0.8, min_web_reason="0.8 mm webs are the designer's own (RVRN spider_1, the uploaded spider.STEP, measures 0.8 at the same four places)",
      shape=M("spider", pivot), at=[0, 0, 0], color="#b8bcc2", label="spiderSL: 3 mm aluminium spider driving the disc (Revron spider geometry)")
    P(id="disc", kind="weapon", material="hardox", process="laser", stock="3 mm Hardox 450", secondary_ops=["drilled"], rotates_with="weapon", joint=joint,
      thin_wall_deviation="RVRN Drisk_floating_3 as drawn: the dog ramps run out to a knife edge (the Revron disc, identical part)",
      min_web_mm=0.9, min_web_reason="0.9 mm webs beside the balance window are the designer's own (RVRN Drisk_floating_3, identical part)",
      shape=M("disc", pivot), at=pivot, color="#d9dde2",
      weapon={"kind": "disc", "motor": "weapon_motor_stator", "cells": 2, "reduction": 1.0, "spin_axis": [1, 0, 0], "spin_dir": "ccw", "supported_both_ends": True, "teeth": 1},
      label="Drisk_floating_3: 3 mm Hardox single-tooth eccentric disc (the Revron disc)")
    P(id="wbearing", kind="bearing", material="steel", process="cots", stock="FS4 MF85ZZ 5 x 8 x 2.5 flanged", rotates_with="fixed", color="#555555",
      shape=M("bearing"), label="FS4 MF85ZZ in the right upright: outboard support of the shaft")


def _drive(P, M):
    for s, n in SIDES:
        P(id=f"motor_{n}", kind="motor", catalog=DRIVE_MOTOR, at=_w(s * N10_X, AXLE_Y, AXLE_Z), rot=[0, 0, 0 if s > 0 else 180], rotates_with="fixed",
          loose_ok={"axis": "+x" if s < 0 else "-x", "max_mm": MOTOR_SLIDE, "reason": "RVRN_revdev STEP: RV12 N10 slides inboard in the ELVRN Alt keyhole until its hub meets the wall, as in the RVRN 2.0 tub"},
          label="RV12 N10 2200 rpm in the rear keyhole, gearbox face on the wall")
        for e, y in (("r", AXLE_Y), ("f", -AXLE_Y)):
            hub = f"whub_{e}{n}"
            piv = _w(s * (HUB_X0 + HUB_LEN / 2), y, AXLE_Z)
            extra = {} if e == "r" else {"driven": False}
            lift = {"loose_ok": {"axis": "+z", "max_mm": MOTOR_LIFT, "reason": "RVRN_revdev STEP: RV12 N10 (z 2.5..14.5) under the ELVRN Alt deck underside at 15: the drive group lifts 0.5 mm, as drawn"}} if e == "r" else {}
            P(id=hub, kind="pulley", print_orientation="+x", **lift, rotates_with=f"wheel_{e}{n}", color="#333333", shape=M(hub), parent="chassis", **PLA,
              joint={"kind": "revolute", "axis": [1, 0, 0], "pivot": piv, "min": 0, "max": 360, "default": 0}, **extra,
              thin_wall_deviation="RVRN RV21 hub as drawn: 0.5 mm O-ring flange and lip (the Revron part, kept for parity)",
              sharp_corners_ok="RVRN RV21 hub as drawn (the Revron part): the D-bore flat meets the bore sharp",
              visual_ok={"ligament": "RVRN RV21 hub as drawn: the M3 grub bore breaks into the D-bore and the seat ramps (STEP Cut-Extrude4)"},
              label="RV21 printed hub (Revron)" + (" on the N10 D-shaft" if e == "r" else ", bore opened to idle on the 10 mm standoff"))
            P(id=f"wheel_{e}{n}", kind="wheel", material="rubber", process="cots", tyre_of=hub, rotates_with=f"wheel_{e}{n}", parent=hub, shape=M(f"wheel_{e}{n}"), **extra,
              color="#1b1b1b", stock="RV22 Scalextric F1 front tyre 21.5 x 14 x 9.5", label="Scalextric F1 tyre 21.5 x 9.5")
        P(id=f"so_{n}", kind="pin", role="standoff", material="aluminium", process="cots", stock="M3 x 10 aluminium standoff, 5 OD", rotates_with="fixed", color="#b8bcc2",
          shape=M(f"so_{n}"), label="10 mm alu standoff: front idler axle, clamped across the keyhole")
        for nm, lab in (("bplate", "BACKING_PLATE: inside the wall behind the front keyhole, spreads the axle screw load"), ("fplate", "FRONT_PLATE: outside the wall, the standoff seats on it")):
            P(id=f"{nm}_{n}", kind="other", role="spacer", print_orientation="+x", rotates_with="fixed", color="#2a2c30", shape=M(f"{nm}_{n}"), **PLA, label=lab)


def _hardware(P):
    for s, n in SIDES:
        for k, y in enumerate((-BOSS_PITCH / 2, BOSS_PITCH / 2)):   # captive in the boss's hex pockets, from the inside
            P(id=f"nut_s{n}{k}", kind="nut", catalog="nut_m3_thin", at=_w(s * (IN_X - BOSS_IN + NUT_HALF), y, AXLE_Z), rot=[0, 90, 0], rotates_with="fixed")
        P(id=f"nut_x{n}", kind="nut", catalog="nut_m3_thin", at=_w(s * (PRONG[0] + NUT_HALF), HY + TAB_HOLE_DY, TAB_HOLE_Z), rot=[0, 90, 0], rotates_with="fixed")   # captive in the module prong
    for i, (x, y) in enumerate(list(POSTS) + list(END_POSTS)):
        P(id=f"insert_b{i}", kind="insert", catalog=INSERT_CAT, at=_w(x, y, WALL + INSERT_LEN / 2), rot=[0, 0, 0], rotates_with="fixed")
    for i, (x, y) in enumerate(POSTS):
        P(id=f"insert_t{i}", kind="insert", catalog=INSERT_CAT, at=_w(x, y, CH_H - INSERT_LEN / 2), rot=[0, 0, 0], rotates_with="fixed")


def _electronics(P):
    P(id="battery", kind="battery", catalog=BATTERY, at=_w(-(COL_R + BAT_SIZE[1] / 2), 0, WALL + BAT_SIZE[2] / 2), rot=[0, 0, 90], retained="press_fit",
      label="2S 180 mAh between the column rows, left of centre, on the base panel")
    rx_x = POSTS[-1][0] - COL_R - BAY_GAP - RX_SIZE[1] / 2
    P(id="rxesc", kind="esc", catalog=RXESC, at=_w(rx_x, 0, WALL + RX_SIZE[2] / 2), rot=[0, 0, 90], retained="kapton",
      label="Malenki nano right of centre on the base panel")
    P(id="wesc", kind="esc", catalog=WESC, at=_w(rx_x, 0, WALL + RX_SIZE[2] + WE_SIZE[2] / 2), rot=[0, 0, 90], retained="kapton",
      label="BBB weapon ESC on the Malenki")
    P(id="power_switch", kind="switch", catalog=SWITCH, at=_w(IN_X - SW_SLOT_IN - SW_SLOT[0] / 2, 0, CH_H - SW_LEVER_TOP), rot=[0, 0, 90], retained="press_fit",
      marked=True, tool_free=True, off_dir=[0, -1, 0], label="BBB ant switch pressed up into the deck slot from inside, lever flush with the deck")


def _connections(C):
    for s, n in SIDES:
        C(f"motor_{n}", "chassis", "interlock", "N10 gearbox boss sits in the side-wall keyhole, its face bears on the wall inner face; the base panel closes the slot under it")
        C(f"whub_r{n}", f"motor_{n}", "shaft", "RV21 D-bore on the N10 D-shaft, M2 grub on the flat carries the drive torque")
        C(f"whub_f{n}", f"so_{n}", "shaft", "front hub runs on the 10 mm standoff as a plain bearing, held on by the screw head end")
        for e in "rf":
            C(f"wheel_{e}{n}", f"whub_{e}{n}", "press_fit", "F1 tyre stretched over the crowned hub seat, the centre groove keys it", interference_mm=PRESS["tyre"])
    C("wbearing", "vert_mod", "press_fit", "MF85ZZ pressed into the 8 mm seat of the right upright, flange against the inner face", interference_mm=PRESS["bearing"])
    C("wshaft", "wbearing", "shaft", "5 mm shaft runs in the MF85 inner race: the outboard support of the weapon")
    C("weapon_motor_can", "wshaft", "press_fit", "the can is the shaft's own rotor: the shaft is pressed into its cap", interference_mm=PRESS["bearing"])
    C("prop_mount", "wshaft", "press_fit", "prop-mount bore on the shaft, clamping the stack against the bell", interference_mm=PRESS["bearing"])
    C("spider", "wshaft", "press_fit", "spider bore pressed on the shaft and clamped between the prop-mount flange and the disc", interference_mm=PRESS["bearing"])
    C("disc", "spider", "pin", "floating disc dogs engage the spider's dog pockets (drive pins), the stack clamped by the prop mount")
    C("wshaft", "disc", "press_fit", "shaft through the disc bore, the stack clamped against the bell face", interference_mm=PRESS["bearing"])
    C("battery", "base_panel", "press_fit", "pack wedged between the column rows on the base panel, deck above it", interference_mm=PRESS["pack"])
    C("rxesc", "base_panel", "tape", "Malenki taped to the base panel with kapton between the column rows; it only carries its own weight")
    C("wesc", "rxesc", "tape", "weapon ESC kapton-wrapped onto the Malenki; it only carries its own weight")
    C("power_switch", "chassis", "press_fit", "switch body pressed up into the 4 x 12 deck slot, the lever flush with the deck", interference_mm=PRESS["bearing"])


def _wires(wires):
    def W(i, a, b, kind, size=None, via=None, **k):
        awg, sl = WIRE[size or kind]
        wires.append({"id": i, "from": a, "to": b, "awg": awg, "kind": kind, "slack_mm": sl, **({"via": via} if via else {}), **k})
    W("w_bat_sw", "battery.jst_rcy", "power_switch.in", "power")
    W("w_sw_rx", "power_switch.out", "rxesc.bat", "power")
    W("w_sw_wesc", "power_switch.out", "wesc.bat", "power")
    W("w_m_l", "rxesc.m2", "motor_l.terminals", "motor")
    W("w_m_r", "rxesc.m1", "motor_r.terminals", "motor")
    W("w_rx_wesc", "rxesc.wpn", "wesc.rx", "signal")
    sx, _, (sz0, sz1) = LEAD_SLOT                          # lead slot along the left upright's inner face
    W("w_wesc_m", "wesc.motor", "weapon_motor_stator.phases", "motor", "phase",
      via=[_w(WIRE_SLOT_X, 0, DECK_Z - LEAD_RISE), _w(WIRE_SLOT_X, 0, DECK_TOP + LEAD_RISE), _w(sx, BULK_Y[0] - LEAD_RISE, DECK_TOP + LEAD_RISE),
           _w(sx, BULK_Y[0], (sz0 + sz1) / 2), _w(sx, LEAD_Y - LEAD_RISE, WZ)],   # up the deck wire slot, back under the shell, along the lead slot to the stub
      exposed_reason="leaves the chassis hull only inside the vert_mod: under its closed shell (deck below, shell and walls round), then in the upright's lead slot")


# parts the RVRN_revdev STEP draws (by its solid stems) and the ones it leaves out (with why they are in the build)
REF_PART = {"motor_": "RV12_N10_2200_RPM*", "wheel_": "RV22_Scalextric_F1_Front_tyre*", "weapon_motor_": "RV08_1806_Brushless*",
            "prop_mount": "RV07_Prop_mount*", "wbearing": "FS4_MF85ZZ*", "so_": "10mm_standoff_3m_alu*", "bplate_": "BACKING_PLATE*",
            "fplate_": "FRONT_PLATE*", "spider": "spiderSL*"}
NOT_IN_STEP = {
    "whub_f": "not in the STEP: it draws the two RV21 hubs on the N10s only; the front idlers carry the same RV21 hub, its bore opened for the standoff",
    "base_panel": "not in the STEP (open-bottom chassis): a 1 mm printed panel in the Cut-Extrude2 rebate closes the electronics bay",
    "battery": "not in the STEP (no electronics drawn): Turnabot 2S 180 between the column rows",
    "rxesc": "not in the STEP (no electronics drawn): Malenki nano receiver / drive ESC",
    "wesc": "not in the STEP (no electronics drawn): BBB ant weapon ESC on the Malenki",
    "power_switch": "not in the STEP (no electronics drawn): BBB ant switch in the dump's 4 x 12 deck slot (Cut-Extrude6)",
    "wshaft": "not in the STEP as its own solid: the BE1806's 5 mm shaft, run on through the stack into the MF85",
    "insert_": "not in the STEP (no hardware drawn): M2 heat-sets in the ELVRN column bores",
    "nut_": "not in the STEP (no hardware drawn): thin M3 nuts, captive in the side bosses' hex pockets and the module prongs",
}
FASTENER_DEV = "not in the STEP (the RVRN_revdev assembly draws no fasteners): every hole it does draw carries one (fasteners.py)"


def _map_to_reference(parts):
    for p in parts:
        for k, g in REF_PART.items():
            if p["id"].startswith(k):
                p.setdefault("ref_part", g)
        for k, why in NOT_IN_STEP.items():
            if p["id"].startswith(k) and "ref_part" not in p:
                p.setdefault("deviation", why)


def make_spec(model_file):
    def M(name, origin=None):
        return {"type": "model", "file": model_file, "params": {"part": name, **({"origin": list(origin)} if origin else {})}}

    parts, conn, wires = [], [], []
    P = lambda **k: parts.append(k)
    C = lambda a, b, m, r, **k: conn.append(dict(a=a, b=b, method=m, reason=r, **k))
    _structure(P, M)
    _weapon(P, M, _w(sum(DISC_X) / 2, WY, WZ))
    _drive(P, M)
    _hardware(P)
    _electronics(P)
    _connections(C)
    _wires(wires)
    _map_to_reference(parts)
    n_ins = (len(POSTS) + len(END_POSTS), len(POSTS))
    overlap = [dict(a=f"insert_{k}{i}", b="chassis", max_depth_mm=INSERT_MELT, reason="M2 heat-set insert (3.5 OD) melted into the ELVRN 2.9 column bore: interference by design")
               for k, cnt in zip("bt", n_ins) for i in range(cnt)]
    overlap.append(dict(a="wshaft", b="weapon_motor_can", max_depth_mm=SHAFT_RACE, reason="shaft in the can's 5.1 bore (0.05 radial running fit; the meshes overlap)"))
    overlap.append(dict(a="wshaft", b="wbearing", max_depth_mm=SHAFT_RACE, reason="shaft in the MF85 inner race (bearing modelled as one solid)"))
    fasteners = records()
    for f in fasteners:
        f.setdefault("deviation", FASTENER_DEV)
    return dict(parts=parts, fasteners=fasteners, connections=conn, wires=wires, allow_overlap=overlap, reference_cad=reference_cad())


REF_DIR = "../../research/elevron_alt"   # RVRN_revdev STEP solids as STL (local only, never committed: .gitignore research/)
REF_TO_WORLD = [[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, FLOOR_LIFT], [0, 0, 0, 1]]
TOL = dict(tight=0.3, std=0.6, loose=1.5)


GRUB_DEV = (35.1, 0.57, 2.0)             # RV21 grub-bore break-in: |x|, z above the axle, capsule radius
TAB_DEV_R = 3.5                        # the Chamfer5 lead-in at the inner tab face
SLOT_DEV_R = 4.0                       # switch slot / window web
REBATE_DEV_R = 5.0                     # the base-panel rebate lip (the ligament check reads the rebate as a 68.5 bore)
VOL_TOL = dict(chassis=0.05, vert=0.2, side=0.4)


def reference_cad():
    gx, gz, gr = GRUB_DEV
    hub = lambda s, y, why: {"near": _w(s * gx, y, AXLE_Z + gz), "r": gr, "reason": why}
    hub_why = "RVRN RV21 hub as drawn: the M3 grub bore breaks into the D-bore (STEP Cut-Extrude4)"
    tab_dev = [{"near": _w(s * (TAB_X_OUT - TAB_PITCH - TAB_W), HY + TAB_HOLE_DY, TAB_HOLE_Z), "r": TAB_DEV_R,
                "reason": "ELVRN3.0 Alt chassis Chamfer5: the 1.5 mm lead-in on the inner tab's cross-bolt hole comes within 0.34 of the tab bottom in the STEP too"} for s in (-1, 1)]
    reb_dev = [{"near": _w(0, 0, REBATE), "r": REBATE_DEV_R, "reason": "ELVRN3.0 Alt chassis Cut-Extrude2: the 1 mm base-panel rebate lip under the 2 mm wall, as in the STEP"}]
    sx0 = IN_X - SW_SLOT_IN                                 # the switch slot's outer edge and the lattice window beside it
    deck_dev = [{"near": _w(x, y, DECK_Z), "r": SLOT_DEV_R, "reason": f"ELVRN3.0 Alt chassis Cut-Extrude6 / Sketch20: {what} sits 0.1 mm off the "
                 "deck lattice window (STEP: window edge x 21.9, slot x 22.0)"}
                for x, y, what in ((sx0 - SW_SLOT[0] / 2, 0, "the switch slot's inner edge"), (sx0 - SW_SLOT[0] / 2, -SW_PITCH / 2, "the front switch pilot"),
                                   (sx0 - SW_SLOT[0] / 2, SW_PITCH / 2, "the rear switch pilot"), (POST_PITCH[0] / 2 - COL_R - SLOT_DEV_R, 0, "the window beside the slot"))]
    rows = [dict(part="chassis", file="Alt_chassis_1.stl", mode="shape", tol_mm=TOL["loose"], tol_vol_frac=VOL_TOL["chassis"], note="Alt_chassis (dump replay by relations)", deviations=tab_dev + reb_dev + deck_dev),
            dict(part="vert_mod", file="vert_mod_1.stl", mode="envelope", tol_mm=TOL["loose"], tol_vol_frac=VOL_TOL["vert"], note="vert_mod: no dump; relation build from STEP sections (see MISSES.md)"),
            dict(part="side_r", file="Side_Panel_alt_sm_1.stl", mode="envelope", tol_mm=TOL["loose"], tol_vol_frac=VOL_TOL["side"], note="Side_Panel_alt_sm: no dump (see MISSES.md)"),
            dict(part="side_l", file="MirrorSide_Panel_alt_sm_1.stl", mode="envelope", tol_mm=TOL["loose"], tol_vol_frac=VOL_TOL["side"], note="MirrorSide_Panel_alt_sm"),
            dict(part="disc", file="Drisk_floating_3_1.stl", mode="envelope", tol_mm=TOL["std"], note="the Revron disc")]
    for s, n, f in ((-1, "l", "RV21_Rear_Wheel_1.stl"), (1, "r", "RV21_Rear_Wheel_2.stl")):
        rows.append(dict(part=f"whub_r{n}", file=f, mode="envelope", tol_mm=TOL["loose"], deviations=[hub(s, AXLE_Y, hub_why)]))
    return {"dir": REF_DIR, "ref_to_world": REF_TO_WORLD, "iou_min": 0.9, "placement_tol_mm": TOL["loose"], "parts": rows}


CLAIMS = [{"id": "c_mass", "text": "150 g or less", "metric": "mass_total_g", "op": "<=", "value": 150}]
ELECTRONICS = {"failsafe": True, "weapon_remote_disable": True, "radio": "2.4 GHz", "cells": 2}
WEAPON_LOCK = {"type": "external_pin", "note": "pit safety pin through the disc and an upright, pulled before a fight (Revron convention); not part of the build"}


def main():
    root = os.path.abspath(os.path.join(HERE, "..", ".."))
    spec = dict(name="Elevron 3.0 Alt", profile="aws2025", robot_type="vertical_spinner", locomotion="roller", archetype="vertical_spinner_forks",
                electronics=ELECTRONICS, weapon_lock=WEAPON_LOCK, can_run_inverted=False, claims=CLAIMS, **make_spec("src/build_elevron_alt.py"))
    out = os.path.join(root, "spec.json")
    json.dump(spec, open(out, "w"), indent=1)
    print("wrote", out, len(spec["parts"]), "parts", len(spec["fasteners"]), "fasteners")
