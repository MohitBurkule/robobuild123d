"""Scythe generator entry (mirrors robots/revron/src/build_revron.py: path setup + re-export). UNTESTED.

spec.json references parts as {"type": "model", "file": "src/build_scythe.py", "params": {"part": "<name>"}}, so
build(part=...) below is the only geometry entry point. Frame: X right, Y forward, Z up, floor Z = 0.
"""
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
for _p in (ROOT, HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import scythe as _pkg

build = _pkg.build
PARTS = _pkg.PARTS


def main():
    """Rule asserts, then STEP export of the assembly next to this file (../step/scythe.step)."""
    import build123d as bd
    _pkg.params.check()
    out = os.path.join(HERE, "..", "step")
    os.makedirs(out, exist_ok=True)
    bd.export_step(build("assembly"), os.path.join(out, "scythe.step"))


if __name__ == "__main__":
    main()
