"""Reference bill of materials and the build-guide details that geometry checks cannot see: which screws hold which
joint (count, size, head, thread host), the battery and phase connectors, a physical weapon-lock part, a stock O-ring,
wires crossing a quick-change module boundary, the switch's OFF direction and a reference write-up that matches the spec.

Spec keys (all optional; a check only runs when its data is declared):
- `reference_bom: [{role, kind: fastener|part|wire, match: [id globs], count, designation, head, threads_into,
  material, connector, optional, deviation}]` from the reference build guide.
- `reference_doc: {path, must_mention: [...], must_not_mention: [...]}` (path relative to the spec).
- part `off_dir: [x, y, z]` on switches (direction the slider moves to switch OFF).
- belt `stock: {id_mm, cs_mm}` on O-ring belts.
- wire `connector` on wires that cross a module boundary.
"""

from __future__ import annotations

import fnmatch
import math
import re
from pathlib import Path

import numpy as np

from .. import catalog
from ..finding import BLOCKER, WARNING, fail, ok

G = "bom"

# Stock metric nitrile O-rings (ID mm) per cross-section (mm), as sold in assortment boxes / by the piece.
STOCK_ORINGS = {
    1.0: [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 22, 24, 25, 26, 28, 30, 32, 34, 35, 36, 38, 40, 42, 45, 48, 50],
    1.5: [5, 6, 7, 8, 9, 10, 12, 14, 15, 16, 18, 20, 22, 24, 25, 26, 28, 30, 32, 35, 36, 38, 40, 42, 45, 48, 50, 55, 60],
    2.0: [5, 6, 8, 10, 12, 14, 15, 16, 18, 20, 22, 24, 25, 26, 28, 30, 32, 35, 38, 40, 42, 45, 48, 50, 55, 60, 65, 70],
}
ORING_LEN_TOL = 0.03       # declared inner circumference within 3 % of pi * stock ID
SWITCH_DIR_COS = math.cos(math.radians(30.0))
HEADS = {"socket": "socket", "cap": "socket", "button": "button", "countersunk": "countersunk", "csk": "countersunk",
         "flat": "countersunk", "pan": "pan", "grub": "grub", "set": "grub"}


def _x(o, k, default=None):
    v = getattr(o, k, None)
    if v is None:
        v = (getattr(o, "_extra", None) or {}).get(k, default)
    return v if v is not None else default


def _match(ids, pats):
    return [i for i in ids if any(fnmatch.fnmatchcase(i, p) for p in pats)]


def _host_kind(r, host):
    """What a screw threads into: nut / insert / standoff / motor / tapped (a part's own plastic or metal)."""
    if not host:
        return "none"
    p = r.spec.part(host)
    if p is None:
        return "missing"
    role = (_x(p, "role") or "").lower()
    if p.kind in ("nut", "insert"):
        return p.kind
    if role == "standoff" or p.kind == "standoff" or "standoff" in (p.label or "").lower() or host.startswith("so_"):
        return "standoff"
    if p.kind in ("motor", "weapon_motor"):
        return "motor"
    if p.kind == "switch":
        return "part"
    return "tapped"


def run(ctx):
    out = []
    out += waiver_schema(ctx)
    out += added_parts(ctx)
    out += reference_bom(ctx)
    out += weapon_lock_part(ctx)
    out += belt_stock(ctx)
    out += wire_cut(ctx)
    out += switch_direction(ctx)
    out += doc_consistency(ctx)
    return out


# ------------------------------------------------------------------------------------------------ spec.waiver_schema
# Waiver / deviation keys some check actually reads. A waiver-shaped key outside this set waives nothing, so it is a
# BLOCKER (e.g. `sharp_corner_deviation`, read by no check, sat on parts looking like a valid opt-out).
WAIVER_KEY = re.compile(r"deviation|waive|exempt|allow_|_ok$|^ok_|ignore|skip")
KNOWN_WAIVERS = {
    "deviation", "deviations", "sharp_corners_ok", "sharp_ok", "ref_ok", "exempt", "waive", "waivers",
    "cover_fasteners_deviation", "thin_wall_deviation", "param_exempt", "allow_overlap", "visual_ok",
    "wire_avoid_ok", "rotor_ok", "render_ok", "offset_ok", "reference_deviation_ids", "practice_ok", "no_contact_ok",
    "assembly_ok", "rub_gap_ok",
}

INTENT_WAIVERS = {"exempt", "gap_ok"}


def _keys(o):
    if isinstance(o, dict):
        return list(o)
    return list(getattr(o, "_extra", {}) or {}) + [k for k in vars(o) if not k.startswith("_")]


def waiver_schema(ctx):
    sp = ctx.r.spec
    bad = []
    for where, objs in (("part", sp.parts), ("fastener", sp.fasteners), ("wire", sp.wires)):
        for o in objs:
            bad += [f"{where} `{o.id}`: `{k}`" for k in _keys(o) if WAIVER_KEY.search(k) and k not in KNOWN_WAIVERS]
    bad += [f"spec: `{k}`" for k in (sp.raw or {}) if WAIVER_KEY.search(k) and k not in KNOWN_WAIVERS]
    for e in (sp.raw or {}).get("intent") or []:   # intent rules read only these (a `waive` text there is ignored)
        if isinstance(e, dict):
            bad += [f"intent `{e.get('rule')}` on `{e.get('part')}`: `{k}`" for k in e if WAIVER_KEY.search(k) and k not in INTENT_WAIVERS]
    if not bad:
        return [ok("spec.waiver_schema", G, "Waiver keys known", "Every waiver/deviation key is one a check reads.")]
    return [fail("spec.waiver_schema", G, BLOCKER, "Unknown waiver key",
                 f"{len(bad)} waiver/deviation key(s) no check reads, so they waive nothing: " + "; ".join(bad))
            .fix("Use a key a check reads (" + ", ".join(sorted(KNOWN_WAIVERS)) + ") or delete it.")]


# ------------------------------------------------------------------------------------------------ bom.added_parts
def added_parts(ctx):
    """A part declared `deviation` (added, not in the reference) must still be listed in reference_bom."""
    sp = ctx.r.spec
    rows = (sp.raw or {}).get("reference_bom")
    if not rows:
        return []
    listed = set()
    for row in rows:
        if row.get("kind", "fastener") == "part":
            listed.update(_match([p.id for p in sp.parts], row.get("match") or []))
    miss = [p.id for p in sp.parts if _x(p, "deviation") and p.id not in listed]
    if not miss:
        return [ok("bom.added_parts", G, "Added parts in BOM", "Every part declared `deviation` has a reference_bom row.")]
    return [fail("bom.added_parts", G, BLOCKER, "Added part missing from BOM",
                 "Part(s) declared `deviation` (added) with no reference_bom row: " + ", ".join(f"`{i}`" for i in miss))
            .on(*miss).fix('Add a reference_bom row {"kind": "part", "role": ..., "match": [id], "count": 1, "deviation": "<why added>"}.')]


# ------------------------------------------------------------------------------------------------ reference.bom
def reference_bom(ctx):
    r = ctx.r
    rows = (r.spec.raw or {}).get("reference_bom")
    if not rows:
        return []
    out, good = [], 0
    fasts = {f.id: f for f in r.spec.fasteners}
    parts = {p.id: p for p in r.spec.parts}
    wires = {w.id: w for w in r.spec.wires}
    covered = set()
    for row in rows:
        kind = row.get("kind", "fastener")
        pool = fasts if kind == "fastener" else parts if kind == "part" else wires
        ids = _match(list(pool), row.get("match") or [])
        covered.update(ids if kind == "fastener" else [])
        role = row.get("role", "?")
        dev = row.get("deviation")
        probs = []
        n = row.get("count")
        if n is not None and len(ids) != n and not (row.get("optional") and not ids):
            probs.append(f"count {len(ids)} vs reference {n}")
        for i in ids:
            o = pool[i]
            if kind == "fastener":
                want = row.get("designation")
                if want:
                    got = catalog.parse_designation(o.designation)
                    ref = catalog.parse_designation(want) if "x" in want.lower() else None
                    if ref is not None and got is not None and (abs(got[0] - ref[0]) > 1e-6 or abs(got[1] - ref[1]) > row.get("length_tol_mm", 0.0) + 1e-6):
                        probs.append(f"`{i}` is {o.designation}, reference {want}")
                    elif ref is None and got is not None and abs(got[0] - float(want.upper().lstrip("M"))) > 1e-6:
                        probs.append(f"`{i}` is {o.designation}, reference {want}")
                h = row.get("head")
                if h and HEADS.get((o.head or "socket").lower(), o.head) != HEADS.get(h.lower(), h):
                    probs.append(f"`{i}` head {o.head or 'socket'}, reference {h}")
                t = row.get("threads_into")
                if t and _host_kind(r, o.threads_into) != t:
                    probs.append(f"`{i}` threads into {_host_kind(r, o.threads_into)} (`{o.threads_into}`), reference {t}")
                m = row.get("material")
                if m and (_x(o, "material") or "steel") != m:
                    probs.append(f"`{i}` is {_x(o, 'material') or 'steel'}, reference {m}")
            elif kind == "part":
                c = row.get("catalog")
                if c and o.catalog != c:
                    probs.append(f"`{i}` is catalog `{o.catalog}`, reference `{c}`")
                m = row.get("material")
                if m and o.material != m:
                    probs.append(f"`{i}` is {o.material}, reference {m}")
            else:
                c = row.get("connector")
                if c and _x(o, "connector") != c:
                    probs.append(f"wire `{i}` connector {_x(o, 'connector')}, reference {c}")
        if probs and dev:
            out.append(ok("reference.bom", G, f"BOM row '{role}' deviates by design",
                          f"{'; '.join(probs)}. Declared deviation: {dev}"))
            good += 1
        elif probs:
            out.append(fail("reference.bom", G, BLOCKER, f"Does not match the reference BOM: {role}",
                            f"Reference BOM row '{role}': {'; '.join(probs)}.")
                       .on(*[i for i in ids if i in parts][:8])
                       .fix("Use the build guide's part (count, size, head, thread host), or add `deviation` with the reason to the row."))
        else:
            good += 1
    extra = sorted(set(fasts) - covered)
    if extra:
        out.append(fail("reference.bom_extra", G, WARNING, "Screws not in the reference BOM",
                        f"{len(extra)} fastener(s) match no `reference_bom` row: {', '.join(extra[:12])}.")
                   .fix("Add a BOM row for them (with `deviation` if the reference has none)."))
    if good and not any(f.id == "reference.bom" and not f.passed for f in out):
        out.append(ok("reference.bom", G, "Matches the reference BOM", f"{good} of {len(rows)} BOM rows match the spec (count, size, head, thread host, connector)."))
    return out


# ------------------------------------------------------------------------------------------------ weapon lock part
def weapon_lock_part(ctx):
    r, w = ctx.r, ctx.world
    if not r.spec.is_spinner:
        return []
    lock = (r.spec.raw or {}).get("weapon_lock") or {}
    wps = [p for p in r.spec.parts if p.weapon is not None and p.weapon.kind != "none"]
    if not wps:
        return []
    out = []
    for p in wps:
        bar = r.spec.part(p.weapon.locking_bar) if p.weapon.locking_bar else None
        if bar is None:
            if lock.get("require_part"):
                out.append(fail("legal.weapon_lock_part", G, BLOCKER, "Weapon lock is only declared, not modelled",
                                f"`{p.id}` has no `weapon.locking_bar` part: a declared pin cannot be weighed, printed or checked against the rotor.")
                           .on(p.id).fix("Model the lock (e.g. the printed TPU tooth stop) as a part and name it in `weapon.locking_bar`."))
            continue
        if w.body(bar.id) is None:
            out.append(fail("legal.weapon_lock_part", G, BLOCKER, "Weapon lock has no geometry", f"`{bar.id}` has no body.").on(bar.id))
            continue
        out.append(ok("legal.weapon_lock_part", G, "Weapon lock is a real part",
                      f"`{bar.id}` ({bar.material or bar.catalog or 'part'}) is modelled and named as the lock of `{p.id}`."))
    return out


# ------------------------------------------------------------------------------------------------ kin.belt_stock
def belt_stock(ctx):
    out = []
    for p in ctx.r.spec.parts:
        b = p.belt
        if b is None or (b.kind or "o_ring") != "o_ring":
            continue
        st = _x(b, "stock") or {}
        idm, cs = st.get("id_mm"), st.get("cs_mm")
        if idm is None or cs is None:
            out.append(fail("kin.belt_stock", G, BLOCKER, "O-ring is not a stock size",
                            f"`{p.id}` declares no `belt.stock` (id_mm, cs_mm): a {b.length_mm} mm loop is not something you can buy.")
                       .on(p.id).fix("Pick a stock O-ring (ID x CS) and set `belt.stock`; length_mm = pi x ID."))
            continue
        sizes = STOCK_ORINGS.get(round(float(cs), 2))
        if sizes is None or float(idm) not in [float(s) for s in sizes]:
            out.append(fail("kin.belt_stock", G, BLOCKER, "O-ring is not a stock size",
                            f"`{p.id}`: {idm} x {cs} mm is not in the stock metric O-ring list.").on(p.id)
                       .fix(f"Use a stock size, e.g. CS 1.0 IDs {STOCK_ORINGS[1.0][-12:]}."))
            continue
        circ = math.pi * float(idm)
        if b.length_mm is None or abs(b.length_mm - circ) > ORING_LEN_TOL * circ:
            out.append(fail("kin.belt_stock", G, BLOCKER, "Belt length is not the O-ring's",
                            f"`{p.id}`: length_mm {b.length_mm} vs pi x {idm} = {circ:.1f} mm for the declared stock ring.").on(p.id))
            continue
        if b.width_mm and abs(float(b.width_mm) - float(cs)) > 0.05:
            out.append(fail("kin.belt_stock", G, BLOCKER, "Belt section is not the O-ring's",
                            f"`{p.id}`: width_mm {b.width_mm} vs stock cross-section {cs} mm.").on(p.id))
            continue
        out.append(ok("kin.belt_stock", G, "Stock O-ring", f"`{p.id}` is a stock {idm:g} x {cs:g} mm nitrile O-ring ({circ:.1f} mm inner circumference)."))
    return out


# ------------------------------------------------------------------------------------------------ disasm.wire_cut
def wire_cut(ctx):
    r = ctx.r
    mods = (r.spec.raw or {}).get("modules") or []
    out = []
    for m in mods:
        inside = set(m.get("parts") or []) | ({m["root"]} if m.get("root") else set())
        bad, okw = [], 0
        for wi in r.spec.wires:
            a, b = (getattr(wi, "from") or "").split(".")[0], (wi.to or "").split(".")[0]
            if (a in inside) == (b in inside):
                continue
            if _x(wi, "connector"):
                okw += 1
            else:
                bad.append(wi.id)
        if bad:
            out.append(fail("disasm.wire_cut", G, BLOCKER, "Module removal cuts a wire",
                            f"Module `{m.get('id')}` is wired to the rest by {', '.join(bad)} with no connector: removing it means desoldering.")
                       .on(*bad).fix("Add an in-line connector (e.g. 2 mm bullets on the motor phases) and declare `connector` on the wire."))
        elif okw:
            out.append(ok("disasm.wire_cut", G, "Module unplugs", f"Module `{m.get('id')}`: {okw} wire(s) cross its boundary, all through connectors."))
    return out


# ------------------------------------------------------------------------------------------------ switch direction
def switch_direction(ctx):
    r, w = ctx.r, ctx.world
    out = []
    lo = np.min([b.aabb[0] for b in w.bodies if b.part_idx is not None], axis=0) if w.bodies else None
    hi = np.max([b.aabb[1] for b in w.bodies if b.part_idx is not None], axis=0) if w.bodies else None
    for p in r.spec.parts:
        if p.kind != "switch":
            continue
        od = _x(p, "off_dir")
        b = w.body(p.id)
        if od is None:
            out.append(fail("electrical.switch_direction", G, WARNING, "Switch OFF direction not declared",
                            f"`{p.id}` does not say which way is OFF; the build guide's rule (e.g. pulled outward = off) cannot be checked.")
                       .on(p.id).fix("Set `off_dir` (world vector the slider moves to switch off)."))
            continue
        if b is None or lo is None:
            ctx.not_checked.append(f"Switch `{p.id}` direction: no body")
            continue
        c = b.center
        v = np.asarray(od, float)
        v = v / (np.linalg.norm(v) or 1.0)
        face = _switch_face(r, w, b, lo, hi)
        if face is None:
            out.append(fail("electrical.switch_direction", G, BLOCKER, "Switch cannot be reached from outside",
                            f"`{p.id}` is covered on every side; the slider must be reachable from outside the robot.")
                       .on(p.id).here(c).fix("Move the switch to an exterior face or open an access slot over it."))
            continue
        n = np.asarray(face, float)
        if float(v @ n) >= SWITCH_DIR_COS:
            out.append(ok("electrical.switch_direction", G, "Switch pulls outward to OFF", f"`{p.id}` switches off when pulled out through its face."))
        elif n[2] != 0.0 and abs(float(v @ n)) < 1.0 - SWITCH_DIR_COS:
            # deck/top (or belly) mount: the lever is reached through the face and slides in its plane; the declared
            # direction is the OFF throw, and with no "outward" in that plane any declared in-plane throw is accepted
            out.append(ok("electrical.switch_direction", G, "Switch OFF throw declared on an exposed deck",
                          f"`{p.id}` is reached from {'+z' if n[2] > 0 else '-z'} and slides to OFF along {[round(float(x), 2) for x in v]}."))
        else:
            out.append(fail("electrical.switch_direction", G, BLOCKER, "Switch turns off the wrong way",
                            f"`{p.id}` switches off along {list(np.round(v, 2))}, not outward through its face ({list(n)}): pulling the slider out from the outside must turn it off.")
                       .on(p.id).here(c).fix("Turn the switch round so OFF is the outward (pulled) position."))
    return out


def _switch_face(r, w, b, lo, hi):
    """Outward normal of the exterior face the switch is reached through. For each of the six axis directions, rays are
    cast outward from the switch's extreme points on that side (its lever, for a deck mount poking through a slot); the
    side is open when at least one ray escapes every other part. Of the open sides, a side wall within 2 mm wins
    (side mount), else the nearest open face. WHY: OFF must be judged against where a hand actually reaches the slider."""
    v = np.asarray(b.mesh.vertices)
    found = []
    for k in range(3):
        for sgn in (1.0, -1.0):
            n = np.zeros(3)
            n[k] = sgn
            proj = v @ n
            pts = v[proj >= proj.max() - 0.5]
            if len(pts) > 64:
                pts = pts[np.linspace(0, len(pts) - 1, 64).astype(int)]
            org = pts + n * 0.05
            free = np.ones(len(org), bool)
            for o in w.bodies:
                if o is b or o.is_wire or o.fastener or o.part_idx is None:
                    continue
                far = org + n * 1.0e3
                if not np.all((np.minimum(org.min(0), far.min(0)) <= o.aabb[1]) & (np.maximum(org.max(0), far.max(0)) >= o.aabb[0])):
                    continue
                idx = np.flatnonzero(free)
                if not len(idx):
                    break
                hit = o.mesh.ray.intersects_any(org[idx], np.tile(n, (len(idx), 1)))
                free[idx[hit]] = False
            if free.any():
                dist = float((hi[k] - proj.max()) if sgn > 0 else (-proj.max() - lo[k]))
                found.append((dist, k, n))
    if not found:
        return None
    # a switch within 2 mm of an open side wall is side-mounted (pulled out sideways); otherwise the nearest open face
    side = [f for f in found if f[1] < 2 and f[0] <= 2.0]
    return min(side or found, key=lambda f: f[0])[2]


# ------------------------------------------------------------------------------------------------ reference.doc_consistency
def doc_consistency(ctx):
    r = ctx.r
    doc = (r.spec.raw or {}).get("reference_doc")
    if not doc:
        return []
    path = Path(doc.get("path", ""))
    if not path.is_absolute():
        path = Path(r.spec.base_dir) / path
    try:
        text = path.read_text().lower()
    except OSError:
        ctx.not_checked.append(f"Reference write-up `{path}` could not be read")
        return []
    missing = [t for t in doc.get("must_mention") or [] if t.lower() not in text]
    stale = [t for t in doc.get("must_not_mention") or [] if t.lower() in text]
    if missing or stale:
        msg = "; ".join(x for x in (f"does not mention {missing}" if missing else "", f"still says {stale}" if stale else "") if x)
        return [fail("reference.doc_consistency", G, BLOCKER, "Reference write-up is out of date", f"`{path.name}` {msg}.")
                .fix("Rewrite the reference notes to the modelled design.")]
    return [ok("reference.doc_consistency", G, "Reference write-up matches the spec", f"`{path.name}` names the modelled parts and none of the retired ones.")]
