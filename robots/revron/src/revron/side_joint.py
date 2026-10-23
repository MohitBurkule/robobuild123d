"""[fix-C-j1] Side panel in its own frame, with joints at its mating features, placed by connecting them.

Frame: origin on the SA datum, the boss face that seats on the 25 mm standoff's outboard end, on the standoff axis.
Joints (build123d RigidJoint, Z along the feature's axis):
  sa          the boss face on the standoff end; Z outboard, same sense as the standoff's `end` joint, so connecting the
              two puts the panel on the standoff axis with its boss face on the standoff end (coaxial + face mate)
  seat_a/b/c  each M3 CSK head seat (SIDE_BOLT_X out on the axis of the part it clamps: 25 mm standoff, 15 mm standoff,
              chassis nut); Z is the screw's insertion direction (inboard). The spec fasteners take at/dir from them.
  nut_relief  the inner face of the relief round the chassis nut lobe, on the nut axis; Z inboard toward the lobe
The panel is modelled once (SP_BUILT_SIDE, left); the right panel and its joints are its YZ mirror."""
import os, sys
import numpy as np
from .params import HERE, NUT, SA, SA_X, SA_X_STOCK, SPEC_DP, SP_BUILT_SIDE, SP_NUT_RELIEF_X, SP_RH_BLEND, SP_SEAT_AXIS
from .common import _b, _mirror_x, _solid
from .hubs import standoff, standoff_end
from .side import _side_body, bolt_x


def _mx(v):
    return (-v[0], *v[1:])


def _so_a_span(s, stock=False):
    """|X| span of the 25 mm standoff, signed by side; `stock`: at the stock chassis width (the frame the panel is drawn in)."""
    return tuple(sorted(s * x for x in (SA_X_STOCK if stock else SA_X)))


def _datum():
    """World point of the built panel's frame origin: its standoff's end on the SA axis."""
    return standoff_end(_so_a_span(SP_BUILT_SIDE, stock=True), SA)[0]


def sp_frames(s):
    """Joint frames {label: (point, z_dir)} in the panel frame of side s; the far side's are the mirror of the built one's."""
    sb, d = SP_BUILT_SIDE, _datum()
    inboard = (-sb, 0.0, 0.0)
    raw = {"sa": (d, standoff_end(_so_a_span(sb, stock=True), SA)[1]),
           **{f"seat_{k}": ((sb * bolt_x(k), *ax), inboard) for k, ax in SP_SEAT_AXIS.items()},
           "nut_relief": ((SP_NUT_RELIEF_X[1], *NUT), inboard)}
    loc = {k: (tuple(p - q for p, q in zip(pt, d)), z) for k, (pt, z) in raw.items()}
    return loc if s == sb else {k: (_mx(p), _mx(z)) for k, (p, z) in loc.items()}


def _rh_blend(body):
    """RV24's own blend: the quarter-round filling the nose slot's roof / wall corner (a sketched fillet: the kernel's edge fillet fails at the
    neighbouring bolt bore), built in the panel frame as the square r x r minus its inscribed circle, swept along the wall."""
    b = _b()
    r, d = SP_RH_BLEND["r"], _datum()
    x, z = SP_RH_BLEND["x"] + d[0], SP_RH_BLEND["z"] - d[2]       # wall and roof in the mirrored panel frame
    y0, y1 = SP_RH_BLEND["y"][0] - d[1], SP_RH_BLEND["y"][1] - d[1]
    sq = b.Solid.make_box(r, y1 - y0, r).moved(b.Location((x - r, y0, z - r)))
    cyl = b.Solid.make_cylinder(r, y1 - y0, b.Plane(origin=(x - r, y0, z - r), z_dir=(0, 1, 0)))
    return _solid(body + _solid(sq - cyl))


def side_panel_local(s, pin=True):
    """RV23/24 panel solid in its own frame, carrying its joints."""
    from OCP.BRepBuilderAPI import BRepBuilderAPI_Transform
    b = _b()
    to_frame = b.Location(tuple(-v for v in _datum())).wrapped.Transformation()
    body = b.Solid(BRepBuilderAPI_Transform(_solid(_side_body(pin)).wrapped, to_frame, True).Shape())   # geometry re-based, not just located
    if s != SP_BUILT_SIDE:
        body = _rh_blend(_solid(_mirror_x(body)))
    for k, (p, z) in sp_frames(s).items():
        b.RigidJoint(k, body, b.Location(b.Plane(origin=p, z_dir=z)))
    return body


def side_panel(s, pin=True):
    """The panel placed on its 25 mm standoff: standoff `end` joint -> panel `sa` joint."""
    so = standoff(_so_a_span(s), SA)
    panel = side_panel_local(s, pin)
    so.joints["end"].connect_to(panel.joints["sa"])
    return panel


def sp_spec(s, so_id):
    """Spec entries derived from the joints: the panel's features + mate to its standoff, the standoff's features, and
    the solved world frame of every panel joint (for the fasteners). Placement is solved by robot.cad.mates."""
    root = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
    if root not in sys.path:
        sys.path.insert(0, root)
    from robot.cad import mates
    fr = sp_frames(s)
    pe, ze = standoff_end(_so_a_span(s), SA)
    so_feat = {"end_face": {"point": list(pe), "normal": list(ze)}, "axis": {"point": list(pe), "axis": list(ze)}}
    (pa, za) = fr["sa"]
    feat = {"sa_face": {"point": list(pa), "normal": [-v for v in za]}, "sa_axis": {"point": list(pa), "axis": list(za)},
            **{k: {"point": list(p), "axis": list(z)} for k, (p, z) in fr.items() if k != "sa"}}
    mate = {"to": so_id, "constraints": [{"type": "coaxial", "a": "axis", "b": "sa_axis"},
                                          {"type": "face", "a": "end_face", "b": "sa_face"}]}
    eye = np.eye(len(pe) + 1)
    M = mates.solve(eye, eye, mate["constraints"], so_feat, feat)
    world = {k: ([round(float(v), SPEC_DP) for v in M[:-1, :-1] @ np.asarray(p) + M[:-1, -1]],
                 [round(float(v), SPEC_DP) + 0.0 for v in M[:-1, :-1] @ np.asarray(z)]) for k, (p, z) in fr.items()}
    return feat, mate, so_feat, world
