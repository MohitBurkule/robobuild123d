"""Copy-of-a-real-robot gate (`likeness.*`): a spec that sits next to reference photos must LOOK like them and must not
be a stock template or another robot's spec with a new name.

Active when the spec's folder has `reference/` photos or a `REFERENCE.json` (photo-read facts written by whoever
collected the photos, NOT by the builder). All findings are blockers:

- likeness.template_copy   made-part voxel IoU >= 0.80 with a bundled template (robot/templates), or >= 0.80 shape
                           fingerprint overlap with a sibling robots/<other>/spec.json.
- likeness.no_reference    no `reference` entry with a photo from reference/ and a mask.
- likeness.mask_source     the mask is not the photo's own silhouette (`robot mask` of that photo, IoU < 0.85), so it
                           was drawn to fit the model.
- likeness.silhouette      best IoU of the model's silhouette (any camera around the robot, mirrored or not) with the
                           photo mask is below 0.70, or not clearly better (+0.05) than the stock template's.
- likeness.type            spec robot_type / wheel count differ from REFERENCE.json.
- REFERENCE.json may also carry `photos` [usable photo file names; each needs an entry] and `mask_thr` {photo: thr}
  (the collector's `robot mask --thr` where the default picks up the floor) and `crop` {photo: [x0,y0,x1,y1] 0..1} and `mask_mode` {photo: "textured"}
  (keep one robot when the photo shows two).
- likeness.weapon          REFERENCE.json `weapon` {kind, axis, position, width_frac, teeth}: weapon part missing, wrong
                           kind, wrong axis, wrong place, wrong width (+-25 %), wrong tooth count.
"""

from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from ..finding import BLOCKER, fail, ok

G = "likeness"
COPY_IOU = 0.80
SIL_MIN = 0.80  # absolute floor (stock templates already reach 0.69-0.81 on iso photos, so 0.70 let blobs pass)
SIL_STRONG = 0.85
SIL_MARGIN = 0.0  # at least as close to the photo as the closest stock template (copies are caught by template_copy)
MASK_MIN = 0.85
VOX = 2.0
IMG = (".png", ".jpg", ".jpeg", ".webp")
TEMPLATES = Path(__file__).resolve().parents[1] / "templates"


def _base(spec):
    return Path(getattr(spec, "base_dir", ".") or ".")


def active(spec) -> bool:
    b = _base(spec)
    return (b / "REFERENCE.json").exists() or any(p.suffix.lower() in IMG for p in (b / "reference").glob("*"))


def folder_key(spec) -> str:
    """Hash of what this group reads outside the spec: the folder's photos + REFERENCE.json and sibling specs."""
    import hashlib
    h = hashlib.sha256()
    b = _base(spec)
    files = [b / "REFERENCE.json", *sorted((b / "reference").glob("*"))]
    if b.parent.name == "robots":
        files += [p for p in sorted(b.parent.glob("*/spec.json")) if p.parent.resolve() != b.resolve()]
    for p in files:
        if p.is_file():
            h.update(str(p.name).encode())
            h.update(p.read_bytes())
    return h.hexdigest()


def _made(world, r):
    out = []
    for b in world.bodies:
        if b.part_idx is None or b.fastener or b.is_wire:
            continue
        rp = r.parts[b.part_idx]
        if rp.cat is None:
            out.append(b)
    return out


def _vox(bodies):
    from .. import cache
    pts = []
    for b in bodies:
        lo, hi = b.aabb
        g = [np.arange(lo[i] + VOX / 2, hi[i], VOX) for i in range(3)]
        if any(len(x) == 0 for x in g):
            continue
        P = np.stack(np.meshgrid(*g, indexing="ij"), -1).reshape(-1, 3)
        P = P[b.inside(P)]
        pts.append(np.round(P / VOX).astype(int))
    if not pts:
        return set()
    return set(map(tuple, np.concatenate(pts)))


def _jac(a, b):
    u = len(a | b)
    return len(a & b) / u if u else 0.0


def _fp(raw):
    """Rounded (1 mm) canonical JSON of every made part's shape + pose: survives renames and id changes."""
    out = set()
    for p in raw.get("parts") or []:
        if p.get("catalog"):
            continue
        s = json.dumps({"shape": p.get("shape"), "at": p.get("at"), "rot": p.get("rot")}, sort_keys=True,
                       default=lambda o: round(o) if isinstance(o, float) else str(o))
        s = json.loads(s, parse_float=lambda x: round(float(x)))
        out.add(json.dumps(s, sort_keys=True))
    return out


def copies(ctx, tws=None):
    r, w = ctx.r, ctx.world
    out = []
    mine = _vox(_made(w, r))
    for name, (tv, _) in template_data().items():
        j = _jac(mine, tv)
        if j >= COPY_IOU:
            out.append(fail("likeness.template_copy", G, BLOCKER, "Robot is a stock template",
                            f"Made parts overlap template `{name}` at voxel IoU {j:.2f} (limit {COPY_IOU:.2f}): this is the "
                            "template, not the robot in the photos.")
                       .fix("Rebuild the chassis, weapon and armour to the photo proportions (`robot mask` + "
                            "`likeness.silhouette` show where it differs)."))
    base = _base(r.spec)
    me = _fp(r.spec.raw or {})
    robots = base.parent
    if me and robots.name == "robots":
        for sib in sorted(robots.glob("*/spec.json")):
            if sib.parent.resolve() == base.resolve():
                continue
            try:
                other = _fp(json.loads(sib.read_text()))
            except Exception:  # noqa: BLE001
                continue
            j = _jac(me, other)
            if j >= COPY_IOU:
                out.append(fail("likeness.template_copy", G, BLOCKER, "Robot copies another robot",
                                f"{j:.0%} of the made-part shapes equal `{sib.parent.name}`'s spec (limit {COPY_IOU:.0%}).")
                           .fix("Each robot must be modelled from its own photos."))
    return out


def _dirs():
    out = []
    for el in (25, 45):
        for az in range(0, 360, 30):
            e, a = np.radians(el), np.radians(az)
            out.append((-np.cos(e) * np.cos(a), -np.cos(e) * np.sin(a), -np.sin(e)))
    return out + [(1.0, 0, 0), (0, -1.0, 0), (0, 0, -1.0)]


def _sils(world):
    from . import reference as ref
    out = []
    for d in _dirs():
        up = (0, 1.0, 0) if abs(d[2]) > 0.99 else (0, 0, 1.0)
        m, _ = ref.silhouette(world, d, up, px_mm=0.6)
        if m is not None and m.any():
            out += [m, m[:, ::-1]]
    return out


def best_match(sils, mask):
    """(iou, stats, index) of the silhouette that best matches the mask."""
    from . import reference as ref
    best = (0.0, None, -1)
    for i, s in enumerate(sils):
        st = ref.compare(s, mask)[0]
        if st["iou"] > best[0]:
            best = (st["iou"], st, i)
    return best


def best_iou(sils, mask):
    return best_match(sils, mask)[0]


def cam_name(i):
    d = _dirs()
    k, mir = divmod(i, 2)
    if k < 24:
        el, az = (25, 45)[k // 12], (k % 12) * 30
        return f"elevation {el} deg, azimuth {az} deg{' (mirrored)' if mir else ''}"
    return ["side", "front", "top"][k - 24] + (" (mirrored)" if mir else "")


def _jaxis(j):
    """Joint axis whether the joint is a spec Obj (attribute) or a raw dict."""
    return j.get("axis") if isinstance(j, dict) else getattr(j, "axis", None)


def photos(ctx):
    from . import reference as ref
    from ..mask import photo_mask
    r, w = ctx.r, ctx.world
    base = _base(r.spec)
    from ..mask import THR
    rj = _refjson(r.spec)
    thr = rj.get("mask_thr") or {}  # photo collector's per-photo `robot mask --thr`, for floors the default picks up
    use = set(rj.get("photos") or [])  # photos the collector marked usable (clean background, whole robot)
    ents = [e for e in ref.entries(r.spec) if e.get("mask") and e.get("image")
            and (base / e["image"]).exists() and "reference" in Path(e["image"]).parts]
    missing = sorted(use - {Path(e["image"]).name for e in ents})
    if ents and missing:
        out0 = [fail("likeness.no_reference", G, BLOCKER, "Usable photo not compared",
                     f"REFERENCE.json marks {', '.join(missing)} usable but the spec has no `reference` entry for it.")]
    else:
        out0 = []
    if not ents:
        return [fail("likeness.no_reference", G, BLOCKER, "No photo comparison",
                     "This robot has reference photos but the spec has no `reference` entry with an `image` from "
                     "reference/ and a `mask`.")
                .fix('Run `robot mask reference/<photo> reference/<photo>_mask.png`, then add "reference": [{"image": '
                     '"reference/<photo>", "mask": "reference/<photo>_mask.png", "view": "iso", "approximate": true}].')]
    out = out0
    sils = _sils(w)
    tsils = None
    for e in ents:
        mask = ref.load_mask(base / e["mask"])
        crop = (rj.get("crop") or {}).get(Path(e["image"]).name)
        mode = (rj.get("mask_mode") or {}).get(Path(e["image"]).name, "plain")
        auto = photo_mask(base / e["image"], float(thr.get(Path(e["image"]).name, THR)), crop=crop, mode=mode)
        mj = ref.compare(auto, mask)[0]["iou"]
        if mj < MASK_MIN:
            t = thr.get(Path(e["image"]).name, THR)
            cs = (f" --crop {','.join(f'{v:g}' for v in crop)}" if crop else "") + (" --textured" if mode == "textured" else "")
            out.append(fail("likeness.mask_source", G, BLOCKER, "Mask is not the photo's outline",
                            f"`{e['mask']}` matches `robot mask {e['image']} --thr {t:g}{cs}` at IoU {mj:.2f} (need {MASK_MIN}): "
                            "it was not taken from the photo.").fix(f"Regenerate it: `robot mask {e['image']} {e['mask']} --thr {t:g}{cs}`."))
            continue
        iou, st, ci = best_match(sils, mask)
        tiou, tname = _template_iou(base / e["mask"], mask)
        # beat the closest template only while the match is mediocre; a strong match (>= SIL_STRONG) stands on its own
        # (literal copies are already caught by template_copy)
        need = SIL_MIN if iou >= SIL_STRONG else max(SIL_MIN, tiou + SIL_MARGIN)
        msg = (f"`{e['image']}`: best silhouette IoU {iou:.2f} at camera {cam_name(ci)} (need {need:.2f}: >= {SIL_MIN} "
               f"and no worse than the closest stock template `{tname}` at {tiou:.2f}).")
        if st:
            reg = st["regions"]
            worst = min(reg, key=reg.get)
            msg += (f" Regions (photo frame, left third first) {reg['front']:.2f} / {reg['middle']:.2f} / {reg['rear']:.2f}:"
                    f" worst = {worst} third. Height/length {st['aspect_model']:.2f} model vs {st['aspect_ref']:.2f} photo"
                    f" ({'too tall: lower it or lengthen it' if st['aspect_model'] > st['aspect_ref'] + 0.05 else 'too flat: raise it or shorten it' if st['aspect_model'] < st['aspect_ref'] - 0.05 else 'proportions ok'}).")
        if iou < need:
            out.append(fail("likeness.silhouette", G, BLOCKER, "Does not look like the photo", msg)
                       .fix("Reshape the outline (chassis plan, wedge/fork length, weapon size and height) toward the photo; "
                            "`robot render spec.json iso out.png` and compare side by side."))
        else:
            out.append(ok("likeness.silhouette", G, "Looks like the photo", msg))
    return out


_TW = None


DATA = TEMPLATES / "likeness_data.npz"  # shipped: per template voxels + silhouettes (rebuild: python -m robot.checks.likeness)
_TD = None


def _thash(p):
    import hashlib
    return hashlib.sha256(p.read_bytes()).hexdigest()[:16]


def _compute_template(name):
    from .. import spec as spec_mod, world as world_mod
    s = spec_mod.load(TEMPLATES / f"{name}.json")
    r = world_mod.resolve(s, fast=True)
    w = world_mod.World.build(r)
    v = np.array(sorted(_vox(_made(w, r))), int).reshape(-1, 3)
    return v, _sils(w)


def template_data(rebuild=False):
    """{name: (voxel set, [silhouettes])} for every bundled template, from the shipped npz when its hash matches."""
    global _TD
    if _TD is not None and not rebuild:
        return _TD
    have = {}
    if DATA.exists() and not rebuild:
        z = np.load(DATA, allow_pickle=True)
        have = z["data"].item()
    out, changed = {}, False
    for p in sorted(TEMPLATES.glob("*.json")):
        h = _thash(p)
        if p.stem in have and have[p.stem]["hash"] == h:
            d = have[p.stem]
        else:
            try:
                v, sl = _compute_template(p.stem)
            except Exception:  # noqa: BLE001 - a template that does not build cannot be copied either
                continue
            d = {"hash": h, "vox": v, "sils": [np.packbits(x, axis=None) for x in sl], "shapes": [x.shape for x in sl]}
            have[p.stem], changed = d, True
        sils = [np.unpackbits(b)[: sh[0] * sh[1]].reshape(sh).astype(bool) for b, sh in zip(d["sils"], d["shapes"])]
        out[p.stem] = (set(map(tuple, d["vox"])), sils)
    if changed and rebuild:
        try:
            np.savez_compressed(DATA, data=np.array(have, dtype=object))
        except OSError:
            pass
    _TD = out
    return out


def _template_iou(path, mask):
    """(best IoU, template name) over the stock templates' silhouettes (cached per mask + template set)."""
    from .. import cache
    key = ("likeness_tpl3", Path(path).read_bytes(),  # not the code hash: template data only changes with templates
           *[_thash(p) for p in sorted(TEMPLATES.glob("*.json"))])
    return tuple(cache.memo("likeness", key, lambda: _template_iou_raw(mask)))


def _template_iou_raw(mask):
    best = (0.0, None)
    for name, (_, sils) in template_data().items():
        i = best_match(sils, mask)[0]
        if i > best[0]:
            best = (i, name)
    return best


def _refjson(spec) -> dict:
    p = _base(spec) / "REFERENCE.json"
    try:
        return json.loads(p.read_text()) if p.exists() else {}
    except Exception:  # noqa: BLE001 - facts() reports the parse error
        return {}


def facts(ctx):
    spec = ctx.r.spec
    p = _base(spec) / "REFERENCE.json"
    if not p.exists():
        return []
    try:
        ref = json.loads(p.read_text())
    except Exception as ex:  # noqa: BLE001
        return [fail("likeness.type", G, BLOCKER, "REFERENCE.json unreadable", str(ex))]
    raw = spec.raw or {}
    out = []
    want = ref.get("robot_type")
    if want and str(raw.get("robot_type")) != str(want):
        out.append(fail("likeness.type", G, BLOCKER, "Wrong robot type",
                        f"Photos show a `{want}`; the spec says `{raw.get('robot_type')}`.")
                   .fix(f"Start from a matching template (`robot templates`) or `robot gen build --hypothesis ...`."))
    wheels = ref.get("wheels")
    if wheels:
        n = sum(1 for q in raw.get("parts") or [] if q.get("kind") == "wheel")
        if n != int(wheels):
            out.append(fail("likeness.type", G, BLOCKER, "Wrong wheel count", f"Photos show {wheels} wheels; spec has {n}."))
    w = ref.get("weapon")
    if isinstance(w, dict):
        out += weapon_facts(ctx, w)
    return out


AXES = "xyz"


def weapon_facts(ctx, want):
    """REFERENCE.json `weapon`: {kind: drum|disc|bar|eggbeater|lifter|flipper|wedge|none, axis: x|y|z (spin / hinge axis),
    position: front|middle|rear, width_frac: weapon width / robot width, teeth: N}."""
    from .power import spin_axis
    r, w = ctx.r, ctx.world
    kind = str(want.get("kind") or "").lower()
    if kind in ("", "none", "wedge"):
        return []
    idx = [i for i, b in enumerate(w.bodies) if b.part_idx is not None and r.parts[b.part_idx].part.kind == "weapon"]
    if not idx:
        return [fail("likeness.weapon", G, BLOCKER, "Weapon missing",
                     f"Photos show a {kind} weapon; the spec has no part of kind `weapon`.")
                .fix(f"Add the {kind} as a `weapon` part (see `robot templates`: vspin_drisk = disc, hspin_bar = bar).")]
    out = []
    i = max(idx, key=lambda j: float(np.prod(w.bodies[j].aabb[1] - w.bodies[j].aabb[0])))
    b = w.bodies[i]
    p = r.parts[b.part_idx].part
    wd = p.weapon
    got_kind = str(getattr(wd, "kind", None) or "").lower()
    spinner = kind in ("drum", "disc", "bar", "eggbeater", "shell", "ring")
    if spinner and got_kind != kind:
        out.append(fail("likeness.weapon", G, BLOCKER, "Wrong weapon type",
                        f"Photos show a {kind}; `{p.id}` is a `{got_kind or 'non-spinning part'}` (`weapon.kind`).")
                   .on(p.id).fix(f"Model a {kind} and set weapon.kind = \"{kind}\"."))
    ax = want.get("axis")
    if ax:
        a = None
        if spinner:
            sa = spin_axis(w, r, i)
            a = None if sa is None else sa[1]
        elif p.joint is not None and _jaxis(p.joint) is not None:
            a = np.asarray(_jaxis(p.joint), float)
        if a is None:
            out.append(fail("likeness.weapon", G, BLOCKER, "Weapon axis unknown",
                            f"`{p.id}` has no spin axis / joint axis; photos show a {kind} turning about {ax}.").on(p.id))
        else:
            g = AXES[int(np.argmax(np.abs(a)))]
            if g != ax:
                out.append(fail("likeness.weapon", G, BLOCKER, "Weapon turns the wrong way",
                                f"Photos: {kind} turns about {ax}; `{p.id}` turns about {g} (axis {np.round(a, 2).tolist()}). "
                                "x = across the robot (horizontal drum/vertical disc), z = up (horizontal spinner).").on(p.id))
    solid = [o for o in w.bodies if not o.is_wire and not o.fastener]
    lo = np.min([o.aabb[0] for o in solid], axis=0)
    hi = np.max([o.aabb[1] for o in solid], axis=0)
    pos = want.get("position")
    if pos:
        f = (b.center[1] - lo[1]) / max(hi[1] - lo[1], 1e-6)
        got = "front" if f > 2 / 3 else "rear" if f < 1 / 3 else "middle"
        if got != pos:
            out.append(fail("likeness.weapon", G, BLOCKER, "Weapon in the wrong place",
                            f"Photos: weapon at the {pos}; `{p.id}` centre is {f:.0%} of the length from the back ({got}).")
                       .on(p.id).here(b.center))
    wf = want.get("width_frac")
    if wf:
        got = (b.aabb[1][0] - b.aabb[0][0]) / max(hi[0] - lo[0], 1e-6)
        if abs(got - float(wf)) > 0.25 * float(wf):
            out.append(fail("likeness.weapon", G, BLOCKER, "Weapon the wrong size",
                            f"Photos: weapon spans {float(wf):.0%} of the robot width; `{p.id}` spans {got:.0%} (tolerance 25 %).")
                       .on(p.id))
    nt = want.get("teeth")
    if nt and spinner:
        rawp = next((q for q in (r.spec.raw or {}).get("parts") or [] if q.get("id") == p.id), {})
        gt = (rawp.get("weapon") or {}).get("teeth", getattr(wd, "teeth", None))
        if gt is None or int(gt) != int(nt):
            out.append(fail("likeness.weapon", G, BLOCKER, "Wrong tooth count",
                            f"Photos show {nt} teeth; `{p.id}` declares {gt} (`weapon.teeth`; shape.weapon_profile measures it).")
                       .on(p.id))
    return out


def run(ctx):
    spec = ctx.r.spec
    if not active(spec):
        return []
    out = facts(ctx) + copies(ctx) + photos(ctx)
    if not any(not f.passed and f.severity == BLOCKER for f in out):
        out.append(ok("likeness.template_copy", G, "Own design", "Differs from every template and sibling robot."))
    return out


def cli_main(path, out_dir=None):
    """`robot likeness SPEC`: only this gate, in seconds; writes model-vs-photo overlays (red model, blue photo)."""
    import time
    from types import SimpleNamespace

    from .. import spec as spec_mod, world as world_mod
    from . import reference as ref
    t0 = time.time()
    s = spec_mod.load(path)
    if not active(s):
        print("likeness: inactive (no reference/ photos or REFERENCE.json next to the spec)")
        return 0
    r = world_mod.resolve(s, fast=True)
    w = world_mod.World.build(r)
    ctx = SimpleNamespace(r=r, world=w, metrics={}, not_checked=[])
    out = facts(ctx) + copies(ctx) + photos(ctx)
    od = Path(out_dir or (_base(s) / "renders"))
    od.mkdir(parents=True, exist_ok=True)
    sils = _sils(w)
    for e in ref.entries(s):
        if not e.get("mask"):
            continue
        mask = ref.load_mask(_base(s) / e["mask"])
        _, _, ci = best_match(sils, mask)
        if ci >= 0:
            _, a, b = ref.compare(sils[ci], mask)
            png = od / f"likeness_{Path(e['mask']).stem}.png"
            png.write_bytes(ref.overlay_png(a, b))
            print(f"overlay {png} (red = model only, blue = photo only, purple = both)")
    bad = [f for f in out if not f.passed]
    for f in out:
        print(f"[{'FAIL' if not f.passed else 'ok'}] {f.id}: {f.message}")
        if not f.passed and f.fix_hint:
            print(f"   fix: {f.fix_hint}")
    print(f"likeness: {'FAIL' if bad else 'PASS'} ({len(bad)} blockers) in {time.time() - t0:.1f}s")
    return 1 if bad else 0


def add_cli(sub):
    p = sub.add_parser("likeness", help="fast copy-of-real-robot gate: template copy, type, silhouette vs photos + overlays")
    p.add_argument("spec")
    p.add_argument("--out", help="overlay dir (default <spec dir>/renders)")
    p.set_defaults(func=lambda a: cli_main(a.spec, a.out))


if __name__ == "__main__":
    import sys
    if "--rebuild" not in sys.argv:
        print("maintainers only: `python -m robot.checks.likeness --rebuild` rewrites the shipped template data after a "
              "template change. Builders: use `robot likeness spec.json`.")
        sys.exit(2)
    template_data(rebuild=True)
    print(f"wrote {DATA}")
