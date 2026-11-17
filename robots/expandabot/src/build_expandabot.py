"""Expandabot generator entry point (mirrors robots/limpet_xxt/src/build_limpet_xxt.py: path setup + re-export).

spec.json references parts as {"type": "model", "file": "src/build_expandabot.py", "params": {"part": "<name>"}},
so build(part=...) below is the only geometry entry point. Frame: +X left, +Y forward (flipper & claws end),
+Z up, floor Z = 0.

Run from the repo root:  python robots/expandabot/src/build_expandabot.py
Writes robots/expandabot/step/expandabot.step and one STL per fabricated part, prints rule checks and mass.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
for _p in (ROOT, HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from expandabot import assembly, params  # noqa: E402
from expandabot.assembly import PARTS, build, cots, made_parts  # noqa: E402,F401


def main(argv=None):
    argv = sys.argv[1:] if argv is None else sys.argv[1:]
    problems = params.check()
    for p in problems:
        print("CHECK:", p)
    made = assembly.export(os.path.join(HERE, "..", "step"))
    m = assembly.mass_report(made)
    print(f"flipper rest angle {params.FLIP_REST_DEG:.1f} deg, overall {params.OVERALL_L} x {params.OVERALL_W} x {params.WHEEL_D} mm")
    print(f"mass estimate {m:.1f} g of {params.MASS_LIMIT_G} g")
    return 1 if problems or m > params.MASS_LIMIT_G else 0


if __name__ == "__main__":
    sys.exit(main())
