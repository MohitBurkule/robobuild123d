"""Purchasable BOM (D4): turn a verified robot into order lines with UK vendors, pack quantities and spares.

`build(r)` maps every catalogue part, fastener, wire and printed part onto a Line;
`cost(lines)` totals it. Vendor rows come from robot/catalog_data/components.json
(supplier, url, price_gbp) matched by category and id substring - an unmatched row
is `unsourced` (a warning the report can carry), never an invented SKU.
Writes bom.csv, bom.md and per-supplier order_<supplier>.csv.
"""

from __future__ import annotations

import csv
import json
from dataclasses import dataclass, field
from pathlib import Path

DATA = Path(__file__).parent / "catalog_data" / "components.json"
SPARES = {"wheel": 1, "weapon": 0, "battery": 0, "esc": 0, "motor": 0}
DEFAULT_SPARES = 1  # one spare screw/bearing of each kind


@dataclass
class Line:
    id: str
    name: str
    kind: str
    qty: int
    unit_gbp: float | None = None
    supplier: str = ""
    url: str = ""
    pack_qty: int = 1
    spares: int = DEFAULT_SPARES
    printed: bool = False

    def to_buy(self) -> int:
        if self.printed:
            return 0
        return self.qty + self.spares

    def packs(self) -> int:
        if self.printed or self.unit_gbp is None:
            return 0
        return -(-self.to_buy() // max(self.pack_qty, 1))

    def cost(self) -> float:
        return round(self.packs() * (self.unit_gbp or 0.0), 2)


def _vendor_rows() -> list:
    try:
        return json.loads(DATA.read_text())
    except (OSError, ValueError):
        return []


def _match_vendor(kind: str, cid: str, rows: list) -> dict:
    cat = {"motor": "drive_motor", "weapon_motor": "weapon_motor", "esc": "esc", "battery": "battery",
           "wheel": "wheel", "bearing": "bearing", "fastener": "fastener", "receiver": "receiver"}.get(kind, kind)
    for row in rows:
        if row.get("category") != cat:
            continue
        name = str(row.get("name", ""))
        if any(tok in name.lower() for tok in cid.split("_")[:2] if len(tok) > 2):
            return row
    return {}


def build(r) -> list:
    """Order lines for a built robot (robot.world result: r.parts with .cat and .part)."""
    rows = _vendor_rows()
    lines, index = [], {}
    for rp in r.parts:
        p, cat = rp.part, rp.cat
        if p.kind in ("printed", "structure", "sheet") or getattr(p, "printed", False):
            lid = f"print:{p.id}"
            if lid not in index:
                index[lid] = Line(p.id, p.id, "printed", 1, printed=True)
                lines.append(index[lid])
            continue
        cid = cat.id if cat is not None else f"unknown:{p.kind}"
        if cid in index:
            index[cid].qty += 1
            continue
        v = _match_vendor(p.kind, cid, rows) if cat is not None else {}
        price = v.get("price_gbp")
        line = Line(cid, (cat.name if cat is not None else cid), p.kind, 1,
                    float(price) if isinstance(price, (int, float)) else None,
                    str(v.get("supplier", "")), str(v.get("url", "")),
                    int(v.get("pack_qty", 1)), SPARES.get(p.kind, DEFAULT_SPARES))
        index[cid] = line
        lines.append(line)
    for f in getattr(r.spec, "fasteners", []):
        cid = f"fastener:{f.size}"
        if cid in index:
            index[cid].qty += 1
        else:
            v = _match_vendor("fastener", f.size, rows)
            price = v.get("price_gbp")
            index[cid] = Line(f.size, f"{f.size} screws", "fastener", 1,
                              float(price) if isinstance(price, (int, float)) else None,
                              str(v.get("supplier", "")), str(v.get("url", "")), 50)
            lines.append(index[cid])
    return lines


def unsourced(lines: list) -> list:
    return [l.id for l in lines if not l.printed and l.unit_gbp is None]


def cost(lines: list) -> float:
    return round(sum(l.cost() for l in lines), 2)


def write(lines: list, out_dir) -> dict:
    """bom.csv, bom.md and per-supplier order CSVs; returns {files, cost_gbp, unsourced}."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    with (out / "bom.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "name", "kind", "qty", "spares", "to_buy", "pack_qty", "packs", "unit_gbp", "cost_gbp",
                    "supplier", "url"])
        for l in lines:
            w.writerow([l.id, l.name, l.kind, l.qty, l.spares, l.to_buy(), l.pack_qty, l.packs(),
                        "" if l.unit_gbp is None else f"{l.unit_gbp:.2f}", f"{l.cost():.2f}", l.supplier, l.url])
    sup = {}
    for l in lines:
        if l.supplier and not l.printed:
            sup.setdefault(l.supplier, []).append(l)
    for s, rows in sup.items():
        slug = "".join(c if c.isalnum() else "_" for c in s.lower())[:40]
        with (out / f"order_{slug}.csv").open("w", newline="") as fh:
            w = csv.writer(fh)
            w.writerow(["id", "name", "packs", "unit_gbp", "cost_gbp", "url"])
            for l in rows:
                w.writerow([l.id, l.name, l.packs(), f"{l.unit_gbp:.2f}", f"{l.cost():.2f}", l.url])
    md = ["# Bill of materials", "", "| part | kind | qty (+spares) | packs | cost | supplier |", "|---|---|---|---|---|---|"]
    for l in lines:
        md.append(f"| {l.name} | {l.kind} | {l.qty} (+{l.spares}) | {l.packs() or '-'} | "
                  f"{'-' if l.unit_gbp is None else f'{l.cost():.2f}'} | {l.supplier or 'unsourced'} |")
    md += ["", f"**Total: {cost(lines):.2f} GBP**"]
    (out / "bom.md").write_text("\n".join(md) + "\n")
    return {"files": sorted(p.name for p in out.iterdir()), "cost_gbp": cost(lines), "unsourced": unsourced(lines)}
