"""Front ground interface: full wedge, forks, wedgelets, skirt. Each bolts onto the front face of the chassis.

A wedge is a printed sloped plate (lip 0.6 mm off the floor, ribs underneath, a mounting web against the front wall)
printed standing on its mounting face (+y up) so the layers run along the slope. Forks and wedgelets are laser-cut
sheet tines (stock gauge) bolted through a printed fork bar.
"""

from __future__ import annotations

import math

from . import fasteners, sh

LIP_GAP = 0.6
WEDGE_T = 2.0
WEB_T = 2.4


def wedge_profile(y_root, z_root, y_tip, z_floor, t=WEDGE_T):
    """Parallelogram side profile (y, z) of the sloped plate: underside lip LIP_GAP above the floor."""
    b0, b1 = (y_root - 0.5, z_root - t), (y_tip, z_floor + LIP_GAP)
    ang = math.atan2(b0[1] - b1[1], b1[0] - b0[0])
    nx, nz = math.sin(ang) * t, math.cos(ang) * t
    return [b0, (b0[0] + nx, b0[1] + nz), (b1[0] + nx, b1[1] + nz), b1], math.degrees(ang)


def rib_profile(y_root, z_root, y_tip, z_floor, z_low, frac=0.55):
    """Triangular gusset under the plate from the root down to z_low, ending `frac` of the way to the tip."""
    yb = y_root + (y_tip - y_root) * frac
    zb = z_root - WEDGE_T + (z_floor + LIP_GAP - z_root + WEDGE_T) * frac
    return [(y_root - 0.5, z_root - WEDGE_T + 0.2), (yb, zb), (yb, z_low), (y_root, z_low)]


def add_wedge(plan, length=46.0, material="petg_cf", pid="wedge"):
    f = plan.frame
    yf, W = f.y1, f.x1
    z_floor = plan.extra.get("_floor_z")
    y_tip = yf + length
    prof, ang = wedge_profile(yf, 0.13, y_tip, z_floor)
    width = 2 * W - 2.0
    items = [sh.side_prism(prof, -width / 2, width / 2),
             sh.box(width, WEB_T, f.zt - f.zb - 0.35, (0, yf + WEB_T / 2, (f.zt + f.zb) / 2 - 0.175))]
    rib = rib_profile(yf, 0.13, y_tip, z_floor, f.zb)
    for x in _rib_xs(W):
        items.append(sh.place(sh.side_prism(rib, -0.6, 0.6), (x, 0, 0)))
    xs = [round(s * W * k, 1) for k in (0.4, 0.8) for s in (1, -1)]
    z_ins = round(f.zt * 0.6, 2)
    holes = [sh.cyl_axis(1.1, yf, yf + WEB_T + 1.6, "y", x, z_ins) for x in xs]
    trim = sh.box(width + 20, 10.0, 40.0, (0, yf - 5.0, 0))
    shape = sh.S(sh.U(*items), *holes, trim)
    plan.part(id=pid, kind="wedge", material=material, process="fdm", shape=shape, color="#ff6a1a",
              print_orientation="+y", label=f"printed wedge, {ang:.0f} deg ramp, lip {LIP_GAP} mm off the floor")
    fasteners.add_front_inserts(plan, xs, z_ins, pid, plate_t=WEB_T)
    return y_tip, ang


def _rib_xs(W):
    n = 7
    return [round(-W + 1.0 + i * (2 * W - 2.0) / (n - 1), 2) for i in range(n)]


def add_front(plan, kind):
    raise NotImplementedError(f"front interface {kind}")
