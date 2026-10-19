"""reference.unmapped_part: every spec part and fastener must map to a part of the REFERENCE design (the STEP parts
index), or carry a written deviation. Our own `reference_bom` rows do not count as a reference: a row maps its ids
only when it cites reference parts that exist in the index.

A spec id is mapped when one of these holds:
- a `reference_cad.parts` entry names it with a file that is in the reference parts index;
- the part / fastener has `ref_part` (a stem glob or list of them) that matches the index;
- a `reference_bom` row matches it and cites the index: `ref_parts` globs, or a role word that starts an index stem
  (`FS8`, `RV15`, `spider`, `Drisk_floating_3`) or a 5+ digit standard number inside one (`24036`). A row whose role
  says "not in the STEP" / "not in the reference" never cites the index;
- a fastener whose designation (M3x8) appears in an index stem (`..._M3_x_8_...`);
- its left/right sibling id (`wheel_rl` / `wheel_rr`) is mapped by reference_cad and the index has a second copy.

Otherwise it needs a `deviation` reason (on the part / fastener, or on a matching reference_bom row) or it fails.
The index is the `.stl`/`.step` stems in `reference_cad.dir` (or `review.reference_index.dir`), plus INDEX.txt beside it.
"""

from __future__ import annotations

import fnmatch
import re
from pathlib import Path

from .. import catalog
from ..finding import BLOCKER, fail, ok
from ._review import x

G = "reference"
NOT_REF = re.compile(r"not in the (step|reference)", re.I)


def index_stems(spec):
    raw = spec.raw or {}
    d = ((raw.get("review") or {}).get("reference_index") or {}).get("dir") or (raw.get("reference_cad") or {}).get("dir")
    if not d:
        return None
    p = Path(d)
    if not p.is_absolute():
        p = Path(spec.base_dir) / p
    stems = set()
    if p.is_dir():
        stems |= {f.stem for f in p.iterdir() if f.suffix.lower() in (".stl", ".step", ".stp")}
    for idx in (p / "INDEX.txt", p.parent / "INDEX.txt"):
        if idx.is_file():
            stems |= {ln.split()[0] for ln in idx.read_text().splitlines() if ln.strip()}
    return stems


def _norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def _base(stem):
    return re.sub(r"_\d+$", "", stem)


def cited(text, stems):
    """Index stems a reference_bom role text cites (empty when it says it is not in the reference)."""
    if not text or NOT_REF.search(text):
        return []
    hits = []
    for tok in re.findall(r"[A-Za-z0-9_]+", text):
        t = tok.lower()
        if len(t) < 3 or (len(t) < 5 and not any(c.isdigit() for c in t)):
            continue
        for s in stems:
            sl = s.lower()
            if sl.startswith(t) and (len(sl) == len(t) or not sl[len(t)].isalnum() or t[-1].isdigit()):
                hits.append(s)
            elif t.isdigit() and len(t) >= 5 and t in sl:
                hits.append(s)
    return sorted(set(hits))


def _glob(pats, stems):
    pats = [pats] if isinstance(pats, str) else list(pats or [])
    return [s for s in stems if any(fnmatch.fnmatchcase(s, p) or fnmatch.fnmatchcase(s, p + "*") for p in pats)]


def _sibling(i):
    """Ids with one of the last two characters swapped l <-> r (wheel_rl -> wheel_rr, side_l -> side_r)."""
    out = []
    for k in range(max(0, len(i) - 2), len(i)):
        if i[k] in "lr":
            out.append(i[:k] + ("r" if i[k] == "l" else "l") + i[k + 1:])
    return out


def classify(spec, stems):
    """{id: (status, why)} with status mapped / deviation / unmapped, for every part and fastener."""
    raw = spec.raw or {}
    cad = {e.get("part"): e.get("file", "") for e in ((raw.get("reference_cad") or {}).get("parts") or [])}
    cad_ok = {pid: Path(f).stem for pid, f in cad.items() if Path(f).stem in stems}
    rows = raw.get("reference_bom") or []
    items = [("part", p) for p in spec.parts] + [("fastener", f) for f in spec.fasteners]
    out = {}
    for kind, o in items:
        i = o.id
        if i in cad_ok:
            out[i] = ("mapped", f"reference_cad -> {cad_ok[i]}")
            continue
        g = _glob(x(o, "ref_part"), stems)
        if g:
            out[i] = ("mapped", f"ref_part -> {g[0]}")
            continue
        status = None
        for row in rows:
            if not any(fnmatch.fnmatchcase(i, m) for m in (row.get("match") or [])):
                continue
            c = _glob(row.get("ref_parts"), stems) or cited(row.get("role", ""), stems)
            if c:
                status = ("mapped", f"reference_bom `{row.get('role')}` -> {c[0]}")
                break
            if row.get("deviation") and status is None:
                status = ("deviation", f"reference_bom `{row.get('role')}`: {row['deviation']}")
        if status is None and kind == "fastener":
            dl = catalog.parse_designation(o.designation)
            if dl:
                key = _norm(f"m{dl[0]:g}x{dl[1]:g}")
                hit = next((s for s in stems if key in _norm(s)), None)
                if hit:
                    status = ("mapped", f"designation {o.designation} -> {hit}")
        if status is None or status[0] != "mapped":
            for sib in _sibling(i):
                if sib in cad_ok:
                    base = _base(cad_ok[sib])
                    if sum(1 for s in stems if _base(s) == base) >= 2:
                        status = ("mapped", f"mirror of `{sib}` -> {base}")
                        break
        if (status is None or status[0] != "mapped") and x(o, "deviation"):
            status = ("deviation", str(x(o, "deviation")))
        out[i] = status or ("unmapped", "")
    return out


def run(ctx):
    spec = ctx.r.spec
    stems = index_stems(spec)
    if not stems:
        ctx.not_checked.append("reference.unmapped_part: no reference parts index (reference_cad.dir)")
        return []
    res = classify(spec, stems)
    bad = sorted(i for i, (s, _) in res.items() if s == "unmapped")
    dev = sorted(i for i, (s, _) in res.items() if s == "deviation")
    out = []
    for i in bad:
        out.append(fail("reference.unmapped_part", G, BLOCKER, "Part not in the reference",
                        f"`{i}` maps to no part of the reference design ({len(stems)} parts in the index) and has no written "
                        "`deviation`. Invented hardware must be justified.").on(i)
                   .fix("Map it (reference_cad entry, `ref_part`, or a reference_bom row citing the STEP part), remove it, "
                        "or add `deviation: \"why it differs from the reference\"`."))
    if not bad:
        out.append(ok("reference.unmapped_part", G, "Every part maps to the reference",
                      f"{len(res) - len(dev)} parts/fasteners map to reference parts; {len(dev)} carry a written deviation."))
    ctx.metrics["reference_unmapped"] = len(bad)
    ctx.metrics["reference_deviation_ids"] = dev
    return out
