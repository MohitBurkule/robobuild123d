"""Internal layout: place components inside a chassis outline as a constraint satisfaction problem.

`solve(inputs, k)` returns the top-k distinct `Layout`s; `inputs` is a `LayoutInputs` or the same fields as a dict
(`robot gen layouts spec_inputs.json`): outline, components (with optional fixed positions), keep-outs, holes, links.
"""

from .model import Component, Keepout, Layout, LayoutInputs, Link, Placement
from .solver import solve

__all__ = ["Component", "Keepout", "Layout", "LayoutInputs", "Link", "Placement", "solve"]
