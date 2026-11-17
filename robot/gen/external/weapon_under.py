"""Undercutter: horizontal bar spinning UNDER the belly at the front, with a centre caster on the spin axis.

Spin axis vertical at (0, y_a). The 1806 outrunner hangs bell-down from a printed column in the top half, stator
bolted from the roof with 2 M2; the bell pokes through a hole in the floor and the steel bar sits on the bell face.
The motor shaft is lengthened both ways: up through the stator into a 683 in the column, and down through the bar
into a second 683 inside a nylon caster puck that rides on the floor. The puck does not spin (its bearing
decouples it), so the nose rests on the spin axis, never on the bar (ground.pitch_rest).
"""

from __future__ import annotations

import math

from ..intent import I
from . import fasteners, sh, spinner
from .weapon import module

BAR_R = 38.0
BAR_W = 9.0
BAR_T = 3.0
AXIS_BACK = 16.0
BELLY_CLEAR = 1.6  # bar top below the belly
FLOOR_CLEAR = 5.0  # bar underside above the floor: the bell's 7 mm shaft boss pokes 4 mm below the bar into the puck
COLUMN_R = 11.0
CAVITY_R = 11.2
PIN_R = 15.0
PUCK_R = 6.0
BOSS_R, BOSS_L = 2.5, 7.0  # catalogue 1806 shaft boss beyond the bell
PUCK_BRG = dict(stock="MR85ZZ", r_out=4.0, r_in=2.5, w=2.5)  # rides on the boss
LOCK_T = 0.8


def belly_z(floor_z):
    """Belly height the module needs (frame_params uses it)."""
    return floor_z + FLOOR_CLEAR + BAR_T + BELLY_CLEAR


@module("undercutter")
class Under:
    @staticmethod
    def geometry(plan):
        f = plan.frame
        ya = f.y1 - AXIS_BACK
        z_bar1 = f.zb - BELLY_CLEAR  # bar top
        zc = z_bar1 + spinner.MOTOR_L / 2 + 0.2  # motor centre: can bottom 0.2 over the bar
        z_col = zc + spinner.MOTOR_L / 2  # stator face = column underside
        return ya, zc, z_col, z_bar1

    @classmethod
    def prepare(cls, plan, h, g):
        plan.extra["weapon_motor"] = "weapon_motor"
        plan.robot_type = "horizontal_spinner"
        plan.archetype = "horizontal_spinner"
        plan.extra["wedge_len"] = 30.0
        plan.extra["battery_side_mm"] = 7.5
        ya, zc, z_col, _ = cls.geometry(plan)
        r = CAVITY_R + 0.2
        plan.keepouts.append(("wmotor", -r, r, ya - r, ya + r))
        plan.anchors["weapon_motor.phases"] = (0.0, ya - 9.0, z_col - 0.5)
        plan.extra.setdefault("approach", {})["weapon_motor.phases"] = (0.0, ya - r - 1.0)

    @classmethod
    def add(cls, plan, h, g):
        f = plan.frame
        ya, zc, z_col, z_bar1 = cls.geometry(plan)
        zt = f.zt
        bw = spinner.BEARING["w"]
        # column hanging from the roof; cavity for the bell through the floor
        plan.add("top", sh.cyl_axis(COLUMN_R, z_col, zt, "z", 0.0, ya),
                 intent=I("load_path", "motor column: the stator hangs from a solid printed column under the roof, so a "
                          "bar hit goes into the roof and both side walls", f"r {COLUMN_R}", threats=["hspin_floor", "reaction_gyro"]))
        cav = I("protection", "the bell turns in a round cavity; only the bar is exposed under the belly",
                f"bell r {spinner.MOTOR_R} + clearance", threats=["hspin_floor", "debris"])
        plan.cut("bottom", sh.cyl_axis(CAVITY_R, f.zb - 1.0, z_col, "z", 0.0, ya), intent=cav)
        plan.cut("top", sh.cyl_axis(CAVITY_R, f.zb - 1.0, z_col, "z", 0.0, ya), intent=cav)
        # top bearing seat in the column above the stator
        zb0 = z_col + 1.0
        plan.late_cut("top", sh.cyl_axis(spinner.BEARING["r_out"], zb0, zb0 + bw, "z", 0.0, ya),
                      intent=I("load_path", "683 seat: the rotor's top support", "683ZZ, press fit", threats=["reaction_gyro"]))
        plan.late_cut("top", sh.cyl_axis(spinner.SHAFT_R + 1.2, z_col - 0.5, zb0 + bw + 1.0, "z", 0.0, ya),
                      intent=I("assembly", "shaft clearance between stator and bearing", "3 mm + 2.4", threats=["debris"]))
        plan.cut("top", sh.boxr(-1.5, 1.5, ya - COLUMN_R - 2.5, ya - 6.0, z_col - 0.5, z_col + 2.0),
                 intent=I("wiring", "phase leads leave the cavity rearward", "3 mm slot", threats=["debris"]))
        for k, ang in enumerate((90.0, 270.0)):
            a = math.radians(ang)
            x, y = 8.0 * math.cos(a), ya + 8.0 * math.sin(a)
            grip = 8.0 - 3.25  # M2x8 with 3.25 mm in the stator's tapped holes
            cb = zt - (z_col + grip)  # head sunk so the screw reaches
            cut, rec = fasteners.hole((x, y, zt), [0.0, 0.0, -1.0], "M2x8", "socket", "tapped", grip,
                                      cbore=cb if cb > 0.3 else None)
            plan.late_cut("top", cut, intent=I("assembly", "counterbored clearance hole down the column for the stator screw "
                                              "(robot.cad.holes)", "M2 clearance + head recess", threats=["flip_landing", "hazard_snag"]))
            plan.screw(id=f"bolt_wm{'ab'[k]}", designation="M2x8", at=list(rec.at), dir=[0.0, 0.0, -1.0], hole=rec.hole,
                       through=["chassis_top"], threads_into="weapon_motor",
                       intent=I("load_path", "stator screws from the roof: weapon reaction torque into the column",
                                "1806 stator r 8, M2x8", threats=["reaction_gyro"]))
        plan.connect("weapon_motor", "chassis_top", "screw", "Stator face bolted under the motor column with 2 M2 from the roof")
        plan.part(id="weapon_motor", kind="weapon_motor", catalog=spinner.MOTOR, at=[0.0, ya, zc], rot=[0.0, 90.0, 0.0],
                  rotates_with="fixed", motor_shaft_extended=True, ports={"phases": [-6.5, -9.0, 0.0]},
                  label="1806 outrunner hung bell-down: the undercutter's hub",
                  intent=I("load_path", "the outrunner is the bar's hub", "1806 on 2S", threats=["hspin_floor", "reaction_gyro"]))
        zm = z_bar1 - BAR_T / 2
        xm = zc - zm  # bar centre along the motor axis (motor local +x points down)
        bar = sh.place(spinner.bar_shape(2 * BAR_R, BAR_W, BAR_T, 0.0, [(PIN_R, 0.0, 1.6), (-PIN_R, 0.0, 1.6)]),
                       (0, 0, 0), (0, 0, 90))
        plan.part(id="weapon", kind="weapon", material="steel", process="laser", shape=bar,
                  parent="weapon_motor", at=[xm, 0.0, 0.0], rot=[0.0, -90.0, 0.0], rotates_with="weapon",
                  joint={"kind": "revolute", "axis": [1, 0, 0], "pivot": [xm, 0.0, 0.0], "min": 0, "max": 360, "default": 0},
                  color="#d9dde2", organic=True,
                  weapon={"kind": "bar", "motor": "weapon_motor", "cells": 2, "reduction": 1.0, "spin_axis": [0, 0, 1],
                          "spin_dir": "ccw", "supported_both_ends": True, "teeth": 2},
                  label=f"{BAR_T:g} mm steel undercutter bar, {2 * BAR_R:g} mm tip to tip",
                  intent=I("load_path", "bar under the belly hits wheels and wedge lips low", f"{2 * BAR_R:g} x {BAR_W:g} x {BAR_T:g}",
                           threats=["hspin_floor", "vspin_side"]))
        # caster puck under the bar, its MR85 on the bell's shaft boss (the boss pokes BOSS_L - BAR_T below the bar)
        zf = plan.extra.get("_floor_z", z_bar1 - BAR_T - FLOOR_CLEAR)
        z_boss = zc - spinner.MOTOR_L / 2 - BOSS_L  # boss end
        zp1 = z_bar1 - BAR_T - 1.0  # 1 mm under the bar: the puck never touches the rotor
        pw = PUCK_BRG["w"]
        zbb = zp1 - pw  # bearing seated against the puck top: inner race on the boss
        puck = sh.S(sh.cyl_axis(PUCK_R, zf, zp1, "z", 0.0, ya),
                    sh.cyl_axis(PUCK_BRG["r_out"], zbb, zp1 + 0.5, "z", 0.0, ya),
                    sh.cyl_axis(BOSS_R + 0.4, z_boss - 0.4, zbb + 0.1, "z", 0.0, ya))
        plan.part(id="caster", kind="caster", material="nylon", process="fdm", print_orientation="-z", shape=puck,
                  rotates_with="fixed", color="#2a2c30",
                  label="nylon caster puck on the spin axis: the nose rides on it, the bar spins above the floor",
                  intent=I("load_path", "front support on the spin axis: keeps the bar off the floor when the robot "
                           "pitches forward", f"r {PUCK_R}, {FLOOR_CLEAR - 0.3:.1f} mm tall", threats=["hspin_floor"]))
        bs = sh.place(sh.S(sh.cyl_axis(PUCK_BRG["r_out"], -pw / 2, pw / 2, "z", 0, 0),
                           sh.cyl_axis(PUCK_BRG["r_in"], -pw / 2 - 1, pw / 2 + 1, "z", 0, 0)), (0.0, ya, zbb + pw / 2))
        plan.part(id="wbearing2", kind="bearing", material="steel", process="cots", stock=PUCK_BRG["stock"],
                  designation=PUCK_BRG["stock"], rotates_with="fixed", color="#555555", shape=bs,
                  label="MR85ZZ in the caster puck, on the bell's shaft boss",
                  intent=I("load_path", "lower rotor support and caster pivot", "MR85ZZ 5 x 8 x 2.5", threats=["hspin_floor"]))
        plan.part(id="wbearing", kind="bearing", material="steel", process="cots", stock=spinner.BEARING["stock"],
                  rotates_with="fixed", color="#555555", shape=spinner.bearing_shape((0.0, ya, zb0 + bw / 2), "z"),
                  label="F683ZZ in the motor column", intent=I("load_path", "upper rotor support", "683ZZ", threats=["reaction_gyro"]))
        plan.part(id="wshaft", kind="shaft", material="titanium", process="cots", stock="3 mm Ti-6Al-4V rod",
                  shaft_of="weapon_motor", rotates_with="weapon", color="#777777", parent="weapon",
                  shape=sh.cyl_axis(spinner.SHAFT_R, -BAR_T / 2, zb0 + bw - 0.5 - zm, "z", 0.0, 0.0),
                  label="motor shaft lengthened up through the stator into the column 683",
                  intent=I("load_path", "both-ends support", "3 mm Ti rod", threats=["reaction_gyro", "hspin_floor"]))
        spinner.rotor_connections(plan, "weapon", "weapon_motor", "wshaft", "wbearing", "chassis_top", hub_depth=2.6)
        plan.connect("wbearing2", "caster", "press_fit", "MR85ZZ outer race pressed into the puck, against its top shoulder",
                     interference_mm=0.05, mechanical_key=True)
        plan.connect("wbearing2", "weapon_motor", "shaft", "MR85ZZ inner race on the bell's 5 mm shaft boss, circlip below: the puck stays still while the bar spins")
        yl = ya - PIN_R
        z0 = f.zb - (LOCK_T - 0.3)  # plate proud of the belly by 0.5, sunk 0.3 in a recess
        plan.late_cut("bottom", sh.boxr(-3.2, 3.2, yl - 3.2, yl + 3.2, f.zb - 0.1, f.zb + 0.3),
                      intent=I("retention", "recess for the lock plate: takes the pin's side load as bearing, not peel",
                               "plate 6 x 6 + 0.2, 0.3 deep", threats=["reaction_gyro"]))
        plan.late_cut("bottom", sh.cyl_axis(1.6, f.zb - 0.5, f.zb + f.floor + 0.5, "z", 0.0, yl),
                      intent=I("service", "lock pin passes up through the floor", "3 mm pin + 0.2", threats=["reaction_gyro"]))
        lp = sh.S(sh.boxr(-3.0, 3.0, yl - 3.0, yl + 3.0, z0, z0 + LOCK_T), sh.cyl_axis(1.6, z0 - 0.5, z0 + LOCK_T + 0.5, "z", 0.0, yl))
        plan.part(id="lock_plate", kind="plate", material="steel", process="laser", shape=lp, rotates_with="fixed",
                  color="#c9ccd1", label="0.8 mm steel lock plate bonded under the belly: the weapon pin's upper seat",
                  intent=I("service", "weapon lock: the pin through the bar seats in steel, not in the printed floor",
                           "3 mm pin, 0.8 mm steel", threats=["reaction_gyro"]))
        plan.connect("lock_plate", "chassis_bottom", "glue", "Epoxied into a 0.3 mm recess in the belly (the recess takes the pin's side load)",
                     mechanical_key=True)
        plan.extra["weapon_lock"] = {"type": "removable_pin", "dia_mm": 3.0, "axis": [0, 0, 1],
                                     "at": [0.0, round(yl, 3), round(zm, 3)], "holes": ["weapon", "lock_plate"],
                                     "note": "red 3 mm REMOVE-BEFORE-FIGHT pin up through the bar into the belly lock plate"}
