"""Fast proxies of the slow groups (robot/proxy): each must flag what its full group flags (good / bad cases)."""

import json

import numpy as np
import trimesh

from robot import spec, world
from robot.checks import Ctx, Options, assembly as full_asm, interference as full_itf
from robot.proxy import assembly, interference, load_baseline, refcad, wiring
from robot.tests.test_interference import box


def _ctx(parts, **extra):
    r = world.resolve(spec.Spec({"name": "t", "parts": parts, **extra}), fast=True)
    return Ctx(r, world.World.start(r), Options(fast=True))


def _bad(fs, fid):
    return [f for f in fs if f.id == fid and not f.passed]


# reference_cad: sliced outlines
def _sig(m, tmp_path):
    p = tmp_path / "ref.stl"
    m.export(p)
    return refcad.ref_signature(p, m, {}, {}, tmp_path)


def test_refcad_same_shape_passes(tmp_path):
    m = trimesh.creation.box((20, 10, 4))
    assert refcad.compare(m.copy(), _sig(m, tmp_path), {}) == []


def test_refcad_missing_hole_flagged(tmp_path):
    ref = trimesh.creation.box((20, 10, 4)).difference(trimesh.creation.cylinder(1.5, 10))
    diffs = refcad.compare(trimesh.creation.box((20, 10, 4)), _sig(ref, tmp_path), {})
    assert diffs and "section" in diffs[0][0]


def test_refcad_deviation_exempts_hole(tmp_path):
    ref = trimesh.creation.box((20, 10, 4)).difference(trimesh.creation.cylinder(1.5, 10))
    e = {"deviations": [{"near": [0, 0, 0], "r": 3.0, "reason": "pilot"}]}
    assert refcad.compare(trimesh.creation.box((20, 10, 4)), _sig(ref, tmp_path), e) == []


def test_refcad_moved_face_flagged(tmp_path):
    m = trimesh.creation.box((20, 10, 4))
    longer = trimesh.creation.box((21.5, 10, 4))
    assert any("bbox" in d for d, _ in refcad.compare(longer, _sig(m, tmp_path), {}))


def test_refcad_signature_cached(tmp_path):
    m = trimesh.creation.box((6, 6, 6))
    _sig(m, tmp_path)
    assert len(list(tmp_path.glob("refcad_*.json"))) == 1


# interference: depth bound and revolved envelopes
def test_touching_parts_pass():
    c = _ctx([box("a", (0, 0, 0), (10, 10, 10)), box("b", (10, 0, 0), (10, 10, 10), kind="armor")])
    assert interference.static(c) == []


def test_overlap_flagged_like_full():
    c = _ctx([box("a", (0, 0, 0), (10, 10, 10)), box("b", (8, 0, 0), (10, 10, 10), kind="armor")])
    assert _bad(interference.static(c), "proxy.interference")
    assert _bad(full_itf.run(c), "interference.overlap")


def _arm(post_at):
    arm = box("arm", (0, 0, 0), (2, 20, 2), kind="armor")
    arm["joint"] = {"kind": "revolute", "axis": [1, 0, 0], "pivot": [0, 0, 0], "min": 0, "max": 360}
    return _ctx([box("base", (0, 0, -30), (40, 40, 4)), arm, box("post", post_at, (4, 4, 4), kind="armor")])


def test_sweep_hit_flagged():
    c = _arm((0, 0, 8))  # inside the arm's 10 mm turning radius, above it at rest
    assert _bad(interference.sweeps(c), "proxy.sweep")


def test_sweep_clear_passes():
    c = _arm((0, 0, 16))  # outside the turning radius
    assert interference.sweeps(c) == []


def test_parts_filter():
    c = _ctx([box("a", (0, 0, 0), (10, 10, 10)), box("b", (8, 0, 0), (10, 10, 10), kind="armor"),
              box("c", (40, 0, 0), (5, 5, 5), kind="armor")])
    assert interference.static(c, parts=["c"]) == []


# assembly: replay the full run's order
def test_assembly_replay_good_and_bad():
    parts = [box("floor", (0, 0, -6), (30, 30, 2)), box("w1", (-8, 0, 0), (2, 30, 10), kind="armor"),
             box("bat", (0, 0, 0), (14, 14, 10), kind="battery")]
    c = _ctx(parts)
    full_asm.run(c)
    steps = [{"id": s.id, "dir": s.dir} for s in c.assembly]
    assert assembly.replay(c, steps) == []
    lid = box("lid", (0, 0, 7), (30, 30, 2), kind="armor")  # a new lid over the battery: the recorded +z exit hits it
    c2 = _ctx(parts + [lid])
    assert any(pid in ("bat", "lid") for pid, _ in assembly.replay(c2, steps))


def test_assembly_no_baseline_flags():
    assert _bad(assembly.run(_ctx([box("a", (0, 0, 0), (5, 5, 5))]), []), "proxy.assembly")


# wiring: replay routes as bands
class _B:
    def __init__(self, id, lo, hi, kind="structure"):
        self.id, self.kind, self.aabb, self.is_wire = id, kind, np.array([lo, hi], float), False

    def sdf(self, P):  # box SDF (outside distance; inside negative)
        q = np.abs(P - self.aabb.mean(0)) - (self.aabb[1] - self.aabb[0]) / 2
        return np.linalg.norm(np.maximum(q, 0), axis=1) + np.minimum(q.max(1), 0)


class _W:
    def __init__(self, bodies):
        self.bodies = bodies


def test_wiring_band_clear_and_blocked():
    shell = _B("tub", (-50, -50, -50), (50, 50, 50))
    shell.sdf = lambda P: np.full(len(P), 10.0)  # hollow: far from every wall
    route = wiring.sample([[-20, 0, 0], [20, 0, 0]])
    hit, _ = wiring.blocked(_W([shell]), route, 0.5, [route[0], route[-1]])
    assert not hit.any()
    post = _B("post", (-1, -1, -1), (1, 1, 1), kind="other")
    hit, who = wiring.blocked(_W([shell, post]), route, 0.5, [route[0], route[-1]])
    assert hit.any() and "post" in set(who[hit])


def test_wiring_sample_spacing():
    s = wiring.sample([[0, 0, 0], [1, 0, 0]])
    assert len(s) == 5 and np.allclose(s[-1], [1, 0, 0])


def test_baseline_stored(tmp_path, monkeypatch):
    monkeypatch.setenv("ROBOT_CACHE", str(tmp_path))
    rep = tmp_path / "r.json"
    rep.write_text(json.dumps({"routes": [{"id": "w"}], "assembly": [{"id": "a", "dir": [0, 0, 1]}]}))
    assert load_baseline("t", rep)["routes"] == [{"id": "w"}]
    assert load_baseline("t")["assembly"][0]["id"] == "a"


def test_fast_section_matches_reference_section():
    from robot.checks import ref_features

    m = trimesh.creation.box((20, 10, 4)).difference(trimesh.creation.cylinder(1.5, 10))
    a, b = refcad.fast_section(m, 2, 0.3), ref_features.section(m, 2, 0.3)
    assert abs(a.area - b.area) < 1e-6 and a.symmetric_difference(b).area < 1e-6
    assert refcad.fast_section(m, 2, 50.0) is None
