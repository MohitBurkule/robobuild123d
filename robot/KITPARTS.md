# Shared kit parts (`use` in kit.json)

Generated from robot/kitparts.py (`robot kit --parts`). Add a part there with @part; every number a named parameter.

## drive_motor

Catalog drive gearmotor, output shaft toward +x.

`motor='bbb_n20_600rpm'`

## drive_pod

One wheel + its gearmotor on one axle. Origin = wheel centre; the motor sits inboard (-x), shaft into the wheel.
Use `mirror: "x"` for the other side (the mirrored copy points its shaft the other way).

`motor='bbb_n20_600rpm', wheel_r=14.0, wheel_w=10.0, omni=False, gap=0.5`

## electronics

Battery, ESC, receiver and switch in a row (catalog parts), centred on the origin, packed along `along`.

`battery='lipo_2s_180', esc='bbb_malenki_nano', receiver='rx_fs_ia6_decased', switch='switch_slide_bbb_ant', gap=2.0, along='y'`

## hinged_arm

Flipper / lifter / axe / hammer arm. Origin = hinge (axis x), arm runs +y. head [x, y, z] box at the tip.

`length=50.0, width=40.0, thick=2.0, head=None, kind='flipper', material='titanium'`

## omni_wheel

Omni wheel: hub disc + `rollers` free rollers round the rim, axles tangential. Axle along x.

`radius=14.0, width=8.0, rollers=8, roller_r=3.0, color='#202226'`

## spinner_disc

Disc / drum / bar spinner from robot.gen.external.spinner, spinning about `axis` (x = vertical spinner).

`radius=30.0, thick=4.0, teeth=2, kind='disc', axis='x', material='steel'`

## weapon_motor

Catalog brushless weapon motor, shaft toward +x.

`motor='be1806_bbb'`

## wheel

Plain printed wheel: TPU tyre on a hub, axle along x.

`radius=14.0, width=10.0, hub=10.0, color='#202226'`

