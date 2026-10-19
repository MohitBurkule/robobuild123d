"""Attack model for the combat failure-mode checks (`threat.CF-*`): who hits the robot, from where, how hard, and the
geometry helpers that turn "from where" into "which surface gets hit".

Conventions as in `_physics` / `combat_ground`: world mm, +Y front, +Z up, +X the robot's left. A *bearing* is the
direction (in the XY plane, degrees, 0 = +X, 90 = front) at which the attacker sits as seen from the robot centre; the
attacker travels toward the centre, so its travel direction is minus the bearing vector.

Visibility is a z-buffer, not a ray library: the robot's surface samples are projected on the plane normal to the attack
direction, binned in `CELL_MM` cells, and in every cell the samples within `DEPTH_TOL_MM` of the nearest one are "hit
first". That is what an incoming blade, hammer or wedge meets. It is cheap (numpy only) and deterministic.
"""

from __future__ import annotations

import math

import numpy as np

from ... import catalog

# ---- the reference attackers (antweight, 150 g class; numbers from combat_failure_modes.md) -------------------------
CELL_MM = 2.0
DEPTH_TOL_MM = 1.0
E_TIP_REF_J = 25.0  # a typical antweight vertical/horizontal spinner tip energy
V_TIP_REF_MS = 40.0  # its tip speed
E_HAMMER_J = 5.0  # hammer / axe blow
CLOSING_MS = 3.0  # closing speed for the bite depth
REF_TEETH, REF_RPM = 2, 15000.0
REF_TOOTH_W_MM = (6.0, 12.0)
REF_WEDGE_LIPS_MM = (0.0, 0.2, 0.3, 0.5, 0.5)  # taxonomy reference opponent lip heights
DROP_G = 20.0  # landing deceleration
DYN_FACTOR = 3.0

# Attack bands: (bearings deg, elevations deg, z band above the floor mm). Bearings: 0 = left (+X), 90 = front, 180 = right.
FRONT_SIDE = tuple(range(0, 181, 10))
ALL_AROUND = tuple(range(0, 360, 10))
ATTACKS = {
    "vertical": {"bearings": FRONT_SIDE, "elev": (0.0, 30.0), "z": (0.0, 40.0)},
    "drum": {"bearings": FRONT_SIDE, "elev": (0.0,), "z": (15.0, 45.0)},
    "horizontal": {"bearings": ALL_AROUND, "elev": (0.0,), "z": (2.0, 15.0)},
    "undercutter": {"bearings": ALL_AROUND, "elev": (0.0,), "z": (0.0, 8.0)},
    "overcutter": {"bearings": ALL_AROUND, "elev": (30.0,), "z": (None, None)},  # top band of the robot
    "hammer": {"bearings": (), "elev": (90.0,), "z": (None, None)},  # from straight above (also top saws)
    "wedge": {"bearings": ALL_AROUND, "elev": (0.0,), "z": (0.0, 3.0)},  # wedges, flippers, lifters at the floor
    "wall": {"bearings": ALL_AROUND, "elev": (0.0,), "z": (0.0, 999.0)},  # arena walls
}
# Debris that jams moving parts: gaps inside the band let it in and hold it; tighter or wider gaps are safe.
DEBRIS_WHEEL_MM = (1.5, 15.0)
DEBRIS_WEAPON_MM = (1.5, 10.0)
VENT_MM = 2.0

# Strain to failure used for impact-energy capacity (handbook-ish; printed values are along the layers).
DUCTILITY = {
    "pla": 0.02, "pla_st": 0.03, "petg": 0.05, "abs": 0.04, "asa": 0.04, "nylon": 0.15, "pa12": 0.12, "taulman910": 0.2,
    "pla_cf": 0.015, "petg_cf": 0.02, "pa_cf": 0.03, "cf_filament": 0.015, "pc": 0.1, "polycarbonate": 0.1, "resin": 0.02,
    "tpu": 1.0, "tpu_95a": 1.0, "tpu_85a": 1.0, "hdpe": 0.3, "pp": 0.3, "polypropylene": 0.3, "uhmw": 0.3,
    "cf_plate": 0.01, "carbon_fibre": 0.01, "fr4": 0.02, "g10": 0.02, "aluminium": 0.1, "aluminum": 0.1, "steel": 0.15,
    "304": 0.3, "stainless": 0.3, "hardox": 0.1, "titanium": 0.1, "brass": 0.2, "copper": 0.3, "spring_steel": 0.05,
}
BRITTLE = {"pla", "pla_st", "pla_cf", "petg_cf", "cf_filament", "resin", "acrylic", "pmma", "cf_plate", "carbon_fibre"}
METAL = {"steel", "304", "stainless", "hardox", "titanium", "aluminium", "aluminum", "brass", "copper", "spring_steel"}
ENERGY_FRACTION = 0.25  # share of a plate's ductile capacity that a local blow actually engages (assumption)
CRITICAL = ("battery", "esc", "receiver", "switch", "motor", "weapon_motor", "servo")
WHEELISH = ("wheel", "tyre")


def bite_depth(v_closing=CLOSING_MS, teeth=REF_TEETH, rpm=REF_RPM):
    """mm a spinner tooth advances into the robot between two teeth: d = v / (n * rpm / 60)."""
    return v_closing * 1000.0 / (teeth * rpm / 60.0)


def travel_dir(bearing_deg, elev_deg=0.0):
    """Unit travel direction of an attacker at `bearing_deg` (around the robot) and `elev_deg` above the horizon."""
    b, e = math.radians(bearing_deg), math.radians(elev_deg)
    return -np.array([math.cos(e) * math.cos(b), math.cos(e) * math.sin(b), math.sin(e)])


def is_metal(mat):
    return bool(mat) and (mat in METAL or any(mat.startswith(m) for m in ("steel", "ti", "alu", "spring")))


def mech(mat):
    """(yield MPa, E MPa, strain to failure) of a material, or None when unknown."""
    m = catalog.mech(mat)
    if m is None:
        return None
    return m[0], m[2] * 1000.0, DUCTILITY.get(mat, 0.05)


def energy_capacity_j(mat, vol_mm3):
    """Impact energy (J) a volume of material soaks up before it breaks: elastic plus a ductile term, scaled by
    `ENERGY_FRACTION` because a local blow engages only part of it. MPa * mm^3 = mJ."""
    m = mech(mat)
    if m is None:
        return None
    sy, E, ef = m
    return (sy * sy / (2.0 * E) + sy * ef) * vol_mm3 * ENERGY_FRACTION * 1e-3


def visible(P, d, cell=CELL_MM, tol=DEPTH_TOL_MM):
    """Boolean mask of the points of `P` an attacker travelling along unit `d` meets first (z-buffer)."""
    d = np.asarray(d, float)
    a = np.array([0.0, 0.0, 1.0]) if abs(d[2]) < 0.9 else np.array([1.0, 0.0, 0.0])
    u = np.cross(d, a)
    u /= np.linalg.norm(u)
    v = np.cross(d, u)
    iu = np.floor(P @ u / cell).astype(np.int64)
    iv = np.floor(P @ v / cell).astype(np.int64)
    key = (iu - iu.min()) * (int(iv.max() - iv.min()) + 1) + (iv - iv.min())
    depth = P @ d
    order = np.lexsort((depth, key))
    ks = key[order]
    first = np.ones(len(ks), bool)
    first[1:] = ks[1:] != ks[:-1]
    start = np.maximum.accumulate(np.where(first, np.arange(len(ks)), 0))
    near = depth[order] <= depth[order][start] + tol
    out = np.zeros(len(P), bool)
    out[order[near]] = True
    return out


def thickness(body, pts, nrm, max_mm=8.0, step=0.25):
    """Wall thickness (mm) at surface points of `body`, marching inward along -normal until leaving the solid. Capped at
    `max_mm`."""
    if not len(pts):
        return np.zeros(0)
    s = np.arange(step, max_mm + step, step)
    Q = (pts[:, None, :] - nrm[:, None, :] * s[None, :, None]).reshape(-1, 3)
    ins = body.inside(Q).reshape(len(pts), len(s))
    ins[:, 0] = True  # the first step can graze a curved face
    out = ~ins
    first = np.where(out.any(axis=1), out.argmax(axis=1), len(s))
    return np.where(first < len(s), s[np.minimum(first, len(s) - 1)] - step / 2, max_mm)


def cyl_gap(P, origin, axis, R, t0, t1):
    """Distance (mm) from points to the solid cylinder swept by a part spinning about (origin, axis): radius R, axial span
    t0..t1. Zero or negative inside."""
    q = np.asarray(P, float) - origin
    t = q @ axis
    r = np.linalg.norm(q - np.outer(t, axis), axis=1)
    dr = r - R
    dt = np.maximum(t0 - t, t - t1)
    return np.where((dr > 0) & (dt > 0), np.hypot(dr, dt), np.maximum(dr, dt))


def part_of(endpoint, ids):
    """Part id of a wire endpoint written `part` or `part.port`."""
    if endpoint in ids:
        return endpoint
    head = str(endpoint).split(".")[0]
    return head if head in ids else None
