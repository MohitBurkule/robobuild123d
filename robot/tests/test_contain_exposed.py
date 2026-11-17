from types import SimpleNamespace

from robot.checks.contain import _exposed_ok


def _p(kind, exposed=True):
    return SimpleNamespace(kind=kind, _extra={"exposed": exposed})


def test_exposed_motor_needs_proven_replica():
    new = SimpleNamespace(raw={})
    rep = SimpleNamespace(raw={"proven_design": {"robot": "Disector", "source": "builder"}})
    assert not _exposed_ok(new, _p("weapon_motor"))
    assert _exposed_ok(rep, _p("weapon_motor"))
    assert _exposed_ok(new, _p("battery")) and not _exposed_ok(new, _p("servo", False))
