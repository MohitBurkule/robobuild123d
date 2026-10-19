"""[fix-T] Geometry-equality guard for param refactors of build_revron.py.

  python robots/revron/tools/geom_equal.py snap DIR     # export the touched parts / helper outputs
  python robots/revron/tools/geom_equal.py check DIR    # rebuild, compare against DIR (exit 1 on mismatch)

Solids: volume, bounding box, and surface deviation (points sampled on every face of each version, distance to the
other version's tessellation at 2 um; max < 0.01 mm). 2-D helpers: shapely symmetric-difference area and point-list max deviation.
"""
import os, pickle, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..")))
import build123d as b
import build_revron as R

SOLIDS = ["top_panel", "base_panel", "esc_tray"]
TOL = 0.01


def helpers():
    out = {f"panel_outline_{g}": R._panel_outline(g) for g in (0.0, 0.05)}
    pts = [(0.0, 0.0), (3.0, 1.0), (5.0, 4.0), (9.0, 4.5)]
    out["chaikin"] = {n: R._chaikin_open(pts, n) for n in (0, 1, 3)}
    return out


def _mesh(shape):
    import trimesh
    v, t = shape.tessellate(0.002, 0.1)
    return trimesh.Trimesh([tuple(p) for p in v], t, process=False)


def _dev(a, c, n=20000):
    """Max distance from n points sampled on a's surface to c's surface (tessellated at 2 um chordal tolerance)."""
    import trimesh
    ma, mc = _mesh(a), _mesh(c)
    pts, _ = trimesh.sample.sample_surface(ma, n, seed=0)
    _, d, _ = trimesh.proximity.closest_point(mc, pts)
    return float(d.max())


def snap(d):
    os.makedirs(d, exist_ok=True)
    for n in SOLIDS:
        b.export_brep(getattr(R, n)(), os.path.join(d, n + ".brep"))
    pickle.dump(helpers(), open(os.path.join(d, "helpers.pkl"), "wb"))
    print("snap", d)


def check(d):
    bad = 0
    for n in SOLIDS:
        old, new = b.import_brep(os.path.join(d, n + ".brep")), getattr(R, n)()
        bo, bn = old.bounding_box(), new.bounding_box()
        dv = abs(old.volume - new.volume)
        db = max(abs(x - y) for x, y in zip((*bo.min, *bo.max), (*bn.min, *bn.max)))
        ds = max(_dev(new, old), _dev(old, new))
        ok = dv < 1e-3 and db < 1e-6 and ds < TOL
        bad += not ok
        print(f"{n:12s} vol {new.volume:10.4f} dV {dv:.2e}  dBB {db:.2e}  maxdev {ds:.2e}  {'OK' if ok else 'FAIL'}")
    old, new = pickle.load(open(os.path.join(d, "helpers.pkl"), "rb")), helpers()
    for k in old:
        if k == "chaikin":
            dm = max(max(abs(a - c) for p, q in zip(old[k][m], new[k][m]) for a, c in zip(p, q)) for m in old[k])
            ok = all(len(old[k][m]) == len(new[k][m]) for m in old[k]) and dm < 1e-9
        else:
            dm = old[k].symmetric_difference(new[k]).area
            ok = dm < 1e-9
        bad += not ok
        print(f"{k:20s} dev {dm:.2e}  {'OK' if ok else 'FAIL'}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    {"snap": snap, "check": check}[sys.argv[1]](sys.argv[2])
