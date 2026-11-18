# Limpet XXT

**UNTESTED: never built or run.** The spec passes the deep gate (`robot verify --tier full`: 0 blockers, mass 127.9 g
against the 150 g limit; warnings remain, mainly catalog mass estimates). Renders in `renders/` are verifier-generated.

A 150 g AWS antweight front-hinged flipper, a small replica of Team 13's Robot Wars heavyweight *Limpet*: a four-wheeled,
invertible box (100 x 101.5 mm footprint, inside the old v4.3 101.6 mm cube as well as the 2025 150 mm square) with a
full-width clear polycarbonate flipper/wedge hinged on the tub's top front edge, resting at 32 degrees and driven by an
SG90-class servo through a horn + drive-pin linkage. 4WD on four N10 300 rpm gearmotors whose gearbox cans sit in the
printed wheel hubs, 24 mm TPU tyres. Clear PC side plates and lid plates on standoffs and pads, zebra decals by
convention. The centre channel between the lids carries the battery, ESC and servo under an armour deck that shuts the
channel from above while leaving the weapon's swept corridor open.

- Design, masses, risks: [BRIEF.md](BRIEF.md)
- Masters and relations: `src/limpet_xxt/params.py`
- Parts: `src/limpet_xxt/parts.py` (tub, side plates, lids, flipper, hinge block, horn); `assembly.py` (`build(part)`)
- Entry: `src/build_limpet_xxt.py` (referenced by `spec.json`)
- Reused: `robot.cad.holes`, `robot.cad.bay`, `robot.cad.fastener_catalog`, `robot.catalog`, `robot.profile`
- History and photo sources: [REFERENCE.md](REFERENCE.md)
