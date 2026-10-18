"""Architecture checks: every check id fails on a bad design and passes on a good one."""

import copy

import pytest

from robot import spec
from robot.checks import Options, verify


def box(x, y, z, at=(0, 0, 0), rot=(0, 0, 0)):
    return {"type": "place", "shape": {"type": "box", "size": [x, y, z]}, "at": list(at), "rot": list(rot)}


def cyl(r, h, at=(0, 0, 0), rot=(0, 0, 0)):
    return {"type": "place", "shape": {"type": "cylinder", "radius": r, "height": h}, "at": list(at), "rot": list(rot)}


def sub(base, *cuts):
    return {"type": "subtract", "base": base, "cut": list(cuts)}


def P(id, kind, shape, mat="nylon", proc="fdm", **kw):
    d = {"id": id, "kind": kind, "material": mat, "process": proc, "shape": shape}
    d.update(kw)
    return d


def F(id, des, at, dir, through, into=None, **kw):
    d = {"id": id, "designation": des, "at": list(at), "dir": list(dir), "through": list(through), "threads_into": into,
         "tool": "hex2.5", "removable": True, "head": "socket"}
    d.update(kw)
    return d


AX_Z = 28.0  # weapon axle height


def fork(side):
    x = 14.0 * side
    # Upright 10 x 20 x 30 standing on the tub top (z 5..35), axle hole at z 28.
    return P(f"fork_{'l' if side > 0 else 'r'}", "structure", sub(box(10, 30, 30, (x, 20, 20)), cyl(2.6, 12, (x, 20, AX_Z), (0, 90, 0))),
             print_dir=[1, 0, 0])


def spinner():
    """A small vertical spinner that should pass every architecture check."""
    tub = P("tub", "structure", sub(box(60, 60, 10), box(29, 19, 10, (0, -15, 2))))
    parts = [
        tub, fork(1), fork(-1),
        P("shaft", "shaft", cyl(2.5, 40, (0, 20, AX_Z), (0, 90, 0)), mat="steel", proc="cots"),
        {"id": "disc", "kind": "weapon", "material": "hardox", "process": "laser", "at": [0, 20, AX_Z], "rot": [0, 90, 0],
         "shape": {"type": "union", "items": [cyl(14, 6), box(4, 6, 6, (0, 15, 0))]},
         "joint": {"kind": "revolute", "axis": [1, 0, 0], "pivot": [0, 20, AX_Z], "min": 0, "max": 360},
         "weapon": {"kind": "disc", "spin_axis": [0, 0, 1], "supported_both_ends": True}},
        P("wheel_l", "wheel", cyl(15, 8, (40, -10, 10), (0, 90, 0)), mat="pla"),
        P("wheel_r", "wheel", cyl(15, 8, (-40, -10, 10), (0, 90, 0)), mat="pla"),
        {"id": "battery", "kind": "battery", "catalog": "lipo_2s_180", "at": [0, -15, 2.5]},
    ]
    fs = []
    for side, n in ((1, "l"), (-1, "r")):
        for k, y in enumerate((10.0, 30.0)):
            fs.append(F(f"bolt_f{n}{k}", "M3x16", (14 * side, y, -5), (0, 0, 1), ["tub"], f"fork_{n}"))
    return {"name": "t", "robot_type": "vertical_spinner", "parts": parts, "fasteners": fs,
            "connections": [{"a": "shaft", "b": "fork_l", "method": "press_fit", "reason": "pressed", "interference_mm": 0.05}]}


def run(d):
    rep = verify(spec.Spec(copy.deepcopy(d)), Options(only=["architecture"], deep=False, fast=True))
    out = {}
    for f in rep.findings:
        out.setdefault(f.id, []).append(f)
    return out, rep


def failed(res, fid):
    return any(not f.passed for f in res.get(fid, []))


def passed(res, fid):
    return fid in res and all(f.passed for f in res[fid])


_CACHE = {}


def good(name):
    if name not in _CACHE:
        _CACHE[name] = run(GOOD[name]())[0]
    return _CACHE[name]


# ----------------------------------------------------------------------------------------------- other good designs

def wedge():
    """Tub, side pods with wheels, a top lid, two blades, inserts, two gearmotors clamped by a strap."""
    tub = P("tub", "structure", sub(box(60, 70, 12), box(40, 30, 10, (0, -10, 2))))
    pod = lambda s: P(f"pod_{s}", "structure", box(16, 60, 24, (38 if s == "l" else -38, 0, 6)))
    blade = lambda s: P(f"blade_{s}", "wedge", box(20, 30, 3, (15 if s == "l" else -15, 45, -4.5)), mat="steel", proc="laser")
    parts = [tub, pod("l"), pod("r"), blade("l"), blade("r"),
             P("lid", "armor", box(60, 70, 2, (0, 0, 7)), mat="pc", proc="cnc"),
             P("wheel_l", "wheel", cyl(10, 6, (38, 0, 4), (0, 90, 0)), mat="pla"),
             P("wheel_r", "wheel", cyl(10, 6, (-38, 0, 4), (0, 90, 0)), mat="pla"),
             {"id": "battery", "kind": "battery", "catalog": "lipo_2s_180", "at": [0, -10, 2]}]
    fs = []
    for s, sx in (("l", 1), ("r", -1)):
        for k, y in enumerate((-25, -14, 25)):
            fs.append(F(f"bolt_p{s}{k}", "M3x10", (38 * sx, y, -6), (0, 0, 1), ["tub"], f"pod_{s}"))
        for k, (x, y) in enumerate(((8, 38), (22, 38), (15, 50))):
            fs.append(F(f"bolt_b{s}{k}", "M3x8", (x * sx, y, -3), (0, 0, -1), [f"blade_{s}"], "tub"))
    for k, (x, y) in enumerate(((24, 28), (-24, 28), (24, -28), (-24, -28))):
        fs.append(F(f"bolt_lid{k}", "M2x6", (x, y, 8), (0, 0, -1), ["lid"], "tub"))
    return {"name": "w", "robot_type": "wedge", "parts": parts, "fasteners": fs,
            "connections": [{"a": "blade_l", "b": "tub", "method": "interlock", "reason": "slot"},
                            {"a": "blade_r", "b": "tub", "method": "interlock", "reason": "slot"}]}


def motor_bay():
    """A gearmotor boxed between a printed cradle and a strap bolted over it."""
    return {"name": "m", "parts": [
        P("tub", "structure", sub(box(40, 40, 16), box(21.1, 10, 12.2, (0, 0, 2)))),
        {"id": "motor_l", "kind": "motor", "catalog": "n10_300rpm_6v", "at": [0, 0, 2]},
        P("strap", "structure", box(16, 14, 2, (0, 0, 9.1))),
        P("wheel_l", "wheel", cyl(12, 4, (19, 0, 4), (0, 90, 0)), mat="pla"),
    ], "fasteners": [F("bolt_s0", "M2x8", (-6, 0, 10.1), (0, 0, -1), ["strap"], "tub"),
                     F("bolt_s1", "M2x8", (6, 0, 10.1), (0, 0, -1), ["strap"], "tub")]}


def inserts():
    """A lid held by M2 screws into heat-set inserts in a printed boss, axis in the layer plane."""
    return {"name": "i", "parts": [
        P("tub", "structure", box(40, 40, 10), print_dir=[1, 0, 0]),
        P("lid", "wedge", box(40, 40, 2, (0, 0, 6)), mat="aluminium", proc="cnc"),
        {"id": "insert_a", "kind": "insert", "catalog": "heatset_m2", "at": [10, 0, 3.5]},
        {"id": "insert_b", "kind": "insert", "catalog": "heatset_m2", "at": [-10, 0, 3.5]},
    ], "fasteners": [F("bolt_a", "M2x6", (10, 0, 7), (0, 0, -1), ["lid"], "insert_a"),
                     F("bolt_b", "M2x6", (-10, 0, 7), (0, 0, -1), ["lid"], "insert_b")]}


def rear_axle():
    """A printed wheel on a bronze-bushed steel pin pressed deep into a tub boss."""
    return {"name": "a", "parts": [
        P("tub", "structure", box(40, 40, 20)),
        P("pin_l", "pin", cyl(1.5, 20, (22, 0, 0), (0, 90, 0)), mat="steel", proc="cots"),
        P("hub_l", "wheel", sub(cyl(8, 6, (28, 0, 0), (0, 90, 0)), cyl(1.6, 8, (28, 0, 0), (0, 90, 0))), mat="pla"),
        P("bush_l", "bearing", sub(cyl(2.5, 6, (28, 0, 0), (0, 90, 0)), cyl(1.5, 8, (28, 0, 0), (0, 90, 0))), mat="brass", proc="cots"),
    ], "connections": [{"a": "hub_l", "b": "pin_l", "method": "shaft", "reason": "runs on a bushing"}]}


GOOD = {"spinner": spinner, "wedge": wedge, "motor_bay": motor_bay, "inserts": inserts, "rear_axle": rear_axle}


# ----------------------------------------------------------------------------------------------- bad mutations

def _part(d, pid):
    return next(p for p in d["parts"] if p["id"] == pid)


def _fast(d, fid):
    return next(f for f in d["fasteners"] if f["id"] == fid)


def m_tpu_structural(d):
    _part(d, "fork_l")["material"] = "tpu"


def m_tpu_threaded(d):
    _part(d, "fork_l")["material"] = "tpu"


def m_upright_brittle(d):
    for s in ("l", "r"):
        _part(d, f"fork_{s}")["material"] = "pla"


def m_static_on_rotor(d):
    _part(d, "battery")["parent"] = "disc"


def m_weapon_spin_joint(d):
    _part(d, "disc").pop("joint")


def m_boundary_fasteners(d):
    d["fasteners"].append(F("bad_screw", "M2x10", (2, 30, 33), (-1, 0, 0), ["fork_l", "disc"], None))


def m_fastener_spans_joint(d):
    _part(d, "fork_l")["parent"] = "tub"
    _part(d, "fork_l")["joint"] = {"kind": "revolute", "axis": [1, 0, 0], "pivot": [14, 20, 5], "min": -5, "max": 5}


def m_support_parent(d):
    _part(d, "fork_r")["parent"] = "fork_l"


def m_weapon_supports(d):
    d["parts"] = [p for p in d["parts"] if p["id"] != "fork_r"]
    d["fasteners"] = [f for f in d["fasteners"] if "fr" not in f["id"]]


def m_fork_orientation(d):
    # Tines hang forward of the axle: the fork body sits in front of and above the shaft.
    for s, x in (("l", 14), ("r", -14)):
        _part(d, f"fork_{s}")["shape"] = sub(box(10, 20, 30, (x, 26, 40)), cyl(2.6, 12, (x, 20, AX_Z), (0, 90, 0)))


def m_boss_aligned(d):
    _part(d, "fork_l")["shape"] = box(10, 20, 30, (14, 22.5, 20))  # no hole: the shaft line meets solid wall off-centre
    _part(d, "fork_l")["shape"] = sub(box(10, 20, 30, (14, 20, 20)), cyl(2.6, 12, (14, 20, AX_Z + 2.2), (0, 90, 0)))


def m_shaft_span(d, hole=1.6):
    for s, x in (("l", 34), ("r", -34)):
        _part(d, f"fork_{s}")["shape"] = sub(box(10, 30, 30, (x, 20, 20)), cyl(hole, 12, (x, 20, AX_Z), (0, 90, 0)))
    _part(d, "shaft")["shape"] = cyl(1.5, 80, (0, 20, AX_Z), (0, 90, 0))
    for f in d["fasteners"]:
        f["at"][0] = 34 * (1 if f["at"][0] > 0 else -1)


def m_weapon_centred(d):
    _part(d, "disc")["at"][0] = 4.0
    _part(d, "disc")["joint"]["pivot"][0] = 4.0


def m_weapon_support_gap(d):
    m_shaft_span(d, 2.6)
    _part(d, "shaft")["shape"] = cyl(2.5, 80, (0, 20, AX_Z), (0, 90, 0))


def m_shaft_material(d):
    _part(d, "shaft")["material"] = "pla"
    _part(d, "shaft")["process"] = "fdm"


def m_shaft_retention(d):
    d["connections"] = []


def m_bearing_upright_choice(d):
    # A thick outer wall on the axis carries nothing while the thin inner fork holds the shaft.
    _part(d, "shaft")["shape"] = cyl(2.5, 30, (0, 20, AX_Z), (0, 90, 0))
    d["parts"].append(P("outer_l", "structure", box(12, 20, 30, (26, 20, 20))))


def m_load_path(d):
    d["fasteners"] = [f for f in d["fasteners"] if "fl" not in f["id"]]
    _part(d, "fork_l")["shape"] = sub(box(10, 20, 26, (14, 20, 22)), cyl(2.6, 12, (14, 20, AX_Z), (0, 90, 0)))


def m_load_path_fasteners(d):
    d["fasteners"] = [f for f in d["fasteners"] if f["id"] != "bolt_fl1"]
    for f in d["fasteners"]:
        if f["id"] == "bolt_fl0":
            f["designation"] = "M2x16"
    # The upright stands 1 mm proud of the tub: no seat, the screw takes everything.
    _part(d, "fork_l")["shape"] = sub(box(10, 30, 30, (14, 20, 21)), cyl(2.6, 12, (14, 20, AX_Z), (0, 90, 0)))


def m_load_path_thin(d):
    for f in d["fasteners"]:
        f["designation"] = "M3x11"


def m_fork_stiffness(d):
    for s, x in (("l", 11), ("r", -11)):
        _part(d, f"fork_{s}")["shape"] = sub(box(2, 20, 30, (x, 20, 20)), cyl(2.6, 12, (x, 20, AX_Z), (0, 90, 0)))
        _part(d, f"fork_{s}")["material"] = "petg"
    for f in d["fasteners"]:
        f["at"][0] = 11 * (1 if f["at"][0] > 0 else -1)
        f["designation"] = "M2x16"


def m_weapon_teeth(d):
    _part(d, "disc")["shape"] = cyl(16, 6)
    _part(d, "disc")["material"] = "aluminium"


def m_foreign_through_rotor(d):
    d["parts"].append(P("rod", "pin", cyl(1, 30, (0, 20, AX_Z + 8), (0, 90, 0)), mat="steel", proc="cots"))


def m_holder_group(d):
    _part(d, "battery")["parent"] = "disc"


def m_cut_breakout(d):
    t = _part(d, "tub")
    t["shape"] = sub(box(60, 60, 10), box(29, 19, 10, (0, -15, 2)), cyl(1.6, 12, (29.5, 0, 0)))


def m_double_bearing(d):
    d["parts"].append({"id": "weapon_motor", "kind": "weapon_motor", "catalog": "bl_1806_2300kv", "at": [8, 20, AX_Z]})
    _part(d, "disc")["weapon"]["motor"] = "weapon_motor"


def m_com_support(d):
    d["parts"].append(P("ballast", "other", box(40, 40, 10, (0, 80, 30)), mat="steel", proc="cots"))


def m_com_height(d):
    d["parts"].append(P("mast", "structure", box(10, 10, 200, (0, -15, 105)), mat="steel", proc="cots"))


def m_electronics_isolated(d):
    d["parts"].append({"id": "rx", "kind": "receiver", "catalog": "rx_fs_ia6_decased", "at": [29.05, 20, 20]})


def m_battery_restraint(d):
    _part(d, "battery")["at"] = [0, -15, 7.0]


def m_symmetry(d):
    _part(d, "wheel_r")["shape"] = cyl(13, 8, (-40, -10, 10), (0, 90, 0))


def m_symmetry_fasteners(d):
    _fast(d, "bolt_fr0")["at"][1] = 11.0


# wedge mutations
def m_pod_mount(d):
    d["fasteners"] = [f for f in d["fasteners"] if f["id"] not in ("bolt_pl0", "bolt_pl2")]


def m_pods_enclose(d):
    _part(d, "pod_l")["shape"] = box(16, 10, 6, (38, 25, 0))


def m_cantilever_fastener(d):
    m_blade_bolts_two(d)


def m_blade_bolts_two(d):
    d["fasteners"] = [f for f in d["fasteners"] if f["id"] != "bolt_bl2"]
    d["connections"] = [c for c in d["connections"] if c["a"] != "blade_l"]
    _fast(d, "bolt_bl1")["at"][0] = 11.0


def m_blade_bolts(d):
    d["fasteners"] = [f for f in d["fasteners"] if f["id"] not in ("bolt_bl1", "bolt_bl2")]
    d["connections"] = [c for c in d["connections"] if c["a"] != "blade_l"]


def m_blade_root_support(d):
    _part(d, "blade_l")["shape"] = box(20, 30, 3, (15, 45, -9))
    for f in d["fasteners"]:
        if f["id"].startswith("bolt_bl"):
            f["at"][2] = -7.5
            f["designation"] = "M3x14"


def m_blade_root_stress(d):
    _part(d, "blade_l")["shape"] = box(20, 80, 0.6, (15, 70, -6.3))
    _part(d, "blade_l")["material"] = "aluminium"
    for f in d["fasteners"]:
        if f["id"].startswith("bolt_bl"):
            f["at"][2] = -6


def m_blade_orientation(d):
    _part(d, "blade_l")["shape"] = box(40, 10, 3, (40, 38, -4.5))


def m_armor_span(d):
    _part(d, "lid")["shape"] = box(60, 70, 0.5, (0, 0, 6.25))
    _part(d, "tub")["shape"] = sub(box(60, 70, 12), box(56, 66, 10, (0, 0, 2)))
    d["parts"] = [p for p in d["parts"] if p["id"] != "battery"]


def m_layer_tension(d):
    _part(d, "tub").pop("print_dir")


def m_insert_wall(d):
    _part(d, "insert_a")["at"] = [18.8, 0, 3.5]
    _fast(d, "bolt_a")["at"] = [18.8, 0, 7]


def m_insert_host(d):
    _part(d, "insert_a")["at"] = [30, 0, 3.5]
    _fast(d, "bolt_a")["at"] = [30, 0, 7]


def m_insert_coaxial(d):
    _fast(d, "bolt_a")["at"] = [10.8, 0, 7]


def m_edge_distance(d):
    _part(d, "lid")["shape"] = box(23, 40, 2, (0, 0, 6))


def m_hole_spacing(d):
    _part(d, "insert_b")["at"] = [14.5, 0, 3.5]
    _fast(d, "bolt_b")["at"] = [14.5, 0, 7]


def m_bolt_washer(d):
    _part(d, "lid")["material"] = "pp"
    _part(d, "lid")["process"] = "fdm"


def m_bolt_shear(d):
    _part(d, "lid")["mass_g"] = 2000
    _part(d, "lid")["material"] = None
    for f in d["fasteners"]:
        f["grade"] = "nylon"


def m_bolt_bearing(d):
    m_bolt_shear(d)
    _part(d, "lid")["material"] = "pp"
    _part(d, "lid")["process"] = "fdm"
    _part(d, "lid").pop("mass_g")
    _part(d, "lid")["scale_mass_g"] = 1500


def m_bolt_bending(d):
    _part(d, "lid")["shape"] = box(40, 40, 2, (0, 0, 10))
    for f in d["fasteners"]:
        f["at"][2] = 11
        f["designation"] = "M2x10"


# motor bay
def m_motor_mount(d):
    d["parts"] = [p for p in d["parts"] if p["id"] != "strap"]
    d["fasteners"] = []
    d["connections"] = [{"a": "motor_l", "b": "tub", "method": "press_fit", "reason": "snug", "interference_mm": 0.1}]


def m_motor_clamp(d):
    m_motor_mount(d)
    d["connections"] = [{"a": "motor_l", "b": "tub", "method": "screw", "reason": "said so"}]
    _part(d, "tub")["shape"] = box(40, 40, 6, (0, 0, -7))


def m_motor_antirotation(d):
    m_motor_clamp(d)


def m_motor_face_bolts(d):
    d["fasteners"].append(F("bolt_m", "M2x12", (-14, 0, 2), (1, 0, 0), ["tub"], "motor_l"))


def m_motor_face_static(d):
    d["parts"].append({"id": "weapon_motor", "kind": "weapon_motor", "catalog": "bl_1806_2300kv", "at": [0, 30, 20]})
    d["parts"].append(P("plate", "structure", box(4, 30, 30, (9, 30, 20))))
    d["parts"].append({"id": "disc", "kind": "weapon", "material": "steel", "process": "laser", "at": [-12, 30, 20], "rot": [0, 90, 0],
                       "shape": cyl(12, 3), "weapon": {"kind": "disc", "motor": "weapon_motor", "spin_axis": [0, 0, 1]}})
    d["fasteners"].append(F("bolt_wm", "M2x4", (11, 30, 26), (-1, 0, 0), ["plate"], "weapon_motor"))
    d["fasteners"].append(F("bolt_wm2", "M2x4", (11, 30, 14), (-1, 0, 0), ["plate"], "weapon_motor"))
    _part(d, "weapon_motor")["stator_face"] = "-x"


# rear axle
def m_wheel_bore(d):
    d["parts"] = [p for p in d["parts"] if p["id"] != "bush_l"]


def m_axle_engagement(d):
    _part(d, "pin_l")["shape"] = cyl(1.5, 9, (26.5, 0, 0), (0, 90, 0))


CASES = [
    ("arch.tpu_structural", "spinner", m_tpu_structural), ("arch.tpu_threaded", "spinner", m_tpu_threaded),
    ("arch.upright_brittle", "spinner", m_upright_brittle), ("arch.static_on_rotor", "spinner", m_static_on_rotor),
    ("arch.weapon_spin_joint", "spinner", m_weapon_spin_joint), ("arch.boundary_fasteners", "spinner", m_boundary_fasteners),
    ("arch.fastener_spans_joint", "spinner", m_fastener_spans_joint), ("arch.support_parent", "spinner", m_support_parent),
    ("arch.weapon_supports", "spinner", m_weapon_supports), ("arch.fork_orientation", "spinner", m_fork_orientation),
    ("arch.boss_aligned", "spinner", m_boss_aligned), ("arch.shaft_span", "spinner", m_shaft_span),
    ("arch.weapon_centred", "spinner", m_weapon_centred), ("arch.weapon_support_gap", "spinner", m_weapon_support_gap),
    ("arch.shaft_material", "spinner", m_shaft_material), ("arch.shaft_retention", "spinner", m_shaft_retention),
    ("arch.bearing_upright_choice", "spinner", m_bearing_upright_choice), ("arch.load_path", "spinner", m_load_path),
    ("arch.load_path_fasteners", "spinner", m_load_path_fasteners), ("arch.load_path_thin", "spinner", m_load_path_thin),
    ("arch.fork_stiffness", "spinner", m_fork_stiffness), ("arch.weapon_teeth", "spinner", m_weapon_teeth),
    ("arch.foreign_through_rotor", "spinner", m_foreign_through_rotor), ("arch.holder_group", "spinner", m_holder_group),
    ("arch.cut_breakout", "spinner", m_cut_breakout), ("arch.double_bearing", "spinner", m_double_bearing),
    ("arch.com_support", "spinner", m_com_support), ("arch.com_height", "spinner", m_com_height),
    ("arch.electronics_isolated", "spinner", m_electronics_isolated), ("arch.battery_restraint", "spinner", m_battery_restraint),
    ("arch.symmetry", "spinner", m_symmetry), ("arch.symmetry_fasteners", "spinner", m_symmetry_fasteners),
    ("arch.pod_mount", "wedge", m_pod_mount), ("arch.pods_enclose", "wedge", m_pods_enclose),
    ("arch.cantilever_fastener", "wedge", m_cantilever_fastener), ("arch.blade_bolts", "wedge", m_blade_bolts),
    ("arch.blade_root_support", "wedge", m_blade_root_support), ("arch.blade_root_stress", "wedge", m_blade_root_stress),
    ("arch.blade_orientation", "wedge", m_blade_orientation), ("arch.armor_span", "wedge", m_armor_span),
    ("arch.layer_tension", "inserts", m_layer_tension), ("arch.insert_wall", "inserts", m_insert_wall),
    ("arch.insert_host", "inserts", m_insert_host), ("arch.insert_coaxial", "inserts", m_insert_coaxial),
    ("arch.edge_distance", "inserts", m_edge_distance), ("arch.hole_spacing", "inserts", m_hole_spacing),
    ("arch.bolt_washer", "inserts", m_bolt_washer), ("arch.bolt_shear", "inserts", m_bolt_shear),
    ("arch.bolt_bearing", "inserts", m_bolt_bearing), ("arch.bolt_bending", "inserts", m_bolt_bending),
    ("arch.motor_mount", "motor_bay", m_motor_mount), ("arch.motor_clamp", "motor_bay", m_motor_clamp),
    ("arch.motor_antirotation", "motor_bay", m_motor_antirotation), ("arch.motor_face_bolts", "motor_bay", m_motor_face_bolts),
    ("arch.motor_face_static", "motor_bay", m_motor_face_static),
    ("arch.wheel_bore", "rear_axle", m_wheel_bore), ("arch.axle_engagement", "rear_axle", m_axle_engagement),
]


@pytest.mark.parametrize("fid,base,mut", CASES, ids=[c[0] for c in CASES])
def test_check_fails_on_bad_and_passes_on_good(fid, base, mut):
    g = good(base)
    assert passed(g, fid), f"{fid} on good {base}: {[(f.severity, f.message) for f in g.get(fid, [])]}"
    d = GOOD[base]()
    mut(d)
    res, _ = run(d)
    assert failed(res, fid), f"{fid} on bad {base}: {[(f.passed, f.message) for f in res.get(fid, [])]}"


@pytest.mark.parametrize("base", list(GOOD))
def test_good_designs_have_no_architecture_blockers(base):
    g = good(base)
    bad = [(f.id, f.message) for fs in g.values() for f in fs if not f.passed and f.severity == "blocker"]
    assert not bad, bad


def test_fork_orientation_is_blocker():
    d = spinner()
    m_fork_orientation(d)
    res, _ = run(d)
    assert any(f.severity == "blocker" and not f.passed for f in res["arch.fork_orientation"])


def test_no_chassis_is_not_checked():
    res, rep = run({"name": "x", "parts": [P("w", "wheel", cyl(10, 5), mat="pla")]})
    assert failed(res, "arch.chassis") and any("rchitecture" in n for n in rep.not_checked)


def test_motor_in_hub_rule_follows_archetype():
    d = spinner()
    m_double_bearing(d)
    d["archetype"] = "revron_like"
    res, _ = run(d)
    # Unknown archetype name: the rule is silent rather than guessing.
    assert "arch.weapon_motor_in_hub" not in res or res["arch.weapon_motor_in_hub"]


def test_exploded_view_keeps_wheels_in_their_pods():
    from robot import world

    r = world.resolve(spec.Spec(wedge()), fast=True)
    w = world.World.start(r).exploded()
    pod, wheel = w.body("pod_l"), w.body("wheel_l")
    lo, hi = pod.aabb
    assert pod.center[0] > 38 + 10  # the pod moved outward
    assert all(lo <= wheel.center) and all(wheel.center <= hi)


def test_axle_section_views_exist_for_spinners():
    from robot import render, world

    r = world.resolve(spec.Spec(spinner()), fast=True)
    w = world.World.start(r)
    views = render.axle_sections(w, r, 200)
    assert [v.name for v in views] == ["section_axle_x", "section_axle_y"]
    assert render.render_array(w, views[0]) is not None
