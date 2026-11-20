# Bzwroink: full reference description (rebuild-from-text)

Reference photos in `reference/` (all small and low resolution):

| File | Size (px) | Content | View |
|---|---|---|---|
| `bzwroink..._and_li_llest_stoink_.aws65.webp` | 170 x 157 | the two robots of the team (Bzwroink and "Li'llest Stoink") sitting on a wooden bench | left side, low elevation (about 25 degrees) |
| `bzwroink...aws61.webp` | 690 x 370 | one robot held upside down in a hand, close-up of the wheels and the clear scoop | left / underside, about 25 degrees |
| `bzwroink.aws68.webp` | 379 x 276 | a robot on a white floor tile, front three-quarter from above, with a second robot stacked or behind | front-left iso, about 45 degrees; the photo the likeness check uses |

Confidence marks:
- **[seen]** is directly visible.
- **[inferred]** is reasoned from the photos.
- **[guess]** is not visible, and is a plausible engineering answer.

Coordinates as in the spec: +y forward (scoop end), +x right, +z up, z = 0 the axle height.

---

## 1. Per-view description

### 1.1 aws65: the pair on the bench (side view)
- Two robots stand one in front of the other on a light wooden surface lit from above. Both are pink.
  - The upper one in the image (further from the camera) is the larger Bzwroink.
  - The lower one (nearer) is the small "Li'llest Stoink".
- **Bzwroink (upper) [seen]:**
  - It shows its left side. The front, with the clear scoop, is at the image left and the rear at the image right.
  - Body: a low, hot-pink rectangular box, about 2.2 times longer than tall in side view.
  - Wheels: four dark-pink or red discs along the side, two at the rear half, close together, one near the middle and one at the front-middle. [seen as 4 round shapes]. Their diameter is about 0.9 of the body height, so they reach almost to the top of the body.
  - Scoop: at the front left, a clear or silver-white plate sloping from the top front edge of the body down to the floor, ahead of the body, for about 0.3 of the body length.
  - A white or silver rectangular patch (tape or a label) lies on the top surface at the front, above the scoop. It is about 0.35 of the length.
- **Li'llest Stoink (lower) [seen]:**
  - A smaller pink box about 0.75 of Bzwroink's length.
  - A large white or silver label covers the middle of its side or top.
  - One red wheel or hub shows at the rear right, with a clear small wedge or cap at the front left.
  - It is a separate robot, possibly the second half of a cluster. [inferred]

### 1.2 aws61: in the hand
- A robot is held in someone's right hand, upside down: its wheels point up at the top left, so the camera sees the underside or top and the left side. [inferred from the wheels being on top]
- **Wheels [seen]:** two wheels in the same row, i.e. on one side.
  - Each is a pale pink tyre ring (about 3 mm radial thickness, 6-7 mm wide).
  - Inside is a hot-pink cup-shaped hub, with a central pale-pink axle boss about 0.3 of the wheel diameter and a smaller pin in its centre.
  - The hubs are recessed about 2-3 mm into the tyre ring, like a dish.
  - The two wheels nearly touch, about 2-3 mm apart. Their diameter is about 0.38 of the body length.
- **Body [seen]:**
  - Built from flat rectangular blocks wrapped in hot-pink duct tape. Tape seams and wrinkles show everywhere.
  - Black marker writing on the faces includes a "D" or arch shape and two short vertical strokes ("| |") on one face. On the scoop's pink part a large arc is drawn with a line under it, like a "D" or a smiling mouth.
- **Scoop [seen]:**
  - A clear polycarbonate sheet, about 1 mm thick, with scratches. Its corners are rounded or chamfered.
  - The sheet carries a pink-taped panel on its upper portion: the tape covers the rear 60% of the sheet.
  - The front 40% is bare clear plastic, bent or angled relative to the taped part by about 20-30 degrees.
  - The sheet extends beyond the body by about 0.35 of the body length.
  - A raised pink or white strip runs across it where the bend is: a tape edge.
  - The scoop is wider than the body face it sits on: it overhangs the side by about 2-3 mm.
- **Hand:** shows the scale. The body is about 75-80 mm long; a finger is about 18 mm wide. [inferred]

### 1.3 aws68: front-left iso on the floor (likeness photo)
- One pink robot fills the centre, with another pink robot or part behind it at the upper left.
- **Front robot [seen]:**
  - Body: a rectangular box covered in pink tape, its long axis running from the lower left to the upper right.
  - A raised rectangular block or step sits on top at the front: a pink, flat-topped "lid" with a pale-pink border.
  - A pink lid with handwritten marks ("V", "P") covers the top.
- **Wheels [seen]:** visible on the left side as round discs:
  - two front pale-pink wheels, close together, with dark pink or red hub centres;
  - rear wheels at the lower right, larger, deeper pink, with a darker red hub.
  - A grey axle bolt end or pin shows in each hub centre.
- **Scoop [seen]:**
  - At the image right, a clear plastic plate from the front of the robot sloping down to the floor, with a light reflection.
  - The scoop starts at the top front edge and reaches about 0.3 of the length ahead.
- **Second robot [seen]:** at the upper left, a pink body with a wheel, partly out of frame. It is the other cluster member, or the pair's second robot. [inferred]

---

## 2. Overall form (Bzwroink, the robot modelled)

- Type: a 4-wheel-drive pusher wedge (rammer) with a fixed clear scoop, built from taped blocks. [inferred]
- Size [inferred from hand scale and aws65]: body about 75-80 mm long (without the scoop), about 50-55 mm wide between the wheels, and about 28-32 mm tall.
  - The scoop adds about 25 mm at the front, so the overall length is about 100-105 mm.
  - The wheels add about 7 mm each side, so the overall width is about 64-70 mm.
- The shape is a brick: flat top, flat vertical sides, square ends.
- The scoop rests from the top front edge down to the floor, so in side view the front is a straight slope at about 25-35 degrees.

---

## 3. Parts

### 3.1 Chassis box: C1
- **Shape [seen]:** a rectangular box, about 78 x 50 x 30 mm, with crisp but slightly rounded taped corners. Tape layers add about 0.5 mm of bulk and visible wrinkles.
- **Colour [seen]:** hot pink, about #e8509a to #f060a8. Shaded faces are #c03a7c.
- **Construction [guess]:** a printed or cardboard and plastic tub wrapped in tape. In CAD: a printed nylon or PLA tub with a lid.
- **Top lid: C2 [seen in aws68]:**
  - A flat plate covering the top. It is a lighter pink, with a pale-pink 2-3 mm border.
  - It is inset about 2 mm from the body edges.
  - Handwritten black marks sit on it.
- **Contacts:**
  - The wheels sit outside its long sides, with about 1-3 mm gaps.
  - The scoop rests on its top front edge and front face.

### 3.2 Wheels: W1 to W4
- **Count:** 4, two per side. [seen in aws65 and aws68]
- **Position [inferred]:**
  - Front pair centred about 20 mm ahead of the body centre; rear pair about 22 mm behind it.
  - The wheels are close together: in aws61 the pair is almost touching, with a 2-3 mm gap between tyres, so the wheel centres are about 38-42 mm apart.
  - They sit outside the body sides, axle at about mid-height of the body.
- **Size [seen]:**
  - Diameter about 28-30 mm, so the wheel tops come about level with the body top.
  - Width about 6-8 mm.
  - The tyre ring's radial thickness is about 3-4 mm.
- **Colour:** tyre ring pale pink #f5b8d0; hub hot pink #e0408a or red #d02050; central boss pale pink.
- **Hub detail [seen]:**
  - A dish-shaped hub recessed 2-3 mm inside the tyre ring.
  - A central raised boss, about 8-9 mm in diameter.
  - A small pin, about 2 mm, in the boss centre: the motor shaft end or a grub screw.
  - In aws68 the rear wheels look like a solid deep-pink disc with a darker centre.
- **Gap to the body [inferred]:** 1-2 mm between the inner wheel face and the body side.
- **Drive [guess]:** one N20 gearmotor per wheel inside the body, its shaft through the side wall.

### 3.3 Scoop (wedge): S1
- **Material:** clear polycarbonate, about 0.8-1 mm, scratched and with a light reflection. [seen]
- **Shape [seen]:**
  - A rectangle about the body width plus 2 mm, by about 45 mm long overall.
  - Its rear part, about 25 mm, is covered in pink tape. That part lies on the body's top front, or forms the upper slope.
  - Its front part, about 20 mm, is bare and clear: the lip. Its free edge is straight, with small chamfered corners.
- **Angle [inferred]:**
  - The taped part slopes at about 30 degrees.
  - The clear lip is bent a little flatter, at about 15-20 degrees, so it reaches the floor about 25 mm ahead of the body.
  - The lip edge touches the floor (0-0.5 mm).
- **Fixing [seen]:** taped onto the body's front top edge with the pink tape wrapping over it. Taped joints read as a fixed connection, with no hinge.
- **Graphic [seen]:** a black marker "D" or arch on the pink-taped part.

### 3.4 Electronics (hidden) [guess]
- A 2S 180 mAh LiPo in the floor, centred.
- A combined receiver and ESC (Malenki nano) above it.
- A slide switch at the rear face, reachable through a slot.
- Four N20 motors in pairs along the side walls.

### 3.5 Fasteners
- None visible. Everything is taped. [seen]
- CAD screws on the lid are allowed, as small flush heads, but the photo shows none.

### 3.6 Graphics
- Black marker on the pink tape:
  - two vertical strokes on one face (aws61, lower left);
  - a "D" arc on the scoop;
  - letters on the lid in aws68.
- Optional. Small black stripes or arcs can be added as decals on the lid.

---

## 4. Part table

| ID | Part | Shape | Size (mm) | Colour | Joint | Fixing | Confidence |
|---|---|---|---|---|---|---|---|
| C1 | chassis tub | box | 78 x 50 x 30 | hot pink #e8509a | fixed | - | seen |
| C2 | lid | plate with border | 74 x 46 x 2 | light pink #ef90bb | fixed | tape (CAD: screws) | seen |
| W1-W4 | wheels | tyre ring + dish hub | 29 dia x 7 | pale pink ring, hot pink hub | rotating, axis x | on motor shafts | seen |
| S1 | scoop | bent clear sheet, rear half taped pink | 52 wide x 45 long x 1 | clear + pink | fixed | tape over the top front edge | seen |
| M1-M4 | N20 motors | boxes | 10 x 12 x 25 | - | fixed | pockets | guess |
| E | battery, ESC, switch | boxes | catalogue | - | fixed | pockets | guess |

## 5. Contact and gap matrix

| | C1 body | C2 lid | W wheels | S1 scoop | floor |
|---|---|---|---|---|---|
| C1 | - | the lid sits on the top rim | 1-2 mm gap to the inner wheel face | the scoop rests on the front top edge and the upper front face | body bottom 3-5 mm up |
| C2 | rim | - | wheel tops about level with the lid | front edge of the lid near the scoop's rear end, 0-2 mm | - |
| W | gap | - | front and rear wheels on one side 2-3 mm apart | front wheel to the scoop side edge, about 3-5 mm behind | tyre contact |
| S1 | taped | - | - | - | lip 0-0.5 mm |

## 6. Mechanism
- None besides the drive: a static wedge pusher with 4WD skid steering.

## 7. Rebuild recipe
1. Body: a 78 x 50 x 30 mm pink box, with its floor about 4 mm above the ground.
2. Four wheels of 29 mm diameter outside the sides, at y = +20 and y = -22, with their axles at the body mid-height.
3. Clear scoop, about 1 mm thick:
   - from the top front edge of the body (y about +39, z about +15) down to the floor at y about +65;
   - a two-segment plate, the upper part pink and the lower part clear, with a slight flattening bend.
4. Lid: a lighter pink plate on top with a 2 mm border.
5. Wheels:
   - pale-pink tyre rings with hot-pink dished hubs;
   - a raised pale centre boss, about 8 mm in diameter, protruding about 1 mm;
   - a grey pin in the boss centre.
6. Optional black marker decals on the lid.

## 8. Differences to watch against the CAD
- The scoop must start at the TOP front edge of the body and slope down. A flat plate lying on the floor ahead of the body is wrong.
- The wheels must show a two-tone ring and dished hub. Plain solid pink cylinders are wrong.
- The front and rear wheel pairs are close together, with tyres almost touching (2-3 mm gap).
- No screws visible in the photo. A taped look is acceptable.

## 9. Notes on low resolution
- All three photos are under 700 px wide.
  - Details like the exact hub boss size, the lid border width and the marker graphics are estimates. [guess]
  - The colour values are reliable to about +-15 per channel.
- The likeness check uses only aws68. In that view the dominant features are:
  - the pink box;
  - the scoop at the image right;
  - the wheel discs along the left side.
  The outline matters most there.

## 10. Symmetry
- The robot is left-right symmetric: build one side and mirror it. The only asymmetric items are the marker graphics.

---

## 11. Coordinate frame

- The origin is at the body centre in plan.
- z = 0 is the wheel axle height. The floor is at z = -14 to -15, because the wheels are about 29 mm in diameter.
- +y points forward (scoop), +x right, +z up. Units are mm and degrees.
- Pitch is measured from the floor.

## 12. Every part in all dimensions

| Part | L (y) | W (x) | H (z) | Thickness | Radii | Angles | Coordinates |
|---|---|---|---|---|---|---|---|
| C1 body | 78 +- 5 | 50 +- 4 | 30 +- 3 | wall 2-2.5 (printed) | taped corners r about 1.5 | - | y -39 to +39, x +-25, z -11 to +19 |
| C2 lid | 74 | 46 | 2 | 2 | corner r 1 | flat | z +17 to +19 |
| C2 border | strip 2-3 wide round the lid | - | flush | - | - | - | inset 2 from the body edge |
| W tyre ring | - | 7 | - | radial 3.5 | outer r 14.5, inner r 11 | axis x | centres (+-33, +20, 0) and (+-33, -22, 0) |
| W hub dish | - | recessed 2.5 | - | web 1.5 | r 11 | - | flush to 2.5 inside the tyre face |
| W centre boss | - | protrudes 1 above the dish | - | - | r 4.25 | - | wheel centre |
| W pin | - | 1 | - | - | r 1 | - | boss centre |
| S1 scoop, taped part | 25 along slope | 52 | rise about 13 | 1 | corner r 2 | pitch 30 | from (y 39, z 17) to (y 61, z 4.5) |
| S1 scoop, clear lip | 20 along slope | 52 | rise about 5 | 1 | corners chamfered 2 x 45 | pitch 15-18 | from (y 61, z 4.5) to (y 80, z -14.5) |
| Marker strokes | 10-14 long | 1.5 wide | - | flush decal | - | vertical | on the side or lid |

## 13. Curves (math)

- Wheel tyre outer edge, in the plane x = x_w: (y - y_c)^2 + (z - 0)^2 = 14.5^2, with y_c = +20 or -22.
- Hub dish, as an annulus: 4.25 <= r <= 11, at x offset 2.5 inboard of the tyre's outer face.
- Centre boss: a cylinder r = 4.25, protruding 1 mm from the dish.
- Scoop side profile: a polyline (two straight segments with a bend):
  - z = 17 - tan(30 deg) * (y - 39) for y in [39, 61];
  - z = 4.3 - 0.98 * (y - 61) for y in [61, 80] (lip segment, about 44 degrees, a 19 mm drop to the floor at z = -14.5).
- Taped corner rounds on the body: r about 1.5 on all vertical edges.

## 14. Independent measurements

| Quantity | (a) Pixels | (b) Ratios | (c) Engineering | (d) CAD | Reconciled |
|---|---|---|---|---|---|
| Body length | aws61: about 2.3 finger widths (18 mm each) from the wheel pair to the scoop root | wheel dia 0.38 x the length | a 2S 180 battery (about 45) plus 2 N20s in line need at least 70 | 78 in the current spec | 78 |
| Wheel diameter | aws61: the wheel is about 120 px against a 320 px body side | about the body height (0.9-1.0) | N20 shafts, 29 mm printed wheels are common | 29 | 29 |
| Wheel spacing | aws61: tyres about 8 px apart at 120 px dia, so a 2-3 mm gap | centres 1.05-1.45 x the wheel dia apart | the motors are 25 long each, back to back | 42 (y +20 / -22) | 42 |
| Scoop reach | aws65: the scoop is about 25% of the total length | 0.32 x the body length | wedge reach for a pusher is typically 20-30 | ends at y = +80 | about 40 past the body front |
| Body height | aws65: height to length 0.38-0.42 | the wheels reach the top | the electronics stack is about 22 | 30 | 30 |

## 15. Consistency check

1. **Scoop angle.**
   - aws65 shows a single straight slope at about 30 degrees. aws61 shows a bend between the taped and clear parts.
   - With the body top at z = +19 and the floor at -14.5, a single 30-degree slope reaches the floor about 58 mm ahead: too long against aws65's 25-30% of the length.
   - Reconciled: the upper part at 30 degrees, the clear lip steeper (about 40-45 degrees), so the scoop ends about 40 mm ahead of the body.
   - In the current CAD the scoop is a flat plate on the floor. This is wrong against every photo and should be changed.
2. **Wheel size.** The front pair looks smaller and paler than the rear pair in aws68. The two robots of the cluster have different wheels. Reconciled: Bzwroink has 4 equal wheels, matching aws61.
3. **Lid.** Seen only in aws68, which may show the other robot. Kept as an optional lighter-pink plate.
4. **Colour of the hubs.** Red in aws65 and pink in aws61, depending on the lighting. Reconciled: hot pink #e0408a.

## 16. Why the designer did it (per part)

### C1 taped box body
- **Fight:** a compact, low, rigid brick is hard to grip. The tape absorbs scuffs and hides seams that a wedge could catch.
- **Construction:**
  - Cheapest possible build (a box plus tape). Fast to repair: re-tape.
  - Duct tape adds grip on the sides and holds loose parts.
  - Light: the tape is about 2-3 g in total.
- **Other:** a beginner or school build with a bright colour identity. The pink is the team colour, shared with the cluster partner.

### C2 lid
- **Construction:** access to the electronics, held by tape (in CAD, by screws).
- **Fight:** keeps the top flat so the robot drives the same way up after a flip (it is invertible: the wheels reach both the top and bottom faces).

### W 4 wheels, close-spaced, outboard
- **Fight:**
  - 4WD gives pushing power and traction. Each wheel has its own motor, so the robot still drives if one fails.
  - Wheels almost as tall as the body let it drive inverted.
- **Construction:**
  - One N20 per wheel needs no gearing or belts.
  - Outboard wheels make the body narrower and are easy to change.
  - Dished hubs save mass and give a press-fit boss on the D-shaft.
- **Why close together:** the four motors pair up back to back near the centre, which leaves the front free for the scoop's root and the rear for the switch.

### S1 clear two-part scoop
- **Fight:**
  - The thin flexible lip conforms to the floor and gets under opponents.
  - The steeper upper part, taped and pink, turns pushing into lift.
  - Polycarbonate does not shatter.
- **Construction:**
  - A cheap sheet off-cut, cut with scissors and cold-bent.
  - Taping it on means no drilling.
  - Clear plastic shows the floor ahead, which matters little, but it is common practice.
- **Other:** the tape over the upper part stiffens it and matches the colour scheme.

### Marker graphics
- **Other:** team identity or numbering (a "D" for the scoop, strokes as the bot's number in the cluster).

## 17. Unseen and inner parts (guesses)

| Part | Guess | Size (mm) | Position (x, y, z) | Confidence | Reason |
|---|---|---|---|---|---|
| Battery | 2S 180 mAh LiPo | 34 x 20 x 8 | (0, -1, -4), the floor centre | medium | the current CAD agrees; the lightest pack for 4 x N20 |
| Rx + ESC | Malenki nano (combined) | 33 x 19 x 3.5 | (0, 0, +5.5), above the battery | medium | a single board drives 2 channels; motors paired per side |
| Switch | slide switch | 12 x 4 x 6 | (0, -31.5, -7.5), rear floor, slider through the underside | medium | |
| Motors | 4 x N20 600 rpm | 10 x 12 x 25 | (+-14.4, +20, 0) and (+-14.4, -22, 0), the shafts outboard along x | high | 4WD with no visible transmission |
| Motor mounts | printed cradles in the tub floor, motor held in a 0.2 mm clearance pocket plus tape | - | around the motors | medium | |
| Wiring | battery to switch to ESC; the ESC left channel to both left motors in parallel, the right to both right motors | 26 AWG | along the centre channel | medium | a 2-channel ESC with 4 motors means parallel pairs |
| Ribs | none (a small box) | - | - | medium | |
| Screws | none visible; the lid is taped | - | - | high (seen) | |
| Bearings | none: the wheels sit on the N20 D-shafts directly | - | - | high | |
