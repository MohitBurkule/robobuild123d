# Change hypotheses: Revron @ acdcd78

Generator `robot/gen/changes.py` (swap / dimension / architecture), settings layer `robot/overlay.py` + the robot's `hooks.json`, run through the robust runner (`robot/checks/robust/hyp.py`): each change rebuilt on the per-part cache and checked with integrity, interference, connections, assembly, fastener_seat, electrical, retention. A change **holds** when it is expressible through settings, builds, and adds no blocker the baseline lacks.

## Versatility score: **23 %** of decided hypotheses hold with zero code change (23 / 101; 23 % of all 102 generated)

| family | hold / decided |
|---|---|
| swap | 13 / 72 |
| dimension | 7 / 15 |
| architecture | 3 / 14 |

Verdicts: breaks 71, holds 23, not expressible 7, timeout 1
Run: 7000 s (budget 7000.0 s, 3 workers); baseline 795.9 s with 12 blockers (excluded from the diff).

## Top missing hooks / fixes per owner

**A (tub)**
- swap fit: assembly.blocked, interference.overlap, interference.sweep: 12 hypothesis(es), e.g. `swap:wheel:wheel_fl+wheel_fr->bbb_wheel_34x6_5`
- swap fit: interference.overlap, interference.sweep: 10 hypothesis(es), e.g. `swap:drive_motor:motor_l+motor_r->bbb_hpn20_1000rpm`
- swap fit: assembly.blocked, interference.overlap, interference.spin: 5 hypothesis(es), e.g. `swap:battery:battery->betafpv_2s_300_45c`
- swap fit: assembly.blocked, interference.overlap: 5 hypothesis(es), e.g. `swap:battery:battery->palmpower_2s_180_45c`
- hook `weapon.type`: 3 hypothesis(es), e.g. `arch:weapon.type=hspin_bar`
- swap fit: assembly.blocked, electrical.battery_weapon_gap, interference.overlap: 2 hypothesis(es), e.g. `swap:battery:battery->c_typical_2s_300mah_lipo_lihv_betafpv_tbs_`

**B (weapon)**
- swap fit: assembly.blocked, interference.overlap, interference.sweep: 21 hypothesis(es), e.g. `swap:weapon_motor:weapon_motor_stator->bbb_be1806_2300kv`
- swap fit: assembly.blocked, interference.overlap, interference.spin: 5 hypothesis(es), e.g. `swap:battery:battery->betafpv_2s_300_45c`
- hook `weapon.type`: 3 hypothesis(es), e.g. `arch:weapon.type=hspin_bar`
- swap fit: assembly.blocked, electrical.battery_weapon_gap, interference.overlap: 2 hypothesis(es), e.g. `swap:battery:battery->c_typical_2s_300mah_lipo_lihv_betafpv_tbs_`
- swap fit: assembly.blocked, checks.crashed, interference.overlap: 2 hypothesis(es), e.g. `swap:weapon_motor:weapon_motor_stator->c_bbb_be1806_2300kv`
- dimension fit: assembly.blocked, interference.overlap: 2 hypothesis(es), e.g. `dim:MNT_IN+10%`

**C (side/fork/wedgelet/hubs)**
- swap fit: assembly.blocked, interference.overlap, interference.sweep: 16 hypothesis(es), e.g. `swap:wheel:wheel_fl+wheel_fr->bbb_wheel_22x10`
- swap fit: interference.overlap, interference.sweep: 10 hypothesis(es), e.g. `swap:drive_motor:motor_l+motor_r->bbb_hpn20_1000rpm`
- swap fit: assembly.blocked, interference.overlap, interference.spin: 4 hypothesis(es), e.g. `swap:battery:battery->betafpv_2s_300_45c`
- dimension fit: assembly.blocked, interference.overlap: 2 hypothesis(es), e.g. `dim:MNT_IN+10%`
- hook `drive.location`: 2 hypothesis(es), e.g. `arch:drive.location=front_driven`
- swap fit: assembly.blocked, electrical.battery_weapon_gap, interference.overlap: 1 hypothesis(es), e.g. `swap:battery:battery->gnb_2s_450_80c`

**spec/framework**
- swap fit: assembly.blocked, interference.overlap, interference.sweep: 24 hypothesis(es), e.g. `swap:weapon_motor:weapon_motor_stator->bbb_be1806_2300kv`
- swap fit: interference.overlap, interference.sweep: 10 hypothesis(es), e.g. `swap:drive_motor:motor_l+motor_r->bbb_hpn20_1000rpm`
- swap fit: assembly.blocked, interference.overlap, interference.spin: 5 hypothesis(es), e.g. `swap:battery:battery->betafpv_2s_300_45c`
- swap fit: assembly.blocked, interference.overlap: 5 hypothesis(es), e.g. `swap:battery:battery->palmpower_2s_180_45c`
- swap fit: assembly.blocked, electrical.battery_weapon_gap, interference.overlap: 2 hypothesis(es), e.g. `swap:battery:battery->c_typical_2s_300mah_lipo_lihv_betafpv_tbs_`
- swap fit: interference.overlap: 2 hypothesis(es), e.g. `swap:drive_motor:motor_l+motor_r->n10_2200rpm_6v`

## Swap hypotheses

| hypothesis | verdict | builds | new blockers | diff needed |
|---|---|---|---|---|
| battery lipo_2s_180_turnabot -> betafpv_2s_300_45c (BETAFPV 2S 300 mAh 45C (XT30)) | breaks | yes | assembly.blocked x20, interference.overlap x4, interference.spin x1 | 8 file(s): drisk.py, fork.py, hubs.py, mount.py, side_joint.py +3 more |
| battery lipo_2s_180_turnabot -> c_palm_power_2s_300mah_65c_us_ref_not_uk (Palm Power 2S 300mAh 65C (US ref, not UK)) | breaks | yes | assembly.blocked x13, interference.overlap x3, interference.spin x1 | 4 file(s): drisk.py, mount.py, tub.py, spec.py |
| battery lipo_2s_180_turnabot -> c_typical_2s_300mah_lipo_lihv_betafpv_tbs_ (Typical 2S 300mAh LiPo/LiHV (BetaFPV/TBS/RDQ class)) | breaks | yes | assembly.blocked x13, interference.overlap x3, electrical.battery_weapon_gap x1 | 4 file(s): drisk.py, mount.py, tub.py, spec.py |
| battery lipo_2s_180_turnabot -> gnb_2s_350_70c_hv (GNB (Gaoneng) 2S 350 mAh 70C HV 7.6 V (XT30)) | breaks | yes | assembly.blocked x20, interference.overlap x4, interference.spin x1 | 8 file(s): drisk.py, fork.py, hubs.py, mount.py, side_joint.py +3 more |
| battery lipo_2s_180_turnabot -> gnb_2s_450_80c (GNB (Gaoneng) 2S 450 mAh 80C (XT30)) | breaks | yes | assembly.blocked x20, interference.sweep x7, interference.overlap x6 | 8 file(s): drisk.py, fork.py, hubs.py, mount.py, side_joint.py +3 more |
| battery lipo_2s_180_turnabot -> gnb_3s_300_80c_hv (GNB (Gaoneng) 3S 300 mAh 80C HV 11.4 V (XT30, GNB3003S80AHV)) | breaks | yes | assembly.blocked x35, interference.overlap x6, electrical.battery_weapon_gap x1 | 10 file(s): drisk.py, fork.py, hubs.py, mount.py, panel_base.py +5 more |
| battery lipo_2s_180_turnabot -> lipo_1s_300 (1S 300 mAh LiPo) | breaks | yes | electrical.cells_consistent x1 | 0 code lines (1 setting(s)) |
| battery lipo_2s_180_turnabot -> lipo_2s_180 (2S 180 mAh LiPo (nano-tech class)) | holds | yes | - | 0 code lines (1 setting(s)) |
| battery lipo_2s_180_turnabot -> lipo_2s_350 (2S 350 mAh LiPo) | holds | yes | - | 0 code lines (1 setting(s)) |
| battery lipo_2s_180_turnabot -> palmpower_2s_180_45c (Palm Power Gen2 2S 180 mAh 45C (JST)) | breaks | yes | assembly.blocked x20, interference.overlap x2 | 8 file(s): drisk.py, fork.py, hubs.py, mount.py, side_joint.py +3 more |
| battery lipo_2s_180_turnabot -> palmpower_2s_300_65c (Palm Power Gen2 2S 300 mAh 65C (JST)) | breaks | yes | assembly.blocked x20, interference.overlap x4, interference.spin x1 | 8 file(s): drisk.py, fork.py, hubs.py, mount.py, side_joint.py +3 more |
| battery lipo_2s_180_turnabot -> tattu_2s_300_75c_hv (Tattu 2S1P 300 mAh 75C HV 7.6 V (JST-PHR)) | breaks | yes | assembly.blocked x20, interference.overlap x4, interference.spin x1 | 8 file(s): drisk.py, fork.py, hubs.py, mount.py, side_joint.py +3 more |
| battery connector jst_rcy -> jst_ph | holds | yes | - | 0 code lines (1 setting(s)) |
| battery connector jst_rcy -> mr30 | holds | yes | - | 0 code lines (1 setting(s)) |
| battery connector jst_rcy -> xt30 | holds | yes | - | 0 code lines (1 setting(s)) |
| battery connector jst_rcy -> xt60 | holds | yes | - | 0 code lines (1 setting(s)) |
| drive esc malenki_nano_rvrn2 -> bbb_dual_esc_v31 (BBB Antweight Dual ESC v3.1 (2x 2 A brushed, 5 V 1 A BEC)) | breaks | yes | assembly.blocked x2, interference.overlap x2 | 2 file(s): tub.py, spec.py |
| drive esc malenki_nano_rvrn2 -> bbb_malenki_nano (BBB Malenki-Nano (receiver + 3x 1 A brushed ESC + 2 PWM out)) | holds | yes | - | 0 code lines (1 setting(s)) |
| drive esc malenki_nano_rvrn2 -> c_antweight_n10_n20_red_esc_motor_mounted (Antweight N10/N20 Red ESC (motor-mounted)) | holds | yes | - | 0 code lines (1 setting(s)) |
| drive esc malenki_nano_rvrn2 -> c_bbb_antweight_dual_esc_v3_1 (BBB Antweight Dual ESC v3.1) | breaks | yes | assembly.blocked x2, interference.overlap x2 | 2 file(s): tub.py, spec.py |
| drive esc malenki_nano_rvrn2 -> c_malenki_nano_antweight_esc_receiver (Malenki-Nano Antweight ESC & Receiver) | holds | yes | - | 0 code lines (1 setting(s)) |
| drive esc malenki_nano_rvrn2 -> esc_dual_brushed (Dual brushed ESC (hobby, heat-shrunk)) | breaks | yes | assembly.blocked x2, interference.overlap x2 | 2 file(s): tub.py, spec.py |
| drive esc malenki_nano_rvrn2 -> malenki_nano (Malenki Nano (Rx + 2 brushed drive ESC), kapton wrapped) | breaks | yes | assembly.blocked x2, interference.overlap x2 | 2 file(s): tub.py, spec.py |
| drive motor n10_2200rpm_spicy -> bbb_hpn20_1000rpm (BBB High Power N20 1000 rpm gearmotor (35 x 12 x 10, ~2.2 A stall at 2S)) | breaks | yes | interference.overlap x6, interference.sweep x2 | 3 file(s): hubs.py, tub.py, spec.py |
| drive motor n10_2200rpm_spicy -> bbb_n10_1000rpm (BBBxN&B N10 1000 rpm gearmotor (33 x 12 x 10, steel plates)) | breaks | yes | interference.overlap x4, interference.sweep x2 | 3 file(s): hubs.py, tub.py, spec.py |
| drive motor n10_2200rpm_spicy -> bbb_n10_600rpm (BBBxN&B N10 600 rpm gearmotor (33 x 12 x 10, steel plates)) | breaks | yes | interference.overlap x4, interference.sweep x2 | 3 file(s): hubs.py, tub.py, spec.py |
| drive motor n10_2200rpm_spicy -> bbb_n20_600rpm (BBB pair-of-N20 600 rpm gearmotor (50:1, 36 x 12 x 10)) | breaks | yes | interference.overlap x6, interference.sweep x2, checks.crashed x1 | 3 file(s): hubs.py, tub.py, spec.py |
| drive motor n10_2200rpm_spicy -> c_bbb_high_power_n20_gearmotor (BBB High Power N20 Gearmotor) | breaks | yes | interference.overlap x8, interference.sweep x4 | 3 file(s): hubs.py, tub.py, spec.py |
| drive motor n10_2200rpm_spicy -> c_bbbxn_b_antweight_n10_gearmotors (BBBxN&B Antweight N10 Gearmotors) | breaks | yes | interference.overlap x8, interference.sweep x4 | 3 file(s): hubs.py, tub.py, spec.py |
| drive motor n10_2200rpm_spicy -> c_pair_of_600rpm_antweight_n20_gearmotors (Pair of 600rpm Antweight N20 Gearmotors) | breaks | yes | interference.overlap x8, interference.sweep x4 | 3 file(s): hubs.py, tub.py, spec.py |
| drive motor n10_2200rpm_spicy -> n10_2200rpm_6v (N10 micro gearmotor 6 V 2200 rpm) | breaks | yes | interference.overlap x2 | 2 file(s): tub.py, spec.py |
| drive motor n10_2200rpm_spicy -> n10_300rpm_6v (N10 micro gearmotor 6 V 300 rpm) | breaks | yes | interference.overlap x2 | 2 file(s): tub.py, spec.py |
| drive motor n10_2200rpm_spicy -> n20_1000rpm_6v (N20 gearmotor 6 V 1000 rpm) | breaks | yes | interference.overlap x6, interference.sweep x2 | 3 file(s): hubs.py, tub.py, spec.py |
| drive motor n10_2200rpm_spicy -> pololu_hpcb6v_30to1 (Pololu 30:1 Micro Metal Gearmotor HPCB 6V (#3062/#3072)) | breaks | yes | interference.overlap x6, interference.sweep x2 | 3 file(s): hubs.py, tub.py, spec.py |
| drive motor n10_2200rpm_spicy -> pololu_hpcb6v_50to1 (Pololu 50:1 Micro Metal Gearmotor HPCB 6V (#3063/#3073)) | breaks | yes | interference.overlap x6, interference.sweep x2 | 3 file(s): hubs.py, tub.py, spec.py |
| drive motor n10_2200rpm_spicy -> pololu_hpcb6v_75to1 (Pololu 75:1 Micro Metal Gearmotor HPCB 6V (#3064/#3074)) | breaks | yes | interference.overlap x6, interference.sweep x2 | 3 file(s): hubs.py, tub.py, spec.py |
| switch switch_bbb_ant_rvrn2 -> fingertech_mini_switch (FingerTech Mini Power Switch (12.7 cube-ish, 2 holes on 7.62, 40 A)) | breaks | yes | assembly.blocked x19, interference.overlap x7, fastener_seat.head_bearing x2 | 8 file(s): drisk.py, fork.py, hubs.py, mount.py, side_joint.py +3 more |
| switch switch_bbb_ant_rvrn2 -> switch_slide_12x4 (Miniature slide switch 11.8 x 3.8) | breaks | yes | assembly.blocked x3, fastener_seat.head_bearing x2, interference.overlap x2 | 2 file(s): tub.py, spec.py |
| switch switch_bbb_ant_rvrn2 -> switch_slide_bbb_ant (BBB ant slide switch 11.8 x 3.8 with a front mounting ear (2 x M2 holes)) | breaks | yes | assembly.blocked x4, interference.overlap x4, fastener_seat.head_bearing x2 | 2 file(s): tub.py, spec.py |
| weapon esc bbb_ant_esc_rvrn2 -> bbb_ant_esc (BBB brushless ant ESC (heat-shrunk)) | holds | yes | - | 0 code lines (1 setting(s)) |
| weapon esc bbb_ant_esc_rvrn2 -> bbb_brushless_esc_20a (BBB Antweight Spinner Brushless ESC 20 A (no BEC)) | holds | yes | - | 0 code lines (1 setting(s)) |
| weapon esc bbb_ant_esc_rvrn2 -> bbb_red_esc (BBB N10/N20 Red ESC (single 1 A brushed, motor mounted)) | breaks | yes | electrical.esc_weapon_current x1 | 0 code lines (1 setting(s)) |
| weapon esc bbb_ant_esc_rvrn2 -> c_bbb_antweight_spinner_brushless_esc (BBB Antweight Spinner Brushless ESC) | holds | yes | - | 0 code lines (1 setting(s)) |
| weapon esc bbb_ant_esc_rvrn2 -> esc_brushless_12a (Brushless ESC 12 A with BEC) | holds | yes | - | 0 code lines (1 setting(s)) |
| weapon motor gr1507 -> bbb_be1806_2300kv (BBB BE1806 2300 kV outrunner (23 mm bell, 4x M2 base on 12/16 mm, 4x M2 top on 9 mm)) (one-piece motor: the split rotor part ['weapon_motor_can'] has no counterpart and is kept) | breaks | yes | assembly.blocked x12, interference.overlap x7, interference.sweep x7 | 2 file(s): drisk.py, spec.py |
| weapon motor gr1507 -> be1806_bbb (BBB BE1806 2300 kV outrunner (23 mm bell, 20.5 incl. base and shaft collar, 5 mm shaft bore)) (one-piece motor: the split rotor part ['weapon_motor_can'] has no counterpart and is kept) | breaks | yes | assembly.blocked x12, interference.overlap x6, interference.sweep x6 | 3 file(s): drisk.py, mount.py, spec.py |
| weapon motor gr1507 -> bl_1806_2300kv (1806 2300 kV outrunner) (one-piece motor: the split rotor part ['weapon_motor_can'] has no counterpart and is kept) | breaks | yes | assembly.blocked x12, interference.overlap x7, interference.sweep x7 | 2 file(s): drisk.py, spec.py |
| weapon motor gr1507 -> bl_2306_1400kv (2306 1400 kV outrunner) (one-piece motor: the split rotor part ['weapon_motor_can'] has no counterpart and is kept) | breaks | yes | assembly.blocked x15, interference.overlap x13, interference.sweep x13 | 2 file(s): drisk.py, spec.py |
| weapon motor gr1507 -> brotherhobby_tc1404_3800kv (BrotherHobby TC 1404 3800 kV outrunner (18.2 x 16, 4x M2 on 9 mm base, 4x M2 on 5 mm bell, 1.5 mm shaft)) (one-piece motor: the split rotor part ['weapon_motor_can'] has no counterpart and is kept) | breaks | yes | assembly.blocked x12, interference.overlap x6, interference.sweep x6 | 2 file(s): drisk.py, spec.py |
| weapon motor gr1507 -> brotherhobby_tc1404_4600kv (BrotherHobby TC 1404 4600 kV outrunner (18.2 x 16, 4x M2 on 9 mm base, 1.5 mm shaft)) (one-piece motor: the split rotor part ['weapon_motor_can'] has no counterpart and is kept) | breaks | yes | assembly.blocked x12, interference.overlap x6, interference.sweep x6 | 2 file(s): drisk.py, spec.py |
| weapon motor gr1507 -> c_bbb_be1806_2300kv (BBB BE1806 2300kv) (one-piece motor: the split rotor part ['weapon_motor_can'] has no counterpart and is kept) | breaks | yes | assembly.blocked x12, interference.overlap x7, interference.sweep x7 | 2 file(s): drisk.py, spec.py |
| weapon motor gr1507 -> c_repeat_2004_antweight_spinner_motor (Repeat 2004 Antweight Spinner Motor) (one-piece motor: the split rotor part ['weapon_motor_can'] has no counterpart and is kept) | breaks | yes | assembly.blocked x16, interference.overlap x14, interference.sweep x13 | 3 file(s): drisk.py, mount.py, spec.py |
| weapon motor gr1507 -> emax_eco2207_1900kv (EMAX ECO 2207 1900 kV outrunner (27.45 x 32.6, 4x M3 16x16, M5 prop shaft)) (one-piece motor: the split rotor part ['weapon_motor_can'] has no counterpart and is kept) | breaks | yes | assembly.blocked x15, interference.overlap x13, interference.sweep x13 | 2 file(s): drisk.py, spec.py |
| weapon motor gr1507 -> gr1507_step (GR1507 outrunner, STEP-simplified fixed half (base cross and pin only, as the STEP): 4-arm cross base with 4 M2 on 12 mm, 12-slot wound stator stack, 3 phase leads (bell is `gr1507_can`)) | breaks | yes | fastener_seat.thread_bite x4, interference.overlap x1 | 2 file(s): drisk.py, spec.py |
| weapon motor gr1507 -> repeat_2004_1400kv (Repeat Robotics DirectDrive 2004 1400 kV outrunner (3 mm through shaft, 3x M3 on 15 mm both ends)) (one-piece motor: the split rotor part ['weapon_motor_can'] has no counterpart and is kept) | breaks | yes | assembly.blocked x15, interference.overlap x13, interference.sweep x13 | 2 file(s): drisk.py, spec.py |
| weapon motor gr1507 -> repeat_2004_2800kv (Repeat Robotics DirectDrive 2004 2800 kV outrunner (3 mm through shaft, 3x M3 on 15 mm both ends)) (one-piece motor: the split rotor part ['weapon_motor_can'] has no counterpart and is kept) | breaks | yes | assembly.blocked x15, interference.overlap x13, interference.sweep x13 | 2 file(s): drisk.py, spec.py |
| wheel RV20 Scalextric micro SLX tyre 11 x 7 x 6 -> bbb_wheel_22x10 (BBB 22 mm antweight wheel (10 mm rubber tyre, PLA+ hub)) | breaks | yes | assembly.blocked x30, interference.overlap x14, interference.sweep x14 | 7 file(s): drisk.py, fork.py, hubs.py, mount.py, side_joint.py +2 more |
| wheel RV20 Scalextric micro SLX tyre 11 x 7 x 6 -> bbb_wheel_34x6_5 (BBB 34 mm antweight wheel (rubber tread, plastic hub, 3 mm D)) | breaks | yes | assembly.blocked x28, interference.overlap x14, interference.sweep x14 | 8 file(s): drisk.py, fork.py, hubs.py, mount.py, side_joint.py +3 more |
| wheel RV20 Scalextric micro SLX tyre 11 x 7 x 6 -> durahubs_25 (DuraHubs 25 mm (silicone tread, PLA-ST hub)) | breaks | yes | assembly.blocked x28, interference.overlap x12, interference.sweep x12 | 7 file(s): drisk.py, fork.py, hubs.py, mount.py, side_joint.py +2 more |
| wheel RV20 Scalextric micro SLX tyre 11 x 7 x 6 -> durahubs_30 (DuraHubs 30 mm (silicone tread, PLA-ST hub)) | breaks | yes | assembly.blocked x28, interference.overlap x12, interference.sweep x12 | 7 file(s): drisk.py, fork.py, hubs.py, mount.py, side_joint.py +2 more |
| wheel RV20 Scalextric micro SLX tyre 11 x 7 x 6 -> durahubs_35 (DuraHubs 35 mm wide (14 mm silicone tread)) | breaks | yes | assembly.blocked x44, interference.overlap x22, interference.sweep x22 | 9 file(s): drisk.py, fork.py, hubs.py, mount.py, panel_base.py +4 more |
| wheel RV20 Scalextric micro SLX tyre 11 x 7 x 6 -> wheel_20x8 (20 x 8 mm wheel (printed hub, silicone tyre)) | breaks | yes | assembly.blocked x28, interference.overlap x12, interference.sweep x12 | 7 file(s): drisk.py, fork.py, hubs.py, mount.py, side_joint.py +2 more |
| wheel RV20 Scalextric micro SLX tyre 11 x 7 x 6 -> wheel_28x10 (28 x 10 mm wheel (printed hub, silicone tyre)) | breaks | yes | assembly.blocked x30, interference.overlap x14, interference.sweep x14 | 8 file(s): drisk.py, fork.py, hubs.py, mount.py, side_joint.py +3 more |
| wheel RV20 Scalextric micro SLX tyre 11 x 7 x 6 -> wheel_30x8 (30 x 8 mm wheel (printed hub, silicone tyre)) | breaks | yes | assembly.blocked x30, interference.overlap x14, interference.sweep x14 | 8 file(s): drisk.py, fork.py, hubs.py, mount.py, side_joint.py +3 more |
| wheel RV22 Scalextric F1 front tyre 21.5 x 14 x 9.5 -> bbb_wheel_22x10 (BBB 22 mm antweight wheel (10 mm rubber tyre, PLA+ hub)) | breaks | yes | assembly.blocked x11, interference.overlap x10, interference.sweep x8 | 4 file(s): hubs.py, panel_base.py, tub.py, spec.py |
| wheel RV22 Scalextric F1 front tyre 21.5 x 14 x 9.5 -> bbb_wheel_34x6_5 (BBB 34 mm antweight wheel (rubber tread, plastic hub, 3 mm D)) | breaks | yes | assembly.blocked x35, interference.overlap x14, interference.sweep x12 | 8 file(s): drisk.py, fork.py, hubs.py, mount.py, side_joint.py +3 more |
| wheel RV22 Scalextric F1 front tyre 21.5 x 14 x 9.5 -> durahubs_25 (DuraHubs 25 mm (silicone tread, PLA-ST hub)) | breaks | yes | interference.overlap x8, interference.sweep x6, assembly.blocked x4 | 3 file(s): hubs.py, tub.py, spec.py |
| wheel RV22 Scalextric F1 front tyre 21.5 x 14 x 9.5 -> durahubs_30 (DuraHubs 30 mm (silicone tread, PLA-ST hub)) | breaks | yes | assembly.blocked x30, interference.overlap x10, interference.sweep x8 | 8 file(s): drisk.py, fork.py, hubs.py, mount.py, side_joint.py +3 more |
| wheel RV22 Scalextric F1 front tyre 21.5 x 14 x 9.5 -> durahubs_35 (DuraHubs 35 mm wide (14 mm silicone tread)) | breaks | yes | assembly.blocked x52, interference.overlap x26, interference.sweep x24 | 10 file(s): drisk.py, fork.py, hubs.py, mount.py, panel_base.py +5 more |
| wheel RV22 Scalextric F1 front tyre 21.5 x 14 x 9.5 -> wheel_20x8 (20 x 8 mm wheel (printed hub, silicone tyre)) | breaks | yes | interference.overlap x6, assembly.blocked x4, interference.sweep x4 | 3 file(s): hubs.py, tub.py, spec.py |
| wheel RV22 Scalextric F1 front tyre 21.5 x 14 x 9.5 -> wheel_28x10 (28 x 10 mm wheel (printed hub, silicone tyre)) | breaks | yes | assembly.blocked x38, interference.overlap x10, interference.sweep x8 | 9 file(s): drisk.py, fork.py, hubs.py, mount.py, panel_base.py +4 more |
| wheel RV22 Scalextric F1 front tyre 21.5 x 14 x 9.5 -> wheel_30x8 (30 x 8 mm wheel (printed hub, silicone tyre)) | breaks | yes | assembly.blocked x30, interference.overlap x8, interference.sweep x6 | 8 file(s): drisk.py, fork.py, hubs.py, mount.py, side_joint.py +3 more |

## Dimension hypotheses

| hypothesis | verdict | builds | new blockers | diff needed |
|---|---|---|---|---|
| MNT_IN 13.4 -> 14.74 (+10%) | breaks | yes | assembly.blocked x15, interference.overlap x3 | 5 file(s): drisk.py, hubs.py, mount.py, panel_top.py, spec.py |
| MNT_IN 13.4 -> 12.06 (-10%) | timeout | - | - | - |
| SA[0] 30.5 -> 33.55 (+10%) | breaks | yes | assembly.blocked x26, interference.overlap x12, interference.sweep x6 | 6 file(s): drisk.py, fork.py, hubs.py, mount.py, wedgelet.py +1 more |
| SA[0] 30.5 -> 27.45 (-10%) | breaks | yes | assembly.blocked x20, interference.overlap x4 | 6 file(s): drisk.py, hubs.py, mount.py, tub.py, wedgelet.py +1 more |
| SA[1] 5.5 -> 6.05 (+10%) | holds | yes | - | 0 code lines (1 setting(s)) |
| SA[1] 5.5 -> 4.95 (-10%) | holds | yes | - | 0 code lines (1 setting(s)) |
| SB[0] 40.5 -> 44.55 (+10%) | breaks | yes | assembly.blocked x10, interference.overlap x4, fastener_seat.head_clash x2 | 5 file(s): fork.py, hubs.py, side_joint.py, tub.py, wedgelet.py |
| SB[0] 40.5 -> 36.45 (-10%) | breaks | yes | validity.load x1 | 1 file(s): wedgelet.py |
| SB[1] 4.5 -> 4.95 (+10%) | breaks | yes | assembly.blocked x14 | 3 file(s): drisk.py, mount.py, spec.py |
| SB[1] 4.5 -> 4.05 (-10%) | holds | yes | - | 0 code lines (1 setting(s)) |
| TY_ARC_STEP 5 -> 6 (+10%) | holds | yes | - | 0 code lines (1 setting(s)) |
| TY_ARC_STEP 5 -> 4 (-10%) | holds | yes | - | 0 code lines (1 setting(s)) |
| WY 38.5 -> 42.35 (+10%) | holds | yes | - | 0 code lines (1 setting(s)) |
| WY 38.5 -> 34.65 (-10%) | breaks | yes | assembly.blocked x14, interference.spin x2, interference.sweep x2 | 4 file(s): drisk.py, mount.py, tub.py, spec.py |
| WZ 23.5 -> 25.85 (+10%) | holds | yes | - | 0 code lines (1 setting(s)) |
| WZ 23.5 -> 21.15 (-10%) | breaks | yes | assembly.blocked x16 | 3 file(s): drisk.py, mount.py, spec.py |

## Architecture hypotheses

| hypothesis | verdict | builds | new blockers | diff needed |
|---|---|---|---|---|
| add a servo (servo_cs07) at `rear_outside` | breaks | yes | connection.cover_fasteners x1, connection.floating x1 | 0 code lines (1 setting(s)) |
| add a servo (servo_cs07) at `top_deck_rear` | breaks | yes | connection.cover_fasteners x1, connection.floating x1 | 0 code lines (1 setting(s)) |
| add a servo (servo_cs07) at `tub_interior_rear` | breaks | yes | assembly.blocked x19, interference.overlap x8, connection.cover_fasteners x1 | 4 file(s): panel_base.py, panel_top.py, tub.py, spec.py |
| battery orientation: long_x (generic fallback (no robot hook needed)) | breaks | yes | assembly.blocked x24, interference.overlap x5 | 8 file(s): drisk.py, fork.py, hubs.py, mount.py, side_joint.py +3 more |
| internal compartments: none | not expressible | - | missing hook `chassis.compartments` | 1 file(s): tub.py ~2 |
| internal compartments: split_battery_bay | not expressible | - | missing hook `chassis.compartments` | 1 file(s): tub.py ~2 |
| driven wheels: 2WD | holds | yes | - | 0 code lines (1 setting(s)) |
| drive location: front_driven | not expressible | - | missing hook `drive.location` | 5 file(s): hubs.py ~20, mount.py ~6, panel_base.py ~1, tub.py ~1, spec.py |
| drive location: front_motors_rear_driven | not expressible | - | missing hook `drive.location` | 5 file(s): hubs.py ~20, mount.py ~6, panel_base.py ~1, tub.py ~1, spec.py |
| declared setting weapon.motor_variant = step | holds | yes | - | 0 code lines (1 setting(s)) |
| declared setting weapon.mount_variant = printable | holds | yes | - | 0 code lines (1 setting(s)) |
| weapon slot: hspin_bar | not expressible | - | missing hook `weapon.type` | 3 file(s): drisk.py ~44, tub.py ~6, mount.py ~5 |
| weapon slot: vspin_drum | not expressible | - | missing hook `weapon.type` | 3 file(s): drisk.py ~44, tub.py ~6, mount.py ~5 |
| weapon slot: vspin_eggbeater | not expressible | - | missing hook `weapon.type` | 3 file(s): drisk.py ~44, tub.py ~6, mount.py ~5 |

## Breaking hypotheses: blockers

- **swap:battery:battery->betafpv_2s_300_45c**
  - `assembly.blocked` on battery: `battery` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `tub`.
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p2: `bolt_p2` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - ... 22 more
- **swap:battery:battery->c_palm_power_2s_300mah_65c_us_ref_not_uk**
  - `assembly.blocked` on battery: `battery` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `tub`.
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p2: `bolt_p2` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - ... 14 more
- **swap:battery:battery->c_typical_2s_300mah_lipo_lihv_betafpv_tbs_**
  - `assembly.blocked` on battery: `battery` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `tub`.
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p2: `bolt_p2` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - ... 15 more
- **swap:battery:battery->gnb_2s_350_70c_hv**
  - `assembly.blocked` on battery: `battery` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `tub`.
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p2: `bolt_p2` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - ... 22 more
- **swap:battery:battery->gnb_2s_450_80c**
  - `assembly.blocked` on battery: `battery` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `tub`.
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p2: `bolt_p2` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - ... 31 more
- **swap:battery:battery->gnb_3s_300_80c_hv**
  - `assembly.blocked` on base_panel: `base_panel` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `battery`.
  - `assembly.blocked` on battery: `battery` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `tub`.
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - ... 41 more
- **swap:battery:battery->lipo_1s_300**
  - `electrical.cells_consistent` on -: Cell counts: battery 1S, electronics.cells 2S, spider.weapon.cells 2S.
- **swap:battery:battery->palmpower_2s_180_45c**
  - `assembly.blocked` on battery: `battery` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `tub`.
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p2: `bolt_p2` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - ... 18 more
- **swap:battery:battery->palmpower_2s_300_65c**
  - `assembly.blocked` on battery: `battery` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `tub`.
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p2: `bolt_p2` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - ... 22 more
- **swap:battery:battery->tattu_2s_300_75c_hv**
  - `assembly.blocked` on battery: `battery` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `tub`.
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p2: `bolt_p2` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - ... 22 more
- **swap:drive_esc:rxesc->bbb_dual_esc_v31**
  - `assembly.blocked` on rxesc: `rxesc` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `tub`.
  - `assembly.blocked` on wesc: `wesc` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `rxesc`.
  - `interference.overlap` on rxesc,tub: `tub` and `rxesc` overlap by 0.37 mm (about 114.4 mm3).
  - `interference.overlap` on rxesc,wesc: `rxesc` and `wesc` overlap by 0.37 mm (about 182.4 mm3).
- **swap:drive_esc:rxesc->c_bbb_antweight_dual_esc_v3_1**
  - `assembly.blocked` on rxesc: `rxesc` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `tub`.
  - `assembly.blocked` on wesc: `wesc` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `rxesc`.
  - `interference.overlap` on rxesc,tub: `tub` and `rxesc` overlap by 0.37 mm (about 120.6 mm3).
  - `interference.overlap` on rxesc,wesc: `rxesc` and `wesc` overlap by 0.37 mm (about 182.4 mm3).
- **swap:drive_esc:rxesc->esc_dual_brushed**
  - `assembly.blocked` on rxesc: `rxesc` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `tub`.
  - `assembly.blocked` on wesc: `wesc` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `rxesc`.
  - `interference.overlap` on rxesc,tub: `tub` and `rxesc` overlap by 0.13 mm (about 20.4 mm3).
  - `interference.overlap` on rxesc,wesc: `rxesc` and `wesc` overlap by 0.15 mm (about 45.0 mm3).
- **swap:drive_esc:rxesc->malenki_nano**
  - `assembly.blocked` on rxesc: `rxesc` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `tub`.
  - `assembly.blocked` on wesc: `wesc` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `rxesc`.
  - `interference.overlap` on rxesc,tub: `tub` and `rxesc` overlap by 0.14 mm (about 40.5 mm3).
  - `interference.overlap` on rxesc,wesc: `rxesc` and `wesc` overlap by 0.15 mm (about 68.4 mm3).
- **swap:drive_motor:motor_l+motor_r->bbb_hpn20_1000rpm**
  - `interference.overlap` on belt_l,motor_l: `motor_l` and `belt_l` overlap by 0.13 mm (about 0.2 mm3).
  - `interference.overlap` on belt_r,motor_r: `motor_r` and `belt_r` overlap by 0.13 mm (about 0.2 mm3).
  - `interference.overlap` on motor_l,tub: `tub` and `motor_l` overlap by 0.88 mm (about 294.6 mm3).
  - `interference.overlap` on motor_l,whub_rl: `motor_l` and `whub_rl` overlap by 0.88 mm (about 195.0 mm3).
  - ... 4 more
- **swap:drive_motor:motor_l+motor_r->bbb_n10_1000rpm**
  - `interference.overlap` on motor_l,tub: `tub` and `motor_l` overlap by 0.88 mm (about 301.7 mm3).
  - `interference.overlap` on motor_l,whub_rl: `motor_l` and `whub_rl` overlap by 0.58 mm (about 92.9 mm3).
  - `interference.overlap` on motor_r,tub: `tub` and `motor_r` overlap by 0.88 mm (about 301.7 mm3).
  - `interference.overlap` on motor_r,whub_rr: `motor_r` and `whub_rr` overlap by 0.49 mm (about 92.9 mm3).
  - ... 2 more
- **swap:drive_motor:motor_l+motor_r->bbb_n10_600rpm**
  - `interference.overlap` on motor_l,tub: `tub` and `motor_l` overlap by 0.88 mm (about 301.7 mm3).
  - `interference.overlap` on motor_l,whub_rl: `motor_l` and `whub_rl` overlap by 0.58 mm (about 92.9 mm3).
  - `interference.overlap` on motor_r,tub: `tub` and `motor_r` overlap by 0.88 mm (about 301.7 mm3).
  - `interference.overlap` on motor_r,whub_rr: `motor_r` and `whub_rr` overlap by 0.49 mm (about 92.9 mm3).
  - ... 2 more
- **swap:drive_motor:motor_l+motor_r->bbb_n20_600rpm**
  - `checks.crashed` on -: `electrical` raised TypeError: '>' not supported between instances of 'NoneType' and 'NoneType'. Its verdicts are unknown.
  - `interference.overlap` on belt_l,motor_l: `motor_l` and `belt_l` overlap by 0.13 mm (about 0.2 mm3).
  - `interference.overlap` on belt_r,motor_r: `motor_r` and `belt_r` overlap by 0.13 mm (about 0.2 mm3).
  - `interference.overlap` on motor_l,tub: `tub` and `motor_l` overlap by 0.88 mm (about 291.4 mm3).
  - ... 5 more
- **swap:drive_motor:motor_l+motor_r->c_bbb_high_power_n20_gearmotor**
  - `interference.overlap` on belt_l,motor_l: `motor_l` and `belt_l` overlap by 0.13 mm (about 0.2 mm3).
  - `interference.overlap` on belt_r,motor_r: `motor_r` and `belt_r` overlap by 0.13 mm (about 0.2 mm3).
  - `interference.overlap` on motor_l,tub: `tub` and `motor_l` overlap by 0.88 mm (about 416.7 mm3).
  - `interference.overlap` on motor_l,wheel_rl: `motor_l` and `wheel_rl` overlap by 0.67 mm (about 57.8 mm3).
  - ... 8 more
- **swap:drive_motor:motor_l+motor_r->c_bbbxn_b_antweight_n10_gearmotors**
  - `interference.overlap` on belt_l,motor_l: `motor_l` and `belt_l` overlap by 0.13 mm (about 0.2 mm3).
  - `interference.overlap` on belt_r,motor_r: `motor_r` and `belt_r` overlap by 0.13 mm (about 0.2 mm3).
  - `interference.overlap` on motor_l,tub: `tub` and `motor_l` overlap by 0.88 mm (about 385.1 mm3).
  - `interference.overlap` on motor_l,wheel_rl: `motor_l` and `wheel_rl` overlap by 0.67 mm (about 55.0 mm3).
  - ... 8 more
- **swap:drive_motor:motor_l+motor_r->c_pair_of_600rpm_antweight_n20_gearmotors**
  - `interference.overlap` on belt_l,motor_l: `motor_l` and `belt_l` overlap by 0.13 mm (about 0.2 mm3).
  - `interference.overlap` on belt_r,motor_r: `motor_r` and `belt_r` overlap by 0.13 mm (about 0.2 mm3).
  - `interference.overlap` on motor_l,tub: `tub` and `motor_l` overlap by 0.88 mm (about 441.3 mm3).
  - `interference.overlap` on motor_l,wheel_rl: `motor_l` and `wheel_rl` overlap by 0.67 mm (about 59.2 mm3).
  - ... 8 more
- **swap:drive_motor:motor_l+motor_r->n10_2200rpm_6v**
  - `interference.overlap` on motor_l,tub: `tub` and `motor_l` overlap by 0.99 mm (about 180.6 mm3).
  - `interference.overlap` on motor_r,tub: `tub` and `motor_r` overlap by 0.99 mm (about 180.6 mm3).
- **swap:drive_motor:motor_l+motor_r->n10_300rpm_6v**
  - `interference.overlap` on motor_l,tub: `tub` and `motor_l` overlap by 0.99 mm (about 180.6 mm3).
  - `interference.overlap` on motor_r,tub: `tub` and `motor_r` overlap by 0.99 mm (about 180.6 mm3).
- **swap:drive_motor:motor_l+motor_r->n20_1000rpm_6v**
  - `interference.overlap` on belt_l,motor_l: `motor_l` and `belt_l` overlap by 0.13 mm (about 0.2 mm3).
  - `interference.overlap` on belt_r,motor_r: `motor_r` and `belt_r` overlap by 0.13 mm (about 0.2 mm3).
  - `interference.overlap` on motor_l,tub: `tub` and `motor_l` overlap by 0.93 mm (about 180.6 mm3).
  - `interference.overlap` on motor_l,whub_rl: `motor_l` and `whub_rl` overlap by 0.88 mm (about 179.5 mm3).
  - ... 4 more
- **swap:drive_motor:motor_l+motor_r->pololu_hpcb6v_30to1**
  - `interference.overlap` on belt_l,motor_l: `motor_l` and `belt_l` overlap by 0.13 mm (about 0.2 mm3).
  - `interference.overlap` on belt_r,motor_r: `motor_r` and `belt_r` overlap by 0.13 mm (about 0.2 mm3).
  - `interference.overlap` on motor_l,tub: `tub` and `motor_l` overlap by 0.88 mm (about 296.3 mm3).
  - `interference.overlap` on motor_l,whub_rl: `motor_l` and `whub_rl` overlap by 0.88 mm (about 173.3 mm3).
  - ... 4 more
- **swap:drive_motor:motor_l+motor_r->pololu_hpcb6v_50to1**
  - `interference.overlap` on belt_l,motor_l: `motor_l` and `belt_l` overlap by 0.13 mm (about 0.2 mm3).
  - `interference.overlap` on belt_r,motor_r: `motor_r` and `belt_r` overlap by 0.13 mm (about 0.2 mm3).
  - `interference.overlap` on motor_l,tub: `tub` and `motor_l` overlap by 0.88 mm (about 296.3 mm3).
  - `interference.overlap` on motor_l,whub_rl: `motor_l` and `whub_rl` overlap by 0.88 mm (about 173.3 mm3).
  - ... 4 more
- **swap:drive_motor:motor_l+motor_r->pololu_hpcb6v_75to1**
  - `interference.overlap` on belt_l,motor_l: `motor_l` and `belt_l` overlap by 0.13 mm (about 0.2 mm3).
  - `interference.overlap` on belt_r,motor_r: `motor_r` and `belt_r` overlap by 0.13 mm (about 0.2 mm3).
  - `interference.overlap` on motor_l,tub: `tub` and `motor_l` overlap by 0.88 mm (about 296.3 mm3).
  - `interference.overlap` on motor_l,whub_rl: `motor_l` and `whub_rl` overlap by 0.88 mm (about 173.3 mm3).
  - ... 4 more
- **swap:switch:power_switch->fingertech_mini_switch**
  - `assembly.blocked` on bolt_sw0: `bolt_sw0` is trapped: its best way out is along (-0, -0, -1), which gets 0.0 mm before it hits `power_switch`.
  - `assembly.blocked` on bolt_sw1: `bolt_sw1` is trapped: its best way out is along (-0, -0, -1), which gets 0.0 mm before it hits `power_switch`.
  - `assembly.blocked` on disc_a: `disc_a` is trapped: its best way out is along (0, 0, 1), which gets 2.8 mm before it hits `weapon_motor_can`.
  - `assembly.blocked` on disc_b: `disc_b` is trapped: its best way out is along (1, 0, 0), which gets 5.6 mm before it hits `tub`.
  - ... 26 more
- **swap:switch:power_switch->switch_slide_12x4**
  - `assembly.blocked` on bolt_sw0: `bolt_sw0` is trapped: its best way out is along (-0, -0, -1), which gets 0.0 mm before it hits `power_switch`.
  - `assembly.blocked` on bolt_sw1: `bolt_sw1` is trapped: its best way out is along (-0, -0, -1), which gets 0.0 mm before it hits `power_switch`.
  - `assembly.blocked` on power_switch: `power_switch` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `bolt_sw0`.
  - `fastener_seat.head_bearing` on bolt_sw0,power_switch,tub,tub: `bolt_sw0` head bears on 0% of its seat
  - ... 3 more
- **swap:switch:power_switch->switch_slide_bbb_ant**
  - `assembly.blocked` on bolt_sw0: `bolt_sw0` is trapped: its best way out is along (-0, -0, -1), which gets 0.0 mm before it hits `power_switch`.
  - `assembly.blocked` on bolt_sw1: `bolt_sw1` is trapped: its best way out is along (-0, -0, -1), which gets 0.0 mm before it hits `power_switch`.
  - `assembly.blocked` on insert_t0: `insert_t0` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `power_switch`.
  - `assembly.blocked` on power_switch: `power_switch` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `tub`.
  - ... 7 more
- **swap:weapon_esc:wesc->bbb_red_esc**
  - `electrical.esc_weapon_current` on -: `wesc` burst 1.8 A vs max 18.0 A per channel.
- **swap:weapon_motor:weapon_motor_stator->bbb_be1806_2300kv**
  - `assembly.blocked` on bolt_d0: `bolt_d0` is trapped: its best way out is along (1, -0, -0), which gets 7.7 mm before it hits `mount_r`.
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - `assembly.blocked` on bolt_p2: `bolt_p2` is trapped: its best way out is along (-1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - ... 22 more
- **swap:weapon_motor:weapon_motor_stator->be1806_bbb**
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - `assembly.blocked` on bolt_p2: `bolt_p2` is trapped: its best way out is along (-1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - `assembly.blocked` on bolt_p3: `bolt_p3` is trapped: its best way out is along (-1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - ... 21 more
- **swap:weapon_motor:weapon_motor_stator->bl_1806_2300kv**
  - `assembly.blocked` on bolt_d0: `bolt_d0` is trapped: its best way out is along (1, -0, -0), which gets 7.7 mm before it hits `mount_r`.
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - `assembly.blocked` on bolt_p2: `bolt_p2` is trapped: its best way out is along (-1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - ... 22 more
- **swap:weapon_motor:weapon_motor_stator->bl_2306_1400kv**
  - `assembly.blocked` on bolt_d0: `bolt_d0` is trapped: its best way out is along (1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - `assembly.blocked` on bolt_d1: `bolt_d1` is trapped: its best way out is along (1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - `assembly.blocked` on bolt_d2: `bolt_d2` is trapped: its best way out is along (1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - `assembly.blocked` on bolt_d3: `bolt_d3` is trapped: its best way out is along (1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - ... 37 more
- **swap:weapon_motor:weapon_motor_stator->brotherhobby_tc1404_3800kv**
  - `assembly.blocked` on bolt_d0: `bolt_d0` is trapped: its best way out is along (1, -0, -0), which gets 7.7 mm before it hits `mount_r`.
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - `assembly.blocked` on bolt_p2: `bolt_p2` is trapped: its best way out is along (-1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - ... 20 more
- **swap:weapon_motor:weapon_motor_stator->brotherhobby_tc1404_4600kv**
  - `assembly.blocked` on bolt_d0: `bolt_d0` is trapped: its best way out is along (1, -0, -0), which gets 7.7 mm before it hits `mount_r`.
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - `assembly.blocked` on bolt_p2: `bolt_p2` is trapped: its best way out is along (-1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - ... 20 more
- **swap:weapon_motor:weapon_motor_stator->c_bbb_be1806_2300kv**
  - `assembly.blocked` on bolt_d0: `bolt_d0` is trapped: its best way out is along (1, -0, -0), which gets 7.7 mm before it hits `mount_r`.
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - `assembly.blocked` on bolt_p2: `bolt_p2` is trapped: its best way out is along (-1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - ... 23 more
- **swap:weapon_motor:weapon_motor_stator->c_repeat_2004_antweight_spinner_motor**
  - `assembly.blocked` on bolt_d0: `bolt_d0` is trapped: its best way out is along (1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - `assembly.blocked` on bolt_d1: `bolt_d1` is trapped: its best way out is along (1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - `assembly.blocked` on bolt_d2: `bolt_d2` is trapped: its best way out is along (1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - `assembly.blocked` on bolt_d3: `bolt_d3` is trapped: its best way out is along (1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - ... 40 more
- **swap:weapon_motor:weapon_motor_stator->emax_eco2207_1900kv**
  - `assembly.blocked` on bolt_d0: `bolt_d0` is trapped: its best way out is along (1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - `assembly.blocked` on bolt_d1: `bolt_d1` is trapped: its best way out is along (1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - `assembly.blocked` on bolt_d2: `bolt_d2` is trapped: its best way out is along (1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - `assembly.blocked` on bolt_d3: `bolt_d3` is trapped: its best way out is along (1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - ... 37 more
- **swap:weapon_motor:weapon_motor_stator->gr1507_step**
  - `fastener_seat.thread_bite` on bolt_p0,spider,weapon_motor_can: `bolt_p0` thread bites material on 50% of the engagement
  - `fastener_seat.thread_bite` on bolt_p1,spider,weapon_motor_can: `bolt_p1` thread bites material on 50% of the engagement
  - `fastener_seat.thread_bite` on bolt_p2,spider,weapon_motor_can: `bolt_p2` thread bites material on 50% of the engagement
  - `fastener_seat.thread_bite` on bolt_p3,spider,weapon_motor_can: `bolt_p3` thread bites material on 50% of the engagement
  - ... 1 more
- **swap:weapon_motor:weapon_motor_stator->repeat_2004_1400kv**
  - `assembly.blocked` on bolt_d0: `bolt_d0` is trapped: its best way out is along (1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - `assembly.blocked` on bolt_d1: `bolt_d1` is trapped: its best way out is along (1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - `assembly.blocked` on bolt_d2: `bolt_d2` is trapped: its best way out is along (1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - `assembly.blocked` on bolt_d3: `bolt_d3` is trapped: its best way out is along (1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - ... 37 more
- **swap:weapon_motor:weapon_motor_stator->repeat_2004_2800kv**
  - `assembly.blocked` on bolt_d0: `bolt_d0` is trapped: its best way out is along (1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - `assembly.blocked` on bolt_d1: `bolt_d1` is trapped: its best way out is along (1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - `assembly.blocked` on bolt_d2: `bolt_d2` is trapped: its best way out is along (1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - `assembly.blocked` on bolt_d3: `bolt_d3` is trapped: its best way out is along (1, -0, -0), which gets 0.0 mm before it hits `weapon_motor_stator`.
  - ... 37 more
- **swap:wheel:wheel_fl+wheel_fr->bbb_wheel_22x10**
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p2: `bolt_p2` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p3: `bolt_p3` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - ... 54 more
- **swap:wheel:wheel_fl+wheel_fr->bbb_wheel_34x6_5**
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p2: `bolt_p2` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p3: `bolt_p3` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - ... 52 more
- **swap:wheel:wheel_fl+wheel_fr->durahubs_25**
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p2: `bolt_p2` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p3: `bolt_p3` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - ... 48 more
- **swap:wheel:wheel_fl+wheel_fr->durahubs_30**
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p2: `bolt_p2` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p3: `bolt_p3` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - ... 48 more
- **swap:wheel:wheel_fl+wheel_fr->durahubs_35**
  - `assembly.blocked` on base_panel: `base_panel` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `wheel_fl`.
  - `assembly.blocked` on battery: `battery` is trapped: its best way out is along (0, 0, -1), which gets 2.8 mm before it hits `base_panel`.
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - ... 84 more
- **swap:wheel:wheel_fl+wheel_fr->wheel_20x8**
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p2: `bolt_p2` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p3: `bolt_p3` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - ... 48 more
- **swap:wheel:wheel_fl+wheel_fr->wheel_28x10**
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p2: `bolt_p2` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p3: `bolt_p3` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - ... 54 more
- **swap:wheel:wheel_fl+wheel_fr->wheel_30x8**
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p2: `bolt_p2` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p3: `bolt_p3` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - ... 54 more
- **swap:wheel:wheel_rl+wheel_rr->bbb_wheel_22x10**
  - `assembly.blocked` on base_panel: `base_panel` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `wheel_rl`.
  - `assembly.blocked` on battery: `battery` is trapped: its best way out is along (0, 0, -1), which gets 2.8 mm before it hits `base_panel`.
  - `assembly.blocked` on nut_cl: `nut_cl` is trapped: its best way out is along (1, 0, 0), which gets 7.7 mm before it hits `battery`.
  - `assembly.blocked` on nut_cr: `nut_cr` is trapped: its best way out is along (-1, 0, 0), which gets 2.1 mm before it hits `power_switch`.
  - ... 25 more
- **swap:wheel:wheel_rl+wheel_rr->bbb_wheel_34x6_5**
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p2: `bolt_p2` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p3: `bolt_p3` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - ... 57 more
- **swap:wheel:wheel_rl+wheel_rr->durahubs_25**
  - `assembly.blocked` on wheel_rl: `wheel_rl` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `tub`.
  - `assembly.blocked` on wheel_rr: `wheel_rr` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `tub`.
  - `assembly.blocked` on whub_rl: `whub_rl` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `tub`.
  - `assembly.blocked` on whub_rr: `whub_rr` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `tub`.
  - ... 14 more
- **swap:wheel:wheel_rl+wheel_rr->durahubs_30**
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p2: `bolt_p2` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p3: `bolt_p3` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - ... 44 more
- **swap:wheel:wheel_rl+wheel_rr->durahubs_35**
  - `assembly.blocked` on base_panel: `base_panel` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `wheel_rl`.
  - `assembly.blocked` on battery: `battery` is trapped: its best way out is along (0, 0, -1), which gets 2.8 mm before it hits `base_panel`.
  - `assembly.blocked` on bolt_b2: `bolt_b2` is trapped: its best way out is along (-0, -0, -1), which gets 0.0 mm before it hits `wheel_rl`.
  - `assembly.blocked` on bolt_b3: `bolt_b3` is trapped: its best way out is along (-0, -0, -1), which gets 0.0 mm before it hits `wheel_rr`.
  - ... 98 more
- **swap:wheel:wheel_rl+wheel_rr->wheel_20x8**
  - `assembly.blocked` on wheel_rl: `wheel_rl` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `tub`.
  - `assembly.blocked` on wheel_rr: `wheel_rr` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `tub`.
  - `assembly.blocked` on whub_rl: `whub_rl` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `tub`.
  - `assembly.blocked` on whub_rr: `whub_rr` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `tub`.
  - ... 10 more
- **swap:wheel:wheel_rl+wheel_rr->wheel_28x10**
  - `assembly.blocked` on base_panel: `base_panel` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `wheel_rl`.
  - `assembly.blocked` on battery: `battery` is trapped: its best way out is along (0, 0, -1), which gets 2.8 mm before it hits `base_panel`.
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - ... 52 more
- **swap:wheel:wheel_rl+wheel_rr->wheel_30x8**
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p2: `bolt_p2` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p3: `bolt_p3` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - ... 40 more
- **dim:MNT_IN+10%**
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 4.2 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 4.2 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p2: `bolt_p2` is trapped: its best way out is along (-1, -0, -0), which gets 4.2 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p3: `bolt_p3` is trapped: its best way out is along (-1, -0, -0), which gets 4.2 mm before it hits `mount_l`.
  - ... 14 more
- **dim:SA[0]+10%**
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p2: `bolt_p2` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p3: `bolt_p3` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - ... 40 more
- **dim:SA[0]-10%**
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p2: `bolt_p2` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p3: `bolt_p3` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - ... 20 more
- **dim:SB[0]+10%**
  - `assembly.blocked` on bolt_slb: `bolt_slb` is trapped: its best way out is along (-1, -0, -0), which gets 0.0 mm before it hits `wedgelet_l`.
  - `assembly.blocked` on bolt_srb: `bolt_srb` is trapped: its best way out is along (1, -0, -0), which gets 0.0 mm before it hits `wedgelet_r`.
  - `assembly.blocked` on fork_l: `fork_l` is trapped: its best way out is along (-1, 0, 0), which gets 11.2 mm before it hits `bolt_slb`.
  - `assembly.blocked` on fork_r: `fork_r` is trapped: its best way out is along (1, 0, 0), which gets 11.9 mm before it hits `bolt_srb`.
  - ... 12 more
- **dim:SB[0]-10%**
  - `validity.load` on wedgelet_l: geometry failed: GEOSException: TopologyException: side location conflict at 41.57610211859798 9.2980409710375511. This can occur if the input geometr
- **dim:SB[1]+10%**
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p2: `bolt_p2` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p3: `bolt_p3` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - ... 10 more
- **dim:WY-10%**
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p2: `bolt_p2` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p3: `bolt_p3` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - ... 14 more
- **dim:WZ-10%**
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p2: `bolt_p2` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p3: `bolt_p3` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - ... 12 more
- **arch:add_servo@rear_outside**
  - `connection.cover_fasteners` on servo_rear_outside: `servo_rear_outside` is an part declared `retained: screws` held by 0 fastener(s); it needs >= 2 real screws. Snap, press-fit or tape retention alone 
  - `connection.floating` on servo_rear_outside: `servo_rear_outside` has no screw, shared print, captive pocket, joint or declared connection leading back to the chassis. Nearest part is `tub`, 0.7 
- **arch:add_servo@top_deck_rear**
  - `connection.cover_fasteners` on servo_top_deck_rear: `servo_top_deck_rear` is an part declared `retained: screws` held by 0 fastener(s); it needs >= 2 real screws. Snap, press-fit or tape retention alone
  - `connection.floating` on servo_top_deck_rear: `servo_top_deck_rear` has no screw, shared print, captive pocket, joint or declared connection leading back to the chassis. Nearest part is `top_panel
- **arch:add_servo@tub_interior_rear**
  - `assembly.blocked` on base_panel: `base_panel` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `servo_tub_interior_rear`.
  - `assembly.blocked` on battery: `battery` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `servo_tub_interior_rear`.
  - `assembly.blocked` on bolt_b4: `bolt_b4` is trapped: its best way out is along (-0, -0, -1), which gets 0.0 mm before it hits `servo_tub_interior_rear`.
  - `assembly.blocked` on insert_b0: `insert_b0` is trapped: its best way out is along (0, 0, 1), which gets 7.0 mm before it hits `insert_t1`.
  - ... 24 more
- **arch:battery.orientation=long_x**
  - `assembly.blocked` on battery: `battery` is trapped: its best way out is along (0, 0, 1), which gets 0.0 mm before it hits `tub`.
  - `assembly.blocked` on bolt_p0: `bolt_p0` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p1: `bolt_p1` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - `assembly.blocked` on bolt_p2: `bolt_p2` is trapped: its best way out is along (-1, -0, -0), which gets 2.8 mm before it hits `mount_l`.
  - ... 25 more

## How to add a hypothesis

- a part swap: add the entry to `robot/catalog_data/components.json` (or the built-in catalog); it is picked up by role.
- a layout change: append to `ARCH` in `robot/gen/changes.py` (hook name, values, keywords).
- make one expressible: declare the hook in the robot's `hooks.json` (overlay ops per value, or an env setting the build reads), or a named location under `anchors`.

---

# Addendum: whole-robot size hypotheses on dev @ c3daa39 (after #27)

## Versatility score: **100 %** of decided hypotheses hold with zero code change (19 / 19; 100 % of all 19 generated)

| family | hold / decided |
|---|---|
| swap | 0 / 0 |
| dimension | 0 / 0 |
| architecture | 0 / 0 |
| size | 19 / 19 |

Verdicts: holds 19
Run: 506 s (budget 7200.0 s, 3 workers); baseline 232.5 s with 0 blockers (excluded from the diff).

## Size hypotheses

| hypothesis | verdict | builds | new blockers | diff needed |
|---|---|---|---|---|
| overall height +10% (setting size.height) | holds | yes | - | 0 code lines (1 setting(s)) |
| overall height +20% (setting size.height) | holds | yes | - | 0 code lines (1 setting(s)) |
| overall height +30% (setting size.height) | holds | yes | - | 0 code lines (1 setting(s)) |
| overall height -10% (setting size.height) | holds | yes | - | 0 code lines (1 setting(s)) |
| overall height -20% (setting size.height) | holds | yes | - | 0 code lines (1 setting(s)) |
| overall height -30% (setting size.height) | holds | yes | - | 0 code lines (1 setting(s)) |
| overall length +10% (setting size.length) | holds | yes | - | 0 code lines (1 setting(s)) |
| overall length +20% (setting size.length) | holds | yes | - | 0 code lines (1 setting(s)) |
| overall length +30% (setting size.length) | holds | yes | - | 0 code lines (1 setting(s)) |
| overall length -10% (setting size.length) | holds | yes | - | 0 code lines (1 setting(s)) |
| overall length -20% (setting size.length) | holds | yes | - | 0 code lines (1 setting(s)) |
| overall length -30% (setting size.length) | holds | yes | - | 0 code lines (1 setting(s)) |
| short 2WD: length -20 %, front wheels removed, 2 motors | holds | yes | - | 0 code lines (3 setting(s)) |
| overall width +10% (setting size.width) | holds | yes | - | 0 code lines (1 setting(s)) |
| overall width +20% (setting size.width) | holds | yes | - | 0 code lines (1 setting(s)) |
| overall width +30% (setting size.width) | holds | yes | - | 0 code lines (1 setting(s)) |
| overall width -10% (setting size.width) | holds | yes | - | 0 code lines (1 setting(s)) |
| overall width -20% (setting size.width) | holds | yes | - | 0 code lines (1 setting(s)) |
| overall width -30% (setting size.width) | holds | yes | - | 0 code lines (1 setting(s)) |

