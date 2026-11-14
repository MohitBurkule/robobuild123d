"""UNTESTED: written without running (user rule for this draft)."""
from robot.checks.robust import inproc


def test_param_hash_stable_and_sensitive():
    a = dict(spec="x/spec.json", env={"REVRON_SIZE_WIDTH": "100"})
    assert inproc.param_hash(a) == inproc.param_hash(dict(a))
    assert inproc.param_hash(a) != inproc.param_hash(dict(a, env={"REVRON_SIZE_WIDTH": "110"}))
    assert inproc.param_hash(a) != inproc.param_hash(dict(a, env={"REVRON_VARIANTS": "grooved"}))


def test_result_store_roundtrip(tmp_path, monkeypatch):
    monkeypatch.setattr(inproc, "RESULTS_DIR", tmp_path)
    inproc.save_result("k", {"id": "j", "blockers": []})
    assert inproc.load_result("k") == {"id": "j", "blockers": []}
    assert inproc.load_result("missing") is None


def test_source_edit_jobs_not_inproc():
    assert not inproc.can_inproc(dict(spec="x/spec.json", file="a.py", line=1))


def test_cached_result_skips_build(tmp_path, monkeypatch):
    monkeypatch.setattr(inproc, "RESULTS_DIR", tmp_path)
    monkeypatch.setattr(inproc, "can_inproc", lambda j: True)
    job = dict(spec="x/spec.json", env={"A": "1"})
    inproc.save_result(inproc.param_hash(job), {"id": "j", "blockers": []})
    monkeypatch.setattr(inproc, "run_inproc", lambda j: (_ for _ in ()).throw(AssertionError("rebuilt")))
    assert inproc.inproc_execute(job, 10)["cached"] is True
