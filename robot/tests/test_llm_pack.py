"""Generated LLM pack (B7, robot/llm_pack.py): content from live sources + drift vs llm/."""

import json
from pathlib import Path

from robot import llm_pack


def test_generate_is_deterministic():
    assert llm_pack.generate() == llm_pack.generate()


def test_skill_lists_live_sources():
    from robot.checks import registry
    skill = llm_pack.generate()["SKILL.md"]
    assert "mass.over" in skill and "robot llm-report" in skill
    for g in [g for g in registry.REGISTRY if g.kind == registry.DESIGN]:
        assert f"`{g.name}`" in skill, g.name
    for n in ("aws2025", "dev", "strict"):
        assert n in skill
    for rel in ("examples/wedge_2wd.spec.json", "examples/compact_report.json", "examples/patch_roundtrip.json"):
        assert rel in skill


def test_example_spec_is_the_template():
    t = json.loads((Path(robot_dir := Path(llm_pack.__file__).parent) / "templates" / "wedge_2wd.json").read_text())
    assert json.loads(llm_pack.generate()["examples/wedge_2wd.spec.json"]) == t


def test_example_compact_has_blockers_with_fixes():
    c = json.loads(llm_pack.generate()["examples/compact_report.json"])
    assert c["counts"]["blockers"] == 2 and c["counts"]["warnings"] == 1
    assert c["blockers"][0]["id"] == "mass.over" and c["blockers"][0]["fixes"]


def test_example_patch_applies_cleanly():
    d = json.loads(llm_pack.generate()["examples/patch_roundtrip.json"])
    assert d["errors"] == []
    assert d["design_after"]["drive"]["motor"] == "n20_2000rpm_6v"
    assert d["design_after"]["body"]["zt"] == 10.0
    assert "profile" not in d["design_after"]


def test_write_creates_all_files(tmp_path):
    files = llm_pack.write(tmp_path)
    assert files == ["SKILL.md", "examples/compact_report.json", "examples/patch_roundtrip.json",
                     "examples/wedge_2wd.spec.json"]
    for rel in files:
        assert (tmp_path / rel).exists()


def test_drift_checked_in_pack_matches_generator():
    """The pack in llm/ must be regenerated whenever the verifier changes."""
    assert llm_pack.CHECKED_IN.is_dir(), "llm/ pack is not checked in"
    gen = llm_pack.generate()
    checked = {rel: (llm_pack.CHECKED_IN / rel).read_text() for rel in gen}
    if checked != gen:
        missing = sorted(set(gen) - set(checked))
        stale = sorted(rel for rel in gen if rel in checked and checked[rel] != gen[rel])
        raise AssertionError(f"llm/ pack is stale (missing: {missing}, stale: {stale}); "
                             f"run `python3 -m robot llm-pack llm`")
