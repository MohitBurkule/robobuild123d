"""Cross-check decoded XT faces against a STEP assembly (AP214, mm).

For each MANIFOLD_SOLID_BREP we collect the entity closure and the multiset of
CYLINDRICAL_SURFACE radii and PLANE count; the brep whose radius multiset best
matches the decoded part is reported."""
import re
from collections import Counter

ENT = re.compile(r'#(\d+)\s*=\s*(\w*)\s*\((.*?)\)\s*;', re.S)
REF = re.compile(r'#(\d+)')


def load(path):
    txt = open(path, encoding='latin1').read()
    ents = {}
    for m in ENT.finditer(txt):
        ents[int(m.group(1))] = (m.group(2), m.group(3))
    return ents


def breps(ents):
    out = {}
    for k, (t, a) in ents.items():
        if t == 'MANIFOLD_SOLID_BREP':
            out[k] = a.split(',')[0].strip().strip("'")
    return out


def closure_stats(ents, root):
    seen, stack = set(), [root]
    radii, planes = Counter(), 0
    while stack:
        n = stack.pop()
        if n in seen or n not in ents:
            continue
        seen.add(n)
        t, a = ents[n]
        if t == 'CYLINDRICAL_SURFACE':
            radii[round(float(a.rsplit(',', 1)[1]), 4)] += 1
        elif t == 'PLANE':
            planes += 1
        stack.extend(int(x) for x in REF.findall(a))
    return radii, planes


def best_match(ents, part_radii_mm, part_planes, cache={}):
    key = id(ents)
    if key not in cache:
        cache[key] = {b: (name, *closure_stats(ents, b)) for b, name in breps(ents).items()}
    target = Counter(round(r, 4) for r in part_radii_mm)
    best = None
    for b, (name, radii, planes) in cache[key].items():
        inter = sum((radii & target).values())
        union = sum((radii | target).values()) or 1
        sc = inter / union
        sset = len(set(radii) & set(target)) / (len(set(radii) | set(target)) or 1)
        sc = 0.5 * sc + 0.5 * sset
        if best is None or sc > best['score']:
            best = {'brep': b, 'name': name, 'score': round(sc, 3), 'set_jaccard': round(sset, 3), 'step_cyl': sum(radii.values()),
                    'part_cyl': sum(target.values()), 'step_planes': planes, 'part_planes': part_planes,
                    'radii_only_in_part': sorted((target - radii).elements())[:20],
                    'radii_only_in_step': sorted((radii - target).elements())[:20]}
    return best
