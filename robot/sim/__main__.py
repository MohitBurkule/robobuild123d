"""python -m robot.sim <spec.json> [drop|drive|ramp|push|ram|all]"""

import json
import sys

from . import load, scenarios

TESTS = {"drop": scenarios.drop_test, "drive": scenarios.drive_test, "ramp": scenarios.ramp_test,
         "push": scenarios.push_prop_test}


def main(argv):
    if not argv:
        print(__doc__)
        return 2
    m = load(argv[0])
    which = argv[1] if len(argv) > 1 else "all"
    print(f"{m.name}: {m.mass * 1000:.1f} g, groups {[(g.name, g.kind) for g in m.groups]}")
    for k, f in TESTS.items():
        if which in ("all", k):
            print(k, json.dumps({a: round(b, 4) if isinstance(b, float) else b for a, b in f(m).items()}))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
