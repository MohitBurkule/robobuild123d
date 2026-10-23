"""Run the baseline and the planned perturbations (each in its own worker process, a few at a time) inside a time
budget, then diff each against the baseline: a perturbation breaks when its build fails or it adds a blocker."""

from __future__ import annotations

import dataclasses
import json
import os
import subprocess
import sys
import tempfile
import time
from concurrent.futures import FIRST_COMPLETED, ThreadPoolExecutor, wait
from pathlib import Path

from ... import cache
from .worker import FAST_GROUPS, TAG


def subprocess_execute(job: dict, timeout: float) -> dict:
    """Run one job in a fresh interpreter (own `revron` import, ROBOT_JOBS=1 so no build pool mixes sources)."""
    import shutil

    td = tempfile.mkdtemp(prefix="robust_job_")  # removed here: a killed worker cannot clean up after itself
    job = dict(job, tmpdir=td)
    path = os.path.join(td, "job.json")
    with open(path, "w") as fh:
        json.dump(job, fh)
    env = dict(os.environ, ROBOT_JOBS="1", ROBOT_ROBUST_CHILD="1")
    env = {k: v for k, v in env.items() if not k.startswith("REVRON_")}
    try:
        p = subprocess.run([sys.executable, "-m", "robot.checks.robust.worker", path], capture_output=True, text=True,
                           timeout=timeout, env=env, cwd=str(Path(__file__).resolve().parents[3]))
        for ln in reversed(p.stdout.splitlines()):
            if ln.startswith(TAG):
                return json.loads(ln[len(TAG):])
        tail = (p.stderr or p.stdout).strip().splitlines()[-1:] or ["no output"]
        return {"id": job.get("id"), "error": f"worker died (rc {p.returncode}): {tail[0][:300]}", "stage": "worker", "blockers": []}
    except subprocess.TimeoutExpired:
        return {"id": job.get("id"), "error": f"timed out after {timeout:.0f} s", "stage": "timeout", "blockers": []}
    finally:
        shutil.rmtree(td, ignore_errors=True)


def key_of(b) -> tuple:
    """A blocker's identity across runs: check id + parts (messages carry numbers that move with any edit)."""
    return (b[0], b[1])


SWAP_EXEMPT = ("integrity.volume",)  # vs the previous run's volume: a swap or variant replaces the part on purpose


def diff(base: dict, res: dict, kind: str = "param") -> dict:
    """{'broken': bool, 'build_error': str|None, 'new': [blockers], 'fixed': [blocker keys]}. For a switch (variant,
    catalog choice, flag) a volume change of a rebuilt part is the intent, not a regression."""
    bk = {key_of(b) for b in base.get("blockers", [])}
    rk = {key_of(b) for b in res.get("blockers", [])}
    new = [b for b in res.get("blockers", []) if key_of(b) not in bk
           and not (kind != "param" and b[0] in SWAP_EXEMPT)]
    err = res.get("error") if res.get("stage") != "timeout" else None
    return {"broken": bool(err or new), "build_error": err, "new": new, "fixed": sorted(bk - rk),
            "timeout": res.get("stage") == "timeout"}


def checks_hash() -> str:
    """cache.code_hash minus this package: editing the sweep's own planning / report code keeps finished results."""
    here = Path(__file__).resolve().parent
    root = here.parents[1]
    files = sorted(f for f in root.rglob("*") if f.is_file() and "__pycache__" not in f.parts and here not in f.parents
                   and "tests" not in f.relative_to(root).parts and (f.suffix == ".py" or "catalog_data" in f.parts or "rules" in f.parts))
    files.append(here / "worker.py")  # how a perturbation is built and checked does change its result
    return cache.h(cache.VERSION, cache.lib_versions(), [(f.relative_to(root).as_posix(), cache.source_hash(f)) for f in files])


def job_key(job: dict, src_hash: str, spec_raw: dict) -> str:
    j = {k: v for k, v in job.items() if k not in ("timeout", "reads", "phase", "spec", "tmpdir")}
    if j.get("file") and job.get("spec"):  # checkout-independent: the edited file relative to the spec folder
        try:
            j["file"] = Path(j["file"]).resolve().relative_to(Path(job["spec"]).resolve().parent).as_posix()
        except ValueError:
            pass
    return cache.h("robust", 1, json.dumps(j, sort_keys=True, default=str), src_hash,
                   json.dumps(spec_raw, sort_keys=True, default=str), FAST_GROUPS)


def run(jobs, spec_path, model_rel, budget_s=900.0, workers=3, execute=subprocess_execute, src_hash="", clock=time.time,
        log=print, groups=None) -> dict:
    """{'baseline': result, 'results': {job id: (job, result, diff)}, 'not_run': [job ids], 'seconds': s}."""
    t0 = clock()
    spec_path = str(Path(spec_path).resolve())
    spec_raw = json.loads(Path(spec_path).read_text())
    common = {"spec": spec_path, "model_rel": model_rel}
    if groups:  # check groups other than FAST_GROUPS: the baseline runs the same ones, so the diff stays like for like
        common["groups"] = list(groups)

    ch = checks_hash() if src_hash else ""

    store = Path(os.environ["ROBOT_ROBUST_RESULTS"]) if os.environ.get("ROBOT_ROBUST_RESULTS") else None
    if store:  # per-job results kept beside the report (a shared folder): a restarted run resumes where it stopped
        store.mkdir(parents=True, exist_ok=True)

    def cached_exec(jd, timeout):
        k = cache.h(job_key(jd, src_hash, spec_raw), ch) if src_hash else None
        if k:
            f = store / f"{k}.json" if store else None
            if f is not None and f.exists():
                try:
                    return json.loads(f.read_text())
                except ValueError:
                    pass
            hit = cache.get("robust", k)
            if not cache.is_missing(hit):
                return hit
        res = execute(jd, timeout)
        if k and res.get("stage") not in ("timeout", "worker"):
            cache.put("robust", k, res)
            if store:
                tmp = store / f".{k}.tmp"
                tmp.write_text(json.dumps(res))
                tmp.replace(store / f"{k}.json")
        return res

    base = cached_exec(dict(common, id="baseline"), max(60.0, budget_s))
    out = {"baseline": base, "results": {}, "not_run": [], "seconds": 0.0}
    if base.get("error"):
        out["not_run"] = [j.id for j in jobs]
        out["seconds"] = round(clock() - t0, 1)
        return out
    broke_first = set()
    pending = [j for j in jobs if j.phase == 0]
    later = [j for j in jobs if j.phase != 0]
    running = {}
    with ThreadPoolExecutor(max(1, workers)) as ex:
        while pending or running or later:
            if not pending and not running and later:
                pending = [j for j in later if j.target in broke_first]
                out["not_run"] += [j.id + " (skipped: +-10% held)" for j in later if j.target not in broke_first]
                later = []
                continue
            left = budget_s - (clock() - t0)
            while pending and len(running) < max(1, workers) and left > 30:
                j = pending.pop(0)
                jd = dict(dataclasses.asdict(j), **common, timeout=max(30.0, left))
                running[ex.submit(cached_exec, jd, max(30.0, left))] = j
            if not running:
                out["not_run"] += [j.id for j in pending] + [j.id for j in later]
                pending, later = [], []
                break
            done, _ = wait(list(running), return_when=FIRST_COMPLETED)
            for fut in done:
                j = running.pop(fut)
                res = fut.result()
                d = diff(base, res, j.kind)
                if d["broken"] and j.phase == 0:
                    broke_first.add(j.target)
                out["results"][j.id] = (j, res, d)
                log(f"  robust {j.id}: {'BREAKS' if d['broken'] else 'timeout' if d['timeout'] else 'ok'} "
                    f"({res.get('seconds', '?')} s, rebuilt {len(res.get('rebuilt') or [])})")
    out["seconds"] = round(clock() - t0, 1)
    return out
