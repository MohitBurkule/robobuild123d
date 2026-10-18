"""Template engine for 150 g UK antweights (AWS 2025 rules).

hypothesis -> layout (CSP) -> external geometry -> assembled spec.json -> verifier gate.

- `hypothesis`: the enumerable design space and its pruning rules (`rules`, `budget`).
- `layout`: places internal components inside a chassis outline (constraint solver, top-K layouts).
- `external`: shell, wheel pockets, skirts, wedge/forks, weapon mounts, screws/inserts, wire channels, switch.
- `build`: hypothesis + layout -> spec dict; `gate` runs the verifier and repairs or rejects.
"""
