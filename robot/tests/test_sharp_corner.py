"""Opt-out sharp internal corner check (robot.checks.sharp_corner)."""

from types import SimpleNamespace as NS

import numpy as np
import trimesh
from shapely.geometry import Point, Polygon

from robot.checks import sharp_corner as S
from robot.finding import BLOCKER, WARNING

L = Polygon([(0, 0), (20, 0), (20, 3), (3, 3), (3, 20), (0, 20)])   # L bracket, inside corner along z at (3, 3)


def bracket(r=0.0, seg=16):
    g = L if r == 0 else L.union(Polygon([(3, 3), (3 + r, 3), (3, 3 + r)]).difference(Point(3 + r, 3 + r).buffer(r, seg)))
    return trimesh.creation.extrude_polygon(g, 10)


def _body(id, m, kind="structure", fastener=False):
    return NS(id=id, mesh=m, kind=kind, fastener=fastener, is_wire=False, aabb=m.bounds,
              inside=lambda P, m=m: m.contains(np.atleast_2d(P)))


def _ctx(m, part_extra=None, raw=None, others=()):
    p = NS(id="br", catalog=None, process="fdm", kind="structure", _extra=part_extra or {})
    bodies = [_body("br", m)] + list(others)
    world = NS(bodies=bodies, body=lambda i: next((b for b in bodies if b.id == i), None))
    spec = NS(raw=raw or {}, base_dir=".")
    parts = [NS(part=p)] + [NS(part=NS(id=b.id, catalog=None, process="fdm", kind=b.kind, _extra={}))
                            for b in others if not b.fastener]
    return NS(r=NS(spec=spec, parts=parts), world=world, metrics={}, not_checked=[])


def _fails(out):
    return [(f.id, f.severity) for f in out if not f.passed]


def test_radius_estimate():
    for r in (0.0, 0.6, 1.0, 2.0):
        m = bracket(r, 4)
        rs = {round(S.local_radius(m, p, t, 4.0)[0], 1) for p, t in S.concave_samples(m)}
        assert rs == {r}


def test_sharp_bracket_fails():
    assert (S.CID, WARNING) in _fails(S.run(_ctx(bracket(0))))


def test_filleted_bracket_passes():
    out = S.run(_ctx(bracket(1.2)))
    assert not _fails(out) and any(f.id == S.CID + ".ok" for f in out)


def test_sharp_with_reason_passes():
    assert not _fails(S.run(_ctx(bracket(0), {"sharp_corners_ok": "TPU bumper, flexes"})))
    raw = {"sharp_ok": [{"part": "br", "near": [3, 3, 5], "r_mm": 6, "reason": "relief slot, not loaded"}]}
    assert not _fails(S.run(_ctx(bracket(0), raw=raw)))


def test_opt_out_without_reason_fails():
    f = _fails(S.run(_ctx(bracket(0), {"sharp_corners_ok": ""})))
    assert ("mfg.sharp_ok_reason", BLOCKER) in f and (S.CID, WARNING) in f
    f = _fails(S.run(_ctx(bracket(0), raw={"sharp_ok": [{"part": "br", "near": [3, 3, 5], "r_mm": 6}]})))
    assert ("mfg.sharp_ok_reason", BLOCKER) in f and (S.CID, WARNING) in f


def test_load_joint_escalates():
    # 0.7 mm fillet: fine as a plain corner (>= 0.5), a blocker beside a fastener seat (< 1.0)
    m = bracket(0.7)
    assert not _fails(S.run(_ctx(m)))
    screw = trimesh.creation.cylinder(1.5, 8)
    screw.apply_translation((5, 5, 5))
    assert (S.CID, BLOCKER) in _fails(S.run(_ctx(m, others=[_body("f1", screw, "fastener", True)])))
    raw = {"sharp_corner_loads": [{"part": "br", "near": [3, 3, 5], "r_mm": 6}]}
    assert (S.CID, BLOCKER) in _fails(S.run(_ctx(bracket(0), raw=raw)))
    deck = trimesh.creation.box((20, 20, 2))
    deck.apply_translation((10, 10, -1))
    assert (S.CID, BLOCKER) in _fails(S.run(_ctx(bracket(0), others=[_body("deck", deck)])))


def test_reference_match_downgrades(tmp_path):
    ref = bracket(0)
    ref.export(tmp_path / "ref.stl")
    raw = {"reference_cad": {"dir": str(tmp_path), "ref_to_world": np.eye(4).tolist(),
                             "parts": [{"part": "br", "file": "ref.stl"}]}}
    out = S.run(_ctx(bracket(0), raw=raw))
    assert not _fails(out) and any("matches original" in f.message for f in out)
    raw["reference_cad"]["parts"][0]["file"] = "ref2.stl"
    bracket(2.0).export(tmp_path / "ref2.stl")
    assert (S.CID, WARNING) in _fails(S.run(_ctx(bracket(0), raw=raw)))


def test_intent_fillet_corner_not_double_reported():
    raw = {"intent": [{"rule": "fillet", "part": "br", "axis": "z", "h": 5, "at": [[3, 3]]}]}
    assert not _fails(S.run(_ctx(bracket(0), raw=raw)))
