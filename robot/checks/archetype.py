"""Robot archetypes: a spec may declare `archetype` (e.g. "vertical_spinner_forks") and is then held to the layout rules
that real robots of that kind share (disc between two forks, blades ahead of the disc, disc close to the floor, ...).

Structure: `facts(ctx)` measures everything once into a plain dict (None = could not be measured); each rule in `RULES`
is a pure function `(facts, params) -> (passed | None, message)`. `ARCHETYPES` lists the rules and default parameters of
each archetype; `archetype_params` in the spec overrides any parameter (e.g. ranges read off photos of the real robot).
Fail-closed: a rule whose facts are missing becomes a WARNING finding plus a NOT CHECKED line, never a silent pass.
A spec without `archetype` gets no findings from this group.
"""

from __future__ import annotations

import math

import numpy as np

from .. import catalog, measure, xform
from ..finding import BLOCKER, WARNING, fail, note, ok
from . import _physics as ph
from .power import rim_radius, spin_axis

G = "archetype"
SUPPORT = ("structure", "plate", "fork", "armor", "bearing")
CHASSIS = ("structure", "armor", "plate", "wedge")
METAL_PROCESSES = ("laser", "waterjet", "milled", "turned", "cnc", "lathe", "sheet", "sheet_bent", "machined", "cots", "edm", "cut")
X, Y, Z = np.eye(3)

# ------------------------------------------------------------------------------------------------------------- rules
# Each entry: id -> (severity on failure, title, fix hint, fn). fn(F, P) -> (True/False/None, message).


def _rng(v, lo_hi, unit, what):
    lo, hi = lo_hi
    good = (lo is None or v >= lo) and (hi is None or v <= hi)
    lim = f"{'' if lo is None else f'{lo:g}'}..{'' if hi is None else f'{hi:g}'} {unit}"
    return good, f"{what} is {v:.1f} {unit} (wanted {lim})."


def r_disc_plane_vertical(F, P):
    a = F.get("axis")
    if a is None:
        return None, "no spinning weapon with a spin axis"
    tilt = math.degrees(math.asin(min(1.0, abs(a[2]))))
    return tilt <= P["axis_tol_deg"], f"The spin axis is {tilt:.1f} deg out of the horizontal plane (vertical disc needs a horizontal axle, tol {P['axis_tol_deg']:g} deg)."


def r_disc_plane_horizontal(F, P):
    a = F.get("axis")
    if a is None:
        return None, "no spinning weapon with a spin axis"
    tilt = math.degrees(math.acos(min(1.0, abs(a[2]))))
    return tilt <= P["axis_tol_deg"], f"The spin axis is {tilt:.1f} deg off vertical (horizontal blade needs a vertical axle, tol {P['axis_tol_deg']:g} deg)."


def r_axle_lateral(F, P):
    a = F.get("axis")
    if a is None:
        return None, "no spinning weapon with a spin axis"
    off = math.degrees(math.acos(min(1.0, abs(a[0]))))
    return off <= P["axis_tol_deg"], f"The axle points {off:.1f} deg away from the left-right (X) axis (tol {P['axis_tol_deg']:g} deg)."


def r_rotor_joint(F, P):
    j = F.get("rotor_joint")
    if j is None:
        return None, "no spinning weapon"
    good, why = j
    return good, why


def r_rotor_fasteners(F, P):
    bad = F.get("rotor_fasteners")
    if bad is None:
        return None, "no spinning weapon"
    if bad:
        return False, "Fasteners join the spinning rotor to static parts: " + "; ".join(bad) + "."
    return True, "No fastener joins the rotor to a static part or passes through its swept volume."


def r_disc_supported(F, P):
    s = F.get("supports")
    if s is None:
        return None, "no spinning weapon with a spin axis"
    a, b = s
    return (a and b), f"Static structure on the axle line: {'yes' if a else 'NO'} on one side, {'yes' if b else 'NO'} on the other (the disc must sit between two supports)."


def r_wedgelets_flank(F, P):
    w = F.get("wedgelets")
    if w is None:
        return None, "no spinning weapon"
    left, right = w
    return (left and right), f"Wedge/blade parts ahead of the disc axle: {'present' if left else 'MISSING'} on -X side, {'present' if right else 'MISSING'} on +X side."


def r_blade_lead(F, P):
    bad = F.get("blade_lead_bad")
    if bad:
        return False, f"Non-ground-game parts ahead of the disc's swept front ({', '.join(bad[:4])}); only low forks/wedgelets/skirts may lead it."
    v = F.get("blade_lead_mm")
    if v is None:
        return None, "needs both a disc and low fork/wedgelet parts"
    return _rng(v, P["blade_lead_mm"], "mm", "Low forks/wedgelets lead the disc's swept front by")


def r_disc_floor_gap(F, P):
    v = F.get("disc_floor_gap_mm")
    if v is None:
        return None, "no spinning weapon or floor"
    return _rng(v, P["disc_floor_gap_mm"], "mm", "The swept disc's lowest point above the floor")


def r_weapon_drive(F, P):
    d = F.get("weapon_drive")
    if d is None:
        return None, "no weapon motor named in `weapon.motor`"
    acc = tuple(P["weapon_drive"])
    good = d in acc or (d == "motor_is_hub" and "inside_hub" in acc)  # the bell carrying the blades is a hub drive
    return good, f"Weapon drive is `{d}` (accepted: {', '.join(P['weapon_drive'])})."


def r_disc_material(F, P):
    m = F.get("disc_material")
    if m is None:
        return None, "weapon has no known material"
    cls, proc, mid = m
    good = cls == "metal" and (proc is None or catalog.process_canon(proc) in METAL_PROCESSES or proc in METAL_PROCESSES)
    return good, f"Disc is `{mid}` ({cls}) made by `{proc}`; it must be sheet- or bar-stock metal (laser/waterjet/milled/turned)."


def r_teeth(F, P):
    t = F.get("teeth")
    if t is None:
        return None, "no spinning weapon"
    lo, hi = P["teeth"]
    return lo <= t <= hi, f"The weapon outline has {t} tooth/teeth (wanted {lo}..{hi}); a round edge skids off armour."


def r_weapon_mass_fraction(F, P):
    v = F.get("weapon_mass_fraction")
    if v is None:
        return None, "weapon or total mass unknown (mass group)"
    lo, hi = P["weapon_mass_fraction"]
    return lo <= v <= hi, f"Rotating mass is {100 * v:.0f} % of the robot (wanted {100 * lo:.0f}..{100 * hi:.0f} %)."


def r_energy_ratio(F, P):
    v = F.get("energy_j_per_kg")
    if v is None:
        return None, "stored energy or total mass unknown (power group)"
    return _rng(v, P["energy_j_per_kg"], "J/kg", "Stored energy per robot mass")


def r_drive_config(F, P):
    d = F.get("drive")
    if d is None:
        return None, "no wheels"
    n, driven, wedge_floor = d
    if n >= 4 and driven >= 4:
        return "4wd" in P["drive"], f"{n} wheels, {driven} driven (4WD)."
    if n >= 2 and driven >= 2 and "2wd_wedge" in P["drive"]:
        if wedge_floor is None:
            return None, "2WD needs a wedge resting on the floor and there is no wedge to measure"
        good = wedge_floor <= P["wedge_floor_gap_mm"][1]
        return good, f"{n} wheels, {driven} driven; the wedge lip is {wedge_floor:.1f} mm off the floor (2WD needs it as the third contact)."
    return False, f"{n} wheels, {driven} driven; accepted layouts: {', '.join(P['drive'])}."


def r_invertible(F, P):
    v = F.get("invert")
    if v is None:
        return None, "no wheels"
    declared, proud = v
    if declared:
        return True, "`can_run_inverted` is declared (the ground group proves it)."
    return proud >= P["wheel_proud_mm"], f"Wheel tops stand {proud:+.1f} mm relative to the top of the chassis (need >= {P['wheel_proud_mm']:g} mm to drive inverted)."


def r_top_armour_slope(F, P):
    v = F.get("top_slope_deg")
    if v is None:
        return None, "no armour/plate part on top"
    return _rng(v, P["top_slope_deg"], "deg", "The top armour slopes down toward the weapon at")


def r_pods_enclose(F, P):
    v = F.get("pods_missing")
    if v is None:
        return None, "no wheels"
    if v:
        return False, "Nothing outboard of wheel(s) " + ", ".join(f"`{x}`" for x in v) + " (side pods must wrap the wheels)."
    return True, "Every wheel has a side pod or wall outboard of it."


def r_floor_ribs(F, P):
    v = F.get("floor")
    if v is None:
        return None, "no printed chassis tub"
    skin, rib = v
    if skin >= P["floor_skin_mm"]:
        return True, f"Floor is {skin:.1f} mm solid (no ribs needed above {P['floor_skin_mm']:g} mm)."
    return rib >= P["rib_height_mm"], f"Floor skin {skin:.1f} mm with ribs standing {rib:.1f} mm above it (a thin printed floor needs an X-rib >= {P['rib_height_mm']:g} mm)."


def r_lid_inserts(F, P):
    v = F.get("lid_bad")
    if v is None:
        return None, "no removable lid fasteners"
    if v:
        return False, "Removable lid screws bite straight into print (no insert or nut): " + ", ".join(f"`{x}`" for x in v) + "."
    return True, "Every removable lid screw threads into an insert or nut."


def r_switch_access(F, P):
    v = F.get("switch_access")
    if v is None:
        return None, "no switch part"
    if v == "side":
        return True, "The switch can be reached from the side."
    if v in ("top", "rear"):
        return "warn", f"The switch is reachable only from the {v}; the archetype puts it on a side wall."
    return False, "Nothing reaches the switch: every direction out of it is covered by another part."


def r_wedge_floor_gap(F, P):
    v = F.get("wedge_floor_gap_mm")
    if v is None:
        return None, "no wedge"
    return _rng(v, P["wedge_floor_gap_mm"], "mm", "The wedge lip above the floor")


def r_wedge_angle(F, P):
    v = F.get("wedge_angle_deg")
    if v is None:
        return None, "no wedge"
    return _rng(v, P["wedge_angle_deg"], "deg", "The wedge face rises at")


def r_wedge_width(F, P):
    v = F.get("wedge_width_frac")
    if v is None:
        return None, "no wedge"
    lo = P["wedge_width_frac"]
    return v >= lo, f"Wedge spans {100 * v:.0f} % of the robot width (wanted >= {100 * lo:.0f} %)."


def r_weapon_leads(F, P):
    v = F.get("weapon_lead_mm")
    if v is None:
        return None, "no spinning weapon"
    return _rng(v, P["weapon_lead_mm"], "mm", "The weapon's swept front leads the rest of the robot by")


def r_drum_width(F, P):
    v = F.get("drum_width_frac")
    if v is None:
        return None, "no spinning weapon"
    lo = P["drum_width_frac"]
    return v >= lo, f"Drum is {100 * v:.0f} % of the robot width (wanted >= {100 * lo:.0f} %)."


def r_arm_actuated(F, P):
    v = F.get("arm")
    if v is None:
        return None, "no jointed arm"
    aid, actuator, _ = v
    return actuator is not None, f"Arm `{aid}` is driven by {f'`{actuator}`' if actuator else 'NOTHING (no actuated_by, servo or weapon motor)'}."


def r_arm_range(F, P):
    v = F.get("arm")
    if v is None:
        return None, "no jointed arm"
    aid, _, rng = v
    return rng >= P["arm_range_deg"], f"Arm `{aid}` travels {rng:.0f} deg (wanted >= {P['arm_range_deg']:g})."


def _param_rule(key, fact, unit, what):
    def fn(F, P):
        if P.get(key) is None:
            return True, f"{what}: no target declared."
        v = F.get(fact)
        if v is None:
            return None, f"{what} cannot be measured"
        return _rng(v, P[key], unit, what)
    return fn


RULES = {
    "disc_plane_vertical": (BLOCKER, "Disc spins in a vertical plane", "Rotate the weapon so its `weapon.spin_axis` is horizontal.", r_disc_plane_vertical),
    "disc_plane_horizontal": (BLOCKER, "Blade spins in a horizontal plane", "Rotate the weapon so its spin axis is vertical.", r_disc_plane_horizontal),
    "axle_lateral": (BLOCKER, "Axle runs left-right", "Turn the axle to run across the robot (X).", r_axle_lateral),
    "rotor_joint": (BLOCKER, "Rotor has a spinning joint", "Give the disc (or its hub/carrier) a `joint` of kind revolute about the spin axis, parented to the static support; do not parent it rigidly to a fork.", r_rotor_joint),
    "rotor_fasteners": (BLOCKER, "No screw ties rotor to stator", "Screws in the disc may only join rotor parts (disc, hub, bell); move screws that reach static parts out of the swept volume.", r_rotor_fasteners),
    "disc_supported": (BLOCKER, "Disc sits between two supports", "Put a fork or bearing block on each side of the disc on the axle line.", r_disc_supported),
    "wedgelets_flank": (WARNING, "Blades either side of the disc", "Add a wedgelet/blade on each side of the disc reaching ahead of the axle.", r_wedgelets_flank),
    "blade_lead": (WARNING, "Blade tips just ahead of the disc", "Lengthen/shorten the blades or move the axle so the tips lead the tooth sweep by the target.", r_blade_lead),
    "disc_floor_gap": (BLOCKER, "Disc sweeps close to the floor", "Lower the axle or enlarge the disc so the swept edge is within the range above the floor.", r_disc_floor_gap),
    "weapon_drive": (WARNING, "Weapon drive layout", "Put the outrunner inside the hub, or belt-drive with a tensioner.", r_weapon_drive),
    "disc_material": (BLOCKER, "Disc is metal stock", "Cut the disc from steel/titanium/aluminium sheet or turn it from bar.", r_disc_material),
    "teeth": (WARNING, "Weapon has teeth", "Give the outline 1-2 hooked teeth (balanced).", r_teeth),
    "weapon_mass_fraction": (WARNING, "Weapon mass share", "Move mass into (or out of) the rotor until it is within the range.", r_weapon_mass_fraction),
    "energy_ratio": (WARNING, "Weapon energy for its size", "Heavier rim, bigger diameter or more speed (within tip-speed limits).", r_energy_ratio),
    "drive_config": (WARNING, "Drive layout", "Drive all four wheels, or two with the wedge as the third contact.", r_drive_config),
    "invertible": (WARNING, "Drives upside down", "Make the wheels stand proud of the top (or declare and prove `can_run_inverted`).", r_invertible),
    "top_armour_slope": (WARNING, "Top armour slopes to the weapon", "Bend the front of the top plate down toward the weapon (about 20-25 deg).", r_top_armour_slope),
    "pods_enclose_wheels": (WARNING, "Side pods wrap the wheels", "Add side pods/walls outboard of each wheel.", r_pods_enclose),
    "floor_ribs": (WARNING, "Printed floor is stiffened", "Add an X-rib (corner to corner, ~3 mm wide) or thicken the floor.", r_floor_ribs),
    "lid_inserts": (WARNING, "Lid screws go into inserts", "Fit heat-set inserts (or captive nuts) where removable lid screws go into print.", r_lid_inserts),
    "switch_access": (BLOCKER, "Switch reachable from the side", "Put the switch in a side-wall slot with nothing outboard of it.", r_switch_access),
    "wedge_floor_gap": (WARNING, "Wedge lip near the floor", "Lower the wedge lip to within the range above the floor.", r_wedge_floor_gap),
    "wedge_angle": (WARNING, "Wedge angle", "Set the wedge face to the archetype range.", r_wedge_angle),
    "wedge_width": (WARNING, "Wedge covers the front", "Widen the wedge across the front.", r_wedge_width),
    "weapon_leads": (WARNING, "Weapon leads the front", "Move the weapon forward or cut the front back.", r_weapon_leads),
    "drum_width": (WARNING, "Drum is wide", "Widen the drum.", r_drum_width),
    "arm_actuated": (BLOCKER, "Arm has an actuator", "Name the servo/motor in `actuated_by` (or add one).", r_arm_actuated),
    "arm_range": (WARNING, "Arm travel", "Increase the joint range.", r_arm_range),
    "axle_height": (WARNING, "Axle height on target", "Move the axle to the target height.", _param_rule("axle_height_mm", "axle_height_mm", "mm", "Axle centre above the floor")),
    "disc_thickness": (WARNING, "Disc thickness on target", "Change the disc thickness.", _param_rule("disc_thickness_mm", "disc_thickness_mm", "mm", "Disc thickness")),
    "disc_diameter": (WARNING, "Disc diameter on target", "Change the disc diameter.", _param_rule("disc_dia_mm", "disc_dia_mm", "mm", "Disc diameter (incl. tooth)")),
    "tub_height": (WARNING, "Tub height on target", "Change the tub height.", _param_rule("tub_height_mm", "tub_height_mm", "mm", "Chassis tub height")),
    "wheel_dia": (WARNING, "Wheel size on target", "Change the wheel diameter.", _param_rule("wheel_dia_mm", "wheel_dia_mm", "mm", "Largest wheel diameter")),
    "wheel_count": (WARNING, "Wheel count on target", "Add or remove wheels.", _param_rule("wheels", "wheel_count", "", "Number of wheels")),
}

COMMON = {"axis_tol_deg": 5.0, "wedge_floor_gap_mm": (0.0, 1.5), "wheel_proud_mm": 0.5, "floor_skin_mm": 2.5, "rib_height_mm": 1.0,
          "top_slope_deg": (10.0, 35.0), "teeth": (1, 3), "energy_j_per_kg": (40.0, 600.0), "drive": ("4wd", "2wd_wedge"),
          "weapon_drive": ("inside_hub", "belt_tensioned"), "axle_height_mm": None, "disc_thickness_mm": None, "disc_dia_mm": None,
          "tub_height_mm": None, "wheel_dia_mm": None, "wheels": None}
_SPIN_COMMON = ["rotor_joint", "rotor_fasteners", "disc_supported", "disc_material", "teeth", "weapon_mass_fraction", "energy_ratio"]
_TAIL = ["drive_config", "invertible", "pods_enclose_wheels", "floor_ribs", "lid_inserts", "switch_access",
         "axle_height", "disc_thickness", "disc_diameter", "tub_height", "wheel_dia", "wheel_count"]

ARCHETYPES = {
    "vertical_spinner_forks": (["disc_plane_vertical", "axle_lateral"] + _SPIN_COMMON + ["wedgelets_flank", "blade_lead", "disc_floor_gap",
                               "weapon_drive", "top_armour_slope"] + _TAIL,
                               {"blade_lead_mm": (5.0, 15.0), "disc_floor_gap_mm": (0.3, 4.0), "weapon_mass_fraction": (0.20, 0.50)}),
    "drum": (["disc_plane_vertical", "axle_lateral"] + _SPIN_COMMON + ["disc_floor_gap", "drum_width", "weapon_leads", "weapon_drive"] + _TAIL,
             {"disc_floor_gap_mm": (0.3, 4.0), "weapon_mass_fraction": (0.20, 0.50), "drum_width_frac": 0.3, "weapon_lead_mm": (2.0, None),
              "teeth": (1, 6), "weapon_drive": ("inside_hub", "belt_tensioned", "direct")}),
    "horizontal_spinner": (["disc_plane_horizontal"] + _SPIN_COMMON + ["weapon_leads", "disc_floor_gap"] + _TAIL,
                           {"disc_floor_gap_mm": (0.5, 25.0), "weapon_mass_fraction": (0.20, 0.45), "weapon_lead_mm": (3.0, None),
                            "weapon_drive": ("inside_hub", "belt_tensioned", "direct")}),
    "wedge_2wd": (["wedge_floor_gap", "wedge_angle", "wedge_width"] + _TAIL,
                  {"wedge_angle_deg": (12.0, 40.0), "wedge_width_frac": 0.8, "drive": ("2wd_wedge", "4wd")}),
    "flipper": (["arm_actuated", "arm_range", "wedge_floor_gap"] + _TAIL, {"arm_range_deg": 60.0, "wedge_floor_gap_mm": (0.0, 2.0)}),
    "lifter": (["arm_actuated", "arm_range", "wedge_floor_gap"] + _TAIL, {"arm_range_deg": 30.0, "wedge_floor_gap_mm": (0.0, 2.0)}),
    "hammer": (["arm_actuated", "arm_range"] + _TAIL, {"arm_range_deg": 150.0}),
}
ARCHETYPES["wedge"] = ARCHETYPES["wedge_2wd"]
ARCHETYPES["vertical_spinner"] = ARCHETYPES["vertical_spinner_forks"]


def params_for(name, override=None):
    rules, own = ARCHETYPES[name]
    P = dict(COMMON)
    P.update(own)
    for k, v in (override or {}).items():
        P[k] = tuple(v) if isinstance(v, list) else v
    return rules, P


def evaluate(name, F, override=None):
    """Run every rule of an archetype over measured facts. Returns [(rule_id, passed True/False/'warn'/None, message)]."""
    rules, P = params_for(name, override)
    return [(rid, *RULES[rid][3](F, P)) for rid in rules]


# ------------------------------------------------------------------------------------------------------------- facts


def _ancestors(spec, pid):
    seen, out = set(), []
    p = spec.part(pid)
    while p is not None and p.parent and p.parent not in seen:
        seen.add(p.parent)
        out.append(p.parent)
        p = spec.part(p.parent)
    return out


def _descendants(spec, pid):
    out, todo = set(), [pid]
    while todo:
        c = todo.pop()
        for p in spec.parts:
            if p.parent == c and p.id not in out:
                out.add(p.id)
                todo.append(p.id)
    return out


def rotor_set(spec, wid):
    """Parts that turn with the weapon: the weapon, its hub(s), children, fused or rigidly connected parts."""
    rot = {wid}
    changed = True
    while changed:
        changed = False
        for p in spec.parts:
            if p.id in rot:
                continue
            j = p.joint is not None
            if (p.parent in rot and not j) or (p.fused_with in rot):
                rot.add(p.id)
                changed = True
        for c in spec.connections:
            if c.method in ("shaft", "bearing", "spin", "slip"):
                continue
            for a, b in ((c.a, c.b), (c.b, c.a)):
                pb = spec.part(b)
                if a in rot and b not in rot and pb is not None and pb.kind in ("hub", "pulley", "weapon"):
                    rot.add(b)
                    changed = True
    for p in spec.parts:  # a hub sitting on the weapon (same parent, overlapping) turns with it
        if p.kind == "hub":
            rot.add(p.id)
    return rot


def _floor(ctx):
    r, w = ctx.r, ctx.world
    if r.spec.ground_z is not None:
        return float(r.spec.ground_z)
    if "ground_z" in ctx.metrics:
        return float(ctx.metrics["ground_z"])
    zs = [float(b.aabb[0][2]) for b in w.bodies if not b.fastener and not b.is_wire]
    return min(zs) if zs else None


def _teeth(pts, origin, axis):
    u = np.cross(axis, Z if abs(axis[2]) < 0.9 else X)
    u /= np.linalg.norm(u)
    v = np.cross(axis, u)
    q = pts - origin
    ang = np.arctan2(q @ v, q @ u)
    rad = np.hypot(q @ u, q @ v)
    nb = 72
    idx = ((ang + math.pi) / (2 * math.pi) * nb).astype(int) % nb
    prof = np.full(nb, np.nan)
    for k in range(nb):
        m = idx == k
        if m.any():
            prof[k] = rad[m].max()
    if np.isnan(prof).all():
        return 0
    good = ~np.isnan(prof)
    k = np.arange(nb)
    prof = np.interp(k, np.concatenate([k[good] - nb, k[good], k[good] + nb]), np.tile(prof[good], 3))
    lo, hi = float(prof.min()), float(prof.max())
    if hi - lo < 2.0:
        return 0
    up = prof > lo + 0.6 * (hi - lo)
    if up.all():
        return 0
    k0 = int(np.argmin(up))  # start at a gap so runs do not wrap
    runs, prev = 0, False
    for k in range(nb):
        cur = bool(up[(k0 + k) % nb])
        if cur and not prev:
            runs += 1
        prev = cur
    return runs


def _bell_carries(spec, mid, rotor):
    """True when a rotor part (blade or spider) is bolted/pinned/pressed straight onto the motor (its bell): motor-as-hub."""
    if any(getattr(p, "_extra", {}).get("shaft_of") == mid or getattr(p, "_extra", {}).get("drive") == "motor_is_hub"
           for p in spec.parts if p.id in rotor):
        return True
    for c in spec.connections:
        pair = {c.a, c.b}
        if mid in pair and (pair - {mid}) & rotor and c.method not in ("shaft", "bearing", "belt"):
            reason = (getattr(c, "reason", None) or "").lower()
            if not any(w in reason for w in ("oldham", "flexible coupl", "jaw coupl")):
                return True
    return False


def _part(r, pid):
    return next((rp for rp in r.parts if rp.part.id == pid), None)


def _slope_deg(verts, front_frac=0.35):
    """Downward slope (deg) of a part's top surface over its front `front_frac` of length (positive = falls toward +Y)."""
    y0, y1 = float(verts[:, 1].min()), float(verts[:, 1].max())
    if y1 - y0 < 2.0:
        return None
    bins = np.linspace(y0, y1, 25)
    ys, zs = [], []
    for a, b in zip(bins[:-1], bins[1:]):
        m = (verts[:, 1] >= a) & (verts[:, 1] <= b)
        if m.any():
            ys.append((a + b) / 2)
            zs.append(float(verts[m, 2].max()))
    ys, zs = np.array(ys), np.array(zs)
    sel = ys >= y1 - front_frac * (y1 - y0)
    if sel.sum() < 2:
        return None
    k = np.polyfit(ys[sel], zs[sel], 1)[0]
    return math.degrees(math.atan(-k))


def facts(ctx) -> dict:
    r, w = ctx.r, ctx.world
    spec = r.spec
    F = {}
    floor = _floor(ctx)
    solid = [b for b in w.bodies if not b.is_wire]
    if solid:
        lo = np.min([b.aabb[0] for b in solid], 0)
        hi = np.max([b.aabb[1] for b in solid], 0)
        F["width"] = float(hi[0] - lo[0])
    weapon_i = None
    for i, b in enumerate(w.bodies):
        if b.part_idx is not None and b.kind == "weapon" and spin_axis(w, r, i) is not None:
            weapon_i = i
            break
    rotor, assembly = set(), set()
    if weapon_i is not None:
        wb = w.bodies[weapon_i]
        wid = wb.id
        wpart = spec.part(wid)
        origin, axis = spin_axis(w, r, weapon_i)
        F["axis"] = axis
        rotor = rotor_set(spec, wid)
        anc = _ancestors(spec, wid)
        assembly = set(rotor) | set(anc)
        for a in anc:
            assembly |= _descendants(spec, a)
        if wpart.weapon and wpart.weapon.motor:
            assembly.add(wpart.weapon.motor)
        rbodies = [w.body(x) for x in rotor if w.body(x) is not None]
        pts = np.vstack([b.mesh.vertices for b in rbodies])
        R = rim_radius(wb, origin, axis)
        half = float(np.abs((wb.mesh.vertices - origin) @ axis).max())
        rhalf = float(np.abs((pts - origin) @ axis).max())  # whole rotor (disc + hub) half width
        F["disc_dia_mm"] = 2 * R
        # Disc thickness = the blade stack (e.g. 3 x 2-3 mm Hardox plates) only: the motor, spider, hub and shaft that ride
        # with the rotor are not "disc". Falls back to the weapon body alone.
        bs = ph.blade_stack(ctx, rotor, origin, axis)
        F["disc_thickness_mm"] = bs if bs is not None else 2 * half
        # spinning joint on the weapon or a rotor part, about the spin axis
        jgood, jwhy = False, f"`{wid}` and its rotor parts ({', '.join(sorted(rotor))}) have no revolute joint; the disc is rigidly part of `{anc[0] if anc else 'the chassis'}`."
        for pid in rotor:
            p = spec.part(pid)
            if p.joint is None or p.joint.kind != "revolute":
                continue
            par = w.body(p.parent) if p.parent else None
            ja = xform.norm(xform.apply_dir(par.M, np.asarray(p.joint.axis, float))) if par is not None else xform.norm(np.asarray(p.joint.axis, float))
            if abs(float(ja @ axis)) > 0.98:
                jgood, jwhy = True, f"`{pid}` has a revolute joint about the spin axis."
            else:
                jwhy = f"`{pid}` has a revolute joint but its axis is not the spin axis."
        F["rotor_joint"] = (jgood, jwhy)
        # fasteners that mix rotor and static parts, or sit in the swept volume while gripping a static part
        bad = []
        for f in spec.fasteners:
            touched = set(f.through or []) | ({f.threads_into} if f.threads_into else set())
            mot = {wpart.weapon.motor} if wpart.weapon and wpart.weapon.motor else set()
            for t in list(touched):  # a nut or insert inside the swept volume rides with the rotor
                tp, tb = spec.part(t), w.body(t)
                if tp is not None and tp.kind in ("nut", "insert") and tb is not None:
                    q = tb.center - origin
                    if abs(float(q @ axis)) <= rhalf + 0.5 and float(np.linalg.norm(q - (q @ axis) * axis)) < R:
                        mot = mot | {t}
            rt, st = touched & rotor, touched - rotor - mot  # an outrunner's bell turns with the rotor: bolting to it is fine
            fb = w.body(f.id)
            in_sweep = False
            if fb is not None:
                q = fb.mesh.vertices - origin
                ax = q @ axis
                rad = np.linalg.norm(q - np.outer(ax, axis), axis=1)
                in_sweep = bool(np.any((np.abs(ax) < half - 0.2) & (rad < R - 0.2)))
            if rt and st:
                bad.append(f"`{f.id}` joins {', '.join(sorted(rt))} to {', '.join(sorted(st))}")
            elif in_sweep and st:
                bad.append(f"`{f.id}` (into {', '.join(sorted(st))}) passes through the disc's swept volume")
        F["rotor_fasteners"] = bad
        # supports either side on the axle line
        sup = [b for b in w.bodies if not b.fastener and not b.is_wire and b.id not in rotor and b.kind in SUPPORT]
        # sample a ring around the axle line (the axle itself sits in a hole), from the rotor's face outward
        u = np.cross(axis, Z if abs(axis[2]) < 0.9 else X)
        u /= np.linalg.norm(u)
        v = np.cross(axis, u)
        ring = np.array([rr * (math.cos(t) * u + math.sin(t) * v) for rr in (0.0, 3.5, 5.0) for t in np.linspace(0, 2 * math.pi, 8, endpoint=False)])
        sides = []
        # reach per side from the rotor's own face: a shaft tail (e.g. the motor shaft running on into the far bearing) is
        # not rotor face and would push the sampling past the upright
        nsh = [b for b in rbodies if b.kind not in ("shaft", "pin")] or rbodies
        tq = np.concatenate([(b.mesh.vertices - origin) @ axis for b in nsh])
        reach = {1.0: max(0.0, float(tq.max())), -1.0: max(0.0, float(-tq.min()))}
        for s in (1.0, -1.0):
            d = reach[s] + np.arange(1, 61) * 0.5
            P = (origin + np.outer(s * d, axis))[:, None, :] + ring[None]
            sides.append(bool(measure.inside_any(sup, P.reshape(-1, 3)).any()))
        F["supports"] = tuple(sides)
        # wedges / blades: forks, wedgelets and skirts working at floor level ahead of the disc (ground game). The lead
        # rule is shared with spinner.reach and shape.weapon_leads (_physics.front_intrusions).
        front = ph.swept_front_y(wb, origin, axis)
        floor_g = floor if floor is not None else ph.floor_z(ctx)
        cand = [b for b in w.bodies if not b.fastener and not b.is_wire and b.id not in rotor
                and (b.kind in ph.GROUND_GAME_KINDS or ph.is_ground_game(ctx, b, floor_g)[0])]
        wedges = [b for b in cand if ph.is_ground_game(ctx, b, floor_g)[0]]
        if wedges:
            xl, xr = float(origin[0]) - half, float(origin[0]) + half
            left = any(b.aabb[1][0] <= xl + 0.5 and b.aabb[1][1] > origin[1] for b in wedges)
            right = any(b.aabb[0][0] >= xr - 0.5 and b.aabb[1][1] > origin[1] for b in wedges)
            F["wedgelets"] = (left, right)
            F["blade_lead_mm"] = max(float(b.aabb[1][1]) for b in wedges) - front
        else:
            F["wedgelets"] = (False, False)
        # tall forks/wedges ahead of the disc are not ground game: they fail blade_lead whatever the low parts do
        F["blade_lead_bad"] = [f"`{b.id}` {float(b.aabb[1][1]) - front:.1f} mm" for b in cand if b not in wedges and float(b.aabb[1][1]) - front > 0.5]
        others = [b for b in solid if not b.fastener and b.id not in rotor and b.kind in CHASSIS + ("fork",) and b not in wedges]
        if others:
            F["weapon_lead_mm"] = front - max(float(b.aabb[1][1]) for b in others)
        mx = ph.ground_lead_max(ctx)
        over = [float(b.aabb[1][1]) - front - mx for b in wedges if float(b.aabb[1][1]) - front > mx]
        if over:  # a ground-game part past its allowance counts against the weapon lead too
            F["weapon_lead_mm"] = min(F.get("weapon_lead_mm", np.inf), -max(over))
        if floor is not None:
            az = abs(float(axis[2]))
            low = float(origin[2]) - R * math.sqrt(max(0.0, 1 - az * az)) - half * az
            F["disc_floor_gap_mm"] = low - floor
            F["axle_height_mm"] = float(origin[2]) - floor
        if F.get("width"):
            F["drum_width_frac"] = 2 * rhalf / F["width"]
        F["teeth"] = _teeth(wb.surface(0.5)[0], origin, axis)
        rp = _part(r, wid)
        mat = catalog.material(rp.part.material) if rp.part.material else None
        if mat is not None:
            F["disc_material"] = (mat.cls, rp.part.process, rp.part.material)
        tot = ctx.metrics.get("mass_total_g")
        rm = ph.rotor_mass(ctx, wid)  # rotor parts + the outrunner bell when the bell carries the rotor
        if tot and rm is not None:
            F["weapon_mass_fraction"] = rm[0] / tot
            ctx.metrics["rotor_mass_g"] = rm[0]
            ctx.metrics["rotor_bell_mass_g"] = rm[2]
        e = ctx.metrics.get("weapon_energy_j")
        if e is not None and tot:
            F["energy_j_per_kg"] = e / (tot / 1000.0)
        # drive
        mid = wpart.weapon.motor if wpart.weapon else None
        mb = w.body(mid) if mid else None
        if mb is not None:
            q = mb.center - origin
            ax = float(q @ axis)
            rad = float(np.linalg.norm(q - ax * axis))
            belts = [p for p in spec.parts if p.kind == "belt" and p.belt is not None and set(p.belt.pulleys) & (rotor | {mid})]
            if belts:
                t = belts[0].tensioner
                F["weapon_drive"] = "belt_tensioned" if t is not None and t.kind != "none" else "belt_untensioned"
            elif abs(ax) <= half + 1.0 and rad < 0.6 * R:
                F["weapon_drive"] = "inside_hub"
            elif rad < 1.5 and _bell_carries(spec, mid, rotor):
                F["weapon_drive"] = "motor_is_hub"
            elif rad < 1.5:
                F["weapon_drive"] = "direct"
            else:
                F["weapon_drive"] = "unconnected"
    # wheels and drive
    wheels = [b for b in w.bodies if b.kind == "wheel"]
    wedges = [b for b in w.bodies if b.kind == "wedge" and not b.fastener]
    if wedges and floor is not None:
        F["wedge_floor_gap_mm"] = min(float(b.aabb[0][2]) for b in wedges) - floor
        big = max(wedges, key=lambda b: (b.aabb[1] - b.aabb[0]).prod())
        F["wedge_angle_deg"] = _slope_deg(big.mesh.vertices, 0.6)
        if F["wedge_angle_deg"] is None:
            F.pop("wedge_angle_deg")
        if F.get("width"):
            F["wedge_width_frac"] = (max(b.aabb[1][0] for b in wedges) - min(b.aabb[0][0] for b in wedges)) / F["width"]
    if wheels:
        motors = sum(1 for p in spec.parts if p.kind == "motor")
        belts = sum(1 for p in spec.parts if p.kind == "belt" and not (set(p.belt.pulleys if p.belt else []) & rotor))
        F["drive"] = (len(wheels), min(len(wheels), motors + belts), F.get("wedge_floor_gap_mm"))
        F["wheel_count"] = float(len(wheels))
        F["wheel_dia_mm"] = max(float(sorted(b.aabb[1] - b.aabb[0])[-1]) for b in wheels)
        chassis = [b for b in solid if not b.fastener and b.kind in CHASSIS and b.id not in assembly]
        top_c = max((float(b.aabb[1][2]) for b in chassis), default=None)
        top_w = max(float(b.aabb[1][2]) for b in wheels)
        if top_c is not None:
            F["invert"] = (bool(spec.can_run_inverted), top_w - top_c)
        missing = []
        for wb_ in wheels:
            c = wb_.center
            s = 1 if c[0] >= 0 else -1
            outer = wb_.aabb[1][0] if s > 0 else wb_.aabb[0][0]
            found = False
            for b in solid:
                if b.fastener or b.kind not in CHASSIS or b.id in rotor:
                    continue
                bo = b.aabb[1][0] if s > 0 else b.aabb[0][0]
                if s * (bo - outer) < 0.5:
                    continue
                ylap = min(b.aabb[1][1], wb_.aabb[1][1]) - max(b.aabb[0][1], wb_.aabb[0][1])
                zlap = min(b.aabb[1][2], wb_.aabb[1][2]) - max(b.aabb[0][2], wb_.aabb[0][2])
                if ylap >= 0.5 * (wb_.aabb[1][1] - wb_.aabb[0][1]) and zlap > 0:
                    found = True
                    break
            if not found:
                missing.append(wb_.id)
        F["pods_missing"] = missing
    # top armour slope
    tops = [b for b in solid if b.kind in ("armor", "plate") and not b.fastener]
    if tops:
        top = max(tops, key=lambda b: b.aabb[1][2])
        s = _slope_deg(top.mesh.vertices)
        if s is not None:
            F["top_slope_deg"] = s
    # printed tub floor
    tubs = []
    for b in solid:
        if b.fastener or b.kind != "structure" or b.part_idx is None or b.id in assembly:
            continue
        rp = r.parts[b.part_idx]
        if catalog.part_is_printed(rp.part.process, rp.part.material):
            tubs.append(b)
    if tubs:
        tub = max(tubs, key=lambda b: float(np.prod(b.aabb[1][:2] - b.aabb[0][:2])))
        F["tub_height_mm"] = float(tub.aabb[1][2] - tub.aabb[0][2])
        F["floor"] = _floor_profile(tub)
        if F["floor"] is None:
            F.pop("floor")
    # removable lids into print
    lid_bad, any_lid = [], False
    for f in spec.fasteners:
        if not f.removable:
            continue
        lid = [x for x in (f.through or []) if spec.part(x) is not None and spec.part(x).kind in ("armor", "plate")]
        if not lid:
            continue
        any_lid = True
        t = spec.part(f.threads_into) if f.threads_into else None
        if t is None:
            lid_bad.append(f.id)
        elif t.kind not in ("insert", "nut") and catalog.part_is_printed(t.process, t.material):
            lid_bad.append(f.id)
    if any_lid:
        F["lid_bad"] = lid_bad
    # switch access
    sw = next((b for b in w.bodies if b.kind == "switch"), None)
    if sw is not None:
        F["switch_access"] = _switch_access(w, sw)
    return F


def _floor_profile(tub):
    lo, hi = tub.aabb
    span = hi[:2] - lo[:2]
    us = np.linspace(-0.7, 0.7, 11)
    zs = lo[2] + 0.125 + np.arange(0, 40) * 0.25
    cols, diag = [], []
    for u in us:
        for v in us:
            x = (lo[0] + hi[0]) / 2 + u * span[0] / 2
            y = (lo[1] + hi[1]) / 2 + v * span[1] / 2
            cols.append([(x, y, z) for z in zs])
            diag.append(abs(abs(u) - abs(v)) < 0.08)
    P = np.array(cols).reshape(-1, 3)
    ins = tub.inside(P).reshape(len(cols), len(zs))
    h = np.array([(np.argmin(c) if not c.all() else len(c)) * 0.25 for c in ins])
    if not (h > 0).any():
        return None
    base = h[h > 0]
    skin = float(np.percentile(base, 30))
    rib = float(h.max() - skin)
    return skin, rib


def _switch_access(w, sw):
    others = [b for b in w.bodies if b is not sw and not b.is_wire]
    scene = measure.Scene(others)
    c = sw.center
    ext = (sw.aabb[1] - sw.aabb[0]) / 2
    res = {}
    for name, d in (("side", X), ("side", -X), ("top", Z), ("rear", -Y)):
        o = c + d * (ext @ np.abs(d) + 0.05)
        off = [np.zeros(3)]
        for k in range(3):
            if abs(d[k]) < 0.5:
                e = np.zeros(3)
                e[k] = ext[k] * 0.5
                off += [e, -e]
        dist, _ = scene.first_hit(np.array([o + e for e in off]), np.tile(d, (len(off), 1)))
        clear = bool(np.isinf(dist).all())
        res[name] = res.get(name, False) or clear
    for k in ("side", "top", "rear"):
        if res.get(k):
            return k
    return "none"


# ------------------------------------------------------------------------------------------------------------- run


def run(ctx):
    spec = ctx.r.spec
    name = spec.raw.get("archetype")
    if not name:
        return []
    if name not in ARCHETYPES:
        ctx.not_checked.append(f"Archetype rules: `{name}` is not a known archetype")
        return [fail("archetype.unknown", G, BLOCKER, "Unknown archetype",
                     f"`archetype` is {name!r}; known: {', '.join(sorted(ARCHETYPES))}.")
                .fix("Use one of the known archetypes or remove the key.")]
    over = spec.raw.get("archetype_params") or {}
    if not isinstance(over, dict):
        return [fail("archetype.unknown", G, BLOCKER, "Archetype parameters are not a table", "`archetype_params` must map names to values.")]
    F = facts(ctx)
    out = [note("archetype.declared", G, f"Archetype {name}", f"Held to the `{name}` layout rules ({len(ARCHETYPES[name][0])} rules).")]
    for rid, passed, msg in evaluate(name, F, over):
        sev, title, hint, _ = RULES[rid]
        fid = f"archetype.{rid}"
        if passed is None:
            ctx.not_checked.append(f"Archetype rule `{rid}`: {msg}")
            out.append(fail(fid, G, WARNING, f"Not checked: {title}", f"Could not evaluate ({msg}).")
                       .fix("Add the missing part or data so this rule can be measured."))
        elif not isinstance(passed, str) and bool(passed):
            out.append(ok(fid, G, title, msg))
        else:
            out.append(fail(fid, G, WARNING if passed == "warn" else sev, title, msg).fix(hint))
    for k, v in F.items():
        if isinstance(v, (int, float)) and not isinstance(v, bool):
            ctx.metrics[f"archetype.{k}"] = float(v)
    return out
