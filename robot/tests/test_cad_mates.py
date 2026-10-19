import numpy as np
import pytest

from robot import xform
from robot.cad import mates
from robot.spec import Spec


def world(spec, pid):
    p = spec.part(pid)
    M = xform.pose(p.at, p.rot)
    if p.parent:
        M = world(spec, p.parent) @ M
    return M


def test_face_on_face_offset():
    MA = xform.pose([0, 0, 0], [0, 0, 0])
    MB = xform.pose([5, 3, 40], [30, 10, 0])
    c = [{"type": "face", "a": {"point": [0, 0, 2], "normal": [0, 0, 1]},
          "b": {"point": [0, 0, 0], "normal": [0, 0, -1]}, "offset": 0.5}]
    M = mates.solve(MA, MB, c)
    assert max(mates.residuals(MA, M, c)) < 1e-6
    assert M[2, 3] == pytest.approx(2.5)
    assert np.allclose(M[:3, 2], [0, 0, 1], atol=1e-9)


def test_coaxial_with_axial_offset_and_face():
    MA = xform.pose([10, 0, 0], [0, 90, 0])  # A's local z is world +x
    c = [{"type": "coaxial", "a": {"point": [0, 0, 0], "axis": [0, 0, 1]}, "b": {"point": [0, 0, 0], "axis": [1, 0, 0]},
          "offset": 7}]
    M = mates.solve(MA, xform.pose([0, 5, 5], [0, 0, 45]), c)
    assert max(mates.residuals(MA, M, c)) < 1e-6
    assert np.allclose(M[:3, 3], [17, 0, 0], atol=1e-6)


def test_point_on_plane_and_angle():
    MA = np.eye(4)
    c = [{"type": "point_on_plane", "a": {"point": [0, 0, 3], "normal": [0, 0, 1]}, "b": {"point": [1, 1, 1]}},
         {"type": "angle", "a": {"point": [0, 0, 0], "axis": [0, 0, 1]}, "deg": 90}]
    M = mates.solve(MA, np.eye(4), c)
    p = M[:3, :3] @ [1, 1, 1] + M[:3, 3]
    assert p[2] == pytest.approx(3)
    assert np.allclose(M[:3, 0], [0, 1, 0], atol=1e-9)


def test_euler_roundtrip():
    for rot in ([10, 20, 30], [-170, 45, 5], [0, 90, 0]):
        R = xform.euler(rot)
        assert np.allclose(xform.euler(mates.euler_from(R)), R, atol=1e-9)


def _spec(plate_at):
    return {"name": "m", "parts": [
        {"id": "plate", "shape": {"type": "box", "size": [40, 40, 3]}, "at": plate_at, "rot": [0, 0, 15],
         "features": {"top": {"point": [0, 0, 1.5], "normal": [0, 0, 1]}, "bore": {"point": [5, 0, 0], "axis": [0, 0, 1]}}},
        {"id": "motor", "shape": {"type": "box", "size": [10, 10, 10]},
         "features": {"face": {"point": [0, 0, -5], "normal": [0, 0, -1]}, "shaft": {"point": [0, 0, 0], "axis": [0, 0, 1]}},
         "mate": {"to": "plate", "constraints": [{"type": "face", "a": "top", "b": "face"},
                                                 {"type": "coaxial", "a": "bore", "b": "shaft"}]}},
        {"id": "cap", "shape": {"type": "box", "size": [4, 4, 1]},
         "mate": {"to": "motor", "constraints": [{"type": "face", "a": {"point": [0, 0, 5], "normal": [0, 0, 1]},
                                                  "b": {"point": [0, 0, -0.5], "normal": [0, 0, -1]}, "offset": 0.2}]}},
    ]}


def test_spec_mates_follow_parent():
    s1, s2 = Spec(_spec([0, 0, 0])), Spec(_spec([12, -3, 4]))
    for s, off in ((s1, np.zeros(3)), (s2, np.array([12, -3, 4]))):
        Mm = world(s, "motor")
        R = xform.euler([0, 0, 15])
        assert np.allclose(Mm[:3, 3], off + R @ [5, 0, 6.5], atol=1e-6)  # on the bore, face on top
        Mc = world(s, "cap")
        assert np.allclose(Mc[:3, 3], Mm[:3, 3] + [0, 0, 5.7], atol=1e-6)  # dependent of dependent moved too
    # idempotent: solving the solved spec again changes nothing
    again = Spec(s2.raw)
    assert np.allclose(world(again, "cap"), world(s2, "cap"), atol=1e-9)


def test_mate_cycle_rejected():
    d = _spec([0, 0, 0])
    d["parts"][0]["mate"] = {"to": "cap", "constraints": []}
    with pytest.raises(ValueError):
        Spec(d)
