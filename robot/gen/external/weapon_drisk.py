"""Vertical drisk / disc on a hub motor between two printed uprights at the front (Revron-like layout, generic sizes).

Spin axis along x at (y_w, z_w) ahead of the chassis front; uprights stand on the roof (feet bolted down into inserts),
motor stator bolted to the right upright, 683 bearing in the left, lock pin through both uprights and the disc.
Forks: two laser-cut steel tines bolted to the chassis side walls, tips 0.6 mm off the floor, leading the disc.
"""

from __future__ import annotations

import math

from shapely.geometry import MultiPoint, Polygon

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
        for side, sgn, yy, z in fork_sites(plan):
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
            plan.add("bottom", sh.cyl_axis(3.0, f.y1 - 6.0, f.y1, "y", xc, z_front))
            plan.late_cuts["bottom"].append(sh.cyl_axis(1.6, f.y1 - 4.6, f.y1 + 0.2, "y", xc, z_front))
            plan.part(id=f"insert_{side}0", kind="insert", catalog="heatset_m2", at=[xc, f.y1 - 1.7, z_front],
                      rot=[90.0, 0.0, 0.0], retained="press_fit")
            plan.screw(id=f"bolt_{side}0", designation="M2x10", at=[xc, f.y1 + FOOT_LEN, z_front], dir=[0.0, -1.0, 0.0],
                       through=[label], threads_into=f"insert_{side}0")
            # upper front screw into an insert in the top half's front wall
            z_up = Z_UPPER
            cuts.append(sh.cyl_axis(1.1, f.y1 - 0.5, f.y1 + FOOT_LEN + 0.5, "y", xc, z_up))
            plan.add("top", sh.cyl_axis(3.0, f.y1 - 6.0, f.y1, "y", xc, z_up))
            plan.late_cuts["top"].append(sh.cyl_axis(1.6, f.y1 - 4.6, f.y1 + 0.2, "y", xc, z_up))
            plan.part(id=f"insert_{side}1", kind="insert", catalog="heatset_m2", at=[xc, f.y1 - 1.7, z_up],
                      rot=[90.0, 0.0, 0.0], retained="press_fit")
            plan.screw(id=f"bolt_{side}1", designation="M2x10", at=[xc, f.y1 + FOOT_LEN, z_up], dir=[0.0, -1.0, 0.0],
                       through=[label], threads_into=f"insert_{side}1")
            plan.connect(label, "chassis_top", "interlock",
                         "Hook tab on the foot's top lies on the roof behind the front wall (takes the peel); "
                         "2 M2 along -y into front-wall inserts", mechanical_key=True)
            if side == "upr":
                for k, (dy, dz) in enumerate(STATOR_SCREWS):
                    cuts.append(sh.cyl_axis(1.1, x0 - 1, x1 + 1, "x", yw + dy, zw + dz))
                    plan.screw(id=f"bolt_wm{'ab'[k]}", designation="M2x8", at=[x0, yw + dy, zw + dz],
                               dir=[1.0, 0.0, 0.0], through=[label], threads_into="weapon_motor")
            else:
                cuts.append(sh.cyl_axis(spinner.BEARING["r_out"], x0 - 0.1, x0 + spinner.BEARING["w"], "x", yw, zw))
                cuts.append(sh.cyl_axis(2.6, x0 + spinner.BEARING["w"] - 0.1, x1 + 0.5, "x", yw, zw))
            shape = sh.S(sh.side_prism(prof, x0, x1), *cuts)
            plan.part(id=label, kind="structure", material="nylon", process="fdm", shape=shape, print_orientation="+x",
                      rotates_with="fixed", color="#2a2c30", solid_fraction=0.9,
                      label=f"{spinner.PLATE_T:g} mm printed weapon upright (spin axis = build direction), foot screwed down onto the roof")
        plan.connect("weapon_motor", "upright_r", "screw", "Stator face bolted to the right upright with 2 M2 along the motor axis")
        # motor, disc, shaft, bearing
        plan.part(id="weapon_motor", kind="weapon_motor", catalog=spinner.MOTOR, at=[xm, yw, zw], rot=[0.0, 0.0, 0.0],
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
                  weapon={"kind": "disc", "motor": "weapon_motor", "cells": 2, "reduction": 1.0, "spin_axis": [0, 0, 1],
                          "spin_dir": "ccw", "supported_both_ends": True, "teeth": 2},
                  label=f"{DISC_T:g} mm steel disc, {2 * DISC_R:g} mm, 2 hooked teeth in the outline, laser cut")
        x_b0 = xs["upl"][0]
        # shaft in the disc frame: the disc's local z is world +x (rot [0, 90, 0]), origin at world x = 0
        plan.part(id="wshaft", kind="shaft", material="titanium", process="cots", stock="3 mm Ti-6Al-4V rod",
                  shaft_of="weapon_motor", rotates_with="weapon", color="#777777", parent="weapon",
                  shape=sh.cyl_axis(spinner.SHAFT_R, xm, x_b0 + spinner.BEARING["w"], "z", 0.0, 0.0),
                  label="motor rotor shaft replaced by a 3 mm Ti rod, lengthened into the 683 (circlip at the stator)")
        plan.part(id="wbearing", kind="bearing", material="steel", process="cots", stock=spinner.BEARING["stock"],
                  rotates_with="fixed", color="#555555",
                  shape=spinner.bearing_shape((x_b0 + spinner.BEARING["w"] / 2, yw, zw), "x"),
                  label="F683ZZ 3x7x3 flanged bearing in the left upright")
        spinner.rotor_connections(plan, "weapon", "weapon_motor", "wshaft", "wbearing", "upright_l")
        plan.extra["weapon_lock"] = {"type": "removable_pin", "dia_mm": 3.0, "axis": [1, 0, 0],
                                     "at": [0.0, round(pin[0], 3), round(pin[1], 3)],
                                     "holes": ["upright_r", "weapon", "upright_l"],
                                     "note": "red 3 mm REMOVE-BEFORE-FIGHT pin through both uprights and the disc"}
        # phase wires leave through the front wall
        plan.cut("bottom", sh.boxr(xm - 1.5, xm + 1.5, f.y1 - 3.0, f.y1 + 0.5, -5.0, 0.5))
        add_forks(plan, yw)


def fork_sites(plan):
    f = plan.frame
    y_root = f.y1 - FORK_ROOT
    return [(side, sgn, yy, f.zb + 4.5) for side, sgn in (("l", 1), ("r", -1)) for yy in (y_root + 4.0, f.y1 - 4.0)]


def add_forks(plan, yw):
    """Two side tines (laser-cut steel, profile in y-z) bolted to the side walls, tips leading the disc by 6 mm."""
    f = plan.frame
    floor = plan.extra["_floor_z"]
    y_tip = yw + DISC_R + 6.0
    y_root = f.y1 - FORK_ROOT
    z_tip = floor + 0.6
    prof = [(y_root, f.zb + 1.0), (y_root, f.zb + 8.0), (f.y1, f.zb + 8.0), (y_tip, z_tip + 1.5), (y_tip, z_tip)]
    for side, sgn in (("l", 1), ("r", -1)):
        x0 = f.x1 if sgn > 0 else -f.x1 - FORK_T
        pid = f"fork_{side}"
        cuts = []
        for k, (_, _, yy, z) in enumerate([q for q in fork_sites(plan) if q[0] == side]):
            cuts.append(sh.cyl_axis(1.1, x0 - 1, x0 + FORK_T + 1, "x", yy, z))
            xw = sgn * f.x1
            plan.add("bottom", sh.cyl_axis(3.0, xw - sgn * 8.0, xw, "x", yy, z) if sgn > 0 else
                     sh.cyl_axis(3.0, xw, xw + 8.0, "x", yy, z))
            bore = (xw - sgn * 3.6, xw + sgn * 0.2)
            plan.late_cuts["bottom"].append(sh.cyl_axis(1.6, min(bore), max(bore), "x", yy, z))
            plan.part(id=f"insert_f{side}{k}", kind="insert", catalog="heatset_m2", at=[xw - sgn * 1.7, yy, z],
                      rot=[0.0, 90.0, 0.0], retained="press_fit")
            plan.screw(id=f"bolt_f{side}{k}", designation="M2x5", at=[xw + sgn * FORK_T, yy, z], dir=[-sgn, 0.0, 0.0],
                       through=[pid], threads_into=f"insert_f{side}{k}")
        shape = sh.S(sh.side_prism(prof, x0, x0 + FORK_T), *cuts)
        plan.part(id=pid, kind="fork", material=FORK_MAT, process="laser", shape=shape, color="#c9ccd1",
                  label=f"{FORK_T:g} mm Ti fork tine, laser cut, bolted to the side wall")
