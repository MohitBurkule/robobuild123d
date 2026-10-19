# Revron parts vs RVRN reference CAD

Silhouette IoU along X/Y/Z (0.15 mm raster, reference placed in our world frame) and volume. Red = reference only, blue = ours only. Reference meshes are for measurement only, never imported.

| part | reference | IoU X | IoU Y | IoU Z | vol ours cm3 | vol ref cm3 | note | image |
|---|---|---|---|---|---|---|---|---|
| blade_c | RVRN_1.7_PT_10_Drisk_Blade_Motor_Side-1.STL | 0.974 | 1.0 | 0.989 | 1.879 | 1.86 |  | [blade_c.png](blade_c.png) |
| disc_f | RVRN_1.7_PT_10_Drisk_Blade_Motor_Side-1.STL | 0.645 | 1.0 | 0.989 | 1.342 | 1.86 | check compares outline only (holes filled): 0.995/0.997/0.99 | [disc_f.png](disc_f.png) |
| spacer | RVRN_1.7_PT_9_Drisk_Spacer-1.STL | 0.94 | 0.995 | 0.995 | 1.305 | 1.36 |  | [spacer.png](spacer.png) |
| upright_l | fl-1.STL | 0.926 | 0.981 | 0.987 | 2.178 | 1.999 |  | [upright_l.png](upright_l.png) |
| upright_r | fr-1.STL | 0.956 | 1.0 | 1.0 | 1.57 | 1.55 |  | [upright_r.png](upright_r.png) |
| base_panel | RVRN_1.7_PT_8_Bottom_Panel-1.STL | 0.981 | 0.984 | 0.924 | 2.516 | 2.334 |  | [base_panel.png](base_panel.png) |
| wedglet_l | MirrorLow_profile_wedglet-2.STL | 0.973 | 0.919 | 0.906 | 6.554 | 5.616 |  | [wedglet_l.png](wedglet_l.png) |
| wedglet_r | MirrorLow_profile_wedglet-2.STL | 0.973 | 0.918 | 0.905 | 6.554 | 5.616 |  | [wedglet_r.png](wedglet_r.png) |
| whub_rl | RVRN_1.7_PT_13_Rear_Wheel-2.STL | 0.947 | 0.944 | 0.942 | 1.476 | 1.499 |  | [whub_rl.png](whub_rl.png) |
| whub_fl | Micro_slx_v1.0-2_Hub_Micro-1.STL | 0.91 | 0.916 | 0.921 | 0.217 | 0.218 |  | [whub_fl.png](whub_fl.png) |
| prop_mount | RVRN_1.7_C4_BE1806_Prop_Mount_Unmodified-1.STL | 0.873 | 0.472 | 0.47 | 0.424 | 0.631 | check compares the flange+spigot union clipped to the reference (with_parts) | [prop_mount.png](prop_mount.png) |
| battery | RVRN_1.7_C7_Turnabot_180mah_2s-1.STL | 0.999 | 0.921 | 0.921 | 7.128 | 7.119 |  | [battery.png](battery.png) |
| wheel_fl | Micro_slx_v1.0-2_11OD_7ID_6W_Micro_slx-1.STL | 0.922 | 0.803 | 0.822 | 0.338 | 0.336 |  | [wheel_fl.png](wheel_fl.png) |
| wheel_rr | RVRN_1.7_C5_Scalextric_F1_Front_tyre-1.STL | 0.967 | 0.901 | 0.907 | 2.366 | 2.201 |  | [wheel_rr.png](wheel_rr.png) |
| motor_r | RVRN_1.7_C1_Turnabot_Spicy_N10_2200_RPM-1.STL | 0.97 | 0.817 | 0.812 | 1.908 | 1.807 |  | [motor_r.png](motor_r.png) |
| weapon_motor | RVRN_1.7_C2_BBB_BE1806_Rough_Motor_Model-1.STL | 0.827 | 0.919 | 0.88 | 6.895 | 6.362 |  | [weapon_motor.png](weapon_motor.png) |
| wbearing | MF85ZZ_Budget_Metal_Shielded_Flanged_Deep_Groove_Ball_Bearing_5x8x2.5mm-1.STL | 0.968 | 0.986 | 0.994 | 0.086 | 0.084 |  | [wbearing.png](wbearing.png) |
