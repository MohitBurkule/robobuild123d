"""LLM front door (work in progress): a small `design.json` -> validated hypothesis for `robot/gen`.

`robot build` (robot/build_cmd.py) and `robot eval` (robot/evals/run.py) wrap this (UNTESTED).
design.json keys (all optional except weapon.type):
  name, rules ("aws2025"), weapon {type, mount, orientation, attachment, disc_stack, esc},
  drive {layout, motor, wheel_dia, transmission, wheel_guards}, front, skirts, chassis, invertible,
  electronics {battery, drive_esc, receiver}, body {outline, y0, y1, zb, zt, axle_y}, options {experimental, thin_forks, seed}
Weapon dimensions and materials are NOT configurable in the generator today, so they are not accepted.
"""

from __future__ import annotations

import difflib
import json

from ..gen import hypothesis as H

# design.json path -> hypothesis axis
FIELDS = {
    ("weapon", "type"): "weapon", ("weapon", "mount"): "mount", ("weapon", "orientation"): "orientation",
    ("weapon", "attachment"): "attachment", ("weapon", "disc_stack"): "disc_stack", ("weapon", "esc"): "weapon_esc",
    ("drive", "layout"): "drive_layout", ("drive", "motor"): "drive_motor", ("drive", "wheel_dia"): "wheel_dia",
    ("drive", "transmission"): "transmission", ("drive", "wheel_guards"): "wheel_guards",
    ("front",): "front", ("skirts",): "skirts", ("chassis",): "chassis", ("invertible",): "invertible",
    ("electronics", "battery"): "battery", ("electronics", "drive_esc"): "drive_esc", ("electronics", "receiver"): "rx",
}
AXIS_PATH = {v: ".".join(k) for k, v in FIELDS.items()}
BODY = ("outline", "y0", "y1", "zb", "zt", "axle_y")  # build.frame_params / make_plan user overrides
OPTIONS = {"experimental": bool, "thin_forks": bool, "seed": int}
RULES_PROFILES = ("aws2025",)
TOP = {"name", "rules", "weapon", "drive", "front", "skirts", "chassis", "invertible", "electronics", "body", "options"}
SECTIONS = {s: [k[1] for k in FIELDS if len(k) == 2 and k[0] == s] for s in ("weapon", "drive", "electronics")}
SECTIONS["body"] = list(BODY)
SECTIONS["options"] = list(OPTIONS)
NOT_CONFIGURABLE = {"materials": "materials are fixed by the generator (nylon shell, PETG-CF wedge, TPU skirts, steel disc)",
                    "mass_target_g": "the mass limit is the rules profile's 150 g; the gate trades skirts/forks to meet it"}


def _err(code, field, message, value=None, allowed=None, hint=None):
    e = {"code": code, "field": field, "message": message, "hint": hint}
    if value is not None:
        e["value"] = value
    if allowed is not None:
        e["allowed"] = list(allowed)
        near = difflib.get_close_matches(str(value), [str(a) for a in allowed], n=1, cutoff=0.4)
        if near:
            e["suggestion"] = near[0]
    return e


def buildable_summary() -> dict:
    return {"weapons": {w: {k: list(v) for k, v in c.items()} for w, c in H.BUILDABLE.items()},
            "drives": sorted(f"{a}+{b}" for a, b in H.BUILDABLE_DRIVES),
            "experimental": {w: {k: list(v) for k, v in c.items()} for w, c in H.EXPERIMENTAL.items()}}


def validate(d) -> tuple:
    """(hypothesis or None, user overrides for gen.build, errors). Errors are dicts: code, field, message, allowed,
    suggestion, hint. Codes: bad_type, unknown_key, not_configurable, bad_enum, unknown_catalog_id, incompatible,
    over_budget, not_buildable."""
    errors, axes, user = [], {}, {}
    if not isinstance(d, dict):
        return None, {}, [_err("bad_type", "", "design.json must be a JSON object")]
    for k in d:
        if k in NOT_CONFIGURABLE:
            errors.append(_err("not_configurable", k, NOT_CONFIGURABLE[k], hint="remove this key"))
        elif k not in TOP:
            errors.append(_err("unknown_key", k, f"unknown key {k!r}", k, sorted(TOP), "use one of the allowed keys"))
    for sec, keys in SECTIONS.items():
        v = d.get(sec, {})
        if not isinstance(v, dict):
            errors.append(_err("bad_type", sec, f"{sec} must be an object with keys {keys}"))
            continue
        for k in v:
            if k not in keys:
                msg = f"unknown key {k!r} in {sec}"
                if sec == "weapon":
                    msg += " (weapon dimensions are derived by the generator and are not configurable yet)"
                errors.append(_err("unknown_key", f"{sec}.{k}", msg, k, keys, "use one of the allowed keys"))
    if d.get("rules", "aws2025") not in RULES_PROFILES:
        errors.append(_err("bad_enum", "rules", "unknown rules profile", d.get("rules"), RULES_PROFILES))
    for path, axis in FIELDS.items():
        cur = d
        for p in path:
            cur = cur.get(p) if isinstance(cur, dict) else None
        if cur is None:
            continue
        if axis == "weapon":
            cur = H.normalise(cur, H.WEAPONS)
        if axis == "drive_motor":
            cur = {"n10_2200rpm_6v": "n10", "n20_1000rpm_6v": "n20"}.get(cur, cur)
        if cur not in H.AXES[axis] or (isinstance(cur, bool) != isinstance(H.AXES[axis][0], bool)):
            code = "bad_enum"
            hint = "pick one of the allowed values"
            if axis in ("battery", "drive_esc", "weapon_esc", "rx", "drive_motor"):
                from .. import catalog
                known = isinstance(cur, str) and catalog.find(cur) is not None
                code = "unknown_catalog_id"
                hint = ("this id is in the catalogue but the generator has no pocket/port map for it yet"
                        if known else "not in the catalogue (`python3 -m robot catalog`)") + "; use an allowed id"
            errors.append(_err(code, ".".join(path), f"{cur!r} is not a supported {axis}", cur, H.AXES[axis], hint))
        else:
            axes[axis] = cur
    if "weapon" not in axes:
        if not any(e["field"] == "weapon.type" for e in errors):
            errors.append(_err("bad_type", "weapon.type", "weapon.type is required", None, H.WEAPONS,
                               f"buildable today: {sorted(H.BUILDABLE)}"))
        return None, {}, errors
    body = d.get("body") if isinstance(d.get("body"), dict) else {}
    for k, v in body.items():
        if k == "outline":
            if not (isinstance(v, list) and len(v) >= 3 and all(isinstance(p, list) and len(p) == 2 for p in v)):
                errors.append(_err("bad_type", "body.outline", "outline is a list of at least 3 [x, y] points in mm"))
        elif k in BODY and not isinstance(v, (int, float)):
            errors.append(_err("bad_type", f"body.{k}", f"{k} is a number in mm"))
        if k in BODY:
            user[k] = v
    opts = d.get("options") if isinstance(d.get("options"), dict) else {}
    for k, v in opts.items():
        if k in OPTIONS and not isinstance(v, OPTIONS[k]):
            errors.append(_err("bad_type", f"options.{k}", f"{k} must be {OPTIONS[k].__name__}"))
        elif k in OPTIONS:
            user[k] = v
    if isinstance(d.get("name"), str):
        user["name"] = d["name"]
    elif "name" in d:
        errors.append(_err("bad_type", "name", "name must be a string"))
    if errors:
        return None, user, errors
    # derived defaults: unspecified axes come from the weapon's preset; receiver and transmission follow ESC and layout
    full = H.preset(axes["weapon"]).to_dict()
    full.update(axes)
    if "rx" not in axes:
        full["rx"] = "integrated" if full["drive_esc"] == "c_malenki_nano_antweight_esc_receiver" else "rx_fs_ia6_decased"
    if "transmission" not in axes:
        full["transmission"] = "belt" if full["drive_layout"] in ("4WD", "6WD", "8WD") else "direct"
    h = H.Hypothesis.from_dict(full)
    from ..gen import rules
    for r in rules.RULES:
        msg = r.check(h)
        if msg:
            code = "over_budget" if r.name in ("mass_budget", "size_budget") else "incompatible"
            errors.append(_err(code, ", ".join(AXIS_PATH[a] for a in r.needs[:4]), msg,
                               hint=f"rule {r.name}: change one of these fields"))
    if not errors and not H.buildable(h, bool(user.get("experimental"))):
        b = H.BUILDABLE.get(h.weapon)
        if b is None:
            errors.append(_err("not_buildable", "weapon.type", f"the generator cannot build weapon {h.weapon!r} yet",
                               h.weapon, sorted(H.BUILDABLE), f"buildable today: {json.dumps(buildable_summary())}"))
        else:
            want = dict({k: (v,) for k, v in H.DEFAULT_ONLY.items()}, **b)
            for k, allowed in want.items():
                if getattr(h, k) not in allowed:
                    errors.append(_err("not_buildable", AXIS_PATH[k], f"{h.weapon} with {k}={getattr(h, k)!r} is not "
                                       "buildable yet", getattr(h, k), allowed,
                                       "use an allowed value" + ("; chassis=tub needs options.experimental=true"
                                                                 if k == "chassis" else "")))
            if (h.drive_layout, h.transmission) not in H.BUILDABLE_DRIVES:
                errors.append(_err("not_buildable", "drive.transmission", f"drive {h.drive_layout}+{h.transmission} is not "
                                   "buildable yet", f"{h.drive_layout}+{h.transmission}",
                                   sorted(f"{a}+{c}" for a, c in H.BUILDABLE_DRIVES), "2WD is direct, 4WD is belt"))
    return (None if errors else h), user, errors


def schema(buildable_only: bool = False) -> dict:
    """JSON Schema of design.json, enums from the live axes (or only the values with an assembler)."""
    def enum(axis):
        vals = list(H.AXES[axis])
        if buildable_only:
            ok = {v for c in H.BUILDABLE.values() for v in c.get(axis, ())}
            if axis == "weapon":
                ok = set(H.BUILDABLE)
            if axis == "drive_layout":
                ok = {a for a, _ in H.BUILDABLE_DRIVES}
            vals = [v for v in vals if v in ok] or vals
        t = "boolean" if isinstance(vals[0], bool) else "integer" if isinstance(vals[0], int) else "string"
        return {"type": t, "enum": vals}

    props = {"name": {"type": "string"}, "rules": {"type": "string", "enum": list(RULES_PROFILES)}}
    for path, axis in FIELDS.items():
        if len(path) == 1:
            props[path[0]] = enum(axis)
        else:
            sec = props.setdefault(path[0], {"type": "object", "additionalProperties": False, "properties": {}})
            sec["properties"][path[1]] = enum(axis)
    props["weapon"]["required"] = ["type"]
    num = {"type": "number", "description": "mm, robot frame: +y forward, z=0 at the axle plane"}
    props["body"] = {"type": "object", "additionalProperties": False,
                     "properties": dict({k: num for k in BODY[1:]}, outline={
                         "type": "array", "minItems": 3, "items": {"type": "array", "items": {"type": "number"},
                                                                    "minItems": 2, "maxItems": 2}})}
    props["options"] = {"type": "object", "additionalProperties": False,
                        "properties": {k: {"type": "boolean" if t is bool else "integer"} for k, t in OPTIONS.items()}}
    return {"$schema": "https://json-schema.org/draft/2020-12/schema", "title": "robot design.json", "type": "object",
            "additionalProperties": False, "required": ["weapon"], "properties": props,
            "x-buildable": buildable_summary()}
