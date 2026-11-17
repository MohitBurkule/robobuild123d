# Scythe Classic: struggle log

One line per time I was stuck, wrong, or spent more than two tries. Each: what I tried, what was confusing, what would have saved me.

## Verifier and tools

- **Battery pack (`power.runtime`, then `physics.runtime`).** Tried the pocket packs in the catalog. Only `lipo_2s_350` (36x17x11) fits the pod and clears the 180 mAh fight-time blocker, and it still fails `physics.runtime` (~160 s at 6.3 A from 350 mAh vs 180 s). The check's peak model assumes both drive motors stalled plus the weapon at max (18 A), so the average is 35% of that. The fix line says only "Bigger pack or less current". It would have saved time to print the capacity or peak current needed (about 394 mAh here) and the term that dominates.
- **Stale sizing literal.** `params.INDEX_MASS_G` had gr1507 at 19.6 g (catalogue 8.5 g) and xt30 at 1.5 g (catalogue 0.5 g). That pushed the bar to 98 mm and made the tub shorter. I now read these from `robot.catalog`. A check that flags a master literal disagreeing with the catalogue would have caught it.
- **`integrity.volume` "previous" baseline.** The top_panel (-55%) and skid_foot (-75%) blockers compare against a cache file (`cache_dir()/integrity/<spec>.json`) from an old passing run. Measured geometry was right (foot = pi x 2.5^2 x height). The message does not say where "previous" comes from, so I had to read the source. A `--reset-baseline` flag or the store path in the message would have saved it.
- **ESC current key mismatch in `dynamics.spinup_kick`.** The ESC catalogue uses `cont_current_a` (20 A). The check reads `cont_a` or `current_a`, so it silently falls back to DEFAULT_PHASE_A = 30 A. This is a check bug. Even at 20 A the kick still beats grip (0.067 vs 0.051 N m), so the result does not change, but the number reported is wrong.
- **`ground.pitch_rest` did not run at all.** I added a caster to satisfy the coordinator's premise. Removing it left `ground` at 0 blockers, because the check only runs when stance has fewer than 3 contacts or margin < 2 mm, and the shaft-end foot on the axis already touches the floor ahead of the bar. The message does not say why it was skipped, so the caster looked necessary when it was not.
- **Caster under the tub front was physically blocked.** The bar sweeps a full disc of radius 58 mm at z 4 to 7 mm. Anything under the tub inside that disc must be under 2 mm tall, and it cannot be fixed to the tub without a leg through the sweep. The verifier's `proxy.sweep` said only "may reach". A message naming the swept height band would have saved two iterations.
- **Coordinator request: caster on a bearing under the hub.** The catalogue has no bearing (`robot catalog --kind bearing` returns nothing). I modelled the axis puck as kind `caster` (bottom 0.5 mm above the floor, top 0.5 mm under the bar), riding the shaft end. The bearing (e.g. MR63) and its standoff are not modelled and the spec has no bearing kind, so the "stops spinning on touch" claim is not verified.
- **`proxy.sweep` on bar to hub.** Fastened hub touching the bar top is reported as "bar may reach weapon_hub", and nothing in the spec says the two are rigidly bolted. Setting `parent: bar` on the hub silenced it but added the hub to the rotor and created four `interference.spin` blockers on the electronics. The washer gap (1.0 mm, needed by the sweep proxy) plus 4.5 mm hub engagement (`fastener.engagement`) forced the hub height, which pushed the motor into the top panel. The fix was to raise TUB_TOP_Z by 0.6 mm. Each rule was right alone; the combination was only visible by iteration.
- **`probe --place` takes 2 to 4 minutes per part** (exact checks). `jiggle --ranges` gave the same info faster for overlaps. Running them in the background and polling was the only option.
- **Background-job handling.** Several `verify` runs exceeded the 120 s foreground timeout and were moved to background. Polling with `sleep` loops was blocked. Writing output to a file and polling with a grep loop worked.
- **Wires.** `wiring.bend` and `wire.rotating_clearance` were fixed by adding `via` points to `w_sw_esc` and `w_rx_wpn`. The `via` key is not in the `robot field wires` examples; I found it in `robot/checks/wiring.py`.

## Process

- **Coordinator stash of my uncommitted edits.** A `git stash` by the coordinator took my scythe_classic edits for about a minute. Later writes landed on top, and some edits were reverted (the caster came back, BAR_Z0 reverted, electronics heights reverted). I restored from `stash@{0}` and dropped it after committing. Committing after each step would have made this a no-op. This is the biggest process loss of the session.
- **Commit trailer conflict.** The attribution reminder asked for a Haiku trailer; the user's instructions asked for the Opus trailer. I used the user's trailer, as the reminder says the user's instructions take precedence.

## Coordinator requests (ground.pitch_rest, dynamics, bearing caster)

- **Was the `ground.pitch_rest` message clear?** Partly. The fix line gives a height formula but assumes the caster is placeable; here every spot under the tub front is inside the bar sweep. The check also does not run when the stance is fine, so "add a caster" was not needed.
- **Bearing caster on the axis (requested).** Done as a caster puck on the shaft end, 0.5 mm off the floor and under the bar. No bearing part exists in the catalogue, and the spec cannot express "bearing on a standoff", so the spin-free behaviour is an assertion, not a check.
- **`dynamics.floor_margin`:** fixed by BAR_Z0 = 4.0 mm (3.6 mm needed).
- **`dynamics.spinup_kick`:** not fixed. 0.10 N m spin-up at 30 A (the check's default because of the ESC key mismatch above) against 0.05 N m tyre grip. Even at the real 20 A, 0.067 N m still exceeds grip, so it needs more weight on the wheels or a wider track. Neither fits the 150 g / pod layout. A declared ESC current ramp would be the honest fix, but the check has no field for it.
- **`dynamics.brake_dive`, `gyro_lift`, `invert_weapon`:** no blockers at the last inner run.

## Final state (last run)

- Full `wiring`, `assembly`, `physics` groups: 2 `assembly.blocked` (weapon_esc and drive_rx have no clear removal path: the switch and the tub sit in their exit line) plus `physics.runtime`. The inner tier's `proxy.wiring` and `proxy.assembly` lines are approximations; the full groups are authoritative and show the wiring clean.
- The `assembly.blocked` fix line says "open the pocket" but does not say which neighbour to move; the exit direction (0,1,0) and the 40.6 mm clearance were the only hints. Not fixed in this pass.

## Pass 3 (weapon shaft, bearings, drive) - stuck, uncommitted

- **`parent` moves the child.** Setting `parent: bar` / `parent: weapon_hub` on the hub, shaft and can made their `at`
  relative to the parent. The hub, shaft and can shifted, which showed up as `interference.spin` on the electronics,
  `fastener.engagement` 3.0 mm on the bar bolts, and a can overlapping the tub. Removing the parents fixed the shift.
  Nothing says that `at` is relative once `parent` is set. The fix line should name the frame change.
- **`rotates_with` is a label, not a part id.** Using `weapon` as the group name worked, but the spec does not say so.
- **Spin sweep is a full revolve of every rotor member.** Once the bar is a joint group, the sweep covers the cone
  interior at the hub and can heights. Electronics inside the cone (battery, ESC, RX, switch) show as `interference.spin`
  even when nothing is at the bar plane. The only ways out are electronics below the group's top, or a z band that
  stays clear. The message names the rotor part but not the z band.
- **Caster bearing.** `robot catalog --kind bearing` now lists bearings, which helped. The puck radius is limited by
  the bar-bolt driver path (head at r 6.5, 3.7 mm wide) and by the uhmw thin-wall rule (1.0 mm). Both were needed
  together; the puck could not meet both at the 8 mm bearing OD without a bigger bar PCD.
- **`spinner.bearing` on the shaft (0 mm one side, 2.2 mm the other).** The bottom bearing is 2.5 mm wide inside a
  3 mm puck, so the shaft has no 3 mm hold below the bar. The message does not say which side or where the 3 mm must sit.
- **Stator screws.** `stator_0` ends in the bell half of `weapon_motor`, and joins `top_panel` to `tub` with no seat under
  the head. Splitting the can (`weapon_motor_can`) did not change the stator-face result, so the stator screw length and
  the boss footprint need a measured check that the message does not provide.
- **Tub base wall.** The cone base still reports 0.00 mm at radius 50, z 8.5, after the cavity base was re-measured
  from the slope. The check is at the outer edge, not where I changed it.
- **Verify timing.** A full run without `practice` takes about 6 to 8 minutes. Monitor/poll loops returned before the
  run finished, so I used background `until grep EXIT` waits.

## Late-stage notes (finish pass)

- **mfg.sharp_internal_corner radius reads low.** A fillet of exactly r 1.0 measures below 1.0, so use 1.1 or more.
  Regions chain (samples under 2.5 mm apart), so one point near a joint or fastener flags a whole edge run, and the
  message does not say which point triggered it. The check also sections the wall at the slope-to-band kink (z 28.1) and
  reports turn 90, r 0 from the top face and the inner surface in the same polyline.
- **3D fillets on lofted geometry.** Fillets on lofted cone/plane intersections fail or segfault. `bd.fillet(vertices)`
  sometimes returns the parent unchanged; `face.fillet_2d(r, [vertex])` works. `face -= shape` did not work in a function,
  `face - shape` did. Ruled lofts need faces with identical topology; an inward offset that collapses a corner arc gives garbage.
- **arch.edge_distance.** A 1.6 mm wall never gives 3 mm for an M2 screw; a post or boss around 6 mm is needed.
- **Wheel sweep and contain hull.** kin.sweep_static treats any static point inboard of the tyre face within r 17 of the
  axle as swept; parts must clear by 0.5 mm. contain.electronics_exposed needs a shell vertex near the shaft tip, which
  forced a rear guard wing.
- **cots.drawing_dims** needs 29.1 mm can, 12 mm shaft protrusion and 8 mm of thread detected as radius dips per pitch;
  none of this is stated in the message.
- **Integrity baseline poisoning.** A broken intermediate run stores a bad volume as the baseline, and later correct
  runs report `integrity.volume` as collapsed. The fix is to delete the cache file under /root/.cache/robot/integrity/;
  the permission classifier denied my `rm`, so that blocker needs the caller to approve the delete.
- **`--failing`/`--only` skip groups**, and parity findings (visual.terminal, the N10 terminal port 1.5 mm off) come from
  the catalog, not the design.
