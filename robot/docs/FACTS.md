# Verifier facts: look these up, do not re-derive them

Small models spent most of their thinking re-deriving how the verifier behaves and doing coordinate maths by
hand. Everything below is how the code behaves, and each line has a tool that gives you the number.

## The loop
`python3 -m robot verify spec.json --tier inner --llm` while iterating: it takes seconds, prints only root causes
with numbers, and needs nothing else. Run the full tier (`--llm` without `--tier`) before you call it done.

## Automatic in every `verify` (nothing to remember)
- ROOT CAUSES come first. Each one carries measured context: its parts' world boxes, ports, and gap or overlap
  to each neighbour. That is what `probe` would print.
- Each overlap blocker lists the smallest measured fix.
- A MASS BUDGET (grams per part, solid-block warning) appears whenever a mass check fails.
- If the spec declares `"levers"` (named masters) and collisions remain, verify runs jiggle itself and reports
  `solve.proposal` with the master values to apply. It never applies them for you. Add `"generator": "make_spec.py"`
  when spec.json is generated from params.
- Off switches: ROBOT_AUTOHELP=0 turns everything off; ROBOT_AUTOJIGGLE=0 turns off only the auto-jiggle.

## Measure, don't compute
| Question | Command |
|---|---|
| Where is a part, how big, what touches it, its ports in world | `python3 -m robot probe spec.json <part>` |
| Does a joint sweep hit anything, and where | `python3 -m robot probe spec.json --joint <part>` |
| Where can a part go (battery/ESC/rx packing) | `python3 -m robot probe spec.json --place <part>`: best spots + SAFE RANGES (x/y intervals, a box where every combination is clear, the free polygon incl. diagonals, z range). Verify prints these itself for packed parts in a collision. Ranges assume the other parts stay put. Never pack boxes in your head |
| Which values of a named param are safe (moves linked parts together) | `python3 -m robot jiggle spec.json --ranges` (uses spec `levers`, or `--param FILE:NAME=lo:hi`; add `--regen make_spec.py` if the spec is generated): clean interval per lever, others unchanged |
| Why is a motor "not captured" | the arch.motor_clamp message lists all 6 sides, what holds each and what to add |
| Button/pan head `at` | the bearing face = the outer surface (no counterbore). `robot.cad.holes.hole_tool(at=surface)` returns `rec.at`: put rec.at in the spec |
| What is at a world point (e.g. a finding's `at`) | `python3 -m robot probe spec.json --at x,y,z` |
| Smallest move that clears an overlap | in the overlap blocker text ("Smallest fixes (measured)") |
| Solve layout variables so collisions clear | `python3 -m robot jiggle spec.json --param params.py:NAME=lo:hi:step [--regen make_spec.py]` |
| Servo horn + pin for a push-only flipper/lifter | `robot.cad.linkage.pusher_crank(...)` (gives the pin, horn radius and a clean joint range) |
| A bay that does not eat the floor | `derive_bay(entry, insert_dir="-z", seat="-z")`, place at `floor_z + seat_offset(bay)` |
| Which blockers are one problem | the `ROOT CAUSES` block at the top of `verify` output |

## Check semantics
- **Touching is fine.** An overlap counts as a collision only when deeper than `contact_tol_mm` = 0.08 mm
  (robot/profile.py), or deeper than its `allow_overlap` max_depth_mm. Depth means the radius of the largest
  ball that fits inside both parts, not the box overlap.
- **Joints are swept one at a time**, with every other joint at its default pose (interference.joint_sweeps,
  3 deg steps, at most 80 poses). Combined motions are not swept. A pin linkage is clean when each sweep
  clears on its own: put the pin beyond the driven bar's end, as `pusher_crank` does.
- **A flat bar end turns on its corner radius** hypot(length, half thickness), not its length. A 19.9 x 5.2 bar
  reaches 20.07 mm.
- **Children move with their parent** (`parent`). A joint rotates about `pivot` in the parent frame. Build a
  moving part in world coordinates at rest, then give it `at` [0,0,0] and joint `default` 0.
- **Connection methods**: screw, shaft, pin, press_fit, glue, tape, snap, interlock, velcro, none
  (checks/connections.py). A press fit needs real interference plus a matching `allow_overlap`.
- **Ground**: the wheels must be the lowest points (contain.wheel_ground). Ground clearance must be at least 1.0 mm,
  and moving parts need at least 0.4 mm of clearance (profile).
- **Cache**: part geometry is keyed on the content of the model file, everything it imports, every .py next to it,
  and active param overrides. A stale part after editing code is a bug: report it. Don't work around it.
- **Memory / OOM**: `ROBOT_JOBS=1` builds parts in one process. Use `verify --only g1,g2` to bisect which group
  blows up, and `--fast` while iterating.

## Habits that save tokens
1. Read ROOT CAUSES and fix those first. The consequences go away with them.
2. Before changing a number, `probe` the part. After changing it, `probe` again. Do not simulate it in your head.
3. Write placement as relations of masters (spec `"params"` and `"at": ["P.x()", ...]`) so jiggle can move a
   part together with its pocket and holes.
4. If a mechanism needs more than a few lines of geometry reasoning, look for a solver in robot/cad/ (bay,
   linkage, mates, holes, fit, seat) or add one there. Don't reason it out in a trace.

## Frames and ids (second trace, Undertow)
- **`at` places the part's frame origin, not its corner.** Catalogue frames: packs and boards are centred on the
  origin (lie long side on X). Motors and wheels have the origin on the shaft axis, with the shaft on +X.
  A battery resting on a floor at z=F goes at z = F + half its height. Use `seat_offset(bay)` or
  `probe spec.json battery`, which prints its box.
- **Ids must match the lists exactly.** Materials: `python3 -m robot materials` (e.g. `titanium`, not
  `titanium_gr5`). Processes: fdm, sla, laser/waterjet (sheet_cut), sheet_bent, turned, milled, cots, molded,
  cast. The blocker now suggests the nearest id.
- **Mass budget**: `python3 -m robot probe spec.json --mass` gives grams per part and flags parts that fill
  most of their box (a tub built as a solid block instead of a shell).
- **TPU chassis is a blocker** (arch.tpu_structural): an elastomer part that is the chassis, or that holds other
  parts, fails. TPU is fine for skins that hold nothing. Make the tub nylon/PLA and use TPU for skins.
- **Reference spec**: robots/revron/spec.json passes the gate. Copy its structure (fasteners with hole
  records, wires, connections, electronics, claims) instead of guessing field names.

## Joins, fasteners, wires (third trace, flipper)
- **Rigid groups are a union-find over holds**: screws (through + threads_into), connections with methods
  screw/pin/press_fit/glue/tape/snap/..., `fused_with`, and a child without its own joint. One hold chain from a
  moving part to the tub makes the whole robot one rigid group and triggers dozens of kin.* blockers. The
  kin.rigid_mix and kin.motion_declared messages print the chain (`via a -> b -> c`). A hinge pin that the moving
  part turns on is an axle: declare that connection as `method: shaft`.
- **Fastener `at` is the bearing face of the head, on the outer surface of the first `through` part.** `dir`
  points into the joint (the shank runs along +dir from `at`). Socket and button heads sit behind `at`. A
  countersunk head is a cone flush with the surface at `at`, and the ISO length is the overall length.
  Engagement in printed plastic should be at least 2.5 d; otherwise use a heat-set insert part.
- **Ports in world**: `probe spec.json <part>` lists every port's world position. Never transform catalogue ports
  by hand.
- **Placement collisions**: overlap blockers name both parts and give the smallest measured move. Before you
  place a part, `probe spec.json --at x,y,z` shows what already occupies that point.
- **Wires**: give `via` points. Check each via point with `probe --at` (it must be free). Keep runs outside a
  rotor's swept band along the joint axis.
- **Electronics and wires must be shielded from every side** (contain.line_of_sight): an open window over the
  battery or wires is a blocker, even when they sit inside the chassis outline.

## Generator body shape (`robot gen build --intent`)
- `shape`: box (default) | oval | round. Round = circle through the default box corners, radius <= 74 mm (150 mm square rule).
- `taper` mm or `profile` [[t, inset_mm]]: sloped walls (cone, dome). Shell = ruled loft of the outline shrunk at each height, resampled to 72 points.
- Layout uses the smallest section, so parts never cut through a sloped wall. Too much taper = `no wireable layout`.
- Spec: robot/gen/INTENT.md.

## Look it up, don't guess (small-LLM aids, 2026-11-17)
- `robot field NAME`: real examples of a spec field from verified specs (Revron first) + the checks that read it. No name = every key.
- `robot catalog --kind battery --fits 40x20x12 --max-mass 15 [--sort capacity_mah]`: catalogue parts that fit a measured box (any yaw). Feed it the box from `probe --place`.
- `fit.interference` now says the measured move: "move `X` +0.6 mm along y (1.5 mm free that side)", or that no side has room (then grow the pocket or pick a smaller part).
- Keep spec.json generated from the CAD masters (a `make_spec.py` next to it); hand-edited `at` values go stale when a master changes.

## ground.pitch_rest (2026-11-17)
- Runs when the support polygon is < 3 contacts or the COM is < 2 mm inside it (2-wheel robots).
- Pitches the robot about the wheel contact line toward the COM; the first body to touch the floor is the rest contact.
- Weapon/hub/weapon_motor first = BLOCKER (blade grinds floor); fix gives the max skid height at a distance: h <= s x tan(angle) - 0.5.
- Plain structure first = WARNING (drags). Give floor-touching parts kind `skid` or `caster` (ball caster) so they count as support.

## Spinner-in-motion checks (dynamics group, robot/checks/spin_dyn.py)
- `dynamics.brake_dive`: braking/accel at 1 g shifts the COM by its height; the pitch first-contact must not be the weapon (BLOCKER).
- `dynamics.spinup_kick`: weapon motor torque Kt*I (Kt = 60/(2 pi kv), I = ESC rating or 30 A) vs tyre grip (vertical axis: yaw) or weight x lever (horizontal axis: rock/hop).
- `dynamics.gyro_lift`: horizontal-axis spinner, 15 rad/s turn: I w Omega vs weight x lever; lifts a wheel.
- `dynamics.floor_margin`: weapon rim within 10 mm of the floor must clear 0.5 mm tyre squash + 3 deg floor seam over its reach.
- `dynamics.invert_weapon`: if `can_run_inverted`, the weapon must not be the highest point (it would rest on it).
- A spinning weapon within 2 mm of the floor no longer counts as a floor contact in traction/tip checks.

## craft group (designer red flags, inner tier)
- `craft.stray_part` BLOCKER: a part > 0.5 mm below the floor or > 15 mm outside the structure box (weapons, wheels, wedges, skids exempt).
- `craft.brick`: printed structure part > 60% of its bounding box (shell + rib it).
- `craft.sharp_edges`: main body only; share of convex silhouette edge length with >= 60 deg corner > 60% (Revron tub 39%, block-out tubs ~100%).
- `craft.weapon_scale`: spinner swept diameter < 0.6 x body width.
- `craft.flat_slab`: 3-8 mm solid plate > 1500 mm2, > 85% solid.
- `dynamics.blade_wobble`: 30% of impact out of plane bends the blade (cantilever from hub, E from material) + 0.3 deg shaft tilt; free span must clear floor and non-rotor parts along the spin axis by wobble + 0.5 mm.
