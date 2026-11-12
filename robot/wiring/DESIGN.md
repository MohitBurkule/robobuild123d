# robot.wiring: harness design and module contracts

STATUS: written without running anything (no builds, tests or renders). Treat every module as UNTESTED.

Goal: wiring any robot spec the way a builder would really wire it. Real gauges, real connectors, a netlist, smooth
routes that respect bend radius and stay out of harm's way, round wire solids in colour, chassis channels and tie
points derived from the routes, and checks. Nothing is Revron-specific; a part swap moves terminals and the harness
follows, because everything is derived from the spec + catalogue each time.

Frame: mm, world X lateral, Y forward, Z up. Shared types: `model.py` (read it first). Settings: `settings.py` +
`data/defaults.json`; code reads `cfg = settings.for_spec(spec)` and never holds a tuning number itself.

## Pipeline (plan.py)

```
cfg      = settings.for_spec(r.spec)
terms    = devices.world_terminals(r, world, cfg)          # {ref: WorldTerminal}
nl       = netlist.build(r, terms, cfg)                    # Netlist (from spec wires[], or derived from part kinds)
space    = field.FreeSpace.from_world(world, r, cfg)       # occupancy, distance fields, keep-outs
paths, bundles = router.route(nl, terms, space, cfg)       # {conductor id: WirePath}, [Bundle]
channels, ties = channels.derive(harness, space, r, cfg)
connectors     = channels.place_connectors(harness, cfg)
findings = checks.run(harness, world, r, space, cfg)       # group "harness"
```

## Terminal references

- A port is a GROUP of terminals (one housing / one lead set): `"battery.lead"`.
- One terminal of it: `"battery.lead/pos"` (`Terminal.name == "lead/pos"`, `Terminal.group == "lead"`).
- Spec `wires[]` keep naming ports (`from: "battery.jst_rcy"`); the netlist expands a lead into one conductor per
  role both ends share.

## Module contracts

### gauges.py (data/gauges.json)
- `table() -> dict[int, Gauge]`; `gauge(awg) -> Gauge` (nearest tabulated, float ok)
- `for_current(amps_cont, amps_burst=0.0, derate=1.0) -> Gauge` thinnest gauge that carries it
- `default_awg(kind, cfg) -> int`
- `lay_radius(ods, lay="round", margin=0.0) -> float` circumscribed radius of wires laid together
- `lay_offsets(ods, lay="round") -> np.ndarray (n, 2)` centre of each wire in the bundle cross-section (y, z)
- `mass_g(awg, length_mm) -> float`; `volt_drop(awg, length_mm, amps) -> float`

### connectors.py (data/connectors.json)
- `table() -> dict[str, ConnectorType]`; `connector(id) -> ConnectorType` (aliases resolved: `jst_rcy`, `bullet2`, `xt30`...)
- `mates(a, b) -> bool`; `mate_of(id) -> str | None`; `takes(id, awg) -> bool`
- `for_pins(family, pins) -> ConnectorType | None`
- `shape(id) -> dict` JSON shape tree (robot/shapes.py vocabulary) of the housing in the connector frame

### devices.py (data/device_ports.json)
- `terminals_of(rpart, cfg, overrides=None) -> dict[str, Terminal]` name -> Terminal, device local frame
- `world_terminals(r, world, cfg) -> dict[str, WorldTerminal]` ref -> placed terminal, every electronic part
- `resolve_ref(terms, ref) -> list[WorldTerminal]` (`dev.port` = whole group, `dev.port/role` = one)
- `group_centre(terms, ref) -> (pos, axis)`
- Port forms accepted on a part / catalogue entry: legacy `[x, y, z]`, typed dict
  `{pos|at, axis|dir, connector|type, roles, pitch_mm, pigtail_mm, awg, max_a}`; spec `harness.terminals["dev.port"]` overrides.

### netlist.py
- `build(r, terms, cfg) -> Netlist` = `from_spec` when the spec declares wires, else `derive`
- `from_spec(spec, terms, cfg) -> Netlist`; `derive(r, terms, cfg) -> Netlist`
- `currents(nl, r, cfg) -> None` fills amps on nets / conductors from catalogue ratings
- `validate(nl, terms) -> None` appends to `nl.problems`

### spline.py (pure numpy, no CAD kernel)
- `class BSpline(ctrl, degree)`: `.eval(u)`, `.deriv(u, k=1)`, `.sample(step_mm) -> (m, 3)`
- `cumlen(pts)`, `length(pts)`, `resample(pts, step)`, `tangents(pts)`, `radius_along(pts)`, `min_radius(pts)`
- `round_corners(poly, r_min, step) -> (pts, r_achieved)` tangent arcs at every corner
- `fit(poly, r_min, cfg, dir_a=None, dir_b=None, straight_a=0.0, straight_b=0.0) -> (ctrl, pts)`
- `add_slack(pts, extra_mm, r_min, side, clear_fn=None) -> pts`
- `frames(pts, up=None) -> (T, N, B)` parallel-transport frames; `offset_curve(pts, N, B, dy, dz) -> pts`

### field.py
- `FreeSpace.from_world(world, r, cfg, skip=()) -> FreeSpace`
- attributes `lo, cell, n, solid, dist, rot, fast` (grids), `hull` (trimesh convex hull of the structure)
- `clearance(P)`, `rot_dist(P)`, `fastener_dist(P)` -> (k,) mm, trilinear; `free(P, radius, ends=())` -> (k,) bool
- `blocked(radius, ends=()) -> bool grid`; `cost() -> float grid` (wall-following step cost multiplier)
- `wall(P) -> (normal (k,3), dist (k,), part ids list)`; `inside_hull(P) -> (k,) bool`; `cell_of(p)`, `centre(c)`
- `rotating_ids(r) -> set`, `lid_ids(r, cfg) -> set`

### router.py
- `route(nl, terms, space, cfg) -> (dict[str, WirePath], list[Bundle])`
- `route_lead(conductors, terms, space, cfg, done) -> (list[WirePath], Bundle | None)`

### solids.py
- `wire_mesh(path, cfg) -> trimesh.Trimesh`; `wire_solid(path) -> build123d Solid`
- `connector_solid(pc) -> build123d Solid`; `connector_mesh(pc) -> trimesh.Trimesh`
- `to_routes(harness) -> list[finding.Route]`; `add_to_world(world, harness, cfg) -> World`; `rgb(hex) -> [r, g, b]`

### channels.py
- `derive(harness, space, r, cfg) -> (list[Channel], list[TiePoint])`
- `place_connectors(harness, cfg) -> list[PlacedConnector]`
- `cut_shape(channel) -> dict`; `tie_shape(tie, cfg) -> dict`; `cuts_for(harness, part_id, world) -> list[dict]` (part local frame)

### checks.py (group "harness")
- `run(harness, world, r, space, cfg) -> list[Finding]`; one function per check id:
  `harness.netlist, harness.route, harness.clearance, harness.rotating, harness.fastener, harness.bend,
  harness.exit_axis, harness.slack, harness.length, harness.ampacity, harness.connector, harness.pinch_lid,
  harness.exposure, harness.retention`; metrics `harness_mass_g`, `harness_length_mm`.

## Spec additions (all optional)

```json
"harness": {
  "auto": false,
  "settings": {"rotating_clearance_mm": 2.5},
  "terminals": {"wesc.motor": {"pos": [0, 9, 1], "axis": [0, 1, 0], "connector": "bullet_2mm_f", "roles": ["phase_a", "phase_b", "phase_c"]}},
  "nets": []
}
```
