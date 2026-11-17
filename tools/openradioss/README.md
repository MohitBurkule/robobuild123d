# OpenRadioss impact calibration (offline)

Calibrates the MuJoCo breakable-weld damage layer: for a rigid steel tooth (spinner tip)
hitting a clamped printed plate, how much energy is absorbed, peak contact force, rebound
speed, and whether the plate fractures — per material x thickness x speed.

Install: `tools/openradioss/setup.sh` (downloads latest linux64 release zip from GitHub into
`$OPENRADIOSS_HOME`, default `~/.cache/openradioss`; idempotent). Then
`eval "$(tools/openradioss/setup.sh --env)"` to export OPENRADIOSS_PATH, RAD_CFG_PATH,
RAD_H3D_PATH, LD_LIBRARY_PATH.

Run sweep: `python -m robot.fight.radioss` -> `robot/fight/data/impact_table.json`
(`{"PLA_3mm": [{"v", "E_abs", "fracture", "peak_N", "eroded_frac", "v_rebound"}, ...]}`).
Single case: `robot.fight.radioss.impact_case(0.010, 40, 3, "PLA")`.
Materials (approx. Johnson-Cook LAW2 + /FAIL/JOHNSON constant-strain failure): PLA, PETG,
TPU, PC, AL6061, HARDOX. Mesh: 16x16 shells on 40 mm plate (tune `n_el`).

Tests: `pytest robot/tests/test_fight_radioss.py` (integration test skips without binaries).
