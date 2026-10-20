"""[W1] Chassis tub shell: outer box with R2 plan corners and a top chamfer, inner cavity, insert columns and corner blocks,
deck and seat cuts, electronics cage ribs. Features live in tub_shell_cols (added material) and tub_shell_cuts (removed)."""
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403
from .tub_util import inset_rect, inner
from .tub_shell_cols import column_adds
from .tub_shell_cuts import deck_pockets, seat_cuts, stop_wall_round, column_bores, switch_slot

TOP_R = 0.5                      # R of the top face outline after the chamfer inset
CAVITY_R = 1.0                   # R of the inner cavity corners
RIB_GAP = 0.1                    # cage ribs stand this far off the Malenki / ESC faces
RIB_T = dict(x0=1.28, x1=1.2, y=1.0)           # rib thickness: -x (gap to the pack), +x, -y
RIB_Y = (-12.0, 8.0)             # Y span of the side ribs
RIB_FRONT_X = 14.6               # length of the -y rib
RIB_ESC_UP = 0.9                 # the -y rib reaches down this far over the weapon ESC top face height WE_Z[0]
RIB_INTO_DECK = 1.1              # ribs run up into the deck skin


def shell(c):
    """Closed-top box: R plan corners, a chamfer loft cap on the top edges, inner cavity up to the deck underside."""
    b = _b()
    cham, z0, z1 = c["cham"], c["z0"], c["z1"]
    plan = _round(inset_rect(c, 0), r_out=cham)
    top = _round(inset_rect(c, cham), r_out=TOP_R)
    lo = _face(plan, "xy")[0].outer_wire().moved(b.Location((0, 0, z1 - cham)))
    hi = _face(top, "xy")[0].outer_wire().moved(b.Location((0, 0, z1)))
    outer = _U(_ext(plan, "xy", z0, z1 - cham), b.Solid.make_loft([lo, hi], ruled=True))
    cavity = _round(inset_rect(c, c["wall"]), r_out=CAVITY_R)
    return _S(outer, _ext(cavity, "xy", z0 - 1, c["deck"]))


def additions(c):
    """Solids to union into the shell: columns, feet, corner blocks, motor stop wall, N10 key tab and ledge."""
    return column_adds(c)


def cuts(c):
    """Solids to subtract after the unions (the old order is irrelevant: one boolean cut)."""
    return deck_pockets(c) + seat_cuts(c) + stop_wall_round(c) + column_bores(c) + switch_slot(c)


def ribs(c):
    """Electronics cage ribs, unioned AFTER the cuts: 0.1 off the Malenki -x / +x faces and the weapon ESC -y face."""
    (ex0, ex1), (ey0, ey1), ez0 = RX_X, RX_Y, RX_Z[0]
    g, t, top = RIB_GAP, RIB_T, c["deck"] + RIB_INTO_DECK
    return [_box(ex0 - g - t["x0"], ex0 - g, *RIB_Y, ez0, top),
            _box(ex1 + g, ex1 + g + t["x1"], *RIB_Y, ez0, top),
            _box(0.0, RIB_FRONT_X, ey0 - g - t["y"], ey0 - g, WE_Z[0] + RIB_ESC_UP, top)]
