# Thwack Attack: full rebuild description from reference photos

Source photos (cut out by the AWS wiki; the green tint on metal edges is a cut-out halo):
- `robots/thwack_attack/reference/thwack_attack.aws74.webp`: 1696 × 1428 px. Front-right three-quarter, about 35° down. Forks point to the lower right, and the hammer head stands up at the upper left.
- `thwack_attack.aws76.webp`: 2033 × 1177 px. Front-left three-quarter, low (about 20°). Forks point left, head at the upper right.
- `thwack_attack.aws77.webp`: 1697 × 1306 px. Front-right three-quarter, about 35°. Forks point to the lower left, head at the upper right.

Facts come from the photos; inferences are marked **(guess)**. Sizes are estimated against the AWS 150 g / 4 in (101.6 mm) cube limit. **W = body width over the orange side plates ≈ 76 mm.**

---

## 0. Coordinate frame
- **Origin O** = the floor point under the centre of the body (midway between the side-plate outer faces, midway between the side-plate front and rear ends).
- **+X** = robot right, **+Y** = forward (toward the forks), **+Z** = up. Units are mm. Side-profile angles are measured from +Y in the YZ plane.
- Body envelope: x ∈ [−38, +38], y ∈ [−38, +38], z ∈ [0, 24] (top plates at z ≈ 24).

## 1. Part IDs

| ID | Part |
|---|---|
| FRM | blue/purple printed inner frame (tub) |
| TP-L / TP-R | salmon-orange top plates |
| SPL-L / SPL-R | orange-red stadium side plates (wheel guards) |
| SO | purple standoffs / axle bosses between the side plates and the frame |
| WH-FL/RL/FR/RR | wheels (purple hub, lilac knurled tyre) |
| BLT-L / BLT-R | black rubber belt / O-ring on each side |
| GB | blue gearbox tower (hammer drive) |
| GBC | second (right) gearbox cheek |
| GR | black spur gear / gear sector inside GB |
| AX | hammer pivot axle (silver screw at the GB centre) |
| ARM | black hammer arm |
| HD | hammer head hub (black round boss with screw rosette) |
| BL | hammer blade plates (two, sickle/hook) |
| WP | aluminium front wedge plate |
| FK-L / FK-R | steel forks |
| SW | ON/OFF slide switch plus label |
| WR | black wire loop (motor lead) on top |
| S-* | screws |

## 2. One-paragraph overview
Thwack Attack is a **low, four-wheel, belt-linked box** with a **steep aluminium front plate** and **two long barbed steel forks** at floor level. Its weapon is an **overhead hammer/axe**. A **blue printed gearbox tower** at the front-left of the top centre holds a transverse pivot. From it a **black arm** about 90 mm long lies **back along a channel** between two flat **salmon top plates** and overhangs the rear. On the arm's end is a **round black hub** clamped between **two steel sickle-shaped blades**. In use, the arm swings up and over to slam the axe tip down **in front of the robot**, over the forks. Large **orange-red stadium-shaped side plates** cover the wheels on both sides.

---

## 3. Part-by-part

### 3.1 Inner frame FRM
- **Shape**: a rectangular tub about **62 mm wide (between the wheels' inner faces) × 70 mm long × 20 mm tall**. Only parts of it are visible: the front face behind the wedge plate, small areas between the wheels, the floor under the arm, and the area around the gearbox tower.
- **Colour**: **royal blue** PLA, with **purple** parts (the wheel hubs and SO) printed in purple.
- **Features**: front mounting face for WP (two vertical rows of screw bosses); axle bosses for the four wheels at z ≈ 11; a central channel about 14 mm wide under the arm; and the base of GB, which may be integral with FRM.

### 3.2 Top plates TP-L, TP-R
- **Shape**: flat rectangles, **2.5 mm thick**.
  - **TP-L** (robot left; seen at the lower-left in AWS74 and the right in AWS76): about **30 mm wide × 62 mm long**. Its front-inner corner is cut out where GB stands (about 14 × 22 mm), and it has a **raised rectangular tab** (about 14 × 10 × 3 mm) at its inner side just behind GB (AWS74).
  - **TP-R**: about **30 mm wide × 52 mm long**, with a **switch slot** of about **7 × 3.5 mm**.
- **Colour**: matt **salmon / light orange** with a fine print texture. This is lighter than the side plates.
- **Fasteners**: each has **4 silver Phillips pan screws**, head Ø about 3.5 mm (M2), about 4 mm in from each corner. AWS77 shows TP-R with screws at the rear-left, rear-right, front-right and front-left; TP-L likewise.
- **Position**: both at z = 21.5–24. TP-L spans x ∈ [−32, −4] and TP-R spans x ∈ [+4, +32], leaving a **central channel about 8 mm wide** (wider at the front, where GB sits in TP-L's notch).
- **Label**: on TP-R, a **white paper label "ON OFF"**, about 14 × 7 mm, printed in black text, next to the slot (rear-right in AWS74, front-right in AWS77, which shows "OFF" / "ON" rotated 90°).

### 3.3 Side plates SPL-L, SPL-R (wheel guards)
- **Shape**: a **stadium** (a rectangle with semicircular ends): overall **L = 76 mm, H = 26 mm, thickness 3 mm**, end radius 13 mm. Math: the outline is the union of rectangle y ∈ [−25, +25], z ∈ [0, 26] and circles of centre (±25, 13), r = 13 (in the plate's YZ frame).
- **Colour**: **bright orange-red** (more saturated than the top plates).
- **Holes/screws**: **2 silver Phillips pan screws** at mid-height (z ≈ 13), at y ≈ −10 and y ≈ +14 (AWS76 left plate at x px 1290 and 1520). There is also a small blind hole at y ≈ +2. The screws thread into the SO standoffs. The top inner edge has a **raised rim lip** where the belt runs (AWS74/77 show a black belt line along the plate's top inside edge).
- **Position**: outer faces at x = ±38. The inner faces at x = ±35 sit **about 1 mm outside the wheel outer faces**. The bottom of the plate is at z ≈ 0.5, practically at the floor; the plate's lowest arc is **level with the wheel bottoms** (wheels Ø 22 centred at z 11, so the bottoms are at 0). The wheels are **almost completely hidden from the side**; only their tread shows at the ends and top (AWS76).
- **Contact**: the plates touch only the SO standoffs (0 gap) and are about 1 mm from the wheel faces.

### 3.4 Standoffs SO
- **Shape**: **purple cylinders**, about **Ø 6 mm × 10 mm long** (along X), between the frame side and the side plate, at the screw positions (y ≈ −10, +14; z ≈ 13). In AWS76 they are visible between the wheels as purple stubs, and AWS77 shows **orange/purple pegs** between the wheels.
- **Function**: they carry the side plates and act as the outer axle supports or belt idlers **(guess)**.

### 3.5 Wheels WH
- **Shape**: **Ø 22 mm × 9 mm**. A **purple hub disc** (about Ø 18) with a **lilac/grey translucent knurled TPU tyre** (about 2 mm thick, about 40 fine teeth). Math: r(φ) = 10 + 1.0·[sin(40φ) > 0]. AWS74 shows **darker grey tyres on black hubs** (a different tyre set).
- **Positions** (centres): (±29, +24, 11) front and (±29, −24, 11) rear. Wheelbase 48 mm, tyre gap 26 mm fore-aft.
- **Height**: the tops reach z = 22, i.e. 2 mm below the top plates. **The robot is not fully invertible** on wheels alone; inverted, it would rest on the plates or the arm **(guess)**. The side plates (26 tall) would however let it drive inverted if the wheels touch the floor through the plate profile: they do not. **(uncertain)**
- **Belts BLT**: a **black rubber band** (about Ø 1.5 mm cord) runs **around the top of the front and rear wheel** on each side (an O-ring belt), so the front and rear wheels on a side turn together (2 motors, 4 driven wheels). Visible in all three photos as a black line along the top inner side of each side plate.

### 3.6 Gearbox tower GB / GBC / gear GR
- **Shape**: a **blue printed housing**. Side profile: a **"D" / tombstone**, a rectangle 28 mm (Y) × 14 mm (Z) topped by a semicircle of r = 14 centred at (y +12, z 38). Overall it stands from z = 24 (plate top) to z = 52. Thickness (X) is about **12 mm**. It sits at **x ∈ [−14, −2]**, y ∈ [−2, +26].
- **Slot**: the rounded top has a **slot about 6 mm wide** along Y, exposing **black spur gear teeth GR** (about 12 teeth visible, module about 1, pitch Ø about 26 mm). The gear is coaxial with the pivot AX.
- **Second cheek GBC**: a smaller blue upright on the **right side of the arm root** (x ≈ +2 to +8), which also carries AX. In AWS76 the blue block on the right of the arm root has **blue ribs** and a **blue curved fairing**.
- **Pivot AX**: a **silver Phillips/pan screw** (head Ø 3.5) at the centre of GB's outer face, at (x −14, y +12, z 38). The axle runs along X through GB, the arm root and GBC.
- **Under the tower**: a **blue lower housing** (about 26 × 20 × 20) extends down into the frame at the front-left, holding the **weapon motor** (guess: N20 or 370-size gearmotor) and the reduction gears.
- **Wire WR**: a **black wire loop** (about Ø 1 mm) comes out of GB's top rear, arcs over (up to about z 60), and goes into a hole in TP-L/TP-R (AWS77). This is the weapon motor lead or a servo lead.

### 3.7 Hammer arm ARM
- **Shape**: a **black printed bar**, about **6 mm wide × 7 mm tall**, with a rough or scuffed top edge (it shows chew marks). Its **length from AX to the head hub centre is about 95 mm**.
- **Root**: at AX (y +12, z 38), with a rounded end (r about 7) around the axle, sitting **between GB and GBC** (gaps of about 0.5 mm).
- **Rest pose** (all photos): the arm points **rearward and slightly up/down** along the centre channel. It descends from the axle at z 38 to about z 26–28 at mid-body (lying just above the plates in the channel), then **rises again** toward the head. AWS77 shows it rising from the plates to the head at about z 40. Model it as a straight line from (y +12, z 38) to (y −80, z 30), with a downward bow of 6 mm at mid-span **(guess)**: z(y) = 38 − 8·(12 − y)/92 − 6·sin(π·(12 − y)/92).
- **At the head end**: the arm widens into a **flat black plate/fork** that clamps the hub (AWS74 shows a wide black section about 14 mm tall just in front of the head).

### 3.8 Hammer head HD + blades BL
- **Hub HD**: a **black cylinder about Ø 28 × 12 mm** (axis along X), with a **rosette of 5–6 black socket-head screws** on its face. AWS76 shows 4 outer screws at about r 9 and 2 inner ones. It looks like a printed boss, a mass, or a small outrunner **(guess: a printed hub, since a spinning head would make no sense with fixed blades)**. Centre at about (x 0, y −80, z 34).
- **Blades BL**: **two steel plates** (or one plate plus a printed backing), about **1.5–2 mm thick**, one either side of the hub (spacing about 12 mm), both with the same outline.
  - **Upper spike**: a long **curved hook** rising from the hub to a sharp tip about **36 mm above the hub centre**, curving toward the robot (forward). Its inner (concave) edge is an arc of centre (y −72, z 40) and r ≈ 30, from θ = 100° to 160°; the outer edge is an arc of r ≈ 38 about the same centre.
  - **Lower toe/spike**: a straight tapered point extending **forward-down** from below the hub, about **32 mm long**, ending in a sharp tip at about (y −50, z 10) in rest pose (AWS74 shows the pointed toe reaching toward the body at the left).
  - **Mounting**: 2–3 small screws through the blades into the hub (AWS74 shows 2 visible silver screws at the plate edge plus a hole).
  - Overall head envelope: about **60 mm tall × 50 mm long × 14 mm wide**.
- **Colour**: dark steel, with silver/green-tinted edges where the cut-out halo falls.

### 3.9 Front wedge plate WP
- **Shape**: a **flat rectangle, 76 mm wide × 30 mm tall × 1.5 mm thick**, aluminium or steel (scratched, silver-grey, with green-tinted edges in AWS74). The **lower right and left corners are chamfered** (about 6 mm × 45°).
- **Angle**: tilted about **65° from horizontal** (steep), leaning back. The bottom edge at (y +46, z 1) and the top edge at (y +33, z 28).
- **Fasteners**: **6 silver Phillips pan/countersunk screws** in **two vertical columns of 3**, at x ≈ ±20, spaced 8 mm vertically (AWS76/77 show 3 + 3, AWS74 shows 2 + 2 visible), going into the blue frame's front bosses.
- **Contact**: the top edge rests against the front of the frame/top plates (gap 0). The bottom edge is about 1 mm above the floor.

### 3.10 Forks FK-L, FK-R
- **Shape**: a **flat steel strip**, about **4 mm wide × 1.5 mm thick**, standing **flat** (wide face horizontal) on the floor. Total length about **80 mm**: about 15 mm hidden under the frame and about **65 mm protruding ahead of WP**.
- **Tip**: a **barb/arrowhead**. At about 12 mm from the end the strip **widens to about 7 mm** in a step (the barb shoulder), then tapers linearly to a sharp point. In plan: rectangle x ∈ [−2, 2] up to y = L − 12, then a step to x ∈ [−3.5, 3.5], then lines to the point (0, L). In AWS74 the barb is a **raised step on the top edge**; the strip may stand on edge (vertical) with the barb on its top **(the photos are ambiguous: AWS76 shows the strips mostly edge-on with the barb rising upward, which supports an on-edge orientation, height 4 → 7 mm)**.
- **Position**: x = ±19 (spacing 38 mm, about 0.5 W). They emerge **under the bottom edge of WP**, so they are fixed under the frame floor **(guess: 2 screws each from below)**.

### 3.11 Switch SW
- A **slide switch** in TP-R's slot: black body, small silver lever. Label "ON OFF" adjacent.

## 4. Per-view descriptions
- **Top view**: a 76 × 76 square. Orange side plates are 3 mm strips at the sides (with the wheel tread visible inside at the four corners). Two salmon plates have a central channel. The blue tower sits at the front-left of the channel, and the black arm runs from it rearward past the rear edge by about 50 mm to the head (seen edge-on in top view, a 14 mm wide × 50 mm long shape). At the front: the 76 mm wide wedge strip (seen as 13 mm deep in plan) and the two forks reaching 65 mm forward. Overall top-view length is about **76 + 13 + 65 + 50 ≈ 200 mm**.
- **Front view**: the wedge plate fills the lower 30 mm across the full width, with 6 screws. The fork tips are at the floor at x ±19. Above the plate are the blue tower (left of centre, rising to z 52) with the gear slot, and the head behind it (its spike tip at z ≈ 70, centred). The side plates frame the left and right edges.
- **Side view (left)**: the orange stadium plate dominates (76 × 26) with 2 screws. Above it is the line of the top plates, then the tower D-shape at the front, the arm sloping back, and the head with its spike and toe at the rear. The wedge plate at the front is a steep line, with the forks as thin lines on the floor ahead.
- **Rear view**: the head hub and blades centred, the side plates at the edges, and the rear wheels' tread in the side plate ends **(not photographed)**.
- **Iso**: as in AWS77.

## 5. Part table

| ID | Shape | Size (L × W × H, mm) | Ratio W | Colour | Fixing | Qty |
|---|---|---|---|---|---|---|
| FRM | tub | 70 × 62 × 20 | 0.92 × 0.82 | blue | — | 1 |
| TP-L | plate | 62 × 30 × 2.5 | 0.82 × 0.39 | salmon | 4 × M2 | 1 |
| TP-R | plate | 52 × 30 × 2.5 | 0.68 × 0.39 | salmon | 4 × M2 | 1 |
| SPL | stadium | 76 × 26 × 3, R13 | 1 × 0.34 | orange-red | 2 × M2 into SO | 2 |
| SO | cylinder | Ø 6 × 10 | 0.08 | purple | screw | 4 |
| WH | wheel | Ø 22 × 9 | 0.29 | purple hub, lilac tyre | motor shaft/axle | 4 |
| BLT | O-ring | Ø 1.5 cord | — | black | over the wheels | 2 |
| GB | D-tower | 28 × 12 × 28 (above the plates) | 0.37 | blue | integral/screws | 1 |
| GBC | cheek | 20 × 6 × 20 | — | blue | — | 1 |
| GR | spur gear | Ø 26, ~26 teeth | 0.34 | black | on AX | 1 |
| AX | screw axle | M3 × 30 | — | silver | through GB | 1 |
| ARM | bar | 95 × 6 × 7 | 1.25 | black | on AX | 1 |
| HD | hub | Ø 28 × 12 | 0.37 | black | 5–6 socket screws | 1 |
| BL | sickle plate | 60 × 50 × 1.8 | 0.8 | steel | 2–3 screws | 2 |
| WP | flat plate | 76 × 30 × 1.5 | 1 × 0.39 | aluminium | 6 × M2 | 1 |
| FK | barbed strip | 80 × 4 (7 at the barb) × 1.5 | 1.05 | steel | under the frame | 2 |
| SW | slide switch | 8 × 4 × 4 | — | black | in TP-R | 1 |

## 6. Contact / gap matrix (mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| TP ↔ FRM top | screwed | 0 |
| TP-L inner ↔ GB | notch | 0.5–1 |
| TP inner edges ↔ ARM | channel | 1 each side |
| ARM bottom ↔ channel floor | resting/near | 0–2 |
| ARM root ↔ GB / GBC | on axle | 0.5 |
| GR ↔ AX | fixed | 0 |
| HD ↔ ARM end | clamped | 0 |
| BL ↔ HD | screwed, both faces | 0 |
| HD front ↔ TP rear edge | behind | ~25 (y) |
| SPL inner ↔ WH outer | clearance | 1 |
| SPL ↔ SO | screwed | 0 |
| SO ↔ FRM side | joined | 0 |
| WH inner ↔ FRM side | clearance | 1–2 |
| BLT ↔ WH tops | wraps | 0 |
| WP top ↔ FRM front-top | screwed | 0 |
| WP bottom ↔ floor | above | 1 |
| FK ↔ FRM floor | screwed (guess) | 0 |
| FK ↔ floor | lying on it | 0 |
| FK ↔ WP bottom edge | passes under | 0–1 |
| WP side edges ↔ SPL front arcs | adjacent | 1–2 |

## 7. Mechanism
- **Drive**: two drive motors (one per side, **guess**), each turning one wheel, with the O-ring belt linking front and rear wheels on that side. Skid steer.
- **Weapon**: a weapon motor in the blue lower housing drives a pinion that meshes with the gear GR on the arm axle (visible teeth). The arm swings up from its rearward rest position, through vertical, and slams the head forward-down, so the **spike tip (or toe) strikes about 40–60 mm ahead of the front plate**, where the forks hold the opponent. Spring or electric return. The "thwack" name implies a powered overhead hammer.
- **Head blades**: the upper spike strikes first when swung over. The lower toe acts as a rest foot / self-righter when inverted **(guess)**.

## 8. Assembly order
1. Print the frame FRM with the GB lower housing. Install the weapon motor plus pinion and the drive motors.
2. Insert the arm with GR onto AX through GB, ARM and GBC. Secure with the silver screw.
3. Fit the wheels and belts, then the standoffs SO, and screw on the side plates SPL (2 screws each).
4. Install the battery, ESCs, receiver and switch. Route WR.
5. Screw on TP-L and TP-R (4 + 4 screws). Stick on the label.
6. Screw the forks under the floor. Screw WP onto the front (6 screws).
7. Bolt the blades BL to the hub HD and the hub to the arm end.

## 9. Pixel measurements (±15 px)
- **AWS76** (2033 × 1177): left side plate x 960–1800, y 650–1040 (840 × 390 px, the plate seen nearly side-on; the 76 mm length gives about 11 px/mm). WP x 475–880, y 410–1050. Fork tips at (65, 715) and (185, 1080). Head hub centre about (1770, 330), Ø about 300 px?! (near the camera edge). GB at x 780–1060, y 330–600. The top-plate front edge is at about y 600.
- **AWS74** (1696 × 1428): head spike tip (200, 30), toe tip (45, 430), hub centre (240, 260); GB x 700–1010, y 490–760; forks tip (1660, 990) and (1350, 1380); WP x 740–1300, y 610–1240.
- **AWS77** (1697 × 1306): head at x 1320–1560, y 40–330. TP-R with the switch at about (1290, 545). WP x 380–1000, y 470–1090. Fork tips (85, 840) and (430, 1210).

## 10. Independent estimates and consistency check

| Quantity | By limit | By ratio | By pixels | Reconciled |
|---|---|---|---|---|
| Side plate length | 76 | 1 × W | AWS76: 840 px / 11 px/mm = 76 | **76** |
| Side plate height | 26 | 0.34 W | AWS76: 390 px / 11 = 35 (top plate rim included) | **26 plate + plates above = 30 overall body height** |
| Wheel Ø | 22 | 0.29 W | AWS76: the visible tread arc spans about 250 px vertically → 23 | **22–23** |
| Fork protrusion | 65 | 0.85 W | AWS76: fork from the WP bottom (880, 1000) to the tip (185, 1080), ~700 px, foreshortened ×1.2 → 76 | **70** |
| Head hub Ø | 28 | 0.37 W | AWS76: ~300 px / ~12 px/mm (nearer) = 25 | **26** |
| Arm length | 95 | 1.25 W | AWS74: GB (850, 620) to hub (240, 260) = 710 px / ~8 px/mm = 88 | **90** |
| Tower height above the plates | 28 | — | AWS76: 270 px / 11 = 25 | **26** |

Conflicts:
1. **Body height**: the plate height (26) plus the top-plate level (24) gives a body slightly lower than the side plates. The side plates stick 2 mm above the top plates (AWS76 shows the side plate rim above the top plate edge). **Reconciled: frame top / top plates at z 24, side plates to z 26.**
2. **Wheel invertibility**: the wheel tops (z 22) are below the side plate top (26), so inverted, the robot rests on its side plates and plates. **Reconciled: not wheel-invertible; it relies on the hammer to self-right (guess).**
3. **Fork orientation**: flat vs on edge. AWS76's edge-on look and the barb rising **upward** suggest **on-edge strips (4 mm tall × 1.5 mm thick)**. **Reconciled: on edge**, which is also stiffer vertically against an opponent's weight.
4. **Arm length**: 88–95. **Use 90.**

## 11. Why the designer did it
- **Overhead hammer**: the weapon reaches the opponent's top, which is usually the weakest armour, and works against wedges and spinners from above. The forks hold the opponent in the strike zone.
- **Rest pose rearward, head overhanging**: in rest pose the head protects the rear from wedges/flippers. The heavy head behind counterbalances the forks and wedge. When inverted, swinging the arm can push the robot back over (**self-righting**).
- **Gear-driven arm (not a servo)**: a gearmotor gives more torque and speed for a meaningful hit, and the gear teeth are shielded inside the blue tower (only a slot is open).
- **Sickle blade with a spike and a toe**: the spike concentrates force for puncturing top plates. The curved hook can also hook opponents. Twin plates around the hub resist bending. Steel survives impacts where a printed part would shatter.
- **Steep 65° front plate**: more a **bulldozer/anti-spinner deflector** than a wedge. It protects the frame front and the drive from spinners. The forks do the getting-under.
- **Forks**: thin steel tips are the first to get under opponents (they win wedge battles). On-edge strips present a narrow profile to spinners. The barbs catch and hold the opponent while the hammer strikes. Steel is cheap and replaceable.
- **Big stadium side plates**: they **shield the wheels and belts** (the fragile parts) from side hits and horizontal spinners. Rounded ends deflect hits and help the robot slide off walls. Bright orange gives a visual identity.
- **O-ring belts**: 4WD traction from 2 motors, saving weight, with the belts hidden behind the side plates.
- **Small wheels (22 mm)**: low gearing for pushing, low centre of gravity, and they fit under the guards.
- **Salmon plates screwed down**: access to the electronics. The switch on the plate is reachable at the arena with a labelled direction.
- **Blue/purple/orange colours**: a mixed multi-colour print using available filament. The visible blue tower makes the gearbox easy to inspect.

## 12. Unseen / inner parts

| Part | Guess | Size | Position | Confidence |
|---|---|---|---|---|
| Weapon motor | N20 high-ratio gearmotor or 050/130 motor plus printed reduction | 12 × 10 × 25 or Ø 20 × 25 | front-left under GB: x −8, y +12, z 10 | medium |
| Weapon pinion | small brass/printed pinion meshing with GR | Ø 6 | x −8, under GR | medium |
| Drive motors | 2 × N20 gearmotors, one per side | 12 × 10 × 25 | rear corners, shafts to the rear wheels at (±22, −24, 11) | medium |
| Front wheel axles | idle steel axle pins through FRM to the SO / side plates | Ø 3 | (±29, +24, 11) | low |
| Battery | 2S LiPo 200–300 mAh | 40 × 18 × 10 | centre-right under TP-R: x +14, y −5, z 8 | medium |
| ESCs | 1 dual drive ESC plus 1 weapon ESC | 25 × 15 × 5 | under TP-L rear: x −14, y −20 | low |
| Receiver | micro receiver | 20 × 12 × 5 | under TP-R front | low |
| Switch | slide switch | 8 × 4 × 4 | in TP-R, as seen | high |
| Wiring | WR loop from the weapon motor (in GB) over the top into TP-R toward the ESC. Other wiring is inside. | — | — | medium |
| Internal ribs | a longitudinal wall each side of the central channel supporting the plates; screw posts at the plate corners | 2 mm walls | x ±5 | medium |
| Fork mounts | fork ends sit in slots under the floor, with 2 × M2 each | — | y +20 to +38 | low |
