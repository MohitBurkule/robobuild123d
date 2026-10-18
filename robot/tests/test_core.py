"""Core API: shapes become valid solids, the world places them, measures agree with known numbers."""

import numpy as np

from robot import measure, shapes, spec, world
from robot.checks import Options, verify

ROOT = __import__("pathlib").Path(__file__).resolve().parents[1]


def test_self_intersecting_prism_is_repaired_like_rust():
    pts = [[35.5161, -1.6103], [60.3418, -7.8], [60.3418, -10.0], [36.0, -10.0], [36.0, -1.6103]]
    s = shapes.to_solid({"type": "prism", "points": pts, "height": 1.2})
    assert s.is_valid and abs(s.volume - 152.9) < 0.5


def test_new_shape_types_build():
    for t in [{"type": "revolve", "profile": [[0, 0], [10, 0], [10, 5], [0, 5]]},
              {"type": "spline_prism", "points": [[0, 0], [10, 0], [10, 10], [0, 10]], "height": 3},
              {"type": "loft", "sections": [{"points": [[0, 0], [10, 0], [10, 10], [0, 10]], "z": 0},
                                            {"points": [[2, 2], [8, 2], [8, 8], [2, 8]], "z": 5}]},
              {"type": "fillet", "shape": {"type": "box", "size": [10, 10, 10]}, "radius": 1}]:
        assert shapes.to_solid(t).is_valid


def test_wedge_world_and_measures():
    r = world.resolve(spec.load(ROOT / "tests" / "fixtures_wedge_rust.json"))
    w = world.World.start(r)
    assert abs(r.parts[2].geom.volume - 12160) < 5  # wedge B-rep volume, Rust sampling gives ~12154
    pts = np.vstack([b.mesh.vertices for b in w.bodies])
    assert abs(measure.footprint_mm(pts) - 122.48) < 0.1
    assert measure.lowest_point(w.body("wheel_l"))[2] == -14.0
    o = measure.overlap(w.body("battery"), w.body("chassis_bottom"))
    assert o is None or o.depth <= 0.08


def test_mass_matches_rust_within_one_percent():
    rep = verify(spec.load(ROOT / "tests" / "fixtures_wedge_rust.json"), Options(only=["mass"]))
    assert abs(rep.metrics["mass_total_g"] - 105.97) / 105.97 < 0.01
