"""[fix-T] Geometry-equality guard for param refactors of build_revron.py.

  python robots/revron/tools/geom_equal.py snap DIR     # export the touched parts / helper outputs
  python robots/revron/tools/geom_equal.py check DIR    # rebuild, compare against DIR (exit 1 on mismatch)

Solids: volume, bounding box, and surface deviation (points sampled on every face of each version, distance to the
other version's tessellation at 3 um; max < 0.01 mm). 2-D helpers: shapely symmetric-difference area and point-list max deviation.
"""
import os, pickle, sys
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..")))
import build123d as b
import build_revron as R

WEAPON = {"mount_l": lambda: R.weapon_mount("l"), "mount_r": lambda: R.weapon_mount("r"), "spider": lambda: R.spider(),
          "drisk_spacer": lambda: R.drisk_spacer(), "disc_a": lambda: R.disc("disc_a"), "disc_b": lambda: R.disc("disc_b"),
          "motor_back_spacer": lambda: R.motor_back_spacer()}   # [fix-B] weapon parts
SOLIDS = list(R.PARTS)   # [fix-S] every part ([fix-C-j1] parts new since the snap are reported, not compared)


def _build(n):
    return R._solid(R.PARTS[n]())
TOL = 0.01


def helpers():
    out = {}
    pts = [(0.0, 0.0), (3.0, 1.0), (5.0, 4.0), (9.0, 4.5)]
    out["disc_outline"] = R.disc_outline()
    out["floating_disc"] = R.floating_disc()
    out["mount_profile_r10"] = R._mount_profile("r")
    out["mount_profile_r7"] = R._mount_profile("l")
    out["chaikin"] = {n: R._chaikin_open(pts, n) for n in (0, 1, 3)}
    return out


def _mesh(shape):
    import trimesh
    v, t = shape.tessellate(0.003, 0.3)
    return trimesh.Trimesh([tuple(p) for p in v], t, process=False)


def _dev(a, c, n=20000):
    """Max distance from n points sampled on a's surface to c's surface (tessellated at 3 um chordal tolerance)."""
    import trimesh
    ma, mc = _mesh(a), _mesh(c)
    pts, _ = trimesh.sample.sample_surface(ma, n, seed=0)
    _, d, _ = trimesh.proximity.closest_point(mc, pts)
    return float(d.max())


def snap(d):
    os.makedirs(d, exist_ok=True)
    for n in SOLIDS:
        b.export_brep(_build(n), os.path.join(d, n + ".brep"))
    pickle.dump(helpers(), open(os.path.join(d, "helpers.pkl"), "wb"))
    print("snap", d)


def check(d):
    bad = 0
    for n in SOLIDS:
        f = os.path.join(d, n + ".brep")
        if not os.path.exists(f):
            print(f"{n:12s} new (not in snap)", flush=True); continue
        new = _build(n); tmp = f + ".new"; b.export_brep(new, tmp)
        same = open(f, "rb").read() == open(tmp, "rb").read(); os.remove(tmp)
        if same:   # byte-identical B-rep: geometry equal, skip the costly surface sampling
            print(f"{n:12s} identical B-rep  OK", flush=True); continue
        old = b.import_brep(f)
        bo, bn = old.bounding_box(), new.bounding_box()
        dv = abs(old.volume - new.volume)
        db = max(abs(x - y) for x, y in zip((*bo.min, *bo.max), (*bn.min, *bn.max)))
        ds = max(_dev(new, old), _dev(old, new))
        ok = dv < 1e-3 and db < 1e-6 and ds < TOL
        bad += not ok
        print(f"{n:12s} vol {new.volume:10.4f} dV {dv:.2e}  dBB {db:.2e}  maxdev {ds:.2e}  {'OK' if ok else 'FAIL'}", flush=True)
    old, new = pickle.load(open(os.path.join(d, "helpers.pkl"), "rb")), helpers()
    for k in old:
        if k == "chaikin":
            dm = max(max(abs(a - c) for p, q in zip(old[k][m], new[k][m]) for a, c in zip(p, q)) for m in old[k])
            ok = all(len(old[k][m]) == len(new[k][m]) for m in old[k]) and dm < 1e-9
        else:
            dm = (old[k].symmetric_difference(new[k]).area if hasattr(old[k], "symmetric_difference")   # shapely
                  else sum(f.area for f in ((old[k] - new[k]).faces() + (new[k] - old[k]).faces())))   # build123d Face
            ok = dm < 1e-9
        bad += not ok
        print(f"{k:20s} dev {dm:.2e}  {'OK' if ok else 'FAIL'}")
    sys.exit(1 if bad else 0)


if __name__ == "__main__":
    {"snap": snap, "check": check}[sys.argv[1]](sys.argv[2])
