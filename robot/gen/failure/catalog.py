"""Turn hypothesis clusters into catalog entries (combat_failure_modes.json schema) and write outputs."""
from __future__ import annotations
import csv
import json
from pathlib import Path
from . import interact as I
from .ontology import ENTITIES, AGENTS, properties

T = {  # mechanism -> (measure, threshold, severity, fix, countermeasure, extends)
    "toggle_by_contact": ("For each switch: actuator axis vs each agent's sweep axis in its band; ray-cast agent cone onto actuator; actuator travel & force; recess depth below surrounding surface.",
                          "actuator recessed >= 2 mm below surface or guarded on 3 sides; actuator axis not parallel to dominant sweep (x for floor/wedge, y for hspin, z for vspin/flipper); actuation force >= 5 N", "critical",
                          "Recess the switch, orient slide axis perpendicular to likely scrape, use a removable link/pin or a guarded/covered actuator, or an electronic switch.", "recessed/guarded switch, link, electronic switch", "CF-GD06"),
    "toggle_on_handling": ("Locate actuator relative to natural grip/carry surfaces (top/side within 20 mm of CG grip zone).", "actuator not in grip zone; requires tool or deliberate push", "warning",
                           "Place switch away from carry points, require a tool/pin to arm, add a cover.", "tool-operated link", "CF-GD06"),
    "actuator_rip": ("Protrusion height of switch body/actuator above local surface; shear area of mount.", "protrusion <= 0 mm (flush) or inside a guard ring >= protrusion+1 mm", "critical",
                     "Mount the switch behind the shell wall, use a panel-mount body with a nut, add a guard boss.", "flush/guarded mount", "CF-GD06"),
    "switch_contact_bounce": ("Switch contact rating & type; shock spec (g) vs datasheet; presence of bulk capacitor at rx/ESC.", "contact rated >= 2x peak current; >= 470 uF bulk cap; switch rated for 50 g shock", "warning",
                              "Use a rated switch or link, add bulk capacitance, prefer link/electronic switch.", "link / MOSFET switch", "CF-GD06"),
    "electronic_switch_trigger": ("Hall/reed switch position vs magnets and steel floor; latching logic.", "trigger magnet path >= 20 mm from motors/floor; non-latching by field alone", "warning",
                                  "Shield or relocate the trigger, use a jumper-type electronic switch.", "jumper electronic switch", "CF-GD06"),
    "indicator_hidden": ("LED visibility cone from start-square viewpoints in upright and inverted poses.", "LED visible from top AND bottom (or through translucent shell) in any pose", "warning",
                         "Put LEDs on both faces or under a light pipe; rule-compliant visible power indicator.", "dual-sided LED", ""),
    "protrusion_shear": ("Protrusion height and base section of part above hull surface in reachable bands.", "no protrusion in reachable bands or protected by guard", "warning",
                         "Recess or guard the part; route antenna internally.", "recess", "CF-VS01"),
    "penetration_crush": ("Ray from agent cone to part through hull; sum wall thickness along ray; clearance part-to-inner wall.", "wall >= 3 mm (PLA) / 1 mm (Ti) along ray AND >= 3 mm air gap behind", "critical",
                          "Move fragile parts to the centre, add a crumple gap, stiffen the panel over it.", "standoff gap, central placement", "CF-GD03,CF-HA02"),
    "shock_dislodge": ("Retention force (friction/tape/press/glue) vs m*a for reference 200 g shock.", "retention >= 3x m*a_peak; positive mechanical retention (strap/cap/clip)", "warning",
                       "Add a positive retainer: printed cap, strap, hot glue on connectors, captive pocket.", "positive retention", "CF-GD07,CF-LD03"),
    "mass_tear_out": ("m * a_peak vs mount shear/pull-out (boss area x material shear).", "mount capacity >= 3x m*a at 200 g", "warning",
                      "Pocket heavy parts, spread load over multiple bosses.", "pocketed mounts", "CF-ST04"),
    "edge_bite": ("Face-step detection along agent cone; step height vs bite depth.", "no step >= 0.5x bite depth", "warning", "Chamfer/slope the edge, sink the part behind sloped armour.", "sloped armour", "CF-VS01"),
    "brittle_fracture": ("Material impact toughness vs face energy; layer direction.", "PLA not on impact faces; use TPU/PETG/nylon or metal facing", "warning",
                         "Change material or add metal facing.", "tough material", "CF-ST05"),
    "flex_fatigue_crack": ("Bending stress at clamp line per deflection; cycles per fight.", "stress < 0.3 UTS at max deflection; radiused clamp", "info",
                           "Radius the clamp edge, use spring steel/hinged mounts.", "radiused clamp", "CF-AS03"),
    "electrical_short": ("Live conductor exposure in reachable bands; insulation; distance to conductive skins.", "no bare live metal within 3 mm of an exposed surface; all joints heatshrunk", "critical",
                         "Insulate, heatshrink, pot joints, keep live parts inboard.", "insulation", "CF-GD02"),
    "debris_ingress": ("Gap size around moving part vs debris size 0.5-5 mm.", "gaps < 0.5 mm or > 6 mm (pass-through)", "warning",
                       "Cover the drive, use scrapers, size gaps out of jam band.", "guards/scrapers", "CF-DB01"),
    "snag_protrusion": ("Underside protrusions below ground plane offset; snag angle vs seam/screw head height.", "underside flush or edge chamfered >= 45 deg", "warning",
                        "Chamfer leading edges, recess underside features.", "chamfer", "CF-AS05"),
    "vibration_loosen": ("Threaded joints without locking (nyloc/threadlocker/insert).", "every threaded joint has locking element", "warning",
                         "Use nylocs, threadlocker, or locking inserts; witness-mark screws.", "threadlocker", ""),
    "insert_pullout": ("Insert pull-out (wall around insert, embed length) vs reference load.", "wall >= 1.5x insert OD; load path in compression", "warning",
                       "Through-bolt to nut, larger bosses, load inserts in shear not tension.", "through-bolts", "CF-ST04"),
    "screw_head_bite": ("Screw head height above surface in reachable bands.", "heads countersunk/recessed >= 0.5 mm", "warning", "Countersink/recess heads.", "recessed fasteners", "CF-VS01"),
    "thermal_overrun": ("Thermal model: I^2R and stall current x duration vs thermal limit; airflow; adjacency to heat.", "T_max < limit - 15 C over a 3 min fight incl. 60 s stall", "warning",
                        "Current-limit, heatsink, gap from heat sources, reduce pre-fight idle.", "thermal margin", "CF-GD09"),
    "stall_heat": ("Stall current x stall time when pinned/beached vs ESC/motor rating.", "ESC rating >= stall current or current limit set", "warning",
                   "Current limit, larger ESC, avoid beaching geometry.", "current limit", "CF-AR01"),
    "rf_degrade": ("Antenna position relative to conductive parts/floor in each pose; RSSI test.", "antenna >= 10 mm from metal, not shadowed in inverted pose", "warning",
                   "Route antenna away from metal & motors, vertical/diverse placement, failsafe tested.", "antenna placement", "CF-GD04"),
    "antenna_snag": ("Exposed antenna length outside hull in reachable bands.", "no exposed antenna; internal in a tube", "warning", "Route inside hull in a printed channel.", "internal antenna", "CF-GD04"),
    "lift_lose_traction": ("Wheel exposure vs get-under margins; centre of pressure.", "see CF-WL01/02 margins", "info", "Lower nose, wheel guards, drive inverted.", "invertible drive", "CF-WL01"),
    "clamp_crush": ("Shell deflection under clamp load vs internal clearance.", "deflection at 200 N < internal clearance", "warning", "Stiffen shell, add internal standoffs.", "standoffs", "CF-WL04"),
    "abrasion_cut": ("Exposed soft/wired parts in scrape bands.", "no exposed wires/tape/tyres in scrape bands", "warning", "Cover, route inside, use sleeving.", "sleeving", "CF-HA03"),
    "wire_fatigue": ("Wire flex points (hinges, solder tabs) without strain relief.", "strain relief within 10 mm of every solder joint; service loop at hinges", "warning",
                     "Add strain relief, glue at tabs, use silicone wire.", "strain relief", "CF-GD07"),
    "weapon_drive_shock": ("Shock load at weapon contact vs belt wrap/tension, press fit, shaft bending, thread lock.", "belt wrap >= 120 deg + guides; shaft bending < yield at 2x hit; threadlock on weapon fasteners", "critical",
                           "Belt guides, larger shaft, keyed/clamped pulley, bearing retaining shoulder, nyloc + threadlock on disc.", "belt guides, retained bearings", "CF-OW03,CF-OW04"),
    "inversion_effect": ("Pose analysis: inverted geometry, which faces become attack faces, gravity on loose parts.", "invertible drive, symmetrical attack faces or self-right", "warning",
                         "Design invertible or add self-righting; protect switch on both faces.", "invertible design", "CF-WL05"),
    "gyro_effect": ("Weapon angular momentum L = I*w; precession torque vs robot mass*wheelbase.", "precession torque at max turn rate < 0.5 x righting moment", "warning",
                    "Lower weapon inertia, slow turns, wider wheelbase.", "inertia/wheelbase", "CF-VS06,CF-OW02"),
    "state_exposure": ("Re-run exposure ray-casts in the given robot state/pose.", "no critical part newly reachable in the state", "warning",
                       "Make faces symmetrical, armour belly as well as top, protect the face exposed in this state.", "pose-symmetric armour", "CF-GD01"),
    "state_helpless": ("Mobility in degraded state (one side, failsafe, brownout).", "can still escape a wall in degraded state", "info", "Redundant drive, failsafe test, voltage margin.", "redundancy", "CF-GD05"),
    "wire_entangle": ("Distance from wire routing to rotating parts.", ">= 5 mm with physical barrier", "critical", "Route wires away, clip/channel them, add barrier.", "wire channels", "CF-GD08"),
    "heat_coupling": ("Distance & conduction path from heat source to sensitive part.", ">= 5 mm air gap or insulating barrier", "warning", "Separate, add barrier or airflow.", "thermal isolation", "CF-GD09"),
    "magnetic_interference": ("Distance from rx/antenna to motors/metal.", ">= 15 mm from motors; antenna not inside metal enclosure", "warning", "Relocate receiver, shield, route antenna out.", "separation", "CF-GD04"),
    "self_toggle": ("Distance and line-of-sight between switch actuator and own rotating part (wheel/belt).", "no line of sight within 10 mm", "critical", "Move switch, add a wall between wheel and switch.", "barrier", "CF-GD06"),
    "internal_puncture": ("Hard edges/screws pointing at fragile parts within deflection distance.", "clearance >= expected shell deflection + 2 mm", "critical", "Pad, reposition screws, cover tips.", "padding", "CF-GD03"),
    "internal_short": ("Live terminals vs conductive structure within 3 mm.", "insulated or >= 3 mm", "critical", "Insulate, reroute.", "insulation", "CF-GD02"),
    "stray_access": ("Wire/connector paths across lid closure plane.", "no wire crosses the lid seal plane un-channelled", "warning", "Wire channel, lid relief.", "channels", ""),
    "post_impact_jam": ("Running clearance between moving part and nearest static structure vs plastic set after a reference 20 J hit: delta = f(material E, yield, wall t, span) from B-rep thickness.", "clearance >= 2x predicted plastic deflection", "critical",
                        "Clearance margin, stiff backing behind guards, sacrificial crumple zones away from moving parts, floating guards.", "clearance margin, floating guards", "CF-DB01,CF-DB02"),
    "cracked_flap_drag": ("Panel crack paths near wheels; fragment hinged to body.", "panel splits away clean or is bonded with no flap", "warning", "Reinforce near wheel cut-outs, split lines away from tyres.", "split lines", "CF-ST02"),
}


def entry(c):
    m, th, sev, fix, cm, ext = T[c["mechanism"]]
    cov = I.coverage(c)
    return dict(
        id=c["id"], group=c["entity_label"], entity=c["entity"], state=c["state"], name=c["titles"][0][:140] + (f" (+{len(c['agents'])-1} other agents)" if len(c["agents"]) > 1 else ""),
        cause=", ".join(a for a in c["agents"]), mechanism=c["mechanism"] + (": " + c["detail"] if c.get("detail") else "")
        + " | " + I.STATES[c["state"]]["desc"],
        measure=m, threshold=th, severity=sev, fix=fix, countermeasure=cm, fight_impact=max(1, min(5, round(1 + c["rank"] * 8))),
        extends=ext, rank=c["rank"], likelihood=c["likelihood"], loses=c["loses"],
        status=("covered_by " + cov) if cov else "NEW", reasoning=f"{c['family']} rule {c['mechanism']} fired for {len(c['agents'])} agent(s); "
        f"criticality {c['crit']}; state {c['state']}", variants=c["titles"][:6], cascade=c.get("cascade", []))


def build(out_dir="/mnt/project-files/robot-cad/research"):
    raw = I.generate()
    cl = I.cascades(I.cluster(raw))
    entries = [entry(c) for c in cl]
    new = [e for e in entries if e["status"] == "NEW"]
    ep, ap = properties()
    eap, eep = I.raw_pairs()
    stats = dict(entities=len(ENTITIES), agents=len(AGENTS), states=len(I.STATES), entity_props=len(ep), agent_props=len(ap),
                 rules=len(I.RULES), raw_pairs_entity_agent_state=eap, raw_pairs_entity_entity=len(ENTITIES) * (len(ENTITIES) - 1),
                 raw_pairs_property=eap * len(ep) * len(ap), raw_hypotheses=len(raw), clusters=len(entries), new=len(new),
                 covered=len(entries) - len(new))
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    (out / "combat_failure_modes_ext.json").write_text(json.dumps(dict(stats=stats, modes=entries), indent=1))
    # matrix
    agents = [a.kind for a in AGENTS] + ["internal"]
    cnt = {}
    for h in raw:
        a = "internal" if h["agent"].startswith("internal:") else h["agent"]
        cnt[(h["entity"], a)] = cnt.get((h["entity"], a), 0) + 1
    with open(out / "combat_failure_modes_ext_matrix.csv", "w", newline="") as f:
        w = csv.writer(f)
        w.writerow(["entity"] + agents)
        for e in ENTITIES:
            w.writerow([e.kind] + [cnt.get((e.kind, a), 0) for a in agents])
    # markdown
    L = ["# Combat failure modes - extended (generated)", "",
         "Generated by `robot/gen/failure` (ontology x mechanism rules x robot state, plus internal entity x entity and post-impact deformation).", "",
         "## Stats", ""] + [f"- {k}: {v}" for k, v in stats.items()] + ["", "## Top 30 NEW by rank", ""]
    for e in new[:30]:
        L.append(f"- **{e['id']}** ({e['rank']}) [{e['state']}] {e['name']}")
    L += ["", "## NEW by entity", ""]
    for ent in ENTITIES:
        items = [e for e in new if e["entity"] == ent.kind]
        if not items:
            continue
        L += [f"### {ent.label} (`{ent.kind}`) - {len(items)}", ""]
        for e in items:
            L.append(f"- **{e['id']}** `{e['mechanism'].split(':')[0].split(' |')[0]}` [{e['state']}] sev={e['severity']} rank={e['rank']}: {e['name']}")
            L.append(f"  - cause: {e['cause'][:200]}")
            L.append(f"  - measure: {e['measure']} | threshold: {e['threshold']}")
            L.append(f"  - fix: {e['fix']} (extends {e['extends'] or '-'})")
            L.append(f"  - reasoning: {e['reasoning']}")
            if e["cascade"]:
                L.append(f"  - cascade: {e['cascade'][0]['text']} (p={e['cascade'][0]['likelihood']})")
        L.append("")
    L += ["## Covered by existing catalog", ""] + [f"- {e['id']} -> {e['status']}: {e['name']}" for e in entries if e["status"] != "NEW"]
    (out / "combat_failure_modes_ext.md").write_text("\n".join(L) + "\n")
    return stats, entries


if __name__ == "__main__":
    s, es = build()
    print(json.dumps(s, indent=1))
    for e in [x for x in es if x["status"] == "NEW"][:20]:
        print(e["id"], e["rank"], e["state"], e["name"])
