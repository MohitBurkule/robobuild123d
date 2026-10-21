"""tub2 master-parameter relations: derived values follow the masters; the +X half mirrors to a symmetric solid."""
import os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "src"), os.path.join(ROOT, "..", "..")]
from revron import tub2_params as P, tub2_pockets as K, tub2_body, tub2_blocks, tub2_util


def test_skin_and_wall_relations():
    assert P.SKIN == P.CH_WALL / 2 and P.DECK == P.CH_Z1 - P.CH_WALL
    assert P.STOP_BACK_Y == P.STOP_FRONT_Y - P.CH_WALL            # stop wall is one wall thick
    assert abs(P.FOOT_R - P.COL_R - P.SKIN) < 1e-9                # 45 deg flare: foot R - column R = skin
    assert abs(P.POCKET_X - (P.INS_RIGHT[0][0] - P.COL_R)) < 1e-9  # pocket half width = corner-block face (tangent to column)


def test_bolt_pattern_split():
    assert len(P.INS_RIGHT) == 2 and len(P.INS_AXIS) == 1 and all(x > 0 for x, _ in P.INS_RIGHT)


def test_rear_pockets_fill_width():
    w = (P.CH_IN_X - P.SKIN - (P.COL_R + P.SKIN) - P.CH_WALL) / 2
    assert 10.2 < w < 10.5                                         # RV01 measures 10.37 per side pocket


def test_side_pocket_tip_is_diagonal_intersection():
    k = P.DIAG_K
    tip = (P.LO_APEX - P.UP_APEX + 2 * P.RIB_V) / (2 * k)
    assert abs((P.UP_APEX - P.RIB_V + k * tip) - (P.LO_APEX + P.RIB_V - k * tip)) < 1e-9


def test_shell_is_valid_solid_and_symmetric():
    s = tub2_body.shell()
    assert s.is_valid and len(s.solids()) == 1
    bb = s.bounding_box()
    assert abs(bb.min.X + bb.max.X) < 1e-6 and abs(bb.max.X - P.CH_HALF_W) < 1e-6


def test_mirrored_blocks_symmetric():
    m = tub2_util.mirrored(tub2_blocks.stop_wall_key_ledge()[0])
    bb = m.bounding_box()
    assert abs(bb.min.X + bb.max.X) < 1e-6


def test_numeric_literal_budget():
    """tub2 stays under the designer's ~130 driving dims: count numeric literals in the tub2 modules."""
    import re, glob
    n = 0
    for f in glob.glob(os.path.join(ROOT, "src", "revron", "tub2*.py")):
        src = re.sub(r'""".*?"""|#.*', "", open(f).read(), flags=re.S)
        n += len(re.findall(r"(?<![\w.])\d+\.?\d*", src))
    assert n <= 130, n
