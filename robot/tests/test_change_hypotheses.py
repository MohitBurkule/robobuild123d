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


def test_size_changes_master_proxy_and_missing():
    from robot.checks.robust import plan as P
    from robot.checks.robust.discover import Param
    from robot.checks.robust.usage import Graph, Usage

    params = [Param("W", "W", 30.0, Path("p.py"), 1, 4, 8), Param("Y0", "Y0", -37.6, Path("p.py"), 2, 5, 10)]
    hooks = {"sizes": {"width": {"param": "W"}, "length": {"proxy": "Y0"}}}
    cs = C.size_changes(hooks, params, Usage(Graph(), {}), P)
    ids = {c.id for c in cs}
    assert sum(i.startswith("size:width:") for i in ids) == 6  # +-10/20/30 % on the master
    assert not any(i.startswith("size:width") and "%" in i and ":" not in i[5:] for i in ids)
    assert sum(c.hook == "size.length" and c.job is None for c in cs) == 7  # 6 steps + short 2WD, missing hook
    assert sum(i.startswith("size:length(proxy):") for i in ids) == 6
    assert all(c.hook == "size.height" for c in cs if c.id.startswith("size:height"))


def test_wheel_swap_removes_hub_and_reseats_on_axle():
    raw = {"parts": [
        {"id": "tub", "kind": "structure"},
        {"id": "motor_l", "kind": "motor", "catalog": "n10_2200rpm_spicy"},
        {"id": "whub_rl", "kind": "pulley", "parent": "tub", "at": [30.0, -30.5, 0.0], "rot": [-180.0, 0.0, 0.0],
         "joint": {"kind": "revolute", "axis": [1, 0, 0]}, "rotates_with": "wheel_rl", "shape": {"type": "model"}},
        {"id": "wheel_rl", "kind": "wheel", "parent": "whub_rl", "tyre_of": "whub_rl", "at": [2.5, 1.0, 0.0], "rot": [0, 0, 0],
         "rotates_with": "wheel_rl", "shape": {"type": "model"}}],
        "connections": [{"a": "whub_rl", "b": "motor_l", "method": "press_fit", "interference_mm": 0.05},
                        {"a": "wheel_rl", "b": "whub_rl", "method": "press_fit"}]}
    out = O.apply(raw, [{"op": "wheel", "select": {"id": "wheel_rl"}, "to": "wheel_20x8"}], hooks={})
    ids = [p["id"] for p in out["parts"]]
    assert "whub_rl" not in ids
    w = O.select(out, {"id": "wheel_rl"})[0]
    assert w["catalog"] == "wheel_20x8" and "shape" not in w and "tyre_of" not in w
    assert w["parent"] == "tub" and w["joint"]["kind"] == "revolute"
    assert w["at"] == pytest.approx([32.5, -31.5, 0.0])  # hub pose (rx 180 flips y) composed with the tyre offset
    import numpy as np
    from robot import xform
    assert np.allclose(xform.euler(w["rot"]), xform.euler([-180, 0, 0]))
    assert out["connections"] == [{"a": "wheel_rl", "b": "motor_l", "method": "press_fit",
                                   "reason": "[wheel swap] catalog wheel hub takes over: "}]
    assert all(c.ops[0]["op"] == "wheel" for c in C.swap_changes(json.loads(json.dumps(
        {"parts": [dict(p, stock="tyre") for p in raw["parts"] if p["kind"] == "wheel"]}))))


def test_swap_uses_declared_build_setting_and_any_env_value(tmp_path):
    from robot.checks.robust import discover as D, hyp
    from robot.checks.robust.usage import Graph, Usage

    hooks = {"hooks": {"drive.motor": {"env": "X_DRIVE_MOTOR", "swap": "drive_motor"}}}
    cs = [c for c in C.swap_changes(_raw(), None, hooks) if c.id.startswith("swap:drive_motor:")]
    assert cs and all(c.ops == [{"op": "hook", "name": "drive.motor", "value": c.id.split("->")[1]}] for c in cs)
    src = tmp_path / "params_x.py"
    src.write_text('import os\nDRIVE_MOTOR = os.environ.get("X_DRIVE_MOTOR", "n10_2200rpm_spicy")\n')
    sw = D.env_setting([src], "X_DRIVE_MOTOR")
    assert sw.symbol == "DRIVE_MOTOR" and sw.default == "n10_2200rpm_spicy"
    jobs, nx = hyp.resolve(cs[:1], _raw(), hooks, D.Discovery(), Usage(Graph(), _raw()), [src])
    assert not nx
    j = jobs[0][1]
    assert j.kind == "choice" and j.new_text == repr(cs[0].id.split("->")[1])
    assert j.env == {"X_DRIVE_MOTOR": cs[0].id.split("->")[1]}  # code reading os.environ itself sees the setting too


def test_swap_setting_limited_to_its_parts():
    raw = {"parts": [{"id": i, "kind": "wheel", "stock": s, "shape": {"type": "model"}}
                     for i, s in (("wheel_rl", "rear"), ("wheel_rr", "rear"), ("wheel_fl", "front"), ("wheel_fr", "front"))]}
    hooks = {"hooks": {"wheel.rear": {"env": "W", "swap": "wheel", "parts": ["wheel_rl", "wheel_rr"], "values": ["stock", "wheel_20x8"]},
                       "drive.belt": {"values": {"o_ring": [], "none": []}}}}
    cs = {c.id: c for c in C.swap_changes(raw, None, hooks)}
    assert cs["swap:wheel:wheel_rl+wheel_rr->wheel_20x8"].ops[0] == {"op": "hook", "name": "wheel.rear", "value": "wheel_20x8"}
    assert cs["swap:wheel:wheel_rl+wheel_rr->wheel_28x10"].ops[0]["op"] == "wheel"  # not offered by the setting
    assert cs["swap:wheel:wheel_fl+wheel_fr->wheel_20x8"].ops[0]["op"] == "wheel"


def test_wheel_swap_sets_belt_none_and_wheel_od(tmp_path):
    from robot.checks.robust import discover as D, hyp
    from robot.checks.robust.usage import Graph, Usage

    raw = {"parts": [{"id": i, "kind": "wheel", "stock": "micro tyre", "shape": {"type": "model"}} for i in ("wheel_fl", "wheel_fr")]}
    hooks = {"hooks": {"drive.belt": {"default": "o_ring", "values": {"o_ring": [], "none": [{"op": "remove", "select": {"kind": "belt"}}]}}},
             "wheel_od": {"wheel_f*": "WHEEL_OD_F"}}
    cs = [c for c in C.swap_changes(raw, None, hooks) if c.id.endswith("->wheel_20x8")]
    c = cs[0]
    assert c.ops[0]["op"] == "wheel" and {"op": "hook", "name": "drive.belt", "value": "none"} in c.ops
    assert c.param_set == ("WHEEL_OD_F", 20.0)
    src = tmp_path / "params_chassis.py"
    src.write_text("WHEEL_OD_F = 11.0\n")
    disc = D.Discovery(params=D.params_in_file(src)[0])
    jobs, nx = hyp.resolve([c], raw, hooks, disc, Usage(Graph(), raw), [src])
    assert not nx
    j = jobs[0][1]
    assert j.kind == "param" and j.new_text == "20.0" and any(o["op"] == "remove" for o in j.overlay)


def test_size_changes_use_declared_size_settings():
    from robot.checks.robust import plan as P
    from robot.checks.robust.usage import Graph, Usage

    steps = ["-30%", "-20%", "-10%", "10%", "20%", "30%"]
    hooks = {"hooks": {f"size.{d}": {"env": f"S_{d}", "values": steps, "default": "0"} for d in ("width", "length", "height")}}
    cs = C.size_changes(hooks, [], Usage(Graph(), {}), P)
    vals = sorted(c.ops[0]["value"] for c in cs if c.id.startswith("size:width"))
    assert vals == sorted(steps)  # the robot's own spelling ("10%", "-10%")
    for c in cs:
        for op in c.ops:
            if op["op"] == "hook" and op["name"].startswith("size."):
                O.expand(op, hooks)  # every step is a declared value: no MissingHook


def test_worker_passes_settings_to_generation(tmp_path, monkeypatch):
    """A setting read straight from os.environ (not through the edited default) must reach the spec generation."""
    from robot.checks.robust import worker

    m = tmp_path / "m.py"
    m.write_text("import os, json, pathlib\npathlib.Path(__file__).with_name('spec.json').write_text(json.dumps({'w': os.environ.get('REVRON_X', '0')}))\n")
    monkeypatch.setenv("REVRON_X", "stale")
    assert worker.regenerate(tmp_path, "m.py", tmp_path, 60, {"REVRON_X": "30%"}) is None
    assert json.loads((tmp_path / "spec.json").read_text())["w"] == "30%"


def test_runner_resumes_from_results_folder(tmp_path, monkeypatch):
    from robot.checks.robust import plan as P, runner as R

    spec = tmp_path / "spec.json"
    spec.write_text("{}")
    monkeypatch.setenv("ROBOT_ROBUST_RESULTS", str(tmp_path / "res"))
    monkeypatch.setenv("ROBOT_NO_CACHE", "1")
    calls = []

    def ex(job, timeout):
        calls.append(job["id"])
        return {"id": job["id"], "blockers": [], "rebuilt": []}

    jobs = [P.Job("a", "a", "hyp", overlay=[{"op": "x"}])]
    R.run(jobs, spec, "m.py", 600, 1, execute=ex, src_hash="s", log=lambda *a: None)
    R.run(jobs, spec, "m.py", 600, 1, execute=ex, src_hash="s", log=lambda *a: None)
    assert calls == ["baseline", "a"]  # the second run reads every result back from the folder


def test_disk_full_is_not_a_verdict():
    from robot.checks.robust import runner as R

    for res in ({"error": "spec generation failed (rc 1): OSError: [Errno 28] No space left on device", "stage": "build"},
                {"error": "Error: [('a', 'b', \"[Errno 28] No space left on device\")]", "stage": "worker"}):
        d = R.diff({"blockers": []}, res, "param")
        assert not d["broken"] and d["infra"]
    assert R.diff({"blockers": []}, {"error": "ValueError: math domain error", "stage": "build"})["broken"]


def test_geometry_key_includes_declared_setting_env(monkeypatch, tmp_path):
    from robot import geom

    m = tmp_path / "m.py"
    m.write_text("x = 1\n")
    sh = {"type": "model", "file": str(m), "params": {"part": "p"}}
    monkeypatch.delenv("ROBOT_CACHE_ENV", raising=False)
    k0 = geom.key_for(sh, tmp_path)
    monkeypatch.setenv("ROBOT_CACHE_ENV", "REVRON_SIZE_WIDTH")
    monkeypatch.setenv("REVRON_SIZE_WIDTH", "10%")
    k1 = geom.key_for(sh, tmp_path)
    monkeypatch.setenv("REVRON_SIZE_WIDTH", "20%")
    assert len({k0, k1, geom.key_for(sh, tmp_path)}) == 3  # a part built under another setting is another part
