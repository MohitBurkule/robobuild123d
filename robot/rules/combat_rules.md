# Combat ground-game rules (antweight / beetleweight)

Knowledge base behind `robot/checks/combat.py`. The premise: in insect-class combat **whoever gets under the other
wins**. A robot that gets lifted loses traction, steering and weapon contact; it can be pushed out, pitted, flipped or
fed to a spinner. That is why good robots run skirts, wedges and forks a fraction of a millimetre above the floor around
as much of their perimeter as possible, keep their wheels behind something, put their weight on the driven wheels, and
keep the same ground game upside down.

Each rule has: **rationale**, a **measurable criterion**, a **threshold**, **applicability** (archetype family and
edge/side) and a **severity**. `Check:` says whether the verifier measures it (finding id `combat.Rnnn`) or lists it under
NOT CHECKED. Thresholds are starting points from 150 g antweight / 1.5 kg beetleweight practice (AWS / UK ant circuit,
NHRL beetles); override them per robot when the designer has a reason, and tell the reviewer.

Conventions: mm, +Y front, +Z up, +X = the robot's left (specs name `wheel_l` at +X). "Edge gap" at a bearing = height above
the floor of the lowest non-wheel point within 6 mm of the outline at that bearing (360 one-degree bins around the
robot centre). Families: **wedge** (wedge, wedge_2wd, rammer, pusher), **vspin** (vertical spinner, forks, drum, beater),
**hspin** (horizontal, undercutter, shell/ring), **lifter** (lifter, flipper, grabber, crusher), **other**. The family comes
from `archetype` or else `robot_type`. "Low-game" = wedge, vspin, lifter, other.

Severity: **warning** unless stated; **blocker** only where the robot cannot work (weapon hitting the floor, no wheels on one
side).

---

## A. Perimeter coverage: is there something low at every edge?

### R001 Front edge sits on the floor
- Rationale: the front is where every engagement starts; a lip higher than the opponent's lets them in first.
- Criterion: median edge gap over the front sector.
- Threshold: <= 1.0 mm (wedge, lifter), <= 1.5 mm (vspin), <= 3.0 mm (others).
- Applies to: all; front edge.
- Severity: warning. Check: `combat.R001`.

### R002 Front edge covered by a low skirt
- Rationale: a lip that is low only in the middle lets an opponent in off-centre.
- Criterion: share of front bearings with edge gap <= 1.5 mm.
- Threshold: >= 80 %.
- Applies to: low-game; front. Severity: warning. Check: `combat.R002`.

### R003 Left side has a low skirt
- Rationale: side hits (T-bones) are the second most common way to be lifted; side skirts stop it.
- Criterion: share of left (+X) side bearings with edge gap <= 3 mm.
- Threshold: >= 60 %.
- Applies to: low-game and hspin; left side. Severity: warning. Check: `combat.R003`.

### R004 Right side has a low skirt
- Rationale/criterion as R003 for the right (-X) side. Threshold >= 60 %.
- Applies to: low-game and hspin; right side. Severity: warning. Check: `combat.R004`.

### R005 Rear edge is guarded
- Rationale: an opponent who gets behind you and under your rear drives you anywhere; a rear skirt or ramp denies it.
- Criterion: share of rear bearings with edge gap <= 3 mm.
- Threshold: >= 50 %.
- Applies to: all; rear. Severity: warning. Check: `combat.R005`.

### R006 Front-left corner closed
- Rationale: corners are where skirts usually stop; a wedge glancing in at 45 deg finds the gap.
- Criterion: highest edge gap in the +-10 deg arc around the corner bearing.
- Threshold: <= 5 mm.
- Applies to: all; front-left corner. Severity: warning. Check: `combat.R006`.

### R007 Front-right corner closed
- As R006 for the front-right corner. Check: `combat.R007`.

### R008 Rear-right corner closed
- As R006 for the rear-right corner. Check: `combat.R008`.

### R009 Rear-left corner closed
- As R006 for the rear-left corner. Check: `combat.R009`.

### R010 Perimeter mostly skirted
- Rationale: overall share of the outline an opponent cannot get under.
- Criterion: share of all 360 bearings with edge gap <= 3 mm.
- Threshold: >= 60 %.
- Applies to: all. Severity: warning. Check: `combat.R010`.

### R011 No wide open arc
- Rationale: one wide gap is as bad as none: the driver turns into it.
- Criterion: longest contiguous arc with edge gap > 5 mm.
- Threshold: <= 45 deg.
- Applies to: all. Severity: warning. Check: `combat.R011`.

### R012 No open door anywhere
- Rationale: an exposed wheel well or cut-out with nothing low under it is an entry point for forks.
- Criterion: maximum edge gap over the perimeter (bins with only a wheel at the edge count as open).
- Threshold: <= 12 mm.
- Applies to: all. Severity: warning. Check: `combat.R012`.

### R013 Gets under a typical wedge
- Rationale: who-gets-under-whom versus a typical competition wedge, which runs a 0.3-0.8 mm lip.
- Criterion: 20th-percentile front edge gap.
- Threshold: <= 0.6 mm.
- Applies to: low-game; front. Severity: warning. Check: `combat.R013`.

### R014 Sides resist a T-bone
- Rationale: an opponent wedge striking the side square-on gets under anything above ~2 mm.
- Criterion: median edge gap of the worse side.
- Threshold: <= 2 mm.
- Applies to: all; sides. Severity: warning. Check: `combat.R014`.

### R015 No fork-sized gap in the front edge
- Rationale: lifter/fork tines are 4-8 mm wide; a gap in the front skirt wider than a tine lets them in.
- Criterion: widest stretch (mm along the edge) of the front with no skirt within 1.5 mm of the floor.
- Threshold: <= 8 mm.
- Applies to: low-game; front. Severity: warning. Check: `combat.R015`.

### R016 Front edge level
- Rationale: a front edge that is low in one place and high in another wins only part of the contest.
- Criterion: max - min edge gap across the front sector.
- Threshold: <= 3 mm.
- Applies to: low-game; front. Severity: warning. Check: `combat.R016`.

### R017 Arena seam crossing at speed
- Rationale: arena floors have 1-2 mm steps between plates; a 0.3 mm skirt bounces or catches when crossing at speed.
- Criterion: dynamic bounce of the lip over a 2 mm step at top speed.
- Threshold: lip must ride over without stopping the robot.
- Applies to: all with fixed skirts. Severity: warning. Check: NOT CHECKED (needs a dynamic model; bench test it).

### R018 Skirt wear and lip rounding
- Rationale: printed and aluminium lips round over within a fight and then ride up on opponents.
- Criterion: lip radius after a fight.
- Threshold: <= 0.3 mm radius.
- Applies to: all skirts. Severity: warning. Check: NOT CHECKED (wear; inspect after testing). R027 covers material.

## B. Wedge and skirt geometry

### R020 Lip clears the floor
- Rationale: a lip touching the floor drags, scrapes, catches seams and digs in on hits.
- Criterion: lowest point of each front skirt/wedge/fork above the floor.
- Threshold: >= 0.2 mm (0.3 mm preferred).
- Applies to: all with a front skirt (a wedge or lifter without one fails). Severity: warning. Check: `combat.R020`.

### R021 Lip is low enough
- Rationale: above ~1 mm most competition wedges get under you.
- Criterion: lowest point of each fixed front skirt.
- Threshold: <= 1.0 mm (hinged skirts: R035).
- Applies to: all with fixed front skirts. Severity: warning. Check: `combat.R021`.

### R022 Ramp angle
- Rationale: shallow wedges (10-25 deg) slide under and lift; steep ones get under but stop the opponent instead of lifting it; very shallow ones are long and floppy.
- Criterion: median slope of up-and-forward facing surface samples on the lower 70 % of the wedge.
- Threshold: 10-35 deg (wedge), 10-45 deg (others).
- Applies to: front wedges. Severity: warning. Check: `combat.R022`.

### R023 Shallow entry
- Rationale: the first 10 mm decide whether the lip slides under or butts against the opponent.
- Criterion: median slope of the wedge surface within 10 mm of the tip.
- Threshold: <= 25 deg.
- Applies to: front wedges. Severity: warning. Check: `combat.R023`.

### R024 Sharp lip
- Rationale: the lip must be thinner than the opponent's gap; a thick lip butts against their skirt.
- Criterion: median vertical thickness 1 mm behind the front edge.
- Threshold: <= 1.2 mm.
- Applies to: front skirts. Severity: warning. Check: `combat.R024`.

### R025 Thin lip
- Rationale: as R024, further back: the lip must keep sliding under for the first few mm.
- Criterion: median vertical thickness 3 mm behind the front edge.
- Threshold: <= 2.5 mm.
- Applies to: front skirts. Severity: warning. Check: `combat.R025`.

### R026 No blunt nose
- Rationale: a vertical face at the front of the lip (e.g. square-cut printed plate) stops at the opponent's lip.
- Criterion: height of forward-facing (n_y > 0.85) surface in the last 2 mm of the lip, below floor + 4 mm.
- Threshold: <= 0.6 mm.
- Applies to: front skirts. Severity: warning. Check: `combat.R026`.

### R027 Hard lip
- Rationale: a printed lip chips and rounds over on the first hit; steel/titanium/laminate (or UHMW for skirts) keeps an edge.
- Criterion: material of each front skirt.
- Threshold: steel, hardox, stainless, titanium, aluminium, CF plate, FR4/G10 or UHMW.
- Applies to: low-game; front. Severity: warning. Check: `combat.R027`.

### R028 Skirt spans the front
- Rationale: a narrow wedge is easy to drive around.
- Criterion: width of the front skirts over body width.
- Threshold: >= 85 % (wedge, lifter), >= 40 % (others).
- Applies to: all with front skirts. Severity: warning. Check: `combat.R028`.

### R029 Skirt is the front-most part
- Rationale: anything ahead of the lip (a bolt head, a fork upright, a frame corner) touches first and stops the lip short.
- Criterion: skirt front Y minus the front-most body point (weapon excluded).
- Threshold: >= -0.5 mm.
- Applies to: low-game. Severity: warning. Check: `combat.R029`.

### R030 Tip does not dig in
- Rationale: if a point behind the tip is lower than the tip, the heel drags and the tip rides up; under a hit the tip digs into seams.
- Criterion: lowest underside 3-13 mm behind the tip minus the tip's lowest point.
- Threshold: >= -0.05 mm.
- Applies to: front skirts. Severity: warning. Check: `combat.R030`.

### R031 Lip parallel to the floor
- Rationale: a lip tilted across its width touches at one corner and pivots the robot.
- Criterion: spread of tip heights across the width (2 mm bins).
- Threshold: <= 0.5 mm.
- Applies to: front skirts. Severity: warning. Check: `combat.R031`.

### R032 Skirt stiff under push
- Rationale: a skirt that bends up under a pushing opponent lets them under; bending down digs it in.
- Criterion: cantilever tip deflection F L^3 / (3 E I) with F = 50 N, L = unsupported overhang, I = w t^3 / 12 at 2/3 of the overhang.
- Threshold: <= 1.0 mm.
- Applies to: fixed front skirts. Severity: warning. Check: `combat.R032`.

### R033 Skirt thick enough
- Rationale: below these thicknesses skirts bend permanently or snap.
- Criterion: thickness at mid-overhang.
- Threshold: metal (E >= 60 GPa) >= 0.8 mm; printed or plastic >= 2.0 mm.
- Applies to: front skirts. Severity: warning. Check: `combat.R033`.

### R034 Skirt overhang short
- Rationale: long unsupported lips flap, bend and transmit leverage to their mounts.
- Criterion: distance from the tip to the last point within 1 mm of structure.
- Threshold: <= 45 mm.
- Applies to: front skirts. Severity: warning. Check: `combat.R034`.

### R035 Hinged skirt rests on the floor
- Rationale: hinged (floating) skirts are the answer to seams: they rest on the floor and lift over steps.
- Criterion: resting gap of each hinged skirt.
- Threshold: <= 0.5 mm.
- Applies to: skirts with a joint. Severity: warning. Check: `combat.R035`.

### R036 Hinged skirt can lift
- Rationale: a hinge without travel is a fixed skirt that rattles.
- Criterion: joint range.
- Threshold: >= 10 deg (or 10 mm prismatic).
- Applies to: skirts with a joint. Severity: warning. Check: `combat.R036`.

### R037 Skirt clears the wheels
- Rationale: flexible or hinged skirts that touch a tyre when pushed brake the drive.
- Criterion: bounding-box gap between skirt and nearest wheel minus its load deflection (R032).
- Threshold: >= 1 mm.
- Applies to: all skirts. Severity: warning. Check: `combat.R037`.

### R038 Skirt bolted down
- Rationale: one screw lets a skirt pivot; skirts take the hardest hits of the robot.
- Criterion: fasteners through or threaded into each fixed skirt.
- Threshold: >= 2.
- Applies to: fixed skirts. Severity: warning. Check: `combat.R038`.

### R039 Countersunk skirt screws
- Rationale: screw heads proud of the ramp catch the opponent's lip and stop them sliding up.
- Criterion: head protrusion above the ramp face.
- Threshold: <= 0.2 mm.
- Applies to: wedges. Severity: warning. Check: NOT CHECKED (needs head-to-surface measurement along the ramp normal).

## C. Forks

### R040 At least two tines
- Rationale: one fork pivots the opponent off; two give a stable lifting line.
- Criterion: number of front forks/blades.
- Threshold: >= 2.
- Applies to: vspin, lifter. Severity: warning. Check: `combat.R040`.

### R041 Tines close together
- Rationale: an opponent wedge narrower than the gap slips between tines (typical ant wedge > 25 mm wide).
- Criterion: widest x-run between outer tines, within 15 mm of the tips, with nothing within 3 mm of the floor.
- Threshold: <= 25 mm.
- Applies to: robots with two or more forks. Severity: warning. Check: `combat.R041`.

### R042 Tines level
- Rationale: uneven tines rock the robot and only one engages.
- Criterion: difference of fork tip heights.
- Threshold: <= 0.5 mm.
- Applies to: robots with two or more forks. Severity: warning. Check: `combat.R042`.

### R043 Tines lead the chassis
- Rationale: forks that sit behind the chassis front never touch the opponent first.
- Criterion: rearmost fork tip minus the chassis (non-skirt) front.
- Threshold: >= 0 mm.
- Applies to: robots with forks. Severity: warning. Check: `combat.R043`.

### R044 Fork tine stiffness under a side load
- Rationale: tines are loaded sideways when the opponent turns; thin printed tines snap.
- Criterion: lateral deflection under 50 N.
- Threshold: <= 1 mm.
- Applies to: forks. Severity: warning. Check: NOT CHECKED (no lateral beam model).

### R045 Fork tip shape
- Rationale: pointed tips slide under rounded lips; square tips butt.
- Criterion: tip planform angle.
- Threshold: <= 60 deg included.
- Applies to: forks. Severity: warning. Check: NOT CHECKED.

## D. Weapons and the floor

### R050 Vertical weapon sweeps low
- Rationale: a vertical disc/drum must reach the opponent's lip to hit under it; a high sweep hits armour instead.
- Criterion: lowest point of the swept circle above the floor.
- Threshold: 0.8-6 mm.
- Applies to: vspin. Severity: warning. Check: `combat.R050`.

### R051 Weapon clears the floor
- Rationale: a weapon that sweeps through the floor plane strikes the arena and launches the robot.
- Criterion: lowest swept point above the floor.
- Threshold: >= 0.3 mm.
- Applies to: any spinning weapon. Severity: **blocker**. Check: `combat.R051`.

### R052 Horizontal blade height
- Rationale: an undercutter blade must hit below the opponent's armour, but above the floor and seams.
- Criterion: lowest swept point of a horizontal blade.
- Threshold: 1-15 mm.
- Applies to: hspin. Severity: warning. Check: `combat.R052`.

### R053 No gap under the weapon
- Rationale: a high weapon with no skirt under it leaves a door for opponent wedges straight into the weapon mount.
- Criterion: weapon sweep floor gap unless a skirt within 1.5 mm covers the weapon's width.
- Threshold: <= 5 mm.
- Applies to: vspin. Severity: warning. Check: `combat.R053`.

### R054 Weapon and lip in step
- Rationale: forks should just lead the disc (they feed the opponent into it); a disc far ahead of the forks takes the floor contest alone.
- Criterion: weapon sweep front minus skirt lip front.
- Threshold: -12 to +3 mm.
- Applies to: vspin. Severity: warning. Check: `combat.R054`.

### R055 Vertical weapon spin direction
- Rationale: the tooth must move up at the front; spinning down hammers the robot into the floor and throws it.
- Criterion: `weapon.spin_dir` about `spin_axis` gives v_z > 0 at the front.
- Threshold: upward.
- Applies to: vspin. Severity: warning. Check: NOT CHECKED here (covered by `kin.spin_dir`).

### R056 Weapon hit reaction (hop, wheelie)
- Rationale: on a big hit the reaction lifts a vertical spinner off its wheels (hop) or pitches it back.
- Criterion: weapon energy over robot mass x CoG lever.
- Threshold: robot lands on wheels.
- Applies to: vspin. Severity: warning. Check: NOT CHECKED (needs a hit model).

### R057 Gyroscopic lift while turning
- Rationale: turning with a spinning vertical disc rolls the robot onto one side and lifts a wheel.
- Criterion: gyro torque vs restoring weight moment.
- Threshold: torque < 0.5 x weight x half-track.
- Applies to: vspin. Severity: warning. Check: NOT CHECKED here (see `dynamics` gyro findings).

### R058 Horizontal spinner recoil
- Rationale: a hit spins the robot opposite to the blade; low traction makes it spin out.
- Criterion: blade angular momentum vs drive traction torque.
- Threshold: recovers within 90 deg.
- Applies to: hspin. Severity: warning. Check: NOT CHECKED.

### R059 Weapon spin-up time vs closing time
- Rationale: an opponent that reaches you before spin-up wins the floor contest.
- Criterion: spin-up to 80 % rpm.
- Threshold: < 2 s for ants.
- Applies to: spinners. Severity: warning. Check: NOT CHECKED.

## E. Weight, traction and drive

### R060 Weight on the driven wheels
- Rationale: pushing force is friction x normal force on the driven wheels; weight on a skid is wasted.
- Criterion: static two-line lever share of weight on the wheels (vs skirts/skids within 2 mm of the floor on the heavy side).
- Threshold: >= 70 %.
- Applies to: all. Severity: warning. Check: `combat.R060`.

### R061 Skirt is not carrying the robot
- Rationale: a loaded lip drags, wears, catches seams and loses its height advantage.
- Criterion: 1 - driven share.
- Threshold: <= 15 %.
- Applies to: all. Severity: warning. Check: `combat.R061`.

### R062 Low centre of mass (track)
- Rationale: high CoG over a narrow track rolls over on side hits.
- Criterion: CoG height / track.
- Threshold: <= 0.5.
- Applies to: all. Severity: warning. Check: `combat.R062`.

### R063 Low centre of mass (wheelbase)
- Rationale: pitch-over when braking or when lifted at the front.
- Criterion: CoG height / wheelbase (wheel and skirt contacts).
- Threshold: <= 0.6.
- Applies to: all. Severity: warning. Check: `combat.R063`.

### R064 Not top-heavy
- Rationale: mass high in the body makes lifts and flips easier.
- Criterion: CoG height / body height.
- Threshold: <= 50 %.
- Applies to: all. Severity: warning. Check: `combat.R064`.

### R065 Centred sideways
- Rationale: an off-centre CoG loads one wheel more: the robot pulls to one side and loses pushing contests.
- Criterion: |CoG x - track centre| / track.
- Threshold: <= 5 %.
- Applies to: all. Severity: warning. Check: `combat.R065`.

### R066 Centre of mass inside the wheelbase
- Rationale: CoG near a contact line tips on small bumps or under a light lift.
- Criterion: distance from CoG to the nearer contact line / wheelbase.
- Threshold: >= 10 %.
- Applies to: all. Severity: warning. Check: `combat.R066`.

### R067 Grippy tyres
- Rationale: hard plastic wheels give mu ~0.3 on steel; silicone/urethane ~1.0: three times the push.
- Criterion: tyre material (tyre part with `tyre_of`, else wheel material; catalog wheels have silicone).
- Threshold: TPU, silicone, rubber, urethane.
- Applies to: all. Severity: warning. Check: `combat.R067`.

### R068 Wheels roll over seams
- Rationale: small wheels hang on 1-2 mm seams and debris.
- Criterion: smallest wheel diameter.
- Threshold: >= 20 mm (10 x seam).
- Applies to: all. Severity: warning. Check: `combat.R068`.

### R069 Wide enough tyres
- Rationale: narrow tyres have little contact patch and cut on seams.
- Criterion: narrowest wheel width.
- Threshold: >= 6 mm.
- Applies to: all. Severity: warning. Check: `combat.R069`.

### R070 Wheels on both sides
- Rationale: skid steering needs a driven wheel on each side.
- Criterion: sides (left/right of centre) with a wheel.
- Threshold: 2.
- Applies to: all wheeled. Severity: **blocker**. Check: `combat.R070`.

### R071 4WD turns
- Rationale: a long 4WD wheelbase scrubs in turns and cannot point at the opponent.
- Criterion: wheelbase / track with four or more wheels.
- Threshold: <= 1.0.
- Applies to: 4WD. Severity: warning. Check: `combat.R071`.

### R072 Wide track
- Rationale: a narrow track tips on side hits and turns twitchily.
- Criterion: track / body width.
- Threshold: >= 50 %.
- Applies to: all. Severity: warning. Check: `combat.R072`.

### R073 Drive can spin the wheels
- Rationale: the drive should be traction-limited, so the contest is decided by the ground game, not the motors.
- Criterion: sum(stall torque) / wheel radius over mu x weight x driven share.
- Threshold: >= 1.0.
- Applies to: all with catalog motors. Severity: warning. Check: `combat.R073`.

### R074 Drive speed
- Rationale: too slow and you are outmanoeuvred to the side and rear; too fast and you cannot aim the lip.
- Criterion: rpm_nominal x pi x wheel diameter.
- Threshold: 1.5-8 m/s (spinners 1.2-8 m/s).
- Applies to: all with catalog motors. Severity: warning. Check: `combat.R074`.

### R075 Acceleration and closing time
- Criterion: time to 2 m/s. Threshold: < 0.5 s. Check: NOT CHECKED (no motor curve model).

### R076 Tyre hardness and dust pickup
- Rationale: soft silicone grips but collects dust; 95A TPU slides. Criterion: Shore hardness. Threshold: 20-40A for silicone/urethane. Check: NOT CHECKED (no hardness in the spec).

### R077 Tyre compression lowers the skirt
- Rationale: a soft tyre under load lets a fixed lip reach the floor and drag.
- Criterion: tyre compression at full weight vs lip gap. Threshold: compression < lip gap. Check: NOT CHECKED.

### R078 Drive current while pushing
- Rationale: stall in a shoving match trips the ESC or browns out the receiver.
- Criterion: stall current x motors vs ESC rating. Threshold: within rating. Check: NOT CHECKED here (see `power`/`electrical`).

### R079 Drive mixing and response
- Criterion: steering response. Check: NOT CHECKED (driver setting).

## F. Floor contact and stance

### R080 Only wheels touch the floor
- Rationale: a rigid part on the floor drags and makes the robot rock between it and the wheels.
- Criterion: non-wheel parts within 0.1 mm of the floor.
- Threshold: none.
- Applies to: all. Severity: warning. Check: `combat.R080`.

### R081 Wheels coplanar
- Rationale: a 4WD robot with one wheel high rocks diagonally and loses traction on one corner.
- Criterion: spread of wheel contact heights.
- Threshold: <= 0.3 mm.
- Applies to: 3+ wheels. Severity: warning. Check: `combat.R081`.

### R082 Belly clears the floor
- Rationale: the chassis must not scrape on seams; skirts and wedges are the only intended low parts.
- Criterion: lowest point of non-skirt chassis parts.
- Threshold: >= 1.0 mm.
- Applies to: all. Severity: warning. Check: `combat.R082`.

### R083 No high-centring
- Rationale: on a 2 mm seam a low flat belly lifts the wheels off the floor.
- Criterion: lowest underside point away from the perimeter band.
- Threshold: >= 1.5 mm.
- Applies to: all. Severity: warning. Check: `combat.R083`.

### R084 No flat dragging belly
- Rationale: large flat areas near the floor stick on debris and seams.
- Criterion: area of downward faces within 0.5 mm of the floor (non-skirt parts).
- Threshold: <= 50 mm2.
- Applies to: all. Severity: warning. Check: `combat.R084`.

### R085 Screw heads off the floor
- Rationale: pan heads under the belly are the lowest point and drag or snag.
- Criterion: lowest fastener point above the floor.
- Threshold: >= 0.5 mm.
- Applies to: all. Severity: warning. Check: `combat.R085`.

### R086 Switch off the floor
- Rationale: a switch at floor level is knocked by seams and debris.
- Criterion: lowest switch point above the floor.
- Threshold: >= 2 mm.
- Applies to: all. Severity: warning. Check: `combat.R086`.

### R087 Wires and tape under the robot
- Criterion: no wire or tape below the belly line. Check: NOT CHECKED (wire routes are deep-mode only).

### R088 Battery puncture from floor impacts
- Criterion: battery separated from the floor by >= 1 mm of structure. Check: NOT CHECKED.

## G. Inverted ground game

### R090 Invertible or self-righting
- Rationale: a robot flipped and unable to drive is counted out.
- Criterion: body height above the wheel tops (inverted the wheels must still reach the floor), unless lifter family (self-rights with the arm).
- Threshold: <= 0.5 mm.
- Applies to: all wheeled. Severity: warning. Check: `combat.R090`.

### R091 Ground game upside down
- Rationale: inverted, a robot with a skirt only on the bottom has no lip at all: double-sided wedges or top skirts keep it.
- Criterion: inverted share of the front edge within 3 mm of the floor.
- Threshold: >= 50 %.
- Applies to: invertible low-game robots. Severity: warning. Check: `combat.R091`.

### R092 No drag upside down
- Criterion: inverted lowest non-wheel edge above the floor. Threshold: >= 0.2 mm.
- Applies to: invertible robots. Severity: warning. Check: `combat.R092`.

### R093 Weapon works upside down
- Rationale: a vertical spinner that runs inverted must still reach the floor zone.
- Criterion: inverted weapon sweep above the floor.
- Threshold: 0.3-10 mm.
- Applies to: invertible spinners. Severity: warning. Check: `combat.R093`.

### R094 Body fits inside the wheels
- Rationale: an invertible robot must not ride on its top on bumps.
- Criterion: body height. Threshold: <= wheel diameter - 1 mm.
- Applies to: invertible robots. Severity: warning. Check: `combat.R094`.

### R095 Self-righting works
- Criterion: the righting mechanism rotates the robot past its tip angle. Check: NOT CHECKED.

### R096 Inverted controls
- Criterion: transmitter has an invert switch. Check: NOT CHECKED.

### R097 Behaviour on its side
- Criterion: from resting on a side, it falls back onto wheels (rounded sides). Check: NOT CHECKED.

## H. Profile and armour angles

### R100 Low profile
- Rationale: tall robots are easier to get under and to tip.
- Criterion: body height (no wheels, no weapon).
- Threshold: <= 45 mm.
- Applies to: all. Severity: warning. Check: `combat.R100`.

### R101 Front armour sloped
- Rationale: sloped faces deflect hits up and over and feed opponents onto the wedge; vertical faces take full impacts.
- Criterion: vertical (|n_z| < 0.34) share of outer, forward-facing surface.
- Threshold: <= 50 %.
- Applies to: wedge, lifter; front. Severity: warning. Check: `combat.R101`.

### R102 Side armour angled
- Rationale: angled or rounded sides deflect horizontal spinners and stop T-bone wedges digging in.
- Criterion: vertical share of outer, side-facing surface.
- Threshold: <= 90 %.
- Applies to: all except hspin; sides. Severity: warning. Check: `combat.R102`.

### R103 Top protrusions a lifter can hook
- Criterion: nothing above the top plane by > 3 mm except wheels/weapon. Check: NOT CHECKED.

### R104 Outline overhangs trap wedges
- Criterion: no undercut deeper than 5 mm on the outline. Check: NOT CHECKED.

### R105 Armour material per face
- Criterion: faces in the spinner hit zone are metal or UHMW. Check: NOT CHECKED.

## I. Wheel exposure

### R110 No wheel at the front edge
- Rationale: a wedge reaching a tyre climbs it and lifts the robot by the wheel.
- Criterion: share of front bearings where a wheel is the outermost part.
- Threshold: 0 %.
- Applies to: all; front. Severity: warning. Check: `combat.R110`.

### R111 Wheels shielded at the sides
- Criterion: share of the worse side's bearings where a wheel is outermost. Threshold: <= 25 %.
- Applies to: all; sides. Severity: warning. Check: `combat.R111`.

### R112 Wheels shielded at the rear
- Criterion: share of rear bearings where a wheel is outermost. Threshold: <= 25 %.
- Applies to: all; rear. Severity: warning. Check: `combat.R112`.

### R113 Wheels not the spinner target
- Rationale: a horizontal spinner takes off any exposed tyre.
- Criterion: share of all bearings where a wheel is outermost. Threshold: <= 10 %.
- Applies to: all. Severity: warning. Check: `combat.R113`.

### R114 Body ahead of the wheels
- Criterion: body front Y - front-most wheel Y. Threshold: >= 5 mm.
- Applies to: all; front. Severity: warning. Check: `combat.R114`.

### R115 Side wall outboard of wheels
- Criterion: body side X beyond wheel outer X on both sides. Threshold: >= 0 mm.
- Applies to: all; sides. Severity: warning. Check: `combat.R115`.

### R116 Wheels below the top
- Rationale: on a robot that does not drive inverted, wheels above the top armour are hit first from above.
- Criterion: wheel top above body top. Threshold: <= 0 mm.
- Applies to: non-invertible robots. Severity: warning. Check: `combat.R116`.

### R117 Wheel hubs survive a side hit
- Check: NOT CHECKED (hub/axle strength; see `strength`).

### R118 Wheel guards stop a spinner
- Check: NOT CHECKED (guard stiffness).

## J. Internal layout vs the ground game

### R120 Battery away from the front
- Rationale: front hits crush whatever sits right behind the lip.
- Criterion: body front - battery front. Threshold: >= 10 mm.
- Applies to: all. Severity: warning. Check: `combat.R120`.

### R121 Battery away from the sides
- Criterion: battery to side outline. Threshold: >= 5 mm.
- Applies to: all. Severity: warning. Check: `combat.R121`.

## K. Arena and opponent context

### R122 Pit and arena edge
- Rationale: long rear overhangs drop into the pit before the wheels do.
- Criterion: overhang behind the rear wheels. Threshold: <= 30 mm. Check: NOT CHECKED.

### R123 Wall rail
- Criterion: skirt lip does not catch the wall bottom rail (rail heights vary 2-10 mm). Check: NOT CHECKED.

### R124 Pushing match vs a heavier opponent
- Criterion: mu x driven weight vs opponent's. Check: NOT CHECKED (opponent unknown).

### R125 Lifter arm stays below the skirt line when lowered
- Criterion: lowered arm tip gap <= skirt gap. Check: NOT CHECKED (arm kinematics in `kinematics`).

---

### Opponent quick reference (who gets under whom)

| Opponent | Their lip | What wins | Rules |
| --- | --- | --- | --- |
| Wedge | 0.3-0.8 mm, 15-25 deg | Lower, sharper, harder lip; skirts on the sides | R001, R013, R014, R024, R027 |
| Horizontal spinner | blade 2-15 mm | No exposed wheels, angled sides, low skirts so the blade hits a skirt | R003-R004, R102, R110-R113 |
| Vertical spinner / drum | sweep 1-5 mm | Lip ahead of your body, shallow front so the tooth glances, mass low | R013, R022, R029, R062 |
| Lifter / flipper | forks 4-8 mm wide | No gaps in the front skirt, invertible or self-righting | R015, R090, R091 |
| Forks | tines with gaps | Your tines close together, level, and leading | R040-R043 |
