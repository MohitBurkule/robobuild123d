"""Horizontal bar spinner on a sunk hub motor (overhead bar, mounted on the top of the body near the front).

Spin axis vertical at (0, y_a). The 1806 outrunner stands bell-up in a printed column of the bottom half, its stator
bolted from the belly with 2 M2; the bell pokes through a hole in the roof and the laser-cut steel bar sits on the
bell face, keyed to the shaft boss. The motor's own shaft is lengthened down through the stator into a 683 bearing in
the column (motor bearings + one coaxial bearing). Lock pin: vertical, through the bar into the roof.
The bar stores < 20 J at 85 % speed so the one-sided support is legal (spinner.bearing only warns).
"""

from __future__ import annotations

import math

from . import sh, spinner
from .weapon import module

BAR_R = 38.0  # half length (tip radius)
BAR_W = 12.0
BAR_T = 3.0
AXIS_BACK = 13.0  # axis behind the chassis front
ROOF_CLEAR = 1.8  # bar underside above the roof
COLUMN_R = 11.0
CAVITY_R = 11.2  # bell clearance (can r 10.5)
PIN_R = 15.0
LOCK_T = 0.8  # 0.3 sunk in the roof recess


@module("hspin_bar")
class HSpin:
    @staticmethod
    def geometry(plan):
        f = plan.frame
        ya = f.y1 - AXIS_BACK
        z_bar0 = f.zt + ROOF_CLEAR  # bar underside
        zc = z_bar0 - spinner.MOTOR_L / 2 - 0.2  # motor centre (can top 0.2 under the bar)
        z_col = zc - spinner.MOTOR_L / 2  # stator face = column top
        return ya, zc, z_col, z_bar0

    @classmethod
    def prepare(cls, plan, h, g):
        plan.extra["weapon_motor"] = "weapon_motor"
        plan.robot_type = "horizontal_spinner"
        plan.extra["wedge_len"] = 30.0
        plan.extra["battery_side_mm"] = 7.5  # the long pack leaves a wire lane past it on both sides
        plan.archetype = "horizontal_spinner"
        ya, zc, z_col, _ = cls.geometry(plan)
        r = CAVITY_R + 0.2  # cavity (+ the pocket wall the solver adds)
        plan.keepouts.append(("wmotor", -r, r, ya - r, ya + r))
        W = plan.frame.x1
        for side, sgn in (("r", 1), ("l", -1)):
            xw = sgn * W
        # phase leads leave the cavity rearward through a slot in the column top
        plan.anchors["weapon_motor.phases"] = (0.0, ya - 9.0, z_col + 0.5)
        plan.extra.setdefault("approach", {})["weapon_motor.phases"] = (0.0, ya - r - 1.0)

    @classmethod
    def add(cls, plan, h, g):
        f = plan.frame
        ya, zc, z_col, z_bar0 = cls.geometry(plan)
        zb = f.zb
        # column in the bottom half, cavity for the bell through both halves (roof hole)
        plan.add("bottom", sh.cyl_axis(COLUMN_R, zb, z_col, "z", 0.0, ya))
        plan.cut("bottom", sh.cyl_axis(CAVITY_R, z_col, 1.0, "z", 0.0, ya))
        plan.cut("top", sh.cyl_axis(CAVITY_R, -1.0, f.zt + 1.0, "z", 0.0, ya))
        # wire slot from the cavity back into the channel band
        plan.cut("bottom", sh.boxr(-1.5, 1.5, ya - COLUMN_R - 2.5, ya - 6.0, z_col - 0.5, 0.5))
        # stator screws from the belly (M2 into the stator's tapped holes)
        for k, ang in enumerate((90.0, 270.0)):
            a = math.radians(ang)
            x, y = 8.0 * math.cos(a), ya + 8.0 * math.sin(a)
            plan.late_cuts["bottom"].append(sh.cyl_axis(1.1, zb - 0.5, z_col + 0.1, "z", x, y))
            seat = z_col + 3.25 - 8.0  # M2x8 engages 3.25 mm of the stator's 3.5 mm tapped depth
            plan.late_cuts["bottom"].append(sh.cyl_axis(2.1, zb - 0.5, seat, "z", x, y))  # counterbore
            plan.screw(id=f"bolt_wm{'ab'[k]}", designation="M2x8", at=[x, y, seat], dir=[0.0, 0.0, 1.0],
                       through=["chassis_bottom"], threads_into="weapon_motor")
        plan.connect("weapon_motor", "chassis_bottom", "screw", "Stator face bolted onto the motor column with 2 M2 from the belly")
        plan.part(id="weapon_motor", kind="weapon_motor", catalog=spinner.MOTOR, at=[0.0, ya, zc], rot=[0.0, -90.0, 0.0],
                  rotates_with="fixed", motor_shaft_extended=True, ports={"phases": [-6.5, -9.0, 0.0]},
                  label="1806 outrunner = weapon hub, bell up through the roof; own shaft lengthened up into a 683 in the bridge")
        # bar: local XY plane, axis local z; in the motor frame (local x = world z) with rot [0, 90, 0]
        # lock pin hole and its balancing twin; the 3 mm bore is reamed after cutting (hub drawn solid)
        bar = spinner.bar_shape(2 * BAR_R, BAR_W, BAR_T, 0.0, [(PIN_R, 0.0, 1.6), (-PIN_R, 0.0, 1.6)])
        # rotate the bar so it points along world y: bar_shape is along local x, which maps to world +x; turn 90 about z
        bar = sh.place(bar, (0, 0, 0), (0, 0, 90))
        xm = z_bar0 + BAR_T / 2 - zc  # bar centre along the motor axis
        plan.part(id="weapon", kind="weapon", material="steel", process="laser", shape=bar,
                  parent="weapon_motor", at=[xm, 0.0, 0.0], rot=[0.0, 90.0, 0.0], rotates_with="weapon",
                  joint={"kind": "revolute", "axis": [1, 0, 0], "pivot": [xm, 0.0, 0.0], "min": 0, "max": 360, "default": 0},
                  color="#d9dde2", organic=True,
                  weapon={"kind": "bar", "motor": "weapon_motor", "cells": 2, "reduction": 1.0, "spin_axis": [0, 0, 1],
                          "spin_dir": "ccw", "supported_both_ends": False, "teeth": 2},
                  label=f"{BAR_T:g} mm steel bar, {2 * BAR_R:g} mm tip to tip, laser cut, swept tips")
        # shaft in the bar frame (local z = world z, origin at the bar centre)
        zo = z_bar0 + BAR_T / 2
        z_boss = zc + spinner.MOTOR_L / 2 + 7.0  # top of the bell's shaft boss
        zbb = z_boss + 1.0  # bridge underside
        z_top_shaft = zbb + spinner.BEARING["w"]
        add_bridge(plan, ya, zbb)
        plan.part(id="wshaft", kind="shaft", material="titanium", process="cots", stock="3 mm Ti-6Al-4V rod",
                  shaft_of="weapon_motor", rotates_with="weapon", color="#777777", parent="weapon",
                  shape=sh.cyl_axis(spinner.SHAFT_R, zc - zo, z_top_shaft - zo, "z", 0.0, 0.0),
                  label="motor rotor shaft replaced by a 3 mm Ti rod, lengthened down into the 683 (circlip at the stator)")
        spinner.rotor_connections(plan, "weapon", "weapon_motor", "wshaft", "wbearing", "top_bridge", hub_depth=2.6)
        # lock pin: through the bar's pin hole into a steel lock plate bonded on the roof under the bar
        yl = ya - PIN_R
        plan.late_cuts["top"].append(sh.boxr(-3.2, 3.2, yl - 3.2, yl + 3.2, f.zt - 0.3, f.zt + 0.1))  # recess
        lp = sh.S(sh.boxr(-3.0, 3.0, yl - 3.0, yl + 3.0, f.zt - 0.3, f.zt - 0.3 + LOCK_T), sh.cyl_axis(1.6, f.zt - 0.5, f.zt + LOCK_T + 0.5, "z", 0.0, yl))
        plan.part(id="lock_plate", kind="plate", material="steel", process="laser", shape=lp, rotates_with="fixed",
                  color="#c9ccd1", label="0.8 mm steel lock plate bonded to the roof: the weapon pin's lower seat")
        plan.connect("lock_plate", "chassis_top", "glue", "Epoxied into a 0.3 mm recess in the roof (the recess takes the pin's side load)",
                     mechanical_key=True)
        plan.extra["weapon_lock"] = {"type": "removable_pin", "dia_mm": 3.0, "axis": [0, 0, 1],
                                     "at": [0.0, round(yl, 3), round(z_bar0, 3)],
                                     "holes": ["weapon", "lock_plate"],
                                     "note": "red 3 mm REMOVE-BEFORE-FIGHT pin through the bar into the lock plate"}


BRIDGE_T, BRIDGE_W, POST_T = 5.0, 8.0, 6.0
BRIDGE_ZS = (3.0, 7.0)  # post screws, both into the top half (clear of the electronics on the floor)


def add_bridge(plan, ya, zbb):
    """Printed bridge over the bar: a beam carrying the top 683 on the spin axis, on two posts outside the bar's
    circle, each screwed to a side wall with 2 M2 into inserts (one per clamshell half)."""
    f = plan.frame
    W = f.x1
    xo = W + 0.02 + POST_T
    y0, y1 = ya - BRIDGE_W / 2, ya + BRIDGE_W / 2
    zt = zbb + BRIDGE_T
    beam = sh.U(sh.boxr(-xo, xo, y0, y1, zbb, zt), sh.cyl_axis(6.0, zbb, zt, "z", 0.0, ya))  # round boss round the bearing
    posts = [sh.boxr(W + 0.02, xo, y0, y1, BRIDGE_ZS[0] - 3.5, zt), sh.boxr(-xo, -W - 0.02, y0, y1, BRIDGE_ZS[0] - 3.5, zt)]
    bw = spinner.BEARING["w"]
    cuts = [sh.cyl_axis(spinner.BEARING["r_out"], zbb - 0.5, zbb + bw, "z", 0.0, ya),
            sh.cyl_axis(spinner.SHAFT_R + 1.2, zbb + bw - 0.1, zt + 0.5, "z", 0.0, ya)]
    for side, sgn in (("r", 1), ("l", -1)):
        xw = sgn * W
        for k, z in enumerate(BRIDGE_ZS):
            half = "bottom" if z < 0 else "top"
            cuts.append(sh.cyl_axis(1.1, W - 0.5, xo + 0.5, "x", ya, z) if sgn > 0 else sh.cyl_axis(1.1, -xo - 0.5, -W + 0.5, "x", ya, z))
            boss = sh.cyl_axis(3.0, xw - sgn * 6.0, xw, "x", ya, z) if sgn > 0 else sh.cyl_axis(3.0, xw, xw + 6.0, "x", ya, z)
            plan.add(half, boss)
            bore = (xw - sgn * 4.6, xw + sgn * 0.2)
            plan.late_cuts[half].append(sh.cyl_axis(1.6, min(bore), max(bore), "x", ya, z))
            iid = f"insert_b{side}{k}"
            plan.part(id=iid, kind="insert", catalog="heatset_m2", at=[xw - sgn * 1.7, ya, z], rot=[0.0, 90.0, 0.0],
                      retained="press_fit")
            plan.screw(id=f"bolt_b{side}{k}", designation="M2x10", at=[sgn * xo, ya, z], dir=[-sgn, 0.0, 0.0],
                       through=["top_bridge"], threads_into=iid)
    plan.part(id="top_bridge", kind="structure", material="nylon", process="fdm", print_orientation="-z",
              shape=sh.S(sh.U(beam, *posts), *cuts), rotates_with="fixed", color="#2a2c30", solid_fraction=0.9,
              label="printed bridge over the bar: top bearing on the spin axis, posts screwed to both side walls")
    plan.part(id="wbearing", kind="bearing", material="steel", process="cots", stock=spinner.BEARING["stock"],
              rotates_with="fixed", color="#555555", shape=spinner.bearing_shape((0.0, ya, zbb + bw / 2), "z"),
              label="F683ZZ in the bridge: the rotor's top support")
