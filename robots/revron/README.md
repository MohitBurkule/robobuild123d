# Revron

![Revron](renders/iso.png)

Verifier (`aws2025`): passes. 0 blockers, 144 warnings, 276 checks passed. 50 items NOT CHECKED (see REPORT.md).

Mass 143.6 g (range 123.5 to 163.7 g).

| Top | Exploded | Section |
|---|---|---|
| ![top](renders/top.png) | ![exploded](renders/exploded.png) | ![section](renders/section_z.png) |

## Reference photo overlays (model red, photo blue)

![compare side](renders/compare_side.png)
![compare iso](renders/compare_iso.png)

## Files

- `spec.json`: the full editable design. Load it back with the robot tools to change and re-verify.
- `report.json`, `REPORT.md`: verifier output (REPORT.md ends with what was NOT CHECKED).
- `stl/`: one STL per part (mm, start pose, so they assemble when imported together; wires included).
- `step/`: exact B-rep STEP per part in the start pose, plus `assembly.step` with every part.
- `renders/`: iso, top, back, exploded and section views.

Regenerate: `python3 -m robot export spec.json revron <dir>`

## Iteration 9 changes
- Battery: 2S 350 mAh (lipo_2s_350). power.runtime is about 5.0 min and electrical.runtime is about 3.6 min.
- Weapon: a single 2 mm tooth plate (blade_c, 13.1 g) with no rings. The Ti top plate and a light grey TPU top cover are kept.
- The box is 3.5 mm shorter, which gives a side silhouette IoU of 0.88.
- The 1e3 overlap allowances are gone and every remaining allowance is ≤1.6 mm (shaft and hub seats drawn solid where they carry joint pivots). base_panel and the upright webs are ≥0.9 mm, and upright_l is back to 5.0 mm.
- Known warnings: rotating mass is 13 % of the robot (below the 20 % target, as accepted with option 2), and spinner.reach is a warning at -2.1 mm.
