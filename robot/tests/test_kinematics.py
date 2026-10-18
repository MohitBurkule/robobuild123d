"""Rotating parts and kinematic consistency: one good spinner and one good 2WD that pass, and a bad mutation per check id."""

import copy

import pytest

from robot import spec
from robot.checks import Options, verify

PLA = {"material": "pla", "process": "fdm"}
CYLX = [0, 90, 0]  # local Z (cylinder axis) -> world +X


def cyl(r, h):
    return {"type": "cylinder", "radius": r, "height": h}


def upright(x):
    return {"id": f"up{'l' if x > 0 else 'r'}", "kind": "structure", **PLA, "at": [x, 0, 25],
            "shape": {"type": "subtract", "base": {"type": "box", "size": [4, 50, 10]},
                      "cut": [{"type": "place", "rot": CYLX, "shape": cyl(4.5, 10)}]}}


def spinner():
    return {
        "name": "kin", "robot_type": "vertical_spinner",
        "parts": [
            {"id": "base", "kind": "structure", **PLA, "at": [0, 0, 2], "shape": {"type": "box", "size": [60, 60, 4]}},
            {"id": "post_l", "kind": "structure", **PLA, "at": [9, -20, 12], "shape": {"type": "box", "size": [4, 6, 16]}},
            upright(9), upright(-9),
            {"id": "disc", "kind": "weapon", "material": "steel", "at": [0, 0, 25], "rot": CYLX, "shape": cyl(20, 3),
             "joint": {"kind": "revolute", "axis": [1, 0, 0], "pivot": [0, 0, 25], "min": 0, "max": 360},
             "weapon": {"kind": "disc", "motor": "wm", "spin_axis": [0, 0, 1], "spin_dir": "ccw", "supported_both_ends": True}},
            {"id": "shaft", "kind": "shaft", "material": "steel", "parent": "disc", "at": [0, 0, 0], "shape": cyl(2, 24)},
            {"id": "brg_l", "kind": "bearing", "material": "steel", "at": [9, 0, 25], "rot": CYLX,
             "shape": {"type": "subtract", "base": cyl(4.5, 4), "cut": [cyl(2, 6)]}},
            {"id": "brg_r", "kind": "bearing", "material": "steel", "at": [-9, 0, 25], "rot": CYLX,
             "shape": {"type": "subtract", "base": cyl(4.5, 4), "cut": [cyl(2, 6)]}},
            {"id": "wm", "kind": "weapon_motor", "catalog": "bl_1806_2300kv", "at": [40, 0, 25], "rot": [0, 0, 180]},
        ],
        "connections": [
            {"a": "disc", "b": "shaft", "method": "press_fit", "reason": "disc keyed on the shaft, e-clips both sides", "mechanical_key": True},
            {"a": "brg_l", "b": "upl", "method": "press_fit", "reason": "bearing pressed in the upright pocket"},
            {"a": "brg_r", "b": "upr", "method": "press_fit", "reason": "bearing pressed in the upright pocket"},
            {"a": "brg_l", "b": "shaft", "method": "shaft", "reason": "inner race on shaft"},
            {"a": "brg_r", "b": "shaft", "method": "shaft", "reason": "inner race on shaft"},
            {"a": "wm", "b": "shaft", "method": "pin", "reason": "oldham flexible coupling, torque only"},
            {"a": "wm", "b": "base", "method": "screw", "reason": "stator mount on a printed boss"},
            {"a": "upl", "b": "base", "method": "screw", "reason": "upright"},
            {"a": "upr", "b": "base", "method": "screw", "reason": "upright"},
        ],
    }


def wheels():
    def wheel(s):
        return {"id": f"wheel_{s}", "kind": "wheel", "catalog": "wheel_28x10", "at": [s * 30, 0, 14]}

    def motor(s):
        return {"id": f"motor_{s}", "kind": "motor", "catalog": "n10_300rpm_6v", "at": [s * 15.5, 0, 14],
                "rot": [0, 0, 0 if s > 0 else 180]}
    d = {"name": "kin2", "robot_type": "wedge", "parts": [
        {"id": "base", "kind": "structure", **PLA, "at": [0, 0, 4], "shape": {"type": "box", "size": [14, 60, 4]}}],
        "connections": []}
    for s, n in ((1, "l"), (-1, "r")):
        w, m = wheel(s), motor(s)
        w["id"], m["id"] = f"wheel_{n}", f"motor_{n}"
        d["parts"] += [w, m]
        d["connections"] += [
            {"a": m["id"], "b": w["id"], "method": "press_fit", "reason": "D-bore on D-shaft", "mechanical_key": True},
            {"a": m["id"], "b": "base", "method": "glue", "reason": "motor glued in cradle"}]
    return d


def run(d):
    rep = verify(spec.Spec(d), Options(only=["mass", "power", "kinematics"], deep=False, fast=True))
    return rep, {f.id for f in rep.findings if f.group == "kinematics" and not f.passed}


def part(d, pid):
    return next(p for p in d["parts"] if p["id"] == pid)


def test_good_spinner_passes():
    rep, bad = run(spinner())
    assert bad == set(), [(f.id, f.message) for f in rep.findings if not f.passed]
    ids = {f.id for f in rep.findings if f.group == "kinematics"}
    for cid in ("kin.spin_joint", "kin.rigid_mix", "kin.sweep_static", "kin.bearing_races", "kin.joint_axis_bearing",
                "kin.joint_axis_shaft", "kin.bearing_count", "kin.torque_path", "kin.axial_retention", "kin.spin_dir",
                "kin.balance_static", "kin.fastener_boundary", "kin.motor_mount", "kin.double_bearing"):
        assert cid in ids


def test_good_wheels_pass():
    rep, bad = run(wheels())
    assert bad == set(), [(f.id, f.message) for f in rep.findings if not f.passed]


def m_nojoint(d):
    del part(d, "disc")["joint"]
    part(d, "shaft")["parent"] = None
    part(d, "shaft")["at"] = [0, 0, 25]
    part(d, "shaft")["rot"] = CYLX


def m_rigid(d):
    d["connections"].append({"a": "disc", "b": "upl", "method": "glue", "reason": "glued to the fork by mistake"})


def m_screw(d):
    d["fasteners"] = [{"id": "s1", "designation": "M2x20", "at": [-3, 12, 25], "dir": [1, 0, 0], "through": [],
                       "threads_into": "upl", "tool": "hex1.5"}]


def m_sweep(d):
    d["parts"].append({"id": "stud", "kind": "structure", **PLA, "at": [0, 15, 4 + 4], "shape": {"type": "box", "size": [6, 4, 8]}})


def m_onebearing(d):
    d["connections"] = [c for c in d["connections"] if "brg_r" not in (c["a"], c["b"])]
    d["parts"] = [p for p in d["parts"] if p["id"] != "brg_r"]


def m_bearing_off(d):
    part(d, "brg_l")["at"] = [9, 0.6, 25]


def m_static_bearing(d):
    for c in d["connections"]:
        if c["a"] == "brg_l" and c["b"] == "shaft":
            c["b"] = "base"


def m_undriven(d):
    d["connections"] = [c for c in d["connections"] if not (c["a"] == "wm" and c["b"] == "shaft")]


def m_friction(d):
    for c in d["connections"]:
        if c["a"] == "wm" and c["b"] == "shaft":
            c.update(method="press_fit", reason="pressed on, friction only")
        if c["a"] == "disc":
            c.update(mechanical_key=False, reason="press fit, e-clips both sides")


def m_spin_dir(d):
    part(d, "disc")["weapon"]["spin_dir"] = "cw"


def m_no_spin_dir(d):
    del part(d, "disc")["weapon"]["spin_dir"]


def m_unbalanced(d):
    part(d, "disc")["shape"] = {"type": "subtract", "base": cyl(20, 3), "cut": [{"type": "place", "at": [0, 12, 0], "shape": cyl(4, 6)}]}


def m_axis_type(d):
    part(d, "disc")["joint"]["axis"] = [0, 0, 1]
    part(d, "disc")["rot"] = [0, 0, 0]


def m_joint_spin(d):
    part(d, "disc")["joint"]["pivot"] = [0, 0, 25.5]


def m_double(d):
    for c in d["connections"]:
        if c["a"] == "wm" and c["b"] == "shaft":
            c["reason"] = "rigid dowels into the bell"


def m_motor_off(d):
    part(d, "wm")["at"] = [40, 1, 25]


def m_stator_static(d):
    d["connections"] = [c for c in d["connections"] if not (c["a"] == "wm" and c["b"] == "base")]
    part(d, "wm")["at"] = [60, 0, 60]


def m_child_static(d):
    d["parts"].append({"id": "esc", "kind": "esc", "catalog": None, **PLA, "parent": "disc", "at": [0, 0, 5],
                       "shape": {"type": "box", "size": [3, 3, 3]}})


def m_wire(d):
    d["wires"] = [{"id": "w1", "from": "disc.x", "to": "wm.phases", "kind": "motor"}]


def m_declared(d):
    part(d, "shaft")["rotates_with"] = "fixed"


def m_retention(d):
    for c in d["connections"]:
        c["reason"] = c["reason"].replace("e-clips both sides", "slid on")
    for u in ("upl", "upr"):
        part(d, u)["shape"]["cut"][0]["shape"]["radius"] = 6
    for b in ("brg_l", "brg_r"):
        part(d, b)["shape"]["base"]["radius"] = 4.5


def m_shaft_motor(d):
    part(d, "wm")["at"] = [24, 0, 25]


def m_prismatic(d):
    part(d, "disc")["joint"]["kind"] = "prismatic"


def m_lock(d):
    part(d, "disc")["weapon"]["locking_bar"] = "lock"
    d["parts"].append({"id": "lock", "kind": "locking_bar", "material": "steel", "at": [0, 0, 60], "shape": cyl(1, 4)})


CASES = [
    (m_nojoint, "kin.spin_joint"), (m_rigid, "kin.rigid_mix"), (m_screw, "kin.fastener_boundary"),
    (m_screw, "kin.fastener_undeclared"), (m_sweep, "kin.sweep_static"), (m_onebearing, "kin.bearing_count"),
    (m_bearing_off, "kin.joint_axis_bearing"), (m_static_bearing, "kin.bearing_races"), (m_undriven, "kin.torque_path"),
    (m_friction, "kin.torque_friction"), (m_spin_dir, "kin.spin_dir"), (m_no_spin_dir, "kin.spin_dir"),
    (m_unbalanced, "kin.balance_static"), (m_axis_type, "kin.weapon_axis_orientation"), (m_joint_spin, "kin.joint_axis_spin"),
    (m_double, "kin.double_bearing"), (m_motor_off, "kin.joint_axis_motor"), (m_stator_static, "kin.motor_mount"),
    (m_child_static, "kin.joint_child_static"), (m_wire, "kin.wire_to_rotor"), (m_declared, "kin.motion_declared"),
    (m_retention, "kin.axial_retention"), (m_shaft_motor, "kin.shaft_through_stator"), (m_prismatic, "kin.joint_kind"),
    (m_lock, "kin.lock_engages"),
]


@pytest.mark.parametrize("mut,cid", CASES, ids=[f"{m.__name__}-{c}" for m, c in CASES])
def test_spinner_mutation_fails(mut, cid):
    d = copy.deepcopy(spinner())
    mut(d)
    rep, bad = run(d)
    assert cid in bad, [(f.id, f.message) for f in rep.findings if not f.passed]


def w_toe(d):
    part(d, "wheel_l")["rot"] = [0, 0, 5]
    part(d, "motor_l")["rot"] = [0, 0, 5]


def w_undriven(d):
    d["connections"] = [c for c in d["connections"] if not (c["a"] == "motor_l" and c["b"] == "wheel_l")]
    part(d, "wheel_l")["at"] = [40, 0, 14]


def w_offshaft(d):
    part(d, "wheel_l")["at"] = [30, 1, 14]


def w_height(d):
    part(d, "wheel_r")["at"] = [-30, 0, 15]
    part(d, "motor_r")["at"] = [-15.5, 0, 15]


def w_rub(d):
    d["parts"].append({"id": "guard", "kind": "structure", **PLA, "at": [30, 0, 28.3], "shape": {"type": "box", "size": [8, 8, 0.4]}})


WCASES = [(w_toe, "kin.wheel_toe"), (w_toe, "kin.wheel_axes_parallel"), (w_undriven, "drive.coverage"),
          (w_offshaft, "kin.wheel_motor_coaxial"), (w_height, "kin.wheel_height"), (w_rub, "kin.rub_gap")]


@pytest.mark.parametrize("mut,cid", WCASES, ids=[f"{m.__name__}-{c}" for m, c in WCASES])
def test_wheel_mutation_fails(mut, cid):
    d = copy.deepcopy(wheels())
    mut(d)
    rep, bad = run(d)
    assert cid in bad, [(f.id, f.message) for f in rep.findings if not f.passed]


def test_dead_wheel_declared_passes():
    d = wheels()
    w_undriven(d)
    part(d, "wheel_l")["driven"] = False
    d["connections"].append({"a": "wheel_l", "b": "base", "method": "none", "reason": "dead wheel test"})
    rep, bad = run(d)
    assert "drive.coverage" not in bad


def test_belt_misaligned():
    d = wheels()
    for s, n in ((1, "a"), (1, "b")):
        pass
    d["parts"] += [
        {"id": "pul_a", "kind": "pulley", **PLA, "at": [36, 0, 14], "rot": CYLX, "shape": cyl(5, 2)},
        {"id": "wheel_b", "kind": "wheel", "catalog": "wheel_28x10", "at": [30, -40, 14]},
        {"id": "pul_b", "kind": "pulley", **PLA, "at": [38, -40, 14], "rot": CYLX, "shape": cyl(5, 2)},
        {"id": "belt", "kind": "belt", **PLA, "at": [37, -20, 14], "shape": {"type": "box", "size": [1, 1, 1]},
         "belt": {"pulleys": ["pul_a", "pul_b"], "kind": "o_ring", "length_mm": 100}},
    ]
    d["connections"] += [{"a": "pul_a", "b": "wheel_l", "method": "glue", "reason": "pulley glued to wheel"},
                         {"a": "pul_b", "b": "wheel_b", "method": "glue", "reason": "pulley glued to wheel"}]
    rep, bad = run(d)
    assert "kin.belt_coplanar" in bad
    assert "drive.coverage" not in bad


# ---------------------------------------------------------------- more ids (one bad mutation each; good = the bases above)
import math as _m


def saw(mirror=False):
    pts = []
    for t in range(3):
        for i in range(24):
            f = i / 24
            th = 2 * _m.pi * (t + f) / 3
            r = 16 + 4 * f
            pts.append([r * _m.cos(th), r * _m.sin(th)])
    if mirror:
        pts = [[x, -y] for x, y in reversed(pts)]
    return {"type": "prism", "height": 3, "points": pts}


def m2_sweep_fastener(d):
    d["fasteners"] = [{"id": "f1", "designation": "M2x10", "at": [3, 10, 12], "dir": [0, 0, -1], "through": ["base"], "tool": "hex1.5"}]
    d["parts"].append({"id": "pad", "kind": "structure", **PLA, "at": [3, 10, 12.5], "shape": {"type": "box", "size": [5, 5, 1]}})


def m2_bell_rub(d):
    d["parts"].append({"id": "lug", "kind": "structure", **PLA, "at": [40, 0, 35.3], "shape": {"type": "box", "size": [4, 4, 1]}})


def m2_motor_face(d):
    d["fasteners"] = [{"id": "f2", "designation": "M2x8", "at": [38, 0, 40], "dir": [0, 0, -1], "through": ["base"],
                       "threads_into": "wm", "tool": "hex1.5"}]


def m2_bearing_seat(d):
    for c in d["connections"]:
        if c["a"] == "brg_l" and c["b"] == "upl":
            c["b"] = "post_l"


def m2_shaft_short(d):
    part(d, "shaft")["shape"] = cyl(2, 10)


def m2_shaft_off(d):
    part(d, "shaft")["at"] = [0, 0.5, 0]


def m2_straddle(d):
    part(d, "brg_r")["at"] = [5, 0, 25]


def m2_parent(d):
    s = part(d, "shaft")
    s.update(parent=None, at=[0, 0, 25], rot=CYLX)


def m2_axes_conflict(d):
    part(d, "shaft")["joint"] = {"kind": "revolute", "axis": [0, 1, 0], "pivot": [0, 0, 0]}


def m2_axis_zero(d):
    part(d, "disc")["joint"]["axis"] = [0, 0, 0]


def m2_elec(d):
    d["parts"].append({"id": "esc2", "kind": "esc", **PLA, "at": [3, 0, 25], "shape": {"type": "box", "size": [3, 3, 3]}})
    d["connections"].append({"a": "esc2", "b": "disc", "method": "glue", "reason": "glued to the disc face"})


def m2_tilt(d):
    part(d, "disc")["rot"] = [0, 84, 0]


def m2_drum(d):
    part(d, "disc")["shape"] = cyl(5, 14)


def m2_screw_imb(d):
    d["fasteners"] = [{"id": "f3", "designation": "M3x3", "at": [-1.5, 0, 43], "dir": [1, 0, 0], "through": ["disc"], "tool": "hex2.5"}]


def m2_bore(d):
    part(d, "disc")["shape"] = {"type": "subtract", "base": cyl(20, 3), "cut": [cyl(2.6, 6)]}


CASES2 = [
    (m2_sweep_fastener, "kin.sweep_fastener"), (m2_bell_rub, "kin.outrunner_bell_rub"), (m2_motor_face, "kin.motor_face"),
    (m2_bearing_seat, "kin.bearing_seat"), (m2_shaft_short, "kin.shaft_through_bearings"), (m2_shaft_off, "kin.joint_axis_shaft"),
    (m2_straddle, "kin.bearing_straddle"), (m2_parent, "kin.parent_mismatch"), (m2_axes_conflict, "kin.group_axes_conflict"),
    (m2_axis_zero, "kin.joint_axis_zero"), (m2_elec, "kin.rotating_electronics"), (m2_tilt, "kin.balance_dynamic"),
    (m2_drum, "kin.spin_stability"), (m2_screw_imb, "kin.fastener_imbalance"), (m2_bore, "kin.bore_fit"),
]


@pytest.mark.parametrize("mut,cid", CASES2, ids=[f"{m.__name__}-{c}" for m, c in CASES2])
def test_spinner_mutation2_fails(mut, cid):
    d = copy.deepcopy(spinner())
    mut(d)
    rep, bad = run(d)
    assert cid in bad, [(f.id, f.message) for f in rep.findings if not f.passed]


def test_tooth_direction():
    res = []
    for mirror in (False, True):
        d = spinner()
        part(d, "disc")["shape"] = saw(mirror)
        res.append("kin.tooth_leading" in run(d)[1])
    assert sorted(res) == [False, True]


def belt_base():
    d = wheels()
    d["parts"] += [
        {"id": "pul_a", "kind": "pulley", **PLA, "at": [38.5, 0, 14], "rot": CYLX, "shape": cyl(5, 2)},
        {"id": "wheel_b", "kind": "wheel", "catalog": "wheel_28x10", "at": [30, -40, 14],
         "joint": {"kind": "revolute", "axis": [1, 0, 0], "pivot": [30, -40, 14]}},
        {"id": "pul_b", "kind": "pulley", **PLA, "parent": "wheel_b", "at": [8.5, 0, 0], "rot": CYLX, "shape": cyl(5, 2)},
        {"id": "belt", "kind": "belt", **PLA, "at": [38.5, -20, 30], "shape": {"type": "box", "size": [1, 1, 1]},
         "belt": {"pulleys": ["pul_a", "pul_b"], "kind": "o_ring", "length_mm": 100}},
        {"id": "tyre", "kind": "tyre", **PLA, "at": [-30, 0, 14], "rot": CYLX, "tyre_of": "wheel_r",
         "shape": {"type": "subtract", "base": cyl(16, 8), "cut": [cyl(14, 10)]}},
    ]
    d["connections"] += [{"a": "pul_a", "b": "wheel_l", "method": "glue", "reason": "pulley glued to wheel"},
                         {"a": "pul_b", "b": "wheel_b", "method": "glue", "reason": "pulley glued to wheel"}]
    return d


def test_good_belt_and_tyre_pass():
    rep, bad = run(belt_base())
    ids = {f.id for f in rep.findings if f.group == "kinematics" and f.passed}
    for cid in ("kin.belt_coplanar", "kin.belt_axes_parallel", "kin.belt_pulleys_joint", "kin.belt_same_group",
                "kin.pulley_coaxial", "kin.tyre_retained", "kin.wheel_track", "kin.sweep_rotating", "drive.coverage"):
        assert cid in ids and cid not in bad, (cid, [(f.id, f.message) for f in rep.findings if not f.passed])


def b_axes(d):
    part(d, "wheel_b")["joint"]["axis"] = [1, 0.1, 0]


def b_static(d):
    part(d, "belt")["belt"]["pulleys"] = ["pul_a", "base"]


def b_same(d):
    for c in d["connections"]:
        if c["a"] == "pul_b":
            c["b"] = "wheel_l"
    part(d, "pul_b").update(parent=None, at=[38.5, 0, 14])


def b_coax(d):
    part(d, "pul_a")["at"] = [38.5, 1, 14]


def b_tyre(d):
    part(d, "tyre")["at"] = [-30, 0, 50]


def b_track(d):
    part(d, "wheel_b")["at"] = [36, -40, 14]
    part(d, "wheel_b")["joint"]["pivot"] = [36, -40, 14]


def b_collide(d):
    part(d, "wheel_b")["at"] = [30, -20, 14]
    part(d, "wheel_b")["joint"]["pivot"] = [30, -20, 14]


def b_camber(d):
    part(d, "wheel_l")["rot"] = [0, 3, 0]
    part(d, "motor_l")["rot"] = [0, 3, 0]


def b_engage(d):
    part(d, "wheel_l")["at"] = [38.5, 0, 14]
    part(d, "pul_a")["at"] = [45, 0, 14]


BCASES = [(b_axes, "kin.belt_axes_parallel"), (b_static, "kin.belt_pulleys_joint"), (b_same, "kin.belt_same_group"),
          (b_coax, "kin.pulley_coaxial"), (b_tyre, "kin.tyre_retained"), (b_track, "kin.wheel_track"),
          (b_collide, "kin.sweep_rotating"), (b_camber, "kin.wheel_camber"), (b_engage, "kin.shaft_engagement")]


@pytest.mark.parametrize("mut,cid", BCASES, ids=[f"{m.__name__}-{c}" for m, c in BCASES])
def test_belt_wheel_mutation_fails(mut, cid):
    d = copy.deepcopy(belt_base())
    mut(d)
    rep, bad = run(d)
    assert cid in bad, [(f.id, f.message) for f in rep.findings if not f.passed]
