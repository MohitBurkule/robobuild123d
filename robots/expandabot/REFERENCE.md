# Expandabot: reference record

## Identity
- **Robot:** Expandabot (also spelled *Expanda-bot* on Rampage and the AWS Wiki)
- **Builder / team:** Adam Stanley — **Team Bits Everywhere** (alongside Dylan Stanley; team robots include *Ice Breaker Junior*, *Bolt*, *Smashie + 1*, *Iceberg*, *Tip & Pit*)
- **Class:** UK antweight, 150 g roller (two-wheeled clamp and rear-hinged flipper)
- **Inspired by:** Team Lobster's UK *Robot Wars* Series 4–8 heavyweight **Thermidor 2** (lobster-styled two-wheeled chassis with a central rear-hinged flipper scoop and flanking horizontal clamping pincers)
- **Active:** AWS 62 (2020) – AWS 79 (2026); also campaigned at Ant Freeze 8–11, ORCS 2–11, and GRoCS
- **Honours:** **8-time Antweight World Series Champion** — **AWS 64** (plus Best Driver award), **AWS 67**, **AWS 69**, **AWS 70**, **AWS 71**, **AWS 72**, **AWS 74**, and **AWS 76**

## Sources
| Source | URL | Status |
|---|---|---|
| AWS Wiki page | https://aws.fandom.com/wiki/Expandabot | read |
| Photo AWS 77 (infobox three-quarter view) | https://static.wikia.nocookie.net/aws/images/e/ea/Expanda-bot.aws77.jpg | referenced |
| Rampage AWS 79 entrant list | https://www.rampagebots.co.uk/member/events/entrants/361 | read |
| Thermidor 2 reference (Robot Wars Wiki) | https://robotwars.fandom.com/wiki/Thermidor_2 | read |
| Repo taxonomy (`antweight_taxonomy.json`) | `robot/gen/data/antweight_taxonomy.json` (`Expandabot`: `grabber_clamp + rear-hinged flipper`, `2-wheel`) | read |
| Rules (current) | `robot/profile.py` `aws2025`: 150 mm floor square, no overhang at any height, no height limit, 150 g | repo rule |
| Rules (historical) | AWS v4.3 §2b: 101.6 mm (4 in) cube at start in any orientation, 150 g | coordinator note |

## Rule era
The CAD model defaults to the **2025 AWS rule** (`RULE_ERA = "aws_2025"`: 150 mm floor square, no overhang at any height, 150 g). Because Expandabot won the majority of its titles under **AWS v4.3** (the 4 in / 101.6 mm start cube rule, from which the "Expanda-bot" name derives), the default rest footprint (`98.0 × 96.0 × 28.0 mm`) fits cleanly inside both the 101.6 mm start cube and the 150 mm floor square. `params.check()` verifies the active rule era.

## SEEN-IN-PHOTO & WIKI RECORD (architecture; no absolute dimensions)
- **Two-wheeled drive (2WD)** positioned toward the rear/flanks of a low, sloped lobster-style body, resembling *Thermidor 2*.
- **Central rear-hinged flipper scoop:** hinged near the top rear of the body, sloping forward and down to a wide front scoop lip near the arena floor. Fired upward from the front to launch opponents into the pit or out of the arena, and used to self-right when inverted (documented across AWS 62–77 fight logs, e.g. self-righting against *Delta V*, *Forky*, *Whopper BVM*, and *Jungle Man*, and lifting *GNC* even while clamped).
- **Left and right horizontal clamping arms / pincers:** flanking the central flipper scoop on the left and right sides ahead of the wheels, curving inward toward the front scoop tip like *Thermidor 2*'s lobster claws. Documented in AWS fight logs (*"shattered Expanda-bot's left-grabbing arm"* vs *Stewie* in AWS 62; *"grasp it on the right-clamping-arm"* vs *Little Devil* in AWS 64; *"got its right-clamp caught in a gap in the wall"* vs *ArmamAnt* in AWS 68). The claws guide opponents onto the central flipper scoop while shielding the two rear wheels from frontal and angled spinner attacks.
- **Rounded rear shell / skid:** allows the robot to rock back and self-right cleanly when the rear-hinged flipper fires while overturned, matching *Thermidor 2*'s Series 5–8 rounded carapace.

## GUESS (every numeric dimension and internal COTS packaging)
- **Every millimetre value is a GUESS.** No public engineering drawings or scale references exist for Expandabot. Dimensions are scaled so the complete rest envelope (`100.5 mm` rest length × `96.0 mm` wide × `26.0 mm` wheel OD) fits inside the 101.6 mm (4 in) v4.3 start cube and the 150 mm aws2025 floor square.
- **COTS selection (GUESS from standard UK antweight practice):**
  - Drive motors: 2 × N10 micro-metal gearmotors (`n10_300rpm_6v`) mounted axially in snug closed-top pockets near the rear axle line.
  - Wheels: 2 × 26 mm × 8 mm TPU tyres (`wheel_l`, `wheel_r`) with D-bores directly on the N10 output shafts, protected outboard by 2 mm polycarbonate side guard plates (`side_l`, `side_r`) on four standoff columns per side.
  - Flipper actuator: 1 × SG90-class micro servo (`servo_cs07`) mounted on its side in the central channel, driving the central flipper (`flipper`) via a printed horn (`horn`), steel M2 drive pin (`drive_pin`), and printed hinge block (`hinge_block`) with a push-only tail lever.
  - Electronics: 2S 180 mAh LiPo battery (`lipo_2s_180`), Malenki-Nano combined receiver + dual ESC (`malenki_nano`), and BBB screw-on antweight link/switch (`switch_bbb_ant_rvrn2`) accessible through the top right lid slot.
- **Clamping arms (`clamp_l`, `clamp_r`):** modelled as a mirrored pair of 2 mm polycarbonate lobster-claw wedge arms bolted to sloped front mounts on the tub with 3 × M2 screws into brass heat-set inserts per side (matching *Thermidor 2*'s flanking claws that funnel opponents onto the central flipper scoop).
