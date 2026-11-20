# Termite Cluster: full rebuild description from reference photos

Termite Cluster (Team Termite) is a **multibot (cluster)**: more than one robot fights as one entry. Every photo shows **two robots**, and the pair changes between events:

- `robots/termite_cluster/reference/termite_cluster.aws69.webp` (3014 × 1308 px, the best photo). AWS 69. **Left: "Alsoran"**, a small black two-wheel wedge seen from the front, about 30° down. **Right: "Defiant"**, a black four-wheel H-shaped box with a clear lid and front/rear wedge lips, seen from the front, about 35° down. Both are on a pale green surface (the green tint in the lips is partly the backdrop showing through clear plastic).
- `robots/termite_cluster/reference/termite_cluster.aws68.webp` (727 × 532 px). AWS 68. The same pair. Defiant is upper left, seen from front-left above (its label upside down to the camera, so we see it from its **rear-left**). Alsoran is lower right, seen from its front-left, about 35° down. This photo shows Alsoran's **left side wall** and **left wheel**, and Defiant's two lips.
- `robots/termite_cluster/reference/termite_cluster.aws65.webp` (419 × 425 px, low resolution). AWS 65. **Upper: "Dominant"**, a blue tracked robot with bright green treads, a purple hex-lattice lid, and a grey front wedge with a label. **Lower: Alsoran** in an earlier livery (black body, **blue-purple lid**, green wheels).

Everything stated as fact is read from these photos. Inferences are marked **(guess)**. Dimensions are **estimates**. Scale anchors: AWS antweight class (150 g total for a cluster; each robot must still fit the 4 in / 101.6 mm cube **(guess on rule)**); the **N20 gearmotor** (12 × 10 mm gearbox, can Ø 12 × 15 mm), which is visible in both robots; the **printed label** (standard 2-line address label, about 38 × 12 mm for Alsoran's, about 50 × 10 mm for Defiant's); and Defiant's 4 small wheels (Ø ≈ 20 mm).

Because there are three different robots, this document describes **Defiant** (§A) and **Alsoran** (§B) in full, and **Dominant** (§C) in as much detail as the 419 px photo allows. Shared sections (frame, assembly, consistency, design intent) follow.

---

## 0. Coordinate system and naming (applies to each robot in its own frame)

- **Origin O**: on the floor (z = 0) under the centre of that robot's plan footprint (mid-width, mid-length).
- **+X** = robot's right, **+Y** = forward, **+Z** = up; mm.
- **Front** of Defiant = the end nearest the camera in AWS69 (the label reads correctly from there). Defiant is **symmetric front/rear** apart from the label, so "front" is nominal.
- **Front** of Alsoran = the lipped wedge end (facing the camera in AWS69).

| ID | Part |
|---|---|
| **Defiant (D-)** | |
| D-CH | H-shaped black printed chassis tub |
| D-BF / D-BR | front / rear full-width bumper bars (part of D-CH) |
| D-WP (×4) | wheel pockets (the 4 notches of the H) |
| D-LF / D-LR | front / rear wedge lips (clear-green plastic sheet + fibre tape) |
| D-LID | clear polycarbonate lid |
| D-S1 / D-S2 | 2 lid screws (front centre, rear centre) |
| D-STK | smiley "TEAM TERMITE" sticker on the lid |
| D-NM | name label "Termite Cluster / Defiant" |
| D-M1..M4 | four N20 gearmotors (brass gearboxes) |
| D-MM | plastic motor cradles / clamp ribs |
| D-WH1..4 | four wheels (white hub, blue segmented tyre) |
| D-PCB | green circuit board (ESC/receiver) under the lid |
| D-BAT | battery (pink/red pack, right side under lid) |
| D-SW | switch (small dark slider near the right edge under/through the lid) |
| D-WR | wires (yellow, green visible under the lid) |
| **Alsoran (A-)** | |
| A-CH | black printed wedge-shaped tub (side walls + floor + rear bay) |
| A-SL / A-SR | left / right sloped side walls |
| A-TP | sloped top plate (black in AWS68/69, blue-purple in AWS65) |
| A-S (×6) | 6 small silver Phillips screws on A-TP |
| A-NM | name label "Termite Cluster / Alsoran" |
| A-LP | front lip (clear-green sheet + grey tape) |
| A-BAY | open rear bay |
| A-RB | rear crossbar (top of the rear wall) |
| A-DV | central printed divider with a tall upright tab (A-TAB) |
| A-M1 / A-M2 | two N20 gearmotors (transverse) |
| A-WH1 / A-WH2 | two rear wheels (white hub, blue segmented tyre; green in AWS65) |
| A-WR | wires (green, yellow, orange, red, purple, blue) |
| A-SW | power switch / link (guess: A-TAB) |
| **Dominant (C-)** | |
| C-CH | blue printed chassis |
| C-TR | two bright-green TPU tracks |
| C-LID | purple hex-lattice lid |
| C-WG | grey front wedge plate with label |

---

## 1. Overall description in one paragraph

**Defiant** is a **flat, symmetric, four-wheel box** about **100 mm square in plan and only about 18 mm tall**. Its black printed chassis is shaped like a capital **H lying on its side**: full-width **bumper bars** at the front and rear, joined by a narrower **central body**, which leaves four **rectangular notches**, one at each corner, where the four small wheels sit. The central body is covered by a **clear polycarbonate lid** held by **two screws**, so the motors, the green circuit board and the battery are visible through it. A big **yellow smiley "TEAM TERMITE" sticker** and a **name label** sit on the lid. The front and rear bars each carry a **thin, wide wedge lip** of clear plastic with **fibre tape**, so it can push from either end and run either way up. **Alsoran** is a **smaller two-wheel wedge**, about **75 mm wide and 75 mm long**: a black printed tub whose **side walls slope down toward the front**, topped by a **sloped plate** held by six screws, with a **grey-taped lip** in front, an **open rear bay** with two transverse N20 motors and colourful wires, and two **wheels at the rear corners** outside the side walls. **Dominant** (AWS65) is a **blue tracked robot** with **green treads**, a **purple honeycomb lid**, and a **grey front wedge**.

---

## A. Defiant

### A.1 Chassis (D-CH) and bumper bars (D-BF, D-BR)
- **Plan**: an H. Overall outer outline **100 mm wide (X) × 96 mm long (Y)** (lip to lip ≈ 112 including lips, see A.4).
  - **Bumper bars**: each spans the full 100 mm width and is about **20 mm deep (Y)**. They form the solid ends of the H.
  - **Central body**: about **64 mm wide (X)** and spans the full length between the bars (overall 96 mm), so it is 56 mm long between the bars.
  - **Notches (D-WP)**: each is **18 mm wide (X, from x = ±32 to ±50) × 56 mm long (Y, between the bars)**. Seen from above (AWS69, AWS68), each notch is not simply open: a **thin inner wall** separates it from the central body, and the bars' inner faces form its front and rear ends. The wheels sit inside, so each notch is a **three-sided pocket open to the outside**.
  - Correction from AWS69: the notches are **open to the side only between the front and rear wheels**. The **bars' ends wrap round each wheel** as short **side lugs** (about 10 mm long, Y) at x = ±50, in line with the wheels. The front-left lug is seen as a block outboard of D-WH1. So each wheel is boxed on its front, outside-front and inside, and the middle of the notch (between the front and rear wheels) is open to the side, about **26 mm long**.
- **Height**: the bars are about **16 mm tall** (z 2–18). Their outer faces show **heavy horizontal print layers** (about 0.3 mm layers, rough, dark grey-black). The central body walls are about **14 mm tall** to the lid seat. The lid sits about **1 mm below** the bar tops.
- **Bar top**: a flat 3 mm wide rim around a **recess** (AWS69 rear bar: the top of the rear bar shows a raised rim with a shallow trough inside). This is the **rear bar shown as an open trough about 90 × 14 mm, 6 mm deep**, a weight-saving pocket **(guess)**.
- **Walls**: about **2.5–3 mm** thick (visible at the notch edges).
- **Floor**: not visible. Presumably a 1.5–2 mm floor at z ≈ 2 with ground clearance about 2 mm **(guess)**.

### A.2 Wheel pockets (D-WP) and wheel support
- Each wheel sits with its axis along X, **just inside the side lug**. Wheel outer face to the lug inner face: about **1–2 mm**. Wheel inner face to the central body wall: about **3–4 mm**, where the brass gearbox and shaft cross.
- Wheel tread to the bar inner face (front wheels to D-BF): about **2 mm**.
- **Guard-to-chassis supports**: the "guard" for each wheel is the **bumper bar end + side lug**, which is **printed integral** with the chassis (continuous layer lines in AWS69). No separate guard parts, no screws.

### A.3 Wheels (D-WH1..4)
- **Shape**: **Ø ≈ 20 mm × 8 mm wide**. A **white hub/inner ring** (Ø about 14 mm, visible as a white disc on the outer face) carries a **blue tyre with 8–10 rectangular blocks** separated by deep transverse slots (a segmented/"paddle" tyre). The blocks are about **5 mm long × 8 mm wide × 3 mm tall**, with gaps of about 1 mm. The blue colour is mottled, like a sponge or a soft-printed TPU.
- **Hub**: white, with a **central bore** (dark hole about 3 mm) on the outer face.
- **Position (centres)**: x = ±41, y = ±34, z = 10. So the **wheelbase is 68 mm** and the **track is 82 mm** (centre to centre).
- **Height**: wheel top at z = 20, about **2 mm above the bar tops** (z 18). Bottom at z = 0. The wheels protrude above and below the chassis, so **Defiant drives either way up**.

### A.4 Wedge lips (D-LF, D-LR)
- **Shape**: a thin flat strip running the full chassis width, **100 mm × 16 mm (Y) × 0.8–1 mm**, angled down from the bottom edge of each bumper bar to the floor at about **15–20°**. It is **wider than the chassis**: in AWS69 the front lip extends **about 4–5 mm beyond each side** (lip ≈ 108 mm wide).
- **Material**: a **clear / pale-green transparent sheet** (polycarbonate or PET) with **filament (reinforced) packing tape** across it. The tape shows a fine **grid of glass fibres** (white parallel lines along X and faint cross threads) over the front 8 mm. In AWS68 the lips look **white/opaque**, which is the tape seen at a different light angle.
- **Fixing**: the lip's rear edge goes under or behind the bumper bar bottom, held by the tape wrapping round the bar's lower front edge, or glued in a slot **(guess: slotted into the bar's bottom-front edge and taped)**.
- **Symmetry**: D-LR at the rear is identical (AWS68 shows both ends lipped; AWS69 shows the rear lip edge rising pale green above the far bar).
- **Invertibility**: a lip angled down from the bar's bottom edge only touches the floor when the robot is the right way up. When upside down, the same lip points up. **(Guess)**: the lip is **hinged / flexible**, so it falls to the floor either way, or the lip comes out of the mid-height of the bar so it reaches the floor at the same angle both ways. From AWS69 the lip leaves the **bottom** of the bar, so it is probably a **flexible sheet** that bends down under its own weight and rubs on the floor both ways.

### A.5 Lid (D-LID), screws (D-S1, D-S2), stickers
- **Lid**: a **clear polycarbonate rectangle**, **62 × 92 mm × 1 mm** (the central body plus its walls), with **slightly rounded corners (r about 2 mm)**. Through it, the **green PCB**, **4 motor cans (silver)** with **brass gear stacks**, **yellow and green wires**, and a **pink/red battery** are visible.
- **Screws**: **2 small silver Phillips pan screws** (head Ø about 3.5 mm), one at the **front centre** and one at the **rear centre** of the lid, about 4 mm in from each end edge. They go into bosses in the central body end walls.
- **D-STK**: a square white sticker, **about 50 × 50 mm**, with a **yellow smiley** whose **upper-right is bitten out by a grey circular saw blade**, with **"TEAM"** above and **"TERMITE"** below in black arched capitals.
- **D-NM**: a white label, **about 50 × 10 mm**, reading "Termite Cluster / Defiant", in front of the sticker.

### A.6 Motors (D-M1..4) and motor mounts (D-MM)
- **4 × N20** gearmotors, one per wheel. Through the lid, two are at the **front** (silver cans side by side near the centreline, brass gearboxes outboard by the wheels) and two at the **rear**, mirrored. Each lies **along X**, with its shaft through the central body wall into the wheel hub.
- **Mounts**: the cans sit in printed **transverse cradles** (dark ribs either side of each can, visible as dark bars through the lid). The lid itself clamps them down from above **(guess)**.
- Visible brass parts: the gear stacks (gold) at x ≈ ±26 near each wheel; brass **standoffs or the gearbox frame**.

### A.7 Electronics
- **D-PCB**: a **green board**, about **40 × 30 mm**, along the left-centre under the lid, with small components. A **clear/white ribbed part** (a crystal or capacitor in clear heatshrink) runs along the left side **(guess: receiver in heatshrink)**.
- **D-BAT**: a pink/red pack under the right half of the lid **(guess: 1S or 2S LiPo, about 30 × 20 × 6 mm)**.
- **D-SW**: a small black slider visible near the right-hand edge of the lid at mid-length, next to a round black part. It is probably reached through a small hole in the lid or the right wall **(guess)**.
- **Wires**: yellow and green leads between the motors and the board.

---

## B. Alsoran

### B.1 Chassis (A-CH)
- **Plan**: a rectangle, **74 mm wide (X, outside the side walls) × 72 mm long (Y)** excluding the lip. With the lip the overall length is about **84 mm**. The wheels add about **8–9 mm on each side** at the rear (overall width about **92 mm**).
- **Side walls (A-SL, A-SR)**: each is a **trapezoid / right-angled wedge in side view**: about **24 mm tall at the rear** (z 0–24), sloping down to about **6 mm tall at the front** (z 0–6), over 72 mm. Thickness about **3 mm**. Outer faces show **heavy horizontal print layers**. The side walls' top edges follow the slope of the top plate (they stand **1–2 mm proud** of the plate, so the plate sits recessed between them).
- **Rear**: an **open bay** (A-BAY) occupying the rear **22 mm** of the length, between the side walls, from the floor up to about z = 24.
- **Rear crossbar (A-RB)**: a **dark rod/bar** running across the top-rear of the bay (AWS69: a straight dark line from the left wall to the right wall at z ≈ 22). It is either a **3 mm steel rod** or the top edge of a printed rear wall **(guess: printed rear rail 3 × 3 mm, part of A-CH)**.
- **Front**: the side walls end at the lip line. The floor under the top plate is presumably hollow **(guess)**.

### B.2 Top plate (A-TP)
- **Shape**: a **flat plate about 62 mm wide × 54 mm long × 1.5 mm thick**, sitting at **about 18°** (from z ≈ 22 at its rear edge to z ≈ 5 at its front edge). The **rear corners are cut at 45°** (chamfers about 6 mm, top-left and top-right in AWS69). The front corners are square.
- **Material/colour**: AWS68/69: **matt black**, with a fine woven or brushed texture and scratches, possibly **black FR4 / G10** or carbon-fibre sheet, or a printed plate with ironed top **(guess: printed)**. AWS65: **blue-purple** (a printed plate, top-surface infill visible), with a white label "TERMITE CLUSTER / ALSORAN".
- **Fasteners (A-S)**: **6 silver Phillips pan-head screws**, head Ø about **3.5 mm** (M2):
  - **2 at the rear-left**: one above the other, about 5 mm apart, at about 6 mm from the left edge, 6 and 11 mm from the rear edge.
  - **2 at the rear-right**, mirrored.
  - **1 at the rear centre**, above the label (about 4 mm from the rear edge).
  - **1 at the centre**, just below the label (about 20 mm from the rear edge).
  - These screw into the side walls' internal ledges (left/right pairs) and into the central divider (the two centre screws) **(guess)**.
- **Label (A-NM)**: white, about **40 × 13 mm**, "Termite Cluster / Alsoran", between the centre screws, slightly peeled and creased at its lower edge.
- **Rear edge**: the plate overhangs the front of the bay. Under its rear edge the motor cans and wires are visible.

### B.3 Front lip (A-LP)
- **Shape**: a strip about **78 mm wide × 16 mm (Y) × 1 mm**, a little wider than the chassis, angled from under the top plate's front edge to the floor at about 15°.
- **Material**: a clear-green sheet (see A.4) with **grey/silver tape** across the rear 8 mm (the tape is a grey band about 8 mm wide covering the joint to the chassis). The front 8 mm reads pale green (the backdrop through the clear sheet).
- **Side ends**: the lip's ends are cut **square at 90°**, flush with or slightly beyond the side walls (the right end protrudes about 3 mm past the right wall in AWS69).

### B.4 Rear bay (A-BAY), divider (A-DV) and tab (A-TAB)
- **Divider A-DV**: a printed **central rib**, about **6 mm wide (X) × 20 mm long (Y) × 22 mm tall**, splitting the bay into left and right halves. Each half holds one motor.
- **Tab A-TAB**: on top of the divider, at the rear, a **tall upright black printed tab**, about **8 mm wide × 3 mm thick**, standing about **10 mm above the crossbar** (to z ≈ 32), **bent slightly back**. It is the highest point of Alsoran. It is most likely the **removable power link** (a printed handle on a jumper plug) or a switch actuator extension **(guess: removable link, medium)**.
- **Bay components** (AWS69): each half has an **N20 motor** lying along X, with its **silver can inboard** next to the divider and its **brass gear stack outboard** near the wheel. **Wires**: green and yellow on the left motor; orange looping at the left front; red, purple and blue on the right. A **white/cream connector** sits at the right of the divider **(guess: JST battery plug)**. A **horizontal dark rod** runs across each half above the motors, at about z ≈ 18 (the clamp bar or the crossbar).

### B.5 Motors (A-M1, A-M2) and mounts
- **2 × N20**, transverse, coaxial, shafts outward through the side walls, at y ≈ −26, z ≈ 10.
- **Mount**: each motor is clamped between the divider and the side wall in a printed cradle, with a **top bar** over the can (the dark rod across the bay) **(guess: printed strap screwed to the divider and the wall)**.

### B.6 Wheels (A-WH1, A-WH2)
- **Shape**: like Defiant's: **Ø ≈ 20 mm × 9 mm**, a **white hub** and a **blue segmented tyre** (8–10 blocks). AWS65: **green tyres**.
- **Position**: outboard of the side walls, centres at x = ±42, y = −26, z = 10. Wheel inner face to side wall gap about **1–2 mm**.
- **No guard**: the wheels' outer faces and treads are **fully exposed**. The side walls protect only their inner side.
- **Height**: the wheel top (z 20) is **below** the chassis rear top (z 24) and the tab (z 32), so Alsoran **cannot drive inverted** (it would sit on its rear bay top and tab).

### B.7 Switch / wires (A-SW, A-WR)
- No dedicated switch is visible, apart from A-TAB (see B.4). Wires are listed in B.4.

---

## C. Dominant (AWS65 only; low resolution)
- **C-CH**: a **bright blue** printed box chassis, about **100 × 90 mm** in plan, about **25 mm tall**, with sloped front and rear faces.
- **C-TR**: **two tracks**, one each side, **bright green TPU**, about **14 mm wide**, running over **white/grey wheels** (2–3 per side visible). The track outer faces show **chevron/ribbed lugs** about every 5 mm. The tracks run the full side length (about 90 mm) and are about **26 mm tall** (they stick out above the chassis top, so it is invertible).
- **C-LID**: a **purple printed hexagonal lattice** (open honeycomb cells about 6 mm across) over the electronics, about **60 × 55 mm**, with **the smiley "TEAM TERMITE" sticker** on it and **small screws** at the corners.
- **C-WG**: a **grey front wedge plate** (aluminium or grey sheet), about **95 × 20 mm**, angled at about 20°, with a white label "TERMITE CLUSTER DOMINANT" on a grey band.
- Detail beyond this is not recoverable from the 419 px photo.

---

## 3. Per-view descriptions

### 3.1 Top views
- **Defiant**: an H, 100 × 96 mm, with 4 wheels (8 × 20 mm rectangles in plan) in the corner notches. The clear lid occupies the central 62 × 92 mm with the smiley sticker. Lips are thin 108 × 16 mm strips at both ends.
- **Alsoran**: a 74 × 72 mm rectangle; the front 54 mm is the dark top plate with 6 screws and the label; the rear 18 mm is the open bay with the divider tab. Wheels: 9 × 20 mm rectangles outboard at the rear corners. A 78 × 16 mm lip in front.

### 3.2 Front views
- **Defiant**: a low, wide slab (100 × 16 mm), striped with print layers, with the taped lip in front. The four wheels' tops (white hub discs and blue tread) show above the bar line at the corners, as in AWS69.
- **Alsoran**: the grey-taped lip, then the dark sloped plate rising to the rear. The two side walls frame it (tall at the back, short at the front). Behind and above: the wheel tops at the corners and the **upright tab** in the middle.

### 3.3 Side views
- **Defiant**: a flat slab, 16 mm tall, with the lip strips running down to the floor at both ends; two wheels sticking out about 2 mm above and below, in the corner pockets, with the open middle notch showing the inner wall.
- **Alsoran** (AWS68 shows the left side): a **right-triangle-ish wedge**, 24 mm tall at the rear tapering to 6 at the front, then the lip to the floor. The rear wheel overlaps the rear third of the side.

### 3.4 Rear views (partly seen in AWS68 for Defiant)
- **Defiant**: identical to the front (rear bar + rear lip).
- **Alsoran**: the open bay with the crossbar, motors, wires and the tab, between the two side walls, with the wheels outboard. **(Not photographed; inferred.)**

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|
| D-CH | H-shaped tub | 100 × 96 × 16 | black printed (PLA/PETG) | — | 1 |
| D-BF/BR | bar | 100 × 20 × 16 (top pocket 90 × 14 × 6) | black | integral | 2 |
| D-WP | notch pocket | 18 × 56 | — | — | 4 (2 per side) |
| D-LF/LR | thin sheet | 108 × 16 × 1 | clear PC/PET + fibre tape | slot + tape (guess) | 2 |
| D-LID | flat plate | 62 × 92 × 1 | clear polycarbonate | 2 × M2 | 1 |
| D-S | pan Phillips | M2, head Ø 3.5 | silver | lid to body | 2 |
| D-STK | sticker | 50 × 50 | white/yellow | adhesive | 1 |
| D-NM | label | 50 × 10 | white | adhesive | 1 |
| D-M | N20 gearmotor | 12 × 10 × 25 | silver/brass | cradles + lid | 4 |
| D-WH | segmented wheel | Ø 20 × 8 | white hub, blue tyre | D-shaft | 4 |
| D-PCB | board | 40 × 30 × 5 | green | — | 1 |
| D-BAT | LiPo | 30 × 20 × 6 | pink/red | — | 1 |
| A-CH | wedge tub | 74 × 72 × 24→6 | black printed | — | 1 |
| A-TP | sloped plate | 62 × 54 × 1.5 | black (blue in AWS65) | 6 × M2 | 1 |
| A-S | pan Phillips | M2, head Ø 3.5 | silver | TP to CH | 6 |
| A-LP | thin sheet | 78 × 16 × 1 | clear + grey tape | tape (guess) | 1 |
| A-DV | rib | 6 × 20 × 22 | black | integral | 1 |
| A-TAB | upright tab | 8 × 3 × 12 | black printed | plugs into the divider (guess) | 1 |
| A-RB | crossbar | 3 × 3 × 68 | black / steel | integral (guess) | 1 |
| A-M | N20 gearmotor | 12 × 10 × 25 | silver/brass | cradle | 2 |
| A-WH | segmented wheel | Ø 20 × 9 | white hub, blue (green AWS65) | D-shaft | 2 |
| A-NM | label | 40 × 13 | white | adhesive | 1 |
| C-* | Dominant | 100 × 90 × 26 | blue/green/purple/grey | — | 1 robot |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| D-LF / D-LR edge ↔ floor | touching | 0 |
| D-LF ↔ D-BF bottom-front edge | slotted/taped | 0 |
| D-CH floor ↔ floor | above | ~2 |
| D-WH bottom ↔ floor | touching | 0 |
| D-WH top ↔ D-BF top | wheel proud | +2 |
| D-WH outer face ↔ side lug | side by side | 1–2 |
| D-WH inner face ↔ central body wall | gap for gearbox/shaft | 3–4 |
| D-WH tread ↔ bar inner face | fore-aft | ~2 |
| front wheel tread ↔ rear wheel tread (same side) | fore-aft gap | ~48 |
| D-LID ↔ central body walls | screwed (2) and resting | 0 |
| D-LID top ↔ bar top | lid lower | −1 |
| D-M ↔ D-MM | clamped by ribs + lid | 0 |
| A-LP ↔ floor | touching | 0 |
| A-LP ↔ A-TP front edge | tape joint | 0 |
| A-TP ↔ side wall ledges | screwed (4) | 0 |
| A-TP ↔ A-DV | screwed (2, guess) | 0 |
| A-TP top ↔ side wall top edges | recessed | −1 to −2 |
| A-WH inner face ↔ side wall | side by side | 1–2 |
| A-WH top ↔ chassis rear top | wheel lower | −4 |
| A-TAB top ↔ chassis top | proud | +8 to +10 |
| A-M ↔ A-DV / side wall | clamped | 0 |

---

## 6. Mechanism
- **Defiant**: 4WD skid steer, one N20 per wheel. No weapon. Pusher/wedge from both ends; invertible (wheels proud of both faces).
- **Alsoran**: 2WD skid steer from rear wheels; the front lip drags. No weapon. Pure wedge. Not invertible.
- **Dominant**: tracked pusher with a front wedge.
- **Cluster tactics**: the robots act together. One wedges under the opponent while the other pushes it, or one acts as a decoy. Losing one robot does not end the fight (cluster rules count robots).

---

## 7. Assembly order (suggested rebuild)

**Defiant**
1. Print D-CH (bars, side lugs, central body with motor cradles and lid bosses, floor) in one piece.
2. Fit 4 N20 motors in the cradles with shafts out through the central body walls into the notches.
3. Press the 4 wheels on.
4. Fit the PCB, battery, switch and wiring in the central body.
5. Screw on the clear lid (2 screws). Apply the smiley sticker and the name label.
6. Slide the clear lip sheets into the bottom of each bar and tape them with fibre tape.

**Alsoran**
1. Print A-CH (side walls, floor, divider, crossbar).
2. Fit the two N20 motors either side of the divider and clamp them.
3. Press the wheels on.
4. Fit the electronics and wires in the bay and under the top plate. Plug in A-TAB.
5. Screw the top plate on (6 screws). Apply the label.
6. Tape the clear lip under the front of the top plate (grey tape).

---

## 8. Hidden / uncertain list
- Lip attachment method and flexibility (both robots).
- Whether Defiant's lips reach the floor when inverted.
- Alsoran's top plate material (printed vs FR4) and its internal ledges.
- What A-TAB is (link vs switch).
- Exact electronics on both.
- Dominant: almost all detail.
- All dimensions ±15 %.

## 9. Coordinate frame (restated)
Each robot: origin on the floor at the centre of its own footprint, +X right, +Y forward, +Z up, mm. Defiant: chassis x ∈ [−50, 50], y ∈ [−48, 48], z ∈ [2, 18]; lips to y = ±62. Alsoran: chassis x ∈ [−37, 37], y ∈ [−36, 36], z ∈ [0, 24]; lip to y = +48; wheels at y = −26.

## 10. Profiles as math

**10.1 Defiant plan outline (XY).** Union of: bars |x| ≤ 50, 28 ≤ |y| ≤ 48; central body |x| ≤ 32, |y| ≤ 48; side lugs 44 ≤ |x| ≤ 50, 18 ≤ |y| ≤ 28. Notch void (open to the side): 32 < |x| ≤ 50, |y| < 18 (open middle), plus wheel pocket 32 < |x| < 44, 18 ≤ |y| < 28. Wheels: discs centred (±41, ±34, 10), r = 10, extruded along X from |x| 37 to 45.

**10.2 Defiant lip (YZ section).** Line from (y 48, z 2) to (y 62, z 0)… measured steeper in AWS69; use slope atan(2/14) ≈ 8° if rigid from the bar bottom, or a flexible strip lying almost flat. Rebuild value: from (48, 3) to (62, 0), 12°, thickness 1.

**10.3 Alsoran side wall (YZ).** Quadrilateral (y −36, z 0), (−36, 24), (+36, 6), (+36, 0). Top edge: z = 15 − 0.25·y.

**10.4 Alsoran top plate.** Plane z = 13.5 − 0.31·(y − 0) … simplified: from (y −26, z 22) to (y +28, z 5), i.e. z = 22 − 0.315·(y + 26); angle atan(0.315) = 17.5°. Plan outline: rectangle |x| ≤ 31, with rear corners chamfered: x + (−26 − y)… i.e. remove the triangles |x| > 25 and y < −20 + (|x| − 25).

**10.5 Alsoran lip.** Line from (y 36, z 4) to (y 48, z 0), 18°, 1 mm thick, |x| ≤ 39.

**10.6 Segmented tyre (both).** In polar form for the wheel's own disc: r(φ) = 7 + 3·[frac(9φ / 2π) < 0.85], i.e. 9 blocks of 3 mm height with 15 % gaps; hub disc r = 7 white; bore r = 1.5.

**10.7 Alsoran tab A-TAB.** Rectangle 8 × 12 in the XZ plane at y = −30, tilted 10° rearward about its base at z = 22.

## 11. Pixel-based measurements (AWS69 native, ±10 px)
- Alsoran: lip front edge x ≈ 70–1060 of 1450 crop (native ≈ 990 px across at the lip). Top plate width at its rear ≈ 760 native. Label ≈ 520 × 135 native. Wheel (right): ≈ 85 px wide × 140 px tall. Tab: ≈ 70 × 110 native.
- Defiant: front bar width ≈ 1250 native (1550→2800). Lid ≈ 720 × 520 native (foreshortened). Smiley sticker ≈ 520 native wide. Wheels ≈ 100 px wide edge-on. Lip ≈ 1310 native wide.

## 12. Several independent estimates

| Quantity | Method A (assumed class/scale) | Method B (label / sticker) | Method C (wheel width 8–9 mm) | Reconciled |
|---|---|---|---|---|
| Defiant width | ≤ 101.6 (cube) → 100 | sticker 50 mm ≈ 520 px → 10.4 px/mm; bar 1250 px → 120 (sticker is farther than the front bar, so this overestimates) | 100 px / 8 mm = 12.5 px/mm → 100 | **100** |
| Defiant height | thin, ~ wheel Ø 20 minus 2 → 16–18 | bar face ≈ 180 px at 12.5 px/mm → 14 (foreshortened by elevation) | — | **16** |
| Alsoran width | cluster share of a cube → 70–80 | label 40 mm ≈ 520 px → 13 px/mm; plate 760 → 58 (plate) → chassis 74 | wheel 85 px / 9 = 9.4 px/mm (farther, at rear) | **74** |
| Wheel Ø | N20 small wheel 20 | AWS69 Alsoran wheel 140 px tall / 13 px/mm ≈ 11 (heavily occluded) | AWS68 wheels look 1/5 of Defiant width → 20 | **20** |
| Alsoran rear height | 24 | wheel top (20) is below the rear top in AWS69 → >20 | side wall in AWS68 ≈ 1.2 × wheel Ø | **24** |

## 13. Consistency check
1. **Defiant's width from the sticker** overestimates because the sticker is further from the camera than the front bar. With a perspective factor of ≈ 0.83, 120 → 100. **Consistent with 100.**
2. **Alsoran's wheel diameter** from AWS69 is badly occluded (only the upper half shows above the side walls). AWS68 shows the left wheel whole and it matches Defiant's wheels. **Use Ø 20 for both.**
3. **Mass**: Defiant ≈ chassis 30 g + lid 6 g + 4 N20 40 g + wheels 6 g + electronics 10 g + battery 8 g ≈ 100 g. Alsoran ≈ chassis 14 g + plate 6 g + 2 N20 20 g + wheels 3 g + electronics/battery 12 g ≈ 55 g. Total ≈ 155 g, slightly over 150; the cluster may use lighter N20s or a shared smaller battery. **Roughly consistent**; trim the chassis infill in a rebuild.
4. **Defiant's lip angle**: a rigid lip from the bar bottom gives only about 8°, which looks too flat compared with AWS69 (it looks 15–20°). That means the lip leaves the bar about **4–5 mm above the floor**, i.e. the bar's bottom is chamfered or the lip is set into the bar face. **Reconciled: lip leaves the bar at z ≈ 4, 16° slope.**
5. **Alsoran's tab height**: the tab is the highest point; at 32 mm the robot still fits a cube. Consistent.

---

## 14. Why the designer did it (per part; adversarial lens first)

**Defiant**
- **H-shaped chassis with wheels in notches**
  - Attacks: the full-width bars at both ends take every frontal and rear hit. The wheels are tucked **inside** the outline, so a spinner or wedge meets the bar or the side lug first. The open middle notch is the weak spot: a side-on horizontal spinner can reach the wheel tread from the side through the 26 mm opening.
  - Getting under: the robot is only 16 mm tall with lips at both ends, so whichever end faces the opponent can get under. Being **reversible** means it never has to turn round.
  - Construction: one print, wheel pockets printed in. No separate guards or brackets.
- **Side lugs (guard-to-chassis)**: protect the wheel hubs and stop the wheel being stripped off its D-shaft by a side impact. Integral printing means no screws to shear.
- **Wheels proud of both faces**: invertible driving. Being flipped costs nothing.
- **4 × N20, one per wheel**: no transmission, maximum traction for pushing, and redundancy: if one motor dies the robot still drives.
- **Clear lid**: lets the team see the electronics (diagnosing damage, checking the LED) without removing screws. Polycarbonate is very tough for a 1 mm sheet and does not crack under impacts. Two screws are enough because the lid is recessed below the bar tops, so it is shielded from side hits.
- **Lips at both ends, fibre tape**: very thin edges get under opponents. Fibre tape stops the sheet splitting and gives a slick surface. Both ends lipped means getting under from either direction.
- **Stickers**: team identity and robot identification (cluster robots must be identifiable).

**Alsoran**
- **Wedge-shaped tub, sloped top plate**: a classic wedge. The opponent rides up the plate onto the high rear. The 18° slope is shallow enough to get under robots with low front edges.
- **Six-screw top plate**: the plate is the armour and the ramp. Six screws spread impact load and make it removable for access.
- **Exposed wheels**: saves weight (Alsoran is the light member of the cluster). The weak point is a side hit on the wheel. The designer relied on the wedge always facing the opponent.
- **Open rear bay**: access and weight saving; rear attacks can reach the motors and wires. In a cluster the other robot covers its rear.
- **Upright tab**: a removable power link is quick to pull for safety and can be grabbed with fingers. It also gives the marshals a visible on/off indication **(guess)**.
- **Lip with grey tape**: thin edge plus tape joint, as on Defiant.

**Dominant**
- **Tracks**: the most traction for pushing, and good at climbing over a low wedge edge. Tracks are taller than the chassis, so it is invertible.
- **Hex-lattice lid**: light, stiff, ventilated, and shows the electronics.
- **Grey wedge**: a metal or hard-sheet wedge edge that gets under opponents.

---

## 15. Unseen / inner parts (guesses with confidence)

| Robot | Part | Guess | Size (mm) | Position | Confidence |
|---|---|---|---|---|---|
| Defiant | battery | 1S/2S LiPo 150–200 mAh | 30 × 20 × 6 | right side of central body, x +16, y 0, z 6 | medium |
| Defiant | ESC/RX | combined 4-motor board or 2 dual ESCs + rx on the green PCB | 40 × 30 × 5 | left-centre, x −12, y 0, z 6 | medium |
| Defiant | switch | micro slide switch reached through the right wall | 8 × 4 × 4 | x +28, y 0, z 9 | low |
| Defiant | lid bosses | 2 printed bosses Ø 5 with M2 holes at the central body end walls | Ø 5 × 14 | (0, ±44) | medium |
| Defiant | bar pockets | weight-relief trough in each bar | 90 × 14 × 6 | top of each bar | medium |
| Alsoran | battery | 1S LiPo 150 mAh under the top plate | 30 × 18 × 6 | x 0, y +10, z 4 | medium |
| Alsoran | ESC/RX | dual ESC + rx under the top plate | 25 × 15 × 5 | x 0, y −5, z 5 | low |
| Alsoran | top plate ledges | 2 mm internal ledges along each side wall | 3 × 60 | inside walls | medium |
| Alsoran | link socket | 2-pin header in the divider into which A-TAB plugs | 5 × 3 | x 0, y −30, z 18 | low |
| Both | wheel fixing | press fit on the N20 D-shaft | — | — | medium |
| Both | wiring | battery → switch/link → ESC → motors; leads ≤ 40 mm | — | inside | medium |

**Photo coverage**: AWS69 gives good detail of both Alsoran and Defiant from the front. AWS68 adds the sides and Defiant's rear. AWS65 is too small for more than Dominant's overall look. Undersides are never shown.
