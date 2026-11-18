# Rammstein struggles
- Generator has no 4WD wedge (BuildError "no assembler"), no wedge length param in intent: built 2WD wedge, make_spec.py adds 2 front idler wheels and scales the wedge ramp prisms (wedge_k) after gen.
- `robot mask` must be run from repo root (cwd elsewhere gives "invalid choice"); reference paths are relative to the spec, not repo root.
- Likeness runs 20-130 s with 4 wheels. Silhouette gate on photo 71 is a razor edge vs template (0.83 vs 0.83 fails on rounding).
- Final: likeness PASS (IoU 0.85 / 0.87). Per coordinator, verify/fasteners NOT run; blocker count unknown.
- Round 2: added carbon top plate (x +-27, rear notch) between the wheel pockets; likeness still PASS. Remaining diffs: no green/black pods with side cutouts, no steel shovel colour, no stickers/screws, wheels slightly large.
- Round 3: wheel_dia 25 (-10%), wedge_k 0.8. Not done: side-pod lobes, full-width foot, rotation, stickers.
