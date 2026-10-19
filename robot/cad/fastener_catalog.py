"""Metric fastener dimensions from the standards, in one table, so holes are never sized by eye.

Every number a hole needs comes from here: clearance (ISO 273), tap drill (ISO 2306 / common practice), countersunk
head (ISO 10642, M2/M2.5 from ISO 14581 since 10642 starts at M3), button head (ISO 7380-1, M2/M2.5 vendor values),
socket cap (ISO 4762), hex nut (ISO 4032), thin nut (ISO 4035) and heat-set inserts (common "short" brass inserts for
FDM, e.g. Ruthex RX-M3x5.7: bore = recommended hole diameter, not the knurl OD).

Head dimensions are the nominal (maximum) values: a hole cut to them always clears a real head.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

# d: (clear_close, clear_normal, clear_loose)  ISO 273 fine / medium / coarse
CLEARANCE = {
    1.6: (1.7, 1.8, 2.0), 2.0: (2.2, 2.4, 2.6), 2.5: (2.7, 2.9, 3.1), 3.0: (3.2, 3.4, 3.6),
    4.0: (4.3, 4.5, 4.8), 5.0: (5.3, 5.5, 5.8), 6.0: (6.4, 6.6, 7.0),
}
TAP_DRILL = {1.6: 1.25, 2.0: 1.6, 2.5: 2.05, 3.0: 2.5, 4.0: 3.3, 5.0: 4.2, 6.0: 5.0}
# countersunk 90 deg: (dk theoretical max, k)
CSK = {1.6: (3.0, 0.96), 2.0: (3.8, 1.2), 2.5: (4.7, 1.5), 3.0: (6.0, 1.86), 4.0: (8.96, 2.48), 5.0: (11.2, 3.1),
       6.0: (13.44, 3.72)}
CSK_STD = {d: ("ISO 14581" if d < 3 else "DIN 7991" if d == 3 else "ISO 10642") for d in CSK}   # M3: DIN 7991 (dk 6.0), the head the Revron STEP drills 6.2 for
# button head (dk, k)
BUTTON = {2.0: (3.5, 1.3), 2.5: (4.7, 1.5), 3.0: (5.7, 1.65), 4.0: (7.6, 2.2), 5.0: (9.5, 2.75), 6.0: (10.5, 3.3)}
# socket head cap (dk, k)
CAP = {1.6: (3.0, 1.6), 2.0: (3.8, 2.0), 2.5: (4.5, 2.5), 3.0: (5.5, 3.0), 4.0: (7.0, 4.0), 5.0: (8.5, 5.0),
       6.0: (10.0, 6.0)}
# nuts: across flats s, height m
HEX_NUT = {1.6: (3.2, 1.3), 2.0: (4.0, 1.6), 2.5: (5.0, 2.0), 3.0: (5.5, 2.4), 4.0: (7.0, 3.2), 5.0: (8.0, 4.7),
           6.0: (10.0, 5.2)}
THIN_NUT = {2.0: (4.0, 1.2), 2.5: (5.0, 1.6), 3.0: (5.5, 1.8), 4.0: (7.0, 2.2), 5.0: (8.0, 2.7), 6.0: (10.0, 3.2)}
# heat-set insert: (hole diameter, insert length)
INSERT = {2.0: (3.2, 4.0), 2.5: (3.6, 5.7), 3.0: (4.0, 5.7), 4.0: (5.6, 8.1), 5.0: (6.4, 9.5)}

HEADS = {"csk": (CSK, "ISO 10642"), "button": (BUTTON, "ISO 7380-1"), "cap": (CAP, "ISO 4762")}
NUTS = {"hex": (HEX_NUT, "ISO 4032"), "thin": (THIN_NUT, "ISO 4035")}
# spec `head` value (robot.world.fastener_shape) for each head style
SPEC_HEAD = {"csk": "countersunk", "button": "button", "cap": None}


@dataclass(frozen=True)
class Screw:
    d: float
    length: float

    @property
    def designation(self) -> str:
        return f"M{_n(self.d)}x{_n(self.length)}"


def _n(x: float) -> str:
    return f"{x:g}"


def parse(designation: str) -> Screw:
    """'M2x6' / 'm2.5 x 10' -> Screw(2.0, 6.0). Raises ValueError for anything else or a size not in the tables."""
    m = re.fullmatch(r"\s*[Mm]?\s*([0-9.]+)\s*[xX]\s*([0-9.]+)\s*", str(designation or ""))
    if not m:
        raise ValueError(f"fastener designation `{designation}` is not like M2x6")
    s = Screw(float(m.group(1)), float(m.group(2)))
    if s.d not in CLEARANCE:
        raise ValueError(f"M{_n(s.d)} is not in the fastener catalog (have M{', M'.join(_n(k) for k in CLEARANCE)})")
    return s


def _get(table, d, what):
    if d not in table:
        raise ValueError(f"no {what} data for M{_n(d)}")
    return table[d]


def clearance(d: float, fit: str = "normal") -> float:
    return _get(CLEARANCE, d, "clearance")[{"close": 0, "normal": 1, "loose": 2}[fit]]


def tap_drill(d: float) -> float:
    return _get(TAP_DRILL, d, "tap drill")


def head(d: float, style: str) -> tuple[float, float]:
    """(head diameter dk, head height k) for style csk | button | cap."""
    if style not in HEADS:
        raise ValueError(f"head must be one of {sorted(HEADS)}, not `{style}`")
    return _get(HEADS[style][0], d, f"{style} head")


def head_standard(d: float, style: str) -> str:
    return CSK_STD.get(d, "ISO 10642") if style == "csk" else HEADS[style][1]


def nut(d: float, style: str = "hex") -> tuple[float, float]:
    """(across flats s, height m) for style hex | thin."""
    if style not in NUTS:
        raise ValueError(f"nut must be one of {sorted(NUTS)}, not `{style}`")
    return _get(NUTS[style][0], d, f"{style} nut")


def insert(d: float) -> tuple[float, float]:
    """(hole diameter, length) of a heat-set insert."""
    return _get(INSERT, d, "heat-set insert")


# hex socket drive: key size s (across flats) and nominal socket depth t, per head style.
# cap ISO 4762, button ISO 7380-1 (M2/M2.5 vendor), countersunk ISO 10642 (M1.6-M2.5 hex variants of ISO 14581 sizes).
DRIVE_KEY = {
    "cap": {1.6: (1.5, 0.7), 2.0: (1.5, 1.0), 2.5: (2.0, 1.1), 3.0: (2.5, 1.3), 4.0: (3.0, 2.0), 5.0: (4.0, 2.5), 6.0: (5.0, 3.0)},
    "button": {2.0: (1.3, 0.7), 2.5: (1.5, 0.9), 3.0: (2.0, 1.04), 4.0: (2.5, 1.3), 5.0: (3.0, 1.56), 6.0: (4.0, 2.08)},
    "csk": {1.6: (0.9, 0.55), 2.0: (1.3, 0.7), 2.5: (1.5, 0.85), 3.0: (2.0, 1.1), 4.0: (2.5, 1.5), 5.0: (3.0, 1.9), 6.0: (4.0, 2.2)},
}
# robot.world.fastener_shape `head` value -> DRIVE_KEY style
WORLD_HEAD = {"countersunk": "csk", "button": "button", None: "cap", "cap": "cap", "socket": "cap"}


def drive_key(d: float, style: str) -> tuple[float, float]:
    """(hex key size across flats, socket depth) of the hex socket in a csk | button | cap head. Off-table diameters
    take the nearest smaller tabled size (never a key that would not fit the head)."""
    style = WORLD_HEAD.get(style, style)
    if style not in DRIVE_KEY:
        raise ValueError(f"drive style must be one of {sorted(DRIVE_KEY)}, not `{style}`")
    t = DRIVE_KEY[style]
    if d in t:
        return t[d]
    lower = [k for k in t if k <= d + 1e-9]
    return t[max(lower) if lower else min(t)]
