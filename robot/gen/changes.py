"""Change hypotheses on an existing robot: "what if someone swapped X, resized Y, or re-arranged Z - does the design
still hold?" The design-space generator (hypothesis.py) enumerates new robots; this one enumerates edits to a built one.

Three families, every one a declarative change (robot/overlay.py ops), never a code edit:

  swap          a COTS part replaced by every other catalog entry of its role (weapon motor, drive motor, battery,
                drive / weapon ESC, switch, wheel) plus battery-connector swaps. Candidates come from
                `catalog.catalog()` at call time, so entries added to catalog_data/components.json show up untouched.
  dimension     the robust sweep's +-10 % master-param edits (robot/checks/robust/plan.py) - added by the runner.
  architecture  layout changes from ARCH: internal compartments, drive location, driven wheels, a servo at a named
                location, battery orientation, weapon type. Each names a settings hook; a robot that declares the
                hook (hooks.json) expresses it, a generic fallback covers a few, the rest are "not expressible" and
                the report names the missing hook and estimates the code that would have to change.

To add a change: append to ARCH (hook name, values, keywords for the diff estimate, the part kinds it touches) or add
a role to ROLES. No other code changes.
"""

from __future__ import annotations

import fnmatch
from dataclasses import dataclass, field

from . import hypothesis as H

# role -> (catalog kinds, how to tell a part / entry of this role). Order = report order.
ROLES = {
    "weapon_motor": ("weapon_motor",),
    "drive_motor": ("motor",),
    "battery": ("battery",),
    "drive_esc": ("esc",),
    "weapon_esc": ("esc",),
    "switch": ("switch",),
    "wheel": ("wheel", "tyre"),
}
CONNECTORS = ("xt30", "jst_rcy", "jst_ph", "mr30", "xt60")


@dataclass
class Change:
    id: str
    family: str  # "swap" | "dimension" | "architecture"
    title: str
    ops: list = field(default_factory=list)  # overlay ops (may hold `hook` ops)
    hook: str = ""  # the settings hook it needs (architecture)
    keywords: tuple = ()  # build-source words a code change would touch (diff estimate when not expressible)
    touches: dict = field(default_factory=dict)  # overlay selector of the parts it affects (diff estimate)
    note: str = ""
    job: object = None  # a plan.Job for dimension changes
    param_set: tuple = ()  # (params name, value) edited together with the ops, e.g. the wheel OD the axles derive from


def _weaponish(e) -> bool:
    ports = set((e.ports or {}) if hasattr(e, "ports") else e)
    name = (getattr(e, "name", "") or "").lower()
    if "motor" in ports or "phases" in ports:
        return True
    if {"m1", "m2"} & ports:
        return False
    return any(w in name for w in ("brushless", "spinner", "weapon"))


def role_of(part: dict, entry) -> str | None:
    if entry is None:
        return "wheel" if part.get("kind") in ("wheel", "tyre") else None
    k = entry.kind
    if k == "esc":
        return "weapon_esc" if _weaponish(entry) else "drive_esc"
    for r, kinds in ROLES.items():
        if k in kinds and r not in ("drive_esc", "weapon_esc"):
            return r
    return None


def candidates(role: str, current: str | None, cat=None) -> list:
    """Catalog entries of `role` other than `current` (read live: new catalog entries appear automatically)."""
    from .. import catalog

    out = []
    for e in cat if cat is not None else catalog.catalog():
        if e.id == current or e.kind not in ROLES[role] or (e.props or {}).get("half_of"):   # derived motor halves swap with their motor
            continue
        if e.kind == "esc" and (role == "weapon_esc") != _weaponish(e):
            continue
        out.append(e)
    return out


def _groups(raw) -> dict:
    """{(role, key): [part ids]}: parts of one role sharing a catalog id (or, for model wheels, a `stock`)."""
    from .. import catalog

    g = {}
    for p in raw.get("parts") or []:
        cid = p.get("catalog")
        e = catalog.find(cid) if cid else None
        r = role_of(p, e)
        if r is None or (e is None and r != "wheel"):
            continue
        key = cid or p.get("stock") or p.get("label") or p["id"]
        g.setdefault((r, key), []).append(p["id"])
    return g


def wheel_extras(hooks, ids, entry, ops) -> tuple:
    """(ops, (param, OD), note) for a catalog wheel swap: a wheel with no belt groove (catalog wheels carry none unless
    props.belt_groove) also sets the robot's `drive.belt` hook to "none"; the wheel OD goes to the params literal the
    robot names for that wheel position under hooks.json `wheel_od` {id glob: PARAM}."""
    hk = (hooks or {}).get("hooks") or {}
    ops = list(ops)
    notes = []
    if not (entry.props or {}).get("belt_groove"):
        if "none" in ((hk.get("drive.belt") or {}).get("values") or {}):
            ops.append({"op": "hook", "name": "drive.belt", "value": "none"})
            notes.append("groove-less wheel: drive.belt=none")
        else:
            notes.append("groove-less wheel; no drive.belt hook")
    od = (entry.props or {}).get("diameter_mm")
    pset = ()
    for pat, param in ((hooks or {}).get("wheel_od") or {}).items():
        if pat.startswith("_"):
            continue
        if od and all(fnmatch.fnmatchcase(i, pat) for i in ids):
            pset = (param, float(od))
            notes.append(f"{param}={od:g}")
            break
    return ops, pset, "; ".join(notes)


def swap_hook(hooks: dict | None, role: str, ids=None):
    """(name, hook) of the robot setting that swaps parts of `role` as one unit (a hook declaring `"swap": "<role>"`),
    else None. A robot whose build derives the fitting parts from the selected catalog entry (mount holes, shaft, bell)
    declares one, and every catalog candidate of that role becomes a setting of it instead of a bare catalog op."""
    for name, h in ((hooks or {}).get("hooks") or {}).items():
        if isinstance(h, dict) and h.get("swap") == role:
            sel = (h.get("swaps") or {}).get("id")  # optional: only these parts (e.g. the rear wheels)
            if sel is None or ids is None or sorted(sel) == sorted(ids):
                return name, h
    return None


def swap_changes(raw, cat=None, hooks=None) -> list:
    from .. import catalog

    out = []
    for (role, key), ids in _groups(raw).items():
        cur = key if catalog.find(key) else None
        cur_e = catalog.find(cur) if cur else None
        cur = ((cur_e.props or {}).get("half_of") or cur) if cur_e else cur   # a derived fixed half stands for its motor
        tag = "+".join(ids) if len(ids) <= 2 else f"{ids[0]}..({len(ids)})"
        sh = swap_hook(hooks, role, ids)
        for e in candidates(role, cur, cat):
            vals = (sh[1].get("values") if sh else None)
            if sh and isinstance(vals, list) and e.id not in vals:  # the setting does not offer this part
                sh_e = None
            else:
                sh_e = sh
            ops = [{"op": "wheel" if role == "wheel" else "catalog", "select": {"id": ids}, "to": e.id}]
            note, pset = "", ()
            if sh_e:
                ops = [{"op": "hook", "name": sh_e[0], "value": e.id}]
                note = f"one unit through the `{sh_e[0]}` setting"
            if role == "wheel":
                ops, pset, wn = wheel_extras(hooks, ids, e, ops)
                if sh_e:
                    pset = ()  # the setting sizes the wheel itself
                note = "; ".join(x for x in (note, wn) if x)
            if not sh_e and role == "weapon_motor":
                cur_e = catalog.find(cur) if cur else None
                rotor_old = (cur_e.props or {}).get("rotor_part") if cur_e else None
                rotor_new = (e.props or {}).get("rotor_part")
                if rotor_old:
                    rp = [p["id"] for p in raw.get("parts") or [] if p.get("catalog") == rotor_old]
                    if rotor_new and rp:
                        ops.append({"op": "catalog", "select": {"id": rp}, "to": rotor_new})
                    elif rp:
                        note = f"one-piece motor: the split rotor part {rp} has no counterpart and is kept"
            out.append(Change(f"swap:{role}:{tag}->{e.id}", "swap", f"{role.replace('_', ' ')} {cur or key} -> {e.id} ({e.name})",
                              ops, hook=sh_e[0] if sh_e else "", touches={"id": ids}, note=note, param_set=pset))
    for p in raw.get("parts") or []:  # battery connector
        e = catalog.find(p.get("catalog")) if p.get("catalog") else None
        if p.get("kind") != "battery" and not (e and e.kind == "battery"):
            continue
        cur = p.get("connector") or (list(e.ports)[0] if e and e.ports else None)
        for c in CONNECTORS:
            if c != cur:
                out.append(Change(f"swap:connector:{p['id']}->{c}", "swap", f"battery connector {cur} -> {c}",
                                  [{"op": "set", "select": {"id": p["id"]}, "field": "connector", "value": c}],
                                  touches={"id": [p["id"]]}))
    return out


# ---------------------------------------------------------------------------------------------------- architecture
# name, hook, values, keywords (build-source words a hard-coded version touches), parts it touches, a generic fallback
# (fn(raw, value) -> ops or None) for robots that declare no hook.
def _battery_rot(raw, value):
    for p in raw.get("parts") or []:
        if p.get("kind") == "battery" and p.get("rot") is not None:
            r = list(p["rot"])
            long_x = round(r[2]) % 180 == 0
            if (value == "long_x") == long_x:
                return []
            r[2] = (r[2] + 90.0) % 360.0
            return [{"op": "set", "select": {"id": p["id"]}, "field": "rot", "value": r}]
    return None


def _remove_belts(raw, value):
    belts = [p["id"] for p in raw.get("parts") or [] if p.get("kind") == "belt"]
    if value == "2WD" and belts:
        return [{"op": "remove", "select": {"id": belts}}]
    return None


ARCH = [
    dict(hook="chassis.compartments", values=("none", "split_battery_bay"),
         title="internal compartments: {v}", keywords=("pocket", "bay", "cage", "rib", "partition", "compartment", "lattice"),
         touches={"kind": "structure"}, fallback=None),
    dict(hook="drive.location", values=("front", "mid", "front_motors_rear_driven"),
         title="drive location: {v}", keywords=("RY", "keyhole", "motor_", "whub", "N10", "belt", "axle"),
         touches={"kind": ["motor", "pulley", "wheel", "belt", "structure"]}, fallback=None),
    dict(hook="drive.driven_wheels", values=("2WD", "4WD"), title="driven wheels: {v}",
         keywords=("belt", "whub_f", "front_hub", "oring", "groove"), touches={"kind": ["belt", "pulley"]}, fallback=_remove_belts),
    dict(hook="battery.orientation", values=("long_x", "long_y"), title="battery orientation: {v}",
         keywords=("battery", "BAT", "bay"), touches={"kind": ["battery", "structure"]}, fallback=_battery_rot),
    dict(hook="weapon.type", values=("vspin_drum", "vspin_eggbeater", "hspin_bar"), title="weapon slot: {v}",
         keywords=("disc", "spider", "blade", "tooth", "WY", "W_FRAME"), touches={"kind": ["weapon", "structure"]}, fallback=None),
]


def arch_changes(raw, hooks: dict, cat=None) -> list:
    from .. import catalog

    hk = hooks.get("hooks") or {}
    out = []
    for a in ARCH:
        default = (hk.get(a["hook"]) or {}).get("default")
        for v in a["values"]:
            if v == default:
                continue
            assert a["hook"] != "weapon.type" or v in H.WEAPONS
            op = {"op": "hook", "name": a["hook"], "value": v}
            fb = None
            if a["hook"] not in hk and a["fallback"]:
                fb = a["fallback"](raw, v)
                if fb == []:  # already the robot's layout: not a change
                    continue
            out.append(Change(f"arch:{a['hook']}={v}", "architecture", a["title"].format(v=v),
                              fb if fb else [op], hook=a["hook"], keywords=a["keywords"], touches=a["touches"],
                              note="generic fallback (no robot hook needed)" if fb else ""))
    known = {a["hook"] for a in ARCH}
    for name, h in hk.items():  # every other declared setting the robot offers is a hypothesis too
        if isinstance(h, dict) and h.get("swap"):  # a swap setting: its values are the swap hypotheses
            continue
        vals = h.get("values")
        vals = list(vals) if isinstance(vals, (list, dict)) else []
        for v in vals:
            if name not in known and v != h.get("default"):
                out.append(Change(f"arch:{name}={v}", "architecture", f"declared setting {name} = {v}",
                                  [{"op": "hook", "name": name, "value": v}], hook=name))
    servos = [e for e in (cat if cat is not None else catalog.catalog()) if e.kind == "servo"]
    if servos:
        sv = servos[0]
        anchors = list((hooks.get("anchors") or {})) or ["rear"]
        for an in anchors:
            part = {"id": f"servo_{an}", "kind": "servo", "catalog": sv.id, "retained": "screws", "rotates_with": "fixed"}
            out.append(Change(f"arch:add_servo@{an}", "architecture", f"add a servo ({sv.id}) at `{an}`",
                              [{"op": "add", "part": part, "anchor": an}], hook=f"anchor:{an}",
                              keywords=("servo", "mount", "pocket"), touches={"kind": "structure"}))
    return out


def change_hypotheses(raw: dict, hooks: dict, cat=None) -> list:
    """Swap + architecture changes for one spec (dimension changes come from the robust plan)."""
    return swap_changes(raw, cat, hooks) + arch_changes(raw, hooks, cat)


# ---------------------------------------------------------------------------------------------- diff estimate
def owner_of(fname: str, owners: dict) -> str:
    for who, pats in (owners or {}).items():
        if any(fnmatch.fnmatch(fname, p) for p in pats):
            return who
    return "spec/framework"


def builder_files(files, graph, raw, part_ids) -> dict:
    """{part id: [build file names]}: the files defining what a part's PARTS entry calls directly (its builder), or
    the spec layer for a catalog part."""
    import ast

    from ..checks.robust.usage import spec_part_keys

    defs = {}
    for f in files:
        try:
            tree = ast.parse(f.read_text())
        except SyntaxError:
            continue
        for st in tree.body:
            ns = [st.name] if isinstance(st, (ast.FunctionDef, ast.ClassDef)) else \
                [t.id for t in ast.walk(st) if isinstance(t, ast.Name) and isinstance(t.ctx, ast.Store)]
            for n in ns:
                defs.setdefault(n, set()).add(f)
    keys = spec_part_keys(raw)
    out = {}
    for pid in part_ids:
        fs = set()
        for k in keys.get(pid, []):
            names = (graph.parts.get(k) or (set(), set()))[0]
            for n in names:
                fs |= {f for f in defs.get(n, set()) if not f.stem.startswith("params")}
        out[pid] = sorted({f for f in fs}, key=lambda f: f.name) or None
    return out


def estimate_diff(files, graph, raw, touches: dict, keywords, owners: dict) -> dict:
    """What a code change would touch: the builder files of the touched parts and, per file, the lines that hard-code
    the change's keywords (an estimate; a declared hook makes it 0). {"files": {name: lines}, "lines", "by_owner"}."""
    import re

    from .. import overlay

    ids = [p["id"] for p in overlay.select(raw, dict(touches))]
    bf = builder_files(files, graph, raw, ids)
    fs = {f for v in bf.values() if v for f in v}
    rx = re.compile("|".join(re.escape(k) for k in keywords), re.I) if keywords else None
    out = {}
    for f in sorted(fs, key=lambda f: f.name):
        n = sum(1 for ln in f.read_text().splitlines() if rx and rx.search(ln) and not ln.lstrip().startswith("#")) if rx else 0
        if n or not rx:
            out[f.name] = n
    if any(v is None for v in bf.values()):
        out.setdefault("spec.py", 0)  # catalog parts are placed by the spec layer
    by_owner = {}
    for fn, n in out.items():
        by_owner.setdefault(owner_of(fn, owners), {})[fn] = n
    return {"files": out, "lines": sum(out.values()), "by_owner": by_owner}


# ------------------------------------------------------------------------------------------------- overall size
SIZE_STEPS = (0.10, -0.10, 0.20, -0.20, 0.30, -0.30)
SIZE_DIMS = ("length", "width", "height")
SIZE_KEYWORDS = {"length": ("CH_Y0", "CH_Y1", "RY", "SA", "SB", "WY"), "width": ("CH_HALF_W", "CH_IN_X", "SA_X0", "SB_X0"),
                 "height": ("CH_Z0", "CH_Z1", "WZ", "TOP_Z0")}


def size_changes(hooks: dict, params: list, usage, plan_mod) -> list:
    """Whole-robot size changes at +-10/20/30 %. A dimension whose `sizes` entry names a single master `param` is a
    params edit; otherwise it is a missing hook `size.<dim>` (plus `proxy` param edits when one is declared), and a
    "short 2WD" (shorter, front wheels off) combines size.length with the drive.short_2wd hook."""
    sizes = hooks.get("sizes") or {}
    by = {p.name: p for p in params}
    out = []
    for dim in SIZE_DIMS:
        ent = sizes.get(dim) or {}
        master = by.get(ent.get("param"))
        if master is None:  # no single master: say so, at every step
            for st in SIZE_STEPS:
                out.append(Change(f"size:{dim}{st:+.0%}", "size", f"overall {dim} {st:+.0%}",
                                  [{"op": "hook", "name": f"size.{dim}", "value": f"{st:+.0%}", "why": ent.get("why", "")}],
                                  hook=f"size.{dim}", keywords=SIZE_KEYWORDS[dim], touches={"kind": "structure"}))
        for p, tag in ((master, ""), (by.get(ent.get("proxy")), " (proxy)")):
            if p is None:
                continue
            for j in plan_mod.param_jobs(p, usage.parts_reading(p.symbol), SIZE_STEPS):
                j.phase = 0
                j.id = f"size:{dim}{tag.strip()}:{j.id}"
                out.append(Change(j.id, "size", f"overall {dim}{tag} via {p.name} {j.base:g} -> {j.value:g} ({j.step:+.0%})", job=j))
    short = [{"op": "hook", "name": "drive.short_2wd", "value": "no_front_wheels"}]
    out.append(Change("size:short_2wd", "size", "short 2WD: length -20 %, front wheels removed, 2 motors",
                      short + [{"op": "hook", "name": "size.length", "value": "-20%"}], hook="size.length",
                      keywords=SIZE_KEYWORDS["length"] + ("whub_f", "front_hub", "belt"), touches={"kind": ["structure", "pulley", "wheel"]}))
    return out
