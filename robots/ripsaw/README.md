# Ripsaw

**UNTESTED: never built, run, rendered or verified.**

A 150 g AWS antweight vertical disc spinner. It uses a 60 mm single-tooth hardox disc on a Repeat 2004 2800 kV hub motor,
held in double shear between the printed tub rails. Drive is 2WD (N10 motors, DuraHubs 30), with two self-levelling Ti
forks reused from Revron. The size limit is one setting, `params.RULES_SIZE`. The default, `aws2025`, is the 150 mm floor
square from robot/profile.py, which gives about 110 x 80 x 45 mm. The optional `aws_v43_cube` is the 101.6 mm cube and gives a
shorter tub.

- Design, masses, energy, risks: [BRIEF.md](BRIEF.md)
- Masters and relations: `src/ripsaw/params.py`
- Parts: `tub.py`, `disc.py`, `weapon_mount.py`, `forks.py`, `drive.py`, `panels.py`; `assembly.py` (`build(part)`)
- Entry: `src/build_ripsaw.py` (referenced by `spec.json`)
- Reused: revron `plate.py`, `hw.py`, `weapon_motor.py`, `fork.py` (via `src/ripsaw/_reuse.py`); `robot.cad.bay.derive_bay`,
  `robot.cad.fastener_catalog`, `robot.catalog`, `robot.profile`.
