"""Writes a robot to disk: editable spec, verifier report, renders, STL meshes, exact B-rep STEP files and a README.

Layout of `<dir>/<slug>/`:
  spec.json, report.json, REPORT.md (ends with a fail-closed NOT CHECKED section), README.md (shows renders/iso.png),
  renders/<view>.png, stl/<body>.stl (tessellated, start pose), step/<body>.step (exact build123d B-rep placed in the
  start pose), step/assembly.step (all placed solids in one compound, named by body id).
"""

from __future__ import annotations

import json

import numpy as np
from pathlib import Path

from . import checks, render, shapes
from . import world as world_mod
from .finding import BLOCKER

# Views written by default; the first is the one used in the README.
VIEWS = ["iso", "top", "exploded", "section_z", "back"]


def safe_name(bid: str) -> str:
    return bid.replace(":", "_").replace("/", "_").replace("\\", "_")


def wire_solid(rt):
    """Exact B-rep of a routed wire: a circle of the gauge OD swept along the route polyline (round transitions).
    Falls back to a fused chain of cylinders and joint spheres if the sweep fails. Returned in world frame."""
    import build123d as bd

    pts = []
    for p in np.asarray(rt.points, float):
        if not pts or np.linalg.norm(p - pts[-1]) > 1e-3:
            pts.append(p)
    if len(pts) < 2:
        raise ValueError("route has fewer than 2 distinct points")
    r = rt.od_mm / 2
    vs = [bd.Vector(*map(float, p)) for p in pts]
    try:
        path = bd.Polyline(*vs)
        e0 = path.edges()[0]
        prof = bd.Face(bd.Wire.make_circle(r, bd.Plane(origin=e0.position_at(0), z_dir=e0.tangent_at(0))))
        s = bd.sweep(prof, path=path, transition=bd.Transition.ROUND)
        sol = s.solids()
        if len(sol) == 1 and sol[0].is_valid and sol[0].volume > 0:
            return sol[0]
    except Exception:  # noqa: BLE001 - fall through to the robust construction
        pass
    acc = None
    for a, b in zip(vs, vs[1:]):
        d = b - a
        c = bd.Solid.make_cylinder(r, d.length, bd.Plane(origin=a, z_dir=d))
        acc = c if acc is None else acc.fuse(c)
    for v in vs[1:-1]:
        acc = acc.fuse(bd.Solid.make_sphere(r).moved(bd.Location(v)))
    acc = acc.clean()
    sol = acc.solids()
    if len(sol) != 1 or not sol[0].is_valid:
        raise ValueError(f"wire B-rep invalid ({len(sol)} solids)")
    return sol[0]


def report_markdown(spec, rep) -> str:
    s = [f"# Verifier report: {spec.name}\n",
         f"Profile `{rep.profile}`. {rep.summary['blockers']} blockers, {rep.summary['warnings']} warnings, "
         f"{rep.summary['passed']} checks passed. Check set revision {rep.checks_revision} (engine {rep.engine}).\n"]
    m = rep.metrics
    if all(k in m for k in ("mass_total_g", "mass_lo_g", "mass_hi_g", "mass_limit_g")):
        s.append(f"Mass {m['mass_total_g']:.1f} g (range {m['mass_lo_g']:.1f} to {m['mass_hi_g']:.1f} g, "
                 f"limit {m['mass_limit_g']:.0f} g).\n")
    s.append("## Findings\n")
    for f in rep.findings:
        tag = "pass" if f.passed else ("BLOCKER" if f.severity == BLOCKER else "warning")
        s.append(f"- **{tag}** `{f.id}`: {f.title} {f.message}")
        if f.fix_hint and not f.passed:
            s.append(f"  - Fix: {f.fix_hint}")
    s.append("\n## Mass budget\n\n| Part | Grams | Plus/minus | Source |\n|---|---|---|---|")
    for l in rep.mass:
        s.append(f"| {l.id} | {l.grams:.2f} | {l.tol_g:.2f} | {l.source} |")
    if rep.routes:
        s.append("\n## Wire routes\n\n| Wire | AWG | Diameter mm | Length mm |\n|---|---|---|---|")
        for r in rep.routes:
            s.append(f"| {r.id} | {r.awg:g} | {r.od_mm:.1f} | {r.length_mm:.0f} |")
    if rep.bench_checklist:
        s.append("\n## Bench checklist (CAD cannot prove these)\n")
        s += [f"- [ ] {c}" for c in rep.bench_checklist]
    s.append("\n## NOT CHECKED\n\nThe verifier did not judge these. A clean report says nothing about them.\n")
    s += [f"- {x}" for x in rep.not_checked] or ["- (nothing listed)"]
    return "\n".join(s) + "\n"


def readme(slug: str, spec, rep, step_ok: bool, compares=()) -> str:
    status = "passes" if rep.ok else "has blockers"
    m = rep.metrics
    s = [f"# {spec.name}\n\n![{spec.name}](renders/iso.png)\n",
         f"Verifier (`{rep.profile}`): {status}. {rep.summary['blockers']} blockers, {rep.summary['warnings']} warnings, "
         f"{rep.summary['passed']} checks passed. {len(rep.not_checked)} items NOT CHECKED (see REPORT.md).\n"]
    if all(k in m for k in ("mass_total_g", "mass_lo_g", "mass_hi_g")):
        s.append(f"Mass {m['mass_total_g']:.1f} g (range {m['mass_lo_g']:.1f} to {m['mass_hi_g']:.1f} g).\n")
    s.append("| Top | Exploded | Section |\n|---|---|---|\n"
             "| ![top](renders/top.png) | ![exploded](renders/exploded.png) | ![section](renders/section_z.png) |\n")
    if compares:
        s.append("## Reference photo overlays (model red, photo blue)\n\n"
                 + "\n".join(f"![compare {v}](renders/compare_{v}.png)" for v in compares) + "\n")
    s.append("## Files\n\n- `spec.json`: the full editable design. Load it back with the robot tools to change and re-verify.\n"
             "- `report.json`, `REPORT.md`: verifier output (REPORT.md ends with what was NOT CHECKED).\n"
             "- `stl/`: one STL per part (mm, start pose, so they assemble when imported together; wires included).\n"
             + ("- `step/`: exact B-rep STEP per part in the start pose, plus `assembly.step` with every part.\n" if step_ok else
                "- `step/`: STEP export failed or was skipped for some parts; see REPORT.md.\n")
             + "- `renders/`: iso, top, back, exploded and section views.\n\n"
             f"Regenerate: `python3 -m robot export spec.json {slug} <dir>`\n")
    return "\n".join(s)


def write_all(slug: str, spec, out_dir, opts=None, step=True, width=1100):
    """Verify `spec` and write everything under `out_dir/<slug>/`. Returns (report, files written)."""
    root = Path(out_dir) / slug
    for d in ("renders", "stl", "step"):
        (root / d).mkdir(parents=True, exist_ok=True)
    world, rep, _ = render.world_for(spec, opts or checks.Options())
    files = []

    def put(rel, data):
        p = root / rel
        p.write_bytes(data if isinstance(data, bytes) else data.encode())
        files.append(rel)

    # Geometry first, so STEP failures make it into the reports (fail closed).
    for b in world.bodies:
        name = safe_name(b.id)
        put(f"stl/{name}.stl", b.mesh.export(file_type="stl"))
    step_ok = True
    if step:
        import build123d as bd

        placed = []
        for b in world.bodies:
            name = safe_name(b.id)
            try:
                if b.is_wire and getattr(b.geom, "route", None) is not None:
                    p = wire_solid(b.geom.route).moved(shapes.location(b.M))  # route points are world frame; M = I
                else:
                    solid = b.geom.solid
                    if solid is None:
                        raise ValueError("no B-rep (tessellated-only body)")
                    p = solid.moved(shapes.location(b.M))
                p.label = b.id
                bd.export_step(p, str(root / "step" / f"{name}.step"))
                files.append(f"step/{name}.step")
                placed.append(p)
            except Exception as e:  # noqa: BLE001 - one bad body must not lose the others
                step_ok = False
                rep.not_checked.append(f"STEP export of `{b.id}`: {type(e).__name__}: {e} (STL only)")
        if placed:
            try:
                asm = bd.Compound(children=placed, label=spec.name or slug)
                bd.export_step(asm, str(root / "step" / "assembly.step"))
                files.append("step/assembly.step")
            except Exception as e:  # noqa: BLE001
                step_ok = False
                rep.not_checked.append(f"STEP assembly export failed: {type(e).__name__}: {e}")
    # Flat patterns of cut/bent sheet parts; a part that cannot be flattened is a blocker (it is not 2D).
    from .checks import process as process_check

    dxf_files, dxf_fails = process_check.export_dxf(world_mod.resolve(spec, fast=True), root)
    files += dxf_files
    if dxf_fails:
        rep.findings += process_check.export_findings(dxf_fails)
        rep.finish()
    for v in VIEWS:
        view = render.named(v, width)
        put(f"renders/{v}.png", render.render_png(world, view, None, []))
    from .checks import reference as ref_check

    compares = []
    for e in ref_check.entries(spec):
        try:
            _, png = ref_check.evaluate(world, spec, e)
        except Exception as ex:  # noqa: BLE001 - the check already reports unusable references
            rep.not_checked.append(f"Reference overlay ({e.get('view') or 'side'}): {type(ex).__name__}: {ex}")
            continue
        v = e.get("view") or "side"
        put(f"renders/compare_{v}.png", png)
        compares.append(v)
    put("spec.json", json.dumps(spec.to_dict(), indent=2))
    put("report.json", json.dumps(rep.to_dict(), indent=2))
    put("REPORT.md", report_markdown(spec, rep))
    put("README.md", readme(slug, spec, rep, step_ok, compares))
    return rep, files


def cli(a):
    from . import spec as spec_mod

    s = spec_mod.load(a.spec)
    rep, files = write_all(a.slug, s, a.dir, checks.Options(deep=not a.quick, fast=a.fast), step=not a.no_step,
                           width=a.width)
    print(f"{rep.name}: ok={rep.ok}, {rep.summary['blockers']} blockers; wrote {len(files)} files to "
          f"{Path(a.dir) / a.slug}")
    return 0 if rep.ok else 2


def add_cli(sub):
    p = sub.add_parser("export", help="write spec, report, renders, STL and STEP to <dir>/<slug>/")
    p.add_argument("spec")
    p.add_argument("slug", nargs="?", default=None)
    p.add_argument("dir", nargs="?", default="robots")
    p.add_argument("--fast", action="store_true")
    p.add_argument("--quick", action="store_true")
    p.add_argument("--no-step", action="store_true")
    p.add_argument("--width", type=int, default=1100)

    def run(a):
        if a.slug is None:
            a.slug = Path(a.spec).stem
        return cli(a)

    p.set_defaults(func=run)
