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
