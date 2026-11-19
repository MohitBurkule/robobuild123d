# Baphomet: full description of the reference photos

Purpose: a rebuild-from-text description of the AWS antweight **Baphomet** as it appears in the three wiki photos in
`reference/`. Every part is described with its shape, size ratios, colour, position relative to the other parts, the
faces that touch, the gaps, how it is fastened and how it works. Anything that cannot be seen directly is marked
**(guess)**; anything measured from a photo is a ratio first and an mm value second (mm values assume the tub width is
about 100 mm, which matches a 150 g class robot of this layout and the 30-35 mm wheels; they are estimates, ±10 %).

Frame used throughout: **+y forward** (towards the drum and spikes), **+x = robot's right**, **+z up**. "Left" and
"right" always mean the robot's own left and right. The floor is z = 0 in this document (not the verifier frame).

---

## 1. The photos and what each one shows

### 1.1 `baphomet.aws74.webp` (1157 x 837, front-left, low elevation about 20-25 deg)
- Camera in front of the robot and to its left, looking back and down. The drum runs across the lower-left half of
  the frame; the robot's **right** end of the drum (aluminium motor bell) is at the image left, the robot's **left**
  arm with its bearing is at the image centre-right.
- Visible: the whole drum with both hooks, both spikes (the right spike at the image far left, the left spike at the
  image bottom centre), both arms (the right arm only as a dark tall silhouette at the far left behind the bell), the
  left front corner block and the left side wall with its screw heads, the left wheel (image right), the right wheel
  (image top left, behind the plate), the top plate with the ON|OFF label, the switch hole and the pentagram, three of
  the four plate fasteners.
- Lighting: strong green cast from the left (green screen spill); silver parts show green highlights.

### 1.2 `baphomet.aws76.webp` (2095 x 1825, front-left, high elevation about 50-60 deg, nearly a plan view)
- Camera above, in front and to the left; the robot's front points to the image lower-left; the left side wall runs
  along the image bottom right; the rear wall is at the image top right.
- This is the best photo for the plan: the octagonal tub outline, the open front of the tub, the inner plate frame,
  both wheels in their wells, the full top plate with all four fasteners, the ON|OFF label and switch, the curved left
  arm with its bearing, the drum seen from above with both hooks and the aluminium bell, the right arm curling round
  the bell, both spikes.

### 1.3 `baphomet.aws77.webp` (1279 x 987, front-right, low elevation about 25-30 deg)
- Camera in front and to the robot's right; the front points to the image lower right; the right side wall and the
  right rear chamfer face the camera along the image left.
- Visible: the right side wall with two rows of black screw heads, the right rear chamfer, the right wheel, the plate
  (ON|OFF label left of the switch hole from this angle), the right arm root with a 2 x 2 group of silver button-head
  screws, the aluminium motor bell (image centre), the drum, both hooks, the left arm (image right, tall and rough),
  both spikes.

---

## 2. Overall layout (one paragraph per zone)

- **Rear two thirds: the tub.** An open-topped black printed box, octagonal in plan, longer across (x) than front to
  back (y): width : length about 1.25 : 1 (about 100 x 75-80 mm). Walls about 24 mm tall, 2-3 mm thick. The tub has
  side walls, a rear wall, chamfered rear corners and chamfered front corners, but **no full front wall**: the front is
  an open bay between the two front corner blocks, closed only by the plate's front support rail (section 5).
- **Middle: wheels and plate.** One grey treaded wheel per side, inside the side walls, at about the tub's mid-length.
  The red/black carbon top plate spans between the wheels and covers the middle 60 % of the width and about 70 % of the
  tub length.
- **Front third: the weapon module.** Two curved black arms reach forward from the front corner blocks and hold a
  horizontal drum across the robot. The drum (black printed body, two silver hook rings) is driven by an outrunner
  whose aluminium bell is on the right end of the drum. Two very thin silver spikes stick forward and down from under
  the arms, well ahead of the drum.
- **Overall envelope:** about 100 mm wide (x) at the side walls; about 75-80 mm tub length + about 30 mm of arms/drum
  ahead of the tub + about 35-40 mm of spike beyond the drum, so about 140-145 mm long overall; about 26-28 mm tall at
  the arms' tips, 24 mm at the walls, wheel tops about 2-4 mm above the wall tops.

---

## 3. Part table

| # | Part | Count | Shape | Approx size (mm) | Colour / material | Held by |
|---|------|-------|-------|------------------|-------------------|---------|
| 1 | Tub (chassis) | 1 | open-top octagonal box, no front wall | 100 W x 77 L x 24 H, walls 2-3 | matte black FDM | base of everything |
| 2 | Side wall outer skins | 2 | flat panels on the outside of the side walls | full length x 24 H x 2 | matte black FDM, layer lines horizontal | 4-6 black screws each (guess: into the tub frame) |
| 3 | Rear chamfer panels | 2 | flat angled panels on the rear corners | 15 x 24 x 2 | matte black FDM | 2 black screws each |
| 4 | Front corner blocks (wheel-guard front ends) | 2 | hollow angled boxes at the front corners | 15 x 18 x 24 | matte black FDM | part of the tub print (guess) |
| 5 | Plate frame (inner rails + posts) | 1 | rectangular printed frame under the plate | 62 x 55, rail 4 x 9 | matte black FDM | part of the tub or screwed in (guess) |
| 6 | Wheels | 2 | treaded TPU tyre on a black spoked hub | 32-34 dia x 12-13 | grey TPU, black hub | pressed onto gearmotor D-shafts (guess) |
| 7 | Drive gearmotors | 2 | N20 / micro metal gearmotors | 12 x 10 x 25-30 | silver can, brass gears | cradles under the plate (guess) |
| 8 | Top plate | 1 | flat rectangle, rounded/cut corners | 62 x 57 x 1-1.5 | red/black 2x2 twill carbon | 4 screws (2 socket heads + 2 nyloc nuts visible) |
| 9 | Pentagram decal | 1 | round sticker | 26-28 dia | black disc, red line art, white ring | adhesive |
| 10 | ON|OFF label | 1 | small rectangle sticker | 15 x 7 | orange-red, black text | adhesive |
| 11 | Power switch | 1 | small slide switch under a plate hole | hole 7 x 5 | black | under the plate (guess: clipped in a printed holder) |
| 12 | Arms | 2 | curved banana/crescent plates | 35 long x 20 tall x 5-6 thick | matte black FDM, rough torn top edges | 4 silver button screws (right arm root) / screws (left, guess) |
| 13 | Drum bearing | 1 visible (left) | flanged ball bearing in the arm end boss | about 8-10 OD | silver steel | pressed into the left arm (guess) |
| 14 | Drum body | 1 | plain cylinder | 23 dia x 42 long | matte black FDM, horizontal layer rings | clamped between bell and left bearing |
| 15 | Hook rings | 2 | flat crescent rings with one hook each | 2 thick, ring OD about 25, hook tip at about 31 dia | bright aluminium or steel | slid over the drum ends, keyed (guess) |
| 16 | Weapon motor (outrunner) | 1 | aluminium bell + stator | bell about 18-20 dia x 12-14 long | bright aluminium with small set screws | stator bolted to the right arm (guess) |
| 17 | Motor spacer / mount boss | 1 | short black cylinder | about 18 dia x 4 | matte black FDM | part of the right arm (guess) |
| 18 | Spikes | 2 | very thin flat needles, triangle in side view | 50 long x 9 tall at root x 1-1.5 thick | bare silver steel/titanium | clamped to the arm feet (screws visible on the right) |
| 19 | Battery, ESCs, receiver | - | not visible | - | - | under the plate (guess) |

---

## 4. Tub (chassis) in detail

### 4.1 Plan outline
- Octagon with two long sides. Taking the tub width W = 100 mm and length L = 77 mm:
  - Rear wall straight, about 0.70 W long (70 mm), centred.
  - Rear corners chamfered at 45 deg, each chamfer about 0.12-0.15 W along each leg (12-15 mm). In aws77 the right rear
    chamfer is a clearly separate flat face with two black screw heads, one above the other.
  - Side walls straight and parallel, about 0.60 L long (45-50 mm) between the chamfers.
  - Front corners chamfered too, about 12 mm legs (aws76 bottom: the left front corner is cut at 45 deg; aws77: the
    right front corner has the angled face that carries the arm root).
  - **No front wall between the front corners.** In aws76 white background is visible through the tub between the
    left front corner block, the plate front rail and the drum. So the front of the tub is an open bay about 0.6 W wide.
- Symmetric about x = 0 except the weapon motor end (right) and the switch (right rear).

### 4.2 Height and walls
- Walls 22-25 mm tall (about 0.24 W), vertical, flat-topped, 2-3 mm thick. The wall top is level all round.
- The tub sits 2-3 mm above the floor (bottom edge visible as a shadow line in aws77). Floor plate not visible
  (guess: a 1.5 mm printed floor, or open with only cross members).
- **Side walls are double:** in aws77 the right side shows a horizontal seam at about half height and two screws
  stacked vertically at the rear end and again at about one third of the length, plus one more pair near the front;
  the outer skin is a separate panel (wheel guard skin) screwed onto an inner wall or frame. Screws: small black
  pan/button heads, M2 (guess), about 5 mm from the top and bottom edges, i.e. two rows at z ≈ 6 and z ≈ 19 mm.
  Count on the right side: 2 at the rear end, 2 at about x-centre of the wheel's rear half, 1-2 near the front corner
  (partly hidden) = 5-6. The left side (aws74 right) shows 3 visible in a row near the top and bottom at the front
  half, consistent with the same pattern.
- The rear chamfer panels each carry 2 black screws (top and bottom, aws77).

### 4.3 Wheel wells (wheel guards)
- Each wheel runs in a well between the outer side wall (outboard) and an inner rail (inboard). The outer wall is the
  wheel guard: it covers the wheel side completely up to the wall top; the wheel shows only above the wall top and
  through the open top.
- Gap wheel-to-outer-wall about 1-2 mm; wheel-to-inner-rail about 1-2 mm (aws76: thin dark gaps both sides of the
  near tyre).
- The well is open at the top (no cover over the wheel) and open at the bottom (tyre touches the floor through it).
- Front and rear ends of each well: printed cross-walls / corner blocks (aws76 far wheel: a black block in front of and
  behind the tyre at the top-left; near wheel: the front corner block ahead of it, a rear block behind it).

### 4.4 Front corner blocks
- At each front corner a hollow angled block (aws76 bottom: a rectangular frame with a big open window, wall about
  2.5 mm, looking like a printed box with no top). Footprint about 15 x 18 mm, full wall height.
- Its outer face is the 45 deg front chamfer; its inner face meets the front end of the inner wheel-well rail.
- The arm root is fixed to this block (right side: four silver button-head screws in a 2 x 2 square, 5-6 mm pitch,
  on the arm root plate, which lies against the angled outer face of the block; left side screws hidden, assume the
  same).

### 4.5 Inner plate frame
- A printed rectangular frame inside the tub under the plate edges (aws76: clearly separate from the outer walls, with
  a dark gap between it and the walls at the wheel wells).
- Front rail: a straight bar across the robot at the plate's front edge, about 4 mm thick (y) and 9-10 mm tall, its
  top at the plate underside. At each end a square post block about 7 x 7 mm with a vertical hole about 2 mm (plate
  screw holes) and a second small hole on the face (aws76: two square bosses with holes at the rail ends).
- Side rails: the inner walls of the wheel wells, same height, running back to the rear wall.
- Rear: posts near the rear corners carry the two rear plate fasteners.

### 4.6 Colour and finish
- Matte black PLA/PETG/nylon (guess), visible horizontal layer lines on all walls, some stringing and rough edges
  (aws76 near wall bottom edge has blobs). No paint.

---

## 5. Top plate, decal, label, switch

### 5.1 Plate
- Flat carbon fibre plate, 2 x 2 twill with **red and black** tows (red aramid/carbon hybrid or dyed), glossy.
- Rectangle about 62 mm (x) x 57 mm (y), 1-1.5 mm thick. Corners square; the plate edge overhangs the front rail
  slightly (1-2 mm) and stops about 8-10 mm short of the rear wall (inside of the rear wall visible behind it in aws76).
- Position: centred in x; in y from just behind the drum's rear clearance (plate front edge about 4-6 mm behind the
  drum surface) to about 10 mm in front of the rear wall. Its centre is about 3-5 mm behind the tub's centre.
- The plate top is at about the wall-top height (aws77: plate surface level with or 1 mm above the side wall top).
- The wheels' tops rise 2-4 mm above the plate on both sides; the plate side edges are 2-4 mm inboard of the tyres.

### 5.2 Plate fasteners (4)
- Near the four corners, inset about 9 mm from the side edges and 8-10 mm from the front and rear edges.
- Front-left and rear-right show silver **socket cap screw heads** with washers (aws76); front-right and rear-left show
  silver **nyloc nuts** (aws76/aws77: hex outline, nylon ring), i.e. two screws come up from below and are nutted on
  top (guess: through the printed posts). All four are M2 (guess) and stand 2-3 mm proud of the plate.
- They clamp the plate down onto the frame posts / rails.

### 5.3 Pentagram decal
- Round sticker, diameter about 0.43 x plate width (26-28 mm), centred in x, centre about 0.45 of the plate length from
  the plate front edge (slightly forward of the plate centre).
- Black disc with a thin white/silver ring at its edge, a thin red inner circle, and a red line-art **inverted
  pentagram** (one point towards the robot's **rear**, two points towards the front) containing a goat head (Sigil of
  Baphomet). Small red characters round the inner ring.

### 5.4 ON|OFF label and switch
- Switch hole: square/rectangular cut-out about 7 x 5 mm in the plate, about 0.27 of the plate length from the rear
  edge, offset about 6-10 mm to the robot's right of centre. A black slide switch lever is visible inside, its top 1-2 mm
  below the plate top.
- ON|OFF label: orange-red rectangle about 15 x 7 mm with black "ON | OFF", just to the right of / beside the switch
  hole, its long axis along y (reads across the hole). (aws74/aws76/aws77 agree it is on the right-rear quarter.)
- The switch is under the plate; it is operated through the hole with a small tool or fingernail.

---

## 6. Wheels and drive

- Two wheels, one per side, axles along x, centres at about the tub mid-length, 0-5 mm behind it (the line between
  the wheel centres passes under the decal's rear half).
- Tyre: grey TPU, outer diameter about 32-34 mm (0.33 W), width about 12-13 mm, with about 36-40 fine axial ribs
  (tread looks like a gear: ribs about 1.5 mm wide, 1 mm deep). Hub: black printed, recessed outer face with about 5-6
  straight spokes (aws74, aws77), the tyre bead sits on the hub rim. A yellowish tint at the far wheel's hub edge in
  aws76 (glue or a different TPU shade).
- Each wheel stands 2-4 mm above the side wall top; bottom touches the floor; outer face 1-2 mm inside the outer wall.
- Drive: micro metal gearmotor per wheel (aws76: brass pinion and silver gearbox seen behind the far tyre), lying along
  x under the plate, gearbox at the wheel end, the two motors back to back near the centre line (guess). Wheels pressed
  on the D-shafts (guess).

---

## 7. Weapon module

### 7.1 Arms (2)
- Separate printed black parts, each a flat plate 5-6 mm thick (x) with a curved crescent/banana outline in side view
  (y-z), thickened locally at the bearing boss.
- **Left arm** (aws76 bottom left, very clear): root at the left front corner block, about 10-12 mm tall there; it
  runs forward and slightly inward, then curves up into a rounded front end about 20 mm tall that carries the bearing
  boss. In plan it bows outward (convex to the left). Inner face flat. Length root-to-boss centre about 30-35 mm.
- **Right arm** (aws77 left and aws74 left): root plate against the right front corner block with **four silver
  button-head screws in a 2 x 2 square** (5-6 mm pitch) on its outer angled face; the arm then rises into a tall rough
  fin about 25 mm high whose top edge is ragged (damage) and whose front wraps round the motor stator; it carries the
  motor stator mount on its inner face.
- Both arm tops stand 3-8 mm above the plate and the drum top: they read as "horns" in aws74/aws77.
- Front tips of the arms end about 3-5 mm ahead of the drum axle; their lower edge comes down to about 6-8 mm above the
  floor, where the spike roots are clamped.

### 7.2 Bearing and shaft
- Left arm boss holds a flanged ball bearing (aws76: silver race about 9-10 mm OD, inner ring with the shaft end and a
  small screw/collar in it). The drum axle (silver, about 3 mm, guess) ends in it, flush with the arm outer face.
- Right end: the drum is carried by the outrunner itself (motor-as-hub).

### 7.3 Drum body
- Black printed cylinder, diameter 22-24 mm (0.23 W), length 40-44 mm (0.42 W), axis along x at about z = 15-16 mm
  (just below mid-height of the walls, about 4-5 mm above the drum radius).
- Its left end is 1-2 mm from the left arm boss; its right end butts against the aluminium bell.
- Plain surface with fine layer rings and scuffs. No visible screws on the black part.
- The drum is centred on the robot x = 0 only together with the bell: the black body is slightly left of centre, the
  bell occupies the right 15 mm (guess: drum spans x -26 .. +16 mm, bell +16 .. +30).

### 7.4 Hook rings (teeth) (2)
- Bright metal (aluminium or steel, guess: 2 mm aluminium from the colour, or hardened steel for a real build),
  about 2 mm thick, flat in planes normal to x.
- Each is a ring that fits snugly over the drum OD with **one hook**: from the drum surface the outline rises
  smoothly over about 90-120 deg to a tip about 4-5 mm proud (tip radius about 15-16 mm), then drops back almost
  radially; the hook is curved like a claw (aws74 shows both hooks pointing down-forward at the bottom of the drum with
  a concave inner face).
- Positions: one at each end of the black drum body (x about -24 and +14 mm), inboard of the arms and the bell.
- Phase: the two hooks are 180 deg apart (aws74: both hook tips near the bottom-front because the drum stopped there,
  aws77: one up-back one down-front). Treat as 2 teeth, 180 deg apart.
- Gap hook tip to floor at the lowest point: about 1-2 mm; gap hook tip to plate front edge: 3-5 mm; to the arms 1-2 mm.

### 7.5 Weapon motor
- Brushless outrunner on the robot's right end of the drum: the bright aluminium cylinder (aws74 left, aws77 centre,
  aws76 top left) is the motor **bell**, diameter about 18-20 mm (slightly less than the drum), length 12-14 mm, with
  two or three small screw/set-screw holes on its circumference and the maker's lettering. A short black printed boss
  (spacer, 18 mm dia x 3-4 mm) sits between the bell and the right arm: the stator mount.
- Mechanism (guess, consistent with the photo): stator bolted to the right arm through that boss; bell bolted to the
  drum's right end; the drum spins with the bell; the motor's bearings carry the right side, the left arm bearing the
  left side. Phase wires run from the stator inside the right arm back into the tub (not visible).

### 7.6 Spikes (2)
- Very thin flat blades (1-1.5 mm, bright steel/titanium), each a long isosceles triangle in side view: root about
  8-10 mm tall, length about 50 mm, needle point. They stand vertical (thin in x), parallel to y.
- One under each arm, x just outboard of the drum ends (about ±32-35 mm), root clamped against the lower outer face of
  the arm foot (right side: the 2 x 2 screw group sits right above the spike root; left: one bolt head visible below
  the bearing in aws76).
- They slope down and forward at about 12-15 deg; the tips reach the floor level (0-1 mm above) about 40-45 mm ahead of
  the drum surface, i.e. 0.42 W.
- Gap spike-to-hook path: 2-4 mm in x (hooks swing inboard of the spikes).

---

## 8. Hidden parts (all guesses)
- Battery: 2S LiPo, 300-450 mAh, under the plate centre, between the drive motors and the front rail.
- Drive ESC/receiver: a combined board (Malenki-Nano class) on top of the battery.
- Weapon ESC: small brushless ESC near the front rail on the right, wires to the motor through the right arm root.
- Wires: battery -> switch (right rear) -> drive board and weapon ESC; drive board -> both gearmotors; weapon ESC
  signal from the drive board; three phase leads from the weapon ESC through the right front corner into the right arm
  and to the stator. No wire is visible outside in any photo.

---

## 9. Contact / gap matrix (main pairs)

| A | B | Relation | Gap / overlap (mm) | Notes |
|---|---|----------|--------------------|-------|
| Plate | frame rails/posts | rests on, screwed | 0 | 4 fasteners |
| Plate | wheels | beside | 2-4 in x | tyres stand above plate |
| Plate front edge | drum | in front | 3-5 in y to the hook path | |
| Wheel | outer side wall | inboard of | 1-2 | wall covers the tyre side |
| Wheel | inner rail | outboard of | 1-2 | |
| Wheel | floor | touching | 0 | only ground contacts with spike tips ~0-1 |
| Arm root | front corner block | bolted face to face | 0 | 4 button screws (right) |
| Left arm boss | drum left end | beside | 1-2 | bearing carries shaft |
| Right arm | motor stator boss | bolted | 0 | |
| Motor bell | drum right end | bolted | 0 | rotates together |
| Hook rings | drum body | snug over the ends | 0 | keyed (guess) |
| Hook tips | floor | above | 1-2 at the lowest point | |
| Hook rings | arms / bell | beside | 1-2 in x | |
| Spike root | arm foot outer face | clamped | 0 | |
| Spike tip | floor | above | 0-1 | |
| Spike | hook sweep | outboard | 2-4 in x | |
| Tub bottom | floor | above | 2-3 | |

---

## 10. Rebuild checklist (in order)
1. Octagonal open-front tub 100 x 77 x 24, walls 2-3, front corner blocks, rear chamfers, side skins with 2 rows of
   black screws.
2. Wheel wells at mid-length; 33 mm grey ribbed tyres on black spoked hubs, tops 2-4 mm above the walls.
3. Inner frame with a front rail and corner posts; red/black carbon plate 62 x 57 on top with 4 fasteners, inverted
   pentagram decal forward of centre, switch hole + ON|OFF label at the right rear.
4. Two curved black arms from the front corner blocks; right arm with 2 x 2 silver screws at the root and the motor
   stator; left arm with a flanged bearing.
5. Drum 23 x 42 black plus aluminium bell 19 x 13 on the right; two 2 mm hook rings at the black drum ends, hooks
   180 deg apart, tip radius ~15.5.
6. Two 1-1.5 mm needle spikes, 50 long, 9 tall at the root, from the arm feet down to the floor 40-45 mm ahead of the
   drum.

---

## 11. Coordinate frame (used by every number below)

Origin: on the floor, at the centre of the tub in x and in y (half way between the rear wall outer face and the front
corner blocks' front tips). +x = robot's right, +y = forward, +z = up. Units mm, angles deg. (The verifier frame puts
the wheel axle at z = 0; subtract 16.5 mm from every z below to convert.)

## 12. Every part in all dimensions (mm, guesses ±10 %)

| Part | L (y) | W (x) | H (z) | Thickness | Radii / angles | Centre (x, y, z) |
|------|-------|-------|-------|-----------|----------------|------------------|
| Tub outline | 77 (y -40 .. +37) | 103 (x ±51.5) | 24 (z 2 .. 26) | walls 2.0, floor 1.5 | rear chamfers 45 deg, legs 12; front chamfers 45 deg, legs 8 | (0, -1.5, 14) |
| Side wall skin | 58 | 2 | 24 | 2 | screws at z 8 and 20 | (±50.5, -6, 14) |
| Rear chamfer panel | 17 (along face) | - | 24 | 2 | 45 deg | (±45.5, -34, 14) |
| Front corner block | 12 | 12 | 24 | 2.5 walls | outer face 45 deg | (±40, 25, 14) |
| Inner rail (wheel-well inner wall) | 66 (y -38 .. 28) | 1.5 | 24 | 1.5 | - | (±34.7, -5, 14) |
| Plate front rail | 4 | 64 | 9 (z 17 .. 26) | 4 | end posts 7 x 7 with 2.2 holes | (0, 26, 21.5) |
| Top plate | 61 (y -34 .. 27) | 65 (x ±32.5) | 1.0-1.5 | 1.0 | square corners | (0, -3.5, 26.5) |
| Plate fasteners | - | - | 2.5 proud | M2 | at (±27, 21) and (±27, -28) | - |
| Decal | 27 dia | - | 0.2 | - | ring 13.5 outer, 12.5 inner circle | (0, 0, 27.1) |
| Switch hole | 4.4 | 11 (stadium, end radii 2.2) | through | - | - | (10, -29.5, 26.5) |
| ON|OFF label | 7 | 15 | 0.1 | - | - | (21, -29, 27.1) |
| Wheel | 34 dia | 11-12 | 34 | tyre 3, web 2 | tread: 18-40 ribs 1.6 wide x 1.4 deep | (±42.5, -12, 17) |
| Drive gearmotor | 12 | 35.5 incl. shaft | 10 | - | can r 6 | (±26.3, -12, 17) |
| Arm | 34 (y 24 .. 58) | 5 | 32 (z 1.5 .. 34) | 5 | outline spline below | (±32.5, 41, 17) |
| Drum body | 23 dia | 47 (x -29 .. 18) | 23 | rim 1.5 | r 11.5 | (-5.5, 50, 16) |
| Hook ring | 31 dia at tip | 2 | 31 | 2 | ring r 13.2, hook r(θ) below | x -28 and +17 |
| Motor bell | 18.2 dia | 10 (x 18 .. 28) | 18.2 | - | r 9.1 | (23, 50, 16) |
| Stator base / arm cup | 12-16 dia | 2 | - | - | r 6 base in r 6.25 cup | (29, 50, 16) |
| Drum shaft | 1.5-3 dia | 64 (x -34 .. 30) | - | - | - | (-2, 50, 16) |
| Left bearing | 8-10 OD | 3 | - | - | - | (-32.5, 50, 16) |
| Spike | 60 (y 36 .. 96) | 1.5 | 8 at root | 1.5 | tip angle 9 deg in side view | (±34.75, 60, 5) |

## 13. Curves as maths

- **Tub plan** (polygon, CCW): (-39.5,-40), (39.5,-40), (51.5,-28), (51.5,18), (43.5,30)... the front tips of the
  corner blocks at y = 30-37; written as the polygon used in the rebuild: (-39.5,-40) (39.5,-40) (51.5,-28) (51.5,18)
  (43.5,30) (-43.5,30) (-51.5,18) (-51.5,-28).
- **Arm side outline** (y, z, verifier z+16.5 here): closed polyline/spline through (24,6.5) (30,6.5) (36,1.5)
  (44,2) (50,7) (57.5,13.5) (58,22.5) (55,31.5) (50,34) (44,33) (38,26.5) (30,22.5) (24,22.5). The front end is
  approximately an arc centre (50, 16), radius 8-9, from -60 deg to +100 deg; the top edge from (38,26.5) to (50,34)
  is the line z = 26.5 + 0.625 (y - 38).
- **Hook ring outline** in the drum's own polar frame (θ from the hook start):
  r(θ) = 13.2 + 2.3 (θ/90)^1.4 for 0 ≤ θ ≤ 90; r = 15.5 - 2.3 (θ-90)/9 for 90 < θ ≤ 99; r = 13.2 otherwise.
  Second ring is the same rotated 180 deg. Inner hole r = 11.6.
- **Spike side outline** (y, z): triangle (36,5) (52,5) (96,0.7) (52,12.5) (36,12.5): lower edge z = 5 - 0.098 (y-52),
  upper edge z = 12.5 - 0.270 (y-52) for y > 52; tip at y = 96.
- **Wheel tread:** n = 18 slots at θk = 20 k deg, each slot a 1.6 x 1.4 box at radius 16.6.
- **Decal pentagram** (inverted, one point to -y): vertices at radius 12, angles 270 + 72 k deg (k = 0..4), joined
  in the order 0, 2, 4, 1, 3.

## 14. Independent measurements

| Quantity | From dimensions | From ratios | From photo pixels | Reconciled |
|----------|-----------------|-------------|-------------------|------------|
| Tub width / length | 103 / 77 = 1.34 | wheel dia 34 ≈ 0.33 W | aws76: near side 1100 px vs rear wall ~820 px (foreshortened) ≈ 1.3 | 1.3 |
| Wheel dia / tub height | 34 / 24 = 1.42 | tyre top 2-4 above wall | aws77: tyre ~205 px tall vs side wall ~150 px ≈ 1.37 | 1.4 |
| Drum length / dia (black body) | 47 / 23 = 2.0 | ≈ 0.45 W | aws74: 230 px long vs 170 px tall (oblique) ≈ 1.35-2.0; aws76: 330 vs 170 ≈ 1.95 | 1.9-2.0 |
| Bell dia / drum dia | 18.2 / 23 = 0.79 | - | aws77: bell 120 px vs drum 150 px ≈ 0.8 | 0.8 |
| Plate W / tub W | 65 / 103 = 0.63 | between the tyres | aws76: plate 475 px vs tub across ~760 px ≈ 0.62 | 0.63 |
| Decal dia / plate W | 27 / 65 = 0.42 | - | aws76: 260 px vs 475 px ≈ 0.55 (perspective inflates) | 0.45 |
| Spike reach ahead of drum / W | 40 / 103 = 0.39 | - | aws74: 210 px vs drum 230 px ≈ 0.9 drum lengths ≈ 0.4 W | 0.4 |
| Hook tip proud of drum | 4 | 0.17 of drum dia | aws74: 30 px on 170 px dia ≈ 0.18 | 4 |
| Arm height above plate | 7 | - | aws74: horns ~60 px above plate edge at drum scale 170 px/23 mm ≈ 8 | 7-8 |

## 15. Consistency check (conflicts and the value chosen)

1. **Front wall:** aws76 shows the tub open at the front between the corner blocks; the rebuild uses a 2 mm front wall
   behind the drum for wiring and stiffness. Chosen: open look is the truth; a front wall is a model compromise (it is
   hidden behind the drum in all three views).
2. **Decal size:** pixel ratio 0.55 vs dimension 0.42: the aws76 view is foreshortened along the plate length, the
   decal is round, so the across-width ratio is less inflated; reconciled 0.45 (27-29 mm).
3. **Hook material:** the colour reads as aluminium; a spinner hook must be hardened steel for the rules checker.
   Chosen: steel 2 mm rings in the model, coloured light silver.
4. **Drum shaft size:** a visible 3 mm-ish shaft end in the left bearing vs the 1.5 mm outrunner shaft. Chosen: the
   motor's own shaft extended (motor-as-hub), 1.5 mm, because that is what the outrunner can carry; noted as a
   deviation.
5. **Wheel position:** aws74 suggests slightly behind the plate centre, aws76 slightly ahead. Chosen: at the plate
   centre, y = -12 in this frame.
6. **Arm thickness:** 5 mm from aws76 vs up to 8 mm at the right arm root (aws77). Chosen 5 mm with a thicker root
   socket in the tub.
