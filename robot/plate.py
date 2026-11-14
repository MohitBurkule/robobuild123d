"""Build-plate export (D3): oriented, packed print plates instead of assembly-frame STLs.

`write(world_or_meshes, out_dir, printer="ender3", filament="pla")` lays every
printed part flat on its declared print orientation, packs the parts onto one or
more bed plates (shelf-packing by footprint area), and writes per-part STLs plus
`plate_<n>.stl` plates and `plates.json` (per-part position, supports flag).
Meshes arrive in assembly frame; orientation comes from the part's declared
`print_orientation` when the caller supplies one.
"""

from __future__ import annotations

import json
from pathlib import Path

ORIENT_AXIS = {"+z": (0, 0, 1), "-z": (0, 0, -1), "+x": (1, 0, 0), "-x": (-1, 0, 0),
               "+y": (0, 1, 0), "-y": (0, -1, 0)}


def orient(mesh, up="+z"):
    """A copy of `mesh` with `up` as the print direction (that axis down) and min z = 0."""
    import numpy as np
    import trimesh

    m = mesh.copy()
    axis = np.asarray(ORIENT_AXIS.get(str(up).lower()) or ORIENT_AXIS["+z"], float)
    rot = np.cross([0, 0, 1], axis)
    if not np.linalg.norm(rot) > 1e-9:
        rot = np.array([1.0, 0.0, 0.0])
    m.apply_transform(trimesh.transformations.rotation_matrix(np.radians(90), rot))
    m.apply_translation(-m.bounds[0])
    return m


def pack(meshes, bed_mm=(220, 220), gap=4.0):
    """Shelf-pack meshes (already oriented, min z=0) by footprint; returns (plates, positioned).
    plates: [{plate: n, parts: [{id, at}]}]; positioned: {id: (plate, x, y)}."""
    plates, positioned, cur, x, y, row_h = [], {}, [], 0.0, 0.0, 0.0
    for mid, m in sorted(meshes, key=lambda kv: -(kv[1].bounds[1][0] - kv[1].bounds[0][0]) * (kv[1].bounds[1][1] - kv[1].bounds[0][1])):
        w = float(m.bounds[1][0] - m.bounds[0][0])
        d = float(m.bounds[1][1] - m.bounds[0][1])
        if w > bed_mm[0] or d > bed_mm[1]:
            raise ValueError(f"part {mid} ({w:.0f}x{d:.0f} mm) does not fit a {bed_mm[0]}x{bed_mm[1]} bed")
        if x + w > bed_mm[0]:
            y, x, row_h = y + row_h + gap, 0.0, 0.0
        if y + d > bed_mm[1]:
            plates.append(cur)
            cur, x, y, row_h = [], 0.0, 0.0, 0.0
        cur.append({"id": mid, "at": [round(x, 2), round(y, 2)]})
        positioned[mid] = (len(plates), round(x, 2), round(y, 2))
        x += w + gap
        row_h = max(row_h, d)
    if cur:
        plates.append(cur)
    return plates, positioned


def write(parts, out_dir, printer="ender3", filament="pla", gap=4.0):
    """parts: [(id, mesh, print_orientation or None)]. Writes STLs + plates; returns the summary dict."""
    import trimesh

    from . import mfg_profiles

    p = mfg_profiles.printer(printer)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    meshes = {}
    for pid, mesh, up in parts:
        om = orient(mesh, up or "+z")
        size = om.bounds[1] - om.bounds[0]
        if not mfg_profiles.bed_fit(printer, (float(size[0]), float(size[1]), float(size[2]))):
            raise ValueError(f"part {pid} ({size[0]:.0f}x{size[1]:.0f}x{size[2]:.0f} mm) does not fit the "
                             f"{p.id} bed {p.bed_mm[0]}x{p.bed_mm[1]}x{p.z_mm}")
        om.export(out / f"{pid}.stl")
        meshes[pid] = om
    plates, positioned = pack(list(meshes.items()), (p.bed_mm[0], p.bed_mm[1]), gap)
    for i, plate in enumerate(plates):
        scene = trimesh.Scene()
        for entry in plate:
            m = meshes[entry["id"]].copy()
            m.apply_translation([entry["at"][0], entry["at"][1], 0])
            scene.add_geometry(m, node_name=entry["id"])
        scene.export(out / f"plate_{i}.stl")
    info = {"printer": p.id, "filament": filament, "bed_mm": list(p.bed_mm), "gap_mm": gap,
            "plates": [{"plate": i, "parts": plate} for i, plate in enumerate(plates)],
            "positioned": positioned}
    (out / "plates.json").write_text(json.dumps(info, indent=2))
    return info
