# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Pedro Sordo Martínez
"""Circuito Josephson: física estándar frente a la reinterpretación (Cergneux, dic. 2025)."""
import math
import numpy as np
from .constants import HBAR, KB, PHI0, TP


def transmon_levels(ej, ec, ng=0.0, ncut=30, nlevels=5):
    """Diagonaliza H = 4E_C (n−ng)² − E_J cos φ en base de carga (unidades de ej, ec)."""
    n = np.arange(-ncut, ncut + 1)
    h = np.diag(4 * ec * (n - ng) ** 2).astype(float)
    off = -ej / 2 * np.ones(len(n) - 1)
    h += np.diag(off, 1) + np.diag(off, -1)
    return np.linalg.eigvalsh(h)[:nlevels]


def washboard(phi, ej, bias_ratio):
    """U(φ) = −E_J cos φ − E_J·(I/I_c)·φ."""
    return -ej * np.cos(phi) - ej * bias_ratio * phi


def dn_dt_standard(phi, ej, f, hbar=HBAR):
    """−(1/ħ)∂H/∂φ con H = … − E_J cos φ − Fφ  ⇒  (F − E_J sin φ)/ħ."""
    return (f - ej * np.sin(phi)) / hbar


def dn_dt_paper(phi, ej, f, hbar=HBAR):
    """Expresión impresa en la sec. 4.1 del PDF: (E_J sin φ + F)/ħ."""
    return (ej * np.sin(phi) + f) / hbar


def barrier_height(i0, bias_ratio):
    """ΔU = (2√2 I0 Φ0 /3π)(1−I/I0)^{3/2} (aprox. cúbica)."""
    return 2 * math.sqrt(2) * i0 * PHI0 / (3 * math.pi) * (1 - bias_ratio) ** 1.5


def plasma_frequency(i0, cap, bias_ratio):
    """ω_p = 2^{1/4} √(2π I0/(Φ0 C)) (1−I/I0)^{1/4}  [rad/s]."""
    return 2 ** 0.25 * math.sqrt(2 * math.pi * i0 / (PHI0 * cap)) * (1 - bias_ratio) ** 0.25


def escape_rate_thermal(i0, cap, bias_ratio, temp):
    du, wp = barrier_height(i0, bias_ratio), plasma_frequency(i0, cap, bias_ratio)
    return wp / (2 * math.pi) * math.exp(-du / (KB * temp))


def escape_rate_quantum(i0, cap, bias_ratio, q=30.0):
    """Γ_q = a_q (ω_p/2π) exp[−7.2 ΔU/ħω_p (1+0.87/Q)]  (Devoret-Martinis-Clarke 1985). Sin T."""
    du, wp = barrier_height(i0, bias_ratio), plasma_frequency(i0, cap, bias_ratio)
    x = du / (HBAR * wp)
    a_q = math.sqrt(120 * math.pi * 7.2 * x)
    return a_q * wp / (2 * math.pi) * math.exp(-7.2 * x * (1 + 0.87 / q))


def crossover_temperature(i0, cap, bias_ratio, q=30.0):
    wp = plasma_frequency(i0, cap, bias_ratio)
    return HBAR * wp / (2 * math.pi * KB) * (math.sqrt(1 + 1 / (4 * q**2)) - 1 / (2 * q))


def escape_rate(i0, cap, bias_ratio, temp, q=30.0):
    """Interpolación simple: la mayor entre la tasa cuántica (plana en T) y la térmica."""
    return max(escape_rate_thermal(i0, cap, bias_ratio, temp),
               escape_rate_quantum(i0, cap, bias_ratio, q))


def cergneux_t2(f01_hz):
    """Test 1 del PDF: T₂ ~ τ_p · 2π/(ΔE/ħ) = τ_p / f₀₁."""
    return TP / f01_hz
