# SPDX-FileCopyrightText: 2026 Pedro Sordo Martínez <amurlaniakea@gmail.com>
# SPDX-License-Identifier: AGPL-3.0-or-later
from pathlib import Path
import pytest
from cergneux_audit import sn_stretch as sn

TABLE3 = Path(__file__).resolve().parent.parent / "data" / "blondin2008_table3.csv"


def test_fit_recovers_exponent_and_discriminates_models():
    """Prueba de la maquinaria con datos sintéticos (no es evidencia): recupera b y separa ±1."""
    for b_true in (1.0, -1.0):
        b, err = sn.fit_exponent(*sn.synthetic(b_true=b_true))
        assert abs(b - b_true) < 4 * err
        assert abs(b + b_true) > 20 * err


@pytest.mark.audit(id=7, ref='TC pp. 34, 46-47', claim='Las supernovas más lejanas duran menos (Tm = Tr/(1+z))', verdict='discrepa',
                   note='Datos reales (Blondin et al. 2008, Tabla 3, 35 SN): χ²≈27 para el estándar 1/(1+z) y ≈796 para la Ley de la Fila; exponente b=0,97±0,10 (la Fila exige b=−1)')
def test_real_data_contradict_ley_de_la_fila():
    z, rate, sig, high = sn.load_aging_csv(TABLE3)
    assert len(z) == 35 and high.sum() == 13
    # reproduce los números publicados (valida la transcripción de la tabla)
    assert sn.chi2_aging(z, rate, sig, 1) == pytest.approx(27.0, abs=0.5)      # paper: 27.0 / 35 gl
    assert sn.chi2_aging(z, rate, sig, 0) == pytest.approx(150.3, abs=1.0)     # sin dilatación: 150.3
    b, err = sn.fit_b_aging(z, rate, sig)
    assert b == pytest.approx(0.97, abs=0.02) and err == pytest.approx(0.10, abs=0.01)
    # la Ley de la Fila (b = −1) queda descartada
    assert sn.chi2_aging(z, rate, sig, -1) > 500
    assert abs(b - (-1)) > 15 * err
