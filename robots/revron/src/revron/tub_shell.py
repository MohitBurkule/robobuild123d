"""[W1] Chassis tub shell: outer box with R2 plan corners and a top chamfer, inner cavity, insert columns and corner blocks,
deck and seat cuts. Features live in tub_shell_cols (added material) and tub_shell_cuts (removed)."""
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403
from .tub_util import inset_rect, inner
from .tub_shell_cols import column_adds
from .tub_shell_cuts import deck_pockets, seat_cuts, stop_wall_round, column_bores, switch_slot

TOP_R = 0.5                      # R of the top face outline after the chamfer inset
CAVITY_R = 1.0                   # R of the inner cavity corners


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

