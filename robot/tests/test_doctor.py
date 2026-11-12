"""UNTESTED when written (no code runs allowed). Fast: no CAD."""
from robot import doctor


def test_run_shape(tmp_path, monkeypatch):
    monkeypatch.setenv("ROBOT_CACHE", str(tmp_path))
    res = doctor.run()
    names = {r["name"] for r in res["rows"]}
    assert {"python", "trimesh", "cache", "GUIDE.md"} <= names
    assert all("fix" in r for r in res["rows"] if not r["ok"])


def test_missing_dep_has_fix():
    r = doctor.check_dep("no_such_mod_xyz", "no-such", True, "test")
    assert not r["ok"] and "pip install" in r["fix"]


def test_bundled_data_present():
    assert all(r["ok"] for r in doctor.check_data())


def test_cli_registers(capsys):
    from robot.cli import main
    assert main(["doctor", "--json"]) in (0, 1)
    assert '"rows"' in capsys.readouterr().out
