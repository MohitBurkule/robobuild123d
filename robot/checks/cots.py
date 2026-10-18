"""Bought-in (COTS) parts must be real, listed sizes: catalog model, standard bearing / fastener designation, and the
modelled dimensions must match the listed ones."""

from __future__ import annotations

import re

import numpy as np

from .. import catalog
from ..finding import BLOCKER, fail, ok

G = "cots"
COTS_KINDS = {"motor", "weapon_motor", "esc", "receiver", "battery", "switch", "servo", "bearing", "insert", "nut", "tyre"}
DIM_TOL_MM = 0.3

# Standard ball bearings: designation -> (bore, OD, width) mm. Flanged (F/MF) share the ring dims; flange adds OD.
BEARINGS = {
    "681": (1, 3, 1), "682": (2, 5, 1.5), "683": (3, 7, 2), "684": (4, 9, 2.5), "685": (5, 11, 3), "686": (6, 13, 3.5),
    "MR52": (2, 5, 2), "MR63": (3, 6, 2), "MR74": (4, 7, 2), "MR83": (3, 8, 3), "MR84": (4, 8, 3), "MR85": (5, 8, 2.5),
    "MR95": (5, 9, 3), "MR105": (5, 10, 4), "MR106": (6, 10, 3), "MR115": (5, 11, 4), "MR117": (7, 11, 3), "MR128": (8, 12, 3.5),
    "MF52": (2, 5, 2), "MF63": (3, 6, 2.5), "MF74": (4, 7, 2.5), "MF83": (3, 8, 3), "MF84": (4, 8, 3), "MF85": (5, 8, 2.5),
    "MF95": (5, 9, 3), "MF105": (5, 10, 4), "MF106": (6, 10, 3), "MF128": (8, 12, 3.5),
    "F683": (3, 7, 3), "F684": (4, 9, 4), "F685": (5, 11, 5), "F693": (3, 8, 4), "F694": (4, 11, 4),
    "693": (3, 8, 4), "694": (4, 11, 4), "695": (5, 13, 4), "623": (3, 10, 4), "624": (4, 13, 5), "625": (5, 16, 5),
    "603": (3, 9, 5), "604": (4, 12, 4), "605": (5, 14, 5), "608": (8, 22, 7),
}
_BRG = re.compile(r"\b((?:MF|MR|F)?\d{2,4})(?:ZZ|2RS|RS|Z)?\b", re.I)
METRIC_D = {1.6, 2.0, 2.5, 3.0, 4.0, 5.0, 6.0}
STD_LEN = {2, 2.5, 3, 4, 5, 6, 8, 10, 12, 14, 16, 18, 20, 22, 25, 28, 30, 35, 40, 45, 50}


def bearing_code(p):
    txt = " ".join(str(x) for x in (p._extra.get("designation"), p._extra.get("model_no"), p.label) if x)
    for m in _BRG.finditer(txt.upper()):
        code = m.group(1)
        if code in BEARINGS:
            return code
    return None


def _ext(lo_hi):
    return np.sort(np.asarray(lo_hi[1], float) - np.asarray(lo_hi[0], float))


def run(ctx):
    r = ctx.r
    out, n = [], 0
    for rp in r.parts:
        p = rp.part
        if p.kind not in COTS_KINDS and not p._extra.get("cots"):
            continue
        n += 1
        if p.catalog:
            if rp.cat is None:
                continue  # validity.load already blocks an unknown catalog id
            want = p._extra.get("dims")
            if want is not None:
                have = _ext(rp.geom.mesh.bounds)
                try:
                    want = np.sort(np.asarray(want, float))
                except (TypeError, ValueError):
                    want = None
                if want is None or want.shape != (3,):
                    out.append(fail("cots.dims_mismatch", G, BLOCKER, "Declared COTS dims unreadable", f"`{p.id}` `dims` must be 3 numbers.").on(p.id))
                elif np.max(np.abs(want - have)) > DIM_TOL_MM:
                    out.append(fail("cots.dims_mismatch", G, BLOCKER, "Modelled size differs from the catalog",
                                    f"`{p.id}` declares {' x '.join(f'{x:g}' for x in want)} mm but catalog `{p.catalog}` is "
                                    f"{' x '.join(f'{x:.1f}' for x in have)} mm (tolerance {DIM_TOL_MM} mm).").on(p.id)
                               .fix("Use the catalog entry that matches the part you will buy, or fix the declared dims."))
            if p.shape is not None or p.model:
                try:
                    from .. import geom
                    shape = p.shape if p.shape is not None else {"type": "model", "file": p.model, "params": p.params or {}}
                    mine = _ext(geom.geom_for(shape, r.spec.base_dir, geom.FAST).mesh.bounds)
                    have = _ext(rp.geom.mesh.bounds)
                    if np.max(np.abs(mine - have)) > DIM_TOL_MM:
                        out.append(fail("cots.dims_mismatch", G, BLOCKER, "Modelled size differs from the catalog",
                                        f"`{p.id}`'s own shape is {' x '.join(f'{x:.1f}' for x in mine)} mm but catalog `{p.catalog}` is "
                                        f"{' x '.join(f'{x:.1f}' for x in have)} mm; the pocket was probably sized for the wrong part.").on(p.id))
                except Exception as e:  # noqa: BLE001
                    ctx.not_checked.append(f"cots.dims_mismatch `{p.id}`: own shape could not be built ({e})")
            continue
        if p.kind == "bearing":
            code = bearing_code(p)
            if code:
                bore, od, wd = BEARINGS[code]
                have = _ext(rp.geom.mesh.bounds)
                flanged = code.startswith(("F", "MF"))
                ok_od = abs(have[1] - od) <= DIM_TOL_MM or (flanged and od <= have[1] <= od + 1.5 + DIM_TOL_MM)
                if not (ok_od and abs(have[0] - wd) <= DIM_TOL_MM + (0.8 if flanged else 0)):
                    out.append(fail("cots.dims_mismatch", G, BLOCKER, "Bearing model does not match its designation",
                                    f"`{p.id}` is {code} ({bore} x {od} x {wd} mm) but is modelled {have[2]:.1f} x {have[1]:.1f} x {have[0]:.1f} mm.")
                               .on(p.id).fix(f"Model it at {bore} x {od} x {wd} mm or name the bearing you will actually fit."))
                continue
        out.append(fail("cots.unlisted", G, BLOCKER, "Bought-in part with an unlisted size",
                        f"`{p.id}` ({p.kind}) has no catalog id{' or standard designation' if p.kind == 'bearing' else ''}; its size cannot be bought as modelled.")
                   .on(p.id).fix("Use a catalog id (`robot catalog`) or, for a bearing, put its designation (e.g. MF85ZZ) in `designation`."))
    for f in r.spec.fasteners:
        dl = catalog.parse_designation(f.designation)
        if not dl:
            continue
        d, ln = dl
        n += 1
        if d not in METRIC_D or ln not in STD_LEN:
            out.append(fail("cots.fastener_size", G, BLOCKER, "Non-standard screw size",
                            f"`{f.id}` is {f.designation}; stocked sizes are M{'/'.join(f'{x:g}' for x in sorted(METRIC_D))} in lengths "
                            f"{', '.join(f'{x:g}' for x in sorted(STD_LEN))} mm.").on(f.id)
                       .fix("Round the length to a stocked one and adjust the counterbore."))
    if not out:
        out.append(ok("cots.listed", G, "Bought-in parts are listed sizes", f"{n} COTS parts and screws match catalog or standard sizes."))
    return out
