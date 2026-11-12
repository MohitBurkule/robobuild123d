"""Tune "mass lever" masters (wall/armour/disc thickness, infill, lightening) within bounds to hit the mass limit.

Generic: knows nothing of CAD. Caller gives `mass_fn(values: dict) -> grams` (e.g. build design + sum part masses,
see revron_levers.mass_fn). Levers are spent in priority order: lever 1 swept fully (bisection) before lever 2 moves.
Mass assumed monotone non-decreasing in each lever (thicker = heavier). UNTESTED.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Callable


class MassInfeasible(ValueError):
    """No lever setting inside the bounds reaches the target band."""


@dataclass(frozen=True)
class Lever:
    name: str            # setting name (Design key) or master name the mass_fn understands
    lo: float
    hi: float
    default: float
    priority: int = 0    # lower = spent first
    step: float = 0.0    # manufacturing quantum (e.g. 0.4 mm nozzle line, 0.5 mm sheet); 0 = continuous
    doc: str = ""

    def __post_init__(self):
        if not self.lo <= self.default <= self.hi:
            raise ValueError(f"lever {self.name}: default {self.default} outside [{self.lo}, {self.hi}]")

    def snap(self, v: float, down: bool = True) -> float:
        """Snap to step; rounding down never adds mass."""
        if self.step <= 0:
            return min(max(v, self.lo), self.hi)
        n = (v - self.lo) / self.step
        n = int(n) if down else int(-(-n // 1))
        return min(max(self.lo + n * self.step, self.lo), self.hi)


@dataclass
class SolveResult:
    target_g: float
    start_g: float
    final_g: float
    values: dict
    changed: dict = field(default_factory=dict)   # name -> (old, new)
    evals: int = 0

    @property
    def margin_g(self) -> float:
        return self.target_g - self.final_g

    def report(self) -> str:
        lines = [f"mass {self.start_g:.2f} g -> {self.final_g:.2f} g (limit {self.target_g:.2f}, margin {self.margin_g:+.2f} g, {self.evals} evals)"]
        lines += [f"  {n}: {a:g} -> {b:g}" for n, (a, b) in self.changed.items()] or ["  no lever moved"]
        return "\n".join(lines)


def _bisect(f, lo, hi, target, tol, max_iter):
    """Largest x in [lo, hi] with f(x) <= target, f monotone up. Returns (x, f(x), evals)."""
    flo, n = f(lo), 1
    if flo > target:
        return lo, flo, n
    fhi = f(hi); n += 1
    if fhi <= target:
        return hi, fhi, n
    best, fbest = lo, flo
    for _ in range(max_iter):
        if hi - lo <= tol:
            break
        mid = 0.5 * (lo + hi)
        fm = f(mid); n += 1
        if fm <= target:
            lo, best, fbest = mid, mid, fm
        else:
            hi = mid
    return best, fbest, n


def solve_mass(mass_fn: Callable[[dict], float], levers: list[Lever], target_g: float = 150.0,
               band_g: float = 0.5, start: dict | None = None, tol: float = 0.01, max_iter: int = 30) -> SolveResult:
    """Move levers (priority order) so target-band <= mass <= target. Over-limit: shrink levers until under.
    Under by more than band: grow levers (spend spare mass on armour). Raises MassInfeasible."""
    order = sorted(levers, key=lambda l: l.priority)
    vals = {l.name: (start or {}).get(l.name, l.default) for l in order}
    evals = 0

    def m(v):
        nonlocal evals
        evals += 1
        return float(mass_fn(v))

    start_g = cur = m(dict(vals))
    for lev in order:
        if target_g - band_g <= cur <= target_g:
            break
        def f(x, lev=lev):
            return m({**vals, lev.name: x})
        x, fx, _ = _bisect(f, lev.lo, lev.hi, target_g, tol, max_iter)
        x = lev.snap(x, down=True)
        vals[lev.name] = x
        cur = m(dict(vals))
    if cur > target_g:
        mins = {l.name: l.lo for l in order}
        raise MassInfeasible(f"{cur:.2f} g > {target_g} g with levers at {vals}; floor at all-min = {m(mins):.2f} g. "
                             f"Need lighter parts or more levers.")
    changed = {n: ((start or {}).get(n, l.default), vals[n]) for l in order for n in [l.name]
               if vals[n] != (start or {}).get(n, l.default)}
    return SolveResult(target_g, start_g, cur, vals, changed, evals)
