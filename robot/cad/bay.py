"""Bays derived from the bought part: the pocket a catalogue part sits in is computed from the part, not drawn by hand.

WHY: hand-drawn pockets break on a part swap in three ways: the part is trapped (`assembly.blocked`), the pocket no
longer fits (`interference.overlap` / `fit.loose`) or the construction crashes. A `Bay` removes all three by
construction:

  cut        the part's rigid body + fit clearance, SWEPT along the removal direction to the open face, plus one
             slot per shaft / lead that is swept to the open face as well. Nothing closes over the part, so it can
             always leave the way it came in.
  exits      where shafts and leads leave the bay (from `entry.shaft` and `entry.ports`).
  retention  what holds the part, as data: screw sites from `props["mount_holes_mm"]`, otherwise a strap / lip
             across the open face. Retainers are NOT host material: the builder adds them as removable parts.
  keep-in    `required_envelope()`: the box the host must provide (cavity + walls), so a chassis sizes itself
             from its contents. `pack_row` / `pack_grid` add several bays up to one interior size.
  unfit      a part that cannot fit the host limits raises `BayUnfit` (a declared verdict, never a crash).

Frames: everything is in the part's catalogue frame (see robot/catalog.py: motors and wheels have the shaft on +X,
packs lie long side on X, boards lie in XY). Faces and directions are named "+x" .. "-z" in that frame. `insert_dir`
is the direction the part TRAVELS when it goes in, so the open face is the opposite one. `placement` (a build123d
`Location`) only moves the finished cut solid into the host frame.

What is "the part's rigid body": the bounding box of the catalogue solid, less (a) a shaft that sticks out of it
(it gets its own slot, sized from the real solid beyond the shaft root) and (b) for kinds in FLEXIBLE_LEAD_KINDS
the pigtail drawn beyond the origin-centred pack (it is flexible: it gets a lead slot at its port instead).

Migrating Revron's tub (robots/revron/src/revron/tub2_bays.py, tub2_pockets.py): `tub2_bays` already cuts each
compartment from the placed catalogue solid, then patches the way out by hand (`pack_drop`, `switch_drop`: the
footprint extruded down to the base opening). Each `hw.placed(part, at, rot)` cutter plus its `*_drop` becomes one
`derive_bay(catalog.find(part), placement=Pos(*at) * Rot(*rot), insert_dir="+z", reach=<seat to tub floor>)`
(the parts leave through the base, i.e. they went in travelling +Z); `_cut()` still subtracts the insert-column
KEEP sleeves from `bay.cut_solid()`. `partition()` and the bay X positions come from `pack_row([battery, rx, wesc])`
instead of ELEC / RX_X / WE_X, and CH_IN_X can be checked against `required_envelope()` so a pack that is too big is
reported as `BayUnfit`. `tub2_pockets` (deck lightening) is not a part bay and stays as it is; its pockets only
need to stay clear of each bay's `required_envelope()`.
"""

from __future__ import annotations

import json
from dataclasses import dataclass, replace
from functools import lru_cache

from robot.cad import fastener_catalog as fc

AXIS_NAMES = "xyz"
N_AXES = len(AXIS_NAMES)

# ----------------------------------------------------------------------------------------------- named defaults (mm)
PRINTED_FIT_CLEARANCE = 0.3     # per side; middle of the printed `fit.*` band (0.1-0.5 mm, GUIDE "Snug fit")
POUCH_CLEARANCE = 0.5           # per side; a LiPo pouch swells, top of the printed fit band
RUNNING_CLEARANCE = 1.0         # wheel to anything that does not turn with it (checks/interference.WHEEL_CLEARANCE_MM)
CLEARANCE_BY_KIND = {"battery": POUCH_CLEARANCE, "wheel": RUNNING_CLEARANCE}
DEFAULT_WALL = 1.6              # four 0.4 mm perimeters
LEAD_SLOT_WIDTH = 5.0           # passes a 2-wire lead (two d1.6 wires on a 3 mm pitch = 4.6); the plug drops in through the open face
LIP_OVERHANG = 1.0              # how far a retaining lip reaches over the part
CUT_OVERSHOOT = 0.05            # the cut passes the host faces it opens by this much so booleans open cleanly (cots_alts.EPS)
TOL = 1e-6                      # numeric slack when comparing coordinates

BAY_KINDS = ("battery", "esc", "receiver", "switch", "motor", "wheel", "connector")
FLEXIBLE_LEAD_KINDS = ("battery",)   # the solid includes a pigtail beyond the origin-centred body
RETENTION_BY_KIND = {"battery": "strap", "motor": "strap", "wheel": "axle"}   # kinds without mount holes; default "lip"
DEFAULT_RETENTION = "lip"


# ------------------------------------------------------------------------------------------------------- errors
class BayError(ValueError):
    """A bay could not be derived."""


class UnsupportedPart(BayError):
    """The catalogue kind is not one a bay is derived for (see BAY_KINDS)."""


class BayUnfit(BayError):
    """The part (or the packed set) does not fit the host limits. `problems` lists (direction or axis, need, limit)."""

    def __init__(self, subject, problems):
        self.subject, self.problems = subject, tuple(problems)
        rows = "; ".join(f"{where}: needs {need:.2f} mm, host allows {limit:.2f} mm" for where, need, limit in self.problems)
        super().__init__(f"{subject} does not fit the host: {rows}")


# ------------------------------------------------------------------------------------------------------ geometry
@dataclass(frozen=True)
class Face:
    """One of the six faces / directions of an axis-aligned box: axis 0..2, sign +1 / -1."""
    axis: int
    sign: int

    @classmethod
    def parse(cls, name):
        if isinstance(name, Face):
            return name
        text = str(name).strip().lower()
        if len(text) != 2 or text[0] not in "+-" or text[1] not in AXIS_NAMES:
            raise BayError(f"face / direction must be one of {[f.name for f in ALL_FACES]}, got {name!r}")
        return cls(AXIS_NAMES.index(text[1]), 1 if text[0] == "+" else -1)

    @property
    def name(self):
        return ("+" if self.sign > 0 else "-") + AXIS_NAMES[self.axis]

    @property
    def opposite(self):
        return Face(self.axis, -self.sign)

    @property
    def normal(self):
        return tuple(float(self.sign) if i == self.axis else 0.0 for i in range(N_AXES))


ALL_FACES = tuple(Face(a, s) for a in range(N_AXES) for s in (1, -1))


@dataclass(frozen=True)
class Box3:
    """Axis-aligned box, corners `lo` / `hi`."""
    lo: tuple
    hi: tuple

    @property
    def size(self):
        return tuple(h - l for l, h in zip(self.lo, self.hi))

    @property
    def center(self):
        return tuple((l + h) / 2 for l, h in zip(self.lo, self.hi))

    @property
    def volume(self):
        sx, sy, sz = self.size
        return sx * sy * sz

    def coord(self, face):
        """Coordinate of the plane of `face`."""
        return (self.hi if face.sign > 0 else self.lo)[face.axis]

    def with_coord(self, face, value):
        lo, hi = list(self.lo), list(self.hi)
        (hi if face.sign > 0 else lo)[face.axis] = value
        return Box3(tuple(lo), tuple(hi))

    def extended(self, face, distance):
        """Moved out by `distance` on one face."""
        return self.with_coord(face, self.coord(face) + face.sign * distance)

    def grown(self, margin, skip=()):
        """Moved out by `margin` on every face not in `skip`."""
        out = self
        for face in ALL_FACES:
            if face not in skip:
                out = out.extended(face, margin)
        return out

    def moved(self, offset):
        return Box3(tuple(l + o for l, o in zip(self.lo, offset)), tuple(h + o for h, o in zip(self.hi, offset)))

    def contains(self, other, tol=TOL):
        return all(sl - tol <= ol and oh <= sh + tol for sl, sh, ol, oh in zip(self.lo, self.hi, other.lo, other.hi))

    def solid(self):
        """build123d box."""
        import build123d as bd  # noqa: PLC0415 - heavy import, only when geometry is really built

        return bd.Pos(*self.center) * bd.Box(*self.size)


def _box_of(solid):
    bb = solid.bounding_box()
    return Box3(tuple(bb.min), tuple(bb.max))


def _fit_interval(centre, half, lo, hi):
    """[centre - half, centre + half] shifted into [lo, hi] (the whole range when it is wider than the range)."""
    if 2 * half >= hi - lo:
        return lo, hi
    start = min(max(centre - half, lo), hi - 2 * half)
    return start, start + 2 * half


# ------------------------------------------------------------------------------------------------ part envelope
@dataclass(frozen=True)
class Protrusion:
    """A rigid feature that sticks out of the body box (a shaft with its bushing): its own box and the face it leaves."""
    name: str
    box: Box3
    face: Face


@dataclass(frozen=True)
class PartEnvelope:
    """What a bay is sized from. `full` = bounding box of the catalogue solid, `body` = the rigid block that is seated."""
    full: Box3
    body: Box3
    protrusions: tuple = ()


def _centred_body(full):
    """Origin-centred part of a box: per axis the smaller of the two half extents (pack bodies are centred, catalog.py)."""
    half = tuple(min(-l, h) for l, h in zip(full.lo, full.hi))
    return Box3(tuple(-h for h in half), half)


def _shaft_face(shaft):
    """Face the shaft points out of, or None when it is not along an axis."""
    for face in ALL_FACES:
        if all(abs(d - n) < TOL for d, n in zip(shaft["dir"], face.normal)):
            return face
    return None


def _shaft_protrusion(solid, body, shaft):
    """(body trimmed at the shaft root, Protrusion) when a shaft sticks out of the body, else (body, None). The root
    must leave the origin inside the body (a wheel's axle starts at its far face: that is not a protrusion)."""
    face = _shaft_face(shaft) if shaft else None
    if face is None:
        return body, None
    root = shaft["at"][face.axis]
    if face.sign * root <= 0 or face.sign * (body.coord(face) - root) <= TOL:
        return body, None
    beyond = body.with_coord(face.opposite, root).grown(CUT_OVERSHOOT, skip=(face.opposite,))
    return body.with_coord(face, root), Protrusion("shaft", _box_of(solid & beyond.solid()), face)


@lru_cache(maxsize=None)
def _envelope(kind, shape_json, shaft_json):
    from robot import shapes  # noqa: PLC0415 - builds the solid

    solid = shapes.to_solid(json.loads(shape_json))
    full = _box_of(solid)
    body = _centred_body(full) if kind in FLEXIBLE_LEAD_KINDS else full
    body, shaft = _shaft_protrusion(solid, body, json.loads(shaft_json))
    return PartEnvelope(full, body, (shaft,) if shaft else ())


def part_envelope(entry) -> PartEnvelope:
    """Envelope of a `catalog.CatalogEntry` (cached on its shape)."""
    return _envelope(entry.kind, json.dumps(entry.shape, sort_keys=True), json.dumps(entry.shaft))


# ------------------------------------------------------------------------------------------------- exits (slots)
@dataclass(frozen=True)
class Exit:
    """Where a shaft or lead leaves the bay. `box` is the slot through the wall on `face`, swept to the open face
    (None when the feature leaves through the open face itself: no cut needed). `rigid`: a shaft, not a wire."""
    name: str
    face: Face
    point: tuple
    box: Box3 | None
    rigid: bool = False


def _exit_face(point, box):
    """Face of `box` the point is furthest outside of (or nearest to, from inside)."""
    return max(ALL_FACES, key=lambda f: f.sign * (point[f.axis] - box.coord(f)))


def _slot(body, cavity, keep_in, open_face, face, spans):
    """Slot through the wall on `face`: from the body face to the host's outer face along the face axis; on the
    other axes `spans[axis]` = (lo, hi), kept inside the cavity and, along the removal axis, run to the open face."""
    if face == open_face:
        return None
    lo, hi = [0.0] * N_AXES, [0.0] * N_AXES
    for axis in range(N_AXES):
        if axis == face.axis:
            lo[axis], hi[axis] = sorted((body.coord(face), keep_in.coord(face)))
            continue
        half = (spans[axis][1] - spans[axis][0]) / 2
        lo[axis], hi[axis] = _fit_interval(sum(spans[axis]) / 2, half, cavity.lo[axis], cavity.hi[axis])
    slot = Box3(tuple(lo), tuple(hi))
    return slot if face.axis == open_face.axis else slot.with_coord(open_face, cavity.coord(open_face))


def _lead_exits(entry, body, cavity, keep_in, open_face, slot_width):
    out = []
    for name, point in sorted(entry.ports.items()):
        face = _exit_face(point, body)
        spans = [(p - slot_width / 2, p + slot_width / 2) for p in point]
        out.append(Exit(name, face, tuple(point), _slot(body, cavity, keep_in, open_face, face, spans)))
    return out


def _protrusion_exits(envelope, clearance, cavity, keep_in, open_face):
    out = []
    for p in envelope.protrusions:
        grown = p.box.grown(clearance)
        spans = list(zip(grown.lo, grown.hi))
        out.append(Exit(p.name, p.face, p.box.center, _slot(envelope.body, cavity, keep_in, open_face, p.face, spans), rigid=True))
    return out


# ---------------------------------------------------------------------------------------------------- retention
@dataclass(frozen=True)
class RetentionSite:
    """One retainer: `kind` screw / strap / lip, `at` in the part frame, `face` it acts on / is driven from."""
    kind: str
    at: tuple
    face: Face
    thread: str | None = None
    clearance_d: float | None = None
    overhang: float | None = None


@dataclass(frozen=True)
class Retention:
    """What holds the part. `holding_faces`: located by host walls / floor. `retained_face`: the open face, closed
    only by `sites` (removable: screws, a strap, a snap lip or the cover), never by host material."""
    method: str
    holding_faces: tuple
    retained_face: Face
    sites: tuple


def _thread_d(thread):
    return float(str(thread).lstrip("Mm"))


def _screw_sites(entry, envelope):
    thread = entry.props.get("mount_thread")
    hole_d = fc.clearance(_thread_d(thread)) if thread else None
    return tuple(RetentionSite("screw", tuple(p), _exit_face(p, envelope.body), thread, hole_d)
                 for p in entry.props.get("mount_holes_mm") or [])


def _transverse_axes(open_face, body):
    """The two axes across the open face, longer body side first."""
    axes = [a for a in range(N_AXES) if a != open_face.axis]
    return sorted(axes, key=lambda a: -body.size[a])


def _flank_sites(kind, body, open_face, offset, overhang=None):
    """Two sites on the open face plane, either side of the body across its shorter side, at mid length."""
    _, across = _transverse_axes(open_face, body)
    sites = []
    for side in (Face(across, 1), Face(across, -1)):
        at = list(body.center)
        at[open_face.axis] = body.coord(open_face)
        at[across] = body.coord(side) + side.sign * offset
        sites.append(RetentionSite(kind, tuple(at), side, overhang=overhang))
    return tuple(sites)


def _retention(entry, envelope, open_face, clearance, wall, lip_overhang):
    holding = tuple(f for f in ALL_FACES if f != open_face)
    sites = _screw_sites(entry, envelope)
    if sites:
        return Retention("screw", holding, open_face, sites)
    method = RETENTION_BY_KIND.get(entry.kind, DEFAULT_RETENTION)
    if method == "strap":      # strap slots sit in the middle of the two flanking walls
        sites = _flank_sites("strap", envelope.body, open_face, clearance + wall / 2)
    elif method == "lip":      # lips root on the flanking walls and reach in over the part
        sites = _flank_sites("lip", envelope.body, open_face, clearance, overhang=lip_overhang)
    return Retention(method, holding, open_face, sites)


# ---------------------------------------------------------------------------------------------------------- bay
@dataclass(frozen=True)
class Bay:
    """A derived bay, in the part's catalogue frame (`placement` moves the cut into the host)."""
    part_id: str
    kind: str
    envelope: PartEnvelope
    clearance: float
    wall: float
    insert_dir: Face
    cavity: Box3            # body + clearance, swept to the open face
    keep_in: Box3           # cavity + wall on every face but the open one
    exits: tuple
    retention: Retention
    placement: object = None

    @property
    def open_face(self):
        return self.insert_dir.opposite

    def cut_boxes(self):
        """The boxes whose union is the cut: the cavity and every exit slot, each passing the faces it opens."""
        through = lambda box, face: box.extended(face, CUT_OVERSHOOT)
        boxes = [through(self.cavity, self.open_face)]
        boxes += [through(through(e.box, e.face), self.open_face) for e in self.exits if e.box is not None]
        return boxes

    def cut_solid(self, placed=True):
        """build123d solid to subtract from the host (in the host frame when `placed` and a placement is set)."""
        boxes = self.cut_boxes()
        solid = boxes[0].solid()
        for box in boxes[1:]:
            solid = solid + box.solid()
        return solid.moved(self.placement) if placed and self.placement is not None else solid

    def required_envelope(self) -> Box3:
        """Keep-in box the host must provide round this bay (part frame)."""
        return self.keep_in

    def required_size(self):
        return self.keep_in.size

    def host_block(self):
        """The smallest host that holds this bay: the keep-in box less the cut (part frame). For checks and previews."""
        return self.keep_in.solid() - self.cut_solid(placed=False)


def _check_supported(entry):
    if entry.kind not in BAY_KINDS:
        raise UnsupportedPart(f"no bay is derived for kind {entry.kind!r} (`{entry.id}`); supported kinds: {', '.join(BAY_KINDS)}")


def _check_params(clearance, wall, reach):
    for name, value in (("clearance", clearance), ("reach", reach)):
        if value < 0:
            raise BayError(f"{name} must be >= 0, got {value}")
    if wall <= 0:
        raise BayError(f"wall must be > 0, got {wall}")


def _limit_problems(where, size, host_max_size):
    """(where, need, limit) rows for every axis whose size passes the host limit (None = unlimited)."""
    if host_max_size is None:
        return []
    return [(f"{where} {AXIS_NAMES[a]}", size[a], host_max_size[a]) for a in range(N_AXES)
            if host_max_size[a] is not None and size[a] > host_max_size[a] + TOL]


def _keep_in_for(body, clearance, wall, reach, open_face):
    cavity = body.grown(clearance).extended(open_face, reach)
    return cavity, cavity.grown(wall, skip=(open_face,))


def _pick_direction(subject, body, clearance, wall, reach, directions, host_max_size):
    """The allowed insertion direction whose bay fits the host limits and needs the least host volume (so the
    part goes in through its broadest face when that is allowed). BayUnfit when none fits."""
    fits, problems = [], []
    for direction in directions:
        _, keep_in = _keep_in_for(body, clearance, wall, reach, direction.opposite)
        rows = _limit_problems(f"insert {direction.name}:", keep_in.size, host_max_size)
        problems += rows
        if not rows:
            fits.append((keep_in.volume, direction))
    if not fits:
        raise BayUnfit(subject, problems)
    return min(fits, key=lambda vd: vd[0])[1]


def derive_bay(entry, *, placement=None, clearance=None, wall=DEFAULT_WALL, insert_dir=None, allowed_dirs=None,
               reach=0.0, host_max_size=None, lead_slot_width=LEAD_SLOT_WIDTH, lip_overhang=LIP_OVERHANG) -> Bay:
    """Bay for one catalogue entry.

    entry           `catalog.CatalogEntry` (kind in BAY_KINDS).
    placement       build123d Location of the part frame in the host; only applied to `cut_solid()`.
    clearance       fit clearance per side; default by kind (CLEARANCE_BY_KIND, else PRINTED_FIT_CLEARANCE).
    wall            host wall / floor thickness round the cavity.
    insert_dir      direction the part travels going in ("+x" .. "-z"); the open face is the opposite one.
    allowed_dirs    used when insert_dir is None: the directions to choose from (default: all six).
    reach           extra depth from the part's open-side face to the host's open face (a deep pocket).
    host_max_size   (x, y, z) limits on the keep-in box in the part frame, None per axis = unlimited.
    Raises UnsupportedPart, BayUnfit or BayError; never a geometry crash for a catalogue part.
    """
    _check_supported(entry)
    clearance = CLEARANCE_BY_KIND.get(entry.kind, PRINTED_FIT_CLEARANCE) if clearance is None else clearance
    _check_params(clearance, wall, reach)
    envelope = part_envelope(entry)
    directions = [Face.parse(insert_dir)] if insert_dir is not None else [Face.parse(d) for d in (allowed_dirs or ALL_FACES)]
    direction = _pick_direction(f"`{entry.id}`", envelope.body, clearance, wall, reach, directions, host_max_size)
    open_face = direction.opposite
    cavity, keep_in = _keep_in_for(envelope.body, clearance, wall, reach, open_face)
    exits = _protrusion_exits(envelope, clearance, cavity, keep_in, open_face)
    exits += _lead_exits(entry, envelope.body, cavity, keep_in, open_face, lead_slot_width)
    retention = _retention(entry, envelope, open_face, clearance, wall, lip_overhang)
    return Bay(entry.id, entry.kind, envelope, clearance, wall, direction, cavity, keep_in, tuple(exits), retention, placement)


# ------------------------------------------------------------------------------------------------------ packing
@dataclass(frozen=True)
class Packing:
    """Several bays laid out in one interior. `size`: required interior (x, y, z). `origins[i]`: where bay i's part
    frame origin sits, measured from the interior's minimum corner. `boxes[i]`: its keep-in box in that frame."""
    size: tuple
    origins: tuple
    boxes: tuple

    def placed(self, bays):
        """The bays with `placement` set to their packed position (interior minimum corner = host origin)."""
        import build123d as bd  # noqa: PLC0415

        return [replace(bay, placement=bd.Pos(*origin)) for bay, origin in zip(bays, self.origins)]


def _shared_wall(before, after, axis):
    """Wall two neighbours along `axis` can share: the thinner of the two, when both adjoining faces are walls."""
    if before.open_face == Face(axis, 1) or after.open_face == Face(axis, -1):
        return 0.0
    return min(before.wall, after.wall)


def _row_starts(bays, axis, gap, share_walls):
    """Start coordinate of each bay's keep-in box along `axis`, and the total length."""
    starts, cursor = [], 0.0
    for i, bay in enumerate(bays):
        if i:
            cursor += gap - (_shared_wall(bays[i - 1], bay, axis) if share_walls else 0.0)
        starts.append(cursor)
        cursor += bay.keep_in.size[axis]
    return starts, cursor


def _packing(bays, corners, host_max_size):
    """Packing from each bay's keep-in minimum corner; BayUnfit when the total passes the host limits."""
    origins = tuple(tuple(c - l for c, l in zip(corner, bay.keep_in.lo)) for bay, corner in zip(bays, corners))
    boxes = tuple(bay.keep_in.moved(origin) for bay, origin in zip(bays, origins))
    size = tuple(max(box.hi[a] for box in boxes) for a in range(N_AXES))
    problems = _limit_problems("packed interior", size, host_max_size)
    if problems:
        raise BayUnfit("bays " + ", ".join(f"`{b.part_id}`" for b in bays), problems)
    return Packing(size, origins, boxes)


def pack_row(bays, axis="x", gap=0.0, share_walls=False, host_max_size=None) -> Packing:
    """Bays side by side along `axis`, all seated on the interior's minimum faces on the other two axes.
    `gap`: extra spacing between neighbours. `share_walls`: neighbours overlap by their thinner wall (one partition
    instead of two). Raises BayUnfit when the row passes `host_max_size`."""
    bays = list(bays)
    if not bays:
        raise BayError("pack_row needs at least one bay")
    along = AXIS_NAMES.index(str(axis).lower())
    starts, _ = _row_starts(bays, along, gap, share_walls)
    corners = [tuple(s if a == along else 0.0 for a in range(N_AXES)) for s in starts]
    return _packing(bays, corners, host_max_size)


def pack_grid(bays, columns, gap=0.0, host_max_size=None) -> Packing:
    """Bays in rows of `columns` along X, rows stacked along Y; each column is as wide as its widest bay and each
    row as deep as its deepest. Raises BayUnfit when the grid passes `host_max_size`."""
    bays = list(bays)
    if not bays or columns < 1:
        raise BayError("pack_grid needs at least one bay and one column")
    x_axis, y_axis = AXIS_NAMES.index("x"), AXIS_NAMES.index("y")
    rows = [bays[i:i + columns] for i in range(0, len(bays), columns)]
    widths = [max(row[c].keep_in.size[x_axis] for row in rows if c < len(row)) for c in range(columns)]
    depths = [max(bay.keep_in.size[y_axis] for bay in row) for row in rows]
    corners = [(sum(widths[:c]) + c * gap, sum(depths[:r]) + r * gap, 0.0) for r, row in enumerate(rows) for c in range(len(row))]
    return _packing(bays, corners, host_max_size)
