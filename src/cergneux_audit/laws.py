# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Pedro Sordo Martínez
"""Ecuaciones de «Teoría del Tiempo Cuántico» (Cergneux, ene. 2025), con página del PDF."""
import math
import numpy as np
from .constants import C, G, LP, TP, GM_SUN


def gamma(v):
    """Factor de Lorentz (p. 13)."""
    b = np.asarray(v, dtype=float) / C
    if np.any(np.abs(b) >= 1):
        raise ValueError("|v| debe ser < c")
    return 1.0 / np.sqrt(1.0 - b**2)


def schwarzschild_radius(mass):
    """r_s = 2GM/c² (p. 43)."""
    return 2 * G * mass / C**2


def rho_velocity(v):
    """ρ = 1/√(1−v²/c²) (Ley del Fotón, p. 32)."""
    return gamma(v)


def rho_schwarzschild(r, mass):
    """ρ = 1/√(1−r_s/r) (p. 32). Solo definido para r > r_s."""
    rs = schwarzschild_radius(mass)
    r = np.asarray(r, dtype=float)
    if np.any(r <= rs):
        raise ValueError("r debe ser > r_s")
    return 1.0 / np.sqrt(1.0 - rs / r)


def r_over_rs_for_rho(rho):
    """Despeja r/r_s de ρ = 1/√(1−r_s/r):  r/r_s = ρ²/(ρ²−1)."""
    rho = np.asarray(rho, dtype=float)
    return rho**2 / (rho**2 - 1.0)


def te_from_tr(tr, rho):
    """Ley del Fotón: Te = Tr/ρ (p. 31)."""
    return tr / rho


def ce_from_cr(cr, rho):
    """Ley de la Luz: Ce = Cr/ρ (p. 33)."""
    return cr / rho


def photons_received_per_emitted(rho):
    """Ley de la Energía (p. 30-31): n_r = ρ·n_e. Es la afirmación a auditar."""
    return rho


def planck_speed():
    """L_p/T_p. Es c por construcción (p. 5): no confirma nada."""
    return LP / TP


def planck_ticks_per_second():
    """1/T_p ≈ 1.85487e43 (p. 6)."""
    return 1.0 / TP


def mercury_numbers():
    """Aritmética de las pp. 37-38: reloj de Mercurio, desfase en km y precesión GR."""
    a_m, e_m = 5.7909e10, 0.2056
    a_e = 1.495978707e11
    v_m, v_e = 47.36e3, 29.78e3

    def rate(a, v):
        return math.sqrt(1 - 2 * GM_SUN / (a * C**2) - (v / C) ** 2)

    clock_gap = 1 - rate(a_m, v_m) / rate(a_e, v_e)
    b_m = a_m * math.sqrt(1 - e_m**2)
    perimeter = math.pi * (3 * (a_m + b_m) - math.sqrt((3 * a_m + b_m) * (a_m + 3 * b_m)))
    shift_dilation_km = perimeter * clock_gap / 1e3
    dphi = 6 * math.pi * GM_SUN / (C**2 * a_m * (1 - e_m**2))
    shift_geometric_km = dphi * a_m / 1e3
    return {
        "clock_gap_ns_per_s": clock_gap * 1e9,
        "paper_clock_gap_ns_per_s": 24.55,
        "shift_from_dilation_km": shift_dilation_km,
        "paper_shift_km": 28.8,
        "shift_from_precession_km": shift_geometric_km,
        "precession_arcsec_per_orbit": math.degrees(dphi) * 3600,
        "ratio_precession_to_dilation": shift_geometric_km / shift_dilation_km,
    }
