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


def synthetic(b_true=1.0, n=40, noise=0.05, seed=0):
    """Datos SINTÉTICOS para probar la maquinaria. No son evidencia."""
    rng = np.random.default_rng(seed)
    z = rng.uniform(0.1, 1.0, n)
    ratio = (1 + z) ** b_true * np.exp(rng.normal(0, noise, n))
    return z, ratio, noise * ratio
