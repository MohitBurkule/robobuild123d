# `robot gen build --intent FILE`

One JSON file says what robot you want. Every key is optional except `hypothesis` (or pass `--hypothesis`).

```json
{
  "hypothesis": "hspin_bar",          // preset name or "weapon=wedge,wheel_dia=25,..." (see `robot gen list-hypotheses`)
  "name": "cone",                     // robot name in the spec
  "shape": "round",                   // body outline: box (default) | oval | round
  "outline": [[x, y], ...],           // OR your own outline (counter-clockwise, mm); overrides shape
  "taper": 6,                         // walls lean in: outline shrinks 6 mm from belly to roof (a cone)
  "profile": [[0, 0], [0.5, 1], [1, 8]], // OR any slope: [t, inset_mm], t = 0 belly .. 1 roof (dome, double slope)
  "y0": -48, "y1": 44, "zb": -9, "zt": 9, "axle_y": -14,   // body box overrides (mm)
  "seed": 0, "fixed": {"battery": [x, y]}, "lighten": [], "switch_free": false
}
```

Rules the generator keeps for you (you do not fight them):
- `round` / `oval` are sized to hold the default box and capped at the 150 mm floor square.
- With a slope, parts are laid out inside the smallest section (the roof), so they never poke through the wall.
  Too much taper -> `no wireable layout`: lower `taper` (6-8 mm works for hspin_bar round), or raise `zt`.
- A sloped wall needs no extra bevel: the slope is the ramp.

Try it:
```
python3 -m robot gen build --intent cone.json --out out/ --no-gate   # build only
python3 -m robot gen build --intent cone.json --out out/ --fast      # gated: 0 blockers or exit 2
python3 -m robot render out/hspin_bar.json iso out/iso.png --quick
```

- `teeth`: tooth count of the vspin_drisk single disc (default 2), from the photo.
