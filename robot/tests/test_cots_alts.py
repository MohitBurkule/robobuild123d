"""cots_alts: vendor-sourced alternative parts build as valid solids at their datasheet sizes, carry sources, and swap
with the existing catalogue entries (same kind / ports / shaft / props interface)."""

import math

import pytest

from robot import catalog, cots_alts, shapes

ENTRIES = {e.id: e for e in cots_alts.entries()}


def _solid(e):
    return shapes.to_solid(e.shape)


def _size(e):
    b = _solid(e).bounding_box()
    return b.size.X, b.size.Y, b.size.Z


def test_ids_unique_and_findable():
    ids = [e.id for e in catalog.catalog()]
    assert len(ids) == len(set(ids))
    for cid in ENTRIES:
        assert catalog.find(cid) is not None


def test_every_part_has_a_source():
    src = cots_alts.sources()
    for cid in ENTRIES:
        s = src[cid]
        assert s and any(str(v).startswith(("http", "research/", "XT30U", "Pololu", "same sheet")) for v in s.values()), cid


@pytest.mark.parametrize("cid", sorted(ENTRIES))
def test_builds_one_valid_solid(cid):
    s = _solid(ENTRIES[cid])
    assert s.is_valid
    assert len(s.solids()) == 1
    assert s.volume > 0


@pytest.mark.parametrize("cid,kind_like", [("repeat_2004_1400kv", "gr1507"), ("bbb_n10_600rpm", "n10_2200rpm_spicy"),
                                           ("gnb_2s_350_70c_hv", "lipo_2s_180"), ("bbb_wheel_34x6_5", "wheel_28x10"),
                                           ("bbb_malenki_nano", "malenki_nano"), ("bbb_brushless_esc_20a", "bbb_ant_esc")])
def test_swaps_with_existing_entry(cid, kind_like):
    new, old = ENTRIES[cid], catalog.find(kind_like)
    assert new.kind == old.kind
    assert set(old.ports) <= set(new.ports) or new.kind == "battery"
    assert (new.shaft is None) == (old.shaft is None)
    if new.shaft:
        assert new.shaft["dir"] == [1, 0, 0] and set(new.shaft) == set(old.shaft)
    for key in {"weapon_motor": ("kv", "max_current_a", "typ_current_a", "bell_mass_frac"),
                "motor": ("nominal_v", "rpm_nominal"), "battery": ("cells", "capacity_mah", "c_rating", "nominal_v"),
                "esc": ("cont_current_a", "burst_current_a", "channels"), "wheel": ("diameter_mm", "width_mm", "friction")}[new.kind]:
        assert key in new.props, (cid, key)


@pytest.mark.parametrize("cid", [k for k, e in ENTRIES.items() if e.kind == "weapon_motor"])
def test_outrunner_matches_datasheet(cid):
    s = cots_alts._resolve(cots_alts.WEAPON_MOTORS)[cid]
    x, y, z = _size(ENTRIES[cid])
    assert x == pytest.approx(s["overall"], abs=0.05)
    assert z == pytest.approx(s["bell_d"], abs=0.05)
    assert ENTRIES[cid].shaft["dia"] == s["shaft_d"]


def test_repeat_2004_drawing_numbers():
    s = cots_alts.WEAPON_MOTORS["repeat_2004_1400kv"]
    assert (s["bell_d"], s["overall"], s["body_len"], s["shaft_d"]) == (24.7, 30.25, 14.8, 3.0)
    assert s["base_holes"] == [(15.0, 3, 3.0)]


@pytest.mark.parametrize("cid", [k for k, e in ENTRIES.items() if e.kind == "motor"])
def test_gearmotor_envelope(cid):
    s = cots_alts._resolve(cots_alts.GEARMOTORS)[cid]
    f = cots_alts.GEARMOTOR_FORMAT
    x, y, z = _size(ENTRIES[cid])
    assert (y, z) == (pytest.approx(f["gb_w"]), pytest.approx(f["gb_h"]))
    if "overall" in s:
        assert x == pytest.approx(s["overall"], abs=0.05)
    assert ENTRIES[cid].shaft["dia"] == 3.0


def test_gearmotor_has_d_flat_and_mount_holes():
    e = ENTRIES["pololu_hpcb6v_50to1"]
    sol = _solid(e)
    f = cots_alts.GEARMOTOR_FORMAT
    tip = e.shaft["at"][0] + e.shaft["len"] - 0.5
    from build123d import Vector
    assert sol.is_inside(Vector(tip, 0, -f["shaft_d"] / 2 + 0.1))           # round side
    assert not sol.is_inside(Vector(tip, 0, f["shaft_d"] / 2 - 0.1))        # flat side cut away
    x1 = e.shaft["at"][0]
    assert not sol.is_inside(Vector(x1 - 0.5, f["hole_dx"], 0))             # M1.6 hole
    assert sol.is_inside(Vector(x1 - 0.5, 0, f["gb_h"] / 2 - 0.5))


@pytest.mark.parametrize("cid", list(cots_alts.BATTERIES))
def test_battery_pack_size(cid):
    s = cots_alts.BATTERIES[cid]
    x, _, z = _size(ENTRIES[cid])
    assert x == pytest.approx(s["l"], abs=0.05) and z == pytest.approx(s["h"], abs=0.05)
    assert ENTRIES[cid].props["cells"] == s["cells"] and s["conn"] in ENTRIES[cid].ports


def test_xt30_drawing():
    for cid in ("xt30u_m", "xt30u_f"):
        s = cots_alts.CONNECTORS[cid]
        assert _size(ENTRIES[cid]) == (pytest.approx(s["l"]), pytest.approx(5.2), pytest.approx(10.2))


def test_fingertech_switch():
    e = ENTRIES["fingertech_mini_switch"]
    x, y, z = _size(e)
    assert (x, z) == (pytest.approx(12.7), pytest.approx(6.35))
    assert y == pytest.approx(12.7 + 6.35, abs=0.06)
    assert e.mass_g == 2.15


# ------------------------------------------------------------------------------ parametric wheels / tyres
def test_wheel_generator_is_parametric():
    a = cots_alts.wheel(od=30, width=8, tyre_t=4)
    b = cots_alts.wheel(od=40, width=12, tyre_t=4)
    sa, sb = _size(a), _size(b)
    assert sa[1] == pytest.approx(30) and sb[1] == pytest.approx(40)
    assert sb[0] > sa[0]
    assert b.mass_g > a.mass_g
    assert a.id != b.id and a.props["params"]["od"] == 30


def test_wheel_bore_and_d_flat():
    from build123d import Vector
    e = cots_alts.wheel(od=30, width=8, bore=3.0, d_flat=2.5, boss_len=0)
    s = _solid(e)
    assert not s.is_inside(Vector(0, 0, -1.4))   # inside the bore
    assert not s.is_inside(Vector(0, -1.4, 0))
    assert s.is_inside(Vector(0, 1.2, 0))        # D-flat: material at the flat (flat 2.5 across -> y > 1.0 is solid)
    with pytest.raises(ValueError):
        cots_alts.wheel(od=30, bore=3.0, d_flat=3.5)


def test_tread_removes_material():
    smooth = _solid(cots_alts.tyre(od=30, width=8, tyre_t=3))
    blocks = _solid(cots_alts.tyre(od=30, width=8, tyre_t=3, tread="blocks", tread_n=24, tread_depth=0.8))
    grooves = _solid(cots_alts.tyre(od=30, width=8, tyre_t=3, tread="grooves", tread_n=2, tread_depth=0.8))
    assert blocks.volume < smooth.volume and grooves.volume < smooth.volume
    r_o, r_i = 15, 12
    assert smooth.volume == pytest.approx(math.pi * (r_o ** 2 - r_i ** 2) * 8, rel=1e-3)


def test_bbb_34_wheel_matches_vendor_step():
    # vendor STEP (research/cots/wheel/bbb_wheels/cad_ref): OD 34, 8.6 wide incl. boss, rim r13.75, bore r1.5
    e = ENTRIES["bbb_wheel_34x6_5"]
    x, y, z = _size(e)
    assert y == pytest.approx(34) and x == pytest.approx(8.6, abs=0.15)
    assert e.props["params"]["od"] / 2 - e.props["tyre_t_mm"] == pytest.approx(13.75)
