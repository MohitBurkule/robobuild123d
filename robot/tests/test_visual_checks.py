"""Visual-review gates (robot.checks.visual, wire.render_wires): each one fails a part that differs from its reference the
way the RVRN 2.0 visual review saw (extra slab, missing countersink, polygon arc, sharp root, sliver, render without
wires) and passes a part that matches, including a reference that has the same "defect" itself."""

import json
import math

import numpy as np
import pytest
import trimesh
from shapely.geometry import Polygon

from robot.checks import visual, wire_review


def _box(ext, at=(0, 0, 0)):
    b = trimesh.creation.box(ext)
    b.apply_translation(at)
    return b


def _union(*ms):
    return trimesh.boolean.union(list(ms))


# ------------------------------------------------------------------ silhouette / depth
def test_identical_part_passes_every_view():
    m = _box((20, 10, 4))
    for d in visual.VIEWS.values():
        iou, blobs = visual.view_diff(m, m.copy(), d)
        assert iou > 0.99 and not blobs


def test_extra_slab_outside_outline_fails():
    ref = _box((20, 10, 4))
    ours = _union(ref, _box((4, 4, 4), (12, 0, 0)))   # a tab sticking out of the end
    iou, blobs = visual.view_diff(ours, ref, visual.VIEWS["top"])
    assert any(b["kind"] == "extra outline" for b in blobs), blobs


def test_slab_inside_outline_fails_by_depth():
    """An extra slab on top of a plate is inside the top-view outline (IoU 1.0): only the depth map sees it."""
    ref = _box((20, 10, 4))
    ours = _union(ref, _box((6, 6, 1.5), (0, 0, 2.7)))
    iou, blobs = visual.view_diff(ours, ref, visual.VIEWS["top"])
    assert iou > 0.99
    assert any(b["kind"] == "proud surface" for b in blobs), blobs


def test_missing_spur_fails():
    ref = _union(_box((20, 10, 4)), _box((3, 5, 4), (0, 7, 0)))
    ours = _box((20, 10, 4))
    _, blobs = visual.view_diff(ours, ref, visual.VIEWS["top"])
    assert any(b["kind"] == "missing outline" for b in blobs), blobs


# ------------------------------------------------------------------ holes on every axis
def _block(csk):
    """10 x 30 x 30 block, a d2.2 hole along X (the thick direction is NOT the thin axis: Y/Z are 30, X is 10 - so
    put the hole along Y, a non-thin axis) with or without a countersink at the +Y face."""
    m = _box((10, 30, 30))
    h = trimesh.creation.cylinder(1.1, 40, sections=64)
    h.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, (1, 0, 0)))
    h.apply_translation((0, 0, 6))
    m = m.difference(h)
    if csk:
        c = trimesh.creation.cone(2.5, 2.5, sections=64)
        c.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, (1, 0, 0)))   # apex towards -Y
        c.apply_translation((0, 15.0 - 2.5 + 2.5, 6))
        c.apply_translation((0, -2.5, 0))
        m = m.difference(c)
    return m


def test_missing_countersink_on_side_axis_fails():
    d = visual.hole_diffs(_block(False), _block(True))
    assert any(x["kind"] == "kind" and x["axis"] == "Y" for x in d), d


def test_matching_holes_pass():
    assert visual.hole_diffs(_block(True), _block(True)) == []


def test_missing_hole_fails():
    d = visual.hole_diffs(_box((10, 30, 30)), _block(False))
    assert any(x["kind"] == "missing" for x in d), d


# ------------------------------------------------------------------ faceting
def _disc(n):
    return trimesh.creation.cylinder(8.0, 4.0, sections=n)


def test_polygon_arc_fails_against_smooth_reference():
    regs = visual.faceted_regions(_disc(18), _disc(360))
    assert regs and regs[0]["len_mm"] > 20, regs


def test_smooth_arc_passes():
    assert visual.faceted_regions(_disc(360), _disc(360)) == []


def test_faceting_the_reference_has_too_is_not_flagged():
    assert visual.faceted_regions(_disc(18), _disc(18)) == []


# ------------------------------------------------------------------ concave fillet vs reference
def _l_bracket(r):
    """L section (20 x 20, 4 thick) extruded 10 along Z, inside root filleted r (0 = sharp)."""
    pts = [(0, 0), (20, 0), (20, 4), (4 + r, 4)]
    if r > 0:
        for a in np.linspace(-math.pi / 2, -math.pi, 24)[1:-1]:
            pts.append((4 + r + r * math.cos(a), 4 + r + r * math.sin(a)))
        pts.append((4, 4 + r))
    pts += [(4, 20), (0, 20)]
    return trimesh.creation.extrude_polygon(Polygon(pts), 10)


def test_sharp_root_where_reference_is_filleted_fails():
    hits = visual.fillet_diffs(_l_bracket(0), _l_bracket(2.0), grid=1.0)
    assert len(hits) >= 3 and min(h[2] for h in hits) > 1.5, hits


def test_matching_fillet_passes():
    assert visual.fillet_diffs(_l_bracket(2.0), _l_bracket(2.0), grid=1.0) == []


def test_sharp_root_the_reference_also_has_passes():
    assert visual.fillet_diffs(_l_bracket(0), _l_bracket(0), grid=1.0) == []


# ------------------------------------------------------------------ slivers
def _stepped(h):
    """Box with a second box on top offset by h in Y: a step face h tall (a sliver when h is tiny)."""
    return _union(_box((20, 10, 4)), _box((20, 10, 2), (0, h, 3)))


def test_sliver_face_is_found_and_relative():
    bad, good = _stepped(0.01), _box((20, 10, 5))
    s = visual.slivers(bad)
    assert s and min(x[2] for x in s) < 0.05, s
    assert visual.slivers(good) == []


# ------------------------------------------------------------------ exemption reasons
def test_exemption_must_cite_reference():
    assert visual.cites("RV01 roots are sharp in the STEP too")
    assert not visual.cites("looks fine")
    out = []
    assert visual._part_ok({"visual_ok": {"faceting": "fine"}}, "faceting", out, "p") is None
    assert out and out[0].id == "visual.exempt_reason"


def test_deviation_covers_point():
    e = {"deviations": [{"near": [0, 0, 0], "r": 2, "reason": "STEP notch is a knife edge"}]}
    assert visual.covered(e, [1, 0, 0]) and visual.covered(e, [3, 0, 0]) is None
    assert visual.covered({"deviations": [{"near": [0, 0, 0], "r": 2, "reason": "flared for strength"}]}, [1, 0, 0]) is None


# ------------------------------------------------------------------ renders must show the wires
def _png(tmp_path, name, rec):
    p = tmp_path / name
    p.write_bytes(b"\x89PNG")
    if rec is not None:
        (tmp_path / (name + ".json")).write_text(json.dumps(rec))
    return p


def test_robot_render_without_wires_fails(tmp_path):
    p = _png(tmp_path, "robot_iso.png", {"bodies": [f"b{i}" for i in range(10)], "wires": {}})
    assert wire_review.robot_render_wires(p, ["w1", "w2"], 10)


def test_robot_render_without_record_fails(tmp_path):
    assert wire_review.robot_render_wires(_png(tmp_path, "iso.png", None), ["w1"], 10)


def test_robot_render_with_every_wire_passes(tmp_path):
    p = _png(tmp_path, "iso.png", {"bodies": [f"b{i}" for i in range(10)], "wires": {"w1": {}, "w2": {}}})
    assert wire_review.robot_render_wires(p, ["w1", "w2"], 10) == []


def test_part_render_is_not_a_robot_render(tmp_path):
    assert wire_review.robot_render_wires(_png(tmp_path, "part_tub.png", None), ["w1"], 10) is None


# ------------------------------------------------------------------ dangling leads
def _lead_ctx(wires, routes):
    from types import SimpleNamespace as NS

    motor = NS(part=NS(id="mot", _extra={}), cat=NS(ports={"phases": [0, 0, 0]}))
    esc = NS(part=NS(id="esc", _extra={}), cat=NS(ports={"motor": [10, 0, 0]}))
    pos = {"mot.phases": np.array([0.0, 0, 0]), "esc.motor": np.array([10.0, 0, 0])}
    r = NS(parts=[motor, esc], spec=NS(wires=wires))
    return NS(r=r, world=NS(port=lambda r, n: pos.get(n)), routes=routes, not_checked=[])


def test_lead_with_no_wire_is_dangling():
    out = visual.leads(_lead_ctx([], []), visual.DEFAULTS)
    assert out and out[0].id == "visual.lead" and not out[0].passed


def test_route_that_stops_short_of_the_lead_fails():
    from types import SimpleNamespace as NS

    w = NS(id="w", to="mot.phases", **{"from": "esc.motor"})
    rt = NS(id="w", points=[[10, 0, 0], [5, 0, 0]])
    out = visual.leads(_lead_ctx([w], [rt]), visual.DEFAULTS)
    assert not out[0].passed and "ends" in out[0].message


def test_routed_lead_passes():
    from types import SimpleNamespace as NS

    w = NS(id="w", to="mot.phases", **{"from": "esc.motor"})
    rt = NS(id="w", points=[[10, 0, 0], [0.2, 0, 0]])
    out = visual.leads(_lead_ctx([w], [rt]), visual.DEFAULTS)
    assert out[0].passed


# ------------------------------------------------------------------ rev2: shaft/bore profile mate
def _d_prism(r, flat, h, sections=96):
    from shapely.geometry import Point
    p = Point(0, 0).buffer(r, sections).intersection(Polygon([(-9, -9), (9, -9), (9, flat), (-9, flat)]))
    m = trimesh.creation.extrude_polygon(p, h)
    m.apply_translation((0, 0, -h / 2))
    return m


def _hub(bore):
    hub = trimesh.creation.cylinder(6.0, 8.0, sections=96)
    return hub.difference(bore)


def test_round_shaft_in_d_bore_fails():
    shaft = trimesh.creation.cylinder(1.5, 12.0, sections=96)
    hub = _hub(_d_prism(1.5, 1.0, 20))
    rows = visual.shaft_mate(shaft, hub, (0, 0, -3), (0, 0, 1), 6.0)
    assert rows and all(s == "round" and b == "D" for _, s, b in rows), rows


def test_d_shaft_in_d_bore_passes():
    shaft = _d_prism(1.45, 0.95, 12)
    hub = _hub(_d_prism(1.5, 1.0, 20))
    rows = visual.shaft_mate(shaft, hub, (0, 0, -3), (0, 0, 1), 6.0)
    assert rows and all(s == b == "D" for _, s, b in rows), rows



def _tyre():
    """Tyre: r10 ring with a round r6 bore stretched over the hub (revron wheel_rl over whub_rl)."""
    return trimesh.creation.cylinder(10.0, 8.0, sections=96).difference(trimesh.creation.cylinder(6.0, 20.0, sections=96))


def test_shaft_not_paired_with_tyre_round_hub():
    """Bad pairing: the tyre's round bore surrounds the shaft but the hub lies between - no rows, no finding."""
    shaft = trimesh.creation.cylinder(1.5, 12.0, sections=96)
    assert visual.shaft_mate(shaft, _tyre(), (0, 0, -3), (0, 0, 1), 6.0) == []


def test_shaft_paired_with_hub_inside_tyre():
    """Good pairing: the D-bore hub inside the tyre is still the shaft's mate and its mismatch is reported."""
    shaft = trimesh.creation.cylinder(1.5, 12.0, sections=96)
    hub = _hub(_d_prism(1.5, 1.0, 20))
    rows = visual.shaft_mate(shaft, hub, (0, 0, -3), (0, 0, 1), 6.0)
    assert rows and all(s == "round" and b == "D" for _, s, b in rows), rows

# ------------------------------------------------------------------ rev2: wall round a bore
def _seat_block(y):
    """20 x 20 x 6 block (Z 0..6) with a d8 bore along Z centred at (0, y): y 4.0 leaves 2 mm of wall, y 5.7 0.3 mm,
    y 6.5 breaks through (an open C)."""
    b = _box((20, 20, 6), (0, 0, 3))
    c = trimesh.creation.cylinder(4.0, 10, sections=96)
    c.apply_translation((0, y, 3))
    return b.difference(c)


def test_thin_bore_wall_fails():
    d = visual.ligament_diffs(_seat_block(5.7), _seat_block(4.0))
    assert any(x["kind"] == "thin" and not x["matches"] for x in d), d


def test_bore_wall_as_thin_as_reference_is_not_flagged():
    d = visual.ligament_diffs(_seat_block(5.7), _seat_block(5.7))
    assert d and all(x["matches"] for x in d), d


def test_bore_broken_through_where_reference_is_closed_fails():
    d = visual.ligament_diffs(_seat_block(6.5), _seat_block(4.0))
    assert any(x["kind"] == "open" for x in d), d


def test_healthy_bore_passes():
    assert visual.ligament_diffs(_seat_block(4.0), _seat_block(4.0)) == []


# ------------------------------------------------------------------ rev2: deviation note extent
def test_claim_box_parses_ranges():
    lo, hi = visual.claim_box("cut the 1.5 mm seat at x -26.5..-25, y 43-50", ([-30, 40, 0], [-20, 55, 10]))
    assert lo.tolist() == [-26.5, 43, 0] and hi.tolist() == [-25, 50, 10]
    assert visual.claim_box("no ranges here", ([0, 0, 0], [1, 1, 1])) is None


def test_full_height_slot_for_a_low_tine_fails():
    ref = _box((10, 10, 10), (0, 0, 5))
    slot = _box((1.5, 12, 10), (0, 0, 5))           # through the whole height
    tine = _box((1.5, 10, 2), (0, 0, 1))            # the part it seats fills only the bottom 2 mm
    vol, fill = visual.claim_fill(ref.difference(slot), ref, [tine], (np.array([-0.75, -5, 0]), np.array([0.75, 5, 10])))
    assert vol > 100 and fill < 0.3


def test_seat_cut_to_the_tine_passes():
    ref = _box((10, 10, 10), (0, 0, 5))
    seat = _box((1.5, 12, 2), (0, 0, 1))
    vol, fill = visual.claim_fill(ref.difference(seat), ref, [seat], (np.array([-0.75, -5, 0]), np.array([0.75, 5, 10])))
    assert vol > 20 and fill > 0.9


# ------------------------------------------------------------------ rev2: terminal features on catalog motors
def _term_ctx(port):
    from types import SimpleNamespace as NS

    can = trimesh.creation.cylinder(5.0, 10.0, sections=64)
    body = NS(id="mot", mesh=can, inside=lambda P: can.contains(np.asarray(P)))
    rp = NS(part=NS(id="mot"), cat=NS(id="gm", kind="motor", ports={"terminals": port}))
    return NS(r=NS(parts=[rp]), world=NS(body=lambda i: body, port=lambda r, n: np.asarray(port, float)))


def test_terminal_port_floating_off_the_can_fails():
    out = visual.terminal_findings(_term_ctx([0, 0, -5.3]), visual.DEFAULTS)
    assert out and not out[0].passed


def test_terminal_on_the_part_passes():
    out = visual.terminal_findings(_term_ctx([0, 0, -4.95]), visual.DEFAULTS)
    assert out and out[0].passed


# ------------------------------------------------------------------ ligament: face graze vs a real thin wall
def _cbore_near_edge(depth):
    """20 x 20 x 6 block (Z 0..6), d3 through bore at (0, 5.9), d7.6 counterbore `depth` deep from the top: its wall
    to the y = 10 face is 0.3 mm."""
    b = _box((20, 20, 6), (0, 0, 3))
    h = trimesh.creation.cylinder(1.5, 10, sections=96)
    h.apply_translation((0, 5.9, 3))
    cb = trimesh.creation.cylinder(3.8, 2 * depth, sections=96)
    cb.apply_translation((0, 5.9, 6))
    return b.difference(h).difference(cb)


def test_face_graze_is_a_note_not_a_blocker():
    m = _cbore_near_edge(0.15)                    # only the last slice before the top face is thin
    d = [x for x in visual.ligament_diffs(m, None) if x["at"][2] > 5.7]
    assert d and all(x["kind"] == "graze" and x["matches"] for x in d), d


def test_deep_thin_counterbore_wall_still_fails():
    m = _cbore_near_edge(3.0)
    d = visual.ligament_diffs(m, None)
    assert any(x["kind"] == "thin" and not x["matches"] for x in d), d


def test_reference_sampled_at_our_height():
    m = _cbore_near_edge(3.0)
    d = visual.ligament_diffs(m, m.copy())
    assert d and all(x["matches"] for x in d), d


# ------------------------------------------------------------------ W3: wires vs rotors, loose exterior runs, render count
def _rotor_bands():
    disc = trimesh.creation.cylinder(20.0, 3.0, sections=96)       # axis Z, swept radius 20, z -1.5..1.5
    return wire_review.swept_bands([type("B", (), {"mesh": disc})()], np.zeros(3), np.array([0, 0, 1.0]))


def test_wire_hanging_near_the_rotor_fails():
    Q = wire_review._samples(np.array([[21.0, 0, 3.0], [21.0, 10, 3.0]]))   # 1.5 mm above the disc rim plane
    gap, _ = wire_review.rotor_gaps(Q, 0.5, np.zeros(3), np.array([0, 0, 1.0]), _rotor_bands())
    assert gap < wire_review.ROTOR_MIN_MM


def test_wire_clear_of_the_rotor_passes():
    Q = wire_review._samples(np.array([[25.0, 0, 6.0], [25.0, 10, 6.0]]))
    gap, _ = wire_review.rotor_gaps(Q, 0.5, np.zeros(3), np.array([0, 0, 1.0]), _rotor_bands())
    assert gap >= wire_review.ROTOR_MIN_MM


def test_long_free_span_outside_chassis_is_unsupported():
    inside = np.array([True] * 4 + [False] * 30 + [True] * 4)
    near = np.zeros(38, bool)
    runs = wire_review.unsupported_runs(None, inside, near)
    assert max(runs)[0] > wire_review.UNSUPPORTED_MAX_MM
    near[4:34] = True                                    # clipped / in a channel all the way
    assert wire_review.unsupported_runs(None, inside, near) == []


def _count_ctx(tmp_path, drawn):
    from types import SimpleNamespace as NS

    d = tmp_path / "renders"
    d.mkdir()
    (d / "iso.png").write_bytes(b"\x89PNG")
    (d / "iso.png.json").write_text(json.dumps({"bodies": ["a"], "wires": {k: {} for k in drawn}}))
    spec = NS(base_dir=str(tmp_path), raw={}, wires=[NS(id="w1"), NS(id="w2")], parts=[])
    return NS(r=NS(spec=spec), not_checked=[])


def test_render_count_mismatch_fails(tmp_path):
    out = wire_review.render_count(_count_ctx(tmp_path, ["w1", "w2", "w_old"]))
    assert out and not out[0].passed


def test_render_count_match_passes(tmp_path):
    out = wire_review.render_count(_count_ctx(tmp_path, ["w1", "w2"]))
    assert out and out[0].passed


def test_twisted_triplet_radius_is_circumscribed_circle():
    from types import SimpleNamespace as NS

    w3 = NS(awg=24, kind="motor", count=3, _extra={})
    od = 1.6   # silicone AWG24
    assert wire_review.bundle_radius(w3) == pytest.approx(od * (0.5 + 1 / math.sqrt(3)) + wire_review.TWIST_MARGIN_MM)
    assert wire_review.bundle_radius(NS(awg=24, kind="motor", count=1, _extra={})) == pytest.approx(0.8)


def test_rotor_pivot_is_in_the_parent_frame():
    from types import SimpleNamespace as NS

    j = {"kind": "revolute", "axis": [1, 0, 0], "pivot": [-20.1, 0, 0]}
    rotor = NS(id="spider", kind="weapon", rotates_with="weapon", parent="mount", joint=j, _extra={})
    mount = NS(id="mount", kind="structure", rotates_with="fixed", parent=None, joint=None, _extra={})
    spec = NS(parts=[rotor, mount], fasteners=[], part=lambda i: {"spider": rotor, "mount": mount}.get(i))
    M = np.eye(4)
    M[:3, 3] = (13.4, 38.5, 23.5)
    world = NS(body=lambda i: NS(M=M) if i == "mount" else None)
    (grp, piv, ax, ids), = wire_review.rotor_groups(spec, world)
    assert piv.tolist() == pytest.approx([-6.7, 38.5, 23.5]) and ax.tolist() == [1, 0, 0]


def _tube_cloud(enclose):
    """Points of a 3 mm bore round the X axis (enclose) or of a plate under it only (one side)."""
    th = np.linspace(0, 2 * math.pi, 48, endpoint=False) if enclose else np.linspace(math.pi * 1.25, math.pi * 1.75, 12)
    xs = np.linspace(0, 20, 41)
    return np.array([(x_, 1.5 * math.cos(t), 1.5 * math.sin(t)) for x_ in xs for t in th])


def test_wire_through_a_hole_is_enclosed():
    Q = wire_review._samples(np.array([[0.0, 0, 0], [20.0, 0, 0]]))
    near = wire_review.enclosed(Q, np.zeros(len(Q), bool), _tube_cloud(True), 2.5)
    assert near.all()


def test_wire_lying_along_a_face_is_not_retained():
    Q = wire_review._samples(np.array([[0.0, 0, 0], [20.0, 0, 0]]))
    near = wire_review.enclosed(Q, np.zeros(len(Q), bool), _tube_cloud(False), 2.5)
    assert not near.any()
    assert max(wire_review.unsupported_runs(Q, np.zeros(len(Q), bool), near))[0] > wire_review.UNSUPPORTED_MAX_MM


# ------------------------------------------------------------------ finding locations are on the geometry (no fake waiver points)
def test_two_coaxial_missing_holes_are_reported_at_each_end():
    ref = _box((60, 10, 10), (0, 0, 5))
    for x0 in (-27, 27):
        h = trimesh.creation.cylinder(2.0, 6.0, sections=64)
        h.apply_transform(trimesh.transformations.rotation_matrix(math.pi / 2, (0, 1, 0)))
        h.apply_translation((x0, 0, 5))
        ref = ref.difference(h)
    d = [x for x in visual.hole_diffs(_box((60, 10, 10), (0, 0, 5)), ref) if x["kind"] == "missing" and x["axis"] == "X"]
    xs = sorted(round(x["at"][0]) for x in d)
    assert xs and xs[0] < -20 and xs[-1] > 20 and not any(abs(v) < 5 for v in xs), d


def test_outline_blob_is_located_on_the_extra_material():
    ref = _box((20, 10, 4))
    ours = _union(ref, _box((4, 4, 4), (12, 0, 0)))
    for name in ("iso", "top", "front"):
        _, blobs = visual.view_diff(ours, ref, visual.VIEWS[name])
        ext = [b for b in blobs if b["kind"] == "extra outline"]
        assert ext and all(abs(b["at"][0] - 12) < 2.5 for b in ext), (name, ext)


def test_fillet_compare_ignores_a_different_reference_corner():
    """Ours: a sharp 90 deg root. Reference at the same spot: a shallow 20 deg bend of large radius (another feature).
    Comparing the two radii would invent a 'missing fillet'; only a corner that turns like ours is compared."""
    ours = _l_bracket(0)
    pts = [(0, 0), (20, 0), (20, 4), (8, 4), (4, 5.4), (4, 20), (0, 20)]   # bend of ~20 deg, not a 90 deg root
    ref = trimesh.creation.extrude_polygon(Polygon(pts), 10)
    hits = [h for h in visual.fillet_diffs(ours, ref, grid=1.0) if abs(h[0][0] - 4) < 1 and abs(h[0][1] - 4) < 1]
    assert hits == [], hits


# ------------------------------------------------------------------ path (capsule) deviation waivers
def _groove_blob():
    xs = np.linspace(0, 20, 41)
    pts = np.array([(x_, 1.0 * math.cos(t), 1.0 * math.sin(t)) for x_ in xs for t in np.linspace(0, 2 * math.pi, 8)])
    return {"centroid": pts.mean(0).tolist(), "bbox": [pts.min(0).tolist(), pts.max(0).tolist()], "pts": pts.tolist(), "volume_mm3": 63.0}


_PATH = {"path": [[0, 0, 0], [20, 0, 0]], "r": 1.5, "max_mm3": 100,
         "reason": "lead-retention groove (design intent: leads clipped away from the rotor, STEP has no leads)"}


def test_path_waiver_covers_a_long_groove():
    from robot.checks import reference_cad as rc

    b = _groove_blob()
    assert rc._covered(b["centroid"], {"deviations": [dict(_PATH)]}, b["bbox"], b["pts"], b["volume_mm3"])
    # one r<=5 sphere cannot hold a 20 mm groove
    assert rc._covered(b["centroid"], {"deviations": [{"near": [10, 0, 0], "r": 5, "reason": "STEP x"}]}, b["bbox"], b["pts"], 63) is None


def test_path_waiver_rejects_blob_off_path_or_over_volume():
    from robot.checks import reference_cad as rc

    b = _groove_blob()
    off = dict(_PATH, path=[[0, 3, 0], [20, 3, 0]])
    assert rc._covered(b["centroid"], {"deviations": [off]}, b["bbox"], b["pts"], 63) is None
    small = dict(_PATH, max_mm3=50)
    assert rc._covered(b["centroid"], {"deviations": [small]}, b["bbox"], b["pts"], 63) is None


def test_path_waiver_needs_cap_radius_and_cited_reason():
    from robot.checks import reference_cad as rc

    assert rc._dev_valid(dict(_PATH)) is None
    assert rc._dev_valid(dict(_PATH, r=4.0))
    assert rc._dev_valid(dict(_PATH, max_mm3=None))
    assert rc._dev_valid(dict(_PATH, max_mm3=5000))
    assert rc._dev_valid(dict(_PATH, reason="groove for the leads"))
    assert rc._dev_valid(dict(_PATH, path=[[0, 0, 0]]))
