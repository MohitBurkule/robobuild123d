"""Reference-copy mode relaxes our combat-effectiveness taste, never physical validity."""

from types import SimpleNamespace

from robot.checks import copymode
from robot.finding import BLOCKER, WARNING, Finding


def _f(fid, group, sev=BLOCKER, passed=False):
    return Finding(id=fid, group=group, severity=sev, passed=passed, title="t", message="m", parts=["drum"])


def test_copy_downgrades_combat_blockers_only():
    spec = SimpleNamespace(raw={"reference_copy": {"robot": "Baphomet", "source": "AWS wiki photos"}})
    reach = _f("spinner.reach", "spinner")
    lead = _f("shape.weapon_leads", "shape")
    inter = _f("interference.overlap", "interference")
    mass = _f("mass.total", "mass")
    used = copymode.apply(spec, [reach, lead, inter, mass])
    assert reach.severity == WARNING and "not enforced" in reach.message
    assert lead.severity == WARNING
    assert inter.severity == BLOCKER and mass.severity == BLOCKER
    assert {u["check"] for u in used} == {"spinner.reach", "shape.weapon_leads"}


def test_own_robot_keeps_every_rule():
    spec = SimpleNamespace(raw={})
    reach = _f("spinner.reach", "spinner")
    assert copymode.apply(spec, [reach]) == [] and reach.severity == BLOCKER


def test_passed_findings_untouched():
    spec = SimpleNamespace(raw={"reference_copy": True})
    ok = _f("spinner.reach", "spinner", sev=WARNING, passed=True)
    assert copymode.apply(spec, [ok]) == [] and ok.message == "m"
