"""Screws and heat-set inserts.

Clamshell joint: M2 socket screws from the roof (counterbored flush) through the top half into brass inserts pushed
into bores that open on the split face of the bottom half. Side-mounted parts (wedge, forks, uprights) bolt along the
normal of the face they sit on into inserts in a boss behind that face.
"""

from __future__ import annotations

from ..layout import geom
from ..intent import I, boss_r_for, screw_dir
from . import sh

STD_LEN = (4, 5, 6, 8, 10, 12, 16, 20)
INSERT_LEN = 3.0
BOSS_R = max(boss_r_for(2.0), 4.0)  # M2 insert (3.2 OD) + 1.2 mm wall = 2.8; 4.0 also seats the screw head


def std_length(max_len: float) -> int:
    ok = [L for L in STD_LEN if L <= max_len + 1e-6]
    return ok[-1] if ok else STD_LEN[0]


def clamshell_sites(plan, n_front=2, n_rear=2) -> list:
    """Bolt sites near the four corners, clear of pockets and keep-outs, inside the wall by a boss radius."""
    f = plan.frame
    inner = geom.inset(f.outline, f.wall + BOSS_R + 0.3)
    # a boss may merge into the solid housing round a wheel slot (2.5 mm), never into a cavity
    blocked = [(k[1] + 2.5, k[2] - 2.5, k[3] + 2.5, k[4] - 2.5) for k in plan.keepouts]
    blocked += [(p.x0 - 1.2, p.x1 + 1.2, p.y0 - 1.2, p.y1 + 1.2) for p in plan.pockets]
    sites = []
    for ty, n in ((f.y1, n_front), (f.y0, n_rear)):
        for sgn in (1, -1)[:n]:
            best = None
            for dx, dy in sorted(((a, b) for a in range(30) for b in range(40)), key=lambda t: (t[0] + t[1], t[1])):
                x = sgn * (f.x1 - f.wall - BOSS_R - 0.5 - dx)
                y = ty - (f.wall + BOSS_R + 0.5 + dy) * (1 if ty > 0 else -1)
                r = (x - BOSS_R, x + BOSS_R, y - BOSS_R, y + BOSS_R)
                if geom.rect_inside(r, inner.buffer(BOSS_R)) and all(geom.rect_gap(r, b) >= 0.0 for b in blocked):
                    best = (x, y)
                    break
            if best:
                sites.append(best)
    return sites


def add_clamshell_screws(plan, sites, prefix="c"):
    """A boss, an insert and a roof screw at each site."""
    f = plan.frame
    head_z = f.zt - 2.2
    L = std_length(head_z - (f.zb + f.floor + 0.3))
    tip = head_z - L
    down = screw_dir([0.0, 0.0, -1.0])  # the top half goes on from above, so its screws are driven downward
    for i, (x, y) in enumerate(sites):
        tag = f"{prefix}{i}"
        boss = I("load_path", "the clamp load of the half-joint screw goes through a solid column, not the thin roof/floor",
                 f"boss r {BOSS_R}: insert OD/2 + 1.2 mm wall (2.8) raised to seat the screw head; full height")
        plan.add("bottom", sh.cyl(BOSS_R, -f.zb, (x, y, f.zb / 2)), intent=boss)
        plan.add("top", sh.cyl(BOSS_R, f.zt, (x, y, f.zt / 2)), intent=boss)
        plan.late_cut("bottom", sh.cyl_axis(1.6, tip, f.split + 0.5, "z", x, y),
                      intent=I("assembly", "melt bore for the M2 heat-set insert", "3.2 mm hole for an M2 insert, depth = screw tip"))
        plan.late_cut("top", sh.cyl_axis(1.2, f.split - 0.5, f.zt + 0.5, "z", x, y),
                      intent=I("assembly", "clearance hole for the screw shank", "M2 + 0.4 mm"))
        plan.late_cut("top", sh.cyl_axis(2.3, head_z, f.zt + 0.5, "z", x, y),
                      intent=I("protection", "counterbore: the head sits below the roof so a hit cannot shear it off",
                               "socket head 3.8 OD + 0.8; 2.2 mm deep"))
        plan.part(id=f"insert_{tag}", kind="insert", catalog="heatset_m2", at=[x, y, tip + INSERT_LEN / 2],
                  retained="press_fit", intent=I("assembly", "brass thread in the printed half: the shell is opened for "
                                                 "service, a printed thread would wear out", "M2 heat-set, 3 mm long"))
        plan.screw(id=f"bolt_{tag}", designation=f"M2x{L}", at=[x, y, head_z], dir=down,
                   through=["chassis_top", "chassis_bottom"], threads_into=f"insert_{tag}",
                   intent=I("assembly", "clamps the two halves at a corner; four corners keep the split closed under a hit",
                            f"longest standard length that stops above the floor: {L} mm"))
        plan.keepouts.append((f"boss_{tag}", x - BOSS_R, x + BOSS_R, y - BOSS_R, y + BOSS_R))


def add_front_inserts(plan, xs, z, part_id, half="top", screw_len=6, plate_t=2.4, boss_r=3.0, prefix="w"):
    """Inserts in the front wall (axis y) for a part bolted onto the front face (wedge, fork bar)."""
    f = plan.frame
    yf = f.y1
    for i, x in enumerate(xs):
        tag = f"{prefix}{i}"
        plan.add(half, sh.cyl_axis(boss_r, yf - 10.0, yf, "y", x, z),
                 intent=I("load_path", f"boss behind the front wall: a hit on {part_id} pushes back into 10 mm of solid, "
                          "not into the 1.6 mm wall", f"boss r {boss_r}, 10 mm deep"))
        plan.late_cut(half, sh.cyl_axis(1.6, yf - 3.6, yf + 0.2, "y", x, z),
                      intent=I("assembly", "melt bore for the M2 insert", "3.2 mm hole, 3.6 deep"))
        plan.part(id=f"insert_{tag}", kind="insert", catalog="heatset_m2", at=[x, yf - 1.7, z], rot=[90.0, 0.0, 0.0],
                  retained="press_fit", intent=I("service", f"brass thread so {part_id} can be swapped between fights",
                                                 "M2 heat-set"))
        plan.screw(id=f"bolt_{tag}", designation=f"M2x{screw_len}", at=[x, yf + plate_t, z], dir=screw_dir([0.0, -1.0, 0.0]),
                   through=[part_id], threads_into=f"insert_{tag}",
                   intent=I("assembly", f"{part_id} goes on from the front, so its screws are driven rearward into the wall",
                            f"plate {plate_t} mm + 3 mm thread = M2x{screw_len}"))
