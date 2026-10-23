import os
import sys

SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
ROOT = os.path.abspath(os.path.join(SRC, "..", "..", ".."))
for p in (ROOT, os.path.join(ROOT, "robots", "shared", "src"), SRC):
    if p not in sys.path:
        sys.path.insert(0, p)
