"""Screws: can the driver reach the head, does the thread bite enough, does the head sit on something (port of fasteners.rs)."""

from __future__ import annotations

import itertools
import re

import numpy as np

from .. import catalog
from ..cad import fastener_catalog
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


# Through-bolt into a standard hex nut: the nut height (ISO 4032 m ~ 0.8 d) is the engagement.
NUT_ENGAGEMENT_D = 0.8


def tool_key(tool: str):
    """Hex key size named by a `tool` like `hex2.5`, or None when the tool is not a sized hex key."""
    m = re.match(r"^hex([0-9.]+)$", str(tool or "").strip())
    try:
        return float(m.group(1)) if m else None
    except ValueError:
        return None


def drive_findings(ctx):
    """Every screw head is modelled with a drive recess and every nut is a true hexagon (so renders read as hardware and
    the tool-access check has a real socket size to use)."""
    from ..world import fastener_shape

    r = ctx.r
    out, n_s, n_n = [], 0, 0
    for f in r.spec.fasteners:
        dl = catalog.parse_designation(f.designation)
        if not dl:
            continue
        n_s += 1
        head = f.head if f.head in ("countersunk", "button") else None
        if not catalog.has_drive_recess(fastener_shape(*dl, head=head)):
            out.append(fail("fastener.drive", G, WARNING, "Screw head has no drive",
                            f"`{f.id}` ({f.designation}, {head or 'socket cap'} head) is modelled without a hex socket.").on(f.id)
                       .fix("Build heads with robot.world.fastener_shape, which cuts the ISO hex socket."))
    for rp in r.parts:
        if rp.part.kind != "nut":
            continue
        n_n += 1
        sh = rp.shape if rp.shape is not None else (rp.cat.shape if rp.cat else None)
        if isinstance(sh, dict) and sh.get("type") == "model":
            ctx.not_checked.append(f"Nut `{rp.part.id}`: shape is an imported model, hexagon not checked")
            continue
        if not catalog.is_hex_nut(sh):
            out.append(fail("fastener.nut_hex", G, WARNING, "Nut is not a hexagon",
                            f"`{rp.part.id}` is modelled as something other than a hexagonal prism with a through bore.").on(rp.part.id)
                       .fix("Use catalog.hex_nut(s, m, bore) (true hexagon, chamfered, bored) or a nut catalog entry."))
    if not out and (n_s or n_n):
        out.append(ok("fastener.drive", G, "Screws have drives, nuts are hexagons",
                      f"{n_s} screw heads carry a hex socket, {n_n} nuts are chamfered hexagons with a bore."))
    return out


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
        if f.head == "button":
            from ..world import button_dims
            dk, k = button_dims(d)
        dr = np.asarray(f.dir, float)
        dr = dr / np.linalg.norm(dr)
        at = np.asarray(f.at, float)
        own = w.body(f.id)
        before = set(getattr(f, "_extra", {}).get("access_before") or [])
        bad_before = [x for x in before if x in set(f.through or []) | ({f.threads_into} if f.threads_into else set()) or r.spec.part(x) is None]
        if bad_before:
            out.append(fail("fastener.access_order", G, BLOCKER, "Screw driven before parts it passes through",
                            f"`{f.id}` declares `access_before` {sorted(bad_before)}, but it passes through / threads into them (or they do not exist).")
                       .on(f.id, *[x for x in bad_before if r.spec.part(x) is not None]))
            before = set()
        elif before:
            out.append(ok("fastener.access_order", G, "Screw driven before later parts",
                          f"`{f.id}` is driven before {', '.join(sorted(before))} are fitted (declared order); those parts do not block its driver."))
        skip = lambda b: b is own or b.is_wire or b.id in before  # noqa: E731
        u, v = perp(dr)
        bad = False
        drv = fastener_catalog.drive_key(d, f.head if f.head in ("countersunk", "button") else None)[0]
        tk = tool_key(f.tool) if f.tool else None
        if f.tool and f.tool.strip() == "hex":  # unsized hex: use the modelled socket's key
            tk = drv
        if tk is not None and abs(tk - drv) > 1e-6:
            out.append(fail("fastener.drive_key", G, WARNING, "Driver does not fit the socket",
                            f"`{f.id}` lists {f.tool} but an {f.designation} {f.head or 'cap'} head has a {drv:g} mm hex socket.").on(f.id)
                       .fix(f"Set `tool` to hex{drv:g}."))
        if f.tool:
            rad = tool_radius(f"hex{tk:g}") if tk is not None else tool_radius(f.tool)
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
            tp = r.spec.part(t)
            if tp is not None and tp.kind == "nut":
                # A standard hex nut (height m ~ 0.8 d) is sized to strip after the bolt breaks: the whole nut is the
                # engagement. 1.5 d is for threads cut or inserted into the parent material.
                need = min(need, NUT_ENGAGEMENT_D * d, (phi - plo) - 0.05)   # a thin nut (DIN 439, 0.5 d) is fully engaged at its height
            if tp is not None and tp.kind in ("motor", "weapon_motor"):
                # Face screws into a motor's own threaded holes: the hole depth is set by the motor maker, so
                # arch.motor_face_bolts judges them (>= 0.8 d, <= the usable depth); 1.5 d would run into the windings.
                need = min(need, 0.8 * d)
            if engaged + 0.01 < need:
                bad = True
                out.append(fail("fastener.engagement", G, BLOCKER, "Screw does not bite enough thread",
                                f"`{f.id}` engages {engaged:.1f} mm in `{t}`; it needs at least {need:.1f} mm ({need / d:.1f} x diameter) or it will strip.")
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
    drive = drive_findings(ctx)
    if r.spec.fasteners and all(x.passed for x in out):
        out.append(ok("fastener.ok", G, "Screws are reachable and bite",
                      f"{good} screws: driver path clear, thread engagement enough, heads seated."))
    return out + drive
