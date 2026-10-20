import trimesh

from robot import geom, world
from robot.checks.drive_recess import recess_depth


def _mesh(head, drive=True):
    g = geom.geom_for(world.fastener_shape(3, 10, head=head), None, geom.FINE)
    return trimesh.Trimesh(g.mesh.vertices, g.mesh.faces) if hasattr(g, "mesh") else g


def test_every_head_style_has_a_recess():
    for head in (None, "countersunk", "button"):
        assert recess_depth(_mesh(head), [0, 0, 0], [0, 0, 1]) > 0.3, head


def test_plain_disc_head_has_none():
    m = trimesh.creation.cylinder(radius=3, height=2)
    m.apply_translation([0, 0, -1])
    assert recess_depth(m, [0, 0, 0], [0, 0, 1]) < 0.01
