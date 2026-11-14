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
    kind: str = "design"  # "design" | "parity" (compares with the reference); set by the pipeline from checks/registry.py

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
                "fix": self.fix_hint, "kind": self.kind}


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
    gate: str = "design"  # "design": ok = no design blocker; "combined": ok = no blocker of any kind (the old rule)
    tier: str | None = None  # inner | full | nightly, None when the run was not tiered (library call, --only)
    design: dict = field(default_factory=dict)  # counts of the design findings, and their ok
    parity: dict = field(default_factory=dict)  # counts and score of the parity findings (never gating unless combined)
    groups: dict = field(default_factory=dict)  # group -> {kind, tier, time_s, how, blockers, warnings, passed}
    not_run: list = field(default_factory=list)  # [{group, kind, tier, reason}] registered groups this run skipped

    def finish(self, combined=None):
        """Count and decide `ok`. The gate is the DESIGN findings; parity findings (kind "parity": comparisons with a
        reference design) are scored in `parity` and never flip `ok`, unless the gate is "combined" (the old rule:
        every blocker counts)."""
        if combined is not None:
            self.gate = "combined" if combined else "design"

        def count(fs):
            return {"blockers": sum(1 for f in fs if not f.passed and f.severity == BLOCKER),
                    "warnings": sum(1 for f in fs if not f.passed and f.severity == WARNING),
                    "passed": sum(1 for f in fs if f.passed), "total": len(fs)}

        par = [f for f in self.findings if getattr(f, "kind", "design") == "parity"]
        des = [f for f in self.findings if getattr(f, "kind", "design") != "parity"]
        self.design = count(des)
        self.design["ok"] = self.design["blockers"] == 0
        pc = count(par)
        judged = pc["total"]
        gs = [g for g in self.groups.values() if g.get("kind") == "parity"]
        self.parity = {**pc, "gating": self.gate == "combined", "run": bool(par or gs),
                       "score": round(pc["passed"] / judged, 3) if judged else None,
                       "groups_total": len(gs), "groups_clean": sum(1 for g in gs if not g.get("blockers")),
                       "failing_ids": sorted({f.id for f in par if not f.passed and f.severity == BLOCKER})}
        self.summary = count(self.findings if self.gate == "combined" else des)
        self.summary["parity_blockers"] = pc["blockers"]
        self.ok = self.summary["blockers"] == 0

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
            "timings_s": self.timings_s, "gate": self.gate, "tier": self.tier, "design": self.design,
            "parity": self.parity, "groups": self.groups, "not_run": self.not_run,
        }
