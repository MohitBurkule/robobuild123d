# Antomic: full rebuild description from reference photos

Source photos:
- `robots/antomic/reference/antomic.aws65.webp` (556 × 498 px): AWS 65. Uncut, on a wooden table, slightly blurred. Camera at the **front-left**, about 45° down. Shows the **yellow body with rounded top edges**, the black **"AntOmic"** logo on the left side, the **red lifter frame** with a **red rear plate** (screwed), and the **red trapezoid scoop** with 4 screws and a taped lower edge.
- `...aws67.webp` (1276 × 1432 px): AWS 67. Cut out onto white (a thin green line under the scoop is the cut-out halo / a green felt edge). Camera **almost straight down from above the front**, about 60–70° down. Best for the **plan layout**: red rear plate with 6 screws, the two red arm rails, the open centre window with a **red servo link** inside, the **scoop face with 4 screws**, the **angled side cheeks**, the **clear tape strip** and the **yellow wheels** bulging from the sides.
- `...aws68.webp` (670 × 660 px): AWS 68. Uncut, on a white surface. Camera at the **front-right**, about 35° down. Best for the **pivot**: a **yellow cross-tube** at the top rear with **steel bolts** through it, the **red arm ends** wrapped round it, a **red cross-bar** joining the arms, a **red servo horn** inside, black internals and yellow/red wires; and the **tall scoop** with a **wide taped band**.

Facts come from the photos; inferences are marked **(guess)**. Sizes are **estimates in mm** from the AWS limits (150 g, 101.6 mm cube) and the spec draft (body 85 × 80 × 40, two inboard wheels r 12, a scoop lifter with a frame). Ratios are against **W = body width ≈ 80 mm** (yellow shell, wheels excluded).

---

## 0. Coordinate system and naming

- **Origin O** = floor point (z = 0) under the centre of the yellow body footprint.
- **+X** = robot right, **+Y** = forward (toward the red scoop), **+Z** = up. mm. Side-profile angles from the floor.
- Body extents (reconciled §12): x ∈ [−40, +40], y ∈ [−40, +32], z ∈ [3, 40]. Scoop leading edge at y ≈ +50 on the floor. Wheels poke out of the sides to x ≈ ±43.

| ID | Part |
|---|---|
| SH | yellow body shell (tall box with rounded/chamfered top long edges) |
| SL-L, SL-R | side wheel wells (openings where the wheels bulge out) |
| LG | black "AntOmic" logo on the left side |
| PT | yellow pivot cross-tube at the top rear |
| PB | steel pivot bolts through PT (pan head + threaded ends) |
| LF | red lifter frame: rear cross-plate / cross-bar + two arm rails |
| RP | red rear cross-plate (AWS65/67) with screws |
| RB | red cross-bar (AWS68 version, no plate) |
| AR-L, AR-R | red arm rails (rear wrap-round ends to the scoop) |
| SC | red scoop: trapezoid face plate + two angled side cheeks |
| SCF | scoop face plate |
| SCC-L, SCC-R | scoop side cheeks (facets) |
| TS | clear tape strip / band along the scoop's lower edge |
| HW | servo window in the shell top (open centre) |
| HN | red servo horn / link visible inside |
| SV | lifter servo (hidden; black units seen inside) |
| WH-L, WH-R | yellow drive wheels in the side wells |
| S-x | screws: silver Torx/Phillips pan heads on shell and scoop, black on the rear plate centre |
| M-L, M-R, BAT, ESC, RX, SW | hidden motors and electronics; yellow/red wires seen |

---

## 1. Overall description in one paragraph

Antomic is a **tall, boxy two-wheel lifter** with a **bright yellow shell** and a **red lifting scoop**. The shell is about 80 mm wide, 72 mm long and 40 mm tall, with its long top edges **rounded/chamfered** like a loaf, flat sides carrying a black **"AntOmic"** logo, and a large opening in the top. Across the top rear of the shell runs a **yellow cross-tube** carrying **steel pivot bolts**, and around it hinge the rear ends of a **red U-shaped lifter frame**: two **red rails** run forward over the top of the shell either side of the opening and bend down over the front, where they carry a **big red scoop** that covers the whole front of the robot. The scoop is a **trapezoid face plate**, wider at the bottom, sloping steeply down to the floor, with two **angled side cheeks**, **four silver screws** in its face and a **clear tape strip** along its leading edge. Between the rails a **red servo horn** inside the shell pushes the frame up. In AWS65/67 a **red plate with six screws** closes the frame's rear; in AWS68 only a cross-bar is fitted. The **yellow wheels** are hidden in wells in the sides, bulging out just a few millimetres.

---

## 2. Part-by-part description

### 2.1 Body shell (SH)
- **Shape**: a box **80 mm wide × 72 mm long × 37 mm tall** (z 3 to 40). The two long top edges are **rounded/chamfered**: AWS65 shows a smooth curve of radius about **10 mm** from the side wall into the top; AWS68 shows it as a flat **45° chamfer facet** about 12 mm wide (a printed chamfer that reads as rounded at low resolution). The front and rear top edges are square.
- **Top**: a flat strip about 12 mm wide along each side (over the wheel wells), with the central part **open** (window HW) between the frame rails.
- **Side walls**: flat, yellow; AWS65 shows the black **"AntOmic"** logo (letters about 6 mm tall, with a stylised atom "O") on the left side, centred about mid-length and mid-height.
- **Screws**: **silver Torx/Phillips pan screws** (head Ø 5 mm, M3) along the top strips: AWS67 shows two on each side strip (front and rear: (310, 335) and (355, 100) on the robot left of the image; (1080, 175) and (1075, 410) on the right), fixing the top strips/lid to the walls, plus two at the rear corners near the pivot tube.
- **Colour/material**: bright **lemon-yellow PLA**, glossy, with diagonal top infill lines.

### 2.2 Wheel wells (SL) and wheels (WH)
- **Wheels**: **yellow printed wheels** (hub and tyre the same yellow, or a yellow TPU tyre), about **Ø 30 × 10 mm**, in wells in the side walls at mid-length. AWS67 shows the wheel bulging about **3 mm outside the shell** on both sides at y ≈ −5 (the yellow lumps at the image's left (200–260, 120–330) and right (1150–1220, 160–430)).
- **Positions**: centres at **x = ±37, y ≈ −6, z = 15**, bottoms at z = 0. The wheels do **not** reach the top (40), so the robot cannot drive inverted.
- **Spec**: two inboard wheels r 12 (Ø 24); the photo bulge suggests a slightly larger wheel **(see §13)**.

### 2.3 Pivot cross-tube (PT) and bolts (PB)
- **PT**: a **yellow cylinder**, **Ø 8 mm**, spanning the full width at the **top rear edge** of the shell (y ≈ −38, z ≈ 40), integral with the rear top edge (AWS68 shows it as a rounded yellow rail along the top rear).
- **PB**: **steel M3 bolts** through PT: AWS68 shows a **pan head** at the robot-right end (image left) and **threaded ends** sticking out about 5 mm where the red arm ends clamp onto the tube (two bolts from each end, or one long rod with nuts). A second **pan head** appears at the robot-left end (image upper right).
- **Function**: the **hinge axis** of the lifter frame (along X at y −38, z 40).

### 2.4 Lifter frame (LF): rails, rear plate / cross-bar
- **Arm rails AR-L/AR-R**: two red printed beams, **6 mm wide × 8 mm tall**, at x ≈ ±19 (outer faces ±22), running from the pivot tube forward along the top of the shell at z ≈ 40–48. At the rear each rail ends in a **hook/eye wrapped round PT** (AWS68). At the front of the shell each rail **bends down at about 60°** (the bend at y ≈ +26) and joins the top edge of the scoop. AWS68 shows **small embossed letters** (an "M"-like mark) on top of each rail near the cross-bar.
- **Rear plate RP (AWS65/67)**: a **red flat plate**, **50 mm wide × 18 mm long × 3 mm thick**, joining the two rails over the rear of the opening, with **6 screws**: **4 silver** at its corners and **2 black** on its centreline (AWS67: silver at (465, 125), (465, 210), (965, 160), (965, 255); black at (690, 110), (685, 240)). Its rear edge sits just in front of the pivot tube. The black centre screws probably fix the **servo horn link** to the plate **(guess)**.
- **Cross-bar RB (AWS68)**: instead of the plate, a **red square bar** (6 × 6 mm) joins the rails about 12 mm in front of the pivot, leaving the inside visible.
- **Frame width**: about **50 mm** between the rails' outer faces at the rear (the rails converge slightly to about 44 mm at the scoop in AWS67).

### 2.5 Scoop (SC: SCF, SCC-L, SCC-R)
- **Face plate SCF**: a red printed plate, **about 3 mm thick**, **trapezoid**: top edge about **54 mm wide**, bottom (leading) edge about **76 mm wide**, slope length about **44 mm**. It slopes from its top edge at about (y +30, z 40) down to the floor at y ≈ +50, i.e. about **63°** to the floor (steep). In AWS68 it covers the whole front of the shell.
- **Side cheeks SCC**: on each side the face folds back into a **narrow angled facet** (about 12 mm wide) at about 40° to the face, so in plan the scoop is a shallow 3-facet "dustpan"; the cheeks' bottom corners are **chamfered** (AWS67: the outline steps in at the lower corners).
- **Screws**: **4 silver Torx pan screws** (Ø 5 mm) in a trapezoid pattern on the face (AWS67: (405, 710), (925, 765), (380, 960), (885, 1015); AWS65: similar), fixing the face to the rails' front legs and an internal web **(guess)**. AWS68's version shows **no visible screws** on the face (a newer print fixed from behind).
- **Tape TS**: a **clear packing-tape strip**, about **14 mm** tall in AWS67 along the full leading edge (a rectangle with visible tape edges), and a **taller band** (about 22 mm, with a wavy top edge) in AWS68. The tape wraps under the edge.
- **Leading edge**: a straight edge resting on the floor; AWS67 shows a thin **green strip** under it (felt pad or the cut-out halo) **(uncertain)**.

### 2.6 Servo window (HW) and horn (HN)
- **HW**: the opening in the shell top between the frame rails, about **36 mm wide × 34 mm long** (y −20 to +14).
- **HN**: a **red printed servo horn / link**, about **6 mm wide × 22 mm long**, inside the window, pointing up and back from a servo output on the right of the centre (AWS68: red bar at (565–700, 360–620) in the zoom; AWS67: red bar at (600–650, 290–390)). Its top end bears on or links to the frame's rear plate / cross-bar.
- **Inside**: black components (servo bodies, two seen in AWS68: one left, one right), a **red/yellow/black wire bundle** (a servo lead) and a steel screw head on a black part.

---

## 3. Per-view descriptions

### 3.1 Top view (AWS67)
- A yellow rectangle 80 × 72 with wheel bulges at mid-length on both sides. A red "ladder": the rear plate (50 × 18) across the rear, two rails (6 wide) running forward, an open window between them showing the red horn, then the big red trapezoid scoop at the front (54 → 76 wide), with the clear tape strip along its leading edge at y ≈ +45 to +50.

### 3.2 Front view (AWS68 is close)
- Almost all red: the scoop face, trapezoid, tall (44 mm on the slope, 40 mm high), with a taped band at the bottom. Above it, the frame cross-bar and the rails rising to the pivot at the rear top; the yellow shell's chamfered top edges either side.

### 3.3 Left side view (AWS65)
- A yellow rectangle 72 × 37 with a rounded top edge, the "AntOmic" logo, a wheel bump at mid-length low down; at the front the red scoop slope from the top front down to the floor about 18 mm ahead of the shell; on top the red rail line from the rear pivot to the scoop.

### 3.4 Rear view (inferred)
- The yellow rear wall 80 × 37 with the pivot tube at the top edge (bolt heads at the ends); red rail ends wrapped round it.

### 3.5 Isometric (AWS65)
- A yellow loaf with a red dustpan hinged over its back.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| SH | box with rounded top edges | 80 × 72 × 37 | 1 × 0.9 × 0.46 | yellow PLA | — | 1 |
| PT | tube | Ø 8 × 80 | 0.1 | yellow | integral | 1 |
| PB | bolt | M3 × 20 (×2) | — | steel | thread into PT | 2 |
| AR | rail | 6 × 8 section, ~70 long + bend | 0.08 | red PLA | wrap PT; integral with SC | 2 |
| RP | plate | 50 × 18 × 3 | 0.63 × 0.23 | red | 6 screws | 1 (AWS65/67) |
| RB | bar | 44 × 6 × 6 | 0.55 | red | integral | 1 (AWS68) |
| SCF | trapezoid plate | 54/76 × 44 × 3 | 0.68/0.95 × 0.55 | red | 4 screws | 1 |
| SCC | side facet | 12 × 40 × 3 | 0.15 | red | integral | 2 |
| TS | tape | 76 × 14–22 | — | clear | adhesive | 1 |
| HN | horn/link | 6 × 22 × 3 | 0.28 | red | servo spline | 1 |
| WH | wheel | Ø 30 × 10 | 0.38 | yellow | motor shaft | 2 |
| LG | logo | 40 × 6 | 0.5 | black | printed/sticker | 1 |
| S-SH | pan screw | Ø 5 | 0.06 | silver | shell | 4–6 |
| S-SC | pan screw | Ø 5 | 0.06 | silver | scoop | 4 |

---

## 5. Contact / gap matrix (est. mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| SH bottom ↔ floor | clearance | 3 |
| WH bottom ↔ floor | contact | 0 |
| WH outer face ↔ SH side plane | outside | +3 |
| WH top ↔ SH top | well below | −10 |
| AR rear eyes ↔ PT | pinned (rotating) | 0 |
| PB ↔ PT | through | 0 |
| AR bottom ↔ SH top strips | above / resting | 0–2 |
| RP ↔ AR | screwed / integral | 0 |
| RP bottom ↔ SH top | above | 2–4 |
| HN tip ↔ RP underside | bearing / linked | 0 |
| SCF top edge ↔ SH front-top edge | in front, clear | 2–4 |
| SCF inner face ↔ SH front wall | clear (the scoop lifts away) | 3–15 (wedge gap) |
| SC leading edge ↔ floor | touching | 0 |
| SCC inner edges ↔ SH side walls | outside | 1–2 |
| TS ↔ SCF | stuck | 0 |

---

## 6. Mechanism

1. **Drive**: two wheels at mid-length in side wells, skid steer; the scoop's leading edge and the shell's rear bottom edge act as skids (the robot rocks slightly).
2. **Lifter**: a servo inside, under the frame's rear, pushes the frame's rear plate/cross-bar up via the red horn; the frame rotates about the top-rear pivot tube (axis X at y −38, z 40) and the scoop's leading edge rises. Lever: pivot to leading edge ≈ √(88² + 40²) ≈ 97 mm; the horn acts about 12–18 mm from the pivot, so a small horn movement gives a large scoop movement (fast, low force). A 30° frame rotation raises the scoop edge by about 50 mm and swings it back toward the robot, **tipping an opponent onto its back** over the shell.
3. **Self-righting**: when the robot lies on its back (resting on the frame and the rounded top edges), raising the frame pushes the floor and rolls the robot back **(guess)**.

---

## 7. Assembly order (suggested rebuild)

1. Print the yellow shell (walls, floor, wheel wells, rounded top edges, top strips with the window, and the pivot tube at the rear top edge).
2. Install the two drive gearmotors and wheels in the side wells.
3. Install the lifter servo (output under the frame's rear), battery, ESC, receiver and switch; route the wires below the top.
4. Screw the top strips (silver screws).
5. Print the red frame (rails + scoop in one piece, or rails screwed to the scoop with the 4 face screws) and the rear plate (or cross-bar).
6. Hook the rails' rear eyes round the pivot tube; insert the pivot bolts from each end.
7. Fit the servo horn so it bears on the rear plate; screw the plate on (6 screws, the 2 black ones into the horn link).
8. Tape the scoop's leading edge.

---

## 8. Hidden / uncertain list
- Servo count (AWS68 shows two black boxes inside: maybe two servos, or one servo + one ESC).
- Exact pivot construction (one rod or two bolts).
- Wheel size and whether it is TPU or PLA.
- Whether the scoop is integral with the rails.
- Underside and rear.
- All sizes ±15%.

---

## 9. Coordinate frame (restated)
- Origin under the shell centre, +X right, +Y forward, +Z up, mm.
- Shell x ∈ [−40, 40], y ∈ [−40, 32], z ∈ [3, 40]. Pivot axis (y −38, z 40) along X. Scoop top edge (y +30, z 40), leading edge (y +50, z 0). Wheels (±37, −6, 15).

## 10. Profiles as math

**10.1 Shell cross-section (XZ).** Rectangle x ∈ [−40, 40], z ∈ [3, 40] with the two top corners rounded: arcs of r 10 centred (±30, 30) from θ = 0° to 90° (right) and 90° to 180° (left). (AWS68's chamfer version: replace each arc by the line from (±40, 30) to (±30, 40).)

**10.2 Lifter frame side profile (YZ, rail top edge, closed).** Rear eye: circle r 6 about P = (−38, 40). Rail top from (−38, 46) to (+24, 48): z = 46 + 0.032·(y + 38). Front bend: arc centred (+24, 40), r 8, from θ = 90° to θ = 27° (down toward the front). Then the scoop face line from (+28, 44) to the leading edge (+50, 0): z = 44 − 2.0·(y − 28) (63.4°). Thickness 3 behind the line.
- Opened by α: rotate every point about P in the YZ plane, scoop moving up.

**10.3 Scoop face (in its own plane: u across, v along the slope from the top edge down).** Trapezoid with top edge u ∈ [−27, 27] at v = 0 and bottom edge u ∈ [−38, 38] at v = 49 (the slope length 44/sin 63.4° ≈ 49). Side cheeks: strips 12 wide along the two slanted sides, folded back by 40°. Lower-corner chamfers 6 × 6. Screw holes at (±18, 8) and (±19, 30). Tape: v ∈ [35, 49].

**10.4 Rear plate RP (plan).** Rectangle x ∈ [−25, 25], y ∈ [−34, −16]; screws at (±21, −30), (±21, −20), (0, −32), (0, −19).

**10.5 Wheel.** Circle r 15, width 10; tread plain.

## 11. Pixel-based measurements

**AWS67 (1276 × 1432, top-down):**
- Shell: x 200–1220 incl. wheel bulges; shell walls ≈ 250–1170 (≈ 920 px); top edge y ≈ 60; front of shell at y ≈ 640.
- Rear plate: x 425–1000, y 80–290. Rails: left x 400–480, right x 925–1000, from y 290 to 650.
- Scoop: top edge x 290–1050 at y 645; bottom edge x 120–1200 at y 1100–1160; tape y 1100–1260.
- Screws on the scoop: (405, 710), (925, 765), (380, 960), (885, 1015).
- Servo link in the window: (600–650, 290–390).

**AWS65 (556 × 498):** shell x 20–440; scoop x 205–530, y 160–465; rear plate (105–290, 30–160); logo (65–160, 220–260).

**AWS68 (670 × 660):** scoop face x 185–615, y 180–590; tape band y 390–590; pivot tube ends (110, 100) and (380, 45); horn (270–300, 140–200).

## 12. Several independent estimates of key sizes

| Quantity | Method A (spec/rules) | Method B (ratios) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Body width | 85 (spec, incl. wheels) | cube 101.6 | AWS67: shell 920 px; scoop bottom 1080 px → scoop 1.17 × shell | **80 shell, 86 over wheels** |
| Body length | 80 (spec, incl. scoop?) | 0.9 W = 72 | AWS67: shell length 580 px (foreshortened by the high view, × 1.1) → 0.69 × 920 → 0.69 × 80 × 1.1 ≈ 61–72 | **72** |
| Body height | 40 (spec) | 0.46 W = 37 | AWS68: shell side ≈ 0.45 of its width | **37 + top = 40** |
| Scoop width (bottom) | — | 0.95 W = 76 | AWS67: 1080/920 × 80 = 94?? (scoop nearer the camera) | **76** (fits inside the cube with the wheels) |
| Scoop slope | — | — | AWS65 side: about 60–65° | **63°** |
| Rail spacing | — | 0.55 W | AWS67: 600 px / 920 × 80 = 52 (outer) | **50** |
| Wheel Ø | 24 (r 12 spec) | 0.38 W = 30 | AWS67: bulge 210–270 px long / 11.5 px/mm → 18–23 (chord of a partly hidden wheel) | **28** |

## 13. Consistency check: conflicts and reconciliation
1. **Scoop width**: the top-down AWS67 makes the scoop look wider than the shell (near the camera); AWS68 (front) shows it about the shell's width with the side cheeks just outside. **Reconciled 76 at the bottom edge**, cheeks reaching ±40.
2. **Wheel size**: the spec's Ø 24 vs a visible bulge that suggests a larger wheel. A 28 mm wheel at z 14 fits the 37 mm walls. **Reconciled Ø 28** (z 14).
3. **Rear frame**: plate (AWS65/67) vs bar (AWS68): event variants; the plate version carries the 2 black screws that probably attach the servo link.
4. **Length**: spec 80 includes the scoop overhang; shell 72 + scoop reach 18 = 90 total, inside the cube.
5. **Pivot height**: the tube is at the top rear edge in AWS68; the rails lie along the top. Consistent.

---

## 14. Why the designer did it (per part, adversarial first)

- **Full-width red scoop on a rear-pivoted frame**
  - Fight: the scoop covers the **entire front**, so there is no gap for an opponent's wedge or forks; its leading edge on the floor (taped thin) gets **under** opponents, and the frame then lifts and tips them backward over the robot. Pivoting at the top rear gives the longest lever and makes the scoop's path an arc that both lifts and pulls the opponent toward the robot.
  - Against spinners: the steep 63° face presents a large, sloped, replaceable red face; a vertical spinner's hit pushes the scoop up and back about the pivot, letting it swing rather than transmitting the full blow into the servo (the servo horn just pushes, it is not hard-linked) **(guess)**.
  - Being got under: the scoop edge is printed plastic with tape, not steel; a sharp metal wedge can get under it, which is the main weakness. The tape band (enlarged in AWS68) makes the edge thinner.
- **Angled side cheeks**
  - Fight: they guide opponents hitting the corners toward the centre and protect the shell's front corners and wheels from side-on wedges.
- **Tall yellow shell with rounded top edges**
  - Fight: a tall shell gives room for the servo under the frame; the rounded long edges mean that when the robot is tipped onto its side it rolls rather than resting stable, helping it get back onto its wheels or onto its back where the frame can self-right. It also deflects spinner hits on the top corners.
  - Weak points: tall flat sides are targets for horizontal spinners; the wheels are tucked in wells to reduce that exposure.
- **Wheels in side wells**
  - Fight: buried wheels are hard to hit; only 3 mm protrudes. Mid-length placement lets the robot pivot on the spot.
  - Cost: the robot cannot drive inverted (wheels far below the top), so self-righting with the frame is essential.
- **Rear plate / cross-bar and red horn**
  - Construction: the plate ties the rails together (stiff frame) and gives the servo horn a flat pad to push on; the AWS68 bar saves weight.
- **Pivot tube with through bolts**
  - Construction: printed tube + steel bolts = a cheap, strong hinge; the frame comes off by removing two bolts.
- **Colours and logo**
  - Identity: yellow and red are high-visibility; the atom logo matches the name.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Lifter servo | 17–25 g high-torque servo (two black boxes seen; maybe two servos for torque) | 30 × 15 × 30 | x ±10, y −20, z 18, output along X near z 30 | medium |
| Drive motors | 2 × N20 gearmotors | 12 × 10 × 25 | x ±22, y −6, z 14 | medium |
| Battery | 2S 300–450 mAh LiPo | 45 × 18 × 12 | front of the shell, x 0, y +18, z 9 | medium |
| ESC | dual brushed ESC | 25 × 15 × 5 | x 0, y +5, z 6 | low |
| Receiver | micro receiver | 20 × 12 × 5 | x −20, y +18, z 20 | low |
| Switch | slide switch in the rear wall | 10 × 5 × 5 | (+20, −40, 20) | low |
| Wiring | yellow/red/black servo lead seen through the window; battery leads along the floor | — | — | medium |
| Scoop inner web | a printed rib behind the face joining the rails, carrying the 4 screws | 50 × 30 × 3 | behind SCF | low |
