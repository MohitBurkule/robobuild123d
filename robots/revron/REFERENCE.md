# Revron reference v2

Our model is parametric and written from scratch. SVRN and the forum diary give **dimensions and specs only**. No SVRN geometry is imported.

## Sources
- **Project SVRN** by Shoverobotics, Printables model 1272536, licence CC-BY. Files used: `SVRN 4.0.step` (id 5310763) and `SVRN Belted.step` (id 6476965), both SolidWorks 2026 exports. These files were measured only and are not stored in the repo. Attribution: "Project SVRN Combat Robot" © Shoverobotics, CC-BY 4.0.
- Bristol Bot Builders forum, the Revron build diary (images in `photos/`).
- Photos in `photos/`:
  - `revron21_top.jpg`: Revron 2.1 render
  - `single_tooth_parts.jpg`: laminated tooth plates and the alu spider on the scale, ≈31 g
  - `weapon_assembly.jpg`: blade stack on the spider, with M3 set screws
  - `tpu_forks_top_armour.jpg`: TPU forks, top armour and fin
  - `chassis17_cad.jpg`: 1.7 chassis tub
  - `old_vs_new.jpg`
  - `ride_height.jpg`
  - `quickchange_weapon_cutaway.png`: same image as ref3
  - `svrn_printables_1-3`
  - `ref1-3`, `forum_*`

## Coordinate frame
X points right, Y points forward (weapon end) and Z points up. Z=0 is the underside of the chassis tub.

## Architecture
- **Weapon:** BE1806 outrunner. The drisk blades bolt to the motor bell through an aluminium spider. The motor is supported on both sides by uprights, with a flanged bearing on the rotating side. The blade stack is one long single tooth plus 2 outer Hardox blades, all laminated on the spider. The uprights are quick-change: they sit on square bosses, each fixed with 4× M3.
- **Drive:** 2× N10 gearmotors.
  - 4WD version (SVRN Belted layout): the motors sit at the front axle and drive the rear stub-axle wheels with O-ring belts.
  - Alternative (SVRN 4.0): 4 motors, one per wheel.
  - Tyres are Scalextric F1 fronts, ≈21.5 OD × 9.5–11 wide.
- **Electronics:** Malenki Nano RX/ESC under the top deck, a 2S ≈350 mAh LiPo and a BBB switch in a side wall.
- **Chassis:** a printed tube with an open bottom and a ≈1.2 mm top deck. A separate base panel (with X ribs) closes the bottom. M2 heat-set inserts at both ends of 6 posts take the base and top screws. The side panels fix with M3 countersunk screws into M3 aluminium nuts held in hex recesses. The motors sit in keyhole slots.
- **Armour:** TPU side panels form the forks and front wedge. The top is a TPU cover with a Ti plate.

## Parameter table
Also available as `params.json` (same keys).

| name | value | unit | source | tolerance |
|---|---|---|---|---|
| frame_note | X=right, Y=forward, Z=up, chassis underside Z=0 | - | SVRN STEP |  |
| chassis_len | 75.8 | mm | SVRN4.0 STEP | ±0.2 (incl. front lugs; box ≈66) |
| chassis_box_len | 66 | mm | SVRN4.0 STEP section | ±1 |
| chassis_width | 65.0 | mm | SVRN4.0 STEP | ±0.2 |
| chassis_height | 17.0 | mm | SVRN4.0 STEP | ±0.2 |
| chassis_wall | 2.0 | mm | SVRN4.0 STEP section | ±0.3 |
| chassis_top_deck_t | 1.2 | mm | SVRN4.0 STEP section | ±0.3 |
| chassis_bottom | open, closed by base panel | - | SVRN4.0 STEP |  |
| base_panel_size | 56.6 x 64.2 | mm | SVRN4.0 STEP | ±0.2 |
| base_panel_t | 2.5 | mm | SVRN4.0 STEP | ±0.2 (incl. X ribs) |
| base_panel_z | -0.5 | mm | SVRN4.0 STEP | recessed 0.5 below chassis rim |
| top_panel_size | 55 x 37 | mm | SVRN4.0 STEP | ±0.2 |
| top_panel_t | 0.9 | mm | SVRN4.0 STEP | steel/Ti 0.8-1.0 |
| top_panel_z | 17.0 | mm | SVRN4.0 STEP | sits on chassis top |
| ground_clearance | 1.75 | mm | SVRN4.0 STEP | ±0.5 (base underside -0.5 vs tyre bottom -2.25) |
| tyre_od | 21.5 | mm | SVRN4.0 STEP (Scalextric F1 front) | ±0.3 |
| tyre_width | 9.5 | mm | SVRN4.0 STEP | ±0.3 (nominal 11 per forum? verify) |
| hub_od_direct | 14.0 | mm | SVRN4.0 STEP SV06 | ±0.2 |
| hub_width_direct | 10.4 | mm | SVRN4.0 STEP | ±0.2 |
| hub_od_belted | 16.0 | mm | SVRN Belted STEP mw2/mod_wheel | ±0.2 |
| hub_width_belted | 12.0 | mm | SVRN Belted STEP | ±0.2 |
| axle_z | 8.5 | mm | SVRN4.0 STEP | ±0.2 above chassis underside |
| wheelbase | 52.4 | mm | SVRN4.0 STEP/SVRN Belted STEP | ±0.3 |
| track_direct | 70.3 | mm | SVRN4.0 STEP | ±0.3 tyre centre-centre |
| track_belted | 75.3 | mm | SVRN Belted STEP | ±0.3 |
| drive_motor | N10 gearmotor (Turnabot Spicy 2200 rpm in belted) | - | SVRN Belted STEP |  |
| drive_motor_envelope | 33.8 x 10 x 12 | mm | SVRN4.0 STEP | L incl. shaft x W x H |
| drive_motor_z_range | 2.5..14.5 | mm | SVRN4.0 STEP |  |
| drive_motor_y_front | 21.2..31.2 | mm | SVRN4.0 STEP | front pair; rear pair -31.2..-21.2 (direct 4WD) |
| drive_layout_belted | 2 motors at front axle; rear wheels on stub axles (M3 spacer 10 mm + ISO7380 M3x6) belted from front | - | SVRN Belted STEP | O-ring belts |
| stub_axle_plates | backing 3x10x12.8, front 1.9x11.4 dia | mm | SVRN Belted STEP | ±0.2 |
| rx_esc | Malenki Nano 32 x 20 x 4.4 | mm | SVRN4.0 STEP |  |
| rx_esc_z | 10.6 | mm | SVRN4.0 STEP | under top deck |
| battery_svrn | 120-180 mAh 2S, 36 x 18 x 11 | mm | SVRN4.0 STEP |  |
| battery_revron | 2S ~350 mAh | - | forum diary | size TBD (~50x30x15 photo est.) |
| switch | BBB antweight switch 20 x 5.8 x 7.2 | mm | SVRN Belted STEP | in side wall at X≈+22, Y -10..10 |
| insert | M2 heat-set, OD 3.5 x 4 L | mm | SVRN4.0 STEP | hole 3.2 |
| insert_xy | (±25,-16),(±25,+16),(0,-29),(0,+29) | mm | SVRN4.0 STEP | centres; ±0.2 |
| insert_z | bottom 2.6..6.6, top 12.4..16.4 | mm | SVRN4.0 STEP | both ends of each post |
| top_base_screws | M2x8 ISO14581 countersunk (FS8) into inserts | - | SVRN4.0 STEP/SVRN Belted STEP |  |
| side_panel_screws | M3x8 countersunk + M3 thin nut ISO4036 (5.5 AF, 1.8 t) in hex recess | - | SVRN4.0 STEP | 2 per side |
| side_panel_screw_pos | Y = -7.0 and +7.0, Z = 8.5 | mm | SVRN4.0 STEP | ±0.3 |
| module_screws | M3x10 (belted)/M3x14 alu CSK, axis along X at Y≈38, Z≈4 | mm | SVRN4.0 STEP | front weapon/module mount, 2x |
| side_panel_len | 103.5 | mm | SVRN4.0 STEP | belted: 130.4 incl. forks |
| side_panel_width | 38.3 | mm | SVRN4.0 STEP |  |
| side_panel_height | 20.8 | mm | SVRN4.0 STEP | z -2.0..18.8 |
| side_panel_wall | 3.0 | mm | SVRN4.0 STEP section | ±0.5 TPU |
| side_panel_front_wedge_tip_y | 70.2 | mm | SVRN4.0 STEP | wedge tip at z≈-2 |
| weapon_motor | BE1806 outrunner | - | forum diary |  |
| weapon_blades | single long tooth + 2 outer Hardox blades, bolted to bell via alu spider | - | forum diary/photo |  |
| weapon_blade_stack_mass | 31 | g | photo est. (scale photo) | ±3 |
| weapon_disc_dia | 53 | mm | photo est. | ±5 |
| weapon_axle_z | 30 | mm | photo est. | ±3 |
| weapon_upright_mount | square bosses + 4x M3 quick-change | - | forum diary | boss size TBD |
| overall_len_target | 145 | mm | photo est. | ≤150 box |
| overall_width | 99.5 | mm | SVRN4.0 STEP | Revron est 115-130 |
| mass_limit | 150 | g | UK antweight | hard |

## Still unknown or to measure
- BE1806 bell dimensions and mounting PCD (take from the datasheet: ≈23 mm bell, M2 holes on a 12/16 PCD, 5 mm shaft).
- Spider and blade profile, blade thickness and layer count. Bearing size (flanged, e.g. MF85/F695?).
- Square boss size, M3 spacing on the quick-change uprights, upright thickness and height.
- Revron chassis length/width if it differs from SVRN (Revron is longer because of the weapon). Keyhole slot dimensions. Battery bay size for 350 mAh.
- O-ring belt cross-section and pulley groove diameters (only the 16 mm hub OD is known).
- TPU top cover thickness and Ti plate size (SVRN top plate: 55×37×0.9).

## Appendix: v1 photo analysis (kept)

Sources: `photos/ref1.jpg` (printed chassis, top view), `photos/ref2.jpg` (CAD render, front-left iso), `photos/ref3.png` (CAD side section, weapon at left = front).
All three show the same version. Dimensions are estimates, scaled from ref3 assuming overall length ≈ 145 mm (blade tip to rear tyre) to fit the AWS 150 mm square.
Scale in ref3 ≈ 0.21 mm/px. Treat numbers as ±15 %; proportions matter more than absolutes.

## Overall layout (ref2, ref3)
- Low, flat, wide robot. Weapon is a vertical spinning disc/drum mounted IN FRONT of the body, between forked uprights.
- Order front→rear: blade wedgelet tips → disc → uprights/fork → tub with battery bay under angled top plate → rear wheels.
- Overall: L ≈ 145 mm, W ≈ 120-130 mm (pods included), tub height ≈ 22 mm, top of disc ≈ 55-60 mm above floor (only tall feature).
- Colours: tub/uprights/disc dark grey-black, side pods red, top plate brushed steel, blades steel.

## Chassis tub (ref1, ref3)
- One printed open-top box, outer ≈ 80 × 75 mm plan, wall ≈ 2-2.5 mm, height ≈ 22 mm.
- Floor: thin skin with a raised X-rib across the whole floor (corner-to-corner ribs ≈ 3 mm wide) plus a perimeter lip.
- Heat-set brass inserts: 4 in the corners (top-plate screws) + 1 at rear centre in a half-round boss. Total 5 visible.
- Rear wall: 3 small pockets/cut-outs along the rear inner wall (wheel-motor/ESC area), rear corners have small holes (axle/switch).
- Left wall: a rectangular slot (≈ 4 × 12 mm) with two small screw holes either side = power switch mount; a round hole below it (≈ 5 mm) = second access/LED or wire exit.
- Side tabs: one flat tab on each side (≈ 15 mm long × 35 mm wide, mid-length) for bolting the red side pods.
- Front edge carries the fork uprights (below).

## Fork uprights (ref1, ref2, ref3)
- 4 printed uprights rising from the tub front edge, integral with the tub:
  - 2 tall OUTER uprights (≈ 30 mm above tub top, ≈ 10 mm thick, rounded tips, with a through hole for the weapon axle near the top and a vertical ribbed/textured outer face).
  - 2 short INNER uprights (≈ 15 mm, rounded tops) just inside them; together each side forms a fork that clamps the axle/bearing block.
- Gap between outer uprights ≈ 40-45 mm (disc + hub sit between them).
- Side view (ref3): the upright is a triangular gusseted plate sloping from the tub top up to the axle boss, with a rectangular window (≈ 6 × 6 mm) and two red bolt heads lower down (where the blade/pod bolts through).

## Weapon (ref2, ref3)
- Vertical spinner, axle horizontal across the robot (left-right), axle centre ≈ 30 mm above floor, ≈ 25 mm ahead of the tub front.
- Disc/drum: ≈ 50-55 mm dia including tooth, ≈ 15-18 mm thick. Profile (ref3): roughly round body with ONE large hooked tooth (asymmetric, single-tooth "bar-disc"), two small balance holes near the rim.
- Inner hub: a toothed/lobed rotor (6-8 rounded lobes) — in ref2 visible as a star-shaped inner ring; the weapon motor is an outrunner sitting INSIDE the hub (drum-motor style) or directly behind it on the axle. Central bore ≈ 10 mm with a bearing block.
- Axle: steel, through both outer uprights, held by bolts/clamps (ref2 shows a round boss with a flat-sided shaft end).
- Disc lower edge ≈ 2-4 mm above the floor; tooth sweep reaches just behind the blade tips.

## Blade wedgelets (ref2, ref3)
- 2 long thin pointed steel blades, one each side of the disc, mounted under the uprights/pods.
- Each ≈ 45-50 mm long ahead of the uprights, ≈ 1-1.5 mm thick, triangular in plan tapering to a needle point, tip ≈ 0.5 mm off the floor, slight upward ramp toward the body.
- Bolted with 2 bolts (red heads in ref3) through the upright/pod.
- Blade tips are the front-most point of the robot.

## Side pods (ref2)
- 2 red printed pods, bolted to the tub side tabs; they wrap the wheels.
- Plan: long curved "C"/boomerang shape running full length, ≈ 15 mm wide, extending from the blades to past the rear wheels; front end is chunky with 2 round lightening holes and holds the blade root.
- Outer face has 3 diagonal slots (styling/lightening) mid-length.
- Wheel arches: curved cut-outs at front and rear; the wheels sit inside the arches, tyres slightly proud of the top.
- Pods height ≈ tub height, top edge curved down at front and rear.

## Drive (ref2, ref3)
- 4 wheels, all driven (rear wheel visible at rear of ref3, front wheel visible inside the front pod arch in ref2).
- Wheels ≈ 28-30 mm dia, ≈ 10-12 mm wide, black foam/rubber tyres on hubs.
- Wheels sit at the 4 corners just inside the pods; wheel tops protrude slightly above tub so the robot is drivable inverted.
- Motors: N20-class gearmotors inside the tub (rear pair visible in ref3 behind the battery). Assume 4 motors (one per wheel) unless mass forces 2 motors + belt/gear coupling front-rear.

## Top plate (ref2)
- Brushed steel/titanium plate over the tub, bent: flat over the rear ⅔, sloping DOWN toward the front (toward the weapon) at ≈ 20-25°; triangular side cheeks at the front bend.
- Screwed to the 4 corner inserts.

## Internals (ref3 section)
- Battery: large flat pack occupying the middle ≈ 50 × 30 × 15 mm, lying flat.
- Rear: drive motors + ESC behind the battery.
- Wires run inside the tub only.

## Build targets for the spec (`targets` block)
| item | value |
|---|---|
| overall length | 140-148 mm |
| overall width | 115-130 mm |
| tub height | 20-24 mm |
| disc dia | 50-56 mm, thickness 15-18 mm, single tooth |
| axle height | 28-32 mm |
| blade tip ahead of disc | 5-15 mm |
| wheels | 4 driven, 28-30 mm |
| mass | ≤150 g, disc ≥ 25 % |
