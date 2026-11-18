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
