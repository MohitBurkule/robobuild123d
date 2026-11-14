"""Ground shafts and ISO 286-2 limit deviations (micrometres converted to mm)."""

from ..types import Shaft, Source

# ISO 286-2 deviations in mm, (upper, lower), per size band (over, up_to]
# Bands: (0,3], (3,6], (6,10]
ISO286: dict[str, dict[tuple[float, float], tuple[float, float]]] = {
    "h6": {(0, 3): (0.0, -0.006), (3, 6): (0.0, -0.008), (6, 10): (0.0, -0.009)},
    "g6": {(0, 3): (-0.002, -0.008), (3, 6): (-0.004, -0.012), (6, 10): (-0.005, -0.014)},
    "m6": {(0, 3): (0.008, 0.002), (3, 6): (0.012, 0.004), (6, 10): (0.015, 0.006)},
    "H7": {(0, 3): (0.010, 0.0), (3, 6): (0.012, 0.0), (6, 10): (0.015, 0.0)},
}


def iso286_limits(tol: str, d: float) -> tuple[float, float]:
    for (lo, hi), lim in ISO286[tol].items():
        if lo < d <= hi:
            return lim
    raise KeyError((tol, d))


_G = Source("ISO 286-2:2010 (tolerance); vendor ground shaft (Misumi/HepcoMotion) for availability")
_D = Source("Typical micro-gearmotor D-shaft (N20/N10 style)", note="flat_depth = material removed from round",
            uncertain_fields=("flat_depth", "tolerance"))

SHAFTS: list[Shaft] = (
    [Shaft(float(d), "round", "h6", src=_G) for d in (2, 3, 4, 5, 6, 8)]
    + [Shaft(float(d), "round", "g6", src=_G) for d in (2, 3, 4, 5, 6, 8)]
    + [
        Shaft(3.0, "d_shaft", "h6", flat_depth=0.5, src=_D),  # N20: 3 mm, D across flat 2.5
        Shaft(2.0, "d_shaft", "h6", flat_depth=0.5, src=_D),  # N10/N20 small: across flat 1.5
        Shaft(4.0, "d_shaft", "h6", flat_depth=0.5, src=_D),
        Shaft(5.0, "d_shaft", "h6", flat_depth=0.5, src=_D),  # common 5 mm brushless/geared
    ]
)
