# Bolt: build struggles (rough pass)

Scope: rough CAD attempt from the three AWS photos in `reference/`, about 20 minute cap.

## Result
- Blockers left: not measured. The `verify --fast --quick` run was killed by my 400 s timeout while still in the `practice` group (about 366 s alone). No verdict was printed.
- The spec is still the unmodified `wedge_2wd` template (renamed to "Bolt"). I did not get to edit geometry to match the photos.
- Render: `robots/bolt/renders/iso.png` and `top.png` were started in the background. They had not finished when this log was written. The render also runs verify groups (including `visual`), so it is slow.

## Where I got stuck
1. **Verify is slow with no progress signal.** `verify --fast --quick` ran for more than 6 minutes, and the `practice` group alone took 366 s. The output is a stream of `[ran] <group> <time>` lines with no summary until the end, so a killed run gives nothing. A `--only` bisect hint helps, but nothing in the first minute says how long the run will take.
2. **Render is not a cheap call.** Render printed the same group timing lines, so it seems to re-run verify groups before drawing. For a "just look at it" step that is surprising, and the docs do not say so.
3. **Template is a large generated JSON.** `wedge_2wd` is 88 KB of nested `shape` trees (`subtract`/`union`/`place`/`prism`). Changing a box size means finding the right nested node by hand. There is no obvious generator or param file next to the spec (the FACTS doc asks for `make_spec.py`, but this template does not have one).
4. **Reference pointers are stale.** `REFERENCE.md` says to use `robots/revron` or `robots/expandabot` for layout. `expandabot` exists, but I did not check whether it is a usable template for a 4-wheel-ish layout. The `reference:` mask/silhouette field needs a traced binary PNG mask, and nothing in the branch provides one for Bolt. I did not make one.
5. **Doc vs layout mismatch.** `robot/GUIDE.md` says the spec layout is `parts[]`, `fasteners[]`, `wires[]` and so on. The template has an extra top-level `calibration` key and `start_pose`/`ground_z`, which the guide does not mention.

## What I read from the photos (guesses)
- Body: cyan printed (PLA/PETG-like) shell, with clear acrylic side walls and a clear top window. The top has a white card label.
- Front: a sloped wedge/ramp front in cyan, with a clear acrylic cover.
- Drive: black linkage arms running front to back on each side (looks like a 4-bar or a lifter arm), 2 visible wheels per side in aws57, rear wheels on the lower side.
- Scale: small, roughly 60-70 mm wide in the photos. I did not measure this against any real dimension.
- Guessed but unverified: the black arms are carbon/nylon bars, not printed.

## Guesses I did not check
- I assumed a wedge robot_type with roller locomotion, which matches the template. The photos may show a lifter, not a wedge.
- I did not set up `reference` silhouette checks.

## Environment / install
- Python 3.13.18. `pip install -e '.[robot]'` succeeded with no errors (build123d, cadquery-ocp-novtk, manifold3d and friends).
- No missing tools so far.

## Final blocker count
- Not measured (verify did not finish). Treat the template defaults as untested for Bolt.

## Suggestions
- Print a per-group progress line with cumulative time, and a final summary even when killed (or write `--json` incrementally).
- Let `render` skip verify groups, or say in `--help` that it runs them.
- A small `make_spec.py` for the template would make it much easier to match photos.

## Bolt rebuild (Bolt agent, ~30 min cap)

### Result
- Likeness: FAIL, 1 blocker. aws63 passes (IoU 0.81, beats `revron_ant` 0.77), aws60 passes (0.80 vs `wedge_2wd` 0.79, marginal), aws57 fails (0.75 vs `hspin_bar` 0.83; rear third worst).
- Inner verify: 19 blockers in 19 root causes (12 shown, 7 hidden): 11 `proxy.interference` (side walls overlap chassis/wheels by 0.2 to 1 mm), 1 `connection.floating` (top_window has no fastener), 1 `mass.over` (150.3 g vs 150 g). Not run: full tier.
- Render: `robots/bolt/renders/iso.png`, `robots/bolt/renders/top.png`.
- Spec: built from `wedge_2wd` (template copy with 2 idler wheels, 2 raised side walls, a flat clear top window, and `reference` entries). It is recognisably a wedge with 4 wheels, but NOT like the photos: it is a closed box with a flat top. The photos show an open top, black linkage bars running front to back, and a clear front plow.

### Where I got stuck
1. **Template copy is the starting point the gate measures against.** The likeness gate scores against the closest stock template per photo, so a light edit of `wedge_2wd` often ties it (aws60: 0.79 vs 0.79). Reshaping the nested `wedge`/`chassis_*` shape trees is slow by hand. A param-driven template or a `gen build --hypothesis` for this layout would help.
2. **Photo masks are noisy.** The default-threshold `robot mask` picked up floor texture on aws60 (the mask looks like the whole frame) and includes floor on aws63 and aws57. A mask that is partly floor makes IoU targets unreachable for a real silhouette. No `--thr` is used so the gate's own mask check (IoU 0.85 against the default mask) still passes. It would help if the tool reported the background colour it chose or warned when floor is included.
3. **Wheel count vs drive.** REFERENCE.json says 4 wheels. The template has 2 motor-driven wheels, so the 2 extra wheels are idlers with no motor. The verifier then reports overlap but no separate idler rule; the doc does not say how to model a free wheel.
4. **Interference tolerance is tight.** Adding walls next to 28 mm wheels gave 0.2 mm overlaps against an 0.08 mm allowance. Nothing in the error says whether to move the part or the wheel.
5. **Likeness loop is fast.** `robot likeness` (about 15 to 45 s) was the useful loop; it printed the worst third and height/length ratio, which pointed to "too flat" correctly.
6. **Materials.** `acrylic` is not a material id; `polycarbonate` is. The error lists known ids, which was enough to fix it.

### Final blocker count
- Verify inner: 19. Likeness: 1 (aws57 silhouette).

### Suggestions
- Name the closest stock template in the likeness error and the margin needed, so you know whether to reshape or move away from it.
- A per-photo mask preview (or a warning when the mask touches the image border) would catch floor-included masks before the gate runs.
- Allow idler wheels in the spec (for example `"idler": true` on wheel parts) so the wheel-count check and drive checks agree.

## Bolt from-scratch rebuild (Bolt robot, 35 min cap, `robot gen` intent)

### Result
- Likeness: FAIL (2 blockers). Wheel count (4) and reference wiring now pass. aws57: IoU 0.82 vs 0.83 needed (beats `hspin_bar` 0.83 is required). aws63: IoU 0.77 vs 0.80 needed; worst third is the front (0.54), where the mask includes floor.
- Inner verify: 15 root causes, of which 12 are shown (overlaps of idler wheels with chassis, inserts and bolts, all 0.2 to 1.7 mm against 0.08 allowed). The 3 hidden causes were not inspected; the mass check reports 143.9 g with a range up to 170.8 g (`mass.may_be_over`).
- Renders: `robots/bolt/renders/iso.png`, `robots/bolt/renders/top.png`.
- Spec: `robot gen build --hypothesis wedge` with `zb -10, zt 16`, then patched by `out/patch_bolt.py` (not committed): 2 idler wheel parts plus `pin` connections, and `reference` entries for aws57 and aws63.

### Where I got stuck
1. The coordinator update (gate changed to an absolute 0.80 IoU floor, `likeness.weapon` added, idlers counted in the wheel total) came in mid-run. After merging `origin/dev` the first likeness run failed on wheel count and on missing `reference`. Idlers are not a generator option, so I added them by hand to the generated spec.
2. The generator's `wedge` hypothesis has no idler option, so idler wheels had to be hand-written as copies of `wheel_l` with a `pin` connection. The verifier gives no direction on where an idler can go without overlapping the chassis walls.
3. Photo masks: `robot mask` at default threshold includes floor on aws63 (left edge), which limits IoU on the front third. I did not tune `--thr`.
4. The body outline is still the generator's box. I did not get to reshape it to the plow silhouette; only height was raised.
5. Likeness takes about 20 to 60 s; it was the most useful loop. Verify inner took about 30 s.

### Final blocker count
- Verify inner: 15 root causes (12 shown). Likeness: 2 blockers.

### Likeness
- FAIL.

## Round: photo fit tools (robot mask --crop, fit-photo, likeness loop)

### What the new tools did
- `robot mask --crop`: aws63 had a second object (another robot's wheel) at the left edge. `crop: {"bolt.aws63.webp": [0.04,0,1,1]}` in REFERENCE.json removed it. The mask was checked by eye (Read) and holds one robot. aws57 needed no crop.
- `robot fit-photo --length 120 --weapon-axis x`: gave width 114, height 36, front ramp 54, length 120, weapon-like cylinder r36 at 108 mm from the back (IoU 0.85 coarse envelope). The body was set from these numbers via an explicit outline (x +-57, y -50..70), zb -10, zt 26.
- The fit-driven build was much closer than the default box (aws57 0.80, aws63 0.78 after idler patch).

### What it did not help with
- The fit's weapon cylinder (r36 along x) does not describe a wedge. The weapon stays `kind: wedge`, so the fitted cylinder is ignored. The weapon check is not clean.
- Taller bodies made it worse: zt 30 gave 0.78 / 0.79, zt 34 gave 0.78 / 0.79. The "too flat" hint is not fixed by height alone.
- A fresh `gen build` drops idler wheels and the reference block. `robots/bolt/patch.py` re-adds them (reproducible, do not hand-edit spec.json).

### Still missing
- Likeness FAILS: aws57 0.80 (needs 0.83, the stock `hspin_bar` template); aws63 0.78 (needs 0.80). Both are below the bar.
- Verify inner: 16 blockers / 13 root causes, mass 203.7 g over 150 g, footprint 169.5 mm over 150 mm, screws `bolt_c*` engage 0 mm in `insert_c*` (the insert sits 3 mm below the chassis top), idler overlap 0.70 mm with `chassis_bottom`, wiring routes stale (proxy.wiring) and two likeness overlays lack render records.
- The generator has no wedge-ramp option tied to the fitted ramp (54 mm). The outline is still a box.
- `fasteners --fill` added 8 hole records (`bolt_w*`, `insert_*`). The engagement issue was not fixed.

## Round 9 (outer look only, per coordinator)
- Outline reshaped to a chamfered rear (x +-42 at y -47, +-57 from y -10 to 60), y -47..60, zt 28. Rebuilt via gen + patch.py.
- Likeness: aws63 PASS (0.82 vs 0.80), aws57 FAIL by rounding (0.83 vs hspin_bar 0.83; rear third 0.69 worst). 1 blocker.
- Verify/fasteners not run this round (told to skip). Blocker count unknown.
- Struggles: aws57 plateaus at 0.83 whatever the length/width; photo has open top and black bars the generator cannot express; likeness takes ~100 s per round.

## Round 2 (kit, looks only)
- Rebuilt with `robot kit` (robots/bolt/kit.json: 112x104x32 box, ramp 56, 4 wheels r14, no weapon) + reference entries.
- Likeness: aws63 PASS 0.86; aws57 FAIL 0.80 (needs 0.83 vs hspin_bar). 1 blocker. Length/width/ramp sweeps plateau at 0.78-0.80.
- Remaining differences: photo has open top, black side bars, clear plastic plow, rounded rear; kit gives a plain wedge block. Kit lacks open-top/bars/clear plow. diff-photo needs a key; read sheet myself. Verify not run.

## Round 3
- Applied Haiku list: lower body (26), smaller wheels r11 moved inboard, ramp 44, front plate via 2 wide forks. Likeness: aws57 0.81 (FAIL, needs 0.83), aws63 0.81 pass. Still different: open top/rails, rear branded plate, trapezoid plan (kit box is rectangular).
