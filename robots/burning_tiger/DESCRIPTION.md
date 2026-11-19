# Burning Tiger: reference photo descriptions

Source photos (both cut out on white, from the AWS wiki):
- `reference/burning_tiger.aws74.webp` (AWS 74)
- `reference/burning_tiger.aws76.webp` (AWS 76)

Robot type: servo **lifter**. The lifting arm is a red two-rail frame on the top centreline. It ends in a front scoop. The robot has four black gear-toothed wheels and a yellow box chassis.

Conventions: **front** = the scoop end, which faces the camera in both photos. **Left/right** = the robot's own left/right. Sizes are given as ratios to the **chassis body width W**, the yellow box measured side to side without wheels or front add-ons. Guesses are marked *(guess)*.

---

## Overall layout (both photos agree)

- **Main chassis body**: a low rectangular box in translucent/sparkly **golden-yellow** FDM plastic. Print layer lines run horizontally. In plan it is roughly as long as it is wide (L ≈ 1.0–1.15 W). Its height is about 0.28–0.33 W, so it is a flat slab.
- **Top plate**: a flat **brick-red/orange-red** printed plate covers the whole top of the box. It is about 0.03 W thick. It is split into a **left half and a right half** by a central channel where the lifter sits. Each half is a rectangle about 0.35–0.4 W wide and the full chassis length long. It sits flush with or slightly overhangs the yellow walls; a thin yellow lip shows below the red edge on the sides.
- **Wheels**: four, two per side, mounted outboard of the yellow body (a front pair and a rear pair).
- **Lifter arm**: a red frame of two parallel rails running front to back down the middle of the top. It drops over the front edge into a centre scoop.
- **Front add-ons**: two outer corner pieces flank the centre scoop. In AWS74 these are two yellow taped wedges. In AWS76 they are two green barbed forks.

---

## Image 1: `burning_tiger.aws74.webp` (AWS 74)

View: from the front, high three-quarter angle, slightly to the right of centre, looking down at about 35–40°. The front face and the three front wedges are nearest the camera. All four wheels are visible.

### Chassis body (yellow)
- A golden-yellow, translucent, glittery box. The front face is a vertical wall spanning the full width between the outer wedges.
- On the front face, **two large silver Phillips pan-head screws**. One is just left of the left lifter rail and one just right of the right rail, both at about mid-height of the wall. Head diameter is about 0.05 W. They probably hold the front wall to the base or fix internal parts *(guess)*.
- The **sides** are partly hidden by the wheels. Between the front and rear wheels on each side, a yellow box section shows at axle height. This looks like a narrower **side pod / motor housing** stepped in from the top plate edge *(guess: houses the N20-style gearmotors driving each wheel)*.
- The **rear** is not visible.

### Top plate (red)
- There are two flat red rectangles, left and right. The left half shows about 4 small **black pan-head screws**: near the rear-left corner, the front-left corner, the mid-left edge, and the inner rear corner. The right half shows about 4–5, laid out in a similar pattern. Screw heads are about 0.025 W.
- In the centre channel between the halves, below the arm rails, there is a **rectangular window/slot** about 0.12 W wide and 0.3 W long. A **white/grey servo body** is visible through it. The servo sits inside the chassis under the arm, roughly at mid-length *(likely a micro servo, 9 g class)*.

### Lifter arm (red)
- **Two rails**: parallel red printed beams. Each is about 0.06–0.07 W wide and 0.1 W tall in section. The outer edges are about 0.30 W apart and the gap between the rails is about 0.17 W. They run the whole chassis length on the centreline.
- **Rear end**: the rails rise into a raised hump/bracket. At the very rear top they are joined by a **yellow cylindrical cross-tube** (spacer), about 0.17 W long and 0.08 W in diameter. A small **steel pin/bolt end** pokes out of the right rail at this location. This is most likely the **pivot axle** of the arm *(guess, consistent with AWS76)*. The rail ends are rounded around the tube.
- **Front end**: the rails reach the front top edge of the chassis. A second **yellow cylindrical cross-tube** joins them there, the same size as the rear one. A small hex nut shows on the outer face of the right rail at this tube (a through-bolt clamps the rails to the spacer). The rails then **bend 90° downward** and run down the front face of the chassis. They form two vertical red legs, each about 0.07 W wide.
- **Centre scoop**: at the bottom, the two legs join a red scoop block. It is about 0.33 W wide (the same as the rail outer width), roughly as deep front to back, and about 0.12 W tall. It is printed with visible horizontal ridges. **Four black screws** sit in a 2×2 pattern on its top/front face and hold a **lower sloped plate** to it. That plate is **brown/tan** (looks like wood, tufnol or a fibre sheet) with a strip of clear tape across it. The plate slopes down to the floor at about 25–30° and its front edge sits on the floor. The scoop extends about 0.25 W ahead of the chassis front wall.
- **Drive linkage**: inside the channel, a **diagonal red link** (about 0.04 W wide, 0.35 W long) runs from the rear cross-tube / left rail at the rear, forward and down to a **small red servo horn/rocker**. That horn sits at about mid-length, directly over the servo window, and carries two small steel pins (one at each joint). A short horn arm (about 0.07 W) connects to the link.
- **Mechanism (inferred)**: the servo rotates the horn. The horn pushes or pulls the diagonal link, which acts on the arm near its rear. The whole red frame (rails, cross-tubes and scoop) then rotates about the rear pivot, and the front scoop rises off the floor to lift the opponent. Pivot placement is a *guess*. The steel pin at the rear top and the raised rear brackets suggest a rear pivot. The front cross-tube also carries a through-bolt, but it looks like a structural spacer.

### Outer front wedges (AWS74 only)
- **Two wedges**, one at each front corner, outboard of the centre scoop with a gap of about 0.08 W either side of it. Each wedge is about 0.32–0.35 W wide, extends about 0.3 W ahead of the chassis front wall, and is as tall at the back as the chassis wall (about 0.3 W). The face slopes at about 30–35° down to a floor-level edge.
- Material: **yellow printed plastic** (the same filament as the chassis), with **wide clear packing tape** stretched over the sloped face. The tape is scuffed white and orange, and a thin dark line marks its edge.
- Mounting: they look fixed to the chassis front corners. The left wedge's side wall carries on from the chassis side. They are probably printed as part of the chassis front, or bolted on *(guess)*. They are the same height as the chassis, so the scoop is lower than the wedges at the back.
- Relative size: each outer wedge is about the same width as the centre scoop (1 : 1). It reaches slightly further forward than the scoop's front edge (about 1.1 : 1).

### Wheels
- **Four black wheels** with a **fine spur-gear-like knurled tread** (about 50–60 small square teeth around the rim; looks like printed TPU or a moulded gear-tyre). Diameter is about 0.38–0.42 W, larger than the chassis height (wheel Ø ≈ 1.3× body height), so they stick up above the top plate and below the floor line, giving invertible running. Width is about 0.1 W.
- Faces have **three oval/kidney cut-outs** (spoked hub). The hub is dark grey/black.
- Position: the rear pair sits at the rear corners; the front pair is about 0.35–0.45 W ahead of the rear pair. That puts the front wheels just behind the outer wedges, roughly in line with the front third of the chassis. The left-front wheel is directly behind the left wedge, touching its back corner. Wheels sit outboard of the body, with the inner wheel face about 0.02 W from the side pod.
- Drive (inferred): each wheel is directly driven by its own small gearmotor inside the side pod, giving **4WD skid steer** *(guess; no belts or gears visible)*.

---

## Image 2: `burning_tiger.aws76.webp` (AWS 76)

View: from the front-left, three-quarter angle, looking down at about 30°. The left side and front are visible. Same chassis, arm and wheels as AWS74. The **outer wedges are replaced by forks**, and the scoop face differs.

### Chassis body
- Same yellow translucent box. The **left side wall** is clearly visible: a plain yellow wall, about 0.3 W tall, with the two left wheels mounted outside it.
- The front face again has the **two large silver Phillips screws** next to the arm legs.
- At **each front corner** there is a **small round yellow boss**, a cylinder about 0.08 W in diameter whose axis runs left–right, sticking out from the front corner at about 2/3 of the wall height. Each boss carries a **small silver screw/nut** on its outer side and a second screw just inboard on the front wall. The forks mount here.

### Top plate
- Same two red halves. The **left half** shows about 5 black screws: at the rear-left corner, mid-left, front-left, near the rear inner edge, and near the front inner edge. The **right half** shows about 4: the rear-right corner, the front-right corner, and two along the inner/rear edge. The surface shows diagonal print lines, scratches and some white scuffs.
- The slot below the arm is visible in the middle. A dark interior and the **servo horn** can be seen.

### Lifter arm
- Same two red rails. From this angle the **rear bracket is clearly a raised trapezoid/triangle**. The rails rise toward the rear and have a downward gusset leg near the rear-left. The leg has a **silver screw** through it at about 0.4 of the hump height (a pivot or bracket screw). At the **top rear** a **steel pin** sticks out to the right of the right rail, at the rear yellow cross-tube. This pin is the most likely pivot axle *(guess)*.
- **Front yellow cross-tube** between the rails at the front top edge. A short **threaded steel bolt end** sticks out to the right of the right rail there, and a silver screw sits on the outer face of the left rail at that point.
- The front legs drop down the front face. The left leg shows a slight **inward step** near the bottom where it meets the scoop.
- The **diagonal link** runs from the rear (top of the left rear bracket) forward and down to the **red rocker horn** at mid-length. The horn has two round eyes with steel pins. Its geometry is consistent with AWS74.
- **Scoop**: a red printed block with **four black screws** (2×2) on its upper part. A dark seam line runs across it. Below that is a **red sloped plate**, about 0.33 W wide, extending about 0.3 W forward to a floor-level front edge, and covered with clear tape (a scuffed white rectangle). In AWS76 the plate looks **red** (red-printed, or a red-tinted sheet), not the brown sheet of AWS74 *(possibly the same sheet in different light; uncertain)*. The plate's front edge is slightly ahead of the chassis front by about 0.3 W.

### Forks (AWS76 only; replace the yellow wedges)
- **Two long flat forks**, one at each front corner, outboard of the scoop. The gap between each fork and the scoop edge is about 0.15–0.2 W.
- Each fork is a **thin flat plate held vertical** (edge-on to travel, in the robot's side plane). It is about 0.01–0.015 W thick and about 0.07 W tall at its narrowest.
- Shape in side view: it starts at the yellow corner boss at about 2/3 chassis height. It curves forward and down, a short curl or hook around the boss, then runs as a straight tapering blade forward and down to a **sharp point on the floor**. About halfway along there is a **backward-facing barb/step** (a sawtooth notch about 0.08 W deep) on the upper edge. Total length from boss to tip is about 0.55–0.65 W. The tips reach about 0.5 W ahead of the chassis front wall, well beyond the scoop's front edge (forks : scoop forward reach ≈ 1.7 : 1).
- Colour/material: **green faces with bright white/silver edges**. This could be green-painted aluminium, green FR4/G10 fibreglass, or green tape over aluminium with cut edges showing metal *(guess)*.
- Mounting: **one screw through the boss** at the rear end of each fork, so they may be **free-hinged** and trail on the floor, rising over obstacles *(guess)*. Or they are clamped fixed by the screw plus a second screw. A second small screw near each boss suggests a stop or a second fixing.
- Purpose: floor-skimming forks (wedgelets) that get under opponents for the scoop or lifter.

### Wheels
- Same four black gear-tooth-tread wheels with **three kidney/oval holes** in the face. Diameter is about 0.4 W, larger than the body height. The two left wheels are fully visible: the front-left is at about 0.45 W behind the front wall and the rear-left is at the rear corner. The gap between their tyres is about 0.15 W. The right-side wheels are visible behind the body, in matching positions.

---

## Relative-size summary (ratios to chassis width W)

| Part | Size (approx.) | Notes |
|---|---|---|
| Yellow chassis body | W × 1.0–1.15 W × 0.3 W tall | flat box |
| Red top plate halves (each) | 0.37 W × 1.0 W × 0.03 W | two halves, about 4–5 screws each |
| Wheels (×4) | Ø 0.40 W, width 0.10 W | gear-tooth tread, 3 holes; Ø ≈ 1.3× body height |
| Arm rails (×2) | 0.065 W wide × 0.10 W tall × ~1.1 W long | 0.30 W outer spacing |
| Yellow cross-tubes (×2) | Ø 0.08 W × 0.17 W long | front top and rear top of arm |
| Rear hump / pivot bracket | about 0.15 W above the top plate | steel pin at the top |
| Diagonal link | 0.04 W × ~0.35 W | rear arm to servo horn |
| Servo horn / rocker | ~0.07 W | over the central slot |
| Centre scoop | 0.33 W wide, ~0.3 W forward reach | 4 screws, sloped plate |
| Outer wedges (AWS74) | 0.33 W wide each, 0.3 W reach, 0.3 W tall | yellow plus tape |
| Forks (AWS76) | ~0.6 W long, ~0.07 W tall, thin | green, barbed, pivot boss |
| Front-wall Phillips screws | head Ø 0.05 W | two |

The wheelbase (front to rear axle) is about 0.45 W. The track (outside of wheels) is about 1.25 W. With the AWS74 wedges or the AWS76 forks, the overall length is about 1.4–1.6 W.

## Hidden / uncertain
- **Servo type and exact pivot**: the servo is only glimpsed (white body through the slot). Whether the arm pivots at the rear cross-tube pin or about a separate rear bracket screw is uncertain; a rear pivot is the best guess.
- **Drive motors, battery, receiver/ESC**: not visible. They are presumed to sit inside the yellow box, with the motors in the side pods behind each wheel *(guess)*.
- **Underside**: not visible. The floor is presumably flat, and the wheels protrude below it.
- **Rear wall**: not seen in either photo. It is presumably a plain yellow wall.
- **Scoop plate material** (brown in AWS74, red in AWS76) and **fork material** are uncertain.
- **Fork hinging**: the single-screw boss suggests a pivot, but it could be fixed.
