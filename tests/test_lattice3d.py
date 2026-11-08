# SPDX-FileCopyrightText: 2026 Pedro Sordo Martínez <amurlaniakea@gmail.com>
# SPDX-License-Identifier: AGPL-3.0-or-later
import numpy as np
import pytest
from cergneux_audit import lattice3d as l3
from cergneux_audit.constants import E


@pytest.mark.audit(id=17, ref='TC pp. 4-6', claim='La luz avanza una celda de Planck por tick en cualquier dirección de una retícula cúbica (c isótropa)',
                   verdict='discrepa', note='Literal en retícula cúbica la velocidad varía un 42 % entre ejes y diagonales (1/√3 a 1, o 1 a √3); las pruebas de isotropía de c llegan a ~1e-17')
def test_cubic_lattice_light_is_anisotropic_at_order_one():
    assert float(l3.axis_move_speed([1, 0, 0])) == pytest.approx(1.0)
    assert float(l3.axis_move_speed([1, 1, 1])) == pytest.approx(1 / np.sqrt(3))
    assert float(l3.king_move_speed([1, 1, 1])) == pytest.approx(np.sqrt(3))
    for fn in (l3.axis_move_speed, l3.king_move_speed):
        spread = l3.speed_spread(fn)
        assert spread == pytest.approx(1 - 1 / np.sqrt(3), abs=1e-3)
        assert spread / l3.LAB_ISOTROPY_LIMIT > 1e16         # >16 órdenes por encima de la cota de laboratorio


@pytest.mark.audit(id=18, ref='TC pp. 4-6', claim='Una retícula espacial de Planck es compatible con las cotas de dispersión de la luz',
                   verdict='coincide', note='Dispersión cuadrática v≈1−(ka)²/8 ⇒ E_QG,2≈3,5 E_P ≈ 4e19 GeV, muy por encima de la cota de Fermi-LAT (1,3e11 GeV): compatible con las cotas y no detectable hoy')
def test_spatial_lattice_dispersion_is_far_above_grb_bound():
    ka = 1e-3
    assert float(l3.kg_group_speed_axis(ka)) == pytest.approx(1 - ka**2 / 8, rel=1e-6)
    k = np.array([0.02, 0.0, 0.0])
    assert float(l3.kg_omega(k)) == pytest.approx(float(np.linalg.norm(k)) * (1 - 0.02**2 / 24), rel=1e-6)
    assert l3.eqg2_in_planck_energies() == pytest.approx(np.sqrt(12))
    assert l3.eqg2_gev() / l3.GRB_EQG2_LIMIT_GEV > 1e8
    assert l3.eqg2_gev() > 1e19
