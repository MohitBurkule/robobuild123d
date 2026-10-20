"""The production chassis is composed from the split tub modules (fast structural test; the geometry test is slow: REVRON_SLOW=1)."""
import inspect, os, sys
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import revron
from revron import tub, tub_shell, tub_lobes, tub_lugs, tub_front
from revron.params import CH

MODS = ("tub_util", "tub_shell_cols", "tub_shell_cuts", "tub_shell", "tub_lobes", "tub_lugs", "tub_front")


def test_split_modules_are_built_modules():
    names = [m.__name__.rsplit(".", 1)[-1] for m in revron.MODULES]
    assert all(n in names for n in MODS)


def test_chassis_is_composed_from_the_modules():
    src = inspect.getsource(tub.chassis)
    for m in ("tub_shell", "tub_lobes", "tub_lugs", "tub_front"):
        assert m + ".additions" in src or m + ".shell" in src
        assert m + ".cuts" in src or m + ".ribs" in src
    assert len(src.splitlines()) < 30


def test_tub_has_no_import_path_hacks():
    assert "sys.path" not in inspect.getsource(tub)


@pytest.mark.skipif(not os.environ.get("REVRON_SLOW"), reason="builds the full chassis (minutes)")
def test_chassis_geometry():
    c = tub.chassis()
    lo, hi = c.bounding_box().min, c.bounding_box().max
    assert abs(hi.X - CH["x"]) < 0.05 and abs(lo.X + CH["x"]) < 0.05 and abs(hi.Z - CH["z1"]) < 0.05
    assert len(c.solids()) == 1
    assert 15000 < c.volume < 17000     # RV01 is 15704 mm3; the printed tub adds the cage ribs and the key tabs
