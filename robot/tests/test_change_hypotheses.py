"""Change hypotheses (robot/gen/changes.py), the settings overlay (robot/overlay.py) and their robust-runner plumbing."""

import json
from pathlib import Path

import pytest

from robot import overlay as O
from robot.catalog import CatalogEntry
from robot.gen import changes as C
from robot.spec import Spec

ROOT = Path(__file__).resolve().parents[2]


def _raw():
    return {"name": "t", "parts": [
        {"id": "tub", "kind": "structure"},
        {"id": "motor_l", "kind": "motor", "catalog": "n10_2200rpm_spicy", "at": [0, 0, 0]},
        {"id": "motor_r", "kind": "motor", "catalog": "n10_2200rpm_spicy", "at": [0, 0, 0]},
        {"id": "battery", "kind": "battery", "catalog": "lipo_2s_180_turnabot", "at": [0, 0, 0], "rot": [0, 0, 90]},
        {"id": "belt_l", "kind": "belt"}, {"id": "belt_r", "kind": "belt"}],
        "connections": [{"a": "belt_l", "b": "tub", "method": "x"}, {"a": "motor_l", "b": "tub", "method": "x"}],
        "wires": [{"id": "w", "from": "battery.jst_rcy", "to": "tub.in", "connector": "jst_rcy"}]}


def test_overlay_catalog_swap_remaps_ports():
    out = O.apply(_raw(), [{"op": "catalog", "select": {"id": "battery"}, "to": "lipo_2s_350"}], hooks={})
    bat = O.select(out, {"id": "battery"})[0]
    assert bat["catalog"] == "lipo_2s_350"
    assert out["wires"][0]["from"] == "battery.xt30" and out["wires"][0]["connector"] == "xt30"


def test_overlay_remove_cascades_and_glob():
    out = O.apply(_raw(), [{"op": "remove", "select": {"id": "belt_*"}}], hooks={})
    assert not O.select(out, {"kind": "belt"})
    assert [c["a"] for c in out["connections"]] == ["motor_l"]


def test_overlay_hook_and_anchor():
    hooks = {"hooks": {"drive.driven_wheels": {"values": {"2WD": [{"op": "remove", "select": {"kind": "belt"}}]}}},
             "anchors": {"deck": {"at": [1, 2, 3], "rot": [0, 0, 90]}}}
    out = O.apply(_raw(), [{"op": "hook", "name": "drive.driven_wheels", "value": "2WD"},
                           {"op": "add", "part": {"id": "sv", "kind": "servo", "catalog": "servo_cs07"}, "anchor": "deck"}], hooks)
    assert not O.select(out, {"kind": "belt"})
    assert O.select(out, {"id": "sv"})[0]["at"] == [1, 2, 3]
    with pytest.raises(O.MissingHook):
        O.apply(_raw(), [{"op": "hook", "name": "chassis.compartments", "value": "none"}], hooks)
    with pytest.raises(O.MissingHook):
        O.apply(_raw(), [{"op": "add", "part": {"id": "sv"}, "anchor": "nowhere"}], hooks)


def test_spec_applies_its_overlay():
    raw = _raw()
    raw["overlay"] = [{"op": "set", "select": {"id": "battery"}, "field": "connector", "value": "xt60"}]
    sp = Spec(raw)
    assert sp.part("battery")._extra.get("connector") == "xt60"


def test_swaps_read_catalog_live():
    """A catalog entry added later (e.g. a new battery in components.json) becomes a swap with no code change."""
    from robot import catalog

    extra = CatalogEntry("lipo_new_test", "battery", "New 2S pack", 10.0, "estimate", {"type": "box", "size": [1, 1, 1]})
    cat = list(catalog.catalog()) + [extra]
    ids = [c.id for c in C.swap_changes(_raw(), cat)]
    assert "swap:battery:battery->lipo_new_test" in ids
    assert any(i.startswith("swap:drive_motor:motor_l+motor_r->") for i in ids)  # paired parts swap together
    assert any(i.startswith("swap:connector:battery->xt30") for i in ids)


def test_arch_changes_hooks_fallbacks_and_missing():
    hooks = {"hooks": {"drive.driven_wheels": {"default": "4WD", "values": {"4WD": [], "2WD": []}}}, "anchors": {"deck": {"at": [0, 0, 0]}}}
    cs = {c.id: c for c in C.arch_changes(_raw(), hooks)}
    assert "arch:drive.driven_wheels=4WD" not in cs  # the robot's default is not a change
    assert cs["arch:drive.driven_wheels=2WD"].ops[0]["op"] == "hook"  # declared hook wins over the fallback
    assert cs["arch:battery.orientation=long_x"].ops[0]["op"] == "set"  # generic fallback
    assert "arch:battery.orientation=long_y" not in cs  # already long along Y
    assert "arch:add_servo@deck" in cs
    for h in ("chassis.compartments", "drive.location", "weapon.type"):
        assert any(c.hook == h and c.ops[0]["op"] == "hook" for c in cs.values()), h


def test_resolve_marks_missing_hooks_not_expressible():
    from robot.checks.robust import discover as D, hyp
    from robot.checks.robust.usage import Graph, Usage

    raw = _raw()
    hooks = {"hooks": {}, "anchors": {}}
    cs = C.change_hypotheses(raw, hooks)
    jobs, nx = hyp.resolve(cs, raw, hooks, D.Discovery(), Usage(Graph(), raw))
    nxh = {h for _, _, h in nx}
    assert {"chassis.compartments", "drive.location", "weapon.type"} <= nxh
    assert all(j.kind == "hyp" and j.overlay for _, j in jobs)


def test_score_and_report_with_fake_runs():
    from robot.checks.robust import hyp

    spec = ROOT / "robots" / "revron" / "spec.json"
    if not spec.exists():
        pytest.skip("revron spec missing")

    def fake(job, timeout):
        i = job.get("id")
        bl = [["interference.overlap", "battery,tub", "overlap"]] if "battery" in (i or "") else []
        return {"id": i, "blockers": bl, "seconds": 0.1}

    ev = hyp.evaluate(spec, 600, 2, 2, log=lambda *a: None, execute=fake)
    rows = hyp.verdicts(ev)
    s = hyp.score(rows)
    assert s["decided"] == len(rows) and 0 < s["pct"] < 100
    nx = [r for r in rows if r["verdict"] == "not expressible"]
    assert nx and all(r["diff"]["files"] for r in nx if r["hook"] in ("chassis.compartments", "weapon.type"))
    md = hyp.markdown(ev, rows)
    assert "Versatility score" in md and "Top missing hooks" in md


def test_revron_hooks_file_is_valid():
    hooks = O.load_hooks({}, ROOT / "robots" / "revron")
    if not hooks["hooks"]:
        pytest.skip("no hooks.json")
    raw = json.loads((ROOT / "robots" / "revron" / "spec.json").read_text())
    for name, h in hooks["hooks"].items():
        if isinstance(h.get("values"), dict):
            for v in h["values"]:
                O.apply(raw, [{"op": "hook", "name": name, "value": v}], hooks)
