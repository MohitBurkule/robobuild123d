"""Rigid transforms as 4x4 numpy matrices. Euler angles are degrees, R = Rz * Ry * Rx (same as the Rust crate and OpenSCAD)."""

from __future__ import annotations

import math

import numpy as np


def euler(rot) -> np.ndarray:
    rx, ry, rz = (math.radians(float(a)) for a in rot)
    cx, sx, cy, sy, cz, sz = math.cos(rx), math.sin(rx), math.cos(ry), math.sin(ry), math.cos(rz), math.sin(rz)
    Rx = np.array([[1, 0, 0], [0, cx, -sx], [0, sx, cx]])
    Ry = np.array([[cy, 0, sy], [0, 1, 0], [-sy, 0, cy]])
    Rz = np.array([[cz, -sz, 0], [sz, cz, 0], [0, 0, 1]])
    return Rz @ Ry @ Rx


def axis_angle(axis, deg) -> np.ndarray:
    a = np.asarray(axis, float)
    n = np.linalg.norm(a)
    if n < 1e-12:
        return np.eye(3)
    a = a / n
    s, c = math.sin(math.radians(deg)), math.cos(math.radians(deg))
    t = 1 - c
    x, y, z = a
    return np.array([[t * x * x + c, t * x * y - s * z, t * x * z + s * y],
                     [t * x * y + s * z, t * y * y + c, t * y * z - s * x],
                     [t * x * z - s * y, t * y * z + s * x, t * z * z + c]])


def align_z_to(d) -> np.ndarray:
    d = np.asarray(d, float)
    n = np.linalg.norm(d)
    if n < 0.5 * 1e-9 or n < 1e-9:
        return np.eye(3)
    d = d / n
    c = d[2]
    if c > 1 - 1e-12:
        return np.eye(3)
    if c < -1 + 1e-12:
        return axis_angle([1, 0, 0], 180)
    return axis_angle(np.cross([0, 0, 1], d), math.degrees(math.acos(max(-1.0, min(1.0, c)))))


def make(R=None, t=None) -> np.ndarray:
    M = np.eye(4)
    if R is not None:
        M[:3, :3] = R
    if t is not None:
        M[:3, 3] = t
    return M


def pose(at, rot) -> np.ndarray:
    return make(euler(rot), at)


def translation(t) -> np.ndarray:
    return make(None, t)


def rotation_about(pivot, axis, deg) -> np.ndarray:
    R = axis_angle(axis, deg)
    p = np.asarray(pivot, float)
    return make(R, p - R @ p)


def apply(M, p) -> np.ndarray:
    p = np.asarray(p, float)
    return p @ M[:3, :3].T + M[:3, 3]


def apply_dir(M, d) -> np.ndarray:
    return np.asarray(d, float) @ M[:3, :3].T


def inv(M) -> np.ndarray:
    R = M[:3, :3]
    return make(R.T, -R.T @ M[:3, 3])


def norm(v) -> np.ndarray:
    v = np.asarray(v, float)
    n = np.linalg.norm(v)
    return v / n if n > 1e-12 else v
