# GYROniNO: full rebuild description from the reference photos

Source photos (three, all from about the same angle):
- `robots/gyronino/reference/gyronino.aws72.webp` (1310 × 1182 px): AWS 72. The weapon blade is **blue-painted steel** with bright ground edges. The feet are **black** with **bare aluminium/steel tips**. The gyro housing is **bright orange**.
- `robots/gyronino/reference/gyronino.aws74.webp` (1412 × 1143 px): AWS 74. The blade is a **dark blue** hooked shape, the feet are **blue printed**, the housing is **salmon orange**, and a pale-green nose cap is visible.
- `robots/gyronino/reference/gyronino.aws76.webp` (1748 × 1245 px): AWS 76. The blade is **dark grey/black steel**, the feet are **blue printed**, the housing is salmon orange and the frame is white.

All three are cut out onto white. The white/translucent parts carry a **pale green cast** from the cut-out: the "white" frame looks green in 74. The camera is at the **robot's left-front-above**, about **25–30° down**. The feet point to the image **lower right**, which is the robot's **front**. The box with the orange end plate is at the image **left**, which is the robot's **rear**. We see the robot's **left side** and its front-left quarter.

**GYROniNO is a walker.** It has **no wheels**. It moves by **gyroscopic precession**:
- A heavy blade spins about a fore-aft axis on a **gyro unit**.
- The gyro unit is carried on two arms and can be **tilted** relative to the rear body.
- Tilting a spinning gyro creates a torque at right angles to the tilt. That torque rocks and twists the robot over its **two front feet and a rear skid**, so it shuffles from foot to foot.

As a walker it may run at the higher walker/shuffler weight allowance (above 150 g). The size limit still applies (101.6 mm cube at the start).

Facts are read from the photos; inferences are marked **(guess)**. Sizes are **estimates in mm**, from:
- the 101.6 mm cube;
- the spec draft (a 60 × 44 × 44 body prism, a gyro ring of r 41/37 at y 40, a 124 mm bar weapon at y 64, two feet and a tail skid);
- pixel ratios using the **ring outer Ø (≈ 56 mm)** and the **M3 socket screw head (5.5 mm)** as scales.

Ratios are against **H = body box height ≈ 40 mm**.

---

## 0. Coordinate system and naming

- **Origin O** = floor point (z = 0) under the gyro pivot (the arm-hub screw), mid-width.
- **+X** = robot right, **+Y** = forward (toward the foot tips), **+Z** = up. mm.
- Extents (reconciled §12): rear box x ∈ [−21, +21], y ∈ [−58, −16], z ∈ [4, 42]. Gyro ring centre (0, 0, 40), Ø 56. Gyro axis along Y. Housing y ∈ [+4, +20]. Bevel crown y ∈ [+20, +28]. Blade plane y ≈ +32. Feet tips reach y ≈ +44. Overall about 100 long × 60 wide (blade sweep 84) × 82 tall (blade top).

| ID | Part |
|---|---|
| BX | rear body box (white/translucent printed, open-top tray with lid ribs) |
| EP | rear end plate (orange printed, 4 screws) |
| SK | orange sacrificial skid strip on the box's lower rear edge (torn edges) |
| TS | tail skid under the box (hidden; from spec) |
| HN-L, HN-R | pale-green translucent horns/fins on the box top, just behind the ring |
| AR-L, AR-R | white printed arms running from the box sides up and forward to the gyro pivot |
| PV | pivot screws: M3 socket head through the arm into the gyro hub (one each side) |
| HB | black printed hub/bushing at the arm tip (on the gyro axis) |
| RG | gyro frame ring: orange-printed annulus with a steel rim band, about Ø 56 × 5 |
| SP | steel cross spokes (two flat bars in a "+" or "×") inside RG |
| RT | black toothed rotor disc behind the spokes (motor bell with a printed toothed cover) |
| MW | weapon outrunner inside RG (label "15…" visible through the spokes) |
| GH | orange gyro housing (bearing block) at the front of RG, with screw holes |
| BC | black bevel-toothed crown (≈ 22 teeth) on the gyro axis, in front of GH |
| NC | pale-green nose cap / front bushing on the axis (74) |
| BL | weapon blade: a bar with a forked claw at one end and a fishtail at the other |
| FT-L, FT-R | front feet: blue (74, 76) or black with metal tips (72) spikes |
| W | black wires from the box to the gyro unit (a twisted bundle loop over the box) |
| M-T, BAT, ESC, WESC, RX, SW | hidden tilt actuator and electronics |

---

## 1. Overall description in one paragraph

GYROniNO is an odd-looking **gyro-walker spinner**. At the rear is a **white printed box** about 42 wide, 42 long and 38 tall. It has a translucent shell with visible internal ribs and an **orange end plate** held by four Phillips screws, and a ragged **orange skid strip** along its lower rear edge. From the front of the box, **two white arms** sweep up and forward to a pivot about 40 mm above the floor. The arms carry the **gyro unit** on M3 socket screws:
- a vertical **ring frame** (orange face, steel rim, Ø 56) braced by **steel cross spokes**, with a **black toothed motor rotor** spinning inside it;
- an **orange bearing housing** bolted to the ring's front;
- a **black bevel-toothed crown**;
- at the front, a **long steel blade**, about 84 mm from end to end, with a **two-pronged hooked claw** at one end and a **flared fishtail** at the other, spinning about the fore-aft axis.

**Two long pointed feet** (printed, sometimes with metal tips) splay forward and down from under the gyro unit. **Two pale-green horns** stand up from the box's front top. A **black wire loop** runs from the box over to the gyro unit. There are no wheels. The robot rests on the feet and the rear skid, and walks by tilting the spinning gyro.

---

## 2. Part-by-part description

### 2.1 Rear box (BX)
- **Shape**: a printed **rectangular tray**, about **42 (X) × 42 (Y) × 38 (Z)**, z 4 to 42. It is translucent white with **visible infill/ribs**: a diagonal brace and internal partitions show through the walls. The top is partly open (wires emerge from it), with a recessed lid frame along the top edges. The **front lower part** blends into the arms' bases.
- **Wall thickness**: about 1.6–2 mm (translucent). Internal pockets for the battery and electronics (from spec: a battery pocket 36.5 × 17.5 × 11.5 at the bottom, an ESC pocket above it, and a weapon ESC pocket at the top).
- **Bottom**: a 2–4 mm gap to the floor at the front. The rear rests on the tail skid TS.

### 2.2 End plate (EP) and skid strip (SK)
- **EP**: a flat **orange plate** about **42 × 38 × 2**, covering the rear face of the box. Its top corners are cut at **45°** (a 6 mm chamfer), giving a shield/coffin outline. It has **four silver Phillips screws** near the corners (image 76: (190, 690), (370, 745), (110, 795), (205, 1030)).
- **SK**: a **second orange strip** about **42 × 14 × 2**, laid over the lower part of EP or glued at an angle. Its **edges are torn and fibrous** (image 76 (270–440, 790–1080); image 74 (100–160, 600–700)). It is a **sacrificial bumper** that has been chewed by opponents' weapons and dragged on the floor.

### 2.3 Horns (HN-L, HN-R)
- **Shape**: two **pale-green translucent spikes**, each about **6 × 10 (base) × 18 tall**. They are tapered triangular fins with flat tops, standing on the box's front top corners at x ±12, y −18, z 42 to 60 (image 76 (550–700, 320–470); image 74 (495–640, 175–260)).
- **Role (guess)**: inverted feet / self-righting points. When the robot is on its back, the horns and the ring rim form a tripod, so the gyro-walk still works upside down.

### 2.4 Arms (AR-L, AR-R)
- **Shape**: white printed **tapered beams**, each about **8 thick (X)**. The base is 30 tall where it joins the box's side at its front half (y −30 to −10, z 4 to 34). They taper to a **rounded tip of r 9** around the pivot at **(±25, 0, 40)**. The upper edge is straight, sloping up about 20° toward the front. The lower edge is concave. Layer lines and a few **scuffs** are visible.
- The **left arm** is fully visible in all photos: it runs from the box's left side up to the black hub HB at the ring centre. The right arm is hidden and assumed symmetric.

### 2.5 Pivot (PV) and hub (HB)
- **PV**: an **M3 socket-head cap screw** (black, head Ø 5.5) in each arm, about **6 mm behind the arm tip** (image 76 (830, 640); 74 (560, 545); 72 (510, 660)). Read as the **tilt pivot** (medium). It might instead be a clamp screw on a shaft through the hub (low).
- **HB**: a **black printed collar/bushing**, Ø 12 × 8, at the arm tip on the gyro axis. It joins the arm to the ring's centre hub where the spokes cross.

### 2.6 Gyro frame ring (RG) and spokes (SP)
- **RG**: a flat **annulus**, about **Ø 56 outer, Ø 48 inner, 5 thick (Y)**. Its face is **orange printed**, with a **bright steel rim band** about 1.5 mm wide around the outside (a laminated steel hoop, or a steel ring with orange paint) (guess). There are small screw holes at about 12 o'clock and 6 o'clock (a nut/insert at the top in 72 and 74). Where it **meets the gyro housing GH**, it has **tabs** at the top and bottom (72: a square steel lug at the top, (600–640, 290–330)).
- **SP**: **two steel flat bars**, about **3 × 1.5**, in a cross. In 76 and 74 the cross is rotated about 15° from vertical. The bars are **scratched/galvanised grey**. They tie the ring to the central hub.
- **Role**: a **stationary frame and guard** around the motor rotor. It ties the arms' pivot (at the back, via HB) to the housing (in front).

### 2.7 Rotor disc (RT) and weapon motor (MW)
- **RT**: a black **toothed disc**, about **Ø 40 × 8**, with about 18 coarse **spur-like teeth** (76 (850–1160, 360–760)). It is seen through the spokes and spins inside the ring. In 72 it reads as a black smooth disc with a low lip, so the teeth may be a printed cover or fan (guess).
- **MW**: a **brushless outrunner** sits behind RT. A **white label with "15…" text** is visible through the lower spokes in 76 (850–960, 760–830). Estimated **Ø 28 × 20**, on the gyro axis, its stator fixed to the hub/housing.
- **Role (guess)**: RT is the motor's bell cover. It adds rotating mass (more gyro momentum) and grips the opponent if the ring is hit.

### 2.8 Gyro housing (GH)
- **Shape**: an **orange printed block** fixed to the front of RG, about **32 wide (X) × 16 deep (Y) × 40 tall (Z)**. Its front edges are rounded (r 6), and it has a **round boss** on the axis.
- **Holes and screws**: a horizontal **socket hole** and **two Phillips screws** on its left lower face (72 (870–990, 750–830)); a hole and screw on its top (72 (720–760, 300–330)); two screw holes at the lower front in 74 (900–990, 680–760).
- **Role**: holds the **front bearing** of the weapon shaft and the base of the feet (guess). It is the structural core of the gyro unit.

### 2.9 Bevel crown (BC) and nose cap (NC)
- **BC**: a black printed **bevel-toothed crown**, about **Ø 40 outer × 9 deep**, with about **22 teeth**. The teeth are triangular and sloping, like a bevel gear facing forward (76 (1100–1370, 260–620); 74 (900–1120, 240–580)). It sits on the axis directly in front of GH and **spins with the weapon** (guess). The **blade's hub** is clamped between BC and the nose.
- **NC**: a pale-green printed **cap**, about **Ø 12 × 10**, on the axis at the front (74 (1110–1160, 310–390)). Read as the shaft-end collar.
- **Alternatives**: BC could be a true bevel gear meshing with a hidden pinion (for example a tilt drive), but no pinion is visible. More likely it is a **toothed impact ring / hub** (medium).

### 2.10 Blade (BL)
- **Material**: flat **steel**, about **3 mm thick**. It is painted (blue in 72 and 74, grey-black in 76) with **ground bright edges** (72 shows bright scratched faces at the tips).
- **Outline**: overall about **84 mm** tip to tip, centred on the axis. It has two **different** ends:
  - **Claw end**: a **broad fan** about 34 wide, with a **deep semicircular notch** (r 9) cut in the middle of its outer edge. This leaves **two prongs**, the leading one hooked (76 (900–1140, 50–290); 74 (800–1020, 40–260)). The arm from the hub to the claw is about 14 wide.
  - **Fishtail end**: a slim arm (≈ 10 wide) that **flares** into a fishtail tip about **26 wide**, with concave flanks of r ≈ 20 (76 (1360–1700, 500–880); 72 (1050–1270, 30–200)).
- **Mounting**: on the gyro axis at y ≈ +32, clamped between BC and NC. It spins in the **XZ plane** (vertical, facing forward).
- **Balance**: the claw end is wider but has the notch; the fishtail end is longer. The arm lengths are about 40 (claw) and 44 (fishtail) to balance (guess).

### 2.11 Feet (FT-L, FT-R)
- **Shape**: long **pointed blades**, each about **50 long × 10 wide × 6 thick**. The section is triangular, with a sharp ridge on top, tapering to a **point**. Each foot starts at a **root block** (14 × 12 × 8) under GH/RG and runs **forward and down** to the floor, splaying outward by about 10°.
- **Variants**:
  - 76 and 74: **blue PLA**; the right foot's tip is at image (1410, 940), the left at (1470, 1170).
  - 72: **black printed with bare metal (aluminium) caps** on the tips, ground and scratched (72 (860–1020, 970–1110)).
- **Spec**: foot profile from (y 34, z 2) to (y 92, z −9.5) in the spec frame (origin elsewhere), 6 thick, at x ±16.
- A **third, longer spike** in 74 (1100–1200, 600–840) is the far-right foot seen past the blade (same part, FT-R).

### 2.12 Wires (W)
- A **black twisted bundle** (three motor phases, about 22 AWG) loops out of the box top (76 (440–620, 510–590)) and runs over to the gyro unit, entering behind the ring. There is slack to allow the tilt motion.

---

## 3. Per-view descriptions

### 3.1 Left-front iso (all three photos)
- The rear box at the left, end plate toward the camera (orange, 4 screws), skid strip at its lower front-left (which is actually the rear corner).
- The arm rising to the right with the pivot screw.
- The ring as an ellipse (aspect about 0.85, so the gyro axis is about 30° off the line of sight) with spokes and the black rotor inside.
- The housing and bevel crown to the right, the blade at the upper right (claw up in 74 and 76, fishtail up in 72).
- The feet stretching to the lower right.

### 3.2 Front view (inferred)
- The blade's full outline face-on in front of the bevel crown and housing. Behind them the ring Ø 56 with the arms at its sides and the horns peeking above. The two feet as triangles splaying down to the floor at x ±22.

### 3.3 Left side view (inferred)
- Box at the rear (42 long, 38 tall). The arm sloping up from the box front to the pivot at (y 0, z 40).
- The ring as a 5 mm vertical bar 56 tall, the housing 16 deep, the crown 9 deep and the blade as a 3 mm vertical line 84 tall at y 32.
- The foot sloping from under the housing (z 12) to the floor at y 44. The horns on the box top.

### 3.4 Top view (inferred)
- Box 42 × 42, horns at its front corners.
- Arms at x ±25 from y −30 to 0.
- The ring as a 56 × 5 bar at y 0, the housing 32 × 16, the crown Ø 40, the blade as an 84 × 3 bar along X at y 32.
- Feet splaying forward to (±22, 44).

### 3.5 Rear view (inferred)
- The orange end plate with its chamfered top corners and 4 screws; the skid strip across the lower part. The ring and blade rising above and behind.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to H | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| BX | tray | 42 × 42 × 38 | 1.05 × 1.05 × 0.95 | white PETG/nylon | — | 1 |
| EP | chamfered plate | 42 × 38 × 2 | 1.05 | orange | 4 × M2 screws | 1 |
| SK | strip | 42 × 14 × 2 | — | orange | glued/screwed | 1 |
| HN | fin | 6 × 10 × 18 | 0.45 tall | pale-green | printed on BX | 2 |
| AR | tapered arm | 40 long × 30→18 × 8 | 1.0 | white | integral with BX | 2 |
| PV | M3 socket screw | M3 × 10 | — | black steel | — | 2 |
| HB | collar | Ø 12 × 8 | 0.3 | black | on PV/axis | 1–2 |
| RG | ring | Ø 56/48 × 5 | 1.4 | orange + steel rim | to GH, tabs | 1 |
| SP | cross bars | 2 × (48 × 3 × 1.5) | 1.2 | steel | in RG | 2 |
| RT | toothed disc | Ø 40 × 8 | 1.0 | black | on MW bell | 1 |
| MW | outrunner | Ø 28 × 20 | 0.7 | — | stator in hub | 1 |
| GH | block | 32 × 16 × 40 | 0.8 × 0.4 × 1.0 | orange | screws to RG | 1 |
| BC | bevel crown | Ø 40 × 9 | 1.0 | black | on shaft | 1 |
| NC | cap | Ø 12 × 10 | 0.3 | pale-green | shaft end | 1 |
| BL | claw/fishtail bar | 84 × 34 (max) × 3 | 2.1 | steel | clamped BC–NC | 1 |
| FT | spike foot | 50 × 10 × 6 | 1.25 | blue / black + metal tip | under GH | 2 |
| TS | skid block | 24 × 8 × 8 | 0.6 | printed | under BX | 1 |

---

## 5. Contact / gap matrix (est. mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| FT tips ↔ floor | contact (walking supports) | 0 |
| TS ↔ floor | contact (rear support) | 0 |
| BX bottom (front) ↔ floor | clearance | 4 |
| BL lowest swept point (r 42 about z 40) ↔ floor | clearance | −2 → see §13 |
| BL ↔ FT | clearance (the feet must pass behind/under the blade plane) | 8 in Y |
| BL ↔ BC | clamped | 0 |
| RT ↔ RG inner edge | clearance | 4 |
| RT ↔ SP | clearance | 1–2 (tight) |
| RG ↔ GH | screwed via tabs | 0 |
| AR tip ↔ HB/RG hub | pivot | 0.3 |
| HN ↔ RG rim | clearance (tilt limit) | 6 |
| W ↔ RG | loose | 2–10 |
| EP ↔ BX | screwed | 0 |

---

## 6. Mechanism

1. **Weapon / gyro**: the outrunner MW spins the shaft carrying RT, BC and the blade about **Y**. The rotating mass is the blade (about 22 g) plus BC and RT (about 8 g). This is the **gyroscope**, with angular momentum **L along ±Y**.
2. **Tilt (guess, medium)**: a small actuator in the box (servo or N20 gearmotor) tilts the gyro unit about the **X axis** through the arm pivots PV, giving a pitch rate ω_t. The gyroscopic reaction torque is τ = ω_t × L, which acts about **Z** (yaw). With L along Y and ω_t along X, τ lies along Z. So pitching the gyro **twists the robot about the vertical axis**.
3. **Walking**: the robot stands on three points: FT-L, FT-R and TS.
   - A yaw torque pivots it about whichever foot carries more load.
   - **Alternating** the tilt direction alternates the twist. With friction differing between the pointed feet and the skid, the robot "waddles" forward one step at a time, like a person walking a heavy wardrobe.
   - Turning on the spot is a sustained tilt in one direction.
4. **Attack**: the blade spins in a **vertical plane facing forward**, so it sweeps across the space in front of the feet. The **claw** end bites and the **fishtail** end slaps. The direction is unknown (clockwise from the front, guess).
5. **Energy**: blade m ≈ 22 g, L 84. I ≈ (1/12)·0.022·0.084² ≈ 1.3 × 10⁻⁵ kg·m², plus BC/RT at about 0.4 × 10⁻⁵, so I ≈ 1.7 × 10⁻⁵ in total. At 8000 rpm (838 rad/s): E ≈ 6 J, and the tip speed is ≈ 35 m/s. L ≈ 1.4 × 10⁻² N·m·s. At a tilt rate of 3 rad/s, τ ≈ 0.04 N·m, which is enough to pivot a 200 g robot on a foot (needs about m·g·r_friction ≈ 0.2·9.8·0.3·0.04 ≈ 0.024 N·m).

---

## 7. Assembly order (suggested rebuild)

1. Print the box with integral arms, the horns and the tail skid; fit the battery, ESC/receiver, weapon ESC and switch in their pockets.
2. Fit the tilt actuator in the box's front upper bay (guess), with its output linked to the gyro unit (a horn rod or a direct gear at the pivot).
3. Build the gyro unit: press the motor stator into the hub at the centre of the spoke cross; bolt the ring RG to the housing GH by its tabs; fit the front bearing in GH.
4. Fit RT on the bell, pass the shaft through GH, fit BC, the blade and the nose cap NC.
5. Screw the feet under GH.
6. Hang the gyro unit between the arms on the two M3 pivot screws; route the phase wires with a slack loop.
7. Screw the end plate and the skid strip to the rear.

---

## 8. Hidden / uncertain list
- The **tilt mechanism** (actuator type, position and linkage). It is not visible, and the walking mode is inferred from the name and class.
- Whether **RG** spins (as a flywheel) or is stationary. It is read as stationary because it is screwed to GH by tabs, and the spokes carry the hub.
- Whether **BC** is a gear or a toothed hub.
- The right arm and right side.
- The tail skid (spec only).
- Sizes ±15%.

---

## 9. Coordinate frame (restated)
- Origin under the pivot; +X right, +Y forward, +Z up; mm.
- Box x ±21, y [−58, −16], z [4, 42]. Pivot (±25, 0, 40). Ring at y [−2, +3], Ø 56 about (0, 0, 40). GH y [+3, +19]. BC y [+19, +28]. Blade y [+30, +33], swept r 42. NC y [+33, +43].
- Feet from (±14, +8, 14) to (±22, +44, 0). Horns at (±12, −18, 42–60).

## 10. Profiles as math

**10.1 Blade (XZ, centred on the axis A).**
- Hub: circle r 10.
- Claw arm (θ = 0, up): a straight band of half-width 7 from r 10 to r 26. Then a fan bounded by two straight lines diverging at ±25°, out to r 40, with an outer arc of r 40. A notch circle of r 9 centred at r 38 on the arm's centreline removes the middle, leaving prongs about 8 wide. The leading prong's tip curves into a hook: an arc of r 6.
- Fishtail arm (θ = 180°): half-width 5 from r 10 to r 30. Then the flanks follow x = ±(5 + 20 − √(20² − (r − 30)²)) for r ∈ [30, 44], flaring to ±13 at r 44. The end edge is straight.
- Thickness 3.

**10.2 Ring.** Annulus r ∈ [24, 28], thickness 5 in Y. Spokes: bars |u| ≤ 1.5 along the diagonals rotated 15°.

**10.3 Arm (YZ, extruded 8).**
- Upper edge: z = 34 + 0.33·(y + 30) from y −30 to −3.
- Lower edge: concave arc of r 30 centred (y −5, z −2), from (−30, 8) to (−4, 31).
- Tip: circle r 9 about (0, 40).

**10.4 Foot.** Centreline from (±14, +8, 14) to (±22, +44, 0): z = 14 − 0.39·(y − 8) (21° slope). Triangular section with base 10 at the root tapering to 0 at the tip, height 6 → 0.

**10.5 End plate outline (XZ).** A rectangle |x| ≤ 21, 4 ≤ z ≤ 42 with corner chamfers: z ≤ 42 − (|x| − 15) for |x| > 15.

**10.6 Bevel crown.** Cone face with a 45° pitch angle. Outer r 20, inner r 11; 22 teeth with tooth height 3.

## 11. Pixel-based measurements

- **76 (1748 × 1245)**: ring outer ellipse (640–1260, 230–930), so the major axis is 700 px. Pivot screw head (805–855, 615–665) is 50 px. Blade (900–1700, 50–880). Rear end plate (90–440, 650–1110). Feet (900–1490, 860–1180). Horns (550–700, 320–480).
- **74 (1412 × 1143)**: ring (495–980, 225–835), 610 px. Screw head (540–580, 525–570), 40 px. Blade (800–1370, 40–850). End plate (50–280, 450–860).
- **72 (1310 × 1182)**: ring (450–860, 290–880), 590 px. Screw head (495–530, 640–685), 40 px. Blade (1040–1270, 30–830).

## 12. Several independent estimates of key sizes

| Quantity | Method A (spec/known) | Method B (ratios) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Scale (76) | M3 SHCS head 5.5 mm | — | 50 px → 9.1 px/mm (near the pivot) | 9.1 px/mm |
| Ring Ø | 82 (spec r 41) | 1.4 H | 700 px / 9.1 ≈ 77 (near, large) / 74: 610/7.3 ≈ 84 | **conflict → §13** |
| Blade length | 124 (spec) | ≤ cube 101.6 | 76: 830 px / 9.1 ≈ 91 | **84** |
| Box height H | 44 (spec) | — | 76: 460 px / ≈ 11 px/mm (nearer) ≈ 42 | **38–42** |
| Feet length | 58 (spec) | 1.25 H | 76: 600 px / 11 ≈ 55 (foreshortened) | **50** |
| Overall length | 102 (spec, −32 to +70) | ≤ 101.6 | — | **100** |

## 13. Consistency check: conflicts and reconciliation
1. **Ring size**: the pixels give 77–84 mm against a 101.6 cube, which still fits, but then the blade (1.15–1.2 × ring) would be about 95 mm and its top at z 40 + 47 = 87. That fits the cube height, but the bottom would cut into the floor (40 − 47 = −7). Since the blade must clear the floor, **either the axis is higher, or the blade is shorter**.
   - If the ring is 77 the axis must be at ≥ 40 + clearance. The ring bottom (z 40 − 38 = 2) touches the floor, and the feet then lift it.
   - **Reconciliation**: the robot **stands on its feet with the gyro axis at z ≈ 44**. The ring is **Ø 64**, which is close to the spec ring's r 41 minus perspective inflation (the ring is nearest the camera). The blade is **84** (r 42), so its lowest point is z 2. This is the floor-skimming swept circle typical of a vertical spinner.
   - The pixel ring figure is inflated by its being closer to the camera than the screw (the screw is on the near arm, but the ring rim's near edge projects further). **Final: ring Ø 60 ± 4, axis z 42 ± 2, blade r 42.**
2. **Spec blade 124** is impossible in a 101.6 cube with a 60-wide body. It must be the bar measured diagonally including perspective. **Use 84.**
3. **Rest pose**: the feet tips at y 44 are ahead of the blade plane (y 32), so the blade sweeps between the feet: the feet are at x ±22 at the tips and the blade (half-length 42) **would hit the feet** at x 22, z < 10. So **the feet pass behind the blade plane at the blade's radius**. The feet run under the housing from y 8 and reach the blade plane (y 32) at z 14 − 0.39·24 ≈ 5 and x ≈ 20, where r = √(20² + (42 − 5)²) ≈ 42. This is right at the blade radius, so the clearance is marginal. **Reconciled: the feet splay wider (x ±26 at y 32) or the blade is r 40.** Use **r 40, blade 80**, and feet at x ±24 at the blade plane.
4. **Mass**: the walker allowance is above 150 g. §17 totals about 175 g, which is consistent with the walker bonus.

---

## 14. Why the designer did it (per part, adversarial first)

- **Gyro-walking instead of wheels**
  - Rules/strategy: walkers earn a **weight bonus**, which here goes into a heavier blade and stronger frame. With no wheels and no drive gearboxes there is nothing in the drivetrain to break: a hit that would snap a wheel hub or shear an N20 shaft finds only a pointed foot.
  - Threats: walking is slow and imprecise. A fast wedge can outmanoeuvre it, and a pusher can shove it across the arena because the pointed feet give limited grip against a determined push. The designer accepts this and relies on the blade being where the opponent has to go.
- **Blade spinning about Y, facing forward**
  - Fight: the blade's plane is perpendicular to the direction of approach. An opponent coming from the front meets the claw/fishtail swinging across its face, hitting its top edge on the down-stroke and its side on the cross-stroke.
  - The **claw** with its notch catches edges and armour lips. The **fishtail** spreads the hit over 26 mm so it does not snap.
  - Being the gyro, the blade's spin also **stabilises** the robot against being flipped about X and Z. A hit that tries to rotate the robot is resisted gyroscopically and turned into a slow precession.
- **Stationary ring frame with steel rim and spokes**
  - Fight: guards the spinning motor rotor RT from side hits, and is the stiff member between the pivots (rear) and the bearing housing (front). The **steel rim** takes impacts from horizontal spinners that reach up to 70 mm. The cross spokes keep it round. Its open centre saves weight.
  - Threats: a vertical spinner could reach into the open ring and hit RT. The black teeth on RT then act as a counter-weapon (guess).
- **Two-arm pivot with socket screws**
  - Construction: the tilt pivot carries the gyro's reaction torque. Two arms, one each side, keep the pivot axis straight; socket screws give a clean bearing surface.
  - Fight: the arms are thick at their roots and taper, so a hit on the gyro unit is passed back into the box as bending. White PETG flexes rather than snapping.
- **Pointed feet**
  - Fight: they are the **front wedge**. Two sharp spikes on the floor get under opponents that approach the blade low, so they meet the blade's down-stroke. The metal caps in 72 harden the tips. The splay gives a wide stance against side-tipping.
  - Getting under vs being got under: the points are only point contacts, so a flat wedge can slide between them. But it would then be directly under the blade's sweep, so a wedge that "wins" the getting-under contest takes a vertical hit.
- **Rear box and end plate, sacrificial skid**
  - Fight: the box holds the electronics far from the blade. The orange end plate shields the rear. The skid strip is replaceable armour, already chewed in photo 76.
  - Threats: the rear is the weak side, since the robot turns slowly. Horizontal spinners will attack the rear box.
- **Horns**
  - Fight: when inverted, the horns and the ring rim become feet, so the gyro-walk still works. They also stop the robot coming to rest on its back on the wires.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Weapon motor | 2207–2808 outrunner, stator in the ring hub | Ø 28 × 20 | (0, −2, 42) | medium |
| Weapon ESC | 20–30 A BLHeli | 25 × 13 × 5 | box top pocket (0, −36, 32) | medium |
| Tilt actuator | micro servo (9 g) or N20 gearmotor + crank | 23 × 12 × 22 | box front upper (0, −22, 28) | low |
| Tilt linkage | horn → pushrod → lever on the gyro hub | 15 rod | (+18, −10, 40) | low |
| Battery | 2S 300–450 mAh | 40 × 18 × 12 | box bottom pocket (0, −37, 10) | medium |
| Receiver / mixer | micro receiver + mixing (the walk gait needs a mixer or a microcontroller) | 20 × 12 × 5 | box (0, −37, 22) | medium |
| Switch | slide switch through the underside | 12 × 6 × 5 | (0, −49, 6) | medium (spec) |
| Front bearing | flanged 3 × 8 × 3 | Ø 8 | in GH (0, +10, 42) | medium |
| Shaft | Ø 3–4 steel | 45 long | along the axis | medium |
| Tail skid | printed block | 24 × 8 × 8 | (0, −52, 2) | medium (spec) |
| Wiring | battery → switch → ESCs; phases through a slack loop to the motor | — | — | high |

---

## 16. Variant differences between the three events

- **AWS 72**: bright orange gyro housing with crisp screw holes. **Blue painted blade with bright ground edges**, oriented fishtail-up. **Black feet with bare metal tips**. Translucent white box with a darker infill pattern, and a **black wedge strip** visible under the box's left side (72 (240–300, 470–520)), possibly an earlier skid. The ring rim is shiny bare steel.
- **AWS 74**: salmon housing and ring, **dark blue blade** (claw up), **blue feet**, pale-green nose cap visible. Box looks green-tinted (cut-out cast). Horns visible.
- **AWS 76**: same as 74 but the blade is dark grey/black, and the skid strip is **heavily torn**. The ring's orange face is worn showing the steel underneath at the edges, and the spokes are scratched. Wire loop visible.
- **Reading**: the design was stable over three events. The blade was repainted or replaced (blue to black), and the feet changed from metal-tipped to plain printed (probably because the printed points were good enough, or for weight).

## 17. Mass budget (est. g)

| Item | Mass | Basis |
|---|---|---|
| Blade (80 × 3 steel, ≈ 9 cm²) | 21 | 7.85 × 0.9 × 0.3 |
| Bevel crown + rotor disc + nose | 10 | printed |
| Weapon motor | 30 | 2808 class |
| Ring (steel rim + orange face) + spokes | 16 | steel hoop 1.5 × 5 × 176 = 10 g + 6 |
| Gyro housing + bearing + shaft | 12 | printed + 4 g steel |
| Feet × 2 | 8 | printed, metal tips +4 |
| Box + arms + horns + end plate + skid | 34 | printed |
| Tilt actuator + linkage | 12 | 9 g servo |
| Battery 2S 450 | 26 | catalogue |
| ESC + receiver + switch | 14 | catalogue |
| Wires + screws | 6 | — |
| **Total** | **≈ 189** | |

This is within a walker allowance well above 150 g. If the allowance is lower, the first saving would be a 300 mAh pack (−8 g) and a lighter motor (−8 g).

## 18. Matchups

- **Vs wedges/pushers**: the feet are the first contact. A wedge slipping between the feet goes under the blade's down-stroke. A pusher hitting the side face of the ring or box can shove GYROniNO freely, since walkers have little traction. Best defence: keep the blade facing the opponent by gyro-turning, which is fast because a sustained tilt turns it on the spot.
- **Vs horizontal spinners**: the steel ring rim and the end plate face them. The blade, held as a gyroscope, resists being spun around, which means hits transfer to the frame as shock. The arm pivot screws are the weak link.
- **Vs vertical spinners and drums**: weapon-to-weapon exchanges in roughly perpendicular planes. The opponent's vertical blade meets GYROniNO's blade broadside, which is risky for both, but GYROniNO's tall blade reaches over a low drum's top.
- **Vs flippers/lifters**: the gyro resists rotation about X and Z, so a flip turns into a slow roll. When inverted, the horns and ring take the weight and the walk continues (guess).

## 19. Wear reading
- Torn skid strip (76): attacked from behind or dragged.
- Scratched spokes and scuffed ring rim: hit by opponents' weapons.
- Repainted/replaced blade between events: the blade edges got ground or bent.
- Feet tips slightly blunted in 74 and 76.
- The arms show white stress marks (whitening) near the pivot in 76 (780–900, 650–720), which shows high loads at the tilt pivot.

## 20. Alternatives considered
- **The ring spins as a flywheel** (instead of being stationary): rejected (medium). The tabs and screws to the housing, and the steel spokes carrying the hub, indicate a fixed frame. A spinning ring would need a bearing at its rim.
- **BC is a gear meshing with a pinion from the tilt motor**: rejected (low–medium). No pinion is visible, and the gear sits on the weapon axis, which spins at thousands of rpm.
- **The arms are rigid (no tilt), with walking by unbalanced vibration (like rbmk)**: possible (low). The socket screw at each arm tip could be a fixed joint, and the walk could come from changing spin speed (reaction torque about Y rolls the robot from foot to foot). A **reaction-torque walker** is a valid alternative: spinning up rolls the robot one way onto one foot, braking rolls it the other way. Both models give foot-to-foot rocking. The tilt-pivot reading is preferred because the arms end in a clean single-screw joint.
