"""Builder profile check (robot/checks/builder.py): design vs the builder's bench."""

from types import SimpleNamespace

import pytest

from robot import builder as builder_mod
from robot.checks import builder


TINY = {"id": "tiny", "name": "Tiny bench", "printer": "ender3", "materials": ["pla"], "processes": ["fdm"],
        "tools": ["hex_driver"], "budget_gbp": 100.0, "skill": "novice"}


def _rp(pid, kind="structure", material="pla", process="fdm", bounds=(0, 0, 0, 50, 40, 20), extra=None):
    import numpy as np
    return SimpleNamespace(part=SimpleNamespace(id=pid, kind=kind, material=material, process=process,
                                               _extra=dict(extra or {}, **({"print_orientation": "+z"} if process == "fdm" else {}))),
                          cat=None, geom=SimpleNamespace(bounds=np.array([[bounds[0], bounds[1], bounds[2]],
                                                                        [bounds[3], bounds[4], bounds[5]]], float)))


def _ctx(raw, rparts, fasteners=()):
    return SimpleNamespace(r=SimpleNamespace(spec=SimpleNamespace(raw=raw, fasteners=list(fasteners)), parts=rparts),
                           world=SimpleNamespace(bodies=[]), not_checked=[], metrics={})


def test_no_builder_key_is_not_checked():
    ctx = _ctx({}, [_rp("chassis")])
    assert builder.run(ctx) == []
    assert any("no `builder` profile" in x for x in ctx.not_checked)


def test_unknown_preset_warns():
    ctx = _ctx({"builder": "no_such_bench"}, [_rp("chassis")])
    out = builder.run(ctx)
    assert "builder.unknown" in [f.id for f in out]
    f = next(f for f in out if f.id == "builder.unknown")
    assert f.severity == "warning" and f.fix_hint


def test_bed_too_small_blocks_the_chassis():
    big = _rp("chassis", bounds=(0, 0, 0, 300, 300, 40))
    ctx = _ctx({"builder": TINY}, [big])
    out = builder.run(ctx)
    assert "builder.bed_fit" in [f.id for f in out]
    f = next(f for f in out if f.id == "builder.bed_fit")
    assert f.severity == "warning" and "300 x 300" in f.message and f.fix_hint


def test_part_fits_the_bed_passes():
    ctx = _ctx({"builder": TINY}, [_rp("chassis")])
    out = builder.run(ctx)
    assert [f.id for f in out] == ["builder.ok"]


def test_material_off_the_shelf_warns():
    ctx = _ctx({"builder": TINY}, [_rp("tyre", material="tpu")])
    out = builder.run(ctx)
    assert "builder.material_unavailable" in [f.id for f in out]
    f = next(f for f in out if f.id == "builder.material_unavailable")
    assert f.severity == "warning" and f.fix_hint


def test_process_unavailable_warns():
    ctx = _ctx({"builder": TINY}, [_rp("plate", material="aluminium", process="cnc")])
    out = builder.run(ctx)
    assert "builder.process_unavailable" in [f.id for f in out]


def test_inserts_need_a_soldering_iron():
    ctx = _ctx({"builder": TINY}, [_rp("chassis"), _rp("ins1", kind="insert", material="brass", process=None)])
    out = builder.run(ctx)
    assert "builder.tool_missing" in [f.id for f in out]
    assert "builder.skill" in [f.id for f in out]  # heat-set inserts are past novice too


def test_inserts_pass_with_iron_and_skill():
    bench = dict(TINY, tools=["hex_driver", "soldering_iron"], skill="intermediate", materials=["pla", "brass"])
    ctx = _ctx({"builder": bench}, [_rp("chassis"), _rp("ins1", kind="insert", material="brass", process=None)])
    out = builder.run(ctx)
    assert [f.id for f in out] == ["builder.ok"]


def test_machined_parts_need_expert_skill():
    bench = dict(TINY, materials=["pla", "aluminium"], processes=["fdm", "cnc"], skill="intermediate")
    ctx = _ctx({"builder": bench}, [_rp("plate", material="aluminium", process="cnc")])
    out = builder.run(ctx)
    assert "builder.skill" in [f.id for f in out]


def test_budget_over_warns(monkeypatch):
    monkeypatch.setattr("robot.checks.builder.bom_out.cost", lambda lines: 95.0)
    ctx = _ctx({"builder": dict(TINY, budget_gbp=50.0)}, [_rp("chassis")])
    out = builder.run(ctx)
    assert "builder.budget" in [f.id for f in out]
    assert ctx.metrics["bom_cost_gbp"] == 95.0


def test_budget_within_passes(monkeypatch):
    monkeypatch.setattr("robot.checks.builder.bom_out.cost", lambda lines: 95.0)
    ctx = _ctx({"builder": TINY}, [_rp("chassis")])
    out = builder.run(ctx)
    assert [f.id for f in out] == ["builder.ok"]


def test_presets_load_and_validate():
    for pid in ("novice_ender3", "club_member", "expert"):
        b = builder_mod.load(pid)
        assert b.printer and b.skill in builder_mod.SKILLS and b.materials
    with pytest.raises(KeyError):
        builder_mod.load("no_such_bench")


def test_negative_print_orientation_does_not_crash():
    import numpy as np
    rp = _rp("fin", bounds=(0, 0, 0, 50, 40, 20))
    rp.part._extra["print_orientation"] = "-z"
    ctx = _ctx({"builder": TINY}, [rp])
    out = builder.run(ctx)
    assert "builder.ok" in [f.id for f in out]
