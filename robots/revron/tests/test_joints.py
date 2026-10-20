"""The mated poses are the design relations, not typed coordinates."""
import math
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import revron  # noqa: E402
from revron import joints as J, params as P  # noqa: E402


def test_inserts_sit_on_bore_floor_and_flush_with_rim():
    for i in range(len(P.INS)):
        assert math.isclose(J.place_at(f"insert_b{i}")[2] - P.INS_LEN / 2, P.INS_Z[0])
    for i in range(len(P.TOP_XY)):
        assert math.isclose(J.place_at(f"insert_t{i}")[2] + P.INS_LEN / 2, P.CH["z1"])


def test_switch_side_face_clears_the_wall():
    x = J.place_at("power_switch")[0]
    assert math.isclose(x + P.SW_HALF + P.SW_WALL_CLEAR, P.CH["x"] - P.CH["wall"])


def test_switch_screws_straddle_the_switch_on_its_body_top():
    yc, zc = P.ELEC["switch_yz"]
    ys = sorted(J.place_at(f"bolt_sw{i}")[1] for i in range(2))
    assert math.isclose((ys[0] + ys[1]) / 2, yc) and math.isclose(ys[1] - ys[0], P.SW_PITCH)
    assert all(math.isclose(J.place_at(f"bolt_sw{i}")[2], zc + P.SW_BODY_H / 2) for i in range(2))


def test_motors_mirror_about_the_centre_plane():
    r, l = J.place_at("motor_r"), J.place_at("motor_l")
    assert math.isclose(r[0], -l[0]) and r[1:] == l[1:]
    assert J.place_rot("motor_l")[2] == 180.0 and J.place_rot("motor_r")[2] == 0.0
