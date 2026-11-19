# Upgraded for the Roboteers Pleasure: full rebuild description from reference photos

Source photos (slug `upgraded_for_the_roboteers_ple`, files named `upgraded_for_the_roboteers_pleasure.*`):
- `robots/upgraded_for_the_roboteers_ple/reference/upgraded_for_the_roboteers_pleasure.aws66.webp` (814 × 805 px, pit photo on a cream/yellow table). AWS 66. Seen from the **front-left, high, about 50–55° down**, the robot's front (the faceted, tape-covered plough) at the **lower left**, the rear at the **upper right**. The best photo of the **top**: the two raised top "pods", the central channel, the **white spur gear** with its teeth showing through the front, the **white arm** lying back over the top towards the rear, a **black hammer head made of anodised hex standoffs** on the arm tip, the **silver hex nut on the pivot bolt**, silver button screws, the **right rear wheel** in its wheel well.
- `robots/upgraded_for_the_roboteers_ple/reference/upgraded_for_the_roboteers_pleasure.aws67.webp` (1168 × 820 px, cut out onto white, blue-tinted). AWS 67. Seen from the **front, slightly right of centre, about 20–25° down**. The best photo of the **front face**: five-facet plough, four facets covered in clear tape, the "crown" shaped upper front wall, the **vertical slot** through which the gear teeth show, and the **arm standing nearly upright** with a **white T-shaped head**. It is the photo with a mask (`aws67_mask.png`), so it is the silhouette reference.
- `robots/upgraded_for_the_roboteers_ple/reference/upgraded_for_the_roboteers_pleasure.aws68.webp` (436 × 395 px, pit photo on a wooden table, soft). AWS 68. Seen from the **right side / above, about 45–50° down**, front to the **left**. Shows the **right side wall** with its slots, the right rear wheel in its well, the arm lying back with a **dog-legged white bar and T-head**, a **blue item on the pivot bolt end**, **white strips** along the plough facets and **battle damage** (chewed, melted top) on the left pod.

Everything stated as fact is read from these photos. Inferences are marked **(guess)** with a confidence. Dimensions are **estimates**. Scale anchors, in order of trust: (1) the AWS antweight limits, 150 g and a 101.6 mm cube (the robot looks like it fills the cube in plan); (2) the **M3 button-head screws** on the top (ISO 7380 head Ø 5.7 mm); (3) the **drive wheels** (black 3-spoke hubs with fine-ribbed black tyres, a common N20 wheel, Ø 28–32 mm); (4) the **M3 hex nut** on the pivot bolt (5.5 mm across flats). Reference length **W = body width over the side walls ≈ 92 mm**.

---

## 0. Coordinate system and naming

- **Origin O**: on the floor (z = 0) under the centre of the robot's plan footprint (halfway between the plough tip and the rear face, halfway between the side walls).
- **+X** = robot's right, **+Y** = forward (toward the plough), **+Z** = up; mm. Angles in the YZ plane are measured from +Y toward +Z unless stated.
- Envelope (arm at rest, lying back): x ∈ [−46, +46], y ∈ [−49, +50], z ∈ [0, 48]. The arm head overhangs the rear to about y −62 when at rest (see §13.3).

| ID | Part |
|---|---|
| CH | black printed chassis tub (one main print: floor, side walls, rear wall, internal cradles) |
| POD-L / POD-R | left / right raised top blocks ("pods"), the top surfaces with lengthwise and crosswise layer lines |
| CHN | central channel between the pods, housing the gear and the resting arm |
| FW | upper front wall with the "crown" (zig-zag) top edge |
| GH | gear housing peak in the front wall, with the vertical gear slot (GS) |
| PL | five-facet front plough (lower front band), facets PL-1..PL-5 from left to right |
| TP | clear tape (and white strips) on the plough facets |
| WW-L / WW-R | wheel wells at the rear corners, with the over-wheel ledges (WL) and the front wheel guards (WG) |
| WH-L / WH-R | drive wheels (black ribbed tyres, black 3-spoke "S" hubs, silver centre screw) |
| M-L / M-R | drive gearmotors (hidden) |
| MM | printed motor cradles / clamps (hidden) |
| GR | white printed spur gear (weapon output gear), axis along X |
| PB | pivot bolt (M3) with hex nut (NT) on the right |
| PN | weapon drive pinion (hidden) |
| WM | weapon motor (hidden, geared) |
| ARM | white arm: root clamp block (AC) + bar (AB) |
| AS | two silver screws clamping the arm root to the gear |
| HD-A | AWS66 head: black block + two black hex standoffs + 3 screws |
| HD-T | AWS67/68 head: white printed T-bar |
| BL | blue item on the pivot bolt end (AWS68) |
| S-T | silver M3 button-head top screws (4 seen) |
| SL | rectangular slots in the right side wall (switch / vents) |
| SW | power switch (hidden, guess in a side slot) |
| BAT, ESC, RX, WR | battery, ESCs, receiver, wires (hidden; a red wire glimpse in AWS66) |

---

## 1. Overall description in one paragraph

Upgraded for the Roboteers Pleasure is a **two-wheel, rear-drive wedge-and-hammer (overhead axe) antweight** printed almost entirely in **black PLA/PETG**. Its footprint is a near-square **about 92 mm wide and 99 mm long**: a box-like rear half with the two **drive wheels (Ø ≈ 30 mm)** sunk into **wheel wells at the rear corners**, and a front half that is wrapped in a **five-facet polygonal plough** that curves around the nose in plan like half a decagon. Each plough facet slopes down to the floor and four of the five are covered in **clear packing tape** (white strips show through in AWS68). Above the plough a **vertical front wall** rises to a **zig-zag "crown" edge**, and behind it the top is split into **two raised flat pods** (left and right, about 32 mm high) with a **narrow channel between them**. In the channel, just behind the front wall, a **white printed spur gear (Ø ≈ 30 mm)** turns on an **M3 pivot bolt** along X whose **hex nut** sits on the right pod's inner slope; its teeth show through a **vertical slot** in the front wall. A **white arm** is clamped to the gear's right face with **two screws** and lies back along the channel and over the rear when at rest; it carries a **hammer head**: two **black anodised hex standoffs** in a black block (AWS66) or a **white printed T-bar** (AWS67/68). A hidden motor turns the gear through a pinion, swinging the arm up and over forward to strike whatever the plough has scooped up in front.

---

## 2. Part-by-part description

### 2.1 Chassis tub (CH)
- **Shape**: an open-topped box, **92 mm wide (X) × about 82 mm long (Y, from the rear face at y −49 to where the plough begins at y +33 on the centreline) × 32 mm tall**, with the plough grown onto its front. Floor about 2 mm thick, at z 2–4 (ground clearance about 2 mm; the plough edge and the wheels touch the floor). Walls about **2.5–3 mm thick**.
- **Side walls**: flat, vertical, at x = ±43 to ±46. The **right side wall** (AWS68) shows, from front to rear:
  - a **vertical seam / slit** about 18 mm behind the plough's side facet, from z ≈ 6 to z ≈ 26: a **parting line between the plough part and the chassis** (they are separate prints, or the plough is a shell slid over the chassis) **(guess, medium)**;
  - a **rectangular slot** low down at the front, about **14 mm long × 2.5 mm tall**, at about (y +18 → +4, z 5): most likely the **power switch slot** or a **vent / zip-tie slot** **(guess, medium)**. AWS66 shows a similar, longer **slot about 20 × 2 mm** on the right side just in front of the wheel guard at about (y −14 → −34, z 4);
  - the **wheel well** at the rear (2.6).
- **Rear wall**: flat, vertical, at y = −49, full width; not photographed directly. The rear top edges of the pods are square with small chamfers.
- **Print**: heavy **layer lines** about 0.25–0.3 mm. On the side walls they run horizontally (the tub was printed upright, floor down).
- **Colour**: matt black, chalky with white dust and scuffs (AWS68).

### 2.2 Pods (POD-L, POD-R) and channel (CHN)
- **POD-R**: a flat-topped block on the right half, top at **z = 32**, spanning **x ≈ +9 to +46** and **y ≈ −49 to +18** (rear part full width to the side wall). Its **front face is a slope** that runs down from the top edge at y ≈ +18 to the front wall crest (z ≈ 22) at y ≈ +26, i.e. about **50° from horizontal**, and its **inner (left) face** next to the channel is also chamfered at about 45° near the front, where the **pivot nut** sits (AWS66). The top shows strong **layer lines running across (along X)** in AWS66/68 and **along Y** in AWS67: either the top is a separate **lid** reprinted in a different orientation between events or the lighting deceives; treat the top as a **separate lid plate about 2.5 mm thick** (guess, medium) held by the **S-T screws**.
  - **Screws on POD-R**: **two silver M3 button heads** near the rear-right corner: one at about (x +40, y −36, z 32) right above the wheel and one at (x +22, y −40, z 32). AWS68 shows the same two at the rear edge above the wheel.
- **POD-L**: mirror block on the left half, x ≈ −46 to −9, the same height. In AWS66 its **front face is a large single slope** running forward-down to the plough's left facets, and its rear-left corner shows **two silver screws** (≈ (−22, −40, 32) and (−40, −36, 32)). In AWS68 the **left pod's top is damaged**: the rear edge is chewed and melted into a ragged, fibrous lump (impact or saw damage) near the screw at the rear-left.
- **Channel CHN**: the gap between the pods, about **16–18 mm wide** at the front (x ≈ −7 to +9, slightly right of centre) and **narrowing to about 12 mm** behind the gear, running from the gear to the rear edge. Floor of the channel about **z 18–20**, i.e. 12–14 mm below the pod tops, so that the arm (about 8 mm deep) lies **below or flush with the pod tops** when at rest. The channel side walls are vertical; AWS66 shows a **black inner wall with an opening** (dark slot about 12 × 6 mm at about (x +9, y −5, z 22)) behind the arm clamp, through which a **red wire** is glimpsed: the pod is hollow and holds electronics.

### 2.3 Upper front wall (FW) and gear housing (GH)
- **Shape**: a vertical wall about **3 mm thick** across the full front, standing on top of the plough's rear edge (z ≈ 14) at y ≈ +26 to +33 (it follows the plough polygon, so it is also faceted in plan). Its **top edge is a zig-zag ("crown")** seen in AWS67, from left to right:
  - rises from the left side (z ≈ 26 at x −46) to a **peak** at x ≈ −38 (z ≈ 32, the front of POD-L);
  - drops in a straight line to a **valley** at x ≈ −20 (z ≈ 20);
  - rises to the **gear-housing peak GH**, a flat-topped tower about **14 mm wide at x ≈ −4 to +10, top z ≈ 32**;
  - drops to a **second valley** at x ≈ +16 (z ≈ 18);
  - rises again to the right front corner of POD-R, z ≈ 28 at x ≈ +40, and falls slightly to the right side.
  The valleys are where the pods' sloped front faces meet the wall; the crown edge is the line where the wall meets those slopes.
- **Gear slot GS**: a **vertical rectangular slot**, about **7 mm wide (X) × 24 mm tall (Z)**, centred at x ≈ +1, from z ≈ 9 to z ≈ 32, cut through the front of GH. The **white gear's teeth stick out through it** (AWS67 shows 9–10 teeth one above another, edge-on, as a ladder of white ridges). The teeth stand about 1–2 mm proud of the wall face, so the gear's front is the frontmost thing above the plough.
- **Purpose**: the tower and wall shield the gear's sides and the motor below from the front; the slot lets the gear be larger than the space inside.

### 2.4 Plough (PL-1..PL-5) and tape (TP)
- **Plan shape**: a **convex polygon of five flat facets** wrapping the front from the left side to the right side, approximating an arc. Bottom edges (on the floor) through the vertices, with arc centre C = (0, +5) and R = 45:
  - V0 = (−45, +5) → V1 = (−36.4, +31.5) → V2 = (−13.9, +47.8) → V3 = (+13.9, +47.8) → V4 = (+36.4, +31.5) → V5 = (+45, +5).
  - Facets: PL-1 left side (V0–V1), PL-2 front-left (V1–V2), PL-3 front-centre (V2–V3, 27.8 mm wide), PL-4 front-right (V3–V4), PL-5 right side (V4–V5). Each facet is about **28 mm long** along its bottom edge.
  - The plough's front-most point (centre of PL-3) is at y ≈ +48 to +50.
- **Elevation**: each facet is a **flat plane sloping up and back at about 50–55° from the floor**, from its floor edge to its top edge at **z ≈ 14**, which is about **10 mm** inboard (horizontally) of the floor edge. So the top edge is the same polygon scaled to R ≈ 35. In AWS67 the facets look steep (60°?) because the camera is low; in AWS66 they look shallower. **Reconciled: 52°.**
- **Leading edge**: the floor edge is **thin (≈ 1 mm)** and sits on the floor; in AWS66 it shows a slight lip.
- **Tape TP**: **clear packing tape** (glossy, wrinkled, with bubbles and frayed edges) is laid over **PL-1 to PL-4**, wrapping over the facets' top edges by a few mm and over the floor edge underneath. **PL-5 (right side) has no tape** in AWS66 and AWS67. Under the tape of PL-2 (AWS66) there are **white/grey marbled patches**, and AWS68 shows **white strips** along the bottom edges of the left facets: either **white tape / paper under the clear tape**, or a **thin sheet (polycarbonate, aluminium?) laid on the facets** (guess, low). The tape makes the faces slippery so opponents slide up onto the wedge and protects the print from cuts.
- **Joins**: the facets are separated by visible creases (sharp polygon edges, no fillets). The plough is a **single print** with the front wall, grown off the chassis front, or a separate shell (see the seam in 2.1) **(guess, medium)**.

### 2.5 Wheels (WH-L, WH-R)
- **Shape**: **Ø ≈ 30 mm × 10 mm wide**. **Tyre**: black rubber with **fine axial ribs** (knurl-like, about 1 mm pitch) around the tread, about 4 mm thick, square shoulders. **Hub**: black plastic, about Ø 22, with **three curved "S" spokes** separated by three **kidney-shaped windows** (the spokes swirl), and a **silver centre screw** (M2/M1.6 pan head on the shaft end, or the D-shaft's grub screw). This is the common "N20 wheel" sold with micro gearmotors.
- **Position**: centres at **(x ±37, y −35, z 15)**. Inner face at |x| = 32, outer face at |x| = 42: the outer face sits **2–4 mm inside the side wall line** (|x| = 46), so in plan the wheels do **not** stick out past the body. Bottom on the floor; top at z 30, 2 mm below the pod top.
- **Not invertible**: the pods stand higher than the wheels, so upside down the robot sits on its pods (needs the arm to self-right; see §6).

### 2.6 Wheel wells (WW), over-wheel ledges (WL) and front wheel guards (WG)
- **Well**: a box-shaped notch out of each rear-corner of the chassis, **open to the side and below**, about **36 mm long (y −53… −17) × 14 mm deep (x from ±46 to ±32) × 32 mm tall**. The wheel sits in it with its outer face recessed.
- **Over-wheel ledge WL**: the pod's top surface continues over the wheel as a **ledge about 3 mm thick**, at z 30–33, with its outer edge flush with the side wall (x ±46) and its rear edge flush with the rear face. Two of the S-T screws sit on this ledge (2.2). AWS66 shows the ledge's outer edge with a **notch where the tyre peeks out above** (the ledge is cut back to x ≈ +40 for the middle 18 mm, so the tyre's top is visible from above; at that point clearance to the tyre is ~1 mm).
- **Front wheel guard WG**: a **solid block** in front of each wheel, the forward end of the well, about **12 mm long × 12 mm wide × 16 mm tall** (AWS68: a black block below and ahead of the wheel, with the side slot just in front of it). It shields the tyre from the front and from horizontal spinners coming along the side.
- **Rear**: the well is **open at the rear** (the tyre's back is flush with or 1–2 mm proud of the rear face at y −49 → tyre rear at y −50). So the wheels can push off walls and drive when the robot backs into something.

### 2.7 Drive motors (M-L, M-R) and motor cradles (MM), hidden
- **Guess (high)**: **2 × N20 micro gearmotors** (12 × 10 × 25 mm gearbox + motor, 3 mm D-shaft), along X, at the rear, shafts outboard through the inner well walls (x ±32) into the hubs at z 15. The motors lie end to end across the rear, each in a **printed cradle** in the tub floor with a **clamp strap or the lid** holding it down. Motor bodies at x ±(8…32), y −35, z 10–20. The sibling robot "Refined for the Roboteers Pleasure" uses Pololu HPCB 50:1 motors; the same is likely here.

### 2.8 Weapon: gear (GR), pivot (PB, NT), pinion (PN), motor (WM)
- **Gear GR**: a **white printed spur gear**, **tip Ø ≈ 30 mm, about 6 mm thick (X)**, with **about 28 teeth** (module ≈ 1, AWS66 shows teeth about 3 mm apart along the rim and 2 mm tall). It turns about an axis along X at **(y +18, z 22)**, centred in X at **x ≈ +1** (gear faces at x −2 and +4). Only the front ≈ 140° of it is visible (through the slot in AWS67 and through the channel in AWS66); the rest is in the housing. Whether it is a **full gear or a sector** is not visible; a sector of ~200° would be enough for the arm's swing **(guess: full gear, medium)**.
- **Pivot bolt PB**: an **M3 bolt** along X through the channel walls and the gear's bore. On the **right**, the bolt's threaded end and an **M3 hex nut (silver, 5.5 AF, 2.4 thick)** stand on the inner sloped face of POD-R at about (x +10, y +18, z 22) (AWS66; the thread protrudes about 3 mm past the nut). In AWS68 the same spot shows a **blue item** (BL): a **blue nylon-insert lock nut, a blue silicone sleeve, or a blue wire loop through a cross-hole** **(guess: blue nylock nut or thread-lock, low)**. The bolt head is on the left side, hidden by POD-L.
- **Pinion PN (hidden)**: **guess (medium)**: a small spur pinion (≈ 8–10 teeth, Ø 10) under the gear at about (y +12, z 8), driven by WM. Ratio ≈ 3:1.
- **Weapon motor WM (hidden)**: **guess (medium)**: a **micro metal gearmotor (N20-size, high ratio such as 150:1–298:1)** or the guts of a **high-torque micro servo** lying along X under the gear/channel, in the front half of the tub between the plough and the drive motors, at about (x 0, y +10, z 8). A servo would explain the arm's rest position (always returns rearward). The sibling robot uses the same gear-plus-arm layout.

### 2.9 Arm (ARM: clamp AC + bar AB) and screws (AS)
- **Root clamp AC**: a **white rectangular block** about **34 mm long × 8 mm wide (X) × 9 mm tall**, lying against the **right face of the gear** (x +4 to +12), its front end at the gear's centre. It carries a **raised rib with a rectangular window** (about 14 × 3 mm) on its top/outer face (AWS66) — a lightening slot or the head of a nut trap. **Two silver M3 pan / button screws (AS)** pass through it into the gear: one near the gear centre (y +12) and one ~12 mm behind (y 0), both through the gear web, fixing arm to gear so they rotate together.
- **Bar AB**: from the clamp's rear end the arm continues as a **slender white bar**. Three variants are seen:
  - **AWS66**: a straight bar in line with the clamp, rising at ≈ **15° above horizontal toward the rear**, with a **cylindrical sleeve section** (Ø ≈ 8, 20 mm long, a printed round section or a white heat-shrink / tube over the bar) near its outer end. Total pivot-to-head-centre length ≈ **72 mm**.
  - **AWS68**: a **dog-legged** arm: the clamp lies flat (≈ 0–5°), then the bar **bends upward at about 35°** at the clamp's rear end and runs ≈ 45 mm to the head. Bar section ≈ **7 × 5 mm**, slightly tapering.
  - **AWS67**: the arm stands **nearly vertical**, slightly leaning back, with the T-head at the top at z ≈ 95 (the top of the frame).
- **Rest position**: lying back along the channel and over the rear, the head **behind and above the rear edge**. The arm's travel is from about **−165° (lying back) to about +0–20° (pointing forward/down onto the plough)**, i.e. about **180°** of swing, measured from +Y.

### 2.10 Hammer heads (HD-A, HD-T)
- **HD-A (AWS66)**: at the arm tip a **black anodised aluminium block** about **10 × 10 × 18 mm** (a square spacer / clamp block) with a **silver screw** through it, holding **two black hex standoffs** (M3 female-female, about **5.5 AF × 12–15 mm**) standing **perpendicular to the arm**, one on top of the other / side by side, with **silver socket / button screws** in their ends (3 screw heads visible: two at the standoff tops, one through the block). It is a **concentrated metal mass of ≈ 6–8 g** at the arm's end: a hammer weight.
- **HD-T (AWS67, AWS68)**: a **white printed T-bar** across the arm's end: about **30 mm long (X) × 6 mm (Z when at rest) × 8 mm**, with **flared ends** (the T's crossbar thickens toward the arm in a smooth fillet, r ≈ 6), giving a broad striking edge. In AWS67 the T is seen end-on at the top: two flat lobes either side of the bar, about 28 mm across. This is a **lighter, wider head** (printed, ≈ 3 g) for spreading the hit or for self-righting.

### 2.11 Screws (S-T, AS, PB) summary
- **S-T**: 4 × **M3 silver button heads** on the pod tops at the four rear corners (2 per pod), fixing the lids/pods to the chassis or into heat-set inserts **(guess)**.
- **AS**: 2 × silver M3 button heads through the arm clamp.
- **PB**: 1 × M3 bolt + nut (pivot).
- **HD-A**: 3 × silver screws in the hammer head.
- **Hidden (guess)**: 2–4 × M2/M3 screws holding the plough part to the chassis from below; motor clamp screws.

### 2.12 Switch, wires, electronics
- **SW**: not clearly visible. Best candidate: the **low rectangular slot in the right side wall** near the front (2.1), or the slot ahead of the right wheel guard; a slide switch reachable with a pin through it **(guess, medium)**.
- **Wires**: a **red wire** glimpsed through the opening on the channel wall behind the arm clamp (AWS66). No external wires.
- **Electronics (hidden)**: see §15.

---

## 3. Per-view descriptions

### 3.1 Top view (synthesised from AWS66/AWS68)
- A near-square black outline ~92 wide × 99 long. The rear ~60 % is a rectangle split down the middle by the channel, giving two flat pods with screw heads at their rear outer corners. At each rear corner the tyre's top peeks through a notch in the pod edge.
- The front ~40 % is the five-facet plough in plan (a half-decagon), its facets seen as trapezoids (floor edge outside, top edge 10 mm inside), four of them glossy with tape.
- Between the pods at the front, the white gear (seen edge-on as a 6 mm wide toothed strip, ~30 mm long) and the white arm lying back along the channel to the rear, its head (black standoffs or white T) beyond the rear edge.

### 3.2 Front view (AWS67)
- Bottom band: the plough facets as five quadrilaterals, the centre one widest (≈ 28 mm), the side ones foreshortened; tape glints on four.
- Above: the black front wall with its zig-zag top edge: left peak, valley, gear tower with the vertical white tooth ladder, valley, right shoulder.
- Above that: the pods' flat tops seen obliquely with layer lines, and the arm rising vertically from the gear tower to the white T at the top. The wheels are hidden behind the plough (they are inboard of the side walls).

### 3.3 Left / front-left view (AWS66)
- The plough's left facets in the foreground lower left, the left pod's large front slope, the channel with the gear and the nut on the right pod's chamfer, the arm going back to the black standoff head, the right rear wheel in its well at the lower right with the ledge and two screws above it, a slot in the right side ahead of the wheel.

### 3.4 Right side view (AWS68)
- A long flat black wall, about 66 mm from the plough's side facet to the rear face, 32 mm tall, with a vertical seam near the front, a low slot, and the wheel at the rear corner sunk in its well, its top just under the ledge. The plough's facets to the left with white strips. The arm rises from just behind the front wall to the right, dog-legged, to the white T above and beyond the rear.

### 3.5 Rear view (not photographed; inferred)
- Flat black rear face 92 × 32 with the two tyres' backs visible in the open wells at the corners (x ±32…±42), the channel notch at the top centre where the arm passes over, the arm head above.

### 3.6 Underside (not photographed; inferred)
- Flat floor, wheels at the rear corners, the plough's floor-edge polygon at the front; probably access holes / screw heads for the plough.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W = 92 | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| CH | open box with wells | 92 × 82 × 32 | 1 × 0.89 × 0.35 | black PLA/PETG | — | 1 |
| POD | flat-topped block / lid | 37 × 67 × 2.5 lid | 0.40 × 0.73 | black | 2 × M3 each | 2 |
| FW+GH | zig-zag wall + tower | 92 × 3 × 18; tower 14 wide | 1.0 | black | integral | 1 |
| PL | 5-facet plough | R 45 polygon, facets 28 × 18 slope | 0.98 | black + clear tape | integral / screws | 1 (5 facets) |
| WH | ribbed tyre, 3 S-spoke hub | Ø 30 × 10 | 0.33 × 0.11 | black, silver screw | N20 D-shaft | 2 |
| WG | guard block | 12 × 12 × 16 | 0.13 | black | integral | 2 |
| GR | spur gear, 28 T | Ø 30 × 6 | 0.33 | white PLA | on PB | 1 |
| PB + NT | bolt + nut | M3 × ~25 | — | steel, silver | — | 1 |
| AC | arm clamp block | 34 × 8 × 9 | 0.37 | white | 2 × M3 to GR | 1 |
| AB | bar | 7 × 5 × ~45 | — | white | integral with AC | 1 |
| HD-A | block + 2 standoffs | 10 × 10 × 18 + 2 × (5.5 AF × 14) | — | black anodised alu | 3 screws | 1 (AWS66) |
| HD-T | T-bar | 30 × 8 × 6 | 0.33 | white | integral | 1 (AWS67/68) |
| S-T | button screw | M3, head Ø 5.7 | — | silver | into chassis | 4 |
| TP | clear tape | facets PL-1..4 | — | clear / white | adhesive | — |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| PL floor edge ↔ floor | sliding contact | 0 |
| CH floor ↔ floor | above | 2 |
| WH bottom ↔ floor | contact | 0 |
| WH outer face ↔ side-wall line (x ±46) | recessed | 4 |
| WH inner face ↔ well inner wall | running clearance | 1 |
| WH top ↔ ledge WL underside | close | 1–2 (tyre visible through notch) |
| WH front ↔ guard WG | running clearance | 2 |
| WH rear ↔ rear face plane | proud | +1 |
| POD tops ↔ wheel top | pods higher | +2 |
| GR teeth ↔ GS slot sides | clearance | 0.5–1 each side |
| GR teeth ↔ FW face | proud | +1…+2 |
| GR bore ↔ PB | running fit | 0.1–0.2 |
| NT ↔ POD-R chamfer face | clamped | 0 |
| AC ↔ GR right face | screwed | 0 |
| AC ↔ POD-R channel wall | clearance | 1–2 |
| ARM (rest) ↔ channel floor | resting / near | 0–2 |
| HD (rest) ↔ rear edge | overhangs above | +10 behind, ~8 above |
| GR ↔ PN (hidden) | meshing | 0 |
| PL top edge ↔ FW bottom | joined | 0 |
| tape ↔ facets | stuck | 0 |
| S-T heads ↔ pod tops | seated (button heads stand 1.6 proud) | 0 |

---

## 6. Mechanism

1. **Wedge**: the five-facet plough meets opponents at any angle across ±70° of the nose. Its floor edge gets under them and the 52° facets lift them onto the front wall, presenting them to the arm. Tape lowers friction so they ride up rather than grip.
2. **Hammer / overhead axe**: the hidden motor turns the pinion → gear (≈ 3:1) → arm. From rest (lying back, head behind the robot) the arm swings **up and over forward through ≈ 160–180°**, bringing the head (standoffs or T) down on the opponent sitting on the plough, about **55–70 mm ahead of the pivot**, i.e. at y ≈ +65…+80 at full reach, or onto the plough top at y ≈ +40 when an opponent is not there. Then it swings back. Arm tip speed with a geared N20 is low (< 2 m/s): it is a **control / harassment hammer**, more a **flipper-style lever** than a high-energy axe. The heavier HD-A head adds momentum for hits; the T-head spreads the hit and acts as a **self-righting lever** (swinging the arm past the back when inverted pushes the robot over).
3. **Self-righting**: when upside down the robot rests on the pod tops (z 32 inverted) and the arm in its channel. Swinging the arm through its full range pushes off the floor behind or in front and rolls the robot back **(guess, medium)**.
4. **Drive**: 2WD rear-wheel skid steer, wheels at the rear corners; the plough edge is the front skid. Turning pivots about the rear axle, swinging the nose across the arena (good for wedge play).

---

## 7. Assembly order (suggested rebuild)

1. Print the **chassis tub** (with wells, wheel guards, motor cradles, gear housing/front wall and channel walls) and the **plough** (if separate), the **pod lids**, the **gear** and the **arm** (white), and the **T-head** if used.
2. Fit the **two drive gearmotors** into their cradles at the rear, shafts through the well walls; fit the **weapon gearmotor/servo** and **pinion** under the gear housing.
3. Place battery, ESCs, receiver and switch in the pods / front bay; route wires (one red wire runs up into the right pod near the arm).
4. Bolt the **plough** onto the chassis front (if separate; the seam on the right side).
5. Screw the **arm clamp** onto the **gear** with two M3 screws. Fit the **hammer head** (standoffs into the black block, or slide/print the T).
6. Insert the **gear + arm** into the channel, meshing it with the pinion; slide the **M3 pivot bolt** from the left through the channel walls and the gear; fit the **nut** (and blue lock/spacer) on the right.
7. Fit the **pod lids** and the **4 M3 button screws**.
8. Push the **wheels** onto the D-shafts and fix the centre screws.
9. Lay **clear tape** (with white strips) over the plough facets PL-1..PL-4.

---

## 8. Hidden / uncertain list
- Whether the arm is driven by a servo or a gearmotor; full gear vs sector; the pinion's position and ratio.
- The arm's exact rest angle (15° in AWS66, 0°/35° dog-leg in AWS68) and the travel limits.
- What is under the tape (sheet metal / polycarbonate / white tape).
- Whether the pods are separate lids and why the top layer lines change direction between photos.
- Position of the power switch.
- Left wheel details (only its top is glimpsed behind POD-L in AWS66).
- All dims ±15 %.

---

## 9. Coordinate frame (restated)
Origin on the floor under the centre of the plan footprint; +X right; +Y forward (plough); +Z up; mm. Gear/pivot axis: the line (y +18, z 22) along X, gear at x −2…+4. Wheels at (±37, −35, 15), Ø 30 × 10. Side walls |x| = 43…46. Rear face y = −49. Plough floor tip y ≈ +48…+50. Pod tops z = 32.

## 10. Profiles as math

**10.1 Plough plan polygon (floor edge).** Vertices V_k = C + R (cos φ_k, sin φ_k), C = (0, 5), R = 45, φ_k = 180° − 36°·k for k = 0…5. Top edge: same with R_top = R − 10/cos(18°) ≈ 34.5 at z = 14. Each facet k (between V_k and V_{k+1}) is the plane through the floor edge with outward normal n_k = (cos ψ_k · sin 52°, sin ψ_k · sin 52°, cos 52°), ψ_k = 162° − 36°·k (the facet's mid-angle). Height on facet: z = (R_floor,k − d) · tan 52° where d is the in-plan distance from C along ψ_k, clipped to z ≤ 14.

**10.2 Front wall crown edge (front view, z as a function of x, piecewise linear).** (−46, 26) → (−38, 32) → (−20, 20) → (−4, 32) → (+10, 32) → (+16, 18) → (+40, 28) → (+46, 26). Wall bottom at z = 14 (top edge of the plough). Gear slot: |x − 1| ≤ 3.5, 9 ≤ z ≤ 32.

**10.3 Pod front slopes.** POD-R front face: plane through (y +18, z 32) and (y +26, z 20), i.e. z = 32 − 1.5 (y − 18) for y ∈ [18, 26]; the inner corner chamfered 45° in X near the nut. POD-L front: one plane from (y +12, z 32) down to the plough top edge at z 14, slope ≈ 40°.

**10.4 Gear.** Pitch circle Ø 28 (m = 1, z = 28), tip Ø 30, root Ø 25.5, involute 20° pressure angle; thickness 6; bore Ø 3.2; hub boss Ø 10 on the right face under the clamp.

**10.5 Arm (in the arm's own frame, u along the arm from the pivot, v perpendicular in YZ).** Clamp: u ∈ [−4, 30], |v| ≤ 4.5, x ∈ [4, 12]. Bar: from u = 30 at angle β (AWS66 β = 0°, AWS68 β = +35° kink upward relative to the clamp) for 42 mm, section 7 × 5. Head HD-T at the end: a rectangle 30 (X) × 6 (along bar) × 8, with fillets r = 6 into the bar. Head HD-A: block 10 × 10 × 18 centred at u ≈ 72, plus two hex prisms 5.5 AF × 14 along the local v-direction.

**10.6 Wheel.** Tyre: annulus r ∈ [11, 15], width 10, with 90 axial ribs (1 mm pitch, 0.4 mm deep). Hub: disc r ≤ 11, with three kidney windows bounded by the spirals r(θ) = 4 + 7·(θ − θ_k)/100°, θ_k = 0°, 120°, 240°, window angular width 70°, spoke width 3.

**10.7 Rest arm pose.** Arm angle α measured from +Y in the YZ plane about (y +18, z 22): rest α ≈ 180° − 15° = 165° (AWS66), head centre at (y 18 + 72 cos 165°, z 22 + 72 sin 165°) = (y −52, z 41).

## 11. Pixel-based measurements
- **AWS66 (814 × 805)**: S-T screw head ≈ 22 px across → 3.9 px/mm at the pod top. Right wheel visible from x 650 to 790 (tyre outer face foreshortened), height ≈ 115 px (≈ 30 mm). Gear visible arc ≈ 120 px chord over ~140° → Ø ≈ 120/(2 sin 70°)/3.9 ≈ 16?? (the gear is lower and partly hidden; chord measured on visible teeth only, see §13). Pivot nut ≈ 25 px across corners → 6.4 mm (M3 nut 6.35 across corners ✔). Pivot → HD-A head centre ≈ 350 px along the image; the arm lies along the robot's axis, foreshortened by sin(55°) ≈ 0.82 → 350/3.9/0.82 ≈ 109?? (perspective: the head is nearer the camera's top, see §13).
- **AWS67 (1168 × 820)**: robot width over the plough ≈ 1050 px (x 80 → 1130). Gear slot ≈ 85 px wide × 210 px tall → 1 : 2.5. Arm bar ≈ 70 px wide. T-head ≈ 80 px across (end-on, foreshortened). Plough band height ≈ 200 px of the 570 px body height → 0.35. Crown peaks at y 150 (left) and 160–200 (gear tower), valleys at y 300 and 420.
- **AWS68 (436 × 395)**: wheel Ø ≈ 87 px, S-T screw head ≈ 15 px; side from plough side facet (x 140) to rear (x 333) ≈ 193 px; arm T-head ≈ 55 px long.

## 12. Several independent estimates

| Quantity | Method A (screw Ø 5.7) | Method B (wheel Ø 30) | Method C (cube 101.6 / W 92) | Reconciled |
|---|---|---|---|---|
| Wheel Ø | AWS68: 87/15 × 5.7 = 33 | assumed 30 | — | **30** (28–33) |
| Side length (plough side facet → rear) | 193/15 × 5.7 = 73 | 193/87 × 30 = 67 | — | **66–72** → body side 66 + facet |
| Overall length | — | 67 + plough ≈ 30 = 97 | ≤ 101.6 | **99** |
| Overall width | AWS67: 1050 px; arm bar 70 px = 7 mm → 105 (near-camera inflation) | — | ≤ 101.6, wheels inboard | **92** |
| Body height (pod top) | AWS68: 32 | AWS68: pod top ≈ 1.07 × wheel Ø = 32 | — | **32** |
| Plough top height | AWS67: band 0.35 × 32 = 11 (foreshortened) | — | — | **14** |
| Gear Ø | AWS67 slot 85 px / 1050 × 92 = 7.4 wide; tooth ladder 210 px → 18 mm visible of the Ø | AWS66: gear ≈ 0.95–1.0 × wheel | — | **30** |
| Arm length (pivot → head) | AWS68: ≈ 175 px /15 × 5.7 = 66 | AWS68: 175/87 × 30 = 60 | AWS67: arm top near z 95 → 95 − 22 = 73 | **≈ 70** |
| Pivot height | AWS67: gear tower top z 32 → pivot below it | AWS68: ~0.7 × wheel Ø above the wheel axle → 15 + 7 = 22 | — | **22** |

## 13. Consistency check
1. **Gear size**: the AWS66 chord method gave a too-small value because only teeth near the slot were counted. The gear spans the full slot height (24 mm visible) and continues into the housing, and it must reach from the pinion (low) to above the channel floor (z ≈ 18) with teeth; Ø 30 centred at z 22 spans z 7–37: **its top would stick 5 mm above the gear tower (z 32)**. AWS67 shows the white teeth rising to the top of the slot and slightly above the tower → the gear's top does protrude a few mm above the tower. **Consistent with Ø 30 at z 22.**
2. **Pivot vs arm clearance over the plough**: with the pivot at (y +18, z 22) and arm length 70, the head swings through y ≤ +88 at z 22 (pointing forward) — ahead of the plough tip (+50) by 38 mm and at mid-height: the hammer strikes an opponent sitting on the wedge. **Consistent.**
3. **Cube rule at rest**: arm at 165° puts the head at (y −52, z 41) → overall length −52…+50 = 102 mm (just over 101.6 by a hair) and with the head's own size (HD-A block 10 mm) → ≈ 107. Either the arm rests steeper (AWS68 kink: head at ≈ (y −40, z 55)), or the cube is measured with the arm upright as in AWS67 (length 99, height 22 + 70 + 4 = 96 < 101.6). **Reconciled: in the rest pose the head's rear is at y ≈ −55 to −62 (outside the cube), the robot fits the cube with the arm upright.**
4. **Wheel vs pod height**: wheel top z 30, pod z 32: AWS68 shows the ledge right above the tyre with no daylight. **Consistent.**
5. **Width**: plough polygon V0/V5 at x ±45; side walls ±46; wheels inboard (outer face ±42). AWS67 shows no wheel visible beyond the plough sides. **Consistent.**
6. **Mass**: chassis + plough + pods 50 g (black PLA, ~30 % infill), gear + arm 6 g, HD-A 7 g, two N20 + wheels 26 g, weapon gearmotor 12 g, battery 2S 300 mAh 18 g, dual ESC + weapon ESC 8 g, RX 3 g, switch 2 g, screws/bolts/nut 6 g, tape 3 g, wire 4 g → **≈ 145 g**. Under 150 g. **Consistent.**

---

## 14. Why the designer did it (per part; adversarial lens first)

- **Five-facet polygonal plough instead of a straight wedge**
  - Getting under: a curved/polygonal front presents an **edge to the floor at every approach angle**: a spinner or wedge coming in at 30–60° off the nose meets a facet roughly square to it, not a corner. Flat facets print and tape far more easily than a true curve.
  - Adversarial: horizontal spinners hitting the front corners **glance off** the angled side facets; there is no square corner to bite. The facets' steep 52° slope is a compromise: steep enough to stay strong and low enough to lift.
  - **Tape**: makes the faces slick so opponents ride up rather than catch, protects the PLA edge from chipping, and is quick to renew between fights. The untaped right-side facet suggests the tape was renewed only where it was worn.
- **Crown-shaped front wall above the plough**: makes the front tall where it needs to shield the gear and pods, and low (valleys) where opponents are meant to slide back toward the hammer's strike zone. It also stops opponents climbing the wedge and riding over the pods.
- **Gear teeth exposed through the front slot**: the gear is bigger than the housing so it gets a long lever on the arm, and the slot is the only way to fit it. Adversarially it is a weakness (a vertical spinner could chip teeth), but it is set back behind the plough's top edge and above it.
- **Raised pods with a central channel**: the channel lets the arm **rest below the top surface**, out of reach of horizontal spinners, and keeps the robot compact in height. The pods hold electronics either side and shield the arm's sides.
- **Arm clamp bolted to the gear (two screws)**: allows **swapping arms and heads** between events (standoff hammer at AWS66, T-head at AWS67/68), and the gear stays meshed while the arm is changed. Two screws resist the twisting load of a hit.
- **Standoff hammer head (HD-A)**: cheap, dense metal mass made from parts every roboteer owns; easy to add/remove to tune weight to 150 g.
- **T-head (HD-T)**: wide striking face to hit an opponent anywhere across the plough, and a long lever for **self-righting**; printed, so it breaks before the gear does.
- **Wheels sunk in rear-corner wells with ledges and front guards**: the wheels are the weak point against horizontal spinners; recessing them 4 mm inside the side line, roofing them with the ledge and blocking the front with a guard means only the tyre's bottom and back are exposed. Rear corners give the longest wheelbase to the plough tip, so the plough edge carries little weight and stays on the floor.
- **Wheels lower than the pods**: accepted because the arm self-rights; it lets the body be taller (room for the gear) without needing huge wheels.
- **Pivot bolt with nut (and blue lock)**: simple, replaceable axle; a nylock (blue) stops the nut backing off under vibration from hits.
- **Black prints with heavy layer lines**: fast, thick-layer, strong (more perimeters). Black hides scuffs.
- **Separate plough seam**: lets the plough be reprinted after damage without reprinting the whole chassis (AWS68 shows heavy battle wear).

---

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Drive motors | 2 × N20 50:1 HPCB gearmotor along X | 12 × 10 × 25 (+ shaft 9) | (±20, −35, 15) | high |
| Motor cradles | printed U-cradles in the floor, lid presses down | walls 2 | rear floor | medium |
| Weapon motor | N20 high-ratio (298:1) gearmotor or micro servo, along X | 12 × 10 × 34 / 23 × 12 × 25 | (0, +8, 8) | medium |
| Pinion | 9–10 T, m 1 | Ø 11 × 6 | on WM shaft at (x +1, y +8, z 9) | medium |
| Battery | 2S LiPo 300 mAh | 45 × 18 × 12 | under POD-L, (−24, −8, 10) | medium |
| Drive ESC | dual brushed (e.g. Malenki Nano / DasMikro) | 20 × 15 × 5 | under POD-R, (+24, −10, 12) | medium |
| Weapon ESC / servo board | brushed ESC or servo electronics | 15 × 10 × 4 | (+24, +10, 12) | low |
| Receiver | micro 2.4 GHz | 15 × 11 × 4 | (−24, +12, 14) | low |
| Switch | slide switch (12 × 4) on the floor/side behind the right side slot | 12 × 4 × 6 | (+42, +12, 5) | medium |
| Wires | battery → switch → ESCs → motors; red/black silicone 26 AWG | — | inside the pods | medium |
| Gear hub / bearing | the gear bore runs directly on the M3 bolt (no bearing) | Ø 3.2 bore | pivot | medium |
| Plough fasteners | 2–4 M3 screws from below into the chassis front | — | (±25, +28, 2) | low |
| Lid inserts | M3 heat-set inserts under the 4 S-T screws | Ø 4 × 5 | pod corners | medium |
