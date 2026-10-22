"""One-at-a-time perturbations: numeric params +-5 / +-10 % (inside declared bounds), each variant switch flipped, each
catalog / model choice swapped to every alternative. Sampled to a time budget: params ranked by how many parts read
them, top N kept; +-10 % runs first and +-5 % only where +-10 % broke (to tell a tight param from a fragile one), unless
`steps="all"`."""

from __future__ import annotations

from dataclasses import dataclass, field

STEPS = (0.10, -0.10, 0.05, -0.05)
BIG = (0.10, -0.10)


@dataclass
class Job:
    id: str  # e.g. "CH_WALL+10%", "variant:esc_tray=on", "REVRON_MOTOR_VARIANT=step"
    target: str  # param / switch name the report names
    kind: str  # "param" | "variant" | "choice" | "flag"
    file: str = ""  # source file (absolute) to rewrite
    line: int = 0
    col: int = 0
    end_col: int = 0
    new_text: str = ""  # replacement for the literal span (param/choice/flag)
    append: str = ""  # line appended to `file` (variant)
    value: object = None
    base: object = None
    step: float = 0.0
    reads: list = field(default_factory=list)  # spec part ids whose build reads the target
    phase: int = 0  # 0 = first pass, 1 = only when the same target's first pass broke


def fmt_num(v: float, is_int: bool) -> str:
    return str(int(round(v))) if is_int else repr(round(v, 6))


def param_jobs(p, reads, steps=STEPS) -> list:
    out, seen = [], {p.value}
    for s in steps:
        v = p.value * (1 + s)
        if p.is_int:
            v = float(round(v))
        if p.bounds:
            lo, hi = sorted(p.bounds)
            v = min(max(v, lo), hi)
        if v in seen:  # zero, an int that rounds back, or clamped onto a value already tried
            continue
        seen.add(v)
        out.append(Job(f"{p.name}{s:+.0%}", p.name, "param", str(p.file), p.line, p.col, p.end_col, fmt_num(v, p.is_int),
                       value=v, base=p.value, step=s, reads=list(reads), phase=0 if abs(s) >= 0.1 or len(steps) == 2 else 1))
    return out


def switch_jobs(s, reads) -> list:
    out = []
    for alt in s.alternatives:
        if s.kind == "variant":
            out.append(Job(f"variant:{s.name}={'on' if alt else 'off'}", s.name, "variant", str(s.file),
                           append=f"\nset_variants(*([n for n in NAMES if VARIANTS[n] and n != {s.name!r}] + ([{s.name!r}] if {bool(alt)!r} else [])))\n",
                           value=alt, base=s.default, reads=list(reads)))
        elif s.kind == "choice":
            out.append(Job(f"{s.name}={alt}", s.name, "choice", str(s.file), s.line, s.col, s.end_col, repr(alt),
                           value=alt, base=s.default, reads=list(reads)))
        else:
            out.append(Job(f"{s.name}={alt}", s.name, "flag", str(s.file), s.line, s.col, s.end_col, repr(alt),
                           value=alt, base=s.default, reads=list(reads)))
    return out


def rank_params(params, usage) -> list:
    """(params, parts reading each) by descending reader count; params nothing reads are dropped."""
    scored = [(p, usage.parts_reading(p.symbol)) for p in params]
    scored = [x for x in scored if x[1]]
    order = {id(p): i for i, p in enumerate(params)}
    scored.sort(key=lambda x: (-len(x[1]), not x[0].master, order[id(x[0])]))
    return scored


def make_plan(disc, usage, top_n: int = 8, steps: str = "adaptive") -> tuple:
    """(jobs in run order, skipped params with their reader count). Switches first (few, and swaps matter most)."""
    jobs = []
    for s in disc.switches:
        jobs += switch_jobs(s, usage.parts_reading(s.symbol, s.kind == "variant"))
    ranked = rank_params(disc.params, usage)
    keep, skipped = ranked[:top_n], [(p.name, len(r)) for p, r in ranked[top_n:]]
    pj = []
    for p, r in keep:
        js = param_jobs(p, r, STEPS)
        if steps == "all":
            for j in js:
                j.phase = 0
        pj += js
    jobs += [j for j in pj if j.phase == 0] + [j for j in pj if j.phase == 1]
    return jobs, skipped
