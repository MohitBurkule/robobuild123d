import pytest

from robot.fight import radioss


@pytest.mark.parametrize("mat", sorted(radioss.MATERIALS))
def test_deck_generation(tmp_path, mat):
    s, e = radioss.write_deck(tmp_path, "t", 0.010, 40.0, 3.0, mat, n_el=8)
    txt = s.read_text()
    assert s.name == "t_0000.rad" and e.name == "t_0001.rad"
    for kw in ("/BEGIN", "/NODE", "/SHELL/1", "/MAT/PLAS_JOHNS/1", "/FAIL/JOHNSON/1",
               "/RBODY/1", "/INIVEL/TRA/1", "/INTER/TYPE7/1", "/BCS/1", "/END"):
        assert kw in txt
    # node block: 9x9 plate + 3x3 tooth + master
    nodes = txt.split("/NODE\n")[1].split("/SHELL/1")[0].strip().splitlines()
    assert len(nodes) == 81 + 9 + 1
    assert "-40" in txt.split("/INIVEL/TRA/1")[1].splitlines()[2]
    assert e.read_text().startswith("/RUN/t/1")


def test_unknown_material(tmp_path):
    with pytest.raises(KeyError):
        radioss.write_deck(tmp_path, "t", 0.01, 40, 3, "WOOD")


@pytest.mark.skipif(not radioss.binaries_available(), reason="OpenRadioss not installed")
def test_integration_pla(tmp_path):
    r = radioss.impact_case(0.010, 20.0, 3.0, "PLA", workdir=tmp_path, n_el=8)
    assert r["E_abs"] is not None and 0 <= r["E_abs"] <= 0.5 * 0.01 * 20 ** 2
