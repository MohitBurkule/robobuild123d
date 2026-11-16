"""Screws and heat-set inserts.

Clamshell joint: M2 socket screws from the roof (counterbored flush) through the top half into brass inserts pushed
into bores that open on the split face of the bottom half. Side-mounted parts (wedge, forks, uprights) bolt along the
normal of the face they sit on into inserts in a boss behind that face.
"""

from __future__ import annotations

from ..layout import geom
from ..intent import I, boss_r_for, screw_dir
from . import sh

from ...cad import fastener_catalog as fc
from ...cad import holes as _holes

STD_LEN = (4, 5, 6, 8, 10, 12, 16, 20)
INSERT_LEN = fc.insert(2.0)[1]  # catalogue length: the bore, the part and the seat check all agree
HEAD_STYLE = {"socket": "cap", "countersunk": "csk", "button": "button"}


def hole(at, axis, designation, head, into, grip, cbore=None):
    """(cut shape JSON, record) from robot.cad.holes, the same rules the seat checks judge with. `at` = the outer
    surface the screw enters; the record's `at` is the head bearing face (what the spec fastener gets)."""
    prims, rec = _holes.hole_plan(at, axis, designation, HEAD_STYLE[head], into, grip=grip, cbore=cbore, head_clear=0.5)
    return _holes.shape_json(prims, at, axis), rec


def front_hole(x, yf, z, plate_t, head, designation="M2x6"):
    return hole((x, yf + plate_t, z), (0.0, -1.0, 0.0), designation, head, "insert", plate_t)
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
                 f"boss r {BOSS_R}: insert OD/2 + 1.2 mm wall (2.8) raised to seat the screw head; full height", threats=["crusher_hammer", "flip_landing", "wall_slam"])
        plan.add("bottom", sh.cyl(BOSS_R, -f.zb, (x, y, f.zb / 2)), intent=boss)
        plan.add("top", sh.cyl(BOSS_R, f.zt, (x, y, f.zt / 2)), intent=boss)
        cut, rec = hole((x, y, f.zt), down, f"M2x{L}", "socket", "insert", f.zt - f.split, cbore=f.zt - head_z)
        for half in ("top", "bottom"):
            plan.late_cut(half, cut, intent=I("assembly", "counterbored clearance hole in the top half, M2 insert bore "
                                              "opening on the split face of the bottom half (robot.cad.holes)",
                                              "catalogue clearance, head recess and insert bore", threats=["flip_landing", "crusher_hammer"]))
        plan.part(id=f"insert_{tag}", kind="insert", catalog="heatset_m2", at=[x, y, f.split - INSERT_LEN / 2],
                  retained="press_fit", _half="bottom", intent=I("assembly", "brass thread in the printed half: the shell is opened for "
                                                 "service, a printed thread would wear out", "M2 heat-set, 3 mm long", threats=["wall_slam", "flip_landing"]))
        plan.screw(id=f"bolt_{tag}", designation=f"M2x{L}", at=list(rec.at), dir=down, hole=rec.hole,
                   through=["chassis_top", "chassis_bottom"], threads_into=f"insert_{tag}",
                   intent=I("assembly", "clamps the two halves at a corner; four corners keep the split closed under a hit",
                            f"longest standard length that stops above the floor: {L} mm", threats=["wall_slam", "flip_landing", "crusher_hammer"]))
        plan.keepouts.append((f"boss_{tag}", x - BOSS_R, x + BOSS_R, y - BOSS_R, y + BOSS_R))


def add_tub_screws(plan, sites, prefix="c"):
    """Open tub: a boss column at each corner site carries an insert at each end; the top sheet screws down into the top
    one, the base panel up into the bottom one (button heads: a 1 mm sheet cannot take a countersink)."""
    f = plan.frame
    col = I("load_path", "corner column: carries both sheets' screws and ties the tub's walls at the corner",
            f"r {BOSS_R}, full height", threats=["crusher_hammer", "flip_landing", "wall_slam"])
    for i, (x, y) in enumerate(sites):
        tag = f"{prefix}{i}"
        plan.add("bottom", sh.cyl(BOSS_R, -f.zb, (x, y, f.zb / 2)), intent=col)
        plan.add("top", sh.cyl(BOSS_R, f.zt, (x, y, f.zt / 2)), intent=col)
        for end, sheet, z_face, d in (("t", "lid", f.zt - f.floor, -1.0), ("b", "base_panel", f.zb + f.floor, 1.0)):
            z_ins = z_face + d * INSERT_LEN / 2
            z_outer = f.zt if d < 0 else f.zb
            cut, rec = hole((x, y, z_outer), screw_dir([0.0, 0.0, d]), "M2x5", "button", "insert", f.floor)
            plan.late_cut("bottom" if d > 0 else "top", cut,
                          intent=I("assembly", f"clearance hole in the {sheet} + M2 insert bore in the column end (robot.cad.holes)",
                                   "catalogue sizes", threats=["flip_landing"]))
            plan.part(id=f"insert_{tag}{end}", kind="insert", catalog="heatset_m2", at=[x, y, z_ins], retained="press_fit", _half="bottom" if d > 0 else "top",
                      intent=I("service", f"brass thread: the {sheet} comes off between fights", "M2 heat-set", threats=["wall_slam", "flip_landing"]))
            plan.screw(id=f"bolt_{tag}{end}", designation="M2x5", at=list(rec.at), dir=screw_dir([0.0, 0.0, d]), hole=rec.hole,
                       through=[sheet], threads_into=f"insert_{tag}{end}", head="button",
                       intent=I("assembly", f"the {sheet} goes on from {'above' if d < 0 else 'below'}: its screws are "
                                "driven along that direction into the column", f"sheet {f.floor} mm + 3.9 mm thread = M2x5", threats=["crusher_hammer", "flip_landing"]))
        plan.keepouts.append((f"boss_{tag}", x - BOSS_R, x + BOSS_R, y - BOSS_R, y + BOSS_R))


def add_front_inserts(plan, xs, z, part_id, half="top", screw_len=6, plate_t=2.4, boss_r=3.0, prefix="w", head="socket"):
    """Inserts in the front wall (axis y) for a part bolted onto the front face (wedge, fork bar)."""
    f = plan.frame
    yf = f.y1
    for i, x in enumerate(xs):
        tag = f"{prefix}{i}"
        plan.add(half, sh.cyl_axis(boss_r, yf - 10.0, yf, "y", x, z),
                 intent=I("load_path", f"boss behind the front wall: a hit on {part_id} pushes back into 10 mm of solid, "
                          "not into the 1.6 mm wall", f"boss r {boss_r}, 10 mm deep", threats=["vspin_front", "wall_slam"]))
        cut, rec = front_hole(x, yf, z, plate_t, head, f"M2x{screw_len}")
        plan.late_cut(half, cut, intent=I("assembly", "M2 insert bore behind the front face (robot.cad.holes)", "catalogue insert bore",
                                          threats=["flip_landing"]))
        plan.part(id=f"insert_{tag}", kind="insert", catalog="heatset_m2", at=[x, yf - INSERT_LEN / 2, z], rot=[90.0, 0.0, 0.0],
                  retained="press_fit", _half=half, intent=I("service", f"brass thread so {part_id} can be swapped between fights",
                                                 "M2 heat-set", threats=["vspin_front", "wall_slam"]))
        plan.screw(id=f"bolt_{tag}", designation=f"M2x{screw_len}", at=list(rec.at), dir=screw_dir([0.0, -1.0, 0.0]), hole=rec.hole,
                   through=[part_id], threads_into=f"insert_{tag}", head=head,
                   intent=I("assembly", f"{part_id} goes on from the front, so its screws are driven rearward into the wall",
                            f"plate {plate_t} mm + 3 mm thread = M2x{screw_len}" + (", countersunk flush so no head stands on the impact face"
                            if head == "countersunk" else ""), threats=["vspin_front", "wall_slam", "CF-ST04", "CF-VS01"]))
