# Ablation: full rebuild description from reference photos

Source photos (all three cut out onto white by the AWS wiki):
- `robots/ablation/reference/ablation.aws72.webp` (1423 × 1208 px): AWS 72. **Front-right three-quarter**, camera about 35° above the floor and about 45–50° to the right of the robot's nose. The two right wheels are on the image left, the four forks point to the bottom-right, and the arm with its disc rises at the image top-left (robot rear-right in projection). Chassis colour is **black**. The forks are **four silver/grey steel bars** with ground chisel tips.
- `robots/ablation/reference/ablation.aws74.webp` (1438 × 1154 px): AWS 74. Almost the same camera pose as AWS72, slightly lower and more frontal. Chassis colour is **very dark green** (it reads black-green). The forks are the same four bars, now with **green-tinted** shanks (paint, or anodised/coloured tape) and bright steel tips. The power switch on the top lid has been swapped for a **white 2-pin connector/link**.
- `robots/ablation/reference/ablation.aws76.webp` (2298 × 1482 px): AWS 76. **Front-left three-quarter**, camera about 25–30° above the floor and about 60° to the left of the nose, so the left side, both left wheels and the disc face-on are visible. Chassis colour is **dark green**. The forks are now **flat green plates** (FR4/G10 fibreglass look, or printed and taped): two **wide outer blades** that grow out of the wedge bottoms and two **narrow inner blades**, all with small upturned barb tips.

Pixel coordinates in this file refer to copies scaled to **1200 px on the long side** (AWS72 → 1200 × 1019, AWS74 → 1200 × 963, AWS76 → 1200 × 774), read by eye, ±10 px.

Everything stated as fact below is read directly from those photos. Anything inferred is marked **(guess)**. Dimensions are **estimates**, scaled from the AWS antweight rules (150 g, must fit inside a 101.6 mm / 4 in cube) and from the wheels. Ratios are given against **W = chassis body width between the wheels ≈ 66 mm**, and **D = wheel diameter ≈ 29 mm**.

Robot class: **hammer-saw** (an overhead swinging arm carrying a spinning vertical disc). `REFERENCE.json` labels it `vertical_spinner`, disc, axis x, position rear, 2 teeth. That label matches the rest pose: the disc sits behind the robot, spinning about a transverse (X) axis. In a fight the arm swings over the top and brings the spinning disc down onto whatever the four front forks are holding.

---

## 0. Coordinate system and naming

- **+X** = robot right, **+Y** = forward (toward the forks), **+Z** = up. **Origin O** = the floor point under the centre of the chassis box footprint (mid-width, mid-length of the tub, not counting wedges or forks).
- **Front** = the end with the two eye-sticker wedges and the forks. **Rear** = the end the arm and disc point to when at rest.
- Left/right are the robot's own. In AWS72/74 the robot's **right** side faces the camera (wheels on image left). In AWS76 the robot's **left** side faces the camera.
- Arm angle **α** is measured in the YZ plane from the **−Y (rearward) horizontal**, positive upward. α = 0° is the arm lying flat pointing backward; α = 90° is vertical; α = 180° is pointing forward (the strike position).

| ID | Part |
|---|---|
| CH | chassis tub (lower box, black in AWS72, dark green in AWS74/76) |
| LD-L / LD-C / LD-R | top lids: left, centre (under the arm hub) and right |
| SW | power switch (AWS72, silver slide switch) / power link (AWS74, white 2-pin plug) |
| SLT | slot in the centre lid behind the arm gear |
| WD-L / WD-R | front wedge modules (left and right), each with an eye sticker |
| EYE-L / EYE-R | white/black eye stickers on the wedge faces |
| HL-L / HL-R | round holes in the wedge faces |
| FK-LO, FK-LI, FK-RI, FK-RO | the four forks (left outer, left inner, right inner, right outer) |
| WH-FL, WH-RL, WH-FR, WH-RR | four yellow speckled wheels |
| HB-L / HB-R | wheel hubs (dark green inserts) |
| PB-1 / PB-2 | arm pivot bearing blocks (black cylinders on the lid) |
| GR | arm spur gear on the pivot shaft |
| AS | arm pivot shaft (hidden steel, guess) |
| AR | arm tube (black, from hub to disc motor) |
| AC | arm root clamp (printed, joins AR to the pivot) |
| WR | weapon motor wires (black, taped along the arm) |
| WT | electrical tape / heat-shrink on the arm |
| MM | weapon motor mount (black printed cup at the arm tip) |
| WM | weapon brushless outrunner motor |
| DS | yellow/green disc with hooked tooth/teeth |
| DS-S | 4 black screws clamping the disc to the motor bell |
| FT | rest foot / skid under the weapon head (AWS76, black L bracket) |
| S-WD | screws on the wedge faces |
| S-LD | screws on the lids |
| AM | arm drive actuator (hidden: servo or geared motor with pinion, guess) |
| DM-x | drive gearmotors (hidden, guess) |
| BAT, RX, ESC-D, ESC-W | battery, receiver, drive ESC, weapon ESC (hidden, guess) |

---

## 1. Overall description in one paragraph

Ablation is a **low four-wheel box** with a **double-wedge, four-fork front** and a **swinging arm on top that carries a small spinning disc**. The chassis tub is about 66 mm wide, 58 mm long and 20 mm tall, closed by three printed lids held with small black and silver screws. Four **yellow, green-speckled solid wheels** (about Ø 29 × 9 mm) sit fully outboard, two per side, nearly touching each other fore-aft; there are **no wheel guards**. The front is two separate **trapezoidal wedge blocks** side by side, each about 33 mm wide, whose sloped faces carry a big white **eye sticker**, a round hole and three or four screws. From the bottom edge of each wedge two **forks** project forward about 28 mm to chisel tips on the floor. In the middle of the top, two black **cylindrical bearing blocks** hold a horizontal transverse shaft with a black **spur gear** on it; a **black tube arm** about 50 mm long leaves this hub toward the rear and upward. At the end of the arm is a black **printed motor cup** holding a **brushless outrunner**, and bolted to the outrunner bell is a **pale-yellow/green disc** (about Ø 32 mm) with one or two **sharp hooked teeth**. The weapon wires run back along the arm under black tape and enter the chassis through a hole in the lid. When the arm is driven, it rotates about the transverse shaft, swings up over the chassis and brings the spinning disc down onto the area above the forks.

---

## 2. Part-by-part description

### 2.1 Chassis tub (CH)
- **Shape**: a rectangular open-top box. Plan **66 mm wide (X) × 58 mm long (Y)**, wall height **18 mm**, floor **2 mm**, giving a tub top at **z ≈ 20 mm** when the floor is at z ≈ 2 mm (ground clearance about 2 mm **(guess)**). Edges are sharp, with small bevels of about 0.5 mm. Fine horizontal layer lines (0.15–0.2 mm) wrap the walls.
- **Side walls**: plain, about **2 mm** thick, flat between the wheels. In AWS76 the left side shows a **lower band** (the tub wall) and an **upper band** (the lid overhang/lip) separated by a fine seam at z ≈ 18 mm. The side wall sits about 1–2 mm inside the wheel inner faces.
- **Front wall**: hidden behind the wedge modules; visible only in the V-notch between WD-L and WD-R (AWS72/74), where a vertical black face shows at x ≈ 0, z 3–20.
- **Rear wall**: not photographed. In AWS76 a short stretch of the rear-left corner is visible: a plain vertical face with the left lid overhanging it slightly **(guess for the rest)**.
- **Colour/material**: matt black PLA/PETG (AWS72) and dark-green PLA/PETG (AWS74/76). The surface texture and lack of gloss suggest PLA or PLA+, or matte PETG **(guess)**. Visible white scuffs and nicks on the lids in all three photos.
- **Internal features (guess)**: four corner posts Ø 5 mm with M2 pilot holes for the lid screws; a pair of drive-motor cradles low on each side; a raised central cradle for the arm actuator; a front cross-wall (the front wall) with screw bosses for the wedge modules.

### 2.2 Top lids (LD-L, LD-C, LD-R)
- **Layout**: the top is closed by **three plates**. Seen in all photos as three rectangles separated by fine seams:
  - **LD-R** (robot right, near camera in AWS72/74) spans x ≈ +8 to +33, y ≈ −29 to +29. About **25 × 58 × 2 mm**. It carries the **switch/link SW** near its middle-rear.
  - **LD-L** (robot left) mirrors it at x ≈ −33 to −8. In AWS76 it shows a **small slot with black wires coming up** at x ≈ −12, y ≈ −5 (the weapon wire exit) and two screws.
  - **LD-C** (centre) is a narrower plate, about **16 × 58 × 2 mm**, at x ≈ −8 to +8. It is set **1–2 mm lower** than the side lids (AWS72 shows a step at its edges) and carries the **pivot bearing blocks PB** and the **slot SLT**.
- **In AWS72** the right lid looks like it rises in two levels: a raised panel over the front half (y 0 to +29) and a slightly lower panel behind. The seam runs across at y ≈ 0, so the right "lid" may be two plates (front 25 × 29, rear 25 × 29) **(uncertain)**.
- **Fasteners (S-LD)**: small **pan-head Phillips screws**, head Ø about 3.5–4 mm (M2). Positions counted:
  - AWS72: a **silver** screw at the right lid's front-outer corner (x +30, y +27); **black** screws at the right lid's rear-inner corner (x +10, y −26), mid-inner (x +10, y +3) and at the front-inner corner (x +10, y +26); on the left lid a silver screw at the rear-outer corner (x −30, y −26) and a black one at the front-inner corner.
  - AWS74: same pattern, with two black screws side by side at the centre lid front corners (x ±7, y +26).
  - AWS76: four black screws visible on the left lid: rear-outer, front-outer (x −30, y +24), front-inner, and one at the inner mid point beside the wire slot.
  - Total **about 10 lid screws**, a mix of silver (older) and black (replacement) heads.
- **Colour**: the same as the tub.

### 2.3 Power switch / link (SW)
- **AWS72**: a **silver miniature slide switch**, body about **12 × 5 mm** in plan, recessed in a rectangular pocket in the right lid at about **x +18, y −6**, its long axis along X. A raised black printed bezel about 1 mm tall surrounds it. The slider knob is a small silver tab about 2 mm.
- **AWS74**: in the same place there is a **white plastic 2-pin JST-PH/XH style housing**, about **7 × 4 mm**, flush with a small round-cornered recess. This is a **removable power link** (the plug is the switch) **(guess)**.
- **AWS76**: not visible (it is on the far right lid).

### 2.4 Slot in the centre lid (SLT)
- **AWS72** shows a long dark **rectangular slot**, about **6 mm wide × 18 mm long**, directly behind the gear at x ≈ 0, y −8 to −26, with a black part visible inside (the drive pinion or a lever) **(guess)**. AWS74 shows the slot behind the gear partly filled with **black wires** that curl out at its rear end and loop back down.
- **Function (guess)**: clearance for the gear teeth that engage a drive pinion below the lid, and the exit for the weapon motor wires.

### 2.5 Wedge modules (WD-L, WD-R)
- **Shape**: each is a **trapezoidal prism** (a doorstop with the top cut flat). Section in the YZ plane:
  - **Back face**: vertical, against the chassis front wall at y = +29, height **24 mm** (it stands about **4 mm above** the lid top line).
  - **Top face**: a flat strip **4–5 mm** deep (y +29 to +33.5) at z ≈ 24.
  - **Front face**: a plane sloping down and forward at **about 60° above the floor**, from (y +33.5, z 24) to the toe line at (y +47, z 1).
  - **Bottom**: flat at z ≈ 1, from y +29 to +47 (about **18 mm deep**).
- **Width**: each **33 mm**, WD-L at x −33 to −0.5 and WD-R at x +0.5 to +33, so the pair spans the full chassis width. Between them there is a **V-notch**: their inner side walls are slightly chamfered so a small gap of **about 1 mm at the back opening to 3–4 mm at the toe** shows the front wall. In AWS76 the two wedges look like they touch along the top, with a valley between them.
- **Side walls**: flat, vertical, triangular-trapezoid, flush with the tub side walls; in AWS76 the outer wall of WD-L shows a **bottom flange/lip** about 2 mm thick that runs forward and becomes the outer fork (see FK-LO).
- **Holes (HL)**: one **round hole Ø 5–6 mm** on each wedge face, low and inboard of centre, at about **z 8, x ±12** on the face. AWS76 shows **two** round holes stacked on the left wedge face (one high near the eye, one low) plus an **oval recess** — possibly for a fork-retaining screw or simply lightening/sticker gaps **(guess)**. The low hole lines up with the fork shank behind it, so it is likely **access to a grub screw clamping the fork** **(guess)**.
- **Screws (S-WD)**: black pan-head Phillips, head Ø 3.5 mm. On each wedge face: **one near each top corner** (x ±3 and ±30 from the wedge's inner/outer edges, about 4 mm below the top edge) and **one at the bottom outer corner** just above the outer fork. AWS72 shows 3 per wedge; AWS74 shows 3–4. They fasten the wedge back into bosses on the chassis front wall **(guess)**.
- **Eye stickers (EYE)**: on each sloped face, high and slightly outboard of centre, a white **almond/shield-shaped eye** about **14 mm wide × 12 mm tall**, with a thick black outline, a white sclera ring, and a **black vertical oval pupil** (about 4 × 7 mm) with a white highlight. In AWS76 the sticker is a **rounded shield/eye** of similar size, both facing forward. These are vinyl decals, cosmetic.
- **Colour**: same as the chassis (black → dark green).

### 2.6 Forks (FK-LO, FK-LI, FK-RI, FK-RO)
- **Positions**: four forks, two per wedge, at the **wedge bottom corners**: x ≈ **−30, −4, +4, +30**. The inner pair are close together either side of the V-notch (gap between them about **7 mm**), the outer pair are flush with the chassis sides.
- **AWS72 / AWS74 form (steel bars)**:
  - A straight **rectangular bar about 3 mm wide × 2 mm tall** (it may be 3 mm square), emerging from the bottom of the wedge front face at about **z 1–3**, and running forward **horizontally and very slightly down** to touch the floor at the tip.
  - **Visible length** from the wedge toe to the tip: about **28 mm**. The bar continues inside the wedge (the shank is hidden, about **15 mm** of embedment, **guess**).
  - **Tip**: a ground **chisel**: the top face is bevelled down over the last **5–6 mm** at about **20–25°** to a sharp edge on the floor, giving a small bright triangular facet. Viewed from above, the tip is square-ended.
  - **Colour**: AWS72: dull grey steel shank with bright ground tip. AWS74: shank coloured **green** (likely paint, dye or green tape), tip bright.
- **AWS76 form (flat plates)**:
  - **Outer forks FK-LO/FK-RO**: a flat plate about **1.5 mm thick** lying horizontal. At its root it is **as wide as the wedge's side flange** and merges with a **flat base plate under the wedge** (the plate runs under the whole wedge bottom and out at the side, with a **small step/notch** at the wedge toe). Forward of the wedge it narrows to about **6 mm wide**, runs about **30 mm** to the tip, where it **kinks upward** into a short **barb** (about 3 mm tall, 4 mm long) forming a hook pointing back.
  - **Inner forks FK-LI/FK-RI**: narrower strips, about **4 mm wide × 1.5 mm thick**, about **26 mm** long beyond the toe, with the same upturned barb at the tip. They appear slightly higher than the outer forks (about z 2–3 at the root, sloping down to the floor at the tip).
  - **Colour**: green faces, a lighter dusty edge, with a black speckled/scuffed bottom face. Looks like **green FR4/G10 fibreglass** or **green-printed plastic with a sanded surface (guess)**.
- **Fixing**: the forks pass **into or under the wedge bottoms**. Most likely they sit in slots moulded into the wedge bottoms and are clamped by the wedge screws, or by a grub screw through the face hole HL **(guess)**.

### 2.7 Wheels (WH-FL, WH-RL, WH-FR, WH-RR)
- **Shape**: solid discs, **Ø 29 mm × 9 mm wide**, with a **flat tread** (no visible pattern) and slightly rounded tread edges (radius about 1 mm). The outer face is flat with a **recessed hub**.
- **Material/colour**: a **yellow/lime foam-like or TPU tyre** with **dark green speckles and smears** across the faces: it looks like **yellow TPU printed over a dark green core**, or **cast polyurethane/silicone** with green pigment flecks. The yellow is matt and slightly rough.
- **Hub (HB)**: a dark green insert Ø about **13–15 mm** on the outer face, with **6 small holes** around a central hole (AWS72 shows a six-petal pattern on the rear-right wheel). At the centre there is a **black socket-head or pan-head screw** about Ø 4 mm, clamping the wheel to the motor shaft/hub adaptor.
- **Positions (centres)**: x **±41.5** (inner face at ±37, outer face at ±46), z **14.5**. Fore-aft: WH-F at **y +16**, WH-R at **y −16**, so the **wheelbase is about 32 mm** and the tyre-to-tyre gap fore-aft is about **3 mm** (they very nearly touch in every photo).
- **Vertical relation**: wheel top z 29 vs lid top z 22 → the wheels stick **7 mm above the lids**; wheel bottom z 0 vs tub floor z 2 → **2 mm below the floor**. So the robot **can drive inverted** on its wheels, though the arm hub (z ≈ 32) and wedges complicate it (see 13).
- **Front wheels vs wedges**: the front wheels' front edge is at y +30.5, i.e. **level with the wedge back face**; the wedges do not cover the wheels (they are inboard of them), so the front wheels are exposed at the front corners.
- **No wheel guards** of any kind are present; there are **no guard-to-chassis supports** and no external motor mounts. The wheel inner faces sit about **4 mm** outboard of the tub side wall, so a short shaft or hub spacer is exposed in that gap (dark, not detailed in the photos).

### 2.8 Arm pivot hub: bearing blocks (PB-1, PB-2), spur gear (GR), shaft (AS)
- **Bearing blocks PB**: two black **cylinders lying on their sides** (axis along X), each about **Ø 12 mm × 7 mm long**, standing on short printed pedestals fixed to the centre lid. Hub axis at about **z 31, y −6**.
  - PB-1 (robot right, near camera in AWS72/74) shows an **end face with a central hole Ø 3 mm** (the shaft end) and a smaller dark spot (a grub screw or a 2nd pin).
  - PB-2 (robot left) is similar; in AWS76 a **silver pan-head Phillips screw** is visible on its outer end face, at the shaft centre, so the shaft is retained by an **end screw into the shaft or a printed cap** **(guess)**.
- **Gear GR**: a black printed **spur gear**, **Ø about 17 mm over the tips**, **10–11 teeth**, face width **5 mm**, on the shaft **between the bearing blocks**, slightly right of centre (x ≈ +3). Its teeth stand clearly above the hub cylinders. In AWS72/74 its lower teeth disappear into the lid slot SLT region: the meshing pinion is below the lid. In AWS76 a **second, finer gear/sprocket** shows on the left of the hub at the same axis (the edge of the gear seen at an angle, or a separate drive gear) **(uncertain)**.
- **Arm root clamp AC**: the black arm tube enters the hub on the **rear side** between the bearing blocks; in AWS72/74 its end is wrapped by a black printed collar about Ø 10 × 8 mm fixed to the shaft. In AWS76 a black printed **clevis** with checker-texture (carbon-look print) around the gear holds the arm root.
- **Overall hub envelope**: about **30 mm wide (X) × 16 mm deep (Y) × 14 mm tall**, from the lid at z 22 to the gear top at z ≈ 40.

### 2.9 Arm (AR), tape (WT), wires (WR)
- **Shape**: a **straight black tube/rod**, about **Ø 8–9 mm**, **50 mm** long from the pivot axis to the weapon motor axis. In AWS72 it rises at **α ≈ 35°** from the rear horizontal; in AWS74 **α ≈ 25–30°**; in AWS76 **α ≈ 15–20°** (nearly flat, with the disc behind the robot and the foot FT touching the floor or just above it).
- **Construction**: near the hub the arm is a **black printed square-ish beam** about 9 × 9 mm with a checker texture (AWS76), changing to a **round black tube** wrapped in **black electrical tape** for the outer two-thirds. The tape bulges and wrinkles (it is binding the three motor wires to the tube). In AWS72 a thicker black **heat-shrink sleeve** about Ø 10 mm covers the middle third, with a step where it ends.
- **Wires WR**: three weapon-motor phase wires (black) run along the **underside/left of the arm**, under the tape, from the motor to the hub, where they leave the arm and **dive into the lid slot** (AWS74) or **the left-lid wire slot** (AWS76), with a loose loop of about 10 mm slack to allow arm rotation. AWS76 shows the wires as a **twisted black bundle**, about Ø 4 mm, standing up from the lid at x −12, y −5, then curving back to the arm root.
- **Material (guess)**: carbon-fibre tube Ø 8 mm (light, stiff) wrapped in tape, or an aluminium tube; the printed root section is PLA/PETG.

### 2.10 Weapon motor mount (MM) and motor (WM)
- **MM**: a black printed **cup/disc-shaped mount**, about **Ø 24 mm × 8 mm**, fixed to the arm tip with its axis along **X**. Its outer face (AWS76) shows a **cross of 4 small holes** around a centre hole (motor-mounting M2 screws on a 12 or 16 mm pattern). In AWS72 the left side of the mount shows a **square printed flange** with **4 small silver screw heads** at its corners and a dark centre.
- **WM**: a **brushless outrunner**, about **Ø 22 mm × 12 mm** (2204/2205 class) **(guess on size)**. In AWS72 the **copper windings** (orange-brown) are visible through the gap between the mount and the disc, so it is an outrunner with the stator on the mount and the bell carrying the disc.
- **Axis position at rest**: about **(x 0, y −62, z 46)** in AWS72's raised pose; with α ≈ 20° (AWS76) about **(0, −53, 46)**... see the math in §10.

### 2.11 Disc (DS) and disc screws (DS-S)
- **Shape**: a **flat disc** about **Ø 32 mm × 2 mm thick**, its plane parallel to **YZ** (spin axis along X). On the rim there are **hooked teeth**: AWS72 shows **one large hook** with an **inner triangular cut-out** (a long kidney/triangle slot about 10 × 4 mm) that projects about **8 mm** beyond the disc circle and ends in a sharp point curving in the direction of rotation. AWS76 shows the **hook at the rear-top** curving upward with a **sharp beak-like tip** and a **counterweight/second tooth bump** on the opposite side (the json says 2 teeth). So: **2 teeth, one large hook and one smaller balancing tooth**, or two equal hooks **(uncertain)**.
- **Colour/material**: **pale yellow-green** with a slightly glossy, semi-translucent edge. AWS72 shows a bright **metallic gold/brass-coloured edge** on the hook. So: **anodised/painted aluminium** or **gold-coloured hardened steel** with a yellow-green paint face **(guess)**; it could also be **yellow FR4/G10**, which would explain the colour (but FR4 is a poor weapon material, so metal is more likely).
- **Fixing DS-S**: **4 black Phillips/hex screws**, head Ø 3 mm, on a circle of radius about **11 mm** (AWS76, at 12, 3, 6 and 9 o'clock, slightly rotated), going through the disc into the motor bell.
- **Spin direction (guess)**: the hook tips point in the direction of travel at the **top** of the disc when it is **striking forward**, so that when the arm comes down onto an opponent, the tooth bites downward-forward.

### 2.12 Rest foot (FT), AWS76
- A **black L-shaped bracket** under the weapon head: a vertical leg about **4 mm wide × 14 mm tall** dropping from the bottom of the motor mount at about y −58, ending in a short horizontal **toe** about **10 mm long** pointing forward along the floor. It acts as a **skid** that rests on the floor when the arm is lowered to the rear, so the spinning disc stays **2–3 mm above the floor** and the arm load goes through the foot, not the actuator. Not visible in AWS72/74 (the arm there is raised, and the foot may be hidden behind the disc, or it was added later) **(uncertain)**.

### 2.13 Hidden arm actuator (AM) and drive (DM) **(guess)**
- **AM**: a **high-torque micro servo** or a **micro gearmotor** (N20 class, high reduction) lying under the centre lid, driving a **pinion** that meshes with GR through the lid slot. Given that the arm swings a ~30 g head over 50 mm, a servo with a 1:1 or 1:2 gear pair is plausible. Gear ratio: GR 10–11 teeth on the arm; pinion probably similar or smaller.
- **DM**: four **N20 gearmotors**, one per wheel, shafts at z 14.5, or two motors driving front/rear wheels through internal gears. With wheels nearly touching, **4 motors** in two transverse pairs is the likely layout.

### 2.14 Electronics (hidden, guess)
- 2S LiPo 180–300 mAh, a small receiver, a dual brushed drive ESC, a small brushless weapon ESC (10–12 A), and the arm servo/actuator signal line. The switch/link SW on the right lid is the only external electrical part besides the weapon wires.

---

## 3. Per-view sections (for silhouette matching)

### 3.1 AWS72 (front-right iso, raised arm)
- **Bottom right**: four forks fanned out toward the viewer, each a thin grey line ending in a bright chisel triangle. Fork tips at about (775, 1000), (910, 850), (1045, 745) and (1160, 640) px.
- **Middle**: two black sloped wedge faces each with a white eye and a hole, joined at a V-notch. The near (right) wedge spans about x 390–690, y 520–840 px; the far (left) wedge about x 690–930, y 360–640 px.
- **Left**: the right-side wheels: rear-right at about x 50–200, y 525–670; front-right at x 225–385, y 585–765. Yellow with green speckled hubs, black centre screws.
- **Top**: three lids, the **silver slide switch** on the right lid at (315–405, 485–505), the **black gear hub** at (360–500, 320–470), the **slot** behind it, and the arm rising to the top-left to the **weapon head** at (95–275, 40–360): black printed mount with copper windings showing, gold/yellow disc with a big hook and triangular cut-out pointing up.
- Visible far-side wheels (left side) peek over the lids at (520–600, 255–295) and (700–790, 315–355).

### 3.2 AWS74 (front-right iso, slightly more frontal)
- Same layout as AWS72. Differences: chassis dark green; fork shanks green; the switch is a **white plug**; wires visibly loop out of the slot behind the hub; the arm is a little lower (α ≈ 28°); the disc is seen almost edge-on as a **yellow ellipse** at the top-left (130–310, 50–200) px with its black mount face (4-hole pattern) toward the camera.

### 3.3 AWS76 (front-left iso, arm low)
- **Left half**: the two wedges from the left, eye stickers (shield-shaped), round holes, and the four **green plate forks** reaching out to the image left. Outer-left fork at the bottom from about (95, 720) to (560, 640); inner forks at (205, 425)–(430, 395) and (230, 500)–(470, 470); the far outer fork at (40, 330)–(330, 290).
- **Right half**: left side of the chassis: a long low box with the lid seam, and the two left wheels at (685–830, 420–560) and (870–1025, 385–520) px, faces toward the camera, both with central screws and smeared green hubs.
- **Top right**: the hub with gear and **silver screw** on PB-2 at (600–735, 150–270), the wire bundle from the lid at (705–760, 220–310), the arm running to the upper right, and the **weapon head**: disc face-on, Ø about 190 px, centred near (1000, 110); the black motor cup with 4-hole cross; the hook tip at (1170, 80); the black **foot FT** below at (955–1045, 190–250).

### 3.4 Top view (plan, synthesised)
- A 66 × 58 mm rectangle (tub + lids) with four 29 × 9 mm wheels outboard, nearly touching fore-aft. In front, two 33 × 18 mm wedges (sloped faces) and four 28 mm forks. Total length tip-of-forks to tub rear about **104 mm** (see §13). The arm runs from the hub at y −6 back along the centreline to the disc, which projects about **20–50 mm behind the tub** depending on α.

### 3.5 Front view
- Floor line: four fork tips at x −30, −4, +4, +30. Above: two sloped wedge faces (each 33 wide, 24 tall), eyes, holes, screws. Behind and above the wedges: the wheel tops (7 mm above the lids) on both sides, the hub and gear on the centreline (to z 40) and, behind it, the disc edge-on as a vertical line (2 mm wide, 32+8 mm tall) on the centreline.

### 3.6 Left side view
- A low rectangle (58 × 22) with two Ø 29 wheels covering most of it, the wedge triangle-trapezoid (24 tall, 18 deep) at the front, forks ahead to y ≈ +75. The arm rises from the hub at (y −6, z 31) to the rear; the disc circle Ø 32 at the arm tip, with its hook tooth.

### 3.7 Rear view (not photographed, inferred)
- The tub rear wall, wheels at both sides, the disc edge-on in the middle (in rest pose low behind the robot), the foot under it. A charge port or second link may be here **(guess)**.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| CH | open box | 66 × 58 × 20 | 1 × 0.88 × 0.30 | black / dark green FDM | — | 1 |
| LD-L/R | flat plate | 25 × 58 × 2 | 0.38 × 0.88 | same | 3–4 × M2 pan | 2 |
| LD-C | flat plate | 16 × 58 × 2 | 0.24 × 0.88 | same | 2 × M2 pan | 1 |
| SW | slide switch / plug | 12 × 5 × 5 / 7 × 4 | — | silver / white | pocket in LD-R | 1 |
| SLT | slot | 6 × 18 | — | — | — | 1 |
| WD | trapezoid prism | 33 × 18 × 24 | 0.50 × 0.27 × 0.36 | same as chassis | 3–4 × M2 | 2 |
| EYE | sticker | 14 × 12 | 0.21 | white/black vinyl | adhesive | 2 |
| HL | round hole | Ø 5–6 | — | — | — | 2–4 |
| FK (72/74) | chisel bar | 3 × 2 × 43 (28 visible) | 0.65 | steel (green-painted in 74) | slot in WD (guess) | 4 |
| FK (76 outer) | barbed plate | 6 × 1.5 × 30 + base | 0.45 | green FR4 (guess) | under WD | 2 |
| FK (76 inner) | barbed strip | 4 × 1.5 × 26 | 0.39 | green FR4 (guess) | under WD | 2 |
| WH | solid wheel | Ø 29 × 9 | 0.44 × 0.14 | yellow TPU/PU with green core | centre screw | 4 |
| HB | hub insert | Ø 14 | 0.21 | dark green | — | 4 |
| PB | bearing cylinder | Ø 12 × 7 | 0.18 | black FDM | integral to LD-C / screws | 2 |
| GR | spur gear, 10–11 T | Ø 17 × 5 | 0.26 | black FDM | on AS | 1 |
| AS | shaft | Ø 3 × 30 | — | steel | end screw | 1 |
| AC | root clamp | 10 × 10 × 8 | — | black FDM, checker | on AS | 1 |
| AR | tube | Ø 8.5 × 50 | 0.76 | carbon/alu + tape | AC/MM | 1 |
| WR | 3 wires | Ø 1.2 each | — | black silicone | taped | 3 |
| MM | motor cup | Ø 24 × 8 | 0.36 | black FDM | 4 × M2 | 1 |
| WM | outrunner | Ø 22 × 12 | 0.33 | copper/black | MM | 1 |
| DS | hook disc | Ø 32 (+8 tooth) × 2 | 0.48 | yellow-green metal | 4 × M2 | 1 |
| FT | L foot | 4 × 14 + 10 toe | — | black FDM | MM | 1 (AWS76) |
| S-WD | pan Phillips | head Ø 3.5 | — | black | into chassis | 6–8 |
| S-LD | pan Phillips | head Ø 3.5–4 | — | black / silver | into posts | ~10 |

---

## 5. Contact / gap matrix (est. mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| LD-L/C/R ↔ CH wall tops | rest on, screwed | 0 |
| LD-L ↔ LD-C ↔ LD-R edges | side by side | 0.3–0.5 seam |
| WD back ↔ CH front wall | screwed | 0 |
| WD-L inner ↔ WD-R inner | V-notch | 1 (top) – 4 (toe) |
| WD bottom ↔ floor | above | 1 |
| FK root ↔ WD bottom | clamped / slotted | 0 |
| FK tip ↔ floor | touching | 0 |
| FK-LI ↔ FK-RI | side by side | ~7 |
| FK-LO outer edge ↔ CH side plane | flush | 0 |
| WH inner face ↔ CH side wall | gap (shaft/spacer) | ~4 |
| WH-F tyre ↔ WH-R tyre | fore-aft | ~3 |
| WH-F front ↔ WD back plane | in line | 0 (y), but 4 mm outboard in x |
| WH top ↔ lid top | wheel above | +7 |
| WH bottom ↔ CH floor | wheel below | +2 |
| PB ↔ LD-C | integral / screwed | 0 |
| GR ↔ PB inner faces | side by side | 0.5–1 |
| GR teeth ↔ hidden pinion | meshing through SLT | 0 |
| AC ↔ AS | clamped | 0 |
| AR ↔ AC, AR ↔ MM | inserted / glued | 0 |
| WR ↔ AR | taped | 0 |
| WR loop ↔ lid slot | passes through | 0 |
| WM ↔ MM | screwed | 0 |
| DS ↔ WM bell | screwed (4) | 0 |
| DS rim ↔ MM | rotating clearance | 1–2 |
| FT toe ↔ floor (arm at rest) | resting | 0 |
| DS bottom ↔ floor (arm at rest) | above | 2–3 |
| DS ↔ CH rear wall (arm at rest) | behind | 5–8 |
| DS ↔ fork tips (arm at strike) | above | 0–10 (depends on opponent) |

---

## 6. Mechanism

1. **Drive**: four-wheel skid steer, solid yellow wheels, invertible within limits (see 13.6).
2. **Weapon spin**: a brushless outrunner spins the hooked disc directly (no belt). With a 2204-class motor at about 2S (7.4 V) and roughly 2300 KV, the no-load speed is about 17 000 rpm, tip speed about **(π·0.040 m·17 000/60) ≈ 36 m/s** **(guess)**.
3. **Weapon swing**: the hidden actuator turns GR, which rotates the shaft AS and the arm clamp AC. The arm swings from the rest pose (α ≈ 15–20°, disc behind, foot on floor) through vertical (α = 90°) to the strike pose (α ≈ 160–170°), where the disc comes down onto the top of an opponent held on the forks. The disc tip at α = 180° is at y ≈ −6 + 50 + 20 = **+64**, which matches the fork reach (tip y ≈ +75, root y +47): the disc lands **above the middle of the forks**. This is the defining design relation of Ablation.
4. **Forks**: passive, they get under the opponent, lift its edge 1–3 mm, and hold it in the strike zone.

---

## 7. Assembly order (suggested rebuild)

1. Print **CH** with posts, motor cradles and the actuator cradle.
2. Install **4 drive gearmotors**, shafts out through the side walls at z 14.5, y ±16. Fit hub adaptors and the **wheels**, fix with the centre screws.
3. Install the **arm actuator AM** (servo or gearmotor + pinion) under the centre.
4. Install the battery, receiver, ESCs and wiring; mount the **switch/link SW** in the right lid.
5. Screw on **LD-L** and **LD-R** (about 8 screws), then **LD-C** carrying **PB-1/PB-2**.
6. Assemble the arm: **AR** into **AC**; slide **AS** through PB-1, **GR**, **AC**, PB-2; fix the end screw. Check the GR–pinion mesh through SLT.
7. Screw **WM** into **MM**, fix MM (+ foot FT) to the arm tip, bolt **DS** to the bell with 4 screws.
8. Route **WR** along the arm, tape it (WT), leave a slack loop at the hub, pass through the slot to the weapon ESC.
9. Slide the **forks** into the wedge bottoms (or lay the AWS76 base plates under them), screw the **wedges WD** to the chassis front wall, tighten the fork grub screws through **HL** **(guess)**.
10. Apply the **eye stickers**.

---

## 8. Hidden / uncertain list
- Actuator type (servo vs gearmotor) and pinion size; whether there is a second gear (AWS76).
- Whether the right lid is one or two plates.
- Disc tooth count (1 big hook visible vs json's 2) and material.
- Fork fixing method (slots + grub screw vs clamp under wedges).
- Foot FT presence in AWS72/74.
- Rear wall content.
- All mm values ±15%.

---

## 9. Coordinate frame (restated)
- Origin O on the floor under the centre of the tub footprint. +X right, +Y forward, +Z up, mm. α measured from −Y horizontal, upward positive, in the YZ plane.
- Tub: x ∈ [−33, +33], y ∈ [−29, +29], z ∈ [2, 20]; lids to z 22.
- Wedges: x ∈ [−33, +33], y ∈ [+29, +47], z ∈ [1, 24].
- Forks: y ∈ [+47, +75] beyond the toe (AWS72/74).
- Wheels: centres (±41.5, ±16, 14.5), Ø 29, width 9.
- Pivot axis: line x ∈ [−15, +15] at (y −6, z 31).

## 10. Profiles as math

**10.1 Wedge WD section (YZ, constant over its 33 mm width).** Polygon (y, z): (29, 1) → (47, 1) → (33.5, 24) → (29, 24) → close. Front face line: z = 1 + (47 − y)·tan 59.6°, i.e. z = 1 + 1.70·(47 − y) for y ∈ [33.5, 47]. Face angle atan(23/13.5) = **59.6°** above the floor.

**10.2 V-notch.** Inner side planes of the wedges: x = ±(0.5 + 0.17·(y − 29)) for y ∈ [29, 47], giving a notch half-width 0.5 at the back and 3.5 at the toe.

**10.3 Steel fork (AWS72/74), side profile (YZ).** Bar bottom z = 0.04·(75 − y) for y ∈ [47, 75] (a 1.1 mm drop over 28 mm: the tip touches the floor). Bar top z_top = z_bottom + 2 for y ∈ [47, 69]; chisel top z_top = 2·(75 − y)/6 + z_bottom for y ∈ [69, 75] (a ~18° bevel).

**10.4 AWS76 plate fork, side profile (YZ, thickness 1.5 mm).** Lower edge z = 0 from y 47 to 77; barb: line from (77, 0) up to (79, 3), then back to (75, 1.5) — a triangle hook with its point facing −Y. Plan outline of the outer fork: half-width w(y) = 3 for y ∈ [50, 79]; w grows linearly to the full wedge-side flange width 6 over y ∈ [47, 50].

**10.5 Arm centreline.** P(α) = (x 0, y −6 − 50·cos α, z 31 + 50·sin α). Rest (α 18°): (0, −53.6, 46.5). AWS72 pose (α 35°): (0, −47, 59.7). Vertical (α 90°): (0, −6, 81). Strike (α 170°): (0, +43.2, 39.7).

**10.6 Disc outline (in its own XZ'-plane, polar about the motor axis).** Base circle r₀ = 16. Hook tooth: for φ ∈ [0, 50°], r(φ) = 16 + 8·(φ/50°)^1.5 (a growing spiral flank), then a near-radial back face from r = 24 at φ = 50° to r = 16 at φ = 56°. Second (balance) tooth at φ + 180° with a smaller amplitude: r(φ) = 16 + 4·(φ'/40°)^1.5 for φ' ∈ [0, 40°]. Lightening slot (AWS72): a triangle with vertices at polar (r 13, φ 10°), (r 20, φ 40°), (r 13, φ 40°). Bolt circle: 4 holes Ø 2.2 at r = 11, φ = 0/90/180/270°.

**10.7 Wheel.** Cylinder r = 14.5, width 9, edge fillet 1; hub recess r = 7, depth 1; six holes Ø 1.8 at r = 4.5, φ = k·60°.

**10.8 Gear GR.** 10 teeth, module m = 1.5: pitch Ø 15, tip Ø 18, root Ø 11.25. Involute approximated as trapezoid teeth: tip width 1.2, root width 2.6.

**10.9 Hub cylinders PB.** Circles r = 6 about (y −6, z 31), extruded x ∈ [−15, −8] and [+8, +15]. Pedestals: rectangles 12 (Y) × 9 (Z) from z 22 to 31 under each.

## 11. Pixel-based measurements (independent check)

**AWS72** (1200 × 1019):
- Front-right wheel: 160 px wide × 180 px tall (ellipse; the vertical axis ≈ true Ø since the wheel faces sideways-toward camera). Rear-right wheel: 150 × 145 (farther).
- Near wedge face: width along its toe edge from (395, 840) to (690, 760) ≈ 305 px; height from toe to top edge ≈ 280 px along the face.
- Fork visible length (near outer): from (520, 850) to (775, 990) ≈ 290 px.
- Weapon head: disc ellipse long axis ≈ 330 px (disc + hook), mount Ø ≈ 110 px.
- Hub: gear tip Ø ≈ 75 px; bearing cylinder Ø ≈ 75–80 px.

**AWS74** (1200 × 963): front-right wheel 140 × 190 px; near wedge toe length 330 px; fork visible length ≈ 260 px; disc long axis ≈ 180 px (seen obliquely, short axis ≈ 160).

**AWS76** (1200 × 774): left wheels each ≈ 145 px wide × 140 tall; their centres 185 px apart; side of tub from wedge back (≈ x 690) to tub rear (≈ x 990) ≈ 300 px; disc Ø ≈ 190 px including the motor cup; the outer fork from the wedge toe (≈ 560, 640) to the tip (≈ 95, 720) ≈ 470 px (heavily foreshortened-to-enlarged: it is the nearest object).

## 12. Several independent estimates of key quantities

| Quantity | Method A (rule/scale) | Method B (ratio to D) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Wheel Ø D | 28–30 (typical ant wheel for a 20 mm body) | — | AWS76: 140–145 px vs tub side 300 px → D/L = 0.48 → D ≈ 28 with L 58 | **29** |
| Wheelbase | D + 3 = 32 | — | AWS76: 185 px / 145 px × 29 = 37 (near wheel enlarged) | **32** |
| Tub length | 4 in cube − wedge − forks = 101.6 − 18 − 28 ≈ 56 | 2.0 D = 58 | AWS76: 300/145 × 29 = 60 | **58** |
| Tub width | track 92 − 2·(9+4) = 66 | 2.3 D = 67 | AWS72: wedge pair ≈ 2 × 305 px / 170 px × 29 / 1.25 (obliquity) ≈ 83?? (see 13.2) | **66** |
| Wedge height | lid 22 + 2 | 0.83 D = 24 | AWS72: face 280 px along slope / 170 × 29 = 48 slope → ×sin 60 → 41?? (near-camera inflation) | **24** |
| Fork visible length | 101.6 limit leaves 28 | 1.0 D = 29 | AWS72: 290/170 × 29 = 49; AWS74: 260/165 × 29 = 46 | **28 (photos say 30–45; see 13.3)** |
| Arm length (pivot–motor axis) | must fit 4 in cube when vertical: 101.6 − 31 − 20 ≈ 50 | 1.7 D = 50 | AWS76: hub to disc centre ≈ 330 px / 145 × 29 ≈ 66 (oblique, behind) | **50** |
| Disc Ø (circle) | 30–35 for a 2204 motor | 1.1 D = 32 | AWS76: 190 px incl. hook ≈ 38 incl. hook → circle 32 | **32 (+8 hook)** |
| Gear tip Ø | 15–18 | 0.6 D = 17 | AWS72: 75 px / 170 × 29 = 13 (farther than the wheel) → ×1.25 = 16 | **17** |

## 13. Consistency check: conflicts and reconciliation

1. **Box limit vs fork length.** The photos suggest forks of 30–45 mm, but that plus wedge (18) and tub (58) would give 106–121 mm, exceeding 101.6 mm. Either the forks are shorter than they look (they are the nearest objects in AWS72/74/76, so perspective enlarges them by 20–40%), or the tub is shorter. Weight given to the rule: **forks 28 mm visible, tub 58**, total 104 including the 2 mm chisel overhang… still 2 mm over; so take **tub 56 mm** if a strict cube fit is needed (wheelbase stays 32: wheels overhang the tub ends by 1–2 mm, which matches AWS76 where the rear wheel's rear edge is level with the tub rear). **Reconciled: tub 56–58, forks 26–28.**
2. **Tub width.** Pixel width from AWS72 is inflated by obliquity and near-camera wedges; the 4-inch rule limits the wheel track to ≤ 101.6, and the wheels look like they protrude about 13 mm per side from the tub. 66 + 2 × 13 = 92 mm track. **Reconciled 66.**
3. **Arm length and the strike point.** If the arm were 66 mm (pixel estimate), the disc tip at the strike would reach y ≈ +80, beyond the fork tips; with 50 mm it reaches y +64, the middle of the forks. The designer would put the strike over the forks, so **50 mm** is preferred. It also fits the cube with the arm vertical: 31 + 50 + 20 = 101.
4. **Disc material.** The yellow-green face colour looks like FR4, but the gold metallic edge on the hook (AWS72) indicates metal. **Reconciled: metal (aluminium or steel) with a coloured face.**
5. **Teeth.** AWS72 shows one prominent hook; AWS76 shows the hook plus a second smaller bump; the json says 2. **Reconciled: 2 teeth, unequal (or one hook and one counter-lobe).**
6. **Invertibility.** Wheels reach z 29 vs the hub at z 40 and the arm head above it. Upside down the robot would rest on the **hub/gear**, not on its wheels, unless the arm is swung to lie flat. So Ablation is **not truly invertible**: the arm is also its **self-righting lever** (swinging the arm when inverted pushes the robot back over) **(guess)**.
7. **Forks change between events**: steel bars (72, 74) vs green plates (76). Both are described; a rebuild should pick one event (AWS72 recommended: black chassis, steel forks, raised arm).

---

## 14. Why the designer did it (per part; adversarial lens first)

- **CH low tub (20 mm)**: a low body keeps the centre of gravity down so the swinging arm's reaction does not tip the robot, and gives opposing wedges only a 20 mm face. Spinners can still hit the flat side walls; the walls are plain and replaceable. Construction: one open-top print, no supports.
- **Three lids**: the centre lid carries the hub and can be removed with the arm still assembled; side lids give quick access to the battery and switch. Splitting the top limits damage from a single overhead hit to one plate. Weak point: lid screws into plastic can strip after repeated hammer reaction loads.
- **Switch/link SW on the top**: easy for the driver to reach in the arena, away from the floor and the forks. The change to a plug link (AWS74) removes a switch that could be knocked off by impacts. Exposed on top, so an overhead weapon could hit it; it is recessed to reduce that.
- **Wedge modules WD**: the two steep (≈60°) faces deflect horizontal spinners and opposing wedges up and over; because they are bolt-on modules, a damaged wedge is swapped in one minute. The V-notch between them lets each be printed and replaced separately. Being 4 mm taller than the lids, they shield the lid front edges. They are not low wedges themselves — the getting-under job is given to the forks.
- **Forks FK**: forks get under flat-bottomed opponents and under rival wedges' leading edges better than any printed edge, because a ground steel chisel can be ~0.2 mm off the floor. Four separated prongs make a wide "net" that catches opponents across the full width, and the gaps reduce surface for a spinner to bite. Crucially they hold the opponent **under the hammer's strike point**. Steel survives spinner hits; FR4 plates (AWS76) are lighter and stiffer per gram but chip. Barbed tips (AWS76) stop the opponent from sliding off forward. Weak points: thin forks bend under vertical spinner hits and give leverage for the opponent to lift Ablation's nose.
- **Eye stickers**: identity and showmanship (the robot looks like a creature); none structural.
- **Holes HL**: most likely give a hex key access to fork grub screws, so forks can be replaced without unbolting the wedges.
- **Wheels WH (yellow, outboard, unguarded)**: a large diameter relative to the body (D 29 vs body 22) lets the robot drive on its wheels if flipped onto a side lid line, and gives good grip on pushing. Unguarded wheels are a risk against horizontal spinners, accepted to save weight for the weapon. The near-touching fore-aft placement keeps the wheelbase short so the robot turns quickly to face opponents (essential for aiming forks and a hammer). Bright yellow aids the driver's orientation.
- **Pivot hub (PB, GR, AS)**: placing the pivot near the middle of the robot gives the arm a full 180° sweep from rear rest to front strike. The gear reduction converts the actuator's speed into torque to lift the heavy head. Printed bearing blocks are easy to replace; a steel shaft with end screw survives impacts. Weak point: the gear teeth are exposed on top; a direct overhead hit could strip them.
- **Arm AR (thin tube, taped)**: a tube is stiff for its weight, which matters because the arm mass multiplies swing inertia. Taping the wires along it keeps them from catching opponents' weapons and stops them flapping into the disc. The slack loop at the hub allows rotation. Weak point: the arm sticks out of the 4-in body; a horizontal spinner can hit it in rest pose (behind the robot).
- **Weapon head (MM, WM, DS)**: a direct-drive outrunner removes belts and pulleys (fewer parts to fail). The disc spinning while being hammered down combines impact energy (from the swing) with cutting/tearing energy (from the spin): the hook bites into plastic lids and armour and tears. The large hook tooth bites deep because the disc is small and slow-ish (big bite per revolution). In rest pose behind the robot, the spinning disc also **protects the rear** from rammers. The foot FT keeps the disc off the floor in rest so the robot does not get thrown by its own disc.
- **Rest pose behind the robot**: keeps the centre of mass low and toward the middle while driving; leaves the forks clear to catch.
- **Screws (mixed silver/black)**: evidence of repairs between events (silver originals replaced by black), consistent with a modular, field-repairable design.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre, mm) | Confidence |
|---|---|---|---|---|
| Arm actuator | metal-gear micro servo (e.g. 25 g class) with a printed pinion, or N20 1000:1 gearmotor | 23 × 12 × 26 | x 0, y −6, z 11 under the hub, output axis along X at z ≈ 17 | medium |
| Pinion | 8–10 tooth, m 1.5, Ø 12–15 | Ø 15 × 5 | meshing GR from below through SLT, axis at (y −6, z 17) | medium |
| Drive motors | 4 × N20 (6 V, 300–500 rpm) | 12 × 10 × 25 + shaft | transverse, two pairs at y ±16, z 14.5, x ±20 | medium |
| Wheel hub adaptors | printed or aluminium D-shaft hubs with M2 centre screw | Ø 8 × 6 | in the wheel bores | medium |
| Battery | 2S LiPo 300 mAh | 45 × 17 × 10 | flat in the front half, y +15, z 8 | medium |
| Weapon ESC | 10–20 A brushless ESC | 25 × 12 × 5 | right side, y −15, z 8 | medium |
| Drive ESC | dual brushed micro ESC | 20 × 15 × 5 | left side, y −15, z 8 | low |
| Receiver | small 2.4 GHz | 20 × 12 × 4 | front left, y +18, z 14 | low |
| Fork sockets | 3 × 2 mm slots in the wedge bottoms, 15 mm deep, with M2 grub screws via HL | 3 × 2 × 15 | at x ±4, ±30, y +32 to +47, z 1–3 | low |
| Lid posts | 4–6 posts Ø 5 with M2 pilots | Ø 5 × 18 | corners and mid-inner edges | medium |
| Wiring | weapon wires enter via slot → ESC; switch on the right lid in series with the battery positive; servo lead from RX to AM under the hub | — | — | medium |
