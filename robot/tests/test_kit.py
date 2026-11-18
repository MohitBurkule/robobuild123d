from robot import kit


def test_kit_twin_pods_4wd_drum():
    s = kit.build({"body": {"style": "twin_pods", "slot": 30}, "weapon": {"kind": "drum", "radius": 20, "width": 24},
                   "wheels": {"n": 4, "radius": 14}, "forks": {"n": 2}})
    ids = [p["id"] for p in s["parts"]]
    assert {"pod_l", "pod_r", "bridge", "weapon"} <= set(ids)
    assert sum(p["kind"] == "wheel" for p in s["parts"]) == 4
    w = next(p for p in s["parts"] if p["id"] == "weapon")
    assert w["weapon"]["kind"] == "drum" and w["at"][2] - 20 >= -14
