"""Component pockets: a housing wall around each placed component and a cavity with a printing gap."""

from __future__ import annotations

from . import sh
from .plan import Pocket

GAP = 0.4
HOUSING = 1.4
PORT_ROOM = 1.6
NOTCH_FLOOR = -1.0  # notches reach at least this low so they meet the wire channels (top at +0.5)
RETAINED = {"battery": "velcro", "esc": "velcro", "receiver": "tape", "switch": "adhesive", "servo": None}


def add_component(plan, cid, kind, catalog, size, x, y, z, rot_z, *, retained="auto", housing=HOUSING, **extra):
    """Place a bought component and its pocket. `size` is the catalog box (x, y, z) before rotation."""
    sx, sy, sz = size
    fx, fy = (sy, sx) if int(round(rot_z)) % 180 == 90 else (sx, sy)
    p = plan.part(id=cid, kind=kind, catalog=catalog, at=[x, y, z], rot=[0.0, 0.0, float(rot_z)], **extra)
    ret = RETAINED.get(kind) if retained == "auto" else retained
    if ret:
        p["retained"] = ret
    pk = Pocket(cid, x - fx / 2 - GAP, x + fx / 2 + GAP, y - fy / 2 - GAP, y + fy / 2 + GAP,
                z - sz / 2 - GAP, z + sz / 2 + GAP, housing)
    for q in _ports_world(p, catalog, x, y, z, rot_z):
        # a small notch round each port, reaching down into the wire-channel band; the rest of the pocket stays
        # snug so the part is captive
        pk.notches.append((q[0] - PORT_ROOM, q[0] + PORT_ROOM, q[1] - PORT_ROOM, q[1] + PORT_ROOM,
                           min(q[2] - PORT_ROOM, NOTCH_FLOOR), max(q[2] + PORT_ROOM, NOTCH_FLOOR + 2.0)))
    plan.pockets.append(pk)
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
