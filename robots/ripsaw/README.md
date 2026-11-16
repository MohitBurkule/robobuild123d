# Ripsaw

**UNTESTED: never built or run.** The spec passes the deep gate (`robot verify --deep`: 0 blockers, mass 145.7 g against
the 150 g limit; warnings remain, mainly catalog mass estimates). Renders in `renders/` are verifier-generated.

A 150 g AWS antweight vertical disc spinner: a 44 mm single-tooth hardox disc on a Repeat 2004 2800 kV hub motor, carried
between two **printed, bolt-on weapon plates** (serviceable: three M2x12 each from inside the tub, threading into tapped
heels; both plates off and the disc + bell + shaft slide forward out of the slot). Drive is 2WD (BBB N10 gearmotors in
printed cradles, 20 mm silicone wheels whose hub bores are cut to the shaft's D-flat), on a GNB 2S 450 mAh 80C pack that
holds the 180 s fight. Two self-levelling Ti forks reused from Revron hang on M3 pins through the plates. The size limit
is one setting, `params.RULES_SIZE`; the default `aws2025` fits a 122 mm square (limit 150).

- Design, masses, energy, risks: [BRIEF.md](BRIEF.md)
- Masters and relations: `src/ripsaw/params.py`
- Parts: `tub.py`, `disc.py`, `weapon_mount.py`, `forks.py`, `drive.py`, `panels.py`; `assembly.py` (`build(part)`)
- Entry: `src/build_ripsaw.py` (referenced by `spec.json`)
- Reused: revron `plate.py`, `hw.py`, `weapon_motor.py`, `fork.py` (via `src/ripsaw/_reuse.py`);
  `robot.cad.fastener_catalog`, `robot.catalog`, `robot.profile`.
