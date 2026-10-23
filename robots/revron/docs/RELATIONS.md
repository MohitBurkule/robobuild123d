# Revron relations

Masters live at the top of `src/revron/params_chassis.py` (`params.py` re-exports the themed modules chassis -> weapon -> side -> hardware -> spec -> drive). Everything else is derived from them or is a catalog / measured
(`# param: organic`) value. Part files must use the derived name, never retype its number (lint: `param.unlinked`, which also scans module-level constants and tables of part files outside `# param: organic` blocks).

| Master | Value | Meaning |
|---|---|---|
| `CH_HALF_W_STOCK` -> `CH_HALF_W` | 29.5 | chassis outer half-width (outer side-wall face) as drawn -> in use (`size.width`) |
| `CH_Y0`, `CH_Y1_STOCK` -> `CH_Y1` | -37.6, 15.0 | chassis rear / stock front face -> front face in use (`size.length`, the pack can push it forward) |
| `CH_Z0`, `CH_Z1_STOCK` -> `CH_Z1` | 2.5, 19.5 | floor underside / stock rim -> rim in use (`size.height`) |
| `CH_WALL` | 2.0 | printed wall and deck thickness |
| `WY_STOCK`, `WZ_STOCK` -> `WY`, `WZ` | 38.5, 23.5 | weapon axis as drawn -> in use (moves with the nose / the rim) |
| `RY`, `RZ` | -30.5, 11.0 | rear axle (N10 shaft) |
| `SA_Y0` -> `SA`, `SB` | (30.5, 5.5), (40.5, 4.5) | front-axle / nose standoff axes (Y, Z); Y moves with the nose |
| `SA_X0`, `SB_X0`; `SA_LEN`, `SB_LEN` | 17.5, 21.5; 25, 15 | standoff inner ends; catalog lengths |
| `SO_R` | 2.5 | standoff radius |
| `M3_THIN_NUT_T` | 1.8 | DIN 439 thin nut |
| `MNT_IN`, `MNT_T`, `MNT_SLAB_T` | 13.4, 8, 4 | weapon mount inner face, thickness, slab |
| `FLOOR_Z` | 1.0 | ground plane of ramps / feet |

## Overall size (hooks `size.width`, `size.length`, `size.height`)

`REVRON_SIZE_WIDTH` / `_LENGTH` / `_HEIGHT` = a delta in mm (`4`, `-3.5`) or a percentage of the stock overall width / length / height (`10%`). Width moves both side walls; length moves the nose
(rear wall, rear axle, drive motors, stop wall stay; front wall, `SA` / `SB`, `WY`, the front column row and the top-panel tab move); height moves the rim (deck, top panel, `WZ`).
A shrink saturates where the contents touch: `CH_HALF_W_MIN` (two gearmotors `MOTOR_PAIR_GAP` apart at the centre), `CH_Y1_MIN` (pack against the stop wall plus a wall),
`CH_Z1_MIN` (gearbox top `MOTOR_DECK_GAP` under the deck). A larger part can raise a floor above the stock size but never lowers the stock.

## Relation tree

```
CH_HALF_W ─┬─ CH.x
           ├─ CH_IN_X = CH_HALF_W - CH_WALL ── SWX = CH_IN_X - SW_CLR - SW_HALF_W
           └─ NUT_X = (CH_HALF_W - M3_THIN_NUT_T, CH_HALF_W)      nut pocket opens on the outer face
CH_Z1 ─┬─ CH.z1, TOP_Z0 (top panel on the rim), MNT_TOP_Z (mount notch top)
       └─ CH.deck = COLUMN_TOP_Z = CH_Z1 - CH_WALL
CH_Y1 ── TAB.y0                                                  mount tab starts at the chassis front
CH_WALL ── CH.wall, CH.cham
SA_X0 + SA_LEN ── SA_X;  SB_X0 + SB_LEN ── SB_X
MNT_IN + MNT_T ── MNT_OUT;  MNT_IN + MNT_SLAB_T ── MNT_SLAB;  MNT_IN - BSP_T ── BSP_X
RX_C ± RX_SIZE/2 ── RX_X/Y/Z;  WE_C ± WE_SIZE/2 ── WE_X/Y/Z     electronics pockets = catalog box at placement
FLOOR_Z ── SP_FOOT_Z, SP_NOSE_Z, SP_BATTER.z, ramp face Z
GR1507 catalog BELL_TOP_X ── BELL_CAP_X ── STACK_X0 = BELL_CAP_X - SPIDER_T   spider inner face on the bell cap
STACK_X0 + SPIDER_T/DISC_T/SPACER_T ── DR_X (each plate flush on the previous)
GR1507 BELL_SCREW_R / BELL_SCREW_PHASE ── HUB_R / DR_ROT          spider clocked to the bell screws
WSHAFT.r ── SHAFT_D, BRG.bore_r, SPIDER.bore_r (+ SHAFT_CLR);  BELL_WALL_R + SHAFT_CLR ── SPACER.bore_r
MNT_IN + BRG_RECESS + BRG.w/2 ── BRG.x;  BRG.od_r - BRG_PRESS ── BRG_SEAT_R;  MNT_SLAB + SHAFT_INTO_RECESS ── WSHAFT.x_end
MNT_FRAME = (±MNT_IN, WY, WZ): mount frames; joint chain in src/revron/assembly_rig.py (_weapon):
  tub tab -> mount notch; RV03 inner face -> back spacer; RV03 stator seat -> stator -> bell (rotor fit)
  -> spider (bell cap) -> disc_a -> dspacer -> disc_b; bell bore -> wshaft; RV02 seat -> MR85
```
