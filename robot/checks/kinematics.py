"""Rotating parts and kinematic consistency.

Builds motion groups (rigid groups joined by fasteners, fused parts, press fits, glue, pins...), decides which of them
rotate (explicit revolute joints, spinning part kinds, `rotates_with`, motor rotors, `shaft` connections) and about which
axis, then checks that nothing ties a rotating group to the static structure, that the rotating groups are carried by
bearings / motors on one axis, driven, retained, balanced, and that nothing static sits in their swept volume.

Boundary parts are never merged into a rigid group: motors (stator on the static side, rotor/bell on the rotating side),
bearings (inner/outer race), belts and locking bars. Missing data never passes: it goes to ctx.not_checked with a warning.
"""

from __future__ import annotations

import math
import re

import numpy as np

from .. import catalog, measure, xform
from ..finding import BLOCKER, INFO, WARNING, fail, note, ok

G = "kinematics"
SPIN_WEAPONS = ("spinner", "drum", "disc", "bar", "shell", "eggbeater")
SPIN_KINDS = {"wheel", "pulley", "wheel_hub", "hub", "tyre"}
BOUNDARY = {"motor", "weapon_motor", "bearing", "belt", "locking_bar"}
STATIC_KINDS = {"structure", "armor", "wedge", "plate", "fork", "battery", "esc", "receiver", "servo", "switch"}
ELECTRONIC = {"battery", "esc", "receiver", "servo", "switch"}
RIGID = {"screw", "pin", "press_fit", "glue", "tape", "snap", "interlock", "velcro"}
FRICTION = {"press_fit", "glue", "tape", "velcro"}
KEY_WORDS = ("key", "d-flat", "d flat", "d-shaft", "flat", "grub", "set screw", "setscrew", "spline", "dowel", "bolted", "bolt",
             "screw", "hex bore", "pin")
RETAIN_WORDS = ("circlip", "e-clip", "eclip", "e clip", "snap ring", "retaining ring", "collar", "shoulder", "nut", "nyloc",
                "grub", "set screw", "flange", "captured", "captive", "spacer", "washer", "clamp")
FLEX_WORDS = ("flexible coupl", "oldham", "jaw coupl", "spider coupl", "torque only, float", "floating")
RUB_GAP = {"weapon": 1.0, "wheel": 0.5, "pulley": 0.3, "other": 0.5}
COAX_MM, COAX_DEG = 0.1, 0.5  # joint vs shaft / bearing / motor axis
AXLE_MM, AXLE_DEG = 0.3, 2.0  # a fastener this close to the spin axis is an axle, not a clamp
STEEL_G_MM3 = 7.9e-3
PLASTIC_G_MM3 = 1.2e-3


# ----------------------------------------------------------------------------------------------- geometry helpers
def unit(v):
    v = np.asarray(v, float)
    n = np.linalg.norm(v)
    return v / n if n > 1e-12 else None


def line_dist(o, d, p):
    q = np.asarray(p, float) - o
    return float(np.linalg.norm(q - (q @ d) * d))


def coax(o1, d1, o2, d2, span=10.0):
    """(angle deg, worst distance mm over +/-span along line 2) between two axes."""
    ang = math.degrees(math.acos(min(1.0, abs(float(d1 @ d2)))))
    dist = max(line_dist(o1, d1, o2 + d2 * s) for s in (-span, 0.0, span))
    return ang, dist


def round_axis(body):
    """(origin, dir) of a round part from its local box: the dim whose two cross extents are equal. None when not round."""
    v = body.geom.mesh.vertices
    if not len(v):
        return None
    lo, hi = v.min(axis=0), v.max(axis=0)
    e = hi - lo
    best = None
    for i in range(3):
        j, k = [x for x in range(3) if x != i]
        if max(e[j], e[k]) < 1e-6:
            continue
        rel = abs(e[j] - e[k]) / max(e[j], e[k])
        if rel < 0.08 and (best is None or rel < best[0] - 1e-6 or (abs(rel - best[0]) < 1e-6 and e[i] < e[best[1]])):
            best = (rel, i)
    if best is None:
        return None
    ax = np.zeros(3)
    ax[best[1]] = 1.0
    c = (lo + hi) / 2
    return xform.apply(body.M, c), unit(xform.apply_dir(body.M, ax))


def radial(P, o, a):
    q = np.atleast_2d(P) - o
    ax = q @ a
    return ax, np.linalg.norm(q - np.outer(ax, a), axis=1)


def basis(a):
    t = np.array([1.0, 0, 0]) if abs(a[0]) < 0.9 else np.array([0, 1.0, 0])
    u = unit(np.cross(a, t))
    return u, np.cross(a, u)


class Sweep:
    """Solid of revolution of a group: per axial bin, the radial band [rmin, rmax] the material passes through."""

    def __init__(self, P, o, a, bw=0.1):
        self.o, self.a, self.bw = o, a, bw
        ax, rad = radial(P, o, a)
        self.amin, self.amax = float(ax.min()), float(ax.max())
        n = max(int(math.ceil((self.amax - self.amin) / bw)), 1)
        idx = np.clip(((ax - self.amin) / bw).astype(int), 0, n - 1)
        self.rmin = np.full(n, np.inf)
        self.rmax = np.full(n, -np.inf)
        np.minimum.at(self.rmin, idx, rad)
        np.maximum.at(self.rmax, idx, rad)
        self.n = n
        self.R = float(rad.max())

    def aabb(self):
        c = self.o + self.a * (self.amin + self.amax) / 2
        h = (self.amax - self.amin) / 2
        e = np.array([h * abs(self.a[k]) + self.R * math.sqrt(max(0.0, 1 - self.a[k] ** 2)) for k in range(3)])
        return np.array([c - e, c + e])

    def classify(self, P, gapmax):
        """(depth inside the sweep (<=0 outside), gap to the sweep) per point."""
        ax, rad = radial(P, self.o, self.a)
        depth = np.full(len(P), -np.inf)
        gap = np.full(len(P), np.inf)
        w = int(math.ceil(gapmax / self.bw)) + 1
        base = np.floor((ax - self.amin) / self.bw).astype(int)
        for k in range(-w, w + 1):
            b = base + k
            ok_ = (b >= 0) & (b < self.n)
            if not ok_.any():
                continue
            bi = np.clip(b, 0, self.n - 1)
            lo_a = self.amin + bi * self.bw
            dax = np.maximum(np.maximum(lo_a - ax, ax - (lo_a + self.bw)), 0.0)
            rmn, rmx = self.rmin[bi], self.rmax[bi]
            valid = ok_ & np.isfinite(rmn)
            dr = np.maximum(np.maximum(rmn - rad, rad - rmx), 0.0)
            g = np.where(valid, np.sqrt(dax ** 2 + dr ** 2), np.inf)
            gap = np.minimum(gap, g)
            if k == 0:
                inner = np.minimum(rad - rmn, rmx - rad)
                axd = np.minimum(ax - self.amin, self.amax - ax)
                depth = np.where(valid, np.minimum(inner, axd), depth)
        return depth, gap


# ----------------------------------------------------------------------------------------------- model
class UF:
    def __init__(self, items):
        self.p = {i: i for i in items}

    def find(self, x):
        while self.p[x] != x:
            self.p[x] = self.p[self.p[x]]
            x = self.p[x]
        return x

    def union(self, a, b):
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            self.p[rb] = ra


class RGroup:
    def __init__(self, gid, members):
        self.gid = gid
        self.members = set(members)
        self.fasteners = []  # fastener ids carried by the group
        self.axis = None  # (origin, dir)
        self.axis_src = None
        self.joints = []  # (pid, origin, dir, joint)
        self.rotors = []  # (motor pid, how, member pid)
        self.bearings = []  # bearing pids with one race on this group
        self.shaft_partners = []  # static parts this group turns on through a `shaft` connection
        self.weapon = None
        self.cls = "other"
        self.driven = False


def declared_fixed(p):
    return bool(p.fixed) or str(p.rotates_with or "").lower() in ("fixed", "static", "none", "ground")


def declared_rot(p):
    return None if declared_fixed(p) or not p.rotates_with else str(p.rotates_with)


def is_spin_weapon(spec, p):
    if p.kind != "weapon":
        return False
    wd = p.weapon
    if wd is not None and wd.kind in SPIN_WEAPONS:
        return True
    return spec.is_spinner and (wd is None or wd.kind != "none")


class Kin:
    def __init__(self, ctx):
        self.ctx, self.r, self.w = ctx, ctx.r, ctx.world
        self.spec = self.r.spec
        self.parts = {rp.part.id: rp for rp in self.r.parts}
        self.out = []
        self.ran = {}
        self.h = 2.0 if self.r.fast else 1.0
        self._pairs_done = {}
        self.edges = {}  # pid -> list of (other pid, label, quality) ; quality: key / friction / rigid
        self.build()

    # findings -----------------------------------------------------------
    def check(self, cid, title_ok, msg_ok):
        self.ran.setdefault(cid, (title_ok, msg_ok, 0))
        return cid

    def bad(self, cid, sev, title, msg, parts=(), fix=None, at=None, expect=None):
        f = fail(cid, G, sev, title, msg).on(*parts)
        if fix:
            f.fix(fix)
        if at is not None:
            f.here(at)
        if expect:
            f.expect(*expect)
        self.out.append(f)
        t, m, n = self.ran.get(cid, (title, msg, 0))
        self.ran[cid] = (t, m, n + 1)
        return f

    def info(self, cid, title, msg, parts=()):
        self.out.append(note(cid, G, title, msg).on(*parts))

    def skip(self, cid, what):
        self.ctx.not_checked.append(f"Kinematics `{cid}`: {what}")

    def finish(self):
        for cid, (t, m, n) in self.ran.items():
            if n == 0:
                self.out.append(ok(cid, G, t, m))
        return self.out

    # model ---------------------------------------------------------------
    def body(self, pid):
        return self.w.body(pid)

    def kind(self, pid):
        rp = self.parts.get(pid)
        return rp.part.kind if rp else None

    def joint_world(self, pid):
        p = self.parts[pid].part
        j = p.joint
        a = unit(j.axis)
        if a is None:
            return None
        Mp = np.eye(4)
        if p.parent and self.body(p.parent) is not None:
            Mp = self.body(p.parent).M
        return xform.apply(Mp, j.pivot), unit(xform.apply_dir(Mp, a))

    def revolute(self, pid):
        j = self.parts[pid].part.joint
        return j is not None and j.kind in ("revolute", "continuous")

    def joint_root(self, pid):
        """Nearest ancestor-or-self with a revolute joint (kinematic rotation source), else None."""
        seen = set()
        cur = pid
        while cur and cur in self.parts and cur not in seen:
            seen.add(cur)
            if self.revolute(cur):
                return cur
            cur = self.parts[cur].part.parent
        return None

    def ancestors(self, pid):
        out, seen = [], set()
        cur = self.parts[pid].part.parent if pid in self.parts else None
        while cur and cur in self.parts and cur not in seen:
            seen.add(cur)
            out.append(cur)
            cur = self.parts[cur].part.parent
        return out

    def motor_info(self, pid):
        rp = self.parts.get(pid)
        b = self.body(pid)
        if rp is None or b is None or rp.cat is None or not rp.cat.shaft:
            return None
        sh = rp.cat.shaft
        o = xform.apply(b.M, sh["at"])
        d = unit(xform.apply_dir(b.M, sh["dir"]))
        v = b.geom.mesh.vertices
        local_dir = unit(sh["dir"])
        xs = v @ local_dir
        return {"o": o, "d": d, "len": float(sh.get("len", 0)), "dia": float(sh.get("dia", 3.0)),
                "outrunner": rp.cat.kind == "weapon_motor" or "outrunner" in rp.cat.name.lower(),
                "back": float(xs.min()), "can_end": float(np.asarray(sh["at"]) @ local_dir), "local_dir": local_dir,
                "R": float(np.linalg.norm(v - np.outer(xs, local_dir), axis=1)[xs <= float(np.asarray(sh["at"]) @ local_dir) + 1e-6].max())}

    def motor_side(self, mpid, entry_world):
        """'stator' or 'bell' for a point where something lands on a motor. Gearmotor cans are static everywhere."""
        mi = self.motor_info(mpid)
        if mi is None:
            return None
        if not mi["outrunner"]:
            return "stator"
        q = xform.apply(xform.inv(self.body(mpid).M), entry_world)
        x = float(q @ mi["local_dir"])
        face = getattr(catalog, "MOTOR_FACES", {}).get(self.parts[mpid].cat.id, {"stator_face": "-x", "depth_mm": 2.0})
        dep = float(face.get("depth_mm", 2.0))
        if face.get("stator_face") == "+x":
            return "stator" if x >= mi["can_end"] - dep else "bell"
        return "stator" if x <= mi["back"] + dep else "bell"

    def pierce(self, f):
        """Bodies the shank of fastener f geometrically passes through (sampled along its axis), with entry points."""
        dl = catalog.parse_designation(f.designation)
        if not dl:
            return None
        d, L = dl
        dr = unit(f.dir)
        at = np.asarray(f.at, float)
        ts = np.arange(0.25, L - 0.1, 0.25)
        P = at + np.outer(ts, dr)
        hits = {}
        for b in self.w.bodies:
            if b.fastener or b.is_wire or b.part_idx is None:
                continue
            if not measure.aabb_overlap(np.array([P.min(axis=0), P.max(axis=0)]), b.aabb, 0.1):
                continue
            ins = np.nonzero(b.inside(P))[0]
            if len(ins) >= 2:
                hits[b.id] = P[ins[0]]
        return hits

    def build(self):
        spec = self.spec
        ids = list(self.parts)
        uf = UF(ids)

        def edge(a, b, label, q):
            self.edges.setdefault(a, []).append((b, label, q))
            self.edges.setdefault(b, []).append((a, label, q))

        self.rotor_links = []  # (motor, partner, how, quality, entry)
        self.stator_links = []  # (motor, partner, how)
        self.bearing_links = {}  # bearing -> list of (partner, how)
        self.shaft_links = []  # (a, b) connections with method shaft
        self.belt_pulleys = {}
        # connections
        for c in spec.connections:
            if c.a not in self.parts or c.b not in self.parts or c.a == c.b:
                continue
            ka, kb = self.kind(c.a), self.kind(c.b)
            reason = (c.reason or "").lower()
            q = "key" if (c.mechanical_key or c.method in ("screw", "pin", "snap") or any(k in reason for k in KEY_WORDS)) \
                and c.method not in ("tape", "velcro") else ("friction" if c.method in FRICTION else "rigid")
            for x, y, kx in ((c.a, c.b, ka), (c.b, c.a, kb)):
                if kx == "bearing":
                    self.bearing_links.setdefault(x, []).append((y, c.method))
            if ka in BOUNDARY or kb in BOUNDARY:
                for m, o in ((c.a, c.b), (c.b, c.a)):
                    if self.kind(m) in ("motor", "weapon_motor") and self.kind(o) not in BOUNDARY:
                        self.rotor_links.append((m, o, f"connection {c.method}", q, None, reason))
                continue
            if c.method == "shaft":
                self.shaft_links.append((c.a, c.b))
                continue
            if c.method in RIGID:
                uf.union(c.a, c.b)
                edge(c.a, c.b, f"{c.method} connection `{c.a}`-`{c.b}`", q)
        for pid, rp in self.parts.items():
            p = rp.part
            for other, label in ((p.fused_with, "fused_with"), (p.tyre_of, "tyre_of")):
                for o in ([other] if isinstance(other, str) else (other or [])):
                    if o in self.parts and self.kind(pid) not in BOUNDARY and self.kind(o) not in BOUNDARY:
                        uf.union(pid, o)
                        edge(pid, o, f"`{pid}` {label} `{o}`", "key")
            if p.belt is not None:
                self.belt_pulleys[pid] = list(p.belt.pulleys or [])
            # a child (without its own joint) of a rotating joint moves with it
            if p.parent in self.parts and p.joint is None and self.joint_root(p.parent) and self.kind(pid) not in BOUNDARY \
                    and self.kind(p.parent) not in BOUNDARY:
                uf.union(pid, p.parent)
                edge(pid, p.parent, f"`{pid}` is a child of `{p.parent}`", "key")
        # parts declaring the same rotating group move together (the declaration is the joint)
        bylab = {}
        for pid, rp in self.parts.items():
            lab = declared_rot(rp.part)
            if lab and self.kind(pid) not in BOUNDARY:
                bylab.setdefault(lab, []).append(pid)
        for lab, ps in bylab.items():
            if lab in self.parts and self.kind(lab) not in BOUNDARY and lab not in ps:
                ps.append(lab)
            for x in ps[1:]:
                uf.union(ps[0], x)
                edge(ps[0], x, f"both declare `rotates_with: {lab}`", "key")
        self.uf = uf
        # fasteners (geometry + declaration)
        self.fpierce = {}
        for f in spec.fasteners:
            hits = self.pierce(f)
            if hits is None:
                self.skip("kin.fastener_boundary", f"fastener `{f.id}` designation `{f.designation}` not understood")
                continue
            declared = [x for x in list(f.through or []) + ([f.threads_into] if f.threads_into else []) if x in self.parts]
            allp = dict(hits)
            for x in declared:
                allp.setdefault(x, None)
            self.fpierce[f.id] = (allp, set(hits), set(declared))

    def finalize_groups(self):
        """Rigid groups -> rotating groups (after fasteners that do not cross a boundary are merged)."""
        uf = self.uf
        ids = list(self.parts)
        seeds = set()
        for pid in ids:
            p = self.parts[pid].part
            if self.kind(pid) in BOUNDARY:
                continue
            if self.revolute(pid) or self.kind(pid) in SPIN_KINDS or is_spin_weapon(self.spec, p) or declared_rot(p):
                seeds.add(pid)
        for m, o, *_ in self.rotor_links:
            if self.kind(o) in SPIN_KINDS or o in seeds:
                seeds.add(o)
        self.seeds = seeds
        groups = {}
        for pid in ids:
            if self.kind(pid) in BOUNDARY:
                continue
            groups.setdefault(uf.find(pid), []).append(pid)
        self.gof = {}
        self.rgroups = {}
        for root, mem in groups.items():
            for m in mem:
                self.gof[m] = root
            if any(m in seeds for m in mem):
                self.rgroups[root] = RGroup(root, mem)

    def group_of(self, pid):
        return self.gof.get(pid)

    def rot(self, pid):
        g = self.gof.get(pid)
        return self.rgroups.get(g)


# ----------------------------------------------------------------------------------------------- checks
def run(ctx):
    k = Kin(ctx)
    spec = k.spec
    # Pre-group so fasteners can be judged against motion groups.
    k.finalize_groups()
    fasteners_checks(k)
    k.finalize_groups()  # fasteners that stay inside one motion group joined it
    for f, (allp, _, _) in k.fpierce.items():
        gs = {k.group_of(p) for p in allp if k.kind(p) not in BOUNDARY}
        gs.discard(None)
        if len(gs) == 1:
            g = k.rgroups.get(next(iter(gs)))
            if g is not None and f not in k.axle_fasteners:
                g.fasteners.append(f)
    motor_links_from_fasteners(k)
    for g in k.rgroups.values():
        setup_group(k, g)
    motion_declared(k)
    joints_checks(k)
    rigid_mix(k)
    bearings_checks(k)
    motors_checks(k)
    torque_path(k)
    bore_fit(k)
    retention(k)
    weapon_checks(k)
    balance(k)
    sweeps(k)
    wheels(k)
    belts(k)
    tyres(k)
    wires(k)
    if not k.rgroups:
        k.info("kin.none", "No rotating parts", "No part rotates (no revolute joint, wheel, pulley or spinning weapon); rotation checks skipped.")
    ctx.metrics["kin_rotating_groups"] = float(len(k.rgroups))
    return k.finish()


def label(g):
    return "+".join(sorted(g.members))


def fasteners_checks(k):
    k.check("kin.fastener_boundary", "No screw ties a rotating part to a static one",
            "Every screw stays inside one motion group, or runs on the spin axis as an axle.")
    k.check("kin.fastener_undeclared", "Screws only pass through declared parts",
            "No screw's shank passes through a rotating part it does not list in `through`/`threads_into`.")
    k.axle_fasteners = set()
    for f in k.spec.fasteners:
        if f.id not in k.fpierce:
            continue
        allp, geo, decl = k.fpierce[f.id]
        dr = unit(f.dir)
        at = np.asarray(f.at, float)
        rot = {}
        stat = []
        for p in allp:
            if k.kind(p) in BOUNDARY:
                continue
            g = k.rot(p)
            if g is not None:
                rot.setdefault(g.gid, []).append(p)
            else:
                stat.append(p)
        for p in geo - decl:
            if k.rot(p) is not None:
                k.bad("kin.fastener_undeclared", WARNING, "Screw passes through a rotating part it does not list",
                      f"The shank of `{f.id}` runs through `{p}` (rotating) but `{p}` is not in its `through`/`threads_into`.",
                      (f.id, p), at=allp[p],
                      fix="Move the screw out of the rotating part, or declare it if it really is meant to clamp it.")
        if rot and (stat or len(rot) > 1):
            g = k.rgroups[next(iter(rot))]
            ax = group_axis_guess(k, g)
            if ax is not None:
                ang, dist = coax(ax[0], ax[1], at, dr, 3.0)
                if ang < AXLE_DEG and dist < AXLE_MM:
                    k.axle_fasteners.add(f.id)
                    k.info("kin.fastener_coaxial", "Screw runs on the spin axis",
                           f"`{f.id}` crosses a rotating/static boundary on the spin axis ({dist:.2f} mm off): it acts as an axle.",
                           (f.id,))
                    continue
            rp = sorted(p for v in rot.values() for p in v)
            k.bad("kin.fastener_boundary", BLOCKER, "Screw ties a rotating part to a static one",
                  f"`{f.id}` passes through {', '.join(f'`{p}`' for p in rp)} (rotating) and "
                  f"{', '.join(f'`{p}`' for p in stat) or 'another rotating group'}; the first spin rips it apart"
                  + ("" if ax is None else f" (it is {line_dist(ax[0], ax[1], at):.1f} mm off the spin axis)") + ".",
                  (f.id, *rp, *stat), at=at,
                  fix="Keep every eccentric screw entirely inside the rotating group (all parts it passes through spin together); "
                      "move or shorten it so it does not reach the fork/body.")
            continue
        # merge: all non-boundary parts it holds become one rigid group
        nb = [p for p in allp if k.kind(p) not in BOUNDARY]
        for p in nb[1:]:
            k.uf.union(nb[0], p)
            k.edges.setdefault(nb[0], []).append((p, f"screw `{f.id}`", "key"))
            k.edges.setdefault(p, []).append((nb[0], f"screw `{f.id}`", "key"))


def motor_links_from_fasteners(k):
    k.check("kin.motor_face", "Screws into motors land on the matching face",
            "Static parts screw to the stator face and rotating parts to the bell.")
    for f in k.spec.fasteners:
        if f.id not in k.fpierce:
            continue
        allp, geo, _ = k.fpierce[f.id]
        motors = [p for p in allp if k.kind(p) in ("motor", "weapon_motor")]
        others = [p for p in allp if k.kind(p) not in BOUNDARY]
        for m in motors:
            entry = allp.get(m)
            if entry is None:
                k.skip("kin.motor_face", f"`{f.id}` does not reach `{m}` geometrically; which motor face it lands on is unknown")
                continue
            side = k.motor_side(m, entry)
            if side is None:
                k.skip("kin.motor_face", f"`{m}` has no catalog shaft, face of `{f.id}` unknown")
                continue
            for o in others:
                g = k.rot(o)
                if side == "stator":
                    if g is not None:
                        k.bad("kin.motor_face", BLOCKER, "Rotating part screwed to the motor's stator",
                              f"`{f.id}` lands on the stator face of `{m}` but also holds rotating `{o}`.", (f.id, m, o), at=entry,
                              fix="Bolt the rotating part to the bell (rotor) bolt circle, not the stator mount face.")
                    else:
                        k.stator_links.append((m, o, f"screw `{f.id}`"))
                else:
                    if g is None:
                        k.bad("kin.motor_face", BLOCKER, "Static part screwed to the spinning bell",
                              f"`{f.id}` holds static `{o}` and lands on the rotating bell of `{m}` (not its stator face); the bell cannot turn.",
                              (f.id, m, o), at=entry,
                              fix="Move the screws to the stator mount face (back of the motor) or mount the motor by its stator.")
                    else:
                        k.rotor_links.append((m, o, f"screw `{f.id}`", "key", entry, ""))


def group_axis_guess(k, g):
    if g.axis is not None:
        return g.axis
    setup_group(k, g)
    return g.axis


def setup_group(k, g):
    if g.axis is not None or g.axis_src == "none":
        return
    spec = k.spec
    g.joints = []
    for m in g.members:
        if k.revolute(m):
            jw = k.joint_world(m)
            if jw is not None:
                g.joints.append((m, jw[0], jw[1]))
        p = k.parts[m].part
        if is_spin_weapon(spec, p):
            g.weapon = m
    kinds = {k.kind(m) for m in g.members}
    g.cls = "weapon" if g.weapon else ("wheel" if kinds & {"wheel", "tyre", "wheel_hub"} else ("pulley" if "pulley" in kinds else "other"))
    g.rotors = [(m, how, o, q, e, rs) for m, o, how, q, e, rs in k.rotor_links if o in g.members]
    for a, b in k.shaft_links:
        if a in g.members and b not in g.members:
            g.shaft_partners.append(b)
        elif b in g.members and a not in g.members:
            g.shaft_partners.append(a)
    if g.joints:
        g.axis, g.axis_src = (g.joints[0][1], g.joints[0][2]), f"joint of `{g.joints[0][0]}`"
        return
    if g.weapon:
        from .power import spin_axis
        i = k.w.index(g.weapon)
        sa = spin_axis(k.w, k.r, i) if i is not None else None
        if sa is not None:
            g.axis, g.axis_src = sa, f"`{g.weapon}` spin_axis"
            return
    for m, how, o, q, e, rs in g.rotors:
        mi = k.motor_info(m)
        if mi is not None:
            g.axis, g.axis_src = (mi["o"], mi["d"]), f"shaft of motor `{m}`"
            return
    for s in g.shaft_partners:
        b = k.body(s)
        ra = round_axis(b) if b is not None else None
        if ra is not None:
            g.axis, g.axis_src = ra, f"axle `{s}`"
            return
    for m in sorted(g.members, key=lambda x: (k.kind(x) not in ("wheel", "pulley", "wheel_hub", "hub"), x)):
        b = k.body(m)
        ra = round_axis(b) if b is not None else None
        if ra is not None:
            g.axis, g.axis_src = ra, f"round shape of `{m}`"
            return
    g.axis_src = "none"


def motion_declared(k):
    k.check("kin.motion_declared", "Declared motion groups match the mechanism",
            "Every `rotates_with` / `fixed` declaration agrees with the joints and joins.")
    labels = {}
    for pid, rp in k.parts.items():
        p = rp.part
        g = k.rot(pid)
        if p.fixed and declared_rot(p):
            k.bad("kin.motion_declared", BLOCKER, "Part is both fixed and rotating",
                  f"`{pid}` declares `fixed` and `rotates_with: {p.rotates_with}`.", (pid,))
        if declared_fixed(p) and g is not None:
            k.bad("kin.motion_declared", BLOCKER, "Fixed part is joined to a rotating group",
                  f"`{pid}` is declared `fixed` but is rigidly joined to rotating {label(g)}.", (pid,),
                  fix="Break the rigid join (screw, press fit, glue, parent) between it and the spinning parts.")
        if declared_rot(p):
            if g is None and k.kind(pid) not in BOUNDARY:
                k.bad("kin.motion_declared", BLOCKER, "Part declared rotating is not on anything that turns",
                      f"`{pid}` declares `rotates_with: {p.rotates_with}` but no joint, motor rotor or bearing makes it turn.", (pid,))
            if g is not None:
                labels.setdefault(g.gid, set()).add(declared_rot(p))
    for gid, ls in labels.items():
        if len(ls) > 1:
            g = k.rgroups[gid]
            k.bad("kin.motion_declared", BLOCKER, "One rigid group declared in two motion groups",
                  f"{label(g)} are rigidly joined but declare `rotates_with` {sorted(ls)}: an overconstraint.", sorted(g.members))
    n_decl = sum(1 for rp in k.parts.values() if declared_fixed(rp.part) or declared_rot(rp.part))
    if k.rgroups:
        k.info("kin.motion_inferred", "Motion groups",
               "; ".join(f"{label(g)} about {g.axis_src}" for g in k.rgroups.values())
               + f" ({n_decl} parts declare motion explicitly, the rest is inferred).")


def joints_checks(k):
    spec = k.spec
    k.check("kin.spin_joint", "Spinning parts are on revolute joints",
            "Every weapon, wheel and pulley turns about a declared joint, motor shaft or axle.")
    k.check("kin.joint_kind", "Spinner joints are revolute", "Spinning parts use revolute joints.")
    k.check("kin.joint_axis_zero", "Joint axes are defined", "Every joint has a non-zero axis.")
    k.check("kin.joint_child_static", "Nothing static hangs off a spinning joint",
            "No structure or electronics is a child of a spinning joint.")
    k.check("kin.parent_mismatch", "Rotating groups move with their joint",
            "Every part rigidly joined to a jointed group is also its child, so sweeps move it.")
    k.check("kin.group_axes_conflict", "One axis per rotating group", "No rotating group has two different joint axes.")
    for pid, rp in k.parts.items():
        j = rp.part.joint
        if j is not None and unit(j.axis) is None:
            k.bad("kin.joint_axis_zero", BLOCKER, "Joint axis is zero", f"`{pid}` has joint axis {j.axis}.", (pid,),
                  fix="Give the joint a unit axis in the parent frame.")
        if j is not None and j.kind == "prismatic" and (is_spin_weapon(spec, rp.part) or k.kind(pid) in SPIN_KINDS):
            k.bad("kin.joint_kind", BLOCKER, "Spinning part on a sliding joint",
                  f"`{pid}` ({k.kind(pid)}) has a prismatic joint; it must be revolute.", (pid,))
        if j is not None and k.revolute(pid) and pid in k.seeds:
            for c, crp in k.parts.items():
                if c != pid and k.joint_root(c) == pid and k.kind(c) in STATIC_KINDS:
                    k.bad("kin.joint_child_static", BLOCKER, "Static part rides on a spinning joint",
                          f"`{c}` ({k.kind(c)}) is a child of spinning `{pid}` without its own joint, so it spins with it.",
                          (c, pid), fix=f"Parent `{c}` to the structure, not to the rotating part.")
    for g in k.rgroups.values():
        members = sorted(g.members)
        if len(g.joints) > 1:
            o0, d0 = g.joints[0][1], g.joints[0][2]
            for m, o, d in g.joints[1:]:
                ang, dist = coax(o0, d0, o, d)
                if ang > COAX_DEG or dist > COAX_MM:
                    k.bad("kin.group_axes_conflict", BLOCKER, "Rigid group has two joint axes",
                          f"`{g.joints[0][0]}` and `{m}` are rigidly joined but their joints are {ang:.1f} deg / {dist:.2f} mm apart; it cannot turn.",
                          (g.joints[0][0], m))
        has_joint = bool(g.joints) or any(k.joint_root(m) for m in g.members)
        if g.weapon:
            if not has_joint:
                k.bad("kin.spin_joint", BLOCKER, "Spinning weapon has no joint",
                      f"Weapon group {label(g)} has no revolute joint (parents: "
                      + ", ".join(f"`{m}`->`{k.parts[m].part.parent}`" for m in members if k.parts[m].part.parent) +
                      "); the verifier sees it as part of the structure and its rotation, sweep and clearances are never checked.",
                      members, fix=f"Give `{g.weapon}` a revolute `joint` about the shaft axis (pivot on the axis) and make hub/shaft/"
                                   "disc its children; keep bearings and the motor stator on the structure.")
        elif not has_joint:
            if g.rotors or g.shaft_partners or g.bearings or any(declared_rot(k.parts[m].part) for m in g.members):
                k.info("kin.spin_joint", "Rotation implied by a motor shaft or axle",
                       f"{label(g)} turns about {g.axis_src} (no explicit joint; declare one to enable sweeps).", members)
            elif not belt_linked(k, g):
                k.bad("kin.spin_joint", BLOCKER, "Spinning part with no joint",
                      f"{label(g)} ({g.cls}) has no revolute joint, no motor shaft, no axle (`shaft` connection) and no bearing.",
                      members, fix="Add a revolute joint, or a `shaft` connection to its axle, or mount it on a motor shaft.")
        for jm, _, _ in g.joints:
            for m in members:
                if m != jm and k.joint_root(m) is None and k.kind(m) not in BOUNDARY:
                    k.bad("kin.parent_mismatch", WARNING, "Part spins with a joint it is not a child of",
                          f"`{m}` is rigidly joined to `{jm}` (jointed) but is not its child; joint sweeps leave it behind.",
                          (m, jm), fix=f"Set `parent: {jm}` (with `at` in its frame) on `{m}`.")
            par = k.parts[jm].part.parent
            if par and k.rot(par) is not None and k.rot(par) is not g:
                k.info("kin.joint_parent_rotating", "Joint mounted on another rotating part",
                       f"`{jm}` is jointed to `{par}`, which itself rotates (nested rotation).", (jm, par))
            j = k.parts[jm].part.joint
            if g.cls == "weapon" and abs(j.max - j.min) < 360 - 1e-6:
                k.info("kin.joint_range", "Spinner joint range below one turn",
                       f"`{jm}` joint range {j.min}..{j.max} deg; this module sweeps the full turn anyway.", (jm,))


def belt_linked(k, g):
    for b, ps in k.belt_pulleys.items():
        if any(p in g.members for p in ps):
            return True
    return False


def rigid_mix(k):
    k.check("kin.rigid_mix", "No rotating group is rigidly tied to the structure",
            "No chain of screws, press fits, glue or pins joins a spinning part to a static one.")
    k.check("kin.rotating_electronics", "No electronics spin", "No battery, ESC, receiver or switch is in a rotating group.")
    for g in k.rgroups.values():
        anc = set()
        for jm, _, _ in g.joints:
            anc |= set(k.ancestors(jm))
        static = sorted(m for m in g.members if (k.kind(m) in STATIC_KINDS and k.kind(m) not in ELECTRONIC) or m in anc
                        or declared_fixed(k.parts[m].part))
        elec = sorted(m for m in g.members if k.kind(m) in ELECTRONIC)
        spin = sorted(m for m in g.members if m in k.seeds)
        if static:
            path = chain(k, spin[0], static[0]) if spin else []
            k.bad("kin.rigid_mix", BLOCKER, "Spinning part is rigidly joined to the structure",
                  f"Rigid group {label(g)} holds spinning {', '.join(f'`{s}`' for s in spin)} and static "
                  f"{', '.join(f'`{s}`' for s in static)}" + (f" via {' -> '.join(path)}" if path else "") + "; it cannot turn (or rips apart).",
                  spin + static, fix="Break that join: the rotating group may meet the structure only through bearings, an axle or the motor stator/rotor boundary.")
        if elec:
            k.bad("kin.rotating_electronics", BLOCKER, "Electronics in a rotating group",
                  f"{', '.join(f'`{e}`' for e in elec)} are rigidly joined to rotating {label(g)}; wires would wrap and tear.",
                  elec + spin)


def chain(k, a, b):
    prev = {a: None}
    q = [a]
    while q:
        x = q.pop(0)
        if x == b:
            break
        for y, lab, _ in k.edges.get(x, []):
            if y not in prev:
                prev[y] = (x, lab)
                q.append(y)
    if b not in prev:
        return []
    out = []
    cur = b
    while prev[cur] is not None:
        x, lab = prev[cur]
        out.append(lab)
        cur = x
    return list(reversed(out))


HUB_COAX_MM = 0.05  # motor-as-hub: the extra bearing / extended shaft must be this coaxial with the motor shaft


def motor_own_shaft(k, sid, m):
    """(bool, why): `sid` is motor `m`'s own shaft (motor-as-hub, the shaft extended through the bell), not a separate shaft
    pushed through the stator. Declared by `shaft_of: <motor>` on the shaft or `motor_shaft_extended: true` on the motor,
    or inferred when the shaft is coaxial with the motor (<0.05 mm) and no fatter than the catalog shaft."""
    mi = k.motor_info(m)
    sb = k.body(sid)
    if mi is None or sb is None:
        return False, f"`{m}` has no catalog shaft"
    ra = round_axis(sb)
    if ra is None:
        return False, f"`{sid}` is not round"
    ang, dist = coax(mi["o"], mi["d"], ra[0], ra[1])
    rad = float(np.max(radial(sb.mesh.vertices, ra[0], ra[1])[1]))
    sp, mp = k.parts[sid].part, k.parts[m].part
    declared = getattr(sp, "_extra", {}).get("shaft_of") == m or bool(getattr(mp, "_extra", {}).get("motor_shaft_extended"))
    fits = rad <= mi["dia"] / 2 + HUB_COAX_MM
    if declared and ang <= COAX_DEG and dist <= COAX_MM and fits:
        return True, f"`{sid}` is declared the motor's own shaft"
    gid = k.group_of(sid)
    rigid = any(mm == m and k.group_of(o) == gid and not any(w in rs for w in FLEX_WORDS) for mm, o, how, q, e, rs in k.rotor_links)
    if not rigid:
        return False, f"`{sid}` is not rigidly coupled to `{m}`'s rotor (a separate shaft)"
    if ang <= COAX_DEG and dist <= HUB_COAX_MM and fits:
        return True, f"`{sid}` is coaxial with `{m}` and inside its {mi['dia']:.1f} mm shaft envelope"
    if not fits:
        return False, f"`{sid}` is {2 * rad:.1f} mm, fatter than `{m}`'s {mi['dia']:.1f} mm shaft"
    return False, f"`{sid}` is {dist:.2f} mm / {ang:.2f} deg off `{m}`'s axis"


def motors_checks(k):
    k.check("kin.motor_mount", "Motor stators are fixed to the structure", "Every motor's stator is held by a static part.")
    k.check("kin.joint_axis_motor", "Motor shafts are coaxial with what they drive",
            f"Direct-drive motor axes match their rotating group within {COAX_MM} mm / {COAX_DEG} deg.")
    k.check("kin.shaft_through_stator", "No shaft passes through a motor",
            "No shaft or pin part intersects a motor body.")
    k.check("kin.double_bearing", "One bearing system per axis",
            "No rotating group is carried both by its own bearings and by a rigidly coupled motor's bearings.")
    motors = [pid for pid in k.parts if k.kind(pid) in ("motor", "weapon_motor")]
    for m in motors:
        b = k.body(m)
        if b is None:
            continue
        held = [o for mm, o, _ in k.stator_links if mm == m]
        for mm, o, how, q, e, rs in k.rotor_links:
            if mm == m and k.rot(o) is None:
                held.append(o)
        if not held:
            near = []
            for sb in k.w.bodies:
                if sb is b or sb.fastener or sb.is_wire or sb.part_idx is None or k.rot(sb.id) is not None or k.kind(sb.id) in BOUNDARY:
                    continue
                if measure.aabb_overlap(b.aabb, sb.aabb, 0.2) and measure.min_gap(b, sb, 0.3) < 0.2:
                    near.append(sb.id)
            if near:
                k.info("kin.motor_mount", "Motor held by contact only",
                       f"`{m}` has no declared stator mount but touches static {', '.join(f'`{x}`' for x in near[:4])}; declare a connection.", (m,))
            else:
                k.bad("kin.motor_mount", BLOCKER, "Motor stator is not fixed",
                      f"Nothing static holds `{m}` (no screw into its stator face, no connection to a static part, no contact).",
                      (m,), fix="Bolt the stator face to the structure or clamp the can in a printed cradle (connection press_fit).")
        mi = k.motor_info(m)
        rotor_groups = {k.rot(o).gid: k.rot(o) for mm, o, *_ in k.rotor_links if mm == m and k.rot(o) is not None}
        if mi is None and rotor_groups:
            k.skip("kin.joint_axis_motor", f"`{m}` has no catalog shaft; coaxiality with the driven part not checked")
            k.bad("kin.joint_axis_motor", WARNING, "Motor shaft axis unknown", f"`{m}` drives {', '.join(label(g) for g in rotor_groups.values())} but has no catalog shaft.", (m,))
        for g in rotor_groups.values():
            if mi is None or g.axis is None:
                continue
            ang, dist = coax(g.axis[0], g.axis[1], mi["o"], mi["d"])
            if ang > COAX_DEG or dist > COAX_MM:
                k.bad("kin.joint_axis_motor", BLOCKER, "Motor shaft is off the rotating axis",
                      f"`{m}` shaft is {dist:.2f} mm / {ang:.2f} deg off the axis of {label(g)} ({g.axis_src}); allowed {COAX_MM} mm / {COAX_DEG} deg.",
                      (m, *sorted(g.members)), at=mi["o"], expect=(f"<= {COAX_MM} mm", f"{dist:.2f} mm"),
                      fix="Put the joint pivot / shaft on the motor axis, or couple through a belt.")
            own = [x for x in g.bearings]
            stator_static = bool(held)
            flex = any(any(w in rs for w in FLEX_WORDS) for mm2, how, o, q, e, rs in g.rotors if mm2 == m)
            hub = [x for x in g.members if k.kind(x) in ("shaft", "pin") and motor_own_shaft(k, x, m)[0]]
            if hub and not flex and stator_static:
                # Motor-as-hub: the motor's own bearings carry the rotor; ONE extra bearing on the far side is fine when it
                # is coaxial with the motor shaft (<0.05 mm). More, or an off-axis one, fights the motor bearings.
                offs = []
                for bp in own:
                    ra = round_axis(k.body(bp)) if k.body(bp) is not None else None
                    a2, d2 = coax(mi["o"], mi["d"], ra[0], ra[1]) if ra is not None else (90.0, 99.0)
                    if a2 > COAX_DEG or d2 > HUB_COAX_MM:
                        offs.append(f"`{bp}` {d2:.2f} mm / {a2:.2f} deg")
                if len(own) >= 2 or offs:
                    k.bad("kin.double_bearing", BLOCKER, "Extra bearing fights the motor's bearings",
                          f"{label(g)} runs on `{m}`'s own shaft ({', '.join(hub)}) and bearings, plus {len(own)} extra bearing(s) "
                          + (f"off the motor axis ({', '.join(offs)}; allowed {HUB_COAX_MM} mm)" if offs else "(only one coaxial extra bearing is allowed)")
                          + ": two bearing systems that are not one line load each other.",
                          (m, *own), at=mi["o"], expect=(f"1 bearing <= {HUB_COAX_MM} mm off the motor axis", f"{len(own)} bearing(s)"),
                          fix="Keep one flanged bearing in the opposite upright, bored on the motor axis, or drive a separate shaft through a flexible coupling.")
                continue
            if len(own) >= 2 and stator_static and ang < 2 and dist < 1 and not flex:
                k.bad("kin.double_bearing", BLOCKER, "Two coaxial bearing systems fight each other",
                      f"{label(g)} runs in its own bearings ({', '.join(own)}) and is rigidly coupled to the bell of `{m}`, whose stator is fixed "
                      "to the structure: the motor's bearings form a second coaxial bearing system and any misalignment loads them.",
                      (m, *own), fix="Either drive through a belt/flexible coupling (live shaft), or mount the stator on a dead shaft "
                                     "clamped in the uprights and run the disc on its own bearings on that shaft.")
    for sb in k.w.bodies:
        if sb.fastener or sb.part_idx is None or k.kind(sb.id) not in ("shaft", "pin"):
            continue
        for m in motors:
            mb = k.body(m)
            if mb is None or not measure.aabb_overlap(sb.aabb, mb.aabb):
                continue
            o = measure.overlap(sb, mb, cap=0.1)
            if o is not None and o.depth > 0.1:
                own_, why = motor_own_shaft(k, sb.id, m)
                if own_:
                    k.info("kin.shaft_through_stator", "Motor's own shaft extended (motor-as-hub)", f"{why}; it runs in the motor's bearings.", (sb.id, m))
                    continue
                k.bad("kin.shaft_through_stator", BLOCKER, "Shaft passes through a motor",
                      f"`{sb.id}` intersects `{m}` ({o.depth:.2f} mm deep, {o.volume:.1f} mm3): a separate shaft cannot pass through the stator "
                      "where the motor's own bearing tube sits.", (sb.id, m), at=o.at,
                      fix="End the shaft at the motor face and couple to the bell, or use the motor's own shaft.")


def bearings_checks(k):
    k.check("kin.bearing_races", "Bearings sit between a rotating and a static part",
            "Every bearing has one race on a rotating group and the other on the structure.")
    k.check("kin.bearing_seat", "Bearings are seated", "Each bearing touches the parts its races are joined to.")
    k.check("kin.joint_axis_bearing", "Bearing bores are on the spin axis",
            f"Every bearing bore is within {COAX_MM} mm / {COAX_DEG} deg of the axis it carries.")
    k.check("kin.shaft_through_bearings", "Something runs in every bearing bore", "Each bearing's bore holds a shaft.")
    for bp, links in k.bearing_links.items():
        b = k.body(bp)
        if b is None:
            continue
        ra = round_axis(b)
        rot = [(o, how) for o, how in links if k.rot(o) is not None]
        stat = [(o, how) for o, how in links if k.rot(o) is None and k.kind(o) not in BOUNDARY]
        if not rot or not stat:
            k.bad("kin.bearing_races", BLOCKER, "Bearing does not sit between moving and static parts",
                  f"`{bp}` is joined to {', '.join(f'`{o}` ({how})' for o, how in links)}: "
                  + ("nothing rotating" if not rot else "nothing static") + " on the other race, so it carries no rotation.",
                  (bp, *[o for o, _ in links]),
                  fix="Join the inner race to the shaft/hub that spins and the outer race to the structure (or the reverse for a dead axle).")
        if len({k.rot(o).gid for o, _ in rot}) > 1:
            k.bad("kin.bearing_races", BLOCKER, "Bearing joined to two rotating groups", f"`{bp}` links two different rotating groups.", (bp,))
        for o, how in rot:
            g = k.rot(o)
            if bp not in g.bearings:
                g.bearings.append(bp)
        for o, how in links:
            ob = k.body(o)
            if ob is None:
                continue
            gap = measure.min_gap(b, ob, 1.0)
            if gap > 0.1:
                k.bad("kin.bearing_seat", BLOCKER, "Bearing is not seated",
                      f"`{bp}` is {('>1' if not np.isfinite(gap) else f'{gap:.2f}')} mm from `{o}` it is joined to ({how}).", (bp, o),
                      fix="Model the pocket/shaft so the race touches it (press fit 0-0.02 mm).")
        if ra is None:
            k.skip("kin.joint_axis_bearing", f"`{bp}` is not round, bore axis unknown")
            k.bad("kin.joint_axis_bearing", WARNING, "Bearing bore axis unknown", f"`{bp}` is not a round solid; its bore axis cannot be found.", (bp,))
            continue
        inner = [ob for ob in (k.body(o) for o, _ in links) if ob is not None and ob.inside(ra[0])[0]]
        if not inner:
            k.bad("kin.shaft_through_bearings", BLOCKER, "Nothing runs in the bearing bore",
                  f"No part joined to `{bp}` passes through its bore centre.", (bp,), at=ra[0],
                  fix="Run the shaft through the bearing (its axis on the bearing axis).")
        for o, how in rot[:1]:
            g = k.rot(o)
            if g.axis is None:
                continue
            ang, dist = coax(g.axis[0], g.axis[1], ra[0], ra[1], 2.0)
            if ang > COAX_DEG or dist > COAX_MM:
                k.bad("kin.joint_axis_bearing", BLOCKER, "Bearing bore is off the spin axis",
                      f"`{bp}` bore is {dist:.2f} mm / {ang:.2f} deg off the axis of {label(g)} ({g.axis_src}).", (bp,), at=ra[0],
                      expect=(f"<= {COAX_MM} mm", f"{dist:.2f} mm"))
            if inner and k.rot(inner[0].id) is None:
                k.info("kin.bearing_orientation", "Bearing turns on its outer race",
                       f"`{bp}`: the inner race is on static `{inner[0].id}` and the outer on rotating `{o}` (dead axle).", (bp,))
    # shafts in rotating groups coaxial with the joint
    k.check("kin.joint_axis_shaft", "Shafts lie on the spin axis",
            f"Every shaft in a rotating group is within {COAX_MM} mm / {COAX_DEG} deg of its axis.")
    k.check("kin.bearing_count", "Weapons are carried by two supports",
            "Every weapon group rests on two bearings, or a motor bearing plus one bearing.")
    for g in k.rgroups.values():
        if g.axis is None:
            continue
        for m in sorted(g.members):
            if k.kind(m) not in ("shaft", "pin"):
                continue
            ra = round_axis(k.body(m))
            if ra is None:
                k.skip("kin.joint_axis_shaft", f"`{m}` is not round")
                continue
            ang, dist = coax(g.axis[0], g.axis[1], ra[0], ra[1])
            if ang > COAX_DEG or dist > COAX_MM:
                k.bad("kin.joint_axis_shaft", BLOCKER, "Shaft is off the spin axis",
                      f"`{m}` is {dist:.2f} mm / {ang:.2f} deg off the axis of {label(g)} ({g.axis_src}).", (m,), at=ra[0],
                      expect=(f"<= {COAX_MM} mm", f"{dist:.2f} mm"), fix="Put the joint pivot on the shaft axis.")
        supports = len(g.bearings) + len({m for m, how, o, q, e, rs in g.rotors
                                          if k.motor_info(m) is not None and not any(w in rs for w in FLEX_WORDS)})
        if g.cls == "weapon" and supports < 2:
            k.bad("kin.bearing_count", BLOCKER, "Weapon is not carried by two supports",
                  f"{label(g)} rests on {len(g.bearings)} bearing(s) and {len(g.rotors)} motor rotor link(s); it needs two supports along the axis.",
                  sorted(g.members), fix="Add bearings (one each side) joined to the shaft/hub and pressed into the structure.")
        if g.cls == "weapon" and len(g.bearings) >= 2:
            ax = [float((k.body(b).center - g.axis[0]) @ g.axis[1]) for b in g.bearings]
            wb = k.body(g.weapon)
            c = float((wb.center - g.axis[0]) @ g.axis[1])
            k.check("kin.bearing_straddle", "Weapon bearings straddle the weapon", "The weapon sits between its bearings.")
            if not (min(ax) < c < max(ax)):
                k.bad("kin.bearing_straddle", WARNING, "Weapon is cantilevered beyond its bearings",
                      f"`{g.weapon}` centre is at {c:.1f} mm along the axis; bearings at {', '.join(f'{a:.1f}' for a in ax)} mm.",
                      (g.weapon, *g.bearings), fix="Put one bearing on each side of the weapon.")


def torque_path(k):
    k.check("kin.torque_path", "Every weapon is driven", "A motor rotor reaches every weapon group directly or through a belt.")
    k.check("kin.torque_friction", "Weapon drive is keyed", "Torque reaches the weapon through keys, pins, screws or flats.")
    for g in k.rgroups.values():
        g.driven = bool(g.rotors)
    changed = True
    while changed:
        changed = False
        for b, ps in k.belt_pulleys.items():
            gs = [k.rot(p) for p in ps if k.rot(p) is not None]
            if any(g.driven for g in gs):
                for g in gs:
                    if not g.driven:
                        g.driven = changed = True
    k.check("drive.coverage", "Every wheel is driven", "Each wheel reaches a motor through shafts, rigid hubs or belts on rotating pulleys.")
    k.check("kin.pulley_coaxial", "Pulleys are coaxial with their wheels", "Each pulley's axis matches its rotating group's axis.")
    for g in k.rgroups.values():
        for m in sorted(g.members):
            if k.kind(m) == "pulley" and g.axis is not None:
                ra = round_axis(k.body(m)) if k.body(m) is not None else None
                if ra is None:
                    k.skip("kin.pulley_coaxial", f"`{m}` is not round")
                    continue
                ang, dist = coax(g.axis[0], g.axis[1], ra[0], ra[1], 3.0)
                if ang > 1.0 or dist > 0.2:
                    k.bad("kin.pulley_coaxial", BLOCKER, "Pulley is off its wheel axis",
                          f"`{m}` is {dist:.2f} mm / {ang:.1f} deg off the axis of {label(g)} ({g.axis_src}).", (m,))
        if g.cls == "wheel" and not g.driven:
            dead = any(k.parts[m].part._extra.get("driven") is False for m in g.members)
            if dead:
                k.info("drive.coverage", "Dead wheel", f"{label(g)} is declared `driven: false`.", sorted(g.members))
            else:
                k.bad("drive.coverage", BLOCKER, "Wheel is not driven",
                      f"Wheel group {label(g)} reaches no motor: no motor rotor joined to it and no belt to a driven pulley.",
                      sorted(g.members), fix="Mount it on a motor shaft, or put a pulley in its rigid group belted to a driven pulley; "
                                             "set `driven: false` only for a deliberate dead wheel.")
        if g.cls == "weapon" and not g.driven:
            k.bad("kin.torque_path", BLOCKER, "Weapon is not driven",
                  f"No motor rotor is joined to {label(g)} (and no belt links it to one).", sorted(g.members),
                  fix="Join the weapon hub to the motor bell/shaft (screws, dowels, key) or add a belt to a driven pulley.")
        if g.cls != "weapon" or not g.rotors:
            continue
        best = None
        for m, how, o, q, e, rs in g.rotors:
            path_q = path_quality(k, o, g.weapon)
            qual = "key" if q == "key" and path_q == "key" else "friction"
            if best is None or qual == "key":
                best = (qual, m, o, how)
        if best and best[0] != "key":
            k.bad("kin.torque_friction", WARNING, "Weapon torque relies on friction",
                  f"Torque from `{best[1]}` reaches `{g.weapon}` only through friction joins (press fit / glue / tape) via `{best[2]}`; a hit slips it.",
                  (best[1], g.weapon), fix="Add a key, D-flat, grub screw, dowels or a bolted hub on the torque path.")


def path_quality(k, a, b):
    """'key' when a and b are joined by key-quality edges only, else 'friction'."""
    if a == b:
        return "key"
    seen = {a}
    q = [a]
    while q:
        x = q.pop()
        for y, _, qual in k.edges.get(x, []):
            if qual == "friction" or y in seen:
                continue
            if y == b:
                return "key"
            seen.add(y)
            q.append(y)
    return "friction"


def retention(k):
    k.check("kin.axial_retention", "Rotating parts are held axially both ways",
            "Every rotating group on bearings or an axle is located by a shoulder, clip, collar or nut both ways.")
    for g in k.rgroups.values():
        if g.axis is None or not (g.bearings or g.shaft_partners):
            continue
        texts = []
        for c in k.spec.connections:
            if c.a in g.members or c.b in g.members or c.a in g.bearings or c.b in g.bearings:
                texts.append((c.reason or "").lower())
        if any(k.parts[m].part.retained for m in g.members) or any(any(w in t for w in RETAIN_WORDS) for t in texts):
            continue
        cap = {}
        bodies = [k.body(m) for m in g.members if k.body(m) is not None]
        others = [b for b in k.w.bodies if not b.is_wire and b.id not in g.members and b.id not in g.fasteners]
        for s in (1.0, -1.0):
            shift = g.axis[1] * 0.8 * s
            cap[s] = any(measure.overlap_exceeds(b, o, 0.1, shift) for b in bodies for o in others
                         if measure.aabb_overlap(b.aabb + shift, o.aabb))
        if not (cap[1.0] and cap[-1.0]):
            sev = BLOCKER if g.cls == "weapon" else WARNING
            k.bad("kin.axial_retention", sev, "Rotating part can slide off its axis",
                  f"{label(g)} is free to move {'both ways' if not (cap[1.0] or cap[-1.0]) else 'one way'} along its axis: "
                  "no shoulder, clip, collar or nut is declared and nothing blocks a 0.8 mm slide.", sorted(g.members),
                  fix="Add e-clips/collars/shoulders each side (say so in the connection reason or set `retained`).")


def weapon_checks(k):
    spec = k.spec
    for g in k.rgroups.values():
        if not g.weapon:
            continue
        p = k.parts[g.weapon].part
        wd = p.weapon
        wb = k.body(g.weapon)
        k.check("kin.spin_axis_declared", "Weapon spin axis declared", "Every spinning weapon declares `weapon.spin_axis`.")
        k.check("kin.joint_axis_spin", "Joint matches the weapon spin axis",
                "The weapon joint axis equals `weapon.spin_axis` and runs through the weapon origin.")
        k.check("kin.weapon_axis_orientation", "Spin axis matches the robot type",
                "Vertical spinners/drums spin about a horizontal sideways axis; horizontal spinners about a vertical one.")
        if wd is None or wd.spin_axis is None:
            k.bad("kin.spin_axis_declared", WARNING, "Weapon spin axis not declared",
                  f"`{g.weapon}` has no `weapon.spin_axis`; local Z is assumed.", (g.weapon,))
        from .power import spin_axis
        sa = spin_axis(k.w, k.r, k.w.index(g.weapon))
        if sa is not None and g.joints:
            ang, dist = coax(g.axis[0], g.axis[1], sa[0], sa[1])
            if ang > COAX_DEG or dist > COAX_MM:
                k.bad("kin.joint_axis_spin", BLOCKER, "Joint axis is not the weapon spin axis",
                      f"`{g.weapon}` joint ({g.axis_src}) is {dist:.2f} mm / {ang:.2f} deg off its spin axis through its origin.",
                      (g.weapon,), at=sa[0], fix="Put the pivot on the disc centre and the axis along `spin_axis`.")
        a = g.axis[1] if g.axis is not None else None
        if a is not None:
            vert = spec.robot_type in ("vertical_spinner", "drum")
            horiz = spec.robot_type == "horizontal_spinner"
            if vert and (abs(a[2]) > 0.05 or abs(a[1]) > 0.1):
                k.bad("kin.weapon_axis_orientation", BLOCKER, "Vertical spinner axis is not horizontal and sideways",
                      f"`{g.weapon}` spins about {np.round(a, 3).tolist()}; a {spec.robot_type} needs +/-X.", (g.weapon,))
            if horiz and abs(a[2]) < 0.995:
                k.bad("kin.weapon_axis_orientation", BLOCKER, "Horizontal spinner axis is not vertical",
                      f"`{g.weapon}` spins about {np.round(a, 3).tolist()}.", (g.weapon,))
        # spin direction and teeth
        k.check("kin.spin_dir", "Weapon spins the right way", "Declared spin direction strikes upward at the front (vertical/drum).")
        k.check("kin.tooth_leading", "Teeth lead with their bite", "Each tooth's steep face leads in the declared spin direction.")
        sd = None if wd is None else wd.spin_dir
        s = {"ccw": 1.0, "+1": 1.0, "1": 1.0, "cw": -1.0, "-1": -1.0}.get(str(sd).lower().strip()) if sd is not None else None
        if s is None:
            k.bad("kin.spin_dir", WARNING, "Weapon spin direction not declared",
                  f"`{g.weapon}` has no `weapon.spin_dir` (cw/ccw about spin_axis); strike direction and tooth orientation are unchecked.",
                  (g.weapon,), fix="Add `weapon.spin_dir`: \"ccw\" (+, right-hand about spin_axis) or \"cw\".")
            k.skip("kin.spin_dir", f"`{g.weapon}` spin direction and tooth leading edge (no spin_dir)")
            continue
        if a is None:
            k.skip("kin.spin_dir", f"`{g.weapon}` has no axis")
            continue
        o = g.axis[0]
        a_s = a * s  # rotation vector direction
        V = wb.mesh.vertices
        front = V[np.argmax(V[:, 1])]
        v = np.cross(a_s, front - o)
        if spec.robot_type in ("vertical_spinner", "drum") and v[2] < 0:
            k.bad("kin.spin_dir", WARNING, "Weapon strikes downward at the front",
                  f"Spinning {sd} about {np.round(a, 3).tolist()}, the front of `{g.weapon}` moves down ({v[2]:.2f}); vertical spinners uppercut.",
                  (g.weapon,), at=front, fix="Reverse `spin_dir` (and the motor wiring) or flip the teeth.")
        tooth_check(k, g, wb, o, a, s)


def tooth_check(k, g, wb, o, a, s):
    P = np.vstack([wb.surface(0.5)[0], wb.mesh.vertices])
    ax, rad = radial(P, o, a)
    u, v = basis(a)
    q = P - o
    th = np.degrees(np.arctan2(q @ v, q @ u)) % 360
    nb = 120  # 3 degree bins
    r = np.full(nb, 0.0)
    np.maximum.at(r, (th / 3).astype(int) % nb, rad)
    for i in np.nonzero(r == 0)[0]:
        r[i] = max(r[(i - 1) % nb], r[(i + 1) % nb])
    med = float(np.median(r))
    if r.max() - med < 1.0:
        return  # round disc, no teeth
    peaks = [i for i in range(nb) if r[i] >= r[(i - 1) % nb] and r[i] > r[(i + 1) % nb] and r[i] > med + 0.6 * (r.max() - med)]
    backwards = 0
    for i in peaks:
        half = r[i] - 0.5 * (r[i] - med)

        def run_(step):
            for n in range(1, nb // 2):
                if r[(i + step * n) % nb] < half:
                    return n
            return nb // 2
        lead, trail = run_(1 if s > 0 else -1), run_(-1 if s > 0 else 1)
        if lead > trail * 1.5 and lead - trail >= 2:
            backwards += 1
    if peaks and backwards > len(peaks) / 2:
        k.bad("kin.tooth_leading", WARNING, "Teeth face backwards",
              f"{backwards} of {len(peaks)} teeth of `{g.weapon}` lead with the ramp, not the steep face, for the declared spin direction.",
              (g.weapon,), fix="Mirror the tooth profile or reverse `spin_dir`.")


def mass_of(k, pid):
    m = k.ctx.metrics.get(f"part_mass_g.{pid}")
    b = k.body(pid)
    if m is None and b is not None:
        m = b.geom.volume * PLASTIC_G_MM3
    return m


def balance(k):
    k.check("kin.balance_static", "Rotating groups are balanced", "Mass centres sit on the spin axis.")
    k.check("kin.balance_dynamic", "Weapon spins about a principal axis", "The weapon's principal axis matches its spin axis.")
    k.check("kin.spin_stability", "Weapon spins about its major axis", "Disc/bar weapons have their largest inertia about the spin axis.")
    k.check("kin.fastener_imbalance", "Screws on the weapon are balanced", "Screws carried by the weapon form a balanced pattern.")
    rpm = k.ctx.metrics.get("weapon_rpm")
    for g in k.rgroups.values():
        if g.axis is None:
            k.skip("kin.balance_static", f"{label(g)}: no axis")
            continue
        o, a = g.axis
        items = []
        for m in g.members:
            b = k.body(m)
            if b is None:
                continue
            mg = mass_of(k, m)
            R = b.M[:3, :3]
            com = xform.apply(b.M, b.geom.centroid)
            I = R @ b.geom.inertia @ R.T * (mg / max(b.geom.volume, 1e-9))
            items.append((mg, com, I))
        fitems = []
        for fid in g.fasteners:
            fb = k.body(fid)
            if fb is None:
                continue
            mg = fb.geom.volume * STEEL_G_MM3
            fitems.append((mg, fb.mesh.center_mass, np.zeros((3, 3))))
        allit = items + fitems
        M = sum(x[0] for x in allit)
        if M <= 0:
            continue
        com = sum(x[0] * x[1] for x in allit) / M
        e = line_dist(o, a, com)
        k.ctx.metrics[f"kin_unbalance_mm.{g.weapon or sorted(g.members)[0]}"] = e
        lim_w, lim_b = (0.05, 0.5) if g.cls == "weapon" else (0.5, 3.0)
        if e > lim_w:
            force = ""
            if rpm and g.cls == "weapon":
                force = f" = {M / 1000 * e / 1000 * (rpm * 2 * math.pi / 60) ** 2:.0f} N at {rpm:.0f} rpm"
            k.bad("kin.balance_static", BLOCKER if e > lim_b else WARNING, "Rotating group is out of balance",
                  f"The mass centre of {label(g)} ({M:.1f} g) is {e:.2f} mm off the spin axis{force}; allowed {lim_w} mm.",
                  sorted(g.members), at=com, expect=(f"<= {lim_w} mm", f"{e:.2f} mm"),
                  fix="Make the weapon symmetric about the axis (matching teeth/counterweight, symmetric holes and screws).")
        if fitems and g.cls == "weapon":
            fm = sum(x[0] for x in fitems)
            vec = sum(x[0] * ((x[1] - o) - ((x[1] - o) @ a) * a) for x in fitems)
            ef = float(np.linalg.norm(vec)) / M
            if ef > 0.05:
                k.bad("kin.fastener_imbalance", WARNING, "Screws on the weapon are not balanced",
                      f"The {len(fitems)} screws ({fm:.1f} g) carried by {label(g)} shift its mass centre {ef:.2f} mm off axis.",
                      g.fasteners, fix="Use an evenly spaced bolt circle (2, 3 or 4 screws at equal angles and radius).")
        if g.cls == "weapon":
            Ic = np.zeros((3, 3))
            for mg, c, I in items:
                d = c - com
                Ic += I + mg * (np.dot(d, d) * np.eye(3) - np.outer(d, d))
            vals, vecs = np.linalg.eigh(Ic)
            j = int(np.argmax(np.abs(vecs.T @ a)))
            tilt = math.degrees(math.acos(min(1.0, abs(float(vecs[:, j] @ a)))))
            k.ctx.metrics["kin_weapon_principal_tilt_deg"] = tilt
            if tilt > 0.5:
                k.bad("kin.balance_dynamic", WARNING, "Weapon wobbles (dynamic imbalance)",
                      f"`{g.weapon}` principal axis is {tilt:.2f} deg from its spin axis; it will shake the bearings at speed.",
                      (g.weapon,), fix="Make the weapon mirror-symmetric about its mid-plane.")
            wd = k.parts[g.weapon].part.weapon
            if wd is not None and wd.kind in ("disc", "bar", "spinner", "shell") and j != int(np.argmax(vals)) and vals[j] < 0.98 * vals.max():
                k.bad("kin.spin_stability", WARNING, "Weapon spins about a minor axis",
                      f"`{g.weapon}` inertia about the spin axis ({vals[j]:.0f}) is below its largest ({vals.max():.0f}); a flexing disc/bar goes unstable.",
                      (g.weapon,))


def static_exclusions(k, g):
    ex = set(g.members) | set(g.fasteners) | set(g.bearings) | set(g.shaft_partners) | k.axle_fasteners
    ex |= {m for m, *_ in g.rotors}
    for b, ps in k.belt_pulleys.items():
        if any(p in g.members for p in ps):
            ex.add(b)
    if g.weapon:
        wd = k.parts[g.weapon].part.weapon
        if wd is not None and wd.locking_bar:
            ex.add(wd.locking_bar)
    if g.axis is not None:
        for b in k.w.bodies:
            if b.part_idx is not None and k.kind(b.id) in ("shaft", "pin") and b.id not in ex:
                ra = round_axis(b)
                if ra is not None:
                    ang, dist = coax(g.axis[0], g.axis[1], ra[0], ra[1], 2.0)
                    if ang < AXLE_DEG and dist < AXLE_MM:
                        ex.add(b.id)
    return ex


def sweeps(k):
    k.check("kin.sweep_static", "Nothing static is in a swept volume", "No static part lies inside the volume a rotating group sweeps.")
    k.check("kin.sweep_fastener", "No screw head or nut in a swept volume", "No static screw protrudes into a rotating group's sweep.")
    k.check("kin.rub_gap", "Rotating parts clear the structure",
            f"Every rotating group clears static parts by its class gap ({', '.join(f'{c} {v} mm' for c, v in RUB_GAP.items())}).")
    k.check("kin.outrunner_bell_rub", "Outrunner bells run clear", "Nothing static touches a spinning outrunner bell.")
    k.check("kin.lock_engages", "Locking bar stops the weapon", "The declared locking bar enters the weapon's swept volume.")
    for g in k.rgroups.values():
        if g.axis is None:
            k.skip("kin.sweep_static", f"{label(g)}: no rotation axis, sweep not built")
            k.bad("kin.sweep_static", WARNING, "Swept volume unknown", f"{label(g)} has no axis; its sweep was not checked.", sorted(g.members))
            continue
        bodies = [k.body(m) for m in list(g.members) + g.fasteners if k.body(m) is not None]
        P = np.vstack([b.surface(k.h)[0] for b in bodies])
        sw = Sweep(P, g.axis[0], g.axis[1])
        gapmin = RUB_GAP[g.cls]
        ex = static_exclusions(k, g)
        box = sw.aabb()
        worst = {}
        for b in k.w.bodies:
            if b.id in ex or b.is_wire:
                continue
            if b.part_idx is not None and k.rot(b.id) is not None:
                continue
            if not measure.aabb_overlap(box, b.aabb, gapmin + 0.1):
                continue
            Q = b.surface(0.5 if not k.r.fast else 1.0)[0]
            sel = np.all((Q >= box[0] - gapmin - 0.1) & (Q <= box[1] + gapmin + 0.1), axis=1)
            Q = Q[sel]
            if not len(Q):
                continue
            depth, gap = sw.classify(Q, gapmin + 0.1)
            i = int(np.argmax(depth))
            if depth[i] > 0.2:
                worst[b.id] = ("in", float(depth[i]), Q[i], b.fastener)
            else:
                j = int(np.argmin(gap))
                if gap[j] < gapmin - 0.01:
                    worst[b.id] = ("near", float(gap[j]), Q[j], b.fastener)
        k.check("kin.sweep_rotating", "Rotating groups clear each other", "No rotating group reaches into another's swept volume.")
        for h in k.rgroups.values():
            if h is g or h.gid in k._pairs_done.get(g.gid, set()):
                continue
            k._pairs_done.setdefault(h.gid, set()).add(g.gid)
            for m in sorted(set(h.members) | set(h.fasteners)):
                b = k.body(m)
                if b is None or m in ex or not measure.aabb_overlap(box, b.aabb, 0.4):
                    continue
                Q = b.surface(0.5 if not k.r.fast else 1.0)[0]
                depth, gap = sw.classify(Q, 0.4)
                i = int(np.argmax(depth))
                if depth[i] > 0.2:
                    k.bad("kin.sweep_rotating", BLOCKER, "Two rotating groups collide",
                          f"`{m}` (turning with {label(h)}) reaches {depth[i]:.1f} mm into the volume {label(g)} sweeps.",
                          (m, *sorted(g.members)), at=Q[i], fix="Separate them axially or radially (0.3 mm or more).")
                    break
                j = int(np.argmin(gap))
                if gap[j] < 0.3:
                    k.bad("kin.sweep_rotating", WARNING, "Two rotating groups run very close",
                          f"`{m}` (turning with {label(h)}) passes {gap[j]:.2f} mm from the volume {label(g)} sweeps (need 0.3 mm).",
                          (m, *sorted(g.members)), at=Q[j])
                    break
        for bid, (what, val, at, isf) in sorted(worst.items()):
            if what == "in":
                cid = "kin.sweep_fastener" if isf else "kin.sweep_static"
                k.bad(cid, BLOCKER, "Static part inside a swept volume" if not isf else "Screw head/nut inside a swept volume",
                      f"`{bid}` reaches {val:.1f} mm into the volume {label(g)} sweeps as it turns about {g.axis_src}; it hits on the first turn.",
                      (bid, *sorted(g.members)), at=at,
                      fix="Move or shorten it, or cut a clearance so it stays outside the swept circle with "
                          f"{gapmin} mm to spare.")
            else:
                k.bad("kin.rub_gap", WARNING if g.cls != "weapon" else BLOCKER, "Rotating part runs too close to a static one",
                      f"{label(g)} passes {val:.2f} mm from `{bid}` (need {gapmin} mm for a {g.cls}).", (bid, *sorted(g.members)), at=at,
                      expect=(f">= {gapmin} mm", f"{val:.2f} mm"), fix="Open the clearance (flex and runout eat small gaps).")
        if g.weapon:
            wd = k.parts[g.weapon].part.weapon
            lb = wd.locking_bar if wd is not None else None
            if lb:
                bb = k.body(lb)
                if bb is None:
                    k.bad("kin.lock_engages", WARNING, "Locking bar missing", f"`{lb}` is not a part.", (g.weapon,))
                else:
                    d, _ = sw.classify(bb.surface(0.5)[0], 0.1)
                    if d.max() <= 0.2:
                        k.bad("kin.lock_engages", WARNING, "Locking bar does not block the weapon",
                              f"`{lb}` never enters the volume `{g.weapon}` sweeps; it cannot stop it turning.", (lb, g.weapon),
                              fix="Run the pin through a hole in the disc (inside its swept ring) in the locked pose.")
        bell_rub(k, g, ex)


def bell_rub(k, g, ex):
    for m in {m for m, *_ in g.rotors}:
        mi = k.motor_info(m)
        if mi is None or not mi["outrunner"]:
            continue
        mb = k.body(m)
        Minv = xform.inv(mb.M)
        stator_fast = {how.split("`")[1] for mm, o, how in k.stator_links if mm == m and how.startswith("screw")}
        for b in k.w.bodies:
            if b is mb or b.is_wire or b.id in g.members or b.id in g.fasteners or b.id in stator_fast:
                continue
            if b.part_idx is not None and (k.rot(b.id) is not None or k.kind(b.id) in ("bearing",)):
                continue
            if not measure.aabb_overlap(mb.aabb, b.aabb, 0.6):
                continue
            Q = xform.apply(Minv, b.surface(0.5)[0])
            x = Q @ mi["local_dir"]
            rr = np.linalg.norm(Q - np.outer(x, mi["local_dir"]), axis=1)
            zone = (x > mi["back"] + 2.0) & (x < mi["can_end"] - 0.2)
            near = zone & (rr < mi["R"] + 0.5)
            if near.any():
                inside = zone & (rr < mi["R"] - 0.2)
                sev = BLOCKER if inside.any() else WARNING
                k.bad("kin.outrunner_bell_rub", sev, "Static part touches the spinning bell",
                      f"`{b.id}` is {'inside' if inside.any() else 'within 0.5 mm of'} the rotating bell of `{m}` "
                      f"({float((mi['R'] - rr[near]).max()):.2f} mm into its radius).", (b.id, m),
                      at=xform.apply(mb.M, Q[np.nonzero(near)[0][0]]),
                      fix="Only the stator face (back 2 mm) may touch structure; open a 0.5 mm gap around the bell.")


def wheels(k):
    wg = [g for g in k.rgroups.values() if g.cls == "wheel"]
    if not wg:
        return
    for cid, t, m in (("kin.wheel_axes_parallel", "Wheel axles are parallel", "All wheel axes within 0.5 deg."),
                      ("kin.wheel_camber", "Wheels stand upright", "Wheel axes are horizontal within 1 deg."),
                      ("kin.wheel_toe", "Wheels point forward", "Wheel axes are square to the direction of travel within 1 deg."),
                      ("kin.wheel_track", "Wheels on a side track together", "Same-side wheel mid-planes within 1 mm."),
                      ("kin.wheel_height", "Wheels reach the same floor", "Lowest wheel points within 0.5 mm."),
                      ("kin.wheel_motor_coaxial", "Wheels sit on their motor shafts", "Wheel axes on the motor shaft within 0.2 mm / 1 deg."),
                      ("kin.shaft_engagement", "Hubs grip enough shaft", "Each driven hub covers at least 3 mm of motor shaft.")):
        k.check(cid, t, m)
    info = []
    for g in wg:
        if g.axis is None:
            k.skip("kin.wheel_axes_parallel", f"{label(g)} has no axis")
            continue
        wheel = sorted(m for m in g.members if k.kind(m) == "wheel") or sorted(g.members)
        b = k.body(wheel[0])
        info.append((g, wheel[0], b.center, g.axis[1], b.aabb[0][2]))
        a = g.axis[1]
        if abs(a[2]) > math.sin(math.radians(1)):
            k.bad("kin.wheel_camber", WARNING, "Wheel axle is tilted", f"`{wheel[0]}` axis tilts {math.degrees(math.asin(min(1, abs(a[2])))):.1f} deg from horizontal.", (wheel[0],))
        if abs(a[1]) > math.sin(math.radians(1)):
            k.bad("kin.wheel_toe", WARNING, "Wheel is toed in/out", f"`{wheel[0]}` axis is {math.degrees(math.asin(min(1, abs(a[1])))):.1f} deg off square to the direction of travel; it scrubs.", (wheel[0],))
        for m, how, o, q, e, rs in g.rotors:
            mi = k.motor_info(m)
            if mi is None or k.parts[m].part.kind != "motor":
                continue
            ra = round_axis(b)
            if ra is not None:
                ang, dist = coax(mi["o"], mi["d"], ra[0], ra[1], 3.0)
                if ang > 1.0 or dist > 0.2:
                    k.bad("kin.wheel_motor_coaxial", BLOCKER, "Wheel is off its motor shaft",
                          f"`{wheel[0]}` axis is {dist:.2f} mm / {ang:.1f} deg off the shaft of `{m}`; it wobbles or does not fit.", (wheel[0], m))
            ts = np.arange(0.0, mi["len"] + 1e-9, 0.25)
            P = mi["o"] + np.outer(ts, mi["d"])
            gb = [k.body(x) for x in g.members if k.body(x) is not None]
            u, v = basis(mi["d"])
            rr = mi["dia"] / 2 + 0.3
            ring = [P] + [P + rr * (math.cos(t) * u + math.sin(t) * v) for t in np.linspace(0, 2 * math.pi, 6, endpoint=False)]
            ins = np.array([measure.inside_any(gb, R) for R in ring])
            cov = float(((ins[0]) | (ins[1:].sum(axis=0) >= 3)).sum() * 0.25)
            if cov < min(3.0, 0.6 * mi["len"]):
                k.bad("kin.shaft_engagement", BLOCKER if cov < 0.5 else WARNING, "Hub barely grips the motor shaft",
                      f"Only {cov:.1f} mm of the {mi['len']:.0f} mm shaft of `{m}` is inside {label(g)}.", (m, wheel[0]),
                      expect=(">= 3 mm", f"{cov:.1f} mm"), fix="Move the hub onto the shaft (bore along the full flat).")
    for i in range(len(info)):
        for j in range(i + 1, len(info)):
            gi, wi, ci, ai, zi = info[i]
            gj, wj, cj, aj, zj = info[j]
            ang = math.degrees(math.acos(min(1.0, abs(float(ai @ aj)))))
            if ang > 0.5:
                k.bad("kin.wheel_axes_parallel", BLOCKER if ang > 3 else WARNING, "Wheel axles are not parallel",
                      f"`{wi}` and `{wj}` axes differ by {ang:.1f} deg; the robot scrubs and pulls.", (wi, wj))
            if abs(zi - zj) > 0.5:
                k.bad("kin.wheel_height", WARNING, "Wheels do not reach the same floor",
                      f"`{wi}` bottom is {zi - zj:+.1f} mm from `{wj}`; one wheel lifts.", (wi, wj))
            if np.sign(ci[0]) == np.sign(cj[0]) and abs(ci[0]) > 1:
                d = abs(float((ci - cj) @ ai))
                if d > 1.0:
                    k.bad("kin.wheel_track", WARNING, "Same-side wheels do not track",
                          f"`{wi}` and `{wj}` mid-planes are {d:.1f} mm apart along the axle.", (wi, wj))


def belts(k):
    if not k.belt_pulleys:
        return
    k.check("kin.belt_pulleys_joint", "Belt pulleys rotate", "Both pulleys of every belt are on rotating groups.")
    k.check("kin.belt_axes_parallel", "Belt pulley axes are parallel", "Pulley axes within 0.5 deg.")
    k.check("kin.belt_coplanar", "Belt grooves line up", "Pulley mid-planes within 0.5 mm.")
    k.check("kin.belt_same_group", "Belts link different shafts", "A belt's pulleys are on different rotating groups.")
    for b, ps in k.belt_pulleys.items():
        if len(ps) < 2:
            k.skip("kin.belt_pulleys_joint", f"belt `{b}` lists fewer than two pulleys")
            k.bad("kin.belt_pulleys_joint", WARNING, "Belt pulleys not listed", f"`{b}` lists {ps}.", (b,))
            continue
        gs = []
        for p in ps:
            g = k.rot(p)
            if g is None:
                k.bad("kin.belt_pulleys_joint", BLOCKER, "Belt pulley does not rotate",
                      f"`{p}` (on belt `{b}`) is not on any joint, motor or axle, or is rigidly tied to the structure.", (b, p))
            gs.append(g)
        if all(gs) and len({g.gid for g in gs}) < len(gs):
            k.bad("kin.belt_same_group", WARNING, "Belt joins pulleys that already turn together",
                  f"`{b}` pulleys {ps} are rigidly joined; the belt transmits nothing.", (b, *ps))
        info = []
        for p, g in zip(ps, gs):
            pb = k.body(p)
            if pb is None:
                continue
            ra = round_axis(pb)
            ax = g.axis if g is not None and g.axis is not None else ra
            if ax is None:
                k.skip("kin.belt_axes_parallel", f"pulley `{p}` axis unknown")
                continue
            c = ra[0] if ra is not None else pb.center
            info.append((p, c, ax[1]))
        for i in range(1, len(info)):
            p0, c0, a0 = info[0]
            p1, c1, a1 = info[i]
            ang = math.degrees(math.acos(min(1.0, abs(float(a0 @ a1)))))
            if ang > 0.5:
                k.bad("kin.belt_axes_parallel", BLOCKER if ang > 2 else WARNING, "Belt pulleys are not parallel",
                      f"`{p0}` and `{p1}` axes differ by {ang:.1f} deg; the belt walks off.", (b, p0, p1))
            off = abs(float((c1 - c0) @ a0))
            if off > 0.5:
                k.bad("kin.belt_coplanar", BLOCKER if off > 1.5 else WARNING, "Belt grooves do not line up",
                      f"`{p0}` and `{p1}` grooves are {off:.2f} mm apart along the axle; the belt runs crooked and jumps off.",
                      (b, p0, p1), expect=("<= 0.5 mm", f"{off:.2f} mm"))


def tyres(k):
    cands = []
    for pid, rp in k.parts.items():
        p = rp.part
        hub = p.tyre_of if isinstance(p.tyre_of, str) else None
        if p.kind == "tyre" or hub:
            cands.append((pid, hub))
        elif p.kind == "wheel":
            hubs = [o for o, _, _ in k.edges.get(pid, []) if k.kind(o) in ("wheel_hub", "hub")]
            if hubs:
                cands.append((pid, hubs[0]))
    if not cands:
        return
    k.check("kin.tyre_retained", "Tyres are held on their hubs", "Every tyre is joined to its hub and sits on the rim.")
    for t, hub in cands:
        tb = k.body(t)
        if hub is None or hub not in k.parts:
            k.bad("kin.tyre_retained", BLOCKER, "Tyre has no hub", f"`{t}` names no hub (`tyre_of`).", (t,))
            continue
        if k.group_of(t) != k.group_of(hub):
            k.bad("kin.tyre_retained", BLOCKER, "Tyre is not joined to its hub",
                  f"`{t}` is not glued, pressed or fused to `{hub}`; it spins on the rim or walks off.", (t, hub),
                  fix=f"Add a press_fit/glue connection `{t}`-`{hub}` or `tyre_of`/`fused_with`.")
            continue
        hb = k.body(hub)
        if tb is not None and hb is not None:
            gap = measure.min_gap(tb, hb, 2.0)
            if gap > 0.1:
                k.bad("kin.tyre_retained", BLOCKER, "Tyre does not touch its hub",
                      f"`{t}` is {('>2' if not np.isfinite(gap) else f'{gap:.2f}')} mm from `{hub}`; it would be loose.", (t, hub),
                      fix="Make the tyre bore 0.2-0.5 mm smaller than the rim.")


def wires(k):
    k.check("kin.wire_to_rotor", "No wire ends on a rotating part", "Every wire ends on static parts or motor terminals.")
    for wr in k.spec.wires:
        for end in (getattr(wr, "from", None), wr.to):
            if not end:
                continue
            pid = str(end).split(".", 1)[0]
            g = k.rot(pid)
            if g is not None:
                k.bad("kin.wire_to_rotor", BLOCKER, "Wire ends on a rotating part",
                      f"Wire `{wr.id}` ends on `{end}`, which turns with {label(g)}; it wraps and tears on the first turn.",
                      (wr.id, pid), fix="Move the device to the static structure or use a slip ring.")


def bore_fit(k):
    k.check("kin.bore_fit", "Bores fit their shafts", "Parts on a shaft have bores within 0.15 mm of the shaft (press/key fit) or run on bearings.")
    for g in k.rgroups.values():
        for sid in sorted(g.members):
            if k.kind(sid) not in ("shaft", "pin"):
                continue
            sb = k.body(sid)
            ra = round_axis(sb)
            if ra is None:
                k.skip("kin.bore_fit", f"`{sid}` is not round")
                continue
            o, a = ra
            ax, rad = radial(sb.surface(0.3)[0], o, a)
            rs = float(np.median(rad[np.abs(ax) < 0.4 * (ax.max() - ax.min())]))
            for m in sorted(g.members):
                if m == sid or k.kind(m) in ("shaft", "pin"):
                    continue
                b = k.body(m)
                if b is None or not measure.aabb_overlap(sb.aabb, b.aabb):
                    continue
                Q = b.surface(0.3)[0]
                qa, qr = radial(Q, o, a)
                sel = (qa > ax.min()) & (qa < ax.max()) & (qr < rs + 1.5)
                if sel.sum() < 8:
                    continue
                bore = float(np.percentile(qr[sel], 5))
                if bore > rs + 0.15:
                    k.bad("kin.bore_fit", WARNING, "Part is loose on its shaft",
                          f"`{m}` bore radius {bore:.2f} mm on `{sid}` radius {rs:.2f} mm ({bore - rs:.2f} mm radial play); it rattles and fretts.",
                          (m, sid), expect=("<= 0.15 mm play", f"{bore - rs:.2f} mm"), fix="Size the bore to the shaft (ream, or 0-0.05 mm press fit).")
