import math

import pytest

from robot.hardware import features as ft
from robot.hardware import registry as reg


def need(kind):
    if not reg.records(kind):
        pytest.skip(f"no {kind} data")


def test_iso273_monotonic_and_ordered():
    prev = None
    for d, (c, n, l) in ft.ISO_273.items():
        assert d < c < n <= l
        if prev:
            assert c > prev[0] and l > prev[2]
        prev = (c, n, l)
    assert ft.clearance(3).value == 3.4 and ft.clearance(3, "close").value == 3.2 and ft.clearance(3, "loose").value == 3.6
    with pytest.raises(ValueError):
        ft.clearance(3, "snug")
    with pytest.raises(ValueError):
        ft.clearance(7)


def test_tap_drill():
    assert ft.tap_drill(3).value == 2.5
    assert ft.tap_drill(8).value == pytest.approx(6.75)  # fallback d - P when threads table stops at M5


def test_pilot_and_engagement_are_uncertain():
    p = ft.pilot(3, "PLA")
    assert p.uncertain and 2.0 < p.value < 3.0
    assert ft.pilot(3, "tpu").value < ft.pilot(3, "PLA").value
    with pytest.raises(ValueError):
        ft.pilot(3, "unobtainium")
    e = ft.engagement_min(3, "plastic")
    assert e.value == 6.0 and e.uncertain
    assert ft.engagement_min(3, "steel").value == 3.0


def test_compensation_and_teardrop():
    assert ft.compensate(3.4) == pytest.approx(3.6)
    assert ft.compensate(3.4, None) == 3.4
    assert ft.teardrop_needed((1, 0, 0)) and not ft.teardrop_needed((0, 0, 1))
    assert not ft.teardrop_needed((1, 0, 0), ft.NO_COMP)


def test_counterbore_countersink():
    need("screw")
    cb = ft.counterbore(3)
    assert cb.d == 6.5 and cb.depth == 3.0  # DIN 974-1, ISO 4762 k
    bb = ft.counterbore(3, "button")
    assert bb.d == pytest.approx(5.7 + 0.4)
    ck = ft.countersink(3, "ISO 10642")
    assert ck.d >= 6.72 and ck.angle == 90
    assert ck.depth == pytest.approx((ck.d - ck.clearance_d) / 2 / math.tan(math.radians(45)))
    assert ft.countersink(3, "DIN 7991").d >= 6.3


def test_keepouts():
    need("screw")
    k = ft.head_keepout(3)
    assert k.d > 5.5 and k.length == 3.0
    a = ft.driver_access(3)
    assert a.uncertain and a.d < ft.head_keepout(3).d and a.length > 0


def test_nut_trap_and_insert():
    need("nut")
    t = ft.nut_trap(3)
    assert t.af == pytest.approx(5.55) and t.corners == pytest.approx(5.55 * 2 / math.sqrt(3), abs=1e-3)
    assert ft.nut_trap(3, fit="drop").depth == pytest.approx(2.6)
    need("insert")
    b = ft.insert_bore(3, "Ruthex", 5.7)
    assert b.d == 4.0 and b.depth >= 5.7 and b.od > b.d


def test_seats():
    need("bearing")
    assert ft.bearing_seat("MR85ZZ").value == 8.0
    assert ft.bearing_seat("MR85ZZ", "slip", ft.DEFAULT_COMP).value == pytest.approx(8.35)
    assert ft.dowel_hole(3).value == 3.0
    need("oring")
    w, dep, _ = ft.oring_groove("6x1.5")
    assert w > 1.5 and 0 < dep < 1.5
