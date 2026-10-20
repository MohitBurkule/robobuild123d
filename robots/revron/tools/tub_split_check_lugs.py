"""[fix-A] Equality guard for the W3 tub split: old chassis() with the lug / front / lattice blocks swapped for
revron.tub_lugs + revron.tub_front, compared with the baseline STL (volume, bbox, surface deviation < 0.01 mm).

  flock /tmp/build.lock python3 robots/revron/tools/tub_split_check_lugs.py [BASELINE.stl]
"""
import inspect, os, sys, types
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..")))
BASE = "/mnt/project-files/robot-cad/b123d/tub_baseline_e85c0e2.stl"
TOL = 0.01

# (first line marker, last line marker, lines above to include): the old blocks the new modules replace
BLOCKS = [("# front tabs (key into the weapon-mount notches)", "add.append(_ext(Polygon([(sg * u, v) for u, v in fil.exterior.coords])", 0),
          ("# lugs carrying the standoffs", "add.append(_ext(lug, \"yz\", sg * 17.5, sg * 21.5))", 0),
          ("# front corner flanges (STEP)", "(sg * x_, y_) for x_, y_ in Polygon([(21.4, 13.0), (29.5, 13.0)] + blend", 1),
          ("# lug underside: flat to Y 26", "front wall stops at the rabbet under the tab", 0),
          ("# standoff holes in the lugs, square key hole", "Polygon([(20.0, 6.9), (25.0, 6.9)", 0),
          ("# rear wall: 1 mm deep triangle lattice", "cuts.append(_lattice_pocket(", 0),
          ("# weapon phase wire hole", "cuts.append(_wall_pocket(xa, xb, 6.55", 0)]


def swapped_chassis():
    import revron.tub as T
    from revron import tub_lugs, tub_front
    lines = inspect.getsource(T).split("\n")
    for start, end, up in BLOCKS:
        i = next(k for k, l in enumerate(lines) if start in l) - up
        j = next(k for k in range(i, len(lines)) if end in lines[k])
        lines[i:j + 1] = []
    src = "\n".join(lines)
    for old, new in (("    body = _U(body, *add)\n", "    add += tub_lugs.additions(c) + tub_front.additions(c)\n    body = _U(body, *add)\n"),
                     ("    body = _S(body, *cuts)\n    # electronics", "    cuts += tub_lugs.cuts(c) + tub_front.cuts(c)\n    body = _S(body, *cuts)\n    # electronics")):
        assert src.count(old) == 1, old
        src = src.replace(old, new)
    mod = types.ModuleType("revron.tub_swapped")
    mod.__package__ = "revron"
    import revron
    mod.__dict__.update(revron.NAMESPACE)   # the package's shared namespace (weapon_mount, side_panel, ...)
    mod.tub_lugs, mod.tub_front = tub_lugs, tub_front
    exec(compile(src, "tub_swapped", "exec"), mod.__dict__)
    return mod.chassis()


def compare(shape, base_stl, n=40000):
    import numpy as np, trimesh
    from scipy.spatial import cKDTree
    v, t = shape.tessellate(0.003, 0.3)
    new = trimesh.Trimesh([tuple(p) for p in v], t, process=False)
    old = trimesh.load(base_stl)
    r = {"vol_new": float(shape.volume), "vol_base": float(old.volume), "bbox_new": new.bounds.round(4).tolist(), "bbox_base": old.bounds.round(4).tolist()}
    def dev(a, b):
        p, _ = trimesh.sample.sample_surface(a, n, seed=0)
        return float(trimesh.proximity.closest_point(b, p)[1].max())
    r["dev_new_to_base"], r["dev_base_to_new"] = dev(new, old), dev(old, new)
    r["ok"] = max(r["dev_new_to_base"], r["dev_base_to_new"]) < TOL and abs(r["vol_new"] - r["vol_base"]) < 0.05   # note: the baseline STL tessellation itself deviates ~0.0153 from the B-rep (run with --old as control)
    return r


if __name__ == "__main__":
    if "--old" in sys.argv:   # control: the unmodified chassis() through the same comparison (mesh tessellation noise floor)
        sys.argv.remove("--old")
        import revron.tub as T
        import revron
        s = T.chassis()
    else:
        s = swapped_chassis()
    if "--direct" in sys.argv:   # exact B-rep check against the unmodified chassis(): volume of the symmetric difference
        sys.argv.remove("--direct")
        import revron.tub as T
        o = T.chassis()
        print({"xor_volume": float(s.cut(o).volume + o.cut(s).volume), "vol_new": float(s.volume), "vol_old": float(o.volume)})
    res = compare(s, sys.argv[1] if len(sys.argv) > 1 else BASE)
    print(res)
    sys.exit(0 if res["ok"] else 1)
