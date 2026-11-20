# Auger the Top: full rebuild description from reference photos

Source photos:
- `robots/auger_the_top/reference/auger_the_top.aws72.webp` (**primary**, cut out onto white): AWS 72. **Front-left three-quarter from above**, camera about 40° above the floor. The four forks point to the image bottom-left. The robot's **left** end (with the visible left wheel) is at the image right/near; the robot's **right** end is at the image upper-left (far). Bright **green** chassis, **black carbon-fibre arm** with two triangular fins, **pale green** printed motor mount at the arm tip, **blue** brushless motor hanging point-down with a thin **black bit**, **yellow** cable ties.
- `robots/auger_the_top/reference/auger_the_top.aws69.webp`: AWS 69, an older version, photographed on a white table at home (not cut out). **Front-left, low** (about 15° elevation). Same green chassis, but the arm is a **translucent yellow printed bent beam**, the motor (blue, labelled "1404 … MADE IN …") carries a **gold titanium-coated drill bit**. Forks are bare steel with harpoon barbs.
- `robots/auger_the_top/reference/auger_the_top.aws73.webp`: AWS 73, in the pits on a yellow robot-box lid. **Front view from above, rotated** (forks point to the image bottom-right; the robot's right end is at the image left). Forks are capped with **green printed cone safety covers**. Motor labelled "SKYSTARS". The arm head is now over the robot's **left** forks. A darker green under-body block is visible.

`REFERENCE.json`: `other`, 2 wheels, weapon `axe`, axis x. (See §13: the photos suggest the arm swings **sideways**, so the axis label may be wrong.)

Pixel coordinates refer to copies scaled to **1200 px on the long side** (AWS72 → 1200 × 1200, AWS69 → 1148 × 1200 native-ish, AWS73 → 709 × 457 native), ±10 px. Dimensions are estimates from the AWS 150 g / 101.6 mm cube limit and from known parts (a **1404 brushless motor is Ø 18 mm × ~12 mm**). Ratios use **W = chassis width (wheel end-cap to end-cap) ≈ 96 mm**.

---

## 0. Coordinate system and naming

- **+X** = robot right, **+Y** = forward (toward the fork tips), **+Z** = up. **Origin O** = floor point under the centre of the green chassis footprint (excluding forks).
- The robot is **wider than it is long**: the two wheels are at the extreme X ends, and the forks project forward along +Y from the long front edge.
- Arm swing angle **ψ** is measured in the **XZ plane** about the servo axis (along Y): ψ = 0° when the arm points straight up, positive toward +X (robot right). In AWS72/69 the arm lies to the right (ψ ≈ +60° to +70°); in AWS73 it lies to the left (ψ ≈ −60°).

| ID | Part |
|---|---|
| CH | green chassis deck/box |
| EC-L / EC-R | rounded end caps around the wheels (wheel guards) |
| WW-L / WW-R | wheel wells (pockets) inside the end caps |
| WH-L / WH-R | drive wheels (black tyre, yellow/green hub) |
| BS-1…BS-4 | four rounded fork bosses along the front edge (BS-1 = robot right end) |
| BS-N | silver nuts/screws at the boss ends |
| FK-1…FK-4 | four steel harpoon forks |
| FC | green cone safety caps on the fork tips (AWS73, pits only) |
| SB | central raised servo box |
| SV | arm servo (black, output along Y) |
| HN | servo horn / arm hub with silver screw |
| AP-A / AP-B | two black carbon-fibre arm plates with triangular fins (AWS72) |
| FN | triangular fin on each arm plate |
| AY | yellow printed bent arm (AWS69) |
| MP | pale green printed motor mount plate at the arm tip |
| MP-S | 4 black socket screws in a diamond on MP |
| WM | blue brushless outrunner (1404 class) |
| BT | bit: black rod (AWS72) / gold drill bit (AWS69) |
| CT | yellow (AWS72/73) or black (AWS69) cable ties on the arm |
| WR | motor wires along the arm |
| UB | darker green under-body block (AWS73) |
| S-CH | black socket screws on the deck |
| BAT, RX, ESC-D, ESC-W, DM-L/R | hidden electronics and drive motors (guess) |

---

## 1. Overall description in one paragraph

Auger the Top is a **wide, flat, two-wheeled fork robot with a swinging "drill" weapon**. Its bright green chassis is a low slab about 96 mm wide, 46 mm deep and 20 mm tall, with **rounded end caps** at each side that wrap around the two small rubber-tyred wheels like mudguards. Along the front lower edge four **rounded bosses** clamp four **long steel forks** that stick out about 42 mm forward and end in **harpoon/arrow barbs** with sharp chisel points. On top, a **raised servo box** in the middle holds a **servo whose output faces forward**. Bolted to its horn, an **arm** (two black carbon-fibre plates with tall triangular fins in AWS72; a yellow printed beam in AWS69) runs **sideways and upward**, then to a **pale green motor mount** that holds a **blue 1404 brushless motor upside down**. The motor spins a **thin vertical bit** (a drill bit in AWS69) pointing at the floor, just above the forks. In use the servo swings the arm over the top from one side to the other, driving the spinning bit down into whatever is lying on the forks like an auger or a spinning top.

---

## 2. Part-by-part description

### 2.1 Chassis (CH)
- **Shape**: a low **rectangular slab/box**, about **70 mm wide** between the wheel wells (the central part) **× 46 mm deep (Y) × 20 mm tall**, merging at each end into the end caps EC to a total width of **96 mm**. The top deck is flat at **z ≈ 20**. The front face is vertical and is lined with the fork bosses. The rear face is vertical (AWS73 shows its long flat rear wall with a rounded lower edge).
- **Deck**: two flat panels either side of the servo box, each about **20 × 40 mm**, with **black socket-head screws** (S-CH, head Ø 3.5–4 mm, M2) — AWS72 shows one at (x +30, y −15) on the near (left) panel at its front-left corner, one at (x −30, y +15) and two by the servo box; AWS73 shows about 6 across the deck, evenly spaced along the front and rear edges.
- **Colour/material**: **bright green PLA/PETG**, glossy, with visible layer lines and a **small dragon/lizard logo** embossed or painted black on the front face of the deck between bosses 2 and 3 (AWS72: a black squiggle at (x −5, y +23, z 12)).
- **Under-body (UB)**: AWS73 shows, under the chassis, a **darker green block** about **50 mm wide × 30 mm deep × 8 mm tall**, set back from the front edge, which is a separate bottom cover or the battery box **(guess)**. It means the main slab floor is at z ≈ 8–10 and the block reaches down to z ≈ 2 **(guess)**.

### 2.2 End caps / wheel guards (EC-L, EC-R) and wheel wells (WW)
- **Shape**: at each end, the chassis becomes a **rounded "D" bumper**: in side view (YZ) a **stadium/rounded rectangle** about **46 mm long × 18 mm tall** with **full rounds (r ≈ 9 mm)** at the front and rear ends, about **6–8 mm thick (X)**, forming the outer wall beside the wheel. Its outer face has a **long horizontal groove** (about 30 mm × 3 mm, 1 mm deep) at mid-height (AWS72, the near end cap).
- **Wheel well**: inboard of the end cap, a **rectangular pocket** about **24 mm long (Y) × 10 mm wide (X)**, open at the top, in which the wheel sits. In AWS72 the top of the left wheel is visible through the pocket, with the deck surface around it. The pocket's front and rear walls join the end cap to the main body, so the wheel is **fully enclosed in plan**.
- **Supports to the chassis**: the end cap is printed **in one piece** with the deck: bridges in front of and behind the wheel (each about 10 mm long) connect it to the central body **(directly seen as continuous green in AWS72/73)**.
- **Fastening**: a **black socket screw** in the end cap's front lower round at (x ±46, y +18, z 9) in AWS72 (the near cap) — possibly the **outer axle screw** or a screw fixing the motor clamp **(guess)**.
- **Coverage**: the end cap covers the wheel's outer face up to about z 18; the wheel tread is visible above the cap top only by 1–2 mm (AWS72) — so the wheels are **almost fully guarded**.

### 2.3 Wheels (WH-L, WH-R)
- **Shape**: small wheels, **Ø 22 mm × 9 mm wide**, with **black rubber tyres** carrying **fine diagonal/knurled tread** (AWS72: a cross-hatched pattern), on **yellow/green hubs** (AWS73 left wheel: yellow-green hub Ø 14 with a central hole). Typical **N20 rubber wheel** (e.g. 22 × 8 mm hobby wheels).
- **Position**: centres at **x ±40, y −2, z 11**. The tyre bottom touches the floor; the top at z 22 is about 2 mm above the deck.
- **Drive**: each on an **N20 gearmotor** shaft, motor lying transversely inside the body **(guess)**.

### 2.4 Fork bosses (BS-1…BS-4) and fork screws (BS-N)
- **Shape**: four **green cylinders/rounded lugs** along the front lower edge, each about **Ø 14 mm (Z-height 14) × 14 mm long (Y)**, with a **rounded front end** (a half-dome or big fillet). Their axes run **fore-aft (Y)**, at **z ≈ 9**. They protrude about **8–10 mm** ahead of the deck's front face.
- **Spacing**: at **x ≈ +34, +12, −12, −34** (equally spaced at about 22–23 mm), with the outermost bosses merging with the end caps' front rounds.
- **Screws**: each boss has a **silver hex nut / button head** (Ø about 4.5 mm) on its **outer side face** (AWS72/69 show them on the face toward the camera, i.e. the left side face of each boss), with a matching screw end on the other side **(guess)**: a **transverse M2.5/M3 bolt** clamping the fork shank in a slot through the boss.
- **Function**: each boss is a **fork clamp**: the fork shank passes through a slot at the boss's bottom and is pinched by the cross bolt.

### 2.5 Forks (FK-1…FK-4)
- **Shape**: four identical **flat steel bars**, about **3 mm tall × 1.2 mm thick**... more likely **2 mm square / 3 × 1.5 mm** strips (they look like **ground hacksaw-blade or feeler-gauge steel**), running forward from the boss bottoms at **z ≈ 2** down to the floor at their tips. **Visible length ≈ 42 mm** ahead of the boss fronts.
- **Tip (harpoon)**: each fork ends in a **barbed arrowhead**: about **10 mm** from the tip the top edge **steps up** sharply by about **2 mm** (a backward-facing barb), then tapers in a straight line to a **sharp point on the floor** (a long chisel bevel ~10 mm). Seen in profile: shank top at z 3, barb peak at z 5, tip at z 0. The barbs face **backward**, to stop opponents sliding off forward.
- **Colour**: grey steel with brighter ground bevels; slightly rusty/tarnished in AWS69.
- **Orientation**: all four parallel to +Y, laid nearly flat (a 3–4° downward slope).
- **Cone caps (FC, AWS73)**: in the pits each tip is covered by a **green printed cone**, about **Ø 12 mm × 22 mm long**, with a pointed end, pushed onto the fork tip — a **safety cover** for handling, removed for fights.

### 2.6 Servo box (SB) and servo (SV)
- **Shape**: a **raised green box** on the centre of the deck, about **30 mm wide (X) × 24 mm deep (Y) × 18 mm tall** above the deck (top at z ≈ 38), slightly to the **left** of centre (x ≈ −5) in AWS72 and a little behind mid-depth. Its top has **two black screws** (AWS72 at the rear corners, AWS69 two near the front-left top edge).
- **Servo**: a **black micro servo** (about 23 × 12 × 26 mm) **standing up inside the box with its output face toward the front (+Y)**: AWS72 shows its black front face and output horn on the **front of the box** at about (x +8, y +12, z 28); AWS69 shows the black servo face with a white label ("CL…", probably "Corona"/"CLS"…) on the front face of the box with the arm hub in front of it.
- **Output axis**: **along +Y**, at about **(x +8, z 30)**.
- **Horn/hub (HN)**: a round **silver/white** hub with a central screw (Ø 7 mm) clamped between the arm plates (AWS72 shows a silver ring with a screw at (850, 510) px).

### 2.7 Arm, AWS72 version (AP-A, AP-B, FN, CT, WR)
- **Plates**: two **black carbon-fibre plates**, each **2 mm thick**, standing **vertically**, parallel to each other, spaced about **14 mm** apart (they sandwich the horn at one end and the motor mount at the other). Each plate is a **long bar 10 mm wide × about 75 mm long** with:
  - a **round end** (r 5) at the servo hub, with **2 black screws** (M2) and the horn screw,
  - a **tall triangular fin** (FN) rising from its upper edge near the motor end: a right triangle about **28 mm tall × 25 mm base**, its vertical edge toward the motor end, with a **triangular lightening hole** (about 14 × 8 mm) inside — a "shark fin" shape,
  - a straight lower edge.
- **Run**: from the servo hub at (x +8, y +12, z 30) the arm runs **toward the robot's right (+X) and up**, at about **25–30° above horizontal**, to the motor mount at its far end. AWS72 shows it passing over the right half of the deck.
- **Ties (CT)**: **two yellow cable ties** (or yellow silicone O-rings) wrapped around both plates near the middle, about 15 mm apart, holding the **motor wires (WR)** (thin black wires) along the plates.
- **Screws**: AWS72 shows **2 black screws** near the motor-mount end of the near plate (x pattern 6 mm apart) and **2–3 black screws** near the hub end.

### 2.8 Arm, AWS69 version (AY)
- A **translucent yellow printed beam**, about **10 mm wide × 6 mm thick**, **bent** in a **dog-leg**: from the servo hub it rises steeply (about 55° from horizontal) for 45 mm, then bends to run **horizontally** about 25 mm to the motor mount. A **steel strip insert** runs along its inside edge (a metal stiffener visible through a slot). **Black screws** (4–6) along it, and **black cable ties** holding wires.

### 2.9 Motor mount (MP) and screws (MP-S)
- **Shape**: a **pale green (mint)** printed plate, about **36 mm × 30 mm × 6 mm**, outline a **rounded triangle / guitar-pick**: a straight edge where it is clamped between the carbon plates and a large round outer end (r ≈ 15) around the motor axis. AWS69's version is a bright green rectangular bracket with a downward lip.
- **Screws**: **4 black socket-head screws** (head Ø 3.5) in a **diamond/cross** on a **12 mm** pattern around the motor axis (the 1404 motor's M2 mounting pattern), plus 2 more screws through the arm plates into its side.
- **Orientation**: horizontal, with the **motor hanging below it**, shaft pointing **down (−Z)**.

### 2.10 Weapon motor (WM) and bit (BT)
- **WM**: a **blue anodised brushless outrunner**, about **Ø 18 mm × 12 mm** (the AWS69 label "1404" confirms a **1404 size**: 14 mm stator, 4 mm stack; can Ø ≈ 18). AWS73 label "SKYSTARS". The bell faces **down**.
- **BT (AWS72)**: a **thin black rod**, about **Ø 2 mm × 25 mm**, from the motor shaft straight down, with a small **step/collar** about 8 mm above its lower end and a pointed tip. Its tip sits about **3–5 mm above the right outer fork**.
- **BT (AWS69)**: a **gold-coloured (TiN coated) twist drill bit**, about **Ø 2.5 mm × 35 mm** visible, in a short collet on the motor shaft, tip about 10 mm above fork level.
- **AWS73**: the bit is replaced by a **green printed cylinder/sleeve** about Ø 8 × 18 (a safety cover or a different spinning "top" body) **(uncertain)**.

### 2.11 Wiring, switch, electronics
- Motor wires from WM run along the arm under the ties and enter the servo box/deck near the hub with a slack loop (AWS72 shows a black wire loop at (820, 470) px).
- No switch is visible; it is probably on the rear wall or on the deck's rear edge **(guess)**.

---

## 3. Per-view sections

### 3.1 AWS72 (front-left from above)
- **Bottom-left**: four forks fanning toward the viewer, tips at (50, 685), (115, 800), (250, 985), (340, 1135) px; barb steps at about 15% from each tip.
- **Centre-left diagonal**: four green bosses with silver nuts at (395, 525), (485, 640), (640, 805), (760, 940) — the row is the front edge.
- **Centre**: the deck with the black logo between bosses 2 and 3, the servo box at (590–910, 290–560), screws at (805, 325), (855, 355), (1000, 580), (775, 720).
- **Right**: the near end cap (690–1150, 650–970) with the groove and a screw at (765, 960); the left wheel's tyre and hub visible in its pocket at (920–1120, 650–760).
- **Top**: the arm: carbon plates from the hub (850, 510) to the pale green mount at (95–330, 185–420); fins at (240–380, 45–215) and (470–560, 185–330); yellow ties at (510, 360) and (690, 410); the motor (blue) under the mount at (120–245, 360–430); the black bit from (230, 450) to (230, 605).

### 3.2 AWS69 (front-left, low)
- Forks large in the foreground (tips at 25–420 px x, 700–1040 y); bosses at (330, 600), (430, 640), (625, 750), (800, 830); the near end cap with its screw at (815, 835); the servo box (440–650, 380–560); the yellow arm from (800, 470) rising to (330, 70) then left to the green mount (110–330, 30–150); blue motor (120–310, 120–230); drill bit down to (185, 565).

### 3.3 AWS73 (front, high, rotated)
- Long green body across the image (70–610, 120–330), wheels at the left end (20–95, 190–290) and right-rear (480–545, 90–140); four cone-capped forks at the bottom (cones at (265, 400), (380, 360), (520, 320), (640, 300)); the arm with two black fins (250–470, 30–210) and yellow ties; the mint motor mount with 4 screws (430–540, 130–200) and blue motor below, with a green sleeve dropping to (470, 320).

### 3.4 Top view (synthesised)
- A 96 × 46 rectangle with rounded ends; wheel pockets 24 × 10 at each end; the servo box near the centre; four forks spaced 22.7 mm, 42 mm long ahead of 10 mm bosses (overall depth ≈ 46 + 10 + 42 = 98 mm). The arm projects from the servo hub at (x +8, y +12) sideways toward ±X, and the motor head (Ø 36 mount) sits over the outer fork at x ≈ ±34, y ≈ +35.

### 3.5 Front view
- Slab 96 × 20 with four round bosses (Ø 14) along the bottom, the forks as dots on the floor in front; the servo box (30 × 18) on top; the arm rising from the box to one side and the motor hanging over the outermost fork with the bit pointing down.

### 3.6 Side view (right, inferred)
- End cap stadium 46 × 18 with the wheel just visible above it; the forks extending 52 mm forward from the body front, barbs near the tip; the arm head above the front.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| CH | slab box | 70 × 46 × 20 (central) | 0.73 × 0.48 × 0.21 | green FDM | — | 1 |
| EC | stadium side wall | 8 × 46 × 18 | 0.08 × 0.48 | green, integral | integral | 2 |
| WW | pocket | 10 × 24 | — | — | — | 2 |
| WH | rubber wheel | Ø 22 × 9 | 0.23 × 0.09 | black tyre, yellow hub | N20 shaft | 2 |
| BS | rounded lug | Ø 14 × 14 | 0.15 | green, integral | — | 4 |
| BS-N | cross bolt + nut | M2.5 | — | silver | through BS | 4 |
| FK | harpoon fork | 3 × 1.5 × 56 (42 exposed) | 0.44 | steel | clamped in BS | 4 |
| FC | cone cap | Ø 12 × 22 | — | green FDM | push-on | 4 (pits) |
| SB | raised box | 30 × 24 × 18 | 0.31 × 0.25 | green | integral / screws | 1 |
| SV | micro servo | 23 × 12 × 26 | — | black | in SB | 1 |
| HN | horn hub | Ø 7 | — | white/silver | spline + screw | 1 |
| AP | finned plate | 75 × 10 × 2 + fin 28 × 25 | 0.78 | black CF | 4–5 × M2 | 2 |
| MP | rounded triangle plate | 36 × 30 × 6 | 0.38 | mint green FDM | 4 + 2 screws | 1 |
| WM | 1404 outrunner | Ø 18 × 12 | 0.19 | blue | 4 × M2 | 1 |
| BT | rod / drill bit | Ø 2–2.5 × 25–35 | 0.3 | black steel / gold drill | collet | 1 |
| CT | ties | — | — | yellow | — | 2 |
| UB | under block | 50 × 30 × 8 | 0.52 | dark green | screws (guess) | 1 |
| S-CH | socket screws | head Ø 3.5 | — | black | into CH | ~6–8 |

---

## 5. Contact / gap matrix (est. mm)

| A ↔ B | Relation | Gap |
|---|---|---|
| EC ↔ CH | integral | 0 |
| WH outer face ↔ EC inner face | side by side | 1 |
| WH inner face ↔ CH pocket wall | side by side | 1 |
| WH tread ↔ pocket front/rear walls | clearance | 1–2 |
| WH top ↔ deck | above | +2 |
| WH bottom ↔ floor | touching | 0 |
| BS ↔ CH front face | integral | 0 |
| FK shank ↔ BS slot | clamped | 0 |
| FK tip ↔ floor | touching | 0 |
| FK-n ↔ FK-n+1 | parallel spacing | ~20 (clear) |
| BS bottom ↔ floor | above | 2 |
| SB ↔ deck | integral/screwed | 0 |
| SV ↔ SB | held inside | 0 |
| HN ↔ AP | screwed | 0 |
| AP-A ↔ AP-B | spacing | 14 |
| AP ↔ MP | screwed | 0 |
| WM ↔ MP | screwed | 0 |
| BT ↔ WM shaft | collet | 0 |
| BT tip ↔ outer fork top (rest) | above | 3–5 |
| AP lower edge ↔ deck (rest) | above | 4–8 |
| UB ↔ CH bottom | screwed | 0 |
| UB bottom ↔ floor | above | 2 |

---

## 6. Mechanism

1. **Drive**: two wheels at the ends of a wide body, skid steer; the forks/bosses at the front and the under-block (or the rear edge) carry the rest of the weight. Short wheelbase → very quick turning.
2. **Weapon spin**: the 1404 outrunner spins the bit at high speed (at 2S and ~4000 KV, ~30 000 rpm no load). The bit is small: it **drills/grinds** rather than storing energy.
3. **Weapon swing**: the servo (axis along Y) swings the arm through the **XZ plane**: from resting on one side (ψ ≈ ±65°, bit over the outer fork) over the top to the other side, a total sweep of ≈ 130°. The bit tip traces a circle of radius ≈ (arm length + mount offset) ≈ **60 mm** about the servo axis at (x +8, z 30): it reaches z ≈ 0–5 over x ≈ ±40, i.e. **it can come down onto the outer forks on either side**. An opponent caught on the forks is hit from above by the spinning bit.
4. **Interpretation alternative (json says axis x)**: the arm could instead pivot about X and swing fore-aft; the photos showing the head on the right (AWS69/72) and on the left (AWS73) favour the sideways swing (or a re-mount between events). Confidence for the sideways swing: **medium**.

---

## 7. Assembly order (suggested)

1. Print CH (with end caps, bosses, servo box) and the under-block UB.
2. Install the two drive gearmotors in the end regions, shafts out into the pockets; press on the wheels; fix end-cap screws.
3. Install battery, receiver, ESCs; fit UB from below.
4. Slide the four forks into the boss slots; tighten the cross bolts.
5. Fit the servo in SB, output forward; centre it.
6. Build the arm: two CF plates, horn hub between them at one end, the mint motor mount MP between them at the other; 4–6 M2 screws.
7. Screw the 1404 motor to MP (4 × M2), fit the bit/drill in its collet.
8. Run the motor wires along the arm; secure with the two yellow ties; leave a slack loop at the hub.
9. Mount the arm on the servo spline with the horn screw.
10. In the pits, cap the fork tips with the green cones.

---

## 8. Hidden / uncertain list
- Swing plane of the arm (XZ preferred) and servo orientation.
- What the AWS73 green sleeve on the motor is.
- Under-block purpose; switch location.
- Fork material (hacksaw/spring steel) and section.
- Exact arm length.
- All mm values ±15–20%.

---

## 9. Coordinate frame (restated)
- Origin O on the floor under the chassis centre. +X right, +Y forward, +Z up, mm. ψ: arm angle in the XZ plane from +Z, positive toward +X.
- Body x ∈ [−48, +48], y ∈ [−23, +23], z ∈ [2, 20]; servo box to z 38; bosses to y +33; fork tips at y +75.

## 10. Profiles as math

**10.1 End cap (YZ, at x = ±44 to ±48).** Stadium: straight top z = 18 and bottom z = 0 for y ∈ [−14, +14], semicircles r = 9 centred at (y ±14, z 9). Groove: rectangle y ∈ [−15, +15], z ∈ [8, 11], depth 1 on the outer face.

**10.2 Boss (YZ section, constant over 14 mm in X).** Rectangle y ∈ [23, 26], z ∈ [2, 16] plus a half-disc of r = 7 centred at (y 26, z 9) for y ≥ 26. Fork slot: 3.5 × 2 at z 2–4.

**10.3 Fork profile (YZ).** Shank bottom z_b(y) = 2·(75 − y)/52 for y ∈ [23, 75] (tip on the floor). Top edge: z_t = z_b + 3 for y ∈ [23, 63]; barb: vertical step at y = 63 up to z_b + 5; arrowhead flank from (63, z_b + 5) straight to the tip (75, 0). Plan: constant width 1.5 mm.

**10.4 Arm plate (in its own plane, s along the arm from the hub, t perpendicular).** Bar: s ∈ [0, 75], t ∈ [−5, +5], hub end semicircle r 5 at s = 0. Fin: triangle (s 45, t 5), (s 70, t 5), (s 70, t 33); hole: triangle (s 54, t 10), (s 66, t 10), (s 66, t 25).

**10.5 Arm pose.** Hub H = (x 8, y 12, z 30). Arm direction in XZ: u(ψ) = (sin ψ, 0, cos ψ). Arm end E = H + 70·u(ψ). Motor axis M = E + (0, +20, −8) (the mount offsets the motor forward and down). Bit tip T = M − (0, 0, 6 + 25). Rest ψ = +62°: E = (69.8, 12, 62.9)… then the head would be outside the body; with the photos' head just over the outer fork (x ≈ 34), the effective arm length is **shorter, ~35 mm in plan** → use |HE| = 45 and ψ = +55°: E = (44.9, 12, 55.8), M = (44.9, 32, 47.8), T = (44.9, 32, 16.8). Raise this into a consistent pose in §13.

**10.6 Motor mount outline (plan, in MP frame centred on the motor axis).** Circle r = 15 on the outer side joined by two tangents to a 14 mm wide straight edge 18 mm from the axis (guitar-pick). Screw holes: 4 × Ø 2.2 at r = 6, φ = 45°, 135°, 225°, 315°.

**10.7 Wheel.** Cylinder r = 11, width 9; tread knurl ±45° grooves 0.5 deep, pitch 1.5.

## 11. Pixel measurements

- **AWS72**: boss spacing ≈ 170–190 px along the row (four bosses over ≈ 560 px), near end-cap length ≈ 440 px, near fork exposed length ≈ 420 px (near) / 330 px (far), wheel Ø ≈ 200 px (left wheel, partly hidden), servo box width ≈ 320 px, motor Ø ≈ 125 px (far), bit length ≈ 155 px, mint mount ≈ 235 × 235 px.
- **AWS69**: near fork exposed ≈ 330 px; end cap ≈ 420 px long; motor Ø ≈ 190 px (near head, label "1404"); drill visible ≈ 340 px; yellow arm length ≈ 600 px total.
- **AWS73**: body length (long axis) ≈ 540 px; wheel Ø ≈ 85 px; motor Ø ≈ 75 px; fork exposed (cone to boss) ≈ 85–110 px.

## 12. Several independent estimates

| Quantity | Method A (rule / known part) | Method B (ratio) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Body width W | ≤ 101.6 | — | AWS73: 540 px; motor 75 px = 18 mm → 4.2 px/mm → 129?? (motor nearer the camera, ×1.3) → 99 | **96** |
| Wheel Ø | N20 hobby wheel 22 | 0.23 W | AWS73: 85 px / 4.2 × (far, ×1.0) = 20; AWS72: 200 px vs motor 125 px (18 mm, farther) → 29 (wheel nearer) | **22** |
| Fork exposed length | 101.6 − 46 − 10 = 45 | 0.44 W = 42 | AWS69: 330 px vs motor 190 px = 18 → 31 (forks nearer → ×0.9) … AWS72: 420 / (125 px / 18 × 1.5 nearer) = 40 | **42** |
| Servo box width | servo 23 + walls 7 = 30 | 0.31 W | AWS72: 320 px vs end-cap 440 px (46) → 33 | **30** |
| Arm length (hub to mount edge) | 45–70 | — | AWS72: ≈ 560 px along the plates vs boss row 560 px (68 mm) → 68 (perspective) | **55** |
| Bit length | 25 | — | AWS72: 155 px / 7 px/mm = 22; AWS69: drill 340 px / (190 px / 18) = 32 | **25 (72), 32 (69)** |
| Height (servo box top) | 38 | 0.4 W | AWS69 low view: box top ≈ 1.9 × deck height → 38 | **38** |

## 13. Consistency check

1. **Box fit**: depth 46 + 10 (bosses) + 42 (forks) = 98 ≤ 101.6 ✓. Width 96 ✓. Height: arm vertical (ψ 0) → hub z 30 + arm 55 + mount 6 ≈ 91 ✓.
2. **Arm geometry**: the head sits over the outer fork (x ≈ ±34, y ≈ +35). From the hub at (x 8, y 12, z 30), the in-plan distance to the head is √(26² + 23²) ≈ 35 mm. So the arm both swings sideways **and** the mount offsets the motor forward by ~23 mm. With ψ = ±50° and an arm of 40 mm, E = (8 + 30.6, 12, 30 + 25.7) = (38.6, 12, 55.7); the motor axis offset forward 23 mm and down 10 → M = (38.6, 35, 45.7); bit tip T = M − (0, 0, 6 + 25 + 12) = (38.6, 35, 2.7): **just above the fork (z 3)** ✓. Reconciled: **arm 40 mm hub-to-mount pivot + 23 mm forward offset, ψ_rest = ±50°**. The CF plates (75 mm) include the fin/mount overlap.
3. **Head side differs between photos**: AWS72/69 right, AWS73 left. A sideways swinging arm explains this. If the arm instead swung fore-aft (json axis x), the head would always be on the same side. **Reconciled: sideways swing (axis Y), medium confidence.**
4. **Weight**: CF arm (6 g) + 1404 (9 g) + mount (3 g) + bit (1 g) + servo (9–12 g) is a light weapon, leaving ~110 g for chassis, forks (4 × 4 g steel) and drive — plausible.

---

## 14. Why the designer did it (adversarial first)

- **Four long steel forks with harpoon barbs**: in the antweight meta, forks beat wedges at getting under, because a thin steel edge can sit at floor level and slips under printed wedge lips. Four widely spaced forks cover most of the robot's 96 mm width, so opponents from any frontal angle get forked. The **backward barbs** hook into plastic and hold the opponent on the forks while the weapon works — that is the whole strategy (catch, hold, drill). Steel forks survive spinner hits; when bent, a cross bolt releases each one for replacement. Weak point: long cantilevers give opponents' lifters leverage; the bosses are the stress concentration.
- **Fork bosses with cross bolts**: printable, adjustable fork height, fast replacement.
- **Wide, shallow body with wheels at the ends**: puts the wheels far apart for stable straight driving, makes the body itself very shallow so the forks dominate the footprint, and keeps the robot inside the 4 in cube with the long forks.
- **End caps wrapping the wheels**: the wheels are the only vulnerable moving parts on the sides; the stadium caps fully guard them against horizontal spinners and opponents' wedges sliding along the sides, and their rounded ends deflect hits and stop the robot snagging on arena walls. Printing them integral avoids separate guard supports.
- **Small rubber wheels just above the deck**: allows (marginal) inverted driving; grippy rubber for pushing with the forks.
- **Servo-swung, overhead drill weapon**: an unusual "control + damage" design: forks immobilise, the bit drills into the opponent's top (often their weakest, thinnest panel, where electronics live). A 1404 motor is tiny and light. The bit spins, so even a soft contact grinds through plastic. The arm resting **to one side** keeps the centre of mass low and the top clear; swinging over the top lets it strike opponents on either outer fork. Weak points: the arm and head are fragile and exposed to vertical and horizontal spinners; the servo gears can strip if the head is hit.
- **CF arm with fins (AWS72) vs printed yellow arm (AWS69)**: the AWS69 printed arm (with a steel stiffener) was heavier and flexed; the later CF plates are stiffer and lighter; the fins add depth (bending stiffness) near the head where the load is, and the triangle holes save weight.
- **Cone caps**: safety rules require fork/spike covers outside the arena.
- **Yellow ties**: keep motor wires from flapping into the bit.

## 15. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre) | Confidence |
|---|---|---|---|---|
| Drive motors | 2 × N20 gearmotors, shafts along X | 12 × 10 × 25 | (±24, −2, 11) | high |
| Battery | 2S LiPo 150–250 mAh | 35 × 18 × 8 | in UB / under the deck, (−15, −8, 7) | medium |
| Weapon ESC | 6–12 A brushless ESC | 20 × 12 × 4 | under the deck, (+18, −8, 12) | medium |
| Drive ESC + RX | combined brushed ESC/RX | 25 × 15 × 6 | (0, −10, 12) | low |
| Servo | 9 g metal-gear micro servo | 23 × 12 × 26 | in SB, output at (8, 12, 30) along +Y | medium |
| Fork clamps | M2.5 cross bolts + nuts | — | at each boss, z 9 | medium |
| Power switch | rear wall slide switch or link | 10 × 5 | (+20, −23, 12) | low |
| Wheel outer axle screws | M2 into the end caps | — | (±46, 0, 11) | low |
| Wiring | weapon leads run down from the arm hub into SB, to the ESC; servo lead to RX; drive leads short | — | — | medium |
