"""A weapon motor modelled as two parts (fixed `<base>_stator`, kind weapon_motor, + spinning `<base>_can`, kind other) is
the same motor to kin.torque_path / kin.bearing_count / kin.sweep_static / arch.weapon_supports / spinner.bearing as one
fused weapon_motor body: the can is the rotor link, the stator the motor body. Each form keeps a bad case that fails."""

import numpy as np
import pytest

from test_revron_fixes import AXZ, CYLX, cyl, drisk, dump, failed, part, passed, run

CHECKS = ("kin.torque_path", "kin.bearing_count", "kin.sweep_static", "arch.weapon_supports", "spinner.bearing")
GROUPS = ("mass", "power", "kinematics", "spinner", "architecture")


def fused():
    return drisk()


def split():
    d = drisk()
    part(d, "wm")["id"] = "wm_stator"
    part(d, "disc")["weapon"]["motor"] = "wm_stator"
    part(d, "shaft")["shaft_of"] = "wm_can"
    # the bell: spins with the disc (child of the spider), around the fixed stator
    d["parts"].append({"id": "wm_can", "kind": "other", "role": "rotor", "material": "steel", "parent": "spider",
                       "at": [0, 0, -3.5], "shape": cyl(11.5, 2, 2.5)})
    for c in d["connections"]:
        if {c["a"], c["b"]} in ({"wm", "spider"}, {"wm", "shaft"}):
            c["a"], c["b"] = ("wm_can", c["b"] if c["a"] == "wm" else c["a"])
        for e in ("a", "b"):
            if c[e] == "wm":
                c[e] = "wm_stator"
    return d


def stator_of(d):
    return "wm_stator" if any(p["id"] == "wm_stator" for p in d["parts"]) else "wm"


@pytest.mark.parametrize("make", [fused, split])
def test_good_passes(make):
    rep = run(make(), GROUPS)
    for cid in CHECKS:
        assert passed(rep, cid), (cid, dump(rep))


def undriven(d):
    # nothing couples the weapon to the motor rotor any more
    rot = "wm_can" if stator_of(d) == "wm_stator" else "wm"
    d["connections"] = [c for c in d["connections"] if rot not in (c["a"], c["b"]) or stator_of(d) in (c["a"], c["b"])
                        and rot == "wm" and c["b"] in ("upr", "base")]
    if rot == "wm_can":
        part(d, "wm_can")["parent"] = None
        part(d, "wm_can")["at"] = [-50, 40, AXZ]
        part(d, "wm_can")["rotates_with"] = "wm_can"
    part(d, "shaft")["shaft_of"] = None


def no_bearing(d):
    d["connections"] = [c for c in d["connections"] if "brg" not in (c["a"], c["b"])]
    d["parts"] = [p for p in d["parts"] if p["id"] != "brg"]


def stud(d):
    d["parts"].append({"id": "stud", "kind": "structure", "material": "pla", "process": "fdm", "at": [2.75, 14, AXZ + 8],
                       "shape": {"type": "box", "size": [2, 3, 3]}})


def unbolted(d):
    st = stator_of(d)
    d["connections"] = [c for c in d["connections"] if {c["a"], c["b"]} != {st, "upr"}]
    part(d, "upr")["at"] = [-40, 0, AXZ]


@pytest.mark.parametrize("make", [fused, split])
@pytest.mark.parametrize("mut,cids", [
    (undriven, ("kin.torque_path",)), (no_bearing, ("kin.bearing_count", "spinner.bearing")), (stud, ("kin.sweep_static",)),
    (unbolted, ("spinner.bearing", "arch.weapon_supports")),
])
def test_bad_fails(make, mut, cids):
    d = make()
    mut(d)
    rep = run(d, GROUPS)
    for cid in cids:
        assert failed(rep, cid), (cid, dump(rep))


def test_pairing():
    from robot.checks.kinematics import split_motors

    class RP:
        def __init__(self, **kw):
            self.part = type("P", (), {"_extra": kw.pop("_extra", {}), "catalog": None, **kw})()

    parts = {"wm_stator": RP(kind="weapon_motor", catalog="gr1507"), "wm_can": RP(kind="other"),
             "bell2": RP(kind="other", catalog="gr1507_can", _extra={"role": "rotor"}), "lone_can": RP(kind="other")}
    assert split_motors(parts) == {"wm_can": "wm_stator", "bell2": "wm_stator"}



class _Tube:
    """Axis-aligned (x) tube r_in..r_out over x0..x1: a stand-in body for spinner.hold_mm."""
    fastener, mesh = False, None

    def __init__(self, kind, x0, x1, r_in, r_out):
        self.kind, self.x0, self.x1, self.r_in, self.r_out = kind, x0, x1, r_in, r_out
        self.mesh = type("M", (), {"vertices": np.array([[x0, 0, 0], [x1, 0, 0], [x0, r_out, 0], [x1, -r_out, 0]], float)})()

    def inside(self, P):
        P = np.atleast_2d(P)
        r = np.hypot(P[:, 1], P[:, 2])
        return (P[:, 0] >= self.x0) & (P[:, 0] <= self.x1) & (r >= self.r_in) & (r <= self.r_out)


def test_hub_motor_with_open_bore_holds_its_shaft():
    """A stator drawn with an open bore (bearings not modelled) still carries its own shaft along its length, exactly as a
    solid fused envelope does; without the motor-as-hub qualification (no `extra`) it does not count."""
    from robot.checks.spinner import hold_mm

    weapon, shaft, stator = _Tube("weapon", -1, 1, 0, 20), _Tube("shaft", -10, 9, 0, 2.5), _Tube("weapon_motor", 2, 10, 4, 9)
    w = type("W", (), {"bodies": [weapon, shaft, stator]})()
    o, a = np.zeros(3), np.array([1.0, 0, 0])
    assert hold_mm(w, 1, 0, o, a, 1.0, 1.0, (2,), 2.5) >= 6.0
    assert hold_mm(w, 1, 0, o, a, 1.0, 1.0, (), 2.5) == 0.0
