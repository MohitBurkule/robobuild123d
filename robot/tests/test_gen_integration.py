"""End-to-end: generated robots pass `robot verify` with zero blockers (fast tessellation, cached).

Each case builds the preset hypothesis through the gate (which itself refuses to return a spec with a blocker) and
re-verifies the result. Slow on a cold cache (about a minute per robot); set RB_GEN_SKIP_SLOW=1 to skip.
"""

import os

import pytest

from robot.gen import gate
from robot.gen import hypothesis as H

pytestmark = pytest.mark.skipif(os.environ.get("RB_GEN_SKIP_SLOW") == "1", reason="slow end-to-end verify")

CASES = {
    "wedge": "wedge_2wd-like",
    "hspin_bar": "horizontal bar spinner",
    "vspin_drisk": "vertical drisk (Revron-like layout, generic sizes)",
    "lifter": "servo lifter",
}

# A servo lifter's limited-range arm is swept a full turn by the kinematics checks (VERIFIER_ISSUES.md #1).

@pytest.mark.parametrize("w", sorted(CASES))
def test_generated_robot_has_no_blockers(w):
    res = gate.gate(H.preset(w), fast=True, max_layouts=2, seeds=(0,))
    assert gate.blockers(res.report) == []
    rep = gate.verify_dict(res.spec, fast=True)
    assert gate.blockers(rep) == [], gate.blockers(rep)[:5]
    assert rep.metrics.get("mass_total_g", 0) <= 150.0
