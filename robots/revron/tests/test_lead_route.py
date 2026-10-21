"""[fix-B-leads] Weapon phase-lead route: the bundle fits RV03's C-groove, the groove carries the via points, and it stays in the boss."""
import math
import _poses  # noqa: F401  (puts src/ and the repo on sys.path)
from revron import params as P
from robot.checks import wire_review as WR


class _W:   # the w_wesc_m wire as wire_review sees it
    awg, kind, count = P.AWG["power"], "motor", 3


def test_bundle_radius_matches_the_wire_check():
    assert abs(WR.bundle_radius(_W()) - P.LEAD_BUNDLE_R) < 1e-6


def test_bundle_fits_the_groove_and_cannot_fall_out():
    assert P.LEAD_GROOVE_R > P.LEAD_BUNDLE_R                       # room for the twist
    assert P.LEAD_MOUTH < 2 * (P.LEAD_BUNDLE_R - P.LEAD_TWIST)        # round twist wider than the mouth: retained
    assert P.LEAD_MOUTH >= P.LEAD_OD * (1 + math.sqrt(3) / 2) - 1e-9  # its narrow side still snaps through
    half = math.sqrt(P.LEAD_GROOVE_R ** 2 - (P.LEAD_GROOVE_X - P.MNT_IN) ** 2)
    assert abs(2 * half - P.LEAD_MOUTH) < 1e-6                        # the inner face cuts the groove in the mouth chord
    assert P.LEAD_GROOVE_X + P.LEAD_GROOVE_R < P.MNT_SLAB            # floor inside the slab, boss behind it


def test_groove_contains_the_via_points_and_stays_in_the_boss():
    (y0, z0), (y1, z1) = P.lead_groove_ends()
    for y, z in ((y0, z0), (y1, z1)):
        assert [P.LEAD_GROOVE_X, y, z] in P.PHASE_VIA
        assert z - P.LEAD_GROOVE_R - P.boss_line_z(y) >= P.LEAD_LIG - 1e-9
    assert abs(y1 - P.WY) < 1e-9                                      # front end straight below the stator exit
    # where the bundle turns out of the groove under the back spacer it clears the spacer ring
    assert P.WZ - z1 >= P.BSP["r"] + P.LEAD_BUNDLE_R - 1e-6


def test_groove_is_cut_in_the_mount():
    from revron import mount
    m = mount.weapon_mount("r")
    (y0, z0), (y1, z1) = P.lead_groove_ends()
    for t in (0.0, 0.5, 1.0):
        p = (P.LEAD_GROOVE_X, y0 + t * (y1 - y0), z0 + t * (z1 - z0))
        assert not m.is_inside(p), p                                 # the groove axis is open
        assert m.is_inside((P.LEAD_GROOVE_X + P.LEAD_GROOVE_R + 0.3, p[1], p[2])), p   # floor behind it
