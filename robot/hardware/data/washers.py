"""Metric washers M1.6-M5: d1 min (nominal), d2 max, h nominal."""
from ..types import Source, Washer

WASHERS: list[Washer] = [
    *[Washer("plain", "ISO 7089", d, d1, d2, h, mass=g,
             src=Source("ISO 7089:2000", note="verified https://www.fasteners.eu/standards/ISO/7089/ (h = mid of min/max)"))
      for d, d1, d2, h, g in [(1.6, 1.7, 4.0, 0.3, 0.024), (2.0, 2.2, 5.0, 0.3, 0.037), (2.5, 2.7, 6.0, 0.5, 0.088),
                              (3.0, 3.2, 7.0, 0.5, 0.119), (4.0, 4.3, 9.0, 0.8, 0.308), (5.0, 5.3, 10.0, 1.0, 0.443)]],
    *[Washer("plain_small", "ISO 7092", d, d1, d2, h, src=Source("ISO 7092:2000"))
      for d, d1, d2, h in [(1.6, 1.7, 3.5, 0.3), (2.0, 2.2, 4.5, 0.3), (2.5, 2.7, 5.0, 0.5), (3.0, 3.2, 6.0, 0.5),
                           (4.0, 4.3, 8.0, 0.5), (5.0, 5.3, 9.0, 1.0)]],
    *[Washer("large", "ISO 7093-1", d, d1, d2, h, src=Source("ISO 7093-1:2000", note="starts at M3"))
      for d, d1, d2, h in [(3.0, 3.2, 9.0, 0.8), (4.0, 4.3, 12.0, 1.0), (5.0, 5.3, 15.0, 1.2)]],
    *[Washer("spring", "DIN 127 B", d, d1, d2, h, src=Source("DIN 127:1987", note="h = section thickness s"))
      for d, d1, d2, h in [(2.0, 2.1, 4.4, 0.5), (2.5, 2.6, 5.1, 0.6), (3.0, 3.1, 6.2, 0.8), (4.0, 4.1, 7.6, 0.9),
                           (5.0, 5.1, 9.2, 1.2)]],
]
