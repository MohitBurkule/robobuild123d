# Failure to Launch: full rebuild description from reference photos

Source photos (three different builds of the same robot name; they are not the same machine):
- `robots/failure_to_launch/reference/ftl.webp` (1200 × 1057 px): **the primary build target** (it is the only photo listed in `REFERENCE.json`). **Yellow chassis, black T-shaped flipper lid.** It is shot on a wooden-laminate table from the **front-left three-quarter, high**: the camera sits about 45–50° above the floor, and about 35–40° to the robot's left of the nose. The two front wedge prongs point to the image bottom-left and bottom, the rear hinge is at the top right, and the robot's **right wheel** is on the image right edge. The left wheel is hidden.
- `robots/failure_to_launch/reference/ftl_original.webp` (1200 × 899 px): **the original build ("Mk 1")**. **Orange** printed body, a large orange tapered **beak-shaped flipper lid** with two googly eyes, a separate orange **lower front wedge**, and black wheels. It is shot on a bamboo chopping board, **front-right three-quarter**, at about 25° elevation and about 50° to the robot's right of the nose (the lid tip is at the image bottom right).
- `robots/failure_to_launch/reference/failure_to_launch.aws63.webp` (458 × 410 px): AWS 63 pit photo, small and soft. **Yellow chassis with a light-blue T-shaped flipper.** It looks like the same design family as `ftl.webp`, with a different flipper colour. It is shot from **front-left, high (about 55°)**. The hinge is at the image top left and the prongs point to the image bottom right. Other objects (a Turnigy charger, a servo tester, another robot) crowd the frame.

Pixel coordinates refer to the files as converted to jpg at the sizes given above. I read them by eye, ±10 px.

Everything stated as fact is read from those photos. Anything inferred is marked **(guess)** and given a confidence where it matters (**H** high, **M** medium, **L** low). Dimensions are **estimates**, scaled from the AWS antweight rules (150 g, must fit inside a 101.6 mm / 4 in cube) and from the drive wheel, which is a common printed or bought "N20 wheel" of about Ø 32 mm. Ratios are given against **D = wheel diameter ≈ 32 mm**.

Robot class: **servo flipper / lifter on a two-wheel wedge**. `REFERENCE.json` says `flipper`, 2 wheels, axis x. The flipper is a flat lid hinged along the **rear** edge of the robot about a transverse (X) axis. It lies forward and down over the front of the robot at rest. When fired it pivots up about the rear hinge, so the front of the stem rises and throws an opponent up and back. This is the "rear-hinged lid flipper" layout (like a bin lid), not a front-hinged flipper. A micro servo drives it (the servo with orange/red/brown leads is visible inside).

---

## 0. Coordinate system and naming

- **+X** = robot right, **+Y** = forward (toward the prong tips), **+Z** = up.
- **Origin O** = the floor point directly below the midpoint of the two drive axles. The drive axle is therefore the line y = 0, z = R_w = 16.
- **Front** = the end with the two yellow prongs. **Rear** = the hinge end.
- Flipper angle **θ** is measured in the YZ plane about the hinge axis, from the plate's rest attitude. θ = 0 is resting on the prop (the stem sloping down forward about 15–20° from horizontal). Positive θ lifts the stem tip.
- All four photos agree that the robot is a two-wheeler with the wheels at the **rear half** and the prongs as the front skids. There are no rear skids or casters visible. At rest the robot balances on the wheels and the prong tips.

| ID | Part |
|---|---|
| CH | yellow printed chassis core (central bay plus two motor pods) |
| MP-L / MP-R | motor pods: yellow boxes on each side that hold the N20 gearmotors |
| FW | chassis front wall / cross-member plate joining the prong roots |
| XB | front cross-plate (low flat yellow plate between the prongs) |
| PR-L / PR-R | the two front wedge prongs (left and right) |
| PT-L / PT-R | rest tower: the raised rear part of the left prong (the flipper rest) |
| TP-PR | clear packing-tape skirts on the prong tips |
| HG | rear hinge: steel pin, yellow chassis knuckles (HK-1…HK-4), nuts (HN), and the black flipper knuckle (FK) |
| FL | black printed T flipper plate (FL-X = crossbar, FL-S = stem) |
| EY-L / EY-R | clear-domed googly eyes on the flipper crossbar, held with clear tape |
| TP-FL | grey cloth/duct tape around the stem tip, plus a clear tape tongue |
| SV | flipper servo (micro size, hidden except for its edge and leads) |
| SH | servo horn and pushrod/link to the flipper (hidden, guess) |
| DM-L / DM-R | N20 brass-gearbox drive motors |
| WH-L / WH-R | black wheels with a fine knurled tread and a 3-hole hub |
| RX | receiver / dual ESC board (green PCB, standing on edge in the bay) |
| ESC | drive ESC(s), possibly combined with RX (guess) |
| BAT | LiPo battery in clear wrap at the rear right of the bay (guess, M) |
| SW | red power link / switch at the rear-left corner |
| WR | wires: servo leads (orange/red/brown), motor leads, battery leads |
| S-x | screws: hinge pin bolt, motor clamp screws (hidden), wheel grub/press fit |

---

## 1. Overall description in one paragraph

Failure to Launch (yellow/black build) is a **small two-wheeled flipper** with a **U-shaped front**. From the rear forward: a black flipper **hinge** runs across the top rear edge. It is a steel pin through four small yellow printed knuckles, with two silver nuts and a central black knuckle that belongs to the flipper. Under the hinge is a **yellow chassis bay** about 55 mm wide and 40 mm long. Its two sides are boxy **motor pods** holding brass N20 gearmotors, and two **black knurled wheels** (Ø ≈ 32 × 10 mm) sit outboard of the pods. The bay is open on top. The flipper plate is the lid, and through its sides you can see a micro servo, a green receiver/ESC board standing on edge, and clear-wrapped electronics. In front of the bay, two long yellow **wedge prongs** (each about 22 mm wide and 50 mm long) run forward to flat bevelled tips. Each tip carries a strip of **clear packing tape** that skims the floor. The prongs are joined at their roots by a low, flat yellow **cross-plate** about 4–5 mm thick, so in plan the front reads as a squared "U" or tuning fork. The left prong's rear part rises into a taller block that acts as the **flipper rest**. The **flipper** is a 2.5 mm black printed plate shaped like a **T**. The crossbar (about 66 × 18 mm) runs along the hinge and carries two clear googly eyes. The stem (about 30 mm wide, 60 mm long) slopes forward and down and rests on the left prong's tower. Its tip is wrapped in grey tape with a clear tape tongue. A **red link/switch** sticks up at the rear-left corner.

---

## 2. Part-by-part description

### 2.1 Chassis core (CH)
- **What is seen**: yellow PLA (bright lemon yellow, matt, fine 0.2 mm layer lines on the vertical faces). The bay is open on top. Its right wall is a solid yellow box (MP-R) whose top is at about z 22 and whose outer face is pierced by the brass gearbox. The rear wall carries the hinge knuckles. The front of the bay is closed low by the cross-plate XB and the prong roots.
- **Plan**: bay outer width (between the pod outer faces) **≈ 56 mm** (x −28 … +28). Length **≈ 40 mm** (y −22 … +18).
- **Height**: the pod tops are at z ≈ 22 (they look level with the battery block in front of the right wheel). The rear wall rises to z ≈ 26 at the hinge line, so the hinge pin centre is at z ≈ 29.
- **Floor (guess, M)**: 1.5–2 mm thick at z ≈ 3–5, giving 3 mm ground clearance under the bay. The prongs carry the robot's front, so the floor can sit higher than in a four-wheeler.
- **Wall thickness**: about 2 mm, visible on the right prong's rear end and at the right pod's front edge (crop: the yellow wall shows a 2 mm lip where the green PCB stands next to it).

### 2.2 Motor pods (MP-L, MP-R)
- **MP-R (seen)**: a yellow box about **16 mm wide (X) × 28 mm long (Y) × 20 mm tall (Z)**, from x +12 to +28. Its front face is flat and vertical at y ≈ +12, and it shows as a lit yellow rectangle in front of the right wheel at image (790–930, 380–470). A small step or chamfer runs along its top-front edge. The outer face has a hole about 11 × 10 mm where the **brass N20 gearbox** sticks out. The gold gearbox is visible between the pod face and the wheel hub at image (900–935, 380–430).
- **MP-L (hidden, guess H)**: a mirror image at x −28 … −12.
- **Purpose**: each pod holds one N20 motor along the X axis (gearbox outboard, motor can inboard), with the output shaft at z 16, y 0.

### 2.3 Front cross-plate (XB) and front wall (FW)
- **Seen**: a **flat yellow plate** between the prong roots, visible in the U-gap at image (480–700, 540–640). Its front edge is straight and transverse, and its top is flat. The front face is about **4–5 mm** tall (crop: a 50 px face against the 200 px prong width).
- **Dimensions**: **≈ 22 mm wide (X, the U gap) × 15 mm deep (Y, from y +18 to +33) × 4.5 mm thick**, top at z ≈ 6, bottom at z ≈ 1.5 (it may touch the floor when the robot is pitched forward).
- Behind it the bay's front wall FW rises to z ≈ 20. It is visible as a sunlit yellow vertical face at image (540–720, 440–560) behind XB and under the servo/PCB.
- **Gap/notch**: the plate does not run to the prong tips. The U opening between the prongs is **≈ 22 mm wide and ≈ 37 mm deep** (from the XB front edge at y +33 to the tip line at y +70).

### 2.4 Front prongs (PR-L, PR-R)
- **Shape**: each prong is a **solid printed wedge**, rectangular in plan and a right trapezoid in side view. It has a flat sloping top, vertical inner and outer side faces, a flat bottom on or just above the floor, and a short **bevel at the tip**.
- **Plan**: width **≈ 21 mm** (X). PR-R spans x +11 … +32 and PR-L spans x −32 … −11, so the outer faces sit **4 mm outboard** of the pods (they shield the front of each wheel). Length from the chassis front (y +18) to the tip (y +70): **≈ 52 mm**.
- **Side profile (PR-R)**: top at the rear z ≈ 14, falling linearly to z ≈ 4 at y +64. Then a steeper **tip bevel** falls from z 4 to z 0.5 over y +64 … +70 (about a 30° face). The bevel is visible as the lighter band, about 6 mm deep, at each tip.
- **Tape (TP-PR)**: a strip of **clear packing tape** about 21 mm wide (the full prong width) is laid over the tip bevel. It runs **10–12 mm past the tip** onto the floor (the faint grey rectangles at image (130–340, 640–800) and (450–690, 860–1010)). Its purpose is to give a zero-height leading edge and a slick surface (see §14).
- **Underside (guess, M)**: flat, z ≈ 0.5 at the tip rising to z ≈ 1.5 at the root, so the tips are the front ground contacts.
- **Wall/infill**: the faces are smooth and uniform, with no visible fill pattern. They are probably printed solid or near-solid for weight at the front (guess).

### 2.5 Left rest tower (PT-L)
- **Seen**: the rear 18–20 mm of the left prong does **not** slope down like the right prong. It rises as a **tall block** whose **vertical inner face** (facing the U gap) runs from the cross-plate top (z 6) up to under the flipper stem. It is visible as the shaded yellow face at image (420–530, 400–600) and in the zoomed crop.
- **Size**: **≈ 21 (X) × 20 (Y) mm**, top at **z ≈ 28–30**, so it is about 15 mm taller than the right prong's root.
- **Function**: the stem FL-S lies on this tower at rest (it is in contact in the photo). That fixes θ = 0 and keeps the stem tip off the floor.
- **Asymmetry note**: the right prong has no tower. Its rear end (at image 705–862, 430–480) is low (z ≈ 14), and a servo wire loop passes over it. See §13.2 for whether the tower is really one-sided.

### 2.6 Rear hinge (HG): pin, knuckles, nuts
- **Seen** (crop of image 450–1050 × 60–520): along the top rear edge, from left to right, there are:
  1. a **yellow cylindrical knuckle** HK-1 (≈ Ø 6 × 5 mm),
  2. a **silver hex nut** HN-1 (M3, 5.5 AF, 2.4 thick) between knuckles,
  3. a **yellow knuckle** HK-2,
  4. a **black printed block** FK, about **18 mm long × 7 × 7 mm**, with a **textured top** (a printed diamond/crosshatch pattern; it looks like a fuzzy-skin or ironing artefact). This is the flipper's own knuckle, part of the crossbar.
  5. a **yellow knuckle** HK-3,
  6. a **silver hex nut** HN-2,
  7. a **yellow knuckle** HK-4,
  8. the **threaded end / screw tip** of the pin, protruding about 2 mm past HK-4 at the right end.
- **Hinge pin** (guess, H): an **M3 × 60–70 mm** bolt or threaded rod running the full width at z ≈ 29, y ≈ −22. The nuts between the knuckle pairs lock the pin to the chassis knuckles (the pin turns in FK) or act as spacers.
- **Knuckle spacing**: HK-1 to HK-4 span ≈ 56 mm (x −28 … +28). FK sits in the middle about 18 mm wide (x −9 … +9). This leaves about 10 mm on each side for the knuckle–nut–knuckle groups.
- In aws63 the same hinge style appears: two yellow knuckle pairs with nuts at the image top left, along the rear edge of the blue flipper.

### 2.7 Flipper plate (FL)
- **Material/colour**: black PLA/PETG, printed flat with a **smooth bed-side face up** (the top shows a satin texture and a faint circular scuff). Thickness **≈ 2.5 mm** (visible on the stem's left edge as a thin dark band, and as about 3 mm at the crossbar right end, which has rough unfinished edges).
- **Planform: T**.
  - **Crossbar FL-X**: **≈ 66 mm (X) × 18 mm (Y)**, along the hinge from x −31 to +35. It overhangs the chassis sides slightly. Its rear edge carries FK. Its far ends are cut square. The right end is visibly ragged (a print artefact or damage).
  - **Stem FL-S**: **≈ 30 mm wide × 62 mm long** beyond the crossbar front edge. Its inner corners at the crossbar junction are sharp 90° notches (no fillet).
  - **Offset**: the stem attaches to the crossbar **left of centre**. The crossbar runs from image x 470 to 965, the stem root spans image x 557–730, and the left overhang (≈ 87 px) is much smaller than the right overhang (≈ 235 px). In robot units the stem centreline is at **x ≈ −8 mm** (M). See §13.2.
- **Pose in ftl.webp**: at rest. The stem slopes down forward. Rear end z ≈ 31 (top of plate at the hinge). Tip z ≈ 26 underside, resting on PT-L. Slope ≈ 10–15°, plus the slope of the tower top.
- **Stem tip (TP-FL)**: the last **≈ 12 mm** of the stem is wrapped top and bottom in **grey cloth/duct tape** (a fibrous grey texture), and a **clear tape tongue** extends **≈ 12 mm** beyond the plate tip as a thin flap. The total "reach" of the stem therefore ends at about y +62.
- **Eyes EY-L / EY-R**: two **clear-dome googly eyes**, Ø ≈ 14 mm outer (white rim ring, clear dome, dark pupil disc). They sit on the crossbar at x ≈ −22 and x ≈ +20, each held by a square patch of **clear tape** (visible as glossy squares with lifted corners around each eye).

### 2.8 Servo (SV), horn (SH) and link
- **Seen**: under the flipper, at the left-centre of the bay, the edge of a **micro servo** case (dark grey/black plastic) with **orange/red/brown leads** that loop to the right over PR-R's root (image 780–850, 440–490: a white/red/black ribbon, the servo-extension or receiver plug).
- **Size (guess, M)**: a 9 g class servo, **23 × 12.5 × 22 mm** body with 32 mm mounting ears, or a smaller 5 g. The visible case section looks about 12 mm thick.
- **Orientation (guess, M)**: the output shaft is parallel to X, near the rear of the bay at about y −12, z 14. The horn (one-arm, 15 mm) drives a short pushrod (1 mm wire, Z-bend) to a pickup under the crossbar about 10 mm forward of the hinge. Alternative (guess, L): the horn presses directly on the flipper underside with no link, as a "lifter by push". That would explain the flipper simply resting on PT-L with no visible attachment.

### 2.9 Electronics (RX, ESC, BAT) and wiring (WR)
- **RX/ESC (seen)**: a **green PCB** about **28 × 15 mm**, wrapped in clear heat-shrink. It stands nearly vertical in the bay centre-right at image (640–770, 330–450), leaning back against the servo. Its long edge is roughly along Y. Brown smudges on its face are probably conformal glue or labels.
- **Second module (seen)**: behind it, a dark block in **clear tape/heat-shrink** fills the rear-right of the bay at image (690–930, 250–380), up to the underside of the crossbar. Most likely this is the **LiPo (2S, 150–180 mAh, ≈ 30 × 15 × 12 mm)** or a dual ESC (M).
- **A small yellow/black PCB** shows behind the eyes at image (700–730, 270–300). It may be the receiver's antenna base or the ESC's yellow capacitor (L).
- **Wires**: orange/red/brown servo leads loop from the bay to the right front over PR-R's root. Black/red motor leads are hidden inside the pods (guess). Clear tape bundles everything.

### 2.10 Drive motors (DM-L, DM-R)
- **Seen (right)**: a **brass N20 gearbox** sticks out of the pod side wall at the wheel hub. The gold gear plates show behind the wheel.
- **Assumed (H)**: two N20 micro gearmotors, 12 × 10 mm section, gearbox 9 mm + can 15 mm long, with a 3 mm D-shaft. The ratio is probably 100:1 to 150:1 for 2S. The shaft axis is at x ±(28 + 2), z 16, y 0.

### 2.11 Wheels (WH-L, WH-R)
- **Seen (right)**: black wheel, outer diameter **≈ 32 mm**, width **≈ 10 mm**. The tyre has a **fine straight-knurl tread** of about **60–70 axial ridges**, like a spur gear's teeth (it reads as a geared rim). There is a 1 mm chamfer on the outer rim edge.
- **Hub face**: a flat disc recessed ≈ 1 mm, with **three large holes**. Two appear as kidney/round holes (Ø ≈ 6 mm) at radius 7, and the third is hidden behind the spoke. The **spokes form a "Y" / three-armed star** (visible clearly on the orange build's wheel as a 3-spoke black hub with triangular openings). In ftl.webp the hub shows one round hole at the upper right and the dark Y spokes.
- **Fit**: pressed onto the N20 D-shaft. The wheel's inner face is about 1.5 mm from the pod outer face.
- **Placement**: centre at (x +35, y 0, z 16). The front of the tyre at y +16 is level with the pod front face and about 2 mm behind the prong root.
- **Wheel guards**: **none**. The wheels are fully exposed at the rear and top. Only the front is screened by the prong outer faces, which are 4 mm outboard of the pods but still inboard of the wheel's outer face (at x 40).

### 2.12 Power switch / link (SW)
- **Seen**: a **red rectangular plastic part** sticks up and back at the rear-left corner, just left of HK-1 and below the crossbar end, at image (470–545, 140–275). It is tilted about 30° from vertical toward the rear-left.
- **Size**: ≈ 6 × 10 × 14 mm.
- **Interpretation (M)**: a red **removable link plug** (a red JST/XT30-style shorting plug) or the red lever of a mini toggle. In aws63 a similar **red block with a black wire** sits at the left side next to the wheel (image 75–125, 205–240), which looks like a red plug on a short lead. **Best guess: a red removable link**, pushed into a socket in the left pod's rear corner.

### 2.13 Screws and fasteners (S-x)
- **Seen**: the hinge pin end (screw tip) and two nuts. Nothing else is visible on the outside. The flipper has no visible screws on top.
- **Guessed (M)**: 2× M2 screws per motor clamp under the floor; 2–4 M2 screws holding the prong block to the bay (or the prongs are printed in one piece with the bay, H). The flipper crossbar knuckle is printed integral with the plate (H).

---

## 3. Per-view sections (for silhouette matching)

### 3.1 ftl.webp (front-left iso, high)
- The dominant shape is the **black T** across the upper half. The crossbar runs from (470, 95) to (970, 235), and the stem runs from about (560–730, 160–240) down-left to the taped tip at (165–430, 380–510).
- **Prongs**: PR-L occupies (160–530, 400–770) and PR-R occupies (480–890, 440–970). Both tips have pale tape tongues on the table. The U gap is (480–700, 540–640) with XB visible.
- **Right wheel**: an ellipse (890–1015, 318–512) on the right edge, black, knurled, with a hub hole at about (990, 380).
- Inside the bay, under the flipper's right edge: the green PCB, servo leads, the clear-wrapped block and a brass gearbox.
- The **red SW** sticks up at the top left behind the crossbar.
- The shadow side is minimal (diffuse light from above).

### 3.2 ftl_original.webp (Mk 1, orange, front-right iso)
- **Lid (LID-0)**: a large orange plate shaped like a **tapered beak**. At the rear-top it is wide (top edge from (350, 190) to (690, 95), ≈ 60 mm). It narrows to the tip on the floor at (870–950, 630–700) (≈ 22 mm wide). It slopes about 35° from horizontal. Two **white googly eyes** (Ø 14 and 16, the near one larger) sit at about 25 % of the length from the top, at (525, 265) and (665, 195). A vertical **side skirt** about 30 mm tall runs down the robot's left side of the lid at image (385–420, 240–470). The lid's top edge is folded back to make a hinge bar (the double line at the top rear (350–690, 95–215)).
- **Lower wedge (WG-0)**: a separate orange block under the lid at the front-right, (500–850, 470–715). Its top face slopes down to the front. Its front face is chamfered, and its sharp toe is at (840, 715). Plan ≈ 28 × 30 mm. There is a **gap of ≈ 6–10 mm** between the lid and the wedge. Through this "mouth" the inner parts show: a white/beige servo case with a yellow/brown/black lead loop, a black N20 motor block, and black wires.
- **Wheel (WH-0)**: on the robot's right (image left): black Ø 32 × 10 knurled tread, with a **3-spoke Y hub** clearly visible, at (390–515, 440–590). A **black motor block** (N20 in a black printed clamp) is behind it at (480–560, 420–500).
- So the Mk 1 was the same N20/servo package with a **beak lid** that came right down to the floor in front, and no prongs.

### 3.3 failure_to_launch.aws63.webp (blue flipper, front-left iso, high)
- **Flipper**: **light blue** T plate. Crossbar at (20–240, 0–150) along the hinge at the image top left, with two googly eyes at (210, 80) and (125, 160). The stem runs from the crossbar to (310–390, 190–310), **filling the gap between the two yellow prongs** and making a continuous wedge with them. The stem's front half shows **fine ribs/print lines along Y** (a printed texture or a strip of ribbed tape).
- **Prongs**: yellow wedges on each side of the stem. The near prong at (130–330, 190–350) and the far prong at (230–430, 90–260) have sloping tops. The prong tops are about the same height as the stem: the stem **lies in the U gap**, flush with the prong tops.
- **Hinge**: yellow knuckles with silver nuts at the left end of the crossbar (35–60, 60–130).
- **Wheel**: black, at the left (20–70, 175–235).
- **Red link**: at (75–125, 205–240), with a short black wire.
- This photo fixes the **design intent**: the stem's width ≈ the U-gap width, and it sits **between** the prongs, not on top of one.

### 3.4 Top view (plan, synthesised for ftl build)
- The T flipper covers the bay. Crossbar from x −31 to +35 at y −31 … −13. Stem from x −23 to +7 (offset left; see §13.2) at y −13 … +49, plus tape to +61.
- The prongs PR-L (x −32 … −11) and PR-R (x +11 … +32) run from y +18 to +70. XB (x −11 … +11) runs from y +18 to +33.
- The wheels (x ±30 … ±40, y −16 … +16) stick out beyond the prongs by 8 mm on each side.
- Overall envelope: **X 80 × Y 101 mm** (y −31 … +70), with the tape tongues to +80 (tape is not counted for the box rule).

### 3.5 Front view
- From the front: two low yellow prong tips (21 mm wide, 4 mm tall with a bevel) on the floor at x ±11 … ±32. The 22 mm gap between them shows XB at z 1.5–6 set back, the bay front wall to z 20 behind it, and the stem descending above. The black wheels stand behind, out to x ±40 and up to z 32. The crossbar is on top at z ≈ 31 with the eyes facing up (not visible from the front).

### 3.6 Right side view
- Wheel Ø 32 at the rear-centre (y −16 … +16). The pod MP-R is behind it. The prong PR-R slopes from z 14 at y +18 to the floor at y +70. The flipper line runs from the hinge at (y −22, z 29) down forward. The hinge knuckles are at the top rear. The robot's highest point is the hinge/crossbar at **z ≈ 33**.

### 3.7 Rear view (not photographed, inferred)
- A flat yellow rear wall, 56 wide × 26 tall, with the hinge knuckles and nuts along its top edge. The wheels are on each side. The red link is at the top left corner. There is probably a charging/link socket hole (guess, L).

---

## 4. Part table (ftl build)

| ID | Shape | Size (mm) | Position (centre) | Material/colour |
|---|---|---|---|---|
| CH bay | open box | 56 × 40 × 26 | (0, −2, 13) | yellow PLA |
| MP-R/L | box | 16 × 28 × 20 | (±20, 0, 13) | yellow PLA |
| FW | wall | 22 × 2 × 18 | (0, +17, 11) | yellow |
| XB | plate | 22 × 15 × 4.5 | (0, +25.5, 3.8) | yellow |
| PR-R/L | wedge | 21 × 52 × 14→0.5 | (±21.5, +44, 7) | yellow |
| PT-L | block | 21 × 20 × 28 | (−21.5, +28, 14) | yellow |
| TP-PR | tape | 21 × 18 × 0.05 | tips y 64–82 | clear |
| HK-1..4 | cylinders | Ø 6 × 5 | x −26, −16, +16, +26; y −22, z 29 | yellow |
| HN-1/2 | M3 nuts | 5.5 AF × 2.4 | x −21, +21 | steel |
| Pin | M3 rod | Ø 3 × 62 | x −30 … +32 | steel |
| FK | block | 18 × 7 × 7 | (0, −22, 29) | black |
| FL-X | plate | 66 × 18 × 2.5 | (+2, −22, 31) | black PLA |
| FL-S | plate | 30 × 62 × 2.5 | (−8, +18, 29 avg) | black PLA |
| TP-FL | tape | 30 × 12 wrap, +12 tongue | stem tip | grey + clear |
| EY-L/R | dome | Ø 14 × 4 | (−22 / +20, −22, 33) | clear/white |
| SV | servo | 23 × 12 × 22 | (−6, −6, 16) | grey/black |
| RX | PCB | 28 × 15 × 4 | (+8, +4, 16), on edge | green + clear shrink |
| BAT | pouch | 30 × 15 × 12 | (+10, −12, 18) | clear wrap |
| DM-L/R | N20 | 12 × 10 × 24 | (±20, 0, 16) along X | brass + silver can |
| WH-L/R | wheel | Ø 32 × 10 | (±35, 0, 16) | black |
| SW | red link | 6 × 10 × 14 | (−27, −26, 30), tilted | red |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| WH bottom ↔ floor | drive contact | 0 |
| PR tip / tape ↔ floor | skid contact | 0 |
| CH floor ↔ floor | clearance | 3 |
| XB bottom ↔ floor | clearance | 1.5 |
| WH inner face ↔ MP outer face | running clearance | 1.5 |
| WH front ↔ PR root | fore-aft | 2 |
| WH outer face ↔ PR outer face (x) | wheel stands proud | 8 |
| PR-L inner ↔ PR-R inner | U gap | 22 |
| PR ↔ CH front | printed integral / screwed | 0 |
| XB ↔ PR inner faces | integral | 0 |
| FL-S underside ↔ PT-L top | resting (θ = 0) | 0 |
| FL-S underside ↔ PR-R top | above | 10–15 |
| FL-S underside ↔ XB top | above | ~20 |
| FL-X underside ↔ MP tops | above | 4–6 |
| FL-X underside ↔ BAT top | near | 1–2 |
| FK ↔ pin | rotating | 0.2 |
| HK ↔ pin | clamped/press | 0 |
| HN ↔ HK faces | clamped | 0 |
| HK-2 ↔ FK ends; FK ↔ HK-3 | side play | 0.5 |
| EY ↔ FL-X | taped | 0 |
| TP-FL ↔ FL-S | wrapped | 0 |
| SV ↔ CH floor/wall | glued/screwed | 0 |
| SH link ↔ FL-X underside | pinned (guess) | 0 |
| RX ↔ SV / CH right wall | leaning, taped | 0 |
| SW ↔ CH rear-left corner | plugged | 0 |
| DM ↔ MP bore | clamped | 0 |
| WH hub ↔ DM shaft | press fit | 0 |

---

## 6. Mechanism

- **Drive**: two-wheel differential drive by N20 gearmotors. The wheels are near the middle of the length (the axle is at about 31 % of the total length from the rear). The robot pitches forward onto the prong tips, so the tips carry about 35–45 % of the weight.
- **Weapon**: the servo rotates the flipper about the rear hinge pin (axis X, at y −22, z 29). The working range is probably θ = 0 … +80°. The stem tip travels on a circle of radius ≈ 84 mm (hinge to tape tip). At θ = 60° the tip rises from z ≈ 22 to z ≈ 22 + 84·(sin(60° − 12°) + sin 12°) ≈ 22 + 84·(0.74 + 0.21) ≈ 102. In practice the servo torque (≈ 1.5–2 kg·cm) at an 8 mm lever only lifts light opponents. The weapon is more a **lifter/self-righter** than a launcher, which suits the self-deprecating name.
- **Self-righting**: when upside down, the robot rests on the crossbar/hinge and the prongs. Firing the flipper pushes the stem into the floor and can roll the robot back over the hinge line (guess, M).

---

## 7. Assembly order (suggested rebuild)

1. Print the chassis (bay + pods + front wall + XB + prongs + PT-L) in yellow as **one piece**, bottom down. (Alternatively, print the prong block separately and screw it to the bay front wall with 2 × M2.)
2. Press both N20 gearmotors into the pod bores from inside, gearbox outboard. Clamp them (screws or glue).
3. Glue or screw the micro servo into the bay at the rear-left, output shaft along X.
4. Install the RX/ESC board on edge in the centre-right, the battery at the rear-right, and the red link socket at the rear-left corner. Tape the bundles.
5. Print the black T flipper (plate + FK knuckle) flat, bed-side up. Stick on the googly eyes with clear tape.
6. Slide the M3 pin through HK-1, HN-1, HK-2, FK, HK-3, HN-2, HK-4, and tighten the nuts.
7. Fit the servo horn and the link to the flipper underside (or set the horn to push the plate).
8. Wrap the stem tip in grey tape. Add clear tape tongues to the stem and both prong tips.
9. Press the wheels onto the shafts.

---

## 8. Hidden / uncertain list

- The left wheel, the left pod, the servo's exact position, and the battery's identity: all hidden.
- Whether the stem is really offset to the left in the ftl build (§13.2).
- Whether PT-L is unique to the left side (no right tower seen).
- The servo–flipper linkage.
- Whether the prongs are separate prints.
- The underside: not photographed in any view.

---

## 9. Coordinate frame (restated)

+X right, +Y forward, +Z up. O on the floor under the axle midpoint. Hinge axis: the line (y −22, z 29), parallel to X. Prong tips at y +70. The rear face is at y −31 (crossbar rear edge, FK behind the pin).

---

## 10. Profiles as math

**10.1 Prong side profile (YZ, constant over the prong width).** Top line z_top(y) = 14 − (10/46)·(y − 18) for y ∈ [18, 64], i.e. a slope of 12.3°. Tip bevel z_top(y) = 4 − (3.5/6)·(y − 64) for y ∈ [64, 70], a 30° bevel. Bottom z = 0.5 + (1/52)·(70 − y).

**10.2 Rest tower PT-L.** A box x ∈ [−32, −11], y ∈ [18, 38], z ∈ [0.5, 28], top face inclined to match the stem: z_top = 28 − 0.2·(y − 18).

**10.3 Flipper planform (in the plate's own UV frame, U = X, V along the stem from the hinge axis).** The union of the rectangles R_X = [−31, 35] × [−9, 9] and R_S = [−23, 7] × [9, 71]. The tape tongue is [−23, 7] × [71, 83] (zero thickness). The knuckle FK is the cylinder r = 3.5 about V = 0, U ∈ [−9, 9], merged with the plate.

**10.4 Flipper pose.** A point (U, V) of the plate maps to world (x, y, z) = (U, −22 + V·cos(β − θ), 29 − V·sin(β − θ)), with the rest slope β = 12°. At θ = 0 the stem tip (V 71) is at y +47.4, z 14.2 (the plate centreline). Adding the 2.5 mm thickness and the tower top gives the contact. Note: the photo suggests the tip is a bit higher, z ≈ 26–29, which needs β ≈ 3–5°. **Use β = 4°** for the ftl pose (the tip on the tower at z ≈ 24) (M).

**10.5 Wheel.** A cylinder r = 16, width 10. Tread: 64 axial ridges, r(φ) = 16 + 0.6·max(0, cos(64φ)). Hub: a recessed disc r ≤ 11, depth 1. Three spokes 3 mm wide at φ = 90°, 210°, 330°, and three openings between them, each a circular-sector cutout r ∈ [3.5, 10.5].

**10.6 Mk 1 beak lid (ftl_original).** Plan trapezoid: rear width 60, front width 22, length 85. Half-width w(v) = 30 − 0.447·v for v ∈ [0, 85]. Slope 35°. Side skirt on the left edge: a triangle from the hinge down to the floor.

---

## 11. Pixel-based measurements (independent check)

**ftl.webp** (1200 × 1057):
- Right wheel ellipse: 125 px wide × 194 px tall. The tall axis ≈ the true diameter (the wheel face is turned toward the camera at about 50°).
- Crossbar length: (470, 95) → (970, 235) = 519 px.
- Stem width at the root: along the crossbar from 557 to 730 → ≈ 180 px. Stem length: root midpoint (643, 200) → tip midpoint (300, 450) ≈ 424 px.
- PR-R: rear-end width (705 → 862) ≈ 160 px; tip width ≈ 230 px (nearer). Length (770, 450) → (590, 960) ≈ 540 px.
- U gap at the XB front edge ≈ 150 px (a transverse span 480 → 607 corrected for slant).
- XB front face height ≈ 40 px.

**aws63** (458 × 410): stem width ≈ 70 px vs near-prong width ≈ 70 px vs wheel height ≈ 60 px.

**ftl_original** (1200 × 899): wheel 125 × 150 px; lid length (top edge to tip) ≈ 640 px; lid rear width ≈ 350 px, tip width ≈ 105 px.

---

## 12. Several independent estimates of key quantities

| Quantity | Method A (rule/parts) | Method B (ratio to D) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Wheel Ø D | 30–34 standard N20 wheel | — | — | **32** |
| Crossbar width | ≈ track − wheel width = 80 − 14 = 66 | 2.1 D = 67 | 519 / 194 × 32 = 86 (near-camera right end inflates; the left end is farther) → ×0.8 = 69 | **66** |
| Stem width | = U gap (aws63) ≈ 22–30 | 0.9 D = 29 | 180 / 194 × 32 = 30 | **30** |
| Stem length | box limit: 101.6 − 31 (rear) − 18 (crossbar) ≈ 52 + tape | 2.0 D = 64 | 424 / 194 × 32 = 70 (foreshortened up, near-inflated) | **62** |
| Prong width | (crossbar − gap)/2 = (66 − 22)/2 = 22 | 0.65 D = 21 | 160 / 194 × 32 = 26 (rear end), ×0.85 | **21** |
| Prong length | 101 total − 49 (rear to y +18) = 52 | 1.6 D = 51 | 540 / 194 × 32 = 89 (heavily near-camera, ×0.6) = 53 | **52** |
| U gap | stem 30 → gap ≥ 30 (aws63 style) | 0.7 D = 22 | 150 / 194 × 32 = 25 | **22–26** |
| XB thickness | 4–5 print | — | 40 / 194 × 32 = 6.6 (near) → 5 | **4.5** |
| Hinge height | wheel top 32 − 3 | 0.9 D = 29 | crossbar top at wheel top in image | **29** |
| Mass check | 2 × N20 (20) + servo (9) + RX/ESC (8) + BAT (12) + wheels (6) + prints (≈ 85) ≈ 140 g | — | — | **≤ 150 g** OK |

---

## 13. Consistency check: conflicts and reconciliation

1. **Box limit.** The total length −31 → +70 = 101 mm. That is just inside 101.6, with the tape tongues excluded (tape is ignored in practice). The width is 80 (wheel outer faces), and the height is 33 at rest. At full flip the flipper would exceed 101.6 in Z, but the rule applies at the start pose. **OK.**
2. **Stem offset and the rest tower.** aws63 shows the stem **centred in the U gap, flush with the prong tops**. ftl.webp shows the stem over the **left prong**, resting on a raised left block, with the crossbar overhanging much further on the right. Three readings:
   - (a) the ftl flipper is a **new asymmetric T** that rests on PT-L (M);
   - (b) the flipper is the same centred T, but the photo's wide-angle near-field perspective and the stem height (z ≈ 25 above the prongs) shift the stem left in projection (L: the computation in §11 gives a residual of about 15 mm, which perspective alone does not explain);
   - (c) the flipper is yawed on a worn hinge (L, because the knuckles are tight).
   **Reconciled for CAD: model the T with the stem centred at x = −8 and PT-L as the rest, matching the primary photo.** Leave a parameter `stem_offset_x` (−8 … 0) for the aws63 variant.
3. **Flipper slope.** The plate maths gives the tip too low for a 12° rest slope if it rests on the tower top at z 28. The photo shows a shallow plate, so **β ≈ 4°**, which puts the tip at z ≈ 24–26 on a tower of z ≈ 24. **Reconciled: PT-L top z = 24, β = 4°.** The tower is then about 10 mm taller than PR-R's root.
4. **Wheel position.** In the photo the right wheel is beside the bay at its rear half. Its tyre top (z 32) is at the image height of the crossbar's right end, consistent with the hinge at z ≈ 29–31. **OK.**
5. **Prongs vs wheels for ground contact.** If the prong tips touch the floor and the wheels touch the floor, the robot body is pitched slightly nose-down. The bottom line of 10.1 gives this. **OK.**
6. **Material.** The yellow is identical across the aws63 and ftl photos, so it is the same chassis with a reprinted flipper (blue → black) (M).

---

## 14. Why the designer did it (per part; adversarial lens first)

- **U-shaped twin prongs (PR-L/R)**: Adversarially, two separate prongs give **two independent low edges** that each conform to an uneven floor better than one wide wedge. They also give a forward reach that gets under opponents before the wheels arrive. The gap lets the flipper stem drop **between** them to the floor line (aws63), so the flipper becomes the third, central blade and lifts from right under the opponent. The gap also saves weight (≈ 25 % of a solid wedge).
- **Clear tape tongues**: these give a **zero-height, flexible leading edge** that slides under wedges and the opponent's skirts. Packing tape is slick and cheap to replace between fights. It is a classic antweight trick against other wedges, and it hides the true printed edge (which is about 4 mm tall).
- **Rest tower (PT-L)**: it makes sure the flipper always sits at the same, slightly raised attitude. The servo then never stalls against the floor at rest, and the stem tip isn't pushed into the arena seams. The one-sided placement may come from where the servo sits (the servo is on the left; the tower could be its housing extension) (L).
- **Rear hinge with a long M3 pin and outboard knuckle groups**: a long hinge spreads impact loads from hits on the flipper across four knuckles. The nuts double as spacers and pin locks. A rear hinge on a lid flipper makes the flipper **also the top armour**: the T crossbar covers the electronics bay.
- **T planform**: the crossbar is as wide as the robot for hinge strength and top cover. The stem is narrow so it fits between the prongs. A full-width plate would hit the prongs and could not reach the floor. The googly eyes on the crossbar give character and an obvious "face".
- **Grey tape on the stem tip**: it protects the print's layer edges from cracking when the stem is driven into the floor. It also adds grip under an opponent's chassis (cloth tape is grippy, unlike the slick clear tongue).
- **N20 motors in side pods, wheels outboard**: the cheapest reliable 150 g drive. Wide wheels outboard of the pods give a wide track for stable flipping. The exposed wheels also let it drive inverted, since the wheel top (z 32) is about level with the hinge top (z 33).
- **Micro servo**: light (≈ 9 g), uses the receiver's BEC, no extra ESC. Its weakness (low speed and force) gives the name **"Failure to Launch"**: the robot lifts rather than launches.
- **Open bay, electronics in clear tape**: fast access and inspection between fights. Clear tape keeps debris out and holds the boards without screws.
- **Red removable link**: required by AWS rules for power isolation. It sits at the rear corner where it is visible and reachable but out of the front's line of attack.
- **Evolution (Mk 1 → yellow)**: the orange beak lid had to reach the floor itself, so it was big and heavy and covered everything. The later build split the front into fixed prongs plus a light T flipper, which saves weight and puts more ground contact on fixed parts.

---

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Confidence |
|---|---|---|
| Left wheel + pod | mirror of the right | H |
| Servo | 9 g analogue, horn along X, at the rear-left of the bay, linked to the crossbar underside by a 1 mm Z-bend rod | M |
| Battery | 2S 150–180 mAh LiPo, rear-right of the bay in clear wrap | M |
| RX/ESC | combined receiver + dual brushed ESC board (green, 28 × 15), e.g. a micro "AWS-style" combo | M |
| Floor | 1.5–2 mm, holes for motor clamp screws | M |
| Prong infill | 100 % or thick walls; mass at the front for stability | L |
| Hinge pin | M3 threaded rod or long bolt, steel | H |
| Wire routing | servo lead to the RX across the bay front, motor leads through slots in the pod inner walls | M |
| Lower stem face | flat, no ribs (the ftl build); the aws63 stem had lengthwise ribs on the top | M |
| Battery charge lead | taped inside, reachable by lifting the flipper | L |

*(Photos are reasonably informative for the outer shell. The underside, the left side and the actuator linkage are never seen, so those sections are guesses.)*
