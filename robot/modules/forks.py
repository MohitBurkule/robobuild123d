"""Shared parametric fork set (antweight forks / wedgelets), as spec part dicts.

One generator for every robot that needs forks, so nobody hand-rolls tines again. `fork_parts(...)` returns spec part
dicts (the same JSON `robot kit` and `robot/kitparts.py` write); `ForkSet` wraps it as a `robot.modules` Module
(build123d solids) for the module registry.

Fork-set frame (mm): x across, y forward (tines point +y), z up. Origin = the hinge axis for a hinged set, or the bend
line between the flat mounting tab and the blades for a rigid set; z = 0 is the tine sheet mid-plane. The set is
mirror-symmetric about x = `x` (tines at x +- k*pitch/2); `mirror=True` emits a second, mirror-image copy at -x
(e.g. one pair either side of a centre disc), with ids `<id>_l` / `<id>_r` and the servo (if any) on the outboard side.

Styles:
  plate  every tine is its own laser-cut plate: flat mounting tab (with screw holes) bent down into the blade.
  sheet  one comb sheet: a back strip (with screw holes) carrying all the tines.

Hinge (`hinge={"pin_d": 2, "range": [-10, 30], ...}` or `hinge=True`): the tines hang from a knuckle tube (`<id>`, kind other,
revolute joint about +x through the origin, limited `range` in degrees, + = tips up) on a steel pin (`<id>_pin`, kind
pin, coaxial: the sweep checks treat it as the axle). A static mount (`<id>_mount`: two pin lugs + a vertical tab with
screw holes along y, bolted to the chassis front face) holds the pin. Plate-style tines are children of the tube
(`parent`), sheet style is one part (tube + comb). The fork group carries no `weapon` and is kind `fork`, so the
kinematics checker sweeps only the joint range (SectorSweep) - a full-turn sweep (what blocks long hinged forks
modelled as `kind: weapon` on a spinner) never happens.

Lift (`lift={"servo": "servo_cs07"}` or `lift=True`, needs a hinge): a catalog servo beside the outboard (+x, or -x for
the mirrored copy) lug with its output coaxial with the hinge, and a horn link (`<id>_horn`, child of the tube) keyed
between them, so the servo drives the forks directly. The servo body stands up (`angle` deg above backward-horizontal,
default 90), so the hinge axis must be >= ~6.5 mm above the floor (`robot kit` raises it).
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field

SERVO_OUT = (10.0, 0.0)      # catalog servo_cs07 output axis in its own frame (x, y), along local +z
SERVO_TOP = 11.35            # catalog servo_cs07 top (output) face, local z
GAP = 0.6                    # running gap between moving and static parts (> kinematics RUB_GAP other 0.5)
PIN_CLEAR = 0.1              # radial clearance pin -> bores
CORNER_R = 0.5               # laser inside-corner radius (process.geometry wants >= kerf)


def _place(shape, at=(0, 0, 0), rot=(0, 0, 0)):
    return {"type": "place", "shape": shape, "at": [float(v) for v in at], "rot": [float(v) for v in rot]}


def _box(size, at=(0, 0, 0)):
    return _place({"type": "box", "size": [float(v) for v in size]}, at)


def _cyl(r, h, at=(0, 0, 0), axis="z"):
    rot = {"x": (0, 90, 0), "y": (90, 0, 0), "z": (0, 0, 0)}[axis]
    return _place({"type": "cylinder", "radius": float(r), "height": float(h)}, at, rot)


def _blade(x, y0, length, width, taper, thick):
    """One flat tine blade (sheet frame: thickness along z) from its root at y = y0 out to the tip at y0 + length."""
    tw = max(0.5, width * taper)
    pts = [[x - width / 2, y0], [x + width / 2, y0], [x + tw / 2, y0 + length], [x - tw / 2, y0 + length]]
    return {"type": "prism", "points": pts, "height": float(thick)}


def _flat(items, cuts=(), r=CORNER_R):
    """A laser-cut sheet: union of flat items, inside corners rounded (>= kerf), then holes cut."""
    s = {"type": "round_inside", "shape": {"type": "union", "items": list(items)} if len(items) > 1 else items[0],
         "radius": float(r), "axis": "z"}
    return {"type": "subtract", "base": s, "cut": list(cuts)} if cuts else s


def tine_xs(n, pitch=None, spread=30.0, x=0.0):
    """Tine centre x positions: symmetric about x, `pitch` apart (or outer centres `spread` apart)."""
    n = int(n)
    if n <= 0:
        return []
    if n == 1:
        return [float(x)]
    p = float(pitch) if pitch is not None else float(spread) / (n - 1)
    return [float(x) + (i - (n - 1) / 2) * p for i in range(n)]


def _hole_row(n, x0, x1):
    n = int(n)
    if n <= 0:
        return []
    if n == 1:
        return [(x0 + x1) / 2]
    return [x0 + (x1 - x0) * (i + 0.5) / n for i in range(n)]


def _euler(R):
    """R (3x3 nested lists, columns = images of local x, y, z) -> spec rot [rx, ry, rz] deg (R = Rz Ry Rx)."""
    ry = -math.asin(max(-1.0, min(1.0, R[2][0])))
    rx = math.atan2(R[2][1], R[2][2])
    rz = math.atan2(R[1][0], R[0][0])
    return [round(math.degrees(a), 9) for a in (rx, ry, rz)]


def auto_tilt(drop, reach, thick):
    """Tilt (deg, tips down) that puts the blade tip's underside `drop` mm below the frame origin, blade `reach` long."""
    a = 0.0
    for _ in range(50):
        a = math.asin(max(-1.0, min(1.0, (drop - thick / 2 * math.cos(a)) / max(reach, 1e-6))))
    return math.degrees(a)


def _hinge_cfg(h):
    h = {} if h is True else dict(h)
    rng = h.get("range", [h.get("min", -10.0), h.get("max", 30.0)])
    return {"pin_d": float(h.get("pin_d", 2.0)), "wall": float(h.get("wall", 1.5)), "lug": float(h.get("lug", 3.0)),
            "min": float(min(rng)), "max": float(max(rng)), "default": float(h.get("default", 0.0)),
            "tab_h": float(h.get("tab_h", 8.0)), "tab_t": float(h.get("tab_t", 2.0)),
            "material": h.get("material", "nylon"), "process": h.get("process", "fdm")}


def _lift_cfg(lf):
    lf = {} if lf is True else dict(lf)
    return {"servo": lf.get("servo", "servo_cs07"), "angle": float(lf.get("angle", 90.0)),
            "horn_w": float(lf.get("horn_w", 2.0)), "horn_len": float(lf.get("horn_len", 8.0))}


def fork_parts(id="forks", style="plate", n=2, length=25.0, width=6.0, taper=1.0, thick=1.5, pitch=None, spread=30.0,
               tilt_deg=0.0, tab=8.0, tab_width=None, holes=1, hole_d=2.2, x=0.0, mirror=False, hinge=None, lift=None,
               material="titanium", process="laser", kind="fork", color="#c9cdd3", _side=1):
    """Fork set as spec part dicts in the fork-set frame (see module doc). Every number is a named parameter."""
    if style not in ("plate", "sheet"):
        raise ValueError(f"forks: style must be plate | sheet, got {style!r}")
    if lift and not hinge:
        raise ValueError("forks: `lift` needs a `hinge` (the servo turns the hinge)")
    if mirror:
        kw = dict(style=style, n=n, length=length, width=width, taper=taper, thick=thick, pitch=pitch, spread=spread,
                  tilt_deg=tilt_deg, tab=tab, tab_width=tab_width, holes=holes, hole_d=hole_d, hinge=hinge, lift=lift,
                  material=material, process=process, kind=kind, color=color)
        xa = abs(float(x))
        return fork_parts(f"{id}_l", x=xa, **kw) + fork_parts(f"{id}_r", x=-xa, _side=-1, **kw)
    xs = tine_xs(n, pitch, spread, x)
    if not xs:
        return []
    t, w, tilt = float(thick), float(width), float(tilt_deg)
    tw = float(tab_width) if tab_width is not None else w
    hd = float(hole_d)
    mat = {"material": material, "process": process, "color": color}
    span = (max(xs) - min(xs)) + max(w, tw)          # across all tines (+ tab margin)
    rest = (-tilt, 0, 0)                             # flat sheet pitched tips-down about the frame x axis
    if not hinge:
        if style == "plate":
            out = []
            for j, xj in enumerate(xs):
                tabp = _box([tw, tab + 0.2, t], (xj, -tab / 2 + 0.1, 0))
                cuts = [_cyl(hd / 2, t + 2, (xj, hy, 0)) for hy in _hole_row(holes, -tab, 0.0)]
                shape = _flat([tabp, _blade(xj, 0.0, length, w, taper, t)], cuts)
                out.append(_part(f"{id}_{j}", kind, shape, rot=rest, label="fork tine with mounting tab", **mat))
            return out
        strip = _box([span, tab + 0.2, t], (x, -tab / 2 + 0.1, 0))
        nh = int(holes) if holes is not None else len(xs) + 1
        cuts = [_cyl(hd / 2, t + 2, (hx, -tab / 2, 0)) for hx in _hole_row(max(nh, 0), x - span / 2, x + span / 2)]
        shape = _flat([strip] + [_blade(xj, 0.0, length, w, taper, t) for xj in xs], cuts)
        return [_part(id, kind, shape, rot=rest, label="fork comb sheet with mounting strip", **mat)]

    # ---- hinged --------------------------------------------------------------------------------------------------
    h = _hinge_cfg(hinge)
    rp = h["pin_d"] / 2
    rb = rp + PIN_CLEAR + h["wall"]                  # knuckle tube radius
    bw = span                                        # tube length
    y0 = math.sqrt(max(rb * rb - (t / 2) ** 2, 0.0))  # blade root where the sheet meets the tube surface
    bore = _cyl(rp + PIN_CLEAR, bw + 2, (x, 0, 0), "x")
    tube = _cyl(rb, bw, (x, 0, 0), "x")
    joint = {"kind": "revolute", "axis": [1.0, 0.0, 0.0], "pivot": [float(x), 0.0, 0.0], "min": h["min"],
             "max": h["max"], "default": h["default"]}
    out = []
    mk = "other"   # moving parts: kind `fork` is a static kind to the kinematics checker (kin.rigid_mix)
    mat = {**mat, "rotates_with": id}
    root = _part(id, mk, {"type": "subtract", "base": tube, "cut": [bore]}, rot=(-tilt, 0, 0), joint=joint,
                 material="steel", process="cnc", color=color, rotates_with=id,
                 label="fork hinge knuckle tube the tines bolt to")
    out.append(root)
    if style == "sheet":
        sd_ = min(3.0, length / 2)
        comb = _flat([_box([bw, sd_, t], (x, y0 + sd_ / 2, 0))] +       # starts on the tube surface, no overlap
                     [_blade(xj, y0 + sd_ - 0.2, length - sd_ + 0.2, w, taper, t) for xj in xs])
        out.append(_part(f"{id}_sheet", mk, comb, parent=id, label="fork comb sheet", **mat))
    else:
        for j, xj in enumerate(xs):
            out.append(_part(f"{id}_{j}", mk, _blade(xj, y0, length, w, taper, t), parent=id, label="fork tine", **mat))
    # static mount: two pin lugs + a vertical tab (screw holes along y) behind the tube
    lw = h["lug"]
    xl = [x - bw / 2 - GAP - lw / 2, x + bw / 2 + GAP + lw / 2]
    tab_y1 = -(rb + GAP)                              # tab front face (clear of the tube)
    tab_y0 = tab_y1 - h["tab_t"]
    zt0, zt1 = -rb, -rb + max(h["tab_h"], 2 * rb)
    items = [_box([xl[1] - xl[0] + lw, h["tab_t"], zt1 - zt0], (x, (tab_y0 + tab_y1) / 2, (zt0 + zt1) / 2))]
    for xx in xl:
        items.append(_box([lw, rb - tab_y0, 2 * rb], (xx, (rb + tab_y0) / 2, 0)))
    cuts = [_cyl(rp + PIN_CLEAR, bw + 2 * lw + 4, (x, 0, 0), "x")]
    zh = (zt0 + zt1) / 2 + rb / 2
    cuts += [_cyl(hd / 2, h["tab_t"] + 2, (hx, (tab_y0 + tab_y1) / 2, zh), "y")
             for hx in _hole_row(max(int(holes) if holes is not None else 2, 2), xl[0], xl[1])]
    out.append(_part(f"{id}_mount", "plate", {"type": "subtract", "base": {"type": "union", "items": items}, "cut": cuts},
                     material=h["material"], process=h["process"], color=color,
                     **({"print_orientation": "+z"} if h["process"] == "fdm" else {}),
                     label="hinge mount: pin lugs + tab bolted to the chassis front"))
    sd = 1.0 if _side >= 0 else -1.0
    out_x = x + sd * (bw / 2 + GAP + lw)              # outboard lug face (the servo side)
    in_x = x - sd * (bw / 2 + GAP + lw)
    pin_x1 = out_x
    if lift:
        lc = _lift_cfg(lift)
        hx0, hx1 = sorted((out_x + sd * GAP, out_x + sd * (GAP + lc["horn_w"])))
        horn = {"type": "union", "items": [_cyl(rb + 1.0, lc["horn_w"], ((hx0 + hx1) / 2, 0, 0), "x"),
                                           _box([lc["horn_w"], lc["horn_len"], 2.0], ((hx0 + hx1) / 2, lc["horn_len"] / 2, 0))]}
        horn = {"type": "subtract", "base": horn, "cut": [_cyl(rp + PIN_CLEAR, lc["horn_w"] + 2, ((hx0 + hx1) / 2, 0, 0), "x")]}
        out.append(_part(f"{id}_horn", "other", horn, parent=id, material="nylon", process="fdm", color="#202226",
                         rotates_with=id, print_orientation="+x",
                         label="servo horn link keyed to the hinge tube"))
        out.append(_servo(f"{id}_servo", lc, (hx1 if sd > 0 else hx0) + sd * GAP, side=sd))
        root["actuated_by"] = f"{id}_servo"
        pin_x1 = hx1 if sd > 0 else hx0
    pin_x0, pin_x1 = sorted((in_x, pin_x1))
    out.append(_part(f"{id}_pin", "pin", _cyl(rp, pin_x1 - pin_x0, ((pin_x0 + pin_x1) / 2, 0, 0), "x"),
                     material="steel", process="cots", stock=f"M{h['pin_d']:g} dowel", color="#9aa0a6",
                     label="hinge pin (axle)"))
    return out


def _servo(pid, lc, face_x, side=1):
    """Catalog servo with its output coaxial with the hinge (x axis), top face at x = face_x, facing the forks."""
    from robot import catalog
    if catalog.find(lc["servo"]) is None:
        raise ValueError(f"forks: unknown servo `{lc['servo']}` (see `robot catalog`)")
    b = math.radians(lc["angle"])
    e = (0.0, -math.cos(b), math.sin(b))          # body direction from the output (backward-up)
    u = tuple(-c for c in e)                       # local +x
    wv = (-float(side), 0.0, 0.0)                  # local +z (output) points back toward the forks
    v = (wv[1] * u[2] - wv[2] * u[1], wv[2] * u[0] - wv[0] * u[2], wv[0] * u[1] - wv[1] * u[0])  # z x x = y
    R = [[u[i], v[i], wv[i]] for i in range(3)]
    ox, oy = SERVO_OUT
    at = [face_x + side * SERVO_TOP - (u[0] * ox + v[0] * oy), -(u[1] * ox + v[1] * oy), -(u[2] * ox + v[2] * oy)]
    return {"id": pid, "kind": "servo", "catalog": lc["servo"], "at": [round(a, 9) for a in at], "rot": _euler(R),
            "label": "lift servo, output coaxial with the fork hinge"}


def _part(pid, kind, shape, at=(0, 0, 0), rot=(0, 0, 0), **kw):
    return {"id": pid, "kind": kind, "shape": shape, "at": [float(v) for v in at], "rot": [float(v) for v in rot],
            **{k: v for k, v in kw.items() if v is not None}}


def translate(parts, d):
    """Move a fork set's parts (frame origin -> d): root parts' `at` and joint pivots; children stay parent-relative."""
    out = []
    for p in parts:
        p = dict(p)
        if not p.get("parent"):
            p["at"] = [a + float(b) for a, b in zip(p["at"], d)]
            if p.get("joint"):
                j = dict(p["joint"])
                j["pivot"] = [a + float(b) for a, b in zip(j["pivot"], d)]
                p["joint"] = j
        out.append(p)
    return out


def from_kit(fk: dict, nose_y: float, floor_z: float, body_bottom: float, body_width: float) -> list:
    """`robot kit` forks with a `style`: place the set at the body nose with tips on the floor (tilt auto unless given)."""
    fk = dict(fk)
    fk.pop("style_note", None)
    gap = float(fk.get("tip_gap", 0.3))              # tip underside above the floor (ground.wedge_gap: 0.2-1.5)
    p = {k: v for k, v in fk.items() if k not in ("y", "z", "pitch_deg", "spread", "range", "tip_gap")}
    p.setdefault("n", 2)
    p.setdefault("length", 25.0)
    p.setdefault("width", 6.0)
    p.setdefault("thick", 1.5)
    if fk.get("pitch") is None:
        p["spread"] = float(fk.get("spread", body_width * 0.6))
    if "pitch_deg" in fk and "tilt_deg" not in fk:
        p["tilt_deg"] = float(fk["pitch_deg"])
    if p.pop("hinged", False) and not p.get("hinge"):
        p["hinge"] = True
    if fk.get("range") is not None and p.get("hinge"):
        p["hinge"] = {**({} if p["hinge"] is True else p["hinge"]), "range": fk["range"]}
    t, L = float(p["thick"]), float(p["length"])
    if p.get("hinge"):
        h = _hinge_cfg(p["hinge"])
        rb = h["pin_d"] / 2 + PIN_CLEAR + h["wall"]
        z = float(fk.get("z", floor_z + rb + 0.5))
        if p.get("lift") and fk.get("z") is None:
            z = max(z, floor_z + 6.6)
        y = float(fk.get("y", nose_y + rb + GAP + h["tab_t"]))
        reach = math.sqrt(max(rb * rb - (t / 2) ** 2, 0.0)) + L
    else:
        z = float(fk.get("z", min(body_bottom - 0.1 - t / 2, floor_z + gap + t / 2 + 1.0)))
        y = float(fk.get("y", nose_y))
        reach = L
    if "tilt_deg" not in p:
        p["tilt_deg"] = max(0.0, auto_tilt(z - floor_z - gap, reach, t))
    return translate(fork_parts(**p), (0.0, y, z))


@dataclass
class ForkSet:
    """Module wrapper: the same fork set as build123d solids (module frame = fork-set frame)."""
    name: str = "forks"
    params: dict = field(default_factory=dict)

    def parts(self) -> list:
        return fork_parts(id=self.name, **self.params)

    def build(self):
        from build123d import Location
        from robot import shapes, xform
        from robot.modules.base import ModuleResult, Mount
        ps = self.parts()
        by = {p["id"]: p for p in ps}
        solids = {}
        for p in ps:
            if not p.get("shape"):
                continue
            M = xform.pose(p["at"], p["rot"])
            if p.get("parent") in by:
                M = xform.pose(by[p["parent"]]["at"], by[p["parent"]]["rot"]) @ M
            solids[p["id"]] = shapes.place(shapes.to_solid(p["shape"], "."), M)
        mounts = {"nose": Mount("nose", Location((0, 0, 0)), kind="revolute" if self.params.get("hinge") else "rigid")}
        return ModuleResult(self.name, solids, mounts, bom=[p["catalog"] for p in ps if p.get("catalog")])
