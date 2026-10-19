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
    out += reference_bom(ctx)
    out += weapon_lock_part(ctx)
    out += belt_stock(ctx)
    out += wire_cut(ctx)
    out += switch_direction(ctx)
    out += doc_consistency(ctx)
    return out


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
        mid = (lo + hi) / 2
        d = np.asarray(c, float) - mid
        d[2] = 0.0
        ax = int(np.argmax(np.abs(d[:2]) / np.maximum((hi - lo)[:2] / 2, 1e-6)))
        outward = np.zeros(3)
        outward[ax] = math.copysign(1.0, d[ax])
        v = np.asarray(od, float)
        v = v / (np.linalg.norm(v) or 1.0)
        if float(v @ outward) < SWITCH_DIR_COS:
            out.append(fail("electrical.switch_direction", G, BLOCKER, "Switch turns off the wrong way",
                            f"`{p.id}` switches off along {list(np.round(v, 2))}, not outward through its face ({list(outward)}): pulling the slider out from the outside must turn it off.")
                       .on(p.id).here(c).fix("Turn the switch round so OFF is the outward (pulled) position."))
        else:
            out.append(ok("electrical.switch_direction", G, "Switch pulls outward to OFF", f"`{p.id}` switches off when pulled out through its face."))
    return out


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
