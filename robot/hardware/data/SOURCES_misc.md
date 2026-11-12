# Sources: misc hardware data

Values were taken from what is known of these standards and catalogs. No web lookup was done in this pass. Check every field listed in a record's `uncertain_fields` before you rely on it.

| Module | Source |
|---|---|
| inserts.py | Ruthex: https://www.ruthex.de ; CNC Kitchen: https://cnckitchen.store/collections/threaded-inserts (hole design table) |
| standoffs.py | Wurth WA-SSTII: https://www.we-online.com (Electromechanical > Spacers); Ettinger: https://www.ettinger.de |
| pins.py | ISO 2338, ISO 8734, ISO 8752 (e.g. https://www.fasteners.eu/standards/ISO/2338/) |
| circlips.py | DIN 471/472/6799 (e.g. https://www.smalley.com , https://www.fasteners.eu/standards/DIN/471/) |
| bearings.py | NMB miniature catalog https://www.nmbtc.com ; EZO https://www.ezo.co.jp ; SKF https://www.skf.com |
| orings.py | ISO 3601-1/-2; Parker ORD 5700 O-Ring Handbook https://www.parker.com/o-ring-handbook |
| shafts.py | ISO 286-2 tables (e.g. https://www.engineeringtoolbox.com/iso-fits-d_1215.html) |

## Uncertain values (verify)
- Inserts: every `wall_min`. RX-M3x4 OD and bore. CNC Kitchen M2 OD, M2.5 length and OD, M4 short length. Generic inserts are rule-of-thumb only, not datasheet values.
- Standoffs: every `male_len`. M3 AF: Wurth uses 5.5, Ettinger and generic often use 5.
- Pins: ISO 8734 length ranges. Chamfers for d1 and d1.5.
- Circlips: DIN 6799 `shaft_d` is the upper end of each shaft range; `groove_d` is the defining size. DIN 472 starts at bore 8. DIN 471 rows below d 3 were left out.
- Bearings: every Cr, C0r, rpm, mass and flange dimension. d/D/B are standard. The 681 and 682 widths are for the shielded versions.
- O-rings: groove dims for CS 1.0, 1.5 and 2.0 are interpolated. ID lists for non-1.78 CS are vendor stock, not ISO 3601. Strictly, only CS 1.78 is ISO 3601-1 class A here.
- Shafts: D-shaft flat depths and tolerances are typical. ISO 286 deviations are standard values.

## Schema
No changes to types.py. Extra module-level helpers: `GROOVE_STATIC_RADIAL` (orings.py), `ISO286` and `iso286_limits()` (shafts.py).
