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
