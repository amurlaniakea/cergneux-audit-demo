# SPDX-FileCopyrightText: 2026 Pedro Sordo Martínez <amurlaniakea@gmail.com>
# SPDX-License-Identifier: AGPL-3.0-or-later
import numpy as np
import pytest
from cergneux_audit import cosmology as cos


def test_rs_equals_hubble_radius_is_an_identity():
    assert cos.rs_over_hubble_radius(67.4) == pytest.approx(1.0, rel=1e-12)


def test_paper_mass_is_the_critical_mass_within_10_percent():
    from cergneux_audit.constants import G, C
    rs = 2 * G * 8.8e52 / C**2
    assert rs == pytest.approx(13.06e25, rel=0.02)
    assert rs == pytest.approx(cos.hubble_radius(67.4), rel=0.10)


def test_sn_stretch_directions_are_opposite():
    z = 1.0
    assert cos.sn_stretch_standard(z) == pytest.approx(2.0)
    assert cos.sn_stretch_cergneux(z) == pytest.approx(0.5)
    # Observaciones (Goldhaber+2001, Blondin+2008, a verificar con los datos): anchura ∝ (1+z).


def test_energy_conservation_claim_gives_rho4_emissivity():
    rho = 10.0
    assert cos.energy_conserving_emissivity(rho) == pytest.approx(rho**4, rel=0.02)


def test_luminosity_distance_monotonic():
    d = cos.luminosity_distance(np.array([0.1, 0.5, 1.0, 2.0]))
    assert np.all(np.diff(d) > 0)
