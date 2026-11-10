# Cómo contribuir

Gracias por el interés. Este repo audita las ecuaciones de dos documentos de Ricardo J. Cergneux; las ideas son suyas y se citan página por página. Se aceptan correcciones, sobre todo si una lectura de sus ecuaciones es incorrecta.

## Quiero corregir una lectura de las ecuaciones
Abre una *issue* con la plantilla **«Corrección de una lectura»**. Indica la página, qué ecuación crees que está mal interpretada y cómo debería leerse. Si tienes razón, se corrige el test y se actualiza `docs/AUDITORIA.md`.

## Quiero reportar un error o proponer una mejora
Abre una *issue* con:
- qué esperabas y qué ocurrió (con el comando y la salida de `pytest -q`),
- tu versión de Python y de NumPy.

## Quiero enviar código
1. Haz un *fork*, crea una rama y escribe tu cambio con un test.
2. Cada afirmación auditada lleva el marcador:
   ```python
   @pytest.mark.audit(id=21, ref='TC p. N', claim='…', verdict='discrepa|coincide|identidad|a-verificar', note='…')
   ```
   El `id` debe ser único. Las afirmaciones sin test ejecutable van en `DOCUMENTAL`, dentro de `src/cergneux_audit/report.py`.
3. Regenera el informe, que **no se edita a mano**:
   ```bash
   pytest -q --audit-report docs/AUDITORIA.md
   ```
   El CI falla si `docs/AUDITORIA.md` no coincide con los tests.
4. Los archivos `.py` llevan cabecera SPDX (`AGPL-3.0-or-later`) y la atribución «Pedro Sordo Martínez».
5. Abre el *pull request* explicando qué cambia y por qué.

## Reglas para datos de la literatura
- Cita la fuente exacta (artículo, tabla) en `data/README.md`.
- Valida cada transcripción reproduciendo en un test algún resultado publicado del propio artículo.
- No uses datos sin fuente ni sin error (por ejemplo, valores «redondos» que coincidan exactamente con la fórmula que se quiere contrastar).
- No uses parámetros que ya asuman lo que se contrasta (como el estiramiento `s` de SALT2 o `s = w/(1+z)` para probar el factor (1+z)).

## Tono
El repo critica ecuaciones, no personas. Los veredictos son la tesis del autor del repo; un test que pasa indica que la evidencia es reproducible, no que el veredicto sea definitivo.
