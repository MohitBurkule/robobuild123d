# robot/ refactor plan

## Problems (measured)
- Oversized: checks/architecture.py 1909, kinematics.py 1555, process.py 821, archetype.py 786, combat.py 758, electrical.py 713 lines (~14.3k total).
- Duplicated helpers: vector unit/perp (4 copies), floor detection (4), weapon lookup (6), spin axis (4), ray casting, part lookup, contact patches (4), motion/rotor groups (3), rule runners (3).
- Private cross-imports: architecture→strength._host, assembly→interference._corners, electrical→archetype._ancestors; `_physics` grab-bag.
- Knowledge in code (RULES lists, thresholds in lambdas); ~60 hand-written `not_checked` strings.

## Target layout
```
robot/core      spec model (pydantic), Finding/Result, units, xform
robot/io        JSON schema, load/validate, report writers
robot/geometry  shapes, geom, world, measure, vec, raycast, section, sampling
robot/analysis  pure cached services: floor, parts, weapons, motion, contacts, perimeter, sweep, mass, sections, electrical
robot/rules     YAML: rule id, severity, title, fix, thresholds, applies_to; materials/bearings/motors data
robot/checks    registry.py (@check), context.py, <domain>/ small check functions (<300 lines/file)
robot/cli, render, export
```
Layering enforced by import-linter: core ← geometry ← analysis ← checks ← cli/export. No cross-domain check imports, no private imports.

Check contract: `@check(rule=..., needs=(...), applies=...)` returns `Result` PASS/FAIL/NA/UNMEASURED(reason, missing) with value, limit, unit. Runner maps to Finding, catches crashes, derives NOT CHECKED (rules without function + UNMEASURED). Services declare `provides`; registry validates `needs` at import.

## Testing
- Unit tests per analysis service on synthetic worlds (exact numbers).
- Per rule good/bad fixture pair; meta-tests: every YAML rule has a check or `unmeasurable: reason`, every check has fixtures, ids unique, needs resolve.
- Integration: verify+export on all robots, golden report.json snapshots.
- Property tests (hypothesis): rigid-transform invariance, no crash on perturbed specs.
- CI: ruff, mypy (strict core/geometry/analysis), import-linter, `pytest -m "not slow"`; nightly deep + golden; coverage ≥90% core/geometry/analysis, ≥80% overall.

## NOT CHECKED → measurable
Beam/section bending for arms/forks/shells; serviceability from assembly graph; wire tethers as disassembly edges; insert/solder iron access by cylinder sweep; spin-up time from Kv/R/I; thermal I²R over 3 min; adhesive area×strength; imbalance m·e·ω²; combat R017–R125 each mapped to a geometric/physics measurement (seam crossing, fork tine stiffness, hit hop, gyro walk, recoil, closing time, tyre Shore→compression, wire ground clearance, battery puncture, rest poses on side, hookable protrusions, undercuts, armour per sector, pushing match). Data gaps become schema-required fields. Target: ~3 human-judged items left.

## Migration
0. Golden reports, CI, registry/context/result alongside old run(ctx), import-linter warn.
1. Parallel: geometry utils; analysis floor/parts/weapons; contacts/motion/mass; rules YAML + catalog data; io/pydantic; service unit tests.
2. Port checks per domain (6 agents, own folders), delete local helpers, fixtures per rule, golden diff empty.
3. Implement NOT CHECKED measurements.
4. Remove shims/_physics, enforce import-linter, raise coverage gate.
