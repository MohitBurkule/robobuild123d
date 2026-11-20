"""`robot brackets SPEC [--wheels a,b] [--spokes 5] [--dry]`: hub caps and axle stubs on the wheels, as part of the
real printed hubs.

WHY: the photo review keeps reporting "photo wheels show a hub cap / axle end; model wheels are plain discs on grey
stubs". Generated drive trains give every wheel a printed hub (`tyre_of` names it) with a short axle-end stub, but its
outer face is a flat disc flush with the tyre, so it does not read as a hub.

What it does, per wheel whose tyre names a printed, unrotated hub:
- finds the wheel axis (its thinnest box side), the outer side (away from the chassis centre), the hub's outer face
  and the end of the axle stub on it, by casting rays;
- adds a hub-cap ring to the hub's shape: from just outside the stub to 0.4 mm inside the hub's rim, standing proud of
  the hub face by up to 1.2 mm but never past the end of the stub. The wheel's widest point therefore does not move
  (footprint and outline unchanged), and the ring is part of the hub print, so mass, BOM and connections stay true;
- cuts N shallow (0.8 mm) lug pockets into the ring so the cap reads as a hub, not as a washer.
It refuses a wheel when the ring would touch any other part (tyre, arch, motor) or would not leave one valid solid
with no extra tiny edges, and it never cuts into the tyre. Wheel *brackets* (outboard supports) change the outline and
how the axle is carried, so they stay a design decision: this tool does not add them.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

ROT = {0: [0, 90, 0], 1: [90, 0, 0], 2: [0, 0, 0]}


def _ray_face(mesh, axis, sign, c, r, ang=0.7):
    """Outermost hit (along axis * sign) of rays parallel to the axis at radius r from centre c; None if no hit."""
    u, v = [i for i in range(3) if i != axis]
    O = np.zeros((8, 3))
    a = np.linspace(0, 2 * np.pi, 8, endpoint=False) + ang
    O[:, u] = c[u] + r * np.cos(a)
    O[:, v] = c[v] + r * np.sin(a)
    O[:, axis] = c[axis] + sign * 80.0
    D = np.zeros_like(O)
    D[:, axis] = -sign
    loc, ri, _ = mesh.ray.intersects_location(O, D, multiple_hits=False)
    if not len(loc):
        return None
    return float(np.max(loc[:, axis] * sign) * sign)


def plan(raw, w, wheel_ids=None, spokes=5):
    """[(wheel id, hub id, shape items to add, info)] or refusal strings."""
    byid = {p["id"]: p for p in raw["parts"]}
    B = {b.id: b for b in w.bodies if not getattr(b, "is_wire", False)}
    root = next((p["id"] for p in raw["parts"] if p.get("kind") == "structure"), None)
    if root not in B:
        return [], ["no chassis body"]
    cc = B[root].center
    out, notes = [], []
    for p in raw["parts"]:
        if p.get("kind") != "wheel" or (wheel_ids and p["id"] not in wheel_ids):
            continue
        hid = p.get("tyre_of")
        hub = byid.get(hid)
        if not hub or "shape" not in hub or hub.get("catalog") or hid not in B or p["id"] not in B:
            notes.append(f"{p['id']}: no printed hub (`tyre_of`)")
            continue
        if any(abs(float(x)) > 1e-9 for x in hub.get("rot") or [0, 0, 0]):
            notes.append(f"{p['id']}: hub `{hid}` is rotated; only unrotated hubs are supported")
            continue
        wb, hb = B[p["id"]], B[hid]
        lo, hi = wb.aabb
        ext = hi - lo
        axis = int(np.argmin(ext))
        c = (lo + hi) / 2
        sign = 1.0 if c[axis] - cc[axis] >= 0 else -1.0
        r_tyre = float(max(ext[i] for i in range(3) if i != axis)) / 2
        hlo, hi_h = hb.aabb
        r_hub = float(max((hi_h - hlo)[i] for i in range(3) if i != axis)) / 2
        r_hub = min(r_hub, r_tyre - 1.0)
        face = _ray_face(hb.mesh, axis, sign, c, 0.75 * r_hub)
        stub = _ray_face(hb.mesh, axis, sign, c, 0.3)
        if face is None or stub is None:
            notes.append(f"{p['id']}: could not find the hub face")
            continue
        # stub radius: the largest radius whose ray still hits the stub end
        r_stub = 0.3
        for rr in np.arange(0.5, r_hub, 0.25):
            f2 = _ray_face(hb.mesh, axis, sign, c, rr)
            if f2 is None or abs(f2 - stub) > 0.05:
                break
            r_stub = rr
        proud = min(1.2, (stub - face) * sign - 0.2)
        r_in, r_out = r_stub + 0.4, r_hub - 0.4
        if proud < 0.6 or r_out - r_in < 1.2:
            notes.append(f"{p['id']}: no room for a cap (stub {(stub - face) * sign:.1f} mm proud, ring {r_out - r_in:.1f} mm)")
            continue
        at = np.asarray(hub.get("at") or [0, 0, 0], float)
        cen = c.copy()
        cen[axis] = face + sign * (proud / 2 - 0.05)
        ring = {"type": "place", "shape": {"type": "subtract",
                "base": {"type": "cylinder", "radius": round(r_out, 3), "height": round(proud + 0.1, 3)},
                "cut": [{"type": "cylinder", "radius": round(r_in, 3), "height": round(proud + 1.0, 3)}]},
                "at": [round(float(x - at[i]), 3) for i, x in enumerate(cen)], "rot": ROT[axis]}
        pockets = []
        rp = (r_in + r_out) / 2
        rr = min(0.3 * (r_out - r_in), 0.9 * np.pi * rp / spokes)
        u, v = [i for i in range(3) if i != axis]
        for k in range(spokes):
            a = 2 * np.pi * k / spokes
            q = cen.copy()
            q[u] += rp * np.cos(a)
            q[v] += rp * np.sin(a)
            q[axis] = face + sign * (proud - 0.8 / 2 + 0.05)
            pockets.append({"type": "place", "shape": {"type": "cylinder", "radius": round(float(rr), 3), "height": 0.9},
                            "at": [round(float(x - at[i]), 3) for i, x in enumerate(q)], "rot": ROT[axis]})
        # nothing else may be where the ring goes
        g = np.linspace(0, 2 * np.pi, 36, endpoint=False)
        P = []
        for r_ in np.linspace(r_in, r_out + 0.2, 5):
            for t in np.linspace(0.1, proud + 0.2, 4):
                for a in g:
                    q = c.copy()
                    q[u] += r_ * np.cos(a)
                    q[v] += r_ * np.sin(a)
                    q[axis] = face + sign * t
                    P.append(q)
        P = np.asarray(P)
        hit = [b.id for i, b in B.items() if i not in (hid,) and not b.fastener and b.inside(P).any()]
        if hit:
            notes.append(f"{p['id']}: the cap would touch {hit}")
            continue
        out.append((p["id"], hid, ring, pockets,
                    f"{p['id']}: cap ring r {r_in:.1f}-{r_out:.1f} mm, {proud:.1f} mm proud of hub `{hid}`, {spokes} lug pockets"))
    return out, notes


def apply(path, wheel_ids=None, spokes=5, dry=False):
    from . import shapes
    from . import spec as spec_mod
    from . import world as world_mod
    from .checks.geom_sanity import tiny_edges

    p = Path(path)
    txt = p.read_text()
    raw = json.loads(txt)
    w = world_mod.World.start(world_mod.resolve(spec_mod.load(path), fast=True))
    todo, notes = plan(raw, w, wheel_ids, spokes)
    byid = {q["id"]: q for q in raw["parts"]}
    done = []
    for wid, hid, ring, pockets, info in todo:
        hub = byid[hid]
        new = {"type": "subtract", "base": {"type": "union", "items": [hub["shape"], ring]}, "cut": pockets}
        try:
            s0, s1 = shapes.to_solid(hub["shape"], p.parent), shapes.to_solid(new, p.parent)
        except Exception as e:  # noqa: BLE001
            notes.append(f"{wid}: CAD failed ({e})")
            continue
        if len(s1.solids()) != len(s0.solids()) or not s1.is_valid or len(tiny_edges(s1)) > len(tiny_edges(s0)):
            notes.append(f"{wid}: refused (the cap would not leave one valid solid without tiny edges)")
            continue
        if not dry:
            hub["shape"] = new
            if hub.get("volume_mm3"):
                hub["volume_mm3"] = round(float(s1.volume), 1)
        done.append(info)
    if done and not dry:
        ind = 1 if txt.startswith("{\n ") and not txt.startswith("{\n  ") else 2
        p.write_text(json.dumps(raw, indent=ind) + "\n")
    return done, notes


def main(a):
    ids = set(a.wheels.split(",")) if a.wheels else None
    done, notes = apply(a.spec, ids, a.spokes, a.dry)
    for n in notes:
        print("  skipped " + n)
    for d in done:
        print(("would add " if a.dry else "") + d)
    print(f"{len(done)} hub cap(s){' (dry run)' if a.dry else ''}")
    return 0 if done else 1


def add_cli(sub):
    p = sub.add_parser("brackets", help="hub caps with lug pockets on the wheels' printed hubs (outline unchanged)")
    p.add_argument("spec")
    p.add_argument("--wheels", help="only these wheel ids (comma separated)")
    p.add_argument("--spokes", type=int, default=5, help="lug pockets per cap")
    p.add_argument("--dry", action="store_true")
    p.set_defaults(func=main)
