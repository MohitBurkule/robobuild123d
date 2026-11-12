# Screw/nut/washer data sources

Values transcribed from standard tables as reproduced by vendor catalogues (not re-fetched in this pass; verify):
- Bossard eShop product tables (ISO 4762, 7380-1, 10642, 14581, 14583, 4032, 4035, 7089/7092/7093)
- fasteners.eu standards pages (DIN 7991, DIN 985, DIN 562, DIN 127, ISO 1207, ISO 4026/4029)
- Wuerth / Accu (M2, M2.5 button heads, not in ISO 7380-1)
- EJOT DELTA PT (WN 1411) design guide (PLASTIC_PILOT factors, head approximations)

## Discrepancies vs robot/cad/fastener_catalog.py
- CSK M3: catalog (6.0, 1.86) mixes DIN 7991 dk 6.0 with ISO 10642 k 1.86. DIN 7991 k = 1.7; ISO 10642 dk = 6.72.
- CSK M4/M5 catalog follows ISO 10642 (8.96/2.48, 11.2/3.1) — matches ISO 10642, not DIN 7991 (8.0/2.3, 10.0/2.8).
- DRIVE_KEY csk M3 socket depth 1.9: ISO 10642 t = 1.1, DIN 7991 t = 1.2. Catalog value looks wrong.
- DRIVE_KEY csk M1.6-M2.5 use hex keys; ISO 14581 is torx (T5/T6/T8). Hex-socket small csk only exist as vendor / DIN 7991-style.
- Everything else (clearance, tap drill, cap, button, hex/thin nut) matches.
