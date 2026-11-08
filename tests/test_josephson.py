# SPDX-FileCopyrightText: 2026 Pedro Sordo Martínez <amurlaniakea@gmail.com>
# SPDX-License-Identifier: AGPL-3.0-or-later
import numpy as np
import pytest
from cergneux_audit import josephson as j
from cergneux_audit.constants import TP

I0, C, RATIO = 9.489e-6, 6.35e-12, 0.97


def test_transmon_anharmonicity_negative_and_small():
    e = j.transmon_levels(ej=50.0, ec=1.0)
    w01, w12 = e[1] - e[0], e[2] - e[1]
    assert w12 < w01
    assert (w12 - w01) == pytest.approx(-1.0, abs=0.15)   # ≈ −E_C


@pytest.mark.audit(id=10, ref='Túnel §4.1', claim='dn/dt = (E_J sin φ + F)/ħ', verdict='discrepa',
                   note='Contradice su propia ecuación dn/dt = −(1/ħ)∂H/∂φ: el signo correcto es (F − E_J sin φ)/ħ')
def test_hamilton_sign_error_in_paper():
    phi, ej, f, h = 0.3, 1.0, 0.2, 1e-6
    energy = lambda p: -ej * np.cos(p) - f * p                      # parte de H que depende de φ
    exact = -(energy(phi + h) - energy(phi - h)) / (2 * h)           # −∂H/∂φ numérico (ħ = 1)
    assert j.dn_dt_standard(phi, ej, f, hbar=1) == pytest.approx(exact, rel=1e-6)
    assert j.dn_dt_paper(phi, ej, f, hbar=1) != pytest.approx(exact, rel=1e-6)
    # sin sesgo (F = 0) el PDF da exactamente el signo contrario
    std0, paper0 = j.dn_dt_standard(phi, ej, 0.0, hbar=1), j.dn_dt_paper(phi, ej, 0.0, hbar=1)
    assert std0 < 0 < paper0
    assert paper0 == pytest.approx(-std0)


@pytest.mark.audit(id=12, ref='Túnel §7', claim='La meseta de la tasa de escape a baja T prueba tiempo discreto', verdict='discrepa',
                   note='La explica el túnel con disipación (Devoret-Martinis-Clarke 1985)')
def test_mqt_plateau_below_crossover_without_discrete_time():
    tcr = j.crossover_temperature(I0, C, RATIO)
    gq = j.escape_rate_quantum(I0, C, RATIO)
    assert j.escape_rate(I0, C, RATIO, 0.2 * tcr) == pytest.approx(gq)
    assert j.escape_rate(I0, C, RATIO, 0.05 * tcr) == pytest.approx(gq)
    assert j.escape_rate_thermal(I0, C, RATIO, 0.2 * tcr) < 1e-3 * gq
    assert j.escape_rate(I0, C, RATIO, 3 * tcr) > gq


def test_crossover_in_millikelvin_range():
    tcr = j.crossover_temperature(I0, C, RATIO)
    assert 0.005 < tcr < 0.2   # K


@pytest.mark.audit(id=13, ref='Túnel §12', claim='Test 1: T₂ ~ τ_p·2π/(ΔE/ħ)', verdict='discrepa',
                   note='~1e-53 s frente a ~1e-4 s medidos')
def test_cergneux_t2_prediction_is_absurdly_short():
    t2 = j.cergneux_t2(5e9)
    assert t2 == pytest.approx(TP / 5e9)
    assert t2 < 1e-50
    assert 100e-6 / t2 > 1e45
