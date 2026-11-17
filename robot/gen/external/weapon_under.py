"""Undercutter: horizontal bar spinning UNDER the belly at the front, with a centre caster on the spin axis.

Spin axis vertical at (0, y_a). The 1806 outrunner stands bell-up on the floor inside the body (fully enclosed), its
stator bolted from the belly with 2 M2. Its own shaft is lengthened DOWN through the stator and the floor; the steel
bar is keyed on it under the belly, and the shaft end runs in one MR63 inside a nylon caster puck that rides on the
floor. Motor bearings + one coaxial extra bearing (kin.double_bearing), the bar held on both sides (motor above,
puck below). The puck does not spin, so the nose rests on the spin axis, never on the bar (ground.pitch_rest).
"""

from __future__ import annotations

import math

from ..intent import I
from . import fasteners, sh, spinner
from .weapon import module

BAR_R = 34.0
BAR_W = 9.0
BAR_T = 3.0
AXIS_BACK = 16.0
BELLY_CLEAR = 1.6  # bar top below the belly
PUCK_GAP = 1.3  # puck top below the bar
PUCK_R = 6.0
PUCK_BASE = 1.8  # puck floor under the bearing (1 mm relief under the shaft end + 0.8 mm floor)
PUCK_BRG = dict(stock="MR63ZZ", r_out=3.0, r_in=1.5, w=2.5)
FLOOR_CLEAR = PUCK_BASE + PUCK_BRG["w"] + PUCK_GAP  # bar underside above the floor
CAVITY_R = 11.2
PIN_R = 15.0
LOCK_T = 0.8
STATOR_SCREW = 5  # M2x5: 1.75 mm grip (floor + pad) + 3.25 mm into the stator's 3.5 mm tapped holes
SCREW_ENG = 3.25


def belly_z(floor_z):
    """Belly height the module needs (frame_params uses it)."""
    return floor_z + FLOOR_CLEAR + BAR_T + BELLY_CLEAR


@module("undercutter")
class Under:
    @staticmethod
    def geometry(plan):
        f = plan.frame
        ya = f.y1 - AXIS_BACK - f.max_inset()  # a sloped (cone) wall must not cut the motor pocket
        z_face = f.zb + STATOR_SCREW - SCREW_ENG  # countersunk heads flush with the belly; stator face on a pad over the floor: the M2x5 grip
        zc = z_face + spinner.MOTOR_L / 2
        z_bar1 = f.zb - BELLY_CLEAR
        return ya, zc, z_face, z_bar1

    @classmethod
    def prepare(cls, plan, h, g):
        plan.extra["weapon_motor"] = "weapon_motor"
        plan.robot_type = "horizontal_spinner"
        plan.archetype = "horizontal_spinner"
        plan.extra["wedge_len"] = 30.0
        plan.extra["battery_side_mm"] = 7.5
        ya, zc, z_face, _ = cls.geometry(plan)
        r = CAVITY_R + 0.2
        plan.keepouts.append(("wmotor", -r, r, ya - r, ya + r))
        plan.anchors["weapon_motor.phases"] = (0.0, ya - 9.0, z_face + 0.5)
        plan.extra.setdefault("approach", {})["weapon_motor.phases"] = (0.0, ya - r - 1.0)

    @classmethod
    def add(cls, plan, h, g):
        f = plan.frame
        ya, zc, z_face, z_bar1 = cls.geometry(plan)
        cav = I("protection", "the bell turns in a round cavity fully inside the shell; only the bar is outside",
                f"bell r {spinner.MOTOR_R} + clearance", threats=["hspin_floor", "debris"])
        plan.cut("bottom", sh.cyl_axis(CAVITY_R, z_face, f.zt + 1.0, "z", 0.0, ya), intent=cav)
        plan.cut("top", sh.cyl_axis(CAVITY_R, z_face, zc + spinner.MOTOR_L / 2 + 7.6, "z", 0.0, ya), intent=cav)
        plan.add("bottom", sh.cyl_axis(CAVITY_R - 0.2, f.zb, z_face, "z", 0.0, ya),
                 intent=I("load_path", "stator pad: floor thickened under the motor so its M2x5 screws get 1.75 mm grip",
                          "floor + pad = M2x5 grip", threats=["reaction_gyro", "hspin_floor"]))
        plan.late_cut("bottom", sh.cyl_axis(spinner.SHAFT_R + 1.0, f.zb - 0.5, z_face + 0.1, "z", 0.0, ya),
                      intent=I("assembly", "shaft passes down through the floor to the bar", "3 mm + 2 mm clearance", threats=["debris"]))
        plan.cut("bottom", sh.boxr(-1.5, 1.5, ya - CAVITY_R - 2.5, ya - 6.0, z_face - 0.5, z_face + 2.0),
                 intent=I("wiring", "phase leads leave the cavity rearward", "3 mm slot", threats=["debris"]))
        for k, ang in enumerate((90.0, 270.0)):  # along y: clear of the bar in its modelled pose (bar along x)
            a = math.radians(ang)
            x, y = 8.0 * math.cos(a), ya + 8.0 * math.sin(a)
            L = STATOR_SCREW
            cut, rec = fasteners.hole((x, y, f.zb), [0.0, 0.0, 1.0], f"M2x{L}", "countersunk", "tapped", L - SCREW_ENG)
            plan.late_cut("bottom", cut, intent=I("assembly", "counterbored clearance hole up through the floor for the stator "
                                                 "screw (robot.cad.holes)", "M2 clearance + head recess", threats=["flip_landing", "hazard_snag"]))
            plan.screw(id=f"bolt_wm{'ab'[k]}", designation=f"M2x{L}", at=list(rec.at), dir=[0.0, 0.0, 1.0], hole=rec.hole, head="countersunk",
                       through=["chassis_bottom"], threads_into="weapon_motor",
                       intent=I("load_path", "stator screws from the belly: weapon reaction torque into the floor",
                                "1806 stator r 8, 3.25 mm engagement", threats=["reaction_gyro"]))
        plan.connect("weapon_motor", "chassis_bottom", "screw", "Stator face bolted onto the floor with 2 M2 from the belly")
        plan.part(id="weapon_motor", kind="weapon_motor", catalog=spinner.MOTOR, at=[0.0, ya, zc], rot=[0.0, -90.0, 0.0],
                  rotates_with="fixed", motor_shaft_extended=True, ports={"phases": [-6.5, -9.0, 0.0]},
                  label="1806 outrunner standing bell-up inside the body; its shaft lengthened down to the bar",
                  intent=I("load_path", "direct drive: the bar is on the motor's own shaft", "1806 on 2S",
                           threats=["hspin_floor", "reaction_gyro"]))
        zm = z_bar1 - BAR_T / 2
        bar = sh.place(spinner.bar_shape(2 * BAR_R, BAR_W, BAR_T, spinner.SHAFT_R, [(PIN_R, 0.0, 1.6), (-PIN_R, 0.0, 1.6)]),
                       (0, 0, 0), (0, 0, 0))
        xm = zm - zc  # bar centre along the motor axis (motor local +x points up)
        plan.part(id="weapon", kind="weapon", material="steel", process="laser", shape=bar,
                  parent="weapon_motor", at=[xm, 0.0, 0.0], rot=[0.0, 90.0, 0.0], rotates_with="weapon",
                  joint={"kind": "revolute", "axis": [1, 0, 0], "pivot": [xm, 0.0, 0.0], "min": 0, "max": 360, "default": 0},
                  color="#d9dde2", organic=True,
                  weapon={"kind": "bar", "motor": "weapon_motor", "cells": 2, "reduction": 1.0, "spin_axis": [0, 0, 1],
                          "spin_dir": "ccw", "supported_both_ends": False, "teeth": 2},
                  label=f"{BAR_T:g} mm steel undercutter bar, {2 * BAR_R:g} mm tip to tip",
                  intent=I("load_path", "bar under the belly hits wheels and wedge lips low", f"{2 * BAR_R:g} x {BAR_W:g} x {BAR_T:g}",
                           threats=["hspin_floor", "vspin_side"]))
        zf = plan.extra.get("_floor_z", z_bar1 - BAR_T - FLOOR_CLEAR)
        pw = PUCK_BRG["w"]
        zp1 = z_bar1 - BAR_T - PUCK_GAP
        zbb = zf + PUCK_BASE
        puck = sh.S(sh.cyl_axis(PUCK_R, zf, zp1, "z", 0.0, ya), sh.cyl_axis(PUCK_BRG["r_out"], zbb, zp1 + 0.5, "z", 0.0, ya),
                    sh.cyl_axis(PUCK_BRG["r_out"] - 0.6, zbb - 1.0, zbb + 0.1, "z", 0.0, ya))  # relief: the outer race sits on a shoulder
        plan.part(id="caster", kind="caster", material="nylon", process="fdm", print_orientation="-z", shape=puck,
                  rotates_with="fixed", color="#2a2c30",
                  label="nylon caster puck on the spin axis: the nose rides on it, the bar spins above the floor",
                  intent=I("load_path", "front support on the spin axis: keeps the bar off the floor when the robot "
                           "pitches forward", f"r {PUCK_R}, {zp1 - zf:.1f} mm tall", threats=["hspin_floor"]))
        bs = sh.place(sh.S(sh.cyl_axis(PUCK_BRG["r_out"], -pw / 2, pw / 2, "z", 0, 0),
                           sh.cyl_axis(PUCK_BRG["r_in"], -pw / 2 - 1, pw / 2 + 1, "z", 0, 0)), (0.0, ya, zbb + pw / 2))
        plan.part(id="wbearing", kind="bearing", material="steel", process="cots", stock=PUCK_BRG["stock"],
                  designation=PUCK_BRG["stock"], rotates_with="fixed", color="#555555", shape=bs,
                  label="MR63ZZ in the caster puck: the shaft's lower support",
                  intent=I("load_path", "lower rotor support and caster pivot (the one coaxial extra bearing)", "MR63ZZ 3 x 6 x 2.5",
                           threats=["hspin_floor"]))
        plan.part(id="wshaft", kind="shaft", material="titanium", process="cots", stock="3 mm Ti-6Al-4V rod",
                  shaft_of="weapon_motor", rotates_with="weapon", color="#777777", parent="weapon",
                  shape=sh.cyl_axis(spinner.SHAFT_R, zbb + 0.2 - zm, zc - zm, "z", 0.0, 0.0),
                  label="motor rotor shaft replaced by a 3 mm Ti rod, lengthened down through floor and bar into the puck",
                  intent=I("load_path", "the bar sits between the motor bearings and the puck bearing", "3 mm Ti rod",
                           threats=["reaction_gyro", "hspin_floor"]))
        plan.connect("weapon", "wshaft", "press_fit", "Bar bore pressed on the shaft's D-flat, 2 M3 grub screws in the hub, circlip below",
                     interference_mm=0.05, mechanical_key=True)
        plan.connect("wshaft", "weapon_motor", "press_fit",
                     "The motor's own rotor shaft, lengthened, pressed in the bell and held by its circlip at the stator",
                     interference_mm=0.05, mechanical_key=True)
        plan.connect("wbearing", "caster", "press_fit", "MR63ZZ outer race pressed into the puck, on its base shoulder",
                     interference_mm=0.05, mechanical_key=True)
        plan.connect("wbearing", "wshaft", "shaft", "MR63ZZ inner race on the shaft end, circlip above: the puck stays still while the bar spins")
        plan.allow_overlap += [
            {"a": "weapon_motor", "b": "wshaft", "max_depth_mm": 1.6, "reason": "the motor's own shaft inside its stator bore (catalog motor drawn solid)"}]
        # weapon lock: pin up through the bar into a steel plate lying on the floor inside
        xl = PIN_R
        z0 = f.zb + f.floor - 0.4  # sunk 0.4 in a pocket in the floor's top: captive sideways
        plan.late_cut("bottom", sh.boxr(xl - 3.1, xl + 3.1, ya - 3.1, ya + 3.1, z0, z0 + 0.5),
                      intent=I("retention", "pocket for the lock plate: the pin's side load goes into the pocket walls",
                               "6 x 6 + 0.2, 0.4 deep", threats=["reaction_gyro"]))
        plan.late_cut("bottom", sh.cyl_axis(1.6, f.zb - 0.5, z0 + 0.1, "z", xl, ya),
                      intent=I("service", "lock pin passes up through the floor", "3 mm pin + 0.2", threats=["reaction_gyro"]))
        lp = sh.S(sh.boxr(xl - 3.0, xl + 3.0, ya - 3.0, ya + 3.0, z0, z0 + LOCK_T), sh.cyl_axis(1.6, z0 - 0.5, z0 + LOCK_T + 0.5, "z", xl, ya))
        plan.part(id="lock_plate", kind="plate", material="steel", process="laser", shape=lp, rotates_with="fixed",
                  color="#c9ccd1", label="0.8 mm steel lock plate bonded on the floor inside: the weapon pin's upper seat",
                  intent=I("service", "weapon lock: the pin through the bar seats in steel, not in the printed floor",
                           "3 mm pin, 0.8 mm steel", threats=["reaction_gyro"]))
        plan.connect("lock_plate", "chassis_bottom", "press_fit", "Pressed into a 0.4 mm pocket in the floor, over the pin hole; the motor pad and pocket walls hold it",
                     interference_mm=0.05, mechanical_key=True)
        plan.extra["weapon_lock"] = {"type": "removable_pin", "dia_mm": 3.0, "axis": [0, 0, 1],
                                     "at": [xl, round(ya, 3), round(zm, 3)], "holes": ["weapon", "lock_plate"],
                                     "note": "red 3 mm REMOVE-BEFORE-FIGHT pin up through the bar into the floor lock plate"}
