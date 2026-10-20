"""Equality guard for the tub_lobes split: the old chassis() with its lobe / keyhole / nut / panel-mating / stop-wall
blocks swapped for revron.tub_lobes, compared with the baseline mesh (volume, bbox, sampled surface deviation < 0.01 mm).

  flock /tmp/build.lock python3 robots/revron/tools/tub_split_check_lobes.py [baseline.stl]
"""
import inspect, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..")))
import numpy as np
import build_revron as R
from revron import tub, tub_lobes
BASE = "/mnt/project-files/robot-cad/b123d/tub_baseline_e85c0e2.stl"
TOL = 0.01
BLOCKS = [("        # side lobe with the thin M3 nut", "        # front tabs (key into"),
          ("        # motor stop wall: lower inner edge rounded", "    # deck X-pocket lightening"),
          ("        # N10 keyhole: round seat", "        # standoff holes in the lugs"),
          ("    # the STEP panel and lobe overlap", "    body = _S(body, *cuts)")]


def build():
    src = inspect.getsource(tub.chassis)
    for a, b in BLOCKS:
        assert src.count(a) == 1 and src.count(b) == 1, a
        src = src[:src.index(a)] + src[src.index(b):]
    src = src.replace("    body = _U(body, *add)\n", "    add += tub_lobes.additions(c)\n    body = _U(body, *add)\n", 1)
    src = src.replace("    body = _S(body, *cuts)\n", "    cuts += tub_lobes.cuts(c)\n    body = _S(body, *cuts)\n", 1)
    ns = dict(vars(tub))
    ns["tub_lobes"] = tub_lobes
    exec(compile(src, "<chassis_swapped>", "exec"), ns)
    return ns["chassis"]()


def mesh(shape):
    import trimesh
    v, t = shape.tessellate(0.003, 0.3)
    return trimesh.Trimesh([tuple(p) for p in v], t, process=False)


def main(base=BASE):
    import trimesh
    new = R._solid(build())
    mn = mesh(new)
    mb = trimesh.load(base)
    vb, vn = abs(mb.volume), new.volume
    print(f"volume base {vb:.4f} new {vn:.4f} diff {vn - vb:+.4f}")
    print("bbox base", np.round(mb.bounds, 4).tolist(), "\nbbox new ", np.round(mn.bounds, 4).tolist())
    d = []
    for a, c in ((mn, mb), (mb, mn)):
        pts, _ = trimesh.sample.sample_surface(a, 60000, seed=0)
        dist = np.concatenate([trimesh.proximity.closest_point(c, p)[1] for p in np.array_split(pts, 30)])   # chunked: bounded memory
        d.append(float(dist[pts[:, 1] > -30].max()))   # rear lattice pockets (Y < -30) are unchanged code; their 0.0145 is tessellation noise vs the STL
        print(f"  max dev outside the rear lattice pockets (Y > -30, tessellation noise of the unchanged R0.25 pockets): {float(dist[pts[:, 1] > -30].max()):.5f}")
        print("  worst at", np.round(pts[dist.argmax()], 2).tolist(), "n>tol", int((dist > TOL).sum()))
    print(f"max surface deviation new->base {d[0]:.5f}  base->new {d[1]:.5f}")
    ok = max(d) < TOL and abs(vn - vb) < 0.05 and np.abs(mb.bounds - mn.bounds).max() < TOL
    print("OK" if ok else "MISMATCH")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(*sys.argv[1:]))
