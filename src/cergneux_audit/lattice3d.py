# SPDX-FileCopyrightText: 2026 Pedro Sordo Martínez <amurlaniakea@gmail.com>
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Retícula cúbica 3D: isotropía de la luz y dispersión espacial, frente a cotas observacionales.

Dos lecturas independientes del postulado «una celda de Planck por tick» (TC pp. 4-6):
 1. Luz que avanza celda a celda por tick sobre una retícula cúbica (literal): la velocidad euclídea depende de
    la dirección. Con vecinos por caras (6 movimientos) v = 1/‖n‖₁ ∈ [1/√3, 1]; con los 26 vecinos
    v = 1/‖n‖∞ ∈ [1, √3]. La anisotropía es O(1), no O((E/E_P)²).
 2. Retícula espacial con tiempo continuo (Klein-Gordon discreto): ω² = Σ (4/a²) sin²(k_i a/2);
    a lo largo de un eje v = cos(ka/2) ≈ 1 − (ka)²/8, con ka = E/E_P.
Nota: el PDF también permite saltos a «cualquier píxel»; eso evita la anisotropía pero abandona la localidad.
Cotas (verificadas en sus abstracts): isotropía de c ~1e-17 (Eisele et al. PRL 103, 090401, 2009; Herrmann et al.
arXiv:1002.1284); Vasileiou et al. PRD 87, 122001 (2013): E_QG,1 > 7,6 E_P y E_QG,2 > 1,3e11 GeV (GRB 090510, 95 % CL).
"""
import numpy as np
from .constants import E
from .lattice import planck_energy

LAB_ISOTROPY_LIMIT = 1e-17          # Δc/c
GRB_EQG1_LIMIT_IN_EP = 7.6          # E_QG,1 > 7,6 E_P
GRB_EQG2_LIMIT_GEV = 1.3e11         # E_QG,2 > 1,3e11 GeV


def _unit(n):
    n = np.asarray(n, dtype=float)
    return n / np.linalg.norm(n, axis=-1, keepdims=True)


def axis_move_speed(n):
    """Velocidad euclídea por tick con movimientos solo a vecinos por caras: 1/‖n‖₁ (n unitario)."""
    return 1.0 / np.sum(np.abs(_unit(n)), axis=-1)


def king_move_speed(n):
    """Velocidad euclídea por tick con los 26 vecinos (un paso de Chebyshev por tick): 1/‖n‖∞."""
    return 1.0 / np.max(np.abs(_unit(n)), axis=-1)


def speed_spread(speed_fn, n_samples=20000, seed=0):
    """(v_max − v_min)/v_max sobre direcciones aleatorias, incluyendo ejes y diagonales exactos."""
    rng = np.random.default_rng(seed)
    d = np.vstack([rng.normal(size=(n_samples, 3)), np.eye(3), np.ones((1, 3))])
    v = speed_fn(d)
    return float((v.max() - v.min()) / v.max())


def kg_omega(kvec, a=1.0):
    """ω(k) de Klein-Gordon sin masa en retícula cúbica de paso a (c = 1)."""
    k = np.asarray(kvec, dtype=float)
    return np.sqrt(np.sum((2.0 / a * np.sin(k * a / 2.0)) ** 2, axis=-1))


def kg_group_speed_axis(k, a=1.0):
    """Velocidad de grupo a lo largo de un eje: cos(ka/2)."""
    return np.cos(np.asarray(k, dtype=float) * a / 2.0)


def eqg2_in_planck_energies():
    """E_QG,2 efectivo en unidades de E_P. v = 1 − (ka)²/8 y, con la convención de Vasileiou et al.,
    v = c[1 − (3/2)(E/E_QG,2)²]  ⇒  E_QG,2 = √12·E_P."""
    return float(np.sqrt(12.0))


def eqg2_gev():
    return eqg2_in_planck_energies() * planck_energy() / (E * 1e9)
