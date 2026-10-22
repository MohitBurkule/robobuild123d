# Elevron 3.0 "Alt": reference

150 g UK antweight vertical spinner (AWS 2025). Source data (kept out of the repo): `RVRN_revdev.STEP` (20 solids),
the ELVRN3.0 part dumps and their decoded faces/sketches. Frame: X lateral, Y forward (weapon end), Z up. The STEP
frame has the chassis underside at z 0 and the floor at z -2.25; the robot world lifts it by `FLOOR_LIFT = TYRE_R - AXLE_Z`.

## Intake (STEP solids)

| STEP solid | vol mm3 | dump / source | class | built by |
|---|---|---|---|---|
| Alt_chassis | 18686 | ELVRN3.0_Alt chassis (18686.4, 65 features) | custom PLA | `chassis.py` (relations, IoU 0.970) |
| vert_mod | 16592 | none in the pack (unknown) | custom PLA | `vert_mod.py` (relations from STEP sections, IoU 0.47) |
| Side_Panel_alt_sm / Mirror | 5937 / 5936 | none ("ELVRN3.0_Side Panel" is a larger family member, 8437 mm3, loft/wrap) | custom TPU | `side_panel.py` (IoU 0.45), left = mirror |
| RV12_N10_2200_RPM x2 | 1810 | Revron | COTS `n10_2200rpm_spicy` | catalog |
| RV08_1806_Brushless | 6374 | Revron family | COTS `be1806_bbb` | catalog |
| Drisk_floating_3 | 1127 | Revron | Hardox disc | `revron.drisk.disc` (1127.0, identical) |
| spiderSL | 1095 | uploaded spider.STEP is Revron spider_1 (1218) | aluminium | `revron.drisk.spider` (1239, see MISSES) |
| RV21_Rear_Wheel x2 | 1501 | Revron | printed hub | `revron.hubs.rear_hub` |
| RV22_Scalextric_F1_Front_tyre x4 | 2202 | Revron | COTS tyre | `revron.hubs.rear_tyre` |
| RV07_Prop_mount | 632 | motor kit | COTS alu | `assembly.prop_mount` (flange + spigot) |
| FS4_MF85ZZ | 84 | catalog BEARINGS mf85 | COTS | `assembly.bearing` |
| 10mm_standoff_3m_alu | 120 | | COTS | `assembly.standoff` |
| BACKING_PLATE / FRONT_PLATE | 206 / 107 | none | custom | `assembly.axle_plate` |

The STEP shows only the left front-axle stack; the right one is its mirror. No battery, ESCs, receiver, switch, base
panel, fasteners or wires are in the STEP.

## Architecture

- **Chassis** (fixed datum): open-bottom printed block 59 x 66.6 x 17 with 2 mm walls and a 2 mm deck. A 1 mm base
  panel drops into the 1 mm x 2 mm rebate. Six screw columns (2 x 2 grid on 50 x 32, the Revron RV01 insert grid,
  plus two on the centre line) take M2 heat-sets at both ends.
- **Drive**: two N10 in the rear (weapon-end) keyholes, gearbox face on the wall inner face, RV21 hubs / F1 tyres.
  Front wheels are idlers: F1 tyres on RV21 hubs whose bore is opened to run on a 10 mm M3 standoff clamped across
  the front keyhole between BACKING_PLATE (inside) and FRONT_PLATE (outside).
- **Weapon module (vert_mod)**: a printed frame on the deck screwed into the four corner columns, a sloped hollow top
  shell and two uprights. The BE1806 base bolts to the left upright (4 x M2); its RV07 prop mount carries the
  spiderSL and the Drisk_floating_3 disc and runs in an MF85ZZ in the right upright: the disc is supported both sides.
- **Side pods (TPU)**: plate screwed sideways into the chassis side boss (2 x M3 into captive nuts), battered skin
  outside the rear wheel, a finger beside the outer chassis tab, and a fork prong running forward past the disc to the
  floor.
- **Cross bolt**: one M3 through side finger, chassis tabs, vert_mod prongs and the other finger, nut at the end. It
  ties the module, both pods and the chassis at the rear.

## Load paths

Disc hit -> spider -> prop mount -> bell / MF85 -> both uprights -> vert_mod frame -> 4 M2 into the columns and the
cross bolt through the tabs -> chassis. Fork / pod hit -> side boss screws (shear across the 2 M3) and the cross bolt.
Ground: the four F1 tyres; forks run 0.25 mm over the floor.

## What rotates

Disc, spider, prop mount and the BE1806 bell (spin axis X at y 59.2, z 23.5 STEP). Rear hubs/tyres with the N10
shafts; front hubs/tyres idle on the standoffs.

## Decisions on open items (ours, not in the STEP)

- **Top retention**: vert_mod is the top. It is located by its frame on the deck and the prongs between the tabs,
  clamped by 4 M2 into the top heat-sets of the corner columns and by the cross bolt.
- **Motor retention**: N10 boss in the keyhole; the base panel closes the slot from below. BE1806 by 4 x M2 through the
  left upright into its base.
- **Front axle**: idler on the standoff (the STEP has two N10 only).
- **Electronics** (STEP silent): battery left of centre and Malenki right of centre on the base panel between the
  column rows, weapon ESC on the Malenki, BBB switch hanging in the deck slot (the dump's 4 x 12 slot with 1.7 pilots
  on 15 mm matches the RV15 switch flange). Wires run inside the chassis; the weapon phase leads go up through the
  deck wire slot (Cut-Extrude17) under the shell.
- **Fasteners**: M2 (columns, motor, switch) and M3 (side pods, front axle, cross bolt): two thread sizes.

## Inherited placements

Hubs/tyres (Revron RV21/RV22 parts at the Alt axle lines), disc and spider (Revron parts on the Alt axis), the
weapon lock convention (external pin, Revron), the electronics catalog entries (Revron RV13/14/15/16).
