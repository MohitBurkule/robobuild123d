# Verifier report: Revron

Profile `aws2025`. 0 blockers, 168 warnings, 361 checks passed. Check set revision 10 (engine build123d).

Mass 148.9 g (range 133.5 to 164.3 g, limit 150 g).

## Findings

- **pass** `validity.ok`: Spec is well formed 42 parts, 27 fasteners, 7 wires.
- **warning** `wiring.bend`: Wire bends too tightly Wire `w_bat_sw` turns 55 degrees with less than 3.2 mm bend radius; it will kink or pull off its solder joint.
  - Fix: Widen the channel at the corner or route it in a straighter line.
- **warning** `wiring.bend`: Wire bends too tightly Wire `w_wesc_m` turns 45 degrees with less than 3.2 mm bend radius; it will kink or pull off its solder joint.
  - Fix: Widen the channel at the corner or route it in a straighter line.
- **warning** `wiring.bend`: Wire bends too tightly Wire `w_sw_rx` turns 53 degrees with less than 2.6 mm bend radius; it will kink or pull off its solder joint.
  - Fix: Widen the channel at the corner or route it in a straighter line.
- **warning** `mass.may_be_over`: May be over the weight limit 148.9 g (range 133.5 to 164.3 g) against the 150 g limit; 4.7 g of the uncertainty is catalog estimates, weigh the real parts and set `scale_mass_g`.
  - Fix: Weigh real parts and set `scale_mass_g`, or remove mass until the upper bound fits.
- **pass** `interference.overlap`: No parts collide 188 touching or overlapping pairs checked; touching is allowed, overlap deeper than 0.08 mm is not.
- **pass** `interference.sweep`: Joint sweep is clear `blade_c` swept 0..360 deg in 80 steps without hitting anything.
- **pass** `interference.sweep`: Joint sweep is clear `whub_rl` swept 0..360 deg in 80 steps without hitting anything.
- **pass** `interference.sweep`: Joint sweep is clear `whub_fl` swept 0..360 deg in 80 steps without hitting anything.
- **pass** `interference.sweep`: Joint sweep is clear `whub_rr` swept 0..360 deg in 80 steps without hitting anything.
- **pass** `interference.sweep`: Joint sweep is clear `whub_fr` swept 0..360 deg in 80 steps without hitting anything.
- **pass** `interference.spin`: Weapon sweep is clear `blade_c` and 13 rotor part(s) swept a full turn without touching another part.
- **warning** `interference.wheel_clearance`: Wheel has no running clearance `wheel_fl` turning about its axle comes within 0.90 mm of `belt_l`; it needs 1.0 mm so tyre squash, flex and debris do not make it rub.
  - Fix: Open the wheel pocket so it clears the wheel by 1 mm on every side (radius and both faces).
- **warning** `interference.wheel_clearance`: Wheel has no running clearance `wheel_fl` turning about its axle comes within 0.00 mm of `so_bl`; it needs 1.0 mm so tyre squash, flex and debris do not make it rub.
  - Fix: Open the wheel pocket so it clears the wheel by 1 mm on every side (radius and both faces).
- **warning** `interference.wheel_clearance`: Wheel has no running clearance `wheel_fl` turning about its axle comes within 0.50 mm of `wedglet_l`; it needs 1.0 mm so tyre squash, flex and debris do not make it rub.
  - Fix: Open the wheel pocket so it clears the wheel by 1 mm on every side (radius and both faces).
- **warning** `interference.wheel_clearance`: Wheel has no running clearance `wheel_fr` turning about its axle comes within 0.90 mm of `belt_r`; it needs 1.0 mm so tyre squash, flex and debris do not make it rub.
  - Fix: Open the wheel pocket so it clears the wheel by 1 mm on every side (radius and both faces).
- **warning** `interference.wheel_clearance`: Wheel has no running clearance `wheel_fr` turning about its axle comes within 0.00 mm of `so_br`; it needs 1.0 mm so tyre squash, flex and debris do not make it rub.
  - Fix: Open the wheel pocket so it clears the wheel by 1 mm on every side (radius and both faces).
- **warning** `interference.wheel_clearance`: Wheel has no running clearance `wheel_fr` turning about its axle comes within 0.50 mm of `wedglet_r`; it needs 1.0 mm so tyre squash, flex and debris do not make it rub.
  - Fix: Open the wheel pocket so it clears the wheel by 1 mm on every side (radius and both faces).
- **warning** `interference.wheel_clearance`: Wheel has no running clearance `wheel_rl` turning about its axle comes within 0.90 mm of `belt_l`; it needs 1.0 mm so tyre squash, flex and debris do not make it rub.
  - Fix: Open the wheel pocket so it clears the wheel by 1 mm on every side (radius and both faces).
- **warning** `interference.wheel_clearance`: Wheel has no running clearance `wheel_rl` turning about its axle comes within 0.00 mm of `motor_l`; it needs 1.0 mm so tyre squash, flex and debris do not make it rub.
  - Fix: Open the wheel pocket so it clears the wheel by 1 mm on every side (radius and both faces).
- **warning** `interference.wheel_clearance`: Wheel has no running clearance `wheel_rl` turning about its axle comes within 0.41 mm of `wedglet_l`; it needs 1.0 mm so tyre squash, flex and debris do not make it rub.
  - Fix: Open the wheel pocket so it clears the wheel by 1 mm on every side (radius and both faces).
- **warning** `interference.wheel_clearance`: Wheel has no running clearance `wheel_rr` turning about its axle comes within 0.90 mm of `belt_r`; it needs 1.0 mm so tyre squash, flex and debris do not make it rub.
  - Fix: Open the wheel pocket so it clears the wheel by 1 mm on every side (radius and both faces).
- **warning** `interference.wheel_clearance`: Wheel has no running clearance `wheel_rr` turning about its axle comes within 0.00 mm of `motor_r`; it needs 1.0 mm so tyre squash, flex and debris do not make it rub.
  - Fix: Open the wheel pocket so it clears the wheel by 1 mm on every side (radius and both faces).
- **warning** `interference.wheel_clearance`: Wheel has no running clearance `wheel_rr` turning about its axle comes within 0.41 mm of `wedglet_r`; it needs 1.0 mm so tyre squash, flex and debris do not make it rub.
  - Fix: Open the wheel pocket so it clears the wheel by 1 mm on every side (radius and both faces).
- **warning** `retention.loose`: Nothing holds this part in place `wshaft` can move more than 0.5 mm toward +x, -x without touching anything (captive means at most 0.5 mm of play in every direction); in a hit it will fall out or rattle.
  - Fix: Make the pocket snug on that side (0.2 to 0.5 mm gap), add a retaining rib or strap, or declare how it is held in `retained` (tape, adhesive, velcro, press_fit).
- **warning** `retention.loose`: Nothing holds this part in place `wbearing` can move more than 0.5 mm toward -x without touching anything (captive means at most 0.5 mm of play in every direction); in a hit it will fall out or rattle.
  - Fix: Make the pocket snug on that side (0.2 to 0.5 mm gap), add a retaining rib or strap, or declare how it is held in `retained` (tape, adhesive, velcro, press_fit).
- **pass** `retention.declared`: Held by declared method `battery` is held by press_fit.
- **pass** `retention.declared`: Held by declared method `rxesc` is held by kapton.
- **pass** `retention.declared`: Held by declared method `wesc` is held by kapton.
- **pass** `retention.declared`: Held by declared method `power_switch` is held by press_fit.
- **warning** `connection.press_fit_interference`: Press fit has no sensible interference `wshaft`-`weapon_motor`: give `interference_mm` between 0.05 and 0.4 for a unknown material press fit (got 0.02).
- **warning** `connection.press_fit_interference`: Press fit has no sensible interference `wbearing`-`upright_r`: give `interference_mm` between 0.05 and 0.4 for a metal/printed press fit (got 0.02).
- **pass** `connection.joined`: Every part is attached All 42 parts lead back to the chassis through screws, shared prints, captive pockets, joints or declared connections.
- **pass** `internal.solid_invalid`: Every part is a valid solid All bodies are closed, outward-facing manifolds.
- **pass** `internal.no_contact`: Every part touches something 42 parts each touch at least one other solid.
- **pass** `internal.fastener_void`: Screw shanks pass through parts 27 screws each run at least 40 % through drawn solids.
- **pass** `internal.wire_in_solid`: Wires stay in free space 7 routed wires sampled every 0.5 mm stay out of every solid away from their ports.
- **pass** `ground.wheels_touch`: Wheels touch the floor All 4 wheels reach the floor plane (z = 0.00 mm).
- **warning** `ground.clearance`: Body is close to the floor `tub` is 0.30 mm above the floor; it will scrape on arena seams and ride on the ground when a tyre compresses.
  - Fix: Raise the chassis or use a bigger wheel; wedges and forks may go lower.
- **pass** `ground.wedge_gap`: Wedge tip height is right `wedglet_l` tip is 0.72 mm above the floor.
- **pass** `ground.wedge_gap`: Wedge tip height is right `wedglet_r` tip is 0.72 mm above the floor.
- **pass** `ground.stance`: Stable on the floor Centre of mass is 19.9 mm inside the support polygon of wheels and wedge.
- **warning** `ground.wedge_load`: Front rests on the wedge About 100% of the weight sits on the wedge tip because the centre of mass is ahead of the axle; the tip drags and wears and the drive loses traction.
  - Fix: Move the battery and motors back, or add a front skid wheel, or put the axle forward.
- **warning** `ground.wheel_exposed`: Wheel sticks out of the body `wheel_rl` reaches open air from 37% of its side and upward rays above the belly line (allowed 5%); a spinner or a wall hits the tyre first.
  - Fix: Pull the wheel inside the outline, or add a side wall or guard over the exposed tread.
- **warning** `ground.wheel_exposed`: Wheel sticks out of the body `wheel_fl` reaches open air from 14% of its side and upward rays above the belly line (allowed 5%); a spinner or a wall hits the tyre first.
  - Fix: Pull the wheel inside the outline, or add a side wall or guard over the exposed tread.
- **warning** `ground.wheel_exposed`: Wheel sticks out of the body `wheel_rr` reaches open air from 35% of its side and upward rays above the belly line (allowed 5%); a spinner or a wall hits the tyre first.
  - Fix: Pull the wheel inside the outline, or add a side wall or guard over the exposed tread.
- **warning** `ground.wheel_exposed`: Wheel sticks out of the body `wheel_fr` reaches open air from 14% of its side and upward rays above the belly line (allowed 5%); a spinner or a wall hits the tyre first.
  - Fix: Pull the wheel inside the outline, or add a side wall or guard over the exposed tread.
- **pass** `legal.switch`: Marked tool-free power switch `power_switch` is a marked, tool-free power switch.
- **warning** `switch.drive_axis`: Switch slides along the drive direction `power_switch` moves forward and back: hard acceleration, braking and head-on hits push the slider.
  - Fix: Orient the slider across the robot (x axis), or add a detent plus a guard rib on both ends.
- **warning** `switch.too_deep`: Switch is buried `power_switch` is 5.9 mm below the surface; a finger cannot move the slider without a tool.
- **pass** `legal.failsafe`: Failsafe declared The robot stops when the transmitter is switched off.
- **pass** `legal.weapon_disable`: Weapon can be disabled remotely The weapon is switched off from the transmitter.
- **pass** `legal.locking_bar`: Removable tooth-stop pin declared `blade_c`: a 2 mm pin through `tub` at 18.7 mm from the axis (tips reach 21.2 mm) stops the first tooth.
- **pass** `legal.footprint`: Fits the square Fits a 103.8 mm square (limit 150 mm).
- **warning** `fastener.head_seat`: Screw head sits on nothing Nothing is under the head of `bolt_sla`; it cannot clamp the parts.
  - Fix: Move `at` to the surface the head presses on, or cut a counterbore whose floor is at `at`.
- **warning** `fastener.head_seat`: Screw head sits on nothing Nothing is under the head of `bolt_slb`; it cannot clamp the parts.
  - Fix: Move `at` to the surface the head presses on, or cut a counterbore whose floor is at `at`.
- **warning** `fastener.head_seat`: Screw head sits on nothing Nothing is under the head of `bolt_slc`; it cannot clamp the parts.
  - Fix: Move `at` to the surface the head presses on, or cut a counterbore whose floor is at `at`.
- **warning** `fastener.head_seat`: Screw head sits on nothing Nothing is under the head of `bolt_sra`; it cannot clamp the parts.
  - Fix: Move `at` to the surface the head presses on, or cut a counterbore whose floor is at `at`.
- **warning** `fastener.head_seat`: Screw head sits on nothing Nothing is under the head of `bolt_srb`; it cannot clamp the parts.
  - Fix: Move `at` to the surface the head presses on, or cut a counterbore whose floor is at `at`.
- **warning** `fastener.head_seat`: Screw head sits on nothing Nothing is under the head of `bolt_src`; it cannot clamp the parts.
  - Fix: Move `at` to the surface the head presses on, or cut a counterbore whose floor is at `at`.
- **pass** `fastener.access_order`: Screw driven before later parts `bolt_d0` is driven before bspacer, so_al, so_bl, tub, upright_l, upright_r, wbearing, weapon_motor, wedglet_l are fitted (declared order); those parts do not block its driver.
- **pass** `fastener.access_order`: Screw driven before later parts `bolt_p0` is driven before bspacer, upright_r, wbearing are fitted (declared order); those parts do not block its driver.
- **pass** `fastener.access_order`: Screw driven before later parts `bolt_d1` is driven before bspacer, so_al, so_bl, tub, upright_l, upright_r, wbearing, weapon_motor, wedglet_l are fitted (declared order); those parts do not block its driver.
- **pass** `fastener.access_order`: Screw driven before later parts `bolt_p1` is driven before bspacer, upright_r, wbearing are fitted (declared order); those parts do not block its driver.
- **pass** `fastener.access_order`: Screw driven before later parts `bolt_d2` is driven before bspacer, so_al, so_bl, tub, upright_l, upright_r, wbearing, weapon_motor, wedglet_l are fitted (declared order); those parts do not block its driver.
- **pass** `fastener.access_order`: Screw driven before later parts `bolt_p2` is driven before bspacer, upright_r, wbearing are fitted (declared order); those parts do not block its driver.
- **pass** `fastener.access_order`: Screw driven before later parts `bolt_d3` is driven before bspacer, so_al, so_bl, tub, upright_l, upright_r, wbearing, weapon_motor, wedglet_l are fitted (declared order); those parts do not block its driver.
- **pass** `fastener.access_order`: Screw driven before later parts `bolt_p3` is driven before bspacer, upright_r, wbearing are fitted (declared order); those parts do not block its driver.
- **pass** `power.tip_speed`: Tip speed is legal 19320 rpm at 42 mm diameter is 96 mph (limit 600).
- **pass** `power.weapon_energy`: Weapon stores useful energy About 7.5 J at 85% of no-load speed.
- **warning** `power.battery`: Battery may sag under peak load Estimated peak 18.2 A against a 7.2 A rating (180 mAh x 40 C); the voltage will collapse in a hit.
  - Fix: Use a bigger or higher-C pack, or a motor that draws less.
- **pass** `power.runtime`: Battery lasts the fight 180 mAh x 80% usable lasts about 4.1 min of fighting (per 3 min fight: drive 52 mAh, weapon spin-ups and hold 48 mAh, electronics 5 mAh = 105 mAh).
- **warning** `mfg.thin_wall`: Wall too thin to make `top_armour` has walls down to 1.01 mm near (14.5, -44.4, 20.4); fdm tpu needs at least 1.2 mm.
  - Fix: Thicken that wall to a multiple of the nozzle width (0.8, 1.2, 1.6 mm) or merge it into a thicker feature.
- **warning** `mfg.thin_wall`: Wall too thin to make `wedglet_l` has walls down to 0.90 mm near (34.4, 12.8, 8.7); fdm tpu needs at least 1.2 mm.
  - Fix: Thicken that wall to a multiple of the nozzle width (0.8, 1.2, 1.6 mm) or merge it into a thicker feature.
- **warning** `mfg.thin_wall`: Wall too thin to make `wedglet_r` has walls down to 0.93 mm near (-28.7, 35.5, 3.3); fdm tpu needs at least 1.2 mm.
  - Fix: Thicken that wall to a multiple of the nozzle width (0.8, 1.2, 1.6 mm) or merge it into a thicker feature.
- **pass** `spinner.bearing`: Weapon on a shaft gripped on both sides `blade_c` turns on `wshaft`, which sits 18.5 mm and 2.5 mm in structure or bearings either side (need 3).
- **warning** `spinner.reach`: Weapon does not lead the front Looking 30 degrees off straight ahead the chassis or a non-ground-game part is -2.8 mm ahead of `blade_c`; the opponent meets it first.
  - Fix: Cut the wedge back or move the weapon forward until it leads by 5-10 mm across plus or minus 30 degrees.
- **warning** `spinner.energy_low`: Weapon stores little energy `blade_c` stores 7.5 J at 85% speed (0.05 J per gram of robot; warns below 0.10, i.e. 15 J at 150 g).
  - Fix: Raise the moment of inertia (larger radius, mass at the rim) before raising rpm.
- **warning** `spinner.invert`: Weapon does not reach the floor both ways up `blade_c` is 5.9 mm above the floor upright and 0.0 mm below the floor plane when inverted; it must be within 2 mm either way.
  - Fix: Centre the weapon on the body mid-plane and size it so its rim just touches the floor plane either way up.
- **warning** `spinner.invert`: Robot cannot run upside down A vertical spinner gets flipped often; if it cannot drive inverted it is out of the fight the first time that happens.
- **warning** `spinner.exposed`: Part sits outside the armour `weapon_motor` has a clear path to open air from 20% of its outward rays; a hit or the floor reaches it directly.
  - Fix: Move it inside the shell or add an armour wall (1.2 mm nylon, or 0.8 mm steel or titanium) on the open side.
- **warning** `spinner.exposed`: Part sits outside the armour `battery` has a clear path to open air from 3% of its outward rays; a hit or the floor reaches it directly.
  - Fix: Move it inside the shell or add an armour wall (1.2 mm nylon, or 0.8 mm steel or titanium) on the open side.
- **warning** `spinner.wire_exposed`: Wire runs outside the armour Wire `w_sw_wesc` has a clear line to open air at this point; a hit or the weapon can cut it.
  - Fix: Route it through the chassis interior or add a wall on the open side.
- **warning** `spinner.wire_exposed`: Wire runs outside the armour Wire `w_wesc_m` has a clear line to open air at this point; a hit or the weapon can cut it.
  - Fix: Route it through the chassis interior or add a wall on the open side.
- **warning** `spinner.wire_exposed`: Wire runs outside the armour Wire `w_sw_rx` has a clear line to open air at this point; a hit or the weapon can cut it.
  - Fix: Route it through the chassis interior or add a wall on the open side.
- **pass** `kin.motion_inferred`: Motion groups blade_c+bspacer+disc_f+prop_mount+spacer+wshaft about joint of `blade_c`; wheel_rl+whub_rl about joint of `whub_rl`; wheel_fl+whub_fl about joint of `whub_fl`; wheel_rr+whub_rr about joint of `whub_rr`; wheel_fr+whub_fr about joint of `whub_fr` (31 parts declare motion explicitly, the rest is inferred).
- **warning** `kin.bore_fit`: Part is loose on its shaft `blade_c` bore radius 2.99 mm on `wshaft` radius 2.49 mm (0.50 mm radial play); it rattles and fretts.
  - Fix: Size the bore to the shaft (ream, or 0-0.05 mm press fit).
- **warning** `kin.rub_gap`: Rotating part runs too close to a static one wheel_rl+whub_rl passes 0.41 mm from `wedglet_l` (need 0.5 mm for a wheel).
  - Fix: Open the clearance (flex and runout eat small gaps).
- **warning** `kin.rub_gap`: Rotating part runs too close to a static one wheel_fl+whub_fl passes 0.20 mm from `wedglet_l` (need 0.5 mm for a wheel).
  - Fix: Open the clearance (flex and runout eat small gaps).
- **warning** `kin.rub_gap`: Rotating part runs too close to a static one wheel_rr+whub_rr passes 0.33 mm from `wedglet_r` (need 0.5 mm for a wheel).
  - Fix: Open the clearance (flex and runout eat small gaps).
- **warning** `kin.rub_gap`: Rotating part runs too close to a static one wheel_fr+whub_fr passes 0.20 mm from `wedglet_r` (need 0.5 mm for a wheel).
  - Fix: Open the clearance (flex and runout eat small gaps).
- **warning** `kin.wheel_track`: Same-side wheels do not track `wheel_rl` and `wheel_fl` mid-planes are 1.8 mm apart along the axle.
- **warning** `kin.wheel_track`: Same-side wheels do not track `wheel_rr` and `wheel_fr` mid-planes are 1.7 mm apart along the axle.
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
- **pass** `kin.axial_retention`: Rotating parts are held axially both ways Every rotating group on bearings or an axle is located by a shoulder, clip, collar or nut both ways.
- **pass** `kin.spin_axis_declared`: Weapon spin axis declared Every spinning weapon declares `weapon.spin_axis`.
- **pass** `kin.joint_axis_spin`: Joint matches the weapon spin axis The weapon joint axis equals `weapon.spin_axis` and runs through the weapon origin.
- **pass** `kin.weapon_axis_orientation`: Spin axis matches the robot type Vertical spinners/drums spin about a horizontal sideways axis; horizontal spinners about a vertical one.
- **pass** `kin.spin_dir`: Weapon spins the right way Declared spin direction strikes upward at the front (vertical/drum).
- **pass** `kin.tooth_leading`: Teeth lead with their bite Each tooth's steep face leads in the declared spin direction.
- **pass** `kin.balance_static`: Rotating groups are balanced Mass centres sit on the spin axis.
- **pass** `kin.balance_dynamic`: Weapon spins about a principal axis The weapon's principal axis matches its spin axis.
- **pass** `kin.spin_stability`: Weapon spins about its major axis Disc/bar weapons have their largest inertia about the spin axis.
- **pass** `kin.fastener_imbalance`: Screws on the weapon are balanced Screws carried by the weapon form a balanced pattern.
- **pass** `kin.sweep_static`: Nothing static is in a swept volume No static part lies inside the volume a rotating group sweeps.
- **pass** `kin.sweep_fastener`: No screw head or nut in a swept volume No static screw protrudes into a rotating group's sweep.
- **pass** `kin.outrunner_bell_rub`: Outrunner bells run clear Nothing static touches a spinning outrunner bell.
- **pass** `kin.lock_engages`: Locking bar stops the weapon The declared locking bar enters the weapon's swept volume.
- **pass** `kin.sweep_rotating`: Rotating groups clear each other No rotating group reaches into another's swept volume.
- **pass** `kin.wheel_axes_parallel`: Wheel axles are parallel All wheel axes within 0.5 deg.
- **pass** `kin.wheel_camber`: Wheels stand upright Wheel axes are horizontal within 1 deg.
- **pass** `kin.wheel_toe`: Wheels point forward Wheel axes are square to the direction of travel within 1 deg.
- **pass** `kin.wheel_height`: Wheels reach the same floor Lowest wheel points within 0.5 mm.
- **pass** `kin.wheel_motor_coaxial`: Wheels sit on their motor shafts Wheel axes on the motor shaft within 0.2 mm / 1 deg.
- **pass** `kin.shaft_engagement`: Hubs grip enough shaft Each driven hub covers at least 3 mm of motor shaft.
- **pass** `kin.belt_pulleys_joint`: Belt pulleys rotate Both pulleys of every belt are on rotating groups.
- **pass** `kin.belt_axes_parallel`: Belt pulley axes are parallel Pulley axes within 0.5 deg.
- **pass** `kin.belt_coplanar`: Belt grooves line up Pulley mid-planes within 0.5 mm.
- **pass** `kin.belt_same_group`: Belts link different shafts A belt's pulleys are on different rotating groups.
- **pass** `kin.tyre_retained`: Tyres are held on their hubs Every tyre is joined to its hub and sits on the rim.
- **pass** `kin.wire_to_rotor`: No wire ends on a rotating part Every wire ends on static parts or motor terminals.
- **pass** `tension.ok`: Forks and belts are tensioned 2 tensioned fork(s) and belt(s) checked.
- **pass** `targets.match`: Model matches the targets 4 target dimensions within tolerance.
- **pass** `shape.tall`: Low profile Body height 38.8 mm over width 103.8 mm = 0.37 (weapon excluded).
- **pass** `shape.aspect`: Length to width is reasonable L/W = 0.96.
- **pass** `shape.weapon_leads`: The weapon tip leads Nothing but low forks/wedgelets reaches further forward than the weapon's swept front (ground game leads by -9.5 mm, allowed -5).
- **pass** `shape.weapon_floor_reach`: Weapon sweeps close to the floor `blade_c` lowest sweep is 1.2 mm above the floor (axle 22.4 mm, rim 21.2 mm).
- **pass** `shape.armour_coverage`: Internals are covered top 96%, front 93%, back 97%, left 95%, right 95% of the view is armour or structure.
- **pass** `dynamics.tip_angle`: Stable against tipping Centre of mass 14.4 mm up; static tip angles back 73°, front 70°, left 74°, right 74°.
- **pass** `dynamics.traction`: Weight is on the driven wheels About 100% of the weight is on the driven wheels (rest on `tub`, `upright_l`, `upright_r`, `so_al`).
- **warning** `dynamics.invertible`: Cannot drive upside down Inverted, `wheel_rl` is 17.3 mm short, `wheel_fl` is 27.8 mm short, `wheel_rr` is 17.3 mm short, `wheel_fr` is 27.8 mm short of the floor; `blade_c`, `bspacer`, `disc_f`, `prop_mount`, `spacer` stick out above the wheels. Once flipped it is stuck unless it can self-right.
  - Fix: Make the wheels stand proud of the top, or add a self-righting feature.
- **pass** `dynamics.balance`: Weapon is balanced `blade_c` mass centre is 0.000 mm off the spin axis: grade G0.0 at 19320 rpm, a 0 N rotating load on the bearings and frame. That is 0.0x the robot's weight.
- **warning** `strength.shaft`: Weapon shaft not analysed `blade_c`: no shaft body passes through the weapon centre and into a support, so bending was not computed.
- **pass** `strength.bolt_pullout`: Bolts hold in the plastic 5 threaded joints each hold their share of the design impact 146 N (100 g on 149 g) with 1.5x margin.
- **warning** `printability.overhang`: Needs support to print `tub`: best print orientation is build-up -z, which still leaves 642 mm² of overhang steeper than 45° or bridge longer than 15 mm.
  - Fix: Chamfer overhangs to 45°, split the part, or accept support material.
- **warning** `printability.bridge`: Bridge too long `tub` printed build-up -z has a 53.8 mm bridge (limit 15 mm); it sags.
- **warning** `printability.overhang`: Needs support to print `top_armour`: best print orientation is build-up -y, which still leaves 166 mm² of overhang steeper than 45° or bridge longer than 15 mm.
  - Fix: Chamfer overhangs to 45°, split the part, or accept support material.
- **warning** `printability.bridge`: Bridge too long `top_armour` printed build-up -y has a 49.7 mm bridge (limit 15 mm); it sags.
- **warning** `printability.overhang`: Needs support to print `wedglet_l`: best print orientation is build-up +z, which still leaves 199 mm² of overhang steeper than 45° or bridge longer than 15 mm.
  - Fix: Chamfer overhangs to 45°, split the part, or accept support material.
- **warning** `printability.overhang`: Needs support to print `wedglet_r`: best print orientation is build-up +z, which still leaves 199 mm² of overhang steeper than 45° or bridge longer than 15 mm.
  - Fix: Chamfer overhangs to 45°, split the part, or accept support material.
- **pass** `printability.ok`: Printable without support 9 printed part(s) print support-free in their best orientation.
- **pass** `mfg.layer_load`: Weapon support layers carry the hit `upright_l` is printed along the spin axis.
- **pass** `mfg.layer_load`: Weapon support layers carry the hit `upright_r` is printed along the spin axis.
- **pass** `mfg.layer_load`: Weapon support layers carry the hit `bspacer` is printed along the spin axis.
- **pass** `process.ok`: Geometry matches the process 28 part(s) are makeable as declared.
- **warning** `shape.curvature`: Organic part is boxy `blade_c`: 9 of 747 faces curved (CYLINDER).
  - Fix: Use splines/lofts and fillet the edges (photo shows smooth shapes).
- **pass** `archetype.declared`: Archetype vertical_spinner_forks Held to the `vertical_spinner_forks` layout rules (26 rules).
- **pass** `archetype.disc_plane_vertical`: Disc spins in a vertical plane The spin axis is 0.0 deg out of the horizontal plane (vertical disc needs a horizontal axle, tol 5 deg).
- **pass** `archetype.axle_lateral`: Axle runs left-right The axle points 0.0 deg away from the left-right (X) axis (tol 5 deg).
- **pass** `archetype.rotor_joint`: Rotor has a spinning joint `blade_c` has a revolute joint about the spin axis.
- **pass** `archetype.rotor_fasteners`: No screw ties rotor to stator No fastener joins the rotor to a static part or passes through its swept volume.
- **pass** `archetype.disc_supported`: Disc sits between two supports Static structure on the axle line: yes on one side, yes on the other (the disc must sit between two supports).
- **pass** `archetype.disc_material`: Disc is metal stock Disc is `hardox` (metal) made by `laser`; it must be sheet- or bar-stock metal (laser/waterjet/milled/turned).
- **pass** `archetype.teeth`: Weapon has teeth The weapon outline has 2 tooth/teeth (wanted 2..2); a round edge skids off armour.
- **pass** `archetype.weapon_mass_fraction`: Weapon mass share Rotating mass is 25 % of the robot (wanted 18..50 %).
- **pass** `archetype.energy_ratio`: Weapon energy for its size Stored energy per robot mass is 50.5 J/kg (wanted 40..600 J/kg).
- **pass** `archetype.wedgelets_flank`: Blades either side of the disc Wedge/blade parts ahead of the disc axle: present on -X side, present on +X side.
- **pass** `archetype.blade_lead`: Blade tips just ahead of the disc Low forks/wedgelets lead the disc's swept front by is -9.5 mm (wanted -12..-5 mm).
- **pass** `archetype.disc_floor_gap`: Disc sweeps close to the floor The swept disc's lowest point above the floor is 1.2 mm (wanted 0.3..4 mm).
- **warning** `archetype.weapon_drive`: Weapon drive layout Weapon drive is `unconnected` (accepted: inside_hub, belt_tensioned).
  - Fix: Put the outrunner inside the hub, or belt-drive with a tensioner.
- **pass** `archetype.top_armour_slope`: Top armour slopes to the weapon The top armour slopes down toward the weapon at is 9.3 deg (wanted -5..25 deg).
- **pass** `archetype.drive_config`: Drive layout 4 wheels, 4 driven (4WD).
- **warning** `archetype.invertible`: Drives upside down Wheel tops stand -1.9 mm relative to the top of the chassis (need >= 0.5 mm to drive inverted).
  - Fix: Make the wheels stand proud of the top (or declare and prove `can_run_inverted`).
- **warning** `archetype.pods_enclose_wheels`: Side pods wrap the wheels Nothing outboard of wheel(s) `wheel_rl`, `wheel_fl`, `wheel_rr`, `wheel_fr` (side pods must wrap the wheels).
  - Fix: Add side pods/walls outboard of each wheel.
- **warning** `archetype.floor_ribs`: Not checked: Printed floor is stiffened Could not evaluate (no printed chassis tub).
  - Fix: Add the missing part or data so this rule can be measured.
- **warning** `archetype.lid_inserts`: Not checked: Lid screws go into inserts Could not evaluate (no removable lid fasteners).
  - Fix: Add the missing part or data so this rule can be measured.
- **warning** `archetype.switch_access`: Switch reachable from the side The switch is reachable only from the rear; the archetype puts it on a side wall.
  - Fix: Put the switch in a side-wall slot with nothing outboard of it.
- **pass** `archetype.axle_height`: Axle height on target Axle centre above the floor is 22.4 mm (wanted 21..24 mm).
- **pass** `archetype.disc_thickness`: Disc thickness on target Disc thickness is 14.0 mm (wanted 13..15 mm).
- **pass** `archetype.disc_diameter`: Disc diameter on target Disc diameter (incl. tooth) is 42.4 mm (wanted 41..45 mm).
- **warning** `archetype.tub_height`: Tub height on target Chassis tub height is 19.1 mm (wanted 13..17 mm).
  - Fix: Change the tub height.
- **pass** `archetype.wheel_dia`: Wheel size on target Largest wheel diameter is 21.5 mm (wanted 10..23 mm).
- **pass** `archetype.wheel_count`: Wheel count on target Number of wheels is 4.0  (wanted 4..4 ).
- **pass** `arch.tpu_skin`: Elastomer skin carries nothing `top_armour` (armor) is tpu but holds no other part; it is a hit-absorbing skin.
- **pass** `arch.tpu_skin`: Elastomer skin carries nothing `wedglet_l` (fork) is tpu but holds no other part; it is a hit-absorbing skin.
- **pass** `arch.tpu_skin`: Elastomer skin carries nothing `wedglet_r` (fork) is tpu but holds no other part; it is a hit-absorbing skin.
- **pass** `arch.tpu_structural`: No structure in elastomer No structural part is TPU or rubber.
- **pass** `arch.tpu_threaded`: No screws in elastomers No fastener threads into TPU or rubber.
- **warning** `arch.upright_brittle`: Weapon upright in a brittle print material `upright_r` carries the weapon and is pla_st, which cracks instead of bending on a hit.
  - Fix: Print weapon uprights in nylon, PETG or TPU-free tough blends, or use metal.
- **warning** `arch.upright_brittle`: Weapon upright in a brittle print material `upright_l` carries the weapon and is pla_st, which cracks instead of bending on a hit.
  - Fix: Print weapon uprights in nylon, PETG or TPU-free tough blends, or use metal.
- **pass** `arch.static_on_rotor`: Rotor carries only rotating parts Rotor `blade_c`: ['blade_c', 'bspacer', 'disc_f', 'prop_mount', 'spacer', 'wshaft'].
- **pass** `arch.weapon_spin_joint`: Weapon has a spin joint `blade_c` turns on a revolute joint.
- **pass** `arch.boundary_fasteners`: No screw crosses the spin boundary 27 fasteners checked.
- **pass** `arch.fastener_spans_joint`: No screw locks a joint 8 fastener/joint pairs checked.
- **warning** `arch.support_parent`: Weapon support hangs on the other support `upright_r` is parented to `upright_l`, the opposite weapon support; moving one drags the other and the tree no longer says both bolt to the chassis.
  - Fix: Parent `upright_r` to `tub`.
- **pass** `arch.support_parent`: Support parented sensibly `upright_l` parent: `world`.
- **pass** `arch.weapon_supports`: Weapon supported both sides Supports at -10.4 and 9.4 mm along the axis: `wbearing`, `weapon_motor`.
- **pass** `arch.fork_orientation`: Fork tine points at the axle `upright_r` holds side -1 at -10.4 mm; its body centre sits -9.0 mm along the axis and points toward the chassis from the axle.
- **pass** `arch.fork_orientation`: Fork tine points at the axle `upright_l` holds side +1 at 9.4 mm; its body centre sits 22.0 mm along the axis and points toward the chassis from the axle.
- **pass** `arch.bearing_coaxial`: Bearing on axis `wbearing` is 0.00 mm off the axis.
- **pass** `arch.bearing_seat`: Bearing seated `upright_r` surrounds 100 % of `wbearing` (Ø9.2).
- **pass** `arch.boss_aligned`: Axle boss aligned `weapon_motor` surrounds 100 % of the shaft at 9.4 mm.
- **pass** `arch.shaft_span`: Shaft span is short `wshaft` Ø5.0 mm spans 19.8 mm between supports (L/d = 4.0).
- **pass** `arch.weapon_centred`: Weapon centred `blade_c` mid-plane is +0.5 mm from the midpoint between its supports (-10.4 / 9.4 mm).
- **pass** `arch.weapon_support_gap`: Supports close to the weapon Clear shaft between the weapon faces and the supports: -5.1 / -10.6 mm (shaft Ø5.0).
- **pass** `arch.shaft_material`: Weapon shaft is metal `wshaft` is steel.
- **pass** `arch.shaft_retention`: Shaft is retained axially `wshaft` ends: open / open; declared retention: True.
- **pass** `arch.bearing_upright_choice`: Weapon in the stoutest upright Side -1: `upright_r` (0.0 mm on axis).
- **pass** `arch.bearing_upright_choice`: Weapon in the stoutest upright Side +1: `upright_l` (0.0 mm on axis).
- **pass** `arch.double_bearing`: One bearing system on the rotor `weapon_motor` does not share the weapon shaft.
- **pass** `arch.weapon_motor_in_hub`: Weapon motor inside the hub `weapon_motor` axis 0.00 mm off the spin axis, 100 % of its length inside the rotor envelope.
- **pass** `arch.load_path`: Weapon load reaches the chassis Side -1: shaft → upright_r → tub
- **pass** `arch.load_path_fasteners`: Load-path joint is bolted or seated `upright_r`→`tub`: 0 bolts, 143 mm² contact.
- **pass** `arch.load_path`: Weapon load reaches the chassis Side +1: shaft → upright_l → tub
- **pass** `arch.load_path_fasteners`: Load-path joint is bolted or seated `upright_l`→`tub`: 0 bolts, 155 mm² contact.
- **pass** `arch.fork_stiffness`: Fork is stiff `upright_r`: 73 N at the axle, lever 19.8 mm, weakest I 884 mm⁴, E 3.5 GPa → 0.06 mm.
- **pass** `arch.fork_stiffness`: Fork is stiff `upright_l`: 73 N at the axle, lever 19.8 mm, weakest I 2014 mm⁴, E 3.5 GPa → 0.03 mm.
- **pass** `arch.motor_mount`: Motor is screwed or clamped `weapon_motor`: 8 fasteners, 1 clamps, sandwiched between nothing.
- **pass** `arch.motor_clamp`: Motor is captured `weapon_motor`: structure on both sides along no axis; 8 screws in its face.
- **pass** `arch.motor_antirotation`: Motor cannot turn in its mount `weapon_motor`: 8 face screws, keyed False, flats held False.
- **pass** `arch.motor_face_bolts`: Motor face screw engagement ok `bolt_wm0` engages 2.0 mm of `weapon_motor` (usable 3.5 mm, need ≥ 1.6).
- **pass** `arch.motor_face_static`: Motor screw on the matching face `bolt_wm0` (static side) ends in the stator half of `weapon_motor` (stator face = opposite the catalog shaft output).
- **pass** `arch.motor_face_bolts`: Motor face screw engagement ok `bolt_wm1` engages 2.0 mm of `weapon_motor` (usable 3.5 mm, need ≥ 1.6).
- **pass** `arch.motor_face_static`: Motor screw on the matching face `bolt_wm1` (static side) ends in the stator half of `weapon_motor` (stator face = opposite the catalog shaft output).
- **pass** `arch.motor_face_bolts`: Motor face screw engagement ok `bolt_wm2` engages 2.0 mm of `weapon_motor` (usable 3.5 mm, need ≥ 1.6).
- **pass** `arch.motor_face_static`: Motor screw on the matching face `bolt_wm2` (static side) ends in the stator half of `weapon_motor` (stator face = opposite the catalog shaft output).
- **pass** `arch.motor_face_bolts`: Motor face screw engagement ok `bolt_wm3` engages 2.0 mm of `weapon_motor` (usable 3.5 mm, need ≥ 1.6).
- **pass** `arch.motor_face_static`: Motor screw on the matching face `bolt_wm3` (static side) ends in the stator half of `weapon_motor` (stator face = opposite the catalog shaft output).
- **pass** `arch.motor_face_bolts`: Motor face screw engagement ok `bolt_p0` engages 2.0 mm of `weapon_motor` (usable 3.5 mm, need ≥ 1.6).
- **pass** `arch.motor_face_static`: Motor screw on the matching face `bolt_p0` (rotating side) ends in the bell half of `weapon_motor` (stator face = opposite the catalog shaft output).
- **pass** `arch.motor_face_bolts`: Motor face screw engagement ok `bolt_p1` engages 2.0 mm of `weapon_motor` (usable 3.5 mm, need ≥ 1.6).
- **pass** `arch.motor_face_static`: Motor screw on the matching face `bolt_p1` (rotating side) ends in the bell half of `weapon_motor` (stator face = opposite the catalog shaft output).
- **pass** `arch.motor_face_bolts`: Motor face screw engagement ok `bolt_p2` engages 2.0 mm of `weapon_motor` (usable 3.5 mm, need ≥ 1.6).
- **pass** `arch.motor_face_static`: Motor screw on the matching face `bolt_p2` (rotating side) ends in the bell half of `weapon_motor` (stator face = opposite the catalog shaft output).
- **pass** `arch.motor_face_bolts`: Motor face screw engagement ok `bolt_p3` engages 2.0 mm of `weapon_motor` (usable 3.5 mm, need ≥ 1.6).
- **pass** `arch.motor_face_static`: Motor screw on the matching face `bolt_p3` (rotating side) ends in the bell half of `weapon_motor` (stator face = opposite the catalog shaft output).
- **pass** `arch.motor_mount`: Motor is screwed or clamped `motor_l`: 0 fasteners, 1 clamps, sandwiched between ['tub', 'base_panel', 'top_armour'].
- **pass** `arch.motor_clamp`: Motor is captured `motor_l`: structure on both sides along ['X', 'Y', 'Z']; 0 screws in its face.
- **pass** `arch.motor_antirotation`: Motor cannot turn in its mount `motor_l`: 0 face screws, keyed False, flats held True.
- **pass** `arch.motor_mount`: Motor is screwed or clamped `motor_r`: 0 fasteners, 1 clamps, sandwiched between ['tub', 'base_panel', 'top_armour'].
- **pass** `arch.motor_clamp`: Motor is captured `motor_r`: structure on both sides along ['X', 'Y', 'Z']; 0 screws in its face.
- **pass** `arch.motor_antirotation`: Motor cannot turn in its mount `motor_r`: 0 face screws, keyed False, flats held True.
- **pass** `arch.bolt_shear`: Bolt groups have shear margin 18 bolt groups have SF ≥ 2.0 in shear.
- **pass** `arch.bolt_bearing`: Bolt holes bear their load No printed hole is crushed by its bolt.
- **pass** `arch.bolt_bending`: No bolt bridges a gap No shank spans more than its diameter of air.
- **pass** `arch.bolt_washer`: Screw heads have bearing area Every head on plastic has enough area.
- **pass** `arch.insert_wall`: Insert bosses thick enough Insert walls ≥ 1.5 mm.
- **pass** `arch.layer_tension`: No load-path screw pulls layers apart Load-path screws lie in the layer plane.
- **pass** `arch.hole_spacing`: Hole spacing ok Parallel holes are ≥ 3d apart.
- **pass** `arch.insert_coaxial`: Inserts line up with screws Every insert is coaxial with its screw in a printed host.
- **pass** `arch.insert_host`: Inserts sit in printed bosses Every heat-set insert is surrounded by a printed part.
- **pass** `arch.cantilever_fastener`: No part levered off its screws 2 lightly-bolted parts checked.
- **warning** `arch.weapon_teeth`: Weapon tooth is blunt or soft `blade_c` tooth at r = 13.4 mm: tip radius ~1.30 mm, leading face 49° from radial, material hardox (hardened). tip radius 1.30 > 1 mm; face 49° off radial (> 30°): it ramps instead of biting.
  - Fix: Sharp (≤ 1 mm) tip, 0-30° leading face, hardened material (Hardox/AR500/S7, or declare `hardened: true`).
- **pass** `arch.foreign_through_rotor`: Nothing passes through the rotor Rotor `blade_c` is clear of static parts.
- **pass** `arch.holder_group`: Parts held by matching structure 21 parent/retainer links checked.
- **pass** `arch.cut_breakout`: Holes keep their webs 39 cylindrical cuts leave ≥ max(1 mm, 1.5x wall).
- **warning** `arch.armor_span`: Top armour span too long `top_armour` (tpu, ~1.3 mm) has an unsupported span of 48 mm: 300 N in the middle deflects 2854.5 mm.
  - Fix: Add a rib/post under the middle, more bolts, or thicker sheet.
- **pass** `arch.electronics_isolated`: Electronics off the load path `battery` touches no weapon support.
- **pass** `arch.battery_restraint`: Battery is boxed in `battery`: walls on both sides along ['Y', 'Z'], 5/6 sides; strap/clamp: False.
- **pass** `arch.electronics_isolated`: Electronics off the load path `rxesc` touches no weapon support.
- **pass** `arch.electronics_isolated`: Electronics off the load path `wesc` touches no weapon support.
- **pass** `arch.electronics_isolated`: Electronics off the load path `power_switch` touches no weapon support.
- **warning** `arch.symmetry`: Left/right parts differ `upright_l` mirrored differs from `upright_r` by 3.50 mm in extent and 27.9 % in volume.
  - Fix: Mirror one from the other, or list both in `asymmetric`.
- **pass** `arch.symmetry_fasteners`: Mirrored screws match 0 screw pairs mirror within 0.5 mm.
- **pass** `arch.com_support`: Centre of mass over the footprint Centre of mass (-0.4, 3.2) is inside the floor contact polygon by 34.8 mm.
- **pass** `arch.com_height`: Centre of mass low 14.4 mm up, 34.8 mm from the nearest tipping edge.
- **pass** `electrical.drive_motor_voltage`: Drive motors suit the pack voltage Pack 7.4 V nominal is within 1.5x of every drive motor's rating (worst 1.23x).
- **warning** `electrical.weapon_motor_voltage`: Not checked: Weapon motor suits the pack voltage Could not evaluate (no max_cells rating for weapon_motor).
  - Fix: Add the rating to the catalog entry or a `ratings` table on the part.
- **warning** `electrical.esc_voltage`: Not checked: ESCs rated for the pack voltage Could not evaluate (no cell rating for rxesc, wesc).
  - Fix: Add the rating to the catalog entry or a `ratings` table on the part.
- **pass** `electrical.esc_drive_current`: Drive ESC covers motor stall `rxesc` burst 6.0 A vs stall 1.6 A per channel.
- **pass** `electrical.esc_weapon_current`: Weapon ESC covers motor current `wesc` burst 18.0 A vs max 15.0 A per channel.
- **warning** `electrical.wire_ampacity`: Wire gauge carries the current Over capacity: `w_bat_sw` 24 AWG carries 11.4 A (rated 8.0 A).
  - Fix: Use a thicker wire (lower AWG).
- **pass** `electrical.connector_rating`: Battery connector rating Battery connector `xt30` rated 30 A; peak load 18.4 A.
- **warning** `electrical.switch_rating`: Not checked: Switch rating Could not evaluate (switch `power_switch` has no current rating (add `ratings.current_a`)).
  - Fix: Add the rating to the catalog entry or a `ratings` table on the part.
- **pass** `electrical.receiver_supply`: Receiver is powered Receiver `rxesc` is powered (wired to an ESC/BEC or integrated).
- **pass** `electrical.failsafe`: Failsafe covers every ESC Failsafe declared and every ESC takes its signal from the receiver.
- **warning** `electrical.indicator`: Power light visible No power indicator LED (a part with `led` in its id/label or `electronics.indicator`).
  - Fix: Add an LED that shows power, visible from outside.
- **pass** `electrical.battery_weapon_gap`: Battery clear of the weapon Battery is 5.2 mm from the weapon's swept volume (need >= 3 mm plus a wall).
- **pass** `electrical.battery_shielded`: Wall between battery and weapon A structural wall sits between the battery and the weapon.
- **pass** `electrical.battery_floor`: Battery protected from below Battery underside is 6.4 mm above the floor and is covered by structure below.
- **pass** `electrical.battery_removable`: Battery comes out without the weapon Battery comes out up past `top_armour`; no weapon part in the way.
- **pass** `electrical.wire_bend_radius`: Wire bend radius No routed wire bends tighter than 2x its diameter.
- **pass** `electrical.wire_rotating_clearance`: Wires clear of rotating parts Every routed wire stays >= 2 mm from rotating parts.
- **pass** `electrical.strain_relief`: Strain relief at ESC and battery Wires at the ESC/battery have slack and the parts are retained.
- **pass** `electrical.cells_consistent`: Cell count consistent Cell counts: battery 2S, electronics.cells 2S, blade_c.weapon.cells 2S.
- **pass** `electrical.switch_in_series`: Switch cuts all power Every ESC is powered through the switch.
- **pass** `electrical.power_path`: Power path complete Every ESC has battery power and every motor is wired to an ESC.
- **warning** `electrical.battery_c_rating`: Battery continuous rating Continuous load 11.4 A against 7.2 A (capacity x C).
  - Fix: Use a bigger or higher-C pack.
- **warning** `electrical.runtime`: Runtime covers a match Estimated runtime 1.7 min at match duty (need >= 3 min).
  - Fix: Use a bigger pack or lower the load.
- **pass** `electrical.wire_gauge_declared`: Wire gauges declared Every power and motor wire declares its gauge.
- **pass** `electrical.parts_retained`: Electronics retained Battery, ESCs and receiver declare how they are held.
- **pass** `electrical.weapon_disable`: Weapon can be disabled remotely Weapon remote disable declared.
- **warning** `combat.R001`: Front edge sits on the floor Median edge gap across the front is 9.22 mm (limit 1.5 mm).
  - Fix: Lower the front skirt/wedge lip to 0.3-1 mm.
- **warning** `combat.R002`: Front edge covered by a low skirt Share of the front edge with a skirt within 1.5 mm of the floor is 38% (needs 80%).
  - Fix: Run the wedge/skirt across the whole front at 0.3-1 mm.
- **pass** `combat.R003`: Left side has a low skirt Share of the left (+X) side edge within 3 mm of the floor is 100% (needs 60%).
- **pass** `combat.R004`: Right side has a low skirt Share of the right (-X) side edge within 3 mm of the floor is 100% (needs 60%).
- **warning** `combat.R005`: Rear edge is guarded Share of the rear edge within 3 mm of the floor is 0% (needs 50%).
  - Fix: Add a rear skirt or lower the rear wall to within 3 mm.
- **pass** `combat.R006`: Front-left corner closed Highest edge gap at the FL corner is 0.72 mm (limit 5 mm).
- **pass** `combat.R007`: Front-right corner closed Highest edge gap at the FR corner is 0.72 mm (limit 5 mm).
- **warning** `combat.R008`: Rear-right corner closed Highest edge gap at the RR corner is 99.00 mm (limit 5 mm).
  - Fix: Wrap the skirt round the corner or chamfer it down to the floor.
- **warning** `combat.R009`: Rear-left corner closed Highest edge gap at the RL corner is 99.00 mm (limit 5 mm).
  - Fix: Wrap the skirt round the corner or chamfer it down to the floor.
- **pass** `combat.R010`: Perimeter mostly skirted Share of the whole perimeter within 3 mm of the floor is 64% (needs 60%).
- **pass** `combat.R011`: No wide open arc Longest arc of the perimeter with nothing within 5 mm of the floor is 42.00 deg (limit 45 deg).
- **warning** `combat.R012`: No open door anywhere Highest edge gap anywhere on the perimeter is 99.00 mm (limit 12 mm).
  - Fix: Nothing on the outline should leave more than 12 mm under it.
- **warning** `combat.R013`: Gets under a typical wedge Front lip gap (20th percentile) against a typical 0.5 mm opponent wedge is 0.72 mm (limit 0.6 mm).
  - Fix: Lip at or below 0.5 mm wins the who-gets-under contest.
- **pass** `combat.R014`: Sides resist a T-bone Median side edge gap (worse side) when T-boned by a wedge is 0.72 mm (limit 2 mm).
- **warning** `combat.R015`: No fork-sized gap in the front edge Widest stretch of the front edge with no skirt within 1.5 mm of the floor is 33.39 mm (limit 8 mm).
  - Fix: Close gaps in the front skirt wider than 8 mm (opponent forks slip in).
- **warning** `combat.R016`: Front edge level Spread of the edge gap across the front is 24.32 mm (limit 3 mm).
  - Fix: Make the front edge height even across the width.
- **pass** `combat.R020`: Lip clears the floor `wedglet_l`: Lowest point above the floor is 0.72 mm (needs 0.2 mm).; `wedglet_r`: Lowest point above the floor is 0.72 mm (needs 0.2 mm).
- **pass** `combat.R021`: Lip is low enough `wedglet_l`: Lip height above the floor is 0.72 mm (limit 1 mm).; `wedglet_r`: Lip height above the floor is 0.72 mm (limit 1 mm).
- **warning** `combat.R024`: Sharp lip `wedglet_l`: Lip thickness 1 mm behind the edge is 2.87 mm (limit 1.2 mm).
  - Fix: Bevel the lip to <= 1.2 mm thick 1 mm back (or use 1 mm sheet).
- **warning** `combat.R025`: Thin lip `wedglet_l`: Lip thickness 3 mm behind the edge is 5.01 mm (limit 2.5 mm).
  - Fix: Keep the lip <= 2.5 mm thick 3 mm behind the edge.
- **warning** `combat.R026`: No blunt nose `wedglet_l`: Height of the vertical front face at the lip is 2.93 mm (limit 0.6 mm).
  - Fix: Remove the vertical face at the lip (> 0.6 mm stops it sliding under).
- **warning** `combat.R027`: Hard lip Lip material: `wedglet_l` tpu, `wedglet_r` tpu; a printed lip chips and rounds over.
  - Fix: Make the lip from steel/titanium/aluminium/laminate, or face it with metal.
- **pass** `combat.R028`: Skirt spans the front Front skirt width over body width is 100% (needs 40%).
- **pass** `combat.R029`: Skirt is the front-most part Skirt lead over the rest of the body (spinning parts excluded) is 0.00 mm (needs -0.5 mm).
- **pass** `combat.R030`: Tip does not dig in `wedglet_l`: Underside 3-13 mm behind the tip relative to the tip is -0.00 mm (needs -0.05 mm).; `wedglet_r`: Underside 3-13 mm behind the tip relative to the tip is -0.00 mm (needs -0.05 mm).
- **pass** `combat.R031`: Lip parallel to the floor `wedglet_l`: Lip height variation across its width is 0.00 mm (limit 0.5 mm).; `wedglet_r`: Lip height variation across its width is 0.00 mm (limit 0.5 mm).
- **pass** `combat.R032`: Skirt stiff under push `wedglet_l`: Tip deflection under 50 N (cantilever) is 0.15 mm (limit 1 mm).; `wedglet_r`: Tip deflection under 50 N (cantilever) is 0.15 mm (limit 1 mm).
- **pass** `combat.R033`: Skirt thick enough `wedglet_l`: Skirt thickness at mid-overhang is 5.16 mm (needs 2 mm).; `wedglet_r`: Skirt thickness at mid-overhang is 5.18 mm (needs 2 mm).
- **pass** `combat.R034`: Skirt overhang short `wedglet_l`: Unsupported overhang past the last support is 4.70 mm (limit 45 mm).; `wedglet_r`: Unsupported overhang past the last support is 4.70 mm (limit 45 mm).
- **warning** `combat.R037`: Skirt clears the wheels `wedglet_l`: Skirt clearance to the nearest wheel minus its load deflection is -0.15 mm (needs 1 mm).
  - Fix: Keep >= 1 mm between skirt and wheels after deflection.
- **pass** `combat.R038`: Skirt bolted down `wedglet_l`: Fasteners holding the skirt is 3.00  (needs 2 ).; `wedglet_r`: Fasteners holding the skirt is 3.00  (needs 2 ).
- **pass** `combat.R040`: At least two tines Fork tines is 2.00  (needs 2 ).
- **warning** `combat.R041`: Tines close together Widest gap between tines with nothing within 3 mm of the floor is 26.00 mm (limit 25 mm).
  - Fix: Keep gaps between tines <= 25 mm, or close them with the weapon/skirt.
- **pass** `combat.R042`: Tines level Height difference between fork tips is 0.00 mm (limit 0.5 mm).
- **pass** `combat.R043`: Tines lead the chassis Fork tips ahead of the chassis is 0.15 mm (needs 0 mm).
- **pass** `combat.R050`: Vertical weapon sweeps low `blade_c`: Vertical weapon sweep above the floor is 1.16 mm (range 0.8 to 6 mm).
- **pass** `combat.R051`: Weapon clears the floor `blade_c`: Weapon sweep above the floor is 1.16 mm (needs 0.3 mm).
- **pass** `combat.R053`: No gap under the weapon `blade_c`: Open floor gap under the weapon (no skirt below it) is 1.16 mm (limit 5 mm).
- **warning** `combat.R054`: Weapon and lip in step Weapon front relative to the skirt lip (negative = lip leads) is 9.54 mm (range -12 to 3 mm).
  - Fix: The lip should lead the weapon sweep by 0-12 mm (or the weapon lead by <= 3 mm).
- **pass** `combat.R060`: Weight on the driven wheels Weight on the driven wheels is 100% (needs 70%).
- **pass** `combat.R061`: Skirt is not carrying the robot Weight resting on the skirt or skids is 0% (limit 15%).
- **pass** `combat.R062`: Low centre of mass (track) Centre-of-mass height over track is 0.19  (limit 0.5 ).
- **pass** `combat.R063`: Low centre of mass (wheelbase) Centre-of-mass height over wheelbase is 0.18  (limit 0.6 ).
- **pass** `combat.R064`: Not top-heavy Centre-of-mass height as a share of body height is 43% (limit 50%).
- **pass** `combat.R065`: Centred sideways Sideways centre-of-mass offset over track is 0% (limit 5%).
- **pass** `combat.R066`: Centre of mass inside the wheelbase Centre of mass inside the wheelbase (share of wheelbase from the nearer end) is 48% (needs 10%).
- **pass** `combat.R067`: Grippy tyres Tyre materials: rubber, rubber, rubber, rubber.
- **warning** `combat.R068`: Wheels roll over seams Smallest wheel diameter (10x a 2 mm seam) is 11.00 mm (needs 20 mm).
  - Fix: Use wheels >= 20 mm diameter.
- **pass** `combat.R069`: Wide enough tyres Narrowest wheel width is 6.00 mm (needs 6 mm).
- **pass** `combat.R070`: Wheels on both sides Sides of the robot with a wheel is 2.00  (needs 2 ).
- **pass** `combat.R071`: 4WD turns 4WD wheelbase over track (turning scrub) is 0.81  (limit 1 ).
- **pass** `combat.R072`: Wide track Track over body width is 73% (needs 50%).
- **pass** `combat.R073`: Drive can spin the wheels Motor stall thrust 5.4 N over traction limit 1.3 N is 4.07 x (needs 1 x).
- **pass** `combat.R074`: Drive speed Top speed at nominal voltage is 1.27 m/s (range 1.2 to 8 m/s).
- **pass** `combat.R080`: Only wheels touch the floor Only the wheels touch the floor.
- **pass** `combat.R081`: Wheels coplanar Height difference between wheel contacts is 0.00 mm (limit 0.3 mm).
- **warning** `combat.R082`: Belly clears the floor Lowest point of the chassis (skirts and wheels excluded) is 0.30 mm (needs 1 mm).
  - Fix: Raise the chassis underside to >= 1 mm.
- **warning** `combat.R083`: No high-centring Underside clearance away from the edges (high-centring on a seam) is 0.30 mm (needs 1.5 mm).
  - Fix: Keep >= 1.5 mm under the interior so a 2 mm seam does not lift the wheels.
- **warning** `combat.R084`: No flat dragging belly Flat chassis underside within 0.5 mm of the floor is 214.20 mm2 (limit 50 mm2).
  - Fix: Recess flat underside areas that sit within 0.5 mm of the floor.
- **pass** `combat.R085`: Screw heads off the floor Lowest screw head above the floor is 1.05 mm (needs 0.5 mm).
- **pass** `combat.R086`: Switch off the floor Switch above the floor is 9.50 mm (needs 2 mm).
- **warning** `combat.R090`: Invertible or self-righting Body above the wheel tops (upside down the wheels must still reach the floor) is 12.35 mm (limit 0.5 mm).
  - Fix: Make the wheels stand proud of the top, or add a self-righting mechanism.
- **pass** `combat.R100`: Low profile Body height without wheels and weapon is 33.85 mm (limit 45 mm).
- **pass** `combat.R102`: Side armour angled Vertical share of the side-facing outer surface is 50% (limit 90%).
- **pass** `combat.R110`: No wheel at the front edge Share of front bearings where a wheel is the outermost part is 0% (limit 0%).
- **pass** `combat.R111`: Wheels shielded at the sides Share of the worse side where a wheel is the outermost part is 0% (limit 25%).
- **pass** `combat.R112`: Wheels shielded at the rear Share of rear bearings where a wheel is the outermost part is 8% (limit 25%).
- **pass** `combat.R113`: Wheels not the spinner target Share of the whole perimeter where a wheel is the outermost part (horizontal spinner target) is 4% (limit 10%).
- **pass** `combat.R114`: Body ahead of the wheels Body ahead of the front-most wheel is 14.15 mm (needs 5 mm).
- **pass** `combat.R115`: Side wall outboard of wheels Side wall outboard of the wheels is 9.40 mm (needs 0 mm).
- **pass** `combat.R116`: Wheels below the top Wheel top above the body top (non-invertible: wheels proud of the top get hit) is -22.85 mm (limit 0 mm).
- **pass** `combat.R120`: Battery away from the front Battery behind the front outline is 37.55 mm (needs 10 mm).
- **pass** `combat.R121`: Battery away from the sides Battery inside the side outline is 29.60 mm (needs 5 mm).
- **pass** `assembly.order`: Everything can be assembled Every part slides in along a clear straight path. Assembly order: rxesc, bolt_p3, bolt_d3, bolt_p2, bolt_d2, bolt_p1, bolt_p0, bolt_urb, bolt_ura, bolt_ulb, bolt_ula, prop_mount, spacer, disc_f, blade_c, weapon_motor, upright_r, upright_l, bolt_wm3, insert_b4, insert_b3, insert_b2, insert_b1, insert_b0, power_switch, wesc, battery, nut_cr, wheel_rr, whub_rr, motor_r, nut_cl, wheel_rl, whub_rl, motor_l, bspacer, wbearing, wshaft, wedglet_r, wheel_fr, whub_fr, so_br, so_ar, wedglet_l, wheel_fl, whub_fl, so_bl, so_al, top_armour, base_panel, bolt_d1, bolt_d0, bolt_src, bolt_srb, bolt_sra, bolt_slc, bolt_slb, bolt_sla, bolt_wm2, bolt_wm1, bolt_wm0, bolt_b4, bolt_b3, bolt_b2, bolt_b1, bolt_b0, belt_r, belt_l.
- **warning** `joint.no_locator`: Joint has no locating feature `upright_l` on `weapon_motor` is held in place only by friction and the screws' shear (`bolt_wm0`, `bolt_wm1`, `bolt_wm2`, `bolt_wm3`); no lip, step, pin or spigot locates it.
  - Fix: Add a lip, step or dowel so the parts register before the screws go in; screws clamp, features locate.
- **warning** `joint.no_locator`: Joint has no locating feature `upright_l` on `so_al` is held in place only by friction and the screws' shear (`bolt_ula`); no lip, step, pin or spigot locates it.
  - Fix: Add a lip, step or dowel so the parts register before the screws go in; screws clamp, features locate.
- **warning** `joint.single_fastener`: Joint held by a single screw `upright_l`-`so_al` is held by only `bolt_ula`; one screw lets the part pivot and loosen.
  - Fix: Use at least two screws, or key the joint (pin, flat, tab) and set `mechanical_key` on the connection.
- **pass** `joint.spigot_bore`: Part located on a coaxial spigot `wedglet_l` meets `so_al` round a bore coaxial with `bolt_sla`; the bore takes the shear, the screw clamps the end face.
- **warning** `joint.no_locator`: Joint has no locating feature `upright_l` on `so_bl` is held in place only by friction and the screws' shear (`bolt_ulb`); no lip, step, pin or spigot locates it.
  - Fix: Add a lip, step or dowel so the parts register before the screws go in; screws clamp, features locate.
- **warning** `joint.single_fastener`: Joint held by a single screw `upright_l`-`so_bl` is held by only `bolt_ulb`; one screw lets the part pivot and loosen.
  - Fix: Use at least two screws, or key the joint (pin, flat, tab) and set `mechanical_key` on the connection.
- **pass** `joint.spigot_bore`: Part located on a coaxial spigot `wedglet_l` meets `so_bl` round a bore coaxial with `bolt_slb`; the bore takes the shear, the screw clamps the end face.
- **warning** `joint.single_fastener`: Joint held by a single screw `wedglet_l`-`tub` is held by only `bolt_slc`; one screw lets the part pivot and loosen.
  - Fix: Use at least two screws, or key the joint (pin, flat, tab) and set `mechanical_key` on the connection.
- **warning** `joint.no_locator`: Joint has no locating feature `upright_r` on `so_ar` is held in place only by friction and the screws' shear (`bolt_ura`); no lip, step, pin or spigot locates it.
  - Fix: Add a lip, step or dowel so the parts register before the screws go in; screws clamp, features locate.
- **warning** `joint.single_fastener`: Joint held by a single screw `upright_r`-`so_ar` is held by only `bolt_ura`; one screw lets the part pivot and loosen.
  - Fix: Use at least two screws, or key the joint (pin, flat, tab) and set `mechanical_key` on the connection.
- **pass** `joint.spigot_bore`: Part located on a coaxial spigot `wedglet_r` meets `so_ar` round a bore coaxial with `bolt_sra`; the bore takes the shear, the screw clamps the end face.
- **warning** `joint.no_locator`: Joint has no locating feature `upright_r` on `so_br` is held in place only by friction and the screws' shear (`bolt_urb`); no lip, step, pin or spigot locates it.
  - Fix: Add a lip, step or dowel so the parts register before the screws go in; screws clamp, features locate.
- **warning** `joint.single_fastener`: Joint held by a single screw `upright_r`-`so_br` is held by only `bolt_urb`; one screw lets the part pivot and loosen.
  - Fix: Use at least two screws, or key the joint (pin, flat, tab) and set `mechanical_key` on the connection.
- **pass** `joint.spigot_bore`: Part located on a coaxial spigot `wedglet_r` meets `so_br` round a bore coaxial with `bolt_srb`; the bore takes the shear, the screw clamps the end face.
- **warning** `joint.single_fastener`: Joint held by a single screw `wedglet_r`-`tub` is held by only `bolt_src`; one screw lets the part pivot and loosen.
  - Fix: Use at least two screws, or key the joint (pin, flat, tab) and set `mechanical_key` on the connection.
- **warning** `joint.insert_boss`: Insert boss too thin Insert `insert_b0` (3.2 mm OD) sits in `tub` with only 62% of a 6.4 mm boss around it; heat-set inserts need a boss OD >= 2x insert OD.
  - Fix: Thicken `tub` around the insert to a 6.4 mm boss.
- **warning** `joint.head_proud`: Screw head proud on an outer surface The head of `bolt_b0` stands 2.0 mm proud of `base_panel` on the outside; hits shear heads and opponents catch on them.
  - Fix: Counterbore the head flush or use a countersunk (`head: countersunk`) screw.
- **warning** `joint.insert_boss`: Insert boss too thin Insert `insert_b1` (3.2 mm OD) sits in `tub` with only 62% of a 6.4 mm boss around it; heat-set inserts need a boss OD >= 2x insert OD.
  - Fix: Thicken `tub` around the insert to a 6.4 mm boss.
- **warning** `joint.head_proud`: Screw head proud on an outer surface The head of `bolt_b1` stands 2.0 mm proud of `base_panel` on the outside; hits shear heads and opponents catch on them.
  - Fix: Counterbore the head flush or use a countersunk (`head: countersunk`) screw.
- **warning** `joint.insert_boss`: Insert boss too thin Insert `insert_b2` (3.2 mm OD) sits in `tub` with only 62% of a 6.4 mm boss around it; heat-set inserts need a boss OD >= 2x insert OD.
  - Fix: Thicken `tub` around the insert to a 6.4 mm boss.
- **warning** `joint.head_proud`: Screw head proud on an outer surface The head of `bolt_b2` stands 2.0 mm proud of `base_panel` on the outside; hits shear heads and opponents catch on them.
  - Fix: Counterbore the head flush or use a countersunk (`head: countersunk`) screw.
- **warning** `joint.insert_boss`: Insert boss too thin Insert `insert_b3` (3.2 mm OD) sits in `tub` with only 62% of a 6.4 mm boss around it; heat-set inserts need a boss OD >= 2x insert OD.
  - Fix: Thicken `tub` around the insert to a 6.4 mm boss.
- **warning** `joint.head_proud`: Screw head proud on an outer surface The head of `bolt_b3` stands 2.0 mm proud of `base_panel` on the outside; hits shear heads and opponents catch on them.
  - Fix: Counterbore the head flush or use a countersunk (`head: countersunk`) screw.
- **warning** `joint.insert_boss`: Insert boss too thin Insert `insert_b4` (3.2 mm OD) sits in `tub` with only 54% of a 6.4 mm boss around it; heat-set inserts need a boss OD >= 2x insert OD.
  - Fix: Thicken `tub` around the insert to a 6.4 mm boss.
- **warning** `joint.head_proud`: Screw head proud on an outer surface The head of `bolt_b4` stands 2.0 mm proud of `base_panel` on the outside; hits shear heads and opponents catch on them.
  - Fix: Counterbore the head flush or use a countersunk (`head: countersunk`) screw.
- **warning** `joint.head_proud`: Screw head proud on an outer surface The head of `bolt_wm0` stands 2.0 mm proud of `upright_l` on the outside; hits shear heads and opponents catch on them.
  - Fix: Counterbore the head flush or use a countersunk (`head: countersunk`) screw.
- **warning** `joint.assembly_dir`: Screw not inserted along the part's assembly direction `upright_l` can only go on along [-0.0, -1.0, -0.0] but `bolt_wm0` is driven along [-1.0, 0.0, 0.0] (90 deg off); the screw cannot pull the part home onto its seat.
  - Fix: Drive the screws along the direction the part slides on, through its seat face.
- **warning** `joint.head_proud`: Screw head proud on an outer surface The head of `bolt_wm1` stands 2.0 mm proud of `upright_l` on the outside; hits shear heads and opponents catch on them.
  - Fix: Counterbore the head flush or use a countersunk (`head: countersunk`) screw.
- **warning** `joint.assembly_dir`: Screw not inserted along the part's assembly direction `upright_l` can only go on along [-0.0, -1.0, -0.0] but `bolt_wm1` is driven along [-1.0, 0.0, 0.0] (90 deg off); the screw cannot pull the part home onto its seat.
  - Fix: Drive the screws along the direction the part slides on, through its seat face.
- **warning** `joint.head_proud`: Screw head proud on an outer surface The head of `bolt_wm2` stands 2.0 mm proud of `upright_l` on the outside; hits shear heads and opponents catch on them.
  - Fix: Counterbore the head flush or use a countersunk (`head: countersunk`) screw.
- **warning** `joint.assembly_dir`: Screw not inserted along the part's assembly direction `upright_l` can only go on along [-0.0, -1.0, -0.0] but `bolt_wm2` is driven along [-1.0, 0.0, 0.0] (90 deg off); the screw cannot pull the part home onto its seat.
  - Fix: Drive the screws along the direction the part slides on, through its seat face.
- **warning** `joint.head_proud`: Screw head proud on an outer surface The head of `bolt_wm3` stands 2.0 mm proud of `upright_l` on the outside; hits shear heads and opponents catch on them.
  - Fix: Counterbore the head flush or use a countersunk (`head: countersunk`) screw.
- **warning** `joint.assembly_dir`: Screw not inserted along the part's assembly direction `upright_l` can only go on along [-0.0, -1.0, -0.0] but `bolt_wm3` is driven along [-1.0, 0.0, 0.0] (90 deg off); the screw cannot pull the part home onto its seat.
  - Fix: Drive the screws along the direction the part slides on, through its seat face.
- **warning** `joint.head_bearing`: Screw head crushes the plastic `bolt_ula` head bears 25 MPa on printed `upright_l` at ~400 N clamp; creep limit ~25 MPa.
  - Fix: Add a washer (`"washer": true`), use a flange/button head, or a larger head.
- **warning** `joint.head_proud`: Screw head proud on an outer surface The head of `bolt_ula` stands 3.0 mm proud of `upright_l` on the outside; hits shear heads and opponents catch on them.
  - Fix: Counterbore the head flush or use a countersunk (`head: countersunk`) screw.
- **warning** `joint.head_bearing`: Screw head crushes the plastic `bolt_sla` head bears 25 MPa on printed `wedglet_l` at ~400 N clamp; creep limit ~4 MPa.
  - Fix: Add a washer (`"washer": true`), use a flange/button head, or a larger head.
- **warning** `joint.head_bearing`: Screw head crushes the plastic `bolt_ulb` head bears 25 MPa on printed `upright_l` at ~400 N clamp; creep limit ~25 MPa.
  - Fix: Add a washer (`"washer": true`), use a flange/button head, or a larger head.
- **warning** `joint.head_proud`: Screw head proud on an outer surface The head of `bolt_ulb` stands 3.0 mm proud of `upright_l` on the outside; hits shear heads and opponents catch on them.
  - Fix: Counterbore the head flush or use a countersunk (`head: countersunk`) screw.
- **warning** `joint.head_bearing`: Screw head crushes the plastic `bolt_slb` head bears 25 MPa on printed `wedglet_l` at ~400 N clamp; creep limit ~4 MPa.
  - Fix: Add a washer (`"washer": true`), use a flange/button head, or a larger head.
- **warning** `joint.head_bearing`: Screw head crushes the plastic `bolt_slc` head bears 25 MPa on printed `wedglet_l` at ~400 N clamp; creep limit ~4 MPa.
  - Fix: Add a washer (`"washer": true`), use a flange/button head, or a larger head.
- **warning** `joint.head_bearing`: Screw head crushes the plastic `bolt_ura` head bears 25 MPa on printed `upright_r` at ~400 N clamp; creep limit ~25 MPa.
  - Fix: Add a washer (`"washer": true`), use a flange/button head, or a larger head.
- **warning** `joint.head_proud`: Screw head proud on an outer surface The head of `bolt_ura` stands 3.0 mm proud of `upright_r` on the outside; hits shear heads and opponents catch on them.
  - Fix: Counterbore the head flush or use a countersunk (`head: countersunk`) screw.
- **warning** `joint.head_bearing`: Screw head crushes the plastic `bolt_sra` head bears 25 MPa on printed `wedglet_r` at ~400 N clamp; creep limit ~4 MPa.
  - Fix: Add a washer (`"washer": true`), use a flange/button head, or a larger head.
- **warning** `joint.head_bearing`: Screw head crushes the plastic `bolt_urb` head bears 25 MPa on printed `upright_r` at ~400 N clamp; creep limit ~25 MPa.
  - Fix: Add a washer (`"washer": true`), use a flange/button head, or a larger head.
- **warning** `joint.head_proud`: Screw head proud on an outer surface The head of `bolt_urb` stands 3.0 mm proud of `upright_r` on the outside; hits shear heads and opponents catch on them.
  - Fix: Counterbore the head flush or use a countersunk (`head: countersunk`) screw.
- **warning** `joint.head_bearing`: Screw head crushes the plastic `bolt_srb` head bears 25 MPa on printed `wedglet_r` at ~400 N clamp; creep limit ~4 MPa.
  - Fix: Add a washer (`"washer": true`), use a flange/button head, or a larger head.
- **warning** `joint.head_bearing`: Screw head crushes the plastic `bolt_src` head bears 25 MPa on printed `wedglet_r` at ~400 N clamp; creep limit ~4 MPa.
  - Fix: Add a washer (`"washer": true`), use a flange/button head, or a larger head.
- **warning** `joint.head_proud`: Screw head proud on an outer surface The head of `bolt_d0` stands 2.0 mm proud of `disc_f` on the outside; hits shear heads and opponents catch on them.
  - Fix: Counterbore the head flush or use a countersunk (`head: countersunk`) screw.
- **warning** `joint.service_access`: Screw only reachable after removing another part The driver line out of `bolt_p0` hits `upright_r` 3.5 mm from the head; `upright_r` must come off before this joint can be serviced.
  - Fix: Turn the screw so its driver path exits through an open face or a removable cover, not through `upright_r`.
- **warning** `joint.head_proud`: Screw head proud on an outer surface The head of `bolt_d1` stands 2.0 mm proud of `disc_f` on the outside; hits shear heads and opponents catch on them.
  - Fix: Counterbore the head flush or use a countersunk (`head: countersunk`) screw.
- **warning** `joint.service_access`: Screw only reachable after removing another part The driver line out of `bolt_p1` hits `upright_r` 3.5 mm from the head; `upright_r` must come off before this joint can be serviced.
  - Fix: Turn the screw so its driver path exits through an open face or a removable cover, not through `upright_r`.
- **warning** `joint.service_access`: Screw only reachable after removing another part The driver line out of `bolt_d2` hits `upright_l` 5.5 mm from the head; `upright_l` must come off before this joint can be serviced.
  - Fix: Turn the screw so its driver path exits through an open face or a removable cover, not through `upright_l`.
- **warning** `joint.service_access`: Screw only reachable after removing another part The driver line out of `bolt_p2` hits `upright_r` 3.5 mm from the head; `upright_r` must come off before this joint can be serviced.
  - Fix: Turn the screw so its driver path exits through an open face or a removable cover, not through `upright_r`.
- **warning** `joint.service_access`: Screw only reachable after removing another part The driver line out of `bolt_d3` hits `wedglet_l` 10.0 mm from the head; `wedglet_l` must come off before this joint can be serviced.
  - Fix: Turn the screw so its driver path exits through an open face or a removable cover, not through `wedglet_l`.
- **warning** `joint.service_access`: Screw only reachable after removing another part The driver line out of `bolt_p3` hits `upright_r` 3.5 mm from the head; `upright_r` must come off before this joint can be serviced.
  - Fix: Turn the screw so its driver path exits through an open face or a removable cover, not through `upright_r`.
- **warning** `joint.screw_variety`: Too many different screws 6 different screws (M2x14, M2x6, M2x8, M3x10, M3x12, M3x16); a pit kit should need <= 5.
  - Fix: Adjust stacks so neighbouring joints share one length.
- **pass** `material.exempt`: Intentionally solid parts Not judged for excess material: top_armour (kind armor), wedglet_l (elastomer), wedglet_r (elastomer).
- **pass** `material.ok`: Material follows the loads 10 of 10 printed part(s) carry no chunky boss, solid core or load-free bulk.
- **pass** `plausibility.density`: Mass fits the envelope `weapon_motor` (weapon_motor): 18.5 g in 6.92 cm3 = 2.67 g/cm3 (plausible 1.5-7.5).
- **pass** `plausibility.density`: Mass fits the envelope `motor_l` (motor): 9.5 g in 1.91 cm3 = 4.97 g/cm3 (plausible 1.2-7.0).
- **pass** `plausibility.density`: Mass fits the envelope `motor_r` (motor): 9.5 g in 1.91 cm3 = 4.97 g/cm3 (plausible 1.2-7.0).
- **pass** `plausibility.density`: Mass fits the envelope `battery` (battery): 12.5 g in 7.13 cm3 = 1.75 g/cm3 (plausible 1.0-2.6).
- **pass** `plausibility.density`: Mass fits the envelope `rxesc` (esc): 3.5 g in 1.84 cm3 = 1.90 g/cm3 (plausible 0.4-4.0).
- **pass** `plausibility.density`: Mass fits the envelope `wesc` (esc): 3.0 g in 0.97 cm3 = 3.10 g/cm3 (plausible 0.4-4.0).
- **pass** `plausibility.density`: Mass fits the envelope `power_switch` (switch): 0.5 g in 0.18 cm3 = 2.79 g/cm3 (plausible 0.3-4.0).
- **pass** `reference.feature_ratio`: Proportion matches the reference `height_over_length`: model 0.388 vs photo 0.390 ± 0.030 (ref3 side: 263 px / 682 px)
- **pass** `reference.feature_ratio`: Proportion matches the reference `width_over_length`: model 1.036 vs photo 1.030 ± 0.040 (RVRN CAD: wedglet outer faces 104.1 (z_ref 0.52 mirrored) / 100.4 (disc tip x 8.22 to tyre x 108.59))
- **pass** `reference.feature_ratio`: Proportion matches the reference `disc_dia_over_length`: model 0.423 vs photo 0.425 ± 0.030 (RVRN CAD: tips at R21.5 -> 43 / 101)
- **pass** `reference.feature_ratio`: Proportion matches the reference `axle_z_over_disc_dia`: model 0.527 vs photo 0.520 ± 0.040 (RVRN CAD: axle y_ref 26.6 - floor 4.25 = 22.35 / 43)
- **pass** `reference.feature_ratio`: Proportion matches the reference `blade_stack_over_disc_dia`: model 0.330 vs photo 0.340 ± 0.040 (RVRN CAD: drisk = 3 mm Hardox disc + 8 mm printed spacer (ID 23.3 around the BE1806 can) + 3 mm floating disc = 14 mm on 41.25 mm). Spinner energy lives in a laminated ring at the rim, not one thin plate.
- **pass** `reference.feature_ratio`: Proportion matches the reference `rotor_mass_fraction`: model 0.254 vs photo 0.280 ± 0.030 (RVRN CAD + BOM: 2 x 14.7 g Hardox discs, 1.7 g spacer, prop mount, 4 long M2 + nuts and half the 18.5 g BE1806 (its bell turns with the drisk) of 150 g; the 31 g photo figure counted the plates only). Budget the rotor first; everything else gets what is left.
- **warning** `reference.feature_ratio`: Proportion differs from the reference `tub_len_over_length`: model 0.823 vs photo 0.600 ± 0.040 (ref3 tub 370 px / 682 px; SVRN box 66)
  - Fix: Move `tub_len_over_length` down by 0.223.
- **warning** `reference.feature_ratio`: Proportion differs from the reference `tub_h_over_height`: model 0.491 vs photo 0.400 ± 0.040 (ref3 / SVRN 17 mm)
  - Fix: Move `tub_h_over_height` down by 0.091.
- **pass** `reference.feature_ratio`: Proportion matches the reference `fork_span_over_width`: model 1.000 vs photo 1.000 ± 0.050 (RVRN CAD: the two low-profile wedglets are the outermost parts (outer faces z_ref 0.52 and its mirror))
- **pass** `reference.feature_ratio`: Proportion matches the reference `upright_symmetry`: model 1.124 vs photo 1.106 ± 0.050 (RVRN CAD: fl 31.23 tall vs fr 28.24 (the bearing-side plate is smaller))
- **pass** `reference.feature_ratio`: Proportion matches the reference `upright_thickness_mm`: model 4.000 vs photo 4.000 ± 0.500 (RVRN CAD fl/fr: 4 mm plates)
- **pass** `reference.feature_ratio`: Proportion matches the reference `heat_set_inserts`: model 5.000 vs photo 5.000 ± 3.000 (RVRN guide BOM: 5x M2 heat-set (base panel); uprights/side panels use alu standoffs + 2 press-fit alu M3 nuts)
- **pass** `reference.feature_ratio`: Proportion matches the reference `top_hood_height_mm`: model 6.000 vs photo 5.000 ± 2.000 (ref2 faceted hood; revron21/tpu photo: raised TPU hood with triangle cut-outs)
- **pass** `reference.feature_ratio`: Proportion matches the reference `weapon_lateral_offset_mm`: model 0.481 vs photo 0.000 ± 1.000 (ref2/revron21: disc centred between uprights)
- **warning** `reference.feature_ratio`: Proportion differs from the reference `pod_h_over_tub_h`: model 0.794 vs photo 1.000 ± 0.150 (RVRN CAD: low-profile wedglet / side panel 15 tall, chassis ~15)
  - Fix: Move `pod_h_over_tub_h` up by 0.206.
- **pass** `reference.feature_ratio`: Proportion matches the reference `rear_over_front_wheel_dia`: model 1.955 vs photo 1.950 ± 0.100 (RVRN CAD: F1 21.5 on the N10 at the rear, micro 11 on the front standoff). Small driven wheels on the motor shaft, belt to the big front wheel: no bearings, hubs or axles for the driven pair.
- **pass** `reference.feature_ratio`: Proportion matches the reference `battery_mass_g`: model 12.500 vs photo 12.500 ± 2.000 (RVRN BOM: Turnabot 2S 180 mAh)
- **pass** `reference.feature_ratio`: Proportion matches the reference `wheel_bearings`: model 0.000 vs photo 0.000 ± 0.000 (RVRN: front wheels run on greased alu standoffs, rear on motor shafts)
- **pass** `reference_cad.dims`: Part size matches the reference CAD `blade_c` vs `RVRN_1.7_PT_10_Drisk_Blade_Motor_Side-1.STL`: extents [32.99, 32.99, 3.0] vs [33.0, 32.95, 3.0] mm (diff [-0.0, 0.03, 0.0], tol 0.5)
- **pass** `reference_cad.volume`: Part volume matches `blade_c` volume 1.878 vs 1.860 cm3 (+1%, tol ±10%)
- **pass** `reference_cad.holes`: Holes, bores and bolt circles match `blade_c`: reference has 13 holes (d, r from centre) [(2.19, 4.5), (2.19, 4.5), (2.19, 4.5), (2.19, 4.5), (2.19, 14.0), (2.19, 14.0), (2.19, 14.0), (2.19, 14.0), (5.98, 0.0), (8.26, 9.46), (8.26, 9.46), (8.26, 9.46), (8.26, 9.46)]; model 13. Missing []; extra [].
- **pass** `reference_cad.silhouette`: Part shape matches the reference in all three views `blade_c` vs `RVRN_1.7_PT_10_Drisk_Blade_Motor_Side-1.STL` silhouette IoU along X/Y/Z [0.976, 0.997, 0.99] (need >= 0.9 on every axis, reference placed in our world frame)
- **pass** `reference_cad.dims`: Part size matches the reference CAD `disc_f` vs `RVRN_1.7_PT_10_Drisk_Blade_Motor_Side-1.STL`: extents [32.99, 32.99, 3.0] vs [33.0, 32.95, 3.0] mm (diff [-0.0, 0.03, 0.0], tol 0.5)
- **pass** `reference_cad.volume`: Part volume matches `disc_f` volume 1.338 vs 1.860 cm3 (-28%, tol ±35%)
- **pass** `reference_cad.silhouette`: Part shape matches the reference in all three views `disc_f` vs `RVRN_1.7_PT_10_Drisk_Blade_Motor_Side-1.STL` outline IoU along X/Y/Z [0.995, 0.997, 0.99] (need >= 0.9 on every axis, reference placed in our world frame)
- **pass** `reference_cad.dims`: Part size matches the reference CAD `spacer` vs `RVRN_1.7_PT_9_Drisk_Spacer-1.STL`: extents [26.29, 26.29, 8.0] vs [26.26, 26.26, 8.0] mm (diff [0.03, 0.03, 0.0], tol 0.5)
- **pass** `reference_cad.volume`: Part volume matches `spacer` volume 1.301 vs 1.360 cm3 (-4%, tol ±15%)
- **pass** `reference_cad.holes`: Holes, bores and bolt circles match `spacer`: reference has 5 holes (d, r from centre) [(2.19, 14.0), (2.19, 14.0), (2.19, 14.0), (2.19, 14.0), (23.27, 0.0)]; model 5. Missing []; extra [].
- **pass** `reference_cad.silhouette`: Part shape matches the reference in all three views `spacer` vs `RVRN_1.7_PT_9_Drisk_Spacer-1.STL` silhouette IoU along X/Y/Z [0.943, 0.997, 1.0] (need >= 0.9 on every axis, reference placed in our world frame)
- **pass** `reference_cad.dims`: Part size matches the reference CAD `upright_l` vs `fl-1.STL`: extents [36.29, 28.58, 4.0] vs [35.81, 28.06, 4.0] mm (diff [0.48, 0.52, 0.0], tol 0.8)
- **pass** `reference_cad.volume`: Part volume matches `upright_l` volume 2.176 vs 1.999 cm3 (+9%, tol ±15%)
- **warning** `reference_cad.holes`: Holes differ from the reference CAD `upright_l`: reference has 9 holes (d, r from centre) [(2.19, 4.63), (2.19, 7.43), (2.19, 13.42), (2.19, 14.22), (3.19, 10.94), (3.19, 13.17), (4.2, 3.86), (4.67, 8.38), (7.98, 8.05)]; model 9. Missing [(4.2, 3.86)]; extra [(3.03, 3.69)].
  - Fix: Add/move the missing holes (bolt circle radius, bore diameter).
- **pass** `reference_cad.silhouette`: Part shape matches the reference in all three views `upright_l` vs `fl-1.STL` silhouette IoU along X/Y/Z [0.929, 0.984, 0.985] (need >= 0.9 on every axis, reference placed in our world frame)
- **pass** `reference_cad.dims`: Part size matches the reference CAD `upright_r` vs `fr-1.STL`: extents [30.1, 28.23, 4.0] vs [30.09, 28.24, 4.0] mm (diff [0.01, -0.02, -0.0], tol 0.8)
- **pass** `reference_cad.volume`: Part volume matches `upright_r` volume 1.569 vs 1.550 cm3 (+1%, tol ±15%)
- **warning** `reference_cad.holes`: Holes differ from the reference CAD `upright_r`: reference has 5 holes (d, r from centre) [(3.19, 8.21), (3.19, 12.04), (4.66, 5.76), (4.67, 6.2), (7.98, 10.86)]; model 5. Missing [(4.67, 6.2), (7.98, 10.86)]; extra [(3.52, 5.59), (9.2, 11.22)].
  - Fix: Add/move the missing holes (bolt circle radius, bore diameter).
- **pass** `reference_cad.silhouette`: Part shape matches the reference in all three views `upright_r` vs `fr-1.STL` silhouette IoU along X/Y/Z [0.955, 1.0, 1.0] (need >= 0.9 on every axis, reference placed in our world frame)
- **pass** `reference_cad.dims`: Part size matches the reference CAD `base_panel` vs `RVRN_1.7_PT_8_Bottom_Panel-1.STL`: extents [55.2, 48.2, 1.0] vs [54.4, 47.4, 1.0] mm (diff [0.8, 0.8, 0.0], tol 0.8)
- **pass** `reference_cad.volume`: Part volume matches `base_panel` volume 2.516 vs 2.334 cm3 (+8%, tol ±15%)
- **warning** `reference_cad.holes`: Holes differ from the reference CAD `base_panel`: reference has 11 holes (d, r from centre) [(2.19, 23.63), (2.19, 27.57), (2.19, 27.57), (2.19, 32.25), (2.19, 32.25), (6.25, 18.16), (6.25, 18.16), (6.97, 25.25), (6.97, 25.25), (7.12, 28.11), (7.12, 28.11)]; model 9. Missing [(2.19, 23.63), (6.25, 18.16), (6.25, 18.16), (6.97, 25.25), (6.97, 25.25), (7.12, 28.11), (7.12, 28.11)]; extra [(2.19, 22.1), (4.72, 17.01), (4.72, 17.01), (5.35, 27.85), (5.35, 27.85)].
  - Fix: Add/move the missing holes (bolt circle radius, bore diameter).
- **pass** `reference_cad.silhouette`: Part shape matches the reference in all three views `base_panel` vs `RVRN_1.7_PT_8_Bottom_Panel-1.STL` silhouette IoU along X/Y/Z [0.985, 0.986, 0.929] (need >= 0.9 on every axis, reference placed in our world frame)
- **pass** `reference_cad.dims`: Part size matches the reference CAD `wedglet_l` vs `MirrorLow_profile_wedglet-2.STL`: extents [90.5, 33.9, 15.15] vs [90.45, 34.55, 15.0] mm (diff [0.05, -0.65, 0.15], tol 1.0)
- **warning** `reference_cad.volume`: Part volume differs from the reference CAD `wedglet_l` volume 6.551 vs 5.616 cm3 (+17%, tol ±15%)
  - Fix: Match wall thickness, pockets and lightening holes to the reference.
- **warning** `reference_cad.holes`: Through-hole count differs from the reference CAD `wedglet_l` has 6 through-holes, `MirrorLow_profile_wedglet-2.STL` has 9.
- **pass** `reference_cad.silhouette`: Part shape matches the reference in all three views `wedglet_l` vs `MirrorLow_profile_wedglet-2.STL` silhouette IoU along X/Y/Z [0.977, 0.921, 0.905] (need >= 0.9 on every axis, reference placed in our world frame)
- **pass** `reference_cad.dims`: Part size matches the reference CAD `wedglet_r` vs `MirrorLow_profile_wedglet-2.STL`: extents [90.5, 33.9, 15.15] vs [90.45, 34.55, 15.0] mm (diff [0.05, -0.65, 0.15], tol 1.0)
- **warning** `reference_cad.volume`: Part volume differs from the reference CAD `wedglet_r` volume 6.551 vs 5.616 cm3 (+17%, tol ±15%)
  - Fix: Match wall thickness, pockets and lightening holes to the reference.
- **warning** `reference_cad.holes`: Through-hole count differs from the reference CAD `wedglet_r` has 6 through-holes, `MirrorLow_profile_wedglet-2.STL` has 9.
- **pass** `reference_cad.silhouette`: Part shape matches the reference in all three views `wedglet_r` vs `MirrorLow_profile_wedglet-2.STL` silhouette IoU along X/Y/Z [0.977, 0.922, 0.907] (need >= 0.9 on every axis, reference placed in our world frame)
- **pass** `reference_cad.dims`: Part size matches the reference CAD `whub_rl` vs `RVRN_1.7_PT_13_Rear_Wheel-2.STL`: extents [16.0, 16.0, 12.0] vs [16.0, 15.98, 12.0] mm (diff [0.0, 0.02, 0.0], tol 0.8)
- **pass** `reference_cad.volume`: Part volume matches `whub_rl` volume 1.481 vs 1.499 cm3 (-1%, tol ±25%)
- **pass** `reference_cad.holes`: Through-hole count matches `whub_rl`: 2 through-holes.
- **pass** `reference_cad.silhouette`: Part shape matches the reference in all three views `whub_rl` vs `RVRN_1.7_PT_13_Rear_Wheel-2.STL` silhouette IoU along X/Y/Z [0.949, 0.939, 0.941] (need >= 0.9 on every axis, reference placed in our world frame)
- **pass** `reference_cad.dims`: Part size matches the reference CAD `whub_fl` vs `Micro_slx_v1.0-2_Hub_Micro-1.STL`: extents [9.2, 9.0, 9.0] vs [9.0, 8.99, 8.99] mm (diff [0.2, 0.01, 0.01], tol 0.8)
- **pass** `reference_cad.volume`: Part volume matches `whub_fl` volume 0.218 vs 0.218 cm3 (-0%, tol ±30%)
- **pass** `reference_cad.holes`: Through-hole count matches `whub_fl`: 1 through-holes.
- **pass** `reference_cad.silhouette`: Part shape matches the reference in all three views `whub_fl` vs `Micro_slx_v1.0-2_Hub_Micro-1.STL` silhouette IoU along X/Y/Z [0.909, 0.912, 0.922] (need >= 0.9 on every axis, reference placed in our world frame)
- **pass** `reference_cad.dims`: Part size matches the reference CAD `prop_mount` vs `RVRN_1.7_C4_BE1806_Prop_Mount_Unmodified-1.STL`: extents [15.0, 15.0, 14.05] vs [14.99, 14.99, 14.0] mm (diff [0.01, 0.01, 0.05], tol 0.5)
- **pass** `reference_cad.volume`: Part volume matches `prop_mount` volume 0.699 vs 0.631 cm3 (+11%, tol ±30%)
- **pass** `reference_cad.dims`: Part size matches the reference CAD `battery` vs `RVRN_1.7_C7_Turnabot_180mah_2s-1.STL`: extents [36.0, 18.0, 11.0] vs [36.0, 18.0, 11.0] mm (diff [0.0, 0.0, 0.0], tol 1.0)
- **pass** `reference_cad.volume`: Part volume matches `battery` volume 7.128 vs 7.119 cm3 (+0%, tol ±15%)
- **pass** `reference_cad.dims`: Part size matches the reference CAD `wheel_fl` vs `Micro_slx_v1.0-2_11OD_7ID_6W_Micro_slx-1.STL`: extents [11.0, 11.0, 6.0] vs [10.98, 10.98, 6.0] mm (diff [0.02, 0.01, 0.0], tol 0.5)
- **pass** `reference_cad.volume`: Part volume matches `wheel_fl` volume 0.339 vs 0.336 cm3 (+1%, tol ±25%)
- **pass** `reference_cad.dims`: Part size matches the reference CAD `wheel_rr` vs `RVRN_1.7_C5_Scalextric_F1_Front_tyre-1.STL`: extents [21.5, 21.49, 9.5] vs [21.5, 21.49, 9.5] mm (diff [0.0, 0.0, 0.0], tol 0.5)
- **pass** `reference_cad.volume`: Part volume matches `wheel_rr` volume 2.374 vs 2.201 cm3 (+8%, tol ±25%)
- **pass** `reference_cad.dims`: Part size matches the reference CAD `motor_r` vs `RVRN_1.7_C1_Turnabot_Spicy_N10_2200_RPM-1.STL`: extents [33.8, 12.0, 10.0] vs [33.8, 12.0, 10.0] mm (diff [0.0, 0.0, 0.0], tol 0.5)
- **pass** `reference_cad.volume`: Part volume matches `motor_r` volume 1.910 vs 1.807 cm3 (+6%, tol ±30%)
- **pass** `reference_cad.dims`: Part size matches the reference CAD `weapon_motor` vs `RVRN_1.7_C2_BBB_BE1806_Rough_Motor_Model-1.STL`: extents [29.83, 22.99, 20.5] vs [29.53, 22.96, 20.5] mm (diff [0.3, 0.03, 0.0], tol 1.0)
- **pass** `reference_cad.volume`: Part volume matches `weapon_motor` volume 6.918 vs 6.362 cm3 (+9%, tol ±30%)
- **pass** `reference_cad.dims`: Part size matches the reference CAD `wbearing` vs `MF85ZZ_Budget_Metal_Shielded_Flanged_Deep_Groove_Ball_Bearing_5x8x2.5mm-1.STL`: extents [9.2, 9.2, 2.5] vs [9.2, 9.19, 2.5] mm (diff [0.0, 0.01, 0.0], tol 0.3)
- **pass** `reference_cad.volume`: Part volume matches `wbearing` volume 0.086 vs 0.084 cm3 (+3%, tol ±30%)
- **pass** `cots.listed`: Bought-in parts are listed sizes 42 COTS parts and screws match catalog or standard sizes.
- **warning** `fit.tight`: Pocket too tight for the process `weapon_motor` has only 0.17 mm total clearance along z: 0.15 mm to `spacer`, 0.02 mm to `spacer`; the printed fit band needs at least 0.1 mm per side.
  - Fix: Open the pocket so print tolerance cannot make it an interference fit.
- **pass** `contain.electronics`: Electronics are inside the armour Every battery, ESC, receiver and motor sits inside the chassis envelope.
- **pass** `contain.wheels`: Wheels protrude as declared Wheels reach 0.3 mm below the body.
- **pass** `contain.wires`: Wires stay inside the chassis 7 routes checked against the chassis envelope.
- **pass** `contain.switch_access`: Switch reachable from outside `power_switch` has a clear 1.6 mm tool line out along -y.
- **pass** `disasm.elastic_stretch`: Belt can be stretched on and off `belt_l` needs 12 % stretch over the flange (rubber limit 50 %).
- **pass** `disasm.elastic_stretch`: Belt can be stretched on and off `belt_r` needs 12 % stretch over the flange (rubber limit 50 %).
- **pass** `disasm.graph`: Disassembly graph is acyclic and serviceable 69 nodes; every screw is reachable; serviceable parts within 8 removals (top_armour:0, blade_c:3, wheel_rl:0, wheel_fl:0, wheel_rr:0, wheel_fr:0, battery:0).
- **warning** `coverage.uncovered`: Parts or contacts no specific check covers 8 gap(s): pair `wheel_rl`/`wedglet_l` (0.40 mm): touching with no declared joint, connection or allowed contact; pair `whub_fl`/`wedglet_l` (0.30 mm): touching with no declared joint, connection or allowed contact; pair `wheel_fl`/`wedglet_l` (0.50 mm): touching with no declared joint, connection or allowed contact; pair `wedglet_l`/`belt_l` (0.13 mm): touching with no declared joint, connection or allowed contact; pair `wheel_rr`/`wedglet_r` (0.40 mm): touching with no declared joint, connection or allowed contact; pair `whub_fr`/`wedglet_r` (0.30 mm): touching with no declared joint, connection or allowed contact; pair `wheel_fr`/`wedglet_r` (0.50 mm): touching with no declared joint, connection or allowed contact; pair `wedglet_r`/`belt_r` (0.13 mm): touching with no declared joint, connection or allowed contact
  - Fix: Declare the relation (fastener, `connections`, `allow_overlap`, `retained`) or the material/process, so a check can verify it.
- **pass** `claim.holds`: Claim matches the model "weighs 150 g or less" (mass_total_g <= 150)
- **pass** `claim.holds`: Claim matches the model "fits the 150 mm square" (footprint_mm <= 150)

## Mass budget

| Part | Grams | Plus/minus | Source |
|---|---|---|---|
| tub | 11.83 | 2.37 | computed |
| base_panel | 2.65 | 0.53 | computed |
| top_armour | 4.74 | 0.95 | computed |
| upright_l | 2.70 | 0.54 | computed |
| upright_r | 1.95 | 0.39 | computed |
| so_al | 0.80 | 0.03 | computed |
| so_bl | 0.99 | 0.04 | computed |
| so_ar | 0.80 | 0.03 | computed |
| so_br | 0.99 | 0.04 | computed |
| weapon_motor | 18.50 | 0.55 | catalog |
| blade_c | 14.84 | 0.59 | computed |
| disc_f | 10.56 | 0.42 | computed |
| spacer | 1.37 | 0.27 | computed |
| prop_mount | 1.15 | 0.05 | computed |
| wshaft | 0.60 | 0.02 | computed |
| wbearing | 0.68 | 0.03 | computed |
| bspacer | 0.06 | 0.01 | computed |
| motor_l | 9.50 | 0.28 | catalog |
| whub_rl | 1.56 | 0.31 | computed |
| wheel_rl | 2.73 | 0.11 | computed |
| whub_fl | 0.23 | 0.05 | computed |
| wheel_fl | 0.39 | 0.02 | computed |
| wedglet_l | 6.68 | 1.34 | computed |
| nut_cl | 0.10 | 0.00 | catalog |
| motor_r | 9.50 | 0.28 | catalog |
| whub_rr | 1.56 | 0.31 | computed |
| wheel_rr | 2.73 | 0.11 | computed |
| whub_fr | 0.23 | 0.05 | computed |
| wheel_fr | 0.39 | 0.02 | computed |
| wedglet_r | 6.68 | 1.34 | computed |
| nut_cr | 0.10 | 0.00 | catalog |
| battery | 12.50 | 1.88 | catalog |
| rxesc | 3.50 | 0.53 | catalog |
| wesc | 3.00 | 0.45 | catalog |
| power_switch | 0.50 | 0.07 | catalog |
| insert_b0 | 0.12 | 0.02 | catalog |
| insert_b1 | 0.12 | 0.02 | catalog |
| insert_b2 | 0.12 | 0.02 | catalog |
| insert_b3 | 0.12 | 0.02 | catalog |
| insert_b4 | 0.12 | 0.02 | catalog |
| belt_l | 0.26 | 0.01 | computed |
| belt_r | 0.26 | 0.01 | computed |
| bolt_b0 | 0.25 | 0.01 | fastener |
| bolt_b1 | 0.25 | 0.01 | fastener |
| bolt_b2 | 0.25 | 0.01 | fastener |
| bolt_b3 | 0.25 | 0.01 | fastener |
| bolt_b4 | 0.25 | 0.01 | fastener |
| bolt_wm0 | 0.33 | 0.02 | fastener |
| bolt_wm1 | 0.33 | 0.02 | fastener |
| bolt_wm2 | 0.33 | 0.02 | fastener |
| bolt_wm3 | 0.33 | 0.02 | fastener |
| bolt_ula | 0.30 | 0.02 | fastener |
| bolt_sla | 0.36 | 0.02 | fastener |
| bolt_ulb | 0.30 | 0.02 | fastener |
| bolt_slb | 0.25 | 0.01 | fastener |
| bolt_slc | 0.29 | 0.01 | fastener |
| bolt_ura | 0.30 | 0.02 | fastener |
| bolt_sra | 0.36 | 0.02 | fastener |
| bolt_urb | 0.30 | 0.02 | fastener |
| bolt_srb | 0.25 | 0.01 | fastener |
| bolt_src | 0.29 | 0.01 | fastener |
| bolt_d0 | 0.52 | 0.03 | fastener |
| bolt_p0 | 0.30 | 0.01 | fastener |
| bolt_d1 | 0.52 | 0.03 | fastener |
| bolt_p1 | 0.30 | 0.01 | fastener |
| bolt_d2 | 0.52 | 0.03 | fastener |
| bolt_p2 | 0.30 | 0.01 | fastener |
| bolt_d3 | 0.52 | 0.03 | fastener |
| bolt_p3 | 0.30 | 0.01 | fastener |
| wires | 0.65 | 0.20 | wire |
| allowance | 1.20 | 0.60 | declared |

## Wire routes

| Wire | AWG | Diameter mm | Length mm |
|---|---|---|---|
| w_bat_sw | 24 | 1.6 | 55 |
| w_sw_wesc | 24 | 1.6 | 31 |
| w_wesc_m | 24 | 1.6 | 42 |
| w_sw_rx | 26 | 1.3 | 31 |
| w_m_l | 28 | 1.1 | 51 |
| w_m_r | 28 | 1.1 | 28 |
| w_rx_wesc | 30 | 0.9 | 38 |

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
- Shaft strength of `blade_c`: no supported shaft through the weapon centre
- Fork bending: forks are not traced to their mount; only weapon uprights are sectioned
- Process: single-profile neck width (web inside one outline) and fdm overhangs per declared orientation are not checked here
- Archetype rule `floor_ribs`: no printed chassis tub
- Archetype rule `lid_inserts`: no removable lid fasteners
- Electrical `weapon_motor_voltage`: no max_cells rating for weapon_motor
- Electrical `esc_voltage`: no cell rating for rxesc, wesc
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
