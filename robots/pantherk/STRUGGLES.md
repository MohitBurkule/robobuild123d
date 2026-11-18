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

## Rebuild from scratch (ref/pantherk, after coordinator gate update)

Built with the chassis generator (`gen build --intent`), not the template. Intent: `hypothesis: wedge`, shape box.
Spec: `robots/pantherk/spec.json`. Intent: `robots/pantherk/intent.json`. Renders: `robots/pantherk/renders/iso.png`, `top.png`.

### Where stuck / confusing
- No `robot likeness` CLI subcommand exists (brief says it does). The gate is `robot verify SPEC --only likeness`. Overlays are only written by calling `robot.checks.likeness.cli_main(spec, out_dir=...)` directly. Running `python3 -m robot.checks.likeness` rewrites the shipped `robot/templates/likeness_data.npz` in the repo; I restored it with git checkout.
- The `wedge` hypotheses are all 2WD. `--hypothesis "weapon=wedge,drive_layout=4WD"` lists 14448 valid slugs, but `gen build` refuses it: `no assembler for wedge-...-4WD ... yet (buildable: hspin_bar, lifter, none_pusher, vspin_drisk, wedge)`. Workaround: build 2WD and add 2 idler wheels by hand.
- Idler wheels need the same chassis clearance cuts as the driven wheels. There is no generator option for them. I copied every chassis node positioned at the driven wheel (x +-34.4, y -16) to y +14 by script. Interference with chassis_bottom went away after that.
- The generated wedge baseline already contains 6 boxes with a non-positive size (`chassis_bottom`: 400x135x-4.5 and 48x32x-8 cut boxes). In the json verify run, `validity.load` reports this as a blocker (`box size must be a positive finite number, got -4.5`). The inner-tier run before it did not show that error, so I could not tell whether it is cache-dependent. This looks like a generator bug.
- Inner tier after the idler edits: 33 blockers in 21 root causes. The categories are proxy.assembly (baseline teardown never removed insert_c0/insert_w0/bolt_c0/bolt_w0), proxy.wiring (wire ports moved 54-65 mm since baseline route), and proxy.interference (small overlaps). These are baseline proxies on the generated spec, not fixed.
- `fasteners --fill` wrote 8 hole records with insert_d/insert_len/insert_depth. Not re-checked by a full verify.
- mfg.sharp_internal_corner skipped per brief. Full tier not run (about 10 min).

### Likeness (FAIL, 2 blockers; likeness.type now PASS)
- likeness.type passes after the 4-wheel change (driven + idler counted as modelled wheels).
- aws67 (iso): IoU 0.72 (floor 0.80). Model overhangs the front-left corner (red), photo has side wings and wheels outboard (blue).
- aws66 (front): IoU 0.89 (need 0.90, must not be worse than stock wedge_2wd at 0.90). The model is essentially the stock wedge_2wd body.
- Tried a `shape: round` outline variant: worse (0.69 and 0.85). Not kept.
- Not fixed: the outline and wedge need hand reshaping (wedge prism, side wings, wheel outboard position) that the intent cannot express. I ran out of time budget.

### Final blocker count
- Inner tier: 33 blockers (21 root causes), plus 1 validity.load in the JSON run (negative box size, see above).
- Likeness: 2 blockers (silhouette). Result: FAIL.
