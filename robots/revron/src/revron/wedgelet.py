"""[fix-C] Revron wedgelet group (split out of side.py; geometry unchanged)."""
import json, math, os, sys
from .params import *  # noqa: F401,F403
from .common import *  # noqa: F401,F403


def wedgelet(s):
    """RV17/18 TPU wedgelet (left built, right mirrored), slabs along X (WG_X) measured on the STEP sections:
    an outer block round the 15 mm standoff end, a ring step, a 2.3 mm ramp skin over a hollow whose top edge is
    capped by an arc swept along the ramp (WG_SKIN_CAP), the cheek round both standoffs with the fork-tail kidney slot and the 2.5 mm fork slot
    through it, and a nose tab. Ramp face 50 deg: Z = FLOOR_Z + RAMP_SLOPE (RAMP_REACH - Y)."""
    from shapely.geometry import LineString, Point, Polygon, box
    P = lambda pts: Polygon(pts).buffer(0)  # noqa: E731
    (r1, tail1), (r2, tail2) = WG_S1, WG_S2
    s1 = Point(*SB).buffer(r1, ARC_N).union(P(tail1))
    s2 = Point(*SB).buffer(r2, ARC_N).union(P(tail2))
    skin, cheek, tab = P(WG_SKIN), P(WG_CHEEK), P(WG_TAB)
    in_slot = P(WG_IN_SLOT).union(Point(*SA).buffer(r1, ARC_N))
    # the nose tab bears on the weapon mount's nose: take the mount's boss outline (its side profile above the
    # notch-to-nose line) out of the tab in 2D and drop any sliver thinner than a TPU wall, so no film is left
    mprof = _mount_profile("l" if s < 0 else "r").intersection(_mount_clip())
    tab = tab.difference(mprof.buffer(WG_MOUNT_GAP, ARC_MOUNT)).buffer(-WG_TAB_FILM, join_style=2).buffer(WG_TAB_FILM, join_style=2)
    bb = _b()
    xb, xr, xs, xc, xt, xe = WG_X
    # skin cap: arc in (X, W = Z - k Y) drawn on the XZ plane (Y = 0) and swept along (0, 1, k) over the skin
    k, (cx, cw), rc = WG_SKIN_CAP["k"], WG_SKIN_CAP["c"], WG_SKIN_CAP["r"]
    xcap = min(cx + rc, xc)
    cap = Point(cx, cw).buffer(rc, ARC_N).union(box(xs, cw, xcap, cw + rc)).intersection(box(xs, cw - rc, xcap, cw + rc))
    reach = RAMP_REACH + rc
    cutter = bb.Solid.extrude(_face(cap, "xz")[0], bb.Vector(0, reach, k * reach))
    sk = _S(_ext(skin, "yz", xs, xc), cutter)
    body = _U(_ext(s1, "yz", xb, xr), _ext(s2, "yz", xr, xs), sk, _ext(cheek, "yz", xc, xt), _ext(tab, "yz", xt, xe) if not tab.is_empty else None)
    line, half, kx = WG_KIDNEY
    bx0, bx1 = WG_BORE_X
    cuts = [_ext(cheek.difference(in_slot), "yz", *WG_FORK_SLOT_X),               # 2.5 mm fork slot through the cheek
            _cyl(WG_BORES["sa"], bx0, bx1, SA), _cyl(WG_BORES["sb"], bx0, bx1, SB), _cyl(WG_BORES["sb_head"], xr, bx1, SB),
            _ext(LineString(line).buffer(half, ARC_KIDNEY), "yz", *kx),
            _ext(P(WG_TAIL_ENTRY[0]).union(LineString(line).buffer(half, ARC_KIDNEY)), "yz", WG_TAIL_ENTRY[1], xt)]   # tail entry from the notch
    # TPU cannot print the ramp's knife toe: keep the full reach but stand the toe on a printable land,
    # the ramp face running parallel to the measured one from there
    body = _U(body, _I(_ext(P(WG_TOE), "yz", xb, xe), _ext(s1.union(cheek).union(tab).buffer(WG_MERGE_EPS), "yz", xb, xe)))
    sh = _S(body, *cuts)
    sh = sh if s < 0 else _mirror_x(sh)
    # the STEP leaves the fork tine and the mount boss inside the TPU nose; cut their seats (the tine slides into a
    # 1.5 mm slit, the TPU nose tab bears on the mount)
    # the nose tab grazes the chassis lug by 0.1 mm: take the chassis out of it (a printed TPU nose conforms)
    sh = _S(sh, _fork_slot(s), weapon_mount("l" if s < 0 else "r"))
    # the chassis is only valid to cut on its +X half (the -X cut of the same shape comes back non-manifold), so always
    # take it out in the +X frame and mirror back: both hands then get the same, symmetric cut
    # only the nose tab (|X| beyond the chassis wall WG_X[4]) meets the chassis; the cheek just touches the wall plane. Cutting
    # the tab alone keeps the wall's lug outline from imprinting a zero-width spur on the cheek's end face
    shp = sh if s > 0 else _mirror_x(sh)
    wall, big = -WG_X[4], 200.0
    tab_part = _I(shp, _box(wall - big, wall, -big, big, -big, big))
    rest = _I(shp, _box(wall, wall + big, -big, big, -big, big))
    tab_cut = _one(tab_part.cut(_one(chassis())))   # no clean(): merging faces after the grazing chassis cut leaves the nose tab non-manifold
    cut_r = _one(rest.fuse(tab_cut))
    return cut_r if s > 0 else _mirror_x(cut_r)
