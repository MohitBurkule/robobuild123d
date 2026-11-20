# My First Bot: full rebuild description from reference photos

Source photos (AWS wiki, cut out onto white except aws66):
- `robots/my_first_bot/reference/my_first_bot.aws66.webp` (AWS 66, 539 × 568 px, small, not cut out). An **early version** with a **wood-grain yellow shell**, seen from almost straight **above** (camera about 60–70° above the floor), the robot rotated so its sloped end faces the upper-left. It sits on a yellow/orange table next to other robots (a dark box at the top, a clear polycarbonate robot with a black wheel at the bottom-left, which is **not** part of this robot).
- `robots/my_first_bot/reference/my_first_bot.aws67.webp` (AWS 67, 2016 × 1836 px). The **same early yellow shell, battered**, now with a **clear plastic + steel blade front wedge** and a **black printed arm**. Camera is **front-left, high** (about 35–40° above the floor, about 45° round from the front toward the robot's left side). Front points to the lower-right of the image.
- `robots/my_first_bot/reference/my_first_bot.aws71.webp` (AWS 71, 2055 × 1855 px). A **rebuilt, all-white 3D-printed** version with the same layout (two hemispherical eyes, one tall arm with a T top, a sloped front wedge). Camera is **front-right, high** (about 35° above the floor, about 45° round from the front toward the robot's right side). Front points to the lower-left of the image, the right side faces the lower-right.

This document describes **the latest (AWS 71, white printed) version as the main build target**, and records the earlier versions (V1 wood-grain aws66, V2 yellow battered aws67) where they differ, because they show the same layout from other directions and help fix positions. The robot is a **simple wedge/pusher with a cosmetic face**: two big googly-style eyes on the lid, a slotted "mouth" on the wedge, and a tall thin servo-driven (guess) arm topped by a little **two-blade propeller** (very likely a "propeller beanie" joke fitting the beginner's name "My First Bot"; guess, medium). No wheels are visible in any photo: the **wheels are inside the body** (kit draft `outside: false`).

Everything stated as fact is read from the photos. Anything inferred is marked **(guess)**. Dimensions in mm are **estimates**. Absolute scale comes from: the AWS 150 g / 101.6 mm cube rule, the black lid screws (button/pan heads read as M3, head Ø ≈ 5.5–6 mm), and the kit draft (`kit.json`: wedge body 105 × 100 × 36, ramp 95, two wheels r 10 × 8 at y −35 inside the body, eye spheres r 11). Ratios are given against **W = body width at the floor ≈ 96 mm**.

---

## 0. Coordinate system and naming

- **+X** = robot's right, **+Y** = forward (toward the wedge tip), **+Z** = up. Units mm.
- **Origin O** = the point on the floor (z = 0) under the centre of the body's footprint (mid-width, mid-length, measured from the wedge tip to the rear wall).
- **Front** = the end with the long sloped wedge panel (in aws71 the panel with the five lens-shaped slots; in aws67 the panel covered with clear plastic and a steel blade).
- In aws71: +Y points to the lower-left of the image (about 30° below horizontal), +X to the lower-right (about 30° below horizontal), +Z up.
- In aws67: +Y points to the lower-right of the image, +X to the upper-right (away from camera), +Z up.

| ID | Part |
|---|---|
| SH | body shell (printed tub in V3; wood-grain/card shell in V1/V2) |
| LID | top lid plate (inset panel with a perimeter rim) |
| RIM | raised perimeter frame/rim around the lid |
| WP | front wedge panel (sloped) |
| MS | five lens-shaped "mouth"/vent slots in WP (V3) |
| SS-L, SS-R | sloped side walls |
| RW | rear wall (not photographed) |
| EY-L, EY-R | two hemispherical eye domes |
| PU-L, PU-R | dark pupils on the eyes (printed insert, marker dot or screw head) |
| SLT | arm slot through the lid |
| ARM | thin vertical arm (mast) with a crank at its root |
| PROP | two-blade propeller / T-bar on top of the arm, with a hub |
| SRV | servo that drives the arm (hidden, guess) |
| S-LID | black lid screws |
| PH | two small pin holes in the lid near the left eye (V3) |
| CP | clear plastic (polycarbonate) wedge cover plate (V2 only) |
| SB | steel blade strip under CP at the wedge tip (V2 only) |
| S-WP | screws holding CP/SB (V2) |
| TP-G, TP-S | green side tape, silver duct tape edging (V2) |
| WH-L, WH-R | drive wheels (inside the body, hidden) |
| M-L, M-R | drive gearmotors (hidden) |
| BAT, ESC, RX, SW | battery, drive ESC, receiver, power switch/link (hidden) |

---

## 1. Overall description in one paragraph

My First Bot is a **two-wheel wedge with internal wheels** and a cartoon face. The body is a low, almost square block about **96 mm wide × 98 mm long × 32 mm tall**. The front third is a **long flat wedge** that slopes from the lid down to a sharp edge on the floor at about **35°**; the left and right sides are also **inclined** (steep, about 60–70° from the floor) with a **rounded top edge**; the top is a **flat inset lid** framed by a thin rim and held by **four black screws**. On the lid sit **two white hemispherical eyes** about **24 mm across and 11 mm tall**, each with a **dark round pupil**, placed **staggered**: the left one toward the rear-left, the right one more toward the front-right (a cross-eyed look). Between them, right at the front edge of the lid, is a **rectangular slot** from which a **thin square-section arm about 4 mm thick** rises about **60 mm**, leaning forward and slightly right, with a **crank (dog-leg) at its root** inside the slot. On top of the arm is a **flat two-blade "propeller" about 30 mm across with a small square hub**. The front wedge panel carries **five lens-shaped slots** in a straight row like a mouth or vents. In V2 the wedge was covered with **clear plastic over a steel scraper blade** whose bare edge forms the tip. The wheels, motors and electronics are all hidden inside.

---

## 2. Part-by-part description (V3, AWS 71, unless stated)

### 2.1 Body shell (SH)
- **Shape**: a **trapezoidal-section tub**. Footprint about **96 (X) × 98 (Y) mm** on the floor. The lid top is at **z ≈ 32**. The top face (lid + rim) is narrower than the footprint because the sides slope in and the front slopes back.
- **Material/colour (V3)**: **off-white/ivory FDM print** (PLA or PETG), smooth, with fine layer lines visible on the eye domes and faint seams where separately printed panels join. The photo has a strong green/cyan colour cast at the right (lighting/cut-out artefact), but the true colour is plain white.
- **Wall thickness (guess)**: 2–2.5 mm. Panels meet at square seams; a visible **vertical seam** runs up the front-right corner where WP meets SS-R (aws71 at about px (1250, 1240)–(1250, 1530)), and a **horizontal seam** along the bottom of SS-R, suggesting the wedge panel, sides and tub are **separate prints glued/screwed together**, or one print with a visible seam line (guess, medium).
- **V1 (aws66)**: the shell is faced with a **yellow wood-grain surface** (visible grain streaks, darker knots) that is **chipped in many places to a white core** (white patches with ragged edges at the right edge and bottom edge). Most likely **thin wood veneer / wood-effect laminate over foam board or a light wood block** (guess). The end face at the upper-left shows **end grain**, so at least that panel is real wood (guess, medium).
- **V2 (aws67)**: the same shell, now **painted yellow** (or with yellow card) showing **regular parallel stripes about 3 mm apart** across the lid (paint over wood grain, or the flutes of corrugated board, guess), badly chipped, exposing a **grey/silver layer** (duct tape or aluminium) and **white fibrous bits** (paper/foam). The left side face is wrapped in **green tape** (TP-G); the lid edge along the left side has strips of **silver duct tape** (TP-S).

### 2.2 Lid (LID) and rim (RIM)
- **Shape**: a **flat plate about 1.5–2 mm thick**, sitting in a pocket inside a **raised rim** about **3 mm wide and 1–1.5 mm proud** of the lid. The rim runs along the rear edge and both side edges (clearly seen as a step line along the right edge in the aws71 crop and along the rear edge at the top of the image). Along the front edge the lid meets the fold to WP directly.
- **Extent (top view)**: rim outer edges at about x −38 to +38 and y −49 to +10; the lid pocket about **70 × 55 mm** (x −35 to +35, y −46 to +9).
- **Split lid (V3)**: the top shows a faint dividing line running front-to-back from the slot, i.e. the lid may be **two plates**, a left plate (around EY-L) and a right plate (around EY-R), meeting at the slot (guess, medium). Each plate has two screws along its outer side edge.
- **Surface**: plain flat white. Two **tiny pin holes** PH (Ø ≈ 1.5 mm) sit in front of and to the right of EY-L, at about (−14, −6) and (−4, −2): likely **wire holes for an LED**, or holes for the eye's locating pins (guess, low).

### 2.3 Lid screws (S-LID)
- **Black button/pan head screws**, head **Ø ≈ 5.5–6 mm**, about 1.5 mm proud, with a **Torx/hexalobular or Phillips** recess (the aws71 crop shows a six-lobed/cross recess). Read as **M3** (guess).
- Positions in aws71 (native px → est. mm):
  - (680, 520) → rear-left area, just left of EY-L, about (−34, −30).
  - (510, 665) → left edge near the front of EY-L, about (−34, −10)... (both left screws sit along the lid's left edge, about 20 mm apart).
  - (1475, 1065) → right edge just behind EY-R's front, about (+34, −14).
  - (1275, 1245) → front-right corner of the lid, about (+34, +6).
- So: **two screws along each side edge of the lid**, at about y −30/−10 on the left and y −14/+6 on the right (the lid pattern is not mirror-symmetric, guess: the visible spacing is about 20 mm on each side; build as 4 screws at (±34, −28) and (±34, +4) if symmetry is preferred).
- **V2 (aws67)**: 2 screws along the left edge near EY-L, 1 screw right of EY-R, 1 screw near the lid's front-left centre at about (−14, +2), plus 3 screws through the clear wedge plate (2.11).
- **V1 (aws66)**: 4–5 black screws on the top (at native px (348, 117), (190, 186), (175, 388), (302, 365)) plus a tiny screw through the centre of each eye as the pupil.

### 2.4 Front wedge panel (WP)
- **Shape**: a **flat inclined plate** spanning the whole front, from the lid's front edge (fold line at about y +10, z 32) down to a **straight leading edge on the floor** at about **y +49, z 0**. Horizontal run about **39 mm**, rise **32 mm**: slope **about 39°** from the floor (35–42° range). Length along the slope about **50 mm**. Width about **96 mm** at the bottom, about **80 mm** at the top fold (the side slopes trim its ends; the panel is a **trapezoid** in its own plane).
- **Thickness**: about **2.5–3 mm**; the leading edge is a blunt printed edge (about 1 mm flat on the floor; V3 has no metal edge).
- **Slots (MS)**: **five lens-shaped (vesica / almond) slots**, each about **12–14 mm long × 3.5–4 mm wide**, long axis roughly along X (slightly skewed), evenly spaced about **14–16 mm** apart in a **straight row across the panel** at about mid-slope (z ≈ 14–18). The slot row runs from about x −34 to +30. The slots are cut straight through (the dark/white interior shows a thin wall). Function: **vents / lightening, or a stylised mouth/teeth** for the face (guess). They read like a row of **cable-tie slots or leaf vents**.
- In aws71 the slots are at native px about (415, 530), (555, 610), (665, 720), (800, 840), (915, 1220): the last is near the front-right corner.

### 2.5 Sloped side walls (SS-L, SS-R)
- **Shape**: **inclined flat walls** from the lid rim (x ±38, z 32) down to the floor edge (x ±48, z 0): run 10 mm over 32 mm rise, about **72° from the floor** (60–75°). The **top edge** where SS meets RIM is **rounded** (radius about 3–4 mm), clearly seen in the aws71 crop as a cylindrical bead along the right side, ending at the rear in a round **end cap**.
- **Side profile (seen from the side)**: rear vertical (guess) at y −49, full height 32 back to y ≈ +10, then following the wedge slope down to y +49. So each side wall is a **trapezoid** 98 long at the floor, 59 long at the top.
- **V2**: the left side wall is covered in **green tape** with ragged edges, its bottom edge chipped; under the front-left corner a **dark gap** (aws67 px (470–520, 1270–1450)) shows the hollow underside/interior, possibly the left wheel's opening (guess, low).

### 2.6 Rear wall (RW)
- Not photographed. Assumed **vertical, flat**, 76–96 mm wide × 32 tall, possibly with the **power switch/link hole** (guess, medium).

### 2.7 Eyes (EY-L, EY-R) and pupils (PU)
- **Shape**: **hemispheres (slightly elongated domes)**, base **Ø ≈ 24 mm**, height **≈ 11–12 mm** (a little less than a full half sphere: a spherical cap of sphere radius ≈ 12.5, cut at 0.5 mm below the equator; guess). Clear concentric **layer rings** from FDM printing (printed dome-up).
- **Colour**: **pure white**, slightly whiter than the body.
- **Pupils (V3)**: a **dark grey circular disc** about **Ø 8–9 mm** inset at the top, with concentric rings (a **separate dark grey print or a dark filament change**), flush or slightly recessed, placed **off-centre toward the front** of each dome (pupils "looking" forward/up-left). EY-R's pupil is near the top-front; EY-L's pupil faces the camera.
- **V2**: pupils are **small dark marker dots** (Ø ≈ 5 mm). **V1**: pupils are **tiny screw heads** (Ø ≈ 2.5 mm) that also **fasten the eyes** to the lid.
- **Positions (V3)**: EY-L centre at about **(−20, −28, 32)**, EY-R centre at about **(+22, −8, 32)**: staggered by about 20 mm in Y, giving a goofy cross-eyed face (the kit draft had eye_l at (−22, −10), eye_r at (24, −22): the stagger is real, but its sign differs between versions/views; see section 12).
- **Fastening**: glued or screwed from below (V1 shows a screw through each pupil). Small burr/tab on the base of EY-L (aws67) shows a glue seam.

### 2.8 Arm slot (SLT)
- **V3**: a **rectangular hole** in the lid at its front edge, about **12 mm (X) × 20 mm (Y)**, centre about **(+0, +2)**, its front end reaching the lid/wedge fold. Through it the arm's root crank and a glimpse of a **dark part below (servo horn/screw, aws71 px (1080, 770))** are visible.
- **V2**: a ragged **round/oval hole about 16 × 22 mm**, torn out of the yellow shell around the arm root.
- **V1**: a square hole about **10 × 10 mm** showing a white servo horn and a red part (servo case or wire) beneath.

### 2.9 Arm (ARM)
- **Shape**: a **thin straight square/rectangular rod**, about **4 mm × 4 mm** in section (V2 shows a flat strip about 6 mm wide × 2.5 mm thick, printed lying flat with fine lengthwise layer lines), **about 60–65 mm long** above the lid.
- **Root crank**: at the bottom, inside the slot, the rod bends through a **rounded elbow** into a **short horizontal foot** about **10–12 mm long** that runs **rearward/down** into the body (seen clearly in aws67 as an L at the slot, and in aws71 as the curved base). This foot is the **lever that attaches to the servo horn** (guess, high).
- **Pose**: V3 (aws71): leans **forward and to the right**, about **20° from vertical** in the YZ plane and 10° in XZ. V2: almost **vertical**, leaning slightly back. V1: leaning far over, almost **lying across the lid** toward EY-R. The varying pose over three photos supports a **moving (servo-driven) arm** (guess, medium-high).
- **Top**: at z ≈ 90 (V3) the rod ends in the propeller hub.
- **Colour**: V3 white, V2 **black** (dark green-black PLA), V1 white.

### 2.10 Propeller / T-bar (PROP)
- **Shape**: a **flat, thin, two-blade bar** about **30 mm long × 5 mm wide at the centre × 1–1.5 mm thick**, the blades **tapering to points**, with a **raised square hub** about **6 × 6 × 4 mm** where it joins the arm. The blades are slightly **twisted / offset** (one blade tilted down, the other up, in aws71 and aws67), like a real propeller or a "propeller beanie" spinner. V2's bar has **wavy/serrated ends**; V1's bar is a plain T, wider (about 6 mm).
- **Orientation**: blades roughly horizontal, along X (V3: along a line rotated about 20° from X).
- **Spinning?**: almost certainly **fixed** (no bearing seen; printed as one with or glued to the arm), decorative (guess, medium).

### 2.11 V2 only: clear wedge cover (CP), steel blade (SB) and their screws (S-WP)
- **CP**: a **clear polycarbonate (or PET) sheet about 1–1.5 mm thick**, covering the whole front slope from just in front of the slot to the tip: about **90 × 45 mm**, its rear edge cut raggedly with a **notch** (step) at the front-left. Scuffed white and fogged by hits.
- **SB**: under CP, at the tip, a **steel strip** about **95 mm wide × 10–15 mm visible × 0.5 mm thick** whose bare **front edge** protrudes about **5–8 mm beyond** the plastic, showing a straight sharpened edge: a **scraper / wallpaper-scraper blade** (guess, high).
- **S-WP**: **three black pan screws** (Ø ≈ 5 mm) through CP: at about (−30, +20), (+5, +38) and (+30, +18) in body mm (aws67 px (745, 1225), (1325, 1275), (1460, 880)), the middle one with a **washer**.

### 2.12 Wheels, motors, electronics (all hidden)
- **Wheels (WH)**: inside the body, near the rear: **Ø ≈ 20–24 mm × 8 mm**, centres about **(±36, −25, 11)**, poking about **1–2 mm** below the floor plate through wheel slots (guess, medium). They cannot be seen in any photo; the side walls reach the floor.
- **Motors**: two **N20 micro gearmotors** lying along X at the rear (guess, medium).
- **Electronics**: a **1S/2S LiPo**, **receiver with integrated dual ESC** (e.g. a beginner "all-in-one" ant board), the **arm servo** (micro 9 g / 3.7 g class) under the slot, and a **switch or removable link** at the rear (guess).

---

## 3. Per-view sections

### 3.1 aws71 (V3, front-right high)
- Left half: the **long sloped front wedge** with its **five almond slots** in a diagonal row from upper-left to lower-right; the wedge's straight bottom edge runs from about px (80, 940) to (1240, 1530).
- Centre: the **lid** with **EY-L** at the rear-left (px ≈ 790, 580; dome Ø ≈ 300 px), the **slot** at the front edge of the lid (px 870–1000, 770–930), the **arm** rising from it to the **propeller** at the top (px 1125–1465, 75–190).
- Right: **EY-R** (px 1290, 960; dome Ø ≈ 380 px, nearer the camera), two black screws below/right of it, the **rounded rim bead** along the right edge, and the **sloped right side wall** in a green-tinted shade going down to the lower-right corner.
- Not visible: rear wall, left side wall, underside.

### 3.2 aws67 (V2, front-left high)
- Front wedge at the lower-right covered with **clear plastic** and the **steel blade** at the very bottom-right edge.
- Left side (green tape) at the far left, inclined.
- Lid: EY-L at px (550, 800), EY-R at px (1100, 700), the **black arm** rising vertically from a torn hole at px (1000, 860–1000) to the T-bar at px (735–945, 45–130).
- Chipped yellow surface with silver/grey showing.

### 3.3 aws66 (V1, near top-down)
- A yellow **wood-grain rectangle** rotated about 45°, the sloped end band at the upper-left, two white domes with screw pupils, a square hole with a white servo horn and red under it, the white arm lying toward the upper-right over EY-R with its **T** at px (330–430, 165–245).

### 3.4 Top view (synthesised)
- An outer rectangle **96 × 98**; inside it, the **lid rectangle 76 × 59** (y −49 to +10) with the rim; the **wedge band** 39 mm deep across the front; the **side bevels** 10 mm wide along each side. EY-L at (−20, −28), EY-R at (+22, −8), the slot at (0, +2), 4 screws along the side edges, 5 almond slots in a row across the wedge at y ≈ +27.

### 3.5 Right side view
- A trapezoid: **32 tall** at the rear, flat top to y +10, slope down to the tip at y +49; the side wall seen inclined (appears as a band). The eye domes stick up 11–12 mm; the arm rises to **z ≈ 90–94** with the propeller as a short horizontal bar at the top.

### 3.6 Front view
- The wide **wedge face** (96 wide at the bottom, 80 at the top fold), the 5 slots in a row; above, the two domes (left one farther back), the arm and propeller in the middle. The **side bevels** give the silhouette a **trapezoid** (96 wide at the floor, 76 at the top).

### 3.7 Rear view (not photographed)
- Flat rear wall 32 tall, the domes and arm above. Probably a switch/link hole (guess).

### 3.8 Underside (not photographed)
- Flat floor plate, two wheel slots near the rear, the wedge edge at the front as the third contact (guess).

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| SH | trapezoid-section tub | 96 × 98 × 32 | 1 × 1.02 × 0.33 | white FDM (V3) | — | 1 |
| LID | inset plate | 70 × 55 × 1.5 | 0.73 × 0.57 | white | 4 × M3 | 1 (or 2) |
| RIM | raised frame + round bead | 3 wide × 1.5 proud, bead r 3.5 | — | white | integral | 1 |
| WP | inclined trapezoid plate | 96/80 × 50 (along slope) × 2.5, 39° | 1 × 0.52 | white | integral/glued | 1 |
| MS | almond slots | 13 × 4, pitch 15 | 0.14 | — | — | 5 |
| SS-L/R | inclined wall, 72° | 98/59 × 33 (slant) × 2.5 | — | white | integral | 2 |
| EY-L/R | hemisphere cap | Ø 24 × 11.5 | 0.25 | white | glue/screw | 2 |
| PU | disc | Ø 8.5 × 1 | 0.09 | dark grey | inset | 2 |
| SLT | rect. hole | 12 × 20 | 0.13 × 0.21 | — | — | 1 |
| ARM | square rod + crank | 4 × 4 × 62, foot 11 | 0.65 | white (V3) / black (V2) | servo horn | 1 |
| PROP | 2-blade flat bar + hub | 30 × 5 × 1.2, hub 6 × 6 × 4 | 0.31 | white | integral | 1 |
| S-LID | button/pan head | Ø 5.7 head, M3 | 0.06 | black | into SH | 4 |
| CP (V2) | clear sheet | 90 × 45 × 1.2 | — | polycarbonate | 3 screws | 1 |
| SB (V2) | steel strip | 95 × 15 × 0.5 | — | steel | under CP | 1 |
| WH | wheels (hidden) | Ø 22 × 8 | 0.23 | black rubber (guess) | motor shaft | 2 |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| LID ↔ RIM inner edge | sits in pocket | 0–0.3 |
| LID top ↔ RIM top | lid below rim | −1.5 |
| EY ↔ LID | glued/screwed on | 0 |
| EY-L edge ↔ nearest S-LID | beside | 3–4 |
| EY-R edge ↔ nearest S-LID | beside | 2–3 |
| EY-R edge ↔ RIM (right) | beside | 4 |
| EY-L edge ↔ ARM (V3) | clear | ≈ 15 |
| ARM ↔ SLT sides | clearance (moving) | 3–4 each side in X |
| ARM foot ↔ servo horn | fixed (screw/press) | 0 (guess) |
| PROP ↔ ARM | integral | 0 |
| PROP bottom ↔ EY tops | far above | > 40 |
| WP top edge ↔ LID front edge | fold | 0 |
| WP leading edge ↔ floor | touching | 0–0.5 |
| SS bottom ↔ floor | skims | 0.5–1 |
| SS top bead ↔ RIM | integral | 0 |
| CP ↔ WP (V2) | screwed flat | 0 |
| SB ↔ CP (V2) | sandwiched | 0 |
| SB edge ↔ floor (V2) | touching | 0 |
| WH bottom ↔ floor | touching | 0 |
| WH side ↔ SS inner face | inside | 2–4 (guess) |
| Floor plate ↔ floor | above | 1–2 (guess) |

---

## 6. Mechanism

1. **Drive**: two internal wheels near the rear, differential steering; the **front wedge tip rests on the floor**, so the robot is a three-point stance: two wheels + wedge edge.
2. **Wedge**: the long 39° slope with a sharp (V2: steel) edge gets under opponents and lifts their front, letting the robot push them; the inclined sides deflect side hits upward.
3. **Arm/propeller**: a micro servo under the slot swings the arm (through the crank foot) **forward/back** through the slot. Its force is tiny; it is **cosmetic** (waving "antenna/hair") or at most a **poke/flag** (guess, medium). It could not self-right a 150 g robot with a 4 mm printed rod.
4. **Invertibility**: the body is only 32 mm tall and the wheels are internal; inverted it probably **cannot drive** (the eyes and arm stand on top, wheels likely do not protrude above the lid; guess, medium). The robot relies on its wedge not to be flipped.

---

## 7. Assembly order (suggested rebuild, V3)

1. Print **SH** (tub with floor, wheel slots, the inclined side walls with rounded top bead, and the front wedge with five almond slots), the **lid** (one or two plates with the slot cut and 4 countersunk/clearance holes), the **two eye domes**, two **pupil discs**, and the **arm + propeller** (one print; arm printed flat).
2. Fit the **drive motors** and **wheels** inside at the rear.
3. Fit the **servo** under the slot location, horn axis along X at about (0, −4, 20).
4. Fit **battery, receiver/ESC, switch**.
5. Screw the **arm foot** to the servo horn so that the arm stands up through the slot.
6. Place the **lid** into the rim pocket and fasten with **4 black M3 screws**.
7. Glue the **pupils** into the domes and glue/screw the **eyes** onto the lid at their staggered positions.
8. (V2 variant) screw the **steel scraper blade** and **clear plate** over the wedge with 3 screws.

---

## 8. Coordinate frame (restated, key numbers)

- SH footprint: x ∈ [−48, +48], y ∈ [−49, +49]. Lid top z 32 (rim top z 33.5).
- Fold lid → wedge at y +10; wedge tip at y +49, z 0.
- Side walls: from x ±48 at z 0 to x ±38 at z 32.
- EY-L (−20, −28, 32) r 12; EY-R (+22, −8, 32) r 12.
- Slot centre (0, +2), 12 × 20. Arm root (0, +4, 32), top (+8, +24, 92). Propeller centre (+8, +24, 93).

## 9. Profiles as math

**9.1 Body side profile (YZ, constant for x inside ±38).**
- z(y) = 32 for −49 ≤ y ≤ +10; z(y) = 32·(49 − y)/39 for +10 < y ≤ +49 (slope tan⁻¹(32/39) = 39.4°).

**9.2 Cross-section (XZ, any y in the box part).**
- Half-width h(z) = 48 − 10·z/32 for 0 ≤ z ≤ 28.5, then a fillet r 3.5 rounding into the top at x ±38: so the section is a trapezoid 96 wide at the floor and 76 at the top, top corners rounded r 3.5.
- In the wedge part, the same side bevel is cut, so the wedge panel's half-width at height z is h(z), giving the trapezoidal wedge face.

**9.3 Eye dome.**
- Spherical cap: sphere radius R = 12.5, centre at z = 32 − 0.5; cap from z 32 to z 44: points with (x − xc)² + (y − yc)² + (z − 31.5)² = 12.5², z ≥ 32. Base radius √(12.5² − 0.5²) ≈ 12.5. Pupil: disc r 4.25 on the sphere, centred at polar angle 25° from the top, tilted toward +Y.

**9.4 Almond slot.**
- In the wedge plane (u along X, v up the slope), each slot is the intersection of two circles of radius R = 8 whose centres are at (uc, vc ± 6): a vesica of length 2·√(8² − 6²) = 10.6 ≈ 11–13 and width 2·(8 − 6) = 4. Centres uc = −30 + 15k, k = 0…4, at v = 25 along the slope (z ≈ 16), each rotated 15° about the panel normal.

**9.5 Arm.**
- Centre line: foot from (0, −8, 22) straight to (0, +2, 30) (elbow radius 4), then a straight line to (+8, +24, 92): direction (0.12, 0.33, 0.94), length ≈ 66. Section 4 × 4 with 0.5 fillets.

**9.6 Propeller.**
- In plane z = 93 (tilted ±8° per blade about its long axis), blade outline half-width w(s) = 2.5·(1 − |s|/15) for s ∈ [−15, 15] along the blade direction (20° from X); hub box 6 × 6 × 4 centred on the arm top.

**9.7 Rim bead.**
- A cylinder of radius 3.5 along Y at (x ±36.5, z 29.5) from y −49 to +10, closed at the rear by a quarter-sphere end cap.

## 10. Pixel-based measurements (aws71, native px, ±10 px)

- Wedge bottom edge: (80, 940) → (1240, 1530): length ≈ 1300 px (foreshortened, receding to the left).
- Lid/wedge fold: (400, 690) → (1250, 1190).
- Right side top bead: (1250, 1190) → (1930, 880); the bead's rear end cap at about (1930, 880–1000).
- EY-L: centre (790, 580), base width 300 px. EY-R: centre (1290, 960), base width 380 px.
- Screws: (680, 520), (510, 665), (1475, 1065), (1275, 1245); head width ≈ 85–95 px for the near ones.
- Slot: (870–1000, 770–930). Arm: base (900, 880), top (1300, 110); width 40–50 px. Propeller: (1125, 80) to (1465, 190), hub at (1300, 100).
- Almond slots: (415, 530), (555, 610), (665, 720), (800, 840), (915, 1220)... the last (lowest) at the right end of the row; each about 100 × 40 px.

## 11. Several independent estimates of key quantities

| Quantity | Method A (rules / kit) | Method B (ratio in photo) | Method C (pixels + scale) | Reconciled |
|---|---|---|---|---|
| Scale near EY-R | — | — | M3 button head 5.7 mm = 90 px → 15.8 px/mm | **≈ 15.8 px/mm (near), ≈ 12.5 (mid)** |
| Eye Ø | kit sphere r 11 → 22 | eye ≈ 1/4 of lid width → 76/4 = 19–24 | 380 px / 15.8 = 24 | **24** |
| Eye height | kit full sphere (r 11) | dome height ≈ 0.48 × base | — | **11.5** |
| Body width | kit 100 | eye Ø × 4 ≈ 96 | (V2) wedge width ≈ 3.8 × eye 24 = 91 | **96** |
| Body length | kit 105 (too long for the cube with arm lean, still < 101.6 needed) | ≈ 1.0 × width (looks square in aws66 top view) | — | **98** |
| Body height | kit 36 | screws/eyes: side ≈ 1.35 × eye Ø → 32 | right side slant 330 px at ≈ 11 px/mm → 30 slant → 32 high with 72° | **32** |
| Wedge angle | kit ramp 95 (length) | V2 side silhouette ≈ 35–40° | rise 32 / run 39 | **39°** |
| Arm length | kit post 50 | arm ≈ 2.6 × eye Ø → 62 | 790 px at ≈ 12.5 px/mm → 63 | **62–65** |
| Arm top height | kit post top z 78 | 32 + 62 × cos 20° = 90 | — | **90–94 (< 101.6)** |
| Propeller span | kit 18 | ≈ 1.25 × eye Ø → 30 | 345 px / 12 → 29 | **30** |
| Arm section | kit 4 × 4 | ≈ 1/6 of eye Ø → 4 | 45 px / 12 → 3.8 | **4 × 4** |

## 12. Consistency check: conflicts and reconciliation

1. **Length vs cube**: kit 105 mm exceeds 101.6. Reduce to **98** (the body looks square: aws66 top view gives ratio ≈ 1.0).
2. **Arm height**: an arm of 62 mm on a 32 mm body reaches **z ≈ 90–94** when leaning 20°, and 96 if vertical: fits under 101.6 **only just**; the propeller hub must stay under 98. Reconciled: arm 60 above the lid, hub top z ≤ 96.
3. **Eye stagger**: in aws71 EY-L is clearly farther back than EY-R (EY-R is close to the front-right screws and the wedge fold region). In aws67 (camera front-left) the stagger is less clear and EY-L looks slightly farther forward; the kit draft has the left eye forward. Because aws71 is the clearer, larger, latest photo, **EY-L at y −28 and EY-R at y −8** is kept (medium). For V2 swap if needed.
4. **Inclined sides**: aws71 shows the right side slanting and aws67 the left side slanting (green tape), so **both sides are inclined**: consistent (medium-high on the angle 60–75°).
5. **Wheels**: none visible in three photos from three directions, so they must be **inside**; consistent with kit `outside: false`.
6. **Arm motion**: three different poses across three events, a long slot, and a crank foot all point to a **servo-driven** arm. Kept (medium-high).
7. **Mass**: a 96 × 98 × 32 printed tub (2.5 mm walls) ≈ 45–55 g, two N20 motors 20 g, wheels 6 g, battery 10–15 g, ESC/receiver 8 g, servo 4–9 g, screws/eyes/arm 8 g: total ≈ 105–125 g, under 150 g. Consistent.

---

## 13. Why the designer did it (per part, adversarial)

Common lens: a beginner's robot (the name says it). Its game plan is to **push and get under** with a wedge, survive hits through low height and inclined faces, and be fun to watch (the face). Attackers: horizontal spinners (hit the sides), vertical spinners (hit the front/top), wedges and flippers (try to get under), and pushers.

- **Long front wedge (WP)**
  - Fight: the 39° slope with a sharp edge gets under flat-fronted opponents and lifts their front wheels, taking away their traction so the robot can push them into the arena hazards or wall. The long ramp means a lifted opponent ends on the robot's lid rather than sliding off.
  - Against attacks: vertical spinners hitting the slope have their blows partly deflected upward; horizontal spinners hit a glancing surface.
  - Weakness: a printed edge cannot be as sharp as metal, so other wedges get under it; in V2 the designer **added a steel scraper blade** for exactly this reason, and clear polycarbonate on top for toughness (polycarbonate does not shatter).
  - Construction: one flat printed panel; slots (MS) save weight and print time and add character as a "mouth".

- **Inclined side walls (SS) and rounded top bead**
  - Fight: side hits from horizontal spinners and pushers glance off a sloped wall instead of landing squarely; opponents trying to push from the side tend to ride up.
  - The rounded bead makes the top edge less likely to be chipped (V1/V2 show heavy chipping on square edges, which the designer fixed in V3).
  - Construction: the slope also stiffens the tub and hides the wheels.

- **Internal wheels**
  - Fight: nothing outside to be hit by spinners; the robot cannot be grabbed by its wheels.
  - Cost: narrower track and less invert ability; acceptable for a pushing wedge.

- **Low height (32 mm)**
  - Fight: low centre of gravity, hard to flip, little side area for spinners.

- **Inset lid with rim and four screws**
  - Construction: easy access to electronics; the rim protects the lid edges and screws from glancing blows.
  - Weakness: the slot in the lid lets debris in.

- **Eyes (EY) and pupils**
  - Fight: none; decorative. They are the tallest parts on the lid besides the arm, so they act as soft sacrificial bumpers (they will be knocked off before the lid is hit). V1 screwed them on through the pupils (screw doubles as pupil): a neat beginner trick.

- **Servo arm with propeller (ARM, PROP)**
  - Fight: essentially none (too thin to hurt or self-right). Possibly a **visual "weapon"** and crowd-pleaser; a moving part also makes the robot look active to judges (activity/aggression scoring, guess).
  - Weakness: easily snapped; cheap to reprint (V2 black, V3 white versions show it was replaced).
  - Construction: the crank foot screws straight onto a standard servo horn; printing the arm flat gives strong lengthwise layers.

- **Material evolution (V1 wood/laminate → V2 painted + tape + polycarbonate + steel → V3 printed)**
  - The early shell chipped and needed tape repairs; the final version is fully printed with rounded edges and a clean screw-on lid, easier to repair and reprint.

---

## 14. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Drive wheels | 2 × rubber/foam wheels | Ø 22 × 8 | (±36, −25, 11) inside wheel wells | medium |
| Drive motors | 2 × N20 gearmotors, shafts along X | 12 × 10 × 25 | (±20, −25, 11) | medium |
| Arm servo | micro servo (3.7–9 g), output axis along X | 23 × 12 × 23 | (0, −6, 16), horn under the slot | medium |
| ESC/receiver | all-in-one ant board (e.g. receiver with dual brushed ESC) | 30 × 20 × 6 | (+18, +5, 8) under the wedge | medium |
| Battery | 2S 7.4 V LiPo 150–300 mAh | 40 × 18 × 10 | across the rear (0, −40, 8) or under EY-L | medium |
| Switch/link | slide switch or removable link | 10 × 6 | rear wall | low |
| Floor | printed floor (integral with tub) | 2 thick | z 0–2 | medium |
| Wiring | motor leads short at the rear; servo lead to receiver; battery → switch → board | — | inside | medium |
| Lid screw bosses | 4 printed bosses with heat-set inserts or self-tapping | Ø 7 | under the screws | medium |

## 15. What the photos cannot show
- The rear wall, underside, wheel positions and size, and whether the wheels protrude above the lid.
- Whether the arm moves, and its range.
- Exact eye positions (they differ between versions).
- All mm values are scaled estimates (±10–15%).
