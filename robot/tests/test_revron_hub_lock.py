"""Motor-as-hub follow-ups: arch.double_bearing, spinner.bearing (motor-side support), kin.outrunner_bell_rub (dead shaft)
and legal.locking_bar via a declared removable pin (`weapon_lock`). Each relaxation keeps a bad case that still fails."""

import copy

from test_revron_fixes import AXZ, CYLX, PLA, box, cyl, drisk, dump, failed, part, passed, run


def _two_bearings(d):
    d["parts"].append({**copy.deepcopy(part(d, "brg")), "id": "brg2", "at": [12, 0, AXZ]})
    d["connections"] += [{"a": "brg2", "b": "upl", "method": "press_fit", "reason": "second bearing"},
                         {"a": "brg2", "b": "shaft", "method": "shaft", "reason": "inner race"}]


ARCH = ("mass", "power", "kinematics", "spinner", "architecture")


def test_arch_double_bearing_hub_passes():
    rep = run(drisk(), ARCH)
    assert passed(rep, "arch.double_bearing"), dump(rep)


def test_arch_double_bearing_hub_inferred_passes():
    d = drisk()
    del part(d, "shaft")["shaft_of"]
    rep = run(d, ARCH)
    assert passed(rep, "arch.double_bearing"), dump(rep)


def test_arch_double_bearing_two_extra_fails():
    d = drisk()
    _two_bearings(d)
    assert failed(run(d, ARCH), "arch.double_bearing")


def test_arch_double_bearing_off_axis_fails():
    d = drisk()
    part(d, "brg")["at"] = [16, 0, AXZ + 0.2]
    assert failed(run(d, ARCH), "arch.double_bearing")


def test_spinner_bearing_counts_bolted_hub_motor():
    rep = run(drisk(), ("mass", "power", "spinner"))
    assert passed(rep, "spinner.bearing"), dump(rep)


def test_spinner_bearing_unbolted_motor_does_not_count():
    d = drisk()
    d["connections"] = [c for c in d["connections"] if {c["a"], c["b"]} != {"wm", "upr"}]
    part(d, "upr")["at"] = [-40, 0, AXZ]  # nothing static near the motor
    assert failed(run(d, ("mass", "power", "spinner")), "spinner.bearing")


def _dead(d, z):
    d["parts"].append({"id": "dead", "kind": "structure", "material": "steel", "at": [-12, 0, z], "rot": CYLX, "shape": cyl(1.5, 6)})
    d["connections"].append({"a": "dead", "b": "upr", "method": "press_fit", "reason": "dead stub in the upright"})


def test_bell_rub_ignores_dead_shaft_in_bore():
    d = drisk()
    _dead(d, AXZ)
    rep = run(d, ("mass", "power", "kinematics"))
    assert not [f for f in failed(rep, "kin.outrunner_bell_rub") if "dead" in f.message], dump(rep)


def test_bell_rub_flags_static_part_in_bell():
    d = drisk()
    _dead(d, AXZ + 6)
    rep = run(d, ("mass", "power", "kinematics"))
    assert [f for f in failed(rep, "kin.outrunner_bell_rub") if "dead" in f.message], dump(rep)


def _lock(d, plate_hole=True, disc_hole=True):
    pin = {"type": "place", "rot": CYLX, "at": [0, 0, 15], "shape": cyl(1.6, 10)}
    d["parts"].append({"id": "lockplate", "kind": "structure", **PLA, "at": [10, 0, AXZ],
                       "shape": {"type": "subtract", "base": box(3, 30, 40), "cut": [pin]} if plate_hole else box(3, 30, 40)})
    d["connections"].append({"a": "lockplate", "b": "base", "method": "screw", "reason": "lock plate"})
    if disc_hole:
        ds = part(d, "disc")
        ds["shape"] = {"type": "subtract", "base": ds["shape"], "cut": [{"type": "place", "at": [-15, 0, 0], "shape": cyl(1.6, 10)}]}
    d["weapon_lock"] = {"type": "removable_pin", "holes": ["disc", "lockplate"]}
    return d


LEGAL = ("mass", "power", "legal")


def test_weapon_lock_pin_declared_passes():
    rep = run(_lock(drisk()), LEGAL)
    assert passed(rep, "legal.locking_bar"), dump(rep)


def test_weapon_lock_missing_declaration_fails():
    d = _lock(drisk())
    del d["weapon_lock"]
    assert failed(run(d, LEGAL), "legal.locking_bar")


def test_weapon_lock_missing_hole_fails():
    assert failed(run(_lock(drisk(), plate_hole=False), LEGAL), "legal.locking_bar")
    assert failed(run(_lock(drisk(), disc_hole=False), LEGAL), "legal.locking_bar")
