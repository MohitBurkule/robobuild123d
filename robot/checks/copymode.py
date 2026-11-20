"""Reference-copy mode: `"reference_copy": {"robot": "<name>", "source": "<where the real robot is documented>"}` in a spec.

A copy of a real robot has to look and work like the original, so combat-effectiveness rules that only encode OUR design
preferences (a vertical spinner's rim must reach the floor, the weapon must lead the chassis, the rotor mass share) must
not force the copy to deviate. In copy mode those findings drop from BLOCKER to WARNING ("not enforced on a reference
copy") and are listed under `copy_mode` in the report summary. Physical validity (interference, assembly, mass, fit,
fasteners, wiring) is never relaxed: a copy still has to be buildable. Our own robots (no `reference_copy`) keep every rule.
"""

from __future__ import annotations

from ..finding import BLOCKER, WARNING

# Our own combat-effectiveness taste. Anything not listed here, or in COMBAT_GROUPS, stays enforced.
COMBAT_IDS = ("spinner.reach", "spinner.mass_share", "shape.weapon_leads", "archetype.blade_lead",
              "archetype.wedgelets_flank")
COMBAT_GROUPS = ("combat", "coverage")
NEVER = {"assembly", "interference", "reference_cad"}


def declared(spec) -> dict | None:
    d = (getattr(spec, "raw", None) or {}).get("reference_copy")
    if not d:
        return None
    return d if isinstance(d, dict) else {"robot": str(d)}


def _combat(fd) -> bool:
    return (fd.id in COMBAT_IDS or any(fd.id.startswith(i + ".") for i in COMBAT_IDS)
            or fd.group in COMBAT_GROUPS) and fd.group not in NEVER


def apply(spec, findings) -> list:
    """Downgrade combat-taste BLOCKERs to WARNING on a reference copy, in place; return what was relaxed."""
    d = declared(spec)
    if d is None:
        return []
    used = []
    for fd in findings:
        if fd.passed or fd.severity != BLOCKER or not _combat(fd):
            continue
        fd.severity = WARNING
        fd.message = f"{fd.message} (not enforced: reference copy of {d.get('robot', 'a real robot')})"
        used.append({"check": fd.id, "parts": list(fd.parts or [])})
    return used
