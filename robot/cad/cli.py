"""CLI hooks for robot.cad: `measure-ref`, `gate`, and `verify --changed` (registered by robot.cli's module loop)."""

from __future__ import annotations


def add_cli(sub):
    from . import gate, measure_ref

    measure_ref.add_cli(sub)
    gate.add_cli(sub)
    v = sub.choices.get("verify")
    if v is not None:
        v.add_argument("--changed", action="store_true",
                       help="incremental: rerun only check groups whose inputs (incl. touched part geometry) changed")
