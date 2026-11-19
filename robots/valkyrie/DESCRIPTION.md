# Valkyrie: full reference description

This file is meant to be detailed enough to rebuild the robot from the text alone. Anything marked **(G)** is a guess or an inference. Everything else is read off the photos.

## 0. Coordinate frame (used everywhere in this file)

- Right-handed frame, in mm.
- Origin: the body centreline (x = 0), at the drive-wheel axle line (y = 0 is **not** used; see below), at the drive axle height (z = 0).
  - To match the current CAD, y = 0 is the CAD origin. The body runs y -50 (rear wall) to y +25 (front wall), the drum axis is at y = +42, and the cheek tips are at y about +56.
- **+x = robot's right, +y = forward (drum end), +z = up.** The ground plane is z = -13 (wheel radius 13).
- Photo pixel coordinates (u, v): u to the right, v down, in each original image's resolution:
  - aws71: 1923 x 1403
  - aws74: 1108 x 806
  - aws70: 423 x 360
- **Yardsticks:** body width over the side walls **W = 104 mm** (from the collector's kit and REFERENCE width_frac 0.77 x W = 80 drum length), and drive tyre diameter **D = 26 mm** (G, from the tyre-to-wall-height ratio).

---

## 1. Photos and cameras

| Photo | Size | Content | Camera (measured) | REFERENCE label |
|---|---|---|---|---|
| aws71 | 1923 x 1403 | cut-out on white, slightly over-exposed and green-tinted | robot front (drum) along the lower right; left wall ("VALKYRIE") along the lower left; chamfered rear corners at the top. So the camera is at the **front-left**, about 35-40 deg elevation, about 45 deg off the front axis (likeness azimuth about 135) | front_right_iso, user pick azimuth 60 / elevation 35 (working-tree edit, uncommitted) |
| aws74 | 1108 x 806 | cut-out, cleaner, colder light; drum windows face up | drum along the right/lower right, VALKYRIE wall facing the camera at the lower left. Same quadrant as aws71 but more from the side: **front-left**, elevation about 35, about 30 deg off the side axis | front_left_iso, elevation 45 |
| aws70 | 423 x 360 | arena table, low-res, other robots at the edge | from the **front**, high (about 60 deg), drum at the bottom | not used |

Notes:
- In aws71 and aws74 the wall with the "VALKYRIE" lettering faces the camera. Given the drum on the right of the image and the rear chamfers at the upper left, that wall is the robot's **left** wall (x = -52). Check: a camera at the front-left looking back-right puts the front on the right of the image. Yes.
- The current checker labels may have left/right mirrored. The checker compares mirrored silhouettes too.

---

## 2. Overall form

- A **squat, wide, flat two-wheel drum spinner**: a folded **sea-green aluminium sheet tub** (side walls and rear wall) with a **clear frosted polycarbonate lid** on top.
- A **raw-aluminium square-section drum with blue anodised end bearings** sits across the front between two **cheek guards**. The cheeks are the side walls continued forward, lined on the inside with **clear thick polycarbonate bearing blocks**.
- The two **black knurled tyres** are inside the side walls near the **rear**, poking up through **rectangular notches** in the lid's side edges just ahead of the rear chamfers.
- Approximate envelope:
  - Width 104 over the walls (W).
  - Length about 106 from the rear wall to the cheek tips (body 75 + cheeks 31).
  - Height about 22 (ground to lid top): body sheet top about z +8, lid z 8..9.5, tyre tops z +13 poking 3.5 above the lid through the notches.
  - Ground clearance at the walls about 2 mm (G).
- Colours:
  - Shell: **sea green**, satin anodised or painted aluminium with silver cut edges (about #2fa77a; highlights #6fd3a8, shade #1f7a58).
  - Lid: **clear frosted polycarbonate**. It reads pale grey-green (about #d6e4e0) with everything inside visible as blurred colour.
  - Drum: **raw machined aluminium**, scuffed silver-grey (about #b9bdc2).
  - Drum end hubs/bearing housings: **anodised royal blue** (about #2146c7) with a silver bearing face.
  - Screws: black socket heads on the drum and cheeks; chrome/silver button heads on the lid.
  - Inside: red wire and red XT30-type plug, a green PCB, a gold/brass motor can, and two white foam squares.

---

## 3. Part list

| # | Part | Count | Colour | Material (G where marked) | Size L x W x H mm (G where marked) |
|---|---|---|---|---|---|
| V1 | Shell tub (side walls + rear wall, one folded sheet) | 1 | green | 1 mm aluminium sheet (G) | 75 (y) x 104 (x) x 19 (z) |
| V2 | Rear chamfer folds | 2 | green | part of V1 | 45 deg legs about 18 x 22 |
| V3 | Base plate / floor | 1 | not visible (G: green or aluminium) | 1-1.5 mm aluminium or printed (G) | 75 x 102 |
| V4 | Lid (top plate) | 1 | clear frosted | 1.5 mm polycarbonate | 72 (y) x 104 (x) x 1.5 |
| V5 | Lid wheel notches | 2 | - | cut-outs in V4 | 15 (x) x 32 (y) |
| V6 | Lid screws | 4 (2 seen rear, 2 front G) | chrome | M2 button head | head 4 dia x 1.2 |
| V7 | Front wall / front cross plate | 1 | clear polycarbonate (frosted) | 3-4 mm PC (G) | 98 (x) x 4 (y) x 14 (z) |
| V8 | Front wall clips/tabs (bent aluminium angles) | 2 | raw aluminium | 1.5-2 mm aluminium | 6 (x) x 6 (y) x 10 (z) |
| V9 | Cheek guards (side wall extension) | 2 | green | part of V1, or a separate riveted plate (G) | 31 (y) x 1 (x) x 20 (z) |
| V10 | Cheek screws/rivets | 4 (2 per cheek) | black | M2/M2.5 socket button or rivet | head 4 dia |
| V11 | Clear bearing blocks (cheek liners) | 2 | clear PC | 4-6 mm thick PC | 30 (y) x 5 (x) x 18 (z) |
| V12 | Cheek foot / skid | 2 | green fold + clear edge | part of V9/V11 | 12 (y) x 8 (x) x 2 |
| V13 | Drum | 1 | raw aluminium | 6061 bar (G) | 80 (x) x 14 x 14 section, 2 edges |
| V14 | Drum windows | 4 | - | rectangular pockets | 9 x 9, on one face |
| V15 | Drum screws | about 8-10 | black | M3 countersunk/socket (G) | head 5 dia |
| V16 | Drum end hubs/bearings | 2 | blue + silver | anodised aluminium housing + ball bearing | 13 OD x 7 wide |
| V17 | Drum shaft / outrunner coupling | 1 | silver, x-shaped spider visible at the right end | steel shaft 4 dia (G); spider = outrunner end bell (G) | 90 long |
| V18 | Drive tyres | 2 | black | knurled rubber/foam | 26 OD x 11 wide |
| V19 | Drive motors | 2 | brass/gold end visible | N20 gearmotor (G) | 12 x 10 x 34 |
| V20 | Battery | 1 | grey with red leads | 2S LiPo (G 300-350 mAh) | 50 x 30 x 10 (G) |
| V21 | XT30-style plug + red lead | 1 | red | | 15 x 8 x 6 |
| V22 | Receiver / ESC (green PCB) | 1 | green | | 25 x 15 x 4 |
| V23 | White foam squares | 2 | white | foam/silicone pads | 14 x 14 x 5, with a 7 dia round dimple |
| V24 | Weapon motor (brass can) | 1 | gold | brushless outrunner (G) | 20 dia x 15 |
| V25 | Lettering "VALKYRIE" | 1 | black | engraved or printed | 30 long x 4.5 tall |

---

## 4. Parts in detail

### V1/V2: shell tub (green sheet)

- One folded sheet makes the two side walls, the rear wall and the two rear chamfer facets.
- **Wall thickness:** about 1 mm. The cut edges read as bright silver lines along the top edges.
- **Plan outline (outer):**
  - Rectangle x -52..+52, y -50..+25.
  - Rear corners chamfered at 45 deg (G angle), from (+/-52, -28) to (+/-34, -50). Legs: 18 in x, 22 in y.
  - The rear wall runs x -34..+34 at y = -50. The chamfer facets join it to the side walls.
- **Height:** from z -11 (bottom edge, 2 mm above the ground) to z +8 (top edge), so 19 mm.
- **Side walls (y -28..+25):** continuous, with **no wheel openings**.
  - The left wall carries the black lettering **VALKYRIE** in a blocky stencil font, letters about 4.5 tall, word about 30 long, centred at about y -5, z -2 (G).
  - In aws74 the word sits left of centre of the wall, nearer the rear: (u 160..290, v 450..470).
- **Side wall top edge:** straight and level. The lid sits on it.
- **Front:**
  - At y +25 each side wall continues forward into the cheek (V9).
  - There is a visible joint/step at about y +25: in aws74 a small green tab at (u 345, v 520) and a slight kink, so the cheek may be a separate plate overlapping the wall (G).
- **Fastening:** the sheet is screwed or riveted to the base plate (V3) along the bottom (G, not visible).

### V3: base plate (not visible)

- A flat floor (G), x -51..51, y -49..+25, 1-1.5 thick, at z -11..-9.5.
- It has openings for the wheel bottoms.

### V4/V5/V6: lid

- **Material:** clear polycarbonate with a frosted/scratched finish, about 1.5 thick.
- **Outline:** the same as the tub top (x +/-52, rear chamfers (+/-52, -28) to (+/-34, -50)), front edge straight at about y +22 (3 mm short of the tub front at +25).
- **Wheel notches (V5):** a rectangular notch in each side edge, x from +/-38 to +/-52 (open to the side), y from -24 to +8 (32 long). The tyre top shows in it.
  - In aws71 the left notch shows the tyre at (u 120..300, v 480..700) under the lid edge.
  - The right notch shows the far tyre at (u 1180..1300, v 150..250).
  - Both notches sit just ahead of the rear chamfer ends (y -28).
- **Height:** z +8..+9.5. The top is flat.
- **Screws (V6):**
  - Two chrome button heads (4 dia, proud 1.2) near the rear chamfer corners: in aws71 at (u 200, v 390) and (u 1095, v 115), so at about (x -40, y -36) and (x +40, y -36).
  - Two more are probably near the front edge (G: hidden by glare). In aws74, one is at the rear-right (u 510, v 90).
  - The current CAD has 2 screws near the centre (x 8.9, y -11.3) and (x -10.2, y -9.4). That **differs**: the photo has them at the rear corners.
- **Contacts:** the lid rests on the tub top edges (face contact, 1 mm wide sheet edges) and on internal standoffs (G). Gap to the drum: the front edge at y +22 versus the drum back at y about +35, so about 13 mm.

### V7/V8: front wall and its clips

- **Front wall (V7):** across the front of the body, between the cheeks, under the lid front edge.
  - A **clear thick polycarbonate plate** (it looks frosted like the lid), standing upright (G slightly raked back).
  - x -45..+45, y +21..+25, z -9..+6 (G).
- **Clips (V8):** two **bent raw-aluminium angle brackets** stand up from the front wall/lid edge.
  - At x about -22 and x about +22 (aws71: at u 365..410 and u 670..720).
  - Each is about 6 wide, 6 deep and 10 tall, with scuffed and hammered edges.
  - They clamp the lid's front edge or act as front bumpers/stops for the drum (G).
  - Gap between clip and drum: about 3-5 mm.

### V9/V10/V11/V12: cheeks (drum guards)

- Each cheek is a **green sheet plate in the side wall plane** (x = +/-52), running from y +25 to the tip at y about +56.
- **Profile (side view, in y-z):**
  - From (y 25, z 8): the top edge runs level to about y 30.
  - Then it steps down/slopes to about (y 40, z +2).
  - Then it slopes down to the tip top at (y 54, z -4).
  - The tip has a vertical front edge from (54, -4) to (54, -11).
  - The bottom edge runs level at z -11 back to y 25.
  - Expressed as a polyline: (25, 8), (30, 8), (46, 0), (56, -4), (56, -11), (25, -11) (G within +/-3).
  - The cheek's front-lower corner is a short green fold (V12) bent inward about 8 mm, forming a **foot/skid** at ground level. Its edge is lined with clear plastic (aws71: (u 580..770, v 1130..1260)).
- **Screws (V10):** two black round heads per cheek, about 4 dia, near the tip.
  - In aws74 at (u 430, v 610) and (u 470, v 690).
  - In frame coordinates about (y 47, z -1) and (y 51, z -7).
  - They clamp the green cheek plate to the clear block V11 behind it.
- **Clear bearing block (V11):** a thick **clear polycarbonate block** inside each cheek.
  - 5 thick in x (x +/-46..+/-51).
  - About 30 long in y (y 28..58) and about 18 tall (z -11..+7).
  - The top front corner is chamfered at about 45 deg (aws71: a chamfered clear plate edge at (u 420..640, v 860..1000)).
  - It carries the drum's bearing (V16). The blue bearing housing sits against its inner face at the drum axis (y 42, z -4).
  - These are the **plastic weapon mounts**: two thick PC plates, one per side, bolted through the green cheeks by the 2 black screws, holding the drum axle in bearings.
- **Gaps:**
  - Cheek inner face (clear block inner face x +/-46) to the drum end (x +/-40): 6 mm, filled by the blue hub (7 wide) less about 1.
  - Cheek tip to drum front: the drum front at y about 49 versus the cheek tip at 56, so the cheeks lead the drum by about 7 mm.

### V13-V17: drum

- **Body (V13):** a square-section aluminium bar, about 14 x 14 mm (G 12-16), 80 mm long (x -40..+40), axis along x at (y 42, z -4).
  - The bottom of the drum swing circle is at z -4 - 9.9 = -13.9, about 1 mm below the ground. That is not possible, so in practice the drum section is about 12 or the axis is higher (see the consistency check).
  - The long edges are slightly bevelled (about 1 mm) and scuffed.
  - Two of the four long edges are the impact "teeth": the bar has 2 effective strike faces per turn.
  - The section's diagonal sweep radius is r = 14 / sqrt(2) = 9.9.
- **Windows (V14):** four square through-pockets, about 9 x 9, on one face, evenly spaced at x = -27, -9, +9, +27 (aws74: at (u 560, 690, 800, 920) along the drum face).
- **Screws (V15):** black socket countersunk heads, about 5 dia, in **pairs** on the face at 90 deg to the windows.
  - aws71 pairs at about x -33/-28, -10/-5, +18/+23, plus 2 at the right end x +30/+35.
  - So about 8. They probably clamp the bar onto a hub/shaft or close a two-part drum (G).
- **End hubs (V16):** at each end, a **blue anodised cylinder** about 13 OD and 7 long (x +/-40..+/-47), coaxial with the drum, with a silver bearing face on its outer side.
  - It presses against the clear block V11.
  - In aws71 the left hub is at (u 600..790, v 280..520) of crop c1, a strong saturated blue.
- **Shaft/motor end (V17):** at the right end, between the drum and the blue hub, a silver disc with an **X-shaped spider/spokes** (aws71 crop c2: (u 600..760, v 180..290)). It is about 12 dia.
  - Reading: either an outrunner motor's rotating bell inside the drum (an in-drum motor) or a flexible jaw coupling (G).
  - The current CAD has the weapon motor inside the body, driving through... **differs** (G). If the drum carries the outrunner, the shaft is static and clamped in the clear blocks.
- **Mechanism:**
  - Drum spin axis x. It spins so that the top surface moves toward the opponent and down (G: typical for drums spinning upward-forward).
  - 2S LiPo, brushless.

### V18/V19: drive

- **Tyres:** black rubber with a **fine knurled/ribbed tread** (straight ribs about 1 mm pitch across the width).
  - 26 OD, 11 wide (G).
  - Hub hidden.
  - A brass gearmotor end is visible next to the left tyre (aws74: (u 330, v 100) in crop c5).
- **Position:**
  - Inside the walls: tyre outer face at x +/-51 (1 mm inside the 1 mm wall).
  - Axle at about y -16 (G; see the consistency check).
  - z 0.
  - The tyre top at z 13 shows through the lid notch.
- **Motors:** N20-type gearmotors along x (G), inboard of the wheels, at about x +/-27, with brass end caps visible.

### V20-V24: internals seen through the lid

- **Battery:** a grey/blue pouch under the lid at the left-centre-rear, with a red lead and **red XT30 plug** lying across at about (x -20, y -25), running toward the rear-left screw.
- **Green PCB:** receiver/ESC at the rear centre-right (x +5..+30, y -40..-30), under the lid near the rear edge.
- **White foam squares (V23):** two, 14 x 14 x about 5, each with a round 7 dia centre dimple (they look like silicone grommet pads).
  - At (x -15, y -20) and (x +25, y -10) (aws71: (u 230..330, v 270..330) and (u 530..650, v 140..210)).
  - They press the lid down on the electronics, or cushion the motors.
- **Brass/gold can (V24):** centre front, about 20 dia: the weapon motor or a drive motor gearbox.

---

## 5. Per-view descriptions

### 5.1 aws71 (front-left, about 38 deg elevation)

- **Lower left:** the long **green left wall** with VALKYRIE, receding from the rear-left chamfer (u 40, v 250) to the front-left cheek (u 330, v 700). Its silver top edge runs parallel to the lid edge.
- **Front-left corner:** the cheek, its two black screws, the clear block, the blue left hub and the green foot at the bottom.
- **Lower right:** the **drum** running from (u 330, v 520) to (u 900, v 260), silver with black screw pairs, then the right blue hub and the right cheek with its clear block and green edge at (u 850..960, v 190..400).
- **Upper area:** the **clear lid** with the rear chamfers top-left and top-right.
  - Screws at the rear corners.
  - Two white squares, the red plug, the green PCB.
  - The tyres in the side notches: left at (u 100..230, v 250..360), right at (u 640..760, v 80..180).
- **Behind the drum:** the clear front wall with the two aluminium clips.

### 5.2 aws74 (more from the left side, about 35 deg elevation)

- The left wall fills the bottom-left (u 40..380, v 300..520) with VALKYRIE.
- The cheek is at (u 360..520, v 450..640) with two screws.
- The drum is at (u 480..930, v 180..520), windows facing up-right.
- The right cheek is at (u 870..960, v 150..330).
- The lid is above, with the left tyre at (u 100..230, v 140..210), the right tyre at (u 290..340, v 60..100), and the rear-left screw (u 70, v 270), rear-right screw (u 510, v 90).

### 5.3 Top view (inferred)

- A 104-wide rectangle with 45 deg rear chamfers, 75 long to the front wall.
- Wheel notches at the sides from y -24 to +8.
- 4 lid screws.
- Cheeks continue forward 31 mm at the outer edges (x +/-46..52).
- The drum is 80 x 14 across between them at y 42.
- A 13 mm gap between the lid front and the drum.

### 5.4 Side view (left, inferred)

- Wall z -11..8 from y -50 (with the chamfer seen as a vertical line at y -28) to y 25.
- The cheek profile beyond.
- The drum circle r 9.9 at (42, -4) sitting inside the cheek outline.
- The tyre (r 13 at y -16) hidden behind the wall except for its top 5 mm above z 8, and its bottom 2 mm below the wall.

### 5.5 Front view (inferred)

- Two cheeks (thin green + clear, 6 wide) at the outer edges.
- The drum spanning between them with the blue hubs.
- Above and behind: the front wall and two clips, the lid edge at z 9.5, and the tyre tops just visible in the notches.

---

## 6. Contact and gap matrix

| A \ B | Shell V1 | Lid V4 | Front wall V7 | Cheek V9/11 | Drum V13 | Hub V16 | Tyre V18 |
|---|---|---|---|---|---|---|---|
| Shell | - | lid sits on the wall top edges (face, screwed) | wall ends meet the cheeks/walls (G bonded) | cheek = wall continuation (G a separate riveted plate) | none | none | tyre 1 mm inside the wall |
| Lid | - | - | lid front edge over the front wall (touch) | none (lid ends at y 22, cheeks start at 25) | about 13 gap | none | tyre top 3.5 above the lid, in a notch with about 1-2 mm side gap |
| Front wall | - | - | - | joins the cheeks (G) | about 8-10 gap | none | none |
| Cheek | - | - | - | - | about 6 axial gap at each end, filled by the hub | hub face against the clear block (bearing) | none |
| Drum | - | - | - | - | - | clamped to the shaft / hub one side (G) | none |

---

## 7. Fasteners summary

- **Lid:** 4 x M2 button head, chrome. 2 seen at the rear chamfer corners (about (+/-40, -36)), 2 at the front (G about (+/-40, +18)).
- **Cheeks:** 2 per cheek, black round heads (M2.5 G), through the green plate into the clear block at about (y 47, z -1) and (y 51, z -7).
- **Drum:** about 8 black countersunk socket screws in 4 pairs on one face.
- **Front clips:** 2 bent angle brackets, fixed by screws hidden under the lid (G).
- **Shell to base:** not visible (G: screws along the bottom edges).

---

## 8. All dimensions per part (mm, G = guess)

| Part | x | y | z | Thickness / radius / angle | Placement |
|---|---|---|---|---|---|
| V1 side wall | 1 | 53 (y -28..25) | 19 | sheet 1 | x +/-51.5 |
| V1 rear wall | 68 | 1 | 19 | sheet 1 | y -50 |
| V2 chamfer facet | 18 | 22 | 19 | 50.7 deg to x (atan(22/18)) | (+/-52, -28) to (+/-34, -50) |
| V4 lid | 104 | 72 (y -50..22) | 1.5 | notch 14 x 32 | z 8..9.5 |
| V6 lid screw | 4 dia | | 1.2 | | (+/-40, -36, 9.5) |
| V7 front wall | 90 | 4 | 15 | | y 21..25, z -9..6 (G) |
| V8 clip | 6 | 6 | 10 | sheet 1.5, bend r 1 | (+/-22, 24, 9..19) G |
| V9 cheek plate | 1 | 31 | 19 at the root, 7 at the tip | polyline above | x +/-51.5 |
| V11 clear block | 5 | 30 | 18 | top-front chamfer 45 deg, legs 8 | x +/-46..51, y 28..58 |
| V13 drum | 80 | 14 | 14 | sweep r 9.9; 4 windows 9 x 9 | axis (y 42, z -4) |
| V16 hub | 7 | 13 dia | 13 dia | r 6.5 | x +/-40..47 |
| V17 shaft | 90 | 4 dia | | r 2 | axis as the drum |
| V18 tyre | 11 | 26 dia | 26 dia | r 13; tread ribs 1 mm pitch | x +/-40..51, axle y -16 G |
| V23 foam | 14 | 14 | 5 | dimple r 3.5 | z 9.5..14.5? no: under the lid, z 3..8 (G) |

---

## 9. Curves as maths

- **Tyre side outline:** (y + 16)^2 + z^2 = 13^2.
- **Drum sweep circle:** (y - 42)^2 + (z + 4)^2 = 9.9^2. The ground (z = -13) is 9 below the axis, so the sweep bottom is 0.9 below the ground. See the consistency check.
- **Hub:** a cylinder of r 6.5 about the drum axis, x in [40, 47].
- **Rear chamfer line (right):** x = 52 - (y + 28) x (18 / 22) ... written in plan: from (52, -28) to (34, -50), so x = 52 + (18 / 22)(y + 28) for y in [-50, -28].
- **Cheek top edge (side, y-z):** piecewise linear:
  - z = 8 for y in [25, 30]
  - z = 8 - 0.5 (y - 30) for y in [30, 46]
  - z = 0 - 0.4 (y - 46) for y in [46, 56]
- **Clear block chamfer:** z = 7 - (y - 50) for y in [50, 58].
- No splines. All edges are straight or circular.

---

## 10. Independent measures of key features

| Feature | (a) From the yardsticks | (b) Ratio | (c) Pixels | (d) Frame coordinates |
|---|---|---|---|---|
| Body width | 104 (W) | drum / W = 0.77 (collector) | aws71 rear edge (u 70, v 230) to (u 640, v 40): 600 px | x +/-52 |
| Drum length | 80 | 0.77 W | aws71 (u 330, v 520) to (u 900, v 260): 627 px versus a body width of 600 px across the rear, more foreshortened. Ratio about 0.8 | x +/-40 |
| Drum section | 14 | 0.54 D | aws74 face width about 70 px against a drum length of about 470 px, so 80 x 70 / 470 = 12 | half-width 6-7 |
| Hub dia | 13 | 0.93 x drum section | aws71 about 75 px across against a drum length of 627, so 13 | r 6.5 |
| Body length (rear to front wall) | 75 | 0.72 W | aws74 wall from (u 40, v 300) to the cheek joint (u 360, v 520): 390 px against a lid width of about 450 px (rear edge), so about 0.75-0.85 W | y -50..25 |
| Wheel axle y | -16 | 0.45 of the body length from the rear | aws71 left tyre centre about 20 % of the full length from the rear; the full length is 106, so 21 from the rear, y = -29. The notch position on the lid (just ahead of the chamfer at y -28) suggests y -16 to -10 | -16 (reconciled) |
| Tyre dia | 26 | 1.37 x wall height | aws74 left tyre arc about 120 px wide against a wall height of about 90 px | r 13 |
| Wall height | 19 | 0.73 D | aws74 about 90 px | z -11..8 |
| Cheek length | 31 | 0.41 x body length | aws74 (u 360..520) about 160 px | y 25..56 |

---

## 11. Consistency check

1. **Wheel fore-aft position.**
   - The pixel estimate is about y -29: the tyre's centre is at 20 % of the length from the rear.
   - The notch just ahead of the rear chamfer, and the tyre seen in the notch, gives y -24..+8, centre -8.
   - The current CAD uses -8.
   - The photo shows the tyres clearly nearer the rear than the middle: the notch starts right at the chamfer end.
   - **Reconciled:** axle y about -16, ±8. The CAD's -8 is within tolerance at the notch's centre. Not moved in this pass (the motors, pockets and wiring depend on it).
2. **Drum sweep below the ground.**
   - A 14 mm square section about an axis at z -4 sweeps to z -13.9, below the ground (-13).
   - Either the section is 12 (sweep 8.5, reaching z -12.5) or the axis is about z -3.
   - **Reconciled:** section 14 x 7 effective (the CAD uses an 18 x 7 flat bar plus an r 3.5 core) or 12 square. The CAD keeps its own.
3. **Lid notches versus "wheels inside".**
   - The tyres are inside the walls (the wall is continuous), but the lid is notched.
   - Both are true: the tyre top (z 13) is above the wall/lid (z 8..9.5) and pokes up through the notch.
   - **Reconciled:** walls closed, lid notched.
4. **Lid screw positions.**
   - Photo: rear chamfer corners.
   - CAD: near the centre.
   - **Reconciled:** the photo wins. Moving them is optional and was not done in this pass.
5. **Camera labels.**
   - aws71 is labelled front_right (user pick azimuth 60), but the measured view is front-left (the VALKYRIE wall is the robot's left).
   - The checker compares mirrored silhouettes, so this does not affect IoU much.
   - Not edited (collector file).
6. **Mass.**
   - The photo robot is aluminium sheet plus PC. The CAD is printed nylon with 2.5 mm walls, which is heavier.
   - The CAD at r4 is 173 g, over 150.
   - **Reconciled:** thin the walls or use a lighter battery in the CAD. This is noted as a CAD issue, not a photo fact.

---

## 12. Why the designer did it (per part)

- **Folded aluminium shell V1/V2**
  - Fight: tough and dent-tolerant. The sheet takes drum and spinner hits better than print. Chamfered rear corners deflect hits and stop the corners catching on walls.
  - Build: one laser-cut blank, bent on a brake. Light at 1 mm thickness.
  - Repair: can be bent back.
  - Looks: green anodised for team colours. The name engraved on the side.
- **Clear PC lid V4 (frosted)**
  - Fight: PC is the toughest light sheet and survives impacts without cracking.
  - Build: a laser-cut flat sheet held by 4 screws.
  - Repair/inspection: you can see the LEDs, plug and wiring without opening.
  - Wheel notches: they let the body be lower than the tyres (keeping the robot height to the wall top), while the tyres are still protected at the sides by the walls.
- **Front wall V7 and clips V8**
  - Fight: they close the electronics bay from drum debris and stop opponents' parts entering. The clips double as stops and hold the lid front.
  - Build: simple bent tabs, cheap.
- **Cheeks V9 and clear bearing blocks V11**
  - Fight: they protect the drum ends and bearings from side hits, and the cheek tips act as forks/skids that lead the drum. Thick PC absorbs shock (it flexes rather than shattering) and isolates the bearings.
  - Build: thick PC blocks are machinable and bolt through the sheet with 2 screws each, so the drum can be removed by loosening the cheeks.
  - Repair: the blocks are swappable.
- **Square aluminium drum V13 with windows V14 and screws V15**
  - Fight: a solid bar gives high bite with 2 effective edges. The windows lighten it and balance it. It is wide (0.77 W), so it is hard to miss.
  - Build: cut from stock bar and milled. The screws clamp the bar to the motor or shaft and are replaceable.
- **Blue hubs/bearings V16:** shielded ball bearings in anodised housings carry the drum near the ends, so the shaft does not bend. They are also visual branding.
- **Possible in-drum outrunner V17**
  - Fight: no belt to break.
  - Build: compact, which frees body space for the drive and battery.
- **Drive tyres inside the walls, near the rear V18/V19**
  - Fight: the walls shield the wheels. The rear placement puts the weight over the wheels when the drum is loaded, and the cheek feet carry the front.
  - Build: N20 gearmotors are cheap and light.
- **White foam pads V23:** they cushion the electronics or motors against impact and are pressed by the lid to stop them rattling (G).

## 13. Unseen and inner parts (guesses with confidence)

| Part | Size (mm) | Position | Confidence | Notes |
|---|---|---|---|---|
| Base plate | 102 x 75 x 1.2 aluminium or 1.5 PC | z -11..-9.8 | medium | Screwed to the folded wall flanges (about 6 M2). |
| Wall-to-base flanges | 1 mm folds 5 wide | inside the bottom of each wall | low | |
| Drive motors (2) | N20 12 x 10 x 34 (+ gearbox) | axis x, at y about -16, from x +/-22 to +/-50 | medium | Brass end seen next to the left tyre. Clamped by printed or aluminium saddles with 2 x M2 each (low). |
| Drive hubs | grub-screw hubs 3 mm D-shaft | inside the tyres | medium | |
| Battery | 2S 300-350 mAh, 50 x 30 x 10 | x -20..+10, y -35..-5, z -9..+1 | medium | Red XT30 at its rear-left. Velcro to the base. |
| Weapon ESC | 20-30 A brushless ESC, 30 x 18 x 6 | x +5..+30, y -15..+15 | low | |
| Receiver / drive ESC (green PCB) | 25 x 15 x 4 (Malenki-style combined board) | x +5..+30, y -40..-28, under the lid's rear | medium (green PCB seen) | |
| Power link / switch | removable link (XT30 loop, G) or a slide switch | rear left, by the red plug | medium | The red plug lying loose in the photo looks like a link (G). |
| Wiring | battery -> link -> PCB -> 2 drive motors (wires along the floor, routed round the battery); PCB -> weapon ESC -> 3 motor phases through the front wall to the drum motor | | medium | |
| Weapon motor | outrunner about 22 dia x 12 inside the drum's right end (the spider seen), or a body-mounted 1404 driving through the shaft | right end of the drum or the centre front of the body | low | |
| Drum shaft | 4 mm steel, 90 long, clamped in the clear blocks | axis y 42, z -4 | medium | |
| Bearings | 2 x MR84 or 684 (4 x 8 x 3) in the blue housings | x +/-44 | medium | |
| Lid standoffs | 4 x M2 standoffs 18 tall or printed pillars | under the lid screw positions | low | |
| Internal ribs | none (sheet tub) | | medium | |
