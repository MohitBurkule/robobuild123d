"""[drawing] Orthographic views: hidden-line removal through build123d's project_to_viewport (OCP HLRBRep).

A view is a camera looking along -n with screen up = v; screen right is u = v x n (the convention of
project_to_viewport). Model points map to view coordinates by dot products, so features found on the B-rep
(hole centres, fillet arcs) land exactly on the projected lines.
"""
from __future__ import annotations

from dataclasses import dataclass, field

import numpy as np

# third-angle names for a part whose "front" is the top-down view (model X across, Y forward, Z up)
VIEW_DIRS = {
    #          n (towards viewer)   up
    "front": ((0, 0, 1), (0, 1, 0)),     # looking down -Z
    "top": ((0, 1, 0), (0, 0, -1)),      # from +Y, placed above the front view
    "bottom": ((0, -1, 0), (0, 0, 1)),   # from -Y, placed below
    "right": ((1, 0, 0), (0, 1, 0)),     # from +X, placed right
    "left": ((-1, 0, 0), (0, 1, 0)),     # from -X, placed left
}


@dataclass
class View:
    name: str
    n: np.ndarray
    v: np.ndarray
    visible: list = field(default_factory=list)   # list of (k,2) polylines in model mm, view frame
    hidden: list = field(default_factory=list)

    @property
    def u(self):
        return np.cross(self.v, self.n)

    def to2d(self, p):
        p = np.asarray(p, float)
        return np.array([p @ self.u, p @ self.v])

    def dir2d(self, d):
        return self.to2d(d)

    def bbox(self):
        pts = np.vstack(self.visible) if self.visible else np.zeros((1, 2))
        return pts.min(0), pts.max(0)


def make_view(name, n=None, up=None):
    if n is None:
        n, up = VIEW_DIRS[name]
    n = np.asarray(n, float) / np.linalg.norm(n)
    v = np.asarray(up, float) / np.linalg.norm(up)
    return View(name, n, v)


def edge_polyline(edge, tol=0.05):
    """Discretise an edge (already in the view plane) to a polyline; lines keep their two end points."""
    from build123d import GeomType
    if edge.geom_type == GeomType.LINE:
        pts = [edge.position_at(0), edge.position_at(1)]
    else:
        n = int(max(8, min(400, edge.length / tol ** 0.5 / 0.6)))
        pts = edge.positions([i / n for i in range(n + 1)])
    return np.array([[p.X, p.Y] for p in pts])


def project(shape, view: View, smooth_edges=True):
    """Fill view.visible / view.hidden from build123d's HLR projection of shape."""
    vis, hid = shape.project_to_viewport(tuple(view.n * 1000.0), tuple(view.v), look_at=(0, 0, 0))
    view.visible = [edge_polyline(e) for e in vis if e.length > 1e-4]
    view.hidden = [edge_polyline(e) for e in hid if e.length > 1e-4]
    return view


def project_all(shape, names=("front", "top", "bottom", "left", "right")):
    return {nm: project(shape, make_view(nm)) for nm in names}
