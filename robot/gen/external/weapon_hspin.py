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
PIN_R = 14.0


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
        plan.archetype = "horizontal_spinner"
        ya, zc, z_col, _ = cls.geometry(plan)
        r = COLUMN_R + 0.5
        plan.keepouts.append(("wmotor", -r, r, ya - r, ya + r))
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
        # bearing seat (dropped in from above, shoulder under it) + shaft clearance
        bw = spinner.BEARING["w"]
        zbr = z_col - bw  # bearing bottom
        plan.late_cuts["bottom"].append(sh.cyl_axis(spinner.BEARING["r_out"], zbr, z_col + 0.1, "z", 0.0, ya))
        plan.part(id="wbearing", kind="bearing", material="steel", process="cots", stock=spinner.BEARING["stock"],
                  rotates_with="fixed", color="#555555", shape=spinner.bearing_shape((0.0, ya, zbr + bw / 2), "z"),
                  label="F683ZZ 3x7x3 flanged bearing in the motor column")
        # stator screws from the belly (M2 into the stator's tapped holes)
        for k, ang in enumerate((90.0, 270.0)):
            a = math.radians(ang)
            x, y = 8.0 * math.cos(a), ya + 8.0 * math.sin(a)
            plan.late_cuts["bottom"].append(sh.cyl_axis(1.1, zb - 0.5, z_col + 0.1, "z", x, y))
            plan.late_cuts["bottom"].append(sh.cyl_axis(2.1, zb - 0.5, zb + 1.6, "z", x, y))  # counterbore
            plan.screw(id=f"bolt_wm{'ab'[k]}", designation="M2x6", at=[x, y, zb + 1.5], dir=[0.0, 0.0, 1.0],
                       through=["chassis_bottom"], threads_into="weapon_motor")
        plan.connect("weapon_motor", "chassis_bottom", "screw", "Stator face bolted onto the motor column with 2 M2 from the belly")
        plan.part(id="weapon_motor", kind="weapon_motor", catalog=spinner.MOTOR, at=[0.0, ya, zc], rot=[0.0, -90.0, 0.0],
                  rotates_with="fixed", motor_shaft_extended=True, ports={"phases": [-6.5, -9.0, 0.0]},
                  label="1806 outrunner = weapon hub, bell up through the roof; own shaft lengthened into a 683 in the column")
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
        plan.part(id="wshaft", kind="shaft", material="titanium", process="cots", stock="3 mm Ti-6Al-4V rod",
                  shaft_of="weapon_motor", rotates_with="weapon", color="#777777", parent="weapon",
                  shape=sh.cyl_axis(spinner.SHAFT_R, zbr + 0.5 - zo, BAR_T / 2, "z", 0.0, 0.0),
                  label="motor rotor shaft replaced by a 3 mm Ti rod, lengthened down into the 683 (circlip at the stator)")
        spinner.rotor_connections(plan, "weapon", "weapon_motor", "wshaft", "wbearing", "chassis_bottom", hub_depth=2.6)
        # lock pin: through the bar's pin hole down into a blind hole in the roof
        plan.late_cuts["top"].append(sh.cyl_axis(1.6, f.zt - f.floor - 3.0, f.zt + 0.5, "z", 0.0, ya - PIN_R))
        plan.extra["weapon_lock"] = {"type": "removable_pin", "dia_mm": 3.0, "axis": [0, 0, 1],
                                     "at": [0.0, round(ya - PIN_R, 3), round(z_bar0, 3)],
                                     "holes": ["weapon", "chassis_top"],
                                     "note": "red 3 mm REMOVE-BEFORE-FIGHT pin through the bar into the roof"}
