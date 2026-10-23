"""[tub2] Fillet3 (R2): the lobe root where each side lobe meets the outer wall face, applied the way the feature tree does (after the unions)."""
from build123d import Plane, fillet
from .tub2_params import CH_HALF_W, CH_WALL, CH_Z0
from .tub2_util import box_xy

LOBE_ROOT_R = CH_WALL                   # RV01 Fillet3 R2: the root round is the wall thickness


def lobe_root(solid, lobe, below=CH_Z0 - 2 * CH_WALL):
    """Fillet R = wall thickness (RV01 Fillet3 R2) round the closed loop where the lobe meets the wall plane |x| = CH_HALF_W.
    The round is made on a plain wall slab that runs on below the chassis floor (down to `below`) and added as a collar: on the real body the
    fillet runs out at the floor and the solver answers with BSplines, whose tessellation shows as 6-25 deg faceting seams; on the slab it is
    the analytic cylinder / torus RV01 has. The collar below the floor is cut off again by the lobe's floor relief."""
    bb = lobe.bounding_box()
    y0, z0, y1, z1 = bb.min.Y, bb.min.Z, bb.max.Y, bb.max.Z
    m = CH_WALL + CH_WALL / 4   # edge search margin round the lobe

    def on_root(e):
        eb = e.bounding_box()
        return (abs(eb.min.X - CH_HALF_W) < CH_WALL / 40 and abs(eb.max.X - eb.min.X) < CH_WALL / 40
                and eb.min.Y > y0 - m and eb.max.Y < y1 + m and eb.min.Z > min(z0, below) - m and eb.max.Z < z1 + m)
    wall = box_xy(CH_HALF_W - CH_WALL, CH_HALF_W, y0 - 2 * m, y1 + 2 * m, below, z1 + 2 * m)
    rooted = fillet([e for e in wall.fuse(lobe).clean().edges() if on_root(e)], LOBE_ROOT_R)
    collar = rooted - wall                       # the fillet material outside the wall slab, the lobe included
    return solid + collar + collar.mirror(Plane.YZ)
