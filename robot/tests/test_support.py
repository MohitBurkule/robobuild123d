"""support.loose: unfastened parts must be captured in all six directions (robot inverted / shaken)."""

from robot import spec, world
from robot.checks import Ctx, Options, support


def _ctx(parts, **extra):
    r = world.resolve(spec.Spec({"name": "t", "parts": parts, **extra}), fast=True)
    return Ctx(r, world.World.start(r), Options(fast=True))


def box(id, at, size=(10, 10, 10), kind="structure", **kw):
    return {"id": id, "kind": kind, "shape": {"type": "box", "size": list(size)}, "at": list(at), "material": "pla", **kw}


WALLS = [box("floor", (0, 0, -6), (30, 30, 2)), box("w1", (-8, 0, 0), (2, 30, 10)), box("w2", (8, 0, 0), (2, 30, 10)),
         box("w3", (0, -8, 0), (30, 2, 10)), box("w4", (0, 8, 0), (30, 2, 10)), box("lid", (0, 0, 6), (30, 30, 2))]
ESC = box("esc", (0, 0, 0), (14, 14, 10), kind="esc")


def loose(fs):
    return [f for f in fs if f.id == "support.loose" and not f.passed]


def test_floating_part_is_blocker():
    f = loose(support.run(_ctx(WALLS[:1] + [box("esc", (0, 0, 20), kind="esc")])))
    assert f and f[0].severity == "blocker" and "esc" in f[0].parts and "-z" in f[0].message and "+x" in f[0].message


def test_seated_captured_part_passes():
    fs = support.run(_ctx(WALLS + [ESC]))
    assert not loose(fs) and any(f.id == "support.loose" and f.passed for f in fs)


def test_inverted_resting_part_fails_only_upward():
    # rests on the floor inside walls, no lid: fine under gravity, falls out when inverted (+z)
    f = loose(support.run(_ctx(WALLS[:-1] + [ESC])))
    assert f and "+z" in f[0].message and "-z" not in f[0].message


def test_declared_hold_is_exempt():
    esc = box("esc", (0, 0, 0), (14, 14, 10), kind="esc", retained="strap")
    assert not loose(support.run(_ctx(WALLS[:-1] + [esc])))


def test_loose_ok_covers_support_loose_same_axis():
    # one physical fact, one waiver: retention.loose's `loose_ok` also clears support.loose on that axis (round 52 motor_l/r)
    walls = WALLS[:2] + [box("w2", (10, 0, 0), (2, 30, 10))] + WALLS[3:]
    why = "RVRN STEP: RV12 N10 slides 2.0 mm inboard in RV01 before it touches"
    mot = lambda wv: box("mot", (0, 0, 0), (14, 14, 10), kind="motor", **({"loose_ok": wv} if wv else {}))
    f = loose(support.run(_ctx(walls + [mot(None)])))
    assert f and "+x" in f[0].message
    fs = support.run(_ctx(walls + [mot({"axis": "+x", "max_mm": 2.2, "reason": why})]))
    assert not loose(fs) and any(x.id == "support.loose_waived" for x in fs)
    for wv, msg in (({"axis": "+x", "max_mm": 1.5, "reason": why}, "still free"),   # re-tested at max_mm: must hit
                    ({"axis": "-x", "max_mm": 2.2, "reason": why}, "stale")):        # another axis covers nothing
        f = loose(support.run(_ctx(walls + [mot(wv)])))
        assert f and "+x" in f[0].message and msg in f[0].message, f[0].message if f else None
