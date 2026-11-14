"""`robot explain <finding-id>`: every check group and default-hint prefix is explained."""

from robot import fix_hints
from robot.checks import explain, registry


def test_every_registry_group_has_an_explanation():
    missing = [g.name for g in registry.REGISTRY if explain.explain(g.name + ".x")["prefix"] is None]
    assert missing == [], f"check groups with no explain entry: {missing}"


def test_every_fix_hint_prefix_has_an_explanation():
    prefixes = {k for k in fix_hints.DEFAULTS if k.endswith(".")}
    missing = [p for p in prefixes if explain.explain(p + "x")["prefix"] is None]
    assert missing == [], f"fix-hint prefixes with no explain entry: {missing}"


def test_longest_prefix_wins():
    e = explain.explain("interference.spin_clearance")
    assert e["prefix"] == "interference." and e["text"]


def test_exact_id_wins_over_prefix():
    explain.EXPLAIN["mass.special"] = "special case text"
    try:
        assert explain.explain("mass.special")["text"] == "special case text"
    finally:
        del explain.EXPLAIN["mass.special"]


def test_unknown_id_says_so():
    assert "no explanation" in explain.explain("totally.unknown_id")["text"]


def test_cli_module_exposes_add_cli():
    import importlib

    mod = importlib.import_module("robot.checks.explain")
    assert callable(mod.add_cli)
