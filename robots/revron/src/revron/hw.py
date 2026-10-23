"""Catalog-derived hardware dimensions: read off the catalog shape of the part, never typed in again.

The tub is dimensioned from what sits in it, so swapping the motor or the pack in the catalog moves the pockets, key tab and pad with it."""
from functools import lru_cache
import build123d as bd

CUT = 0.1   # section thickness: a slice just under the top face of the plate stack


@lru_cache(maxsize=None)
def _solid(catalog_id):
    from robot import catalog, shapes
    return shapes.to_solid(catalog.find(catalog_id).shape)


def size(catalog_id):
    """(L, W, H) of the catalog part's bounding box."""
    bb = _solid(catalog_id).bounding_box()
    return bb.size.X, bb.size.Y, bb.size.Z


def reach(catalog_id):
    """The catalog part's bounding box in its own frame: x0 / x1 and y0 / y1 (the motor's reach along the shaft and across it)."""
    bb = _solid(catalog_id).bounding_box()
    return dict(x0=bb.min.X, x1=bb.max.X, y0=bb.min.Y, y1=bb.max.Y)


@lru_cache(maxsize=None)
def gearbox(catalog_id):
    """A gearmotor's plate stack in its own frame (x along the shaft, origin on the axis): `top` and `half_w` (the plates' Z top and
    half width), `end` (outer face of the last plate) and `gaps` (the open X spans between plates, front to back).
    Read from a section just under the top face, which the shaft and the screws do not reach."""
    s = _solid(catalog_id)
    bb = s.bounding_box()
    top = bb.max.Z
    cut = s & bd.Pos(0, 0, top - CUT / 2) * bd.Box(bb.size.X, bb.size.Y, CUT)
    spans = sorted((p.bounding_box().min.X, p.bounding_box().max.X) for p in cut.solids())
    gaps = [(a1, b0) for (_, a1), (b0, _) in zip(spans, spans[1:]) if b0 - a1 > 0.5]
    return dict(top=top, half_w=bb.size.Y / 2, end=spans[-1][1], gaps=gaps)


def placed(catalog_id, at, rot=(0, 0, 0)):
    """The catalog part's solid at a spec placement (`at` / `rot` as in spec.json parts), so the tub can cut its pockets from what sits in them."""
    from robot import shapes, xform
    return shapes.place(_solid(catalog_id), xform.pose(list(at), list(rot)))
