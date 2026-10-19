"""Design intent as data: every generated feature says WHY it exists, and its size follows from that why.

A feature is a part, a solid added to or cut from a chassis half, a pocket, a fastener, a wire or a joint between parts.
Each one carries `intent = {purpose, reason, load_or_constraint}`:

- purpose: one of PURPOSES
- reason: the design reason in words (what would go wrong without it)
- load_or_constraint: the number or rule that sized it (a load in N / J, a part dimension, a print rule, a clearance)

`check(spec)` lists every feature of a generated spec that has no valid intent; the gate refuses such a spec. The sizing
helpers below are what generators call to turn an intent into geometry (see DESIGN_INTENT.md for the rules).
"""

from __future__ import annotations

import math

PURPOSES = ("load_path", "retention", "assembly", "service", "protection", "ground_game", "wiring", "mass")

# print rules (FDM, 0.4 mm nozzle)
LINE_W = 0.42
MIN_PERIMETERS = 4  # impact parts: 4 perimeters (Revron build guide: 4-6 perimeters, never fewer)
MIN_WALL_FDM = round(MIN_PERIMETERS * LINE_W - 0.08, 2)  # 1.6 mm
MIN_SKIN_FDM = 1.0  # roof / floor skin: 4-5 top/bottom layers at 0.2 mm
# allowable bending stress for printed nylon / PLA-ST under a one-off hit, with a factor of 2 (MPa)
SIGMA_ALLOW = {"nylon": 20.0, "pla_st": 22.0, "pla": 18.0, "petg": 18.0, "tpu": 6.0, "pc": 25.0}


def I(purpose: str, reason: str, load_or_constraint: str) -> dict:  # noqa: E743 (short on purpose: used everywhere)
    """An intent record. Raises on an unknown purpose or an empty reason/constraint, so it cannot be skipped."""
    if purpose not in PURPOSES:
        raise ValueError(f"intent purpose {purpose!r} not in {PURPOSES}")
    if not str(reason).strip() or not str(load_or_constraint).strip():
        raise ValueError("intent needs a reason and the load or constraint that sized it")
    return {"purpose": purpose, "reason": str(reason), "load_or_constraint": str(load_or_constraint)}


def valid(intent) -> bool:
    return (isinstance(intent, dict) and intent.get("purpose") in PURPOSES and bool(str(intent.get("reason", "")).strip())
            and bool(str(intent.get("load_or_constraint", "")).strip()))


# ------------------------------------------------------------------------------------------------- sizing from intent

def wall_for(load_n: float, span_mm: float, material: str = "nylon", min_wall: float = MIN_WALL_FDM) -> float:
    """Plate wall that carries `load_n` across `span_mm` in bending (simply supported strip as wide as the span):
    t = sqrt(6 M / (b sigma)), M = F L / 4, b = L  ->  t = sqrt(1.5 F / sigma). Never under the print minimum."""
    sig = SIGMA_ALLOW.get(material, 18.0)
    t = math.sqrt(1.5 * max(load_n, 0.0) / sig)
    return round(max(t, min_wall), 2)


def boss_r_for(screw_d: float, insert_od: float | None = None) -> float:
    """Boss round a heat-set insert: insert OD / 2 + 1.2 mm wall (Revron guide: >= 1.2 mm round an M2 insert)."""
    od = insert_od if insert_od is not None else {2.0: 3.2, 2.5: 3.6, 3.0: 4.0}.get(screw_d, screw_d + 1.2)
    return round(od / 2 + 1.2, 2)


def screw_dir(assembly_dir) -> list:
    """A screw is driven along the direction its part is assembled (the head ends up on the outside)."""
    n = math.sqrt(sum(v * v for v in assembly_dir)) or 1.0
    return [round(v / n, 6) for v in assembly_dir]


def pocket_gap(retention: str) -> float:
    """Clearance round a bought part: a press fit hugs it, a strapped/stuck part needs print tolerance only."""
    return {"press_fit": 0.1, "captive": 0.3}.get(retention, 0.4)


def chamfer_for(cause: str) -> float:
    """Edge bevel: `print` = a 45 deg lead-in that removes elephant's foot / overhang (1 mm); `impact` = knock the corner
    off a face that takes hits so it deflects rather than catching (1.5 mm); `handling` = 0.6 mm."""
    return {"print": 1.0, "impact": 1.5, "handling": 0.6}[cause]


def belt_ring_for(centre_mm: float, groove_r_rear: float, groove_r_front: float, stretch: float = 0.07) -> float:
    """Inside diameter of an O-ring belt over two grooved pulleys at `centre_mm`, stretched by `stretch`:
    belt length = 2 C + pi (r1 + r2) (open belt, approx), ring ID = length / (pi (1 + stretch))."""
    L = 2 * centre_mm + math.pi * (groove_r_rear + groove_r_front)
    return L / (math.pi * (1 + stretch))


# ------------------------------------------------------------------------------------------------- check

def check(spec: dict) -> list[str]:
    """Every feature of a generated spec that lacks a valid intent (empty list = every feature has its why)."""
    gen = spec.get("generator") or {}
    feats = gen.get("features")
    if feats is None:
        return ["spec has no generator.features record (not generated, or generated without intents)"]
    out = []
    for f in feats:
        if not valid(f.get("intent")):
            out.append(f"{f.get('op')} {f.get('target') or f.get('id')} ({f.get('src', '?')}): no intent")
    has = {(f.get("op"), f.get("target")) for f in feats if valid(f.get("intent"))}
    for p in spec.get("parts", []):
        if ("part", p["id"]) not in has:
            out.append(f"part {p['id']}: no intent")
    for fa in spec.get("fasteners", []):
        if ("fastener", fa["id"]) not in has:
            out.append(f"fastener {fa['id']}: no intent")
    for w in spec.get("wires", []):
        if ("wire", w["id"]) not in has:
            out.append(f"wire {w['id']}: no intent")
    for c in spec.get("connections", []):
        if ("connect", f"{c['a']}~{c['b']}") not in has:
            out.append(f"connection {c['a']}~{c['b']}: no intent")
    return out
