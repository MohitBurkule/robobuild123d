# Io: full reference description (rebuild-from-text)

Source: `reference/io.aws63.webp`, 675 x 777 px. It is the only photo. It was taken at an event, on a white speckled table, from above at about 45-55 degrees of elevation. Another robot (a carbon-fibre deck with a red frame and black foam wheels) shows at the top left, and blue plastic boxes and a "Competitor/Robot/T..." label card sit at the right. These are background, not part of Io.

Tags:
- **[seen]** is directly visible.
- **[inferred]** is reasoned from geometry.
- **[guess]** is not visible.

## 0. Coordinate frame

- The origin is at the robot's centre in plan. z = 0 is the axle height, and the floor is at z = -10.
- +y is forward (the flipper's lip end), +x is the robot's right, +z up. Units are mm and degrees.
- Camera reading [inferred]:
  - The image's lower-left yellow bar (pixels (30, 550) to (110, 440)) is the robot's FRONT bumper.
  - The long yellow bar along the bottom ((30, 550) to (360, 725)) is the robot's LEFT side.
  - The camera therefore looks from the front-left, from above, and the robot's +y points to the image's upper-left/left.
- Alternative reading: see section 9.

## 1. View description (pixel facts)

- **Yellow frame [seen]:** a bright saffron-yellow printed U/L-shaped bumper, colour about (240, 200, 40).
  - It runs along the image's left end (the front) and the bottom (the left side), with a small yellow corner at the image right, (600, 290) to (640, 330): the rear-left or rear-right corner.
  - Width of the bar in plan: about 18-22 px.
  - Height: about 20-25 px of visible vertical face.
  - Its outer corners are rounded, radius about 15-20 px.
- **Wheels [seen]:** black foam or rubber tyres with red hub rims, four of them:
  - W-FL at (130, 535): inside the frame corner, its red hub face pointing at the camera-left;
  - W-RL at (370, 665);
  - W-FR at (340, 470): partly hidden under the flipper;
  - W-RR at (595, 330).
  - Tyre diameter about 70-75 px; tyre width about 60-70 px. The tyres are wide (about 1:1 width to diameter).
  - The red hub ring shows as a 6-8 px red band on the outer face of each tyre.
  - The wheels sit INSIDE the yellow frame: the frame passes round their outside faces with about 5 px of clearance.
- **White deck plates [seen]:** cream/white printed blocks, colour about (210, 200, 185):
  - a front deck block between the front wheels at (160, 480) to (390, 640), with 2 screws (210, 605) and (360, 590);
  - a right-hand long rail block at (380, 420) to (600, 640), carrying a screw at (480, 465);
  - a rear block at (470, 230) to (600, 380), with screws at (505, 250) and (530, 355).
  The blocks look like a printed white tub covered by flat lids, all screwed down with silver button-head screws (about 6 visible).
- **Flipper plate [seen]:** a grey brushed-aluminium rectangular plate.
  - Corners at about (115, 400), (420, 30), (530, 120) and (200, 515). It is raised high, about 50-60 degrees from the deck.
  - A strip of fine dot-texture (a grip pattern or anti-slip tape) runs along its upper-left long edge, about 35 px wide.
  - Three silver dome screws sit along its centre line, at (285, 370), (330, 240) and (435, 175).
  - The plate's lower short end has chamfered corners, about 15 px at 45 degrees.
  - Plate size [inferred]: about 90 mm along the long edges (which run parallel to the wheel axles, i.e. across the robot) by about 40 mm along the short edges. Thickness about 2 mm (seen at its edge (420, 30) to (530, 120) as a 5 px band).
- **Flipper bracket [seen]:** a white printed triangular gusset under the plate, from (300, 300) to (500, 200) to (480, 470).
  - It attaches to the plate's underside with the 3 screws.
  - It pivots on a white tab and silver screw at (480, 465), next to the right rail. That pivot is a horizontal axis across the robot.
  - A small grey metal block (a stop or hinge-pin housing) shows at (385, 300) to (420, 340).
- **Wires [seen]:** black and red wires at (290, 470) to (340, 520), plus a white connector, between the front deck and the bracket. A small white servo-horn-like part and a red/blue wire show at (330, 615).

## 2. Overall form

- A small, low, rectangular flipper robot. The body (frame) is about 95 mm long by 80 mm wide by 20-25 mm tall. The flipper plate is about 90 x 45 x 2 mm. [inferred]
- At rest the plate lies flat on top, covering most of the deck: a low "flat box" robot.
- In the photo it is shown fired, rotated about 55 degrees.

## 3. Parts (all dimensions, why, how fixed)

### 3.1 Yellow bumper frame (F)
- **Shape:**
  - A U-channel perimeter bar, 6 mm wide, 22 mm tall, along the front and both sides.
  - It joins at the rear corners, which are rounded r = 8 mm. The front corners are rounded r = 6-8 mm.
  - Outer size 95 x 80 mm. [inferred]
- **Coordinates:** front bar at y = +41 to +47; side bars at x = +-34 to +-40; z from -10 to +12.
- **Colour:** #f0c828.
- **Fixed by:** screws from the white tub into the frame (hidden) [guess], or printed in one piece with the tub floor in a second colour [guess].
- **Contacts:**
  - inner face to the outer tyre faces: about 1-2 mm gap;
  - top edge about 2 mm above the white deck;
  - bottom edge about 0.5-1 mm above the floor (skirt).
- **Why:**
  - Fight: protects the wheels from side hits and keeps opponents from climbing the wheels. Its low front bar acts as a mini wedge or skirt.
  - Construction: printed flat in tough PLA or nylon, cheap and replaceable.
  - Visibility: the bright yellow identifies the team.

### 3.2 White tub and deck blocks (T)
- **Shape:** an inner rectangular tub, about 70 x 66 x 20 mm, with lids:
  - front lid 40 x 25 mm;
  - right rail 70 x 14 mm;
  - rear lid 30 x 25 mm.
- **Colour:** #ece6d8.
- **Screws:**
  - 6 visible M2 button heads: 2 on the front lid, 1 on the right rail, 2 on the rear block, 1 at the pivot.
  - About 2-4 more are likely on the hidden left rail. [guess]
- **Why:**
  - Construction: modular lids give access to the electronics.
  - Fight: the white blocks form the floor and walls that carry the motors.

### 3.3 Wheels W1-W4
- **Shape:** cylinders, diameter 20-22 mm and width 16-18 mm.
  - The black foam tyre has a radial thickness of 5 mm.
  - The red printed hub rim is 1.5 mm proud of the tyre face, outer r 9-10.
- **Positions:** (+-28, +27, 0) and (+-28, -27, 0). [inferred: the wheels sit inside the frame at its four corners]
- **Drive [guess]:**
  - 4 x N20 gearmotors, or 2 motors driving the front and rear wheels on each side via direct shafts.
  - The collector's REFERENCE.json says 2 wheels. The photo clearly shows 4.
- **Why:**
  - Fight: wide foam tyres give grip for pushing. The wheels are tucked inside the bumper.
  - Construction: off-the-shelf foam tyres on printed hubs.

### 3.4 Flipper plate (P)
- **Shape:** an aluminium plate of 90 x 45 x 2 mm, its free end's corners chamfered 4 mm x 45 degrees. A dot-grip strip runs along one long edge.
- **Screws:** 3 M3 button heads in a line on the centre line, at about 12, 28 and 42 mm from the hinge end.
- **Rest position [inferred]:** flat over the deck at z = +12, covering y from -30 to +15.
- **Hinge:** through the white bracket's pivot at about (x = +30, y = -5, z = +5). The axis is ALONG Y if the plate's long edges really run parallel to the axles. See section 9.
- **Colour:** #8c8f93, with a textured strip of #a5a8ab.
- **Why:**
  - Fight: a thin metal plate is tough and light, and the large flat area lifts opponents. The grip strip stops the opponent sliding off.
  - Construction: a laser-cut aluminium off-cut, screwed to a printed arm so that it is replaceable.

### 3.5 Flipper bracket (B)
- **Shape:** a white printed triangular gusset, about 45 long x 30 tall x 8 thick, with a round boss of r 5 at the pivot.
- **Fixed:** to the plate by the 3 screws; it pivots on an M3 shoulder screw.
- **Why:** it puts the hinge low and inboard, near the actuator. The triangle gives stiffness for little mass.

### 3.6 Actuator (A) [guess]
- A servo (9 g class, 23 x 12 x 22 mm), or an N20 gearmotor with high reduction, under the bracket at (x +10, y -5, z 0).
- The white horn seen at (330, 615) suggests a servo. [inferred]

### 3.7 Electronics [guess]
- Battery: a 2S 180-300 mAh LiPo (45 x 17 x 10), under the front lid.
- ESC/receiver: a Malenki-class board (30 x 17 x 4), beside the actuator.
- Switch: on the hidden left side or the rear, slide type.
- Wires: the battery to the switch, then to the ESC; the ESC to the motors along the side rails; the ESC to the servo.

## 4. Part table

| ID | Part | L x W x H (mm) | Colour | Fixed / moving | Fixing | Confidence |
|---|---|---|---|---|---|---|
| F | bumper frame | 95 x 80 x 22, bar 6 wide | yellow #f0c828 | fixed | screws (hidden) | seen |
| T | white tub + lids | 70 x 66 x 20 | cream #ece6d8 | fixed | 6+ M2 | seen |
| W1-4 | wheels | dia 21 x 17 | black + red rim | rotating | motor shafts | seen |
| P | flipper plate | 90 x 45 x 2 | aluminium | revolute | 3 screws to B | seen |
| B | bracket | 45 x 30 x 8 | white | revolute with P | pivot screw | seen |
| A | servo | 23 x 12 x 22 | - | fixed | pocket | guess |
| E | battery / ESC / switch | catalogue | - | fixed | pockets | guess |

## 5. Contact and gap matrix (at rest)

| | F | T | W | P | B |
|---|---|---|---|---|---|
| F | - | inner faces flush to the tub walls (0 mm, bonded or screwed) | 1-2 mm to the outer tyre faces | the plate at rest lies 0-2 mm below the frame top at the front | - |
| T | - | - | 1 mm to the inner tyre faces | the plate rests on the lids | the pivot boss in a slot in the right rail, 0.5 mm |
| W | - | - | front and rear tyres about 10 mm apart | - | - |
| P | - | - | - | - | screwed flat on B |

## 6. Mechanism
- The servo or gearmotor rotates the bracket and plate about the pivot by 0-90 degrees.
- In the photo it is at about 55 degrees.

## 7. Curves
- Frame corners: arcs. Plan centre (+-32, -38), r 8, angles 180-270 (rear-left) and 270-360 (rear-right). Front corners: centre (+-34, +41), r 6.
- Wheels: (y - y_c)^2 + z^2 = 10.5^2.
- Plate chamfers: straight 4 mm x 45 degree lines.
- No splines.

## 8. Several independent measures

| Quantity | Pixels | Ratio | Engineering | Reconciled |
|---|---|---|---|---|
| Frame length | the bottom bar is about 360 px, against a plate long edge of about 480 px | frame length about 0.75-0.85 x the plate | an antweight box limit of 150, typical 90-100 | 95 |
| Plate long edge | 480 px | about 2.1 x the plate short edge (230 px) | 90 x 45 | 90 |
| Wheel diameter | 72 px against the frame's 360 px length | 0.2 | foam tyres of 20-22 are common | 21 |
| Frame height | 22 px | about 0.23 x the length | must clear the wheels: 21 + 1 | 22 |

## 9. Consistency check

1. **Hinge axis.**
   - The plate's long edges are parallel to the wheel axles in the image, so the hinge (along the short end) would run along y: a SIDE-flipper.
   - Most antweight flippers hinge across the robot (axis x). The current CAD and REFERENCE.json use axis x.
   - Reconciled: keep axis x (REFERENCE), with the plate's long edge across the robot (90 mm wide), lifting from the rear pivot. The CAD's long axis was 112 mm along y; that is wrong in size, but the orientation is kept.
2. **Wheel count.** The photo shows 4 and REFERENCE.json says 2. REFERENCE.json is the collector's file and cannot change, so the CAD keeps 2 and the conflict is recorded here.
3. **Plate thickness.** The CAD had a 12 mm slab (53.9 g); the photo shows about 2 mm. Reconciled: a thin plate (about 3 mm printed, or 2 mm aluminium), which also fixes the mass blocker.
4. **Colours.** The CAD had an all-yellow chassis. The photo shows yellow only on the frame, with a white tub and lids. Reconciled: a white deck (decal or plate) inside a yellow rim.

## 10. Why (summary per design decision)

- **Low flat body:** hard to get under, and the plate covers the top. Fight benefit.
- **Wheels inside the bumper:** protected from wedges and spinners.
- **Thin metal plate on a printed bracket:** the cheapest strong flipper, and a quick repair.
- **Modular screwed lids:** fast pit repairs. Construction benefit.
- **Bright two-colour print:** visibility and team identity.
