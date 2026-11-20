# Hot Flip: full reference description (rebuild-from-text)

Source photo: `reference/hot_flip.aws71.webp`, 1875 x 1836 px. It is the only reference image: a studio-style photo with the background removed (white). Everything below comes from that one view, plus one user note: "hot flip has a triangular sloping sides design, it is also a wedge lifter so its front panel can lift up".

Confidence marks:
- **[seen]** is directly visible in the photo.
- **[inferred]** follows from geometry or perspective with good confidence.
- **[guess]** cannot be seen, and is the most likely engineering answer for a 150 g UK antweight of this style.

Coordinate convention used in this document (the same as the CAD spec):
- +y is forward (towards the lifting lip) and +x is to the robot's right.
- +z is up, and z = 0 is the wheel axle height.
- "Left" and "right" are as seen by the robot, looking forward.

---

## 1. What the photo shows (view description)

### 1.1 Camera
- The camera looks at the robot from the front-left, from above. [inferred]
  - Its azimuth is roughly 30-40 degrees left of straight ahead.
  - Its elevation is about 35-45 degrees above the floor.
- Perspective is mild: a phone camera at about 30-40 cm. [inferred]
- The robot fills the frame. The front lower edge (the lip) runs along the bottom right of the image, from about pixel (960, 1800) to (1830, 1530).
- The top rear of the robot is at the top of the image, about y_px 50-100.

### 1.2 What is visible
- **The front panel [seen]:** the big light-green plane taking the centre and right of the image. It is the dominant visual element and covers about 45% of the robot's pixels.
- **The top panel [seen]:** the short light-green band at the very top, from about (450, 90) to (1080, 50) along its rear edge and (600, 260) to (1380, 180) along its front edge. It is a flat plane seen almost edge-on from above.
- **The left side assembly [seen]:** all the dark green on the left half of the image. It consists of:
  - a vertical outer side plate;
  - a sloped, triangular chamfer facet between the side plate and the front panel;
  - a lower rear chamfer.
- **The right side [seen, in part]:** a thin dark strip along the right edge of the front panel, from (1380, 180) to (1830, 1530). Here the far side's sloped facet shows just beyond the front panel's right rail.
- **Rails or lips [seen]:** a raised light-green strip, about 12-18 px wide (about 1.5-2 mm), runs along both long edges of the front panel and along the front edge of the top panel.
- **Hinge pin end [seen]:** a small silver cylindrical stub at about pixel (395, 130), at the top-left corner where the side plate, top panel and front panel meet. A matching notch or tab at the top right, about (1075, 50), is probably the other end of the same pin or a hinge knuckle. [inferred]
- **Fasteners on the left side plate [seen]:**
  - a dark round hole or countersunk screw near the top, at about (365, 255), just below the side plate's top edge and about 30 px from its upper corner;
  - one near the bottom, at about (730, 1500), about 1/5 of the side plate's height above its bottom edge and about 1/3 of the way back from its front-lower corner (its socket shows a black hex recess with a silver rim highlight).
- **Not visible [seen as absent]:** wheels, tyres, the floor contact of wheels, electronics, wires, switch, graphics, text, stickers and colour stripes. The robot is a fully closed shell from this viewpoint.

### 1.3 Colours (sampled RGB at given pixels)
| Area | Pixel | RGB | Name |
|---|---|---|---|
| Front panel centre | (1000, 700) | (1, 228, 192) | bright mint / aqua green |
| Front panel right | (1600, 900) | (5, 233, 190) | same mint |
| Top panel | (700, 150) | (2, 236, 180) | mint, slightly yellower (lit from above) |
| Front panel low right | (1550, 1300) | (0, 211, 173) | mint in slight shade |
| Rail at lower right | (1300, 1700) | (64, 160, 141) | rail edge in shade |
| Left side sloped facet | (300, 900) | (5, 74, 83) | dark teal-green (blue-grey sheen from layer lines) |
| Left side plate | (150, 800) | (2, 98, 95) | dark green |
| Left side plate low | (400, 1200) | (0, 61, 61) | very dark bottle green |

- All parts are printed in one filament colour: a mint/teal "emerald" PLA or PETG. [inferred]
- The light and dark difference comes from lighting: the front and top faces face the camera and the light, and the side faces are in shadow. [inferred]
- This matters for the CAD colours: in render the faces facing the light should read light mint (#1fe0b8 to #2fe0b8). The sides could take a darker shade (#0f6a5a) to mimic the photo.
- The layer lines on the left sloped facet run diagonally, at about 30 degrees to the facet's long edge. This shows the facet was printed flat as a separate plate, or at least on a different orientation from the front panel, which shows almost no lines. [inferred]

---

## 2. Overall form and proportions

- Plan outline: close to square, about 100 mm long (y) by 100 mm wide (x) at floor level. [inferred from the front panel width vs the visible side depth]
  - The rear corners are chamfered in plan (a hexagonal plan), seen as the lower rear chamfer facet on the left side. [seen]
  - The front corners are square: the front panel's lower edge runs to the full width. [seen]
- Height: the photo's silhouette height to length ratio, measured by the likeness tool, is 0.98 at its best camera. The real robot is therefore tall for a flipper: the top is about 55-60 mm above the floor. [inferred]
- Side profile, in four sections [inferred]:
  1. The front panel rises from the floor at the front lip, back and up at about 40-45 degrees, to about 0.75-0.8 of the length back.
  2. A short flat top runs about 0.15-0.2 of the length.
  3. A tall rear wall stands almost vertical, about 0.75-0.85 of the full height.
  4. A short chamfer joins the rear wall to the top.
- Front view cross-section [seen + user note]:
  - It is a trapezoid at mid-height and above: the body narrows from full width at the lower vertical side plates to about 0.65-0.7 of the width at the top.
  - The width lost is made up by the triangular sloped facets, one per side.
- Overall impression: a faceted wedge or tent shape, like a cut gem or an old tank turret, with every face flat and every edge crisp.

---

## 3. Parts (each part fully described)

### 3.1 Front panel: P1, the weapon (hinged wedge/lifter plate)
- **Shape [seen]:** a flat plate with a trapezoid outline.
  - The long bottom edge is the lip, about 92-96 mm wide.
  - The shorter top edge is the hinge edge, about 60-68 mm wide.
  - The two slanted side edges join them.
  - The bottom-to-top length measured along the plate is about 85-90 mm. [inferred]
  - The plate is about 2-3 mm thick. [guess, consistent with the rail height]
- **Surface [seen]:** perfectly flat, with no holes, screws, text or graphics. Smooth, with faint vertical streaks: it was printed face down.
- **Lip [seen]:** the bottom edge rests on, or within 1 mm of, the floor along its full width, to scoop under opponents.
  - Its outer corners are square.
  - In the photo the lip's edge shows a small raised bead at about (875, 1460) where the rail meets the lip, which is the rail end. The lip edge itself may have a slight 45-degree chamfer underneath. [guess]
- **Angle [inferred]:** 40-45 degrees from the floor at rest.
- **Rails [seen]:**
  - Along each slanted side edge a raised rib runs the full length, from the lip to the top edge: about 1.5-2 mm wide and about 1.5 mm proud of the panel surface.
  - The rails are the same mint colour, slightly darker in shade.
  - They visually separate the front panel from the side facets.
  - They are either:
    - (a) fixed to the side facets, forming a channel the panel sits in, so the panel lifts out of it; or
    - (b) on the panel's own edges.
  - Most likely (a): there is a visible gap line between the rail and the panel along the right side. [inferred] That means the rails are the edges of the fixed body or side facets, and the panel sits in a recess between them with a running gap of about 0.5-1 mm. [guess]
- **Hinge [seen + user note]:**
  - The top edge of the panel meets the front edge of the top panel along a straight horizontal line, axis x.
  - The silver pin stub at the top left (pixel 395, 130) sits right at this junction on the side. The hinge axis is therefore along this top edge, about 1-2 mm under the top surface.
  - When actuated, the panel rotates about this axis so that its lip rises: a "wedge lifter" or front-hinged-at-top flipper.
  - Range [guess]: 0 to about 60-80 degrees.
- **Actuator [guess, not visible]:** a small geared DC motor (N20 class) or a servo inside the body under the top panel.
  - It is coupled to the panel by a crank or directly on the hinge shaft.
  - It probably sits in the rear upper volume, behind the panel and under the top panel. This is the only place with room above the wheels.
- **Colour:** mint #2fe0b8 (lit). **Material:** printed PLA, PETG or nylon. [guess]

### 3.2 Top panel: P2
- **Shape [seen]:** a flat rectangle-to-trapezoid.
  - Its width equals the front panel's top edge (about 60-68 mm).
  - Its length is about 15-20 mm, front to back.
  - Its plane is horizontal. [inferred]
- **Front edge:** this is the hinge line with P1. A thin rail or lip lies along it, the light line at the top of the front panel from (600, 260) to (1380, 180). The gap between P1 and P2 is about 1 mm.
- **Rear edge:** meets the rear chamfer or rear wall.
  - At the rear left corner, near (450, 90), a small notch is visible.
  - At the rear right corner, near (1075, 50), a small raised tab shows: hinge knuckles or pin bosses. [inferred]
- **Fasteners:** none visible on the top face.
- **Colour:** mint, lit, #2ae8b4. It is fixed to the chassis, probably printed as one piece with the side facets or the body. [guess]

### 3.3 Left side plate: P3 (and its mirror on the right, P3')
- **Shape [seen]:** a vertical flat plate forming the outer left wall. Its outline in side view (looking from the left, front to the right) is a polygon:
  - the bottom edge on the floor line, from the front lip back to the rear chamfer;
  - the rear lower chamfer edge, going up and back;
  - the vertical rear edge, about 0.4-0.5 of the height;
  - an upper edge rising from the rear edge's top towards the top panel's corner. This edge is shared with the sloped facet P4.
- **Thickness [guess]:** 2-3 mm, with a printed surface showing a fine diagonal hatch.
- **Position:** flush with the robot's left extreme at x = -50, between y = about -30 and y = +50.
- **Front edge [seen]:** where P3 meets the front panel's rail, the front edge of P3 follows the panel slope, so P3 is wedge-shaped.
- **Fasteners [seen]:**
  - one round hole or screw near the top front, below the hinge pin, about 6 mm below its top edge;
  - one countersunk or socket screw near the bottom, about 10-12 mm above the floor and about 35-40 mm behind the lip.
  - These screws fix P3 to internal structure (motor mount or floor plate). [guess] The lower screw is the likeliest position for the left drive motor clamp or the axle of the left wheel. [guess]
- **Colour:** dark bottle green in shadow (#06625f to #003d3d).

### 3.4 Left sloped facet: P4 (and its mirror P4')
- **Shape [seen + user note]:** a flat triangular or long-trapezoid plate, leaning inwards at about 30-45 degrees from vertical.
  - Its lower outer edge meets P3's top edge.
  - Its inner edge meets the front panel's rail and the top panel's side.
  - It is widest at the top rear, about 15-20 mm across the slope, and tapers to a point lower down towards the front, where the front panel reaches the full width at the side plate. This is the "triangular sloping side".
- **Surface:** clear diagonal printing lines (the hatch shows a blue-grey sheen).
- **Colour:** dark teal (5, 74, 83).
- **Function:** narrows the body above the side plates to match the narrower top of the trapezoid front panel. It deflects hits and makes the shell gem-like.
- **Joint to P3:** a crisp edge with no visible fastener, so it is printed as one piece with P3 or bonded. [guess]

### 3.5 Lower rear chamfer facet: P5 (each side)
- **Shape [seen]:** a narrow vertical facet at the rear-left corner, going from the side plate's rear edge diagonally back and inwards to the rear wall. This is the clipped rear corner of the hexagonal plan.
- **Size:** about 20-25 mm along the diagonal, in plan.
- **Colour:** dark green, slightly lighter than P3: it faces more towards the light.

### 3.6 Rear wall: P6
- Not visible. [inferred to exist] A vertical wall closes the back between the two rear chamfers.
- Its width is about 0.7 of the overall width (the plan's rear edge) and its height is about 0.8 of the overall height.
- It probably carries the power switch, as most antweights do. [guess]

### 3.7 Hinge pin: P7
- **Seen:** a silver steel stub about 3 mm in diameter, protruding about 1-2 mm from the left side at the top front corner of the side assembly, at (395, 130).
- **Inferred:** the pin runs across the full width along the top edge of the front panel, through knuckles on P1 and bosses on P2/P4. Its ends are retained by e-clips or a press fit.

### 3.8 Drive: wheels and motors (hidden)
- **Wheels [guess]:**
  - Two wheels, one each side, inside the side plates and fully hidden. They protrude below the floor line by 1-2 mm so the shell clears the ground.
  - Likely at the rear half, under the high part of the body, so the front lip stays down. They are invertible only if the shell is symmetric top to bottom; here it is not, so the robot is not invertible.
  - Diameter about 22-25 mm, width 6-8 mm, probably rubber or TPU tyres on printed hubs.
- **Motors [guess]:** two N20-size gearmotors lying across the robot near the rear axle line.
- **Batteries and electronics [guess]:** a 2S LiPo of about 180-300 mAh, a dual brushed ESC (Malenki class) and a receiver, all inside the central cavity under the front panel.

### 3.9 Screws (summary)
- Seen: two on the left side plate (top front, bottom middle). By symmetry, two more on the right side are inferred.
- Seen: hinge pin ends at the top front corners.
- None on the front panel or the top panel.

### 3.10 Wires
- None visible. All internal. [seen as absent]

---

## 4. Part table

| ID | Part | Shape | Approx. size (mm) | Colour | Fixed / moving | Fastening | Confidence |
|---|---|---|---|---|---|---|---|
| P1 | Front panel (weapon) | trapezoid plate | 94 bottom x 64 top x 88 long x 2.5 | mint #2fe0b8 | revolute, axis x at top edge | hinge pin P7 | seen + note |
| P2 | Top panel | flat rectangle | 64 x 18 x 2.5 | mint | fixed | printed with body | seen |
| P3/P3' | Side plates | vertical polygon plate | about 80 long x 40 tall x 2.5 | dark green | fixed | 2 screws each | seen (left) |
| P4/P4' | Sloped facets | triangle, leaning 30-45 deg | 18 wide at top, tapering | dark teal | fixed | printed with P3 | seen + note |
| P5/P5' | Rear corner chamfers | vertical narrow facets | about 22 diag x 40 tall | dark green | fixed | printed with body | seen |
| P6 | Rear wall | vertical plate | about 70 x 45 | not seen | fixed | printed with body | inferred |
| P7 | Hinge pin | steel rod | 3 dia x about 66 | silver | fixed axle | e-clip / press fit | seen (end) |
| P8 | Rails | thin ribs | 1.5 x 1.5 x 88 | mint | fixed | printed with P4 | seen |
| W | Wheels (2) | cylinders | 24 dia x 8 | black (guess) | rotating | on motor shafts | guess |
| M | Drive motors (2) | N20 | 12 x 10 x 25 | metal | fixed | clamp under P3 screws | guess |
| A | Lifter actuator | gearmotor or servo | about 25 x 12 x 10 | n/a | fixed | pocket under P2 | guess |
| E | Battery, ESC, Rx, switch | boxes | standard | n/a | fixed | pockets | guess |

---

## 5. Contact and gap matrix (fixed pose, panel down)

Rows touch columns as described. "-" means not adjacent.

| | P1 front panel | P2 top | P3 side | P4 facet | P5 rear chamfer | P8 rails | floor |
|---|---|---|---|---|---|---|---|
| **P1** | - | top edge, about 1 mm hinge gap | lower part of the side edges: 0.5-1 mm running gap past the rail | side edges, about 0.5-1 mm gap inside the rails | - | rails just outside the panel's edges, panel 1.5 mm below the rail tops | lip at 0-1 mm |
| **P2** | hinge | - | top corners meet P3 at the pin | side edges, sharp edge | rear corners | front rail | - |
| **P3** | via rails | at the pin | - | shared top edge, about 135-150 degree interior angle | shared vertical edge | front edge | bottom edge 1-2 mm above the floor (wheels carry) |
| **P4** | rail | edge | edge | - | upper rear corner | carries rails | - |
| **P5** | - | rear corner | edge | corner | - | - | bottom edge 1-2 mm up |

Gaps:
- P1 to rails: about 0.5-1 mm on each side. [guess]
- P1 hinge edge to P2 front edge: about 1 mm. [seen as a dark line]
- Shell to floor: about 1-2 mm. [inferred from the shadowless bottom edge]
- Lip to floor: 0-0.5 mm. [inferred]

---

## 6. Mechanism

- The front panel P1 pivots on P7 along its top edge, axis x, at about 75-80% of the length back and just under the top surface.
- The actuator A turns P1 so that the lip swings up and forward, lifting any robot that has driven up the wedge. This is a "wedge-lifter".
- At rest P1 lies flush inside the rails and acts as a full-width static wedge.
- The pivot is high, so the lip moves forward and up in an arc about 85 mm in radius. 60 degrees of travel lifts the lip about 75 mm.

---

## 7. Rebuild recipe (CAD)

1. Body. Intersect three extrusions:
   - (a) a side profile polygon extruded along x: floor, front lip at y = +50, slope up to (y = -18, z_top), flat top to y = -40, short chamfer down to the rear wall at y = -50, rear wall down to the floor;
   - (b) a hexagonal plan polygon extruded along z: full 100 mm width from the front back to about y = -25, then chamfered to about 72 mm wide at y = -50;
   - (c) a front-view trapezoid extruded along y: full width from the floor up to about 0.5 of the height, then leaning inwards to about 0.68 of the width at the top.
   Then shell it to a 2.5 mm wall.
2. Recess the sloped front face by the panel's thickness, inside full-length rails about 2 mm wide at each side.
3. Front panel: a trapezoid plate of 94 / 64 x 88 x 2 mm, in that recess. Make it a revolute joint about x at its top edge, range 0-80 degrees.
4. Wheels hidden inside the side plates, at the rear half. Motors across the robot. Battery and ESC in the floor cavity. Actuator under the top panel.
5. Colours: mint #2fe0b8 on the panel and top, darker #1a8a6a or #0f6a5a on the sides. No decals.
6. Screws:
   - an M2 countersunk on each side plate, about 10 mm up and 40 mm behind the lip;
   - one near the top front of each side plate, below the hinge;
   - the hinge pin ends showing at the top corners.

---

## 8. Differences to watch against the CAD

- The front panel must be nearly the full robot width at the lip, and trapezoidal. A narrow inset plate is wrong.
- The sides must lean inwards above the lower side plates. Vertical full-height sides are wrong (user note).
- The rear must be tall: height to length is about 0.95-1.0 in the photo's view. A low rear is wrong.
- No visible wheels from the front three-quarter view. Wheels that stick out of the side plates are wrong.
- No graphics.

---

## 9. Pixel measurements used for the ratios (photo frame)

These are approximate pixel positions in the 1875 x 1836 photo, so others can check the ratios.

- Front panel corners:
  - lower right lip corner: about (1830, 1530);
  - lower left lip corner: about (960, 1800);
  - upper left hinge corner: about (600, 260);
  - upper right hinge corner: about (1380, 180).
- In image space, the lip edge is about 900 px long and the hinge edge about 780 px long.
  - The hinge edge is further from the camera and seen more obliquely, so after correcting for perspective (the far edge is about 1.25x smaller), the real hinge to lip width ratio is about 0.65-0.72.
- Front panel length in the image: (600, 260) to (960, 1800) is about 1580 px, and (1380, 180) to (1830, 1530) is about 1420 px. The panel is long. Projected on the slope, its length is about 0.9 of the lip width.
- Top panel depth in the image: about 170 px at the left and about 130 px at the right, i.e. about 0.11 of the panel's image length. A 45-degree view foreshortens a horizontal surface less than the slope, so the true depth is about 0.18-0.2 of the panel length (about 16-18 mm). [inferred]
- Left side assembly:
  - its silhouette runs from x_px 60 (the rear vertical edge) to the rail at x_px 560-900;
  - the vertical rear edge of the side plate runs from about (60, 580) to (130, 1080), 500 px tall;
  - the lower rear chamfer runs from (130, 1080) to (260, 1400);
  - the floor edge runs from (260, 1400) to (960, 1800).
  These outline a side plate whose rear vertical edge is about 0.45 of the full robot height, with the sloped facet above it.
- The sloped facet's visible boundary with the side plate runs from about (130, 720) to (560, 260). Its top width, along the top panel side, is about 110 px. It narrows to nothing at about (870, 1460), where the rail meets the lip corner. This is the triangular shape the user describes.
- Screw positions: lower screw (730, 1500), about 140 px above the floor edge; upper hole (365, 255); hinge pin (395, 130).

## 10. Symmetry

- The robot is mirror-symmetric about its centre plane (x = 0): the right-side rail, facet and rear tab match the left. [inferred]
- Build one side and mirror it.
- The only asymmetric internal items are likely the actuator and switch. [guess]

## 11. What makes it look like Hot Flip (priority order for likeness)

1. A big, flat, full-width trapezoidal front plate, rising to a high hinge.
2. Inward-leaning triangular facets above vertical side plates.
3. Tall rear with chamfered rear corners: a gem-like or tank-turret block.
4. Two-tone mint (lit faces) and dark green (shaded faces), with no other colours.
5. Thin rails framing the front plate.
6. Hidden wheels: nothing round visible from the front three-quarter view.

---

## 12. Coordinate frame (used by every number below)

- The origin is at the robot's centre in plan (x = 0, y = 0).
- z = 0 is the wheel axle height. The floor is at z = -9 to -11, because the wheels are about 22-24 mm in diameter. [guess]
- +y points forward (towards the lip), +x to the robot's right, +z up.
- Angles are in degrees:
  - pitch about x, measured from the floor (horizontal);
  - lean measured from vertical.

## 13. Every part in all dimensions (mm, with guesses marked)

| Part | L (y) | W (x) | H (z) | Thickness | Radii | Angles | Key coordinates |
|---|---|---|---|---|---|---|---|
| P1 front panel | 88 along slope (62 in plan) | 94 at the lip, 64 at the hinge | 58 rise | 2.0-2.5 | corner radius about 0.5 (sharp print) | pitch 42 +- 4 at rest; lift range 0-80 | lip edge y = +50, z = -9; hinge edge y = -18, z = +49 |
| P2 top panel | 18-22 | 64-68 | - | 2.5 | none | 0 (flat) | y = -18 to -40, z = +49 |
| P3 side plate | 100 at the floor | - (plane at x = +-50) | 22-25 vertical part | 2.5 | none | 0 lean (vertical) | x = +-50, z = -9 to about +16 |
| P4 sloped facet | 88 along the front edge (triangle) | 15-18 across the slope at the top | 33 | 2.5 | none | lean 30 +- 8 from vertical | from (x = +-50, z = +16) to (x = +-34, z = +49) |
| P5 rear chamfer | 20-25 diagonal | - | 40-55 | 2.5 | none | 45 in plan | from (x = +-50, y = -25) to (x = +-36, y = -50) |
| P6 rear wall | - | 72 | 55 | 2.5 | none | vertical | y = -50 |
| P7 hinge pin | - | 66-70 | - | dia 3 | r 1.5 | axis x | y = -18, z = +47.5 |
| P8 rails | 88 | 1.5-2 | 1.5 proud | - | none | follow P1 | along the P1 side edges |
| Wheels (hidden) | - | 8 | - | - | r 11-12 | - | x = +-45, y = -30, z = 0 [guess] |

## 14. Curves

- There are no curved surfaces visible. Every face is planar and every edge a straight line segment. [seen]
- Edge lines in the side view (x = const plane), with y in mm and z in mm:
  - P1 top surface: z = -9 + (50 - y) * tan(42 deg) = -9 + 0.90 * (50 - y), for y in [-18, 50].
  - P2: z = 49, for y in [-40, -18].
  - Rear chamfer: runs from (y = -40, z = 49) to (y = -50, z = 44), slope 0.5, so z = 49 + 0.5 * (y + 40) for y in [-50, -40].
  - Rear wall: y = -50, z in [-9, 44].
- Front-view lean of the side (y = const plane): half-width h(z) = 50 for z <= 16, and h(z) = 50 - 16 * (z - 16) / 33 for z in [16, 49].
- Plan outline: |x| <= 50 for y >= -25, and |x| <= 50 - 14 * (-25 - y) / 25 for y in [-50, -25].
- The P1 panel half-width along its slope: w(s) = 47 - 15 * s / 88, where s is the distance from the lip along the slope, in [0, 88].

## 15. Each dimension measured several independent ways

| Quantity | (a) Photo pixels | (b) Ratio to another part | (c) Engineering / limit | (d) CAD coordinate | Reconciled |
|---|---|---|---|---|---|
| Overall width | lip 900 px vs panel length 1580 px | the lip is about 1.05 x the panel's plan length | an antweight must fit a 150 mm box, typical 100 | x = +-50 | 100 |
| Hinge width | 780 px (far edge, about 1.25x foreshortened, gives 975 px equivalent) | 0.65-0.72 x the lip | must clear the 20 mm actuator either side of the centre | +-32 to +-34 | 66 |
| Height | the silhouette height / length is 0.98 in the likeness camera | the rear wall is about 0.8 of the height | the wheel diameter is 22-24, so z_floor = -9 to -11 | z from -9 to 49 | 58 |
| Panel pitch | the panel image length vs the lip, with the top foreshortening | the rise of 58 over a plan run of 62 to 68 | flippers are typically 35-45 degrees | 42 | 42 |
| Top panel depth | 130-170 px vs 1420-1580 px for the panel | 0.18-0.2 x the panel | room for a hinge plus the actuator, at least 18 | y -18 to -40 | 20 |
| Side-plate vertical height | rear edge 500 px of a total height of about 1100 px, so 0.45 | about 0.4-0.5 of the height | must clear the drive motors (box to z = +5) plus a 2.5 mm wall | z -9 to 16 | 25 (z0 = 16 to 22) |
| Facet lean | facet image width 110 px at the top vs the side plate's 500 px rear edge | top width 0.68 x the lip | the actuator at x = -26 must stay inside the facet | 16 inward over 27-33 rise | 27-30 degrees |

## 16. Consistency check

1. **Top width ratio.**
   - The photo ratio gives 0.65-0.72.
   - The user note "triangular sloping sides" suggests a strong lean.
   - The likeness check dropped to 0.75-0.77 when the top width was 0.6 (lean starting at z = 10). It recovered to 0.80-0.81 at 0.68 with the lean starting at z = 22.
   - Reconciled: top half-width 34, lean starting at z = 22.
2. **Height.**
   - Pixel estimates suggested about 55. The likeness gives a height-to-length ratio of 0.98.
   - A taller rear (rear wall to z = 46, chamfer to the top at y = -44) matches 0.99.
   - Reconciled: a tall rear wall at z = 46, with the top at 49.
3. **Where the hinge is.**
   - The pin end is seen at the top front corner, so the hinge is at the panel's top edge.
   - Engineering says a top hinge makes a "lifter" whose lip rises, which agrees with the user's note.
   - No conflict.
4. **Rails.**
   - In the photo they could belong to either the panel or the body.
   - The gap line is visible on the outer side of the rail, which suggests the body.
   - Reconciled: the rails are on the body and the panel sits in a recess.
   - In CAD: the panel recess sits inside a 4 mm side margin at the lip, widening to about 3 mm at the top.
5. **Wheels.**
   - None are seen.
   - The CAD has wheels at x = +-45.5, partly outside the rear chamfer in plan, so they show slightly in the iso_back render.
   - Accepted: the photo camera does not see the rear corners.

---

## 17. Why the designer did it (per part, from several angles)

### P1 front panel (hinged wedge-lifter)

**Fight**
- The full-width lip on the floor gets under opponents from any approach angle.
- The 40-45 degree slope turns rams into lift.
- The top hinge lets the actuator raise the lip and tip the opponent onto its back or side, or at least take the weight off its wheels.
- A wide, flat face gives no edges for spinners to catch. Hits glance off.

**Construction**
- A flat plate prints face-down with a perfect surface and no supports.
- It is replaceable on its own (pull the hinge pin).
- It is thin (2 mm), so it is light (about 10-12 g).
- The trapezoid follows the body's narrowing top, so the hinge edge needs no overhangs.

**Other**
- Because the panel is the whole front, the robot looks "all weapon", a deliberate aesthetic of a clean gem.

### P2 top panel

**Fight**
- Shields the hinge and actuator from hits from above (hammers, overhead flippers).

**Construction**
- Carries the hinge bosses.
- Closes the body over the actuator pocket.
- It is printed with the body, so there is no extra assembly.

### P3 vertical side plates

**Fight**
- Vertical lower walls stop pushers getting under the side, since the wheels are hidden behind them.
- They protect the wheels from horizontal spinners.

**Construction**
- They give a flat face for screws into the internal motor mounts: the two seen screws are the motor clamp or the axle support.
- They print flat, and are easy to replace.

### P4 triangular sloped facets

**Fight**
- Inward-leaning upper sides deflect hits upwards and away. They reduce the target profile from the front-side, and give no vertical face for spinner teeth to bite.
- If the robot is pushed onto its side, the slope helps it roll back.

**Construction**
- They narrow the body only where the internals allow it: above the drive motors (z > 16-22), where only the actuator and wires live.
- This saves material (less top area), so it saves weight.
- They are printable without supports, since 30 degrees from vertical is under the 45-degree overhang limit.

**Other**
- The signature look: the "triangular sloping sides" the builder wanted.

### P5 rear corner chamfers

**Fight**
- Remove the corners an opponent's wedge can hook. Present glancing faces to rear attacks.

**Construction**
- They save about 2 x 0.5 x 14 x 25 mm of footprint and material. They give clearance for the rear of the wheels to sit inside, or nearly inside, the outline.

### P6 tall rear wall

**Fight**
- A tall rear means that, when flipped upside down, the robot rests on its rear edge and top. That is not invertible, but it gives a self-righting lever: the lifter, pushing on the floor, can rotate it back over.

**Construction**
- Hosts the power switch and the charging access.
- Gives internal height for the actuator above the drive motors.

### P7 hinge pin

**Fight**
- A steel pin survives impacts better than a printed one.

**Construction**
- Removable for maintenance. A 3 mm rod is cheap and standard.

### P8 rails

**Fight**
- Protect the panel's side edges from being caught. Keep debris out of the gap.

**Construction**
- Hide the running gap and the panel's edge imperfections.
- They also act as alignment guides when the panel closes.

### Hidden wheels

**Fight**
- The wheels are invisible and unreachable. Nothing to snag, and wedges cannot drive onto them.

**Construction**
- Needs small wheels (22-24 mm), with the motors close to the floor.

## 18. Unseen and inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (x, y, z) | Confidence | Reason |
|---|---|---|---|---|---|
| Battery | 2S LiPo, 180-300 mAh | 45 x 17 x 10 | (0, 0, -2), flat on the floor in the centre | medium | the largest flat free volume, under the panel; keeps the CoM low and central |
| ESC | dual brushed plus mixing (Malenki nano or similar) | 30 x 17 x 3 | (0, 0, 20), on a shelf above the battery | medium | short wires to both motors and the actuator |
| Receiver | built into the Malenki, or a 4-channel micro Rx | 20 x 12 x 5 | next to the ESC | low | |
| Power switch | slide switch or removable link | 12 x 4 x 6 | rear wall, centre, z about -4 (or the floor at y = -15) | medium | AWS rules need an accessible switch; the rear is protected |
| Drive motors (2) | N20 gearmotors, 50:1 to 100:1 | 10 x 12 x 25 (+ shaft 9) | (+-26, -30, 0), lying across, the shafts outward to the wheels | medium-high | the wheels must be at the rear under the high part, so the lip can touch the floor |
| Wheels (2) | 22-24 mm printed hub + TPU or silicone tyre | dia 22-24 x 8 | (+-45, -30, 0) | medium | must sit inside the side plates, which are 100 wide |
| Motor mounts | printed clamp blocks fused to the floor, with M2 screws through the side plates | 14 x 14 x 26 | around each motor | medium | the side screw seen at about (-50, -30... -10, about +2) lines up |
| Lifter actuator | N20 or N10 high-torque gearmotor (300 rpm 6 V) or a micro servo with a crank | 24 x 12 x 10 | (about -14, -25, +41), across the body under the top panel | medium | the only free volume near the hinge |
| Actuator coupling | a gear or crank on the hinge shaft; or the motor shaft directly as the hinge pin, with a D-flat | - | the hinge axis y = -18, z = +47 | low | |
| Hinge knuckles | 3-4 printed knuckles alternating between the panel and the body | about 8 long x 6 dia each | along the hinge line | medium | |
| Internal ribs | a floor ribbed lengthwise (2 x 1.2 mm ribs) | - | the floor | low | strength against flipping loads |
| Wires | battery to switch to ESC, ESC to the 2 drive motors, ESC to the actuator | 22-26 AWG | along the floor and up the left side to the actuator | medium | |
| Bearings | none (antweight): the motor shafts carry the wheels directly | - | - | high | |
| Hidden screws | M2 x 6-8: 2 per side plate (seen), 2-4 under the top panel (guess) | - | - | medium | |
