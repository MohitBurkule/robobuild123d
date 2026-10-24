"""Shared-folder job queue for the robust / hypothesis sweeps, so any number of containers can work one sweep.

  enqueue: ROBOT_ROBUST_QUEUE=<dir> python3 -m robot.checks.robust.hyp <spec> --out <md> ...
           every job whose result is not in <dir>/results becomes a ticket <dir>/tickets/<key>.json; the report is
           written from the results that exist (the rest show as "not run"). Re-run it to refresh the report.
  work:    python3 -m robot.checks.robust.queue <dir> [--workers N]
           claim a ticket (<dir>/claims/<key>), run it, write <dir>/results/<key>.json, drop the ticket. A claim is
           refreshed every 60 s while its job runs; one older than STALE_S (its container died) is taken over.
           A worker runs only tickets whose code hash (build sources + checks code, what the result key hashes) matches
           its own checkout, so any commit with the same robot and checks code can help.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import socket
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

STALE_S = 900.0   # a claim not refreshed this long belongs to a dead container; purged at startup
JOB_CAP_S = 3600.0  # per-ticket wall-clock cap, whatever --budget the enqueuer had (a hung job must come back)
MIN_FREE_B = 1.5e9  # do not start a job with less free disk under the geometry cache: it would fail ENOSPC and loop


def purge_stale_claims(qdir, now=time.time) -> int:
    n = 0
    for c in (Path(qdir) / "claims").glob("*"):
        try:
            if now() - c.stat().st_mtime > STALE_S:
                c.unlink()
                n += 1
        except FileNotFoundError:
            pass
    return n


def disk_ok(min_free=None) -> bool:
    """Enough free space where jobs write: the local part cache (ROBOT_CACHE) and the job folders (TMPDIR), e.g. both
    on /dev/shm. ROBOT_MIN_FREE_GB overrides the floor (on /dev/shm keep RAM for the builds)."""
    import tempfile

    from ...geom import cache_dir

    if min_free is None:
        min_free = float(os.environ.get("ROBOT_MIN_FREE_GB") or MIN_FREE_B / 1e9) * 1e9
    return all(shutil.disk_usage(d).free >= min_free for d in (cache_dir(), tempfile.gettempdir()))
BEAT_S = 60.0
REPO = Path(__file__).resolve().parents[3]


def head_sha(repo: Path = REPO) -> str:
    try:
        return subprocess.run(["git", "rev-parse", "HEAD"], cwd=repo, capture_output=True, text=True).stdout.strip()
    except OSError:
        return ""


def _rel(p):
    try:
        return Path(p).resolve().relative_to(REPO).as_posix()
    except ValueError:
        return p


def _atomic(path: Path, text: str):
    tmp = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    tmp.write_text(text)
    tmp.replace(path)


_CODE: dict = {}


_PARTS: dict = {}


def model_hash(spec: str, model_rel: str) -> str:
    """The model's python sources: git-tracked files of its package, by path relative to it, with their content."""
    from ... import cache
    from . import discover as D

    pkg = (Path(spec).resolve().parent / model_rel).parent
    files = cache.tracked(D.package_files(pkg / Path(model_rel).name), pkg)
    _PARTS[(spec, model_rel)] = dict(model_files=len(files))
    return cache.h([(f.relative_to(pkg).as_posix(), f.read_bytes()) for f in files])


def code_hash(spec: str, model_rel: str) -> str:
    """cache.h(model_hash, checks_hash) of this checkout: exactly the `code` the enqueuer (runner.run) writes."""
    k = (spec, model_rel)
    if k not in _CODE:
        from ... import cache
        from .runner import checks_hash

        m, c = model_hash(spec, model_rel), checks_hash()
        _CODE[k] = cache.h(m, c)
        _PARTS[k].update(model=m, checks=c)
    return _CODE[k]


def enqueue(qdir, key: str, job: dict, timeout: float, sha: str | None = None, code: str = "", parts: dict | None = None) -> bool:
    """Write a ticket unless the result or the ticket exists. True when a ticket was written."""
    q = Path(qdir)
    for d in ("tickets", "claims", "results"):
        (q / d).mkdir(parents=True, exist_ok=True)
    if (q / "results" / f"{key}.json").exists() or (q / "tickets" / f"{key}.json").exists():
        return False
    j = dict(job)
    for k in ("spec", "file"):
        if j.get(k):
            j[k] = _rel(j[k])
    _atomic(q / "tickets" / f"{key}.json", json.dumps({"key": key, "sha": sha or head_sha(), "code": code, "code_parts": parts or {}, "timeout": timeout, "job": j}))
    return True


def claim(qdir, key: str, me: str, now=time.time) -> bool:
    """Take the ticket: create the claim, or take over one not refreshed for STALE_S."""
    c = Path(qdir) / "claims" / key
    try:
        fd = os.open(c, os.O_CREAT | os.O_EXCL | os.O_WRONLY)
        os.write(fd, me.encode())
        os.close(fd)
        return True
    except FileExistsError:
        try:
            if now() - c.stat().st_mtime < STALE_S:
                return False
        except FileNotFoundError:
            return claim(qdir, key, me, now)
        _atomic(c, me)  # stale: its worker died; take it, then make sure no one else did at the same moment
        time.sleep(0.5)
        try:
            return c.read_text() == me
        except FileNotFoundError:
            return False


def next_ticket(qdir, me: str, sha: str, log=None, why=None):
    """The next ticket this checkout may run, claimed. `why` collects the reason per skipped ticket."""
    q = Path(qdir)
    why = why if why is not None else {}
    def order(p):  # baselines first: they warm the part cache every other job reuses
        try:
            return (0 if "baseline" in p.read_text()[:4000] else 1, p.stat().st_mtime)
        except FileNotFoundError:
            return (2, 0)

    for t in sorted((q / "tickets").glob("*.json"), key=order):
        try:
            tk = json.loads(t.read_text())
        except (ValueError, FileNotFoundError):
            continue
        if tk.get("code"):  # same robot + checks code as the enqueuer: its result is valid under the ticket's key
            j = tk["job"]
            try:
                mine = code_hash(str(REPO / j["spec"]) if not Path(j["spec"]).is_absolute() else j["spec"], j["model_rel"])
            except Exception as e:  # noqa: BLE001 - cannot hash here: leave it to another worker
                why[tk["key"]] = f"cannot hash: {e}"
                continue
            if mine != tk["code"]:
                cp = tk.get("code_parts") or {}
                mp = _PARTS.get((str(REPO / j["spec"]) if not Path(j["spec"]).is_absolute() else j["spec"], j["model_rel"])) or {}
                diff = [n for n in ("model", "checks") if cp.get(n) and cp.get(n) != mp.get(n)]
                why[tk["key"]] = f"code {tk['code'][:8]} != mine {mine[:8]}" + (f" ({'+'.join(diff)} differ)" if diff else "")
                continue
        elif tk.get("sha") and sha and tk["sha"] != sha:
            why[tk["key"]] = f"sha {tk['sha'][:8]} != {sha[:8]}"
            continue
        if claim(qdir, tk["key"], me):
            if (q / "results" / f"{tk['key']}.json").exists() or not t.exists():  # finished while we looked
                (q / "claims" / tk["key"]).unlink(missing_ok=True)
                continue
            return tk
        why[tk["key"]] = "claimed elsewhere"
    return None


def run_ticket(qdir, tk: dict, me: str, execute=None, log=None) -> dict:
    from .runner import is_infra, subprocess_execute

    q = Path(qdir)
    c = q / "claims" / tk["key"]
    stop = threading.Event()

    def beat():
        while not stop.wait(BEAT_S):
            try:
                os.utime(c)
            except FileNotFoundError:
                return

    th = threading.Thread(target=beat, daemon=True)
    th.start()
    job = dict(tk["job"])
    for k in ("spec", "file"):
        if job.get(k) and not Path(job[k]).is_absolute():
            job[k] = str(REPO / job[k])
    to = min(float(tk.get("timeout") or 1800), JOB_CAP_S)
    jid = tk["job"].get("id")
    if log:
        log(f"  {me} {jid}: start ({tk['key'][:8]})")
    try:
        if execute:
            res = execute(job, to)
        else:  # progress every minute: elapsed, child CPU, parts built, CPU-idle time (a stall shows as idle growing)
            res = subprocess_execute(job, to, progress=(lambda d: log(f"  {me} {jid}: running " + " ".join(f"{k}={v}" for k, v in d.items()))) if log else None)
    finally:
        stop.set()
    final = res.get("stage") not in ("timeout", "worker") and not is_infra(res)
    if final:
        _atomic(q / "results" / f"{tk['key']}.json", json.dumps(res))
        (q / "tickets" / f"{tk['key']}.json").unlink(missing_ok=True)
    c.unlink(missing_ok=True)  # an unfinished job (timeout, crash, disk full) goes back to the queue
    return res


POLL_S = 60.0


def describe(qdir) -> str:
    """This checkout's code hash and its parts, for the worker log (to compare across containers)."""
    import sys

    from ... import cache

    lines = []
    for t in sorted((Path(qdir) / "tickets").glob("*.json"))[:1]:
        j = json.loads(t.read_text())["job"]
        spec = str(REPO / j["spec"]) if not Path(j["spec"]).is_absolute() else j["spec"]
        lines.append(f"code {code_hash(spec, j['model_rel'])} {_PARTS.get((spec, j['model_rel']))}")
    lines.append(f"python {sys.version.split()[0]}; libs {cache.lib_versions()}; repo {REPO}; head {head_sha()[:12]}")
    return "\n".join(lines)


def _log(*a):
    print(time.strftime("%H:%M:%S"), *a, flush=True)  # nohup'd to a file: unflushed lines only appear at exit


def work(qdir, workers=1, execute=None, log=_log, once=False, poll=False) -> int:
    sha = head_sha()
    me0 = f"{socket.gethostname()}:{os.getpid()}:{os.urandom(3).hex()}"  # every container is "vm" and pids repeat after a restart
    try:
        log("queue: " + describe(qdir))
    except Exception as e:  # noqa: BLE001 - diagnostics only
        log(f"queue: describe failed: {e}")
    n = purge_stale_claims(qdir)
    if n:
        log(f"queue: dropped {n} claim(s) older than {STALE_S / 60:.0f} min")
    done = [0]

    def loop(i):
        me = f"{me0}:{i}"
        while True:
            if not disk_ok():
                log(f"  {me}: low free space under the part cache or TMPDIR; stopping (free space, then re-run)")
                return
            why = {}
            tk = next_ticket(qdir, me, sha, why=why)
            if tk is None:
                if not why:
                    return  # queue empty
                kinds = {}
                for w in why.values():
                    kinds[w] = kinds.get(w, 0) + 1
                if i == 0:
                    log(f"  {me}: nothing to take: " + "; ".join(f"{n} x {w}" for w, n in sorted(kinds.items(), key=lambda x: -x[1])[:4]))
                if all(w == "claimed elsewhere" for w in why.values()) or poll:
                    time.sleep(POLL_S)  # others hold them; they come back if their container dies
                    continue
                return
            t0 = time.time()
            res = run_ticket(qdir, tk, me, execute, log)
            done[0] += 1
            log(f"  {me} {tk['job'].get('id')}: {res.get('error') or 'ok'} ({time.time() - t0:.0f} s)")
            if once:
                return

    with ThreadPoolExecutor(max(1, workers)) as ex:
        list(ex.map(loop, range(max(1, workers))))
    left = len(list((Path(qdir) / "tickets").glob("*.json")))
    log(f"queue: ran {done[0]}; {left} ticket(s) left" + (" (other commits or claimed elsewhere)" if left else ""))
    return done[0]


def main(argv=None):
    ap = argparse.ArgumentParser(prog="robot.checks.robust.queue")
    ap.add_argument("queue")
    ap.add_argument("--workers", type=int, default=2)
    ap.add_argument("--poll", action="store_true", help="keep waiting for tickets this checkout can run")
    ap.add_argument("--shared-cache", default=None, help="part cache shared by all containers (default: <queue>/../../cache)")
    a = ap.parse_args(argv)
    os.environ.setdefault("ROBOT_SHARED_CACHE", a.shared_cache or str(Path(a.queue).resolve().parents[1] / "cache"))
    (Path(a.queue) / "logs").mkdir(exist_ok=True)
    own = open(Path(a.queue) / "logs" / f"{socket.gethostname()}-{time.strftime('%m%d-%H%M%S')}-{os.getpid()}-{os.urandom(2).hex()}.log", "a")

    def log(*m):  # one log file per worker process: shared files appended from several containers lose lines
        line = " ".join([time.strftime("%H:%M:%S"), *map(str, m)])
        print(line, flush=True)
        own.write(line + "\n")
        own.flush()

    work(a.queue, a.workers, poll=a.poll, log=log)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
