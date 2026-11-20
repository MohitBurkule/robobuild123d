# Blue Terror: full rebuild description from the reference photo

Source photo (only one):
- `robots/blue_terror/reference/blue-terror.aws72.webp` (1469 × 1220 px): AWS 72. Cut out onto white by the AWS wiki. The camera is at the **front-right**, about **35–40° down**; the front (the clear scoop) faces the lower right, so the robot's **right** side, with its three wheels, is on the image **left**, and the left side's three wheels are at the upper right. The clear polycarbonate parts pick up a strong **green tint** from the cut-out background (the scoop is really **clear**).

Facts are read from the photo; inferences are marked **(guess)**. Sizes are **estimates in mm**, from the AWS limit (150 g, 101.6 mm cube) and the spec draft (body 95 × 54 × 26, **six outboard wheels** r 12, a wedge with a scoop). Ratios are against **W = tub width ≈ 54 mm**.

---

## 0. Coordinate system and naming

- **Origin O** = floor point (z = 0) under the centre of the blue tub's footprint.
- **+X** = robot right, **+Y** = forward (toward the scoop), **+Z** = up. mm.
- Tub extents (reconciled §12): x ∈ [−27, +27], y ∈ [−39, +39], z ∈ [3, 26]. Wheels outboard to x ≈ ±46. Scoop to y ≈ +60 on the floor, x ≈ ±34.

| ID | Part |
|---|---|
| TB | translucent blue printed tub |
| LD | clear polycarbonate lid |
| S-LD | 6 silver Phillips lid screws |
| LB | black tape label "BLUE TERROR" (blue marker) |
| FB | blue front bulkhead / cross-member under the lid's front |
| BR-L, BR-R | blue scoop brackets (vertical lugs at the front corners) |
| S-BR | 2 silver Phillips screws per bracket |
| SC | clear polycarbonate scoop (bent "dustpan": face + side flaps) |
| SC-F | scoop face |
| SC-L, SC-R | scoop side flaps (folded back) |
| WH-R1..3, WH-L1..3 | six black knurled wheels (front, middle, rear on each side) |
| MT-x | black drive motor gearboxes / shaft housings visible between the wheels |
| BAT | LiPo battery (white warning label visible through the lid) |
| WR | red and black wires, red connector |
| ESC, RX, SW | hidden electronics |

---

## 1. Overall description in one paragraph

Blue Terror is a **six-wheel wedge pusher**. Its body is a **translucent bright-blue printed tub** about 54 mm wide, 78 mm long and 23 mm tall, closed by a **clear polycarbonate lid** held by **six silver screws**, so the **battery** (its white warning label readable upside down), **red and black wires** and a red connector are visible inside. A strip of **black tape** across the lid carries the name **"BLUE TERROR"** hand-written in blue marker. Along each side, **three black knurled wheels** (about Ø 26 × 12 mm, with large hollow hubs) are mounted outboard on short shafts, nearly touching each other, so the sides are almost solid walls of tyres; between them, black motor gearbox ends show. At the front, two **blue vertical brackets** with two screws each hold a **clear bent polycarbonate scoop**: a sloping face running down to the floor with **two side flaps** folded back, like a dustpan, wider than the tub and covering the front wheels' inner faces.

---

## 2. Part-by-part description

### 2.1 Tub (TB)
- **Shape**: a rectangular open box, **54 mm wide × 78 mm long × 23 mm tall** (z 3 to 26), walls about **2.5 mm** thick, with internal **screw bosses** in the corners and at mid-length of the side walls (visible through the lid as blue cylinders). The top rim is flat for the lid.
- **Internal layout (seen through the lid)**: a **front compartment** behind the front bulkhead holds the **battery** lying across the width (white label, "WARNING… NEVER LEAVE CHARGING BATTERIES UNATTENDED… LiPo… CE", printed upside down from the camera's view); the **middle/rear** holds the receiver/ESC (a dark board with a small red part) and **red and black wire loops**.
- **Sides**: between the wheels, black cylindrical parts (Ø about 10 mm) stick out of the side walls at axle height: the **gearbox ends / shaft housings** of the drive motors **(MT)**.
- **Colour/material**: **translucent bright blue PETG/PLA**, glossy, with visible layer lines and stress whitening at the bracket screws.

### 2.2 Lid (LD) and screws (S-LD)
- **Shape**: a flat **clear polycarbonate plate**, **54 × 78 × 1.5 mm**, edges cut square, lying on the tub rim.
- **Screws**: **6 silver Phillips pan screws** (head Ø 4 mm, M2): four at the corners (about 4 mm in) and two at mid-length on each side (image: (300, 270), (495, 205), (720, 150), (1085, 460), (600, 625), (875, 545)).
- **Label LB**: a **black tape strip**, about **40 × 18 mm**, across the lid at mid-length, angled slightly, with **"BLUE" over "TERROR"** written in blue marker (letters about 6 mm tall).

### 2.3 Front bulkhead (FB)
- **Shape**: the tub's front wall, thickened into a **blue cross-member** about **54 mm wide × 6 mm deep × 20 mm tall**, its front face set back about 4 mm from the lid's front edge. Below the lid's front edge a darker band shows the gap above the battery.

### 2.4 Scoop brackets (BR-L, BR-R)
- **Shape**: two **blue printed vertical lugs**, each about **10 mm wide (X) × 8 mm deep (Y) × 26 mm tall**, at the front corners of the tub (x ≈ ±22), standing proud of the front wall. Each has a **sloped front face** following the scoop's angle.
- **Screws S-BR**: **two silver Phillips pan screws** per bracket, one high (z ≈ 20) and one low (z ≈ 6), passing through the scoop face into the bracket (image: right bracket (1170, 580) and (1215, 700); left bracket (685, 760) and (725, 905)).
- **Function**: the only mounts for the scoop; they also act as front corner posts.

### 2.5 Scoop (SC)
- **Material**: **clear polycarbonate sheet**, about **1.5 mm** thick, with scuffed white edges and some scratches on the face.
- **Face SC-F**: a flat sloping plate about **68 mm wide** (wider than the tub) and **34 mm long** down the slope, running from the top of the brackets (y ≈ +44, z ≈ 26) down to the floor at **y ≈ +60**, steep (about **66°**) in its upper part, with a lower section bending to a shallower angle. In the photo the face shows a **horizontal fold line** about 8 mm above the floor (image y ≈ 1020–1040 across the scoop), where the sheet bends to a **shallower lip** (about 25°) for the last 10 mm. Reconciled profile in §10.1.
- **Side flaps SC-L/SC-R**: each side of the face is **folded back** by about 110° to form a **triangular side flap**, about **30 mm long × 26 mm tall** at the back, tapering to the floor at the front, so the scoop is a **three-sided dustpan**. The flaps sit just outside the front wheels' inner faces (x ≈ ±34).
- **Fixing**: four screws through the face into the two brackets.

### 2.6 Wheels (WH)
- **Shape**: **Ø 26 mm × 12 mm**, **black printed or rubber wheels** with a **knurled/gear-tooth tread** (about 40 square ribs, 1.5 mm tall) and a **large hollow centre**: a hub hole about **Ø 10 mm** (dark, open through), with a flat outer face ring about 8 mm wide.
- **Positions**: three per side, centres at **x = ±40**, **y = +27, 0, −27**, **z = 13**. Tyre gap between neighbours about **1 mm**. Tops at z = 26 (level with the lid), bottoms at z = 0.
- **Mounting**: each wheel is on a short shaft emerging from the tub side; between each wheel and the tub, a black **spacer/gearbox end** (MT) about Ø 10 × 6 mm.
- **Drive**: either **six motors** (one per wheel, the black cylinders being N20 gearboxes) or **two motors with gear/belt coupling** (the black parts being idler shafts). The six identical black cylinders suggest **six N10/N20 micro gearmotors** or **two motors driving the middle wheels with the outer wheels geared** **(guess; see §13)**.

### 2.7 Battery (BAT), wiring (WR)
- **BAT**: a flat LiPo, about **45 × 25 × 8 mm**, lying across the front compartment with its label up (readable through the lid).
- **WR**: red and black silicone wires (about 22 AWG) looping at the rear-centre, a **red JST/XT-style connector** at the front-centre beside the battery.

---

## 3. Per-view descriptions

### 3.1 Top view (inferred)
- A blue rectangle 54 × 78 with a clear lid, the black name label in the middle and six screws. Along each side, three black 26 × 12 wheel rectangles touching each other (overall width about 92 mm). In front, the scoop: a 68 mm trapezoid extending 19 mm ahead of the brackets, with the side flaps as thin lines angled back to the front wheels.

### 3.2 Front view
- The clear scoop dominates: a wide trapezoid with two blue brackets and four screws visible through it; behind it the blue front bulkhead and the battery; the six wheels' front pair at the outer edges, their tops level with the lid.

### 3.3 Right side view (inferred from the photo's near side)
- A row of three black knurled wheels nearly touching, covering almost the entire side (78 mm of wheels on a 78 mm body), the blue tub visible only as a thin band above and between them; at the front, the scoop's side flap triangle running down to the floor.

### 3.4 Rear view (inferred)
- The rear wall of the tub (54 × 23) between the rear wheels; the lid edge on top. Probably the switch is here **(guess)**.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| TB | open box | 54 × 78 × 23 | 1 × 1.44 × 0.43 | translucent blue | — | 1 |
| LD | flat plate | 54 × 78 × 1.5 | 1 × 1.44 | clear PC | 6 × M2 | 1 |
| LB | tape label | 40 × 18 | 0.74 | black tape + blue marker | adhesive | 1 |
| FB | bulkhead | 54 × 6 × 20 | 1 | blue | integral | 1 |
| BR | lug | 10 × 8 × 26 | 0.19 × 0.15 × 0.48 | blue | integral (guess) | 2 |
| SC-F | sloped sheet | 68 × 34 × 1.5 | 1.26 × 0.63 | clear PC | 4 × M2 | 1 |
| SC-L/R | folded flap | 30 × 26 triangle | 0.56 | clear PC | bent | 2 |
| WH | knurled wheel | Ø 26 × 12, bore Ø 10 | 0.48 × 0.22 | black | shaft | 6 |
| MT | gearbox end | Ø 10 × 6 | — | black | — | 6 |
| BAT | LiPo | 45 × 25 × 8 | — | white label | inside | 1 |

---

## 5. Contact / gap matrix (est. mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| TB bottom ↔ floor | clearance | 3 |
| WH bottom ↔ floor | contact | 0 |
| WH top ↔ LD top | level | 0 |
| WH ↔ neighbouring WH | tread gap | 1 |
| WH inner face ↔ TB side | spacer | 6 |
| LD ↔ TB rim | screwed | 0 |
| SC-F ↔ BR | screwed | 0 |
| SC leading edge ↔ floor | contact | 0–0.5 |
| SC-L/R ↔ front WH inner face | near | 2–3 |
| BR ↔ TB front | integral | 0 |
| BAT ↔ LD underside | near | 1–2 |

---

## 6. Mechanism

1. **Drive**: six-wheel skid steer. With three wheels in a near-continuous row per side, the robot behaves like a tracked vehicle: high traction for pushing, and the middle wheel carries weight when the front is lifted. Turning scrubs the front and rear wheels.
2. **Weapon**: none; a **wedge/scoop pusher**. The clear scoop gets under opponents; the six-wheel drive then pushes them.

---

## 7. Assembly order (suggested rebuild)

1. Print the blue tub with bosses, bulkhead and front brackets.
2. Install the drive motors (six micro gearmotors in pockets along the side walls, or two motors plus gear trains) with shafts through the side walls at z 13, y +27 / 0 / −27.
3. Press on the six wheels.
4. Fit the battery across the front compartment, the ESC, receiver and switch; route the wires.
5. Screw on the clear lid (6 screws); apply the name label.
6. Bend the polycarbonate scoop (face fold + two side folds), drill four holes, and screw it to the brackets.

---

## 8. Hidden / uncertain list
- Motor count and gearing.
- Switch location; rear wall.
- Exact scoop profile (single slope vs two-angle).
- Underside.
- Sizes ±15% (single photo).

---

## 9. Coordinate frame (restated)
- Origin under the tub centre; +X right, +Y forward, +Z up; mm.
- Tub x ∈ [−27, 27], y ∈ [−39, 39], z ∈ [3, 26]. Wheels (±40, +27 / 0 / −27, 13), Ø 26 × 12. Brackets at x ±22, y +39 to +47. Scoop leading edge at y +60, x ∈ [−34, 34].

## 10. Profiles as math

**10.1 Scoop face (YZ, centre section).** Upper part from (y +45, z 26) to (y +53, z 8): z = 26 − 2.25·(y − 45) (66°); the fold at z 8; lower lip from (+53, 8) to (+60, 0): z = 8 − 1.14·(y − 53) (48.8°). Thickness 1.5 behind the line. Total scoop reach ahead of the tub: 21 mm (leading edge y = +60).

**10.2 Side flap (plan and side).** Each flap is the triangle with vertices (top-back) (±34, +45, 26), (bottom-back) (±34, +45, 0) and (bottom-front) (±34, +60, 0), folded from the face along its side edge.

**10.3 Wheel.** Tread r(φ) = 12.0 + 1.0·[sin(40φ) > 0]; bore r 5; width 12; outer face ring r 5–9 flat.

**10.4 Lid screw layout (XY).** (±23, ±35) and (±23, 0).

## 11. Pixel-based measurements (1469 × 1220)

- Lid: corners about (240, 285), (720, 145), (1110, 470), (600, 655).
- Wheels (robot right, near): front (350–540, 565–790), middle (200–380, 390–620), rear (70–230, 225–420). Robot left (far): front (1050–1250, 340–520), middle (870–1060, 195–360), rear (700–860, 60–220).
- Scoop: top edge from (470, 720) to (1260, 480); fold line from (450, 1000) to (1355, 860); leading edge at y ≈ 1080–1140 on the near (left) end.
- Brackets: right (650–770, 640–950); left (1130–1250, 520–760).
- Label: (440–860, 290–460).

## 12. Several independent estimates of key sizes

| Quantity | Method A (spec/rules) | Method B (ratios) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Tub width | 54 (spec) | — | lid short side ≈ 560 px (oblique) | **54** |
| Tub length | 95 (spec, incl. scoop?) | 3 × Ø 26 + 2 gaps = 80 | lid long side ≈ 1.45 × short side → 78 | **78** |
| Height | 26 (spec) | 0.48 W = wheel Ø 26 | wheel tops level with the lid | **26** |
| Wheel Ø | 24 (r 12 spec) | 0.48 W | near front wheel 225 px vs lid width 560 px → 0.40 × 54 = 22 (perspective, nearer → larger, so ~24–26) | **26** |
| Overall width | — | 54 + 2 × (6 + 12) = 90 | — | **92** |
| Scoop width | — | 1.26 W | top edge 830 px vs lid short side 560 px (scoop nearer) → 68 | **68** |
| Overall length | ≤ 101.6 | 78 + 21 = 99 | — | **99** |

## 13. Consistency check: conflicts and reconciliation
1. **Spec 95 × 54**: 95 is the overall length with the scoop (78 + ~20); consistent with the photo. **Reconciled tub 78, overall 99.**
2. **Wheel size**: r 12 (spec) gives Ø 24; three wheels of Ø 26 nearly touching cover 80 mm, about the tub length. Ø 24 would leave 3 mm gaps, also plausible; the photo shows gaps of about 1 mm. **Reconciled Ø 26.**
3. **Motors**: six black shaft housings, one per wheel. Six N20 motors (≈ 60 g) leave about 90 g for the rest, possible for a simple wedge. Alternatively two motors and geared outer wheels. **Reconciled: six motors (medium-low)**; a builder could use 2 motors with a gear train.
4. **Scoop profile**: the face appears steep at the top and shallower near the floor (a fold line). **Reconciled two-angle profile (§10.1).**

---

## 14. Why the designer did it (per part, adversarial first)

- **Six wheels in solid rows**
  - Fight: maximum **pushing traction** and a near-continuous contact patch, like tracks. If an opponent lifts the front, the middle and rear wheels still drive; if one wheel is damaged, five remain. The tyres form the robot's sides: a horizontal spinner hitting the side hits rubber/printed tyres that bounce rather than the tub.
  - Invertibility: wheel tops are level with the lid, so it drives upside down (the scoop then points up; the robot is less effective but not stranded).
  - Threats: outboard wheels are exposed to side hits; each is cheap and replaceable.
- **Clear polycarbonate dustpan scoop**
  - Fight: polycarbonate is **thin, tough and flexible**: the leading edge can be very thin (1.5 mm) to get under opponents, and it bends instead of cracking when hit by spinners. The side flaps **funnel** opponents onto the centre and **shield the front wheels**' inner faces from being caught. The scoop is wider than the tub, so opponents at an angle meet it before the tyres.
  - Being got under: the scoop's edge is on the floor, as low as practical; a steel wedge could still beat it.
  - Construction: one sheet, three folds, four screws: quick to replace.
- **Translucent tub and clear lid**
  - Construction: everything inside is visible for checks (battery state, loose wires) without opening; the lid is polycarbonate, so a flipper or lifter landing on it does not shatter it.
  - Identity: bright blue = "Blue Terror", with a hand-written tape label.
- **Battery across the front**
  - Fight: puts weight over the front wheels and the scoop, keeping the scoop edge pressed to the floor, which matters for a wedge.
- **Brackets as front posts**
  - Fight: take the pushing load from the scoop straight into the tub's front corners.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Drive motors | 6 × N10/N20 micro gearmotors, one per wheel (or 2 motors + gear trains) | 10 × 12 × 24 | along X in pockets at y +27 / 0 / −27, x ±15, z 13 | medium-low |
| Battery | 2S 300–450 mAh LiPo (seen) | 45 × 25 × 8 | across the front, x 0, y +25, z 8 | high |
| ESC | dual brushed ESC driving left and right groups | 25 × 15 × 5 | rear, x 0, y −20, z 8 | medium |
| Receiver | micro receiver | 20 × 12 × 5 | middle, x 0, y 0, z 15 | low |
| Switch | slide switch in the rear wall | 10 × 5 × 5 | (0, −39, 15) | low |
| Wiring | battery → switch → ESC → three motors per side wired in parallel; red connector at the battery | — | — | medium |
| Screw bosses | Ø 5 posts for the 6 lid screws | Ø 5 × 20 | under each lid screw | medium |

## 16. Mass budget (independent check)

| Item | Estimate (g) | Basis |
|---|---|---|
| 6 × micro gearmotors (N10/N20) | 54 | 9 g each (N10 ≈ 6 g, N20 ≈ 10 g) |
| 6 × wheels Ø 26 × 12 | 18 | 3 g each, hollow hubs |
| Battery 2S 300–450 mAh | 22 | label-size estimate |
| ESC + receiver + switch + wiring | 14 | — |
| Clear lid 54 × 78 × 1.5 PC | 8 | 6.3 cm³ × 1.2 g/cm³ |
| Scoop sheet ≈ 68 × 34 + 2 flaps, 1.5 mm PC | 6 | ≈ 5 cm³ |
| Tub (walls, floor, bulkhead, brackets, bosses) | 24 | ≈ 20 cm³ of PETG/PLA |
| Screws (10 × M2) | 4 | — |
| **Total** | **150** | |

The budget closes at 150 g only with **small (N10-class or light N20) motors**; six full-size N20s with metal gearboxes (about 10–12 g each) would push the total to about 165 g. This supports either **six light N10 motors** or the **two-motor + gear-train** alternative in §13. The tub's 24 g also limits its wall thickness to about 2–2.5 mm, matching the photo.

## 17. Drive-train geometry check

- **Wheelbase** (front to rear axle): 54 mm; **track** (wheel centre to centre across): 80 mm. Track/wheelbase = 1.48, so the robot is **wider in track than long in wheelbase**, which makes six-wheel skid steering workable: the scrub force needed to turn is proportional to the wheelbase/track ratio (≈ 0.68 here), so it turns readily despite six tyres.
- **Middle wheels**: on a flat floor all six touch. If the middle wheels were 0.5–1 mm lower (a common trick), the robot would pivot on them and turn faster; the photo cannot show this.
- **Ground clearance**: tub bottom at 3 mm; with the scoop edge at 0 and the wheels at 0, the scoop's weight rests partly on its lip, keeping it in contact.
- **Push force**: with about 150 g on six rubber-like tyres (μ ≈ 1.0) the maximum push is about 1.5 N; all of the weight is on driven wheels (if all six are driven), which is the point of six-wheel drive.

## 18. Matchups (how each kind of attacker meets Blue Terror)

| Attacker | Where it reaches | How Blue Terror survives / wins |
|---|---|---|
| Vertical spinner | the scoop face first (it is the most forward part) | thin PC flexes and deflects the hit upward; the brackets carry the shock into the tub; the scoop is the sacrificial part |
| Horizontal spinner | the outboard wheels (sides) | the tyres are the outer surface; they bounce the blade, and a lost wheel leaves five; the tub sits 13 mm inboard |
| Wedge | the scoop edge vs its edge | Blue Terror's 1.5 mm PC edge is thinner than most printed wedges; six-wheel traction wins the shove afterwards |
| Flipper / lifter | under the scoop or the side tyres | if flipped, the wheel tops are level with the lid, so it keeps driving upside down; the scoop then points up and is useless, so the robot must avoid being flipped |
| Pusher / control bot | head-on | six driven wheels, weight forward over the scoop: the robot is built for exactly this fight |
| Hammer / overhead | the clear lid | polycarbonate does not shatter; electronics sit low |

## 19. Alternative interpretations considered

1. **Scoop as a single straight slope** instead of two angles: possible; the fold line visible near the floor could be a tape edge. Either way the leading edge is on the floor at y ≈ +60.
2. **Front brackets printed separately** and screwed to the tub: they show a slightly different surface texture from the tub walls; they could be separate parts, which would make scoop changes faster.
3. **Black side cylinders as bearings/spacers** rather than motors: if only two motors drive the middle wheels, the cylinders would be bearing housings for idler shafts geared to the middle ones. No gear teeth are visible between the wheels, so belts or internal gears would be needed.

## 20. Surface and wear reading

- **Scoop**: the face is scuffed with fine horizontal scratches and its leading edge is whitened along the full width, the marks of driving under opponents and scraping the floor; the outer top corner of the right side flap (image lower left) is slightly bent outward, showing a side hit.
- **Wheels**: the knurled treads are intact and the outer faces show only light dust: no wheel has been struck hard.
- **Tub**: stress whitening around the bracket screws (the brackets take the push load); the lid is clear with few scratches, so the robot has rarely been driven over or flipped onto its lid.
- **Label**: the black tape name strip is slightly crooked and lifting at one corner, a hand-applied identity mark rather than a printed decal.
