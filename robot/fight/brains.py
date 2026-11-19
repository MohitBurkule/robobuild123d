"""Scripted drivers. Each brain sees both robots (pose, heading, opponent's profile) and returns wheel speeds plus a weapon
or lifter command. Behaviours come from the opponent's declared danger arcs, so a new robot needs no new code:

- every brain picks an attack bearing on the opponent that is furthest from its danger arcs (an undercutter's blade side,
  a spinner's front, a flipper's plate) and orbits outside the danger reach to get there before turning in;
- spinner: spins up first, then faces the target and drives through it (a vertical/horizontal spinner wants a square hit);
- lifter: drives its plate under the opponent and fires only when the opponent's centre of mass is over the plate and
  touching it; it also fires to self-right when upside down;
- pusher (wedges too): picks the arena hazard (open pit, unwalled edge) nearest the opponent, gets onto the far side of
  the opponent from it and drives through, so the shove ends in the pit;
- every brain keeps its own front edge on the platform (a driver does not drive itself into the pit).
After `patience` seconds without reaching a safe bearing, any brain charges anyway (real drivers get impatient too).
"""

from __future__ import annotations

import math

import numpy as np


def wrap(a):
    return (a + math.pi) % (2 * math.pi) - math.pi


class Brain:
    def __init__(self, me, opp, patience=4.0):
        self.me, self.opp, self.patience = me, opp, patience
        self.t_safe = 0.0
        self.state = "approach"
        self.fire_t = None

    # ---- geometry helpers ---------------------------------------------
    def _bearing_in_opp(self, sim):
        """Angle of my position seen from the opponent, in the opponent's frame (0 = its forward)."""
        mp, _, _ = sim.frame(self.me)
        op, oh, _ = sim.frame(self.opp)
        d = mp - op
        return wrap(math.atan2(d[1], d[0]) - oh), float(np.linalg.norm(d))

    def _danger(self, sim, bearing, dist):
        for c, half, reach in sim.profiles[self.opp].danger:
            if abs(wrap(bearing - c)) < half and dist < reach + 0.06:
                return True
        return False

    def _safe_bearing(self, sim):
        arcs = sim.profiles[self.opp].danger
        best, score = math.pi, -1
        for k in range(36):
            b = wrap(k * math.pi / 18)
            s = min((abs(wrap(b - c)) - h for c, h, _ in arcs), default=math.pi)
            if s > score:
                best, score = b, s
        return best

    def _steer(self, sim, target_xy, speed=1.0, reverse_ok=False):
        mp, mh, _ = sim.frame(self.me)
        # a real driver with reaction delay T steers where things WILL be: own heading + yaw rate * T, target + its v * T
        T = getattr(sim, "reaction_s", {}).get(self.me, 0.0)
        mh = mh + sim.yaw_rate(self.me) * T
        mp = mp + sim.vel_xy(self.me) * T
        if np.allclose(target_xy, sim.frame(self.opp)[0]):
            target_xy = np.asarray(target_xy) + sim.vel_xy(self.opp) * T
        d = np.asarray(target_xy) - mp
        want = math.atan2(d[1], d[0])
        err = wrap(want - mh)
        vmax = sim.profiles[self.me].drive_max
        if reverse_ok and abs(err) > 2.2:  # backing in is quicker than turning round
            err = wrap(err + math.pi)
            speed = -speed
        turn = max(-1.0, min(1.0, 2.0 * err))
        fwd = speed * max(0.0, math.cos(err)) ** 2
        return vmax * (fwd - turn), vmax * (fwd + turn)

    def _orbit_point(self, sim, bearing, dist, safe):
        op, oh, _ = sim.frame(self.opp)
        r = max(0.14, sim.profiles[self.opp].danger[0][2] + 0.08) if sim.profiles[self.opp].danger else 0.14
        step = math.copysign(min(abs(wrap(safe - bearing)), 0.9), wrap(safe - bearing))
        a = oh + bearing + step
        return op + r * np.array([math.cos(a), math.sin(a)])

    def _touching(self, sim):
        return any((a.startswith(self.me + "/") and b.startswith(self.opp + "/")) or
                   (a.startswith(self.opp + "/") and b.startswith(self.me + "/")) for a, b, _ in sim.contacts())

    # ---- policy ---------------------------------------------------------
    def act(self, sim, t, dt):
        bearing, dist = self._bearing_in_opp(sim)
        safe = self._safe_bearing(sim)
        op, _, _ = sim.frame(self.opp)
        off = abs(wrap(bearing - safe))
        if self.state == "approach":
            self.t_safe += dt
            if off < 0.6 or self.t_safe > self.patience or not self._danger(sim, bearing, dist) and dist < 0.12:
                self.state = "attack"
        elif self.state == "attack":
            if dist > 0.3 and not self._touching(sim):
                self.state, self.t_safe = "approach", 0.0
        if self.state == "approach" and dist < 0.5:
            l, r = self._steer(sim, self._orbit_point(sim, bearing, dist, safe), 1.0)
        else:
            l, r = self._steer(sim, op, 1.0)
        return {"drive": self._edge_guard(sim, t, (l, r))}

    def _edge_guard(self, sim, t, cmd):
        """If the edge of me I am driving towards would be off the platform, back off instead."""
        ar = getattr(sim, "arena", None)
        if ar is None:
            return cmd
        mp, mh, _ = sim.frame(self.me)
        lo, hi = sim.robots[self.me].bounds()
        reach = 0.5 * float(max(hi[0] - lo[0], hi[1] - lo[1])) + 0.015
        s = 1.0 if cmd[0] + cmd[1] >= 0 else -1.0
        f = np.array([math.cos(mh), math.sin(mh)])
        ahead = mp + s * reach * f
        if not ar.on_platform(ahead, t):
            v = 0.6 * sim.profiles[self.me].drive_max
            return (-s * v, -s * v)
        return cmd


class SpinnerBrain(Brain):
    def act(self, sim, t, dt):
        out = super().act(sim, t, dt)
        prof = sim.profiles[self.me]
        out["weapon"] = prof.weapon_omega
        if t < 0.6:  # spin up before engaging
            out["drive"] = (0.0, 0.0)
        if self.state == "attack":
            # drive THROUGH the opponent (forks/wedge get under it, the weapon follows); only back off to re-spin when
            # the weapon has really been stopped and we are not in contact
            w = abs(sim.weapon_omega(self.me))
            if w < 0.25 * abs(prof.weapon_omega) and not self._touching(sim):
                out["drive"] = tuple(-0.6 * v for v in self._steer(sim, sim.frame(self.opp)[0], 1.0))
        return out


class LifterBrain(Brain):
    def act(self, sim, t, dt):
        out = super().act(sim, t, dt)
        lf = sim.profiles[self.me].lifter
        if lf is None:  # servo lead cut: no flipper any more
            return out
        mp, mh, R = sim.frame(self.me)
        cmd = lf["down_rad"]
        inverted = R[2, 2] < -0.3
        if inverted:  # self-right
            cmd = lf["up_rad"]
        elif self.fire_t is not None and t - self.fire_t < 0.35:
            cmd = lf["up_rad"]
        elif self._over_plate(sim) and (self.fire_t is None or t - self.fire_t > 0.8):
            self.fire_t = t
            sim.events.append((t, "fire", self.me, lf["group"], 0))
            cmd = lf["up_rad"]
        out["lift"] = cmd
        return out

    def _over_plate(self, sim):
        op = sim.com(self.opp)
        mp, mh, R = sim.frame(self.me)
        rel = op[:2] - mp
        fwd = np.array([math.cos(mh), math.sin(mh)])
        along = float(rel @ fwd)
        side = abs(float(rel[0] * -fwd[1] + rel[1] * fwd[0]))
        touching = any(self.me + "/" in a and self.opp + "/" in b or self.opp + "/" in a and self.me + "/" in b
                       for a, b, _ in sim.contacts())
        return touching and 0.02 < along < 0.11 and side < 0.04


class PusherBrain(Brain):
    """Shove the opponent into the nearest pit / off the nearest open edge."""

    def act(self, sim, t, dt):
        ar = getattr(sim, "arena", None)
        pts = ar.hazards(t) if ar is not None else []
        if not pts:
            return super().act(sim, t, dt)
        op = sim.frame(self.opp)[0]
        mp = sim.frame(self.me)[0]
        hz = min(pts, key=lambda p: float(np.linalg.norm(p - op)))
        u = (hz - op) / (np.linalg.norm(hz - op) or 1.0)  # push direction
        to = op - mp
        dist = float(np.linalg.norm(to))
        cosang = float(to @ u) / (dist or 1.0)
        bearing, _ = self._bearing_in_opp(sim)
        if self._touching(sim) and cosang > 0.5 or cosang > 0.85:
            l, r = self._steer(sim, op, 1.0)  # lined up: drive through it towards the hazard
        else:
            # get behind it (side away from the hazard), going round it outside its danger reach
            back = op - 0.16 * u
            side = np.array([-u[1], u[0]])
            if float((mp - op) @ u) > -0.05:  # on the hazard side: swing wide round the opponent
                back = op + 0.18 * side * (1 if float((mp - op) @ side) >= 0 else -1) - 0.05 * u
            if self._danger(sim, bearing, dist) and dist < 0.2:
                back = mp + 0.1 * (mp - op) / (dist or 1.0) + 0.1 * side
            l, r = self._steer(sim, back, 1.0, reverse_ok=True)
        return {"drive": self._edge_guard(sim, t, (l, r))}


BRAINS = {"spinner": SpinnerBrain, "lifter": LifterBrain, "pusher": PusherBrain, "flanker": Brain}


def make(strategy, me, opp):
    return BRAINS.get(strategy, Brain)(me, opp)
