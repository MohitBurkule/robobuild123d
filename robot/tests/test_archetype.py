"""Archetype rules: every rule id fails on a bad fact set and passes on a good one; plus geometry on small specs."""

import numpy as np
import pytest

from robot import spec
from robot.checks import Options, verify
from robot.checks.archetype import ARCHETYPES, COMMON, RULES, params_for

GOOD = {
    "axis": np.array([1.0, 0, 0]), "rotor_joint": (True, "ok"), "rotor_fasteners": [], "supports": (True, True),
    "wedgelets": (True, True), "blade_lead_mm": 8.0, "disc_floor_gap_mm": 2.0, "weapon_drive": "inside_hub",
    "disc_material": ("metal", "laser", "titanium"), "teeth": 1, "weapon_mass_fraction": 0.3, "energy_j_per_kg": 150.0,
    "drive": (4, 4, None), "invert": (False, 2.0), "top_slope_deg": 22.0, "pods_missing": [], "floor": (1.0, 3.0),
    "lid_bad": [], "switch_access": "side", "wedge_floor_gap_mm": 0.5, "wedge_angle_deg": 20.0, "wedge_width_frac": 0.95,
    "weapon_lead_mm": 6.0, "drum_width_frac": 0.5, "arm": ("arm", "servo", 180.0), "axle_height_mm": 30.0,
    "disc_thickness_mm": 16.0, "disc_dia_mm": 54.0, "tub_height_mm": 22.0, "wheel_dia_mm": 29.0, "wheel_count": 4.0,
}
TARGETS = {"axle_height_mm": (28, 32), "disc_thickness_mm": (15, 18), "disc_dia_mm": (50, 56), "tub_height_mm": (20, 24),
           "wheel_dia_mm": (28, 30), "wheels": (4, 4)}
BAD = {
    "disc_plane_vertical": {"axis": np.array([0, 0, 1.0])},
    "disc_plane_horizontal": {"axis": np.array([1.0, 0, 0])},
    "axle_lateral": {"axis": np.array([0, 1.0, 0])},
    "rotor_joint": {"rotor_joint": (False, "no joint")},
    "rotor_fasteners": {"rotor_fasteners": ["`s1` joins disc to fork"]},
    "disc_supported": {"supports": (True, False)},
    "wedgelets_flank": {"wedgelets": (True, False)},
    "blade_lead": {"blade_lead_mm": -3.0},
    "disc_floor_gap": {"disc_floor_gap_mm": 9.0},
    "weapon_drive": {"weapon_drive": "unconnected"},
    "disc_material": {"disc_material": ("printed", "fdm", "pla")},
    "teeth": {"teeth": 0},
    "weapon_mass_fraction": {"weapon_mass_fraction": 0.08},
    "energy_ratio": {"energy_j_per_kg": 5.0},
    "drive_config": {"drive": (3, 1, None)},
    "invertible": {"invert": (False, -10.0)},
    "top_armour_slope": {"top_slope_deg": 0.0},
    "pods_enclose_wheels": {"pods_missing": ["wheel_fl"]},
    "floor_ribs": {"floor": (1.0, 0.0)},
    "lid_inserts": {"lid_bad": ["bolt_t0"]},
    "switch_access": {"switch_access": "none"},
    "wedge_floor_gap": {"wedge_floor_gap_mm": 5.0},
    "wedge_angle": {"wedge_angle_deg": 60.0},
    "wedge_width": {"wedge_width_frac": 0.4},
    "weapon_leads": {"weapon_lead_mm": -5.0},
    "drum_width": {"drum_width_frac": 0.1},
    "arm_actuated": {"arm": ("arm", None, 180.0)},
    "arm_range": {"arm": ("arm", "servo", 10.0)},
    "axle_height": {"axle_height_mm": 45.0},
    "disc_thickness": {"disc_thickness_mm": 3.0},
    "disc_diameter": {"disc_dia_mm": 80.0},
    "tub_height": {"tub_height_mm": 39.0},
    "wheel_dia": {"wheel_dia_mm": 20.0},
    "wheel_count": {"wheel_count": 2.0},
}


def _params(rid):
    for name, (rules, _) in ARCHETYPES.items():
        if rid in rules:
            _, P = params_for(name, TARGETS)
            return P
    raise AssertionError(rid)


def test_every_rule_has_a_bad_case_and_belongs_to_an_archetype():
    assert set(BAD) == set(RULES)
    used = {r for rules, _ in ARCHETYPES.values() for r in rules}
    assert used == set(RULES)


@pytest.mark.parametrize("rid", sorted(RULES))
def test_rule_good_passes_bad_fails_missing_unknown(rid):
    fn, P = RULES[rid][3], _params(rid)
    good = dict(GOOD)
    if rid == "disc_plane_horizontal":
        good["axis"] = np.array([0, 0, 1.0])
    passed, msg = fn(good, P)
    assert passed is True or (not isinstance(passed, str) and bool(passed)), (rid, msg)
    bad = dict(GOOD, **BAD[rid])
    passed, msg = fn(bad, P)
    assert passed is not None and (isinstance(passed, str) or not bool(passed)), (rid, msg)
    key = next(iter(BAD[rid]))
    passed, _ = fn({k: v for k, v in GOOD.items() if k != key}, P)
    assert passed is None or (rid in ("axle_height", "disc_thickness", "disc_diameter", "tub_height", "wheel_dia", "wheel_count")
                              and passed is None)


def test_param_rules_skip_without_target():
    assert RULES["axle_height"][3](GOOD, dict(COMMON))[0] is True


def test_switch_top_only_is_a_warning():
    assert RULES["switch_access"][3](dict(GOOD, switch_access="top"), dict(COMMON))[0] == "warn"


def test_two_wd_needs_wedge_contact():
    _, P = params_for("wedge_2wd")
    assert RULES["drive_config"][3](dict(GOOD, drive=(2, 2, 0.5)), P)[0]
    assert not RULES["drive_config"][3](dict(GOOD, drive=(2, 2, 5.0)), P)[0]


# ---------------------------------------------------------------- geometry on a small vertical spinner


def box(x, y, z):
    return {"type": "box", "size": [x, y, z]}


def _vs(joint=True, screw_into_fork=False, archetype="vertical_spinner_forks"):
    disc_shape = {"type": "union", "items": [{"type": "cylinder", "radius": 22, "height": 16},
                                             {"type": "place", "shape": box(8, 8, 16), "at": [24, 0, 0], "rot": [0, 0, 0]}]}
    parts = [
        {"id": "tub", "kind": "structure", "material": "nylon", "process": "fdm", "shape": box(70, 70, 20), "at": [0, 0, 10]},
        {"id": "fork_l", "kind": "structure", "material": "nylon", "process": "fdm", "shape": box(6, 30, 40), "at": [-14, 45, 25]},
        {"id": "fork_r", "kind": "structure", "material": "nylon", "process": "fdm", "shape": box(6, 30, 40), "at": [14, 45, 25]},
        {"id": "shaft", "kind": "shaft", "material": "steel", "shape": {"type": "cylinder", "radius": 2, "height": 34},
         "at": [0, 55, 26], "rot": [0, 90, 0]},
        {"id": "disc", "kind": "weapon", "material": "titanium", "process": "laser", "shape": disc_shape, "at": [0, 55, 26],
         "rot": [0, 90, 0], "parent": "fork_l" if not joint else None,
         "weapon": {"kind": "disc", "motor": None, "spin_axis": [0, 0, 1]},
         **({"joint": {"kind": "revolute", "axis": [1, 0, 0], "pivot": [0, 55, 26], "min": -180, "max": 180}} if joint else {})},
    ]
    fasteners = [{"id": "s1", "designation": "M2x6", "at": [0, 55, 40], "dir": [0, 0, -1], "through": ["disc"],
                  "threads_into": "fork_l" if screw_into_fork else "disc", "removable": True}]
    d = {"name": "vs", "robot_type": "vertical_spinner", "archetype": archetype, "parts": parts, "fasteners": fasteners,
         "electronics": {"failsafe": True}}
    rep = verify(spec.Spec(d), Options(only=["archetype"], deep=False, fast=True))
    return {f.id: f for f in rep.findings if f.group in ("archetype", "checks")}, rep


def test_spinner_geometry_good():
    f, _ = _vs()
    assert f["archetype.rotor_joint"].passed, f["archetype.rotor_joint"].message
    assert f["archetype.rotor_fasteners"].passed
    assert f["archetype.disc_supported"].passed
    assert f["archetype.disc_plane_vertical"].passed and f["archetype.axle_lateral"].passed
    assert f["archetype.disc_material"].passed
    assert f["archetype.teeth"].passed, f["archetype.teeth"].message


def test_spinner_geometry_bad_rigid_disc_and_screw_into_fork():
    f, rep = _vs(joint=False, screw_into_fork=True)
    assert f["archetype.rotor_joint"].severity == "blocker" and not f["archetype.rotor_joint"].passed
    assert not f["archetype.rotor_fasteners"].passed
    # no weapon motor and no wheels: fail closed, listed under NOT CHECKED
    assert not f["archetype.weapon_drive"].passed and any("weapon_drive" in x for x in rep.not_checked)


def test_unknown_archetype_blocks():
    f, _ = _vs(archetype="toaster")
    assert f["archetype.unknown"].severity == "blocker"


def test_no_archetype_no_findings():
    rep = verify(spec.Spec({"name": "x", "parts": [{"id": "a", "kind": "structure", "material": "pla", "shape": box(10, 10, 10)}]}),
                 Options(only=["archetype"], deep=False, fast=True))
    assert not [f for f in rep.findings if f.group == "archetype"]


def test_rotor_fasteners_sweep_uses_rotor_axial_extent():
    # an off-centre rotor (disc hub one side of the pivot, as revron's spider at x -9.7..-6.7 with discs to 5.3):
    # a static bolt beside the rotor but within |x| < weapon half width of the pivot is not in the swept volume
    def run(bx):
        d = {"name": "vs", "robot_type": "vertical_spinner", "archetype": "vertical_spinner_forks", "electronics": {"failsafe": True},
             "parts": [
                 {"id": "tub", "kind": "structure", "material": "nylon", "process": "fdm", "shape": box(70, 70, 20), "at": [0, 0, 10]},
                 {"id": "fork_r", "kind": "structure", "material": "nylon", "process": "fdm", "shape": box(6, 30, 40), "at": [14, 45, 25]},
                 {"id": "disc", "kind": "weapon", "material": "titanium", "process": "laser", "at": [0, 55, 26], "rot": [0, 90, 0],
                  "shape": {"type": "place", "shape": {"type": "cylinder", "radius": 22, "height": 16}, "at": [0, 0, -10], "rot": [0, 0, 0]},
                  "weapon": {"kind": "disc", "motor": None, "spin_axis": [0, 0, 1]},
                  "joint": {"kind": "revolute", "axis": [1, 0, 0], "pivot": [0, 55, 26], "min": -180, "max": 180}}],
             "fasteners": [{"id": "s1", "designation": "M2x6", "at": [bx, 55, 36], "dir": [1, 0, 0], "threads_into": "fork_r",
                            "removable": True}]}
        rep = verify(spec.Spec(d), Options(only=["archetype"], deep=False, fast=True))
        return {f.id: f for f in rep.findings}["archetype.rotor_fasteners"]
    assert run(5).passed            # disc spans x -18..-2: the bolt at x 5..11 is beside it
    assert not run(-12).passed      # inside the disc slab
