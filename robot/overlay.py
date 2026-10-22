"""Declarative spec overlays: change a robot through settings, not code.

An overlay is a list of primitive ops applied to a spec dict (spec.json) before it is loaded. `Spec()` applies the
spec's own `overlay` key, so a variant robot is a spec plus an overlay; the change-hypothesis generator
(robot/gen/changes.py) and the robust runner use the same ops.

Ops (each a dict with "op"):
  set      {select, field, value}     set a (dotted) field on every match; value null deletes it
  catalog  {select, to}               swap the COTS entry: sets `catalog`, drops `shape`/`model`, and re-points
                                      wire ends on a port the new entry does not have (same port index)
  wheel    {select, to}               swap a wheel for a catalog wheel (which carries its own hub): the model hub
                                      the tyre sits on (`tyre_of`) is removed and the catalog wheel is re-seated on
                                      the hub's shaft / axle frame (hub parent, composed pose, hub joint); the hub's
                                      connections (to the motor shaft or axle) move to the wheel
  remove   {select, cascade=true}     drop the matches; cascade also drops connections / fasteners / wires /
                                      allow_overlap entries that name a removed part
  add      {part, anchor?}            add a part; `anchor` names an entry of the robot's anchors (hooks file)
                                      whose at / rot / parent fill the fields the part leaves out
  hook     {name, value}              a robot-declared setting, expanded from the robot's hooks file (see below)

`select` matches on `in` (list key, default "parts") and any of: id (str, list or glob with *), kind, catalog,
role, and `where` {field: value}. A robot declares its settings hooks in `hooks.json` beside spec.json (or under the
spec's `hooks` key):

  {"anchors": {"rear_deck": {"at": [x, y, z], "rot": [rx, ry, rz], "parent": "tub"}},
   "hooks":   {"drive.driven_wheels": {"values": {"4WD": [], "2WD": [<ops>]}, "default": "4WD"},
               "weapon.motor_variant": {"env": "REVRON_MOTOR_VARIANT", "values": ["datasheet", "step"]}},
   "owners":  {"A": ["tub*.py"], ...}}

A hook value that maps to ops is pure overlay; an `env` / `variant` hook is a build-time setting the caller applies
when it regenerates the spec (robust runner: a choice / variant edit). An undeclared hook raises `MissingHook`.
"""

from __future__ import annotations

import copy
import fnmatch
import json
from pathlib import Path

LISTS = ("parts", "fasteners", "connections", "wires", "allow_overlap")


class MissingHook(KeyError):
    """The robot declares no settings hook that expresses this change."""

    def __init__(self, name, why=""):
        super().__init__(name)
        self.name, self.why = name, why

    def __str__(self):
        return f"missing hook `{self.name}`" + (f": {self.why}" if self.why else "")


def load_hooks(raw: dict | None = None, base_dir=None) -> dict:
    """The robot's hooks: spec `hooks` key merged over `<spec dir>/hooks.json`."""
    out = {"anchors": {}, "hooks": {}, "owners": {}, "sizes": {}}
    if base_dir is not None:
        f = Path(base_dir) / "hooks.json"
        if f.exists():
            d = json.loads(f.read_text())
            for k in out:
                out[k].update(d.get(k) or {})
    for k in out:
        out[k].update(((raw or {}).get("hooks") or {}).get(k) or {})
    return out


def _match_val(v, want) -> bool:
    if isinstance(want, (list, tuple)):
        return any(_match_val(v, w) for w in want)
    if isinstance(want, str) and isinstance(v, str) and "*" in want:
        return fnmatch.fnmatchcase(v, want)
    return v == want


def matches(item: dict, sel: dict) -> bool:
    for k in ("id", "kind", "catalog", "role"):
        if k in sel and not _match_val(item.get(k), sel[k]):
            return False
    for k, want in (sel.get("where") or {}).items():
        if not _match_val(_get(item, k), want):
            return False
    return True


def select(raw: dict, sel: dict) -> list:
    return [x for x in raw.get(sel.get("in", "parts")) or [] if isinstance(x, dict) and matches(x, sel)]


def _get(d, path):
    for k in str(path).split("."):
        if not isinstance(d, dict):
            return None
        d = d.get(k)
    return d


def _set(d, path, value):
    ks = str(path).split(".")
    for k in ks[:-1]:
        d = d.setdefault(k, {})
    if value is None:
        d.pop(ks[-1], None)
    else:
        d[ks[-1]] = copy.deepcopy(value)


def _names_part(entry: dict, ids: set) -> bool:
    for k in ("a", "b", "with", "part", "parent"):
        v = entry.get(k)
        if isinstance(v, str) and v.split(".")[0] in ids:
            return True
    for k in ("from", "to"):
        v = entry.get(k)
        if isinstance(v, str) and v.split(".")[0] in ids:
            return True
    for k in ("through", "parts"):
        v = entry.get(k)
        if isinstance(v, list) and any(isinstance(x, str) and x in ids for x in v):
            return True
    return False


def _ports(cid):
    from . import catalog

    e = catalog.find(cid) if cid else None
    return list((e.ports or {}) if e else [])


def _catalog_swap(raw, op):
    hits = select(raw, op["select"])
    if not hits:
        raise ValueError(f"catalog: nothing matches {op['select']}")
    for p in hits:
        old = _ports(p.get("catalog"))
        new = _ports(op["to"])
        p["catalog"] = op["to"]
        for k in ("shape", "model", "params"):
            p.pop(k, None)
        remap = {o: new[i] for i, o in enumerate(old) if o not in new and i < len(new)}
        for w in raw.get("wires") or []:
            for end in ("from", "to"):
                v = w.get(end)
                if isinstance(v, str) and "." in v:
                    pid, port = v.split(".", 1)
                    if pid == p["id"] and port in remap:
                        w[end] = f"{pid}.{remap[port]}"
                        if w.get("connector") == port:
                            w["connector"] = remap[port]


def _compose(a_at, a_rot, b_at, b_rot) -> tuple:
    """(at, rot) of pose b given in frame a, expressed in a's parent frame (R = Rz Ry Rx, degrees)."""
    from scipy.spatial.transform import Rotation

    from . import xform

    M = xform.pose(a_at or [0, 0, 0], a_rot or [0, 0, 0]) @ xform.pose(b_at or [0, 0, 0], b_rot or [0, 0, 0])
    rz, ry, rx = Rotation.from_matrix(M[:3, :3]).as_euler("ZYX", degrees=True)
    r = lambda v: round(float(v), 6) + 0.0
    return [r(v) for v in M[:3, 3]], [r(rx), r(ry), r(rz)]


def _wheel_swap(raw, op):
    hits = select(raw, op["select"])
    if not hits:
        raise ValueError(f"wheel: nothing matches {op['select']}")
    parts = {p["id"]: p for p in raw.get("parts") or []}
    gone = set()
    for w in hits:
        hub = parts.get(w.get("tyre_of") or (w.get("parent") if parts.get(w.get("parent"), {}).get("kind") in ("pulley", "hub") else None))
        for k in ("shape", "model", "params", "tyre_of", "stock", "label"):
            w.pop(k, None)
        w["catalog"] = op["to"]
        if hub is None:
            continue
        w["at"], w["rot"] = _compose(hub.get("at"), hub.get("rot"), w.get("at"), w.get("rot"))
        if hub.get("parent"):
            w["parent"] = hub["parent"]
        else:
            w.pop("parent", None)
        for k in ("joint", "rotates_with"):
            if hub.get(k) is not None:
                w[k] = copy.deepcopy(hub[k])
        hid, wid = hub["id"], w["id"]
        conns = []
        for c in raw.get("connections") or []:
            ends = {c.get("a"), c.get("b")}
            if ends == {hid, wid}:
                continue  # tyre on hub: gone with the hub
            if hid in ends:
                c = dict(c, **{k: wid for k in ("a", "b") if c.get(k) == hid})
                c["reason"] = f"[wheel swap] catalog wheel hub takes over: {c.get('reason', '')}"
                c.pop("interference_mm", None)
            conns.append(c)
        raw["connections"] = conns
        for p in raw.get("parts") or []:
            if p.get("parent") == hid and p is not w:
                p["at"], p["rot"] = _compose(hub.get("at"), hub.get("rot"), p.get("at"), p.get("rot"))
                p["parent"] = hub.get("parent")
        gone.add(hid)
    if gone:
        raw["parts"] = [p for p in raw["parts"] if p["id"] not in gone]
        for lk in LISTS[1:]:
            if raw.get(lk):
                raw[lk] = [e for e in raw[lk] if not (isinstance(e, dict) and _names_part(e, gone))]


def expand(op: dict, hooks: dict) -> list:
    """A `hook` op as primitive ops (raises MissingHook); other ops unchanged."""
    if op.get("op") != "hook":
        return [op]
    h = (hooks.get("hooks") or {}).get(op["name"])
    if not h:
        raise MissingHook(op["name"], op.get("why", ""))
    vals = h.get("values")
    if isinstance(vals, dict):
        if op["value"] not in vals:
            raise MissingHook(f"{op['name']}={op['value']}", f"declared values: {sorted(vals)}")
        out = []
        for o in vals[op["value"]]:
            out += expand(o, hooks)
        return out
    if h.get("env") or h.get("variant"):
        if vals is not None and op["value"] not in vals:
            raise MissingHook(f"{op['name']}={op['value']}", f"declared values: {vals}")
        return [dict(op="build_setting", name=op["name"], env=h.get("env"), variant=h.get("variant"), value=op["value"])]
    raise MissingHook(op["name"], "hook declares no values")


def apply(raw: dict, ops: list, hooks: dict | None = None, base_dir=None) -> dict:
    """A new spec dict with `ops` applied. `build_setting` ops (env / variant hooks) are skipped here: they change the
    generated spec, so the caller applies them before generation."""
    raw = copy.deepcopy(raw)
    raw.pop("overlay", None)
    hooks = hooks if hooks is not None else load_hooks(raw, base_dir)
    for op0 in ops or []:
        for op in expand(op0, hooks):
            kind = op.get("op")
            if kind == "set":
                hits = select(raw, op["select"])
                if not hits:
                    raise ValueError(f"set: nothing matches {op['select']}")
                for x in hits:
                    _set(x, op["field"], op.get("value"))
            elif kind == "catalog":
                _catalog_swap(raw, op)
            elif kind == "wheel":
                _wheel_swap(raw, op)
            elif kind == "remove":
                key = op["select"].get("in", "parts")
                gone = select(raw, op["select"])
                raw[key] = [x for x in raw.get(key) or [] if x not in gone]
                if key == "parts" and op.get("cascade", True):
                    ids = {p["id"] for p in gone}
                    for lk in LISTS[1:]:
                        if raw.get(lk):
                            raw[lk] = [e for e in raw[lk] if not (isinstance(e, dict) and _names_part(e, ids))]
            elif kind == "add":
                part = copy.deepcopy(op["part"])
                if op.get("anchor"):
                    a = (hooks.get("anchors") or {}).get(op["anchor"])
                    if a is None:
                        raise MissingHook(f"anchor:{op['anchor']}", "no such named location")
                    for k in ("at", "rot", "parent"):
                        if k in a:
                            part.setdefault(k, copy.deepcopy(a[k]))
                if any(p.get("id") == part["id"] for p in raw.get("parts") or []):
                    raise ValueError(f"add: part `{part['id']}` exists")
                raw.setdefault("parts", []).append(part)
            elif kind == "build_setting":
                continue
            else:
                raise ValueError(f"unknown overlay op {kind!r}")
    return raw


def build_settings(ops: list, hooks: dict) -> list:
    """The env / variant settings among `ops` (after hook expansion)."""
    out = []
    for op0 in ops or []:
        out += [o for o in expand(op0, hooks) if o.get("op") == "build_setting"]
    return out
