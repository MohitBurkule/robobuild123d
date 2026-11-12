"""Brass hex standoffs. AF per Wurth WA-SSTII / Ettinger catalog ranges (M2 AF4, M2.5 AF5, M3 AF5/5.5)."""

from ..types import Source, Standoff

_W = "Wurth Elektronik WA-SSTII / WA-SMSI catalog; Ettinger hex spacer catalog"
_LEN = (3, 4, 5, 6, 8, 10, 12, 15, 20, 25, 30)
_AF = {2.0: 4.0, 2.5: 5.0, 3.0: 5.5}
_MALE = {2.0: 4.0, 2.5: 5.0, 3.0: 6.0}

STANDOFFS: list[Standoff] = [
    Standoff(fam, d, _AF[d], float(L), male_len=(_MALE[d] if fam == "mf" else None),
             src=Source(_W, note="lengths = common catalog range; check stock per length",
                        uncertain_fields=("male_len",) + (("af",) if d == 3.0 else ())))
    for d in (2.0, 2.5, 3.0)
    for fam in ("ff", "mf")
    for L in _LEN
]
# Note: M3 AF5 also common (Ettinger, generic) -- af=5.5 is Wurth; treat as uncertain.
