# Datos

## `blondin2008_table3.csv`
Tabla 3 de Blondin et al. 2008, *Time Dilation in Type Ia Supernova Spectra at High Redshift*, ApJ 682, 724
([arXiv:0804.3595](https://arxiv.org/abs/0804.3595)): 22 supernovas Ia cercanas y 13 lejanas (0,28 ≤ z ≤ 0,62).

- `aging_rate`: pendiente de Δt_reposo frente a Δt_observado, medida con espectros. Esperado: 1/(1+z).
- `sigma`: error de `aging_rate`. `sample`: `low` (z < 0,04) o `high` (z > 0,2).
- Transcrita a mano desde el PDF del artículo. Los tests la validan reproduciendo sus resultados publicados
  (χ² = 27,0 con 35 gl para 1/(1+z); χ² = 150,3 sin dilatación; b = 0,97 ± 0,10).

Por qué espectros y no parámetros de curva de luz como x1 de SALT2 (Pantheon+): SALT2 ya modela las curvas en el
sistema en reposo suponiendo la dilatación (1+z), así que ajustarlo frente a z sería circular. Blondin et al. explican
además que la anchura de la curva de luz se confunde con la luminosidad intrínseca (relación de Phillips).
