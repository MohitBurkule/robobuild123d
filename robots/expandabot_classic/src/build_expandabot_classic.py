"""Expandabot Classic generator entry point."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
for _p in (ROOT, HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from expandabot_classic import assembly, params  # noqa: E402
from expandabot_classic.assembly import PARTS, build, cots, made_parts  # noqa: E402,F401


def main():
    problems = params.check()
    for p in problems:
        print("CHECK:", p)
    made = assembly.made_parts()
    m = assembly.mass_report(made)
    print(f"mass estimate {m:.1f} g of {params.MASS_LIMIT_G} g")
    return 1 if problems or m > params.MASS_LIMIT_G else 0


if __name__ == "__main__":
    sys.exit(main())
