"""Revron params: fasteners, wiring, electronics, reference BOM and check tolerances. Re-exported by params.py."""
from .params_side import *  # noqa: F401,F403
from . import hw


# ====================================================================================================================
# Spec
# ====================================================================================================================
SOLID = dict(tub=0.8, mount=0.85, hub=0.85, tpu=0.9, shaft=0.05)    # solid_fraction of printed parts (infill and shell mass share)
WEDGE_REF = {-1: "RV17", 1: "RV18"}                      # STEP part ids of the wedgelets and side panels per side
SIDE_REF = {-1: "RV23", 1: "RV24"}
SIDE_BOLT_X = dict(a=46.26, b=41.76, c=35.26)            # |X| of the side-panel screw heads (STEP: seated in a bore below the face; axle standoff, nose standoff, chassis nut)
SIDE_SINK = dict(a=2.15, b=5.75, c=1.05)                 # depth of each screw head below the battered outer face, measured on the STEP side panels RV23 (LH) / RV24 (RH): outer face |X| 48.41 / 47.51 / 36.31 at the screw axes, minus the head planes above
SIDE_FACE_X = {k: SIDE_BOLT_X[k] + SIDE_SINK[k] for k in SIDE_BOLT_X}   # |X| of the battered outer face at each screw
SIDE_PROBE_R, SIDE_PROBE_N = 3.9, 12                      # the ring round a screw axis on which the outer face is read (head radius + 0.8, 12 points)
SIDE_PROBE_OFF = dict(a=0.136, b=0.051, c=0.061)   # table - probe at the default standoffs
assert all(0 < d <= SP_CSK["head_clear"] for d in SIDE_SINK.values()), "a screw head must sit inside its driver bore (sink <= bore depth)"
SIDE_BOLT_DES = dict(a="M3x10", b="M3x10", c="M3x8")
BASE_HEAD_PROUD = 0.6                                     # STEP RV26: the seat (dk 3.2, 0.5 deep) cannot take the ISO head, so the head plane stays this far outside the panel outer face (head proud)
BASE_BOLT_Z = round(BASE_Z0 - (0.0 if variant("base_csk_fit") else BASE_HEAD_PROUD), 6)   # base-panel screw head plane: flush with the outer face once the variant opens the seat to the head
TOP_BOLT_XY = INS[1::-1] + INS[3:1:-1]                   # top-panel screws sit on the four corner columns, right-hand first
PCT = 100                                                # percent
AWG = dict(power=24, rx=26, motor=28, signal=30)
SLACK = dict(short=6, bench=8, phases=15)                # wire slack allowed, mm
# (id, from, to, awg, kind, slack, extras)
LEAD_TAPE_WHY = "INFERRED, not in the STEP (it has no wires): the original has no lead channel, so the 3 phase leads are taped flat along the RV03 lug; the optional lead groove (REVRON_LEAD_GROOVE=on) replaces the tape"
LEAD_TAPE = dict(exposed_reason=LEAD_TAPE_WHY)
WIRES = [("w_bat_sw", "battery.jst_rcy", "power_switch.in", AWG["power"], "power", SLACK["bench"], dict(connector="jst_rcy")),
         ("w_sw_wesc", "power_switch.out", "wesc.bat", AWG["power"], "power", SLACK["bench"], {}),
         ("w_sw_rx", "power_switch.out", "rxesc.bat", AWG["rx"], "power", SLACK["bench"], {}),
         # phases run rearward in the gap behind the drisk (4 mm axial from the stack), over the front lug (its top is the deck) and down into the tub at the deck front
         ("w_wesc_m", "wesc.motor", "weapon_motor_stator.phases", AWG["power"], "motor", SLACK["phases"], dict(connector="bullet2", count=3, via=PHASE_VIA, **({} if LEAD_GROOVE else LEAD_TAPE))),
         ("w_rx_wesc", "rxesc.wpn", "wesc.rx", AWG["signal"], "signal", SLACK["short"], {}),
         ("w_m_l", "rxesc.m2", "motor_l.terminals", AWG["motor"], "motor", SLACK["short"], {}),
         ("w_m_r", "rxesc.m1", "motor_r.terminals", AWG["motor"], "motor", SLACK["short"], {})]


# make_spec tables: weapon shaft, web floors, hub pivots, electronics placements, press-fit interference, belt geometry
WEB = dict(spider=0.8, disc=0.9, fork=1.05)             # min_web_mm the designer owns (STEP measures the same webs)
HUB_SPIN_DEG = 2.45                                   # rear hubs sit this far round the D-shaft (STEP: the D-bore flat, nut slot and grub are turned 2.45 deg; the Distance/Concentric mates leave the spin free)
HUB_PIVOT_X = dict(rear=41.6, front=34.5)               # |X| of each hub's revolute pivot
# BATTERY (RV16 pack catalog id) comes from params_chassis: the front wall follows the pack length
BAT_L, BAT_W, BAT_H = hw.size(BATTERY)                    # catalog box (long side L): in the bay it is turned 90 about Z, so L runs along Y and W along X
BAT_BELOW = BAT_H / 2                                     # catalog origin -> pack underside (STEP pack 11 thick, z 6.5..17.5 about origin z 12)
BAT_STOP_GAP = 0.0                                        # pack rear face to the stop wall front face it butts (STEP: the RV16 pack touches the RV01 stop wall)
BAT_X = -11.81                                          # pack centre X (STEP envelope)
BAT_Y = round(KEY_SPAN[1] + BAT_STOP_GAP + BAT_L / 2, 6)  # pack centre Y: the pack stands against the stop wall, so a wider gearmotor (stop wall further forward) pushes it forward
BAT_Z = round(CH["deck"] - BAT_H / 2, 6)                # pack centre Z: the pack top rests against the deck underside (STEP pack 11 thick, z 6.5..17.5 about origin z 12), so a taller pack hangs lower; underside 2.0 over the base panel skin at the default (original: no pad, pack mated to the chassis only; foam pad = variant battery_pad)
ELEC = dict(battery=(BAT_X, BAT_Y, BAT_Z), rxesc=(8.67, -3.0, 15.3), wesc=(8.63, -7.25, 10.6), switch_yz=(-5.6, 14.25))   # catalog origins (STEP envelopes)
BAT_PAD_FRAC = 3                                         # the foam pad is this fraction of the pack footprint each way
_bx, _by = ELEC["battery"][:2]   # pack centre
BAT_PAD = dict(x=(_bx - BAT_W / BAT_PAD_FRAC / 2, _bx + BAT_W / BAT_PAD_FRAC / 2), y=(_by - BAT_L / BAT_PAD_FRAC / 2, _by + BAT_L / BAT_PAD_FRAC / 2))   # double-sided foam pad footprint under the pack, centred, base-panel skin top -> pack underside
FILLET_REAR_X = 26.77   # |X| where the squared N10 gearbox-plate seat meets its seat arc at the rear wall (measured on our section z=10; RV01 26.5)
SWX_DEV_R = 1.5   # reference_cad deviation radius round each switch pilot (hole shifted 0.45 from the STEP)
SW_PITCH, SW_BODY_H = 15.0, 3.5   # BBB ant switch ear-hole pitch and body height (catalog)
SW_SCREW_Y = tuple(round(ELEC["switch_yz"][0] + sg * SW_PITCH / 2, 6) for sg in (1, -1))   # the two ear holes straddle the switch centre
SW_BOLT_Z, TOP_BOLT_Z = ELEC["switch_yz"][1] + SW_BODY_H / 2, TOP_Z0 + TOP_T  # switch screws (Y, head Z) and the top-panel screw head plane
PRESS = dict(hub=0.05, tyre=0.3, micro=0.2, nut=0.05, shaft=0.02, bearing=BRG_PRESS, pack=0.1)   # press-fit interference per joint, mm
BELT_R, BELT_r = 7.95, 4.2   # O-ring centreline radii: rear / front hub groove floor (7.45, 3.7) + half the 1.0 cs
BELT_X = dict(centre=31.25)                                              # |X| of the O-ring centreline (hub groove centre)
O_RING = (45, 1.0)                                      # stock O-ring ID x cross-section


# intent-probe parameters (rear hub / tyre / nut / seat) and the TPU-print exceptions of the chassis wall
HUB_PROBE_X = 35.0                                      # |X| of the keyed-bore probe point (inside the bore, off its centre line)
HUB_BORE_SPAN, TYRE_SPAN = (30.5, 40.5), (32.5, 42.0)   # |X| of the hub's blind D-bore and of the tyre seat
TYRE_ID, TYRE_STRETCH, NUT_MOVE, WHEEL_MIN_GAP = 13.0, 1.0, 0.3, 1.0   # relaxed F1 tyre ID, its stretch over the crown, nut play, wheel-to-armour gap
SEAT_PLAY, SEAT_TURN_DEG = 0.15, 2.0                      # motor boss play in the keyhole, shaft turn it allows
WALL_MIN = 1.8                                            # printed wall floor: 4+ perimeters on a 2 mm wall
WALL_EXCEPT = [[[-29.6, -37.7, 4.6], [29.6, -35.4, 17.5]], [[-33.0, -38.0, 0.0], [33.0, 44.0, 4.6]], [[-33.0, 41.5, 4.6], [33.0, 44.0, 7.0]],
               [[-33.0, -15.0, 4.6], [-31.0, NUT_RELIEF_END_Y + 2.0, 15.0]], [[31.0, -15.0, 4.6], [33.0, NUT_RELIEF_END_Y + 2.0, 15.0]]]   # rear truss, base lip and the +Y flange foot (1.7 mm over the lattice, same in the STEP RV01) and the lobe tail where the nut relief ends (STEP RV01)
FILLET_H, ROTOR_CLEAR = 10.0, 2.0                         # inside-corner fillet probe height; lead-to-rotor clearance




REF_BOM = [   # RVRN 2.0 STEP part list (research/rvrn_step/INDEX.txt); one row per joint or part family
    dict(role="FS8: base panel 5 x M2 CSK into heat-sets", match=["bolt_b*"], count=5, designation="M2x6", head="countersunk", threads_into="insert"),
    *([dict(role="top panel: 4 x M2 thread-forming (not in the STEP; its d2.8 holes over the corner columns are)", match=["bolt_t*"], count=4, designation="M2x6", threads_into="tub",
         deviation="the STEP top panel has 4 countersunk corner holes over the corner columns' d3 bores but no screws; 4 M2x6 added, tapping a 1.7 pilot in a 5 mm web left under the column rim, so the Ti panel cannot peel off")] if TOP_SCREW_WEB else []),
    dict(role="FS1 M2 heat-sets (floor)", kind="part", match=["insert_b*"], count=5, catalog=INSERT_CAT),
    dict(role="FS9: mount to standoff 2 x M3x12 CSK alu (axle standoff)", match=["bolt_u?a"], count=2, designation="M3x12", head="countersunk", threads_into="standoff", material="aluminium"),
    dict(role="FS9: mount to nose standoff 2 x M3 CSK alu", match=["bolt_u?b"], count=2, designation="M3x14", head="countersunk", threads_into="standoff", material="aluminium",
         deviation="M3x14 instead of the STEP's M3x12: through mount and lug, 12 mm engages 3.9 mm of the 15 mm standoff (< 1.5 d)"),
    dict(role="side panel to standoff ends: 4 x M3 CSK (STEP M3x8)", match=["bolt_s?a", "bolt_s?b"], count=4, designation="M3x10", head="countersunk", threads_into="standoff",
         deviation="M3x10 instead of the STEP's M3x8: 8 mm engages 4.2 / 2.7 mm of standoff thread, under 1.5 d in aluminium"),
    dict(role="side panel to chassis: 2 x M3x8 CSK into thin nuts", match=["bolt_s?c"], count=2, designation="M3x8", head="countersunk", threads_into="nut"),
    dict(role="M3 thin nuts (BS EN 24036)", kind="part", match=["nut_c*"], count=2, catalog="nut_m3_thin"),
    dict(role="RV11 25 mm + RV10 15 mm alu standoffs", kind="part", match=["so_*"], count=4, material="aluminium"),
    dict(role="GR1507 weapon motor", kind="part", match=["weapon_motor_stator"], count=1, catalog=MOTOR["stator"]),
    dict(role="GR1507 bell (rotor half)", kind="part", match=["weapon_motor_can"], count=1, catalog=MOTOR["can"]),
    dict(role="Motor back spacer", kind="part", match=["motor_spacer"], count=1),
    dict(role="spider + 2 Drisk_floating_3 + Drisk_spacer_alt_x", kind="part", match=["spider", "disc_a", "disc_b", "dspacer"], count=4),
    dict(role="fork_5 x 2", kind="part", match=["fork_*"], count=2),
    dict(role="RV17/18 wedgelets", kind="part", match=["wedgelet_*"], count=2, material="tpu"),
    dict(role="RV23/24 side panels", kind="part", match=["side_*"], count=2, material="tpu"),
    dict(role="Top panel 0.9 sheet", kind="part", match=["top_panel"], count=1),
    dict(role="RV15 BBB antweight switch", kind="part", match=["power_switch"], count=1, catalog="switch_bbb_ant_rvrn2"),
    dict(role="RV16 Turnabot 2S 180 mAh", kind="part", match=["battery"], count=1, catalog=BATTERY),
    dict(role="RV13 Malenki nano", kind="part", match=["rxesc"], count=1, catalog=RXESC),
    dict(role="RV14 brushless ESC", kind="part", match=["wesc"], count=1, catalog=WESC),
    dict(role="RV12 N10 2200 rpm x 2", kind="part", match=["motor_l", "motor_r"], count=2, catalog=DRIVE_MOTOR),
    dict(role="drisk stack: 4 x M2 into the spider (not in the STEP, holes are)", match=["bolt_d*"], count=4, designation="M2", threads_into="spider",
         deviation="the STEP leaves the r14 stack holes empty; 4 M2x14 added from the back, tapped into the spider (r0.8 tap holes there, the STEP r1.1 clearance elsewhere): no nuts, nothing invented beyond the screws"),
    dict(role="spider to bell: 4 x M2 (not in the STEP)", match=["bolt_p*"], count=4, designation="M2", threads_into="motor",
         deviation="the STEP shows the r4.5 holes only"),
    dict(role="stator: 4 x M2 (not in the STEP)", match=["bolt_wm*"], count=4, designation="M2", threads_into="motor",
         deviation="the STEP shows the RV03 counterbores only"),
    dict(role="switch: 2 x M2 into the deck pilot holes (not in the STEP)", match=["bolt_sw*"], count=2, designation="M2",
         deviation="the STEP has the two 1.7 pilot holes but no screws"),
    dict(role="nitrile O-ring belts (not in the STEP; hub grooves are)", kind="part", match=["belt_l", "belt_r"], count=2),
    dict(role="battery lead: JST RCY", kind="wire", match=["w_bat_sw"], count=1, connector="jst_rcy"),
    dict(role="weapon phases: 3 x 2 mm bullets", kind="wire", match=["w_wesc_m"], count=1, connector="bullet2"),
    dict(role="MR85ZZ bearing in the RV02 seat (outboard shaft support)", kind="part", match=["wbearing"], count=1,
         deviation="added: bought part left out of the STEP (INDEX.txt lists no bearing), but RV02 carries the 7.9 mm printed seat and the guide BOM lists an MR85ZZ"),
    dict(role="GR1507 5 mm threaded shaft", kind="part", match=["wshaft"], count=1,
         deviation="added: the shaft belongs to the bought GR1507, which the STEP draws as one body (INDEX.txt lists no shaft); drawn apart for the MR85 support and the spider collar, its mass stays in the motor"),
]
# REF_BOM extras that exist only when the named variant (variants.py) is on: spec.ref_bom() appends them
REF_BOM_VARIANT = {
    "battery_pad": [
    dict(role="bat_pad: double-sided foam tape pad under the pack (not in the STEP)", kind="part", match=["bat_pad"], count=1, material="foam_tape",
         deviation="the STEP pack floats 2 mm over the base panel; a foam tape pad supports and retains it (adds ~0.05 g, reversible)",
         reason="the STEP pack floats 2 mm over the base panel; a foam tape pad supports and retains it (adds ~0.05 g, reversible)"),
    ],
    "esc_tray": [
    dict(role="esc_tray: TPU weapon-ESC tray (not in the STEP)", kind="part", match=["esc_tray"], count=1, material="tpu",
         deviation="the STEP holds the weapon ESC with kapton tape alone; a TPU tray with 0.1 mm lips keeps the board in if the tape fails (adds 1.1 g, reversible)",
         reason="the STEP holds the weapon ESC with kapton tape alone; a TPU tray with 0.1 mm lips keeps the board in if the tape fails (adds 1.1 g, reversible)"),
    ],
}

REF_DIR = "/mnt/project-files/robot-cad/research/rvrn_step/parts"
DRISK_T = None


MICRO_T = {   # STEP Micro_slx_v1_0 instance placements (assembly frame), composed with REF_TO_WORLD
    "l": [[0, -0.33, 0.944, -30.5], [0, 0.944, 0.33, 5.5], [-1, 0, 0, 35.5], [0, 0, 0, 1]],
    "r": [[0, -0.33, -0.944, -30.5], [0, 0.944, -0.33, 5.5], [1, 0, 0, -35.5], [0, 0, 0, 1]],
}


TOE_DEV_YZ, TOE_DEV_R, TOE_DEV_X, TOE_DEV_MM3 = (49.3, 1.4), 3.0, (19.5, 36.5), 40.0   # knife-toe land: path capsule from the first to the last x   # mm3: land volume the STEP knife has over the printable land


# reference_cad tolerances and the reasoned-deviation sites (centres + radii of the regions allowed to differ from the STEP)
TOL = dict(tight=0.3, std=0.5, motor=0.6, wedge=0.8, loose=1.0)             # mm: surface deviation allowed per part class
VOL = dict(part=0.25, hub=0.15, motor=0.3, standoff=0.2, switch=0.5)          # fraction: volume mismatch allowed
REF_IOU_MIN = 0.9                                                              # silhouette IoU floor on every axis
FOOT_DEV_Z, FOOT_DEV_R = 5.0, 4.0       # tub corner column flared foot
KEYHOLE_DEV, KEYHOLE_DEV_R = (28.5, -30.5, 5.85), 5.0   # N10 keyhole U-slot: centre of its 2 x 4.1 x 6.7 cut, and the sphere that holds all of it
LOBE_DEV, LOBE_DEV_R = (32.0, -13.5, 9.4), 3.5  # param: organic centroid of the lobe-tail trim vs STEP blobs
# param: end
BASE_DEV_Z, PANEL_DEV_R, TOP_DEV_Z = 4.5, 3.5, 19.95
# Top Panel Cut-Extrude3 (RVRN 2.0 STEP Top_Panel_1, dumps_v2): 0.1 mm-deep engraved lettering, world x -17.75..18.81,
# y -8.68..-2.53, top face z 19.57; four r5 spheres along the text line cover it (laser-etched, not modelled)
TOP_TEXT_DEV_Z, TOP_TEXT_DEV_R = 19.57, 3.0   # path waiver radius (check cap 3)
TOP_TEXT_X, TOP_TEXT_Y, TOP_TEXT_MAX_MM3 = (-17.75, 18.81), (-7.1, -4.1), 20.0   # lettering span in X (y -8.68..-2.53), two capsule centre lines Y (r 3 each covers the edge strokes), volume cap per capsule
TOP_TEXT_DEV_XY = ((-3.78, -5.57), (-13.73, -5.62), (5.84, -5.26), (15.04, -5.66))
NOSE_DEV, NOSE_DEV_R = (MNT_IN + 2.0, SB[0] + 0.6, SB[1] - 1.7), 5.0             # mount nose pad (|x|, y, z): thickened nose wall, deviation from the STEP nose
STATOR_DEV_X, TAP_DEV_R = 16.8, 2.0                                              # stator lead-in cone site; tap-hole sites
STACK_TAP_DEV_R = 2.5   # spider stack-hole site: the whole STEP r1.1 hole wall over the 3 mm plate (half-diagonal 2.2) lies inside it
__all__ = [n for n in dir() if not n.startswith("__")]   # last line: every name above is exported
