"""Does a screw's head and thread actually fit the hole the part has? Pure geometry probes, no build123d.

`probe(f, host_inside, thread_inside=None)` measures, along the fastener axis (t = 0 at the spec `at`, + toward tip):
  surface_t    where the host's outer surface is just outside the head recess (csk flush: 0; counterbore: -depth)
  head_clash   fraction of points just inside the head envelope that sit in host material (hole too small / head proud
               into a wall); should be 0
  head_bearing fraction of points just under the head (csk: on the cone) that sit in material; should be ~1
  thread_bite / pilot_open   tapped holes: material between tap drill and major diameter / pilot bore open
  nut_open / nut_held        nut pockets: inside the flats is empty / material just outside the flats (press fit)
and `judge()` turns that into (id, ok, message) rows against the recorded `hole` dict (from robot.cad.holes) or, if
there is none, against the defaults implied by the head type (a countersunk head must sit flush).
"""

from __future__ import annotations

import numpy as np

from . import fastener_catalog as fc

HEAD_MAP = {"countersunk": "csk", "csk": "csk", "button": "button", None: "cap", "cap": "cap", "socket": "cap"}
FLUSH_TOL = 0.25


def _basis(a):
    a = np.asarray(a, float)
    a = a / np.linalg.norm(a)
    t = np.array([1.0, 0, 0]) if abs(a[0]) < 0.9 else np.array([0, 1.0, 0])
    u = np.cross(a, t)
    u /= np.linalg.norm(u)
    return a, u, np.cross(a, u)


def _ring(at, a, u, v, t, r, n=12):
    ang = np.arange(n) * 2 * np.pi / n
    return at + a * t + np.outer(np.cos(ang) * r, u) + np.outer(np.sin(ang) * r, v)


def _frac(inside, P):
    return float(np.mean(inside(P))) if len(P) else 0.0


def probe(f, host_inside, thread_inside=None) -> dict:
    """f: dict-like with designation, at, dir, head and optional hole; *_inside: callable(P[n,3]) -> bool[n]."""
    g = lambda k, dflt=None: (f.get(k, dflt) if isinstance(f, dict) else getattr(f, k, dflt))  # noqa: E731
    hole = g("hole") or (getattr(f, "_extra", {}) or {}).get("hole") or {}
    s = fc.parse(g("designation"))
    style = hole.get("head") or HEAD_MAP.get(g("head"), "cap")
    dk, k = fc.head(s.d, style)
    c = hole.get("clearance_d") or fc.clearance(s.d)
    at = np.asarray(g("at"), float)
    a, u, v = _basis(g("dir"))
    out = {"style": style, "d": s.d, "dk": dk, "k": k}
    # surface just outside the recess: march from 6 mm above to 6 mm below `at`
    r_out = max(dk / 2 + 0.8, (hole.get("csk_d") or hole.get("cbore_d") or dk) / 2 + 0.5)
    ts = np.arange(-6.0, 6.0, 0.05)
    surf = None
    for t in ts:
        if _frac(host_inside, _ring(at, a, u, v, t + 0.025, r_out)) >= 0.5:
            surf = float(t)
            break
    out["surface_t"] = surf
    if style != "csk" and surf is not None:
        # counterbore floor: first material under the head annulus, marching from the outer surface toward the tip
        rf = (c / 2 + dk / 2) / 2
        floor = None
        for t in np.arange(surf, surf + 12.0, 0.05):
            if _frac(host_inside, _ring(at, a, u, v, t + 0.025, rf)) >= 0.5:
                floor = float(t)
                break
        out["cbore_depth"] = None if floor is None else floor - surf
    if style == "csk":
        # head cone: top radius dk/2 at t=0, 90 deg (or recorded angle), down to d/2
        ang = np.radians(hole.get("csk_angle", 90.0) / 2)
        h = (dk / 2 - s.d / 2) / np.tan(ang)
        clash, bear = [], []
        for t in np.linspace(0.15 * h, 0.85 * h, 5):
            r = dk / 2 - t * np.tan(ang)
            nrm = 0.2 / np.cos(ang)
            clash.append(_ring(at, a, u, v, t, max(r - nrm, 0.05)))
            bear.append(_ring(at, a, u, v, t, r + nrm + 0.15))
        out["head_clash"] = _frac(host_inside, np.vstack(clash))
        out["head_bearing"] = _frac(host_inside, np.vstack(bear))
    else:
        clash = [_ring(at, a, u, v, -t, rr) for t in np.linspace(0.15, k - 0.1, 4) for rr in (dk / 2 - 0.15, dk / 4)]
        out["head_clash"] = _frac(host_inside, np.vstack(clash))
        out["head_bearing"] = _frac(host_inside, _ring(at, a, u, v, 0.15, (c / 2 + dk / 2) / 2, 16))
    into = hole.get("into")
    th = thread_inside or host_inside
    if into == "tapped" or (thread_inside is not None and into is None):
        tap = hole.get("tap_d") or fc.tap_drill(s.d)
        tip = s.length if style == "csk" else s.length
        t0 = (hole.get("grip") or 0.0) + 0.3
        ts2 = np.linspace(t0, tip - 0.3, 6) if tip - 0.3 > t0 else np.array([t0])
        out["thread_bite"] = _frac(th, np.vstack([_ring(at, a, u, v, t, (tap / 2 + s.d / 2) / 2) for t in ts2]))
        out["pilot_open"] = 1.0 - _frac(th, np.vstack([_ring(at, a, u, v, t, max(tap / 2 - 0.25, 0.05), 6) for t in ts2]))
    if into == "insert":
        ib, il = hole.get("insert_d"), hole.get("insert_len")
        g0 = hole.get("grip") or 0.0
        out["insert_open"] = 1.0 - _frac(th, np.vstack([_ring(at, a, u, v, t, ib / 2 - 0.15, 6)
                                                        for t in np.linspace(g0 + 0.3, g0 + il, 4)]))
        out["insert_wall"] = _frac(th, np.vstack([_ring(at, a, u, v, t, ib / 2 + 0.3, 6)
                                                  for t in np.linspace(g0 + 0.3, g0 + il, 4)]))
    if into == "nut":
        sf, m = hole.get("nut_af"), hole.get("nut_m")
        z = (hole.get("nut_z") or 0.0) + m / 2
        out["nut_open"] = 1.0 - _frac(th, _ring(at, a, u, v, z, sf / 2 - 0.15, 6))
        out["nut_held"] = _frac(th, _ring(at, a, u, v, z, sf / 2 + 0.35, 6) if hole.get("nut_fit") == "press"
                                else _ring(at, a, u, v, z, sf / np.sqrt(3) + 0.6, 6))
    return out


def judge(f, m: dict) -> list:
    """[(check id, ok, recorded, message)] for one probe result. `recorded` = the fastener carries a `hole` record."""
    g = lambda k, dflt=None: (f.get(k, dflt) if isinstance(f, dict) else getattr(f, k, dflt))  # noqa: E731
    hole = g("hole") or (getattr(f, "_extra", {}) or {}).get("hole") or {}
    rec = bool(hole)
    fid = g("id", "?")
    rows = []
    st = m["style"]
    s = m["surface_t"]
    if st == "csk":
        want = -(hole.get("sink") or 0.0)
        good = s is not None and abs(s - want) <= FLUSH_TOL
        rows.append(("csk_flush", good, rec,
                     f"`{fid}` countersunk head top is {'no surface found' if s is None else f'{-s:+.2f} mm from the surface'}"
                     f" (want {-want:+.2f} mm, tol {FLUSH_TOL})"))
    else:
        got = m.get("cbore_depth")
        if rec and "cbore_depth" in hole:
            want = hole["cbore_depth"]
            good = got is not None and abs(got - want) <= FLUSH_TOL
            rows.append(("cbore_depth", good, rec,
                         f"`{fid}` counterbore floor {'not found' if got is None else f'{got:.2f} mm'} below the surface "
                         f"(recorded {want:.2f} mm)"))
    rows.append(("head_clash", m["head_clash"] <= 0.05, rec,
                 f"`{fid}` head envelope is {m['head_clash'] * 100:.0f}% inside material (recess too small or wrong place)"))
    rows.append(("head_bearing", m["head_bearing"] >= 0.6, rec,
                 f"`{fid}` head bears on {m['head_bearing'] * 100:.0f}% of its seat"))
    if "thread_bite" in m:
        rows.append(("thread_bite", m["thread_bite"] >= 0.6, rec,
                     f"`{fid}` thread bites material on {m['thread_bite'] * 100:.0f}% of the engagement"))
        rows.append(("pilot_open", m["pilot_open"] >= 0.8, rec,
                     f"`{fid}` tap-drill pilot is {m['pilot_open'] * 100:.0f}% open"))
    if "insert_open" in m:
        rows.append(("insert_bore", m["insert_open"] >= 0.8 and m["insert_wall"] >= 0.6, rec,
                     f"`{fid}` insert bore {m['insert_open'] * 100:.0f}% open, wall {m['insert_wall'] * 100:.0f}% present"))
    if "nut_open" in m:
        rows.append(("nut_pocket", m["nut_open"] >= 0.8 and m["nut_held"] >= 0.6, rec,
                     f"`{fid}` nut pocket {m['nut_open'] * 100:.0f}% open inside the flats, walls {m['nut_held'] * 100:.0f}% present"))
    return rows
