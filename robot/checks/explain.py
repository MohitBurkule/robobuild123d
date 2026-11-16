"""Explain a finding id (B8): `robot explain <id>` prints what the check means and how to act on it.

Finding ids are the machine interface; this is the human one. EXPLAIN is keyed by
id prefix (longest prefix wins, like fix_hints.DEFAULTS). The test keeps coverage
honest: every registry group and every id prefix used by the default hints table
has an entry.
"""

from __future__ import annotations

EXPLAIN = {
    "integrity.": "The part is not one closed solid (bad boolean, zero-thickness wall, or an import gone wrong). Rebuild the last feature before the failure.",
    "mass.": "The 150 g limit. mass.over is total mass, mass.may_be_over is the worst-case tolerance stack, mass.unknown a part with no mass source. Cut grams from the thickest printed part or the weapon disc.",
    "legal.": "AWS 2025 rules: 150 mm floor square footprint, 150 g, weapon restraint, radio. These are competition disqualifiers, never waive them.",
    "fit.": "A bought-in part does not fit the pocket/bore made for it (diameter band, depth, or clearance). Widen the pocket or pick a different catalogue part.",
    "interference.": "Two solids overlap that must not (static overlap, spinning part vs static, swept volume, wheel rub). Move parts apart or cut a pocket in the printed part.",
    "wiring.": "The wire router could not find a legal channel (pinched, too tight, or crossing the weapon sweep). Open a channel or reroute.",
    "wire.": "Wire-level review: clearance to rotating parts, or a render inconsistency of the route.",
    "assembly.": "The greedy take-apart search could not remove a part (assembly.blocked): something traps it. Open a slot, change the order, or split the part.",
    "disasm.": "Disassembly: a part is unreachable for service, the order is circular, or a belt must stretch too far to fit.",
    "connections.": "A declared connection (screw, glue, press) does not hold geometrically: missing mate, wrong method for the parts, or nothing to bite.",
    "fastener.": "Screw problems: too long/short, no thread to bite, head does not seat, no driver access, or the hole record is missing.",
    "fasteners.": "Screw set review: lengths, threads, access across the whole fastener list.",
    "fastener_seat.": "Screw head/thread vs the hole geometry (counterbore depth, seat angle, shank clearance).",
    "fastener_record.": "A hole was made without the fastener record the build needs (size, depth, method).",
    "drive_recess.": "The motor or screw drive (hex/phillips) has no recess to sit in.",
    "contain.": "A vulnerable part (battery, ESC, receiver) is exposed to hits or ground. Shield it or move it inboard.",
    "joints.": "Screwed-joint engineering defaults: boss wall, edge distance, thread engagement, nut traps.",
    "power.": "Power budget: tip speed, stored energy, battery peak current, runtime. Usually means the pack is too small or the weapon too heavy.",
    "physics.": "Closed-form weapon/drive/power physics (spin-up time, bite, push force). Cross-check of power.* with real motor constants.",
    "drive.": "Drivetrain performance: push force, top speed, slip current. Traction-limited or motor-limited.",
    "combat.": "Combat design rules (ground game): wedge angle, ground clearance, invertibility, self-righting.",
    "combat_ground.": "Ground-game geometry: the robot cannot get its weapon or wedge onto a standard opponent.",
    "threat.": "Adversarial failure modes (CF-*): the design loses to a class of attack it declared it must survive.",
    "electrical.": "Electrical rules: motor voltage, connector rating, cell consistency, ESC limits.",
    "mfg.": "Manufacturability of the declared process: min walls, hole sizes, tolerances the process cannot hold.",
    "dfm.": "Per-process manufacturability drafts (bed contact, tall thin walls, horizontal holes, sheet tabs, undeclared fits).",
    "printability.": "FDM limits: minimum holes, overhangs, bridges, first layer. Chamfer, reorient, or add supports.",
    "print.": "Print orientation declared vs what the geometry implies.",
    "print_orient.": "A printed part did not declare (or contradicts) its print orientation.",
    "process.": "Process steps (print, cut, turn) that the geometry contradicts.",
    "material.": "Material placement: brittle material in an impact zone, wrong grain, or a part of the wrong stock.",
    "shape.": "Shape-level rules: wall thickness, thin fins, closed cavities.",
    "wall.": "Wall below the process minimum. Thicken or declare a waiver with a reason.",
    "thickness.": "Wall below the process minimum. Thicken or declare a waiver with a reason.",
    "geom.": "Geometry sanity: tiny edges, sliver faces, near-coplanar steps, near-miss holes, off-axis faces, open shells, zero thickness.",
    "waiver.": "Waiver audit: every opt-out needs a reason and an expiry; no blanket waivers; the waiver budget caps how many one design may carry.",
    "waiver_audit.": "Same audit, group entry point: reason, expiry, budget, blanket and duplicate-reason rules.",
    "practice.": "Best-CAD-practice gates with no reference (naming, fully constrained sketches, stray geometry).",
    "spinner.": "Weapon spinner checks: balance, bearings, shaft, retention at speed.",
    "kinematics.": "Motion checks: weapon sweep, drive kinematics, declared rotation.",
    "retention.": "A rotating part is not held in both axial directions by hardware.",
    "tension.": "Belt/o-ring tensioner travel and range.",
    "belt_wrap.": "Belt wrap angle on a pulley is too small to transmit torque.",
    "ground.": "Ground interaction: clearance, approach angle, wheel contact.",
    "strength.": "Static strength: weapon shaft, bearings, uprights, pull-out. Usually fix by thickening or shortening a lever.",
    "dynamics.": "Dynamic behaviour: tip angles, invertibility, gyroscopic effects, hit reaction.",
    "support.": "The part is not supported in one of the 6 orientations (gravity on a loose part).",
    "sharp_corner.": "Sharp internal corner the process cannot resolve; add a radius or opt out with a reason.",
    "coverage.": "A declared claim (spec claims[]) has no check covering it.",
    "cots.": "Bought-in part usage: belt wrap, motor volume, port mismatches against the catalogue.",
    "bom.": "Bill of materials: lock part, O-ring stock, wire cut length, or a reference BOM difference.",
    "targets.": "The spec's own declared target dimensions do not match what was built.",
    "reference.": "Comparison with the original designer's data (photos, meshes, dumps). Never gating for a new design.",
    "reference_ratios.": "Proportions measured on reference photos (panel splits, wheelbase ratio) differ from the original.",
    "reference_cad.": "Per-part diff vs the reference CAD meshes (volume, bbox, position).",
    "ref_map.": "A built part has no entry in the reference parts index (or vice versa).",
    "cots_fidelity.": "A bought-in part was modelled differently from its catalogue/STEP data.",
    "wire_review.": "Wire-route review: clearance to rotating parts or a missing render of the route.",
    "param.": "Param lint: raw literals where a setting should be, or a dimension-count mismatch vs the reference.",
    "intent.": "A feature does not do what its design intent claims (probes of the declared intent).",
    "plausibility.": "Density/mass plausibility vs the real robot class.",
    "archetype.": "Archetype rules for the declared weapon/drive class.",
    "architecture.": "Architecture: pods enclose what they must, mounts hold their parts.",
    "internal.": "Internal layout: parts inside the shell collide or do not fit.",
    "visual.": "Visual parity with the reference mesh (silhouette/depth/fillet).",
    "sldprt_dump.": "Comparison with the SolidWorks part dumps of the original design.",
    "asm_dump.": "Comparison with the SolidWorks assembly dump (order, mates, counts).",
    "robust.": "Robustness sweep: a param or COTS swap variant failed to build or verify.",
    "harness.": "Planned wiring harness (robot/wiring): nets, connectors, service loops.",
    "thermal.": "Thermal/voltage-sag budget: the pack's voltage under peak current (nominal minus I x internal resistance) must stay above 3.3 V per cell or the receiver/ESC browns out mid-fight. Bigger pack (more mAh / lower resistance) or less peak current.",
    "impact.": "Hit reaction: gyroscopic wheel-lift when turning with a spun-up weapon (turn rate above the lift threshold rolls the robot), hop when a vertical spinner lands a hit, and yaw spin-out from a horizontal spinner. Slow the turn rate, lower the weapon speed, or widen the track.",
    "requirements.": "A requirement the user declared (speed, force, energy, budget) is not met by the design.",
    "rest.": "Dead pose: with the power cut the weapon coasts to an unknowable rest angle; if some rotation of the weapon reaches the floor the dead robot props itself on its own blade. Raise the weapon or its spin axis.",
    "clearance.": "Clearance at rest: tyres squash under the robot's weight and a loaded wedge bends down, so a belly that cleared on the bench can scrape and a wedge tip can dig in. Raise the chassis, use firmer/bigger wheels, or stiffen the wedge.",
    "service.": "Between-fight service: the battery, weapon and wheels must come out along at least one straight line without removing other parts, or a swap costs the match. Give the part an open hatch or slot.",
    "rf.": "RF placement: the receiver must sit away from motor/ESC switching noise (2.4 GHz swamps at close range) and its antenna must exit the top face without conductive material over it. Move the receiver to the far corner, cut a window in metal/carbon above it, or stand the antenna out.",
    "traction.": "Traction patch: the centre of mass must project inside the polygon of the driven wheels' floor contacts, with margin, or the first push unloads the wheels and the robot pivots. Move mass over the driven wheels or widen the stance.",
    "builder.": "Builder profile: the design does not fit the declared builder's bench - printer bed, shelf materials, processes, tools, skill or budget. Split parts, switch to stocked materials, add the tool, or raise the budget.",
    "validity.": "The spec itself is invalid (unknown part, bad placement) - fix the spec before reading other findings.",
}


def explain(fid: str) -> dict:
    """{id, prefix, text} for one finding id; longest matching prefix wins."""
    if not isinstance(fid, str) or not fid:
        return {"id": fid, "prefix": None, "text": "an empty id explains nothing"}
    best = None
    for p in EXPLAIN:
        if fid == p.rstrip(".") or fid.startswith(p):
            best = p if best is None or len(p) > len(best) else best
    if fid in EXPLAIN:
        best = fid
    return {"id": fid, "prefix": best, "text": EXPLAIN.get(best, "no explanation recorded for this id yet")}


def add_cli(sub):
    p = sub.add_parser("explain", help="what a finding id means and how to act on it")
    p.add_argument("id", help="a finding id (exact, or a prefix like mass.)")
    p.set_defaults(func=_run)


def _run(a):
    e = explain(a.id)
    print(f"{e['id']}" + (f" (matched prefix {e['prefix']})" if e["prefix"] and e["prefix"] != e["id"] else ""))
    print(f"  {e['text']}")
    return 0
