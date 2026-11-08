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


def test_hamilton_sign_error_in_paper():
    phi, ej, f = 0.3, 1.0, 0.2
    assert j.dn_dt_standard(phi, ej, f, hbar=1) == pytest.approx(f - ej * np.sin(phi))
    assert j.dn_dt_paper(phi, ej, f, hbar=1) != pytest.approx(j.dn_dt_standard(phi, ej, f, hbar=1))


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


def test_cergneux_t2_prediction_is_absurdly_short():
    t2 = j.cergneux_t2(5e9)
    assert t2 == pytest.approx(TP / 5e9)
    assert t2 < 1e-50
    assert 100e-6 / t2 > 1e45
