"""Joint-chain placement: every part's world pose equals the pre-joint baseline, and every mate is a real coincidence."""
import json, os
import numpy as np
from _poses import world_poses
from revron import joints as J

HERE = os.path.dirname(os.path.abspath(__file__))
TOL = 1e-3


def test_world_poses_match_baseline():
    base = json.load(open(os.path.join(HERE, "placements_baseline.json")))
    poses, joints = world_poses()
    assert poses.keys() == base["poses"].keys()
    for k, v in base["poses"].items():
        a, b = np.concatenate([np.ravel(x) for x in v]), np.concatenate([np.ravel(x) for x in poses[k]])
        assert np.abs(a - b).max() < TOL, k
    assert joints == base["joints"]


def _world(part, label):
    h = J.RIG.parts[part]
    return h.location * h.joints[label].relative_location


def test_every_mate_coincides():
    """Parent and child joint frames coincide after solving: same origin and same axes."""
    assert len(J.RIG._mates) >= 50
    for parent, pl, child, cl in J.RIG._mates:
        a, b = _world(parent, pl), _world(child, cl)
        assert (a.position - b.position).length < TOL, (parent, pl, child, cl)
        ma, mb = (np.array([[t.Value(i, j) for j in (1, 2, 3)] for i in (1, 2, 3)]) for t in
                  (a.wrapped.Transformation(), b.wrapped.Transformation()))
        assert np.abs(ma - mb).max() < TOL, (parent, pl, child, cl)


def test_spin_axes_pass_through_their_hubs():
    """Each revolute axis runs through the bore of the part that spins on it."""
    for part, host, ax, bore in (("spider", "mount_r", "weapon_axis", "bore"), ("whub_rr", "motor_r", "output_shaft", "d_bore"),
                                 ("whub_fl", "so_al", "axle", "bore")):
        h = J.RIG.parts[host]
        axis = h.joints[ax].relative_axis.located(h.location)
        p = _world(part, bore).position
        d = p - axis.position
        assert (d - axis.direction * d.dot(axis.direction)).length < TOL, part
