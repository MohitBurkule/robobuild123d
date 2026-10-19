from robot import progress


def test_progress_log_appends_when_set(tmp_path, monkeypatch):
    f = tmp_path / "p.log"
    monkeypatch.setenv("ROBOT_PROGRESS_LOG", str(f))
    progress.log("check mfg ran; blockers so far 3")
    progress.log("part tub built")
    lines = f.read_text().splitlines()
    assert len(lines) == 2 and lines[0].endswith("blockers so far 3") and "part tub built" in lines[1]


def test_progress_log_off_by_default(tmp_path, monkeypatch):
    monkeypatch.delenv("ROBOT_PROGRESS_LOG", raising=False)
    progress.log("nothing")
    assert not list(tmp_path.iterdir())


def test_check_groups_log_blocker_counts(tmp_path, monkeypatch):
    from robot.checks import _progress
    from robot.finding import BLOCKER, fail
    f = tmp_path / "p.log"
    monkeypatch.setenv("ROBOT_PROGRESS_LOG", str(f))
    _progress("mfg", 0.0, "ran", [fail("x", "g", BLOCKER, "t", "m")])
    assert "check mfg ran" in f.read_text() and "blockers so far 1" in f.read_text()
