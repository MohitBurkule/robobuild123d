"""Revron params: robot-level declarations: archetype, targets, claims, teardown. Re-exported by params.py."""
from .params_hardware import *  # noqa: F401,F403

# robot-level declarations (data tables, not geometry): archetype ranges, targets, claims, allowed overlaps
ARCHETYPE_PARAMS = {"blade_lead_mm": [-30, -10], "axle_height_mm": [22, 25], "disc_thickness_mm": [14, 16], "disc_dia_mm": [44, 48], "teeth": [1, 1],
                    "tub_height_mm": [15, 19], "wheels": [4, 4], "wheel_dia_mm": [10, 23], "weapon_mass_fraction": [0.18, 0.5], "top_slope_deg": [-5, 25],
                    "disc_floor_gap_mm": [5.0, 9.0]}   # STEP: R16.5 drisk on the 23.5 axle sweeps ~7 mm up; the forks and wedgelets work the floor, not the disc
TARGETS = {"length_mm": 107, "width_mm": 104.1, "disc_dia_mm": 46, "wheel_dia_mm": 21.5, "tol_mm": 3,
           "source": "RVRN 2.0 STEP (research/rvrn_step) measured in its assembly frame",
           "note": "GR1507 drisk (single tooth, 3+6+3 on a 3 mm spider) on 8 mm XALT mounts; N10 direct to 21.5 rear tyres, O-rings to 11 mm fronts"}
WEAPON_LOCK = {"type": "external_pin", "note": "pit safety pin handled outside the robot and pulled before a fight: not part of the build, no bore in RV02/RV03 (the STEP has none; user 2026-10-19)"}
REFERENCE_DOC = {"path": "REFERENCE.md", "must_mention": ["GR1507", "180 mAh", "Hardox", "JST RCY", "RV00", "XALT", "0.9 mm"],
                 "must_not_mention": ["through an aluminium spider", "2S ≈350 mAh LiPo"]}
ELECTRONICS = dict(failsafe=True, weapon_remote_disable=True, radio="2.4 GHz", cells=2)
MASS_LIMIT_G, SQUARE_MM = 150, 150      # AWS 2025 antweight limits
CLAIMS = [dict(id="c_mass", text=f"weighs {MASS_LIMIT_G} g or less", metric="mass_total_g", op="<=", value=MASS_LIMIT_G),
          dict(id="c_fit", text=f"fits the {SQUARE_MM} mm square", metric="footprint_mm", op="<=", value=SQUARE_MM)]
SHARP_OK = [dict(part="tub", near=[sg * 31.4, -11.7, 5.4], r_mm=1.0, reason="inside corner of the lobe-tail step is the side panel's own square relief edge (STEP RV23 diamond): the TPU panel conforms, rounding it in the tub would leave a 0.07 mm sliver") for sg in (1, -1)] + [dict(part="base_panel", near=[27.9, -21.5, 4.5], r_mm=3.0,
                 reason="screw boss is 0.3 mm tall (any taller breaks the reference silhouette), so its base fillet is capped at R0.25; the STEP pad base is R0.5")]
_ORING = "O-ring is rubber: it squashes 0.16 mm against the plain inner face of the STEP side panel (the STEP has no belt channel)"
_N10_FLAT = "the catalog N10 shaft is drawn round; the hub's D-flat sits on its flat"
ALLOW_OVERLAP = [dict(a="belt_l", b="side_l", max_depth_mm=0.3, reason=_ORING),
                 dict(a="belt_r", b="side_r", max_depth_mm=0.3, reason=_ORING),
                 dict(a="wshaft", b="wbearing", max_depth_mm=0.3, reason="shaft in the MR85 inner race (bearing modelled as one solid)"),
                 dict(a="wshaft", b="weapon_motor_can", max_depth_mm=2.6, reason="wshaft is the GR1507's own shaft, already drawn inside the catalog motor envelope"),
                 dict(a="motor_l", b="whub_rl", max_depth_mm=0.4, reason=_N10_FLAT),
                 dict(a="motor_r", b="whub_rr", max_depth_mm=0.4, reason=_N10_FLAT),
                 *[dict(a=f"insert_b{i}", b="tub", max_depth_mm=0.2, reason="heat-set insert: 3.5 OD melted into a 3.4 bore (interference by design)") for i in range(len(INS))],
                 *[dict(a=f"insert_{k}", b="tub", max_depth_mm=0.2, reason="heat-set insert: 3.5 / 3.2 OD melted into a 3.4 / 3.1 bore (interference by design)") for k in ("t0", "t1", "t2", "t3")],
                 *[dict(a=f"nut_c{n}", b="tub", max_depth_mm=0.1, reason="thin M3 nut pressed into a hex pocket 0.05 under its flats (captive)") for n in "lr"],
                 dict(a="wbearing", b="mount_l", max_depth_mm=0.1, reason="MR85 8.0 OD pressed into the RV02 7.9 printed seat (0.05 radial interference, the STEP seat size)")]
MODULE_NOTE = "RVRN quick change: 4 M3 out, both mounts with the drisk lift off the chassis tabs"


# real service order (Build Guide): side screws out, side panels off, then each wedgelet comes off its standoffs
# outward together with the fork whose tail sits in its cheek slot; then the standoffs slide out of the lugs.
TEARDOWN = [t for s, n in ((-1, "l"), (1, "r")) for t in (
    dict(parts=[f"wedgelet_{n}", f"fork_{n}"], dir=[s, 0, 0], reason="fork tail is pinned in the wedgelet cheek slot: they slide off the standoffs as one"),
    dict(parts=[f"so_b{n}"], dir=[s, 0, 0], reason="nose standoff slides out of the chassis lug once the mount screw is out"),
    dict(parts=[f"so_a{n}"], dir=[s, 0, 0], reason="axle standoff slides out of the lug with the front hub and wheel on it"))] + [
    # weapon module (fix-B): with both standoff pairs and the front end out, the module (both mounts, motor, drisk, lock)
    # slides forward off the chassis tabs as one unit (the tub's side lugs close the other five ways)
    dict(parts=["mount_r"], dir=[0, 1, 0], reason="RV02/RV03 with the motor and drisk slide forward off the chassis tabs as one quick-change module")]

# bench teardown of the module with RV03 held: RV02 off the shaft end, drisk off the shaft, motor off its 4 stator screws
MODULE_TEARDOWN = [
    dict(parts=["mount_l", "bolt_ula", "bolt_ulb"], dir=[-1, 0, 0], reason="RV02 slides outboard off the shaft end, its CSK screws captive"),
    dict(parts=["spider"], dir=[-1, 0, 0], reason="drisk (spider, discs, spacer, stack bolts) slides off the GR1507 shaft once the 4 bell screws are out"),
    dict(parts=["weapon_motor_stator"], dir=[-1, 0, 0], reason="GR1507 leaves inboard-left once the 4 stator screws are out")]


# the drisk is turned by hand before the nose screws (bolt_u?b) are drawn: in the STEP pose the eccentric rim and tooth flank
# pass within 2.1 mm of their line (heads r3.0); 160 deg about the axis puts the rim 3.07 mm off it, so the screws leave inward
SERVICE_TURN_DEG = 160.0
SERVICE_POSE = [dict(parts=["spider", "disc_a", "disc_b", "dspacer"] + [f"bolt_{c}{k}" for c in "pd" for k in range(N_STACK)],
                     axis_at=[0.0, WY, WZ], axis_dir=[1, 0, 0], deg=SERVICE_TURN_DEG,
                     reason="drisk turned by hand so the rim clears the nose screws; whole stack with its bolts moves as one")]

UNIT = 1          # unit direction-cosine norm (k^2 + h^2 = UNIT) for the belt tangent construction
BELT_DIGITS = 4   # decimals kept on belt path points in the spec
__all__ = [n for n in dir() if not n.startswith("__")]   # last line: every name above is exported
