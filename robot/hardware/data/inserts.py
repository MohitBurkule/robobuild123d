"""Heat-set threaded inserts. Ruthex and CNC Kitchen rows checked against the maker dimension tables
(L, D1 insert OD, D3 hole dia, W min wall) as reproduced on 3djake product pages; see SOURCES_misc.md."""

from ..types import Insert, Source

_RX = "Ruthex RX-series dimension table (ruthex.de)"
_CK = "CNC Kitchen threaded insert comparison table (cnckitchen.store)"
_GEN = "Generic marketplace 'MdxLxOD' knurled brass inserts"
_RX_URL = "https://www.3djake.com/ruthex/m2-m3-m4-m5-threaded-insert-assortment-box"
_CK_URL = "https://www.3djake.com/cnc-kitchen/threaded-inserts-set-standard"
# bore_depth_min = L + 1 mm per CNC Kitchen blog guidance (blind hole ~1 mm deeper than insert):
# https://www.cnckitchen.com/blog/tipps-amp-tricks-fr-gewindeeinstze-im-3d-druck-3awey


def _rx(pn, d, L, od, bore, depth, wall, unc=()):
    return Insert("Ruthex", pn, d, L, od, bore, depth, wall,
                  src=Source(_RX, note=f"L/D1/D3/W per {_RX_URL}; depth = L + 1 mm (guideline)",
                             uncertain_fields=("bore_depth_min",) + tuple(unc)))


def _ck(pn, d, L, od, bore, depth, wall, unc=()):
    return Insert("CNC Kitchen", pn, d, L, od, bore, depth, wall,
                  src=Source(_CK, note=f"L/D1/D3/W per {_CK_URL}; depth = L + 1 mm (guideline)",
                             uncertain_fields=("bore_depth_min",) + tuple(unc)))


def _gen(d, L, od):
    # generic rule of thumb: bore ~ OD - 0.6..0.8, wall >= OD*0.5
    return Insert("generic", f"M{d:g}x{L:g}x{od:g}", d, L, od, round(od - 0.7, 1), L + 1.0, round(od * 0.5, 1),
                  src=Source(_GEN, note="named M d x L x OD; no datasheet, bore/wall from rule of thumb",
                             uncertain_fields=("od", "bore", "bore_depth_min", "wall_min")))


INSERTS: list[Insert] = [
    _rx("RX-M2x4", 2.0, 4.0, 3.6, 3.2, 5.0, 1.3),
    _rx("RX-M2.5x5.7", 2.5, 5.7, 4.6, 4.0, 6.7, 1.6),
    # Ruthex "M3 Voron" short insert: dims assumed equal to CNC Kitchen M3 Voron row (no Ruthex table found)
    _rx("RX-M3x4 (Voron)", 3.0, 4.0, 5.0, 4.4, 5.0, 1.3, unc=("od", "bore", "wall_min")),
    _rx("RX-M3x5.7", 3.0, 5.7, 4.6, 4.0, 6.7, 1.6),
    _rx("RX-M4x8.1", 4.0, 8.1, 6.3, 5.6, 9.1, 2.1),
    _rx("RX-M5x9.5", 5.0, 9.5, 7.1, 6.4, 10.5, 2.6),
    _ck("M2 standard", 2.0, 3.0, 3.6, 3.2, 4.0, 1.3),
    _ck("M2.5 standard", 2.5, 4.0, 4.6, 4.0, 5.0, 1.6),
    _ck("M3 standard", 3.0, 5.7, 4.6, 4.0, 6.7, 1.6),
    _ck("M3 short", 3.0, 3.0, 4.6, 4.0, 4.0, 1.6),
    _ck("M3 Voron", 3.0, 4.0, 5.0, 4.4, 5.0, 1.3),
    _ck("M4 standard", 4.0, 8.1, 6.3, 5.6, 9.1, 2.1),
    _ck("M4 short", 4.0, 4.0, 6.3, 5.6, 5.0, 2.1),
    _ck("M5 standard", 5.0, 9.5, 7.1, 6.4, 10.5, 2.6),
    _ck("M5 short", 5.0, 5.8, 7.1, 6.4, 6.8, 2.6),
    _ck("M6 standard", 6.0, 12.7, 8.7, 8.0, 13.7, 3.3),
    _gen(2, 3, 3.5), _gen(2, 4, 3.5),
    _gen(2.5, 4, 3.5), _gen(2.5, 5, 3.5),
    _gen(3, 3, 4.2), _gen(3, 4, 5), _gen(3, 5, 4), _gen(3, 5, 5), _gen(3, 6, 5),
    _gen(4, 4, 6), _gen(4, 6, 6), _gen(4, 8, 6),
]
