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
- Moving parts: `parent` plus `joint: {kind (revolute|prismatic), axis, pivot (parent frame), min, max, default}`; the verifier sweeps it.

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
