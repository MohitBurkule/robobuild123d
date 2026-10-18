"""Measurements for the combat ground-game rules (not a check group itself; used by `combat`).

`facts(ctx)` measures the robot once into a flat dict; every value is None when it could not be measured, so the rules
can fail closed. Conventions as in `_physics`: world mm, +Y front, +Z up, +X is the robot's left side (the specs name
`wheel_l` at +X), the floor is `_physics.floor_z`.

Perimeter profile: the surface of every solid is sampled and binned by its bearing around the robot centre (1 degree
bins, 0 deg = +X, 90 deg = front). In each bin the outermost radius is the outline; the "edge gap" is the height above the
floor of the lowest non-wheel point within `BAND_MM` of that outline - what an opponent's wedge meets when it arrives
from that bearing. Wheels are excluded from the gap (a tyre at the edge is something to drive up, not a skirt) and
reported separately as "wheel at the edge".
"""

from __future__ import annotations

import math

import numpy as np

from .. import catalog
from . import _physics as ph
from .power import spin_axis

BAND_MM = 6.0  # depth of the perimeter band behind the outline
WHEELISH = ("wheel", "tyre")
SKIRTISH = ("wedge", "fork")
SPINNING = ("weapon",)
GRIP = {"tpu", "tpu_95a", "tpu_85a", "silicone", "rubber", "lego_tyre", "urethane", "polyurethane", "neoprene"}
MU = {"silicone": 1.1, "urethane": 1.0, "polyurethane": 1.0, "rubber": 0.9, "lego_tyre": 0.9, "neoprene": 0.9,
      "tpu": 0.8, "tpu_95a": 0.8, "tpu_85a": 0.9}
MU_HARD = 0.35  # printed hard plastic or metal on a steel/polycarbonate floor
TEST_LOAD_N = 50.0  # a pushing opponent leaning on a skirt or fork tip

FAMILIES = {
    "wedge": "wedge", "wedge_2wd": "wedge", "rammer": "wedge", "pusher": "wedge",
    "vertical_spinner": "vspin", "vertical_spinner_forks": "vspin", "drum": "vspin", "beater": "vspin",
    "horizontal_spinner": "hspin", "undercutter": "hspin", "shell_spinner": "hspin", "ring_spinner": "hspin",
    "lifter": "lifter", "flipper": "lifter", "grabber": "lifter", "crusher": "lifter",
}


def family(spec):
    name = spec.raw.get("archetype") or spec.robot_type or "other"
    return FAMILIES.get(name, "other"), name


def _is_skirt(ctx, b):
    p = ph.part(ctx, b)
    return b.kind in SKIRTISH or (p is not None and ("skirt" in b.id or bool(p._extra.get("skirt"))))


def _sectors(F):
    """Bin masks for front, rear, left (+X), right (-X) and the four corners, from the outline's own corner bearings."""
    ex, ey = F["half_x"], F["half_y"]
    a = math.degrees(math.atan2(ey, ex))  # bearing of the front-left corner
    deg = np.arange(360) + 0.5
    def arc(lo, hi):
        lo, hi = lo % 360, hi % 360
        return (deg >= lo) & (deg < hi) if lo < hi else (deg >= lo) | (deg < hi)
    c = 10.0
    S = {
        "front": arc(a + c, 180 - a - c), "rear": arc(180 + a + c, 360 - a - c),
        "left": arc(-a + c, a - c), "right": arc(180 - a + c, 180 + a - c),
        "corner_fl": arc(a - c, a + c), "corner_fr": arc(180 - a - c, 180 - a + c),
        "corner_rr": arc(180 + a - c, 180 + a + c), "corner_rl": arc(360 - a - c, 360 - a + c),
    }
    S["corners"] = S["corner_fl"] | S["corner_fr"] | S["corner_rr"] | S["corner_rl"]
    S["all"] = np.ones(360, bool)
    return S


def profile(P, kinds, floor, centre):
    """Per-degree outline radius, edge gap (non-wheel) and whether a wheel reaches the outline."""
    q = P[:, :2] - centre
    ang = (np.degrees(np.arctan2(q[:, 1], q[:, 0])) % 360).astype(int) % 360
    r = np.hypot(q[:, 0], q[:, 1])
    rout = np.full(360, np.nan)
    np.fmax.at(rout, ang, r)
    band = r >= rout[ang] - BAND_MM
    wheel = np.isin(kinds, WHEELISH)
    gap = np.full(360, np.inf)
    sel = band & ~wheel
    np.fmin.at(gap, ang[sel], P[sel, 2] - floor)
    wedge_edge = np.zeros(360, bool)
    selw = wheel & (r >= rout[ang] - 1.0)
    wedge_edge[np.unique(ang[selw])] = True
    gap[np.isinf(gap)] = 99.0  # only wheel at this bearing: nothing keeps a wedge out
    gap[~np.isfinite(rout)] = np.nan
    return rout, gap, wedge_edge


def _pct(v, m, q):
    x = v[m]
    x = x[np.isfinite(x)]
    return float(np.percentile(x, q)) if len(x) else None


def _cover(gap, m, t):
    x = gap[m]
    x = x[~np.isnan(x)]
    return float(np.mean(x <= t)) if len(x) else None


def _longest_run(flags):
    """Longest run of True in a circular boolean array (bins)."""
    if flags.all():
        return len(flags)
    f = np.concatenate([flags, flags])
    best = cur = 0
    for v in f:
        cur = cur + 1 if v else 0
        best = max(best, cur)
    return min(best, len(flags))


def _slice_thickness(pts, y, x_bins, axis=1):
    """Median vertical extent of points in a 1 mm slice at coordinate `y` along `axis`, per 2 mm bin across."""
    m = np.abs(pts[:, axis] - y) <= 0.5
    if m.sum() < 3:
        return None
    s = pts[m]
    other = 0 if axis == 1 else 1
    idx = np.floor(s[:, other] / 2.0).astype(int)
    v = []
    for k in np.unique(idx):
        z = s[idx == k, 2]
        if len(z) >= 2:
            v.append(float(z.max() - z.min()))
    return float(np.median(v)) if v else None


def facts(ctx):
    w, r = ctx.world, ctx.r
    spec = r.spec
    F = {}
    F["family"], F["archetype"] = family(spec)
    solid = [b for b in ph.solids(w) if not b.fastener]
    if not solid:
        return F
    floor = ph.floor_z(ctx)
    F["floor"] = floor
    wheels = [b for b in solid if b.kind == "wheel"]
    tyres = [b for b in solid if b.kind == "tyre"]
    skirts = [b for b in solid if _is_skirt(ctx, b)]
    weapons = [b for b in solid if b.kind in SPINNING]
    rotor_ids = {b.id for b in weapons}
    for b in solid:  # parts riding on a weapon (hub, bell) spin with it
        p = ph.part(ctx, b)
        if p is not None and p.parent in rotor_ids:
            rotor_ids.add(b.id)
    body = [b for b in solid if b.kind not in WHEELISH and b.id not in rotor_ids]
    structure = [b for b in body if not _is_skirt(ctx, b)]
    F["n_wheels"], F["n_skirts"], F["n_weapons"] = len(wheels), len(skirts), len(weapons)

    pts, kinds, owner = [], [], []
    for b in solid:
        p, _ = b.surface(1.0)
        pts.append(p)
        kinds.append(np.full(len(p), "wheel" if b.kind in WHEELISH else ("rotor" if b.id in rotor_ids else b.kind), dtype=object))
        owner.append(np.full(len(p), b.id, dtype=object))
    P = np.vstack(pts)
    K = np.concatenate(kinds)
    lo, hi = P.min(axis=0), P.max(axis=0)
    centre = (lo[:2] + hi[:2]) / 2
    F["centre"] = centre
    F["half_x"], F["half_y"] = float((hi[0] - lo[0]) / 2), float((hi[1] - lo[1]) / 2)
    rout, gap, wedge_edge = profile(P, K, floor, centre)
    F["rout"], F["gap"], F["wheel_edge"] = rout, gap, wedge_edge
    S = _sectors(F)
    F["sectors"] = S
    for s in ("front", "rear", "left", "right", "corners", "all"):
        F[f"gap_med.{s}"] = _pct(gap, S[s], 50)
        F[f"gap_p20.{s}"] = _pct(gap, S[s], 20)
        F[f"gap_max.{s}"] = _pct(gap, S[s], 100)
        for t in (1.0, 1.5, 2.0, 3.0, 5.0):
            F[f"cover_{t:g}.{s}"] = _cover(gap, S[s], t)
        F[f"wheel_edge.{s}"] = float(wedge_edge[S[s]].mean()) if S[s].any() else None
    for c in ("corner_fl", "corner_fr", "corner_rr", "corner_rl"):
        F[f"gap_max.{c}"] = _pct(gap, S[c], 100)
    open5 = np.nan_to_num(gap, nan=99.0) > 5.0
    F["open_arc_deg"] = float(_longest_run(open5))
    # Front edge in mm: the widest stretch of the front bins with no skirt within 1.5 mm of the floor.
    fb = np.nonzero(S["front"])[0]
    if len(fb):
        g = np.nan_to_num(gap[fb], nan=99.0) > 1.5
        run, best, start = 0, (0, None), None
        for k, v in enumerate(g):
            if v:
                run += 1
                if run == 1:
                    start = k
                if run > best[0]:
                    best = (run, (start, k))
            else:
                run = 0
        if best[1] is None:
            F["front_open_mm"] = 0.0
        else:
            a0, a1 = math.radians(fb[best[1][0]]), math.radians(fb[best[1][1]] + 1)
            rr = np.nanmean(rout[fb[best[1][0]]:fb[best[1][1]] + 1])
            F["front_open_mm"] = float(abs(rr * math.cos(a0) - rr * math.cos(a1)))
        F["front_gap_spread"] = float(np.nanmax(gap[fb]) - np.nanmin(gap[fb])) if np.isfinite(gap[fb]).any() else None

    # Body extents without wheels and spinning parts.
    def ext(bs):
        if not bs:
            return None
        return np.array([np.min([b.aabb[0] for b in bs], axis=0), np.max([b.aabb[1] for b in bs], axis=0)])
    eb, es = ext(body), ext(structure)
    F["body_front_y"] = float(eb[1][1]) if eb is not None else None
    F["struct_front_y"] = float(es[1][1]) if es is not None else None
    F["body_height"] = float(eb[1][2] - floor) if eb is not None else None
    F["body_width"] = float(eb[1][0] - eb[0][0]) if eb is not None else None
    F["body_max_x"] = float(eb[1][0]) if eb is not None else None
    F["body_min_x"] = float(eb[0][0]) if eb is not None else None
    F["body_rear_y"] = float(eb[0][1]) if eb is not None else None

    # Lowest points.
    belly = [b for b in structure if b.kind not in ("insert", "nut", "bearing", "pin", "shaft", "belt", "pulley")]
    if belly:
        F["belly_gap"] = float(min(b.aabb[0][2] for b in belly) - floor)
        # Interior underside: belly points not in the perimeter band.
        q = P[:, :2] - centre
        ang = (np.degrees(np.arctan2(q[:, 1], q[:, 0])) % 360).astype(int) % 360
        rr = np.hypot(q[:, 0], q[:, 1])
        inner = rr < rout[ang] - BAND_MM - 4.0
        bid = {b.id for b in belly}
        O = np.concatenate(owner)
        m = inner & np.isin(O, list(bid))
        F["interior_gap"] = float(P[m, 2].min() - floor) if m.any() else None
        down = []
        for b in belly:
            fn, fa, fc = b.mesh.face_normals, b.mesh.area_faces, b.mesh.triangles_center
            sel = (fn[:, 2] < -0.95) & (fc[:, 2] <= floor + 0.5)
            down.append(float(fa[sel].sum()))
        F["drag_area_mm2"] = float(sum(down))
    nonwheel_low = [(b.id, float(b.aabb[0][2] - floor)) for b in body]
    F["touching"] = [i for i, g in nonwheel_low if g < 0.1]
    F["fastener_gap"] = None
    fz = [b for b in ph.solids(w) if b.fastener]
    if fz:
        F["fastener_gap"] = float(min(b.aabb[0][2] for b in fz) - floor)
        F["fastener_low_id"] = min(fz, key=lambda b: b.aabb[0][2]).id
    else:
        F["fastener_gap"] = 99.0

    # Wheels.
    if wheels:
        lows = [b.mesh.vertices[b.mesh.vertices[:, 2] <= b.aabb[0][2] + 0.5] for b in wheels]
        F["wheel_low_spread"] = float(max(b.aabb[0][2] for b in wheels) - min(b.aabb[0][2] for b in wheels))
        cx = [float(v[:, 0].mean()) for v in lows]
        cy = [float(v[:, 1].mean()) for v in lows]
        F["track"] = float(max(cx) - min(cx))
        F["wheel_y"] = cy
        F["wheel_x"] = cx
        F["wheelbase_wheels"] = float(max(cy) - min(cy))
        F["wheel_dia"] = float(min(b.aabb[1][2] - b.aabb[0][2] for b in wheels))
        F["wheel_width"] = float(min(min(b.aabb[1][0] - b.aabb[0][0], b.aabb[1][1] - b.aabb[0][1]) for b in wheels))
        F["wheel_front_y"] = float(max(b.aabb[1][1] for b in wheels))
        F["wheel_max_x"] = float(max(b.aabb[1][0] for b in wheels))
        F["wheel_min_x"] = float(min(b.aabb[0][0] for b in wheels))
        F["wheel_top"] = float(min(b.aabb[1][2] for b in wheels))
        mats = []
        for b in wheels:
            t = [tb for tb in tyres if (ph.part(ctx, tb) and ph.part(ctx, tb).tyre_of == b.id)]
            m = ph.material_of(ctx, t[0]) if t else ph.material_of(ctx, b)
            if m is None and ph.part(ctx, b) is not None and ph.part(ctx, b).catalog:
                m = "silicone"  # catalog wheels come with silicone tyres
            mats.append(m)
        F["tyre_mats"] = mats
        known = [m for m in mats if m is not None]
        F["mu"] = min(MU.get(m, MU_HARD) for m in known) if len(known) == len(mats) else None
        F["driven_sides"] = len({1 if x > F["centre"][0] else -1 for x in cx})

    # Skirt / wedge geometry: front-facing skirts are those reaching within 15 mm of the body front.
    F["skirts"] = []
    front = F["body_front_y"]
    for b in skirts:
        p = ph.part(ctx, b)
        v = b.mesh.vertices
        sp, _ = b.surface(0.5)
        ymax = float(v[:, 1].max())
        d = {"id": b.id, "kind": b.kind, "front": front is not None and ymax >= front - 15.0, "ymax": ymax,
             "gap": float(v[:, 2].min() - floor), "material": p.material if p else None,
             "x0": float(v[:, 0].min()), "x1": float(v[:, 0].max()), "hinged": bool(p and p.joint is not None),
             "joint": p.joint if p else None}
        tip = sp[sp[:, 1] >= ymax - 3.0]
        heel = sp[(sp[:, 1] < ymax - 3.0) & (sp[:, 1] >= ymax - 13.0)]
        d["tip_low"] = float(tip[:, 2].min() - floor) if len(tip) else None
        d["heel_low"] = float(heel[:, 2].min() - floor) if len(heel) else None
        d["tip_spread"] = None
        if len(tip):
            idx = np.floor(tip[:, 0] / 2.0).astype(int)
            lows_ = [float(tip[idx == k, 2].min()) for k in np.unique(idx)]
            d["tip_spread"] = float(max(lows_) - min(lows_))
        d["t1"] = _slice_thickness(sp, ymax - 1.0, None)
        d["t3"] = _slice_thickness(sp, ymax - 3.0, None)
        sp_all, sn = b.surface(0.5)
        up = (sn[:, 2] > 0.1) & (sn[:, 1] > 0.02)
        ramp = up & (sp_all[:, 2] <= floor + 0.7 * max(float(v[:, 2].max()) - floor, 1.0))
        d["ramp_deg"] = float(np.degrees(np.median(np.arctan2(sn[ramp, 1], sn[ramp, 2])))) if ramp.any() else None
        entry = up & (sp_all[:, 1] >= ymax - 10.0)
        d["entry_deg"] = float(np.degrees(np.median(np.arctan2(sn[entry, 1], sn[entry, 2])))) if entry.any() else None
        fn, fc = b.mesh.face_normals, b.mesh.triangles_center
        blunt = (fn[:, 1] > 0.85) & (fc[:, 2] <= floor + 4.0) & (fc[:, 1] >= ymax - 2.0)
        d["blunt_h"] = float(np.ptp(b.mesh.triangles[blunt][:, :, 2])) if blunt.any() else 0.0
        # Unsupported overhang: how far the tip reaches past the nearest point that touches structure.
        L = None
        if structure:
            samp = sp[:: max(len(sp) // 400, 1)]
            near = np.zeros(len(samp), bool)
            for sb in structure:
                if sb.kind in ("insert", "nut"):
                    continue
                lo_, hi_ = sb.aabb
                m = np.all((samp >= lo_ - 1.0) & (samp <= hi_ + 1.0), axis=1)
                if m.any():
                    near[np.nonzero(m)[0][sb.distance(samp[m]) <= 1.0]] = True
            if near.any():
                L = max(ymax - float(samp[near, 1].max()), 0.0)
            else:
                L = None
        d["overhang"] = L
        d["width"] = d["x1"] - d["x0"]
        mech = catalog.mech(d["material"])
        d["E"] = mech[2] * 1000.0 if mech else None
        if L is not None and L > 0.5:
            t = _slice_thickness(sp, ymax - L * 2.0 / 3.0, None)
            d["t_mid"] = t
            if t and d["E"]:
                I = d["width"] * t ** 3 / 12.0
                d["deflection"] = TEST_LOAD_N * L ** 3 / (3.0 * d["E"] * I)
            else:
                d["deflection"] = None
        else:
            d["t_mid"], d["deflection"] = None, (0.0 if L is not None else None)
        d["fasteners"] = sum(1 for f in spec.fasteners if b.id in (f.through or []) or f.threads_into == b.id)
        if wheels:
            d["wheel_gap"] = float(min(_aabb_gap(b.aabb, wb.aabb) for wb in wheels))
        F["skirts"].append(d)
    fs = [d for d in F["skirts"] if d["front"]]
    F["front_skirts"] = fs
    if fs:
        F["skirt_width"] = float(max(d["x1"] for d in fs) - min(d["x0"] for d in fs))
        F["skirt_front_y"] = max(d["ymax"] for d in fs)
    forks = [d for d in fs if d["kind"] == "fork" or ("fork" in d["id"] or "blade" in d["id"] or "tine" in d["id"])]
    F["forks"] = forks
    if len(forks) >= 2:
        F["fork_tip_spread"] = float(max(d["tip_low"] or 0 for d in forks) - min(d["tip_low"] or 0 for d in forks))
        # Gaps between tines at the lip not closed by anything within 3 mm of the floor.
        x0, x1 = min(d["x0"] for d in forks), max(d["x1"] for d in forks)
        ytip = min(d["ymax"] for d in forks)
        m = P[:, 1] >= ytip - 15.0
        m &= ~np.isin(K, WHEELISH)
        xs = np.arange(math.floor(x0), math.ceil(x1))
        low = np.full(len(xs), np.inf)
        idx = np.floor(P[m, 0]).astype(int) - int(xs[0]) if len(xs) else None
        if len(xs):
            ok = (idx >= 0) & (idx < len(xs))
            np.fmin.at(low, idx[ok], P[m][ok, 2] - floor)
            F["fork_open_mm"] = float(_longest_run_linear(low > 3.0))
    # Spinning weapon sweep.
    F["weapon"] = []
    for b in weapons:
        i = w.index(b.id)
        sa = spin_axis(w, r, i)
        p = ph.part(ctx, b)
        if sa is None:
            F["weapon"].append({"id": b.id, "axis": None})
            continue
        o, a = sa
        q = b.mesh.vertices - o
        R = float(np.linalg.norm(q - np.outer(q @ a, a), axis=1).max())
        reach = R * math.sqrt(max(1.0 - a[2] ** 2, 0.0))
        low = float(min(o[2] - reach, b.aabb[0][2]))
        high = float(max(o[2] + reach, b.aabb[1][2]))
        F["weapon"].append({"id": b.id, "axis": a, "vertical": abs(a[2]) < 0.5, "gap": low - floor, "high": high,
                            "R": R, "front": float(o[1] + R * math.sqrt(max(1 - a[1] ** 2, 0.0))),
                            "x0": float(b.aabb[0][0]), "x1": float(b.aabb[1][0]), "kind": p.weapon.kind if p and p.weapon else None})
    # Inverted: flip about the wheel tops.
    if wheels:
        top_floor = float(max(b.aabb[1][2] for b in wheels))
        Pi = P.copy()
        Pi[:, 2] = 2 * floor - Pi[:, 2]  # mirror so the old top faces down
        fi = 2 * floor - top_floor
        _, gi, _ = profile(Pi, K, fi, centre)
        F["inv_gap"] = gi
        F["inv_cover_3.front"] = _cover(gi, S["front"], 3.0)
        F["inv_min_gap"] = float(np.nanmin(gi)) if np.isfinite(gi).any() else None
        F["inv_shortfall"] = float(max(float(np.max([bb.aabb[1][2] for bb in body])) - top_floor, 0.0)) if body else None
        F["inv_weapon_gap"] = [top_floor - d["high"] for d in F["weapon"] if d.get("axis") is not None]
    # Mass, centre of mass and drive.
    F["mass_g"] = ctx.metrics.get("mass_total_g")
    if "com_x" in ctx.metrics:
        F["com"] = np.array([ctx.metrics["com_x"], ctx.metrics["com_y"], ctx.metrics["com_z"]])
        F["cog_h"] = float(F["com"][2] - floor)
    else:
        F["com"] = None
    if wheels and F["com"] is not None:
        wy = float(np.mean(F["wheel_y"]))
        cy = float(F["com"][1])
        share = 1.0
        if not (min(F["wheel_y"]) - 1 <= cy <= max(F["wheel_y"]) + 1):
            others = [d for d in F["skirts"] if d["gap"] <= 2.0]
            side = [d for d in others if (d["ymax"] - wy) * (cy - wy) > 0]
            oth = [b for b in body if b.aabb[0][2] - floor <= 2.0 and not _is_skirt(ctx, b)]
            ys = [d["ymax"] - 2.0 for d in side] + [float(b.center[1]) for b in oth if (b.center[1] - wy) * (cy - wy) > 0]
            if ys:
                oy = float(np.mean(ys))
                share = min(max(1.0 - (cy - wy) / (oy - wy), 0.0), 1.0) if abs(oy - wy) > 1 else 1.0
            else:
                share = None  # nothing else holds it up: it tips (ground.stance reports that)
        F["driven_share"] = share
        ext_y = [*F["wheel_y"], *[d["ymax"] - 2.0 for d in F["skirts"] if d["gap"] <= 2.0]]
        F["wheelbase"] = float(max(ext_y) - min(ext_y)) if len(ext_y) >= 2 else None
        F["com_long_margin"] = float(min(cy - min(ext_y), max(ext_y) - cy)) if F["wheelbase"] else None
        F["com_lat_off"] = float(abs(F["com"][0] - (max(F["wheel_x"]) + min(F["wheel_x"])) / 2))
    motors = [b for b in solid if b.kind == "motor"]
    F["n_drive_motors"] = len(motors)
    torque, rpm = [], []
    for b in motors:
        p = ph.part(ctx, b)
        rp = r.parts[b.part_idx]
        props = dict(rp.cat.props) if rp.cat is not None else {}
        props.update((p._extra.get("props") or {}) if p else {})
        if props.get("stall_torque_gcm") is not None:
            torque.append(float(props["stall_torque_gcm"]))
        if props.get("rpm_nominal") is not None:
            rpm.append(float(props["rpm_nominal"]))
    F["stall_torque_gcm"] = torque if len(torque) == len(motors) and motors else None
    F["motor_rpm"] = min(rpm) if rpm and len(rpm) == len(motors) else None
    F["robot_height"] = float(np.max([b.aabb[1][2] for b in solid]) - floor)
    # Battery and switch placement.
    bat = [b for b in solid if b.kind == "battery"]
    if bat and F["body_front_y"] is not None:
        F["battery_front_clear"] = float(F["body_front_y"] - max(b.aabb[1][1] for b in bat))
        F["battery_side_clear"] = float(min(min(F["body_max_x"] - b.aabb[1][0], b.aabb[0][0] - F["body_min_x"]) for b in bat))
    sw = [b for b in solid if b.kind == "switch"]
    F["switch_gap"] = float(min(b.aabb[0][2] for b in sw) - floor) if sw else None
    # Outer armour angle: share of outward-facing outer area (front / sides) that is a vertical wall.
    for s, nvec in (("front", (0, 1)), ("sides", None)):
        tot = vert = 0.0
        for b in body:
            if b.kind not in ("structure", "armor", "plate", "wedge", "fork"):
                continue
            fc, fn = b.surface(1.0)
            fa = np.ones(len(fc))
            q = fc[:, :2] - centre
            ang = (np.degrees(np.arctan2(q[:, 1], q[:, 0])) % 360).astype(int) % 360
            outer = np.hypot(q[:, 0], q[:, 1]) >= np.nan_to_num(rout[ang], nan=0) - 3.0
            if s == "front":
                face = outer & S["front"][ang] & (fn[:, 1] > 0.1)
            else:
                face = outer & (S["left"][ang] | S["right"][ang]) & (np.abs(fn[:, 0]) > 0.3)
            tot += float(fa[face].sum())
            vert += float(fa[face & (np.abs(fn[:, 2]) < 0.34)].sum())
        F[f"vertical_frac.{s}"] = vert / tot if tot >= 5 else None
    return F


def _aabb_gap(a, b):
    d = np.maximum(np.maximum(a[0] - b[1], b[0] - a[1]), 0.0)
    return float(np.linalg.norm(d))


def _longest_run_linear(flags):
    best = cur = 0
    for v in flags:
        cur = cur + 1 if v else 0
        best = max(best, cur)
    return best
