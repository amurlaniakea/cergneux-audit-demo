# Registro de cambios

Formato basado en [Keep a Changelog](https://keepachangelog.com/es-ES/1.1.0/). Las cifras de tests son las de la suite en cada versión.

## [0.2.1] - 2026-11-10

36 tests.

### Añadido
- Fila 20 de la auditoría: la Ley del Tiempo (Tₑ = Tᵣ/ρ) y la Ley de la Fila no son coherentes entre sí; aplicada a un proceso de duración propia fija, la Ley del Tiempo da un estiramiento (1+z), que coincide con los datos.
- `tests/test_robustness.py` (casos límite numéricos), `CITATION.cff`, este registro, `CONTRIBUTING.md` y una plantilla de *issue* para corregir lecturas de las ecuaciones.

### Cambiado
- Fila 4: de «discrepa» a «a verificar» (si la fórmula de Schwarzschild solo vale en el límite del CMB, el PDF no da ρ(d) para corrimientos intermedios).
- `comoving_distance` integra en ln(1+z) y se valida contra el caso analítico de Einstein-de Sitter.
- `lattice.py`: fórmulas estables (`atan2`); la velocidad de grupo sin masa es exactamente 1, incluso para k pequeño y k = 0.
- README: sin tabla duplicada (enlaza a `docs/AUDITORIA.md`), secciones «Cómo citar» y «Cómo contribuir».
- La versión del paquete pasa a 0.2.1 (declaraba 0.1.0).

### Corregido
- `tdse.analytic_transmission`: sin `RuntimeWarning` para E → 0.
- `sn_stretch_*`, `observed_duration_*`, `comoving_distance`: lanzan `ValueError` si z ≤ −1.

## [0.2.0] - 2026-11-09

30 tests.

### Añadido
- `docs/AUDITORIA.md` generado por pytest (`--audit-report`) y comprobación de sincronía en CI.
- Contraste con datos reales de supernovas Ia: envejecimiento espectral (Blondin et al. 2008, Tabla 3, 35 SN) y anchuras de curvas de luz (Goldhaber et al. 2001, Tablas 1-2, 58 SN); filas 7 y 19.
- `lattice.py` (paseo cuántico 1D) y `lattice3d.py` (retícula cúbica 3D y cotas de Fermi-LAT y de isotropía); filas 15-18; visualizador `viz/lattice.html`.

### Cambiado
- El test del signo del hamiltoniano Josephson compara con la derivada numérica de H.

## [0.1.0] - 2026-11-08

18 tests.

### Añadido
- Primera versión pública: leyes del Tiempo Cuántico (`laws.py`), cosmología, circuito Josephson, paquete de ondas contra barrera, visualizadores `josephson.html` y `redshift.html`, README didáctico, CI y licencia AGPL-3.0-or-later.

[0.2.1]: https://github.com/amurlaniakea/cergneux-audit-demo/releases/tag/v0.2.1
