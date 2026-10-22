"""Master sweep: wedgelets, side panels, fork and hubs derive from SA / SB / FK_* / WG_* / RH_*, so they must still build when a master moves
+-10 % (no domain error in the datum maths, no fillet a pocket cannot take) and the derived values must follow the master. Each case runs
in a fresh interpreter on a COPY of the package whose params module gets `NAME = NAME * f` right after the master's own statement, so every
constant derived from it further down (and every `from .params import ...` copy) sees the swept value."""
import ast
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

SRC = Path(__file__).resolve().parents[1] / "src"
REPO = Path(__file__).resolve().parents[3]
SWEEP = 0.1

BODY = """
import sys
sys.path.insert(0, {repo!r})
sys.path.insert(0, {src!r})
import revron.wedgelet as W, revron.side_joint as S, revron.fork as F, revron.hubs as H
{extra}
for s in (-1, 1):
    W.wedgelet(s)
    S.side_panel_local(s)
F.fork_local()
H.rear_hub()
"""


def swept_copy(root, name, idx, f):
    """Copy the revron package into `root` and scale master `name` (element `idx` of a tuple) by f right after its defining statement."""
    dst = Path(root) / "revron"
    shutil.copytree(SRC / "revron", dst, ignore=shutil.ignore_patterns("__pycache__"))
    for mod in sorted(dst.glob("params*.py")):
        lines = mod.read_text().splitlines(keepends=True)
        for node in ast.parse("".join(lines)).body:
            names = [n.id for t in getattr(node, "targets", []) for n in ast.walk(t) if isinstance(n, ast.Name)]
            if name in names:
                expr = (f"tuple(x * {f!r} if i == {idx} else x for i, x in enumerate({name}))" if idx is not None else f"{name} * {f!r}")
                lines.insert(node.end_lineno, f"{name} = {expr}\n")
                mod.write_text("".join(lines))
                return
    raise AssertionError(f"master {name} not found in the params modules")


def run(name, idx, f, extra=""):
    with tempfile.TemporaryDirectory() as root:
        swept_copy(root, name, idx, f)
        code = BODY.format(repo=str(REPO), src=str(root), extra=extra)
        return subprocess.run([sys.executable, "-I", "-c", code], capture_output=True, text=True, timeout=900)


@pytest.mark.parametrize("name,idx", [("SA", 0), ("SA", 1), ("SB", 0), ("SB", 1), ("FK_EYE_D", None), ("WG_SKIN_T", None), ("RH_BORE_X", None)])
@pytest.mark.parametrize("f", [1 - SWEEP, 1 + SWEEP])
def test_wedgelet_and_side_survive_standoff_sweep(name, idx, f):
    r = run(name, idx, f)
    assert r.returncode == 0, r.stderr[-1500:]


def test_seat_face_matches_the_step_table_at_the_defaults():
    sys.path.insert(0, str(SRC))
    from revron.params import SIDE_FACE_X
    from revron.side import face_x
    for k in "abc":
        assert abs(face_x(k) - SIDE_FACE_X[k]) < 0.01, k



def test_nose_seat_follows_a_moved_nose_standoff():
    extra = "import revron.side as X\nprint('FACE', X.face_x('b'), X.bolt_x('b'))"
    base, moved = run("SB", 0, 1.0, extra), run("SB", 0, 1 + SWEEP, extra)
    assert base.returncode == 0 and moved.returncode == 0, (base.stderr + moved.stderr)[-1500:]
    pick = lambda r: float([ln for ln in r.stdout.splitlines() if ln.startswith("FACE")][0].split()[1])   # noqa: E731
    assert abs(pick(moved) - pick(base)) > 0.05          # the seat reads the modelled face where SB now stands (a fixed table would not move)
