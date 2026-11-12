"""Typed design settings: one named, documented, validated set of build choices for a robot generator.

A generator declares its settings once as a `Schema` of `Setting`s (name, type, default, allowed values, doc, legacy env
var). A `Design` is a validated set of values for one schema, loadable from a dict or a JSON file:

    schema = load_schema("robots/revron")              # robots/revron/src/revron/settings.py : SCHEMA
    d = schema.design({"drive.motor": "n10_300rpm_6v", "size.width": "10%"})
    with use(d):
        ...                                            # generator code reads value("REVRON_DRIVE_MOTOR", "<default>")

Reading a setting (`value(env, default)`, called by the generator where it used to call os.environ.get) resolves, in
order: the active design (`use`) if it sets that setting, then the legacy environment variable, then the default. So
the environment stays a backwards-compatible fallback: existing runners that export REVRON_* keep working unchanged.

Values are kept as the same strings the environment variables carry ("10%", "on", "battery_pad,esc_tray"), so the
generator code does not change with the source of a value; `Design` accepts JSON-native forms (a number for a size, a
bool for a flag, a list for a set) and normalises them.

Limits, stated plainly:
* A generator that reads its settings at import time (Revron does: module-level constants) only sees a design that is
  active WHILE ITS MODULES ARE IMPORTED. `fresh_import(package)` drops the package from sys.modules for the duration so
  it is imported again under the active design, and puts the previous modules back afterwards. That swap is
  process-global: it is serialised by a lock, but other threads importing the same package meanwhile are not safe.
* `use()` is a context variable: it does not reach child processes. Pass `Design.env()` to a subprocess, or use
  `use(design, env=True)` to also export the legacy variables (process-global) for the duration.
* An environment variable still applies to a setting the active design leaves unset (lowest priority, by design).

CLI:  python -m robot.design schema <robot dir | settings.py>            the settings schema as JSON
      python -m robot.design spec <robot dir | settings.py> <design.json> [-o spec.json]
"""
from __future__ import annotations

import contextlib
import contextvars
import difflib
import importlib.util
import json
import os
import re
import sys
import threading
from dataclasses import dataclass, field
from pathlib import Path

TYPES = {"choice": "one of `choices` (string)",
         "size": "a delta in mm (number or string: 4, \"-3.5\") or a percentage of the stock dimension (\"10%\", \"-20%\")",
         "flag": "true / false (also \"on\" / \"off\")",
         "set": "a list of names from `choices` (also a comma-separated string; \"all\" = every name)",
         "text": "any string"}
_SIZE = re.compile(r"[+-]?(\d+(\.\d*)?|\.\d+)%?")


class DesignError(ValueError):
    """An unknown setting or a value the setting does not allow."""


@dataclass(frozen=True)
class Setting:
    name: str  # dotted name, e.g. "drive.motor"
    type: str  # a key of TYPES
    default: str  # in the env-var string form
    doc: str = ""
    env: str | None = None  # legacy environment variable (fallback source, and the key generator code reads by)
    choices: tuple = ()

    def __post_init__(self):
        if self.type not in TYPES:
            raise DesignError(f"setting {self.name!r}: unknown type {self.type!r}; known: {sorted(TYPES)}")
        object.__setattr__(self, "choices", tuple(self.choices))
        object.__setattr__(self, "default", self.parse(self.default))

    def parse(self, v) -> str:
        """`v` (JSON-native or string form) as the canonical string; DesignError when the setting does not allow it."""
        def bad(why):
            return DesignError(f"setting {self.name!r}: bad value {v!r}: {why}")
        if self.type == "flag":
            if isinstance(v, bool):
                return "on" if v else "off"
            if v in ("on", "off"):
                return v
            raise bad("expected true / false or \"on\" / \"off\"")
        if self.type == "size":
            if isinstance(v, (int, float)) and not isinstance(v, bool):
                return repr(v)
            if isinstance(v, str) and _SIZE.fullmatch(v.strip()):
                return v.strip()
            raise bad("expected mm (4, \"-3.5\") or a percentage of the stock dimension (\"10%\")")
        if self.type == "set":
            names = [t.strip() for t in v.split(",")] if isinstance(v, str) else list(v) if isinstance(v, (list, tuple, set, frozenset)) else None
            if names is None or not all(isinstance(n, str) for n in names):
                raise bad("expected a list of names")
            names = [n for n in names if n]
            if names == ["all"]:
                return "all"
            unknown = [n for n in names if n not in self.choices]
            if unknown:
                raise bad(f"unknown {unknown}; allowed: {list(self.choices)} (or \"all\")")
            return ",".join(n for n in self.choices if n in names)
        if not isinstance(v, str):
            raise bad(f"expected a string, got {type(v).__name__}")
        if self.type == "choice" and v not in self.choices:
            near = difflib.get_close_matches(v, self.choices, 3)
            raise bad((f"did you mean {near}? " if near else "") + f"allowed: {list(self.choices)}")
        return v

    def native(self, s: str):
        """The canonical string as its JSON-native value (bool for a flag, list for a set)."""
        if self.type == "flag":
            return s == "on"
        if self.type == "set":
            return list(self.choices) if s == "all" else [t for t in s.split(",") if t]
        return s

    def to_dict(self) -> dict:
        d = dict(name=self.name, type=self.type, default=self.native(self.default))
        if self.choices:
            d["choices"] = list(self.choices)
        d.update(doc=self.doc, env=self.env)
        return d


class Schema:
    """The settings of one robot generator, in declaration order."""

    def __init__(self, robot: str, settings):
        self.robot = robot
        self.settings = tuple(settings)
        self.by_name = {s.name: s for s in self.settings}
        self.by_env = {s.env: s for s in self.settings if s.env}
        if len(self.by_name) != len(self.settings) or len(self.by_env) != sum(1 for s in self.settings if s.env):
            raise DesignError(f"schema {robot!r}: a setting name or env var is declared twice")

    def find(self, key: str) -> Setting:
        """The setting called `key` (its name, or its legacy env var); DesignError names the close matches."""
        s = self.by_name.get(key) or self.by_env.get(key)
        if s is None:
            near = difflib.get_close_matches(key, list(self.by_name) + list(self.by_env), 3)
            raise DesignError(f"unknown setting {key!r} for {self.robot}" + (f"; did you mean {near}?" if near else "") + f"; known: {list(self.by_name)}")
        return s

    def design(self, values=None, **more) -> "Design":
        """A Design from None, a Design of this schema, or a dict {setting name: value} (optionally under "settings")."""
        if isinstance(values, Design):
            if values.schema.robot != self.robot:
                raise DesignError(f"design is for {values.schema.robot!r}, not {self.robot!r}")
            return Design(self, {**values.values, **more}) if more else values
        if values is not None and not isinstance(values, dict):
            raise DesignError(f"a design is a JSON object {{setting: value}}, got {type(values).__name__}")
        return Design(self, {**(values or {}), **more})

    def load(self, path) -> "Design":
        """A Design from a JSON file."""
        return self.design(json.loads(Path(path).read_text()))

    def to_dict(self) -> dict:
        return dict(robot=self.robot,
                    format="a design is a JSON object {setting name: value}; a setting left out keeps its default (or the legacy env var when that is set)",
                    types=TYPES, settings=[s.to_dict() for s in self.settings])


@dataclass(frozen=True)
class Design:
    """Validated values for one Schema. `values` holds only the settings given, as canonical strings."""
    schema: Schema
    values: dict = field(default_factory=dict)

    def __post_init__(self):
        raw = self.values
        if not isinstance(raw, dict):
            raise DesignError(f"a design is a JSON object {{setting: value}}, got {type(raw).__name__}")
        if set(raw) <= {"robot", "settings"} and isinstance(raw.get("settings"), dict):
            if raw.get("robot", self.schema.robot) != self.schema.robot:
                raise DesignError(f"design is for {raw['robot']!r}, not {self.schema.robot!r}")
            raw = raw["settings"]
        out = {}
        for k, v in raw.items():
            s = self.schema.find(k)
            if s.name in out:
                raise DesignError(f"setting {s.name!r} is given twice (by name and by env var)")
            out[s.name] = s.parse(v)
        object.__setattr__(self, "values", out)

    def __getitem__(self, name: str) -> str:
        """The value this design gives the setting, else its default (the environment is not consulted)."""
        s = self.schema.find(name)
        return self.values.get(s.name, s.default)

    def env(self) -> dict:
        """{legacy env var: value} of the settings this design sets: what a subprocess needs to build the same design."""
        return {self.schema.by_name[n].env: v for n, v in self.values.items() if self.schema.by_name[n].env}

    def to_dict(self) -> dict:
        """JSON-native {setting: value} of the settings this design sets (round-trips through Schema.design)."""
        return {n: self.schema.by_name[n].native(v) for n, v in self.values.items()}

    def resolved(self) -> dict:
        """{setting: (canonical value, source)} for every setting, source = "design" | "env" | "default": what a build under this design reads."""
        out = {}
        for s in self.schema.settings:
            if s.name in self.values:
                out[s.name] = (self.values[s.name], "design")
            elif s.env and s.env in os.environ:
                out[s.name] = (os.environ[s.env], "env")
            else:
                out[s.name] = (s.default, "default")
        return out

    def __hash__(self):
        return hash((self.schema.robot, tuple(sorted(self.values.items()))))


_CURRENT: contextvars.ContextVar = contextvars.ContextVar("robot_design", default=None)
_IMPORT_LOCK = threading.RLock()


def current() -> Design | None:
    """The design made active by `use`, or None."""
    return _CURRENT.get()


@contextlib.contextmanager
def use(design: Design | None, env: bool = False):
    """Make `design` the active design for the block (None = no design: environment and defaults only).

    env=True also exports the design's legacy env vars for the block, so child processes build the same design
    (process-global; the previous values are put back)."""
    tok = _CURRENT.set(design)
    saved = {}
    try:
        if env and design is not None:
            for k, v in design.env().items():
                saved[k] = os.environ.get(k)
                os.environ[k] = v
        yield design
    finally:
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
        _CURRENT.reset(tok)


def value(env: str, default: str) -> str:
    """The setting whose legacy env var is `env`: the active design's value, else the env var, else `default`.

    A drop-in for os.environ.get(env, default) in generator code. `default` is the literal at the read site (the
    robustness runner edits it in a copy of the sources to try an alternative)."""
    d = _CURRENT.get()
    if d is not None:
        s = d.schema.by_env.get(env)
        if s is not None and s.name in d.values:
            return d.values[s.name]
    return os.environ.get(env, default)


@contextlib.contextmanager
def fresh_import(package: str, path=None):
    """Drop `package` (and its submodules) from sys.modules for the block, so it is imported again and its import-time
    settings are read under the design active now; afterwards the block's modules are dropped and the previous ones put
    back. `path` is put on sys.path for the block. Process-global, serialised by a lock (see the module docstring)."""
    def mine():
        return [k for k in sys.modules if k == package or k.startswith(package + ".")]
    with _IMPORT_LOCK:
        saved = {k: sys.modules.pop(k) for k in mine()}
        path = str(path) if path is not None else None
        added = path is not None and path not in sys.path
        if added:
            sys.path.insert(0, path)
        try:
            yield
        finally:
            for k in mine():
                del sys.modules[k]
            sys.modules.update(saved)
            if added and path in sys.path:
                sys.path.remove(path)


def settings_file(path) -> Path:
    """The settings module of a robot: `path` itself when it is a .py file, else <path>/src/<package>/settings.py."""
    p = Path(path)
    if p.is_file():
        return p
    found = sorted(p.glob("src/*/settings.py")) + sorted(p.glob("settings.py"))
    if len(found) != 1:
        raise DesignError(f"{p}: expected one settings.py (src/<package>/settings.py), found {[str(f) for f in found]}")
    return found[0]


def load_settings(path):
    """The settings module of a robot, loaded on its own (the generator package is not imported). It declares SCHEMA
    and may declare build(design) -> spec dict."""
    f = settings_file(path).resolve()
    name = "robot_design_settings_" + re.sub(r"\W", "_", str(f))
    if name in sys.modules:
        return sys.modules[name]
    spec = importlib.util.spec_from_file_location(name, f)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    try:
        spec.loader.exec_module(mod)
    except BaseException:
        del sys.modules[name]
        raise
    if not isinstance(getattr(mod, "SCHEMA", None), Schema):
        del sys.modules[name]
        raise DesignError(f"{f}: no SCHEMA (a robot.design.Schema)")
    return mod


def load_schema(path) -> Schema:
    return load_settings(path).SCHEMA


def build_spec(path, design=None) -> dict:
    """The spec dict of the robot at `path` built under `design` (None, a dict, a JSON file path or a Design), in this
    process and without touching the environment. Safe to call again with another design."""
    mod = load_settings(path)
    if isinstance(design, (str, Path)):
        design = mod.SCHEMA.load(design)
    if not hasattr(mod, "build"):
        raise DesignError(f"{settings_file(path)}: no build(design)")
    return mod.build(mod.SCHEMA.design(design))


def main(argv=None) -> int:
    import argparse
    ap = argparse.ArgumentParser(prog="python -m robot.design", description="Design settings of a robot generator.")
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("schema", help="print the settings schema as JSON")
    s.add_argument("robot", help="robot directory (robots/revron) or its settings.py")
    b = sub.add_parser("spec", help="build the spec of a design (JSON file) in this process")
    b.add_argument("robot")
    b.add_argument("design", help="design JSON file: {setting name: value}")
    b.add_argument("-o", "--out", help="write the spec here (default: stdout)")
    a = ap.parse_args(argv)
    try:
        if a.cmd == "schema":
            print(json.dumps(load_schema(a.robot).to_dict(), indent=1))
            return 0
        text = json.dumps(build_spec(a.robot, a.design), indent=1)
    except DesignError as e:
        print(f"design error: {e}", file=sys.stderr)
        return 2
    if a.out:
        Path(a.out).write_text(text)
    else:
        print(text)
    return 0


if __name__ == "__main__":
    from robot.design import main as _main   # the importable module, not this __main__ copy: settings files import its classes
    sys.exit(_main())
