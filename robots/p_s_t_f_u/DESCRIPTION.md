# P.S.T.F.U.: full rebuild description from the reference photo

Source photo (AWS fan wiki `File:P.S.T.F.U..aws69.jpg`, stored as `robots/p_s_t_f_u/reference/p.s.t.f.u..aws69.webp`, 1808 × 1196 px):
- AWS 69. The robot is cut out onto white. The camera is at the **front-left three-quarter**, about 30–35° down (the user's camera pick is azimuth 120°, elevation 35°; the likeness gate still judges at 45°).
- Visible:
  - the whole **front wedge**: its sloped face with three screws, the lower bevel band, the robot's left end face, and the right end in the distance;
  - the **left yellow side rail** along its full length;
  - the **right yellow rail**, only at its front end and rear corner;
  - the **taped deck plates** with their screws;
  - **four black wheels**, seen through the gaps;
  - blue and black parts inside.

There is only one photo, so every hidden face is a guess. Everything stated as fact below is read from that photo. Anything inferred is marked **(guess)**, with a confidence tag where it matters. Dimensions in mm are **estimates**, scaled from the current spec: chassis 112 mm wide × 80 mm long × 20 mm tall, wheels Ø 22 inside the body, rails 4 mm wide. The proportions match the photo (see §11–12). Ratios are given against **W = chassis width ≈ 112 mm**.

---

## 0. Coordinate system and naming

- **+X** = the robot's right, **+Y** = forward (toward the wedge), **+Z** = up. Units are mm.
- **Origin O** = the floor point (z = 0) under the centre of the chassis footprint. The spec uses the wheel axle as z = 0 (wheel radius 11), so model z = floor z − 11.
- In the photo the wedge runs from the upper-left (the robot's **right** end) to the lower-right (the robot's **left** end). The robot faces the image's lower-left, and the side nearest the camera (bottom-right of the image, the long yellow rail with two black wheels) is the robot's **left** side. The rear edge is the top-right of the image.

| ID | Part |
|---|---|
| CH | chassis tub (yellow/amber printed; seen only as the rails and the rear corners) |
| RL-L / RL-R | yellow side rails (the tops of the tub side walls; rounded top edge) |
| WD | front wedge: aluminium, sloped face + lower bevel + end faces |
| WF | wedge main face (sloped, with 3 screws) |
| WB | wedge lower bevel band (steeper, along the floor edge) |
| WE-L / WE-R | wedge end faces (closed, chamfered) |
| WS-1..3 | wedge face screws (pan head, six-lobe/Torx-Plus recess) |
| WT | clear tape patches on the wedge face (rectangular outline) |
| DK | deck: white-taped plates on top, at several heights |
| DP-1 | right-front deck plate (rectangular, 2 screws) |
| DP-2 | right/rear plate with a rounded lobe and 1 raised screw (hatch) |
| DP-3 | centre sloped plate (from the wedge top up to the centre ridge, torn tape) |
| DP-4 | left-rear deck plate (rectangular, 3 screws) |
| DP-5 | left-front corner plate / tape strip by the wedge's left end |
| DS | deck screws (pan heads, same type as WS) |
| WH-FL, WH-RL, WH-FR, WH-RR | four black wheels inside the tub |
| M-x | four N20-class drive gearmotors (hidden, guess) |
| BLU | blue part inside (ESC heat-shrink or battery wrap) |
| BAT, RX, SW | battery, receiver, switch (hidden, guess) |

---

## 1. Overall description in one paragraph

P.S.T.F.U. is a **low, wide, four-wheel box wedge** ("pusher") with a **heavy-looking metal wedge** across the whole front. The body is a **flat rectangular tub** about 112 mm wide, 80 mm long and 20 mm tall, printed in **yellow/amber** filament. Only its **rounded top edges (the yellow "rails")** show along both sides and at the rear corners. The four **black wheels** sit inside the tub in wheel wells, two per side, and peep out through gaps in the deck. The top is covered by **several flat plates wrapped in white tape** (duct/gaffer tape, scuffed and torn). They sit at slightly different heights, overlap like shingles, and are held by **pan-head screws with six-lobe recesses**. The front is a **full-width aluminium wedge**, about 116 mm wide. It is a sloped face about 25 mm tall, bent or machined into a **closed triangular section**, with a steeper **bevel band** along the floor and **chamfered, closed end faces**. Three large pan-head screws fix it through its face. Patches of clear tape outline areas of the face. The overall look is a **matt grey slab of metal in front of a white-and-yellow box**. No weapon other than the wedge is visible.

---

## 2. Part-by-part description

### 2.1 Chassis tub (CH)
- **Shape**: a shallow rectangular box, about **112 mm wide (W) × 80 mm long (0.71 W) × 20 mm tall** (floor z 2 to 22), with the wedge ahead of it. The plan corners are square with a small external radius (~2 mm). The rear corners are visible as yellow rounded ends in the top-left and top-right of the photo.
- **Material/colour**: **yellow-amber**, slightly translucent, glossy. Probably PETG or nylon with a yellow tint **(guess)**. The fine scratches and the rounded edges look like a **printed** part.
- **Walls**: the side walls are about **3–4 mm** thick, with a **fully rounded top edge** (r ≈ 2 mm). This is the "yellow rail" the user sees on both sides. The rear wall is presumably the same **(guess)**.
- **Wheel wells**: openings in the deck at the four corners (the tyres show as black arcs between the deck plates and the rails). Each well is about 26 × 12 mm in plan.
- **Floor**: never seen. Probably a printed 2 mm floor with motor pockets **(guess)**.

### 2.2 Side rails (RL-L, RL-R): "the yellow things on both the sides"
- **What they are**: the visible **tops of the tub's side walls**, about **4 mm wide** (X) and standing **2–4 mm above** the deck plates' outer edges. They run the **full length** of the tub, from the wedge's back face to the rear wall.
- **Shape**: a bar with a rounded (half-round) top, roughly a 4 × 6 mm section above the deck line. It continues down as the wall (hidden).
- **Left rail (near the camera)**: from the wedge's left end (image ≈ (1440, 780)) to the left-rear corner (≈ (1725, 430)). Its outer face is visible as a bright yellow strip about 30 px tall, with two black wheel arcs showing inside it.
- **Right rail (far)**: a short yellow strip by the wedge's right end (≈ (300–400, 240–290)) and the right-rear corner (≈ (600, 90)).
- **Height**: the rail top is about **z 18–20**. Its outer face is flush with the wedge's end faces in X (rail outer face at x ≈ ±58–60). The wedge's end faces line up with the rails **(medium)**.
- **Earlier model error**: the yellow rail was modelled on one side only. **Both sides have it** (user note).

### 2.3 Front wedge (WD): "it's actually a wedge, like a metallic wedge"
- **Overall**: an **aluminium** part spanning the full front, about **116 mm wide** (end face to end face, slightly wider than the tub, flush with the rail outer faces). It has a matt, brushed-grey look, with scratches, black scuffs and white tape residue. It is **not a thin scoop or fork**: it reads as a **solid triangular block**.
- **Main face (WF)**: a flat plane sloping up from the bevel band to the top edge. Its slant height is about **24–26 mm** and its angle is about **50–55°** to the floor (the face foreshortens strongly in the photo, even though the camera is above it). The top edge is a sharp, straight line at about **z 20–22**, at or slightly above the deck plates' front edges. Behind the top edge there is a **narrow flat top** (about 3–4 mm) meeting the deck **(medium)**.
- **Lower bevel (WB)**: a **second, steeper facet** along the bottom, about **8–10 mm** tall (slant), angled at about **65–75°**. It meets the main face at a visible crease. The bottom edge sits on or just above the floor. In the photo it is the lower band, slightly darker, with a clear-tape strip along part of it.
- **End faces (WE-L, WE-R)**: **closed, flat faces** perpendicular to X. The left end face is clearly visible at the lower-right of the wedge (image ≈ (1230–1445, 785–1085)). Its outline is a **pentagon**: back edge vertical (against the rail/tub front), top edge short, the main-face edge, the bevel edge, and the floor edge. The **outer corners are chamfered**: the corner where the main face, bevel and end face meet is cut at about 45°, about 5–8 mm. That is why the right end looks clipped in plan.
- **Section (YZ, constant across X)** (see §10.1): back face vertical, about 22 mm tall; floor depth about 22–24 mm; main face at 52°; bevel at 70°.
- **How it is made**: a solid aluminium bar of this section would weigh about 60–80 g, half the robot. So it is almost certainly **folded aluminium sheet (1.5–2 mm)** bent into a closed triangle (face + bevel + back/bottom), with the **ends closed** by folded tabs or separate end plates **(medium)**. An alternative is a **printed core clad in an aluminium face** with aluminium end caps **(low)**.
- **Screws (WS-1..3)**: three **pan-head screws with a six-lobe (Torx/Torx-Plus) recess**, head Ø about **6–7 mm** (M3–M3.5). They sit along a line about **40%** of the slant up the main face, at x ≈ −40 (robot's right end … near the right third), 0 and +40 (by eye: image (410, 440), (645, 640), (975, 680)). The heads stand proud about 2 mm (they are not countersunk). They go through the face into the tub's front wall or a printed nose block **(guess)**.
- **Tape (WT)**: two **clear packing-tape patches**:
  - a long rectangle on the right half of the face (outlined by a thin lighter line, about 60 × 15 mm);
  - a strip along the lower bevel at the left.

  The tape makes the face slick and covers scratches.

### 2.4 Deck plates (DK, DP-1..5): "taped deck plates"
- **What they are**: flat plates (probably 1–1.5 mm aluminium or thin printed plates **(guess)**) **wrapped in white tape** (duct/gaffer tape with a cloth weave, scuffed grey). They sit at **different heights**, overlap, and leave **gaps** through which the wheels and the inside show.
- **DP-1, right-front plate**: a rectangle about **50 × 25 mm** at the robot's right-front, just behind the wedge's right half. It has **2 screws** at its outer corners (image ≈ (500, 165) and (790, 135) for the far one, (255, 305) for the near one). It is raised about **1–2 mm** above the next plate.
- **DP-2, rear/right plate with a lobe**: a long plate along the rear right, with a **rounded lobe** (a D-shaped tab about 20 mm across) in the middle, carrying **1 raised screw** (≈ (1085, 215)). The lobe stands about **3–4 mm** proud, so it is a separate hatch or the cover over the switch/battery **(guess)**. The plate's edge shows a gap with a black part (wheel) below.
- **DP-3, centre sloped plate**: a white-taped panel that rises from the wedge's top edge toward the centre at about 10–15°, forming a low **ridge** across the middle. The tape is **torn** at its left end (≈ (1130–1230, 380–450)), exposing a black wire bundle and a **blue** part (heat-shrink or battery). It has **1 screw** near its right end (≈ (555, 305)).
- **DP-4, left-rear plate**: a rectangle about **45 × 35 mm** at the left-rear quadrant, with **3 screws**: one at the inner-front corner (≈ (1205, 570)), one at the outer-rear corner (≈ (1405, 370)), one at the outer-front corner (≈ (1515, 560)). It sits about 1–2 mm below the centre ridge.
- **DP-5, left-front strip**: a narrow white strip between the wedge's left end and DP-4, partly over the left-front wheel well.
- **Deck height**: the deck plates are at **z ≈ 20–24** (floor z). The ridge of DP-3 is the highest point, at about z 24–25, a little above the wedge top edge.
- **Gaps**: between the plates, 2–6 mm wide, showing:
  - the black tyres of all four wheels;
  - black wiring;
  - a **blue** component (ESC heat-shrink or battery label) under the torn tape of DP-3.

### 2.5 Wheels (WH-FL, WH-RL, WH-FR, WH-RR)
- **Size**: about **Ø 22 mm × 8–10 mm wide**. They are matt black rubber (or black TPU / foam), with a slightly rounded tread edge.
- **Positions**: inside the tub, in the four corner wells. Centres at about **x ±51.5**, **y −26 and +18** (spec). The front wheels sit right behind the wedge's back face; the rear wheels sit near the rear corners.
- **Visibility**: only their **tops** show, through the deck gaps and above the rails (the left-front tyre at image ≈ (1200–1360, 620–700); the left-rear at ≈ (1480–1650, 340–470); the right ones at ≈ (350–520, 270–330) and (680–800, 50–120)).
- **Height**: the tyres stick up to about the deck plate height (z ≈ 22), so the robot is **close to invertible** **(guess)**: inverted, it would rest on the deck and the wheel tops.

### 2.6 Drive motors (M-x), hidden
- **Guess**: four **N20 600 rpm gearmotors** (`bbb_n20_600rpm` in the spec), one per wheel, lying across the tub with their shafts out through the side walls into the wheel hubs (x ±32.85, y −26 and +18, axle z 11) **(medium)**. Four-wheel drive suits a pusher.

### 2.7 Electronics
- **Blue part**: under the torn tape of DP-3, at the centre-left. It could be a **blue heat-shrink** around an ESC or receiver, or the **battery label** **(low)**.
- **Battery**: 2S 180–300 mAh LiPo at the centre, under DP-3 **(medium)**.
- **RX/ESC**: a Malenki-type combined board **(guess)**, under DP-1 or DP-2.
- **Switch**: possibly under the DP-2 lobe (a removable link reached by taking off the hatch screw) **(low)**.
- **Wiring**: a black wire bundle shows at the tape tear. No external wiring.

### 2.8 Screws (WS, DS)
- All visible screws are the **same type**: **pan head, six-lobe recess**, zinc/silver, head Ø 5–7 mm.
  - Wedge: 3 screws (bigger, about 7 mm heads).
  - Deck: about **7 visible** (DP-1 ×2, DP-2 ×1, DP-3 ×1, DP-4 ×3), about 5–6 mm heads (M2.5–M3).
- They likely thread into **printed bosses** in the tub, or into heat-set inserts **(guess)**.

---

## 3. Per-view descriptions (for silhouette matching)

### 3.1 Top view (plan; synthesised)
- The outline is a **rectangle about 120 × 80** (tub with rails), plus the wedge strip, **116 × 22–24**, across the front. Total length about **104 mm**. The front corners are chamfered in plan (the wedge end chamfers).
- Inside: the rail strips (4 mm) along both long sides, black wheel crescents at the four corners, and the white deck plates in a patchwork (DP-1 right-front, DP-2 right-rear with a D-lobe, DP-3 centre band, DP-4 left-rear, DP-5 left-front strip). About 7 screw dots on the deck and 3 on the wedge.

### 3.2 Front view
- A wide, low rectangle: the wedge face, 116 wide × 22 tall, with the bevel band along the bottom and 3 screws. Above it, just visible: the deck plates' front edges and the DP-3 ridge. At the extreme sides, the wedge end chamfers. The wheels are hidden behind the wedge.

### 3.3 Left side view
- A low profile: the wedge's triangular/pentagonal end face at the front (22 deep × 22 tall). Behind it, the yellow rail/wall (80 long × 20 tall) with two black wheel arcs (Ø 22) visible through or below it. The white deck edge runs on top, and the DP-3 ridge peaks in the middle.

### 3.4 Rear view (not photographed)
- The yellow rear wall (120 × 20) with rounded corners, the deck plates on top, and the DP-2 lobe. Probably a switch or link **(guess)**.

### 3.5 Isometric (front-left-top, as AWS 69)
- The grey metal wedge dominates the lower-left half of the silhouette. The white patchwork deck fills the top. The yellow rail edges frame the right/lower-right side and the far corners. The black tyres peep out at the corners.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| CH | shallow tub | 112 × 80 × 20 | 1 × 0.71 × 0.18 | yellow-amber FDM | — | 1 |
| RL | rounded wall top | 4 × 80 × (2–4 above the deck) | 0.04 × 0.71 | yellow | integral | 2 |
| WD | closed triangular wedge | 116 × 23 × 22 | 1.04 × 0.21 × 0.20 | aluminium | 3 × M3 pan Torx | 1 |
| WF | main face | 116 × 25 slant, 52° | — | aluminium | — | 1 |
| WB | bevel band | 116 × 9 slant, 70° | — | aluminium | — | 1 |
| WE | end face (pentagon, chamfered) | 23 × 22 | — | aluminium | folded/closed | 2 |
| WT | tape patch | ~60 × 15 | — | clear tape | stuck | 2 |
| DP-1 | plate | 50 × 25 × 1.5 | 0.45 × 0.22 | white-taped | 2 screws | 1 |
| DP-2 | plate + D-lobe hatch | 60 × 20 (+ lobe Ø 20) | 0.54 × 0.18 | white-taped | 1 screw on the lobe + hidden | 1 |
| DP-3 | sloped plate, ridge | 90 × 25 | 0.80 × 0.22 | white-taped (torn) | 1 screw | 1 |
| DP-4 | plate | 45 × 35 × 1.5 | 0.40 × 0.31 | white-taped | 3 screws | 1 |
| DP-5 | strip | 30 × 10 | — | white tape | — | 1 |
| WH | wheel | Ø 22 × 8 | 0.20 × 0.07 | black rubber | N20 D-shaft | 4 |
| M | N20 gearmotor | 12 × 10 × 32 | — | metal | printed pocket | 4 |
| WS | pan Torx screw | head Ø 7 | 0.06 | zinc | wedge to tub | 3 |
| DS | pan Torx screw | head Ø 5.5 | 0.05 | zinc | deck to tub | ~7 |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| WD back face ↔ CH front wall | bolted (WS through WF) | 0 |
| WD bottom edge ↔ floor | lip | 0.5–1 |
| WD end faces ↔ RL outer faces | flush in X | 0 (±1) |
| WD top edge ↔ DP-1/DP-3 front edges | butt or tuck under | 0–1 |
| DP plates ↔ CH wall tops / bosses | screwed | 0 |
| DP plates ↔ each other | overlap/step | 1–4 height steps, 2–6 plan gaps |
| RL top ↔ DP outer edges | rail stands proud | +2 to +4 |
| WH tyre ↔ well edges / deck plates | running clearance | 1–2 |
| WH top ↔ deck plane | about level | 0 to −2 |
| WH bottom ↔ floor | contact | 0 |
| CH floor ↔ floor | clearance | ~2 |
| front wheels ↔ WD back face | close behind | 2–4 |
| M ↔ CH pockets | captured | 0.25 |

---

## 6. Mechanism
- **Drive**: 4WD skid steer on four inboard wheels. With no active weapon, it is a **pusher/wedge**: it gets under opponents with the metal wedge and drives them into the walls or out of the arena.
- **Wedge**: fixed. It is heavy and stiff, and does not flex or hinge. The bevel band gives a sharper, lower entry edge than the 52° main face alone.
- **Inverted**: it can probably drive upside down (the wheels reach about the deck height), but the wedge would then point up. So inverted it is a box with an overhang **(guess)**.

---

## 7. Assembly order (suggested rebuild)
1. Print the tub CH with wheel wells, motor pockets and screw bosses for the deck and the wedge.
2. Fit 4 N20 gearmotors and press on the wheels.
3. Fit the battery, ESC/RX and switch, and route the wires.
4. Fold the aluminium wedge (face + bevel + back/bottom flange; close the ends), drill 3 holes, and bolt it to the tub front with 3 pan-head screws.
5. Cut the deck plates, wrap them in white tape, and screw them down (about 7 screws), overlapping as in the photo.
6. Apply clear tape to the wedge face.

---

## 8. Hidden / uncertain list
- The wedge's internal construction (folded sheet vs solid vs clad core) and the back face/flange.
- Deck plate material (aluminium vs printed vs card), exact outlines and heights.
- Battery/ESC/switch locations; the purpose of the DP-2 lobe.
- Floor and rear wall.
- Whether the wheels stick out above the deck (invertibility).
- All dimensions ±15%; the right-hand (far) details are low confidence.

---

## 9. Coordinate frame (restated)
- O = the floor point under the tub centre. +X right, +Y forward, +Z up, mm. Model z = floor z − 11.
- Tub: x ∈ [−56, +56] (rails to ±60), y ∈ [−40, +40], z ∈ [2, 22]. Wedge: y ∈ [+40, +63], z ∈ [0.5, 22], x ∈ [−58, +58].

## 10. Profiles as math

**10.1 Wedge section (YZ, constant for |x| ≤ 50; chamfered beyond).** Vertices (y, z), counter-clockwise from the back-bottom:
- B0 = (40.0, 1.0): back face bottom (on the tub front wall, just above the floor).
- F0 = (62.0, 1.0): front bottom edge (the lip); it rests about 0.5–1 mm off the floor.
- F1 = (59.0, 9.2): top of the bevel band. The bevel is the line from F0 to F1, angle atan(8.2/3.0) = 70°.
- T0 = (44.0, 21.5): top edge. The main face is the line from F1 to T0, z = 9.2 + (59 − y)·tan 39.4° … i.e. slope atan(12.3/15) = **39°** from the floor.
- B1 = (40.0, 21.5): back top. The top flat is the line from T0 to B1, 4 mm wide.

Main face angle reconciliation: the photo suggests 50–55°, but the photo is taken from above, which steepens a slope's apparent angle. Using the visible slant ratio (main face 290 px against the end-face depth 200 px at about 12 px/mm → 24 mm slant over 16–18 mm depth) gives atan(√(24² − 17²)/17) ≈ 45°. **Reconciled: main face 45°** with T0 = (44, 21.5), F1 = (56.3, 9.2). The bevel is then from F1 = (56.3, 9.2) to F0 = (59.3, 1.0).

**10.2 Wedge plan with end chamfers (XY at z = 1).** A rectangle x ∈ [−58, 58], y ∈ [40, 59.3], with the two front corners cut by lines from (±58, 52) to (±51, 59.3) (a 7 mm chamfer at 45°).

**10.3 Wedge as folded sheet (rebuild option).** Sheet thickness t = 1.5:
- face panel F1→T0, 17.4 mm;
- bevel panel F0→F1, 8.7 mm;
- top flange T0→B1, 4 mm;
- back flange B1→B0, 20.5 mm (bolted to the tub front);
- end caps: the pentagon B0–F0–F1–T0–B1 at x = ±58, cut from the same sheet.

Area per metre of width: (17.4 + 8.7 + 4 + 20.5) mm × 1.5 mm ≈ 76 mm². For 116 mm of width this gives 8.8 cm³, about 24 g in aluminium. The end caps add 2 × 0.6 cm³ (3 g). Total about **27 g**.

**10.4 Rail top section (XZ).** A half-round of r = 2 on top of a 4 mm wall: centre (±58, 20), top at z 22. Outer face x = ±60.

**10.5 Deck plates (XY outlines, z = top face).**
- DP-1: x ∈ [20, 54], y ∈ [12, 36], z 22.5.
- DP-2: x ∈ [−10, 54], y ∈ [−38, −14], z 22.0; lobe: a circle centre (10, −14), r 10, z 25.
- DP-3: x ∈ [−52, 30], y ∈ [−12, 38], a plane rising from z 21.5 at y 38 to z 24.5 at y 10, then falling to z 22 at y −12.
- DP-4: x ∈ [−54, −12], y ∈ [−38, −10], z 23.0.
- DP-5: x ∈ [−54, −36], y ∈ [−8, 38], z 22.5.
- Gaps between the plates: 2–4 mm.

**10.6 Wheels.** Cylinders r = 11, width 8, axis X, centres (±51.5, −26, 11) and (±51.5, 18, 11).

## 11. Pixel-based measurements (independent check)
Coordinates are (x px, y px), ±15 px.
- Wedge top edge: (230, 258) → (1445, 785). Length about 1325 px, foreshortened. With the robot's 116 mm along this edge and the camera azimuth about 30° off the face normal, that is about 11.5–12 px/mm along the edge.
- Wedge bottom (bevel) edge: (65, 500) → (1230, 1085).
- Left end face: corners about (1245, 790), (1445, 790), (1430, 955), (1230, 1085). Width about 200 px, height about 300 px (z is foreshortened by the elevation).
- Wedge screws: (410, 440), (645, 640), (975, 680).
- Left rail: (1440, 780) → (1725, 430); about 30 px thick in the image.
- Rear-left corner: (1725, 430). Rear-right corner: (600, 90).
- The deck's highest point (DP-3 ridge): around (870, 310).
- Wheels: left-front (1200–1360, 620–700), left-rear (1480–1650, 340–470), right-front (350–520, 270–330), right-rear (680–800, 50–120).
- Mask-based (likeness gate): the photo mask's height/length in the camera frame is about 0.62.

## 12. Several independent estimates of key sizes

| Quantity | Method A (spec / class) | Method B (photo ratio) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Tub width | 112 (spec) | — | wedge 1325 px / 11.7 px/mm = 113 | **112** (+ rails 120) |
| Tub length | 80 (spec) | 0.7 W from the left-rail length vs the wedge length (≈ 450 px vs 1325 px foreshortened differently) | — | **80** |
| Wedge width | 112 (old model) | the end faces are flush with the rails | — | **116** |
| Wedge height | 16 (old model blade) | about equal to the tub height + 2 | end face 300 px tall × cos(35°) / 12 → 20–22 | **21.5** |
| Wedge depth (plan) | — | about 0.2 of the tub width | 200 px / 12 = 17 at the end face (top part) + bevel 3 | **19–20** |
| Wheel Ø | 22 (spec) | 0.2 W | tyre arcs about 160 px across / 12 = 13 visible (tops only) | **22** |
| Screw head Ø (wedge) | M3 pan = 6 | — | about 75 px / 12 = 6.3 | **6.5** |
| Mass of the wedge | 24–27 g (folded sheet) | — | — | **≈ 25 g** (cannot be solid) |

## 13. Consistency check: conflicts and reconciliation
1. **Solid vs sheet wedge**: the end face looks solid and thick (no visible open box). But a solid aluminium bar of 116 × ~230 mm² is about 27 cm³ ≈ 72 g. With 4 motors (38 g), battery, ESC and tub, that breaks the 150 g limit. **Reconciled: a folded closed section with closed ends.** It looks solid because the ends are capped.
2. **Wedge angle**: the main face looks steep in the image (50–55°), but foreshortening exaggerates it. **Reconciled: 45° main face + 70° bevel.**
3. **Rails on both sides**: the near (left) rail is fully visible. The far (right) rail shows at both ends of the right side. **Reconciled: identical rails on both sides** (the round-5 model has `rail` + `rail_2` mirrored).
4. **Deck heights**: the deck plates step by 1–4 mm. The likeness silhouette is dominated by the outer outline, so the steps matter little for the IoU, but they matter for looks.
5. **Likeness gate camera**: the gate judges at elevation 45°, while the photo is about 30–35°. Seen from 45°, the model shows more deck relative to the wedge, so the model looks "too tall" (0.75 vs 0.62). Making the wedge face taller and steeper, and the deck lower, moves the 45° silhouette toward the photo's.
6. **Wedge vs front wheels**: the front wheels at y 18 (r 11) end at y 29. The wedge's back face at y 40 is clear by 11 mm. In the spec the chassis nose ramp starts at y 18, so the model's wedge cannot be a closed block that far back. It sits on the nose ramp instead.

---

## 14. Why the designer did it (per part, mostly adversarial)

- **Full-width metal wedge (the robot's only weapon)**
  - Fight:
    - Aluminium is harder and keeps a straighter, lower edge than any printed nose. A printed wedge chips and rounds off; a metal one stays sharp, so it wins the "who gets under whom" contest that decides wedge fights.
    - Full width means there is no gap for an opponent's forks.
    - The 70° bevel band at the bottom is a deliberate **lip edge**. A thin, steep band makes a strong edge that does not fold, and the shallower main face above it then lifts the opponent.
    - A closed triangular section is far stiffer than a single plate. It takes vertical-spinner hits without folding and spreads the impact into the tub through the back flange and 3 big screws.
  - Weak points:
    - It adds front mass, so the robot may nose-dive when pushed from behind.
    - The screws through the face are hit directly, but pan heads on a sloped face mostly glance off.
- **Chamfered wedge ends**
  - Fight: square corners catch on walls and opponents and get bent. A chamfer deflects horizontal spinners and stops the robot from hooking on the arena wall.
- **Clear tape on the wedge face**
  - Fight: a slick surface so opponents slide up rather than grip. It also protects the face finish. It is cheap and replaced between fights.
- **Low, wide tub (112 × 80 × 20)**
  - Fight: wide means it is hard to flip sideways and hard to push around (a long lever arm against turning). Low means a vertical spinner has little face to bite and the centre of gravity is low. The wheels are inside the tub, so a horizontal spinner cannot strike them directly.
  - Construction: a single print with room for 4 motors.
- **Yellow rails (rounded tub-wall tops) on both sides**
  - Fight: the rounded top edge glances side hits off. The rails stand slightly above the deck, protecting the deck plate edges from being peeled up by an opponent's wedge or a horizontal spinner tooth. They also act as bump strips against the arena wall.
- **Taped deck plates in several pieces**
  - Fight: the top can be hit by overhead weapons and is the surface opponents ride over. Several small plates mean a dent or tear is local and cheap to replace. The tape adds a sacrificial wear layer and stops plates rattling.
  - Construction: separate plates give **independent access** to each compartment (battery, ESC, switch hatch under the D-lobe) without removing the wedge. The scruffiness suggests repairs between events.
- **D-lobe hatch on DP-2**
  - Construction: a one-screw hatch for the power link or switch, so the robot can be armed quickly at the arena **(guess)**.
- **Four inboard wheels**
  - Fight: 4WD gives pushing traction even when one end is lifted. The wheels are shielded by the tub walls and rails. Their tops reaching the deck height may allow inverted driving.
  - Weak points: small wheels (Ø 22) mean low ground clearance, so the robot can be beached on seams.
- **Pan-head six-lobe screws everywhere**
  - Construction: one driver for the whole robot. Six-lobe recesses resist cam-out, which matters when screws are tight in aluminium/printed parts and heads get damaged.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre, floor z) | Confidence |
|---|---|---|---|---|
| Drive motors | 4 × N20 600 rpm | 12 × 10 × 32 | (±32.85, −26 / +18, 11), shafts along ±X | medium |
| Motor pockets | printed pockets in the floor, with the deck as the top clamp | 13 × 11 × 33 | under each motor | medium |
| Battery | 2S 180 mAh LiPo (blue wrap?) | 28 × 18 × 10 | (0, −3, 9) | medium |
| ESC/RX | Malenki Nano (4 motor outputs paralleled to 2 channels) | 23 × 16 × 5 | (−30, −0.5, 6.5) | low |
| Switch | slide switch under the DP-2 lobe, or a floor slot | 12 × 4 × 4 | (0, −24.5, 5.5) | low |
| Wedge mount | 3 × M3 into a printed front wall/nose block with heat-set inserts | — | y 40–44, z 10–14 | medium |
| Deck bosses | about 7 printed posts with M2.5 inserts | Ø 6 × 15 | under each deck screw | medium |
| Wiring | battery → switch (rear) → ESC (left-centre) → 4 motors (front/rear pairs in parallel) | — | below z 18 | medium |

**Wiring path summary (guess)**: everything is under the deck plates, inside the tub. The black bundle visible at the DP-3 tear is the battery/ESC lead running across the centre.

---

## 16. Model status vs this description (round 5 of `spec.json`)
- Matches: a full-width aluminium wedge (1.2 mm plate on the nose ramp), 116 wide, chamfered bottom corners, 3 screws normal to the face; yellow rails on both sides; 4 inboard wheels; tub size.
- To fix (driven by this description):
  1. **Chunky wedge**: add **end caps** (closed pentagonal ends) and a **lower bevel band** so the wedge reads as a closed triangular block, within the mass limit (the folded-sheet estimate is about 25 g; the model has 148.3 g with a 9.4 g plate).
  2. **Taped deck plates**: replace the single flat top plate with 4–5 stepped plates (§10.5) at slightly different heights, with a D-lobe hatch, in white.
  3. **Silhouette toward 0.80** at the gate's 45° camera: lower the deck/raise the wedge face (§13.5), and make the wedge ends flush with the rails.
