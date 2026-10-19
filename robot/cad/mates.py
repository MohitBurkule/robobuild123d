"""Assembly mates: place a part by constraints against another part instead of typing world coordinates.

WHY: hand-typed `at`/`rot` drift apart when one part moves (a plate gets 0.5 mm thicker, the screws and the motor on
it stay where they were). A mate states the intent once ("motor face on plate top, motor shaft coaxial with the bore")
and the placement is recomputed from the parent part's current pose every time the spec is loaded.

Features are given in each part's own frame: a plane {"point", "normal"}, an axis {"point", "axis"} or a point
{"point"}. A part may name them under "features" and constraints may then refer to them by name.

Constraint types (sequential, rigid; each one moves only the dependent part B, as little as possible):
  face     B's plane against A's plane: normals opposed (or `"flip": true` for same direction), B's plane at
           `offset` mm from A's along A's normal (gap > 0)
  coaxial  B's axis on A's axis (`"flip": true` reverses it); optional `"offset"`: B's axis point at that axial
           distance from A's axis point
  point_on_plane   B's point on A's plane (+ offset along its normal)
  point    B's point on A's point (+ optional "offset" vector in A's frame)
  angle    rotate B about A's axis/normal (feature `a`) by `deg` relative to its current orientation — use it last to
           fix the leftover spin
The constraint list is solved in order and swept a few times (Gauss-Seidel) so later constraints do not undo earlier
ones when the set is consistent; `residuals()` reports what is still off.

Spec use: a part with {"mate": {"to": "<part id>" | null, "constraints": [...]}} gets its `at`/`rot` computed by
`apply(spec_dict)` (run by robot.spec on load). The part's own `at`/`rot` are overwritten (in its parent's frame
as usual); the starting guess for the free degrees of freedom is the mate's own "at"/"rot", in A's frame, so a
part that is only face-mated still slides along with A. Mated parts may mate to mated parts (solved in dependency order), so
moving a part moves every part mated to it.
"""

from __future__ import annotations

import copy
import math

import numpy as np

from .. import xform

TOL = 1e-6


def _v(x):
    return np.asarray(x, float)


def _unit(x):
    x = _v(x)
    return x / np.linalg.norm(x)


def _rot_between(a, b):
    """Minimal rotation taking unit vector a to b."""
    a, b = _unit(a), _unit(b)
    c = float(np.clip(a @ b, -1, 1))
    if c > 1 - 1e-12:
        return np.eye(3)
    ax = np.cross(a, b)
    if np.linalg.norm(ax) < 1e-9:  # opposite: any perpendicular axis
        t = np.array([1.0, 0, 0]) if abs(a[0]) < 0.9 else np.array([0, 1.0, 0])
        ax = np.cross(a, t)
    return xform.axis_angle(ax, math.degrees(math.acos(c)))


def _rotate_about(M, R, pivot):
    """Apply world rotation R about world point pivot to pose M."""
    T = np.eye(4)
    T[:3, :3] = R
    T[:3, 3] = pivot - R @ pivot
    return T @ M


def _shift(M, d):
    M = M.copy()
    M[:3, 3] += d
    return M


def _feat(feats, f):
    if isinstance(f, str):
        if f not in (feats or {}):
            raise ValueError(f"unknown feature `{f}`")
        return feats[f]
    return f


def _world(M, f):
    out = {}
    if "point" in f:
        out["point"] = M[:3, :3] @ _v(f["point"]) + M[:3, 3]
    for k in ("normal", "axis"):
        if k in f:
            out[k] = _unit(M[:3, :3] @ _v(f[k]))
    return out


def _dir(f):
    return f.get("normal", f.get("axis"))


def step(MA, MB, c, fa_feats=None, fb_feats=None):
    """One constraint: returns B's new pose."""
    t = c.get("type")
    A = _world(MA, _feat(fa_feats, c["a"]))
    B = _world(MB, _feat(fb_feats, c["b"])) if "b" in c else None
    off = c.get("offset", 0.0)
    if t == "face":
        target = _dir(A) if c.get("flip") else -_dir(A)
        MB = _rotate_about(MB, _rot_between(_dir(B), target), B["point"])
        B = _world(MB, _feat(fb_feats, c["b"]))
        n = _dir(A)
        return _shift(MB, n * (float(off) - float((B["point"] - A["point"]) @ n)))
    if t == "coaxial":
        target = -_dir(A) if c.get("flip") else _dir(A)
        MB = _rotate_about(MB, _rot_between(_dir(B), target), B["point"])
        B = _world(MB, _feat(fb_feats, c["b"]))
        ax = _dir(A)
        d = B["point"] - A["point"]
        corr = -(d - ax * (d @ ax))
        if "offset" in c:
            corr += ax * (float(off) - float(d @ ax))
        return _shift(MB, corr)
    if t == "point_on_plane":
        n = _dir(A)
        return _shift(MB, n * (float(off) - float((B["point"] - A["point"]) @ n)))
    if t == "point":
        o = MA[:3, :3] @ _v(off) if not np.isscalar(off) else np.zeros(3)
        return _shift(MB, A["point"] + o - B["point"])
    if t == "angle":
        return _rotate_about(MB, xform.axis_angle(_dir(A), float(c.get("deg", 0.0))), A["point"])
    raise ValueError(f"unknown mate type `{t}`")


def residual(MA, MB, c, fa_feats=None, fb_feats=None) -> float:
    """How far constraint c is from satisfied (mm, or mm-equivalent 1 - cos for directions)."""
    t = c.get("type")
    if t == "angle":
        return 0.0
    A = _world(MA, _feat(fa_feats, c["a"]))
    B = _world(MB, _feat(fb_feats, c["b"]))
    off = c.get("offset", 0.0)
    if t == "face":
        target = _dir(A) if c.get("flip") else -_dir(A)
        return abs(1 - float(_dir(B) @ target)) + abs(float((B["point"] - A["point"]) @ _dir(A)) - float(off))
    if t == "coaxial":
        ax = -_dir(A) if c.get("flip") else _dir(A)
        d = B["point"] - A["point"]
        r = abs(1 - float(_dir(B) @ ax)) + float(np.linalg.norm(d - _dir(A) * (d @ _dir(A))))
        if "offset" in c:
            r += abs(float(d @ _dir(A)) - float(off))
        return r
    if t == "point_on_plane":
        return abs(float((B["point"] - A["point"]) @ _dir(A)) - float(off))
    if t == "point":
        o = MA[:3, :3] @ _v(off) if not np.isscalar(off) else np.zeros(3)
        return float(np.linalg.norm(A["point"] + o - B["point"]))
    raise ValueError(f"unknown mate type `{t}`")


def solve(MA, MB, constraints, fa_feats=None, fb_feats=None, sweeps=20):
    """B's pose satisfying the constraints in order (sequential Gauss-Seidel sweeps). `angle` steps run once."""
    MA, MB = _v(MA), _v(MB).copy()
    geo = [c for c in constraints if c.get("type") != "angle"]
    for _ in range(sweeps):
        for c in geo:
            MB = step(MA, MB, c, fa_feats, fb_feats)
        if max((residual(MA, MB, c, fa_feats, fb_feats) for c in geo), default=0.0) < TOL:
            break
    for c in constraints:
        if c.get("type") == "angle":
            MB = step(MA, MB, c, fa_feats, fb_feats)
            for c2 in geo:  # re-seat after the spin (it is about A's axis, so this is a no-op when consistent)
                MB = step(MA, MB, c2, fa_feats, fb_feats)
    return MB


def residuals(MA, MB, constraints, fa_feats=None, fb_feats=None) -> list:
    return [residual(MA, MB, c, fa_feats, fb_feats) for c in constraints]


def euler_from(R) -> list:
    """Degrees (rx, ry, rz) with R = Rz Ry Rx (robot.xform.euler's convention)."""
    R = _v(R)
    sy = -R[2, 0]
    ry = math.asin(max(-1.0, min(1.0, sy)))
    if abs(sy) < 1 - 1e-9:
        rx = math.atan2(R[2, 1], R[2, 2])
        rz = math.atan2(R[1, 0], R[0, 0])
    else:  # gimbal lock: put everything in rz
        rx = 0.0
        rz = math.atan2(-R[0, 1], R[1, 1])
    return [math.degrees(rx), math.degrees(ry), math.degrees(rz)]


def _pose(p):
    return xform.pose(p.get("at") or [0, 0, 0], p.get("rot") or [0, 0, 0])


def apply(spec: dict) -> dict:
    """Return a copy of a spec dict with every mated part's `at`/`rot` solved. Raises ValueError on a cycle."""
    parts = spec.get("parts") or []
    if not any(isinstance(p, dict) and p.get("mate") for p in parts):
        return spec
    out = copy.deepcopy(spec)
    by_id = {p.get("id"): p for p in out["parts"] if isinstance(p, dict)}
    world: dict = {}
    state: dict = {}

    def W(pid):
        if pid in world:
            return world[pid]
        if state.get(pid) == "busy":
            raise ValueError(f"mate cycle through `{pid}`")
        state[pid] = "busy"
        p = by_id[pid]
        parent = p.get("parent")
        PW = W(parent) if parent in by_id and parent != pid else np.eye(4)
        m = p.get("mate")
        if m:
            to = m.get("to")
            if to is not None and to not in by_id:
                raise ValueError(f"part `{pid}` mates to unknown part `{to}`")
            MA = W(to) if to is not None else np.eye(4)
            fa = by_id[to].get("features") if to is not None else m.get("features")
            MB = solve(MA, MA @ _pose(m), m.get("constraints") or [], fa, p.get("features"))
            local = np.linalg.inv(PW) @ MB
            p["at"] = [round(float(x), 6) for x in local[:3, 3]]
            p["rot"] = [round(float(x), 6) for x in euler_from(local[:3, :3])]
            world[pid] = MB
        else:
            world[pid] = PW @ _pose(p)
        state[pid] = "done"
        return world[pid]

    for pid in by_id:
        W(pid)
    return out
