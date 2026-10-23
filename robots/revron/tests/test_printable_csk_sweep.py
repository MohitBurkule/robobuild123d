"""[fix-B-zero] The mount CSK screws (bolt_u*) in the printable mount variant (REVRON_MOUNT_VARIANT=printable, also with
REVRON_LEAD_GROOVE=on) over the size / standoff sweep: the modelled ISO 10642 head (robot.world.fastener_shape: dk at the
top, the thread d at depth k) seated at the rig's seat (MNT_IN - MNT_CSK_PROUD) must not cut into mount_l / mount_r
(the d6.4 cone over a loose d3.6 bore: flush, the head's foot cut 0.08 into the bore edge), and the head stays within the
flush_head limit (0.2). MNT_CSK_PROUD is derived (params_weapon.csk_seat_proud), so it follows the screw, the fit and the cone."""
import json, os, re, shutil, subprocess, sys

import pytest

SRC = os.path.join(os.path.dirname(__file__), "..", "src")
ROOT = os.path.abspath(os.path.join(SRC, "..", "..", ".."))
CODE = r"""
import json, sys
sys.path.insert(0, %r); sys.path.insert(0, sys.argv[1])
import build123d as bd
try:
    from revron import params as P, mount as M
except Exception as e:
    if type(e).__name__ == "WeaponMotorError":   # MNT_IN -10 percent: the drisk stack no longer fits between the mounts (by design)
        print(json.dumps(dict(skip=str(e)))); sys.exit(0)
    raise
from robot.world import csk_dims
out = dict(proud=P.MNT_CSK_PROUD, cut={})
for side, s in (("r", 1), ("l", -1)):
    mt = M.weapon_mount(side)
    for (y, z), des, key in zip((P.SA, P.SB), P.MNT_SCREW, "ab"):
        d, L = (float(v) for v in des[1:].split("x"))
        dk, k = csk_dims(d)
        prof = bd.Polyline((0, 0), (dk / 2, 0), (d / 2, k), (d / 2, L), (0, L), close=True)
        scr = bd.revolve(bd.make_face(bd.Plane.XZ * prof), bd.Axis.Z)   # head + shank along +z from `at`
        x0 = s * (P.MNT_IN - P.MNT_CSK_PROUD)
        scr = bd.Location((x0, y, z)) * (bd.Rot(0, 90 * s, 0) * scr)
        out["cut"][side + key] = (mt & scr).volume
print(json.dumps(out))
""" % ROOT

SA0, SB0 = (30.5, 5.5), (40.5, 4.5)
CASES = {
    "default": ({}, {}),
    "w-10": ({}, {"REVRON_SIZE_WIDTH": "-10%"}), "w+10": ({}, {"REVRON_SIZE_WIDTH": "10%"}), "w+20": ({}, {"REVRON_SIZE_WIDTH": "20%"}),
    "l+10": ({}, {"REVRON_SIZE_LENGTH": "10%"}), "l+20": ({}, {"REVRON_SIZE_LENGTH": "20%"}),
    "SA1+10": ({"SA": (SA0[0], SA0[1] * 1.1)}, {}), "SA1-10": ({"SA": (SA0[0], SA0[1] * 0.9)}, {}),
    "SB0+10": ({"SB": (SB0[0] * 1.1, SB0[1])}, {}), "SB0-10": ({"SB": (SB0[0] * 0.9, SB0[1])}, {}),
    "MNT_IN+10": ({"MNT_IN": 13.4 * 1.1}, {}), "MNT_IN-10": ({"MNT_IN": 13.4 * 0.9}, {}),
}
VARIANTS = {"printable": {"REVRON_MOUNT_VARIANT": "printable"},
            "printable_groove": {"REVRON_MOUNT_VARIANT": "printable", "REVRON_LEAD_GROOVE": "on"}}
FLUSH_HEAD = 0.2


def _src(over, tmp):
    if not over:
        return SRC
    dst = os.path.join(tmp, "src")
    shutil.copytree(SRC, dst, ignore=shutil.ignore_patterns("__pycache__"))
    f = os.path.join(dst, "revron", "params_chassis.py")
    txt = open(f).read()
    for k, v in over.items():
        if k == "MNT_IN":
            txt, n = re.subn(r"^MNT_IN, MNT_T, MNT_SLAB_T = [\d.]+,", f"MNT_IN, MNT_T, MNT_SLAB_T = {v!r},", txt, count=1, flags=re.M)
        else:
            txt, n = re.subn(rf"^{k} = \([^)]*\)", f"{k} = ({v[0]!r}, {v[1]!r})", txt, count=1, flags=re.M)
        assert n == 1, k
    open(f, "w").write(txt)
    return dst


@pytest.mark.parametrize("variant", list(VARIANTS))
@pytest.mark.parametrize("case", list(CASES))
def test_printable_csk_head_clears_mount(case, variant, tmp_path):
    over, env = CASES[case]
    e = dict(os.environ, **env, **VARIANTS[variant])
    p = subprocess.run([sys.executable, "-c", CODE, _src(over, str(tmp_path))], env=e, capture_output=True, text=True, cwd=ROOT, timeout=900)
    assert p.returncode == 0, p.stderr[-3000:]
    r = json.loads(p.stdout.strip().splitlines()[-1])
    if "skip" in r:
        pytest.skip(r["skip"])
    assert 0.0 <= r["proud"] <= FLUSH_HEAD, r
    for k, v in r["cut"].items():
        assert v < 1e-3, (case, variant, k, v)
