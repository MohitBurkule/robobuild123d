"""[fix-S] Revron master dimensions and module-level constants (measured on the RVRN 2.0 STEP)."""
# Themed modules, each building on the previous: chassis -> weapon -> side -> hardware -> spec -> drive.
# Master design params are at the top of params_chassis.py; docs/RELATIONS.md has the relation tree.
from .params_drive import *  # noqa: F401,F403
from .params_drive import __all__  # noqa: F401
