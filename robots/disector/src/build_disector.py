"""Thin shim for Disector spec.json model references."""

import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)

from disector.make_spec import build, main  # noqa: E402, F401

if __name__ == "__main__":
    main()
