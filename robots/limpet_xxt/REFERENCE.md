# Limpet XXT: references, and what is known vs guessed

**UNTESTED copy.** No CAD from the builders exists or was used. No photos are committed, only links.

## Identity and ownership
- **Team: Team 13** (John M Denny, Hinckley, Leicestershire). Source: the AWS fan wiki robot page infobox and the
  Team 13 team page.
- The brief suggested "Team Bits Everywhere". **No source found links Limpet XXT to Team Bits Everywhere.** Searching
  the AWS wiki for "Bits Everywhere" returned no team page. Treat that attribution as unverified, and probably wrong.
- Lineage: it replicates Team 13's Robot Wars Series 2 heavyweight **Limpet** (1998, tracked, white with black zebra
  stripes). Sister robots: Limpet XL (featherweight) and Limpet XS (beetleweight). Team 13 also runs Ant Ratchet,
  No Parking, Ant Clank and others.
- Record per the wiki: AWS 46–78, 29 wins / 24 losses on the robot page (the team table says 19/16, so the wiki
  disagrees with itself).

## Design history (wiki text)
- AWS 46–47: six wheels at first, then four. Wedge, then a rear-hinged flipper.
- AWS 53 onward: a **front-hinged flipper**, which makes it "look like Storm 2". It self-rights (the AWS 53 fight
  text describes repeated self-righting).
- The wiki category list says "Weaponless Robots" and also "Front-hinged Flippers". The infobox gives the weapon as
  "Flipper/Vertical Spinner", which looks like a template error, since no photo shows a spinner.

## Sources
| what | link | access |
|---|---|---|
| AWS wiki robot page | https://aws.fandom.com/wiki/Limpet_XXT | WebFetch 402; read via `api.php?action=parse&page=Limpet_XXT&prop=wikitext` |
| Team 13 page | https://aws.fandom.com/wiki/Team_13 | same, via api.php |
| AWS 71 event | https://aws.fandom.com/wiki/AWS_71 | search result only |
| Original heavyweight Limpet | https://robotwars.fandom.com/wiki/Limpet | via api.php |
| Archive snapshot | http://web.archive.org/web/20260706195414/https://aws.fandom.com/wiki/Limpet_XXT | listed by the archive.org availability API; not fetched |
| Photo AWS 76 | https://static.wikia.nocookie.net/aws/images/2/2f/Limpet_XXT.aws76.jpg | viewed |
| Photo AWS 74 | https://static.wikia.nocookie.net/aws/images/8/8b/Limpet_XXT.aws74.jpg | viewed |
| Photo AWS 72 | https://static.wikia.nocookie.net/aws/images/3/3e/Limpet_XXT.aws72.jpg | viewed |
| Photo AWS 71 | https://static.wikia.nocookie.net/aws/images/d/d5/Limpet_XXT.aws71.jpg | viewed |
| Photo V3.1 (AWS 67, lid off, wiring visible) | https://static.wikia.nocookie.net/aws/images/8/81/Limpet_XXT_V3.1.jpg | viewed |
| Photo V3.0 (AWS 64, Team Panoramic photo) | https://static.wikia.nocookie.net/aws/images/a/af/Limpet_XXT_V3.0.jpg | viewed |
| Photo AWS 53 | https://static.wikia.nocookie.net/aws/images/b/b1/Limpet_XXTaws53.jpg | viewed |
| Rules (current) | repo draft PR #77: 150 mm floor square, no overhang, no height limit, 150 g | coordinator note |
| Rules (old) | AWS v4.3 §2b: 101.6 mm cube at start, any orientation | coordinator note |

## Rule era
The copy defaults to the **2025 AWS rule** (`RULE_ERA = "aws_2025"`: 150 mm square). The robot itself was built and
campaigned mostly under **v4.3** (4 in cube). The default dimensions (100 × 96 × 24 mm) satisfy both rules, and
`params.check()` tests the selected era.

## SEEN-IN-PHOTO (architecture; no absolute dimensions)
- A box chassis with **four wheels at the corners**. The wheels sit between the tub and the side plates, with tyres
  proud of the top and bottom, so it can run inverted. Wheels are white or black printed with treaded tyres (aws71–76).
- **Outboard clear side plates** in an elongated hexagon (chamfered corners), bolted with domed screws (one at
  mid-length on every version, plus more near the ends).
- A **full-width front flipper/wedge** of clear sheet with chamfered front corners. Its rear edge is at the top front
  of the body, and at rest it slopes to the floor. It sits between the side plates.
- **Two lid plates with a centre slot** running the length of the body. A long bar (black on aws71/V3.1, white on
  aws72/74) is visible in the slot.
- V3.1 (lid off): a long black block in the centre (read as the battery), a red-labelled servo beside it, a small
  PCB, and twisted motor leads to the corners.
- Materials: clear polycarbonate with zebra/leaf vinyl decals; a printed tub (dark green/black on aws76, white
  internals on aws72/74).
- Proportions read off the three-quarter photos: plan roughly square; flipper about 1/3 of the length; body height
  about 1/4 of the width.

## GUESS (everything numeric, plus the inner layout)
- **Every mm value is a GUESS.** No photo has a scale reference. The scale assumes the plan view nearly fills the
  4 in cube, which is typical for UK ants.
- OVERALL_L 100, OVERALL_W 96, WHEEL_D 24, WHEEL_W 8, WHEEL_PROUD 1.5, SHEET_T 2.0, LID_T 1.5, FLIP_TIP_LIFT 0.5 and
  FLIP_SIDE_GAP 1.0 are all GUESSES. FLIPPER_SHARE 0.32 and the chamfer fractions are PHOTO proportions at a GUESS
  scale.
- Four N10 300 rpm motors, one per wheel, are a GUESS. Drive is not visible. The photos show 4 wheels and leads to
  each corner.
- The SG90-class servo is a GUESS. A servo is visible on V3.1, but its model is unreadable.
- The flipper drive (tail lever on the hinge block, pushed by a servo horn pin) is a GUESS. It explains the bar seen
  in the lid slot, but that bar may be the battery cover.
- The 2S 180 mAh battery, Malenki Nano ESC and BBB switch are GUESSES based on common UK ant practice.
- Side-plate fixing uses a mid-wheelbase standoff with two screws (GUESS). The photographed end screws are not modelled.
- FLIP_OPEN_DEG 90 is a GUESS.
