# Verifier report: Reference 2WD wedge

Profile `aws2025`. 0 blockers, 2 warnings, 38 checks passed. Check set revision 9 (engine build123d).

Mass 114.6 g (range 93.6 to 135.6 g, limit 150 g).

## Findings

- **pass** `validity.ok`: Spec is well formed 19 parts, 8 fasteners, 5 wires.
- **pass** `wiring.route`: Every wire has a route 5 wires routed as real-thickness tubes through free space, 257 mm in total, no collisions.
- **pass** `mass.ok`: Within the weight limit 114.6 g (range 93.6 to 135.6 g) against the 150 g limit; 6.1 g of the uncertainty is catalog estimates, weigh the real parts and set `scale_mass_g`.
- **pass** `interference.overlap`: No parts collide 44 touching or overlapping pairs checked; touching is allowed, overlap deeper than 0.08 mm is not.
- **pass** `interference.sweep`: No joints to sweep No part has a joint.
- **pass** `interference.wheel_clearance`: Wheels run clear 2 wheels and tyres keep at least 1.0 mm from every part that does not turn with them.
- **pass** `retention.declared`: Held by declared method `battery` is held by velcro.
- **pass** `retention.declared`: Held by declared method `esc` is held by tape.
- **pass** `retention.declared`: Held by declared method `rx` is held by tape.
- **pass** `retention.declared`: Held by declared method `power_switch` is held by adhesive.
- **pass** `retention.captive`: Every loose part is held 6 parts checked, 4 held by a declared method, the rest captive in their pockets.
- **pass** `connection.joined`: Every part is attached All 19 parts lead back to the chassis through screws, shared prints, captive pockets, joints or declared connections.
- **pass** `ground.wheels_touch`: Wheels touch the floor All 2 wheels reach the floor plane (z = -14.00 mm).
- **pass** `ground.clearance`: Body clears the floor Lowest body part is 4.0 mm above the floor.
- **pass** `ground.wedge_gap`: Wedge tip height is right `wedge` tip is 0.60 mm above the floor.
- **pass** `ground.stance`: Stable on the floor Centre of mass is 18.8 mm inside the support polygon of wheels and wedge.
- **warning** `ground.wheel_exposed`: Wheel sticks out of the body `wheel_l` reaches open air from 53% of its side and upward rays above the belly line (allowed 5%); a spinner or a wall hits the tyre first.
  - Fix: Pull the wheel inside the outline, or add a side wall or guard over the exposed tread.
- **warning** `ground.wheel_exposed`: Wheel sticks out of the body `wheel_r` reaches open air from 45% of its side and upward rays above the belly line (allowed 5%); a spinner or a wall hits the tyre first.
  - Fix: Pull the wheel inside the outline, or add a side wall or guard over the exposed tread.
- **pass** `legal.switch`: Marked tool-free power switch `power_switch` is a marked, tool-free power switch.
- **pass** `switch.recess`: Switch is recessed `power_switch` sits 1.2 mm below the surrounding surface and slides across the robot.
- **pass** `legal.failsafe`: Failsafe declared The robot stops when the transmitter is switched off.
- **pass** `legal.footprint`: Fits the square Fits a 122.5 mm square (limit 150 mm).
- **pass** `fastener.ok`: Screws are reachable and bite 8 screws: driver path clear, thread engagement enough, heads seated.
- **pass** `power.battery`: Battery covers peak current Peak 2.0 A within the 7.2 A rating.
- **pass** `mfg.walls`: Walls are thick enough to make 5 made parts checked for minimum wall and bed size.
- **pass** `shape.tall`: Low profile Body height 28.0 mm over width 84.0 mm = 0.33.
- **pass** `shape.aspect`: Length to width is reasonable L/W = 1.46.
- **pass** `shape.weapon_leads`: The wedge edge leads Nothing reaches further forward than the wedge edge.
- **pass** `shape.armour_coverage`: Internals are covered top 100%, front 100%, back 100%, left 100%, right 100% of the view is armour or structure.
- **pass** `dynamics.tip_angle`: Stable against tipping Centre of mass 13.5 mm up; static tip angles back 62°, front 80°, left 71°, right 71°.
- **pass** `dynamics.traction`: Weight is on the driven wheels About 81% of the weight is on the driven wheels (rest on `wedge`).
- **pass** `dynamics.invertible`: Drives upside down Every wheel stands proud of the top, so it drives inverted.
- **pass** `strength.shaft`: No spinning weapon shaft No spinning weapon, so shaft and bearing loads are not computed.
- **pass** `strength.bolt_pullout`: Bolts hold in the plastic 8 threaded joints each hold their share of the design impact 112 N (100 g on 115 g) with 1.5x margin.
- **pass** `printability.ok`: Printable without support 5 printed part(s) print support-free in their best orientation.
- **pass** `process.ok`: Geometry matches the process 5 part(s) are makeable as declared.
- **pass** `shape.feature_direction`: Blade points forward `wedge` tip at [-41.0, 82.5, -11.5] points [-0.65, 0.71, -0.27] (forward = +y, dot 0.71); tip 2.5 mm above the floor; robot front is y = 82.5.
- **pass** `assembly.order`: Everything can be assembled Every part slides in along a clear straight path. Assembly order: insert_rr, insert_rl, insert_fr, insert_fl, rx, esc, battery, motor_r, motor_l, chassis_top, insert_wol, insert_wor, insert_wr, insert_wl, power_switch, wheel_r, wheel_l, wedge, bolt_rr, bolt_rl, bolt_fr, bolt_fl, bolt_wol, bolt_wor, bolt_wr, bolt_wl.
- **pass** `claim.holds`: Claim matches the model "weighs 150 g or less" (mass_total_g <= 150)
- **pass** `claim.holds`: Claim matches the model "fits the 150 mm square" (footprint_mm <= 150)

## Mass budget

| Part | Grams | Plus/minus | Source |
|---|---|---|---|
| chassis_bottom | 23.43 | 4.69 | computed |
| chassis_top | 23.07 | 4.61 | computed |
| wedge | 13.42 | 2.68 | computed |
| motor_l | 7.50 | 1.12 | catalog |
| motor_r | 7.50 | 1.12 | catalog |
| wheel_l | 6.42 | 1.28 | computed |
| wheel_r | 6.42 | 1.28 | computed |
| battery | 12.50 | 1.88 | catalog |
| esc | 3.00 | 0.45 | catalog |
| rx | 4.50 | 0.67 | catalog |
| power_switch | 0.50 | 0.07 | catalog |
| insert_wl | 0.12 | 0.02 | catalog |
| insert_wr | 0.12 | 0.02 | catalog |
| insert_wor | 0.12 | 0.02 | catalog |
| insert_wol | 0.12 | 0.02 | catalog |
| insert_fl | 0.12 | 0.02 | catalog |
| insert_fr | 0.12 | 0.02 | catalog |
| insert_rl | 0.12 | 0.02 | catalog |
| insert_rr | 0.12 | 0.02 | catalog |
| bolt_wl | 0.33 | 0.02 | fastener |
| bolt_wr | 0.33 | 0.02 | fastener |
| bolt_wor | 0.33 | 0.02 | fastener |
| bolt_wol | 0.33 | 0.02 | fastener |
| bolt_fl | 0.57 | 0.03 | fastener |
| bolt_fr | 0.57 | 0.03 | fastener |
| bolt_rl | 0.57 | 0.03 | fastener |
| bolt_rr | 0.57 | 0.03 | fastener |
| wires | 0.57 | 0.17 | wire |
| allowance | 1.20 | 0.60 | declared |

## Wire routes

| Wire | AWG | Diameter mm | Length mm |
|---|---|---|---|
| w_bat_sw | 26 | 1.3 | 101 |
| w_sw_esc | 26 | 1.3 | 21 |
| w_esc_ml | 26 | 1.3 | 25 |
| w_esc_mr | 26 | 1.3 | 27 |
| w_rx_esc | 26 | 1.3 | 83 |

## NOT CHECKED

The verifier did not judge these. A clean report says nothing about them.

- Strength: arm, fork and shell bending under impact (no stress or stiffness model; load path is not traced)
- Battery access and field service: swap time, number of fasteners to reach the battery or change a wheel
- Wire tether in assembly order: soldered wires between parts are not part of the disassembly sweep
- Heat-set insert iron clearance and soldering-iron access
- Gyro, spin-up time and ESC current limits of the weapon
- Thermal limits and glue or tape strength (declared only)
- Process: single-profile neck width (web inside one outline) and fdm overhangs per declared orientation are not checked here
