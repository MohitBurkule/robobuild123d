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
from . import intent as intent_mod


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


# generator features that remove material, keyed by the part-id prefix the verifier reports saveable mass on
LIGHTENABLE = {"wheel": "wheel", "top_bridge": "bridge", "upright": "upright"}
SAVE_MIN_G = 0.4


def saveable(rep) -> dict:
    """{feature: grams} from the verifier's `material.saveable_g.<part>` metrics, for features we know how to pocket."""
    out = {}
    for k, v in (getattr(rep, "metrics", None) or {}).items():
        if not k.startswith("material.saveable_g.") or v < SAVE_MIN_G:
            continue
        pid = k[len("material.saveable_g."):]
        for pre, feat in LIGHTENABLE.items():
            if pid.startswith(pre):
                out[feat] = out.get(feat, 0.0) + float(v)
    return out


def lighten(h, user, idx, res, fast, log=None):
    """Material removal driven by the verifier: rebuild with pockets in the parts it reports as saveable, and keep
    the lighter variant only if it still has zero blockers."""
    feats = saveable(res.report)
    if not feats:
        return res
    u = dict(user, lighten=sorted(set(user.get("lighten", ())) | set(feats)))
    try:
        d = build.build(h, u, layout_index=idx)
    except ValueError:
        return res
    rep = verify_dict(d, fast=fast)
    b = blockers(rep)
    if log:
        log(f"  lighten {sorted(feats)}: {len(b)} blockers")
    if b:
        return res
    d.setdefault("generator", {})["lightened"] = {k: round(v, 2) for k, v in feats.items()}
    return GateResult(d, rep, res.attempts + [{"lighten": sorted(feats), "blockers": []}])


def gate(h, user: dict | None = None, fast=False, max_layouts=3, seeds=(0, 1), log=None) -> GateResult:
    attempts = []
    for over, idx in repairs(max_layouts, seeds):
        u = dict(user or {}, **over)
        try:
            d = build.build(h, u, layout_index=idx)
        except ValueError as e:
            attempts.append({"seed": u.get("seed"), "layout": idx, "blockers": [f"build: {e}"]})
            continue
        missing = intent_mod.check(d)
        if missing:  # a feature without a why is a generator bug, not a layout problem: refuse at once
            raise Rejected(getattr(h, "slug", str(h)), attempts + [{"blockers": [f"intent: {m}" for m in missing]}])
        rep = verify_dict(d, fast=fast)
        b = blockers(rep)
        attempts.append({"seed": u.get("seed"), "layout": idx, "blockers": b})
        if log:
            log(f"  seed {u.get('seed')} layout {idx}: {len(b)} blockers")
        if not b:
            res = GateResult(d, rep, attempts)
            res = lighten(h, u, idx, res, fast, log)
            res.spec.setdefault("generator", {})["gate"] = {"attempts": len(attempts), "fast": fast}
            return res
    raise Rejected(getattr(h, "slug", str(h)), attempts)
