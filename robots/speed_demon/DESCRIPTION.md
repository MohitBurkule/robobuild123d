# Speed Demon: full rebuild description from reference photos

Source photos (all cut out onto white by the AWS wiki):
- `robots/speed_demon/reference/speed_demon.aws.71.webp`: AWS 71, 2562 × 1732 px, sharp. Front-left three-quarter view, about 30° down, robot turned about 35° to its left so the **front panel faces the lower left** and the **right side** is seen at the far right. This is the **white-framed, clear-skinned** version with **white gear-rim wheels and grey foam/rubber tyres**. A **red part** is visible through the top centre opening.
- `robots/speed_demon/reference/speed_demon.aws72.webp`: AWS 72, 1357 × 1006 px. Front-right three-quarter, about 35° down, front facing the lower right, **left side** visible at the left. This version has a **black printed frame**, a **green translucent left side guard**, **olive-green triple O-ring tyres** on black hubs, and a **silver/lilac foil front face**. The top skin is **battle-damaged**: two torn holes, one showing a **black spur gear** inside.
- `robots/speed_demon/reference/speed_demon.aws74.webp`: AWS 74, 1370 × 881 px. Front-left three-quarter, about 30° down. **White printed frame**, **white hubs with olive triple O-rings**, **clear polycarbonate side guards**, a **green flat base plate** that sticks out beyond the wheels, a **dark green square patch** on the top left, and a torn top opening showing a **black circuit board**.

Speed Demon is a **four-wheel, low, box-shaped pushing robot (a "rammer/wedge") with no active weapon**. All three photos are the same design in three liveries/repairs. Everything stated as fact below is read directly from the photos. Anything inferred is marked **(guess)**. All mm values are **estimates** (±15%), scaled from the AWS antweight size limit (fits a 101.6 mm cube) and from the wheel diameter. Ratios are given against **W = overall width across the side guards ≈ 100 mm**.

---

## 0. Coordinate system and naming

- **+X** = robot's right, **+Y** = forward (toward the decorated sloped front panel), **+Z** = up. **Origin** on the floor (z = 0) under the centre of the footprint (mid-width between the side guards, mid-length of the guards). Units mm. Side-profile angles are measured from +Y in the YZ plane; "slope" means angle from the floor.
- **Front** = the end with the face decal (eyes and zigzag teeth).
- **Left/right** are the robot's own. In AWS71 and AWS74 the robot's **left** side faces the camera's left/front; in AWS72 the robot's **left** side faces the camera's left (with the front at the lower right).

| ID | Part |
|---|---|
| BP | base plate (green, wider than the body, chamfered corners) |
| FR | printed inner frame (white at AWS71/74, black at AWS72): side rails, motor blocks, front/rear walls |
| FR-ML / FR-MR | motor blocks between the front and rear wheels, each side |
| FR-FC-L / FR-FC-R | front corner blocks (white, screwed through the guard) |
| FR-RW | rear wall (ribbed black at AWS72) |
| TS | top skin (clear polycarbonate with green/black "tiger stripe" decal) |
| TS-H | top centre opening / damage hole |
| TS-P | dark green square patch on the top left (AWS74) |
| FP | front panel (sloped clear polycarbonate with silver foil "demon face" decal) |
| FB | printed front wedge block behind FP (guess, partly seen) |
| SG-L / SG-R | side guards (clear polycarbonate AWS71/74; green translucent AWS72) |
| WH-FL, WH-RL, WH-FR, WH-RR | four wheels |
| TY | tyres: 3 olive O-rings per wheel (AWS72/74), grey foam/rubber (AWS71) |
| AX | wheel axle nuts/screws on the outer hub faces |
| S-TS | small silver Torx/Phillips screws around the top skin |
| S-FP | 2–3 silver screws across the face decal |
| S-SG | silver screws through the side guards into the frame blocks |
| GR | black spur gear seen through the AWS72 hole |
| LK | red part seen through the AWS71 hole (power link/switch) |
| PCB | black circuit board seen through the AWS74 hole (receiver/ESC) |
| M-x, BAT, RX, ESC | drive motors, battery, receiver, ESCs (hidden, guess) |
| W | wires (one black wire seen along the AWS74 left rail) |

---

## 1. Overall description in one paragraph

Speed Demon is a **low, flat, square, four-wheel pusher** about **100 mm wide, 95 mm long and 32–35 mm tall**. Its body is a **printed frame** (white or black) clad in **thin clear polycarbonate sheet**. The **top skin** carries a **green-and-black tiger-stripe decal** and is held down by small silver screws around its edge. The **front** is a **full-width sloped panel** (about 45°) with a **silver foil "demon face" decal**: two angry black eyes with yellow-green irises and a row of black zigzag teeth. Three silver screws run through the teeth. The four wheels (about Ø 32 × 11 mm, white or black hubs with **three olive-green O-rings** as tyres, or grey foam in AWS71) sit in a **tunnel down each side**, two per side, between the body and a **flat side guard** that covers their outer faces. The side guards are rectangles with chamfered corners, the same height as the wheels. A **green base plate** sticks out under everything. The wheels are slightly taller than the body so it drives either way up. There is no weapon: it wins by **speed and pushing**, getting under opponents with the sloped front.

---

## 2. Part-by-part description

### 2.1 Base plate (BP)
- **Shape**: a flat sheet about **1.5–2 mm thick**, about **100 × 95 mm**, with **all four corners chamfered** at 45° (legs about 8–10 mm). Its outline is the same as the side guards in plan, so the base plate's long edges lie **under the side guards**.
- **Colour/material**: **bright green, slightly glossy**. It looks like **green FR4 (PCB laminate)** or green-tinted polycarbonate **(guess: FR4, medium)**. In AWS74 it is plainly seen from x = −50 to the left body wall and under both left wheels; its top face is flat and uniform.
- **Z**: z = 0 to 1.5 (or it may be raised 1–2 mm if the wheels protrude below it; the wheels must touch the floor, so the plate is **raised: z ≈ 2–3.5**, with the wheel bottoms 2 mm lower) **(guess)**.
- **Fastening**: the printed frame stands on it; screws from below **(guess)**.

### 2.2 Printed inner frame (FR)
- **Colour**: matte **white** (AWS71, AWS74) or **black** (AWS72). FDM print with visible layer lines.
- **Side rails**: along each side, inboard of the wheels, a **vertical wall about 3 mm thick and about 26 mm tall** runs the full length of the body. In AWS74 there is a **long dark slit** (a black line about 1 mm thick) running along the top of the left rail, under the top skin edge: either a **black wire** laid in a groove or simply the gap between rail and skin **(guess: gap, medium)**.
- **Motor blocks FR-ML/FR-MR**: between the front and rear wheels on each side, a **white rectangular block** about **22 mm long (Y) × 12 mm wide (X) × 18 mm tall**, standing out from the rail to the side guard. Its outer face shows a **rectangular pocket** (about 10 × 6 mm) at the top and a **silver Phillips pan screw** (M2.5/M3) that passes through the side guard into it. These blocks act as **side guard standoffs**, and probably also clamp the drive motors (two motors back to back inside each block, shafts out to the front and rear wheels) **(guess, medium)**. AWS71 shows the same white block on the right side, with a screw. AWS72's black version has a **lattice/ladder** pattern on the left (open rectangles) below the top skin.
- **Front corner blocks FR-FC**: at the bottom front corners, outboard of the front wheels, a **small white block** about **10 × 10 × 10 mm** with a silver screw through the side guard (AWS74, bottom left). This ties the lower front of the side guard to the frame.
- **Rear wall FR-RW**: AWS72 shows, at the rear right, a **black block with vertical ribs** (like a heat sink or grip texture), about 30 mm wide × 10 mm tall, between the rear wheels. It is probably the **rear bumper** with a ribbed face to grip opponents or the arena when pushing backward **(guess)**.
- **Height**: frame top at about **z = 28** (under the top skin).

### 2.3 Top skin (TS)
- **Shape**: a **clear polycarbonate sheet about 0.75–1 mm thick**, covering the whole top between the side rails (about **72 mm wide × 80 mm long**), slightly **domed or bent** along the centre so the centre is a little lower than the edges in AWS74 (two flat facets meeting at a shallow valley along y) **(guess, low)**.
- **Decal**: under or on the sheet, a **green-white foil print with black diagonal "tiger" stripes** radiating from the front toward the rear corners. In AWS74 the green is brighter and patchier; in AWS71 it is darker green; in AWS72 it is pale green-white with a frosted/crinkled foil look.
- **Screws S-TS**: small **silver Torx or Phillips pan/countersunk screws, M2, head Ø 3.5–4 mm**, along both side edges about every 25–30 mm: AWS71 shows about 6 (left edge at y ≈ +30, 0, −30; right edge similar), AWS72 shows about 5 (left front corner, left mid, rear left, right rear, right front), AWS74 about 6.
- **Centre opening TS-H**: in all three photos the centre of the top is open or torn:
  - **AWS71**: a **neat rectangular window** about **24 × 20 mm** at the centre front, through which a **red rectangular plastic part** (two red ribs, about 14 × 10 mm) and a **silver cylindrical part** (a motor can) are seen. The red part is most likely a **removable power link (red plug)** **(guess, high)**.
  - **AWS72**: an **irregular torn hole** about **30 × 22 mm** at the centre, showing a **black spur gear** (about Ø 12, 6 mm wide, 15–20 teeth) next to a black block, and a small **silver sphere** (a screw head or a bearing ball). A second **torn hole** about **14 × 8 mm** at the front-left of the top skin, at about (−22, +25). Both holes have curled, torn edges: **damage from spinner hits**.
  - **AWS74**: a torn opening about **30 × 22 mm** at the centre, showing a **black circuit board** (receiver/ESC) and a curled silver edge of foil.
- **Patch TS-P (AWS74)**: a **dark green square patch** about **26 × 24 mm** stuck on the top left at about (−18, +5): **gaffer tape or a hook-and-loop pad** covering an earlier hole **(guess, high)**.

### 2.4 Front panel (FP) and front block (FB)
- **Shape**: a **flat clear polycarbonate sheet about 1 mm thick**, about **96 mm wide** (nearly the full width between the outer faces of the side guards) and about **38 mm long along the slope**, forming a **sloped front** from the top skin's front edge (z ≈ 30, y ≈ +25) down to **near the floor** at y ≈ +48. The slope is about **45°** (35–50°). **Both top corners are chamfered** at 45° (legs about 10–12 mm), so the panel is a flat hexagon: in AWS72 and AWS74 the chamfers are clear on both ends.
- **Lower edge**: in AWS71 and AWS74 the bottom 6–8 mm of the panel looks **bent to a shallower angle** (a second fold near the floor, so it meets the floor at about 20–25°) **(guess, medium)**. In AWS72 the lower edge is hidden behind the lilac shadow.
- **Decal**: **silver/holographic foil** (lilac-tinted in AWS72) printed with:
  - two **angry eyes**: each a black half-disc (about 16 mm wide × 12 mm tall) under a black slanted brow bar, with a **yellow-green round iris** (Ø 7) and black pupil. The left eye is at about x = −25, the right at x = +22, both about 20 mm up the slope.
  - a **row of black zigzag teeth** (about 10 triangles, each 5 mm wide × 6 mm tall) across the middle of the panel from x ≈ −15 to +30, running slightly diagonally in AWS72.
  - **black stripe marks** on both chamfered corners (continuing the tiger stripes).
- **Screws S-FP**: **2–3 silver screws** across the teeth: AWS72 has **three Phillips pan heads** (head Ø 5 mm) in a diagonal row at x ≈ −12, +3, +18; AWS74 has three **Torx countersunk** in the same positions; AWS71 has one screw at the left eye's lower edge and one at the right eye plus one mid. They fasten the panel to a **printed front block FB** behind it.
- **FB (guess)**: a printed wedge-section block behind the panel, the full width between the front wheels, about **70 × 20 × 28 mm**, giving the panel a solid backing so it does not fold on impact. Edges of a white printed part are visible behind the AWS74 panel at its left end.

### 2.5 Side guards (SG-L, SG-R)
- **Shape**: flat plates, about **95 mm long × 32 mm tall × 1–1.5 mm thick**, outboard of the wheels at x = ±50. The **four corners are chamfered** (the lower ones about 8 mm, the upper ones about 5 mm), matching the base plate outline.
- **Material**: **clear polycarbonate** in AWS71 and AWS74 (wheels visible through it, edges catching light), **green translucent** polycarbonate/acrylic in AWS72.
- **Screws S-SG**: at least **two per side**: one into the motor block FR-ML (centre, z ≈ 15) and one into the front corner block (front-bottom, z ≈ 6). AWS72 shows two small silver screws on the green guard: at the front-centre and rear-centre.
- **Height**: the guard top is about level with the wheel tops (z ≈ 32–34); in AWS74 the top edge sits about 1 mm below the O-rings.

### 2.6 Wheels (WH) and tyres (TY)
- **Position**: two per side, in the tunnels between the frame rails (x ≈ ±35) and the side guards (x ≈ ±50). Axles along X at **y ≈ −28 (rear) and y ≈ +22 (front)**, axle height z ≈ 16. Gap between the front and rear tyres about 18 mm (occupied by the motor block).
- **Size**: about **Ø 32 mm**, **11 mm wide**.
- **AWS72/AWS74 hubs**: printed **white (AWS74)** or **black (AWS72)** discs with a flat outer face, a raised central boss and **a D-shaped or rectangular slot** for the motor shaft. AWS74 rear-left hub shows an **M3 nut and washer** on a threaded stub at the centre; the front-left hub shows a small hex grub/shaft end at the centre and a little slot.
- **Tyres**: **three olive-green O-rings** (cord about 3 mm, Ø 32 outer) side by side in grooves on the hub rim.
- **AWS71**: white printed hubs with a **toothed/gear-like rim** (front right, about 20 teeth), and the rear right wheel has a **grey foam or textured rubber** tread. These appear to be printed **TPU or foam tyres**.
- **Ground**: wheel bottoms are the lowest point (z = 0); wheel tops at about z = 32, i.e. **1–3 mm above the top skin**, so the robot can drive inverted.

### 2.7 Visible inner parts (GR, LK, PCB) and wires (W)
- **GR (AWS72)**: a black spur gear about **Ø 12 × 6 mm**, axis along X, under the torn hole at about (−2, −5, 15), next to a black rectangular part (a motor or gearbox housing). This suggests the drive uses **exposed spur gears**, e.g. a **motor with a printed or plastic gear driving a wheel shaft** **(guess, medium)**.
- **LK (AWS71)**: a red ribbed rectangle about **14 × 10 × 6 mm** under the window at about (+2, +12, 22): a **red removable power link** **(guess, high)**.
- **PCB (AWS74)**: a black board with components under the hole at about (+5, +5, 20): receiver/ESC combo **(guess, high)**.
- **W**: one black wire (or the rail gap) along the AWS74 left rail at z ≈ 26.

---

## 3. Per-view descriptions (for silhouette matching)

### 3.1 AWS71 (front-left, 30° down)
The front panel dominates the lower left as a wide flat silver hexagon with the face decal. The top skin, green with black stripes, slopes up and back to the upper right. At the upper left and right, the green base plate peeks out beyond the clear side guards. At the right edge the right side guard shows two wheels behind it: a white gear-rim wheel in front and a grey foam wheel behind, with a white motor block and a screw between them. The top window shows the red link.

### 3.2 AWS72 (front-right, 35° down)
The front panel at the lower right, lilac-silver with three Phillips screws through the teeth. The left green side guard at the far left, through which two black-hub wheels with olive O-rings are seen. The right wheels' O-rings show at the top right. The top skin pale green with stripes, two torn holes, a black gear visible. A ribbed black rear block at the top right.

### 3.3 AWS74 (front-left, 30° down)
The left side is fully exposed: green base plate under, white wheels with olive O-rings, white motor block with screw between them, white front corner block with screw, the clear side guard over everything. The front panel at the right with three Torx screws. A dark green square on the top left, a torn opening with black PCB at the top centre.

### 3.4 Top view (synthesised)
A square 100 × 95 with chamfered corners (base plate and side guards), a central body 72 wide, a sloped front band from y = +25 to +48, and the wheel tunnels down each side. A central opening about 25 × 20.

### 3.5 Side view (synthesised, left)
A chamfered rectangle (the side guard) 95 × 32, two wheel circles Ø 32 behind it, the base plate as a thin line at the bottom. The front panel's slope shows only as the front chamfer region beyond the guard (the panel is inside the guards).

### 3.6 Rear view (inferred)
A flat rear wall between the rear wheels with a ribbed bumper, the side guard edges at each side, the top skin edge at z ≈ 30.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| BP | chamfered plate | 100 × 95 × 1.5 | 1 × 0.95 | green FR4 (guess) | under frame | 1 |
| FR rails | wall | 3 × 90 × 26 | 0.9 L × 0.26 | white / black FDM | on BP | 2 |
| FR-M | block | 12 × 22 × 18 | 0.12 × 0.22 × 0.18 | same | integral | 2 |
| FR-FC | small block | 10 × 10 × 10 | 0.1 | same | screw through SG | 2 |
| FR-RW | ribbed block | 30 × 10 × 10 | 0.3 | black (72) | integral | 1 |
| TS | sheet | 72 × 80 × 1 | 0.72 × 0.8 | clear PC + stripe decal | ~6 × M2 silver | 1 |
| TS-H | hole/window | 24–30 × 20–22 | 0.25 | — | — | 1–2 |
| TS-P | patch | 26 × 24 | 0.26 | dark green tape | adhesive | 1 (74) |
| FP | sloped sheet | 96 × 38 × 1 | 0.96 × 0.38 | clear PC + foil face decal | 3 × silver screws | 1 |
| FB | wedge block | 70 × 20 × 28 | 0.7 | FDM (guess) | screws | 1 |
| SG | chamfered plate | 95 × 32 × 1.2 | 0.95 × 0.32 | clear PC / green | 2 screws each | 2 |
| WH | hub | Ø 32 × 11 | 0.32 × 0.11 | white / black FDM | motor shaft + nut | 4 |
| TY | O-ring | Ø 32 × 3 cord | — | olive rubber (72/74), grey foam (71) | grooves | 12 (3/wheel) |
| S-TS | pan/csk | head Ø 4 | — | silver | into frame | ~6 |
| S-FP | pan/csk | head Ø 5 | — | silver | into FB | 3 |
| S-SG | pan | head Ø 5 | — | silver | into blocks | 4 |
| GR | spur gear | Ø 12 × 6 | — | black | on shaft | ≥1 |
| LK | red link | 14 × 10 × 6 | — | red | plug | 1 |
| PCB | board | 25 × 20 × 5 | — | black | inside | 1 |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| FR ↔ BP | standing on, screwed | 0 |
| TS ↔ FR rail tops | screwed | 0 |
| TS front edge ↔ FP top edge | butt/overlap | 0–1 |
| FP ↔ FB | screwed (3) | 0 |
| FP bottom edge ↔ floor | near | 0–2 |
| FP side edges ↔ SG front edges | near | 1–3 |
| SG ↔ FR-M | screwed | 0 |
| SG ↔ FR-FC | screwed | 0 |
| SG bottom ↔ BP edge | resting on/over | 0 |
| SG inner face ↔ WH outer face | side by side | 1–2 |
| WH inner face ↔ FR rail | side by side | 1–2 |
| WH-F tyre ↔ FR-M front face | in front | 1–2 |
| WH-R tyre ↔ FR-M rear face | behind | 1–2 |
| WH-F tyre ↔ FP back | near | 2–4 |
| WH bottom ↔ floor | touching | 0 |
| WH top ↔ TS top | wheel above | +1–3 |
| WH top ↔ SG top | about level | 0–1 |
| BP bottom ↔ floor | clearance | 1.5–2.5 (guess) |
| GR ↔ motor shaft | mounted | 0 |
| LK ↔ socket in FR | plugged | 0 |

---

## 6. Mechanism

1. **Drive**: four-wheel skid steer. Either **four motors** (one per wheel, two back to back in each side block) or **two motors with a gear to both wheels on each side** (the AWS72 gear). **(guess: 4 × N20 high-rpm gearmotors, medium; geared 2-motor drive, low.)** The name and the 32 mm wheels point to **high-rpm motors** for speed.
2. **No weapon**. The sloped front panel is the "weapon": it gets under opponents so they lose traction, and the robot pushes them into walls/pits.
3. **Invertible**: wheel tops stick above the top skin, so it drives upside down. The front panel would then slope the wrong way (a blunt front) unless the lower fold gives some ramp.

---

## 7. Assembly order (suggested rebuild)

1. Cut the base plate BP (green FR4, chamfered).
2. Print the frame FR (rails, motor blocks, front/rear walls, front corner blocks), screw it to BP.
3. Fit the drive motors in the side blocks; fit wheel hubs on the shafts; fit three O-rings on each hub.
4. Fit the electronics (receiver/ESC board, battery) in the centre bay; fit the red power link socket under the top window.
5. Screw the front block FB on, then the front panel FP with three screws through the decal teeth.
6. Screw the top skin TS on (about 6 × M2) with the window over the link.
7. Screw the side guards SG on (2 screws each) into the motor blocks and the front corner blocks.
8. Apply decals (stripes on top and sides, face on the front).

---

## 8. Hidden / uncertain list
- Motor count and gearing (4 direct vs 2 geared).
- The front panel's exact lower edge (single slope vs two-stage).
- Base plate material and whether the wheels protrude through/below it.
- The rear.
- All mm ±15%.

---

## 9. Coordinate frame (restated)
- Origin on the floor under the centre of the footprint; +X right, +Y forward, +Z up, mm.
- Extents: x ∈ [−50, +50], y ∈ [−47, +48], z ∈ [0, 34]. Body (frame) x ∈ [−36, +36]. Wheel axes at y = −28 and +22, z = 16, x = ±43 (wheel centre plane).

## 10. Profiles as math (for rebuilding curves)

**10.1 Side guard outline (YZ plane, x = ±50).** Octagon:
P1 (y −47, z 8), P2 (−39, 0), P3 (+40, 0), P4 (+48, 8), P5 (+48, 28), P6 (+43, 33), P7 (−42, 33), P8 (−47, 28), back to P1. Lower chamfers 8 × 8, upper chamfers 5 × 5.

**10.2 Base plate outline (XY plane).** Rectangle x ∈ [−50, 50], y ∈ [−47, 48] with 45° chamfers of 9 mm at all corners: |x| + |y − 0.5| ≤ 89.5 in each corner region.

**10.3 Front panel side profile (YZ).** Two segments: upper from (y +25, z 30) to (y +43, z 8): slope atan(22/18) = **51°**; The simplest model is a single plane from (+25, 30) to (+48, 2), slope atan(28/23) = **51°**. If the two-stage fold is modelled, use upper 55° and lower 25°: (+25, 30) → (+41, 7) → (+48, 3.5).

**10.4 Front panel plan (XZ projected).** A flat hexagon: bottom edge x ∈ [−48, 48], full width up the slope until 11 mm from the top edge, then 45° chamfers of 11 × 11 at both top corners, so the top edge spans x ∈ [−37, 37].

**10.5 Wheels.** Circle (y − y0)² + (z − 16)² = 16², y0 ∈ {−28, +22}. O-ring grooves at x offsets −3.5, 0, +3.5 from the wheel centre plane, torus minor radius 1.5.

**10.6 Top skin.** Plane z = 30 ± 0.5 (with a 1° valley along x = 0 optional).

## 11. Pixel-based measurements (independent check)

- **AWS74** (1370 px wide): rear-left wheel vertical diameter ≈ **215 px**; front-left wheel ≈ **235 px** (nearer). Left side length from the front corner block (590, 790) to the rear plate tip (60, 330) ≈ **700 px** along an oblique. With wheel Ø 32 at ~225 px average: 700/225 × 32 ≈ **100 mm** (includes chamfers and perspective) → side length **95**.
- **AWS74** front panel width from the left chamfer (620, 420) to the right tip (1345, 500) ≈ **730 px**, nearer to the camera → **96–100 mm**. Consistent with nearly full width.
- **AWS74** top patch ≈ **190 × 120 px** → 26 × 17 (foreshortened) → **26 × 24**.
- **AWS72** (1357 px): front panel height along the slope (top edge 330 → bottom edge 900 at x ≈ 900) ≈ **400 px** projected; wheel ≈ **190 px** → 2.1 × 32 ≈ **67 mm**?! The panel is close to the camera and faces it, so its slope is seen near full length while the wheel is farther and foreshortened. Corrected (×0.6) → **38–42 mm**. **Use 38.**
- **AWS71** (2562 px, scaled 1400): front panel width ≈ **950 px**; right front wheel ≈ **190 px** → 5 × 32 = **160 mm**, impossible; the wheel is at the back right, far away and partly hidden (we see only its top half). Discard this one.
- **AWS72** screw head ≈ **30 px** vs wheel 190 → 0.16 × 32 = **5 mm** → M3 pan. Consistent with Phillips pan heads.

## 12. Several independent estimates of key sizes

| Quantity | Method A (rule / part class) | Method B (ratio) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Overall width | ≤ 101.6 | 1.0 W | AWS74 front ≈ 96–100 | **100** |
| Overall length | ≤ 101.6 | 0.95 W | AWS74 side ≈ 95–100 | **95** |
| Height | wheel Ø + 2 | 0.33 W | AWS74 guard ≈ 0.95 wheel Ø = 30 | **33** (wheel), body 30 |
| Wheel Ø | common 30–32 printed hubs with 3 O-rings | 0.32 W | 32 | **32** |
| Wheel width | 3 O-rings × 3 + flanges | 0.11 W | AWS74 ≈ 75 px / 225 × 32 = 11 | **11** |
| Front slope | wedges 30–50° | — | AWS72 apparent ≈ 50° | **45–51°** |
| Top window | access for link | — | 24 × 20 | **24 × 20** |
| Side guard thickness | 1–1.5 PC | — | edge glint ≈ 8 px → 1.2 | **1.2** |

## 13. Consistency check: conflicts and reconciliation
1. **Width**: 2 × (guard 1.2 + gap 1.5 + wheel 11 + gap 1.5 + rail 3) + bay = 36.4 + bay. With overall 100, the inner bay between the rails is about **64 mm**, the frame width 70. Consistent with the top skin width of 72 (overlapping the rails).
2. **Length**: wheel centres 50 apart, wheel Ø 32 → wheel span 82, plus guard overhang ~6 at each end → 94–95. Consistent. The front panel must then project **inside** the guard length: it runs from y = +25 to +48. The front wheels' front edge is at y = +38, so the panel's lower part is in front of the wheels and the upper part over them: the panel must clear the tyres by ≥ 2 mm → at y = +38, panel z ≈ 2 + 28 × (48 − 38)/23 = 14 ✓ (tyre top at z 32, but the tyre is outboard of the panel in X? No — the panel is 96 wide, spanning the wheel tunnels). **Conflict**: a 96-wide panel would hit the front tyres. **Reconciled**: the panel's ends are **in front of** the tyres; at x = ±43 the tyre front surface is at y = 22 + 16 = 38 at z = 16 and the panel there is at y = 25 + (30 − 16)/28 × 23 = 36.5. Too close: move the panel 4 mm forward: **top edge at y = +29, bottom at y = +50**, guards extended to y = +50. Final length **97**.
3. **Height of guards vs wheel tops**: wheels Ø 32 and guards 32–33 tall: consistent; inverted, the wheels touch first.
4. **AWS71 wheels**: different tyres (gear rim/foam). Same diameter by eye. Keep Ø 32.
5. **Spec says wedge/roller**: consistent with a pusher with a sloped front.

---

## 14. Why the designer did it (per part, from several angles)

Common lens: **adversarial**. For each part: what can attack it (spinners, wedges, lifters, flippers, wall slams, inversion), how it survives, and how it helps win. Then construction reasons.

- **Full-width sloped front panel (FP)**
  - Fight: the main tool. A wide slope catches opponents anywhere across the front and lifts their front edge, taking their wheels' grip; then the robot pushes them out. Polycarbonate flexes instead of cracking under spinner hits; the solid block FB behind stops it folding.
  - Weak points: a 1 mm sheet edge is not as low as a steel wedge, so a sharper opponent wedge gets under it. If inverted, the slope faces up: the robot becomes a blunt pusher.
  - Construction: one bent sheet, three screws, decals for character.
- **Clear polycarbonate skins (TS, SG, FP)**
  - Fight: PC is light and very tough; it absorbs hits by flexing. Damage (torn holes in AWS72/74) shows it does get cut, but the frame stays intact underneath.
  - Construction: cut with scissors/knife; decals printed on paper/foil behind the clear sheet are protected from scuffs.
- **Side guards (SG) covering the wheels**
  - Fight: protect the tyres and hubs from horizontal spinners and from wedges hooking the wheels. The guards are the same height as the wheels, so the robot presents flat sides only.
  - Weak points: a guard is only held by two screws; a big hit can bend it into the tyre.
  - Construction: clear, so the wheels can be checked without removal; easy to swap.
- **Green base plate (BP)**
  - Fight: a stiff, flat floor; its overhang beyond the guards protects the lower guard edges and acts as a skid.
  - Construction: FR4 is very stiff for its weight and easy to cut; it carries the frame and motor blocks.
- **Wheels with O-ring tyres, 4WD**
  - Fight: four driven wheels give maximum pushing traction and keep driving if one loses grip. O-rings give good grip on the arena floor and are cheap to replace. Wheel tops above the body let it drive inverted.
  - Construction: printed hubs, standard O-rings.
- **Motor blocks between the wheels**
  - Fight: keep the motors inside the frame, away from the outside; they also support the guards in the middle (the most likely place to be hit).
  - Construction: two motors back-to-back per block keeps the wiring short.
- **Top window and power link**
  - Rules: AWS requires a removable link or switch reachable from outside; the window gives access with a finger.
  - Weak point: the hole lets a spinner tooth into the robot (later damaged holes are here).
- **Ribbed rear block**
  - Fight: a textured rear to push with when driving backward, and to resist being slid by wedges.
- **Decals (tiger stripes, demon face)**
  - Branding: "Speed Demon" character; makes the robot instantly recognisable.
- **Small silver screws**
  - Construction: M2–M3 screws into printed bosses; quick to replace skins after damage.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre, mm) | Confidence |
|---|---|---|---|---|
| Drive motors | 4 × N20 gearmotors, high rpm (500–1000 rpm), back-to-back in each side block | 12 × 10 × 25 (+ shaft) | (±38, +8, 16) and (±38, −14, 16), shafts along X (see note) | medium |
| (alt) Geared drive | 2 motors, each with a spur gear driving both wheels on its side | motor 12 × 10 × 25, gear Ø 12 | (±15, −5, 15) | low |
| Note on motor axis | N20 shafts must point along X to the wheels; "back-to-back" therefore means two motors side by side in Y, each with its shaft out to its own wheel | — | — | medium |
| Battery | 2S 300 mAh LiPo | 45 × 25 × 8 | (0, −15, 10) | medium |
| Receiver/ESC | combined board (black PCB seen) | 25 × 20 × 5 | (+5, +5, 20) | high |
| Power link | red plug in a socket | 14 × 10 × 10 | (+2, +12, 20) | high |
| Front block FB | printed wedge-section backing | 70 × 20 × 28 | (0, +35, 15) | medium |
| Frame floor | integral 1 mm floor or BP only | — | z 2–3 | low |
| Wires | short leads from the board to the four motors | — | centre bay | high |
| Rear bumper | ribbed printed rear wall | 30 × 10 × 10 | (0, −44, 8) | medium |
