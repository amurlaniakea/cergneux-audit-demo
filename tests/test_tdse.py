# SPDX-FileCopyrightText: 2026 Pedro Sordo Martínez <amurlaniakea@gmail.com>
# SPDX-License-Identifier: AGPL-3.0-or-later
import pytest
from cergneux_audit import tdse


def test_wavepacket_transmission_matches_analytic():
    r = tdse.simulate()
    assert r["T_numeric"] == pytest.approx(r["T_analytic_avg"], rel=0.03)
    assert 0 < r["T_numeric"] < 0.5
