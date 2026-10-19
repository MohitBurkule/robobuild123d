# Design intent rules for `robot gen`

Every feature the generator emits records why it exists and what sized it:

```
intent = {purpose, reason, load_or_constraint}
```

A feature is any of:
- a part;
- a solid added to a shell half;
- a cut;
- a pocket;
- a fastener;
- a wire;
- a joint between parts.

`purpose` is one of:
- `load_path`: carries a force;
- `retention`: holds a part in place;
- `assembly`: lets it be put together;
- `service`: lets it be taken apart or switched;
- `protection`: keeps hits off something;
- `ground_game`: wins at floor level;
- `wiring`;
- `mass`: removed because it carried nothing.

Where these live:
- The records are in `spec.generator.features`.
- The plan API (`plan.part/add/cut/late_cut/pocket/screw/wire/connect`) takes `intent=`.
- `robot/gen/intent.py: check()` lists every feature without a valid intent.
- The gate refuses such a spec. The tests build every preset and require the list to be empty.

The rules below were mined from three sources:
- the merged Revron spec and its builder (`robots/revron/src/build_revron.py`);
- the RVRN build guide notes in `research/revron_deconstruction.md`;
- the RVRN reference STLs in `research/rvrn_drive`, read as measurements only, never imported.

Each rule names the generator code that applies it.

## Load path

1. **Support the weapon at both ends.**
   - Revron: a stator clamp on one upright and an MF85ZZ in the other.
   - The disc is never cantilevered off the motor's own bearings.
   - Generator: `weapon_drisk` puts the motor stator on `upright_r` and a 683 bearing in `upright_l`, joined by a lengthened shaft.
2. **Print an upright flat, with the axle along the build direction.**
   - Layer lines must not shear across the axle hole (RVRN guide).
   - Generator: uprights use `print_orientation="+x"`.
3. **Two fixings per bolted-on part, spread against the lever of the load.**
   - Revron: two standoffs per upright, three M3 per wedglet.
   - Generator: forks and wedgelets get two side-wall screws spread `FORK_ROOT - 8` mm apart. Upright feet get a low screw and a high screw, which form a couple.
4. **Every screw runs into a boss, never into the bare wall.**
   - Revron: 5 heat-set insert bosses, plus aluminium-nut pockets with a 2.1 mm wall outboard.
   - Generator: `intent.boss_r_for` gives insert OD / 2 + 1.2 mm. The boss is as deep as the load needs (6–10 mm on front and side walls).
5. **Walls are sized from the side load, with the print minimum as the floor.**
   - Side load: a 150 g robot at 3 m/s, shared by the wall strips between housings, about 34 N.
   - The bending formula `intent.wall_for` gives 1.5 mm.
   - 4 perimeters of 0.42 mm (1.6 mm) governs, matching the RVRN guide's "4–6 perimeters".
   - The reasoning is recorded as `wall_basis`.
6. **A shaft is either keyed or captured, never just a friction fit.**
   - Revron: a D-shaft with a grub screw on the flat, and standoffs held by screws in both ends.
   - Generator: rear hubs have a D-bore with `mechanical_key`. Front axles are captured in the split-plane bore and clamped by the top half.
7. **Belts and O-rings carry drive to the axles without extra motors.**
   - Revron: two N10 motors and two O-rings give 4WD.
   - Generator: the 4WD belt option of `drive.add_drive` (`belt_geometry`) works out the ideal ring from the centre distance at 10 % stretch over the flanges, then picks the nearest stock 1.0 mm-section metric O-ring (`belt.stock`). You buy belts; you do not make them.

8a. **Two discs straddle the bell when the energy is needed wide (RVRN 2.0).**
   - The motor-side disc is keyed to the bell face. The floating disc rides round the can. A spider spaces the two discs.
   - Two long M2 through disc, spider and the tapped floating disc make one rotor.
   - Generator: `disc_stack=spider_pair` in `weapon_drisk._spider_pair`.
   - The lock pin circle moves in to keep the laser web rule (0.75 t to the tooth roots).
8b. **Uprights on standoffs in a tub (Revron).**
   - Each upright is clamped to the inner ends of two 5 mm alu standoffs.
   - The standoffs are pressed through a lug at the chassis corner. The wedgelet hangs on their outer ends.
   - A hit goes upright, then standoff, then lug, then side wall.
   - Generator: `chassis=tub` in `weapon_drisk._standoff_mount`.
   - Experimental: it is built only on request, with `experimental: true`. It still has 6 blockers (see `hypothesis.EXPERIMENTAL`).

## Retention

8. **A bought part sits in a snug pocket on all faces.** The clearance follows from how the part is held (`intent.pocket_gap`):

   | Holding method | Clearance |
   |---|---|
   | Press fit | 0.1 mm |
   | Captive | 0.3 mm |
   | Velcro or tape | 0.4 mm |

   Revron: a battery + ESC + Malenki stack between ribs, and N10 motors that drop into pockets with stop walls.
9. **Motors are keyed by their gearbox flats.** The pocket is snug on the flats, so reaction torque goes into the shell.
10. **Anything that could turn about a single fixing gets a key.**
   - Revron: the wedglet clip bears on the box section.
   - Generator: the wedgelet on the front axle hooks over the roof edge (`interlock`, `mechanical_key`). The drisk upright foot has a hook tab over the roof.

## Assembly and service

11. **The screw axis is the assembly direction.** A part that goes on from the front is screwed rearward. The halves close from above, so their screws are driven down (`intent.screw_dir`).
12. **Brass threads go wherever a part is swapped between fights.**
   - Revron: heat-set inserts and press-in aluminium nuts.
   - Generator: inserts in front-wall and side-wall bosses.
13. **The weapon is a module that comes off with a few screws.**
   - Revron: unbolt 4 M3 and the weapon module lifts off.
   - Generator: the uprights carry the motor, disc and bearing and come off with 4 M2.
14. **Wheels come off from outside without opening the shell.**
   - Rear wheels use a slide-on opening in the side wall.
   - Front 4WD wheels drop into their wells before the top half goes on.
15. **The switch is reachable with a finger and recessed below the surface.**
   - AWS rule. Revron: the switch is on the rear boss and you pull it rearward to turn it off.
   - Generator: a roof slot with a 1.2 mm recess.

## Protection

16. **Edges that take hits or touch the bed are bevelled.**
   - Bed edge: removes the elephant's-foot lip.
   - Hit edge: gives a corner a ramp to slide off.
   - Generator: `intent.chamfer_for` gives print 1.0 mm and impact 1.5 mm.
17. **Wheels sit in closed wells, and an arch guards a tyre top that rises above the roof.**
   - Revron: side panels act as armour and wheel retainers.
18. **Belts run enclosed.** The pulley groove sits on the inboard side of the wheel, in a closed pulley room cut into both shell halves, so no ray from outside reaches the O-ring (CF-DB03).
19. **Screw heads sit in counterbores below the surface.** Roof bolts are counterbored 2.2 mm.

## Ground game

20. **Lips sit just off the floor.**
   - Wedge: 0.6 mm, so it clears arena seams.
   - TPU skirt: 0.3 mm, because it flexes.
   - Generator: the drisk wedgelets and forks also run 0.6 mm off the floor.
21. **Wedgelets and forks lead the weapon by about 6 mm.** They feed the opponent up into the teeth.
22. **4WD keeps traction when the front is lifted** and pushes with the weapon's weight over the front axle.

## Wiring

23. **Leads run in floor channels under the parts.** No lead crosses a moving part or is pinched between parts.
   - Revron: phase wires run through the box section and out through a hole in the chassis.
   - Generator: the drisk phase leads leave through the front wall under the right upright.

## Mass

24. **Remove material only where the verifier reports it carries nothing** (`material.saveable_g`).
   - Revron: X-ribbed floor pockets, 4 lightening pockets in each disc, 6 holes in the base panel.
   - Generator: the gate's lighten pass. Wheels become a web with 5 windows.

## Adversarial intent

Every intent names the attacks it answers (`threats: [...]`, attack ids from `robot/gen/threats.py` or failure-mode
ids `CF-xxxx` from `robot/gen/data/combat_failure_modes.json`). The gate runs `intent.check(spec, adversarial=True)`,
which casts each attack's rays at the built robot and fails any reachable critical or fragile feature that has no
honest answer. Per-robot reports: `/mnt/project-files/robot-cad/gen/threats/<robot>.md`.

### The ground game comes first

In the UK 150 g class most fights are decided by who gets under whom (taxonomy: the front-interface axis, wedge /
wedgelets / forks / skirt, is listed as decisive; every winning archetype in it carries one). A robot that is lifted
loses its traction, its weapon's bite and often the fight to an arena wall, so `lift_and_throw` is the top threat
class. For each of 8 directions the engine scores: **under-ness** (our lowest leading edge against an opponent lip at
0.3-0.5 mm), **bite** (downward-facing steps a rising tooth can catch, what it would rip off and how high it would
launch us) and **edge shape** (ramp vs square), on the same perimeter profile as the verifier's combat.R0xx rules.
Each hypothesis states how it plays it (`generator.ground_game`): front interface, side and rear skirts, lip
material, and the trade-off; any direction it leaves open is an accepted risk with a reason.

25. **Every direction is skirted or accepted.** Front lip <= 1.0 mm, sides and rear <= 3.0 mm over most of the arc; the
    default `skirts=sides_rear` adds a 0.5 mm lip skirt round the sides and rear (it runs under the wedge's side ends
    and fills right up under side-mounted tines, 0.15 mm below their sloping edge). Skirts are the robot's mass trade:
    when a variant is over 150 g only on mass after lightening, the gate steps `sides_rear -> rear -> none` and records
    `generator.skirt_trade`; the lighter variant's ground-game statement accepts the directions it opens. A rear skirt
    wraps both rear quarters to mid-length (the 45 deg rear-quarter sector reaches that far) and, behind a front ramp,
    the front quarters beside its root. Rationale: a side or rear T-bone is how wedges beat a front-only wedge
    (CF-WL07, CF-WL01).
26. **No bite edges.** No downward face 1-30 mm up that a tooth reaches first. The wedge's ramp ends are closed by 1.2 mm
    cheeks down to lip height. Ti fork bolts are countersunk flush in 2 mm plates. The 4WD TPU wedgelet's edge over the
    front wheel's door and its axle screw head stay an accepted risk. An arch directly over a tyre and a seat under a flush screw head
    do not count, because the tyre or the head is met first. Rationale: a vertical spinner lifts by the first ledge it
    catches (CF-VS01, CF-VS05).
27. **Lips and tines follow CF-AS01..04.** Tip underside 10-20 deg with a 0.3-1 mm tip radius; a >= 1 mm
    under-chamfer or a hinge; tip pressure < 5 MPa with 0.5-5 N/mm stiffness for a flexible lip; tines > 8 mm
    wide, joined or tip-rounded when 2-6 mm and flexible. The generator writes the numbers into each lip's intent;
    a rule it misses is an accepted risk with a reason. Rationale: floor gouges, seams and floor-wall gaps catch
    lips (taxonomy: forks vs. wedge stalemates).

### Shielding

28. **A critical or fragile feature is shielded or accepted.** Critical: drive, weapon, power, radio. Fragile: belt,
    wire, switch, tyre, thin print. Shields: inside the hull, behind armour, recessed, captured (all must be
    unreachable), or doubled, sacrificial, guarded (honest about being reachable). Rationale: chunk removal and
    single points of failure end fights (CF-GD01, CF-GD02).
29. **Belts inside** (CF-DB03, CF-OW03). The groove is inboard of the tyre, in a closed pulley room.
30. **Battery >= 10 mm from every exposed face, receiver and ESC >= 8 mm from the skin** (CF-GD03, CF-GD04). The
    layout solver enforces it; a robot too small for it builds on a relaxed tier that the spec records
    (`generator.margins`) as an accepted risk.
31. **Each drive side has its own motor lead, and the motors sit on opposite sides** (CF-GD02, CF-GD05).
32. **Moving-to-static gaps are < 1.5 mm or > 15 mm** (CF-DB01, CF-DB02). Wheels run 0.4-1 mm from their wells. The
    disc's 2-4 mm running gap stays an accepted risk. A concentric fender can close the 3.6 mm gap at the top-front
    corner, but the verifier's CF-DB02 sectors below the axle are set by the uprights, which sit 3.5-5 mm axially from
    the disc to clear its 2.5 mm hub boss. Clearing them needs a weapon-module redesign (a flush hub, or uprights
    under 1.5 mm from the disc face).
33. **Switch recessed 2 mm, sliding across the robot** (CF-GD06). The layout fixes its slide axis along x, square to
    the front-rear scrape of an opponent or a wall. Only a point dropped straight down the slot reaches it, which
    stays an accepted risk: at worst it turns the robot off, and the robot is failsafe. A spec records in
    `generator.margins.switch_across` whether the layout had to turn it.
34. **Screws on impact faces are countersunk or recessed** (CF-ST04). Wedge, skirt and plow webs take ISO 10642 heads
    flush in a cone, Ti fork bolts are countersunk (declared `secondary_ops: countersink`), and roof bolts are
    counterbored. Heads on replaceable contact parts (upright feet, the 4WD TPU wedgelet's axle screw) are accepted.
35. **Weapon supports take a front hit in compression.** The upright's rear face bears on the chassis, so a hit
    pushes it into the structure and not off its screws (CF-OW04, CF-ST04).
36. **Cheap, replaceable parts sit at the contact points.** Uprights, wedgelets, fork sheets, tyres and the wedge are
    bolt-on spares, marked `sacrificial` or `guarded`. Rationale: in a 3-minute fight, a 20 p part is what should
    break (taxonomy: Revron's quick-change wedgelets).
