"""One perturbation in its own process: copy the build sources, apply the edit, regenerate the spec, rebuild only the
affected parts (the others keep their cached geometry: same shape JSON + same sources = same per-part cache key) and
run the fast groups. Prints one JSON line `ROBUST_RESULT {...}`.

  python -m robot.checks.robust.worker <job.json>      (job = plan.Job fields + spec path; no job fields = baseline)
"""

from __future__ import annotations

import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
from pathlib import Path

FAST_GROUPS = ["integrity", "interference", "connections", "assembly", "fastener_seat"]
REPO = Path(__file__).resolve().parents[3]
TAG = "ROBUST_RESULT "


def apply_edit(path: Path, job: dict) -> None:
    """Replace the literal span (one line) or append a line; raises if the span does not hold the expected literal."""
    text = path.read_text()
    if job.get("append"):
        path.write_text(text + job["append"])
        return
    lines = text.splitlines(keepends=True)
    i = job["line"] - 1
    ln = lines[i]
    lines[i] = ln[:job["col"]] + job["new_text"] + ln[job["end_col"]:]
    path.write_text("".join(lines))


def stage_copy(spec_path: Path, model_rel: str, tmp: Path) -> tuple:
    """Mirror the spec folder under `tmp` at its repo-relative path: the model's top folder copied, the rest symlinked.
    `tmp/robot/templates` is a real folder so generators that also write a template never touch the repo."""
    spec_dir = spec_path.resolve().parent
    try:
        rel = spec_dir.relative_to(REPO)
    except ValueError:
        rel = Path(spec_dir.name)
    dst = tmp / rel
    dst.mkdir(parents=True)
    top = Path(model_rel).parts[0]
    for e in spec_dir.iterdir():
        if e.name == top:
            shutil.copytree(e, dst / e.name, ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        elif e.name != "spec.json":
            (dst / e.name).symlink_to(e)
    (tmp / "robot" / "templates").mkdir(parents=True)
    return spec_dir, dst


def regenerate(dst: Path, model_rel: str, tmp: Path, timeout: float) -> str | None:
    """Run the model file as a script (it writes spec.json next to its folder). Returns an error text or None."""
    env = {k: v for k, v in os.environ.items() if not k.startswith("REVRON_")}
    env["PYTHONPATH"] = str(REPO)
    try:
        p = subprocess.run([sys.executable, str(dst / model_rel)], cwd=tmp, env=env, capture_output=True, text=True, timeout=timeout)
    except subprocess.TimeoutExpired:
        return f"spec generation timed out after {timeout:.0f} s"
    if p.returncode or not (dst / "spec.json").exists():
        tail = (p.stderr or p.stdout).strip().splitlines()[-1:] or ["no output"]
        return f"spec generation failed (rc {p.returncode}): {tail[0][:300]}"
    return None


def _rewrite_models(shape, absfile: str):
    if isinstance(shape, dict):
        if shape.get("type") == "model" and shape.get("file"):
            shape["file"] = absfile
        for v in shape.values():
            _rewrite_models(v, absfile)
    elif isinstance(shape, list):
        for v in shape:
            _rewrite_models(v, absfile)


def hybrid_spec(base_raw: dict, new_raw: dict, reads: list, model_rel: str, new_model: Path, spec_dir: Path, tess) -> tuple:
    """The perturbed spec, with the parts whose build reads the edit (or whose spec entry changed, or that are not cached)
    pointed at the edited sources; every other part keeps its baseline entry and so its cached geometry."""
    from ... import geom
    from ...spec import Spec
    from ...world import _part_shape

    base = {p["id"]: p for p in base_raw.get("parts", [])}
    raw = json.loads(json.dumps(new_raw))
    rebuilt = []
    probe = Spec(raw, spec_dir)
    by_id = {p.id: p for p in probe.parts}
    for p in raw.get("parts", []):
        pid = p["id"]
        changed = base.get(pid) != p
        sh = _part_shape(by_id[pid]) if pid in by_id else None
        has_model = bool(sh and json.dumps(sh).find('"type": "model"') >= 0)
        if not has_model:
            continue
        stale = pid in reads or changed
        if not stale:
            try:
                stale = not geom.cached(geom.key_for(sh, spec_dir, tess))
            except Exception:  # noqa: BLE001 - cannot key it: rebuild it
                stale = True
        if stale:
            if p.get("model"):
                p["model"] = str(new_model)
            if p.get("shape"):
                _rewrite_models(p["shape"], str(new_model))
            rebuilt.append(pid)
    return raw, rebuilt


def blockers(rep) -> list:
    return sorted({(f.id, ",".join(sorted(f.parts or [])), (f.message or "")[:200]) for f in rep.findings
                   if not f.passed and str(f.severity).lower() == "blocker"})


def run_job(job: dict) -> dict:
    t0 = time.time()
    spec_path = Path(job["spec"]).resolve()
    base_raw = json.loads(spec_path.read_text())
    model_rel = job["model_rel"]
    from ... import geom
    from ...spec import Spec
    from .. import Options, verify
    from .. import integrity

    res = {"id": job.get("id", "baseline"), "rebuilt": [], "error": None, "blockers": []}
    with tempfile.TemporaryDirectory(prefix="robust_", dir=job.get("tmpdir")) as td:
        tmp = Path(td)
        store = tmp / "integrity.json"
        src_store = integrity.store_path(base_raw.get("name"))
        if Path(src_store).exists():
            shutil.copy(src_store, store)
        integrity.store_path = lambda name: store  # never move the real previous-volume baseline
        if job.get("file"):
            spec_dir, dst = stage_copy(spec_path, model_rel, tmp)
            target = dst / Path(job["file"]).resolve().relative_to(spec_dir)
            try:
                apply_edit(target, job)
            except Exception as e:  # noqa: BLE001
                res["error"] = f"edit failed: {e}"
                return res
            err = regenerate(dst, model_rel, tmp, float(job.get("timeout", 600)))
            if err:
                res.update(error=err, stage="build", seconds=round(time.time() - t0, 1))
                return res
            new_raw = json.loads((dst / "spec.json").read_text())
            raw, res["rebuilt"] = hybrid_spec(base_raw, new_raw, set(job.get("reads") or []), model_rel, dst / model_rel, spec_dir, geom.FINE)
        else:
            raw, spec_dir = base_raw, spec_path.parent
        rep = verify(Spec(raw, spec_dir), Options(only=list(FAST_GROUPS)))
        res["blockers"] = blockers(rep)
        res["seconds"] = round(time.time() - t0, 1)
    return res


def main(argv=None):
    argv = argv or sys.argv[1:]
    os.environ["ROBOT_ROBUST_CHILD"] = "1"
    job = json.loads(Path(argv[0]).read_text())
    try:
        res = run_job(job)
    except Exception as e:  # noqa: BLE001 - a crash is a result, not a lost job
        res = {"id": job.get("id", "baseline"), "error": f"{type(e).__name__}: {e}", "stage": "worker", "blockers": []}
    print(TAG + json.dumps(res), flush=True)


if __name__ == "__main__":
    main()
