"""Limpet XXT generator entry point. UNTESTED: this file has never been run.

Run (when allowed), from the repo root:  python robots/limpet_xxt/src/build_limpet_xxt.py [flip_deg]
Writes robots/limpet_xxt/step/limpet_xxt.step and one STL per fabricated part, prints rule checks and mass.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
for _p in (ROOT, HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from limpet_xxt import params, assembly  # noqa: E402


def main(argv=None):
    argv = sys.argv[1:] if argv is None else argv
    flip = float(argv[0]) if argv else params.START_FLIP_DEG
    problems = params.check()
    for p in problems:
        print("CHECK:", p)
    made = assembly.export(os.path.join(HERE, "..", "step"), flip)
    m = assembly.mass_report(made)
    print(f"flipper rest angle {params.FLIP_REST_DEG:.1f} deg, overall {params.OVERALL_L} x {params.OVERALL_W} x {params.WHEEL_D} mm")
    print(f"mass estimate {m:.1f} g of {params.MASS_LIMIT_G} g")
    return 1 if problems or m > params.MASS_LIMIT_G else 0


if __name__ == "__main__":
    sys.exit(main())
