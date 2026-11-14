# Speed analysis and changes (UNTESTED: written without running any code)

## Where time goes (Oct 24 logs, one verify round: ~800 s wall, ~6,000 s summed check time)

| group | s | likely hot spot (from reading the code) |
|---|---|---|
| intent | 1,289 | mesh booleans + `inscribed_depth` -> `geom.voxelize` python loop per triangle |
| reference_cad | 950 | B-rep booleans vs reference (OCC, not touched here) |
| robust | 900 | one new process per sweep point (params are env globals read at import) |
| visual / practice | 725 each | renders: `render._raster` python loop per triangle, repeated per body per view |

Render: FINE tessellation (0.01 mm chord) gives 10^5..10^6 triangles per robot. `_raster` ran one python
iteration (meshgrid + 6 temporaries) per triangle, 10 views + axle sections, so python overhead dominated, not pixels.

## Changed in this PR

1. `render._raster`: triangles grouped by pixel-box size and evaluated as numpy blocks (`robot/_batch.py`), one
   depth resolve per touched pixel (lexsort: nearest, then lowest triangle index). Same formulas, same tolerances.
   Expected 20-100x on the raster step. Images should match except where two triangles have exactly equal depth.
2. Back-face culling for closed, uncut bodies (watertight + consistent winding, memoised per part geometry):
   about half the triangles skipped on non-section views.
3. `render._clip`: bodies wholly on the kept side of the section plane are not sliced; wholly cut bodies are dropped
   before slicing. Section views slice only bodies the plane really crosses.
4. `render.render_views`: several views in threads over one set of placed meshes; `export` uses it
   (`ROBOT_RENDER_JOBS`, default min(4, cpus)).
5. `ROBOT_RENDER_SCALE` (default 1): proxy renders, e.g. 0.5 = about 4x fewer pixels. Part of the render cache key
   through the view width.
6. `geom.voxelize`: same block method for column parity (`_voxel_columns`). Counts are order independent, so the
   occupancy grid should be bit-identical. Speeds every `inscribed_depth` (penetration depth) call.

## Not tested

Nothing here was run, imported or compiled. Before merge: unit tests, then compare old vs new on one robot:
`voxelize` grids equal, each view PNG equal or within a few pixels, timing per view.
Risks: index/broadcast slips in the block code; culling on a mesh trimesh calls watertight but with flipped
winding (guarded by `volume > 0` and positive transform determinant); thread safety of lazy `Body.mesh`
(pre-filled before threads start).

## Next wins (not done, outside render/cache/tessellation or need measuring)

- Params as env globals: make a sweep point a function call (Design object refactor), then one process can run a
  sweep and reuse unchanged parts. Biggest win for `robust` (900 s).
- Part cache key: env names must be listed in `ROBOT_CACHE_ENV`; `REVRON_VARIANTS` is not, so variants can share a
  wrong key. Key should come from the resolved params per part, so a changed param rebuilds only parts that read it.
- `PartGeom` loads with `trimesh process=True` (vertex merge on every load) from compressed npz: store the merged
  mesh once, load with `process=False`.
- Checks that need only shape, not detail (visual, practice proxies): use `FAST` tessellation (0.05 mm), 5-10x
  fewer triangles for every mesh query.
- `cache.code_hash` hashes the whole package into every group key: any edit to any check invalidates all groups.
  Key each group on its own import closure (`model_closure` already does this for model files).
- Shared placed-mesh / manifold cache across `World` copies (`material_palette`, `without_lid`, `exploded` rebuild
  transformed meshes per body).
