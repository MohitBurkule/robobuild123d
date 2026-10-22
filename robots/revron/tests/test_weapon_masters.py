"""[fix-B-rebuild] Editing one weapon master dimension makes the whole part follow, and the part still builds as one
solid: each case edits one line of a copy of the generator's params and rebuilds the parts in a fresh interpreter."""
import json
import os
import re
import shutil
import subprocess
import sys

import pytest

SRC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "src")
REPO = os.path.abspath(os.path.join(SRC, "..", "..", ".."))

PROBE = r"""
import json, sys
sys.path[:0] = [{src!r}, {repo!r}]
from revron import drisk, mount, params as P
out = {{}}
for name, fn in (("mount_r", lambda: mount.weapon_mount("r")), ("mount_l", lambda: mount.weapon_mount("l")),
                 ("spacer", mount.motor_back_spacer), ("spider", drisk.spider), ("disc", lambda: drisk.disc("disc_a")),
                 ("dspacer", drisk.drisk_spacer)):
    s = fn()
    bb = s.bounding_box()
    out[name] = dict(solids=len(s.solids()), vol=s.volume, min=[bb.min.X, bb.min.Y, bb.min.Z], max=[bb.max.X, bb.max.Y, bb.max.Z])
def inside(s, p):
    import build123d as bd
    return s.is_inside(bd.Vector(*p))
c = mount.stator_bolt_circle()[0]
out["stator_hole_open"] = not inside(mount.weapon_mount("r"), (P.MNT_IN + 1.0, P.WY + c[0], P.WZ + c[1]))
out["spacer_hole_open"] = not inside(mount.motor_back_spacer(), (P.MNT_IN - P.BSP_T / 2, P.WY + c[0], P.WZ + c[1]))
u, v = drisk._disc_local(P.BOLT_R, 0.0)
x = sum(P.DR_X["spider"]) / 2
out["spider_bolt_open"] = not inside(drisk.spider(), (x, u, v))
out["dspacer_bolt_open"] = not inside(drisk.drisk_spacer(), (sum(P.DR_X["spacer"]) / 2, u, v))
print(json.dumps(out))
"""


def _build(tmp_path, edit=None):
    dst = tmp_path / "src"
    shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("__pycache__"))
    if edit:
        fname, pat, new = edit
        f = dst / "revron" / fname
        text, n = re.subn(pat, new, f.read_text(), count=1, flags=re.M)
        assert n == 1, pat
        f.write_text(text)
    r = subprocess.run([sys.executable, "-c", PROBE.format(src=str(dst), repo=REPO)], capture_output=True, text=True, timeout=600)
    assert r.returncode == 0, r.stderr[-2000:]
    return json.loads(r.stdout.strip().splitlines()[-1])


@pytest.fixture(scope="module")
def base(tmp_path_factory):
    return _build(tmp_path_factory.mktemp("base"))


def _ok(m):
    for k in ("mount_r", "mount_l", "spacer", "spider", "disc", "dspacer"):
        assert m[k]["solids"] == 1, k
    assert m["stator_hole_open"] and m["spacer_hole_open"] and m["spider_bolt_open"] and m["dspacer_bolt_open"]


def test_base_holes_line_up(base):
    _ok(base)


def test_mount_thickness_follows(tmp_path, base):
    m = _build(tmp_path, ("params_chassis.py", r"^MNT_IN, MNT_T, MNT_SLAB_T = 13.4, 8.0, 4.0", "MNT_IN, MNT_T, MNT_SLAB_T = 13.4, 9.0, 4.0"))
    _ok(m)
    assert m["mount_r"]["max"][0] - m["mount_r"]["min"][0] > base["mount_r"]["max"][0] - base["mount_r"]["min"][0]
    assert m["mount_l"]["vol"] > base["mount_l"]["vol"]


def test_stator_bolt_circle_follows(tmp_path):
    _ok(_build(tmp_path, ("params_weapon.py", r"^STATOR_PCD = 2 \* math.hypot.*$", "STATOR_PCD = 13.0")))


def test_stack_bolt_circle_follows(tmp_path):
    _ok(_build(tmp_path, ("params_weapon.py", r"^BOLT_R, HUB_R = 14.0,", "BOLT_R, HUB_R = 13.6,")))


def test_disc_radius_follows(tmp_path, base):
    m = _build(tmp_path, ("params_weapon.py", r"^DISC_R, DISC_ECC, DISC_ECC_A = 16.5,", "DISC_R, DISC_ECC, DISC_ECC_A = 17.0,"))
    _ok(m)
    assert m["disc"]["vol"] > base["disc"]["vol"]


def test_plate_height_follows(tmp_path, base):
    """The mount notch top is the chassis rim (MNT_TOP_Z = CH_Z1): lowering the rim lowers the plate's rear top."""
    m = _build(tmp_path, ("params_chassis.py", r"^CH_Z0, CH_Z1 = 2.5, 19.5", "CH_Z0, CH_Z1 = 2.5, 19.0"))
    _ok(m)
    assert m["mount_r"]["vol"] != base["mount_r"]["vol"]
