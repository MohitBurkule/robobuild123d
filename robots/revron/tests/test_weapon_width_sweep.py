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
