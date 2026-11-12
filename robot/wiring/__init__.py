"""Wiring harness for any robot spec: real gauges, catalogue connectors, a netlist, smooth bundled routes, wire solids,
chassis channels / tie points derived from the routes, and checks. See DESIGN.md; entry point `plan.build(r, world)`.

Submodules are imported on use (`from robot.wiring import plan`), so the catalogues stay usable without the geometry stack.
"""
