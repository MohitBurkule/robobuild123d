"""realworld group: wire.outside and the real-build gap checks (robot/checks/realworld.py)."""
from robot import spec
from robot.checks import Options, verify


def box(x, y, z):
    return {"type": "box", "size": [x, y, z]}


def tub():
    return {"id": "tub", "kind": "structure", "shape": box(80, 80, 20), "at": [0, 0, 10], "material": "pla", "process": "fdm"}


def esc(at=(0, 0, 10), **kw):
    return {"id": "esc", "kind": "esc", "shape": box(10, 10, 4), "at": list(at), "material": "pla", "process": "cots",
            "ports": {"p": [0, 0, 0]}, **kw}


def bat(at=(20, 0, 10), **kw):
    return {"id": "bat", "kind": "battery", "shape": box(20, 10, 6), "at": list(at), "material": "pla", "process": "cots",
            "ports": {"p": [0, 0, 0]}, **kw}


def run(parts, wires=(), fasteners=()):
    d = {"name": "r", "parts": parts, "wires": list(wires), "fasteners": list(fasteners)}
    rep = verify(spec.Spec(d), Options(fast=True, only=["realworld"]))
    assert not [f for f in rep.findings if f.id == "realworld.crashed"], [str(f) for f in rep.findings if f.id == "realworld.crashed"]
    return rep


def ids(rep, fid):
    return [f for f in rep.findings if f.id == fid and not f.passed]


W = {"id": "w1", "from": "esc.p", "to": "bat.p", "kind": "signal", "awg": 30}


def test_wire_inside_passes():
    rep = run([tub(), esc(), bat()], [W])
    assert not ids(rep, "wire.outside")
    assert any(f.id == "wire.outside" and f.passed for f in rep.findings)


def test_wire_via_outside_is_blocker():
    w = dict(W, via=[[10, 60, 10]])
    assert ids(run([tub(), esc(), bat()], [w]), "wire.outside")


def test_wire_tube_radius_counts():
    # centreline 0.2 mm inside the wall plane, but a 2.2 mm thick wire sticks out
    w = dict(W, awg=20, via=[[10, 39.8, 10]])
    assert ids(run([tub(), esc(), bat()], [w]), "wire.outside")


def test_external_needs_reason():
    w = dict(W, via=[[10, 60, 10]], external=True)
    assert ids(run([tub(), esc(), bat()], [w]), "wire.outside")
    w["exposed_reason"] = "charge lead"
    assert not ids(run([tub(), esc(), bat()], [w]), "wire.outside")


def test_wire_gauge_vs_current():
    w = dict(W, kind="power", awg=30, current_a=10 * 3)
    assert ids(run([tub(), esc(), bat()], [w]), "wire.gauge_current")
    w["awg"] = 20
    assert not ids(run([tub(), esc(), bat()], [w]), "wire.gauge_current")


def test_wire_to_spinning_part():
    disc = {"id": "disc", "kind": "weapon", "shape": box(30, 30, 3), "at": [0, 0, 22], "material": "steel",
            "process": "cnc", "rotates_with": "disc", "ports": {"p": [0, 0, 0]},
            "joint": {"kind": "revolute", "axis": [0, 0, 1], "pivot": [0, 0, 0]}}
    w = dict(W, to="disc.p")
    assert ids(run([tub(), esc(), bat(), disc], [w]), "wire.spans_rotation")
    w["slip_ring"] = True
    assert not ids(run([tub(), esc(), bat(), disc], [w]), "wire.spans_rotation")


def test_connector_rating():
    rep = run([tub(), esc(), bat(connector="JST-PH")], [])
    assert not ids(rep, "connector.rating")   # no peak current known -> not judged


def test_battery_near_wall():
    assert ids(run([tub(), bat(at=(29.5, 0, 10))]), "battery.armour_gap")
    assert not ids(run([tub(), bat(at=(0, 0, 10))]), "battery.armour_gap")


def test_heat_neighbour():
    mot = {"id": "m", "kind": "motor", "shape": box(10, 10, 10), "at": [0, 15, 10], "material": "steel", "process": "cots"}
    assert ids(run([tub(), esc(at=(0, 5.2, 10)), mot]), "heat.neighbour")
    assert not ids(run([tub(), esc(at=(0, -10, 10)), mot]), "heat.neighbour")


def test_screw_lock_on_rotor():
    disc = {"id": "disc", "kind": "weapon", "shape": box(30, 30, 3), "at": [0, 0, 22], "material": "steel",
            "process": "cnc", "rotates_with": "disc", "joint": {"kind": "revolute", "axis": [0, 0, 1], "pivot": [0, 0, 0]}}
    hub = {"id": "hub", "kind": "structure", "shape": box(10, 10, 3), "at": [0, 0, 25], "material": "aluminium",
           "process": "cnc", "rotates_with": "disc"}
    f = {"id": "b", "designation": "M2x6", "at": [0, 0, 27], "dir": [0, 0, -1], "through": ["hub"], "threads_into": "disc",
         "tool": "hex1.5", "head": "socket"}
    assert ids(run([tub(), disc, hub], fasteners=[f]), "fastener.lock")
    assert not ids(run([tub(), disc, hub], fasteners=[dict(f, lock="threadlock")]), "fastener.lock")


def test_no_crash():
    rep = run([tub(), esc(), bat()], [W])
    assert not [f for f in rep.findings if f.id == "realworld.crashed"]
