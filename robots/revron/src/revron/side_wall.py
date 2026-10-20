"""[fix-C] Revron side-panel wall thickness and inner-face path (split out of side.py; geometry unchanged)."""
import json, math, os, sys
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403


def _sp_path(z):
    """Inner face path (X, Y) of the side wall at height z."""
    ks = sorted(SW_X)
    sw = [_interp(z, ks, [SW_X[k][i] for k in ks]) for i in range(len(SW_Y))]
    return SP_IN[:9] + list(zip(sw, SW_Y))


def _tent(v, centre, half):
    """Triangular weight: 1 at centre, 0 at centre +- half."""
    return max(0.0, 1.0 - abs(v - centre) / half)


def _sp_bump(y, z):
    """STEP RV23: the outer face swells round the nut lobe."""
    (y0, yh), (z0, zh) = SP_BUMP_Y, SP_BUMP_Z
    return SP_BUMP * _tent(y, y0, yh) * _tent(z, z0, zh)


def _sp_w(y, z):
    r, m, w = (_interp(z, SP_W_Z, t) for t in (SP_W_REAR, SP_W_MID, SP_W_SWING))
    return _interp(y, SP_W_Y, (r, m, m, w)) + _sp_bump(y, z)
