"""Generate robots/unstoppable_force/spec.json from named numbers (photo-matched drum robot)."""
import json, sys, math, os
E = lambda k, d: float(os.environ.get(k, d))
from pathlib import Path

OUT = Path("/tmp/work10_unstoppable_force/robots/unstoppable_force/spec.json")
old = json.loads(OUT.read_text())

# ---------------------------------------------------------------- numbers (mm)
PLATE_T = 1.5
WR = E("WR", 16.5)
ZB, ZT = -WR + 1.5, E("ZT", 13.0)
FLOOR_TOP = ZB + 1.2
W = E("W", 47.0)                       # body half width
YR, YF = E("YR", -50.0), 18.0           # rear / front face of tub
CH = E("CH", 14.0)                      # rear chamfer legs
NARROW = W - 7.0                  # half width of the tub front section the arms bolt onto
STEP_Y = 2.0                   # arms start here
WALL = 1.6
WW, WY, WX = 10.0, E("WY", -17.0), W - 9.0   # wheel radius, width, y, centre |x|
WELL = (W - 15.0, W - 2.5, WY - 17.0, WY + 17.0)           # |x| lo/hi, y lo/hi
BULK = W - 17.0                                  # bulkhead inner face |x|
MOT_X = BULK - 11.25 - 0.27                                 # N10 origin |x|
DY, DZ, DR, DHALF = 34.0, 0.0, 12.0, W - 8.5   # drum axle y, z, outer r, half length
DBORE, DBORE_M = 11.0, 9.1
ARM_OUT = W
ARM_IN, ARM_R = W - 7.0, 14.5
AV = E("AV", 1) > 0
AH = E("AH", 11.0)
AZT, AZB = E("AZT", 10.0), -WR + 1.0 + AH
X0 = DHALF - 6.1                                    # weapon motor origin x (+x side, rot 180,0,180)


def box(sx, sy, sz, at=(0, 0, 0)):
    return {"type": "place", "shape": {"type": "box", "size": [sx, sy, sz]}, "at": list(at), "rot": [0, 0, 0]}


def bx(x0, x1, y0, y1, z0, z1):
    return box(x1 - x0, y1 - y0, z1 - z0, ((x0 + x1) / 2, (y0 + y1) / 2, (z0 + z1) / 2))


def cylx(r, x0, x1, y, z):
    return {"type": "place", "shape": {"type": "cylinder", "radius": r, "height": x1 - x0},
            "at": [(x0 + x1) / 2, y, z], "rot": [0, 90, 0]}


def cylz(r, z0, z1, x, y):
    return {"type": "place", "shape": {"type": "cylinder", "radius": r, "height": z1 - z0},
            "at": [x, y, (z0 + z1) / 2], "rot": [0, 0, 0]}


def prism_z(pts, z0, z1):
    return {"type": "place", "shape": {"type": "prism", "points": [list(p) for p in pts], "height": z1 - z0},
            "at": [0, 0, (z0 + z1) / 2], "rot": [0, 0, 0]}


def U(*items):
    return {"type": "union", "items": list(items)}


def S(base, *cuts):
    return {"type": "subtract", "base": base, "cut": list(cuts)}


def mx(s):
    return {"type": "mirror", "shape": s, "axis": "x"}


def both(f):
    """f(sign) -> shape; returns [f(+1), f(-1)]."""
    return [f(1), f(-1)]


# ---------------------------------------------------------------- tub (chassis)
def half_outline():
    return [(0, YR), (W - CH, YR), (W, YR + CH), (W, STEP_Y), (NARROW, STEP_Y), (NARROW, YF), (0, YF)]


def full(pts):
    right = [p for p in pts if p[0] > 0]
    left = [(-x, y) for (x, y) in reversed(right)]
    return right + left


outer = full(half_outline())
k = 2 * math.sqrt(2) * WALL / 2 * 2  # offset of the chamfer line by WALL
c_in = (W - CH - YR) - WALL * math.sqrt(2)          # x - y = c on the inner chamfer
_yw = WELL[2] - WALL
_corner = [(W - WALL, (W - WALL) - c_in), (W - WALL, _yw)] if (W - WALL) - c_in < _yw - 0.5 else [(c_in + _yw, _yw)]
inner_half = [(0, YR + WALL), (c_in + YR + WALL, YR + WALL)] + _corner + [(BULK, _yw), (BULK, STEP_Y),
              (NARROW - WALL, STEP_Y), (NARROW - WALL, YF - WALL), (0, YF - WALL)]
inner = full(inner_half)

tub_solid = prism_z(outer, ZB, ZT)
cavity = prism_z(inner, FLOOR_TOP, ZT + 1)
cuts = [cavity]
for s in (1, -1):
    cuts.append(bx(*sorted((s * WELL[0], s * WELL[1])), WELL[2], WELL[3], ZB - 1, ZT + 1))      # wheel well
    cuts.append(cylx(2.3, *sorted((s * (BULK - 0.5), s * (BULK + 2.5))), WY, 0))                # gearbox shaft hole
adds = []
for s in (1, -1):
    # motor cradle: two saddles + low end wall, pocket 0.25 mm per side
    sad = U(bx(*sorted((s * (MOT_X - 12.25), s * (MOT_X - 7.5))), WY - 7.5, WY + 7.5, FLOOR_TOP - 0.3, 0.0),
            bx(*sorted((s * (BULK - 5.0), s * BULK)), WY - 7.5, WY + 7.5, FLOOR_TOP - 0.3, 0.0))
    pocket = bx(*sorted((s * (MOT_X - 11.5), s * (BULK - 0.01))), WY - 6.25, WY + 6.25, -5.25, 5.25)
    pocket = U(pocket, bx(*sorted((s * (MOT_X - 12.5), s * (MOT_X - 11.0))), WY - 4.5, WY + 4.5, -1.0, 1.0))
    adds.append(S(sad, pocket))
    # arm bolt columns (also take the plate's front-middle screw)
    adds.append(bx(*sorted((s * (NARROW - WALL - 9.0), s * (NARROW - WALL + 0.3))), STEP_Y - 0.3, 7.0, FLOOR_TOP - 0.3, ZT))
    adds.append(bx(*sorted((s * (NARROW - WALL - 9.0), s * (NARROW - WALL + 0.3))), 12.5, YF - WALL + 0.3, FLOOR_TOP - 0.3, ZT))
    # rear plate-screw columns
    adds.append(bx(*sorted((s * (W - 21.0), s * (W - 14.0))), YR + WALL - 0.3, YR + 9.0, FLOOR_TOP - 0.3, ZT))
BAT = (0.0, -37.0, 45.0, 16.0, 12.0)   # centre x, y, size x, y, z (tattu 2S 300)
bz1 = FLOOR_TOP + BAT[4]
for s_ in (1, -1):
    adds.append(bx(*sorted((s_ * (BAT[2] / 2 + 0.25), s_ * (BAT[2] / 2 + 1.45))), BAT[1] - 6, BAT[1] + 6, FLOOR_TOP - 0.3, FLOOR_TOP + 4))
    adds.append(bx(-12, 12, *sorted((BAT[1] + s_ * (BAT[3] / 2 + 0.25), BAT[1] + s_ * (BAT[3] / 2 + 1.45))), FLOOR_TOP - 0.3, FLOOR_TOP + 4))
cuts.append(bx(-15, 15, BAT[1] - 4, BAT[1] + 4, ZB - 1, FLOOR_TOP + 0.5))   # floor window under the battery
# phase-lead pass from the +x arm into the tub
cuts.append(bx(NARROW - WALL - 1.5, NARROW + 0.5, 8.0, 12.0, -2.0, 2.0))
tub = S(U(S(tub_solid, *cuts[:1]), *adds), *cuts[1:])

# ---------------------------------------------------------------- arms (separate prints, +x layers)
def arm_body(s):
    x0, x1 = sorted((s * ARM_IN, s * ARM_OUT))
    if AV:   # upright stadium (photo): ends r AH about (DY, AZT) and (DY, AZB), plus a rear tab beside the tub
        prof = U(bx(x0, x1, STEP_Y, DY, -9.0, ZT),
                 bx(x0, x1, DY - AH, DY + AH, AZB, AZT), cylx(AH, x0, x1, DY, AZT), cylx(AH, x0, x1, DY, AZB))
    else:
        prof = U(bx(x0, x1, STEP_Y, DY, -ARM_R, ZT), cylx(ARM_R, x0, x1, DY, DZ))
    return prof


# screws: arm -> tub (along x), motor -> +x arm (along x)
CB_DEPTH = 1.5
CB_MOT = 2.0
ARM_SCREWS = [(4.0, -5.0), (15.0, -5.0)]
MOT_SCREWS = [(DY - 3.182, DZ - 3.182), (DY + 3.182, DZ + 3.182)]


def screw_cut_x(s, y, z, x_head, x_tip):
    """counterbore + clearance in the arm (from the outer face to x_head ... arm inner face)."""
    xo = s * ARM_OUT
    return [cylx(2.15, *sorted((xo + s * 0.5, s * x_head)), y, z),
            cylx(1.2, *sorted((s * x_head, s * (ARM_IN - 2.0))), y, z)]


x_head = ARM_OUT - CB_DEPTH
arm_l_cuts, arm_r_cuts = [], []
for s, lst in ((1, arm_l_cuts), (-1, arm_r_cuts)):
    for (y, z) in ARM_SCREWS:
        lst += screw_cut_x(s, y, z, x_head, 0)
arm_l_extra = [cylx(5.5, X0 + 6.05, ARM_IN + 0.01, DY, DZ)]       # stator boss
for (y, z) in MOT_SCREWS:
    arm_l_cuts += screw_cut_x(1, y, z, ARM_OUT - CB_MOT, 0)
arm_l_cuts += [
    bx(X0 + 5.1, ARM_OUT - 2.5, 22.5, 27.5, -2.5, 2.5),        # lead exit from the stator end
    bx(ARM_IN + 1.5, ARM_OUT - 2.5, 7.5, 27.5, -2.0, 2.0),         # lead channel inside the arm
    bx(ARM_IN - 0.5, ARM_OUT - 2.5, 8.0, 12.0, -2.0, 2.0),  # into the tub
]
arm_l = S(U(arm_body(1), *arm_l_extra), *arm_l_cuts)
arm_r_cuts += [cylx(2.0, -ARM_OUT - 1, -ARM_IN + 1, DY, DZ),           # dead shaft bore
               cylx(1.1, -ARM_OUT - 1, -ARM_IN + 1, DY, DZ - 12.8)]    # locking pin
arm_r = S(arm_body(-1), *arm_r_cuts)
# pilot holes in the tub for the arm screws
for s in (1, -1):
    for (y, z) in ARM_SCREWS:
        tub = S(tub, cylx(0.8, *sorted((s * (NARROW - WALL - 8.5), s * (NARROW + 0.5))), y, z))

# ---------------------------------------------------------------- top plate
pl_half = [(0, YR), (W - CH, YR), (W, YR + CH), (W, WELL[2] - 1.0), (WELL[0] - 1.0, WELL[2] - 1.0),
           (WELL[0] - 1.0, WELL[3] + 1.0), (W, WELL[3] + 1.0), (W, YF), (0, YF)]
plate = prism_z(full(pl_half), ZT, ZT + PLATE_T)
SW = (0.0, -6.0)
sw_z = ZT - 2.25
plate_adds = []
for s in (1, -1):
    plate_adds.append(bx(*sorted((s * (MOT_X - 6.2), s * (MOT_X + 7.8))), WY - 2.0, WY + 2.0, 5.25, ZT + 0.3))   # motor hold-down ribs
plate_adds.append(bx(-12, 12, BAT[1] - 1.0, BAT[1] + 1.0, bz1 + 0.25, ZT + 0.3))   # battery hold-down rib
# switch pocket block hanging under the plate
pblock = bx(SW[0] - 11.5, SW[0] + 11.5, SW[1] - 4.5, SW[1] + 4.5, 8.5, ZT + 0.3)
pcut = [bx(SW[0] - 5.4, SW[0] + 5.4, SW[1] - 3.0, SW[1] + 3.0, 8.0, ZT - 0.4),       # body
        bx(SW[0] - 10.1, SW[0] + 10.1, SW[1] - 3.0, SW[1] + 3.0, ZT - 0.6, ZT + 0.0)]  # flange
plate = S(U(plate, *plate_adds, S(pblock, *pcut)),
          bx(SW[0] - 2.0, SW[0] + 5.5, SW[1] - 2.0, SW[1] + 2.0, ZT - 1, ZT + PLATE_T + 1),   # lever slot
          bx(-17.5, -10.5, 3.0, 9.0, ZT - 1, ZT + PLATE_T + 1))                                # bind/LED window

# ---------------------------------------------------------------- drum (weapon), local frame at (0, DY, DZ)
drum = S(U(cylx(DR, -DHALF, DHALF, 0, 0),
           bx(0.0, DHALF, -1.6, 1.6, DR - 0.6, 14.5),
           bx(-DHALF, 0.0, -1.6, 1.6, -14.5, -(DR - 0.6))),
         cylx(DBORE, -DHALF - 1, X0 - 6.0, 0, 0),
         cylx(DBORE_M, X0 - 6.01, DHALF + 1, 0, 0),
         cylx(1.1, -DHALF - 1, -DHALF + 4.0, 0, -12.8),
         cylx(1.1, DHALF - 4.0, DHALF + 1, 0, 12.8))
endcap = S(cylx(DBORE, -DHALF, -DHALF + 1.5, 0, 0),
           cylx(2.05, -DHALF - 1, -DHALF + 4, 0, 0))

# ---------------------------------------------------------------- wheels
HUB_R = WR - 3.5


def tyre(s):
    x0, x1 = sorted((s * (WX - WW / 2), s * (WX + WW / 2)))
    return S(cylx(WR, x0, x1, WY, 0), cylx(HUB_R, x0 - 1, x1 + 1, WY, 0))


def hub(s):
    x0, x1 = sorted((s * (WX - WW / 2), s * (WX + WW / 2)))
    web = sorted((s * (WX - WW / 2), s * (WX - WW / 2 + 3.0)))
    h = U(S(cylx(HUB_R, x0, x1, WY, 0), cylx(HUB_R - 1.6, x0 - 1, x1 + 1, WY, 0)),
          cylx(HUB_R, web[0], web[1], WY, 0),
          cylx(3.5, x0, x1, WY, 0))
    return S(h, cylx(1.55, *sorted((s * (WX - WW / 2 - 1), s * 39.0)), WY, 0))


# ---------------------------------------------------------------- parts
P = []
P.append({"id": "chassis", "kind": "structure", "material": "nylon", "process": "fdm", "at": [0, 0, 0], "rot": [0, 0, 0],
          "color": "#22262a", "print_orientation": "+z", "shape": tub})
P.append({"id": "top_plate", "kind": "structure", "material": "nylon", "process": "fdm", "at": [0, 0, 0], "rot": [0, 0, 0],
          "color": "#2b3034", "print_orientation": "-z", "shape": plate})
P.append({"id": "drum_arm_l", "kind": "structure", "material": "nylon", "process": "fdm", "at": [0, 0, 0], "rot": [0, 0, 0],
          "color": "#22262a", "print_orientation": "+x", "shape": arm_l})
P.append({"id": "drum_arm_r", "kind": "structure", "material": "nylon", "process": "fdm", "at": [0, 0, 0], "rot": [0, 0, 0],
          "color": "#22262a", "print_orientation": "-x", "shape": arm_r})
P.append({"id": "weapon", "kind": "weapon", "material": "aluminium", "process": "cnc", "at": [0, DY, DZ], "rot": [0, 0, 0],
          "color": "#b9b9b4",
          "weapon": {"kind": "drum", "spin_axis": [1, 0, 0], "teeth": 2, "cells": 2, "reduction": 1.0,
                     "motor": "weapon_motor", "locking_bar": "lock_pin"},
          "joint": {"kind": "revolute", "axis": [1, 0, 0], "pivot": [0, DY, DZ], "min": 0, "max": 360, "default": 0},
          "rotates_with": "rotor_weapon", "shape": drum})
P.append({"id": "drum_endcap", "kind": "other", "material": "aluminium", "process": "turned",
          "at": [0, 0, 0], "rot": [0, 0, 0], "color": "#a9aaa5", "parent": "weapon", "rotates_with": "rotor_weapon",
          "shape": endcap})
P.append({"id": "drum_shaft", "kind": "shaft", "material": "steel", "process": "cots", "label": "4 mm silver steel dead shaft",
          "at": [0, 0, 0], "rot": [0, 0, 0], "color": "#9aa3a8", "retained": "press_fit",
          "retained_reason": "4 mm silver steel pressed into the 4.0 mm arm bore; the drum end cap turns on it",
          "shape": cylx(2.0, -ARM_OUT + 0.5, -DHALF + 1.8, DY, DZ)})
P.append({"id": "lock_pin", "kind": "locking_bar", "material": "steel", "process": "cots", "label": "2 mm silver steel locking pin",
          "at": [0, 0, 0], "rot": [0, 0, 0], "color": "#d23a2a", "tethered": True,
          "shape": cylx(1.0, -ARM_OUT + 0.5, -DHALF + 3.5, DY, DZ - 12.8)})
P.append({"id": "weapon_motor", "kind": "weapon_motor", "catalog": "brotherhobby_tc1404_3800kv",
          "at": [X0, DY, DZ], "rot": [180, 0, 180]})
for s, side in ((1, "l"), (-1, "r")):
    P.append({"id": f"wheel_{side}", "kind": "wheel", "material": "tpu", "process": "fdm", "at": [0, 0, 0], "rot": [0, 0, 0],
              "color": "#e07a6a", "tyre_of": f"hub_{side}", "print_orientation": "+x" if s > 0 else "-x", "shape": tyre(s)})
    P.append({"id": f"hub_{side}", "kind": "other", "material": "nylon", "process": "fdm", "at": [0, 0, 0], "rot": [0, 0, 0],
              "color": "#3a2c2a", "print_orientation": "+x" if s > 0 else "-x", "shape": hub(s)})
    P.append({"id": f"drive_{side}", "kind": "motor", "catalog": "bbb_n10_1000rpm",
              "at": [s * MOT_X, WY, 0], "rot": [0, 0, 0 if s > 0 else 180]})
P.append({"id": "battery", "kind": "battery", "catalog": "tattu_2s_300_75c_hv", "at": [0, -37.0, FLOOR_TOP + 6.01],
          "rot": [0, 0, 0], "retained": "pocket", "retained_reason": "printed rails on the floor (0.25 mm per side) and a lid rib above hold it on every side"})
P.append({"id": "rx_esc", "kind": "esc", "catalog": "bbb_malenki_nano", "at": [-6.0, 6.0, FLOOR_TOP + 1.26], "rot": [0, 0, 0],
          "retained": "velcro", "retained_reason": "velcro pad on the tub floor in the front bay"})
P.append({"id": "weapon_esc", "kind": "esc", "catalog": "bbb_ant_esc", "at": [16.5, 5.0, FLOOR_TOP + 2.01], "rot": [0, 0, 90],
          "retained": "velcro", "retained_reason": "velcro pad on the front bay floor beside the receiver"})
P.append({"id": "switch", "kind": "switch", "catalog": "switch_bbb_ant_rvrn2", "at": [SW[0], SW[1], sw_z], "rot": [0, 0, 0],
          "tool_free": True, "marked": True, "label": "POWER ON/OFF", "off_dir": [-1, 0, 0]})

d = {k: old[k] for k in ("name", "profile", "robot_type", "locomotion") if k in old}
d["parts"] = P
d["fasteners"] = []
for s, side, arm in ((1, "l", "drum_arm_l"), (-1, "r", "drum_arm_r")):
    for i, (y, z) in enumerate(ARM_SCREWS):
        d["fasteners"].append({"id": f"f_arm_{side}{i}", "designation": "M2x16", "at": [s * x_head, y, z], "dir": [-s, 0, 0],
                               "through": [arm], "threads_into": "chassis", "tool": "hex1.3", "removable": True,
                               "head": "button"})
for i, (y, z) in enumerate(MOT_SCREWS):
    d["fasteners"].append({"id": f"f_wmot{i}", "designation": "M2x10", "at": [ARM_OUT - CB_MOT, y, z], "dir": [-1, 0, 0],
                           "through": ["drum_arm_l"], "threads_into": "weapon_motor", "tool": "hex1.3", "removable": True,
                           "head": "button"})
d["wires"] = [
    {"id": "w_bat_sw", "from": "battery.jst_ph", "to": "switch.in", "kind": "power", "awg": 22, "slack_mm": 10, "via": [[0.0, 9.5, -3.0]]},
    {"id": "w_sw_rx", "from": "switch.out", "to": "rx_esc.bat", "kind": "power", "awg": 24, "slack_mm": 10},
    {"id": "w_sw_wesc", "from": "switch.out", "to": "weapon_esc.bat", "kind": "power", "awg": 22, "slack_mm": 10, "via": [[19.5, -9.0, -7.0]]},
    {"id": "w_m1", "from": "rx_esc.m1", "to": "drive_l.terminals", "kind": "motor", "awg": 26, "slack_mm": 10, "via": [[2.5, WY, 1.5]]},
    {"id": "w_m2", "from": "rx_esc.m2", "to": "drive_r.terminals", "kind": "motor", "awg": 26, "slack_mm": 10, "via": [[-2.5, WY, 1.5]]},
    {"id": "w_wsig", "from": "rx_esc.wpn", "to": "weapon_esc.rx", "kind": "signal", "awg": 28, "slack_mm": 10},
    {"id": "w_phases", "from": "weapon_esc.motor", "to": "weapon_motor.phases", "kind": "motor", "awg": 24, "slack_mm": 10,
     "rotor_ok": "in-drum outrunner: the phase leads leave the fixed stator base inside the drum end and run straight into the "
                 "fixed arm boss; they never cross the drum wall, only pass the open drum end on the stationary side"},
]
R = "reason"
d["connections"] = [
    {"a": "top_plate", "b": "chassis", "method": "screw", R: "lid screwed down onto the tub wall tops and corner columns; the wall tops locate it"},
    {"a": "drum_arm_l", "b": "chassis", "method": "screw", R: "arm bolted sideways through the tub's front side wall into the bolt columns; its rear face bears on the tub step"},
    {"a": "drum_arm_r", "b": "chassis", "method": "screw", R: "arm bolted sideways through the tub's front side wall into the bolt columns; its rear face bears on the tub step"},
    {"a": "weapon_motor", "b": "drum_arm_l", "method": "screw", R: "outrunner stator base bolted with two M2 screws through the arm boss; the boss spigot locates it"},
    {"a": "weapon", "b": "weapon_motor", "method": "press_fit", "interference_mm": 0.05, R: "drum bore pressed over the outrunner bell, which drives it; Loctite 638 retaining compound backs the fit"},
    {"a": "drum_endcap", "b": "weapon", "method": "press_fit", "interference_mm": 0.05, R: "aluminium end cap pressed into the drum's open end; it carries the drum on the dead shaft"},
    {"a": "drum_shaft", "b": "drum_arm_r", "method": "press_fit", "interference_mm": 0.05, R: "4 mm dead shaft pressed into the right arm bore, carries the drum end cap radial load"},
    {"a": "lock_pin", "b": "drum_arm_r", "method": "pin", R: "steel locking pin through the right arm into a blind hole in the drum impact bar; tethered, fitted before handling"},
    {"a": "drive_l", "b": "chassis", "method": "interlock", R: "N10 in a printed cradle (0.25 mm per side), gearbox face on the bulkhead, held down by the lid rib"},
    {"a": "drive_r", "b": "chassis", "method": "interlock", R: "N10 in a printed cradle (0.25 mm per side), gearbox face on the bulkhead, held down by the lid rib"},
    {"a": "hub_l", "b": "drive_l", "method": "press_fit", "interference_mm": 0.1, R: "hub D-bore pressed on the 3 mm gearmotor D-shaft; the flat carries the torque"},
    {"a": "hub_r", "b": "drive_r", "method": "press_fit", "interference_mm": 0.1, R: "hub D-bore pressed on the 3 mm gearmotor D-shaft; the flat carries the torque"},
    {"a": "wheel_l", "b": "hub_l", "method": "press_fit", "interference_mm": 0.1, R: "TPU tyre stretched over the printed hub rim; traction load carried by the stretch"},
    {"a": "wheel_r", "b": "hub_r", "method": "press_fit", "interference_mm": 0.1, R: "TPU tyre stretched over the printed hub rim; traction load carried by the stretch"},
    {"a": "battery", "b": "chassis", "method": "interlock", R: "battery boxed by printed floor rails 0.25 mm per side and pressed down by a rib under the lid"},
    {"a": "rx_esc", "b": "chassis", "method": "velcro", R: "receiver/ESC board on a velcro pad on the front bay floor"},
    {"a": "weapon_esc", "b": "chassis", "method": "velcro", R: "weapon ESC on a velcro pad on the front bay floor beside the receiver"},
    {"a": "switch", "b": "top_plate", "method": "interlock", R: "switch flange trapped between the lid and the printed pocket ledge under it; lever through the lid slot"},
]
d["reference"] = old["reference"]
d["electronics"] = old["electronics"]
OUT.write_text(json.dumps(d, indent=1))
print("wrote", OUT, len(P), "parts")
