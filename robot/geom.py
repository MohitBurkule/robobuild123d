"""Part geometry: build123d B-rep -> cached tessellation, mass properties, and mesh queries.

Every part solid is built once per distinct shape (cache key = hash of the shape JSON, model files and tessellation
settings) and stored under the cache directory as `<key>.brep` (exact B-rep for STEP export), `<key>.npz` (local-frame
triangle mesh) and `<key>.json` (volume, centroid, inertia from the B-rep). Bodies then only move meshes around.

Queries used by the checks:
  * exact booleans on meshes (manifold3d): overlap volume, penetration depth (largest ball inside the intersection),
  * point containment (trimesh ray parity), closest distance (trimesh), first ray hits,
  * voxel occupancy by column parity + Euclidean distance transform (for routing grids and depth).
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass
from pathlib import Path

import manifold3d as mf
import numpy as np
import trimesh
from scipy import ndimage

from . import shapes, xform

CACHE_VERSION = "1"


def cache_dir() -> Path:
    d = Path(os.environ.get("ROBOT_CACHE") or Path.home() / ".cache" / "robot")
    d.mkdir(parents=True, exist_ok=True)
    return d


@dataclass
class Tess:
    lin: float  # chord tolerance mm
    ang: float  # angular tolerance rad


FINE = Tess(0.01, 0.1)
FAST = Tess(0.05, 0.3)


class PartGeom:
    """One solid in its own (part) frame."""

    def __init__(self, key: str, vertices: np.ndarray, faces: np.ndarray, volume: float, centroid, inertia, brep_path: Path | None):
        self.key = key
        self.mesh = trimesh.Trimesh(vertices, faces, process=True)
        self.volume = float(volume)
        self.centroid = np.asarray(centroid, float)
        self.inertia = np.asarray(inertia, float)  # about centroid, unit density, mm^5
        self.brep_path = brep_path
        self._solid = None

    @property
    def solid(self):
        """The exact build123d solid (part frame), loaded on demand."""
        if self._solid is None and self.brep_path and self.brep_path.exists():
            import build123d as b

            self._solid = b.import_brep(str(self.brep_path))
        return self._solid

    @property
    def bounds(self) -> np.ndarray:
        return self.mesh.bounds


def mass_props(solid):
    from OCP.BRepGProp import BRepGProp
    from OCP.GProp import GProp_GProps

    g = GProp_GProps()
    BRepGProp.VolumeProperties_s(solid.wrapped, g)
    c = g.CentreOfMass()
    m = g.MatrixOfInertia()
    I = [[m.Value(i, j) for j in (1, 2, 3)] for i in (1, 2, 3)]
    return g.Mass(), [c.X(), c.Y(), c.Z()], I


def tessellate(solid, tess: Tess):
    v, f = solid.tessellate(tess.lin, tess.ang)
    V = np.array([[p.X, p.Y, p.Z] for p in v], float).reshape(-1, 3)
    F = np.array(f, np.int64).reshape(-1, 3)
    return V, F


_MEM: dict[str, PartGeom] = {}


def _b123d_version() -> str:
    try:
        import build123d as b

        return str(getattr(b, "__version__", "?"))
    except ImportError:
        return "none"


def key_for(shape: dict, base_dir: Path | None, tess: Tess = FINE, key_extra: str = "") -> str:
    """Cache key: shape JSON + model file sources + build123d version + tessellation settings."""
    return shapes.shape_key(shape, base_dir, f"{CACHE_VERSION}|{_b123d_version()}|{tess.lin}|{tess.ang}|{key_extra}")


def cached(key: str) -> bool:
    d = cache_dir()
    return key in _MEM or ((d / f"{key}.npz").exists() and (d / f"{key}.json").exists())


def geom_for(shape: dict, base_dir: Path | None, tess: Tess = FINE, solid_factory=None, key_extra: str = "") -> PartGeom:
    """Build (or load from cache) the geometry of a shape tree."""
    from . import cache

    key = key_for(shape, base_dir, tess, key_extra)
    use = cache.enabled()
    if use and key in _MEM:
        cache.hits["part_geom"] += 1
        return _MEM[key]
    d = cache_dir()
    npz, js, brep = d / f"{key}.npz", d / f"{key}.json", d / f"{key}.brep"
    if use and npz.exists() and js.exists():
        try:
            z = np.load(npz)
            meta = json.loads(js.read_text())
            g = PartGeom(key, z["v"], z["f"], meta["volume"], meta["centroid"], meta["inertia"], brep)
            _MEM[key] = g
            cache.hits["part_geom"] += 1
            return g
        except (OSError, ValueError, KeyError):
            pass
    cache.misses["part_geom"] += 1
    solid = solid_factory() if solid_factory else shapes.to_solid(shape, base_dir)
    vol, cen, I = mass_props(solid)
    V, F = tessellate(solid, tess)
    try:
        import build123d as b

        b.export_brep(solid, str(brep))
    except Exception:  # noqa: BLE001 - B-rep cache is optional
        brep = None
    np.savez_compressed(npz, v=V, f=F)
    js.write_text(json.dumps({"volume": vol, "centroid": cen, "inertia": I}))
    g = PartGeom(key, V, F, vol, cen, I, brep)
    g._solid = solid
    _MEM[key] = g
    return g


# ---------------------------------------------------------------------------- mesh helpers


def to_manifold(mesh: trimesh.Trimesh) -> mf.Manifold:
    m = mf.Manifold(mf.Mesh(np.asarray(mesh.vertices, np.float32), np.asarray(mesh.faces, np.uint32)))
    if m.status() != mf.Error.NoError or m.is_empty():
        # Merge near-duplicate vertices and retry; tessellations of compounds can leave seams.
        mm = mf.Mesh(np.asarray(mesh.vertices, np.float32), np.asarray(mesh.faces, np.uint32))
        mm.merge()
        m = mf.Manifold(mm)
    return m


def from_manifold(m: mf.Manifold) -> trimesh.Trimesh:
    mm = m.to_mesh()
    return trimesh.Trimesh(np.asarray(mm.vert_properties)[:, :3], np.asarray(mm.tri_verts), process=False)


def voxelize(mesh: trimesh.Trimesh, h: float, lo=None, hi=None, max_cells: int = 40_000_000):
    """Occupancy of `mesh` on a grid of cell size `h` (cell centres lo + (i + 0.5) h). Column ray parity, so it is exact
    for watertight meshes up to the grid resolution. Returns (occ[nx, ny, nz] bool, lo, h)."""
    lo = np.asarray(mesh.bounds[0] if lo is None else lo, float)
    hi = np.asarray(mesh.bounds[1] if hi is None else hi, float)
    n = np.maximum(np.ceil((hi - lo) / h).astype(int), 1)
    if int(np.prod(n)) > max_cells:
        h = h * (np.prod(n) / max_cells) ** (1 / 3) * 1.01
        n = np.maximum(np.ceil((hi - lo) / h).astype(int), 1)
    nx, ny, nz = (int(x) for x in n)
    # Tiny irrational offsets keep ray columns off mesh edges and vertices.
    xs = lo[0] + (np.arange(nx) + 0.5) * h + h * 1.37e-4
    ys = lo[1] + (np.arange(ny) + 0.5) * h + h * 2.71e-4
    zs = lo[2] + (np.arange(nz) + 0.5) * h
    T = mesh.triangles
    counts = np.zeros((nx * ny, nz + 1), np.int32)
    for tri in T:
        x0, y0 = tri[:, 0].min(), tri[:, 1].min()
        x1, y1 = tri[:, 0].max(), tri[:, 1].max()
        i0 = max(int(np.ceil((x0 - xs[0]) / h - 1e-9)), 0) if nx else 0
        i1 = min(int(np.floor((x1 - xs[0]) / h + 1e-9)), nx - 1)
        j0 = max(int(np.ceil((y0 - ys[0]) / h - 1e-9)), 0)
        j1 = min(int(np.floor((y1 - ys[0]) / h + 1e-9)), ny - 1)
        if i1 < i0 or j1 < j0:
            continue
        a, b, c = tri
        det = (b[1] - c[1]) * (a[0] - c[0]) + (c[0] - b[0]) * (a[1] - c[1])
        if abs(det) < 1e-14:
            continue
        X, Y = np.meshgrid(xs[i0:i1 + 1], ys[j0:j1 + 1], indexing="ij")
        l1 = ((b[1] - c[1]) * (X - c[0]) + (c[0] - b[0]) * (Y - c[1])) / det
        l2 = ((c[1] - a[1]) * (X - c[0]) + (a[0] - c[0]) * (Y - c[1])) / det
        l3 = 1 - l1 - l2
        m = (l1 >= 0) & (l2 >= 0) & (l3 >= 0)
        if not m.any():
            continue
        z = l1 * a[2] + l2 * b[2] + l3 * c[2]
        I, J = np.nonzero(m)
        col = (I + i0) * ny + (J + j0)
        k = np.clip(np.searchsorted(zs, z[m], side="left"), 0, nz)
        np.add.at(counts, (col, k), 1)
    occ = (np.cumsum(counts[:, :nz], axis=1) % 2 == 1).reshape(nx, ny, nz)
    return occ, lo, h


def inscribed_depth(m: mf.Manifold, cap: float | None = None):
    """Largest distance from a point inside `m` to its boundary (the penetration depth of an intersection), and where."""
    best, where = 0.0, None
    for piece in m.decompose() if m.num_vert() else []:
        lo, hi = (np.asarray(x) for x in _bbox(piece))
        ext = hi - lo
        bound = float(ext.min()) / 2
        if bound <= best or bound <= 1e-6:
            continue
        if cap is not None and bound <= cap:
            # Cannot exceed the threshold; report the bound as an upper estimate.
            if bound > best:
                best, where = bound, (lo + hi) / 2
            continue
        h = float(np.clip(ext.min() / 14, 0.004, 0.25))
        mesh = from_manifold(piece)
        occ, glo, h = voxelize(mesh, h, lo - h, hi + h, max_cells=4_000_000)
        if not occ.any():
            continue
        dist = ndimage.distance_transform_edt(occ) * h - 0.5 * h
        k = np.unravel_index(int(np.argmax(dist)), dist.shape)
        d = float(min(dist[k], bound))
        if d > best:
            best, where = d, glo + (np.asarray(k) + 0.5) * h
    return best, where


def _bbox(m: mf.Manifold):
    b = m.bounding_box()
    return (b[0], b[1], b[2]), (b[3], b[4], b[5])


def sample_surface(mesh: trimesh.Trimesh, h: float, max_pts: int = 60000, seed: int = 7):
    """Roughly uniform surface points (spacing about h) with outward normals, deterministic."""
    area = float(mesh.area)
    n = int(min(max(area / (h * h), 50), max_pts))
    pts, fi = trimesh.sample.sample_surface(mesh, n, seed=seed)
    pts = np.vstack([pts, mesh.vertices])
    nrm = np.vstack([mesh.face_normals[fi], mesh.vertex_normals])
    return pts, nrm


def axial_inertia(g: PartGeom, M: np.ndarray, origin, axis) -> float:
    """Unit-density moment of inertia (mm^5) of a part placed by M about the world axis (origin, axis)."""
    a = xform.norm(axis)
    R = M[:3, :3]
    Iw = R @ g.inertia @ R.T
    c = xform.apply(M, g.centroid)
    q = c - np.asarray(origin, float)
    perp = q - a * q.dot(a)
    return float(a @ Iw @ a + g.volume * perp.dot(perp))
