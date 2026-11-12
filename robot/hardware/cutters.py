"""Hole cutters sized from robot.hardware.features. Each builder returns (cutter_solid, record_dict).

Frame, same as robot.cad.holes: `at` is the point on the part surface where the feature starts, `axis` points into
the material (the way a screw travels). Locally z = 0 is the surface and +z goes into the part; every cutter also
pokes `lead` mm out of the surface so the boolean leaves no skin. Subtract the cutter: `part - cutter`.

`comp` (features.PrintComp) adds the FDM hole offset; leave it None for nominal (metal / measured) geometry.
The record dict lists every dimension used, so checks can compare it with the measured geometry.
"""

from __future__ import annotations

import math

import numpy as np

from . import features as ft
from . import registry as reg
from .solids import cone, cyl, hex_prism, square_prism

BIG = 1000.0


def _place(solid, at, axis):
    import build123d as bd

    a = np.asarray(axis, float)
    a = a / np.linalg.norm(a)
    loc = bd.Location(bd.Plane(origin=tuple(map(float, at)), z_dir=tuple(map(float, a))))
    return loc * solid


def _off(comp):
    return comp.hole_offset if comp else 0.0


def _union(parts):
    out = parts[0]
    for p in parts[1:]:
        out = out + p
    return out


def _done(tools, at, axis, kind, **info):
    rec = {"kind": kind, "at": tuple(map(float, at)), "axis": tuple(map(float, axis))}
    rec.update({k: (round(v, 4) if isinstance(v, float) else v) for k, v in info.items()})
    return _place(_union(tools), at, axis), rec


def clearance(at, axis, d: float, depth: float = BIG, fit: str = "normal", comp=None, lead: float = 0.5):
    c = ft.clearance(d, fit).value + _off(comp)
    return _done([cyl(c / 2, -lead, depth)], at, axis, "clearance", d=d, fit=fit, hole_d=c, depth=depth,
                 src=ft.ISO_273_SRC)


def tapped(at, axis, d: float, depth: float, material: str | None = None, comp=None, lead: float = 0.5):
    """Tap-drill hole (metal, material=None) or thread-forming pilot in a plastic (material='PLA', ...)."""
    dim = ft.pilot(d, material) if material else ft.tap_drill(d)
    h = dim.value + _off(comp)
    eng = ft.engagement_min(d, material or "steel").value
    return _done([cyl(h / 2, -lead, depth)], at, axis, "tapped", d=d, hole_d=h, depth=depth, material=material,
                 engagement_min=eng, engagement_ok=depth >= eng, src=dim.src, uncertain=dim.uncertain)


def insert(at, axis, d: float, maker: str | None = None, length: float | None = None, comp=None,
           through_d: float | None = None, lead: float = 0.5):
    """Heat-set insert bore; optional screw clearance continuing below it (through_d, e.g. tip relief)."""
    b = ft.insert_bore(d, maker, length, comp=comp)
    tools = [cyl(b.d / 2, -lead, b.depth)]
    if through_d:
        tools.append(cyl(through_d / 2, b.depth - 0.01, BIG))
    return _done(tools, at, axis, "insert", d=d, hole_d=b.d, depth=b.depth, insert_len=b.insert_length,
                 insert_od=b.od, wall_min=b.wall_min, src=b.src, uncertain=b.uncertain)


def nut_trap(at, axis, d: float, z0: float, family: str = "hex", fit: str = "press", entry: str = "axial",
             angle: float = 0.0, fit_bolt: str = "normal", comp=None, lead: float = 0.5):
    """Bolt clearance from the surface, nut pocket from depth z0. entry='axial' opens the pocket out of the far side
    (pocket to BIG); entry='side' slot along local +x for sliding the nut in."""
    t = ft.nut_trap(d, family, fit, comp=comp)
    c = ft.clearance(d, fit_bolt).value + _off(comp)
    tools = [cyl(c / 2, -lead, BIG)]
    z1 = BIG if entry == "axial" else z0 + t.depth
    if family == "square":
        tools.append(square_prism(t.af, z0, z1))
    else:
        tools.append(hex_prism(t.af, z0, z1, angle))
    if entry == "side":
        import build123d as bd

        tools.append(bd.Pos(BIG / 2, 0, z0) * bd.Box(BIG, t.af, t.depth,
                                                      align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN)))
    elif entry != "axial":
        raise ValueError(f"entry must be axial | side, not `{entry}`")
    return _done(tools, at, axis, "nut_trap", d=d, nut=family, nut_std=t.standard, nut_af=t.nut_af, nut_m=t.nut_m,
                 pocket_af=t.af, pocket_depth=t.depth, nut_z=z0, entry=entry, clearance_d=c)


def countersunk(at, axis, d: float, depth: float = BIG, standard: str | None = None, sink: float = 0.0,
                fit: str = "normal", head_clear: float = 10.0, comp=None):
    """Flush csk head (top at z = sink), cone to the clearance hole, clearance to `depth`."""
    k = ft.countersink(d, standard, fit)
    top = k.d + _off(comp)
    c = k.clearance_d + _off(comp)
    h = (top - c) / 2 / math.tan(math.radians(k.angle / 2))
    tools = [cyl(top / 2, -head_clear, sink + 0.001), cone(top / 2, c / 2, sink, sink + h), cyl(c / 2, sink, depth)]
    return _done(tools, at, axis, "countersink", d=d, csk_d=top, csk_angle=k.angle, csk_depth=h, sink=sink,
                 clearance_d=c, depth=depth, src=k.src, uncertain=k.uncertain)


def counterbored(at, axis, d: float, depth: float = BIG, family: str = "cap", standard: str | None = None,
                 sink: float = 0.0, fit: str = "normal", head_clear: float = 10.0, comp=None):
    """Counterbore (DIN 974-1 for cap heads) to k + sink deep, then clearance."""
    cb = ft.counterbore(d, family, standard, sink)
    D = cb.d + _off(comp)
    c = ft.clearance(d, fit).value + _off(comp)
    tools = [cyl(D / 2, -head_clear, cb.depth), cyl(c / 2, cb.depth - 0.01, depth)]
    return _done(tools, at, axis, "counterbore", d=d, cbore_d=D, cbore_depth=cb.depth, clearance_d=c, depth=depth,
                 src=cb.src, uncertain=cb.uncertain)


def bearing_seat(at, axis, designation: str, fit: str = "press", depth: float | None = None,
                 shoulder_d: float | None = None, comp=None, lead: float = 0.5):
    """Blind pocket for a bearing OD, depth B (default); a shoulder hole (default between d and D, clear of the inner
    ring) continues through so the inner ring can turn."""
    b = reg.get(designation).record
    D = ft.bearing_seat(designation, fit, comp).value
    dep = b.B if depth is None else depth
    sh = shoulder_d if shoulder_d is not None else (b.d + b.D) / 2
    tools = [cyl(D / 2, -lead, dep)]
    if sh > 0:
        tools.append(cyl(sh / 2, dep - 0.01, BIG))
    return _done(tools, at, axis, "bearing_seat", designation=b.designation, seat_d=D, depth=dep, shoulder_d=sh,
                 fit=fit, bearing_D=b.D, bearing_B=b.B, uncertain=True)


def dowel(at, axis, d: float, depth: float, fit: str = "press", comp=None, lead: float = 0.5):
    h = ft.dowel_hole(d, fit, comp)
    return _done([cyl(h.value / 2, -lead, depth)], at, axis, "dowel", d=d, hole_d=h.value, depth=depth, fit=fit,
                 src=h.src, uncertain=h.uncertain)


def oring_groove(at, axis, designation: str, style: str = "face", seal_d: float | None = None):
    """O-ring gland. style 'face': annular groove in the surface, inner diameter = ring ID (seal_d overrides).
    'shaft': groove round a shaft of diameter seal_d (default ID + 2*depth, i.e. ring stretched onto groove bottom
    = ID). 'bore': groove in a bore of diameter seal_d (default ID + 2 cs)."""
    w, dep, unc = ft.oring_groove(designation)
    o = reg.get(designation if designation.lower().startswith("o") else f"oring {designation}").record
    if style == "face":
        ri = (seal_d if seal_d is not None else o.id) / 2
        tools = [cyl(ri + w, -0.5, dep) - cyl(ri, -1.0, dep + 1.0)]
        info = dict(groove_id=2 * ri, groove_od=2 * (ri + w), depth=dep)
    elif style == "shaft":
        sd = seal_d if seal_d is not None else o.id + 2 * dep
        tools = [cyl(sd / 2 + 1.0, -w / 2, w / 2) - cyl(sd / 2 - dep, -w, w)]
        info = dict(shaft_d=sd, groove_bottom_d=sd - 2 * dep, width=w)
    elif style == "bore":
        bd_ = seal_d if seal_d is not None else o.id + 2 * o.cs
        tools = [cyl(bd_ / 2 + dep, -w / 2, w / 2)]
        info = dict(bore_d=bd_, groove_bottom_d=bd_ + 2 * dep, width=w)
    else:
        raise ValueError(f"style must be face | shaft | bore, not `{style}`")
    return _done(tools, at, axis, "oring_groove", designation=o.designation, style=style, groove_w=w,
                 groove_depth=dep, uncertain=unc, **info)


def circlip_groove(at, axis, designation: str):
    """Groove for a retaining ring, centred on z = 0 (place `at` at the groove centre on the shaft/bore axis).
    External: annulus from groove_d out past the shaft; internal: annulus from the bore out to groove_d."""
    c = reg.get(designation).record
    w = c.groove_w
    if c.family.startswith("int"):
        tools = [cyl(c.groove_d / 2, -w / 2, w / 2)]
    else:
        tools = [cyl(c.shaft_d / 2 + 1.0, -w / 2, w / 2) - cyl(c.groove_d / 2, -w, w)]
    return _done(tools, at, axis, "circlip_groove", designation=f"{c.standard} {c.shaft_d:g}", groove_d=c.groove_d,
                 groove_w=w, src=c.src.standard)
