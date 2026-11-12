"""Small metric O-rings. Static radial groove dims (gland depth = radial, groove width, no backup ring)
from Parker O-Ring Handbook ORD 5700 metric static radial table; CS 1.0/1.5/2.0 rows interpolated."""

from ..types import ORing, Source

# cs -> (groove_w, groove_depth)
GROOVE_STATIC_RADIAL: dict[float, tuple[float, float]] = {
    1.0: (1.4, 0.75),
    1.5: (2.0, 1.15),
    1.78: (2.4, 1.35),
    2.0: (2.7, 1.5),
    2.4: (3.2, 1.85),
}
_INTERP = {1.0, 1.5, 2.0}

# ISO 3601-1 class A uses CS 1.78/2.62/3.53...; 1.0/1.5/2.0/2.4 are common DIN 3771-style / metric stock.
_IDS: dict[float, tuple[float, ...]] = {
    1.0: (1, 1.5, 2, 2.5, 3, 4, 5, 6, 7, 8, 10, 12),
    1.5: (2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 18, 20),
    1.78: (1.78, 2.57, 2.9, 3.68, 4.47, 5.28, 6.07, 7.65, 9.25, 10.82, 12.42, 14.0, 15.6, 17.17, 18.77,
           20.35, 21.95, 23.52, 25.12, 26.7, 28.3),
    2.0: (3, 4, 5, 6, 8, 10, 12, 14, 15, 16, 18, 20, 22, 25, 28, 30),
    2.4: (5, 6, 8, 10, 12, 14, 16, 18, 20, 22, 25, 28, 30),
}


def _src(cs):
    std = "ISO 3601-1:2012 class A (AS568-equivalent series)" if cs == 1.78 else "Metric stock O-ring range (DIN 3771 / vendor)"
    unc = ("groove_w", "groove_depth") if cs in _INTERP else ()
    if cs != 1.78:
        unc = unc + ("id",)
    return Source(std + "; groove: Parker ORD 5700 static radial", uncertain_fields=unc)


ORINGS: list[ORing] = [
    ORing(f"{i:g}x{cs:g}", float(i), cs, *GROOVE_STATIC_RADIAL[cs], src=_src(cs))
    for cs, ids in _IDS.items() for i in ids
]
