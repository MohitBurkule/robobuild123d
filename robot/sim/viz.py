"""Software rendering of the current simulation state with the verifier's own rasteriser (no GL needed)."""

from __future__ import annotations

import mujoco
import numpy as np
import trimesh

from .. import render


class _B:
    def __init__(self, mesh, color):
        self.mesh = mesh
        self.color = color


class _W:
    def __init__(self, bodies):
        self.bodies = bodies

    def bounds(self):
        v = np.vstack([b.mesh.bounds for b in self.bodies])
        return v[:, :].min(axis=0), v[:, :].max(axis=0)

    def exploded(self, f):
        return self


def _geom_mesh(m, d, i):
    t = m.geom_type[i]
    if t == mujoco.mjtGeom.mjGEOM_MESH:
        k = m.geom_dataid[i]
        va, vn, fa, fn = m.mesh_vertadr[k], m.mesh_vertnum[k], m.mesh_faceadr[k], m.mesh_facenum[k]
        mesh = trimesh.Trimesh(m.mesh_vert[va:va + vn], m.mesh_face[fa:fa + fn], process=False)
    elif t == mujoco.mjtGeom.mjGEOM_BOX:
        mesh = trimesh.creation.box(extents=2 * m.geom_size[i])
    elif t == mujoco.mjtGeom.mjGEOM_SPHERE:
        mesh = trimesh.creation.icosphere(radius=m.geom_size[i][0])
    elif t == mujoco.mjtGeom.mjGEOM_CYLINDER:
        mesh = trimesh.creation.cylinder(radius=m.geom_size[i][0], height=2 * m.geom_size[i][1])
    else:
        return None
    T = np.eye(4)
    T[:3, :3] = d.geom_xmat[i].reshape(3, 3)
    T[:3, 3] = d.geom_xpos[i]
    mesh = mesh.copy()
    mesh.apply_transform(T)
    mesh.apply_scale(1000.0)  # m -> mm for the rasteriser
    return mesh


def snapshot(sim, view="iso", width=900) -> np.ndarray:
    """Render the current state to an (H, W, 3) uint8 image."""
    m, d = sim.m, sim.d
    bodies = []
    for i in range(m.ngeom):
        mesh = _geom_mesh(m, d, i)
        if mesh is None:
            continue
        c = (np.asarray(m.geom_rgba[i][:3]) * 255).astype(int)
        bodies.append(_B(mesh, list(c)))
    v = render.named(view, width)
    return render.render_array(_W(bodies), v, ground_z=0.0)


def save(sim, path, **kw):
    img = snapshot(sim, **kw)
    from PIL import Image

    Image.fromarray(img).save(path)
    return path
