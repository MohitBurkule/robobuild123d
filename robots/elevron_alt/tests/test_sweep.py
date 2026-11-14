"""Robustness: master sweeps and a weapon-plate swap rebuild valid single solids (fresh interpreter per case)."""
import json
import os
import subprocess
import sys

import pytest

SRC = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "src"))
ROOT = os.path.abspath(os.path.join(SRC, "..", "..", ".."))
CODE = r"""
import sys, json
for p in (%r, %r, %r):
    sys.path.insert(0, p)
from elevron_alt import chassis, side_panel, vert_mod
out = {}
for name, f in (("chassis", chassis.chassis), ("side", side_panel.side_panel_r), ("vert", vert_mod.vert_mod)):
    s = f(); out[name] = dict(n=len(s.solids()), valid=s.is_valid, vol=s.volume)
print(json.dumps(out))
""" % (ROOT, os.path.join(ROOT, "robots", "shared", "src"), SRC)

CASES = {"default": {}, "wall+25%": {"WALL": 2.5}, "len+10%": {"CH_L": 73.26}, "width-5%": {"CH_W": 56.05}, "height+10%": {"CH_H": 18.7}}


@pytest.mark.parametrize("case", sorted(CASES))
def test_master_sweep(case):
    env = dict(os.environ, ELEVRON_MASTERS=json.dumps(CASES[case]))
    p = subprocess.run([sys.executable, "-c", CODE], capture_output=True, text=True, timeout=900, env=env)
    assert p.returncode == 0, p.stderr[-3000:]
    out = json.loads(p.stdout.strip().splitlines()[-1])
    for name, r in out.items():
        assert r["valid"] and r["n"] == 1, (case, name, r)
