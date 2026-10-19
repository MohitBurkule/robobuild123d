"""Drive train: gearmotors in clamshell pockets, printed D-bore wheels in open wheel slots (slide on from outside).

Geometry follows the verified reference wedge (robots/wedge_2wd): motors back to back on the axle line, gearbox face
against the wall between motor pocket and wheel slot, shaft through a 4 mm hole, wheel 2.45 mm outboard of the face.

4WD belt (Revron pattern): the same two rear motors; each rear hub carries an O-ring groove on its outboard side and
drives a front wheel of the same size through a nitrile O-ring running in a tunnel inside the side wall. The front
wheel turns on a 5 mm aluminium standoff captured in a bore on the split plane (the top half clamps it, no bearing:
greased printed hub on alu, as Revron). The standoff's outer end carries the side armour / wedgelet.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

from . import sh

MOTORS = {
    # catalog id, body length (can + gearbox), body height, flats, shaft length
    "n10": dict(cat="n10_2200rpm_6v", L=21.1, h=12.0, flats=10.0, shaft=9.0),
    "n20": dict(cat="n20_1000rpm_6v", L=24.0, h=12.0, flats=10.0, shaft=10.0),
}
MOTOR_INNER_X = 5.85  # inner end of each motor (the 11.7 mm between them carries the wire channel)
FACE_TO_WHEEL = 2.45  # gearbox face to the inner face of the wheel
SIDE_MARGIN = 2.6  # outer face of the wheel to the outline
# O-ring belt (4WD): groove section on the outboard face of every wheel
GROOVE_W = 3.0  # flange 0.8 + groove 1.4 + flange 0.8
GROOVE_R = 4.5  # groove bottom radius: low enough that the tunnel clears the floor and roof skins
BELT_CORD = 1.0  # nitrile cord: the nearest stock metric O-ring section to Revron's 1.2 mm
STOCK_ID_CS1 = (30, 32, 34, 35, 36, 38, 40, 42, 45, 48, 50)  # stock 1.0 mm-section ring IDs (metric list)
BELT_STRETCH = 0.10  # over the flange radius (verifier convention); 6-7 % at the cord centre: nitrile's working range
AXLE_R = 2.5  # 5 mm OD M3 aluminium standoff (front axle, Revron)
TUNNEL_CLEAR = 0.6  # belt to tunnel wall


@dataclass
class DriveGeom:
    motor: str
    wheel_dia: float
    wheel_w: float
    axle_y: float
    belt: bool = False  # 4WD: O-ring from each rear hub to a front wheel
    front_y: float | None = None  # front axle (4WD)

    @property
    def total_w(self):
        """Wheel width along the axle: tyre + the O-ring groove section (4WD)."""
        return self.wheel_w + (GROOVE_W if self.belt else 0.0)

    @property
    def m(self):
        return MOTORS[self.motor]

    @property
    def motor_cx(self):
        return MOTOR_INNER_X + self.m["L"] / 2

    @property
    def face_x(self):
        return MOTOR_INNER_X + self.m["L"]

    @property
    def wheel_cx(self):
        return self.face_x + FACE_TO_WHEEL + self.total_w / 2

    @property
    def half_width(self):
        return self.wheel_cx + self.total_w / 2 + SIDE_MARGIN

    @property
    def tyre_cx(self):
        """Tyre (wheel part) centre |x|: the inboard part of the wheel width."""
        return self.wheel_cx - self.total_w / 2 + self.wheel_w / 2

    @property
    def groove_x(self):
        """Groove mid-plane (|x|): the outboard section of the wheel."""
        return self.wheel_cx + self.total_w / 2 - GROOVE_W / 2

    @property
    def radius(self):
        return self.wheel_dia / 2


def wheel_width(dia: float) -> float:
    return 10.0 if dia >= 25 else 8.0


def geom_for(h, axle_y: float, front_y: float | None = None) -> DriveGeom:
    belt = h.transmission == "belt" and h.drive_layout == "4WD"
    return DriveGeom(h.drive_motor, float(h.wheel_dia), wheel_width(h.wheel_dia), axle_y, belt, front_y if belt else None)


def belt_geometry(g: DriveGeom) -> dict:
    """O-ring size from the centre distance (intent: grip by stretch, no tensioner)."""
    from ..intent import belt_ring_for
    C = g.front_y - g.axle_y
    r = GROOVE_R + BELT_CORD / 2  # cord centre radius in the groove
    rf = r + 0.6  # flange radius: the loop is measured over the flanges (as the verifier does), the cord sits 0.6 lower
    L_installed = 2 * C + 2 * math.pi * rf
    ideal = belt_ring_for(C, r, r, BELT_STRETCH)
    # buy, don't make: the stock ring whose stretch over the flanges lands nearest the design stretch
    ring_id = min(STOCK_ID_CS1, key=lambda d: abs(L_installed / (math.pi * d) - 1 - BELT_STRETCH))
    stretch = L_installed / (math.pi * ring_id) - 1
    return {"centre_mm": C, "cord_r": r, "length_installed": L_installed, "length_rest": round(math.pi * ring_id, 2),
            "ring_id": ring_id, "ideal_id": ideal, "stretch": stretch}


def wheel_shape(dia: float, width: float, lighten: bool = False, bore: str = "d") -> dict:
    """Printed hub inside a tyre ring; axis along x, centred.
    bore "d": 3 mm D-bore (flat 1.0 mm from the axis) for a gearmotor shaft; "axle": round 5.2 mm bore that runs
    greased on a 5 mm standoff (4WD front wheel).
    `lighten`: the hub becomes a boss + a 2.4 mm web (with round windows when there is room) instead of a solid disc."""
    rt = dia / 2
    total = width
    xt = 0.0
    def cx(r, w, x=0.0):
        return sh.cyl(r, w, (x, 0, 0), (0, 90, 0))
    rim = sh.S(cx(rt, width, xt), cx(rt - 5.0, width + 2, xt))
    if bore == "d":
        bore_s = {"type": "intersect", "items": [sh.cyl(1.5, total + 2, rot=(0, 90, 0)), sh.box(total + 2, 3.2, 2.6, (0, 0, -0.3))]}
    else:
        bore_s = sh.cyl(AXLE_R + 0.1, total + 2, rot=(0, 90, 0))
    boss_r = 4.0 if bore == "d" else AXLE_R + 1.6
    if not lighten:
        body = cx(rt - 4.5, width, xt)
    else:
        web_t = min(width, 2.4)
        body = sh.U(cx(boss_r, width, xt), cx(rt - 4.5, web_t, xt))
    cuts = [bore_s]
    if lighten:
        r_in, r_out = boss_r + 1.0, rt - 5.0 - 1.0
        hr = (r_out - r_in) / 2
        if hr >= 1.0:
            rc = (r_in + r_out) / 2
            for k in range(5):
                a = 2 * math.pi * k / 5
                cuts.append(sh.cyl(hr, width + 2, (xt, rc * math.cos(a), rc * math.sin(a)), (0, 90, 0)))
    return sh.S(sh.U(rim, body), *cuts)


def pulley_shape(bore: str = "d") -> dict:
    """O-ring pulley printed as one piece with its wheel (fused): two flanges and a groove, axis x, centred."""
    rf = GROOVE_R + BELT_CORD / 2 + 0.6
    groove = sh.S(sh.cyl(rf + 1.0, 1.4, rot=(0, 90, 0)), sh.cyl(GROOVE_R, 1.6, rot=(0, 90, 0)))
    bore_s = ({"type": "intersect", "items": [sh.cyl(1.5, GROOVE_W + 2, rot=(0, 90, 0)), sh.box(GROOVE_W + 2, 3.2, 2.6, (0, 0, -0.3))]}
              if bore == "d" else sh.cyl(AXLE_R + 0.1, GROOVE_W + 2, rot=(0, 90, 0)))
    # a 0.4 mm spigot into the hub face on the inboard (-x) side: the two print as one piece
    spigot = sh.cyl(GROOVE_R, 0.8, (-GROOVE_W / 2, 0, 0), (0, 90, 0))
    return sh.S(sh.U(sh.cyl(rf, GROOVE_W, rot=(0, 90, 0)), spigot), groove, bore_s)


def _well(plan, g, sgn, y, side, kind):
    """Wheel well round a wheel at (sgn * wheel_cx, y, 0): solid housing block in both halves, a slot open through the
    belly (ground contact) and the roof (or an arched guard over a narrow roof slot)."""
    from ..intent import I
    zb, zt = plan.frame.zb, plan.frame.zt
    W = plan.frame.x1
    tw = g.total_w
    for half, zc in (("bottom", zb / 2), ("top", zt / 2)):
        hz = abs(zc * 2)
        plan.add(half, sh.box(tw + 5.0, g.wheel_dia + 5.8, hz, (sgn * g.wheel_cx, y, zc)),
                 intent=I("protection", f"{kind} wheel well: a closed box round the wheel so a hit from the side or a "
                          "spinner tooth lands on structure, not on the tyre", "wheel + 2.9 mm wall each way (print 1.4 mm + 1.5 mm clearance)"))
    slot_h = max(-zb, zt) + 0.5
    plan.cut("bottom", sh.box(tw + 2.0, g.wheel_dia + 3.0, slot_h, (sgn * g.wheel_cx, y, zb + slot_h / 2 - 0.25)),
             intent=I("ground_game", "slot through the belly: the tyre reaches the floor; the body rides clear of it",
                      f"wheel + 1 mm clearance each side; belly {zb} vs floor {-g.radius}"))
    h = plan.hyp
    guard = getattr(h, "wheel_guards", False) and not getattr(h, "invertible", False) and h.weapon != "hspin_bar"
    z_roof = zt - plan.frame.floor
    R = g.radius
    if guard and R + 0.3 > z_roof:
        r_in, r_out = R + 1.5, R + 2.9
        # roof slot: wide enough for the tyre chord at the roof underside, but never wider than where the guard's bore
        # leaves the roof top (else a knife edge of roof is left over the bore)
        half_roof = min(math.sqrt(max(R * R - z_roof * z_roof, 0.0)) + 1.5, math.sqrt(max(r_in * r_in - zt * zt, 0.0)) - 0.3)
        xa, xb = sgn * g.wheel_cx - (tw + 2.0) / 2, sgn * g.wheel_cx + (tw + 2.0) / 2
        plan.cut("top", sh.boxr(xa, xb, y - (g.wheel_dia + 3.0) / 2, y + (g.wheel_dia + 3.0) / 2, -0.25, z_roof),
                 intent=I("ground_game", "wheel room under the roof", "wheel + 1.5 mm"))
        plan.cut("top", {"type": "intersect", "items": [sh.cyl_axis(r_in, xa, xb, "x", y, 0.0),
                                                        sh.boxr(xa, xb, y - half_roof, y + half_roof, z_roof - 0.1, zt + r_out)]},
                 intent=I("ground_game", "the tyre top rises above the roof: a slot just as wide as it needs",
                          f"chord of R {R:g} at the roof underside + 1.5 mm"))
        lim = W - 0.35 - 1.85  # flush with the slide-on opening face: no sliver between them
        xa2, xb2 = max(xa, -lim), min(xb, lim)
        if kind == "front":
            xa2, xb2 = xa, xb
        arch = sh.S(sh.cyl_axis(r_out, xa2, xb2, "x", y, 0.0), sh.cyl_axis(r_in, xa2 - 0.5, xb2 + 0.5, "x", y, 0.0))
        plan.add("top", {"type": "intersect", "items": [arch, sh.boxr(xa2, xb2, y - r_out, y + r_out, z_roof, zt + r_out)]},
                 intent=I("protection", "wheel guard: an arch over the exposed tyre top so nothing lands on the tyre from "
                          "above; concentric, so it keeps an even wall and lands on the roof slab either side",
                          f"r {r_in:g}..{r_out:g} (1.5 mm clearance, 1.4 mm wall)"))
    else:
        plan.cut("top", sh.box(tw + 2.0, g.wheel_dia + 3.0, slot_h, (sgn * g.wheel_cx, y, zt - slot_h / 2 + 0.25)),
                 intent=I("ground_game", "slot through the roof: the tyre reaches the floor when inverted",
                          "wheel + 1 mm clearance each side"))
    wx0, wx1 = sorted((sgn * (g.wheel_cx - (tw + 5.0) / 2), sgn * (W + 0.5)))
    dy = (g.wheel_dia + 5.8) / 2
    plan.keepouts.append((f"wheel_{kind[0]}{side}" if kind == "front" else f"wheel_{side}", wx0, wx1, y - dy, y + dy))


def add_drive(plan, g: DriveGeom):
    """Two motors + two wheels on one axle; pockets, slots, shaft holes; keep-outs and wire anchors for the layout.
    4WD belt: + two front wheels on captured standoff axles, driven by O-rings in tunnels along the side walls."""
    from ..intent import I
    zb, zt = plan.frame.zb, plan.frame.zt
    W = plan.frame.x1
    m = g.m
    lighten = "wheel" in plan.extra.get("lighten", ())
    for side, sgn in (("l", 1), ("r", -1)):
        mid, wid = f"motor_{side}", f"wheel_{side}"
        plan.part(id=mid, kind="motor", catalog=m["cat"], at=[sgn * g.motor_cx, g.axle_y, 0.0],
                  rot=[0.0, 0.0, 0.0 if sgn > 0 else 180.0], label=f"{'left' if sgn > 0 else 'right'} drive",
                  intent=I("load_path", "drive: one gearmotor per side, back to back on the rear axle line (tank steering)",
                           f"{m['cat']}: torque to push 150 g at {g.wheel_dia:g} mm wheels"))
        plan.part(id=wid, kind="wheel", material="pla", process="fdm",
                  shape=wheel_shape(g.wheel_dia, g.wheel_w, lighten),
                  at=[sgn * g.tyre_cx, g.axle_y, 0.0], print_orientation="+x",
                  mass_g=round(0.0045 * g.wheel_dia ** 2 + (0.6 if g.belt else 0.0), 1),
                  label=f"{g.wheel_dia:g} x {g.wheel_w:g} mm wheel, printed hub with 3 mm D-bore, silicone tyre"
                        + (", O-ring groove outboard" if g.belt else ""),
                  intent=I("ground_game", "rear drive wheel straight on the motor shaft: no axle, bearing or coupling "
                           "to fail" + ("; its outboard groove drives the front wheel" if g.belt else ""),
                           f"{g.wheel_dia:g} mm sets ground clearance (belly {zb} above floor {-g.radius})"
                           + ("; lightened: the gate found spare mass in the hub" if lighten else "")))
        if g.belt:
            plan.part(id=f"pulley_{side}", kind="pulley", material="pla", process="fdm", shape=pulley_shape("d"),
                      at=[sgn * g.groove_x, g.axle_y, 0.0], rot=[0.0, 0.0, 0.0 if sgn > 0 else 180.0], fused_with=wid, print_orientation="+x", color="#333333",
                      label="O-ring groove printed on the outboard face of the rear hub",
                      intent=I("load_path", "drive pulley for the front wheel's O-ring, printed with the hub so it needs no "
                               "key of its own", f"groove r {GROOVE_R} (tunnel clears the floor/roof skins), {BELT_CORD} mm cord"))
        reason = ("Printed hub with a D-bore matching the flat of the 3 mm gearmotor D-shaft: the flat carries drive "
                  "torque, the 0.1 mm interference only stops the hub walking off axially")
        plan.connect(mid, wid, "press_fit", reason, interference_mm=0.1, mechanical_key=True)
        plan.allow_overlap.append({"a": mid, "b": wid, "max_depth_mm": 0.6, "reason": (
            "The catalog shaft is modelled round; the real shaft has a D-flat 1.0 mm from the axis that the wheel's "
            "D-bore keys onto, so the flat of the bore overlaps the round stand-in by up to 0.5 mm")})
        # motor housing + cavity
        hx = sgn * (g.motor_cx + 0.2)
        housing = (m["L"] + 4.1, m["flats"] + 4.5)
        for half, zc in (("bottom", zb / 2), ("top", zt / 2)):
            hz = abs(zc * 2)
            plan.add(half, sh.box(housing[0], housing[1], hz, (hx, g.axle_y, zc)),
                     intent=I("retention", "solid block round the gearmotor: the pocket in it holds the motor on every "
                              "face, so drive torque and hits go into the shell, not into a clip",
                              f"motor {m['L']} x {m['flats']} + 2 mm wall"))
        _well(plan, g, sgn, g.axle_y, side, "rear")
        cav_h = m["h"] + 1.3
        plan.cut_both(sh.box(m["L"] + 0.3, m["flats"] + 0.3, cav_h, (sgn * g.motor_cx, g.axle_y, 0.0)),
                      intent=I("retention", "motor pocket: snug on the gearbox flats (they key it against reaction torque)",
                               f"flats {m['flats']} + 0.3 mm"))
        if plan.is_tub:
            plan.cut("top", sh.box(m["L"] + 0.3, m["flats"] + 0.3, zt, (sgn * g.motor_cx, g.axle_y, zt / 2)),
                     intent=I("assembly", "tub: the motor pocket opens upward so the motor drops in from above; the top "
                              "sheet holds it down", f"flats {m['flats']} + 0.3 mm"))
        plan.cut_both(sh.box(3.3, 5.0, 3.5, (sgn * (MOTOR_INNER_X - 1.7), g.axle_y, 0.0)),
                      intent=I("wiring", "terminal tab exit into the wire channel", "tab 3 x 4.6 mm + clearance"))
        plan.cut_both(sh.cyl(2.0, 3.0, (sgn * (g.face_x + 1.15), g.axle_y, 0.0), (0, 90, 0)),
                      intent=I("load_path", "shaft hole: the gearbox boss locates in it", "boss 3.5 mm + 0.5"))
        if plan.is_tub:
            plan.cut("top", sh.boxr(*sorted((sgn * (g.face_x - 0.5), sgn * (g.face_x + 3.0))), g.axle_y - 2.0, g.axle_y + 2.0,
                                    -0.1, zt), intent=I("assembly", "tub: keyhole over the shaft hole, so the motor and "
                                                        "its shaft drop in from above (Revron rear keyhole pockets)",
                                                        "boss 3.5 mm + 0.5"))
        slot_h = max(-zb, zt) + 0.5
        side_x = sgn * (W - 0.35)
        plan.cut_both(sh.box(3.7, g.wheel_dia + 1.0, 2 * slot_h + 1, (side_x, g.axle_y, 0.0)),
                      intent=I("service", "slide-on opening in the side wall: the wheel goes on and off the shaft from "
                               "outside without opening the shell", "wheel + 0.5 mm"))
        mx0, mx1 = sorted((hx - housing[0] / 2, hx + housing[0] / 2))
        plan.keepouts.append((f"drive_{side}", mx0, mx1, g.axle_y - housing[1] / 2, g.axle_y + housing[1] / 2))
        plan.anchors[f"{mid}.terminals"] = (sgn * (MOTOR_INNER_X - 0.3), g.axle_y, 0.0)
        plan.extra.setdefault("approach", {})[f"{mid}.terminals"] = (sgn * 1.5, g.axle_y)
        if g.belt:
            _front_and_belt(plan, g, side, sgn)
    # a transverse wire lane in front of the motors: every pocket can reach the motor terminals through it
    hy = (g.m["flats"] + 4.5) / 2
    plan.keepouts.append(("lane_drive", -plan.frame.x1, plan.frame.x1, g.axle_y + hy, g.axle_y + hy + 3.0))
    plan.keepouts.append(("lane_rear", -plan.frame.x1, plan.frame.x1, g.axle_y - hy - 3.0, g.axle_y - hy))
    plan.keepouts.append(("drive_mid", -MOTOR_INNER_X, MOTOR_INNER_X, g.axle_y - 3.0, g.axle_y + 3.0))


def _front_and_belt(plan, g, side, sgn):
    """Front wheel on a captured standoff axle + the O-ring from the rear hub groove to the front hub groove."""
    from ..intent import I
    f = plan.frame
    W = f.x1
    yf = g.front_y
    plan.extra["front_axle_y"] = yf
    plan.extra["front_well_dy"] = (g.wheel_dia + 5.8) / 2
    wid, aid, bid = f"wheel_f{side}", f"axle_f{side}", f"belt_{side}"
    wcx = sgn * g.wheel_cx
    _well(plan, g, sgn, yf, side, "front")
    # axle: from inside the inner housing wall to AXLE_OUT beyond the side wall (the side armour hangs on that end)
    x_in = g.wheel_cx - g.total_w / 2 - 1.2  # 1.3 mm of the 2.5 mm inner well wall stays behind the axle end
    x_out = W + plan.extra.get("axle_out", 0.0)
    plan.part(id=aid, kind="pin", material="aluminium", process="cots", stock="M3 x 5 mm OD aluminium standoff",
              shape=sh.S(sh.cyl_axis(AXLE_R, sgn * x_in if sgn > 0 else -x_out, x_out if sgn > 0 else -x_in, "x", yf, 0.0),
                         # M3 tapped hole in the outer end (2.5 mm tap drill, 6 deep): the side armour screws in here
                         sh.cyl_axis(1.25, x_out - 6.0, x_out + 0.1, "x", yf, 0.0) if sgn > 0 else
                         sh.cyl_axis(1.25, -x_out - 0.1, -x_out + 6.0, "x", yf, 0.0)),
              rotates_with="fixed", color="#b8bcc2",
              label="5 mm alu standoff: front axle (greased, no bearing), captured in the split-plane bore",
              intent=I("load_path", "front axle: a stiff alu standoff carried at both ends (inner housing wall and side "
                       "wall), so the wheel load never cantilevers off the shell; its tapped ends take the side armour",
                       f"5 mm OD (Revron); span {x_out - x_in:.1f} mm"))
    bore = sh.cyl_axis(AXLE_R + 0.05, min(sgn * x_in, sgn * (x_out + 0.5)), max(sgn * x_in, sgn * (x_out + 0.5)), "x", yf, 0.0)
    plan.cut_both(bore, intent=I("assembly", "axle bore on the split plane: half in each shell half, so the top half "
                                 "clamps the axle and the wheel drops in from above", "5 mm + 0.1 mm"))
    if plan.is_tub:
        plan.cut("top", sh.boxr(min(sgn * x_in, sgn * (x_out + 0.5)), max(sgn * x_in, sgn * (x_out + 0.5)),
                                yf - AXLE_R - 0.05, yf + AXLE_R + 0.05, -0.1, f.zt),
                 intent=I("assembly", "tub: the axle bore is a U-slot open upward, so axle and wheel drop in from above; "
                          "the wedgelet screwed to its end holds it down", "5 mm + 0.1 mm"))
        plan.connect(aid, "tub", "interlock", "Standoff drops into the U-slot of the inner well wall and the side wall; "
                     "the wedgelet screwed into its end and the top sheet hold it down", mechanical_key=True)
    else:
        plan.connect(aid, "chassis_bottom", "interlock",
                     "Standoff lies in the half-bore of the bottom half, clamped by the top half's half-bore when the "
                     "corner screws close the shell", mechanical_key=True)
    plan.part(id=wid, kind="wheel", material="pla", process="fdm",
              shape=wheel_shape(g.wheel_dia, g.wheel_w, "wheel" in plan.extra.get("lighten", ()), bore="axle"),
              at=[sgn * g.tyre_cx, yf, 0.0], print_orientation="+x",
              joint={"kind": "revolute", "axis": [1, 0, 0], "pivot": [sgn * g.tyre_cx, yf, 0.0], "min": 0, "max": 360, "default": 0},
              mass_g=round(0.0045 * g.wheel_dia ** 2 + 0.6, 1),
              label=f"{g.wheel_dia:g} mm front wheel, printed hub greased on the 5 mm standoff, O-ring groove outboard",
              intent=I("ground_game", "driven front wheel: 4WD keeps traction when the front is lifted by a wedge and "
                       "pushes with the weapon's weight over the front", f"same {g.wheel_dia:g} mm as the rear: one belt ratio 1:1"))
    plan.connect(wid, aid, "shaft", "Printed hub turns greased on the alu standoff, located between the well walls")
    plan.part(id=f"pulley_f{side}", kind="pulley", material="pla", process="fdm", shape=pulley_shape("axle"),
              at=[sgn * g.groove_x, yf, 0.0], rot=[0.0, 0.0, 0.0 if sgn > 0 else 180.0], fused_with=wid, print_orientation="+x", color="#333333",
              label="O-ring groove printed on the outboard face of the front hub",
              intent=I("load_path", "driven pulley: the O-ring turns the front wheel through it", f"same groove as the rear: 1:1"))
    bg = belt_geometry(g)
    r = bg["cord_r"]
    xg = sgn * g.groove_x
    ring = [(yy, zz) for yy, zz in _stadium(g.axle_y, yf, r + BELT_CORD / 2)]
    inner = [(yy, zz) for yy, zz in _stadium(g.axle_y, yf, r - BELT_CORD / 2)]
    belt_shape = sh.S(sh.side_prism(ring, xg - BELT_CORD / 2, xg + BELT_CORD / 2),
                      sh.side_prism(inner, xg - BELT_CORD, xg + BELT_CORD))
    plan.part(id=bid, kind="belt", material="rubber", process="cots", shape=belt_shape, color="#111111",
              belt={"pulleys": [f"pulley_{side}", f"pulley_f{side}"], "kind": "o_ring", "length_mm": round(bg["length_rest"], 1),
                    "width_mm": BELT_CORD, "thickness_mm": 0.0,
                    "stock": {"id_mm": bg["ring_id"], "cs_mm": BELT_CORD}},
              label=f"stock {bg['ring_id']:g} x {BELT_CORD:g} mm nitrile O-ring, {bg['stretch'] * 100:.0f} % stretch: "
                    "drives the front wheel off the rear hub",
              intent=I("load_path", "O-ring belt: drives the front wheel from the rear motor, so 4WD costs no extra motor; "
                       "it slips instead of breaking under a stall", f"centre {bg['centre_mm']:.1f} mm, groove r {GROOVE_R}, "
                       f"{BELT_STRETCH * 100:.0f} % stretch -> {bg['ideal_id']:.1f} mm ID; nearest stock ring {bg['ring_id']:g} x {BELT_CORD:g} "
                       f"({bg['stretch'] * 100:.1f} %)"))
    for p in (f"pulley_{side}", f"pulley_f{side}"):
        plan.connect(bid, p, "interlock", f"O-ring seated in the groove of {p} under {BELT_STRETCH * 100:.0f} % stretch")
    # belt tunnel inside the side wall, between the two wells
    tz = r + BELT_CORD / 2 + TUNNEL_CLEAR
    x0, x1 = g.groove_x - GROOVE_W / 2 - 0.1, g.groove_x + GROOVE_W / 2 + 0.3
    z_lo = -tz
    if plan.is_tub and -tz - (f.zb + f.floor) < 0.9:  # no skin thinner than print under the tunnel: the base panel closes it
        z_lo = f.zb + f.floor
    tun = sh.boxr(min(sgn * x0, sgn * x1), max(sgn * x0, sgn * x1), g.axle_y, yf, z_lo, tz)
    plan.cut_both(tun, intent=I("protection", "belt tunnel inside the side wall: the O-ring runs enclosed between the "
                                "wheels, so nothing outside can snag or cut it", f"cord {BELT_CORD} mm + {TUNNEL_CLEAR} mm all round"))
    plan.keepouts.append((f"belt_{side}", min(sgn * (x0 - 1.4), sgn * (W + 0.5)), max(sgn * (x0 - 1.4), sgn * (W + 0.5)),
                          g.axle_y, yf))


def _stadium(y0, y1, r, n=16):
    pts = []
    for k in range(n + 1):
        a = -math.pi / 2 + math.pi * k / n
        pts.append((round(y1 + r * math.cos(a), 4), round(r * math.sin(a), 4)))
    for k in range(n + 1):
        a = math.pi / 2 + math.pi * k / n
        pts.append((round(y0 + r * math.cos(a), 4), round(r * math.sin(a), 4)))
    return pts
