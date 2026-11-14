# Undertow

**UNTESTED: never built, run, rendered or verified.**

150 g UK antweight 4WD invertible control bot: four N10 direct-drive wheels inside the outline, TPU tub between
carbon plates, gravity-hinged titanium skirts, and a one-setting front swap (`forks` | `plough`) on a shared pivot pin.
Sized to the robot/profile.py AWS 2025 limit (150 mm floor square, no height limit; forks start down). One setting `rules=aws_v43_cube` switches to the 101.6 mm start cube (attachment folded up). See `BRIEF.md`.

- Masters: `src/undertow/params.py`; swaps: `src/undertow/settings.py` (env `UNDERTOW_SETTINGS`).
- Entry: `src/build_undertow.py` (`build(part=...)`, mirrors Revron's).
- Spec: `spec.json` (hand-written, regenerate after the first real build).
