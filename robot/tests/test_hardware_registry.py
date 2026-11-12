import pytest

from robot import hardware as hw
from robot.hardware import registry as reg


def need(kind):
    if not reg.records(kind):
        pytest.skip(f"no {kind} data ({reg.load_errors().get(kind, 'empty')})")


@pytest.mark.parametrize("des,family,std", [
    ("M3x8 DIN7991", "csk", "DIN 7991"), ("M3x8 DIN 7991", "csk", "DIN 7991"), ("M3x8 ISO 10642", "csk", "ISO 10642"),
    ("M2.5x6 cap", "cap", "ISO 4762"), ("m3 x 10 shcs", "cap", "ISO 4762"), ("M3x10 DIN912", "cap", "ISO 4762"),
    ("M3x6 bhcs", "button", "ISO 7380-1"), ("M3x8 fhcs", "csk", "ISO 10642"), ("M3x10", "cap", "ISO 4762"),
    ("M3x10 ISO 4762:2004", "cap", "ISO 4762"), ("M3x6 ISO7380", "button", "ISO 7380-1"),
])
def test_screw_designations(des, family, std):
    need("screw")
    p = hw.get(des)
    assert p.kind == "screw" and p.record.family == family and p.record.standard == std
    assert p.record.d == float(des.lower().split("x")[0].strip().lstrip("m"))
    assert p.length is not None


def test_grub_prefix_family():
    need("screw")
    assert hw.get("M3x4 grub").record.family.startswith("grub")


@pytest.mark.parametrize("des,family", [
    ("M3 nut", "hex"), ("M3 nut ISO4032", "hex"), ("M3 nyloc", "nyloc"), ("M3 thin nut", "thin"),
    ("M3 square nut", "square"), ("M3 nut DIN934", "hex"),
])
def test_nuts(des, family):
    need("nut")
    p = hw.get(des)
    assert p.kind == "nut" and p.record.family == family and p.record.d == 3.0


def test_din934_note():
    need("nut")
    assert any("DIN 934" in n for n in hw.get("M3 nut DIN934").notes)


def test_washers_inserts_standoffs():
    need("washer")
    w = hw.get("M3 washer ISO7089")
    assert w.kind == "washer" and w.record.standard == "ISO 7089"
    assert hw.get("M3 washer DIN125").record.standard == "ISO 7089"
    need("insert")
    i = hw.get("M3 insert Ruthex")
    assert i.record.maker == "Ruthex" and i.record.d == 3.0
    assert hw.get("M3x5.7 insert").length == 5.7
    need("standoff")
    s = hw.get("M3x10 standoff mf")
    assert s.record.family == "mf" and s.length == 10


@pytest.mark.parametrize("des,bore,variant", [("MR85ZZ", 5, ""), ("683", 3, ""), ("608-2RS", 8, "2RS"), ("MR63", 3, "")])
def test_bearings(des, bore, variant):
    need("bearing")
    p = hw.get(des)
    assert p.kind == "bearing" and p.record.d == bore and p.variant == variant


def test_pins_circlips_orings_shafts():
    need("pin")
    p = hw.get("dowel 3x10")
    assert p.kind == "pin" and p.record.d == 3 and p.length == 10 and p.record.family.startswith("dowel")
    need("circlip")
    c = hw.get("DIN471 5")
    assert c.kind == "circlip" and c.record.shaft_d == 5 and c.record.family.startswith("ext")
    need("oring")
    o = hw.get("oring 6x1.5")
    assert o.record.id == 6 and o.record.cs == 1.5
    need("shaft")
    assert hw.get("shaft 5 h6").record.tolerance == "h6"


def test_thread():
    need("thread")
    assert hw.get("M3 thread").record.pitch == 0.5


@pytest.mark.parametrize("bad", ["", "M7x3", "M3x8 ISO 9999", "M3 frobnicator", "banana", "M3x7 cap",
                                 "oring 6x9", "dowel 3x11"])
def test_errors_are_value_errors_with_options(bad):
    need("screw")
    with pytest.raises(ValueError) as e:
        hw.get(bad)
    assert str(e.value)


def test_non_strict_length():
    need("screw")
    p = hw.get("M3x7 cap", strict=False)
    assert p.length == 7 and p.notes


def test_nearest_length():
    need("screw")
    p = hw.get("M3x10 cap")
    assert hw.nearest_length(p, 9) == 10
    assert hw.nearest_length(p, 9, "floor") == 8
    assert hw.nearest_length(p, 10) == 10
    with pytest.raises(ValueError):
        hw.nearest_length(p, 1e6)


def test_list_family():
    need("screw")
    caps = hw.list_family("screw", family="cap")
    assert caps and all(r.family == "cap" for r in caps)
    assert hw.list_family("screw", d=3, standard="DIN 912")  # alias resolves to ISO 4762
    with pytest.raises(ValueError):
        hw.list_family("spaceship")
