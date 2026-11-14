"""Wiring skeleton: settings merge over defaults.json, and the typed model's invariants."""

from types import SimpleNamespace

from robot.wiring import model, settings
from robot.wiring.model import KINDS, ROLES, ROLES_OF_KIND, ConnectorType, Gauge, Net


def test_defaults_load_and_merge():
    d = settings.defaults()
    assert d and "_doc" not in d
    over = {"gauge_default_awg": 22, "nested": {"a": 1}}
    m = settings.merge(d, over)
    assert m["gauge_default_awg"] == 22 and m["nested"]["a"] == 1
    deep = settings.merge({"nested": {"a": 0, "b": 2}}, {"nested": {"a": 1}})
    assert deep["nested"] == {"a": 1, "b": 2}


def test_roles_cover_every_kind():
    for k in KINDS:
        assert k in ROLES_OF_KIND and set(ROLES_OF_KIND[k]) <= set(ROLES)


def test_gauge_radius_is_half_the_od():
    g = Gauge(awg=22, conductor_d_mm=0.6, od_mm=1.8, min_bend_r_mm=3.2, g_per_mm=0.003, amps_cont=1.5,
              amps_burst=5.0, ohm_per_m=0.05, strands="65/0.08")
    assert abs(g.r_mm - 0.9) < 1e-9


def test_connector_pin_offsets_are_centred():
    c = ConnectorType(id="jst_ph_2", family="jst_ph", pins=2, pitch_mm=2.0, body_mm=(5, 7, 3), gender="m",
                      amps_per_pin=2.0, awg_min=28, awg_max=22, mass_g=0.2, unplug_mm=2.0, boot_mm=1.5)
    pts = c.pin_offsets()
    assert pts.shape == (2, 3) and abs(pts[:, 1].sum()) < 1e-9  # pins spread on Y, centred


def test_netlist_kinds_are_the_declared_ones():
    assert set(ROLES_OF_KIND) == set(KINDS)
    n = Net(id="bat_plus", kind="power", role="pos")
    assert n.kind in KINDS and n.role in ROLES_OF_KIND[n.kind]
