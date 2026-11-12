# Screw/nut/washer data sources

## Verified this pass (URLs actually fetched)
- ISO 4762 M1.6-M5 dk/k/s/t/b: https://www.fasteners.eu/standards/ISO/4762/ (all match; no masses on page)
- DIN 7991 M3-M5 dk/k/s: https://www.fasteners.eu/standards/DIN/7991/ (match; t differs, see below; no M2/M2.5)
- ISO 10642: https://www.fasteners.eu/standards/ISO/10642/ (page lists DIN 7991-like values; conflicts with ours)
- ISO 7380-1 M3: https://westfieldfasteners.co.uk/Standards/ScrewBolt-SHBtn-M.pdf, https://fasten.it/en/norms/norm/din_en_iso_7380-1
- ISO 4032 M1.6-M5: https://www.fasteners.eu/standards/ISO/4032/ (all match)
- DIN 985 M3-M5 s/h/e/mass: https://www.fasteners.eu/standards/DIN/985/ (match)
- ISO 7089 M1.6-M5 d1/d2/h/mass: https://www.fasteners.eu/standards/ISO/7089/ (match)

## Corrections / changes made
- No numeric dimension was found wrong. Added masses: DIN 985 M3-M5 (0.5/1.0/1.4 g), ISO 7089 M1.6-M5.
- DIN 7991 M3-M5 `t` marked uncertain (fasteners.eu t min 0.95/1.5/2.05 vs our 1.2/1.8/2.3).
- ISO 10642 dk/k/t marked uncertain (source conflict).
- ISO 7380-1 M4/M5 `t` marked uncertain (not re-checked).

## Still unverified (not fetched)
threads.py, ISO 4035, ISO 10511, DIN 562, ISO 7092/7093, DIN 127, ISO 14581, 14583, 7045, 1207, 4026/4029,
WN 1411, PLASTIC_PILOT, button M2/M2.5, DIN 7991 M2/M2.5, all screw mass_per_1000.

## Discrepancies vs robot/cad/fastener_catalog.py
- CSK M3: catalog (6.0, 1.86) mixes DIN 7991 dk 6.0 with ISO 10642 k 1.86. DIN 7991 k = 1.7; ISO 10642 dk = 6.72.
- CSK M4/M5 catalog follows ISO 10642 (8.96/2.48, 11.2/3.1) — matches ISO 10642, not DIN 7991 (8.0/2.3, 10.0/2.8).
- DRIVE_KEY csk M3 socket depth 1.9: larger than both ISO 10642 and DIN 7991 values. Catalog value looks wrong.
- DRIVE_KEY csk M1.6-M2.5 use hex keys; ISO 14581 is torx (T5/T6/T8).
