# SPDX-FileCopyrightText: 2026 Pedro Sordo Martínez <amurlaniakea@gmail.com>
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Paquete de ondas contra barrera rectangular (ħ = m = 1), split-step Fourier."""
import numpy as np


def analytic_transmission(k, v0, a):
    """T(E) rectangular, E = k²/2 (ħ = m = 1)."""
    e = k**2 / 2
    out = np.empty_like(e)
    lo = e < v0
    kap = np.sqrt(2 * (v0 - e[lo]))
    out[lo] = 1 / (1 + v0**2 * np.sinh(kap * a) ** 2 / (4 * e[lo] * (v0 - e[lo])))
    q = np.sqrt(2 * (e[~lo] - v0))
    s = np.sin(q * a) ** 2
    out[~lo] = 1 / (1 + v0**2 * s / (4 * e[~lo] * np.maximum(e[~lo] - v0, 1e-30)))
    return out


def simulate(v0=1.0, a=1.5, k0=1.0, sigma=8.0, x0=-60.0, L=600.0, n=4096, dt=0.02, t_end=130.0):
    x = np.linspace(-L / 2, L / 2, n, endpoint=False)
    dx = x[1] - x[0]
    k = 2 * np.pi * np.fft.fftfreq(n, d=dx)
    mask = (x >= 0) & (x < a)
    a = mask.sum() * dx          # anchura efectiva sobre la rejilla
    v = np.where(mask, v0, 0.0)
    psi = np.exp(-((x - x0) ** 2) / (4 * sigma**2) + 1j * k0 * x)
    psi /= np.sqrt(np.sum(np.abs(psi) ** 2) * dx)
    pk = np.abs(np.fft.fft(psi)) ** 2
    pk /= pk.sum()
    t_avg = float(np.sum(pk * analytic_transmission(np.maximum(np.abs(k), 1e-9), v0, a)))
    half_v = np.exp(-0.5j * v * dt)
    kin = np.exp(-0.5j * k**2 * dt)
    for _ in range(int(t_end / dt)):
        psi = half_v * np.fft.ifft(kin * np.fft.fft(half_v * psi))
    dens = np.abs(psi) ** 2
    t_num = float(np.sum(dens[x > a]) / np.sum(dens))
    return {"x": x, "density": dens, "T_numeric": t_num, "T_analytic_avg": t_avg}
