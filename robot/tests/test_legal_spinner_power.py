"""legal, power and spinner groups: parity with the Rust report on the wedge, and a synthetic horizontal spinner."""

import math

import pytest

from robot import spec
from robot.checks import Options, verify
from robot.checks.spinner import dirs26

ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]


def box(x, y, z):
    return {"type": "box", "size": [x, y, z]}


def cyl(r, h):
    return {"type": "cylinder", "radius": r, "height": h}


def spinner_spec(**over):
    parts = [
        {"id": "base", "kind": "structure", "material": "nylon", "shape": box(100, 100, 4), "at": [0, 0, 0], "color": "#202020"},
        {"id": "top", "kind": "structure", "material": "nylon", "shape": box(100, 100, 4), "at": [0, 0, 24]},
        {"id": "disc", "kind": "weapon", "material": "steel", "shape": cyl(40, 4), "at": [0, 0, 12],
         "weapon": {"kind": "disc", "motor": "wm", "reduction": 2.0, "locking_bar": "pin"}},
        {"id": "shaft", "kind": "shaft", "material": "steel", "shape": cyl(2.5, 28), "at": [0, 0, 12]},
        {"id": "pin", "kind": "locking_bar", "material": "steel", "shape": cyl(1.5, 30), "at": [30, 0, 12], "color": "#ff2000",
         "tethered": True},
        {"id": "wm", "kind": "weapon_motor", "catalog": "bl_2306_1400kv", "at": [0, 60, 12]},
        {"id": "bat", "kind": "battery", "catalog": "lipo_2s_180", "at": [0, -60, 12]},
        {"id": "sw", "kind": "switch", "catalog": "switch_slide_12x4", "tool_free": True, "marked": True, "at": [0, -60, 30]},
    ]
    d = {"name": "spin", "robot_type": "horizontal_spinner", "locomotion": "roller", "parts": parts,
         "electronics": {"failsafe": True, "weapon_remote_disable": True}}
    d.update(over)
    return spec.Spec(d)


@pytest.fixture(scope="module")
def spin_rep():
    return verify(spinner_spec(), Options(only=["mass", "legal", "power", "spinner"], deep=False, fast=True))


@pytest.fixture(scope="module")
def wedge_rep():
    return verify(spec.load(ROOT / "templates" / "wedge_2wd.json"), Options(only=["mass", "legal", "power", "spinner"], deep=False, fast=True))


def ids(rep, passed=None):
    return {f.id for f in rep.findings if passed is None or f.passed == passed}


def test_wedge_matches_rust(wedge_rep):
    rep = wedge_rep
    assert {"legal.switch", "switch.recess", "legal.failsafe", "legal.footprint", "power.battery"} <= ids(rep, True)
    assert not any(f.group in ("legal", "power", "spinner") and not f.passed for f in rep.findings)
    assert abs(rep.metrics["footprint_mm"] - 122.48) < 0.1
    assert abs(rep.metrics["peak_current_a"] - 2.0) < 1e-9  # two N10s stalled at ~1 A each (was 0.65 = half of one in Rust)
    assert "legal.weapon_disable" not in ids(rep)


def test_spinner_power_numbers(spin_rep):
    m = spin_rep.metrics
    assert abs(m["weapon_rpm"] - 4.2 * 2 * 1400 / 2) < 1e-6
    rim = 40.0
    assert m["tip_speed_mph"] == pytest.approx(m["weapon_rpm"] * 2 * rim * math.pi * 60 / 1_609_344, rel=0.01)
    # Solid disc: I = 1/2 m r^2, m = rho V.
    iner = 0.5 * (7.9e-3 * math.pi * 40 ** 2 * 4) * 1e-3 * (0.040 ** 2)
    om = m["weapon_rpm"] * 0.85 * 2 * math.pi / 60
    assert m["weapon_energy_j"] == pytest.approx(0.5 * iner * om * om, rel=0.03)
    assert "power.tip_speed" in ids(spin_rep, True)
    assert m["peak_current_a"] == pytest.approx(20.0)
    assert "power.battery" in ids(spin_rep, False)


def test_spinner_bearing_and_lock(spin_rep):
    f = spin_rep.get("spinner.bearing")
    assert f.passed, f.message
    assert spin_rep.metrics["weapon_shaft_hold_mm"] >= 3.0
    assert {"legal.weapon_disable", "legal.switch", "legal.failsafe"} <= ids(spin_rep, True)
    assert not ids(spin_rep, False) & {"legal.locking_bar", "legal.locking_bar_blocks", "legal.locking_bar_colour", "legal.locking_bar_tether"}
    assert "spinner.exposed" in ids(spin_rep, False)  # motor and battery sit in the open
    assert "spinner.sweep_near" not in ids(spin_rep)


def test_spinner_failures():
    s = spinner_spec(electronics={"failsafe": False})
    s.parts = [p for p in s.parts if p.id not in ("shaft", "sw")]
    s.part("pin").at = [70, 0, 12]
    s.part("pin").tethered = False
    s.part("disc").material = "pla"
    s.part("bat").at = [0, -38, 12]
    rep = verify(s, Options(only=["mass", "legal", "power", "spinner"], deep=False, fast=True))
    bad = ids(rep, False)
    assert {"legal.switch", "legal.failsafe", "legal.weapon_disable", "legal.weapon_brittle", "legal.weapon_soft",
            "legal.locking_bar_blocks", "legal.locking_bar_tether", "spinner.bearing", "spinner.sweep_near"} <= bad


def test_switch_axis_and_exposure():
    s = spinner_spec()
    s.part("sw").actuation = [0, 0, 1]
    s.part("sw").at = [0, -30, 27]  # proud of the top plate
    rep = verify(s, Options(only=["legal"], deep=False, fast=True))
    assert "switch.vertical_axis" in ids(rep, False)
    assert "switch.exposed" in ids(rep, False)


def test_footprint_fails_when_too_big():
    s = spinner_spec()
    s.part("base").shape = box(160, 100, 4)
    rep = verify(s, Options(only=["legal"], deep=False, fast=True))
    assert "legal.footprint" in ids(rep, False)


def test_dirs26():
    d = dirs26()
    assert d.shape == (26, 3)
