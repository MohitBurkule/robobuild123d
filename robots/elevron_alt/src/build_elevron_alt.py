"""Elevron 3.0 "Alt" generator: model-file entry point for spec.json (`build(part=...)`); running it writes the spec.
The geometry lives in the elevron_alt package next to this file (explicit imports, no merged namespace)."""
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
for _p in (ROOT, os.path.join(ROOT, "robots", "shared", "src"), HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from elevron_alt.assembly import build, PARTS  # noqa: E402,F401

if __name__ == "__main__":
    from elevron_alt.spec import main
    main()
