# Refined for the Roboteers Pleasure: full reference description

This file describes the real robot in enough detail to rebuild it from the text alone. It covers every visible part and its shape,
size, colour, position relative to the other parts, contacts, gaps, fastening and mechanism. Lengths are estimated from the
photos by proportion. The wheel diameter (about 24 mm, typical for an AWS antweight on N20 gearmotors) is the scale reference.
Values marked **(guess)** are not visible in any photo and are inferred from how such robots are normally built. Values
marked **(est.)** are measured by proportion from a photo and are probably within ±15 %.

Coordinate convention: +y = forward (the plough end), +x = the robot's right, +z = up. Heights in this document are above the floor
(z = 0 at the floor); the CAD puts the wheel axle at z = 0, so subtract the wheel radius (11-12 mm) to get CAD z. "Left" and
"right" are the robot's own left and right when it drives forward. "Front", "rear", "inboard" and "outboard" follow the same frame.

---

## 1. Photos and what each one shows

### 1.1 `aws73` (front-left, high angle, on a grey event table, slightly blurred)
- Camera is in front of the robot, to its left, about 50-60 degrees above the table. The robot's front (red plough) is
  nearest the camera at the bottom of the frame. Its rear (two black wheels) is at the top of the frame, one wheel at the top
  left and one at the right.
- This is the only photo that shows the **top plate pattern** clearly: the black top plate, the angled slots in it, the
  silver screw heads, the gear seen almost edge-on (its teeth look like a stack of white ridges), and the arm rising out of the
  gear towards the camera.
- The weapon head is the **saw configuration**: a small black/silver outrunner motor with a silver saw disc, bolted to the
  arm top. The motor can shows the letters "TC" (BrotherHobby Tornado TC-class 14xx motor; est.).
- A black heat-shrink sleeve wraps the arm about one third of the way up. Thin wires (blue and black) loop over the top plate at
  the rear left and drop into a slot.
- In the background (top left) is another robot (black wheel and black arm). It is not part of this robot.

### 1.2 `aws74` (left side, low elevation, cut out on white; front on the LEFT of the picture)
- Camera is on the robot's left, about 10-20 degrees above the floor (est.: the near wheel's hub face looks almost circular).
  The REFERENCE.json pick says elevation 35, but the image looks lower. The front (red plough) is at the left of the frame
  and the rear wheel at the right.
- This photo shows the **side profile**: the plough's wedge and hood, the black chassis side with its lightening windows,
  the near (left) rear wheel, the gear side-on with its black side link, and the full arm with its fin, sleeve, wires and saw.
- The weapon head is the **saw configuration**: a black 6-hook saw disc with a green edge layer, centred on 4 + 1 small
  screws (bell clamp), with 3 black motor leads running down the arm.

### 1.3 `aws76` (front-left three-quarter, about 30-35 degrees elevation, cut out on white)
- Camera is in front-left of the robot. The plough front face is lower left, the left rear wheel is at the right of the
  frame, and the arm rises up and leans to the upper left (forward).
- The plough is **orange** in this event (red in aws73/aws74), so it was reprinted. The chassis and top plate are the same black parts.
- The weapon head is the **axe configuration**: no motor. A sharpened steel blade (hooked like a pick or beak) is bolted to the
  arm tip with 2 Torx/Phillips pan screws. The arm is a plain bar, **without** the fin of aws74.
- This photo shows the orange **U-shaped cradle** on the rear centre of the top plate, the black cheek link at the gear,
  and the slot pattern on the left half of the top plate.

### 1.4 Consequence for the model
- The body (plough, chassis, top plate, wheels, gear, cheek link) is the same in all photos.
- The arm and head differ between events. aws73/aws74 (saw, finned arm, nearly upright) and aws76 (axe, plain arm, leaning
  forward ~30-40 degrees) are two weapon fits of the same lifting/striking arm. REFERENCE.json asks for a 6-tooth disc spinning
  about x, so the CAD models the **saw fit of aws73/aws74**.
- One fixed arm pose can only match one photo well: an upright arm matches aws74, and a forward-leaning arm matches aws76.

---

## 2. Overall dimensions and proportions

| quantity | value | source |
|---|---|---|
| overall length (plough lip to wheel rear) | ~110-115 mm (est.) | aws74 side: plough lip to wheel back ≈ 4.6 wheel diameters |
| overall width over the wheels | ~90-94 mm (est.) | aws73: wheels stick out ~3 mm past the plough sides |
| plough width | ~80-84 mm (est.) | aws73/aws76 |
| chassis/top plate width | ~70-72 mm (est.) | inside the plough side walls |
| top plate height above floor | ~24-26 mm (est.) | ≈ wheel diameter |
| plough top edge height | ~27-30 mm (est.) | 2-4 mm above the top plate |
| gear axle height | ~25-28 mm (est.) | just above the top plate |
| arm top (saw centre) height | ~100-105 mm (est.) | aws74: ≈ 4.2 wheel diameters |
| overall height incl. saw | ~115 mm (est.) | aws74 |
| wheel diameter | ~22-26 mm | reference scale |
| gear tip diameter | ~32 mm (est.) | aws74: 1.3 × wheel |
| saw disc tip diameter | ~26-30 mm (est.) | aws74: ≈ 1.1 × wheel |
| mass | ≤ 150 g (rule) | — |

Side-view proportions (aws74, measured along the length from the front lip = 0 % to the wheel back = 100 %):
- plough front lip: 0 %; top of the plough front face: ~25 %; plough hood top edge runs from ~25 % to ~60 %;
  plough side wall ends: ~74 %.
- gear centre: ~52 %. arm base: ~52-55 %. arm mid-height: ~58 % (the arm bows slightly to the rear).
  saw centre: ~55 %. arm top crest: ~48 %.
- wheel front edge: ~79 %; wheel centre: ~90 %; chassis back face: ~97 %; wheel back: 100 %.

Height ratios (aws74): the top plate is ~1.0 wheel diameter above the floor. The plough top is ~1.15 wheel diameters. The gear top is
~1.75 wheel diameters. The arm top is ~4.2 wheel diameters. The arm is about 3.5 × as tall as the body.

Plan ratios (aws73): the plough covers the front ~45 % of the plan and wraps the sides back to ~75 %. The top plate shows over the
rear ~55 % and is ~85 % of the overall width. The wheels take the outer ~10 % on each side at the rear ~25 % of the length.

---

## 3. Part list (summary table)

| # | part | colour | material (est.) | count | size (est.) | fastened by |
|---|---|---|---|---|---|---|
| 1 | plough (front + side armour shell) | red (aws73/74), orange (aws76) | PLA/PETG print, clear tape on the front face | 1 | 82 W × 85 L × 28 H mm, 2 mm walls | screws into the chassis sides (guess: 2-4 × M2/M3, hidden) |
| 2 | chassis tub | black | PLA/PETG print | 1 | 71 W × 62 L × 20 H mm | carries everything |
| 3 | top plate | black | print (matte, textured) | 1 (maybe 2 halves) | 71 × 62 × 2 mm | 6-8 silver button screws |
| 4 | wheels | black tyre, black or clear hub | TPU/rubber tyre on a printed hub | 2 | Ø24 × 10 mm | press fit on the gearmotor D-shafts (guess) |
| 5 | drive gearmotors | hidden (blue through the slots, est.) | N20 / micro metal gearmotors | 2 | 12 × 10 × 25 mm | in the tub, clamped by the top plate (guess) |
| 6 | big gear (arm root) | white | print | 1 | Ø32 tip × 12 mm thick, ~16-18 teeth | pivot screw through the black cheek link |
| 7 | arm | white | print, one piece with the gear | 1 | 85 long × 9 wide × 8 thick mm | part of the gear |
| 8 | cheek link / bearing plate | black | print | 1 visible (left side), probably 2 | 20 × 12 × 4 mm, rounded | screws into the chassis |
| 9 | arm actuator | hidden | servo or geared motor (guess) | 1 | — | in the tub, drives the big gear through a pinion (guess) |
| 10 | weapon motor | black/silver | BrotherHobby TC 1404-class outrunner (est.) | 1 | Ø18 × 16 mm | screwed to the arm head |
| 11 | saw disc | black with green edge (aws74), silver (aws73) | steel or hardened plate | 1 | Ø28 × 1-1.5 mm, 6 hook teeth | 4 small screws into the bell + centre screw |
| 12 | axe blade (aws76 only) | bare steel | sharpened steel sheet | 1 | 30 × 12 × 1.5 mm | 2 pan screws |
| 13 | heat-shrink sleeve | black | heat-shrink | 1 | 12 long × Ø10 mm | shrunk round the arm and wires |
| 14 | motor leads | black, red crimps | 3 × silicone wire | 3 | ~110 mm | down the arm to crimp connectors |
| 15 | rear cradle (U fork) | orange (aws76), red (aws74) | print | 1 | 16 W × 6 D × 10 H mm | on the top plate rear centre (guess: screwed or glued) |
| 16 | top plate screws | silver | M2/M2.5 button-head socket or Torx | 6-8 visible | head Ø4 mm | into the chassis |
| 17 | battery, receiver/drive ESC, weapon ESC, power switch | hidden | — | 1 each (guess) | — | inside the tub (guess) |

There are **no wheel guards** and no separate guard supports. The wheels are fully exposed at the sides, top and rear.
There is no separate plastic motor mount block: the weapon motor bolts straight onto the white arm head, which is widened to form the mount.

---

## 4. Part-by-part description

### 4.1 Plough (front and side armour)
**Shape.** A thin printed shell, open at the back and at the bottom, that wraps round the front and both sides of the
black chassis. In plan it is a rectangle with the two front corners cut off at about 45 degrees (corner facets about 8-10 mm
long, est.). In side view it has three zones:
1. **Front wedge face**: a large flat face, about the full plough width (~76-80 mm across the flat, est.). It slopes up and back
   from a lip about 1-2 mm above the floor to a horizontal crease about 20-24 mm above the floor and about 20-25 mm behind the
   lip. Its angle is about 45-55 degrees from the floor (est.; aws74 and aws76 agree). Wide clear packing tape covers it; the tape
   shows as lighter, glossy streaks with peeled corners (aws76) and a crease line half way up where two tape strips overlap.
2. **Hood / steep band**: above the crease a short steeper face (about 70-80 degrees from the floor) rises 4-6 mm to the top edge.
   The top edge is horizontal and runs back as a narrow flat top rim (about 2-3 mm wide, the wall thickness) along both sides.
3. **Side walls**: vertical outer faces from the top edge down to about 9-12 mm above the floor. Below that a lower facet
   angles inward towards the floor (a chamfered skirt, about 30-40 degrees off vertical), so the bottom edge of the side is
   about 4-5 mm further in than the side face. aws74 shows this facet as the darker red band along the bottom of the side, and
   aws76 shows it under the orange side face.
- The side walls run back to about 74 % of the length and end 2-3 mm in front of the tyres, with a vertical cut end.
- **Top-edge notch**: in the middle of the top edge, where the plough meets the gear, the edge is cut down in a smooth
  concave arc (scallop) about 25-30 mm wide (aws76 shows it clearly; in aws74 the red edge dips behind the gear). The gear's lower
  front teeth sit in this notch, about 1-2 mm clear of the plough.
- Small diagonal facets join the hood band to the side walls at the front corners (aws76: the orange corner shows 3 facets meeting
  at a point, like a cut gem).
- Wall thickness about 2 mm (est., from the cut edge at the notch in aws76).
- Size ratios: plough height ≈ 1.15 × wheel diameter; plough length (lip to side end) ≈ 3.4 × wheel diameter; plough width ≈ 3.4 ×
  wheel diameter, ≈ 1.15 × top plate width.

**Colour.** Bright red (aws73, aws74) or bright orange (aws76). Plain print surface with visible horizontal layer lines.

**Position vs other parts.**
- Inside, the plough's side walls lie against the outside of the chassis side walls (contact or a gap of 0-1 mm, guess).
- The top edge stands ~2-4 mm above the top plate. Seen from the front, the top plate is recessed behind and below the plough rim.
- The front of the chassis tub is hidden inside the plough. The plough nose (between the front face and the chassis front) is
  probably hollow (guess) or holds the battery (guess).
- Gap to the wheels: 2-3 mm between the plough's rear cut end and the front of each tyre. Gap to the floor: lip 1-2 mm;
  side skirt bottom edge ~2-3 mm (est.).
- Gap to the gear: 1-2 mm between the notch edge and the gear teeth. The gear sits above and behind the notch, never inside the shell.
- Relation to the arm: the arm in the aws76 pose passes over the plough top, ~20 mm above it. In the aws74 pose the arm is behind the plough.

**Fastening.** No screw heads are visible on the plough faces in any photo. The plough is probably fastened by screws from inside
or from the top plate edge into the plough rim, or by screws through the plough sides hidden by the wheels (guess). The CAD uses
2 × M2 through the side walls into heat-set inserts in the chassis, plus the chassis front wall as a locator.

**Mechanism.** Passive ramp/plough. It gets under the opponent and guides it into the arm's reach. The tape lowers friction and
protects the print.

### 4.2 Chassis tub (black)
**Shape.** A rectangular printed tub, ~71 mm wide, ~62 mm long, ~20 mm tall (est.). Its front half is hidden inside the plough.
Its rear half is exposed between and in front of the wheels.
- Side walls (aws74): vertical and flat, with a row of **4 tall rectangular windows** (about 3 × 8 mm each, ~6 mm pitch, est.) in the
  lower half of the exposed side behind the plough. Blue parts (probably the motor cans or a blue ESC wrap) show through them.
- Rear wall: flat, with a low raised ridge on top. The red/orange prongs at the rear in aws74 belong to the cradle (4.10).
- Bottom: flat, about 2-3 mm off the floor (guess, from the wheel size and the ground line).
- Inside (guess): two motor pockets across the rear for the drive gearmotors, a battery bay in the middle or nose, and room under the
  gear for the arm servo and its pinion.

**Position.** The rear face is ~4-6 mm in front of the wheel back. The wheel axles pass through the side walls near the rear,
~10 mm in from the back face, at about half the tub height. The side walls are ~71 mm apart outside, so each tyre's inner face is ~1-2 mm
outside its wall.

**Fastening.** It is the root part. The plough, top plate, cheek link and cradle attach to it.

### 4.3 Top plate (black)
**Shape.** A flat printed plate, about 2 mm thick, covering the chassis from the rear wall forward to the plough top edge. It has:
- a **rectangular opening at the front centre** for the gear, about 16-18 mm wide (est.: gear width + ~3 mm each side), open
  towards the plough. The gear's lower half passes through it into the tub.
- **angled slots** on each side of the gear opening: aws73 shows 3 long slots on each side (about 3 mm wide, 15-20 mm long, est.),
  running diagonally like a chevron (each slot slants towards the centre at the front). aws76 shows the left side's slots as
  3 parallel, slightly angled slots, with a further short slot nearer the edge. These are lightening and ventilation slots, and the
  electronics show through them.
- one or two **raised steps**: aws76 shows the plate rising by about 1-2 mm in a step near the middle, with the rear section
  slightly higher (the plate may be two pieces or have a raised rear section, guess).
- Rounded corners, radius about 3 mm.
- **Screws**: silver button-head screws, head Ø ~4 mm. aws73 shows them at the 4 outer corners plus about 2 more at the
  middle of each long side (6-8 total). aws76 shows 2 at the front left corner area, 1 at the rear right corner and 1 at the
  mid left side. aws74 shows 3 along the left side (front, middle, rear) and 1 at the rear corner. They are M2 or M2.5 (est.).
  Each screw sits 3-4 mm in from the plate edges.

**Colour.** Matte black textured print (looks like a textured PEI bed finish on the upper face).

**Position.** It sits on top of the chassis walls, flush with the outer faces. Its front edge butts against the plough top
rim from inside, with the plough rim 2-4 mm higher. The gear passes through the front opening with ~1-2 mm clearance each side.
The cradle sits on its rear centre. The wheel tops are about level with it (within ±2 mm).

**Fastening.** Screwed down into the chassis walls or corner bosses with the screws above. The top plate also clamps the
drive motors and electronics down (guess).

### 4.4 Wheels (2)
**Shape.** Two identical wheels, Ø ~24 mm, ~10 mm wide.
- aws74: a black tyre with a fine knurled/ribbed tread (many small transverse ribs, ~30 around), and a black printed hub with 3 curved
  spokes and a small centre boss with the shaft hole.
- aws76: chunky black tyre treads (larger ribs, about 16-20 around) and a translucent grey dished hub (reprinted or different wheels).
- aws73: black wheels with ribbed treads, the outer face slightly dished.

**Position.** Outside the chassis at the two rear corners. The axle sits ~10 mm in front of the robot's rear end and at about
half the chassis height (~12 mm above the floor). The inner face of each tyre is ~1-2 mm outside the chassis side wall. The tyre outer
face is ~3-5 mm outside the plough side line. The tyre top is at about the top plate height. The tyre bottom is the lowest point
(floor contact). The front of the tyre is ~2-3 mm behind the plough's rear cut end. There are **no wheel guards**: the wheels are
fully exposed at the sides, top and rear.

**Fastening / mechanism.** Directly on the output shafts of two micro gearmotors inside the tub (guess: N20-size metal
gearmotors, 3 mm D-shaft, press fit or grub screw). 2WD with skid steering. The plough lip/skirt is the front contact point (the robot
sits slightly nose-down on the plough lip, or the lip floats ~1 mm up).

### 4.5 Drive gearmotors (hidden)
**Not visible.** They are probably two N20-class micro gearmotors placed across the rear of the tub, back to back, with their
shafts out through the side walls to the wheels (guess). The blue colour seen through the side windows and top slots may be the
motors' blue wraps or a blue-wrapped ESC (guess). They sit between the side windows and the rear wall.

### 4.6 Big gear (white)
**Shape.** A spur gear about 32 mm tip diameter (est.: 1.3 × wheel), about 16-18 teeth (aws74 shows ~15 teeth over ~300 degrees; aws76
shows ~9 teeth over the visible half). Straight teeth, tooth depth about 2.5-3 mm, a printed involute-like form with flat tips.
Thickness about 12 mm (aws73: the gear seen edge-on is a block about as wide as the arm is thick plus ~4 mm; aws76: face width ≈ 12 mm, est.).
- It has a central bore for the pivot screw. A hex socket screw head shows at the centre in aws74, sunk in the black cheek link.

**Position.** On the robot centreline (aws73 suggests slightly left of centre, about 2-4 mm, est.). The axle is about 2-4 mm above the top
plate (≈ 26 mm above the floor). It is at about 52 % of the length from the front, so the gear's front teeth overhang forward into the
plough notch and its bottom teeth go down into the tub through the top-plate opening (about 12-14 mm below the plate).
- Gap to the top-plate opening sides: ~1-2 mm. Gap to the plough notch: ~1-2 mm.
- The arm leaves the gear at its rim on the upper rear quadrant in aws74 (the arm root covers the gear's top-rear teeth). In aws76
  it leaves at the upper front quadrant (the arm is rotated forward there).

**Fastening.** A pivot screw (est. M3 socket head) runs along the x axis through the black cheek link into the gear (or through
the gear into a second cheek on the far side, guess).

**Mechanism.** The gear is the arm's drive gear. A hidden pinion on a servo or geared motor in the tub meshes with its lower
teeth through the top-plate opening (guess, typical for a gear-driven hammer/axe robot). Turning the pinion swings the arm about
the x axis: forward to strike down onto the opponent in front of the plough, backward to rest in the rear cradle (guess).

### 4.7 Arm (white)
**Shape (saw fit, aws73/aws74).**
- A flat printed bar ~8 mm thick (x) and ~9-11 mm wide (y) at the bottom, printed as one piece with the gear (same white plastic,
  no seam visible).
- Side profile (aws74): it rises from the gear's upper rear rim almost vertically, with a slight bow to the **rear** in the
  middle (the mid-height is ~5-8 mm behind the gear centre). Then it widens at the top into a head.
- **Mid fin**: at about 60-75 % of the arm height a white triangular fin sticks out to the rear by ~15 mm. Its upper edge is
  nearly horizontal and its lower edge slopes back down to the arm. aws74 shows it to the right of the arm, behind the wires.
  It is thinner than the arm (~4-6 mm, est.).
- **Head**: the top ~25 mm is wider (~18-20 mm in y). It carries a crescent-shaped white horn that curves forward over the top of
  the saw disc, like a beak (aws74: a white curve above the disc, with the disc's green edge just inside it). The motor mounts on the
  left face of the head in aws74 (the disc is on the camera side), so the motor and disc hang off the arm's left side.
- aws73: the arm looks straight and plain from the front, leaning ~10 degrees towards the camera (forward-left) because the
  pose differs. The black sleeve sits at ~25-35 % of the height.

**Shape (axe fit, aws76).** A plain curved bar, constant ~10 mm width, ~85 mm long, curving forward (concave side forward-down),
leaning ~35 degrees forward of vertical at the top. The tip is cut square and carries the axe blade on its front/left face.

**Colour.** White/ivory (slightly creamy in aws76).

**Position.**
- Base: on the gear, ~26 mm above the floor, on the centreline.
- In aws74 the arm stays within ~10 mm of the gear centre in y over its whole height. The saw centre is ~2-4 mm behind the gear centre.
- At the root the arm passes ~5-8 mm above the rear part of the top plate, with no contact.
- The rear cradle (4.10) is behind and below the arm. The arm probably folds back into it (guess).

**Fastening.** One piece with the gear. The motor is screwed to the head (4.8). The sleeve wraps the arm and the wires (4.11).

### 4.8 Weapon motor (saw fit)
**Shape.** A small outrunner, ~18 mm diameter × ~16 mm long (est.; aws73 shows a black can with a silver band and "TC" lettering).
The bell has 4 small screw holes and a centre shaft. The disc is clamped on the bell face.
**Position.** On the left side face of the arm head (aws74, camera side), axis along x. The base is against the arm and the bell
faces outward. The motor axis is ~100 mm above the floor (est.), level with the head. Its outer bell face is ~16 mm outboard of the arm face.
**Fastening.** Screwed through the arm head into the motor base (guess: 2-4 × M2, hidden behind the disc).
**Mechanism.** Direct drive. The disc spins about x (in the y-z plane) and cuts or hooks the opponent when the arm swings down.

### 4.9 Saw disc (saw fit)
**Shape.** A flat disc ~26-30 mm across the tips, with 6 **hook teeth** (each tooth is a curved hook, like a circular-saw or ratchet tooth,
all pointing the same way round). The root circle is ~20-22 mm diameter. There is a 5-hole pattern at the centre: 4 small screws in a
cross on a ~5 mm circle plus 1 centre screw (aws74). Thickness ~1-1.5 mm (est.).
**Colour.** aws74: black face with a bright green outline/edge layer (a green-coated disc, a two-layer disc, or a green printed guard
behind it, guess). aws73: bare silver steel.
**Position.** Outboard (left, camera side) of the motor bell, centred on the motor axis. The tips reach ~2-4 mm beyond the white head outline.
**Fastening.** 4 × M2 screws into the bell (5 mm pattern).

### 4.10 Rear cradle (U fork)
**Shape.** A small printed U: two upright prongs about 4 mm square and ~10 mm tall, joined at the bottom by a curved web, with a
round-bottomed slot between them about 8-9 mm wide (aws76, orange). aws74 shows two red prongs at the rear (the same part in red).
**Position.** On the top plate at the rear centre, ~5-8 mm in front of the rear edge, with the slot open upward and running
front-to-back, so a bar lying along y drops into it (guess: the arm rests in it when folded back, or it holds the locking pin).
**Fastening.** Probably screwed or glued to the top plate (guess; no screw visible).

### 4.11 Wires, sleeve and connectors
- 3 black silicone motor leads (~22 AWG, est.) run from the weapon motor down the arm's rear edge. They are held together and against
  the arm by a ~12 mm long black heat-shrink sleeve (aws74 at ~45-60 % of the arm height, aws73 at ~30 %).
- At the bottom of the sleeve, just above the top plate, the leads end in **red insulated crimp/bullet connectors** (aws74: 2-3 red
  ferrules visible) that plug into matching leads from inside the tub. The black wire then goes down into the tub behind the gear (aws74).
- aws73 shows thin blue and black wires in a loop on top of the top plate at the rear left, running into the slots (receiver aerial or
  ESC leads, guess).

### 4.12 Cheek link / pivot plate (black)
**Shape.** A black printed plate ~4 mm thick, a rounded oblong ~20 mm long and ~12 mm wide (est.) with fully rounded ends. A
socket screw sits in its upper end, on the gear axis.
**Position.** On the left face of the gear (camera side in aws74/aws76), in contact with the gear face (0 mm gap; it is the bearing
face). Its upper end is at the gear centre. It runs down and **forward** at about 40-50 degrees to the lower front, where it disappears
into the top-plate opening. aws76 shows the same plate angled down to the front-left. There is probably a matching plate on the right (guess).
**Fastening.** The pivot screw at the upper end runs through it into the gear. The lower end is presumably screwed or keyed into the
chassis floor or walls inside the opening (guess).
**Mechanism.** It carries the gear and arm pivot. It may itself be the servo horn or a side plate of the servo saddle (guess).

### 4.13 Axe blade (aws76 only)
A flat steel blade ~30 mm long, ~12 mm wide at the root, tapering to a point, angled ~70 degrees to the arm so it points
forward-down like a pick or beak. It has a sharpened bevel on the leading edge. 2 pan-head Torx screws hold it to the side face of the
arm tip, one near the tip and one ~8 mm lower.

### 4.14 Hidden electronics (guess)
A 2S LiPo (~15-20 g), a combined receiver + drive ESC, a weapon ESC for the outrunner and a power switch are inside the tub (guess).
None are visible. The power switch is probably reached through one of the top-plate slots or a hole in the rear wall (guess).

---

## 5. Per-view checklists (what a render from that camera must show)

### aws74 side (from the left, low)
- Left: the red plough. The lower front wedge slopes back from the lip, then the hood band rises to the flat top edge at ~28 mm.
  The side wall has a darker lower chamfer.
- Middle: the white gear (~32 mm, 15+ teeth visible) with the black rounded cheek link and the centre screw. The gear axle is just above the top plate.
- Behind the gear: the black top plate edge with 2-3 silver screws, and the black chassis side with 4 windows showing blue.
- Right: the left wheel, black, Ø24, 3-spoke hub, centred ~10 mm from the rear.
- Above: the white arm rising to ~100 mm, the black sleeve with 3 black leads, red crimps at the bottom, the rear fin at mid height,
  and the saw head at the top with the black/green 6-hook disc and the white horn above it.
- At the rear right: red cradle prongs just above the top plate.

### aws76 front-left iso
- Lower left: the big taped orange front face, the chamfered corners, and the side wall with its lower facet running back to just
  before the wheel at the right.
- Centre: the white gear in the plough notch. The black cheek link angles down-forward on its left face, with a screw at the gear centre.
- The black top plate with slots on the left half, 4-5 silver screws, and the orange U cradle at the rear centre.
- Right: the left wheel with chunky treads and a clear hub, sticking out past the plough side.
- Arm: a plain white curved bar leaning forward, with the steel axe at its tip pointing forward-down.

### aws73 front-left high
- The red plough fills the lower half (taped front face, chamfered corner).
- The black top plate with the angled slot pattern either side of the gear opening, and screws at the corners and sides.
- The white gear edge-on in its opening, with the arm rising towards the camera.
- The black sleeve, then the motor (TC) and the silver saw at the top. Both wheels show at the rear corners.

---

## 6. Contact / gap matrix (est.; 0 = touching, "—" = no relation)

| | plough | chassis | top plate | wheels | gear+arm | cheek link | motor/disc | cradle |
|---|---|---|---|---|---|---|---|---|
| plough | — | 0 (sides and front, screwed) | 0 at the front edge, rim 2-4 above | 2-3 gap | 1-2 gap at the notch | 1-3 gap | — | — |
| chassis | 0 | — | 0 (screwed) | 1-2 gap (shaft through the wall) | lower gear teeth inside, ≥1 gap | 0 (screwed, guess) | — | — |
| top plate | 0 | 0 | — | tyre top ±2 of the plate | 1-2 gap each side of the opening | 1-2 gap | — | 0 (mounted) |
| wheels | 2-3 | 1-2 | — | — | — | — | — | — |
| gear+arm | 1-2 | ≥1 | 1-2 | — | — | 0 (pivot face) | 0 (motor screwed to the head) | arm rests in it when folded (guess) |
| cheek link | — | 0 | 1-2 | — | 0 | — | — | — |
| motor/disc | — | — | — | — | 0 | — | — | — |
| cradle | — | — | 0 | — | 0 or gap (pose) | — | — | — |

---

## 7. Screws and fasteners (visible and inferred)
- Top plate: 6-8 silver button heads (est. M2.5 × 6-8), at the 4 corners and at the middle of each long side, threading into the chassis walls.
- Gear pivot: 1 socket head (est. M3) at the gear centre through the black cheek link. If there is a matching right cheek, a nut or
  insert sits on the far side (guess).
- Cheek link lower end: 1 screw or a key into the chassis (guess).
- Weapon motor: 2-4 × M2 through the arm head into the motor base (guess, hidden).
- Saw disc: 4 × M2 on a 5 mm circle into the bell, plus 1 centre screw (aws74).
- Axe blade (aws76): 2 pan-head Torx screws.
- Plough: hidden fasteners (guess: 2-4 screws through the side walls or up from below into the chassis).
- Cradle: hidden (guess: glued, or 1-2 small screws from below the top plate).

---

## 8. Mechanism summary
- **Drive**: 2 rear wheels on 2 micro gearmotors, skid steer. The front rests on, or floats just above, the plough lip.
- **Weapon**: a gear-driven overhead arm. A hidden servo/gearmotor pinion turns the large white gear, which swings the arm about the
  x axis. The head carries either a small spinning saw (outrunner direct drive, aws73/74) or a fixed steel axe/pick (aws76). The arm
  hits down in front of the plough. The rear U cradle probably catches the arm when it is folded back (guess).
- **Power**: a LiPo, receiver/ESC and weapon ESC in the tub under the top plate (guess, not visible). The weapon motor's leads run up the
  arm in a sleeve and plug in with red crimp connectors just above the plate.

---

## 9. Rebuild recipe (numbers to model with; CAD frame, wheel axle at z = 0, wheel radius 11)
1. Tub: x ±35.5, y -45..+14, z -9.5..+10, 1.5 mm walls and floor. Add 2 gearmotors at y -36 across the rear, shafts out through the side walls.
2. Top plate: 2 mm on top (z 10..12), with a gear opening x ±12 from y ≈ -9 forward, 3-4 slots each side, and corner screws 4 mm in from the edges.
3. Wheels: Ø22 × 10 at x ±42, y -36 (outer face ~47 mm from the centreline), ribbed tread.
4. Plough: a 1.8-2 mm shell. Front lip at y +63, z -9 (about 2 mm off the floor). Front face rising to y +48, z +14, then steep to z +18 at y +44,
   flat top back to y -21. Plan: x ±40 with 10 mm 45-degree corner chamfers to x ±34 at the front. Side skirt chamfer from z -1 at x ±40 to z -9 at x ±35.
   Notch: an arc of radius ~17.5 round the gear axle.
5. Gear: 18 teeth, tip radius 16, root 13.6, 12 thick, axle at y +8, z +14, on the centreline. Black cheeks either side (x ±6.5..9.5).
6. Arm: centreline (y, z) = (8, 14) → (3, 45) → (-1, 70) → (2, 92), 9 mm wide tapering to 7, 8 thick, rear fin at z 62-82, head pad Ø15.
7. Weapon motor: TC1404 on the arm head's +x face, axis x at (y 2, z 92). Disc: 6 hook teeth, root r 11.5, tips r 14, 1.5 thick, outboard on the bell.
8. Colours: plough #e2412c, tub and plate #1b1c1f, gear and arm #f1f1ec, disc dark steel, wheels #202226.

---

## 10. Coordinate frame (used by all numbers below)
- Frame **F**: to keep one
  frame for photo and CAD, **F** is the CAD frame. Origin = the robot centreline (x = 0), at the y of the gear axle minus 8 mm
  (so the gear axle is at y = +8), at the height of the wheel axles (z = 0). +x = robot's right, +y = forward, +z = up. The floor is
  z = -11 (wheel radius 11). Angles are measured in the y-z plane from +y towards +z unless stated otherwise.
- Floor-referenced heights (h) in sections 1-8 convert as z = h - 11.

## 11. Every part in all dimensions (mm, F frame; est. unless marked guess)

| part | L (y) | W (x) | H (z) | thickness | radii / angles | centre or anchor in F |
|---|---|---|---|---|---|---|
| plough shell | 84 (y -21..+63) | 80 (x ±40) | 27 (z -9..+18) | 1.8-2.0 wall | front face 59° to floor; hood band 75°; corner chamfers 45° × 8.5 mm (x 34→40 over y 63→53); skirt chamfer 32° from vertical (x 40→35 over z -1→-9) | lip edge line y 63, z -9 |
| plough notch | 30 chord | x ±10.5 | to z +10 | — | arc centre (y 8, z 14), r 17.5, spans ~±60° about the -z direction | gear axle |
| tub | 59 (y -45..+14) | 71 (x ±35.5) | 19.5 (z -9.5..+10) | 1.5 walls/floor | outer corners r 0-1 | centre (0, -15.5, 0.25) |
| side windows | 3 each (y) | — | 8 (z) | through the wall | corners square, pitch 6 | y -30..-8, z -6..+2 (4 windows) |
| top plate | 59 | 71 | 2 (z 10..12) | 2 | corner r 3 | centre (0, -15.5, 11) |
| gear opening | y -9..+14 | x ±12 | through | — | square corners | — |
| plate slots | 18 long | 2.4 wide | through | — | chevron: 15-20° to y (photo); CAD straight | x ±16, ±20.5, ±25, ±29.5; y -30..-12 |
| plate screws | head Ø4 | — | head 1.5 high | — | button head | (±31.5, -41.5), (±31.5, +10.5) plus mid-sides (guess) |
| wheel | Ø22 | 10 | Ø22 | tread ribs 0.9 high | 24-30 ribs; hub dish r 7.5 × 2 deep | (±41.5, -36, 0) |
| gear | Ø32 tips | 12 | Ø32 | 12 | 18 teeth, tip r 16, root r 13.6, tooth tip width ≈ 2.8 (0.32 × pitch) | axle (0, 8, 14) |
| cheek link | 20 | 3-4 | 12 | 3-4 | stadium: two r 6 arcs 14 apart, axis at 45° down-forward | upper arc centre = gear axle; lower arc centre (±7.5, 18, 4) (photo); CAD uses upright cheeks y 1..15 |
| arm (saw fit) | 9 → 7 wide | 8 | 78 (z 14..92) | 8 | centreline spline below | root on the gear axle |
| arm fin | 15 (rear) | 6 | 20 | 6 | triangle (y,z): (0, 62), (-10, 76), (-12, 82), (-2, 78) | rear edge of the arm |
| arm head pad | Ø15 | 8 | Ø15 | 8 | circle r 7.5 about the motor axis | (0, 2, 92) |
| weapon motor | 16 (x) | Ø18.2 | Ø18.2 | — | bell r 9.1, base r 6 | base face at x = +4, axis (y 2, z 92) |
| saw disc | Ø28 tips | 1.5 | Ø28 | 1.5 | root r 11.5, tip r 14, 6 hooks | centre (+16.8, 2, 92), axis x |
| axe blade (aws76) | 30 | 1.5 | 12 | 1.5 | 70° to the arm, bevel 25° | arm tip |
| sleeve | 12 along the arm | Ø10 | — | 0.3 | cylinder | arm z 45..57 |
| cradle | 6 | 16 | 10 above the plate | prongs 4 × 4 | slot r 4.5 semicircle, centre z +18 | (0, -40, 12..22) |

### 11.1 Curves as maths
- **Gear tooth outline** (F, y-z plane about C = (8, 14)): for tooth k = 0..17, the polar points about C are (r, θ) = (13.6, θk), (16, θk + 3.6°),
  (16, θk + 10°), (13.6, θk + 13.6°), with θk = 20°·k. Straight segments join them.
- **Arm centreline (saw fit)**: a quadratic-ish polyline through P0 (8, 14), P1 (3, 45), P2 (-1, 70), P3 (2, 92). The fitted curve
  y(z) ≈ 8 - 0.235 (z - 14) + 0.0021 (z - 14)² (max |error| 1.2 mm against the photo trace). Half-width w(z) = 4.5 - 1.0 (z - 14)/78.
- **Arm centreline (axe fit, aws76)**: a circular arc of radius 75 whose centre is at (y +83, z 14) (forward of the robot). The arm runs from
  θ = 180° (the root at y 8, z 14) to θ = 128° (the tip at y +37, z 73), with θ measured about that centre from +y towards +z. Parametric form:
  y = 83 + 75 cos θ, z = 14 + 75 sin θ. In words: a constant-radius forward bow that leans ~35° forward at the tip.
- **Head horn (aws74)**: an arc centre (y 2, z 92) r 15, θ from 40° to 150° (it covers the upper front of the disc), 3 mm wide.
- **Plough side profile** (y, z), polygon: (63, -9) → (48, 14) → (44, 18) → (-21, 18) → (-21, -9). Front face line: z = -9 + 1.53 (63 - y), for 48 ≤ y ≤ 63.
- **Plough plan** (x, y): (-34, 63), (34, 63), (40, 53), (40, -21), (-40, -21), (-40, 53).
- **Plough front section** (x, z): (-40, 18), (40, 18), (40, -1), (35, -9), (-35, -9), (-40, -1).
- **Saw hook tooth** (disc frame, polar about the axis): for tooth k = 0..5, φk = 60°·k: (11.5, φk), (11.5, φk + 33°), (14, φk + 37°),
  (14, φk + 48°), (11, φk + 58°). The tooth face is the near-radial edge from (11.5, φk + 33°) to (14, φk + 37°).
- **Wheel**: revolve of (r, x) = (1, -5), (9.8, -5), (11, -3.8), (11, 3.8), (9.8, 5), (1, 5) about the x axis.
- **Cradle slot**: semicircle of centre (y -40, z 18), r 4.5, open upward; prongs are 4 × 4 squares at x ±6.5.

## 12. Each feature measured independent ways

Photo pixel measures are in the native photo resolution (aws74 1198 × 1401 px, aws76 1519 × 1569 px, aws73 679 × 818 px).

| feature | (a) mm estimate | (b) ratio to another part | (c) photo pixels | (d) F coordinates |
|---|---|---|---|---|
| overall length | 112 | 4.7 × wheel Ø (24) / 5.1 × wheel Ø (22) | aws74: lip x 160 → wheel back x 1160 = 1000 px | y -47 .. +63 |
| wheel Ø | 22-24 | 0.73 × gear Ø | aws74: 960 → 1160 = 200 px → 22.4 mm at 0.112 mm/px | centre (±41.5, -36, 0) |
| gear Ø | 32 | 1.4 × wheel Ø; 0.29 × length | aws74: x 520 → 830 = 310 px → 34.7 mm (the near face, perspective +5 %) → 33 | axle (0, 8, 14) |
| gear axle height above the floor | 25 | 1.1 × wheel Ø | aws74: centre y 840; centreline ground ≈ y 956 → 116 px × 0.116 = 13.5 mm above the wheel-axle line, i.e. ~25 above the floor | z 14 |
| saw centre height above the floor | 100-103 | 4.3 × wheel Ø | aws74: y 200 → (956 - 200) × 0.116 = 88 above the axle line ≈ 99 above the floor | z 92 (103 above the floor) |
| saw tip Ø | 28 | 1.2 × wheel Ø | aws74: ~180 px (the disc spans x 640 → 820 incl. hooks) → 20 mm (seen partly edge-on) | tip r 14 |
| plough length | 84 | 0.75 × overall length | aws74: x 160 → 900 = 740 px → 83 | y -21 .. +63 |
| plough top height above the floor | 29 | 1.3 × wheel Ø | aws74: far edge y 745 (depth-shifted) → 27-36 | z 18 |
| top plate height above the floor | 23 | 1.0 × wheel Ø | aws74: near edge y ≈ 915 → 17 at the near side + depth correction → 21-25 | z 10..12 |
| width over the wheels | 93 | 1.1 × plough width | aws73: wheel outer faces at x 20 and 665 (perspective, front row ≈ 600 px for 82 mm plough) → 94 | x ±46.5 |
| arm width | 9 | 0.28 × gear Ø | aws74: ~70-80 px at mid height → 8-9 | ±4.5 about the centreline |
| fin reach behind the arm | 15 | 0.47 × gear Ø | aws74: x 800 → 900 behind the arm edge = 100 px → 11-15 | y -12 at z 82 |
| chassis side window | 3 × 8 | 0.13 × wheel Ø wide | aws74: 30 × 70 px → 3.4 × 7.8 | z -6..+2 |

## 13. Consistency check (conflicts and the value used)
1. **Camera elevation of aws74**: REFERENCE.json says 35°, but the near wheel's hub is nearly circular, which means ≤ 15°. *Reconciled*: ~15° for
   pixel conversion. The likeness check uses its fixed 25° camera anyway.
2. **Arm pose**: aws74 is upright with a rear bow; aws76 leans 35° forward. *Reconciled*: model the aws74 pose (saw fit). The aws76 IoU therefore stays low.
3. **Plough height**: the side-photo pixels give 27-36 mm above the floor (the depth correction is uncertain), while aws76 shows the rim only 2-4 mm above
   a plate that is ≈ 1 wheel Ø high (~23-25). *Reconciled*: 29 above the floor (z 18).
4. **Gear diameter**: 34.7 mm from aws74 pixels vs 1.3 × wheel (29-31). The near face is closer to the camera than the wheel's centre plane. *Reconciled*: 32 (tip r 16).
5. **Saw disc size**: the pixels give ~20 mm because the disc is partly edge-on and hidden; "≈ wheel" from aws73 gives 24-28. *Reconciled*: tip Ø 28 (r 14),
   root 23. The CAD's lock-pin hole needs r ≥ 11.6, which favours the larger value.
6. **Cheek link**: the photos show one rounded link angled down-forward on the left. The CAD uses two upright cheeks fused to the tub so the
   pivot is supported both sides. *Reconciled*: CAD deviation, noted in §9.
7. **Wheel size**: aws74 pixels give 22.4; the antweight norm (N20 + 24 mm wheel) gives 24. *Reconciled*: Ø22 (r 11), which also gave better IoU.
8. **Top-plate slots**: aws73 shows them angled (chevron, ~15-20°); aws76 shows them nearly straight. *Reconciled*: straight slots in the CAD (cosmetic only).
9. **Plough fastening**: no screws are visible. *Reconciled*: 2 hidden side screws (guess) so the armour is bolted.

## 14. Why the designer did it (per part, several angles)

**Plough (front + side shell).**
- Fight: a full-width low lip gets under wedges and robots with low skirts and lifts their front, so the arm can strike exposed tops.
  The sloped face deflects horizontal spinner hits upward rather than taking them square. The side wings stop the robot being pushed
  from the side at the front and guard the gear area.
- Construction: a separate shell printed face-down (or nose-up) needs no supports for the slope. It can be reprinted in a new colour
  (red → orange between events) without touching the drive. Tape on the face is a cheap wear layer, renewed between fights.
- Weight: a 2 mm open-bottom shell is light (~12-15 g) for its area.
- Repair: being a bolt-on part, a cracked plough is swapped in minutes.
- Other: the notch in the top edge lets the gear sit low and forward, which lowers the arm pivot and the centre of mass.

**Chassis tub.**
- Fight: a closed box with only small side windows keeps the electronics out of reach. The rear wheels are outside it for traction and
  for driving when the robot is pushed.
- Construction: one print with no supports (open top). The side windows save weight and let the builder see and cool the motors.
- Assembly: everything drops in from above, and then the top plate closes it.

**Top plate.**
- Fight: gives a flat, screwed-down roof that the arm can fold back over. The slots are too narrow for a weapon tip to catch.
- Construction: a flat 2 mm print, fast and stiff. The slots save weight and cool the ESCs. Corner and side screws make it removable
  for charging and repair.
- Other: textured finish from the print bed; it hides scratches.

**Wheels.**
- Fight: outside wheels give the widest track for stable turning and pushing. Ribbed tyres grip dusty arena floors. Rear placement
  puts the drive under the battery and arm weight for traction.
- Construction: printed hubs with rubber or TPU tyres on N20 D-shafts are cheap and quick to swap. Exposed wheels are a known risk accepted
  for weight (no guards = ~6-8 g saved).

**Gear and arm (one print).**
- Fight: a big gear on the arm root gives a high reduction from a small servo/motor pinion, so the arm can lift or slam with torque.
  An overhead arm reaches over wedges and hits the top of the opponent, where armour is thinnest.
- Construction: printing gear and arm in one piece removes a joint that could slip or break, and needs no hub keying.
- Weight and cost: plastic gear and arm are light and cheap to reprint. The arm is a sacrificial part.
- Versatility: the arm head takes either a powered saw (aws73/74) or a plain axe (aws76), so the robot can be re-tuned between events.

**Arm fin and head horn (aws74).**
- Fight: the rear fin stiffens the arm against bending where the sleeve and wires sit. The horn over the disc shields the top of the saw and
  stops the disc's teeth hooking the arena floor or the robot's own plough when the arm swings forward.
- Construction: both are flat extrusions of the arm outline, so they print free with the arm.

**Cheek link.**
- Fight: holds the pivot screw on a wide bearing face, so a hit on the arm is taken by the cheek and the chassis, not by the actuator.
- Construction: a small separate print, easy to replace if the pivot hole wears.

**Weapon motor + saw (aws73/74).**
- Fight: a fast small saw at the arm tip can cut or grind the opponent's top armour while the arm holds it down. It is a
  "control + damage" combination.
- Construction: a ~9 g drone motor directly drives the disc (no belts or bearings to make).
- Weight: a small disc keeps the arm's tip mass low, so the arm actuator can still lift it.

**Axe (aws76).**
- Fight: a sharp point concentrates the impact energy to pierce or dent thin top armour. With no motor or ESC on the arm it is lighter and simpler.
- Construction: a cut steel plate and 2 screws.

**Sleeve + crimps.**
- Fight/reliability: keeps the leads tight on the arm so they cannot snag when the arm moves. The crimp connectors let the arm be unplugged and swapped.

**Rear cradle.**
- Fight: catches the arm when folded back, so a hit on the folded arm goes into the plate instead of the servo gears (guess). It also
  keeps the arm from flopping past vertical.
- Construction: a tiny print, glued or screwed on. It is reprinted in the plough colour, which shows it is a matched accessory.

## 15. Unseen and inner parts (guesses, with confidence)

Confidence tags: **[high]** = almost certain from the class of robot or partial evidence; **[med]** = likely; **[low]** = plausible only.

| inner part | guessed size (mm) | guessed position (F) | why / evidence | confidence |
|---|---|---|---|---|
| 2 drive gearmotors (N20-class, 50:1-100:1) | 12 × 10 × 25 each (+ 3 mm D-shaft 10 long) | across the rear, axis x, at (±22, -36, 0); gearbox faces against the side walls | 2 rear wheels with no external motors visible; blue through the side windows | [high] |
| motor clamp ribs | 2 × 12 × 9 per motor | ribs either side of each gearbox in y, rising from the floor | printed tubs normally hold N20s this way | [med] |
| arm actuator: servo (micro, 9 g class) | 23 × 12 × 22 | under the gear, axis x, output pinion meshing with the gear's bottom teeth at about (0, 8, -2) | a big driven gear with no visible motor; the gear dips into the tub | [med] |
| alternative actuator: N20 gearmotor + pinion | 12 × 10 × 25 | same place | some gear-arm ants use a high-ratio N20 | [low] |
| pinion | Ø8-10, 8 teeth, 6 thick | on the servo output under the gear | needed for the gear drive | [med] |
| pivot screw / shaft | M3 × 20 or a 3 mm steel pin | along x through the gear centre (0, 8, 14) | the screw head is visible in aws74 | [high] |
| second cheek (right side) | 20 × 12 × 4 | mirror of the left cheek at x ≈ +8 | a pivot normally has support both sides | [med] |
| bearing / bushing in the gear bore | 3 mm bore printed sleeve, or a 3 × 8 × 3 bearing (693) | in the gear bore | arm robots often add a small bearing; nothing visible | [low] |
| battery: 2S LiPo 300-450 mAh | 35-45 × 17-20 × 10-12 | middle of the tub, across x, at (0, -18, -3) or in the plough nose (0, +35, -4) | needed; the nose hollow is a common battery bay | [med] |
| receiver + dual drive ESC (e.g. Malenki Nano) | 32 × 19 × 3 | on top of the battery (0, -18, +4) | standard UK ant electronics | [med] |
| weapon ESC (small brushless, saw fit only) | 22 × 11 × 4 | beside the gear, (±18, 0, -6) | the outrunner needs one; the red crimps join its leads to the motor's | [med] |
| power switch | 12 × 4 × 4 slide switch or a BBB screw switch | rear wall or under a top-plate slot, (0, -42, -4) | AWS rules need an accessible switch | [high] that it exists, [low] on its position |
| power link / LED | 3 mm LED | in a top-plate slot | AWS needs an indicator | [low] |
| top-plate screws | M2.5 × 6 into heat-set inserts or self-tapped bosses | 4 corners + 2-4 sides, 3-4 mm in from the edges | screw heads are visible | [high] |
| plough screws | 2-4 × M2 or M3 | through the plough side walls into the tub sides, near y 0 and y +12; or up through the tub floor into the nose | no heads visible, so they are either hidden behind the wheels/floor or countersunk | [med] |
| wiring path | — | battery → switch (rear) → ESC on the battery → motor leads along the rear wall to each motor; weapon ESC → leads up through the gear opening behind the gear → sleeve → motor | aws74 shows the black lead going down behind the gear | [med] |
| aerial | 30 mm wire | looped on the top plate at the rear left (aws73 blue/black loop) | visible loop | [med] |
| floor openings | 10 × 20 window or none | under the battery | weight saving; not visible | [low] |
| internal rib under the top plate at mid length | 2 × 60 × 8 | x = 0 ... y -20 | top plates this size usually need a middle support | [low] |
