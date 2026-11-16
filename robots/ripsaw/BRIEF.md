# Ripsaw: design brief

> **UNTESTED: never built or run.** The spec passes the deep gate (`robot verify --deep`, 0 blockers, mass 145.7 g);
> every number below is still an estimate from `src/ripsaw/params.py` relations and catalogue values.

## Architecture
- Vertical single-tooth disc on the robot centreline, spinning up at the front. 44 mm OD, 3 mm hardox, laser cut; the
  rim/notch geometry keeps the balance window inside its spokes (numeric notch-moment closure, asserted in params.py).
- Hub motor: Repeat DirectDrive 2004 2800 kV, modelled as its split catalogue halves (`repeat_2004_stator` /
  `repeat_2004_can`). Disc bolts to the bell face (3x M3 on the 15 mm catalogue pattern); the stator bolts through the
  LEFT plate with 3x M2.5 into its back mounting ring.
- **Serviceable weapon plates** (the whole point of this revision): the stator plate (`mount_l`) and the bearing post
  plate (`post_r`) are printed nylon, bolted to integral pads on the tub's front wall with 3x M2x12 each, inserted from
  inside the tub and threading into tapped holes in the plates' 6 mm heels (5.4 mm of plastic thread). With both plates
  off, the weapon (disc + bell + shaft) slides forward out of the disc slot; the stator then lifts off its screws.
- Outboard support: MR63 (3x6x2.5, MF63 flanged class) pressed in `post_r`, flush with the plate's outer face; the
  motor's own 3 mm shaft runs on through it.
- 2WD: BBB N10 1000 rpm gearmotors in printed cradles (walls, capture ribs, axial stops — 0.2 mm play in every
  direction), inserted from below with the base panel off; the 20x8 wheels' hub bores are cut to the shaft's D-flat
  (flat 1.0 mm from the axis) and press on. Motor + wheel drop out together as one unit (declared teardown move).
- Battery: GNB 2S 450 mAh 80C (28 g) on the rear shelf — the 350 mAh class browns out at the 2004's 17 A peak and runs
  ~169 s against a 180 s fight. The Malenki Nano (rx + brushed ESC) rides the pack's top face under the strap; the
  weapon ESC (20 A) is double-side-taped to a printed ledge behind the cradle; the switch sits under a top-panel keyway
  (marked, tool-free).
- Ground game: two Revron fork_5 parts (1.5 mm Ti, reused unchanged), hung on M3 pins through the plates' outer faces —
  self-levelling skids, tips 0.5 mm off the floor so the wheels alone set the contact patch.
- Tub: printed nylon unibody (wall ring, rear shelf, cradles, front-wall pads, side-wall bosses, ESC ledge, strap
  posts), open top and bottom; printed base and top panels on M2 screws into heat-set inserts (as Revron).

## Load path / what rotates
| Rotates (weapon) | Fixed |
|---|---|
| disc, bell + shaft, disc screws | stator, both plates, tub, MR63 outer race, panels, forks (skids) |

Hit on tooth -> disc -> 3 bell screws (shear) -> bell/shaft -> (a) stator -> 3x M2.5 -> mount plate, (b) shaft end ->
MR63 -> post plate -> both plates -> 3x M2 each -> front-wall pads -> tub.

## Size rule
One setting, `RULES_SIZE` in params.py. Default `"aws2025"`: the 150 mm floor square (robot/profile.py), envelope 148 mm.
Sizing: TUB_BODY_L 78, RAIL_L 24. Optional `"aws_v43_cube"`: the 101.6 mm cube (TUB_BODY_L 52, RAIL_L 18).

| Extent (default, verifier) | Value |
|---|---|
| Footprint | 122 mm square (limit 150) |
| Width | TUB_W 84 mm (wheels inside, behind the walls) |
| Height | plate tops 37.4 mm (no height limit) |
| Fork tips | y 83, behind the disc front (y 79) |

## Mass budget (2S build)
Verifier total **145.7 g** (range 128.6-162.7; 8 g of the range is catalog estimates — weigh the real parts).
Big items: 2004 stator 5.5 + bell 6.0, disc 26 (hardox, 3559 mm3 x 7.9), battery 28, 2x N10 16, 2x wheel 3.6,
tub 21.4 cm3 nylon (x1.12 x0.85 about 20), panels 8.2, ESCs 7.3, switch 2.15, forks + pins 4.6, fasteners 3.5,
wires + XT30 4, allowance 1.2.

## Energy (verifier)
- 23520 rpm at 44 mm: tip 121 mph (limit 600); **about 15.4 J** at 85% of no-load speed.
- Bite: one tooth, TOOTH_STEP 6 mm radial against the closing-speed bite at own top speed (see disc.py relations).
- Drive: N10 1000 rpm at 6 V on 30 mm... on 20 mm wheels, about 1.3 m/s; the 450 mAh 80C pack (40 mOhm) holds the bus
  above 3.3 V/cell at the 17 A peak and runs the 180 s fight.

## Service (what the bolted plates buy)
1. Top panel off (4x M2) -> battery stack out (teardown move), switch through the keyway.
2. Base panel off (4x M2 csk) -> motor + wheel units drop out (teardown move, press fit stays engaged).
3. Weapon plates off (6x M2x12 from inside) -> the weapon slides forward out of the slot; stator lifts off its screws.
A bent fork is a pin-and-screw swap; the disc is a 3x M3 swap with the right plate off.

## Risks
- Nothing run. The cradle/plate/pad geometry is verifier-checked but never printed; expect tolerance surprises at the
  0.2 mm captive fits and the M2 plastic taps (heat-sets are the fallback).
- MR63 is a small bearing for a 15 J disc; check the shaft and bearing load after the first fights.
- 3x M3 into the bell carry all the torque (clearance fit); expect slip and wear at the disc screws.
- The balance window closure is a numeric notch moment, not a mass-properties run; spin-test the disc before fighting.
- The 2004 at 17 A peak is an estimate from the catalogue; spin-up time not measured.
- The gyro behaviour of a vertical spinner (stutter turns) is a declared archetype trade-off (adjudicated on PR #82).
