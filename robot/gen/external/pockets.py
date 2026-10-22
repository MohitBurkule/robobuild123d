"""Component pockets: a housing wall around each placed component and a cavity with a printing gap."""

from __future__ import annotations

from . import sh
from ..intent import I, pocket_gap
from .plan import Pocket

GAP = 0.4
HOUSING = 1.4
PORT_ROOM = 1.6
NOTCH_FLOOR = -1.0  # notches reach at least this low so they meet the wire channels (top at +0.5)
RETAINED = {"battery": "velcro", "esc": "velcro", "receiver": "tape", "switch": "adhesive", "servo": None}


PURPOSE = {"battery": "power", "esc": "motor control", "receiver": "radio link", "switch": "power isolation",
           "servo": "weapon actuation"}


def add_component(plan, cid, kind, catalog, size, x, y, z, rot_z, *, retained="auto", housing=HOUSING, **extra):
    """Place a bought component and its pocket. `size` is the catalog box (x, y, z) before rotation.
    The pocket exists to retain the part: its clearance comes from how it is held (pocket_gap), the housing wall
    round it is the print minimum (it only locates the part; the outer wall takes the hits)."""
    sx, sy, sz = size
    fx, fy = (sy, sx) if int(round(rot_z)) % 180 == 90 else (sx, sy)
    ret = RETAINED.get(kind) if retained == "auto" else retained
    p = plan.part(id=cid, kind=kind, catalog=catalog, at=[x, y, z], rot=[0.0, 0.0, float(rot_z)],
                  intent=I("load_path" if kind == "servo" else "wiring", f"{PURPOSE.get(kind, kind)}: {catalog}",
                           f"chosen by the hypothesis; placed by the layout solver at ({x:g}, {y:g})", threats=["wall_slam", "flip_landing"]), **extra)
    if ret:
        p["retained"] = ret
    gap = pocket_gap(ret or "captive") if ret != "velcro" else GAP
    pk = Pocket(cid, x - fx / 2 - gap, x + fx / 2 + gap, y - fy / 2 - gap, y + fy / 2 + gap,
                z - sz / 2 - gap, z + sz / 2 + gap, housing,
                intent=I("retention", f"{cid} sits in a snug pocket so it cannot shift under impact ({ret or 'captive'}); "
                         "port notches let its leads out into the channels",
                         f"catalog box {sx:g}x{sy:g}x{sz:g} mm + {gap} mm gap; housing {housing} mm = print minimum", threats=["wall_slam", "flip_landing", "crusher_hammer"]))
    for q in _ports_world(p, catalog, x, y, z, rot_z):
        # a small notch round each port, reaching down into the wire-channel band; the rest of the pocket stays
        # snug so the part is captive
        pk.notches.append((q[0] - PORT_ROOM, q[0] + PORT_ROOM, q[1] - PORT_ROOM, q[1] + PORT_ROOM,
                           min(q[2] - PORT_ROOM, NOTCH_FLOOR), max(q[2] + PORT_ROOM, NOTCH_FLOOR + 2.0)))
    plan.pocket(pk)
    return p, pk


def _ports_world(p, catalog, x, y, z, rot_z):
    import math

    from ... import catalog as cat
    ports = p.get("ports") or (cat.find(catalog).ports if catalog else {})
    a = math.radians(rot_z)
    for lx, ly, lz in ports.values():
        yield (x + lx * math.cos(a) - ly * math.sin(a), y + lx * math.sin(a) + ly * math.cos(a), z + lz)


def cavity(pk: Pocket):
    return sh.U(sh.boxr(pk.x0, pk.x1, pk.y0, pk.y1, pk.z0, pk.z1), *(sh.boxr(*n) for n in pk.notches))
