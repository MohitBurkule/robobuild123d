"""Things that end real antweight fights besides big hits:

- debris: a broken-off chunk collides with its own robot too (after it has moved clear of its old seat) and can wedge
  into a wheel or the weapon; a driven hinge that is commanded but stalled while touching debris is logged as a jam;
- tyre damage: an opponent's weapon hitting a tyre hard cuts it; grip falls with damage, a destroyed tyre barely grips;
- power switch: a hit landing on or next to the switch knocks it off: the robot is dead (all motors cut);
- wires: a hit landing on a wire's route (now exposed, because something hard got there) cuts it; what that wire feeds dies
  (battery/switch/ESC power line = whole robot, a drive motor's lead = that side, the weapon lead = weapon);
- driver: commands reach the robot after a reaction delay (default 150 ms) with a little steering noise.
Thresholds are spec-overridable (`sim.hazards`), defaults below; they are hand values, like the weld limits.
"""

from __future__ import annotations

from collections import deque

import mujoco
import numpy as np

DEFAULTS = {"tyre_cut_N": 250.0, "tyre_destroy": 1.0, "switch_N": 60.0, "switch_mm": 8.0, "wire_N": 200.0,
            "wire_mm": 6.0, "debris_clear_mm": 5.0, "jam_s": 0.3, "reaction_s": 0.15, "steer_noise": 0.03}
POWER_KINDS = ("battery", "switch", "esc", "receiver", "bec")
DEBRIS_BIT = 1 << 15


def params(prof):
    h = dict((prof.raw or {}).get("hazards") or {})
    return {k: float(h.get(k, v)) for k, v in DEFAULTS.items()}


class Hazards:
    def __init__(self, sim, specs: dict, seed=0):
        """specs: robot name -> Spec (wires, switch part, part kinds)."""
        self.sim = sim
        self.rng = np.random.default_rng(seed)
        m = sim.m
        self.p = {r: params(sim.profiles[r]) for r in sim.robots}
        # geom id -> (robot, group, part)
        self.owner = {}
        for r, model in sim.robots.items():
            pre = r + "/"
            for g in model.groups:
                for p in g.parts:
                    for gi in range(m.ngeom):
                        nm = m.geom(gi).name
                        if nm.startswith(pre + p.id + "_g") or nm.startswith(pre + p.id + "_s") or nm.startswith(pre + p.id + "_c"):
                            self.owner[gi] = (r, g.name, p.id)
        self.kind = {r: {p.id: p.kind for g in sim.robots[r].groups for p in g.parts} for r in sim.robots}
        self.com = {r: {p.id: p.com for g in sim.robots[r].groups for p in g.parts} for r in sim.robots}
        self.switch = {r: [pid for pid, k in self.kind[r].items() if k == "switch"] for r in sim.robots}
        self.wires = {r: self._wires(r, specs.get(r)) for r in sim.robots}
        self.tyre = {}  # (robot, wheel group) -> damage 0..1+
        self.dead = {r: None for r in sim.robots}
        self.cut = {r: set() for r in sim.robots}
        self.stall_t = {}
        self.debris_live = set()
        self.queue = {r: deque() for r in sim.robots}
        self.mu0 = m.geom_friction[:, 0].copy()
        self.bounds = {r: sim.robots[r].bounds() for r in sim.robots}
        sim.reaction_s = {r: self.p[r]["reaction_s"] for r in sim.robots}

    # ---- wires -----------------------------------------------------------
    def _wires(self, r, spec):
        out = []
        if spec is None:
            return out
        for w in spec.raw.get("wires") or []:
            a = str(w.get("from", "")).split(".")[0]
            b = str(w.get("to", "")).split(".")[0]
            ca, cb = self.com[r].get(a), self.com[r].get(b)
            if ca is None or cb is None:
                continue
            pts = [ca] + [np.asarray(v, float) * 1e-3 for v in (w.get("via") or [])] + [cb]
            out.append({"id": w.get("id"), "ends": (a, b), "pts": np.asarray(pts)})
        return out

    def _wire_effect(self, r, w):
        kinds = [self.kind[r].get(e, "") for e in w["ends"]]
        if any(k in POWER_KINDS for k in kinds) and not any(k in ("motor", "weapon_motor", "servo") for k in kinds):
            return "all"
        if any(k == "weapon_motor" for k in kinds) or any("weapon" in e or e.startswith("w") and "esc" in e for e in w["ends"]):
            return "weapon"
        for e, k in zip(w["ends"], kinds):
            if k == "motor":
                return "side:" + ("l" if self.com[r][e][0] < 0 else "r")
            if k == "servo":
                return "lifter"
        return None

    # ---- per step ----------------------------------------------------------
    def setup_collision_bits(self):
        """Own-robot geoms never collide; robots collide with the world, each other and debris (contype/conaffinity)."""
        m = self.sim.m
        bits = {r: 1 << (i + 1) for i, r in enumerate(self.sim.robots)}
        for gi in range(m.ngeom):
            o = self.owner.get(gi)
            if o is None:
                m.geom_contype[gi], m.geom_conaffinity[gi] = 1, 0xFFFF
            else:
                b = bits[o[0]]
                m.geom_contype[gi], m.geom_conaffinity[gi] = b, 0xFFFF & ~b
        for w in self.sim.welds:  # a breakable part collides through its rigid copy until it comes off
            for gi in (w.copies if w.broken_at is not None else w.ghosts):
                m.geom_contype[gi] = m.geom_conaffinity[gi] = 0
            for gi in (w.ghosts if w.broken_at is not None else w.copies):
                b = bits[w.robot]
                m.geom_contype[gi], m.geom_conaffinity[gi] = b, 0xFFFF & ~b

    def tick(self, t, dt):
        sim, m, d = self.sim, self.sim.m, self.sim.d
        # debris: once a broken part has moved clear of its seat, it collides with its own robot too
        for w in sim.welds:
            if w.broken_at is None or (w.robot, w.part) in self.debris_live:
                continue
            bid = m.body(f"{w.robot}/{w.part}").id
            cb = m.body(f"{w.robot}/chassis").id
            rel = d.xmat[cb].reshape(3, 3).T @ (d.xipos[bid] - d.xpos[cb])
            # only once it has left its own robot's envelope: switching collisions on while it still overlaps its old
            # pocket would fire it out with a huge contact force (and blow up the solver)
            lo, hi = self.bounds[w.robot]
            if np.all((rel > lo - 0.002) & (rel < hi + 0.002)):
                continue
            for gi, o in self.owner.items():
                if gi in w.ghosts:
                    m.geom_contype[gi], m.geom_conaffinity[gi] = DEBRIS_BIT, 0xFFFF
            self.debris_live.add((w.robot, w.part))
        # a gram-scale chip pinched between a 1500 rad/s disc and the chassis can get a non-physical kick in one 0.1 ms
        # step (the solver's stiffness, not the impact); cap free debris at speeds no real chunk reaches (100 m/s)
        for w in sim.welds:
            if w.broken_at is None:
                continue
            j = m.joint(f"{w.robot}/{w.part}_free")
            a = j.dofadr[0]
            v = d.qvel[a:a + 3]
            om = d.qvel[a + 3:a + 6]
            sv, so = float(np.linalg.norm(v)), float(np.linalg.norm(om))
            if sv > 100.0:
                d.qvel[a:a + 3] = v * (100.0 / sv)
            if so > 5000.0:
                d.qvel[a + 3:a + 6] = om * (5000.0 / so)
        f6 = np.zeros(6)
        debris_touch = set()
        for i in range(d.ncon):
            c = d.contact[i]
            oa, ob = self.owner.get(c.geom1), self.owner.get(c.geom2)
            if oa is None and ob is None:
                continue
            mujoco.mj_contactForce(m, d, i, f6)
            fn = abs(f6[0])
            for me, other, gi in ((oa, ob, c.geom1), (ob, oa, c.geom2)):
                if me is None:
                    continue
                r = me[0]
                if other is not None and (other[0], other[1]) in self.debris_live:
                    debris_touch.add((r, me[1]))
                hit_by_opponent = other is not None and other[0] != r and (other[0], other[1]) not in self.debris_live
                if not hit_by_opponent:
                    continue
                pr = self.p[r]
                kind = self.kind[r].get(me[2], "")
                okind = self.kind[other[0]].get(other[2], "")
                weapon_hit = other[1] == "weapon" or okind == "weapon"
                if kind in ("wheel", "tyre") and weapon_hit and fn > pr["tyre_cut_N"]:
                    key = (r, me[1])
                    self.tyre[key] = self.tyre.get(key, 0.0) + fn / 1000.0
                    self._set_grip(r, me[1])
                    sim.events.append((t, "tyre", r, me[1], round(self.tyre[key], 2)))
                pos = self._local(r, c.pos)
                if self.dead[r] is None and fn > pr["switch_N"]:
                    for sw in self.switch[r]:
                        if np.linalg.norm(pos - self.com[r][sw]) < pr["switch_mm"] * 1e-3 + 0.006:
                            self._kill(r, t, f"switch {sw} knocked off ({fn:.0f} N)")
                if fn > pr["wire_N"]:
                    for w in self.wires[r]:
                        if w["id"] in self.cut[r]:
                            continue
                        if _seg_dist(pos, w["pts"]) < pr["wire_mm"] * 1e-3:
                            self.cut[r].add(w["id"])
                            eff = self._wire_effect(r, w)
                            sim.events.append((t, "wire_cut", r, w["id"], eff))
                            self._apply_wire(r, eff, t)
        # jams: commanded but stalled while debris touches it
        for r, pl in sim.plant.items():
            for gname, mot in pl["motors"].items():
                j = m.joint(f"{r}/{gname}_hinge")
                om = abs(float(d.qvel[j.dofadr[0]]))
                w0 = 8.4 / mot.ke
                stalled = abs(pl["duty"][gname]) > 0.3 and om < 0.05 * w0 and (r, gname) in debris_touch
                k = (r, gname)
                if stalled:
                    self.stall_t[k] = self.stall_t.get(k, 0.0) + dt
                    if self.stall_t[k] >= self.p[r]["jam_s"] and self.stall_t[k] - dt < self.p[r]["jam_s"]:
                        sim.events.append((t, "jam", r, gname, round(om, 1)))
                else:
                    self.stall_t[k] = 0.0
        # dead robots: every motor off, lifter limp
        for r, why in self.dead.items():
            if why is not None and r in sim.plant:
                for gname in sim.plant[r]["duty"]:
                    sim.plant[r]["duty"][gname] = 0.0

    def _local(self, r, p):
        cb = self.sim.m.body(f"{r}/chassis").id
        return self.sim.d.xmat[cb].reshape(3, 3).T @ (np.asarray(p) - self.sim.d.xpos[cb])

    def _set_grip(self, r, wheel):
        dmg = self.tyre[(r, wheel)]
        scale = 0.2 if dmg >= self.p[r]["tyre_destroy"] else max(0.3, 1.0 - 0.7 * dmg)
        for gi, o in self.owner.items():
            if o[0] == r and o[1] == wheel:
                self.sim.m.geom_friction[gi, 0] = self.mu0[gi] * scale

    def _kill(self, r, t, why):
        self.dead[r] = why
        self.sim.events.append((t, "dead", r, why, 0))

    def _apply_wire(self, r, eff, t):
        pl = self.sim.plant.get(r)
        if eff == "all":
            self._kill(r, t, "power wire cut")
        elif pl and eff == "weapon":
            for g, mot in pl["motors"].items():
                if g == "weapon":
                    mot.dead = True
        elif pl and eff and eff.startswith("side:"):
            side = eff[-1]
            for g, mot in pl["motors"].items():
                grp = self.sim.robots[r].group(g)
                if grp is not None and grp.kind == "wheel" and (grp.com[0] < 0) == (side == "l"):
                    mot.dead = True
        elif eff == "lifter":
            self.sim.profiles[r].lifter = None

    # ---- driver ------------------------------------------------------------
    def delay(self, r, t, cmd):
        """Push the brain's command; return the one decided `reaction_s` ago (with steering noise), or None."""
        q = self.queue[r]
        if cmd is not None and "drive" in cmd:
            n = self.p[r]["steer_noise"]
            l, rr = cmd["drive"]
            dv = n * self.sim.profiles[r].drive_max * self.rng.normal()
            cmd = dict(cmd, drive=(l - dv, rr + dv))
        q.append((t, cmd))
        out = None
        while q and t - q[0][0] >= self.p[r]["reaction_s"]:
            out = q.popleft()[1]
        return out


def _seg_dist(p, pts):
    best = 1e9
    for a, b in zip(pts[:-1], pts[1:]):
        ab = b - a
        L = float(ab @ ab)
        s = 0.0 if L < 1e-12 else max(0.0, min(1.0, float((p - a) @ ab) / L))
        best = min(best, float(np.linalg.norm(p - (a + s * ab))))
    return best
