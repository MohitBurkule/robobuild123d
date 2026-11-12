"""BOM rows from the spec: made parts, COTS (catalog) parts, fasteners grouped by designation, wires."""

from __future__ import annotations

from collections import Counter

from .. import catalog
from ._util import x

PROCESS_MADE = {"fdm": "print", "resin": "print", "laser": "cut", "waterjet": "cut", "cnc": "machine",
                "sheet": "cut", "bent_sheet": "cut+bend", "turned": "turn"}


def _source(p):
    cid = x(p, "catalog")
    if cid:
        e = catalog.find(cid)
        return "buy", (e.name if e else cid), e
    return PROCESS_MADE.get((x(p, "process") or "").lower(), "make"), x(p, "label") or p.id, None


def bom(spec):
    """One row per part (made or bought), fasteners grouped, wires summed. List of dicts."""
    rows = []
    for p in spec.parts:
        how, name, e = _source(p)
        rows.append({"id": p.id, "name": name, "qty": 1, "how": how, "kind": p.kind,
                     "material": x(p, "material"), "process": x(p, "process"),
                     "catalog": x(p, "catalog"), "mass_g": e.mass_g if e else x(p, "mass_g"),
                     "source": (e.props or {}).get("vendor") if e else None})
    for desig, n in fastener_counts(spec).items():
        rows.append({"id": desig, "name": desig, "qty": n, "how": "buy", "kind": "fastener",
                     "material": None, "process": None, "catalog": None, "mass_g": None, "source": None})
    for w in spec.wires:
        rows.append({"id": w.id, "name": f"wire {x(w, 'awg') or '?'} AWG {x(w, 'kind') or ''}".strip(), "qty": 1,
                     "how": "cut", "kind": "wire", "material": "copper", "process": None, "catalog": None,
                     "mass_g": None, "source": None})
    return rows


def fastener_counts(spec):
    """{designation: count}, plus a key per insert/nut part kind."""
    c = Counter((f.designation or "?").strip() for f in spec.fasteners)
    for p in spec.parts:
        if p.kind in ("nut", "insert"):
            c[f"{p.kind}:{x(p, 'catalog') or x(p, 'label') or p.id}"] += 1
    return dict(sorted(c.items()))


def buy_list(spec):
    """COTS rows merged by catalog id / designation: what to order."""
    agg = {}
    for r in bom(spec):
        if r["how"] != "buy":
            continue
        k = r["catalog"] or r["name"]
        if k in agg:
            agg[k]["qty"] += r["qty"]
        else:
            agg[k] = dict(r)
    # spares: one extra per small fastener size, they get lost
    for r in agg.values():
        r["order_qty"] = r["qty"] + (max(1, r["qty"] // 4) if r["kind"] == "fastener" else 0)
    return sorted(agg.values(), key=lambda r: (r["kind"] != "fastener", r["name"]))
