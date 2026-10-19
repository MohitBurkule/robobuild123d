"""Attack exposure (adversarial survivability): can an opponent's weapon reach a vulnerable function part?

For every vulnerable part (belts / O-rings, motors, ESCs, receiver, battery, switch, bearings, connectors, pulleys,
wires) the surface is sampled and, for each attack class, rays are cast from each sample point back toward the attacker.
A point is EXPOSED for an attack when its surface faces the attacker (n . d > 0.1) and the ray escapes without hitting any
other body (structure, armour, wheels, the weapon...). The exposed fraction is the share of sampled area exposed to at
least one direction of the class.

Attack classes (rays point from the part toward the attacker):
  horizontal  horizontal spinner / arena wall: 12 azimuths in the floor plane, every height.
  overhead    vertical spinner / hammer coming down: straight up plus 4 directions 30 deg off vertical.
  floor       wedge / lifter / flipper at floor level: 12 azimuths, only points within `floor_mm` (6) of the floor.

Findings (BLOCKER when over the limit unless the spec gives a reason):
  exposure.part          exposed fraction of a vulnerable part over `max_frac` (default 0.35; belts 0.6 because an
                         O-ring must touch its pulleys; drive tyres are not vulnerable parts).
  exposure.wire_outer    a routed wire lies on the outer envelope (within 1 mm of the robot's convex hull).
  exposure.switch_recess the power switch body stands proud of the surface round it (a hit can knock it on/off).
  exposure.drive_redundancy  one attack direction exposes the drive on both sides (both motors or both belts), so a
                         single hit can stop the robot.
  exposure.tilt_gap      ground game under tilt: the robot is tilted +-2 / +-5 deg in pitch and roll and dropped onto
                         the floor; per side (front, rear, left, right) the highest edge gap (lowest non-wheel point in
                         the perimeter band) is reported. A side whose gap passes `tilt_gap_mm` (3) within `tilt_deg`
                         (2: tyre squash, a bump) loses
                         the ground game there (WARNING; BLOCKER for the front).
  exposure.catch         catchability: exposed faces that square up (n . d > 0.9) to a horizontal attack in the tooth
                         band (3..30 mm) are what a spinner tooth bites. Reported per side in mm2; WARNING over
                         `catch_mm2` (default 60, or the reference robot's value x 1.2).
  exposure.screw_heads   a screw head proud (> 0.2 mm) of the robot's envelope can be caught and sheared (BLOCKER).
  exposure.rip_off       a bought-in / small part more than 30 % exposed and held by fewer than 2 joints (WARNING).
Spec: {"exposure": {"max_frac": 0.35, "parts": {"<id>": {"max_frac": 0.5, "reason": "why it may be exposed"}},
                    "skip": ["<id>"]}}
"""

from __future__ import annotations

import math

import numpy as np

from ..finding import BLOCKER, WARNING, fail, ok

G = "exposure"
VULN_KINDS = ("belt", "motor", "esc", "receiver", "battery", "switch", "bearing", "connector", "pulley")
DEFAULT_FRAC = {"belt": 0.6}


def attack_dirs():
    az = [(math.cos(a), math.sin(a), 0.0) for a in np.linspace(0, 2 * math.pi, 12, endpoint=False)]
    s, c = math.sin(math.radians(30)), math.cos(math.radians(30))
    over = [(0.0, 0.0, 1.0)] + [(s * math.cos(a), s * math.sin(a), c) for a in np.linspace(0, 2 * math.pi, 4, endpoint=False)]
    return {"horizontal": np.array(az), "overhead": np.array(over), "floor": np.array(az)}


def exposed_fraction(part, shield, floor_z=0.0, floor_mm=6.0, n=600, seed=4):
    """{class: fraction} of the part's surface an attacker of each class can reach past the shield mesh."""
    import trimesh

    p, fi = trimesh.sample.sample_surface_even(part, n, seed=seed)
    nrm = part.face_normals[fi]
    out = {}
    for cls, D in attack_dirs().items():
        hit = np.zeros(len(p), bool)
        mask = np.ones(len(p), bool) if cls != "floor" else (p[:, 2] <= floor_z + floor_mm)
        for d in D:
            face = mask & (nrm @ d > 0.1) & ~hit
            if not face.any():
                continue
            o = p[face] + d * 0.05
            blocked = shield.ray.intersects_any(o, np.repeat(d[None], len(o), 0)) if shield is not None else np.zeros(len(o), bool)
            idx = np.flatnonzero(face)
            hit[idx[~blocked]] = True
        out[cls] = float(hit.sum() / len(p))
    return out


def proud_of(part, others):
    """How far `part` sticks outside the convex hull of the other bodies (> 0: proud)."""
    import trimesh

    return float(-trimesh.proximity.signed_distance(_concat(others).convex_hull, part.vertices).min())


def envelope_margin(points, meshes):
    """Smallest distance from points to the outside of the robot's convex hull (< 1 mm: on an outer face)."""
    import trimesh

    return float(trimesh.proximity.signed_distance(_concat(meshes).convex_hull, points).min())


def _concat(meshes):
    import trimesh

    ms = [m for m in meshes if m is not None and len(m.faces)]
    return trimesh.util.concatenate(ms) if ms else None


def run(ctx):
    spec = ctx.r.spec
    cfg = (spec.raw or {}).get("exposure") or {}
    skip = set(cfg.get("skip", []))
    over = cfg.get("parts", {})
    bodies = [b for b in ctx.world.bodies if not b.is_wire]
    floor_z = float(min(b.aabb[0][2] for b in bodies)) if bodies else 0.0
    out, res = [], {}
    vuln = [p for p in spec.parts if (p.kind in VULN_KINDS or (p.catalog and p.kind in ("electronics",))) and p.id not in skip]
    for p in vuln:
        b = ctx.world.body(p.id)
        if b is None:
            continue
        own = {p.id}
        shield = _concat([o.mesh for o in bodies if o.id not in own and not o.id.startswith("belt")
                          and not (getattr(o, "fastener", False))])
        fr = exposed_fraction(b.mesh, shield, floor_z)
        res[p.id] = fr
        worst = max(fr, key=fr.get)
        o = over.get(p.id, {})
        lim = o.get("max_frac", DEFAULT_FRAC.get(p.kind, cfg.get("max_frac", 0.35)))
        msg = f"`{p.id}` ({p.kind}): exposed {fr['horizontal']:.0%} to a horizontal spinner / wall, {fr['overhead']:.0%} from above, {fr['floor']:.0%} to a wedge at floor level (limit {lim:.0%})."
        if fr[worst] > lim:
            if o.get("reason"):
                out.append(fail("exposure.part", G, WARNING, "Vulnerable part exposed (accepted)", msg + f" Accepted: {o['reason']}").on(p.id))
            else:
                out.append(fail("exposure.part", G, BLOCKER, "Vulnerable part exposed to attack", msg).on(p.id)
                           .fix("Put structure or armour between it and the attacker (a side panel over the belt, a wall over the ESC), or move it inboard."))
        else:
            out.append(ok("exposure.part", G, "Vulnerable part shielded", msg))
    ctx.metrics["exposure"] = res
    out += _tilt(ctx, bodies, cfg, floor_z)
    out += _catch(ctx, bodies, cfg)
    out += _rip(ctx, spec, res)
    out += _redundancy(spec, res, cfg)
    out += _wires_outer(ctx, bodies)
    out += _switch(ctx, spec, bodies)
    return out


def _side(ctx, pid):
    b = ctx.world.body(pid)
    return 0 if b is None else int(np.sign(b.center[0]))


def _redundancy(spec, res, cfg):
    """A single attack class must not expose BOTH drive sides (motor or belt) past the limit."""
    out = []
    drive = [p for p in spec.parts if p.kind in ("motor", "belt") and p.id in res and not (p.catalog or "").startswith("gr")
             and p.role != "weapon" and "weapon" not in p.id]
    lim = cfg.get("redundancy_frac", 0.5)
    for cls in ("horizontal", "overhead", "floor"):
        sides = {}
        for p in drive:
            x = 1 if p.id.endswith("r") else -1 if p.id.endswith("l") else 0
            if res[p.id][cls] > lim:
                sides.setdefault(x, []).append(p.id)
        if 1 in sides and -1 in sides:
            out.append(fail("exposure.drive_redundancy", G, BLOCKER, "One hit can stop the drive",
                            f"a {cls} attack reaches both drive sides: {sides[-1]} and {sides[1]} (each > {lim:.0%} exposed)."))
    if not out and drive:
        out.append(ok("exposure.drive_redundancy", G, "Drive survives a single hit", f"no attack class exposes both drive sides past {lim:.0%}."))
    return out


def _wires_outer(ctx, bodies):
    wires = [b for b in ctx.world.bodies if b.is_wire]
    if not wires:
        ctx.not_checked.append("exposure.wire_outer: no routed wire geometry (run with the deep sweeps)")
        return []
    out = []
    for w in wires:
        P = w.mesh.vertices
        d = envelope_margin(P[:: max(1, len(P) // 400)], [b.mesh for b in bodies])
        if d < 1.0:
            out.append(fail("exposure.wire_outer", G, BLOCKER, "Wire on an outer face",
                            f"`{w.id}` comes within {max(d, 0):.2f} mm of the robot's outer envelope; route it inside the structure."))
    if not out:
        out.append(ok("exposure.wire_outer", G, "Wires run inside", f"{len(wires)} wire(s) stay > 1 mm inside the outer envelope."))
    return out


def _switch(ctx, spec, bodies):
    """The switch body must sit at or below the surface round it (recessed); only the lever may reach the face."""
    out = []
    for p in spec.parts:
        if p.kind != "switch":
            continue
        b = ctx.world.body(p.id)
        if b is None:
            continue
        proud = proud_of(b.mesh, [o.mesh for o in bodies if o.id != p.id])
        if proud > 0.2:
            out.append(fail("exposure.switch_recess", G, BLOCKER, "Switch stands proud",
                            f"`{p.id}` sticks {proud:.2f} mm outside the rest of the robot; a hit can knock it on or off.").on(p.id))
        else:
            out.append(ok("exposure.switch_recess", G, "Switch recessed", f"`{p.id}` stays inside the robot's envelope (margin {-proud:.2f} mm)."))
    return out


# ------------------------------------------------------------------------------------------------ ground game / catch
def edge_gaps(meshes, wheel_mask, band=6.0):
    """{side: edge gap mm} for front (+Y), rear, left (+X), right with the mesh set already resting on z = 0."""
    P = np.vstack([m.vertices for m in meshes])
    W = np.concatenate([np.full(len(m.vertices), w) for m, w in zip(meshes, wheel_mask)])
    out = {}
    for side, (ax, sg) in {"front": (1, 1), "rear": (1, -1), "left": (0, 1), "right": (0, -1)}.items():
        c = P[:, ax] * sg
        k = (c >= c.max() - band) & ~W
        out[side] = float(P[k, 2].min()) if k.any() else math.inf
    return out


def tilt_sweep(meshes, wheel_mask, angles=(-5, -2, 0, 2, 5)):
    """{side: {angle_label: gap}} with the robot pitched / rolled and dropped onto the floor."""
    import trimesh

    c = np.vstack([m.vertices for m in meshes]).mean(0)
    res = {}
    for axis, name in (((1, 0, 0), "pitch"), ((0, 1, 0), "roll")):
        for a in angles:
            R = trimesh.transformations.rotation_matrix(math.radians(a), axis, c)
            ms = [m.copy().apply_transform(R) for m in meshes]
            z0 = min(m.vertices[:, 2].min() for m in ms)
            for m in ms:
                m.vertices[:, 2] -= z0
            for side, g in edge_gaps(ms, wheel_mask).items():
                res.setdefault(side, {})[f"{name} {a:+d}"] = round(g, 2)
    return res


def catch_area(meshes, shield, zband=(3.0, 30.0), n=4000, seed=5):
    """{side: mm2} of exposed faces squarely facing a horizontal attacker in the tooth band."""
    import trimesh

    m = trimesh.util.concatenate(meshes)
    p, fi = trimesh.sample.sample_surface_even(m, n, seed=seed)
    nrm = m.face_normals[fi]
    da = float(m.area) / len(p)
    z0 = m.bounds[0][2]
    inb = (p[:, 2] >= z0 + zband[0]) & (p[:, 2] <= z0 + zband[1])
    sides = {"front": (0, 1, 0), "rear": (0, -1, 0), "left": (1, 0, 0), "right": (-1, 0, 0)}
    out = {}
    for side, d in sides.items():
        d = np.array(d, float)
        tot = 0.0
        for rot in (-30, 0, 30):   # the tooth arrives within +-30 deg of square to the side
            a = math.radians(rot)
            dd = np.array([d[0] * math.cos(a) - d[1] * math.sin(a), d[0] * math.sin(a) + d[1] * math.cos(a), 0.0])
            k = inb & (nrm @ dd > 0.9)
            if k.any():
                o = p[k] + dd * 0.05
                free = ~shield.ray.intersects_any(o, np.repeat(dd[None], len(o), 0))
                tot = max(tot, float(free.sum()) * da)
        out[side] = round(tot, 1)
    return out


def _tilt(ctx, bodies, cfg, floor_z):
    solid = [b for b in bodies if not getattr(b, "fastener", False)]
    wheelish = [any(w in (b.kind or "") for w in ("wheel", "tyre")) or b.id.startswith("wheel") for b in solid]
    sw = tilt_sweep([b.mesh for b in solid], wheelish)
    ctx.metrics["tilt_gap"] = sw
    lim = cfg.get("tilt_gap_mm", 3.0)
    out = []
    for side, d in sw.items():
        near = {k: v for k, v in d.items() if abs(int(k.split()[1])) <= cfg.get('tilt_deg', 2)}
        worst = max(near, key=near.get)
        msg = f"{side}: edge gap {near[worst]:.1f} mm at {worst} (all tilts: {d})."
        if near[worst] > lim:
            out.append(fail("exposure.tilt_gap", G, BLOCKER if side == "front" else WARNING, "Loses the ground game under tilt",
                            msg + " An opponent's wedge gets under this side.").fix("Lower the skirt / fork tips or extend them outboard."))
        else:
            out.append(ok("exposure.tilt_gap", G, "Keeps the ground game under tilt", msg))
    return out


def _catch(ctx, bodies, cfg):
    solid = [b for b in bodies if not getattr(b, "fastener", False)]
    shield = _concat([b.mesh for b in solid])
    ca = catch_area([b.mesh for b in solid], shield)
    ctx.metrics["catch_mm2"] = ca
    lim = cfg.get("catch_mm2", 60.0)
    lims = lim if isinstance(lim, dict) else {k: lim for k in ca}
    out = []
    for side, a in ca.items():
        msg = f"{side}: {a:.0f} mm2 of square-on exposed face in the 3-30 mm tooth band (limit {lims[side]:.0f})."
        if a > lims[side]:
            out.append(fail("exposure.catch", G, WARNING, "Catchable faces", msg + " A spinner tooth can bite these and lift or rip the robot.")
                       .fix("Batter / slope the face (a ramp deflects the tooth), round the corner, or hide it behind armour."))
        else:
            out.append(ok("exposure.catch", G, "Few catchable faces", msg))
    heads = [b for b in ctx.world.bodies if getattr(b, "fastener", False)]
    others = [b.mesh for b in solid]
    for h in heads:
        pr = proud_of(h.mesh, others)
        if pr > 0.2:
            out.append(fail("exposure.screw_heads", G, BLOCKER, "Screw head can be caught",
                            f"`{h.id}` stands {pr:.2f} mm outside the robot; a tooth can catch and shear it.").on(h.id))
    if heads and not any(f.id == "exposure.screw_heads" for f in out):
        out.append(ok("exposure.screw_heads", G, "No catchable screw heads", f"{len(heads)} screw heads stay inside the envelope."))
    return out


def _rip(ctx, spec, res):
    joints = {}
    for c in spec.raw.get("connections", []):
        for k in ("a", "b"):
            joints[c[k]] = joints.get(c[k], 0) + 1
    for f in spec.raw.get("fasteners", []):
        for t in list(f.get("through", [])) + [f.get("threads_into")]:
            if t:
                joints[t] = joints.get(t, 0) + 1
    out = []
    for pid, fr in res.items():
        p = next((q for q in spec.parts if q.id == pid), None)
        if p is None or p.kind in ("belt", "pulley"):
            continue
        if max(fr.values()) > 0.3 and joints.get(pid, 0) < 2:
            out.append(fail("exposure.rip_off", G, WARNING, "Exposed part held by one joint",
                            f"`{pid}` is {max(fr.values()):.0%} exposed and held by {joints.get(pid, 0)} joint(s); one caught hit can tear it off.").on(pid))
    return out
