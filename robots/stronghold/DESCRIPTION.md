# Stronghold: full rebuild description from reference photos

Source photos (all cut out onto white by the AWS wiki):
- `robots/stronghold/reference/stronghold.aws72.webp`: AWS 72, 1217 × 1009 px, with a slight green colour cast. **Front-left three-quarter from about 35° above**, robot turned about 30° to its left so the front faces the lower left and the **right side** shows at the right. **Black front corner wedges**; the two **black fuzzy hook arms** are separate (no crossbar visible) and the left one is **raised**. The right side wheel (blue/teal hub) and the top-rear electronics housing with a **green slide-switch board** are visible.
- `robots/stronghold/reference/stronghold.aws74.webp`: AWS 74, 1061 × 850 px. **Front view, slightly from the right, about 30° above.** **Blue front corner wedges.** The two arms are joined by a **fuzzy crossbar** and rest down in front of the plate. A **steel rod** across the top, wires (red, blue, green, yellow) in the top opening, and the green switch board at the top right.
- `robots/stronghold/reference/stronghold.aws76.webp`: AWS 76, 1264 × 893 px. **Front-right three-quarter from about 30° above**, robot turned to its right so the **left side** shows at the left. **Black corner wedges**, arms with crossbar resting down. Shows the **silver spur gear on the left end of the arm shaft**, the left side pod with a **blue-hubbed, grey-tyred wheel**, and a badly **chewed/torn fuzzy top** at the rear.

Stronghold is a **two-wheel "fork and clamp" robot (a grabber/crusher-style clamp, or lifter)**. A **vertical aluminium front plate** has **two steel barbed forks** sticking out of slots at its foot, and **two curved black hook arms** pivot on a **gear-driven cross shaft** at the top front. They swing down in front of the plate to clamp an opponent onto the forks. Everything stated as fact is read from the photos; anything inferred is marked **(guess)**. All mm values are **estimates** (±15%), scaled from the AWS 101.6 mm (4 in) cube, from screw sizes (M2/M2.5 black socket/button heads ≈ Ø 4–4.5 mm) and from pixel ratios. Ratios are given against **W = front plate width ≈ 78 mm**.

---

## 0. Coordinate system and naming

- **+X** = robot's right, **+Y** = forward (toward the forks), **+Z** = up; mm. **Origin** = the point on the floor (z = 0) under the centre of the body footprint (mid-width between the side pods' outer faces, mid-length from the front plate to the rear of the body, **not** counting the forks). Side-profile angles are measured from the floor; arm angles from the +Y axis in the YZ plane.
- **Front** = the fork end. In all three photos the front faces the camera (AWS72 toward the lower left, AWS74 toward the camera, AWS76 toward the lower right).

| ID | Part |
|---|---|
| BD | black printed body/chassis (tub) |
| SP-L / SP-R | side pods (black printed, enclosing the wheels) |
| FP | aluminium front plate |
| FP-SL | two fork slots at the foot of the front plate |
| FK-L / FK-R | steel barbed forks |
| CW-L / CW-R | front corner wedges (black AWS72/76, blue AWS74) |
| AR-L / AR-R | curved hook arms (black fuzzy-skin print) |
| AR-X | arm crossbar (fuzzy mesh plate, AWS74/76) |
| AR-RT | arm root blocks on the shaft |
| SH | steel arm shaft along X |
| GR | silver spur gear on the left end of SH |
| GM | arm drive gearmotor and its pinion (hidden, partly seen as a black block) |
| BS-L / BS-R | shaft bearing bosses |
| TH | top-rear housing (black, fuzzy, with a lid) |
| SWB | green slide-switch board with LED |
| SP-AL | aluminium side/top-rear plate (right rear, AWS76) |
| WH-L / WH-R | drive wheels (blue/teal hubs, grey or black tyres) |
| RB | blue rear part (AWS74 right rear: blue wheel tread/bumper) |
| W | wires (red, blue, yellow, green, black) |
| S-xx | screws (listed per part) |
| DM, BAT, RX, ESC | drive motors, battery, receiver, ESCs (hidden, guess) |

---

## 1. Overall description in one paragraph

Stronghold is a **compact, squared-off robot** about **92 mm wide, 72 mm long (body) plus 32 mm of forks, and 38 mm tall**, printed in **matte black** with a **fuzzy/rough skin** on the top parts. Its whole front is a **flat brushed-aluminium plate**, about 78 mm wide and 32 mm tall, nearly vertical, fixed with small **black socket screws**. At the foot of the plate, at about one-third and two-thirds of its width, two **slots** let two **flat steel forks** pass through. These are thin steel blades set on edge, each about 35 mm long, sloping down to the floor, with an **arrow-like barb** near the tip. Small **triangular wedges** cover the two front bottom corners. Above the plate, a **steel rod** runs across the top of the body. On it pivot **two thick, curved black hook arms** (joined by a fuzzy crossbar in later versions) that arc forward over the plate and **hang down in front of it** to just above the forks. A **silver spur gear** on the rod's left end shows that the arms are **motor-driven through gears**. The two drive wheels (**blue hubs**, grey/black tyres) sit at the rear in **black side pods**. A **black housing** on the top rear carries a **green slide-switch board** with an LED. The robot's job is to **slide the forks under an opponent and clamp it down with the arms** ("Stronghold"), then push it out.

---

## 2. Part-by-part description

### 2.1 Body (BD)
- **Shape**: a printed tub about **78 mm wide (between the pods) × 70 mm long × 30 mm tall**, behind the front plate. Its top front edge is **chamfered** (about 45°, 6–8 mm) above the plate (seen as a sloping black strip in AWS76 and AWS72). The top centre is **open** (a window about **40 × 20 mm** between the arm roots), through which the wires and the steel rod are seen (AWS74, AWS76).
- **Material**: black FDM; the top surfaces are printed with **fuzzy skin** (rough, bobbly texture). The side pods and corner wedges are normal smooth prints with visible layer lines.
- **Bottom**: a black printed floor band shows under the front plate in AWS72 (about 4 mm tall strip at z = 2–6 with layer lines) **(seen)**.

### 2.2 Side pods (SP-L, SP-R)
- **Shape**: black printed **boxes on both sides**, about **8 mm wide × 70 mm long × 30 mm tall**, enclosing the wheels. Their **front-top corner is chamfered** (a sloping face from z ≈ 32 at y ≈ +10 down to z ≈ 18 at the front, seen at the right of AWS72 and the left of AWS76), so in side view each pod is a **wedge-fronted rectangle**.
- **Wheel opening**: the wheel shows through a large opening in the pod's outer face near the rear (AWS72 right: a blue/teal hub behind a black arch; AWS76 left: a blue hub with grey tread behind an opening, with a **small black triangular nub** on the pod side at about (−46, +10, 14)).
- **Screws**: AWS72 shows a screw on the right pod's front face at (+44, +30, 8) and one at the rear upper edge.

### 2.3 Front plate (FP) and fork slots (FP-SL)
- **Shape**: a flat **aluminium sheet about 1.5–2 mm thick**, **78 mm wide × 32 mm tall**, covering the front of the body at about y = +35. It is **nearly vertical**, leaning back about **5–10°**. Its corners are sharp.
- **Surface**: brushed aluminium, with **many scratches** (fine diagonal scratch marks all over in AWS76), some grime.
- **Screws S-FP**: black **socket button/cap screws** (M2.5, head Ø 4.5): **upper left** (x ≈ −32, z ≈ 30), **upper right** (x ≈ +32, z ≈ 30), and **mid-right** (x ≈ +30, z ≈ 18) in AWS72; similar positions in AWS74/76. A small round hole/screw near the top at x ≈ −10 (AWS72) **(seen)**.
- **Slots FP-SL**: two **rectangular slots** at the bottom edge, each about **4 mm wide × 10 mm tall**, open at the bottom edge, at **x ≈ −18** and **x ≈ +18**. The forks pass through them.
- **Bottom edge**: at about z = 5, sitting on the body's floor band.

### 2.4 Forks (FK-L, FK-R)
- **Shape**: flat **steel blades** about **1.5 mm thick**, set **on edge** (blade plane vertical, YZ), about **38 mm long** in total. Each has a **vertical root** about 10 mm tall inside the slot, then runs **forward and down at about 20–25°** to a **sharp point on the floor**. Near the tip, the upper edge has a **barb step**: the blade's top edge drops by about **3 mm** in a notch about 6 mm from the tip, then continues as a **narrow pointed tip** (an arrow/harpoon outline). The lower edge is straight.
- **Height**: about **10 mm tall** at the root, tapering to a point.
- **Position**: centre planes x = ±18; from y = +34 (inside the slot) to y ≈ **+68** (tip).
- **Look**: bright, ground steel edges (filed/ground bevel along the top edge in AWS72), darker flat faces.
- **Fixing**: held inside the body behind the plate, probably bolted to the floor or a printed block **(guess)**.

### 2.5 Front corner wedges (CW-L, CW-R)
- **Shape**: small **printed triangular wedges** at the two front-bottom corners, each about **12 mm wide × 20 mm long × 14 mm tall**, sloping down from z ≈ 14 at the plate to the floor at y ≈ +52 (slope about **35°**). Their outer faces are flush with the pod sides. Each has **one black screw** in its upper rear part (through into the body/pod).
- **Colour**: **black** in AWS72 and AWS76, **blue** in AWS74 (blue PLA with visible layers).
- **Position**: x ∈ [−46, −34] and [+34, +46], outboard of the forks.

### 2.6 Hook arms (AR-L, AR-R), crossbar (AR-X) and roots (AR-RT)
- **Shape**: each arm is a **thick curved bar**, about **8 mm wide (X) × 7 mm deep**, shaped like a **hook or question mark** in side view. It starts at a **root block** on the shaft at about **(±18, +18, 36)**, rises slightly, then arcs **forward over the front plate's top edge**, and curves **down in front of the plate** to a rounded tip. At rest (AWS74/76) the tip hangs about **5–10 mm above the forks**, at about **y = +40, z = 10** (just in front of the plate). The arc's outer radius is about **18–20 mm**.
- **Texture**: **fuzzy-skin black print**, very rough; the tips are rounded and slightly ragged.
- **Crossbar AR-X** (AWS74/76): a **flat fuzzy plate** about **30 mm wide × 10 mm deep × 5 mm thick** joining the two arms at the top of the arc, just above the plate's top edge (at about y = +32, z = 36). It makes the two arms one **U-shaped clamp frame**. AWS72 shows **no crossbar** and the arms look more round in section (tubular, Ø 8) with the left one **raised** about 30° (its tip at the plate's top left).
- **Root blocks AR-RT**: printed blocks about **10 × 12 × 8 mm** clamping the arms to the shaft, each with a **screw on top** (AWS76 shows a black socket screw on the left root).
- **Spacing**: the arms line up with the forks: x = ±18 (AWS74/76) so that each arm comes down **directly above a fork**.

### 2.7 Arm shaft (SH), gear (GR), bosses (BS) and arm motor (GM)
- **Shaft SH**: a **bright steel rod** about **Ø 3–4 mm × 70 mm**, along X at about **(0, +14, 34)**, seen across the top opening in AWS74 and AWS76.
- **Gear GR**: a **silver (steel or brass-nickel) spur gear** about **Ø 10 mm × 3 mm**, about **20–24 teeth**, on the **left end** of the shaft at x ≈ −30, beside the left bearing boss (AWS76 close-up). A **short silver shaft stub** (Ø 2, 4 mm long) pokes out of a black block to its left at about (−38, +16, 34): that is probably the **pinion/motor output** or a second idler **(guess)**.
- **Bosses BS**: black printed cylindrical bosses about **Ø 9 × 8 mm** around the shaft near each end.
- **Arm motor GM**: hidden in the black block at the left front top (about **(−36, +6, 28)**): probably an **N20 gearmotor** (high ratio) along Y or X, driving GR through a pinion **(guess, medium)**.

### 2.8 Top-rear housing (TH) and switch board (SWB)
- **Shape**: a black printed **box/lid** over the rear half of the top, about **60 × 30 × 10 mm**, top at z ≈ 38. Its rear end slopes down (AWS72 right: a chamfered, notched rear edge with a slot). In AWS76 its fuzzy top is **badly chewed/torn** (ragged edges, spinner damage) and a **blue tape** piece sits on top at the far right.
- **Switch board SWB**: a small **green PCB** about **14 × 6 mm** carrying a **silver slide switch** and a **green LED** (lit in AWS72), set into the top of the housing at the right rear (about (+12, −10, 38)). AWS74 shows it at the top right with a **blue mark** next to it.
- **Screws**: two or three black screws on the housing top (AWS72: one near the front left, one at the right).
- **Visible inside**: an **orange/brown capacitor-like part** next to the switch board (AWS72) and wires.

### 2.9 Wires (W)
- Through the top window: **red**, **blue**, **yellow**, **green** and **black** silicone wires (AWS74: a red/blue loop with a **blue heat-shrink** joint; AWS76: red/yellow loops; AWS72: two red wires running from the top housing to the front and a red/blue bundle behind the plate).

### 2.10 Wheels (WH-L, WH-R) and blue rear part (RB)
- **Position**: **two wheels at the rear**, inside the side pods, axles along X at about **y = −18**, z ≈ 14, centre planes x ≈ ±40.
- **Size**: about **Ø 28 × 8 mm**.
- **Look**: **blue/teal printed hubs** (AWS72, flat face with a hub boss) with **grey or black tyres** (AWS76 shows a grey ribbed tyre on a blue hub). The wheels stand slightly proud of the pods' bottom edge to touch the floor.
- **RB (AWS74)**: a **blue curved surface** at the far right rear, probably the **right wheel's blue tyre/hub** seen through the pod, or a blue rear bumper **(guess: the wheel)**.

---

## 3. Per-view descriptions (for silhouette matching)

### 3.1 AWS72 (front-left, 35° down)
- **Outline**: a squat block whose front is the **grey aluminium rectangle**, with **two long, thin steel forks** pointing toward the lower left from slots at its foot, **two black triangular corner wedges** at its lower corners, and **two black curved hooks** above it (the left raised and arching up, the right curving down to the plate). Behind: a black top housing with a green switch board; at the right, a side pod with a blue/teal wheel.

### 3.2 AWS74 (front, 30° down)
- **Outline**: the aluminium plate centred, the two forks pointing toward the camera at the lower left and lower centre, **blue corner wedges** at both lower corners, the **U-frame of arms** hanging down in front of the plate (two legs with rounded tips just above the forks, joined at the top by a fuzzy crossbar), the steel rod and wires in the window above, the switch board at the top right.

### 3.3 AWS76 (front-right, 30° down)
- **Outline**: the plate at the centre right, the forks pointing toward the lower right, black corner wedges, the U-frame of arms, the **left side pod with the blue/grey wheel** at the left, and the **silver gear** on the shaft's left end. The torn black top behind.

### 3.4 Top view (synthesised)
- A 92 × 70 rectangle (body + pods), the plate as a line across the front at y = +35, two thin fork lines from y = +35 to +68 at x = ±18, corner wedge triangles at the front corners to y = +52, the arms as two 8-wide bars from the shaft (y = +14) forward to y = +42, the top window and rear housing.

### 3.5 Side view (synthesised, left)
- A rectangle 70 × 32 with a chamfered top front, the pod's wedge front, the wheel circle Ø 28 at the rear, the plate as a near-vertical line at the front, the fork as a thin triangle from (y +34, z 10) to (y +68, z 0), the corner wedge triangle, and the arm hook from (y +14, z 34) up to z ≈ 42 and down to (y +40, z 10).

### 3.6 Rear view (inferred)
- Two pods with wheels at the outer sides, a black rear wall between, the housing's sloped rear edge on top.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W (78) | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| BD | tub | 78 × 70 × 30 | 1 × 0.9 × 0.38 | black FDM (fuzzy top) | — | 1 |
| SP | pod box | 8 × 70 × 30 | 0.1 × 0.9 | black FDM | integral/screwed | 2 |
| FP | flat plate | 78 × 32 × 1.8 | 1 × 0.41 | aluminium | 3–4 × M2.5 black | 1 |
| FP-SL | slot | 4 × 10 | — | — | — | 2 |
| FK | barbed blade on edge | 38 × 10 × 1.5 | 0.49 × 0.13 | steel | inside body (guess bolted) | 2 |
| CW | triangle wedge | 12 × 20 × 14 | 0.15 × 0.26 | black / blue FDM | 1 screw each | 2 |
| AR | hook bar | 8 × 7 section, ~60 developed | 0.1 | black fuzzy FDM | root block on SH | 2 |
| AR-X | flat bar | 30 × 10 × 5 | 0.38 | black fuzzy | integral | 1 (74/76) |
| AR-RT | block | 10 × 12 × 8 | — | black | screw onto SH | 2 |
| SH | rod | Ø 3.5 × 70 | 0.9 | steel | bosses | 1 |
| GR | spur gear | Ø 10 × 3, ~22 T | 0.13 | silver steel | on SH | 1 |
| BS | boss | Ø 9 × 8 | — | black | integral | 2 |
| TH | housing | 60 × 30 × 10 | 0.77 × 0.38 | black fuzzy | 2–3 screws | 1 |
| SWB | PCB + switch | 14 × 6 × 3 | — | green, silver, green LED | set in TH | 1 |
| WH | wheel | Ø 28 × 8 | 0.36 | blue hub, grey/black tyre | motor shaft | 2 |
| S | socket/button | M2.5, head Ø 4.5 | — | black | various | ~12 |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| FP ↔ BD front | screwed | 0 |
| FK ↔ FP-SL sides | passing through | 0.5–1 |
| FK root ↔ BD inner mount | bolted (guess) | 0 |
| FK tip ↔ floor | touching | 0 |
| CW ↔ BD/SP front corners | screwed | 0 |
| CW bottom ↔ floor | near | 0–1 |
| CW inner face ↔ FK | side by side | 14–16 |
| AR inner/outer faces ↔ FK planes | aligned above | 0 sideways |
| AR tip ↔ FK top edge (rest) | above | 5–10 |
| AR back ↔ FP front face (rest) | in front | 3–5 |
| AR arc ↔ FP top edge | over it | 2–4 |
| AR-RT ↔ SH | clamped | 0 |
| GR ↔ SH | fixed | 0 |
| GR ↔ GM pinion | meshing | 0 |
| SH ↔ BS | bearing fit | 0.1 |
| TH ↔ BD top rear | screwed | 0 |
| SWB ↔ TH | set in | 0 |
| WH outer face ↔ SP inner wall | inside the pod | 1–2 |
| WH bottom ↔ floor | touching | 0 |
| WH top ↔ BD top | below the top | about −10 (not invertible on its wheels) |
| BD floor ↔ ground | clearance | 2–3 |

---

## 6. Mechanism

1. **Drive**: two rear wheels, differential drive, with the **forks and corner wedges as the front skids** **(guess: N20 gearmotors)**.
2. **Clamp/lifter arms**: the arm motor turns the shaft SH through GR. The arms swing about SH (axis at (0, +14, 34)). **Downward**, their tips press onto anything sitting on the forks, **clamping** it (fork below, hook above). **Upward**, they open wide (AWS72 shows one raised about 30°) to let an opponent onto the forks. With the arms down hard, the robot can **drag/push the opponent** without it escaping. Rotating the arms further back would also let them act as a **self-righter** if the robot is flipped **(guess, medium)**.
3. **Forks**: passive; the barbs hold an opponent's edge.

---

## 7. Assembly order (suggested rebuild)

1. Print BD with the pods, floor, window, shaft bosses and fork mounts; print TH, the corner wedges and the arm frame (fuzzy skin on top parts).
2. Fit the two drive motors and wheels in the pods.
3. Fit the arm motor; slide the shaft through the bosses with the gear GR on the left end and the arm root blocks; screw the roots on.
4. Fit the forks through the plate slots into their mounts.
5. Screw the aluminium front plate on (3–4 × M2.5).
6. Fit the electronics (battery, receiver/ESCs, arm motor driver) in the body; route the wires.
7. Screw on the corner wedges and the top-rear housing with the switch board.

---

## 8. Hidden / uncertain list
- Arm motor type and gear ratio; whether the arms are a clamp, lifter, self-righter, or all three.
- Fork mounting inside the body.
- Wheel count (2 rear is assumed; front wheels hidden behind the plate are possible but unlikely given the forks).
- Whether the wheels stick out above the top (invertibility).
- All mm ±15%.

---

## 9. Coordinate frame (restated)
- Origin on the floor under the body footprint centre; +X right, +Y forward, +Z up; mm.
- Body x ∈ [−46, +46] (incl. pods), y ∈ [−35, +35], z ∈ [2, 38]. Plate at y +35…+37, z 5–37. Forks x = ±18, y +34…+68, z 0–10. Corner wedges to y +52. Shaft (0, +14, 34). Arm tips at rest (±18, +40, 10). Wheels axles y = −18, z = 14, x = ±40.
- Overall bounding box: **92 × 103 × 42** — **over the 101.6 cube in length**; see §13.2.

## 10. Profiles as math (for rebuilding curves)

**10.1 Fork side profile (YZ, x = ±18).** Polygon: (34, 0) → (68, 0) (straight lower edge to the point) → (60, 2.5) → (60, 5.5) (the 3 mm barb step) → (34, 10) (upper edge rising back to the root) → back to (34, 0). The upper edge between the root and the barb slopes at atan(4.5/26) ≈ 10°; the tip from the barb to the point at atan(2.5/8) ≈ 17°.

**10.2 Arm centreline (YZ, x = ±18), rest pose.** Starting at the shaft centre S = (14, 34):
- straight segment from S at +25° (rising forward) for 10 mm → (23.1, 38.2);
- circular arc of radius R = 9, centre C = (27, 30), sweeping clockwise from 115° to −30° (over the top and down the front) → ends at (34.8, 25.5);
- straight leg from (34.8, 25.5) running down and slightly forward at about −72° for 16 mm → tip at about (39.5, 10.5), rounded with R 4.
So the arm's outer curve encloses the plate's top edge at (35, 37) with about 2–4 mm clearance.

**10.3 Arm swing.** Tip radius from S: √((39.5 − 14)² + (10.5 − 34)²) ≈ 34.7 mm. Tip position as a function of the swing angle φ (positive = arms up): y = 14 + 34.7 cos(−42.7° + φ), z = 34 + 34.7 sin(−42.7° + φ). At φ = +30° (AWS72 left arm) the tip is at (47.9, 26.4), above the plate top level in front.

**10.4 Corner wedge (YZ).** Triangle (35, 0), (52, 0), (35, 14): slope atan(14/17) = **39°**.

**10.5 Pod front chamfer (YZ, x = ±42).** From (10, 32) to (35, 18): slope atan(14/25) = 29°.

**10.6 Wheels.** (y + 18)² + (z − 14)² = 14² at x = ±40.

## 11. Pixel-based measurements (independent check)

- **AWS74** (1061 px): plate width from its left edge (200, 160–490) to its right edge (950, 270–560) ≈ **750 px** along the near bottom edge; plate height at the centre ≈ **230 px** (y 300 → 530). Ratio h/w = 0.31; the view is from 30° above, so a vertical plate is shortened by cos 30° ≈ 0.87 → true h/w ≈ 0.35 → with W = 78, **h ≈ 28–32**. ✓
- **AWS74** fork length from the slot (330, 380) to the tip (130, 670) ≈ **350 px**, pointing toward the camera (foreshortened by roughly 0.6) → 350/750 × 78 / 0.6 ≈ **61 mm**?? Too long; the forks are nearer the camera than the plate, enlarging them by about 1.3 → **47**; with the 30° view the true length is between 35 and 47. **Use 38.**
- **AWS74** screw head ≈ **25 px** → 25/750 × 78 ≈ **2.6 mm**? Too small for a head; it is the visible black socket recess plus rim (the head is countersunk/flush). Use M2.5 button **Ø 4.5**.
- **AWS74** arm width ≈ **75 px** → 75/750 × 78 ≈ **7.8 mm** ✓ (8 mm).
- **AWS74** arm spacing (left leg centre x ≈ 230, right leg centre x ≈ 545) ≈ **315 px** → **33 mm** → arms at ±16.5 ✓ (±18 used, matching the forks).
- **AWS76** (1264 px): gear GR ≈ **55 px** across; plate width ≈ **830 px** (x 200 → 1030 at the top edge) → 55/830 × 78 ≈ **5.2 mm**?? The gear is farther (behind the plate top, about 20 mm deeper) and at the left; corrected ≈ **7–10 mm**. **Use Ø 9.**
- **AWS72** (1217 px): right wheel hub visible height ≈ **130 px**; plate width ≈ **620 px** along its top edge (oblique) → 130/620 × 78 / cos 45° ≈ **23 mm** visible part → full wheel ≈ **26–30 mm**. ✓

## 12. Several independent estimates of key sizes

| Quantity | Method A (rules / parts) | Method B (ratios) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Plate width | body 78 + pods | 1 W | — (reference) | **78** |
| Overall width | ≤ 101.6 | 1.18 W | AWS74 plate + pods ≈ 1.15 × plate | **92** |
| Body length | ≥ wheel + plate | 0.9 W | AWS72 side ≈ 0.9 × plate | **70** |
| Height | — | 0.41 W (plate) + housing | AWS74 plate 28–32, housing above +6 | **38 (top), 42 (arms)** |
| Fork length | knife-blade forks 30–40 | 0.49 W | 35–47 | **38** (34 beyond the plate) |
| Arm section | printed 7–10 | 0.1 W | 7.8 | **8 × 7** |
| Arm spacing | aligned with forks | — | ±16.5 | **±18** |
| Wheel Ø | 26–30 | 0.36 W | 26–30 | **28** |
| Gear Ø | 8–12 small steel gear | — | 7–10 | **9–10** |

## 13. Consistency check: conflicts and reconciliation
1. **Fork length**: pixel estimates range from 35 to 61 depending on the perspective correction. Forks longer than about 34 mm beyond the plate break the size limit (see 2). **Reconciled: 38 total, 33 beyond the plate.**
2. **Size limit**: body 70 + forks 33 = **103 > 101.6**. Either the body is shorter (≈ 66) or the forks are 30. AWS74's front view cannot settle the depth. **Reconciled: body 66 long (y ∈ [−33, +33]), plate at y +33, fork tips at y +66 → overall 99.** Update §9 accordingly: shaft at (0, +12, 34), arm tips at y ≈ +38.
3. **Arm crossbar**: missing in AWS72, present in AWS74/76: **two versions**. In AWS72 the left arm is raised while the right is down, which means the arms were **independent** (or one was bent) in that version.
4. **Corner wedge colour**: black (72, 76) vs blue (74): replacement parts; same shape.
5. **Invertibility**: the wheels (Ø 28, axle z 14 → top z 28) are below the body top (38). **Not invertible by wheels**; hence the arms likely also serve to self-right **(guess)**.
6. **Spec says wedge**: the forks and corner wedges make it wedge-like, but the arms are its weapon. Describe as a **fork-and-clamp** robot.

---

## 14. Why the designer did it (per part, from several angles)

Common lens: **adversarial**. For each part: what can attack it (spinners, wedges, lifters, flippers, wall slams, inversion), how it survives, and how it helps win. Then construction reasons.

- **Steel barbed forks through the plate**
  - Fight: forks beat wedges: their thin points get under opponents' edges first. Being steel and set on edge, they are stiff vertically and survive being driven over. The barbs hook the opponent's edge so it cannot simply back off. Passing them through slots lets them be mounted deep inside the body (strong) while the plate covers the mounts.
  - Weak points: narrow forks can miss an opponent between them; on-edge blades can be pushed sideways and bent.
  - Construction: cut from steel strip (or knife blades), easy to replace.
- **Aluminium front plate**
  - Fight: the main armour, facing spinners and pushers. Aluminium resists cuts much better than printed plastic (all the scratches show it took hits) and spreads impacts. It also gives the clamp something solid to squeeze against.
  - Construction: a flat rectangle with two slots and 3–4 screws.
- **Hook arms clamping down from above**
  - Fight: the robot's name: once an opponent is on the forks, the arms close over it, holding it so it cannot escape or flip away; then the robot drives it into the wall or out of the arena. Hooks that hang in front of the plate also protect the plate's top edge and stop opponents riding up over the robot.
  - Weak points: the thin printed arms (8 mm) can be broken by spinners (fuzzy-skin texture cushions small hits); the gear train takes shock loads when an opponent lands on the arms.
  - Construction: fuzzy-skin printing hides layer lines and adds grip on opponents; the crossbar (later version) ties both arms together so they move as one stiff frame.
- **Shaft + spur gear drive**
  - Fight: a geared motor holds position against back-driving (the clamp stays shut without power); a metal gear survives better than a printed one.
  - Construction: off-the-shelf small steel gear on a steel rod, simple bosses.
- **Corner wedges**
  - Fight: cover the front corners (the weak points beside the plate) and deflect opponents coming from an angle onto the forks; they also protect the side pods' front.
  - Construction: small replaceable prints (two colours seen).
- **Side pods enclosing the wheels**
  - Fight: protect the wheels from horizontal spinners and hooking; flat sides.
  - Weak points: the wheels are hidden inside and below the top, so the robot cannot drive inverted.
- **Two rear wheels**
  - Fight: weight on the forks keeps them on the floor; two-wheel drive saves weight for the clamp motor and aluminium plate.
- **Top-rear housing with switch board**
  - Rules: accessible power switch with an LED to show "armed/on" status.
  - Weak points: on top, exposed to overhead hits (AWS76 shows heavy damage there).
- **Black screws**
  - Construction: socket screws are easy to tighten and look tidy; black blends in.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre, mm) | Confidence |
|---|---|---|---|---|
| Drive motors | 2 × N20 gearmotors along X in the pods | 12 × 10 × 25 | (±28, −16, 14) | medium |
| Arm motor | N20 high-ratio gearmotor (e.g. 298:1), pinion meshing with GR | 12 × 10 × 25 | (−32, +2, 28), shaft along X | medium |
| Fork mounts | printed blocks with M2 bolts through the fork roots | 6 × 12 × 10 | (±18, +26, 6) | low |
| Battery | 2S 300 mAh LiPo | 45 × 25 × 8 | (0, −10, 10) under the housing | medium |
| Receiver/ESC | combined board with three channels (2 drive + arm) | 30 × 20 × 5 | (0, −5, 24) | medium |
| Switch | slide switch on the green board (seen) | 14 × 6 | (+12, −10, 38) | high |
| Plate backing | printed front wall 2 mm behind FP | 78 × 2 × 30 | y +31 | medium |
| Arm stops | end stops limiting the arm swing | — | at the root blocks | low |
| Wiring | red/black power, three-core motor leads | — | through the top window | high (seen) |
