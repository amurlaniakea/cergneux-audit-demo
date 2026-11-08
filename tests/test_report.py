# SPDX-FileCopyrightText: 2026 Pedro Sordo Martínez <amurlaniakea@gmail.com>
# SPDX-License-Identifier: AGPL-3.0-or-later
import pytest
from cergneux_audit.report import DOCUMENTAL, Record, render


def _rec(i, status="passed", verdict="coincide"):
    return Record(i, "p. 1", "afirmación", verdict, "nota", f"test_{i}", status)


def test_render_is_deterministic_and_sorted():
    a = render([_rec(2), _rec(1)])
    assert a == render([_rec(1), _rec(2)])
    assert a.index("| 1 |") < a.index("| 2 |")


def test_failed_test_is_reported_as_failure_not_verdict():
    assert "🚨 FALLA" in render([_rec(1, status="failed")])


def test_duplicate_ids_rejected():
    with pytest.raises(ValueError):
        render([_rec(1), _rec(1)])


def test_documental_claims_are_included():
    out = render([])
    assert all(f"| {d['id']} |" in out for d in DOCUMENTAL)
