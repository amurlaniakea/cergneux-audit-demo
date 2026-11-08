# Datos reales de estiramiento de supernovas Ia

Aquí va `sn_stretch.csv` cuando se disponga de datos reales. Sin ese archivo, `test_real_data_exponent` se omite.

Formato (con cabecera):

```
z,width_ratio,sigma
0.35,1.38,0.06
```

- `width_ratio`: anchura **observada** de la curva de luz dividida por la anchura **en reposo** de una referencia local.
- `sigma`: error de `width_ratio`.
- Los números de arriba son un ejemplo de formato, no datos.

Advertencia: no sirve el parámetro `x1` de SALT2 (p. ej. en Pantheon+): SALT2 ya modela las curvas en el sistema en reposo
suponiendo la dilatación (1+z), así que ajustarlo frente a z sería circular. Hacen falta anchuras en el sistema del
observador (Goldhaber et al. 2001, ApJ 558, 359) o envejecimiento espectral (Blondin et al. 2008, ApJ 682, 724).
Anota en el CSV la fuente y comprueba cada cifra contra la tabla del artículo antes de usarla.
