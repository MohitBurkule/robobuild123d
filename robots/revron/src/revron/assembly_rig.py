"""The whole Revron as one joint chain from the tub (datum) outward, built on joints.Rig.

Build order = mate order: tub -> weapon mounts (tab notch on the chassis tab bolt) -> GR1507 stator (base on RV03,
shaft along the weapon axis) -> spider (on the weapon spin axis) -> bell -> shaft, and the disc stack face on face;
tub -> N10 seats (joints.tub_rig) -> rear hubs on the gearbox D-shaft (spin axis); mount / chassis lug -> 25 and
15 mm standoffs (end on the seat) -> front hubs on the standoff axle, side panels and wedgelets on the standoff ends,
fork on the 15 mm standoff; tub -> nut pockets, electronics bays, inserts, panel and switch screws (joints.tub_rig).
Parts drawn in robot coordinates (tub, panels, mounts, standoffs, armour, hubs) carry each shared feature at the same
place as their host, so the mate leaves them at identity and the tests prove the features coincide.
"""
from .params import *  # noqa: F401,F403
from .joints import Rig, tub_rig
from .fastener_rig import screws

SIDES = ((-1, "l"), (1, "r"))


def _mid(span):
    return sum(span) / 2


def _flip(s):
    """Clocking of a mirrored part: the left one is the right one turned half a turn about Z."""
    return (0, 0, 0 if s > 0 else 180)


def _bay(r, part, at, sink=(0, 0, 0)):
    """Board/battery on its bay: catalog origin on the bay datum, long side along Y (turned 90 about Z)."""
    r.joint("tub", f"{part}_bay", at, (0, 0, 90))
    r.joint(part, "origin", sink)
    r.mate("tub", f"{part}_bay", part, "origin")


def _electronics(r):
    for k in ("battery", "rxesc", "wesc"):
        _bay(r, k, ELEC[k])
    for s, n in SIDES:                                      # thin M3 nut in its chassis-wall pocket, axis along X
        r.joint("tub", f"nut_pocket_{n}", (s * _mid(NUT_X), *NUT), (0, 90, 0))
        r.joint(f"nut_c{n}", "bore", (0, 0, 0))
        r.mate("tub", f"nut_pocket_{n}", f"nut_c{n}", "bore")


def _weapon(r):
    WA = (0, WY, WZ)                                         # weapon axis on the robot centre plane
    for s, n in SIDES:                                       # mount: notch over the chassis tab, on the bolt_u?b axis
        r.joint("tub", f"mount_tab_{n}", (s * MNT_IN, *SB))
        r.joint(f"mount_{n}", "tab_notch", (s * MNT_IN, *SB))
        r.mate("tub", f"mount_tab_{n}", f"mount_{n}", "tab_notch")
    r.joint("mount_r", "stator_seat", WA, (0, 0, 180))       # GR1507 base on RV03: catalog +X shaft points inboard (-X)
    r.joint("weapon_motor_stator", "base", (0, 0, 0))
    r.mate("mount_r", "stator_seat", "weapon_motor_stator", "base")
    r.joint("mount_r", "weapon_frame", WA)                   # weapon frame: on the spin axis
    r.axis("mount_r", "weapon_axis", (_mid(DR_X["spider"]), WY, WZ))   # spin axis at the spider mid-plane
    r.joint("spider", "bore", (0, 0, 0))
    r.mate("mount_r", "weapon_frame", "spider", "bore")
    r.joint("spider", "bell_flange", (0, 0, 0), (0, 0, 180))  # 4 M2 on r4.5 into the bell: bell faces the spider
    r.joint("weapon_motor_can", "flange", (0, 0, 0))
    r.mate("spider", "bell_flange", "weapon_motor_can", "flange")
    r.joint("weapon_motor_can", "shaft_bore", (0, 0, 0), (0, 0, 180))   # shaft pressed through the bell
    r.joint("wshaft", "axis", (0, 0, 0))
    r.mate("weapon_motor_can", "shaft_bore", "wshaft", "axis")
    r.joint("mount_l", "bearing_seat", (BRG["x"], WY, WZ), (0, 90, 0))   # MR85 centred in the RV02 seat, bore on the axis
    r.joint("wbearing", "seat", (0, 0, 0))                               # MR85 drawn on its own axis (z)
    r.mate("mount_l", "bearing_seat", "wbearing", "seat")
    r.joint("mount_r", "spacer_seat", (BSP_X[1], WY, WZ))             # back spacer flat on RV03, stator base on its far face
    r.joint("motor_spacer", "mount_face", (BSP_X[1], WY, WZ))
    r.mate("mount_r", "spacer_seat", "motor_spacer", "mount_face")
    prev, face = "spider", DR_X["spider"][1]                 # disc stack: each layer flush on the previous one
    for nm, key in (("disc_a", "disc_a"), ("dspacer", "spacer"), ("disc_b", "disc_b")):
        r.joint(prev, "stack_face", (face, 0, 0))
        r.joint(nm, "face", (DR_X[key][0], 0, 0))
        r.mate(prev, "stack_face", nm, "face")
        prev, face = nm, DR_X[key][1]


def _drive(r):
    for s, n in SIDES:
        r.axis(f"motor_{n}", "output_shaft", (HUB_PIVOT_X["rear"] - MOTX, 0, 0))   # D-shaft the rear hub turns with
        r.joint(f"motor_{n}", "shaft_tip", (HUB_PIVOT_X["rear"] - MOTX, 0, 0))
        r.joint(f"whub_r{n}", "d_bore", (s * HUB_PIVOT_X["rear"], RY, RZ), _flip(s))
        r.mate(f"motor_{n}", "shaft_tip", f"whub_r{n}", "d_bore")
        a, b_ = f"so_a{n}", f"so_b{n}"
        r.joint(f"mount_{n}", "so_a_seat", (s * SA_X[0], *SA))      # 25 mm standoff end on the mount outer face
        r.joint(a, "inner_end", (s * SA_X[0], *SA))
        r.mate(f"mount_{n}", "so_a_seat", a, "inner_end")
        r.joint("tub", f"lug_b_{n}", (s * SB_X[0], *SB))            # 15 mm standoff end on the nose lug
        r.joint(b_, "inner_end", (s * SB_X[0], *SB))
        r.mate("tub", f"lug_b_{n}", b_, "inner_end")
        for so, xs, yz in ((a, SA_X, SA), (b_, SB_X, SB)):
            r.joint(so, "outer_end", (s * xs[1], *yz))
        r.axis(a, "axle", (s * HUB_PIVOT_X["front"], *SA))           # micro hub greased on the 25 mm standoff
        r.joint(a, "hub_seat", (s * HUB_PIVOT_X["front"], *SA))
        r.joint(f"whub_f{n}", "bore", (s * HUB_PIVOT_X["front"], *SA))
        r.mate(a, "hub_seat", f"whub_f{n}", "bore")
        for part, so, xs, yz in ((f"side_{n}", a, SA_X, SA), (f"wedgelet_{n}", b_, SB_X, SB), (f"fork_{n}", b_, SB_X, SB)):
            r.joint(part, "standoff_seat", (s * xs[1], *yz))         # screw seat / 5.3 hole on the standoff end
            r.mate(so, "outer_end", part, "standoff_seat")
    for i, (x, y) in enumerate(INS):                                 # base panel: its screw holes on the floor bores
        r.joint("base_panel", f"hole_{i}", (x, y, BASE_BOLT_Z))
    r.mate("tub", "screw_b0", "base_panel", "hole_0")
    for i, (x, y) in enumerate(TOP_XY):                              # Ti top panel: its holes on the column tops
        r.hole("top_panel", f"hole_{i}", (x, y, TOP_BOLT_Z), (0, 0, -1))
    r.mate("tub", "screw_t0", "top_panel", "hole_0")


def assembly_rig():
    """Declare every joint first (a joint on a placed host would be taken in world), then mate in build order."""
    r = Rig()
    tub_rig(r, solve=False)
    _electronics(r)
    _weapon(r)
    _drive(r)
    screws(r)
    r.solve()
    return r


def revolutes(r):
    """Spec `joint` dicts of the spinning parts, read off their spin axes."""
    out = {"spider": r.revolute("mount_r", "weapon_axis")}
    for _, n in SIDES:
        out[f"whub_r{n}"] = r.revolute(f"motor_{n}", "output_shaft")
        out[f"whub_f{n}"] = r.revolute(f"so_a{n}", "axle")
    return out
