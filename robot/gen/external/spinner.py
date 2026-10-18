"""Spinner weapon modules built on one pattern: the outrunner is the weapon hub.

The stator is bolted to a static support on one side, the weapon plate is keyed to the bell, the motor's own shaft is
lengthened through the weapon into a flanged 683 bearing in the support on the other side (motor bearings + one
coaxial bearing = two supports, `kin.bearing_count`). A removable lock pin runs parallel to the spin axis through both
supports and the weapon (`weapon_lock`). Weapon plates are laser-cut steel with the teeth in the outline.
"""

from __future__ import annotations

import math

from . import sh

MOTOR = "bl_1806_2300kv"
MOTOR_R, MOTOR_L = 10.5, 14.0  # catalog can radius and length (shaft boss r 2.5 beyond the bell)
SHAFT_R = 1.5
BEARING = dict(stock="683ZZ", r_out=3.5, r_in=1.5, w=3.0)
PLATE_T = 5.0  # printed support plate thickness (along the spin axis)


def tooth_outline(radius, teeth=2, depth=1.6, n=48):
    """Closed outline of a toothed disc/bar: radius with `teeth` hooked rises (spline points, counter-clockwise)."""
    pts = []
    for i in range(n):
        a = 2 * math.pi * i / n
        ph = (a * teeth / (2 * math.pi)) % 1.0  # 0..1 within one tooth pitch
        rise = depth * (1 - ph / 0.85) if ph < 0.85 else depth * (ph - 0.85) / 0.15
        pts.append((round((radius - depth + rise) * math.cos(a), 3), round((radius - depth + rise) * math.sin(a), 3)))
    return pts


def disc_shape(radius, t, bore_r, holes, teeth=2):
    """Laser-cut toothed disc in its own XY plane (axis z), centred, with a bore and extra round holes [(x, y, r)]."""
    base = {"type": "spline_prism", "points": [list(p) for p in tooth_outline(radius, teeth)], "height": t}
    cuts = ([sh.cyl(bore_r, t + 2)] if bore_r > 0 else []) + [sh.cyl(r, t + 2, (x, y, 0)) for x, y, r in holes]
    return sh.S(base, *cuts)


def bar_shape(length, width, t, bore_r, holes):
    """Laser-cut bar spinner (rounded ends, swept tips) in its XY plane, axis z."""
    hl, hw = length / 2, width / 2
    pts = [(-hl, -hw * 0.6), (-hl + 3, -hw), (hl - 6, -hw), (hl, -hw * 0.2), (hl, hw * 0.6), (hl - 3, hw), (-hl + 6, hw),
           (-hl, hw * 0.2)]
    base = {"type": "spline_prism", "points": [[round(x, 3), round(y, 3)] for x, y in pts], "height": t}
    cuts = ([sh.cyl(bore_r, t + 2)] if bore_r > 0 else []) + [sh.cyl(r, t + 2, (x, y, 0)) for x, y, r in holes]
    return sh.S(base, *cuts)


def bearing_shape(at, axis):
    b = BEARING
    lo, hi = -b["w"] / 2, b["w"] / 2
    outer = sh.cyl_axis(b["r_out"], lo, hi, axis, 0, 0)
    inner = sh.cyl_axis(b["r_in"], lo - 1, hi + 1, axis, 0, 0)
    return sh.place(sh.S(outer, inner), at)


def rotor_connections(plan, weapon_id, motor_id, shaft_id, bearing_id, bearing_host, hub_depth=1.7):
    plan.connect(weapon_id, motor_id, "press_fit",
                 "Weapon hub bore pressed over the bell's shaft boss and keyed by 2 M3 grub screws on the shaft flat; "
                 "4 M2.5 screws clamp the plate to the bell face, circlip outboard", interference_mm=0.05, mechanical_key=True)
    plan.connect(shaft_id, motor_id, "press_fit",
                 "The motor's own rotor shaft, lengthened, pressed in the bell and held by its circlip at the stator",
                 interference_mm=0.05, mechanical_key=True)
    plan.connect(bearing_id, bearing_host, "press_fit",
                 "683ZZ flanged bearing pressed into the support, flange against the inner face (shoulder)",
                 interference_mm=0.05, mechanical_key=True)
    plan.connect(bearing_id, shaft_id, "shaft",
                 "683ZZ inner race on the shaft end: the second support of the rotor, located by a shoulder and circlip")
    plan.allow_overlap += [
        {"a": motor_id, "b": shaft_id, "max_depth_mm": 1.6, "reason": "the motor's own shaft inside its stator bore (catalog motor drawn solid)"},
        {"a": weapon_id, "b": motor_id, "max_depth_mm": hub_depth, "reason": "weapon hub drawn solid over the bell's shaft boss (catalog motor drawn with a solid boss)"},
        {"a": weapon_id, "b": shaft_id, "max_depth_mm": 1.6, "reason": "3 mm shaft bore drilled and reamed after laser cutting (secondary op), so the hub is drawn solid"},
    ]
