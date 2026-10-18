"""Verifier fixes the Revron build had to hack around. Each fix keeps a bad case that still fails.
1. interference.spin: a weapon's own rotor parts are swept with it, not hit by it; allow_overlap > 2 mm warns.
2. mfg.thin_wall: no false walls on the rim of curved (spline) extrusion ends; real thin walls still caught.
3. legal.locking_bar (removable pin): the hole test does not depend on where a slice lands (5.0 vs 4.95 mm).
4. power.runtime: the pack must last a fight (profile.fight_s) with margin under a match duty cycle, else BLOCKER."""

import copy
import json
from pathlib import Path

import pytest

from robot import spec, world
from robot.checks import Ctx, Options, interference, verify
from test_revron_fixes import drisk, failed, passed, run
from test_revron_hub_lock import LEGAL, _lock

ROOT = Path(__file__).resolve().parents[1]


def _ctx(parts, **extra):
    r = world.resolve(spec.Spec({"name": "t", "parts": parts, **extra}), fast=True)
    return Ctx(r, world.World.start(r), Options(fast=True))


def box(id, at, size, kind="structure", **kw):
    return {"id": id, "kind": kind, "shape": {"type": "box", "size": list(size)}, "at": list(at), "material": "steel", **kw}


def _spin(fs):
    return [f for f in fs if f.id in ("interference.spin", "interference.spin_clearance")]


# 1. spinning-weapon sweep and its rotor ---------------------------------------------------------------------------

def _rotor(pin_at=(15, 0, 0), pin_kw=None, post_at=(60, 0, 0)):
    disc = box("disc", (0, 0, 0), (40, 4, 3), kind="weapon", weapon={"kind": "bar"})
    pin = box("pin", pin_at, (2, 2, 8), kind="pin", **(pin_kw if pin_kw is not None else {"parent": "disc"}))
    return [disc, pin, box("post", post_at, (4, 4, 30))]


def test_rotor_child_is_not_hit_by_its_own_weapon():
    # the screw through the bar sticks out of it, inside the swept disc, but it turns with the bar
    fs = _spin(interference.spin_sweeps(_ctx(_rotor())))
    assert fs and all(f.passed for f in fs), [f.message for f in fs]


def test_rotor_by_motion_group_is_not_hit():
    parts = _rotor(pin_kw={"rotates_with": "w"})
    parts[0]["rotates_with"] = "w"
    fs = _spin(interference.spin_sweeps(_ctx(parts)))
    assert fs and all(f.passed for f in fs), [f.message for f in fs]


def test_static_part_in_sweep_still_hit():
    parts = _rotor(pin_kw={})  # same screw, not on the rotor: the bar sweeps through it
    fs = _spin(interference.spin_sweeps(_ctx(parts)))
    assert [f for f in fs if not f.passed and f.parts == ["disc", "pin"]]


def test_fixed_child_of_rotor_is_still_hit():
    parts = _rotor(pin_kw={"parent": "disc", "rotates_with": "fixed"})
    fs = _spin(interference.spin_sweeps(_ctx(parts)))
    assert [f for f in fs if not f.passed and "pin" in f.parts]


def test_rotor_part_sweep_hits_frame():
    # the screw head stands proud of the bar; the post is clear of the bar's own sweep but not of the screw's
    parts = _rotor(pin_at=(15, 0, 4), post_at=(0, 12, 8))
    parts[2]["shape"]["size"] = [4, 4, 4]
    fs = _spin(interference.spin_sweeps(_ctx(parts)))
    bad = [f for f in fs if not f.passed]
    assert bad and bad[0].parts == ["disc", "post"] and "`pin`" in bad[0].message


def test_blanket_allow_overlap_warns():
    c = _ctx([box("a", (0, 0, 0), (10, 10, 10)), box("b", (9, 0, 0), (10, 10, 10))],
             allow_overlap=[{"a": "a", "b": "b", "max_depth_mm": 1000.0, "reason": "hack"}])
    f = [f for f in interference.run(c) if f.id == "interference.blanket_allow"]
    assert f and f[0].severity == "warning" and "hides real collisions" in f[0].title
    c = _ctx([box("a", (0, 0, 0), (10, 10, 10)), box("b", (9.5, 0, 0), (10, 10, 10))],
             allow_overlap=[{"a": "a", "b": "b", "max_depth_mm": 0.6, "reason": "press fit"}])
    assert not [f for f in interference.run(c) if f.id == "interference.blanket_allow"]


# 2. thin walls on curved extrusion ends ---------------------------------------------------------------------------

BLOB = [[0, 0], [30, 0], [40, 10], [30, 25], [5, 30], [-5, 15]]


def _mfg(shape):
    rep = verify(spec.Spec({"name": "t", "parts": [{"id": "p", "kind": "structure", "material": "pla", "process": "fdm", "shape": shape}]}),
                 Options(only=["mfg"], deep=False, fast=True))
    return {f.id: f for f in rep.findings if f.group == "mfg"}


@pytest.mark.parametrize("t", ["spline_prism", "prism"])
def test_curved_profile_end_is_not_a_thin_wall(t):
    f = _mfg({"type": t, "points": BLOB, "height": 5})
    assert "mfg.thin_wall" not in f and f["mfg.walls"].passed


def test_thin_spline_plate_still_fails():
    f = _mfg({"type": "spline_prism", "points": BLOB, "height": 0.5})
    assert f["mfg.thin_wall"].severity == "blocker"


def test_thin_tapered_web_still_fails():
    # a knife-edge triangle: the walls face each other at a shallow angle, a real sliver
    f = _mfg({"type": "prism", "points": [[0, 0], [40, 0], [0, 6]], "height": 5})
    assert "mfg.thin_wall" in f


# 3. removable weapon pin: robust to the plate thickness -----------------------------------------------------------

@pytest.mark.parametrize("thick", [3.0, 4.95, 5.0, 5.05])
def test_weapon_lock_independent_of_thickness(thick):
    d = _lock(drisk())
    lp = next(p for p in d["parts"] if p["id"] == "lockplate")
    lp["shape"]["base"]["size"][0] = thick
    lp["at"][0] = 10 + (thick - 3) / 2  # keep the inner face where it was
    rep = run(d, LEGAL)
    assert passed(rep, "legal.locking_bar")


@pytest.mark.parametrize("thick", [4.95, 5.0])
def test_weapon_lock_missing_hole_fails_any_thickness(thick):
    d = _lock(drisk(), plate_hole=False)
    lp = next(p for p in d["parts"] if p["id"] == "lockplate")
    lp["shape"]["size"][0] = thick
    assert failed(run(d, LEGAL), "legal.locking_bar")


# 4. battery runtime -----------------------------------------------------------------------------------------------

def _revron_with(cat):
    d = json.loads((ROOT / "templates" / "revron.json").read_text())
    for p in d["parts"]:
        if p["id"] == "battery" or p.get("kind") == "battery":
            p["catalog"] = cat
    return verify(spec.Spec(d), Options(only=["power"], deep=False, fast=True))


def test_runtime_small_pack_blocks():
    rep = _revron_with("lipo_2s_180")
    f = [f for f in rep.findings if f.id == "power.runtime"]
    assert f and not f[0].passed and f[0].severity == "blocker", [x.message for x in f]
    assert rep.metrics["runtime_min"] < 3.0


def test_runtime_adequate_pack_passes():
    rep = _revron_with("lipo_2s_350")
    f = [f for f in rep.findings if f.id == "power.runtime"]
    assert f and f[0].passed and rep.metrics["runtime_min"] >= 3.0 * 1.25


def test_runtime_unknown_current_is_not_a_pass():
    d = drisk()
    d["parts"].append({"id": "bat", "kind": "battery", "catalog": "lipo_2s_350", "at": [0, -40, 10]})
    d["parts"].append({"id": "m1", "kind": "motor", "material": "steel", "at": [20, -40, 10],
                       "shape": {"type": "box", "size": [5, 5, 5]}})
    rep = verify(spec.Spec(d), Options(only=["power"], deep=False, fast=True))
    f = [f for f in rep.findings if f.id == "power.runtime"]
    assert f and not f[0].passed and any("runtime" in n.lower() for n in rep.not_checked)
