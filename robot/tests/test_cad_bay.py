"""robot.cad.bay: every battery, ESC / receiver, switch, drive motor (and wheel, connector) in the catalogue gets a bay
that builds, fits with the stated clearance and lets the part out along the insertion axis. Parametrised over the
catalogue, so a new or swapped part is covered without a new test."""

import math
from functools import lru_cache

import build123d as bd
import pytest

from robot import catalog, shapes
from robot.cad import bay as B

ENTRIES = [e for e in catalog.catalog() if e.kind in B.BAY_KINDS]
REQUIRED_KINDS = ("battery", "esc", "receiver", "switch", "motor")
DIRECTIONS = [f.name for f in B.ALL_FACES]
VOLUME_TOL = 1e-3            # mm3: boolean noise
SWEEP_MARGIN = 5.0           # how far past the host the part is pulled in the sweep check
LENGTH_TOL = 1e-6

by_entry = pytest.mark.parametrize("entry", ENTRIES, ids=[e.id for e in ENTRIES])
by_direction = pytest.mark.parametrize("direction", DIRECTIONS)


def overlap(a, b):
    """Common volume of two solids (0 when they do not meet)."""
    common = a & b
    return 0.0 if common is None else sum(s.volume for s in common.solids())


@lru_cache(maxsize=None)
def bay_and_host(entry_id, direction):
    """Bay of a catalogue part for one direction and its host block, built once for all tests."""
    bay = B.derive_bay(catalog.find(entry_id), insert_dir=direction)
    return bay, bay.host_block()


def rigid_boxes(bay):
    return [bay.envelope.body] + [p.box for p in bay.envelope.protrusions]


def swept(box, bay):
    """The box dragged out of the bay along the removal direction, past the host by SWEEP_MARGIN."""
    travel = bay.keep_in.size[bay.open_face.axis] + SWEEP_MARGIN
    return box.extended(bay.open_face, travel)


def test_catalogue_covers_the_required_kinds():
    kinds = {e.kind for e in ENTRIES}
    assert set(REQUIRED_KINDS) <= kinds
    assert len(ENTRIES) > len(REQUIRED_KINDS)


@by_entry
def test_bay_builds_a_valid_solid(entry):
    bay = B.derive_bay(entry)
    cut, host = bay.cut_solid(), bay.host_block()
    assert cut.is_valid and cut.volume > bay.envelope.body.volume
    assert host.is_valid and host.volume > 0
    assert bay.insert_dir.name in DIRECTIONS and bay.open_face == bay.insert_dir.opposite


@by_entry
@by_direction
def test_part_fits_with_the_stated_clearance(entry, direction):
    bay = B.derive_bay(entry, insert_dir=direction)
    body, c = bay.envelope.body, bay.clearance
    assert bay.cavity.contains(body.grown(c))
    for face in B.ALL_FACES:            # not loose either: exactly the clearance on every walled face
        if face != bay.open_face:
            assert math.isclose(abs(bay.cavity.coord(face) - body.coord(face)), c, abs_tol=LENGTH_TOL)
    assert bay.required_envelope().contains(bay.cavity)
    assert (body.grown(c).solid() - bay.cut_solid()).volume < VOLUME_TOL      # the real cut holds body + clearance


@by_entry
@by_direction
def test_part_is_never_trapped(entry, direction):
    """Swept insertion: the body and every rigid protrusion, dragged out along the removal direction, never meet host
    material (keep-in block less the cut)."""
    bay, host = bay_and_host(entry.id, direction)
    for box in rigid_boxes(bay):
        assert overlap(host, swept(box, bay).solid()) < VOLUME_TOL, (entry.id, direction)


@by_entry
def test_real_part_seats_without_touching_the_host(entry):
    """The catalogue solid itself (shaft, bushing, tabs, lead stubs) clears the host in every direction's bay."""
    solid = shapes.to_solid(entry.shape)
    for direction in DIRECTIONS:
        _, host = bay_and_host(entry.id, direction)
        assert overlap(host, solid) < VOLUME_TOL, (entry.id, direction)


@by_entry
def test_auto_direction_respects_limits_or_declares_unfit(entry):
    size = B.derive_bay(entry).required_size()
    roomy = tuple(s + 1.0 for s in size)
    assert B.derive_bay(entry, host_max_size=roomy).required_size() == size
    body = B.part_envelope(entry).body.size
    with pytest.raises(B.BayUnfit) as err:
        B.derive_bay(entry, host_max_size=tuple(s / 2 for s in body))
    assert entry.id in str(err.value) and err.value.problems


# ------------------------------------------------------------------------------------------------- derived data
def test_pack_body_excludes_the_flexible_lead():
    spec = __import__("robot.cots_alts", fromlist=["BATTERIES"]).BATTERIES["palmpower_2s_180_45c"]
    env = B.part_envelope(catalog.find("palmpower_2s_180_45c"))
    assert env.body.size == pytest.approx((spec["l"], spec["w"], spec["h"]))
    assert env.full.hi[1] > env.body.hi[1]


def test_motor_shaft_gets_a_rigid_exit_swept_to_the_open_face():
    entry = catalog.find("pololu_hpcb6v_30to1")
    bay = B.derive_bay(entry, insert_dir="-z")
    shaft = next(e for e in bay.exits if e.rigid)
    assert shaft.face.name == "+x" and bay.envelope.body.hi[0] == pytest.approx(entry.shaft["at"][0])
    assert shaft.box.hi[2] == pytest.approx(bay.cavity.hi[2])                 # runs to the open (+z) face
    assert shaft.box.hi[0] == pytest.approx(bay.keep_in.hi[0])                # through the wall
    along = B.derive_bay(entry, insert_dir="-x")                              # shaft leaves through the opening: no cut
    assert next(e for e in along.exits if e.rigid).box is None


def test_lead_exit_follows_the_port():
    entry = catalog.find("gnb_2s_450_80c")
    bay = B.derive_bay(entry, insert_dir="-z")
    lead = next(e for e in bay.exits if e.name == "xt30")
    assert lead.face.name == "+y" and not lead.rigid
    assert lead.box.size[0] == pytest.approx(B.LEAD_SLOT_WIDTH)
    assert {e.name for e in B.derive_bay(catalog.find("malenki_nano")).exits} == set(catalog.find("malenki_nano").ports)


def test_retention_from_mount_pattern():
    motor = catalog.find("pololu_hpcb6v_30to1")
    r = B.derive_bay(motor, insert_dir="-z").retention
    assert r.method == "screw" and len(r.sites) == len(motor.props["mount_holes_mm"])
    assert all(s.thread == "M1.6" and s.face.name == "+x" and s.clearance_d == pytest.approx(1.8) for s in r.sites)
    assert r.retained_face.name == "+z" and r.retained_face not in r.holding_faces and len(r.holding_faces) == 5
    pack = B.derive_bay(catalog.find("lipo_2s_180"), insert_dir="-z").retention
    assert pack.method == "strap" and [s.face.name for s in pack.sites] == ["+y", "-y"]
    board = B.derive_bay(catalog.find("malenki_nano"), insert_dir="-z").retention
    assert board.method == "lip" and all(s.overhang == B.LIP_OVERHANG for s in board.sites)


def test_unsupported_kind_and_bad_arguments_are_declared():
    with pytest.raises(B.UnsupportedPart):
        B.derive_bay(catalog.find("gr1507"))
    with pytest.raises(B.BayError):
        B.derive_bay(catalog.find("lipo_2s_180"), insert_dir="up")
    with pytest.raises(B.BayError):
        B.derive_bay(catalog.find("lipo_2s_180"), wall=0)


def test_direction_is_picked_from_the_allowed_ones():
    entry = catalog.find("lipo_2s_350")
    assert B.derive_bay(entry).open_face.axis == 2                             # broadest face by default
    assert B.derive_bay(entry, allowed_dirs=["+x", "-y"]).insert_dir.name in ("+x", "-y")
    deep = B.derive_bay(entry, insert_dir="-z").required_size()[1]             # walls on both Y sides
    picked = B.derive_bay(entry, allowed_dirs=["-z", "-y"], host_max_size=(None, deep - B.DEFAULT_WALL / 2, None))
    assert picked.insert_dir.name == "-y"


def test_reach_deepens_the_pocket_and_placement_moves_the_cut():
    entry, reach, shift = catalog.find("malenki_nano"), 4.0, (10.0, -5.0, 3.0)
    flush, deep = B.derive_bay(entry, insert_dir="-z"), B.derive_bay(entry, insert_dir="-z", reach=reach)
    assert deep.required_size()[2] == pytest.approx(flush.required_size()[2] + reach)
    placed = B.derive_bay(entry, insert_dir="-z", placement=bd.Pos(*shift))
    assert tuple(placed.cut_solid().center()) == pytest.approx(tuple(c + s for c, s in zip(flush.cut_solid().center(), shift)))


# ------------------------------------------------------------------------------------------------------ packing
def pack_parts():
    return [B.derive_bay(catalog.find(i), insert_dir="-z") for i in ("lipo_2s_350", "malenki_nano", "bbb_ant_esc")]


def test_pack_row_adds_up_and_does_not_overlap():
    bays, gap = pack_parts(), 0.5
    packing = B.pack_row(bays, axis="x", gap=gap)
    sizes = [b.required_size() for b in bays]
    assert packing.size[0] == pytest.approx(sum(s[0] for s in sizes) + gap * (len(bays) - 1))
    assert packing.size[1:] == pytest.approx((max(s[1] for s in sizes), max(s[2] for s in sizes)))
    for before, after in zip(packing.boxes, packing.boxes[1:]):
        assert after.lo[0] == pytest.approx(before.hi[0] + gap)
    shared = B.pack_row(bays, axis="x", share_walls=True)
    assert shared.size[0] == pytest.approx(sum(s[0] for s in sizes) - B.DEFAULT_WALL * (len(bays) - 1))
    cuts = [b.cut_solid() for b in packing.placed(bays)]
    assert overlap(cuts[0], cuts[1]) < VOLUME_TOL


def test_pack_grid_and_unfit():
    bays = pack_parts()
    grid = B.pack_grid(bays, columns=2)
    sizes = [b.required_size() for b in bays]
    assert grid.size[0] == pytest.approx(max(sizes[0][0], sizes[2][0]) + sizes[1][0])
    assert grid.size[1] == pytest.approx(max(sizes[0][1], sizes[1][1]) + sizes[2][1])
    row = B.pack_row(bays)
    with pytest.raises(B.BayUnfit):
        B.pack_row(bays, host_max_size=(row.size[0] - 1.0, None, None))
    assert B.pack_row(bays, host_max_size=row.size).size == row.size


@pytest.mark.parametrize("kind", REQUIRED_KINDS)
def test_swap_within_a_kind_resizes_the_interior(kind):
    """Swapping any part of a kind into a packed row never crashes: the interior grows to the new part's keep-in."""
    fixed = B.derive_bay(catalog.find("malenki_nano"), insert_dir="-z")
    for entry in (e for e in ENTRIES if e.kind == kind):
        swapped = B.derive_bay(entry, insert_dir="-z")
        packing = B.pack_row([fixed, swapped])
        assert packing.size[0] == pytest.approx(fixed.required_size()[0] + swapped.required_size()[0])
        assert all(B.Box3((0.0, 0.0, 0.0), packing.size).contains(box) for box in packing.boxes)
