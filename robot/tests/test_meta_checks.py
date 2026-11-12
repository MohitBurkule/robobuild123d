"""Meta-checks on the checks themselves (static: reads source with `ast`, builds no geometry).

A check that nobody tests, that gives no fix hint, or that no rule in GUIDE.md explains is weak for automated
development: the LLM gets a verdict it cannot trust or cannot act on. So every check module listed in STRICT must keep:

  * every finding id it emits is a plain string (no f-string ids: ids are the machine interface);
  * every finding id appears in a test file (bad case and good case live there);
  * every `fail(...)` carries a `.fix(...)` hint;
  * every finding id (or its `prefix.*`) is named in robot/GUIDE.md;
  * the module reports missing inputs through `ctx.not_checked` (never a silent pass);
  * no id is also emitted by another check module (one id, one owner);
  * the group is in the registry and its module file exists.

Older modules are not held to this yet. `legacy_gaps()` lists what they lack; when robot/tests/meta_baseline.json exists
(`{"untested": N, "no_fix": N}`) the count may only go down (ratchet).
"""

import ast
import json
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]          # robot/
CHECKS = ROOT / "checks"
TESTS = ROOT / "tests"
GUIDE = ROOT / "GUIDE.md"
BASELINE = TESTS / "meta_baseline.json"

# module file stem -> registry group name
STRICT = {"code_lint": "code", "geom_sanity": "geom", "spec_lint": "spec_lint", "waiver_audit": "waiver_audit",
          "swap_contract": "swap", "dfm": "dfm", "hardware": "hardware"}
EMIT = ("fail", "ok", "note")
HELPERS = {"__init__", "_review", "_physics", "registry", "waiver", "ref_diff", "ref_features", "ref_local", "ref_radii",
           "combat_ground"}   # not groups themselves: shared code used by groups


def _calls(tree):
    return [n for n in ast.walk(tree) if isinstance(n, ast.Call)]


def _name(call):
    f = call.func
    return f.id if isinstance(f, ast.Name) else (f.attr if isinstance(f, ast.Attribute) else None)


def emitted(path):
    """(ids {id: set of emitters}, dynamic [line], n_fail, n_fix) for one check source file."""
    tree = ast.parse(Path(path).read_text())
    ids, dynamic, n_fail, n_fix = {}, [], 0, 0
    for c in _calls(tree):
        nm = _name(c)
        if nm == "fix" and isinstance(c.func, ast.Attribute):
            n_fix += 1
        if nm not in EMIT or not isinstance(c.func, ast.Name) or not c.args:
            continue
        n_fail += nm == "fail"
        a = c.args[0]
        if isinstance(a, ast.Constant) and isinstance(a.value, str):
            ids.setdefault(a.value, set()).add(nm)
        else:
            dynamic.append(c.lineno)
    return ids, dynamic, n_fail, n_fix


def check_files():
    out = sorted(p for p in CHECKS.glob("*.py"))
    out += sorted(p for p in CHECKS.glob("*/*.py"))
    return out


def tests_text():
    return "\n".join(p.read_text() for p in sorted(TESTS.glob("test_*.py")) if p.name != Path(__file__).name)


def guide_mentions(guide, fid):
    """The id itself, or a wildcard for its prefix (`code.*`), is written in the guide."""
    return fid in guide or f"{fid.split('.')[0]}.*" in guide


def legacy_gaps():
    """{"untested": [id], "no_fix": [module]} over the check modules NOT in STRICT."""
    tt = tests_text()
    untested, no_fix = [], []
    for p in check_files():
        if p.stem in STRICT or p.stem in HELPERS:
            continue
        ids, _dyn, n_fail, n_fix = emitted(p)
        untested += [i for i in ids if i not in tt]
        if n_fail > n_fix:
            no_fix.append(f"{p.relative_to(ROOT)}: {n_fail} fail(), {n_fix} .fix()")
    return {"untested": sorted(set(untested)), "no_fix": no_fix}


@pytest.fixture(scope="module")
def strict():
    out = {}
    for stem in STRICT:
        p = CHECKS / f"{stem}.py"
        assert p.is_file(), f"strict check module missing: {p}"
        out[stem] = emitted(p)
    return out


def test_strict_modules_emit_plain_ids(strict):
    for stem, (ids, dynamic, _f, _x) in strict.items():
        assert ids, f"{stem}: emits no finding at all"
        assert not dynamic, f"{stem}: finding id built at run time on lines {dynamic}; ids must be plain strings"


def test_strict_ids_are_tested(strict):
    tt = tests_text()
    gaps = {stem: sorted(i for i in ids if i not in tt) for stem, (ids, *_r) in strict.items()}
    gaps = {k: v for k, v in gaps.items() if v}
    assert not gaps, f"finding ids with no test naming them (add a bad and a good case): {gaps}"


def test_strict_modules_have_their_own_test_file():
    for stem in STRICT:
        assert (TESTS / f"test_{stem}.py").is_file(), f"robot/tests/test_{stem}.py is missing"


def test_strict_fails_have_fix_hints(strict):
    bad = {stem: (n_fail, n_fix) for stem, (_i, _d, n_fail, n_fix) in strict.items() if n_fail > n_fix}
    assert not bad, f"modules with more fail() than .fix() calls (every failure needs a fix hint): {bad}"


def test_strict_ids_are_in_the_guide(strict):
    guide = GUIDE.read_text()
    gaps = {stem: sorted(i for i in ids if not guide_mentions(guide, i)) for stem, (ids, *_r) in strict.items()}
    gaps = {k: v for k, v in gaps.items() if v}
    assert not gaps, f"finding ids GUIDE.md never names (write the rule the builder must follow): {gaps}"


def test_strict_modules_report_not_checked():
    for stem in STRICT:
        src = (CHECKS / f"{stem}.py").read_text()
        assert "not_checked" in src, f"{stem}: never writes ctx.not_checked, so a missing input would read as a pass"


def test_strict_ids_have_one_owner(strict):
    owner = {}
    for p in check_files():
        if p.stem in HELPERS:
            continue
        for i in emitted(p)[0]:
            owner.setdefault(i, set()).add(p.stem)
    shared = {i: sorted(m) for i, m in owner.items() if len(m) > 1 and any(s in STRICT for s in m)}
    assert not shared, f"finding ids emitted by more than one module: {shared}"


def test_strict_groups_are_registered():
    src = (CHECKS / "registry.py").read_text()
    init = (CHECKS / "__init__.py").read_text()
    for stem, group in STRICT.items():
        assert f'_g("{group}"' in src, f"group `{group}` is not in checks/registry.py"
        if stem != group:
            assert f'"{group}": "{stem}"' in init, f"checks/__init__.py MODULE does not map `{group}` to {stem}.py"


def test_every_registered_group_has_a_module():
    tree = ast.parse((CHECKS / "registry.py").read_text())
    names = [c.args[0].value for c in _calls(tree) if _name(c) == "_g" and c.args and isinstance(c.args[0], ast.Constant)]
    assert len(names) == len(set(names)), "a group is registered twice"
    init = ast.parse((CHECKS / "__init__.py").read_text())
    module = {}
    for n in ast.walk(init):
        if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == "MODULE" for t in n.targets):
            module = ast.literal_eval(n.value)
    missing = [g for g in names if not ((CHECKS / f"{module.get(g, g)}.py").is_file() or (CHECKS / module.get(g, g)).is_dir())]
    assert not missing, f"registered groups with no module: {missing}"


def test_legacy_gaps_only_shrink():
    gaps = legacy_gaps()
    if not BASELINE.is_file():
        pytest.skip(f"no meta_baseline.json yet; legacy gaps now: {len(gaps['untested'])} untested ids, "
                    f"{len(gaps['no_fix'])} modules short of fix hints")
    base = json.loads(BASELINE.read_text())
    assert len(gaps["untested"]) <= base["untested"], f"new untested finding ids: {gaps['untested']}"
    assert len(gaps["no_fix"]) <= base["no_fix"], f"modules short of fix hints: {gaps['no_fix']}"
