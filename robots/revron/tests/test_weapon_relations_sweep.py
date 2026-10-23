"""[fix-B-vers2] Sweep of the weapon-part relations over the catalog weapon motors (REVRON_WEAPON_MOTOR): the RV02 shaft
nut recess follows the nut catalog for the motor's shaft thread, RV02's teardrop rim stays one skin round it, the
chassis clear radius follows the disc rim envelope, the mount nose follows the lug's standoff arc and the heel the
chassis floor, and RV02 / RV03 still build as one valid solid. Motors the drisk cannot take fail at import with
WeaponMotorError (by design) and are skipped."""
import json, os, subprocess, sys

import pytest

SRC = os.path.join(os.path.dirname(__file__), "..", "src")
ROOT = os.path.abspath(os.path.join(SRC, "..", "..", ".."))
CODE = r"""
import json, sys
sys.path.insert(0, %r); sys.path.insert(0, %r)
try:
    from revron import params as P
except Exception as e:
    if type(e).__name__ == "WeaponMotorError":
        print(json.dumps(dict(skip=str(e)))); sys.exit(0)
    raise
from revron import mount as M
from robot.cad import fastener_catalog as fc
out = dict(recess=P.NUT_RECESS_R, s=fc.nut(P.SHAFT_NUT_D)[0], nut_d=P.SHAFT_NUT_D, shaft_d=P.SHAFT_D, top_l=P.MNT_SIDE["l"]["top_r"],
           wall=P.CH_WALL, clear=P.WEAPON_CLEAR_R, rim=P.DISC_R - P.DISC_ECC, nose=P.NOSE_R, lug=P.LUG_SB_R,
           heel=P.MNT_HEEL, z0=P.CH_Z0, brg=P.BRG_SEAT_R)
for side in ("r", "l"):
    m = M.weapon_mount(side)
    out[side] = [len(m.solids()), m.is_valid]
print(json.dumps(out))
""" % (ROOT, SRC)
MOTORS = ["gr1507", "bbb_be1806_2300kv", "brotherhobby_tc1404_3800kv", "repeat_2004_1400kv", "emax_eco2207_1900kv"]


@pytest.mark.parametrize("motor", MOTORS)
def test_weapon_relations_follow_motor(motor):
    p = subprocess.run([sys.executable, "-c", CODE], env=dict(os.environ, REVRON_WEAPON_MOTOR=motor), capture_output=True, text=True, cwd=ROOT)
    assert p.returncode == 0, p.stderr[-3000:]
    r = json.loads(p.stdout.strip().splitlines()[-1])
    if "skip" in r:
        pytest.skip(r["skip"])
    assert r["nut_d"] >= r["shaft_d"] - 1e-9
    assert abs(r["recess"] - 0.75 * r["s"]) < 1e-6                     # recess takes the socket on the catalog nut
    assert r["recess"] > r["brg"]                                        # the nut recess is wider than the bearing seat
    assert abs(r["top_l"] - r["recess"] - r["wall"] / 2) < 1e-6          # RV02 rim one skin round the recess
    assert abs(r["clear"] - r["rim"]) < 1e-9 and abs(r["nose"] - r["lug"]) < 1e-9
    assert r["heel"]["z_hook"] == r["z0"] and abs(r["heel"]["z_lip"] - r["z0"] - r["wall"]) < 1e-9
    assert r["r"] == [1, True] and r["l"] == [1, True], r
    if motor == "gr1507":
        assert (r["recess"], r["top_l"], r["clear"], r["nose"]) == (6.0, 7.0, 16.0, 3.25)   # STEP values


UNFIT = ["repeat_2004_1400kv", "repeat_2004_2800kv", "emax_eco2207_1900kv", "bl_1806_2300kv", "bl_2306_1400kv", "be1806_bbb",
         "c_bbb_be1806_2300kv", "c_repeat_2004_antweight_spinner_motor"]
FIT = ["gr1507", "bbb_be1806_2300kv", "brotherhobby_tc1404_3800kv", "brotherhobby_tc1404_4600kv"]
CHK = r"""
import json, sys
sys.path.insert(0, %r); sys.path.insert(0, %r)
try:
    from revron import params as P
except Exception as e:
    print(json.dumps(dict(err=type(e).__name__, msg=str(e)))); sys.exit(0)
from revron import drisk as D
i = P.tub_interface()
print(json.dumps(dict(n_hub=P.N_HUB, spider_x=i["spider_x"], exp=[P.MOTOR_X + v for v in P.DR_X["spider"]],
                      sp=[len(D.spider().solids()), D.spider().is_valid])))
""" % (ROOT, SRC)


@pytest.mark.parametrize("motor", FIT + UNFIT)
def test_weapon_motor_fits_or_says_why(motor):
    p = subprocess.run([sys.executable, "-c", CHK], env=dict(os.environ, REVRON_WEAPON_MOTOR=motor), capture_output=True, text=True, cwd=ROOT)
    assert p.returncode == 0, p.stderr[-3000:]
    r = json.loads(p.stdout.strip().splitlines()[-1])
    if motor in UNFIT:
        assert r.get("err") == "WeaponMotorError" and "does not fit" in r["msg"], r
        return
    assert "err" not in r, r
    assert all(abs(a - b) < 1e-6 for a, b in zip(r["spider_x"], r["exp"])) and r["sp"] == [1, True], r
    if motor.startswith("brotherhobby_tc1404"):
        assert r["n_hub"] == 2      # 4 x M2 on d5 is too tight for button heads: every other screw
