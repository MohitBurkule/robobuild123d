"""[fix-G] Merge-gate decision helpers for robot/tools/ci_loop.sh.

  python3 robot/tools/ci_gate.py count LOG              # print number of [BLOCKER] lines (or -1 if the run did not finish)
  python3 robot/tools/ci_gate.py decide BRANCH SHA A0 A1 I0 I1 [PROGRESS_DIR]
        exit 0 = accept; exit 1 = reject (logs the [ci] line to builder.log and a row to blockers_live_<owner>.jsonl)
  python3 robot/tools/ci_gate.py kind FILE...           # print 'verifier-only' if every path is under robot/checks/ or docs
  python3 robot/tools/ci_gate.py groups "KNOWN" FILE...  # check groups the changed robot/checks modules feed ('all' if unsure)
  python3 robot/tools/ci_gate.py vanished BASE TRIAL     # exit 1 (and print them) if blockers in BASE are gone in TRIAL,
                                                         # or either log did not finish: a verifier change needs review
  python3 robot/tools/ci_gate.py ok A0 A1 I0 I1          # exit 0 if not worse, 1 if worse (no logging)
  python3 robot/tools/ci_gate.py halves B...             # print the two bisect halves, one per line
  python3 robot/tools/ci_gate.py state FILE get KEY      # print a key of the round-state json ('' if absent)
  python3 robot/tools/ci_gate.py state FILE set K=V...   # update keys atomically (tmp + rename; the file is on a share)
  python3 robot/tools/ci_gate.py unitok LOG RC           # exit 0 pass, 1 tests failed, 2 infra (no pytest summary)
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


def state_load(path):
    try:
        with open(path) as f:
            d = json.load(f)
        return d if isinstance(d, dict) else {}
    except (OSError, ValueError):
        return {}


def state_set(path, pairs):
    """Merge K=V pairs into the round-state json; written to a temp name and renamed so a kill never leaves half a file."""
    d = state_load(path)
    for kv in pairs:
        k, _, v = kv.partition("=")
        d[k] = v
    d["t"] = datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    tmp = f"{path}.tmp.{os.getpid()}"
    with open(tmp, "w") as f:
        json.dump(d, f, indent=1, sort_keys=True)
    os.replace(tmp, path)
    return d


def unit_result(text, rc):
    """0 = unit tests passed, 1 = failed, 2 = infra (killed/timeout/not a pytest run, e.g. an old shard worker)."""
    if not re.search(r"\b(passed|failed|errors?|no tests ran)\b.* in [0-9.]+s", text):
        return 2
    return 0 if int(rc) == 0 else 1


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
    if cmd == "ok":
        return 0 if decide(*map(int, argv[1:5])) else 1
    if cmd == "state":
        if argv[2] == "get":
            v = state_load(argv[1]).get(argv[3], "")
            print(v)
            return 0
        state_set(argv[1], argv[3:])
        return 0
    if cmd == "unitok":
        try:
            text = open(argv[1], errors="replace").read()
        except OSError:
            return 2
        return unit_result(text, argv[2] if argv[2].lstrip("-").isdigit() else 99)
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
