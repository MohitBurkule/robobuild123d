"""[tub2] Power switch seat: the pad under the deck the switch ears bear on (Boss-Extrude9, one skin thick, R fillets), and the switch
slot with its two pilots (Cut-Extrude10, through all). Everything is centred on the switch row (CENTRE_Y) and the bolt column X."""
from build123d import Align, BuildSketch, Cylinder, Locations, Pos, Rectangle, fillet
from .tub2_params import (CENTRE_Y, INS_RIGHT, SIDE_X, CH_IN_X, DECK, SKIN, OVER, CH_Z0, CH_Z1)
from .tub2_util import concave_filler, prism

SWITCH_X = INS_RIGHT[0][0]            # slot and pilots sit on the bolt column X
SWITCH_PITCH = 15.0                   # D1: screw pitch of the switch ears; the pad is longer by 5
PAD_LEN = SWITCH_PITCH + 5.0          # D1 of Sketch23: 20
SLOT_L, SLOT_W, SLOT_R = 12.0, 4.0, SKIN / 2   # D3 / D4 and the slot corner R
PILOT_R = 0.85                        # D2: 1.7 thread-forming pilot
PAD_R = 3 * SKIN / 2                  # R1.5 on the pad's free corners and into the wall


def switch_pad():
    """+X pad: SKIN thick under the deck, from the side pocket edge into the wall; free corners R, concave R into the wall."""
    y0, y1 = CENTRE_Y - PAD_LEN / 2, CENTRE_Y + PAD_LEN / 2
    with BuildSketch() as sk:
        with Locations((SIDE_X, y0)):
            Rectangle(CH_IN_X + OVER - SIDE_X, PAD_LEN, align=(Align.MIN, Align.MIN))
        fillet([v for v in sk.vertices() if abs(v.X - SIDE_X) < OVER], PAD_R)
    fills = [concave_filler((CH_IN_X, y), (-1, s), PAD_R) for y, s in ((y0, -1), (y1, 1))]
    return [prism(g, DECK - SKIN, DECK + OVER) for g in (sk, *fills)]


def switch_slot():
    """Slot beside the top panel plus the two pilots, cut through everything at those places."""
    with BuildSketch() as sk:
        with Locations((SWITCH_X, CENTRE_Y)):
            Rectangle(SLOT_W, SLOT_L)
        fillet(sk.vertices(), SLOT_R)
    cuts = [prism(sk, CH_Z0 - OVER, CH_Z1 + OVER)]
    for s in (-1, 1):
        cuts.append(Pos(SWITCH_X, CENTRE_Y + s * SWITCH_PITCH / 2, CH_Z0 - OVER) * Cylinder(PILOT_R, CH_Z1 - CH_Z0 + 2 * OVER, align=(Align.CENTER, Align.CENTER, Align.MIN)))
    return cuts
