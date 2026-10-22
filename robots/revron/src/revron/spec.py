"""[fix-S] Spec generation: make_spec, intent_checks, reference_cad, main."""
import json, math, os, sys
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403
from . import panel_base, panel_top
from .tub2_params import OVER   # the squared rear corner overshoots the wall by the tub2 over-cut


def _mid(span):
    """Midpoint of an interval, rounded to the micron so JSON stays free of float noise."""
    return round(sum(span) / 2, 6)


def make_spec(model_file):
    def M(name, origin=None):
        return {"type": "model", "file": model_file, "params": {"part": name, **({"origin": list(origin)} if origin else {})}}
    WO = W_FRAME   # weapon frame: on the spin axis (spider, discs, shaft are drawn in robot coordinates about it)
    from .assembly_rig import revolutes
    JT = revolutes(RIG)   # spin axes read off the joint chain (assembly_rig)

    parts, fast, conn = [], [], []
    def P(**k): parts.append(k)
    def F(**k):
        k.setdefault("head", "countersunk"); k.setdefault("tool", "hex2"); k.setdefault("removable", True); fast.append(k)
    def C(a, b, m, r, **k): conn.append(dict(a=a, b=b, method=m, reason=r, **k))
    PLA = dict(material="pla_st", process="fdm")
    SIDES = ((-1, "l"), (1, "r"))

    # ---------------------------------------------------------------- structure
    P(id="tub", kind="structure", print_orientation="-z", rotates_with="fixed", solid_fraction=SOLID["tub"], color="#2a2c30", shape=M("chassis"), **PLA,
      thin_wall_deviation="matches original RVRN 2.0: the switch-slot rim is 0.5 mm wide on RV01_Chassis_1 too (RV01 section y=-10: slot edge x=27.0, outer face x=27.5) and 0.65 mm between the slot front and the deck pocket (section x=25: y -12.25 to -11.6)",
      label="RV01 printed chassis: closed X-ribbed deck (printed deck-down), open floor for the base panel, N10 keyhole side pockets, nut lobes, weapon-mount tabs and standoff lugs")
    P(id="base_panel", kind="structure", print_orientation="+z", rotates_with="fixed", color="#2a2c30", shape=M("base_panel"), **place("base_panel"), **PLA,
      thin_wall_deviation="the 1 mm panel is shallower than the 1.2 mm M2 CSK head (STEP RV26 has the same 5 countersunk seats): a 90 deg seat cone leaves a knife wedge under the countersink rim, unavoidable at this thickness (parity with RV26)",
      sharp_corners_ok="the panel's concave corners at (+-25.1,-25.5,4.5) are where its 1 mm plate edge butts the tub floor lip; RV26 is a flat plate against the RV01 lip (reference r 0.27), a round there would lift the panel off the lip and unseat bolt_b2/b3; the RV26 Chamfer2 is 1.3 mm away from these corners and there is no fillet on them in the dump",
      label="RV26 1 mm printed base panel, 5 M2 CSK into the floor heat-sets, 0.45 mm pads preload the N10s")
    P(id="top_panel", kind="armor", material="titanium", process="laser", stock="0.9 mm Ti Gr5 sheet", secondary_ops=["countersink"], rotates_with="fixed", color="#8d939b", shape=M("top_panel"), **place("top_panel"),
      label="0.9 mm Ti top panel: laser outline with 4 countersunk 2.2 corner holes, 4 M2 flat-head thread-forming screws into the column tops (material inferred, see REFERENCE.md)")
    # ---------------------------------------------------------------- weapon module
    P(id="mount_r", kind="structure", print_orientation="+x", rotates_with="fixed", solid_fraction=SOLID["mount"], color="#2a2c30", shape=M("mount_r", MNT_FRAME["r"]), **place("mount_r"), **PLA,
      label="RV03 XALT HD right weapon mount (8 mm): GR1507 stator on 4 M2 through the back spacer, notch on the chassis tab, 2 M3 CSK into the standoffs")
    P(id="mount_l", kind="structure", parent="mount_r", print_orientation="-x", rotates_with="fixed", solid_fraction=SOLID["mount"], color="#2a2c30", shape=M("mount_l", MNT_FRAME["l"]), **place("mount_l", "mount_r"), **PLA,
      label="RV02 XALT HD left weapon mount (8 mm): outboard MR85 bearing for the threaded shaft end, notch on the chassis tab, 2 M3 CSK into the standoffs")
    P(id="motor_spacer", kind="other", role="spacer", parent="mount_r", print_orientation="+x", rotates_with="fixed", color="#2a2c30", shape=M("motor_back_spacer", MNT_FRAME["r"]), **place("motor_spacer", "mount_r"), **PLA,
      label="1.5 mm printed motor back spacer: stator base off the mount, clears the rear bearing boss and the phase leads")
    P(id="weapon_motor_stator", kind="weapon_motor", catalog=MOTOR["stator"], parent="mount_r", **place("weapon_motor_stator", "mount_r"), rotates_with="fixed", exposed=True,
      exposed_reason="Drisk: the GR1507 bell is the hub of the weapon, inside the spacer bore between the two Hardox discs; the discs shield it radially",
      label="GR1507 outrunner, fixed half: stator and cross base on RV03, phase leads out the back",
      deviation="RVRN 2.0 STEP draws the GR1507 as one empty can with no stator, no windings and no leads; the real fixed stator stack, windings and the 3 phase leads (out of the base through the -Z arm, STEP shows no wire exit) are added: a real motor has them")
    P(id="weapon_motor_can", kind="other", role="rotor", catalog=MOTOR["can"], parent="spider", **place("weapon_motor_can", "spider"), rotates_with="weapon", exposed=True,
      exposed_reason="Drisk: the GR1507 bell is the hub of the weapon, inside the spacer bore between the two Hardox discs; the discs shield it radially",
      label="GR1507 bell and core: spins with the spider, wshaft and discs round the fixed stator")
    P(id="wbearing", kind="bearing", parent="mount_l", material="steel", process="cots", rotates_with="fixed", stock="MR85ZZ 5 x 8 x 2.5", color="#555555",
      deviation="bought part left out of the STEP (INDEX.txt lists no bearing): RV02 carries the 7.9 mm printed seat for it and the guide BOM lists an MR85ZZ; added for the shaft support",
      shape=_spec_bearing(), **place("wbearing", "mount_l"), label="MR85ZZ in the RV02 8 mm seat: outboard support of the threaded shaft end (inferred: the STEP shows the 7.9 seat but no bearing)")
    P(id="wshaft", kind="shaft", material="steel", process="cots", stock="GR1507 5 mm shaft (part of the motor): modelled whole, MR85 end X -18.7 through the bell and the rear bearing to its circlip end X 11.4", rotates_with="weapon", shaft_of="weapon_motor_can", parent="weapon_motor_can",
      deviation="the GR1507 shaft is part of the bought motor, which the STEP draws as one body (INDEX.txt lists no shaft); drawn separately here for the MR85 support and the spider collar",
      **place("wshaft", "weapon_motor_can"), shape=M("weapon_shaft", WO), color="#777777", solid_fraction=SOLID["shaft"],
      label="threaded end of the GR1507 shaft through the MR85 (its mass is in the motor)")
    P(id="spider", kind="weapon", material="aluminium", process="waterjet", stock="3 mm 7075 plate (one 2D profile: water-jet, no milling needed)",
      min_web_mm=WEB["spider"], min_web_reason="0.8 mm webs between the dog pockets and the rim are the designer's own (RVRN 2.0 STEP spider_1 measures 0.8 at the same four places)", rotates_with="weapon", parent="mount_r", **place("spider", "mount_r"), shape=M("spider", WO),
      joint=JT["spider"], color="#b8bcc2",
      weapon={"kind": "disc", "motor": "weapon_motor_stator", "cells": 2, "reduction": 1.0, "spin_axis": [1, 0, 0], "spin_dir": "ccw", "supported_both_ends": True, "teeth": 1},
      label="3 mm aluminium spider: bolted to the bell (4 M2 on r4.5), carries the disc stack on 4 M2 on r14")
    for nm, lab in (("disc_a", "inner"), ("disc_b", "outer")):
        P(id=nm, kind="other", role="blade", material="hardox", process="laser", stock="3 mm Hardox 450", parent="spider",
          min_web_mm=WEB["disc"], min_web_reason="0.9 mm webs beside the balance window are the designer's own (RVRN 2.0 STEP Drisk_floating_3 measures 0.9 at the same four places)", rotates_with="weapon", shape=M(nm, WO), **place(nm, "spider"), color="#d9dde2",
          label=f"Drisk_floating_3 ({lab}): 3 mm Hardox single-tooth disc, R16.5 rim 0.5 mm eccentric against the R23 tooth, 12 mm bore with 4 ramped dogs, 4 M2 on r14")
    P(id="dspacer", kind="other", role="spacer", parent="spider", rotates_with="weapon", print_orientation="+x", shape=M("drisk_spacer", WO), **place("dspacer", "spider"), color="#2a2c30", **PLA,
      label="Drisk_spacer_alt_x: 6 mm printed ring round the bell, 4 arc windows, 4 M2 on r14")
    for s, n in SIDES:
        mnt = f"mount_{n}"
        P(id=f"so_a{n}", kind="pin", role="standoff", material="aluminium", process="cots", rotates_with="fixed", color="#b8bcc2", stock="RV11 M3 x 25 aluminium standoff, 5 OD",
          shape=M(f"so_a_{n}"), features=sp_spec(s, f"so_a{n}")[2], label="RV11 25 mm alu standoff: front axle, clamps the mount, the side panel screws to its end")
        P(id=f"so_b{n}", kind="pin", role="standoff", material="aluminium", process="cots", rotates_with="fixed", color="#b8bcc2", stock="RV10 M3 x 15 aluminium standoff, 5 OD",
          shape=M(f"so_b_{n}"), label="RV10 15 mm alu standoff: nose, through the chassis lug, the fork and the wedgelet cheeks")
        P(id=f"fork_{n}", kind="fork", material="titanium", process="laser", stock="1.5 mm Ti Gr5 sheet", min_web_mm=FK_WEB, min_web_reason="every web is the laser minimum 0.75 x 1.5 mm sheet = 1.12 mm (rings round the standoff and pin holes; the STEP fork_5 draws 1.10 and 1.098)", parent=f"so_b{n}", rotates_with="fixed", color="#9aa0a6", shape=M(f"fork_{n}"), **place(f"fork_{n}"),
          label="fork_5: 1.5 mm Ti fork on the 15 mm standoff, tail pinned in the wedgelet cheek slot")
        P(id=f"wedgelet_{n}", kind="armor", deviation=f"RVRN 2.0 STEP: the wedgelet and the fork tine interpenetrate in the original (an interference there); we cut the tine's own {FK_X[s][1]-FK_X[s][0]:g} mm outline out of the wedgelet as its seat, so the fork sits in with interference 0, hence the wedgelet is short by the tine volume at x {FK_X[s][0]:g}..{FK_X[s][1]:g}", material="tpu", process="fdm", thin_wall_deviation="matches original RVRN 2.0: the sub-1.2 mm sections (ramp knife toe, SB countersink 0.2 mm off the floor, thin ribs) are measured from the STEP RV17/18/23/24 and kept for parity (user order)", solid_fraction=SOLID["tpu"], print_orientation="-z", parent=f"so_a{n}", rotates_with="fixed", color="#3c4048",
          shape=M(f"wedgelet_{n}"), cover_fasteners_deviation="RVRN 2.0 STEP: the wedgelet is clamped between the side panel nose and the 15 mm standoff end by bolt_s?b (listed in its `through`), and located on both standoffs; bolt_s?a seats the side panel directly on the 25 mm standoff end (the STEP wedgelet stops at |X| 38.5 and never enters that stack). Kept as designed; no extra screw (coordinator decision).",
          label=f"{WEDGE_REF[s]} TPU wedgelet: 50 deg ramp over the nose, cheeks round both standoffs and the fork tail")
        P(id=f"side_{n}", kind="armor", deviation="matches original RVRN 2.0: RV23/RV24 front leads the spider swept rim by the same amount at +-30 deg (STEP projection 64.45 mm vs ours 64.24 mm at -30 deg, within 0.5 mm)", material="tpu", process="fdm", thin_wall_deviation="matches original RVRN 2.0: the sub-1.2 mm sections (ramp knife toe, SB countersink 0.2 mm off the floor, thin ribs) are measured from the STEP RV17/18/23/24 and kept for parity (user order)", solid_fraction=0.9, print_orientation="+z", parent=f"so_a{n}", rotates_with="fixed", color="#3c4048", shape=M(f"side_panel_{n}_local"),
          features=sp_spec(s, f"so_a{n}")[0], mate=sp_spec(s, f"so_a{n}")[1],
          label=f"{SIDE_REF[s]} TPU side panel: battered S-wall round the wheels, 3 M3x8 CSK (two standoff ends, one chassis nut)")
        P(id=f"nut_c{n}", kind="nut", catalog="nut_m3_thin", **place(f"nut_c{n}"), rotates_with="fixed")
        # drive
        P(id=f"motor_{n}", kind="motor", catalog="n10_2200rpm_spicy", at=place_at(f"motor_{n}"), rot=place_rot(f"motor_{n}"), rotates_with="fixed")
        P(id=f"whub_r{n}", kind="pulley", solid_fraction=SOLID["hub"], rotates_with=f"wheel_r{n}", print_orientation="+x", shape=M(f"rear_hub_{n}"), parent="tub", **place(f"whub_r{n}"),
          thin_wall_deviation="matches original RVRN 2.0: RV21 draws the 0.5 mm O-ring flange, the 0.5 mm raised lip at the free end and the 0.2 mm end recess; kept for parity (user order)",
          joint=JT[f"whub_r{n}"], color="#333333", **PLA,
          label="RV21 printed rear hub 16 x 12: blind D-bore on the N10, O-ring groove, crowned F1 tyre seat, M2 grub on the flat")
        P(id=f"wheel_r{n}", kind="wheel", material="rubber", process="cots", tyre_of=f"whub_r{n}", rotates_with=f"wheel_r{n}", parent=f"whub_r{n}", shape=M(f"rear_tyre_{n}"), **place(f"wheel_r{n}", f"whub_r{n}"),
          color="#1b1b1b", stock="RV22 Scalextric F1 front tyre 21.5 x 14 x 9.5", label="Scalextric F1 tyre 21.5 x 14 x 9.5")
        P(id=f"whub_f{n}", kind="pulley", solid_fraction=SOLID["hub"], rotates_with=f"wheel_f{n}", print_orientation="+x", shape=M(f"front_hub_{n}"), parent=f"so_a{n}", **place(f"whub_f{n}", f"so_a{n}"),
          thin_wall_deviation="matches original RVRN 2.0: RV19 draws its three flanges 0.5 mm thick; kept for parity (user order)",
          joint=JT[f"whub_f{n}"], color="#333333", **PLA,
          label="RV19 micro hub 9 x 9 greased on the 25 mm standoff, O-ring groove inboard")
        P(id=f"wheel_f{n}", kind="wheel", material="rubber", process="cots", tyre_of=f"whub_f{n}", rotates_with=f"wheel_f{n}", parent=f"whub_f{n}", shape=M(f"front_tyre_{n}"), **place(f"wheel_f{n}", f"whub_f{n}"),
          color="#1b1b1b", stock="RV20 Scalextric micro SLX tyre 11 x 7 x 6", label="Scalextric micro tyre 11 x 7 x 6")
    P(id="battery", kind="battery", catalog="lipo_2s_180_turnabot", **place("battery"), retained="press_fit")
    P(id="rxesc", kind="esc", catalog="malenki_nano_rvrn2", **place("rxesc"), retained="strap",
      deviation="RV01/RV13: the Malenki is taped (kapton) to the deck in the STEP; with the cage ribs gone a 6 mm TPU strap (RV01 esc_tray strap slot, glued to the chassis walls over the board) holds it instead, so it cannot slide inverted (adds ~0.3 g, reversible)")
    P(id="wesc", kind="esc", catalog="bbb_ant_esc_rvrn2", **place("wesc"), retained="kapton")
    P(id="power_switch", kind="switch", catalog="switch_bbb_ant_rvrn2", at=place_at("power_switch"), rot=place_rot("power_switch"), retained="screws", marked=True, tool_free=True,
      off_dir=[0, -1, 0], label="BBB ant switch hung under the deck beside the top panel: lever flush in the deck slot, 2 M2 into the deck")
    for i, (x, y) in enumerate(INS):
        P(id=f"insert_b{i}", kind="insert", catalog="heatset_m2_4", at=place_at(f"insert_b{i}"))
    for i, (x, y) in enumerate(TOP_XY):
        P(id=f"insert_t{i}", kind="insert", catalog="heatset_m2_4", at=place_at(f"insert_t{i}"))
    P(id="esc_tray", kind="other", material="tpu", process="fdm", print_orientation="+z", rotates_with="fixed", shape=M("esc_tray"),
      label="TPU weapon-ESC tray (not in the STEP): glued to the base panel, lips hold the ESC when inverted",
      deviation="the STEP holds the weapon ESC with kapton tape alone; a hit that flips the robot or tears the tape would free the board, so a TPU tray with 0.1 mm lips holds it (adds 1.1 g, reversible)")

    P(id="bat_pad", kind="other", material="foam_tape", process="manual", rotates_with="fixed", shape=M("bat_pad"),
      label="Double-sided foam tape pad under the pack (not in the STEP): carries the pack 2 mm above the base panel",
      deviation="the STEP pack floats 2 mm over the base panel; a foam tape pad supports and retains it (adds ~0.05 g, reversible)")

    # ---------------------------------------------------------------- fasteners
    for i, (x, y) in enumerate(INS):
        F(id=f"bolt_b{i}", designation="M2x6", material="aluminium", **seat(f"bolt_b{i}"), through=["base_panel", "tub"], threads_into=f"insert_b{i}", tool="hex1.3",
          hole=panel_base.seat(i, local=False)[1].hole)
    for s, n in SIDES:
        mnt = f"mount_{n}"
        F(id=f"bolt_u{n}a", designation="M3x12", head="countersunk", material="aluminium", **seat(f"bolt_u{n}a"), through=[mnt], threads_into=f"so_a{n}", hole=_mount_csk(s, *SA, "M3x12")[1].hole,
          reason="FS9 M3x12 CSK alu, head flush in the mount's inner face")
        F(id=f"bolt_u{n}b", designation="M3x14", head="countersunk", reason="M3x14 CSK alu (STEP FS9 M3x12): through mount and lug, 12 mm bites only 3.9 mm of the 15 mm standoff", material="aluminium", **seat(f"bolt_u{n}b"), through=[mnt, "tub"], threads_into=f"so_b{n}", hole=_mount_csk(s, *SB, "M3x14")[1].hole)
        F(id=f"bolt_s{n}a", designation=SIDE_BOLT_DES["a"], head="countersunk", material="aluminium", reason="M3x10 CSK (STEP: M3x8): 8 mm bites only 4.2 mm of the standoff thread; 10 mm gives 6.2 (>= 1.5 d in aluminium)", **seat(f"bolt_s{n}a"), through=[f"side_{n}"], threads_into=f"so_a{n}", hole=_side_seat("a", SA, s)[1].hole)
        F(id=f"bolt_s{n}b", designation=SIDE_BOLT_DES["b"], head="countersunk", material="aluminium", reason="M3x10 CSK (STEP: M3x8): the head sits 5.3 mm out from the 15 mm standoff end, so 8 mm bites 2.7 mm; 10 mm bites 4.7", **seat(f"bolt_s{n}b"), through=[f"side_{n}", f"wedgelet_{n}"], threads_into=f"so_b{n}", hole=_side_seat("b", SB, s)[1].hole)
        F(id=f"bolt_s{n}c", designation=SIDE_BOLT_DES["c"], head="countersunk", material="aluminium", reason="alu M3 CSK (Build Guide: aluminium bolts for weight; the STEP draws stainless)", **seat(f"bolt_s{n}c"), through=[f"side_{n}", "tub"], threads_into=f"nut_c{n}", hole=_side_seat("c", NUT, s)[1].hole)
    for k, (dy, dz) in enumerate((STATOR_PCD / 2 * u, STATOR_PCD / 2 * v) for u, v in STATOR_DIRS):
        F(id=f"bolt_wm{k}", designation="M2x8", head="button", tool="hex1.3", material="titanium", **seat(f"bolt_wm{k}"), hole=_stator_hole(1, dy, dz)[1].hole, through=["mount_r", "motor_spacer"],
          threads_into="weapon_motor_stator", reason="button heads (one hex1.3 key for every M2) sunk in the RV03 boss counterbores (inferred: the STEP shows the 4.4 counterbores, not the screws)")
    for k, (hub_c, bolt_c) in enumerate(zip(_polar(HUB_R), _polar(BOLT_R))):
        dy, dz = _disc_local(*hub_c)
        F(id=f"bolt_p{k}", designation="M2x6", head="button", tool="hex1.3", material="titanium", **seat(f"bolt_p{k}"), through=["spider"], threads_into="weapon_motor_can", hole=_stack_hole("M2x6", DR_X["spider"][0], dy, dz, 1, SPIDER_T).hole,
          access_before=["mount_l", "wbearing"], reason="spider to bell, fitted before the left mount goes on (inferred)")
        dy, dz = _disc_local(*bolt_c)
        F(id=f"bolt_d{k}", designation="M2x16", head="button", tool="hex1.3", material="titanium", **seat(f"bolt_d{k}"),
          through=["disc_b", "dspacer", "disc_a"], threads_into="spider", hole=_stack_hole("M2x16", DR_X["disc_b"][1], dy, dz, -1, DISC_T * 2 + SPACER_T).hole,
          access_before=["tub", "mount_r", "motor_spacer"],
          reason="stack screwed into the spider from the back (heads on disc_b, 2 mm of thread in the 3 mm alu spider tapped M2): no nuts, since the STEP has none (inferred: it has the 2.2 holes but no screws)")
    for i, (x, y) in enumerate(TOP_BOLT_XY):
        F(id=f"bolt_t{i}", designation="M2x5", head="button", tool="hex1.3", **seat(f"bolt_t{i}"), through=["top_panel", "tub"], threads_into=f"insert_t{i}",
          reason="M2 flat head in the panel's 90 deg countersink, thread-forming into the 1.7 column-top pilot (inferred: the STEP top panel has the countersunk 2.2 holes but no screws)",
          hole=panel_top.seat(i)[1].hole)
    for i, yy in enumerate(SW_SCREW_Y):
        F(id=f"bolt_sw{i}", designation="M2x3", head="button", tool="hex1.3", **seat(f"bolt_sw{i}"), through=["power_switch", "tub"], threads_into="tub", access_before=["base_panel"], hole=_switch_hole(yy)[1].hole,
          reason="thread-forming into the 1.7 pilot holes either side of the switch flange; heads clamp the flange to the deck underside (inferred)",
          waive={"fastener.hole_record": "switch retention only, no structural load; RVRN RV01 has 5 FS1_M2_heatsert, all base panel, none at the switch, the switch's 2 M2 screws self-tap in plastic"})

    # ---------------------------------------------------------------- connections
    for s, n in SIDES:
        mnt = f"mount_{n}"
        C(f"motor_{n}", "tub", "interlock", "N10 gearbox boss seats in the side-wall keyhole, its front face bears on the stop wall; the base-panel pad preloads it up")
        C(f"whub_r{n}", f"motor_{n}", "press_fit", "Blind D-bore on the 3 mm D-shaft, M2 grub on the flat", interference_mm=PRESS["hub"], mechanical_key=True)
        C(f"wheel_r{n}", f"whub_r{n}", "press_fit", "F1 tyre (14 ID) stretched over the crowned 14 mm seat", interference_mm=PRESS["tyre"], mechanical_key=True)
        C(f"whub_f{n}", f"so_a{n}", "shaft", "Micro hub runs greased on the 25 mm standoff between the mount face and the side panel")
        C(f"wheel_f{n}", f"whub_f{n}", "press_fit", "Micro tyre stretched into the 7.4 seat between the flanges", interference_mm=PRESS["micro"], mechanical_key=True)
        for nm in "ab":
            C(f"so_{nm}{n}", mnt, "screw", "M3x12 CSK alu through the mount into the standoff end")
            C(f"so_{nm}{n}", f"side_{n}", "screw", "Side panel screwed to the standoff's outer end (M3x8 CSK)", mechanical_key=True)
        C(f"so_b{n}", "tub", "pin", "Nose standoff clamped between the mount and its chassis lug", mechanical_key=True)
        C(f"so_a{n}", "tub", "pin", "Axle standoff passes through the 5 mm lug hole", mechanical_key=True)
        C(f"fork_{n}", f"so_b{n}", "pin", "Fork hangs on the 15 mm standoff (5.3 hole)", mechanical_key=True)
        C(f"fork_{n}", f"wedgelet_{n}", "interlock", "Fork tail clamped in the wedgelet cheek slot: cannot rotate about the standoff")
        C(f"wedgelet_{n}", f"so_a{n}", "pin", "Wedgelet ring over the axle standoff", mechanical_key=True)
        C(f"wedgelet_{n}", f"so_b{n}", "pin", "Wedgelet cheeks over the nose standoff", mechanical_key=True)
        C(f"wedgelet_{n}", f"side_{n}", "interlock", "Side panel nose holds the wedgelet on the standoffs")
        C(f"side_{n}", "tub", "screw", "Side panel screwed into the captive thin nut in the chassis wall")
        C(f"nut_c{n}", "tub", "press_fit", "Thin M3 nut in the hex pocket inside the wall: cannot turn or fall in", interference_mm=PRESS["nut"], mechanical_key=True)
        C(mnt, "tub", "interlock", "Mount notch drops over the chassis tab: the tab takes fore/aft and vertical load, the screws only clamp", mechanical_key=True)
        C(f"belt_{n}", f"whub_r{n}", "interlock", "O-ring stretched into the rear hub groove; its tension and the groove flanks keep it on the pulley")
        C(f"belt_{n}", f"whub_f{n}", "interlock", "O-ring in the front hub groove: drives the front wheel")
    C("weapon_motor_stator", "mount_r", "screw", "Stator base on 4 M2 through RV03 and the back spacer")
    C("motor_spacer", "mount_r", "interlock", "Spacer clamped between the stator base and RV03 by the 4 motor screws", mechanical_key=True)
    C("spider", "weapon_motor_can", "screw", "Spider on the bell, 4 M2 on r4.5; its 5.2 bore centres it on the shaft collar", mechanical_key=True)
    C("disc_a", "spider", "pin", "Disc located and driven by the 4 r14 stack bolts and the spider dogs; the bolts clamp it in shear", mechanical_key=True)
    C("dspacer", "disc_a", "pin", "Spacer on the 4 stack bolts between the discs", mechanical_key=True)
    C("disc_b", "dspacer", "pin", "Outer disc located by the 4 stack bolts through the spacer and clamped by their nuts", mechanical_key=True)
    C("wshaft", "wbearing", "shaft", "Threaded shaft end in the MR85 inner race: second support of the drisk")
    C("wshaft", "weapon_motor_can", "press_fit", "The shaft is the GR1507 motor's own steel shaft, pressed into the bell at the factory", interference_mm=PRESS["shaft"], mechanical_key=True)
    C("wshaft", "spider", "press_fit", "Spider bore on the shaft collar", interference_mm=PRESS["shaft"], mechanical_key=True)
    C("wbearing", "mount_l", "press_fit", "MR85 pressed into the 7.9 seat", interference_mm=PRESS["bearing"], mechanical_key=True)
    C("mount_l", "mount_r", "interlock", "Both mounts tied by the standoffs and the chassis tabs")
    C("base_panel", "tub", "screw", "Base panel under the open floor, 5 M2 CSK into heat-sets")
    C("top_panel", "tub", "screw", "Ti top panel held by 4 M2 flat-head screws through its countersunk corner holes into M2 heat-sets in the column tops (the STEP has the holes, not the screws)")
    C("battery", "tub", "press_fit", "Pack between the motor wall, the insert columns and the deck", interference_mm=PRESS["pack"], mechanical_key=True)
    C("battery", "bat_pad", "tape", "Pack underside taped to the foam pad (double-sided), which holds it against sliding")
    C("bat_pad", "base_panel", "tape", "Foam pad stuck to the base panel skin; deck and top panel close the pack in from above")
    C("rxesc", "tub", "interlock", "Malenki held by a TPU strap, boxed by the front wall and the deck; the weapon ESC under it")
    C("wesc", "esc_tray", "interlock", "weapon ESC in the TPU tray lips (0.1 mm); lips on all four sides, the Malenki +z")
    C("esc_tray", "base_panel", "glue", "TPU tray contact-glued to the base panel top")
    C("power_switch", "tub", "screw", "Switch flange clamped under the deck by 2 M2", mechanical_key=True)

    # O-ring belts (front micro hub <-> rear hub, plane |X| 31.3)
    def belt_shape(s):
        # O-ring: round section (stock cs) swept along the closed belt path round the rear hub groove (R = groove floor + cs/2)
        # and the front hub groove (r), joined by the two external tangent runs; centreline plane = groove centre |X|
        (ay, az), (by, bz) = (RY, RZ), SA
        c = math.hypot(by - ay, bz - az)
        d = ((by - ay) / c, (bz - az) / c)
        k = (BELT_R - BELT_r) / c
        h = math.sqrt(UNIT - k * k)
        P2 = lambda y, z: [round(-z, BELT_DIGITS), round(y, BELT_DIGITS)]   # noqa: E731 - the YZ plane as _prism_yz lays it out
        segs, tgt = [], []
        for sg in (1, -1):
            n = (k * d[0] - sg * h * d[1], k * d[1] + sg * h * d[0])
            tgt.append((P2(ay + BELT_R * n[0], az + BELT_R * n[1]), P2(by + BELT_r * n[0], bz + BELT_r * n[1])))
        (ra, fa), (rb, fb) = tgt
        segs = [["line", ra, fa], ["arc", fa, P2(by + BELT_r * d[0], bz + BELT_r * d[1]), fb], ["line", fb, rb],
                ["arc", rb, P2(ay - BELT_R * d[0], az - BELT_R * d[1]), ra]]
        return {"type": "place", "shape": {"type": "ring", "radius": O_RING[1] / 2, "path": segs}, "at": [s * BELT_X["centre"], 0, 0], "rot": [0, 90, 0]}
    c_ = math.hypot(SA[0] - RY, SA[1] - RZ)
    loop = 2 * math.sqrt(c_ ** 2 - (BELT_R - BELT_r) ** 2) + math.pi * (BELT_R + BELT_r) + 2 * (BELT_R - BELT_r) * math.asin((BELT_R - BELT_r) / c_)
    ORING = O_RING
    BELT_L = round(math.pi * ORING[0], 1)
    for s, n in SIDES:
        P(id=f"belt_{n}", kind="belt", material="rubber", process="cots", deviation="O-rings are bought parts and are not modelled in the RVRN 2.0 STEP (the original CAD shows the groove and hub only); modelled here as a stretched loop for fit and clearance checks", shape=belt_shape(s), color="#3f7fbf",
          belt={"pulleys": [f"whub_r{n}", f"whub_f{n}"], "kind": "o_ring", "length_mm": BELT_L, "width_mm": ORING[1], "stock": {"id_mm": ORING[0], "cs_mm": ORING[1]}},
          label=f"stock {ORING[0]} x {ORING[1]} nitrile O-ring ({PCT * (loop / BELT_L - 1):.0f} % stretch on the 61 mm centres): front wheel drive (not in the STEP; the hub grooves are)")

    wires = [dict(_Wr(*w[:-1]), **w[-1]) for w in WIRES]
    return dict(parts=parts, fasteners=fast, connections=conn, wires=wires, intent=intent_checks())


def intent_checks():
    """Functional design-intent probes (robot.checks.intent): each tests what the feature is FOR."""
    out = []
    A = lambda rule, why, **k: out.append(dict(rule=rule, why=why, **k))  # noqa: E731
    for s, n in ((-1, "l"), (1, "r")):
        A("keyed_bore", "the N10 shaft is a 3 mm D; the flat in the blind bore drives the hub (a round printed bore slips at stall)",
          part=f"whub_r{n}", axis="x", at=[s * HUB_PROBE_X, RY, RZ], span=sorted(s * x for x in HUB_BORE_SPAN))
        A("tyre_retention", "the F1 tyre (13 mm relaxed ID, assumed; the STEP shows it stretched to 14) is held by stretch over the 45 deg crown, so side hits cannot walk it off",
          hub=f"whub_r{n}", axis=[1, 0, 0], at=[0, RY, RZ], span=sorted(s * x for x in TYRE_SPAN), tyre_id=TYRE_ID, min_interference=TYRE_STRETCH)
        A("captive_nut", "the thin M3 nut sits in a hex pocket inside the wall: with the side panel off it cannot turn or drop into the electronics bay",
          nut=f"nut_c{n}", host="tub", move=NUT_MOVE)
        A("wheel_clearance", "a tyre rubbing the armour or chassis is a brake on a 2-motor 4WD", wheel=f"wheel_r{n}", exclude=[f"whub_r{n}", f"belt_{n}"], min=WHEEL_MIN_GAP)
        A("wheel_clearance", "front tyres run on the standoff axle and must clear the wedgelet and side panel", wheel=f"wheel_f{n}",
          exclude=[f"whub_f{n}", f"so_a{n}", f"belt_{n}"], min=WHEEL_MIN_GAP)
        A("flush_head", "side-panel screws sit in TPU countersinks: nothing proud for a spinner to catch", fastener=f"bolt_s{n}a", host=f"side_{n}", out=[s, 0, 0])
        A("flush_head", "mount screws are countersunk in the inner face, the face beside the disc rim", fastener=f"bolt_u{n}a", host=f"mount_{n}", out=[-s, 0, 0])
        A("seat_locates", "the N10 gearbox boss seats in the keyhole and its body bears on the stop walls: shaft concentric, stall torque reacted by the chassis",
          part=f"motor_{n}", host=["tub", "base_panel"], axis=[1, 0, 0], at=[s * MOTX, RY, RZ], play=SEAT_PLAY, turn_deg=SEAT_TURN_DEG)
    for n in ("l", "r"):
        A("notch_bears", "a hit drives the mount back; the notch on the chassis tab bears it in compression, the bolts only clamp",
          part=f"mount_{n}" if n == "l" else "mount_r", lug="tub", bolts=[f"bolt_u{n}a", f"bolt_u{n}b"], dir=[0, -1, 0])
    for pid, up in (("tub", "-z"), ("mount_r", "+x"), ("mount_l", "-x"), ("whub_rr", "+x"), ("whub_rl", "-x"), ("whub_fr", "+x"), ("whub_fl", "-x"),
                    ("wedgelet_r", "-z"), ("wedgelet_l", "-z"), ("side_r", "+z"), ("side_l", "+z"), ("motor_spacer", "+x")):
        A("support_free", "every printed part prints without supports in its declared orientation", part=pid, up=up)
    # exceptions (STEP RV01, by design): the rear wall is a triangulated truss - 2 mm ribs round 1 mm deep pockets, the ribs carry
    # the load and the 1 mm web only closes the box; the 1 mm lip below the base-panel rabbet only locates the panel edge
    A("min_wall", "2 mm walls are 4+ perimeters: the box takes wheel-side and clamp loads without delaminating", part="tub", min=WALL_MIN, envelope=True, **{"except": WALL_EXCEPT})
    A("insert_column", "printed deck-down, each heat-set insert sits on a solid column back to the deck (the first layers): no hanging boss to pull out",
      part="tub", inserts=[[x, y, CH["deck"]] for x, y in INS], floor_z=INS_Z[0], r=2.2)
    x, w = CH["x"], CH["wall"]
    # a corner sharp in the original may be listed as exempt=[{"at": [x, y], "reason": "<cites RVRN / RVnn / FSn>"}]
    # (still probed; INFO "matches original" within 0.5 mm; JSON: "exempt": [...] on the same intent entry)
    A("fillet", "inside wall corners are radiused: sharp PLA inside corners crack under impact", part="tub", axis="z", h=FILLET_H,
      at=[[-x + w, CH["y0"] + w], [x - w, CH["y0"] + w], [x - w, CH["y1"] - w], [-x + w, CH["y1"] - w]],
      exempt=[dict(at=[sg * fx, CH["y0"] + w - OVER], reason="RVRN RV01 square, N10 gearbox plate seat, r=0.0 (RV01_Chassis_1 z=10 slice: wall x=27.5 meets y=-35.6 at 90 deg, seat arc starts at x=26.5; ours squares at x=%.2f and the seat arc starts at x=%.2f)" % (x - w + OVER, FILLET_REAR_X))
              for sg in (1, -1) for fx in (x - w + OVER, FILLET_REAR_X)])
    A("tool_count", "pit kit: one hex key per screw size (1.3 for M2, 2 for M3); the weapon swap needs only the 2 mm key", max=2, module_max=1,
      module=["bolt_ula", "bolt_ulb", "bolt_ura", "bolt_urb"])
    rot = ["spider", "disc_a", "disc_b", "dspacer"]
    A("wire_clear_rotor", "phases and power leads stay out of the drisk's swept volume", rotor=rot, axis=[1, 0, 0], at=[0, WY, WZ], min=ROTOR_CLEAR,
      via={"w_wesc_m": PHASE_VIA})
    return out


def _prism_yz(poly, x0, x1):
    pts = [[round(-z, BELT_DIGITS), round(y, BELT_DIGITS)] for y, z in list(poly.exterior.coords)[:-1]]
    x0, x1 = min(x0, x1), max(x0, x1)
    return {"type": "place", "shape": {"type": "prism", "points": pts, "height": x1 - x0}, "at": [(x0 + x1) / 2, 0, 0], "rot": [0, 90, 0]}


def _spec_bearing():
    def cyl(r, h):
        return {"type": "place", "shape": {"type": "cylinder", "radius": r, "height": h}, "at": [0, 0, 0], "rot": [0, 0, 0]}   # on the bearing's own axis (z)
    return {"type": "subtract", "base": cyl(BRG["od_r"], BRG["w"]), "cut": [cyl(BRG["bore_r"], BRG["od_r"])]}


def _Wr(i, a, b, awg, kind, sl): return {"id": i, "from": a, "to": b, "awg": awg, "kind": kind, "slack_mm": sl}


def _drisk_to_world():
    a = math.radians(DR_ROT)
    D = [[math.cos(a), -math.sin(a), 0, -WY], [math.sin(a), math.cos(a), 0, WZ], [0, 0, 1, -_mid(DR_X["spider"])], [0, 0, 0, 1]]
    import numpy as np
    return (np.array(REF_TO_WORLD, float) @ np.array(D, float)).round(6).tolist()


def _micro_to_world(side):
    import numpy as np
    return (np.array(REF_TO_WORLD, float) @ np.array(MICRO_T[side], float)).round(6).tolist()


def _fork_dev(s):
    return [dict(near=[s * FORK_DEV["x"], FORK_DEV["y"], FORK_DEV["z"]], r=FORK_DEV["r"], reason="laser-cut Ti cannot hold the STEP's knife tip (0.0 mm): the tip ends "
                 "in a 0.45 mm land at full length (laser titanium min web 0.4 mm)")]


def _wedge_dev(s):
    slit = "the STEP draws the Ti fork tine inside the TPU nose (interpenetrating solids); the TPU has the 1.5 mm slit the tine slides into"
    toe = "the STEP ramp ends in a 0 mm knife toe FDM TPU cannot print; the toe stands on a 0.85 mm land at the same reach"
    boss = "the STEP nose tab interpenetrates the weapon mount's boss; the tab is cut by the boss outline plus the WG_MOUNT_GAP clearance, and its arc round SB stands WG_MOUNT_GAP off the chassis lug radius"
    return ([dict(path=[[s * WG_TAB_DEV["x"], WG_TAB_DEV["y"], z] for z in WG_TAB_DEV["z"]], r=WG_TAB_DEV["r"], max_mm3=WG_TAB_DEV["mm3"], reason="RV17 STEP: " + boss),
             dict(path=[[s * FORK_PATH_X, y, z] for y, z in FORK_PATH_YZ], r=FORK_PATH_R, max_mm3=FORK_PATH_MM3,
                  reason="RV17 STEP: the Ti fork tine interpenetrates the solid TPU cheek (26 mm3, y 41.5-50.1); " + slit),
             dict(path=[[s * x, *TOE_DEV_YZ] for x in TOE_DEV_X], r=TOE_DEV_R, max_mm3=TOE_DEV_MM3, reason="RV17 STEP: " + toe)])


def _side_dev(s):
    return [dict(near=[s * SIDE_DEV_X, SB[0], SB[1]], r=SIDE_DEV_R, reason="nose screw seat: ISO 10642 M3 head is 6.6 (catalog max), the STEP's "
                 "6.2 bore would trap it; 6.7 seat with a straight head bore out through the nose for the driver")]


def _GRUB_DEV(s):
    return [] if not HUB_GRUB_PRINTABLE else [{"near": [s * 34.4, RY, RZ + 3.0], "r": 3.5,
             "reason": "grub bore is the catalog M2 tap drill (1.6, robot.cad.holes) 0.2 inboard, not the STEP 2.5 hole at |X| 34.5: "
                       "a 2.5 hole breaks into both 45 deg tyre-seat ramps and leaves knife edges (mfg.thin_wall 0.01 mm); the grub "
                       "threads the 1.6 bore and the captive nut, so it clamps the flat the same"}]


def reference_cad():
    def R(part, file, mode="shape", **k):
        return dict(part=part, file=file, mode=mode, **k)
    dt = _drisk_to_world()
    rows = [
        R("tub", "RV01_Chassis_1.stl", tol_mm=TOL["loose"], tol_vol_frac=VOL["part"], note="RV01 chassis",
          deviations=[dict(near=[sx * KEYHOLE_DEV[0], KEYHOLE_DEV[1], KEYHOLE_DEV[2]], r=KEYHOLE_DEV_R, reason="N10 keyhole opened into a U-slot to the floor so the gearbox boss and shaft drop in from below with the base panel off (the STEP closes the keyhole, the shaft cannot be threaded through it)")
             for sx in (1, -1)]
          + [dict(near=[sx * sum(N10_KEY) / 2, sum(KEY_SPAN) / 2, N10_TOP - KEY_DROP / 2], r=KEY_DEV_R, reason="N10 key tab reaches KEY_DROP below the gearbox plate top so it keys between the plates and stops the motor inboard (the STEP tab is flush, which leaves the motor free to slide in x: retention.loose)")
             for sx in (1, -1)]
          + [dict(near=[SWX, yy, CH["deck"]], r=SWX_DEV_R, reason="switch pilot holes follow the switch, which sits 0.45 mm in from the STEP X 25.0 so its body clears the 27.5 inner wall face (the STEP switch penetrates the wall 0.4 mm)")
             for yy in SW_SCREW_Y]
          + [dict(near=[x, y, FOOT_DEV_Z], r=FOOT_DEV_R, reason="RV01 column foot is an R8 blend (RV01 Chassis.SLDPRT Fillet2, 4 edges); flared to R3.7 because the 1.0 mm base skin cannot seat a 1.2 mm M2 flat head")
             for x, y in INS]
          + [dict(near=[sx * LOBE_DEV[0], LOBE_DEV[1], LOBE_DEV[2]], r=LOBE_DEV_R, reason="lobe tail below Y -11.7 trimmed to the side-panel inner face: the STEP lobe and side panel overlap by 31 mm3, the tub does not duplicate it")
             for sx in (1, -1)]),
        R("base_panel", "RV26_Base_Panel_1.stl", tol_mm=TOL["tight"], note="RV26 1 mm panel",
          deviations=[dict(near=[x, y, BASE_DEV_Z], r=PANEL_DEV_R, reason="R2.6 edge ears + 4.5 countersink on a 3.4 hole: an ISO 10642 M2 head (4.4 x 1.2) needs 1.6 mm of seat; the STEP's 3.2 x 0.5 seat leaves it proud")
                      for x, y in INS]),
        R("top_panel", "Top_Panel_1.stl", tol_mm=TOL["tight"], note="0.9 mm top panel",
          deviations=[dict(near=[x, y, TOP_DEV_Z], r=PANEL_DEV_R, reason="4.5 countersink on a 3.5 hole (STEP 3.65 on 2.2) for an ISO M2 flat head, ear R2.7 (STEP 2.5) to keep 0.45 mm of Ti round it")
                      for x, y in INS[:4]]
          + [dict(near=[x, y, TOP_TEXT_DEV_Z], r=TOP_TEXT_DEV_R, reason="0.1 mm engraved lettering, laser-etch omitted")
             for x, y in TOP_TEXT_DEV_XY]),
        R("mount_l", "RV02_XALT_HD_left_hand_weapon_mount_1.stl", tol_mm=TOL["std"],
          deviations=[{"near": [-MNT_TIP_DEV[0], MNT_TIP_DEV[1], MNT_TIP_DEV[2]], "r": MNT_TIP_DEV_R, "reason": "the STEP notch top is a zero-thickness wedge (mfg.thin_wall); thickened to a printable wall, rearmost point unchanged"}, {"near": [-NOSE_DEV[0], NOSE_DEV[1], NOSE_DEV[2]], "r": NOSE_DEV_R,
                       "reason": "nose pad round the nose CSK (NOSE_PAD_R): the ISO 10642 d7 cone is wider than the STEP R3.25 nose arc and left a 0 mm knife edge (mfg.thin_wall); up to ~1 mm of added material at the nose underside and front edge, so the countersink keeps a 0.9 mm wall"}]),
        R("mount_r", "RV03_XALT__HD_Right_hand_weapon_mount_1.stl", tol_mm=TOL["std"],
          deviations=[{"near": [MNT_TIP_DEV[0], MNT_TIP_DEV[1], MNT_TIP_DEV[2]], "r": MNT_TIP_DEV_R, "reason": "the STEP notch top is a zero-thickness wedge (mfg.thin_wall); thickened to a printable wall, rearmost point unchanged"}, {"near": [NOSE_DEV[0], NOSE_DEV[1], NOSE_DEV[2]], "r": NOSE_DEV_R,
                       "reason": "nose pad round the nose CSK (NOSE_PAD_R): the ISO 10642 d7 cone is wider than the STEP R3.25 nose arc and left a 0 mm knife edge (mfg.thin_wall); up to ~1 mm of added material at the nose underside and front edge, so the countersink keeps a 0.9 mm wall"}] + [{"near": [STATOR_DEV_X, WY + dy, WZ + dz], "r": TAP_DEV_R,
                       "reason": "STEP 16.4-17.15 lead-in cone under each stator counterbore left out: the d3.5 button head needs a flat seat on the 17.15 floor (fastener_seat.head_bearing)"}
                      for dy, dz in stator_bolt_circle()] + _lead_groove_dev()),
        R("motor_spacer", "Motor_back_spacer_1.stl", tol_mm=TOL["tight"]),
        R("spider", "spider_1.stl", tol_mm=TOL["std"], ref_to_world=dt,
          deviations=[dict(near=[sum(DR_X["spider"]) / 2, *_disc_local(*c)], r=TAP_DEV_R,
                           reason="r14 stack hole is the M2 tap drill (1.6) where the stack screws thread into the spider; the STEP shows the 2.2 clearance and no screw or nut")
                      for c in _polar(BOLT_R)]),
        R("disc_a", "Drisk_floating_3_1.stl", tol_mm=TOL["std"], ref_to_world=dt),
        R("disc_b", "Drisk_floating_3_2.stl", tol_mm=TOL["std"], ref_to_world=dt),
        R("dspacer", "Drisk_spacer_alt_x_1.stl", tol_mm=TOL["std"], ref_to_world=dt),
        R("wedgelet_l", "RV17_Wedgelet_LH_1.stl", tol_mm=TOL["wedge"], tol_vol_frac=VOL["part"], deviations=_wedge_dev(-1)),
        R("wedgelet_r", "RV18_Wedgelet_RH_1.stl", tol_mm=TOL["wedge"], tol_vol_frac=VOL["part"], deviations=_wedge_dev(1)),
        R("side_l", "RV23_side_panel_LH_1.stl", tol_mm=TOL["loose"], tol_vol_frac=VOL["part"], deviations=_side_dev(-1)),
        R("side_r", "RV24_Mirrorside_panel_RH_1.stl", tol_mm=TOL["loose"], tol_vol_frac=VOL["part"], deviations=_side_dev(1)),
        R("fork_l", "fork_5_2.stl", tol_mm=TOL["std"], deviations=_fork_dev(-1)), R("fork_r", "fork_5_1.stl", tol_mm=TOL["std"], deviations=_fork_dev(1)),
        R("whub_rl", "RV21_Rear_Wheel_1.stl", tol_mm=TOL["std"], tol_vol_frac=VOL["hub"], deviations=_GRUB_DEV(-1)),
        R("whub_rr", "RV21_Rear_Wheel_2.stl", tol_mm=TOL["std"], tol_vol_frac=VOL["hub"], deviations=_GRUB_DEV(1)),
        R("whub_fl", "RV19_Hub_Micro_1.stl", tol_mm=TOL["std"], ref_to_world=_micro_to_world("l")),
        R("whub_fr", "RV19_Hub_Micro_2.stl", tol_mm=TOL["std"], ref_to_world=_micro_to_world("r")),
        R("so_al", "RV11_m3_25mm_aluminium_standoff_1.stl", mode="envelope", tol_mm=TOL["tight"], tol_vol_frac=VOL["standoff"]),
        R("so_bl", "RV10_m3_standoff_15mm_1.stl", mode="envelope", tol_mm=TOL["tight"], tol_vol_frac=VOL["standoff"]),
        R("wheel_rl", "RV22_Scalextric_F1_Front_tyre_1.stl", mode="envelope", tol_mm=TOL["tight"]),
        R("wheel_fl", "RV20_11OD_7ID_6W_Micro_slx_1.stl", mode="envelope", tol_mm=TOL["tight"], ref_to_world=_micro_to_world("l")),
        R("motor_l", "RV12_N10_2200_RPM_1.stl", mode="envelope", tol_mm=TOL["motor"], tol_vol_frac=VOL["motor"]),
        R("weapon_motor_can", "GR1507_1.stl", mode="envelope", with_parts=["weapon_motor_stator", "wshaft"], tol_mm=TOL["motor"], tol_vol_frac=VOL["motor"],
          note="fixed half + rotating bell compared together; the STEP bell is empty, the real stator stack and windings sit in it (declared on the part)"),
        R("battery", "RV16_Turnabot_180mah_2s_1.stl", mode="envelope", tol_mm=TOL["motor"], tol_vol_frac=VOL["standoff"]),
        R("rxesc", "RV13_Malenki_nano_1.stl", mode="envelope", tol_mm=TOL["motor"], tol_vol_frac=VOL["motor"]),
        R("wesc", "RV14_Brushless_ESC__1.stl", mode="envelope", tol_mm=TOL["motor"], tol_vol_frac=VOL["motor"]),
        R("power_switch", "RV15_BBB_Antweight_Switch_1.stl", mode="envelope", tol_mm=TOL["loose"], tol_vol_frac=VOL["switch"]),
        R("nut_cl", "hex_thin_nut_gradeb_bsi_BS_EN_24036_-_M3_-_N_1.stl", mode="envelope", tol_mm=TOL["tight"], tol_vol_frac=VOL["motor"]),
    ]
    return {"dir": REF_DIR, "ref_to_world": REF_TO_WORLD, "iou_min": REF_IOU_MIN, "placement_tol_mm": TOL["std"], "parts": rows}


def _lead_groove_dev():
    """reference_cad capsule waiver along RV03's phase-lead C-groove (the STEP has none: its leads run free over the lug)."""
    (y0, z0), (y1, z1) = lead_groove_ends()
    return [{"path": [[LEAD_GROOVE_X, y0, z0], [LEAD_GROOVE_X, y1, z1]], "r": LEAD_DEV_R, "max_mm3": LEAD_DEV_MAX_MM3,
             "reason": "phase-lead C-groove in the inner face (added, not in the STEP): the twisted 3 x AWG24 bundle snaps through a 3.0 mouth into a "
                       "R2.0 channel from the stator exit to the lug top: the original RV03/STEP has no lead channel (leads run free over the lug), so the leads are retained and held "
                       "clear of the disc bolt heads (wire.exterior_support, wire.rotor_clearance)"}]


def main():
    spec_dir = os.path.join(HERE, "..")
    out_spec = os.path.join(spec_dir, "spec.json")
    out_tpl = os.path.join(ROOT, "robot/templates/revron.json")
    for out, mf in ((out_spec, "src/build_revron.py"), (out_tpl, "../../robots/revron/src/build_revron.py")):
        body = make_spec(mf)
        spec = dict(name="Revron", profile="aws2025", robot_type="vertical_spinner", locomotion="roller", archetype="vertical_spinner_forks",
                    archetype_params=ARCHETYPE_PARAMS, targets=TARGETS, weapon_lock=WEAPON_LOCK, reference_bom=REF_BOM, reference_doc=REFERENCE_DOC,
                    electronics=ELECTRONICS, can_run_inverted=False, allow_overlap=ALLOW_OVERLAP, claims=CLAIMS, sharp_ok=SHARP_OK,
                    teardown=TEARDOWN, module_teardown=MODULE_TEARDOWN, service_pose=SERVICE_POSE, reference_cad=reference_cad(),
                    start_pose={f"whub_r{n}": HUB_SPIN_DEG for n in "lr"},   # spin of the rear hubs on their shafts (STEP pose)
                    asm_dump={"rig": "revron.joints:RIG"},   # asm.mate: our assembly mates (joints.Rig)
                    renders={"dir": "renders", "views": ["iso.png", "top.png", "back.png", "exploded.png"]}, **body)
        spec["modules"] = [{"id": "weapon_module", "root": "mount_r", "note": MODULE_NOTE,
                            "parts": [p["id"] for p in spec["parts"] if _root(spec["parts"], p) == "mount_r" and p["id"] != "mount_r"]}]
        json.dump(spec, open(out, "w"), indent=1)
    print("wrote", out_spec, len(spec["parts"]), "parts", len(spec["fasteners"]), "fasteners")


def _root(parts, q):
    by = {x["id"]: x for x in parts}
    while q.get("parent"):
        q = by[q["parent"]]
    return q["id"]
