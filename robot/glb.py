"""World -> GLB (E1): the built robot as one binary glTF for the HTML viewer.

`world_to_glb(world)` exports every body mesh with its world transform and a
colour from the catalogue; returns GLB bytes. Node count equals body count
(the test checks that).
"""

from __future__ import annotations

import numpy as np
import trimesh


def _body_mesh(b):
    m = b.mesh.copy()
    M = np.asarray(b.M, float)
    m.apply_transform(M)
    return m


def world_to_glb(world) -> bytes:
    import io

    scene = trimesh.Scene()
    for b in world.bodies:
        m = _body_mesh(b)
        color = getattr(b, "color", None) or "#b0b4ba"
        try:
            rgb = tuple(int(color[i:i + 2], 16) for i in (1, 3, 5))
            m.visual = trimesh.visual.TextureVisuals(
                material=trimesh.visual.material.PBRMaterial(baseColorFactor=[*rgb, 255]))
        except (ValueError, TypeError):
            pass
        scene.add_geometry(m, node_name=getattr(b, "id", None) or f"body_{len(scene.graph.nodes)}")
    buf = io.BytesIO()
    scene.export(buf, file_type="glb")
    return buf.getvalue()
