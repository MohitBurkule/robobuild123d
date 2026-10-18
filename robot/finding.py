"""Check results. JSON field names match the Rust crate's report.json."""

from __future__ import annotations

from dataclasses import asdict, dataclass, field

BLOCKER, WARNING, INFO = "blocker", "warning", "info"


@dataclass
class Finding:
    id: str
    group: str
    severity: str
    passed: bool
    title: str
    message: str
    expected: str | None = None
    actual: str | None = None
    parts: list = field(default_factory=list)
    at: list | None = None
    fix_hint: str | None = None

    # Builder-style helpers, like the Rust API.
    def expect(self, expected, actual):
        self.expected, self.actual = str(expected), str(actual)
        return self

    def on(self, *parts):
        self.parts = [str(p) for p in parts]
        return self

    def here(self, p):
        if p is not None:
            self.at = [float(p[0]), float(p[1]), float(p[2])]
        return self

    def fix(self, hint):
        self.fix_hint = hint
        return self

    def to_dict(self):
        return {"id": self.id, "group": self.group, "severity": self.severity, "pass": self.passed, "title": self.title,
                "message": self.message, "expected": self.expected, "actual": self.actual, "parts": self.parts, "at": self.at,
                "fix": self.fix_hint}


def ok(id, group, title, message) -> Finding:
    return Finding(id, group, INFO, True, title, message)


def fail(id, group, severity, title, message) -> Finding:
    return Finding(id, group, severity, False, title, message)


def note(id, group, title, message) -> Finding:
    return Finding(id, group, INFO, True, title, message)


@dataclass
class MassLine:
    id: str
    kind: str
    grams: float
    tol_g: float
    source: str  # scale, slicer, catalog, computed, declared, wire, fastener


@dataclass
class Route:
    id: str
    awg: float
    kind: str
    od_mm: float
    length_mm: float
    points: list


@dataclass
class AssemblyStep:
    order: int
    id: str
    dir: list
    travel_mm: float


@dataclass
class Report:
    name: str = ""
    profile: str = ""
    ok: bool = False
    summary: dict = field(default_factory=dict)
    findings: list = field(default_factory=list)
    metrics: dict = field(default_factory=dict)
    mass: list = field(default_factory=list)
    bench_checklist: list = field(default_factory=list)
    routes: list = field(default_factory=list)
    assembly: list = field(default_factory=list)
    not_checked: list = field(default_factory=list)
    checks_revision: int = 0
    engine: str = "build123d"
    timings_s: dict = field(default_factory=dict)

    def finish(self):
        b = sum(1 for f in self.findings if not f.passed and f.severity == BLOCKER)
        w = sum(1 for f in self.findings if not f.passed and f.severity == WARNING)
        p = sum(1 for f in self.findings if f.passed)
        self.summary = {"blockers": b, "warnings": w, "passed": p, "total": len(self.findings)}
        self.ok = b == 0

    def failed(self, fid) -> bool:
        return any(not f.passed and f.id == fid for f in self.findings)

    def get(self, fid):
        return next((f for f in self.findings if f.id == fid), None)

    def to_dict(self):
        return {
            "name": self.name, "profile": self.profile, "ok": self.ok, "summary": self.summary,
            "findings": [f.to_dict() for f in self.findings], "metrics": dict(sorted(self.metrics.items())),
            "mass": [asdict(m) for m in self.mass], "bench_checklist": self.bench_checklist,
            "routes": [asdict(r) for r in self.routes], "assembly": [asdict(a) for a in self.assembly],
            "not_checked": self.not_checked, "checks_revision": self.checks_revision, "engine": self.engine,
            "timings_s": self.timings_s,
        }
