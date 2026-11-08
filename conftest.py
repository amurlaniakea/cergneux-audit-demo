# SPDX-FileCopyrightText: 2026 Pedro Sordo Martínez <amurlaniakea@gmail.com>
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Plugin local: recoge los marcadores @pytest.mark.audit y escribe el informe con --audit-report."""
from pathlib import Path
import pytest
from cergneux_audit.report import Record, render


def pytest_addoption(parser):
    parser.addoption("--audit-report", action="store", default=None, metavar="RUTA",
                     help="escribe el informe de auditoría en Markdown en RUTA")


def pytest_configure(config):
    config.addinivalue_line(
        "markers", "audit(id, ref, claim, verdict, note=''): metadatos de la afirmación auditada por este test")
    config._audit_records = []
    config._audit_deselected = 0


def pytest_deselected(items):
    for it in items:
        if it.get_closest_marker("audit"):
            it.config._audit_deselected += 1


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    m = item.get_closest_marker("audit")
    if not m:
        return
    if rep.when == "call" or (rep.when == "setup" and rep.outcome != "passed"):
        k = m.kwargs
        item.config._audit_records.append(Record(
            id=k["id"], ref=k["ref"], claim=k["claim"], verdict=k["verdict"], note=k.get("note", ""),
            test=item.name, status=rep.outcome))


def pytest_sessionfinish(session, exitstatus):
    path = session.config.getoption("--audit-report")
    if not path:
        return
    if session.config._audit_deselected:
        print("\n[audit] informe NO escrito: hay tests de auditoría deseleccionados (-k/-m).")
        return
    Path(path).write_text(render(session.config._audit_records), encoding="utf-8")
    print(f"\n[audit] informe escrito en {path}")
