# Robobuild123d: design an antweight combat robot (SKILL)

You iterate on a JSON design file until the verifier passes it. `robot` below means `python3 -m robot`.
Units are mm and degrees; X lateral (left +x), Y forward, Z up; wheel centres at z = 0.

## Workflow (the whole skill is this loop)

1. Start from a template, never a blank file: `robot template wedge_2wd > spec.json` (templates: revron, revron_ant, wedge_2wd).
2. `robot verify spec.json --json report.json` - exit 0 means the design gate passed.
3. Read the failures with `robot llm-report report.json` (compact, blockers first, each with `fixes`).
   Re-run it with `--prev last_report.json` to see the delta: `fixed` / `new` / `still` finding ids, and the mass move.
4. Fix the ROOT CAUSE the finding names (wrong part, wrong size, wrong place) - do not nudge numbers until a check goes quiet.
5. Repeat until `blockers` is 0. Warnings are acceptable; blockers never are.
6. `robot render spec.json iso out.png` to look at it, `robot export spec.json <slug> <dir>` when done.

## Rules profiles (E4)

The `profile` key of the spec selects a rules profile (`robot profiles` lists them):
- `aws2025` - Antweight World Series 2025 ruleset (version 05.06.25): the competition profile. 150 g roller / 225 g non-roller, 150 mm floor-square footprint, weapon restraint, tool-free switch. This file is the canonical source the Profile() defaults mirror (test_profiles.py fails if they drift).
- `dev` - Early-iteration profile: the AWS legality numbers stay strict (mass, footprint, tip speed, locking bar, switch) but the engineering margins relax so the first verify of a rough design is not buried in wall/clearance noise. Switch to aws2025 before trusting a pass.
- `strict` - Tournament-hard profile: same AWS legality numbers, tighter engineering margins (walls, clearances, engagement, runtime) so a pass here survives tolerance stack, wear and a hard weekend of fights.

## Machine interfaces

- `robot llm-report report.json [--prev old.json]` - the compact report for your context window.
- `robot explain <finding-id>` - what one finding id means and how to act on it.
- `robot mcp` - stdio JSON-RPC server exposing the same thing as tools: schema, catalog, validate, explain, diff, guide.
- Design patch language (iterate without resending the file): ops `set` / `nudge` / `unset` on dotted paths;
  `robot design_io.patch.apply(design, patch)` returns the new design plus errors with the allowed sibling paths.
- One error envelope everywhere: `{"ok": false, "errors": [{"path", "message", "expected", "actual"}]}`.

## Finding-id discipline

Findings are stable machine ids (`group.something`), never prose. Fix by id, verify by id - the delta section is keyed on ids.
What each id prefix means (from `robot explain`):
- `integrity.` The part is not one closed solid (bad boolean, zero-thickness wall, or an import gone wrong). Rebuild the last feature before the failure.
- `mass.` The 150 g limit. mass.over is total mass, mass.may_be_over is the worst-case tolerance stack, mass.unknown a part with no mass source. Cut grams from the thickest printed part or the weapon disc.
- `legal.` AWS 2025 rules: 150 mm floor square footprint, 150 g, weapon restraint, radio. These are competition disqualifiers, never waive them.
- `fit.` A bought-in part does not fit the pocket/bore made for it (diameter band, depth, or clearance). Widen the pocket or pick a different catalogue part.
- `interference.` Two solids overlap that must not (static overlap, spinning part vs static, swept volume, wheel rub). Move parts apart or cut a pocket in the printed part.
- `wiring.` The wire router could not find a legal channel (pinched, too tight, or crossing the weapon sweep). Open a channel or reroute.
- `wire.` Wire-level review: clearance to rotating parts, or a render inconsistency of the route.
- `assembly.` The greedy take-apart search could not remove a part (assembly.blocked): something traps it. Open a slot, change the order, or split the part.
- `disasm.` Disassembly: a part is unreachable for service, the order is circular, or a belt must stretch too far to fit.
- `connections.` A declared connection (screw, glue, press) does not hold geometrically: missing mate, wrong method for the parts, or nothing to bite.
- `fastener.` Screw problems: too long/short, no thread to bite, head does not seat, no driver access, or the hole record is missing.
- `fasteners.` Screw set review: lengths, threads, access across the whole fastener list.
- `fastener_seat.` Screw head/thread vs the hole geometry (counterbore depth, seat angle, shank clearance).
- `fastener_record.` A hole was made without the fastener record the build needs (size, depth, method).
- `drive_recess.` The motor or screw drive (hex/phillips) has no recess to sit in.
- `contain.` A vulnerable part (battery, ESC, receiver) is exposed to hits or ground. Shield it or move it inboard.
- `joints.` Screwed-joint engineering defaults: boss wall, edge distance, thread engagement, nut traps.
- `power.` Power budget: tip speed, stored energy, battery peak current, runtime. Usually means the pack is too small or the weapon too heavy.
- `physics.` Closed-form weapon/drive/power physics (spin-up time, bite, push force). Cross-check of power.* with real motor constants.
- `drive.` Drivetrain performance: push force, top speed, slip current. Traction-limited or motor-limited.
- `combat.` Combat design rules (ground game): wedge angle, ground clearance, invertibility, self-righting.
- `combat_ground.` Ground-game geometry: the robot cannot get its weapon or wedge onto a standard opponent.
- `threat.` Adversarial failure modes (CF-*): the design loses to a class of attack it declared it must survive.
- `electrical.` Electrical rules: motor voltage, connector rating, cell consistency, ESC limits.
- `mfg.` Manufacturability of the declared process: min walls, hole sizes, tolerances the process cannot hold.
- `dfm.` Per-process manufacturability drafts (bed contact, tall thin walls, horizontal holes, sheet tabs, undeclared fits).
- `printability.` FDM limits: minimum holes, overhangs, bridges, first layer. Chamfer, reorient, or add supports.
- `print.` Print orientation declared vs what the geometry implies.
- `print_orient.` A printed part did not declare (or contradicts) its print orientation.
- `process.` Process steps (print, cut, turn) that the geometry contradicts.
- `material.` Material placement: brittle material in an impact zone, wrong grain, or a part of the wrong stock.
- `shape.` Shape-level rules: wall thickness, thin fins, closed cavities.
- `wall.` Wall below the process minimum. Thicken or declare a waiver with a reason.
- `thickness.` Wall below the process minimum. Thicken or declare a waiver with a reason.
- `geom.` Geometry sanity: tiny edges, sliver faces, near-coplanar steps, near-miss holes, off-axis faces, open shells, zero thickness.
- `waiver.` Waiver audit: every opt-out needs a reason and an expiry; no blanket waivers; the waiver budget caps how many one design may carry.
- `waiver_audit.` Same audit, group entry point: reason, expiry, budget, blanket and duplicate-reason rules.
- `practice.` Best-CAD-practice gates with no reference (naming, fully constrained sketches, stray geometry).
- `spinner.` Weapon spinner checks: balance, bearings, shaft, retention at speed.
- `kinematics.` Motion checks: weapon sweep, drive kinematics, declared rotation.
- `retention.` A rotating part is not held in both axial directions by hardware.
- `tension.` Belt/o-ring tensioner travel and range.
- `belt_wrap.` Belt wrap angle on a pulley is too small to transmit torque.
- `ground.` Ground interaction: clearance, approach angle, wheel contact.
- `strength.` Static strength: weapon shaft, bearings, uprights, pull-out. Usually fix by thickening or shortening a lever.
- `dynamics.` Dynamic behaviour: tip angles, invertibility, gyroscopic effects, hit reaction.
- `support.` The part is not supported in one of the 6 orientations (gravity on a loose part).
- `sharp_corner.` Sharp internal corner the process cannot resolve; add a radius or opt out with a reason.
- `coverage.` A declared claim (spec claims[]) has no check covering it.
- `cots.` Bought-in part usage: belt wrap, motor volume, port mismatches against the catalogue.
- `bom.` Bill of materials: lock part, O-ring stock, wire cut length, or a reference BOM difference.
- `targets.` The spec's own declared target dimensions do not match what was built.
- `reference.` Comparison with the original designer's data (photos, meshes, dumps). Never gating for a new design.
- `reference_ratios.` Proportions measured on reference photos (panel splits, wheelbase ratio) differ from the original.
- `reference_cad.` Per-part diff vs the reference CAD meshes (volume, bbox, position).
- `ref_map.` A built part has no entry in the reference parts index (or vice versa).
- `cots_fidelity.` A bought-in part was modelled differently from its catalogue/STEP data.
- `wire_review.` Wire-route review: clearance to rotating parts or a missing render of the route.
- `param.` Param lint: raw literals where a setting should be, or a dimension-count mismatch vs the reference.
- `intent.` A feature does not do what its design intent claims (probes of the declared intent).
- `plausibility.` Density/mass plausibility vs the real robot class.
- `archetype.` Archetype rules for the declared weapon/drive class.
- `architecture.` Architecture: pods enclose what they must, mounts hold their parts.
- `internal.` Internal layout: parts inside the shell collide or do not fit.
- `visual.` Visual parity with the reference mesh (silhouette/depth/fillet).
- `sldprt_dump.` Comparison with the SolidWorks part dumps of the original design.
- `asm_dump.` Comparison with the SolidWorks assembly dump (order, mates, counts).
- `robust.` Robustness sweep: a param or COTS swap variant failed to build or verify.
- `harness.` Planned wiring harness (robot/wiring): nets, connectors, service loops.
- `thermal.` Thermal/voltage-sag budget: the pack's voltage under peak current (nominal minus I x internal resistance) must stay above 3.3 V per cell or the receiver/ESC browns out mid-fight. Bigger pack (more mAh / lower resistance) or less peak current.
- `impact.` Hit reaction: gyroscopic wheel-lift when turning with a spun-up weapon (turn rate above the lift threshold rolls the robot), hop when a vertical spinner lands a hit, and yaw spin-out from a horizontal spinner. Slow the turn rate, lower the weapon speed, or widen the track.
- `requirements.` A requirement the user declared (speed, force, energy, budget) is not met by the design.
- `rest.` Dead pose: with the power cut the weapon coasts to an unknowable rest angle; if some rotation of the weapon reaches the floor the dead robot props itself on its own blade. Raise the weapon or its spin axis.
- `clearance.` Clearance at rest: tyres squash under the robot's weight and a loaded wedge bends down, so a belly that cleared on the bench can scrape and a wedge tip can dig in. Raise the chassis, use firmer/bigger wheels, or stiffen the wedge.
- `service.` Between-fight service: the battery, weapon and wheels must come out along at least one straight line without removing other parts, or a swap costs the match. Give the part an open hatch or slot.
- `engagement.` Fastener engagement: a screw must be longer than the parts it clamps and its thread must bite the host. Use a longer screw, shorten the stack, or thread into a boss with enough material.
- `tool_access.` Tool access: every screw needs its driver and every nut needs its wrench, along a clear straight line. Open a pocket, use a retained nut, or rework the joint so only the screw turns.
- `wire_care.` Wire care: the harness must survive vibration and hits, not just fit. Ease tight bends, line or deburr hole edges (grommet), and anchor a relief via near vibrating ends.
- `rf.` RF placement: the receiver must sit away from motor/ESC switching noise (2.4 GHz swamps at close range) and its antenna must exit the top face without conductive material over it. Move the receiver to the far corner, cut a window in metal/carbon above it, or stand the antenna out.
- `traction.` Traction patch: the centre of mass must project inside the polygon of the driven wheels' floor contacts, with margin, or the first push unloads the wheels and the robot pivots. Move mass over the driven wheels or widen the stance.
- `builder.` Builder profile: the design does not fit the declared builder's bench - printer bed, shelf materials, processes, tools, skill or budget. Split parts, switch to stocked materials, add the tool, or raise the budget.
- `validity.` The spec itself is invalid (unknown part, bad placement) - fix the spec before reading other findings.

## Check groups (design gate)

Later groups read the metrics of earlier ones; run order is fixed. `--tier inner` is the cheap edit loop, `full` is the merge gate.
| group | tier |
|---|---|
| `integrity` | inner | - one closed solid, no volume collapse (first and cheap)
| `wiring` | full | - voxel router, A* per wire
| `mass` | inner |
| `interference` | full | - inscribed depth, joint sweeps
| `connections` | inner |
| `internal` | full |
| `ground` | full |
| `legal` | inner |
| `fasteners` | inner |
| `power` | inner |
| `mfg` | full |
| `spinner` | full |
| `kinematics` | full |
| `tension` | inner |
| `targets` | inner | - the spec's own declared target dimensions
| `shape` | inner |
| `dynamics` | inner |
| `strength` | inner |
| `printability` | inner |
| `process` | inner |
| `archetype` | full |
| `architecture` | full |
| `electrical` | inner |
| `combat` | inner |
| `physics` | inner | - closed-form weapon/drive/power physics (robot/checks/physics), UNTESTED
| `thermal` | inner | - thermal.*: pack sag / brownout at peak current (robot/checks/thermal)
| `impact` | inner | - impact.*: gyro wheel-lift, hop, spin-out yaw from the weapon metrics
| `rest` | inner | - rest.*: dead-pose weapon sweep vs the floor (robot/checks/rest)
| `clearance` | inner | - clearance.*: ground clearance at rest with tyre squash and wedge deflection
| `service` | inner | - service.*: straight-line extraction of battery / weapon / wheels between fights
| `assembly` | full | - greedy take-apart search
| `joints` | full |
| `material` | full |
| `plausibility` | inner |
| `intent` | full | - functional design-intent probes
| `cots` | inner |
| `fit` | inner |
| `contain` | full |
| `disasm` | full |
| `coverage` | full |
| `bom` | inner | - lock part, O-ring stock, wire cut, switch; its reference.* findings are parity
| `support` | full |
| `threat` | full |
| `fastener_seat` | full |
| `cots_fidelity` | full | - vs catalog feature tables; cots.motor_volume (vs STEP) is parity
| `wire_review` | inner |
| `fastener_record` | inner |
| `drive_recess` | inner |
| `belt_wrap` | inner |
| `print_orient` | full |
| `retention` | inner |
| `sharp_corner` | full | - reads the reference only to excuse corners it also has
| `practice` | full | - best-CAD-practice gates with NO reference
| `param` | full | - raw-literal lint; param.budget (vs dump dimension count) is parity
| `waiver_audit` | inner | - waiver.*: every opt-out has a reason and an expiry, none blanket, budget
| `geom` | inner | - geom.*: tiny edges, sliver faces, near-miss steps / holes, off-axis faces
| `dfm` | inner | - dfm.*: per-process manufacturability not covered by printability / process
| `harness` | full | - robot/wiring: planned harness (opt-in: spec harness.enabled)
| `requirements` | inner | - requirements.*: the spec's declared requirements vs measured metrics
| `engagement` | inner | - engagement.*: screw length vs the clamped stack, engagement % of d (G3)
| `tool_access` | inner | - tool_access.*: driver path for undeclared-tool screws, wrench clearance at nuts (G4)
| `wire_care` | inner | - wire_care.*: wire chafe at hole edges, via bend radius, connector strain relief (G5)
| `rf` | inner | - rf.*: receiver away from motor/ESC noise, antenna exit path (G6)
| `traction` | inner | - traction.*: COM over the drive contact patch, push balance (G9)
| `builder` | inner | - builder.*: design vs the builder's printer bed, shelf materials, tools, budget, skill (E3)
| `robust` | nightly | - one-at-a-time param / variant / COTS-swap sweep

## Guide sections

The full guide is `robot guide` (or `robot guide "<section>"` for one). Sections:
`Commands`, `Spec layout (all keys optional except parts)`, `Rules checked (AWS 2025)`, `Common mistakes the verifier catches`, `Tips`, `Rules the tool enforces that are easy to miss`, `Process (how each made part is manufactured)`, `Reference photos (does it look like the real robot?)`, `Engineering defaults (screwed joints; checked by `joints.*`)`, `Material placement (checked by `material.*`)`, `Combat design rules (ground game; checked by `combat.R*`)`, `Reference proportions and reference CAD (checked by `reference.feature_ratio`, `reference_cad.*`, `plausibility.density`)`, `Design rules learned from reference matching (Revron/RVRN audit, 2026-10)`, `Modelling a part from a reference STEP (lessons from review/code/MISSES.md, 2026-10)`, `Sharp internal corners are opt-OUT (`mfg.sharp_internal_corner`, robot/checks/sharp_corner.py)`, `Design intent: check what a feature is FOR (`intent.*`, `intent` list in the spec)`, `Bought-in sizes, fit, containment, disassembly and coverage (`cots.*`, `fit.*`, `contain.*`, `disasm.*`, `coverage.*`)`, `Template engine (`robot gen`)`, `Reference BOM and build-guide details (`bom` group)`, `Combat failure modes (checked by `threat.CF-*`, `threat.CFX-*`)`, `Design-review gates (groups `ref_map`, `cots_fidelity`, `wire_review`, `fastener_record`, `belt_wrap`, `print_orient`)`, `Support in every orientation (`support.loose`)`, `CAD authoring tools (`robot/cad`): remove recurring modelling mistakes`, `Parametric build code (`param.*`, group `param`, opt out with `review.param.enabled: false`)`, `Geometry sanity (`geom.*`, group `geom`, per check opt out with `geom_ok`)`, `Waiver audit (`waiver.*`, group `waiver_audit`)`, `Manufacturability drafts (`dfm.*`, group `dfm`, per check opt out with `dfm_ok`)`, `Thermal and brownout (`thermal.*`, group `thermal`)`, `Hit reaction and gyroscopic wheel-lift (`impact.*`, group `impact`)`, `Dead pose (`rest.*`, group `rest`)`, `Clearance at rest (`clearance.*`, group `clearance`)`, `Between-fight service (`service.*`, group `service`)`, `Named fits (`robot/fits.py`)`, `Slice-based mass & print-time estimate (`robot/slice_est.py`)`, `DXF sheet/turned-part order pack (`robot/dxf_order.py`)`, `Requirements block (`requirements.*`, group `requirements`)`, `Fastener engagement vs the clamped stack (`engagement.*`, group `engagement`)`, `Tool access for every fastener (`tool_access.*`, group `tool_access`)`, `Wire chafe, bend radius, strain relief (`wire_care.*`, group `wire_care`)`, `RF placement (`rf.*`, group `rf`)`, `COM over the drive contact patch (`traction.*`, group `traction`)`, `Builder profile (`builder.*`, group `builder`)`, `Fixing collisions without hand maths (jiggle)`

## Examples (in this pack, `examples/`)

- `examples/wedge_2wd.spec.json` - a working starter design (the template itself).
- `examples/compact_report.json` - what `robot llm-report` gives you for a failing design: blockers with fixes first.
- `examples/patch_roundtrip.json` - a design, a patch, and the result of applying it.

## Regenerate this pack

`robot llm-pack <dir>` writes this pack from the live verifier sources; the drift test
(robot/tests/test_llm_pack.py) fails if the checked-in copy is stale.
