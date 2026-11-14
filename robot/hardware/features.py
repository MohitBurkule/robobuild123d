"""Derived hole/feature dimensions for standard hardware. Pure functions, dataclass outputs, no CAD import.

Every output carries `src` (where the number comes from) and `uncertain` (True when it is a rule of thumb, a vendor
typical or a recalled value that has not been checked against the standard text). Checks may treat uncertain values
as soft limits.

Tables defined here (only those not already in robot/hardware/data):
  ISO_273           clearance holes, fine/medium/coarse          ISO 273:1979 (values match robot.cad.fastener_catalog)
  CBORE_DIN974      counterbore diameter for ISO 4762 heads      DIN 974-1:2008 row 1 (M1.6-M2.5 uncertain)
  CSK_ISO15065      90 deg countersink diameter                   ISO 15065:2005 (recalled; uncertain)
  KEY_SHANK         hex/torx driver shank diameter per key size  vendor typical (Wiha/Wera), uncertain
  ENGAGEMENT        min thread engagement / d by host material   rules of thumb (VDI 2230 style, EJOT), uncertain
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

from . import registry as reg

# ---------------------------------------------------------------------------------------------- tables
# d: (fine/close, medium/normal, coarse/loose)
ISO_273: dict[float, tuple[float, float, float]] = {
    1.0: (1.1, 1.2, 1.3), 1.2: (1.3, 1.4, 1.5), 1.4: (1.5, 1.6, 1.8), 1.6: (1.7, 1.8, 2.0), 2.0: (2.2, 2.4, 2.6),
    2.5: (2.7, 2.9, 3.1), 3.0: (3.2, 3.4, 3.6), 3.5: (3.7, 3.9, 4.2), 4.0: (4.3, 4.5, 4.8), 5.0: (5.3, 5.5, 5.8),
    6.0: (6.4, 6.6, 7.0), 8.0: (8.4, 9.0, 10.0), 10.0: (10.5, 11.0, 12.0), 12.0: (13.0, 13.5, 14.5),
}
FITS = {"close": 0, "fine": 0, "normal": 1, "medium": 1, "loose": 2, "coarse": 2}
ISO_273_SRC = "ISO 273:1979"

# coarse pitch fallback (ISO 261) when data/threads has no row
COARSE_PITCH = {1.0: 0.25, 1.2: 0.25, 1.4: 0.3, 1.6: 0.35, 2.0: 0.4, 2.2: 0.45, 2.5: 0.45, 3.0: 0.5, 3.5: 0.6,
                4.0: 0.7, 5.0: 0.8, 6.0: 1.0, 8.0: 1.25, 10.0: 1.5, 12.0: 1.75}

CBORE_DIN974: dict[float, float] = {1.6: 3.5, 2.0: 4.4, 2.5: 5.5, 3.0: 6.5, 4.0: 8.0, 5.0: 10.0, 6.0: 11.0, 8.0: 15.0,
                                    10.0: 18.0, 12.0: 20.0}
CBORE_UNCERTAIN = {1.6, 2.0, 2.5}

CSK_ISO15065: dict[float, float] = {1.6: 3.7, 2.0: 4.6, 2.5: 5.7, 3.0: 6.5, 3.5: 7.6, 4.0: 8.6, 5.0: 10.4, 6.0: 12.4,
                                    8.0: 16.4, 10.0: 20.4}

# key size (hex AF, or torx T-number) -> (driver shank diameter, typical blade length) -- vendor typical, uncertain
KEY_SHANK: dict[float, tuple[float, float]] = {0.7: (2.5, 40), 0.9: (2.5, 40), 1.3: (3.0, 50), 1.5: (3.0, 50),
                                               2.0: (4.0, 60), 2.5: (4.5, 75), 3.0: (5.0, 75), 4.0: (6.0, 100),
                                               5.0: (7.0, 100), 6.0: (8.0, 125)}
TORX_SHANK: dict[float, tuple[float, float]] = {5: (2.5, 40), 6: (3.0, 50), 8: (3.0, 60), 10: (3.5, 60), 15: (4.0, 75),
                                                20: (4.5, 80), 25: (5.0, 100)}

# host material -> minimum engaged thread length / d (rule of thumb)
ENGAGEMENT: dict[str, float] = {"steel": 1.0, "stainless": 1.0, "brass": 1.5, "aluminium": 1.5, "aluminum": 1.5,
                                "cast_iron": 1.5, "plastic": 2.0, "PLA": 2.0, "PETG": 2.0, "ABS": 2.0,
                                "nylon": 2.0, "PA": 2.0, "TPU": 2.5}
ENGAGEMENT_SRC = "rule of thumb: steel 1d, Al/brass 1.5d (VDI 2230 style), plastics 2d (EJOT DELTA PT)"

# FDM pilot-hole factor fallback (x d) when data/screws.PLASTIC_PILOT has no entry; nylon/TPU not in EJOT tables
PILOT_FALLBACK = {"PLA": 0.80, "PETG": 0.80, "ABS": 0.80, "ASA": 0.80, "NYLON": 0.75, "PA": 0.75, "PA6": 0.75,
                  "TPU": 0.70, "PC": 0.85}


@dataclass(frozen=True)
class Dim:
    """A single derived dimension."""
    value: float
    src: str
    uncertain: bool = False
    note: str = ""


@dataclass(frozen=True)
class Counterbore:
    d: float
    depth: float
    src: str
    uncertain: bool = False


@dataclass(frozen=True)
class Countersink:
    d: float  # top diameter at the surface (flush head)
    angle: float
    depth: float  # cone depth down to the clearance hole
    clearance_d: float
    src: str
    uncertain: bool = False


@dataclass(frozen=True)
class InsertBore:
    d: float
    depth: float
    insert_length: float
    od: float
    wall_min: float | None
    src: str
    uncertain: bool = False


@dataclass(frozen=True)
class KeepOut:
    """Coaxial cylinder that must stay empty (z from the head seat, away from the part)."""
    d: float
    length: float
    src: str
    uncertain: bool = False


@dataclass(frozen=True)
class NutTrap:
    af: float  # pocket across flats
    corners: float  # pocket across corners
    depth: float
    nut_af: float
    nut_m: float
    standard: str
    uncertain: bool = False


@dataclass(frozen=True)
class PrintComp:
    """FDM compensation. hole_offset is added to every hole diameter (printed holes come out small);
    teardrop: horizontal holes get a 45 deg teardrop top so they print without support."""
    hole_offset: float = 0.2
    pocket_offset: float = 0.15  # added to polygon pockets (nut traps) across flats
    teardrop: bool = True
    uncertain_fields: tuple[str, ...] = field(default=("hole_offset", "pocket_offset"))


DEFAULT_COMP = PrintComp()
NO_COMP = PrintComp(0.0, 0.0, False)


def _near(table: dict, d: float):
    for k in table:
        if abs(k - float(d)) < 1e-9:
            return table[k]
    return None


def _fmt(d):
    return f"M{float(d):g}"


# ---------------------------------------------------------------------------------------------- holes
def clearance(d: float, fit: str = "normal") -> Dim:
    """ISO 273 clearance hole diameter. fit: close|normal|loose (fine|medium|coarse)."""
    if fit not in FITS:
        raise ValueError(f"fit must be one of {sorted(FITS)}, not `{fit}`")
    row = _near(ISO_273, d)
    if row is None:
        raise ValueError(f"no ISO 273 clearance for {_fmt(d)} (have {', '.join(_fmt(k) for k in ISO_273)})")
    return Dim(row[FITS[fit]], ISO_273_SRC)


def tap_drill(d: float) -> Dim:
    """Tap drill for a coarse metric thread (data/threads, else d - P)."""
    try:
        t = reg.thread(d)
        return Dim(t.tap_drill, t.src.standard)
    except ValueError:
        p = _near(COARSE_PITCH, d)
        if p is None:
            raise ValueError(f"no thread data for {_fmt(d)}") from None
        return Dim(round(d - p, 3), "ISO 261 pitch; tap drill = d - P (ISO 2306 practice)")


def pilot(d: float, material: str = "PLA") -> Dim:
    """Pilot hole for a thread-forming / self-tapping screw (or a metric screw driven straight) into plastic."""
    key = material.upper()
    tab = {k.upper(): v for k, v in reg.plastic_pilot().items()}
    if key in tab:
        return Dim(round(d * tab[key], 2), "robot.hardware.data.screws.PLASTIC_PILOT (EJOT DELTA PT / FDM practice)",
                   True, f"{tab[key]:g} x d")
    if key in PILOT_FALLBACK:
        f = PILOT_FALLBACK[key]
        return Dim(round(d * f, 2), "FDM community practice (no standard)", True, f"{f:g} x d; verify with a test coupon")
    raise ValueError(f"no pilot factor for `{material}` (have {', '.join(sorted(set(tab) | set(PILOT_FALLBACK)))})")


def engagement_min(d: float, host: str = "plastic") -> Dim:
    """Minimum engaged thread length in a host material."""
    f = ENGAGEMENT.get(host, ENGAGEMENT.get(host.lower(), ENGAGEMENT.get(host.upper())))
    if f is None:
        raise ValueError(f"no engagement rule for `{host}` (have {', '.join(sorted(ENGAGEMENT))})")
    return Dim(round(f * d, 3), ENGAGEMENT_SRC, True, f"{f:g} x d")


def compensate(d: float, comp: PrintComp | None = DEFAULT_COMP) -> float:
    """Printed hole diameter to model so the hole comes out at `d`."""
    return float(d) + (comp.hole_offset if comp else 0.0)


def teardrop_needed(axis, comp: PrintComp | None = DEFAULT_COMP, build_dir=(0, 0, 1), max_angle: float = 45.0) -> bool:
    """True when a hole along `axis` is steeper than max_angle from vertical and the comp asks for teardrops."""
    if not comp or not comp.teardrop:
        return False
    ax = [float(x) for x in axis]
    n = math.sqrt(sum(x * x for x in ax)) or 1.0
    b = [float(x) for x in build_dir]
    nb = math.sqrt(sum(x * x for x in b)) or 1.0
    cos = abs(sum(a * c for a, c in zip(ax, b))) / (n * nb)
    return math.degrees(math.acos(min(1.0, cos))) > max_angle


# ---------------------------------------------------------------------------------------------- heads
def _screw(d, family, standard=None):
    c = reg.list_family("screw", family=family, d=d, standard=standard)
    if not c:
        raise ValueError(f"no {family} screw {standard or ''} at {_fmt(d)}")
    if standard is None:
        pref = reg.DEFAULT_STD.get(family)
        c = sorted(c, key=lambda r: 0 if pref and reg._std_match(pref, r.standard) else 1)
    return c[0]


def counterbore(d: float, family: str = "cap", standard: str | None = None, sink: float = 0.0,
                clear: float = 0.4) -> Counterbore:
    """Counterbore for a socket head. Cap screws use DIN 974-1; other heads dk + clear. Depth = k + sink (flush)."""
    rec = _screw(d, family, standard)
    tab = _near(CBORE_DIN974, d) if family == "cap" else None
    if tab is not None:
        return Counterbore(max(tab, rec.dk + clear), rec.k + sink, "DIN 974-1:2008 (ISO 4762 heads)",
                           d in CBORE_UNCERTAIN)
    return Counterbore(round(rec.dk + clear, 3), rec.k + sink, f"{rec.standard} dk + {clear:g}", "dk" in rec.src.uncertain_fields)


def countersink(d: float, standard: str | None = None, fit: str = "normal", clear: float = 0.3,
                angle: float | None = None) -> Countersink:
    """Countersink for a csk head: max(ISO 15065 value, head dk + clear) so a flush head always fits."""
    rec = _screw(d, "csk", standard)
    ang = angle or rec.csk_angle or 90.0
    c = clearance(d, fit).value
    tab = _near(CSK_ISO15065, d)
    top = max(rec.dk + clear, tab or 0.0)
    depth = (top - c) / 2 / math.tan(math.radians(ang / 2))
    return Countersink(round(top, 3), ang, round(depth, 4), c,
                       f"{rec.standard} dk + {clear:g}" + (" / ISO 15065" if tab else ""), True if tab else False)


def head_keepout(d: float, family: str = "cap", standard: str | None = None, clear: float = 0.5,
                 extra: float = 0.0) -> KeepOut:
    """Cylinder the head occupies (dk + clear wide, k + extra tall)."""
    rec = _screw(d, family, standard)
    return KeepOut(round(rec.dk + clear, 3), rec.k + extra, rec.standard, bool(rec.src.uncertain_fields))


def driver_access(d: float, family: str = "cap", standard: str | None = None, length: float | None = None) -> KeepOut:
    """Straight tool path above the head: driver shank dia per key size, typical blade length. Uncertain (vendor)."""
    rec = _screw(d, family, standard)
    if rec.drive == "torx":
        row = _near(TORX_SHANK, rec.s) if rec.s is not None else None
    else:
        row = _near(KEY_SHANK, rec.s) if rec.s is not None else None
    if row is None:
        row = (max(3.0, rec.dk * 0.8), 60.0)
    return KeepOut(row[0], float(length if length is not None else row[1]),
                   f"vendor typical driver for {rec.drive} {rec.s:g}" if rec.s is not None else "vendor typical", True)


def wrench_access(d: float, family: str = "hex", length: float = 30.0) -> KeepOut:
    """Socket wrench around a nut: socket OD ~ 1.45 s + 3 (thin-wall nut driver; uncertain)."""
    n = reg.get(f"M{d:g} {family} nut").record
    return KeepOut(round(1.45 * n.s + 3.0, 2), length, "vendor typical nut driver (uncertain)", True)


# ---------------------------------------------------------------------------------------------- nuts, inserts
def nut_trap(d: float, family: str = "hex", fit: str = "press", depth_extra: float = 0.0,
             comp: PrintComp | None = None) -> NutTrap:
    """Hex pocket for a nut: AF + 0.05 (press) / + 0.3 (drop-in), as robot.cad.holes; depth m (+0.2 drop-in)."""
    n = reg.get(f"M{d:g} {family} nut").record
    add = {"press": 0.05, "drop": 0.3, "slip": 0.3}[fit] + (comp.pocket_offset if comp else 0.0)
    af = n.s + add
    corners = af * 2 / math.sqrt(3.0) if family != "square" else af * math.sqrt(2.0)
    return NutTrap(round(af, 4), round(corners, 4), n.m + depth_extra + (0.0 if fit == "press" else 0.2),
                   n.s, n.m, n.standard, bool(n.src.uncertain_fields))


def insert_bore(d: float, maker: str | None = None, length: float | None = None, melt_extra: float = 0.3,
                comp: PrintComp | None = None) -> InsertBore:
    """Heat-set insert hole: maker's recommended bore, depth = max(datasheet min depth, length + melt_extra)."""
    words = f" {maker}" if maker else ""
    des = f"M{d:g}x{length:g} insert{words}" if length is not None else f"M{d:g} insert{words}"
    r = reg.get(des).record
    bore = r.bore + (comp.hole_offset if comp else 0.0)
    unc = bool(set(r.src.uncertain_fields) & {"bore", "bore_depth_min", "od"})
    return InsertBore(round(bore, 3), round(max(r.bore_depth_min, r.length + melt_extra), 3), r.length, r.od,
                      r.wall_min, r.src.standard, unc)


# ---------------------------------------------------------------------------------------------- seats
BEARING_FIT = {"press": 0.0, "transition": 0.05, "slip": 0.15}  # added to D for a printed seat (FDM practice)


def bearing_seat(designation: str, fit: str = "press", comp: PrintComp | None = None) -> Dim:
    """Bore for a bearing OD. Metal (comp=None): D + fit allowance; FDM: plus comp.hole_offset. Uncertain."""
    b = reg.get(designation).record
    if fit not in BEARING_FIT:
        raise ValueError(f"fit must be one of {sorted(BEARING_FIT)}")
    return Dim(round(b.D + BEARING_FIT[fit] + (comp.hole_offset if comp else 0.0), 3), b.src.standard, True,
               f"D {b.D:g} + {fit}")


def dowel_hole(d: float, fit: str = "press", comp: PrintComp | None = None) -> Dim:
    """Hole for a dowel pin: press = d (H7 in metal; pin is m6), slip = d + 0.1. FDM adds comp (uncertain)."""
    add = {"press": 0.0, "slip": 0.1}[fit]
    return Dim(round(d + add + (comp.hole_offset if comp else 0.0), 3), "ISO 2338 m6 pin in H7 hole", comp is not None)


def oring_groove(designation: str) -> tuple[float, float, bool]:
    """(groove width, groove depth, uncertain) from the O-ring record; else 1.4 cs / 0.75 cs (25% squeeze)."""
    r = reg.get(designation if designation.lower().startswith("o") else f"oring {designation}").record
    if r.groove_w and r.groove_depth:
        return r.groove_w, r.groove_depth, bool(r.src.uncertain_fields)
    return round(1.4 * r.cs, 3), round(0.75 * r.cs, 3), True
