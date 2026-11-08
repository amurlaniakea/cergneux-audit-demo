# SPDX-FileCopyrightText: 2026 Pedro Sordo Martínez <amurlaniakea@gmail.com>
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Retícula espacio-temporal discreta como paseo cuántico (1D), en unidades a = τ = 1.

Modela el postulado de «Teoría del Tiempo Cuántico» (pp. 5-6): un paso de una celda por tick
(c = ℓ_p/T_p) para la luz y movimiento más lento para partículas con masa.
Operador por tick: U(k) = S(k)·C(θ), con S = diag(e^{-ik}, e^{+ik}) y C = [[cosθ, i sinθ],[i sinθ, cosθ]].
Relación de dispersión exacta: cos ω = cosθ·cos k.  Con a = ℓ_p y τ = T_p: k = p·c/E_P y θ = m/m_P.
Límite continuo: ω² = k² + θ² − θ²k²/3 + O(6): la desviación de Lorentz es de orden (E/E_P)².
Alcance: modelo 1D; no prueba anisotropía de una retícula cúbica 3D ni la simultaneidad universal.
"""
import numpy as np
from .constants import C, G, HBAR


def planck_energy():
    """E_P = √(ħc⁵/G) [J] = ħ/T_p."""
    return float(np.sqrt(HBAR * C**5 / G))


def dispersion(k, theta):
    """ω(k) exacto: cos ω = cosθ cos k (ω ≥ 0)."""
    return np.arccos(np.clip(np.cos(theta) * np.cos(k), -1.0, 1.0))


def group_velocity(k, theta):
    """v_g = dω/dk = cosθ·sin k / sin ω  (celdas por tick)."""
    k = np.asarray(k, dtype=float)
    w = dispersion(k, theta)
    with np.errstate(divide="ignore", invalid="ignore"):
        v = np.cos(theta) * np.sin(k) / np.sin(w)
    return np.where(np.isfinite(v), v, 0.0)


def eigen_omega(k, theta):
    """ω obtenido diagonalizando U(k) (comprobación independiente de la fórmula cerrada)."""
    s = np.diag([np.exp(-1j * k), np.exp(1j * k)])
    c = np.array([[np.cos(theta), 1j * np.sin(theta)], [1j * np.sin(theta), np.cos(theta)]])
    return float(np.max(np.abs(np.angle(np.linalg.eigvals(s @ c)))))


def relative_deviation(k, theta):
    """ω_retícula/√(k²+θ²) − 1 (exacto, sirve para λ moderados)."""
    return dispersion(k, theta) / np.sqrt(k**2 + theta**2) - 1.0


def relative_deviation_series(k, theta):
    """Orden dominante: −θ²k²/(6(k²+θ²)) (negativa: la retícula va más lenta). Válida y estable para k, θ ≪ 1."""
    return -theta**2 * k**2 / (6.0 * (k**2 + theta**2))


def physical_deviation(energy_j, mass_j):
    """Desviación relativa esperada en este modelo para una partícula de energía y masa dadas."""
    ep = planck_energy()
    return float(relative_deviation_series(energy_j / ep, mass_j / ep))


def simulate_walk(k0, theta, sigma=25.0, steps=300, n=4096):
    """Paquete gaussiano en la rama de eigenvalor e^{-iω}; devuelve celdas/tick medidas (centroide)."""
    x = np.arange(n) - n // 2
    k = 2 * np.pi * np.fft.fftfreq(n)
    s_k = np.exp(-1j * k)
    ct, st = np.cos(theta), np.sin(theta)
    # spinor propio en k0 (rama con ángulo +ω ⇒ velocidad de grupo +)
    s0 = np.diag([np.exp(-1j * k0), np.exp(1j * k0)])
    c0 = np.array([[ct, 1j * st], [1j * st, ct]])
    vals, vecs = np.linalg.eig(s0 @ c0)
    w = dispersion(k0, theta)
    idx = int(np.argmin(np.abs(vals - np.exp(-1j * w))))
    spinor = vecs[:, idx]
    env = np.exp(-(x.astype(float) ** 2) / (4 * sigma**2)) * np.exp(1j * k0 * x)
    psi = np.stack([spinor[0] * env, spinor[1] * env])
    pk = np.fft.fft(psi, axis=1)
    for _ in range(steps):
        a = ct * pk[0] + 1j * st * pk[1]
        b = 1j * st * pk[0] + ct * pk[1]
        pk = np.stack([np.exp(-1j * k) * a, np.exp(1j * k) * b])
    dens = np.sum(np.abs(np.fft.ifft(pk, axis=1)) ** 2, axis=0)
    return float(np.sum(x * dens) / np.sum(dens) / steps)
