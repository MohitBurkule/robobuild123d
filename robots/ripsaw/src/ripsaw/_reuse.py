"""Reused Revron helpers, loaded without pulling in the whole Revron namespace.

plate.py, hw.py and weapon_motor.py are self-contained (no relative imports), so they are loaded by file path and
Ripsaw does not inherit Revron's masters. fork.py depends on Revron's fork params, so it is imported through the
`revron` package, lazily (only forks.py needs it).

UNTESTED: never run."""
import importlib.util
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
REVRON_SRC = os.path.join(ROOT, "robots", "revron", "src")
REVRON_PKG = os.path.join(REVRON_SRC, "revron")
for _p in (ROOT,):
    if _p not in sys.path:
        sys.path.insert(0, _p)


def _load(name):
    spec = importlib.util.spec_from_file_location(f"ripsaw_reuse_{name}", os.path.join(REVRON_PKG, f"{name}.py"))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


plate = _load("plate")              # holes(), polar(), ring_window(), round_corners(), placed()
hw = _load("hw")                    # size(), reach(), placed(), switch_mount()
weapon_motor = _load("weapon_motor")  # describe(), pick_bearing()


def revron_fork():
    """revron.fork (fork_local / fork_outline) and its params module; imports the revron package on first use."""
    if REVRON_SRC not in sys.path:
        sys.path.insert(0, REVRON_SRC)
    from revron import fork, params_drive
    return fork, params_drive
