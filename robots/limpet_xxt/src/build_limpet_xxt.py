"""Limpet XXT generator entry point (mirrors robots/scythe/src/build_scythe.py: path setup + re-export).

spec.json references parts as {"type": "model", "file": "src/build_limpet_xxt.py", "params": {"part": "<name>"}},
so build(part=...) below is the only geometry entry point. Frame: X forward (flipper end), Y left, Z up, floor Z = 0;
every part is built in world coordinates at the rest pose.

Run from the repo root:  python robots/limpet_xxt/src/build_limpet_xxt.py
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
from limpet_xxt.assembly import build, made_parts, cots, PARTS  # noqa: E402,F401


def main(argv=None):
    argv = sys.argv[1:] if argv is None else sys.argv[1:]
    problems = params.check()
    for p in problems:
        print("CHECK:", p)
    import build123d as bd
    made = assembly.export(os.path.join(HERE, "..", "step"))
    m = assembly.mass_report(made)
    print(f"flipper rest angle {params.FLIP_REST_DEG:.1f} deg, overall {params.OVERALL_L} x {params.OVERALL_W} x {params.WHEEL_D} mm")
    print(f"mass estimate {m:.1f} g of {params.MASS_LIMIT_G} g")
    return 1 if problems or m > params.MASS_LIMIT_G else 0


if __name__ == "__main__":
    sys.exit(main())
