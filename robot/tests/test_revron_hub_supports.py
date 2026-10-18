"""Motor-as-hub supports: the weapon motor's own bearings count as the motor-side support (arch.weapon_supports) when its
stator is screwed to a static upright, and a shaft tail does not push archetype.disc_supported sampling past the upright.
Each relaxation keeps a bad case that still fails."""

from test_revron_fixes import AXZ, dump, drisk, failed, part, passed, run

ARCH = ("mass", "power", "kinematics", "architecture")
ARC = ("mass", "power", "archetype")


def _unbolt(d):
    d["connections"] = [c for c in d["connections"] if {c["a"], c["b"]} != {"wm", "upr"}]
    part(d, "upr")["at"] = [-40, 0, AXZ]  # nothing static near the motor
    return d


def test_arch_supports_hub_motor_counts():
    rep = run(drisk(), ARCH)
    assert passed(rep, "arch.weapon_supports"), dump(rep)


def test_arch_supports_unbolted_motor_fails():
    assert failed(run(_unbolt(drisk()), ARCH), "arch.weapon_supports")


def test_arch_supports_no_far_support_fails():
    d = drisk()
    d["parts"] = [p for p in d["parts"] if p["id"] not in ("brg", "upl")]
    d["connections"] = [c for c in d["connections"] if not {c["a"], c["b"]} & {"brg", "upl"}]
    assert failed(run(d, ARCH), "arch.weapon_supports")


def test_disc_supported_ignores_shaft_tail():
    rep = run(drisk(), ARC)
    assert passed(rep, "archetype.disc_supported"), dump(rep)


def test_disc_supported_missing_side_fails():
    d = drisk()
    part(d, "upl")["at"] = [16, 0, AXZ + 40]  # far upright moved off the axle line
    part(d, "brg")["at"] = [16, 0, AXZ + 40]
    assert failed(run(d, ARC), "archetype.disc_supported")
