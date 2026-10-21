"""[tub2] +X half of the deck-hung blocks: the two corner blocks round the column pairs, the motor stop wall, the N10 key tab and
ledge. Each block face is tangent to its column (face x = column x - COL_R), noses are COL_R rounds, wall ends take a SKIN fillet."""
from build123d import Align, BuildSketch, Locations, Rectangle, fillet
from .tub2_params import (INS_RIGHT, COL_R, SKIN, CH_Z0, CH_IN_X, DECK, OVER, WALL_IN_FRONT, STOP_FRONT_Y, STOP_BACK_Y, SA_X0,
                          N10_KEY, N10_TOP, KEY_SPAN, LEDGE_X0, LEDGE_Y0, LEDGE_R)
from .tub2_util import box_xy, concave_filler, prism

_FRONT, _REAR = INS_RIGHT[0], INS_RIGHT[1]


def _block(face_x, nose_y, wall_y, up):
    """Corner block plan from the column-tangent face to the side wall, from the nose Y to the wall Y (up: +1 block lies toward +Y)."""
    top, bot = (wall_y, nose_y) if up > 0 else (nose_y, wall_y)
    with BuildSketch() as sk:
        with Locations((face_x, bot)):
            Rectangle(CH_IN_X + OVER - face_x, top - bot, align=(Align.MIN, Align.MIN))
        corner = [v for v in sk.vertices() if abs(v.X - face_x) < OVER and abs(v.Y - nose_y) < OVER]
        fillet(corner, COL_R)
    fills = [concave_filler((CH_IN_X, nose_y), (-1, -up), SKIN)]
    return sk, fills


def corner_blocks():
    """Front block (nose toward the rear) up to the front wall; rear block (nose toward the front) down to the stop wall front face."""
    out = []
    fx, fy = _FRONT
    sk, fills = _block(fx - COL_R, fy - COL_R, WALL_IN_FRONT + OVER, 1)
    out += [prism(sk, CH_Z0, DECK + OVER)] + [prism(f, CH_Z0, DECK + OVER) for f in fills]
    out.append(prism(concave_filler((fx - COL_R, WALL_IN_FRONT), (-1, -1), SKIN), CH_Z0, DECK + OVER))
    rx, ry = _REAR
    sk, fills = _block(rx - COL_R, ry + COL_R, STOP_FRONT_Y, -1)
    out += [prism(sk, CH_Z0, DECK + OVER)] + [prism(f, CH_Z0, DECK + OVER) for f in fills]
    out.append(prism(concave_filler((rx - COL_R, STOP_FRONT_Y), (-1, 1), SKIN), CH_Z0, DECK + OVER))
    return out


def stop_wall_key_ledge():
    """Motor stop wall (one wall thick), the key tab between the N10 gearbox plates (reaches SKIN below the plate top), the ledge and its R fillets."""
    top = DECK + OVER
    xo = CH_IN_X + OVER
    stop = box_xy(SA_X0, xo, STOP_BACK_Y, STOP_FRONT_Y, CH_Z0, top)
    key = box_xy(N10_KEY[0], N10_KEY[1], KEY_SPAN[0], STOP_FRONT_Y, N10_TOP - SKIN, top)
    ledge = box_xy(LEDGE_X0, xo, LEDGE_Y0, STOP_FRONT_Y, N10_TOP + OVER, top)
    fil = [prism(concave_filler(c, q, LEDGE_R), N10_TOP + OVER, top)
           for c, q in (((LEDGE_X0, STOP_BACK_Y), (-1, -1)), ((CH_IN_X, LEDGE_Y0), (-1, -1)))]
    return [stop, key, ledge] + fil
