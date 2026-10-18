"""Architecture: structure, mounts, load paths and fasteners under load (python-only group, no Rust counterpart).

Hand calculations with conservative handbook numbers. Conventions follow `_physics`: world mm, +Y front, +Z up, loads in
N, stresses in MPa. The design impact is `_physics.impact_n` (100 g on the robot). Every check reports a pass line when it
judged something, a NOT CHECKED entry when data is missing, and nothing silently.

Declarations read from the spec (all optional extra keys):
  part.rotates_with: "<weapon id>" | "fixed"    motion group override
  part.asymmetric: true / spec.asymmetric: [ids] left/right parts that are meant to differ
  part.print_dir: [x, y, z]                      build direction of a printed part (default +Z)
  part.motor_shaft_removed: true                 a hub-motor conversion: the outrunner's own shaft and bearings are gone
  spec.chassis: "<id>"                           the main tub (default: the biggest structure part)
  fastener.washer: true / head: "washer"|"flange" a washer under the head or nut
  fastener.grade: "8.8" | "10.9" | "12.9" | "a2" | "nylon"
  connection.method "interlock"/"snap" or mechanical_key: true between a cantilevered part and its holder = a locating lip
"""

from __future__ import annotations

import math
import re
from itertools import combinations

import numpy as np
import trimesh
from shapely import affinity
from shapely.geometry import MultiPoint, Point

from .. import catalog, measure
from ..finding import BLOCKER, WARNING, fail, ok
from . import _physics as ph

G = "architecture"
CONTACT_GAP = 0.35
STRUCT = ("structure", "plate", "fork", "armor", "wedge")
ELEC = ("battery", "esc", "receiver", "switch", "servo")
BLADE_TIP_N = 300.0
BOLT_SF = 2.0
FORK_DEFL_MM = 0.3
FORK_DEFL_BLOCK_MM = 1.0
SYM_TOL_MM = 0.5
MIN_INSERT_WALL = 1.5
MIN_LAYER_MM = 1.6  # material under a load-path bolt: fewer than ~8 layers of 0.2 mm is a single skin
CANTILEVER_RATIO = 3.0
SHAFT_SPAN_D = 10.0
# Thread pitch (coarse) and shear strength of the bolt material (0.6 x tensile), MPa.
PITCH = {1.6: 0.35, 2.0: 0.4, 2.5: 0.45, 3.0: 0.5, 4.0: 0.7, 5.0: 0.8, 6.0: 1.0}
GRADE_SHEAR = {"8.8": 480.0, "10.9": 600.0, "12.9": 730.0, "a2": 420.0, "a4": 420.0, "titanium": 500.0, "nylon": 40.0}
GRADE_YIELD = {"8.8": 640.0, "10.9": 900.0, "12.9": 1080.0, "a2": 450.0, "a4": 450.0, "titanium": 830.0, "nylon": 60.0}
DEFAULT_GRADE = "8.8"
# Assembly preload assumed for a screw tightened into plastic, N per mm^2 of d^2 (M2 ~ 200 N).
PRELOAD_PER_D2 = 40.0
MOTOR_THREAD_DEPTH = {"motor": 2.5, "weapon_motor": 3.5}  # usable thread depth of a motor face hole


# ----------------------------------------------------------------------------------------------------------------- helpers

def _unit(v):
    v = np.asarray(v, float)
    n = np.linalg.norm(v)
    return v / n if n > 1e-12 else v


def _perp(ax):
    u = np.cross(ax, [0, 0, 1.0])
    if np.linalg.norm(u) < 1e-6:
        u = np.cross(ax, [1.0, 0, 0])
    u = _unit(u)
    return u, _unit(np.cross(ax, u))


def _ring(c, ax, r, n=24):
    u, v = _perp(ax)
    return np.array([c + r * (math.cos(k) * u + math.sin(k) * v) for k in np.linspace(0, 2 * math.pi, n, endpoint=False)])


def _ray_exit(body, c, d, r0, rmax, step=0.1):
    """Distance from c along d (starting at r0) to the first point outside `body`; rmax when it never leaves."""
    ts = np.arange(r0, rmax + step, step)
    ins = body.inside(c + np.outer(ts, d))
    idx = np.nonzero(~ins)[0]
    return float(ts[idx[0]]) if len(idx) else float(rmax)


def _extra(o, k, default=None):
    return getattr(o, "_extra", {}).get(k, default)


def _plane_section(mesh, c, n, u):
    """Cross-section of `mesh` by the plane through c with normal n, as a shapely (Multi)Polygon in (u, n x u) coords."""
    n = _unit(n)
    u = _unit(np.asarray(u, float) - n * (np.asarray(u, float) @ n))
    v = np.cross(n, u)
    try:
        segs = trimesh.intersections.mesh_plane(mesh, n, c)
    except Exception:  # noqa: BLE001
        return None
    if len(segs) == 0:
        return None
    from shapely.geometry import LineString
    from shapely.ops import polygonize, unary_union

    q = np.asarray(segs) - c
    uv = np.round(np.stack([q @ u, q @ v], axis=-1), 3)
    lines = [LineString(sg) for sg in uv if np.linalg.norm(sg[0] - sg[1]) > 0]
    polys = list(polygonize(unary_union(lines)))
    if not polys:
        return None
    from functools import reduce

    return reduce(lambda x, y: x.symmetric_difference(y), polys)


class A:
    """Shared look-ups for one run."""

    def __init__(self, ctx):
        self.ctx, self.r, self.w, self.spec = ctx, ctx.r, ctx.world, ctx.r.spec
        self.parts = {p.id: p for p in self.spec.parts}
        self.bodies = [b for b in self.w.bodies if not b.is_wire]
        self.solids = [b for b in self.bodies if not b.fastener]
        self._contact = {}
        self._area = {}
        self.F = ph.impact_n(ctx)
        self.chassis = self._chassis()
        self.fast = [f for f in self.spec.fasteners if catalog.parse_designation(f.designation)]
        self.insert_host = {}
        for b in self.solids:
            if b.kind in ("insert", "nut"):
                h = self._holder(b)
                if h is not None:
                    self.insert_host[b.id] = h.id
        self.rotor = self._rotor()

    def part(self, bid):
        return self.parts.get(bid)

    def body(self, bid):
        return self.w.body(bid)

    def mat(self, b):
        return ph.material_of(self.ctx, b)

    def cls(self, b):
        m = catalog.material(self.mat(b))
        return m.cls if m else None

    def printed(self, b):
        return ph.printed(self.ctx, b)

    def mass(self, b):
        m = self.ctx.metrics.get(f"part_mass_g.{b.id}")
        if m is not None:
            return float(m)
        if b.fastener:
            return b.geom.volume * 7.85e-3
        from .connections import part_mass_g

        return part_mass_g(self.r.parts[b.part_idx], b) if b.part_idx is not None else None

    def _chassis(self):
        cid = self.spec.raw.get("chassis")
        if cid and self.w.body(cid) is not None:
            return self.w.body(cid)
        cands = [b for b in self.solids if b.kind in ("structure", "plate")]
        return max(cands, key=lambda b: b.geom.volume) if cands else None

    def _holder(self, tgt):
        """Body holding most of a ring just outside a small cylindrical part (insert, nut, bearing)."""
        ax = _unit(tgt.M[:3, 2])
        rr = ph.perp_radius(tgt.mesh.vertices, tgt.center, ax)
        ring = _ring(tgt.center, ax, float(rr.max()) + 0.5, 16)
        best = None
        for b in self.solids:
            if b is tgt or b.kind in ("insert", "nut") or not measure.aabb_overlap(b.aabb, tgt.aabb, 2.0):
                continue
            n = int(b.inside(ring).sum())
            if n and (best is None or n > best[0]):
                best = (n, b)
        return best[1] if best else None

    def contact(self, a, b):
        key = tuple(sorted((a.id, b.id)))
        if key not in self._contact:
            if not measure.aabb_overlap(a.aabb, b.aabb, CONTACT_GAP):
                self._contact[key] = False
            else:
                try:
                    self._contact[key] = measure.min_gap(a, b, 1.0) <= CONTACT_GAP
                except Exception:  # noqa: BLE001 - non-manifold mesh: fall back to the bounding boxes
                    self._contact[key] = True
        return self._contact[key]

    def area(self, a, b):
        key = (a.id, b.id)
        if key not in self._area:
            from .connections import contact_area_mm2

            self._area[key] = contact_area_mm2(a, b, CONTACT_GAP)
        return self._area[key]

    def coupled(self, f):
        """Part ids a fastener holds together; an insert or nut stands for the part it sits in."""
        ids = list(f.through or [])
        if f.threads_into:
            ids.append(f.threads_into)
            h = self.insert_host.get(f.threads_into)
            if h:
                ids.append(h)
        return [i for i in dict.fromkeys(ids) if self.w.body(i) is not None]

    def threaded_host(self, f):
        """The part whose material carries the thread (the insert's host for an insert)."""
        t = f.threads_into
        if not t:
            return None
        return self.insert_host.get(t, t)

    def fasteners_of(self, pid):
        return [f for f in self.fast if pid in self.coupled(f)]

    def between(self, a, b):
        return [f for f in self.fast if a in self.coupled(f) and b in self.coupled(f)]

    def conns(self, a, b=None):
        return [c for c in self.spec.connections if (c.a == a and (b is None or c.b == b)) or (c.b == a and (b is None or c.a == b))]

    def _rotor(self):
        """Weapon id -> set of part ids that spin with it."""
        out = {}
        for p in self.spec.parts:
            if p.kind == "weapon" and p.weapon is not None and p.weapon.kind in ph.SPINS:
                out[p.id] = {p.id}
        for wid, s in out.items():
            changed = True
            while changed:
                changed = False
                for p in self.spec.parts:
                    if p.id in s:
                        continue
                    rw = _extra(p, "rotates_with")
                    if rw == "fixed":
                        continue
                    if rw == wid or (p.parent in s and p.kind not in ("weapon_motor",)) or p.kind == "hub" and any(
                            c.method in ("press_fit", "glue", "screw", "pin") for x in s for c in self.conns(p.id, x)):
                        s.add(p.id)
                        changed = True
        return out

    def group_of(self, pid):
        """Motion group: a weapon id, 'fixed', or None when ambiguous (shaft, bearing, weapon motor, wheels)."""
        p = self.part(pid)
        if p is None:
            return None
        rw = _extra(p, "rotates_with")
        if rw:
            return rw
        for wid, s in self.rotor.items():
            if pid in s:
                return wid
        if p.kind in ("shaft", "bearing", "weapon_motor", "motor", "wheel", "tyre", "pulley", "belt", "pin", "hub", "wheel_hub") or p.joint:
            return None
        if p.kind in ("insert", "nut"):
            h = self.insert_host.get(pid)
            return self.group_of(h) if h else None
        return "fixed"


def _print_dir(p):
    v = _extra(p, "print_dir") or _extra(p, "print_orientation")
    if isinstance(v, str) and len(v) == 2 and v[1] in "xyz":
        e = np.zeros(3)
        e["xyz".index(v[1])] = 1.0
        return e
    return _unit(v) if v is not None else np.array([0, 0, 1.0])


def _res(out, fid, sev, title, bad, good_msg, judged):
    """Append one pass line when nothing failed and something was judged."""
    if judged and not bad:
        out.append(ok(fid, G, title, good_msg))


# --------------------------------------------------------------------------------------------------------------- run

def run(ctx):
    a = A(ctx)
    out = []
    if a.chassis is None:
        ctx.not_checked.append("Architecture: no structure part to act as the chassis; mounts and load paths not traced")
        out.append(fail("arch.chassis", G, WARNING, "No chassis found", "No `structure` or `plate` part, so nothing is a chassis.")
                   .fix("Add the tub as a `structure` part or set `chassis` in the spec."))
        return out
    ctx.metrics["arch_chassis"] = a.chassis.id
    for fn in (materials, motion, weapon, motors, fasteners, cantilevers, blades, blade_orientation, teeth, foreign_through_rotor, holders, cut_breakout, armour, pods, pods_enclose, electronics, wheels,
               symmetry, balance):
        try:
            out += fn(a)
        except Exception as e:  # noqa: BLE001 - fail closed per sub-check
            ctx.not_checked.append(f"Architecture `{fn.__name__}` crashed: {type(e).__name__}: {e}")
            out.append(fail("arch.crashed", G, WARNING, "Architecture sub-check crashed",
                            f"`{fn.__name__}` raised {type(e).__name__}: {e}; its verdicts are unknown."))
    return out


# --------------------------------------------------------------------------------------------------------------- materials

SKIN_KINDS = ("armor", "fork", "wedge")


def _carries(spec, pid):
    """True when another part is parented to `pid` or a screw threads into it: it is in some part's load path."""
    return any(q.parent == pid for q in spec.parts) or any(f.threads_into == pid for f in spec.fasteners)


def materials(a):
    out = []
    bad = 0
    struct_kinds = STRUCT + ("weapon", "shaft", "pin", "locking_bar", "hub", "bearing")
    for b in a.solids:
        p = a.part(b.id)
        if p is None or a.cls(b) != "elastomer":
            continue
        if p.kind in SKIN_KINDS and b.id != a.chassis.id and not _carries(a.spec, p.id):
            # TPU armour / wedgelets / side panels that carry nothing (no child part, nothing threads into them) are a
            # skin that soaks hits and springs back (RVRN: TPU hood and wedglets on a PLA tub); the load path is elsewhere.
            out.append(ok("arch.tpu_skin", G, "Elastomer skin carries nothing",
                          f"`{b.id}` ({p.kind}) is {p.material} but holds no other part; it is a hit-absorbing skin."))
            continue
        if p.kind in struct_kinds or b.id == a.chassis.id:
            bad += 1
            out.append(fail("arch.tpu_structural", G, BLOCKER, "Structural part made of an elastomer",
                            f"`{b.id}` ({p.kind}) is {p.material}: modulus ~0.03 GPa, it deflects tens of mm under a {a.F:.0f} N hit.")
                       .on(b.id).fix("Make it nylon/PETG/PC or metal; keep TPU for tyres, bumpers and dampers."))
    out += [] if bad else [ok("arch.tpu_structural", G, "No structure in elastomer", "No structural part is TPU or rubber.")]
    bad = 0
    for f in a.fast:
        h = a.threaded_host(f)
        hb = a.body(h) if h else None
        if hb is not None and a.cls(hb) == "elastomer":
            bad += 1
            out.append(fail("arch.tpu_threaded", G, BLOCKER, "Screw threads into an elastomer",
                            f"`{f.id}` threads into `{h}` ({a.mat(hb)}); TPU cannot hold a thread or an insert.").on(f.id, h)
                       .fix("Thread into a rigid part or use a through bolt with a nut and washer."))
    out += [] if bad else [ok("arch.tpu_threaded", G, "No screws in elastomers", "No fastener threads into TPU or rubber.")]
    # Brittle printed weapon supports shatter instead of yielding.
    sup = _supports(a)
    bad = 0
    for _, (t, b, host) in sup.items() if sup else []:
        h = host or b
        m = catalog.material(a.mat(h))
        if a.printed(h) and m is not None and m.brittle:
            bad += 1
            out.append(fail("arch.upright_brittle", G, WARNING, "Weapon upright in a brittle print material",
                            f"`{h.id}` carries the weapon and is {a.mat(h)}, which cracks instead of bending on a hit.").on(h.id)
                       .fix("Print weapon uprights in nylon, PETG or TPU-free tough blends, or use metal."))
    if sup:
        out += [] if bad else [ok("arch.upright_brittle", G, "Weapon uprights are tough", "No weapon support is a brittle print.")]
    return out


# --------------------------------------------------------------------------------------------------------------- motion groups

def motion(a):
    out = []
    spec = a.spec
    # Static parts parented to the rotor would spin with it.
    for wid, s in a.rotor.items():
        static = [pid for pid in s if pid != wid and a.part(pid).kind in STRUCT + ("battery", "esc", "receiver", "switch")]
        if static:
            out.append(fail("arch.static_on_rotor", G, BLOCKER, "Static part rides on the spinning weapon",
                            f"{', '.join('`' + x + '`' for x in static)} are children of the rotor `{wid}` and would spin with it.")
                       .on(wid, *static).fix("Parent structure to the chassis, not the weapon; declare `rotates_with: fixed`."))
        else:
            out.append(ok("arch.static_on_rotor", G, "Rotor carries only rotating parts", f"Rotor `{wid}`: {sorted(s)}."))
        wp = a.part(wid)
        if wp.joint is None or wp.joint.kind != "revolute":
            out.append(fail("arch.weapon_spin_joint", G, WARNING, "Weapon has no spin joint",
                            f"`{wid}` is fixed rigidly to `{wp.parent or 'the world'}`; nothing in the model says it turns, so "
                            "parts bolted across the spin boundary are not obvious.").on(wid)
                       .fix("Give the weapon a `revolute` joint about its spin axis (parent = the shaft or the support)."))
        else:
            out.append(ok("arch.weapon_spin_joint", G, "Weapon has a spin joint", f"`{wid}` turns on a revolute joint."))
    # Fasteners across a rotating/static boundary, by declaration and by geometry.
    if a.rotor:
        bad = 0
        rotor_bodies = [a.body(x) for s in a.rotor.values() for x in s if a.body(x) is not None]
        for f in a.fast:
            groups = {a.group_of(pid) for pid in a.coupled(f)} - {None}
            fb = a.body(f.id)
            hit = []
            if fb is not None:
                d, ln = catalog.parse_designation(f.designation)
                ax = _unit(f.dir)
                P = np.asarray(f.at, float) + np.outer(np.arange(0.2, ln, 0.3), ax)
                hit = [rb.id for rb in rotor_bodies if measure.aabb_overlap(rb.aabb, fb.aabb) and rb.inside(P).any()]
            if len(groups) > 1 or (hit and "fixed" in groups) or (hit and any(g not in (None,) and g not in [a.group_of(h) for h in hit] for g in groups)):
                bad += 1
                out.append(fail("arch.boundary_fasteners", G, BLOCKER, "Screw crosses the spinning/static boundary",
                                f"`{f.id}` couples {sorted(a.coupled(f))} (motion groups {sorted(groups)})"
                                f"{'; its shank passes through the spinning ' + ', '.join(hit) if hit else ''}. It shears off at spin-up.")
                           .on(f.id, *hit).here(f.at).fix("Fasten rotating parts only to rotating parts (or on the spin axis), static to static."))
        out += [] if bad else [ok("arch.boundary_fasteners", G, "No screw crosses the spin boundary", f"{len(a.fast)} fasteners checked.")]
    # Fasteners between parts that move relative to each other on a joint.
    bad, judged = 0, 0
    for f in a.fast:
        ids = a.coupled(f)
        moving = [i for i in ids if a.part(i) is not None and a.part(i).joint is not None and a.part(i).joint.kind != "fixed"
                  and (a.part(i).joint.max - a.part(i).joint.min) > 1e-6]
        for m in moving:
            judged += 1
            others = [i for i in ids if i != m and a.part(i) is not None and a.part(i).parent != m and a.part(m).parent == i]
            j = a.part(m).joint
            pb = a.body(a.part(m).parent) if a.part(m).parent else None
            piv = (pb.M[:3, :3] @ np.asarray(j.pivot, float) + pb.M[:3, 3]) if pb is not None else np.asarray(j.pivot, float)
            jax = _unit(pb.M[:3, :3] @ np.asarray(j.axis, float)) if pb is not None else _unit(j.axis)
            on_axis = abs(abs(_unit(f.dir) @ jax) - 1) < 0.05 and np.linalg.norm(np.cross(np.asarray(f.at) - piv, jax)) < 1.0
            if others and not on_axis:
                bad += 1
                out.append(fail("arch.fastener_spans_joint", G, BLOCKER, "Screw locks a moving joint",
                                f"`{f.id}` bolts `{m}` (a {j.kind} joint) to its parent `{others[0]}` off the joint axis, so the joint cannot move.")
                           .on(f.id, m).here(f.at).fix("Make the screw the pivot pin (on the joint axis) or remove the joint."))
    if not bad:
        out.append(ok("arch.fastener_spans_joint", G, "No screw locks a joint", f"{judged} fastener/joint pairs checked."))
    # Supports should hang on the chassis, not on each other.
    sup = _supports(a)
    for s, (t, b, host) in (sup or {}).items():
        h = host or b
        p = a.part(h.id)
        if p is None or h.id == a.chassis.id:
            continue
        par = a.part(p.parent) if p.parent else None
        if par is not None and par.id != a.chassis.id and (par.kind in STRUCT or par.kind == "fork") and par.id in [
                (x[2] or x[1]).id for x in sup.values()]:
            out.append(fail("arch.support_parent", G, WARNING, "Weapon support hangs on the other support",
                            f"`{h.id}` is parented to `{par.id}`, the opposite weapon support; moving one drags the other and the "
                            "tree no longer says both bolt to the chassis.").on(h.id, par.id).fix(f"Parent `{h.id}` to `{a.chassis.id}`."))
        else:
            out.append(ok("arch.support_parent", G, "Support parented sensibly", f"`{h.id}` parent: `{p.parent or 'world'}`."))
    return out


# --------------------------------------------------------------------------------------------------------------- weapon

def _supports(a):
    """{side: (t, support body (bearing or structure), structure host)} along the weapon shaft, cached; {} for none."""
    if hasattr(a, "_sup"):
        return a._sup
    a._sup, a._lay = {}, None
    ws = ph.weapons(a.ctx)
    if not ws:
        return a._sup
    p, wb, origin, axis = ws[0]
    a._weapon = (p, wb, origin, axis)
    lay = ph.shaft_layout(a.ctx, wb, origin, axis)
    a._lay = lay
    if lay is None:
        return a._sup
    sh = lay["shaft"]
    rot = a.rotor.get(p.id, set())
    tv = (sh.mesh.vertices - origin) @ axis
    ts = np.arange(float(tv.min()) + 0.1, float(tv.max()) - 0.1, 0.25)
    P = origin + np.outer(ts, axis)
    cands = [b for b in a.solids if b is not sh and b is not wb and b.id not in rot and b.kind in ph.SUPPORT + ("bearing",)
             and measure.aabb_overlap(b.aabb, sh.aabb)]
    ts = np.arange(float(tv.min()) + 0.1, float(tv.max()) - 0.1, 0.5)
    P = origin + np.outer(ts, axis)
    u_, v_ = _perp(axis)
    rr = lay["d"] / 2 + 0.5
    ring = [P + rr * (math.cos(k) * u_ + math.sin(k) * v_) for k in np.linspace(0, 2 * math.pi, 8, endpoint=False)]

    def hits(b, m):
        h = b.inside(P[m])
        n = sum(b.inside(R[m]).astype(int) for R in ring)
        return h | (n >= 5)  # a bearing / upright bore around the shaft: the axis itself is in the hole

    for s in (1.0, -1.0):
        m = ts * s > 0
        best = None
        for b in cands:
            hit = hits(b, m)
            if hit.any():
                tc = float(ts[m][hit].min() if s > 0 else ts[m][hit].max())
                if best is None or abs(tc) < abs(best[0]) - 1e-6 or (abs(tc - best[0]) < 1e-6 and b.kind == "bearing"):
                    best = (tc, b)
        if best is None:
            continue
        t, b = best
        hit = hits(b, m)
        t = float(ts[m][hit].mean())
        host = b
        if b.kind == "bearing":
            from .strength import _host

            od = 2 * float(ph.perp_radius(b.mesh.vertices, origin, axis).max())
            host = _host(a.ctx, b, origin, axis, t, od)
        a._sup[s] = (t, b, host)
    for s in (1.0, -1.0):
        if s not in a._sup:
            hub = _hub_support(a, p, sh, origin, axis, s)
            if hub is not None:
                a._sup[s] = hub
    return a._sup


def _hub_support(a, p, sh, origin, axis, s):
    """Motor-as-hub: the weapon motor's own bearings carry side `s` when `sh` is its own extended shaft and its stator is
    screwed to a static upright on that side (no shaft passes through the stator). (t, motor body, static host) or None."""
    mid = p.weapon.motor if p.weapon else None
    mb = a.body(mid) if mid else None
    if mb is None:
        return None
    try:
        from .kinematics import BOUNDARY, motor_hub

        own, static, k, _ = motor_hub(a.ctx, sh.id, mid)
    except Exception:  # noqa: BLE001
        return None
    if not (own and static):
        return None
    mt = (mb.mesh.vertices - origin) @ axis
    t = float(mt.mean())
    if t * s <= 0:
        return None
    held = [o for mm, o, _ in k.stator_links if mm == mid] + [o for mm, o, *_ in k.rotor_links if mm == mid]
    hosts = [a.body(o) for o in held if k.rot(o) is None and k.kind(o) not in BOUNDARY and a.body(o) is not None]
    if not hosts:
        return None
    return (t, mb, hosts[0])


def weapon(a):
    out = []
    ws = ph.weapons(a.ctx)
    if not ws:
        return [ok("arch.weapon_supports", G, "No spinning weapon", "No spinning weapon: fork and shaft checks do not apply.")]
    p, wb, origin, axis = ws[0]
    sup = _supports(a)
    lay = a._lay
    if lay is None:
        a.ctx.not_checked.append(f"Weapon architecture of `{p.id}`: no shaft body through the weapon centre")
        return [fail("arch.weapon_supports", G, BLOCKER, "Weapon has no shaft",
                     f"No `shaft` part passes through the centre of `{p.id}`, so nothing carries it to the chassis.").on(p.id)
                .fix("Add the weapon shaft as a `shaft` part through the weapon and both supports.")]
    sh, d = lay["shaft"], lay["d"]
    # Supports on both sides.
    if len(sup) < 2:
        sev = BLOCKER if p.weapon.supported_both_ends else WARNING
        out.append(fail("arch.weapon_supports", G, sev, "Weapon supported on one side only",
                        f"`{p.id}` has a support only on side {list(sup) or 'none'} of the disc"
                        f"{' although `supported_both_ends` is declared' if p.weapon.supported_both_ends else ''}; it is a cantilever.")
                   .on(p.id, sh.id).fix("Carry the shaft in a bearing or boss on both sides of the weapon."))
    else:
        out.append(ok("arch.weapon_supports", G, "Weapon supported both sides",
                      f"Supports at {sup[-1.0][0]:.1f} and {sup[1.0][0]:.1f} mm along the axis: `{sup[-1.0][1].id}`, `{sup[1.0][1].id}`."))
    # Fork orientation: each host on its own side, tine reaching back toward the chassis.
    cc = a.chassis.center - origin
    cperp = cc - axis * (cc @ axis)
    for s, (t, b, host) in sup.items():
        h = host or b
        if h is None:
            a.ctx.not_checked.append(f"Fork orientation side {s:+.0f}: no structure holds the support")
            continue
        hc = (h.mesh.vertices.mean(axis=0) if h.geom.volume <= 0 else h.center) - origin
        if h.id == a.chassis.id:
            hc = h.mesh.vertices[np.abs((h.mesh.vertices - origin) @ axis - t) < 6].mean(axis=0) - origin if np.any(
                np.abs((h.mesh.vertices - origin) @ axis - t) < 6) else hc
        tc = float(hc @ axis)
        hperp = hc - axis * tc
        both_sides_one_body = len(sup) == 2 and (sup[1.0][2] or sup[1.0][1]) is (sup[-1.0][2] or sup[-1.0][1])
        crosses = (not both_sides_one_body) and tc * s < -2.0
        away = np.linalg.norm(cperp) > 1 and np.linalg.norm(hperp) > 1 and float(_unit(hperp) @ _unit(cperp)) < -0.2
        msg = (f"`{h.id}` holds side {s:+.0f} at {t:.1f} mm; its body centre sits {tc:.1f} mm along the axis and points "
               f"{'away from' if away else 'toward'} the chassis from the axle.")
        if crosses or away:
            out.append(fail("arch.fork_orientation", G, BLOCKER, "Weapon fork points the wrong way", msg +
                            (" It reaches across the weapon to the other side (inside-out)." if crosses else
                             " The tine hangs out beyond the axle instead of running back to the tub."))
                       .on(h.id, p.id).fix("Mirror the fork so each tine is on its own side of the weapon and runs from the tub forward to the axle boss."))
        else:
            out.append(ok("arch.fork_orientation", G, "Fork tine points at the axle", msg))
    # Boss / bearing seat around the axis on each side.
    r_sh = d / 2
    for s, (t, b, host) in sup.items():
        c = origin + axis * t
        if b.kind == "bearing":
            od = 2 * float(ph.perp_radius(b.mesh.vertices, origin, axis).max())
            off = float(np.linalg.norm(np.cross(b.center - origin, axis)))
            if off > 0.3:
                out.append(fail("arch.bearing_coaxial", G, BLOCKER, "Bearing off the weapon axis",
                                f"`{b.id}` centre is {off:.2f} mm off the spin axis; the shaft binds.").on(b.id).expect("<= 0.3 mm", f"{off:.2f} mm"))
            else:
                out.append(ok("arch.bearing_coaxial", G, "Bearing on axis", f"`{b.id}` is {off:.2f} mm off the axis."))
            if host is None:
                out.append(fail("arch.bearing_seat", G, BLOCKER, "Bearing not held", f"No structure surrounds `{b.id}`.").on(b.id)
                           .fix("Seat the bearing in a pocket in the upright."))
                continue
            cov = float(host.inside(_ring(c, axis, od / 2 + 0.6)).mean())
            m = f"`{host.id}` surrounds {cov * 100:.0f} % of `{b.id}` (Ø{od:.1f})."
            if cov < 0.75:
                out.append(fail("arch.bearing_seat", G, BLOCKER if cov < 0.3 else WARNING, "Bearing seat is open", m)
                           .on(b.id, host.id).expect(">= 75 %", f"{cov * 100:.0f} %").fix("Close the bearing pocket around the outer race."))
            else:
                out.append(ok("arch.bearing_seat", G, "Bearing seated", m))
        else:
            cov = float(b.inside(_ring(c, axis, r_sh + 0.6)).mean())
            m = f"`{b.id}` surrounds {cov * 100:.0f} % of the shaft at {t:.1f} mm."
            if cov < 0.75:
                out.append(fail("arch.boss_aligned", G, BLOCKER if cov < 0.3 else WARNING, "Axle boss misaligned or open", m)
                           .on(b.id, sh.id).expect(">= 75 %", f"{cov * 100:.0f} %").fix("Centre the boss hole on the weapon axis on both forks."))
            else:
                out.append(ok("arch.boss_aligned", G, "Axle boss aligned", m))
    # Shaft span and support gaps.
    if len(sup) == 2:
        ta, tb = sup[-1.0][0], sup[1.0][0]
        span = tb - ta
        ratio = span / max(d, 1e-6)
        a.ctx.metrics["arch_shaft_span_over_d"] = ratio
        m = f"`{sh.id}` Ø{d:.1f} mm spans {span:.1f} mm between supports (L/d = {ratio:.1f})."
        if ratio > SHAFT_SPAN_D:
            out.append(fail("arch.shaft_span", G, WARNING, "Weapon shaft span too long for its diameter", m).on(sh.id)
                       .expect(f"L/d <= {SHAFT_SPAN_D:.0f}", f"{ratio:.1f}").fix("Bring the supports in or use a thicker shaft."))
        else:
            out.append(ok("arch.shaft_span", G, "Shaft span is short", m))
        rot_ids = set(a.rotor.get(p.id, {p.id})) | ({p.weapon.motor} if p.weapon.motor else set())
        Vr = np.vstack([a.body(x).mesh.vertices for x in rot_ids if a.body(x) is not None and a.part(x).kind not in ("bearing",)])
        wt = (Vr - origin) @ axis
        dt = (wb.mesh.vertices - origin) @ axis
        mid = (float(dt.min()) + float(dt.max())) / 2
        off = mid - (ta + tb) / 2
        decl = bool(_extra(p.weapon, "offset_ok")) or p.id in set(a.spec.raw.get("asymmetric") or []) or bool(_extra(p, "asymmetric"))
        a.ctx.metrics["arch_weapon_lateral_offset_mm"] = off
        m = f"`{p.id}` mid-plane is {off:+.1f} mm from the midpoint between its supports ({ta:.1f} / {tb:.1f} mm)."
        if abs(off) >= 1.0 and not decl:
            out.append(fail("arch.weapon_centred", G, WARNING, "Weapon not centred between its supports", m).on(p.id)
                       .expect("|offset| < 1 mm", f"{off:+.1f} mm")
                       .fix("Centre the disc between the uprights, or declare `asymmetric: true` on the weapon (bearing loads then differ)."))
        else:
            out.append(ok("arch.weapon_centred", G, "Weapon centred" if abs(off) < 1 else "Weapon offset declared", m))
        gaps = (float(wt.min()) - ta, tb - float(wt.max()))
        g = max(gaps)
        m = f"Clear shaft between the weapon faces and the supports: {gaps[0]:.1f} / {gaps[1]:.1f} mm (shaft Ø{d:.1f})."
        if g > 2.5 * d:
            out.append(fail("arch.weapon_support_gap", G, WARNING, "Supports far from the weapon", m).on(sh.id, p.id)
                       .expect(f"<= {2.5 * d:.1f} mm", f"{g:.1f} mm").fix("Move the bearings next to the hub; spacers close the gap."))
        else:
            out.append(ok("arch.weapon_support_gap", G, "Supports close to the weapon", m))
    # Shaft material.
    shm = catalog.material(a.mat(sh))
    if a.printed(sh) or (shm is not None and shm.cls != "metal"):
        out.append(fail("arch.shaft_material", G, BLOCKER, "Weapon shaft is not metal", f"`{sh.id}` is {a.mat(sh)} ({a.part(sh.id).process}).")
                   .on(sh.id).fix("Use a hardened steel or titanium shaft."))
    elif shm is None:
        a.ctx.not_checked.append(f"Shaft `{sh.id}` material unknown")
    else:
        out.append(ok("arch.shaft_material", G, "Weapon shaft is metal", f"`{sh.id}` is {a.mat(sh)}."))
    # Shaft axial retention: something beyond both ends of the shaft, or a declared joint.
    tsh = (sh.mesh.vertices - origin) @ axis
    ends = [origin + axis * (float(tsh.min()) - 0.4), origin + axis * (float(tsh.max()) + 0.4)]
    held = []
    for e in ends:
        hit = [b.id for b in a.bodies if b is not sh and b.id != p.id and b.inside(e[None])[0]]
        held.append(bool(hit))
    declared = any(c.method in ("press_fit", "glue", "pin", "screw") for c in a.conns(sh.id))
    m = f"`{sh.id}` ends: {'capped' if held[0] else 'open'} / {'capped' if held[1] else 'open'}; declared retention: {declared}."
    if not (all(held) or declared or any(held)):
        out.append(fail("arch.shaft_retention", G, WARNING, "Weapon shaft can walk out", m).on(sh.id)
                   .fix("Cap the shaft ends (a blind boss, a bolt head, a collar) or declare a press fit / clamp."))
    else:
        out.append(ok("arch.shaft_retention", G, "Shaft is retained axially", m))
    # Bearings in the thick outer uprights, not idle thick walls beyond them.
    for s, (t, b, host) in sup.items():
        h = host or b
        far = np.arange(abs(t), abs(t) + 40, 0.5) * s
        P = origin + np.outer(far, axis)
        thick = {}
        for x in a.solids:
            if x.kind not in STRUCT or x is sh:
                continue
            n = int(x.inside(P).sum())
            if n:
                thick[x.id] = n * 0.5
        mine = thick.get(h.id, 0.0)
        other = max(((k, v) for k, v in thick.items() if k != h.id), key=lambda kv: kv[1], default=None)
        if other and other[1] >= 1.5 * max(mine, 0.5) and other[1] >= 4:
            out.append(fail("arch.bearing_upright_choice", G, WARNING, "Weapon carried by the thin upright",
                            f"Side {s:+.0f}: `{h.id}` ({mine:.1f} mm of wall on the axis) carries the weapon while `{other[0]}` "
                            f"({other[1]:.1f} mm) further out on the same axis carries nothing.").on(h.id, other[0])
                       .fix(f"Put the bearing or shaft clamp in `{other[0]}` and tie the uprights together."))
        else:
            out.append(ok("arch.bearing_upright_choice", G, "Weapon in the stoutest upright", f"Side {s:+.0f}: `{h.id}` ({mine:.1f} mm on axis)."))
    out += double_bearing(a, p, wb, origin, axis, sh)
    out += motor_in_hub(a, p, wb, origin, axis)
    out += load_path(a, p, origin, axis, sup)
    out += fork_stiffness(a, origin, axis, sup)
    return out


def double_bearing(a, p, wb, origin, axis, sh):
    out = []
    mid = p.weapon.motor
    mb = a.body(mid) if mid else None
    if mb is None or mb.part_idx is None:
        return [ok("arch.double_bearing", G, "No weapon motor on the shaft", f"`{p.id}` names no weapon motor; one bearing system.")]
    rp = a.r.parts[mb.part_idx]
    if rp.cat is None or rp.cat.shaft is None:
        a.ctx.not_checked.append(f"Double bearing check: `{mid}` has no catalog shaft")
        return out
    mdir = _unit(mb.M[:3, :3] @ np.asarray(rp.cat.shaft["dir"], float))
    coax = abs(abs(mdir @ axis) - 1) < 0.02 and np.linalg.norm(np.cross(mb.M[:3, 3] - origin, axis)) < 1.0
    hits = measure.aabb_overlap(sh.aabb, mb.aabb) and mb.inside(origin + np.outer(np.linspace(-30, 30, 121), axis)).any()
    flexible = any(c.method in ("flexible_coupling",) or _extra(c, "coupling") == "flexible" for c in a.conns(mid))
    declared = bool(_extra(a.part(mid), "motor_shaft_removed"))
    if hits and not coax:
        out.append(fail("arch.double_bearing", G, BLOCKER, "Weapon shaft runs through the motor off its axis",
                        f"`{sh.id}` passes through `{mid}` but the motor shaft is not coaxial with the weapon axis.").on(sh.id, mid))
    elif hits and coax and not (flexible or declared) and _hub_ok(a, p, mid, sh, out):
        pass
    elif hits and coax and not (flexible or declared):
        out.append(fail("arch.double_bearing", G, BLOCKER, "Rotor on two bearing systems",
                        f"`{p.id}` runs on external bearings on `{sh.id}` and `{sh.id}` also runs through `{mid}`, which has its own "
                        "shaft and bearings: overconstrained, any misalignment loads the motor bearings.").on(p.id, sh.id, mid)
                   .fix("Pick one: live shaft + belt, or a dead shaft hub motor (declare `motor_shaft_removed: true` on the motor)."))
    else:
        out.append(ok("arch.double_bearing", G, "One bearing system on the rotor",
                      f"`{mid}` {'is a declared hub-motor conversion' if declared else 'does not share the weapon shaft'}."))
    return out


def _hub_ok(a, p, mid, sh, out):
    """Motor-as-hub (same rule as kin.double_bearing): the weapon shaft is the motor's own extended shaft, the stator is
    bolted to structure, and exactly ONE extra bearing carries the far end, coaxial with the motor shaft. Appends the
    verdict and returns True when the motor-as-hub reading applies (pass or fail), False to fall back to the plain rule."""
    from .kinematics import COAX_DEG, HUB_COAX_MM, coax, motor_hub, round_axis

    own, static, k, why = motor_hub(a.ctx, sh.id, mid)
    if not own or not static:
        return False
    mi = k.motor_info(mid)
    rotor = set(a.rotor.get(p.id, {p.id})) | {sh.id}
    brgs = sorted({x.id for x in a.spec.parts if x.kind == "bearing"
                   for c in a.conns(x.id) if (c.b if c.a == x.id else c.a) in rotor})
    offs = []
    for bp in brgs:
        bb = a.body(bp)
        ra = round_axis(bb) if bb is not None else None
        ang, d = coax(mi["o"], mi["d"], ra[0], ra[1]) if ra is not None else (90.0, 99.0)
        if ang > COAX_DEG or d > HUB_COAX_MM:
            offs.append(f"`{bp}` {d:.2f} mm / {ang:.2f} deg")
    if len(brgs) == 1 and not offs:
        out.append(ok("arch.double_bearing", G, "Motor-as-hub on one extra bearing",
                      f"{why}; its stator is bolted to structure and one coaxial bearing `{brgs[0]}` carries the far end."))
    else:
        out.append(fail("arch.double_bearing", G, BLOCKER, "Extra bearing fights the motor's bearings",
                        f"`{p.id}` runs on `{mid}`'s own shaft `{sh.id}` plus {len(brgs)} extra bearing(s) "
                        + (f"off the motor axis ({', '.join(offs)}; allowed {HUB_COAX_MM} mm)" if offs else "(exactly one coaxial extra bearing is allowed)")
                        + ": two bearing systems that are not one line load each other.").on(p.id, sh.id, mid, *brgs)
                   .fix("Keep one flanged bearing in the opposite upright, bored on the motor axis."))
    return True


def motor_in_hub(a, p, wb, origin, axis):
    """When the archetype wants the outrunner inside the hub: coaxial and inside the rotor's axial envelope."""
    name = a.spec.raw.get("archetype")
    if not name:
        return []
    try:
        from . import archetype as arc

        _, P = arc.params_for(name, a.spec.raw.get("archetype_params") or {})
    except Exception:  # noqa: BLE001
        return []
    acc = P.get("weapon_drive") or ()
    if "inside_hub" not in acc:
        return []
    mb = a.body(p.weapon.motor) if p.weapon.motor else None
    if mb is None:
        a.ctx.not_checked.append("Motor-in-hub: no weapon motor named")
        return []
    rp = a.r.parts[mb.part_idx]
    if rp.cat is None or rp.cat.shaft is None:
        return []
    mdir = _unit(mb.M[:3, :3] @ np.asarray(rp.cat.shaft["dir"], float))
    mc = mb.M[:3, 3]
    off = float(np.linalg.norm(np.cross(mc - origin, axis)))
    coax = abs(abs(mdir @ axis) - 1) < 0.02 and off < 0.5
    rot = [a.body(x) for x in a.rotor.get(p.id, {p.id}) if a.body(x) is not None and a.part(x).kind != "bearing"]
    rt = np.concatenate([(b.mesh.vertices - origin) @ axis for b in rot])
    mt = (mb.mesh.vertices - origin) @ axis
    lo, hi = float(rt.min()), float(rt.max())
    inside = max(0.0, min(hi, float(mt.max())) - max(lo, float(mt.min()))) / max(float(np.ptp(mt)), 1e-6)
    belt = any(x.kind == "belt" and p.weapon.motor in str(x.belt.pulleys if x.belt else "") for x in a.spec.parts)
    m = f"`{mb.id}` axis {off:.2f} mm off the spin axis, {inside * 100:.0f} % of its length inside the rotor envelope."
    if coax and inside >= 0.5:
        return [ok("arch.weapon_motor_in_hub", G, "Weapon motor inside the hub", m)]
    if belt and "belt_tensioned" in acc:
        return [ok("arch.weapon_motor_in_hub", G, "Weapon belt-driven", m + " Belt drive accepted by the archetype.")]
    return [fail("arch.weapon_motor_in_hub", G, WARNING, "Weapon motor not in the hub", m).on(mb.id, p.id)
            .fix("Put the outrunner coaxial inside the hub (stator on the dead shaft), or belt-drive it.")]


def pods_enclose(a):
    """Each wheel sits inside a side pod's envelope in the side and top views."""
    out = []
    from shapely.geometry import MultiPoint as MP

    pods_ = [b for b in a.solids if re.search(r"pod", b.id) and b.kind in STRUCT]
    if not pods_:
        return out
    for wb in a.solids:
        if wb.kind != "wheel":
            continue
        best = None
        for pb in pods_:
            if np.sign(pb.center[0]) != np.sign(wb.center[0]):
                continue
            cov = []
            for dims in ((1, 2), (0, 1)):  # side (YZ), top (XY)
                wh = MP([tuple(v) for v in wb.mesh.vertices[:, dims]]).convex_hull
                ph_ = MP([tuple(v) for v in pb.mesh.vertices[:, dims]]).convex_hull
                cov.append(wh.intersection(ph_).area / max(wh.area, 1e-9))
            if best is None or min(cov) > min(best[1]):
                best = (pb.id, cov)
        if best is None:
            out.append(fail("arch.pods_enclose", G, WARNING, "Wheel has no side pod", f"`{wb.id}` has no pod on its side.").on(wb.id))
            continue
        m = f"`{wb.id}` is {best[1][0] * 100:.0f} % covered by `{best[0]}` in the side view and {best[1][1] * 100:.0f} % in the top view."
        if min(best[1]) < 0.6:
            out.append(fail("arch.pods_enclose", G, WARNING, "Wheel sticks out of its pod", m).on(wb.id, best[0])
                       .expect(">= 60 % in both views", f"{min(best[1]) * 100:.0f} %").fix("Grow the pod around the wheel (leave only the contact patch exposed)."))
        else:
            out.append(ok("arch.pods_enclose", G, "Wheel enclosed by its pod", m))
    return out


def _graph(a, kinds=STRUCT + ("insert", "nut", "bearing")):
    nodes = [b for b in a.solids if b.kind in kinds]
    adj = {b.id: set() for b in nodes}
    for x, y in combinations(nodes, 2):
        if a.between(x.id, y.id) or a.contact(x, y):
            adj[x.id].add(y.id)
            adj[y.id].add(x.id)
    return adj


def load_path(a, p, origin, axis, sup):
    out = []
    if not sup:
        return out
    adj = _graph(a)
    ch = a.chassis.id
    for s, (t, b, host) in sup.items():
        start = (host or b).id
        prev = {start: None}
        q = [start]
        while q:
            x = q.pop(0)
            if x == ch:
                break
            for y in sorted(adj.get(x, ())):
                if y not in prev and a.part(y) is not None and a.part(y).kind not in ("bearing",):
                    prev[y] = x
                    q.append(y)
        if ch not in prev:
            out.append(fail("arch.load_path", G, BLOCKER, "Weapon load does not reach the chassis",
                            f"Side {s:+.0f}: from `{start}` no chain of touching or bolted structure reaches `{ch}`.").on(start, ch)
                       .fix("Bolt or seat the weapon uprights directly on the tub floor/walls."))
            continue
        path, x = [], ch
        while x is not None:
            path.append(x)
            x = prev[x]
        path.reverse()
        out.append(ok("arch.load_path", G, "Weapon load reaches the chassis", f"Side {s:+.0f}: shaft → " + " → ".join(path)))
        R = a.F / max(len(sup), 1)
        for u, v in zip(path, path[1:]):
            bu, bv = a.body(u), a.body(v)
            fs = a.between(u, v)
            area = max(a.area(bu, bv), a.area(bv, bu)) if a.contact(bu, bv) else 0.0
            # Bolts only, one small one: the whole reaction on one screw.
            if fs and len(fs) == 1 and catalog.parse_designation(fs[0].designation)[0] <= 2.05 and area < 20:
                out.append(fail("arch.load_path_fasteners", G, BLOCKER, "Weapon load hangs on a lone M2",
                                f"`{u}`→`{v}` is held by `{fs[0].id}` only (contact {area:.0f} mm²); {R:.0f} N goes through one M2.")
                           .on(u, v, fs[0].id).fix("Seat the upright on the floor (bearing surface) and use ≥ 2 bolts ≥ M2.5."))
            elif not fs and area < 5 and not a.conns(u, v):
                out.append(fail("arch.load_path_fasteners", G, WARNING, "Load-path joint held by contact only",
                                f"`{u}`→`{v}` touch over {area:.0f} mm² with no bolt or declared connection.").on(u, v))
            else:
                out.append(ok("arch.load_path_fasteners", G, "Load-path joint is bolted or seated",
                              f"`{u}`→`{v}`: {len(fs)} bolts, {area:.0f} mm² contact."))
            # Material under the bolts on this joint.
            for f in fs:
                d, ln = catalog.parse_designation(f.designation)
                ax = _unit(f.dir)
                P = np.asarray(f.at, float) + np.outer(np.arange(0.05, ln, 0.1), ax)
                for pid in (u, v):
                    pb = a.body(pid)
                    if pb is None or not a.printed(pb):
                        continue
                    th = float(pb.inside(P).sum()) * 0.1
                    if 0 < th < MIN_LAYER_MM:
                        out.append(fail("arch.load_path_thin", G, BLOCKER, "Load path through a thin printed skin",
                                        f"`{f.id}` grips only {th:.1f} mm of `{pid}`: a few layers carry {R:.0f} N.").on(f.id, pid).here(f.at)
                                   .expect(f">= {MIN_LAYER_MM} mm", f"{th:.1f} mm").fix("Thicken the floor/flange under the bolt to ≥ 2.5 mm."))
                    elif th > 0:
                        out.append(ok("arch.load_path_thin", G, "Load-path flange thick enough", f"`{f.id}` grips {th:.1f} mm of `{pid}`."))
    return out


def fork_stiffness(a, origin, axis, sup):
    out = []
    for s, (t, b, host) in sup.items():
        h = host or b
        if h is None or h.id == a.chassis.id:
            continue
        mp = catalog.mech(a.mat(h))
        if mp is None:
            a.ctx.not_checked.append(f"Fork stiffness of `{h.id}`: unknown modulus")
            continue
        E = mp[2] * 1e3
        boss = origin + axis * t
        # Root: centroid of the contact with the chassis or of its bolts.
        fs = a.fasteners_of(h.id)
        pts = [np.asarray(f.at, float) for f in fs if a.chassis.id in a.coupled(f)]
        if not pts:
            near = h.mesh.vertices[a.chassis.distance(h.mesh.vertices[:2000]) < 0.5] if len(h.mesh.vertices) else []
            pts = list(near)
        if not len(pts):
            a.ctx.not_checked.append(f"Fork stiffness of `{h.id}`: no root on the chassis found")
            continue
        root = np.mean(pts, axis=0)
        lever = boss - root
        lever -= axis * (lever @ axis)
        L = float(np.linalg.norm(lever))
        if L < 2:
            out.append(ok("arch.fork_stiffness", G, "Fork is short", f"`{h.id}` axle is {L:.1f} mm from its root."))
            continue
        ld = _unit(lever)
        load = _unit(np.cross(axis, ld))  # bending in the plane of the fork
        Imin = None
        for k in np.linspace(0.15, 0.85, 6):
            c = root + lever * k
            poly = _plane_section(h.mesh, c, ld, axis)  # u = along the axle, v = load direction (n x u)
            if poly is None:
                continue
            poly = poly.intersection(Point(0, 0).buffer(30))
            if poly.is_empty:
                continue
            from .strength import section_modulus

            I, _, A_ = section_modulus(poly)
            if I > 0 and (Imin is None or I < Imin):
                Imin = I
        if Imin is None:
            a.ctx.not_checked.append(f"Fork stiffness of `{h.id}`: no cross-section between root and axle")
            continue
        R = a.F / max(len(sup), 1)
        defl = R * L ** 3 / (3 * E * Imin)
        a.ctx.metrics[f"arch_fork_deflection_mm.{h.id}"] = defl
        m = f"`{h.id}`: {R:.0f} N at the axle, lever {L:.1f} mm, weakest I {Imin:.0f} mm⁴, E {E / 1e3:.1f} GPa → {defl:.2f} mm."
        if defl > FORK_DEFL_MM:
            out.append(fail("arch.fork_stiffness", G, BLOCKER if defl > FORK_DEFL_BLOCK_MM else WARNING, "Fork flexes on a hit", m)
                       .on(h.id).expect(f"<= {FORK_DEFL_MM} mm", f"{defl:.2f} mm").fix("Shorten the fork, deepen its section or tie both forks with a crossbar."))
        else:
            out.append(ok("arch.fork_stiffness", G, "Fork is stiff", m))
    return out


# --------------------------------------------------------------------------------------------------------------- motors

def _clamp_axes(a, b, structs, gap=0.8):
    """Axes (0..2) on which structure touches the body on both sides, and the directions blocked."""
    pts, nrm = b.surface(1.0)
    blocked = set()
    for k, d in enumerate([(1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1)]):
        sel = nrm @ np.asarray(d, float) > 0.8
        if not sel.any():
            continue
        P = pts[sel][:400] + np.asarray(d, float) * gap
        for s in structs:
            if measure.aabb_overlap(s.aabb, b.aabb, gap + 0.1) and s.inside(P).any():
                blocked.add(k)
                break
    axes = [i for i in range(3) if 2 * i in blocked and 2 * i + 1 in blocked]
    return axes, blocked


def _clamp_bodies(a, b, structs, gap=0.8):
    """Structure bodies touching the motor surface."""
    pts, nrm = b.surface(1.0)
    P = (pts + nrm * gap)[::3]
    return [s.id for s in structs if measure.aabb_overlap(s.aabb, b.aabb, gap + 0.1) and s.inside(P).any()]


def motors(a):
    out = []
    if not any(f.threads_into and a.part(f.threads_into) is not None and a.part(f.threads_into).kind in ("motor", "weapon_motor")
               for f in a.fast):
        out.append(ok("arch.motor_face_bolts", G, "No screws into motors", "No fastener threads into a motor."))
        out.append(ok("arch.motor_face_static", G, "No screws into motors", "No fastener threads into a weapon motor."))
    structs = [b for b in a.solids if b.kind in STRUCT]
    for b in a.solids:
        if b.kind not in ("motor", "weapon_motor"):
            continue
        p = a.part(b.id)
        rp = a.r.parts[b.part_idx]
        fs = a.fasteners_of(b.id)
        into = [f for f in fs if f.threads_into == b.id]
        cons = a.conns(b.id)
        clamp_cons = [c for c in cons if c.method in ("screw", "interlock", "snap") and a.body(c.a if c.b == b.id else c.b) is not None
                      and a.part(c.a if c.b == b.id else c.b).kind in STRUCT]
        struct_cons = [c for c in cons if a.part(c.a if c.b == b.id else c.b) is not None and a.part(c.a if c.b == b.id else c.b).kind in STRUCT]
        axes, blocked = _clamp_axes(a, b, structs)
        holders = _clamp_bodies(a, b, structs)
        sandwich = len(holders) >= 2 and any(a.between(x, y) for x, y in combinations(holders, 2)) and len(axes) >= 2
        # Mount method.
        if not fs and not clamp_cons and not sandwich and struct_cons and all(c.method in ("press_fit", "glue", "tape", "velcro") for c in struct_cons):
            out.append(fail("arch.motor_mount", G, BLOCKER, "Motor held by press fit alone",
                            f"`{b.id}` is held to {[c.a if c.b == b.id else c.b for c in struct_cons]} only by "
                            f"{sorted({c.method for c in struct_cons})}; drive torque and hits walk it out.").on(b.id)
                       .fix("Clamp it with a screwed strap/cap (2x M2) or screw its face into a boss."))
        elif not fs and not struct_cons and not sandwich:
            out.append(fail("arch.motor_mount", G, BLOCKER, "Motor mount not declared",
                            f"`{b.id}` has no fasteners, no clamp between bolted halves and no connection to the structure.").on(b.id)
                       .fix("Bolt the motor face or add a clamp, and declare it."))
        else:
            out.append(ok("arch.motor_mount", G, "Motor is screwed or clamped",
                          f"`{b.id}`: {len(fs)} fasteners, {len(clamp_cons)} clamps, sandwiched between {holders if sandwich else 'nothing'}."))
        # Clamped in >= 2 directions.
        m = f"`{b.id}`: structure on both sides along {['XYZ'[i] for i in axes] or 'no axis'}; {len(into)} screws in its face."
        if len(axes) >= 2 or (len(axes) >= 1 and len(into) >= 2) or len(into) >= 2:
            out.append(ok("arch.motor_clamp", G, "Motor is captured", m))
        else:
            out.append(fail("arch.motor_clamp", G, BLOCKER if not blocked and not into else WARNING, "Motor not captured", m).on(b.id)
                       .fix("Box the motor between walls on two axes, or screw its face."))
        # Anti-rotation about its own shaft.
        if rp.cat is not None and rp.cat.shaft is not None:
            sax = _unit(b.M[:3, :3] @ np.asarray(rp.cat.shaft["dir"], float))
            rr = ph.perp_radius(b.mesh.vertices, b.M[:3, 3], sax)
            rr = rr[rr > 0.5 * rr.max()]
            noncirc = len(rr) > 3 and float(rr.min()) < 0.9 * float(rr.max())
            keyed = any(c.mechanical_key for c in struct_cons)
            flats = noncirc and len(axes) >= 1
            if len(into) >= 2 or keyed or flats:
                out.append(ok("arch.motor_antirotation", G, "Motor cannot turn in its mount",
                              f"`{b.id}`: {len(into)} face screws, keyed {keyed}, flats held {flats}."))
            else:
                out.append(fail("arch.motor_antirotation", G, BLOCKER if b.kind == "weapon_motor" else WARNING,
                                "Nothing stops the motor turning", f"`{b.id}` is round in its mount with {len(into)} face screws and no key.")
                           .on(b.id).fix("Use ≥ 2 face screws, clamp on the gearbox flats, or key the can."))
            # Face screws: into the motor, at the stator end, not too deep.
            for f in fs:
                d, ln = catalog.parse_designation(f.designation)
                ax = _unit(f.dir)
                tip = np.asarray(f.at, float) + ax * ln
                in_motor = bool(b.inside(tip[None])[0])
                if in_motor and f.threads_into != b.id:
                    out.append(fail("arch.motor_face_bolts", G, BLOCKER, "Motor screw threads into plastic",
                                    f"`{f.id}` ends inside `{b.id}` but is declared to thread into `{f.threads_into}`.").on(f.id, b.id).here(tip))
                    continue
                if f.threads_into != b.id:
                    continue
                P = np.asarray(f.at, float) + np.outer(np.arange(0.05, ln, 0.1), ax)
                eng = float(b.inside(P).sum()) * 0.1
                lim = float(rp.cat.props.get("thread_depth_mm", MOTOR_THREAD_DEPTH[b.kind]))
                m = f"`{f.id}` engages {eng:.1f} mm of `{b.id}` (usable {lim:.1f} mm, need ≥ {0.8 * d:.1f})."
                if eng > lim + 0.3:
                    out.append(fail("arch.motor_face_bolts", G, BLOCKER, "Motor screw too long", m + " It hits the windings.")
                               .on(f.id, b.id).here(tip).expect(f"<= {lim:.1f} mm", f"{eng:.1f} mm").fix("Use a shorter screw or a spacer."))
                elif eng < 0.8 * d:
                    out.append(fail("arch.motor_face_bolts", G, WARNING, "Motor screw barely engages", m).on(f.id, b.id).here(tip))
                else:
                    out.append(ok("arch.motor_face_bolts", G, "Motor face screw engagement ok", m))
                if b.kind == "weapon_motor":
                    loc = (np.linalg.inv(b.M) @ np.append(tip, 1.0))[:3]
                    sd = np.asarray(rp.cat.shaft["dir"], float)
                    sf_decl = _extra(p, "stator_face")  # "+x"/"-x"/...: local side of the stator mount face
                    if sf_decl:
                        sd = -np.asarray({"x": [1, 0, 0], "y": [0, 1, 0], "z": [0, 0, 1]}[sf_decl[-1]], float) * (1 if sf_decl[0] == "+" else -1)
                    half = float(np.ptp(rp.geom.mesh.vertices @ sd)) / 2 if hasattr(rp.geom, "mesh") else 7.0
                    cen = float(rp.geom.mesh.vertices.mean(axis=0) @ sd) if hasattr(rp.geom, "mesh") else 0.0
                    x = float(loc @ sd) - cen  # > 0: toward the shaft output (bell) face
                    at_bell = x > 0
                    grp = {a.group_of(i) for i in a.coupled(f) if i != b.id} - {None}
                    rotating = any(g_ != "fixed" for g_ in grp)
                    want = "bell" if rotating else "stator"
                    got = "bell" if at_bell else "stator"
                    msg = (f"`{f.id}` ({'rotating' if rotating else 'static'} side) ends in the {got} half of `{b.id}`"
                           f"{' (stator face declared ' + sf_decl + ')' if sf_decl else ' (stator face = opposite the catalog shaft output)'}.")
                    if want != got:
                        out.append(fail("arch.motor_face_static", G, BLOCKER, f"Screw into the motor's {got} from the {'rotating' if rotating else 'static'} side",
                                        msg).on(f.id, b.id).here(tip)
                                   .fix("Static parts bolt to the stator face, rotating parts to the bell; set `stator_face` on the motor if the catalog orientation is wrong."))
                    else:
                        out.append(ok("arch.motor_face_static", G, "Motor screw on the matching face", msg))
        else:
            a.ctx.not_checked.append(f"Motor `{b.id}`: no catalog shaft, anti-rotation and face screws not judged")
    return out


# --------------------------------------------------------------------------------------------------------------- fasteners

def _grade(f):
    g = str(_extra(f, "grade", DEFAULT_GRADE)).lower()
    return g if g in GRADE_SHEAR else DEFAULT_GRADE


def _as(d):
    p = PITCH.get(round(d, 1), 0.2 * d)
    return math.pi / 4 * (d - 0.9382 * p) ** 2


def _group_load(a, ids):
    """Design load (N) a bolt group carries: the full impact for exposed or weapon-path parts, else 100 g on its own mass."""
    sup = _supports(a)
    path = {(x[2] or x[1]).id for x in sup.values()} if sup else set()
    exposed = [i for i in ids if a.part(i) is not None and (a.part(i).kind in ("wedge", "armor", "fork", "weapon_motor") or i in path)]
    if exposed:
        return a.F, f"design impact {a.F:.0f} N on `{exposed[0]}`"
    ms = [a.mass(a.body(i)) or 0.0 for i in ids if i != a.chassis.id]
    m = max(ms or [0.0])
    return m * 1e-3 * ph.IMPACT_G * ph.G0, f"{ph.IMPACT_G:.0f} g on {m:.1f} g"


def _groups(a):
    gr = {}
    for f in a.fast:
        key = tuple(sorted(a.coupled(f)))
        if len(key) >= 2:
            gr.setdefault(key, []).append(f)
    return gr


def fasteners(a):
    out = []
    gr = _groups(a)
    ws = ph.weapons(a.ctx)
    # Shear on each bolt group (impact + weapon reaction torque for groups on the weapon motor).
    bad = 0
    for key, fs in gr.items():
        V, basis = _group_load(a, key)
        n = len(fs)
        T = 0.0
        mot = next((i for i in key if a.part(i) is not None and a.part(i).kind == "weapon_motor"), None)
        if mot and ws:
            p, wb, origin, axis = ws[0]
            from .power import rim_radius

            T = a.F * rim_radius(wb, origin, axis)
            r_b = np.mean([np.linalg.norm(np.cross(np.asarray(f.at) - origin, axis)) for f in fs])
            Vt = T / max(n * max(r_b, 1.0), 1e-9)
        else:
            Vt = 0.0
        per = V / n + Vt
        cap = min(_as(catalog.parse_designation(f.designation)[0]) * GRADE_SHEAR[_grade(f)] for f in fs)
        sf = cap / max(per, 1e-9)
        a.ctx.metrics[f"arch_bolt_shear_sf.{fs[0].id}"] = sf
        m = (f"{n}x {fs[0].designation} holding {list(key)}: {basis}/{n}" + (f" + torque {T / 1e3:.1f} N·m" if T else "")
             + f" = {per:.0f} N per bolt against {cap:.0f} N shear capacity (SF {sf:.1f}).")
        if sf < BOLT_SF:
            bad += 1
            out.append(fail("arch.bolt_shear", G, BLOCKER, "Bolts shear on a hit", m).on(*[f.id for f in fs])
                       .expect(f"SF >= {BOLT_SF}", f"{sf:.1f}").fix("More or bigger bolts, or a shear key/lip so the bolts only clamp."))
        # Hole bearing in the thinnest plastic plate.
        for f in fs:
            d, ln = catalog.parse_designation(f.designation)
            ax = _unit(f.dir)
            P = np.asarray(f.at, float) + np.outer(np.arange(0.05, ln, 0.1), ax)
            for pid in key:
                pb = a.body(pid)
                if pb is None or pb.kind in ("insert", "nut") or not a.printed(pb):
                    continue
                t = float(pb.inside(P).sum()) * 0.1
                mp = catalog.mech(a.mat(pb))
                if t <= 0 or mp is None:
                    continue
                sb = per / (d * t)
                if sb > mp[0] / 1.5:
                    bad += 1
                    out.append(fail("arch.bolt_bearing", G, WARNING, "Bolt tears through the plastic",
                                    f"`{f.id}` bears {per:.0f} N on {t:.1f} mm of `{pid}`: {sb:.0f} MPa against {mp[0]:.0f} MPa.")
                               .on(f.id, pid).here(f.at).expect(f"<= {mp[0] / 1.5:.0f} MPa", f"{sb:.0f} MPa").fix("Thicker flange or larger bolt."))
    if gr:
        _res(out, "arch.bolt_shear", None, "Bolt groups have shear margin", bad, f"{len(gr)} bolt groups have SF ≥ {BOLT_SF} in shear.", True)
        if not any(x.id == "arch.bolt_bearing" for x in out):
            out.append(ok("arch.bolt_bearing", G, "Bolt holes bear their load", "No printed hole is crushed by its bolt."))
    # Bending across gaps, washer area, edge distance, layer direction.
    bend_bad = wash_bad = edge_bad = layer_bad = 0
    judged_edge = 0
    for f in a.fast:
        d, ln = catalog.parse_designation(f.designation)
        ax = _unit(f.dir)
        at = np.asarray(f.at, float)
        ts = np.arange(0.05, ln, 0.1)
        P = at + np.outer(ts, ax)
        ins = measure.inside_any([b for b in a.solids if measure.aabb_overlap(b.aabb, a.body(f.id).aabb)], P)
        idx = np.nonzero(ins)[0]
        if len(idx):
            run_, best, inside_run = 0, 0, False
            for k in range(idx[0], idx[-1] + 1):
                if not ins[k]:
                    run_ += 1
                    best = max(best, run_)
                else:
                    run_ = 0
            gap = best * 0.1
            if gap > d:
                V, _ = _group_load(a, a.coupled(f))
                n = len(gr.get(tuple(sorted(a.coupled(f))), [f]))
                Mb = V / n * gap / 2
                sig = Mb / (math.pi * (0.85 * d) ** 3 / 32)
                y = GRADE_YIELD[_grade(f)]
                bend_bad += 1
                out.append(fail("arch.bolt_bending", G, BLOCKER if sig > y / 1.5 else WARNING, "Bolt bridges a gap",
                                f"`{f.id}` spans {gap:.1f} mm of air (> d = {d:.1f}): {V / n:.0f} N bends it to {sig:.0f} MPa (yield {y:.0f}).")
                           .on(f.id).here(at + ax * float(ts[idx[0]])).fix("Close the gap with a boss or spacer so the bolt is in shear, not bending."))
        # Washer area under head (plastic).
        head_pt = at + ax * 0.3
        under = [b for b in a.solids if measure.aabb_overlap(b.aabb, a.body(f.id).aabb) and b.inside(head_pt[None])[0]]
        washer = bool(_extra(f, "washer")) or str(f.head or "").lower() in ("washer", "flange", "button_flange")
        if under and a.printed(under[0]) and catalog.mech(a.mat(under[0])):
            dk, _, _ = catalog.screw_dims(d)
            dk = dk + 3.0 if washer else dk
            A = math.pi / 4 * (dk ** 2 - (d + 0.4) ** 2)
            pre = PRELOAD_PER_D2 * d * d
            pr = pre / A
            lim = catalog.mech(a.mat(under[0]))[0] / 1.5
            if pr > lim:
                wash_bad += 1
                out.append(fail("arch.bolt_washer", G, WARNING, "Screw head sinks into the plastic",
                                f"`{f.id}` head bears {A:.1f} mm² on `{under[0].id}` ({a.mat(under[0])}): {pre:.0f} N preload → {pr:.0f} MPa > {lim:.0f}.")
                           .on(f.id, under[0].id).here(at).fix("Add a washer or a flanged/button head."))
        # Edge distance in each part it passes.
        for pid in a.coupled(f):
            pb = a.body(pid)
            if pb is None or pb.kind in ("insert", "nut", "motor", "weapon_motor"):
                continue
            inside = ts[pb.inside(P)]
            if not len(inside):
                continue
            c = at + ax * float(np.median(inside))
            rad = d / 2
            if pid == a.threaded_host(f) and f.threads_into != pid:
                ib = a.body(f.threads_into)
                rad = float(ph.perp_radius(ib.mesh.vertices, at, ax).max()) if ib is not None else rad
            u, v = _perp(ax)
            ed = min(_ray_exit(pb, c, math.cos(k) * u + math.sin(k) * v, rad + 0.05, 3 * d + rad) for k in np.linspace(0, 2 * math.pi, 12, endpoint=False))
            edge = ed  # centre to edge
            judged_edge += 1
            if f.threads_into in a.insert_host and pid == a.threaded_host(f):
                wall = ed - rad
                m = f"Insert `{f.threads_into}` in `{pid}` has {wall:.1f} mm of wall around it."
                if wall < MIN_INSERT_WALL:
                    edge_bad += 1
                    out.append(fail("arch.insert_wall", G, BLOCKER if wall < 0.8 else WARNING, "Insert boss wall too thin", m)
                               .on(f.threads_into, pid).here(c).expect(f">= {MIN_INSERT_WALL} mm", f"{wall:.1f} mm").fix("Grow the boss around the insert."))
                continue
            if edge < 1.5 * d:
                edge_bad += 1
                out.append(fail("arch.edge_distance", G, BLOCKER if edge < 1.0 * d else WARNING, "Hole too close to the edge",
                                f"`{f.id}` in `{pid}`: centre {edge:.1f} mm from the edge (need ≥ 1.5d = {1.5 * d:.1f}).")
                           .on(f.id, pid).here(c).expect(f">= {1.5 * d:.1f} mm", f"{edge:.1f} mm").fix("Move the hole in or add material around it."))
        # Pure tension across layer lines in a printed host.
        h = a.threaded_host(f)
        hb = a.body(h) if h else None
        if hb is not None and a.printed(hb):
            pd = _print_dir(a.part(h))
            if abs(ax @ pd) > 0.8:
                V, basis = _group_load(a, a.coupled(f))
                on_path = basis.startswith("design impact") and not any(
                    a.part(i) is not None and a.part(i).kind == "armor" for i in a.coupled(f))
                if on_path:
                    layer_bad += 1
                    out.append(fail("arch.layer_tension", G, WARNING, "Screw pulls along the layer lines",
                                    f"`{f.id}` pulls on `{h}` along its print direction; a hit ({basis}) peels layers apart around the insert.")
                               .on(f.id, h).here(at).fix("Turn the joint so the screw axis lies in the layer plane, or clamp through with a nut."))
    out.append(ok("arch.bolt_bending", G, "No bolt bridges a gap", "No shank spans more than its diameter of air.")) if not bend_bad else None
    out.append(ok("arch.bolt_washer", G, "Screw heads have bearing area", "Every head on plastic has enough area.")) if not wash_bad else None
    if judged_edge and not any(x.id == "arch.edge_distance" for x in out):
        out.append(ok("arch.edge_distance", G, "Holes clear of edges", f"{judged_edge} holes ≥ 1.5d from the edge."))
    if a.insert_host and not any(x.id == "arch.insert_wall" for x in out):
        out.append(ok("arch.insert_wall", G, "Insert bosses thick enough", f"Insert walls ≥ {MIN_INSERT_WALL} mm."))
    out.append(ok("arch.layer_tension", G, "No load-path screw pulls layers apart", "Load-path screws lie in the layer plane.")) if not layer_bad else None
    out = [x for x in out if x is not None]
    # Hole spacing within one part.
    bad = 0
    for pid in {i for f in a.fast for i in a.coupled(f)}:
        fs = a.fasteners_of(pid)
        for f1, f2 in combinations(fs, 2):
            d = max(catalog.parse_designation(f1.designation)[0], catalog.parse_designation(f2.designation)[0])
            a1, a2 = np.asarray(f1.at, float), np.asarray(f2.at, float)
            ax = _unit(f1.dir)
            q = a2 - a1
            s = float(np.linalg.norm(q - ax * (q @ ax)))
            ln1, ln2 = catalog.parse_designation(f1.designation)[1], catalog.parse_designation(f2.designation)[1]
            t2 = float(q @ ax)
            overlap_ax = t2 < ln1 and t2 + ln2 > 0
            if ax @ _unit(f2.dir) > 0.95 and overlap_ax and s < 3 * d:
                bad += 1
                out.append(fail("arch.hole_spacing", G, WARNING, "Holes too close together",
                                f"`{f1.id}` and `{f2.id}` in `{pid}` are {s:.1f} mm apart (need ≥ 3d = {3 * d:.1f}).")
                           .on(f1.id, f2.id, pid).expect(f">= {3 * d:.1f} mm", f"{s:.1f} mm"))
    if not bad:
        out.append(ok("arch.hole_spacing", G, "Hole spacing ok", "Parallel holes are ≥ 3d apart."))
    # Inserts: in a printed host, coaxial with their screw.
    bad = 0
    for f in a.fast:
        ib = a.body(f.threads_into) if f.threads_into else None
        if ib is None or ib.kind != "insert":
            continue
        h = a.insert_host.get(ib.id)
        hb = a.body(h) if h else None
        if hb is None:
            bad += 1
            out.append(fail("arch.insert_host", G, WARNING, "Insert sits in nothing", f"`{ib.id}` is not surrounded by any part.").on(ib.id))
        elif not a.printed(hb):
            bad += 1
            out.append(fail("arch.insert_host", G, WARNING, "Heat-set insert in a non-printed part",
                            f"`{ib.id}` sits in `{h}` ({a.mat(hb)}); heat-set inserts melt into thermoplastic prints only.").on(ib.id, h))
        iax = _unit(ib.M[:3, 2])
        off = float(np.linalg.norm(np.cross(ib.center - np.asarray(f.at, float), _unit(f.dir))))
        if abs(abs(iax @ _unit(f.dir)) - 1) > 0.02 or off > 0.3:
            bad += 1
            out.append(fail("arch.insert_coaxial", G, BLOCKER, "Screw misses its insert",
                            f"`{f.id}` axis is {off:.2f} mm off and {math.degrees(math.acos(min(1, abs(iax @ _unit(f.dir))))):.0f}° from `{ib.id}`.")
                       .on(f.id, ib.id).here(ib.center).fix("Align the insert with the screw axis."))
    if not bad:
        out.append(ok("arch.insert_coaxial", G, "Inserts line up with screws", "Every insert is coaxial with its screw in a printed host."))
    if not any(x.id == "arch.insert_host" for x in out):
        out.append(ok("arch.insert_host", G, "Inserts sit in printed bosses", "Every heat-set insert is surrounded by a printed part."))
    return out


# --------------------------------------------------------------------------------------------------------------- cantilevers

def cantilevers(a):
    out = []
    judged = bad = 0
    for b in a.solids:
        p = a.part(b.id)
        if p is None or b.id == a.chassis.id or p.kind not in STRUCT:
            continue
        fs = [f for f in a.fasteners_of(b.id) if a.chassis.id in a.coupled(f) or any(
            a.part(i) is not None and a.part(i).kind in STRUCT and i != b.id for i in a.coupled(f))]
        if not fs or len(fs) > 2:
            continue
        lip = any(c.mechanical_key or c.method in ("interlock", "snap") for c in a.conns(b.id))
        judged += 1
        P = np.array([f.at for f in fs], float)
        c = P.mean(axis=0)
        spacing = max((float(np.linalg.norm(x - y)) for x, y in combinations(P, 2)), default=0.0)
        tip = float(np.linalg.norm(b.mesh.vertices - c, axis=1).max())
        ratio = tip / max(spacing, 1e-6)
        m = f"`{b.id}` hangs on {len(fs)} bolts {spacing:.1f} mm apart with its far end {tip:.1f} mm away (lever/spacing {ratio:.1f})."
        if ratio > CANTILEVER_RATIO and not lip:
            bad += 1
            out.append(fail("arch.cantilever_fastener", G, BLOCKER, "Part levered off two screws", m).on(b.id, *[f.id for f in fs])
                       .expect(f"<= {CANTILEVER_RATIO:.0f}", f"{ratio:.1f}")
                       .fix("Use ≥ 3 bolts spread over the part, or seat its root in a slot/lip so bending bears on plastic."))
    if judged and not bad:
        out.append(ok("arch.cantilever_fastener", G, "No part levered off its screws", f"{judged} lightly-bolted parts checked."))
    elif not judged:
        out.append(ok("arch.cantilever_fastener", G, "No part on ≤ 2 bolts", "Every bolted structure part has ≥ 3 bolts."))
    return out


# --------------------------------------------------------------------------------------------------------------- blades

def _is_blade(p):
    return p.kind == "wedge" or (p.kind in STRUCT and re.search(r"blade|wedgelet|fork_blade|scoop", p.id))


def blades(a):
    out = []
    structs = [b for b in a.solids if b.kind in STRUCT]
    for b in a.solids:
        p = a.part(b.id)
        if p is None or not _is_blade(p):
            continue
        fs = a.fasteners_of(b.id)
        fused = bool(p.fused_with) or any(c.method in ("glue", "interlock") for c in a.conns(b.id))
        if len(fs) < 2 and not fused:
            out.append(fail("arch.blade_bolts", G, BLOCKER, "Blade held by fewer than two bolts",
                            f"`{b.id}` has {len(fs)} bolts; one bolt is a pivot.").on(b.id).fix("Use ≥ 2 bolts (3 for a long blade)."))
        else:
            out.append(ok("arch.blade_bolts", G, "Blade bolted at ≥ 2 points", f"`{b.id}`: {len(fs)} bolts."))
        support = [s for s in structs if s is not b and a.contact(b, s)]
        area = sum(a.area(b, s) for s in support)
        if area < 10:
            out.append(fail("arch.blade_root_support", G, WARNING, "Blade root stands off its support",
                            f"`{b.id}` touches structure over {area:.0f} mm²; the bolts take all the bending.").on(b.id)
                       .fix("Seat the blade root flat on the chassis or in a slot."))
        else:
            out.append(ok("arch.blade_root_support", G, "Blade root seated", f"`{b.id}` bears on {area:.0f} mm² of structure."))
        # Root bending under a 300 N tip load.
        mp = catalog.mech(a.mat(b))
        if mp is None or not fs:
            a.ctx.not_checked.append(f"Blade root stress of `{b.id}`: no material strength or no bolts")
            continue
        sy = mp[0] * (catalog.PRINTED_Z_FACTOR if a.printed(b) else 1.0)
        V = b.mesh.vertices
        tip = V[int(np.argmax(V[:, 1] - 0.5 * V[:, 2]))]  # front-most, lowest point
        # Root: the supported point (contact with structure, else a bolt) nearest the tip.
        bp, _ = b.surface(1.0)
        cand = [np.asarray(f.at, float) for f in fs]
        for s_ in support:
            sel = np.all((bp >= s_.aabb[0] - 0.5) & (bp <= s_.aabb[1] + 0.5), axis=1)
            if sel.any():
                Q = bp[sel][:3000]
                cand += list(Q[s_.distance(Q) <= CONTACT_GAP])
        C = np.array(cand)
        k = int(np.argmin(np.linalg.norm(C - tip, axis=1)))
        root = C[k]
        lever = tip - root
        L = float(np.linalg.norm(lever))
        if L < 1.0:
            out.append(ok("arch.blade_root_stress", G, "Blade supported to its tip", f"`{b.id}` is backed by structure up to the tip."))
            continue
        ld = _unit(lever)
        worst = None
        from shapely.geometry import LineString
        from shapely.ops import polygonize, unary_union

        from .strength import section_modulus

        u, v = _perp(ld)
        for kf in (0.1, 0.2, 0.3, 0.45, 0.6):
            cut = root + lever * kf
            poly = _plane_section(b.mesh, cut, ld, u)
            if poly is None:
                continue
            if poly.is_empty or poly.area < 2.0 or L * (1 - kf) < 3.0:
                continue  # the last 3 mm of a pointed tip is a contact patch, not a beam
            Zk = None
            for ang in range(0, 180, 15):
                I, cf, A_ = section_modulus(affinity.rotate(poly, ang, origin=(0, 0)))
                if cf > 0 and (Zk is None or I / cf < Zk):
                    Zk = I / cf
            if not Zk:
                continue
            sk = BLADE_TIP_N * L * (1 - kf) / Zk
            if worst is None or sk > worst[0]:
                mrr = poly.minimum_rotated_rectangle
                xs, ys = mrr.exterior.coords.xy
                e = sorted(math.dist((xs[q], ys[q]), (xs[q + 1], ys[q + 1])) for q in range(2))
                worst = (sk, Zk, (e[-1], e[0]))
        if worst is None:
            if L < 6.0:
                out.append(ok("arch.blade_root_stress", G, "Blade supported to its tip", f"`{b.id}` is backed by structure to within {L:.1f} mm of the tip."))
            else:
                a.ctx.not_checked.append(f"Blade root stress of `{b.id}`: no cross-section at the root")
            continue
        sig, Zmin, dims = worst
        w2, t_ = dims
        m = f"`{b.id}`: {BLADE_TIP_N:.0f} N at the tip, {L:.1f} mm from the bolts, from its last support, root ~{w2:.1f} x {t_:.1f} mm (Z {Zmin:.0f} mm³) → {sig:.0f} MPa (yield {sy:.0f})."
        small_blade = bool(re.search(r"blade|wedgelet|scoop", b.id))
        if sig > sy:
            out.append(fail("arch.blade_root_stress", G, BLOCKER if small_blade else WARNING, "Blade bends at the root", m).on(b.id).expect(f"<= {sy / 1.5:.0f} MPa", f"{sig:.0f} MPa")
                       .fix("Thicker blade, shorter overhang or support the root closer to the tip."))
        elif sig > sy / 1.5:
            out.append(fail("arch.blade_root_stress", G, WARNING, "Blade root is marginal", m).on(b.id))
        else:
            out.append(ok("arch.blade_root_stress", G, "Blade root strong enough", m))
    return out


# --------------------------------------------------------------------------------------------------------------- armour

def armour(a):
    out = []
    for b in a.solids:
        p = a.part(b.id)
        if p is None or b.id == a.chassis.id:
            continue
        ext = b.aabb[1] - b.aabb[0]
        if not (p.kind in ("armor", "plate") or "top" in b.id or "lid" in b.id) or ext[2] > 0.35 * min(ext[0], ext[1]):
            continue
        pts, nrm = b.surface(1.5)
        under = pts[nrm[:, 2] < -0.7]
        if len(under) < 4:
            continue
        others = [s for s in a.solids if s is not b and s.kind in STRUCT + ("battery", "motor", "esc") and measure.aabb_overlap(s.aabb, b.aabb, 1.0)]
        sup = np.zeros(len(under), bool)
        for s in others:
            sup |= s.inside(under - [0, 0, 0.6])
        fs = a.fasteners_of(b.id)
        bolt_pts = np.array([f.at for f in fs], float)[:, :2] if fs else np.zeros((0, 2))
        S = np.vstack([under[sup][:, :2], bolt_pts])
        if len(S) == 0:
            out.append(fail("arch.armor_span", G, BLOCKER, "Top armour not supported", f"`{b.id}` rests on nothing and has no bolts.").on(b.id))
            continue
        from scipy.spatial import cKDTree

        dist, _ = cKDTree(S).query(under[:, :2])
        L = 2 * float(dist.max())
        mp = catalog.mech(a.mat(b))
        t = min(float(ext[2]), 2 * b.geom.volume / max(float(b.mesh.area), 1e-6))
        if mp is None:
            a.ctx.not_checked.append(f"Armour span of `{b.id}`: unknown modulus")
            continue
        E = mp[2] * 1e3
        defl = BLADE_TIP_N * L * L / (4 * E * t ** 3)
        a.ctx.metrics[f"arch_armor_span_mm.{b.id}"] = L
        m = f"`{b.id}` ({a.mat(b)}, ~{t:.1f} mm) has an unsupported span of {L:.0f} mm: {BLADE_TIP_N:.0f} N in the middle deflects {defl:.1f} mm."
        if defl > 2.0:
            out.append(fail("arch.armor_span", G, WARNING, "Top armour span too long", m).on(b.id).expect("<= 2 mm", f"{defl:.1f} mm")
                       .fix("Add a rib/post under the middle, more bolts, or thicker sheet."))
        else:
            out.append(ok("arch.armor_span", G, "Top armour well supported", m))
    return out


# --------------------------------------------------------------------------------------------------------------- pods

def pods(a):
    out = []
    for b in a.solids:
        p = a.part(b.id)
        if p is None or b.id == a.chassis.id or p.kind not in ("structure", "plate") or not re.search(r"pod|side|rail|module", b.id):
            continue
        fs = [f for f in a.fasteners_of(b.id) if len(a.coupled(f)) >= 2]
        lip = any(c.mechanical_key or c.method in ("interlock", "snap") for c in a.conns(b.id)) or bool(p.fused_with)
        ext = b.aabb[1] - b.aabb[0]
        Lp = float(max(ext[:2]))
        P = np.array([f.at for f in fs], float) if fs else np.zeros((0, 3))
        spread = max((float(np.linalg.norm(x[:2] - y[:2])) for x, y in combinations(P, 2)), default=0.0)
        m = f"`{b.id}` ({Lp:.0f} mm long): {len(fs)} bolts spread {spread:.0f} mm; locating lip declared: {lip}."
        if (len(fs) >= 3 and spread >= 0.4 * Lp) or (lip and len(fs) >= 2):
            out.append(ok("arch.pod_mount", G, "Pod is located and spread-bolted", m))
        else:
            out.append(fail("arch.pod_mount", G, BLOCKER, "Pod pivots on its mount", m).on(b.id)
                       .expect(f">= 3 bolts over >= {0.4 * Lp:.0f} mm, or a lip", f"{len(fs)} bolts over {spread:.0f} mm")
                       .fix("Bolt front, middle and rear into the tub, and add a tongue/lip so the screws only clamp."))
    return out


# --------------------------------------------------------------------------------------------------------------- electronics

def electronics(a):
    out = []
    sup = _supports(a)
    hosts = {(x[2] or x[1]).id for x in sup.values()} - {a.chassis.id} if sup else set()
    rot = {x for s in a.rotor.values() for x in s}
    structs = [b for b in a.solids if b.kind in STRUCT]
    for b in a.solids:
        if b.kind not in ELEC:
            continue
        touch_rot = [r for r in rot if a.body(r) is not None and a.contact(b, a.body(r))]
        touch_up = [h for h in hosts if a.contact(b, a.body(h))]
        if touch_rot:
            out.append(fail("arch.electronics_isolated", G, BLOCKER, "Electronics touch the spinning weapon",
                            f"`{b.id}` touches {touch_rot}.").on(b.id, *touch_rot))
        elif touch_up:
            out.append(fail("arch.electronics_isolated", G, WARNING, "Electronics on the weapon load path",
                            f"`{b.id}` bears on the weapon upright {touch_up}; every hit goes through it.").on(b.id, *touch_up)
                       .fix("Leave a gap or foam between electronics and the uprights."))
        else:
            out.append(ok("arch.electronics_isolated", G, "Electronics off the load path", f"`{b.id}` touches no weapon support."))
        if b.kind == "battery":
            axes, blocked = _clamp_axes(a, b, structs)
            cons = a.conns(b.id)
            strap = any(c.method in ("screw", "interlock", "snap") for c in cons) or bool(a.fasteners_of(b.id))
            m = f"`{b.id}`: walls on both sides along {['XYZ'[i] for i in axes] or 'no axis'}, {len(blocked)}/6 sides; strap/clamp: {strap}."
            if len(axes) >= 2 and (strap or len(blocked) >= 5):
                out.append(ok("arch.battery_restraint", G, "Battery is boxed in", m))
            else:
                out.append(fail("arch.battery_restraint", G, WARNING, "Battery can move", m).on(b.id)
                           .fix("Box it on 2 axes and hold it down with a strap, foam and a lid."))
    return out


# --------------------------------------------------------------------------------------------------------------- wheels

def wheels(a):
    out = []
    for b in a.solids:
        p = a.part(b.id)
        if p is None or p.kind not in ("wheel", "wheel_hub"):
            continue
        cons = a.conns(b.id)
        pins = [c for c in cons if c.method in ("shaft", "pin")]
        for c in pins:
            o = c.a if c.b == b.id else c.b
            ob = a.body(o)
            bearing = any(a.part(x).kind == "bearing" for x in a.parts if a.body(x) is not None and a.part(x).kind == "bearing"
                          and a.contact(a.body(x), b))
            if a.printed(b) and not bearing:
                out.append(fail("arch.wheel_bore", G, WARNING, "Wheel turns on a printed bore",
                                f"`{b.id}` ({a.mat(b)}) spins on `{o}` with no bearing or bushing; the bore wears oval.").on(b.id, o)
                           .fix("Press a bronze bushing or a small bearing into the hub, or accept wear and say so."))
            else:
                out.append(ok("arch.wheel_bore", G, "Wheel runs on a bearing", f"`{b.id}` on `{o}`."))
            # Axle pin engagement in the structure.
            if ob is not None and a.part(o).kind in ("pin", "shaft"):
                Vp = ob.mesh.vertices - ob.center
                ax = _unit(np.linalg.eigh(np.cov(Vp.T))[1][:, -1])  # long axis of the pin
                d = 2 * float(np.percentile(ph.perp_radius(ob.mesh.vertices, ob.center, ax), 95))
                tv = (ob.mesh.vertices - ob.center) @ ax
                P = ob.center + np.outer(np.arange(tv.min() + 0.05, tv.max(), 0.1), ax)
                eng = max((float(s.inside(P).sum()) * 0.1 for s in a.solids if s.kind in STRUCT), default=0.0)
                m = f"`{o}` (Ø{d:.1f}) is held over {eng:.1f} mm of structure (need ≥ 2d = {2 * d:.1f})."
                if eng < 2 * d:
                    out.append(fail("arch.axle_engagement", G, WARNING, "Axle pin barely held", m).on(o).fix("Lengthen the boss or support the pin both sides."))
                else:
                    out.append(ok("arch.axle_engagement", G, "Axle pin well held", m))
    return out


# --------------------------------------------------------------------------------------------------------------- symmetry

_PAIR = [(r"(^|_)l(\d*)$", r"\1r\2"), (r"(^|_)left", r"\1right"), (r"_fl$", "_fr"), (r"_rl$", "_rr"), (r"(^|_)l(\d*)_", r"\1r\2_"), (r"_([a-z]*)l(\d*)$", r"_\1r\2")]


def _mirror_id(i):
    for pat, rep in _PAIR:
        if re.search(pat, i):
            return re.sub(pat, rep, i)
    return None


def symmetry(a):
    out = []
    asym = set(a.spec.raw.get("asymmetric") or [])
    bad = judged = 0
    for b in a.solids:
        o = _mirror_id(b.id)
        ob = a.body(o) if o else None
        if ob is None or b.id in asym or o in asym or _extra(a.part(b.id), "asymmetric") or _extra(a.part(o), "asymmetric"):
            continue
        judged += 1
        mb = b.aabb.copy()
        mir = np.array([[-mb[1][0], mb[0][1], mb[0][2]], [-mb[0][0], mb[1][1], mb[1][2]]])
        dev = float(np.abs(mir - ob.aabb).max())
        dv = abs(b.geom.volume - ob.geom.volume) / max(b.geom.volume, ob.geom.volume, 1e-9)
        if dev > SYM_TOL_MM or dv > 0.03:
            bad += 1
            out.append(fail("arch.symmetry", G, WARNING, "Left/right parts differ",
                            f"`{b.id}` mirrored differs from `{o}` by {dev:.2f} mm in extent and {dv * 100:.1f} % in volume.").on(b.id, o)
                       .expect(f"<= {SYM_TOL_MM} mm", f"{dev:.2f} mm").fix("Mirror one from the other, or list both in `asymmetric`."))
    if judged and not bad:
        out.append(ok("arch.symmetry", G, "Mirrored parts match", f"{judged} left/right pairs within {SYM_TOL_MM} mm."))
    bad = judged = 0
    byid = {f.id: f for f in a.fast}
    for f in a.fast:
        o = _mirror_id(f.id)
        g = byid.get(o) if o else None
        if g is None or f.id in asym:
            continue
        judged += 1
        dev = float(np.abs(np.array([-f.at[0], f.at[1], f.at[2]]) - np.asarray(g.at, float)).max())
        if dev > SYM_TOL_MM or f.designation != g.designation:
            bad += 1
            out.append(fail("arch.symmetry_fasteners", G, WARNING, "Left/right screws differ",
                            f"`{f.id}` mirrored is {dev:.2f} mm from `{o}` ({f.designation} vs {g.designation}).").on(f.id, o))
    if not bad:
        out.append(ok("arch.symmetry_fasteners", G, "Mirrored screws match", f"{judged} screw pairs mirror within {SYM_TOL_MM} mm."))
    return out


# --------------------------------------------------------------------------------------------------------------- balance

def balance(a):
    out = []
    tot, com = 0.0, np.zeros(3)
    for b in a.bodies:
        m = a.mass(b)
        if m is None:
            a.ctx.not_checked.append(f"Centre of mass: `{b.id}` has no mass")
            continue
        tot += m
        com += m * (b.M[:3, :3] @ b.geom.centroid + b.M[:3, 3])
    if tot <= 0:
        return out
    com /= tot
    fz = ph.floor_z(a.ctx)
    pts = []
    for b in a.solids:
        if b.aabb[0][2] > fz + 0.6:
            continue
        v = b.mesh.vertices
        pts.append(v[v[:, 2] <= fz + 0.6][:, :2])
    if not pts:
        a.ctx.not_checked.append("Centre of mass vs support polygon: nothing touches the floor")
        return out
    P = np.vstack(pts)
    hull = MultiPoint([tuple(x) for x in P]).convex_hull
    c = Point(com[0], com[1])
    inside = hull.buffer(1e-6).contains(c)
    margin = hull.exterior.distance(c) if hull.geom_type == "Polygon" else 0.0
    a.ctx.metrics["arch_com_margin_mm"] = margin if inside else -margin
    m = f"Centre of mass ({com[0]:.1f}, {com[1]:.1f}) is {'inside' if inside else 'outside'} the floor contact polygon by {margin:.1f} mm."
    if not inside or hull.geom_type != "Polygon":
        out.append(fail("arch.com_support", G, BLOCKER, "Robot tips over at rest", m).here(com)
                   .fix("Move the battery/motors so the centre of mass is between the wheels and the skids."))
    else:
        out.append(ok("arch.com_support", G, "Centre of mass over the footprint", m))
        h = float(com[2] - fz)
        ratio = h / max(2 * margin, 1e-6)
        if ratio > 1.0:
            out.append(fail("arch.com_height", G, WARNING, "Centre of mass high for the footprint",
                            f"Centre of mass {h:.1f} mm up, {margin:.1f} mm from the nearest tipping edge (h / 2·margin = {ratio:.2f}).").here(com))
        else:
            out.append(ok("arch.com_height", G, "Centre of mass low", f"{h:.1f} mm up, {margin:.1f} mm from the nearest tipping edge."))
    return out


# --------------------------------------------------------------------------------------------------------------- blade direction

def blade_orientation(a):
    out = []
    for b in a.solids:
        p = a.part(b.id)
        if p is None or not _is_blade(p):
            continue
        fs = a.fasteners_of(b.id)
        base = np.mean([f.at for f in fs], axis=0) if fs else b.mesh.vertices.mean(axis=0)
        V = b.mesh.vertices
        reach = np.linalg.norm((V - base)[:, :2], axis=1)
        cand = V[reach >= 0.5 * reach.max()]
        ymax = float(cand[:, 1].max())
        far = cand[cand[:, 1] >= ymax - 0.5].mean(axis=0)  # the front-most of the far points is the tip
        vec = far - base
        h = np.array([vec[0], vec[1]])
        ang = math.degrees(math.atan2(abs(h[0]), h[1])) if np.linalg.norm(h) > 1e-6 else 180.0
        front = V[:, 1].max()
        tip_front = far[1] >= front - 1.0
        m = (f"`{b.id}` tip vector from its mount points {ang:.0f}° off straight ahead"
             f"{'' if tip_front else f' and its far end ({far[1]:.1f}) is not its front-most point ({front:.1f})'}.")
        if ang > 20 or not tip_front:
            out.append(fail("arch.blade_orientation", G, BLOCKER, "Blade does not point forward", m).on(b.id).here(far)
                       .expect("<= 20° from +Y, tip front-most", f"{ang:.0f}°").fix("Rotate/mirror the blade so its tip points forward (+Y)."))
        else:
            out.append(ok("arch.blade_orientation", G, "Blade points forward", m))
    return out


# --------------------------------------------------------------------------------------------------------------- teeth

HARD_TEETH = {"hardox", "ar400", "ar500", "s7", "tool_steel", "spring_steel", "d2", "o1", "4140", "titanium", "ti6al4v"}


def teeth(a):
    out = []
    for p, wb, origin, axis in ph.weapons(a.ctx):
        dt = (wb.mesh.vertices - origin) @ axis
        c = origin + axis * (float(dt.min()) + float(dt.max())) / 2
        u, _ = _perp(axis)
        poly = _plane_section(wb.mesh, c, axis, u)
        if poly is None or poly.is_empty:
            a.ctx.not_checked.append(f"Teeth of `{p.id}`: no section through the disc")
            continue
        g = max(getattr(poly, "geoms", [poly]), key=lambda x: x.area)
        P = np.asarray(g.exterior.coords)[:-1]
        if len(P) < 8:
            continue
        # Resample the outline at 0.2 mm.
        seg = np.vstack([P, P[:1]])
        L = np.r_[0, np.cumsum(np.linalg.norm(np.diff(seg, axis=0), axis=1))]
        ss = np.arange(0, L[-1], 0.2)
        Q = np.c_[np.interp(ss, L, seg[:, 0]), np.interp(ss, L, seg[:, 1])]
        r = np.linalg.norm(Q, axis=1)
        k = int(np.argmax(r))
        tip = Q[k]
        n = len(Q)
        # Tip radius: circle through points 0.6 mm either side along the outline.
        A_, B_, C_ = Q[(k - 3) % n], tip, Q[(k + 3) % n]
        ab, bc, ca = np.linalg.norm(A_ - B_), np.linalg.norm(B_ - C_), np.linalg.norm(C_ - A_)
        cross = abs((B_ - A_)[0] * (C_ - A_)[1] - (B_ - A_)[1] * (C_ - A_)[0])
        R_tip = ab * bc * ca / max(2 * cross, 1e-9)
        # Leading face: the side where the radius falls fastest; rake = angle between that face and the radius.
        best = None
        for sgn in (1, -1):
            j = next((i for i in range(1, n // 2) if r[(k + sgn * i) % n] < r[k] - 3.0), None)
            if j is None:
                continue
            face = Q[(k + sgn * j) % n] - tip
            if best is None or j < best[0]:
                best = (j, face)
        if best is None:
            out.append(fail("arch.weapon_teeth", G, WARNING, "Weapon has no tooth",
                            f"`{p.id}` outline never drops 3 mm below its tip radius: it is round and will not bite.").on(p.id)
                       .fix("Cut 1-2 hooked teeth into the profile."))
            continue
        face = best[1]
        rake = math.degrees(math.acos(min(1.0, abs(float(face @ (-tip)) / (np.linalg.norm(face) * np.linalg.norm(tip) + 1e-9)))))
        mat = (a.mat(wb) or "").lower()
        hard = mat in HARD_TEETH or bool(_extra(p, "hardened"))
        m = (f"`{p.id}` tooth at r = {r[k]:.1f} mm: tip radius ~{R_tip:.2f} mm, leading face {rake:.0f}° from radial, "
             f"material {mat or 'unknown'}{' (hardened)' if hard else ''}.")
        probs = []
        if R_tip > 1.0:
            probs.append(f"tip radius {R_tip:.2f} > 1 mm")
        if rake > 30:
            probs.append(f"face {rake:.0f}° off radial (> 30°): it ramps instead of biting")
        if not hard:
            probs.append("tooth material is not a hardened steel/titanium")
        if probs:
            out.append(fail("arch.weapon_teeth", G, WARNING, "Weapon tooth is blunt or soft", m + " " + "; ".join(probs) + ".")
                       .on(p.id).fix("Sharp (≤ 1 mm) tip, 0-30° leading face, hardened material (Hardox/AR500/S7, or declare `hardened: true`)."))
        else:
            out.append(ok("arch.weapon_teeth", G, "Weapon tooth bites", m))
    return out


# --------------------------------------------------------------------------------------------------------------- foreign objects

def foreign_through_rotor(a):
    out = []
    if not a.rotor:
        return out
    exempt = ("shaft", "bearing", "weapon_motor")
    for wid, s in a.rotor.items():
        rb = [a.body(x) for x in s if a.body(x) is not None]
        bad = 0
        for b in a.solids:
            p = a.part(b.id)
            if p is None or b.id in s or p.kind in exempt or p.kind in ("insert", "nut"):
                continue
            hit = [r_.id for r_ in rb if measure.aabb_overlap(r_.aabb, b.aabb) and measure.overlap_exceeds(r_, b, 0.05)]
            if not hit:
                continue
            if p.kind == "locking_bar":
                ax = _unit(b.M[:3, 2])
                ext = float(np.ptp((b.mesh.vertices - b.center) @ ax)) + 5
                others = [o for o in a.solids if o is not b and measure.aabb_overlap(o.aabb, b.aabb, ext)]
                free = False
                for sg in (1, -1):
                    path = [b.moved(ax * sg * t) for t in np.linspace(1, ext, 6)]
                    if not any(measure.overlap_exceeds(o, mb_, 0.05) for mb_ in path[-2:] for o in others if o.id not in hit) and \
                            not any(measure.overlap_exceeds(r_, path[-1], 0.05) for r_ in rb):
                        free = True
                        break
                removable = bool(p.tool_free or _extra(p, "removable", True))
                if free and removable:
                    out.append(ok("arch.foreign_through_rotor", G, "Locking bar can be pulled out",
                                  f"`{b.id}` passes through {hit} and slides out along its axis."))
                    continue
                bad += 1
                out.append(fail("arch.foreign_through_rotor", G, BLOCKER, "Locking bar cannot be removed",
                                f"`{b.id}` passes through {hit} but cannot slide out along its own axis without hitting other parts.")
                           .on(b.id, *hit).fix("Give the locking bar a clear straight exit path through the structure."))
                continue
            bad += 1
            out.append(fail("arch.foreign_through_rotor", G, BLOCKER, "Object passes through the spinning weapon",
                            f"`{b.id}` ({p.kind}) intersects rotating {hit}; it is hit at spin-up.").on(b.id, *hit)
                       .fix("Move it out of the rotor's swept volume, or make it the declared `locking_bar` (kind locking_bar)."))
        if not bad and not any(x.id == "arch.foreign_through_rotor" for x in out):
            out.append(ok("arch.foreign_through_rotor", G, "Nothing passes through the rotor", f"Rotor `{wid}` is clear of static parts."))
    return out


# --------------------------------------------------------------------------------------------------------------- holders

def holders(a):
    out = []
    bad = judged = 0
    for p in a.spec.parts:
        refs = []
        if p.parent:
            refs.append(("parent", p.parent))
        if isinstance(p.retained, str) and p.retained in a.parts:
            refs.append(("retained", p.retained))
        for how, h in refs:
            hp = a.part(h)
            if hp is None:
                continue
            judged += 1
            g1, g2 = a.group_of(p.id), a.group_of(h)
            elec_on_weapon = p.kind in ELEC and (g2 not in (None, "fixed") or hp.kind == "weapon")
            # a jointed part held by its parent moves relative to it by design (that is what the joint is)
            cross = g1 is not None and g2 is not None and g1 != g2 and not (how == "parent" and p.joint is not None)
            weak_holder = hp.kind in ELEC and p.kind in STRUCT
            if cross or elec_on_weapon or weak_holder:
                bad += 1
                why = ("electronics carried by the weapon" if elec_on_weapon else
                       f"motion groups differ ({g1} vs {g2})" if cross else f"a {hp.kind} holds structure")
                out.append(fail("arch.holder_group", G, BLOCKER, "Part held by the wrong thing",
                                f"`{p.id}` ({p.kind}) is held ({how}) by `{h}` ({hp.kind}): {why}.").on(p.id, h)
                           .fix("Hold static parts with chassis structure and rotating parts with the rotor."))
    if not bad:
        out.append(ok("arch.holder_group", G, "Parts held by matching structure", f"{judged} parent/retainer links checked."))
    return out


# --------------------------------------------------------------------------------------------------------------- cut breakout

def _cyl_cuts(shape, M=np.eye(4)):
    """[(4x4 placement in part frame, radius, height)] of cylinder cuts in top-level subtracts (through fillets)."""
    from .. import xform

    out = []
    if not isinstance(shape, dict):
        return out
    t = shape.get("type")
    if t in ("fillet", "chamfer") and isinstance(shape.get("shape"), dict):
        return _cyl_cuts(shape["shape"], M)
    if t == "subtract":
        cuts = shape.get("cut") or shape.get("cuts") or []
        cuts = cuts if isinstance(cuts, list) else [cuts]
        for c in cuts:
            out += _cyl_leaf(c, M)
        out += _cyl_cuts(shape.get("base"), M)
    return out


def _cyl_leaf(c, M):
    from .. import xform

    if not isinstance(c, dict):
        return []
    if c.get("type") == "place":
        return _cyl_leaf(c.get("shape"), M @ xform.pose(c.get("at") or [0, 0, 0], c.get("rot") or [0, 0, 0]))
    if c.get("type") == "cylinder" and c.get("radius") is not None:
        return [(M, float(c["radius"]), float(c.get("height") or 0))]
    if c.get("type") == "union":
        return [x for it in c.get("items") or [] for x in _cyl_leaf(it, M)]
    return []


def _base_of(shape):
    while isinstance(shape, dict) and shape.get("type") in ("fillet", "chamfer"):
        shape = shape.get("shape")
    while isinstance(shape, dict) and shape.get("type") == "subtract":
        shape = shape.get("base")
    return shape


def cut_breakout(a):
    from .. import geom as geom_mod

    out = []
    judged = bad = 0
    for rp in a.r.parts:
        p = rp.part
        b = a.body(p.id)
        if b is None or rp.cat is not None or not isinstance(rp.shape, dict) or p.kind not in STRUCT + ("hub", "wheel_hub", "pulley"):
            continue
        cuts = [c for c in _cyl_cuts(rp.shape) if c[1] <= 4.0]
        if not cuts:
            continue
        base = _base_of(rp.shape)
        try:
            bg = geom_mod.geom_for(base, a.spec.base_dir, geom_mod.FAST)
        except Exception as e:  # noqa: BLE001
            a.ctx.not_checked.append(f"Cut breakout of `{p.id}`: base solid failed ({type(e).__name__})")
            continue
        bb = b.placed(b.M)
        bb.geom = bg
        bb._mesh = None
        mat = catalog.material(p.material)
        wall = mat.min_wall_mm if mat else 0.9
        # An elastomer (TPU) web stretches instead of cracking out: 1 mm holds a screw or a standoff bore (RVRN wedglet).
        lim = 1.0 if (mat is not None and mat.cls == "elastomer") else max(1.0, 1.5 * wall)
        for Mc, r, hgt in cuts:
            W = b.M @ Mc
            c, ax = W[:3, 3], _unit(W[:3, 2])
            ts = np.linspace(-hgt / 2, hgt / 2, 13)
            axis_in = bb.inside(c + np.outer(ts, ax))
            # Only stations deep in the material: entry/exit chamfers and fillets are not webs.
            deep = [k for k in range(1, len(ts) - 1) if axis_in[k - 1] and axis_in[k] and axis_in[k + 1]]
            if not deep:
                continue
            judged += 1
            u, v = _perp(ax)
            web = 1e9
            for k in deep[len(deep) // 4::max(len(deep) // 3, 1)][:3]:
                cc = c + ax * ts[k]
                poly = _plane_section(bb.mesh, cc, ax, u)
                if poly is None or poly.is_empty:
                    continue
                piece = next((g_ for g_ in getattr(poly, "geoms", [poly]) if g_.buffer(1e-6).contains(Point(0, 0))), None)
                if piece is None:
                    continue
                hole = Point(0, 0).buffer(r, 32)
                if not piece.buffer(1e-6).contains(hole):
                    web = 0.0
                    break
                web = min(web, float(piece.boundary.distance(Point(0, 0))) - r)
            if web >= 1e8:
                continue
            if web < lim:
                bad += 1
                out.append(fail("arch.cut_breakout", G, BLOCKER, "Hole breaks out or leaves a thin web",
                                f"`{p.id}`: a Ø{2 * r:.1f} mm cut at {np.round(c, 1).tolist()} leaves {max(web, 0):.1f} mm to the outer edge "
                                f"(need ≥ {lim:.1f} mm{'; it breaks through' if web <= 0 else ''}).").on(p.id).here(c)
                           .expect(f">= {lim:.1f} mm", f"{max(web, 0):.1f} mm").fix("Move the hole inward or add a boss around it."))
    if judged and not bad:
        out.append(ok("arch.cut_breakout", G, "Holes keep their webs", f"{judged} cylindrical cuts leave ≥ max(1 mm, 1.5x wall)."))
    return out
