# COTS alternatives for Revron (antweight, 150 g)

Catalogue code: `robot/cots_alts.py` (one data table per part, each row with its `src`). Swap a part by setting
`"catalog": "<key>"` in a template. Downloads: `<category>/<model>/raw/` (vendor pages and images, untrusted data, kept as fetched);
vendor CAD: `<category>/<model>/cad_ref/` (reference only, never imported into the build).
Fetched 2026-10-22.

## Weapon brushless motors (kind `weapon_motor`)
| Key | Brand / model | Bell x length | Shaft | Mount | Mass | kV / current | Source |
|---|---|---|---|---|---|---|---|
| `gr1507` (existing) | GEPRC GR1507 | 19.6 | 5 (M5) | 4x M2 on 12 | 8.5+7 | 2850 | research/motor_cad/GR1507_datasheet.png |
| `repeat_2004_1400kv`, `repeat_2004_2800kv` | Repeat Robotics DirectDrive 2004 | 24.70 x 14.80 (30.25 overall) | 3 mm steel through-shaft | 3x M3 tap on 15 (base and bell) | ~18 g with wires | 1400 / 2800 kV, 2-4S | [BBB page](https://shop.bristolbotbuilders.com/product/2004/), drawing `weapon_motor/repeat_2004/raw/original.PNG`, STEP in cad_ref (bbox 24.70 x 30.75 x 24.70) |
| `bbb_be1806_2300kv` | BBB BE1806 2300 kV | 23 x 18.5 (21.5 overall) | 2 mm | base 2x M2 on 12 + 2x M2 on 16; top 4x M2 on 9 | ~23 g incl. 150 mm wires | 2300 kV, 2-4S | [BBB page](https://shop.bristolbotbuilders.com/product/brushlessmotor/), drawing `raw/be3.jpg`, STEP in cad_ref (23.10 x 22.15 x 23.10) |
| `brotherhobby_tc1404_3800kv`, `_4600kv` | BrotherHobby TC 1404 | 18.2 x 16 overall | 1.5 mm (4 mm stick-out) | 4x M2 on 9 (base), 4x M2 on 5 (bell) | 8.6 / 8.7 g (100 mm 30 AWG) | 3800 kV 8.1 A 322 mOhm / 4600 kV 13.6 A 207 mOhm, 4S | [BrotherHobby store](https://www.brotherhobbystore.com/products/tc-1404-ultralight-motor-139), drawing `raw/01bab18143.jpg`, table `raw/85357ed61f.jpg` |
| `emax_eco2207_1900kv` | EMAX ECO 2207 1900 kV | 27.45 x 32.6 | M5 prop shaft | 16x16 (M3 assumed) | 31.5 g w/o wire | 1900 kV, 3-6S | [EMAX model shop](https://shop.emaxmodel.com/products/emax-eco-series-2207-3-6s-1700kv-1900kv-2400kv-brushless-motor-for-rc-drone-fpv-racing), [EMAX USA (16x16)](https://shop.emax-usa.com/products/eco-ii-2207-brushless-motor-1700kv-1900kv-2400kv) - no drawing published |

Not added: **T-Motor F1507** (store.tmotor.com product page 404, t-hobby.com 403; search snippets only: dia 18.9 x 29.7, 2 mm shaft, 15.2 g, no mount pattern). RCX / iFlight not attempted.

## Drive gearmotors (kind `motor`, 12 x 10 N10/N20 format)
Format drawing: [Pololu micro-metal-gearmotors-dimensions.pdf](https://www.pololu.com/file/0J949/micro-metal-gearmotors-dimensions.pdf) - gearbox 12.0 x 10.0 x 9 (L), motor 15, 2x M1.6 at 4.5 each side of the shaft, bushing dia 4 x 0.7, dia 3 D-shaft 2.5 across the flat, 10 long.

| Key | Model | Size | Speed / current | Mass | Source |
|---|---|---|---|---|---|
| `pololu_hpcb6v_30to1` | Pololu 30:1 HPCB 6V (#3072) | 9 + 15 + 10 shaft | 1100 rpm, 0.15 A, 1.5 A stall, 0.45 kg.cm | not stated (9.5 g estimate) | [pololu.com/product/3072](https://www.pololu.com/product/3072) |
| `pololu_hpcb6v_50to1` | Pololu 50:1 HPCB 6V (#3073) | same | 650 rpm, 1.5 A stall, 0.74 kg.cm | not stated | [rev 6.2 datasheet](https://www.pololu.com/file/0J1487/pololu-micro-metal-gearmotors-rev-6-2.pdf) |
| `pololu_hpcb6v_75to1` | Pololu 75:1 HPCB 6V (#3074) | same | 430 rpm, 0.15 A, 1.5 A stall, 1.1 kg.cm | not stated | [pololu.com/product/3074](https://www.pololu.com/product/3074) |
| `bbb_n20_600rpm` | BBB N20 600 rpm (50:1) | 36 x 12 x 10, 9 x 3 shaft | ~0.1 A no load at 7.8 V | 9.7 g | [BBB n20](https://shop.bristolbotbuilders.com/product/n20/), STEP 12.00 x 36.20 x 10.00 |
| `bbb_hpn20_1000rpm` | BBB High Power N20 | 35 x 12 x 10 | ~0.2 A no load, ~2.2 A stall at 2S | ~9.5 g | [BBB hpn20](https://shop.bristolbotbuilders.com/product/hpn20/) |
| `bbb_n10_600rpm`, `bbb_n10_1000rpm` | BBBxN&B N10 | 33 x 12 x 10 | ~0.1 A no load, ~1 A stall at 7.8 V | ~8 g | [BBB n10](https://shop.bristolbotbuilders.com/product/n10/), STEP 12.00 x 10.00 x 32.50 |

## LiPo packs (kind `battery`)
| Key | Pack | L x W x H | Mass | Plug | Source |
|---|---|---|---|---|---|
| `palmpower_2s_180_45c` | Palm Power Gen2 2S 180 mAh 45C | 36.25 x 19.75 x 9.9 | 13.3 g | JST | [palmbeachbots](https://palmbeachbots.com/products/palm-power-2s-180mah-45c-lipo-battery) |
| `palmpower_2s_300_65c` | Palm Power Gen2 2S 300 mAh 65C | 46.25 x 16.25 x 13.2 | 20.2 g | JST | [palmbeachbots](https://palmbeachbots.com/products/palm-power-2s-300mah-65c-lipo-battery) |
| `tattu_2s_300_75c_hv` | Tattu 2S1P 300 mAh 75C 7.6 V | 45 x 16 x 12 | 16 g | JST-PHR | [racedayquads](https://racedayquads.com/products/tattu-300mah-7-6v-75c-2s1p-lipo-jst) |
| `betafpv_2s_300_45c` | BETAFPV 2S 300 mAh 45C | 45 x 17 x 12 | 18.4 g | XT30, 18 AWG | [betafpv.com](https://betafpv.com/products/300mah-2s-lipo-battery-2pcs) |
| `gnb_2s_350_70c_hv` | GNB 2S 350 mAh 70C HV | 48 x 18 x 12 | 17 g | XT30 | [kiwiquads](https://www.kiwiquads.co.nz/product/gnb-lipo-battery-7-6v-70c-350mah-2s-hv/) |
| `gnb_2s_450_80c` | GNB 2S 450 mAh 80C | 61 x 17 x 14 | 28 g | XT30 | [racedayquads](https://racedayquads.com/products/gaoneng-7-4v-2s-450mah-80c-lipo-whoop-micro-battery-w-xt30) |
| `gnb_3s_300_80c_hv` | GNB 3S 300 mAh 80C HV (GNB3003S80AHV) | 53 x 17 x 18 | 28 g | XT30 | [fpv24](https://www.fpv24.com/en/gaoneng/gaoneng-gnb-lipo-akku-lihv-300mah-3s-114v-80c-xt30) |

## ESCs (kind `esc`)
| Key | Model | Size | Mass | Rating | Source |
|---|---|---|---|---|---|
| `bbb_malenki_nano` | BBB Malenki-Nano (Rx + 3 brushed) | 32 x 19 x 2.5 | 2.3 g | 1-2S, 3x 1 A cont / 1.8 A peak | [BBB malenki](https://shop.bristolbotbuilders.com/product/malenki/), CAD zip in cad_ref |
| `bbb_dual_esc_v31` | BBB Antweight Dual ESC v3.1 | 23 x 19 x 6 | ~7 g | 2-4S, 2x 2 A cont / 4 A peak, 5 V 1 A BEC | [BBB bbbv3](https://shop.bristolbotbuilders.com/product/bbbv3/) |
| `bbb_brushless_esc_20a` | BBB Spinner Brushless ESC | 23 x 12 x 4 (PCB) | ~5 g with wires | 2-4S, 20 A cont, 25 A 10 s, no BEC | [BBB brushless](https://shop.bristolbotbuilders.com/product/brushless/), STEP 13.0 x 46.7 x 5.5 incl. leads |
| `bbb_red_esc` | BBB N10/N20 Red ESC | 20 x 11.6 x 4 | 0.4 g (1.4 g with lead) | 1-2S, 1 A cont / 1.8 A | [BBB redesc](https://shop.bristolbotbuilders.com/product/redesc/) |

Not added: DasMikro, Repeat AM32 ESCs (not researched in this pass).

## Connectors and switches (kinds `connector`, `switch`)
| Key | Part | Size | Rating | Source |
|---|---|---|---|---|
| `xt30u_m` / `xt30u_f` | Amass XT30U male / female | 5.20 x 10.20 x 13.70 / 12.40, pins on 5.00 | 15 A, 30 A peak, 0.70 mOhm, 18 AWG | [Amass XT datasheet via LCSC](https://www.lcsc.com/datasheet/C99101.pdf) p7, `connector/amass_xt30/raw/` |
| `betafpv_bt20_m` | BETAFPV BT2.0 male | 6.0 x 4.2 x 10.5 (F 8.3) | 9 A, 15 A burst; 0.34 g | [fpvfaster](https://www.fpvfaster.com.au/products/betafpv-bt2-0-connectors-male-female-5-pairs) |
| `jst_phr2` | JST PHR-2 | 5.8 x 4.5 (height estimated) | 2 A, AWG 32-24 | [Arrow](https://www.arrow.com/en/products/phr-2/jst-manufacturing.html); JST ePH.pdf in raw (fonts unrenderable here) |
| `fingertech_mini_switch` | FingerTech Mini Power Switch | 12.7 x 12.7 x 6.35, terminals 3.5 x 1 x 6.35, holes 7.62 apart | 40 A, 100 A 10 s; 2.15 g | [fingertechrobotics](https://www.fingertechrobotics.com/proddetail.php?prod=ft-mini-switch), IGS in cad_ref |

## Wheels and tyres (kinds `wheel`, `tyre`) - parametric
`cots_alts.wheel(od, width, tyre_t, bore, d_flat, hub_boss_d, boss_len, web_t, spokes, spoke_w, tread, tread_n, tread_depth, tread_w)`
and `cots_alts.tyre(...)`; tread = smooth / grooves / blocks.

| Key | Wheel | OD x width | Mass | Source |
|---|---|---|---|---|
| `bbb_wheel_34x6_5` | BBB 34 mm (rubber tread, plastic hub, 3 mm D) | 34 x 6.5 (+2 boss) | ~4.1 g | [BBB wheels](https://shop.bristolbotbuilders.com/product/wheels/), STEP: rim r13.75, boss r3.5, 8.6 wide |
| `bbb_wheel_22x10` | BBB 22 mm (10 mm tyre, PLA+ hub) | 22 x 10.7 | ~3.5 g | [BBB 22mm](https://shop.bristolbotbuilders.com/product/22mmwheels/), STEP: rim r9.25, boss r6.25 |
| `durahubs_25`, `durahubs_30`, `durahubs_35` | DuraHubs (silicone tread, PLA-ST hub) | 25 / 30 x 6 (+2), 35(36) x 14 | 3 / 4 / 11 g | [BBB durahubs](https://shop.bristolbotbuilders.com/product/durahubs/), 35 mm STEP: 54 tread blocks r17/r18, hub r10.4 |
