"""Part integrity (`integrity`, opt-out, every part, runs first): each part is one valid closed solid of the right size.

Catches a CAD build that silently collapsed (e.g. a fillet that made a boolean cut shred a tub into 7 slivers of
413 mm3 instead of 1 solid of ~16000 mm3), which otherwise only shows up later as confusing downstream findings.

  integrity.solids (BLOCKER)  the part mesh is not exactly `solids` (default 1) closed, consistently wound shells.
                              A part may declare `"solids": n` with `"solids_reason": "..."` (reason REQUIRED).
  integrity.volume            volume vs each reference available: the part's declared `volume_mm3`, its
                              reference_cad mesh volume when mapped, and the previous passing run's volume (stored
                              per spec in <cache_dir>/integrity/<spec>.json). Within `tol` (10 %) of any -> pass;
                              below `collapse` (50 %) of every one -> BLOCKER; otherwise WARNING.
  integrity.nonempty (BLOCKER) the part's shape is empty: no faces or zero volume (e.g. a boolean cut away everything, a
                              radius that made a ring's inside larger than its outside). Judged for EVERY part,
                              catalogue or made, even when `integrity` is opted out or `solids` is declared.
Opt out (all but nonempty): spec "integrity": {"enabled": false}; params "integrity": {"tol": 0.1, "collapse": 0.5}.
Cheap: mesh connected components and the B-rep volume already in the geometry cache; no booleans.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from ..finding import BLOCKER, WARNING, fail, ok

G = "integrity"
DEFAULTS = {"tol": 0.10, "collapse": 0.50}


def params(raw):
    p = dict(DEFAULTS)
    c = (raw or {}).get("integrity") or {}
    if isinstance(c, dict):
        p.update({k: float(v) for k, v in c.items() if k in DEFAULTS})
    return p


def enabled(raw):
    c = (raw or {}).get("integrity")
    return not (c is False or (isinstance(c, dict) and c.get("enabled") is False))


def shells(m):
    """(outer closed shells, open/inconsistent component count) of a trimesh mesh. Inner void shells (negative signed
    volume) belong to their outer shell and are not counted."""
    import trimesh

    if len(m.faces) == 0:
        return 0, 0
    labels = trimesh.graph.connected_components(m.face_adjacency, nodes=np.arange(len(m.faces)), min_len=1)
    outer = bad = 0
    for faces in labels:
        c = m.submesh([faces], append=True, repair=False)
        if not (c.is_watertight and c.is_winding_consistent):
            bad += 1
        elif c.volume > 0:
            outer += 1
    return outer, bad


def store_path(spec_name):
    from ..geom import cache_dir

    return cache_dir() / "integrity" / f"{spec_name or 'spec'}.json"


def _load(path):
    try:
        return json.loads(Path(path).read_text())
    except Exception:  # noqa: BLE001 - missing or broken store = no previous volumes
        return {}


def ref_volumes(spec):
    """{part id: reference_cad mesh volume mm3} for mapped, watertight reference meshes."""
    c = (spec.raw or {}).get("reference_cad") or {}
    c = c if isinstance(c, dict) else {"parts": list(c)}
    rdir = Path(getattr(spec, "base_dir", ".") or ".") / (c.get("dir") or ".")
    out = {}
    for e in c.get("parts") or []:
        pid, fn = e.get("part"), e.get("file")
        if not pid or not fn or e.get("with_parts") or not (rdir / fn).is_file():
            continue
        try:
            import trimesh

            m = trimesh.load(rdir / fn, force="mesh")
            if m.is_watertight:
                out[pid] = abs(float(m.volume)) * float(e.get("scale", 1.0)) ** 3
        except Exception:  # noqa: BLE001 - reference_cad reports unusable files
            pass
    return out


def _mesh_and_volume(rp):
    g = rp.geom
    m = g.mesh
    v = float(getattr(g, "volume", 0.0) or 0.0)
    return m, (v if v > 0 else abs(float(m.volume)))


EMPTY_VOLUME_MM3 = 1e-6   # a shape this small has no material (mesh noise of a collapsed boolean)


def is_empty(rp):
    """True when the part's mesh has no faces or its volume is nil."""
    m, vol = _mesh_and_volume(rp)
    return len(m.faces) == 0 or vol <= EMPTY_VOLUME_MM3


def empty_findings(ctx, parts=None):
    """integrity.nonempty for every spec part (None-geometry parts are reported empty too); returns (findings, empty ids)."""
    out, empty = [], set()
    for rp in ctx.r.parts:
        pid = rp.part.id
        if parts is not None and pid not in parts:
            continue
        try:
            gone = is_empty(rp)
        except Exception:  # noqa: BLE001 - a part whose geometry cannot even be read has no usable shape
            gone = True
        if gone:
            empty.add(pid)
            out.append(fail("integrity.nonempty", G, BLOCKER, "Part shape is empty",
                            f"`{pid}` has no volume: its CAD build returned an empty shape (a boolean removed everything, or a "
                            f"ring whose inner radius is not below its outer).").on(pid)
                       .fix("Fix the part's build so it returns a solid; print its volume and check the last boolean."))
    return out, empty


def run(ctx, parts=None):
    spec = ctx.r.spec
    raw = spec.raw or {}
    out, empty = empty_findings(ctx, parts)
    if not enabled(raw):
        ctx.not_checked.append("Part integrity (solid count, volume collapse): opted out")
        return out
    p = params(raw)
    store = store_path(getattr(spec, "name", None))
    prev = _load(store)
    refs = ref_volumes(spec)
    keep = dict(prev)
    for rp in ctx.r.parts:
        part = rp.part
        pid = part.id
        if parts is not None and pid not in parts or pid in empty:
            continue
        ex = getattr(part, "_extra", {}) or {}
        m, vol = _mesh_and_volume(rp)
        n, bad = shells(m)
        want, why = 1, ""
        if "solids" in ex:
            why = str(ex.get("solids_reason") or "").strip()
            if why:
                want = int(ex["solids"])
            else:
                out.append(fail("integrity.solids_reason", G, BLOCKER, "`solids` declared without a reason",
                                f"`{pid}` declares solids: {ex['solids']} but no `solids_reason`; expecting 1.").on(pid))
        blocked = False
        if n != want or bad:
            blocked = True
            out.append(fail("integrity.solids", G, BLOCKER, "Part is not one valid closed solid",
                            f"`{pid}` has {n} closed solid(s) and {bad} open/invalid shell(s), expected {want} "
                            f"({vol:.0f} mm3). A boolean or fillet probably collapsed the build.").on(pid)
                       .fix("Check the last CAD op (fillet/cut order); or declare `solids` with `solids_reason`."))
        else:
            out.append(ok("integrity.solids", G, "Part is one valid closed solid",
                          f"`{pid}`: {n} closed solid(s){' (' + why + ')' if why else ''}").on(pid))
        exp = {}
        if ex.get("volume_mm3"):
            exp["declared"] = float(ex["volume_mm3"])
        if pid in refs:
            exp["reference_cad"] = refs[pid]
        if pid in prev:
            exp["previous"] = float(prev[pid])
        if exp:
            rel = {k: (vol - v) / v for k, v in exp.items() if v > 0}
            txt = ", ".join(f"{k} {exp[k]:.0f} ({rel[k]:+.0%})" for k in rel)
            msg = f"`{pid}` volume {vol:.0f} mm3 vs {txt}"
            if any(abs(r) <= p["tol"] for r in rel.values()):
                out.append(ok("integrity.volume", G, "Part volume as expected", msg).on(pid))
            elif rel and all(vol < p["collapse"] * exp[k] for k in rel):
                blocked = True
                out.append(fail("integrity.volume", G, BLOCKER, "Part volume collapsed", msg).on(pid)
                           .fix("The solid lost most of its material: check the last boolean/fillet."))
            else:
                out.append(fail("integrity.volume", G, WARNING, "Part volume changed more than "
                                f"{p['tol']:.0%}", msg).on(pid)
                           .fix("'Previous' is the last passing run's volume, stored in "
                                f"{store_path(getattr(spec, 'name', None))}. If the change is intended: set `volume_mm3` on the part, or "
                                "delete that file to accept the new geometry as the baseline."))
        if not blocked:
            keep[pid] = vol
    if keep != prev:
        try:
            store.parent.mkdir(parents=True, exist_ok=True)
            store.write_text(json.dumps(keep, indent=1, sort_keys=True))
        except OSError:
            pass
    return out
