# Verifier issues found while building the template engine (`robot/gen`)

These were not fixed here, because `robot/checks` belongs to the verifier thread. Each entry has a minimal reproduction:
`python3 -m robot gen build --hypothesis lifter --out /tmp/l --no-gate`, then `python3 -m robot verify /tmp/l/lifter.json --fast`.

## 1. [RESOLVED upstream in antweight-verifier: SectorSweep] A limited-range revolute joint is swept and balanced as if it spun a full turn (blocks every lifter/flipper)

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

The lifter `xfail` has been removed; the lifter passes full verify.

## 2. [RESOLVED upstream] `arch.fork_stiffness` takes the root from fasteners into `a.chassis` only

When the chassis is a clamshell, `a.chassis` is one half, so bolts into the other half are ignored. For a drisk
upright bolted to both halves, the root fell on the single top-half bolt and the lever ran through a 3 mm roof tab:
I = 11 mm⁴, reported deflection 26.7 mm. The real upright section is above 1000 mm⁴.

Suggested fix: count every structure part rigidly joined to the chassis (the clamshell halves) as root.

## 3. [RESOLVED upstream: band hits confirmed against posed meshes] `SectorSweep` fills the radial band between a part's inner and outer radius in each (axial, angle) bin

`SectorSweep` keeps one `[rmin, rmax]` band per axial bin and angle bin. When a part has material near the axis and
far from it in the same axial slice, the band covers everything in between. Here, a lifter hub on the axis
(r 2.2) and the scoop plate (r 20-37) share the same x slice. Any static geometry between the two is then reported
inside the sweep, even though nothing passes there.

Example: the front-wall corner at r 13.7 was reported as `kin.sweep_static` 5.3 mm deep. A direct rotation of the
mesh over 0..35° shows the scoop never comes within 6 mm of it. `interference.sweep` passes for the same arm.

Generator workaround: the servo now sits in a window in the side wall, with its output face outside the wall, so no
part of the scoop shares an axial slice with the chassis.

Suggested fix: keep a list of radial intervals per bin, or confirm hits with a posed-mesh test, as
`interference.sweep` does.

## 4. [NOT A BUG, withdrawn] joint frame

The verifier correctly reads a joint's pivot and axis in the parent's declared `at`/`rot` frame. My diagnosis was
wrong: I took the measurement from a spec where I had already rewritten the joint as world `[1,0,0]` under the
rotated servo parent. The lifter scoop is a servo-parented joint again, with axis `[0,0,1]` in the servo frame, and it
passes.

## 5. `mfg.thin_wall` warns about a stock 1.0 mm O-ring that `kin.belt_stock` requires

`kin.belt_stock` accepts only O-ring sections in `STOCK_ORINGS` (1.0, 1.5 and 2.0 mm). Every O-ring belt has
`process: cots` and `material: rubber`. `mfg.thin_wall` then warns that a 1.0 mm cord is under the 1.2 mm minimum for
cots rubber. A bought part has no printed walls, so the warning does not apply. This is a warning, not a blocker.

Suggested fix: skip `mfg.thin_wall` for `process: cots` parts, or at least for `kind: belt`.

## 6. `arch.fork_stiffness` roots an upright at its contact with the chassis, not at the standoff it is screwed to

The setup is the experimental `chassis=tub` option. Each weapon upright is clamped by M3 screws to alu standoffs, and
the standoffs sit in lugs of the tub. The standoffs are not part of `_rigid_chassis`, so the screws do not count as the
upright's root. The check falls back to the foot's mesh contact with the tub, which gives a 29.3 mm lever. Revron's
real uprights are rooted the same way. I have not confirmed whether the lever is wrong, or whether the plate really is
too flexible there. It is recorded so the generator's tub option can be re-checked once this is settled.
