"""`robot kit KIT.json OUT.json`: a LOOKS-FIRST robot from a few named numbers (no layout search, no electronics).

For matching reference photos fast: body (box or twin pods with a centre slot, front ramp), weapon (disc / drum / bar,
size, position, axis, teeth), 2 or 4 wheels, forks. Every part is a made part with real material/process, so the
`likeness` gate (template copy, type, weapon facts, silhouette) judges it. The other verifier groups WILL fail (no
motors, battery, wiring, fasteners): this is a shape draft. Start the full build from it later.

KIT.json (mm, x = across, y = forward, z = up, wheel axles at z = 0):
{"name": "...", "robot_type": "vertical_spinner",
 "body": {"length": 110, "width": 90, "height": 30, "ramp": 30, "style": "box" | "twin_pods", "slot": 30,
          "clearance": 2},
 "weapon": {"kind": "disc" | "drum" | "bar" | "none", "radius": 30, "width": 4, "y": 0, "z": 10,
            "axis": "x" | "z", "teeth": 2},
 "wheels": {"n": 2 | 4, "radius": 14, "width": 10, "y": [-25] (or [-30, 30] for 4), "outside": true},
 "forks": {"n": 2, "length": 25, "width": 6, "spread": 60}}
Shape extras (all optional):
 body.plan: "rect" | "trapezoid" | "pentagon" | "round_nose" (top-view outline; `front_width` mm for trapezoid /
   pentagon tip, `nose` mm = pentagon / round-nose length)
 "walls": {"height": 30, "thick": 2, "length": 100, "y": 0, "flare_deg": 0}  side plates / wings outside the wheels
 "shield": {"radius": 45, "thick": 3, "width": 90, "angle": 120, "y": 0, "z": 0}  arched shell over the body (about x)
 wheels.tread: true  -> a track loop (stadium) per side spanning wheels.y instead of round wheels
 weapon.kind "ring": a band ring (radius, width = band height, `thick` wall), axis z; weapon.tilt_deg tilts the weapon
   about y (angled blade); weapon.kind "bar" + `curve` mm bends the bar tips (S-blade)
 forks.tilt_deg: forks pitched down at the nose
 body.pod_nose: "round" rounds each twin pod's nose
 "legs": {"n": 2, "length": .., "width": 8, "thick": 4, "foot": 14, "y": [..]} per side: walker / shuffler, no wheels
   (locomotion "walker": 225 g non-roller limit, as AWS; set "locomotion" yourself to override)
 wheeled kits are "roller" (150 g)
`twin_pods`: two pods either side of a `slot` mm wide centre gap open at the front (centre disc / drum sits in it),
joined behind the slot.
"""

from __future__ import annotations

import json
from pathlib import Path

_COL0 = {"body": "#3a3d44", "weapon": "#d9dde2", "wheel": "#202226", "fork": "#c9cdd3"}


def _ramp_body(x0, x1, y0, y1, zb, h, ramp):
    """Side profile extruded across x: rear wall full height, top flat, then down the ramp to 1.5 mm at the nose."""
    yt = max(y0 + 1.0, y1 - ramp)
    prof = [[y0, 0.0], [y1, 0.0], [y1, 1.5], [yt, h], [y0, h]]
    w = x1 - x0
    # prism in its XY plane, extruded along local z; rot [90, 0, 90] maps local x -> world y, local y -> world z,
    # local z -> world x
    return {"type": "place", "shape": {"type": "prism", "points": prof, "height": w},
            "at": [(x0 + x1) / 2, 0.0, zb], "rot": [90.0, 0.0, 90.0]}


def _yz_prism(pts, x0, x1):
    """(y, z) outline extruded across x from x0 to x1."""
    return {"type": "place", "shape": {"type": "prism", "points": pts, "height": x1 - x0},
            "at": [(x0 + x1) / 2, 0.0, 0.0], "rot": [90.0, 0.0, 90.0]}


def _plan(b, W, y0, y1):
    """Top-view outline (x, y) for body.plan, or None for a plain rectangle."""
    import math
    plan = b.get("plan", "rect")
    fw = float(b.get("front_width", W * 0.3))
    nose = float(b.get("nose", (y1 - y0) * 0.3))
    if plan == "trapezoid":
        return [[-W / 2, y0], [W / 2, y0], [fw / 2, y1], [-fw / 2, y1]]
    if plan == "pentagon":
        return [[-W / 2, y0], [W / 2, y0], [W / 2, y1 - nose], [fw / 2, y1], [-fw / 2, y1], [-W / 2, y1 - nose]]
    if plan == "round_nose":
        n = min(nose, W / 2)
        arc = [[W / 2 * math.cos(a), y1 - n + n * math.sin(a)] for a in [math.pi * i / 16 for i in range(17)]]
        return [[-W / 2, y0], [W / 2, y0]] + arc
    return None


def _clip(shape, outline, zb, H):
    if not outline:
        return shape
    cut = {"type": "place", "shape": {"type": "prism", "points": outline, "height": H + 20},
           "at": [0.0, 0.0, zb + H / 2], "rot": [0, 0, 0]}
    return {"type": "intersect", "items": [shape, cut]}


def build(k: dict) -> dict:
    COL = {**_COL0, **(k.get("colors") or {})}
    b = k.get("body") or {}
    L, W, H = float(b.get("length", 100)), float(b.get("width", 90)), float(b.get("height", 30))
    ramp = float(b.get("ramp", 25))
    wh = k.get("wheels") or {}
    radii = wh.get("radius", 14)
    radii = [float(v) for v in radii] if isinstance(radii, list) else None
    R = max(radii) if radii else float(wh.get("radius", 14))
    zb = -R + float(b.get("clearance", 2.0))
    y0, y1 = -L / 2, L / 2
    parts = []

    def part(pid, kind, shape, mat, proc, **kw):
        parts.append({"id": pid, "kind": kind, "material": mat, "process": proc, "shape": shape,
                      "at": [0, 0, 0], "rot": [0, 0, 0], **kw})

    if b.get("style") == "twin_pods":
        slot = float(b.get("slot", 30))
        pw = (W - slot) / 2
        back = float(b.get("bridge", 25))
        for sgn, side in ((1, "l"), (-1, "r")):
            xa, xb = sorted((sgn * slot / 2, sgn * W / 2))
            pl = _plan(b, W, y0, y1)
            if b.get("pod_nose") == "round":  # each pod gets its own rounded nose
                pw2 = xb - xa
                pl = [[x + (xa + xb) / 2, y] for x, y in _plan({"plan": "round_nose", "nose": b.get("nose", pw2 / 2)},
                                                                  pw2, y0, y1)]
            part(f"pod_{side}", "structure", _clip(_ramp_body(xa, xb, y0, y1, zb, H, ramp), pl, zb, H),
                 "nylon", "fdm",
                 color=COL["body"], print_orientation="+z")
        part("bridge", "structure", {"type": "place", "shape": {"type": "box", "size": [slot + 0.2, back, H]},
                                     "at": [0, y0 + back / 2, zb + H / 2], "rot": [0, 0, 0]}, "nylon", "fdm",
             color=COL["body"], print_orientation="+z")
        xo = W / 2
    else:
        part("chassis", "structure", _clip(_ramp_body(-W / 2, W / 2, y0, y1, zb, H, ramp), _plan(b, W, y0, y1), zb, H),
             "nylon", "fdm",
             color=COL["body"], print_orientation="+z")
        xo = W / 2

    wp = k.get("weapon") or {}
    kind = wp.get("kind", "none")
    if kind in ("disc", "drum", "bar", "ring"):
        from .gen.external import spinner
        r, t = float(wp.get("radius", 25)), float(wp.get("width", 4 if kind == "disc" else 20))
        ax = "z" if kind == "ring" else wp.get("axis", "x" if kind in ("disc", "drum") else "z")
        floor = -R
        rr = r if ax == "x" else 0.0
        yw = float(wp.get("y", y1))
        zw = float(wp.get("z", floor + rr + 2.0 if ax == "x" else zb + H + t / 2))
        if ax == "x" and zw - r < floor + 0.5:
            print(f"kit: weapon z {zw:g} puts the rim {floor + 0.5 - (zw - r):.1f} mm into the floor; raised to {floor + r + 2:g}")
            zw = floor + r + 2.0
        nt = int(wp.get("teeth", 2))
        if kind == "ring":
            th = float(wp.get("thick", 4))
            shape = {"type": "subtract", "base": {"type": "cylinder", "radius": r, "height": t},
                     "cut": [{"type": "cylinder", "radius": r - th, "height": t + 2}]}
        elif kind == "bar" and float(wp.get("curve", 0)):
            bw, c = float(wp.get("bar_width", 12)), float(wp.get("curve", 0))
            # S-blade: centre hub strip + two tip pieces bent by `curve` mm (point-symmetric)
            pts = [[-r, -bw / 2 - c], [-r * 0.5, -bw / 2], [r * 0.5, -bw / 2], [r, -bw / 2 + c], [r, bw / 2 + c],
                   [r * 0.5, bw / 2], [-r * 0.5, bw / 2], [-r, bw / 2 - c]]
            shape = {"type": "prism", "points": pts, "height": t}
        elif kind == "bar":
            shape = spinner.bar_shape(2 * r, float(wp.get("bar_width", 12)), t, 0.0, [])
        else:
            shape = spinner.disc_shape(r, t, 0.0, [], teeth=nt)
        rot = [0.0, 90.0, 0.0] if ax == "x" else [0.0, float(wp.get("tilt_deg", 0)), 0.0]
        axis = [1, 0, 0] if ax == "x" else [0, 0, 1]
        part("weapon", "weapon", {"type": "place", "shape": shape, "at": [0, 0, 0], "rot": [0, 0, 0]},
             "aluminium" if kind == "drum" else "steel", "cnc" if kind == "drum" else "laser", color=COL["weapon"],
             weapon={"kind": kind, "spin_axis": [0, 0, 1], "teeth": nt, "cells": 2, "reduction": 1.0},
             joint={"kind": "revolute", "axis": axis, "pivot": [0.0, yw, zw], "min": 0, "max": 360, "default": 0})
        parts[-1]["at"], parts[-1]["rot"] = [0.0, yw, zw], rot
    elif kind in ("flipper", "lifter", "axe", "hammer"):
        import math
        ln = float(wp.get("length", L * 0.6 if kind in ("flipper", "lifter") else L * 0.7))
        wd = float(wp.get("width", W * 0.7 if kind in ("flipper", "lifter") else 10))
        th = float(wp.get("thick", 2 if kind in ("flipper", "lifter") else 4))
        py = float(wp.get("y", y0 + L * 0.3 if kind in ("flipper", "lifter") else y0 + 10))
        pz = float(wp.get("z", zb + H if kind in ("axe", "hammer") else zb + H * 0.4))
        ang = float(wp.get("angle_deg", -math.degrees(math.atan2(pz - (-R + 1), max(1.0, y1 - py)))
                                        if kind in ("flipper", "lifter") else 10.0))
        items = [{"type": "place", "shape": {"type": "box", "size": [wd, ln, th]}, "at": [0, ln / 2, 0], "rot": [0, 0, 0]}]
        hd = wp.get("head") or ([24, 8, 16] if kind == "hammer" else [4, 14, 20] if kind == "axe" else None)
        if hd:
            items.append({"type": "place", "shape": {"type": "box", "size": [float(v) for v in hd]},
                          "at": [0, ln - float(hd[1]) / 2, -float(hd[2]) / 2 + th / 2], "rot": [0, 0, 0]})
        part("weapon", "weapon", {"type": "place", "shape": {"type": "union", "items": items}, "at": [0, 0, 0],
                                  "rot": [0, 0, 0]}, "titanium" if kind in ("flipper", "lifter") else "aluminium",
             "laser", color=COL["weapon"], weapon={"kind": kind},
             joint={"kind": "revolute", "axis": [1, 0, 0], "pivot": [0.0, py, pz], "min": -10, "max": 90, "default": 0})
        parts[-1]["at"], parts[-1]["rot"] = [0.0, py, pz], [ang, 0.0, 0.0]

    lg = k.get("legs") or {}
    if lg:  # walker / shuffler: legs with foot pads instead of wheels (AWS walkers get the non-roller mass limit)
        nl, ll = int(lg.get("n", 2)), float(lg.get("length", R + zb + 6))
        lw, lt, ft = float(lg.get("width", 8)), float(lg.get("thick", 4)), float(lg.get("foot", 14))
        lys = lg.get("y") or [y0 + L * (i + 0.5) / nl for i in range(nl)]
        for i, yy in enumerate(lys):
            for sgn, side in ((1, "l"), (-1, "r")):
                xl = sgn * (W / 2 + lt / 2 + 0.5)
                leg = {"type": "union", "items": [
                    {"type": "place", "shape": {"type": "box", "size": [lt, lw, ll]}, "at": [0, 0, ll / 2], "rot": [0, 0, 0]},
                    {"type": "place", "shape": {"type": "box", "size": [ft, ft, 2.0]}, "at": [0, 0, 1.0], "rot": [0, 0, 0]}]}
                part(f"leg_{side}{i}", "structure", {"type": "place", "shape": leg, "at": [xl, float(yy), -R],
                                                     "rot": [0, 0, 0]}, "nylon", "fdm", color=COL["wheel"])
        wh = {**wh, "n": 0, "y": []}
    n = int(wh.get("n", 2))
    ww = float(wh.get("width", 10))
    ys = [] if n == 0 else (wh.get("y") or ([-L / 4] if n == 2 else [-L / 4, L / 4]))
    xw = float(wh["x"]) if wh.get("x") is not None else (xo + ww / 2 + 0.5 if wh.get("outside", True) else xo - ww / 2 - 0.5)
    i = 0
    if wh.get("tread"):
        import math
        ya, yb = min(map(float, ys)), max(map(float, ys))
        if yb - ya < 1:
            ya, yb = ya - R, yb + R
        loop = ([[yb + R * math.cos(a), R * math.sin(a)] for a in [math.pi * (i / 12 - 0.5) for i in range(13)]] +
                [[ya + R * math.cos(a), R * math.sin(a)] for a in [math.pi * (i / 12 + 0.5) for i in range(13)]])
        for sgn, side in ((1, "l"), (-1, "r")):
            part(f"tread_{side}", "wheel", _yz_prism(loop, sgn * xw - ww / 2, sgn * xw + ww / 2), "tpu", "fdm",
                 color=COL["wheel"])
        ys = []
    for yy in ys:
        Ri = radii[min(i, len(radii) - 1)] if radii else R
        for sgn, side in ((1, "l"), (-1, "r")):
            part(f"wheel_{side}{i}", "wheel", {"type": "place", "shape": {"type": "cylinder", "radius": Ri, "height": ww},
                                               "at": [0, 0, 0], "rot": [0, 90, 0]}, "tpu", "fdm", color=COL["wheel"])
            parts[-1]["at"] = [sgn * xw, float(yy), Ri - R]  # all wheels touch the floor
        i += 1

    fk = k.get("forks") or {}
    for j in range(int(fk.get("n", 0))):
        fl, fw = float(fk.get("length", 25)), float(fk.get("width", 6))
        sp = float(fk.get("spread", W * 0.6))
        x = -sp / 2 + (sp * j / max(1, int(fk["n"]) - 1) if int(fk["n"]) > 1 else sp / 2)
        part(f"fork_{j}", "wedge", {"type": "place", "shape": {"type": "box", "size": [fw, fl, 1.5]},
                                    "at": [x, y1 + fl / 2 - 2, -R + 0.8 + fl / 2 * __import__("math").sin(
                                        __import__("math").radians(float(fk.get("tilt_deg", 0))))],
                                    "rot": [-float(fk.get("tilt_deg", 0)), 0, 0]}, "titanium", "laser",
             color=COL["fork"])
    wl = k.get("walls") or {}
    if wl:
        th, wl_h = float(wl.get("thick", 2)), float(wl.get("height", H))
        wl_l, wy = float(wl.get("length", L)), float(wl.get("y", 0))
        xs = (xw + ww / 2 + 0.6 + th / 2) if wh.get("outside", True) else W / 2 + th / 2
        for sgn, side in ((1, "l"), (-1, "r")):
            part(f"wall_{side}", "structure", {"type": "place", "shape": {"type": "box", "size": [th, wl_l, wl_h]},
                                               "at": [sgn * xs, wy, -R + 1.0 + wl_h / 2],
                                               "rot": [0, 0, sgn * float(wl.get("flare_deg", 0))]},
                 "nylon", "fdm", color=COL["body"], print_orientation="+z")
    sh = k.get("shield") or {}
    if sh:
        import math
        r2, th = float(sh.get("radius", W / 2)), float(sh.get("thick", 3))
        ang = math.radians(float(sh.get("angle", 120)))
        sy, sz = float(sh.get("y", 0)), float(sh.get("z", zb))
        aa = [math.pi / 2 - ang / 2 + ang * i / 16 for i in range(17)]
        pts = ([[sy + r2 * math.cos(a), sz + r2 * math.sin(a)] for a in aa] +
               [[sy + (r2 - th) * math.cos(a), sz + (r2 - th) * math.sin(a)] for a in reversed(aa)])
        sw = float(sh.get("width", W))
        part("shield", "armor", _yz_prism(pts, -sw / 2, sw / 2), "tpu", "fdm", color=COL["body"])
    sc = k.get("scoop") or {}
    if sc:
        import math
        sw, sl = float(sc.get("width", W)), float(sc.get("length", 30))
        a, th, cv = math.radians(float(sc.get("angle", 20))), float(sc.get("thick", 1.5)), float(sc.get("curve", 0))
        ty = float(sc.get("y", y1 + sl * math.cos(a) - 2))  # nose tip y
        tz = float(sc.get("z", -R + 0.5))
        n = 12
        top = []
        for i in range(n + 1):  # from the tip back up the slope, bowed down by `curve` in the middle
            t = i / n
            top.append([ty - t * sl * math.cos(a), tz + th + t * sl * math.sin(a) - cv * 4 * t * (1 - t)])
        bot = [[y, z - th] for y, z in reversed(top)]
        part("scoop", "wedge", _yz_prism(top + bot, -sw / 2, sw / 2), "titanium", "laser", color=COL["fork"])
    for e in k.get("extras") or []:
        e = dict(e)
        e.setdefault("kind", "structure")
        e.setdefault("material", "nylon")
        e.setdefault("process", "fdm")
        e.setdefault("at", [0, 0, 0])
        e.setdefault("rot", [0, 0, 0])
        e.setdefault("color", COL["body"])
        parts.append(e)
    return {"name": k.get("name", "kit robot"), "profile": "aws2025", "robot_type": k.get("robot_type", "other"),
            "locomotion": k.get("locomotion") or ("walker" if lg else "roller"), "kit_draft": True, "parts": parts, "fasteners": [], "wires": [], "connections": [],
            **({"reference": k["reference"]} if k.get("reference") else {})}


def main(src, out):
    k = json.loads(Path(src).read_text())
    Path(out).write_text(json.dumps(build(k), indent=1))
    print(f"wrote {out}: looks draft (likeness only; other groups will fail until the full build)")
    return 0


def add_cli(sub):
    p = sub.add_parser("kit", help="looks-first robot from body/weapon/wheels/forks numbers (for photo matching)")
    p.add_argument("kit")
    p.add_argument("out")
    p.set_defaults(func=lambda a: main(a.kit, a.out))
