# Limpet XXT: design brief

> **UNTESTED: never built or run.** The spec passes the deep gate (`robot verify --tier full`, 0 blockers, mass 127.9 g);
> every number below is still an estimate from `src/limpet_xxt/params.py` relations and catalogue values.

## Architecture
- Four-wheeled invertible box, front-hinged full-width flipper. X is forward, the flipper end; the flipper rests at
  32 degrees sloping to the floor and opens to -42 degrees below the hinge line (joint range -42..0 about the hinge
  axis at x 21.8, z 21.5).
- **Flipper**: 1.5 mm clear PC sheet, 90 mm wide, chamfered front corners; hinged on an M2 pin pressed into the tub's
  outer knuckles, riding the plate's hinge bores and the printed centre knuckle's r1.3 bore (0.3 mm running fit).
- **Drive**: 4x N10 300 rpm 6V gearmotors, one per wheel, pressed into snug closed-top pockets through the side walls;
  the printed wheel hubs (TPU tyre, D-bore on the shaft) cup the gearbox cans. 0.30 m/s on 24 mm wheels.
- **Servo + linkage**: SG90-class servo lying on its side in the centre tray, output axis along +Y; a printed horn on
  the output shaft drives the flipper through a radial drive pin seated beyond the tail's angular shadow.
- **Battery + ESC**: 2S 180 mAh pack in the rear of the centre channel (taped), Malenki Nano (rx + dual brushed ESC) in
  the left side zone, BBB ant switch on its tray with the knob through a slot in the right lid (marked, tool-free).
- **Tub**: printed PLA unibody (wall ring, motor pockets, servo tray, lid pads, standoff bosses, hinge knuckles),
  rounded cavity corners (r1.2) and pad/wall seam fillets (r1.0) for the sharp-corner gate.
- **Armour**: clear PC side plates (elongated hexagon, M2 into heat-sets on standoff columns) and two lid plates
  (M2 into heat-sets in printed pads). Both lids carry an **armour deck** across the centre channel (z 21..22.5,
  x -49.5..7.0) that closes the channel from above against `contain.line_of_sight` while ending clear of the tail
  lever's sweep (the lever crosses the lid plane from x 7.57); the left deck's horn corridor (y 11.3..13.3 from x 1.8)
  passes the servo horn at max lift. Armour cover measured: top 0.985, front/back 1.0, sides 0.997/0.998.

## Load path / what rotates
| Rotates | Fixed |
|---|---|
| flipper, hinge block, tail lever, horn, drive pin, wheels (free on shafts) | tub, lids, side plates, standoffs, servo, motors |

Hit on the flipper face -> sheet -> hinge pin (M2 shear, safety factor 148) -> tub knuckles; the servo sees the load
only through the horn -> drive pin -> tail lever chain (pin shear 0.41 g part, seated beyond the tail's shadow).

## Size rule
`RULE_ERA = "aws_2025"` (150 mm floor square) by default; `aws_v4_3` (101.6 mm cube) also passes: footprint
**101.5 mm** x 100.0 mm, height 32.9 mm (no height limit). Expansion is the flipper joint angle only; at rest the
robot is inside both envelopes.

## Mass budget
Verifier total **127.9 g** (range 110.3-145.6; catalog estimates — weigh the real parts). Big items: 4x N10 30,
tub 22.0, servo 9.0, battery 12.5, 4x wheel 14.5, flipper 6.8, lids 8.0, side plates 6.5, hinge block 3.2 + pin 2.3,
ESC 3.5, switch 1.0, fasteners ~5.4, inserts 1.9, wires 1.1, horn + drive pin 0.6.

## Drive and fight numbers (verifier)
- 0.30 m/s top speed, 29.4 N push, 1.13 N traction; all four wheels driven (share 1.0).
- COG 11.6 mm high, 18.7 mm inside the drive patch; tip angles 52.6 to 79.3 degrees — invertible, tyres proud of the
  tub top and bottom by 1.5 mm.
- 2S 180 mAh: 6.2 min runtime against the 180 s fight; 4 A peak, 0.4 V pack sag.

## Service
1. Both lids off (4x M2) -> battery, ESC and switch out; the servo drops out of the tray upwards.
2. Side plates off (8x M2) -> motors and wheels exposed; each wheel pulls off its D-flat shaft.
3. Flipper: the hinge pin is pressed into the tub's outer knuckles; drift it out and the plate + hinge block + horn
   come off as one group.

## Risks
- Nothing run. The tub/pad/knuckle geometry is verifier-checked but never printed; expect tolerance surprises at the
  0.05 mm motor pocket fits and the M2 plastic taps (heat-sets are the fallback).
- The servo is **declared exposed** with a measured physical reason: it lies in the weapon corridor and the tail lever
  sweeps 1.4-2.6 mm above its case across the exposed band at full open, so no fixed cover fits without fouling the
  weapon. Its ends and underside are boxed by the tray and decks.
- The four motors are **declared exposed** with a measured physical reason: each gearbox can sits inside its printed
  wheel hub (0.00 mm gap), the only visible surface being the output-face annulus where the shaft enters the hub.
- Flipper servo torque is an SG90-class guess; the linkage's mechanical advantage at 32 degrees rest is not measured.
- The 0.30 m/s drive is slow even for a flipper; a 600 rpm motor swap is the first upgrade if it matters.
