"""[W1] Equality guard for the split tub shell: old chassis() with the shell blocks swapped for tub_shell, vs the baseline mesh.

  flock /tmp/build.lock python3 robots/revron/tools/tub_split_check.py [--old] [--lint]

Builds shell -> union (old other-feature additions + tub_shell.additions) -> subtract (old other-feature cuts + tub_shell.cuts)
-> union tub_shell.ribs, from the HEAD (e85c0e2) source of tub.chassis with the shell blocks cut out by line range.
--old builds the unmodified chassis() instead. Compares volume, bbox and surface deviation (both ways) to BASELINE.
"""
import inspect, os, sys, time
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, "..", "src"))
sys.path.insert(0, os.path.abspath(os.path.join(HERE, "..", "..", "..")))
BASELINE = "/mnt/project-files/robot-cad/b123d/tub_baseline_e85c0e2.stl"
TOL = 0.01
# (first line number, last line number, expected start of the first line, replacement) of tub.chassis() at e85c0e2
CUT = [(131, 141, "plan = _round", "    body = SHELL(c)\n"),
       (143, 149, "# insert columns", ""),
       (151, 170, "def mx(poly)", ""),
       (209, 209, "cuts = []", "    cuts = list(NEW_CUTS(c))\n"),
       (218, 220, "# motor stop wall: lower", ""),
       (221, 251, "# deck X-pocket", ""),
       (283, 290, "pan = _panel_outline", ""),
       (299, 306, "# electronics cage", "    return _U(body, *RIBS(c))\n")]


def old_source():
    import revron.tub as T
    src, first = inspect.getsourcelines(T.chassis)
    assert first == 123, "tub.chassis moved: this guard targets e85c0e2"
    return T, src, first


def swapped_chassis():
    T, src, first = old_source()
    out, i = [], 0
    cuts = {a - first: (b - first, exp, rep) for a, b, exp, rep in CUT}
    while i < len(src):
        if i in cuts:
            j, exp, rep = cuts[i]
            assert src[i].strip().startswith(exp), (i + first, src[i])
            out.append(rep)
            i = j + 1
            continue
        out.append(src[i])
        i += 1
        if out[-1].strip() == "add = []":
            out.append("    add += NEW_ADD(c)\n")
    ns = dict(vars(T))
    from revron import tub_shell as S
    ns.update(SHELL=S.shell, NEW_ADD=S.additions, NEW_CUTS=S.cuts, RIBS=S.ribs)
    exec(compile("".join(out), "<chassis-swapped>", "exec"), ns)
    return ns["chassis"]


def lint():
    from robot.checks.param_lint import lint_source
    for f in ("tub_util", "tub_shell", "tub_shell_cols", "tub_shell_cuts"):
        p = os.path.join(HERE, "..", "src", "revron", f + ".py")
        text = open(p).read()
        r = lint_source(text)
        print(f"{f}.py: {len(text.splitlines())} lines; literals per function:", {k: v["count"] for k, v in r["funcs"].items()}, r["problems"])


def compare(shape, ref_path=BASELINE, tag="new"):
    import numpy as np, trimesh
    from build123d import export_stl
    out = f"/tmp/tub_split_{tag}.stl"
    export_stl(shape, out, tolerance=0.001, angular_tolerance=0.05)
    new, ref = trimesh.load(out), trimesh.load(ref_path)
    print(f"volume new {shape.volume:.4f} (mesh {new.volume:.4f}) baseline mesh {ref.volume:.4f}")
    print("bbox dev", float(abs(new.bounds - ref.bounds).max()))
    worst = 0.0
    for a, b, nm in ((new, ref, "new->ref"), (ref, new, "ref->new")):   # 15000 samples: closest_point on a 370k-face mesh needs ~10 GB beyond that
        pts = trimesh.sample.sample_surface(a, 15000, seed=1)[0]
        _, d, _ = trimesh.proximity.closest_point(b, pts)
        print(f"{nm}: exact point-triangle max {d.max():.5f} p99.9 {np.percentile(d, 99.9):.5f}", flush=True)
        worst = max(worst, float(d.max()))
    print("RESULT", "OK" if worst < TOL else "FAIL", "max surface deviation", worst)
    return worst < TOL


if __name__ == "__main__":
    if "--lint" in sys.argv:
        lint()
        sys.exit(0)
    import revron
    t = time.time()
    fn = revron.tub.chassis if "--old" in sys.argv else swapped_chassis()
    shape = fn()
    print("built in", round(time.time() - t, 1), "s")
    sys.exit(0 if compare(shape, tag="old" if "--old" in sys.argv else "new") else 1)
