"""Shared parametric parts for `robot kit` (and anything else that writes spec parts).

One function per part family, registered with @part. Each takes `id` plus named parameters (all with defaults) and
returns a list of spec part dicts in the part's own frame (placed later by the kit `use` entry's `at` / `rot`).
Use from kit.json:

  "use": [{"part": "drive_pod", "id": "drive", "at": [0, -25, 0], "mirror": "x", "wheel_r": 14, "motor": "bbb_n20_600rpm"},
          {"part": "electronics", "id": "elec", "at": [0, 5, -6]}]

`mirror: "x"` places a second copy at -x (ids get _l / _r). `robot kit --parts` lists every part and its parameters;
robot/KITPARTS.md is the same list. Fasteners are not parts: add them to the spec's `fasteners` list
(`robot fasteners SPEC --fill` measures grip and picks lengths). To add a part: write a function here with @part, keep every number a named
parameter with a sensible default (from the catalog where a real component exists), add it to a test.
Axes: x across, y forward, z up. Wheel / motor axles run along x. Catalog components are real COTS parts
(`robot catalog`), so mass, ports and fasteners come from the catalog, not guesses.
"""

from __future__ import annotations

import inspect
import math

LIB: dict = {}


def part(fn):
    LIB[fn.__name__] = fn
    return fn


def _p(pid, kind, shape=None, at=(0, 0, 0), rot=(0, 0, 0), **kw):
    d = {"id": pid, "kind": kind, "at": [float(v) for v in at], "rot": [float(v) for v in rot], **kw}
    if shape is not None:
        d["shape"] = shape
    return d


def _cyl_x(r, w):
    return {"type": "place", "shape": {"type": "cylinder", "radius": r, "height": w}, "at": [0, 0, 0], "rot": [0, 90, 0]}


def _cat(pid, cid, at=(0, 0, 0), rot=(0, 0, 0)):
    from . import catalog
    c = catalog.find(cid)
    if c is None:
        raise ValueError(f"kitparts: unknown catalog id `{cid}` (see `robot catalog`)")
    return _p(pid, c.kind, None, at, rot, catalog=cid)


# ---- wheels -------------------------------------------------------------------------------------------------------

@part
def wheel(id="wheel", radius=14.0, width=10.0, hub=10.0, color="#202226"):
    """Plain printed wheel: TPU tyre on a hub, axle along x."""
    tyre = {"type": "subtract", "base": _cyl_x(radius, width), "cut": [_cyl_x(hub / 2 - 0.5, width + 2)]}
    hubs = {"type": "subtract", "base": _cyl_x(hub / 2, width), "cut": [_cyl_x(1.5, width + 2)]}
    return [_p(id, "wheel", {"type": "union", "items": [tyre, hubs]}, material="tpu", process="fdm", color=color)]


@part
def omni_wheel(id="omni", radius=14.0, width=8.0, rollers=8, roller_r=3.0, color="#202226"):
    """Omni wheel: hub disc + `rollers` free rollers round the rim, axles tangential. Axle along x."""
    hub = _cyl_x(radius - roller_r, width * 0.6)
    items = [hub]
    rc = radius - roller_r
    rl = 2 * rc * math.tan(math.pi / rollers) * 0.9
    for i in range(int(rollers)):
        a = 360.0 * i / rollers
        y, z = rc * math.cos(math.radians(a)), rc * math.sin(math.radians(a))
        items.append({"type": "place", "shape": {"type": "cylinder", "radius": roller_r, "height": rl},
                      "at": [0, y, z], "rot": [a + 90, 0, 0]})
    return [_p(id, "wheel", {"type": "union", "items": items}, material="tpu", process="fdm", color=color)]


# ---- drive --------------------------------------------------------------------------------------------------------

@part
def drive_motor(id="motor", motor="bbb_n20_600rpm"):
    """Catalog drive gearmotor, output shaft toward +x."""
    return [_cat(id, motor)]


@part
def drive_pod(id="drive", motor="bbb_n20_600rpm", wheel_r=14.0, wheel_w=10.0, omni=False, gap=0.5):
    """One wheel + its gearmotor on one axle. Origin = wheel centre; the motor sits inboard (-x), shaft into the wheel.
    Use `mirror: "x"` for the other side (the mirrored copy points its shaft the other way)."""
    from . import catalog
    c = catalog.find(motor)
    if c is None:
        raise ValueError(f"kitparts: unknown motor `{motor}`")
    shaft = (c.shaft or {}).get("at", [18.0, 0, 0])[0]
    w = (omni_wheel if omni else wheel)(f"{id}_wheel", radius=wheel_r, width=wheel_w)
    m = _cat(f"{id}_motor", motor, at=(-wheel_w / 2 - gap - shaft, 0, 0))
    return w + [m]


# ---- electronics --------------------------------------------------------------------------------------------------

@part
def electronics(id="elec", battery="lipo_2s_180", esc="bbb_malenki_nano", receiver="rx_fs_ia6_decased",
                switch="switch_slide_bbb_ant", gap=2.0, along="y"):
    """Battery, ESC, receiver and switch in a row (catalog parts), centred on the origin, packed along `along`."""
    from . import catalog
    ids = [("battery", battery), ("esc", esc), ("rx", receiver), ("switch", switch)]
    sizes = []
    for _, cid in ids:
        c = catalog.find(cid)
        if c is None:
            raise ValueError(f"kitparts: unknown catalog id `{cid}`")
        sizes.append(_bbox(c.shape))
    k = 1 if along == "y" else 0
    total = sum(s[k] for s in sizes) + gap * (len(sizes) - 1)
    pos, out = -total / 2, []
    for (n, cid), s in zip(ids, sizes):
        c = pos + s[k] / 2
        out.append(_cat(f"{id}_{n}", cid, at=(0, c, 0) if k else (c, 0, 0)))
        pos += s[k] + gap
    return out


def _bbox(shape):
    try:
        from . import shapes
        bb = shapes.to_solid(shape, ".").bounding_box()
        return [bb.size.X, bb.size.Y, bb.size.Z]
    except Exception:  # noqa: BLE001
        return [20.0, 20.0, 10.0]


# ---- weapons ------------------------------------------------------------------------------------------------------

@part
def weapon_motor(id="wmotor", motor="be1806_bbb"):
    """Catalog brushless weapon motor, shaft toward +x."""
    return [_cat(id, motor)]


@part
def hinged_arm(id="arm", length=50.0, width=40.0, thick=2.0, head=None, kind="flipper", material="titanium"):
    """Flipper / lifter / axe / hammer arm. Origin = hinge (axis x), arm runs +y. head [x, y, z] box at the tip."""
    items = [{"type": "place", "shape": {"type": "box", "size": [width, length, thick]}, "at": [0, length / 2, 0],
              "rot": [0, 0, 0]}]
    if head:
        items.append({"type": "place", "shape": {"type": "box", "size": [float(v) for v in head]},
                      "at": [0, length - float(head[1]) / 2, -float(head[2]) / 2 + thick / 2], "rot": [0, 0, 0]})
    return [_p(id, "weapon", {"type": "union", "items": items}, material=material, process="laser",
               weapon={"kind": kind},
               joint={"kind": "revolute", "axis": [1, 0, 0], "pivot": [0, 0, 0], "min": -10, "max": 90, "default": 0})]


@part
def spinner_disc(id="disc", radius=30.0, thick=4.0, teeth=2, kind="disc", axis="x", material="steel"):
    """Disc / drum / bar spinner from robot.gen.external.spinner, spinning about `axis` (x = vertical spinner)."""
    from .gen.external import spinner
    if kind == "bar":
        shape = spinner.bar_shape(2 * radius, 12.0, thick, 0.0, [])
    else:
        shape = spinner.disc_shape(radius, thick, 0.0, [], teeth=int(teeth))
    rot = [0, 90, 0] if axis == "x" else [0, 0, 0]
    ax = [1, 0, 0] if axis == "x" else [0, 0, 1]
    return [_p(id, "weapon", {"type": "place", "shape": shape, "at": [0, 0, 0], "rot": rot}, material=material,
               process="laser", weapon={"kind": kind, "spin_axis": [0, 0, 1], "teeth": int(teeth)},
               joint={"kind": "revolute", "axis": ax, "pivot": [0, 0, 0], "min": 0, "max": 360, "default": 0})]


@part
def fork_set(id="forks", style="plate", n=2, length=25.0, width=6.0, taper=1.0, thick=1.5, pitch=None, spread=30.0,
             tilt_deg=0.0, tab=8.0, tab_width=None, holes=1, hole_d=2.2, x=0.0, mirror=False, hinge=None, lift=None,
             material="titanium", process="laser"):
    """Fork set (robot/modules/forks.py): `n` tines `length` x `width` (tip = width*taper), `thick` sheet, `pitch` mm
    apart (or outer centres `spread` apart), pitched `tilt_deg` down; style plate (own tab per tine) | sheet (one comb).
    Origin = hinge axis / tab bend line, tines +y. hinge {pin_d, range: [min, max], tab_h} adds pin, lugs + mount tab;
    lift {servo, angle} adds a coaxial servo + horn link. Symmetric about `x`; `mirror` (here or in the use entry)
    adds the mirror-image set at -x.
    Parts: rigid plate -> `<id>_<j>` (kind fork, tab with `holes` x `hole_d` screw holes); rigid sheet -> `<id>`;
    hinged -> `<id>` knuckle tube (revolute about +x, joint `range` deg, + = tips up), `<id>_<j>` tines or `<id>_sheet`
    (children, kind other), `<id>_mount` (lugs + tab with screw holes), `<id>_pin` (kind pin); lift adds `<id>_horn`
    and `<id>_servo`. Hinged parts are kind other with no `weapon`, so the kinematics checker sweeps only the joint
    range: long hinged forks on a spinner are not swept through a full circle (what blocks `kind: weapon` forks).
    In kit.json the same set is `"forks": {"style": "plate" | "sheet", ...}` (placed at the nose, tips on the floor)."""
    from .modules import forks
    return forks.fork_parts(id=id, style=style, n=n, length=length, width=width, taper=taper, thick=thick, pitch=pitch,
                            spread=spread, tilt_deg=tilt_deg, tab=tab, tab_width=tab_width, holes=holes, hole_d=hole_d,
                            x=x, mirror=mirror, hinge=hinge, lift=lift, material=material, process=process)


fork_set.own_mirror = True  # mirror: "x" = mirror-image copy at -x (not the 180 deg turn drive pods use)


# ---- placing ------------------------------------------------------------------------------------------------------

def _place(p, at, rot, mx=False):
    """Compose a part's own at/rot under the use entry's placement (rot about z only is composed exactly; full rot
    is applied by wrapping the part's shape). A part with a `parent` stays in its parent's frame (it follows it)."""
    p = dict(p)
    if p.get("parent"):
        return p
    a = [float(v) for v in p.get("at", [0, 0, 0])]
    if mx:
        a[0] = -a[0]
        p["rot"] = [p["rot"][0], p["rot"][1], (p["rot"][2] + 180.0) % 360.0]
        if p.get("joint"):
            j = dict(p["joint"])
            j["pivot"] = [-j["pivot"][0], j["pivot"][1], j["pivot"][2]]
            p["joint"] = j
    rz = math.radians(float(rot[2]))
    x, y = a[0] * math.cos(rz) - a[1] * math.sin(rz), a[0] * math.sin(rz) + a[1] * math.cos(rz)
    p["at"] = [x + float(at[0]), y + float(at[1]), a[2] + float(at[2])]
    p["rot"] = [p["rot"][0] + float(rot[0]), p["rot"][1] + float(rot[1]), p["rot"][2] + float(rot[2])]
    if p.get("joint"):
        j = dict(p["joint"])
        pv = j["pivot"]
        j["pivot"] = [pv[0] * math.cos(rz) - pv[1] * math.sin(rz) + float(at[0]),
                      pv[0] * math.sin(rz) + pv[1] * math.cos(rz) + float(at[1]), pv[2] + float(at[2])]
        p["joint"] = j
    return p


def expand(use: list) -> list:
    """kit.json `use` entries -> spec parts."""
    out = []
    for u in use or []:
        u = dict(u)
        name = u.pop("part")
        if name not in LIB:
            raise ValueError(f"kit use: unknown part `{name}`; known: {', '.join(sorted(LIB))}")
        at, rot, mir = u.pop("at", [0, 0, 0]), u.pop("rot", [0, 0, 0]), u.pop("mirror", None)
        pid = u.pop("id", name)
        if mir == "x" and getattr(LIB[name], "own_mirror", False):
            u.update(mirror=True, x=float(u.get("x", 0.0)) + float(at[0]))
            out += [_place(p, [0.0, at[1], at[2]], rot) for p in LIB[name](id=pid, **u)]
        elif mir == "x":
            for side, mx in (("l", False), ("r", True)):
                out += [_place(p, [(-1 if mx else 1) * float(at[0]), at[1], at[2]], rot, mx)
                        for p in LIB[name](id=f"{pid}_{side}", **u)]
        else:
            out += [_place(p, at, rot) for p in LIB[name](id=pid, **u)]
    return out


def describe() -> str:
    rows = ["# Shared kit parts (`use` in kit.json)", "",
            "Generated from robot/kitparts.py (`robot kit --parts`). Add a part there with @part; every number a named "
            "parameter.", ""]
    for n, fn in sorted(LIB.items()):
        sig = ", ".join(f"{k}={v.default!r}" for k, v in inspect.signature(fn).parameters.items() if k != "id")
        rows += [f"## {n}", "", (fn.__doc__ or "").strip(), "", f"`{sig}`", ""]
    return "\n".join(rows)
