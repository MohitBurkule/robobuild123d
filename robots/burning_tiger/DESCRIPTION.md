# Burning Tiger: full rebuild description from reference photos

Source photos (both cut out onto white by the AWS wiki):
- `robots/burning_tiger/reference/burning_tiger.aws74.webp`: AWS 74. Shows the front, a high three-quarter from slightly right of centre, about 35–40° down. All four wheels are visible. Fitted with two **yellow taped outer wedges**.
- `robots/burning_tiger/reference/burning_tiger.aws76.webp`: AWS 76. Shows the front-left three-quarter, about 30° down. The left side wall and both left wheels are visible. Fitted with two **green barbed forks** instead of the outer wedges.

Everything stated as fact below is read directly from those two photos. Anything inferred is marked **(guess)**. Dimensions in mm are **estimates**, scaled from the AWS antweight limit (150 g, fits a 101.6 mm / 4 in cube) and from the project spec draft (`spec.json` uses a body prism about 70 mm wide × 80 mm long × 24 mm tall, which matches the photo proportions). Ratios are given against **W = yellow chassis width ≈ 70 mm**.

---

## 0. Coordinate system and naming

- **+X** = robot's right, **+Y** = forward (toward the scoop), **+Z** = up. The origin is at the centre of the chassis footprint on the floor.
- **Front** = the end with the red scoop and the outer wedges/forks. In both photos the front faces the camera.
- **Left/right** are the robot's own (in AWS74 the robot's left is on the image left; in AWS76 the left side faces the camera).
- Part IDs (used in the tables):

| ID | Part |
|---|---|
| CH | yellow chassis body (tub) |
| SP-L / SP-R | yellow side pods (between wheels, each side) |
| TP-L / TP-R | red top plate halves |
| SL | central slot/window in the top (servo window) |
| SV | lifter servo (inside) |
| HN | red servo horn / rocker |
| LK | red diagonal pushrod link |
| RL-L / RL-R | red lifter arm rails (left/right) |
| CT-F | yellow front cross-tube (arm spacer) |
| CT-R | yellow rear cross-tube (arm spacer / pivot) |
| PV | steel pivot pin at the rear of the arm |
| BR-L / BR-R | red rear pivot brackets / gussets (part of or under the rails) |
| SC | red scoop block (bottom of the arm) |
| SCP | scoop face plate (brown sheet in AWS74, red/taped in AWS76) |
| WG-L / WG-R | yellow taped outer wedges (AWS74 only) |
| BS-L / BS-R | yellow front-corner fork bosses (AWS76 only) |
| FK-L / FK-R | green barbed forks (AWS76 only) |
| WH-FL, WH-RL, WH-FR, WH-RR | four black gear-tread wheels |
| M-x | drive gearmotors (hidden, guess) |
| S-FW | 2 large silver Phillips screws on the chassis front wall |
| S-TP | small black screws on the top plates |
| S-SC | 4 black screws on the scoop |
| S-AR | bolts/nuts through the arm rails |
| S-FK | fork boss screws |
| BAT, RX, ESC | battery, receiver, ESCs (hidden, guess) |

---

## 1. Overall description in one paragraph

Burning Tiger is a **low, flat, four-wheel servo lifter**. The body is a **golden-yellow, translucent, glittery FDM box** about 70 mm wide, 80 mm long and 22–24 mm tall. Its top is covered by **two flat brick-red plates**, one left and one right, with a central channel between them. Lying in that channel is a **red two-rail lifting arm**. The rails run front to back on the centreline. Their **rear ends are raised into a hump** where a **steel pin** pivots them, and their **front ends bend 90° down** over the front edge of the chassis into a **red scoop** that sits on the floor ahead of the chassis. Two **yellow cylindrical spacers** tie the rails together, one at the front top edge and one at the rear hump. A **small red servo horn** in the middle of the channel drives the arm through a **diagonal red pushrod**. The four **black wheels** have fine gear-tooth tread and are larger than the body is tall, so the robot can run upside down. They sit outboard of the body, two per side, in the rear two-thirds of the length. The front corners carry either **two yellow sloped wedges covered in packing tape** (AWS74) or **two long thin green barbed forks** on round bosses (AWS76). These flank the centre scoop, giving the front a three-pronged look.

---

## 2. Part-by-part description

### 2.1 Chassis body (CH)
- **Shape**: a rectangular box. Plan is about **70 mm wide (W) × 80 mm long (1.15 W)**; height to the underside of the top plates is about **21 mm (0.30 W)**. The edges are sharp; any corner radii are under 1 mm. The walls are plain and flat, with no chamfers visible.
- **Colour/material**: translucent **golden-yellow/amber** filament with a sparkle/glitter effect. Horizontal print layer lines (about 0.2 mm) run around the walls. Possibly PETG or "silk"/glitter PLA (the spec says nylon; the look is glittery PETG/PLA) **(guess)**.
- **Walls**: front, left, right and rear walls are each about **2–3 mm** thick **(guess, from edge highlights)**. The floor is not seen.
- **Front wall**: a full-width vertical face, about **70 mm × 21 mm**. It carries the **two large silver Phillips pan-head screws S-FW**. Each sits about **4–6 mm outboard of the arm legs** (x ≈ ±19 mm) at about **mid-height** (z ≈ 11 mm). Head Ø is about **5.5 mm**, so roughly M3 pan head. They probably fasten the front wall to an internal part, such as the servo mount or the front of the floor **(guess)**.
- **Side walls**: the left wall is seen fully in AWS76. It is plain yellow, about **80 mm long × 21 mm tall**, with no screws visible between the wheels. Behind each wheel there is presumably an axle hole **(hidden)**.
- **Rear wall**: never seen. Presumably plain yellow **(guess)**.
- **Top**: open, closed by the two red top plates (TP-L/TP-R). There is a thin **yellow lip** (about 0.5–1 mm) visible just under the red plate edges, so the red plates sit flush with or slightly inside the wall tops.

### 2.2 Side pods (SP-L, SP-R)
- In AWS74, on the **right** side between the front-right and rear-right wheels, a **yellow box section** sticks out from the side wall at about axle height. It is roughly **12–14 mm long (fore-aft) × 10–12 mm tall**, and projects about **6–8 mm outboard** of the main side wall, almost to the inner faces of the wheels. A similar block on the left appears in AWS74 (left, behind the left wedge, x ≈ −38 mm).
- In AWS76 the left side shows the wall running straight between the wheels at full height, and a lower **yellow step/rail** under the wheels. So the pod may simply be the **lower part of the side wall protruding** to carry the wheel axles/motors **(guess)**.
- **Function (guess)**: housing for the N20-style gearmotors or the outer bearing of the wheel axles. It also acts as a spacer, so the wheel inner faces sit about **1–2 mm** from it.

### 2.3 Top plates (TP-L, TP-R)
- **Shape**: two flat rectangles. Each is about **26–28 mm wide × 80 mm long × 2 mm thick**, running the full chassis length. Their inner edges stop about **8–10 mm** from the centreline, leaving a **central channel about 18 mm wide** where the arm rails sit. Their outer edges are flush with the chassis side walls; the plates do not overhang the wheels.
- **Colour**: matt **brick-red / tomato red** printed plastic, the same colour as the arm. There are visible **diagonal 45° infill lines** on the top surface (AWS76) and light white scuffs.
- **Fasteners (S-TP)**: small **black pan-head (or button) Phillips screws**, head Ø about **4 mm** (M2–M2.5).
  - Left plate (seen in both photos): **5** screws. One at the rear-left outer corner (about 5 mm in from the edges), one at the mid-left outer edge, one at the front-left outer corner, one at the rear inner corner beside the arm hump, and one at the front inner corner near the front cross-tube.
  - Right plate: **4–5** screws. Rear-right corner, front-right corner, mid-right edge, rear inner corner (by the hump), and front inner corner.
  - Total is about **9–10 screws**, threading into the yellow walls or into internal bosses in the chassis corners **(guess)**.
- **Contact**: the bottom faces rest on the top edges of the yellow walls (and on internal posts). The inner edges face the arm rails with a **gap of about 1–2 mm** (the rails must swing freely).

### 2.4 Central slot / servo window (SL)
- Between the two rails, at about mid-length (y ≈ −5 to +15 mm), there is a **rectangular opening about 10 mm wide × 22 mm long** through which the inside is visible. AWS74 shows a **white/light-grey servo case** inside, and a small amount of wiring. AWS76 shows a darker interior.
- The channel floor between the rails, outside the window, is **red**. It looks like a third narrow red plate or the inner flange of the top plates, so the channel is closed except at the window **(guess)**.

### 2.5 Lifter servo (SV), hidden
- **Seen**: only its white/grey top through the window in AWS74.
- **Guess**: a **micro servo (9 g class, about 23 × 12 × 23 mm)**, mounted inside the chassis with its **output spline pointing sideways (±X)** or up. Its output is coupled to the red horn HN visible in the window. The horn's rotation axis looks **transverse (X)**: the horn swings in the vertical fore-aft plane.

### 2.6 Servo horn / rocker (HN)
- **Shape**: a short **red printed lever**, about **8–10 mm long × 4 mm wide × 3 mm thick**, with **two round eyes**. One eye is on the servo output; the other carries a **small steel pin** (about 1.5–2 mm) that connects to the pushrod LK. AWS74 shows a second small rocker with **two pins** (silver dots) at about y ≈ +5 mm in the window. AWS76 shows a red **double-eye link** sitting at the window, angled.
- **Position**: in the window, centred on X, at about **mid-length**. Its top is about **3–5 mm above the top plates**.
- **Function**: the servo output arm. It rotates about the transverse axis and pushes or pulls LK.

### 2.7 Diagonal pushrod link (LK)
- **Shape**: a **straight red printed bar** about **25–28 mm long × 4 mm wide × 3 mm thick**, with a round eye at each end.
- **Position**: from the horn HN at mid-length, it runs **rearward and upward** to the **rear arm cross-tube / left rail inner face** at the hump. It is seen running diagonally, from the inside of the left rail at the rear (top) to the centre window (bottom). In AWS74 it crosses from the rear-left (top of the image) toward the centre, between the rails.
- **Joints**: a small steel pin at each end.
- **Function**: a 4-bar linkage. The servo horn rotates, LK transfers the force to the arm frame close to the pivot, and the arm rotates.

### 2.8 Arm rails (RL-L, RL-R)
- **Shape**: two identical, parallel **red printed beams**, each about **5 mm wide (X) × 7–8 mm tall (Z)** in section. The outer faces are about **22 mm apart** (x = ±11 mm) and the inner gap is about **12 mm**. In plan the rails are straight.
- **Side profile** (best in AWS76):
  1. **Rear hump**: at the rear (y ≈ −40 to −25 mm) the rail top rises to about **z ≈ 36 mm** (about 13–15 mm above the top plates). It forms a **trapezoid** with a sloped front face, and the rear end is rounded around CT-R. A **downward gusset leg** below the hump on the left rail reaches down to the top plate at about y ≈ −28 mm. A **silver Phillips screw** goes through that leg at about z ≈ 28 mm; this could be the bracket fixing **(guess)**.
  2. **Main run**: from the hump the rails **slope gently down to the front**, from about z ≈ 30 mm at y ≈ −20 to about z ≈ 26–27 mm at the front top edge (y ≈ +40), lying about **2–4 mm above the top plates**.
  3. **Front bend**: at the front top edge of the chassis the rails make a **rounded 90° bend** (inner radius about 3 mm) and drop vertically **down the front wall** as two **legs**. Each leg is about **6 mm wide × 5 mm deep (Y) × 20 mm tall**, standing about **1–2 mm proud of the yellow front wall** (they do not touch it, leaving room to swing).
  4. **Leg foot**: the legs end in the scoop block SC at about z ≈ 4–14 mm.
- **Fasteners (S-AR)**:
  - At **CT-F** (front top): a **through-bolt** runs across both rails and the tube. AWS74 shows a **small hex nut** on the right rail's outer face. AWS76 shows a **threaded steel bolt end protruding about 4 mm** from the right rail, and a **silver Phillips pan head** on the left rail's outer face.
  - At **CT-R** (rear hump): a **steel pin** protrudes about **3–4 mm from the right rail's outer face** near the top-rear (AWS74 and AWS76). AWS74 shows a small silver pin end on the left rear too.
- **Colour**: the same brick-red as the top plates, with a slightly glossier surface and visible layer lines.

### 2.9 Front cross-tube (CT-F)
- **Shape**: a **yellow cylinder** (the same glitter filament as the chassis), about **Ø 7–8 mm × 12 mm long**. It spans exactly the inner gap between the rails, which clamp it between their inner faces.
- **Position**: at the **front top edge**, at y ≈ +36 mm, z ≈ 27 mm. Its top is about level with the rail tops and its bottom about 1 mm above the top plates/front wall top edge.
- **Hold**: a through-bolt (see S-AR) runs along its axis.
- **Function**: a structural spacer keeping the rails parallel, and possibly a stop resting on the chassis front top edge when the arm is down **(guess)**.

### 2.10 Rear cross-tube (CT-R) and pivot (PV)
- **Shape**: a **yellow cylinder**, about **Ø 8 mm × 12 mm long**, like CT-F.
- **Position**: at the **top-rear of the hump**, y ≈ −36 mm, z ≈ 32 mm, between the rails.
- **Pivot pin PV**: a **steel pin, about Ø 2–3 mm**, passes along the tube axis and protrudes from the right rail (and probably the left). It is the **most likely pivot axis** of the arm **(guess)**. The pin is held by the **rear pivot brackets BR**: fixed red brackets screwed to the top plates, inside or outside the rails. These are visible in AWS76 as the downward gusset leg with a screw. Either the tube is fixed to the chassis brackets and the rails rotate on the pin, or the tube rotates with the arm on the fixed pin **(uncertain)**.

### 2.11 Scoop block (SC) and scoop plate (SCP)
- **SC shape**: a red printed **block**, about **24 mm wide (X, the same as the rail outer width) × 10–12 mm deep (Y) × 10 mm tall**, fixed to the bottoms of both legs (printed as one piece with the legs, or screwed) **(guess)**. Its front face shows **horizontal ribbing** (print layers). It has a **2 × 2 pattern of black Phillips pan-head screws S-SC** (head Ø about 4 mm) on its top-front face: two upper screws about 6 mm apart vertically from two lower ones, about 16 mm apart horizontally.
- **SCP shape**: a **flat sloped plate**, about **24 mm wide × 22 mm long (down the slope) × 1.5 mm thick**, angled about **25–30° to the floor**. Its leading edge rests on the floor about **25–30 mm ahead of the chassis front wall**. Its rear/upper edge tucks under SC and is clamped by the four screws.
  - **AWS74**: **brown/tan** (looks like wood veneer, tufnol or brown fibreboard), with a **rectangular patch of clear packing tape** over most of its face (scuffed white). It is slightly wider than the legs.
  - **AWS76**: **red** (a red printed plate, or the same sheet in a red tint). It has a **taped patch** and a **dark seam line** between SC and SCP across the full width, so it is a separate part.
- **Contact**: SCP's front edge touches the floor. SC's bottom is about **3–5 mm above the floor**. SC's rear face sits about **1–2 mm ahead of the chassis front wall** (a small gap so it can rise).

### 2.12 Outer wedges (WG-L, WG-R), AWS74 only
- **Shape**: a **solid right-triangle prism** (doorstop). The back face is vertical and **as tall as the chassis wall (about 21 mm)**. The bottom is flat on the floor. The top is a sloped face at about **35°** running from the chassis top edge down to a floor-level front edge. Each wedge is about **22–24 mm wide (X) × 28–30 mm long (Y)**. Small vertical side walls (triangles) are visible.
- **Colour**: the same **yellow glitter filament** as the chassis. The sloped face is covered in **clear packing tape**, scuffed orange-white, with a thin dark outline where the tape edges are.
- **Position**: WG-L spans x ≈ −35 to −12 mm and WG-R x ≈ +12 to +35 mm, i.e. **flush with the chassis side walls on the outside**. Between each wedge's inner side and the scoop's outer side there is a **gap of about 3–6 mm**. Their back faces **touch the chassis front wall** (integral or glued/screwed; the left wedge's side wall looks continuous with the chassis side wall, so they are probably **printed as part of the chassis front** **(guess)**).
- **Relative**: the wedge front edges are about **3–5 mm ahead** of the scoop's front edge. Each wedge is about **the same width as the scoop** (1 : 1). The wedge back height (21 mm) is about **twice the scoop block height**.
- **Front wheels**: the rear faces of the wedges are close to the **front-left and front-right wheels** (gap about 1–3 mm in AWS74; the left wedge back corner nearly touches WH-FL).

### 2.13 Fork bosses (BS-L, BS-R), AWS76 only
- **Shape**: a **short yellow cylinder**, about **Ø 8 mm × 6 mm long**, with its axis along **X**, standing proud of each **front corner**. It is centred about **4 mm behind the front wall plane** and **at about z ≈ 14 mm** (2/3 of the wall height). It looks printed as part of the chassis (a lug).
- **Screws S-FK**: a **silver pan-head Phillips screw** or nut on the outer end of each boss (Ø about 4 mm). A **second small silver screw** sits on the front wall about 5 mm inboard and 3 mm lower. It may be a stop for the fork **(guess)**.

### 2.14 Forks (FK-L, FK-R), AWS76 only
- **Shape**: a **thin flat plate standing on edge** (the plate plane is vertical and parallel to the YZ plane). Thickness is about **1–1.5 mm**. Seen from the side (the left fork is clearly visible):
  1. Rear end: a **short curved hook** that wraps around the boss (inner radius about 4 mm) with a hole for the boss screw.
  2. From the boss it runs **forward and down** at about 35° below horizontal.
  3. At about the halfway point there is a **backward-facing barb/step**: the top edge drops by about **6 mm** in a sharp notch (a sawtooth).
  4. It then continues as a **tapered blade** to a **sharp point on the floor**.
  - Total length from boss centre to tip is about **45 mm**. Height (top to bottom edge) is about **5 mm**, tapering to 0 at the tip.
- **Colour/material**: **green faces with white/silver edges**. Possibly green FR4/G10 fibreglass, green-anodised or green-painted aluminium, or aluminium wrapped in green tape **(guess)**.
- **Position**: FK-L at x ≈ −33 mm, FK-R at x ≈ +33 mm, i.e. just inside the chassis side planes. The gap between each fork and the scoop's outer edge is about **18–20 mm**. The tips reach about **y ≈ +78 mm**, roughly **38 mm ahead of the chassis front wall** and about **10 mm beyond the scoop front edge**.
- **Mount/mechanism**: one screw through the boss. They are likely **hinged** so they rest on the floor under their own weight and ride over obstacles. Or they are clamped tight **(guess)**.

### 2.15 Wheels (WH-FL, WH-RL, WH-FR, WH-RR)
- **Shape**: a cylinder about **Ø 30 mm × 8 mm wide**. The rim carries **fine square gear-like teeth**: about **50–60 teeth**, each about **1 mm tall × 1 mm wide**, running across the full width (like a spur gear or a knurled timing pulley). The outer face is flat, with **three kidney/oval cut-outs** (each about 8 × 5 mm) arranged at 120°, leaving three spokes and a central hub about Ø 8 mm.
- **Colour/material**: matt **black**. Possibly printed TPU or black PLA with a TPU tread **(guess)**.
- **Positions** (wheel centres):
  - WH-RL: x ≈ −40 mm, y ≈ −28 mm, z ≈ 15 mm.
  - WH-FL: x ≈ −40 mm, y ≈ +12 mm, z ≈ 15 mm.
  - WH-RR / WH-FR mirror these at x ≈ +40 mm.
  - So the **wheelbase is about 40 mm**, the **tyre-to-tyre gap fore-aft is about 10 mm**, and the **track (outer faces) is about 88 mm** (1.25 W).
- **Height**: Ø 30 mm against a body height of about 23 mm (with top plates), so the wheels stick out **about 4 mm above the top plates** and **about 4 mm below the body floor** **(guess for the bottom)**. That makes the robot **invertible**.
- **Mount**: each wheel is on an axle/motor shaft coming out of the chassis side or side pod. There is **no outer wheel guard**; the outer faces are exposed. Each wheel's inner face is about **1–2 mm** from the yellow side wall or pod.
- **Drive (guess)**: **4WD skid steer**, each wheel driven by its own **N20 micro gearmotor** (about 12 × 10 × 25 mm) lying transversely inside the chassis, or two motors with front/rear wheels coupled internally. No belts or chains are visible.

### 2.16 Wiring, switch, electronics (hidden)
- No external wiring or switch is visible in either photo. The power switch/link is probably on the **rear wall or underside** **(guess)**.
- The battery (about 2S 300 mAh LiPo), receiver and two dual ESCs or a combined board are presumed inside the chassis **(guess)**.

---

## 3. Per-view descriptions (for silhouette matching)

### 3.1 Top view (plan; synthesised from both photos)
- The outline is a **cross/"H" shape**: a 70 × 80 mm rectangle (CH plus TP), with four 30 × 8 mm wheel rectangles stuck to the sides in the rear 2/3. In front there are three prongs: two outer wedges (each 23 × 29 mm, flush with the sides) and a centre scoop (24 × 30 mm). Overall length is about 110 mm with wedges and about 118 mm with forks.
- On top: two red rectangles left and right with about 4–5 black screw dots each. A central channel holds two parallel red rails (22 mm outer width) running the full length. There is a yellow tube across the front end and a yellow tube across the rear end. A diagonal red link runs inside the channel from the rear-left to the centre window, where the red horn is.
- The forks in plan (AWS76) are thin lines (about 1.5 mm) at x ≈ ±33 mm, extending to y ≈ +78 mm.

### 3.2 Front view
- Bottom layer: the floor line. On it sit the **outer wedge fronts** (AWS74: two sloped yellow faces with tape, each 23 mm wide, rising to 21 mm at the back) or **fork tips** (AWS76). The **scoop plate SCP** sits in the middle, 24 mm wide, sloped.
- Middle: the yellow front wall (70 × 21 mm) with **two big silver Phillips screws** at x ≈ ±19 mm, z ≈ 11 mm. The **red arm legs** run vertically at x ≈ ±8.5 mm (6 mm wide each) and end in **SC** with its 4 black screws.
- Top: the top-plate edges and the **front yellow cross-tube** between the legs at the top. Above and behind are the **rear hump** of the rails (up to z ≈ 36 mm) and the **pivot pin** ends.
- Sides: the **wheels** stick out beyond the chassis, about 9 mm each side, and above the top plates by about 4 mm. Their black gear tread silhouettes are visible.

### 3.3 Left side view (AWS76 is closest)
- Silhouette: the low yellow rectangle (80 × 21 mm) topped by the red plate line (2 mm). Two big black wheels (Ø 30) cover most of the side, with a 10 mm gap between them. Each wheel face shows 3 kidney holes.
- Above the body: the **rear hump** of the arm (trapezoid, up to z ≈ 36 mm) with the gusset leg and a silver screw. The rail slopes down to the front top edge, then the leg drops down the front wall, the scoop SC, and the sloped plate SCP to the floor.
- At the front-left corner: the **boss** (Ø 8) with the **fork** curving down to a sharp floor point about 38 mm ahead of the wall. The barb is visible halfway.
- AWS74 equivalent: the **taped yellow wedge** triangle in front of the front-left wheel instead.

### 3.4 Rear view (not photographed; inferred)
- The yellow rear wall (70 × 21 mm), with the four wheels sticking out at the sides and top. The rear hump of the arm pokes up in the middle (22 mm wide, up to z ≈ 36), showing the end of CT-R and the pivot pin. Probably a switch and charge port **(guess)**.

### 3.5 Isometric (front-left-top, as AWS76)
- The most informative view. The left wall shows both wheels. The top shows both plates with screws. The arm runs the full length with the hump at the back. The scoop and forks are at the front. The robot reads as a **flat tank with a raised spine and three front prongs**.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| CH | open box | 70 × 80 × 21 | 1 × 1.15 × 0.30 | yellow glitter FDM | — | 1 |
| SP | side block | 13 × 7 × 11 | 0.19 × 0.10 × 0.16 | yellow | integral (guess) | 2 |
| TP | flat plate | 27 × 80 × 2 | 0.39 × 1.15 × 0.03 | red FDM | 4–5 × M2 black pan | 2 |
| SL | window | 10 × 22 | 0.14 × 0.31 | — | — | 1 |
| SV | micro servo | 23 × 12 × 23 | — | white/grey | inside (guess) | 1 |
| HN | 2-eye lever | 9 × 4 × 3 | 0.13 | red | servo spline plus pin | 1 |
| LK | straight link | 27 × 4 × 3 | 0.39 | red | 2 steel pins | 1 |
| RL | bent beam | 5 × 8 section, ~85 long + 20 leg | 0.07 × 0.11 | red | bolts at CT-F, CT-R | 2 |
| CT-F | cylinder | Ø 8 × 12 | 0.11 × 0.17 | yellow | through-bolt plus nut | 1 |
| CT-R | cylinder | Ø 8 × 12 | 0.11 × 0.17 | yellow | pivot pin | 1 |
| PV | steel pin | Ø 2.5 × ~26 | — | steel | press/clip (guess) | 1 |
| BR | gusset | ~8 × 10 | — | red | 1 silver Phillips screw | 1–2 |
| SC | block | 24 × 11 × 10 | 0.34 × 0.16 × 0.14 | red | integral with legs (guess) | 1 |
| SCP | sloped plate | 24 × 22 × 1.5 | 0.34 × 0.31 | brown (AWS74) / red (AWS76), taped | 4 × M2 black pan | 1 |
| WG | doorstop wedge | 23 × 29 × 21 | 0.33 × 0.41 × 0.30 | yellow plus clear tape | integral/glued (guess) | 2 (AWS74) |
| BS | lug cylinder | Ø 8 × 6 | 0.11 | yellow | integral | 2 (AWS76) |
| FK | barbed blade | 45 × 5 × 1.5 | 0.64 × 0.07 | green plus silver edges | 1 screw (pivot) plus 1 stop screw | 2 (AWS76) |
| WH | gear-tread wheel | Ø 30 × 8 | 0.43 × 0.11 | black | motor shaft | 4 |
| S-FW | pan Phillips | head Ø 5.5 | 0.08 | silver | into the front wall | 2 |
| S-TP | pan Phillips | head Ø 4 | 0.06 | black | into the chassis | 9–10 |
| S-SC | pan Phillips | head Ø 4 | 0.06 | black | SCP to SC | 4 |
| S-AR | bolt/nut/pin | Ø 2.5–3 | — | steel | through the rails | 2–3 |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| TP-L/R bottom ↔ CH wall tops | rest on, screwed | 0 |
| TP inner edge ↔ RL outer face | side by side | 1–2 |
| RL bottom ↔ TP/channel floor (main run) | above | 2–4 |
| RL inner faces ↔ CT-F / CT-R ends | clamped | 0 |
| CT-F bottom ↔ CH front-top edge | above (rest stop, guess) | 0–1 |
| CT-R ↔ PV | concentric | 0 |
| BR ↔ TP | screwed (guess) | 0 |
| RL legs back ↔ CH front wall | in front | 1–2 |
| SC rear ↔ CH front wall | in front | 1–2 |
| SC bottom ↔ floor | above | 3–5 |
| SCP front edge ↔ floor | touching | 0 |
| SCP ↔ SC | screwed (4) | 0 |
| WG back ↔ CH front wall | joined | 0 |
| WG inner side ↔ SC/SCP outer edge | side by side | 3–6 |
| WG bottom ↔ floor | sitting | 0 |
| WG back corner ↔ WH-FL/FR tyre | near | 1–3 |
| BS ↔ CH front corner | integral | 0 |
| FK ↔ BS | screwed/pivot | 0 |
| FK tip ↔ floor | touching | 0 |
| FK inner face ↔ SCP outer edge | side by side | 18–20 |
| WH inner face ↔ CH side / SP | near | 1–2 |
| WH-FL tyre ↔ WH-RL tyre | fore-aft gap | ~10 |
| WH top ↔ TP top plane | wheel sticks out above | +4 |
| WH bottom ↔ CH floor plane | wheel sticks out below | +3–4 (guess) |
| HN ↔ LK | pinned | 0 |
| LK ↔ RL/CT-R | pinned | 0 |
| HN ↔ SV | on spline | 0 |

---

## 6. Mechanism

1. **Drive**: four wheels, skid steer. The wheels stick out above and below the body for invertible running **(motors guessed)**.
2. **Lifter**: the servo rotates the horn HN. The pushrod LK pushes the arm frame near the rear pivot PV, so the whole red frame (rails, tubes, legs, scoop) **rotates about PV**. Because the scoop is about 75 mm in front of the pivot and the link acts about 10–15 mm from it, a small servo rotation gives a large scoop rise, roughly **20–30 mm of tip lift** **(guess)**. The front cross-tube resting on the chassis front edge acts as a **down stop**.
3. **Outer wedges / forks**: passive. The forks may be free-hinged so they trail on the floor.

---

## 7. Assembly order (suggested rebuild)

1. Print **CH** (box with floor, walls, side pods, and in AWS76 the corner bosses BS; in AWS74 the wedges WG as integral front lugs).
2. Install **4 drive gearmotors** in the chassis (two each side, shafts out through the side walls at z ≈ 15 mm, y ≈ −28 and +12 mm). Press the **wheels** on.
3. Install the **servo SV** centrally under the window, output toward the side or up. Fit the **horn HN**.
4. Install the electronics (battery, receiver, ESCs) and the switch.
5. Screw the **top plates TP-L/TP-R** onto the wall tops (9–10 black M2 screws), leaving the central channel open.
6. Fix the **rear pivot brackets BR** (screw).
7. Assemble the **arm**: slide **CT-R** between the rails at the hump, insert the **pivot pin PV** through the rails, tube and brackets. Bolt **CT-F** between the rails at the front with the through-bolt and nut.
8. Screw **SCP** to **SC** with 4 black screws, and apply **packing tape** to SCP (and to the WG faces).
9. Connect **LK** between **HN** and the arm (steel pins at both ends).
10. AWS76: screw the **forks FK** onto the bosses **BS** with the silver screws.
11. Tape the wedge faces (AWS74).

---

## 8. Hidden / uncertain list
- Exact pivot point of the arm (rear pin is the best guess) and where LK attaches.
- Whether the servo output is transverse or vertical.
- Drive motor count (4 vs 2) and layout.
- The side pod form and whether it is part of the wall.
- Floor/underside, rear wall, switch location.
- Scoop plate material (brown sheet vs red), fork material (FR4 vs aluminium), and whether the forks are hinged.
- All mm values are scaled estimates (±15%).
