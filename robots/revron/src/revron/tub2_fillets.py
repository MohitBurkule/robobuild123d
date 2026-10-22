"""[tub2] Fillet3 (R2): the lobe root where each side lobe meets the outer wall face, applied the way the feature tree does (after the unions)."""
from build123d import fillet
from .tub2_params import CH_HALF_W, CH_WALL

LOBE_ROOT_R = CH_WALL                   # RV01 Fillet3 R2: the root round is the wall thickness


def lobe_root(solid, lobe_bounds):
    """Fillet R = wall thickness (RV01 Fillet3 R2) round the closed loop where the lobe meets the wall plane |x| = CH_HALF_W."""
    y0, z0, y1, z1 = lobe_bounds
    m = CH_WALL + CH_WALL / 4   # edge search margin round the lobe

    def on_root(e):
        bb = e.bounding_box()
        return (abs(abs(bb.min.X) - CH_HALF_W) < CH_WALL / 40 and abs(bb.max.X - bb.min.X) < CH_WALL / 40
                and bb.min.Y > y0 - m and bb.max.Y < y1 + m and bb.min.Z > z0 - m and bb.max.Z < z1 + m)
    return fillet([e for e in solid.edges() if on_root(e)], LOBE_ROOT_R)
