"""Screws: can the driver reach the head, does the thread bite enough, does the head sit on something (port of fasteners.rs)."""

from __future__ import annotations

import itertools
import re

import numpy as np

from .. import catalog
from ..finding import BLOCKER, WARNING, fail, ok

G = "fasteners"


def tool_radius(tool: str) -> float:
    m = re.match(r"^[A-Za-z]*(.*)$", tool)
    try:
        size = float(m.group(1))
    except (ValueError, AttributeError):
        size = 1.5
    if tool.startswith("hex"):
        return size * 0.5 * 1.16 + 0.4
    if tool.startswith("torx"):
        return 1.5
    if tool.startswith("phillips"):
        return 1.7
    return 1.8


def perp(d):
    a = np.array([1.0, 0, 0]) if abs(d[0]) < 0.9 else np.array([0, 1.0, 0])
    u = np.cross(d, a)
    u /= np.linalg.norm(u)
    v = np.cross(d, u)
    return u, v / np.linalg.norm(v)


def _first_inside(bodies, P, skip):
    """(point index, body) of the first point (in order) inside any body; bodies in order break ties. None when clear."""
    best = None
    for b in bodies:
        if skip(b):
            continue
        ins = np.nonzero(b.inside(P))[0]
        if len(ins) and (best is None or ins[0] < best[0]):
            best = (int(ins[0]), b)
    return best


def run(ctx):
    r, w = ctx.r, ctx.world
    out, good = [], 0
    for f in r.spec.fasteners:
        dl = catalog.parse_designation(f.designation)
        if not dl:
            ctx.not_checked.append(f"Fastener `{f.id}`: designation `{f.designation}` not understood, access/engagement/seat not checked")
            continue
        d, ln = dl
        dk, k, _ = catalog.screw_dims(d)
        dr = np.asarray(f.dir, float)
        dr = dr / np.linalg.norm(dr)
        at = np.asarray(f.at, float)
        own = w.body(f.id)
        skip = lambda b: b is own or b.is_wire  # noqa: E731
        u, v = perp(dr)
        bad = False
        if f.tool:
            rad = tool_radius(f.tool)
            reach = r.profile.driver_access_len_mm
            top = at - dr * k
            pts, ts = [], []
            for s in range(int(reach / 0.5) + 1):
                t = s * 0.5
                c = top - dr * (t + 0.05)
                for a in range(8):
                    ang = a * np.pi / 4
                    pts.append(c if a == 0 else c + u * (rad * np.cos(ang)) + v * (rad * np.sin(ang)))
                    ts.append(t)
            hit = _first_inside(w.bodies, np.array(pts), skip)
            if hit is not None:
                bad = True
                t, bid = ts[hit[0]], hit[1].id
                out.append(fail("fastener.access", G, BLOCKER, "Screwdriver cannot reach the screw",
                                f"`{f.id}` ({f.tool}) is blocked by `{bid}` {t:.1f} mm above the head; the driver needs a clear {rad * 2:.1f} mm wide, {reach:.0f} mm long path straight out of the head.")
                           .on(f.id, bid).here(top - dr * t)
                           .fix("Open a straight access hole or move the screw out from under the overhang; counterbores need to be wider than the head."))
        else:
            out.append(fail("fastener.no_tool", G, WARNING, "Screw has no driver listed", f"`{f.id}` has no `tool`, so access cannot be checked.").on(f.id))
        tb = w.body(f.threads_into) if f.threads_into else None
        if tb is not None:
            t = f.threads_into
            lo, hi = float(at @ dr), float((at + dr * ln) @ dr)
            corners = np.array(list(itertools.product(*zip(tb.aabb[0], tb.aabb[1]))))
            cs = corners @ dr
            plo, phi = float(cs.min()), float(cs.max())
            engaged = max(min(hi, phi) - max(lo, plo), 0.0)
            need = r.profile.engagement_d * d
            if engaged + 0.01 < need:
                bad = True
                out.append(fail("fastener.engagement", G, BLOCKER, "Screw does not bite enough thread",
                                f"`{f.id}` engages {engaged:.1f} mm in `{t}`; it needs at least {need:.1f} mm (1.5 x diameter) or it will strip.")
                           .on(f.id, t).expect(f">= {need:.1f} mm", f"{engaged:.1f} mm")
                           .fix("Use a longer screw, a longer insert, or move the insert closer to the screw tip."))
            if hi > phi + 4.0:
                out.append(fail("fastener.too_long", G, WARNING, "Screw sticks out far past its nut",
                                f"`{f.id}` pokes {hi - phi:.1f} mm beyond `{t}`; it will catch on wires or the floor.").on(f.id, t))
        elif not f.threads_into and len(f.through) < 2:
            out.append(fail("fastener.no_thread", G, WARNING, "Screw holds nothing",
                            f"`{f.id}` has neither `threads_into` nor two `through` parts.").on(f.id))
        elif f.threads_into:
            ctx.not_checked.append(f"Fastener `{f.id}`: thread engagement not checked, `{f.threads_into}` is not a body")
        ring = np.array([at + dr * 0.15 + u * (dk * 0.36 * np.cos(a * np.pi / 4)) + v * (dk * 0.36 * np.sin(a * np.pi / 4))
                         for a in range(8)])
        if _first_inside(w.bodies, ring, skip) is None:
            bad = True
            out.append(fail("fastener.head_seat", G, WARNING, "Screw head sits on nothing",
                            f"Nothing is under the head of `{f.id}`; it cannot clamp the parts.").on(f.id).here(at)
                       .fix("Move `at` to the surface the head presses on, or cut a counterbore whose floor is at `at`."))
        if not bad:
            good += 1
    if r.spec.fasteners and all(x.passed for x in out):
        out.append(ok("fastener.ok", G, "Screws are reachable and bite",
                      f"{good} screws: driver path clear, thread engagement enough, heads seated."))
    return out
