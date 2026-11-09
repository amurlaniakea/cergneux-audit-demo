# SPDX-FileCopyrightText: 2026 Pedro Sordo Martínez <amurlaniakea@gmail.com>
# SPDX-License-Identifier: AGPL-3.0-or-later
from pathlib import Path
import pytest
from cergneux_audit import sn_stretch as sn

DATA = Path(__file__).resolve().parent.parent / "data"
TABLE3 = DATA / "blondin2008_table3.csv"
GOLDHABER = DATA / "goldhaber2001_tables12.csv"


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


@pytest.mark.audit(id=19, ref='TC pp. 34, 46-47', claim='Las curvas de luz de supernovas lejanas se ven más estrechas (w = s/(1+z))', verdict='discrepa',
                   note='Muestra independiente (Goldhaber et al. 2001, 58 SN, curvas de luz): ln w = a + b·ln(1+z) da b≈1,08±0,07; la Fila exige b=−1 (>25σ), χ²≈857 frente a ≈57')
def test_goldhaber_light_curve_widths_contradict_fila():
    z, w, sig = sn.load_goldhaber_csv(GOLDHABER)
    assert len(z) == 58
    # reproduce los resultados publicados (valida la transcripción de las tablas)
    slope, err, delta = sn.fit_width_slope(z, w, sig)
    assert slope == pytest.approx(1.07, abs=0.10) and err == pytest.approx(0.06, abs=0.03)   # paper: 1,07 ± 0,06
    assert delta == pytest.approx(0.08, abs=0.02)                                             # δ_s ≈ 0,08
    # la anchura w observada crece como (1+z): b = +1 (estándar), no −1 (Fila)
    b, berr, d = sn.fit_width_exponent(z, w, sig)
    assert abs(b - 1) < 3 * berr
    assert abs(b + 1) > 20 * berr
    assert sn.chi2_width_fixed_b(z, w, sig, -1, d) > 500
    assert sn.chi2_width_fixed_b(z, w, sig, 1, d) < 80      # ≈ 57 con 57 gl


def test_goldhaber_table_structure():
    import csv
    rows = list(csv.DictReader(open(GOLDHABER, encoding="utf-8")))
    assert sum(r["sample"] == "SCP" for r in rows) == 42 and sum(r["sample"] == "CT" for r in rows) == 18
    assert sorted(r["sn"] for r in rows if r["comment"]) == sorted(["1994G", "1996cl", "1997G", "1997I", "1997N", "1997O", "1997ap"])
    assert all(abs(float(r["w"]) / (1 + float(r["z"])) - float(r["s"])) < 0.01 for r in rows)   # s = w/(1+z)
