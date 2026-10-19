"""Vertical drisk / disc on a hub motor between two printed uprights at the front (Revron-like layout, generic sizes).

Spin axis along x at (y_w, z_w) ahead of the chassis front; uprights stand on the roof (feet bolted down into inserts),
motor stator bolted to the right upright, 683 bearing in the left, lock pin through both uprights and the disc.
Forks: two laser-cut steel tines bolted to the chassis side walls, tips 0.6 mm off the floor, leading the disc.
"""

from __future__ import annotations

import math

from shapely.geometry import MultiPoint, Polygon

from ..intent import I
from . import drive as drive_mod
from . import sh, spinner
from .weapon import module

DISC_R = 20.0
DISC_T = 3.0
# spider_pair (RVRN 2.0): two floating 3 mm discs, 33 mm across the rim (tooth tips 36.2), straddling the bell on a spider
PAIR_R = 18.1  # tooth tips; rim (tooth roots) 16.5 = 33 mm disc
PAIR_BORE_B = 11.75  # floating disc's bore clears the can (r 10.5)
PAIR_BOLT_R = 14.0  # long M2 through both discs and the spider arms
PAIR_BOLT_A = (45.0, 225.0)  # disc-local angles, clear of the lock pin (135 / 315) and the lightening holes
SPIDER_R = (11.0, 12.1)  # spider ring round the can, inside the lock pin's circle (pin r 14 - 1.6)


PAIR_PIN_R = 12.5  # lock pin circle on the 33 mm disc: 2.4 mm web to the tooth roots (laser web rule 0.75 t)


def pin_r(plan):
    return PAIR_PIN_R if plan.extra.get("disc_stack") == "spider_pair" else PIN_R_FROM_AXIS


def disc_r(plan):
    return PAIR_R if plan.extra.get("disc_stack") == "spider_pair" else DISC_R
FLOOR_GAP = 2.0  # lowest point of the swept rim above the floor
FRONT_GAP = 2.5  # chassis front to the rim
PIN_R_FROM_AXIS = 14.0
PIN_ANGLE = 135.0  # degrees in the y-z plane, from +y towards +z (behind and above the axis)
FOOT_LEN = 6.0  # foot block ahead of the front wall, screwed into it along -y
ARM_LOW = 9.5  # the arm joins the foot only above this height so the foot screw below it has a clear driver path
AXIS_BOSS_R = 5.0  # round boss at the axis (bearing seat r 3.5 + wall)
STATOR_SCREW_R = 8.0
# two adjacent holes of the 1806's 4-hole stator pattern: behind (clear of the foot screws' driver path below) and
# above the axis, so nothing of the upright leads the disc
STATOR_SCREWS = ((-STATOR_SCREW_R, 0.0), (0.0, STATOR_SCREW_R))
Z_UPPER = 3.5  # upper foot screw (top half); the arm starts above its driver path
TAB_LEN, TAB_T = 6.0, 2.0  # hook tab over the roof edge
FORK_T = 1.5
FORK_MAT = "titanium"
HUB_BORE_R = 0.0  # 3 mm bore reamed after cutting: not in the laser outline, hub drawn solid
FORK_ROOT = 30.0  # fork tine length along the side wall (bolt spread against the lever of the tip)
WEDGELET_T = 3.0  # printed TPU wedgelet plate (Revron RV17/18): thick enough to stay a ramp under load


def _circle(c, r, n=20):
    return [(c[0] + r * math.cos(2 * math.pi * i / n), c[1] + r * math.sin(2 * math.pi * i / n)) for i in range(n)]


def upright_profile(yf, zb, zt, axis_yz, pin_yz, hook=True, foot_len=None):
    """Outline (y, z) of an upright: foot block flat on the front wall (screws below ARM_LOW), and an arm = hull of
    the foot's top, the round boss at the axis and the lock-pin lobe. Not convex: the screws' driver path stays clear."""
    FL = foot_len or FOOT_LEN
    foot = Polygon([(yf, zb + 1.0), (yf + FL, zb + 1.0), (yf + FL, zt), (yf, zt)])
    tab = Polygon([(yf - TAB_LEN, zt + 0.05), (yf, zt + 0.05), (yf, zt + TAB_T), (yf - TAB_LEN, zt + TAB_T)])
    ay, az = axis_yz
    arm = MultiPoint([(yf, ARM_LOW), (yf + FL, ARM_LOW), (yf, zt + TAB_T), (yf + FL, zt)]
                     + _circle(axis_yz, AXIS_BOSS_R) + _circle(pin_yz, 4.0)
                     + [q for dy, dz in STATOR_SCREWS for q in _circle((ay + dy, az + dz), 3.5)]).convex_hull
    shape = (foot.union(arm).union(tab) if hook else foot.union(arm)).simplify(0.01)
    return [(round(x, 3), round(y, 3)) for x, y in list(shape.exterior.coords)[:-1]]


@module("vspin_drisk")
class Drisk:
    @staticmethod
    def geometry(plan):
        f = plan.frame
        floor = plan.extra["_floor_z"]
        R = disc_r(plan)
        yw = f.y1 + FRONT_GAP + R
        zw = floor + FLOOR_GAP + DISC_R  # axis height is the uprights' (foot screws' driver paths stay clear under it)
        a = math.radians(PIN_ANGLE)
        pin = (yw + pin_r(plan) * math.cos(a), zw + pin_r(plan) * math.sin(a))
        # x stations along the axis: disc centred at 0, motor bell against it on -x, right upright on the stator face
        xs = dict(disc=(-DISC_T / 2, DISC_T / 2), motor=(-DISC_T / 2 - spinner.MOTOR_L, -DISC_T / 2))
        pt = TUB_PLATE_T if plan.is_tub else spinner.PLATE_T
        xs["upr"] = (xs["motor"][0] - pt, xs["motor"][0])
        xs["upl"] = (DISC_T / 2 + 5.0, DISC_T / 2 + 5.0 + pt)  # 1 mm past the 2.5 mm shaft boss end
        return yw, zw, pin, xs

    @classmethod
    def prepare(cls, plan, h, g):
        plan.extra["weapon_motor"] = "weapon_motor"
        plan.extra["disc_stack"] = getattr(h, "disc_stack", "single")
        plan.robot_type = "vertical_spinner"
        plan.archetype = "vertical_spinner_forks"
        yw, zw, pin, xs = cls.geometry(plan)
        f = plan.frame
        for side in ("upr", "upl"):
            xc = sum(xs[side]) / 2
            plan.keepouts.append((f"boss_u{side}", xc - 3.0, xc + 3.0, f.y1 - 6.0, f.y1))
        # motor phase leads leave the chassis through a hole in the front wall under the right upright
        xm = sum(xs["motor"]) / 2
        for side, sgn, yy, z in ([] if on_axle(plan) else fork_sites(plan)):
            xw = sgn * f.x1
            plan.keepouts.append((f"boss_f{side}{yy:.0f}", min(xw, xw - sgn * 8), max(xw, xw - sgn * 8), yy - 3, yy + 3))
        plan.anchors["weapon_motor.phases"] = (xm, yw, zw - 9.0)
        plan.extra.setdefault("approach", {})["weapon_motor.phases"] = (xm, f.y1 - 3.0)

    @classmethod
    def add(cls, plan, h, g):
        f = plan.frame
        yw, zw, pin, xs = cls.geometry(plan)
        xm = sum(xs["motor"]) / 2
        prof = upright_profile(f.y1, f.zb, f.zt, (yw, zw), pin, hook=not plan.is_tub, foot_len=foot_len(plan))
        z_front = round(f.zb + 3.7, 2)
        for side, label in (("upr", "upright_r"), ("upl", "upright_l")):
            x0, x1 = xs[side]
            xc = (x0 + x1) / 2
            cuts = [sh.cyl_axis(1.6, x0 - 1, x1 + 1, "x", pin[0], pin[1])]  # lock pin hole
            if plan.is_tub:
                cuts += _standoff_mount(plan, side, label, xs)
            else:
                # front screw: through the foot along -y into an insert in the front wall (bottom half)
                cuts.append(sh.cyl_axis(1.1, f.y1 - 0.5, f.y1 + FOOT_LEN + 0.5, "y", xc, z_front))
                boss_i = I("load_path", "boss behind the front wall: the disc's reaction pulls the upright foot forward; the "
                           "screw load goes into 6 mm of solid, not the 1.6 mm wall", "boss r 3, 6 mm deep")
                bore_i = I("assembly", "melt bore for the M2 insert", "3.2 mm, 4.6 deep")
                ins_i = I("service", "brass thread: the weapon module comes off for service (Revron: quick-change module)",
                          "M2 heat-set")
                scr_i = I("load_path", "the upright goes on from the front: screws along -y through the foot; the low screw "
                          "takes the tooth's upward kick as tension", "foot 6 mm + 4 mm thread = M2x10")
                plan.add("bottom", sh.cyl_axis(3.0, f.y1 - 6.0, f.y1, "y", xc, z_front), intent=boss_i)
                plan.late_cut("bottom", sh.cyl_axis(1.6, f.y1 - 4.6, f.y1 + 0.2, "y", xc, z_front), intent=bore_i)
                plan.part(id=f"insert_{side}0", kind="insert", catalog="heatset_m2", at=[xc, f.y1 - 1.7, z_front],
                          rot=[90.0, 0.0, 0.0], retained="press_fit", intent=ins_i)
                plan.screw(id=f"bolt_{side}0", designation="M2x10", at=[xc, f.y1 + FOOT_LEN, z_front], dir=[0.0, -1.0, 0.0],
                           through=[label], threads_into=f"insert_{side}0", intent=scr_i)
                # upper front screw into an insert in the top half's front wall
                z_up = Z_UPPER
                cuts.append(sh.cyl_axis(1.1, f.y1 - 0.5, f.y1 + FOOT_LEN + 0.5, "y", xc, z_up))
                plan.add("top", sh.cyl_axis(3.0, f.y1 - 6.0, f.y1, "y", xc, z_up), intent=boss_i)
                plan.late_cut("top", sh.cyl_axis(1.6, f.y1 - 4.6, f.y1 + 0.2, "y", xc, z_up), intent=bore_i)
                plan.part(id=f"insert_{side}1", kind="insert", catalog="heatset_m2", at=[xc, f.y1 - 1.7, z_up],
                          rot=[90.0, 0.0, 0.0], retained="press_fit", intent=ins_i)
                plan.screw(id=f"bolt_{side}1", designation="M2x10", at=[xc, f.y1 + FOOT_LEN, z_up], dir=[0.0, -1.0, 0.0],
                           through=[label], threads_into=f"insert_{side}1",
                           intent=I("load_path", "upper screw: with the low one it makes a couple that resists the disc's "
                                    "moment about the foot", f"{Z_UPPER - z_front:.1f} mm lever between the two screws"))
            if not plan.is_tub:
                plan.connect(label, plan.roof, "interlock",
                             "Hook tab on the foot's top lies on the roof behind the front wall (takes the peel); "
                             "2 M2 along -y into front-wall inserts", mechanical_key=True)
            if side == "upr":
                for k, (dy, dz) in enumerate(STATOR_SCREWS):
                    cuts.append(sh.cyl_axis(1.1, x0 - 1, x1 + 1, "x", yw + dy, zw + dz))
                    plan.screw(id=f"bolt_wm{'ab'[k]}", designation="M2x8" if x1 - x0 <= 6 else "M2x10", at=[x0, yw + dy, zw + dz],
                               dir=[1.0, 0.0, 0.0], through=[label], threads_into="weapon_motor",
                               intent=I("load_path", "stator screws: the motor's reaction torque goes into the upright "
                                        "through them; two holes behind/above the axis keep the driver path clear",
                                        f"1806 stator pattern r 8, M2; upright {x1 - x0:g} mm + 3 mm thread"))
            else:
                cuts.append(sh.cyl_axis(spinner.BEARING["r_out"], x0 - 0.1, x0 + spinner.BEARING["w"], "x", yw, zw))
                cuts.append(sh.cyl_axis(2.6, x0 + spinner.BEARING["w"] - 0.1, x1 + 0.5, "x", yw, zw))
            shape = sh.S(sh.side_prism(prof, x0, x1), *cuts)
            plan.part(id=label, kind="structure", material="nylon", process="fdm", shape=shape, print_orientation="+x",
                      rotates_with="fixed", color="#2a2c30", solid_fraction=0.9,
                      label=f"{x1 - x0:g} mm printed weapon upright (spin axis = build direction), foot screwed down onto the roof",
                      intent=I("load_path", "weapon upright: carries the spinning disc both sides (motor stator one side, "
                               "bearing the other) and takes the hit reaction back into the chassis front; printed flat so "
                               "layer lines do not shear across the axle hole (Revron rule)",
                               f"{x1 - x0:g} mm plate; boss r {AXIS_BOSS_R} round the axis"))
        if plan.is_tub:  # one weapon module: the uprights, their standoffs and the motor slide out forward together
            for p in plan.parts:
                if p["id"] == "upright_r":
                    p["parent"] = "upright_l"
        plan.connect("weapon_motor", "upright_r", "screw", "Stator face bolted to the right upright with 2 M2 along the motor axis")
        # motor, disc, shaft, bearing
        plan.part(id="weapon_motor", kind="weapon_motor", catalog=spinner.MOTOR, at=[xm, yw, zw], rot=[0.0, 0.0, 0.0],
                  intent=I("load_path", "the outrunner IS the disc hub: no separate shaft, pulley or belt between motor "
                           "and weapon (fewest parts, all the can's inertia stored)", "BE1806 class, 2S"),
                  rotates_with="fixed", motor_shaft_extended=True, ports={"phases": [-6.5, 0.0, -9.0]},
                  **({"parent": "upright_r"} if plan.is_tub else {}),
                  exposed=True, exposed_reason="motor-as-hub: the bell is the disc's hub between the uprights, shielded by the disc",
                  label="1806 outrunner = weapon hub: stator on the right upright, own shaft lengthened into a 683 in the left")
        if plan.extra.get("disc_stack") == "spider_pair":
            _spider_pair(plan, xs, xm)
        else:
            _single_disc(plan, xm)
        x_b0 = xs["upl"][0]
        # shaft in the disc frame: the disc's local z is world +x (rot [0, 90, 0]), origin at world x = 0
        plan.part(id="wshaft", kind="shaft", material="titanium", process="cots", stock="3 mm Ti-6Al-4V rod",
                  shaft_of="weapon_motor", rotates_with="weapon", color="#777777", parent="weapon",
                  shape=sh.cyl_axis(spinner.SHAFT_R, xm, x_b0 + spinner.BEARING["w"], "z", 0.0, 0.0),
                  label="motor rotor shaft replaced by a 3 mm Ti rod, lengthened into the 683 (circlip at the stator)",
                  intent=I("load_path", "a lengthened shaft carries the disc into the far bearing: the disc is supported "
                           "both sides, so a hit does not bend the motor's own shaft", "3 mm Ti, to the 683 bearing"))
        plan.part(id="wbearing", kind="bearing", material="steel", process="cots", stock=spinner.BEARING["stock"],
                  rotates_with="fixed", color="#555555",
                  shape=spinner.bearing_shape((x_b0 + spinner.BEARING["w"] / 2, yw, zw), "x"),
                  label="F683ZZ 3x7x3 flanged bearing in the left upright", **({"parent": "upright_l"} if plan.is_tub else {}),
                  intent=I("load_path", "second support of the rotor (both-ends support, Revron rule 2)",
                           "F683ZZ: 3 mm bore = shaft, flange takes the axial push"))
        spinner.rotor_connections(plan, "weapon", "weapon_motor", "wshaft", "wbearing", "upright_l")
        plan.extra["weapon_lock"] = {"type": "removable_pin", "dia_mm": 3.0, "axis": [1, 0, 0],
                                     "at": [0.0, round(pin[0], 3), round(pin[1], 3)],
                                     "holes": ["upright_r", "weapon", "upright_l"],
                                     "note": "red 3 mm REMOVE-BEFORE-FIGHT pin through both uprights and the disc"}
        # phase wires leave through the front wall
        plan.cut("bottom", sh.boxr(xm - 1.5, xm + 1.5, f.y1 - 3.0, f.y1 + 0.5, -5.0, 0.5),
                 intent=I("wiring", "phase leads leave through the front wall under the right upright, away from the disc",
                          "3 x 3 mm hole for 3 x 24 AWG"))
        add_forks(plan, yw)


def _disc_holes(r_light, n_light=4, extra=(), pr=PIN_R_FROM_AXIS):
    """Disc-local holes: lock pin hole and its balancing twin, lightening holes between them, `extra` (polar deg, r, hole r)."""
    a = math.radians(PIN_ANGLE)
    holes = []
    for k in range(2):
        ang = a + math.pi * k
        holes.append((pr * math.cos(ang), pr * math.sin(ang), 1.6))
    for k in range(n_light):
        ang = a + math.pi / 4 + k * math.pi / 2
        holes.append((10.0 * math.cos(ang), 10.0 * math.sin(ang), r_light))
    for deg, rr, hr in extra:
        holes.append((rr * math.cos(math.radians(deg)), rr * math.sin(math.radians(deg)), hr))
    # disc local (u, v) -> world (y, z): rot [0, 90, 0] maps local x -> -z, local y -> y; build in (z', y) order
    return [(-(v), u, r) for u, v, r in holes]


WEAPON_SPEC = {"kind": "disc", "motor": "weapon_motor", "cells": 2, "reduction": 1.0, "spin_axis": [0, 0, 1],
               "spin_dir": "ccw", "supported_both_ends": True, "teeth": 2}


def _single_disc(plan, xm):
    disc = spinner.disc_shape(DISC_R, DISC_T, HUB_BORE_R, _disc_holes(4.0))
    # the disc hangs on the motor (parent) with a revolute joint about the motor axis (motor frame = world axes)
    plan.part(id="weapon", kind="weapon", material="steel", process="laser", shape=disc,
              parent="weapon_motor", at=[-xm, 0.0, 0.0], rot=[0.0, 90.0, 0.0], rotates_with="weapon",
              joint={"kind": "revolute", "axis": [1, 0, 0], "pivot": [-xm, 0.0, 0.0], "min": 0, "max": 360, "default": 0},
              color="#d9dde2", organic=True,
              intent=I("load_path", "the disc stores the energy and delivers it at the teeth; teeth are in the "
                       "laser outline (no bolted teeth to loosen)", f"r {DISC_R} x {DISC_T} mm steel, 2 teeth, holes balanced"),
              weapon=dict(WEAPON_SPEC),
              label=f"{DISC_T:g} mm steel disc, {2 * DISC_R:g} mm, 2 hooked teeth in the outline, laser cut")


def _spider_pair(plan, xs, xm):
    """RVRN 2.0 drisk: the motor-side disc is the weapon (keyed to the bell face), a floating disc rides round the can at the
    stator end, a printed spider ring between them; two long M2 through disc, spider and floating disc (tapped) make
    the stack one rotor. The discs straddle the bell, so the energy sits on a 14 mm wide stack without a wider rotor."""
    m0, m1 = xs["motor"]
    xb = (m0 + 1.0, m0 + 1.0 + DISC_T)  # floating disc, 1 mm off the stator plate
    xsp = (xb[1], m1)  # spider fills the bell length between the discs
    bolts = [(d, PAIR_BOLT_R, 1.1) for d in PAIR_BOLT_A]
    disc_a = spinner.disc_shape(PAIR_R, DISC_T, HUB_BORE_R, _disc_holes(3.5, extra=[(d, r, 1.1) for d, r, _ in bolts], pr=PAIR_PIN_R))
    plan.part(id="weapon", kind="weapon", material="steel", process="laser", shape=disc_a,
              parent="weapon_motor", at=[-xm, 0.0, 0.0], rot=[0.0, 90.0, 0.0], rotates_with="weapon",
              joint={"kind": "revolute", "axis": [1, 0, 0], "pivot": [-xm, 0.0, 0.0], "min": 0, "max": 360, "default": 0},
              color="#d9dde2", organic=True, secondary_ops=["drilled"],
              intent=I("load_path", "motor-side disc: keyed to the bell face, it drives the stack and takes the lock pin",
                       f"33 mm rim (tips {2 * PAIR_R:g}) x {DISC_T} mm steel, 2 teeth"),
              weapon=dict(WEAPON_SPEC),
              label=f"motor-side drisk disc: {DISC_T:g} mm steel, 33 mm rim, 2 hooked teeth, 2 M2 stack holes")
    # floating disc: same outline, bore clears the can; local origin on the axis at its own centre plane
    cx_b = (xb[0] + xb[1]) / 2
    ring_holes = _disc_holes(3.0, n_light=0, extra=[(d, r, 0.8) for d, r, _ in bolts])[2:]  # no pin hole: pin stops at disc A
    disc_b = sh.S(spinner.disc_shape(PAIR_R, DISC_T, PAIR_BORE_B, []),
                  *[sh.cyl(r, DISC_T + 2, (x, y, 0)) for x, y, r in ring_holes])
    plan.part(id="disc_b", kind="other", material="steel", process="laser", shape=disc_b, parent="weapon",
              at=[0.0, 0.0, cx_b], rot=[0.0, 0.0, 0.0], rotates_with="weapon", color="#d9dde2",
              secondary_ops=["drilled", "tapped"], role="blade",
              intent=I("load_path", "floating second disc (RVRN 2.0): doubles the bite width and the stored energy on the "
                       "same bell; floats on the long M2 so a hit on one disc shares into the other",
                       f"33 mm rim x {DISC_T} mm steel, bore {2 * PAIR_BORE_B:g} clears the 21 mm can, M2 tapped"),
              label="floating drisk disc: same steel outline, 23.5 mm bore round the can, M2 tapped for the stack bolts")
    sp = sh.S(sh.U(sh.cyl(SPIDER_R[1], xsp[1] - xsp[0]),
                   *[sh.cyl(2.45, xsp[1] - xsp[0], (x, y, 0)) for x, y, _ in ring_holes]),
              sh.cyl(SPIDER_R[0], xsp[1] - xsp[0] + 2), *[sh.cyl(1.1, xsp[1] - xsp[0] + 2, (x, y, 0)) for x, y, _ in ring_holes])
    plan.part(id="spider", kind="other", material="nylon", process="fdm", shape=sp, parent="weapon", print_orientation="+z",
              at=[0.0, 0.0, (xsp[0] + xsp[1]) / 2], rot=[0.0, 0.0, 0.0], rotates_with="weapon", color="#2a2c30",
              role="spacer",
              intent=I("load_path", "spider: spaces the discs to straddle the bell and carries the stack bolts' shear "
                       "between them, so the bolts do not bend", f"ring r {SPIDER_R[0]}-{SPIDER_R[1]}, {xsp[1] - xsp[0]:.1f} mm, "
                       "an arm round each long M2"),
              label="printed drisk spider: ring round the bell, an arm round each long M2 (the bolts take the shear)")
    xa1 = -DISC_T / 2 + DISC_T  # disc A's +x face (world), disc A centred on x = 0 ... see geometry()
    for k, (deg, rr, _) in enumerate(bolts):
        u, v = rr * math.cos(math.radians(deg)), rr * math.sin(math.radians(deg))
        plan.screw(id=f"bolt_d{k}", designation="M2x16", at=[xa1, plan_y(plan) + u, plan_z(plan) + v], dir=[-1.0, 0.0, 0.0],
                   through=["weapon", "spider"], threads_into="disc_b", head="button", tool="hex1.3",
                   reason="The drisk stack is bolted up on the bench before it goes onto the bell",
                   intent=I("load_path", "long stack bolt: clamps both discs on the spider so the stack turns as one; the "
                            "floating disc is tapped (no nut in the 1 mm gap to the stator plate)",
                            f"disc 3 + spider {xsp[1] - xsp[0]:.0f} + 3 tapped = M2x16"))
    plan.connect("disc_b", "spider", "screw", "Floating disc clamped to the spider by the 2 long M2 (tapped in the disc)",
                 mechanical_key=True)
    plan.connect("spider", "weapon", "screw", "Spider clamped between the discs by the 2 long M2; its arms key it",
                 mechanical_key=True)


def plan_y(plan):
    return Drisk.geometry(plan)[0]


def plan_z(plan):
    return Drisk.geometry(plan)[1]


STANDOFF_ZS = (None, Z_UPPER)  # low standoff z is set from the belly (see standoff_points)
TUB_PLATE_T = 6.0  # standoff-rooted upright: the plate alone carries the disc's bending (RVRN 2.0: 8 mm)
TUB_FOOT_LEN = 9.0  # deeper foot = deeper neck where the arm meets it: I grows with its cube


def foot_len(plan):
    return TUB_FOOT_LEN if plan.is_tub else FOOT_LEN
LUG_W = 8.0  # chassis lug (ear) ahead of the front wall at each corner, the standoffs pass through it


def standoff_points(plan):
    """(y, z) of the two standoffs per side: through the upright feet, ahead of the front wall."""
    f = plan.frame
    return [(f.y1 + foot_len(plan) / 2, round(f.zb + 5.0, 2)), (f.y1 + foot_len(plan) / 2, Z_UPPER)]


def _standoff_mount(plan, side, label, xs):
    """Tub chassis: the upright is clamped to the inner ends of two 5 mm alu standoffs that run out sideways through a
    lug at the chassis corner to the wedgelet (Revron: uprights, standoffs and wedgelets are one quick-change front).
    Returns the holes to cut in the upright."""
    f = plan.frame
    W = f.x1
    sgn = 1 if side == "upl" else -1
    x_face = xs["upl"][1] if sgn > 0 else xs["upr"][0]  # outer face of the upright
    x_head = xs["upl"][0] if sgn > 0 else xs["upr"][1]  # inner face: screw head
    out = plan.extra.get("standoff_out", WEDGELET_T / 2)
    x_end = W + out
    cuts = []
    lug = I("load_path", "lug (ear) at the chassis corner ahead of the front wall: the standoffs pass through it, so a hit "
            "on the disc goes upright -> standoffs -> lug -> side wall", f"{LUG_W:g} mm wide, as deep as the foot")
    for half, z0, z1 in (("bottom", f.zb + 1.0, 0.0), ("top", 0.0, f.zt)):
        plan.add(half, sh.boxr(*sorted((sgn * (W - LUG_W), sgn * W)), f.y1 - 0.5, f.y1 + foot_len(plan), z0, z1), intent=lug)
    for k, (ys, zs) in enumerate(standoff_points(plan)):
        sid = f"so_{side[-1]}{k}"
        lo, hi = sorted((x_face, sgn * x_end))
        tap = [sh.cyl_axis(1.25, lo - 0.1, lo + 6.0, "x", ys, zs), sh.cyl_axis(1.25, hi - 6.0, hi + 0.1, "x", ys, zs)]
        plan.part(id=sid, kind="pin", material="aluminium", process="cots", stock=f"M3 x {hi - lo:.0f} mm alu standoff, 5 mm OD",
                  shape=sh.S(sh.cyl_axis(2.5, lo, hi, "x", ys, zs), *tap), rotates_with="fixed", color="#b8bcc2", parent=label,
                  label="5 mm alu standoff: upright on its inner end, wedgelet on its outer end, through the chassis lug",
                  intent=I("load_path", "standoff: a stiff alu tube carries the weapon upright out to the chassis lug and the "
                           "wedgelet, so the uprights need no screws into the printed front wall (Revron)",
                           f"5 mm OD, {hi - lo:.1f} mm; two per side {abs(Z_UPPER - zs) if k == 0 else 0:.1f} mm apart in z"))
        lx = sorted((sgn * (W - LUG_W - 0.5), sgn * (W + 0.5)))
        plan.cut_both(sh.U(sh.cyl_axis(2.55, *lx, "x", ys, zs), sh.boxr(*lx, ys, f.y1 + foot_len(plan) + 1.0, zs - 2.55, zs + 2.55)),
                      intent=I("service", "key-slot in the lug, open forward: the weapon module (uprights on their standoffs) "
                               "slides out forward once the wedgelets are off (Revron box-section key-slot)",
                               "5 mm + 0.1 (slide fit)"))
        plan.connect(sid, plan.body("bottom"), "pin", "Standoff sits in the forward-open key-slot of the chassis lug; the "
                     "wedgelet screwed to its end and to the front axle holds it back in the slot", mechanical_key=True)
        cuts.append(sh.cyl_axis(1.6, *sorted((x_head - sgn, x_face + sgn)), "x", ys, zs))
        plan.screw(id=f"bolt_{side}{k}", designation=f"M3x{abs(x_face - x_head) + 6:.0f}", at=[x_head, ys, zs], dir=[float(sgn), 0.0, 0.0],
                   through=[label], threads_into=sid, head="button", material="aluminium",
                   intent=I("load_path", "M3 from the upright's inner face into the standoff end: clamps the upright to the "
                            "standoff end face; button head so the key clears the disc", f"upright {abs(x_face - x_head):g} mm + 6 mm thread"))
        plan.connect(label, sid, "screw", "Upright clamped to the standoff's inner end face by an M3 along its axis")
    return cuts


def fork_sites(plan):
    f = plan.frame
    y_root = f.y1 - FORK_ROOT
    return [(side, sgn, yy, f.zb + 4.5) for side, sgn in (("l", 1), ("r", -1)) for yy in (y_root + 4.0, f.y1 - 4.0)]


def on_axle(plan) -> bool:
    """4WD belt + wedgelets: the wedgelet hangs on the front axle standoff's outer end (Revron's dual-use standoff)."""
    return plan.extra.get("axle_out", 0.0) > 0.0


def add_forks(plan, yw):
    """Side ground interface leading the disc. `forks`: laser-cut Ti tines; `wedgelets`: printed TPU ramps
    (flex over seams, shrug off the disc's own debris). 2WD: each bolted to the side wall with 2 M2 into inserts.
    4WD belt: the wedgelet slides over the front axle standoff (M3 into its end) and hooks over the roof edge."""
    f = plan.frame
    h = plan.hyp
    kind = "wedgelets" if h.front == "wedgelets" else "forks"
    floor = plan.extra["_floor_z"]
    y_tip = yw + disc_r(plan) + 6.0
    z_tip = floor + 0.6
    t = WEDGELET_T if kind == "wedgelets" else FORK_T
    mat, proc = ("tpu", "fdm") if kind == "wedgelets" else (FORK_MAT, "laser")
    axle = on_axle(plan)
    tub = plan.is_tub
    if tub:
        # tub: the wedgelet hangs on the weapon standoffs' outer ends (and the front axle's, 4WD): no hook needed
        z_hi = standoff_points(plan)[1][1]
        y_root = (plan.extra["front_axle_y"] - 5.5) if axle else f.y1 - 2.0
        prof = [(y_root, f.zb + 1.0), (y_root, z_hi + 4.5), (f.y1 + foot_len(plan), z_hi + 4.5), (y_tip, z_tip + 1.5), (y_tip, z_tip)]
    elif axle:
        y_ax = plan.extra["front_axle_y"]
        r_well = plan.extra["front_well_dy"]
        y_root = y_ax - r_well - 7.0  # the hook lands on the roof behind the front wheel's arch
        prof = [(y_root, f.zb + 1.0), (y_root, f.zt + 0.05), (f.y1 - 4.0, f.zt + 0.05), (y_tip, z_tip + 1.5), (y_tip, z_tip)]
    else:
        y_root = f.y1 - FORK_ROOT
        prof = [(y_root, f.zb + 1.0), (y_root, f.zb + 8.0), (f.y1, f.zb + 8.0), (y_tip, z_tip + 1.5), (y_tip, z_tip)]
    lip = (f"lip {z_tip - floor:.1f} mm off the floor, tip {y_tip - yw - disc_r(plan):.0f} mm ahead of the disc")
    for side, sgn in (("l", 1), ("r", -1)):
        x0 = f.x1 if sgn > 0 else -f.x1 - t
        pid = f"fork_{side}"
        cuts = []
        items = [sh.side_prism(prof, x0, x0 + t)]
        if tub:
            ends = [(f"so_{side}{k}", yy, zz) for k, (yy, zz) in enumerate(standoff_points(plan))]
            if axle:
                ends.append((f"axle_f{side}", plan.extra["front_axle_y"], 0.0))
            for k, (sid, yy, zz) in enumerate(ends):
                out = plan.extra.get("axle_out" if sid.startswith("axle") else "standoff_out", WEDGELET_T / 2)
                xa, xb = sorted((sgn * f.x1 - sgn * 0.5, sgn * (f.x1 + out + 0.05)))
                cuts.append(sh.cyl_axis(drive_mod.AXLE_R + 0.1, xa, xb, "x", yy, zz))
                cuts.append(sh.cyl_axis(1.6, x0 - 1, x0 + t + 1, "x", yy, zz))
                plan.screw(id=f"bolt_f{side}{k}", designation="M3x6", at=[sgn * (f.x1 + t), yy, zz], dir=[-sgn, 0.0, 0.0],
                           through=[pid], threads_into=sid, head="button", material="aluminium",
                           intent=I("load_path", "M3 into the standoff's outer end: the wedgelet's bore over the end takes "
                                    "the shear, the screw clamps it; " + str(len(ends)) + " points key it (Revron wedglet)",
                                    f"wedgelet {t} mm + 4.5 mm thread"))
                plan.connect(pid, sid, "screw", "Wedgelet bore over the standoff end, M3 along its axis into the tapped end",
                             mechanical_key=True)
        elif axle:
            ax = f"axle_f{side}"
            x_in, x_end = (x0, x0 + plan.extra["axle_out"] + 0.05) if sgn > 0 else (x0 + t - plan.extra["axle_out"] - 0.05, x0 + t)
            cuts.append(sh.cyl_axis(drive_mod.AXLE_R + 0.1, min(x_in, x_end) - (0.5 if sgn > 0 else 0), max(x_in, x_end) + (0 if sgn > 0 else 0.5), "x", y_ax, 0.0))
            cuts.append(sh.cyl_axis(1.6, x0 - 1, x0 + t + 1, "x", y_ax, 0.0))
            # hook over the roof edge: keys the wedgelet against turning about the standoff
            hx = sorted((sgn * (f.x1 - 5.0), sgn * (f.x1 + t)))
            items.append(sh.boxr(hx[0], hx[1], y_root, y_root + 6.0, f.zt + 0.05, f.zt + 2.0))
            plan.screw(id=f"bolt_f{side}0", designation="M3x6", at=[sgn * (f.x1 + t), y_ax, 0.0], dir=[-sgn, 0.0, 0.0],
                       through=[pid], threads_into=ax, head="button", material="aluminium",
                       intent=I("assembly", "M3 into the tapped end of the front axle standoff: the wedgelet slides on "
                                "from the side and one screw holds it (and the axle) - Revron's quick-change front",
                                f"wedgelet {t} mm + 3 mm thread"))
            plan.connect(pid, ax, "screw", "Wedgelet slides over the axle standoff end, M3 countersunk into the standoff",
                         mechanical_key=True)
            plan.connect(pid, plan.roof, "interlock", "Hook along the wedgelet's top edge lies on the roof: it keys "
                         "the wedgelet against turning about the standoff when the tip is loaded", mechanical_key=True)
        else:
            for k, (_, _, yy, z) in enumerate([q for q in fork_sites(plan) if q[0] == side]):
                cuts.append(sh.cyl_axis(1.1, x0 - 1, x0 + t + 1, "x", yy, z))
                xw = sgn * f.x1
                plan.add("bottom", sh.cyl_axis(3.0, xw - sgn * 8.0, xw, "x", yy, z) if sgn > 0 else
                         sh.cyl_axis(3.0, xw, xw + 8.0, "x", yy, z),
                         intent=I("load_path", f"boss behind the side wall: the {kind[:-1]} tip load levers about the "
                                  "front screw and this boss takes it into 8 mm of solid", "boss r 3, 8 mm deep"))
                bore = (xw - sgn * 3.6, xw + sgn * 0.2)
                plan.late_cut("bottom", sh.cyl_axis(1.6, min(bore), max(bore), "x", yy, z),
                              intent=I("assembly", "melt bore for the M2 insert", "3.2 mm, 3.6 deep"))
                plan.part(id=f"insert_f{side}{k}", kind="insert", catalog="heatset_m2", at=[xw - sgn * 1.7, yy, z],
                          rot=[0.0, 90.0, 0.0], retained="press_fit",
                          intent=I("service", f"brass thread: {kind} are consumables, swapped between fights", "M2 heat-set"))
                plan.screw(id=f"bolt_f{side}{k}", designation=f"M2x{5 if t <= 2 else 6}", at=[xw + sgn * t, yy, z],
                           dir=[-sgn, 0.0, 0.0], through=[pid], threads_into=f"insert_f{side}{k}",
                           intent=I("assembly", f"the {kind[:-1]} goes on from the side: its screws are driven inward; "
                                    f"spread {FORK_ROOT - 8:.0f} mm apart against the lever of the tip",
                                    f"plate {t} mm + 3 mm thread"))
        shape = sh.S(sh.U(*items), *cuts)
        if kind == "wedgelets":
            plan.part(id=pid, kind="fork", material=mat, process=proc, shape=shape, color="#3c4048", print_orientation="+x",
                      label=f"{t:g} mm printed TPU wedgelet leading the disc" + (", on the front axle standoff" if axle else ""),
                      intent=I("ground_game", "wedgelets get under the opponent and feed it up into the disc; TPU flexes "
                               "over floor seams and survives the disc's own hits", lip))
        else:
            plan.part(id=pid, kind="fork", material=mat, process=proc, shape=shape, color="#c9ccd1",
                      label=f"{t:g} mm Ti fork tine, laser cut, bolted to the side wall",
                      intent=I("ground_game", "fork tines get under the opponent and feed it up into the disc; thin Ti "
                               "keeps the lip low and does not bend", lip))
