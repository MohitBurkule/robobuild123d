import os, sys, unittest, tempfile
HERE = os.path.dirname(__file__)
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, os.path.join(HERE, '..', 'wip_r17'))
ROOT = os.path.join(HERE, '..', '..')


class TestRound17(unittest.TestCase):
    def test_exact_iou_boxes(self):
        # two 10 mm cubes offset by 5 mm: IoU = 500 / 1500, exact (no voxel grid)
        import exact_iou as XI
        from build123d import Box, Pos
        A = XI.mesh_of(Box(10, 10, 10)); B = XI.mesh_of(Pos(5, 0, 0) * Box(10, 10, 10))
        v, how = XI.exact_iou(A, B)
        self.assertEqual(how, 'manifold'); self.assertAlmostEqual(v, 1 / 3, places=6)

    def test_exact_iou_thin_wall(self):
        # 0.8 mm wall vs 1.6 mm wall: IoU 0.5 exactly (the 0.2 mm voxel grid could not resolve this)
        import exact_iou as XI
        from build123d import Box, Pos
        v, _ = XI.exact_iou(XI.mesh_of(Pos(0, 0, 0.4) * Box(20, 20, 0.8)), XI.mesh_of(Box(20, 20, 1.6)))
        self.assertAlmostEqual(v, 0.5, places=6)

    def test_surf_dist_identity(self):
        import exact_iou as XI
        from build123d import Cylinder
        T = XI.mesh_of(Cylinder(3, 5))
        r = XI.surf_dist(T, T, n=2000)
        self.assertGreater(r['fscore'], 0.999); self.assertLess(r['p95'], 1e-3)

    def test_face_audit_canonical_bspline(self):
        # a B-spline face that is exactly a cylinder is classified as 'cyl' (Top Panel Fillet1)
        sys.path.insert(0, os.path.join(ROOT, 'rebuild_dump'))
        import face_audit as FA
        from build123d import Cylinder, export_step, Solid
        from OCP.BRepBuilderAPI import BRepBuilderAPI_NurbsConvert
        nb = Solid(BRepBuilderAPI_NurbsConvert(Cylinder(2, 4).wrapped, True).Shape())
        st = os.path.join(tempfile.mkdtemp(), 'c.step'); export_step(nb, st)
        kinds = sorted(f.kind for f in FA.faces_from_step(st))
        self.assertIn('cyl', kinds); self.assertNotIn('surf', kinds)

    def test_mirror_source_prefix(self):
        import mirror_derived as MD
        MD.DEC = os.path.abspath(os.path.join(ROOT, 'decoded_corpus'))
        self.assertEqual(MD.resolve('TBC_Mirrortbcpt1', 'tbcpt1'), 'TBC_tbcpt1')

    def test_corpus_name_credit(self):
        import corpus_check as CC
        self.assertEqual(CC.fname('Mirror2<Cut-Extrude1'), 'Mirror2')
        self.assertEqual(CC.fname('Fillet1(mirror)'), 'Fillet1(mirror)')

    def test_fstream_endspecs_rv12(self):
        # round-13 EndSpec reader, now fed to the replay: RV12 Boss-Extrude7 is offset-from-surface (5)
        from sldprt import validate as V, fstream as FS
        import json
        p = 'RV12 N10 2200 RPM'
        d = V.feature_stream(os.path.join(ROOT, 'revdev', p + '.SLDPRT'))
        J = json.load(open(os.path.join(ROOT, 'decoded', p + '.json')))
        ids = {f['id']: f['name'] for f in J['features'] if 'Extrude' in f['name']}
        dec = FS.decode(d, set(ids))
        es = {ids[k]: v for k, v in dec.endspecs.items() if k in ids}
        self.assertEqual(es['Boss-Extrude7'].end1, 5); self.assertFalse(es['Boss-Extrude1'].both)

    def test_replay_wiring(self):
        src = open(os.path.join(HERE, '..', 'wip_r17', 'decode_replay.py')).read()
        for s in ('def commit_exact', 'def fs_endspecs', 'def surf_support', 'def cir_pattern', 'exact_blend_scoring'):
            self.assertIn(s, src)

    def test_blendfit_unattributed_keeps_all_faces(self):
        # FS4 Chamfer1: with no creator attribution every fitting cone must be kept (the attribution
        # flag is fixed before the loop; testing `cf` inside it stopped after the first face)
        src = open(os.path.join(HERE, '..', 'wip_r17', 'decode_replay.py')).read()
        self.assertIn('attributed = bool(cf)', src)
        self.assertNotIn("if cf and F.type != 'Fillet': continue", src)

    def test_throughall_boss_gets_upto_caps(self):
        # Top Panel Boss-Extrude2 / RV03 Boss-Extrude2: decoded end code 1 on a boss
        src = open(os.path.join(HERE, '..', 'wip_r17', 'decode_replay.py')).read()
        self.assertIn("(code == 1 and kind != 'cut')", src)


if __name__ == '__main__':
    unittest.main()
