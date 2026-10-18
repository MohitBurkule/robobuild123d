# Verifier report: Revron

Profile `aws2025`. 0 blockers, 158 warnings, 271 checks passed. Check set revision 10 (engine build123d).

Mass 146.8 g (range 127.3 to 166.2 g, limit 150 g).

## Findings

- **pass** `validity.ok`: Spec is well formed 70 parts, 21 fasteners, 7 wires.
- **warning** `wiring.bend`: Wire bends too tightly Wire `w_sw_wesc` turns 45 degrees with less than 3.8 mm bend radius; it will kink or pull off its solder joint.
  - Fix: Widen the channel at the corner or route it in a straighter line.
- **warning** `mass.may_be_over`: May be over the weight limit 146.8 g (range 127.3 to 166.2 g) against the 150 g limit; 8.8 g of the uncertainty is catalog estimates, weigh the real parts and set `scale_mass_g`.
  - Fix: Weigh real parts and set `scale_mass_g`, or remove mass until the upper bound fits.
- **pass** `interference.overlap`: No parts collide 240 touching or overlapping pairs checked; touching is allowed, overlap deeper than 0.08 mm is not.
- **pass** `interference.sweep`: Joint sweep is clear `blade_c` swept 0..360 deg in 80 steps without hitting anything.
- **pass** `interference.sweep`: Joint sweep is clear `whub_fl` swept 0..360 deg in 80 steps without hitting anything.
- **pass** `interference.sweep`: Joint sweep is clear `wbrg_l0` swept 0..360 deg in 80 steps without hitting anything.
- **pass** `interference.sweep`: Joint sweep is clear `whub_fr` swept 0..360 deg in 80 steps without hitting anything.
- **pass** `interference.sweep`: Joint sweep is clear `wbrg_r0` swept 0..360 deg in 80 steps without hitting anything.
- **warning** `interference.spin_clearance`: Spinning weapon has almost no clearance `blade_i` is within 0.4 mm of the sweep of `blade_c`; bearings, flex and hits will make them touch.
  - Fix: Leave at least 1 mm between a spinning weapon and anything fixed.
- **warning** `interference.wheel_clearance`: Wheel has no running clearance `wheel_fl` turning about its axle comes within 0.00 mm of `motor_l`; it needs 1.0 mm so tyre squash, flex and debris do not make it rub.
  - Fix: Open the wheel pocket so it clears the wheel by 1 mm on every side (radius and both faces).
- **warning** `interference.wheel_clearance`: Wheel has no running clearance `wheel_fl` turning about its axle comes within 0.70 mm of `pod_l`; it needs 1.0 mm so tyre squash, flex and debris do not make it rub.
  - Fix: Open the wheel pocket so it clears the wheel by 1 mm on every side (radius and both faces).
- **warning** `interference.wheel_clearance`: Wheel has no running clearance `wheel_fl` turning about its axle comes within 0.25 mm of `pulley_fl`; it needs 1.0 mm so tyre squash, flex and debris do not make it rub.
  - Fix: Open the wheel pocket so it clears the wheel by 1 mm on every side (radius and both faces).
- **warning** `interference.wheel_clearance`: Wheel has no running clearance `wheel_fr` turning about its axle comes within 0.00 mm of `motor_r`; it needs 1.0 mm so tyre squash, flex and debris do not make it rub.
  - Fix: Open the wheel pocket so it clears the wheel by 1 mm on every side (radius and both faces).
- **warning** `interference.wheel_clearance`: Wheel has no running clearance `wheel_fr` turning about its axle comes within 0.69 mm of `pod_r`; it needs 1.0 mm so tyre squash, flex and debris do not make it rub.
  - Fix: Open the wheel pocket so it clears the wheel by 1 mm on every side (radius and both faces).
- **warning** `interference.wheel_clearance`: Wheel has no running clearance `wheel_fr` turning about its axle comes within 0.25 mm of `pulley_fr`; it needs 1.0 mm so tyre squash, flex and debris do not make it rub.
  - Fix: Open the wheel pocket so it clears the wheel by 1 mm on every side (radius and both faces).
- **warning** `interference.wheel_clearance`: Wheel has no running clearance `wheel_rl` turning about its axle comes within 0.00 mm of `axle_l`; it needs 1.0 mm so tyre squash, flex and debris do not make it rub.
  - Fix: Open the wheel pocket so it clears the wheel by 1 mm on every side (radius and both faces).
- **warning** `interference.wheel_clearance`: Wheel has no running clearance `wheel_rl` turning about its axle comes within 0.69 mm of `pod_l`; it needs 1.0 mm so tyre squash, flex and debris do not make it rub.
  - Fix: Open the wheel pocket so it clears the wheel by 1 mm on every side (radius and both faces).
- **warning** `interference.wheel_clearance`: Wheel has no running clearance `wheel_rl` turning about its axle comes within 0.25 mm of `pulley_rl`; it needs 1.0 mm so tyre squash, flex and debris do not make it rub.
  - Fix: Open the wheel pocket so it clears the wheel by 1 mm on every side (radius and both faces).
- **warning** `interference.wheel_clearance`: Wheel has no running clearance `wheel_rl` turning about its axle comes within 0.00 mm of `wbrg_l1`; it needs 1.0 mm so tyre squash, flex and debris do not make it rub.
  - Fix: Open the wheel pocket so it clears the wheel by 1 mm on every side (radius and both faces).
- **warning** `interference.wheel_clearance`: Wheel has no running clearance `wheel_rr` turning about its axle comes within 0.00 mm of `axle_r`; it needs 1.0 mm so tyre squash, flex and debris do not make it rub.
  - Fix: Open the wheel pocket so it clears the wheel by 1 mm on every side (radius and both faces).
- **warning** `interference.wheel_clearance`: Wheel has no running clearance `wheel_rr` turning about its axle comes within 0.69 mm of `pod_r`; it needs 1.0 mm so tyre squash, flex and debris do not make it rub.
  - Fix: Open the wheel pocket so it clears the wheel by 1 mm on every side (radius and both faces).
- **warning** `interference.wheel_clearance`: Wheel has no running clearance `wheel_rr` turning about its axle comes within 0.25 mm of `pulley_rr`; it needs 1.0 mm so tyre squash, flex and debris do not make it rub.
  - Fix: Open the wheel pocket so it clears the wheel by 1 mm on every side (radius and both faces).
- **warning** `interference.wheel_clearance`: Wheel has no running clearance `wheel_rr` turning about its axle comes within 0.00 mm of `wbrg_r1`; it needs 1.0 mm so tyre squash, flex and debris do not make it rub.
  - Fix: Open the wheel pocket so it clears the wheel by 1 mm on every side (radius and both faces).
- **warning** `retention.loose`: Nothing holds this part in place `wshaft` can move more than 0.5 mm toward +x, -x, +y, -y, +z, -z without touching anything (captive means at most 0.5 mm of play in every direction); in a hit it will fall out or rattle.
  - Fix: Make the pocket snug on that side (0.2 to 0.5 mm gap), add a retaining rib or strap, or declare how it is held in `retained` (tape, adhesive, velcro, press_fit).
- **warning** `retention.loose`: Nothing holds this part in place `wnut0` can move more than 0.5 mm toward -x without touching anything (captive means at most 0.5 mm of play in every direction); in a hit it will fall out or rattle.
  - Fix: Make the pocket snug on that side (0.2 to 0.5 mm gap), add a retaining rib or strap, or declare how it is held in `retained` (tape, adhesive, velcro, press_fit).
- **warning** `retention.loose`: Nothing holds this part in place `wnut1` can move more than 0.5 mm toward -x without touching anything (captive means at most 0.5 mm of play in every direction); in a hit it will fall out or rattle.
  - Fix: Make the pocket snug on that side (0.2 to 0.5 mm gap), add a retaining rib or strap, or declare how it is held in `retained` (tape, adhesive, velcro, press_fit).
- **warning** `retention.loose`: Nothing holds this part in place `wnut2` can move more than 0.5 mm toward -x without touching anything (captive means at most 0.5 mm of play in every direction); in a hit it will fall out or rattle.
  - Fix: Make the pocket snug on that side (0.2 to 0.5 mm gap), add a retaining rib or strap, or declare how it is held in `retained` (tape, adhesive, velcro, press_fit).
- **warning** `retention.loose`: Nothing holds this part in place `wnut3` can move more than 0.5 mm toward -x without touching anything (captive means at most 0.5 mm of play in every direction); in a hit it will fall out or rattle.
  - Fix: Make the pocket snug on that side (0.2 to 0.5 mm gap), add a retaining rib or strap, or declare how it is held in `retained` (tape, adhesive, velcro, press_fit).
- **warning** `retention.loose`: Nothing holds this part in place `wbearing` can move more than 0.5 mm toward -x without touching anything (captive means at most 0.5 mm of play in every direction); in a hit it will fall out or rattle.
  - Fix: Make the pocket snug on that side (0.2 to 0.5 mm gap), add a retaining rib or strap, or declare how it is held in `retained` (tape, adhesive, velcro, press_fit).
- **warning** `retention.loose`: Nothing holds this part in place `axle_l` can move more than 0.5 mm toward +x, -x without touching anything (captive means at most 0.5 mm of play in every direction); in a hit it will fall out or rattle.
  - Fix: Make the pocket snug on that side (0.2 to 0.5 mm gap), add a retaining rib or strap, or declare how it is held in `retained` (tape, adhesive, velcro, press_fit).
- **warning** `retention.loose`: Nothing holds this part in place `wbrg_l0` can move more than 0.5 mm toward -x without touching anything (captive means at most 0.5 mm of play in every direction); in a hit it will fall out or rattle.
  - Fix: Make the pocket snug on that side (0.2 to 0.5 mm gap), add a retaining rib or strap, or declare how it is held in `retained` (tape, adhesive, velcro, press_fit).
- **warning** `retention.loose`: Nothing holds this part in place `wbrg_l1` can move more than 0.5 mm toward +x without touching anything (captive means at most 0.5 mm of play in every direction); in a hit it will fall out or rattle.
  - Fix: Make the pocket snug on that side (0.2 to 0.5 mm gap), add a retaining rib or strap, or declare how it is held in `retained` (tape, adhesive, velcro, press_fit).
- **warning** `retention.loose`: Nothing holds this part in place `axle_r` can move more than 0.5 mm toward +x, -x without touching anything (captive means at most 0.5 mm of play in every direction); in a hit it will fall out or rattle.
  - Fix: Make the pocket snug on that side (0.2 to 0.5 mm gap), add a retaining rib or strap, or declare how it is held in `retained` (tape, adhesive, velcro, press_fit).
- **warning** `retention.loose`: Nothing holds this part in place `wbrg_r0` can move more than 0.5 mm toward +x without touching anything (captive means at most 0.5 mm of play in every direction); in a hit it will fall out or rattle.
  - Fix: Make the pocket snug on that side (0.2 to 0.5 mm gap), add a retaining rib or strap, or declare how it is held in `retained` (tape, adhesive, velcro, press_fit).
- **warning** `retention.loose`: Nothing holds this part in place `wbrg_r1` can move more than 0.5 mm toward -x without touching anything (captive means at most 0.5 mm of play in every direction); in a hit it will fall out or rattle.
  - Fix: Make the pocket snug on that side (0.2 to 0.5 mm gap), add a retaining rib or strap, or declare how it is held in `retained` (tape, adhesive, velcro, press_fit).
- **pass** `retention.declared`: Held by declared method `battery` is held by press_fit.
- **pass** `retention.declared`: Held by declared method `rxesc` is held by velcro.
- **pass** `retention.declared`: Held by declared method `wesc` is held by press_fit.
- **pass** `retention.declared`: Held by declared method `power_switch` is held by press_fit.
- **pass** `connection.joined`: Every part is attached All 70 parts lead back to the chassis through screws, shared prints, captive pockets, joints or declared connections.
- **pass** `internal.solid_invalid`: Every part is a valid solid All bodies are closed, outward-facing manifolds.
- **pass** `internal.no_contact`: Every part touches something 70 parts each touch at least one other solid.
- **pass** `internal.fastener_void`: Screw shanks pass through parts 21 screws each run at least 40 % through drawn solids.
- **pass** `internal.wire_in_solid`: Wires stay in free space 7 routed wires sampled every 0.5 mm stay out of every solid away from their ports.
- **pass** `ground.wheels_touch`: Wheels touch the floor All 4 wheels reach the floor plane (z = -2.25 mm).
- **warning** `ground.clearance`: Body is close to the floor `bolt_b0` is -0.25 mm above the floor; it will scrape on arena seams and ride on the ground when a tyre compresses.
  - Fix: Raise the chassis or use a bigger wheel; wedges and forks may go lower.
- **pass** `ground.wedge_gap`: Wedge tip height is right `spike_l` tip is 0.30 mm above the floor.
- **pass** `ground.wedge_gap`: Wedge tip height is right `spike_r` tip is 0.30 mm above the floor.
- **pass** `ground.stance`: Stable on the floor Centre of mass is 37.2 mm inside the support polygon of wheels and wedge.
- **warning** `ground.wedge_load`: Front rests on the wedge About 35% of the weight sits on the wedge tip because the centre of mass is ahead of the axle; the tip drags and wears and the drive loses traction.
  - Fix: Move the battery and motors back, or add a front skid wheel, or put the axle forward.
- **warning** `ground.wheel_exposed`: Wheel sticks out of the body `wheel_fl` reaches open air from 18% of its side and upward rays above the belly line (allowed 5%); a spinner or a wall hits the tyre first.
  - Fix: Pull the wheel inside the outline, or add a side wall or guard over the exposed tread.
- **warning** `ground.wheel_exposed`: Wheel sticks out of the body `wheel_rl` reaches open air from 29% of its side and upward rays above the belly line (allowed 5%); a spinner or a wall hits the tyre first.
  - Fix: Pull the wheel inside the outline, or add a side wall or guard over the exposed tread.
- **warning** `ground.wheel_exposed`: Wheel sticks out of the body `wheel_fr` reaches open air from 17% of its side and upward rays above the belly line (allowed 5%); a spinner or a wall hits the tyre first.
  - Fix: Pull the wheel inside the outline, or add a side wall or guard over the exposed tread.
- **warning** `ground.wheel_exposed`: Wheel sticks out of the body `wheel_rr` reaches open air from 25% of its side and upward rays above the belly line (allowed 5%); a spinner or a wall hits the tyre first.
  - Fix: Pull the wheel inside the outline, or add a side wall or guard over the exposed tread.
- **pass** `legal.switch`: Marked tool-free power switch `power_switch` is a marked, tool-free power switch.
- **warning** `switch.drive_axis`: Switch slides along the drive direction `power_switch` moves forward and back: hard acceleration, braking and head-on hits push the slider.
  - Fix: Orient the slider across the robot (x axis), or add a detent plus a guard rib on both ends.
- **warning** `switch.too_deep`: Switch is buried `power_switch` is 6.0 mm below the surface; a finger cannot move the slider without a tool.
- **pass** `legal.failsafe`: Failsafe declared The robot stops when the transmitter is switched off.
- **pass** `legal.weapon_disable`: Weapon can be disabled remotely The weapon is switched off from the transmitter.
- **pass** `legal.locking_bar`: Removable weapon pin declared `blade_c`: a pin hole lines up through `upright_r`, `blade_o`, `blade_c`, `blade_i`, `upright_l` at [0.0, 41.9, 15.2].
- **pass** `legal.footprint`: Fits the square Fits a 115.7 mm square (limit 150 mm).
- **warning** `fastener.head_seat`: Screw head sits on nothing Nothing is under the head of `bolt_b0`; it cannot clamp the parts.
  - Fix: Move `at` to the surface the head presses on, or cut a counterbore whose floor is at `at`.
- **warning** `fastener.head_seat`: Screw head sits on nothing Nothing is under the head of `bolt_b1`; it cannot clamp the parts.
  - Fix: Move `at` to the surface the head presses on, or cut a counterbore whose floor is at `at`.
- **warning** `fastener.head_seat`: Screw head sits on nothing Nothing is under the head of `bolt_b2`; it cannot clamp the parts.
  - Fix: Move `at` to the surface the head presses on, or cut a counterbore whose floor is at `at`.
- **warning** `fastener.head_seat`: Screw head sits on nothing Nothing is under the head of `bolt_b3`; it cannot clamp the parts.
  - Fix: Move `at` to the surface the head presses on, or cut a counterbore whose floor is at `at`.
- **warning** `fastener.head_seat`: Screw head sits on nothing Nothing is under the head of `bolt_b4`; it cannot clamp the parts.
  - Fix: Move `at` to the surface the head presses on, or cut a counterbore whose floor is at `at`.
- **pass** `power.tip_speed`: Tip speed is legal 19320 rpm at 40 mm diameter is 91 mph (limit 600).
- **pass** `power.weapon_energy`: Weapon stores useful energy About 3.4 J at 85% of no-load speed.
- **warning** `power.battery`: Battery may sag under peak load Estimated peak 17.0 A against a 7.2 A rating (180 mAh x 40 C); the voltage will collapse in a hit.
  - Fix: Use a bigger or higher-C pack, or a motor that draws less.
- **warning** `mfg.thin_wall`: Wall too thin to make `base_panel` has walls down to 0.80 mm near (-22.8, -6.6, 0.3); fdm nylon needs at least 0.9 mm.
  - Fix: Thicken that wall to a multiple of the nozzle width (0.8, 1.2, 1.6 mm) or merge it into a thicker feature.
- **warning** `mfg.thin_wall`: Wall too thin to make `upright_r` has walls down to 0.80 mm near (-20.0, 40.2, 11.2); fdm nylon needs at least 0.9 mm.
  - Fix: Thicken that wall to a multiple of the nozzle width (0.8, 1.2, 1.6 mm) or merge it into a thicker feature.
- **warning** `mfg.thin_wall`: Wall too thin to make `upright_l` has walls down to 0.80 mm near (9.2, 41.0, 11.2); fdm nylon needs at least 0.9 mm.
  - Fix: Thicken that wall to a multiple of the nozzle width (0.8, 1.2, 1.6 mm) or merge it into a thicker feature.
- **pass** `spinner.bearing`: Weapon on a shaft gripped on both sides `blade_c` turns on `wshaft`, which sits 6.0 mm and 8.8 mm in structure or bearings either side (need 3).
- **warning** `spinner.reach`: Weapon does not lead the front Looking -30 degrees off straight ahead the chassis or a non-ground-game part is -1.6 mm ahead of `blade_c`; the opponent meets it first.
  - Fix: Cut the wedge back or move the weapon forward until it leads by 5-10 mm across plus or minus 30 degrees.
- **warning** `spinner.mass_share`: Weapon is a small share of the robot `blade_c` is 13.1 g, 9% of 147 g; spinners that win put 25-40% of the mass into the weapon (warns below 20%).
- **warning** `spinner.energy_low`: Weapon stores little energy `blade_c` stores 3.4 J at 85% speed (0.02 J per gram of robot; warns below 0.10, i.e. 15 J at 150 g).
  - Fix: Raise the moment of inertia (larger radius, mass at the rim) before raising rpm.
- **warning** `spinner.invert`: Weapon does not reach the floor both ways up `blade_c` is 5.6 mm above the floor upright and -0.2 mm below the floor plane when inverted; it must be within 2 mm either way.
  - Fix: Centre the weapon on the body mid-plane and size it so its rim just touches the floor plane either way up.
- **warning** `spinner.invert`: Robot cannot run upside down A vertical spinner gets flipped often; if it cannot drive inverted it is out of the fight the first time that happens.
- **warning** `spinner.exposed`: Part sits outside the armour `weapon_motor` has a clear path to open air from 38% of its outward rays; a hit or the floor reaches it directly.
  - Fix: Move it inside the shell or add an armour wall (1.2 mm nylon, or 0.8 mm steel or titanium) on the open side.
- **warning** `spinner.wire_exposed`: Wire runs outside the armour Wire `w_bat_sw` has a clear line to open air at this point; a hit or the weapon can cut it.
  - Fix: Route it through the chassis interior or add a wall on the open side.
- **warning** `spinner.wire_exposed`: Wire runs outside the armour Wire `w_wesc_m` has a clear line to open air at this point; a hit or the weapon can cut it.
  - Fix: Route it through the chassis interior or add a wall on the open side.
- **warning** `spinner.wire_exposed`: Wire runs outside the armour Wire `w_m_r` has a clear line to open air at this point; a hit or the weapon can cut it.
  - Fix: Route it through the chassis interior or add a wall on the open side.
- **pass** `kin.motion_inferred`: Motion groups blade_c+blade_i+blade_o+spider+wnut0+wnut1+wnut2+wnut3+wpin0+wpin1+wpin2+wpin3+wshaft about joint of `blade_c`; pulley_fl+wheel_fl+whub_fl about joint of `whub_fl`; pulley_rl+wheel_rl+whub_rl about round shape of `pulley_rl`; pulley_fr+wheel_fr+whub_fr about joint of `whub_fr`; pulley_rr+wheel_rr+whub_rr about round shape of `pulley_rr` (47 parts declare motion explicitly, the rest is inferred).
- **pass** `kin.bearing_orientation`: Bearing turns on its outer race `wbrg_l0`: the inner race is on static `axle_l` and the outer on rotating `whub_rl` (dead axle).
- **pass** `kin.bearing_orientation`: Bearing turns on its outer race `wbrg_l1`: the inner race is on static `axle_l` and the outer on rotating `whub_rl` (dead axle).
- **pass** `kin.bearing_orientation`: Bearing turns on its outer race `wbrg_r0`: the inner race is on static `axle_r` and the outer on rotating `whub_rr` (dead axle).
- **pass** `kin.bearing_orientation`: Bearing turns on its outer race `wbrg_r1`: the inner race is on static `axle_r` and the outer on rotating `whub_rr` (dead axle).
- **pass** `kin.shaft_through_stator`: Motor's own shaft extended (motor-as-hub) `wshaft` is declared the motor's own shaft; it runs in the motor's bearings.
- **warning** `kin.balance_static`: Rotating group is out of balance The mass centre of blade_c+blade_i+blade_o+spider+wnut0+wnut1+wnut2+wnut3+wpin0+wpin1+wpin2+wpin3+wshaft (28.1 g) is 0.06 mm off the spin axis = 7 N at 19320 rpm; allowed 0.05 mm.
  - Fix: Make the weapon symmetric about the axis (matching teeth/counterweight, symmetric holes and screws).
- **pass** `kin.fastener_boundary`: No screw ties a rotating part to a static one Every screw stays inside one motion group, or runs on the spin axis as an axle.
- **pass** `kin.fastener_undeclared`: Screws only pass through declared parts No screw's shank passes through a rotating part it does not list in `through`/`threads_into`.
- **pass** `kin.motor_face`: Screws into motors land on the matching face Static parts screw to the stator face and rotating parts to the bell.
- **pass** `kin.motion_declared`: Declared motion groups match the mechanism Every `rotates_with` / `fixed` declaration agrees with the joints and joins.
- **pass** `kin.spin_joint`: Spinning parts are on revolute joints Every weapon, wheel and pulley turns about a declared joint, motor shaft or axle.
- **pass** `kin.joint_kind`: Spinner joints are revolute Spinning parts use revolute joints.
- **pass** `kin.joint_axis_zero`: Joint axes are defined Every joint has a non-zero axis.
- **pass** `kin.joint_child_static`: Nothing static hangs off a spinning joint No structure or electronics is a child of a spinning joint.
- **pass** `kin.parent_mismatch`: Rotating groups move with their joint Every part rigidly joined to a jointed group is also its child, so sweeps move it.
- **pass** `kin.group_axes_conflict`: One axis per rotating group No rotating group has two different joint axes.
- **pass** `kin.rigid_mix`: No rotating group is rigidly tied to the structure No chain of screws, press fits, glue or pins joins a spinning part to a static one.
- **pass** `kin.rotating_electronics`: No electronics spin No battery, ESC, receiver or switch is in a rotating group.
- **pass** `kin.bearing_races`: Bearings sit between a rotating and a static part Every bearing has one race on a rotating group and the other on the structure.
- **pass** `kin.bearing_seat`: Bearings are seated Each bearing touches the parts its races are joined to.
- **pass** `kin.joint_axis_bearing`: Bearing bores are on the spin axis Every bearing bore is within 0.1 mm / 0.5 deg of the axis it carries.
- **pass** `kin.shaft_through_bearings`: Something runs in every bearing bore Each bearing's bore holds a shaft.
- **pass** `kin.joint_axis_shaft`: Shafts lie on the spin axis Every shaft in a rotating group is within 0.1 mm / 0.5 deg of its axis.
- **pass** `kin.bearing_count`: Weapons are carried by two supports Every weapon group rests on two bearings, or a motor bearing plus one bearing.
- **pass** `kin.motor_mount`: Motor stators are fixed to the structure Every motor's stator is held by a static part.
- **pass** `kin.joint_axis_motor`: Motor shafts are coaxial with what they drive Direct-drive motor axes match their rotating group within 0.1 mm / 0.5 deg.
- **pass** `kin.shaft_through_stator`: No shaft passes through a motor No shaft or pin part intersects a motor body.
- **pass** `kin.double_bearing`: One bearing system per axis No rotating group is carried both by its own bearings and by a rigidly coupled motor's bearings.
- **pass** `kin.torque_path`: Every weapon is driven A motor rotor reaches every weapon group directly or through a belt.
- **pass** `kin.torque_friction`: Weapon drive is keyed Torque reaches the weapon through keys, pins, screws or flats.
- **pass** `drive.coverage`: Every wheel is driven Each wheel reaches a motor through shafts, rigid hubs or belts on rotating pulleys.
- **pass** `kin.pulley_coaxial`: Pulleys are coaxial with their wheels Each pulley's axis matches its rotating group's axis.
- **pass** `kin.bore_fit`: Bores fit their shafts Parts on a shaft have bores within 0.15 mm of the shaft (press/key fit) or run on bearings.
- **pass** `kin.axial_retention`: Rotating parts are held axially both ways Every rotating group on bearings or an axle is located by a shoulder, clip, collar or nut both ways.
- **pass** `kin.spin_axis_declared`: Weapon spin axis declared Every spinning weapon declares `weapon.spin_axis`.
- **pass** `kin.joint_axis_spin`: Joint matches the weapon spin axis The weapon joint axis equals `weapon.spin_axis` and runs through the weapon origin.
- **pass** `kin.weapon_axis_orientation`: Spin axis matches the robot type Vertical spinners/drums spin about a horizontal sideways axis; horizontal spinners about a vertical one.
- **pass** `kin.spin_dir`: Weapon spins the right way Declared spin direction strikes upward at the front (vertical/drum).
- **pass** `kin.tooth_leading`: Teeth lead with their bite Each tooth's steep face leads in the declared spin direction.
- **pass** `kin.balance_dynamic`: Weapon spins about a principal axis The weapon's principal axis matches its spin axis.
- **pass** `kin.spin_stability`: Weapon spins about its major axis Disc/bar weapons have their largest inertia about the spin axis.
- **pass** `kin.fastener_imbalance`: Screws on the weapon are balanced Screws carried by the weapon form a balanced pattern.
- **pass** `kin.sweep_static`: Nothing static is in a swept volume No static part lies inside the volume a rotating group sweeps.
- **pass** `kin.sweep_fastener`: No screw head or nut in a swept volume No static screw protrudes into a rotating group's sweep.
- **pass** `kin.rub_gap`: Rotating parts clear the structure Every rotating group clears static parts by its class gap (weapon 1.0 mm, wheel 0.5 mm, pulley 0.3 mm, other 0.5 mm).
- **pass** `kin.outrunner_bell_rub`: Outrunner bells run clear Nothing static touches a spinning outrunner bell.
- **pass** `kin.lock_engages`: Locking bar stops the weapon The declared locking bar enters the weapon's swept volume.
- **pass** `kin.sweep_rotating`: Rotating groups clear each other No rotating group reaches into another's swept volume.
- **pass** `kin.wheel_axes_parallel`: Wheel axles are parallel All wheel axes within 0.5 deg.
- **pass** `kin.wheel_camber`: Wheels stand upright Wheel axes are horizontal within 1 deg.
- **pass** `kin.wheel_toe`: Wheels point forward Wheel axes are square to the direction of travel within 1 deg.
- **pass** `kin.wheel_track`: Wheels on a side track together Same-side wheel mid-planes within 1 mm.
- **pass** `kin.wheel_height`: Wheels reach the same floor Lowest wheel points within 0.5 mm.
- **pass** `kin.wheel_motor_coaxial`: Wheels sit on their motor shafts Wheel axes on the motor shaft within 0.2 mm / 1 deg.
- **pass** `kin.shaft_engagement`: Hubs grip enough shaft Each driven hub covers at least 3 mm of motor shaft.
- **pass** `kin.belt_pulleys_joint`: Belt pulleys rotate Both pulleys of every belt are on rotating groups.
- **pass** `kin.belt_axes_parallel`: Belt pulley axes are parallel Pulley axes within 0.5 deg.
- **pass** `kin.belt_coplanar`: Belt grooves line up Pulley mid-planes within 0.5 mm.
- **pass** `kin.belt_same_group`: Belts link different shafts A belt's pulleys are on different rotating groups.
- **pass** `kin.tyre_retained`: Tyres are held on their hubs Every tyre is joined to its hub and sits on the rim.
- **pass** `kin.wire_to_rotor`: No wire ends on a rotating part Every wire ends on static parts or motor terminals.
- **warning** `tension.belt_stretch`: Belt stretch out of range `belt_l`: loop 155.1 mm on a 148.8 mm o_ring is 4.2 % stretch, slack: it will slip.
  - Fix: Use a 141 mm loop or move the pulleys.
- **warning** `tension.belt_stretch`: Belt stretch out of range `belt_r`: loop 155.1 mm on a 148.8 mm o_ring is 4.2 % stretch, slack: it will slip.
  - Fix: Use a 141 mm loop or move the pulleys.
- **pass** `targets.match`: Model matches the targets 4 target dimensions within tolerance.
- **pass** `shape.tall`: Low profile Body height 40.6 mm over width 98.4 mm = 0.41 (weapon excluded).
- **pass** `shape.aspect`: Length to width is reasonable L/W = 1.18.
- **pass** `shape.weapon_leads`: The weapon tip leads Nothing but low forks/wedgelets reaches further forward than the weapon's swept front (ground game leads by 4.9 mm, allowed 15).
- **pass** `shape.weapon_floor_reach`: Weapon sweeps close to the floor `blade_c` lowest sweep is 2.9 mm above the floor (axle 23.0 mm, rim 20.1 mm).
- **warning** `shape.armour_coverage`: Internals exposed from the front Only 87% of the front view is covered (need 90%); exposed: `weapon_motor` 12%, `wesc` 1%, `battery` 1%.
  - Fix: Extend the top plate or side walls over these parts.
- **warning** `shape.armour_coverage`: Internals exposed from the back Only 87% of the back view is covered (need 90%); exposed: `weapon_motor` 8%, `battery` 6%.
  - Fix: Extend the top plate or side walls over these parts.
- **pass** `dynamics.tip_angle`: Stable against tipping Centre of mass 14.8 mm up; static tip angles back 75°, front 75°, left 72°, right 73°.
- **pass** `dynamics.traction`: Weight is on the driven wheels About 100% of the weight is on the driven wheels (rest on `base_panel`, `spike_l`, `nut_sl0`, `spike_r`).
- **warning** `dynamics.invertible`: Cannot drive upside down Inverted, `wheel_fl` is 19.3 mm short, `wheel_rl` is 19.3 mm short, `wheel_fr` is 19.3 mm short, `wheel_rr` is 19.3 mm short of the floor; `blade_c`, `blade_i`, `blade_o`, `pod_l`, `pod_r` stick out above the wheels. Once flipped it is stuck unless it can self-right.
  - Fix: Make the wheels stand proud of the top, or add a self-righting feature.
- **pass** `dynamics.balance`: Weapon is balanced `blade_c` mass centre is 0.000 mm off the spin axis: grade G0.1 at 19320 rpm, a 0 N rotating load on the bearings and frame. That is 0.0x the robot's weight.
- **pass** `strength.shaft`: Weapon shaft is strong enough `wshaft` (Ø3.0 mm, titanium) cantilevered 8.5 mm from its only support: design impact 144 N (100 g on 147 g) at the weapon gives 463 MPa (yield 830) and 0.066 mm deflection.
- **warning** `strength.bearing`: Bearing overloaded on a hit `wbearing` (MR73, static rating 120 N) takes 144 N of the design impact 144 N (100 g on 147 g). The balls dent the races (brinelling).
  - Fix: Use a bigger bearing or share the load over more bearings.
- **warning** `strength.upright`: Weapon upright may snap `upright_l` carries 144 N of the design impact 144 N (100 g on 147 g) at 23.0 mm; the weakest cut, 16.9 mm up, has 31 mm² and section modulus 32 mm³: 27 MPa against 22 MPa (across layers).
  - Fix: Thicken the upright front-to-back, add a gusset, or print it so the layers run up the upright.
- **pass** `strength.bolt_pullout`: Bolts hold in the plastic 17 threaded joints each hold their share of the design impact 144 N (100 g on 147 g) with 1.5x margin.
- **warning** `printability.overhang`: Needs support to print `tub`: best print orientation is build-up -z, which still leaves 278 mm² of overhang steeper than 45° or bridge longer than 15 mm.
  - Fix: Chamfer overhangs to 45°, split the part, or accept support material.
- **warning** `printability.bridge`: Bridge too long `tub` printed build-up -z has a 25.0 mm bridge (limit 15 mm); it sags.
- **warning** `printability.overhang`: Needs support to print `base_panel`: best print orientation is build-up +y, which still leaves 320 mm² of overhang steeper than 45° or bridge longer than 15 mm.
  - Fix: Chamfer overhangs to 45°, split the part, or accept support material.
- **warning** `printability.bridge`: Bridge too long `base_panel` printed build-up +y has a 30.0 mm bridge (limit 15 mm); it sags.
- **pass** `printability.ok`: Printable without support 17 printed part(s) print support-free in their best orientation.
- **pass** `mfg.layer_load`: Weapon support layers carry the hit `upright_r` is printed along the spin axis.
- **pass** `mfg.layer_load`: Weapon support layers carry the hit `upright_l` is printed along the spin axis.
- **pass** `process.ok`: Geometry matches the process 46 part(s) are makeable as declared.
- **pass** `shape.curvature`: Organic part is curved `blade_c`: 10 of 12 faces curved (CYLINDER, EXTRUSION).
- **pass** `shape.wheel_enclosure`: Wheel sits in its pod `wheel_fl`: 95% of the wheel (side view) lies inside the pod envelope.
- **pass** `shape.wheel_enclosure`: Wheel sits in its pod `wheel_rl`: 83% of the wheel (side view) lies inside the pod envelope.
- **pass** `shape.wheel_enclosure`: Wheel sits in its pod `wheel_fr`: 95% of the wheel (side view) lies inside the pod envelope.
- **pass** `shape.wheel_enclosure`: Wheel sits in its pod `wheel_rr`: 83% of the wheel (side view) lies inside the pod envelope.
- **warning** `reference.silhouette`: Does not look like the reference photo side view: silhouette IoU 0.87 with `../../robots/revron/photos/ref3.png` (front 0.83, middle 0.86, rear 0.93); outlines differ by up to 6 mm. Worst region: front. Height/length 0.36 model vs 0.37 photo. Overlay (model red, photo blue): /tmp/robot_reference/Revron_compare_side.png
  - Fix: Compare /tmp/robot_reference/Revron_compare_side.png: red = model only, blue = photo only. Fix the front of the robot first.
- **warning** `reference.silhouette`: Does not look like the reference photo iso view: silhouette IoU 0.69 with `../../robots/revron/photos/ref2.jpg` (front 0.45, middle 0.75, rear 0.83); outlines differ by up to 27 mm. Worst region: front. Height/length 0.60 model vs 0.65 photo. Overlay (model red, photo blue): /tmp/robot_reference/Revron_compare_iso.png
  - Fix: Compare /tmp/robot_reference/Revron_compare_iso.png: red = model only, blue = photo only. Fix the front of the robot first.
- **pass** `archetype.declared`: Archetype vertical_spinner_forks Held to the `vertical_spinner_forks` layout rules (26 rules).
- **pass** `archetype.disc_plane_vertical`: Disc spins in a vertical plane The spin axis is 0.0 deg out of the horizontal plane (vertical disc needs a horizontal axle, tol 5 deg).
- **pass** `archetype.axle_lateral`: Axle runs left-right The axle points 0.0 deg away from the left-right (X) axis (tol 5 deg).
- **pass** `archetype.rotor_joint`: Rotor has a spinning joint `blade_c` has a revolute joint about the spin axis.
- **pass** `archetype.rotor_fasteners`: No screw ties rotor to stator No fastener joins the rotor to a static part or passes through its swept volume.
- **pass** `archetype.disc_supported`: Disc sits between two supports Static structure on the axle line: yes on one side, yes on the other (the disc must sit between two supports).
- **pass** `archetype.disc_material`: Disc is metal stock Disc is `steel` (metal) made by `laser`; it must be sheet- or bar-stock metal (laser/waterjet/milled/turned).
- **pass** `archetype.teeth`: Weapon has teeth The weapon outline has 1 tooth/teeth (wanted 1..1); a round edge skids off armour.
- **warning** `archetype.weapon_mass_fraction`: Weapon mass share Rotating mass is 19 % of the robot (wanted 20..50 %).
  - Fix: Move mass into (or out of) the rotor until it is within the range.
- **warning** `archetype.energy_ratio`: Weapon energy for its size Stored energy per robot mass is 23.4 J/kg (wanted 40..600 J/kg).
  - Fix: Heavier rim, bigger diameter or more speed (within tip-speed limits).
- **pass** `archetype.wedgelets_flank`: Blades either side of the disc Wedge/blade parts ahead of the disc axle: present on -X side, present on +X side.
- **warning** `archetype.blade_lead`: Blade tips just ahead of the disc Low forks/wedgelets lead the disc's swept front by is 4.9 mm (wanted 5..15 mm).
  - Fix: Lengthen/shorten the blades or move the axle so the tips lead the tooth sweep by the target.
- **pass** `archetype.disc_floor_gap`: Disc sweeps close to the floor The swept disc's lowest point above the floor is 2.9 mm (wanted 0.3..4 mm).
- **pass** `archetype.weapon_drive`: Weapon drive layout Weapon drive is `motor_is_hub` (accepted: inside_hub, belt_tensioned).
- **pass** `archetype.top_armour_slope`: Top armour slopes to the weapon The top armour slopes down toward the weapon at is 0.0 deg (wanted 0..25 deg).
- **pass** `archetype.drive_config`: Drive layout 4 wheels, 4 driven (4WD).
- **pass** `archetype.invertible`: Drives upside down Wheel tops stand +1.8 mm relative to the top of the chassis (need >= 0.5 mm to drive inverted).
- **warning** `archetype.pods_enclose_wheels`: Side pods wrap the wheels Nothing outboard of wheel(s) `wheel_fl`, `wheel_rl`, `wheel_fr`, `wheel_rr` (side pods must wrap the wheels).
  - Fix: Add side pods/walls outboard of each wheel.
- **pass** `archetype.floor_ribs`: Printed floor is stiffened Floor is 4.0 mm solid (no ribs needed above 2.5 mm).
- **pass** `archetype.lid_inserts`: Lid screws go into inserts Every removable lid screw threads into an insert or nut.
- **pass** `archetype.switch_access`: Switch reachable from the side The switch can be reached from the side.
- **pass** `archetype.axle_height`: Axle height on target Axle centre above the floor is 23.0 mm (wanted 21..25 mm).
- **warning** `archetype.disc_thickness`: Disc thickness on target Disc thickness is 4.0 mm (wanted 4.5..7 mm).
  - Fix: Change the disc thickness.
- **pass** `archetype.disc_diameter`: Disc diameter on target Disc diameter (incl. tooth) is 40.1 mm (wanted 37..43 mm).
- **pass** `archetype.tub_height`: Tub height on target Chassis tub height is 17.0 mm (wanted 16..19 mm).
- **pass** `archetype.wheel_dia`: Wheel size on target Largest wheel diameter is 21.5 mm (wanted 20..23 mm).
- **pass** `archetype.wheel_count`: Wheel count on target Number of wheels is 4.0  (wanted 4..4 ).
- **pass** `arch.tpu_structural`: No structure in elastomer No structural part is TPU or rubber.
- **pass** `arch.tpu_threaded`: No screws in elastomers No fastener threads into TPU or rubber.
- **pass** `arch.upright_brittle`: Weapon uprights are tough No weapon support is a brittle print.
- **pass** `arch.static_on_rotor`: Rotor carries only rotating parts Rotor `blade_c`: ['blade_c', 'blade_i', 'blade_o', 'spider', 'wnut0', 'wnut1', 'wnut2', 'wnut3', 'wpin0', 'wpin1', 'wpin2', 'wpin3', 'wshaft'].
- **pass** `arch.weapon_spin_joint`: Weapon has a spin joint `blade_c` turns on a revolute joint.
- **pass** `arch.boundary_fasteners`: No screw crosses the spin boundary 21 fasteners checked.
- **pass** `arch.fastener_spans_joint`: No screw locks a joint 0 fastener/joint pairs checked.
- **warning** `arch.support_parent`: Weapon support hangs on the other support `upright_l` is parented to `upright_r`, the opposite weapon support; moving one drags the other and the tree no longer says both bolt to the chassis.
  - Fix: Parent `upright_l` to `tub`.
- **pass** `arch.support_parent`: Support parented sensibly `upright_r` parent: `world`.
- **pass** `arch.weapon_supports`: Weapon supported both sides Supports at -4.9 and 8.7 mm along the axis: `weapon_motor`, `wbearing`.
- **pass** `arch.fork_orientation`: Fork tine points at the axle `upright_l` holds side +1 at 8.7 mm; its body centre sits 9.5 mm along the axis and points toward the chassis from the axle.
- **pass** `arch.fork_orientation`: Fork tine points at the axle `upright_r` holds side -1 at -4.9 mm; its body centre sits -19.7 mm along the axis and points toward the chassis from the axle.
- **pass** `arch.bearing_coaxial`: Bearing on axis `wbearing` is 0.00 mm off the axis.
- **pass** `arch.bearing_seat`: Bearing seated `upright_l` surrounds 100 % of `wbearing` (Ø7.0).
- **pass** `arch.boss_aligned`: Axle boss aligned `weapon_motor` surrounds 100 % of the shaft at -4.9 mm.
- **pass** `arch.shaft_span`: Shaft span is short `wshaft` Ø3.0 mm spans 13.6 mm between supports (L/d = 4.5).
- **warning** `arch.weapon_centred`: Weapon not centred between its supports `blade_c` mid-plane is -1.9 mm from the midpoint between its supports (-4.9 / 8.7 mm).
  - Fix: Centre the disc between the uprights, or declare `asymmetric: true` on the weapon (bearing loads then differ).
- **pass** `arch.weapon_support_gap`: Supports close to the weapon Clear shaft between the weapon faces and the supports: -12.2 / -1.4 mm (shaft Ø3.0).
- **pass** `arch.shaft_material`: Weapon shaft is metal `wshaft` is titanium.
- **pass** `arch.shaft_retention`: Shaft is retained axially `wshaft` ends: capped / open; declared retention: True.
- **pass** `arch.bearing_upright_choice`: Weapon in the stoutest upright Side +1: `upright_l` (0.0 mm on axis).
- **pass** `arch.bearing_upright_choice`: Weapon in the stoutest upright Side -1: `upright_r` (5.0 mm on axis).
- **pass** `arch.double_bearing`: Motor-as-hub on one extra bearing `wshaft` is declared the motor's own shaft; its stator is bolted to structure and one coaxial bearing `wbearing` carries the far end.
- **pass** `arch.weapon_motor_in_hub`: Weapon motor inside the hub `weapon_motor` axis 0.00 mm off the spin axis, 64 % of its length inside the rotor envelope.
- **pass** `arch.load_path`: Weapon load reaches the chassis Side +1: shaft → upright_l → tub
- **pass** `arch.load_path_fasteners`: Load-path joint is bolted or seated `upright_l`→`tub`: 2 bolts, 165 mm² contact.
- **pass** `arch.load_path`: Weapon load reaches the chassis Side -1: shaft → upright_r → tub
- **pass** `arch.load_path_fasteners`: Load-path joint is bolted or seated `upright_r`→`tub`: 2 bolts, 163 mm² contact.
- **pass** `arch.fork_stiffness`: Fork is stiff `upright_l`: 72 N at the axle, lever 16.3 mm, weakest I 936 mm⁴, E 1.6 GPa → 0.07 mm.
- **pass** `arch.fork_stiffness`: Fork is stiff `upright_r`: 72 N at the axle, lever 16.3 mm, weakest I 2424 mm⁴, E 1.6 GPa → 0.03 mm.
- **pass** `arch.motor_mount`: Motor is screwed or clamped `weapon_motor`: 2 fasteners, 1 clamps, sandwiched between nothing.
- **pass** `arch.motor_clamp`: Motor is captured `weapon_motor`: structure on both sides along no axis; 2 screws in its face.
- **pass** `arch.motor_antirotation`: Motor cannot turn in its mount `weapon_motor`: 2 face screws, keyed False, flats held False.
- **pass** `arch.motor_face_bolts`: Motor face screw engagement ok `bolt_wm0` engages 3.0 mm of `weapon_motor` (usable 3.5 mm, need ≥ 1.6).
- **pass** `arch.motor_face_static`: Motor screw on the matching face `bolt_wm0` (static side) ends in the stator half of `weapon_motor` (stator face = opposite the catalog shaft output).
- **pass** `arch.motor_face_bolts`: Motor face screw engagement ok `bolt_wm1` engages 3.0 mm of `weapon_motor` (usable 3.5 mm, need ≥ 1.6).
- **pass** `arch.motor_face_static`: Motor screw on the matching face `bolt_wm1` (static side) ends in the stator half of `weapon_motor` (stator face = opposite the catalog shaft output).
- **pass** `arch.motor_mount`: Motor is screwed or clamped `motor_l`: 0 fasteners, 2 clamps, sandwiched between ['tub', 'base_panel'].
- **pass** `arch.motor_clamp`: Motor is captured `motor_l`: structure on both sides along ['X', 'Y', 'Z']; 0 screws in its face.
- **pass** `arch.motor_antirotation`: Motor cannot turn in its mount `motor_l`: 0 face screws, keyed False, flats held True.
- **pass** `arch.motor_mount`: Motor is screwed or clamped `motor_r`: 0 fasteners, 2 clamps, sandwiched between ['tub', 'base_panel'].
- **pass** `arch.motor_clamp`: Motor is captured `motor_r`: structure on both sides along ['X', 'Y', 'Z']; 0 screws in its face.
- **pass** `arch.motor_antirotation`: Motor cannot turn in its mount `motor_r`: 0 face screws, keyed False, flats held True.
- **pass** `arch.bolt_shear`: Bolt groups have shear margin 20 bolt groups have SF ≥ 2.0 in shear.
- **pass** `arch.bolt_bearing`: Bolt holes bear their load No printed hole is crushed by its bolt.
- **warning** `arch.layer_tension`: Screw pulls along the layer lines `bolt_ur0` pulls on `upright_r` along its print direction; a hit (design impact 144 N on `upright_r`) peels layers apart around the insert.
  - Fix: Turn the joint so the screw axis lies in the layer plane, or clamp through with a nut.
- **warning** `arch.layer_tension`: Screw pulls along the layer lines `bolt_ur1` pulls on `upright_r` along its print direction; a hit (design impact 144 N on `upright_r`) peels layers apart around the insert.
  - Fix: Turn the joint so the screw axis lies in the layer plane, or clamp through with a nut.
- **warning** `arch.layer_tension`: Screw pulls along the layer lines `bolt_ul0` pulls on `upright_l` along its print direction; a hit (design impact 144 N on `upright_l`) peels layers apart around the insert.
  - Fix: Turn the joint so the screw axis lies in the layer plane, or clamp through with a nut.
- **warning** `arch.layer_tension`: Screw pulls along the layer lines `bolt_ul1` pulls on `upright_l` along its print direction; a hit (design impact 144 N on `upright_l`) peels layers apart around the insert.
  - Fix: Turn the joint so the screw axis lies in the layer plane, or clamp through with a nut.
- **pass** `arch.bolt_bending`: No bolt bridges a gap No shank spans more than its diameter of air.
- **pass** `arch.bolt_washer`: Screw heads have bearing area Every head on plastic has enough area.
- **pass** `arch.insert_wall`: Insert bosses thick enough Insert walls ≥ 1.5 mm.
- **warning** `arch.hole_spacing`: Holes too close together `bolt_ur0` and `bolt_ur1` in `tub` are 4.0 mm apart (need ≥ 3d = 6.0).
- **warning** `arch.hole_spacing`: Holes too close together `bolt_ul0` and `bolt_ul1` in `tub` are 4.0 mm apart (need ≥ 3d = 6.0).
- **warning** `arch.hole_spacing`: Holes too close together `bolt_ul0` and `bolt_ul1` in `upright_l` are 4.0 mm apart (need ≥ 3d = 6.0).
- **warning** `arch.hole_spacing`: Holes too close together `bolt_ur0` and `bolt_ur1` in `upright_r` are 4.0 mm apart (need ≥ 3d = 6.0).
- **pass** `arch.insert_coaxial`: Inserts line up with screws Every insert is coaxial with its screw in a printed host.
- **pass** `arch.insert_host`: Inserts sit in printed bosses Every heat-set insert is surrounded by a printed part.
- **pass** `arch.cantilever_fastener`: No part levered off its screws 2 lightly-bolted parts checked.
- **warning** `arch.weapon_teeth`: Weapon has no tooth `blade_c` outline never drops 3 mm below its tip radius: it is round and will not bite.
  - Fix: Cut 1-2 hooked teeth into the profile.
- **pass** `arch.foreign_through_rotor`: Nothing passes through the rotor Rotor `blade_c` is clear of static parts.
- **pass** `arch.holder_group`: Parts held by matching structure 36 parent/retainer links checked.
- **pass** `arch.cut_breakout`: Holes keep their webs 68 cylindrical cuts leave ≥ max(1 mm, 1.5x wall).
- **pass** `arch.armor_span`: Top armour well supported `top_cover` (tpu, ~1.1 mm) has an unsupported span of 0 mm: 300 N in the middle deflects 0.0 mm.
- **warning** `arch.armor_span`: Top armour span too long `top_armour` (titanium, ~0.5 mm) has an unsupported span of 28 mm: 300 N in the middle deflects 4.5 mm.
  - Fix: Add a rib/post under the middle, more bolts, or thicker sheet.
- **pass** `arch.electronics_isolated`: Electronics off the load path `battery` touches no weapon support.
- **warning** `arch.battery_restraint`: Battery can move `battery`: walls on both sides along ['Y'], 3/6 sides; strap/clamp: False.
  - Fix: Box it on 2 axes and hold it down with a strap, foam and a lid.
- **pass** `arch.electronics_isolated`: Electronics off the load path `rxesc` touches no weapon support.
- **pass** `arch.electronics_isolated`: Electronics off the load path `wesc` touches no weapon support.
- **pass** `arch.electronics_isolated`: Electronics off the load path `power_switch` touches no weapon support.
- **warning** `arch.symmetry`: Left/right parts differ `upright_l` mirrored differs from `upright_r` by 10.20 mm in extent and 23.0 % in volume.
  - Fix: Mirror one from the other, or list both in `asymmetric`.
- **warning** `arch.symmetry`: Left/right parts differ `insert_ul0` mirrored differs from `insert_ur0` by 10.20 mm in extent and 0.0 % in volume.
  - Fix: Mirror one from the other, or list both in `asymmetric`.
- **warning** `arch.symmetry`: Left/right parts differ `insert_ul1` mirrored differs from `insert_ur1` by 10.20 mm in extent and 0.0 % in volume.
  - Fix: Mirror one from the other, or list both in `asymmetric`.
- **warning** `arch.symmetry_fasteners`: Left/right screws differ `bolt_ul0` mirrored is 10.20 mm from `bolt_ur0` (M2x10 vs M2x10).
- **warning** `arch.symmetry_fasteners`: Left/right screws differ `bolt_ul1` mirrored is 10.20 mm from `bolt_ur1` (M2x10 vs M2x10).
- **pass** `arch.com_support`: Centre of mass over the footprint Centre of mass (-1.6, 22.8) is inside the floor contact polygon by 44.5 mm.
- **pass** `arch.com_height`: Centre of mass low 14.8 mm up, 44.5 mm from the nearest tipping edge.
- **pass** `electrical.drive_motor_voltage`: Drive motors suit the pack voltage Pack 7.4 V nominal is within 1.5x of every drive motor's rating (worst 1.23x).
- **warning** `electrical.weapon_motor_voltage`: Not checked: Weapon motor suits the pack voltage Could not evaluate (no max_cells rating for weapon_motor).
  - Fix: Add the rating to the catalog entry or a `ratings` table on the part.
- **pass** `electrical.esc_voltage`: ESCs rated for the pack voltage 2S pack; ESC ratings: `rxesc` 2S, `wesc` 4S.
- **warning** `electrical.esc_drive_current`: Not checked: Drive ESC covers motor stall Could not evaluate (`rxesc` has no current rating).
  - Fix: Add the rating to the catalog entry or a `ratings` table on the part.
- **warning** `electrical.esc_weapon_current`: Not checked: Weapon ESC covers motor current Could not evaluate (`wesc` has no current rating).
  - Fix: Add the rating to the catalog entry or a `ratings` table on the part.
- **pass** `electrical.wire_ampacity`: Wire gauge carries the current All 7 wires within their gauge's continuous rating.
- **pass** `electrical.connector_rating`: Battery connector rating Battery connector `xt30` rated 30 A; peak load 17.2 A.
- **warning** `electrical.switch_rating`: Not checked: Switch rating Could not evaluate (switch `power_switch` has no current rating (add `ratings.current_a`)).
  - Fix: Add the rating to the catalog entry or a `ratings` table on the part.
- **pass** `electrical.receiver_supply`: Receiver is powered Receiver `rxesc` is powered (wired to an ESC/BEC or integrated).
- **pass** `electrical.failsafe`: Failsafe covers every ESC Failsafe declared and every ESC takes its signal from the receiver.
- **warning** `electrical.indicator`: Power light visible No power indicator LED (a part with `led` in its id/label or `electronics.indicator`).
  - Fix: Add an LED that shows power, visible from outside.
- **pass** `electrical.battery_weapon_gap`: Battery clear of the weapon Battery is 39.4 mm from the weapon's swept volume (need >= 3 mm plus a wall).
- **pass** `electrical.battery_shielded`: Wall between battery and weapon A structural wall sits between the battery and the weapon.
- **pass** `electrical.battery_floor`: Battery protected from below Battery underside is 4.2 mm above the floor and is covered by structure below.
- **pass** `electrical.battery_removable`: Battery comes out without the weapon Battery comes out up past `rxesc`, `top_armour`; no weapon part in the way.
- **pass** `electrical.wire_bend_radius`: Wire bend radius No routed wire bends tighter than 2x its diameter.
- **pass** `electrical.wire_rotating_clearance`: Wires clear of rotating parts Every routed wire stays >= 2 mm from rotating parts.
- **pass** `electrical.strain_relief`: Strain relief at ESC and battery Wires at the ESC/battery have slack and the parts are retained.
- **pass** `electrical.cells_consistent`: Cell count consistent Cell counts: battery 2S, electronics.cells 2S, blade_c.weapon.cells 2S.
- **pass** `electrical.switch_in_series`: Switch cuts all power Every ESC is powered through the switch.
- **pass** `electrical.power_path`: Power path complete Every ESC has battery power and every motor is wired to an ESC.
- **warning** `electrical.battery_c_rating`: Battery continuous rating Continuous load 10.2 A against 7.2 A (capacity x C).
  - Fix: Use a bigger or higher-C pack.
- **warning** `electrical.runtime`: Runtime covers a match Estimated runtime 1.8 min at match duty (need >= 3 min).
  - Fix: Use a bigger pack or lower the load.
- **pass** `electrical.wire_gauge_declared`: Wire gauges declared Every power and motor wire declares its gauge.
- **pass** `electrical.parts_retained`: Electronics retained Battery, ESCs and receiver declare how they are held.
- **pass** `electrical.weapon_disable`: Weapon can be disabled remotely Weapon remote disable declared.
- **warning** `combat.R001`: Front edge sits on the floor Median edge gap across the front is 12.95 mm (limit 1.5 mm).
  - Fix: Lower the front skirt/wedge lip to 0.3-1 mm.
- **warning** `combat.R002`: Front edge covered by a low skirt Share of the front edge with a skirt within 1.5 mm of the floor is 0% (needs 80%).
  - Fix: Run the wedge/skirt across the whole front at 0.3-1 mm.
- **pass** `combat.R003`: Left side has a low skirt Share of the left (+X) side edge within 3 mm of the floor is 99% (needs 60%).
- **pass** `combat.R004`: Right side has a low skirt Share of the right (-X) side edge within 3 mm of the floor is 100% (needs 60%).
- **pass** `combat.R005`: Rear edge is guarded Share of the rear edge within 3 mm of the floor is 100% (needs 50%).
- **pass** `combat.R006`: Front-left corner closed Highest edge gap at the FL corner is 2.99 mm (limit 5 mm).
- **warning** `combat.R007`: Front-right corner closed Highest edge gap at the FR corner is 12.55 mm (limit 5 mm).
  - Fix: Wrap the skirt round the corner or chamfer it down to the floor.
- **warning** `combat.R008`: Rear-right corner closed Highest edge gap at the RR corner is 7.79 mm (limit 5 mm).
  - Fix: Wrap the skirt round the corner or chamfer it down to the floor.
- **warning** `combat.R009`: Rear-left corner closed Highest edge gap at the RL corner is 8.90 mm (limit 5 mm).
  - Fix: Wrap the skirt round the corner or chamfer it down to the floor.
- **pass** `combat.R010`: Perimeter mostly skirted Share of the whole perimeter within 3 mm of the floor is 77% (needs 60%).
- **warning** `combat.R011`: No wide open arc Longest arc of the perimeter with nothing within 5 mm of the floor is 62.00 deg (limit 45 deg).
  - Fix: Close the open arc with a skirt or a low wall.
- **warning** `combat.R012`: No open door anywhere Highest edge gap anywhere on the perimeter is 21.50 mm (limit 12 mm).
  - Fix: Nothing on the outline should leave more than 12 mm under it.
- **warning** `combat.R013`: Gets under a typical wedge Front lip gap (20th percentile) against a typical 0.5 mm opponent wedge is 10.63 mm (limit 0.6 mm).
  - Fix: Lip at or below 0.5 mm wins the who-gets-under contest.
- **pass** `combat.R014`: Sides resist a T-bone Median side edge gap (worse side) when T-boned by a wedge is 1.13 mm (limit 2 mm).
- **warning** `combat.R015`: No fork-sized gap in the front edge Widest stretch of the front edge with no skirt within 1.5 mm of the floor is 40.74 mm (limit 8 mm).
  - Fix: Close gaps in the front skirt wider than 8 mm (opponent forks slip in).
- **warning** `combat.R016`: Front edge level Spread of the edge gap across the front is 19.25 mm (limit 3 mm).
  - Fix: Make the front edge height even across the width.
- **pass** `combat.R020`: Lip clears the floor `spike_l`: Lowest point above the floor is 0.30 mm (needs 0.2 mm).; `spike_r`: Lowest point above the floor is 0.30 mm (needs 0.2 mm).
- **pass** `combat.R021`: Lip is low enough `spike_l`: Lip height above the floor is 0.30 mm (limit 1 mm).; `spike_r`: Lip height above the floor is 0.30 mm (limit 1 mm).
- **pass** `combat.R024`: Sharp lip `spike_l`: Lip thickness 1 mm behind the edge is 0.78 mm (limit 1.2 mm).; `spike_r`: Lip thickness 1 mm behind the edge is 0.78 mm (limit 1.2 mm).
- **pass** `combat.R025`: Thin lip `spike_l`: Lip thickness 3 mm behind the edge is 1.23 mm (limit 2.5 mm).; `spike_r`: Lip thickness 3 mm behind the edge is 1.32 mm (limit 2.5 mm).
- **pass** `combat.R026`: No blunt nose `spike_l`: Height of the vertical front face at the lip is 0.50 mm (limit 0.6 mm).; `spike_r`: Height of the vertical front face at the lip is 0.50 mm (limit 0.6 mm).
- **pass** `combat.R027`: Hard lip Lip material: `spike_l` steel, `spike_r` steel; a printed lip chips and rounds over.
- **pass** `combat.R028`: Skirt spans the front Front skirt width over body width is 97% (needs 40%).
- **pass** `combat.R029`: Skirt is the front-most part Skirt lead over the rest of the body (spinning parts excluded) is 0.00 mm (needs -0.5 mm).
- **pass** `combat.R030`: Tip does not dig in `spike_l`: Underside 3-13 mm behind the tip relative to the tip is 0.00 mm (needs -0.05 mm).; `spike_r`: Underside 3-13 mm behind the tip relative to the tip is 0.00 mm (needs -0.05 mm).
- **pass** `combat.R031`: Lip parallel to the floor `spike_l`: Lip height variation across its width is 0.00 mm (limit 0.5 mm).; `spike_r`: Lip height variation across its width is 0.00 mm (limit 0.5 mm).
- **pass** `combat.R032`: Skirt stiff under push `spike_l`: Tip deflection under 50 N (cantilever) is 0.12 mm (limit 1 mm).; `spike_r`: Tip deflection under 50 N (cantilever) is 0.09 mm (limit 1 mm).
- **pass** `combat.R033`: Skirt thick enough `spike_l`: Skirt thickness at mid-overhang is 1.61 mm (needs 0.8 mm).; `spike_r`: Skirt thickness at mid-overhang is 1.81 mm (needs 0.8 mm).
- **pass** `combat.R034`: Skirt overhang short `spike_l`: Unsupported overhang past the last support is 7.85 mm (limit 45 mm).; `spike_r`: Unsupported overhang past the last support is 8.04 mm (limit 45 mm).
- **pass** `combat.R037`: Skirt clears the wheels `spike_l`: Skirt clearance to the nearest wheel minus its load deflection is 15.94 mm (needs 1 mm).; `spike_r`: Skirt clearance to the nearest wheel minus its load deflection is 15.97 mm (needs 1 mm).
- **warning** `combat.R038`: Skirt bolted down `spike_l`: Fasteners holding the skirt is 1.00  (needs 2 ).
  - Fix: Fix each skirt with >= 2 fasteners.
- **pass** `combat.R040`: At least two tines Fork tines is 2.00  (needs 2 ).
- **warning** `combat.R041`: Tines close together Widest gap between tines with nothing within 3 mm of the floor is 89.00 mm (limit 25 mm).
  - Fix: Keep gaps between tines <= 25 mm, or close them with the weapon/skirt.
- **pass** `combat.R042`: Tines level Height difference between fork tips is 0.00 mm (limit 0.5 mm).
- **pass** `combat.R043`: Tines lead the chassis Fork tips ahead of the chassis is 8.60 mm (needs 0 mm).
- **pass** `combat.R050`: Vertical weapon sweeps low `blade_c`: Vertical weapon sweep above the floor is 2.94 mm (range 0.8 to 6 mm).
- **pass** `combat.R051`: Weapon clears the floor `blade_c`: Weapon sweep above the floor is 2.94 mm (needs 0.3 mm).
- **pass** `combat.R053`: No gap under the weapon `blade_c`: Open floor gap under the weapon (no skirt below it) is 2.94 mm (limit 5 mm).
- **pass** `combat.R054`: Weapon and lip in step Weapon front relative to the skirt lip (negative = lip leads) is -4.94 mm (range -12 to 3 mm).
- **pass** `combat.R060`: Weight on the driven wheels Weight on the driven wheels is 100% (needs 70%).
- **pass** `combat.R061`: Skirt is not carrying the robot Weight resting on the skirt or skids is 0% (limit 15%).
- **pass** `combat.R062`: Low centre of mass (track) Centre-of-mass height over track is 0.18  (limit 0.5 ).
- **pass** `combat.R063`: Low centre of mass (wheelbase) Centre-of-mass height over wheelbase is 0.14  (limit 0.6 ).
- **pass** `combat.R064`: Not top-heavy Centre-of-mass height as a share of body height is 43% (limit 50%).
- **pass** `combat.R065`: Centred sideways Sideways centre-of-mass offset over track is 2% (limit 5%).
- **pass** `combat.R066`: Centre of mass inside the wheelbase Centre of mass inside the wheelbase (share of wheelbase from the nearer end) is 48% (needs 10%).
- **pass** `combat.R067`: Grippy tyres Tyre materials: tpu, tpu, tpu, tpu.
- **pass** `combat.R068`: Wheels roll over seams Smallest wheel diameter (10x a 2 mm seam) is 21.50 mm (needs 20 mm).
- **pass** `combat.R069`: Wide enough tyres Narrowest wheel width is 9.50 mm (needs 6 mm).
- **pass** `combat.R070`: Wheels on both sides Sides of the robot with a wheel is 2.00  (needs 2 ).
- **pass** `combat.R071`: 4WD turns 4WD wheelbase over track (turning scrub) is 0.65  (limit 1 ).
- **pass** `combat.R072`: Wide track Track over body width is 85% (needs 50%).
- **pass** `combat.R073`: Drive can spin the wheels Motor stall thrust 2.7 N over traction limit 1.2 N is 2.38 x (needs 1 x).
- **pass** `combat.R074`: Drive speed Top speed at nominal voltage is 2.48 m/s (range 1.2 to 8 m/s).
- **pass** `combat.R080`: Only wheels touch the floor Only the wheels touch the floor.
- **pass** `combat.R081`: Wheels coplanar Height difference between wheel contacts is 0.00 mm (limit 0.3 mm).
- **warning** `combat.R082`: Belly clears the floor Lowest point of the chassis (skirts and wheels excluded) is 0.50 mm (needs 1 mm).
  - Fix: Raise the chassis underside to >= 1 mm.
- **pass** `combat.R083`: No high-centring Underside clearance away from the edges (high-centring on a seam) is 1.75 mm (needs 1.5 mm).
- **pass** `combat.R084`: No flat dragging belly Flat chassis underside within 0.5 mm of the floor is 0.00 mm2 (limit 50 mm2).
- **warning** `combat.R085`: Screw heads off the floor Lowest screw head above the floor is -0.25 mm (needs 0.5 mm).
  - Fix: Countersink or recess screw heads on the underside.
- **pass** `combat.R086`: Switch off the floor Switch above the floor is 8.75 mm (needs 2 mm).
- **warning** `combat.R090`: Invertible or self-righting Body above the wheel tops (upside down the wheels must still reach the floor) is 12.70 mm (limit 0.5 mm).
  - Fix: Make the wheels stand proud of the top, or add a self-righting mechanism.
- **pass** `combat.R100`: Low profile Body height without wheels and weapon is 34.20 mm (limit 45 mm).
- **pass** `combat.R102`: Side armour angled Vertical share of the side-facing outer surface is 53% (limit 90%).
- **pass** `combat.R110`: No wheel at the front edge Share of front bearings where a wheel is the outermost part is 0% (limit 0%).
- **pass** `combat.R111`: Wheels shielded at the sides Share of the worse side where a wheel is the outermost part is 0% (limit 25%).
- **pass** `combat.R112`: Wheels shielded at the rear Share of rear bearings where a wheel is the outermost part is 0% (limit 25%).
- **pass** `combat.R113`: Wheels not the spinner target Share of the whole perimeter where a wheel is the outermost part (horizontal spinner target) is 5% (limit 10%).
- **pass** `combat.R114`: Body ahead of the wheels Body ahead of the front-most wheel is 41.85 mm (needs 5 mm).
- **pass** `combat.R115`: Side wall outboard of wheels Side wall outboard of the wheels is 2.30 mm (needs 0 mm).
- **pass** `combat.R116`: Wheels below the top Wheel top above the body top (non-invertible: wheels proud of the top get hit) is -12.70 mm (limit 0 mm).
- **pass** `combat.R120`: Battery away from the front Battery behind the front outline is 83.80 mm (needs 10 mm).
- **pass** `combat.R121`: Battery away from the sides Battery inside the side outline is 33.20 mm (needs 5 mm).
- **pass** `assembly.order`: Everything can be assembled Every part slides in along a clear straight path. Assembly order: pulley_fr, wheel_fr, whub_fr, motor_r, pulley_fl, wheel_fl, whub_fl, motor_l, insert_ul1, insert_ul0, insert_ur1, insert_ur0, wbearing, wnut3, wpin3, wnut2, wpin2, wnut1, wpin1, wnut0, wpin0, blade_i, blade_o, spider, wshaft, blade_c, weapon_motor, upright_l, upright_r, bolt_ul1, bolt_ul0, bolt_ur1, bolt_ur0, insert_pr1, insert_pr0, insert_pl1, insert_pl0, insert_t3, insert_t2, insert_t1, insert_t0, insert_b4, insert_b3, insert_b2, insert_b1, insert_b0, power_switch, wesc, rxesc, battery, belt_r, pulley_rr, wheel_rr, wbrg_r1, whub_rr, wbrg_r0, axle_r, pulley_fr, wheel_fr, whub_fr, belt_l, pulley_rl, wheel_rl, wbrg_l1, whub_rl, wbrg_l0, axle_l, pulley_fl, wheel_fl, whub_fl, wnut2, wpin2, wnut1, wpin1, wnut0, wpin0, wshaft, pod_r, pod_l, top_armour, top_cover, nut_sr0, spike_r, nut_sl0, spike_l, base_panel, bolt_sr0, bolt_sl0, bolt_pr1, bolt_pr0, bolt_pl1, bolt_pl0, bolt_wm1, bolt_wm0, bolt_t3, bolt_t2, bolt_t1, bolt_t0, bolt_b4, bolt_b3, bolt_b2, bolt_b1, bolt_b0.
- **warning** `joint.no_locator`: Joint has no locating feature `base_panel` on `tub` is held in place only by friction and the screws' shear (`bolt_b0`, `bolt_b1`, `bolt_b2`, `bolt_b3`, `bolt_b4`); no lip, step, pin or spigot locates it.
  - Fix: Add a lip, step or dowel so the parts register before the screws go in; screws clamp, features locate.
- **warning** `joint.no_locator`: Joint has no locating feature `top_armour` on `tub` is held in place only by friction and the screws' shear (`bolt_t0`, `bolt_t1`, `bolt_t2`, `bolt_t3`); no lip, step, pin or spigot locates it.
  - Fix: Add a lip, step or dowel so the parts register before the screws go in; screws clamp, features locate.
- **warning** `joint.bolt_spread`: Screws bunched together The 2 screws of `tub`-`upright_r` span only 4.0 mm (needs >= 6.0 mm = 3d) and cannot resist a twisting load.
  - Fix: Spread the screws to opposite ends of the joint.
- **warning** `joint.bolt_spread`: Screws bunched together The 2 screws of `tub`-`upright_l` span only 4.0 mm (needs >= 6.0 mm = 3d) and cannot resist a twisting load.
  - Fix: Spread the screws to opposite ends of the joint.
- **warning** `joint.no_locator`: Joint has no locating feature `upright_r` on `weapon_motor` is held in place only by friction and the screws' shear (`bolt_wm0`, `bolt_wm1`); no lip, step, pin or spigot locates it.
  - Fix: Add a lip, step or dowel so the parts register before the screws go in; screws clamp, features locate.
- **warning** `joint.no_locator`: Joint has no locating feature `pod_l` on `tub` is held in place only by friction and the screws' shear (`bolt_pl0`, `bolt_pl1`); no lip, step, pin or spigot locates it.
  - Fix: Add a lip, step or dowel so the parts register before the screws go in; screws clamp, features locate.
- **warning** `joint.no_locator`: Joint has no locating feature `pod_r` on `tub` is held in place only by friction and the screws' shear (`bolt_pr0`, `bolt_pr1`); no lip, step, pin or spigot locates it.
  - Fix: Add a lip, step or dowel so the parts register before the screws go in; screws clamp, features locate.
- **warning** `joint.single_fastener`: Joint held by a single screw `pod_l`-`spike_l` is held by only `bolt_sl0`; one screw lets the part pivot and loosen.
  - Fix: Use at least two screws, or key the joint (pin, flat, tab) and set `mechanical_key` on the connection.
- **warning** `joint.single_fastener`: Joint held by a single screw `pod_r`-`spike_r` is held by only `bolt_sr0`; one screw lets the part pivot and loosen.
  - Fix: Use at least two screws, or key the joint (pin, flat, tab) and set `mechanical_key` on the connection.
- **warning** `joint.insert_boss`: Insert boss too thin Insert `insert_b0` (3.2 mm OD) sits in `tub` with only 6% of a 6.4 mm boss around it; heat-set inserts need a boss OD >= 2x insert OD.
  - Fix: Thicken `tub` around the insert to a 6.4 mm boss.
- **warning** `joint.insert_boss`: Insert boss too thin Insert `insert_b1` (3.2 mm OD) sits in `tub` with only 6% of a 6.4 mm boss around it; heat-set inserts need a boss OD >= 2x insert OD.
  - Fix: Thicken `tub` around the insert to a 6.4 mm boss.
- **warning** `joint.insert_boss`: Insert boss too thin Insert `insert_b2` (3.2 mm OD) sits in `tub` with only 6% of a 6.4 mm boss around it; heat-set inserts need a boss OD >= 2x insert OD.
  - Fix: Thicken `tub` around the insert to a 6.4 mm boss.
- **warning** `joint.insert_boss`: Insert boss too thin Insert `insert_b3` (3.2 mm OD) sits in `tub` with only 6% of a 6.4 mm boss around it; heat-set inserts need a boss OD >= 2x insert OD.
  - Fix: Thicken `tub` around the insert to a 6.4 mm boss.
- **warning** `joint.insert_boss`: Insert boss too thin Insert `insert_b4` (3.2 mm OD) sits in `tub` with only 6% of a 6.4 mm boss around it; heat-set inserts need a boss OD >= 2x insert OD.
  - Fix: Thicken `tub` around the insert to a 6.4 mm boss.
- **warning** `joint.insert_boss`: Insert boss too thin Insert `insert_t0` (3.2 mm OD) sits in `tub` with only 38% of a 6.4 mm boss around it; heat-set inserts need a boss OD >= 2x insert OD.
  - Fix: Thicken `tub` around the insert to a 6.4 mm boss.
- **warning** `joint.head_proud`: Screw head proud on an outer surface The head of `bolt_t0` stands 2.0 mm proud of `top_armour` on the outside; hits shear heads and opponents catch on them.
  - Fix: Counterbore the head flush or use a countersunk (`head: countersunk`) screw.
- **warning** `joint.insert_boss`: Insert boss too thin Insert `insert_t1` (3.2 mm OD) sits in `tub` with only 38% of a 6.4 mm boss around it; heat-set inserts need a boss OD >= 2x insert OD.
  - Fix: Thicken `tub` around the insert to a 6.4 mm boss.
- **warning** `joint.head_proud`: Screw head proud on an outer surface The head of `bolt_t1` stands 2.0 mm proud of `top_armour` on the outside; hits shear heads and opponents catch on them.
  - Fix: Counterbore the head flush or use a countersunk (`head: countersunk`) screw.
- **warning** `joint.insert_boss`: Insert boss too thin Insert `insert_t2` (3.2 mm OD) sits in `tub` with only 38% of a 6.4 mm boss around it; heat-set inserts need a boss OD >= 2x insert OD.
  - Fix: Thicken `tub` around the insert to a 6.4 mm boss.
- **warning** `joint.head_proud`: Screw head proud on an outer surface The head of `bolt_t2` stands 2.0 mm proud of `top_armour` on the outside; hits shear heads and opponents catch on them.
  - Fix: Counterbore the head flush or use a countersunk (`head: countersunk`) screw.
- **warning** `joint.insert_boss`: Insert boss too thin Insert `insert_t3` (3.2 mm OD) sits in `tub` with only 38% of a 6.4 mm boss around it; heat-set inserts need a boss OD >= 2x insert OD.
  - Fix: Thicken `tub` around the insert to a 6.4 mm boss.
- **warning** `joint.head_proud`: Screw head proud on an outer surface The head of `bolt_t3` stands 2.0 mm proud of `top_armour` on the outside; hits shear heads and opponents catch on them.
  - Fix: Counterbore the head flush or use a countersunk (`head: countersunk`) screw.
- **warning** `joint.service_access`: Screw only reachable after removing another part The driver line out of `bolt_ur0` hits `pod_r` 15.5 mm from the head; `pod_r` must come off before this joint can be serviced.
  - Fix: Turn the screw so its driver path exits through an open face or a removable cover, not through `pod_r`.
- **warning** `joint.service_access`: Screw only reachable after removing another part The driver line out of `bolt_ur1` hits `pod_r` 15.5 mm from the head; `pod_r` must come off before this joint can be serviced.
  - Fix: Turn the screw so its driver path exits through an open face or a removable cover, not through `pod_r`.
- **warning** `joint.service_access`: Screw only reachable after removing another part The driver line out of `bolt_ul0` hits `pod_l` 25.5 mm from the head; `pod_l` must come off before this joint can be serviced.
  - Fix: Turn the screw so its driver path exits through an open face or a removable cover, not through `pod_l`.
- **warning** `joint.service_access`: Screw only reachable after removing another part The driver line out of `bolt_ul1` hits `pod_l` 25.5 mm from the head; `pod_l` must come off before this joint can be serviced.
  - Fix: Turn the screw so its driver path exits through an open face or a removable cover, not through `pod_l`.
- **warning** `joint.head_proud`: Screw head proud on an outer surface The head of `bolt_wm0` stands 2.0 mm proud of `upright_r` on the outside; hits shear heads and opponents catch on them.
  - Fix: Counterbore the head flush or use a countersunk (`head: countersunk`) screw.
- **warning** `joint.assembly_dir`: Screw not inserted along the part's assembly direction `upright_r` can only go on along [-0.0, -0.0, -1.0] but `bolt_wm0` is driven along [1.0, 0.0, 0.0] (90 deg off); the screw cannot pull the part home onto its seat.
  - Fix: Drive the screws along the direction the part slides on, through its seat face.
- **warning** `joint.head_proud`: Screw head proud on an outer surface The head of `bolt_wm1` stands 2.0 mm proud of `upright_r` on the outside; hits shear heads and opponents catch on them.
  - Fix: Counterbore the head flush or use a countersunk (`head: countersunk`) screw.
- **warning** `joint.assembly_dir`: Screw not inserted along the part's assembly direction `upright_r` can only go on along [-0.0, -0.0, -1.0] but `bolt_wm1` is driven along [1.0, 0.0, 0.0] (90 deg off); the screw cannot pull the part home onto its seat.
  - Fix: Drive the screws along the direction the part slides on, through its seat face.
- **warning** `joint.head_bearing`: Screw head crushes the plastic `bolt_pl0` head bears 20 MPa on printed `pod_l` at ~150 N clamp; creep limit ~4 MPa.
  - Fix: Add a washer (`"washer": true`), use a flange/button head, or a larger head.
- **warning** `joint.head_proud`: Screw head proud on an outer surface The head of `bolt_pl0` stands 2.0 mm proud of `pod_l` on the outside; hits shear heads and opponents catch on them.
  - Fix: Counterbore the head flush or use a countersunk (`head: countersunk`) screw.
- **warning** `joint.head_bearing`: Screw head crushes the plastic `bolt_pl1` head bears 20 MPa on printed `pod_l` at ~150 N clamp; creep limit ~4 MPa.
  - Fix: Add a washer (`"washer": true`), use a flange/button head, or a larger head.
- **warning** `joint.head_proud`: Screw head proud on an outer surface The head of `bolt_pl1` stands 2.0 mm proud of `pod_l` on the outside; hits shear heads and opponents catch on them.
  - Fix: Counterbore the head flush or use a countersunk (`head: countersunk`) screw.
- **warning** `joint.head_bearing`: Screw head crushes the plastic `bolt_pr0` head bears 20 MPa on printed `pod_r` at ~150 N clamp; creep limit ~4 MPa.
  - Fix: Add a washer (`"washer": true`), use a flange/button head, or a larger head.
- **warning** `joint.head_proud`: Screw head proud on an outer surface The head of `bolt_pr0` stands 2.0 mm proud of `pod_r` on the outside; hits shear heads and opponents catch on them.
  - Fix: Counterbore the head flush or use a countersunk (`head: countersunk`) screw.
- **warning** `joint.head_bearing`: Screw head crushes the plastic `bolt_pr1` head bears 20 MPa on printed `pod_r` at ~150 N clamp; creep limit ~4 MPa.
  - Fix: Add a washer (`"washer": true`), use a flange/button head, or a larger head.
- **warning** `joint.head_proud`: Screw head proud on an outer surface The head of `bolt_pr1` stands 2.0 mm proud of `pod_r` on the outside; hits shear heads and opponents catch on them.
  - Fix: Counterbore the head flush or use a countersunk (`head: countersunk`) screw.
- **warning** `joint.loose_nut`: Nut is not captive Nut `nut_sl0` on `bolt_sl0` has material on only 0% of its flats; it will spin and must be held with a spanner (impossible once assembled).
  - Fix: Sink the nut into a hex nut trap in the part (or replace it with a heat-set insert).
- **warning** `joint.head_bearing`: Screw head crushes the plastic `bolt_sl0` head bears 20 MPa on printed `pod_l` at ~150 N clamp; creep limit ~4 MPa.
  - Fix: Add a washer (`"washer": true`), use a flange/button head, or a larger head.
- **warning** `joint.head_proud`: Screw head proud on an outer surface The head of `bolt_sl0` stands 2.0 mm proud of `pod_l` on the outside; hits shear heads and opponents catch on them.
  - Fix: Counterbore the head flush or use a countersunk (`head: countersunk`) screw.
- **warning** `joint.loose_nut`: Nut is not captive Nut `nut_sr0` on `bolt_sr0` has material on only 0% of its flats; it will spin and must be held with a spanner (impossible once assembled).
  - Fix: Sink the nut into a hex nut trap in the part (or replace it with a heat-set insert).
- **warning** `joint.head_bearing`: Screw head crushes the plastic `bolt_sr0` head bears 20 MPa on printed `pod_r` at ~150 N clamp; creep limit ~4 MPa.
  - Fix: Add a washer (`"washer": true`), use a flange/button head, or a larger head.
- **warning** `joint.head_proud`: Screw head proud on an outer surface The head of `bolt_sr0` stands 2.0 mm proud of `pod_r` on the outside; hits shear heads and opponents catch on them.
  - Fix: Counterbore the head flush or use a countersunk (`head: countersunk`) screw.
- **pass** `material.exempt`: Intentionally solid parts Not judged for excess material: top_cover (kind skirt), pod_l (kind skirt), pod_r (kind skirt), wheel_fl (elastomer), wheel_rl (elastomer), wheel_fr (elastomer), wheel_rr (elastomer).
- **pass** `material.ok`: Material follows the loads 12 of 12 printed part(s) carry no chunky boss, solid core or load-free bulk.
- **pass** `claim.holds`: Claim matches the model "weighs 147 g or less" (mass_total_g <= 147)
- **pass** `claim.holds`: Claim matches the model "fits the 150 mm square" (footprint_mm <= 150)

## Mass budget

| Part | Grams | Plus/minus | Source |
|---|---|---|---|
| tub | 11.64 | 2.33 | computed |
| base_panel | 4.81 | 0.96 | computed |
| spike_l | 0.71 | 0.03 | computed |
| nut_sl0 | 0.25 | 0.01 | computed |
| spike_r | 0.71 | 0.03 | computed |
| nut_sr0 | 0.25 | 0.01 | computed |
| top_cover | 0.84 | 0.17 | computed |
| top_armour | 4.47 | 0.18 | computed |
| pod_l | 3.57 | 0.71 | computed |
| pod_r | 3.53 | 0.71 | computed |
| upright_r | 2.26 | 0.45 | computed |
| upright_l | 1.74 | 0.35 | computed |
| weapon_motor | 17.50 | 2.62 | catalog |
| blade_c | 13.13 | 0.53 | computed |
| wshaft | 0.62 | 0.02 | computed |
| spider | 2.45 | 0.10 | computed |
| blade_o | 4.63 | 0.19 | computed |
| blade_i | 4.63 | 0.19 | computed |
| wpin0 | 0.47 | 0.02 | computed |
| wnut0 | 0.18 | 0.01 | computed |
| wpin1 | 0.47 | 0.02 | computed |
| wnut1 | 0.18 | 0.01 | computed |
| wpin2 | 0.47 | 0.02 | computed |
| wnut2 | 0.18 | 0.01 | computed |
| wpin3 | 0.47 | 0.02 | computed |
| wnut3 | 0.18 | 0.01 | computed |
| wbearing | 0.91 | 0.04 | computed |
| motor_l | 7.50 | 1.12 | catalog |
| whub_fl | 1.17 | 0.23 | computed |
| wheel_fl | 1.81 | 0.36 | computed |
| pulley_fl | 0.42 | 0.08 | computed |
| axle_l | 1.02 | 0.04 | computed |
| wbrg_l0 | 0.56 | 0.02 | computed |
| whub_rl | 1.11 | 0.22 | computed |
| wbrg_l1 | 0.56 | 0.02 | computed |
| wheel_rl | 1.81 | 0.36 | computed |
| pulley_rl | 0.42 | 0.08 | computed |
| belt_l | 0.40 | 0.02 | computed |
| motor_r | 7.50 | 1.12 | catalog |
| whub_fr | 1.17 | 0.23 | computed |
| wheel_fr | 1.81 | 0.36 | computed |
| pulley_fr | 0.42 | 0.08 | computed |
| axle_r | 1.02 | 0.04 | computed |
| wbrg_r0 | 0.56 | 0.02 | computed |
| whub_rr | 1.11 | 0.22 | computed |
| wbrg_r1 | 0.56 | 0.02 | computed |
| wheel_rr | 1.81 | 0.36 | computed |
| pulley_rr | 0.42 | 0.08 | computed |
| belt_r | 0.40 | 0.02 | computed |
| battery | 12.50 | 1.88 | catalog |
| rxesc | 2.30 | 0.34 | catalog |
| wesc | 5.00 | 0.75 | catalog |
| power_switch | 0.50 | 0.07 | catalog |
| insert_b0 | 0.12 | 0.02 | catalog |
| insert_b1 | 0.12 | 0.02 | catalog |
| insert_b2 | 0.12 | 0.02 | catalog |
| insert_b3 | 0.12 | 0.02 | catalog |
| insert_b4 | 0.12 | 0.02 | catalog |
| insert_t0 | 0.12 | 0.02 | catalog |
| insert_t1 | 0.12 | 0.02 | catalog |
| insert_t2 | 0.12 | 0.02 | catalog |
| insert_t3 | 0.12 | 0.02 | catalog |
| insert_ur0 | 0.12 | 0.02 | catalog |
| insert_ur1 | 0.12 | 0.02 | catalog |
| insert_ul0 | 0.12 | 0.02 | catalog |
| insert_ul1 | 0.12 | 0.02 | catalog |
| insert_pl0 | 0.12 | 0.02 | catalog |
| insert_pl1 | 0.12 | 0.02 | catalog |
| insert_pr0 | 0.12 | 0.02 | catalog |
| insert_pr1 | 0.12 | 0.02 | catalog |
| bolt_b0 | 0.33 | 0.02 | fastener |
| bolt_b1 | 0.33 | 0.02 | fastener |
| bolt_b2 | 0.33 | 0.02 | fastener |
| bolt_b3 | 0.33 | 0.02 | fastener |
| bolt_b4 | 0.33 | 0.02 | fastener |
| bolt_t0 | 0.33 | 0.02 | fastener |
| bolt_t1 | 0.33 | 0.02 | fastener |
| bolt_t2 | 0.33 | 0.02 | fastener |
| bolt_t3 | 0.33 | 0.02 | fastener |
| bolt_ur0 | 0.42 | 0.02 | fastener |
| bolt_ur1 | 0.42 | 0.02 | fastener |
| bolt_ul0 | 0.42 | 0.02 | fastener |
| bolt_ul1 | 0.42 | 0.02 | fastener |
| bolt_wm0 | 0.38 | 0.02 | fastener |
| bolt_wm1 | 0.38 | 0.02 | fastener |
| bolt_pl0 | 0.38 | 0.02 | fastener |
| bolt_pl1 | 0.38 | 0.02 | fastener |
| bolt_pr0 | 0.38 | 0.02 | fastener |
| bolt_pr1 | 0.38 | 0.02 | fastener |
| bolt_sl0 | 0.33 | 0.02 | fastener |
| bolt_sr0 | 0.33 | 0.02 | fastener |
| wires | 0.91 | 0.27 | wire |
| allowance | 1.20 | 0.60 | declared |

## Wire routes

| Wire | AWG | Diameter mm | Length mm |
|---|---|---|---|
| w_bat_sw | 22 | 1.9 | 39 |
| w_sw_wesc | 22 | 1.9 | 52 |
| w_wesc_m | 24 | 1.6 | 66 |
| w_sw_rx | 26 | 1.3 | 30 |
| w_m_l | 28 | 1.1 | 46 |
| w_m_r | 28 | 1.1 | 46 |
| w_rx_wesc | 30 | 0.9 | 49 |

## NOT CHECKED

The verifier did not judge these. A clean report says nothing about them.

- Strength: arm, fork and shell bending under impact (no stress or stiffness model; load path is not traced)
- Battery access and field service: swap time, number of fasteners to reach the battery or change a wheel
- Wire tether in assembly order: soldered wires between parts are not part of the disassembly sweep
- Heat-set insert iron clearance and soldering-iron access
- Gyro, spin-up time and ESC current limits of the weapon
- Thermal limits and glue or tape strength (declared only)
- Spinner balance and vibration at speed (mass centre of the weapon is not compared with its axis)
- Gyro bearing load of `blade_c`: no shaft supported on both sides
- Fork bending: forks are not traced to their mount; only weapon uprights are sectioned
- Process: single-profile neck width (web inside one outline) and fdm overhangs per declared orientation are not checked here
- Electrical `weapon_motor_voltage`: no max_cells rating for weapon_motor
- Electrical `esc_drive_current`: `rxesc` has no current rating
- Electrical `esc_weapon_current`: `wesc` has no current rating
- Electrical `switch_rating`: switch `power_switch` has no current rating (add `ratings.current_a`)
- combat.R017: Arena seam crossing at speed (dynamic bounce over a 1-2 mm step)
- combat.R018: Skirt wear and lip rounding over a fight
- combat.R039: Countersunk skirt screws flush with the ramp (head protrusion above the ramp face)
- combat.R044: Fork tine stiffness under a 50 N side load
- combat.R045: Fork tip shape (pointed vs square) against opponent wedge lips
- combat.R055: Vertical weapon spin direction (checked by kin.spin_dir)
- combat.R056: Weapon hit reaction: hop and recoil wheelie of the robot
- combat.R057: Gyroscopic lift/walk of a vertical spinner while turning (see dynamics gyro)
- combat.R058: Horizontal spinner recoil spin-out after a hit
- combat.R059: Weapon spin-up time vs closing distance
- combat.R075: Acceleration and closing time across the arena
- combat.R076: Tyre hardness (Shore) and dust pickup
- combat.R077: Tyre compression under load lowering the skirt
- combat.R078: Drive current limit while pushing (ESC/BEC)
- combat.R079: Driver control: steering response and drive mixing
- combat.R087: Ground effect of wires and loose tape under the robot
- combat.R088: Battery puncture risk from floor impacts
- combat.R095: Self-righting mechanism actually rights the robot
- combat.R096: Inverted controls (remote mixing flip)
- combat.R097: Behaviour on its side (rolls back onto wheels)
- combat.R103: Top armour protrusions that a lifter can hook
- combat.R104: Overhangs on the outline that trap an opponent's wedge
- combat.R105: Armour material per face vs the expected weapon
- combat.R117: Wheel hubs survive a side hit (hub/axle strength)
- combat.R118: Wheel guards stiff enough to stop a spinner
- combat.R122: Pit and arena edge: rear overhang falling into the pit
- combat.R123: Arena wall: skirt catching the wall bottom rail
- combat.R124: Pushing match outcome vs a heavier opponent (mass + grip)
- combat.R125: Lifter/flipper arm stays below the skirt line when lowered
- Joint `bolt_sl0`: no part found around `nut_sl0` (insert/nut host unknown)
- Joint `bolt_sr0`: no part found around `nut_sr0` (insert/nut host unknown)
- Joint `bolt_ur0`: `tub` has no assembly step, screw vs assembly direction not checked
- Joint `bolt_ur1`: `tub` has no assembly step, screw vs assembly direction not checked
- Joint `bolt_ul0`: `tub` has no assembly step, screw vs assembly direction not checked
- Joint `bolt_ul1`: `tub` has no assembly step, screw vs assembly direction not checked
