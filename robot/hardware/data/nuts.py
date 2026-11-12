"""Metric nuts M1.6-M5: s nominal, m max, e min."""
from ..types import Nut, Source

NUTS: list[Nut] = [
    *[Nut("hex", "ISO 4032", d, s, m, e, src=Source("ISO 4032:2012"))
      for d, s, m, e in [(1.6, 3.2, 1.3, 3.41), (2.0, 4.0, 1.6, 4.32), (2.5, 5.0, 2.0, 5.45), (3.0, 5.5, 2.4, 6.01),
                         (4.0, 7.0, 3.2, 7.66), (5.0, 8.0, 4.7, 8.79)]],
    *[Nut("thin", "ISO 4035", d, s, m, e, src=Source("ISO 4035:2012"))
      for d, s, m, e in [(1.6, 3.2, 1.0, 3.41), (2.0, 4.0, 1.2, 4.32), (2.5, 5.0, 1.6, 5.45), (3.0, 5.5, 1.8, 6.01),
                         (4.0, 7.0, 2.2, 7.66), (5.0, 8.0, 2.7, 8.79)]],
    *[Nut("nyloc", "DIN 985", d, s, m, e, src=Source("DIN 985:1987", uncertain_fields=u))
      for d, s, m, e, u in [(2.0, 4.0, 2.8, 4.32, ("m",)), (2.5, 5.0, 3.0, 5.45, ("m",)), (3.0, 5.5, 4.0, 6.01, ()),
                            (4.0, 7.0, 5.0, 7.66, ()), (5.0, 8.0, 5.0, 8.79, ())]],
    *[Nut("nyloc", "ISO 10511", d, s, m, e, src=Source("ISO 10511:2012", note="thin type, close to DIN 985",
                                                     uncertain_fields=("m",)))
      for d, s, m, e in [(3.0, 5.5, 3.9, 6.01), (4.0, 7.0, 5.0, 7.66), (5.0, 8.0, 5.0, 8.79)]],
    *[Nut("square", "DIN 562", d, s, m, src=Source("DIN 562:1986", uncertain_fields=("m",) if d < 3 else ()))
      for d, s, m in [(1.6, 3.2, 1.0), (2.0, 4.0, 1.2), (2.5, 5.0, 1.6), (3.0, 5.5, 1.8), (4.0, 7.0, 2.2),
                      (5.0, 8.0, 2.7)]],
]
