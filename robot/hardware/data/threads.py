"""ISO metric coarse threads M1.6-M5. d2/d3 basic values (ISO 724), As (ISO 898-1), tap drill (ISO 2306 / DIN 336)."""
from ..types import Source, Thread

_S = Source("ISO 261:1998 / ISO 724:1993 / ISO 898-1:2013", note="basic profile values; tap drill = d - P")

THREADS: dict[float, Thread] = {
    1.6: Thread(1.6, 0.35, 1.171, 1.373, 1.25, 1.27, _S),
    2.0: Thread(2.0, 0.40, 1.509, 1.740, 1.6, 2.07, _S),
    2.5: Thread(2.5, 0.45, 1.948, 2.208, 2.05, 3.39, _S),
    3.0: Thread(3.0, 0.50, 2.387, 2.675, 2.5, 5.03, _S),
    4.0: Thread(4.0, 0.70, 3.141, 3.545, 3.3, 8.78, _S),
    5.0: Thread(5.0, 0.80, 4.019, 4.480, 4.2, 14.2, _S),
}
