# Team Phyte's Little Sytes: full rebuild description from reference photos

Source photos (all three cut out onto white by the AWS wiki). Every photo shows **two robots side by side**. This is a **two-robot cluster** ("Little Sytes", plural): two near-identical small wedge robots that fight together.
- `robots/team_phyte_s_little_sytes/reference/team_phyte_s_little_sytes.aws74.webp` (2116 × 761 px). AWS 74. Both robots are dark green with a **bright translucent green front lip**. The left robot is seen from the front, about 25° down and slightly from its left. The right robot is seen from its front-right three-quarter, about 30° down. The right robot's right side guard is the clearest side view in the set.
- `robots/team_phyte_s_little_sytes/reference/team_phyte_s_little_sytes.aws76.webp` (2626 × 1341 px). AWS 76. The same two robots, both seen from the front-left three-quarter, about 30° down. The near (right-hand) robot is large in frame and shows the wedge surface, the black corner tape, the switch, and the right side guard edge best. Its wedge panel reads **black**; its ears, base and lip read **dark green / translucent green**.
- `robots/team_phyte_s_little_sytes/reference/team_phyte_s_little_sytes.aws77.webp` (2267 × 914 px). AWS 77. Both robots are now **black**, and the front lip is **wrapped in clear packing tape** (shiny, white highlights). Long strips of black tape run down both sides of the wedge, with **U-shaped bumps** under the tape (screw heads). Seen from the front, 30–35° down.

Everything stated as fact is read from these photos. Anything inferred is marked **(guess)**. Dimensions in mm are **estimates**. The scale anchor is **W = width of the wedge at its rear fillet ≈ 100 mm**, cross-checked against the wheel (N20-class wheel, Ø 22–26 mm) and the slide switch (standard SS-12 class, about 12 × 6 mm body). The draft spec in the branch uses 96 × 112 × 30 mm for the body box, which is the same ballpark.

Unless noted, the description is of **one robot**. Section 16 lists the differences between the two robots and between events.

---

## 0. Coordinate system and naming

- **Origin O**: on the floor (z = 0), at mid-width (x = 0), directly under the **wheel axle line** (y = 0).
- **+X** = robot's right, **+Y** = forward (toward the wedge lip), **+Z** = up. Units mm. Side-profile angles are measured from the floor (+Y axis) in the YZ plane.
- **Front** = the wedge end. In all photos the fronts face the camera.
- Overall envelope (one robot): x ∈ [−52, +52], y ∈ [−16, +62], z ∈ [0, 38].

| ID | Part |
|---|---|
| BP | base plate / floor (green translucent, forms the front lip LP) |
| LP | front lip strip (front 12 mm of BP, bright green in AWS74/76, tape-wrapped in AWS77) |
| WP | wedge panel (black / dark green sloped plate on top of BP) |
| FL | concave fillet where WP turns up into the front wall |
| FW | V-topped front wall (rises from FL, dips in the middle) |
| EA-L / EA-R | left / right ears (the tall triangular tips of FW at the outer ends) |
| BAY | open electronics bay behind FW, between the wheels |
| SG-L / SG-R | left / right side guards (D-shaped plates outboard of the wheels) |
| SGS | guard-to-chassis joint (guard integral with the bay side walls, plus floor) |
| MM-L / MM-R | plastic motor mounts (clamp blocks / cradles inside the bay) |
| M-L / M-R | N20 gearmotors (brass gearbox visible) |
| WH-L / WH-R | two drive wheels |
| SW | slide power switch |
| SWH | printed switch housing / bezel |
| LBL | "ON / OFF" sticker |
| S-WF | 2 silver pan/flange screws at the wedge front corners |
| S-WR | 2 screws under tape at the wedge rear corners (AWS77 bumps) |
| S-SW | 1 silver countersunk Torx screw on the switch housing |
| S-MM | motor clamp screws (hidden) |
| TP-C | black tape patches on the wedge rear corners (AWS76) / long side strips (AWS77) |
| TP-L | clear tape on the lip (AWS77) |
| ESC, RX, BAT | ESC board(s), receiver, LiPo (partly visible in BAY) |
| WR | wires (red battery lead visible) |

---

## 1. Overall description in one paragraph

Each Little Syte is a **very flat, wide, two-wheel wedge** in which the wedge is most of the robot. Seen from above it is a wide trapezoid, about **100 mm wide and 78 mm long**, and about **two-thirds of its length is wedge**. The **wedge panel** is a broad, flat, slightly dished printed plate. It runs from a **thin green lip on the floor** at the front, up at about **20°**, then curves through a **concave fillet** into a near-vertical **front wall**. The top edge of that wall is a shallow **V** seen from the front: it is lowest in the middle, where a **slide switch** and an **ON/OFF sticker** sit, and it rises to two pointed **ears** at the outer corners that stand a little higher than the wheels. Behind the wall is a narrow, **open-topped electronics bay** running across the robot. It holds two **N20 gearmotors** (brass gearboxes visible) driving two **small treaded wheels** at the rear outer corners. Each wheel sits inside a **D-shaped side guard** that covers its outer face from the floor to about axle height. The top half of each wheel is exposed above the guard and above the bay. There is **no lid**: ESC/receiver connectors, wires and the switch are visible from above. The robot has no active weapon. It is a pure **pusher/wedge**, and the pair works as a team to get under and herd the opponent.

---

## 2. Part-by-part description

### 2.1 Base plate (BP) and front lip (LP)
- **Shape**: a flat plate forming the floor of the whole robot. In plan it is a trapezoid: about **104 mm wide at the front**, about **98 mm wide at the rear of the wedge**, and continuing under the bay to the rear at y ≈ −12. Thickness about **1.5–2 mm** under the wedge **(guess for the hidden part)**.
- **Lip LP**: the front 10–14 mm of BP is visible in front of the wedge panel as a **bright translucent green strip** (AWS74, AWS76). It is about **12 mm deep (Y) × 104 mm wide × 1.5 mm thick**, and it shows **2–3 fine grooves / raised lines parallel to the front edge**, about 3–4 mm apart. These read as print perimeter lines, or a stepped chamfer toward the edge. The very front edge is **thin (under 1 mm)**, as a sharpened chamfer would be. In AWS76 the lip is scuffed white along the front edge and has **chips/scratches** at mid-width (it has been in fights).
- **Colour/material**: translucent emerald green. It looks like **PETG** (glossy, translucent, with some light piping through the edges) **(guess)**. AWS77: same part, now **wrapped over the leading edge with clear packing tape** (TP-L), shiny with white highlights and a visible tape fold line about 6–8 mm behind the edge.
- **Plan curvature**: in AWS76 (near robot) the lip's front edge is a gentle **convex bow** (forward/downward at mid-width). It reads as a **slight downward sag at the centre of about 1–2 mm**: the lip's corners sit slightly higher than its centre, so the centre touches the floor first. This could also be perspective **(uncertain; see §13)**.
- **Seam with WP**: a straight, clear **step line** across the full width where the black/dark wedge panel ends on top of the green lip, about **1–1.5 mm high** (the panel's front edge). In AWS77 the clear tape runs over that step.

### 2.2 Wedge panel (WP)
- **Shape**: a broad flat plate, **about 98 mm wide (X) × 46 mm long along the slope × 2 mm thick**. It starts at the lip seam (y ≈ +50, z ≈ 2) and rises at about **20°** to the fillet (y ≈ +18, z ≈ 13).
- **Surface**: diagonal (about 45°) **top-surface infill lines** cover the whole panel (clear in AWS76 and AWS77). Pale scuffs and a few white dots/scratches are present.
- **Side edges**: the panel's side edges are not vertical walls. The panel simply ends at the side edges, which slope slightly inward toward the rear (trapezoid), and meet the ears' outer edges at the back. There are no cheek plates along the wedge sides: from the side, the wedge is a thin sloping sheet.
- **Colour**: AWS74 dark bottle green; AWS76 near robot black with green tint; AWS77 black.
- **Fasteners**:
  - **S-WF**: two **silver pan-head (flanged / washer-face) Phillips or Torx screws**, head Ø about **6 mm**. Each is about **10 mm in from the side edge** and about **14 mm behind the lip seam** (x ≈ ±40, y ≈ +36). They are clearly visible in AWS74 and AWS76.
  - **S-WR**: under the black tape near the rear corners (AWS77) there are **U-shaped bumps**, about 6 mm wide, two per side. One is at the rear (y ≈ +22) and one at the front (y ≈ +36). The front bumps are the S-WF screws under tape. The rear ones are probably **two more screws** near the fillet corners **(guess)**. So the wedge panel is held by **4 screws** into the base plate / chassis.

### 2.3 Fillet (FL) and front wall (FW)
- **Fillet**: the wedge panel turns upward through a **concave curve** (cylindrical, axis along X). Seen side-on (AWS74 right robot) the inner radius is about **8–10 mm**. In the photos this shows as a **band of horizontal print layer lines** about 8–10 mm tall across the full width (a stair-stepped look, printed with the curve rising in Z).
- **Front wall**: above the fillet the surface continues **near vertical, leaning back about 10–15°**, up to the V-shaped top edge.
- **Top edge in front view (the V)**: the centre (x = 0) top edge is at about **z ≈ 22**. It rises **linearly** to the ears at x = ±50. The V is not a sharp notch: there is a **flat-bottomed dip about 22 mm wide** at the centre, where the switch housing sits (AWS74 left robot, AWS77). So the top edge is a trapezoid trough: flat at z ≈ 22 for |x| ≤ 11, then rising at about **18°** to z ≈ 36 at |x| = 50.
- **Wall thickness**: the top edge shows as a **2–2.5 mm wide strip** with fine ridges (the print layers seen end-on as a toothed edge). The ears' top edges have a slightly ragged "serrated" look.

### 2.4 Ears (EA-L, EA-R)
- **Shape**: the outer ends of FW, forming **upright triangular fins**. Each is about **14 mm wide at its base** (x from ±36 to ±50) and its tip reaches about **z ≈ 36–38**. The tip is a **sharp point** at the outer front corner, raked slightly **outward and forward**. The ear's outer edge drops almost vertically to the wedge side edge.
- **Relation to the wheels**: in AWS74 (both robots) the ear tips are level with, or **2–4 mm above**, the wheel tops. Ears are about **6 mm in front of** the wheel front faces.
- **Marks**: AWS74 right robot left ear has a small embossed **"Y"/arrow mark** near its tip (a printed logo or a print artefact). AWS76 near robot left ear shows the same small mark.

### 2.5 Electronics bay (BAY)
- **Shape**: an open-topped tub across the robot, directly behind FW. About **74 mm wide** inside (between the motor cradles), **18–20 mm deep (Y)** and **about 20 mm tall**, from the floor up to about z ≈ 20. Its front wall is FW itself. Its rear wall is low and only partly visible (AWS74 right robot: a dark rim about 3 mm above the floor at the rear) **(guess)**.
- **No lid**: in every photo the bay is open from above. Visible contents, left to right (AWS77 left robot is clearest):
  1. Left wheel and the **brass gear stack of M-L** right inside it.
  2. A **black 2–3-pin connector block** and small **silver/white board parts** (ESC MOSFETs or a receiver crystal).
  3. **The switch SW** in its housing at the centre.
  4. A **white/silver rectangular part** (receiver antenna-end or a crystal can) and **black header blocks**.
  5. The **brass gear stack of M-R** and the right wheel.
- **Red wire**: AWS74 left robot shows a **red insulated wire** looping just behind the right half of FW. It is the battery positive or a motor lead.

### 2.6 Motors (M-L, M-R) and plastic motor mounts (MM-L, MM-R)
- **Motors**: AWS77 (both robots) shows a **brass-coloured gear stack** right inboard of each wheel, with a **silver motor can** further inboard. This is the classic **N20 micro gearmotor**: gearbox 12 × 10 × 9 mm plus can 12 × 10 × 15 mm, about 24–26 mm long overall, with the D-shaft out to the wheel. Each motor lies **along X** (transverse), with its axis at the wheel axle line (y = 0, z ≈ 11).
- **Mounts**: the motors are seated in a **printed cradle**, a U-channel in the bay floor plus a clamp block. The visible **black squared blocks** above each gearbox (AWS74 left robot, both sides: "black block with a slot") are probably the **motor clamp straps**, about **14 × 6 × 6 mm**, each held by **1–2 M2 screws (S-MM)** into the bay floor **(guess)**.

### 2.7 Wheels (WH-L, WH-R)
- **Shape**: a cylinder, **Ø ≈ 24 mm × 9 mm wide**. The tyre carries **transverse ribs (grooves across the tread)**, about **28–32 ribs** round the circumference, each about **1 mm deep**. The ribs look slightly irregular and soft, like a printed TPU tyre or a moulded rubber N20 wheel.
- **Hub**: black. The outer face shows a **central hole/recess Ø about 4–5 mm** (AWS74 left robot, left wheel). There may be a hub boss with a grub screw (not visible).
- **Position**: centres at x ≈ ±44, y = 0, z ≈ 12. The wheels sit at the **rear outer corners**, just behind the ears.
- **Height**: the top is at z ≈ 24, about **2 mm above the bay rim** and about **2 mm above the V-dip**, but **below the ear tips**. The bottom touches the floor (z = 0), so the base plate must clear the floor by about **1–2 mm** there **(guess)**.
- **Invertibility**: when the robot is upside down, the wheels protrude only about 2–4 mm beyond the bay top. The ears (z = 36–38) protrude **more** than the wheels (z = 24), so an inverted robot would rest on its ear tips and the base. **It is probably not designed to drive inverted** (see §14).

### 2.8 Side guards (SG-L, SG-R)
- **Shape**: a **vertical flat plate**, about **2.5–3 mm thick**, outboard of each wheel (wheel outer face to guard inner face gap about 1–1.5 mm).
- **Side profile** (AWS74 right robot, right side; AWS76 near robot right side): a **D shape**.
  - The front edge is a vertical line at y ≈ +14 (just behind the ear), height from z = 0 to z ≈ 16.
  - The top edge is a line falling gently rearward, from z ≈ 16 at the front to z ≈ 14 above the axle.
  - The rear is a **semicircle concentric with the wheel axle**, radius **≈ 16 mm**, sweeping from the top round the back to the floor.
  - The bottom edge is flat on the floor line, from y ≈ −16 forward to y ≈ +14.
  - So the guard covers the **lower ~60 %** of the wheel's outer face and fully covers it at the rear. The wheel's upper arc and tread are exposed above the guard (AWS74 right robot: the rear-right wheel's top half shows above the guard).
- **Hole**: AWS76 near robot shows a **round dark hole (Ø ≈ 4–5 mm)** in the right guard about level with the axle. It is either the axle end visible through the guard (an outer bearing) or an access hole for the wheel grub screw **(guess: access/outer-axle hole)**.
- **Colour**: dark green (AWS74/76), black (AWS77).
- **Joint to the wedge**: a **vertical seam** is visible between the guard's front edge and the wedge side/ear (AWS76 near robot, right side). So the guard is **not the same part as WP**. Its front edge stands about **1 mm behind** the wedge side edge.

### 2.9 Guard-to-chassis supports (SGS)
- The guards appear **printed integral with the bay** (the bay's side walls extended outward and down around each wheel, joined by the floor). Specifically **(guess)**: each guard is joined to the bay by **(a)** the bay floor, which runs out under each wheel to the guard bottom edge as a 2 mm floor tab, and **(b)** a **motor-cradle end wall** inboard of the wheel, which links to the guard top through a short **bridge rib** behind the wheel (y ≈ −14, 3 mm thick). That makes a C-shaped wheel pocket open at the top.
- No screws are visible on the guards' outer faces, which supports the integral-print reading.

### 2.10 Switch (SW), switch housing (SWH), label (LBL)
- **SW**: a small **slide switch**. The slider is visible as a **black/silver toggle about 3 × 3 mm** in a slot. In AWS74 (left robot) a **red-and-white bodied** switch sits proud of the dip with its slider pushed left. In AWS77 the switch is a black slider in a **rectangular printed bezel**.
- **SWH**: a printed **rectangular collar** about **20 × 10 × 6 mm** at the bottom of the V-dip, with a **slot about 8 × 3 mm** for the slider. It is fixed by **one silver countersunk Torx/Phillips screw (S-SW)**, head Ø about **4 mm**, at its right end (AWS74 right robot, AWS77 left robot). There is a small **square hole** for an indicator or link at its left end (AWS77) **(guess)**.
- **LBL**: a printed paper sticker, about **18 × 6 mm**, reading **"ON" on green / "OFF" on red**. It is stuck on the front face of the V-dip directly below the switch, the right way up for someone standing in front of the robot. On the AWS76 near robot and the AWS77 left robot it is **upside down / mirrored in order ("OFF ON")**, matching the switch's own direction on that unit.

### 2.11 Tape (TP-C, TP-L)
- **AWS76**: rectangular patches of **black electrical (PVC) tape**, about **20 × 15 mm**, cover each **rear corner of the wedge** where WP meets the ear and fillet. They wrap over the fillet curve. They are probably **covering the rear screws S-WR** and protecting the corner from crack propagation.
- **AWS77**: the black tape is extended into **long strips about 18 mm wide** along **both side edges of the wedge**, from the fillet down to the lip. Clear tape then wraps the lip. The U-bumps under the black tape are screw heads.

### 2.12 Wires (WR)
- Visible: one **red** lead near the right of the switch (AWS74 left robot). Everything else is hidden below the bay rim.
- **Guess**: battery red/black, through the switch, to the ESC; each motor has 2 short leads from the ESC; the receiver sits on or beside the ESC. All leads are under 50 mm long and lie in the bay below z ≈ 18.

---

## 3. Per-view descriptions

### 3.1 Top view (plan)
- A wide trapezoid: the **front edge 104 mm wide** (green lip), side edges converging to **98 mm** at y ≈ +16, then a **narrow 28 mm-deep band** (FW + BAY) with a wheel at each rear corner (9 mm wide × 24 mm long rectangles in plan, at x ≈ ±44). The **D-guards** add a thin 3 mm strip outboard of each wheel to x = ±52.
- Visible features from above: the green lip; the infilled wedge face with 2 silver screw dots at front corners; the thin V wall; the open bay full of components with the brass gearboxes at each end and the switch housing in the middle.
- Overall length about **78 mm**; overall width about **104 mm**.

### 3.2 Front view
- Bottom: the lip line on the floor, full width.
- Middle: the wedge face foreshortened into a wide band, with 2 silver screw heads near the bottom corners.
- Top: the **V-shaped top edge**, low in the middle (z 22) with the switch and the ON/OFF sticker, rising to the two pointed ears at the corners (z 36–38).
- Behind the V: the two **wheel tops** peeking over the bay at the outer ends (just inboard of the ears), and component tops in the bay.
- At the far sides: the thin side guards (2.5 mm) standing vertically, roughly the height of the wheel centre.

### 3.3 Right side view (AWS74 right robot is closest)
- A **long, low right triangle** (the wedge, 20° slope) running back to a **vertical ear** (z 36), then the **D-shaped guard** with the wheel's upper arc showing above it.
- The wedge side is a thin edge (2 mm sheet plus 1.5 mm lip below it). There are **no side cheeks**, so from the side you see under the panel into the hollow wedge (dark gap) **(guess: the space under WP is closed by BP at the bottom, so it reads as a thin triangular slot)**.

### 3.4 Rear view (not photographed; inferred)
- A low rear wall (z ≈ 0–18) across the bay. The two wheels are at the corners, each enclosed by its guard's semicircular back. The ear tips stick up at the outer corners behind/above the wheels. The component tops are visible over the wall. The switch is at the front of the bay, so it is **not reachable from the rear**.

### 3.5 Isometric (front-left-top, as AWS76)
- Reads as a **dustpan with two wheels**: a huge sloping tray with a curled-up back edge, two pointed ear tips, and a small row of electronics hidden behind the curl.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W=100 | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| BP | flat trapezoid plate | 104/98 × 74 × 1.5–2 | 1.04 × 0.74 | translucent green PETG (guess) | carries WP screws | 1 |
| LP | front strip of BP | 104 × 12 × 1.5, sharp edge | 1.04 × 0.12 | green / tape-wrapped | integral with BP | 1 |
| WP | sloped plate | 98 × 46 (slope) × 2 | 0.98 × 0.46 | black / dark green PLA | 4 screws | 1 |
| FL | concave fillet | r 9, 98 wide | — | same as WP | integral | 1 |
| FW | V-topped wall | 100 × 22–36 tall × 2.5 | — | same | integral | 1 |
| EA | triangular fin | 14 base × 14 rise | 0.14 | same | integral | 2 |
| BAY | open tub | 74 × 18 × 20 | 0.74 × 0.18 × 0.20 | dark green/black | — | 1 |
| SG | D plate | 30 long × 16 tall × 2.5, rear r 16 | 0.30 × 0.16 | dark green/black | integral (guess) | 2 |
| MM | U cradle + strap | 14 × 12 × 6 | — | black printed | 1–2 × M2 | 2 |
| M | N20 gearmotor | 12 × 10 × 25 | — | silver can, brass gears | in MM | 2 |
| WH | treaded wheel | Ø 24 × 9 | 0.24 × 0.09 | black TPU/rubber | D-shaft | 2 |
| SW | slide switch | 12 × 6 × 6 | — | red/white or black | in SWH | 1 |
| SWH | collar | 20 × 10 × 6 | — | dark green/black | 1 × S-SW | 1 |
| LBL | sticker | 18 × 6 | — | paper green/red | adhesive | 1 |
| S-WF | flanged pan screw | head Ø 6, M2.5–M3 | — | silver | WP into BP | 2 |
| S-WR | screw (under tape) | head Ø 5 | — | — | WP into BP/chassis | 2 (guess) |
| S-SW | countersunk Torx | head Ø 4, M2 | — | silver | SWH into FW | 1 |
| S-MM | pan screw | M2 | — | — | MM into floor | 2–4 (hidden) |
| TP-C | black tape | 20 × 15 / strips 18 × 45 | — | black PVC | adhesive | 2 |
| TP-L | clear tape | 104 × 15 | — | clear | adhesive | 1 (AWS77) |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| LP front edge ↔ floor | touching (or ≤ 0.5 at the corners if bowed) | 0 |
| BP ↔ floor (under the wedge) | slightly above, rising toward the rear | 0–2 |
| WP front edge ↔ LP top | stacked, step 1–1.5 | 0 |
| WP ↔ BP | screwed at 4 points; hollow wedge between | 0 at screws |
| WP rear ↔ FL ↔ FW | continuous, one print | 0 |
| EA outer edge ↔ SG front edge | seam, separate parts | ~1 |
| WH outer face ↔ SG inner face | side by side | 1–1.5 |
| WH tread ↔ SG semicircle | concentric clearance | 2–3 |
| WH inner face ↔ MM / gearbox | close | 1–2 |
| WH front ↔ FW back (at the ears) | close | 3–6 |
| WH bottom ↔ floor | touching | 0 |
| WH top ↔ BAY rim | sticks out above | +2–4 |
| WH top ↔ EA tip | below the ear | −12 |
| M ↔ MM | clamped | 0 |
| SWH ↔ FW dip top | screwed | 0 |
| SW slider top ↔ FW dip top | proud | +3–4 |
| LBL ↔ FW front face | stuck | 0 |
| TP-C ↔ WP rear corners | stuck over FL | 0 |
| BAY components ↔ BAY rim | mostly below; connectors level with or proud of rim | −2 to +3 |

---

## 6. Mechanism
1. **Drive**: 2WD, skid steer, two N20 gearmotors directly driving the two rear wheels. There is no front wheel: the front of the robot rides on the **lip of the wedge**, which drags on the floor. The robot's weight is split between the wheels and the lip. The motor mass at the rear keeps most of the load on the wheels.
2. **Weapon**: none. The wedge **is** the weapon. Two Sytes work as a pair: one gets under the opponent while the other pushes or blocks it.
3. **Steering**: differential. The wide lip has very little scrub because it slides.

---

## 7. Assembly order (suggested rebuild)
1. Print the **chassis**: BP floor, BAY walls, motor cradles MM and the two **side guards SG** as one part (green PETG in AWS74/76) **(guess)**. Sharpen or chamfer the lip.
2. Push the two **N20 motors** into the cradles with shafts outward. Fit the **clamp straps** with M2 screws.
3. Press the **wheels** onto the D-shafts through the open top of each guard pocket.
4. Place the **ESC/receiver**, **battery** and wiring in the bay. Mount **SW** in **SWH**.
5. Print the **wedge shell** (WP + FL + FW + EA) as one part. The fillet and ears look printed with the wall standing up (layer lines horizontal on the fillet) **(guess)**.
6. Lay the wedge shell onto BP and fix it with the **4 screws** (2 front S-WF visible, 2 rear S-WR).
7. Screw **SWH** into the V-dip with **S-SW**. Stick on the **ON/OFF label**.
8. Apply **black tape** to the rear corners (and side strips, AWS77) and **clear tape** to the lip (AWS77).
9. Build the second robot identically.

---

## 8. Hidden / uncertain list
- Whether BP and the guards are one part, and whether the green lip is part of BP or a separate strip.
- The exact screw count on WP (2 visible, 2–4 total).
- Bay rear wall height; how the bay is closed underneath.
- Motor clamp details; ESC/receiver type; battery size.
- Whether the lip is bowed (sag) or flat.
- All mm values ±15 %.

---

## 9. Coordinate frame (restated)
- **Origin O** = floor point at mid-width under the wheel axle line. **+X** right, **+Y** forward, **+Z** up, mm.
- Key planes: lip edge y = +62; lip seam y = +50; wedge top / fillet start y = +18; FW face y ≈ +14 to +12; bay y ∈ [−8, +12]; wheel axle y = 0; guard rear y = −16.

## 10. Profiles as math

**10.1 Wedge centreline side profile (YZ plane at x = 0, top surface).**
- Lip: z = 1.5 for y ∈ [+50, +62], with an underside chamfer from (62, 0) to (56, 1.5) (sharp edge).
- Wedge: z = 3 + tan(20°)·(50 − y) = 3 + 0.364·(50 − y) for y ∈ [+18, +50], reaching z ≈ 14.6 at y = 18.
- Fillet: arc with centre C = (y +9, z 18), r = 9.5, from θ = −70° (tangent to the 20° slope) to θ = 0° … chosen so the surface meets the wall: points (y 18.0, z 14.8) → (y 18.5, z 18). Wall face then leans back 12°: y = 18.5 − tan(12°)·(z − 18) for z ∈ [18, z_top(x)].
- Wall top z_top(x) (V-trough): z_top = 22 for |x| ≤ 11; z_top = 22 + 0.36·(|x| − 11) for 11 < |x| ≤ 50, giving 36 at |x| = 50 (rise angle atan(0.36) = 19.8°).

**10.2 Ear (in the plane of FW).** Triangle with vertices (|x| 36, z 31), (50, 38), (50, 22): the outer edge is near vertical at |x| = 50 from z 22 to 38, the tip is at (50, 38), and the inner edge follows the V line.

**10.3 Wedge plan outline (XY, z = top of WP).** Trapezoid: front corners (±52, 62), rear corners (±49, 18). Side edges: x = ±(49 + 3·(y − 18)/44).

**10.4 Lip bow (if present).** Front edge z(x) = 0 + 1.5·(x/52)², i.e. the corners lift 1.5 mm above the centre.

**10.5 Side guard (YZ plane at x = ±51.5).** Outline: from (y +14, z 0) up to (14, 16); line to (0, 14.5); arc centre (0, 12), r = 16 from θ = 81° round through 180° (rear) to θ = 228° where it meets the floor line z = 0 at y ≈ −10.6 … then the floor line z = 0 from y = −10.6 back to +14. (Implicit form of the rear: (y)² + (z − 12)² = 16², y ≤ 0.)

**10.6 Wheel tread (XZ disc in the wheel frame).** r(φ) = 11.0 + 1.0·[sin(30φ) > 0], φ ∈ [0, 2π), extruded 9 mm along X. Hub hole r = 2.2 at the centre.

**10.7 Switch housing (in the FW dip).** Box x ∈ [−10, +10], y ∈ [+8, +18], z ∈ [18, 24], with a slot x ∈ [−4, +4], y ∈ [+12, +15].

## 11. Pixel-based measurements (independent check; px are native resolution, ±10 px)

**AWS74 left robot (front view):** the native 2116 px image was viewed at 1100/2116 scale in the crop. Native: lip front edge from x ≈ 150 to ≈ 1000 px of the left half (about 850 px). Wedge rear at FW base ≈ 200–985 (≈ 785 px). Left wheel visible width ≈ 90 px, top at y ≈ 120 (crop px ×1.92). Switch body ≈ 85 × 50 crop px. Screws: (190, 505) and (905, 360) crop px. ON/OFF label ≈ 115 × 35 crop px.

**AWS74 right robot (front-right iso):** right wheel ≈ 140 × 160 crop px; guard semicircle ≈ 170 px tall; ear tip at (95, 45) crop px.

**AWS76 near robot:** wedge rear width (ear tip to ear tip) ≈ 1090 px; right wheel ≈ 150 px tall; switch label ≈ 145 × 45 px.

**AWS77 left robot:** wedge top width ≈ 820 crop px; wheel tread width (edge-on) ≈ 65 px; ON/OFF label ≈ 95 × 30 px.

## 12. Several independent estimates of key sizes

| Quantity | Method A (assumed scale) | Method B (switch label / switch) | Method C (wheel width) | Reconciled |
|---|---|---|---|---|
| Wedge width W | 96–112 (spec draft 112 for body width) | AWS74 left: label 115 crop px ≈ 18 mm → 6.4 px/mm; lip 850·(1100/2116)=442 crop px → 69?? (see §13.1) | AWS77: wheel tread 65 px ≈ 9 mm → 7.2 px/mm; wedge 820 px → 114 mm | **100** |
| Wheel Ø | 22–26 (N20 wheel range) | AWS76: 150 px vs label 145 px ≈ 18 mm → 19 mm (far away, smaller) | AWS74 right: 160 px tall vs guard 170 px | **24** |
| Wedge slope | 20° (side view, AWS74 right) | screws-to-lip foreshortening in AWS74 left: wedge looks 0.30 of its width tall at ~25° camera elevation → slope ≈ 18–22° | AWS76: fillet to lip appears 0.45 W along slope | **20°** |
| Overall length | 78 | wedge 0.46 W slope → 44 mm horizontal + bay 28 + guard 6 → 78 | — | **78** |
| Ear height | 36–38 | ear tip 2–4 mm above the wheel top (24) → 26–28?? | V rise ratio from AWS77: centre dip 0.6 of ear height → 22 / 0.6 = 37 | **36** (see §13.3) |
| Screw head Ø | M3 flanged = 6 | 0.06 W ≈ 6 | — | **6** |

## 13. Consistency check: conflicts and reconciliation
1. **Wedge width from the switch label**: the label gives 6.4 px/mm at the FW depth, but the lip is much nearer the camera and the photo crop is scaled, so that method underestimates width. Using the label against the FW top width instead (FW top ≈ 600 crop px in AWS74 left) gives ≈ 94 mm. Using the wheel tread gives 114 mm. **Reconciled W = 100 mm**, inside both bounds and close to the spec draft.
2. **Wheel diameter**: 19 mm (label-based, far wheel) vs 26 mm (guard ratio). A Ø 24 tyre on an N20 hub is common. **Reconciled Ø 24**, centre z = 12.
3. **Ear height**: in AWS74 the ears look only slightly higher than the wheel tops, which suggests about 28–30 mm. The V-geometry from AWS77 suggests 37. The camera is high in AWS74, so the far wheel tops project higher in the image than their true height, which makes the ears look lower relative to them. **Reconciled 36 mm** at the tip. It can be dropped to 32 if a build looks too tall.
4. **Guard height**: the guard top looks level with the wheel centre in AWS74 right, and a bit higher in AWS76. **Reconciled: 16 mm at the front, 14.5 over the axle.**
5. **Lip bow**: the convex lip edge in AWS76 could be the wide-angle lens. AWS74 left shows the lip almost straight. **Reconciled: flat, with at most a 1.5 mm corner lift** (§10.4 is optional).
6. **Bay depth**: the bay must hold an N20 (10 mm deep in Y) plus a board. 18 mm inner depth is the minimum that fits the switch housing (10 mm) and a 2S battery standing on edge. Consistent with the photos, where the bay is a narrow strip.
7. **Mass budget** (cluster, about 75 g each **(guess)**): WP + FW + ears ≈ 15 g, BP + guards ≈ 12 g, 2 × N20 ≈ 20 g, wheels 4 g, 1S/2S 150 mAh LiPo ≈ 8–10 g, ESC + RX ≈ 6 g, screws ≈ 3 g, total ≈ 70 g. **Consistent** with a two-robot cluster in a 150 g class.

---

## 14. Why the designer did it (per part; adversarial lens first)

- **BP / LP: a thin, sharp, green lip on the floor**
  - Attack vs getting under: the whole robot's job is to be **lower than the opponent's front edge**. A 1.5 mm chamfered lip touching the floor wins the "who is under whom" contest against most printed wedges, whose edges are 2–3 mm thick. PETG is tougher than PLA and flexes, so the lip does not chip when it meets an enemy wedge edge-to-edge. Clear tape (AWS77) makes the lip slick and smooths the step from lip to panel, so an opponent's edge does not snag on the step and stop.
  - Attacks reaching it: horizontal spinners hit the lip first. It is sacrificial, and the chips visible in AWS76 show it doing that job.
  - Construction: green translucent for the team colour; the lip is part of the floor print so it costs nothing extra.
- **WP: a huge, shallow (20°) wedge, nearly the whole robot**
  - Getting under: a shallow angle gives the most ramp length and gives opponents the most time to ride up. With 100 mm width, it is very hard to drive past or around the wedge at an angle.
  - Attacks: vertical spinners and drums hit the slope at a glancing angle and are deflected upward, while the robot is driven down into the floor (the wedge loads the lip onto the floor). Flippers have very little to get under, because the lip is on the floor.
  - Construction: a single flat plate that prints quickly. The 45° infill lines show it printed face-up. Four screws make it replaceable after damage.
- **FL fillet**: removes the sharp internal corner where cracks start, and makes an opponent who rides up the slope roll upward and back onto the wall rather than jam in a corner.
- **FW: V-shaped top**
  - Adversarial: the high outer ears stop an opponent riding up the wedge from simply rolling over the wheels at the corners. The low centre lets the **switch** sit at the lowest, most sheltered point and saves weight.
  - It also acts as a **backstop**: an opponent pushed up the wedge hits the wall and is pushed rather than climbing on top of the electronics.
- **EA ears**
  - Adversarial: they shield the **wheels' front arcs**. A wedge or spinner coming at a front corner meets the ear before it reaches the wheel tread. When **flipped over**, the ear tips stand higher than the wheels, so the robot may rest on its ears and lose drive. That is the trade-off this design accepted: it is optimised for not being flipped (low, wide, wedge-first) rather than for running inverted. (A self-righting role is possible: if it lands on its back with the ears down, the robot may tip forward onto the wedge, **(guess)**.)
  - Construction: pointed ears are where print layers end, so the ragged top edges are expected.
- **BAY open, no lid**
  - Weight: a lid costs about 4–6 g, which in a 75 g cluster robot is a lot.
  - Adversarial: the bay is behind and below the FW top line, so a frontal attack never sees it. The risk is an overhead weapon or an opponent climbing on top. The designer accepted that risk because most attacks come up the wedge and are stopped by FW.
  - Repair: open access to the switch, connectors and motors without tools.
- **SG side guards (D-shaped)**
  - Adversarial: they stop horizontal spinners and opponents' wedges from contacting the **wheel's outer face and hub**, and stop the wheel being ripped off the shaft. The semicircular rear makes a rear impact glance off. Keeping the top of the wheel exposed means the wheel still grips walls and the opponent when pushing.
  - Getting under vs contact: the guard is on the floor line, so an enemy wedge from the side meets a vertical plate and cannot get under the wheel to lift it.
  - Construction: integral with the chassis, no screws, light.
- **SGS supports (floor tab + rear bridge)**: tie the guard to the motor cradle so a side hit is taken by the chassis, not by the motor shaft.
- **MM motor mounts**: the cradle plus strap carries the impact load into the floor, not the gearbox.
- **Wheels Ø 24, ribbed TPU**: ribs grip the arena floor for pushing. Small wheels keep the robot low. Placing them at the rear corners, with the lip as the front skid, gives a long wheelbase for straight pushing.
- **SW in a recessed housing at the V-dip**: the switch is reachable from the front (the rules need it accessible) but sits at the lowest point of the wall, behind the wedge, so a hit to the face rarely knocks it off. The single-screw housing makes swapping a broken switch quick.
- **LBL ON/OFF**: event safety requirement: the marshals must see the switch state.
- **S-WF / S-WR screws**: flanged pan heads spread the load on the printed panel. Four screws let the panel be replaced quickly between fights.
- **TP-C / TP-L tape**: black tape at the rear corners covers the screws (so opponents do not catch on the heads) and holds cracks closed. Clear tape on the lip makes the edge slick and protects it from chipping.

---

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Battery | 2S 7.4 V LiPo 150–180 mAh, or 1S 3.7 V with N20 6 V motors | 30 × 12 × 10 | lying across the bay behind the switch, x 0, y −2, z 6 | medium |
| ESC | dual brushed micro ESC (e.g. DasMikro / Ant ESC) | 20 × 12 × 4 | left of the switch, x −20, y 0, z 4 | medium |
| Receiver | small 2.4 GHz rx (e.g. FS2A / DSM micro) | 18 × 12 × 4 | right of the switch, x +20, y 0, z 4 | medium |
| Wedge interior | hollow triangular void between WP and BP, possibly with 2–3 ribs along Y | — | y 18–50 | low |
| WP screw bosses | 4 printed bosses Ø 6 on BP with M2.5 holes, rising to WP underside | Ø 6 × 3–12 | under S-WF / S-WR | medium |
| Motor clamp screws | 2 × M2 per strap into BP | — | x ±30, y 0 | low |
| Wheel retention | D-shaft press fit, no grub screw | — | — | medium |
| Wiring | battery → switch (front-centre) → ESC → 2 motor leads (about 25 mm each); RX lead to ESC | — | in bay below z 18 | medium |

---

## 16. Differences between the two robots and between events
- **AWS74**: both robots dark green with bright green lips. Left robot: red-and-white switch body exposed, the red wire visible, label "ON OFF" reading correctly. Right robot: switch in a dark housing with a silver screw; label reads "OFF ON" (the opposite orientation).
- **AWS76**: the near robot's wedge panel is black with black tape patches at the rear corners. The far robot looks the same as the near one.
- **AWS77**: both robots fully black, lips wrapped in clear tape, long black tape strips down both side edges of the wedge, with U-shaped screw bumps under the tape. Brass gearboxes and white/silver components are visible in the bays. One label reads "OFF ON", the other "ON OFF".
- **Photo limits**: there is no side-on or rear photo, so the guard shape, bay rear and underside are partly inferred. The photos are good for the wedge, ears, switch and the general layout, and limited for everything behind the front wall.
