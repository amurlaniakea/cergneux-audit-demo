# SPDX-FileCopyrightText: 2026 Pedro Sordo Martínez <amurlaniakea@gmail.com>
# SPDX-License-Identifier: AGPL-3.0-or-later
from pathlib import Path
import pytest
from cergneux_audit import sn_stretch as sn

DATA = Path(__file__).resolve().parent.parent / "data" / "sn_stretch.csv"


def test_fit_recovers_exponent_and_discriminates_models():
    """Prueba de la maquinaria con datos sintéticos (no es evidencia): recupera b y separa ±1."""
    for b_true in (1.0, -1.0):
        b, err = sn.fit_exponent(*sn.synthetic(b_true=b_true))
        assert abs(b - b_true) < 4 * err
        assert abs(b + b_true) > 20 * err   # el modelo contrario queda a >20σ


@pytest.mark.skipif(not DATA.exists(), reason="faltan datos reales: ver data/README.md")
def test_real_data_exponent():
    """Con datos reales, el exponente debe quedar cerca de +1 (estándar) y lejos de −1 (Fila)."""
    b, err = sn.fit_exponent(*sn.load_csv(DATA))
    assert abs(b - 1) < 4 * err
    assert abs(b + 1) > 10 * err
