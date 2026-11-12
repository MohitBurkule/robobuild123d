"""Schema sanity for robot/hardware/data: sources cited, dimensions physically ordered, monotonic by size, no dupes,
every record reachable by a designation string."""

from collections import defaultdict

import pytest

from robot import hardware as hw
from robot.hardware import registry as reg


def recs(kind):
    r = reg.records(kind)
    if not r:
        pytest.skip(f"no {kind} data ({reg.load_errors().get(kind, 'empty')})")
    return r


def test_all_modules_import():
    assert reg.load_errors() == {}


@pytest.mark.parametrize("kind", reg.KINDS)
def test_every_record_cites_a_source(kind):
    for r in recs(kind):
        assert r.src.standard.strip(), r
        fields = set(type(r).__dataclass_fields__)
        assert set(r.src.uncertain_fields) <= fields, (r, set(r.src.uncertain_fields) - fields)


@pytest.mark.parametrize("kind", reg.KINDS)
def test_no_duplicates(kind):
    keyf = {"thread": lambda r: r.d, "screw": lambda r: (r.family, r.standard, r.d),
            "nut": lambda r: (r.family, r.standard, r.d), "washer": lambda r: (r.family, r.standard, r.d),
            "insert": lambda r: (r.maker, r.part_no), "standoff": lambda r: (r.family, r.d, r.length),
            "pin": lambda r: (r.family, r.standard, r.d), "circlip": lambda r: (r.family, r.shaft_d),
            "bearing": lambda r: r.designation, "oring": lambda r: (r.id, r.cs),
            "shaft": lambda r: (r.d, r.form, r.tolerance)}[kind]
    keys = [keyf(r) for r in recs(kind)]
    dupes = {k for k in keys if keys.count(k) > 1}
    assert not dupes


def test_threads():
    for t in recs("thread"):
        assert t.d_minor_ext < t.tap_drill < t.d and t.d_minor_ext < t.d_pitch < t.d and t.pitch > 0
        assert t.stress_area > 0


def _groups(rs, key):
    g = defaultdict(list)
    for r in rs:
        g[key(r)].append(r)
    return g


def test_screw_heads():
    for r in recs("screw"):
        if r.family.startswith("grub"):
            assert r.dk == r.d and r.k == 0
            continue
        assert r.dk > r.d and r.k > 0, r
        if r.drive == "hex" and r.s:
            assert r.s < r.dk and (r.t is None or r.t < r.k + 1e-9 or r.family == "csk"), r
        if r.family == "csk":
            assert r.csk_angle == 90
        assert list(r.lengths) == sorted(set(r.lengths)), r
    for key, g in _groups(recs("screw"), lambda r: (r.family, r.standard)).items():
        g = sorted(g, key=lambda r: r.d)
        for a, b in zip(g, g[1:]):
            assert b.dk >= a.dk and b.k >= a.k, (key, a.d, b.d)


def test_nuts_washers():
    for n in recs("nut"):
        assert n.s > n.d and n.m > 0
        if n.e is not None:
            assert n.s < n.e <= n.s * 2 / 3 ** 0.5 + 1e-6, n
    for key, g in _groups(recs("nut"), lambda r: (r.family, r.standard)).items():
        g = sorted(g, key=lambda r: r.d)
        assert all(b.s >= a.s and b.m >= a.m for a, b in zip(g, g[1:])), key
    for w in recs("washer"):
        assert w.d < w.d1 + 1e-9 < w.d2 and w.h > 0, w


def test_inserts_standoffs_pins():
    for i in recs("insert"):
        assert i.d < i.bore < i.od + 1e-9 and i.bore_depth_min >= i.length, i
    for s in recs("standoff"):
        assert s.af > s.d and s.length > 0
    for p in recs("pin"):
        assert p.lengths and list(p.lengths) == sorted(p.lengths) and p.lengths[0] > p.d / 2


def test_circlips_bearings_orings_shafts():
    for c in recs("circlip"):
        if c.family.startswith("int"):
            assert c.groove_d > c.shaft_d, c
        else:
            assert c.groove_d < c.shaft_d, c
        assert c.groove_w >= c.thickness, c
    for b in recs("bearing"):
        assert b.D > b.d and b.B > 0, b
        if b.flange_D:
            assert b.flange_D > b.D and b.flange_B < b.B
    for o in recs("oring"):
        assert o.cs > 0 and o.id > 0
        if o.groove_depth:
            assert o.groove_depth < o.cs < o.groove_w
    for s in recs("shaft"):
        assert s.d > 0 and (s.flat_depth is None or s.flat_depth < s.d / 2)


def test_lookup_round_trips():
    for r in recs("screw"):
        assert hw.get(f"M{r.d:g}x{r.lengths[0]:g} {r.standard} {r.family.split('_')[0]}").record == r
    for n in recs("nut"):
        assert hw.get(f"M{n.d:g} {n.family} nut {n.standard}").record == n
    for b in recs("bearing"):
        assert hw.get(b.designation).record == b
    for o in recs("oring"):
        assert hw.get(f"oring {o.id:g}x{o.cs:g}").record == o
    for i in recs("insert"):
        got = hw.get(f"M{i.d:g}x{i.length:g} insert {i.maker}").record
        assert (got.d, got.length, got.maker) == (i.d, i.length, i.maker)
