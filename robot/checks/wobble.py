"""Spinner wobble under real-world imbalance, mount flex, bearing play and a hit (MuJoCo, robot/fight/wobble.py), then the
real weapon meshes swept through a turn at that deflection: every static part they would touch is a blocker.
Resonance: spin frequency within 15 % of the mount's natural frequency is a warning (the weapon shakes the robot apart)."""

from __future__ import annotations

from ..finding import BLOCKER, WARNING, fail, note, ok

G = "wobble"


def run(ctx):
    sp = ctx.r.spec
    if not sp.is_spinner:
        return []
    try:
        from ..fight import profile, wobble
        from ..sim import model as model_mod
    except ImportError as e:  # mujoco not installed
        ctx.not_checked.append(f"Spinner wobble: {e} (pip install -e .[sim])")
        return []
    m = model_mod.extract(ctx.world, ctx.r)
    if m.weapon is None:
        ctx.not_checked.append("Spinner wobble: no rotating weapon group (spec joint / rotates_with)")
        return []
    p, guessed = wobble.params(sp)
    res = wobble.simulate(m, profile.build(sp), p)
    if res is None:
        return []
    ctx.metrics.update({f"wobble.{k}": v for k, v in res.items()})
    out = [note("wobble.numbers", G, "Weapon wobble and hit deflection",
                ", ".join(f"{k} {v}" for k, v in res.items()) + (f" (guessed: {', '.join(guessed)})" if guessed else ""))]
    r = res["spin_hz"] / max(res["mount_hz"], 1e-6)
    if 0.85 < r < 1.15:
        out.append(fail("wobble.resonance", G, WARNING, "Weapon spins at the mount's natural frequency",
                        f"spin {res['spin_hz']} Hz vs mount {res['mount_hz']} Hz: stiffen the uprights or change the rpm."))
    hits, coupled = wobble.clearance(ctx.world, m, res["hit_mm"], res["hit_tilt_deg"])
    if hits:
        sev = WARNING if {"mount_k_Npm", "hit_N"} & set(guessed) else BLOCKER  # guessed stiffness/hit: flag, don't block
        out.append(fail("wobble.clearance", G, sev, "Weapon hits the robot when it deflects",
                        f"at {res['hit_mm']} mm / {res['hit_tilt_deg']} deg after a {p['hit_N']:.0f} N hit the weapon touches: "
                        + ", ".join(f"{k} ({v} pts)" for k, v in sorted(hits.items(), key=lambda x: -x[1]))
                        + f". Riding with the weapon (skipped): {', '.join(coupled) or 'none'}."))
    else:
        out.append(ok("wobble.clearance", G, "Weapon clears the robot when deflected",
                      f"{res['hit_mm']} mm / {res['hit_tilt_deg']} deg"))
    return out
