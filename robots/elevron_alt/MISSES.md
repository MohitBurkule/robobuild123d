# Elevron 3.0 Alt: what the relation build misses

Scored against the RVRN_revdev STEP solids (local reference pack, not in the repo) with a mesh boolean IoU
(`trimesh` + `manifold3d`, 0.01 mm tessellation). Revron's RV01 dump replay reached 0.990.

| part | ours mm3 | STEP mm3 | IoU | source of truth |
|---|---|---|---|---|
| chassis | 18272 | 18686 | **0.972** | ELVRN3.0_Alt chassis dump (65 features) + decoded faces/sketches |
| vert_mod | 16394 | 16592 | 0.38 | no dump in the pack; STEP sections only |
| side_r (left = mirror) | 4905 | 5937 | 0.43 | no dump for the "sm" panel; STEP sections only |
| disc | 1127 | 1127 | identical part | Revron `drisk.disc` |

## Chassis: dump feature by feature

| dump feature | status | cause / note |
|---|---|---|
| Sketch1 + Boss-Extrude1 (59 x 66.6 x 17) | present | `CH_W, CH_L, CH_H` masters |
| Fillet1 R2 front verticals, Chamfer1 C2 top edges | present | `CORNER_R`, `EDGE_CH`; the rear chamfer plane is carried over the tabs (Chamfer3) |
| Cut-Extrude1 (Sketch2: walls, 2x2 columns on 50 x 32, 10.2 x 23 axle bays, 2.9 bores) | present | `POST_PITCH`, `BAY_LEN`, `BAY_X0`; column web to the wall is a straight block, the dump's web has R1.5/R2 blends (Fillet2/3): **fillet** |
| Cut-Extrude2 rebate 1 x 2 | present | front corners concentric with Fillet1 (fixed after visual.ligament flagged the 0.58 mm corner) |
| Cut-Extrude3 keyholes (6 bore, R1.8 slot, 4 drop) | present | |
| Cut-Extrude4/5 boss holes, hex nut pockets | present | pocket phase set by the catalog nut (`HEX_PHASE`) |
| Boss-Extrude2 R5 obround + Fillet5 R3 root | present | |
| Cut-Extrude15 boss window + Fillet12 R1 | window present, **R1 corners missing** | fillet; reference_cad.radii lists them |
| Cut-Extrude6 switch slot + 1.7 pilots | present | |
| Cut-Extrude17 wire slot | present | |
| Cut-Extrude7/14/16 deck lattice (Sketch9/18/20, 92 arcs) | present as relations | centre cells shrink one column radius (3.1) off the post-to-post diagonals; end cells 2.05; corner pockets end at the axle-bay walls. Window tips differ by up to ~0.6 mm: **point table** in the dump vs our offsets |
| Boss-Extrude3 + LPattern1 + Mirror7 rear tabs, Chamfer5 lead-ins | present | the inner tabs' round end (Fillet8 R2 around the cross-bolt hole, y to 42.5) is a square end here: **fillet** |
| Boss-Extrude4 end columns | present | |
| Sketch15/16 Boss-Extrude5/6, Cut-Extrude8/9/10/13 | **not reproduced** | Sketch10/14/15/16/17 decode with "D=0" or no dims (low confidence); the STEP shows small blends at the tab roots and the backing-plate seat. Remaining 3 % volume |
| Fillet4/6/8/9/10/11/13/14/15 small blends (R1 to R2) | **missing** | fillet; listed by reference_cad.radii when the pack is present |

## vert_mod (no dump)

Built from relations to the chassis and the weapon axis: a frame on the deck with legs to the four column screws, a
hollow shell sloped from 22.5 to 30 high, a rear bulkhead, two uprights (web 3 mm, full 6 mm round the motor-can
pocket and the lead slot; the right one only round the MF85 seat), prongs between the chassis tabs that carry the
cross-bolt nuts, and a phase-lead duct. Differences from the STEP: the STEP uprights are C-channels with a separate
outer flange, its frame is a curved lattice, its shell has a stepped front and two obround wire windows in the
bulkhead. Our module is lighter in the frame and heavier in the duct. **Open item: needs the vert_mod dump** (the port
guide lists it as unmatched).

## Side_Panel_alt_sm (no dump)

Plate on the side boss, battered skin outside the rear tyre, crossbar behind it and a fork prong to y 98.6. The STEP
panel is an organic TPU part (curved skin, flared fork root, arrow tip); ours keeps the envelope, attachment and fork
reach. **Open item: needs the panel's dump or point tables of its loft sections.**

## Deliberate design decisions (not misses)

- BE1806: the catalog can is 18.5 mm against the STEP's 15.5 mm; its base sinks 2.8 mm into a pocket in the left
  upright so the disc stays on the STEP bell face.
- The motor is turned so its phase leads point forward into a duct (the STEP shows no leads).
- Cross bolts: one M3x12 per side through the pod land and the outer tab into a nut captive in the module prong (the
  STEP has no fasteners; a nut in TPU fails `arch.tpu_threaded`).
- Base panel: 1 mm printed panel in the rebate (the STEP has none).
- Front wheels idle on the standoff (two N10 in the STEP).

## Checks added from what the eye found

- `robots/elevron_alt/tests/test_relations.py`: chassis envelope and volume vs the STEP (3 %), lattice windows clear
  the ribs, N10 gearbox on the wall, weapon stack contiguous, pods one solid and mirrored, module prongs inside the
  tab gap, tyres on the floor.
- `robots/elevron_alt/tests/test_sweep.py`: master sweeps rebuild valid single solids.
