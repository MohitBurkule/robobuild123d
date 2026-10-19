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
18. **Belts run enclosed.** The O-ring runs in a tunnel inside the side wall, so nothing outside can snag it.
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
