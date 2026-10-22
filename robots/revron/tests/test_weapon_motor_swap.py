"""[fix-B-vers] The weapon motor swaps as ONE catalog setting (hooks.json `weapon.motor`, env REVRON_WEAPON_MOTOR), the
weapon style is a setting (`weapon.type`), and the weapon module follows the mount spacing MNT_IN.

Sweep: weapon motor (GR1507 datasheet / STEP, a larger one-piece BE1806, a smaller one-piece TC1404) x MNT_IN (STEP,
+-10 %). Each case runs in a fresh interpreter (the params are module constants) with MNT_IN edited in
params_chassis.py, builds RV03, the back spacer, the spider and the shaft, and checks the relations that must follow
the motor entry and MNT_IN:

- the motor's base back face sits LEAD_GAP + BSP_T inboard of RV03 (it is bolted to RV03), read off the catalog solid;
- RV03 is drilled on the motor's own base pattern: open on every hole axis, material closed round each hole; the
  counterbore floor keeps WM_WEB out from the inner face, and the screw tip bites WM_BITE inside the base flange;
- the back spacer has the same pattern open; its bore clears the base hub;
- the spider is drilled on the bell-top pattern, its bore on the shaft; the spider sits on the bell cap and the
  bell-screw heads stay inboard of RV02; the drisk spacer bore clears the bell;
- the shaft runs from the base back face to RV02's nut recess, in a catalog bearing of its own diameter.
"""
import json, os, re, shutil, subprocess, sys

import pytest

SRC = os.path.join(os.path.dirname(__file__), "..", "src")
ROOT = os.path.abspath(os.path.join(SRC, "..", "..", ".."))
HOOKS = os.path.join(SRC, "..", "hooks.json")
CODE = r"""
import json, math, sys
sys.path.insert(0, %r); sys.path.insert(0, sys.argv[1])
from revron import params as P, mount as M, drisk as D
import build123d as bd
from robot import catalog
from robot.shapes import to_solid
from robot.cad import fastener_catalog as fc
V = lambda *p: bd.Vector(*p)
out = dict(MNT_IN=P.MNT_IN, MOTOR=P.MOTOR, MOTOR_X=P.MOTOR_X, BASE_BACK_X=P.BASE_BACK_X, BSP_T=P.BSP_T, LEAD_GAP=P.LEAD_GAP,
           CB_FLOOR_X=P.CB_FLOOR_X, WM_LEN=P.WM_LEN, WM_BITE=P.WM_BITE, WM_WEB=P.WM_WEB, WM=P.WM, DR_X=P.DR_X, WSHAFT=P.WSHAFT,
           BRG=P.BRG, BRG_NAME=P.BRG_NAME, SHAFT_R=P.SHAFT_R, SPIDER_BORE=P.SPIDER["bore_r"], SPACER_BORE=P.SPACER["bore_r"],
           BSP_BORE=P.BSP["bore_r"], MNT_SLAB_T=P.MNT_SLAB_T, SHAFT_INTO_RECESS=P.SHAFT_INTO_RECESS, HUB_D=P.HUB_D)
st = to_solid(catalog.find(P.MOTOR["stator"]).shape)
can = to_solid(catalog.find(P.MOTOR["can"]).shape)
out["stator_bb"] = [st.bounding_box().min.X, st.bounding_box().max.X]
out["can_bb"] = [can.bounding_box().min.X, can.bounding_box().max.X]
out["solids"] = dict(stator=[len(st.solids()), st.is_valid], can=[len(can.solids()), can.is_valid])
mr, sp, spi, sh = M.weapon_mount("r"), M.motor_back_spacer(), D.spider(), D.weapon_shaft()
out["solids"].update(mount_r=[len(mr.solids()), mr.is_valid], spacer=[len(sp.solids()), sp.is_valid], spider=[len(spi.solids()), spi.is_valid], shaft=[len(sh.solids()), sh.is_valid])
holes = []
for dy, dz, d in P.STATOR_HOLES:
    y, z = P.WY + dy, P.WZ + dz
    r = fc.clearance(d, "close") / 2
    ring = lambda x, rr: all(mr.is_inside(V(x, y + rr * math.cos(a), z + rr * math.sin(a))) for a in [k * math.pi / 6 for k in range(12)])
    holes.append(dict(open_mount=not mr.is_inside(V(P.MNT_IN + 0.5, y, z)), closed_mount=ring(P.MNT_IN + 0.5, r + 0.5),
                      open_spacer=not sp.is_inside(V(P.MNT_IN - P.BSP_T / 2, y, z))))
out["holes"] = holes
bx = P.W_FRAME[0] + P.DR_X["spider"][0] + P.SPIDER_T / 2
out["bell_holes"] = [not spi.is_inside(V(bx, *D._disc_local(*c))) for c in M._polar(P.HUB_R, P.N_HUB)]
out["spider_on_axis_open"] = not spi.is_inside(V(bx, P.WY, P.WZ))
bb = sh.bounding_box()
out["shaft_x"] = [bb.min.X, bb.max.X]
out["button_k"] = fc.head(P.HUB_D, "button")[1]
print(json.dumps(out, default=list))
""" % ROOT

MNT_IN0 = 13.4
MOTORS = ("gr1507", "gr1507_step", "bbb_be1806_2300kv", "brotherhobby_tc1404_3800kv")
CASES = {f"{m}@{k}": (m, v) for m in MOTORS for k, v in (("step", None), ("+10", round(MNT_IN0 * 1.1, 6)), ("-10", round(MNT_IN0 * 0.9, 6)))
         if not (m == "brotherhobby_tc1404_3800kv" and k == "-10")}
# the stack does not fit between the mounts: the GR1507 at MNT_IN -10 % (2.4 mm of head room, 2.68 taken), the BE1806
# (1.4 mm longer body) at -10 %; they must fail with the reason, not build a clash
NO_FIT = {"gr1507@-10", "bbb_be1806_2300kv@-10"}


def _src(mnt_in, tmp):
    if mnt_in is None:
        return SRC
    dst = os.path.join(tmp, "src")
    shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("__pycache__"))
    f = os.path.join(dst, "revron", "params_chassis.py")
    txt, n = re.subn(r"^MNT_IN, MNT_T, MNT_SLAB_T = 13\.4,", f"MNT_IN, MNT_T, MNT_SLAB_T = {mnt_in!r},", open(f).read(), count=1, flags=re.M)
    assert n == 1
    open(f, "w").write(txt)
    return dst


def _run(code, src, env):
    e = {k: v for k, v in os.environ.items() if not k.startswith("REVRON_")}
    e.update(env)
    return subprocess.run([sys.executable, "-c", code, src], env=e, capture_output=True, text=True, cwd=ROOT)


@pytest.mark.parametrize("case", list(CASES))
def test_weapon_follows_motor_and_mnt_in(case, tmp_path):
    motor, mnt_in = CASES[case]
    p = _run(CODE, _src(mnt_in, str(tmp_path)), {"REVRON_WEAPON_MOTOR": motor})
    if case in NO_FIT:
        assert p.returncode != 0 and "does not fit between the mounts" in p.stderr, p.stderr[-1500:]
        return
    assert p.returncode == 0, p.stderr[-3000:]
    r = json.loads(p.stdout.strip().splitlines()[-1])
    W = r["WM"]
    assert r["MNT_IN"] == (mnt_in or MNT_IN0)
    for k, (n, ok) in r["solids"].items():
        assert n == 1 and ok, (case, k)
    # the motor is bolted to RV03: base back face LEAD_GAP + BSP_T inboard of the inner face (catalog solid, flipped)
    assert abs(r["BASE_BACK_X"] - (r["MNT_IN"] - r["BSP_T"] - r["LEAD_GAP"])) < 1e-6, case
    assert abs(r["stator_bb"][0] - W["back_x"]) < 0.05, (case, r["stator_bb"])
    assert abs(r["can_bb"][1] - W["cap_x"]) < 0.05, (case, r["can_bb"])
    if motor == "gr1507" and mnt_in is None:   # the STEP layout: motor origin on the centre plane, M2x8, floor 16.7
        assert r["MOTOR_X"] == 0.0 and r["WM_LEN"] == 8.0 and abs(r["CB_FLOOR_X"] - 16.7) < 1e-9 and r["BRG_NAME"] == "mr85"
    # stator screws: on the motor's pattern in RV03 and the back spacer; reach and bite
    assert len(r["holes"]) == len(W["base_holes"])
    for h in r["holes"]:
        assert h["open_mount"] and h["closed_mount"] and h["open_spacer"], (case, h)
    assert r["CB_FLOOR_X"] >= r["MNT_IN"] + r["WM_WEB"] - 1e-6, case
    tip = r["CB_FLOOR_X"] - r["WM_LEN"]
    assert r["BASE_BACK_X"] - W["base_h"] < tip < r["BASE_BACK_X"], (case, tip)
    assert r["BSP_BORE"] > W["base_hub_r"], case
    # spider on the bell cap, drilled on the bell pattern, bore on the shaft; heads clear of RV02
    assert all(r["bell_holes"]) and r["spider_on_axis_open"], case
    assert abs(r["DR_X"]["spider"][1] + W["cap_x"]) < 1e-6, case
    assert r["MOTOR_X"] + r["DR_X"]["spider"][0] - r["button_k"] > -r["MNT_IN"], (case, "bell screw heads reach RV02")
    assert r["SPIDER_BORE"] > r["SHAFT_R"] and r["SPACER_BORE"] > W["bell_r"], case
    # shaft: base back face to RV02's nut recess, in a bearing of its own bore
    assert abs(r["shaft_x"][1] - r["BASE_BACK_X"]) < 1e-3, (case, r["shaft_x"])
    assert abs(r["shaft_x"][0] + (r["MNT_IN"] + r["MNT_SLAB_T"] + r["SHAFT_INTO_RECESS"])) < 1e-3, (case, r["shaft_x"])
    assert abs(r["BRG"]["bore_r"] - r["SHAFT_R"]) < 1e-9 and r["SHAFT_R"] == W["shaft_r"], case


@pytest.mark.parametrize("motor,why", [("repeat_2004_1400kv", "does not fit the disc dog bore"), ("emax_eco2207_1900kv", "does not declare top_holes"),
                                       ("c_bbb_be1806_2300kv", "one piece and declares no mounting geometry"), ("no_such_motor", "not a catalog weapon motor")])
def test_unfit_motor_fails_clearly(motor, why):
    p = _run("import sys; sys.path.insert(0, sys.argv[1]); import revron.params", SRC, {"REVRON_WEAPON_MOTOR": motor})
    assert p.returncode != 0 and "WeaponMotorError" in p.stderr and why in p.stderr, p.stderr[-800:]


@pytest.mark.parametrize("value,why", [("vspin_drum", "is not implemented"), ("hspin_bar", "is not implemented"), ("saw", "is unknown")])
def test_weapon_type_setting(value, why):
    p = _run("import sys; sys.path.insert(0, sys.argv[1]); import revron.params", SRC, {"REVRON_WEAPON_TYPE": value})
    assert p.returncode != 0 and "WeaponTypeError" in p.stderr and why in p.stderr and "drisk" in p.stderr, p.stderr[-800:]
    ok = _run("import sys; sys.path.insert(0, sys.argv[1]); import revron.params as P; print(P.WEAPON_TYPE)", SRC, {"REVRON_WEAPON_TYPE": "drisk"})
    assert ok.returncode == 0 and ok.stdout.strip().endswith("drisk"), ok.stderr[-800:]


def test_settings_match_catalog_and_hooks():
    """Every catalog weapon motor is a value of the setting (and of hooks.json `weapon.motor`); weapon.type values too."""
    sys.path.insert(0, ROOT)
    sys.path.insert(0, SRC)
    from robot import catalog
    from revron import params_weapon as PW
    ids = {e.id for e in catalog.catalog() if e.kind == "weapon_motor" and not (e.props or {}).get("half_of")}
    assert set(PW.WEAPON_MOTORS) == ids
    h = json.load(open(HOOKS))["hooks"]
    assert set(h["weapon.motor"]["values"]) == ids and h["weapon.motor"]["swap"] == "weapon_motor"
    assert h["weapon.motor"]["default"] == "gr1507" and h["weapon.type"]["default"] == "drisk"
    assert set(h["weapon.type"]["values"]) == set(PW.WEAPON_TYPES)


def test_weapon_motor_swap_is_one_setting():
    """The change generator turns every weapon-motor swap into the one `weapon.motor` setting (stator + bell together)."""
    sys.path.insert(0, ROOT)
    from robot import overlay as O
    from robot.gen import changes as C
    raw = json.load(open(os.path.join(SRC, "..", "spec.json")))
    hooks = O.load_hooks(raw, os.path.join(SRC, ".."))
    sw = [c for c in C.change_hypotheses(raw, hooks) if c.id.startswith("swap:weapon_motor:")]
    assert sw and all(c.ops == [{"op": "hook", "name": "weapon.motor", "value": c.id.split("->")[1]}] for c in sw)
    assert not any("__" in c.id for c in sw)   # derived halves are not candidates
    assert not any(c.id.startswith("arch:weapon.motor=") for c in C.change_hypotheses(raw, hooks))
