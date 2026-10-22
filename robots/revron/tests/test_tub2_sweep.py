"""Param sweep: change a master and rebuild the tub in a fresh interpreter; it must still be ONE valid closed solid.

Each case copies the revron package, rewrites the named module-level assignment (`NAME = value`) in the copy and builds
tub2.chassis2() there, so every module sees the new master exactly as if the designer had edited it."""
import os, pathlib, re, shutil, subprocess, sys, tempfile, pytest

SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
ROOT = os.path.abspath(os.path.join(SRC, "..", "..", ".."))

# a drive motor that is not the RV12: same recipe as the catalog's n10_2200rpm_spicy (can, three gearbox plates, shaft) with its own plate
# pitch, height and width, registered in the catalog of the child interpreter only
SYNTH_MOTOR = """
import dataclasses
from robot import catalog as C
def synth(h, w, xs, t):
    shape = C.union([C.at(C.cyl_x(5.0, 12.0), -6.4, 0, 0), C.at(C.cyl_x(1.5, 10.0), xs[-1] + 5.0, 0, 0)] + [C.at(C.box(t, w, h), x, 0, 0) for x in xs])
    return dataclasses.replace(C.find("n10_300rpm_6v"), id="synth_motor", shape=shape)
_all = C.catalog() + (synth(%s, %s, %s, %s),)
C.catalog = lambda: _all
"""

BUILD = """
import sys
sys.path[:0] = [%r, %r]
%s
from revron import tub2, tub
c = %s
bb = c.bounding_box()
print("RESULT", len(c.solids()), c.is_valid, round(c.volume, 1), round(bb.max.X + bb.min.X, 4), *[round(v, 3) for v in (bb.min.X, bb.max.X, bb.min.Y, bb.max.Y, bb.min.Z, bb.max.Z)])
"""
SYNTH_PACK = """
import dataclasses
from robot import catalog as C
_p = C.find("lipo_2s_180_turnabot")
_all = C.catalog() + (dataclasses.replace(_p, id="synth_pack", shape=C.box(%s, %s, %s)),)
C.catalog = lambda: _all
"""


def build_with(overrides, tmp_path, pre="", what="tub2.chassis2()"):
    """overrides: {module: {NAME: 'python expr'}}; returns (solids, valid, volume, x_asymmetry)."""
    dst = pathlib.Path(tempfile.mkdtemp(dir=tmp_path)) / "src"
    shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("__pycache__"))
    for mod, names in overrides.items():
        f = dst / "revron" / f"{mod}.py"
        text = f.read_text()
        for name, expr in names.items():
            text, n = re.subn(rf"^{name} = [^#\n]*", f"{name} = {expr}   ", text, count=1, flags=re.M)
            assert n == 1, f"{mod}.{name} is not a plain module-level assignment"
        f.write_text(text)
    r = subprocess.run([sys.executable, "-c", BUILD % (str(dst), ROOT, pre, what)], capture_output=True, text=True)
    out = [ln for ln in r.stdout.splitlines() if ln.startswith("RESULT")]
    assert out, r.stderr[-1500:]
    n, ok, vol, asym, *bb = out[-1].split()[1:]
    return int(n), ok == "True", float(vol), float(asym), [float(v) for v in bb]


def check(overrides, tmp_path, pre="", what="tub2.chassis2()", symmetric=True):
    n, ok, vol, asym, bb = build_with(overrides, tmp_path, pre, what)
    assert n == 1 and ok and vol > 0 and (abs(asym) < 1e-3 or not symmetric), (n, ok, vol, asym)
    return vol, bb


@pytest.mark.parametrize("wall", [1.7, 1.85, 2.15, 2.3])
def test_wall_sweep(wall, tmp_path):
    """CH_WALL +-0.3: every rib, skin, fillet and pocket follows it."""
    check({"params_chassis": {"CH_WALL": repr(wall)}}, tmp_path)


@pytest.mark.parametrize("motor", ["n10_300rpm_6v", "n20_1000rpm_6v"])
def test_motor_catalog_swap(motor, tmp_path):
    """Another catalog gearmotor (no plate gap to key into, different length): the stack end, top and width move the seat, ledge and stop wall."""
    check({"params_chassis": {"DRIVE_MOTOR": repr(motor)}}, tmp_path)


@pytest.mark.parametrize("dims", [("12.0", "10.0", "(0.6, 3.35, 7.15)", "0.9"), ("13.0", "11.0", "(0.6, 3.85, 8.15)", "0.9"), ("11.0", "9.0", "(0.8, 3.4, 6.4)", "1.1")])
def test_motor_plate_stack_swap(dims, tmp_path):
    """A gearmotor with its own plate pitch, height and width: key tab, stop wall, ledge follow."""
    check({"params_chassis": {"DRIVE_MOTOR": repr("synth_motor")}}, tmp_path, SYNTH_MOTOR % dims)


@pytest.mark.parametrize("pack", [(37.0, 18.0, 11.0), (35.0, 18.0, 11.0), (36.0, 19.0, 11.0), (36.0, 17.0, 11.0), (36.0, 18.0, 12.0), (36.0, 18.0, 10.0)])
def test_battery_size_sweep(pack, tmp_path):
    """Pack +-1 mm each way: the foam pad stays one solid, a third of the pack footprint, topped at the pack's underside."""
    over = {"params_hardware": {"BATTERY": repr("synth_pack")}}
    _, bb = check(over, tmp_path, SYNTH_PACK % pack, what="tub.bat_pad()", symmetric=False)
    x0, x1, y0, y1, z0, z1 = bb
    L, W, H = pack
    assert abs((z1 - 12.0) + H / 2) < 1e-6                 # pad top = pack underside (BAT_Z = 12)
    assert abs(x1 - x0 - W / 3) < 1e-3 and abs(y1 - y0 - L / 3) < 1e-3


def test_tub_does_not_depend_on_the_pack(tmp_path):
    """The pack is a tenant of the bay, not a dimension of the tub."""
    over = {"params_hardware": {"BATTERY": repr("synth_pack")}}
    assert check(over, tmp_path, SYNTH_PACK % (37.0, 19.0, 12.0))[0] == check({}, tmp_path)[0]
