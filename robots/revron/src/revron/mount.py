"""[fix-B] Weapon mounts RV02/RV03: profile, notch, standoff screws, stator holes, motor back spacer."""
import json, math, os, sys
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403


def stator_bolt_circle():
    """(dY, dZ) of the GR1507 base screws about the weapon axis: one per arm of the stator cross (STATOR_DIRS) on its PCD.
    RV03's counterbores, the back spacer's holes and the reference deviations all use this one pattern."""
    return _polar(STATOR_PCD / 2, len(STATOR_DIRS))


def _mount_clip(nose_step=False):
    """Region above the line from the notch top to the nose (the battered boss) as a polygon. The line runs on past the
    nose to Y = BIG (no horizontal step at BOSS_Z): RV03's front edge passes within 1 um of the nose point, and a corner
    there left a zero-width sliver face (visual.sliver). nose_step=True: the STEP outline (horizontal at BOSS_Z past the
    nose), which the wedgelet's nose tab is cut to."""
    if nose_step:
        return Polygon_([(TAB["y0"], MNT_TOP_Z), (BOSS_NOSE_Y, BOSS_Z), (BIG, BOSS_Z), (BIG, BIG), (0, BIG), (0, MNT_TOP_Z)])
    return Polygon_([(TAB["y0"], MNT_TOP_Z), (BIG, boss_line_z(BIG)), (BIG, BIG), (0, BIG), (0, MNT_TOP_Z)])


def _mount_profile(side, pad_up=True):
    """Weapon mount side profile (Y, Z): a teardrop round the weapon axis (R top_r) running down to the standoffs,
    with the notch that drops over the chassis tab (open to the rear)."""
    m, t = MNT_SIDE[side], TAB
    c = (WY, WZ)
    t0 = _tangent_line_circle((m["notch_y"], MNT_TOP_Z), c, m["top_r"], upper=True)
    a0 = math.degrees(math.atan2(t0[1] - c[1], t0[0] - c[0]))
    rim = _arc(c, m["top_r"], a0, m["rim_end"], WSEG_ARC)
    nose = _arc(SB, NOSE_R, NOSE_A0, -90.0, WSEG_ARC_S)
    zt = t["z0"] + t["h"]
    heel = [(t["y0"] + MNT_HEEL["step"], MNT_HEEL["z"]), (t["y0"] - MNT_HEEL["back"], MNT_HEEL["z_hook"]), (t["y0"] - MNT_HEEL["back"], MNT_HEEL["z_lip"]), (t["y0"], MNT_HEEL["z_lip"])]
    # notch front face on the lug (0 gap): the lug bears a hit before the screws
    notch = [(t["y0"], t["z0"]), (t["y1"] - t["cham"], t["z0"]), (t["y1"], t["z0"] + t["cham"]), (t["y1"], zt - t["cham"]), (t["y1"] - t["cham"], zt), (t["y0"], zt),
             (t["y0"], MNT_TOP_Z - MNT_NOTCH_UP), (t["y0"] - MNT_NOTCH_UP, MNT_TOP_Z), (m["notch_y"], MNT_TOP_Z)]
    p = _poly(rim + [nose[0]] + nose[1:] + heel + notch)
    # the nose CSK (DIN 7991 cone) is wider than the STEP's nose arc and left a 0 mm knife edge there: a local pad
    # (CSK radius + printed wall) wraps the countersink, under the nose and up the front edge (RV02's front tangent passed 0.3 mm from the cone rim)
    # pad_up=False: the pad only under the nose (the 4 mm boss carries no countersink, and a pad bump there left a knife
    # edge on the battered face); the slab's pad crosses the front edge (declared deviation)
    from shapely.geometry import Point, box as _sbox
    pad = Point(SB).buffer(NOSE_PAD_R, WSEG_HI)
    p = p.union(pad.intersection(_sbox(0, SB[1] - NOSE_PAD_R, BIG + 20, SB[1])))
    # the rear notch meets the rim tangent in a wedge thinner than a printed wall: thicken it to MNT_TIP_WALL without
    # moving the part's rearmost point (the grown copy is cut at the notch-top Y)
    from shapely.geometry import Point, box as _sb
    tip = Point((m["notch_y"], MNT_TOP_Z)).buffer(MNT_TIP_REACH, WSEG_HI).intersection(_sb(m["notch_y"], MNT_TOP_Z, BIG, BIG))
    p = p.union(p.buffer(MNT_TIP_WALL / 2, WSEG_HI).intersection(tip))
    # the notch takes the chassis tab (sharp 45 deg chamfered corners in the STEP): the corner relief must not fill the notch,
    # or the sharp tab corners would be cut away by the relief when the mount is subtracted from the chassis
    from shapely.geometry import Polygon as _P
    void = _P([(t["y0"], t["z0"]), (t["y1"] - t["cham"], t["z0"]), (t["y1"], t["z0"] + t["cham"]), (t["y1"], zt - t["cham"]),
               (t["y1"] - t["cham"], zt), (t["y0"], zt)])
    out = _sharpen(_round(p, r_out=0.0, r_in=MNT_RELIEF_R).difference(void))
    # the slab's pad above the nose goes on after the relief rounding: it crosses the front edge at a shallow angle
    # (no relief needed), and a relief-rounded crossing left arc stubs that broke the wedgelet's boolean with the mount
    return out.union(pad) if pad_up else out


def weapon_mount(side):
    """RV02 (left, shaft end) / RV03 (right, stator): 8 mm printed XALT HD plates. A 4 mm slab carries the full
    profile; the outer 4 mm is a boss above the standoff line whose outer face is battered (leans in 7.7 deg) so side
    hits glance off. The rear notch drops over the chassis tab: the tab, not the screws, takes fore/aft load."""
    m = MNT_SIDE[side]
    s = 1 if side == "r" else -1
    prof = _mount_profile(side)
    xi, xm, xo = s * MNT_IN, s * MNT_SLAB, s * MNT_OUT
    eps = m["slab_eps"]                          # RV03's STEP slab face sits just inside the slab plane, RV02's on it
    slab = _ext(prof, "yz", xi, xm - s * eps, arcs=True)
    # boss: the profile above the line from the notch top to the nose, clipped in 3D so it keeps the slab's true arcs
    # (a 2D clip left arc stubs too short to refit, whose chords against the slab's arcs made sliver faces)
    boss = _one(_ext(_mount_profile(side, pad_up=False), "yz", xm - s * eps, xo + s * BOSS_OVER, arcs=True)).intersect(_ext(_mount_clip(), "yz", xm - s * eps - s, xo + s * (BOSS_OVER + 1)))
    a_, kz, ky = m["face"]                        # outer battered face (STEP): one plane leaning in with height and towards the nose
    bb = _b()
    boss = _one(boss).split(bb.Plane(origin=(s * a_, 0.0, 0.0), z_dir=(s * 1.0, ky, kz)), keep=bb.Keep.BOTTOM)
    body = _U(slab, boss)
    cuts = []
    axis = (WY, WZ)
    if side == "r":
        cuts.append(_cyl(SHAFT_D / 2 + SHAFT_CLR, -BIG / 2, BIG / 2, axis))          # shaft end clearance
        for dy, dz in stator_bolt_circle():                                # GR1507 stator M2 on its bolt circle
            cuts.append(_stator_hole(s, dy, dz)[0])
        cuts.append(lead_groove())                                         # snap-in channel for the weapon phase leads
    else:
        cuts.append(_cyl(BRG_SEAT_R, -BIG / 2, BIG / 2, axis))                        # outboard bearing seat
        cuts.append(_cyl(NUT_RECESS_R, xm, xo + s, axis))                             # shaft nut recess
    for (y, z), fastener in zip((SA, SB), MNT_SCREW):                                 # M3 CSK into the standoffs, flush inside
        cuts.append(_mount_csk(s, y, z, fastener)[0])
    return _S(body, *cuts)


def lead_groove_section(half=False):
    """[(kind, points)] outline in (u = world X, v = offset across the run) of RV03's phase-lead C-groove section: the
    round channel (LEAD_GROOVE_R) on u = LEAD_GROOVE_X, opened to the inner face by the LEAD_MOUTH slot through the
    LEAD_LIP lip, the lip / channel chord filleted LEAD_ROUND (it was a sharp crease, mfg.sharp_internal_corner), a
    LEAD_FLOOR_W flat on the channel floor (the revolved ends then close on a flat, not on a degenerate pole: integrity.solids).
    kind 'l' = line (2 points), 'a' = arc (3 points); half=True gives the v >= 0 half closed on v = 0."""
    X, R, h, r = LEAD_GROOVE_X, LEAD_GROOVE_R, LEAD_MOUTH / 2, LEAD_ROUND
    u0 = MNT_IN - LEAD_ROUND                                                   # slot starts outside the part
    uc = X - math.sqrt((R + r) ** 2 - (h + r) ** 2)                           # fillet centre (uc, h + r): on the lip side, tangent to both
    k = R / (R + r)
    t = (X + k * (uc - X), k * (h + r))                                       # fillet / channel tangent point
    def fm(sg):   # fillet arc midpoint on the side sg
        a0, a1 = math.atan2(-r, 0.0), math.atan2(t[1] - (h + r), t[0] - uc)
        a = (a0 + a1) / 2
        return (uc + r * math.cos(a), sg * (h + r + r * math.sin(a)))
    top = [("l", [(u0, h), (uc, h)]), ("a", [(uc, h), fm(1), t])]
    w = LEAD_FLOOR_W / 2                                                      # flat floor strip: the revolved ends get a flat, not a pole on the surface
    ta, fa = math.atan2(t[1], t[0] - X), math.asin(w / R)
    am = (ta + fa) / 2
    f = (X + R * math.cos(fa), w)
    arc = lambda sg: ("a", [(t[0], sg * t[1]), (X + R * math.cos(am), sg * R * math.sin(am)), (f[0], sg * w)])   # noqa: E731
    if half:
        return [("l", [(u0, 0.0), (u0, h)])] + top + [arc(1), ("l", [f, (f[0], 0.0)]), ("l", [(f[0], 0.0), (u0, 0.0)])]
    rev = lambda e: (e[0], e[1][::-1])   # noqa: E731
    return ([("l", [(u0, -h), (u0, h)])] + top + [arc(1), ("l", [f, (f[0], -w)]), rev(arc(-1)), ("a", [(t[0], -t[1]), fm(-1), (uc, -h)]), ("l", [(uc, -h), (u0, -h)])])


def lead_groove():
    """Cutter of RV03's phase-lead C-groove: lead_groove_section() swept along the run between the lead_groove_ends(),
    each end closed by its half section revolved half a turn about the X line through it (a round end matching the section)."""
    bb = _b()
    (y0, z0), (y1, z1) = lead_groove_ends()
    L = math.hypot(y1 - y0, z1 - z0)
    ry, rz = (y1 - y0) / L, (z1 - z0) / L
    def face(y, z, outline):
        P = lambda q: bb.Vector(q[0], y - q[1] * rz, z + q[1] * ry)   # noqa: E731
        return bb.Face(bb.Wire([bb.Edge.make_line(*map(P, q)) if kd == "l" else bb.Edge.make_three_point_arc(*map(P, q)) for kd, q in outline]))
    body = bb.Solid.extrude(face(y0, z0, lead_groove_section()), bb.Vector(0, y1 - y0, z1 - z0))
    # half a turn each, outwards only: a full turn would lie on the swept prism's own faces (coincident boolean faces)
    ends = [bb.Solid.revolve(face(y, z, lead_groove_section(half=True)), 180, bb.Axis((0, y, z), (k, 0, 0))) for (y, z), k in (((y0, z0), 1), ((y1, z1), -1))]
    return _U(body, *ends)


def _mount_csk(s, y, z, fastener):
    """robot.cad.holes cutter + record for a mount-to-standoff M3 CSK (bolt_u*): head flush in the inner face, DIN 7991
    countersink (dk 6.0 head in the STEP's 6.2 mm cone) and ISO 273 loose 3.6
    clearance through the 4 mm slab, so the notch, not the shank, takes fore/aft load."""
    _repo = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
    if _repo not in sys.path:
        sys.path.insert(0, _repo)
    from robot.cad.holes import hole_tool
    return hole_tool((s * MNT_IN, y, z), (s, 0, 0), fastener, head="csk", into="through", side="head", grip=MNT_SLAB - MNT_IN, fit=MNT_SCREW_FIT, csk_clear=MNT_CSK_CLEAR)


def _stator_hole(s, dy, dz):
    """robot.cad.holes cutter + record for one RV03 stator screw (bolt_wm*): M2x8 button, head on the counterbore floor."""
    _repo = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
    if _repo not in sys.path:
        sys.path.insert(0, _repo)
    from robot.cad.holes import hole_tool
    from robot.cad import fastener_catalog as fc
    y, z = WY + dy, WZ + dz
    a_, kz, ky = MNT_SIDE["r"]["face"]
    face = a_ - kz * z - ky * y + HOLE_FACE_RISE * math.hypot(kz, ky)   # RV03 battered outer face |X| (STEP plane, see weapon_mount)
    depth = face - CB_CONE_X[1]                     # counterbore down to the STEP floor
    cut, rec = hole_tool((s * face, y, z), (-s, 0, 0), "M2x8", head="button", into="through", side="head",
                         grip=face - MNT_IN, cbore=depth, cbore_clear=2 * CB_R - fc.head(2.0, "button")[0], fit="normal")
    return _one(cut.solids()[0] if hasattr(cut, "solids") and len(cut.solids()) == 1 else cut), rec


def _stack_hole(fastener, x, y, z, sx, grip):
    """robot.cad.holes record of an M2 button screw on the weapon axis direction sx: clearance through `grip` mm, tapped beyond."""
    _m2()   # puts the repo on sys.path
    from robot.cad.holes import hole_tool
    return hole_tool((x, y, z), (sx, 0, 0), fastener, head="button", into="tapped", side="both", grip=grip, fit="close")[1]


def _bsp_window(c, a0):
    """Face (YZ plane at X 0) of one back-spacer window: the ring sector win_in..win_out, half_deg either side of a0,
    its outer corners filleted round_out and its inner ones round_in as true arcs (STEP windows, measured)."""
    bb, b = _b(), BSP
    P = lambda r, a: bb.Vector(0.0, c[0] + r * math.cos(math.radians(a)), c[1] + r * math.sin(math.radians(a)))   # noqa: E731
    lo, hi = a0 - b["half_deg"], a0 + b["half_deg"]
    w = bb.Wire([bb.Edge.make_three_point_arc(P(b["win_out"], lo), P(b["win_out"], a0), P(b["win_out"], hi)), bb.Edge.make_line(P(b["win_out"], hi), P(b["win_in"], hi)),
                 bb.Edge.make_three_point_arc(P(b["win_in"], hi), P(b["win_in"], a0), P(b["win_in"], lo)), bb.Edge.make_line(P(b["win_in"], lo), P(b["win_out"], lo))])
    f = bb.Face(w)
    rc = lambda v: math.hypot(v.Y - c[0], v.Z - c[1])   # noqa: E731
    mid = (b["win_in"] + b["win_out"]) / 2
    f = f.fillet_2d(b["round_out"], [v for v in f.vertices() if rc(v) > mid])
    return f.fillet_2d(b["round_in"], [v for v in f.vertices() if rc(v) < mid and abs(rc(v) - b["win_in"]) < 1e-6])


def motor_back_spacer():
    """1.5 mm printed spacer between the GR1507 stator base and RV03: clears the motor's rear bearing boss and wires.
    Built from true circles and arcs (a shapely polyline ring tessellates as faceted seams, visual.faceting)."""
    bb, b, c = _b(), BSP, (WY, WZ)
    x0, x1 = BSP_X
    cuts = [_cyl(b["bore_r"], x0 - 1, x1 + 1, c)]
    cuts += [_cyl(b["hole_r"], x0 - 1, x1 + 1, (WY + dy, WZ + dz)) for dy, dz in stator_bolt_circle()]
    cuts += [bb.Solid.extrude(_bsp_window(c, b["phase"] + 360.0 * k / N_STACK), bb.Vector(x1 - x0 + 2, 0, 0)).moved(bb.Location((x0 - 1, 0, 0)))
             for k in range(N_STACK)]
    return _S(_cyl(b["r"], x0, x1, c), *cuts)
