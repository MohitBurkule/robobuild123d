"""Hinged weapons (lifter / flipper / axe) are judged on what they really do (robot/checks/arm_sweep.py):

- wire.rotor_clearance, battery.rotor_gap, electrical.battery_weapon_gap and the wire router use the volume the arm
  sweeps over its declared joint range, not a full revolution or its whole box;
- power.weapon_motor wants a servo or gearmotor for an arm, a kV brushless motor for a spinner;
- process.weapon_printed applies to spinners only.

Each rule has a good case and a bad case that must still fail (an arm that really sweeps through a wire or the battery).
"""

import copy

import numpy as np

from robot import spec, world
from robot.checks import Ctx, Options, verify
from robot.checks import arm_sweep, wiring
from robot.proxy import wiring as pwiring

NYLON = {"material": "nylon", "process": "fdm", "print_orientation": "+z"}
PIVOT = [0, -30, 22]


def box(x, y, z):
    return {"type": "box", "size": [x, y, z]}


def lifter(kind="lifter", lo=0, hi=80, bat_at=(0, 0, 6), via=None, **weapon):
    """An open 80 x 80 x 20 tub (3 mm floor) and a back post that lifts the world (and router) bounds to z 40. The arm
    is a 20 x 60 x 3 plate with a front lip hanging into the tub, hinged at its back edge (pivot y -30, z 22), lifting
    its front up over lo..hi degrees. The battery, ESC and their wire sit in the tub under the plate: inside the arm's
    box and inside a full revolution (34 mm from the pivot), but never reached by the upward sweep."""
    w = {"id": "w1", "from": "esc.p", "to": "bat.p", "kind": "signal", "awg": 30}
    if via is not None:
        w["via"] = [list(via)]
    arm = {"type": "union", "items": [box(20, 60, 3), {"type": "place", "at": [0, 28.5, -7.5], "shape": box(20, 3, 12)}]}
    return {
        "name": "arm", "robot_type": "lifter",
        "parts": [
            {"id": "tub", "kind": "structure", **NYLON, "at": [0, 0, 10],
             "shape": {"type": "subtract", "base": box(80, 80, 20), "cut": [{"type": "place", "at": [0, 0, 2], "shape": box(76, 76, 18)}]}},
            {"id": "plate", "kind": "weapon", **NYLON, "at": [0, 0, 22], "shape": arm,
             "joint": {"kind": "revolute", "axis": [1, 0, 0], "pivot": PIVOT, "min": lo, "max": hi, "default": 0},
             "weapon": {"kind": kind, **weapon}},
            {"id": "esc", "kind": "esc", "shape": box(10, 10, 4), "at": [0, 20, 6], "material": "pla", "process": "cots",
             "ports": {"p": [0, 0, 2]}},
            {"id": "bat", "kind": "battery", "shape": box(20, 10, 6), "at": list(bat_at), "material": "pla",
             "process": "cots", "ports": {"p": [0, 0, 3]}},
            {"id": "post", "kind": "structure", **NYLON, "at": [35, -35, 20], "shape": box(4, 4, 40)},
        ],
        "wires": [w],
    }


def run(d, groups):
    rep = verify(spec.Spec(d), Options(fast=True, only=list(groups)))
    crashed = [str(f) for f in rep.findings if f.id.endswith(".crashed")]
    assert not crashed, crashed
    return rep


def bad(rep, fid):
    return [f.message for f in rep.findings if f.id == fid and not f.passed]


def good(rep, fid):
    return [f for f in rep.findings if f.id == fid and f.passed]


def ctx_of(d):
    r = world.resolve(spec.Spec(d), fast=True)
    return r, world.World.start(r)


# ------------------------------------------------------------------------------------------- the sweep itself
def test_arm_range_only_for_hinged_weapons_on_limited_joints():
    for kind, lo, hi, want in (("lifter", 0, 80, (0.0, 80.0)), ("flipper", -10, 60, (-10.0, 60.0)),
                               ("lifter", 0, 360, None), ("disc", 0, 80, None), ("saw", 0, 80, None)):
        r, w = ctx_of(lifter(kind, lo, hi))
        assert arm_sweep.arm_range(r.spec, w, "plate", ["plate"]) == want, (kind, lo, hi)


def test_arc_sweep_matches_the_posed_arm():
    """Points on the arm at any pose in its range are inside the sweep; points it reaches only past `max`, or below the
    pivot (a full turn), are not."""
    d = lifter()
    r, w0 = ctx_of(d)
    sw = arm_sweep.arm_sweeps(r.spec, w0)["plate"]
    for v in (0, 25, 57, 80):
        b = world.World.build(r, {"plate": v}).body("plate")
        P = b.surface(1.0)[0][:200]
        assert sw.dist(P).max() < 0.05, v
    tip = np.array([0.0, 29.0, 22.0])   # front edge at 0 deg
    beyond = world.World.build(r, {"plate": 120}).body("plate").center   # only reached past max
    below = np.array([0.0, 0.0, 6.0])   # the battery's place: reached only by a full turn
    dist = sw.dist(np.array([tip, beyond, below]), cap=50.0)
    assert dist[0] == 0.0 and dist[1] > 5.0 and dist[2] > 10.0


# ---------------------------------------------------------------------------------------- wire.rotor_clearance
def test_wire_under_lifter_is_clear():
    rep = run(lifter(), ["wire_review"])
    assert not bad(rep, "wire.rotor_clearance"), bad(rep, "wire.rotor_clearance")
    assert good(rep, "wire.rotor_clearance")


def test_wire_in_lifter_path_still_fails():
    rep = run(lifter(via=(0, 0, 35)), ["wire_review"])   # 33 mm from the pivot at 23 deg: inside the 0..80 sweep
    msgs = bad(rep, "wire.rotor_clearance")
    assert msgs and "0..80 deg range" in msgs[0], msgs


def test_full_turn_and_spinner_still_revolve():
    for d in (lifter(hi=360), lifter(kind="disc")):
        assert bad(run(d, ["wire_review"]), "wire.rotor_clearance")


# --------------------------------------------------------------------------- battery.rotor_gap / battery_weapon_gap
def test_battery_under_lifter_is_clear():
    rep = run(lifter(), ["realworld", "electrical"])
    assert not bad(rep, "battery.rotor_gap"), bad(rep, "battery.rotor_gap")
    assert not bad(rep, "electrical.battery_weapon_gap"), bad(rep, "electrical.battery_weapon_gap")


def test_battery_in_lifter_path_still_fails():
    rep = run(lifter(bat_at=(0, 0, 35)), ["realworld", "electrical"])
    assert bad(rep, "battery.rotor_gap")
    assert bad(rep, "electrical.battery_weapon_gap")


def test_battery_under_full_turn_arm_fails():
    assert bad(run(lifter(hi=360), ["realworld"]), "battery.rotor_gap")


# ------------------------------------------------------------------------------------------ power.weapon_motor
def with_actuator(d, cat, kind, **weapon):
    d = copy.deepcopy(d)
    d["parts"].append({"id": "act", "kind": kind, "catalog": cat, "at": [0, -33, 10]})
    d["parts"][1]["weapon"].update({"motor": "act", **weapon})
    return d


def test_lifter_with_servo_or_gearmotor_passes():
    for cat, kind in (("servo_cs07", "servo"), ("n20_1000rpm_6v", "motor")):
        rep = run(with_actuator(lifter(), cat, kind), ["power"])
        assert not bad(rep, "power.weapon_motor"), (cat, bad(rep, "power.weapon_motor"))
        assert good(rep, "power.weapon_motor")


def test_actuated_by_names_the_servo():
    d = with_actuator(lifter(), "servo_cs07", "servo")
    d["parts"][1]["weapon"].pop("motor")
    d["parts"][1]["actuated_by"] = "act"
    assert not bad(run(d, ["power"]), "power.weapon_motor")


def test_lifter_without_actuator_or_on_direct_brushless_fails():
    msgs = bad(run(lifter(), ["power"]), "power.weapon_motor")
    assert msgs and "no actuator" in msgs[0], msgs
    direct = with_actuator(lifter(), "bl_1806_2300kv", "weapon_motor")
    assert bad(run(direct, ["power"]), "power.weapon_motor")
    geared = with_actuator(lifter(), "bl_1806_2300kv", "weapon_motor", reduction=30)
    assert not bad(run(geared, ["power"]), "power.weapon_motor")


def test_spinner_still_needs_kv_motor():
    msgs = bad(run(with_actuator(lifter(kind="disc"), "servo_cs07", "servo"), ["power"]), "power.weapon_motor")
    assert msgs and "brushless" in msgs[0], msgs


# --------------------------------------------------------------------------------------- process.weapon_printed
def test_printed_lifter_ok_printed_spinner_fails():
    assert not bad(run(lifter(), ["process"]), "process.weapon_printed")
    assert bad(run(lifter(kind="disc"), ["process"]), "process.weapon_printed")
    assert bad(run(lifter(kind="none"), ["process"]), "process.weapon_printed")


# ------------------------------------------------------------------------------------------------- the router
def test_router_blocks_the_sweep_not_the_box():
    r, w = ctx_of(lifter())
    sw = arm_sweep.arm_sweeps(r.spec, w)
    old, new = wiring.Router(w), wiring.Router(w, sw)
    under = np.array([0.0, 0.0, 12.0])   # in the tub under the plate: inside the arm's padded box, never swept
    up = np.array([0.0, 0.0, 35.0])      # in the arm's path at 23 deg, outside its box at rest
    rest = np.array([0.0, 0.0, 22.0])    # the plate itself
    assert old.solid[old.cell(under)] and not new.solid[new.cell(under)]
    assert not old.solid[old.cell(up)] and new.solid[new.cell(up)]
    assert old.solid[old.cell(rest)] and new.solid[new.cell(rest)]


def test_router_routes_under_the_arm_only_with_the_sweep():
    r, w = ctx_of(lifter())
    a, b = np.asarray(w.port(r, "esc.p"), float), np.asarray(w.port(r, "bat.p"), float)
    path, _ = wiring.Router(w).route(a, b, 0.45)
    assert path is None                    # the arm's box covers both ports' surroundings
    path, _ = wiring.Router(w, arm_sweep.arm_sweeps(r.spec, w)).route(a, b, 0.45)
    assert path is not None


def test_proxy_wiring_uses_the_sweep():
    r, w = ctx_of(lifter())
    sw = arm_sweep.arm_sweeps(r.spec, w)
    under = pwiring.sample([[0, -10, 12], [0, 10, 12]])
    hit_box, who = pwiring.blocked(w, under, 0.3, [])
    assert hit_box.any() and "plate" in set(who[hit_box])
    hit_sw, _ = pwiring.blocked(w, under, 0.3, [], sw)
    assert not hit_sw.any()
    through = pwiring.sample([[0, 0, 33], [0, 0, 37]])
    hit, who = pwiring.blocked(w, through, 0.3, [], sw)
    assert hit.any() and "plate" in set(who[hit])
