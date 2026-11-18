"""export_one.py SLUG OUTDIR : GLB (one named node per body, decimated) + photos + meta.json for one robot.
Run with cwd = the robot's clone so its own `robot` package is imported (read-only use)."""
import json, sys, glob, os, re, traceback
from pathlib import Path
import numpy as np

slug, out = sys.argv[1], Path(sys.argv[2])
S = "/tmp/claude-0/-home-user/a49462ed-bed0-54a5-8dcf-e0aab9a96f04/scratchpad"
clone = Path(f"/tmp/work10_{slug}")
d = clone / "robots" / slug
sys.path.insert(0, str(clone))
meta = {"slug": slug, "photos": [], "parts": [], "model": None, "errors": []}

# ---------- photos + default camera guesses ----------
NAMED = {"front": (90, 20), "rear": (270, 20), "right": (0, 20), "left": (180, 20), "front_right_iso": (45, 35),
         "front_left_iso": (135, 35), "rear_left_iso": (225, 35), "rear_right_iso": (315, 35), "top": (90, 90),
         "bottom": (90, -90)}
def rd(p):
    try: return json.loads(Path(p).read_text())
    except Exception: return {}
rj, vm = rd(d / "REFERENCE.json"), rd(d / "renders" / "view_match.json")
photos = [p for p in vm if (d / "reference" / p).exists()]
for m in sorted(glob.glob(str(d / "renders" / "match_*.png"))):
    st = Path(m).name[len("match_"):-4]
    for f in sorted((d / "reference").glob(st + ".*")):
        if f.name not in photos and "_mask" not in f.name: photos.append(f.name)
if not photos:
    photos = [p for p in rj.get("photos") or [] if (d / "reference" / p).exists()]
if not photos:
    photos = sorted(f.name for f in (d / "reference").glob("*") if "_mask" not in f.name and f.suffix.lower() in (".webp", ".jpg", ".jpeg", ".png"))
ov = {}
for l in Path(S, "ov_table.txt").read_text().splitlines():
    t = l.split()
    if len(t) == 3 and t[0] == slug: ov[t[1]] = t[2]  # later lines win
from PIL import Image
pd = out / "photos" / slug; pd.mkdir(parents=True, exist_ok=True)
for p in photos:
    stem = Path(p).stem
    im = Image.open(d / "reference" / p).convert("RGB"); im.thumbnail((900, 900))
    im.save(pd / f"{stem}.jpg", quality=82)
    src, az, el = None, None, None
    keys = [k for k in ov if re.search(r"(^|[._])" + re.escape(k) + r"($|[._])", stem)]
    if keys:
        v = ov[keys[-1]]; a, e = v.rstrip("~").split(","); az, el, src = float(a), float(e), f"ov_table {v}"
    elif p in vm and vm[p].get("azimuth") is not None:
        az, el, src = float(vm[p]["azimuth"]), float(vm[p]["elevation"]), f"view_match ({vm[p].get('view')})"
    else:
        nv = (rj.get("view") or {}).get(p)
        if isinstance(nv, str) and "," in nv:
            a, e = nv.replace("auto:", "").rstrip("~").split(",")[:2]; az, el = float(a), float(e)
        elif nv in NAMED:
            az, el = NAMED[nv]
        else:
            az, el = 135.0, 35.0
        e2 = (rj.get("elevation") or {}).get(p)
        if e2 is not None and not (isinstance(nv, str) and "," in nv): el = float(e2)
        src = f"REFERENCE.json view={nv} elevation={e2}" if nv else "fallback 135,35"
    meta["photos"].append({"name": stem, "file": p, "w": im.width, "h": im.height,
                           "default": {"azimuth_deg": az, "elevation_deg": el, "roll_deg": 0.0, "source": src}})

# ---------- model ----------
try:
    import trimesh
    from robot import spec as spec_mod, world as world_mod
    s = spec_mod.load(str(d / "spec.json"))
    r = world_mod.resolve(s, fast=False)
    w = world_mod.World.start(r)
    meshes = []
    for b in w.bodies:
        m = b.mesh.copy(); m.merge_vertices()
        meshes.append((b, m))
    total = sum(len(m.faces) for _, m in meshes)
    md = out / "models"; md.mkdir(parents=True, exist_ok=True)
    def cluster(m, cell):
        q = np.floor(m.vertices / cell).astype(np.int64)
        _, inv = np.unique(q, axis=0, return_inverse=True); inv = inv.reshape(-1)
        nv = inv.max() + 1
        v = np.zeros((nv, 3)); cnt = np.zeros(nv)
        np.add.at(v, inv, m.vertices); np.add.at(cnt, inv, 1); v /= cnt[:, None]
        f = inv[m.faces]
        ok = (f[:, 0] != f[:, 1]) & (f[:, 1] != f[:, 2]) & (f[:, 0] != f[:, 2])
        f = f[ok]
        if len(f) < 4: return m
        f = np.unique(np.sort(f, axis=1), axis=0, return_index=True)[1]
        f = inv[m.faces][ok][np.sort(f)]
        return trimesh.Trimesh(v, f, process=False)
    def build(BUDGET, cell=0.0):
        sc = trimesh.Scene(); parts = []; nf = 0
        lo, hi = np.full(3, 1e9), np.full(3, -1e9)
        for b, m in meshes:
            n = len(m.faces)
            tgt = max(12, int(BUDGET * n / max(total, 1))) if total > BUDGET else n
            if n > tgt:
                for agg in (7, 10):
                    try:
                        m2 = m.simplify_quadric_decimation(face_count=tgt, aggression=agg)
                        if len(m2.faces) > 0: m = m2
                    except Exception as ex:
                        meta["errors"].append(f"decimate {b.id}: {ex}")
                    if len(m.faces) <= tgt * 1.3: break
                if cell > 0 and len(m.faces) > tgt * 1.3:
                    m = cluster(m, cell)
            nf += len(m.faces)
            c = b.color
            c = list(np.asarray(c, float)[:3]) if c is not None else [0.7, 0.7, 0.72]
            if max(c) > 1.0: c = [x / 255 for x in c]
            mat = trimesh.visual.material.PBRMaterial(name=b.id, baseColorFactor=[*c, 1.0], metallicFactor=0.1,
                                                      roughnessFactor=0.8, doubleSided=True)
            m.visual = trimesh.visual.TextureVisuals(material=mat)
            sc.add_geometry(m, node_name=b.id, geom_name=b.id)
            lo, hi = np.minimum(lo, m.bounds[0]), np.maximum(hi, m.bounds[1])
            parts.append({"id": b.id, "kind": b.kind, "color": "#%02x%02x%02x" % tuple(int(round(x * 255)) for x in c),
                          "fastener": bool(b.fastener)})
        return sc.export(file_type="glb", include_normals=False), parts, lo, hi, nf
    budget = 14000
    for cell in (0.0, 0.4, 0.6, 0.8, 1.0, 1.3, 1.6, 2.0, 2.5):
        data, parts, lo, hi, nf = build(budget, cell)
        if len(data) <= 300_000: break
    meta["cluster_mm"] = cell
    meta["parts"] = parts; meta["faces_out"] = nf
    (md / f"{slug}.glb").write_bytes(data)
    meta["model"] = f"models/{slug}.glb"
    meta["bbox"] = [lo.round(2).tolist(), hi.round(2).tolist()]
    meta["glb_bytes"] = len(data); meta["faces_src"] = total
except Exception as ex:
    meta["errors"].append("model: " + "".join(traceback.format_exception_only(type(ex), ex)).strip())
mdir = out / "meta"; mdir.mkdir(parents=True, exist_ok=True)
(mdir / f"{slug}.json").write_text(json.dumps(meta, indent=1))
print(slug, "photos", len(meta["photos"]), "model", meta.get("glb_bytes"), meta["errors"][:2])
