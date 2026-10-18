"""Rules of the event: size, switch, failsafe, weapon controls (port of legal.rs)."""

from __future__ import annotations

import numpy as np
import shapely

from .. import catalog, measure, xform
from ..finding import BLOCKER, WARNING, fail, ok

G = "legal"
SPINS = ("spinner", "drum", "disc", "bar")


def footprint_mm(world) -> float:
    """Smallest square (any rotation about Z) that holds every vertex of every solid body."""
    pts = [b.mesh.vertices for b in world.bodies if not b.is_wire]
    if not pts:
        return 0.0
    return measure.footprint_mm(np.vstack(pts))


def run(ctx):
    r = ctx.r
    out = controls(ctx) + weapons(ctx)
    limit = r.profile.footprint_mm
    fp = footprint_mm(ctx.world)
    ctx.metrics["footprint_mm"] = fp
    if fp > limit:
        out.append(fail("legal.footprint", G, BLOCKER, "Robot does not fit the square",
                        f"Smallest square that holds the robot is {fp:.1f} mm; the limit is {limit:.0f} mm with no overhang at any height.")
                   .expect(f"<= {limit:.0f} mm", f"{fp:.1f} mm").fix("Shorten the wedge, narrow the wheels or move parts inward."))
    else:
        out.append(ok("legal.footprint", G, "Fits the square", f"Fits a {fp:.1f} mm square (limit {limit:.0f} mm)."))
    return out


def colour_dist(a, b) -> float:
    return float(np.sqrt(sum((float(x) - float(y)) ** 2 for x, y in zip(a, b))))


def controls(ctx):
    r = ctx.r
    out = []
    switches = [p for p in r.spec.parts if p.kind == "switch"]
    if r.profile.require_tool_free_switch:
        s = next((s for s in switches if s.tool_free and s.marked), None)
        if s is not None:
            out.append(ok("legal.switch", G, "Marked tool-free power switch", f"`{s.id}` is a marked, tool-free power switch."))
        else:
            out.append(fail("legal.switch", G, BLOCKER, "No tool-free marked power switch",
                            "Rule 4a needs an externally accessible way to shut down that works without tools and is clearly marked on/off.")
                       .fix("Add a `switch` part (or removable link) with `tool_free: true` and `marked: true` and a visible ON/OFF `label`."))
    out += switch_safety(ctx)
    if r.spec.electronics.failsafe:
        out.append(ok("legal.failsafe", G, "Failsafe declared", "The robot stops when the transmitter is switched off."))
    else:
        out.append(fail("legal.failsafe", G, BLOCKER, "Failsafe not declared",
                        "Rule 4d: the robot must stop all motion when the transmitter is off.")
                   .fix("Set `electronics.failsafe` to true and configure the receiver and ESC failsafe."))
    armed = r.spec.is_spinner or any(p.weapon is not None and p.weapon.kind not in ("none", "wedge") for p in r.spec.parts)
    if armed:
        if r.spec.electronics.weapon_remote_disable:
            out.append(ok("legal.weapon_disable", G, "Weapon can be disabled remotely", "The weapon is switched off from the transmitter."))
        else:
            out.append(fail("legal.weapon_disable", G, BLOCKER, "Weapon cannot be disabled remotely",
                            "Rule 4c: all weaponry must be deactivatable by remote control.")
                       .fix("Set `electronics.weapon_remote_disable` and put the weapon on its own receiver channel."))
    for p in r.spec.parts:
        if p.sharp and p.cover is None:
            out.append(fail("legal.sharp_cover", G, BLOCKER, "Sharp edge has no cover", f"`{p.id}` is marked sharp but has no protective cover.")
                       .on(p.id).fix("Name the cover in `cover` (a clearly visible guard fitted outside the arena)."))
    return out


def weapons(ctx):
    r, w = ctx.r, ctx.world
    out = []
    for rp in r.parts:
        p = rp.part
        if p.kind != "weapon":
            continue
        wd = p.weapon
        if wd is None:
            out.append(fail("legal.weapon_def", G, BLOCKER, "Weapon has no definition",
                            f"`{p.id}` is a weapon but has no `weapon` block (kind, motor, reduction).").on(p.id))
            continue
        m = catalog.material(p.material)
        if m is not None:
            if m.brittle:
                out.append(fail("legal.weapon_brittle", G, BLOCKER, "Weapon material shatters",
                                f"`{p.id}` is {p.material or '?'} which is brittle; a weapon that shatters sends fragments into the arena and is not allowed.")
                           .on(p.id).fix("Use steel, titanium, hardened tool steel or AR400 for a spinner."))
            if m.cls in ("printed", "elastomer", "tape") and wd.kind in SPINS:
                out.append(fail("legal.weapon_soft", G, WARNING, "Weapon is a soft plastic",
                                f"`{p.id}` is a printed or elastomer spinner; it will deform in the first hit and carry almost no energy.").on(p.id))
        if not (r.profile.require_locking_bar and wd.kind in SPINS):
            continue
        bar = r.spec.part(wd.locking_bar) if wd.locking_bar else None
        lock = (getattr(r.spec, "raw", None) or {}).get("weapon_lock")
        if bar is None and isinstance(lock, dict) and lock.get("type") == "removable_pin":
            out += pin_lock(r, w, p, lock)
            continue
        if bar is None:
            out.append(fail("legal.locking_bar", G, BLOCKER, "No locking bar",
                            "Rule 5f: every spinner needs a locking bar that physically stops the weapon from turning.")
                       .on(p.id).fix("Add a `locking_bar` part (a pin through the weapon into the frame), name it in `weapon.locking_bar`, give it a contrasting colour and `tethered: true`."))
            continue
        chassis = next((b.color for b in w.bodies if b.part_idx is not None and r.parts[b.part_idx].part.kind == "structure"), [60, 60, 60])
        bb = w.body(bar.id)
        barc = bb.color if bb is not None else [0, 0, 0]
        if colour_dist(chassis, barc) < 140.0:
            out.append(fail("legal.locking_bar_colour", G, WARNING, "Locking bar is hard to see",
                            f"`{bar.id}` is too close in colour to the chassis; the rule wants a contrasting colour.")
                       .on(bar.id).fix("Colour it bright red or orange against a dark chassis."))
        if not bar.tethered:
            out.append(fail("legal.locking_bar_tether", G, WARNING, "Locking bar can be lost",
                            f"`{bar.id}` is not tethered; it must be fixed so it cannot be accidentally removed or lost.")
                       .on(bar.id).fix("Set `tethered: true` and describe the lanyard in a connection."))
        wb = w.body(p.id)
        blocks = False
        if wb is not None and bb is not None:
            o = measure.overlap(wb, bb, cap=0.05)
            blocks = bool(o and o.depth > 0.05) or measure.min_gap(wb, bb, 0.4) < 0.3
        if not blocks:
            out.append(fail("legal.locking_bar_blocks", G, BLOCKER, "Locking bar does not touch the weapon",
                            f"`{bar.id}` does not reach `{p.id}`, so it cannot hold it still.")
                       .on(bar.id, p.id).fix("Move the pin so it passes through a hole in the weapon or sits against a tooth."))
    return out


PIN_R = 1.0  # smallest pin radius a hole must pass (2 mm pin)


def _section(b, at, axis, u, v):
    """Cross-section of body `b` on the plane through `at` normal to `axis`, in (u, v): (material, material with holes filled)."""
    from trimesh.intersections import mesh_plane

    seg = mesh_plane(b.mesh, axis, at)
    if seg is None or not len(seg):
        return None, None
    seg = np.round(np.stack([(seg - at) @ u, (seg - at) @ v], axis=-1), 5)
    lines = [shapely.union_all(shapely.linestrings(seg))]
    polys = list(shapely.get_parts(shapely.polygonize(lines)))
    if not polys:
        return None, None
    rp = np.array([q.representative_point().coords[0] for q in polys])
    solid = b.inside(at + np.outer(rp[:, 0], u) + np.outer(rp[:, 1], v))  # faces of the partition that are material
    if not solid.any():
        return None, None
    mat = shapely.union_all([q for q, k in zip(polys, solid) if k])
    filled = shapely.union_all(polys)
    return mat, filled


def pin_lock(r, w, p, lock):
    """Rule 5f via a declared removable pin (`weapon_lock: {type: removable_pin, holes: [ids]}`): the pin itself is not
    modelled, but the named parts must have one through-hole, parallel to the spin axis, that lines up across the static
    parts and the weapon in the modelled pose."""
    from .power import spin_axis

    ids = [x for x in (lock.get("holes") or []) if isinstance(x, str)]
    i = w.index(p.id)
    sa = spin_axis(w, r, i) if i is not None else None
    bodies = {x: w.body(x) for x in ids}
    rot = {p.id} | {q.id for q in r.spec.parts if getattr(q, "parent", None) == p.id}
    missing = [x for x, b in bodies.items() if b is None]
    if sa is None or missing or not any(x in rot for x in ids) or all(x in rot for x in ids):
        why = (f"unknown part(s) {', '.join(f'`{x}`' for x in missing)}" if missing else
               "no spin axis for the weapon" if sa is None else
               "`holes` must name the weapon (or a part on it) and at least one static part")
        return [fail("legal.locking_bar", G, BLOCKER, "Weapon lock declaration is incomplete", f"`{p.id}`: {why}.")
                .on(p.id, *ids).fix("Set `weapon_lock: {type: removable_pin, holes: [<weapon>, <upright>, ...]}` naming parts that the pin passes through.")]
    origin, axis = sa
    u = np.cross(axis, [1.0, 0.0, 0.0] if abs(axis[0]) < 0.9 else [0.0, 1.0, 0.0])
    u /= np.linalg.norm(u)
    v = np.cross(axis, u)
    wb = w.body(p.id)
    q = wb.mesh.vertices - origin
    R = float(np.linalg.norm(q - np.outer(q @ axis, axis), axis=1).max())
    g = np.arange(-R, R + 0.01, 0.25)
    G2 = np.array([(x, y) for x in g for y in g])
    ok_ = np.hypot(G2[:, 0], G2[:, 1]) >= 2 * PIN_R + 1.0  # off the spin axis, or the pin does not stop it turning
    for x, b in bodies.items():
        t = (b.mesh.vertices - origin) @ axis
        for tt in np.linspace(float(t.min()) + 0.15, float(t.max()) - 0.15, 3):  # a hole all the way through
            mat, filled = _section(b, origin + tt * axis, axis, u, v)
            if mat is None:
                ok_[:] = False
                break
            idx = np.nonzero(ok_)[0]
            P = G2[idx]
            inside = shapely.contains_xy(filled, P[:, 0], P[:, 1])  # surrounded by material ...
            near = shapely.dwithin(mat, shapely.points(P), PIN_R)  # ... yet a pin's width of clear space
            ok_[idx[~inside | near]] = False
        if not ok_.any():
            break
    C = origin + np.outer(G2[:, 0], u) + np.outer(G2[:, 1], v)
    if not ok_.any():
        return [fail("legal.locking_bar", G, BLOCKER, "Weapon lock holes do not line up",
                     f"No {2 * PIN_R:.0f} mm through-hole parallel to the spin axis passes through all of {', '.join(f'`{x}`' for x in ids)} in the modelled pose.")
                .on(p.id, *ids).fix("Drill one hole on a common line through the weapon and the uprights (pin parallel to the spin axis).")]
    c = C[int(np.argmax(ok_))]
    return [ok("legal.locking_bar", G, "Removable weapon pin declared",
               f"`{p.id}`: a pin hole lines up through {', '.join(f'`{x}`' for x in ids)} at {np.round(c, 1).tolist()}.")]


def switch_safety(ctx):
    """The power switch must not be toggled by the robot's own motion or by landing on it upside down."""
    r, w = ctx.r, ctx.world
    out = []
    for rp in r.parts:
        p = rp.part
        if p.kind != "switch":
            continue
        i = w.index(p.id)
        if i is None:
            ctx.not_checked.append(f"Switch `{p.id}` orientation and recess: it has no body in the world")
            continue
        b = w.bodies[i]
        local = np.asarray(p.actuation, float) if p.actuation is not None else np.array([1.0, 0.0, 0.0])
        axis = xform.norm(xform.apply_dir(b.M, local))
        ay, az = abs(axis[1]), abs(axis[2])
        if az > 0.7:
            out.append(fail("switch.vertical_axis", G, BLOCKER, "Switch slides up and down",
                            f"`{p.id}` moves along the vertical axis: when the robot is flipped, or lands hard, gravity and impact slide it to OFF.")
                       .on(p.id).fix("Turn the switch so it slides sideways (along the robot's x axis), or use a rocker or a removable link."))
        elif ay > 0.7:
            out.append(fail("switch.drive_axis", G, WARNING, "Switch slides along the drive direction",
                            f"`{p.id}` moves forward and back: hard acceleration, braking and head-on hits push the slider.")
                       .on(p.id).fix("Orient the slider across the robot (x axis), or add a detent plus a guard rib on both ends."))
        # Recess: highest surface of other parts around the switch, by downward rays.
        lo, hi = b.aabb
        c = (lo + hi) / 2
        top = hi[2]
        others = [o for j, o in enumerate(w.bodies) if j != i and not o.is_wire and o.part_idx is not None]
        offs = [(7.5, 0.0), (-7.5, 0.0), (0.0, 5.0), (0.0, -5.0), (7.5, 5.0), (-7.5, -5.0)]
        origins = np.array([[c[0] + dx, c[1] + dy, top + 6.0] for dx, dy in offs])
        around = -np.inf
        start_in = measure.inside_any(others, origins)
        dist, _ = measure.Scene(others).first_hit(origins, np.tile([0.0, 0.0, -1.0], (len(origins), 1)))
        for k in range(len(origins)):
            if start_in[k]:
                around = max(around, origins[k, 2])
            elif np.isfinite(dist[k]) and origins[k, 2] - dist[k] > lo[2]:
                around = max(around, origins[k, 2] - dist[k])
        if not np.isfinite(around):
            ctx.not_checked.append(f"Switch `{p.id}` recess: no surrounding surface found next to it")
            continue
        recess = around - top
        if recess < 0.3:
            out.append(fail("switch.exposed", G, WARNING, "Switch is not recessed",
                            f"`{p.id}` stands {abs(recess):.1f} mm {'above' if recess < 0 else 'level with'} the surrounding surface; landing on that face or a hit will flip it off.")
                       .on(p.id).here(c).fix("Sink it at least 1 mm below the surface inside a pocket with raised walls on both sides, leaving finger access."))
        elif recess > 4.0:
            out.append(fail("switch.too_deep", G, WARNING, "Switch is buried",
                            f"`{p.id}` is {recess:.1f} mm below the surface; a finger cannot move the slider without a tool.").on(p.id).here(c))
        else:
            out.append(ok("switch.recess", G, "Switch is recessed",
                          f"`{p.id}` sits {recess:.1f} mm below the surrounding surface and slides across the robot."))
    return out
