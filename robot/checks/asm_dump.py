"""Assembly parity with the SolidWorks assembly dump (`research/sldprt/dumps_v2/<asm>.asmdump.txt`): component
transforms, mass properties, mates and the interferences SolidWorks itself reports.

Spec (top level, all optional): {"asm_dump": {"file": path (default DEFAULT_FILE), "rig": "module:ATTR" (a joints.Rig
whose `_mates` are our assembly mates; the robot's `src/` is on the path), "map": {"<part>": "<component>"},
"ok": {"<check>:<part or mate>": "reason citing the reference"}}}.
Our part <-> component: `map`, else the reference_cad entry's STL stem (RV12_N10_2200_RPM_1 -> "RV12 N10 2200 RPM-<n>"),
picking among same-named components the one whose mass centre lies inside / nearest that STL (STEP and SolidWorks number
copies differently). Frames: component XFORM (SolidWorks assembly frame, m) -> STL frame is the identity; then
reference_cad's ref_to_world / mirror_x / ref_shift.
  asm.placement (BLOCKER)  our part frame (body M) vs the component's transform in world: origin within PLACE_MM and
                           axes within PLACE_DEG. An entry `ref_frame` 4x4 (our part frame -> the SolidWorks part frame,
                           mm) with `ref_frame_reason` states a deliberate frame offset (e.g. a catalog origin).
  asm.mass (BLOCKER)       our part's volume and mass centre vs the component's: VOL_FRAC / COM_MM.
  asm.mate (BLOCKER)       every unsuppressed reference mate between two mapped parts has a Rig (or spec) mate between
                           them; mates of unmapped components are listed as NOT CHECKED.
  known_interference()     used by interference.overlap: a pair that SolidWorks also reports interfering, with our
                           volume <= INT_FRAC x theirs, is a known waiver citing the asmdump; anything else stays ours.
Opt-out: `asm_dump.ok` with a reason that cites the reference (reference_cad.PATH_CITE), else the waiver is a BLOCKER.
"""

from __future__ import annotations

import re
from functools import lru_cache
from pathlib import Path

import numpy as np

from ..finding import BLOCKER, fail, note, ok

G = "reference"
DEFAULT_FILE = "/mnt/project-files/robot-cad/research/sldprt/dumps_v2/rvrn 2.0.asmdump.txt"
PLACE_MM = 0.1
PLACE_DEG = 0.5
VOL_FRAC = 0.02
COM_MM = 0.3
INT_FRAC = 1.1
MATE_TYPES = {0: "coincident", 1: "concentric", 2: "perpendicular", 3: "parallel", 4: "tangent", 5: "distance",
              6: "angle", 8: "symmetric", 10: "gear", 11: "width"}

_KV = re.compile(r"(\w+)=(\([^)]*\)|[^ |]+)")


def _nums(s):
    return [float(x) for x in s.strip("()").split(",") if x.strip()]


def xform(arr):
    """4x4 (mm) from a SolidWorks MathTransform array (rows of the 3x3 = images of the part X, Y, Z; translation m)."""
    T = np.eye(4)
    T[:3, :3] = np.asarray(arr[:9], float).reshape(3, 3).T
    T[:3, 3] = np.asarray(arr[9:12], float) * 1e3
    return T


# ------------------------------------------------------------------------------------------------ parsing (pure)
def parse(text):
    """{'comps': {name: {file, suppressed, T (4x4 mm), com (mm, part frame), vol_mm3, mass_kg, material}},
    'mates': [{name, type, kind, suppressed, ents: [{comp, reftype, params}]}], 'ints': [{vol_mm3, comps: [a, b]}]}"""
    comps, mates, ints = {}, [], []
    cur = None
    for raw in text.splitlines():
        line = raw.strip()
        if raw.startswith("COMP "):
            head, *rest = raw[5:].split(" | ")
            kv = dict(x.split("=", 1) for x in rest if "=" in x)
            cur = comps[head.strip()] = {"file": kv.get("file", ""), "suppressed": kv.get("suppressed") == "True"}
        elif raw.startswith("MATE "):
            head, *rest = raw[5:].split(" | ")
            kv = dict(x.split("=", 1) for x in rest if "=" in x)
            t = int(kv.get("type", -1))
            cur = {"name": head.strip(), "type": t, "kind": MATE_TYPES.get(t, str(t)), "suppressed": kv.get("suppressed") == "True", "ents": []}
            mates.append(cur)
        elif line.startswith("XFORM ") and cur is not None:
            cur["T"] = xform(_nums(line[6:]))
        elif line.startswith("MASS ") and cur is not None:
            kv = dict(_KV.findall(line[5:]))
            cur["com"] = np.asarray(_nums(kv["com"]), float) * 1e3
            cur["vol_mm3"] = float(kv["vol"]) * 1e9
            cur["mass_kg"] = float(kv.get("mass", "nan"))
        elif line.startswith("MATERIAL ") and cur is not None:
            cur["material"] = line[9:]
        elif line.startswith("ENT ") and cur is not None and "ents" in cur:
            m = re.match(r"ENT (\d+) comp=(.*?) reftype=(\d+) params=(.*)$", line)
            if m:
                cur["ents"].append({"comp": m[2].strip(), "reftype": int(m[3]), "params": _nums(m[4])})
        elif line.startswith("INT ") and "comps=" in line:
            kv = dict(_KV.findall(line.split("comps=")[0]))
            names = [x.strip() for x in line.split("comps=", 1)[1].split(";") if x.strip()]
            ints.append({"vol_mm3": float(kv["vol"]) * 1e9, "comps": names})
            cur = None
    return {"comps": comps, "mates": mates, "ints": ints}


@lru_cache(maxsize=4)
def load(path):
    return parse(Path(path).read_text(errors="replace"))


def _norm(s):
    return re.sub(r"[^a-z0-9]", "", s.lower())


def base(comp):
    """Component name without sub-assembly path and instance number: 'Micro slx v1.0-1/RV19 Hub Micro-1' -> 'RV19 Hub Micro'."""
    return re.sub(r"-\d+$", "", comp.split("/")[-1])


def pose_diff(A, B):
    """(origin distance mm, rotation angle deg) between two 4x4 frames."""
    R = A[:3, :3].T @ B[:3, :3]
    ang = float(np.degrees(np.arccos(np.clip((np.trace(R) - 1) / 2, -1, 1))))
    return float(np.linalg.norm(A[:3, 3] - B[:3, 3])), ang


def world_of(e, cfg):
    """4x4 STL/assembly frame -> our world frame for a reference_cad entry (ref_to_world, mirror_x, ref_shift)."""
    W = np.eye(4)
    T = e.get("ref_to_world", cfg.get("ref_to_world"))
    if T is not None:
        W = np.asarray(T, float) @ W
    if e.get("mirror_x"):
        W = np.diag([-1.0, 1, 1, 1]) @ W
    if e.get("ref_shift") is not None:
        S = np.eye(4)
        S[:3, 3] = e["ref_shift"]
        W = S @ W
    return W


# ------------------------------------------------------------------------------------------------ mapping
def part_map(ctx, asm):
    """{part id: (component name, reference_cad entry or None)} for the parts we can name in the assembly: `map`, else
    the entry's STL stem; among same-named components the one whose mass centre (assembly frame -> world by the
    config's ref_to_world) is nearest our part's. Entries with their own `ref_to_world` keep STLs in another frame, so
    our body, not the STL, is the reference point."""
    from .reference_cad import _cfg

    spec = ctx.r.spec
    cfg = _cfg(spec)
    ac = (spec.raw or {}).get("asm_dump") or {}
    W = world_of({}, cfg)
    out = {}
    for pid, comp in (ac.get("map") or {}).items():
        if comp in asm["comps"]:
            out[pid] = (comp, next((e for e in cfg.get("parts") or [] if e.get("part") == pid), None))
    taken = {c for c, _ in out.values()}
    for e in cfg.get("parts") or []:
        pid = e.get("part")
        if pid in out or not e.get("file"):
            continue
        stem = re.sub(r"_\d+$", "", Path(e["file"]).stem)
        cands = [c for c, v in asm["comps"].items() if _norm(base(c)) == _norm(stem) and "com" in v and "T" in v and c not in taken]
        if not cands:
            continue
        b = ctx.world.body(pid) if getattr(ctx, "world", None) is not None else None
        if len(cands) > 1 and b is not None and b.mesh is not None:
            ctr = np.asarray(b.mesh.center_mass if b.mesh.is_volume else b.mesh.bounds.mean(0), float)
            cands.sort(key=lambda c: float(np.linalg.norm((W @ asm["comps"][c]["T"] @ np.r_[asm["comps"][c]["com"], 1])[:3] - ctr)))
        out[pid] = (cands[0], e)
        taken.add(cands[0])
    return out


def _waiver(ctx, key):
    """(reason, valid) of `asm_dump.ok[key]`: valid when it cites the reference."""
    from .reference_cad import PATH_CITE

    why = (((ctx.r.spec.raw or {}).get("asm_dump") or {}).get("ok") or {}).get(key)
    if not why:
        return None, False
    return why, bool(PATH_CITE.search(str(why)))


def _asm(ctx):
    raw = ctx.r.spec.raw or {}
    p = ((raw.get("asm_dump") or {}).get("file")) or DEFAULT_FILE
    return load(str(p)) if Path(p).is_file() else None


def known_interference(ctx, a, b, vol_mm3):
    """Reason string when parts a, b also interfere in the reference assembly with our volume <= INT_FRAC x theirs."""
    try:
        asm = _asm(ctx)
        if asm is None:
            return None
        pm = getattr(ctx, "_asm_map", None)
        if pm is None:
            pm = ctx._asm_map = part_map(ctx, asm)
    except Exception:  # noqa: BLE001 - no waiver when the dump cannot be read
        return None
    ca, cb = (pm.get(a) or (None,))[0], (pm.get(b) or (None,))[0]
    if not ca or not cb:
        return None
    for it in asm["ints"]:
        cs = {c.split("/")[-1] if c not in asm["comps"] else c for c in it["comps"]}
        names = set(it["comps"])
        if ({ca, cb} <= names or {ca.split("/")[-1], cb.split("/")[-1]} <= cs) and vol_mm3 <= INT_FRAC * it["vol_mm3"]:
            return (f"SolidWorks interference report (rvrn 2.0.asmdump.txt) lists `{ca}` x `{cb}` at {it['vol_mm3']:.1f} mm3; "
                    f"ours {vol_mm3:.1f} mm3 <= {INT_FRAC:g}x")
    return None


# ------------------------------------------------------------------------------------------------ group
def _model(ctx, pid, e):
    import trimesh

    b = ctx.world.body(pid)
    if b is None or b.mesh is None:
        return None, None
    ms = [b.mesh] + [ctx.world.body(x).mesh for x in (e or {}).get("with_parts") or [] if ctx.world.body(x) is not None]
    return b, (ms[0] if len(ms) == 1 else trimesh.util.concatenate(ms))


def run(ctx):
    from .reference_cad import _cfg

    asm = _asm(ctx)
    if asm is None:
        return []
    cfg = _cfg(ctx.r.spec)
    pm = ctx._asm_map = part_map(ctx, asm)
    out = []
    pl_bad, pl_ok, ms_bad, ms_ok = [], [], [], []
    for pid, (comp, e) in sorted(pm.items()):
        c = asm["comps"][comp]
        b, mesh = _model(ctx, pid, e)
        if b is None:
            continue
        W = world_of({k: v for k, v in (e or {}).items() if k != "ref_to_world"}, cfg)   # assembly frame -> world
        ref = W @ c["T"]
        ours = np.asarray(b.M, float)
        if (e or {}).get("ref_frame") is not None:
            ours = ours @ np.asarray(e["ref_frame"], float)
        d, ang = pose_diff(ours, ref)
        row = (pid, comp, d, ang)
        if d <= PLACE_MM and ang <= PLACE_DEG:
            pl_ok.append(row)
        else:
            why, valid = _waiver(ctx, f"placement:{pid}")
            (pl_ok if valid else pl_bad).append(row + (why,))
        if mesh is not None and "vol_mm3" in c:
            vol = float(abs(mesh.volume))
            com = np.asarray(mesh.center_mass if mesh.is_volume else mesh.bounds.mean(0), float)
            rcom = (ref @ np.r_[c["com"], 1.0])[:3]
            dv, dc = vol / c["vol_mm3"] - 1 if c["vol_mm3"] else 0.0, float(np.linalg.norm(com - rcom))
            row = (pid, comp, dv, dc, vol, c["vol_mm3"])
            if abs(dv) <= VOL_FRAC and dc <= COM_MM:
                ms_ok.append(row)
            else:
                why, valid = _waiver(ctx, f"mass:{pid}")
                (ms_ok if valid else ms_bad).append(row + (why,))
    ctx.metrics["asm.placement"] = {r[0]: {"comp": r[1], "d_mm": round(r[2], 3), "deg": round(r[3], 3)} for r in pl_ok + pl_bad}
    ctx.metrics["asm.mass"] = {r[0]: {"comp": r[1], "dvol": round(r[2], 4), "dcom_mm": round(r[3], 3)} for r in ms_ok + ms_bad}

    def fmt_pl(r):
        return f"`{r[0]}` vs `{r[1]}`: origin {r[2]:.2f} mm, axes {r[3]:.2f} deg" + (f" (invalid waiver: {r[4]})" if len(r) > 4 and r[4] else "")

    def fmt_ms(r):
        return f"`{r[0]}` vs `{r[1]}`: volume {r[4]:.0f} vs {r[5]:.0f} mm3 ({r[2]:+.1%}), COM {r[3]:.2f} mm" + (f" (invalid waiver: {r[6]})" if len(r) > 6 and r[6] else "")

    head = f"{len(pl_ok)}/{len(pl_ok) + len(pl_bad)} parts within {PLACE_MM} mm / {PLACE_DEG} deg of the SolidWorks component transform"
    out.append(fail("asm.placement", G, BLOCKER, "Part frame differs from the reference assembly", head + ". " + "; ".join(fmt_pl(r) for r in pl_bad[:12]))
               .on(*[r[0] for r in pl_bad[:12]]).fix("Place the part (origin and axes) as the reference component, or declare `ref_frame` "
                                                      "with `ref_frame_reason` / an `asm_dump.ok` reason citing the reference.")
               if pl_bad else ok("asm.placement", G, "Every mapped part sits on its reference component transform", head + "."))
    head = f"{len(ms_ok)}/{len(ms_ok) + len(ms_bad)} parts within {VOL_FRAC:.0%} volume / {COM_MM} mm COM of the SolidWorks mass properties"
    out.append(fail("asm.mass", G, BLOCKER, "Part volume / mass centre differs from the reference", head + ". " + "; ".join(fmt_ms(r) for r in ms_bad[:12]))
               .on(*[r[0] for r in ms_bad[:12]]).fix("Match the material distribution (walls, pockets, bosses), or give an `asm_dump.ok` reason citing the reference.")
               if ms_bad else ok("asm.mass", G, "Every mapped part matches the reference volume and mass centre", head + "."))
    out += mate_findings(ctx, asm, pm)
    return out


def rig_pairs(ctx):
    """{frozenset(parent, child)} of our assembly mates: the Rig named by `asm_dump.rig` plus spec `mate` parts."""
    import importlib
    import sys

    spec = ctx.r.spec
    pairs = set()
    for p in spec.raw.get("parts") or []:
        if isinstance(p, dict) and isinstance(p.get("mate"), dict) and p["mate"].get("to"):
            pairs.add(frozenset((p["id"], p["mate"]["to"])))
    ref = ((spec.raw or {}).get("asm_dump") or {}).get("rig")
    if ref:
        mod, _, attr = ref.partition(":")
        src = str(Path(getattr(spec, "base_dir", ".") or ".") / "src")
        if src not in sys.path:
            sys.path.insert(0, src)
        rig = getattr(importlib.import_module(mod), attr or "RIG")
        rig = rig() if callable(rig) else rig
        for m in getattr(rig, "_mates", []):
            pairs.add(frozenset((m[0], m[2])))
    return pairs


def mate_findings(ctx, asm, pm):
    by_comp = {}
    for pid, (comp, _e) in pm.items():
        by_comp[comp] = pid
    try:
        pairs = rig_pairs(ctx)
    except Exception as ex:  # noqa: BLE001 - fail closed
        return [fail("asm.mate", G, BLOCKER, "Rig mates could not be read", f"{ex}")]
    hit, miss, unmapped, waived = [], [], [], []
    for m in asm["mates"]:
        if m["suppressed"] or len(m["ents"]) < 2:
            continue
        parts = []
        for en in m["ents"][:2]:
            c = en["comp"]
            pid = by_comp.get(c)
            if pid is None:   # a sub-assembly path: the leaf, or the sub-assembly itself
                pid = next((v for k, v in by_comp.items() if c.endswith("/" + k) or k.endswith("/" + c) or k.split("/")[0] == c), None)
            parts.append(pid)
        if None in parts:
            unmapped.append(f"{m['name']} ({' / '.join(e['comp'] for e in m['ents'][:2])})")
            continue
        if parts[0] == parts[1]:
            continue
        if frozenset(parts) in pairs:
            hit.append(m["name"])
            continue
        why, valid = _waiver(ctx, f"mate:{m['name']}")
        (waived if valid else miss).append(f"{m['name']} {m['kind']} `{parts[0]}`-`{parts[1]}`" + (f" (invalid waiver: {why})" if why else ""))
    ctx.metrics["asm.mate"] = {"hit": len(hit), "miss": len(miss), "waived": len(waived), "unmapped": len(unmapped)}
    msg = (f"{len(hit)}/{len(hit) + len(miss) + len(waived)} reference mates between mapped parts have a Rig mate"
           + (f", {len(waived)} reasoned" if waived else "") + (f"; {len(unmapped)} involve unmapped components (not checked)" if unmapped else ""))
    out = [fail("asm.mate", G, BLOCKER, "Reference mate without a Rig mate", msg + ". Missing: " + "; ".join(miss[:15]))
           .fix("Mate the two parts in the Rig (joints.py / assembly_rig.py) as the reference does, or give an `asm_dump.ok` "
                "\"mate:<name>\" reason citing the reference.")
           if miss else ok("asm.mate", G, "Every reference mate has a Rig mate", msg + ".")]
    if unmapped:
        out.append(note("asm.mate_unmapped", G, "Reference mates of components we do not model as parts", "; ".join(unmapped[:30])))
        ctx.not_checked.append(f"{len(unmapped)} reference mates of unmapped components (asm.mate)")
    return out
