"""[tub2] RV01 chassis rebuilt as the designer's feature tree: master params (tub2_params), +X half features mirrored.
Done natively: shell, columns, bores, corner blocks / stop wall / key / ledge, deck pockets, base seat. Still delegated to the
old modules (organic, not yet re-derived): side lobes + keyholes + nut pocket, lugs, front flanges / lattice, switch pad + slot."""
from . import tub2_fillets, tub2_lobes, tub2_body, tub2_cols, tub2_blocks, tub2_pockets, tub2_seat
from .tub2_util import mirrored


def additions():
    """Material added on the shell: feet, rear boss, then the +X half blocks mirrored."""
    half = tub2_blocks.corner_blocks() + tub2_blocks.stop_wall_key_ledge()
    return [tub2_cols.feet(), tub2_cols.rear_boss()] + tub2_lobes.additions() + [mirrored(h) for h in half]


def cuts():
    return tub2_pockets.deck_pockets() + tub2_seat.seat_cuts() + [tub2_cols.bores()] + tub2_lobes.cuts()


def chassis2():
    from .common import _U, _S
    from .params_chassis import CH
    from . import tub_lobes, tub_lugs, tub_front, tub_shell_cuts
    from .tub import switch_pad, CHASSIS_MIN_VOL
    c = CH
    adds = additions() + tub_lugs.additions(c) + tub_front.additions(c) + [switch_pad(c)]
    old_cuts = tub_lobes.panel_mating() + tub_lugs.cuts(c) + tub_front.cuts(c) + tub_shell_cuts.switch_slot(c)
    body = _U(tub2_body.shell(), *adds)
    tub = _S(tub2_fillets.lobe_root(body, tub2_lobes.bounds()), *cuts(), *old_cuts)
    assert len(tub.solids()) == 1 and tub.volume > CHASSIS_MIN_VOL, f"tub2 boolean collapsed: {len(tub.solids())} solids, {tub.volume:.0f} mm3"
    return tub
