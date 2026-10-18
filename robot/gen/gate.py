"""Final gate: every complete robot the engine emits passes the verifier with zero blockers.

`gate(h)` builds the hypothesis, verifies it, and on blockers tries repairs in order (the next-best layouts, then
other solver seeds). If nothing passes it raises `Rejected` with the last report's blockers; it never returns a spec
with a blocker.
"""

from __future__ import annotations

from dataclasses import dataclass, field

from .. import checks
from .. import spec as spec_mod
from ..finding import BLOCKER
from . import build


class Rejected(RuntimeError):
    def __init__(self, slug, attempts):
        self.attempts = attempts
        last = attempts[-1]["blockers"] if attempts else []
        super().__init__(f"{slug}: no variant passed the verifier; last blockers: {last[:5]}")


@dataclass
class GateResult:
    spec: dict
    report: object
    attempts: list = field(default_factory=list)


def blockers(rep) -> list[str]:
    return [f"{f.id}: {f.message}" for f in rep.findings if not f.passed and f.severity == BLOCKER]


def verify_dict(d: dict, fast=False, deep=True, base_dir=None):
    return checks.verify(spec_mod.Spec(d, base_dir), checks.Options(fast=fast, deep=deep))


def repairs(max_layouts=3, seeds=(0, 1)):
    """(user overrides, layout index) to try, in order."""
    for seed in seeds:
        for i in range(max_layouts):
            yield {"seed": seed}, i


def gate(h, user: dict | None = None, fast=False, max_layouts=3, seeds=(0, 1), log=None) -> GateResult:
    attempts = []
    for over, idx in repairs(max_layouts, seeds):
        u = dict(user or {}, **over)
        try:
            d = build.build(h, u, layout_index=idx)
        except ValueError as e:
            attempts.append({"seed": u.get("seed"), "layout": idx, "blockers": [f"build: {e}"]})
            continue
        rep = verify_dict(d, fast=fast)
        b = blockers(rep)
        attempts.append({"seed": u.get("seed"), "layout": idx, "blockers": b})
        if log:
            log(f"  seed {u.get('seed')} layout {idx}: {len(b)} blockers")
        if not b:
            d.setdefault("generator", {})["gate"] = {"attempts": len(attempts), "fast": fast}
            return GateResult(d, rep, attempts)
    raise Rejected(getattr(h, "slug", str(h)), attempts)
