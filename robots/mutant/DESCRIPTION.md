# Mutant: what the reference photos show

Photos: `reference/mutant.aws72.webp` (blue version, front_right_iso per REFERENCE.json),
`mutant.aws74.webp` (blue version, rear-right iso per REFERENCE.json; the curved front plates and skirts are on the
viewer's left), `mutant.aws76.webp` (white/cream version, low front view from the robot's left-front corner).
Model frame: front +y (curved metal plates + skirts), right +x, up +z.

## Overall
- A **shuffler** (walker class): no round wheels. Two box pods side by side, separated by a narrow centre slot that
  holds a **thin vertical disc** with a hook tooth. Rotating lobed cam stacks (one per pod) poke out through windows
  in the top (and, since the robot is invertible, through the bottom) and shuffle the robot along.
- Proportions: overall plan about 1.3-1.4x as long as wide; pods about 45 % of the width each, slot about 6-8 mm;
  height about 0.35-0.4x the length; front skirts add about 20 % of the length ahead of the body.
- Colours (blue version): translucent blue PETG/PLA pods; silver/grey metal front plates; clear/white ribbed plastic
  skirts; white printed cams with green TPU tread pads; red 2-pin charge port; black slide switch; white "MUTANT"
  label on the right front plate. White version: cream pods, yellow cam pads, blue "MUTANT" lettering and "ON / OFF"
  printed on the top, red charge plug.

## Pods (body)
- Two near-identical rectangular boxes, flat top and flat sides, small black screw heads at the top corners and along
  the side panel edges. The rear lower edge is bevelled/rounded (aws76: a big chamfer on the rear bottom, aws72 a
  rounded rear-bottom corner) so the robot rocks over it.
- Each pod's outer side is a separate thin side panel screwed on (screws at the corners and one centre screw with a
  green insert), carrying one or two small blue triangular fins pointing down/back (low side fins near the bottom
  edge: stand-offs when the robot is on its side).
- Top: one rectangular window per pod, rear half, about 40 % of the pod width x 30 % of the pod length, the cam stack
  sticks up through it. Between the pods at the top: a raised triangular printed hump (disc guard) over the rear part of
  the disc, with a hole near its top (lock-pin hole). A small slot/window on the top ahead of the hump.
- Front of each pod: a curved grey metal plate (steel/titanium sheet, about 1 mm) wraps from the top front edge down
  and forward in a concave quarter-round to floor level, screwed at its top edge and sides; under it a clear/white
  ribbed flexible skirt (polycarbonate/PET film) lies on the floor and projects forward about 20-25 mm, full pod width.
  The two plates and skirts are separate per pod with the slot between them.

## Disc (weapon)
- Thin (about 2-3 mm) steel vertical disc on a lateral (x) axle in the centre slot, axle at about mid-height in the
  front half of the robot; diameter close to the body height (it fills the slot height), with one large hook
  tooth (aws72/aws74) that sweeps out of the front of the slot between the two metal plates.
- Driven by a small motor hidden in the pods (likely an outrunner beside the slot with a belt, or a hub motor in one
  pod wall).

## Shuffle drive (the interesting part)
- Per pod one lateral axle carrying a stack of 3 lobed cams (white printed discs about 25-30 mm across with 3-4
  rounded lobes, green TPU pads on the lobe tips), rear half of the pod, lobes staggered between the discs.
- As the axle turns, the lobes press on the floor one after another and lift/push the pod: a non-circular rotating
  "foot" (shuffler). The front rests on the skirts/plates. One gearmotor per pod (red motor visible behind the cams in
  aws72), differential steering like a 2WD robot.
- Invertible: the cams stick out of both top and bottom windows.

## Electronics / controls
- Red 2-pin charge port (JST-style, red housing) recessed in the top of the robot's right pod (aws72 near pod, aws74
  far-left pod top), close to the front half. It is the **charging port**, not a weapon.
- Black slide switch in a small top slot (aws72: on the left pod's top near the front-left; white version: centre
  front with "ON / OFF" printed beside it). A small black link/switch slot on the pod side in aws74.
- Battery, ESCs, receiver hidden inside the pods.
