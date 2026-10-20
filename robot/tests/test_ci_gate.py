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
    assert G.decide(-1, 7, 5, 5)          # unknown baseline: do not block on it


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
