"""[fix-G] Merge-gate decision helpers for robot/tools/ci_loop.sh.

  python3 robot/tools/ci_gate.py count LOG              # print number of [BLOCKER] lines (or -1 if the run did not finish)
  python3 robot/tools/ci_gate.py decide BRANCH SHA A0 A1 I0 I1 [PROGRESS_DIR]
        exit 0 = accept; exit 1 = reject (logs the [ci] line to builder.log and a row to blockers_live_<owner>.jsonl)
  python3 robot/tools/ci_gate.py kind FILE...           # print 'verifier-only' if every path is under robot/checks/ or docs
  python3 robot/tools/ci_gate.py groups "KNOWN" FILE...  # check groups the changed robot/checks modules feed ('all' if unsure)
  python3 robot/tools/ci_gate.py vanished BASE TRIAL     # exit 1 (and print them) if blockers in BASE are gone in TRIAL,
                                                         # or either log did not finish: a verifier change needs review
"""
import datetime, json, os, re, sys


def count_blockers(text, rc=None):
    """Blocker lines in a verify log; -1 when the run did not finish (no summary, or an exit code other than
    0 = clean / 2 = blockers found)."""
    if "blockers," not in text or (rc is not None and int(rc) not in (0, 2)):
        return -1
    return sum(1 for l in text.splitlines() if l.startswith("[BLOCKER]"))


def blocker_lines(text):
    return [l.strip() for l in text.splitlines() if l.startswith("[BLOCKER]")]


def vanished(base, trial):
    """Blocker lines of the base log missing from the trial log (multiset). None when either did not finish."""
    if count_blockers(base) < 0 or count_blockers(trial) < 0:
        return None
    left = list(blocker_lines(trial))
    gone = []
    for l in blocker_lines(base):
        if l in left:
            left.remove(l)
        else:
            gone.append(l)
    return gone


def check_groups(known, paths):
    """Check groups fed by the changed robot/checks modules: the module's own group name, else its `G = "..."`.
    Any module that maps to no known group (a shared helper) means every group: returns ['all']."""
    known = set(known)
    out = []
    for p in paths:
        if not (p.startswith("robot/checks/") and p.endswith(".py")):
            continue
        m = os.path.basename(p)[:-3]
        g = m if m in known else None
        if g is None:
            try:
                mm = re.search(r'^G = "([a-z_]+)"', open(p).read(), re.M)
            except OSError:
                mm = None
            g = mm.group(1) if mm and mm.group(1) in known else None
        if g is None:
            return ["all"]
        out.append(g)
    return sorted(set(out))


def owner(branch):
    m = re.match(r"(?:origin/)?fix-([A-Za-z])", branch)
    return m.group(1).upper() if m else "X"


def decide(a0, a1, i0, i1):
    """Accept only when every run finished (no -1, baseline or trial) and neither count rises. An unknown baseline is
    never an accept: the loop re-measures it once and holds the branch if it still did not finish."""
    if min(a0, a1, i0, i1) < 0:
        return False
    return a1 <= a0 and i1 <= i0


def reject_line(branch, sha, a0, a1, i0, i1):
    return f"[ci] gate rejected {branch.replace('origin/', '')} {sha}: assembly {a0}->{a1}, interference {i0}->{i1}"


def verifier_only(paths):
    def ok(p):
        return p.startswith("robot/checks/") or p.startswith("docs/") or p.endswith(".md")
    return bool(paths) and all(ok(p) for p in paths)


def report(branch, sha, a0, a1, i0, i1, pdir):
    line = reject_line(branch, sha, a0, a1, i0, i1)
    now = datetime.datetime.now().isoformat(timespec="seconds")
    with open(os.path.join(pdir, "builder.log"), "a") as f:
        f.write(f"{now} {line}\n")
    row = {"t": now, "pid": os.getpid(), "sha": sha, "group": "ci_gate", "id": "ci_gate.rejected",
           "parts": [], "message": line, "branch": branch.replace("origin/", ""),
           "assembly": [a0, a1], "interference": [i0, i1]}
    with open(os.path.join(pdir, f"blockers_live_{owner(branch)}.jsonl"), "a") as f:
        f.write(json.dumps(row) + "\n")
    return line


def main(argv):
    cmd = argv[0]
    if cmd == "count":
        rc = argv[2] if len(argv) > 2 else None
        print(count_blockers(open(argv[1], errors="replace").read(), rc))
        return 0
    if cmd == "groups":
        print(" ".join(check_groups(argv[1].split(), argv[2:])))
        return 0
    if cmd == "vanished":
        gone = vanished(open(argv[1], errors="replace").read(), open(argv[2], errors="replace").read())
        if gone is None:
            print("verify did not finish")
            return 1
        for l in gone:
            print(l)
        return 1 if gone else 0
    if cmd == "kind":
        print("verifier-only" if verifier_only(argv[1:]) else "geometry")
        return 0
    if cmd == "decide":
        b, sha = argv[1], argv[2]
        a0, a1, i0, i1 = map(int, argv[3:7])
        pdir = argv[7] if len(argv) > 7 else os.environ.get("PROGRESS_DIR", "/mnt/project-files/robot-cad/b123d/progress")
        if decide(a0, a1, i0, i1):
            return 0
        print(report(b, sha, a0, a1, i0, i1, pdir))
        return 1
    print(__doc__)
    return 2


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
