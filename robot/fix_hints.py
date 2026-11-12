"""Machine-readable fix hints for failed findings, so an LLM can self-repair without reading logs.

UNTESTED (written without running). Each hint = {kind, target, direction, amount, unit, parts, why}.
kind: "param" (a master param / spec setting), "swap" (catalogue part), "move" (placement), "waive" (last resort).
direction: "increase" | "decrease" | "set" | "move_apart" | "shorten" | "lengthen" | "swap" | "add" | "remove".
A check may attach exact hints via Finding.hint(...); otherwise DEFAULTS below give a generic one by id prefix.
"""

from __future__ import annotations

import re
from dataclasses import asdict, dataclass, field


@dataclass
class Hint:
    kind: str
    target: str
    direction: str
    amount: float | None = None
    unit: str = "mm"
    parts: list = field(default_factory=list)
    why: str = ""

    def to_dict(self):
        return asdict(self)


def _num(s):
    """First number in a string, or None."""
    m = re.search(r"-?\d+(?:\.\d+)?", str(s or ""))
    return float(m.group()) if m else None


def _gap(f, more=True):
    """|expected - actual| when both parse as numbers (amount to change by), else None."""
    e, a = _num(f.expected), _num(f.actual)
    return None if e is None or a is None else round(abs(e - a), 3)


# id (exact or prefix ending in '.') -> fn(finding) -> list[Hint]
def _h(kind, target, direction, why, amount=None, unit="mm"):
    return lambda f: [Hint(kind, target, direction, amount(f) if callable(amount) else amount, unit, list(f.parts), why)]


DEFAULTS = {
    "interference.overlap": _h("move", "placement/clearance of listed parts", "move_apart",
                               "solids overlap; move apart or cut pocket in the softer/printed part", _gap),
    "interference.spin_clearance": _h("param", "weapon clearance (disc radius or tub/wedge offset)", "increase",
                                      "spinning part too close to static part", _gap),
    "interference.spin": _h("param", "weapon swept radius vs chassis", "move_apart", "rotor sweep hits static part", _gap),
    "interference.sweep": _h("move", "placement of listed parts", "move_apart", "swept volume collides", _gap),
    "interference.wheel_clearance": _h("param", "wheel pocket clearance", "increase", "wheel rubs tub/side", _gap),
    "assembly.blocked": _h("move", "assembly order / insertion direction", "set",
                           "part has no free insertion path; open slot, change order, or split part"),
    "disasm.unreachable": _h("move", "service path of listed part", "set", "part trapped; add access opening or reorder"),
    "disasm.cycle": _h("move", "assembly order", "set", "circular dependency in disassembly; split one part or change retention"),
    "disasm.elastic_stretch": _h("param", "belt/o-ring length or pulley span", "lengthen", "stretch over material limit"),
    "mass.over": _h("param", "mass budget: weapon disc thickness / tub wall / infill", "decrease",
                    "robot over 150 g limit; cut mass from largest printed or steel part", _gap, "g"),
    "mass.may_be_over": _h("param", "mass margin", "decrease", "worst-case tolerance exceeds 150 g", _gap, "g"),
    "mass.unknown": _h("param", "declared mass of listed part", "add", "missing mass source; add catalogue/declared grams", None, "g"),
    "fastener.too_long": _h("swap", "screw length (catalogue)", "shorten", "screw bottoms out / pokes through", _gap),
    "fastener.engagement": _h("swap", "screw length or boss depth", "lengthen", "thread engagement too short", _gap),
    "fastener.no_thread": _h("param", "add heat-set / tapped hole / nut", "add", "screw has nothing to bite"),
    "fastener.head_seat": _h("param", "counterbore/countersink depth or Ø", "increase", "head does not seat", _gap),
    "fastener.access": _h("move", "tool access path / hole position", "set", "driver cannot reach screw"),
    "fastener.no_tool": _h("move", "tool access path", "set", "no straight tool path"),
    "fastener.nut_hex": _h("param", "nut trap hex size", "set", "nut trap not matching nut"),
    "printability.min_hole": _h("param", "hole diameter", "increase", "hole below printable minimum", _gap),
    "printability.overhang": _h("param", "chamfer/print orientation", "set", "unsupported overhang; chamfer 45 or reorient"),
    "printability.bridge": _h("param", "bridge span", "decrease", "bridge too long", _gap),
    "wall.": _h("param", "wall thickness", "increase", "wall below minimum", _gap),
    "thickness.": _h("param", "wall thickness", "increase", "wall below minimum", _gap),
    "contain.": _h("move", "shielding/routing of listed part", "set", "vulnerable part exposed to hits/ground"),
}


def _lookup(fid):
    if fid in DEFAULTS:
        return DEFAULTS[fid]
    best = max((k for k in DEFAULTS if k.endswith(".") and fid.startswith(k)), key=len, default=None)
    if best:
        return DEFAULTS[best]
    head = fid.split(".")[0] + "."
    return DEFAULTS.get(head)


def hints_for(f) -> list:
    """Hints for a finding: the check's own (Finding.repair) first, else the default table, else from fix_hint text."""
    if getattr(f, "repair", None):
        return list(f.repair)
    fn = _lookup(f.id)
    if fn:
        return [h.to_dict() for h in fn(f)]
    if f.fix_hint:
        return [Hint("text", "", "set", None, "", list(f.parts), f.fix_hint).to_dict()]
    return []


def suggest_fixes(report, severities=("blocker",)) -> dict:
    """Summary for an LLM repair loop: hints grouped by target, ranked by how many failures they address."""
    rows, by_target = [], {}
    for f in report.findings:
        if f.passed or f.severity not in severities:
            continue
        for h in hints_for(f):
            rows.append({"finding": f.id, **h})
            t = by_target.setdefault(h["target"] or f.id, {"target": h["target"], "direction": h["direction"],
                                                            "findings": [], "parts": set(), "max_amount": None})
            t["findings"].append(f.id)
            t["parts"].update(h["parts"])
            if h["amount"] is not None:
                t["max_amount"] = max(h["amount"], t["max_amount"] or 0)
    ranked = sorted(by_target.values(), key=lambda t: -len(t["findings"]))
    for t in ranked:
        t["parts"] = sorted(t["parts"])
    return {"count": len(rows), "ranked": ranked, "hints": rows}
