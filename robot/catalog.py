"""Parts catalog (real components with locked dimensions, mass, ports, ratings), materials and screw sizes.

Built-in entries are the same as the Rust crate (same frames, same shapes) so verdicts carry over. Entries from the shared
research file `catalog_data/components.json` are merged in as box-shaped `estimate` entries (id = `c_<slug>`); their
numbers are parsed from the research text and are only as good as that text.

Frame conventions: motors and wheels have their shaft/axle along local +X, origin at the body centre; batteries have their
long side along X; flat electronics lie in the XY plane.
"""

from __future__ import annotations

import json
import math
import re
from dataclasses import dataclass, field
from functools import lru_cache
from pathlib import Path


# Shape helpers (JSON shape trees, see shapes.py).
def box(x, y, z):
    return {"type": "box", "size": [x, y, z]}


def cyl(r, h):
    return {"type": "cylinder", "radius": r, "height": h}


def at(s, x, y, z):
    return {"type": "place", "shape": s, "at": [x, y, z], "rot": [0.0, 0.0, 0.0]}


def rot(s, r):
    return {"type": "place", "shape": s, "at": [0.0, 0.0, 0.0], "rot": list(r)}


def cyl_x(r, length):
    return rot(cyl(r, length), [0.0, 90.0, 0.0])


def union(items):
    return {"type": "union", "items": items}


def minus(base, cuts):
    return {"type": "subtract", "base": base, "cut": cuts} if cuts else base


def _gr1507_base():
    """GR1507 stator base as in the RVRN 2.0 STEP: a 2 mm cross (4 arms 3.5 wide, round tips to R9.8) round a R3.9 hub,
    one d1.6 tap-drill hole per arm at R6 (the M2 stator screws; the STEP shows d2.0). Measured sections, not a plate: a solid disc was 3.5 mm too much."""
    arm = [box(2.0, 16.1, 3.5), box(2.0, 3.5, 16.1)] + [at(rot(cyl(1.75, 2.0), [0.0, 90.0, 0.0]), 0, sy * 8.05, sz * 8.05)
                                                       for sy, sz in ((1, 0), (-1, 0), (0, 1), (0, -1))]
    holes = [at(cyl_x(0.8, 3.0), 0, 6.0 * sy, 6.0 * sz) for sy, sz in ((1, 0), (-1, 0), (0, 1), (0, -1))]
    return minus(union(arm + [cyl_x(3.9, 2.0)]), holes)


BELL_SCREW_R, BELL_SCREW_PHASE = 4.5, -54.889  # spider screw circle on the bell top and its phase about the axis (STEP; local frame)


def _gr1507_bell():
    """GR1507 bell as in the RVRN 2.0 STEP (sections, local X = -world X): a hub r3 through (-4.5..6.5), an open wall r8..9.8
    over -4.5..4.0, and a vented top: a r6.2 disc (4.5..6.0) joined to the wall by 8 ribs (two per quadrant at world
    34 and 62 deg), the 4 big vents between them. The stator inside is not modelled (the STEP leaves it out)."""
    ribs = [rot(at(box(1.5, 4.6, 1.4), 4.75, 7.5, 0), [ang, 0.0, 0.0]) for ang in (146, 118, 236, 208, 326, 298, 56, 28)]
    wall = minus(cyl_x(9.8, 8.5), [cyl_x(8.0, 9.0)])
    top = minus(cyl_x(6.2, 1.5), [rot(at(cyl_x(0.8, 1.7), 0, BELL_SCREW_R, 0), [BELL_SCREW_PHASE + 90.0 * k, 0.0, 0.0]) for k in range(4)])   # M2 tap holes (ISO 2306 r0.8) for the spider screws
    return union([at(cyl_x(3.0, 11.0), 1.0, 0, 0), at(wall, -0.25, 0, 0), at(top, 5.25, 0, 0)] + ribs)


@dataclass
class CatalogEntry:
    id: str
    kind: str
    name: str
    mass_g: float
    confidence: str
    shape: dict
    ports: dict = field(default_factory=dict)
    shaft: dict | None = None
    props: dict = field(default_factory=dict)
    color: str = "#b0b4ba"
    source: str = "builtin"

    def to_dict(self):
        return dict(self.__dict__)


def gearmotor(id, name, can_len, can_dia, flats, gb_len, gb_h, shaft_len, mass, p):
    total = can_len + gb_len
    gb_c = total / 2 - gb_len / 2
    can_c = -total / 2 + can_len / 2
    can = at({"type": "intersect", "items": [cyl_x(can_dia / 2, can_len), box(can_len + 2, flats, can_dia + 2)]}, can_c, 0, 0)
    gb = at(box(gb_len, flats, gb_h), gb_c, 0, 0)
    shaft_at = total / 2
    shaft = at(cyl_x(1.5, shaft_len), shaft_at + shaft_len / 2, 0, 0)
    return CatalogEntry(id, "motor", name, mass, "estimate", union([can, gb, shaft]), {"terminals": [-total / 2 - 0.3, 0, 0]},
                        {"at": [shaft_at, 0, 0], "dir": [1, 0, 0], "len": shaft_len, "dia": 3.0}, dict(p), "#9aa0a6")


def outrunner(id, name, dia, length, shaft_len, mass, kv, p):
    body = cyl_x(dia / 2, length)
    shaft = at(cyl_x(2.5, shaft_len), length / 2 + shaft_len / 2 - 1, 0, 0)
    pr = dict(p)
    pr["kv"] = kv
    return CatalogEntry(id, "weapon_motor", name, mass, "estimate", union([body, shaft]), {"phases": [-length / 2, 0, 0]},
                        {"at": [length / 2 - 1, 0, 0], "dir": [1, 0, 0], "len": shaft_len, "dia": 5.0}, pr, "#3a3d42")


def lipo(id, name, l, w, h, mass, cells, mah, c, conn="xt30"):
    return CatalogEntry(id, "battery", name, mass, "estimate", box(l, w, h), {conn: [0, w / 2 + 2, 0]}, None, {
        "cells": cells, "capacity_mah": mah, "c_rating": c, "nominal_v": 3.7 * cells,
        "internal_resistance_mohm": 90 / max(mah / 100, 0.5) * cells}, "#2a9d8f")


def flat(id, name, kind, x, y, z, mass, pts, p, color):
    return CatalogEntry(id, kind, name, mass, "estimate", box(x, y, z), dict(pts), None, dict(p), color)


def wheel(id, dia, width, hub, mass):
    tire = minus(cyl_x(dia / 2, width), [cyl_x(hub / 2 - 0.5, width + 2)])
    hubs = minus(cyl_x(hub / 2, width), [cyl_x(1.5, width + 2)])
    return CatalogEntry(id, "wheel", f"{dia:g} x {width:g} mm wheel (printed hub, silicone tyre)", mass, "estimate", union([tire, hubs]), {},
                        {"at": [-width / 2, 0, 0], "dir": [1, 0, 0], "len": width, "dia": 3.0},
                        {"diameter_mm": dia, "width_mm": width, "friction": 0.9}, "#25282c")


def hexagon(r):
    return [[r * math.cos(math.radians(i * 60)) * 1.1547, r * math.sin(math.radians(i * 60)) * 1.1547] for i in range(6)]


def hex_prism(s, h):
    """Hexagonal prism, `s` across flats, height `h`, centred on the origin, axis z (corners on +-x)."""
    return {"type": "prism", "points": hexagon(s / 2), "height": h}


def hex_nut(s, m, bore_d):
    """ISO 4032/4035 style nut: true hexagon `s` across flats, height `m`, 30 deg chamfer on both faces down to the
    bearing circle (dia = s), through bore. Envelope (bbox) is the same as the plain hexagon prism."""
    R = s / 2 * 1.1547
    c = (R - s / 2) * math.tan(math.radians(30))
    chamf = {"type": "revolve", "profile": [[0.0, -m / 2], [s / 2, -m / 2], [R + 0.05, -m / 2 + c + 0.03],
                                            [R + 0.05, m / 2 - c - 0.03], [s / 2, m / 2], [0.0, m / 2]]}
    return minus({"type": "intersect", "items": [hex_prism(s, m), chamf]}, [cyl(bore_d / 2, m + 1.0)])


def heatset(od, length, bore_d, ribs=12):
    """Brass heat-set insert: cylinder `od` x `length` with `ribs` axial knurl grooves cut into its outer face (inside the
    OD, so the envelope is unchanged) and a through bore."""
    r = od / 2
    g = max(0.12, 0.06 * od)
    grooves = [at(cyl(g, length + 1.0), r * math.cos(math.pi * (2 * i + 1) / ribs), r * math.sin(math.pi * (2 * i + 1) / ribs), 0.0)
               for i in range(ribs)]
    return minus(cyl(r, length), [cyl(bore_d / 2, length + 1.0)] + grooves)


def hex_recess(key, depth, z0, toward=1.0):
    """Hex socket cut: key `key` across flats, `depth` deep from the plane z=z0 into the head along `toward` (+1/-1 z).
    Overlaps the face by 0.05 so the cut opens cleanly. (No drill-point cone: its apex tessellates non-watertight.)"""
    e = 0.05
    return at(hex_prism(key, depth + e), 0.0, 0.0, z0 + toward * (depth - e) / 2)


def is_hex_recess(c) -> bool:
    """True if `c` is (contains) a hexagonal prism cut, i.e. a hex drive or nut-shaped cut."""
    if not isinstance(c, dict):
        return False
    if c.get("type") == "prism":
        return len(c.get("points") or []) == 6
    return any(is_hex_recess(x) for x in (c.get("items") or []) + ([c["shape"]] if isinstance(c.get("shape"), dict) else []))


def has_drive_recess(shape) -> bool:
    """A fastener shape carries a drive if, somewhere in its tree, a subtract cuts a hexagonal (or other polygonal)
    socket out of it."""
    if not isinstance(shape, dict):
        return False
    if shape.get("type") == "subtract" and any(is_hex_recess(c) for c in shape.get("cut") or []):
        return True
    kids = list(shape.get("items") or []) + [shape.get(k) for k in ("base", "shape") if isinstance(shape.get(k), dict)]
    return any(has_drive_recess(k) for k in kids)


def is_hex_nut(shape) -> bool:
    """A nut shape is hexagonal if its solid (subtract base, possibly intersected with a chamfer) is a 6-sided prism
    and it has a through bore cut."""
    if not isinstance(shape, dict):
        return False
    if shape.get("type") == "place":
        return is_hex_nut(shape.get("shape"))
    if shape.get("type") != "subtract" or not shape.get("cut"):
        return False
    base = shape.get("base") or {}
    if base.get("type") == "prism":
        return len(base.get("points") or []) == 6
    if base.get("type") == "intersect":
        return any(i.get("type") == "prism" and len(i.get("points") or []) == 6 for i in base.get("items") or [])
    return False


def builtin() -> list[CatalogEntry]:
    v = [
        gearmotor("n10_300rpm_6v", "N10 micro gearmotor 6 V 300 rpm", 12, 12, 10, 9.1, 12, 9, 7.5,
                  {"nominal_v": 6.0, "rpm_nominal": 300.0, "stall_current_a": 1.0, "no_load_current_a": 0.06, "stall_torque_gcm": 900.0}),
        gearmotor("n10_2200rpm_6v", "N10 micro gearmotor 6 V 2200 rpm", 12, 12, 10, 9.1, 12, 9, 7.5,
                  {"nominal_v": 6.0, "rpm_nominal": 2200.0, "stall_current_a": 1.0, "no_load_current_a": 0.08, "stall_torque_gcm": 150.0}),
        gearmotor("n20_1000rpm_6v", "N20 gearmotor 6 V 1000 rpm", 15, 12, 10, 9, 12, 10, 10.5,
                  {"nominal_v": 6.0, "rpm_nominal": 1000.0, "stall_current_a": 0.8, "no_load_current_a": 0.07, "stall_torque_gcm": 600.0}),
        outrunner("bl_1806_2300kv", "1806 2300 kV outrunner", 21, 14, 8, 17.5, 2300, {"max_current_a": 15.0, "typ_current_a": 8.0}),
        outrunner("bl_2306_1400kv", "2306 1400 kV outrunner", 27.5, 14, 10, 29, 1400, {"max_current_a": 20.0, "typ_current_a": 10.0}),
        lipo("lipo_2s_180", "2S 180 mAh LiPo (nano-tech class)", 28, 18, 10, 12.5, 2, 180, 40),
        lipo("lipo_2s_350", "2S 350 mAh LiPo", 36, 17, 11, 21.5, 2, 350, 30),
        lipo("lipo_1s_300", "1S 300 mAh LiPo", 30, 13, 8, 8.5, 1, 300, 30),
        flat("esc_dual_brushed", "Dual brushed ESC (hobby, heat-shrunk)", "esc", 15, 10, 5, 3.0,
             {"bat": [0, -6, 3], "m1": [-8, 0, 3], "m2": [8, 0, 3], "rx": [0, 6, 3]},
             {"cont_current_a": 2.5, "burst_current_a": 5.0, "channels": 2.0}, "#e76f51"),
        flat("esc_brushless_12a", "Brushless ESC 12 A with BEC", "esc", 20, 12, 4, 6.0,
             {"bat": [0, -6.5, 0], "motor": [-10.5, 0, 0], "rx": [10.5, 0, 0]},
             {"cont_current_a": 12.0, "burst_current_a": 15.0, "channels": 1.0}, "#d4af37"),
        flat("rx_fs_ia6_decased", "FlySky FS-iA6 receiver, decased", "receiver", 20, 14, 4, 4.5,
             {"esc": [0, 6.8, 0], "servo": [-5, 6.8, 0]}, {"antenna_len_mm": 80.0}, "#ff9800"),
        flat("servo_cs07", "KingMax CS07 micro servo", "servo", 22, 11.5, 20, 6.5, {"signal": [-11.5, 0, 0]},
             {"stall_torque_kgcm": 1.8, "nominal_v": 4.8, "stall_current_a": 0.7}, "#4a4e57"),
        flat("switch_slide_12x4", "Miniature slide switch 11.8 x 3.8", "switch", 11.8, 3.8, 4, 0.5,
             {"in": [-4, 0, -2.5], "out": [4, 0, -2.5]}, {}, "#111111"),
        CatalogEntry("switch_slide_bbb_ant", "switch", "BBB ant slide switch 11.8 x 3.8 with a front mounting ear (2 x M2 holes)", 0.6, "estimate",
                     union([box(11.8, 3.8, 4), minus(at(box(15.8, 6.4, 1.0), 13.8, 0.8, 2.5), [at(cyl(1.1, 3), x, 0.8, 2.5) for x in (12.1, 18.1)])]),
                     {"in": [-4, 0, -2.5], "out": [4, 0, -2.5]}, None, {"mount_holes_mm": [[12.1, 0.8, 3.0], [18.1, 0.8, 3.0]], "mount_thread": "M2"}, "#111111"),
        wheel("wheel_28x10", 28, 10, 19, 3.4),
        wheel("wheel_30x8", 30, 8, 19, 3.0),
        wheel("wheel_20x8", 20, 8, 12, 1.8),
        # RVRN reference-CAD envelopes (Revron audit 2026-10): vendor/reference envelopes, not memory.
        CatalogEntry("n10_2200rpm_spicy", "motor", "Turnabot Spicy N10 2200 rpm (micro-metal 10 x 12, 33.8 incl. 9.5 mm shaft)", 9.5, "datasheet",
                     union([at({"type": "intersect", "items": [cyl_x(6.3, 13.0), box(15.0, 10.0, 12.0)]}, -6.4, 0, 0),
                            at(cyl_x(2.4, 3.0), -14.4, 0, 0)]
                           + [at(box(0.9, 10.0, 12.0), x, 0, 0) for x in (0.6, 3.35, 7.15)]
                           + [at(cyl_x(1.1, 7.6), 3.9, 0, z) for z in (-3.5, 3.5)]
                           + [at(cyl_x(1.5, 10.0), 12.9, 0, 0)]),
                     {"terminals": [-16.2, 0, 0]}, {"at": [7.9, 0, 0], "dir": [1, 0, 0], "len": 10.0, "dia": 3.0},
                     {"nominal_v": 6.0, "rpm_nominal": 2200.0, "stall_current_a": 1.6, "no_load_current_a": 0.1, "stall_torque_gcm": 150.0}, "#9aa0a6"),
        CatalogEntry("be1806_bbb", "weapon_motor", "BBB BE1806 2300 kV outrunner (23 mm bell, 20.5 incl. base and shaft collar, 5 mm shaft bore)", 18.5, "datasheet",
                     minus(union([at(cyl_x(11.5, 15.0), 0.75, 0, 0), at(cyl_x(9.5, 3.5), -8.5, 0, 0), at(cyl_x(2.95, 2.0), 9.25, 0, 0),
                                  at(box(1.5, 5.0, 8.0), -7.6, 0, -15.5)]), [cyl_x(2.55, 22.0)]),
                     {"phases": [-7.5, 0, -15.0]}, {"at": [8.25, 0, 0], "dir": [1, 0, 0], "len": 2.0, "dia": 5.0},
                     {"kv": 2300, "max_current_a": 15.0, "typ_current_a": 8.0, "bell_mass_frac": 0.5}, "#3a3d42"),
        lipo("lipo_2s_180_turnabot", "Turnabot 2S 180 mAh LiPo (36 x 18 x 11)", 36, 18, 11, 12.5, 2, 180, 40, conn="jst_rcy"),
        flat("malenki_nano", "Malenki Nano (Rx + 2 brushed drive ESC), kapton wrapped", "esc", 23, 16, 5, 3.5,
             {"bat": [-11.5, -4, 0], "m1": [11.5, 4, 0], "m2": [-11.5, 4, 0], "wpn": [11.5, -4, 0]},
             {"cont_current_a": 3.0, "burst_current_a": 6.0, "channels": 2.0}, "#e76f51"),
        flat("bbb_ant_esc", "BBB brushless ant ESC (heat-shrunk)", "esc", 22, 11, 4, 3.0,
             {"bat": [-11, -3, 0], "motor": [11, 0, 0], "rx": [-11, 3, 0]},
             {"cont_current_a": 12.0, "burst_current_a": 18.0, "channels": 1.0}, "#d4af37"),
        CatalogEntry("nut_m3_alu", "nut", "M3 aluminium hex nut (5.5 AF)", 0.1, "datasheet",
                     hex_nut(5.5, 2.4, 3.0), {}, None, {"thread_d_mm": 3.0}, "#c0c4c8"),
        CatalogEntry("heatset_m2", "insert", "M2 brass heat-set insert 3.0 mm", 0.12, "estimate", heatset(3.2, 3.0, 2.0),
                     {}, None, {"thread_d_mm": 2.0}, "#d4af37"),
        # RVRN 2.0 STEP envelopes (Revron rebuild 2026-10): measured outline of the vendor models, not memory.
        CatalogEntry("gr1507", "weapon_motor", "GR1507 outrunner (19.6 bell: open 1.8 wall, 8-rib vented top; 4-arm cross stator base with 4 M2 on 12 mm; threaded 5 mm shaft out of the bell face)", 15.5, "estimate",
                     union([at(_gr1507_base(), -9.4, 0, 0), at(cyl_x(0.75, 4.1), -6.35, 0, 0), at(_gr1507_bell(), 0.0, 0, 0),
                            at(cyl_x(2.5, 3.0), 8.0, 0, 0), at(cyl_x(2.26, 9.2), 14.1, 0, 0),
                            at(cyl_x(0.75, 1.4), -11.1, 0, 0)]),
                     {"phases": [-11.0, 0, -9.0]}, {"at": [4.1, 0, 0], "dir": [1, 0, 0], "len": 14.6, "dia": 5.0},   # shaft leaves the bell face at 4.1 (the vented top to 6.0 is not bell wall)
                     {"kv": 2850, "max_current_a": 18.0, "typ_current_a": 8.0, "bell_mass_frac": 0.45}, "#3a3d42"),
        flat("malenki_nano_rvrn2", "Malenki Nano (Rx + 2 brushed ESC), kapton wrapped with its leads (RVRN 2.0 RV13 envelope)", "esc", 32, 20, 4.4, 4.0,
             {"bat": [-16, -6, -1.0], "m1": [16, 6, -1.0], "m2": [-16, 6, -1.0], "wpn": [16, -6, -1.0]},
             {"cont_current_a": 3.0, "burst_current_a": 6.0, "channels": 2.0}, "#e76f51"),
        flat("bbb_ant_esc_rvrn2", "BBB brushless ant ESC, heat-shrunk (RVRN 2.0 RV14 envelope)", "esc", 23.5, 12, 5, 3.0,
             {"bat": [-11.75, -3, 0], "motor": [11.75, 0, 0], "rx": [-11.75, 3, 0]},
             {"cont_current_a": 12.0, "burst_current_a": 18.0, "channels": 1.0}, "#d4af37"),
        CatalogEntry("switch_bbb_ant_rvrn2", "switch", "BBB ant switch (RVRN 2.0 RV15): 10.6 x 5.8 x 3.5 body, 20 x 5.8 flange with 2.2 holes in ears on 15 mm (STEP RV15 envelope 20 long), 2.9 x 3 lever, 3 pins", 1.0, "estimate",
                     union([at(box(10.6, 5.8, 3.5), 0, 0, 0), minus(at(box(20.0, 5.8, 0.5), 0, 0, 2.0), [at(cyl(1.1, 1.0), 7.5, 0, 2.0), at(cyl(1.1, 1.0), -7.5, 0, 2.0)]), at(box(2.9, 3.0, 3.2), 1.75, 0, 3.85),
                            at(box(1.0, 3.0, 4.0), -3.0, 0, -3.75), at(box(1.0, 3.0, 4.0), 0.0, 0, -3.75), at(box(1.0, 3.0, 4.0), 3.0, 0, -3.75)]),
                     {"in": [-3.0, 0, -5.5], "out": [0.0, 0, -5.5]}, None, {"lever_travel_mm": 3.0}, "#111111"),
        CatalogEntry("nut_m3_thin", "nut", "M3 thin hex nut BS EN 24036 (5.5 AF x 1.8)", 0.25, "datasheet",
                     hex_nut(5.5, 1.8, 3.0), {}, None, {"thread_d_mm": 3.0}, "#aaaaaa"),
        CatalogEntry("heatset_m2_4", "insert", "M2 brass heat-set insert 3.5 OD x 4 (FS1)", 0.15, "estimate", heatset(3.5, 4.0, 2.0),
                     {}, None, {"thread_d_mm": 2.0}, "#d4af37"),
        CatalogEntry("nut_m2", "nut", "M2 hex nut", 0.1, "datasheet",
                     hex_nut(4.0, 1.6, 2.0), {}, None, {"thread_d_mm": 2.0}, "#aaaaaa"),
    ]
    return v


CATEGORY_KIND = {
    "drive_motor": "motor", "weapon_motor": "weapon_motor", "battery": "battery", "lipo": "battery", "esc": "esc",
    "drive_esc": "esc", "weapon_esc": "esc", "receiver": "receiver", "rx": "receiver", "switch": "switch",
    "power_switch": "switch", "servo": "servo", "wheel": "wheel", "tyre": "tyre", "bearing": "bearing",
    "insert": "insert", "fastener": "other", "motor_mount": "other",
}


def _num(s, pat):
    m = re.search(pat, s, re.I)
    return float(m.group(1)) if m else None


def _slug(s):
    return re.sub(r"[^a-z0-9]+", "_", s.lower()).strip("_")[:40]


def research_entries(path: Path | None = None) -> list[CatalogEntry]:
    path = path or Path(__file__).parent / "catalog_data" / "components.json"
    try:
        rows = json.loads(path.read_text())
    except (OSError, ValueError):
        return []
    out, seen = [], set()
    for row in rows if isinstance(rows, list) else []:
        if not isinstance(row, dict):
            continue
        kind = CATEGORY_KIND.get(str(row.get("category", "")).lower())
        mass = _num(str(row.get("mass_g", "")), r"([0-9]+(?:\.[0-9]+)?)")
        dims = re.search(r"([0-9.]+)\s*x\s*([0-9.]+)(?:\s*x\s*([0-9.]+))?", str(row.get("dimensions_mm", "")))
        if not kind or mass is None or not dims:
            continue
        try:
            a, b = float(dims.group(1)), float(dims.group(2))
            c = float(dims.group(3)) if dims.group(3) else min(a, b)
        except ValueError:
            continue
        if min(a, b, c) <= 0 or max(a, b, c) > 300:
            continue
        cid = "c_" + _slug(str(row.get("name", "")))
        if cid in seen:
            continue
        seen.add(cid)
        text = " ".join(str(row.get(k, "")) for k in ("electrical", "dimensions_mm", "notes"))
        props = {}
        for key, pat in (("kv", r"([0-9]+)\s*kv"), ("rpm_nominal", r"([0-9]+)\s*rpm"), ("stall_current_a", r"([0-9.]+)\s*A\s*stall"),
                         ("capacity_mah", r"([0-9]+)\s*mah"), ("cells", r"([0-9])\s*S\b"), ("c_rating", r"([0-9]+)\s*C\b")):
            val = _num(text, pat)
            if val is not None:
                props[key] = val
        if kind == "battery" and "cells" in props:
            props["nominal_v"] = 3.7 * props["cells"]
        l, w, h = sorted([a, b, c], reverse=True)
        shape = box(l, w, h)
        ports = {}
        if kind == "motor":
            shape = cyl_x(h / 2, l) if abs(w - h) < 0.5 else box(l, w, h)
            ports = {"terminals": [-l / 2 - 0.3, 0, 0]}
        elif kind == "weapon_motor":
            shape = cyl_x(max(w, h) / 2, min(l, max(w, h)))
            ports = {"phases": [-min(l, max(w, h)) / 2, 0, 0]}
        elif kind == "battery":
            ports = {"xt30": [0, w / 2 + 2, 0]}
        elif kind in ("esc", "receiver", "switch"):
            ports = {"in": [-l / 2, 0, 0], "out": [l / 2, 0, 0]}
        out.append(CatalogEntry(cid, kind, str(row.get("name", cid)), mass, "estimate", shape, ports, None, props, "#8a8f98",
                                str(row.get("url") or row.get("source") or "components.json")))
    return out


@lru_cache(maxsize=1)
def catalog() -> tuple:
    return tuple(builtin() + research_entries())


def find(cid: str):
    for c in catalog():
        if c.id == cid:
            return c
    return None


@dataclass(frozen=True)
class Material:
    density: float
    cls: str  # printed, sheet, elastomer, laminate, metal, tape
    brittle: bool
    min_wall_mm: float


_MAT = [
    (("pla", "pla_st"), Material(1.24, "printed", True, 0.9)),
    (("petg",), Material(1.27, "printed", False, 0.9)),
    (("abs", "asa"), Material(1.05, "printed", False, 0.9)),
    (("nylon", "taulman910", "pa12"), Material(1.12, "printed", False, 0.9)),
    (("pla_cf", "petg_cf", "pa_cf", "cf_filament"), Material(1.3, "printed", True, 1.0)),
    (("pc", "polycarbonate"), Material(1.2, "sheet", False, 0.5)),
    (("resin",), Material(1.15, "printed", True, 0.8)),
    (("tpu", "tpu_95a", "tpu_85a"), Material(1.2, "elastomer", False, 1.2)),
    (("silicone",), Material(1.1, "elastomer", False, 1.0)),
    (("rubber", "lego_tyre"), Material(1.15, "elastomer", False, 0.8)),
    (("hdpe",), Material(0.95, "sheet", False, 1.0)),
    (("pp", "polypropylene"), Material(0.91, "sheet", False, 1.0)),
    (("uhmw",), Material(0.94, "sheet", False, 1.0)),
    (("cf_plate", "carbon_fibre"), Material(1.55, "laminate", True, 0.5)),
    (("fr4", "g10"), Material(1.85, "laminate", True, 0.5)),
    (("aluminium", "aluminum"), Material(2.7, "metal", False, 0.5)),
    (("steel", "hardox", "stainless", "304"), Material(7.9, "metal", False, 0.3)),
    (("titanium",), Material(4.43, "metal", False, 0.4)),
    (("brass",), Material(8.5, "metal", False, 0.3)),
    (("copper",), Material(8.96, "metal", False, 0.2)),
    (("tape", "kapton", "duct_tape"), Material(0.9, "tape", False, 0.0)),
    (("double_sided_tape", "foam_tape"), Material(0.5, "tape", False, 0.0)),
    (("heat_shrink",), Material(1.2, "tape", False, 0.0)),
    (("velcro",), Material(0.4, "tape", False, 0.0)),
]
MATERIALS = {name: m for names, m in _MAT for name in names}
MATERIAL_LIST = ["pla", "petg", "abs", "asa", "nylon", "pla_cf", "petg_cf", "pa_cf", "tpu", "silicone", "rubber", "hdpe", "pp", "uhmw",
                 "pc", "cf_plate", "fr4", "aluminium", "steel", "titanium", "brass", "copper", "tape", "velcro", "resin"]


def material(mid):
    return MATERIALS.get(mid) if mid else None


def density(mid):
    m = material(mid)
    return m.density if m else None


def is_printed(process):
    return process in ("fdm", "resin")


def part_is_printed(process, mat):
    if process is not None:
        return is_printed(process)
    m = material(mat)
    return bool(m and m.cls == "printed")


def screw_dims(d):
    """(head diameter, head height, key size) of an ISO socket-head screw by thread diameter."""
    for lim, v in ((1.65, (3.0, 1.6, 1.5)), (2.05, (3.8, 2.0, 1.5)), (2.55, (4.5, 2.5, 2.0)), (3.05, (5.5, 3.0, 2.5)), (4.05, (7.0, 4.0, 3.0))):
        if d <= lim:
            return v
    return (8.5, 5.0, 4.0)


def parse_designation(s):
    s = str(s or "").strip().lstrip("Mm")
    m = re.fullmatch(r"([0-9.]+)\s*[xX]\s*([0-9.]+)", s)
    if not m:
        return None
    try:
        d, l = float(m.group(1)), float(m.group(2))
    except ValueError:
        return None
    return (d, l) if 0 < d < 12 and 0 < l < 100 else None


# Diametral press-fit interference (mm) by the material class of the two parts, (min, max). A printed bore creeps and
# splits above ~0.3 mm; metal-in-metal needs a few hundredths; an elastomer takes far more.
PRESS_FIT_MM = {
    ("printed", "printed"): (0.05, 0.3),
    ("metal", "printed"): (0.05, 0.4),  # shaft, pin or insert into a printed bore
    ("metal", "metal"): (0.005, 0.05),
    ("metal", "sheet"): (0.01, 0.1),
    ("printed", "sheet"): (0.05, 0.3),
    ("sheet", "sheet"): (0.02, 0.15),
    ("elastomer", "elastomer"): (0.2, 1.5),
}
PRESS_FIT_ELASTOMER_MM = (0.1, 1.0)  # an elastomer against anything rigid
PRESS_FIT_DEFAULT_MM = (0.05, 0.4)  # a side with unknown material (catalog motor shaft into a catalog hub)


def press_fit_range(mat_a, mat_b) -> tuple:
    """(min, max) interference for a press fit between two materials, and a short label of the pair."""
    ca = material(mat_a).cls if material(mat_a) else None
    cb = material(mat_b).cls if material(mat_b) else None
    if ca is None or cb is None:
        return PRESS_FIT_DEFAULT_MM, "unknown material"
    key = tuple(sorted((ca, cb)))
    if key in PRESS_FIT_MM:
        return PRESS_FIT_MM[key], f"{key[0]}/{key[1]}"
    if "elastomer" in key:
        return PRESS_FIT_ELASTOMER_MM, f"{key[0]}/{key[1]}"
    return PRESS_FIT_DEFAULT_MM, f"{key[0]}/{key[1]}"


# Tape and hook-and-loop: grams of part per cm2 of contact they can hold through a 50 g-class hit (conservative).
TAPE_MAX_G_PER_CM2 = 2.0
TAPE_LIKE = {"tape", "double_sided_tape", "foam_tape", "velcro", "hook_and_loop"}
TAPE_CONTACT_GAP_MM = 0.5


# Mechanical properties for the strength checks: (yield or tensile strength MPa, shear strength MPa, Young's modulus GPa).
# Printed values are in-plane (XY) strengths of typical FDM parts; across layers use PRINTED_Z_FACTOR. Conservative
# handbook values, not datasheets: a blend or grade that matters should be measured.
_MECH = [
    (("pla", "pla_st"), (50.0, 30.0, 3.5)),
    (("petg",), (45.0, 28.0, 2.0)),
    (("abs", "asa"), (38.0, 24.0, 2.2)),
    (("nylon", "taulman910", "pa12"), (45.0, 30.0, 1.6)),
    (("pla_cf", "petg_cf", "pa_cf", "cf_filament"), (55.0, 32.0, 5.0)),
    (("pc", "polycarbonate"), (60.0, 40.0, 2.4)),
    (("resin",), (40.0, 25.0, 2.0)),
    (("tpu", "tpu_95a", "tpu_85a"), (8.0, 6.0, 0.03)),
    (("hdpe",), (25.0, 15.0, 0.9)),
    (("pp", "polypropylene"), (30.0, 18.0, 1.4)),
    (("uhmw",), (20.0, 14.0, 0.7)),
    (("cf_plate", "carbon_fibre"), (500.0, 60.0, 60.0)),
    (("fr4", "g10"), (250.0, 100.0, 20.0)),
    (("aluminium", "aluminum"), (240.0, 150.0, 69.0)),
    (("steel", "304", "stainless"), (350.0, 210.0, 200.0)),
    (("hardox",), (1000.0, 600.0, 200.0)),
    (("titanium",), (830.0, 550.0, 114.0)),
    (("brass",), (200.0, 140.0, 100.0)),
    (("copper",), (70.0, 50.0, 117.0)),
]
MECH = {name: v for names, v in _MECH for name in names}
PRINTED_Z_FACTOR = 0.5  # strength across layer lines relative to in-plane


def mech(mid):
    """(yield MPa, shear MPa, E GPa) of a material, or None when unknown."""
    return MECH.get(mid) if mid else None


# ---- Process-aware manufacturability (checks/process.py) ----
# Process names in specs -> canonical process. Kerf (mm) for 2D-cut processes = minimum internal corner radius.
PROCESS_ALIASES = {
    "fdm": "fdm", "fff": "fdm", "resin": "sla", "sla": "sla", "msla": "sla",
    "sheet_cut": "sheet_cut", "laser": "sheet_cut", "waterjet": "sheet_cut", "plasma": "sheet_cut",
    "wire_edm": "sheet_cut", "router_sheet": "sheet_cut",
    "sheet_bent": "sheet_bent", "bent": "sheet_bent", "brake": "sheet_bent", "line_bent": "sheet_bent",
    "turned": "turned", "lathe": "turned", "milled": "milled", "cnc": "milled",
    "cots": "cots", "bought": "cots", "molded": "molded", "moulded": "molded", "cast": "cast",
}
KERF_MM = {"laser": 0.1, "waterjet": 0.5, "plasma": 1.0, "wire_edm": 0.15, "router_sheet": 1.5, "sheet_cut": 0.5}
MILL_MIN_TOOL_RADIUS_MM = 1.0

# Common sheet stock thicknesses (mm) per material family.
SHEET_STOCK_MM = {
    "steel": [0.5, 0.8, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0],
    "spring_steel": [0.3, 0.5, 0.8, 1.0, 1.2, 1.5, 2.0],
    "hardox": [3.0, 4.0, 5.0, 6.0, 8.0, 10.0],
    "titanium": [0.5, 0.8, 0.9, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0],  # 0.9 = 0.035 in (US Ti Gr5 sheet)
    "aluminium": [0.5, 0.8, 1.0, 1.2, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0],
    "cf_plate": [0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0],
    "polycarbonate": [0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0],
    "hdpe": [1.0, 1.5, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0],
    "uhmw": [1.0, 2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0],
    "g10": [0.5, 0.8, 1.0, 1.5, 1.6, 2.0, 3.0],
}
SHEET_FAMILY = {
    "steel": "steel", "304": "steel", "stainless": "steel", "mild_steel": "steel", "spring_steel": "spring_steel",
    "hardox": "hardox", "ar400": "hardox", "ar500": "hardox", "titanium": "titanium", "ti6al4v": "titanium",
    "aluminium": "aluminium", "aluminum": "aluminium", "cf_plate": "cf_plate", "carbon_fibre": "cf_plate",
    "pc": "polycarbonate", "polycarbonate": "polycarbonate", "hdpe": "hdpe", "uhmw": "uhmw", "fr4": "g10", "g10": "g10",
}
# Metals where a cut hole must be >= 1x thickness (others 0.5x).
HARD_SHEET = {"steel", "spring_steel", "hardox", "titanium"}
# Minimum inside bend radius as a multiple of thickness (default 1.0).
BEND_MIN_R_OVER_T = {"spring_steel": 2.0, "hardox": 3.0, "titanium": 2.5, "polycarbonate": 1.0}
# Round bar / dowel stock diameters (mm) for bought pins and shafts.
ROD_STOCK_MM = {
    "steel": [1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0],
    "titanium": [2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0],
    "aluminium": [2.0, 3.0, 4.0, 5.0, 6.0, 8.0, 10.0, 12.0],
}
# Ball bearings: designation -> (bore, OD, width) mm.
BEARINGS = {
    "684": (4.0, 9.0, 4.0), "mr84": (4.0, 8.0, 3.0), "mr104": (4.0, 10.0, 4.0), "694": (4.0, 11.0, 4.0),
    "604": (4.0, 12.0, 4.0), "683": (3.0, 7.0, 3.0), "mr63": (3.0, 6.0, 2.5), "623": (3.0, 10.0, 4.0),
    "mf85": (5.0, 8.0, 2.5), "mr85": (5.0, 8.0, 2.5), "685": (5.0, 11.0, 5.0), "mr105": (5.0, 10.0, 4.0), "625": (5.0, 16.0, 5.0), "686": (6.0, 13.0, 5.0),
    "688": (8.0, 16.0, 5.0), "608": (8.0, 22.0, 7.0),
}
# Flange OD of flanged bearings (the drawn envelope includes the flange).
BEARING_FLANGE_OD = {"mf85": 9.2, "mf63": 7.2, "mf84": 9.2, "f683": 8.1, "f684": 10.3}


def process_canon(p):
    return PROCESS_ALIASES.get(str(p).lower()) if p else None


def sheet_family(mid):
    return SHEET_FAMILY.get(str(mid).lower()) if mid else None


# Outrunner faces (kinematics checks): which end of the motor is the static stator mount and how deep that face zone is.
# "-x"/"+x" in the catalog frame (shaft stub along +X). Everything else of an outrunner's can is the rotating bell.
MOTOR_FACES = {
    "bl_1806_2300kv": {"stator_face": "-x", "depth_mm": 2.0},
    "be1806_bbb": {"stator_face": "-x", "depth_mm": 3.5},
    "gr1507": {"stator_face": "-x", "depth_mm": 2.0},
}
