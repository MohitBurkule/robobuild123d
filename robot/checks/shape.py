"""Silhouette and layout: proportions, profile height, what leads at the front, how low a vertical weapon sweeps, and how
much of the top and sides is covered by armour rather than exposed internals (ray casting)."""

from __future__ import annotations

import numpy as np

from .. import measure
from ..finding import WARNING, fail, note, ok
from . import _physics as ph

G = "shape"
MAX_H_OVER_W = 0.7  # taller than this against the track width: tips on a shove, big target
LW_RANGE = (0.45, 2.2)  # length over width outside this turns badly or spins out
LEAD_TOL_MM = 3.0  # a declared wedgelet or fork may sit this far ahead of the weapon tip
FLOOR_REACH_MM = 4.0  # a vertical spinner's sweep must come this close to the floor to hit wedges and low robots
PROTECTIVE = ("armor", "structure", "plate", "wedge", "fork", "weapon", "shaft", "bearing", "locking_bar", "wheel", "tyre", "other")
INTERNAL = ("battery", "esc", "receiver", "motor", "weapon_motor", "servo", "pcb", "wire")
TOP_COVER_MIN, SIDE_COVER_MIN = 0.95, 0.90
RAY_STEP_MM = 2.0


def run(ctx):
    w = ctx.world
    out = []
    S = ph.solids(w)
    if not S:
        ctx.not_checked.append("Shape: no solid bodies")
        return out
    floor = ph.floor_z(ctx)
    lo = np.min([b.aabb[0] for b in S], axis=0)
    hi = np.max([b.aabb[1] for b in S], axis=0)
    width, length, height = hi[0] - lo[0], hi[1] - lo[1], hi[2] - floor
    ctx.metrics.update({"shape_width_mm": float(width), "shape_length_mm": float(length), "shape_height_mm": float(height)})
    out += proportions(ctx, S, floor, width, length, height)
    out += weapon_leads(ctx, S)
    out += weapon_floor_reach(ctx, floor)
    out += armour_coverage(ctx, S, lo, hi, floor)
    return out


def proportions(ctx, S, floor, width, length, height):
    out = []
    spinner = ctx.r.spec.is_spinner
    # The profile without the weapon: a vertical disc stands proud on purpose.
    body = [b for b in S if b.kind != "weapon"]
    prof = (max(float(b.aabb[1][2]) for b in body) - floor) if body else height
    ctx.metrics["profile_height_mm"] = prof
    hw, lw = prof / max(width, 1e-6), length / max(width, 1e-6)
    ctx.metrics["h_over_w"], ctx.metrics["l_over_w"] = hw, lw
    if hw > MAX_H_OVER_W:
        out.append(fail("shape.tall", G, WARNING, "Robot is tall for its width",
                        f"Body height {prof:.1f} mm over width {width:.1f} mm is {hw:.2f} (limit {MAX_H_OVER_W}); it tips on a side "
                        "shove and gives opponents a tall face to hit.").expect(f"<= {MAX_H_OVER_W}", f"{hw:.2f}")
                   .fix("Lay the battery and electronics flat, widen the track, or lower the top plate."))
    else:
        out.append(ok("shape.tall", G, "Low profile", f"Body height {prof:.1f} mm over width {width:.1f} mm = {hw:.2f}"
                      f"{' (weapon excluded)' if spinner else ''}."))
    if not LW_RANGE[0] <= lw <= LW_RANGE[1]:
        out.append(fail("shape.aspect", G, WARNING, "Odd length to width ratio",
                        f"Length {length:.1f} mm over width {width:.1f} mm is {lw:.2f}; outside {LW_RANGE[0]} to {LW_RANGE[1]} the robot "
                        "either will not drive straight or will not turn.").expect(f"{LW_RANGE[0]} to {LW_RANGE[1]}", f"{lw:.2f}"))
    else:
        out.append(ok("shape.aspect", G, "Length to width is reasonable", f"L/W = {lw:.2f}."))
    return out


def weapon_leads(ctx, S):
    """The weapon (or the wedge on a wedge robot) must be the first thing an opponent meets at the front."""
    out = []
    spec = ctx.r.spec
    front = lambda b: float(b.mesh.vertices[:, 1].max())  # noqa: E731
    if spec.is_spinner:
        ws = ph.weapons(ctx)
        if not ws:
            ctx.not_checked.append("Weapon lead: spinner with no weapon body or spin axis")
            return out
        tip = max(front(wb) for _, wb, _, _ in ws)
        lead_ids = {wb.id for _, wb, _, _ in ws}
        allowed = ("wedge", "fork")
        tol = LEAD_TOL_MM
        what = "weapon tip"
    elif spec.robot_type == "wedge":
        wedges = [b for b in S if b.kind in ("wedge", "fork")]
        if not wedges:
            out.append(fail("shape.weapon_leads", G, WARNING, "Wedge robot has no wedge",
                            "`robot_type` is wedge but no part has kind `wedge` or `fork`."))
            return out
        tip = max(front(b) for b in wedges)
        lead_ids = {b.id for b in wedges}
        allowed, tol, what = (), 0.5, "wedge edge"
    else:
        out.append(note("shape.weapon_leads", G, "Front lead not judged", f"No front-lead rule for `{spec.robot_type}`."))
        return out
    ctx.metrics["front_tip_y_mm"] = tip
    ahead = []
    for b in S:
        if b.id in lead_ids or b.fastener:
            continue
        lim = tip + (tol if b.kind in allowed else 0.5)
        f = front(b)
        if f > lim:
            ahead.append((b, f - tip))
    if ahead:
        ahead.sort(key=lambda x: -x[1])
        b, d = ahead[0]
        p = b.mesh.vertices[np.argmax(b.mesh.vertices[:, 1])]
        out.append(fail("shape.weapon_leads", G, WARNING, f"Something sits ahead of the {what}",
                        f"{', '.join(f'`{x.id}` ({dd:.1f} mm)' for x, dd in ahead[:5])} reach further forward than the {what}; an "
                        "opponent meets that first instead of the weapon.").on(*[x.id for x, _ in ahead[:5]]).here(p)
                   .expect(f"nothing ahead (wedgelets/forks up to {tol:.1f} mm)", f"`{b.id}` {d:.1f} mm ahead")
                   .fix("Pull the part back behind the weapon line, or move the weapon forward."))
    else:
        out.append(ok("shape.weapon_leads", G, f"The {what} leads", f"Nothing reaches further forward than the {what}."))
    return out


def weapon_floor_reach(ctx, floor):
    out = []
    if ctx.r.spec.robot_type not in ("vertical_spinner", "drum"):
        return out
    for p, wb, origin, axis in ph.weapons(ctx):
        r = float(ph.perp_radius(wb.mesh.vertices, origin, axis).max())
        # Lowest point of the swept circle: the axle height minus the rim radius times the horizontal share of the axis.
        low = float(origin[2]) - r * float(np.sqrt(max(1.0 - axis[2] ** 2, 0.0)))
        gap = low - floor
        ctx.metrics[f"weapon_axle_height_mm.{p.id}"] = float(origin[2]) - floor
        ctx.metrics[f"weapon_sweep_low_mm.{p.id}"] = gap
        if gap > FLOOR_REACH_MM:
            out.append(fail("shape.weapon_floor_reach", G, WARNING, "Weapon does not sweep near the floor",
                            f"`{p.id}` axle is {origin[2] - floor:.1f} mm up with a {r:.1f} mm rim, so its lowest sweep is {gap:.1f} mm above "
                            f"the floor (need <= {FLOOR_REACH_MM:.0f}); wedges and low robots pass underneath.").on(p.id)
                       .expect(f"<= {FLOOR_REACH_MM:.0f} mm", f"{gap:.1f} mm").fix("Lower the axle or use a bigger disc."))
        else:
            out.append(ok("shape.weapon_floor_reach", G, "Weapon sweeps close to the floor",
                          f"`{p.id}` lowest sweep is {gap:.1f} mm above the floor (axle {origin[2] - floor:.1f} mm, rim {r:.1f} mm)."))
    return out


def _cover(scene, kinds, O, D):
    _, who = scene.first_hit(O, D)
    hit = who >= 0
    if not hit.any():
        return None, {}
    k = np.array([kinds[i] for i in who[hit]])
    bad = np.isin(k, INTERNAL)
    exposed = {}
    for i in who[hit][bad]:
        exposed[scene.bodies[i].id] = exposed.get(scene.bodies[i].id, 0) + 1
    return 1.0 - bad.mean(), {b: n / hit.sum() for b, n in exposed.items()}


def armour_coverage(ctx, S, lo, hi, floor):
    """Share of the robot's silhouette, seen from above and from the four sides, whose first surface is armour or structure
    and not a battery, ESC, receiver, motor or wire."""
    out = []
    bodies = [b for b in S if not (b.part_idx is not None and ph.part(ctx, b).kind == "switch")]
    wires = [b for b in ctx.world.bodies if b.is_wire]
    scene = measure.Scene(bodies + wires)
    kinds = [("wire" if b.is_wire else b.kind) for b in scene.bodies]
    h = RAY_STEP_MM
    xs, ys = np.arange(lo[0] + h / 2, hi[0], h), np.arange(lo[1] + h / 2, hi[1], h)
    zs = np.arange(floor + 1.0 + h / 2, hi[2], h)
    X, Y = np.meshgrid(xs, ys)
    top_O = np.c_[X.ravel(), Y.ravel(), np.full(X.size, hi[2] + 5)]
    res = {}
    res["top"] = _cover(scene, kinds, top_O, np.tile([0, 0, -1.0], (len(top_O), 1)))
    for name, ax, sgn in (("front", 1, 1), ("back", 1, -1), ("left", 0, -1), ("right", 0, 1)):
        other = xs if ax == 1 else ys
        A, Z = np.meshgrid(other, zs)
        O = np.zeros((A.size, 3))
        O[:, 1 - ax] = A.ravel()
        O[:, 2] = Z.ravel()
        O[:, ax] = (hi[ax] + 5) if sgn > 0 else (lo[ax] - 5)
        d = np.zeros(3)
        d[ax] = -sgn
        res[name] = _cover(scene, kinds, O, np.tile(d, (len(O), 1)))
    for side, (cov, exposed) in res.items():
        if cov is None:
            continue
        ctx.metrics[f"armour_cover_{side}"] = float(cov)
        need = TOP_COVER_MIN if side == "top" else SIDE_COVER_MIN
        if cov < need:
            worst = sorted(exposed.items(), key=lambda x: -x[1])[:4]
            out.append(fail("shape.armour_coverage", G, WARNING, f"Internals exposed from the {side}",
                            f"Only {cov * 100:.0f}% of the {side} view is covered (need {need * 100:.0f}%); exposed: "
                            + ", ".join(f"`{b}` {f * 100:.0f}%" for b, f in worst) + ".")
                       .on(*[b for b, _ in worst]).expect(f">= {need * 100:.0f}%", f"{cov * 100:.0f}%")
                       .fix("Extend the top plate or side walls over these parts."))
    if not any(c is not None and c < (TOP_COVER_MIN if s == "top" else SIDE_COVER_MIN) for s, (c, _) in res.items()):
        out.append(ok("shape.armour_coverage", G, "Internals are covered",
                      ", ".join(f"{s} {c * 100:.0f}%" for s, (c, _) in res.items() if c is not None) + " of the view is armour or structure."))
    return out
