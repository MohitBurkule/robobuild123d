"""SolidWorks dump parity (robot/checks/sldprt_dump.py, asm_dump.py): parsing and the bad / good geometry cases."""
import numpy as np
import pytest
import trimesh

from robot.checks import asm_dump, ref_features, sldprt_dump as sd

DUMP = """PART plate.SLDPRT
FEATURE 13 | Front Plane | RefPlane | id=2 | suppressed=False
  PLANE 1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,
FEATURE 17 | Sketch1 | ProfileFeature | id=26 | suppressed=False
  SKETCH_TO_MODEL 1,0,0,0,1,0,0,0,1,0,0,0,1,0,0,0,
  PT 0_2 (0,0,0)
  SEG 0_1 type=0 constr=False p0=(-0.01,-0.01,0) p1=(0.01,-0.01,0)
  CONTOUR 0 closed=True segs=0_1
FEATURE 18 | Boss-Extrude1 | Extrusion | id=48 | suppressed=False
  DIM D1@Boss-Extrude1@plate.Part = 0.004
  PARENT Sketch1 | ProfileFeature
  EXTRUDE end1=0 d1=0.004 both=False end2=0 d2=0 reverse=False draft1=0 thin=False merge=True
  FACE plane n=(0,0,1) o=(0,0,0.004) box=-0.01,-0.01,0.004,0.01,0.01,0.004, area=4E-04
  FEATURE -1 | Sketch1 | ProfileFeature | id=26 | suppressed=False
  SKETCH_TO_MODEL 9,9,9,9,9,9,9,9,9,9,9,9,1,0,0,0,
FEATURE 19 | Sketch2 | ProfileFeature | id=30 | suppressed=False
  SKETCH_TO_MODEL 1,0,0,0,1,0,0,0,1,0,0,0.004,1,0,0,0,
  SEG 0_1 type=1 constr=False c=(0.003,0.002,0) p0=(0.0045,0.002,0) p1=(0.0045,0.002,0) r=0.0015 dir=1
  CONTOUR 0 closed=True segs=0_1
FEATURE 20 | Cut-Extrude1 | ICE | id=60 | suppressed=False
  PARENT Sketch2 | ProfileFeature
  EXTRUDE end1=1 d1=0 both=False end2=0 d2=0 reverse=True draft1=0 thin=False merge=True
FEATURE 21 | Fillet1 | Fillet | id=70 | suppressed=False
  DIM D1@Fillet1@plate.Part = 0.001
  PARENT Boss-Extrude1 | Extrusion
  FILLET r=0.001 type=0 items=-1
  FACE cyl o=(0.009,0.009,0.002) ax=(0,0,1) r=0.001 box=0.009,0.009,0,0.01,0.01,0.004, area=6E-06
FEATURE 22 | Chamfer1 | Chamfer | id=80 | suppressed=True
  DIM D1@Chamfer1@plate.Part = 0.0005
"""


def test_parse_features_sketch_and_faces():
    d = sd.parse(DUMP)
    names = [f["name"] for f in d["features"]]
    assert names[:2] == ["Front Plane", "Sketch1"] and "Fillet1" in names
    ex = next(f for f in d["features"] if f["name"] == "Boss-Extrude1")
    assert ex["extrude"]["d1"] == 0.004 and ex["faces"][0]["type"] == "plane"
    assert "sketch" not in ex   # the nested sketch copy is skipped
    assert sd.radii(d) == {"fillet": [1.0], "chamfer": []}   # suppressed chamfer left out
    (c,) = sd.circles(d)
    assert c["kind"] == "cut" and c["d"] == 3.0 and c["end"] == "through_all"
    assert np.allclose(c["centre"], [3, 2, 4]) and np.allclose(c["normal"], [0, 0, 1])


def test_sketch_transform_rows_are_axis_images():
    # sketch X -> part Z, sketch Y -> part -X: p = x*row0 + y*row1 + t
    T = sd.sketch_xf([0, 0, 1, -1, 0, 0, 0, -1, 0, 0.001, 0, 0, 1, 0, 0, 0])
    assert np.allclose(T @ [1, 2, 0, 1], [0.001 - 2, 0, 1, 1])


def _plate(fillet=True, hole=True, thick=4.0):
    """20 x 20 x thick plate (Z 0..thick) with an r1 rounded corner at (+10, +10) and a d3 hole at (3, 2)."""
    from shapely.geometry import Point, box

    p = box(-10, -10, 10, 10)
    if fillet:
        p = p.difference(box(9, 9, 10, 10)).union(Point(9, 9).buffer(1.0, 64))
    if hole:
        p = p.difference(Point(3, 2).buffer(1.5, 64))
    return trimesh.creation.extrude_polygon(p, thick)


def _rows(model):
    d = sd.parse(DUMP)
    faces = [(f, fc) for f in d["features"] for fc in f.get("faces") or []]
    ref = _plate()
    return sd.compare(model, ref, sd.features_in_frame(d, faces, np.eye(4), sd.part_vertices(faces)))


def test_exact_reference_passes():
    rows = _rows(_plate())
    assert {r["kind"] for r in rows} == {"fillet", "hole", "extrude"}
    assert all(r["ok"] for r in rows), [r.get("msg") for r in rows]


def test_sharp_corner_fails_fillet():
    rows = _rows(_plate(fillet=False))
    f = [r for r in rows if r["kind"] == "fillet"]
    assert f and not f[0]["ok"], f
    assert all(r["ok"] for r in rows if r["kind"] != "fillet")


def test_missing_hole_fails():
    rows = _rows(_plate(hole=False))
    h = [r for r in rows if r["kind"] == "hole"]
    assert h and h[0]["ref_ok"] and not h[0]["ok"], h


def test_wrong_depth_fails_extrude():
    rows = _rows(_plate(thick=4.3))
    e = [r for r in rows if r["kind"] == "extrude"]
    assert e and not e[0]["ok"], e


def test_register_recovers_rotation_and_shift():
    d = sd.parse(DUMP)
    faces = [(f, fc) for f in d["features"] for fc in f.get("faces") or []]
    m = _plate()
    T = np.eye(4)
    T[:3, :3] = [[0, -1, 0], [0, 0, -1], [1, 0, 0]]
    T[:3, 3] = [1.0, 11.0, -2.0]
    ref = m.copy().apply_transform(T)
    pts = np.vstack([m.vertices, trimesh.sample.sample_surface(m, 400, seed=2)[0]])
    A, gap = sd.register(pts, ref, [T @ np.diag([1, 1, 1, 1.0])])
    assert gap < 0.01 and np.allclose(A, T, atol=1e-3)
    del faces


def test_snap_to_exact():
    assert sd.snap(1.3, [1.0, 2.0]) == 1.0
    assert sd.snap(3.4, [1.0, 2.0]) == 3.4


def test_exact_hole_size_tightens_section_compare():
    ref = _plate(fillet=False)
    from shapely.geometry import Point, box

    p = box(-10, -10, 10, 10).difference(Point(3, 2).buffer(1.4, 64))   # d2.8 vs exact d3.0
    model = trimesh.creation.extrude_polygon(p, 4.0)
    loose, _ = ref_features.compare_sections(model, ref)
    tight, _ = ref_features.compare_sections(model, ref, exact_d=[3.0])
    assert not [x for x in loose if x["kind"] == "hole_size"]
    assert [x for x in tight if x["kind"] == "hole_size"]


ASM = """ASM a.SLDASM
COMP Plate-1 | file=C:\\x\\Plate.SLDPRT | config=Default | suppressed=False | fixed=False
  XFORM 0,0,1,-1,0,0,0,-1,0,0,0.011,0,1,0,0,0,
  MASS com=(0,0,0.002) vol=1.6E-06 area=1E-03 mass=0.002
  MATERIAL ABS
COMP Pin-2 | file=C:\\x\\Pin.SLDPRT | config=Default | suppressed=False | fixed=False
  XFORM 1,0,0,0,1,0,0,0,1,0.003,0.002,0,1,0,0,0,
MATE Concentric1 | type=1 | align=0 | flip=False | suppressed=False
  ENT 0 comp=Plate-1 reftype=2 params=0.003,0.002,0,0,0,1,0.0015,0,
  ENT 1 comp=Pin-2 reftype=2 params=0.003,0.002,0,0,0,1,0.0015,0,
MATE Coincident9 | type=0 | align=0 | flip=False | suppressed=True
  ENT 0 comp=Plate-1 reftype=2 params=0,0,0,0,0,1,0,0,
  ENT 1 comp=Pin-2 reftype=2 params=0,0,0,0,0,1,0,0,
INTERFERENCES 1
  INT vol=2E-09 comps=Plate-1 ; Pin-2 ;
"""


def test_asm_parse():
    a = asm_dump.parse(ASM)
    T = a["comps"]["Plate-1"]["T"]
    assert np.allclose(T @ [1, 0, 0, 1], [0, 11, 1, 1]) and np.allclose(T[:3, 3], [0, 11, 0])
    assert a["comps"]["Plate-1"]["vol_mm3"] == pytest.approx(1600) and np.allclose(a["comps"]["Plate-1"]["com"], [0, 0, 2])
    assert [m["kind"] for m in a["mates"]] == ["concentric", "coincident"] and a["mates"][1]["suppressed"]
    assert a["ints"] == [{"vol_mm3": pytest.approx(2.0), "comps": ["Plate-1", "Pin-2"]}]
    assert asm_dump.base("Micro slx v1.0-1/RV19 Hub Micro-1") == "RV19 Hub Micro"


def test_pose_diff():
    A = np.eye(4)
    B = np.eye(4)
    B[:3, 3] = [0.05, 0, 0]
    c, s = np.cos(np.radians(0.4)), np.sin(np.radians(0.4))
    B[:2, :2] = [[c, -s], [s, c]]
    d, ang = asm_dump.pose_diff(A, B)
    assert d == pytest.approx(0.05) and ang == pytest.approx(0.4, abs=1e-6)
    assert d <= asm_dump.PLACE_MM and ang <= asm_dump.PLACE_DEG
    B[:3, 3] = [0.2, 0, 0]
    assert asm_dump.pose_diff(A, B)[0] > asm_dump.PLACE_MM


class _Ctx:
    def __init__(self, asm, pm, raw=None):
        self._asm_map = pm
        self.r = type("R", (), {"spec": type("S", (), {"raw": {"asm_dump": {"file": asm}, **(raw or {})}})()})()


def test_known_interference(tmp_path):
    f = tmp_path / "a.asmdump.txt"
    f.write_text(ASM)
    asm_dump.load.cache_clear()
    ctx = _Ctx(str(f), {"plate": ("Plate-1", None), "pin": ("Pin-2", None), "other": ("Other-1", None)})
    assert asm_dump.known_interference(ctx, "plate", "pin", 2.1)            # <= 1.1 x 2 mm3: known, cited
    assert "asmdump" in asm_dump.known_interference(ctx, "pin", "plate", 2.0)
    assert asm_dump.known_interference(ctx, "plate", "pin", 2.5) is None    # bigger than the original: ours
    assert asm_dump.known_interference(ctx, "plate", "other", 0.1) is None  # not in the original: ours
