"""OpenRadioss offline impact calibration for the fight-sim damage layer.

A rigid steel tooth block (spinner tip) hits the centre of a clamped printed
plate. We sweep speed per material/thickness and store absorbed energy,
rebound speed, peak force and fracture into robot/fight/data/impact_table.json,
which the MuJoCo breakable-weld layer looks up.

Units in the deck: mm, ms, g  ->  force N, stress MPa, energy mJ, velocity mm/ms (= m/s).
Binaries: see tools/openradioss/setup.sh (env OPENRADIOSS_PATH etc).
"""
from __future__ import annotations

import csv
import glob
import json
import os
import shutil
import subprocess
from pathlib import Path

import numpy as np

# Johnson-Cook (LAW2, /MAT/PLAS_JOHNS): rho g/mm3, E MPa, nu, a,b MPa, n, eps_max (failure strain).
# Values are approximate, room temperature, quasi-static, lower-end for FDM prints:
#  PLA/PETG/PC/TPU: manufacturer TDS (Prusament, Polymaker) and Farbak et al. 2023
#   "Johnson-Cook params for FDM PLA"; layer-direction strength derated ~30%.
#  Al 6061-T6: Johnson & Cook 1985 / Lesuer 2000 (A=324,B=114,n=0.42).
#  Hardox 450-ish steel: SSAB datasheet (Rp0.2~1200, A5~10%).
MATERIALS = {
    "PLA":    dict(rho=1.24e-3, E=3500.0,   nu=0.36, a=45.0,   b=15.0,  n=0.30, eps_max=0.03),
    "PETG":   dict(rho=1.27e-3, E=2100.0,   nu=0.38, a=40.0,   b=20.0,  n=0.35, eps_max=0.12),
    "TPU":    dict(rho=1.21e-3, E=50.0,     nu=0.45, a=8.0,    b=30.0,  n=0.60, eps_max=4.00),
    "PC":     dict(rho=1.20e-3, E=2300.0,   nu=0.37, a=60.0,   b=25.0,  n=0.40, eps_max=0.40),
    "AL6061": dict(rho=2.70e-3, E=69000.0,  nu=0.33, a=324.0,  b=114.0, n=0.42, eps_max=0.12),
    "HARDOX": dict(rho=7.85e-3, E=210000.0, nu=0.30, a=1200.0, b=400.0, n=0.20, eps_max=0.10),
}

# ---------------------------------------------------------------- deck writer
def _f(*vals, w=10):
    """Fixed-width (10 char) Radioss field line."""
    out = []
    for v in vals:
        s = "" if v is None else (f"{v:.4g}" if isinstance(v, float) else str(v))
        out.append(s.rjust(w)[:w] if len(s) <= w else f"{v:.3e}".rjust(w)[:w])
    return "".join(out)


def _grid(nx, ny, lx, ly, z, nid0):
    xs = np.linspace(-lx / 2, lx / 2, nx + 1)
    ys = np.linspace(-ly / 2, ly / 2, ny + 1)
    nodes, ids = [], np.zeros((ny + 1, nx + 1), int)
    k = nid0
    for j, y in enumerate(ys):
        for i, x in enumerate(xs):
            nodes.append((k, x, y, z)); ids[j, i] = k; k += 1
    return nodes, ids


def write_deck(workdir, name, tooth_mass_kg, tooth_speed_mps, plate_thickness_mm,
               plate_material, tooth_width_mm=6.0, plate_size_mm=40.0, n_el=16,
               t_end_ms=None):
    """Write <name>_0000.rad and <name>_0001.rad into workdir. Returns paths."""
    m = MATERIALS[plate_material.upper()]
    wd = Path(workdir); wd.mkdir(parents=True, exist_ok=True)
    gap = 0.2
    if t_end_ms is None:  # time to cross gap + ~3 plate-thicknesses deformation, min 0.3 ms
        t_end_ms = max(0.3, (gap + 6 * plate_thickness_mm) / tooth_speed_mps * 4)
    pn, pid = _grid(n_el, n_el, plate_size_mm, plate_size_mm, 0.0, 1)
    tn, tid = _grid(2, 2, tooth_width_mm, tooth_width_mm,
                    gap + plate_thickness_mm / 2, 100001)
    L = ["#RADIOSS STARTER", "/BEGIN", name, "      2024         0",
         "                  g                  mm                  ms",
         "                  g                  mm                  ms",
         "/TITLE", name, "/NODE"]
    for k, x, y, z in pn + tn:
        L.append(f"{k:10d}{x:20.6f}{y:20.6f}{z:20.6f}")
    L += ["/SHELL/1"]
    e = 1
    for j in range(n_el):
        for i in range(n_el):
            L.append(_f(e, pid[j, i], pid[j, i + 1], pid[j + 1, i + 1], pid[j + 1, i])); e += 1
    L += ["/SHELL/2"]
    for j in range(2):
        for i in range(2):
            L.append(_f(e, tid[j, i], tid[j, i + 1], tid[j + 1, i + 1], tid[j + 1, i])); e += 1
    L += ["/PART/1", "plate", _f(1, 1), "/PART/2", "tooth", _f(2, 2),
          "/PROP/SHELL/1", "plate", _f(24, 0, None, 1, 0), "", _f(None, None, None),
          _f(None, None, 5, None, None), _f(float(plate_thickness_mm)),
          "/PROP/SHELL/2", "tooth", _f(24), "", "", "", _f(1.0),
          f"/MAT/PLAS_JOHNS/1", plate_material,
          _f(m["rho"], w=20), _f(m["E"], m["nu"]),
          _f(m["a"], m["b"], m["n"], m["eps_max"], 1e30),
          "", "",
          "/FAIL/JOHNSON/1", "plate_fail",
          # D1..D5 = eps_f constant (simple plastic-strain failure), Ifail_sh=1 element deletion
          _f(m["eps_max"], 0.0, 0.0, 0.0, 0.0), _f(0.0, 1.0, 1, 1),
          "/MAT/ELAST/2", "steel_tooth", _f(7.85e-3, w=20), _f(210000.0, 0.3)]
    # tooth = rigid body on its 9 nodes, mass/inertia overridden to tooth_mass
    master = 200001
    L += [f"{master:10d}{0.0:20.6f}{0.0:20.6f}{gap + plate_thickness_mm/2:20.6f}"]
    L.insert(L.index("/SHELL/1"), L.pop())  # keep master in /NODE block
    L += ["/GRNOD/NODE/2", "tooth_nodes"] + [_f(*tid.ravel()[i:i + 8])
                                             for i in range(0, 9, 8)]
    L += ["/RBODY/1", "tooth", _f(master, None, None, 2, 0, 0, None),
          _f(tooth_mass_kg * 1e3, w=20),  # mass in g
          _f(1.0, w=20) + _f(1.0, w=20) + _f(1.0, w=20),
          _f(0.0, w=20) * 3, ""]
    # clamp plate edges
    edge = np.unique(np.concatenate([pid[0], pid[-1], pid[:, 0], pid[:, -1]]))
    L += ["/GRNOD/NODE/1", "clamp"] + [_f(*edge[i:i + 8]) for i in range(0, len(edge), 8)]
    L += ["/BCS/1", "clamp", "   111 111         0         1"]
    L += ["/GRNOD/NODE/3", "tooth_master", _f(master)]
    L += ["/INIVEL/TRA/1", "tooth_v", _f(0.0, w=20) + _f(0.0, w=20) +
          _f(-float(tooth_speed_mps), w=20) + _f(3)]
    L += ["/SURF/PART/1", "plate_s", _f(1), "/GRNOD/PART/4", "tooth_n", _f(2),
          "/INTER/TYPE7/1", "tooth_plate", _f(4, 1), "", _f(0.0, 0.0, 0.0), _f(0.1), "", "",
          "/TH/RBODY/1", "tooth_th", "DEF", _f(1),
          "/TH/PART/2", "plate_th", "DEF", _f(1),
          "/TH/INTER/3", "contact_th", "DEF", _f(1),
          "/END"]
    starter = wd / f"{name}_0000.rad"
    starter.write_text("\n".join(L) + "\n")
    eng = ["/RUN/" + name + "/1", f"{t_end_ms:.6g}",
           "/TFILE/0", f"{t_end_ms/400:.6g}", "/ANIM/DT", "0", f"{t_end_ms/10:.6g}",
           "/ANIM/ELEM/EPSP", "/ANIM/ELEM/DAMA", "/DT/NODA/CST/0", "0.67 1e-6",
           "/PRINT/-100", "/END"]
    engine = wd / f"{name}_0001.rad"
    engine.write_text("\n".join(eng) + "\n")
    return starter, engine


# ---------------------------------------------------------------- runner
def _exe(prefix):
    root = os.environ.get("OPENRADIOSS_PATH") or os.path.expanduser("~/.cache/openradioss")
    hits = sorted(glob.glob(f"{root}/**/{prefix}_linux64_gf", recursive=True))
    return hits[0] if hits else shutil.which(prefix)


def binaries_available():
    return bool(_exe("starter") and _exe("engine"))


def _th_csv(wd, name):
    exe = _exe("th_to_csv")
    t01 = wd / f"{name}T01"
    if not (exe and t01.exists()):
        return None
    subprocess.run([exe, str(t01)], cwd=wd, check=True, capture_output=True)
    p = wd / f"{name}T01.csv"
    with open(p) as fh:
        rows = list(csv.reader(fh))
    head = [h.strip() for h in rows[0]]
    data = np.array([[float(x) for x in r] for r in rows[1:] if r], float)
    return head, data


def impact_case(tooth_mass_kg, tooth_speed_mps, plate_thickness_mm, plate_material,
                tooth_width_mm=6.0, workdir=None, ncpu=4, **kw):
    if not binaries_available():
        raise RuntimeError("OpenRadioss binaries not found; run tools/openradioss/setup.sh")
    name = f"imp_{plate_material}_{plate_thickness_mm:g}_{tooth_speed_mps:g}".replace(".", "p")
    wd = Path(workdir or f"/tmp/openradioss/{name}")
    write_deck(wd, name, tooth_mass_kg, tooth_speed_mps, plate_thickness_mm,
               plate_material, tooth_width_mm, **kw)
    env = dict(os.environ, OMP_NUM_THREADS=str(ncpu))
    subprocess.run([_exe("starter"), "-i", f"{name}_0000.rad", "-np", "1"],
                   cwd=wd, env=env, check=True, capture_output=True)
    subprocess.run([_exe("engine"), "-i", f"{name}_0001.rad"],
                   cwd=wd, env=env, check=True, capture_output=True)
    out = parse_outputs(wd, name, tooth_mass_kg, tooth_speed_mps, n_el=kw.get("n_el", 16))
    out.update(material=plate_material, t_mm=plate_thickness_mm, v=tooth_speed_mps)
    return out


def parse_outputs(wd, name, mass_kg, v0, n_el=16):
    wd = Path(wd)
    th = _th_csv(wd, name)
    res = dict(E_abs=None, v_rebound=None, max_eps_p=None, fracture=None,
               eroded_frac=None, peak_N=None)
    if th:
        head, d = th
        col = lambda key: next((i for i, h in enumerate(head) if key in h.upper()), None)
        iv = col("VZ"); iF = col("FZ")  # rigid-body VZ, contact normal force
        if iv is not None:
            v1 = d[-1, iv]
            res["v_rebound"] = float(v1)
            res["E_abs"] = float(0.5 * mass_kg * (v0 ** 2 - v1 ** 2))  # J
        if iF is not None:
            res["peak_N"] = float(np.abs(d[:, iF]).max())
    # listing: count deleted shells ("ELEMENT DELETED" / "SHELL ELEMENT ... DELETED")
    lst = list(wd.glob(f"{name}_0001.out"))
    if lst:
        txt = lst[0].read_text(errors="ignore")
        ndel = txt.upper().count("DELETED")
        res["eroded_frac"] = ndel / (n_el * n_el)
        res["fracture"] = ndel > 0
    return res


def calibrate(cases, out_path=None, **kw):
    """cases: iterable of (material, thickness_mm, tooth_mass_kg, [speeds])."""
    out_path = Path(out_path or Path(__file__).parent / "data" / "impact_table.json")
    table = {}
    for mat, t, mass, speeds in cases:
        rows = []
        for v in speeds:
            r = impact_case(mass, v, t, mat, **kw)
            rows.append({"v": v, "E_abs": r["E_abs"], "fracture": r["fracture"],
                         "peak_N": r["peak_N"], "eroded_frac": r["eroded_frac"],
                         "v_rebound": r["v_rebound"]})
        table[f"{mat}_{t:g}mm"] = rows
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_text(json.dumps(table, indent=2))
    return table


DEFAULT_SWEEP = [("PLA", 3, 0.010, [20, 40, 60]),
                 ("TPU", 3, 0.010, [20, 40, 60]),
                 ("PC", 2, 0.010, [20, 40, 60])]

if __name__ == "__main__":
    print(json.dumps(calibrate(DEFAULT_SWEEP), indent=2))
