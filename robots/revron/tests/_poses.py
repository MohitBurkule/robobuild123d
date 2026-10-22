"""World placement of every spec part's geometry (parent chain of `at`/`rot`, then the model's `origin` shift: a part
drawn in robot coordinates about its frame) and every spin joint in world, for the joint-placement regression test."""
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
    def placed(pid):
        sh = by[pid].get("shape") or {}
        o = sh.get("params", {}).get("origin")
        if o:
            return out[pid] @ xform.translation([-v for v in o])
        base = sh.get("base", sh)   # spec primitive (e.g. the MR85: subtract of placed cylinders): its base placement
        if base.get("type") == "place":
            return out[pid] @ xform.pose(base["at"], base["rot"])
        return out[pid]
    poses = {k: np.round(placed(k), 9).tolist() for k in out}
    poses.update({f["id"]: [list(f["at"]), list(f.get("dir") or [])] for f in spec["fasteners"]})
    joints = {}
    for p in spec["parts"]:
        if p.get("joint"):
            j, M = dict(p["joint"]), out[p["parent"]] if p.get("parent") in by else np.eye(4)
            j["pivot"] = [round(float(v), 6) + 0.0 for v in (M @ np.array([*j["pivot"], 1.0]))[:3]]   # pivot is in the parent frame
            j["axis"] = [round(float(v), 6) + 0.0 for v in M[:3, :3] @ np.array(j["axis"], float)]
            joints[p["id"]] = j
    return poses, joints


if __name__ == "__main__":
    import json
    json.dump(dict(zip(("poses", "joints"), world_poses())), open(sys.argv[1], "w"), indent=0)
