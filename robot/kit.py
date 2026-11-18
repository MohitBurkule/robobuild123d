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
`twin_pods`: two pods either side of a `slot` mm wide centre gap open at the front (centre disc / drum sits in it),
joined behind the slot.
"""

from __future__ import annotations

import json
from pathlib import Path

COL = {"body": "#3a3d44", "weapon": "#d9dde2", "wheel": "#202226", "fork": "#c9cdd3"}


def _ramp_body(x0, x1, y0, y1, zb, h, ramp):
    """Side profile extruded across x: rear wall full height, top flat, then down the ramp to 1.5 mm at the nose."""
    yt = max(y0 + 1.0, y1 - ramp)
    prof = [[y0, 0.0], [y1, 0.0], [y1, 1.5], [yt, h], [y0, h]]
    w = x1 - x0
    # prism in its XY plane, extruded along local z; rot [90, 0, 90] maps local x -> world y, local y -> world z,
    # local z -> world x
    return {"type": "place", "shape": {"type": "prism", "points": prof, "height": w},
            "at": [(x0 + x1) / 2, 0.0, zb], "rot": [90.0, 0.0, 90.0]}


def build(k: dict) -> dict:
    b = k.get("body") or {}
    L, W, H = float(b.get("length", 100)), float(b.get("width", 90)), float(b.get("height", 30))
    ramp = float(b.get("ramp", 25))
    wh = k.get("wheels") or {}
    R = float(wh.get("radius", 14))
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
            part(f"pod_{side}", "structure", _ramp_body(xa, xb, y0, y1, zb, H, ramp), "nylon", "fdm",
                 color=COL["body"], print_orientation="+z")
        part("bridge", "structure", {"type": "place", "shape": {"type": "box", "size": [slot + 0.2, back, H]},
                                     "at": [0, y0 + back / 2, zb + H / 2], "rot": [0, 0, 0]}, "nylon", "fdm",
             color=COL["body"], print_orientation="+z")
        xo = W / 2
    else:
        part("chassis", "structure", _ramp_body(-W / 2, W / 2, y0, y1, zb, H, ramp), "nylon", "fdm",
             color=COL["body"], print_orientation="+z")
        xo = W / 2

    wp = k.get("weapon") or {}
    kind = wp.get("kind", "none")
    if kind in ("disc", "drum", "bar"):
        from .gen.external import spinner
        r, t = float(wp.get("radius", 25)), float(wp.get("width", 4 if kind == "disc" else 20))
        ax = wp.get("axis", "x" if kind in ("disc", "drum") else "z")
        floor = -R
        rr = r if ax == "x" else 0.0
        yw = float(wp.get("y", y1))
        zw = float(wp.get("z", floor + rr + 2.0 if ax == "x" else zb + H + t / 2))
        if ax == "x" and zw - r < floor + 0.5:
            print(f"kit: weapon z {zw:g} puts the rim {floor + 0.5 - (zw - r):.1f} mm into the floor; raised to {floor + r + 2:g}")
            zw = floor + r + 2.0
        nt = int(wp.get("teeth", 2))
        if kind == "bar":
            shape = spinner.bar_shape(2 * r, float(wp.get("bar_width", 12)), t, 0.0, [])
        else:
            shape = spinner.disc_shape(r, t, 0.0, [], teeth=nt)
        rot = [0.0, 90.0, 0.0] if ax == "x" else [0.0, 0.0, 0.0]
        axis = [1, 0, 0] if ax == "x" else [0, 0, 1]
        part("weapon", "weapon", {"type": "place", "shape": shape, "at": [0, 0, 0], "rot": [0, 0, 0]},
             "aluminium" if kind == "drum" else "steel", "cnc" if kind == "drum" else "laser", color=COL["weapon"],
             weapon={"kind": kind, "spin_axis": [0, 0, 1], "teeth": nt, "cells": 2, "reduction": 1.0},
             joint={"kind": "revolute", "axis": axis, "pivot": [0.0, yw, zw], "min": 0, "max": 360, "default": 0})
        parts[-1]["at"], parts[-1]["rot"] = [0.0, yw, zw], rot

    n = int(wh.get("n", 2))
    ww = float(wh.get("width", 10))
    ys = wh.get("y") or ([-L / 4] if n == 2 else [-L / 4, L / 4])
    xw = xo + ww / 2 + 0.5 if wh.get("outside", True) else xo - ww / 2 - 0.5
    i = 0
    for yy in ys:
        for sgn, side in ((1, "l"), (-1, "r")):
            part(f"wheel_{side}{i}", "wheel", {"type": "place", "shape": {"type": "cylinder", "radius": R, "height": ww},
                                               "at": [0, 0, 0], "rot": [0, 90, 0]}, "tpu", "fdm", color=COL["wheel"])
            parts[-1]["at"] = [sgn * xw, float(yy), 0.0]
        i += 1

    fk = k.get("forks") or {}
    for j in range(int(fk.get("n", 0))):
        fl, fw = float(fk.get("length", 25)), float(fk.get("width", 6))
        sp = float(fk.get("spread", W * 0.6))
        x = -sp / 2 + (sp * j / max(1, int(fk["n"]) - 1) if int(fk["n"]) > 1 else sp / 2)
        part(f"fork_{j}", "wedge", {"type": "place", "shape": {"type": "box", "size": [fw, fl, 1.5]},
                                    "at": [x, y1 + fl / 2 - 2, -R + 0.8], "rot": [0, 0, 0]}, "titanium", "laser",
             color=COL["fork"])
    return {"name": k.get("name", "kit robot"), "profile": "aws2025", "robot_type": k.get("robot_type", "other"),
            "locomotion": "wheels", "kit_draft": True, "parts": parts, "fasteners": [], "wires": [], "connections": [],
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
