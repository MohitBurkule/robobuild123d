"""Optional progress log: one timestamped line per part build and per check group, appended to $ROBOT_PROGRESS_LOG.

Off unless the variable is set. Never raises: a log that cannot be written must not break a verify or render."""

from __future__ import annotations

import os
import time

_T0 = time.time()


def log(msg: str) -> None:
    path = os.environ.get("ROBOT_PROGRESS_LOG")
    if not path:
        return
    try:
        with open(path, "a") as f:
            f.write(f"{time.strftime('%Y-%m-%dT%H:%M:%S')} [{os.getpid()}] +{time.time() - _T0:.0f}s {msg}\n")
    except OSError:
        pass


_SEEN = {"n": 0}


def blockers(group: str, findings) -> None:
    """Append the blocker rows a check group just added to blockers_live.jsonl next to $ROBOT_PROGRESS_LOG (or to
    $ROBOT_BLOCKERS_LIVE), one JSON object per row, as soon as the group finishes."""
    import json
    log_path = os.environ.get("ROBOT_PROGRESS_LOG")
    path = os.environ.get("ROBOT_BLOCKERS_LIVE") or (os.path.join(os.path.dirname(log_path) or ".", "blockers_live.jsonl") if log_path else None)
    if not path:
        return
    findings = list(findings)
    if len(findings) < _SEEN["n"]:   # a new run in this process
        _SEEN["n"] = 0
    new, _SEEN["n"] = findings[_SEEN["n"]:], len(findings)
    rows = [f for f in new if not f.passed and str(f.severity).lower() == "blocker"]
    if not rows:
        return
    try:
        with open(path, "a") as fh:
            for f in rows:
                fh.write(json.dumps({"t": time.strftime("%Y-%m-%dT%H:%M:%S"), "pid": os.getpid(), "sha": os.environ.get("ROBOT_RUN_SHA"), "group": group, "id": f.id,
                                     "parts": list(getattr(f, "parts", []) or []), "message": f.message,
                                     "at": getattr(f, "at", None)}) + "\n")
    except OSError:
        pass


def reset() -> None:
    _SEEN["n"] = 0
