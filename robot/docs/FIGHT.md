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

Per-robot requirements (spec `sim` block; `robot verify --only fight` checks them)
```json
"sim": {
  "forward": [0, 1],                      // robot-frame driving direction
  "strategy": "spinner",                  // spinner | lifter | pusher | flanker
  "drive":  {"max_rad_s": 230, "torque_Nm": 0.05},
  "weapon": {"rpm": 15000, "torque_Nm": 0.12, "spin": 1},          // spinners
  "lifter": {"group": "flipper", "up_rad": 1.2, "down_rad": 0, "torque_Nm": 0.25, "lock": ["horn"]},  // lifters
  "danger": [{"deg": 0, "half_deg": 60, "reach_mm": 75}],          // where opponents must not go (0 = forward)
  "breakable": {"top_panel": 880}                                  // optional override of fastener-derived break N
}
```
Check group `fight` (inner tier): no block = warning (everything guessed); block present but wrong (missing weapon rpm,
lifter group that no part rotates with, unknown breakable id, non-positive break force) = blocker; a weld weaker than
its part's own weight at 40 g = blocker; lists every break force.

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
