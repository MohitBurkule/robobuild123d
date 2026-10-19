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


def upright_profile(yf, zb, zt, axis_yz, pin_yz):
    """Outline (y, z) of an upright: foot block flat on the front wall (screws below ARM_LOW), and an arm = hull of
    the foot's top, the round boss at the axis and the lock-pin lobe. Not convex: the screws' driver path stays clear."""
    foot = Polygon([(yf, zb + 1.0), (yf + FOOT_LEN, zb + 1.0), (yf + FOOT_LEN, zt), (yf, zt)])
    tab = Polygon([(yf - TAB_LEN, zt + 0.05), (yf, zt + 0.05), (yf, zt + TAB_T), (yf - TAB_LEN, zt + TAB_T)])
    ay, az = axis_yz
    arm = MultiPoint([(yf, ARM_LOW), (yf + FOOT_LEN, ARM_LOW), (yf, zt + TAB_T), (yf + FOOT_LEN, zt)]
                     + _circle(axis_yz, AXIS_BOSS_R) + _circle(pin_yz, 4.0)
                     + [q for dy, dz in STATOR_SCREWS for q in _circle((ay + dy, az + dz), 3.5)]).convex_hull
    shape = foot.union(arm).union(tab).simplify(0.01)
    return [(round(x, 3), round(y, 3)) for x, y in list(shape.exterior.coords)[:-1]]


@module("vspin_drisk")
class Drisk:
    @staticmethod
    def geometry(plan):
        f = plan.frame
        floor = plan.extra["_floor_z"]
        yw = f.y1 + FRONT_GAP + DISC_R
        zw = floor + FLOOR_GAP + DISC_R
        a = math.radians(PIN_ANGLE)
        pin = (yw + PIN_R_FROM_AXIS * math.cos(a), zw + PIN_R_FROM_AXIS * math.sin(a))
        # x stations along the axis: disc centred at 0, motor bell against it on -x, right upright on the stator face
        xs = dict(disc=(-DISC_T / 2, DISC_T / 2), motor=(-DISC_T / 2 - spinner.MOTOR_L, -DISC_T / 2))
        xs["upr"] = (xs["motor"][0] - spinner.PLATE_T, xs["motor"][0])
        xs["upl"] = (DISC_T / 2 + 5.0, DISC_T / 2 + 5.0 + spinner.PLATE_T)  # 1 mm past the 2.5 mm shaft boss end
        return yw, zw, pin, xs

    @classmethod
    def prepare(cls, plan, h, g):
        plan.extra["weapon_motor"] = "weapon_motor"
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
        prof = upright_profile(f.y1, f.zb, f.zt, (yw, zw), pin)
        z_front = round(f.zb + 3.7, 2)
        for side, label in (("upr", "upright_r"), ("upl", "upright_l")):
            x0, x1 = xs[side]
            xc = (x0 + x1) / 2
            cuts = [sh.cyl_axis(1.6, x0 - 1, x1 + 1, "x", pin[0], pin[1])]  # lock pin hole
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
            plan.connect(label, "chassis_top", "interlock",
                         "Hook tab on the foot's top lies on the roof behind the front wall (takes the peel); "
                         "2 M2 along -y into front-wall inserts", mechanical_key=True)
            if side == "upr":
                for k, (dy, dz) in enumerate(STATOR_SCREWS):
                    cuts.append(sh.cyl_axis(1.1, x0 - 1, x1 + 1, "x", yw + dy, zw + dz))
                    plan.screw(id=f"bolt_wm{'ab'[k]}", designation="M2x8", at=[x0, yw + dy, zw + dz],
                               dir=[1.0, 0.0, 0.0], through=[label], threads_into="weapon_motor",
                               intent=I("load_path", "stator screws: the motor's reaction torque goes into the upright "
                                        "through them; two holes behind/above the axis keep the driver path clear",
                                        "1806 stator pattern r 8, M2; upright 5 mm + 3 mm thread"))
            else:
                cuts.append(sh.cyl_axis(spinner.BEARING["r_out"], x0 - 0.1, x0 + spinner.BEARING["w"], "x", yw, zw))
                cuts.append(sh.cyl_axis(2.6, x0 + spinner.BEARING["w"] - 0.1, x1 + 0.5, "x", yw, zw))
            shape = sh.S(sh.side_prism(prof, x0, x1), *cuts)
            plan.part(id=label, kind="structure", material="nylon", process="fdm", shape=shape, print_orientation="+x",
                      rotates_with="fixed", color="#2a2c30", solid_fraction=0.9,
                      label=f"{spinner.PLATE_T:g} mm printed weapon upright (spin axis = build direction), foot screwed down onto the roof",
                      intent=I("load_path", "weapon upright: carries the spinning disc both sides (motor stator one side, "
                               "bearing the other) and takes the hit reaction back into the chassis front; printed flat so "
                               "layer lines do not shear across the axle hole (Revron rule)",
                               f"{spinner.PLATE_T:g} mm plate; boss r {AXIS_BOSS_R} round the axis"))
        plan.connect("weapon_motor", "upright_r", "screw", "Stator face bolted to the right upright with 2 M2 along the motor axis")
        # motor, disc, shaft, bearing
        plan.part(id="weapon_motor", kind="weapon_motor", catalog=spinner.MOTOR, at=[xm, yw, zw], rot=[0.0, 0.0, 0.0],
                  intent=I("load_path", "the outrunner IS the disc hub: no separate shaft, pulley or belt between motor "
                           "and weapon (fewest parts, all the can's inertia stored)", "BE1806 class, 2S"),
                  rotates_with="fixed", motor_shaft_extended=True, ports={"phases": [-6.5, 0.0, -9.0]},
                  exposed=True, exposed_reason="motor-as-hub: the bell is the disc's hub between the uprights, shielded by the disc",
                  label="1806 outrunner = weapon hub: stator on the right upright, own shaft lengthened into a 683 in the left")
        a = math.radians(PIN_ANGLE)
        # disc-local holes: lock pin hole and its balancing twin, four lightening holes between them
        holes = []
        for k in range(2):
            ang = a + math.pi * k
            holes.append((PIN_R_FROM_AXIS * math.cos(ang), PIN_R_FROM_AXIS * math.sin(ang), 1.6))
        for k in range(4):
            ang = a + math.pi / 4 + k * math.pi / 2
            holes.append((10.0 * math.cos(ang), 10.0 * math.sin(ang), 4.0))
        # disc local (u, v) -> world (y, z): rot [0, 90, 0] maps local x -> -z, local y -> y; build in (z', y) order
        holes_local = [(-(v), u, r) for u, v, r in holes]
        disc = spinner.disc_shape(DISC_R, DISC_T, HUB_BORE_R, holes_local)
        # the disc hangs on the motor (parent) with a revolute joint about the motor axis (motor frame = world axes)
        plan.part(id="weapon", kind="weapon", material="steel", process="laser", shape=disc,
                  parent="weapon_motor", at=[-xm, 0.0, 0.0], rot=[0.0, 90.0, 0.0], rotates_with="weapon",
                  joint={"kind": "revolute", "axis": [1, 0, 0], "pivot": [-xm, 0.0, 0.0], "min": 0, "max": 360, "default": 0},
                  color="#d9dde2", organic=True,
                  intent=I("load_path", "the disc stores the energy and delivers it at the teeth; teeth are in the "
                           "laser outline (no bolted teeth to loosen)", f"r {DISC_R} x {DISC_T} mm steel, 2 teeth, holes balanced"),
                  weapon={"kind": "disc", "motor": "weapon_motor", "cells": 2, "reduction": 1.0, "spin_axis": [0, 0, 1],
                          "spin_dir": "ccw", "supported_both_ends": True, "teeth": 2},
                  label=f"{DISC_T:g} mm steel disc, {2 * DISC_R:g} mm, 2 hooked teeth in the outline, laser cut")
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
                  label="F683ZZ 3x7x3 flanged bearing in the left upright",
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
    y_tip = yw + DISC_R + 6.0
    z_tip = floor + 0.6
    t = WEDGELET_T if kind == "wedgelets" else FORK_T
    mat, proc = ("tpu", "fdm") if kind == "wedgelets" else (FORK_MAT, "laser")
    axle = on_axle(plan)
    if axle:
        y_ax = plan.extra["front_axle_y"]
        r_well = plan.extra["front_well_dy"]
        y_root = y_ax - r_well - 7.0  # the hook lands on the roof behind the front wheel's arch
        prof = [(y_root, f.zb + 1.0), (y_root, f.zt + 0.05), (f.y1 - 4.0, f.zt + 0.05), (y_tip, z_tip + 1.5), (y_tip, z_tip)]
    else:
        y_root = f.y1 - FORK_ROOT
        prof = [(y_root, f.zb + 1.0), (y_root, f.zb + 8.0), (f.y1, f.zb + 8.0), (y_tip, z_tip + 1.5), (y_tip, z_tip)]
    lip = (f"lip {z_tip - floor:.1f} mm off the floor, tip {y_tip - yw - DISC_R:.0f} mm ahead of the disc")
    for side, sgn in (("l", 1), ("r", -1)):
        x0 = f.x1 if sgn > 0 else -f.x1 - t
        pid = f"fork_{side}"
        cuts = []
        items = [sh.side_prism(prof, x0, x0 + t)]
        if axle:
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
            plan.connect(pid, "chassis_top", "interlock", "Hook along the wedgelet's top edge lies on the roof: it keys "
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
