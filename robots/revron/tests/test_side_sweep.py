"""Standoff sweep: wedgelets and side panels derive from SA / SB, so they must still build when a standoff moves +-10 %
(no domain error in the wedgelet datum maths, no fillet the nose pocket cannot take). One fresh interpreter per case: the masters are
module globals read at import time."""
import subprocess
import sys
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[1] / "src"
SWEEP = 0.1

BODY = """
import sys
sys.path.insert(0, {src!r})
import revron.params as P
name, idx, f = {name!r}, {idx}, {f}
v = getattr(P, name); v = list(v) if idx is not None else v
if idx is None: v *= f
else: v[idx] *= f
v = tuple(v) if idx is not None else v
for m in list(sys.modules.values()):
    if m and getattr(m, "__name__", "").startswith("revron") and hasattr(m, name):
        setattr(m, name, v)
import revron.wedgelet as W, revron.side_joint as S, revron.fork as F, revron.hubs as H
for s in (-1, 1):
    W.wedgelet(s)
    S.side_panel_local(s)
F.fork_local()
H.rear_hub()
"""


@pytest.mark.parametrize("name,idx", [("SA", 0), ("SA", 1), ("SB", 0), ("SB", 1), ("FK_EYE_D", None), ("WG_SKIN_T", None), ("RH_BORE_X", None)])
@pytest.mark.parametrize("f", [1 - SWEEP, 1 + SWEEP])
def test_wedgelet_and_side_survive_standoff_sweep(name, idx, f):
    code = BODY.format(src=str(SRC), name=name, idx=idx, f=f)
    r = subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True, timeout=600)
    assert r.returncode == 0, r.stderr[-1500:]


def test_seat_face_matches_the_step_table_at_the_defaults():
    sys.path.insert(0, str(SRC))
    from revron.params import SIDE_FACE_X
    from revron.side import face_x
    for k in "abc":
        assert abs(face_x(k) - SIDE_FACE_X[k]) < 0.01, k

