"""apply_user_picks.py : merge user angle picks + refreshed exports into viewer/data/robots.json.
Letter key (pick sheets, pick_body.py): A0 B60 C120 D180 E240 F300, el 35; same az convention as the viewer."""
import json, re, difflib, shutil, sys
from pathlib import Path

V = Path("/mnt/project-files/robot-cad/viewer")
B = Path("/tmp/claude-0/-home-user/a49462ed-bed0-54a5-8dcf-e0aab9a96f04/scratchpad/viewer_build")
PICKS = [Path("/mnt/project-files/robot-cad/refprs/user_angle_picks_1.txt"), Path("/mnt/project-files/robot-cad/refprs/user_angle_picks_2.txt")]
LET = {"A": 0, "B": 60, "C": 120, "D": 180, "E": 240, "F": 300}
FRONT = 90.0  # midpoint of the B/C pair = front-on

def norm(a): return a % 360
def toward(a, b, d):
    """move azimuth a by d degrees toward b along the shorter arc (not past b)"""
    diff = ((b - a + 180) % 360) - 180
    step = max(-abs(diff), min(abs(diff), d if diff >= 0 else -d)) if diff else 0
    return norm(a + step)
def mid(a, b): return norm(a + (((b - a + 180) % 360) - 180) / 2)

# hand-checked readings for lines the rules can't read cleanly: key -> (az, el, note or None, ambiguous?)
MANUAL = {
    "auger_the_top|auger_the_top.aws72": (120, 35, "C orientation; 'more like B' read as about the weapon arm, not the camera", True),
    "the_golden_nuggets|the_golden_nugget.aws67": (120, 35, "user unsure: C or opposite of C (300) depending on hinge", True),
    "queen_sarah_denning|queen_sarah_denning.aws70": (90, 90, "straight top view, front arrow pointing down on screen", True),
    "relativity|relativity.aws72": (40, 35, "'B slightly further away facing than B' read as B turned 20 away from front-on", True),
    "thwack_attack|thwack_attack.aws74": (40, 50, "'more away from us' read as B turned 20 away from front-on; slightly top", True),
    "antomic|antomic.aws67": (80, 35, "'closer to B but more front facing so between B and C' -> between, leaning B", True),
    "rammstein|rammstein.aws71": (100, 50, "'C but more between B and C' -> C shifted 20 toward B; slightly top", True),
    "recycler|recycler.aws67": (90, 20, None, False),
    "brisk|brisk.aws76": (60, 20, "'not as top view, slightly closer to earth' -> el 20", True),
    "alpha|alpha.aws72": (100, 50, "'more like C but more front facing' -> C shifted 20 toward front; slightly from top", False),
}
NOANGLE = {"gyronino|gyronino.aws72", "shoveron|shoveron.aws72"}

def parse(t):
    s = t.lower().replace("slighly", "slightly").replace("slghtly", "slightly").replace("cbut", "c but")
    lets = re.findall(r"(?<![a-z])([a-f])(?![a-z])", s)
    lets = [x.upper() for x in lets]
    if not lets: return None
    el = 35
    if re.search(r"camera (slightly )?(lower|near the ground|closer to earth)|lower to (the )?ground|near the ground", s): el = 20
    elif re.search(r"slightly (more )?top|slightly from top|slightly top", s): el = 50
    elif "top view" in s: el = 65
    m = re.search(r"between ([a-f]) and ([a-f])|([a-f]) and ([a-f]) between", s)
    if m:
        x, y = [g.upper() for g in m.groups() if g]
        az = mid(LET[x], LET[y])
    else:
        base = lets[0]; az = LET[base]
        m2 = re.search(r"more like ([a-f])\b", s)
        m3 = re.search(r"(towards?|tilted to|turned slightly to|turned slightly away towards) +([a-f])\b", s)
        if m2 and m2.group(1).upper() != base: az = toward(az, LET[m2.group(1).upper()], 30)
        elif m3 and m3.group(2).upper() != base: az = toward(az, LET[m3.group(2).upper()], 20)
    if re.search(r"facing us|front facing|facing front", s) and not m:
        az = toward(az, FRONT, 20)
    return round(az, 1), el

def main():
    rob = json.loads((V / "data/robots.json").read_text())
    # ---- refresh models from the re-export (out2) ----
    refreshed = []
    for r in rob["robots"]:
        mp = B / "out2/meta" / f"{r['slug']}.json"
        if not mp.exists(): continue
        m = json.loads(mp.read_text())
        if not m.get("model"): print("no model in re-export", r["slug"], m["errors"][:1]); continue
        shutil.copy(B / "out2/models" / f"{r['slug']}.glb", V / "data/models" / f"{r['slug']}.glb")
        r["model"], r["bbox"], r["parts"], r["errors"] = m["model"], m["bbox"], m["parts"], m["errors"]
        have = {p["name"] for p in r["photos"]}
        for p in m["photos"]:
            if p["name"] not in have:
                src = B / "out2/photos" / r["slug"] / f"{p['name']}.jpg"
                (V / "data/photos" / r["slug"]).mkdir(parents=True, exist_ok=True); shutil.copy(src, V / "data/photos" / r["slug"] / src.name)
                r["photos"].append({"name": p["name"], "src": f"photos/{r['slug']}/{p['name']}.jpg", "orig": p["file"], "w": p["w"], "h": p["h"], "default": p["default"]})
                print("new photo", r["slug"], p["name"])
        refreshed.append(r["slug"])
    # ---- user picks ----
    bys = {r["slug"]: r for r in rob["robots"]}
    remarks = []; amb = []; unmatched = []; applied = 0; noted = 0
    for f in PICKS:
        for line in f.read_text().splitlines():
            if not line.strip() or "|" not in line or ":" not in line: continue
            head, text = line.split(":", 1); text = " ".join(text.split())
            slug, ph = head.split("|", 1); ph = ph.strip()
            r = bys.get(slug.strip())
            if not r: unmatched.append(line); continue
            names = [p["name"] for p in r["photos"]]
            k = re.sub(r"\.(jpg|webp|png)$", "", ph)
            if k not in names:
                aws = re.findall(r"aws\.?\d+", k); cand = [n for n in names if aws and n.endswith(aws[-1])]
                if len(cand) != 1: cand = difflib.get_close_matches(k, names, 1, 0.3)
                if not cand: unmatched.append(line); continue
                k = cand[0]
            p = r["photos"][names.index(k)]
            key = f"{slug}|{ph}"
            prev = p.get("previous_guess") or dict(p["default"])
            p["previous_guess"] = prev; p["user_text"] = text
            note = None
            if key in NOANGLE or (key not in MANUAL and parse(text) is None):
                p["user_note"] = "user: " + text; noted += 1; got = None
            else:
                if key in MANUAL:
                    az, el, note, a = MANUAL[key]
                    if a: amb.append(f"{slug}/{k}: '{text}' -> az {az} el {el} ({note})")
                else:
                    az, el = parse(text)
                p["default"] = {"azimuth_deg": float(az), "elevation_deg": float(el), "roll_deg": 0.0, "source": "user pick: " + text + (f" [read as: {note}]" if note else "")}
                p["user_pick"] = {"azimuth_deg": float(az), "elevation_deg": float(el), "text": text, "parse_note": note}
                applied += 1
            remarks.append({"id": "u-" + re.sub(r"[^a-z0-9]+", "-", f"{slug}-{k}".lower()), "slug": slug, "kind": "photo", "photo": k, "part": None,
                            "tag": "user-remark", "text": "user: " + text, "created_at": "2026-11-18T00:00:00Z", "preloaded": True})
    rob["user_remarks"] = remarks
    (V / "data/robots.json").write_text(json.dumps(rob, separators=(",", ":")))
    tot = sum(len(r["photos"]) for r in rob["robots"]); with_pick = sum(1 for r in rob["robots"] for p in r["photos"] if "user_pick" in p)
    with_text = sum(1 for r in rob["robots"] for p in r["photos"] if "user_text" in p)
    print(f"refreshed models: {len(refreshed)}; photos {tot}; default=user pick {with_pick}; note only {noted}; no user line {tot - with_text}")
    print("unmatched:", unmatched); print("ambiguous:"); [print("  ", a) for a in amb]
    if "-v" in sys.argv:
        for r in rob["robots"]:
            for p in r["photos"]:
                if "user_text" in p: print(f"{r['slug']:32s} {p['name'][-12:]:12s} {p['previous_guess']['azimuth_deg']:5.0f},{p['previous_guess']['elevation_deg']:3.0f} -> {p['default']['azimuth_deg']:5.0f},{p['default']['elevation_deg']:3.0f}  {p['user_text'][:60]}")

main()
