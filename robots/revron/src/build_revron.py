"""Revron (RVRN 2.0) generator.

Every part is built here from scratch with build123d, from named dimensions measured on the RVRN 2.0 STEP
(research/rvrn_step, measured with trimesh sections, never imported). The spec (robots/revron/spec.json) references the
parts as `{"type": "model", "file": <this file>, "params": {"part": "<name>"}}`, so `build(part=...)` below is the only
geometry entry point; running this file as a script writes the spec.

Frame: X right, Y forward (weapon end), Z up, floor at Z = 0. RVRN 2.0 assembly frame -> ours: X = -z_ref,
Y = -x_ref, Z = y_ref (a proper rotation, no offset), so left-hand parts (RV02, RV17, RV23) sit at -X.

Architecture (RVRN 2.0 STEP): GR1507 drisk on two 8 mm printed XALT HD weapon mounts (RV03 carries the stator through a
1.5 mm back spacer, RV02 the threaded shaft end in an outboard bearing); a 3 mm aluminium spider on the bell drives two
3 mm Hardox single-tooth eccentric "floating" discs and a 6 mm printed spacer on 4 long M2. The mounts drop onto the
chassis tabs (notch), 4 M3x12 CSK alu screws through the mounts and the chassis lugs into 2 x 25 + 2 x 15 mm alu
standoffs; TPU wedgelets (RV17/18, with the 1.5 mm Ti forks in their cheek slots) and S-shaped TPU side panels
(RV23/24) slide over the standoffs, 6 M3x8 CSK (4 standoff ends + 2 into captive thin nuts in the chassis wall).
Printed closed-top chassis (RV01) with an X-ribbed deck, 1 mm printed base panel on 5 M2 CSK into heat-sets, 0.9 mm
Ti top panel bonded on the deck. N10s in keyhole side-wall pockets drive the rear F1 tyres; O-rings drive the front
micro wheels on the 25 mm standoffs.
"""
# [fix-S] Thin shim: the generator lives in the `revron` package next to this file (params, common, tub, side, weapon,
# assembly, spec). This file re-exports every name so spec.json (`"file": "src/build_revron.py"`), the CLI and the tests
# keep working unchanged.
import os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
for _p in (ROOT, HERE):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import revron as _pkg
globals().update({k: v for k, v in _pkg.NAMESPACE.items() if k not in ("HERE", "ROOT")})


if __name__ == "__main__":
    main()
