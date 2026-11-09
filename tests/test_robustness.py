# SPDX-FileCopyrightText: 2026 Pedro Sordo Martínez <amurlaniakea@gmail.com>
# SPDX-License-Identifier: AGPL-3.0-or-later
import warnings
import numpy as np
import pytest
from cergneux_audit import cosmology as cos, lattice as lt, tdse


def test_transmission_at_zero_energy_has_no_warning_and_vanishes():
    with warnings.catch_warnings():
        warnings.simplefilter("error")
        t = tdse.analytic_transmission(np.array([0.0, 1e-9, 0.3]), 1.0, 1.5)
    assert t[0] < 1e-20 and 0 <= t[2] <= 1


def test_redshift_domain_is_validated():
    for fn in (cos.sn_stretch_standard, cos.sn_stretch_cergneux, cos.observed_duration_ley_del_tiempo):
        with pytest.raises(ValueError):
            fn(-1.0)
        with pytest.raises(ValueError):
            fn(-2.0)
    assert float(cos.sn_stretch_cergneux(0.0)) == 1.0


def test_massless_group_velocity_is_exactly_one_including_small_k():
    k = np.array([0.0, 1e-12, 1e-6, 0.5, 3.0])
    assert np.allclose(lt.group_velocity(k, 0.0), 1.0, rtol=0, atol=1e-15)
    assert float(lt.group_velocity(0.0, 0.3)) == 0.0            # con masa y k = 0: en reposo


def test_dispersion_is_stable_for_tiny_arguments():
    w = float(lt.dispersion(1e-9, 0.0))
    assert w == pytest.approx(1e-9, rel=1e-12)                  # arccos(cos k) daría ruido de redondeo


def test_comoving_distance_matches_einstein_de_sitter_analytic():
    # Ω_m = 1: d_C = 2 (c/H0) (1 − 1/√(1+z)), exacta
    for z in (0.5, 2.0, 10.0, 1090.0):
        exact = 2 * cos.hubble_radius(67.4) * (1 - 1 / np.sqrt(1 + z))
        assert float(cos.comoving_distance(z, om=1.0)[0]) == pytest.approx(exact, rel=1e-6)
