"""Linkage designers: solve servo-to-arm drives numerically so nobody derives them by hand in a thinking trace.

All maths is 2D in the plane normal to the joint axes (x, z for axes along Y). Angles in degrees, counter-clockwise
from +x in that plane. The verifier sweeps every joint ON ITS OWN with all others at their default pose
(robot/checks/interference.py joint_sweeps), so a design is clean when:
  * sweeping the driven arm (tail) over its range never reaches the drive pin / horn at rest, and
  * sweeping the horn over its range never reaches the tail at rest.
`pusher_crank` returns a layout that satisfies both, with the margins it achieved, or raises LinkageError saying
which constraint failed and by how much.

    from robot.cad.linkage import pusher_crank
    L = pusher_crank(hinge=(19.05, 21.5), tail_deg=146.7, tail_len=19.9, tail_half=2.6, sweep_deg=-45,
                     servo_out=(10.1, 9.1), pin_r=1.0, horn_half=2.0, gap=0.3)
    L.pin, L.horn_r, L.horn_deg0, L.horn_range   # spec joint: range (0, L.horn_range) in L.horn_sign direction
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field


class LinkageError(ValueError):
    pass


def _v(a, b):
    return (b[0] - a[0], b[1] - a[1])


def _len(v):
    return math.hypot(v[0], v[1])


def _rot(p, c, deg):
    a = math.radians(deg)
    x, z = p[0] - c[0], p[1] - c[1]
    return (c[0] + x * math.cos(a) - z * math.sin(a), c[1] + x * math.sin(a) + z * math.cos(a))


def _polar(c, r, deg):
    a = math.radians(deg)
    return (c[0] + r * math.cos(a), c[1] + r * math.sin(a))


def seg_point(a, b, p):
    """Distance from point p to segment ab."""
    ab, ap = _v(a, b), _v(a, p)
    L2 = ab[0] ** 2 + ab[1] ** 2
    t = 0.0 if L2 == 0 else max(0.0, min(1.0, (ap[0] * ab[0] + ap[1] * ab[1]) / L2))
    return _len(_v((a[0] + t * ab[0], a[1] + t * ab[1]), p))


def seg_seg(a, b, c, d):
    """Distance between segments ab and cd (0 when they cross)."""
    def cross(o, p, q):
        return (p[0] - o[0]) * (q[1] - o[1]) - (p[1] - o[1]) * (q[0] - o[0])
    d1, d2, d3, d4 = cross(c, d, a), cross(c, d, b), cross(a, b, c), cross(a, b, d)
    if (d1 > 0) != (d2 > 0) and (d3 > 0) != (d4 > 0):
        return 0.0
    return min(seg_point(c, d, a), seg_point(c, d, b), seg_point(a, b, c), seg_point(a, b, d))


def rect_point(c, deg, length, half, p):
    """Distance from p to the bar from c along `deg`, `length` long, `half` thick each side (flat ends; 0 inside)."""
    a = math.radians(deg)
    x, z = p[0] - c[0], p[1] - c[1]
    u = x * math.cos(a) + z * math.sin(a)
    w = -x * math.sin(a) + z * math.cos(a)
    du = max(0.0, -u, u - length)
    dw = max(0.0, abs(w) - half)
    return math.hypot(du, dw)


def rect_seg(c, deg, length, half, a, b, n=40):
    """Distance from segment ab to that bar (sampled)."""
    return min(rect_point(c, deg, length, half, (a[0] + (b[0] - a[0]) * i / n, a[1] + (b[1] - a[1]) * i / n))
               for i in range(n + 1))


@dataclass
class Crank:
    pin: tuple            # pin centre at rest (x, z)
    horn_r: float         # servo output to pin
    horn_deg0: float      # horn arm angle at rest
    horn_sign: int        # +1 / -1: the horn direction that moves the pin AWAY from the tail (lift)
    horn_range: float     # largest clean horn travel in that direction, deg
    margins: dict = field(default_factory=dict)   # achieved clearances, mm
    notes: list = field(default_factory=list)

    def spec_joint(self, servo_out, axis=(0, 1, 0)):
        """Spec `joint` for a horn modelled at rest (default 0)."""
        lo, hi = sorted((0.0, self.horn_sign * self.horn_range))
        return {"kind": "revolute", "axis": list(axis), "pivot": [servo_out[0], 0.0, servo_out[1]],
                "min": round(lo, 2), "max": round(hi, 2), "default": 0.0}


def pusher_crank(hinge, tail_deg, tail_len, tail_half, sweep_deg, servo_out, pin_r=1.0, horn_half=2.0, gap=0.3,
                 max_horn_deg=60.0, step=0.5, same_plane=False) -> Crank:
    """Push-only crank: the drive pin sits just beyond the tail's END, so the tail sweep can never reach it.

    hinge       arm pivot (x, z); tail_deg: tail direction at rest; tail_len: hinge to tail end; tail_half: half the
                tail thickness. sweep_deg: signed arm travel from rest (e.g. -45 = tail rotates clockwise as it lifts).
    servo_out   servo output axis (x, z). pin_r / horn_half: pin radius and horn arm half width. gap: wanted margin.
    same_plane  False (default, the workable layout): the horn sits beside the tail along the joint axis (other Y
                band) and only the pin spans across into the tail's band, so only the PIN must clear the tail. True:
                horn and tail share a band; the whole arm must clear (usually infeasible next to a push-only pin).
    """
    corner = math.hypot(tail_len, tail_half)   # the flat end's corners reach further than tail_len as it turns
    pin = _polar(hinge, corner + pin_r + gap, tail_deg)
    hv = _v(servo_out, pin)
    R = _len(hv)
    if R < pin_r + horn_half + gap:
        raise LinkageError(f"servo output is {R:.2f} mm from the pin: closer than the horn hub can be")
    a0 = math.degrees(math.atan2(hv[1], hv[0]))
    tail_end = corner - tail_len + pin_r + gap   # pin centre beyond the tail end face, minus pin_r = surface gap
    reach = tail_len + tail_half + pin_r + gap
    notes = []

    def bar_clear(deg, p):
        pin_m = rect_point(hinge, deg, tail_len, tail_half, p) - pin_r
        if not same_plane:
            return pin_m
        return min(pin_m, rect_seg(hinge, deg, tail_len, tail_half, servo_out, p) - horn_half)

    def arm_clear(horn_deg):   # horn swept, tail at rest
        p = _polar(servo_out, R, horn_deg)
        return bar_clear(tail_deg, p), p

    # pick the horn direction that moves the pin away from the tail
    best = None
    for sgn in (1, -1):
        ok_to = 0.0
        d = step
        while d <= max_horn_deg + 1e-9:
            m, _ = arm_clear(a0 + sgn * d)
            if m < gap - 1e-9:
                break
            ok_to = d
            d += step
        if best is None or ok_to > best[1]:
            best = (sgn, ok_to)
    sgn, rng = best
    if rng <= 0:
        raise LinkageError("the horn hits the tail in both directions straight away: move the servo output")
    # tail sweep vs horn + pin at rest (flipper sweep check)
    worst = float("inf")
    n = max(2, int(abs(sweep_deg) / step) + 1)
    for i in range(n + 1):
        worst = min(worst, bar_clear(tail_deg + sweep_deg * i / n, pin))
    if worst < gap - 1e-9:
        raise LinkageError(f"the tail sweep comes {worst:.2f} mm from the horn/pin (need {gap}): move the servo "
                           f"output away from the swept sector, or route the horn round it")
    m0, _ = arm_clear(a0)
    notes.append(f"pin surface {tail_end - pin_r:.2f} mm beyond the tail end face (corner radius {corner:.2f} mm, not "
                 f"{tail_len:g}): the tail sweep never reaches it")
    if not same_plane:
        notes.append("keep the horn outside the tail's band along the joint axis; the pin spans into it")
    notes.append(f"horn turns {'+' if sgn > 0 else '-'}{rng:.1f} deg clean; set the servo travel within it")
    return Crank(pin, R, a0, sgn, rng, {"tail_sweep_mm": round(worst, 3), "horn_rest_mm": round(m0, 3),
                                         "reach_mm": round(reach, 3)}, notes)
