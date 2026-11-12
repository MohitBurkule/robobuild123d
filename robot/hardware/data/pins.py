"""Dowel and spring pins, d 1-4 mm."""

from ..types import Pin, Source

PINS: list[Pin] = [
    # ISO 2338 m6 (unhardened), lengths per standard table range
    Pin("dowel_m6", "ISO 2338", 1.0, (4, 5, 6, 8, 10), 0.2, Source("ISO 2338:1997", uncertain_fields=("chamfer",))),
    Pin("dowel_m6", "ISO 2338", 1.5, (4, 5, 6, 8, 10, 12, 16), 0.3, Source("ISO 2338:1997", uncertain_fields=("chamfer",))),
    Pin("dowel_m6", "ISO 2338", 2.0, (5, 6, 8, 10, 12, 16, 20), 0.35, Source("ISO 2338:1997")),
    Pin("dowel_m6", "ISO 2338", 2.5, (6, 8, 10, 12, 16, 20, 24), 0.4, Source("ISO 2338:1997")),
    Pin("dowel_m6", "ISO 2338", 3.0, (8, 10, 12, 16, 20, 24, 30), 0.5, Source("ISO 2338:1997")),
    Pin("dowel_m6", "ISO 2338", 4.0, (8, 10, 12, 16, 20, 24, 30, 40), 0.63, Source("ISO 2338:1997")),
    # ISO 8734 hardened
    Pin("dowel_hardened", "ISO 8734", 1.0, (3, 4, 5, 6, 8, 10), 0.2, Source("ISO 8734:1997", uncertain_fields=("lengths", "chamfer"))),
    Pin("dowel_hardened", "ISO 8734", 1.5, (4, 5, 6, 8, 10, 12, 16), 0.3, Source("ISO 8734:1997", uncertain_fields=("lengths", "chamfer"))),
    Pin("dowel_hardened", "ISO 8734", 2.0, (5, 6, 8, 10, 12, 16, 20), 0.35, Source("ISO 8734:1997", uncertain_fields=("lengths",))),
    Pin("dowel_hardened", "ISO 8734", 2.5, (6, 8, 10, 12, 16, 20, 24), 0.4, Source("ISO 8734:1997", uncertain_fields=("lengths",))),
    Pin("dowel_hardened", "ISO 8734", 3.0, (6, 8, 10, 12, 16, 20, 24, 30), 0.5, Source("ISO 8734:1997", uncertain_fields=("lengths",))),
    Pin("dowel_hardened", "ISO 8734", 4.0, (8, 10, 12, 16, 20, 24, 30, 40), 0.63, Source("ISO 8734:1997", uncertain_fields=("lengths",))),
    # ISO 8752 heavy spring pins (hole d = nominal, H12); chamfer field unused
    Pin("spring", "ISO 8752", 1.0, (4, 5, 6, 8, 10), None, Source("ISO 8752:2009", note="hole H12 = nominal d")),
    Pin("spring", "ISO 8752", 1.5, (4, 5, 6, 8, 10, 12, 16), None, Source("ISO 8752:2009", note="hole H12 = nominal d")),
    Pin("spring", "ISO 8752", 2.0, (4, 5, 6, 8, 10, 12, 16, 20), None, Source("ISO 8752:2009", note="hole H12 = nominal d")),
    Pin("spring", "ISO 8752", 2.5, (5, 6, 8, 10, 12, 16, 20, 24), None, Source("ISO 8752:2009", note="hole H12 = nominal d")),
    Pin("spring", "ISO 8752", 3.0, (5, 6, 8, 10, 12, 16, 20, 24, 30), None, Source("ISO 8752:2009", note="hole H12 = nominal d")),
    Pin("spring", "ISO 8752", 4.0, (6, 8, 10, 12, 16, 20, 24, 30, 40), None, Source("ISO 8752:2009", note="hole H12 = nominal d")),
]
