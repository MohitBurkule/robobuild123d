"""[fix-B-robust] Robustness sweep of the weapon mounts against the standoff positions (robust report: SA[1] +-10 %,
SB[0] +-10 %) and the GR1507 STEP motor variant. Each case patches the chassis masters SA / SB in a fresh interpreter,
reloads the param, mount and rig modules and checks the relations that must follow the standoffs:

- RV02 / RV03 each build as one valid solid; the STEP rotor (weapon_motor_can) is one valid solid;
- the mount CSK cones sit on the standoff axes, closed all round in the mount (no break-out), the screw head seated on
  the cone stands MNT_CSK_PROUD <= 0.2 mm (flush_head) out of the inner face, and the rig's screw seat is on the cone;
- the screws are seated: their shank runs on into the standoff they thread into;
- the rotor does not trap them: the head is outside the discs' rim envelope at every rotor angle, so a screw backed
  out of the mount passes the discs;
- the boss line rides on SB: tangent to the nose arc round it (STEP 0.4 um; within 0.2 mm over the sweep).
"""
import json, os, re, shutil, subprocess, sys

import pytest

SRC = os.path.join(os.path.dirname(__file__), "..", "src")
ROOT = os.path.abspath(os.path.join(SRC, "..", "..", ".."))
CODE = r"""
import json, math, sys
sys.path.insert(0, %r); sys.path.insert(0, sys.argv[1])
from revron import params as P, mount as M
import build123d as bd
from robot import catalog
from robot.shapes import to_solid
from robot.cad import fastener_catalog as fc
out = {}
for side, s in (("r", 1), ("l", -1)):
    mt = M.weapon_mount(side)
    r = dict(n=len(mt.solids()), valid=mt.is_valid, csk=[])
    for (y, z), des in zip((P.SA, P.SB), P.MNT_SCREW):
        rec = M._mount_csk(s, y, z, des)[1]
        h = rec.hole
        r0 = h["csk_d"] / 2
        xin = s * P.MNT_IN                                   # inner face
        on_axis = abs(rec.at[1] - y) < 1e-9 and abs(rec.at[2] - z) < 1e-9 and abs(rec.at[0] - xin) < 1e-9
        ring = [(xin + s * 0.3 * h["csk_depth"], y + (r0 + 0.05) * math.cos(a), z + (r0 + 0.05) * math.sin(a)) for a in [k * math.pi / 8 for k in range(16)]]
        closed = all(mt.is_inside(bd.Vector(*p)) for p in ring)   # material all round the cone: no break-out of the seat
        opened = not mt.is_inside(bd.Vector(xin + s * 0.5 * h["csk_depth"], y, z))
        r["csk"].append(dict(on_axis=on_axis, closed=closed, open=opened, proud=P.MNT_CSK_PROUD, d=h["d"], len=h["length"], dk=h["head_dk"]))
    out[side] = r
# rig screw seats on the cone axes
from revron.joints import seat
out["seats"] = {f: seat(f) for f in ("bolt_ula", "bolt_ulb", "bolt_ura", "bolt_urb")}
can = to_solid(catalog.find(P.MOTOR["can"]).shape)
out["can"] = dict(n=len(can.solids()), valid=can.is_valid)
out["P"] = dict(SA=P.SA, SB=P.SB, WY=P.WY, WZ=P.WZ, MNT_IN=P.MNT_IN, MNT_SLAB_T=P.MNT_SLAB_T, MNT_CSK_PROUD=P.MNT_CSK_PROUD,
                SA_X=P.SA_X, SB_X=P.SB_X, DISC_R=P.DISC_R, DISC_ECC=P.DISC_ECC, DR_X=P.DR_X, NOSE_R=P.NOSE_R,
                boss=[P.boss_line_z(P.BOSS_NOSE_Y), P.BOSS_Z, P.BOSS_NOSE_Y], TAB_Y0=P.TAB["y0"], TOP_Z=P.MNT_TOP_Z)
print(json.dumps(out, default=list))
""" % ROOT

SA0, SB0 = (30.5, 5.5), (40.5, 4.5)   # the defaults the report perturbed (asserted against params below)
CASES = {
    "default": ({}, {}),
    "SA1+10": ({"SA": (SA0[0], SA0[1] * 1.1)}, {}),
    "SA1-10": ({"SA": (SA0[0], SA0[1] * 0.9)}, {}),
    "SB0+10": ({"SB": (SB0[0] * 1.1, SB0[1])}, {}),
    "SB0-10": ({"SB": (SB0[0] * 0.9, SB0[1])}, {}),
    "motor_step": ({}, {"REVRON_MOTOR_VARIANT": "step"}),
}
FLUSH_HEAD = 0.2   # spec flush_head limit (mm)


def _src(over, tmp):
    """The sources with the standoff masters edited in params_chassis.py (every relation downstream re-derives)."""
    if not over:
        return SRC
    dst = os.path.join(tmp, "src")
    shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("__pycache__"))
    f = os.path.join(dst, "revron", "params_chassis.py")
    txt = open(f).read()
    for k, v in over.items():
        txt, n = re.subn(rf"^{k} = \([^)]*\)", f"{k} = ({v[0]!r}, {v[1]!r})", txt, count=1, flags=re.M)
        assert n == 1, k
    open(f, "w").write(txt)
    return dst


def _run(over, env, tmp):
    e = dict(os.environ, **env)
    p = subprocess.run([sys.executable, "-c", CODE, _src(over, tmp)], env=e, capture_output=True, text=True, cwd=ROOT)
    assert p.returncode == 0, p.stderr[-3000:]
    return json.loads(p.stdout.strip().splitlines()[-1])


@pytest.mark.parametrize("case", list(CASES))
def test_mount_follows_standoffs(case, tmp_path):
    r = _run(*CASES[case], str(tmp_path))
    P = r["P"]
    if case == "default":
        assert tuple(P["SA"]) == SA0 and tuple(P["SB"]) == SB0
    for k, v in CASES[case][0].items():
        assert tuple(P[k]) == tuple(v), (case, k)        # the edit reached the build
    assert r["can"]["n"] == 1 and r["can"]["valid"], (case, "weapon_motor_can")
    axis = (P["WY"], P["WZ"])
    for side, s in (("r", 1), ("l", -1)):
        m = r[side]
        assert m["n"] == 1 and m["valid"], (case, side)
        for (y, z), c, so_x, key in zip((P["SA"], P["SB"]), m["csk"], (P["SA_X"], P["SB_X"]), ("a", "b")):
            assert c["on_axis"] and c["open"] and c["closed"], (case, side, key, c)
            assert 0.0 <= c["proud"] <= FLUSH_HEAD, (case, side, key)
            st = r["seats"][f"bolt_u{side}{key}"]
            at = st["at"] if isinstance(st, dict) else st[0]
            assert abs(at[1] - y) < 1e-6 and abs(at[2] - z) < 1e-6, (case, side, key, at)   # rig seat on the cone axis
            assert abs(abs(at[0]) - (P["MNT_IN"] - P["MNT_CSK_PROUD"])) < 1e-6, (case, side, key, at)
            tip = P["MNT_IN"] - P["MNT_CSK_PROUD"] + c["len"]
            assert so_x[0] < tip <= so_x[1], (case, side, key)                               # shank threads into the standoff
            # rotor never traps it: the head is outside the discs' rim envelope at any rotor angle ...
            assert ((y - axis[0]) ** 2 + (z - axis[1]) ** 2) ** 0.5 - c["dk"] / 2 > P["DISC_R"] - P["DISC_ECC"], (case, side, key)
    # boss line: from the notch top to the nose point riding on SB
    (yb, zb), (y0, z0) = (P["boss"][2], P["boss"][1]), (P["TAB_Y0"], P["TOP_Z"])
    assert abs(P["boss"][0] - zb) < 1e-9
    nx, nz = -(zb - z0), (yb - y0)
    n = (nx * nx + nz * nz) ** 0.5
    d = abs((P["SB"][0] - y0) * nx + (P["SB"][1] - z0) * nz) / n
    assert abs(d - P["NOSE_R"]) < (1e-3 if case == "default" else 0.2), (case, d)   # tangent to the STEP's 0.4 um; it rides on SB
