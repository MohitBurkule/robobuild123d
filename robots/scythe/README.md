# Scythe

Scythe is a 150 g UK antweight (AWS 2025: 150 mm floor square from `robot/profile.py`) horizontal undercutter
bar spinner. A 57 mm (energy- and pitch-limited, derived), 3 mm Hardox two-tooth bar spins under the tub,
cantilevered on the weapon motor's own extended 3 mm shaft (motor-as-hub, the reference hspin_bar topology).
2WD on N10 gearmotors behind the sweep; invertible (wheels protrude top and bottom). Verified gate-clean:
`robot verify robots/scythe/spec.json` -> 0 blockers (237 warnings). Design, load paths, mass and energy are
in [BRIEF.md](BRIEF.md).

Code: `src/build_scythe.py` provides `build(part=...)`, built from `src/scythe/`. `make_spec.py` (run from the
repo root) regenerates `spec.json` from `src/scythe/params.py`:

```
LD_LIBRARY_PATH=/tmp/usrlib/usr/lib/x86_64-linux-gnu .venv/bin/python robots/scythe/make_spec.py
```

| File | Contents |
|---|---|
| `params.py` | masters and relations (all poses derive from these) |
| `bar.py` | the bar |
| `weapon_hub.py` | the turned hub on the motor shaft |
| `tub.py` | the tub: sloped disc + rear pod, motor housing tube, weapon boss, wire slots, N10 cradles/reliefs, skid pads |
| `drive.py` | the drive |
| `panels.py` | the top panel |
| `assembly.py` | the assembly, with joints |
| `variants.py` | the variants |

## Iterating with the jiggle solvers (PR #83 / #84)

Measured, not hand-computed:

```
# part-level nudges (PR #83): moves parts with numeric `at`, reports the shift
PYTHONPATH=<dev worktree> .venv/bin/python -m robot jiggle robots/scythe/spec.json --clear 1.0 --json /tmp/j.json

# named-param solve (PR #84): damped least squares over a master; pockets/holes/placements re-derive.
# make_spec.py writes an expr-placement variant with SCYTHE_EXPR_SPEC=robots/scythe/jiggle_spec.json
PYTHONPATH=<dev worktree> .venv/bin/python -m robot jiggle robots/scythe/jiggle_spec.json \
    --param src/scythe/params.py:POD_W_MIN=65:78:0.5 --clear 1.0 --params-only --write-params
```

`POD_W_MIN` was set this way (bell-to-N10 gap: 0.64 mm at 65, 1.79 at 68, 2.57 at 70; kin.rub_gap needs 1.0).
Then re-run `make_spec.py` and `robot verify`.

## Status
- `spec.json` is generated, not hand-written; edit `params.py` and re-run `make_spec.py`.
- Full verify: 0 blockers, 0 parity blockers. `renders/iso.png` is rendered with all 7 wire routes drawn.
- Not yet built or fought: masses of printed parts are model-derived estimates.
