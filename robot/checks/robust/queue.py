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
import socket
import subprocess
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

STALE_S = 600.0
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


def code_hash(spec: str, model_rel: str) -> str:
    """cache.h(build-source hash, checks hash) of this checkout, as the runner keys results (runner.run)."""
    k = (spec, model_rel)
    if k not in _CODE:
        from ... import cache
        from . import discover as D
        from .runner import checks_hash

        files = D.package_files(Path(spec).resolve().parent / model_rel)
        _CODE[k] = cache.h(cache.h([f.read_bytes() for f in files]), checks_hash())
    return _CODE[k]


def enqueue(qdir, key: str, job: dict, timeout: float, sha: str | None = None, code: str = "") -> bool:
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
    _atomic(q / "tickets" / f"{key}.json", json.dumps({"key": key, "sha": sha or head_sha(), "code": code, "timeout": timeout, "job": j}))
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


def next_ticket(qdir, me: str, sha: str):
    q = Path(qdir)
    for t in sorted((q / "tickets").glob("*.json"), key=lambda p: p.stat().st_mtime if p.exists() else 0):
        try:
            tk = json.loads(t.read_text())
        except (ValueError, FileNotFoundError):
            continue
        if tk.get("code"):  # same robot + checks code as the enqueuer: its result is valid under the ticket's key
            j = tk["job"]
            try:
                mine = code_hash(str(REPO / j["spec"]) if not Path(j["spec"]).is_absolute() else j["spec"], j["model_rel"])
            except Exception:  # noqa: BLE001 - cannot hash here: leave it to another worker
                continue
            if mine != tk["code"]:
                continue
        elif tk.get("sha") and sha and tk["sha"] != sha:
            continue
        if claim(qdir, tk["key"], me):
            if (q / "results" / f"{tk['key']}.json").exists() or not t.exists():  # finished while we looked
                (q / "claims" / tk["key"]).unlink(missing_ok=True)
                continue
            return tk
    return None


def run_ticket(qdir, tk: dict, me: str, execute=None) -> dict:
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
    try:
        res = (execute or subprocess_execute)(job, float(tk.get("timeout") or 1800))
    finally:
        stop.set()
    final = res.get("stage") not in ("timeout", "worker") and not is_infra(res)
    if final:
        _atomic(q / "results" / f"{tk['key']}.json", json.dumps(res))
        (q / "tickets" / f"{tk['key']}.json").unlink(missing_ok=True)
    c.unlink(missing_ok=True)  # an unfinished job (timeout, crash, disk full) goes back to the queue
    return res


def work(qdir, workers=1, execute=None, log=print, once=False) -> int:
    sha = head_sha()
    me0 = f"{socket.gethostname()}:{os.getpid()}"
    done = [0]

    def loop(i):
        me = f"{me0}:{i}"
        while True:
            tk = next_ticket(qdir, me, sha)
            if tk is None:
                return
            t0 = time.time()
            res = run_ticket(qdir, tk, me, execute)
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
    a = ap.parse_args(argv)
    work(a.queue, a.workers)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
