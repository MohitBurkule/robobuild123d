"""Heat-set threaded inserts. Values from maker datasheets (recalled; see SOURCES_misc.md)."""

from ..types import Insert, Source

_RX = "Ruthex RX-series datasheet (ruthex.de)"
_CK = "CNC Kitchen threaded insert product page (cnckitchen.store)"
_GEN = "Generic marketplace 'MdxLxOD' knurled brass inserts"


def _rx(pn, d, L, od, bore, depth, wall, unc=()):
    return Insert("Ruthex", pn, d, L, od, bore, depth, wall,
                  src=Source(_RX, note="bore = recommended hole for FDM; depth = L + ~1 mm",
                             uncertain_fields=("wall_min",) + tuple(unc)))


def _ck(pn, d, L, od, bore, depth, wall, unc=()):
    return Insert("CNC Kitchen", pn, d, L, od, bore, depth, wall,
                  src=Source(_CK, note="hole dia per CNC Kitchen 'hole design' table",
                             uncertain_fields=("wall_min",) + tuple(unc)))


def _gen(d, L, od):
    # generic rule of thumb: bore ~ OD - 0.6..0.8, wall >= OD*0.5
    return Insert("generic", f"M{d:g}x{L:g}x{od:g}", d, L, od, round(od - 0.7, 1), L + 1.0, round(od * 0.5, 1),
                  src=Source(_GEN, note="named M d x L x OD; no datasheet, bore/wall from rule of thumb",
                             uncertain_fields=("od", "bore", "bore_depth_min", "wall_min")))


INSERTS: list[Insert] = [
    _rx("RX-M2x3", 2.0, 3.0, 3.6, 3.2, 4.0, 1.3),
    _rx("RX-M2.5x4", 2.5, 4.0, 4.6, 4.0, 5.0, 1.5),
    _rx("RX-M3x4", 3.0, 4.0, 4.5, 4.0, 5.0, 1.6, unc=("od", "bore")),
    _rx("RX-M3x5.7", 3.0, 5.7, 4.6, 4.0, 6.7, 1.6),
    _rx("RX-M4x8.1", 4.0, 8.1, 6.3, 5.6, 9.1, 2.0),
    _ck("M2 standard", 2.0, 4.0, 3.6, 3.2, 5.0, 1.3, unc=("od",)),
    _ck("M2.5 standard", 2.5, 5.7, 4.6, 4.0, 6.7, 1.5, unc=("length", "od")),
    _ck("M3 standard", 3.0, 5.7, 4.6, 4.4, 6.7, 1.6),
    _ck("M3 short", 3.0, 3.0, 4.6, 4.4, 4.0, 1.6),
    _ck("M4 standard", 4.0, 8.1, 6.3, 5.6, 9.1, 2.0),
    _ck("M4 short", 4.0, 4.0, 6.3, 5.6, 5.0, 2.0, unc=("length",)),
    _gen(2, 3, 3.5), _gen(2, 4, 3.5),
    _gen(2.5, 4, 3.5), _gen(2.5, 5, 3.5),
    _gen(3, 3, 4.2), _gen(3, 4, 5), _gen(3, 5, 4), _gen(3, 5, 5), _gen(3, 6, 5),
    _gen(4, 4, 6), _gen(4, 6, 6), _gen(4, 8, 6),
]
