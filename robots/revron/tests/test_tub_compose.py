"""The production chassis is composed from the split tub modules (fast structural test; the geometry test is slow: REVRON_SLOW=1)."""
import inspect, os, sys
import pytest
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import revron
from revron import tub, tub2
from revron.params import CH

MODS = ("tub2_params", "tub2_body", "tub2_cols", "tub2_blocks", "tub2_pockets", "tub2_seat", "tub2_fillets", "tub2_lobes", "tub2_front",
        "tub2_switch", "tub2_lug", "tub2_tab", "tub2_flange", "tub2_lattice", "tub2")


def test_split_modules_are_built_modules():
    names = [m.__name__.rsplit(".", 1)[-1] for m in revron.MODULES]
    assert all(n in names for n in MODS)


def test_chassis_is_composed_from_the_feature_modules():
    src = inspect.getsource(tub2.cuts) + inspect.getsource(tub2.additions)
    for m in ("tub2_lobes", "tub2_pockets", "tub2_seat", "tub2_lattice", "tub2_flange", "tub2_lug", "tub2_switch"):
        assert m in src
    assert tub.chassis.__code__.co_firstlineno and len(inspect.getsource(tub.chassis).splitlines()) < 10


def test_tub_has_no_import_path_hacks():
    assert "sys.path" not in inspect.getsource(tub)


@pytest.mark.skipif(not os.environ.get("REVRON_SLOW"), reason="builds the full chassis (minutes)")
def test_chassis_geometry():
    c = tub.chassis()
    lo, hi = c.bounding_box().min, c.bounding_box().max
    assert abs(hi.X - CH["x"]) < 0.05 and abs(lo.X + CH["x"]) < 0.05 and abs(hi.Z - CH["z1"]) < 0.05
    assert len(c.solids()) == 1
    assert 15000 < c.volume < 17000     # RV01 is 15704 mm3; the printed tub adds the key tabs
