# SPDX-FileCopyrightText: 2026 Pedro Sordo Martínez <amurlaniakea@gmail.com>
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Contraste cosmológico (pp. 43-51 del PDF de la Teoría del Tiempo Cuántico)."""
import numpy as np
from .constants import C, G, MPC, KB, H


def hubble_radius(h0_km_s_mpc=67.4):
    return C / (h0_km_s_mpc * 1e3 / MPC)


def critical_mass_in_hubble_sphere(h0_km_s_mpc=67.4):
    """M = ρ_c·(4π/3)(c/H0)³ = c³/(2·G·H0)."""
    h0 = h0_km_s_mpc * 1e3 / MPC
    return C**3 / (2 * G * h0)


def rs_over_hubble_radius(h0_km_s_mpc=67.4):
    """r_s de esa masa / (c/H0): identidad algebraica = 1, no coincidencia."""
    m = critical_mass_in_hubble_sphere(h0_km_s_mpc)
    return (2 * G * m / C**2) / hubble_radius(h0_km_s_mpc)


def _check_z(z):
    z = np.asarray(z, dtype=float)
    if np.any(z <= -1.0):
        raise ValueError("z debe ser > −1")
    return z


def comoving_distance(z, h0=67.4, om=0.315, n=20001):
    """Distancia comóvil (plano, ΛCDM). Integra en u = ln(1+z) con trapecios: preciso hasta z ~ 1e3."""
    z = _check_z(np.atleast_1d(z))
    out = []
    for zi in z:
        if zi == 0:
            out.append(0.0)
            continue
        u = np.linspace(0.0, np.log1p(zi), n)
        zz = np.expm1(u)
        f = (1 + zz) / np.sqrt(om * (1 + zz) ** 3 + (1 - om))        # dz = (1+z) du
        out.append(np.sum((f[1:] + f[:-1]) * np.diff(u)) / 2)
    return hubble_radius(h0) * np.array(out)


def luminosity_distance(z, h0=67.4, om=0.315):
    return (1 + np.atleast_1d(z)) * comoving_distance(z, h0, om)


def sn_stretch_standard(z):
    """Dilatación temporal cosmológica estándar: Δt_obs = (1+z)·Δt_rest."""
    return 1.0 + _check_z(z)


def sn_stretch_cergneux(z):
    """Ley de la Fila (p. 34, 47): Tr = ρ·Tm con ρ = 1+z  ⇒  Tm = Tr/(1+z)."""
    return 1.0 / (1.0 + _check_z(z))


def observed_duration_ley_del_tiempo(z, proper_duration=1.0):
    """Lectura coherente con la Ley del Tiempo (TC p. 31): Tr = ρ·Te con ρ = 1+z.
    Un proceso de duración propia fija Te = N se observa durando N·ρ en nuestros segundos (estiramiento)."""
    return (1.0 + _check_z(z)) * proper_duration


def _planck_u(nu, temp):
    return 8 * np.pi * H * nu**3 / C**3 / np.expm1(H * nu / (KB * temp))


def energy_conserving_emissivity(rho, temp_emit=3000.0, n=200_000):
    """Aplica Ee=Er por bandas (p. 29-30) a un cuerpo negro de T_e con f→f/ρ.

    Devuelve (energía recibida) / (energía de un cuerpo negro a T_e/ρ) = emisividad efectiva.
    El estándar da 1 (FIRAS: 1 ± 1e-5). Aquí sale ρ⁴.
    """
    nu_e = np.linspace(1e9, 40 * KB * temp_emit / H, n)
    e_received = np.sum(_planck_u(nu_e, temp_emit)) * (nu_e[1] - nu_e[0])
    nu_r = np.linspace(1e6, 40 * KB * (temp_emit / rho) / H, n)
    e_bb = np.sum(_planck_u(nu_r, temp_emit / rho)) * (nu_r[1] - nu_r[0])
    return e_received / e_bb
