"""World pose of every spec part (parent chain of `at`/`rot`) for the joint-placement regression test."""
import os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "src"), os.path.join(ROOT, "..", "..")]
import numpy as np
import revron  # noqa: F401
from revron.spec import make_spec
from robot import xform


def world_poses():
    spec = make_spec("m.py")
    by = {p["id"]: p for p in spec["parts"]}
    out = {}

    def W(pid):
        if pid not in out:
            p = by[pid]
            par = p.get("parent")
            out[pid] = (W(par) if par in by else np.eye(4)) @ xform.pose(p.get("at") or [0, 0, 0], p.get("rot") or [0, 0, 0])
        return out[pid]
    for pid in by:
        W(pid)
    poses = {k: v.tolist() for k, v in out.items()}
    poses.update({f["id"]: [list(f["at"]), list(f.get("dir") or [])] for f in spec["fasteners"]})
    joints = {p["id"]: p["joint"] for p in spec["parts"] if p.get("joint")}
    return poses, joints


if __name__ == "__main__":
    import json
    json.dump(dict(zip(("poses", "joints"), world_poses())), open(sys.argv[1], "w"), indent=0)
