
## Relativity (round 9)
- Likeness: FAIL (silhouette IoU 0.62/0.67/0.75 vs 0.80; weapon width passes). Verify/fasteners not run (told to focus on look only).
- Generator hspin_bar puts the bar on top with a bridge and wedge; I hand-edited the spec (edit script not kept): removed bridge/wedge/lock plate, hung the bar under the nose, clipped chassis with an outline prism because wedge hinge knuckles floated outside the outline.
- Missing: intent options for under-nose bar, no wedge/bridge, taller rear side walls, open wheel bays (photo has them); `front=none` unsupported.
- `robot` CLI silently skips subcommands on ImportError and a stray PYTHONPATH install exists; run from repo root.

## Round 2
- Merged dev. kit.py only does box/ramp bodies, no pointed plan outline, so I kept the hand-edited gen spec. Likeness still FAIL (3 silhouette blockers).
- diff-photo (read by hand, no key): top lid looks missing/open tray in the model (chassis_top intersect clip likely the cause), blade too small and lacks crescent tips, nose not rounded, rear side walls/wheel pods missing, floating bolts.
- Round 2 fixes: replaced chassis with one solid ruled loft (pointed rounded nose, spline:false is essential, default loft splines into a blob), restored lid, crescent blade under nose, removed bolts/inserts. Scores: aws76 0.81 PASS, aws72 0.67, aws74 0.67 FAIL. Still: rear third, photo has stepped open rear pods.
- Round 3: added handle bar, eyes, rear side walls, hub disc, bigger hooked blade, longer rear. aws76 0.84 pass, aws72 0.66, aws74 0.65 fail. Still differs: wheel pods, bolts cluster, colour, tool orientation.
