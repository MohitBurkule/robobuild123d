# Verifier issues found while building the template engine (`robot/gen`)

These were not fixed here, because `robot/checks` belongs to the verifier thread. Each entry has a minimal reproduction:
`python3 -m robot gen build --hypothesis lifter --out /tmp/l --no-gate`, then `python3 -m robot verify /tmp/l/lifter.json --fast`.

## 1. A limited-range revolute joint is swept and balanced as if it spun a full turn (blocks every lifter/flipper)

`kinematics.finalize_groups` makes every part with a `revolute` joint a rotating group. After that:

- `sweeps()` builds `Sweep(P, axis)` over 360°.
- `kin.balance_static` applies spinner limits (0.5 mm CoM offset).

None of this reads `joint.min/max`. A servo lifter scoop on a `0..35°` joint is reported as hitting the chassis, the
drive motors and the top half "on the first turn" (`kin.sweep_static`). It also fails `kin.balance_static` because its
mass centre is 20 mm off the pivot, which is true of every lifting arm.

`interference.sweep` already sweeps the declared joint range correctly and passes for the same arm.

Suggested fix:
- For a group whose joint range is below 360° and that is not a spin weapon, sweep only `[min, max]`.
- Skip the balance check for such a group, or use a torque-about-pivot check instead.

`robot/tests/test_gen_integration.py` marks the lifter case `xfail` with a pointer to this entry. Every other
lifter blocker has been fixed in the generator.

## 2. `arch.fork_stiffness` takes the root from fasteners into `a.chassis` only

When the chassis is a clamshell, `a.chassis` is one half, so bolts into the other half are ignored. For a drisk
upright bolted to both halves, the root fell on the single top-half bolt and the lever ran through a 3 mm roof tab:
I = 11 mm⁴, reported deflection 26.7 mm. The real upright section is above 1000 mm⁴.

Suggested fix: count every structure part rigidly joined to the chassis (the clamshell halves) as root.
