"""Internal layout: place components inside a chassis outline as a constraint satisfaction problem.

`solve(inputs, k)` returns the top-k distinct `Layout`s. `inputs_from_spec_inputs(dict)` reads the user-facing JSON
(`robot gen layouts spec_inputs.json`): outline (or archetype default), components with optional fixed positions,
holes and compartment wishes.
"""

from .model import Component, Keepout, Layout, LayoutInputs, Link, Placement
from .solver import solve

__all__ = ["Component", "Keepout", "Layout", "LayoutInputs", "Link", "Placement", "solve"]
