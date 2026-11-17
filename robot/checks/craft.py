"""Craft: what an experienced robot CAD designer rejects at a glance in a render (rated 7-10/10 bad, 2026-11-17).

  craft.stray_part   - a part hangs below the floor or far outside the body (a misplaced shaft/pole): BLOCKER.
  craft.brick        - a printed structure part fills most of its box: a solid brick, not a shelled, ribbed part.
  craft.sharp_edges  - most outside edges of a structure part are sharp 90 deg corners (no fillet/chamfer design).
  craft.weapon_scale - the spinning weapon is small next to the body (weapon robots are built round the weapon).
  craft.flat_slab    - a big flat face with no relief (lid/panel/wedge) thicker than it needs to be.
Every finding says what to change; thresholds are the designer's rules of thumb, made measurable.
"""

from __future__ import annotations

import numpy as np

from ..finding import BLOCKER, WARNING, fail, ok
from . import _physics as ph

G = "craft"
STRAY_BELOW_MM = 0.5
STRAY_OUT_MM = 15.0
BRICK_FILL = 0.6  # volume / bounding box of a printed structure part
BRICK_MIN_DIM = 8.0  # thinner parts (plates) are judged by flat_slab instead
SHARP_FRAC = 0.6  # share of convex outside edge length that is a sharp (>= 60 deg) corner
SHARP_DEG = 60.0
WEAPON_SCALE = 0.6  # weapon swept diameter / body width
SLAB_T_MM = 3.0  # flat panels thicker than this with no pocket/rib look like blocks
SLAB_AREA_MM2 = 1500.0
STRUCT_KINDS = ("structure", "chassis", "tub", "panel", "lid", "wedge", "mount", "armour", "armor")


def _structs(w):
    return [b for b in w.bodies if not b.is_wire and not b.fastener and b.kind in STRUCT_KINDS]


def stray(ctx, floor):
    w = ctx.world
    st = _structs(w)
    if not st:
        return []
    lo = np.min([b.aabb[0] for b in st], axis=0)
    hi = np.max([b.aabb[1] for b in st], axis=0)
    out = []
    for b in w.bodies:
        if b.is_wire:
            continue
        below = floor - float(b.aabb[0][2])
        outside = max(float(lo[0] - b.aabb[0][0]), float(b.aabb[1][0] - hi[0]), float(lo[1] - b.aabb[0][1]),
                      float(b.aabb[1][1] - hi[1]), 0.0)
        if b.kind in ("weapon", "wheel", "tyre", "wedge", "fork", "skid", "caster"):
            outside = 0.0  # these lead or stick out by design
        if below > STRAY_BELOW_MM or outside > STRAY_OUT_MM:
            what = f"{below:.1f} mm below the floor" if below > STRAY_BELOW_MM else f"{outside:.1f} mm outside the body"
            out.append(fail("craft.stray_part", G, BLOCKER, "Part hangs out of the robot",
                            f"`{b.id}` ({b.kind}) reaches {what}: a misplaced or wrong-length part (it reads as a CAD error in "
                            "every render).").on(b.id).here(b.center)
                       .fix("Check its `at`/`rot` and length; it must sit inside the body or on the floor."))
    return out


def brick(ctx):
    out = []
    for b in _structs(ctx.world):
        ext = b.aabb[1] - b.aabb[0]
        if min(ext) < BRICK_MIN_DIM:
            continue
        fill = float(b.geom.volume) / max(float(np.prod(ext)), 1e-9)
        ctx.metrics[f"craft_fill.{b.id}"] = fill
        if fill > BRICK_FILL:
            out.append(fail("craft.brick", G, WARNING, "Solid brick",
                            f"`{b.id}` fills {fill * 100:.0f}% of its {ext[0]:.0f} x {ext[1]:.0f} x {ext[2]:.0f} mm box: a designer "
                            "shells it to walls and ribs that follow the load paths.").on(b.id)
                       .expect(f"<= {BRICK_FILL * 100:.0f}%", f"{fill * 100:.0f}%")
                       .fix("Hollow it to 1.6-2.4 mm walls, add ribs only where loads run, pocket the rest."))
    return out


def sharp_edges(ctx):
    """Judged on the main body only (the biggest structure part): sheet plates are sharp-edged by nature, and Revron's
    tub (a designer's part) has 39% sharp silhouette edges while a block-out tub has ~100%."""
    out = []
    st = _structs(ctx.world)
    for b in sorted(st, key=lambda q: -float(q.geom.volume))[:1]:
        m = b.mesh
        try:
            ang = np.degrees(m.face_adjacency_angles)
            conv = m.face_adjacency_convex
            e = m.face_adjacency_edges
            ln = np.linalg.norm(m.vertices[e[:, 0]] - m.vertices[e[:, 1]], axis=1)
        except Exception:  # noqa: BLE001
            continue
        try:
            onhull = np.zeros(len(m.vertices), bool)
            hv = m.convex_hull.vertices
            from scipy.spatial import cKDTree
            d, _ = cKDTree(hv).query(m.vertices)
            onhull = d < 1e-3
        except Exception:  # noqa: BLE001
            continue
        outer = onhull[e[:, 0]] & onhull[e[:, 1]]  # silhouette edges: pockets and holes do not count
        feat = conv & (ang > 5.0) & outer
        tot = float(ln[feat].sum())
        if tot < 20.0:
            continue
        sharp = float(ln[feat & (ang >= SHARP_DEG)].sum()) / tot
        ctx.metrics[f"craft_sharp_frac.{b.id}"] = sharp
        if sharp > SHARP_FRAC:
            out.append(fail("craft.sharp_edges", G, WARNING, "Box corners everywhere",
                            f"{sharp * 100:.0f}% of `{b.id}`'s outside edge length is a sharp corner: it looks like a block "
                            "out, and sharp corners crack and catch opponents' teeth.").on(b.id)
                       .expect(f"<= {SHARP_FRAC * 100:.0f}%", f"{sharp * 100:.0f}%")
                       .fix("Fillet vertical outside corners (R >= 3 mm) and chamfer/fillet top edges (>= 1 mm)."))
    return out


def weapon_scale(ctx):
    out = []
    st = _structs(ctx.world)
    if not st:
        return out
    lo = np.min([b.aabb[0] for b in st], axis=0)
    hi = np.max([b.aabb[1] for b in st], axis=0)
    width = float(hi[0] - lo[0])
    for p, wb, origin, axis in ph.weapons(ctx):
        d = 2 * float(ph.perp_radius(wb.mesh.vertices, origin, axis).max())
        r = d / max(width, 1e-6)
        ctx.metrics[f"craft_weapon_scale.{p.id}"] = r
        if r < WEAPON_SCALE:
            out.append(fail("craft.weapon_scale", G, WARNING, "Weapon is small for the robot",
                            f"`{p.id}` sweeps {d:.0f} mm on a {width:.0f} mm wide body ({r:.2f}): the robot reads as a box with a "
                            "weapon added, not a weapon with a robot round it.").on(p.id)
                       .expect(f">= {WEAPON_SCALE:.2f}", f"{r:.2f}")
                       .fix("Size the body round the weapon: shrink the body or grow the weapon (mass budget allowing)."))
    return out


def flat_slab(ctx):
    out = []
    for b in _structs(ctx.world):
        ext = sorted(b.aabb[1] - b.aabb[0])
        t, a = float(ext[0]), float(ext[1] * ext[2])
        if t <= SLAB_T_MM or t >= BRICK_MIN_DIM or a < SLAB_AREA_MM2:
            continue
        fill = float(b.geom.volume) / max(t * a, 1e-9)
        if fill > 0.85:
            out.append(fail("craft.flat_slab", G, WARNING, "Thick flat slab",
                            f"`{b.id}` is a {t:.1f} mm solid plate over {ext[1]:.0f} x {ext[2]:.0f} mm ({fill * 100:.0f}% solid): "
                            "heavy and blocky.").on(b.id)
                       .fix("Use 1-2 mm sheet (metal/CF) or a thin printed skin with ribs under it; taper wedges to a sharp lip."))
    return out


def run(ctx):
    floor = ph.floor_z(ctx)
    out = []
    for f in (lambda: stray(ctx, floor), lambda: brick(ctx), lambda: sharp_edges(ctx), lambda: weapon_scale(ctx),
              lambda: flat_slab(ctx)):
        try:
            out += f()
        except Exception as e:  # noqa: BLE001
            ctx.not_checked.append(f"craft: {e}")
    if not out:
        out.append(ok("craft.clean", G, "Reads as a designed part set", "No stray parts, bricks, box corners or tiny weapon."))
    return out
