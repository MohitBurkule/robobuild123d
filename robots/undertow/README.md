# Undertow (4WD invertible wedge / control bot)

![Undertow (4WD invertible wedge / control bot)](renders/iso.png)

Verifier (`aws2025`): has blockers. 26 blockers, 230 warnings, 340 checks passed. 55 items NOT CHECKED (see REPORT.md).

Mass 140.4 g (range 129.8 to 151.0 g).

| Top | Exploded | Section |
|---|---|---|
| ![top](renders/top.png) | ![exploded](renders/exploded.png) | ![section](renders/section_z.png) |

## Files

- `spec.json`: the full editable design. Load it back with the robot tools to change and re-verify.
- `report.json`, `REPORT.md`: verifier output (REPORT.md ends with what was NOT CHECKED).
- `stl/`: one STL per part (mm, start pose, so they assemble when imported together; wires included).
- `step/`: exact B-rep STEP per part in the start pose, plus `assembly.step` with every part.
- `renders/`: iso, top, back, exploded and section views.

Regenerate: `python3 -m robot export spec.json undertow <dir>`
