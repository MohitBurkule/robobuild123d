"""[fix-B-rel] Weapon module relations: the stack, bolt circles, shaft and mounts are where their mates say."""
import math
import numpy as np
import pytest
import _poses  # noqa: F401  (puts src/ and the repo on sys.path)
from revron import params as P
from revron import joints as J
from revron.spec import make_spec
from robot import catalog as cat

TOL = 1e-6


def _spec():
    s = make_spec("m.py")
    return {p["id"]: p for p in s["parts"]}, {f["id"]: f for f in s["fasteners"]}


def _world(part, label):
    h = J.RIG.parts[part]
    loc = h.location * h.joints[label].relative_location
    return np.array([loc.position.X, loc.position.Y, loc.position.Z])


def test_stack_plates_are_flush_and_sit_on_the_bell_cap():
    order = ("spider", "disc_a", "spacer", "disc_b")
    for a, b in zip(order, order[1:]):
        assert abs(P.DR_X[a][1] - P.DR_X[b][0]) < TOL, (a, b)
    for k, t in zip(order, (P.SPIDER_T, P.DISC_T, P.SPACER_T, P.DISC_T)):
        assert abs(P.DR_X[k][1] - P.DR_X[k][0] - t) < TOL, k
    # the spider's inner face is the bell cap face (catalog frame flipped into the weapon frame)
    cap = _world("weapon_motor_can", "cap_face")
    assert abs(cap[0] - P.DR_X["spider"][1]) < TOL
    assert np.allclose(cap[1:], (P.WY, P.WZ), atol=TOL)


def test_spider_is_clocked_to_the_bell_screws():
    assert P.HUB_R == cat.BELL_SCREW_R and P.DR_ROT == cat.BELL_SCREW_PHASE


def test_bolt_circles_are_centred_on_the_weapon_axis():
    _, fast = _spec()
    for pre, r, x in (("bolt_p", P.HUB_R, P.DR_X["spider"][0]), ("bolt_d", P.BOLT_R, P.DR_X["disc_b"][1]),
                      ("bolt_wm", P.STATOR_PCD / 2, P.CB_CONE_X[1])):
        pts = [fast[f"{pre}{k}"]["at"] for k in range(P.N_STACK)]
        for p in pts:
            assert abs(math.hypot(p[1] - P.WY, p[2] - P.WZ) - r) < 1e-5, pre
            assert abs(p[0] - x) < 1e-5, pre
        c = np.mean(np.array(pts)[:, 1:], axis=0)
        assert np.allclose(c, (P.WY, P.WZ), atol=1e-5), pre   # a full pattern: centroid on the axis


def test_stator_pcd_matches_the_motor_base_holes():
    base = cat._gr1507_base()
    holes = [c["at"] for c in base["cut"]]
    assert len(holes) == len(P.STATOR_DIRS)
    for x, y, z in holes:
        assert abs(math.hypot(y, z) - P.STATOR_PCD / 2) < TOL
    # and the RV03 counterbores are on the same circle, one per base arm
    dirs = {(round(y / (P.STATOR_PCD / 2)), round(z / (P.STATOR_PCD / 2))) for _, y, z in holes}
    assert {(abs(u), abs(v)) for u, v in P.STATOR_DIRS} == {(abs(u), abs(v)) for u, v in dirs}


def test_shaft_axis_is_the_weapon_axis_and_runs_in_the_mr85():
    parts, _ = _spec()
    j = parts["spider"]["joint"]
    pivot_world = np.array(j["pivot"]) + np.array(P.MNT_FRAME["r"])   # pivot is in the RV03 frame
    assert np.allclose(pivot_world[1:], (P.WY, P.WZ), atol=TOL) and j["axis"] == [1.0, 0.0, 0.0]
    shaft = J.RIG.parts["wshaft"].location.position
    assert np.allclose((shaft.Y, shaft.Z), (P.WY, P.WZ), atol=TOL)
    seat = _world("mount_l", "bearing_seat")
    assert np.allclose(seat, (P.BRG["x"], P.WY, P.WZ), atol=TOL)
    assert P.BRG["bore_r"] == P.WSHAFT["r"] and P.SHAFT_D == 2 * P.WSHAFT["r"]
    # shaft free end past the bearing, into the RV02 nut recess; bearing inside the RV02 slab
    assert P.WSHAFT["x_end"] < P.BRG["x"] - P.BRG["w"] / 2 and -P.MNT_SLAB > P.WSHAFT["x_end"]
    assert -P.MNT_SLAB < P.BRG["x"] - P.BRG["w"] / 2 and P.BRG["x"] + P.BRG["w"] / 2 < -P.MNT_IN


def test_mounts_and_spacer_sit_on_their_frames():
    for n in "lr":
        loc = J.RIG.parts[f"mount_{n}"].location.position
        assert np.allclose((loc.X, loc.Y, loc.Z), P.MNT_FRAME[n], atol=TOL), n
    sp = J.RIG.parts["motor_spacer"].location.position
    assert np.allclose((sp.X, sp.Y, sp.Z), (P.BSP_X[1], P.WY, P.WZ), atol=TOL)   # back spacer face on RV03's inner face
    assert abs(P.BSP_X[1] - P.MNT_IN) < TOL


@pytest.mark.skipif(not P.PRINTABLE, reason="nose pad belongs to the optional printable mount variant (REVRON_MOUNT_VARIANT=printable)")
def test_nose_csk_keeps_a_printed_wall_at_the_inner_face():
    """mfg.thin_wall: the nose pad (NOSE_PAD_R) leaves >= 0.9 mm round the nose CSK rim on both mounts (RV02 was 0.27)."""
    from shapely.geometry import Point
    from revron import mount
    from revron import params as P
    for side in "lr":
        prof = mount._mount_profile(side)
        rim = Point(P.SB).buffer(P.NOSE_PAD_R - 0.9 + 1e-3)   # cone rim at the flush inner face + one fdm wall
        assert prof.contains(rim), side
