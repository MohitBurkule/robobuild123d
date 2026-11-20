# PLA-ST is a Perfectly Legitimate Choice of Material: full rebuild description from reference photos

Slug `pla_st_is_a_perfectly_legitima` (listed as `pla_st` in hard20). Three photos:
- `robots/pla_st_is_a_perfectly_legitima/reference/pla-st_is_a_perfectly_legitimate_choice_of_material.aws63.webp` (485 × 475 px): AWS 63. An uncut photo on a speckled grey table. The camera is **front-right and high**, about 50–55° down, looking along the robot's length from the front. All four wheels are visible. The wedge is **wrapped in grey duct tape**.
- `...aws65.webp` (680 × 478 px): AWS 65. An uncut photo on a wooden table. The camera is at the **front-left**, about 30–35° down, so the robot's **left side** faces the camera, with the front pointing to the image left. It is the best photo for the **arm's side profile**, the **left side towers** and the **mecanum hubs**. The wedge is bare, dented aluminium.
- `...aws67.webp` (1352 × 1232 px): AWS 67. Cut out by the wiki onto white; the green fringes are cut-out halo plus the green tint of the polycarbonate edges. The camera is **almost straight in front**, slightly to the robot's right, about 20–25° down. It is the best photo for the **wedge facets and screws**, the **arm front block** and the **rear pivot hub**.

Everything stated as fact is read from those photos. Anything inferred is marked **(guess)**. All dimensions are **estimates in mm**, scaled from the AWS antweight rules (150 g, must fit a 101.6 mm cube) and cross-checked against the earlier spec draft (body 95 × 104 × 28, which is slightly too long for the cube once the wedge is added; see §12). Ratios are given against **W = chassis frame width ≈ 88 mm** (outer faces of the printed side walls, without the polycarbonate skirts).

---

## 0. Coordinate system and naming

- **Origin O** = the floor point (z = 0) directly under the centre of the printed chassis footprint.
- **+X** = robot right, **+Y** = forward (toward the aluminium wedge), **+Z** = up. Units are mm. Side-profile angles are measured from the floor (+Y) in the YZ plane.
- **Front** = the wedge end. In AWS67 the front faces the camera, so the robot's right is on the image left. In AWS65 the front points to the image left and the **left side** faces the camera. In AWS63 the front points to the image bottom and the robot's right is on the image left/near side.
- Chassis extents (reconciled, §12): x ∈ [−44, +44], y ∈ [−44, +32], z ∈ [2, 26]. Wedge extends to y ≈ +56 on the floor. Arm top reaches z ≈ 46 at the rear.

| ID | Part |
|---|---|
| CH | grey PLA chassis frame (open cellular box) |
| CF | chassis floor / belly plate |
| WP-FL, WP-FR, WP-RL, WP-RR | four corner wheel pockets (cells of CH) |
| SPN | central spine (three centre cells: front, middle, rear) |
| TW-L, TW-R | mid-side towers (raised boxes between the front and rear wheel pockets) |
| RT | rear pivot block / rear pillars (two, left and right) |
| LID-x | clear polycarbonate lids: LID-FC (front centre), LID-MC (middle centre), LID-TL, LID-TR (towers), LID-RL, LID-RR (rear corners) |
| SK-L, SK-R | clear (green-edged) polycarbonate side skirts |
| FL-R | clear front-right polycarbonate flap (AWS65) |
| WH-FL, WH-FR, WH-RL, WH-RR | four mecanum wheels (printed hub + rollers) |
| HB-x | mecanum hubs (grey printed star/cog discs) |
| RO | mecanum rollers (about 9 per wheel, 36 total) |
| M-x | four N20-class gearmotors (one per wheel) |
| GR | exposed brass pinion / black spur gear at the front-left motor (AWS67) |
| AR-L, AR-R | arm rails (two grey printed beams) |
| AB-F | arm front block (U-channel with hatched centre and 2 screws) |
| AB-R | arm rear hoop / cross-bar |
| AL-L, AL-R | arm rear drop legs to the pivot |
| PV | pivot axle (along X at the rear) with hubs PH-L, PH-R |
| SV | lifter servo (hidden; guessed at the rear centre) |
| WD-C | wedge centre facet (aluminium sheet) |
| WD-L, WD-R | wedge side facets (bent back) |
| WDM | wedge mount bulkhead (printed, hidden) |
| S-WD | 4 silver Torx/Phillips pan screws in a 2 × 2 square on WD-C |
| H-WD | 2 open holes low on WD-C |
| S-AB | 2 silver Phillips screws on AB-F |
| S-LID | silver Phillips screws holding the lids (2–4 each) |
| S-SK | 2 silver screws per side skirt |
| BAT, RX, ESC, SW | battery, receiver, ESC board, switch |
| WR | visible wiring (red/black power, orange/red/brown servo lead, white/orange signal leads) |

---

## 1. Overall description in one paragraph

PLA-ST is a **four-wheel mecanum-drive lifter/wedge** whose whole structure is **dark slate-grey PLA** (hence the name). The chassis is an **open "egg-crate" box** about 88 mm wide, 76 mm long and 26 mm tall, divided into cells: four **corner pockets** each holding a **mecanum wheel** that bulges out of the sides and top, a **central spine** of three cells carrying the electronics, and two **taller mid-side towers** with clear lids. Most cells are closed by small **clear polycarbonate lids** held by silver Phillips screws, so the wiring (red/black power, orange-red-brown servo lead) is visible through them. Over the top runs a **twin-rail grey arm**: two slim parallel beams with a row of round holes, rising in a gentle **arch** from a **front block** just behind the wedge's top edge to a **rear hoop** about 46 mm high, where they drop down to a **transverse pivot** with round hubs at each side. The front is a **wide three-facet aluminium wedge** (flat centre facet, two side facets swept back about 30°) that slopes from about chassis-top height to the floor, held by **four screws in a square** with **two spare holes** below. Clear polycarbonate **side skirts** cover the wheel pockets' outer faces. The look is a "bulldozer with a roll bar": a wide, scratched silver blade at the front and a grey hooped spine on top.

---

## 2. Part-by-part description

### 2.1 Chassis frame (CH)
- **Shape**: an open-topped rectangular box, **88 mm wide (W) × 76 mm long (0.86 W) × 26 mm tall (0.30 W)** to the wall tops, with internal walls dividing it into cells. All corners are sharp (radius < 1 mm). The walls are about **2.5 mm** thick (0.03 W). Layer lines are horizontal at about 0.2 mm. Small bosses at the cell corners carry the lid screws.
- **Cell layout in plan** (x across, y along), read from AWS63 (top view) and AWS65:
  - **Corner wheel pockets WP**: four open-sided cells, each about **24 mm wide (X) × 26 mm long (Y)**, open to the outside so that the wheel can protrude. Front pockets span y ≈ +4 to +30, rear pockets y ≈ −42 to −16.
  - **Mid-side towers TW-L/TW-R** between the front and rear pockets on each side, y ≈ −16 to +4 (about **20 mm long × 22 mm wide**), standing **taller than the frame, up to z ≈ 34** (8 mm above the wall tops). AWS65 shows TW-L clearly as a square grey box with a clear lid and 2 screws; AWS67 shows both towers as **black** boxes (a reprinted or painted part at AWS67, or simply very dark grey in the cut-out lighting) **(guess)**.
  - **Central spine SPN**, about **36 mm wide** (x ≈ −18 to +18), running the full length. It is split into a front-centre cell (y ≈ +8 to +32), a middle cell (y ≈ −14 to +8) and a rear cell (y ≈ −44 to −14), separated by thin cross walls.
- **Front wall**: hidden behind the wedge in every photo. It must carry the wedge mount WDM **(guess)**.
- **Side walls**: the outer faces of the towers and the wheel-pocket edges. The polycarbonate skirts cover them.
- **Rear wall**: never seen squarely. AWS67 shows the rear pillars RT standing up at the rear corners of the spine.
- **Colour/material**: matt **slate/blue-grey PLA** (a cool grey with a slight blue tint, like the arm), visible infill hatching on the flat tops.

### 2.2 Chassis floor (CF), hidden
- **Guess**: a printed floor 1.5–2 mm thick, integral with the walls, at z = 2 to 3.5 (2 mm ground clearance). It has openings under the wheel pockets for the wheels. Confidence **medium** (the spec draft has a 1.5 mm skin).

### 2.3 Mid-side towers (TW-L, TW-R)
- **Shape**: rectangular boxes, **20 (Y) × 22 (X) × 32 (Z)** mm, sitting on the frame between the wheel pockets, flush with the chassis side planes. Each has a **clear polycarbonate lid** on top held by **2 silver Phillips screws** at diagonal corners (AWS65: screws at the near-front and far-rear corners of TW-L).
- **Contents**: TW-R (far side in AWS65, image left of the rails in AWS67) shows **red silicone battery leads and a red connector** through its lid, so it probably holds the **battery** (or one end of it). TW-L (near side in AWS65) shows a **silver metal-cased part with a small tab and a grey tube**, possibly the **power switch / link** or a **servo** **(guess)**.
- **Why at mid-side**: between the wheels there is unused volume that is just as tall as the wheels; putting the heavy parts there keeps the centre of gravity between the axles.

### 2.4 Clear lids (LID-x) and screws (S-LID)
- **Shape**: flat polycarbonate rectangles, **about 1 mm thick**, cut to each cell (for example LID-FC ≈ 34 × 24 mm; the rear-corner lids ≈ 26 × 24 mm, tower lids ≈ 22 × 20 mm). Edges are slightly cloudy and scratched; AWS67 shows the edges with a green tint.
- **Fasteners**: small **silver Phillips pan-head screws**, head Ø about **4 mm** (M2), 2–4 per lid, into printed corner bosses. In AWS67 there are screws visible at the top-left lid (2: front-left and rear-left corners), the top-right lid (3: one at each visible corner), the middle-left lid (1) and the middle-right lid (1).
- **Function**: closing the cells while allowing visual inspection of wiring and status LEDs. Polycarbonate does not shatter.

### 2.5 Side skirts (SK-L, SK-R) and front-right flap (FL-R)
- **SK-L/SK-R**: **flat clear polycarbonate plates**, about **1 mm thick**, **76 mm long × 28 mm tall**, screwed to the outer faces of the towers with **2 silver screws** each (AWS67: two silver screw heads on the left of the image, on the robot's right skirt, at z ≈ 20 and z ≈ 10). They cover the outer faces of the wheel pockets but stand off from the wheels by 1–3 mm. In AWS63 the skirt on the robot's right **flares outward toward the front**.
- **FL-R (AWS65)**: a separate small **clear flap**, about **25 × 25 mm**, angled outward and down in front of the right-front wheel like a small wedgelet. It is screwed to TW-L/front pocket with 1 screw (AWS65 shows a silver screw at about (850, 520) in the zoomed crop). A dark block (a spare part or the table) lies under it. It may have been bent out by a hit **(guess)**.
- **Function**: protect the exposed wheel rollers from side impacts, and stop the wheels catching on arena walls.

### 2.6 Mecanum wheels (WH-x), hubs (HB-x) and rollers (RO)
- **Overall**: **Ø 36 mm × 14 mm wide**. Four wheels, one per corner pocket. Wheel centres at **x = ±32, y = +17 (front) and y = −29 (rear), z = 18**. The wheel tops reach z ≈ 36 (about 10 mm above the wall tops; 1/3 of the wheel shows above the frame), and the bottoms are at z = 0.
- **Hub (HB)**: a **grey printed star/cog disc**. AWS65 shows **8 lobes** around a central round hub of about Ø 12 mm, with the space between lobes forming 8 notches. The disc is double: two parallel plates about 2 mm thick and 10 mm apart, each with 8 lobes, joined at the centre. Each lobe carries a hole for a **roller pin**.
- **Rollers (RO)**: **barrel-shaped** rollers about **Ø 7 mm at the middle, Ø 5 mm at the ends, 14 mm long**, set at **45°** to the wheel axle. The roller bodies are black/dark grey (TPU, or printed and sleeved with rubber/heat-shrink); the end caps are light grey printed parts. About **8–9 rollers per wheel**, so 32–36 in total. In AWS65 the near rollers clearly show a **dark middle band with lighter grey ends**.
- **Roller axis geometry**: each roller axis lies in a plane tangent to the wheel; its direction is (cos 45° along the wheel axle, sin 45° tangential). Front-left and rear-right wheels are one hand, front-right and rear-left the other, giving the standard X pattern when viewed from above **(guess for handedness)**.
- **Drive**: each hub is pressed onto the **D-shaft of an N20 gearmotor** lying transversely in the spine. AWS67 shows, inboard of the front-left (image right) wheel, a **brass shaft/pinion** and a **black spur gear** (about Ø 10 mm). This suggests either a geared N20 with its last stage exposed, or a short **external gear reduction** at that wheel **(guess)**.

### 2.7 Arm rails (AR-L, AR-R)
- **Shape**: two identical slim grey printed beams, **6 mm wide × 6 mm tall** in section. The outer faces are about **26 mm apart** (x = ±13) and the inner gap is about **14 mm**. Seen from above (AWS63) they are **straight and parallel**, running exactly along the centreline. Seen from the front (AWS67) they converge in perspective toward the rear.
- **Holes**: each rail has a row of **round Ø 2.5 mm holes** through its top face, about every **8–9 mm** (AWS67 shows 5 visible holes on each rail from the front block to the top of the arch). In AWS65 the holes are on the side faces too, so they may be cross holes for zip ties or lightening **(guess)**.
- **Surface**: one rail in AWS67 (robot left, image right) has a **ribbed/textured top**; it looks like exposed infill or a grip pattern. AWS65 shows a **dotted line along the side faces** of both rails, which is the same texture.
- **Side profile** (AWS65): from the front block AB-F at z ≈ 30, each rail rises in a **shallow straight slope (about 15°)** for most of its length to z ≈ 44 at y ≈ −30, then curves over a **rounded corner (R ≈ 8 mm)** into the rear hoop AB-R and drops down to the pivot. There is no intermediate support between the front block and the rear hoop; the rails pass **6–18 mm above the lids** (the gap increases toward the rear).

### 2.8 Arm front block (AB-F) and screws (S-AB)
- **Shape**: a grey printed **U-shaped block**, **26 mm wide (X) × 10 mm deep (Y) × 14 mm tall (Z)**. The two rails merge into its upper corners. Its front face shows a **hatched infill square** (about 10 × 10 mm) in the middle, where the top skin is missing or sanded, flanked by two **silver Phillips screws** (S-AB, head Ø about 5 mm, M2.5–M3) at x ≈ ±9, about 3 mm below the top.
- **Underside**: the **lower part is open**: the two side legs (each about 7 mm wide) drop about 8 mm below the cross-piece, forming a **U-channel** with an inverted-U window about 10 mm wide × 7 mm tall in the centre (AWS67).
- **Position**: centred on X, at **y ≈ +26 to +36, z ≈ 22 to 36**, directly **behind and above the wedge's top edge**. In AWS67 the block bottom legs sit on (or 0–2 mm above) the top edge of WD-C.
- **Fastening**: the two screws run **along Y** (their heads face forward), so they probably go through the block into the **wedge mount WDM** or into a bent-over lip of the wedge's top edge **(guess)**. If the arm is a moving lifter, the block is the lifting "forks" and the screws are the rail-to-block joint instead **(alternative)**.

### 2.9 Arm rear hoop (AB-R), drop legs (AL-L, AL-R) and pivot (PV, PH)
- **AB-R**: at the rear the rails meet a **transverse grey cross-bar**, **6 × 6 mm** in section, about **50 mm long (X)**, at **y ≈ −38, z ≈ 44–46**. It is the top of the "hoop" in AWS67 (the rails curve up and join it). In AWS65 the near end of the hoop is the highest point of the robot.
- **AL-L/AL-R**: from each end of the cross-bar a **vertical leg**, **8 mm wide (Y) × 6 mm thick (X) × about 20 mm tall**, drops down outside the rear spine cell to the pivot hub.
- **Pivot hubs PH**: a **grey cylinder**, about **Ø 10 mm × 8 mm long (X)**, at the bottom of each leg, at **x ≈ ±25, y ≈ −38, z ≈ 24**. AWS67 shows the robot's right hub with a **black hex nut** on its outer end (M3 nut, about 5.5 mm AF) and a grey hub body; on the robot's left there is a **black block with a small black screw**. AWS65 shows the left hub as a grey round boss with a dark screw head in the middle.
- **Pivot axle PV**: a steel bolt or rod **Ø 3 mm**, about **56 mm long**, running across the robot along X through both hubs and the rear pillars RT **(guess)**. The arm rotates about it.

### 2.10 Rear pillars (RT)
- **Shape**: two grey (left) / black (right, AWS67) printed **pillars**, about **10 × 10 mm in plan × 28 mm tall**, at the rear corners of the spine (x ≈ ±22, y ≈ −38). They rise above the frame to carry the pivot axle at z ≈ 24 **(guess for the internal hole)**.
- In AWS67 the right pillar is visible as a **black vertical block** behind the grey hub; on the left there is a smaller dark block with a black screw at (700, 130) px.

### 2.11 Lifter servo (SV), hidden
- **Guess**: a **micro or mini servo** (9–17 g class, about 23 × 12 × 28 mm), lying in the **rear spine cell**, with its output spline along X at the pivot height, driving one hub directly (the hub is the servo horn) or via a short link. Confidence **low–medium**. The alternative is that the arm is **not powered** but simply a **fixed roll hoop** bolted to the pillars; see §6 and §13.

### 2.12 Wedge (WD-C, WD-L, WD-R)
- **Material**: **aluminium sheet**, about **1.2–1.5 mm thick**. It is heavily scratched with random diagonal score marks (AWS67), dented at the lower right corner of the centre facet (AWS65) and with a **torn notch** at the top right corner (AWS67, near the image right end of the top edge). In AWS63 it is **wrapped in grey duct tape**, with screw heads showing through.
- **Plan shape**: a **three-facet chevron**. The centre facet WD-C is **flat, about 42 mm wide** (0.48 W). The side facets WD-L/WD-R are each about **30 mm wide** along the sheet and are **bent back by about 30°** in plan, so that the total width across the outer tips is about **100 mm** (1.14 W): the wedge is **wider than the chassis** and covers the front wheels.
- **Elevation**: the **top edge** is at **z ≈ 30** (slightly above the wall tops), at y ≈ +30 for the centre facet. The **leading edge** rests on the floor at **y ≈ +56**. So the sheet length down the slope is √(26² + 30²) ≈ 40 mm and the slope is **atan(30/26) ≈ 49°** to the floor. On the side facets the bend lines run from top to bottom; because of the sweep, the side facets' outer edges are about 12–15 mm further back than the centre (at y ≈ +44 on the floor).
- **Top edge profile (AWS67)**: the top edge is **not straight**: it rises from the outer tips (z ≈ 25) to the bend lines (z ≈ 30), then dips slightly toward the centre where the arm block sits. The lower edge is the floor line, with the side-facet lower corners chamfered upward (AWS67 shows the bottom outer corners cut at about 45°, about 10 mm).
- **Screws S-WD**: **4 silver pan-head screws** with Torx/cross recesses, head Ø about **5 mm** (M2.5–M3), in a **square pattern about 14 mm (X) × 12 mm (down the slope)** centred at x ≈ +2 on WD-C, about **12–24 mm below the top edge** (down the slope).
- **Holes H-WD**: **2 open round holes**, Ø about **3 mm**, about **10 mm below the lower screws**, about **14 mm apart**, slightly to the right of the screw pattern's centre. They look like holes for an earlier mounting position or for a lower tab of the mount **(guess)**.
- **Mount (WDM, hidden)**: a printed **wedge bulkhead** behind the plate, sloped at the same 49°, into which the 4 screws thread. It is presumably part of CH's front wall **(guess, medium)**.

### 2.13 Exposed gears (GR)
- AWS67 shows, just inboard of the front-left wheel (image right side at about (950, 590) px), a **brass shaft end** and a small **black spur gear** about **Ø 10 mm**. A matching brass part appears at the front-right (image left at (360, 590)). These are the **output stages** of the drive motors or a short spur reduction **(guess)**.

### 2.14 Electronics and wiring (WR), partly visible
- **Visible**: red and black silicone **battery leads** (about 20 AWG) looping under LID-FC and LID-MC; a **red XT-style connector** (about 10 × 8 mm) in the centre-left cell (AWS67 at (390, 400) px); a **three-wire servo lead** (orange/red/brown or orange/white/brown) under the front-centre lid; a **red PCB** (ESC or receiver, about 25 × 15 mm) with a white connector in the centre-rear cell (AWS65); fine **multi-colour leads** to the motors.
- **Guess**: a **2S LiPo** about 300 mAh, a **4-channel brushed ESC** (or two dual ESCs) for the four motors, a receiver, and a switch. See §15.

---

## 3. Per-view descriptions (for silhouette matching)

### 3.1 Top view (plan; from AWS63, synthesised)
- A grey rectangle, 88 × 76 mm, divided into a 3 × 3 grid: four corner wheel pockets (with mecanum wheels whose rollers make knobbly outlines at the corners), two mid-side towers, and a three-cell central spine.
- Down the centreline, two parallel grey rails (outer width 26) running from the front block at the wedge top to the rear hoop, which is a cross-bar about 50 mm long at the rear.
- In front, the wedge appears as a trapezoid: rear edge (top of the wedge) about 85 mm wide at y ≈ +30, front edge (floor) about 100 mm wide at y ≈ +44 to +56, with the centre facet 42 mm wide projecting further forward than the swept sides.
- Total plan footprint: about **100 mm wide × 100 mm long**.

### 3.2 Front view (AWS67)
- The bottom half is filled by the **wedge**: a wide scratched silver band about 100 mm wide and 30 mm tall, its centre facet flat to the camera and its side facets turning away. Four screws in a square and two holes below sit just right of centre.
- Above the wedge, in the middle, the **arm front block** (26 mm wide, two screws, hatched centre), with the two rails rising straight away from the camera to the hoop at the top of the image.
- Either side of the rails, the clear lids with red/orange wiring below; then the dark towers; then, at the outer edges, the **mecanum wheels** with their rollers showing above the wedge's ends; the skirts at the far left and right.
- At the top: the **rear hoop** (the highest part), the **right pivot hub** with its hex nut (image left of the rails) and the dark left pillar (image right).

### 3.3 Left side view (AWS65 is closest)
- A low grey box (76 long × 26 tall) with two mecanum wheels (Ø 36) at the front and rear corners, their lobes and rollers protruding above and beside the box. Between them the **tower TW-L**, 8 mm taller than the box, with a clear lid.
- Above: the **arm** rising from the front block (z ≈ 30) in a straight slope to the rear (z ≈ 44), curving down to the **pivot hub** at z ≈ 24 at the rear.
- In front: the **wedge** side facet sloping from z ≈ 30 down to the floor about 25 mm ahead of the box.
- The clear skirt covers the side, with 2 screws on the tower.

### 3.4 Rear view (not photographed; inferred)
- The rear wall 88 × 26, with the rear wheels at the corners, the two rear pillars, the **pivot hubs** at x ≈ ±25, z ≈ 24, and the **rear hoop** cross-bar spanning between the drop legs at z ≈ 44–46. Probably the switch is accessible here **(guess)**.

### 3.5 Isometric (front-right-top, the user's chosen view for AWS67: azimuth 60°, elevation 35°)
- A wide silver blade in front, a grey grid-box with four knobbly wheels, clear lids with red wires, and a slim grey hooped spine running from the blade top to the rear.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| CH | cellular open box | 88 × 76 × 26 | 1 × 0.86 × 0.30 | slate-grey PLA | — | 1 |
| CF | floor | 88 × 76 × 1.5 | — | grey PLA | integral (guess) | 1 |
| TW | box | 22 × 20 × 32 | 0.25 × 0.23 × 0.36 | grey (black at AWS67) | integral/screwed | 2 |
| RT | pillar | 10 × 10 × 28 | 0.11 | grey/black | integral (guess) | 2 |
| LID | flat plate | 22–34 × 20–26 × 1 | — | clear PC | 2–4 × M2 | 6–7 |
| SK | flat plate | 76 × 28 × 1 | 0.86 × 0.32 | clear PC, green edges | 2 screws | 2 |
| FL-R | flap | 25 × 25 × 1 | 0.28 | clear PC | 1 screw | 1 (AWS65) |
| WH | mecanum wheel | Ø 36 × 14 | 0.41 × 0.16 | grey hub, black rollers | press on D-shaft | 4 |
| RO | barrel roller | Ø 7 × 14 | 0.08 × 0.16 | black + grey caps | pinned | ~36 |
| AR | rail | 6 × 6 section, ~80 long | 0.07 | grey PLA | integral with AB-F/AB-R | 2 |
| AB-F | U-block | 26 × 10 × 14 | 0.30 × 0.11 × 0.16 | grey PLA | 2 silver screws | 1 |
| AB-R | cross-bar | 50 × 6 × 6 | 0.57 | grey PLA | integral | 1 |
| AL | drop leg | 8 × 6 × 20 | — | grey PLA | integral | 2 |
| PH | hub | Ø 10 × 8 | 0.11 | grey + black nut | on PV | 2 |
| PV | axle | Ø 3 × 56 | — | steel | nut each end | 1 |
| WD-C | flat facet | 42 × 40 × 1.3 | 0.48 × 0.45 | aluminium (taped at AWS63) | 4 screws | 1 |
| WD-L/R | swept facet | 30 × 38 × 1.3 | 0.34 | aluminium | bent from same sheet | 2 |
| S-WD | pan screw | head Ø 5 | 0.06 | silver | into WDM | 4 |
| S-AB | pan screw | head Ø 5 | 0.06 | silver | AB-F | 2 |
| S-LID | pan screw | head Ø 4 | 0.05 | silver | into bosses | ~16 |
| M | N20 gearmotor | 12 × 10 × 25 | — | metal | pressed in pocket (guess) | 4 |
| SV | servo | 23 × 12 × 28 | — | — | rear cell (guess) | 0–1 |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| CH bottom ↔ floor | clearance | 2 |
| WH bottom ↔ floor | contact | 0 |
| WH top ↔ CH wall top plane | wheel above frame | +10 |
| WH top ↔ TW top | tower lower than wheel | −2 |
| WH outer face ↔ SK inner face | side by side | 1–3 |
| WH inner face ↔ spine wall | side by side | 2–3 |
| RO ↔ HB lobes | pinned | 0 |
| front WH tread ↔ WD inner face | near | 3–6 |
| LID ↔ cell wall tops | screwed | 0 |
| TW ↔ CH | integral | 0 |
| SK ↔ TW outer face | screwed | 0 |
| AR bottom ↔ LID-FC | above | 6 |
| AR bottom ↔ LID-MC / TW lids | above | 10–14 |
| AB-F legs bottom ↔ WD-C top edge | resting / just above | 0–2 |
| AB-F ↔ WDM | screwed (if fixed arm) | 0 |
| AB-R bottom ↔ rear spine lid | above | 14–16 |
| AL ↔ PH | integral | 0 |
| PH ↔ PV | concentric | 0 |
| PH inner face ↔ RT | side by side, bearing | 0–0.5 |
| WD-C ↔ WDM | screwed (4) | 0 |
| WD leading edge ↔ floor | touching | 0–0.5 |
| WD-L/R outer tips ↔ front WH | in front of wheel | 4–8 |
| M ↔ HB | D-shaft press | 0 |

---

## 6. Mechanism

1. **Drive**: four independent mecanum wheels give **holonomic drive**: forward/back, spin, and **strafing sideways** (all four wheels running with the left pair opposite to the right pair on one diagonal). Each N20 motor drives its own wheel. Mecanum drive is unusual in antweights; it lets the robot sidestep a charge and line up its wedge without turning **(design reading)**.
2. **Arm**: the twin rails are pinned at the **rear pivot PV** (transverse) and joined at the front to the block AB-F, which sits on the top edge of the wedge. Two readings:
   - **(a) Lifter**: a servo at the rear turns the pivot; the arm's front block lifts whatever has ridden up the wedge. The front block rises on an arc of radius ≈ √(68² + 8²) ≈ 68 mm about PV; a 25° servo stroke lifts it by about **29 mm**.
   - **(b) Fixed roll hoop / brace**: the arm is bolted at both ends and ties the wedge top to the rear pillars, forming a **truss** that stiffens the wedge against hits and lets the robot roll over when flipped.
   - The spec draft and robot_type say **lifter**; the rear hubs with a nut on one side and a dark block on the other match a **servo horn + idler bolt** pair. Reconciled: **(a) with low-medium confidence**.
3. **Wedge**: passive, screwed to the chassis front. It gets under opponents; the mecanum strafing lets it be aimed.

---

## 7. Assembly order (suggested rebuild)

1. Print **CH** in grey PLA with the floor, cell walls, corner pockets, towers, rear pillars, the wedge bulkhead WDM and screw bosses.
2. Press the **four N20 gearmotors** into the spine pockets, shafts out into the wheel pockets at z = 18.
3. Assemble the **mecanum wheels**: fit the rollers onto their pins between the hub flanges (about 9 per wheel, at 45°), then press the hubs onto the motor shafts. Check the X pattern.
4. Fit the **servo SV** in the rear cell with its spline at the pivot line (if a lifter).
5. Fit the battery (right tower), ESC and receiver (spine cells) and switch (left tower). Route all wires below the lid plane.
6. Screw the **clear lids** onto the cells.
7. Screw the **side skirts** to the towers; add the front-right flap.
8. Bend the **aluminium wedge** into three facets (two bends about 30°), drill the 4 holes, and screw it to WDM. Optionally wrap it in duct tape (AWS63).
9. Assemble the **arm** (rails, front block, rear hoop, drop legs printed as one part), slide the **pivot axle** through the hubs and pillars, nut it, and attach the servo horn.
10. Screw the **arm front block** (2 screws) down onto the wedge top (fixed) or set its rest position just above it (lifter).

---

## 8. Hidden / uncertain list
- Whether the arm moves. The hubs, the robot type and the spec say it does; the front screws into the wedge suggest it might not.
- Servo location and type.
- Mecanum roller count (8 vs 9 vs 10) and handedness.
- Whether the black boxes in AWS67 are the same towers as the grey ones in AWS65 (reprint) or different parts.
- Underside, rear wall, switch location.
- Wedge thickness, and whether it is one bent sheet or three separate plates.
- All mm values are scaled estimates (±15%).

---

## 9. Coordinate frame (restated)
- **Origin O** = the floor point under the centre of CH's footprint. **+X** right, **+Y** forward, **+Z** up, mm.
- CH: x ∈ [−44, +44], y ∈ [−44, +32], z ∈ [2, 26]. Towers to z = 34. Arm hoop top z = 46. Wedge floor edge y = +56 (centre) and +44 (outer corners). Wheel centres (±32, +17, 18) and (±32, −29, 18).

## 10. Profiles as math (for rebuilding curves)

**10.1 Arm rail top edge (YZ plane, x = ±10 to ±16).**
- Front block top P0 = (y +32, z 36). Front block front face at y = +36 from z = 22 to z = 36.
- Main slope from P1 = (+26, 34) to P2 = (−28, 46): z = 34 + 0.222·(26 − y) for y ∈ [−28, +26] (slope ≈ 12.5°).
- Rear corner: an arc centred C = (−36, 38), r = 8, from θ = 90° to θ = 180° (top to rear), then the rear face of the drop leg at y = −44 from z = 38 down to z = 20.
- Rail bottom edge: parallel to the top, 6 mm below.

**10.2 Pivot hub.** Circle r = 5 about (y −38, z 24), extruded along X from ±21 to ±29. Axle r = 1.5 on the same axis from x = −29 to +29. Hex nut AF 5.5, 2.4 thick, on the robot-right end (+X; image left in AWS67), from x = +29 to +31.

**10.3 Wedge centre facet (YZ section, x ∈ [−21, +21]).** A line from the top T = (y +30, z 30) to the leading edge L = (+56, 0): z = 30 − 1.154·(y − 30). Thickness 1.3 mm behind the line. Slope angle atan(30/26) = 49.1°.

**10.4 Wedge side facets (plan).** The bend line at x = ±21. The facet's plan direction makes 30° with the X axis, swept back: a point at distance s from the bend along the facet has x = ±(21 + s·cos 30°), y_shift = −s·sin 30°. With s ∈ [0, 32]: outer tip at x = ±48.7, shifted back 16 mm. Each facet keeps the same 49° slope in its own normal plane. Bottom outer corner chamfer: cut by the line through (s = 22, z = 0) and (s = 32, z = 10).

**10.5 Mecanum wheel.** Hub lobes: polar outline r(φ) = 10 + 5·max(0, cos(4φ))^0.5 (8 lobes, r from 10 to 15). Rollers: N = 9 barrels; roller k centred at radius 14.5, angle φ_k = 2πk/9, axis direction (in the wheel's frame with u = axle, t = tangent) d = (cos 45°)·u + (sin 45°)·t. Barrel profile along its own axis s ∈ [−7, +7]: radius ρ(s) = 3.5·√(1 − (s/9.5)²) (so ρ = 3.5 at the middle and 2.4 at the ends). The outer envelope of all rollers is a cylinder of radius 18.

**10.6 Front block AB-F (front elevation, XZ plane at y = +36).** Outer rectangle x ∈ [−13, +13], z ∈ [22, 36]; inverted-U window x ∈ [−5, +5], z ∈ [22, 29]. Hatched square x ∈ [−5, +5], z ∈ [29, 36] (surface only). Screw centres (±9, 33).

## 11. Pixel-based measurements (independent check)

**AWS67 (1352 × 1232, front view):**
- Wedge: left tip x ≈ 160, right tip x ≈ 1240 at the top edge (y ≈ 700–630); bottom edge y ≈ 1060–1150; centre facet x ≈ 500–1010 at the top edge.
- Screws S-WD: (668, 775), (835, 768), (690, 905), (850, 885). Holes H-WD: (690, 1045), (860, 1022).
- Front block AB-F: x 590–850, y 575–705; screws (632, 625) and (808, 610).
- Rails at the front block: left rail x 595–680, right rail x 770–850. At the top (y ≈ 50): x 430–640.
- Right pivot hub (robot right, image left): about (395, 150), Ø ≈ 75 px.
- Front-left wheel (image right): x 1000–1170, y 420–600. Front-right wheel (image left): x 190–330, y 480–700.

**AWS65 (680 × 478, left side):**
- Wedge: x 20–295 in the image, top at y ≈ 170 near the arm, bottom at y ≈ 440.
- Front-left wheel: x 290–420, y 270–380 (Ø ≈ 125 px in the ellipse's long axis). Rear-left wheel: x 530–660, y 175–330.
- Left tower: x 395–530, y 190–350.
- Arm: front block at about (175, 225); rail top at the rear (480, 55); pivot hub (590, 120).

**AWS63 (485 × 475, high front):**
- Wedge bottom edge: x 115–470; top edge x 130–440. Rails: from (270, 300) front to (180, 15) rear. Chassis frame: x 60–380.

## 12. Several independent estimates of key sizes

| Quantity | Method A (rules/spec) | Method B (ratios) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Chassis width | 95 (spec draft) | wedge 1.14 W must be ≤ 101.6 → W ≤ 89 | AWS67: frame between skirts ≈ 860 px at 11.0 px/mm → 78–88 | **88** |
| Chassis length | 104 (spec) | 4-in cube: 101.6 − wedge reach 24 = 77 | AWS63: frame 290 px long vs 320 px wide → 0.9 W = 79 | **76** |
| Chassis height | 28 (spec) | 0.30 W = 26 | AWS65: box side 105 px vs wheel 125 px × 36 mm → 30 incl. lid | **26 + 1 lid** |
| Wheel Ø | 22 (spec r 11) | 0.41 W = 36 | AWS67: 170–220 px / 11 = 15–20 (partly hidden) ; AWS65: wheel 125 px vs wedge 275 px × 40 → 18?? | **36** (see §13) |
| Wedge width | 100 (spec, box spans) | 1.14 W = 100 | AWS67: 1080 px / 11 → 98 | **100** |
| Wedge slope | 45° (spec) | — | AWS65: rise 270 px over run 250 px, foreshortened → 47–52° | **49°** |
| Arm rail c-c | — | 0.22 W = 19 | AWS67: 170 px at 11 px/mm → 16; rails' outer span 255 px → 23 | **20 c-c, 26 outer** |
| Arm hoop height | 45 (spec arm at z 19 + rail) | 0.52 W = 46 | AWS65: hoop 115 px above the tower lid, scale ~3.3 px/mm → 35 + 34 = 46?? approx | **46** |
| Screw square | — | 0.16 W = 14 | AWS67: 167 px / 11.5 = 14.5; vertical 130 px foreshortened by sin49 → 15 | **14 × 14** |

## 13. Consistency check: conflicts and reconciliation
1. **Cube limit vs spec length**: the spec draft's 104 mm body plus a 24 mm wedge would be 128 mm long, which fails the 101.6 mm cube. The photos show the wedge reaching about 0.3 of the chassis length ahead of it. **Reconciled: chassis 76 long + wedge to y = +56 → total ≈ 100 mm.**
2. **Wheel size**: the spec draft's r = 11 (Ø 22) is far too small: in AWS65 the mecanum wheels are almost as tall as the towers and clearly larger than half the chassis height. The pixel estimate in AWS67 is unreliable because the wedge hides the wheels' lower halves. Ratios to the tower and the frame give Ø 34–38. **Reconciled Ø 36**, with the wheel tops 10 mm above the wall tops (matching "a third of the wheel shows above the frame").
3. **Arm width**: the front block at 26 mm against a 42 mm centre facet is 0.62 of it; AWS67 pixels give 260 / 510 = 0.51. **Reconciled 26 mm outer** (block slightly wider than the rails, rails 20 c-c).
4. **Arm moving or fixed**: the rear hub/nut pair and the robot_type say "lifter"; the screws on the front block face forward into the wedge zone, which suggests it is fixed. A lifter whose front block is screwed to a wedge hinged at its lower edge would also work: the arm lifts the wedge top, tilting the whole wedge up into a steeper ramp. **Reconciled: lifter, pivot PV at (y −38, z 24), front block fixed to the wedge top, wedge pivoting with the arm** is not supported by any visible hinge at the wedge foot, so the most likely build is **arm lifts, wedge fixed** (low–medium confidence). Both are noted for the builder.
5. **Tower colour**: grey at AWS65, black at AWS67. Same geometry. **Reconciled: same parts; use grey, with black as the AWS67 variant.**
6. **Total height**: wheel top 36, hoop 46, so the hoop stands 10 mm above the wheels: when flipped, the robot rests on the hoop and the wheel tops do not touch the floor. If the arm is powered, it can **self-right** by pushing the hoop down. Consistent with the hoop being so tall.

---

## 14. Why the designer did it (per part, from several angles)

Common lens: **adversarial**. For each part: which attacks reach it (vertical spinners, horizontal spinners, enemy wedges and lifters, flippers, wall pins, inversion), how it survives, and how it helps win (getting under the opponent versus being got under, controlling the contact). Then construction reasons.

- **CH, a cellular PLA box ("PLA-ST")**
  - Fight: the name is a joke: PLA is brittle and normally a poor choice against spinners. The designer offsets this with **many small cells**: each internal wall is a stiffening rib, so a hit on one corner cracks one cell, not the whole body. The box is low (26 mm), so a vertical spinner's disc sees only a short wall and the wedge in front takes the first contact.
  - Weak points: square sharp corners give a horizontal spinner something to bite; PLA shatters in cold, so pieces may break off; the wheel pockets are open at the sides.
  - Construction: one print, no supports, cheap; cells make wiring tidy and parts easy to access with lids.
- **Corner wheel pockets with exposed mecanum wheels**
  - Fight: wheels at the corners maximise the turning moment and the stability footprint. Mecanum wheels let the robot **strafe**: against a straight-line rammer it can slide sideways and then turn the wedge back in, or approach a spinner at an angle it chooses. The rollers' rubber gives grip, but mecanum wheels **push poorly sideways** (lower traction than plain tyres), so in a shoving match the robot is weaker; the wedge must win the contact rather than the push.
  - Threats: the rollers are delicate and exposed at the corners. A horizontal spinner can strip rollers off. The skirts and the wedge's swept wings are there to protect them.
- **Wheels taller than the frame**
  - Fight: the wheel tops (z 36) are above the frame (26), so if inverted the robot rests on wheel tops and the hoop. Because the hoop is taller (46), inverted driving needs the arm to push the robot back over (self-righting) or the rollers to touch.
- **Mid-side towers (battery/switch)**
  - Fight: they put the heaviest mass between the axles and close to the floor, so the robot is hard to tip over from the front. Their walls also act as **side rams** that a sideways-hitting opponent meets before the wheels.
  - Construction: the towers are the only place tall enough for a battery pack beside the low spine.
- **Clear lids**
  - Fight: polycarbonate bends but does not shatter, which is why it is used for every top cover; a flipper or lifter landing on the robot hits flexible PC.
  - Construction: the operator can see wiring and LEDs without opening anything, and lids come off with two screws for repairs between fights.
- **Side skirts (PC)**
  - Fight: they keep opponents from catching the mecanum rollers and protect them from glancing side hits. The front flare (AWS63) and the separate front-right flap (AWS65) act as small **side wedgelets** to deflect an opponent arriving from the side downward rather than into the rollers.
  - Survival: thin PC deforms (AWS65's flap is visibly bent) and absorbs energy, then is replaced cheaply.
- **Wide three-facet aluminium wedge**
  - Fight: this is the main tool to **get under** opponents. Aluminium can be sharpened to a thin leading edge that rests on the floor, beating printed wedges. The facets: the flat centre aligns with the arm and is the lifting zone; the **swept side facets** deflect opponents coming at the corners toward the centre and cover the front wheels so they cannot be attacked from the front. Being wider than the chassis (100 vs 88 mm) means an opponent attacking the front corner meets the wedge, not a wheel.
  - Against spinners: a 49° slope deflects vertical spinner hits upward rather than taking them square; the scratches on AWS67 are exactly such glancing hits. The dent and torn corner show it is sacrificial.
  - Weak point: a steep 49° wedge is less good at getting under low wedges (which are typically 15–25°). The duct tape (AWS63) smooths the face so opponents slide up more easily and hides the screw heads.
  - Construction: one sheet bent twice, four screws; quick to replace or rebend between fights.
- **The two spare holes (H-WD)**
  - Construction: the plate has been re-mounted (moved up the slope) or flipped; the old holes remain **(guess)**.
- **Twin-rail arch arm**
  - Fight (lifter reading): once an opponent is on the wedge, the arm's front block lifts it at the wedge top, taking its wheels off the floor so it cannot drive away, while the mecanum drive pushes it to the wall. Two thin rails make a light but stiff frame. Holes reduce weight and let zip ties or wires pass.
  - Fight (roll-hoop reading): the hoop is the highest point, so if flipped the robot lands on the hoop, and the arm acts as a roll bar protecting the lids from overhead hammer and vertical spinner hits. It also braces the wedge top to the rear pillars so a frontal hit is carried through the arm to the rear of the chassis.
  - Threats: overhead weapons can hit the hoop; it is PLA and could snap at the rear corner (stress concentrator at R 8). The pivot hubs are on the outside and could be hit by horizontal spinners.
- **Rear pivot (PV) and hubs**
  - Fight: the longest possible lever (pivot at the back, lift at the front). Hubs on both sides share the load so the arm does not twist when lifting an off-centre opponent.
  - Construction: one steel axle with a nut on each end; easy to remove the whole arm.
- **Front block with hatched square**
  - Construction: the hatched square is where the top skin has been removed (or never printed) to save weight, or it is the print's infill exposed after sanding **(guess)**. The U-opening underneath gives clearance for the wedge mount's top edge or for wires.
- **Screws (silver, M2–M3)**
  - Construction: one size of silver pan screws everywhere for quick pit maintenance.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre, mm) | Confidence |
|---|---|---|---|---|
| Drive motors | 4 × N20 6 V gearmotors, 300–500 rpm, D-shaft 3 mm | 12 × 10 × 25 (+10 shaft) | lying across the spine, x ±14, y +17 and −29, z 18 | medium |
| Motor clamps | printed pockets in the spine walls, press fit | 13 × 11 × 26 | around each motor | medium |
| Spur gear stage | small exposed spur pair at the front-left (and front-right) | Ø 10, 4 wide | inboard of the front wheels, x ±22, y +17 | low |
| Lifter servo | 9–17 g servo, metal gear | 23 × 12 × 28 | rear spine cell, x 0, y −32, z 14, spline on +X at z 24 | low–medium |
| Battery | 2S LiPo 300–450 mAh | 45 × 18 × 12 or split across the right tower | right tower, x +33, y −6, z 16 | medium |
| ESC | 4-channel brushed ESC or 2 dual ESCs (red PCB seen) | 25 × 15 × 5 | rear-centre cell, x 0, y −18, z 6 | medium |
| Receiver | 2.4 GHz micro receiver | 20 × 12 × 5 | front-centre cell, x 0, y +20, z 6 | low |
| Switch / link | slide switch or removable link | 10 × 5 × 5 | left tower, x −33, y −6, z 22 | low |
| Wedge bulkhead WDM | printed 49° plate with 4 heat-set inserts or nuts | 42 × 40 × 3 | behind WD-C, y +34 to +54 | medium |
| Pivot bushings | holes in the rear pillars, maybe brass tube | Ø 3 bore | x ±22, y −38, z 24 | low |
| Corner bosses | Ø 5 printed posts with M2 pilot holes for the lid screws | Ø 5 × 24 | each cell corner | medium |
| Wiring | battery (right tower) → switch (left tower) via the middle cell → ESC (rear-centre) → four motor pairs; RX at front with servo lead to the rear; all under the lids | — | — | medium |

**Wiring path summary (guess)**: power runs across the middle cell under LID-MC (the red/black loops seen in AWS67), the signal leads (orange/white/brown) come forward to the receiver under LID-FC, and the motor leads drop into the wheel pockets beside the motors. Only the lids separate the wiring from the top, so the arm and the hoop are its main overhead protection.
