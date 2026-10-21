"""[drawing] Orchestration: shape -> projected views -> annotation plan -> placement -> sheet canvas -> SVG / PDF / PNG."""
from __future__ import annotations

import datetime
from dataclasses import dataclass
from pathlib import Path

from . import annotate, features as F, layout, sheet as S, views as Vw
from .canvas import Canvas
from .svg import to_svg

VIEW_NAMES = ("front", "top", "bottom", "left", "right")


@dataclass
class Drawing:
    canvas: Canvas
    svg: str
    scale: float
    plan: object
    placed: list
    skipped: list
    views: dict
    mass_g: float


def mass_g(shape, material, solid_fraction=1.0):
    try:
        from robot.catalog import material as mat
        rho = mat(material).density
    except Exception:            # noqa: BLE001 - unknown / no material
        return None, None
    return shape.volume * rho / 1000.0, shape.volume * rho / 1000.0 * solid_fraction


def make_drawing(info, size="A1", names=VIEW_NAMES, date=None):
    shape = info.shape
    views = {n: Vw.project(shape, Vw.make_view(n)) for n in names}
    holes = F.holes(shape)
    P = annotate.plan(shape, views, holes=holes, hole_roles=getattr(info, 'hole_roles', ()))
    sh = S.make_sheet(size)
    x0, y0, x1, y1 = sh.frame
    region = (x0 + 4, sh.title_block[3] + 18, x1 - 4, y1 - 4)
    pl = layout.place_views(views, region, annotate.margins(P, views))
    for k, V in views.items():
        V.name = k
    c = Canvas(sh.w, sh.h)
    S.draw_frame(c, sh)
    occ = layout.Occupancy()
    occ.add(sh.title_block, "text-title")
    occ.add((x0 - 10, y0 - 10, sh.w, y0 + 1), "text-frame")
    occ.add((x0 - 10, y1 - 1, sh.w, sh.h), "text-frame")
    occ.add((0, 0, x0 + 1, sh.h), "text-frame")
    occ.add((x1 - 1, 0, sh.w, sh.h), "text-frame")
    for k, V in views.items():
        occ.add(annotate.view_box(pl, V), "view-" + k)
        with c.group(cls="view", name=k):
            for p in V.hidden:
                c.poly(pl.to_sheet(k, p), "hidden")
            for p in V.visible:
                c.poly(pl.to_sheet(k, p), "visible")
    annotate.render_marks(c, P, views, pl)
    annotate.render_dims(c, P, views, pl, occ)
    placed, skipped = annotate.render_callouts(c, P, views, pl, occ)
    # view labels under each view
    for k, V in views.items():
        bx = annotate.view_box(pl, V)
        lab = f"{k.upper()} VIEW"
        for dy in (-(annotate.BASE + annotate.STEP * max(P.levels(k, 'b') - 1, 0) + 10), -6):
            pos = ((bx[0] + bx[2]) / 2, bx[1] + dy)
            tb = (pos[0] - 15, pos[1] - 1, pos[0] + 15, pos[1] + 4)
            if occ.free(tb, pad=0.5):
                occ.add(tb, "text-label")
                c.text(pos, lab, 3.5, "middle")
                break
    full, printed = mass_g(shape, info.material, info.solid_fraction)
    mat_label = {"pla_st": "PLA (pla_st)", "tpu": "TPU"}.get(info.material, info.material.upper() or "-")
    mass = "-" if full is None else (f"{full:.2f} g solid / {printed:.2f} g at {info.solid_fraction:.0%} fill" if info.solid_fraction < 1 else f"{full:.2f} g")
    S.title_block(c, sh, dict(
        title=info.title or info.name, part=info.name, dwg_no=info.dwg_no, material=mat_label, mass=mass,
        scale=layout.scale_label(pl.scale), date=date or datetime.date.today().isoformat(), units="mm",
        drawn="robot.drawing (build123d HLR + drafting)", source=str(info.source)[-60:], sheet="1 OF 1", size=size,
        notes=["NOTES:", "1. ALL DIMENSIONS IN MM, MEASURED FROM THE B-REP MODEL.",
               f"2. VOLUME {shape.volume:.1f} mm3. THIRD ANGLE PROJECTION.",
               "3. HIDDEN LINES DASHED, CENTRE LINES CHAIN."]))
    svg = to_svg(c, info.title or info.name)
    return Drawing(c, svg, pl.scale, P, placed, skipped, views, full)


def write(drawing, out, png=True, dpi=150):
    """Write <out>.svg next to out (.pdf), and a PNG preview; returns the converter used."""
    from .output import convert
    out = Path(out)
    svg_path = out.with_suffix(".svg")
    svg_path.write_text(drawing.svg)
    used = convert(svg_path, out, drawing.canvas) if out.suffix.lower() != ".svg" else "svg"
    if png:
        convert(svg_path, out.with_suffix(".png"), drawing.canvas, dpi=dpi)
    return used
