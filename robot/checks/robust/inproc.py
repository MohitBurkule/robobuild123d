"""In-process sweep execution (UNTESTED draft): run settings-only jobs (job["env"] = {legacy env var: value}, no source
edit) inside this interpreter under a robot.design.Design instead of a fresh process per point.

- `inproc_execute(job, timeout)` has the same signature/result as runner.subprocess_execute, so it drops into
  runner.run(execute=...) and queue.run_ticket(execute=...). Jobs it cannot run in-process (source edits, overlays on
  regenerated specs, no settings.py) fall back to subprocess_execute.
- results are memoised in a resumable on-disk store keyed by param hash (design values + code hash + groups), so a
  restarted sweep skips points already done.
- per-part geometry cache: geom.key_for now folds the active Design into the key, so parts whose inputs did not
  change hit the cache and only changed parts rebuild.
- `pool_execute(jobs, workers)` runs settings jobs on a process pool (each worker keeps its imports warm across many
  points: one import cost per worker, not per point).
"""

from __future__ import annotations

import json
import multiprocessing
import os
import time
from concurrent.futures import ProcessPoolExecutor, as_completed
from pathlib import Path

from ... import cache

RESULTS_DIR = Path(os.environ.get("ROBOT_INPROC_RESULTS", "progress/inproc_results"))


def param_hash(job: dict, code: str = "") -> str:
    """Stable hash of everything a settings job's result depends on (incl. the code hash)."""
    return cache.h(json.dumps(dict(spec=str(job.get("spec")), env=job.get("env") or {}, overlay=job.get("overlay"),
                                   groups=job.get("groups"), code=code or job.get("code") or cache.code_hash()), sort_keys=True))


def _store(key: str) -> Path:
    return RESULTS_DIR / f"{key}.json"


def load_result(key: str) -> dict | None:
    try:
        return json.loads(_store(key).read_text())
    except (OSError, ValueError):
        return None


def save_result(key: str, res: dict) -> None:
    RESULTS_DIR.mkdir(parents=True, exist_ok=True)
    tmp = _store(key).with_suffix(".tmp")
    tmp.write_text(json.dumps(res))
    os.replace(tmp, _store(key))  # atomic: a killed run never leaves half a result


def can_inproc(job: dict) -> bool:
    """Settings-only jobs: no source edit, and the robot has a settings.py with build(design)."""
    if job.get("file") or job.get("append"):
        return False
    try:
        from ...design import load_settings

        return hasattr(load_settings(Path(job["spec"]).resolve().parent), "build")
    except Exception:  # noqa: BLE001
        return False


def run_inproc(job: dict) -> dict:
    """Build the spec under the job's Design in this process, then verify the fast groups."""
    from ...design import load_settings, use
    from ...spec import Spec
    from .. import Options, verify
    from .worker import FAST_GROUPS, blockers

    t0 = time.time()
    spec_dir = Path(job["spec"]).resolve().parent
    mod = load_settings(spec_dir)
    res = {"id": job.get("id", "baseline"), "rebuilt": [], "error": None, "blockers": [], "inproc": True}
    try:
        d = mod.SCHEMA.design(job.get("env") or {})  # Design accepts legacy env var names as keys
    except Exception as e:  # noqa: BLE001
        res.update(error=f"design invalid: {e}", stage="build")
        return res
    with use(d):
        try:
            raw = mod.build(d)
        except Exception as e:  # noqa: BLE001 - a build failure is a result
            res.update(error=f"{type(e).__name__}: {e}", stage="build", seconds=round(time.time() - t0, 1))
            return res
        if job.get("overlay"):
            from ... import overlay

            try:
                raw = overlay.apply(raw, job["overlay"], overlay.load_hooks(raw, spec_dir))
            except Exception as e:  # noqa: BLE001
                res.update(error=f"overlay failed: {e}", stage="build", seconds=round(time.time() - t0, 1))
                return res
            res["overlaid"] = True
        rep = verify(Spec(raw, spec_dir), Options(only=list(job.get("groups") or FAST_GROUPS)))
    res["blockers"] = blockers(rep)
    res["seconds"] = round(time.time() - t0, 1)
    return res


def inproc_execute(job: dict, timeout: float, progress=None, **kw) -> dict:
    """Drop-in for runner.subprocess_execute. NOTE: no hard timeout in-process (cannot kill a thread); pool_execute
    is the place to enforce one."""
    if not can_inproc(job):
        from .runner import subprocess_execute

        return subprocess_execute(job, timeout, progress=progress, **kw)
    key = param_hash(job)
    hit = load_result(key)
    if hit is not None:
        return dict(hit, cached=True)
    try:
        res = run_inproc(job)
    except Exception as e:  # noqa: BLE001
        res = {"id": job.get("id", "baseline"), "error": f"{type(e).__name__}: {e}", "stage": "worker", "blockers": []}
    if res.get("stage") != "worker":  # crashes are infra: retry next time, don't memoise
        save_result(key, res)
    return res


def _child(job):
    os.environ["ROBOT_ROBUST_CHILD"] = "1"
    return job.get("id"), inproc_execute(job, float(job.get("timeout", 600)))


def pool_execute(jobs, workers: int = 3, timeout: float = 900.0, log=print) -> dict:
    """{job id: result} for many jobs on a warm process pool; done points come from the result store (resumable)."""
    out, todo = {}, []
    for j in jobs:
        hit = load_result(param_hash(j)) if can_inproc(j) else None
        if hit is not None:
            out[j.get("id")] = dict(hit, cached=True)
        else:
            todo.append(j)
    log(f"inproc: {len(out)} cached, {len(todo)} to run on {workers} workers")
    # spawn: max_tasks_per_child is rejected with the default fork start method on Linux
    with ProcessPoolExecutor(max_workers=workers, max_tasks_per_child=20, mp_context=multiprocessing.get_context("spawn")) as ex:
        futs = {ex.submit(_child, j): j for j in todo}
        for f in as_completed(futs):
            j = futs[f]
            try:
                jid, res = f.result(timeout=timeout)
            except Exception as e:  # noqa: BLE001
                jid, res = j.get("id"), {"id": j.get("id"), "error": f"{type(e).__name__}: {e}", "stage": "worker", "blockers": []}
            out[jid] = res
            log(f"inproc: {jid} -> {'error' if res.get('error') else len(res.get('blockers', []))}")
    return out
