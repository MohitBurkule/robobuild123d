"""`robot screws SPEC PART --face +z [--pattern corners|row|ring|at] [--n N] [--inset MM] [--at "u,v;u,v"] [--plug] [--dry]`

Visible screw heads where the reference photo shows them, as REAL fasteners (not printed dots). For each position on
the chosen outside face of PART (a static printed part) it casts a ray inward and:
- seats an M2 button-head screw (ISO 7380, head 3.5 x 1.3 mm) in a 0.2 mm-clear counterbore, so the head sits flush
  with the face (`joint.head_proud`) and the outline does not change;
- clamps PART to the first static printed part under it: a 2.4 mm clearance hole through PART, a 1.6 mm tap/pilot
  hole into the host, the shortest stock length giving >= 2d (4 mm) of thread in the host material;
- with --plug, when nothing lies under PART, threads into PART itself (the reason says it plugs its hole);
- skips the spot if the driver line above the head is blocked, if the shank or pilot would touch any other part, or
  if there is not enough material to thread into. Each skip is printed with its reason.
Then fills the `hole` records (`robot fasteners --fill`). Re-run `robot verify` and the likeness gate afterwards.

Face positions are in the face's own plane: for --face +z/-z they are (x, y); for +x/-x (y, z); for +y/-y (x, z).
--pattern corners = 4 points `inset` mm in from the corners of the part's face box; row = N points along the longer
side through the centre; ring = N points on a circle `inset` mm inside the smaller half-width; at = the --at list.
"""

from __future__ import annotations

import itertools
import json
import math

import numpy as np

HEAD_DK, HEAD_K, CLEAR_R, PILOT_R, CB_R = 3.5, 1.3, 1.2, 0.8, 1.95
STD_L = (4, 5, 6, 8, 10, 12, 16, 20)
MIN_THREAD = 4.0
AX = {"x": 0, "y": 1, "z": 2}


def _face(face):
    s = -1.0 if face.startswith("-") else 1.0
    k = AX[face[-1]]
    n = np.zeros(3); n[k] = s
    uv = [i for i in range(3) if i != k]
    return n, k, uv


def positions(aabb, face, pattern, n_pts, inset, at):
    n, k, (iu, iv) = _face(face)
    lo, hi = aabb
    if pattern == "at":
        pts = [tuple(float(x) for x in p.split(",")) for p in at.split(";") if p.strip()]
    elif pattern == "corners":
        pts = [(u, v) for u in (lo[iu] + inset, hi[iu] - inset) for v in (lo[iv] + inset, hi[iv] - inset)]
    elif pattern == "row":
        c = (lo + hi) / 2
        if hi[iu] - lo[iu] >= hi[iv] - lo[iv]:
            pts = [(u, c[iv]) for u in np.linspace(lo[iu] + inset, hi[iu] - inset, n_pts)]
        else:
            pts = [(c[iu], v) for v in np.linspace(lo[iv] + inset, hi[iv] - inset, n_pts)]
    elif pattern == "ring":
        c = (lo + hi) / 2
        r = min(hi[iu] - lo[iu], hi[iv] - lo[iv]) / 2 - inset
        pts = [(c[iu] + r * math.cos(a), c[iv] + r * math.sin(a)) for a in np.linspace(0, 2 * math.pi, n_pts, endpoint=False)]
    else:
        raise SystemExit(f"unknown pattern {pattern}")
    out = []
    for u, v in pts:
        q = np.zeros(3); q[iu], q[iv] = u, v; q[k] = (hi[k] if n[k] > 0 else lo[k]) + n[k] * 3.0
        out.append(q)
    return n, out


def _rot_for(d):
    """Euler angles (multiples of 90) turning local +z onto the axis-aligned direction d."""
    from . import xform
    for r in itertools.product((0, 90, 180, 270), repeat=3):
        if np.allclose(xform.euler(r) @ [0, 0, 1.0], d, atol=1e-6):
            return [float(x) for x in r]
    raise SystemExit("face must be axis-aligned")


def _local(p, q, d):
    from . import xform
    R = xform.euler(p.get("rot", [0, 0, 0]))
    ql = R.T @ (np.asarray(q, float) - np.asarray(p.get("at", [0, 0, 0]), float))
    return ql, R.T @ d


def _cyl_cut(p, start, d, r, length):
    """A cylinder radius r from world point `start` running `length` along d, in p's local frame."""
    sl, dl = _local(p, start, d)
    mid = sl + dl * length / 2
    return {"type": "place", "shape": {"type": "cylinder", "radius": r, "height": round(float(length), 3)},
            "at": [round(float(x), 3) for x in mid], "rot": _rot_for(np.round(dl, 6))}


def _add_cut(p, item):
    sh = p["shape"]
    if sh.get("type") == "subtract":
        sh.setdefault("cut", []).append(item)
    else:
        p["shape"] = {"type": "subtract", "base": sh, "cut": [item]}


def _static(p):
    return not p.get("joint") and not p.get("parent") and not p.get("rotates_with")


def main(path, part, face="+z", pattern="corners", n_pts=4, inset=4.0, at="", plug=False, dry=False):
    from . import spec as spec_mod, world as world_mod
    raw = json.load(open(path))
    byid = {p["id"]: p for p in raw["parts"]}
    if part not in byid:
        raise SystemExit(f"no part {part}")
    P = byid[part]
    if "catalog" in P or "shape" not in P or not _static(P):
        raise SystemExit(f"{part} must be a static printed part with a shape")
    w = world_mod.World.build(world_mod.resolve(spec_mod.load(path), fast=True))
    B = {b.id: b for b in w.bodies if not getattr(b, "is_wire", False)}
    nrm, starts = positions(B[part].aabb, face, pattern, n_pts, inset, at)
    d = -nrm
    hosts_ok = {i for i, p in byid.items() if "catalog" not in p and "shape" in p and _static(p) and p.get("kind") not in ("wheel", "weapon")}
    ring = [np.zeros(3)] + [CLEAR_R * np.array(v) for v in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0), (0, 0, 1), (0, 0, -1))]
    used = [f["id"] for f in raw.get("fasteners") or []]
    added, report = [], []
    for k, q0 in enumerate(starts):
        tag = f"{part}@{np.round(q0, 1).tolist()}"
        ts = np.arange(0.0, 60.0, 0.1)
        line = q0[None] + np.outer(ts, d)
        inp = B[part].inside(line)
        if not inp.any():
            report.append(f"{tag}: the ray misses {part}"); continue
        s = line[int(np.argmax(inp))]                      # outside surface point
        above = s[None] - np.outer(np.arange(0.3, 12.0, 0.3), d)
        if any(o.inside(above).any() for i, o in B.items() if i != part):
            report.append(f"{tag}: driver line above the head is blocked"); continue
        head_at = s + d * HEAD_K                           # underside of the flush head
        tt = np.arange(0.05, 30.0, 0.1)
        L_ = head_at[None] + np.outer(tt, d)
        inP = B[part].inside(L_)
        endP = int(np.argmax(~inP)) if (~inP).any() else len(tt)
        host, h0, h1 = None, None, None
        for i in hosts_ok - {part}:
            m = B[i].inside(L_)
            if m.any():
                a0 = int(np.argmax(m)); a1 = a0 + (int(np.argmax(~m[a0:])) if (~m[a0:]).any() else len(tt) - a0)
                if h0 is None or a0 < h0:
                    host, h0, h1 = i, a0, a1
        if host is not None and tt[h0] - tt[max(endP - 1, 0)] > 0.6:
            host = None                                    # not in contact under PART: it would clamp nothing
        if host is None:
            if not plug:
                report.append(f"{tag}: nothing under {part} to clamp (use --plug to thread into {part} itself)"); continue
            host, h0, h1, thr = part, 0, endP, []
        else:
            thr = [part]
        grip = tt[h0]
        Ls = [L for L in STD_L if L >= grip + MIN_THREAD and L <= tt[h1 - 1] - 0.3]
        boss = None
        if Ls:
            L = Ls[0]
        else:
            # a thin shell wall: grow a printed boss (OD 3d = 6 mm) on the inside of the host behind the wall, in its
            # own cavity only (the ray must re-enter the host or end inside its box before anything else), so the
            # outside does not change
            L = next((L for L in STD_L if L >= grip + MIN_THREAD), None)
            if L is None:
                report.append(f"{tag}: not {MIN_THREAD:g} mm of {host} material to thread into"); continue
            b0, b1 = tt[h1 - 1], L + 0.8                       # boss from the wall's inner face to past the tip
            tl = np.arange(0.05, 150.0, 0.1)
            mh = B[host].inside(head_at[None] + np.outer(tl, d))
            back = int(np.argmax(mh[h1:])) + h1 if mh[h1:].any() else None   # the far wall of the cavity
            if back is None or tl[back] < b1 + 0.5:
                report.append(f"{tag}: no room behind the {host} wall for a boss"); continue
            cyl = head_at[None] + np.outer(np.arange(b0, b1, 0.25), d)
            rim = [np.zeros(3)] + [3.3 * np.array(v) for v in itertools.product((-1, 0, 1), repeat=3) if any(v) and np.dot(v, np.abs(d)) == 0]
            near = [o.id for i, o in B.items() if i != host and any(o.inside(cyl + r).any() for r in rim)]
            if near:
                report.append(f"{tag}: boss behind the wall would touch {near}"); continue
            boss = (b0, b1)
        shank = head_at[None] + np.outer(np.arange(0, L + 0.6, 0.25), d)
        others = [o for i, o in B.items() if i not in (part, host) and not getattr(o, "fastener", False)]
        hit = [o.id for o in others if any(o.inside(shank + r).any() for r in ring)]
        if hit:
            report.append(f"{tag}: shank would touch {hit}"); continue
        fid = f"fs_look_{part}_{len(used) + len(added)}"
        rec = {"id": fid, "designation": f"M2x{L}", "at": [round(float(x), 3) for x in head_at], "dir": [round(float(x), 3) for x in d],
               "through": thr, "threads_into": host, "head": "button", "tool": "hex1.3", "removable": True,
               "reason": (f"M2 button-head screw where the photo shows a screw head, flush in a counterbore; `{part}` and `{host}` are one print, so it holds nothing else (plugs its hole)"
                          if thr and (P.get("fused_with") == host or byid[host].get("fused_with") == part) else
                          f"M2 button-head screw where the photo shows a screw head, flush in a counterbore; clamps `{part}` to `{host}`"
                          if thr else f"M2 button-head screw where the photo shows a screw head, flush in a counterbore; threads into `{part}` (holds nothing else; plugs its hole)")}
        if not dry:
            if boss:
                hp = byid[host]; c_ = _cyl_cut(hp, head_at + d * (boss[0] - 0.3), d, 3.0, boss[1] - boss[0] + 0.3)
                hp["shape"] = {"type": "union", "items": [hp["shape"], c_]}
                if hp is P: P = hp
            _add_cut(P, _cyl_cut(P, s - d * 0.5, d, CB_R, HEAD_K + 0.5))
            if thr:
                _add_cut(P, _cyl_cut(P, head_at - d * 0.05, d, CLEAR_R, tt[max(endP - 1, 0)] + 0.1))
                _add_cut(byid[host], _cyl_cut(byid[host], head_at + d * grip, d, PILOT_R, L - grip + 0.3))
            else:
                _add_cut(P, _cyl_cut(P, head_at - d * 0.05, d, PILOT_R, L + 0.35))
        added.append(rec)
        report.append(f"{tag}: {fid} M2x{L} " + (f"clamps {part} to {host}" if thr else f"into {part} (plug)") + (" with a 6 mm boss behind the wall" if boss else ""))
    for r in report:
        print(r)
    if dry or not added:
        print(f"{len(added)} screw(s){' (dry run)' if dry else ''}")
        return 0
    raw.setdefault("fasteners", []).extend(added)
    json.dump(raw, open(path, "w"), indent=1)
    from .fasten_fill import main as fill
    fill(path, fill=True)
    print(f"{len(added)} screw(s) added to {path}")
    return 0


def add_cli(sub):
    p = sub.add_parser("screws", help="visible screw heads where the photo shows them, as real flush M2 fasteners")
    p.add_argument("spec")
    p.add_argument("part", help="static printed part the heads sit on")
    p.add_argument("--face", default="+z", help="outside face the heads are on: +z (top), -z, +x, -x, +y (front), -y")
    p.add_argument("--pattern", default="corners", choices=("corners", "row", "ring", "at"))
    p.add_argument("--n", type=int, default=4, help="screws for row / ring")
    p.add_argument("--inset", type=float, default=4.0, help="mm in from the face box edge (corners, row) or rim (ring)")
    p.add_argument("--at", default="", help='with --pattern at: "u,v;u,v" face-plane coordinates (see module doc)')
    p.add_argument("--plug", action="store_true", help="when nothing is under the part, thread into the part itself")
    p.add_argument("--dry", action="store_true", help="print what would be added, change nothing")
    p.set_defaults(func=lambda a: main(a.spec, a.part, a.face, a.pattern, a.n, a.inset, a.at, a.plug, a.dry))
