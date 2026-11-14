"""Check-group registry (robot/checks/registry.py): kind (design | parity), tier (inner | full | nightly), the design
gate vs the parity score, and the `robot verify --tier / --no-parity / --parity-only / --combined` flags."""

import importlib
import json

import pytest

from robot import checks, cli, proxy, spec
from robot.checks import Options, registry, verify
from robot.finding import BLOCKER, Report, fail, ok


def _spec(name="tier_probe"):
    return {"name": name, "parts": [{"id": "plate", "kind": "structure", "shape": {"type": "box", "size": [40, 30, 4]},
                                     "at": [0, 0, 2], "material": "petg", "process": "fdm"}]}


@pytest.fixture
def nocache(monkeypatch):
    """Group results are cached by spec + sources, which cannot see a monkeypatched `run`: keep these runs out."""
    from robot import cache

    was = cache.enabled()
    monkeypatch.setenv("ROBOT_PROGRESS", "0")  # cli.main turns progress printing on for the process: undo it after
    cache.set_enabled(False)
    yield
    cache.set_enabled(was)


@pytest.fixture
def parity_blocker(monkeypatch, nocache):
    """The parity group `ref_map` reports one blocker, as on a new robot that has no reference to match."""
    from robot.checks import ref_map

    monkeypatch.setattr(ref_map, "run", lambda ctx: [fail("reference.unmapped_part", "reference", BLOCKER, "No reference part",
                                                          "`plate` maps to no reference part.").on("plate")])


# registry
def test_every_group_has_kind_and_tier():
    names = [g.name for g in registry.REGISTRY]
    assert len(names) == len(set(names)) and len(names) >= 55
    assert [n for n, _ in checks.GROUPS] == names  # GROUPS is a view of the registry, nothing registered elsewhere
    for g in registry.REGISTRY:
        assert g.kind in registry.KINDS, g.name
        assert g.tier in registry.TIERS, g.name
        assert g.proxy is None or g.proxy in proxy.GROUPS, g.name
        importlib.import_module(f"robot.checks.{checks.MODULE.get(g.name, g.name)}")  # a registered group exists
    assert {g.name: d for g in registry.REGISTRY for d in [g.deep_only] if d} == {"wiring": True, "assembly": True, "robust": True}


def test_reference_comparisons_are_parity_and_never_cheap_tiers():
    par = {g.name for g in registry.REGISTRY if g.kind == registry.PARITY}
    assert par == {"reference", "reference_ratios", "reference_cad", "ref_map", "visual", "sldprt_dump", "asm_dump"}
    assert all(registry.INFO[n].tier == registry.NIGHTLY for n in par)
    assert registry.INFO["practice"].kind == registry.DESIGN  # "best practice with NO reference"
    assert registry.INFO["robust"].tier == registry.NIGHTLY


def test_single_findings_of_design_groups_can_be_parity():
    assert registry.kind_of("bom", "reference.bom") == registry.PARITY
    assert registry.kind_of("bom", "kin.belt_stock") == registry.DESIGN
    assert registry.kind_of("cots_fidelity", "cots.motor_volume") == registry.PARITY
    assert registry.kind_of("cots_fidelity", "cots.fidelity") == registry.DESIGN
    assert registry.kind_of("visual", "anything") == registry.PARITY
    assert registry.kind_of("claims", "claim.false") == registry.DESIGN


def test_inner_tier_is_cheap_on_the_logged_revron_times():
    inner = [g for g in registry.REGISTRY if g.tier == registry.INNER]
    assert sum(g.ref_s or 0 for g in inner) < 60
    assert all((g.ref_s or 0) < 10 for g in inner)


def test_select_by_tier_and_parity():
    inner, full, night = (registry.select(t) for t in registry.TIERS)
    assert set(inner.run) == {g.name for g in registry.REGISTRY if g.tier == "inner"}
    assert set(inner.proxies) == {"wiring", "interference", "assembly"}  # slow design groups with a stand-in
    assert "reference_cad" not in inner.proxies  # parity: not part of the inner loop
    assert not set(full.run) & {"robust", "visual", "reference_cad", "sldprt_dump", "asm_dump"} and not full.proxies
    assert {"intent", "mfg", "interference", "assembly"} <= set(full.run)
    assert night.run == [g.name for g in registry.REGISTRY] and not night.not_run
    # every registered group is either run, proxied or listed as not run
    for s in (inner, full, night):
        assert sorted(s.run + s.proxies + [x["group"] for x in s.not_run]) == sorted(registry.INFO)
    assert all(registry.INFO[n].kind == "design" for n in registry.select("nightly", "no").run)
    assert set(registry.select(None, "only").run) == {g.name for g in registry.REGISTRY if g.kind == "parity"}
    plain = registry.select()
    assert plain.run == night.run and not plain.filtered  # library default: every group, as before
    assert registry.select("nightly", only=["mfg"]).run == ["mfg"]  # --only wins
    assert "wiring" not in registry.select("full", deep=False).run
    with pytest.raises(ValueError):
        registry.select("hourly")


# gate
def test_report_gate_counts_design_only():
    rep = Report(findings=[ok("a.ok", "a", "t", "m"), fail("visual.silhouette", "visual", BLOCKER, "t", "m")])
    rep.findings[1].kind = "parity"
    rep.finish()
    assert rep.ok and rep.summary["blockers"] == 0 and rep.design == {"blockers": 0, "warnings": 0, "passed": 1, "total": 1, "ok": True}
    assert rep.parity["blockers"] == 1 and rep.parity["score"] == 0.0 and not rep.parity["gating"]
    rep.finish(combined=True)
    assert not rep.ok and rep.summary["blockers"] == 1 and rep.gate == "combined" and rep.parity["gating"]
    d = rep.to_dict()
    assert d["findings"][1]["kind"] == "parity" and d["parity"]["failing_ids"] == ["visual.silhouette"] and d["gate"] == "combined"


def test_design_blocker_still_fails_the_gate():
    rep = Report(findings=[fail("mfg.thin_wall", "mfg", BLOCKER, "t", "m")])
    rep.finish()
    assert not rep.ok and rep.summary["blockers"] == 1 and rep.parity["total"] == 0 and rep.parity["score"] is None


def test_parity_blocker_does_not_flip_ok(parity_blocker):
    rep = verify(spec.Spec(_spec()), Options(fast=True, only=["mass", "ref_map"]))
    f = rep.get("reference.unmapped_part")
    assert f is not None and not f.passed and f.kind == "parity"
    assert rep.ok and rep.summary["blockers"] == 0 and rep.design["ok"]
    assert rep.parity["blockers"] == 1 and rep.parity["groups_total"] == 1 and rep.parity["groups_clean"] == 0
    assert rep.groups["ref_map"]["kind"] == "parity" and rep.groups["ref_map"]["blockers"] == 1
    assert rep.groups["mass"]["kind"] == "design" and rep.groups["mass"]["time_s"] is not None


def test_combined_gate_reproduces_the_old_result(parity_blocker):
    new = verify(spec.Spec(_spec()), Options(fast=True, only=["mass", "ref_map"]))
    old = verify(spec.Spec(_spec()), Options(fast=True, only=["mass", "ref_map"], combined=True))
    assert not old.ok and old.gate == "combined"
    # the old rule: every finding counts, ok = no blocker at all
    b = sum(1 for f in old.findings if not f.passed and f.severity == BLOCKER)
    assert old.summary["blockers"] == b == 1 and old.summary["total"] == len(old.findings)
    assert [(f.id, f.passed, f.severity) for f in old.findings] == [(f.id, f.passed, f.severity) for f in new.findings]


def test_crashed_parity_group_is_a_parity_blocker(monkeypatch, nocache):
    from robot.checks import mass, ref_map

    monkeypatch.setattr(ref_map, "run", lambda ctx: 1 / 0)
    rep = verify(spec.Spec(_spec()), Options(fast=True, only=["mass", "ref_map"]))
    assert rep.failed("checks.crashed") and rep.ok and rep.parity["blockers"] == 1 and rep.groups["ref_map"]["how"] == "crashed"
    monkeypatch.setattr(mass, "run", lambda ctx: 1 / 0)  # a crashed DESIGN group still fails closed
    assert not verify(spec.Spec(_spec()), Options(fast=True, only=["mass"])).ok


# tiers end to end
def test_tier_inner_runs_only_inner_groups(nocache):
    rep = verify(spec.Spec(_spec()), Options(fast=True, tier="inner"))
    inner = {g.name for g in registry.REGISTRY if g.tier == "inner"}
    full_ran = {n for n, g in rep.groups.items() if g["how"] != "proxy"}
    assert full_ran == inner and rep.tier == "inner"
    proxied = {n for n, g in rep.groups.items() if g["how"] == "proxy"}
    assert "interference" in proxied and proxied <= {"interference", "wiring", "assembly"}
    assert "proxy.interference" in rep.timings_s and "interference" not in rep.timings_s
    skipped = {x["group"] for x in rep.not_run}
    assert {"mfg", "intent", "visual", "robust", "reference_cad"} <= skipped and not skipped & set(rep.groups)
    assert skipped | set(rep.groups) == set(registry.INFO)  # nothing dropped silently
    assert any(x.startswith("NOT RUN in this tier") for x in rep.not_checked)
    assert any("judged by its fast proxy" in x for x in rep.not_checked)
    assert all(f.kind == "design" for f in rep.findings)


def test_cli_tier_inner_report(tmp_path, capsys, nocache):
    p = tmp_path / "spec.json"
    p.write_text(json.dumps(_spec("tier_cli")))
    out_json = tmp_path / "report.json"
    rc = cli.main(["verify", str(p), "--tier", "inner", "--fast", "--json", str(out_json)])
    out = capsys.readouterr().out
    d = json.loads(out_json.read_text())
    assert rc == (0 if d["ok"] else 2)
    assert d["tier"] == "inner" and d["gate"] == "design" and d["design"]["ok"] == d["ok"]
    assert set(d["groups"]) - {"interference", "wiring", "assembly"} == {g.name for g in registry.REGISTRY if g.tier == "inner"}
    assert all(g["time_s"] is not None and g["tier"] and g["kind"] for g in d["groups"].values())
    assert {"group", "kind", "tier", "reason"} == set(d["not_run"][0])
    assert "gate: design" in out and "tier inner" in out and "NOT RUN in this tier" in out and "groups run (" in out
    assert "parity vs reference: not run" in out


def test_cli_default_gate_vs_combined(tmp_path, capsys, parity_blocker):
    p = tmp_path / "spec.json"
    p.write_text(json.dumps(_spec("tier_cli_gate")))
    assert cli.main(["verify", str(p), "--fast", "--only", "mass,ref_map"]) == 0  # the parity blocker does not gate
    out = capsys.readouterr().out
    assert "[parity blocker] reference.unmapped_part" in out and "[BLOCKER]" not in out
    assert "0 blockers," in out and "ok=True" in out and "1 parity blockers" in out and "[not gating]" in out
    assert cli.main(["verify", str(p), "--fast", "--only", "mass,ref_map", "--combined"]) == 2  # the old exit code
    out = capsys.readouterr().out
    assert "[BLOCKER] reference.unmapped_part" in out and "1 blockers," in out and "ok=False" in out  # what ci_gate.py counts
    assert "gate: combined" in out


def test_cli_flags_pick_tier_and_parity():
    def o(*flags):
        ap = type("A", (), {"quick": False, "fast": False, "only": None, "tier": None, "combined": False,
                            "no_parity": False, "parity_only": False})()
        for k, v in flags:
            setattr(ap, k, v)
        return cli.opts_from(ap)

    assert (o().tier, o().parity, o().combined) == ("full", "both", False)  # default: the full design tier
    assert o(("tier", "nightly")).tier == "nightly"
    assert o(("combined", True)).tier is None and o(("combined", True)).combined  # old: every group, every blocker
    assert o(("only", "mfg")).tier is None
    assert (o(("parity_only", True)).parity, o(("parity_only", True)).tier) == ("only", None)
    assert o(("no_parity", True), ("tier", "nightly")).parity == "no"
    with pytest.raises(SystemExit):
        cli.main(["verify", "x.json", "--no-parity", "--parity-only"])
    with pytest.raises(SystemExit):
        cli.main(["verify", "x.json", "--tier", "hourly"])


def test_ci_scripts_keep_the_combined_gate():
    """The CI loop counts every `[BLOCKER]` line of every group: its verify calls must ask for the old gate."""
    from pathlib import Path

    tools = Path(cli.__file__).parent / "tools"
    for name in ("shard_worker.sh", "ci_loop.sh"):
        for line in (tools / name).read_text().splitlines():
            if "-m robot verify" in line and "--only" in line:
                assert "--combined" in line, f"{name}: {line.strip()[:120]}"
