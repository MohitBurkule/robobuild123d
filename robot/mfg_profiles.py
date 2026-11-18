"""Printer and filament profiles (D1): ask what the builder owns, not what a module constant assumes.

A PrinterProfile is one machine (bed, nozzle, enclosure, temps); a Filament is one
spool (material, needs, shrink). capability(filament, printer) lists every reason
the spool cannot print on the machine (needs an enclosure, a hardened nozzle,
higher temps than the hotend allows, direct drive). printability.py and the mfg
pack read these instead of module constants as they adopt it.
"""

from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class PrinterProfile:
    id: str
    make: str
    bed_mm: tuple  # (x, y)
    z_mm: float
    nozzle_mm: float
    max_nozzle_c: int
    enclosure: bool = False
    hardened_nozzle: bool = False
    direct_drive: bool = False
    xy_hole_shrink_mm: float = 0.15
    max_bridge_mm: float = 40.0
    max_overhang_deg: float = 50.0


@dataclass(frozen=True)
class Filament:
    id: str
    base_material: str
    nozzle_c: int
    bed_c: int
    gbp_per_kg: float = 20.0
    needs_enclosure: bool = False
    needs_hardened: bool = False
    needs_direct_drive: bool = False
    needs_dry: bool = False
    shrink_pct: float = 0.4
    density_g_cc: float = 1.24
    impact_ok: bool = True  # survives being hit (PLA does not really)


PRINTERS = (
    PrinterProfile("ender3", "Creality Ender 3", (220, 220), 250, 0.4, 260),
    PrinterProfile("ender3_0.6", "Creality Ender 3, 0.6 nozzle", (220, 220), 250, 0.6, 260),
    PrinterProfile("prusa_mk4", "Prusa MK4", (250, 210), 220, 0.4, 280),
    PrinterProfile("bambu_p1p", "Bambu Lab P1P", (256, 256), 256, 0.4, 300),
    PrinterProfile("bambu_x1c", "Bambu Lab X1 Carbon (enclosed)", (256, 256), 256, 0.4, 300, enclosure=True, hardened_nozzle=True),
    PrinterProfile("voron_24", "Voron 2.4 350 (enclosed)", (350, 350), 340, 0.4, 300, enclosure=True, hardened_nozzle=True, direct_drive=True),
)

FILAMENTS = (
    Filament("pla", "PLA", 210, 60, 18.0, shrink_pct=0.35, density_g_cc=1.24),
    Filament("petg", "PETG", 240, 80, 22.0, shrink_pct=0.3),
    Filament("tpu", "TPU 95A", 230, 50, 30.0, needs_direct_drive=True, shrink_pct=0.2),
    Filament("pa6_cf", "PA6-CF nylon", 290, 100, 55.0, needs_enclosure=True, needs_hardened=True, needs_dry=True, shrink_pct=0.7, density_g_cc=1.17),
    Filament("petg_cf", "PETG-CF", 270, 90, 45.0, needs_hardened=True, needs_dry=True, density_g_cc=1.29),
    Filament("abs", "ABS", 250, 100, 20.0, needs_enclosure=True, shrink_pct=0.8, density_g_cc=1.04),
)


def printer(pid: str) -> PrinterProfile:
    for p in PRINTERS:
        if p.id == pid:
            return p
    raise KeyError(f"unknown printer {pid!r}; known: {[p.id for p in PRINTERS]}")


def filament(fid: str) -> Filament:
    for f in FILAMENTS:
        if f.id == fid:
            return f
    raise KeyError(f"unknown filament {fid!r}; known: {[f.id for f in FILAMENTS]}")


def capability(fid: str, pid: str) -> list:
    """Every reason `fid` cannot print on `pid`; [] when it can."""
    f, p = filament(fid), printer(pid)
    out = []
    if f.nozzle_c > p.max_nozzle_c:
        out.append(f"{f.id} needs {f.nozzle_c} C; {p.id} tops out at {p.max_nozzle_c} C")
    if f.needs_enclosure and not p.enclosure:
        out.append(f"{f.id} needs an enclosed chamber; {p.id} is open")
    if f.needs_hardened and not p.hardened_nozzle:
        out.append(f"{f.id} is abrasive; {p.id} has no hardened nozzle")
    if f.needs_direct_drive and not p.direct_drive:
        out.append(f"{f.id} needs direct drive; {p.id} is a bowden setup")
    return out


def bed_fit(pid: str, part_mm: tuple) -> bool:
    p = printer(pid)
    return (part_mm[0] <= p.bed_mm[0] and part_mm[1] <= p.bed_mm[1]
            and (len(part_mm) < 3 or part_mm[2] <= p.z_mm))


def hole_compensation(pid: str) -> float:
    """CAD hole shrink for this printer (mm) - printability.min_hole and fits use it."""
    return printer(pid).xy_hole_shrink_mm
