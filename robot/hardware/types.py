"""Typed records for standard hardware. All lengths mm, masses g. Every record cites its source.

`uncertain=True` (or a key listed in `uncertain_fields`) marks a value not read directly from the standard
(vendor typical, interpolated, or derived). Checks may treat those as soft.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class Source:
    standard: str  # e.g. "ISO 4762:2004", "Ruthex RX-M3x5.7 datasheet"
    note: str = ""
    uncertain_fields: tuple[str, ...] = ()


@dataclass(frozen=True)
class Thread:
    d: float  # nominal major diameter
    pitch: float  # coarse pitch, ISO 261/262
    d_minor_ext: float  # external minor d3 (ISO 724)
    d_pitch: float  # d2
    tap_drill: float  # ISO 2306 / common practice
    stress_area: float  # As mm^2, ISO 898-1
    src: Source = Source("ISO 261/262/724, ISO 898-1")


@dataclass(frozen=True)
class ScrewHead:
    """One screw family at one diameter (lengths are a separate list)."""
    family: str  # cap | button | csk | pan | cheese | grub | thread_forming_pan ...
    standard: str  # "ISO 4762"
    d: float
    dk: float  # head diameter, max (csk: theoretical max)
    k: float  # head height, max (csk: overall head height)
    drive: str  # hex | torx | phillips | slot | none
    s: float | None = None  # hex key / AF, or torx size as float e.g. 10 for T10
    t: float | None = None  # min socket/recess depth
    csk_angle: float | None = None  # 90 for ISO 10642 / DIN 7991
    lengths: tuple[float, ...] = ()  # standard preferred lengths
    b_thread: float | None = None  # thread length ref (long screws)
    mass_per_1000: dict[float, float] = field(default_factory=dict)  # length -> kg/1000 pcs (= g per pc)
    src: Source = Source("")


@dataclass(frozen=True)
class Nut:
    family: str  # hex | thin | nyloc | square
    standard: str
    d: float
    s: float  # across flats
    m: float  # height
    e: float | None = None  # across corners, min
    mass: float | None = None  # g per pc
    src: Source = Source("")


@dataclass(frozen=True)
class Washer:
    family: str  # plain | plain_small | large | spring
    standard: str
    d: float
    d1: float  # inner
    d2: float  # outer
    h: float
    mass: float | None = None
    src: Source = Source("")


@dataclass(frozen=True)
class Insert:
    """Heat-set threaded insert for thermoplastics."""
    maker: str  # "Ruthex", "CNC Kitchen", "generic"
    part_no: str
    d: float  # thread
    length: float
    od: float  # knurl OD
    bore: float  # recommended hole diameter
    bore_depth_min: float  # min hole depth (blind)
    wall_min: float | None = None  # min wall around
    mass: float | None = None
    src: Source = Source("")


@dataclass(frozen=True)
class Standoff:
    family: str  # ff | mf | mm (female/male)
    d: float
    af: float  # hex across flats
    length: float  # body length
    male_len: float | None = None
    material: str = "brass"
    src: Source = Source("")


@dataclass(frozen=True)
class Pin:
    family: str  # dowel_m6 | dowel_h8 | spring | grooved
    standard: str  # "ISO 2338"
    d: float
    lengths: tuple[float, ...]
    chamfer: float | None = None
    src: Source = Source("")


@dataclass(frozen=True)
class Circlip:
    family: str  # ext_din471 | int_din472 | e_clip_din6799
    standard: str
    shaft_d: float  # nominal shaft (ext/e) or bore (int)
    groove_d: float
    groove_w: float  # m (H13)
    thickness: float
    free_d: float | None = None
    src: Source = Source("")


@dataclass(frozen=True)
class Bearing:
    designation: str  # "MR63", "683ZZ", "MR85"
    d: float  # bore
    D: float  # OD
    B: float  # width
    flange_D: float | None = None
    flange_B: float | None = None
    C_dyn_N: float | None = None
    C0_N: float | None = None
    max_rpm: float | None = None
    mass: float | None = None
    src: Source = Source("")


@dataclass(frozen=True)
class ORing:
    designation: str  # "ISO 3601 A0110" or "1.5x6"
    id: float
    cs: float
    groove_w: float | None = None  # static radial groove width
    groove_depth: float | None = None
    src: Source = Source("")


@dataclass(frozen=True)
class Shaft:
    d: float
    form: str  # round | d_shaft | hex
    tolerance: str  # h6, g6 ...
    flat_depth: float | None = None
    src: Source = Source("")
