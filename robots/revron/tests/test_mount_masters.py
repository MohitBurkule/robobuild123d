"""[fix-B-relm] Weapon mounts RV02/RV03 and the motor back spacer stay valid when a master changes or a part is swapped:
mount thickness / slab thickness (chassis masters), outboard bearing (catalog), GR1507 motor variant. Each case rebuilds
the parts in a fresh interpreter (masters patched, then the param and mount modules reloaded) and checks the relations:
one valid solid, bores and stator holes on centre, the notch clear of the chassis tab with material behind it, the
standoff screw holes open, the spacer holes on the stator bolt circle."""
import json, os, subprocess, sys

import pytest

SRC = os.path.join(os.path.dirname(__file__), "..", "src")
ROOT = os.path.abspath(os.path.join(SRC, "..", "..", ".."))
CODE = r"""
import importlib, json, math, sys
sys.path.insert(0, %r); sys.path.insert(0, %r)
over = json.loads(sys.argv[1])
from robot import catalog
if "bearing_od" in over:
    b = catalog.BEARINGS["mr85"]; catalog.BEARINGS["mr85"] = (b[0], over.pop("bearing_od"), b[2])
from revron import params_chassis as C
for k, v in over.items():
    setattr(C, k, v)
C.MNT_OUT, C.MNT_SLAB = C.MNT_IN + C.MNT_T, C.MNT_IN + C.MNT_SLAB_T
from revron import params_weapon as W, params as P, mount as M
for m in (W, P, M):
    importlib.reload(m)
import build123d as bd
out = {}
def inside(s, p):
    return bool(s.is_inside(bd.Vector(*p)))
for side in ("r", "l"):
    s = M.weapon_mount(side)
    sg = 1 if side == "r" else -1
    x = lambda d: sg * (P.MNT_IN + d)
    mid = P.MNT_SLAB_T / 2
    bb = s.bounding_box()
    tab = P.TAB
    r = dict(n=len(s.solids()), valid=s.is_valid, xspan=bb.max.X - bb.min.X,
             bore=not inside(s, (x(mid), P.WY, P.WZ)),
             bore_r=(P.RV03_BORE_R if side == "r" else P.BRG_SEAT_R),
             bore_wall=inside(s, (x(mid), P.WY, P.WZ + (P.RV03_BORE_R if side == "r" else P.BRG_SEAT_R) + 0.3)),
             screws=[not inside(s, (x(mid), y, z)) for y, z in (P.SA, P.SB)],
             tab_clear=not inside(s, (x(mid), (tab["y0"] + tab["y1"]) / 2, tab["z0"] + tab["h"] / 2)),
             over_tab=inside(s, (x(mid), (tab["y0"] + tab["y1"]) / 2, tab["z0"] + tab["h"] + 0.5)),
             hook=inside(s, (x(mid), tab["y0"] - P.MNT_HEEL["back"] / 2, (P.MNT_HEEL["z_hook"] + P.MNT_HEEL["z_lip"]) / 2)))
    if side == "r":
        r["stator"] = [not inside(s, (x(mid), P.WY + dy, P.WZ + dz)) for dy, dz in M.stator_bolt_circle()]
    out[side] = r
sp = M.motor_back_spacer()
xs = P.MNT_IN - P.BSP_T / 2
out["bsp"] = dict(n=len(sp.solids()), valid=sp.is_valid,
                  holes=[not inside(sp, (xs, P.WY + dy, P.WZ + dz)) for dy, dz in M.stator_bolt_circle()],
                  rim=inside(sp, (xs, P.WY, P.WZ + P.BSP["r"] - P.BSP_T / 2)), bore=not inside(sp, (xs, P.WY, P.WZ)))
out["masters"] = dict(MNT_T=C.MNT_T + P.BOSS_OVER, MNT_SLAB_T=C.MNT_SLAB_T)   # the boss may keep its BOSS_OVER where the batter runs past MNT_T
print(json.dumps(out))
""" % (ROOT, SRC)

CASES = {
    "default": ({}, {}),
    "motor_step": ({}, {"REVRON_MOTOR_VARIANT": "step"}),
    "motor_datasheet": ({}, {"REVRON_MOTOR_VARIANT": "datasheet"}),
    "thick_mount": ({"MNT_T": 9.0}, {}),
    "thin_slab": ({"MNT_SLAB_T": 3.5}, {}),
    "bigger_bearing": ({"bearing_od": 9.0}, {}),
    "printable_groove": ({}, {"REVRON_MOUNT_VARIANT": "printable", "REVRON_LEAD_GROOVE": "on"}),
}


def _run(over, env):
    e = dict(os.environ, **env)
    p = subprocess.run([sys.executable, "-c", CODE, json.dumps(over)], env=e, capture_output=True, text=True, cwd=ROOT)
    assert p.returncode == 0, p.stderr[-2000:]
    return json.loads(p.stdout.strip().splitlines()[-1])


@pytest.mark.parametrize("case", sorted(CASES))
def test_mount_relations_hold(case):
    r = _run(*CASES[case])
    for side in ("r", "l"):
        m = r[side]
        assert m["n"] == 1 and m["valid"], (case, side)
        assert m["xspan"] <= r["masters"]["MNT_T"] + 1e-3 and m["xspan"] >= r["masters"]["MNT_SLAB_T"] - 1e-3, (case, side)
        assert m["bore"] and m["bore_wall"], (case, side)        # bore on the weapon axis, wall right outside its radius
        assert all(m["screws"]), (case, side)                   # standoff CSK holes open on SA / SB
        assert m["tab_clear"] and m["over_tab"] and m["hook"], (case, side)  # notch drops over the tab, heel hooks under it
    assert all(r["r"]["stator"]), case                          # RV03 stator holes on the bolt circle
    b = r["bsp"]
    assert b["n"] == 1 and b["valid"] and all(b["holes"]) and b["rim"] and b["bore"], case
