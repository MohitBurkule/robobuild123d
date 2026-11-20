# Dragoon: full rebuild description from reference photos

Source photos (all cut out onto white by the AWS wiki; clear polycarbonate edges show a **green halo** from the cut-out, which is not a real colour):
- `robots/dragoon/reference/dragoon.aws72.webp` (1210 × 984 px): AWS 72. Camera at the **front-left**, about 35° down. The forks point to the lower left. The robot's **left** side is nearest (image right). Fitted with the **eccentric steel ring** weapon and **four black printed tines with steel chisel tips**. Black knurled wheels.
- `...aws74.webp` (1127 × 883 px): AWS 74. Camera at the **front, slightly left**, about 35° down. Same ring weapon (tooth up at the top right of the image). Front pods with **flat black ledges** and **one zig-zag steel blade-fork per pod**. White tyres on blue hubs.
- `...aws76.webp` (1485 × 1232 px): AWS 76. Camera at the **front-right**, about 25° down; the forks point to the lower right and the robot's **right** side is nearest (image left). Fitted with a **flat plate disc with two kidney windows and one big triangular tooth**, a black **cheek arm** with a Phillips axle screw, and **two curved steel spring prongs per pod**. White foam tyres on blue hubs, taped clear side plate.

Everything stated as fact is read from those photos; inferences are marked **(guess)**. Sizes are **estimates in mm**, scaled from the AWS antweight rules (150 g, 101.6 mm cube) and the earlier spec draft (body 84 × 108 × 28, wheels r 15 outboard, disc r 40 with one tooth, four 50 mm forks), checked by pixel ratios. Ratios are against **W = width across the two blue halves ≈ 76 mm**.

---

## 0. Coordinate system and naming

- **Origin O** = floor point (z = 0) under the centre of the blue body's footprint (mid-width, mid-length of the blue halves, pods and forks excluded).
- **+X** = robot right, **+Y** = forward (toward the forks), **+Z** = up. mm. Side-profile angles from the floor.
- Orientation in the photos: AWS72 and AWS74 have the front toward the camera, the robot's right on the image left. AWS76 has the front to the lower right, the robot's right on the image left (near).
- Body extents (reconciled §12): x ∈ [−38, +38], y ∈ [−36, +30], z ∈ [3, 27]. Pods to y = +44. Forks to y ≈ +70. Wheels and side plates to x = ±50. Weapon top to z ≈ 75 (AWS76 tooth) or 62 (ring).

| ID | Part |
|---|---|
| BH-L, BH-R | blue body halves (left/right blocks either side of the slot) |
| LID-L, LID-R | blue top lids of the halves (separated by a parting line) |
| RX-B | rear bridge (blue cross-member joining the halves behind the slot) |
| SL | weapon slot (centre gap between halves and pods) |
| CO | cut-outs in the lids (switch hole, wire hole) |
| PD-L, PD-R | black front pods (wedge blocks at the front of each half) |
| LG-L, LG-R | black flat ledges/skirts on the pods (AWS74) |
| TN-1…4 | black printed tines with steel chisel tips (AWS72) |
| ZF-L, ZF-R | zig-zag steel blade-forks (AWS74) |
| SP-1…4 | curved steel spring prongs (AWS76) |
| MH | black weapon motor housing (cylinder, transverse axis) with its leg |
| MC | motor housing end cap (3–4 screws) |
| CK | black cheek arm / outer bearing upright (opposite side of the disc from MH) |
| AX | weapon axle with Phillips axle screw |
| MW | brushless outrunner (copper windings visible in AWS76) |
| RG | eccentric steel ring weapon with one hook tooth (AWS72/74) |
| PDK | plate disc with two kidney windows and a triangular tooth (AWS76) |
| WH-L, WH-R | rear drive wheels |
| SD-L, SD-R | clear polycarbonate side plates / wheel guards |
| S-x | screws: black pan heads on lids, pods, side plates; silver Phillips axle screw |
| WR | wiring: black motor-phase loop (AWS72), orange/red wires in a lid cut-out (AWS76) |
| M-L, M-R, BAT, ESC, WESC, RX | hidden drive motors and electronics |

---

## 1. Overall description in one paragraph

Dragoon is a **compact vertical spinner** with a **bright blue printed body split down the middle**. Two blue blocks (halves), each about 30 mm wide, 66 mm long and 24 mm tall, sit either side of a **16 mm centre slot** and are joined at the rear by a blue bridge. Their tops are flat at the rear and **bevelled down at about 40° toward the front**, where each half ends in a **black printed wedge pod**. A **vertical weapon** spins in the slot on a transverse axle carried high above the body by a **black cylindrical motor housing** on one side (robot left) and a **black cheek arm** on the other (robot right), so the weapon sits in the **front half**, with its lower edge dipping into the slot just behind the pods. Three weapons appear: a **rusty eccentric steel ring** with one hook tooth (AWS72/74), and a **flat dark plate disc with two kidney windows and one huge triangular tooth** (AWS76). The front pods carry interchangeable **forks**: four black printed tines with steel chisel tips (AWS72), a flat black ledge with one zig-zag steel blade per pod (AWS74), or two thin curved steel spring prongs per pod (AWS76). Two drive wheels sit at the **rear corners** outboard of the halves, each behind a **clear polycarbonate side plate**.

---

## 2. Part-by-part description

### 2.1 Body halves (BH-L, BH-R) and lids (LID-L, LID-R)
- **Shape**: each half is a blue printed block, **30 mm wide (X) × 66 mm long (Y) × 24 mm tall (Z)** (z = 3 to 27). Inner faces at x = ±8 (slot 16 mm), outer faces at x = ±38.
- **Top profile**: the rear **40 mm** of the top is **flat** at z = 27; the front **20 mm** is a **bevel** sloping down at about **40°** to z ≈ 12 at the front face (y = +30), where it meets the pod. The bevel is clear in all three photos (it is the large sloping blue face behind each pod).
- **Lid split**: a **horizontal parting line** about **5 mm below the top** runs around each half (AWS72 and AWS76 show a dark seam), i.e. a **5 mm thick removable lid** on each half, covering the flat and bevelled top. The lids are held by **black pan screws** (head Ø 4 mm, M2–M2.5) at the corners: AWS72 shows screws at the rear-left (top of image), rear-right corner, and near the cut-outs.
- **Cut-outs CO**: a small **rectangular hole about 8 × 5 mm** in the robot-left lid near its rear inner corner (AWS72, (870, 290) px: switch or link access), and a **notch about 12 × 6 mm** at the inner rear edge of the right half (AWS76, where **orange/red wires** and a strip of **blue tape** show; the weapon ESC leads or the drive wiring).
- **Colour/material**: **bright cyan-blue PLA** with clear horizontal layer lines on the sides and diagonal top infill lines; small stringing on the bevels.

### 2.2 Rear bridge (RX-B)
- **Shape**: the halves are joined behind the slot by a blue block about **16 mm wide (the slot width) × 20 mm long × 24 mm tall** (y = −36 to −16), flush with the halves' tops, so the slot runs only from y ≈ −16 to the front. AWS72 shows a continuous blue top across the rear at the top of the image; AWS74 shows the slot's rear end as a square step behind the motor housing.
- **Function**: makes the two halves one stiff U-shaped tub and stops the disc's rear edge being exposed.

### 2.3 Weapon slot (SL)
- **Shape**: a rectangular channel, **16 mm wide**, from y ≈ −16 to the front of the pods (y = +44), open at the top and the front, with the floor at z ≈ 3 (the body's bottom skin may continue under it **(guess)**).
- **Contents**: the weapon's lower part. The disc runs **2–4 mm** clear of each slot wall.

### 2.4 Front pods (PD-L, PD-R)
- **Shape**: two black printed blocks, one in front of each half, each **30 mm wide × 14 mm long (Y) × 14 mm tall** at the back, with a **sloped top** continuing the halves' bevel down toward the front. Their front faces are vertical, about 8 mm tall, carrying the fork mounts. In AWS76 each pod is a **triangular-section wedge block** whose sloped top has a **rectangular recess/pocket** (about 10 × 12 mm) with a screw in it.
- **Fastening**: **2–3 black pan screws** through the pod into the blue half (AWS72: screws visible on the front faces at (275, 440), (480, 510), (655, 565), (880, 630) px; AWS74: two screws per pod front plate).
- **Slot**: the 16 mm slot continues between the pods.

### 2.5 Fork sets (three versions)
- **AWS72, tines TN-1…4**: four **black printed flat tines**, two per pod, each **9 mm wide × 3 mm thick × 32 mm long**, running **forward and slightly down** (about 8°) from the pod front face to the floor. Each tine ends in a **silver steel chisel tip** about **9 mm wide × 10 mm long × 2 mm thick**, bevelled to an edge on the floor, set into or glued onto the tine end. Tine centres at about x = −30, −14, +14, +30 (the inner tines flank the slot, the outer tines at the outer edges of the pods).
- **AWS74, ledges LG and zig-zag forks ZF**: each pod carries a **flat black ledge plate** (about **30 mm wide × 24 mm long × 3 mm thick**, with a stepped/layered edge, its front corners **chamfered at 45°** about 8 mm) lying flat on the floor in front of the pod, plus **one steel blade-fork** in its centre (x ≈ ±22). The fork is a **steel strip about 2 mm thick × 4 mm tall**, standing on edge in a slot in the pod's front plate, held by **2 screws**, and bent into a **zig-zag** in side view: from the pod top it runs forward, steps down twice (two "Z" steps of about 4 mm), and ends in a **chisel point** about 8 mm ahead of the ledge's front edge, touching the floor. Its total length is about **40 mm**.
- **AWS76, spring prongs SP-1…4**: each pod carries **two thin curved steel prongs** (spring-steel strip about **3 mm wide × 1 mm thick × 45 mm long**), emerging from slots at the bottom of the pod's front face (x ≈ ±16 and ±30). Each prong **curves forward and down**, concave-up (like a ski tip reversed): it leaves the pod nearly horizontal, then bends down to touch the floor about 35 mm ahead, the last 10 mm running along the floor with a slight **outward sweep** (about 5°).
- **Colour**: black printed parts with white scuffs; steel parts bright silver with scratches.

### 2.6 Weapon motor housing (MH) and end cap (MC)
- **Shape**: a **black printed cylinder**, **Ø 26 mm × 26 mm long**, its axis along **X**, centred at about **x = −16, y = +12, z = 40** (robot left of the disc). The outer end carries an **end cap (MC)**: a disc of the same diameter with **3–4 black screws** (AWS72 shows 4: two at the top, two at the bottom; AWS74 shows 3–4), and a raised **wire boss** from which the **three black motor phase wires** loop up and over toward the rear (AWS72, a loop rising about 15 mm above the housing).
- **Leg**: below the cylinder a **black printed leg** (about **14 mm wide × 12 mm deep**) drops vertically into the slot area / onto the left pod's inner rear corner (AWS74: the leg runs from the cylinder down to the pod at (650–720, 330–540) px). It is the housing's mounting post, screwed into the body or pod **(guess)**.
- **Content**: the **outrunner MW** sits inside the housing's inner end, with its bell spinning **with the weapon** (the disc is bolted to the bell's face) **(guess, medium)**.
- **Surface**: textured black (fuzzy-skin or matt), with a green tint in the photos.

### 2.7 Cheek arm (CK) and axle (AX)
- **Shape (AWS76)**: a black printed **upright bar**, **10 mm wide (Y) × 6 mm thick (X) × 40 mm tall**, with a **rounded top** (semicircle r = 5) around the axle and a **flared base** joining the right pod's inner rear corner. A **silver Phillips pan screw** (head Ø 6 mm, M3) is at the axle centre (AWS76 at (690, 470) px).
- **Position**: at x ≈ +12 (robot right of the disc), from z ≈ 15 (pod top) to z ≈ 50.
- **Axle AX**: a steel bolt **M3–M4**, along X, from the cheek through the disc hub into the motor shaft or housing, at **(y ≈ +12, z ≈ 42)**. In AWS72/74 (ring weapon) the cheek is hidden behind the disc; the ring's centre is at a similar height.

### 2.8 Weapon A: eccentric ring (RG), AWS72/74
- **Shape**: a **flat steel ring** (rust-brown/copper oxide colour with bright scuffs on its edge), **outer Ø 52 mm, inner Ø 40 mm** (ring band 6 mm wide), **3 mm thick**, standing vertically in the slot.
- **Eccentricity**: the ring is **not centred** on the axle: it is attached to the motor bell / a hub plate at one side, so the axle lies about **8–10 mm off the ring's centre**, inside the ring's hole near one side. This gives a **large hollow** with the axle hub showing through (AWS72: the black hub with a copper ring is visible inside the ring).
- **Tooth**: **one hook tooth** on the outer rim (AWS74: at the top right, a **rectangular/hooked tab** about 10 mm long × 6 mm tall projecting outward), with its leading face radial.
- **Position**: centred in the slot (x ≈ 0), the lowest point of the ring at about z = 8 (just above the slot floor), the top at about z = 62.
- **Mounting**: a flat inner flange or spokes joining the ring to the bell are hidden by the housing **(guess)**.

### 2.9 Weapon B: plate disc (PDK), AWS76
- **Shape**: a **flat dark steel (or titanium) plate**, **3 mm thick**, outer **Ø 58 mm**. Inside it, **two large kidney-shaped windows** (each about 22 × 14 mm) leave an **S-shaped central spoke** around a hub of about Ø 18 mm. The rim band is about 5 mm wide.
- **Tooth**: **one large triangular tooth** projecting about **26 mm** beyond the rim at one point, with a **triangular lightening window** (about 16 × 12 mm) inside it. Its **leading edge is a straight line** running radially out to a sharp tip; its trailing edge is a concave curve back to the rim. In AWS76 the tooth points **up and back**.
- **Counterweight**: none visible; the single tooth is balanced by the material distribution of the S-spoke (heavier on the opposite side) **(guess)**.
- **Position**: in the slot at x ≈ 0, axle at (y +12, z 42). The disc's lowest point is at z ≈ 13, and the tooth tip sweeps to a radius of about 55 mm from the axle, i.e. up to z ≈ 97 at the top and down to... it would hit the floor at the bottom (42 − 55 < 0) unless the tooth only passes through the slot. **See §13 for reconciliation (the tooth radius is about 44 mm).**
- **Visible motor**: through the window near the hub, the **outrunner's copper windings and stator** are visible (AWS76), so the disc is bolted directly to the outrunner's bell on the housing side.

### 2.10 Rear wheels (WH-L, WH-R)
- **Shape**: **Ø 30 mm × 10 mm wide**.
  - AWS72: **black knurled/gear-tooth tyres** (about 36 teeth, 1.5 mm tall) on **black hubs with large round lightening holes** (3–4 holes about Ø 6).
  - AWS74/76: **white/translucent foam or soft TPU tyres** on **blue hubs with 3 round holes** (Ø about 5 mm) and a central boss.
- **Positions**: centres at **x = ±43, y = −22, z = 15**; tops at z = 30 (3 mm above the lids), bottoms at z = 0.
- **Drive**: each on an N20-class gearmotor in the rear of a half **(guess)**.

### 2.11 Side plates (SD-L, SD-R)
- **Shape**: flat **clear polycarbonate** plates, about **1.5 mm thick**, about **60 mm long × 26 mm tall**, outboard of each half's rear two-thirds, covering the wheels' outer faces. The front end is **cut at an angle** (about 45°, AWS72 left side: a sloping front edge) and the top edge is straight.
- **Fasteners**: **2–4 black pan screws** into the halves' outer faces (AWS74 right: 2–3 screws along the bottom and front; AWS76 right: 3 screws, one high near the front, two low).
- **Tape**: edges **wrapped with clear tape** (AWS74, AWS76), some layers lifting; AWS76 also shows a strip of **blue tape** on top near the wheel.
- **Gap**: the plate stands **1–2 mm** off the tyre's outer face, on spacers or via the screw bosses **(guess)**.

### 2.12 Wiring (WR)
- AWS72: **three black phase wires** from the motor end cap forming a loop over the housing top toward the rear (into the body through the slot's rear end).
- AWS76: **orange/red wires** visible in the notch at the right half's rear inner edge, with **blue tape** over it.

---

## 3. Per-view descriptions

### 3.1 Top view (plan)
- Two blue rectangles (30 × 66 each) with a 16 mm gap between their front 46 mm, joined by a bridge at the rear. Each has a darker front bevel strip (20 mm). In front, two black pods (30 × 14). The forks project 25–30 mm further (four tines / two zig-zags with ledges / four curved prongs).
- In the gap, the weapon (3 mm thick line, 52–58 mm long in plan) at y ≈ −14 to +40 (ring) or longer with the tooth. The motor housing (26 × 26 square in plan) sits over the left half's inner front at x −29 to −3. The cheek (6 × 10) sits at x +12.
- At the rear corners, the two wheels (30 × 10) and the clear plates (1.5 × 60) outboard.
- Overall: about **100 mm wide × 106 mm long** with tines, which fits a 101.6 cube only diagonally; probably the true width is a little less (§13).

### 3.2 Front view (AWS74 is close)
- Bottom: the fork tips/ledges. Above them, the two black pod front faces with screws, separated by the slot. Behind them, the two blue bevels rising to the flat lids.
- In the middle, the weapon's edge (3 mm wide) running up from the slot to above the body; the motor housing (Ø 26 circle face-on is not visible; it is seen side-on as a 26 × 26 square) on the robot's left of the disc at z 27–53, with its leg down to the pod; the cheek on the right.
- At the sides: clear plates and the wheel tops just showing above the lids.

### 3.3 Right side view (AWS76 is close)
- A blue rectangle (66 long × 24 tall) with the front bevel; the clear side plate covering the rear two-thirds and the wheel behind it (top just above the lid). In front, the black pod (triangular profile) with the two curved prongs sweeping down to the floor.
- Above: the cheek arm with its round top and axle screw, the plate disc behind it with the triangular tooth up, the motor housing behind.

### 3.4 Rear view (inferred)
- The blue rear faces of the halves and bridge (76 × 24), the wheels at the corners, the weapon top and the motor wire loop above. Possibly the switch hole on top at the rear **(guess)**.

### 3.5 Isometric (front-left, as AWS72)
- A blue split block with black "teeth" at the front, a round black drum on top beside a rusty hoop, and black knobbly wheels at the back.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| BH | block with front bevel | 30 × 66 × 24 | 0.39 × 0.87 × 0.32 | blue PLA | bridge | 2 |
| LID | lid | 30 × 66 × 5 | — | blue PLA | 2–4 × M2 black | 2 |
| RX-B | bridge | 16 × 20 × 24 | 0.21 | blue PLA | integral | 1 |
| PD | wedge block | 30 × 14 × 14 | 0.39 × 0.18 × 0.18 | black PLA | 2–3 × M2 | 2 |
| TN | tine + steel tip | 9 × 32 × 3 (+10 tip) | 0.12 × 0.42 | black PLA + steel | integral / glued tip | 4 (AWS72) |
| LG | ledge plate | 30 × 24 × 3 | 0.39 × 0.32 | black PLA | integral with PD | 2 (AWS74) |
| ZF | zig-zag strip | 40 × 4 × 2 | 0.53 | steel | 2 screws | 2 (AWS74) |
| SP | curved prong | 45 × 3 × 1 | 0.59 | spring steel | slot in PD | 4 (AWS76) |
| MH | cylinder + leg | Ø 26 × 26 (+ leg 14 × 12 × 15) | 0.34 | black PLA | screws to body | 1 |
| MC | end cap | Ø 26 × 3 | — | black PLA | 3–4 × M2 | 1 |
| CK | upright arm | 10 × 6 × 40 | 0.13 × 0.08 × 0.53 | black PLA | screws into PD-R | 1 |
| AX | bolt | M3–M4 × 35 | — | steel | nut / thread in motor | 1 |
| MW | outrunner | Ø 22 × 12 | 0.29 | — | in MH | 1 |
| RG | eccentric ring | Ø 52 / Ø 40 × 3, 1 tooth | 0.68 | rusty steel | bolted to bell | 1 (AWS72/74) |
| PDK | plate disc | Ø 58 × 3 + 26 tooth | 0.76 | dark steel / Ti | bolted to bell | 1 (AWS76) |
| WH | wheel | Ø 30 × 10 | 0.39 × 0.13 | black knurled / white foam on blue | motor shaft | 2 |
| SD | flat plate | 60 × 26 × 1.5 | 0.79 × 0.34 | clear PC + tape | 2–4 × M2 | 2 |

---

## 5. Contact / gap matrix (est. mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| BH bottom ↔ floor | clearance | 3 |
| WH bottom ↔ floor | contact | 0 |
| TN/ZF/SP tips ↔ floor | contact | 0 |
| LG bottom ↔ floor | resting | 0–1 |
| PD ↔ BH front face | screwed | 0 |
| BH-L inner ↔ BH-R inner | slot | 16 |
| weapon faces ↔ slot walls | clearance | 2–4 each side (weapon 3 thick, offset by 2–3) |
| weapon lowest point ↔ slot floor | clearance | 5–10 |
| weapon ↔ MH inner face | bolted to bell / 1 mm to the housing | 0–1 |
| weapon ↔ CK inner face | clearance | 2–3 |
| MH leg ↔ PD-L / BH-L | screwed | 0 |
| CK base ↔ PD-R | screwed | 0 |
| weapon rim ↔ PD front edges | ring/disc behind the pod fronts | 3–8 |
| WH outer face ↔ SD | clearance | 1–2 |
| WH inner face ↔ BH outer face | clearance | 2 |
| WH top ↔ LID top | wheel above | +3 |
| SD ↔ BH outer face | screwed | 0 |
| LID ↔ BH | screwed | 0 |

---

## 6. Mechanism

1. **Drive**: 2WD rear wheels (skid steer); the pods and forks slide on the floor at the front.
2. **Weapon**: the outrunner in MH drives the weapon directly (bolted to the bell). The disc spins in the vertical YZ plane, its front edge moving **upward** (so hits throw opponents up) **(guess)**. The axle is held at both ends (motor side and cheek), a "dead axle" or motor shaft supported by the cheek.
   - Ring energy: m ≈ 7.85 g/cm³ · π(2.6² − 2.0²)·0.3 ≈ 6.5 g + tooth ≈ 8 g; I ≈ m·r̄² ≈ 0.008·0.023² ≈ 4.2 × 10⁻⁶ kg·m². At 20,000 rpm (2094 rad/s) E ≈ ½·I·ω² ≈ 9 J.
   - Plate disc: m ≈ 7.85·π·2.9²·0.3 ≈ 62 g minus windows (≈ 40%) ≈ 37 g + tooth 6 g. Too heavy for a 150 g robot with all the rest; it is probably **titanium (4.5 g/cm³) ≈ 25 g** or thinner steel **(guess)**.
3. **Forks**: passive; they get under opponents and present them to the weapon.

---

## 7. Assembly order (suggested rebuild)

1. Print the blue tub (two halves + rear bridge) with motor pockets, and the two blue lids.
2. Install the drive gearmotors in the rear of each half, shafts out at (±38, −22, 15); press on the wheels.
3. Install battery, drive ESC, weapon ESC, receiver and switch in the halves; route the weapon phase wires to the slot's rear end.
4. Screw the black pods to the halves' fronts; fit the chosen fork set (tines printed with the pods + steel tips glued; or ledges + zig-zag forks with 2 screws each; or spring prongs pushed into slots).
5. Fit the outrunner into MH, bolt the weapon (ring or plate disc) to its bell, and screw MH's leg down to the left pod/half.
6. Fit the cheek arm CK on the right pod and pass the axle bolt through the cheek into the motor/hub.
7. Screw on the lids, then the clear side plates (with tape on the edges).

---

## 8. Hidden / uncertain list
- How the ring is attached to the motor (flange vs spokes).
- Whether the axle is a dead shaft or the motor shaft.
- The cheek arm in AWS72/74 (hidden by the ring).
- Drive motors, electronics layout, underside.
- Weapon material/thickness (steel vs titanium for AWS76).
- All sizes ±15%.

---

## 9. Coordinate frame (restated)
- Origin under the blue body's centre; +X right, +Y forward, +Z up; mm.
- Halves: x ∈ [−38, −8] and [+8, +38], y ∈ [−36, +30], z ∈ [3, 27]. Bridge y ∈ [−36, −16]. Pods y ∈ [+30, +44]. Axle (y +12, z 42). Wheels (±43, −22, 15). Fork tips y ≈ +70.

## 10. Profiles as math

**10.1 Body half side profile (YZ).** Bottom z = 3, y ∈ [−36, +30]. Rear face y = −36, z ∈ [3, 27]. Top z = 27 for y ∈ [−36, +10]. Bevel from (+10, 27) to (+30, 12): z = 27 − 0.75·(y − 10) (36.9°). Front face y = +30 from z = 12 to 3. Lid split plane z = 22.

**10.2 Pod side profile (YZ, AWS76).** Triangle-ish: (y 30, z 3), (30, 14), (44, 6), (44, 3). The sloped top z = 14 − 0.571·(y − 30) (29.7°). Recess pocket on top 10 × 12 × 3.

**10.3 Tine (AWS72).** Rectangle in plan 9 wide; side profile from (y 44, z 6) to (70, 0): z = 6 − 0.23·(y − 44); 3 mm thick above that line. Steel tip occupies y ∈ [60, 70], bevel from 2 mm thick to 0 over the last 4 mm.

**10.4 Zig-zag fork (AWS74, side profile, x = ±22).** Polyline (y 32, z 14) → (40, 14) → (42, 10) → (48, 10) → (50, 6) → (58, 6) → tip (72, 0). Strip 4 mm tall (below the polyline), 2 mm thick in X.

**10.5 Spring prong (AWS76, side profile).** A curve from P0 = (y 44, z 4) with horizontal tangent to P2 = (80, 0) with a tangent 15° below horizontal: quadratic Bézier with control point P1 = (65, 4). Plan: x(t) = x0 ± 3t² (outward sweep). Section 3 × 1 mm.

**10.6 Eccentric ring (AWS72/74, in the YZ plane, axle at A = (12, 42)).** Ring centre C = A + (−6, +6) (offset 8.5 mm). Outer circle r = 26 about C; inner circle r = 20 about C. Tooth: a rectangle 10 × 6 attached to the outer circle at angle 30° (measured from +Y), leading face radial.

**10.7 Plate disc (AWS76, about the axle A).** Outer circle r = 29. Windows: two kidneys, each the region between r = 11 and r = 24, spanning angles [20°, 160°] and [200°, 340°], with the boundary between them an S-curve r(φ) through the hub. Tooth: triangle with vertices on the rim at φ = 60° and φ = 100° and the tip at r = 44, φ = 75°; the trailing edge replaced by a concave arc. Inner triangular window: the tooth triangle shrunk by 4 mm (offset inward).

**10.8 Motor housing.** Cylinder r = 13 along X from x = −29 to −3, centred (y 12, z 40). Leg: box x ∈ [−23, −9], y ∈ [6, 18], z ∈ [14, 30].

## 11. Pixel-based measurements

**AWS72 (1210 × 984):**
- Front edge of pods: from (200, 370) to (1000, 620). Tines: tips at (70–180, 545–630), (245–355, 620–700), (575–680, 760–830), (800–910, 815–890).
- Ring: x 410–660, y 110–590 (≈ 480 px tall). Motor housing: x 515–835, y 250–550. End cap screws at (785, 355), (820, 355), (745, 455), (770, 460).
- Wheels: far (robot right) x 450–580, y 30–135; near (robot left) x 1050–1170, y 180–330.
- Clear plates: left of image (360–445, 120–330), right (1000–1170, 280–610).

**AWS74 (1127 × 883):**
- Pods: left x 60–390, y 345–680; right x 440–865, y 515–795. Zig-zag forks: tips at (75, 665) and (460, 845).
- Ring: x 390–690, y 40–470 (430 px). Motor housing: x 495–780, y 140–420. Leg: (640–700, 330–540).
- Right clear plate: x 860–1080, y 270–690.

**AWS76 (1485 × 1232):**
- Plate disc: x 595–1010 (rim), y 290–790; tooth tip at (615, 70). Cheek: x 665–780, y 365–810; axle screw (690, 470).
- Near pod: x 510–950, y 830–1090. Far pod: x 860–1160, y 690–900.
- Prong tips: (1060, 1150), (850, 1010)?, (1420, 870), (1220, 760).
- Right wheel: x 60–260, y 640–860. Clear plate: x 60–480, y 620–1000.
- Body bevel: (500–870, 600–820).

## 12. Several independent estimates of key sizes

| Quantity | Method A (spec/rules) | Method B (ratios) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Body width (halves) | 84 (spec) | ≤ 101.6 − 2 × (10 wheel + 2 gap + 1.5 plate) ≈ 74 | AWS74: halves span 60–960 px incl. ledges ≈ 900 px; ring 430 px = 55 mm → 7.8 px/mm → 115?? (ledges nearer camera) | **76** |
| Body length | 108 (spec) | cube 101.6 − forks 26 − pods 14 = 62 | AWS76: half side 66 mm vs wheel Ø 30 (200 px) → 6.7 px/mm; side 440 px → 66 | **66** |
| Body height | 28 (spec) | 0.32 W = 24 | AWS76: side 160 px / 6.7 = 24 | **24** |
| Wheel Ø | 30 (r 15) | 0.39 W | AWS76: 200 px / 6.7 = 30 | **30** |
| Ring outer Ø | 80 (spec disc r 40) | 0.68 W = 52 | AWS74: 430 px vs housing 285 px (Ø 26) → 39?? ; AWS72: 480 vs 320 → 39 | **52** (see §13) |
| Plate disc Ø | 80 (spec) | 0.76 W | AWS76: 415 px vs cheek 40 mm (445 px) → 37?? ; vs wheel 200 px = 30 → 62 | **58** |
| Housing Ø | — | 0.34 W | AWS72: 300 px vs ring 480 → 0.62 of ring | **26** |
| Fork length (tines) | 50 (spec) | 0.42 W = 32 | AWS72: 260 px along the tine / 8 px/mm → 32 | **32 + pod** |

## 13. Consistency check: conflicts and reconciliation
1. **Spec vs cube**: the spec's 108 mm body + 50 mm forks is far too long. Photos show the forks about half the body length. **Reconciled: body 66 + pods 14 + forks 26 = 106** (the forks may be angled or the cube check measured with forks folded).
2. **Weapon diameter**: the spec's r 40 (Ø 80) contradicts the photos: the ring is clearly smaller than the body length and only about twice the housing diameter. Ratios to the housing give 39–45; ratios to the body give 52–55. The housing is probably larger than Ø 26 if it hides a 28 mm motor. **Reconciled: housing Ø 28, ring Ø 52/40, plate disc Ø 58.**
3. **Plate disc tooth reach**: with the axle at z = 42 and a tooth tip at r = 44, the tip sweeps down to z = −2, i.e. below the floor. The slot floor is open at the front, so the tooth would strike the floor. **Reconciled: axle at z = 46 for the AWS76 version** (the cheek arm is tall: 40 mm from the pod top) and the tooth tip radius 44, sweeping to z = 2 at the bottom, just above the floor, which is what a vertical spinner wants (hits at floor level).
4. **Ring axle offset**: the ring's hole shows the hub to one side in both AWS72 and AWS74; the ring centre is about 8 mm off the axle. This makes the weapon **eccentric**: the off-centre mass is the "tooth", and the hook tab adds bite. Consistent with a deliberately unbalanced "eccentric beater" design.
5. **Motor housing side**: in all photos the housing is on the robot's **left** of the weapon and the cheek on the right.
6. **Wheel visibility**: wheel tops at 30 vs lids at 27 means only 3 mm above; with the weapon sticking 35+ mm above, the robot **cannot run inverted** with the weapon working; consistent with no invertible design features.

---

## 14. Why the designer did it (per part, adversarial first)

- **Split blue body with a centre slot**
  - Fight: the slot lets the weapon sit **low and central**, so its contact point is near the floor where opponents' wedges and front edges are. The two halves on either side act as a **guard**: an opponent can only meet the weapon in the front opening, not from the sides. The front bevels slope down so that opponents climbing the forks are led straight into the weapon's arc.
  - Threats: horizontal spinners hit the square outer faces; the halves are thick (30 mm), so a single hit cracks a corner but the tub remains whole. A wedge could get under the 3 mm ground clearance at the rear; the forks at the front prevent that from the front.
  - Construction: two identical halves plus a bridge print without supports; the lids give access to each side.
- **Black front pods (replaceable)**
  - Fight: the pods take the **reaction of every weapon hit** (the opponent is thrown up and back onto them) and the floor impacts; they are a different colour because they are the **wear parts**, printed separately so they can be swapped with 2–3 screws.
  - Fork mounts: having fork mounts on the pods lets the builder choose forks per opponent.
- **Fork sets**
  - Fight, general: **forks beat wedges** for getting under, because thin tips find gaps under opponents' wedge edges. They lift the opponent's front so the weapon hits its underside or front edge.
  - **Tines with steel tips (AWS72)**: four points spread across the width → whatever angle the opponent comes from, one tine finds a gap. Steel tips wear slowly and stay sharp.
  - **Zig-zag steel forks + ledges (AWS74)**: the ledge is a broad low wedge covering the front; the zig-zag fork in its middle is a thin steel point that gets under first and its steps **catch and hold** an opponent's edge (barbs), stopping them sliding off before the weapon hits.
  - **Curved spring prongs (AWS76)**: spring steel flexes and returns, so it survives hits that would snap printed tines; the curve keeps the tips on the floor even when the robot pitches (it acts like a leaf spring). Narrow strips also give a horizontal spinner almost nothing to hit.
- **Tall weapon yoke (housing + cheek)**
  - Fight: the axle high above the body gives a **large weapon diameter** for the robot's size while keeping the body low. The **cheek arm** supports the axle on the second side so a hit does not bend the motor shaft; without it, the outrunner's bearings would take the entire impact.
  - Threats: the housing and cheek stand tall and can be struck by an opponent's vertical spinner from above; the housing is a thick printed cylinder, and the motor is protected inside it.
  - Construction: the motor housing hides the outrunner's can (it does not spin exposed); the phase wires leave from its end cap so they cannot be cut by the weapon.
- **Eccentric ring weapon (AWS72/74)**
  - Fight: an off-centre ring concentrates mass on one side, giving one heavy **bite per revolution** (a "single-tooth" effect) with a light total weight. The hook tooth catches on opponents' edges. The ring's hollow saves weight and lets the axle sit low while the rim still reaches the floor.
  - Survival: unbalanced weapons vibrate the robot; the stiff U-tub and the two-sided axle support resist this.
- **Plate disc with a big tooth (AWS76)**
  - Fight: a large tooth gives **more bite** (more time between impacts for the tooth to penetrate before the opponent bounces away). The windows reduce weight while keeping rim mass; the triangular window in the tooth lightens it so the disc's balance is closer to centre.
  - The tooth's long straight leading edge takes the impact in compression; the curved trailing edge reduces stress concentration at the root.
- **Rear wheels with clear side plates**
  - Fight: wheels at the very rear corners keep them away from the weapon and the opponent; the clear plates protect the tyres' outer faces from horizontal spinners and stop the tyres rubbing on the wall. Polycarbonate flexes without cracking; the tape stops the edges splitting.
  - Construction: tyres change with events (black knurled for grip vs white foam for cushioning/grip on dusty floors).
- **Lid cut-outs**
  - Rules/maintenance: the small rectangular hole is the switch/link access; the notch passes wires from the body to the weapon housing.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Drive motors | 2 × N20 gearmotors, 6 V, 500–1000 rpm | 12 × 10 × 25 | in the rear of each half, x ±24, y −22, z 15 | medium |
| Weapon motor | 2205–2208 outrunner, 2000–2600 kV | Ø 28 × 14 | inside MH, x −12, y 12, z 42 | medium |
| Weapon ESC | 20–30 A BLHeli ESC | 30 × 14 × 6 | left half, x −23, y −5, z 12 | medium |
| Drive ESC | dual brushed micro ESC | 22 × 15 × 5 | right half, x +23, y −5, z 10 | medium |
| Battery | 3S 300 mAh or 2S 450 mAh LiPo | 45 × 17 × 13 | split across the bridge or in the right half, along Y | low |
| Receiver | small 2.4 GHz | 20 × 12 × 5 | right half, rear, x +23, y −28, z 10 | low |
| Switch | link/slide switch under the rectangular cut-out | 10 × 5 × 5 | left half rear, x −20, y −22, z 22 | medium |
| Axle bearing | small flanged bearing in the cheek top (MR63 or 683) | Ø 6 or 7 × 2.5 | at the cheek's round top | low |
| Weapon hub adapter | printed or aluminium flange bolting the ring to the bell | Ø 22 × 3 | on the bell face | medium |
| Wiring | battery → switch → both ESCs; weapon ESC phase leads forward through the slot's rear end and up into MH's end cap (the black loop); drive leads to the rear motors | — | — | medium |
