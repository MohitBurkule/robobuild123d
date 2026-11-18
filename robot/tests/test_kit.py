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


def test_kit_wishlist_round1():
    from robot import shapes
    for kind in ("flipper", "lifter", "axe", "hammer"):
        s = kit.build({"weapon": {"kind": kind}, "scoop": {"curve": 3}, "wheels": {"n": 4, "x": 50, "radius": [10, 14]},
                       "colors": {"body": "#ff0000"},
                       "extras": [{"id": "spine", "shape": {"type": "box", "size": [4, 60, 10]}, "at": [0, 0, 20]}]})
        ids = {p["id"]: p for p in s["parts"]}
        assert ids["weapon"]["weapon"]["kind"] == kind and ids["weapon"]["joint"]["axis"] == [1, 0, 0]
        assert ids["chassis"]["color"] == "#ff0000" and "spine" in ids and "scoop" in ids
        assert abs(ids["wheel_l0"]["at"][0] - 50) < 1e-9 and ids["wheel_l0"]["at"][2] == -4
        for p in s["parts"]:
            assert shapes.to_solid(p["shape"], ".").volume > 1, (kind, p["id"])
    assert kit.build({})["parts"][0]["color"] == "#3a3d44"


def test_kit_shared_parts():
    from robot import kitparts, shapes, spec as spec_mod, world as world_mod
    k = {"wheels": {"n": 0}, "use": [
        {"part": "drive_pod", "id": "drive", "at": [45, -20, 0], "mirror": "x"},
        {"part": "drive_pod", "id": "front", "at": [45, 25, 0], "mirror": "x", "omni": True},
        {"part": "electronics", "id": "elec", "at": [0, 0, -4]},
        {"part": "hinged_arm", "id": "flip", "at": [0, 10, 8], "length": 40}]}
    s = kit.build(k)
    ids = {p["id"]: p for p in s["parts"]}
    assert ids["drive_l_motor"]["catalog"] and ids["drive_r_wheel"]["at"][0] == -45
    assert ids["drive_l_motor"]["at"][0] < 45 and ids["drive_r_motor"]["at"][0] > -45  # motors inboard
    assert ids["flip"]["joint"]["pivot"] == [0.0, 10.0, 8.0]
    for p in s["parts"]:
        if p.get("shape"):
            assert shapes.to_solid(p["shape"], ".").volume > 1, p["id"]
    world_mod.resolve(spec_mod.Spec(s), fast=True)
    assert "drive_pod" in kitparts.describe()
