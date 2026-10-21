"""Design-intent probes (robot.checks.intent): each rule fails on a part that has the shape but not the function,
and passes on one that works."""

import math

import numpy as np
import trimesh
from shapely.geometry import Point, Polygon

from robot.checks import intent as I


def _box(lo, hi):
    b = trimesh.creation.box(np.subtract(hi, lo))
    b.apply_translation(np.add(lo, hi) / 2)
    return b


def _hub(bore="round", crest=6.0):
    """Hub along Z (0..10), seat radius `crest`, 3 mm bore (round or D with a 2.5 flat)."""
    hub = trimesh.creation.cylinder(crest, 10, sections=96)
    hub.apply_translation((0, 0, 5))
    p = Point(0, 0).buffer(1.5, 64)
    if bore == "D":
        p = p.intersection(Polygon([(-2, -2), (2, -2), (2, 1.0), (-2, 1.0)]))
    c = trimesh.creation.extrude_polygon(p, 14)
    c.apply_translation((0, 0, -2))
    return hub.difference(c)


def test_keyed_bore():
    assert set(I.keyed_bore_probe(_hub("round"), "z", (0, 0, 0), (1, 9))) == {"round"}
    assert set(I.keyed_bore_probe(_hub("D"), "z", (0, 0, 0), (1, 9))) == {"D"}


def test_support_free():
    ok = _box((0, 0, 0), (10, 10, 5))
    t = _box((0, 0, 0), (10, 10, 1)).union(_box((0, 0, 1), (2, 10, 6))).union(_box((0, 0, 6), (10, 10, 7)))  # table top
    assert I.overhang_frac(ok, (0, 0, 1))[0] == 0
    assert I.overhang_frac(t, (0, 0, 1))[0] > 0.05


def test_min_wall():
    thin = _box((0, 0, 0), (20, 20, 10)).difference(_box((1, 1, 1), (19, 19, 11)))   # 1 mm walls
    thick = _box((0, 0, 0), (20, 20, 10)).difference(_box((2, 2, 2), (18, 18, 11)))
    for m, bad in ((thin, True), (thick, False)):
        p, t = I.wall_thickness(m)
        assert (np.mean(t < 1.8) > 0.02) == bad


def test_fillet_on_load_corner():
    sharp = _box((0, 0, 0), (10, 2, 5)).union(_box((0, 0, 0), (2, 10, 5)))   # L, inside corner at (2, 2)
    L = Polygon([(0, 0), (10, 0), (10, 2), (2, 2), (2, 10), (0, 10)])
    fil = L.union(Polygon([(2, 2), (4, 2), (2, 4)]).difference(Point(4, 4).buffer(2, 64)))
    rounded = trimesh.creation.extrude_polygon(fil, 5)
    assert I.sharp_corners_near(sharp, "z", 2.5, [(2, 2)])
    assert not I.sharp_corners_near(rounded, "z", 2.5, [(2, 2)])


def test_insert_column():
    floor = _box((-10, -10, 0), (10, 10, 1))
    hanging = floor.union(_box((-3, -3, 6), (3, 3, 10)))
    column = floor.union(_box((-3, -3, 0), (3, 3, 10)))
    assert I.column_gaps(hanging, [(0, 0, 6)], 1.0, 2.2)
    assert not I.column_gaps(column, [(0, 0, 6)], 1.0, 2.2)


def test_tyre_retention():
    assert 2 * I.seat_radius(_hub(crest=6.05), "z", (0, 0, 0), (0, 10)) - 12 < 1.0
    assert 2 * I.seat_radius(_hub(crest=7.0), "z", (0, 0, 0), (0, 10)) - 12 >= 1.0


def test_captive_nut():
    nut = trimesh.creation.cylinder(2.5, 2, sections=6)
    nut.apply_translation((0, 0, 3))
    block = _box((-6, -6, 0), (6, 6, 8))
    pocket = trimesh.creation.cylinder(2.55, 2.1, sections=6)
    pocket.apply_translation((0, 0, 3))
    closed = block.difference(pocket)
    slot = closed.difference(_box((-2.55, -2.2, 3), (2.55, 2.2, 9)))   # drop-in slot from above
    assert not I.escape_dirs(nut, [closed])
    assert (0.0, 0.0, 1.0) in I.escape_dirs(nut, [slot])


def test_wheel_clearance():
    w = trimesh.creation.cylinder(5, 3, sections=64)
    near = _box((5.5, -3, -3), (8, 3, 3))
    far = _box((6.5, -3, -3), (9, 3, 3))
    assert I.min_gap(w, [("a", near)])[0] < 1.0
    assert I.min_gap(w, [("a", far)])[0] >= 1.0


def test_flush_head():
    host = _box((-10, -10, 0), (10, 10, 4))
    sunk = trimesh.creation.cylinder(2, 2, sections=32)
    sunk.apply_translation((0, 0, 3))
    proud = sunk.copy()
    proud.apply_translation((0, 0, 2))
    host = host.difference(trimesh.creation.cylinder(2.1, 10, sections=32))
    assert I.proud(sunk, host, (0, 0, 1)) <= 0.2
    assert I.proud(proud, host, (0, 0, 1)) > 0.2


def test_notch_bears():
    plate = _box((0, 0, 0), (2, 20, 10)).difference(_box((-1, 8, -1), (3, 12, 3)))   # notch 8..12 at the bottom
    plate = plate.difference(trimesh.creation.cylinder(1.6, 10, sections=32).apply_transform(
        trimesh.transformations.rotation_matrix(math.pi / 2, (0, 1, 0))).apply_translation((1, 4, 6)))
    bolt = trimesh.creation.cylinder(1.5, 6, sections=32).apply_transform(
        trimesh.transformations.rotation_matrix(math.pi / 2, (0, 1, 0))).apply_translation((1, 4, 6))
    tight_lug = _box((0.5, 8.05, -1), (1.5, 11.95, 2.5))
    loose_lug = _box((0.5, 9.0, -1), (1.5, 11.0, 2.5))
    d = (0, -1, 0)
    assert I.first_contact(plate, [tight_lug], d) < I.first_contact(plate, [bolt], d)
    assert I.first_contact(plate, [loose_lug], d) > I.first_contact(plate, [bolt], d)


def test_seat_locates():
    motor = trimesh.creation.cylinder(2.1, 3, sections=64)   # gearbox boss along Z
    motor = motor.union(_box((-5, -6, -6), (5, 6, -1.5)))     # body
    seat = _box((-8, -8, -1.5), (8, 8, 1.5)).difference(trimesh.creation.cylinder(2.15, 6, sections=64))
    stops = seat.union(_box((-8, 6.05, -7), (8, 8, -1.5))).union(_box((-8, -8, -7), (8, -6.05, -1.5)))
    shaft_only = _box((-8, -8, -1.5), (8, 8, 1.5)).difference(trimesh.creation.cylinder(3.0, 6, sections=64))
    assert not I.seat_free(motor, stops, (0, 0, 1), (0, 0, 0))
    assert I.seat_free(motor, shaft_only, (0, 0, 1), (0, 0, 0))


def test_wire_clear_rotor():
    disc = trimesh.creation.cylinder(20, 3, sections=64)
    rmax, a0, a1 = I.rotor_envelope([disc], (0, 0, 1), (0, 0, 0))
    assert I.swept_gap(np.array([[21, 0, 0]]), (0, 0, 1), (0, 0, 0), rmax, a0, a1).min() < 2
    assert I.swept_gap(np.array([[23, 0, 0], [0, 0, 5]]), (0, 0, 1), (0, 0, 0), rmax, a0, a1).min() >= 2


def test_tool_count():
    from types import SimpleNamespace as NS

    def ctx(tools):
        fs = [{"id": f"b{i}", "tool": t} for i, t in enumerate(tools)]
        return NS(r=NS(spec=NS(raw={"fasteners": fs})))
    e = {"rule": "tool_count", "max": 2, "module_max": 1, "module": ["b0", "b1"]}
    assert I._rule(ctx(["hex2", "hex2", "hex1.3"]), e)[0]
    assert not I._rule(ctx(["hex2", "hex1.5", "hex1.3"]), e)[0]
    assert not I._rule(ctx(["hex2", "hex1.3"]), e)[0]   # the module swap needs two keys


def test_fillet_exempt():
    found = [(2.0, 2.0)]
    cite = "RVRN STEP RV01 has a sharp inside corner here"
    b, m, s = I.fillet_exempt(found, [{"at": [2.2, 2.1], "reason": cite}])
    assert not b and m == [((2.0, 2.0), cite)] and not s                      # valid -> INFO
    b, m, s = I.fillet_exempt(found, [{"at": [2.0, 2.0], "reason": "the original has it sharp too"}])
    assert b and "invalid exemption" in b[0][1] and not m                     # missing citation blocks
    b, m, s = I.fillet_exempt(found, [{"at": [3.0, 2.0], "reason": cite}])
    assert b == [((2.0, 2.0), "")] and not m and len(s) == 1                  # far point doesn't exempt (and is stale)
    b, m, s = I.fillet_exempt([], [{"at": [9, 9], "reason": cite}])
    assert not b and not m and s == [{"at": [9, 9], "reason": cite}]         # stale -> warning


def test_fillet_exempt_corner_still_probed():
    sharp = _box((0, 0, 0), (10, 2, 5)).union(_box((0, 0, 0), (2, 10, 5)))
    f = I.sharp_corners_found(sharp, "z", 2.5, [(2, 2)])
    assert f and all(abs(x - 2) < 0.5 and abs(y - 2) < 0.5 for x, y in f)


def _slot_roof(width, angle_deg):
    """30 x 30 x 8 block (printed +Z) with a 3 mm tall slot of `width` running through it at `angle_deg` to X, under
    a 3 mm roof: the roof is an overhang as wide as the slot."""
    blk = _box((-15, -15, 0), (15, 15, 8))
    slot = _box((-30, -width / 2, 2), (30, width / 2, 5))
    slot.apply_transform(trimesh.transformations.rotation_matrix(math.radians(angle_deg), (0, 0, 1)))
    return blk.difference(slot)


def test_bridge_span_is_the_narrowest_width():
    x, y = np.array([0, 10, 10, 0.0]), np.array([0, 0, 2.9, 2.9])
    c, s = math.cos(math.radians(30)), math.sin(math.radians(30))
    assert abs(I.bridge_span(x * c - y * s, x * s + y * c) - 2.9) < 0.05   # a slanted strip: its width, not its run


def test_slanted_narrow_slot_roof_bridges():
    for ang in (0, 24, 45):
        a, f, _ = I.unsupported(_slot_roof(2.9, ang), (0, 0, 1))
        assert a == 0, (ang, a)


def test_wide_slot_roof_needs_support_at_any_angle():
    for ang in (0, 24):
        a, f, _ = I.unsupported(_slot_roof(8.0, ang), (0, 0, 1))
        assert a > 0, (ang, a)
