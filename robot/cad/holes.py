"""Fastener holes cut from the catalog: one call gives the right clearance, head recess, thread bore or nut pocket.

    from robot.cad.holes import hole
    plate, rec = hole(plate, at=(10, 5, 3), axis=(0, 0, -1), fastener="M2x6", head="csk", into="tapped", grip=3)
    spec["fasteners"].append(rec.to_spec("bolt_a", through=["plate"], threads_into="tub"))

Frame: `at` is the point on the part surface where the hole starts (part frame); `axis` points the way the screw
travels (head -> tip). Along the axis, z = 0 is that surface:

  head  csk:    90 deg cone, dk (catalog) at z = -sink -> flush head when sink = 0; free cylinder above it
        cap/button: counterbore dk + cbore_clear wide, `cbore` deep (cap default: k, i.e. flush; button: 0)
  shank clearance (ISO 273) from the head seat to `grip` (thickness of the clamped part)
  into  through: clearance all the way; tapped: tap drill from grip to the tip (+0.5);
        insert: heat-set insert bore from grip, insert length + 0.3; nut: hex/thin nut pocket at grip (+nut_offset),
        across flats + 0.05 (press) or + 0.3 (drop-in), open out of the far face when nut_entry="axial"
  side  "both" (default) cuts all of it in this part; "head" only the head recess + clearance through the part;
        "thread" only the threaded side, starting at `at` (the joint face of the host).

The returned FastenerRecord carries the spec entry (bearing point `at`, `dir`, `head`, designation) and a `hole` dict
with every dimension used, which `robot.checks.fastener_seat` compares with the real geometry.
"""

from __future__ import annotations

import math
from dataclasses import dataclass, field

import numpy as np

from . import fastener_catalog as fc

BIG = 1000.0  # "through everything" length


@dataclass
class FastenerRecord:
    designation: str
    at: tuple  # bearing point (where the spec's fastener `at` goes), part frame
    dir: tuple
    head: str  # csk | button | cap
    into: str
    hole: dict = field(default_factory=dict)

    def placed(self, M) -> "FastenerRecord":
        """The record moved by a 4x4 part->world transform."""
        M = np.asarray(M, float)
        at = M[:3, :3] @ np.asarray(self.at, float) + M[:3, 3]
        d = M[:3, :3] @ np.asarray(self.dir, float)
        return FastenerRecord(self.designation, tuple(map(float, at)), tuple(map(float, d / np.linalg.norm(d))),
                              self.head, self.into, dict(self.hole))

    def to_spec(self, id: str, through=(), threads_into=None, tool=None, M=None, **extra) -> dict:
        """A `fasteners[]` entry for the spec (world frame if M is given)."""
        r = self.placed(M) if M is not None else self
        out = {"id": id, "designation": r.designation, "at": [round(x, 4) for x in r.at],
               "dir": [round(x, 6) for x in r.dir], "through": list(through), "threads_into": threads_into,
               "head": fc.SPEC_HEAD[r.head], "hole": dict(r.hole)}
        if tool:
            out["tool"] = tool
        out.update(extra)
        return out


def _frame(at, axis):
    import build123d as bd

    a = np.asarray(axis, float)
    a = a / np.linalg.norm(a)
    return bd.Location(bd.Plane(origin=tuple(map(float, at)), z_dir=tuple(map(float, a)))), a


def _cyl(r, z0, z1):
    import build123d as bd

    return bd.Pos(0, 0, z0) * bd.Cylinder(r, z1 - z0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def _cone(r0, r1, z0, z1):
    import build123d as bd

    return bd.Pos(0, 0, z0) * bd.Cone(r0, r1, z1 - z0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def _hex(s, z0, z1, angle=0.0):
    import build123d as bd

    r = s / math.sqrt(3.0)  # circumradius from across flats
    sk = bd.Sketch() + bd.RegularPolygon(r, 6, rotation=angle)
    return bd.Pos(0, 0, z0) * bd.extrude(sk, z1 - z0)


def hole_tool(at, axis, fastener="M2x6", head="cap", into="tapped", grip=None, side="both", fit="normal",
              sink=0.0, cbore=None, cbore_clear=0.4, csk_clear=0.3, csk_angle=90.0, head_clear=10.0,
              nut="hex", nut_fit="press", nut_offset=0.0, nut_entry="axial", nut_angle=0.0, engage=None):
    """The cutter solid (part frame) and the FastenerRecord, without cutting anything. See module doc for arguments."""
    if into not in ("through", "tapped", "insert", "nut"):
        raise ValueError(f"into must be through | tapped | insert | nut, not `{into}`")
    if side not in ("both", "head", "thread"):
        raise ValueError(f"side must be both | head | thread, not `{side}`")
    s = fc.parse(fastener)
    d, L = s.d, s.length
    dk, k = fc.head(d, head)
    loc, a = _frame(at, axis)
    c = fc.clearance(d, fit)
    info = {"d": d, "length": L, "head": head, "head_std": fc.head_standard(d, head), "head_dk": dk, "head_k": k,
            "clearance_d": c, "into": into, "side": side}
    tools = []
    # z of the head bearing face (where the spec `at` sits)
    if side == "thread":
        seat = 0.0
        grip = 0.0
    elif head == "csk":
        seat = float(sink)
        r0 = dk / 2 + csk_clear / 2
        h = (r0 - c / 2) / math.tan(math.radians(csk_angle / 2))
        tools += [_cyl(r0, -head_clear, seat), _cone(r0, c / 2, seat, seat + h)]
        info.update(csk_angle=csk_angle, csk_d=2 * r0, csk_depth=round(h, 4), sink=seat)
    else:
        cb = (k if head == "cap" else 0.0) if cbore is None else float(cbore)
        seat = cb
        tools.append(_cyl(dk / 2 + cbore_clear / 2, -head_clear, seat))
        info.update(cbore_d=dk + cbore_clear, cbore_depth=cb)
    # tip: the ISO length of a countersunk screw is overall (head included); the others are measured under the head
    # screw tip: ISO length is overall for csk (seat = top of head) and under the head otherwise (seat = bearing face).
    # On the thread side alone the screw enters at the joint face, `engage` mm deep (default: the full length).
    tip = (float(engage) if engage is not None else L) if side == "thread" else seat + L
    g = BIG if grip is None else float(grip)
    if side == "head":
        tools.append(_cyl(c / 2, seat - 0.01, BIG if grip is None else g + 0.01))
        info["grip"] = grip
    else:
        g = float(grip or 0.0) if side == "both" else 0.0
        if g > 0:
            tools.append(_cyl(c / 2, seat - 0.01, g + 0.01))
        info["grip"] = g
        if into == "through":
            tools.append(_cyl(c / 2, g, BIG))
        elif into == "tapped":
            td = fc.tap_drill(d)
            tools.append(_cyl(td / 2, g, tip + 0.5))
            info.update(tap_d=td, thread_depth=round(tip + 0.5 - g, 4))
        elif into == "insert":
            ib, il = fc.insert(d)
            tools.append(_cyl(ib / 2, g, g + il + 0.3))
            if tip + 0.5 > g + il + 0.3:
                tools.append(_cyl(c / 2, g + il, tip + 0.5))
            info.update(insert_d=ib, insert_len=il, insert_depth=round(il + 0.3, 4))
        else:
            sf, m = fc.nut(d, nut)
            s_cut = sf + (0.05 if nut_fit == "press" else 0.3)
            z0 = g + nut_offset
            z1 = BIG if nut_entry == "axial" else z0 + m + (0.0 if nut_fit == "press" else 0.2)
            tools += [_cyl(c / 2, g, BIG if nut_entry == "axial" else tip + 0.5), _hex(s_cut, z0, z1, nut_angle)]
            info.update(nut=nut, nut_std=fc.NUTS[nut][1], nut_af=sf, nut_m=m, nut_pocket_af=s_cut, nut_z=z0,
                        nut_fit=nut_fit, nut_entry=nut_entry)
    cutter = tools[0]
    for t in tools[1:]:
        cutter = cutter + t
    cutter = loc * cutter
    bear = np.asarray(at, float) + a * seat
    rec = FastenerRecord(s.designation, tuple(map(float, bear)), tuple(map(float, a)), head, into,
                         {k2: (round(v, 4) if isinstance(v, float) else v) for k2, v in info.items()})
    return cutter, rec


def hole(part, at, axis, fastener="M2x6", head="cap", into="tapped", **kw):
    """Cut a catalog-sized fastener hole into `part` (a build123d solid/Part). Returns (new_part, FastenerRecord)."""
    cutter, rec = hole_tool(at, axis, fastener, head, into, **kw)
    return part - cutter, rec
