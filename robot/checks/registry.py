"""The one registry of check groups: run order, what each group judges (`kind`) and what it costs (`tier`).

kind   "design"  valid for any robot: is this a legal, working, manufacturable design. Needs no reference.
       "parity"  compares with the ORIGINAL designer's data (reference CAD meshes, SolidWorks dumps, photos, the
                 reference parts index). A newly generated robot has none of it, so parity never decides `ok` unless
                 the caller asks for the old combined gate (`Options.combined`, `robot verify --combined`).
tier   "inner"   cheap: the whole tier is the edit loop (target well under 60 s on Revron).
       "full"    every design group at full fidelity (the merge gate).
       "nightly" sweeps and parity: robust (perturbation sweep) and every reference comparison.
       A tier runs its own groups and those of the cheaper tiers.
proxy  name of the fast stand-in in robot/proxy that the inner tier runs in place of a slower group.
ref_s  seconds the group took on robots/revron/spec.json in the last logged full run (progress/verify.log, one
       process per group, cold group cache); `robust` is from the CI summary. A guide for tiering, not a promise.

A few design groups also emit findings that compare with the reference (the BOM group's `reference.bom`, the motor
envelope vs the STEP): PARITY_IDS moves those single findings to the parity section.
"""

from __future__ import annotations

from dataclasses import dataclass

DESIGN, PARITY = "design", "parity"
INNER, FULL, NIGHTLY = "inner", "full", "nightly"
KINDS = (DESIGN, PARITY)
TIERS = (INNER, FULL, NIGHTLY)


@dataclass(frozen=True)
class Group:
    name: str
    kind: str
    tier: str
    ref_s: float | None = None  # logged seconds on Revron
    deep_only: bool = False  # skipped by --quick (Options.deep = False)
    proxy: str | None = None  # robot.proxy group the inner tier runs instead
    note: str = ""


def _g(name, kind, tier, ref_s=None, **kw):
    return Group(name, kind, tier, ref_s, **kw)


# Run order matters (later groups read metrics / routes / captive maps of earlier ones); same order as the Rust crate.
REGISTRY = [
    _g("integrity", DESIGN, INNER, 3.2, note="one closed solid, no volume collapse (first and cheap)"),
    _g("wiring", DESIGN, FULL, 8.4, deep_only=True, proxy="wiring", note="voxel router, A* per wire"),
    _g("mass", DESIGN, INNER, 0.0),
    _g("interference", DESIGN, FULL, 149.9, proxy="interference", note="inscribed depth, joint sweeps"),
    _g("connections", DESIGN, INNER, 8.6),
    _g("internal", DESIGN, FULL, 17.0),
    _g("ground", DESIGN, FULL, 42.9),
    _g("legal", DESIGN, INNER, 0.7),
    _g("fasteners", DESIGN, INNER, 7.6),
    _g("power", DESIGN, INNER, 0.1),
    _g("mfg", DESIGN, FULL, 153.1),
    _g("spinner", DESIGN, FULL, 19.8),
    _g("kinematics", DESIGN, FULL, 179.0),
    _g("tension", DESIGN, INNER, 0.0),
    _g("targets", DESIGN, INNER, 0.2, note="the spec's own declared target dimensions"),
    _g("shape", DESIGN, INNER, 6.5),
    _g("dynamics", DESIGN, INNER, 0.0),
    _g("strength", DESIGN, INNER, 2.6),
    _g("printability", DESIGN, INNER, 6.0),
    _g("process", DESIGN, INNER, 0.8),
    _g("reference", PARITY, NIGHTLY, 0.2, note="silhouette vs reference photos"),
    _g("archetype", DESIGN, FULL, 14.9),
    _g("architecture", DESIGN, FULL, 100.0),
    _g("electrical", DESIGN, INNER, 1.1),
    _g("combat", DESIGN, INNER, 2.6),
    _g("assembly", DESIGN, FULL, 145.3, deep_only=True, proxy="assembly", note="greedy take-apart search"),
    _g("joints", DESIGN, FULL, 44.9),
    _g("material", DESIGN, FULL, 5.7),
    _g("plausibility", DESIGN, INNER, 0.0),
    _g("reference_ratios", PARITY, NIGHTLY, 0.0, note="proportions measured on reference photos"),
    _g("reference_cad", PARITY, NIGHTLY, 892.8, proxy="reference_cad", note="per-part diff vs reference meshes"),
    _g("intent", DESIGN, FULL, 1092.0, note="functional design-intent probes"),
    _g("cots", DESIGN, INNER, 0.0),
    _g("fit", DESIGN, INNER, 1.7),
    _g("contain", DESIGN, FULL, 23.7),
    _g("disasm", DESIGN, FULL, 11.2),
    _g("coverage", DESIGN, FULL, 5.0),
    _g("bom", DESIGN, INNER, 0.9, note="lock part, O-ring stock, wire cut, switch; its reference.* findings are parity"),
    _g("support", DESIGN, FULL, 5.0),  # gravity in all 6 orientations (robot/checks/support.py)
    _g("threat", DESIGN, FULL, 311.1),  # combat failure modes CF-* (robot/checks/threat)
    _g("fastener_seat", DESIGN, FULL, 51.8),  # head/thread vs hole geometry (robot/cad/seat.py)
    # design-review gates (CAD review of Revron 2.0): one module each
    _g("ref_map", PARITY, NIGHTLY, 0.3, note="reference.unmapped_part vs the reference parts index"),
    _g("cots_fidelity", DESIGN, FULL, 14.6, note="vs catalog feature tables; cots.motor_volume (vs STEP) is parity"),
    _g("wire_review", DESIGN, INNER, 0.5),  # wire.rotating_clearance, wire.render_present
    _g("fastener_record", DESIGN, INNER, 0.0),  # fastener.hole_record
    _g("drive_recess", DESIGN, INNER, 0.4),  # fastener.drive_recess
    _g("belt_wrap", DESIGN, INNER, 0.3),  # cots.belt_wrap
    _g("print_orient", DESIGN, FULL, 4.7),  # print.orientation_declared
    _g("retention", DESIGN, INNER, 0.0),  # retention.axial (robot/checks/retention.py)
    _g("sharp_corner", DESIGN, FULL, 59.5, note="reads the reference only to excuse corners it also has"),
    _g("visual", PARITY, NIGHTLY, 934.0, note="silhouette / depth / fillet vs the reference mesh"),
    _g("practice", DESIGN, FULL, 614.8, note="best-CAD-practice gates with NO reference"),
    _g("sldprt_dump", PARITY, NIGHTLY, 14.9, note="dump.* vs the SolidWorks part dumps"),
    _g("asm_dump", PARITY, NIGHTLY, 0.9, note="asm.* vs the SolidWorks assembly dump"),
    _g("param", DESIGN, FULL, 9.0, note="raw-literal lint; param.budget (vs dump dimension count) is parity"),
    _g("robust", DESIGN, NIGHTLY, 900.0, deep_only=True, note="one-at-a-time param / variant / COTS-swap sweep"),
]

INFO = {g.name: g for g in REGISTRY}
# Findings of design groups that compare with the reference: id (exact) or "prefix." -> parity.
PARITY_IDS = ("reference.", "bom.added_parts", "cots.motor_volume", "param.budget")


def kind_of(group: str, finding_id: str = "") -> str:
    """Kind of one finding produced by registry group `group` (pseudo-groups such as validity / claims are design)."""
    g = INFO.get(group)
    if g is not None and g.kind == PARITY:
        return PARITY
    if any(finding_id == k or (k.endswith(".") and finding_id.startswith(k)) for k in PARITY_IDS):
        return PARITY
    return DESIGN


def in_tier(group: Group, tier: str) -> bool:
    return TIERS.index(group.tier) <= TIERS.index(tier)


@dataclass
class Selection:
    run: list  # full groups to run, in registry order
    proxies: list  # groups judged by their robot.proxy stand-in instead (inner tier)
    not_run: list  # [{group, kind, tier, reason}] of everything else
    filtered: bool  # False: nothing was asked for, every group runs exactly as before


def select(tier=None, parity="both", only=None, deep=True) -> Selection:
    """Which groups a run executes. `only` (explicit names) wins over `tier`; `parity` is "both" | "no" | "only"
    ("only" runs the parity groups whatever their tier)."""
    if parity not in ("both", "no", "only"):
        raise ValueError(f"parity must be both|no|only, not {parity!r}")
    if tier is not None and tier not in TIERS:
        raise ValueError(f"unknown tier {tier!r}; tiers: {', '.join(TIERS)}")
    run, proxies, not_run = [], [], []

    def skip(g, why):
        not_run.append({"group": g.name, "kind": g.kind, "tier": g.tier, "reason": why})

    for g in REGISTRY:
        if g.deep_only and not deep and not (tier == INNER and g.proxy and not only):
            skip(g, "slow sweep skipped by --quick")
        elif only:
            (run.append(g.name) if g.name in only else skip(g, "not named by --only"))
        elif parity == "only":
            (run.append(g.name) if g.kind == PARITY else skip(g, "design group (--parity-only)"))
        elif g.kind == PARITY and parity == "no":
            skip(g, "parity group (--no-parity)")
        elif tier is None or in_tier(g, tier):
            run.append(g.name)
        elif tier == INNER and g.proxy and g.kind == DESIGN:
            proxies.append(g.name)
        else:
            skip(g, f"{g.tier}-tier group, run with --tier {g.tier}")
    return Selection(run, proxies, not_run, bool(only) or tier is not None or parity != "both")
