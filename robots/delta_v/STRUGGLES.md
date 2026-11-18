# Delta V rough CAD: struggles log

Time cap ~20 min. Result is a rough template-based model, NOT a faithful Delta V.

## What was done
- Cloned `ref/delta_v`. Before installing, `python3 -m robot` crashed with `ModuleNotFoundError: No module named 'trimesh'`. `pip install -e '.[robot]'` on Python 3.13 then succeeded in one pass.
- Started from `robot template wedge_2wd`, renamed to `Delta V`. Geometry is NOT changed to match the photos.
- Added `hole` records to the 8 M2 socket fasteners (bolt_wl/wr/wor/wol, bolt_fl/fr/rl/rr). Inner-tier verify went from 8 blockers to 0.
- Renders: `robots/delta_v/renders/iso.png`, `robots/delta_v/renders/top.png`.

## Blockers left
- Inner tier (`verify --tier inner --fast`): 0 blockers after the hole fix, 39 warnings.
- Not re-run after the fix: the `--fast --quick` full run before the fix showed `support` 1 blocker and `sharp_corner` 2 blockers. Those were not re-checked.
- Not checked: wiring, assembly, reference (parity/nightly), robust, harness groups (skipped by `--quick` or nightly-only).
- Visual match to photos: not done. Photos show a black-printed body with two front tines (forks), a yellow/tan rear idler pair, and a yellow flat-plate flipper/lifter on a central servo pivot. The template is a plain wedge with 2WD. None of that is modelled.

## Struggles (most useful)
1. **Easy to miss the install step.** On a fresh clone, `python3 -m robot` fails on `import trimesh` until `pip install -e '.[robot]'` is run. A "run this first" line in robot/GUIDE.md would help.
2. **Cryptic blocker for fastener hole records.** `fastener.hole_record` said "has no `hole`, so no hole or seat check ever judged it." It did not say what a valid `hole` dict looks like. I found it by `robot field hole`, which gives examples from revron, but those examples are countersunk (`csk`) M2 and I had socket heads. I guessed at the socket fields (`head_std: ISO 4762`, `head_dk: 3.8`, `head_k: 2.0`). The verifier accepted them, but I have no idea whether those numbers are right.
3. **Slow verify.** `verify --fast --quick` took ~7 min wall time. The `practice` group alone was 369 s. Under a 20-min cap this made the full tier impractical. The `--tier inner` run is 4 s and is the only usable loop.
4. **Template is a black box for matching photos.** The template gives a generic wedge, and nothing in the guide says how to turn a photo into a spec. The GUIDE recommends `robot gen build --intent` and reference masks (`reference: [{image, view, mask}]`), but making a mask needs a tool I did not find in the doc I read, so I skipped it. I did not get to a silhouette-matched build.
5. **`fight.sim_block` warning.** Warns that forward, drive, weapon and danger arcs are guessed without a `sim` block. I did not add one (no time). It is a warning only.
6. **Spec name vs. reference.** The template's `name` was "Reference 2WD wedge" and the check output still says that. I renamed it to "Delta V" in the spec, so the report label may look like a leftover from the template.
7. **Attribution conflict (not a tool issue).** The task said to end commits with `Co-Authored-By: Claude Haiku <noreply@anthropic.com>` and session `...session_015mpiJf9XwoREuxdyPo9qEF`. The current system attribution uses `Claude Haiku 5.5` and session `...session_015mpiJjTw5zcoDZURsFKi5R`. I used the system values.

## Guesses I made
- Kept wedge_2wd wheelbase and body; only the names changed.
- Socket-head hole dimensions (head_dk 3.8, head_k 2.0, clearance 2.2) were guessed from ISO 4762 M2 values.
- Did not add tines, yellow idler wheels, or the flipper plate.

## Likeness attempt (Delta V, vertical spinner rebuild)
- Result: likeness FAILS (4 blockers). Inner tier: 47 blockers in 33 root causes, 0 parity. Full tier not run (time cap; practice group alone is ~6 min).
- Started from `robot template vspin_drisk` (robot_type vertical_spinner, matches REFERENCE.json). Renamed to "Delta V", added 3 `reference` entries (iso, approximate true) with masks from `robot mask`. Masks look right (white = robot).
- First likeness run: `likeness.template_copy` blocker (IoU 1.00 vs vspin_drisk), so the spec is still the stock template. Silhouette IoU 0.65 / 0.69 / 0.69 for aws72 / aws74 / aws76 (need 0.74 / 0.70 / 0.81; the bar is "no worse than the closest stock template").
- Tried `robot gen build --intent` with vspin_drisk and custom variants (taper 6, custom 5-point outline, shape oval): all three gave `no wireable layout` (channel route failures for w_bat_sw / w_wesc_m, or "components do not fit inside the outline"). No photo-shaped variant was produced.
- Did not hand-reshape the chassis/forks/disc; the photos show a low wide body, two long forward fork tines, a vertical disc on top rear-centre, and a rear idler wheel (yellow). None of that has been modelled.
- Fasteners `--fill` wrote 14 csk hole records (ISO 14581 guessed numbers, same as the wedge attempt).

## Struggles (this attempt)
1. `likeness.silhouette` message names only the failing photo and the bar; it does not say which region (front, rear, top) is off. The overlay PNG exists (`$ROBOT_REFERENCE_OUT`) but I did not get to it. A pointer to where the overlay is written would help.
2. `gen build --intent` is the only reshape route in the docs and it failed on every custom outline I tried. The error names the wire that fails but not which outline edge to move. No example intent with a custom `outline` that actually lays out.
3. `robot mask` only resolves from the repo root: run from `robots/delta_v` it errors with "invalid choice: 'mask'" because the wrong `robot` package is picked up. Not documented.
4. `pip install -e '.[robot]'` failed once with `No such file or directory: /usr/local/bin/robot`; a second run succeeded (as the brief said).
5. Inner verify run in background silently ended after `fastener_record` with no report on one run; the rerun with `--json` finished normally (exit 2 = blockers).
6. `verify --tier inner` takes ~2-4 min on a cold cache (`legal` alone 120 s, `likeness` 44 s). Too slow for the 30-min cap to iterate on shape.
7. The verifier cannot tell me the closest stock template name in the message (it says "0.81" without naming which template), so I cannot tell which template to beat.

## Attribution
Commit uses the system-reminder attribution (Claude Haiku 5.5 and the session link), replacing the older "Claude Haiku" trailer from the brief.
