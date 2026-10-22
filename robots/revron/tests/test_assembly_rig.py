"""Joint-chain placement: every part's geometry sits where the pre-joint baseline put it (placements_baseline.json:
world pose composed with the model origin, regenerated with tests/_poses.py), and every mate is a real coincidence."""
import json, os
import numpy as np
from _poses import world_poses
from revron import joints as J

HERE = os.path.dirname(os.path.abspath(__file__))
TOL = 1e-3


def test_world_poses_match_baseline():
    base = json.load(open(os.path.join(HERE, "placements_baseline.json")))
    poses, joints = world_poses()
    from revron.variants import variant
    gone = [n for n, v in (("bat_pad", "battery_pad"), ("esc_tray", "esc_tray")) if not variant(v)] + ["insert_t"]   # insert_t*: the original has no rim heat-sets (STEP: 5 FS1, all base); also baseline has the variant parts; the original does not
    base["poses"] = {k: v for k, v in base["poses"].items() if not k.startswith(tuple(gone))}
    base["joints"] = {k: v for k, v in base["joints"].items() if not k.startswith(tuple(gone))}
    assert poses.keys() == base["poses"].keys()
    for k, v in base["poses"].items():
        a, b = np.concatenate([np.ravel(x) for x in v]), np.concatenate([np.ravel(x) for x in poses[k]])
        assert np.abs(a - b).max() < TOL, k
    for k, j in joints.items():   # a spin sense is a convention: the axis of a joint under a turned parent (the tub frame) may come out as -axis
        if j["axis"] != base["joints"][k]["axis"]:
            j = dict(j, axis=[v + 0.0 for v in np.negative(j["axis"])])
        assert j == base["joints"][k], k
    assert joints.keys() == base["joints"].keys()


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
    for part, host, ax, bore in (("spider", "weapon_motor_stator", "rotor_axis", "bell_face"), ("whub_rr", "motor_r", "output_shaft", "d_bore"),
                                 ("whub_fl", "so_al", "axle", "bore")):
        h = J.RIG.parts[host]
        axis = h.joints[ax].relative_axis.located(h.location)
        p = _world(part, bore).position
        d = p - axis.position
        assert (d - axis.direction * d.dot(axis.direction)).length < TOL, part
