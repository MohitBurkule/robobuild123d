"""build123d solids for standard hardware, with the features that matter for fit checks.

Frame (every function): the part axis is +Z. Screws: z = 0 is the head bearing face (csk: the top of the head, which
is flush with the surface), the shank runs to -Z. Nuts, washers, bearings, standoffs, dowels: sit on z = 0, extend to
+Z. Inserts: top at z = 0, body to -Z (as pressed into a surface). Approximations are noted per function; threads are
not modelled (shank = nominal d, nut/insert bore = thread minor diameter).

    from robot.hardware import solids
    s = solids.screw("M3x10 ISO 4762")
"""

from __future__ import annotations

import math

from . import registry as reg


def _bd():
    import build123d as bd

    return bd


def cyl(r: float, z0: float, z1: float):
    """Cylinder radius r on the Z axis from z0 to z1."""
    bd = _bd()
    return bd.Pos(0, 0, z0) * bd.Cylinder(r, z1 - z0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def cone(r0: float, r1: float, z0: float, z1: float):
    """Frustum, radius r0 at z0 and r1 at z1 (z1 > z0)."""
    bd = _bd()
    return bd.Pos(0, 0, z0) * bd.Cone(r0, r1, z1 - z0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def hex_prism(af: float, z0: float, z1: float, angle: float = 0.0):
    """Hexagonal prism, across flats `af`, from z0 to z1."""
    bd = _bd()
    sk = bd.Sketch() + bd.RegularPolygon(af / math.sqrt(3.0), 6, rotation=angle)
    return bd.Pos(0, 0, z0) * bd.extrude(sk, z1 - z0)


def square_prism(af: float, z0: float, z1: float):
    bd = _bd()
    return bd.Pos(0, 0, z0) * bd.Box(af, af, z1 - z0, align=(bd.Align.CENTER, bd.Align.CENTER, bd.Align.MIN))


def ring(r_in: float, r_out: float, z0: float, z1: float):
    return cyl(r_out, z0, z1) - cyl(r_in, z0 - 0.01, z1 + 0.01)


def _part(x, kind):
    p = x if isinstance(x, reg.Part) else reg.get(x)
    if p.kind != kind:
        raise ValueError(f"`{p.designation}` is a {p.kind}, not a {kind}")
    return p


def _minor(d):
    try:
        return reg.thread(d).d_minor_ext
    except ValueError:
        return 0.85 * d  # approximate when the thread table lacks the size


def _recess(rec, z_top):
    """Drive recess cut down from z_top: hex socket (AF s, depth t); other drives a round pocket (approximation)."""
    if rec.drive == "none" or not rec.t:
        return None
    if rec.drive == "hex" and rec.s:
        return hex_prism(rec.s, z_top - rec.t, z_top + 0.01)
    r = min(0.3 * rec.dk, 0.45 * rec.d + 0.4)  # torx/phillips/slot: round pocket of similar size
    return cyl(r, z_top - rec.t, z_top + 0.01)


# ---------------------------------------------------------------------------------------------- screws
def screw(designation, length: float | None = None):
    """Screw solid. Lengths: under the head (csk: overall, per ISO). Button head is a frustum (approximate dome)."""
    p = _part(designation, "screw")
    r = p.record
    L = float(length if length is not None else (p.length or (r.lengths[len(r.lengths) // 2] if r.lengths else 3 * r.d)))
    fam = r.family
    if fam == "csk":
        ang = r.csk_angle or 90.0
        r_bot = max(r.d / 2, r.dk / 2 - r.k * math.tan(math.radians(ang / 2)))
        body = cone(r_bot, r.dk / 2, -r.k, 0.0) + cyl(r.d / 2, -L, -r.k + 0.01)
        top = 0.0
    elif fam.startswith("grub"):
        body = cyl(r.d / 2, -L, 0.0)
        top = 0.0
    else:
        if fam == "button":
            head = cone(r.dk / 2, r.dk * 0.3, 0.0, r.k)
        else:
            head = cyl(r.dk / 2, 0.0, r.k)
        body = head + cyl(r.d / 2, -L, 0.01)
        top = r.k
    rc = _recess(r, top)
    return body - rc if rc is not None else body


# ---------------------------------------------------------------------------------------------- nuts, washers
def nut(designation):
    """Hex nut with 30 deg chamfer on both faces (bearing circle = AF); square nut is a plain box; nyloc height m."""
    p = _part(designation, "nut")
    n = p.record
    if n.family == "square":
        body = square_prism(n.s, 0.0, n.m)
    else:
        body = hex_prism(n.s, 0.0, n.m)
        grow = n.m / math.tan(math.radians(30.0))
        r0 = n.s / 2
        body = body & cone(r0, r0 + grow, 0.0, n.m) & cone(r0 + grow, r0, 0.0, n.m)
    return body - cyl(_minor(n.d) / 2, -0.01, n.m + 0.01)


def washer(designation):
    w = _part(designation, "washer").record
    return ring(w.d1 / 2, w.d2 / 2, 0.0, w.h)


def insert(designation):
    """Heat-set insert: knurl approximated as a plain cylinder of the knurl OD; bore = thread minor."""
    i = _part(designation, "insert").record
    return ring(_minor(i.d) / 2, i.od / 2, -i.length, 0.0)


def standoff(designation):
    """Hex standoff, threaded holes (tap drill) from both ends (female) or a male stud (mf) on top."""
    p = _part(designation, "standoff")
    s = p.record
    body = hex_prism(s.af, 0.0, s.length)
    td = _minor(s.d)
    depth = min(s.length / 2 - 0.2, 2.0 * s.d) if s.family == "ff" else min(s.length - 0.5, 2.0 * s.d)
    body = body - cyl(td / 2, -0.01, depth)
    if s.family == "ff":
        body = body - cyl(td / 2, s.length - depth, s.length + 0.01)
    else:
        body = body + cyl(s.d / 2, s.length - 0.01, s.length + (s.male_len or s.d * 2))
    return body


# ---------------------------------------------------------------------------------------------- rotating, pins
def bearing(designation):
    """Deep-groove bearing: inner and outer rings (each 30% of the radial section) plus a shield annulus 0.2 mm
    inset from each face standing in for balls/cage/shields; flange on the outer ring at the top (z = B)."""
    b = _part(designation, "bearing").record
    sec = (b.D - b.d) / 2
    ri, ro = b.d / 2 + 0.3 * sec, b.D / 2 - 0.3 * sec
    s = ring(b.d / 2, ri, 0.0, b.B) + ring(ro, b.D / 2, 0.0, b.B) + ring(ri - 0.01, ro + 0.01, 0.2, b.B - 0.2)
    if b.flange_D and b.flange_B:
        s = s + ring(ro, b.flange_D / 2, b.B - b.flange_B, b.B)
    return s


def dowel(designation, length: float | None = None):
    """Dowel / spring pin, chamfered both ends (chamfer from the record, else 0.1 d). Spring pins modelled solid."""
    p = _part(designation, "pin")
    r = p.record
    L = float(length if length is not None else p.length)
    c = r.chamfer if r.chamfer else 0.1 * r.d
    c = min(c, L / 4, r.d / 4)
    return cone(r.d / 2 - c, r.d / 2, 0.0, c) + cyl(r.d / 2, c - 0.01, L - c + 0.01) + cone(r.d / 2, r.d / 2 - c, L - c, L)


def circlip(designation):
    """Retaining ring as a plain flat annulus at the groove: external sits on groove_d, internal inside groove_d.
    Radial band = 0.15 x size + 0.4 (approximation; real clips are tapered with lugs)."""
    c = _part(designation, "circlip").record
    band = 0.15 * c.shaft_d + 0.4
    if c.family.startswith("int"):
        return ring(c.groove_d / 2 - band, c.groove_d / 2, 0.0, c.thickness)
    return ring(c.groove_d / 2, c.groove_d / 2 + band, 0.0, c.thickness)


def oring(designation):
    """O-ring torus, centre plane z = cs/2 so it sits on z = 0."""
    bd = _bd()
    o = _part(designation if str(designation).lower().startswith("o") or isinstance(designation, reg.Part)
              else f"oring {designation}", "oring").record
    return bd.Pos(0, 0, o.cs / 2) * bd.Torus((o.id + o.cs) / 2, o.cs / 2)


def make(designation, **kw):
    """Any kind: dispatch on the resolved Part's kind."""
    p = designation if isinstance(designation, reg.Part) else reg.get(designation)
    fn = {"screw": screw, "nut": nut, "washer": washer, "insert": insert, "standoff": standoff, "bearing": bearing,
          "pin": dowel, "circlip": circlip, "oring": oring}.get(p.kind)
    if fn is None:
        raise ValueError(f"no solid builder for kind `{p.kind}`")
    return fn(p, **kw)
