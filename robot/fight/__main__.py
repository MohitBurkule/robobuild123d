import argparse, json
from .run import fight

ap = argparse.ArgumentParser(prog="python -m robot.fight")
ap.add_argument("a"); ap.add_argument("b")
ap.add_argument("--seconds", type=float, default=20.0)
ap.add_argument("--out", default=None, help="video path (.mp4/.gif)")
ap.add_argument("--json", default=None)
ap.add_argument("--view", default="arena", choices=["arena", "chase", "fpv"])
ap.add_argument("--follow", default=None, help="robot name for chase/fpv (default: first)")
ap.add_argument("--seed", type=int, default=0)
ap.add_argument("--arena", default=None, help="closed | aws2025 | aws_classic | beetle_champs")
a = ap.parse_args()
r = fight(a.a, a.b, a.seconds, a.out, seed=a.seed, view=a.view, follow=a.follow, arena=a.arena)
if a.json:
    open(a.json, "w").write(json.dumps(r, indent=1))
print(json.dumps({k: r[k] for k in ("winner", "hits", "outcome")}, indent=1))
