"""`robot plate` / `robot colors` helpers: the pure parts (rectangle search, face finding, colour sameness)."""

import numpy as np
import trimesh

from robot import look_colors, look_plates


def test_largest_rect_finds_the_big_block():
    m = np.zeros((10, 12), bool)
    m[2:8, 3:11] = True
    m[0, 0] = True
    assert look_plates._largest_rect(m) == (2, 8, 3, 11)


def test_largest_rect_none_when_empty():
    assert look_plates._largest_rect(np.zeros((4, 4), bool)) is None


def test_find_face_on_a_box_top():
    mesh = trimesh.creation.box(extents=(40, 30, 10))  # top face at z = +5
    f = look_plates.find_face(mesh, 2, 1, inset=1.0)
    assert abs(f["level"] - 5.0) < 0.3
    w, h = f["hi"][0] - f["lo"][0], f["hi"][1] - f["lo"][1]
    assert 34 <= w <= 40 and 24 <= h <= 30  # inside the face, inset ~1 mm per side


def test_find_face_picks_the_largest_level():
    a = trimesh.creation.box(extents=(60, 40, 10))
    b = trimesh.creation.box(extents=(16, 16, 4))
    b.apply_translation((20, 0, 7))  # small raised block on top
    mesh = trimesh.util.concatenate([a, b])
    assert abs(look_plates.find_face(mesh, 2, 1)["level"] - 5.0) < 0.3
    assert abs(look_plates.find_face(mesh, 2, 1, level="outer")["level"] - 9.0) < 0.3


def test_box_spans_level_minus_thick():
    f = {"level": 14.0, "lo": (-10.0, -5.0), "hi": (10.0, 5.0), "u": 0, "v": 1}
    bx = look_plates._box(f, 2, 1, 2.0)
    z0 = bx["at"][2] - bx["shape"]["size"][2] / 2
    assert abs(z0 - 12.0) < 1e-6 and bx["shape"]["size"][:2] == [20.0, 10.0]


def test_boss_top_is_flush_with_plate_underside():
    f = {"level": 14.0, "lo": (-10.0, -5.0), "hi": (10.0, 5.0), "u": 0, "v": 1}
    bs = look_plates._boss(f, 2, 1, 2.0, (3.0, 4.0), np.zeros(3))
    top = bs["at"][2] + bs["shape"]["height"] / 2
    assert abs(top - 12.0) < 1e-6 and bs["at"][:2] == [3.0, 4.0]


def test_colors_same_colour_lit_differently_is_kept():
    assert not look_colors.different("#f08a6a", "#ffb090")  # salmon, lighter
    assert not look_colors.different("#1c1d20", "#45535a")  # black vs dark grey
    assert look_colors.different("#5a5e66", "#f4ecec")  # grey printed vs white plate
    assert look_colors.different("#202226", "#e8c020")  # black vs yellow
    assert look_colors.different("#d03030", "#3050d0")  # red vs blue
