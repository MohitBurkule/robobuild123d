"""Threat model: what an opponent (or the arena, or our own weapon) can do to each feature of a generated robot.

Design intent is mostly adversarial: a feature exists to answer an attack, and a feature that losing would kill the robot
(drive, weapon, power, radio) or that breaks easily (belt, wire, switch, tyre, thin print) must not be reachable by one.

* `ATTACKS` enumerates the attacks of UK 150 g antweight fights, each as a band of directions it arrives from and the
  height band (above the floor) it acts in.
* `exposure(spec)` casts each attack's directions at the robot from outside (a point z-buffer over sampled surface
  points, back faces culled) and lists, per part and fastener, the attacks whose first contact lands on it.
* `classify(part)` gives a part's criticality (what dies with it) and fragility (why it breaks).
* `check(spec)` applies the rule: an exposed critical or fragile feature needs an intent that names the exposing attack
  in `threats` AND either a shield that is compatible with being reachable (`doubled`, `sacrificial`, `guarded`) or an
  explicit `accepted_risk`. A shield claim that exposure contradicts (`inside_hull`, `behind_armour`, `recessed`,
  `captured` while the attack reaches it) fails. Screw heads reachable by an impact attack must be countersunk or
  recessed. Weapon supports must take a front hit in compression (bear on the chassis behind them).

Robot frame: +y is the front, +z up, x across; the floor is the lowest point of the wheels.
"""

from __future__ import annotations

import math
from dataclasses import dataclass

import numpy as np


def _n(*v):
    a = np.asarray(v, float)
    return a / np.linalg.norm(a)


def _ring(n, e=0.0, start=0.0):
    return [_n(math.cos(start + 2 * math.pi * k / n), math.sin(start + 2 * math.pi * k / n), e) for k in range(n)]


@dataclass(frozen=True)
class Attack:
    id: str
    label: str
    dirs: tuple  # unit vectors pointing FROM the robot TOWARDS where the attack comes from
    z_band: tuple  # (lo, hi) mm above the floor in which it acts; None = any height
    impact: bool  # a hard hit (screw heads, thin prints at risk), not a scrape or a grab
    note: str


F, B, L, R, U, D = (0, 1, 0), (0, -1, 0), (1, 0, 0), (-1, 0, 0), (0, 0, 1), (0, 0, -1)
ATTACKS = {a.id: a for a in [
    Attack("vspin_front", "vertical spinner, head on", (_n(0, 1, 0), _n(0, 1, -0.4), _n(0, 1, 0.5), _n(0.5, 1, 0), _n(-0.5, 1, 0)),
           None, True, "the most common UK ant weapon: teeth rise from the floor into the front corners and the front edge"),
    Attack("vspin_side", "vertical spinner from the side", (_n(1, 0, 0), _n(-1, 0, 0), _n(1, 0, 0.5), _n(-1, 0, 0.5),
                                                            _n(1, 0, -0.4), _n(-1, 0, -0.4)),
           None, True, "a side hit when the opponent wins the turn: wheels and side walls take it"),
    Attack("vspin_rear", "vertical spinner from behind", (_n(0, -1, 0), _n(0, -1, 0.5), _n(0, -1, -0.4)), None, True,
           "chased from behind: the rear wall, switch and rear wheels take it"),
    Attack("hspin_floor", "horizontal spinner at floor height", tuple(_ring(12)), (0.0, 14.0), True,
           "a bar or shell at 2-14 mm sweeps whatever stands proud of the hull at that height: tyres, wedgelets, screw heads"),
    Attack("under_front", "wedge or forks getting under the front", (_n(0, 1, -0.05),), (0.0, 4.0), False,
           "the ground game: whoever is lower wins; exposed things at floor level get scooped or snagged"),
    Attack("under_side", "wedge or forks getting under a side", (_n(1, 0, -0.05), _n(-1, 0, -0.05)), (0.0, 4.0), False,
           "side-on scoop: a tyre that stands proud of the side is lifted first"),
    Attack("under_rear", "wedge or forks getting under the rear", (_n(0, -1, -0.05),), (0.0, 4.0), False,
           "pushed from behind onto a wedge"),
    Attack("lifter_flipper", "lifter or flipper", (_n(0, 1, -0.6), _n(1, 0, -0.6), _n(-1, 0, -0.6), D), (0.0, 12.0), False,
           "a lifter arm comes under the belly and heaves: belly openings, low wires and belts are what it reaches"),
    Attack("grabber", "grabber or clamp", (_n(0, 1, 0), _n(1, 0, 0), _n(-1, 0, 0), _n(0, -1, 0)), (4.0, 40.0), False,
           "jaws close on whatever stands proud of the sides: arches, uprights, switch"),
    Attack("crusher_hammer", "crusher or hammer from above", (U, _n(0, 0.5, 1), _n(0, -0.5, 1), _n(0.5, 0, 1), _n(-0.5, 0, 1)),
           None, True, "an axe or crusher lands on the top: the top sheet must spread it; nothing critical straight under it"),
    Attack("wall_slam", "arena wall slam", tuple(_ring(8)), None, True,
           "thrown into the wall by a spinner: every face is an impact face for a moment"),
    Attack("inverted", "driving inverted", (U,), None, False,
           "upside down the top becomes the floor face: what stands proud of the top drags and snags"),
    Attack("flip_landing", "landing after a flip", (U, _n(1, 0, 0.6), _n(-1, 0, 0.6), _n(0, 1, 0.6), _n(0, -1, 0.6)), None, True,
           "a 300-600 mm fall onto a corner or the top: shock on everything stuck out, connectors and screws"),
    Attack("hazard_snag", "pit edge, arena seam or hazard snag", tuple(_ring(8, -0.1)), (0.0, 8.0), False,
           "seams, pit edges and spikes catch whatever hangs low or stands proud at the floor"),
    Attack("debris", "debris and fragments", (U, _n(0, 1, 0.3)), None, False,
           "tooth fragments, TPU shreds and screws fly about: open slots over moving parts swallow them"),
    Attack("reaction_gyro", "our own weapon's reaction torque and gyro", (), None, False,
           "spin-up torque twists the weapon supports; gyro precession loads them sideways when we turn"),
]}
# top threat class: everything in the arena tries to get under us, lift and throw us out (flippers, lifters, wedges, and
# vertical spinners whose rising tooth catches any edge, lip or face). Scored per bearing by `lift_and_throw`.
ATTACKS["lift_and_throw"] = Attack(
    "lift_and_throw", "get under, lift and throw", (), (0.0, 30.0), True,
    "the top threat class: a wedge, fork, lifter or flipper gets under the lowest leading edge, or a vertical spinner's "
    "tooth catches a step, hook or square face and either rips the part off or launches the robot")
ATTACKS = {"lift_and_throw": ATTACKS.pop("lift_and_throw"), **ATTACKS}
RAY_ATTACKS = [a for a in ATTACKS.values() if a.dirs]


def _load_cf():
    import json
    from pathlib import Path
    try:
        return {m["id"]: m for m in json.loads((Path(__file__).parent / "data" / "combat_failure_modes.json").read_text())}
    except (OSError, ValueError):
        return {}


# the combat failure-mode catalog (research/combat_failure_modes.json, 61 modes): intents may cite its ids in `threats`
CF = _load_cf()
# which catalogued failure modes each attack produces (the report lists them; countermeasures cite them)
ATTACK_CF = {
    "lift_and_throw": ["CF-VS01", "CF-VS04", "CF-WL01", "CF-WL07", "CF-HS05", "CF-AS01", "CF-AS02", "CF-AS03", "CF-AS04"],
    "vspin_front": ["CF-VS01", "CF-VS02", "CF-VS03", "CF-GD03"], "vspin_side": ["CF-VS01", "CF-GD03", "CF-HS02"],
    "vspin_rear": ["CF-VS01", "CF-GD06"], "hspin_floor": ["CF-HS01", "CF-HS02", "CF-HS05"],
    "under_front": ["CF-WL01", "CF-WL06"], "under_side": ["CF-WL07"], "under_rear": ["CF-WL07"],
    "lifter_flipper": ["CF-WL02", "CF-DB03"], "grabber": ["CF-WL03", "CF-WL04"],
    "crusher_hammer": ["CF-HA01", "CF-HA02", "CF-HA03"], "wall_slam": ["CF-AR01", "CF-ST02", "CF-ST04"],
    "inverted": ["CF-OW05", "CF-GD06"], "flip_landing": ["CF-LD01", "CF-LD02", "CF-LD03", "CF-WL05"],
    "hazard_snag": ["CF-AS05", "CF-AS06", "CF-AS07", "CF-AR02"], "debris": ["CF-DB01", "CF-DB02", "CF-DB04", "CF-DB05"],
    "reaction_gyro": ["CF-VS06", "CF-OW02", "CF-OW04"],
}


def known_threat(t: str) -> bool:
    return t in ATTACKS or t in CF
IMPACT = {a.id for a in ATTACKS.values() if a.impact}

SHIELDS = ("inside_hull", "behind_armour", "recessed", "captured", "doubled", "sacrificial", "guarded")
REACHABLE_OK = {"doubled", "sacrificial", "guarded"}  # shields that are honest about the feature being reachable

# what dies with a part (criticality) and why it breaks (fragility), by kind then by id prefix
CRIT_KIND = {"motor": "drive", "wheel": "drive", "pulley": "drive", "belt": "drive", "esc": "drive", "battery": "power",
             "switch": "power", "receiver": "radio", "weapon_motor": "weapon", "bearing": "weapon", "shaft": "weapon",
             "servo": "weapon", "weapon": "weapon"}
CRIT_ID = {"wesc": "weapon", "axle": "drive", "upright": "weapon", "spider": "weapon", "disc_b": "weapon"}
FRAG_KIND = {"belt": "belt", "switch": "switch", "wheel": "tyre", "battery": "lipo (punctures, then burns)",
             "receiver": "radio board", "esc": "bare board", "pulley": "thin print"}


def classify(p: dict) -> tuple:
    """(criticality or None, fragility or None) of a part dict."""
    crit = CRIT_KIND.get(p.get("kind"))
    for pre, c in CRIT_ID.items():
        if p["id"].startswith(pre):
            crit = crit or c
    frag = FRAG_KIND.get(p.get("kind"))
    return crit, frag


# ----------------------------------------------------------------------------------------------- exposure (z-buffer)
PIX = 0.8  # mm per pixel of the attack's view
SPACING = 0.45  # surface sample spacing (mm)
DEPTH_TOL = 0.6  # a point within this of the nearest surface in its pixel counts as the surface
MIN_AREA = 1.5  # mm2 of first-contact surface for a feature to count as reached


def _world(spec: dict, fast=True):
    from .. import spec as spec_mod
    from .. import world as world_mod
    r = world_mod.resolve(spec_mod.Spec(spec, None), fast=fast)
    return world_mod.World.start(r)


def _samples(w):
    from .. import geom
    P, N, I = [], [], []
    for i, b in enumerate(w.bodies):
        if b.is_wire:
            continue
        p, n = geom.sample_surface(b.mesh, SPACING, max_pts=80000)
        P.append(p), N.append(n), I.append(np.full(len(p), i))
    return np.vstack(P), np.vstack(N), np.concatenate(I)


def _visible(P, N, d):
    """Mask of points that are the first thing a straight attack along -d meets."""
    from scipy.ndimage import maximum_filter
    d = np.asarray(d, float)
    a = np.array([0.0, 0.0, 1.0]) if abs(d[2]) < 0.9 else np.array([1.0, 0.0, 0.0])
    u = np.cross(a, d)
    u /= np.linalg.norm(u)
    v = np.cross(d, u)
    front = (N @ d) > 0.05  # faces the attacker
    uu, vv, dep = P @ u, P @ v, P @ d
    iu = np.floor((uu - uu.min()) / PIX).astype(int)
    iv = np.floor((vv - vv.min()) / PIX).astype(int)
    zb = np.full((iu.max() + 1, iv.max() + 1), -np.inf)
    np.maximum.at(zb, (iu, iv), dep)  # every point occludes, front-facing or not (the hull is closed)
    zb = maximum_filter(zb, size=3, mode="constant", cval=-np.inf)  # close sampling gaps in the occluder
    return front & (dep >= zb[iu, iv] - DEPTH_TOL)


def exposure(spec: dict, w=None) -> dict:
    """{body id: {attack id: first-contact area mm2}} for every part and fastener an attack reaches."""
    w = w or _world(spec)
    P, N, I = _samples(w)
    wheels = [b for b in w.bodies if b.kind == "wheel"]
    floor = min(float(b.aabb[0][2]) for b in wheels) if wheels else float(P[:, 2].min())
    h = P[:, 2] - floor
    per_pt = SPACING * SPACING
    out: dict = {}
    for a in RAY_ATTACKS:
        hit = np.zeros(len(P), bool)
        for d in a.dirs:
            hit |= _visible(P, N, d)
        if a.z_band is not None:
            hit &= (h >= a.z_band[0]) & (h <= a.z_band[1])
        cnt = np.bincount(I[hit], minlength=len(w.bodies))
        for i in np.nonzero(cnt)[0]:
            area = cnt[i] * per_pt
            if area >= MIN_AREA:
                out.setdefault(w.bodies[i].id, {})[a.id] = round(float(area), 1)
    return out


# ----------------------------------------------------------------------------------------------- lift and throw
OPP_LIP = (0.3, 0.5)  # a typical opponent fork / acetate lip height (mm): we win the under-contest at or below it
DIRS8 = {"front": 90, "front_left": 45, "left": 0, "rear_left": 315, "rear": 270, "rear_right": 225, "right": 180,
         "front_right": 135}  # bearing (deg) around the centre: 0 = +x (left), 90 = +y (front)
BAND = 3.0  # outer band behind the outline that an attacker meets first (mm)
TOOTH_REACH = 30.0  # height a rising tooth can catch an edge at (mm above the floor)
BITE_MIN_AREA = 3.0  # mm2 of hookable downward-facing ledge for a bite
RAMP_DEG = 20.0  # leading surface tilted up at least this much deflects a rising hit; flatter takes it square
# how high an edge may sit above the floor per direction before the robot counts as un-skirted there
LIP_MAX = {"front": 1.0, "front_left": 3.0, "front_right": 3.0, "left": 3.0, "right": 3.0, "rear_left": 3.0,
           "rear_right": 3.0, "rear": 3.0}


def lift_and_throw(spec: dict, w=None) -> dict:
    """Per direction of the 8: under-ness (lowest leading edge vs an opponent lip), bite (hookable ledges a rising tooth
    catches, what it would rip off, how high it would launch us) and edge shape (ramp vs square), measured on the same
    perimeter profile the verifier's combat.R0xx rules use (`checks.combat_ground.profile`)."""
    from ..checks import combat_ground as cg
    w = w or _world(spec)
    P, N, I = _samples(w)
    bodies = w.bodies
    rot = {p["id"] for p in spec.get("parts", []) if p.get("rotates_with") not in (None, "fixed")}
    kind = np.array(["wheel" if bodies[i].kind == "wheel" else ("rotor" if bodies[i].id in rot else bodies[i].kind)
                     for i in range(len(bodies))], dtype=object)
    K = kind[I]
    keep = K != "other_fastener"
    wheels = [b for b in bodies if b.kind == "wheel"]
    floor = min(float(b.aabb[0][2]) for b in wheels) if wheels else float(P[:, 2].min())
    lo, hi = P.min(axis=0), P.max(axis=0)
    centre = (lo[:2] + hi[:2]) / 2
    rout, gap, wheel_edge = cg.profile(P[keep], K[keep], floor, centre)
    q = P[:, :2] - centre
    ang = (np.degrees(np.arctan2(q[:, 1], q[:, 0])) % 360).astype(int) % 360
    r = np.hypot(q[:, 0], q[:, 1])
    radial = np.zeros_like(P)
    radial[:, :2] = q / np.maximum(r, 1e-9)[:, None]
    nr = (N * radial).sum(axis=1)
    h = P[:, 2] - floor
    outer = (r >= rout[ang] - BAND) & (K != "wheel") & (K != "rotor")
    fasteners = [b for b in bodies if getattr(b, "fastener", None) is not None]
    # an arch or guard directly over a tyre is reached only past the tyre (a rising tooth meets the tyre first)
    over_tyre = np.zeros(len(P), bool)
    for b in wheels:
        (x0, y0, _), (x1, y1, z1) = b.aabb
        over_tyre |= (P[:, 0] > x0 - 1.0) & (P[:, 0] < x1 + 1.0) & (P[:, 1] > y0 - 1.0) & (P[:, 1] < y1 + 1.0)
    out = {}
    for name, b0 in DIRS8.items():
        sec = ((np.arange(360) - b0 + 22.5) % 360) < 45.0
        g = gap[sec & ~wheel_edge]  # where a tyre is the edge, the tyre is what a wedge meets (reported apart)
        g = g[np.isfinite(g) & (g < 98.0)]
        door = float(np.mean(g > LIP_MAX[name])) if len(g) else 1.0
        m = outer & sec[ang]
        # bite: downward-facing ledge (overhang / step) on the outer band, inside the tooth's reach, above the lowest edge
        med = float(np.median(g)) if len(g) else 99.0
        # a rising tooth arrives from this bearing and from below the edge: only ledges it can see count
        br = math.radians(b0)
        vis = np.zeros(len(P), bool)
        for e in (-0.5, -1.2):
            vis |= _visible(P, N, _n(math.cos(br), math.sin(br), e))
        ledge = m & vis & (N[:, 2] < -0.6) & (h > med + 1.0) & (h < TOOTH_REACH) & ~over_tyre
        if ledge.any() and fasteners:  # a seat in contact with a flush screw head is covered by the head
            idx = np.nonzero(ledge)[0]
            near = np.zeros(len(idx), bool)
            for fb in fasteners:
                near |= np.abs(fb.distance(P[idx])) < 0.35
            ledge[idx[near]] = False
        cnt = np.bincount(I[ledge], minlength=len(bodies)) * SPACING * SPACING
        bites = {bodies[i].id: round(float(cnt[i]), 1) for i in np.nonzero(cnt >= BITE_MIN_AREA)[0]}
        bite_h = float(h[ledge].min()) if ledge.any() and bites else None
        # edge shape of what a hit meets low down: outward-facing points in the low band
        face = m & (nr > 0.2) & (h < 12.0)
        elev = np.degrees(np.arctan2(N[face, 2], np.maximum(nr[face], 1e-9))) if face.any() else np.array([0.0])
        ramp = float(np.mean(elev >= RAMP_DEG))
        first = {}
        for i in np.unique(I[m]):
            first[bodies[i].id] = round(float(np.sum(I[m] == i) * SPACING * SPACING), 1)
        out[name] = {"gap_mm": round(med, 2), "gap_min_mm": round(float(g.min()), 2) if len(g) else None,
                     "door_frac": round(door, 2), "wheel_edge_frac": round(float(np.mean(wheel_edge[sec])), 2),
                     "under": "wins" if med <= OPP_LIP[1] else ("contests" if med <= 1.0 else "loses"),
                     "bite": bites, "bite_h_mm": None if bite_h is None else round(bite_h, 1),
                     "launch_lever_mm": None if bite_h is None else round(bite_h - med, 1),
                     "ramp_frac": round(ramp, 2), "first_contact": dict(sorted(first.items(), key=lambda kv: -kv[1])[:4])}
    return out


def ground_game_problems(spec: dict, lt: dict) -> list[str]:
    """The gate rule for the top threat class: every direction skirted (lowest edge under LIP_MAX), no bite edge, unless
    the hypothesis's ground-game statement accepts that direction's risk with a reason."""
    gg = (spec.get("generator") or {}).get("ground_game") or {}
    acc = gg.get("accepted") or {}
    out = []
    for name, v in lt.items():
        if v["door_frac"] > 0.5 and name not in acc:
            out.append(f"lift_and_throw {name}: un-skirted - lowest edge {v['gap_mm']} mm (> {LIP_MAX[name]} mm over "
                       f"{v['door_frac'] * 100:.0f}% of the arc); an opponent lip at {OPP_LIP[1]} mm gets under")
        if v["bite"] and f"{name}.bite" not in acc:
            out.append(f"lift_and_throw {name}: bite edge at {v['bite_h_mm']} mm on {sorted(v['bite'])} - a rising tooth "
                       "hooks it")
    return out


# ----------------------------------------------------------------------------------------------- the rule
def _intents(spec):
    feats = (spec.get("generator") or {}).get("features") or []
    by = {}
    for f in feats:
        if f.get("op") in ("part", "fastener") and f.get("intent"):
            by[f["target"]] = f["intent"]
    return by


JAM_BAND = (1.5, 15.0)


def jam_gaps(spec: dict, w) -> list[tuple]:
    """CF-DB01/DB02: moving parts (wheels, weapon) whose smallest gap to static structure lies in the jam band."""
    from .. import geom
    parts = {p["id"]: p for p in spec.get("parts", [])}
    static_k = ("structure", "wedge", "skirt", "armor", "fork")
    mov = [b for b in w.bodies if b.id in parts and parts[b.id].get("kind") in ("wheel", "weapon")]
    stat = [b for b in w.bodies if b.id in parts and parts[b.id].get("kind") in static_k
            and parts[b.id].get("rotates_with") in (None, "fixed")]
    out = []
    for m in mov:
        p, _ = geom.sample_surface(m.mesh, 0.6, max_pts=15000)
        best = min(((float(np.min(np.abs(s_.distance(p)))), s_.id) for s_ in stat), default=None)
        if best and JAM_BAND[0] <= best[0] <= JAM_BAND[1]:
            out.append((m.id, best[0], best[1]))
    return out


def wire_sides(spec: dict) -> list[str]:
    """CF-GD02 / CF-GD05: each drive side has its own motor lead (one cut wire stops one side, not both)."""
    parts = {p["id"]: p for p in spec.get("parts", [])}
    motors = [pid for pid, p in parts.items() if p.get("kind") == "motor" and pid.startswith("motor_")]
    out = []
    for m in motors:
        leads = [w for w in spec.get("wires", []) if str(w.get("to", "")).split(".")[0] == m or str(w.get("from", "")).split(".")[0] == m]
        if len(leads) != 1:
            out.append(f"part {m}: {len(leads)} motor leads - each drive side needs exactly one lead of its own (CF-GD02)")
    xs = {round(parts[m]["at"][0]) > 0 for m in motors if parts[m].get("at")}
    if len(motors) >= 2 and len(xs) < 2:
        out.append("drive motors all on one side: one hit there stops both (CF-GD05)")
    return out


def compression_ok(w, upright_id, chassis_ids, gap=0.4) -> bool:
    """A weapon support takes a front hit in compression: some of its rear-facing surface bears on the chassis just
    behind it (a hit pushes it rearward into structure, not away from it)."""
    from .. import geom
    b = w.body(upright_id)
    if b is None:
        return True
    p, n = geom.sample_surface(b.mesh, 0.6)
    back = p[n[:, 1] < -0.7] - np.array([0.0, gap, 0.0])
    if not len(back):
        return False
    return any(w.body(c) is not None and w.body(c).inside(back).any() for c in chassis_ids)


def recessed(w, f) -> bool:
    """A socket/button head sits in a counterbore: a ring just outside the head, two thirds of the way up it, lies inside
    solid (so a tooth or hammer cannot reach the side of the head to shear it)."""
    from .. import catalog
    dl = catalog.parse_designation(f.get("designation", ""))
    if not dl:
        return False
    d = dl[0]
    dk, k = (1.9 * d, 0.55 * d) if f.get("head") == "button" else catalog.screw_dims(d)[:2]
    n = np.asarray(f["dir"], float)
    n /= np.linalg.norm(n)
    a = np.array([0.0, 0.0, 1.0]) if abs(n[2]) < 0.9 else np.array([1.0, 0.0, 0.0])
    u = np.cross(n, a)
    u /= np.linalg.norm(u)
    v = np.cross(n, u)
    c = np.asarray(f["at"], float) - n * (0.66 * k)
    ring = np.array([c + (dk / 2 + 0.5) * (math.cos(t) * u + math.sin(t) * v) for t in np.linspace(0, 2 * math.pi, 12, endpoint=False)])
    inside = np.zeros(len(ring), bool)
    for b in w.bodies:
        if not b.fastener and not b.is_wire:
            inside |= b.inside(ring)
    return float(inside.mean()) >= 0.75


def part_problems(spec: dict, exp: dict) -> list[str]:
    """The shielding rule: a critical or fragile part an attack reaches must claim a shield that admits being reachable
    (doubled / sacrificial / guarded) or carry an accepted risk, and its intent must name each attack that reaches it."""
    ints = _intents(spec)
    out = []
    parts = {p["id"]: p for p in spec.get("parts", [])}
    for pid, p in parts.items():
        crit, frag = classify(p)
        if not (crit or frag):
            continue
        reach = exp.get(pid, {})
        if not reach:
            continue
        it = ints.get(pid) or {}
        named = set(it.get("threats") or [])
        shield = it.get("shield")
        why = f"{p.get('kind')} ({'kills ' + crit if crit else ''}{', ' if crit and frag else ''}{frag or ''})"
        for att, area in sorted(reach.items()):
            if shield in SHIELDS and shield not in REACHABLE_OK:
                out.append(f"part {pid}: claims shield `{shield}` but `{att}` reaches {area:g} mm2 of it - {why}")
            elif not (shield in REACHABLE_OK or str(it.get("accepted_risk") or "").strip()):
                out.append(f"part {pid}: `{att}` reaches {area:g} mm2 of it and it has no shield or accepted risk - {why}")
            elif att not in named:
                out.append(f"part {pid}: `{att}` reaches it but its intent does not name that threat - {why}")
    return out


def check(spec: dict, exp: dict | None = None, w=None) -> list[str]:
    """Problems with the robot's answers to the threat model (empty = every reachable critical or fragile feature is
    shielded honestly or carries an accepted risk; impact-face screws countersunk or recessed; weapon supports in
    compression)."""
    w = w or _world(spec)
    exp = exposure(spec, w) if exp is None else exp
    ints = _intents(spec)
    out = ground_game_problems(spec, lift_and_throw(spec, w))
    parts = {p["id"]: p for p in spec.get("parts", [])}
    out += part_problems(spec, exp)
    rotor = {pid for pid, p in parts.items() if p.get("rotates_with") not in (None, "fixed")}
    for f in spec.get("fasteners", []):
        reach = {a: v for a, v in exp.get(f["id"], {}).items() if a in IMPACT}
        if not reach or set(f.get("through") or []) & rotor:  # a screw riding on the weapon is part of the weapon
            continue
        it = ints.get(f["id"]) or {}
        head = f.get("head") or "socket"
        if head in ("countersunk", "csk", "flat") or recessed(w, f):
            continue
        if str(it.get("accepted_risk") or "").strip() and set(reach) <= set(it.get("threats") or []):
            continue
        out.append(f"fastener {f['id']}: {head} head on an impact face ({', '.join(sorted(reach))}); countersink or recess it")
    out += wire_sides(spec)
    for mid, g, sid in jam_gaps(spec, w):
        it = ints.get(mid) or {}
        cf = "CF-DB01" if (parts[mid].get("kind") == "wheel") else "CF-DB02"
        if not (str(it.get("accepted_risk") or "").strip() and cf in (it.get("threats") or [])):
            out.append(f"part {mid}: {g:.1f} mm from {sid} - in the 1.5-15 mm jam band where debris wedges ({cf}); "
                       "close it under 1.5 mm or open it past 15 mm")
    chassis = [pid for pid, p in parts.items() if p.get("kind") == "structure" and pid.startswith(("chassis", "tub"))]
    for pid in parts:
        if pid.startswith("upright") and not compression_ok(w, pid, chassis):
            out.append(f"part {pid}: a front hit pulls the weapon support off the chassis (no bearing face behind it)")
    return out


def report(spec: dict, name: str, exp: dict | None = None, w=None) -> str:
    """Markdown threat report: per attack, which features it reaches and how each survives."""
    w = w or _world(spec)
    exp = exposure(spec, w) if exp is None else exp
    ints = _intents(spec)
    parts = {p["id"]: p for p in spec.get("parts", [])}
    lines = [f"# Threat report: {name}", "",
             "Generated by `robot/gen/threats.py`. Reach = surface area (mm2) an attack meets first, cast from outside the hull "
             "along the attack's directions within its height band. Survival = the feature's intent (shield, accepted risk, "
             "reason).", ""]
    gg = (spec.get("generator") or {}).get("ground_game") or {}
    acc = gg.get("accepted") or {}
    lt = lift_and_throw(spec, w)
    lines += ["## Ground game (lift and throw: the top threat class)", ""]
    for k in ("front", "lip_material", "skirts", "trade"):
        if gg.get(k):
            lines.append(f"- **{k.replace('_', ' ')}**: {gg[k]}")
    lines += ["", f"Polar under-ness and bite, 8 directions (opponent lip {OPP_LIP[0]}-{OPP_LIP[1]} mm; "
              "bearing 0 = left, 90 = front). Gap = our median lowest leading edge off the floor in that 45 deg sector "
              "(wheel-only bins excluded).", "",
              "| dir | bearing | gap mm | under | ramp | bite (mm2) | bite h / lever mm | first contact | answer |",
              "|---|---|---|---|---|---|---|---|---|"]
    for name, bearing in DIRS8.items():
        v = lt[name]
        bite = ", ".join(f"`{k}` {a:g}" for k, a in sorted(v["bite"].items())) or "-"
        hl = "-" if v["bite_h_mm"] is None else f"{v['bite_h_mm']} / {v['launch_lever_mm']}"
        fc = ", ".join(f"`{k}`" for k in v["first_contact"]) or "-"
        ans = "; ".join(x for x in (acc.get(name) and ("accepted: " + acc[name][:90]),
                                    acc.get(name + ".bite") and ("bite accepted: " + acc[name + ".bite"][:90])) if x) or "skirted, no bite"
        lines.append(f"| {name} | {bearing} | {v['gap_mm']} | {v['under']} | {v['ramp_frac']:.0%} | {bite} | {hl} | {fc} | {ans} |")
    lines.append("")
    for a in ATTACKS.values():
        lines += [f"## {a.label} (`{a.id}`)", "", f"_{a.note}_", ""]
        cfs = ATTACK_CF.get(a.id) or []
        if cfs:
            lines += ["Failure modes: " + ", ".join(f"{c} {CF[c].get('name', '')}" if c in CF else c for c in cfs), ""]
        if not a.dirs:
            sup = [pid for pid in parts if pid.startswith(("upright", "weapon_motor", "wbearing", "top_bridge", "spider"))]
            lines += ["Not a ray attack: it loads the weapon supports from inside.", ""]
            for pid in sup:
                it = ints.get(pid) or {}
                lines.append(f"- `{pid}`: {it.get('reason', '-')} ({it.get('load_or_constraint', '-')})")
            lines.append("")
            continue
        hit = sorted(((v[a.id], k) for k, v in exp.items() if a.id in v), reverse=True)
        if not hit:
            lines += ["Reaches nothing.", ""]
            continue
        lines += ["| feature | reach mm2 | criticality / fragility | survives by |", "|---|---|---|---|"]
        for area, k in hit:
            p = parts.get(k)
            crit, frag = classify(p) if p else (None, "screw head" if a.impact else None)
            it = ints.get(k) or {}
            how = it.get("shield") or ""
            if it.get("accepted_risk"):
                how = (how + "; " if how else "") + "accepted: " + it["accepted_risk"]
            if not how:
                how = "structure / armour: " + (it.get("reason", "-")[:120])
            lines.append(f"| `{k}` | {area:g} | {crit or '-'} / {frag or '-'} | {how} |")
        lines.append("")
    probs = check(spec, exp, w)
    lines += ["## Check", "", "No unanswered threats." if not probs else "\n".join(f"- {m}" for m in probs), ""]
    return "\n".join(lines)


# ----------------------------------------------------------------------------------------------- generator answers
ALL_RAY = tuple(a for a in ATTACKS if ATTACKS[a].dirs)
# (id prefix or kind, shield, accepted risk, CF ids): the engine's standing answer for a feature class it cannot hide.
ANSWERS = (
    ("kind:wheel", "guarded", "the tyre must touch the floor and stand proud of the side wall to drive and to self-right; "
     "the wells and skirts cover all but the tread arc, the hub is inside the well, and tyres are cheap press-on spares",
     ["CF-HS02", "CF-LD02", "CF-DB01", "CF-GD05"]),
    ("kind:switch", None, "the switch must be reachable with a pin through the shell; it sits below the "
     "roof 2 mm deep, sliding across the robot (square to a front-rear scrape); only a point dropped straight down "
     "the slot reaches it, and that at worst turns it off (failsafe)",
     ["CF-GD06"]),
    ("upright", "sacrificial", "the uprights are the weapon module and stand outside the hull to carry the disc; they are "
     "bolted on, take hits in compression on the chassis, and are spares", ["CF-OW04", "CF-VS06", "CF-ST04"]),
    ("weapon_motor", "guarded", "the outrunner turns inside the disc/spider; only its can is reachable between the "
     "uprights, behind the disc", ["CF-DB05", "CF-GD08"]),
    ("weapon", "sacrificial", "the weapon is meant to be hit: hardened steel, spares in the pit kit; its 2-4 mm running "
     "gap to the chassis sits in the debris jam band because the disc must clear the hull under impact deflection "
     "(a tighter gap rubs after the first hit, a 15 mm gap costs the bite height) - the weapon ESC's current limit stalls "
     "rather than strips on a jam", ["CF-VS02", "CF-OW01", "CF-DB02"]),
    ("disc_b", "sacrificial", "the second disc is the weapon", ["CF-VS02"]),
    ("spider", "guarded", "the spider sits between the discs; only its rim shows", ["CF-OW04"]),
    ("wshaft", "guarded", "the shaft ends sit in the uprights' bores; only the end faces show", ["CF-DB05", "CF-LD02"]),
    ("servo", "guarded", "the lifter servo drives the scoop arm through the side wall: its output side must reach the "
     "arm, so its case shows through the arm slot; the scoop cheeks cover it from the side and it is a cheap spare",
     ["CF-GD01", "CF-HS01"]),
    ("wbearing", "guarded", "seen only down the shaft bore; the shaft end fills the line of sight", ["CF-OW04"]),
)
FAST_ANSWERS = (
    (("bolt_up", "bolt_wm"), "the head sits on the weapon module (upright foot / stator), which is itself the contact "
     "surface; bolts are spares and the uprights bear on the chassis in compression, so a sheared head does not free the "
     "weapon", ["CF-ST04", "CF-OW04"]),
    (("bolt_br", "bolt_bl"), "the bridge screws ride on the top bridge of the bar module, above the bar's sweep; a "
     "head sheared there leaves the bar shaft held by the bottom bearing", ["CF-ST04", "CF-OW04"]),
    (("bolt_f",), "button head on a replaceable side tine or wedgelet whose plate cannot take a countersink (the 4WD "
     "TPU wedgelet's M3 cone would meet the axle standoff's bore; a 1.5 mm Ti tine would keep 0.2 mm under the cone); "
     "a tooth that catches it bends or tears a spare, not the chassis", ["CF-AS04", "CF-VS03"]),
)


def answer(plan) -> None:
    """Attach the engine's shield / accepted-risk answer, naming every ray attack and the CF ids, to each critical or
    fragile feature class that must stay reachable (wheels, switch, weapon module), and to the screw heads that ride on
    replaceable contact parts. Features already shielded inside the hull keep their own intent."""
    kinds = {p["id"]: p.get("kind") for p in plan.parts}
    for f in plan.features:
        it, tgt = f.get("intent"), f.get("target")
        if not it or f.get("op") not in ("part", "fastener"):
            continue
        hit = None
        if f["op"] == "part":
            for key, sh_, why, cf in ANSWERS:
                if (key.startswith("kind:") and kinds.get(tgt) == key[5:]) or (not key.startswith("kind:") and tgt.startswith(key)):
                    hit = (sh_, why, cf)
                    break
        else:
            for pre, why, cf in FAST_ANSWERS:
                if tgt.startswith(pre):
                    hit = (None, why, cf)
                    break
        if not hit:
            continue
        sh_, why, cf = hit
        if sh_:
            it["shield"] = sh_
        it["accepted_risk"] = why
        it["threats"] = list(dict.fromkeys(list(it.get("threats") or []) + list(ALL_RAY) + cf))


# ----------------------------------------------------------------------------------------------- lip / fork rules
E_MPA = {"titanium": 110000.0, "tpu": 26.0, "petg_cf": 3500.0, "petg": 2000.0, "spring_steel": 200000.0, "acetate": 2500.0}


def lip_rules(mat, under_deg, tip_r, under_chamfer, hinged, t, h, L, w_tip, joined, tip_load_n=50.0, contact_mm2=None):
    """CF-AS01..AS04 for a lip or tine: (one-line statement with the numbers, list of rules it does not meet).
    AS01 tip underside 10-20 deg and tip radius 0.3-1 mm; AS02 under-chamfer >= 1 mm or hinged; AS03 tip pressure
    < 5 MPa and stiffness 0.5-5 N/mm (a flexible lip); AS04 tine tip width > 8 mm, joined tips or tip radius >= w/2
    (risk when w is in [2, 6] mm and the tine flexes). Stiffness: cantilever of length L, section t (across the bend)
    x h (along the load), k = 3 E (t h^3 / 12) / L^3, tip load `tip_load_n`."""
    k = 3 * E_MPA.get(mat, 2000.0) * (t * h ** 3 / 12.0) / max(L, 1.0) ** 3
    area = contact_mm2 or max(w_tip * max(tip_r, 0.3) * 2, 0.1)
    p = tip_load_n / area
    miss = []
    if not (10.0 <= under_deg <= 20.0) or not (0.3 <= tip_r <= 1.0):
        miss.append("CF-AS01")
    if not (under_chamfer >= 1.0 or hinged):
        miss.append("CF-AS02")
    if not (p < 5.0 and 0.5 <= k <= 5.0):
        miss.append("CF-AS03")
    flexible = k < 50.0
    if not (w_tip > 8.0 or joined or tip_r >= w_tip / 2) and 2.0 <= w_tip <= 6.0 and flexible:
        miss.append("CF-AS04")
    txt = (f"AS01 underside {under_deg:.0f} deg, tip r {tip_r:g} mm; AS02 under-chamfer {under_chamfer:g} mm"
           f"{' (hinged)' if hinged else ''}; AS03 tip {p:.1f} MPa at {tip_load_n:g} N, stiffness {k:.3g} N/mm; "
           f"AS04 tip width {w_tip:g} mm{' joined' if joined else ''}")
    return txt, miss
