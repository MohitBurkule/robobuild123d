"""Whole-robot deviation heat map (top, side, front) of a spec against its reference_cad STEP parts.

usage: python3 -m robot.tools.whole_diff SPEC OUT.png
"""
import sys

import trimesh

from robot import spec as S, world as W
from robot.checks import ref_diff as D, reference_cad as R


def main(spec_path, out):
    sp = S.load(spec_path)
    w = W.World.start(W.resolve(sp))
    cfg = R._cfg(sp)
    from pathlib import Path

    rdir = Path(cfg["dir"])
    mods, refs = [], []
    for e in cfg["parts"]:
        mods.append(w.body(e["part"]).mesh)
        refs.append(D.clean(R.ref_in_world(trimesh.load(rdir / e["file"], force="mesh"), e, cfg)))
    dev = D.surface_deviation(trimesh.util.concatenate(mods), trimesh.util.concatenate(refs), 40000)
    D.render_deviation(dev, out, "whole robot")
    print(f"wrote {out}: model->ref {dev['model_to_ref']} ref->model {dev['ref_to_model']}")


if __name__ == "__main__":
    main(*sys.argv[1:3])
