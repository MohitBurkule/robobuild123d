"""Generator body shapes: round/oval outlines and sloped (cone) shells."""
import math

from robot.gen import build as B
from robot.gen.external import shell
from robot.gen.external.plan import Frame


def test_round_outline_capped_by_size_rule():
    pts = B.disc_outline(60.0, -60.0, 60.0)
    r = max(math.hypot(x, y) for x, y in pts)
    assert r <= B.ROUND_MAX_R + 0.01


def test_round_holds_default_box():
    pts = B.disc_outline(30.0, -40.0, 36.0)
    from shapely.geometry import Point
    from robot.gen.layout import geom
    poly = geom.polygon(pts).buffer(0.5)  # polygon chords sit just inside the true circle
    for c in ((-30, -40), (30, -40), (30, 36), (-30, 36)):
        assert poly.contains(Point(c))


def test_profile_interpolates_and_clamps():
    f = Frame(outline=B.disc_outline(30, -40, 36), zb=-10, zt=10, profile=[[0, 0], [1, 8]])
    assert f.inset_at(-10) == 0 and f.inset_at(10) == 8 and abs(f.inset_at(0) - 4) < 1e-9
    assert f.inset_at(50) == 8 and f.max_inset() == 8
    assert f.breaks(-10, 10) == [-10, 10]


def test_sections_same_count_and_shrink():
    out = B.disc_outline(30, -40, 36)
    a, b = shell.section(out, 0), shell.section(out, 6)
    assert len(a) == len(b) == shell.SECTION_N
    ra = max(math.hypot(x, y + 2) for x, y in a)
    rb = max(math.hypot(x, y + 2) for x, y in b)
    assert rb < ra - 5


def test_shell_profile_from_user():
    assert B.shell_profile({"taper": 5}) == [[0.0, 0.0], [1.0, 5.0]]
    assert B.shell_profile({"profile": [[0, 0], [1, 3]]}) == [[0.0, 0.0], [1.0, 3.0]]
    assert B.shell_profile({}) is None


def test_unknown_shape_message():
    import pytest
    from robot.gen import hypothesis as H
    with pytest.raises(ValueError, match="shape `star` unknown"):
        B.make_plan(H.preset("hspin_bar"), {"shape": "star"})
