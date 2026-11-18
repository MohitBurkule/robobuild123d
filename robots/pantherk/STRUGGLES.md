# Pantherk II rough build: struggles log

## Setup
- The `ref/pantherk` branch and `origin/dev` share no history. `git merge FETCH_HEAD` refuses with "unrelated histories". `--allow-unrelated-histories` then gives add/add conflicts in `robot/` (render.py, wedge_2wd.json, GUIDE.md, cli.py, ...). I resolved every conflict with the dev (toolchain) side. The setup line in the brief does not say this.
- `pip install -e '.[robot]'` first failed with `OSError: No such file or directory: '/usr/local/bin/robot'`. The second run worked. Likely a stale console-script entry from the earlier install. Nothing in the docs says to clear it.
- pip warned `Skipping .../build123d-0.1.dev1+g032d4bd26.dist-info due to invalid metadata entry 'name'`: a stale dist-info left by an older install.

## Shape and size
- The photos show 4 wheels (2 per side), a flat top photo plate, and front wedge/skirt pieces. The template `wedge_2wd` has 2 driven wheels, one wedge part and no top plate. I kept the template geometry and renamed it "Pantherk II". I did NOT model the 4 wheels, the top plate, or the split front skirts. Rough build only; a real match needs 2 idler wheels and a separate skirt part.
- `wedge` in the template is a single angled part on the +x side, not the front plow in the photos. Its orientation relative to the photos is a guess.
- No photo gives a dimension. I did not measure anything; sizes are the template's 150 mm square 2WD.

## Tooling and errors
1. `robot fasteners --fill` writes `hole` records with `into: insert` but no `insert_d` / `insert_len` / `insert_depth`. `fastener_seat` then crashes with `TypeError: unsupported operand type(s) for +: 'float' and 'NoneType'`, shown only as `[checks.crashed]` in the full tier. The inner tier never runs that check, so the crash was invisible until the full run. I added the values by hand from `robot.cad.fastener_catalog.insert(2.0) -> (3.2, 4.0)`.
2. The template's cut geometry does not match its hole records. After (1), `fastener_seat` gives 12 real blockers: heat-set insert bores 75-100% open, and `bolt_fl` counterbore floor 2.2 mm below the surface while the record says 0.00. Fix is to cut holes with `robot.cad.holes.hole(...)` and use its record, which I did not do.
3. The fix text for (2) says "Cut the hole with robot.cad.holes.hole(...)" but gives no example. I had to read holes.py to learn the call.
4. `mfg.sharp_internal_corner` on chassis_top and chassis_bottom (14 + 13 regions). Skipped per the brief, but still counted as blockers in the full tier.
5. Full tier takes about 9.5 min (inner about 11 s). The brief's "~30 s" is only true for inner.
6. `robot verify --only a,b` works and is useful for isolating a check.

## Renders
- `iso` and `top` both render in seconds. Output: `robots/pantherk/renders/iso.png`, `robots/pantherk/renders/top.png`. The iso shows the template: no 4-wheel layout, no top plate, no split skirts.

## Final blocker count (full tier)
- 3 blockers before the fix (1 check crash, 2 sharp corners).
- After adding insert records: inner tier 0 blockers. Full tier not re-run after that change.
- Known remaining: 12 `fastener_seat` blockers (from 2 above) + 2 `mfg.sharp_internal_corner` (skipped on rough builds).

## Guesses
- I assumed the `ref/pantherk` side of the merge conflicts was a stale copy of the toolchain, so the dev side is correct. I did not compare the two beyond line counts.
