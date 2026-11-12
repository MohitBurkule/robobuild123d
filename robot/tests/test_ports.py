"""ROADMAP R1/R2 acceptance. UNTESTED: written without running."""
import pytest

from robot import ports


def _all_ids():
    from robot import cots_alts as ca
    ids = []
    for t in (ca.WEAPON_MOTORS, ca.GEARMOTORS, ca.BATTERIES, ca.ESCS, ca.SWITCHES, ca.WHEELS):
        ids += list(t)
    return ids


@pytest.mark.parametrize("cid", _all_ids())
def test_every_id_iface_or_porterror(cid):
    try:
        i = ports.iface(cid)
    except ports.PortError as e:
        assert e.cid == cid
        return
    assert i.cid == cid and i.envelope.lx > 0


def test_unknown_id_is_porterror():
    with pytest.raises(ports.PortError):
        ports.iface("no_such_part_xyz")


def test_3mm_d_shaft_vs_2mm_bore_flagged():
    sh = ports.Shaft(d=3.0, length=9.0, flat=2.5)
    bad = ports.shaft_bore(sh, ports.Bore(d=2.0))
    assert any(m.field == "d" for m in bad)
    assert any(m.field == "flat" for m in bad)


def test_n20_with_bbb_wheel_ok():
    m, w = ports.iface("bbb_n20_600rpm"), ports.iface("bbb_wheel_34x6_5")
    assert ports.compatible(m, w) == []
    assert ports.compatible(w, m) == []


def test_gearmotor_mount_two_holes():
    m = ports.iface("pololu_hpcb6v_30to1")
    assert m.mount.n == 2 and len(m.mount.points()) == 2


def test_outrunner_patterns():
    m = ports.iface("bbb_be1806_2300kv")
    assert len(m.base_mount) == 2 and m.shaft.d == 2.0


def test_pack_over_esc_cells():
    p, e = ports.iface("gnb_3s_300_80c_hv"), ports.iface("bbb_malenki_nano")
    assert any(m.field == "cells" for m in ports.compatible(p, e))


def test_wheel_derive_stock_none():
    from revron import wheel_ports
    assert wheel_ports.derive("stock") is None


@pytest.mark.parametrize("cid", ["bbb_wheel_34x6_5", "bbb_wheel_22x10", "durahubs_25", "durahubs_30", "durahubs_35"])
def test_wheel_derive_or_unfit(cid):
    from revron import wheel_ports
    try:
        g = wheel_ports.derive(cid, "bbb_n20_600rpm")
    except wheel_ports.WheelUnfit:
        return
    assert g.seat_r > g.bore_r and g.od / 2 > g.flange_r
