# pla_st_is_a_perfectly_legitima: struggles

The robot has omni-directional wheels.

## What the model has
- Each wheel is a hub with two staggered rows of 8 barrel rollers (generator key `wheels.omni: true`, spec tag `wheel_type: "omni"`). The shared kit part `omni_wheel` (dev #227) exists now and is the right home for this shape.

## What the toolchain lacks
1. The spec has no wheel type field that the checks read. `wheel_type: "omni"` is carried as an extra and ignored: traction, pushing force and the fight sim treat it as a plain grippy wheel (an omni wheel has near-zero sideways grip, which is the whole point).
2. Ground contact: the contact patch is a roller, not the wheel cylinder; `ground.wheel_floating` measures the envelope and can be off by the roller sag.
3. Printability/mfg: the rollers need pins; there is no catalog omni wheel SKU at antweight size, so every roller is a free bought part (`mfg.stock`).
4. Drive layout: omni wheels usually sit at 45/90 degrees to each other; the kit only places wheels with axles along x.
