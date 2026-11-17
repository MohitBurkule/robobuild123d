# Check audit: real antweight build + fight failures (2026-11-17)

Question that started it: "is there a check that a part of a wire is outside the robot?"
Answer before this audit: partly. `contain.wire_exposed` tested only the wire CENTRELINE, only after the slow router
(full tier, deep only; skipped in the inner loop), and `external: true` exempted a wire with no reason.
`wire.exterior_support` even passes a wire outside the hull if a clip holds it. Now `wire.outside` (inner tier).

Legend: OK = existing check covers it. NEW = added in `robot/checks/realworld.py` (group `realworld`, inner tier,
tests `robot/tests/test_realworld.py`). OPEN = no check yet, reason given.

## Wiring
| Failure in real builds | Check |
|---|---|
| wire leaves the body (tube incl. insulation, below floor, no reason) | NEW wire.outside |
| wire visible through an opening | OK contain.wire_line_of_sight |
| wire in weapon / wheel sweep | OK wire.rotor_clearance, wire.rotating_clearance, spinner.wire_exposed |
| wire from static part to spinning part (winds up) | NEW wire.spans_rotation |
| wire too thin for current (melts, sags voltage) | NEW wire.gauge_current |
| solder joint with no strain relief (cracks after hits) | NEW wire.strain_relief (warning) |
| no room for wire / kinks | OK wiring.route, wiring.bend |
| wire loose outside | OK wire.exterior_support |
| wire through a solid | OK internal.wire_in_solid |
| wire cut to length / BOM | OK disasm.wire_cut |
| wire pinched in lid / panel seam on closing | OPEN: needs mating-face extraction per joint; next |
| wire on a sharp hole edge (chafe) | OPEN: needs edge-radius at wire-crossing holes |

## Electrical
| Failure | Check |
|---|---|
| battery connector under-rated (JST-PH on a spinner) | NEW connector.rating (needs `connector:` on battery) |
| ESC / battery current, C rating | OK power.esc, power.battery, physics.c_rating, physics.esc_margin |
| switch missing / wrong / unreachable | OK legal.switch, contain.switch_access, switch.* |
| failsafe / weapon disable / locking bar | OK legal.failsafe, legal.weapon_disable, legal.locking_bar* |
| receiver boxed in metal / CF (signal loss) | NEW rf.antenna |
| no visible power light | NEW led.visible (warning) |
| electronics touching motor can (heat) | NEW heat.neighbour (warning) |
| runtime too short | OK power.runtime, physics.runtime |

## Battery
| Failure | Check |
|---|---|
| LiPo against outer wall (punctured by dent) | NEW battery.armour_gap |
| LiPo near rotor | NEW battery.rotor_gap |
| LiPo loose | OK arch.battery_restraint, retention.battery_undeclared |
| LiPo visible / outside | OK contain.electronics_exposed, contain.line_of_sight |

## Fasteners / mechanics
| Failure | Check |
|---|---|
| metal-thread screw on weapon / motor backs out | NEW fastener.lock |
| thread engagement in plastic, pull-out | OK fastener.engagement, strength.bolt_pullout, joint.plastic_engagement |
| tool access, head seat, length | OK fastener.access, fastener.head_seat, fastener.too_long |
| bearing seat / retention / coaxial | OK arch.bearing_seat, arch.bearing_coaxial, retention.axial |
| shaft retention / bending | OK arch.shaft_retention, strength.shaft, arch.bolt_bending |
| wheel bore / hub on shaft | OK arch.wheel_bore, arch.axle_engagement |
| tyre slips off hub | OPEN: tyre retention only via generic retention; needs tyre stretch + lip check |
| belt off / stretch | OK tension.*, cots.belt_wrap |

## Manufacture
| Failure | Check |
|---|---|
| print orientation vs load | OK print.orientation_declared, mfg.layer_load, arch.layer_tension |
| overhang, bridge, thin wall, min hole | OK printability.*, mfg.thin_wall |
| TPU / brittle in structure | OK arch.tpu_structural, arch.upright_brittle, legal.weapon_brittle |

## Fight / rules
| Failure | Check |
|---|---|
| 150 g, 150 mm footprint | OK mass.*, legal.footprint |
| self-righting / invertible | OK dynamics.invertible, physics.invert, contain.wheel_invert |
| weapon gyro / imbalance / mount flex | OK dynamics.gyro, wobble.* |
| wedge gap / under-race | OK ground.wedge_gap, ground.clearance |
| sharp edges uncovered for transport | OK legal.sharp_cover |
| weapon spin-down time after disarm | OPEN: rule text for 2025 not extracted (see RULES memory) |
| expanded-state size (clusterbots, flippers open) | OPEN: rule text not extracted |

## Spec fields added
`wire.external` + `wire.exposed_reason`, `wire.slip_ring`, `wire.current_a`, `wire.strain_relief`, `wire.connector`,
`part.connector`, `part.antenna_out`, part kind `led`, `fastener.lock` (nyloc | threadlock | thread_forming | locknut |
safety_wire).
