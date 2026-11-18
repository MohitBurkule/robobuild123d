# Th'UNDER'er build notes
- Likeness: FAIL (silhouette IoU ~0.64/0.66, need 0.80). type/weapon/reference gates pass. Verify/fasteners NOT run (coordinator said focus on look only).
- Generator: flipped outline (wheels at +y) gave "no wireable layout" (esc.m2 -> motor route); only the wheels-at--y orientation builds. Small waist also fails layout.
- Generator emits a top bridge, wedge and a bar above the roof; hspin_bar with under-body hook needs hand edits (patch.py strips them, moves the bar below, adds pods and hub disc).
- Missing: intent keys for pods/centre disc/bar below the body, 4-wheel-free pods; likeness weapon width reads the default pose (joint default 90 needed to lay bar across x).
- Floating insert-like cylinders appear outside the hex in iso render (not diagnosed).
