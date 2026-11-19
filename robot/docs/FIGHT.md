# Fight simulation (`robot.fight`, MuJoCo + breakable welds + scripted drivers)

```
pip install -e .[robot,sim] imageio imageio-ffmpeg
MUJOCO_GL=egl python -m robot.fight robots/revron/spec.json robots/expandabot/spec.json --seconds 20 --seed 2 \
    --out fight.mp4 --json fight.json
```

What it does
- Loads both specs through `robot.sim` (per-part mass/inertia from the verifier, hulls for collision, wheel/weapon hinges).
- **Damage**: every breakable part (kinds armor, wedge, fork, plate, or listed in `sim.breakable`) is its own free body
  welded to the chassis. Each step the weld force is read; above the part's break force the weld switches off and the
  part flies free (chopped off). Sturdy robots keep their welds and get thrown whole. Break force default = sum over the
  fasteners through the part (`profile.FASTENER_N`: M2 220 N, M3 400 N ...), else 120 N (clip/glue).
- **Weapons**: spinners are velocity servos with the motor's torque cap; spinner parts are split into angular sector hulls
  so teeth keep a bite face (a convex hull of a toothed disc is a smooth cam). Lifters/flippers are position servos.
- **Contacts**: 0.3 ms contact time constant at a 0.1 ms step (impacts are ~0.1-0.5 ms; MuJoCo's 20 ms default turns hits
  into pillows and weld forces never reach break level).
- **Drivers** (`brains.py`): each robot reads the *opponent's* declared danger arcs, picks the safest attack bearing
  (furthest from them), orbits outside the danger reach to get there, then turns in. Spinner: spins up first, backs off
  when the weapon slows, re-engages. Lifter: fires only when the opponent's COM is over the plate and touching it;
  fires to self-right when upside down. Impatience timer: charges anyway after 4 s.
- **Judging**: out of the arena loses, then stuck upside-down loses, then parts knocked off + weapon energy delivered.
- Output: JSON with events (hit J, fire, break N), peak tilt/lift per robot, weld peaks, which spec fields were guessed.

Real-world effects modelled
- **Gyroscope**: full rigid-body dynamics, so a spinning disc resists turning and tips the robot (test: a turning
  vertical spinner tips ~2x further with the disc spinning; Revron 15 deg -> 28 deg).
- **Motors** (`physics.py`): DC curve per driven hinge (torque falls linearly to zero at no-load speed), ESC current limit,
  brain commands are throttle like an RC stick. Weapon throttle = declared rpm on a full pack, so speed sags with the
  battery and drops on each hit, then re-spins at the motor's real torque.
- **Battery**: LiPo OCV vs charge, internal resistance sag under current, charge used (mAh).
- **Heat**: I^2R into a thermal mass with copper resistance rise; above the cut-out temperature the motor dies.
- **Weapon wobble**: centre-of-mass offset (imbalance), weapon on a carrier with radial and tilt springs (bearings +
  uprights flex). Same model in `wobble.py` for the `wobble` check (spin-up, one rim hit, real-mesh swept clearance).
- **Contacts**: 0.3 ms impact time constant with damping ratio 0.5 (some bounce), tyres mu 1.2, plastic/steel 0.5.
- **Arena**: closed box with roof, steel floor with 0.4 mm seams every 300 mm.
- Output JSON `electric`: battery V, charge left, each motor's temperature and whether it burnt out.
- **Blade flex**: weapon contacts are softer (`sim.weapon.blade_tc`, default 0.4 ms): a thin disc gives on impact.
- **Hazards** (`hazards.py`, thresholds in `sim.hazards`):
  - debris: a broken-off part collides with its OWN robot too once it is 5 mm clear of its seat, so it can wedge
    into a wheel or the weapon; a commanded driven hinge stalled 0.3 s while touching debris logs a `jam`;
  - tyre damage: an opponent's weapon hitting a tyre over 250 N cuts it; grip falls with damage, 0.2x when destroyed;
  - power switch: a hit over 60 N landing within ~14 mm of the switch knocks it off: robot dead, all motors cut;
  - wires: a hit over 200 N within 6 mm of a wire's route cuts it; power line = robot dead, motor lead = that side,
    weapon lead = weapon, servo lead = no flipper;
  - driver: 150 ms reaction delay with steering noise; brains steer on predicted positions (own yaw rate, target v).
  - JSON `hazards`: dead (why), tyre damage, wires cut, debris live. Judge: a dead robot loses.
- Not yet: plate bending (FEM), belt throw, radio dropouts, battery puncture/fire.

Physics from data, validated (no per-robot tuning)
- Friction and restitution per part come from its spec `material` (`materials.py`, published values, sources in the
  file); the floor is set below every material so each part's own value touches it.
- Exact (elliptic) Coulomb friction cone; multi-point convex contacts (thin fork tips sliding under an edge).
- `test_ramp_lift_matches_incline_physics`: a block pushed into a ramp starts climbing exactly at
  F = m g (sin + mu cos) / (cos - mu sin) (checked at 15/20/30 deg, mu 0.35/0.8). Forks and wedges get under opponents
  from this physics, not from any fork-specific rule.
- Drivers push through on contact (no back-off while touching).
- Step 50 us with 0.3 ms contacts; on a solver blow-up (a violent pinch) the fight rolls back to the last 20 ms
  checkpoint and redoes it at a quarter step (adaptive stepping); `solver_retries` in the JSON. Before this, blow-ups
  silently restarted the fight from t=0.

Self-audit: what is still simplified (biggest first)
1. Collision shapes are one convex hull per part: pockets/slots in a tub are filled in (CoACD decomposition next).
2. Parts are rigid until a joint breaks: no bending/denting (needs FEM, OpenRadioss blocked here); break limits are
   hand values from fastener ratings.
3. One contact stiffness (0.3 ms) for all materials: TPU should be softer/longer than steel.
4. Robot-vs-robot friction uses the larger of the two materials (MuJoCo combine rule), not a pair table.
5. Tyres are rigid hulls with one mu: no contact patch, no load sensitivity, no rolling resistance.
6. Weapon losses only through the motor model: no bearing friction or air drag.
7. Motors: no winding inductance, ESC braking or brushless timing; gearbox losses folded into the curve.
8. Wire routes are straight lines between part centres and via points.
9. Hits are measured from weapon speed drops; arena has no pits or hazards; drivers are scripted.

Per-robot requirements (spec `sim` block; `robot verify --only fight` checks them)
```json
"sim": {
  "forward": [0, 1],                      // robot-frame driving direction
  "strategy": "spinner",                  // spinner | lifter | pusher | flanker
  "drive":  {"max_rad_s": 230, "torque_Nm": 0.05},
  "weapon": {"rpm": 15000, "torque_Nm": 0.12, "spin": 1},          // spinners
  "lifter": {"group": "flipper", "up_rad": 1.2, "down_rad": 0, "torque_Nm": 0.25, "lock": ["horn"]},  // lifters
  "danger": [{"deg": 0, "half_deg": 60, "reach_mm": 75}],          // where opponents must not go (0 = forward)
  "breakable": {"top_panel": 880},                                 // optional override of fastener-derived break N
  "battery": {"cells": 2, "mAh": 180, "r_int_ohm": 0.08},
  // weapon extras: "motor": {"kv": 3800, "r_ohm": 0.12, "i_max_a": 30}, "imbalance_mm": 0.05, "mount_k_Npm": 2e5,
  //   "tilt_k_Nm": 20, "play_mm": 0.02, "hit_N": 1500
  // drive extras: "motor": {"no_load_rad_s": 250, "stall_Nm": 0.06, "stall_a": 1.6}
}
```
Check group `fight` (inner tier): no block = warning (everything guessed); block present but wrong (missing weapon rpm,
lifter group that no part rotates with, unknown breakable id, non-positive break force) = blocker; a weld weaker than
its part's own weight at 40 g = blocker; lists every break force.

Check group `wobble` (full tier, spinners): MuJoCo spin-up with imbalance + mount flex, one rim hit, then the real weapon
meshes (every part, full detail) swept through a turn at the peak deflection and tilt; any static part touched is a
blocker (a warning while mount stiffness / hit force are guessed). Spin frequency within 15 % of the mount's natural
frequency = resonance warning. Revron today (guessed values): 0.09 mm steady wobble, 3.4 mm / 13.6 deg after a 1500 N hit,
the weapon then touches mount_l and the tub.

Calibration (OpenRadioss, `robot/fight/radioss.py`, `tools/openradioss/`): explicit FEM of a tooth hitting a clamped
printed plate, swept over material/thickness/speed, written to `robot/fight/data/impact_table.json` for the weld layer.
Not yet run: the OpenRadioss binary download is blocked from the cloud sandbox (GitHub releases 403); run
`tools/openradioss/setup.sh` then `python -m robot.fight.radioss` on a machine with GitHub access.

Speed: ~0.2-0.3x real time on 4 CPU cores for two robots (20 s fight = 65-90 s). Seeds run in parallel.

Limits / next
- Break limits are hand values until the OpenRadioss table exists; parts break whole (Voronoi pre-cut chunks next).
- Collision = convex hulls per part (CoACD decomposition next for concave tubs).
- Electronics damage (battery/ESC hit = robot dead), wire cuts, belt throws not modelled; no motor curves.
- Ripsaw and Scythe specs currently fail to build (CAD errors), so they can't fight yet.

## Arenas (`--arena`)

Real UK antweight arenas are not all closed boxes. Many have a drop-off edge or a pit, which is how pushers and wedges
win. Presets in `robot/fight/arenas.py`. In each one the platform top is at z=0, with a lower floor 100 mm down.
If a robot's COM drops below -30 mm, it has touched the floor outside the arena. That is an immediate loss, even if it
bounces back. The fight stops 0.5 s later. `judge` checks this before anything else: the first robot out loses.

| preset | layout | source |
|---|---|---|
| `closed` (default) | 1.2 m box, walls + roof | old behaviour |
| `aws2025` | 1.0 m square, 300 mm walls + lid, 400 mm drop-off slot on the east edge, 200 mm square pit | AWS 2025 rules: arena at least 750 mm (1 m recommended), at least one unwalled 200 mm gap for a pit/drop-off ([rules PDF](https://www.robotwars101.org/wp-content/uploads/2024/10/AWS-Rules-2025-211024.pdf), [AWS World Series 2025](https://bristolbotbuilders.com/wp-content/uploads/2025/06/Antweight-World-Series-Rules-2025-050625.pdf)) |
| `aws_classic` | 762 mm platform, south and east edges open (50 % of the perimeter) | older AWS rules ([v2.3](https://robotwars101.org/ants/rules23.htm), [v4.2](https://robotwars101.org/ants/rules-42.htm)); [antweights wiki arena page with photos](http://www.antweights.co.uk/doku.php?id=antweight_arena) |
| `beetle_champs` | 1.2 m walled box, 300 mm out-of-the-arena gap, 250 mm pit whose cover drops at 30 s | Bristol Bot Builders events: OOTA zone plus a pit switched on partway through; touching the pit floor = out ([programme](https://bristolbotbuilders.com/programme/)) |

Other rule sets agree that touching the pit or outside floor loses: [CCRL](https://www.flsbattlebots.cz/en/rules/antweight), [SCAR](https://www.socalattackrobots.com/2025-ruleset.html), [NERC](http://www.nerc.us/rules2.htm).
SCAR's exact pit wording was not found.

Brains:
- **Pusher (the default for wedges):** picks the hazard nearest the opponent (an open pit centre or a spot just past an
  open edge span). It drives round to the far side of the opponent and pushes through towards that hazard.
- **Every brain:** has an edge guard. If the front (or back, when reversing) edge of its own body would leave the
  platform, it backs off.

Simplifications:
- Every preset has a lid at wall height, and the gaps are slots under it. Without the lid, spinner recoil threw robots over
  the walls, which enclosed arenas prevent.
- Pits are square holes and walls are thin boxes.
- There are no arena hazards beyond pits and edges (no spikes or hammers).
- The pit floor is a box; no padding is modelled.
