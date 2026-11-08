# SPDX-License-Identifier: AGPL-3.0-or-later
# Copyright (C) Pedro Sordo Martínez
"""Constantes CODATA 2018 (SI)."""
import math

C = 299_792_458.0
G = 6.67430e-11
H = 6.62607015e-34
HBAR = H / (2 * math.pi)
KB = 1.380649e-23
E = 1.602176634e-19
PHI0 = H / (2 * E)
GM_SUN = 1.32712440018e20
MPC = 3.0856775814913673e22

LP = math.sqrt(G * HBAR / C**3)   # longitud de Planck
TP = math.sqrt(G * HBAR / C**5)   # tiempo de Planck
