# Stronghold: rough CAD build struggles

Scope: rough build from the three AWS photos (aws72, aws74, aws76). Not optimised. Time cap was about 20 minutes and was exceeded, mostly by verify runtime.

## What was done
- Install: `pip install -e '.[robot]'` on Python 3.13 worked with no errors.
- Start point: `robot template wedge_2wd` (no change to geometry yet, so this is the stock 2WD wedge, NOT yet Stronghold-shaped). Stronghold looks like a fork/lifter-type front (two spike forks, black TPU arches, aluminium side plates, blue/green rear gear housing), so `wedge` is only a placeholder.
- Renders produced: `robots/stronghold/renders/iso.png` and `robots/stronghold/renders/top.png`, both of the unmodified template.

## Verify results
- Run 1 (`verify --fast --quick`): 3 groups blocked (support 1, fastener_record 8, sharp_corner 2). Took about 7 min.
- Run 2 (same command with `--json`): **11 blockers, 98 warnings, 284 checks passed**, parity score 1.00 (not gating). Also about 7 min.
- Fix rounds: 0 of 6. I did not get to fixing anything, so the blocker count left is 11 root causes.

## Struggles, in order of how much they cost
1. **Runtime.** `--fast --quick` still took 7 min. The `practice` group alone was 370 s. There is no progress indicator beyond per-group lines, so it is hard to tell a hang from work. This alone ate the time budget. A `--tier inner` quick loop would be a much better default for iteration; the GUIDE says `--tier inner --llm` is the fast loop, but I did not try it.
2. **Template is not a Stronghold.** The first step is "start from a template, then edit to match the photos", but nothing in the docs says how far to deviate from a template before starting over. Stronghold's forks, arches and side plates are not represented; I did not get to change them.
3. **fastener.hole_record (8 blockers).** Every M2 fastener in the template says "has no `hole`, so no hole or seat check ever judged it". GUIDE and FACTS say to copy `robots/revron/spec.json` for fastener records, but I did not check that file, so I do not know whether the template is out of date with the checker or the fastener records are just missing. The message does not say which field to add. This is the clearest gap in the hints.
4. **support.loose.** The wedge (and its four inserts) slides freely in +y. The template depends on the wedge being fastened to the chassis via the inserts, but the bolts have no hole records, so the checker does not count them as fastening it. Likely the same root cause as (3).
5. **mfg.sharp_internal_corner (2 blockers, 28 concave regions).** Both chassis halves have many concave corners below r 1 mm. The GUIDE says `round_inside` fixes this "by construction", but the template's prism/box unions do not use it. Adding `round_inside` around the pocket unions is the obvious fix, but I did not do it.
6. **Cache/time confusion.** The second verify run reported `[cached]` for many groups yet still took 7 min. I could not tell from the output which numbers are cache hits and which are real work, and `ROBOT_CACHE` is not in the docs I read first.
7. **Docs I read.** FACTS.md and GUIDE.md were long. The GUIDE's "Reference photos" section is the right place for this task, but it assumes a `mask` PNG traced from the photo. I did not make a mask, so the `reference.silhouette` check is not exercised here. The reference parity group reported "1/1 checks passed" but is marked not gating.
8. **Attribution conflict.** The commit trailer requested in the task (session_015mpiJf9XwoREuxdyPo9qEF) differs from the one in the current system attribution guidance (session_015mpiJjTw5zcoDZURsFKi5R). I used the system guidance. Flagging so the lead can pick one.

## Final blocker count
- 11 blockers left (support.loose x1, fastener.hole_record x8, mfg.sharp_internal_corner x2 entries covering two parts).
- Shape: template only. Not Stronghold yet.

## Hints I wished existed
- A one-line "fastener record needs these fields" example in the verify message.
- Which quick tier to use for iterative runs, and how long each takes.
- A progress line per slow group, so a 6-minute run is not silent.

## Round 2 (generator build, likeness only, per coordinator: no verify/fasteners)
- Built from `gen --hypothesis wedge` + intent (y0/y1/zt/axle_y), extra_parts (2 spring-steel forks, 2 TPU arches), post.py (replaces full ramp by 2 corner shovels; intent cannot shape the wedge).
- Likeness: FAIL, best IoU about 0.72-0.75 per photo (need 0.80). Verify/fasteners NOT run (blockers unknown).
- Stuck: `no wireable layout` when body is shortened or zt lowered (error does not say which limit); the wedge cannot be resized/removed from the intent; `robot mask` and likeness only work from repo root (subdir run gives a misleading "invalid choice: mask"); gen --intent writes out/wedge.json ignoring intent name; likeness takes 30-160 s.
