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
    over = {"params_chassis": {"BATTERY": repr("synth_pack")}}
    _, bb = check(over, tmp_path, SYNTH_PACK % pack, what="tub.bat_pad()", symmetric=False)
    x0, x1, y0, y1, z0, z1 = bb
    L, W, H = pack
    assert abs(z1 - (17.5 - H)) < 1e-6                     # pad top = pack underside: the pack top rests on the deck underside (17.5)
    assert abs(x1 - x0 - W / 3) < 1e-3 and abs(y1 - y0 - L / 3) < 1e-3


BAYS = """
import sys, os
sys.path[:0] = [%r, %r]
from revron import tub2, tub2_bays as B, hw, params as P
from revron.params import *
tub = tub2.chassis2()
keep = B._U(*B.KEEP)
print("TUB", len(tub.solids()), tub.is_valid, round(tub.volume, 3))
for pid, cid, at, rot in (("motor_l", DRIVE_MOTOR, (-MOTX, RY, RZ), (0, 0, 180)), ("motor_r", DRIVE_MOTOR, (MOTX, RY, RZ), (0, 0, 0)),
                          ("battery", BATTERY, ELEC["battery"], (0, 0, 90)), ("rxesc", RXESC, RX_C, (0, 0, 90)), ("wesc", WESC, WE_C, (0, 0, 90)),
                          ("power_switch", SWITCH, (SWX, *ELEC["switch_yz"]), (0, 0, 90))):
    sol = hw.placed(cid, at, rot)
    print("OVL", pid, round(((tub & sol) - keep).volume, 4), round((tub & sol).volume, 4))   # clear of the tub outside the heat-set bore sleeves
    print("SLV", pid, round((sol & keep).volume, 4))                                          # nothing stands in a heat-set bore sleeve
print("PACK", ELEC["battery"][1], KEY_SPAN[1] + BAT_L / 2, ELEC["battery"][2] + BAT_H / 2)
print("WALL", CH_Y1, WALL_IN_FRONT, ELEC["battery"][1] + BAT_L / 2, INS[4][0], INS[4][1])
"""


def bays(env, tmp_path):
    """Build the tub in a fresh interpreter with the REVRON_* masters in `env`; {'tub': (solids, valid, volume), 'ovl': {part: volume outside the bore sleeves}, 'pack': (Y, Y_expected, top)}."""
    dst = pathlib.Path(tempfile.mkdtemp(dir=tmp_path)) / "src"
    shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("__pycache__"))
    r = subprocess.run([sys.executable, "-c", BAYS % (str(dst), ROOT)], capture_output=True, text=True, env={**os.environ, **env})
    rows = [ln.split() for ln in r.stdout.splitlines()]
    assert any(x[0] == "TUB" for x in rows), r.stderr[-1500:]
    tub = next(x for x in rows if x[0] == "TUB")
    return dict(tub=(int(tub[1]), tub[2] == "True", float(tub[3])), ovl={x[1]: float(x[2]) for x in rows if x[0] == "OVL"},
                slv={x[1]: float(x[2]) for x in rows if x[0] == "SLV"}, wall=[float(v) for v in next(x for x in rows if x[0] == "WALL")[1:]],
                pack=[float(v) for v in next(x for x in rows if x[0] == "PACK")[1:]])


DEFAULT_TUB_VOLUME = 15814.91   # mm3 at the shipped masters (the tub as the designer drew it, before the compartment pockets; lobe-root round trimmed at the floor in r53: +0.33 mm3)


def test_default_tub_is_unchanged_by_the_compartment_pockets(tmp_path):
    """The shipped motor, pack and ESCs clear the tub, so no pocket is cut: the volume is the drawn tub's."""
    b = bays({}, tmp_path)
    assert b["tub"][:2] == (1, True) and abs(b["tub"][2] - DEFAULT_TUB_VOLUME) < 1e-2 and all(v == 0 for v in b["ovl"].values()), b


@pytest.mark.parametrize("motor", ["bbb_hpn20_1000rpm", "bbb_n10_600rpm", "pololu_hpcb6v_30to1", "n20_1000rpm_6v"])
def test_drive_motor_swap_gets_its_pocket(motor, tmp_path):
    """Another catalog gearmotor (wider, longer): the stack end sets MOTX, the width sets the stop wall and key, and what still reaches the wall or boss is pocketed from the motor's own catalog solid, so it clears the tub outside the insert bores."""
    b = bays({"REVRON_DRIVE_MOTOR": motor}, tmp_path)
    assert b["tub"][:2] == (1, True) and b["ovl"]["motor_l"] == 0 and b["ovl"]["motor_r"] == 0 and b["ovl"]["battery"] == 0, b


@pytest.mark.parametrize("pack", ["betafpv_2s_300_45c", "palmpower_2s_300_65c", "tattu_2s_300_75c_hv", "gnb_3s_300_80c_hv"])
def test_battery_swap_gets_its_bay(pack, tmp_path):
    """Another catalog pack: it stands against the stop wall (Y) and under the deck (Z) and its bay is cut from its own envelope."""
    b = bays({"REVRON_BATTERY": pack}, tmp_path)
    assert b["tub"][:2] == (1, True) and b["ovl"]["battery"] == 0 and abs(b["pack"][0] - b["pack"][1]) < 1e-6 and abs(b["pack"][2] - 17.5) < 1e-6, b


def test_wider_motor_pushes_the_pack_forward(tmp_path):
    """The stop wall front face follows the gearmotor's width, and the pack stands against it."""
    wide = bays({"REVRON_DRIVE_MOTOR": "bbb_hpn20_1000rpm"}, tmp_path)["pack"][0]
    assert wide > bays({}, tmp_path)["pack"][0]


@pytest.mark.parametrize("env", [{"REVRON_RXESC": "esc_dual_brushed"}, {"REVRON_WESC": "bbb_red_esc"}, {"REVRON_RXESC": "bbb_dual_esc_v31"}])
def test_esc_swap_gets_its_bay(env, tmp_path):
    """Another catalog ESC: its bay is cut from its envelope."""
    b = bays(env, tmp_path)
    assert b["tub"][:2] == (1, True) and b["ovl"]["rxesc"] == 0 and b["ovl"]["wesc"] == 0, b


def test_compartments_setting(tmp_path):
    """chassis.compartments: none drops the motor locating features, split_battery_bay adds the rib between the pack bay and the electronics bay; each is one valid solid and the parts still clear the tub."""
    std = bays({}, tmp_path)["tub"][2]
    none = bays({"REVRON_COMPARTMENTS": "none"}, tmp_path)
    split = bays({"REVRON_COMPARTMENTS": "split_battery_bay"}, tmp_path)
    assert none["tub"][:2] == split["tub"][:2] == (1, True)
    assert none["tub"][2] < std < split["tub"][2]
    assert all(v == 0 for v in none["ovl"].values()) and all(v == 0 for v in split["ovl"].values())


@pytest.mark.parametrize("loc", ["mid", "front"])
def test_drive_location_setting(loc, tmp_path):
    """drive.location: the drive axle line moves, and the keyhole, key tab, stop wall, pad recess and the pack follow it (the rear-only structure stays); still one valid solid and the pack stands against the stop wall."""
    b = bays({"REVRON_DRIVE_LOCATION": loc}, tmp_path)
    assert b["tub"][:2] == (1, True) and abs(b["pack"][0] - b["pack"][1]) < 1e-6 and b["tub"][2] != DEFAULT_TUB_VOLUME, b


def test_top_screw_web_switch_off(tmp_path):
    """TOP_SCREW_WEB off: the corner columns keep the STEP's through-bore; the tub is still one valid solid."""
    check({"params_chassis": {"TOP_SCREW_WEB": "False"}}, tmp_path)


# ---- the standoffs SA / SB (master params): the tub follows them -----------------------------------------------------------------
# +-10 % of each coordinate, one at a time. The tub, and everything that sits against it, must stay valid and clear of it.
SA_SB_CASES = [("SA", "(33.55, 5.5)"), ("SA", "(27.45, 5.5)"), ("SA", "(30.5, 6.05)"), ("SA", "(30.5, 4.95)"),
               ("SB", "(44.55, 4.5)"), ("SB", "(36.45, 4.5)"), ("SB", "(40.5, 4.95)"), ("SB", "(40.5, 4.05)")]
# the wedgelet (armor, params_side WG_*) does not build at SA[0] +10 % (its R10 cheek flank can no longer reach the K line) and at SB[0] -10 % (T misses the SB ring)
WEDGELET_BUILDS = {c: c not in (("SA", "(33.55, 5.5)"), ("SB", "(36.45, 4.5)")) for c in SA_SB_CASES}

OVERLAP = """
import sys
sys.path[:0] = [%r, %r]
import build123d as b
from revron import assembly as A
from revron.params import SA, SB, MNT_IN, SA_X, SB_X, M3
tub = A.build("chassis")
shank = lambda yz, x0, x1: b.Pos((x0 + x1) / 2, *yz) * b.Rotation(0, 90, 0) * b.Cylinder(M3 / 2, x1 - x0)   # the M3 screw through the mount into the standoff
tools = {"shank_a": shank(SA, MNT_IN, SA_X[0] + 3), "shank_b": shank(SB, MNT_IN, SB_X[0] + 3)}
for p in %r:
    try:
        tools[p] = A.build(p)
    except Exception as e:
        print("BUILDFAIL", p, type(e).__name__)
for k, v in tools.items():
    print("OVERLAP", k, round((tub & v).volume, 4))
"""


def overlaps(overrides, tmp_path, parts):
    dst = pathlib.Path(tempfile.mkdtemp(dir=tmp_path)) / "src"
    shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("__pycache__"))
    for mod, names in overrides.items():
        f = dst / "revron" / f"{mod}.py"
        text = f.read_text()
        for name, expr in names.items():
            text, n = re.subn(rf"^{name} = [^#\n]*", f"{name} = {expr}   ", text, count=1, flags=re.M)
            assert n == 1
        f.write_text(text)
    r = subprocess.run([sys.executable, "-c", OVERLAP % (str(dst), ROOT, parts)], capture_output=True, text=True)
    assert "OVERLAP" in r.stdout, r.stderr[-1500:]
    return {ln.split()[1]: float(ln.split()[2]) for ln in r.stdout.splitlines() if ln.startswith("OVERLAP")}, r.stdout


@pytest.mark.parametrize("name,val", SA_SB_CASES)
def test_standoff_sweep_tub_is_one_valid_solid(name, val, tmp_path):
    """SA / SB +-10 % per coordinate: the lug, tab, key and flange follow (no fillet or boolean failure, one closed solid, still symmetric)."""
    check({"params_chassis": {name: val}}, tmp_path)


@pytest.mark.parametrize("name,val", SA_SB_CASES)
def test_standoff_sweep_tub_clears_what_sits_on_it(name, val, tmp_path):
    """The mount screws through SA / SB, the standoffs, both mounts, the side panel and (where it builds) the wedgelet never overlap the tub."""
    parts = ["so_a_l", "so_b_l", "mount_l", "mount_r", "side_panel_l"] + (["wedgelet_l"] if WEDGELET_BUILDS[(name, val)] else [])
    vol, out = overlaps({"params_chassis": {name: val}}, tmp_path, parts)
    assert all(v < 0.01 for v in vol.values()) and len(vol) == len(parts) + 2 and "BUILDFAIL" not in out, vol


@pytest.mark.parametrize("name,val", SA_SB_CASES)
def test_standoff_sweep_side_panel_is_one_valid_solid(name, val, tmp_path):
    """The side panel's post, notch and screw seats follow SA / SB too (its fillet R1 and its heads sunk below the battered face)."""
    check({"params_chassis": {name: val}}, tmp_path, what="__import__('revron.assembly', fromlist=['build']).build('side_panel_l')", symmetric=False)


MESH = """
import sys
sys.path[:0] = [%r, %r]
import trimesh
from revron import assembly as A
from robot import geom
from robot.checks.integrity import shells
c = A.build("chassis")
for nm, t in (("FINE", geom.FINE), ("FAST", geom.FAST)):
    v, f = geom.tessellate(c, t)
    m = trimesh.Trimesh(v, f)
    print("MESH", nm, *shells(m))
"""


@pytest.mark.parametrize("name,val", [("SA", "(27.45, 5.5)"), ("SA", "(33.55, 5.5)"), ("SB", "(44.55, 4.5)"), ("SB", "(40.5, 4.05)")])
def test_standoff_sweep_tub_mesh_is_one_closed_shell(name, val, tmp_path):
    """The tub as the integrity check meshes it (FINE and FAST tessellation): exactly one closed shell and no open or lone-triangle pieces."""
    dst = pathlib.Path(tempfile.mkdtemp(dir=tmp_path)) / "src"
    shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("__pycache__"))
    f = dst / "revron" / "params_chassis.py"
    text, n = re.subn(rf"^{name} = [^#\n]*", f"{name} = {val}   ", f.read_text(), count=1, flags=re.M)
    assert n == 1
    f.write_text(text)
    r = subprocess.run([sys.executable, "-c", MESH % (str(dst), ROOT)], capture_output=True, text=True)
    rows = [ln.split() for ln in r.stdout.splitlines() if ln.startswith("MESH")]
    assert len(rows) == 2, r.stderr[-1500:]
    assert all(row[2] == "1" and row[3] == "0" for row in rows), rows


def value_with(overrides, tmp_path, expr):
    """repr-evaluated `expr` (an expression in the revron package) in a fresh interpreter with the module-level assignments overridden."""
    dst = pathlib.Path(tempfile.mkdtemp(dir=tmp_path)) / "src"
    shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("__pycache__"))
    for mod, names in overrides.items():
        f = dst / "revron" / f"{mod}.py"
        text = f.read_text()
        for name, e in names.items():
            text, n = re.subn(rf"^{name} = [^#\n]*", f"{name} = {e}   ", text, count=1, flags=re.M)
            assert n == 1
        f.write_text(text)
    code = f"import sys; sys.path[:0] = [{str(dst)!r}, {ROOT!r}]\nfrom revron import params\nprint('VALUE', repr({expr}))"
    r = subprocess.run([sys.executable, "-c", code], capture_output=True, text=True)
    out = [ln for ln in r.stdout.splitlines() if ln.startswith("VALUE")]
    assert out, r.stderr[-1500:]
    return eval(out[-1][6:])


@pytest.mark.parametrize("name,val,wz", [("SA", "(30.5, 6.05)", 24.05), ("SB", "(40.5, 4.95)", 23.95), ("SA", "(30.5, 4.95)", 23.5), ("SB", "(44.55, 4.5)", 23.5)])
def test_rotor_axis_keeps_its_distance_to_the_mount_screws(name, val, wz, tmp_path):
    """The weapon axis rises with the standoffs (the mount screws back out inboard past the disc) and never drops below its master WZ."""
    assert abs(value_with({"params_chassis": {name: val}}, tmp_path, "params.WZ") - wz) < 1e-6


# ---- parts that reach the heat-set bore sleeves: the rear boss, the column rows and the front wall are relations to what sits in the tub ----
REAR_BOSS_Y = -33.6   # the default boss (one wall in front of the rear inner face)


def test_default_boss_and_columns_unchanged(tmp_path):
    """The shipped motor does not reach the boss: it stays one wall off the rear wall, the columns and the front wall are the stock ones."""
    b = bays({}, tmp_path)
    assert b["wall"][0] == 15.0 and b["wall"][3:] == [0.0, REAR_BOSS_Y] and all(v == 0 for v in b["slv"].values()), b


@pytest.mark.parametrize("motor", ["pololu_hpcb6v_30to1", "bbb_n20_600rpm", "c_pair_of_600rpm_antweight_n20_gearmotors", "c_bbb_high_power_n20_gearmotor"])
def test_rear_boss_moves_clear_of_a_long_gearmotor(motor, tmp_path):
    """A motor whose stack reaches the rear boss's bore sleeve: the boss (and with it the base panel's insert hole, the lattice window and the deck pocket collars) moves out in front of the motor; the tub stays one solid and no part stands in any sleeve."""
    b = bays({"REVRON_DRIVE_MOTOR": motor}, tmp_path)
    assert b["tub"][:2] == (1, True) and b["wall"][4] > REAR_BOSS_Y and all(v == 0 for v in b["slv"].values()) and all(v == 0 for v in b["ovl"].values()), b


@pytest.mark.parametrize("pack", ["gnb_2s_450_80c", "betafpv_2s_300_45c", "palmpower_2s_300_65c", "gnb_3s_300_80c_hv"])
def test_long_pack_moves_the_front_wall_not_into_it(pack, tmp_path):
    """A pack longer than the stock wall holds: the front wall (and the front column row with it) moves forward, as far as the weapon-mount tab allows, and no part stands in a sleeve."""
    b = bays({"REVRON_BATTERY": pack}, tmp_path)
    assert b["tub"][:2] == (1, True) and b["wall"][0] > 15.0 and all(v == 0 for v in b["slv"].values()), b


@pytest.mark.parametrize("loc", ["mid", "front"])
def test_drive_location_clears_the_sleeves(loc, tmp_path):
    """drive.location mid / front: the motor plates and the pack stand clear of every column sleeve and the boss."""
    b = bays({"REVRON_DRIVE_LOCATION": loc}, tmp_path)
    assert b["tub"][:2] == (1, True) and all(v == 0 for v in b["slv"].values()) and all(v == 0 for v in b["ovl"].values()), b


# ---- the nose and the axle heights follow the wheels --------------------------------------------------------------------------------
@pytest.mark.parametrize("od", [18.0, 22.0, 26.0])
def test_front_wheel_od_drives_the_nose(od, tmp_path):
    """WHEEL_OD_F 18..26: the front axle stands at the wheel radius, the nose standoff stays a clearance outside the tyre, and the tub is one valid solid."""
    over = {"params_chassis": {"WHEEL_OD_F": repr(od)}}
    check(over, tmp_path)
    sa, sb, so_r, clr = (value_with(over, tmp_path, e) for e in ("params.SA", "params.SB", "params.SO_R", "params.SB_WHEEL_CLR"))
    assert abs(sa[1] - od / 2) < 1e-9 and abs(sb[1] - (sa[1] - 1.0)) < 1e-9
    assert ((sb[0] - sa[0]) ** 2 + (sb[1] - sa[1]) ** 2) ** 0.5 >= od / 2 + so_r + clr - 1e-6 and sb[0] >= 40.5


def test_front_wheel_default_nose_is_the_step(tmp_path):
    assert value_with({}, tmp_path, "(params.SA, params.SB, params.WHEEL_OD_F)") == ((30.5, 5.5), (40.5, 4.5), 11.0)


@pytest.mark.parametrize("rz", [9.25, 13.25])
def test_axle_height_drives_the_drive_features(rz, tmp_path):
    """The N10 axle height RZ (a rear wheel of OD 2 * (RZ - gap)): keyhole, key tab Z, wire slot, pockets and the motor pocket follow it; one valid solid."""
    dst = pathlib.Path(tempfile.mkdtemp(dir=tmp_path)) / "src"
    shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("__pycache__"))
    f = dst / "revron" / "params_chassis.py"
    text, n = re.subn(r"^RY, RZ = ([^#\n]*?),[^,#\n]*(?=\s*#)", lambda m: f"RY, RZ = {m.group(1)}, {rz}", f.read_text(), count=1, flags=re.M)
    assert n == 1
    f.write_text(text)
    r = subprocess.run([sys.executable, "-c", BUILD % (str(dst), ROOT, "", "tub2.chassis2()")], capture_output=True, text=True)
    out = [ln for ln in r.stdout.splitlines() if ln.startswith("RESULT")]
    assert out, r.stderr[-1500:]
    n, ok, vol, asym, *_ = out[-1].split()[1:]
    assert int(n) == 1 and ok == "True" and abs(float(asym)) < 1e-3


# ---- weapon interface (params_weapon.tub_interface): the tab, key, slot and wall follow the weapon type and the spider seat ----------------
WEAPON_MOTOR_BUILDS = ["gr1507", "gr1507_step", "bbb_be1806_2300kv"]    # the catalog weapon motors the drisk can be fitted with


def test_standoff_ends_follow_the_mount(tmp_path):
    from_p = value_with({}, tmp_path, "[params.SA_X0, params.SB_X0, params.MNT_IN, params.MNT_T, params.MNT_SLAB_T]")
    sa, sb, mi, mt, ms = from_p
    assert abs(sa - (mi + ms + 0.1)) < 1e-9 and abs(sb - (mi + mt + 0.1)) < 1e-9 and (sa, sb) == (17.5, 21.5)


SPIDER_PROBE = """
import sys
sys.path[:0] = [%r, %r]
import os
os.environ['REVRON_WEAPON_MOTOR'] = %r
from revron import tub2, tub2_tab, assembly as A
c = tub2.chassis2()
print("RESULT", len(c.solids()), c.is_valid, round(c.volume, 1))
print("SPIDER", round((c & A.build("spider")).volume, 4), round((c & A.build("disc_a")).volume, 4), round((c & A.build("disc_b")).volume, 4),
      round(tub2_tab.WALL_X[0] - tub2_tab.SPIDER_OUT, 4), round(tub2_tab.rub_point()[0], 4), round(tub2_tab.WALL_X[1], 4))
"""


@pytest.mark.parametrize("motor", WEAPON_MOTOR_BUILDS)
def test_weapon_motor_swap_tub_is_valid_and_clear_of_the_spider(motor, tmp_path):
    """Each buildable weapon.motor: one valid tub, no volume shared with the spider / discs, the tab wall stands SPIDER_TAB_GAP off the spider's outer face, inboard of the mount."""
    dst = pathlib.Path(tempfile.mkdtemp(dir=tmp_path)) / "src"
    shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("__pycache__"))
    r = subprocess.run([sys.executable, "-c", SPIDER_PROBE % (str(dst), ROOT, motor)], capture_output=True, text=True)
    res = [ln.split() for ln in r.stdout.splitlines() if ln.startswith(("RESULT", "SPIDER"))]
    assert len(res) == 2, r.stderr[-1500:]
    assert res[0][1:3] == ["1", "True"], res
    sp, da, db, gap, rub, wx1 = map(float, res[1][1:])
    assert sp < 0.01 and da < 0.01 and db < 0.01, res
    assert gap >= 0.6 - 1e-6 and abs(rub) >= 10.3 - 1e-6 and wx1 < 13.4, res


def test_weapon_without_a_tab_gives_a_valid_tub_with_no_tab_features(tmp_path):
    """A weapon type that has no notch tab: empty tab / key / slot / rabbet, no rub point, still one valid closed solid."""
    off = {"tub2_iface": {"TYPES_WITH_TAB": "()"}}
    vol, _ = check(off, tmp_path)
    out = value_with(off, tmp_path, "[(m := __import__('revron.tub2_tab', fromlist=['x'])).HAS_TAB, m.key_tab(), m.key_hole(), m.wall_blend(), m.rabbet(), m.rub_point(), "
                                    "__import__('revron.tub2_front', fromlist=['x']).wire_slot()]")
    assert out == [False, None, None, None, None, None, None], out
    assert vol > 0


# ---- overall size (hooks size.width / size.length / size.height): longer / wider / shorter / taller must just work ------------------------------------
# REVRON_SIZE_* is a delta in mm or a percentage of the stock overall width / length / height. Each case builds in a fresh interpreter: the tub is ONE valid
# solid, the base and top panels are valid, the spec builds, and the gearmotors, pack and ESCs never overlap the tub (outside the heat-set bore sleeves, which
# no part may stand in either). A shrink saturates where the contents touch (CH_HALF_W_MIN / CH_Y1_MIN / CH_Z1_MIN): the same stock chassis, not a broken one.
SIZE = """
import sys
sys.path[:0] = [%r, %r]
from revron import tub2, tub2_bays as B, hw, panel_base, panel_top, spec as S
from revron.params import *
tub = tub2.chassis2()
keep = B._U(*B.KEEP)
print("TUB", len(tub.solids()), tub.is_valid, round(tub.volume, 3), round(tub.bounding_box().min.X + tub.bounding_box().max.X, 4))
for pid, cid, at, rot in (("motor_l", DRIVE_MOTOR, (-MOTX, RY, RZ), (0, 0, 180)), ("motor_r", DRIVE_MOTOR, (MOTX, RY, RZ), (0, 0, 0)),
                          ("battery", BATTERY, ELEC["battery"], (0, 0, 90)), ("rxesc", RXESC, RX_C, (0, 0, 90)), ("wesc", WESC, WE_C, (0, 0, 90))):
    sol = hw.placed(cid, at, rot)
    print("OVL", pid, round(((tub & sol) - keep).volume, 4), round((sol & keep).volume, 4))
for nm, p in (("base_panel", panel_base.base_panel()), ("top_panel", panel_top.top_panel())):
    print("PANEL", nm, len(p.solids()), p.is_valid)
print("SIZE", CH_HALF_W, CH_Y1, CH_Z1, SA[0], SB[0], WY, WZ, SIZE_DW, SIZE_DL, SIZE_DH)
try:
    print("SPEC ok", len(S.make_spec("x")["parts"]))
except Exception as e:
    import traceback
    fr = [f for f in traceback.extract_tb(e.__traceback__) if "revron" in f.filename][-1]
    print("SPEC FAIL", type(e).__name__, fr.filename.split("/")[-1], fr.lineno, fr.name)
"""
STOCK_TUB_VOLUME = DEFAULT_TUB_VOLUME


def size_build(env, tmp_path):
    dst = pathlib.Path(tempfile.mkdtemp(dir=tmp_path)) / "src"
    shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("__pycache__"))
    r = subprocess.run([sys.executable, "-c", SIZE % (str(dst), ROOT)], capture_output=True, text=True, env={**os.environ, **env})
    rows = [ln.split() for ln in r.stdout.splitlines()]
    assert any(x[0] == "SIZE" for x in rows), r.stderr[-1500:]
    tub = next(x for x in rows if x[0] == "TUB")
    return dict(tub=(int(tub[1]), tub[2] == "True", float(tub[3]), float(tub[4])), ovl={x[1]: float(x[2]) for x in rows if x[0] == "OVL"}, slv={x[1]: float(x[3]) for x in rows if x[0] == "OVL"},
                panel={x[1]: (int(x[2]), x[3] == "True") for x in rows if x[0] == "PANEL"}, size=[float(v) for v in next(x for x in rows if x[0] == "SIZE")[1:]], spec=" ".join(next(x for x in rows if x[0] == "SPEC")[1:]))


STEPS = ["-30%", "-20%", "-10%", "10%", "20%", "30%"]
SIZE_ENV = {"width": "REVRON_SIZE_WIDTH", "length": "REVRON_SIZE_LENGTH", "height": "REVRON_SIZE_HEIGHT"}

@pytest.mark.parametrize("axis", ["width", "length", "height"])
@pytest.mark.parametrize("step", STEPS)
def test_overall_size_step_holds(axis, step, tmp_path):
    """Each declared step of each size hook: the tub is one valid symmetric solid, both panels are valid solids and nothing that sits in the tub overlaps it."""
    b = size_build({SIZE_ENV[axis]: step}, tmp_path)
    assert b["tub"][:2] == (1, True) and abs(b["tub"][3]) < 1e-3, b
    assert all(v == 0 for v in b["ovl"].values()) and all(v == 0 for v in b["slv"].values()), b
    assert b["panel"] == {"base_panel": (1, True), "top_panel": (1, True)}, b


@pytest.mark.parametrize("axis", ["width", "length", "height"])
@pytest.mark.parametrize("step", STEPS)
def test_overall_size_step_builds_the_spec(axis, step, tmp_path):
    """The whole spec (all parts) builds at each step."""
    b = size_build({SIZE_ENV[axis]: step}, tmp_path)
    assert b["spec"].startswith("ok"), b["spec"]


def test_growth_steps_move_what_they_should(tmp_path):
    """+30 %: the walls, nose and rim move out by 30 % of the stock overall size and the front axle, nose standoff and weapon axis come with them."""
    w = size_build({"REVRON_SIZE_WIDTH": "30%"}, tmp_path)["size"]
    assert abs(w[0] - 29.5 * 1.3) < 1e-6
    ln = size_build({"REVRON_SIZE_LENGTH": "30%"}, tmp_path)["size"]
    d = 0.3 * (15.0 + 37.6)
    assert abs(ln[1] - (15.0 + d)) < 1e-6 and abs(ln[3] - (30.5 + d)) < 1e-6 and abs(ln[4] - (40.5 + d)) < 1e-6 and abs(ln[5] - (38.5 + d)) < 1e-6
    h = size_build({"REVRON_SIZE_HEIGHT": "30%"}, tmp_path)["size"]
    assert abs(h[2] - (19.5 + 0.3 * 17.0)) < 1e-6 and abs(h[6] - (23.5 + 0.3 * 17.0)) < 1e-6


@pytest.mark.parametrize("axis,step", [("length", "-10%"), ("height", "-30%")])
def test_shrink_past_the_contents_is_the_stock_tub(axis, step, tmp_path):
    """The pack against the stop wall (length) and the gearbox under the deck (height) are already as tight as the STEP: a shrink saturates and gives the stock tub."""
    b = size_build({SIZE_ENV[axis]: step}, tmp_path)
    assert b["tub"][:2] == (1, True), b
    if axis == "height":
        assert abs(b["tub"][2] - STOCK_TUB_VOLUME) < 0.5 and b["size"][2] == 19.5, b
    else:   # the nose stops 0.2 mm short of the stock (CH_Y1_MIN): the pack needs 14.8, the STEP front wall stands at 15.0
        assert abs(b["size"][1] - 14.8) < 1e-6, b


def test_size_in_mm_equals_the_percentage(tmp_path):
    """'5.26' mm and '10%' of the stock length (52.6) are the same setting."""
    a = size_build({"REVRON_SIZE_LENGTH": "5.26"}, tmp_path)
    b = size_build({"REVRON_SIZE_LENGTH": "10%"}, tmp_path)
    assert a["size"] == b["size"] and abs(a["tub"][2] - b["tub"][2]) < 1e-3


def test_default_size_is_the_stock_tub(tmp_path):
    b = size_build({}, tmp_path)
    assert b["tub"][:2] == (1, True) and abs(b["tub"][2] - STOCK_TUB_VOLUME) < 1e-2 and b["size"][:3] == [29.5, 15.0, 19.5], b


# ---- [fix-A-hyp] change-hypothesis sweeps: swaps are settings the tub follows; a screw size is a name, not a dimension ----
HOOKS_JSON = pathlib.Path(SRC).parent / "hooks.json"
SWAP_ENV = {"drive_motor": ("REVRON_DRIVE_MOTOR", "DRIVE_MOTORS", "n10_2200rpm_spicy"), "battery": ("REVRON_BATTERY", "BATTERYS", "lipo_2s_180_turnabot"),
            "drive_esc": ("REVRON_RXESC", "RXESCS", "malenki_nano_rvrn2"), "weapon_esc": ("REVRON_WESC", "WESCS", "bbb_ant_esc_rvrn2"),
            "switch": ("REVRON_SWITCH", "SWITCHES", "switch_bbb_ant_rvrn2")}


def test_swap_settings_list_every_catalog_candidate():
    """The catalog candidates of each role (robot.gen.changes) are exactly the values the tub's setting names, so a catalog entry added later is a visible gap, not a silent break."""
    import json, sys
    sys.path[:0] = [SRC, ROOT]
    from robot.gen import changes as C
    from revron import params_chassis as PC
    hooks = json.loads(HOOKS_JSON.read_text())["hooks"]
    for role, (env, table, default) in SWAP_ENV.items():
        h = next(h for h in hooks.values() if h.get("env") == env)
        assert h["swap"] == role and h["default"] == default, (role, h)
        names = {e.id for e in C.candidates(role, default)}
        assert names | {default} == set(getattr(PC, table)), (role, names ^ set(getattr(PC, table)))


def test_wheel_swap_setting_covers_the_rear_wheels():
    import json, sys
    sys.path[:0] = [SRC, ROOT]
    from robot.gen import changes as C
    from revron import wheel_variant as WV
    h = json.loads(HOOKS_JSON.read_text())["hooks"]["wheel.rear"]
    assert h["swap"] == "wheel" and set(h["parts"]) == {"wheel_rl", "wheel_rr"} and set(h["values"]) == set(WV.REAR_WHEELS)
    assert C.swap_hook({"hooks": {"wheel.rear": h}}, "wheel", ["wheel_rl", "wheel_rr"])[0] == "wheel.rear"
    assert C.swap_hook({"hooks": {"wheel.rear": h}}, "wheel", ["wheel_fl", "wheel_fr"]) is None   # the front wheels are not this setting's


def test_thread_sizes_are_names_not_dimensions():
    """M2 / M3 come from the ISO size names, so a +-10 % sweep of 'literals' cannot ask the nut table for an M3.3: no numeric literal assignment names them."""
    import ast
    src = (pathlib.Path(SRC) / "revron" / "params_chassis.py").read_text()
    node = next(n for n in ast.parse(src).body if isinstance(n, ast.Assign) and ast.unparse(n.targets[0]).strip("()") == "M2, M3")
    assert not any(isinstance(c, ast.Constant) and isinstance(c.value, float) for c in ast.walk(node.value))


@pytest.mark.parametrize("sa_x0", ["15.75", "19.25"])
def test_axle_standoff_start_sweep(sa_x0, tmp_path):
    """SA_X0 +-10 %: the standoff's inner end moves, the M3 thin nut pocket (a named size) is unaffected, the tub stays one valid solid."""
    check({"params_chassis": {"SA_X0": sa_x0}}, tmp_path)


@pytest.mark.parametrize("half_w", ["26.55", "32.45"])
def test_stock_half_width_sweep(half_w, tmp_path):
    """CH_HALF_W_STOCK +-10 %: both side walls move with the nut lobes, pockets and lugs; one valid symmetric solid."""
    check({"params_chassis": {"CH_HALF_W_STOCK": half_w}}, tmp_path)


@pytest.mark.parametrize("env", [{"REVRON_BATTERY": "gnb_3s_300_80c_hv"}, {"REVRON_RXESC": "esc_dual_brushed"}, {"REVRON_WESC": "bbb_red_esc"},
                                 {"REVRON_DRIVE_MOTOR": "n10_300rpm_6v"}, {"REVRON_REAR_WHEEL": "wheel_28x10"}])
def test_swap_setting_builds_one_valid_tub(env, tmp_path):
    b = bays(env, tmp_path)
    assert b["tub"][:2] == (1, True) and all(v == 0 for v in b["ovl"].values()), b


@pytest.mark.parametrize("sw", ["switch_slide_12x4", "switch_slide_bbb_ant", "fingertech_mini_switch"])
def test_switch_swap_gets_its_pad_pilots_and_pocket(sw, tmp_path):
    """Another catalog switch: the ears seat on the pad (their top face on the pad underside), the pilots sit on its catalog mount holes (none: no pilots), the screw is as long as the ears
    and the bite need, and what of its envelope reaches the tub outside the bore sleeves is pocketed from its own catalog solid."""
    b = bays({"REVRON_SWITCH": sw}, tmp_path)
    assert b["tub"][:2] == (1, True) and b["ovl"]["power_switch"] == 0, b


SWITCH_RELATIONS = """
import sys
sys.path[:0] = [%r, %r]
from revron import hw
from revron.params import *
from revron.tub2_params import DECK, SKIN
m = hw.switch_mount(SWITCH)
print("SEAT", round(ELEC["switch_yz"][1] + m["top"] - (DECK - SKIN), 6))
print("HOLES", len(SW_SCREW_Y), len(m["holes"]), round(SW_PITCH - m["pitch"], 6), round(SW_BOLT_Z - (DECK - SKIN) + (m["top"] - m["under"]), 6))
print("SCREW", SW_SCREW if SW_SCREW else "none", 0 if not m["holes"] else round(int(SW_SCREW.split("x")[1]) - (m["top"] - m["under"]) - SW_BITE, 6))
"""


@pytest.mark.parametrize("sw", ["switch_bbb_ant_rvrn2", "switch_slide_12x4", "switch_slide_bbb_ant", "fingertech_mini_switch"])
def test_switch_literals_follow_the_catalog_switch(sw, tmp_path):
    """SW_PITCH / the ears' height / the screw are read off the catalog switch: its ears' top face seats on the pad underside, every catalog mount hole gets a screw, and the screw reaches
    the bite through the ears (within a whole mm); the stock switch keeps M2x3 with the head plane 1.5 under the deck."""
    dst = pathlib.Path(tempfile.mkdtemp(dir=tmp_path)) / "src"
    shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("__pycache__"))
    r = subprocess.run([sys.executable, "-c", SWITCH_RELATIONS % (str(dst), ROOT)], capture_output=True, text=True, env={**os.environ, "REVRON_SWITCH": sw})
    rows = {ln.split()[0]: ln.split()[1:] for ln in r.stdout.splitlines() if ln.split() and ln.split()[0].isupper()}
    assert "SCREW" in rows, r.stderr[-1500:]
    assert float(rows["SEAT"][0]) == 0.0 and rows["HOLES"][0] == rows["HOLES"][1] and float(rows["HOLES"][2]) == 0.0 and float(rows["HOLES"][3]) == 0.0, rows
    assert 0.0 <= float(rows["SCREW"][1]) < 1.0 or rows["SCREW"][0] == "none", rows   # rounded up to a whole mm: less than a mm over the ears + the bite
    if sw == "switch_bbb_ant_rvrn2":
        assert rows["SCREW"][0] == "M2x3", rows


@pytest.mark.parametrize("motor", ["n10_300rpm_6v", "n10_2200rpm_6v", "bbb_n10_600rpm", "n20_1000rpm_6v"])
def test_drive_motor_swap_slides_less_than_the_declared_travel(motor, tmp_path):
    """The inboard stop follows the motor's own inboard end: a gearmotor without the stock's long can (no key gap, end further out) still bears on the tub within MOTOR_SLIDE_MAX,
    which the spec declares as its play (retention.loose_ok)."""
    r = relation_build({"REVRON_DRIVE_MOTOR": motor}, tmp_path)
    assert r["MOTOR_IN"][0] > 0, r


# ---- what leaves / stays in the tub follows each size step (retention, assembly, fastener seat) -----------------------------------------------------------
RELATIONS = """
import sys
sys.path[:0] = [%r, %r]
import build123d as b
from revron import tub2, tub2_bays as B, hw, panel_top
from revron.params import *
from revron.tub2_params import DECK, CENTRE_Y
from revron.tub2_switch import PILOT_DEPTH
tub = tub2.chassis2()
def hit(sol, d, k):
    return round((tub & sol.moved(b.Location(tuple(k * c for c in d)))).volume, 3)
bat = hw.placed(BATTERY, ELEC["battery"], (0, 0, 90))
print("PACK_DOWN", max(hit(bat, (0, 0, -1), k) for k in (0.3, 1, 3, 8, 15, 25)))
ml = hw.placed(DRIVE_MOTOR, (-MOTX, RY, RZ), (0, 0, 180))
print("MOTOR_IN", hit(ml, (1, 0, 0), MOTOR_SLIDE_MAX), hit(ml, (1, 0, 0), 0.4))
print("RX_FRONT", round(RX_C[1] + RX_SIZE[0] / 2 - WALL_IN_FRONT, 6))
print("SWITCH", round(ELEC["switch_yz"][0] - CENTRE_Y, 6), round(SW_BOLT_Z - DECK, 6), round(SW_BOLT_Z - (DECK - PILOT_DEPTH), 6))
from revron.params_weapon import MNT_SIDE
print("SHOULDER", round(panel_top.SHOULDER + panel_top.YC, 6), round(min(m["notch_y"] for m in MNT_SIDE.values()) - TOP_NOTCH_CLR, 6))
"""


def relation_build(env, tmp_path):
    dst = pathlib.Path(tempfile.mkdtemp(dir=tmp_path)) / "src"
    shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("__pycache__"))
    r = subprocess.run([sys.executable, "-c", RELATIONS % (str(dst), ROOT)], capture_output=True, text=True, env={**os.environ, **env})
    rows = {ln.split()[0]: [float(v) for v in ln.split()[1:]] for ln in r.stdout.splitlines() if ln.split() and ln.split()[0].isupper()}
    assert "SHOULDER" in rows, r.stderr[-1500:]
    return rows


@pytest.mark.parametrize("env", [{}, {"REVRON_SIZE_WIDTH": "10%"}, {"REVRON_SIZE_WIDTH": "-10%"}, {"REVRON_SIZE_LENGTH": "10%"}, {"REVRON_SIZE_LENGTH": "-10%"},
                                 {"REVRON_SIZE_HEIGHT": "10%"}, {"REVRON_SIZE_HEIGHT": "30%"}])
def test_size_steps_keep_the_parts_retained_removable_and_seated(env, tmp_path):
    """At each size step: the pack can leave downwards (the tub never closes over it), the gearmotor slides in less than MOTOR_SLIDE_MAX before it bears on the tub
    (the stop follows the motor), the receiver stands against the front wall, the switch sits on the middle of the column rows and its screws keep the same
    bite in the deck pilots, and the top panel's shoulder stays behind the weapon mounts' rear tips."""
    r = relation_build(env, tmp_path)
    assert r["PACK_DOWN"] == [0.0], r
    assert r["MOTOR_IN"][0] > 0 and r["MOTOR_IN"][1] == 0, r
    assert r["RX_FRONT"] == [0.0], r
    assert r["SWITCH"] == [0.0, -1.5, -0.5], r
    assert r["SHOULDER"][0] <= r["SHOULDER"][1] + 1e-6, r
