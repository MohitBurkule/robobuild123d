# Revron relations

Masters live at the top of `src/revron/params.py`. Everything else is derived from them or is a catalog / measured
(`# param: organic`) value. Part files must use the derived name, never retype its number (lint: `param.unlinked`).

| Master | Value | Meaning |
|---|---|---|
| `CH_HALF_W` | 29.5 | chassis outer half-width (outer side-wall face) |
| `CH_Y0`, `CH_Y1` | -37.6, 15.0 | chassis rear / front face |
| `CH_Z0`, `CH_Z1` | 2.5, 19.5 | floor underside / rim |
| `CH_WALL` | 2.0 | printed wall and deck thickness |
| `WY`, `WZ` | 38.5, 23.5 | weapon axis |
| `RY`, `RZ` | -30.5, 11.0 | rear axle (N10 shaft) |
| `SA`, `SB` | (30.5, 5.5), (40.5, 4.5) | front-axle / nose standoff axes (Y, Z) |
| `SA_X0`, `SB_X0`; `SA_LEN`, `SB_LEN` | 17.5, 21.5; 25, 15 | standoff inner ends; catalog lengths |
| `SO_R` | 2.5 | standoff radius |
| `M3_THIN_NUT_T` | 1.8 | DIN 439 thin nut |
| `MNT_IN`, `MNT_T`, `MNT_SLAB_T` | 13.4, 8, 4 | weapon mount inner face, thickness, slab |
| `FLOOR_Z` | 1.0 | ground plane of ramps / feet |

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
STACK_X0 + SPIDER_T/DISC_T/SPACER_T ── DR_X (each plate flush on the previous)
```
