"""Builder profile (E3): who is building this robot, and what they own.

A Builder is one person's machine and shelf: the printer (a `mfg_profiles`
PrinterProfile id, so D1's printer data is the single source), the materials
they have spools of (catalog material ids), the processes they can run, the
tools on the bench, a budget and a skill level. Presets live in `robot/builders/*.json`;
a spec declares one with a top-level `builder` key (the preset id, or the
object itself). The `builder` check group judges the design against it - no
`builder` key and the report is unchanged.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from pathlib import Path

PRESETS = Path(__file__).parent / "builders"
SKILLS = ("novice", "intermediate", "expert")


@dataclass(frozen=True)
class Builder:
    id: str
    name: str
    printer: str  # mfg_profiles PrinterProfile id
    materials: tuple = ()
    processes: tuple = ()
    tools: tuple = ()
    budget_gbp: float | None = None
    skill: str = "intermediate"

    def skill_index(self) -> int:
        return SKILLS.index(self.skill) if self.skill in SKILLS else len(SKILLS) - 1


def _from_dict(d: dict) -> Builder:
    return Builder(str(d.get("id") or "custom"), str(d.get("name") or "custom"),
                   str(d.get("printer") or ""),
                   tuple(d.get("materials") or ()), tuple(d.get("processes") or ()),
                   tuple(d.get("tools") or ()),
                   d.get("budget_gbp"), str(d.get("skill") or "intermediate"))


def load(key) -> Builder:
    """A builder by preset id (robot/builders/<id>.json) or by the declared object."""
    if isinstance(key, dict):
        return _from_dict(key)
    for p in sorted(PRESETS.glob("*.json")):
        if p.stem == str(key):
            return _from_dict(json.loads(p.read_text()))
    raise KeyError(f"unknown builder {key!r}; known presets: {[p.stem for p in sorted(PRESETS.glob('*.json'))]}")


def skill_of(s: str) -> int:
    return SKILLS.index(s) if s in SKILLS else len(SKILLS) - 1
