# Boss Baby: full reference description

This description is written so the robot can be rebuilt from the text alone. Every number is an estimate scaled from the photos.
- **(seen)**: visible in at least one photo.
- **(guess)**: inferred; it cannot be seen.
- Unmarked numbers: measured from the photo with roughly +/-15 % error.

## 0. Sources, axes and scale

### Photos
- `reference/boss_baby.aws72.webp` is the **primary** photo, 1194 x 1007 px.
  - Black-printed version, cut out onto a pure white background.
  - Camera is in front of the robot, raised about 35 deg, and swung toward the robot's LEFT side by about 30 deg. The best automatic match is azimuth 60 / elevation 35 (renders/view_match.json).
  - All four fork tines point roughly toward the camera and down.
- `reference/boss_baby.aws73.webp` is the **secondary** photo, 861 x 751 px.
  - An older, white-bodied build standing on a miniature wooden "EUR" pallet.
  - Camera is front-left and above, about 45 deg elevation.
  - It has the same architecture: two drive sides, a centre outrunner with a disc, and forks at the front. But:
    - the white body is one joined deck, not two separate pods;
    - wide black flat forks are bolted to long black side rails;
    - a long rod wrapped in black tape lies across the top.
  - Use it only to understand the mechanism: motor mount, wheel slots, screw style, how the disc bolts to the bell. Never use it for the black version's outline.

### Axes used everywhere below
- +y is forward (the direction the forks point).
- +x is the robot's RIGHT.
- +z is up.
- z = 0 is the drive axle line, and the floor is at z = -11 (wheel radius about 11).

In aws72 the robot faces the camera, so:
- the **image-LEFT pod is the robot's RIGHT pod (+x)**;
- the **image-RIGHT pod is the robot's LEFT pod (-x)**.

This matters, because the two pods differ: the motor mount, the lid extension and the battery lead are all on the robot's right.

### Scale
- The right pod's front face is about 460 px wide and about 140 px tall in aws72, about 7.5-8 px/mm at that depth. The left pod is farther from the camera and reads about 10 % smaller.
- Overall width over both pods is about 135-145 mm. This fits the 150 mm square, as the weight class requires.
- Overall length:
  - about 58-60 mm of pod;
  - plus 6 mm of fork bar;
  - plus about 40 mm of tine ahead of the bar;
  - so about 105 mm in total.
- Overall height: about 24 mm at the pods, about 47 mm at the disc top, and about 60-70 mm at the top of the loose battery plug.

## 1. Overall architecture
- Boss Baby is a **twin-pod vertical spinner with hinged forks**. Two flat, near-square black boxes ("pods") sit side by side. They are separated by an open slot about 22-26 mm wide that runs the full depth from front to back.
- A brushless outrunner motor sits in the slot on a lateral (x) axis, high up: its axis is a few mm above the pod top plane.
  - Its fixed end (the stator) is held by a black printed cup-and-plate mount on the inboard side of the RIGHT pod.
  - Its rotating bell carries a dark ring disc on its LEFT end. The disc spins in the slot just inboard of the LEFT pod's inner wall, with a few mm of running gap.
- Each pod has one drive wheel inside it, near its outer-rear corner. The tread shows through a rectangular slot in the pod's top plate.
- Each pod's lower front face carries a black printed fork bar with two clevis lugs. Each lug holds a narrow steel tine that slopes down to the floor about 40 mm ahead of the robot.
- The battery lead comes out of the top of the right pod near the slot and sticks up and outboard. It is a red/black twisted pair ending in a red plug in black heat-shrink.
- A white 3-pin JST plug lies loose on top of the left pod beside the disc.
- Finish: the main body (pods, top plates, fork bars, motor cup) is matte black FDM. It shows layer lines on the vertical faces and a diagonal (about 45 deg) top-skin infill pattern on the top plates.

## 2. Part table

| # | Part | Count | Colour | Material | Size (mm, x * y * z) | Where (model coords) |
|---|---|---|---|---|---|---|
| 1 | Right pod tub | 1 | black | FDM (PLA or nylon, guess) | 56 * 58 * 21 | x 13..69, y -29..29, z -9..12 |
| 2 | Left pod tub | 1 | black | same | 56 * 58 * 21 | x -69..-13, mirror of 1 |
| 3 | Right top plate | 1 | black | FDM, 2.5-3 thick | 56 * 58 + inboard rear extension about 12 * 22 | z 12..14.5 |
| 4 | Left top plate | 1 | black | FDM, 2.5-3 thick | 56 * 58 | z 12..14.5 |
| 5 | Top-plate screws | 7 seen, about 8-10 total | silver | steel M2 cross-head pan/button | head about 3.5 dia, 1 tall | edge mid-lines and rear-inboard corners |
| 6 | Wheels | 2 | black | rubber tread (seen), printed hub (guess) | dia 22, width 7-8 | x +/-58..61, y -12..-14, z 0 |
| 7 | Drive gearmotors | 2 | hidden | N10/N20 class (guess) | 10 * 12 * 25-33 | inside the pods, inboard of the wheels, axis x |
| 8 | Weapon outrunner | 1 | red bell ends, black centre band | about 1806-2205 class (guess) | dia 23-25, length about 20 | axis x at y about 7, z about 18 |
| 9 | Motor mount (cup + plate) | 1 | black | FDM | cup dia 27 * 6 long; plate 4 * 25 * 28 | on the right pod inboard wall |
| 10 | Weapon disc | 1 | dark faces, bright edge | hardened steel (guess) | OD 56, ID 28-30, t 3 | plane at x about -8 |
| 11 | Disc hub | 1 | black | printed or alloy (guess) | dia 20-22, t 3 | between the bell and the disc |
| 12 | Left shaft upright | 1 | black | FDM (partly seen) | 4 * 18 * 20 above the lid | left pod inboard wall at the axis |
| 13 | Fork bars | 2 | black | FDM | 40 * 6 * 7 | on each pod front, z -6..+1 |
| 14 | Clevis lugs | 4 | black | part of the bar | 7 * 7 * 9 | 2 per bar, 11-13 apart |
| 15 | Fork tines | 4 | silver steel | steel strip | 5 wide * 1.3 thick * 46 long | sloping from the lugs to the floor |
| 16 | Fork-bar screws | 4 | dark | M2/M3 (guess) | head about 4 | ends of each bar, along -y |
| 17 | Stator screws | 4 | black | M2.5/M3 caps | head about 4.5 | outboard face of the mount plate |
| 18 | Battery lead + plug | 1 | red/black wire, black sleeve, red housing | n/a | about 50 long free | exits the right lid rear-inboard |
| 19 | JST 3-pin plug | 1 | white | nylon | 10 * 6 * 5 | loose on the left lid |
| 20 | Battery, ESCs, receiver, switch | n/a | not visible | catalog parts (guess) | n/a | inside the pods |

Not present on this robot: wheel guards, outboard wheel brackets, guard-to-chassis supports, top armour, side armour plates, wedge plates or skirts. Do not add any of them. The wheels are fully enclosed by the pod walls, which act as the guards.

## 3. Pods (tubs)

### 3.1 Shape and size
- Each pod is a closed, flat-sided rectangular box: a printed tub (floor plus four walls) with a separate top plate laid on it and screwed down.
- In plan each pod is close to square:
  - width (x) about 54-58 mm;
  - depth (y) about 55-60 mm;
  - so width/depth is about 0.95-1.0.
- Height, floor to the top of the top plate, is about 23-25 mm. The tub is about 21 mm of that and the plate about 2.5-3 mm.
- Pod height is about 0.42 x pod width.
- The pod underside sits about 2 mm above the floor **(guess)**; only the wheels touch the ground. The fork tips rest on it lightly.

### 3.2 Corners and edges
- Vertical edges are sharp, with at most about 1 mm radius.
- The top-plate rear-outer corner of the LEFT pod is visibly rounded (radius about 4-5 mm, seen at the far right of aws72).
- The right pod's rear-outer corner reads square, with a slight bevel.
- The top edges have no visible chamfer: the plate edge is square.

### 3.3 Outer side faces
- The right pod's +x face is seen as a sliver at the image far left. The left pod's -x face is seen as a long dark parallelogram on the image right.
- Both are plain flat walls. No wheel, axle, hub or opening shows on them, so **the wheels are inboard, inside the pods**.

### 3.4 Front face
- From the pod bottom to about z = +1 it is a plain wall, with the fork bar screwed on (section 7).
- Above that the wall rises to the top plate.
- The top plate's front edge sits flush or about 0.5 mm proud, and shows as a light seam line about 3 mm below the top surface (seen on both pods).

### 3.5 Inner faces (toward the slot)
Flat walls running full depth.
- **Right pod**: the motor mount plate (part 9) sits against this wall in the rear-middle region, centred about y = +5. The wall below the motor mount is plain.
- **Left pod**: a dark vertical block (part 12) stands at the motor axis position. It is seen through the disc's central hole and as a dark rectangle just above the disc rim behind it (aws72 px about 690,260). It is the second shaft support.

### 3.6 Rear faces and internals
- Rear faces: not visible. Assume plain walls with the power switch on a rear or inner wall **(guess)**; aws73 shows nothing useful here.
- Internals:
  - wall thickness about 1.5-2 mm **(guess)**;
  - inside, a clamp for each drive gearmotor, the battery (most likely in the left pod), the drive ESC/receiver and the weapon ESC **(guess)**;
  - screw bosses under each visible top screw position.

### 3.7 Relative position of the two pods
- The inner walls face each other across the slot, about 22-26 mm apart. Slot width is about 0.42 x pod width.
- Both pods share the same front plane and the same rear plane: they are not staggered fore-aft. Their top planes are at the same height.
- They are mirror images of each other except for:
  - the right lid extension;
  - the motor mount on the right;
  - the left shaft upright.

### 3.8 What joins the pods
- Nothing at the front: white background shows through the slot under the motor and between the two fork bars (aws72 px 560-650, 450-520; also the notch in the photo mask). So the slot is open at the front and under the motor.
- The pods must be joined at the REAR, behind the disc. Options:
  - a beam or plate between the inner walls at the back **(guess, structurally required)**;
  - and/or the right lid's inboard extension (section 4.1), which spans part of the slot at the rear;
  - and/or the motor itself, from the right mount to the left bearing upright. This alone is not enough.
- Model a rear beam about 6-9 mm deep (y), full pod height, between the inner walls. It must clear the disc sweep (axis about y 7, z 18, r 28) by at least 1.5 mm. With those numbers its front face must be at y <= -22.

## 4. Top plates (lids)

### 4.1 Right top plate (+x pod, image-left), about 2.5-3 mm thick
- **Outline**: an L / hook shape rather than a rectangle.
  - Over the tub it covers the full tub top (about 56 wide x 58 deep).
  - At the REAR it extends inboard past the tub's inner wall by about 10-14 mm, over the slot behind the motor, from the rear edge forward to about y = -8.
  - The extension's front edge is a **concave arc** (radius about 30-40 mm). It sweeps from the slot side back and around toward the pod's front-inboard corner, so it hugs the motor's rear-bottom.
- **Front-inboard step**: in front of the arc, the top plate's front-inboard corner is cut away by the same arc. A tub surface about 4-6 mm lower (a ledge) shows there (aws72 px 330-550, 520-640). The visible edge of the plate is that arc.
- **Notch**: a rectangle about 10 x 14 mm in the plate's inboard edge, level with the motor axis.
  - The mount plate (part 9) stands up through it.
  - A black wire loop is visible in the notch: the motor's phase leads going down into the pod.
  - The plate wraps around the mount on three sides with about 0.5 mm clearance.
- **Wheel slot**:
  - about 9-10 mm wide (x) by 22-25 mm long (y), with square corners;
  - near the OUTER-REAR corner, its centre about 9-11 mm in from the outer side and 15-18 mm forward of the rear edge;
  - the black treaded tyre fills it, its top flush with or up to 1 mm above the plate.
- **Battery-lead hole**:
  - round, about 4-5 mm;
  - on the extension about 6-10 mm in front of the rear edge, just inboard of the tub's inner-wall line;
  - the twisted red/black pair comes out of it.
- **Screws**: see section 6.

### 4.2 Left top plate (-x pod, image-right), about 2.5-3 mm thick
- A plain rectangle, about 56 x 58. The rear-outer corner is rounded (radius about 4-5).
- Wheel slot near the OUTER-REAR corner, the mirror of the right one (about 9-10 x 22-25), with the tyre flush.
- No inboard extension: the inboard edge stops at the tub's inner wall (about 2-3 mm from the disc face).
- The front edge reads very slightly convex in aws72. This is most likely lens perspective **(guess: straight)**.
- The white JST plug lies on it about 5 mm outboard of the disc, at about mid-depth.

## 5. Wheels and drive

### Wheels
- 2 wheels, one per pod, near the outer-rear corner. Axles run along x.
- Diameter about 20-24 mm, so the pod height is about wheel diameter + 2 mm. Tyre width about 7-8 mm.
- The tyre is black rubber with a coarse transverse (paddle) tread, about 1.5 mm pitch and about 0.8 mm deep, clearly visible in both slots.

### Wheel position
- Wheel centre about 9-11 mm in from the outer side wall and 15-18 mm forward of the rear wall. In model coordinates: x about +/-58..61, y about -12..-14, z = 0.
- Each wheel is enclosed on its outboard side by the pod wall (gap about 1.5-2.5 mm), and on the front and rear by the tub interior.
- It reaches the ground through an opening in the tub floor (about 10 x 25).
- It reaches up to the top-plate slot.

### Drive motors
- Hidden. Most likely N10/N20 micro gearmotors lying along x, inboard of each wheel, with the shaft pointing outboard into the hub **(guess)**. A D-shaft into a D-bore printed hub **(guess)**.
- Motor length about 25-33 mm, so each motor occupies the region from about 3 mm inboard of the wheel to about 30 mm inboard.

### Drive layout
- 2WD differential steering.
- The wheels are behind the pod mid-depth, so the robot rests on the two wheels and the fork tips (or the front pod corners).
- The centre of mass is between the wheels and the forks.
- It is **not invertible**: the disc and motor stand about 20-30 mm above the pod tops, and the wheels barely reach the top plane.

## 6. Screws (visible)
All top-plate screws are small silver cross-head (Phillips) pan or button heads:
- about 3.5 mm across;
- standing proud by about 1 mm (not counterbored);
- probably M2 self-tapping into tub bosses, or M2 into heat-set inserts **(guess)**.

### Right top plate (+x), seen in aws72
1. On the extension near the battery-lead hole: about 4 mm from the rear edge, about 8 mm outboard of the lead hole (px about 215,330).
2. Rear edge at the inboard end of the tub, about 4 mm from the rear (px about 410,322).
3. Outer side edge: about 4 mm in from the outer side, about 35-40 % of the depth from the rear (px about 95,480), just in front of the wheel slot.
4. Front edge at about the middle of the pod width, about 4 mm in from the front (px about 300,598).

Possibly a 5th at the front-inboard ledge, hidden by the motor **(guess)**.

### Left top plate (-x)
1. Rear edge, inboard end, about 4 mm from the rear, about 6 mm from the inner wall (px about 820,278).
2. Outer side edge, about 35-40 % of the depth from the rear, about 4 mm in (px about 1045,380), just in front of the wheel slot.
3. Front edge, middle, about 4 mm from the front (px about 975,528).

Possibly a 4th at the front-inboard corner, hidden by the disc **(guess)**.

### Placement rule for the rebuild
- Screws go at the edge mid-lines (front middle, outer side middle) and at the rear-inboard corner. They do not go at all four corners.
- Each needs a boss in the tub at that point (6 mm boss, 5+ mm thread engagement).

### Other screws
- **Fork bars**: 2 per bar, one at each end, entering the pod front wall along -y. Dark heads, about 4 mm, proud by about 1.5 mm.
- **Stator**:
  - The black cross-shaped stator base shows 2-3 dark cap screws on the outboard face of the mount (aws72 px about 480-500, 380-480).
  - aws73 shows 4 black cap screws in a square on the white stator plate.
  - Rebuild with 4 x M2.5/M3 caps on a 16 x 16 (or 12 x 12) pattern, along -x from the mount's outboard face into the stator.
- **Disc to bell**: hidden. 4 x M2 or M2.5 on a 9-12 mm circle **(guess)**.

## 7. Forks

### 7.1 Fork bar
- One black printed bar per pod, mounted horizontally on the lower front face:
  - about 40 mm wide (x), 6 mm deep (y, standing off the wall), 7 mm tall (z);
  - top at about z = +1, bottom at about z = -6;
  - centred about the pod's middle, slightly inboard.
- Its ends carry the two dark screws (section 6). The bar face is flat with layer lines.
- Two **clevis lugs** stand forward from the bar's front face, about 11-13 mm apart centre to centre:
  - each lug is a U-shaped / slotted block about 7 wide x 7 deep x 9 tall, its top slightly above the bar top;
  - the slot is about 1.6 mm wide and vertical, open at the front and bottom;
  - a cross pin or small screw runs along x through the lug **(guess, not resolved in the photo)**.
- Lug positions:
  - right pod: about x = +32 and +44;
  - left pod: about x = -32 and -44.
  - The innermost lug is about 18-20 mm outboard of the slot wall.

### 7.2 Tines
- Bare steel strips:
  - about 5 mm wide, 1.2-1.5 mm thick, about 46-50 mm long from the lug to the tip;
  - edges bright, faces slightly mottled (cut steel, unpainted).
- Each tine has a small step about 70-75 % of the way out, where it narrows to about 3.5 mm. The tip is square or slightly angled.
- Orientation:
  - The wide face is mostly up (we see the flat face from above). They are not edge-on blades.
  - They slope down at about 18-22 deg from horizontal, so the tips touch, or come within about 1 mm of, the floor about 40-45 mm in front of the pod front faces (y about +72..+75).
  - In plan, the two tines of a pair are parallel (about 11-13 mm apart) and splay outward only very slightly (0-5 deg).
- **Mechanism**: almost certainly **hinged**. Each tine root sits in its clevis on a cross pin, so it rests on the floor by gravity and rides over bumps (standard antweight hinged forks). A static model at the resting angle is acceptable. If modelled static, each tine needs two fixings (a pin plus a stop) so it cannot pivot.
- **Reach versus the disc**:
  - The tines lead the disc by about 35-40 mm at the floor.
  - The disc's lowest front point is about 30 mm behind the tips.
  - In plan the disc lies between the two pairs, so the tines never cross the disc's path.

## 8. Weapon system

### 8.1 Disc
- A **ring disc**, OD about 56 mm (about 1.0 x pod width, about 2.3 x pod height), thickness about 3 mm.
- The central hole is large: ID about 28-30 mm (ID/OD about 0.5).
  - Through the hole you see the black hub on the bell face and, behind it, the dark left upright.
  - The ring band is about 13 mm wide radially.
- Finish: the faces are dark grey (black-oxide or blued). The outer cylindrical edge and the about 45 deg edge chamfers (about 1 mm) are bright bare steel. This gives the bright-ring look in aws72.
- **2 teeth**:
  - One clear step is visible at the bottom-right of the rim (aws72 px about 760,560). There the radius drops by about 2-3 mm going around, forming a small hook.
  - Assume 2 identical teeth 180 deg apart, each a radial step, with the rim spiralling inward about 2.5 mm from each tip to the next step.
- Position:
  - spin axis along x;
  - disc plane at about x = -6.5..-9.5 (centre about -8). It sits just inboard of the LEFT pod's inner wall (x = -13), with about 3 mm of running gap, and about 1.5-2 mm from the left shaft upright;
  - axis height z about 18 (about 29 mm above the floor). Disc top about z = +46, about 31 mm above the pod tops; disc bottom about z = -10, about 1-2 mm above the floor;
  - axis fore-aft at y about +6..+8, slightly ahead of pod mid-depth. The disc's front reach is y about +34..+36: about 5 mm ahead of the pod front faces, level with the clevis lugs, and well behind the fork tips;
  - the rear reach is y about -20..-22, which sets the rear beam position.
- **Relative to the motor**: the disc is about 2.3 x the motor diameter. It sits on the motor's left (-x) end, flush against the hub.

### 8.2 Disc hub
- A black ring about 20-22 mm in diameter and about 3 mm thick, between the bell face and the disc. It fills the disc's 28-30 mm hole only partly: a gap ring shows.
- In aws72 the inside of the disc hole shows black material close to the edge, so the hub may actually be about 28 mm with a lip **(guess)**.
- Bolting: hub to bell by the bell's top-face holes; disc to hub by 3-4 screws **(guess)**.
- In aws73 the disc has a smaller centre hole and bolts straight to the bell face.

### 8.3 Weapon motor
- A direct-drive outrunner whose bell is the weapon hub.
- Overall diameter about 23-25 mm. Visible length about 20 mm, plus the about 6 mm mount cup on the right.
- Appearance from right (stator end) to left (disc end):
  1. Black printed mount cup.
  2. Red anodised ring (about 5 mm) with oval ventilation windows (one seen, about 4 x 8 mm).
  3. Black centre band (about 8 mm) printed with "...KV", "CE", "RoHS".
  4. Red anodised ring (about 4 mm).
  5. Black hub.
  6. The disc.
- Class about 1806-2205 **(guess)**, roughly a 2204 2300 kV.
- Axis along x at about y +6..+8, z about 18. The motor's bottom (z about 6) is about 6 mm below the pod top plane. Its top (z about 30) is about 15 mm above it.
- It occupies the slot from x about +9 (stator face on the mount) to about -5 (bell face). That is about 14 mm long plus the 6 mm cup outboard of it, inside the mount.
- Gaps:
  - about 2-3 mm from the bell to the right lid's curved edge;
  - about 3-4 mm from the bell bottom to anything below. Nothing is below: the slot is open.

### 8.4 Motor mount (right side)
- A black printed **cup** about 27 mm in diameter and about 5-6 mm long (x), with ridged printed texture on its rim. It wraps the stator end of the motor.
- The cup is part of (or bolted to) a black **mount plate**:
  - about 4 mm thick (x), about 25-28 mm tall, about 25 mm deep (y);
  - standing against the right pod's inboard wall;
  - rising from inside the pod (through the lid notch) to about z = 30-32.
- The stator's cross-shaped (X) base is screwed to the plate's outboard face with 4 caps (2-3 visible).
- Below the cup, the plate continues down into the pod through the right lid notch, where the phase wires go.
- Contact faces:
  - the cup's outboard face sits on the plate;
  - the plate's outboard face is against, or set into, the right tub's inner wall and the lid notch;
  - the plate bottom sits on the tub floor or a ledge **(guess)**.

### 8.5 Left shaft upright
- A dark block on the left pod's inboard wall, behind the disc, at the motor axis (partly seen).
- About 4 mm thick (x), 15-20 mm wide (y), rising from inside the pod to about z = 28-30 (its top edge is seen just above the disc rim's inner edge).
- **(Guess)**: it carries a small bearing (683, 3 x 7 x 3) on the motor's lengthened 3 mm shaft. The rotor is then supported at both ends: motor bearings on the right, this bearing on the left.
- Running gap between the disc face and this upright: about 1.5-2 mm.

### 8.6 Locking
- No lock pin is visible. The rules need one: model a removable 3 mm pin through the right mount, the disc web (between bore and rim) and the left upright, parallel to the axis, at about 14 mm radius above and behind the axis.

## 9. Wires and loose items

### Battery lead
- Two silicone wires, red and black, about 20-22 AWG, twisted.
- Path:
  - leaves the right lid's rear-inboard hole;
  - goes up and outboard (toward the image top-left) about 20 mm;
  - enters a black heat-shrink sleeve about 7 mm in diameter and about 25 mm long;
  - ends in a red rectangular plug housing about 8 x 6 x 14 mm (JST-RCY/BEC style), pointing up-outboard at about 60 deg.
- It stands about 40-50 mm above the lid.
- It is a flying lead, probably the main power lead or the link used as the power switch (a removable link). It is in the photo mask (about 4 % of the mask area), but no CAD part should copy it as structure.

### Other wiring
- **White 3-pin plug** (JST-XH/PH style) on the left lid beside the disc: about 10 x 6 x 5 mm, pins visible. Probably the balance lead or a receiver lead, loose.
- **Phase wires**: a black wire loop shows in the right lid's notch at the motor base, where the three phase leads drop into the right pod.
- **Inside (guess)**:
  - battery to switch/link;
  - to the drive ESC and the weapon ESC;
  - drive ESC to both gearmotors (one run crosses to the other pod through the rear joining beam);
  - weapon ESC to the motor phases through the notch.

## 10. Per-view notes

### 10.1 aws72 (front, raised about 35 deg, camera toward the robot's left)
- Image left to right:
  1. the right pod (near, large);
  2. the black motor cup and mount;
  3. the red/black motor;
  4. the ring disc (seen nearly edge-on to three-quarter, as an ellipse about 150 px wide and 430 px tall);
  5. the left pod (farther), whose outer side face is a long dark parallelogram along the image's right edge.
- Front faces:
  - the right pod's front face shows its fork bar with 2 lugs and 2 tines reaching to the bottom-left (tips at px about 380,950 and 445,950);
  - the left pod's tines reach to the bottom-right (tips at px about 1050,840 and 1090,830).
- Top: the disc's top (px about 200) rises well above both pods (top planes at px about 270-350). The battery plug sticks up at the image top-left.
- Visible faces: both lids, both front faces, the left pod's outer side face, and a sliver of the right pod's outer side face.
- The gap under the motor shows white.

### 10.2 aws73 (older white version)
- One white printed body joined by a deck. The centre outrunner (red bell, a black "FLASH HOBBY" stator label) is mounted on a white plate with 4 black cap screws.
- The disc is a plain circular disc with one tooth step.
- The wheels sit in rectangular openings in the top deck, near the corners.
- Wide black flat forks bolt to long black side rails on both sides.
- It confirms the mechanism:
  - the stator is bolted to a printed plate;
  - the disc is bolted to the bell face;
  - the wheels are inside, seen through top openings;
  - the top screws are pan heads.
- Do not use its outline.

## 11. Contact / gap matrix
Units are mm. "touch" means a shared face; "screw" means fastened; "slot" means the part passes through an opening.

| A \ B | R tub | L tub | R lid | L lid | motor | mount | disc | L upright | bar R | bar L | wheel R | wheel L | rear beam |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| R tub | - | 24 gap | touch top, 4-5 screws | - | about 6 below the bell bottom, open | touch inboard wall (screwed or printed) | 13+ | - | touch front, 2 screws | - | 1.5-2.5 to walls; floor slot | - | touch (guess) |
| L tub | 24 | - | - | touch top, 3-4 screws | 12 | - | 3 running gap to the inner wall | touch inboard wall | - | touch front, 2 screws | - | 1.5-2.5 | touch (guess) |
| R lid | | | - | about 10-14 at the rear (extension), 24 elsewhere | 2-3 from the curved edge | notch, 0.5 all round | 3+ | - | - | - | slot, about 1 | - | sits on (guess) |
| L lid | | | | - | - | - | about 3 sideways | butts (guess) | - | - | - | slot, about 1 | - |
| motor | | | | | - | stator, 4 screws | hub, bolted | shaft to bearing, about 5 axial gap from the disc | - | - | - | - | 3+ |
| disc | | | | | | 12+ | - | 1.5-2 | - | - | - | - | 1.5+ sweep |
| tines | | | | | | | about 35 ahead at the floor | - | pinned in lugs | pinned in lugs | - | - | - |
| wheels | | | | | | | | | | | - | about 120 apart | - |

## 12. Part-by-part narrative: faces, sides, holds

### Right tub
- Its floor underside faces the ground with about 2 mm clearance.
- Its outer (+x) face is the robot's right flank.
- Its front (+y) face carries the right fork bar with 2 screws.
- Its inner (-x) face carries the motor mount plate.
- Its top rim carries the right lid, held by 4-5 screws.
- It encloses the right wheel (rear-outer), the right gearmotor (inboard of the wheel) and, likely, the weapon ESC near the mount (short phase wires).

### Left tub
- The same, mirrored, without the motor mount.
- Its inner face carries the left shaft upright.
- It encloses the left wheel, the left gearmotor and, likely, the battery and drive ESC/receiver.

### Right lid
- Its underside touches the right tub rim and the rear beam (extension).
- Its notch wraps the mount plate.
- Its wheel slot frames the right tyre.
- Its rear-inboard hole passes the battery lead.
- Its concave front-inboard edge faces the motor bell with about 2-3 mm gap.

### Left lid
- Its underside touches the left tub rim. Its inboard edge is about 3 mm from the disc face.
- Its slot frames the left tyre.
- It carries the loose JST plug on top.

### Motor
- Its stator end (+x) touches the mount plate.
- Its bell (-x end) carries the hub and the disc.
- Its shaft continues -x through the disc to the left upright's bearing.
- It hangs in free air over the open slot.

### Disc
- Its right face touches the hub on the bell. Its left face runs about 1.5-2 mm from the left upright.
- Its rim passes about 3 mm from the left tub's inner wall top and the left lid edge.
- Its lower rim runs about 1-2 mm above the floor.
- Its rear rim runs clear of the rear beam.
- It is held by bolts to the hub/bell and by the shaft through its centre.

### Fork bars
- Their back faces touch the pod front walls, held by 2 screws each.
- Their lugs hold the tine roots by cross pins.

### Tines
- Each root sits between the cheeks of a lug.
- The tines touch nothing else except the floor at the tip.

### Wheels
- Each is pressed on its gearmotor shaft.
- Each runs inside its pod with about 1.5-2.5 mm clearance to the walls and lid slot.
- Only the tyre bottom touches the ground.

## 13. Rebuild recipe (the dimensions to use)
1. **Right tub**: x 13..69, y -30..30, z -9..12.
   - 1.6 walls and floor, open top.
   - Floor opening about 10 x 25 at the wheel.
   - Clamp for an N10 gearmotor at y -12, shaft outboard; wheel centre x 61, dia 22, width 8.
   - Bosses under the screw positions of section 6.
2. **Left tub**: the mirror of 1 (x -69..-13).
3. **Rear beam**: x -14.6..14.6, y -30..-21.5, z -9..14.5, hollow for the cross wires. It must clear the disc sweep by 1.5 or more.
4. **Lids**: z 12..14.5.
   - Each has a wheel slot 10 x 25 centred on its wheel.
   - Screws on the front-middle, the outer-side middle and the rear-inboard corner.
   - Right lid: add the rear-inboard extension over the beam with a concave front edge (R about 35), a 4.5 mm battery-lead hole and a notch about 10 x 14 round the motor mount.
5. **Motor**:
   - axis x at (y 8, z 18);
   - stator face against a 5 mm black upright on the right tub's inner face (x 9..14.6, y -7..20, z -9..31.5) with a cup lip about 27 diameter;
   - bell toward -x.
6. **Disc**:
   - 3 mm thick, OD 54-56, ring with an ID about 28 (or a web with 4 large windows if a solid bolt circle is needed);
   - 2 teeth;
   - plane x -9.5..-6.5, bolted to the bell through a black hub.
7. **Left upright**: x -14.6..-11, y -7..20, up to z 31.5, carrying a 683 bearing for the lengthened 3 mm shaft. Lock-pin bore through both uprights at about (y -2, z 28).
8. **Forks**:
   - a 40 x 6 x 7 bar on each front face at z -6..+1;
   - 2 lugs per bar at about x = +/-34 and +/-46;
   - 1.5 x 5 mm tines about 46 long sloping to the floor, tips at about y 75, z -10.5.
9. **Colours**:
   - all printed parts #1c1d20;
   - disc #3a3c40 faces (single-colour model: steel grey #c9cdd3 is acceptable);
   - tines #c9cdd3;
   - motor red #c8202c with a black band;
   - tyres #2a2b2e.
10. **Do not add**: wheel guards, outboard brackets, armour plates, a wedge, or a bridge at the front of the slot.

## 14. Known modelling compromises versus the photo
- The battery plug and the JST plug are not modelled. They are loose wiring, but they count in the photo mask, so they cost a few points of IoU at the top-left.
- If the tines are modelled as vertical plates (thickness along x) instead of flat-up strips, they read thinner from above. The silhouette in aws72 is nearly the same.
- The ring disc's dark faces cannot be shown with a single part colour. Use steel grey (silhouette unchanged).
- The rear joining beam is a guess. It is hidden in the photo behind the motor, so it does not affect the silhouette.

## 15. Full dimensions per part (L x W x H, thickness, radii, angles)
Frame: the one defined in section 0 (+x right, +y front, +z up, origin at the midpoint between the wheel axles, floor z = -11). All sizes are in mm.

| Part | x size | y size | z size | Thickness | Radii | Angles | Centre (x, y, z) |
|---|---|---|---|---|---|---|---|
| Right tub | 56 | 60 | 21 (z -9..12) | walls 1.6, floor 1.6 | vertical edges <= 1 | all faces axis-aligned | (41, 0, 1.5) |
| Left tub | 56 | 60 | 21 | 1.6 | rear-outer corner R 4.5 in plan | axis-aligned | (-41, 0, 1.5) |
| Right lid (main) | 54.4 | 60 | 2.5 | 2.5 | concave front-inboard arc R 35 | arc spans about 60 deg | (41.8, 0, 13.25) |
| Right lid extension | 12 (x 1..13) | 22 (y -30..-8) | 2.5 | 2.5 | front edge = same R 35 arc | - | (7, -19, 13.25) |
| Left lid | 54.4 | 60 | 2.5 | 2.5 | rear-outer R 4.5 | - | (-41.8, 0, 13.25) |
| Lid wheel slots | 10 | 25 | through | - | square corners (R <= 0.5) | - | (+/-61, -12, 13.25) |
| Right lid notch | 6 (x 13..19) | 14 (y 1..15) | through | - | square | - | (16, 8, 13.25) |
| Battery-lead hole | dia 4.5 | - | through | - | R 2.25 | - | (8, -24, 13.25) |
| Wheel (each) | 8 (width) | 22 (dia) | 22 | tyre about 3 radial | R 11 outer, R 6.5 hub | tread pitch 1.5 | (+/-61, -12, 0) |
| Drive gearmotor | 21 body + 9 shaft | 10 | 12 | - | can R 6 | axis +/-x | (+/-44, -12, 0) |
| Weapon motor | 14 | 21 dia | 21 dia | - | R 10.5 (bell), shaft boss R 2.5 | axis x | (2, 8, 18) |
| Mount cup | 6 | 27 dia | 27 dia | wall about 2 | R 13.5 | axis x | (11, 8, 18) |
| Mount plate (right upright) | 5.6 (x 9..14.6) | 27 (y -7..20) | 40.5 (z -9..31.5) | 5.6 | top corners about R 2 | vertical | (11.8, 6.5, 11.25) |
| Disc | 3 (x -9.5..-6.5) | OD 54-56 | OD 54-56 | 3 | outer R 27..28, inner R 14..15, edge chamfer 1 x 45 deg | 2 teeth 180 deg apart | (-8, 8, 18) |
| Disc hub | 3 | dia 20-22 | dia 20-22 | 3 | R 10.5 | - | (-5, 8, 18) |
| Left upright | 3.6 (x -14.6..-11) | 27 | 40.5 | 3.6 | - | vertical | (-12.8, 6.5, 11.25) |
| 683 bearing | 3 | 7 dia | 7 dia | - | R 3.5 / bore R 1.5 | axis x | (-12.5, 8, 18) |
| Rear beam | 29.2 | 8.5 (y -30..-21.5) | 23.5 (z -9..14.5) | walls 1.6 | - | - | (0, -25.75, 2.75) |
| Fork bar (each) | 40 | 6 | 7 | - | edges about R 0.5 | - | (+/-40, 33, -2.5) |
| Clevis lug | 7 | 7 | 9 | cheeks 2 + slot 1.6 + 3.4 | - | slot vertical | (+/-34 or +/-46, 36, -2) |
| Fork tine | 1.5 thick | 46 long | 5 wide (then 3.5 after the step) | 1.3-1.5 | tip square | slope 20 deg down, splay 0-5 deg out | root (+/-34 or 46, 36, -2), tip (same x, 75, -10.5) |
| Top screws | head dia 3.5 | - | head height 1.1 | M2 | dome R about 3 | vertical | see section 6 |
| Fork-bar screws | head dia 4 | - | 1.5 | M2/M3 | - | along -y | bar ends (+/-(40 +/- 17), 36, -2.5) |
| Battery plug | 8 | 6 | 14 | - | - | 60 deg up-outboard | (30, -22, 50) free end |
| JST plug | 10 | 6 | 5 | - | - | flat | (-20, 5, 17) |

## 16. Curves as maths (frame of section 0)
- **Right lid concave edge**: a circle in the plane z = 14.5.
  - Centre (cx, cy) = (2, 12); radius R = 35.
  - The visible arc runs from angle theta = 205 deg (point (-29.7, -2.8), clipped by the lid's inboard limit x >= 1) to theta = 300 deg (point (19.5, -18.3)), measured from +x counter-clockwise.
  - Material lies OUTSIDE the circle: (x-2)^2 + (y-12)^2 >= 35^2 within the lid's front-inboard quarter x in [1, 30], y in [-8, 30].
  - In practice this removes the lid's front-inboard corner and leaves a tub ledge 4-6 mm lower.
  - Equivalent explicit form for the lid edge in that quarter: y = 12 - sqrt(1225 - (x - 2)^2), for x in [1, 30].
- **Left lid rear-outer corner**: a quarter circle with centre (-64.5, -25.5), R = 4.5, theta from 180 to 270 deg.
- **Disc outer profile (2 teeth)**: in the disc's own polar coordinates (angle phi about the x axis, phi = 0 at the +y direction in the rest pose):
  - r(phi) = 27.5 - 2.5 * frac(phi / 180 deg), where frac is the fractional part.
  - Each tooth tip is at phi = 0 and phi = 180 deg (radius 27.5). The rim spirals in to 25.0 just before the next tip, then steps back out radially (the hook).
  - The inner edge is a circle r = 14.5.
  - The edge chamfer is 1 mm x 45 deg on both faces.
- **Disc sweep envelope**: a cylinder about the axis (y 8, z 18), radius 27.5, x in [-9.5, -6.5].
  - Floor clearance: 18 - 27.5 - (-11) = 1.5.
  - Rear clearance to the beam face y = -21.5: dy = 29.5, so the gap is 2.0.
- **Fork tine centreline** (side view, plane x = const):
  - z(y) = -2 - (y - 36) * tan(20 deg) for y in [36, 75];
  - so z = -2 at the lug and z = -16.2 at y 75. The tip is clipped at the floor, so in practice z_tip = -10.5 and the tine is bent or stepped.
  - Simpler model: a straight line from (y 36, z -2) to (y 75, z -10.5), slope 12.3 deg. The photo's apparent 18-22 deg includes perspective, so the reconciled value is 12-15 deg (section 18).
- **Tine plan taper**: half-width w(s) = 2.5 for s in [0, 0.72 L]; w = 1.75 for s in (0.72 L, L], where s is the distance from the lug and L = 46.
- **Wheel**: a circle of R 11 about (+/-61, -12, 0) in the yz plane; tread is 30 lugs, 1.5 pitch, 0.8 deep.
- **Motor bell**: a cylinder of R 10.5 about the axis, x in [-5, 9]; oval vent windows about 4 x 8 on the red end ring.
- **Battery lead**: a polyline from (8, -24, 14.5) to (14, -26, 30) to (25, -30, 45). The plug box is centred at (30, -32, 52), rotated 60 deg about y.

## 17. Each key feature described several independent ways

### Pod width (one pod)
- (a) Pixels: the right pod's front edge is about 460 px at about 7.9 px/mm, giving about 58.
- (b) Ratio: about 1.0 x the disc OD (about 56).
- (c) Ratio: about 2.4 x the pod height (24), giving about 58.
- (d) Rule: the total of 2 pods + slot must be <= 150; with a 24 slot this gives <= 63.
- **Reconciled: 56.**

### Pod depth
- (a) The top-face foreshortening, about 250 px vertical / sin(35 deg), gives about 440 px, about 56-60.
- (b) Fork tine length is about 0.8 x the depth, and the tines measure about 46, giving about 58.
- (c) Ratio: about the same as the width (square-ish plan).
- **Reconciled: 60.**

### Pod height
- (a) Front face about 140 px / cos(35 deg), giving about 170 px, about 22-24.
- (b) Wheel diameter (22) + 2.
- (c) About 0.43 x the disc OD.
- **Reconciled: 23.5 (z -9..14.5).**

### Slot width
- (a) Pixels: the gap between the front faces is about 170 px at the front, about 22.
- (b) It holds a 14 mm motor plus a 6 mm cup, so at least 20 plus clearances.
- (c) About 0.4 x the pod width.
- **Reconciled: 26 between the tub walls.**

### Disc OD
- (a) Ellipse major axis about 430 px at about 7.5 px/mm (farther than the pod front), about 57.
- (b) About 2.3 x the motor diameter (24), about 55.
- (c) Top about 31 above the pod tops plus bottom about 1.5 above the floor, from the axis height: 2R = 46 + 10 = 56.
- **Reconciled: 55 (R 27.5).**

### Disc ID
- (a) Inner ellipse about 0.5 of the outer.
- (b) Black hub (about 21) visible with a gap ring.
- **Reconciled: 29 (R 14.5).**

### Axis height
- (a) Disc top at z = 18 + 27.5 = 45.5. The photo shows the disc top about 30 above the lids (z 14.5): 44.5. Consistent.
- (b) Motor bottom (z 7.5) below the lid top: matches the bell sitting partly in the slot.
- **Reconciled: 18.**

### Fork tip position
- (a) Pixels: the tips are about 40 mm ahead of the front faces.
- (b) Length 46 at a slope of about 12-15 deg gives about 44-45 horizontal from the lug at y 36, so y about 80. The photo suggests 72-75, so the tines may be about 42.
- **Reconciled: tip y 75, length about 40-46 depending on the bend.**

### Wheel position
- (a) The slot centre is about 10 in from the outer side and about 17 from the rear.
- (b) Model: x 61 = 69 - 8; y -12 = -30 + 18.
- **Consistent.**

## 18. Consistency check (conflicts and reconciled values)
1. **Tine slope.** The photo look of 18-22 deg conflicts with the geometry: a 46 mm tine from z -2 dropping to the floor (z -10.5) is only about 11-13 deg. Perspective at 35 deg elevation exaggerates downward slopes. **Use about 12-13 deg** with the tip on the floor.
2. **Lid screw count.** Section 6 counts 4 seen on the right lid and 3 on the left, which conflicts with the usual 4-corner pattern. **Use 4 per lid at the corners** if the build tool needs symmetric bosses (visual difference is small). Otherwise use mid-edge positions: front-middle, outer-middle, rear-inboard, rear-outer.
3. **Joining structure.** Nothing visible joins the pods, yet they must be one rigid frame. **Use the hidden rear beam** (section 13 item 3). It is invisible in aws72 because the motor and disc cover that region.
4. **Disc front reach versus "forks lead".** The disc at y 8 + 27.5 = 35.5 is level with the clevis lugs (y 30..37) but 40 mm behind the tips. This is consistent with the photo, where the disc rim and the lugs are at about the same depth.
5. **Tine orientation.** They look flat-face-up in the photo; the model uses edge-on vertical plates. This conflicts in looks only, not in silhouette at this camera. **Prefer flat-up 5 x 1.5 strips** when the hinge clevis is modelled; edge-on is acceptable for a static bolted version.
6. **Disc hub versus ring ID.** The photo suggests ID 28-30 with a 21 black hub. A real disc would bolt to the bell through a web, which conflicts with a pure ring. **Reconciled**: a disc with a web (hub r <= 17 plus 4 large windows r 17..23) looks like a ring with a dark centre from this camera. It is an acceptable stand-in.
7. **Right lid extension versus rear beam.** The extension (x 1..13, y -30..-8) would overlap the disc sweep if it came forward of y -21.5 at x < -6.5. It does not: it stays at x >= 1, beside the bell, not in the disc plane. **Consistent.**
8. **Height.** Pod height from wheel + 2 = 24 and from pixels = 22-24. **Use 23.5.**

## 19. Why the designer did it (per part)
- **Two separate pods with an open slot.**
  - Fight: the disc sits low and central, so it is hard to reach from the sides, and the pods shield it from side hits.
  - Fight: the open slot lets the disc bite low, close to the floor, without a front bridge getting in the way.
  - Construction: each pod is a small, quick FDM print (about 1 h) that fits any bed, and the two are mirror-identical (one CAD file).
  - Repair: a smashed pod is reprinted alone.
  - Weight: no deck across the front saves about 5-8 g.
- **Separate screwed top plates.**
  - Assembly: the tub is open while you build, so motors, battery and wiring drop in from above. The lid closes it and also clamps the drive motors and battery.
  - Printability: the tub prints open-side-up with no supports; the lid is a flat plate.
  - Repair: 4 screws give access to everything.
  - Fight: a thick top plate takes the disc-on-disc kickback.
- **Right lid rear extension with a concave front.**
  - Construction: it bridges toward the slot to stiffen the right pod, and it carries the battery-lead exit near the switch/link.
  - Fight: the concave arc keeps the plate clear of the motor bell while still covering the gap behind it, so debris and opposing wedges cannot enter the motor area from above-rear.
- **Wheel slots in the lids.**
  - Assembly: the wheel can be fitted or inspected without removing the lid.
  - Weight: removes material.
  - Driving: the tyre tops sit near the lid plane, so the robot can still crawl a little when tipped onto its back **(guess; it is not truly invertible)**.
- **Inboard wheels.**
  - Fight: the wheels are protected by the pod walls (no separate guards needed), so a horizontal spinner cannot strip a tyre.
  - Weight: no outboard brackets.
  - Width: the full 150 mm can go to pod and slot.
- **Direct-drive outrunner, stator on the right, bell carrying the disc.**
  - Construction: no belt, pulleys or idlers. That means fewer parts, lower cost and simpler repair: the motor is one bolt pattern.
  - Weight: the bell is the hub, so there is no separate weapon shaft assembly, bearings or blocks on that side.
  - Fight: the disc's energy is close to the motor's; a short stiff path from the disc to the right pod.
- **Black printed mount cup + plate.**
  - Construction: the cup centres the stator (locating spigot) and the plate spreads the stator screws' load into the pod wall.
  - Printability: the cup is printed axis-vertical so the stator seat is round.
  - Repair: a cracked mount is a 20-minute reprint.
- **Left upright with a bearing.**
  - Fight: it supports the disc end of the shaft, so a hit does not bend the motor shaft (the main killer of direct-drive vertical spinners).
  - Construction: a 683 bearing is cheap and light (0.7 g).
- **Ring disc (large central hole).**
  - Weight: the energy is in the rim; the hole saves about 30 % of the disc mass with only about 10 % less moment of inertia.
  - Fight: 2 teeth give a bigger bite than many teeth.
  - Cost: laser-cut from a sheet.
  - Dark faces: hardened or black-oxide steel resists edge chipping **(guess)**.
- **Hinged steel tines in clevis bars.**
  - Fight: hinged forks always rest on the floor (the ground game), lift opponents into the disc and ride over seams.
  - Fight: narrow tines leave a gap for the disc to reach between the pods.
  - Construction: steel strip is cheap, and the printed clevis bar is a quick print.
  - Repair: a bent tine slides out after removing one pin.
  - Weight: tines about 2 g each.
- **Exposed screws, not counterbored.**
  - Construction: simple prints with no counterbore needed.
  - Repair: a cross-head driver is always in the pit kit.
- **Battery lead / red plug sticking out.**
  - Rules: it acts as the removable power link (a tool-free switch). Pulling the plug kills the power.
  - Construction: no switch pocket is needed.
  - Fight: easy for marshals to reach **(guess)**.
- **Matte black PLA/nylon.**
  - Cost and printability.
  - Looks: it matches the name "Boss Baby" (a suit).

## 20. Unseen and inner parts (guesses with confidence)
Confidence levels: H = high, M = medium, L = low.

| Part | Guess | Size (mm) | Position (frame of section 0) | Confidence |
|---|---|---|---|---|
| Battery | 2S 300-350 mAh LiPo | 48 x 18 x 12 | left pod front half, lying along x, (-41, 13, -1.4) | M |
| Drive ESC + receiver | Malenki-Nano class (receiver + 2 brushed ESC) | 32 x 19 x 2.5 | left pod, on top of the battery, (-41, 13, 6) | M |
| Weapon ESC | BBB 20 A brushless, heat-shrunk | 23 x 12 x 4 | right pod front half, on the floor, (41, 16, -5.4) | M |
| Power link / switch | red JST/XT plug link on the flying lead, OR a slide switch in the rear wall | link: 8 x 6 x 14 | lead exits at (8, -24, 14.5) | M (link) / L (switch) |
| Drive motors | N10/N20 gearmotors, 1000-2200 rpm | 10 x 12 x 30 | (+/-44, -12, 0), shaft outboard | H |
| Motor clamps | printed cradles in each tub plus lid rails pressing down | wall 1.6, up to z 12 | around each gearmotor | M |
| Lid screw bosses | 5.5-6 mm square/round posts, full tub height | 6 x 6 x 19 | under each screw (section 6) | H |
| Ribs | none beyond the cradles and bosses; the tub walls carry the load | - | - | L |
| Weapon shaft | the motor's own 3 mm shaft lengthened to the left bearing (or a 3 mm Ti rod) | 3 dia x 17 | x -14.6..2 at (y 8, z 18) | M |
| Bearing | 683ZZ (3 x 7 x 3) pressed into the left upright | 7 dia x 3 | (-12.5, 8, 18) | M |
| Stator screws | 4 x M2.5/M3 x 8 caps through the right mount plate | - | on a 16 x 16 square about the axis | H |
| Disc screws | 4 x M2.5 x 6 through the disc/hub into the bell face | - | 9-12 mm bolt circle | M |
| Fork pins | M2 x 10 screws or 2 mm pins through each lug | 2 dia x 9 | lugs at x +/-34, +/-46, (y 36, z -2) | M |
| Fork-bar screws | 2 x M2 x 8 per bar into heat-set inserts in the tub front wall | - | bar ends | M |
| Wiring path | battery -> link lead -> right pod (through the rear joining beam) -> weapon ESC -> phases up through the right lid notch to the stator; battery -> drive ESC (left pod) -> left motor directly, right motor via the rear beam | 22-26 AWG | through the hollow rear beam y -28..-23 | M |
| Rear joining beam | hollow printed beam, part of one or both tubs | 29 x 8.5 x 23.5 | (0, -25.75, 2.75) | M |
| Hub on the bell | printed or alloy adaptor ring | 21 dia x 3 | (-5, 8, 18) | M |
