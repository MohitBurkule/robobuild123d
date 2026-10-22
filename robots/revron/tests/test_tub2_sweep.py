"""Param sweep: change a master and rebuild the tub in a fresh interpreter; it must still be ONE valid closed solid.

Each case copies the revron package, rewrites the named module-level assignment (`NAME = value`) in the copy and builds
tub2.chassis2() there, so every module sees the new master exactly as if the designer had edited it."""
import os, re, shutil, subprocess, sys, tempfile, pytest

SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
ROOT = os.path.abspath(os.path.join(SRC, "..", "..", ".."))

BUILD = """
import sys
sys.path[:0] = [%r, %r]
from revron import tub2
c = tub2.chassis2()
bb = c.bounding_box()
print("RESULT", len(c.solids()), c.is_valid, round(c.volume, 1), round(bb.max.X + bb.min.X, 4))
"""


def build_with(overrides, tmp_path):
    """overrides: {module: {NAME: 'python expr'}}; returns (solids, valid, volume, x_asymmetry)."""
    dst = tmp_path / "src"
    shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("__pycache__"))
    for mod, names in overrides.items():
        f = dst / "revron" / f"{mod}.py"
        text = f.read_text()
        for name, expr in names.items():
            text, n = re.subn(rf"^{name} = [^#\n]*", f"{name} = {expr}   ", text, count=1, flags=re.M)
            assert n == 1, f"{mod}.{name} is not a plain module-level assignment"
        f.write_text(text)
    r = subprocess.run([sys.executable, "-c", BUILD % (str(dst), ROOT)], capture_output=True, text=True)
    out = [ln for ln in r.stdout.splitlines() if ln.startswith("RESULT")]
    assert out, r.stderr[-1500:]
    n, ok, vol, asym = out[-1].split()[1:]
    return int(n), ok == "True", float(vol), float(asym)


def check(overrides, tmp_path):
    n, ok, vol, asym = build_with(overrides, tmp_path)
    assert n == 1 and ok and vol > 0 and abs(asym) < 1e-3, (n, ok, vol, asym)
    return vol


@pytest.mark.parametrize("wall", [1.7, 1.85, 2.15, 2.3])
def test_wall_sweep(wall, tmp_path):
    """CH_WALL +-0.3: every rib, skin, fillet and pocket follows it."""
    check({"params_chassis": {"CH_WALL": repr(wall)}}, tmp_path)
