# Antweight robot builder guide

You design a 150 g UK antweight combat robot as a JSON file (`spec.json`). The verifier (`robot verify`) measures the solid model
and fails anything unbuildable. Work in a loop: edit the spec, run `python3 -m robot verify spec.json`, read each failure (it names the parts,
a position and a fix), repeat until there are no blockers. Then `robot render` and `robot export`.
Every solid is an exact build123d (OpenCascade) B-rep; the checks run on its tessellation and the export writes real STEP.
`robot` below means `python3 -m robot`.

Start from a working design: `robot template wedge_2wd > spec.json` (run `robot templates` to list). Change it, do not guess the
format from scratch. Units are mm and degrees. X is lateral (left +x), Y is forward, Z is up. Wheel centres are at z = 0 and the floor
is the lowest wheel point.

## Commands
- `robot guide` this text.  `robot catalog` bought parts with sizes and ports.  `robot materials` materials and densities.
- `robot template <name>` prints a spec.  `robot verify spec.json [--full]` checks it (default shows failures only).
- `--fast` coarse tessellation for quick iteration (verdicts near limits may move); `--quick` skips the slow sweeps (wiring, assembly);
  `--json report.json` also writes the report.
- `robot render spec.json <view> out.png [--markers]` views: iso, iso_back, top, bottom, front, back, side, exploded, section_z,
  section_x. `--markers` draws numbered red rings on every failure that has a position (the numbers are printed).
- `robot export spec.json <slug> <dir>` writes `<dir>/<slug>/`: spec.json, report.json, REPORT.md (with NOT CHECKED), README.md
  (iso render on top), renders/, stl/ per part, step/ per part plus step/assembly.step (exact B-rep, start pose).

## Spec layout (all keys optional except parts)
`name, profile ("aws2025"), robot_type (wedge|horizontal_spinner|vertical_spinner|drum|lifter|flipper), locomotion (roller),
parts[], fasteners[], wires[], connections[], allow_overlap[], electronics{failsafe, weapon_remote_disable, radio, cells}, claims[]`.

### parts[]
`{id, kind, catalog?, shape?, material?, process?, at:[x,y,z], rot:[rx,ry,rz], retained?, fused_with?, ...}`
- `kind`: structure, armor, wedge, motor, weapon_motor, wheel, battery, esc, receiver, servo, switch, weapon, locking_bar, insert, nut,
  bearing, plate, fork, tyre, pulley, belt, shaft, pin, spring, other. The first `structure` part is the chassis root.
- Bought parts use `catalog` (id from `robot catalog`): size, mass and ports come from there, give only `at` and `rot`.
- Made parts need `shape`, `material` (`robot materials`) and `process` (fdm, resin, cnc, laser, waterjet, cast, bought).
  Printed parts get mass = volume x density x `solid_fraction` (default 0.85 for printed parts, 1.0 otherwise; shells with 20-45% infill need it set explicitly; per-part mass shows as `part_mass_g.<id>` in metrics).
  Give `slicer_mass_g` or `scale_mass_g` when you have a real number; they narrow the mass uncertainty.
- `retained`: how a part with no screw stays put (`tape`, `adhesive`, `press_fit`, `velcro`). Otherwise it must be captive in a pocket.
- `fused_with`: printed as one piece with that part (same material, both printed). A wedge in PETG on a nylon shell is NOT fused.
- Spinners: `weapon: {kind, motor, cells, reduction, spin_axis (3-element local axis array such as [0,0,1], not a letter), locking_bar}` on the weapon part; the weapon motor,
  the weapon and a `locking_bar` part must exist. Tip speed is limited to 600 mph.
- Moving parts: `parent` plus `joint: {kind (revolute|prismatic), axis, pivot, min, max, default}`; the verifier sweeps it. `pivot` and `axis` are in the parent's declared frame: the parent's `at`/`rot` composed with its own parents (and their joints), the same frame the child's `at`/`rot` uses, never the catalog model's internal origin. Under a rotated parent (e.g. a servo at `rot: [90, 0, 90]`) write them in that rotated frame; with no `parent` they are world coordinates.

### shape (build123d solids)
JSON with `"type"`; everything is centred on its own origin, use `place` to move it inside a shape:
- `box {size:[x,y,z]}`, `cylinder {radius,height}` (axis z), `sphere {radius}`.
- `prism {points:[[x,y]..],height}`: straight-edged outline extruded along z (centred). Must not self-intersect.
- `spline_prism {points:[[x,y]..],height}`: the points are threaded by a closed smooth B-spline, then extruded. Use it for
  rounded shells and organic outlines (8 to 30 points is plenty).
- `loft {sections:[{points:[[x,y]..], z, spline (default true)}], ruled (default false)}`: skin through 2+ planar outlines at
  increasing z. Give every section the same number of points in the same winding. Good for tapered wedges and domes.
- `revolve {profile:[[r,z]..], angle (default 360)}`: profile in the r-z half plane (r >= 0) turned about z (wheels, hubs, discs).
- `tube {points:[[x,y,z]..],radius}`: swept round bar through the points.
- `union {items}`, `intersect {items}`, `subtract {base, cut:[..]}`, `place {shape, at, rot}`, `offset {shape, d}` (d in +-50 mm).
- `fillet {shape, radius}`, `chamfer {shape, length}`: round or bevel every edge of the child (keep radius below half the thinnest
  wall or the kernel fails, which becomes a `geometry failed` blocker).
- `mirror {shape, axis:"x"|"y"|"z"}`: reflect across the plane normal to that axis.
- `model {file, params}` (or `"model": "file.py", "params": {...}` on the part): a Python file next to the spec defining
  `build(**params)` that returns a build123d solid (or a BuildPart). Use it when JSON gets awkward; it is cached by file content.
Build pockets by subtracting boxes from the housing. A part at `at` is that shape moved to that position.

### fasteners[]
`{id, designation "M2x16", at (underside of the head), dir (direction the shank points), through [part ids with clearance holes],
threads_into (insert, nut or structure part id), tool "hex1.5", removable, head "socket"}`. Heat-set inserts are parts of kind `insert`
(catalog `heatset_m2`) in a bore that is OPEN to a face so they can be pushed in. The verifier slides every part out along a straight
path; closed cavities, shafts through solid walls and screws under overhangs fail.

### wires[]
`{id, from:"part.port", to:"part.port", awg, kind (power|motor|signal), slack_mm}`. Ports come from the catalog or from `ports`
on the part. Wires are routed as tubes of real thickness through free space inside the chassis: you must cut channels (about 2.5 mm
wide, 3+ mm tall) between pockets.

### connections[]
Every part must be attached to the chassis. Screws, a shared print (`fused_with`), a pocket that captures it on all sides, a joint or
a `connections` entry `{a, b, method, reason}` counts. Methods: screw, shaft, pin, press_fit (add `interference_mm` 0.05 to 0.4),
glue, tape, snap, interlock, velcro, none (loose on purpose). The reason must be real engineering (30+ characters, say what load it carries).
Glue and tape are rejected on wedges, weapons, armour, forks and on HDPE, PP, nylon (unless `mechanical_key`). Bolt impact parts.

### claims[]
`{id, text, metric, op, value}` e.g. `{"id":"c_mass","text":"150 g or less","metric":"mass_total_g","op":"<=","value":150}`.
Metrics include mass_total_g, mass_hi_g, footprint_mm. An unknown metric is a blocker.

## Rules checked (AWS 2025)
150 g (roller), fits a 150 mm square at any height, tool-free marked power switch, failsafe, weapon remote disable, locking bar on spinners,
sharp edges covered, tip speed <= 600 mph, no entanglement/flame/etc. Mass is reported as a range: the heaviest realistic value must not
exceed the limit by a lot, and the lightest must be under it.

## Common mistakes the verifier catches
Wedge not attached; glue on nylon/HDPE; parts floating next to each other; motor shaft through a closed wall; inserts in closed cavities;
screw heads under overhangs; wires with no channel; wheel not touching the floor; wedge tip too high or low; centre of mass outside the
wheels; parts too thin to print (min wall about 0.9 mm FDM); brittle material for weapons; no locking bar; switch can be knocked by the
robot's own motion or when inverted.

## Tips
- Keep a 0.2 to 0.5 mm gap around pockets (printing tolerance) but snug enough to capture parts.
- Moving parts need at least 1 mm of running clearance. Wheels need walls cut away to slide on from outside.
- Fix blockers first, then warnings. Re-run verify after every change; it takes a few seconds.

## Rules the tool enforces that are easy to miss
- Wires only route through `structure` parts. A port outside that volume gives "got within N mm" errors; make the holding part `structure`.
- Catalog part ports and axes: `robot catalog <id>` lists port names; the weapon motor's `phases` port is on its local +z face and its shaft runs along local z.
- Spinners: the disc must sit on a `shaft` part running through structure on BOTH sides (`spinner.bearing`); declaring `supported_both_ends` is checked, not trusted.
- `robot verify` prints `check set revision N`; compare it with `CHECKS_REVISION` in robot/checks/__init__.py.
- A check group that is missing or crashes is never a silent pass: it shows as `checks.missing` (warning) or `checks.crashed` (blocker) and in NOT CHECKED.
- Geometry is cached under `~/.cache/robot` (override with `ROBOT_CACHE`); delete it if a model file's imports changed.
- The report ends with NOT CHECKED: those items were not judged, a pass says nothing about them.

## Process (how each made part is manufactured)
Every non-catalog part declares `process`; the `process` group checks the exact B-rep against it.
- `laser` / `waterjet` / `sheet_cut` / `wire_edm`: one 2D profile extruded to one thickness (two parallel faces, every
  other face perpendicular). Thickness must be a stock gauge for the material (`catalog.SHEET_STOCK_MM`), holes
  dia >= t (steel, spring steel, Hardox, Ti) or 0.5 t, internal corner radius >= kerf (laser 0.1, waterjet 0.5 mm; a
  sharp internal corner fails), web between cut features >= t. Pockets, chamfers and countersinks need
  `secondary_ops: ["pocket"|"chamfer"|"countersink"]`. Spinner teeth are part of the outline, never a block on top.
- `sheet_bent`: planar + cylindrical faces only, bends as cylindrical folds with inside radius >= k t (k = 1, spring
  steel 2, Ti 2.5, Hardox 3), flange >= 3 t + r, holes >= 2 t from a bend. Sharp folds fail.
- `turned` / `lathe`: surfaces of revolution about one axis; flats, keyways, cross holes and off-axis drillings need
  `secondary_ops: ["flat"|"keyway"|"cross_hole"|"drilled"]`.
- `milled` / `cnc`: internal corner radius >= 1 mm, no sharp internal corner a tool cannot reach along a face normal,
  every face reachable along +-X/Y/Z (no undercuts).
- `fdm` / `resin`: geometry is judged by `mfg` and `printability`; `print_orientation` (+x/-x/+y/-y/+z/-z, the
  part-frame axis pointing up off the bed) is required. Printed parts carrying the weapon axle must be printed with the
  spin axis as build direction (`mfg.layer_load`). A printed spinner weapon without metal teeth is a blocker.
- `bought` / `cots` with free geometry: must match a stock rod diameter, a bearing named in `label`/`stock`
  (684, MR84, ...) or an O-ring belt; otherwise use a catalog part (`mfg.stock`).
- `molded` / `cast`: accepted, geometry listed under NOT CHECKED.
Missing `process` is `process.undeclared` (blocker). `export` writes `dxf/<part>.dxf` for every cut part; a part that
cannot be flattened (including bent parts, unfold not yet implemented) is an `mfg.export` blocker.

## Reference photos (does it look like the real robot?)

Optional `reference: [{image, view, mask, scale_hint?, dir?, approximate?}]`. `view` is `side` (looking along +x, front on
the LEFT), `front`, `top` (front left), `iso` (front-left from above) or `iso_back`; `dir` overrides the camera direction.
`mask` is a binary PNG traced from the photo (white = robot, holes filled), path relative to the spec; e.g.
`robots/revron/reference/side_mask.png` from `photos/ref3.png`. The model's orthographic silhouette and the mask are cropped to
their bounding boxes, scaled to the same length and aligned at ground line + front tip, then compared: IoU overall and per
third (front/middle/rear) plus outline Hausdorff (mm). `reference.silhouette`: IoU < 0.80 blocker, 0.80-0.88 warning
(`approximate: true`, for perspective renders, caps at warning). The message names the worst third; the overlay PNG
(model red, photo blue) goes to `$ROBOT_REFERENCE_OUT` (default `<tmp>/robot_reference/`, path in metrics `reference`) and
`export` writes `renders/compare_<view>.png`, linked from README. A missing/unreadable mask is `reference.unusable` + NOT CHECKED.
Typical catches: fork/disc on the wrong end (front third fails), boxy pods (rear/middle), wrong height/length ratio.

## Engineering defaults (screwed joints; checked by `joints.*`)
Decide each joint like a mechanical engineer before placing screws. Off-default choices need `"reason"` on the fastener.
- **Screw direction = how the two parts meet.** Find the face where part A sits on part B; screws run along that face's
  normal, head on the part being attached, insert/nut in the base. Example: a side pod meeting the tub on its side wall is
  bolted sideways through that wall, not down through small tabs. >30 deg off the mating face normal is a blocker
  (`joint.axis_vs_interface`) unless `reason` (e.g. "shear pin"). Screws parallel to the contact faces clamp nothing
  (`joint.parallel_interface`); the screw must pass through the faces it clamps (`joint.through_contact`).
- **Top screws need a reason.** Drive screws along the direction the part slides on during assembly (`joint.assembly_dir`)
  and keep the driver line clear without removing other parts (`joint.service_access`); a removable cover is fine.
- **Locate, then clamp.** Add a lip, step, spigot or dowel so parts register; screws are not locators (`joint.no_locator`).
- **Pattern:** >= 2 screws per joint unless keyed (`joint.single_fastener`), spread >= 3d (`joint.bolt_spread`),
  centred on the interface (`joint.bolt_symmetry`).
- **Stack:** clearance hole >= d+0.2 in every head-side part (`joint.clearance_hole`); counterbore >= head dia+0.4 and
  head height deep (`joint.counterbore`); edge/boss: insert boss OD >= 2x insert OD (`joint.insert_boss`), insert length
  >= 1.5d (`joint.insert_length`); tapped plastic >= 2d engagement (`joint.plastic_engagement`) and >= 3d boss
  (`joint.thin_wall`).
- **Printed parts:** removable joints use heat-set inserts, not self-tapping (`joint.selftap_removable`); never self-tap
  along the print Z axis (`joint.layer_tension`); spread head load on plastic with a washer / flange head (`"washer": true`,
  `joint.head_bearing`).
- **Armour and covers are bolted** (`connection.cover_fasteners`, blocker): every armour / cover / lid / panel part, and
  every part declared `retained: screws` (e.g. a switch with M2 holes in its housing), needs >= 2 real fasteners through
  or into it. A snap, press fit or tape alone peels off on the first hit.
- **Nuts** sit in hex traps (captive) or are replaced by inserts (`joint.loose_nut`).
- **Outside surfaces:** no proud heads on armour or exterior (`joint.head_proud`), never on the ground plane
  (`joint.head_ground`): counterbore flush or countersink.
- **Kit:** <= 3 thread sizes (`joint.screw_sizes`), <= 5 distinct screws (`joint.screw_variety`), stock ISO lengths
  (`joint.standard_length`).

## Material placement (checked by `material.*`)
- **Shape material to loads in all axes; no chunky bosses.** A screw into a part (even sideways into the tub) needs only
  its boss: insert boss OD 2x insert OD, tapped plastic 3d, clearance hole d/2 + one wall. The ring 2 walls outside it
  must not be solid for more than 3 walls (6 mm) along the screw, nor > 35% thicker than 2 walls (`material.boss_excess`).
- Printed parts are shells at the design wall (2 mm, `"design_wall_mm"` to override): <= 10% of volume deeper than 2 walls
  (`material.solid_core`), p99 wall away from fasteners <= 3 walls (`material.thick_wall`), <= 0.3 g of thick material
  more than 10 mm from every fastener/insert/contact face (`material.load_free`). Grams saveable per part and in total
  are reported (`material.saving`, metric `material.saveable_g`).
- Intentional mass is exempt: kind armor/weapon/wedge/wedgelet/skirt, elastomers, or `"solid_reason": "..."`.

## Combat design rules (ground game; checked by `combat.R*`)
Whoever gets under the other wins. Full rules with rationale, thresholds and applicability: `robot/rules/combat_rules.md`
(112 rules, 83 measured as `combat.Rnnn`, the rest listed under NOT CHECKED). Family from `archetype`, else `robot_type`.
- **Skirt every edge.** Something within 1-1.5 mm of the floor across >= 80% of the front (R001-R002), within 3 mm on
  >= 60% of each side (R003-R004) and >= 50% of the rear (R005); corners <= 5 mm (R006-R009); no open arc > 45 deg
  (R011), no 8 mm gap in the front edge for forks (R015). A wheel at the outline counts as open.
- **Lip:** 0.2-1.0 mm off the floor (R020-R021; hinged skirts rest <= 0.5 mm with >= 10 deg travel, R035-R036), ramp
  10-35 deg with a <= 25 deg entry (R022-R023), <= 1.2 mm thick 1 mm back and no vertical nose (R024-R026), metal or
  laminate (R027), the front-most part (R029), lowest at the tip (R030), level (R031), bends <= 1 mm under 50 N
  (R032-R034), clear of the wheels (R037), >= 2 screws (R038).
- **Forks:** >= 2 tines, gaps <= 25 mm unless the weapon/skirt closes them, tips level and leading (R040-R043).
- **Weapon vs floor:** vertical sweep 0.8-6 mm (R050), never through the floor (R051, blocker), horizontal blade 1-15 mm
  (R052), no open door under the weapon (R053), lip leads the disc by 0-12 mm (R054).
- **Weight and drive:** >= 70% on driven wheels, <= 15% on the lip (R060-R061); CoG/track <= 0.5, CoG/wheelbase <= 0.6,
  lower half of the body, centred (R062-R066); grippy tyres >= 20 mm dia, >= 6 mm wide (R067-R069); traction-limited
  drive, 1.5-8 m/s (R073-R074).
- **Floor contact:** only wheels touch (R080-R081); belly >= 1 mm, interior >= 1.5 mm, no flat drag area, screw heads and
  switch off the floor (R082-R086).
- **Inverted:** drive upside down or self-right (R090); keep a lip on the top side too (R091-R094).
- **Wheels hidden:** none at the front edge, <= 25% of sides/rear, <= 10% overall (R110-R113); body ahead of and outboard
  of the wheels (R114-R115). Battery >= 10 mm from the front, >= 5 mm from the sides (R120-R121).

## Reference proportions and reference CAD (checked by `reference.feature_ratio`, `reference_cad.*`, `plausibility.density`)
- `reference_ratios` (or `reference.ratios`): `[{name, num, den?, value, tol | tol_frac, severity?, source, lesson?, fix?}]`.
  Terms: `overall.L|W|H`, `part:<glob>.<q>`, `kind:<glob>.<q>` (q = L W H cx cy cz mass vol count), `mass.total`,
  `count.fasteners`, `metric:<report metric>` (any earlier group's metric), or a number; a list is summed. Ratios cancel
  photo scale. Off by more than tol → warning (or `severity: blocker`); a term that cannot be measured → NOT CHECKED.
- `reference_cad: {dir, parts: [{part, file, mode: shape|envelope, tol_mm, tol_vol_frac, hole_tol_mm, at?, at_tol?}]}`
  compares our part with a reference STL by pose-independent fingerprint: oriented-box extents, volume, through-hole count,
  and for plates the mid-plane holes (diameter, radius from centre: bores, bolt circles, pockets), plus optional placement.
  Reference CAD is for MEASURING only: a model mesh that is triangle-for-triangle the reference (Hausdorff ≈ 0 after
  alignment, same face count) is `reference_cad.copied` BLOCKER. Build every part from parametric code.
- `plausibility.density`: bought-in parts (battery, motors, ESC, switch) must have mass / modelled volume in a physical range
  (LiPo 1.0-2.6 g/cm3). A wrong envelope hides a packaging problem; a wrong mass hides a budget problem.

## Design rules learned from reference matching (Revron/RVRN audit, 2026-10)
1. **Budget the rotor first.** A spinner puts ≥20 % of the robot mass in the rotating stack; everything else gets what is
   left. If the rotor fraction is low, look for mass in the drive, shell and fasteners, not in the weapon.
2. **Wrap the rotor around the motor can (drisk).** Two discs on a spacer around an outrunner bell: the can becomes rotating
   mass, the stack width becomes impact width, and two plates on a spacer form a stiff box section. Bolt the disc to the
   can's own mount holes; no spider, no pins.
3. **Support the weapon motor on both sides** on the strongest shaft available (the 5 mm prop mount), bearing on one
   upright, clamp on the other.
4. **Make one part do several jobs.** RVRN's 4 Al standoffs clamp the weapon module, are the front-wheel axles and carry
   the wedglets and side panels. Count parts and fasteners against the reference; each joint costs flanges, screws and inserts.
5. **Direct drive where possible.** Driven wheels sit straight on the gearmotor shafts; idler wheels run on a structural
   standoff via a belt. Every axle, bearing and hub you delete is mass and a failure point gone.
6. **Size the battery to the duty cycle, not "biggest that fits".** A 150 g drisk runs 3 min on 2S 180 mAh.
7. **Calibrate verifier models on a robot that is known to work.** A check that fails a proven winner (the old runtime model
   failed RVRN on 180 mAh) is wrong; anchor it with a test.
8. **Use vendor/reference CAD envelopes for bought-in parts**, and sanity-check mass against volume.
9. **Thin covers, ribs in the tub.** The base panel is a 1 mm plate; stiffness comes from the tub's X-rib and walls.
10. **Compliant armour on hard nodes.** TPU wedglets and side panels hang on the standoffs and press-fit nuts, so hits go
    straight into structure; forks sit inside the pods, just outside the disc.
11. **Inserts only where screws come out often.** RVRN uses 5 (base panel); the rest are standoffs and press-fit nuts.
12. **Keep paired supports matched** and plates loaded in their own plane (4 mm uprights printed flat).
13. **Centre the rotor between its supports**, so both bearings and the chassis see symmetric loads.

## Design intent: check what a feature is FOR (`intent.*`, `intent` list in the spec)
A part can match the reference outline and still not work. List each purposeful feature in `intent` with a `why`; the
probe tests the function (robot/checks/intent.py has the keys). BLOCKER unless `"severity": "warning"`.
1. **Keyed drive** (`keyed_bore`): a hub on a D-shaft has a D in its bore over its whole length. A round printed bore slips at stall.
2. **No supports** (`support_free`): in the declared build direction, overhang steeper than 45 deg that is wider than a
   6 mm bridge and a 1 mm ledge is <= 2 % of the area. Use 45 deg chamfers under ledges and flanges.
3. **Walls >= 1.8 mm** (`min_wall`, `envelope` for the outer skin): 4 perimeters at 0.45 mm.
4. **Fillet concave load corners** (`fillet`): no sharp inside corner where a hit loads PLA.
5. **Insert columns reach the bed** (`insert_column`): solid material from each heat-set insert back to the first layers.
6. **Tyre retention** (`tyre_retention`): the seat crest is >= 1 mm over the relaxed tyre ID on diameter.
7. **Captive nuts** (`captive_nut`): with the screw out, the nut moved 0.3 mm in any of 14 directions hits its pocket.
8. **Wheels run clear** (`wheel_clearance`): >= 1 mm from every body except its own hub, axle and belt. A rub is a brake.
9. **Flush heads** (`flush_head`): countersunk heads are no more than 0.2 mm proud of the face they sit in.
10. **Notch bears, bolts clamp** (`notch_bears`): pushed along the hit reaction, the plate meets the chassis tab before
    it meets any bolt shank.
11. **Seats locate** (`seat_locates`): a gearmotor in its keyhole cannot shift 0.15 mm radially or turn 2 deg.
12. **Small pit kit** (`tool_count`): two hex keys for the full teardown, one for the weapon-module swap.
13. **Wires clear the rotor** (`wire_clear_rotor`): every wire (straight proxy between ports) stays >= 2 mm outside the
    rotor's swept cylinder.

## Bought-in sizes, fit, containment, disassembly and coverage (`cots.*`, `fit.*`, `contain.*`, `disasm.*`, `coverage.*`)

- **No unlisted sizes** (`cots.unlisted`, BLOCKER): every motor, ESC, battery, RX, switch, servo, bearing, insert, nut and
  tyre (or any part with `cots: true`) uses a catalog id; a bearing may instead carry a standard designation (e.g.
  `MF85ZZ`) in `designation` or `label`. `cots.dims_mismatch` (BLOCKER): a declared `dims` or own shape/bearing model
  differs from the listed size by > 0.3 mm. `cots.fastener_size` (BLOCKER): screws are M1.6/2/2.5/3/4/5/6 in stocked lengths.
- **Snug fit** (`fit.*`): a component with walls within 3 mm on two or more faces is in a pocket; gaps are ray-measured on
  all six faces. Per axis with walls on both sides the clearance must be in the wall process's band (printed 0.1-0.5 mm
  per side, machined 0.05-0.3; override with `fit: {min_mm, max_mm}`, opt out with `fit: "none"`). `fit.loose` and
  `fit.tight` warn, `fit.interference` blocks; `clearance_mm` declared on the part must match the model (`fit.declared_mismatch`).
- **Containment by role** (`contain.*`): electronics inside the convex envelope of chassis/armour parts (a shaft inside its
  own wheel/hub/weapon is fine; deliberately exposed parts declare `exposed: true`); wheels protrude below the body and,
  when `can_run_inverted`, above it; routed wires stay inside unless the wire has `external: true`; the power switch has a
  clear straight tool line from outside (`contain.switch_access`).
- **Disassembly graph** (`disasm.*`, shared builder `robot/analysis/disassembly.py`): nodes are parts and screws; an edge
  X -> Y means X must come off first (X in Y's driver line, a screw clamping a part, a part trapped by another; mutually
  trapped clamped stacks come off as one). The graph must be acyclic (`disasm.cycle`), every screw reachable
  (`disasm.unreachable`), and battery, weapon, wheels, armour (or `serviceable: true`) reachable within
  `service.max_removals` (default 8, `disasm.service_depth`). O-rings/elastic belts are not "trapped" when they can be
  stretched over the largest flange within the material limit (nitrile 50 %, viton 30 %; `disasm.elastic_stretch`);
  installed tension is `tension.belt_stretch`.
- **Coverage** (`coverage.uncovered`, WARNING): lists any part kind only generic checks touch, made parts with no
  material/process, rotating parts of a kind no balance/clearance check knows, and part pairs within 0.5 mm with no
  declared relation (screw, connection, allow_overlap, parent/fused/cover, captive pocket, belt/pulley, tyre/rotating group).

## Template engine (`robot gen`)

`robot/gen` turns a design hypothesis into a complete spec that passes `robot verify` with zero blockers.

- **Hypothesis space** (`robot/gen/hypothesis.py`): axes weapon, mount, orientation, attachment, front, drive layout,
  drive motor, wheel size, transmission, guards, invertible, battery, ESCs, receiver. Values follow
  `research/antweight_taxonomy.json` (copied to `robot/gen/data/`). `robot/gen/rules.py` prunes the space with small
  named rules (one function each, each tested), including a mass and size lower bound (`budget.py`).
- **Layout CSP** (`robot/gen/layout/`): places battery, ESCs, receiver and switch inside the outline around fixed
  keep-outs (drive, weapon, screw bosses). It uses forward-checking DFS and returns the top-K distinct layouts, scored on
  wire length, centre-of-mass offset and compactness.
- **Generators** (`robot/gen/external/`): clamshell shell halves, housings and snug pockets with port notches, drive
  pods, clamshell screws with heat-set inserts, A*-routed wire channels, power switch, wedge, and weapon modules
  (`vspin_drisk`, `hspin_bar`, `lifter`).
- **Assembler + gate** (`build.py`, `gate.py`): `gate()` builds, verifies, and on blockers retries other layouts and
  seeds. It never returns a spec that has a blocker; if no variant passes it raises `Rejected`.

```
python3 -m robot gen list-hypotheses --fix weapon=vspin_drisk --limit 5
python3 -m robot gen build --hypothesis vspin_drisk --out out/ --fast   # gated: 0 blockers or exit 2
python3 -m robot gen build --hypothesis "weapon=wedge,wheel_dia=25" --out out/
python3 -m robot gen layouts spec_inputs.json -k 5    # LayoutInputs JSON (outline, components, keepouts, ...)
python3 -m robot gen layouts hspin_bar -k 3           # or the layout problem of a hypothesis
```

## Reference BOM and build-guide details (`bom` group)
- **Match the build guide's BOM** (`reference.bom`, blocker): list the guide's rows in `reference_bom`
  (`role`, `kind` fastener/part/wire, `match` id globs, `count`, `designation`, `head`, `threads_into`
  nut/insert/standoff/motor/tapped, `material`, `catalog`, `connector`, `optional`). A row that differs fails unless it
  carries `deviation` with the engineering reason (e.g. a 1 mm panel cannot take a 1.3 mm CSK head). Screws in no row
  are a warning (`reference.bom_extra`).
- **The weapon lock is a real part** (`legal.weapon_lock_part`): name it in `weapon.locking_bar`; a declared virtual
  pin cannot be weighed, printed or checked against the rotor (enforced when `weapon_lock.require_part` is set). A printed tooth stop that hugs a tip (<= 0.3 mm, no
  overlap at rest) is fine; give it `role: weapon_lock` (not kind locking_bar) when it is TPU.
- **O-ring belts are stock sizes** (`kin.belt_stock`): set `belt.stock: {id_mm, cs_mm}` from the stock list,
  `length_mm = pi x ID`, `width_mm = CS`; 5-15 % stretch over the pulleys.
- **Modules unplug** (`disasm.wire_cut`): a wire that crosses a `modules` boundary needs `connector` (bullets on the
  weapon phases), or removing the module means desoldering.
- **Switch OFF direction** (`electrical.switch_direction`): declare `off_dir` on every switch (missing = warning, wrong = blocker); OFF must be the outward
  (pulled) direction through the face it sits in.
- **Reference notes stay current** (`reference.doc_consistency`): `reference_doc: {path, must_mention, must_not_mention}`
  names the parts the write-up must describe and the retired ones it must no longer claim.

## Combat failure modes (checked by `threat.CF-*`, `threat.CFX-*`)

How an opponent, the arena or the robot's own weapon breaks the robot (research/combat_failure_modes.json). Each failing
finding names the weak point, WHY it matters and the FIX. Measured once per run in `robot/checks/threat/` against a
reference attack model (`attack.py`: spinner 25 J / 40 m/s tip, 6 mm bite, 5 J hammer, debris bands 1.5-15 mm wheel /
1.5-10 mm weapon, attack bearings and height bands per weapon type). Blockers: **CF-GD08** (wire within 3 mm of the
weapon's swept volume; needs `--full` wiring routes) and **CF-OW01** (weapon touches the floor at 5 deg nose-down pitch).
Everything else is a warning or info. Assumptions where the catalogue leaves a number open are in each rule docstring
(`robot/checks/threat/rules.py`), e.g. CF-WL06 uses 0.65 N/100 g because 1.3 N/100 g needs mu > 1.3.

| id | sev | check | WHY |
|---|---|---|---|
| CF-VS01 | warning | Bite-edge exposure to vertical spinner | A tooth needs a horizontal-ish edge or step to catch; any step >= tooth bite depth lets it transfer full energy instead of glancing. |
| CF-VS02 | warning | Front lip survives a vertical-spinner hit | Thin wedge/fork tips meet the teeth first; a printed or 0.8 mm lip shatters or bends up, leaving a gap the spinner then exploits. |
| CF-VS03 | info | Forks vs spinner (sacrificial spacing) | Forks present less bite; if tine gaps are wider than tooth width they still let the disc reach the body, but they should break off before the chassis. |
| CF-VS04 | info | Launch arm: CG height vs contact point | Hit below CG flips/launches robot; impulse J = sqrt(2*m_opp_weapon_I*E)/r. Rotational launch more likely when contact far below CG. |
| CF-VS05 | warning | Top edge catch for drum | Drums hit the top front edge of tall robots; vertical face above the lip is a catch. |
| CF-VS06 | warning | Gyro of own vertical weapon on hit (stall/reaction) | Opposite reaction torque on hit pitches robot; if weapon motor mount or belt slips, weapon dead. |
| CF-HS01 | warning | Side armour bite by horizontal spinner | Undercutters hit 0-15 mm high at the side; vertical side walls give full bite. |
| CF-HS02 | warning | Wheel exposure to horizontal blade | A wheel touched by an undercutter is torn off or stalls the drive. |
| CF-HS03 | warning | Overcutter top exposure | Bar at 30-60 mm clears low wedges and hits tops; protruding top features (switches, weapon pulleys) get ripped. |
| CF-HS04 | info | Being launched sideways (recoil spin-out) | Hit imparts lateral impulse; if traction low robot spins out and the side wall then gets hit. |
| CF-HS05 | warning | Skirt edge lift into undercutter | A flexible skirt rising >3 mm gives the blade an edge. |
| CF-HA01 | warning | Top plate penetration by axe | Pointed axe tip punches printed top plates; damage lands on internals underneath. |
| CF-HA02 | warning | Critical part directly under thin top | Damage path from top: what is within 10 mm below a thin region. |
| CF-HA03 | warning | Hammer-saw / top saw abrasion of wires | Saw dwells on top; any wire within top 3 mm cut. |
| CF-WL01 | warning | Get-under margin vs reference opponents | Whoever is lower wins; compare edge gap distribution to reference opponents from taxonomy. |
| CF-WL02 | info | Lift torque needed (resistance to being lifted) | A lifter must raise CG; heavy front & low CG increase required lift work. |
| CF-WL03 | warning | Grab points for grabbers/crushers | Grabbers need a gripable section; overhangs and narrow waists help them. |
| CF-WL04 | warning | Crusher clamp load on shell | Clamp crushes printed shell onto battery. |
| CF-WL05 | info | Flip landing recovery | Once flipped you must work inverted. |
| CF-WL06 | info | Wedge-on-wedge stalemate push | When both are equal, pushing force decides. |
| CF-WL07 | warning | Side approach / T-bone get-under | Sides usually higher than front. |
| CF-AR01 | warning | Wall pinning | Robot pinned with weapon side to wall loses mobility. |
| CF-AR02 | info | Pit/out-of-arena drift | Low traction or slow robot is pushed out. |
| CF-AR03 | warning | Stuck on the side | Robot resting on side cannot recover. |
| CF-LD01 | warning | Landing impact on printed chassis | Drop energy m*g*h = 0.15*9.81*1 = 1.5 J concentrates on corners. |
| CF-LD02 | warning | Landing on wheels/shaft | Landing on a wheel bends a 3 mm shaft or N20 output. |
| CF-LD03 | warning | Component ejection on landing | Loose battery/receiver moves and rips connectors. |
| CF-DB01 | warning | Wheel-to-guard gap jam band | Debris wedges between rotating tyre and static guard and stalls the wheel. |
| CF-DB02 | warning | Weapon-to-frame jam band | Debris caught between spinning weapon and frame stops it or breaks belt. |
| CF-DB03 | warning | Belt/pulley pinch point exposure | Debris into belt nip throws belt. |
| CF-DB04 | info | Open vents/holes admitting debris | Holes >2 mm over electronics let shards in. |
| CF-DB05 | info | Exposed gearbox/motor shaft | N20 output exposed gets debris in gears. |
| CF-DB06 | info | Tyre debris trap (treads) | Tyre grooves 2-4 mm pack with dust. |
| CF-ST01 | warning | Layer-direction weakness at hit points | FDM inter-layer strength ~ 30-60% of in-plane; hits loading layers in tension delaminate. |
| CF-ST02 | warning | Thin wall at hit point | Wall thickness < 2 mm fails on any spinner hit. |
| CF-ST03 | info | Stress concentration at sharp internal corners | Sharp internal corners crack. |
| CF-ST04 | warning | Bolt boss pull-out under hit | Bosses in PLA tear out. |
| CF-ST05 | warning | Brittle material on impact face | PLA shatters; TPU/PETG/Nylon absorb. |
| CF-ST06 | warning | Global frame torsion / split | Hits split the chassis at narrow cross-sections. |
| CF-GD01 | warning | Chunk-removal survivability | Remove 20 mm sphere at each hit-point; check if drive, weapon, power and radio subgraph remain connected. |
| CF-GD02 | warning | Single-point-of-failure wire | One wire supplying everything near the skin. |
| CF-GD03 | warning | Battery near impact face | LiPo puncture -> fire / disqualification. |
| CF-GD04 | warning | Receiver/antenna exposure | Receiver damage = dead robot; antenna cut = failsafe. |
| CF-GD05 | info | Drive redundancy | 2WD with one wheel lost is crippled; 4WD survives. |
| CF-GD06 | warning | Switch/link accessibility and protection | Removable link needed per rules; exposed switch may switch off when hit. |
| CF-GD07 | info | Connector strain relief | Shock tears unrelieved solder joints. |
| CF-GD08 | blocker | Weapon motor wires near spinning parts | Wire touching weapon is cut. |
| CF-GD09 | info | ESC thermal/mechanical isolation | ESC boards crack under shock. |
| CF-AS01 | warning | Splinter/gouge snag vs fork tip angle | A tip that meets a raised splinter at a steep angle hooks it and stops/pivots the robot; a shallow tip rides over. Trade-off: lower tip wins the under race but meets more splinters. |
| CF-AS02 | warning | Floor-panel seam/step catch | Lip at 0.2 mm meets a 1 mm step head-on and stops dead (or pivots if only one side catches). Trade-off: lip below step height maximises get-under but guarantees seam strikes. |
| CF-AS03 | warning | Lip stiffness vs dig-in | A very stiff lip pressed down by robot weight/opponent digs into soft wood; a too-flexible lip folds under. Trade-off: stiff = consistent low edge, but digs; flexible = conforms, but folds or lifts. |
| CF-AS04 | warning | Flexible tine wedging into floor-wall gap | Narrow flexible tines enter the gap under/beside the wall and jam; robot is self-pinned. Trade-off: thin, narrow, flexible tines are best at getting under and worst for this. |
| CF-AS05 | info | Snag on arena screws/hazard plates | Low edges hook raised screws; side skirts snag hazard plates. Trade-off: same as floor seams. |
| CF-AS06 | info | Pit-edge hang-up | Long overhanging forks bridge a pit edge and lever robot in, or hang it. Trade-off: long forks reach under further. |
| CF-AS07 | info | Asymmetric snag pivot | Single tine snagging makes robot spin, presenting its side. Trade-off: multiple independent tines = more snag points. |
| CF-AS08 | info | Floor wear rounding over time | Lip wear rounds the edge raising effective height after 2-3 fights. Trade-off: soft lips conform but wear. |
| CF-OW01 | blocker | Weapon self-damage on floor strike when hopping | Hop on hit lowers weapon into the floor. |
| CF-OW02 | info | Gyro bounce onto back while turning | Gyro torque lifts one side on turns. |
| CF-OW03 | warning | Belt slip/derail on hit | Hit shock derails belt. |
| CF-OW04 | info | Weapon bearing support after shell damage | If an upright is chunked, weapon falls out. |
| CF-OW05 | info | Power-on after inversion (battery shift) | Battery shift pulls connector. |

Extended clusters (combat_failure_modes_ext.json, uncalibrated, all warnings): **CFX-SWITCH** switch hit first from the
side or dragging on the floor when inverted; **CFX-ANTENNA** modelled antenna on the outer skin; **CFX-FRICTION** pins/tyres
held only by friction/press fit; **CFX-TAPE** electronics held only by tape/velcro; **CFX-STATE** no answer when inverted,
one drive side dead, weapon dead, radio failsafe, or on its side.

## Design-review gates (groups `ref_map`, `cots_fidelity`, `wire_review`, `fastener_record`, `belt_wrap`, `print_orient`)

From the Revron 2.0 CAD review: findings a reviewer had to spot by eye are now checks. Run them alone with
`python3 -m robot verify spec.json --only ref_map,cots_fidelity,wire_review,fastener_record,belt_wrap,print_orient`.

- **reference.unmapped_part**: every part and fastener maps to a part in the reference STEP parts index
  (`reference_cad.dir`): a reference_cad entry, `ref_part: "<stem glob>"`, or a `reference_bom` row that cites an index
  part (`ref_parts` globs or a role word such as `FS8`/`RV15`/`spider`). Our own BOM rows (no cited part, or "not in the
  STEP") do not count. Otherwise write `deviation: "why"` on the part, fastener or row. WHY: disc nuts and a lock pin
  were invented and nobody asked why.
- **cots.fidelity**: motors carry their identifying features (outrunner bell, stator base, shaft, mount bolt circle;
  gearmotor can and shaft) within 0.3 mm of `cots_fidelity.FEATURES` or the part's `features`. WHY: the GR1507 model had
  no stator holes and "looked wrong". Screw drive recesses are cut by `fastener_shape`, not judged here.
- **wire.rotating_clearance**: every fastener and nut that turns with the weapon sweeps a ring; each wire bundle
  (`count` x (OD + 0.3)) along port -> via -> port, and the motor phase exit, keeps >= `review.wire.rotating_clearance_mm`
  (3). WHY: the phase leads ran next to the disc nuts.
- **wire.render_present**: every wire end resolves to a current port, and with `renders: {dir, views}` at least one
  render draws the wires (the `<png>.json` record `robot render` writes), newer than the spec, with each drawn end
  within 3 mm of the port now. WHY: the final renders had no wires and the only wiring view predated the switch move.
- **fastener.hole_record**: every fastener has a `hole` record, and a screw into a printed part (not an insert or nut)
  has length - grip >= `review.fastener.min_engagement_d` x d (2.5 d). WHY: switch screws had no hole record; M2x4 into
  PLA strips.
- **cots.belt_wrap**: an O-ring belt is one closed loop (Euler number 0) with a run on both sides of each pulley centre.
  WHY: the belts were flat strips.
- **print.orientation_declared**: every FDM part declares `print_orientation` and its overhang/bridge is judged in THAT
  orientation (limit `review.print.max_overhang_mm2`, default 60 mm²), not the best of six. WHY: the electronics cage
  only works deck-down, which turns the floor lugs into overhangs.

## Support in every orientation (`support.loose`)

Every part not held to the chassis by a declared hold (screw through/into it, press_fit, clamp, strap, glue, pin, shaft,
fused; chains of holds count, and a group held only to itself moves as one body) is slid along all six axis directions:
gravity with the robot upright, inverted and on each side. More than 0.2 mm of free travel before hitting another part is
a blocker naming the part, direction and travel. WHY: robots are flipped and shaken every match, so "it rests in the
pocket" is not retention; a part held by gravity alone drops out or hammers itself and its wires apart the first time the
robot is upside down. `retained: pocket`, tape/kapton/velcro and `interlock` are measured, not trusted (tape peels once
the part hammers). Joints and tensioned belts are left to `kinematics.*`/`tension.*`. Fix by closing the open side to
<= 0.2 mm (lid, rib, clip) or adding a real hold to the chassis.

## CAD authoring tools (`robot/cad`): remove recurring modelling mistakes

**Holes from the fastener catalog** (`robot.cad.holes.hole`). WHY: holes sized by eye gave countersinks too small
(head proud or clashing), counterbores the wrong depth, tap holes at clearance size and nut pockets that fall out.
`part, rec = hole(part, at, axis, "M2x6", head="csk"|"button"|"cap", into="through"|"tapped"|"insert"|"nut", grip=...)`
cuts ISO 273 clearance, tap drill, heat-set insert bore, ISO 10642/14581 90 deg countersink, ISO 7380/4762
counterbore (cap: flush by default) and ISO 4032/4035 hex pockets (`nut_fit="press"` +0.05 AF, `"drop"` +0.3).
`at` is the surface point, `axis` points head -> tip; `side="head"|"thread"` cuts one part of a two-part joint.
`rec.to_spec(id, through=[...], threads_into=..., M=part_to_world)` gives the `fasteners[]` entry, including a
`hole` record. The `fastener_seat.*` group then probes the real geometry: csk flush (+-0.25 mm), counterbore floor
depth, head clash with material, head bearing, thread bite / pilot open, insert bore, nut pocket. With a `hole`
record a mismatch is a BLOCKER; without one, only head-type defaults are checked (WARNING).

**Assembly mates** (`robot.cad.mates`, applied on spec load). WHY: hand-typed world coordinates drift when the part
they sit on moves. A part with `"mate": {"to": "plate", "constraints": [{"type": "face", "a": "top", "b": "face",
"offset": 0}, {"type": "coaxial", "a": "bore", "b": "shaft"}]}` gets its `at`/`rot` solved from the target's
current pose (features in each part's own frame, by name from `"features"` or inline). Types: face, coaxial (+axial
offset), point_on_plane, point, angle. Sequential rigid solve; mates chain, so moving a part moves its dependents.

**Smooth parts** (`robot.cad.smooth`). WHY: stacked extrusions at measured heights leave stair steps (90 deg creases)
that fail section/silhouette matching. `loft_stations([Station(z, profile), ...])` lofts exact B-spline / ellipse /
rounded-rect sections; `sweep_profile`, `fillet_all`. `smoothness(solid)` reports max crease angle, section-radius
curvature and step count; a loft scores ~0 steps, a stack scores one per tread. Test new organic parts with it.

**Curve fitting** (`robot.cad.fit`, `measure-ref --fit`). WHY: organic outlines were copied as dense polylines (a copy
and a stair source) or guessed. `fit_bspline(points)` finds the FEWEST control points (4..8, capped) meeting RMS
<= 0.3 mm; `segments()` splits an outline into lines and arcs; `fillet_radii()`. The ctrl lists go straight into a
`{"type": "bspline", "ctrl": [...]}` profile for `loft_stations`.

**Reference measuring** `python3 -m robot measure-ref ref.stl|step [--part NAME] [--sections N] [--fit]
[--stations "z:2,5;x:0"] [--md]`. WHY: params were guessed from renders. Prints numbers only: bbox, per-axis section
sizes/areas/hole counts, holes (diameter, shape round/D/hex/slot, shapes along the axis, axis, through/depth, csk
angle + dia, cbore dia + depth), wall thickness stats, fillet radii, and with --fit low-DOF sketches. A guard
refuses to print any point list longer than 8 (no polygons/meshes): type the numbers into params.

**Incremental verify** `python3 -m robot verify spec.json --changed`. WHY: full verifies take minutes, so people
skipped them. Each check group's actual reads of part geometry are recorded; a group is reused only if the spec
(minus geometry fields), code, options, earlier groups' outputs and every part it read are unchanged. Equivalence with
a full run is tested. Plain `verify` is unchanged and remains the reference.

**Done gate** `python3 -m robot gate spec.json [--renders DIR] [--views iso.png,top.png]`. WHY: "matches the
reference" was claimed on partial evidence. Prints PASS/FAIL for: full verify 0 blockers, every
`reference_cad.diff`/`.features` passing (and present), every `intent.support_free`/`printability.*` passing (and
present), render PNGs present and newer than the spec. Exit 0 only when all pass. Run it before claiming a match.
