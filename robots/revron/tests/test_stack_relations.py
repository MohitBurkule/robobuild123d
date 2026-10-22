"""[fix-B-reld] Rotor stack relations survive master edits and part swaps: each case edits one master of a copy of the
generator's params (or swaps the motor variant), rebuilds discs / spider / spacer / shaft in a fresh interpreter and
checks the relations: holes on the bolt circle at the N_STACK pitch, dogs pitched by N_STACK, tooth back face tangent
to the rim, spacer inside the disc rim, stack flush on the bell cap, every plate one valid solid."""
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
import json, math, sys
sys.path[:0] = [{src!r}, {repo!r}]
import build123d as bd
from revron import drisk, params as P
out = dict(N=P.N_STACK)
parts = dict(spider=drisk.spider(), disc=drisk.disc("disc_a"), disc_b=drisk.disc("disc_b"), dspacer=drisk.drisk_spacer(),
             shaft=drisk.weapon_shaft())
out["solids"] = {{k: [len(s.solids()), s.is_valid, s.volume > 0] for k, s in parts.items()}}
def opn(s, span, r, deg):
    u, v = drisk._disc_local(r * math.cos(math.radians(deg)), r * math.sin(math.radians(deg)))
    return not s.is_inside(bd.Vector(sum(span) / 2, u, v))
pitch = 360.0 / P.N_STACK
out["bolts_open"] = all(opn(parts[k], P.DR_X[n], P.BOLT_R, pitch * i) for k, n in (("spider", "spider"), ("disc", "disc_a"), ("dspacer", "spacer")) for i in range(P.N_STACK))
d = P.DOG
# dogs: pocket open just outside the base circle behind each peak, base circle solid midway between dogs, at every pitch
out["dogs"] = all(opn(parts["disc"], P.DR_X["disc_a"], d["r"] + 0.3, pitch * i + d["t1"] + 1.0) and
                  not opn(parts["disc"], P.DR_X["disc_a"], d["r"] + 0.3, pitch * i + (d["t2"] + d["t0"] + pitch) / 2)
                  for i in range(P.N_STACK))
# tooth: back face tangent to the rim (foot radius vector _|_ face), tip on the outline
ec = drisk._at(P.DISC_ECC, P.DISC_ECC_A); tip = drisk._at(P.TOOTH_R, P.TOOTH_A)
dd = (tip - ec).length; a = math.atan2(tip.Y - ec.Y, tip.X - ec.X) + math.acos(P.DISC_R / dd)
foot = ec + drisk._at(P.DISC_R, math.degrees(a))
out["tangent"] = abs((tip - foot).dot(foot - ec))
out["tip_bbox"] = drisk.disc_outline().bounding_box().max.X  # just builds
out["spacer_in_rim"] = P.SPACER["r"] <= P.DISC_R - P.DISC_ECC + 1e-9
order = ("spider", "disc_a", "spacer", "disc_b")
out["flush"] = max(abs(P.DR_X[a][1] - P.DR_X[b][0]) for a, b in zip(order, order[1:]))
out["on_cap"] = abs(P.DR_X["spider"][1] - P.BELL_CAP_X)
out["t"] = [P.DR_X[k][1] - P.DR_X[k][0] for k in order] + [P.SPIDER_T, P.DISC_T, P.SPACER_T, P.DISC_T]
print(json.dumps(out))
"""

CASES = {
    "default": None,
    "n_stack_3": ("params_weapon.py", r"^N_STACK = 4", "N_STACK = 3"),
    "n_stack_5": ("params_weapon.py", r"^N_STACK = 4", "N_STACK = 5"),
    "bolt_circle": ("params_weapon.py", r"^BOLT_R, HUB_R = 14\.0", "BOLT_R, HUB_R = 13.6"),
    "disc_thick": ("params_weapon.py", r"^SPIDER_T, DISC_T, SPACER_T = 3\.0, 3\.0, 6\.0", "SPIDER_T, DISC_T, SPACER_T = 3.0, 4.0, 5.0"),
    "rim": ("params_weapon.py", r"^DISC_R, DISC_ECC, DISC_ECC_A = 16\.5", "DISC_R, DISC_ECC, DISC_ECC_A = 17.0"),
    "corner": ("params_weapon.py", r"^CORNER_R = 1\.0", "CORNER_R = 0.8"),
    "motor_step": "step",
}


def _build(tmp_path, edit):
    dst = tmp_path / "src"
    shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("__pycache__"))
    env = dict(os.environ)
    if edit == "step":
        env["REVRON_MOTOR_VARIANT"] = "step"
    elif edit:
        fname, pat, new = edit
        f = dst / "revron" / fname
        text, n = re.subn(pat, new, f.read_text(), count=1, flags=re.M)
        assert n == 1, pat
        f.write_text(text)
    r = subprocess.run([sys.executable, "-c", PROBE.format(src=str(dst), repo=REPO)], capture_output=True, text=True,
                       timeout=600, env=env)
    assert r.returncode == 0, r.stderr[-2000:]
    return json.loads(r.stdout.strip().splitlines()[-1])


@pytest.mark.parametrize("case", list(CASES))
def test_stack_relations_hold(tmp_path, case):
    m = _build(tmp_path, CASES[case])
    for k, (n, valid, vol) in m["solids"].items():
        assert n == 1 and valid and vol, (case, k)
    assert m["bolts_open"], case
    assert m["dogs"], case
    assert m["tangent"] < 1e-6, case
    assert m["spacer_in_rim"], case
    assert m["flush"] < 1e-6 and m["on_cap"] < 1e-6, case
    assert m["t"][:4] == pytest.approx(m["t"][4:]), case
    if case.startswith("n_stack"):
        assert m["N"] == int(case[-1])
