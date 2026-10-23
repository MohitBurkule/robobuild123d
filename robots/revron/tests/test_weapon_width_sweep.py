"""Width sweep (hook size.width, env REVRON_SIZE_WIDTH): the weapon module (mounts, motor, drisk stack and its bell screws
bolt_p*) is drawn about the robot centre plane from MNT_IN, so a wider or narrower chassis must leave every weapon X datum, the
bell-screw circle and the bolt_p seats where they are (hyp_runs_28: bolt_p* trapped by mount_l at width +10 %)."""
import json
import os
import subprocess
import sys
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[1] / "src"
REPO = Path(__file__).resolve().parents[3]

BODY = """
import sys, json
sys.path.insert(0, {repo!r}); sys.path.insert(0, {src!r})
import revron.params_weapon as P
from revron.common import _polar
from revron.drisk import _disc_local
hubs = [_disc_local(*h) for h in _polar(P.HUB_R, P.N_HUB)]
print(json.dumps(dict(dr_x=P.DR_X, motor_x=P.MOTOR_X, mnt=[P.MNT_IN, P.MNT_OUT, P.MNT_SLAB], hub=[P.HUB_R, P.HUB_D, P.N_HUB],
                      hubs=[[round(a, 6) for a in h] for h in hubs], ch=P.CH_HALF_W)))
"""


def _run(width):
    env = dict(os.environ, REVRON_SIZE_WIDTH=width)
    out = subprocess.run([sys.executable, "-c", BODY.format(repo=str(REPO), src=str(SRC))], env=env, capture_output=True, text=True, timeout=300)
    assert out.returncode == 0, out.stderr[-2000:]
    return json.loads(out.stdout.strip().splitlines()[-1])


@pytest.mark.parametrize("width", ["-10%", "10%", "20%"])
def test_weapon_datums_ignore_width(width):
    base, swept = _run("0"), _run(width)
    assert swept["ch"] != base["ch"]             # the hook really moved the side walls
    for k in ("dr_x", "motor_x", "mnt", "hub", "hubs"):
        assert swept[k] == base[k], k


TOP = """
import sys, json
sys.path.insert(0, {repo!r}); sys.path.insert(0, {src!r})
import revron.params_weapon as P
print(json.dumps(dict(notch_x=P.TOP_NOTCH_X[1], above=P.MNT_ABOVE_RIM_X + P.MNT_IN, shoulder=P.TOP_SHOULDER_Y,
                      notch_y=[P.MNT_SIDE[s]["notch_y"] for s in "rl"])))
"""


@pytest.mark.parametrize("env", [("REVRON_SIZE_WIDTH", "-10%"), ("REVRON_SIZE_LENGTH", "10%"), ("REVRON_SIZE_LENGTH", "20%")])
def test_mount_follows_top_panel_notch(env):
    """mount_l / mount_r rise through the top panel's front notch: above the rim they stay inside its outer edge (width -10 %:
    overlap + mount/top_panel locked) and stay ahead of its shoulder by the STEP gap (length +10 %: both locked)."""
    e = dict(os.environ, **{env[0]: env[1]})
    out = subprocess.run([sys.executable, "-c", TOP.format(repo=str(REPO), src=str(SRC))], env=e, capture_output=True, text=True, timeout=300)
    assert out.returncode == 0, out.stderr[-2000:]
    d = json.loads(out.stdout.strip().splitlines()[-1])
    assert d["above"] < d["notch_x"]
    assert all(y > d["shoulder"] for y in d["notch_y"])
    assert [round(y - d["shoulder"], 6) for y in d["notch_y"]] == [2.27, 1.1]


EARS = """
import sys, json
sys.path.insert(0, {repo!r}); sys.path.insert(0, {src!r})
from revron.mount import weapon_mount
from revron.panel_top import top_panel
t = top_panel()
print(json.dumps({{s: [(m & t).volume, m.distance_to(t)] for s, m in ((s, weapon_mount(s)) for s in "lr")}}))
"""


@pytest.mark.parametrize("variant", ["", "printable"])
def test_mount_clears_top_panel_ears_narrow(variant):
    """width -10 %: the top panel's front ears pass under the mount's notch-top tip (thickened in the printable variant);
    mount_l / mount_r must keep a gap to top_panel, not touch it (fixer A report after #41)."""
    e = dict(os.environ, REVRON_SIZE_WIDTH="-10%", REVRON_MOUNT_VARIANT=variant)
    out = subprocess.run([sys.executable, "-c", EARS.format(repo=str(REPO), src=str(SRC))], env=e, capture_output=True, text=True, timeout=600)
    assert out.returncode == 0, out.stderr[-2000:]
    d = json.loads(out.stdout.strip().splitlines()[-1])
    for s, (vol, gap) in d.items():
        assert vol < 0.01 and gap > 0.2, (s, vol, gap)


STOCK = """
import sys, json
sys.path.insert(0, {repo!r}); sys.path.insert(0, sys.argv[1])
from revron.mount import weapon_mount
print(json.dumps({{s: [len(m.solids()), m.is_valid, m.volume] for s, m in ((s, weapon_mount(s)) for s in "rl")}}))
"""


@pytest.mark.parametrize("variant", ["", "printable"])
def test_mount_builds_at_narrow_stock_width(variant, tmp_path):
    """[fix-B-zero] dim:CH_HALF_W_STOCK -10 %: the top-panel notch clip lands on RV03's batter seam; mount_r must still be one
    valid solid (it came back empty before the plate was fixed for the clip)."""
    import re, shutil
    dst = tmp_path / "src"
    shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("__pycache__"))
    f = dst / "revron" / "params_chassis.py"
    txt, n = re.subn(r"^CH_HALF_W_STOCK = ([\d.]+)", lambda m: f"CH_HALF_W_STOCK = {float(m.group(1)) * 0.9!r}", f.read_text(), count=1, flags=re.M)
    assert n == 1
    f.write_text(txt)
    e = dict(os.environ, REVRON_MOUNT_VARIANT=variant)
    out = subprocess.run([sys.executable, "-c", STOCK.format(repo=str(REPO)), str(dst)], env=e, capture_output=True, text=True, timeout=600)
    assert out.returncode == 0, out.stderr[-2000:]
    d = json.loads(out.stdout.strip().splitlines()[-1])
    for s, (n, ok, vol) in d.items():
        assert n == 1 and ok and vol > 2000.0, (s, d)


ROTOR = """
import sys, json
sys.path.insert(0, {repo!r}); sys.path.insert(0, {src!r})
import revron.params_weapon as P
from revron.joints import seat
from robot.cad import fastener_catalog as fc
i = P.tub_interface()
print(json.dumps(dict(rotor=i["rotor_x"], spider=i["spider_x"], head=seat("bolt_d0")["at"][0] + fc.head(P.STACK_BOLT_D, "button")[1])))
"""


@pytest.mark.parametrize("motor", ["gr1507", "brotherhobby_tc1404_3800kv"])
def test_rotor_x_reaches_the_stack_bolt_heads(motor):
    """[fix-B-zero] the weapon contract's rotor_x spans the spider's outer face to the bolt_d heads (TC1404: the heads, not the
    spider, are the +X end); at the stock motor it adds nothing past spider_x on the spider's side."""
    e = dict(os.environ, REVRON_WEAPON_MOTOR=motor)
    out = subprocess.run([sys.executable, "-c", ROTOR.format(repo=str(REPO), src=str(SRC))], env=e, capture_output=True, text=True, timeout=300)
    assert out.returncode == 0, out.stderr[-2000:]
    d = json.loads(out.stdout.strip().splitlines()[-1])
    assert d["rotor"][0] == min(d["spider"]) and abs(d["rotor"][1] - d["head"]) < 1e-6, d


def test_unfit_errors_are_declared():
    sys.path[:0] = [str(REPO), str(SRC)]
    from revron.params_weapon import WeaponTypeError
    from revron.weapon_motor import WeaponMotorError
    assert WeaponTypeError.declared_unfit is True and WeaponMotorError.declared_unfit is True
