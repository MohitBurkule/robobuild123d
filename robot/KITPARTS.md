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

## fork_set

Fork set (robot/modules/forks.py): `n` tines `length` x `width` (tip = width*taper), `thick` sheet, `pitch` mm
apart (or outer centres `spread` apart), pitched `tilt_deg` down; style plate (own tab per tine) | sheet (one comb).
Origin = hinge axis / tab bend line, tines +y. hinge {pin_d, range: [min, max], tab_h} adds pin, lugs + mount tab;
lift {servo, angle} adds a coaxial servo + horn link. Symmetric about `x`; `mirror` (here or in the use entry)
adds the mirror-image set at -x.
Parts: rigid plate -> `<id>_<j>` (kind fork, tab with `holes` x `hole_d` screw holes); rigid sheet -> `<id>`;
hinged -> `<id>` knuckle tube (revolute about +x, joint `range` deg, + = tips up), `<id>_<j>` tines or `<id>_sheet`
(children, kind other), `<id>_mount` (lugs + tab with screw holes), `<id>_pin` (kind pin); lift adds `<id>_horn`
and `<id>_servo`. Hinged parts are kind other with no `weapon`, so the kinematics checker sweeps only the joint
range: long hinged forks on a spinner are not swept through a full circle (what blocks `kind: weapon` forks).
In kit.json the same set is `"forks": {"style": "plate" | "sheet", ...}` (placed at the nose, tips on the floor).

`style='plate', n=2, length=25.0, width=6.0, taper=1.0, thick=1.5, pitch=None, spread=30.0, tilt_deg=0.0, tab=8.0, tab_width=None, holes=1, hole_d=2.2, x=0.0, mirror=False, hinge=None, lift=None, material='titanium', process='laser'`

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

