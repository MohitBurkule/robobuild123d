"""Miniature deep-groove ball bearings (ZZ shielded dims). d/D/B are ISO 15 / maker standard dimensions.
Load ratings, rpm (grease, shielded) and mass are typical catalog values (NMB/EZO/SKF/NSK) recalled, not
read per-row; all marked uncertain. Flanged dims per NMB/MinebeaMitsumi flanged series.
"""

from ..types import Bearing, Source

_DIM = "ISO 15 / NMB-EZO miniature bearing catalog"
_U = ("C_dyn_N", "C0_N", "max_rpm", "mass")

# designation: d, D, B, Cr N, C0r N, rpm, mass g
_T = {
    "MR52": (2, 5, 2.5, 169, 50, 85000, 0.2),
    "MR63": (3, 6, 2.5, 230, 74, 71000, 0.3),
    "MR74": (4, 7, 2.5, 280, 107, 60000, 0.4),
    "MR83": (3, 8, 3, 615, 179, 60000, 0.7),
    "MR84": (4, 8, 3, 435, 139, 56000, 0.6),
    "MR85": (5, 8, 2.5, 305, 131, 53000, 0.4),
    "MR95": (5, 9, 3, 475, 168, 50000, 0.7),
    "MR105": (5, 10, 4, 715, 280, 50000, 1.2),
    "MR106": (6, 10, 3, 545, 218, 45000, 0.8),
    "MR115": (5, 11, 4, 715, 280, 48000, 1.8),
    "MR117": (7, 11, 3, 500, 201, 43000, 0.9),
    "MR128": (8, 12, 3.5, 560, 260, 42000, 1.2),
    "MR148": (8, 14, 4, 816, 400, 38000, 2.0),
    "681": (1, 3, 1, 80, 23, 130000, 0.03),
    "682": (2, 5, 2.3, 186, 50, 85000, 0.2),
    "683": (3, 7, 3, 425, 130, 63000, 0.5),
    "684": (4, 9, 4, 705, 225, 53000, 1.1),
    "685": (5, 11, 5, 790, 281, 45000, 2.0),
    "686": (6, 13, 5, 1190, 440, 40000, 2.6),
    "687": (7, 14, 5, 1290, 510, 40000, 3.0),
    "688": (8, 16, 5, 1610, 710, 38000, 3.6),
    "689": (9, 17, 5, 1330, 665, 36000, 4.0),
    "692": (2, 6, 3, 365, 98, 75000, 0.4),
    "693": (3, 8, 4, 615, 179, 60000, 0.9),
    "694": (4, 11, 4, 1050, 345, 48000, 1.7),
    "695": (5, 13, 4, 1190, 430, 43000, 2.4),
    "696": (6, 15, 5, 1910, 670, 40000, 4.0),
    "697": (7, 17, 5, 1770, 715, 36000, 5.0),
    "698": (8, 19, 6, 2240, 910, 36000, 7.3),
    "699": (9, 20, 6, 2490, 1090, 34000, 8.0),
    "603": (3, 9, 5, 630, 187, 56000, 1.7),
    "604": (4, 12, 4, 1050, 345, 48000, 2.0),
    "605": (5, 14, 5, 1460, 505, 40000, 3.5),
    "606": (6, 17, 6, 2490, 835, 38000, 6.0),
    "607": (7, 19, 6, 2570, 885, 36000, 8.0),
    "608": (8, 22, 7, 3290, 1360, 34000, 12.0),
    "623": (3, 10, 4, 695, 218, 50000, 1.6),
    "624": (4, 13, 5, 1430, 485, 40000, 3.0),
    "625": (5, 16, 5, 1910, 670, 36000, 5.0),
    "626": (6, 19, 6, 2570, 885, 32000, 8.0),
}

# Rows whose Cr/C0r/grease-rpm were read from the NSK flanged metric miniature listing (same bearing, flange
# variant): https://www.nsk.com/au-en/engineering/products/bearings/ball-bearings/deep-groove-ball-bearings/
# extra-small-ball-bearings-and-miniature-ball-bearings-metric-series-with-flamge.html (pages p=1..6)
_NSK_RATED = {"MR63", "MR74", "MR83", "MR84", "MR85", "MR95", "MR106", "MR117", "682", "683", "684", "685",
              "686", "687", "692", "693", "694", "695", "696", "697", "603", "604", "605", "606", "607",
              "623", "624", "625", "626"}
# Flange D1/C1 confirmed in the same NSK listing (ZZ rows).
_NSK_FLANGE = {"MR63", "MR74", "MR84", "MR85", "MR95", "MR105", "MR106", "MR117", "682", "683", "684",
               "686", "693", "694", "695", "696", "623", "624", "626"}
_NSK_URL = ("NSK flanged metric miniature listing, nsk.com/au-en/.../extra-small-ball-bearings-and-miniature-"
            "ball-bearings-metric-series-with-flamge.html")

# flanged variants: base -> (flange_D, flange_B) for shielded (ZZ) versions
_FL = {
    "MR63": (7.2, 0.6), "MR74": (8.2, 0.6), "MR83": (9.2, 0.6), "MR84": (9.2, 0.6),
    "MR85": (9.2, 0.6), "MR95": (10.2, 0.6), "MR105": (11.6, 0.8), "MR106": (11.2, 0.6),
    "MR115": (12.5, 0.8), "MR117": (12.2, 0.6), "MR128": (13.6, 0.8), "MR148": (15.6, 0.8),
    "682": (6.1, 0.6), "683": (8.1, 0.8), "684": (10.3, 1.0), "685": (12.5, 1.0),
    "686": (15.0, 1.1), "688": (18.0, 1.1), "693": (9.5, 0.9), "694": (12.5, 1.0),
    "695": (15.0, 1.0), "696": (17.0, 1.2), "623": (11.5, 1.0), "624": (15.0, 1.0),
    "625": (18.0, 1.2), "626": (22.0, 1.5),
}


def _b(base, name, row, fl=None):
    d, D, B, cr, c0, rpm, m = row
    unc = ("mass",) if base in _NSK_RATED else _U
    if fl and base not in _NSK_FLANGE:
        unc += ("flange_D", "flange_B")
    note = "ZZ shielded; open versions may be narrower (e.g. 683 open B=2)"
    if base in _NSK_RATED or (fl and base in _NSK_FLANGE):
        note += "; ratings/grease rpm/flange per " + _NSK_URL
    return Bearing(name, d, D, B, fl[0] if fl else None, fl[1] if fl else None, cr, c0, rpm, m,
                   src=Source(_DIM, note=note, uncertain_fields=unc))


BEARINGS: list[Bearing] = [_b(k, k + "ZZ", v) for k, v in _T.items()]
BEARINGS += [_b(k, ("F" if not k.startswith("MR") else "M") + ("F" + k[2:] if k.startswith("MR") else k) + "ZZ",
                _T[k], _FL[k]) for k in _FL]
# Flanged naming: MR63 -> MF63ZZ, 683 -> F683ZZ.
