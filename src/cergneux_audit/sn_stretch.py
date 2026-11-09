# SPDX-FileCopyrightText: 2026 Pedro Sordo Martínez <amurlaniakea@gmail.com>
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Contraste del estiramiento temporal de supernovas Ia: anchura_obs/anchura_reposo = (1+z)^b.

Estándar: b = +1.  Ley de la Fila de Cergneux (TC pp. 34, 47): Tm = Tr/(1+z)  ⇒  b = −1.
"""
import csv
import numpy as np


def fit_exponent(z, ratio, sigma):
    """Ajusta ln(ratio) = b·ln(1+z) (sin término libre) con pesos 1/σ². Devuelve (b, error)."""
    z, ratio, sigma = (np.asarray(a, dtype=float) for a in (z, ratio, sigma))
    x, y = np.log1p(z), np.log(ratio)
    w = (ratio / sigma) ** 2                      # σ(ln r) = σ/r
    sxx = np.sum(w * x * x)
    return float(np.sum(w * x * y) / sxx), float(1.0 / np.sqrt(sxx))


def load_csv(path):
    """CSV con cabecera: z,width_ratio,sigma. width_ratio = anchura observada / anchura en reposo."""
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    cols = ("z", "width_ratio", "sigma")
    return tuple(np.array([float(r[c]) for r in rows]) for c in cols)


def load_aging_csv(path):
    """CSV de Blondin et al. 2008 (Tabla 3): sn,z,aging_rate,sigma,sample. Devuelve (z, tasa, σ, es_lejana)."""
    with open(path, newline="", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    z, rate, sig = (np.array([float(r[c]) for r in rows]) for c in ("z", "aging_rate", "sigma"))
    return z, rate, sig, np.array([r["sample"] == "high" for r in rows])


def chi2_aging(z, rate, sigma, b):
    """χ² de la tasa de envejecimiento (Δt_reposo/Δt_obs) frente a (1+z)^(−b).

    b = +1: estándar, tasa = 1/(1+z).  b = 0: sin dilatación (tired light).
    b = −1: Ley de la Fila de Cergneux (TC pp. 34, 47): Tm = Tr/(1+z) ⇒ Tr/Tm = 1+z.
    """
    z, rate, sigma = (np.asarray(a, dtype=float) for a in (z, rate, sigma))
    return float(np.sum(((rate - (1 + z) ** (-b)) / sigma) ** 2))


def fit_b_aging(z, rate, sigma, grid=np.arange(-3.0, 5.0, 0.0005)):
    """Mejor b en tasa = (1+z)^(−b) y error 1σ (Δχ² = 1), como en Blondin et al. 2008 §4."""
    chi = np.array([chi2_aging(z, rate, sigma, b) for b in grid])
    i = int(chi.argmin())
    inside = grid[chi <= chi[i] + 1.0]
    return float(grid[i]), float((inside.max() - inside.min()) / 2)


def load_goldhaber_csv(path):
    """Tablas 1-2 de Goldhaber et al. 2001: devuelve (z, w, σ_w) de las SN usadas en su ajuste (58)."""
    with open(path, newline="", encoding="utf-8") as fh:
        rows = [r for r in csv.DictReader(fh) if r["used_in_fit"] == "1"]
    return tuple(np.array([float(r[c]) for r in rows]) for c in ("z", "w", "sigma_w"))


def _linfit(x, y, err):
    wgt = 1.0 / err**2
    a = np.vstack([np.ones_like(x), x]).T
    cov = np.linalg.inv(a.T @ (a * wgt[:, None]))
    par = cov @ (a.T @ (wgt * y))
    return par, np.sqrt(np.diag(cov)), float(np.sum(wgt * (y - a @ par) ** 2))


def intrinsic_scatter(x, y, base_err, scale=1.0):
    """Dispersión intrínseca δ (en cuadratura, ×scale) que lleva χ²/gl a 1 en un ajuste lineal."""
    lo, hi = 0.0, 1.0
    for _ in range(80):
        d = (lo + hi) / 2
        chi = _linfit(x, y, np.sqrt(base_err**2 + (d * scale) ** 2))[2]
        lo, hi = (d, hi) if chi / (len(x) - 2) > 1 else (lo, d)
    return (lo + hi) / 2


def fit_width_slope(z, w, sigma_w):
    """Pendiente dw/dz de w = a + b·z con dispersión intrínseca δ_s·(1+z), como Goldhaber et al. 2001 §IV."""
    d = intrinsic_scatter(z, w, sigma_w, scale=1 + z)
    par, err, _ = _linfit(z, w, np.sqrt(sigma_w**2 + (d * (1 + z)) ** 2))
    return float(par[1]), float(err[1]), float(d)


def fit_width_exponent(z, w, sigma_w):
    """Ajusta ln w = a + b·ln(1+z). Estándar b = +1 (w = s(1+z)); Ley de la Fila b = −1. Devuelve (b, err, δ)."""
    x, y, base = np.log1p(z), np.log(w), sigma_w / w
    d = intrinsic_scatter(x, y, base)
    par, err, _ = _linfit(x, y, np.sqrt(base**2 + d**2))
    return float(par[1]), float(err[1]), float(d)


def chi2_width_fixed_b(z, w, sigma_w, b, delta):
    """χ² de ln w = a + b·ln(1+z) con b fijo y normalización a libre (misma dispersión δ)."""
    x, y = np.log1p(z), np.log(w)
    e = np.sqrt((sigma_w / w) ** 2 + delta**2)
    a = np.sum((y - b * x) / e**2) / np.sum(1 / e**2)
    return float(np.sum(((y - a - b * x) / e) ** 2))


def synthetic(b_true=1.0, n=40, noise=0.05, seed=0):
    """Datos SINTÉTICOS para probar la maquinaria. No son evidencia."""
    rng = np.random.default_rng(seed)
    z = rng.uniform(0.1, 1.0, n)
    ratio = (1 + z) ** b_true * np.exp(rng.normal(0, noise, n))
    return z, ratio, noise * ratio
