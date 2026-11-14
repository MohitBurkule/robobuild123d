"""Named settings of the wiring package: data/defaults.json, overridden per robot by the spec's `harness.settings`."""

from __future__ import annotations

import copy
import json
from functools import lru_cache
from pathlib import Path

DATA = Path(__file__).resolve().parent / "data"
SPEC_KEY = "harness"          # spec.raw["harness"]: {"settings": {...}, "terminals": {...}, "nets": [...], "auto": bool}


@lru_cache(maxsize=None)
def load_json(name: str):
    return json.loads((DATA / name).read_text())


def defaults() -> dict:
    d = copy.deepcopy(load_json("defaults.json"))
    d.pop("_doc", None)
    return d


def merge(base: dict, over: dict | None) -> dict:
    """`over` laid on `base`, dict by dict; unknown keys are kept (a spec may carry its own notes)."""
    out = dict(base)
    for k, v in (over or {}).items():
        out[k] = merge(out[k], v) if isinstance(v, dict) and isinstance(out.get(k), dict) else v
    return out


def section(spec) -> dict:
    """The spec's `harness` object ({} when absent)."""
    raw = getattr(spec, "raw", None) or {}
    return dict(raw.get(SPEC_KEY) or {})


def for_spec(spec=None) -> dict:
    return merge(defaults(), section(spec).get("settings") if spec is not None else None)
