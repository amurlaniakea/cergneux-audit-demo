# cergneux-audit

Auditoría ejecutable de las ecuaciones de dos documentos de Ricardo J. Cergneux:

1. *Teoría del Tiempo Cuántico* (versión enero 2025).
2. *Reinterpretación del efecto túnel cuántico a escala macroscópica* (diciembre 2025).

Este repo **no valida** la teoría. Cada ecuación del PDF es una función con su página, y cada afirmación tiene un test que la contrasta con la física estándar. Los tests que revelan problemas se quedan en el repo como resultados.

Las ideas y ecuaciones son de su autor; aquí solo se citan con página y no se reproducen figuras.

## Uso

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -e ".[dev]"
pytest -q
```

Visualizadores (HTML autocontenido, sin dependencias): abre `viz/josephson.html` y `viz/redshift.html` en el navegador.

## Contenido

| Módulo | Qué contrasta |
|---|---|
| `laws.py` | Leyes del Tiempo, Fotón y Luz, aritmética de Mercurio, identidad L_p/T_p = c |
| `cosmology.py` | r_s frente a c/H₀, estiramiento de supernovas, emisividad al conservar energía por bandas |
| `josephson.py` | Niveles transmon, washboard, tasa de escape térmica y cuántica, predicción de T₂ |
| `tdse.py` | Paquete de ondas contra barrera, comparado con la transmisión analítica |

Resultados y páginas en `docs/AUDITORIA.md`.

## Licencia

AGPL-3.0-or-later. Copyright (C) Pedro Sordo Martínez.
