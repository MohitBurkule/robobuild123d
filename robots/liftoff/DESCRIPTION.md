# Liftoff: full rebuild description from reference photos

Source photo (cut out onto white by the AWS wiki):
- `robots/liftoff/reference/liftoff.aws76.webp`: AWS 76, native 1759 × 1100 px. **Front-right, low-to-mid**: camera about 25–30° above the floor and about 30–35° to the robot's right of straight-on, close (noticeable perspective: the right front wedge looks much larger than the left). Visible: both front wedges with their clear plates, the black centre lifter plate, the tops of both side pods, the right side's sloped outer face with a hole, both rear wheels (right fully, left top only), a screw/pin sticking up at the rear-right corner, and a blue part under the right pod's lid. Not visible: the rear, the underside, the left outer side.

One photo only, sharp and well lit. Facts are read from it; inferences are marked **(guess)**. Dimensions are estimates scaled from the 150 g / 101.6 mm cube limit and the project kit draft (`kit.json`: lifter; body 72 long × 80 wide × 24 tall; two wheels r 13 × 8 at y −22; two polycarbonate-faced wedges in side profile (y 30, z 2) → (y 80, z 0) → (y 36, z 26), at |x| 14–44; a black lift plate 24 × 80 × 3 at z 27 with its pivot at (y −28, z 26)). Ratios are against **W = body width across the pods ≈ 80 mm**.

---

## 0. Coordinate system and naming

- **+X** = robot right, **+Y** = forward (toward the wedges), **+Z** = up. mm.
- **Origin O** = the floor point under the centre of the body footprint (between the pods, mid-length of the pods).
- In the photo the front faces the lower-left; the right side faces the lower-right.

| ID | Part |
|---|---|
| PD-L, PD-R | white printed side pods |
| WG-L, WG-R | sloped front wedge faces of the pods |
| CP-L, CP-R | clear polycarbonate face plates on the wedges |
| S-CP | Phillips pan screws on the clear plates (4 each) |
| LD-L, LD-R | white pod top lids |
| S-LD | silver pan screws on the lids |
| RB-L, RB-R | ribbed (grip-textured) sloped outer side faces of the pods |
| HL | round hole in the right pod's outer face |
| LP | black centre lifter plate (flat rear + sloped front ramp) |
| BN | bend/crease line on LP |
| PV | lifter pivot (hidden at the rear, guess) |
| SV | lifter servo (blue, seen under LD-R) |
| PIN | screw/pin sticking up at the rear-right corner |
| WH-L, WH-R | two rear drive wheels (black, knurled) |
| M-L, M-R | drive gearmotors (hidden) |
| BAT, ESC, RX | electronics (hidden, guess) |

---

## 1. Overall description in one paragraph

Liftoff is a **flat, low, two-wheel servo lifter** built mostly in **white printed plastic**. The body is three strips side by side: a **white pod on each side** (about 25 mm wide) and a **matt black lifter plate** in the middle (about 30 mm wide), all running front to back. Each pod's front is a **long sloping wedge** reaching the floor, faced with a **screwed-on clear polycarbonate plate** (four screws; the left one edged in black). The pods' outer sides are **chamfered slopes** with a **ribbed grip texture**, and their tops are **flat white lids** with small silver screws. The **black lifter plate** lies between the pods: its rear two-thirds is flat at the pods' top height, and its front third is **bent down** into a ramp whose front edge sits just above the floor, set back from the pod wedges. It is lifted by a **blue micro servo** visible under the right pod's lid. Two **black, knurled rear wheels** (about Ø 30) are outboard at the back corners, beside the pods' cut-back rear ends. A **screw sticking up** from the rear-right of the right pod looks like the **arming link** (guess).

---

## 2. Part-by-part description

### 2.1 Side pods (PD-L, PD-R)
- **Shape**: two long white prints, each about **25 mm wide (X) × 78 mm long (Y) × 22 mm tall (Z)** (top at z ≈ 24), at **x ∈ ±[15, 40]**. Each has:
  - a **flat top** (the lid LD) from about y −40 to y +4;
  - a **front wedge WG** sloping from the top front edge (y ≈ +4, z 24) down to the floor at about **y ≈ +44**, i.e. about **31°**;
  - an **outer side chamfer RB** sloping from the top outer edge down and outward at about **55–60°** (from x ≈ ±36 at z 24 to x ±40 at z 8), carrying a **ribbed texture** (parallel ridges about 1 mm apart, running fore-aft), and then a short vertical band to the floor;
  - the **rear end cut back** on the outside (a notch about 12 mm wide × 30 mm long) to make room for the wheel.
- **Colour/material**: **off-white/ivory FDM** (PLA or PETG), matt with faint layer lines; the wedge regions are slightly translucent at the edges.
- **Inner faces**: vertical, facing the lifter plate with about **1–2 mm** clearance.
- **HL**: a **round hole about Ø 4 mm** in the right pod's outer face, low down near the front of the wheel notch at about (+39, −2, 8): an **axle/motor screw access** or a **switch/LED hole** **(guess)**.

### 2.2 Pod lids (LD-L, LD-R)
- **LD-L**: a flat white plate about **25 × 44 × 2 mm** on top of the left pod, with **two silver Phillips pan screws** (Ø ≈ 4 mm, M2): one at its rear-outer corner (native (835, 85)) and one at its front-inner corner (native (525, 318)). Flush with the pod top.
- **LD-R**: a similar plate on the right pod, but it **sits slightly raised**, with a **visible gap** (about 2–3 mm) along its inner side and front, under which a **blue part** (the servo, SV) and a **white internal part** show. One silver screw at its front-inner corner (native (1222, 478)). It may be a **lid that bulges over the servo** or a **hatch held by one screw** **(guess)**.

### 2.3 Front wedges (WG) and clear plates (CP)
- **WG**: the sloping front face of each pod, about **25 mm wide × 46 mm long (down the slope)** at about **31°**, from the lid front (y +4, z 24) to a sharp toe at (y +44, z 0).
- **CP-L/CP-R**: **clear polycarbonate plates** (about **1 mm** thick), slightly smaller than the wedge face (about 23 × 40 mm), lying on it and screwed at the **four corners** with **silver Phillips pan screws** (head Ø ≈ 4 mm). The plates are scuffed and show **diagonal scratch lines** and a frosted look. Their **lower edge overhangs the printed toe by about 1–2 mm** to give a thinner leading edge **(guess)**.
  - **CP-L** has a **black border** about **2–3 mm** wide along its edges and around each screw boss (a black outline, probably **black tape** or a **black-printed rim/recess** under the clear plate) **(guess)**.
  - **CP-R** shows **raised round bosses** under each screw (the white print's screw bosses showing through) and a **small empty hole** at its upper-right (a fifth hole, unused or for a missing screw).
- The toes of the two wedges are the **lowest front points**, on the floor.

### 2.4 Black lifter plate (LP)
- **Shape**: a **matt black printed plate** (PLA/PETG) about **30 mm wide (x ±15) × 3 mm thick**, about **80 mm long** in total, with a **bend line BN** at about 55% of its length from the rear:
  - **Rear flat part**: about **44 mm long**, from y ≈ −40 to y ≈ +4, at z ≈ 24–27 (flush with or 1 mm above the pod lids). A **faint transverse seam** across it at about y −14 (a print layer change or a joint between two parts).
  - **Front ramp**: about **38 mm long**, sloping down at about **25–28°** from BN to its front edge at about **(y +38, z 6–8)**, i.e. about **6 mm behind** and about **6–8 mm above** the pods' toes. Its **front-right corner is chipped**.
- **Pivot PV (hidden, guess)**: at the rear, about **(y −36, z 22)**, on a transverse axis; lifting rotates the whole plate so the front ramp rises.
- **Clearance**: 1–2 mm to the pods' inner faces on each side.

### 2.5 Servo (SV)
- A **blue** part seen through the gap under LD-R (native (1220–1300, 330–540)): almost certainly a **blue SG90-type 9 g micro servo** (23 × 12 × 23 mm), lying in the right pod with its output **toward the centre (−X)** to drive the lifter plate's pivot or a horn under the plate **(guess)**.

### 2.6 Pin (PIN)
- A **silver pan-head screw** sticking up about **10 mm** from the rear-right corner of the right pod top (native (1560–1575, 140–215)), head Ø ≈ 4 mm. Likely a **removable arming link** (screw bridging two contacts) or the **servo/lid retaining screw** left proud **(guess)**.

### 2.7 Wheels (WH-L, WH-R)
- **Shape**: **black printed (TPU) wheels**, about **Ø 30 mm × 12 mm**, with a **knurled tread** (about 50 axial ribs) and a **flat outer face** with **three cut-outs** forming a stylised symbol (a three-lobed logo).
- **Positions**: centres at **(±45, −26, 15)**, outboard of the pods' cut-back rear ends; outer faces at x ≈ ±51. WH-R fully visible at native (1550–1730, 220–500); WH-L top at (650–790, 55–165).
- **Heights**: tops at z ≈ 30, about **6 mm above** the pod lids, so the robot can drive inverted.

---

## 3. Per-view sections

### 3.1 The photo (front-right)
- Two big white wedges with clear plates in front (left small, right large in perspective), the black centre plate between them bending down at the front, the white lids behind, the right wheel at the right, the left wheel's top behind the left pod, the pin at the top right, blue showing under the right lid.

### 3.2 Top view (plan, synthesised)
- Three strips: left pod (25 × 78 incl. wedge), black plate (30 × 80), right pod (25 × 78); the pods' front wedges reaching y +44, the black ramp to y +38; two wheels (30 × 12) outboard at the rear (x ±45, y −26). Overall width ≈ 102 (see section 12), length ≈ 88.

### 3.3 Front view
- Two white wedge faces (25 wide each) going down to the floor at the sides, the black ramp (30 wide) between them ending 6–8 mm above the floor; the wheels showing at both sides behind, taller than the pods.

### 3.4 Right side view
- The pod: a long low shape with a 31° front slope to the floor, a flat top at z 24, the ribbed outer chamfer, the hole near the middle, the wheel at the rear (Ø 30) sticking up 6 mm; the black plate's ramp visible behind the wedge; the pin sticking up at the rear.

### 3.5 Rear and underside (not photographed)
- Rear: the pods' rear ends, the black plate's pivot region, the wheels. Underside: flat with the wedge toes and wheel contacts (two-wheel + toes stance).

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| PD | pod with wedge and chamfer | 25 × 78 × 22 | 0.31 × 0.98 × 0.28 | white FDM | to a floor/frame (hidden) | 2 |
| LD | lid | 25 × 44 × 2 | 0.31 × 0.55 | white FDM | 1–2 × M2 pan | 2 |
| CP | clear plate | 23 × 40 × 1 | 0.29 × 0.5 | clear PC (+ black edge on L) | 4 × M2 pan | 2 |
| LP | bent plate | 30 × 80 × 3 (bend at 44) | 0.38 × 1.0 | black FDM | pivot (hidden) | 1 |
| SV | micro servo | 23 × 12 × 23 | — | blue | in the right pod | 1 |
| PIN | proud screw | M2 × 12 | — | steel | in the right pod | 1 |
| WH | knurled wheel | Ø 30 × 12 | 0.38 × 0.15 | black TPU | motor shaft | 2 |
| HL | hole | Ø 4 | — | — | — | 1 |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| LD ↔ PD top | screwed | 0 (LD-R raised 2–3) |
| CP ↔ WG | screwed flat | 0 |
| CP toe ↔ floor | touching | 0 |
| LP sides ↔ PD inner faces | side by side | 1–2 |
| LP rear part ↔ PD top plane | flush / just above | 0–1 |
| LP front edge ↔ floor | above | 6–8 |
| LP front edge ↔ WG toes (Y) | behind | 6 |
| LP ↔ PV | pivot | 0 |
| SV ↔ PD-R cavity | in pocket | 0 |
| WH inner face ↔ PD rear notch | near | 2 |
| WH ↔ floor | touching | 0 |
| WH top ↔ LD top | wheel above | +6 |
| PD floor ↔ floor | above | 2 |

---

## 6. Mechanism
1. **Drive**: two rear wheels, differential steer; the wedge toes slide on the floor at the front.
2. **Lifter**: the servo rotates LP about the rear pivot. The ramp's front edge, about 74 mm from the pivot, rises by about 74·sin θ: at 30°, ≈ 37 mm. An opponent driven onto the wedges slides onto the black ramp and is lifted, losing traction.
3. **Inverted**: the wheels stick out 6 mm above the lids, so it drives inverted; the lifter could also self-right.

---

## 7. Assembly order (suggested rebuild)
1. Print the two pods (with wedge, ribbed chamfer, wheel notch, servo pocket in the right pod, motor pockets), the lids, the black plate and the wheels; likely a floor or cross-members join the pods under the black plate **(guess)**.
2. Fit the drive motors in the pods' rear and press on the wheels.
3. Fit the servo in the right pod, output toward the centre; fit the battery, receiver/ESC and arming link.
4. Mount the black plate on its pivot and couple it to the servo.
5. Screw the clear plates onto the wedges (4 screws each); add the black edging on the left plate.
6. Screw on the lids; fit the pin.

---

## 8. Coordinate frame (restated)
- Origin O on the floor under the body centre; +X right, +Y forward, +Z up; mm.
- Pods x ∈ ±[15, 40], y ∈ [−40, +44] (incl. wedge), z ∈ [2, 24]. LP x ∈ [−15, 15], y ∈ [−40, +38]. Wheels (±45, −26, 15), Ø 30.

## 9. Profiles as math
- **Pod side profile (YZ, at |x| = 15…36)**: polygon (−40, 2), (−40, 24), (4, 24), (44, 0), (40, 0)… simplified: top z = 24 for y ∈ [−40, 4]; wedge z = 24 − 0.6·(y − 4) for y ∈ [4, 44] (31°); bottom z = 2 for y ≤ 40.
- **Pod cross-section (XZ, right pod)**: (15, 2), (15, 24), (36, 24), (40, 12), (40, 2). Chamfer slope atan(12/4) = 72°… use (36, 24) → (40, 10): 74°; ribs: ridges every 1.2 mm on this face.
- **Lifter plate (YZ, at rest)**: rear flat from (−40, 25.5) to (4, 25.5); bend arc r 3; ramp line from (4, 25.5) to (38, 8): z = 25.5 − 0.515·(y − 4) (27°). Thickness 3 below the line.
- **Lift rotation** about P = (−36, 22): (y, z) → P + R(θ)·((y, z) − P). Front edge (38, 8) at θ = 20°: (−36 + 74 cos 20° + 14 sin 20°, 22 + 74 sin 20° − 14 cos 20°) = (38.3, 34.2).
- **Wheel**: r(φ) = 14.5 + 0.8·[sin(50φ) > 0]; face cut-outs: three lobes centred at r 7, φ = 90°, 210°, 330°, each a circle r 3.

## 10. Pixel-based measurements
Native 1759 × 1100, ±10 px.
- CP-L: (30–600, 300–740); CP-R: (750–1390, 480–1010).
- LP: front edge (495, 600)–(880, 625); rear edge (1010, 85)–(1350, 150); bend line (640, 365)–(1150, 380).
- LD-L: (600–1000, 60–330); LD-R: (1050–1560, 150–560).
- WH-R (1550–1730, 220–500); WH-L (650–790, 55–165).
- PIN (1560–1575, 140–215). HL (1305, 540).

## 11. Several independent estimates

| Quantity | Method A (kit / rules) | Method B (ratio) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Centre plate width | kit 24 | ≈ 0.38 W | front edge 385 px vs CP-L 330 px at a similar depth → LP ≈ 1.17 × pod plate (23) = 27; rear edge 340 px vs LD-L ≈ 300 px → 1.13 × 25 = 28 | **30** |
| Pod width | kit (44 − 14) = 30 | ≈ 0.31 W | as above → 25 | **25** |
| Body width | kit 80 | 2 × 25 + 30 = 80 | — | **80** (+ wheels → 102) |
| Wedge angle | kit atan(26/44) = 30.6° | — | CP-R face shape vs its width in perspective → 28–34° | **31°** |
| Wheel Ø | kit 26 | ≈ 1.25 × pod height | WH-R 280 px tall at ≈ 9 px/mm (rear depth) → 31 | **30** |
| Body height | kit 24 | — | right pod rear height ≈ 200 px at 9 → 22 | **24 to the lid** |
| Ramp tip height | kit lift plate at z 27 flat | — | LP front edge ≈ 90 px above the CP-L toe line at ≈ 13 px/mm → 7 | **7** |

## 12. Consistency check
1. **Overall width**: 80 + 2 × (2 + 12) − overlap with the pods' cut-back rear (12 each) = **≈ 98–102**. To stay in the cube, wheel centres at x ±43 (outer faces ±49): **98 mm**.
2. **Overall length**: pods y −40 to toes +44 = 84; wheel rear edge −26 − 15 = −41: **85 mm.** Fits.
3. **Lifter plate vs kit**: the kit models LP as a flat plate at z 27; the photo shows a **bent plate** with a ramp. Use the bent profile.
4. **Servo location**: blue part under LD-R. Consistent with a side-mounted servo driving the plate's pivot near the rear (the pin and lid gap are both on the right).

---

## 13. Why the designer did it (per part, mostly adversarial)

- **Twin wedge pods with clear PC faces (WG, CP)**
  - Getting under vs contact: two long, shallow (31°) wedges with **thin polycarbonate edges on the floor** get under opponents across most of the width. The clear PC is **tougher and slicker** than the printed face, so opponents slide up and the printed toe does not chip. The **gap between the pods** is where the lifter ramp sits, so whatever rides up a wedge or into the middle ends up on the lifter.
  - Against spinners: shallow slopes deflect horizontal hits upward; the PC plates spread impacts; four screws per plate make replacement quick.
- **Sloped, ribbed outer sides (RB)**
  - Fight: side attacks meet another slope, not a wall; the ribs may **grip** an opponent being pushed sideways or simply add stiffness and hide layer lines.
- **Black bent lifter plate (LP)**
  - Fight: its ramp front sits **behind and above** the wedge toes so it never digs into the floor; once an opponent is on it, the servo lifts its front, taking its wheels off the ground (it can then be pushed anywhere) or tipping it over. The long pivot arm (≈ 74 mm) gives a big lift.
  - Weak points: a servo gearbox can strip; the plate is printed, so a heavy hit can crack the bend (the chipped front-right corner shows wear).
- **Servo hidden in the right pod**
  - Fight: protected on all sides by printed walls; only reachable by cutting through a pod.
- **Wheels outboard at the rear, taller than the body**
  - Fight: rear-wheel drive keeps the wedges loaded on the floor; tall wheels give invertible driving; the pods' cut-back rear corners partly shield the inner faces.
  - Weak points: outer faces exposed to side spinners.
- **Arming pin at the rear-right corner**
  - Construction: easy to reach and pull, far from the front where fights happen **(guess on function)**.

---

## 14. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position | Confidence |
|---|---|---|---|---|
| Drive motors | 2 × N20 gearmotors | 12 × 10 × 25 | in the pods' rear, shafts at (±35, −26, 15) | medium |
| Lifter servo | blue SG90 / MG90 | 23 × 12 × 23 | right pod, (+27, −10, 13), output toward −X | medium-high |
| Pivot | servo output or a pin through both pods at (y −36, z 22) | — | — | medium |
| Battery | 2S LiPo 180–300 mAh | 40 × 18 × 10 | left pod or under LP | low |
| ESC + receiver | combined board | 30 × 18 × 5 | left pod | low |
| Arming link | screw link | M2 | rear-right corner | low |
| Floor/cross-members | a printed floor joining the pods under LP | 30 × 70 × 2 | z 2–4 | medium |

## 15. What the photo cannot show
- The rear, underside, left outer side, the pivot and the servo linkage.
- What the black edging on CP-L is.
- All mm values ±10–15%.
