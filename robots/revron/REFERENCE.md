# Revron reference: photo analysis

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
