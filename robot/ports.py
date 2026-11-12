"""Typed port contracts for COTS catalogue parts (ROADMAP R1). UNTESTED: written without running.

A port is what a part offers to its neighbours: mount bolt pattern, envelope, shaft, bore, lead exit, connector.
`iface(cid)` turns a catalogue id into a frozen per-kind Iface, or raises PortError naming the missing fields
(never KeyError/TypeError). `compatible(a, b)` lists Mismatch rows so a swap becomes "declared unfit, because ..."
instead of an OCP crash deep in a builder.

Frames follow catalog.py: shaft/axle along local +X, out of the +X end; packs long side on X; connectors mate on +X.
Data comes only from robot.cots_alts tables and robot.catalog built-ins; no number is invented here except the
documented defaults in DEFAULTS (fit clearances), each named.
"""
from __future__ import annotations

import math
from dataclasses import dataclass, field, fields

# Named fit defaults (mm). Only relations, no vendor numbers.
DEFAULTS = dict(
    shaft_bore_clr=0.05,     # max diametral slop allowed between a shaft and a bore it drives
    shaft_bore_max_gap=0.3,  # bore bigger than shaft by more than this = loose / needs adaptor
    min_wall=0.8,            # printed wall between bore and seat
)


class PortError(ValueError):
    def __init__(self, kind, cid, missing=(), why=""):
        self.kind, self.cid, self.missing, self.why = kind, cid, list(missing), why
        super().__init__(f"{kind} '{cid}': " + (f"missing {self.missing}" if self.missing else "") + (f" {why}" if why else ""))


@dataclass(frozen=True)
class Mismatch:
    port: str
    field: str
    have: object
    need: object
    why: str = ""


# ------------------------------------------------------------------------------------------------- port types
@dataclass(frozen=True)
class BoltPattern:
    """Holes on a pitch circle (pcd) or a rectangle (dx, dy) in the mount face, normal = insertion direction."""
    n: int
    hole_d: float
    pcd: float | None = None
    dx: float | None = None
    dy: float | None = None
    phase_deg: float = 0.0
    thread: str | None = None          # "M2", "M1.6", ... (tapped in the part); None = clearance holes
    face: str = "-X"                   # which local face the holes are in

    def points(self):
        if self.pcd:
            return [(self.pcd / 2 * math.cos(math.radians(self.phase_deg + 360.0 * i / self.n)),
                     self.pcd / 2 * math.sin(math.radians(self.phase_deg + 360.0 * i / self.n))) for i in range(self.n)]
        if self.dx is not None and self.n == 2:
            return [(-self.dx / 2, 0.0), (self.dx / 2, 0.0)]
        if self.dx is not None and self.dy is not None and self.n == 4:
            return [(sx * self.dx / 2, sy * self.dy / 2) for sx in (-1, 1) for sy in (-1, 1)]
        return []


@dataclass(frozen=True)
class Shaft:
    d: float
    length: float
    flat: float | None = None           # across-flat for D shafts; None = round
    at_x: float = 0.0                   # shaft root along local X
    dir: tuple = (1.0, 0.0, 0.0)


@dataclass(frozen=True)
class Bore:
    d: float
    flat: float | None = None
    depth: float | None = None


@dataclass(frozen=True)
class Envelope:
    """Axis-aligned keep-out box in the part frame (lx along X)."""
    lx: float
    ly: float
    lz: float
    round_d: float | None = None        # cylindrical body dia, if the body is round about X

    def fits_in(self, other: "Envelope", clr=0.0):
        return all(a + clr <= b for a, b in zip(sorted((self.lx, self.ly, self.lz)), sorted((other.lx, other.ly, other.lz))))


@dataclass(frozen=True)
class LeadExit:
    face: str                           # "+Y", "-X", "radial" ...
    length: float | None = None
    bend_r: float | None = None


@dataclass(frozen=True)
class Connector:
    family: str                         # "xt30", "jst_ph", "jst_rcy", "bt20"
    gender: str | None = None
    rated_a: float | None = None
    envelope: Envelope | None = None
    mate_dir: tuple = (1.0, 0.0, 0.0)


# ---------------------------------------------------------------------------------------------- per-kind ifaces
@dataclass(frozen=True)
class Iface:
    cid: str
    kind: str
    envelope: Envelope
    mass_g: float | None = None
    insert_dir: tuple = (0.0, 0.0, -1.0)   # direction the part moves to seat in its bay (assembly frame default: top-down)


@dataclass(frozen=True)
class GearmotorIface(Iface):
    shaft: Shaft | None = None
    mount: BoltPattern | None = None
    gearbox: Envelope | None = None
    leads: LeadExit | None = None
    rpm: float | None = None
    stall_a: float | None = None


@dataclass(frozen=True)
class OutrunnerIface(Iface):
    shaft: Shaft | None = None
    base_mount: tuple = ()                  # tuple[BoltPattern]
    top_mount: tuple = ()
    bell_d: float | None = None
    leads: LeadExit | None = None
    kv: float | None = None


@dataclass(frozen=True)
class WheelIface(Iface):
    od: float = 0.0
    width: float = 0.0
    bore: Bore | None = None
    own_hub: bool = True                    # COTS wheel ships with its hub: no printed hub needed
    rim_r: float | None = None              # tyre inner radius (= hub seat radius)
    boss_d: float | None = None
    boss_len: float = 0.0


@dataclass(frozen=True)
class PackIface(Iface):
    cells: int = 0
    mah: float = 0.0
    c: float = 0.0
    connector: Connector | None = None
    leads: LeadExit | None = None


@dataclass(frozen=True)
class EscIface(Iface):
    channels: int = 0
    cont_a: float = 0.0
    max_cells: int = 0
    pads: dict = field(default_factory=dict)   # name -> (x, y, z)


@dataclass(frozen=True)
class SwitchIface(Iface):
    mount: BoltPattern | None = None
    rated_a: float = 0.0
    actuator_d: float | None = None
    actuator_dir: tuple = (0.0, 0.0, 1.0)


KIND_IFACE = {"drive_motor": GearmotorIface, "motor": GearmotorIface, "weapon_motor": OutrunnerIface, "wheel": WheelIface,
              "battery": PackIface, "esc": EscIface, "switch": SwitchIface}


# --------------------------------------------------------------------------------------------- table -> iface
def _need(kind, cid, row, keys):
    miss = [k for k in keys if row.get(k) is None]
    if miss:
        raise PortError(kind, cid, miss)


def _weapon(cid, r):
    _need("weapon_motor", cid, r, ["bell_d", "body_len", "shaft_d"])
    pats = lambda hs: tuple(BoltPattern(n=h[1], hole_d=h[2], pcd=h[0], phase_deg=(h[3] if len(h) > 3 else 45.0), thread=f"M{h[2]:g}")
                            for h in hs or [])
    out = r.get("overall", r["body_len"]) - r["body_len"]
    return OutrunnerIface(cid, "weapon_motor", Envelope(r.get("overall", r["body_len"]), r["bell_d"], r["bell_d"], round_d=r["bell_d"]),
                          r.get("mass_g"), shaft=Shaft(r["shaft_d"], out, at_x=r["body_len"]),
                          base_mount=pats(r.get("base_holes")), top_mount=pats(r.get("top_holes")), bell_d=r["bell_d"],
                          leads=LeadExit("radial", r.get("wires_mm")), kv=r.get("kv"))


def _gear(cid, r, f):
    _need("drive_motor", cid, r, ["gb_len", "shaft_len"])
    if r.get("can_len") is None and r.get("overall") is None:
        raise PortError("drive_motor", cid, ["can_len|overall"])
    body = r.get("overall", r.get("can_len", 0) + r["gb_len"] + f["tab_len"] + r["shaft_len"]) - r["shaft_len"]
    return GearmotorIface(cid, "drive_motor", Envelope(body + r["shaft_len"], f["gb_w"], f["gb_h"]), r.get("mass_g"),
                          shaft=Shaft(f["shaft_d"], r["shaft_len"], flat=f["shaft_flat"], at_x=body),
                          mount=BoltPattern(n=2, hole_d=f["hole_d"], dx=2 * f["hole_dx"], thread=f"M{f['hole_d']:g}", face="+X"),
                          gearbox=Envelope(r["gb_len"], f["gb_w"], f["gb_h"]), leads=LeadExit("-X"),
                          rpm=r.get("rpm_nominal"), stall_a=r.get("stall_current_a"))


def _pack(cid, r, conns):
    _need("battery", cid, r, ["l", "w", "h", "cells", "mah"])
    fam = r.get("conn") or ""
    c = next((v for k, v in conns.items() if k.startswith(fam.split("_")[0])), None) if fam else None
    con = Connector(fam, None, c.get("rated_a") if c else None, Envelope(c["l"], c["w"], c["h"]) if c else None) if fam else None
    return PackIface(cid, "battery", Envelope(r["l"], r["w"], r["h"]), r.get("mass_g"), cells=int(r["cells"]), mah=r["mah"],
                     c=r.get("c") or 0.0, connector=con, leads=LeadExit("+Y"))


def _esc(cid, r):
    _need("esc", cid, r, ["l", "w", "h"])
    p = r.get("props", {})
    return EscIface(cid, "esc", Envelope(r["l"], r["w"], r["h"]), r.get("mass_g"), channels=int(p.get("channels", 0)),
                    cont_a=p.get("cont_current_a", 0.0), max_cells=int(p.get("max_cells", 0)),
                    pads={k: tuple(v) for k, v in (r.get("ports") or {}).items()})


def _switch(cid, r):
    _need("switch", cid, r, ["body", "hole_pitch", "hole_d"])
    bx, by, bz = r["body"]
    return SwitchIface(cid, "switch", Envelope(bx, by, bz), r.get("mass_g"),
                       mount=BoltPattern(n=2, hole_d=r["hole_d"], dx=r["hole_pitch"], face="-Z"),
                       rated_a=r.get("rated_a") or 0.0, actuator_d=r.get("screw_d"))


def _wheel(cid, r):
    _need("wheel", cid, r, ["od", "width", "bore"])
    tt = r.get("tyre_t")
    return WheelIface(cid, "wheel", Envelope(r["width"], r["od"], r["od"], round_d=r["od"]), r.get("mass_g"),
                      insert_dir=(-1.0, 0.0, 0.0), od=r["od"], width=r["width"], bore=Bore(r["bore"], r.get("d_flat")),
                      own_hub=True, rim_r=(r["od"] / 2 - tt) if tt else None, boss_d=r.get("hub_boss_d"), boss_len=r.get("boss_len") or 0.0)


def _from_entry(cid, e):
    """Fallback for catalog.py built-ins (CatalogEntry): shaft + props only, envelope from props when present."""
    kind, p, s = e.kind, e.props or {}, e.shaft or {}
    if kind == "wheel":
        if "diameter_mm" not in p or "width_mm" not in p:
            raise PortError("wheel", cid, [k for k in ("diameter_mm", "width_mm") if k not in p])
        od, w = p["diameter_mm"], p["width_mm"]
        return WheelIface(cid, "wheel", Envelope(w, od, od, round_d=od), e.mass_g, insert_dir=(-1.0, 0.0, 0.0), od=od, width=w,
                          bore=Bore(s.get("dia", 0.0)) if s else None, own_hub=False)
    if kind in ("motor", "weapon_motor"):
        if not s:
            raise PortError(kind, cid, ["shaft"])
        sh = Shaft(s["dia"], s["len"], at_x=s["at"][0])
        env = Envelope(2 * abs(s["at"][0]) + s["len"], 0.0, 0.0)
        cls = GearmotorIface if kind == "motor" else OutrunnerIface
        return cls(cid, "drive_motor" if kind == "motor" else kind, env, e.mass_g, shaft=sh)
    raise PortError(kind, cid, why="no port mapping for this built-in kind")


def _tables():
    from robot import cots_alts as ca
    res = getattr(ca, "_resolve", lambda t: t)
    return ca, res


def iface(cid: str) -> Iface:
    """Typed iface for a catalogue id. Raises PortError (never KeyError/TypeError)."""
    try:
        ca, res = _tables()
        for table, fn in ((ca.WEAPON_MOTORS, _weapon), (ca.GEARMOTORS, lambda c, r: _gear(c, r, ca.GEARMOTOR_FORMAT)),
                          (ca.BATTERIES, lambda c, r: _pack(c, r, ca.CONNECTORS)), (ca.ESCS, _esc), (ca.SWITCHES, _switch)):
            if cid in table:
                return fn(cid, res(table)[cid])
        if cid in ca.WHEELS:
            row = dict(ca.WHEEL_DEFAULTS)
            row.update(res(ca.WHEELS)[cid])
            return _wheel(cid, row)
        from robot import catalog
        return _from_entry(cid, catalog.find(cid))
    except PortError:
        raise
    except (KeyError, TypeError, AttributeError, LookupError) as ex:
        raise PortError("unknown", cid, why=f"{type(ex).__name__}: {ex}") from None


def missing_fields(i: Iface) -> list[str]:
    """Port fields left None on an iface (what a builder may not rely on)."""
    return [f.name for f in fields(i) if getattr(i, f.name) is None]


# ------------------------------------------------------------------------------------------------ compatibility
def shaft_bore(shaft: Shaft, bore: Bore, port="shaft/bore", c=DEFAULTS) -> list[Mismatch]:
    out = []
    if bore.d + c["shaft_bore_clr"] < shaft.d:
        out.append(Mismatch(port, "d", bore.d, shaft.d, "bore smaller than shaft"))
    elif bore.d - shaft.d > c["shaft_bore_max_gap"]:
        out.append(Mismatch(port, "d", bore.d, shaft.d, "bore loose on shaft (needs adaptor)"))
    if shaft.flat is not None and bore.flat is None:
        out.append(Mismatch(port, "flat", None, shaft.flat, "D shaft into round bore: no drive"))
    return out


def compatible(a: Iface, b: Iface) -> list[Mismatch]:
    """Mismatches between two parts that mate. Empty list = compatible. Order-insensitive."""
    pair = {type(a), type(b)}
    if pair == {GearmotorIface, WheelIface}:
        m, w = (a, b) if isinstance(a, GearmotorIface) else (b, a)
        if m.shaft is None or w.bore is None:
            return [Mismatch("shaft/bore", "present", None, "shaft+bore", "port missing")]
        out = shaft_bore(m.shaft, w.bore)
        if w.boss_len + 0.0 > m.shaft.length:
            out.append(Mismatch("shaft/bore", "length", m.shaft.length, w.boss_len, "shaft shorter than hub boss"))
        return out
    if pair == {PackIface, EscIface}:
        p, e = (a, b) if isinstance(a, PackIface) else (b, a)
        out = []
        if e.max_cells and p.cells > e.max_cells:
            out.append(Mismatch("power", "cells", p.cells, e.max_cells, "pack voltage over ESC limit"))
        return out
    if pair == {PackIface, SwitchIface}:
        p, s = (a, b) if isinstance(a, PackIface) else (b, a)
        burst = p.c * p.mah / 1000.0
        return [Mismatch("power", "rated_a", s.rated_a, burst, "switch rating under pack burst")] if s.rated_a and burst > s.rated_a * 2.5 else []
    return []


def envelope_fits(part: Iface, bay: Envelope, clr=0.0) -> list[Mismatch]:
    return [] if part.envelope.fits_in(bay, clr) else [Mismatch("envelope", "lxlylz", (part.envelope.lx, part.envelope.ly, part.envelope.lz),
                                                                (bay.lx, bay.ly, bay.lz), "part does not fit bay")]
