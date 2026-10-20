"""[fix-G] Merge-gate decision helpers for robot/tools/ci_loop.sh.

  python3 robot/tools/ci_gate.py count LOG              # print number of [BLOCKER] lines (or -1 if the run did not finish)
  python3 robot/tools/ci_gate.py decide BRANCH SHA A0 A1 I0 I1 [PROGRESS_DIR]
        exit 0 = accept; exit 1 = reject (logs the [ci] line to builder.log and a row to blockers_live_<owner>.jsonl)
  python3 robot/tools/ci_gate.py kind FILE...           # print 'verifier-only' if every path is under robot/checks/ or docs
  python3 robot/tools/ci_gate.py ok A0 A1 I0 I1          # exit 0 if not worse, 1 if worse (no logging)
  python3 robot/tools/ci_gate.py halves B...             # print the two bisect halves, one per line
"""
import datetime, json, os, re, sys


def count_blockers(text):
    if "blockers," not in text:
        return -1
    return sum(1 for l in text.splitlines() if l.startswith("[BLOCKER]"))


def owner(branch):
    m = re.match(r"(?:origin/)?fix-([A-Za-z])", branch)
    return m.group(1).upper() if m else "X"


def decide(a0, a1, i0, i1):
    """Reject when either count rises, or when a trial run did not finish (-1) while the baseline did."""
    worse = lambda b, t: (t < 0 <= b) or (b >= 0 and t > b)
    return not (worse(a0, a1) or worse(i0, i1))


def halves(branches):
    """Split a branch set for bisection: first half gets the extra one; order preserved."""
    k = (len(branches) + 1) // 2
    return list(branches[:k]), list(branches[k:])


def bisect(branches, gate):
    """Pure model of the combined gate in ci_loop.sh. gate(subset) -> True (not worse), False (worse) or
    None (infra failure). Returns {branch: 'pass'|'reject'|'hold'}.
    The whole set passing merges all; a failing single branch is rejected; otherwise both halves are gated
    (in parallel in the shell) and recursed. If every branch of both halves passes although the union failed
    (an interaction), the second half is held for the next round so the passing first half still merges."""
    branches = list(branches)
    if not branches:
        return {}
    r = gate(branches)
    if r is None:
        return {b: "hold" for b in branches}
    if r:
        return {b: "pass" for b in branches}
    if len(branches) == 1:
        return {branches[0]: "reject"}
    h1, h2 = halves(branches)
    out1, out2 = bisect(h1, gate), bisect(h2, gate)
    if all(v == "pass" for v in out1.values()) and all(v == "pass" for v in out2.values()):
        out2 = {b: "hold" for b in out2}
    return {**out1, **out2}


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
        print(count_blockers(open(argv[1], errors="replace").read()))
        return 0
    if cmd == "kind":
        print("verifier-only" if verifier_only(argv[1:]) else "geometry")
        return 0
    if cmd == "ok":
        return 0 if decide(*map(int, argv[1:5])) else 1
    if cmd == "halves":
        for h in halves(argv[1:]):
            print(" ".join(h))
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
