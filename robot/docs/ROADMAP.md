# Roadmap: features and gaps

Goal: anyone with an LLM specifies a 150 g UK antweight and gets an accurate,
instantly manufacturable robot.

Written 2026-11-12 from a read-only review of the repo by six reviewers, one
angle each. Nothing was run. Paths were read on a working branch, so confirm
each against `dev` before coding. Items another thread already owns are left
out: `robot build design.json` CLI and eval set, Revron tub bays from catalogue
parts, shared `robot/modules/`, in-process swap sweeps and param-hash cache,
basic `robot/mfg/` pack, render speed, Design object / `bay.py` / verify tiers /
CI.

Ids: L = LLM interface, R = robustness and speed, M = manufacturability,
U = user experience, C = checks and physics, A = archetypes.

## Ranked list

| # | Id | Feature | Why it ranks here |
|---|----|---------|-------------------|
| 1 | L1 | Structured fix actions on every finding | Unblocks self-repair, MCP, compact report. About a quarter of failures have no hint at all. |
| 2 | R1 | Typed COTS port contracts | Swap hold rate is 24/64. Turns crashes into declared-unfit with a reason. |
| 3 | R2 | Wheels fully derived from `WheelIface` | 8 of 40 swap breaks are one literal-driven error. |
| 4 | R6 | Robust geometry ops with blame | Bare OCP errors give "rc 1" with no param name. |
| 5 | U1 | Installable package, `robot doctor`, `robot quickstart` | `pip install` does not install `robot` today. First wall for any newcomer. |
| 6 | M2 | Named fits with process compensation | Printed bores come out 0.1 to 0.2 mm tight. Decides if it assembles first time. |
| 7 | M3 | Build-plate export, oriented and packed | STLs are in assembly frame. User must re-orient by hand. |
| 8 | L5 | Compact LLM report with delta between iterations | Full report does not fit a context window. LLM cannot see if its edit helped. |
| 9 | R3 | Param relation graph with provenance | Unblocks R4, R5, R7, R8. Removes `fresh_import` hack. |
| 10 | L6 | Self-repair loop that searches fixes | Today only `mass.over` auto-repairs. |
| 11 | L2 | Requirements block in design.json | Users speak intent ("fast pusher, survives vertical spinners"), not enums. |
| 12 | L4 | One error envelope and one schema | Two front doors with different error shapes. |
| 13 | R5 + M5 | Mass autosolver plus slice-based mass estimate | Printed mass is `volume * density * 0.85`, about 20% error on a 150 g limit. |
| 14 | R7 | Proxy tier and per-part incremental rebuild | Target under 1 s proxy verdict, under 10 s inner loop. |
| 15 | R4 | Clearance and insertion-path relations | `assembly.blocked` is the top hypothesis failure (about 24). |
| 16 | L3 | `robot mcp` stdio server | CLI is human print only. |
| 17 | U2 | One-page HTML report with 3D viewer | Only markdown and five PNGs today. |
| 18 | M1 + U5 | Printer, filament and builder profiles | FDM limits are module constants. Nothing asks what the user owns. |
| 19 | M4 | Purchasable BOM with UK vendors, cost, spares | Price and URL exist in data but nothing uses them. |
| 20 | U3 | `robot diff A B` | "What did my change do" has no answer. |
| 21 | M6 | Sheet and turned-part order pack | HARDOX and Ti weapons are the parts users cannot make at home. |
| 22 | M7 | Wiring harness and solder schedule | Where first-time builders fail. |
| 23 | M8 | Step-by-step assembly instructions | Removal order exists, nothing writes build steps. |
| 24 | L7 | Design patch language and provenance | Iteration means resending a whole design. |
| 25 | L8 + U7 | Generated LLM pack, AGENTS.md, skill | GUIDE.md targets raw-spec authors. |
| 26 | U4 | `robot explain <finding-id>` | Finding ids are opaque to newcomers. |
| 27 | U6 | Selectable rules profiles | Only `aws2025`. |
| 28 | R8 | Single source of truth for choices | Three hand-kept lists drift. |
| 29 | U8 | Gallery, fork hygiene, licence separation | `publish.yml` from upstream is a hazard. |

Start now, independent of each other: L1, R1, R2, R6, U1, M2, M3.
Define the fix/patch JSON shape once (L1 and L7 share it) in
`robot/design_io/patch.py`.

---

## L. LLM interface

Context: two unconnected front doors, `robot/design_io/__init__.py`
(`validate`, `schema`) and `robot/design.py` (`Schema`/`Setting`/`Design`).
`Finding.fix_hint` is prose. `gen/gate.py` `Rejected` keeps five strings.
No MCP server or prompt pack.

### L1. Structured fix actions on every Finding
- `robot/finding.py`: add `fixes: list[dict] = []`,
  `Finding.fix_op(op, path, value=None, delta=None, why="", est=None)`, emit
  `"fixes"` in `to_dict`.
- Shape: `{"op":"set"|"nudge"|"swap"|"remove","path":"drive.motor",
  "value":...,"delta_mm":...,"est":{"mass_g":-6.2},"confidence":"high|med|low"}`.
  `path` is a design.json or `Design` setting path, never a spec part path.
- New `robot/checks/fixmap.py`: `FIXERS: dict[id_prefix, Callable[[Finding,
  Spec, dict], list[dict]]]`. First 15: `mass.over`, `legal.footprint`,
  `legal.switch`, `fit.*`, `interference.*`, `power.*`, `combat.R*`,
  `joints.*`, `printability.*`. Called by `checks.verify` after groups. Swap
  candidates from `gen/changes.py candidates()` and `robot/cots_alts.py`.
- Accept (`robot/tests/test_fixmap.py`): `mass.over` fixture yields a fix whose
  path is in `design_io.schema()`; every fix validates after apply; a shrinking
  allowlist of blocker ids with neither `fix_hint` nor `fixes`.

### L2. Requirements block in design.json
- `design_io` accepts top-level `requirements`:
  `{"top_speed_mps":{"min":1.5},"push_force_n":{"min":3},
  "weapon_tip_speed_mps":{"min":40,"max":110},"weapon_energy_j":{"min":8},
  "mass_margin_g":{"min":3},"printer":{"bed_mm":[180,180,180],
  "materials":["pla","petg","tpu"]},"owned_parts":["n10_300rpm_6v"],
  "budget_gbp":{"max":80},"must_survive":["vspin","hspin"],"invertible":true}`
- New `robot/design_io/requirements.py`: `resolve(req, h) -> (Hypothesis,
  errs)` fills unset axes by filtering `H.enumerate_hypotheses`; `claims(req)`
  writes verifier `claims[]`; new check group `requirements` emits
  `requirements.<key>` with expected/actual.
- Accept: `owned_parts` forces `drive.motor`; impossible combo returns
  `unsatisfiable` naming the binding constraint; failing claim is a blocker.

### L3. `robot mcp` stdio server
- New `robot/mcp_server.py`, hooked in `robot/cli.py`. Tools: `schema`,
  `catalog(kind?, query?)`, `validate(design)`, `build(design, tier="inner")`
  returning `{ok, design_hash, summary, findings, metrics, mass_top5,
  not_checked, not_run}`, `apply_fix`, `explain`, `render`, `diff`.
- Responses capped near 4k tokens, findings paged with `cursor`.
- Accept (`robot/tests/test_mcp.py`): `tools/list` returns 8 tools with
  schemas; `{"weapon":{"type":"hspinbar"}}` suggests `hspin_bar`; no response
  over 16 kB on the wedge fixture.

### L4. One error envelope and one schema
- `robot/design.py`: `DesignError(code, field, message, value, allowed,
  suggestion, hint)` with `.to_dict()` matching `design_io._err`;
  `Schema.json_schema()`; `Schema.errors(values) -> list[dict]` collecting all
  errors.
- `design_io.validate` accepts `{"base":"revron","settings":{...}}`.
  `design_io.schema()` is `oneOf` hypothesis form or base form per robot.
- Accept: three bad settings give three errors in one call; identical envelope
  keys on both paths; `Design.to_dict()` round trip validates.

### L5. Compact LLM report with delta
- New `robot/llm_report.py`: `compact(rep, prev=None, budget_chars=6000)`
  returning `{ok, tier, blockers:[{id,msg,expected,actual,parts,fixes}],
  warnings_top, counts, mass:{total,lo,hi,limit,top5}, metrics_key,
  not_checked, not_run, delta:{fixed,new,still,mass_g}, next}`.
- Dedupe repeated ids by part. Order by root cause: validity, legal, mass,
  fit/interference, rest. Suppress downstream noise when `validity.*` fails.
- CLI `robot verify --llm [--prev report.json]`.
- Accept: within budget on `robots/revron/report.json`; delta correct on two
  synthetic reports; no passed findings.

### L6. Self-repair loop
- New `robot/gen/repair.py`: `repair(design, max_steps=6, tier="inner") ->
  RepairResult(design, report, trace)`. Take root-cause blocker, try its fixes
  by confidence, keep only if blocker set strictly shrinks, tabu on design
  hashes.
- `Rejected` gains `.report` and `.trace`. `gen/cli.py build --repair
  --trace out.json`. When stuck return `needs_user: [{question, options,
  tradeoff}]`.
- Accept (stubbed verify): converges on two-blocker fixture; never accepts a
  step adding a blocker; terminates on cycle; `needs_user` set when no fix.

### L7. Design patch language and provenance
- New `robot/design_io/patch.py`: `apply(design, patch) -> (design, errors)`,
  `diff(a, b) -> patch`. Patch ops `set`, `nudge`, `unset`.
- `gen/build.py` writes `spec["generator"]["design"]`, `design_hash`,
  `history`, `choices` (`{axis:{value, source, why}}`).
- CLI `robot design patch`, `robot design why spec.json drive.motor`.
- Accept: `apply(a, diff(a, b)) == b`; bad path returns error with suggestion;
  built spec round-trips to the same hypothesis slug.

### L8. Generated LLM pack with drift test
- New `robot/llm/pack.py build_pack()` from live schema, catalogue, top finding
  ids. Emits `robot/llm/SKILL.md` (150 lines max), `examples/*.json`,
  `system_prompt.txt`. CLI `robot llm-pack`, `robot guide --llm`.
- Accept: checked-in pack equals generated; every example validates.

---

## R. Robustness and speed

Root causes of the 53% hold rate: params are import-time module constants (no
graph, no blame); `CatalogEntry.ports` are bare dicts; wheel literals in
`params_chassis.py:92` and `params_drive.py:26-27`; neighbours do not follow a
growing bay; fragile selectors (`mount.py:289`, `panel_top.py:46-47`,
`panel_base.py:44`, `side.py:95`); choice lists in three places.

### R1. Typed COTS port contracts
- New `robot/ports.py`: frozen dataclasses `BoltPattern`, `Shaft`, `Envelope`,
  `LeadExit`, `Connector`, `Bore`; per-kind `GearmotorIface`, `OutrunnerIface`,
  `WheelIface`, `PackIface`, `EscIface`, `SwitchIface`.
- `iface(cid) -> Iface` raises `PortError(kind, cid, missing=[...])`.
  `compatible(a, b) -> list[Mismatch(port, field, have, need)]`.
- `weapon_motor.py` wraps it; `wheel_variant.py` returns `WheelIface`;
  `cots_alts.py` builders populate `ports`.
- Accept (`robot/tests/test_ports.py`): every catalogue id in every choices
  list yields an iface or a `PortError`, never `KeyError`/`TypeError`; 3 mm D
  shaft vs 2 mm bore flagged.

### R2. Wheels fully derived from `WheelIface`
- Add setting `wheel.front`. `WHEEL_OD_F = front_wheel().od`. `TY_FRONT`,
  `TY_REAR`, `FH_SEAT_R`, `FH_SEAT_W`, `FH_BORE_R`, `RH_SEAT_R`, `RH_LEN` from
  the iface. A wheel with its own hub skips printed RV19/RV21.
- Guards `seat_r > bore_r + MIN_WALL`, `od/2 > flange_r` raise `WheelUnfit`.
- Accept: 8 front and 8 rear ids build or raise `WheelUnfit`; zero
  `Standard_ConstructionError`; stock output byte-identical.

### R3. Param relation graph with provenance
- New `robot/params/graph.py`: `P(design).get(name)` lazy, memoised, records
  edges. `@param("SA_Z", unit="mm", lo=, hi=)`. `Graph.deps`, `dependents`,
  `masters`, `trace(name) -> [(param, value, file:line)]`.
  `@require("pack fits", lambda p: ..., blame=("battery.pack","size.width"))`.
- Migration: `robots/revron/src/revron/pgraph.py` AST-parses `params_*.py`
  into nodes; keep `from .params import *` via module `__getattr__`.
- Accept: graph equals module constants for default and 20 sampled designs;
  `dependents("CH_WALL")` includes `nut_cr` params; violation raises
  `ParamError` listing blamed settings.

### R4. Clearance and insertion-path relations
- New `robot/cad/insertion.py`: `insertion_corridor(bay) -> Box3`,
  `blockers(corridor, keepouts) -> list[str]`.
- Each fastener/pin position is a relation. Unfit raises `BayUnfit("battery
  trapped by bolt_p2; needs size.length >= +3.2 mm")`, delta by 1-D bisection.
  Optional `autosize=true`.
- Accept: 13 battery swaps hold or return n/a with a numeric fix; with
  autosize at least 10 of 13 hold.

### R5. Mass-budget autosolver
- New `robot/gen/mass_solve.py`: `solve_mass(design, target_g=149.0,
  knobs=("CH_WALL","BASE_T","TOP_T","lattice_density","DISC_T"), bounds,
  weights) -> MassSolution(values, mass_g, per_part, iterations, binding)`.
- Analytic sensitivities, bounded least squares, one exact CAD check, secant
  correction. Spare mass goes to weapon and armour first. Lower bounds from
  `checks/strength.py` and process min wall.
- Accept: every building swap lands in [148.5, 150.0] g within 3 exact
  rebuilds; infeasible reports binding constraint and grams over.

### R6. Robust geometry ops with blame
- New `robot/cad/safe.py`: `safe_fillet(shape, edges, r, *, name, min_r=0.2,
  steps=(1,.75,.5,.25,0))` clamps, validates, falls back to chamfer then none,
  records a `Degrade` warning. `safe_cut`/`safe_fuse` retry fuzzy, assert single
  non-empty solid, else `GeomError`.
- Selectors `sel.edges_at`, `sel.circle`, `sel.face_by_normal`, `sel.one`
  raising `SelectorError` with expected vs found. Replace the fragile sites
  listed above.
- `@feature("mount_r.notch", params=("MNT_IN","CH_HALF_W"))` rethrows as
  `BuildFailure(part, feature, params, suggestion)`.
- Fix `electrical` None comparison: emit `electrical.rating_unknown`.
- Accept: `CH_HALF_W_STOCK` -10% yields a built `mount_r` or a `BuildFailure`
  naming `CH_HALF_W`; fuzz 200 designs at 15% with no bare OCP/GEOS exception.

### R7. Proxy tier and per-part incremental rebuild
- New `robot/proxy.py`: `proxy_spec(design)` of boxes and cylinders, no OCP.
  `fast_verify(design) -> Report` with `tier="proxy"`: mass, legal fit, AABB
  overlap, insertion corridors, port compatibility, ground clearance, weapon
  sweep vs chassis, power budget.
- Per-part cache key = hash of only the graph params that part read.
- Accept: proxy agrees with full verdict on 90% of the 113 hypotheses; a
  one-setting change rebuilds 5 parts or fewer; p95 proxy under 1 s.

### R8. Single source of truth for choices
- `Setting(..., choices_from=lambda: [...])` from catalogue plus
  `ports.try_iface`. Delete `REAR_WHEELS`; generate `hooks.json`.
- Accept: adding a catalogue wheel needs zero edits in `robots/revron`.

---

## M. Manufacturability

Exists: `robot/catalog.py` materials and stock tables,
`robot/cad/fastener_catalog.py`, `checks/printability.py`, `checks/mfg.py`,
`checks/process.py`, `catalog_data/components.json` (37 UK rows with price and
URL).

### M1. Printer and filament profiles
- New `robot/mfg_profiles.py`: `PrinterProfile(id, bed_mm, nozzle_mm,
  layer_mm, xy_hole_shrink_mm, elephant_foot_mm, max_bridge_mm,
  max_overhang_deg, enclosure, max_nozzle_c, hardened_nozzle, direct_drive)`,
  `Filament(id, base_material, nozzle_c, bed_c, needs_enclosure,
  needs_hardened, needs_dry, needs_direct_drive, max_bridge_mm,
  max_overhang_deg, min_wall_lines, shrink_pct, gbp_per_kg, flow_mm3_s)`,
  `resolve(spec)`.
- `printability.py` and `mfg.min_wall_for` read the profile.
- New findings `printability.printer_capability` (blocker),
  `printability.bed_fit`, `printability.thin_feature`.
- Accept: 0.9 mm wall passes at 0.4 nozzle, fails at 0.6; `pa6_cf` on `ender3`
  blocks; default profile reproduces current findings.

### M2. Named fits with process compensation
- New `robot/fits.py`: `Fit(name, kind, delta_mm, note)` keyed
  `(fit_name, hole_process)`: `bearing_press`, `bearing_slip`,
  `shaft_running`, `shaft_press`, `heatset_m2/m2.5/m3`, `screw_clear_*`,
  `self_tap_plastic`, `axle_dflat_n20`, `pocket_snug`, `pocket_loose`.
  `cad_diameter(fit, nominal, hole_process, printer)`, `check(...)`.
- Part JSON features gain `"fit": "bearing_press"`. `catalog.press_fit_range`,
  `checks/fit.band_for`, `cad/holes.py` delegate.
- Findings `fit.named_missing` (warning), `fit.out_of_band` (blocker).
- Accept: `cad_diameter("bearing_press", 8.0, "fdm", generic)` in
  [8.05, 8.13]; MR84 seat at 8.00 nominal fails with the right diameter in the
  fix; M3 heat-set bore 4.0 fails, 3.7 passes.

### M3. Build-plate export
- New `robot/plate.py`: `orient(mesh, up)`, `pack(parts, bed_mm, gap=4.0)`,
  `write(root, plates)` giving `print/plate_<n>_<filament>.3mf`, per-part STL,
  `print/plates.json` with supports and brim flags. Called from
  `export.write_all`.
- New check `printability.first_layer`.
- Accept: every mesh min z = 0; plate fits bed; part count matches spec;
  200 mm part on 180 bed raises `bed_fit`.

### M4. Purchasable BOM
- New `robot/catalog_data/vendors.json` (no invented SKUs; unverified rows
  flagged). `CatalogEntry` gains `price_gbp`, `url`, `supplier`.
- New `robot/bom_out.py`: `build(r) -> list[Line]`, spares policy, `cost()`,
  writes `bom.csv`, `bom.md`, `order_<supplier>.csv`.
- Findings `bom.unsourced`, `bom.vendor_stale`.
- Accept: every fastener, bearing, catalogue part in `revron_ant.json` maps to
  a line; packs = ceil((qty + spares) / pack_qty).

### M5. Print time and filament estimate
- New `robot/slice_est.py`: `estimate(mesh, up, printer, filament, walls=3,
  top_bottom=4, infill=0.25) -> {mass_g, shell_g, infill_g, support_g,
  time_min, filament_m}`. `mass.py` source `slice_est` at tolerance 0.08.
- Accept: 20 mm solid PLA cube within 2% of 9.92 g; at 3 walls / 25% lands in
  4.0 to 5.5 g.

### M6. Sheet and turned-part order pack
- `export_dxf(r, out_dir, compensate=False)` with layers `CUT_OUTER`,
  `CUT_INNER`, `ETCH`, `BEND`; nest per stock; `dxf/ORDER.md`.
- Checks `process.sheet_min_hole`, `sheet_web`, `sheet_inside_radius`,
  `cf_dust`. Turned parts get `turned/<id>.svg`.
- Accept: DXF has only closed polylines; area within 0.5%; 1 mm hole in 3 mm
  HARDOX fails.

### M7. Wiring harness and solder schedule
- New `robot/harness.py`: `build(ctx) -> Harness(wires, joints)`; writes
  `wiring/harness.md` and `harness.svg`.
- Checks `wiring.ampacity`, `wiring.service_loop`, `wiring.removable_link`.
- Accept: every port pair appears once; 28 AWG battery lead on 10 A ESC fails.

### M8. Assembly instructions
- New `robot/assembly_doc.py`: `steps(ctx) -> list[Step]` from reversed
  disassembly order, at most 12 steps, prep steps, torque defaults (confirm
  against datasheets), per-step render, tool list, pre-fight checklist.
- Check `assembly.step_blocked`.
- Accept: every part and fastener in exactly one step; valid topological order.

---

## U. User experience

Today: root `README.md` is upstream build123d; no `AGENTS.md`, `CLAUDE.md`,
`Dockerfile`; `pyproject.toml` does not package `robot`; outputs have no HTML
report or GLB; one rules profile.

### U1. Installable package, `robot doctor`, `robot quickstart`
- `pyproject.toml`: extra `robot = [trimesh, manifold3d, shapely, rtree,
  networkx, pillow]`, script `robot = "robot.cli:main"`, package find includes
  `robot*`, package-data for templates, catalogue, guide, rules.
- New `robot/doctor.py`: `robot doctor [--json]`. `robot quickstart [dir]`.
  `Dockerfile`.
- Accept: `doctor.run()` all OK in CI; missing trimesh gives exit 1 with a pip
  line; CI runs `robot doctor` from outside the repo.

### U2. HTML report with 3D viewer
- New `robot/report_html.py build_html(spec, rep, renders, glb, prev=None)`,
  self-contained. New `robot/glb.py world_to_glb(world, palette)`.
  CLI `robot report spec.json [-o report.html] [--no-glb] [--fast]`.
- Accept: HTML contains mass, every failing id, not_checked count; GLB node
  count equals part count.

### U3. `robot diff A B`
- New `robot/diffcmd.py`: mass delta, findings newly failing/passing, metrics
  deltas, change categories, `--html` side-by-side renders and heatmap. Exit 3
  on regressions.
- Accept: identical specs give empty diff; removed fastener gives exit 3.

### U4. `robot explain <finding-id>`
- New `robot/checks/explain.py` `EXPLAIN` keyed by id prefix. `print_report`
  appends the hint. Coverage test with a shrinking allowlist.

### U5. Builder profile
- New `robot/builder.py` `Builder(printer_bed_mm, nozzle_mm, materials,
  processes, tools, budget_gbp, skill)`, presets in `robot/builders/`.
- New group `robot/checks/builder.py`: `bed_fit`, `material_unavailable`,
  `process_unavailable`, `tool_missing`, `budget`, `skill`. Share data with M1.
- Accept: 100 mm bed blocks the chassis; no builder key leaves reports
  unchanged.

### U6. Selectable rules profiles
- Move constants to `robot/profiles/*.json` with `source_url` and `version`.
  `robot profiles`, `verify --profile X`. Unknown profile exits 2.

### U7. Agent docs and skill
- Root `AGENTS.md` (80 lines max), `CLAUDE.md`, `.claude/skills/antweight/
  SKILL.md`, split `GUIDE.md` into sections, robot section atop `README.md`.
  Merge with L8 so there is one generated source.

### U8. Gallery, fork hygiene, licence
- New `robot/gallery.py`. `NOTICE` section for `robot/` and `robots/`.
  Restrict upstream `publish.yml` and `benchmark.yml`. CI path guard on
  `src/`, `docs/`, `tests/`, `examples/`. Remove dead `crates/` references.

---

## C. Checks and physics

Pending: reviewer still reading.

## A. Generator coverage and new archetypes

Pending: reviewer still reading.
