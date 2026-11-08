# SPDX-FileCopyrightText: 2026 Pedro Sordo Martínez <amurlaniakea@gmail.com>
# SPDX-License-Identifier: AGPL-3.0-or-later
import numpy as np
import pytest
from cergneux_audit import lattice as lt
from cergneux_audit.constants import E


@pytest.mark.audit(id=15, ref='TC pp. 5-6', claim='El fotón avanza una celda de Planck por tick (c = ℓ_p/T_p) y las partículas con masa son más lentas',
                   verdict='coincide', note='Realizable como paseo cuántico discreto 1D: v=1 exacta sin masa, v<1 con masa; el paquete simulado lo confirma')
def test_lattice_walk_reproduces_postulated_speeds():
    ks = np.linspace(0.05, 3.0, 25)
    assert np.allclose(lt.group_velocity(ks, 0.0), 1.0)                # luz: 1 celda/tick para todo k
    assert np.all(lt.group_velocity(ks, 0.3) < 1.0)                    # con masa: más lenta
    assert lt.eigen_omega(0.7, 0.4) == pytest.approx(float(lt.dispersion(0.7, 0.4)), abs=1e-12)
    for k0, theta in ((0.5, 0.0), (0.5, 0.4), (1.0, 0.3)):             # simulación = velocidad de grupo
        assert lt.simulate_walk(k0, theta) == pytest.approx(float(lt.group_velocity(k0, theta)), abs=2e-3)


@pytest.mark.audit(id=16, ref='TC pp. 4-6, 12', claim='Una retícula de Planck es compatible con la invariancia de Lorentz macroscópica',
                   verdict='a-verificar', note='Modelo 1D: la desviación escala como (E/E_P)² y es ínfima a energías accesibles; no prueba la anisotropía 3D ni la simultaneidad universal')
def test_lattice_lorentz_violation_scales_as_lambda_squared():
    k, th = 0.04, 0.03
    exact = float(lt.relative_deviation(k, th))
    assert exact == pytest.approx(float(lt.relative_deviation_series(k, th)), rel=0.02)
    ratio = float(lt.relative_deviation(k, th)) / float(lt.relative_deviation(k / 2, th / 2))
    assert ratio == pytest.approx(4.0, rel=0.05)                       # k, θ → λk, λθ  ⇒  δ ∝ λ²
    proton = lt.physical_deviation(7e12 * E, 938.272e6 * E)             # 7 TeV, protón
    assert abs(proton) < 1e-30
