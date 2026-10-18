"""Model validity: ids, references, shapes, units; and claims against measurements."""

from __future__ import annotations

from .. import catalog, shapes
from ..finding import BLOCKER, WARNING, fail, ok
from ..spec import finite
from ..world import parse_color

G = "validity"


def _prisms(s):
    if isinstance(s, dict):
        if s.get("type") in ("prism",) and isinstance(s.get("points"), list):
            yield s["points"]
        for v in s.values():
            yield from _prisms(v)
    elif isinstance(s, list):
        for v in s:
            yield from _prisms(v)


def run(r, out) -> bool:
    good = True
    sp = r.spec
    if not sp.parts:
        out.append(fail("validity.no_parts", G, BLOCKER, "No parts", "The spec has no parts.").fix("Add parts with a `shape` or a `catalog` id."))
        return False
    if len(sp.parts) > 300:
        out.append(fail("validity.too_many_parts", G, BLOCKER, "Too many parts", f"{len(sp.parts)} parts; the limit is 300."))
        return False
    for pid, e in r.load_errors:
        good = False
        out.append(fail("validity.load", G, BLOCKER, "Part could not be loaded", e).on(pid)
                   .fix("Use a valid catalog id (see `robot catalog`) or give a valid `shape` / `model`."))
    seen = set()
    for p in sp.parts:
        if not p.id or p.id in seen:
            good = False
            out.append(fail("validity.part_id", G, BLOCKER, "Part id missing or duplicated", f"id `{p.id}`").on(p.id)
                       .fix("Give every part a unique non-empty id."))
        seen.add(p.id)
        if p.material and catalog.density(p.material) is None:
            out.append(fail("validity.material", G, WARNING, "Unknown material", f"`{p.material}` has no density; mass cannot be computed.")
                       .on(p.id).fix("Use one of: " + ", ".join(catalog.MATERIAL_LIST) + "."))
        if p.color and parse_color(p.color) is None:
            out.append(fail("validity.color", G, WARNING, "Invalid colour", f"`{p.color}` is not `#rrggbb`.").on(p.id))
        if not (finite(p.at) and finite(p.rot)) or len(p.at) != 3 or len(p.rot) != 3:
            good = False
            out.append(fail("validity.pose", G, BLOCKER, "Non-finite pose", "at/rot must be 3 finite numbers each.").on(p.id))
        if p.catalog and (p.shape is not None or p.model):
            out.append(fail("validity.catalog_shape", G, WARNING, "Catalog part with its own shape",
                            "The catalog shape is used; the given `shape`/`model` is ignored.").on(p.id)
                       .fix("Remove `shape`, or drop `catalog` for a custom part."))
        for ref in (p.parent, p.fused_with, p.cover):
            if ref and sp.part(ref) is None:
                good = False
                out.append(fail("validity.ref", G, BLOCKER, "Reference to a missing part", f"`{p.id}` refers to `{ref}`").on(p.id))
        for pts in _prisms(p.shape):
            if shapes.self_intersecting(pts):
                out.append(fail("validity.self_intersecting", G, WARNING, "Prism outline crosses itself",
                                f"`{p.id}` has a prism outline whose edges cross; it was repaired by even-odd fill, which may not be what you meant.")
                           .on(p.id).fix("List the outline points in order around the edge without crossings."))
                break
    for f in sp.fasteners:
        if catalog.parse_designation(f.designation) is None:
            good = False
            out.append(fail("validity.fastener", G, BLOCKER, "Bad fastener designation", f"`{f.designation}` on `{f.id}`; use e.g. `M2x16`.")
                       .fix("Use the form M<d>x<length>."))
        try:
            d = sum(float(v) ** 2 for v in f.dir) ** 0.5
        except (TypeError, ValueError):
            d = 0
        if not (d > 1e-6 and d == d):
            good = False
            out.append(fail("validity.fastener_dir", G, BLOCKER, "Fastener has no direction", f"`{f.id}` has a zero `dir`."))
        for pid in list(f.through) + ([f.threads_into] if f.threads_into else []):
            if sp.part(pid) is None:
                good = False
                out.append(fail("validity.ref", G, BLOCKER, "Reference to a missing part", f"fastener `{f.id}` refers to `{pid}`"))
    if good:
        out.append(ok("validity.ok", G, "Spec is well formed", f"{len(sp.parts)} parts, {len(sp.fasteners)} fasteners, {len(sp.wires)} wires."))
    for rp in r.parts:
        if rp.part.kind in ("motor", "battery", "esc", "receiver", "servo", "weapon_motor") and rp.cat is None and not rp.part.catalog:
            out.append(fail("validity.no_catalog", G, WARNING, "Electronic part without a catalog entry",
                            f"`{rp.part.id}` has custom dimensions; its mass and ratings are unverified.").on(rp.part.id)
                       .fix("Use a catalog id so dimensions and ratings are locked to the real part."))
    return good


def claims(ctx):
    out = []
    for c in ctx.r.spec.claims:
        actual = ctx.metrics.get(c.metric)
        if actual is None:
            out.append(fail("claim.unknown_metric", "claims", BLOCKER, "Claim cannot be checked", f"claim `{c.id}`: no measured metric `{c.metric}`"))
            continue
        v = float(c.value)
        holds = {"<=": actual <= v + 1e-9, ">=": actual >= v - 1e-9, "==": abs(actual - v) <= 0.05 * max(abs(v), 1e-9)}.get(c.op, False)
        msg = f'"{c.text}" ({c.metric} {c.op} {v:g})'
        if holds:
            out.append(ok("claim.holds", "claims", "Claim matches the model", msg).expect(f"{c.metric} {c.op} {v:g}", f"{actual:.2f}"))
        else:
            out.append(fail("claim.false", "claims", WARNING, "Claim contradicted by the model", msg).expect(f"{c.metric} {c.op} {v:g}", f"{actual:.2f}")
                       .fix("Fix the model or correct the claim; the measured value is the truth."))
    return out
