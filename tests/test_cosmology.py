# SPDX-FileCopyrightText: 2026 Pedro Sordo Martínez <amurlaniakea@gmail.com>
# SPDX-License-Identifier: AGPL-3.0-or-later
import numpy as np
import pytest
from cergneux_audit import cosmology as cos


@pytest.mark.audit(id=5, ref='TC p. 43', claim='r_s de la masa bariónica = radio del universo observable', verdict='identidad',
                   note='r_s de la masa crítica en la esfera de Hubble es c/H₀ por álgebra, no por coincidencia')
def test_rs_equals_hubble_radius_is_an_identity():
    assert cos.rs_over_hubble_radius(67.4) == pytest.approx(1.0, rel=1e-12)


def test_paper_mass_is_the_critical_mass_within_10_percent():
    from cergneux_audit.constants import G, C
    rs = 2 * G * 8.8e52 / C**2
    assert rs == pytest.approx(13.06e25, rel=0.02)
    assert rs == pytest.approx(cos.hubble_radius(67.4), rel=0.10)


@pytest.mark.audit(id=7, ref='TC pp. 46-47', claim='Las supernovas más lejanas duran menos (Tm = Tr/(1+z))', verdict='a-verificar',
                   note='Opuesto al estiramiento (1+z) de la literatura. Ajuste de exponente listo (b=+1 estándar, b=−1 Fila); faltan datos reales en data/')
def test_sn_stretch_directions_are_opposite():
    z = 1.0
    assert cos.sn_stretch_standard(z) == pytest.approx(2.0)
    assert cos.sn_stretch_cergneux(z) == pytest.approx(0.5)
    # Observaciones (Goldhaber+2001, Blondin+2008, a verificar con los datos): anchura ∝ (1+z).


@pytest.mark.audit(id=8, ref='TC pp. 30-31', claim='Ley de la Energía: ρ fotones por cada fotón emitido', verdict='discrepa',
                   note='Aplicada a un cuerpo negro da emisividad ρ⁴; FIRAS mide 1')
def test_energy_conservation_claim_gives_rho4_emissivity():
    rho = 10.0
    assert cos.energy_conserving_emissivity(rho) == pytest.approx(rho**4, rel=0.02)


def test_luminosity_distance_monotonic():
    d = cos.luminosity_distance(np.array([0.1, 0.5, 1.0, 2.0]))
    assert np.all(np.diff(d) > 0)
