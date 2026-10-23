"""[tub2] RV01 chassis rebuilt as the designer's feature tree: master params (tub2_params), +X half features mirrored.
Done natively: shell, columns, bores, corner blocks / stop wall / key / ledge, deck pockets, base seat. Still delegated to the
old modules (organic, not yet re-derived): side lobes + keyholes + nut pocket, lugs, front flanges / lattice, switch pad + slot."""
from . import tub2_fillets, tub2_lobes, tub2_front, tub2_switch, tub2_lug, tub2_tab, tub2_body, tub2_cols, tub2_blocks, tub2_pockets, tub2_seat, tub2_flange, tub2_lattice, tub2_mates, tub2_bays
from build123d import Plane
from .tub2_util import mirrored


def additions():
    """Material added on the shell: rear boss, switch pad, then the +X half blocks mirrored."""
    half = (tub2_blocks.corner_blocks() + tub2_blocks.stop_wall_key_ledge() + tub2_pockets.rear_pad()
            + [tub2_lug.lug(), tub2_tab.key_tab(), tub2_tab.wall_blend(), tub2_flange.flange()])
    return [tub2_cols.rear_boss(), tub2_tab.tab_wall('+x'), tub2_tab.tab_wall('-x').mirror(Plane.YZ)] + tub2_lobes.additions() + [mirrored(h) for h in half] + tub2_switch.switch_pad() + tub2_bays.additions()


def cuts():
    return tub2_pockets.deck_pockets() + tub2_seat.seat_cuts() + [tub2_cols.bores()] + tub2_lobes.cuts() + [mirrored(c) for c in (tub2_tab.rabbet(), tub2_tab.key_hole()) + tuple(tub2_lattice.pockets())] + tub2_front.wall_pockets() + [tub2_front.wire_slot()] + tub2_switch.switch_slot()


def chassis2():
    from .common import _U, _S
    from .params_chassis import CH
    c = CH
    adds = additions()
    old_cuts = tub2_mates.keepouts()
    shell = tub2_body.shell()
    body = _U(shell, *adds)
    tub = _S(tub2_fillets.lobe_root(body, tub2_lobes.lobe()), *cuts(), *old_cuts)
    assert len(tub.solids()) == 1 and tub.volume > shell.volume, f"tub2 boolean collapsed: {len(tub.solids())} solids, {tub.volume:.0f} mm3 (bare shell {shell.volume:.0f})"   # the blocks add more than the pockets take
    return tub2_bays.carve(tub)
