"""Ripsaw generator entry (mirrors robots/revron/src/build_revron.py): spec.json model parts reference this file as
{"type": "model", "file": "src/build_ripsaw.py", "params": {"part": "<name>"}}. UNTESTED: never run."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
for _p in (ROOT, HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from ripsaw import build, assembly, PARTS  # noqa: E402,F401


def main():
    for name in PARTS:
        print(name, build(name).volume)


if __name__ == "__main__":
    main()
