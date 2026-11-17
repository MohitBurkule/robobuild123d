"""AntiC generator entry point.

spec.json references parts as {"type": "model", "file": "src/build_antic.py", "params": {"part": "<name>"}}.
Frame: X right, Y forward, Z up, floor Z = 0.
"""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
for _p in (ROOT, HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

import antic as _pkg

build = _pkg.build
PARTS = _pkg.PARTS


def main():
    """Export AntiC assembly to STEP."""
    import build123d as bd

    out = os.path.join(HERE, "..", "step")
    os.makedirs(out, exist_ok=True)
    bd.export_step(build("assembly"), os.path.join(out, "antic.step"))


if __name__ == "__main__":
    main()
