# Recycler struggles
- Generator has no horizontal-drum hypothesis: used hspin_bar with a box outline, then hand-replaced the weapon by a cylinder (x axis), removed wedge/top_bridge, added arms and 5 ring bands (scripted in a throwaway mk.py).
- Box outline needs exactly y -44..40, z -9..14 to find a wireable layout; narrower sizes fail with no hint which constraint binds.
- REFERENCE.json says drum axis y but the photos and the likeness doc (x = across) say x; the weapon-axis check fails for a correct lateral drum. Not edited.
- Masks for aws65/aws66 (wood background) are unusable via `robot mask`; only aws67 used.
- Silhouette IoU 0.80 (display) but fails vs stock template threshold; photo has tall wheels at rear corners that the generator cannot place outside the body.
- Per coordinator instruction, verify/fasteners not run. Likeness: FAIL (2 blockers: weapon axis, silhouette).

## Round 2
- Rebuilt with `robot kit` (kit.json); weapon-axis check now passes. Silhouette IoU stuck ~0.78 (best camera is a rear view, mirrored). Remaining differences: no ring bands, no servo/top plate, rear wheels in photo sit higher and further back, drum end plates/shaft missing. Likeness FAIL (1 blocker: silhouette).
- Kit hint: no ring-band/extra detail part and the matcher choosing a rear camera for a front-facing photo is confusing.
