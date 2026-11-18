# Verty Little Secret: rough build struggles (Haiku run)

## What was built
- Started from `robot template wedge_2wd` (2WD wedge, nylon chassis, two N10 motors, wedge front). Only renamed it
  "Verty Little Secret (rough)" and filled hole records. Did NOT yet model the photos' features (see below).
- Photos show: two separated pods with a central BE1806 outrunner motor and curved claw/blade pieces between them,
  gear-toothed wheels at the outer ends, tapered forked skids at the front and rear, and a top switch. The template has
  none of the central motor/claw weapon, and no pod split. Shape/size/weapon were NOT moved toward the photos.

## Setup problems
- `git merge FETCH_HEAD` from `origin dev` failed: "refusing to merge unrelated histories" (shallow clones). Needed
  `--allow-unrelated-histories`. That then gave add/add conflicts in robot/cli.py, robot/render.py, robot/GUIDE.md,
  robot/checks/support.py, robot/checks/fastener_record.py, robot/templates/wedge_2wd.json. Resolved by taking the dev
  side for all of them (guess: dev is the toolchain of record). Merge commit 9063991 on the ref branch.
- First `pip install -e '.[robot]'` failed with an OSError uninstalling the old editable build123d .pth. Re-running it
  worked. Hint for the docs: pip uninstall first, or retry.

## Verify / tooling
- `verify --tier inner --llm` was clean on the raw template (0 blockers, ~10 s). Good.
- `fasteners --fill` wrote 8 hole records but only for the grip/head/clearance fields. It did NOT write
  `insert_d` / `insert_len` for `into: insert` holes, and it wrote `cbore_depth: 0.0` for counterbored screws.
- Full tier crashed the `fastener_seat` check: `TypeError: unsupported operand type(s) for +: 'float' and 'NoneType'`.
  The message only says "Report this". Traceback location: robot/cad/seat.py line ~112 (`g0 + il`), where `il` came
  from `insert_len`. The fix that worked was to fill `insert_d` / `insert_len` from `robot.cad.fastener_catalog.insert(2.0)`
  = (3.2, 4.0). The fill tool should do this itself (holes.py line ~150 computes it).
- After that, full verify reported 14 root causes (not fixed, see below):
  - 8 x `fastener_seat.insert_bore` (heat-set bore 75-100% open or wall 50% present). Likely the insert modelled as
    a bare hole in the spec, or the 3.2 mm bore not matching the insert part.
  - 4 x `fastener_seat.cbore_depth` (floor 2.20 mm below the surface, recorded 0.00). Fill writes cbore_depth 0.0 for
    counterbored screws, which is the wrong value for the seat check.
  - `mfg.sharp_internal_corner` on both chassis halves, skipped per instructions for rough builds.
- Full verify takes about 4 min; `ROBOT_JOBS=1` was not needed.

## Guesses and gaps
- Cannot tell from the template or docs how to model the central outrunner/claw weapon. No spinner/claw template exists
  in `robot templates` (only revron, revron_ant, wedge_2wd). A new template or a weapon-kind example would help.
- No mask was made for `reference:` (needs a traced silhouette PNG), so the silhouette check is not run.
- `template` output has no `reference` block, and `field reference` examples were not read.

## Final blocker count
- Full tier: 14 root causes (12 printed by verify: 8 fastener_seat.insert_bore, 4 fastener_seat.cbore_depth, plus
  2 sharp-corner and/or insert-related lines not individually shown). Mass 114.5 / 150 g.
- Shape, size and weapon do NOT match the photos. This is a template with fastener fixes only.
