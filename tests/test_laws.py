# SPDX-FileCopyrightText: 2026 Pedro Sordo Martínez <amurlaniakea@gmail.com>
# SPDX-License-Identifier: AGPL-3.0-or-later
import pytest
from cergneux_audit import laws
from cergneux_audit.constants import C


@pytest.mark.audit(id=1, ref='TC p. 5', claim='c = L_p/T_p confirma el movimiento cuántico', verdict='identidad',
                   note='Identidad por definición de L_p y T_p; no confirma nada')
def test_planck_speed_is_c_by_construction():
    assert laws.planck_speed() == pytest.approx(C, rel=1e-12)


@pytest.mark.audit(id=2, ref='TC p. 6', claim='1/T_p ≈ 1,85487e43 movimientos por segundo', verdict='coincide',
                   note='Valor numérico correcto')
def test_ticks_per_second_matches_paper():
    assert laws.planck_ticks_per_second() == pytest.approx(1.85487e43, rel=1e-4)


@pytest.mark.audit(id=3, ref='TC pp. 12-14', claim='Gemelos: T₁ = γ·T₂ con v = 0,866 c', verdict='coincide',
                   note='Es la dilatación temporal estándar con otra notación')
def test_twin_gamma_two():
    assert float(laws.gamma(0.8660254 * C)) == pytest.approx(2.0, rel=1e-6)


def test_rho_schwarzschild_diverges_at_rs():
    assert laws.r_over_rs_for_rho(1090.0) == pytest.approx(1.0, abs=1e-6)


@pytest.mark.audit(id=4, ref='TC pp. 32, 48', claim='CMB en r = r_s con ρ → ∞', verdict='discrepa',
                   note='Un ρ pequeño exige r ≫ r_s (ρ = 1,1 ⇒ r ≈ 5,76 r_s); no hay regla distancia → r')
def test_small_redshift_needs_r_far_beyond_rs():
    # ρ = 1.1  ⇒  r ≈ 5.76 r_s: más lejos que el «borde» r = r_s donde el PDF pone el CMB
    assert float(laws.r_over_rs_for_rho(1.1)) == pytest.approx(5.76, abs=0.01)


def test_mercury_clock_gap_close_to_paper():
    m = laws.mercury_numbers()
    assert m["clock_gap_ns_per_s"] == pytest.approx(m["paper_clock_gap_ns_per_s"], rel=0.10)


@pytest.mark.audit(id=6, ref='TC pp. 37-38', claim='Mercurio: 28,8 km de desfase por dilatación temporal', verdict='discrepa',
                   note='La dilatación da ~8 km; 28,8 km es el desfase geométrico de la precesión de la RG')
def test_mercury_paper_shift_is_the_precession_not_the_dilation():
    """El desfase de 28,8 km del PDF coincide con la precesión de la RG (~29 km),
    pero la dilatación temporal que invoca da ~8 km: no se deriva de ella."""
    m = laws.mercury_numbers()
    assert m["shift_from_precession_km"] == pytest.approx(m["paper_shift_km"], rel=0.05)
    assert m["shift_from_dilation_km"] < m["paper_shift_km"] / 3
    assert 3.0 < m["ratio_precession_to_dilation"] < 3.8
