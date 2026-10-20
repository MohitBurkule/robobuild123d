"""[W1] Fast structural test of the split tub shell modules (no CAD build)."""
import os, sys
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import revron  # noqa: F401
from revron import tub_shell, tub_shell_cols, tub_shell_cuts
from revron.params import CH, INS, N10_KEY


def test_interface():
    for name in ("shell", "additions", "cuts"):
        assert callable(getattr(tub_shell, name))
    for name in ("column_bores", "switch_slot"):
        assert callable(getattr(tub_shell_cuts, name))


def test_relations():
    assert tub_shell_cols.KEY_Z0 < 17.0 and tub_shell_cols.STOP_X0 < N10_KEY[0]
    assert tub_shell_cuts.SEAT_Z == 4.5 and len(INS) == 5
    xi = CH["x"] - CH["wall"]
    assert all(blk[0] < xi for blk in tub_shell_cols.CORNER_BLOCKS)


def test_file_sizes():
    d = os.path.join(os.path.dirname(__file__), "..", "src", "revron")
    for f in ("tub_util", "tub_shell", "tub_shell_cols", "tub_shell_cuts"):
        assert len(open(os.path.join(d, f + ".py")).read().splitlines()) < 200
