# Struggles: Team Phyte's Little Sytes (rough build)

## What was built
- Started from `wedge_2wd` template (`python3 -m robot template wedge_2wd`). Geometry NOT edited toward the photos: the template is a low wedge with two rear wheels, which matches the photos in class, but the ramp, side tabs, switch and green/black split are not modelled. Name set to "Team Phyte's Little Sytes".
- `robot fasteners --fill` wrote 8 hole records.
- Inner verify: 0 blockers, mass 114.5 / 150 g.
- Full verify: 13 root causes (see `verify_full.txt`).

## Struggles and blockers
1. **Setup: `git merge FETCH_HEAD` of dev refused** ("unrelated histories"). Retried with `--allow-unrelated-histories`: conflicts in GUIDE.md, checks/fastener_record.py, checks/support.py, cli.py, render.py, templates/wedge_2wd.json. Aborted the merge. Instead copied the three toolchain pieces I needed from dev by hand: `robot/fasten_fill.py` (+ its test), the `fasten_fill` entry in `cli.py`, and the `render.py` change that skips the full verify unless `--markers/--checks` (fast renders). The ref branch's own CLI had no `fasteners` command at all.
2. **Confusing crash:** `fastener_seat` raised `TypeError: float + NoneType` in `robot/cad/seat.py:106`. Cause: `fasteners --fill` writes `into: "insert"` but no `insert_d` / `insert_len`. Patched in the spec by hand (3.2 mm bore, 3.5 mm length, a guess). The fill tool should emit these from the insert catalog.
3. **Seat blockers after the patch:** `insert_bore` open or wall-missing on 8 bolts, and `cbore_depth` recorded 0 while the head floor is 2.2 mm below the surface on the four chassis bolts (`bolt_fl/fr/rl/rr`). Not fixed: I did not work out the intended insert-bore rule.
4. **`support.loose`:** the wedge (with its inserts) slides +y at least 10 mm. Its bolts go through the wedge into its own inserts, so nothing holds it to the chassis. A real pivot/hinge or a `connections` hold would be needed. Not done.
5. **`mfg.sharp_internal_corner`:** many concave corners on both chassis halves. Skipped as the brief allows for rough builds.
6. The `--markers` flag used by `render` is only defined in the dev version of the render CLI; in the ref branch the patched `render.py` reads `a.markers`, which is defined there, so renders work.

## Final blocker count
- Full tier: 13 root causes. 1 support.loose, 10 fastener_seat (insert_bore / cbore_depth), 2 mfg.sharp_internal_corner (skipped by brief; the verifier reports them as blockers).
- Inner tier: 0 blockers.

## Not done (time cap ~25 min)
- No shape/size edits toward the photos (ramp, tabs, switch).
- Wedge hold to chassis.
- Insert and counterbore seat values.

## Rebuild from scratch (generator run)

Built from scratch with the chassis generator, not from a template: `robot gen build --intent intent.json --hypothesis wedge --no-gate` (intent.json: hypothesis wedge, taper 6, box shape). Spec at spec.json, intent at intent.json. Merged origin/dev (gate update #210) and pulled the ref branch REFERENCE.json (now weapon kind wedge, front, width 0.95) as the coordinator asked.

Struggles:
1. Photo masks are two-robot images. Each of the three photos shows a pair of robots side by side. `robot mask` has no crop/region option, so the mask covers both and a one-robot model cannot reach IoU 0.80. This is the main reason likeness fails; I did not hand-edit masks.
2. Reshape is limited: taper 10 gives `no wireable layout` in the generator, so the intent could not express the deeper scoop I wanted. Only taper 6 was kept. No outline or weapon-placement edits were made (the intent has no outline override I could fit in the time cap).
3. `robot gen build --no-gate` prints a `TypeError` from a version regex at `list-hypotheses` when run before the dev merge. Harmless, but confusing.
4. verify inner tier: 22 blockers in 10 root causes. 6 are `proxy.assembly` (insert_c0/c1/w0/w1 and bolts; teardown never removes the inserts; the wedge and chassis_top cannot come out). 1 is `wire.render_wires` (renders lack a `.json` record; re-render with checks on). 3 are `likeness.silhouette`.
5. Likeness renders are not checked by the wire group unless rendered with checks; the plain `render` command does not write the record.

Final blocker count: inner tier 10 root causes (22 blockers). Likeness: FAIL (3 blockers: IoU 0.61 / 0.54 / 0.61 vs 0.80 needed).
