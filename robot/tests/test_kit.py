from robot import kit


def test_kit_twin_pods_4wd_drum():
    s = kit.build({"body": {"style": "twin_pods", "slot": 30}, "weapon": {"kind": "drum", "radius": 20, "width": 24},
                   "wheels": {"n": 4, "radius": 14}, "forks": {"n": 2}})
    ids = [p["id"] for p in s["parts"]]
    assert {"pod_l", "pod_r", "bridge", "weapon"} <= set(ids)
    assert sum(p["kind"] == "wheel" for p in s["parts"]) == 4
    w = next(p for p in s["parts"] if p["id"] == "weapon")
    assert w["weapon"]["kind"] == "drum" and w["at"][2] - 20 >= -14


def test_kit_shape_extras_build():
    from robot import shapes
    for plan in ("trapezoid", "pentagon", "round_nose"):
        s = kit.build({"body": {"plan": plan}, "weapon": {"kind": "ring", "radius": 60, "width": 12, "thick": 4},
                       "wheels": {"n": 4, "tread": True, "y": [-30, 30]}, "walls": {"height": 25, "flare_deg": 5},
                       "shield": {"radius": 50, "angle": 120}, "forks": {"n": 2, "tilt_deg": 8}})
        for p in s["parts"]:
            assert shapes.to_solid(p["shape"], ".").volume > 1, (plan, p["id"])
    s = kit.build({"weapon": {"kind": "bar", "radius": 40, "width": 6, "curve": 8, "tilt_deg": 10}})
    assert shapes.to_solid(next(p for p in s["parts"] if p["id"] == "weapon")["shape"], ".").volume > 1


def test_kit_walker_and_pod_nose():
    from robot import shapes
    s = kit.build({"body": {"style": "twin_pods", "pod_nose": "round"}, "legs": {"n": 2}})
    assert s["locomotion"] == "walker" and not any(p["id"].startswith("wheel") for p in s["parts"])
    for p in s["parts"]:
        assert shapes.to_solid(p["shape"], ".").volume > 1, p["id"]
    assert kit.build({})["locomotion"] == "roller"
