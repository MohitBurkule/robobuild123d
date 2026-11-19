# Recycler (Recycler 5): full rebuild description from reference photos

Source photos (in `robots/recycler/reference/`):
- `recycler.aws65.webp` (524 × 374 px): a **pit snapshot on a wooden table**. Front view from slightly to the robot's right and about **30° above horizontal**. The drum is nearest the camera. Low resolution and slightly blurred. **Green "Recycler 5" lettering** on the lid. The drum carries **5 thin silver bands**.
- `recycler.aws66.webp` (366 × 274 px, very low resolution): a pit snapshot on an **orange table**. Front view from slightly to the robot's left, about **35° above horizontal**. **White "Recycler 5" lettering**. The drum bands look **flush rings** (4 visible), not hooks. Other robots' parts appear at the bottom left and bottom right; ignore them.
- `recycler.aws67.webp` (1808 × 1112 px): cut out onto white. The **best photo**. Front view from about **25–30° above horizontal**, square to the front. **White lettering**. The drum carries **4 bent steel strip teeth** whose ends stick out below the drum. A dark-green clip crosses the lid.

Everything stated as fact is read from those photos. Anything inferred is marked **(guess)** with a confidence. All dimensions are **estimates in mm**, scaled from the AWS antweight limits (150 g, fits a 101.6 mm cube) and from the overall width, which is taken as **≈ 96 mm** (wheel outer face to wheel outer face). That is the largest dimension in every photo and plainly near the cube limit. **W = 96 mm** is used for ratios.

**What the photos show and do not show**: all three are **front views** from a similar height. The rear, the underside, the sides in profile and the rear wheels' outer faces are never seen squarely. So the fore-aft (Y) dimensions are the least certain part of this description, and they are reasoned from perspective and from mechanical necessity. I say so wherever it matters.

Recycler 5 is a **wide, low drum spinner**: a full-width horizontal drum across the front, two rear drive wheels at the outer corners, and a flat box body between them with a lid that shows a servo through a window.

---

## 0. Coordinate system and naming

- **Origin O** = the floor point (z = 0) under the centre of the **body box** (mid-width, mid-depth of the box behind the drum; the drum is not included).
- **+X** = robot's right, **+Y** = forward (toward the drum), **+Z** = up. Units mm.
- All three photos look at the **front**, so the **robot's right is on the image left**. Every position below has been mirrored into robot coordinates. For example, the steel shaft end sticking out at the image left of AWS67 is on the **robot's right** (x > 0), and the "Recycler 5" text on the image right is on the **robot's left** half of the lid.

Part IDs:

| ID | Part |
|---|---|
| BX | main body box (black printed tub) |
| FW | body front wall with lightening/vent holes |
| LD | lid (black printed top plate) |
| LW-R | right lid window (servo window) |
| LW-L | left lid window/slot |
| TXT | "Recycler 5" lettering on the lid |
| CL | dark-green / black clip that crosses the lid front edge (link handle or lid latch) |
| SV-R | visible servo under LW-R ("Blue Arrow D0474HT HV") |
| SV-L | presumed mirror drive servo under the left of the lid (hidden) |
| WH-L / WH-R | rear drive wheels with pink ribbed tyres |
| WG-L / WG-R | wheel guards / wheel side plates (black, around the wheels) |
| AR-R / AR-L | drum side arms (black printed plates at each drum end, running forward from the body corners) |
| FT-R / FT-L | feet of the drum arms (lower tips that reach the floor) |
| DR | drum body (stack of black printed rings) |
| DR-1…5 | drum ring segments |
| TT-1…4 | steel strip teeth (bent bands clamped between drum segments) |
| SH | steel drum shaft (sticks out of AR-R) |
| EC | drum end cap / motor end (robot's left end of the drum) |
| WM | weapon motor (hidden, inside or at EC, guess) |
| SK | silver centre tab/skid under the drum (AWS67) |
| S-LD | lid screws |
| S-AR | drum-arm screws, nut and bolt |
| WR | wiring visible through the front-wall holes |
| BAT, ESC, WESC, RX, SWT | electronics (hidden, guess) |

---

## 1. Overall description in one paragraph

Recycler 5 is a **wide, flat drum spinner** about **96 mm wide, ≈ 70 mm long and ≈ 30 mm tall** (wheel tops). The back two-thirds is a **black printed box** about **80 mm wide × 34 mm deep × 24 mm tall**. Its front wall is pierced by **two rows of round/hexagonal lightening holes**, through which **coloured wires** (red, blue, yellow) show. The box is closed by a **flat black lid** with a rectangular **window on the right** showing a **Blue Arrow D0474HT HV servo** label, a **slot on the left**, the hand-painted name **"Recycler 5"**, and a **clip** (dark green in AWS67, black in AWS65) that straddles the lid's front edge at the centre. At the **rear corners**, outboard of the box, are two **drive wheels** about **Ø 26 mm** with **pink ribbed tyres** (they look like pink foam or loop-tape tread), each in a black side guard. In front of the box, carried between two **black printed side arms** that run forward from the box's front corners, is a **horizontal drum** about **Ø 23 mm** and **≈ 82 mm long**, made of **stacked black printed rings**. Between the rings, **4–5 silver steel bands** are clamped; in AWS67 they are **bent strips whose ends stick out below the drum as hooked teeth**. A **steel shaft** sticks out of the right arm. The left end of the drum is a separate **end cap** that probably holds the **weapon motor**. The arms' lower tips reach down to the floor as **feet** on which the front of the robot rests.

---

## 2. Part-by-part description

### 2.1 Body box (BX)
- **Shape**: a rectangular box, **x ∈ [−40, +40] (80 mm)**, **y ∈ [−17, +17] (34 mm, guess)**, **z ∈ [3, 24]** (≈ 21 mm of wall height, with ≈ 3 mm ground clearance **(guess)**).
- **Colour / material**: matt black FDM with visible **horizontal layer lines**, and a slightly rough, worn finish. Nylon is the likely material (the spec uses nylon) **(guess)**.
- **Front corners**: at each front corner a **square block** about **12 × 12 × 14 mm** sticks out forward and down (AWS67 image-left block px ≈ (150–280, 300–450) and image-right block px ≈ (1600–1690, 470–560)). These are the **roots of the drum arms** AR.
- **Rear**: never seen. Presumed a plain wall with the switch or link access **(guess)**.

### 2.2 Front wall with holes (FW)
- **Shape**: the box's front face, **80 mm wide × ≈ 16 mm tall** visible below the lid overhang. It is set **back about 3–4 mm** under the lid's front lip.
- **Holes**: **two staggered rows of round or hexagonal holes**, each about **Ø 5–6 mm**, about **9–10 per row**, pitch ≈ **8 mm**. AWS65 shows them clearly as **hexagons** (a honeycomb pattern). AWS67 shows them as dark round holes partly hidden by the drum.
- **What shows through**: AWS65 shows **red, blue, yellow and white wires** behind the holes (centre-left and right of centre). AWS67 shows **a red spot** at the far image right (robot's left) and grey at the centre.
- **Function**: weight saving and cooling, at a place the drum shields **(see §12)**.

### 2.3 Lid (LD)
- **Shape**: a flat black plate about **82 mm wide × 34 mm deep × 3 mm thick**, sitting on the box wall tops at z ≈ 24–27. The front edge has a **downturned lip** about **3 mm** deep, which overhangs the front wall by about 3 mm (a visible shadow line in AWS67, px y ≈ 460–490).
- **Raised panels**: the lid is not perfectly flat. The **left half** (robot's left, with the lettering) is a slightly **raised rectangular panel** about **38 × 20 mm**, about **1–2 mm** higher, with a chamfered edge. The **right half** has the **window LW-R** surrounded by a raised frame.
- **LW-R (servo window)**: a rectangular opening about **26 mm wide (X) × 14 mm deep (Y)**, centred at about **(x +17, y −2)**. The **servo SV-R** fills it, its label face up and its long axis along X.
- **LW-L (slot)**: a shallow rectangular **recess or slot** about **30 × 5 mm** along X near the rear edge of the left half, at about **(x −20, y −12)**. AWS67 shows a dark slot with a lighter edge (px ≈ 970–1250, 180–215).
- **Lid screws S-LD**: small black **countersunk or button Phillips screws**, head Ø ≈ **3 mm**. Visible in AWS67 at px (342, 272) [robot right-front], (1225, 212) [robot left-rear], (1495, 382) [robot left-front] and one at the image centre top near the clip (≈ 945, 190 hidden). In AWS65 also at (85, 118), (360, 100), (430, 165). So **4 screws, one near each lid corner (± ≈ 34, ± ≈ 12)**.
- **Lettering TXT**: hand-painted **"Recycler"** on one line and **"5"** below it. **White paint pen** in AWS66/67, **green** in AWS65. Height of the letters ≈ **7 mm**, line length ≈ **36 mm**, on the robot's left half of the lid.

### 2.4 Clip (CL)
- **Shape**: a printed part about **8 mm wide**, shaped like a **flattened "X" or bow tie** in plan, lying across the lid at the centre (x ≈ 0). It runs from about **y −14 (lid middle)** forward over the lid front edge and **down the front wall** to about **z ≈ 10**. So in side profile it is an **inverted "L"** (or a "J"), about **28 mm** along the lid and **15 mm** down the front.
- **Colour**: **dark green** (AWS67), **black** (AWS65; AWS66 shows a black stem).
- **Interpretation**: the most likely reading is a **removable link handle / power key**: a printed handle that plugs a link into the electronics through the lid, shaped to grip **(guess, medium)**. Alternative: a **latch** that holds the lid down at the front, or the **lock pin** for the weapon (the spec has a `lock_pin`), which is inserted through the front wall into the drum area to stop the drum turning in the pits **(guess, medium)**. Its downward leg reaching toward the drum supports the lock-pin reading.

### 2.5 Servos (SV-R visible, SV-L hidden)
- **SV-R**: a **Blue Arrow D0474HT HV** digital micro servo. The label reads "BLUE ARROW", "SERVOS", "D0474HT", "MAGNESIUM ALLOY", "DIGITAL PRECISION" and "HV" in red. It lies with its long axis along **X**, label up, under LW-R. Visible label ≈ **22 × 12 mm**. A D0474-class servo is about **23 × 12 × 25 mm** with a magnesium case **(guess from the model number)**. Its output end points toward the **centre** of the robot (x ≈ 0) **(guess, from where the label's text block sits)**.
- **Purpose (the main open question)**: two readings.
  1. **Drive servo, modified for continuous rotation (guess, medium)**. Antweights often use converted micro servos for drive. The servo lies along X close to the right wheel, so a short shaft or gear could drive WH-R. A second, mirrored servo **SV-L** would then sit under the left half of the lid (where the raised panel is) to drive WH-L.
  2. **Actuator for a self-righting arm or a weapon lock (low)**: no arm is visible anywhere, which argues against this.
- The spec models the drive as `dm_wheel_l0` / `dm_wheel_r0` motors; I keep the servo-drive reading as the most likely physical build.

### 2.6 Rear drive wheels (WH-L, WH-R)
- **Shape**: a cylinder about **Ø 26 mm × 9 mm wide**.
- **Tyre**: **pink / salmon-red**, with **fine transverse ribs** about **1 mm** apart. It looks soft and fibrous, like **pink foam** or **hook-and-loop (Velcro) tape** wrapped around a hub. AWS67's right wheel (robot left) shows a few loose fibres at the bottom edge, which supports loop tape or foam **(guess)**.
- **Hub**: a black disc behind the tyre (visible as a dark ring on the inner face, AWS67 px ≈ (1490–1520, 200–400)).
- **Position (centres)**: **x = ±43.5**, **y ≈ −12**, **z = 13**. The outer tyre faces are at **x = ±48 (96 mm track)**. The wheel tops at z ≈ 26 stand **about 1–2 mm above the lid**, so the robot may run inverted on the wheel tops and lid edges **(guess)**.
- **Visibility**: in all three photos the wheels sit at the **back corners**, their tops visible above and behind the lid corners, their fronts hidden by the front corner blocks and the drum arms.

### 2.7 Wheel guards / side plates (WG-L, WG-R)
- **Shape**: each wheel is flanked by **black printed plates**. On the **inner side**, the box wall end (x = ±40) acts as the inner support. On the **outer side** (AWS67 image left, px ≈ (135–200, 60–300), and AWS66 left), a **black plate about 3 mm thick and ≈ 28 mm tall** covers part of the wheel's outer face. Its top is rounded to follow the wheel.
- In AWS67 the image-left wheel (robot right) shows a **black rim outboard of the pink tread**, i.e. a **guard or hub flange** about 3 mm thick. The image-right wheel (robot left) shows a **black ring behind the tread** that could be the guard edge or the hub.
- **Interpretation**: a **C-shaped wheel bracket**. The outer plate is an **axle support / partial guard**: the wheel is carried between the box wall and an outer plate that is tied to the box at the rear (above or behind the wheel) **(guess, medium)**. The outer plate covers only the centre of the wheel (hub area), so the tread is still exposed at the rear and top.
- **Guard-to-chassis support (guess, medium)**: the outer plate is joined to the box by a **top bridge** behind the lid (≈ 10 mm wide in Y, at z ≈ 22–26) or by the **wheel axle itself** passing through both plates. Neither is seen.

### 2.8 Drum side arms (AR-R, AR-L) and feet (FT-R, FT-L)
- **Shape (AR-R, best seen at the AWS67 image left)**: a **vertical black printed plate** about **4–5 mm thick (X)** lying in a YZ plane at **x ≈ +44**. In side profile it is a **dog-leg**:
  - **Root**: the front-corner block of the box (y ≈ +17, z 10–24).
  - **Main run**: forward and down to the drum axle at about **(y +33, z 14)**, with a **round boss** about **Ø 16 mm** around the shaft (px ≈ (150–245, 520–700) in AWS67).
  - **Foot FT**: below and slightly ahead of the boss the plate continues **down to the floor** as a tapered tip about **6 mm wide**, ending at about **(y +36, z 0)** (AWS67 px ≈ (190–235, 900–1010)). In AWS67 the image-right foot (robot left) is also visible at px ≈ (1460–1530, 970–1060).
- **Fasteners S-AR**: on AR-R, a **small hex socket screw** above the shaft (px ≈ (315, 465)), the **shaft end SH** (px ≈ (75–150, 580–620)), and below the shaft a **bolt with a hex nut** (M3, px ≈ (270, 665)) and a small **screw end** at px ≈ (250, 720). So the arm likely has a **clamp**: the boss is split and squeezed onto the shaft or a bearing by the lower bolt **(guess, medium)**.
- **AR-L**: the robot's left arm is similar but carries the **end cap EC** and probably the weapon motor.
- **Inner faces**: the drum ends sit about **1–2 mm** from the inner faces of the arms.
- **Function**: they carry the drum ahead of the body and take the weapon's reaction loads straight back into the box corners. The feet are the **front skids**: together with the two rear wheels they form a 4-point stance.

### 2.9 Drum (DR) and ring segments (DR-1…5)
- **Shape**: a **cylinder about Ø 23 mm** (outer diameter of the printed rings), **≈ 76 mm long** between the end of the right ring and the start of the end cap, plus the end cap EC (≈ 9 mm). Total drum length between the arm inner faces ≈ **84 mm**.
- **Construction**: the cylinder is built from **separate printed rings** stacked on the shaft. AWS67 shows joints (each with a steel band) at px x ≈ 330, 660, 950 and 1240, which gives segments of about **20–23 mm** each. In AWS65 there are **5 bands**, so 5–6 segments. The ring faces show **circumferential layer lines** (the rings were printed flat, axis vertical) and the outer surface has fine vertical ridges.
- **Colour**: matt black.
- **Axis**: along X at **(y ≈ +33, z ≈ 13)**. Bottom of the drum ≈ **1.5 mm** above the floor. Top ≈ 24.5, about level with the box top.

### 2.10 Steel teeth (TT-1…4)
- **AWS67 (current version)**: **4 steel strips**, each about **4 mm wide × 1 mm thick**. Each strip **wraps around most of the drum** in a groove/joint between two segments, and its **end is bent outward** to form a **hook or tab** sticking out of the drum surface by **≈ 3–5 mm**. In the photo the tails stick out at the **bottom-front** of the drum (px y ≈ 830–990), at slightly different angles from strip to strip. The strips' outer faces are bright, scratched steel.
- The strip edges in AWS67 also show that each strip has **a small step where it overlaps itself**, which is where the tail leaves the circumference.
- **AWS65**: **5 bands**, look like **thin rings** with small protruding ends at the bottom.
- **AWS66**: **4 flush rings**: shiny bands with no visible hooks (the photo is tiny, so hooks may be there but unresolved).
- **Function**: the tails are the **impactors**. The steel rings also **bind the printed segments** radially, stopping them from bursting under centrifugal load and hits.

### 2.11 Shaft (SH) and end cap (EC)
- **SH**: a **steel rod about Ø 4 mm**, sticking out **≈ 8 mm** beyond the outer face of AR-R (robot right). Plain end, no nut, possibly a **press-fit axle** or held by the clamp bolt.
- **EC**: at the robot's left end of the drum, a **separate black cylinder** about **Ø 22 × 9 mm**, with a **gap of ≈ 2 mm** before the last drum segment. Through the gap a **dark metallic can with a silver ring** is visible (AWS67 px ≈ (1405–1440, 650–770)), which looks like the **bell of a small brushless motor** or a **bearing**.
- **Interpretation (guess, medium)**: the weapon motor **WM** is a small **outrunner (e.g. 1806-class, Ø 23 × 18 mm) mounted on AR-L inside EC**, with the drum bolted to the bell (direct drive). The rest of the drum runs on the steel shaft, supported by AR-R. Alternative (low): an inrunner inside the box with a belt to the drum; no belt is visible, so this is unlikely.

### 2.12 Centre tab / skid (SK), AWS67
- Below the drum, between teeth TT-2 and TT-3 (px ≈ (770–880, 760–890)), a **silver, angular piece** hangs lower than the drum's bottom line. It looks like a **steel plate edge**, about **8 mm wide**, with a **sloped edge**.
- **Interpretation (guess, low–medium)**: the front edge of a **steel floor plate** under the body that extends under the drum, acting as a **centre skid/wedgelet**, or the tail of a tooth seen end-on. Because it appears **between** teeth rather than at a joint, the floor-plate reading is favoured.

### 2.13 Wires and switch
- **Wires**: visible only through the front-wall holes (AWS65: red, blue, yellow, white; AWS67: red, grey). They are presumably the leads between the weapon ESC and the weapon motor, which must cross from the box to the left drum arm. A **cable path** along the inside of the front wall toward the left corner block is likely **(guess, medium)**.
- **Switch**: not visible. Candidates are the clip CL (if it is a link) or a switch on the rear wall **(guess)**.

---

## 3. Per-view sections

### 3.1 AWS67 (front, ≈ 25–30° above, cut out)
- **Top band (px y 60–480)**: the lid with the servo label on the image left half (robot right) and "Recycler 5" on the image right half. The green clip crosses the front edge at px x ≈ 860–1000. The two pink tyres stand up behind the lid's ends (px x ≈ 180–400 and 1480–1570).
- **Middle (px y 380–560)**: the front wall with two rows of dark holes, mostly behind the drum.
- **Bottom (px y 440–1060)**: the drum, spanning px x ≈ 300–1530. Four steel teeth. The right arm with shaft, nut and foot at the image left; the left arm's foot at the image right.
- **Silhouette**: wider than tall, roughly **1.65 : 1**. The drum is the lowest, nearest, widest feature.

### 3.2 AWS65 (front, slightly from the robot's right)
- The same layout. Clearer **hexagonal holes** in the front wall and coloured wires behind them. 5 drum bands. A black clip. The right arm's shaft end at the image left (px ≈ 20–45, 228). The wheels are pink with black side plates, the right wheel's outer guard clearly visible (px ≈ 10–60, 30–140).

### 3.3 AWS66 (front, slightly from the robot's left)
- The same layout, at a small size. A red-labelled servo in the right window, white lettering, 4 flush drum bands, the shaft end at the image left with a nut (px ≈ 70–100, 205–215).

### 3.4 Top view (synthesised)
- An **80 × 34 mm** rectangle (box + lid), with two **9 × 26 mm** wheel rectangles at the rear corners (x ±39 to ±48) and two **thin arm strips** at the front corners running forward to the drum. Across the front, the **drum rectangle (84 × 23 mm)** at y ≈ +21.5 to +44.5. Overall plan **≈ 96 × 70 mm** (y from about −26 for the wheel rears to about +45 for the drum front).

### 3.5 Side view (synthesised, from the right)
- A low box (z 3–27) of 34 mm length; behind its rear lower corner, the **Ø 26 wheel** (its centre at y −12, partly overlapping the box side). In front, the **arm dog-leg** from the box corner down to the **Ø 16 boss** and the **foot** at the floor, with the **Ø 23 drum** behind the arm and the **shaft end** at the boss centre.

### 3.6 Rear view (not photographed; inferred)
- The rear wall of the box between the two wheels; the wheels' rear treads exposed; perhaps a switch or link. The drum is hidden behind the box.

---

## 4. Part table

| ID | Shape | Size (mm, est.) | Ratio to W | Colour / material | Fastening | Qty |
|---|---|---|---|---|---|---|
| BX | box | 80 × 34 × 21 | 0.83 × 0.35 × 0.22 | black FDM (nylon?) | — | 1 |
| FW | wall with holes | 80 × 16, holes Ø 5–6 × ~19 | — | black | integral | 1 |
| LD | plate with windows and lip | 82 × 34 × 3 | 0.85 × 0.35 | black FDM | 4 small screws | 1 |
| LW-R | window | 26 × 14 | 0.27 | — | — | 1 |
| LW-L | slot | 30 × 5 | 0.31 | — | — | 1 |
| CL | bow-tie "L" clip | 8 wide, 28 + 15 long | — | dark green / black | push fit (guess) | 1 |
| SV-R | micro servo | 23 × 12 × 25 | — | grey/white label | in box | 1 (+1 hidden) |
| WH | wheel with pink tyre | Ø 26 × 9 | 0.27 × 0.09 | pink foam/loop tape on black hub | servo/motor shaft | 2 |
| WG | outer wheel plate | 3 × 28 × ~20 | — | black FDM | to box (guess) | 2 |
| AR | dog-leg arm plate | 4.5 thick, ≈ 30 long, 24 tall | — | black FDM | integral with box corner (guess) + clamp bolt | 2 |
| FT | arm foot | 6 wide tip | — | black | integral | 2 |
| DR | stacked ring drum | Ø 23 × 76 (+ EC 9) | 0.24 × 0.79 | black FDM | on shaft | 1 (4–6 rings) |
| TT | bent strip tooth | 4 × 1 strip, tail 3–5 proud | — | steel | clamped between rings | 4 (AWS67), 5 (AWS65) |
| SH | rod | Ø 4 × ≈ 95 | — | steel | clamp in AR-R | 1 |
| EC | end cap | Ø 22 × 9 | — | black | on motor (guess) | 1 |
| SK | plate tab | 8 wide | — | steel | floor plate (guess) | 1 |
| S-LD | small screws | head Ø 3 | — | black | lid to box | 4 |
| S-AR | screw + bolt/nut | M2.5–M3 | — | steel | arm clamp | 2–3 per arm |

---

## 5. Contact / gap matrix (estimated mm; 0 = touching/fastened)

| A ↔ B | Relation | Gap |
|---|---|---|
| LD ↔ BX wall tops | rests on, screwed | 0 |
| LD front lip ↔ FW | overhangs | 3 forward |
| CL ↔ LD top / FW | clipped/plugged | 0 |
| SV-R top ↔ LW-R | sits in window | 0–0.5 |
| AR root ↔ BX front corners | integral or screwed | 0 |
| AR inner face ↔ DR ends | running clearance | 1–2 |
| SH ↔ AR-R boss | clamped | 0 |
| DR rings ↔ SH | on shaft | 0 |
| TT ↔ DR rings | clamped in joints | 0 |
| TT tails ↔ floor | tail tip clearance at bottom of rotation | 1–3 |
| DR surface ↔ FW | gap | ≈ 3–4 |
| DR bottom ↔ floor | clearance | ≈ 1.5 |
| FT tips ↔ floor | rest on | 0 |
| EC ↔ last DR ring | gap | ≈ 2 |
| EC ↔ AR-L | mounted | 0 |
| WH tyre ↔ floor | contact | 0 |
| WH inner face ↔ BX side wall | running gap | 1–2 |
| WH outer face ↔ WG plate | running gap | 1 |
| WH top ↔ LD top plane | stands proud | +1 to +2 |
| WH front ↔ AR root block | gap | ≈ 3 |
| SK ↔ floor | near | 0–1 |

---

## 6. Mechanism

1. **Weapon**: the drum spins about the X axis (**top surface moving forward**, the usual drum direction, so teeth hit the opponent upward **(guess, high)**). The tails of the steel straps are the impact points. A **direct-drive outrunner** in the left end cap is the likely drive. The drum is about 23 mm across, so the tooth-tip speed at, say, 15 000 rpm would be π × 0.029 m × 250 s⁻¹ ≈ 23 m/s **(guess)**.
2. **Drive**: two rear wheels, skid steer. The front rests on the arm feet (and the skid SK if it exists), so the robot **drags its front**. The drive is by converted servos (medium) or N20 gearmotors (medium) **(guess)**.
3. **Invertibility**: the wheel tops stand only 1–2 mm above the lid, and the drum top is roughly level with the lid, so upside down the robot can probably still move, with the drum still able to hit (it then spins in the opposite sense relative to the floor) **(guess)**.

---

## 7. Assembly order (suggested rebuild)

1. Print **BX** with the front wall holes, the front corner blocks and the arms **AR** (one piece, guess) or with separate arms screwed to the corner blocks.
2. Install the **drive servos/motors** at the rear corners, with the output shafts through the side walls. Fit the **wheel hubs**, wrap the **pink tread**, and fit the **outer guard plates WG**.
3. Install the **battery, ESCs, receiver and switch** in the box. Route the **weapon leads** to the left arm.
4. Mount the **weapon motor WM** on the inner face of **AR-L** and fit the **end cap EC** onto it.
5. Thread the **drum rings** and **steel straps** onto the **shaft SH**, alternating ring, strap, ring. Slide the shaft through **AR-R**, engage the drum with the motor bell, and tighten the **clamp bolt**.
6. Fit the **lid LD** with its four screws, then the **clip CL**.
7. Paint "Recycler 5" on the lid.

---

## 8. Profiles as math (for rebuilding curves)

**8.1 Drum ring (XZ disc in the drum frame, axis along X).** Circle **r = 11.5**, centre at (y +33, z 13). Each ring is the extrusion of this circle along X for 20 mm, with a 4.5 mm wide, 1 mm deep groove at each joint for the strap.

**8.2 Steel strap tooth (YZ plane, in drum polar coordinates (ρ, θ), θ measured from +Y toward +Z).**
- Band: **ρ = 11.5** (in the groove, flush) for θ ∈ [θ₀ + 15°, θ₀ + 345°].
- Tail: a straight segment from (ρ = 11.5, θ₀) outward to (ρ = 15.5, θ₀ − 8°), i.e. a **4 mm tooth leaning back by about 30° from radial**.
- θ₀ for the four straps (as photographed at rest, AWS67): **−80°, −95°, −90°, −110°** (all near the bottom-front). For the build, stagger them at **0°, 180°, 90°, 270°** for balance **(guess: a balanced drum needs the tails spread; the photo positions are probably the rest positions after the drum coasted to a stop, or the straps may be in two pairs)**.

**8.3 Drum arm AR profile (YZ plane, extruded 4.5 mm in X at x ∈ [±42, ±46.5]).**
- Root rectangle: y ∈ [+12, +22], z ∈ [10, 24].
- Upper edge: line from (+22, 24) to (+38, 20), then the boss arc.
- Boss: circle centre B = (+33, 13), r = 8.
- Foot: from the boss's lower front, a tapered tip with edges **z = 13 − 2.6·(y − 33)** (front) and **z = 13 − 4.3·(33 − y)** (rear), meeting at **(y +36, z 0)**, i.e. a narrow wedge foot pointing at the floor slightly ahead of the drum axis.
- Lower edge back to the root: line from (+30, 5) to (+12, 10).

**8.4 Wheel tread.** r(φ) = 13 + 0.4·(1 + cos(80·φ)), width 9.

**8.5 Lid outline (XY).** Rectangle x ∈ [−41, +41], y ∈ [−17, +17], corner radius 2. LW-R: x ∈ [+4, +30], y ∈ [−9, +5]. LW-L: x ∈ [−35, −5], y ∈ [−14.5, −9.5]. Front lip: a 3 mm down-stand along y = +17.

---

## 9. Pixel-based measurements (independent check)

**AWS67 (1808 × 1112):**
- Overall image width of the robot: px x ≈ 70 (shaft end) to ≈ 1700 (left corner block). Without the shaft end: ≈ 135 → 1700 = **1565 px**.
- Drum: px x 300 → 1530 = 1230 px long (incl. EC); diameter px y ≈ 450–760 = **310 px**.
- Lid: px x ≈ 280 → 1600 = 1320 px; front edge at y ≈ 470; rear edge at y ≈ 120–150.
- Tyres: image-left (robot right) px x 185–400, y 55–230; image-right (robot left) px x 1480–1570, y 120–400.
- Servo window: px x ≈ 590–870, y ≈ 130–270.
- Arm boss: px ≈ (150–245, 520–700). Shaft: Ø ≈ 30 px.
- Steel strap width: ≈ 50–60 px.

**AWS65 (524 × 374):**
- Robot spans px x ≈ 15 → 505. Drum px y ≈ 165–335 (≈ 170 px), x 50–440. Shaft Ø ≈ 8 px.

---

## 10. Several independent estimates of key quantities

| Quantity | Method A (limits / spec) | Method B (ratio) | Method C (pixels) | Reconciled |
|---|---|---|---|---|
| Overall width | ≤ 101.6 (cube); the robot looks cube-limited in width | — | — | **96** |
| Scale | — | — | AWS67: 1565 px / 96 mm ≈ **16.3 px/mm** (front plane) | 16.3 |
| Drum Ø | spec drum ≈ 24 | D/L ratio 310/1230 = 0.25 × 84 = 21 | 310 px / 16.3 = **19** (+ teeth); AWS65: 170/490 × 96 = 33 (blurred, includes tails) | **23** (body), ≈ 31 over tooth tails |
| Drum length | — | 0.79 W = 76 | 1230 px / 16.3 = **75** (incl. EC) | **76 + 9 EC = 85 → 84 between arms** |
| Shaft Ø | M4 rod typical | 30/310 × 23 = 2.2 (too small?) | AWS65 8 px / 5.1 px/mm = 1.6 | **4** (see §11) |
| Wheel Ø | — | tyre vertical span at the image left ≈ 175 px but seen from above, partly hidden | AWS67 image-right tyre 280 px tall / 13 px/mm (farther) ≈ 22 | **26** |
| Lid width | — | 0.85 W | 1320/16.3 = 81 | **82** |
| Body height | — | AWS67 lid-front to front-wall bottom ≈ 300 px foreshortened | 21 + 3 lid | **24 (+3 clearance) = 27** |
| Strap width | 4 mm flat bar | — | 55 px / 16.3 = 3.4 | **4 × 1** |

---

## 11. Consistency check: conflicts and reconciliation

1. **Shaft diameter**: the pixel estimate (1.6–2.2 mm) is far smaller than a sensible drum axle. The protruding end in AWS67 may be a **thinner stub** (e.g. a turned-down end or a separate pin), or it may be an **M3 bolt shank**. **Reconciled: a Ø 4 axle through the drum, with a Ø 3 visible end.**
2. **Drum Ø (19 vs 23 vs 33)**: the 19 mm figure comes from the front-plane scale, but the drum's top is farther from the camera than its front, so it is slightly under-measured; the 33 mm figure from AWS65 includes blur and tails. **Reconciled: 23 mm body, 31 mm over the tails.**
3. **Teeth at the bottom**: all four tails at the bottom-front of the drum would be badly unbalanced. Either they are actually spread around and the photo catches only those near the bottom (the upper ones being **flush overlaps**), or the straps are **full rings** with short overlaps and the "tails" are only the bent ends. **Reconciled: each strap is a near-full ring with one short radial tail; tails staggered for balance.**
4. **Number of bands (4 vs 5)**: different events, different drum builds. Build **4** (AWS67, the clearest).
5. **Body depth**: never seen. The wheels (Ø 26) sit behind the drum arms' roots, and the lid in AWS67 looks about **0.42 of its width** deep after correcting for the 28° view (≈ 330 px tall / sin 28° → about 700 px → 43 mm, but the top includes the wheel tops). **Reconciled: 34 mm box, total length ≈ 70 mm.**
6. **Weight check**: drum 85 × Ø 23 with ~30% infill PLA/nylon ≈ 15 g, 4 steel straps ≈ 6 g, shaft ≈ 9 g, motor ≈ 18 g, box + lid ≈ 30 g, 2 servos ≈ 22 g, battery ≈ 20 g, ESCs + RX ≈ 12 g, wheels ≈ 6 g: total ≈ 138 g, inside the 150 g limit. **Consistent.**

---

## 12. Why the designer did it (per part, mostly adversarial)

- **Wide drum across the whole front**
  - Attacks: any opponent approaching from the front meets the drum first, so the box, wheels and electronics are reached only from the sides or rear. A full-width drum also means there is no un-weaponed front corner for an opponent to push on.
  - Getting under vs contact: a drum does **not** need to get under. It makes **contact** and throws the opponent up. Its low axle (z = 13) and teeth reaching to ≈ 1 mm above the floor mean even low wedges get hit on their leading edges. The feet keep the drum height fixed.
  - Weakness: an opposing wedge that gets under the **feet** can lift the front and push the robot, with the drum spinning in air. A **vertical spinner** hitting the drum from the front meets a spinning drum: drum-vs-vertical exchanges are energetic and can break the printed rings.
- **Stacked printed rings + steel straps**
  - Construction: easy to print (each ring flat on the bed) and easy to repair (replace one ring). The straps add mass at the largest radius, where it stores the most energy (I ∝ m·r²), and bind the rings together.
  - Adversarial: printed rings alone would shatter on a big hit; the steel straps act as **hoops** holding them together.
- **Steel strap tails as teeth**: cheap, bendable, and replaceable. A bent strap gives a tooth without machining.
- **Drum arms with feet**
  - Attacks: the arms are the load path for every weapon hit, so they are thick (4.5 mm) and short, joining the box at its solid corners. The feet are the front skids; their narrow tips present little for an opponent's wedge to get under, compared with a full-width skid.
  - Weakness: the arms are the most exposed structural part at the corners. A horizontal spinner hitting the corner hits the arm and the shaft end.
- **Shaft end sticking out** (AWS67/65): a weakness. It can catch on walls or be hit and bent. It is probably left long for easy removal of the drum.
- **End cap / direct-drive motor**: no belt to throw or snap. The motor bell carries the drum, so the hit shocks pass into the motor bearings **(weakness)**. The end cap protects the motor's exposed end.
- **Box with honeycomb front wall**: saves weight in a wall that the drum shields from direct hits. It also cools the ESCs. Weakness: debris and opponents' teeth could enter through the holes when the drum is stopped.
- **Lid with servo window**: saves weight and gives clearance for a servo that is taller than the box allows. The servo label on top is exposed to hits from overhead weapons. A window this size lets a hammer or the edge of an arena wall reach the servo.
- **Clip CL**: if it is the weapon lock pin or the link, it must be accessible from the top for safety checks; it is painted green (AWS67) to be seen.
- **Rear wheels, pink foam / loop tread**: soft treads grip well on dusty arena floors. Rear placement keeps the wheels far from the drum and its debris, and puts the robot's weight on them (the drum and arms are at the front, so the centre of mass is mid-length; the front rests on the feet). Weakness: the wheels are exposed at the rear and top. Outer plates protect only the hub.
- **Wheel guard plates**: they hold the outer end of the axle so the wheels do not wobble under side hits; they also protect the hub. A full guard would add weight and width beyond the cube limit, so they are minimal.

---

## 13. Unseen / inner parts (guesses with confidence)

| Part | Guess | Size (mm) | Position (centre, mm) | Confidence |
|---|---|---|---|---|
| Weapon motor WM | small brushless outrunner (1806/2204 class) | Ø 23 × 18 | in EC on AR-L, axis X, (−38, +33, 13) | medium |
| Motor mount | printed boss on AR-L with 2–4 M2 screws into the motor stator base; the drum is bolted to the bell | Ø 20 × 4 | inner face of AR-L | medium |
| Drum bearing | small ball bearing (e.g. 4 × 10 × 4) in the AR-R boss | Ø 10 × 4 | (+44, +33, 13) | medium |
| Drive actuators | 2 × converted micro servos (D0474HT) **or** 2 × N20 gearmotors | 23 × 12 × 25 or 12 × 10 × 25 | (±25, −8, 14), axes along X | medium |
| Motor/servo mounts | printed **plastic cradles** with straps or screw ears in the box floor, 2 × M2 each | 26 × 14 × 6 | under each servo | medium |
| Battery | 2S 7.4 V LiPo, 300–450 mAh (weapon needs current) | 45 × 25 × 8 | centre of the box, (0, −2, 9) | medium |
| Drive ESC | dual brushed ESC (if gearmotors); none needed if servos | 20 × 15 × 5 | (−8, +8, 8) | low |
| Weapon ESC | small brushless ESC (10–20 A) | 25 × 12 × 5 | near the left front corner, (−28, +10, 8) | medium |
| Receiver | 2.4 GHz micro receiver | 20 × 12 × 5 | (+8, −10, 8) | low |
| Switch / link | removable link under CL, or a mini switch on the rear wall | — | (0, +10, 20) or (0, −17, 12) | low–medium |
| Floor plate | thin steel or printed floor, extending under the drum as SK | 80 × 40 × 1 | z 2–3 | low |
| Wiring | battery → link → ESCs; weapon leads (3 wires) along the inside of the front wall to the left corner and out to the motor; drive leads short to the rear corners | — | — | high (exists), low (route) |
