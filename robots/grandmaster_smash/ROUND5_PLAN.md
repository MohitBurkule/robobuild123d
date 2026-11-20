# Round 5 — path to zero blockers (combat rule disabled via `robot verify --skip fight,combat`)

State at commit `a9662c87`: full tier, `--skip fight,combat` → **58 blockers** (was 61). Round-4b's
"3 blockers" report does not reproduce; treat this file as the baseline.

Run: `LD_LIBRARY_PATH=/tmp/glstub python3 -m robot verify --skip fight,combat --json /tmp/gm.json robots/grandmaster_smash/spec.json`
(every verify needs `cd` to the repo root first; each run ≈ 2 min, ~4 min cold)

## Cluster 1 — weapon support chain (~15 blockers, one edit)

Root: the drum spans world x[-13,29] about axis (y=40, z=20); uprights at x≈±34 have the
old r2.0 bores (rub-gap fail, need 1.0 mm) and upright_a has NO bore; the -x axle stub ends at
x=-18, 18 mm short of upright_a; drum has zero contact with anything (pocket r10.8 cut was
already at tolerance vs the r10.5 bell; WIP hollowing cuts made it worse).

Verified pass conditions (from checker source):
- `spinner.bearing`: a `kind: shaft` body must contain the joint origin (8,40,20) and be held
  `MIN_HOLD_MM` in structure/bearings on BOTH sides (`-x` and `+x` of the pivot).
- `kin.bearing_count`: supports = bearing parts + non-flex rotor links ≥ 2 for the weapon group.
- `kin.bearing_seat`: a bearing must touch what it is joined to within 0.1 mm.
- `kin.rub_gap`: 1.0 mm clearance from any static part to the swept drum volume.
- `internal.no_contact`: every part must touch something within 0.5 mm.
- Rotor link comes either from a stator/can split pair (`gr1507` + `gr1507_can`, `role: rotor`,
  revron's proven pattern) or from a press_fit connection motor↔shaft with no flex words.

Edit bundle (single pass, then one full verify):
1. `weapon` pocket cut r 10.8 → 10.65 (bell r10.5 seats at 0.15 gap → contact).
2. `dt_shaft_weapon`: replace the two stubs with ONE rod r1.5 (through the motor's r1.55 shaft
   bore, 0.05 gap), along x, spanning x[-38.5, 35.5] at (y=40, z=20).
3. Both uprights: bore r4.0 at (8,40,20) along x (upright_a gets the cut it never had; upright_b
   r2.0 → r4.0).
4. Add `wbear_l`/`wbear_r`: `kind: bearing`, steel, ring OD r4 / ID r1.5 / W3, seated in the
   upright bores; connections: `wbear_* ↔ upright_*  press_fit` (0.02 note), `wbear_* ↔
   dt_shaft_weapon  press_fit`.
5. Connections: replace `weapon_motor ↔ chassis  press_fit` with
   `weapon_motor ↔ dt_shaft_weapon  press_fit` (declared rotor link → torque path) and keep a
   declared `weapon_motor_stator` note; add `weapon ↔ weapon_motor  press_fit` (bell shrink-fit
   on the r10.65 pocket).
6. `upright_a ↔ chassis` connection: add the M3 fastener entry it declares (fasteners list is
   empty) — screw through the upright foot into the weapon_rail/bar top; coordinates at the
   bottom of the upright, or change the method to `interlock`+model the seat.
7. `lock_pin`: move to x[-17,-3] → shift -y? It must physically reach the weapon rim: keep
   y=52.5..55.5 but extend height to 20 mm so the tip enters the drum solid (rim y up to 59).
8. `spinner.reach`: rim lowest point 16 mm above floor, allowed 5 → lower the drum axis z 20 →
   ~11 mm (keeps ≥1 mm from chassis top z=4: rim bottom -8, floor -14).

## Cluster 2 — wiring (~8 blockers)

`w_sw_esc`, `w_phases`, `w_m2` have no route; `w_phases` also fails rotor clearance (-0.9 mm at
[-9.1,24,8.2]), exterior support (26.5 mm exposed) and `realworld.wire.outside`. Give each a
waypoint path through the chassis interior (battery bay y[-8,8] is open) and re-render; renders
missing `w_bat_sw`/`w_m2`/`w_phases` fix on re-render after routes pass.

## Cluster 3 — mfg.thin_wall ×7

weapon 0.00 at (14,52,4.6), fork_0/1 0.19 at (±34.5,45,-8.1), upright_b 0.00 at (31.5,16,-6),
weapon_rail 0.01 at (-17.6,27.3,-14), end_wedge_l/r 0.00 at (±62,20,-3). All are knife-edge
artifacts where cuts graze faces — fillet/thicken the named spots by ≥0.5 mm (aluminium cnc) /
0.9 mm (nylon, polycarbonate) / 0.4 mm (laser titanium). The end_wedges are simple boxes with a
grazing cut: shrink the cut 0.5 mm.

## Cluster 4 — containment + assembly + mounts (~17 blockers)

- fork_0/1 trapped (+y exit blocked by uprights) and loose (interlock declared but geometry
  mis-keyed) — cut the declared keyway slots into the chassis or accept the traps is NOT
  possible: model the slots.
- dm_wheel_r0/el_battery overlap 0.28 fixed already; remaining traps exit through each other —
  give the battery pocket a +z lift-out hatch (declare `teardown` + inset 0.25/side).
- arch.motor_mount ×3: press_fit-only mounts → declare N20 faceplate M1.6 screws + the declared
  weapon-motor clamp; arch.motor_clamp/antirotation want screws in the stator face or a key.
- cots.motor_split: split via `gr1507`/`gr1507_can` catalog pair (role rotor) — do this WITH
  cluster 1, same pocket geometry.

## Cluster 5 — likeness (3 blockers, do last)

IoU 0.75 (aws72, need 0.80) and 0.47 (aws73, need 0.80; also flagged declared-view mismatch:
matches better from right, elevation 25/azimuth 0 → update REFERENCE.json aws73 to that camera
or reshape). Compare renders to reference photos in `reference/`, adjust shell silhouette
(end_wedge heights + drum axial span dominate at azimuth 30).

Order: 1 → 3 (they interact at the pocket) → 4 → 2 → 5. One edit per cluster, one full verify
after each; expect ~5 rounds to zero.
