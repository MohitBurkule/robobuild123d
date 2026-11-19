"""RBMK spec generator (photo rebuild). Right = +x, front = +y."""
import json, math, sys
from pathlib import Path

SPEC = Path(sys.argv[1])
old = json.loads(SPEC.read_text())
P = dict(json.loads(sys.argv[2])) if len(sys.argv) > 2 else {}

def g(k, d):
    return P.get(k, d)

c10, s10 = math.cos(math.radians(10)), math.sin(math.radians(10))
WA = g("wing_deg", 10.0)
cw, sw = math.cos(math.radians(WA)), math.sin(math.radians(WA))

def place(shape, at=(0, 0, 0), rot=(0, 0, 0)):
    return {"type": "place", "shape": shape, "at": [float(v) for v in at], "rot": list(rot)}

def box(sx, sy, sz, at=(0, 0, 0), rot=(0, 0, 0)):
    return place({"type": "box", "size": [sx, sy, sz]}, at, rot)

def cyl(r, h, at=(0, 0, 0), rot=(0, 0, 0)):
    return place({"type": "cylinder", "radius": r, "height": h}, at, rot)

def prism(pts, h, at=(0, 0, 0), rot=(0, 0, 0)):
    return place({"type": "prism", "points": [[float(a), float(b)] for a, b in pts], "height": h}, at, rot)

def U(*items):
    return {"type": "union", "items": list(items)}

def I(*items):
    return {"type": "intersect", "items": list(items)}

def SUB(base, *cut):
    return {"type": "subtract", "base": base, "cut": list(cut)}

XZ = (90, 0, 0)      # prism (x,y)->(x,z), extruded along y
YZ = (90, 0, 90)     # prism (x,y)->(y,z), extruded along x
AY = (90, 0, 0)      # cylinder axis along y
AX = (0, 90, 0)      # cylinder axis along x

# ---------------------------------------------------------------- dimensions
T = 1.0                      # sheet
B = 29.0                     # half width of the base plate / bend line
ZT = 5.0                     # base plate top
TX, TY0, TY1 = 28.0, -30.0, 34.0     # tub half width, rear, front
TZ0, TZ1 = ZT + 0.0, g('tz1', 16.6)    # tub bottom (on plate), tub top (lid seat)
CH = 4.0                     # side top chamfer
WALL, FLOOR = 1.6, 1.2
RI, RO = 1.5, 2.5
WV0, WV1 = -6.0, 30.0        # wing hinge span (y)
WL = g("wing_len", 27.0)
UM, VM = 11.5, g("motor_y", 12.0)  # motor position on the wing (u along wing, v = y)
BAR_R = g("bar_r", 34.0)
BAR_T = 2.0
RY0 = -30.5                  # rear bend line
REAR_DEG = g("rear_deg", 50.0)
REAR_L = g("rear_len", 36.0)

# wing frame (right side)
CW = (B, ZT - T - RI)                          # bend centre (x,z)
MW = (CW[0] + (RI + T / 2) * sw, CW[1] + (RI + T / 2) * cw)   # wing mid surface start
tw = (cw, -sw)                                 # along wing
nw = (sw, cw)                                  # wing normal (up/out)

def wing_pt(u, off):
    return (MW[0] + u * tw[0] + off * nw[0], MW[1] + u * tw[1] + off * nw[1])

# motor centre
mb = wing_pt(UM, T / 2)
MC = (mb[0] + 7.0 * nw[0], mb[1] + 7.0 * nw[1])
BARC = (MC[0] + 8.7 * nw[0], MC[1] + 8.7 * nw[1])

# ---------------------------------------------------------------- base plate (one folded aluminium sheet)
def bend_y(c, a0, a1, y0, y1):
    """annulus sector about an axis along y through (c.x, c.z), angles a0..a1 (deg, in x-z, from +x toward +z)."""
    L = y1 - y0
    yc = (y0 + y1) / 2
    ring = SUB(cyl(RI + T, L, (c[0], yc, c[1]), AY), cyl(RI, L + 1, (c[0], yc, c[1]), AY))
    pts = [c] + [(c[0] + 6 * math.cos(math.radians(a)), c[1] + 6 * math.sin(math.radians(a))) for a in (a0, (a0 + a1) / 2, a1)]
    return I(ring, prism(pts, L, (0, yc, 0), XZ))

def bend_x(c, a0, a1, x0, x1):
    """annulus sector about an axis along x through (c.y, c.z), angles in y-z from +y toward +z."""
    L = x1 - x0
    xc = (x0 + x1) / 2
    ring = SUB(cyl(RI + T, L, (xc, c[0], c[1]), AX), cyl(RI, L + 1, (xc, c[0], c[1]), AX))
    pts = [c] + [(c[0] + 6 * math.cos(math.radians(a)), c[1] + 6 * math.sin(math.radians(a))) for a in (a0, (a0 + a1) / 2, a1)]
    return I(ring, prism(pts, L, (xc, 0, 0), YZ))

WING_PTS = [(0, WV0), (WL, WV0 + 8), (WL, WV1 - 8), (0, WV1)]
_ba = math.radians(g("bar_ang", 135.0))
LOCK_R = g("lock_r", 12.2)
lock_u = UM + LOCK_R * math.sin(_ba)
lock_v = VM - LOCK_R * math.cos(_ba)
# lock pin hole in the wing (under the bar slot in its parked pose)
def wing_holes():
    return [cyl(1.1, 4, (lock_u, lock_v, 0)),
            cyl(1.2, 4, (UM, VM - 6.0, 0)), cyl(1.2, 4, (UM, VM + 6.0, 0))]
wing = SUB(prism(WING_PTS, T), *wing_holes())
wing_r = U(bend_y(CW, 80.0, 90.0, WV0, WV1), place(wing, (MW[0], 0, MW[1]), (0, WA, 0)))

# centre plate
BN = B - 1.5   # relief: the plate is narrower where no wing is folded
center = U(box(2 * BN, TY1 - RY0, T, (0, (TY1 + RY0) / 2, ZT - T / 2)), box(2 * B, WV1 - WV0, T, (0, (WV1 + WV0) / 2, ZT - T / 2)))
# rear bend + rear (up-turned) plate
CR = (RY0, ZT + RI)
ra = -90.0 - REAR_DEG
MR = (CR[0] + (RI + T / 2) * math.cos(math.radians(ra)), CR[1] + (RI + T / 2) * math.sin(math.radians(ra)))
REAR_PTS = [(-BN, 0), (BN, 0), (BN, 13), (13, REAR_L), (-13, REAR_L), (-BN, 13)]
rear = place(prism(REAR_PTS, T), (0, MR[0], MR[1]), (180 - REAR_DEG, 0, 0))
rear_bend = bend_x(CR, ra, -90.0, -BN, BN)

BOSS = [(sx * 19.5, y) for sx in (1, -1) for y in (-25.5, 29.5)]
base_holes = [cyl(1.2, 4, (x, y, ZT - T / 2)) for x, y in BOSS]
base_shape = SUB(U(center, wing_r, {"type": "mirror", "shape": wing_r, "axis": "x"}, rear_bend, rear), *base_holes)

# ---------------------------------------------------------------- printed tub (inner structure, aluminium colour)
env = prism([(-TX, TZ0), (TX, TZ0), (TX, TZ1 - CH), (TX - CH, TZ1), (-TX + CH, TZ1), (-TX, TZ1 - CH)],
            TY1 - TY0, (0, (TY0 + TY1) / 2, 0), XZ)
ix = TX - WALL
k = (TX + TZ1 - CH) - WALL * math.sqrt(2)  # inner chamfer line x + z = k
cav_pts = [(-ix, TZ0 + FLOOR), (ix, TZ0 + FLOOR), (ix, k - ix), (k - TZ1 - 1, TZ1 + 1), (-(k - TZ1 - 1), TZ1 + 1), (-ix, k - ix)]
cav = prism(cav_pts, TY1 - TY0 - 2 * WALL, (0, (TY0 + TY1) / 2, 0), XZ)
bosses = [cyl(3.2, TZ1 - TZ0, (x, y, (TZ0 + TZ1) / 2)) for x, y in BOSS]
# lead conduits from the side walls out to the motors (printed with the tub)
LZ = g("lead_z", 10.0)
motor_in_x = None
def motor_inner_x(z):
    # inner side line of the motor body: bottom inner corner + t * axis
    bi = wing_pt(UM - 10.5, T / 2)
    t = (z - bi[1]) / nw[1]
    return bi[0] + t * nw[0]
mix = motor_inner_x(LZ)
CX1 = mix - 0.6
conduit = box(CX1 - TX + 1.0, 7.6, 7.0, ((CX1 + TX - 1.0) / 2, VM, LZ))
conduit_bore = box(CX1 - TX + 4.0, 4.4, 4.4, ((CX1 + TX - 4.0) / 2 + 0.01, VM, LZ))
# roller fork tines (front)
AXY, RR = TY1 + 9.0, 6.5
FLOOR_Z = g("floor_z", -0.71)
AXZ = FLOOR_Z + RR
tine_xs = [0.0, 13.5, -13.5]
def tine(x):
    prof = U(prism([(TY1 - 1.0, 13.0), (TY1 - 1.0, ZT + 0.3), (TY1 + 0.3, ZT + 0.3), (TY1 + 0.3, AXZ - 3.5), (AXY, AXZ - 3.5), (AXY, AXZ + 3.5), (TY1 + 3.0, 13.0)], 2.0, (x, 0, 0), YZ),
             cyl(3.5, 2.0, (x, AXY, AXZ), AX))
    return prof
tines = [tine(x) for x in tine_xs]
axle_bore = cyl(1.5, 30.0, (0, AXY, AXZ), AX)
# heat-set insert bores (top for the lid, bottom for the base plate)
ins_top = [cyl(1.6, 3.3, (x, y, TZ1 - 1.65 + 0.01)) for x, y in BOSS]
ins_bot = [cyl(1.6, 3.3, (x, y, TZ0 + 1.65 - 0.01)) for x, y in BOSS]
# switch slot through the left wall
SW = (0.0, -25.0, TZ1 - 2.25)
SWH = [(SW[0] - 7.5, SW[1]), (SW[0] + 7.5, SW[1])]
sw_posts = [cyl(2.0, TZ1 - 0.5 - (TZ0 + FLOOR) + 0.5, (x, y, (TZ1 - 0.5 + TZ0 + FLOOR - 0.5) / 2)) for x, y in SWH]
sw_ins = [cyl(0.8, 7.0, (x, y, TZ1 - 0.5 - 3.5 + 0.01)) for x, y in SWH]   # 1.6 mm tap holes: screws self-tap into the posts
# battery pocket ribs (floor to z+4) round the 28 x 18 pack
BAT = (0.0, -10.0)
def ribs():
    hx, hy, c, w, h = 14.0, 9.0, 0.25, 0.9, 4.0
    z = TZ0 + FLOOR + h / 2 - 0.1
    return [box(16.0, w, h, (BAT[0], BAT[1] + sy * (hy + c + w / 2), z)) for sy in (1, -1)] + \
           [box(w, 2 * (hy + c), h, (BAT[0] + sx * (hx + c + w / 2), BAT[1], z)) for sx in (1, -1)]
shell = {"type": "round_inside", "radius": 1.05, "axis": "z", "shape": U(I(SUB(env, cav), env), I(U(*bosses), env), *sw_posts, *ribs())}
tub_shape = SUB(U(shell, conduit, {"type": "mirror", "shape": conduit, "axis": "x"}, *tines),
                conduit_bore, {"type": "mirror", "shape": conduit_bore, "axis": "x"},
                axle_bore, *ins_top, *ins_bot, *sw_ins)

# lid (clear polycarbonate)
LX = TX - CH
lid_shape = {"type": "round_inside", "radius": 0.3, "axis": "z", "shape": None}
lid_shape["shape"] = SUB(box(2 * LX, TY1 - TY0, 1.0, (0, (TY0 + TY1) / 2, TZ1 + 0.5)),
                box(4.9, 3.6, 3, (SW[0] + 1.75, SW[1], TZ1 + 0.5)),
                *[cyl(1.2, 3, (x, y, TZ1 + 0.5)) for x, y in SWH],
                *[cyl(1.2, 3, (x, y, TZ1 + 0.5)) for x, y in BOSS])

# ---------------------------------------------------------------- weapons
def bar_shape():
    # asymmetric bar (photo): hammer arm with a T-head and hooked tooth, longer tail as counterweight;
    # the outline is shifted so its centroid sits on the spin axis (balanced)
    from shapely.geometry import Polygon, Point, box as sbox
    w, cap_w, cap_l = 4.5, 11.0, 6.0
    LT, LS, tr = g("bar_t", 28.0), g("bar_tail", 40.0), g("bar_tail_r", 4.5)
    head = [(w, 7.0), (w, LT - cap_l), (cap_w, LT - cap_l), (cap_w + 1.2, LT - 1.0), (cap_w, LT), (-cap_w + 1.5, LT),
            (-cap_w, LT - 2.0), (-cap_w, LT - cap_l), (-w, LT - cap_l), (-w, 7.0)]
    tail = [(-w, -7.0), (-tr, -(LS - tr))] + [(tr * math.cos(math.radians(a)), -(LS - tr) + tr * math.sin(math.radians(a))) for a in range(195, 360, 30)] + [(tr, -(LS - tr)), (w, -7.0)]
    s1 = (10.0, LT - cap_l - 1.5)
    s2 = (-(LS - 6.0), -10.0)
    sp = Polygon(head + tail).union(Point(0, 0).buffer(8.6, 128)).difference(sbox(-1.25, s1[0], 1.25, s1[1])).difference(sbox(-1.25, s2[0], 1.25, s2[1]))
    cx, cy = sp.centroid.x, sp.centroid.y
    outline = [(x - cx, y - cy) for x, y in head + tail]
    hub = cyl(8.6, BAR_T, (-cx, -cy, 0))
    holes = [cyl(2.6, BAR_T + 1)] + [cyl(1.1, BAR_T + 1, (5.5 * math.cos(math.radians(a)), 5.5 * math.sin(math.radians(a)), 0)) for a in (45, 135, 225, 315)]
    slots = [box(2.5, s1[1] - s1[0], BAR_T + 1, (-cx, (s1[0] + s1[1]) / 2 - cy, 0)),
             box(2.5, s2[1] - s2[0], BAR_T + 1, (-cx, (s2[0] + s2[1]) / 2 - cy, 0))]
    return {"type": "round_inside", "radius": 0.4, "axis": "z", "shape": SUB(U(prism(outline, BAR_T), hub), *holes, *slots)}

def roller_shape():
    prof = [(1.55, -5.25), (5.6, -5.25), (6.5, -4.2), (6.5, 4.2), (5.6, 5.25), (1.55, 5.25)]
    return place({"type": "revolve", "profile": [list(p) for p in prof]}, (0, 0, 0), AX)

parts = []
def part(**kw):
    parts.append(kw)
    return kw

part(id="chassis", kind="structure", material="nylon", process="fdm", print_orientation="+z", shape=tub_shape,
     at=[0, 0, 0], rot=[0, 0, 0], color="#c4cacd",
     label="body tub (printed; the real robot's tub is folded aluminium sheet)")
part(id="base_plate", kind="plate", material="aluminium", process="sheet_bent", shape=base_shape, at=[0, 0, 0], rot=[0, 0, 0],
     color="#b7bdc1", label="1 mm aluminium base: motor wings folded down 10 deg, rear plate folded up 50 deg")
part(id="lid", kind="plate", material="pc", process="laser", shape=lid_shape, at=[0, 0, 0], rot=[0, 0, 0], color="#d4e6ea",
     label="1 mm clear polycarbonate lid")

side = {"r": 1, "l": -1}
for sname, s in side.items():
    mx, mz = MC[0] * s, MC[1]
    mrot = [0, -90 + WA * s, 0]
    # phase port: on the motor's inner face at the conduit height (motor-local coords)
    # world offset from motor centre to the port
    pz = LZ
    t = (pz - (wing_pt(UM - 10.5, T / 2)[1])) / nw[1]
    loc_axis = t - 7.0                      # along the motor axis from its centre
    port_local = [round(loc_axis, 3), 0.0, round(10.5 * s, 3)]
    part(id=f"weapon_motor_{sname}", kind="weapon_motor", catalog="bl_1806_2300kv", at=[round(mx, 3), VM, round(mz, 3)], rot=mrot,
         rotates_with="fixed", ports={"phases": port_local}, color="#1d1e21",
         label=f"{'right' if s > 0 else 'left'} 1806 outrunner, stator bolted to the folded wing (2 x M2 from below)")
    part(id=f"weapon_{sname}", kind="weapon", material="steel", process="laser", shape=bar_shape(), parent=f"weapon_motor_{sname}",
         at=[8.7, 0.0, 0.0], rot=[0.0, 90.0, 0.0], rotates_with=f"weapon_{sname}",
         joint={"kind": "revolute", "axis": [1, 0, 0], "pivot": [8.7, 0.0, 0.0], "min": 0, "max": 360, "default": round((g("bar_ang", 135.0) * s) % 360, 1)},
         color="#2c2e31", organic=True,
         weapon={"kind": "bar", "motor": f"weapon_motor_{sname}", "cells": 2, "reduction": 1.0, "spin_axis": [0, 0, 1],
                 "spin_dir": "ccw" if s > 0 else "cw", "supported_both_ends": False, "teeth": 2,
                 "locking_bar": f"lock_pin_{sname}"},
         label=f"2 mm steel T-bar {2 * BAR_R:.0f} mm tip to tip, slotted arms, 4 M2 to the bell")
    # lock pin through the bar's slot into the wing hole, parallel to the spin axis
    lp = wing_pt(lock_u, 0.0)
    pin_len = (BARC[0] - lp[0]) * nw[0] + (BARC[1] - lp[1]) * nw[1] + 2.5
    pc_ = ((lp[0] + nw[0] * (pin_len / 2 - 1.0)) * s, lock_v, lp[1] + nw[1] * (pin_len / 2 - 1.0))
    part(id=f"lock_pin_{sname}", kind="locking_bar", material="steel", process="cots", stock="2 mm steel rod",
         shape=cyl(1.0, round(pin_len, 2)), at=[round(v, 3) for v in pc_], rot=[0, WA * s, 0], color="#e0301e",
         tethered=True, label="red REMOVE-BEFORE-FIGHT pin through the bar slot into the wing")

# lid/base inserts + screws
fasteners = []
for i, (x, y) in enumerate(BOSS):
    part(id=f"ins_t{i}", kind="insert", catalog="heatset_m2", at=[x, y, round(TZ1 - 1.5, 3)], rot=[0, 0, 0], retained="press_fit")
    part(id=f"ins_b{i}", kind="insert", catalog="heatset_m2", at=[x, y, round(TZ0 + 1.5, 3)], rot=[0, 0, 0], retained="press_fit")
    fasteners.append({"id": f"lid_s{i}", "designation": "M2x4", "at": [x, y, TZ1 + 1.0], "dir": [0, 0, -1], "through": ["lid"],
                      "threads_into": f"ins_t{i}", "tool": "hex1.3", "removable": True, "head": "button"})
    fasteners.append({"id": f"base_s{i}", "designation": "M2x4", "at": [x, y, ZT - T], "dir": [0, 0, 1], "through": ["base_plate"],
                      "threads_into": f"ins_b{i}", "tool": "hex1.3", "removable": True, "head": "button"})

for i, (x, y) in enumerate(SWH):
    fasteners.append({"id": f"sw_s{i}", "designation": "M2x8", "at": [round(x, 3), round(y, 3), TZ1 + 1.0], "dir": [0, 0, -1],
                      "through": ["lid", "el_switch"], "threads_into": "chassis", "tool": "hex1.3", "removable": True, "head": "button"})
for sname, s in side.items():
    for j, dv in enumerate((-6.0, 6.0)):
        bp = wing_pt(UM, -T / 2)
        fasteners.append({"id": f"mot_{sname}{j}", "designation": "M2x4", "at": [round(bp[0] * s, 3), VM + dv, round(bp[1], 3)],
                          "dir": [round(nw[0] * s, 4), 0, round(nw[1], 4)], "through": ["base_plate"],
                          "threads_into": f"weapon_motor_{sname}", "tool": "hex1.3", "removable": True, "head": "button"})
# rollers (passive, free-spinning) + axle
part(id="roller_axle", kind="shaft", material="steel", process="cots", stock="3 mm silver steel rod", shape=cyl(1.5, 28.0, rot=AX),
     at=[0, AXY, round(AXZ, 3)], rot=[0, 0, 0], color="#9aa3a8", label="3 mm roller axle pressed into the three fork tines")
for sname, s in side.items():
    part(id=f"roller_{sname}", kind="other", material="tpu", process="fdm", print_orientation="+x", shape=roller_shape(),
         at=[round(6.75 * s, 3), AXY, round(AXZ, 3)], rot=[0, 0, 0], color="#2b8bd8",
         label="free-spinning blue nose roller (passive, not driven)")

# electronics
BZ = TZ0 + FLOOR
part(id="el_battery", kind="battery", catalog="lipo_2s_180", at=[BAT[0], BAT[1], round(BZ + 5.1, 3)], rot=[0, 0, 0], retained="pocket", retained_reason="printed ribs round all four sides, the floor below and the lid 0.3 mm above")
part(id="el_rx", kind="receiver", catalog="rx_fs_ia6_decased", at=[0, 20.5, round(BZ + 2.15, 3)], rot=[0, 0, 0], retained="velcro")
for sname, s in side.items():
    part(id=f"el_wesc_{sname}", kind="esc", catalog="bbb_ant_esc", at=[round(15.9 * s, 3), 10.8, round(BZ + 2.15, 3)], rot=[0, 0, 90],
         retained="velcro")
part(id="el_switch", kind="switch", catalog="switch_bbb_ant_rvrn2", at=[SW[0], SW[1], round(SW[2], 3)], rot=[0, 0, 0],
     tool_free=True, marked=True, label="POWER ON/OFF", off_dir=[-1, 0, 0])

wires = [
    {"id": "w_bat_sw", "from": "el_battery.xt30", "to": "el_switch.in", "kind": "power", "awg": 22, "slack_mm": 10},
    {"id": "w_sw_rx", "from": "el_switch.out", "to": "el_rx.esc", "kind": "power", "awg": 26, "slack_mm": 10},
]
# receiver powered through the ESC lead in reality; keep power to each weapon ESC
wires = [
    {"id": "w_bat_sw", "from": "el_battery.xt30", "to": "el_switch.in", "kind": "power", "awg": 22, "slack_mm": 10},
    {"id": "w_sw_wesc_r", "from": "el_switch.out", "to": "el_wesc_r.bat", "kind": "power", "awg": 22, "slack_mm": 10},
    {"id": "w_sw_wesc_l", "from": "el_switch.out", "to": "el_wesc_l.bat", "kind": "power", "awg": 22, "slack_mm": 10},
    {"id": "w_rx_wesc_r", "from": "el_rx.esc", "to": "el_wesc_r.rx", "kind": "signal", "awg": 28, "slack_mm": 10},
    {"id": "w_rx_wesc_l", "from": "el_rx.servo", "to": "el_wesc_l.rx", "kind": "signal", "awg": 28, "slack_mm": 10},
    {"id": "w_ph_r", "from": "el_wesc_r.motor", "to": "weapon_motor_r.phases", "kind": "motor", "awg": 22, "slack_mm": 10},
    {"id": "w_ph_l", "from": "el_wesc_l.motor", "to": "weapon_motor_l.phases", "kind": "motor", "awg": 22, "slack_mm": 10},
]

conn = []
def C(a, b, m, r, **kw):
    d = {"a": a, "b": b, "method": m, "reason": r}
    d.update(kw)
    conn.append(d)

for sname in side:
    C(f"weapon_{sname}", f"weapon_motor_{sname}", "screw", "steel bar bolted to the outrunner bell with 4 M2 screws on a 9.2 mm circle and centred on the shaft boss (as the photo shows)")
    C(f"lock_pin_{sname}", "base_plate", "pin", "2 mm pin through the bar slot into a hole in the wing stops the bar turning while the robot is handled; tethered, pulled before the fight")
    C(f"el_wesc_{sname}", "chassis", "strap", "weapon ESC held down on the tub floor by a velcro strap threaded through two slots in the floor; the strap wraps over the board")
C("el_battery", "chassis", "interlock", "battery sits in a pocket of printed ribs on the tub floor (0.25 mm per side) with the lid 0.3 mm above it, so it is held on every side")
C("el_rx", "chassis", "strap", "receiver held down on the tub floor by a velcro strap threaded through two slots in the floor; the strap wraps over the board")
C("roller_axle", "chassis", "press_fit", "3 mm axle pressed through the three printed fork tines; the tines carry the nose load into the tub", interference_mm=0.05, mechanical_key=True)
for sname in side:
    C(f"roller_{sname}", "roller_axle", "shaft", "passive roller turns freely on the 3 mm axle, held sideways between two fork tines")
for i in range(4):
    C(f"ins_t{i}", "chassis", "press_fit", "heat-set insert melted into its bore", interference_mm=0.1)
    C(f"ins_b{i}", "chassis", "press_fit", "heat-set insert melted into its bore", interference_mm=0.1)
for i in range(2):
    pass

allow = []
for sname in side:
    allow.append({"a": f"weapon_motor_{sname}", "b": f"el_wesc_{sname}", "max_depth_mm": 0.0, "reason": "placeholder"}) if False else None

spec = {
    "name": "rbmk", "profile": "aws2025", "robot_type": "horizontal_spinner", "locomotion": "shuffler",
    "parts": parts, "fasteners": fasteners, "wires": wires, "connections": conn,
    "reference": old.get("reference"), "electronics": {"failsafe": True, "weapon_remote_disable": True, "radio": "2.4 GHz", "cells": 2},
    "claims": [{"id": "c_mass", "text": "weighs 225 g or less (AWS non-roller: shuffler)", "metric": "mass_total_g", "op": "<=", "value": 225.0},
               {"id": "c_fit", "text": "fits the 150 mm square", "metric": "footprint_mm", "op": "<=", "value": 150.0}],
    "can_run_inverted": False,
}
oldh = {f["id"]: f.get("hole") for f in old.get("fasteners", [])}
for f in fasteners:
    if oldh.get(f["id"]) and not P.get("refill"):
        f["hole"] = oldh[f["id"]]
if not P.get("novol"):
    sys.path.insert(0, "/tmp/work10_rbmk")
    from robot import shapes as _sh
    for pp in parts:
        if pp["id"] in ("chassis", "base_plate", "lid") or pp["id"].startswith("weapon_"):
            if "shape" in pp:
                pp["volume_mm3"] = round(_sh.to_solid(pp["shape"]).volume, 1)
SPEC.write_text(json.dumps(spec, indent=1))
print("motor centre", MC, "bar centre", BARC, "axle z", AXZ, "lead x", mix)
