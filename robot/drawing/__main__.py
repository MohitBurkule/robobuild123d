"""python -m robot.drawing <part> -o out.pdf [--size A1|A3] [--no-check]"""
import argparse
import sys
from pathlib import Path


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m robot.drawing", description=__doc__)
    ap.add_argument("part", help="registry name (revron.chassis), a .step/.brep file, or module:function")
    ap.add_argument("-o", "--out", default=None, help="output .pdf (an .svg and a .png preview are written next to it)")
    ap.add_argument("--size", default="A1", choices=["A1", "A2", "A3"])
    ap.add_argument("--no-png", action="store_true")
    ap.add_argument("--no-check", action="store_true")
    ap.add_argument("--date", default=None)
    ap.add_argument("--ref", default=None, help="reference part (.brep/.step, e.g. the original STEP body) to compare holes / fillets / chamfers with")
    ap.add_argument("--strict", action="store_true", help="design findings (insert bores, reference compare) also fail the run")
    a = ap.parse_args(argv)
    from . import check, parts
    from .drawing import make_drawing, write
    info = parts.load(a.part)
    d = make_drawing(info, a.size, date=a.date)
    out = Path(a.out or f"{info.dwg_no or info.name}.pdf")
    used = write(d, out, png=not a.no_png)
    print(f"wrote {out} ({used}), {out.with_suffix('.svg')}" + ("" if a.no_png else f", {out.with_suffix('.png')}"))
    print(f"scale {d.scale:g}, {len(d.plan.dims)} linear dims, {len(d.placed)} callouts placed, {len(d.skipped)} skipped (no room)")
    if a.no_check:
        return 0
    m = check.Model(info.shape)
    t1, ok1 = check.report(check.check_svg(d.svg, info.shape, m), "dimension text vs model")
    t2, ok2 = check.report(check.check_params(info, m), "named params vs model")
    print(t1)
    print(t2)
    design_ok = True
    if info.insert_bores:
        t, ok = check.report(check.check_insert_bores(info, m), "heat-set bores vs insert catalogue")
        print(t)
        design_ok &= ok
    if a.ref:
        ref = check.Model(check.load_reference(a.ref, info.ref_matrix))
        t, ok = check.report(check.compare_reference(m, ref), f"model vs reference {Path(a.ref).name} (shown = ours, model = reference)")
        print(t)
        design_ok &= ok
    if not (ok1 and ok2):
        return 1
    return 2 if a.strict and not design_ok else 0


if __name__ == "__main__":
    sys.exit(main())
