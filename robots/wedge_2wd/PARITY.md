# wedge_2wd: Python (build123d) vs Rust parity

Python report: `robots/wedge_2wd/report.json` (check set revision 8, engine build123d, run on the **fixed** spec).
Rust report: `/home/user/mohitburkule/robocadcraft/robots/wedge_2wd/report.json` (run on the **original** spec).

Both: `ok = true`, 0 blockers, 0 warnings, 24/24 passed, and the same finding ids in the same order.

## Spec changes made to clear the Python verifier

The Python verifier found 3 blockers and 1 warning on the original template. Rust missed all of them. Each one is a real flaw:

| Finding on the original spec | Cause | Fix in `robot/templates/wedge_2wd.json` |
|---|---|---|
| `mfg.thin_wall` chassis_bottom 0.10 mm at (5.5, 17.5, -0.3) | The battery-pocket cut ends at y = 17.4. The 17x3 wire-channel cut starts at y = 17.5, leaving a 0.1 mm skin. | Moved the channel centre from y 19.0 to 18.9 so it merges into the pocket (both shell halves). |
| `mfg.thin_wall` chassis_top 0.10 mm at (12.0, 17.4, 0.2) | Same cut, mirrored into the top half. | Same move. |
| `mfg.thin_wall` 0.30 mm at x≈14.4 (showed up after the first fix) | The battery pocket ends at x = 14.4. The 3.6x26 vertical channel at x = 16.5 starts at x = 14.7. | Moved the channel to x = 17.5 (15.7 to 19.3), giving a 1.3 mm wall. Widening it into the pocket instead opened the pocket side and caused `retention.loose` on the battery. |
| `connection.floating` esc (1.5 mm from chassis) | The ESC (15x10x5) sat at z = 0 in an 18x13x9 cavity, with a 2 mm gap above and below. Its tape had nothing to stick to, and Python's captive test (1.5 mm side play) does not count it as held. | Lowered the ESC to z = -2.0 so it sits on the pocket floor, where the tape bonds. |
| `validity.self_intersecting` warning on wedge | The seven rib prisms had a closing edge, (36,-10)→(36,-1.61)→(35.52,-1.61), that crosses the first edge. | Removed the redundant last point. The outline is now a simple quad. |

## Findings

| Finding | Rust | Python | Explanation |
|---|---|---|---|
| validity.ok | 17 parts, 6 fasteners, 5 wires | same | identical |
| wiring.route | 5 wires, 257 mm | 5 wires, 257 mm | routes agree to 0.1 mm (256.98 vs 256.87) |
| mass.ok | 106.0 g (87.0 to 125.0) | 105.8 g (86.8 to 124.8) | The fixed spec removes slightly more chassis material. Python B-rep volume is also exact where Rust used a mesh. |
| interference.overlap | 40 pairs | 38 pairs | The candidate-pair AABB pruning differs. The ESC moved, and Python prunes pairs whose AABBs are separated by more than the touch tolerance. No overlaps in either. |
| interference.sweep | no joints | same | identical |
| retention.declared x3 | esc, rx tape; switch adhesive | same | identical |
| retention.captive | 6 checked, 3 declared | same | identical |
| connection.joined | all 17 parts | all 17 parts | On the original spec Python flagged the ESC as floating; the fix is above. |
| ground.wheels_touch | z = -14.00 | same | identical |
| ground.clearance | 4.0 mm | 4.0 mm | identical |
| ground.wedge_gap | 0.64 mm | 0.60 mm | Python measures the tip on the exact B-rep; Rust used a tessellated hull (chord error of about 0.04 mm). |
| ground.stance | 20.3 mm | 20.0 mm | follows the CoM shift (see metrics) |
| legal.switch | pass | pass | identical |
| switch.recess | 1.0 mm | 1.2 mm | Python measures the surrounding surface by ray hit on the exact solid; Rust used voxel or mesh sampling. Both are well above the requirement. |
| legal.failsafe / legal.footprint | pass, 122.5 mm | same | identical |
| fastener.ok | 6 screws | 6 screws | identical |
| power.battery | 0.7 A / 7.2 A | same | identical |
| mfg.walls | 3 parts | 3 parts | Same pass now. Python's thickness sampler found the 0.1 mm skins that Rust's missed. |
| assembly.order | same order | same order | identical sequence |
| claim.holds x2 | pass | pass | identical |

## Metrics

| Metric | Rust | Python | Δ / note |
|---|---|---|---|
| mass_total_g | 105.97 | 105.81 | -0.16 g: chassis cuts changed, plus B-rep vs mesh volume |
| mass_lo_g / mass_hi_g | 86.95 / 124.99 | 86.82 / 124.79 | same cause |
| part_mass_g.chassis_bottom | 22.61 | 22.53 | moved and enlarged channel merge |
| part_mass_g.chassis_top | 22.20 | 22.11 | same |
| part_mass_g.wedge | 13.430 | 13.437 | the rib sliver is no longer even-odd filled |
| part_mass_g.bolt_* | 0.5733 / 0.3257 | 0.5726 / 0.3260 | thread or head tessellation vs exact (<0.2 %) |
| catalog parts (battery, esc, motors, rx, wheels, inserts, switch) | — | — | identical |
| com_x / com_y / com_z | -0.327 / 3.931 / -0.548 | -0.304 / 3.990 / -0.606 | The ESC was lowered 2 mm and the chassis mass changed. |
| stance_margin_mm | 20.33 | 19.99 | follows CoM |
| tip_angle_deg | 56.51 | 56.18 | follows CoM height |
| wedge_load_frac | 0.2068 | 0.2040 | follows CoM |
| footprint_mm | 122.484 | 122.484 | identical |
| ground_z / min_ground_clearance_mm | -14 / 4.0 | -14 / 4.0 | identical |
| peak_current_a | 0.65 | 0.65 | identical |
| wire_length_mm / wire_mass_g | 256.87 / 0.5643 | 256.98 / 0.5646 | +0.1 mm route difference |
| min_wall_mm | 0.5 | (absent) | Rust records the global minimum sample, even a sub-cluster sliver. Python records the metric only when a below-limit wall sample exists, and on the fixed spec there is none. |

## not_checked

Both list the same 6 standing items. Python adds 5 export-time notes: `STEP export of wire:*: no B-rep (tessellated-only body) (STL only)`. The wire tubes are mesh sweeps, so they go into the STLs but not into `step/assembly.step`.

## Export

`python3 -m robot export robot/templates/wedge_2wd.json wedge_2wd robots` wrote 61 files, 5.0 MB in total. The largest file is `step/assembly.step` at 1.4 MB. No STL is over 20 MB.
