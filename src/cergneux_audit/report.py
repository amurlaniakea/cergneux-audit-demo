# SPDX-FileCopyrightText: 2026 Pedro Sordo Martínez <amurlaniakea@gmail.com>
# SPDX-License-Identifier: AGPL-3.0-or-later
"""Generador de docs/AUDITORIA.md a partir de los veredictos marcados en los tests.

Cada test que audita una afirmación lleva @pytest.mark.audit(id=…, ref=…, claim=…, verdict=…, note=…).
El informe solo se escribe si todos esos tests se ejecutaron y se refleja su resultado real
(un test que falla aparece como FALLA, no como veredicto). Salida determinista: sin fechas.
"""
from dataclasses import dataclass

VERDICTS = {
    "coincide": "✅ Coincide",
    "identidad": "ℹ️ Identidad",
    "discrepa": "❌ Discrepa",
    "a-verificar": "⚠️ A verificar",
    "documental": "📄 Documental",
}

# Afirmaciones auditadas por lectura, sin test ejecutable (se mantienen aquí, versionadas).
DOCUMENTAL = [
    {"id": 9, "ref": "TC pp. 10, 51", "verdict": "documental", "test": "—",
     "claim": "ΔD constante e invariable (p. 10) y ΔD decreciente en el tiempo (p. 51)",
     "note": "Contradicción interna del texto"},
    {"id": 11, "ref": "Túnel §3.3", "verdict": "documental", "test": "—",
     "claim": "«n entero ⇒ φ discreta»",
     "note": "n entero implica φ periódica (compacta), no discreta"},
]


@dataclass(frozen=True)
class Record:
    id: int
    ref: str
    claim: str
    verdict: str
    note: str
    test: str
    status: str  # "passed" | "failed" | "skipped"


def _cell(text):
    return str(text).replace("|", "\\|").replace("\n", " ")


def render(records, documental=DOCUMENTAL):
    rows = [r for r in records] + [
        Record(d["id"], d["ref"], d["claim"], d["verdict"], d["note"], d["test"], "n/a") for d in documental
    ]
    ids = [r.id for r in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("ids de afirmación duplicados: " + str(sorted(i for i in ids if ids.count(i) > 1)))
    rows.sort(key=lambda r: r.id)
    counts = {}
    for r in rows:
        key = "FALLA" if r.status in ("failed", "skipped") else VERDICTS[r.verdict]
        counts[key] = counts.get(key, 0) + 1
    out = [
        "# Auditoría: resultados",
        "",
        "> Archivo **generado** con `pytest --audit-report docs/AUDITORIA.md`. No lo edites a mano: "
        "cambia los marcadores `@pytest.mark.audit` de los tests o `DOCUMENTAL` en `src/cergneux_audit/report.py`.",
        "",
        "«TC» = *Teoría del Tiempo Cuántico* (ene. 2025); «Túnel» = *Reinterpretación del efecto túnel* (dic. 2025).",
        "",
        "**Resumen:** " + " · ".join(f"{k}: {v}" for k, v in counts.items()),
        "",
        "| # | Afirmación | Página | Veredicto | Detalle | Test |",
        "|---|---|---|---|---|---|",
    ]
    for r in rows:
        verdict = "🚨 FALLA el test" if r.status in ("failed", "skipped") else VERDICTS[r.verdict]
        test = f"`{r.test}`" if r.test != "—" else "—"
        out.append(f"| {r.id} | {_cell(r.claim)} | {_cell(r.ref)} | {verdict} | {_cell(r.note)} | {test} |")
    out += ["", "El veredicto es la tesis del autor del repo; que el test pase significa que la evidencia es reproducible.", ""]
    return "\n".join(out)
