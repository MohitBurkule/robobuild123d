# Ice Breaker Junior - rough build struggles

Status: rough build from the `wedge_2wd` template. It passes the inner tier with 0 blockers and the full tier with 3 blockers (see below). It does NOT model the real robot's shape, flipper/fork tines or the two roller wheels.

## What was built
- Started from `python3 -m robot template wedge_2wd` (no template matches a flipper / lifter with rollers and forks; `robot templates` lists only revron, revron_ant, wedge_2wd).
- Shape and size were NOT changed toward the photos. This is a known gap: the photos show a flat chassis with a blue roller nose at one end, a second roller at the other end, two fork-like tines and two vertical servo-horn flippers. I ran out of time budget before editing geometry.
- `fasteners --fill` wrote 8 hole records. Mass 114.5 g of 150 g.
- Renders: `robots/ice_breaker_junior/renders/iso.png` and `robots/ice_breaker_junior/renders/top.png`.

## Struggles and confusing points
1. Merging `dev` into `ref/ice_breaker_junior` failed with "refusing to merge unrelated histories". Needed `--allow-unrelated-histories`. Then 6 add/add conflicts (robot/GUIDE.md, robot/cli.py, robot/render.py, robot/checks/*.py, robot/templates/wedge_2wd.json). Resolved by taking the dev side (`--theirs`) for all of them. A ref branch that is a fresh orphan history should not need this; the setup instructions should say so.
2. `pip install -e '.[robot]'` failed first with `OSError: No such file or directory: '/usr/local/bin/robot'`. It worked on a second run. Unclear whether the first run was a stale entry-point problem; no hint in the docs.
3. `robot verify --tier inner --llm` runs in about 15 s and is a good loop. Good.
4. Full tier (`robot verify SPEC --llm`) took about 5 minutes and produced:
   - `checks.crashed` (BLOCKER): `fastener_seat` raised `TypeError: unsupported operand type(s) for +: 'float' and 'NoneType'`. The traceback is not printed, only the message "Its verdicts are unknown". The error is somewhere in `robot/cad/seat.py` (`probe` at line 48 or `judge` at line 118). This is a toolchain bug: a crash should show its traceback, and the check should not crash on a spec that passes the inner tier. Found no hint in docs for it.
   - `mfg.sharp_internal_corner` on chassis_top and chassis_bottom (27 regions). Skipped as instructed for rough builds.
   - "overlap allowed" lines for the heat-set inserts, shown as info but printed under a blocker, which is confusing.
5. `robot/docs/FACTS.md` and `GUIDE.md` are long (9 KB and 58 KB). The GUIDE has no quick start for picking a template by robot type, so I could not tell which template to start from.
6. No template for a flipper or lifter with roller wheels and forks; wedge_2wd is the closest, but it is a plain wedge. A small-model agent would need a flipper/lifter template or a how-to for adding a flipper.
7. The reference REFERENCE.md says "see robots/revron, robots/expandabot for layout". `robots/expandabot` does not exist on this branch.

## Blockers left (full tier)
- 1 crash: `fastener_seat` TypeError (toolchain bug).
- 2 sharp-corner blockers (chassis_top, chassis_bottom), skipped on purpose.
- Total: 3 blockers. Inner tier: 0.

## Toolchain suggestions
- Print the traceback when a check crashes (or give the file:line).
- Make `sharp_internal_corner` a warning in rough mode, or accept a `--rough` flag.
- Add a flipper/lifter template and a robot-type-to-template table in GUIDE.md.

## Round 2 (from scratch, vspin_drisk generator)
- Built with `gen build` (vspin_drisk, outline 104x76, teeth 3) then `patch_after_gen.py out/vspin_drisk.json spec.json 6 36 66` (shifts disc to mid-length, shortens forks, widens disc via hub, moves wheels out to rear corners, bigger wheels).
- Likeness: FAIL (3 blockers): weapon check passes; silhouette IoU 0.70 / 0.64 / 0.69 (need 0.80). Photo forks angle downward and wheels bulge past rear; not modelled.
- Inner verify: 82 blockers, mass 195 g vs 150 g (stock drisk is heavy). Not worked on per coordinator instruction (looks only).
- Generator gaps: drisk always places the disc ahead of the body (80% of length, fails "middle"); no intent key for weapon position, weapon width, 2 rear outboard wheels, fork length; no way to tilt forks. likeness takes ~2 min on a loaded machine.
