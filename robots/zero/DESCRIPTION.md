# Zero: full rebuild description from reference photos

Source photos (all cut out onto white, each with a mask; all three are almost the same view, so the rear, right side and underside are never seen):
- `robots/zero/reference/zero.aws71.webp` (1200 × 1017 px in the PNG conversion). AWS 71. Seen from the **front-left three-quarter, about 35–40° down**, the front (the **bolted aluminium plough blade**) at the **lower right**, the rear at the **upper left**. Everything reflects the green studio surroundings, so the metal looks green; the real colour is **bare / silver aluminium** (the blade) and **aluminium sheet, probably green-anodised or green-tinted, for the body shell** (see 2.1).
- `robots/zero/reference/zero.aws74.webp` (1045 × 748). AWS 74. **Same view**, slightly more from the front, a little lower; the shell is a stronger, more uniform **green**, which suggests the shell really is **green-anodised or green-painted aluminium** while the blade is bare.
- `robots/zero/reference/zero.aws76.webp` (1200 × 768). AWS 76. **Same view**, a little lower (≈ 30°) and slightly more from the left; best view of the **left wheel** (black foam tyre with faint white sidewall lettering, deep machined aluminium hub), the **blade's left end profile** and the **curled, torn top edge** of the blade.

Everything stated as fact is read from these photos. Because all three photos show the same front-left view, the rear, the right side below the top and the underside are **inferred by symmetry and by how such robots are built** and are marked **(guess)** with a confidence. The photos show little hidden detail (a closed sheet-metal box), so the inside parts are guesses. Dimensions are **estimates**. Scale anchors: (1) the **M3 button-head socket screws** (ISO 7380 head Ø 5.7 mm) on the top and the blade; (2) the **drive wheels** (foam tyres on aluminium hubs, Ø ≈ 32 mm, a common size for antweight foam wheels); (3) the AWS 101.6 mm cube (the robot is near the limit in width with the blade). Reference **W = blade width ≈ 94 mm**.

---

## 0. Coordinate system and naming

- **Origin O**: on the floor (z = 0) under the centre of the **body shell's** plan footprint (excluding the blade).
- **+X** = robot's right, **+Y** = forward (toward the blade), **+Z** = up; mm.
- Envelope: x ∈ [−48, +48], y ∈ [−42, +52], z ∈ [0, 36].

| ID | Part |
|---|---|
| SH | folded aluminium body shell (top + side walls + front face + rear) |
| TP | top plate of the shell |
| SW-L / SW-R | sloped side walls of the shell |
| RC-L / RC-R | rear corner chamfer facets |
| FF | front face of the shell (vertical, under the top's front fold) |
| WN-L / WN-R | wheel notches in the shell's front side corners |
| S-T | 3 silver M3 button screws on the top |
| BL | aluminium plough blade (BL-L lip, BL-F face, BL-U upper flange, BL-C curl) |
| S-B | 4 silver M3 button screws through the blade's flange (2 pairs) |
| WH-L / WH-R | drive wheels: black foam tyres (TY) on machined aluminium cup hubs (HB) |
| AX | wheel axle / motor shaft & bracket (silver glimpse in the right notch) |
| DM-L / DM-R | drive gearmotors (hidden) |
| MM | motor mounts / brackets (hidden) |
| BAT, ESC, RX, SW, WR | electronics (hidden) |

---

## 1. Overall description in one paragraph

Zero is a **two-wheel pushing wedge / rammer** with **no active weapon**. It is a **closed box of folded aluminium sheet** about **68 mm wide at the top, 66 mm long and 34 mm tall**, whose **side walls slope outward toward the floor** and whose **rear corners are chamfered**, giving a "doorstop / coffin" shape, with **three silver button screws** on its flat top. Two **fat foam-tyred wheels (Ø ≈ 32 mm × 14 mm)** on **deep, cup-shaped machined aluminium hubs** sit in **notches at the front corners** of the shell, just behind the front face. Bolted across the front face with **four M3 button screws** (two pairs, near each end) is a **full-width aluminium plough blade ≈ 94 mm wide**, about **1–1.5 mm thick**: from the bolted **upright flange** it bends forward and down in a **slightly concave two-facet ramp** to a **sharp lip on the floor** about 28 mm ahead of the shell, and its **upper edge** above the screws is **curled forward and torn** from battle damage. The blade is wider than the shell and covers the front of both wheels.

---

## 2. Part-by-part description

### 2.1 Body shell (SH: TP, SW, RC, FF, WN)
- **Material**: **aluminium sheet ≈ 1–1.2 mm thick**, folded at crisp radiused bends (inside radius ≈ 1.5 mm), with scratches and small dents (bright specks on the top). In AWS74 the shell is uniformly **green** (green anodising or paint) while the blade is silvery, so **the shell is green-anodised aluminium and the blade bare aluminium** **(medium)**. Small **cut/scratched spots** are bright silver.
- **Top plate TP**: flat, at **z ≈ 34**, a **hexagon in plan**: front edge straight across (x −30…+30) at **y +22** (where it folds down into the front face, a rounded edge r ≈ 2), sides straight back to y −26, then **two 45°-ish rear chamfers** to a rear edge (x −18…+18) at y −42. Size **≈ 60 mm wide × 64 mm long**. In AWS71 the top plate shows a **raised rim / bend line** along the left edge and rear-left chamfer: the top plate's edges are **bent down** into the side walls and rear chamfers (a single folded shell), not separate plates.
- **Side walls SW**: run down from the top's side edges and **flare outward** by about **15–20° from vertical**, from x ±30 at z 34 to **x ±36 at z ≈ 4** (their bottom edges). The left wall is the **large green plane at the far left** of every photo, about **64 mm long × 31 mm tall (slant)**. Its bottom edge is about **3–4 mm above the floor** (only seen in AWS76, at the lower left, a thin dark gap under it).
- **Rear chamfers RC / rear**: the rear corners are **cut off at ≈ 45°** in plan (in AWS71 the upper-left facet from the top's left edge to its rear edge), so the rear is a **three-facet (chamfer–rear–chamfer)** end. The rear face is assumed **vertical or slightly sloped** (hidden; **guess: sloped back at 15° like the sides, medium**).
- **Front face FF**: a vertical wall across the front at **y ≈ +23…+24**, from the top's front fold (z 34) down to z ≈ 6, ≈ 60 mm wide; the blade's flange is bolted to it (2.3). It is mostly hidden behind the blade.
- **Wheel notches WN**: at each **front side corner** the shell has a **rectangular cut-out ≈ 36 mm long (y −12…+24) × 10 mm deep (x from the side-wall line inward) × full height up to the top's edge**, in which the wheel sits. The top plate's front corners **overhang the wheel's inner half** (AWS71: the right wheel's top is seen under the front-right corner of the top; the top's front-right corner has a short **tab bent down** in front of the wheel at (x +28, y +22)). In the right notch a **silver bracket / axle** shows inside the wheel (AX, at ≈ (+32, +6, 16)).
- **Fasteners**: three **S-T** screws on the top (2.5) hold the top/shell to internal brackets or standoffs.

### 2.2 Wheels (WH-L, WH-R: tyre TY, hub HB)
- **Tyre TY**: **black foam (sponge rubber)** with a fine porous texture, **Ø ≈ 32 mm outside, Ø ≈ 20 mm inside, ≈ 14 mm wide**, with **rounded shoulders** (r ≈ 3) and a **slight central crease / mould line** around the tread (AWS71 shows a faint circumferential line on the left tyre). AWS76 shows **faint white lettering** on the left tyre's sidewall (two or three characters, perhaps the brand/size).
- **Hub HB**: **machined aluminium**, bright, a **cup** whose **outer face is open**: an outer rim Ø ≈ 20 (holding the foam), a **deep bore ≈ Ø 15, ≈ 10 mm deep** (the hollow is clearly visible with reflections), and a floor at the inner end with the shaft/screw in its centre (not visible). The cup is the classic **"lightweight aluminium hub"** that slides onto a 3 mm or 4 mm motor shaft with a grub screw **(guess)**.
- **Position**: centres at **(x ±41, y +6, z 16)**: inner faces at x ±34, outer faces at **x ±48**. They sit in the front-corner notches, **about 18 mm behind the front face** (the tyre's front at y +22, just behind FF/the blade flange).
- **Height**: tyre tops at z 32, **2 mm below the top plate** (z 34). Upside down the robot would rest on the top plate and the wheels would just **not** touch: **guess (medium)**: the foam tyres are compressible and the shell top is 2 mm higher, so it is **not invertible** (or barely: the foam might reach when it rocks) — but see §13.4, the tyres may be slightly larger.
- **Guards**: the notch's back and inner side, the **top's overhang** above the inner half and the **blade** in front (the blade is wider than the shell and its ends reach the wheels' outer line) protect the wheels; their outer faces and rears are exposed.

### 2.3 Plough blade (BL: lip BL-L, face BL-F, upper flange BL-U, curl BL-C) and screws (S-B)
- **Material**: **bare aluminium sheet ≈ 1.2–1.5 mm thick** (edge thickness seen at the blade's left end in AWS76 ≈ 1.5 mm), heavily scratched, with **gouges and a torn upper edge**. **(guess: 5052/6061 aluminium; could be titanium (darker grey) — low)**.
- **Width**: **≈ 94 mm** (x −47…+47), i.e. wider than the shell (±30…±36) and spanning **the full width including the wheels' fronts** (its ends are at the wheels' outer line).
- **Profile (YZ, uniform along X)**: from the floor up:
  - **Lip BL-L**: the front edge on the floor at **y ≈ +52, z ≈ 0.5**, sharp (sheet edge), slightly wavy along its length from use.
  - **Lower facet**: rises back at **≈ 22°** for ≈ 15 mm (y +52 → +38, z 0.5 → 6).
  - **Crease**: a **longitudinal bend line** across the full width at about (y +38, z 6) (visible in all three photos as a straight line along the blade at ≈ 40 % of its visible height).
  - **Upper facet BL-F**: rises more steeply at **≈ 40°** for ≈ 16 mm to (y +26, z 16), with a **slight concave curvature** (the blade is curved, not perfectly flat; its shading grades from bright at the lip to darker at the top).
  - **Upper flange BL-U**: bends up to **vertical** at (y +25, z 16) and runs up **flat against the shell's front face** to about **z 30**, where the **4 screws** pass through it at **z ≈ 22–25**.
  - **Curl BL-C**: above the screws, the flange's top edge **bends forward** ≈ 20–30° and at the **right end** rises to a **pointed wing** reaching about **z 36** (AWS71/74/76: the right end of the top edge sticks up and forward above the shell's top line like a curled tip). The middle of the top edge is **jagged and torn** (bitten by opponents' weapons) and **bent forward** in places.
- **Ends**: the blade's left end (AWS76) shows the full profile as a **J-like curve**: from the curled top down the flange, bending forward into the ramp, to the floor lip. The ends are straight cut, no side cheeks.
- **S-B**: **4 silver M3 button-head hex-socket screws** (head Ø 5.7) through the flange into the shell's front face (nuts or rivnuts inside **(guess)**): **left pair** at x ≈ −26 and −16, **right pair** at x ≈ +16 and +26 (in the photos the pairs are ≈ 10–12 mm apart, the left pair slightly staggered in height: the outer screw ≈ 3 mm lower than the inner, i.e. the flange or the photo is slightly tilted). Both pairs at z ≈ 22–25.

### 2.4 Screws on the top (S-T)
- **3 silver M3 button-head hex-socket screws** (Ø 5.7, 1.6 tall): **rear-centre** at (x 0, y −36), **left** at (x −24, y −10), **front-centre-right** at (x +6, y +10). An asymmetric triangle; the hidden right side probably has a mirror of the left one at (x +24, y −10) **(guess, medium)** — the right side of the top is visible in AWS71/74 and shows **no** screw there, so the third point is the front-centre one: **3 screws total (high)**. They go into internal standoffs / brackets that tie the top to the motor mounts and floor.

### 2.5 Drive motors (DM) and mounts (MM), hidden
- **Guess (medium-high)**: **2 × micro metal gearmotors** (Pololu micro / N20 class 12 × 10 × 26, or a larger 2 × 25 mm "Pololu 25D" is too big) along X at the wheel axis (y +6, z 16), shafts outward into the aluminium hubs, motors inward, held in **folded aluminium brackets** (the silver bracket seen in the right notch) bolted to the shell floor. Because the foam wheels are large (32) and the robot is a pusher, a **high-torque ratio (100:1–150:1)** is likely.

### 2.6 Electronics, switch, wires (hidden)
- Nothing visible; no switch or LED on the visible faces. **Guess**: switch and link on the rear or right side (unseen).

---

## 3. Per-view descriptions

### 3.1 Front-left view (AWS71 / AWS74 / AWS76, all similar)
- Upper left: the shell's big sloped left wall and the rear-left chamfer, green; the flat top with three screws. Right: the right wheel's foam tyre in the right notch, under the top's front-right corner. Lower left: the left wheel, large and close, its open aluminium cup hub facing the camera. Lower right: the full-width aluminium blade, its upright flange with two pairs of screws, its torn and curled top edge rising into a wing at the right end, its two-facet ramp with the crease, and its sharp lip on the floor.

### 3.2 Top view (inferred)
- A hexagonal top (60 × 64) with three screws, the sloped side walls visible as 6 mm wide strips either side, wheels in the front-corner notches (x ±34…±48, y −10…+22), the blade across the whole front (94 wide) from y +24 to +52, its curled top edge along y +24…+28.

### 3.3 Front view (inferred)
- The blade fills the lower front: a 94 mm wide ramp from the floor to z 16 then the vertical flange to z 30 with four screw heads and a ragged top edge, its right end rising to a point at z 36. Behind, the top of the shell at z 34 and, at the sides, the tops of the foam tyres (z 32) just behind the blade's ends.

### 3.4 Left side view (inferred from AWS76)
- The shell's slanted side wall (64 long) with the wheel at its front end (centre y +6), the blade's J-profile in front: floor lip at y +52, crease at y +38, flange at y +25 up to z 30, curl forward at the top.

### 3.5 Rear view (not photographed; inferred)
- A trapezoidal end: the rear facet (36 wide) with two 45° chamfers, flaring out toward the floor, 30 mm tall; the wheels not visible behind (they are at the front), the blade's tips just visible at the sides.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W = 94 | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| SH | folded box, hexagonal top, flared sides | 60–72 × 66 × 34 | 0.7 × 0.7 × 0.36 | green-anodised aluminium 1.1 | 3 top screws + internal brackets | 1 |
| WN | wheel notch | 36 × 10 × 30 | — | — | cut-out | 2 |
| BL | J-profile plough blade | 94 wide, 30 deep, 36 tall at the wing | 1.0 | bare aluminium 1.5 | 4 × M3 button | 1 |
| S-B | button screw | M3, Ø 5.7 | — | stainless | into FF (nuts) | 4 |
| S-T | button screw | M3, Ø 5.7 | — | stainless | into standoffs | 3 |
| TY | foam tyre | Ø 32 / Ø 20 × 14 | 0.34 | black foam | glued on hub | 2 |
| HB | cup hub | Ø 20 × 14, bore Ø 15 × 10 | — | aluminium | grub screw on shaft | 2 |
| DM | micro gearmotor | 12 × 10 × 26 | — | metal | aluminium bracket | 2 (guess) |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| BL lip ↔ floor | contact (sliding) | 0 |
| TY bottoms ↔ floor | contact | 0 |
| SW bottom edges ↔ floor | above | 3–4 |
| Rear bottom edge ↔ floor | above (tilts down when the robot rocks back) | 3 |
| BL-U flange ↔ FF | bolted | 0 |
| BL-C curl ↔ TP front fold | curl ahead of / above the fold | 1–3 |
| BL ends ↔ TY fronts | blade in front of the tyres | 2–4 |
| TY inner face ↔ WN inner wall | running clearance | 2 |
| TY top ↔ TP overhang underside | clearance | 1–2 |
| TY front ↔ WN front (FF line / bent tab) | clearance | 2 |
| TY top ↔ TP top plane | below | −2 |
| HB ↔ motor shaft | grub screw | 0 |
| S-T ↔ TP | seated | 0 |
| S-B ↔ BL-U | seated | 0 |

---

## 6. Mechanism

1. **Pushing wedge**: there is no powered weapon. The sharp, full-width lip on the floor gets under opponents; the **two-facet ramp** (22° then 40°) lifts them as Zero drives forward; the **vertical flange and forward-curled top edge** stop them riding up over the top and hold them in front so they can be pushed into walls or pits.
2. **Drive**: 2WD, the wheels near the **front** of the body directly behind the blade: the robot's weight sits on the wheels and the blade lip, so the lip stays on the floor (good wedge contact) and traction is at the pushing point. The rear end floats about 3 mm above the floor and acts as a **tip-back stop**.
3. **Foam tyres**: high grip on the arena floor for pushing matches; light.
4. **Inverted**: probably cannot drive upside down (tyres 2 mm short of the top) **(guess, medium)**; the low, wide shape makes it hard to flip.

---

## 7. Assembly order (suggested rebuild)
1. Cut and fold the **shell** (top with chamfers and front fold, flared side walls with front-corner notches, rear facets, front face), anodise green.
2. Cut and bend the **blade**: lip, crease at 14 mm, ramp, bend up to vertical, drill 4 holes; (the curl is from battle damage, or bend the top edge forward ≈ 20°).
3. Fit the **two gearmotors** in aluminium brackets on the shell floor / a base plate at the wheel axis; fit **battery, ESC, receiver, switch**; wire.
4. Close the shell; fit the **3 top screws** into the internal standoffs.
5. Bolt the **blade** onto the front face with **4 M3 button screws** and nuts.
6. Push the **aluminium cup hubs** with **foam tyres** onto the shafts and tighten the grub screws.

---

## 8. Hidden / uncertain list
- The rear, right side and underside (never photographed).
- Motor type, bracket design, floor plate.
- Whether the shell is one folded part or top + bottom halves.
- Blade material (aluminium vs titanium), whether the curl is designed or damage.
- Electronics and switch location.
- All dims ±15 %.

## 9. Coordinate frame (restated)
Origin on the floor under the shell's plan centre; +X right; +Y forward (blade); +Z up; mm. Wheel axis: the line (y +6, z 16) along X; wheels Ø 32 × 14 at x ±34…±48. Top plate z 34, y −42…+22. Blade lip at (y +52, z 0.5), flange at y +25, screws at z 22–25.

## 10. Profiles as math

**10.1 Top plate (plan).** Polygon: (−30, 22) → (30, 22) → (30, −26) → (18, −42) → (−18, −42) → (−30, −26) → close; z = 34. Wheel-notch overhang: the parts of the polygon with |x| > 26 and y ∈ [−12, 22] are the overhang (the shell walls below are cut away there).

**10.2 Side wall.** The plane through the top's side edge (x ±30, z 34) and the bottom edge (x ±36, z 4): x = ±(30 + 0.2 (34 − z)) (slope 11° from vertical… → with the photos' flare ≈ 15–20°: x = ±(30 + 0.3 (34 − z)), bottom at ±39). **Reconciled: bottom at ±36 (flare 11°)** so that the notch depth (to x ±34 → wheel inner face) remains positive.

**10.3 Blade profile (YZ), piecewise linear with bend radii r = 2.**
P0 = (y 52, z 0.5) → P1 = (38, 6) [crease, angle 22°] → P2 = (26, 16) [angle 40°] → P3 = (25, 16) bend to vertical → P4 = (25, 30) [flange] → P5 = (27, 33) [curl forward 35°]. Right-end wing: P5' = (29, 36). Thickness 1.5 offset backward/inward. Extruded over x ∈ [−47, 47].

**10.4 Blade concavity.** Upper facet slight sag: z(s) = linear(P1→P2) − 0.8 · sin(π s), s ∈ [0, 1] along the facet.

**10.5 Wheel.** Tyre: torus-like annulus, r ∈ [10, 16], width 14, shoulder fillets r 3. Hub: cylinder r 10, width 14, with an open bore r 7.5 depth 10 from the outer face; inner floor 4 thick with Ø 3 shaft bore.

## 11. Pixel-based measurements
- **AWS71 (1200 × 1017)**: S-B screw heads ≈ 42 px (near pair) and 38 px (far pair); S-T heads ≈ 35 px. Left wheel: x 30 → 330 (tyre outer), y 270 → 620; hub opening ≈ 150 px across. Right wheel: x 690 → 930, y 60 → 260. Blade: flange line from (370, 470) to (870, 215); lip from (300, 1010) to (1110, 600); crease from (230, 720) to (1100, 400); right wing tip at (1065, 160). Top screws at (470, 68), (125, 205), (565, 282).
- **AWS74 (1045 × 748)**: left wheel 70 → 290 (220 px); blade lip (300, 650) → (965, 380); screws ≈ 32 px.
- **AWS76 (1200 × 768)**: left wheel x 145 → 410 (tyre), 275 → 545 tall (270 px); hub bore ≈ 120 px; blade left-end profile from (350, 420) top to (430, 650) bottom; lip from (430, 650) to (1085, 320); screws ≈ 30 px (near pair).

## 12. Several independent estimates

| Quantity | Method A (screw Ø 5.7) | Method B (wheel Ø 32) | Method C (cube / W 94) | Reconciled |
|---|---|---|---|---|
| px/mm at the blade flange (AWS71) | 42/5.7 = 7.4 | — | — | 7.4 |
| Blade width | flange (370 → 870 px along an oblique line, ≈ 560 px) / 7.4 / cos(≈ 35°) ≈ 92 | lip 1000 px?/ (AWS76: 270 px = 32 mm at the wheel → 8.4 px/mm) → 800/8.4 ≈ 95 | ≤ 101.6 | **94** |
| Wheel Ø | AWS71: 350 px tall / (7.4 × 1.2 nearer) ≈ 39?? | assumed 32 | — | **32–34** (§13) |
| Hub bore | AWS76: 120/8.4 ≈ 14 | — | — | **15** |
| Blade depth (flange → lip) | AWS76 profile 230 px tall at the end (z 0 → 30) → 27 mm tall | — | — | **flange top z 30, lip 27 ahead** |
| Shell top width | AWS71 front fold ≈ 560 px vs flange: the top's front edge is ≈ 0.64 of the blade → 60 | — | — | **60** |
| Shell length | AWS71: rear screw to front fold ≈ 300 px foreshortened by ≈ 0.6 → 68 | — | — | **64** (top) |
| Body height | AWS76: side wall ≈ 270 px slant at the near end ≈ wheel height → 32 + 2 | — | — | **34** |

## 13. Consistency check
1. **Wheel diameter**: method A gave ≈ 39 because the left wheel is much nearer the camera than the blade screws (perspective magnification ≈ 1.2–1.3). The wheel's top is just under the top plate (AWS76: tyre top a little below the top's edge), so **Ø ≈ 32** with the top at z 34. **Reconciled: Ø 32.**
2. **Width**: blade 94; wheels' outer faces ±48 → 96 overall. Cube 101.6. **Consistent.**
3. **Length**: rear y −42 to lip y +52 → 94 mm. **Consistent** (< 101.6).
4. **Inverted driving**: wheel top z 32 vs shell top z 34 → 2 mm short; the blade's flange/wing rises to z 36. Upside down the robot rests on the wing and the top: **not drivable inverted**. If the tyres were Ø 36 they would protrude; the photos show the tyre top below the top's edge → **not invertible (medium)**.
5. **Balance**: wheels at y +6, blade lip at y +52, rear at y −42. If the CG is at y ≈ −5 (battery at the rear), the robot would rest on the wheels and the rear edge, lifting the lip **off** the floor — bad for a wedge. So the CG must be **ahead of the axle** (y ≈ +8…+12: the motors, the blade (≈ 15 g) and the electronics forward) so that the lip carries a few grams. Then the rear floats. **Reconciled: CG at y ≈ +10, rear 3 mm above the floor, lip on the floor.**
6. **Mass**: shell 1.1 mm aluminium ≈ 2.7 g/cm³ × (area ≈ 60 × 64 + 2 × 64 × 32 + 60 × 30 + rear 40 × 30 ≈ 11 000 mm² → 12 cm³) ≈ 33 g; blade 94 × 52 × 1.5 → 7.3 cm³ ≈ 20 g; 2 gearmotors 20 g; 2 wheels (aluminium hubs + foam) 2 × 7 = 14 g; battery 2S 300 mAh 18 g; ESC 5 g; RX 3 g; brackets/screws 10 g; wires 4 g → **≈ 127 g**: under 150 g, room for a heavier battery or thicker blade. **Consistent.**

---

## 14. Why the designer did it (per part; adversarial lens first)

- **Full-width bolted aluminium blade**
  - Getting under: a **thin sheet lip** (1.5 mm) on the floor beats thick printed wedge edges in the "who gets under whom" contest; the **two-facet ramp** starts shallow (22°) to slip under, then steepens (40°) to lift; full width means nothing can come at the front without meeting the lip, and it covers the **wheels' fronts**.
  - Adversarial: aluminium **bends instead of shattering**: the torn, curled top edge shows it took spinner hits and stayed on. **Bolted** with 4 screws so it can be swapped or straightened between fights. The upright flange with a forward curl stops opponents riding over onto the shell and keeps them in front for pushing.
- **Folded aluminium box shell (green-anodised)**: very strong for its mass, no printed parts to crack; the **flared side walls** and **chamfered rear corners** deflect horizontal spinners' hits upward/away rather than taking them square. Anodising protects and identifies.
- **Wheels at the front corners in notches**: the weight sits on the wheels right behind the blade, which keeps the lip pressed down and gives maximum traction at the pushing point. The notches and the top's overhang shield the wheels from above and the inside, and the blade shields them from the front.
- **Foam tyres on aluminium cup hubs**: foam gives very high grip on the typical arena floor for pushing, is light and absorbs shocks; the open cup hub is light and lets the grub screw be reached.
- **Only 3 top screws**: minimal fasteners for quick access; the triangle pattern is enough to hold a stiff folded lid.
- **No active weapon**: the whole 150 g budget goes into armour, traction and a robust wedge; a rammer like Zero wins by control and pushing out / into hazards.

---

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Drive motors | 2 × micro metal gearmotor (Pololu micro HP 100:1 / N20) along X | 12 × 10 × 26 + shaft 10 | (±20, +6, 16) | medium |
| Motor brackets | folded aluminium L-brackets on the floor | 14 × 12 × 2 | (±28, +6, 10) | medium |
| Floor / base | separate aluminium or carbon base plate, or folded shell bottom | 70 × 64 × 1 | z 3–4 | medium |
| Standoffs | 3 × M3 standoffs under the top screws | Ø 5 × 28 | under S-T | medium |
| Battery | 2S LiPo 300–450 mAh | 50 × 20 × 12 | (0, −20, 12) | medium |
| Drive ESC | dual brushed ESC | 20 × 15 × 5 | (0, +14, 22) | medium |
| Receiver | micro rx | 15 × 11 × 4 | (−12, −30, 24) | low |
| Switch / link | in the rear face or right side (unseen) | 12 × 4 × 6 | (+10, −40, 14) | low |
| Blade nuts | 4 × M3 nyloc nuts behind the front face (or rivnuts) | M3 | behind S-B | medium |
| Wiring | battery → switch → ESC → motors | — | inside | high |
