"""Incremental verify: `python3 -m robot verify spec.json --changed` reruns only the check groups whose inputs changed.

WHY: a full verify of a real robot takes minutes, so after moving one bracket people skipped verifying, or ran
`--only` on the group they thought mattered and missed the one that broke. This runner records, for every check group,
which parts' GEOMETRY it actually read (dynamic dependency tracking, like a build system) and reuses the group's
findings when nothing it depends on changed.

Correctness argument. A group's inputs are split in two:
  * the base: all code, the spec with each part's geometry fields (shape, model, params, at, rot) removed, the
    options, load errors, and every context field written by earlier groups (pickled). Any change -> rerun.
  * per-part geometry: a part's signature = geometry key + its geometry fields. While a group runs, every read of
    those (Part.at/rot/shape/model/params, RPart.geom/shape, any Body geometry/placement accessor, raw spec `parts`
    access, Spec.to_dict) records the part as a dependency.
Given an identical base, the group's control flow can only differ if a value it read differs, and every value it read
is either in the base or in a recorded part signature. So equal base + equal recorded signatures => same findings.
Bulk access (raw `parts`, to_dict) conservatively records every part. Lazily cached context (`ctx._*`) is dropped
before each group so no group can read geometry another group computed.

`verify_incremental(spec, opts)` returns (Report, stats) where stats = {"rerun": [...], "reused": [...]}.
A full run (`robot verify` without --changed) never uses this.
"""

from __future__ import annotations

import importlib
import json
import os
import pickle
import time
import traceback

from .. import cache, world as world_mod
from ..finding import BLOCKER, WARNING, Report, fail

GEOM_FIELDS = ("shape", "model", "params", "at", "rot")
BODY_ATTRS = frozenset({"geom", "M", "mesh", "manifold", "aabb", "center", "inside", "distance", "sdf", "surface",
                        "moved", "placed", "_mesh", "_man", "_surf"})
RPART_ATTRS = frozenset({"geom", "shape"})
PART_ATTRS = frozenset(GEOM_FIELDS + ("__dict__", "to_dict"))
KIND = "incr"

_rec: set | None = None  # part ids read by the running group
_all_ids: tuple = ()


def _note(pid):
    if _rec is not None and pid is not None:
        _rec.add(pid)


def _note_all():
    if _rec is not None:
        _rec.update(_all_ids)


class _TBody(world_mod.Body):
    def __getattribute__(self, name):
        if name in BODY_ATTRS:
            d = object.__getattribute__(self, "__dict__")
            if d.get("part_idx") is not None:
                _note(d.get("id"))
        return object.__getattribute__(self, name)


class _TRPart(world_mod.RPart):
    def __getattribute__(self, name):
        if name in RPART_ATTRS:
            _note(object.__getattribute__(self, "__dict__")["part"].__dict__.get("id"))
        return object.__getattribute__(self, name)


def _tpart_cls(base):
    class _TPart(base):
        def __getattribute__(self, name):
            if name in PART_ATTRS:
                _note(object.__getattribute__(self, "__dict__").get("id"))
            return object.__getattribute__(self, name)
    return _TPart


class _TRaw(dict):
    """Spec raw dict: reading `parts` (or iterating everything) counts as reading every part's geometry."""

    def __getitem__(self, k):
        if k == "parts":
            _note_all()
        return dict.__getitem__(self, k)

    def get(self, k, d=None):
        if k == "parts":
            _note_all()
        return dict.get(self, k, d)

    def items(self):
        _note_all()
        return dict.items(self)

    def values(self):
        _note_all()
        return dict.values(self)

    def copy(self):
        _note_all()
        return dict.copy(self)

    def __iter__(self):
        _note_all()
        return dict.__iter__(self)


class _Tracking:
    """Context manager installing the tracking classes on the live objects of one run (and removing them)."""

    def __init__(self, ctx):
        self.ctx = ctx

    def __enter__(self):
        r, w = self.ctx.r, self.ctx.world
        self.saved = []
        for b in w.bodies:
            if type(b) is world_mod.Body:
                self.saved.append((b, world_mod.Body))
                b.__class__ = _TBody
        for rp in r.parts:
            if type(rp) is world_mod.RPart:
                self.saved.append((rp, world_mod.RPart))
                rp.__class__ = _TRPart
            p = rp.part
            cls = type(p)
            if not cls.__name__ == "_TPart":
                self.saved.append((p, cls))
                p.__class__ = _tpart_cls(cls)
        self.raw = r.spec.raw
        r.spec.raw = _TRaw(self.raw or {})
        return self

    def __exit__(self, *exc):
        for o, cls in self.saved:
            o.__class__ = cls
        # bodies a group appended or new worlds keep plain classes; restore raw
        self.ctx.r.spec.raw = self.raw
        return False


def _strip(raw):
    d = json.loads(json.dumps(raw, default=str))
    for p in d.get("parts") or []:
        if isinstance(p, dict):
            for k in GEOM_FIELDS:
                p.pop(k, None)
    return d


def part_sigs(r) -> dict:
    out = {}
    for rp in r.parts:
        p = rp.part
        fields = {k: getattr(p, k, None) for k in GEOM_FIELDS}
        out[p.id] = cache.h(rp.geom.key, json.dumps(fields, sort_keys=True, default=str))
    return out


def _ctx_bytes(ctx):
    from ..checks import _SKIP

    out = {}
    for k, v in vars(ctx).items():
        if k in _SKIP or k.startswith("_"):
            continue
        try:
            out[k] = pickle.dumps(v, protocol=pickle.HIGHEST_PROTOCOL)
        except Exception:  # noqa: BLE001
            out[k] = None
    return out


def verify_incremental(spec, opts=None):
    """Same pipeline and result as robot.checks.verify, with per-group reuse keyed on recorded dependencies."""
    global _rec, _all_ids
    from .. import checks
    from ..checks import GROUPS, Ctx, Options, not_checked, validity

    opts = opts or Options()
    r = world_mod.resolve(spec, fast=opts.fast)
    rep = Report(name=r.spec.name, profile=r.profile.name)
    findings, stats = [], {"rerun": [], "reused": []}
    t0 = time.time()
    valid = validity.run(r, findings)
    rep.timings_s["validity"] = round(time.time() - t0, 3)
    ctx = None
    sigs = part_sigs(r)
    _all_ids = tuple(sigs)
    base = cache.h(cache.code_hash(), json.dumps(_strip(r.spec.raw), sort_keys=True, default=str), cache.referenced_hash(r.spec.raw, r.spec.base_dir),
                   r.load_errors, json.dumps(dict(vars(opts)), sort_keys=True, default=str), r.fast,
                   [rp.part.id for rp in r.parts])
    if valid:
        ctx = Ctx(r, world_mod.World.start(r), opts)
        from ..checks import effective_only
        _only = effective_only(r.spec, opts.only)
        for name, deep_only in GROUPS:
            if deep_only and not opts.deep:
                continue
            if _only and name not in _only:
                continue
            t0 = time.time()
            try:
                mod = importlib.import_module(f"robot.checks.{name}")
            except ModuleNotFoundError:
                findings.append(fail("checks.missing", "checks", WARNING, "Check group not available",
                                     f"The `{name}` checks are not in this build; nothing in that group was judged."))
                ctx.not_checked.append(f"Check group `{name}` is not available in this build")
                continue
            for k in [k for k in vars(ctx) if k.startswith("_")]:
                delattr(ctx, k)
            before = _ctx_bytes(ctx)
            gkey = cache.h("incr", name, base, sorted((k, v) for k, v in before.items()))
            hit = cache.get(KIND, gkey)
            if not cache.is_missing(hit) and all(sigs.get(p) == s for p, s in hit[0].items()):
                _, found, delta = hit
                findings.extend(found)
                for k, v in delta.items():
                    setattr(ctx, k, v)
                stats["reused"].append(name)
                rep.timings_s[name] = round(time.time() - t0, 3)
                continue
            _rec = set()
            try:
                with _Tracking(ctx):
                    found = mod.run(ctx)
                deps = {p: sigs[p] for p in _rec if p in sigs}
                findings.extend(found)
                after = _ctx_bytes(ctx)
                delta = {k: getattr(ctx, k) for k, v in after.items() if before.get(k) != v}
                if all(after[k] is not None for k in delta):
                    cache.put(KIND, gkey, (deps, found, delta))
                stats["rerun"].append(name)
            except Exception as e:  # noqa: BLE001 - fail closed, as the full pipeline does
                findings.append(fail("checks.crashed", "checks", BLOCKER, "A check crashed",
                                     f"`{name}` raised {type(e).__name__}: {e}. Its verdicts are unknown.")
                                .fix("Report this; the spec may hold geometry the check cannot handle."))
                ctx.not_checked.append(f"Check group `{name}` crashed: {type(e).__name__}")
                stats["rerun"].append(name)
                if os.environ.get("ROBOT_DEBUG"):
                    traceback.print_exc()
            finally:
                _rec = None
            rep.timings_s[name] = round(time.time() - t0, 3)
        findings.extend(validity.claims(ctx))
        rep.routes = ctx.routes
        rep.assembly = ctx.assembly
        rep.mass = getattr(ctx, "mass_lines", [])
    rep.findings = findings
    from ..checks import waiver as _waiver
    waivers = _waiver.apply(r.spec, findings)
    rep.metrics = ctx.metrics if ctx else {}
    rep.checks_revision = checks.CHECKS_REVISION
    rep.not_checked = not_checked(r, opts) + (ctx.not_checked if ctx else ["Every geometric check: the spec is not valid"])
    rep.bench_checklist = []
    rep.finish()
    if waivers:
        rep.summary["waivers"] = waivers
    return rep, stats


def cli(a):
    import sys
    from pathlib import Path

    from .. import spec as spec_mod
    from ..cli import opts_from, print_report

    try:
        s = spec_mod.load(a.spec)
    except ValueError as e:
        print(f"error: {e}", file=sys.stderr)
        return 1
    if not cache.enabled():
        print("note: cache disabled, --changed reruns everything", file=sys.stderr)
    rep, st = verify_incremental(s, opts_from(a))
    print(f"incremental: reran {len(st['rerun'])} groups ({', '.join(st['rerun']) or 'none'}); reused {len(st['reused'])}")
    print_report(rep, a.full)
    if a.json:
        Path(a.json).write_text(json.dumps(rep.to_dict(), indent=2))
    return 0 if rep.ok else 2
