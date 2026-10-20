"""[fix-G] Tests for the CI merge-gate decision function."""
import json, os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "tools"))
import ci_gate as G


def test_count():
    assert G.count_blockers("[BLOCKER] a.x\n[BLOCKER] a.y\nfoo: 2 blockers, 0 warnings") == 2
    assert G.count_blockers("Traceback\nKilled") == -1


def test_decide():
    assert G.decide(3, 3, 5, 4)
    assert G.decide(3, 2, 5, 5)
    assert not G.decide(3, 4, 5, 5)
    assert not G.decide(3, 3, 5, 6)
    assert not G.decide(3, -1, 5, 5)      # trial crashed while baseline finished
    assert not G.decide(-1, 7, 5, 5)      # unknown baseline: never an accept (review #1)
    assert not G.decide(-1, 50, -1, 50) and not G.decide(3, 3, -1, 99)
    assert not G.decide(3, 3, 5, -1)


def test_kind_and_owner():
    assert G.verifier_only(["robot/checks/a.py", "docs/x.md"])
    assert not G.verifier_only(["robot/checks/a.py", "robots/revron/src/build_revron.py"])
    assert G.owner("origin/fix-B2") == "B" and G.owner("fix-c-param") == "C"


def test_reject_logs(tmp_path):
    assert G.main(["decide", "origin/fix-B", "abc1234", "2", "3", "4", "4", str(tmp_path)]) == 1
    log = (tmp_path / "builder.log").read_text()
    assert "[ci] gate rejected fix-B abc1234: assembly 2->3, interference 4->4" in log
    row = json.loads((tmp_path / "blockers_live_B.jsonl").read_text())
    assert row["group"] == "ci_gate" and row["assembly"] == [2, 3]
    assert G.main(["decide", "fix-B", "abc", "2", "2", "4", "4", str(tmp_path)]) == 0


def test_halves():
    assert G.halves(["a", "b", "c"]) == (["a", "b"], ["c"])
    assert G.halves(["a"]) == (["a"], [])


def _gate(bad, infra=()):
    calls = []
    def g(s):
        calls.append(tuple(s))
        if any(b in infra for b in s):
            return None
        return not any(b in bad for b in s)
    return g, calls


def test_bisect_all_pass_one_trial():
    g, calls = _gate(set())
    assert G.bisect(list("abcde"), g) == {b: "pass" for b in "abcde"}
    assert calls == [tuple("abcde")]


def test_bisect_finds_offenders():
    g, _ = _gate({"b", "e"})
    r = G.bisect(list("abcde"), g)
    assert [b for b, v in r.items() if v == "reject"] == ["b", "e"]
    assert all(r[b] == "pass" for b in "acd")


def test_bisect_infra_holds():
    g, _ = _gate(set(), infra={"d"})
    assert G.bisect(list("abcd"), g) == {b: "hold" for b in "abcd"}   # infra on the union: nothing merges
    calls = iter([False, True, None])                                  # union worse, half 1 ok, half 2 infra
    assert G.bisect(list("abcd"), lambda s: next(calls)) == {"a": "pass", "b": "pass", "c": "hold", "d": "hold"}


def test_bisect_interaction_holds_second_half():
    g = lambda s: not ({"a", "c"} <= set(s))
    r = G.bisect(list("abcd"), g)
    assert r == {"a": "pass", "b": "pass", "c": "hold", "d": "hold"}


def test_ok_cli():
    assert G.main(["ok", "3", "3", "5", "5"]) == 0
    assert G.main(["ok", "3", "4", "5", "5"]) == 1
