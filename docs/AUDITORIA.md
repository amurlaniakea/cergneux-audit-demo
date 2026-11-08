# Auditoría: resultados

Estado de cada afirmación frente a los tests del repo. «Tiempo Cuántico» = PDF de enero 2025; «Túnel» = PDF de diciembre 2025.

| Afirmación (página) | Resultado | Test |
|---|---|---|
| c = L_p/T_p confirma el movimiento cuántico (TC p. 5) | Identidad por definición de L_p y T_p; no confirma nada | `test_planck_speed_is_c_by_construction` |
| 1/T_p ≈ 1,85487e43 (TC p. 6) | Correcto | `test_ticks_per_second_matches_paper` |
| Gemelos: T₁ = γT₂ (TC pp. 12-14) | Correcto; es la dilatación temporal estándar con otra notación | `test_twin_gamma_two` |
| CMB en r = r_s, ρ → ∞ (TC pp. 32, 48) | Un ρ pequeño exige r ≫ r_s (ρ = 1,1 ⇒ r ≈ 5,76 r_s); no hay regla distancia→r | `test_small_redshift_needs_r_far_beyond_rs` |
| r_s de la masa bariónica = radio del universo observable (TC p. 43) | Identidad: r_s de la masa crítica en la esfera de Hubble es c/H₀ | `test_rs_equals_hubble_radius_is_an_identity` |
| Mercurio: 28,8 km por dilatación temporal (TC pp. 37-38) | La dilatación da ~8 km; 28,8 km es el desfase geométrico de la precesión de la RG | `test_mercury_paper_shift_is_the_precession_not_the_dilation` |
| Supernovas más lejanas duran menos (TC pp. 46-47) | Opuesto al estiramiento (1+z) medido; verificar con datos | `test_sn_stretch_directions_are_opposite` |
| Ley de la Energía: ρ fotones por cada fotón emitido (TC pp. 30-31) | Aplicada a un cuerpo negro da emisividad ρ⁴; FIRAS mide 1 | `test_energy_conservation_claim_gives_rho4_emissivity` |
| ΔD constante (TC p. 10) y ΔD decreciente (TC p. 51) | Contradicción interna del texto | (documental) |
| dn/dt = (E_J sin φ + F)/ħ (Túnel §4.1) | Signo incorrecto: (F − E_J sin φ)/ħ | `test_hamilton_sign_error_in_paper` |
| «n entero ⇒ φ discreta» (Túnel §3.3) | n entero implica φ periódica, no discreta | (documental) |
| Meseta de la tasa de escape a baja T prueba tiempo discreto (Túnel §7) | La explica el túnel con disipación (DMC 1985) | `test_mqt_plateau_below_crossover_without_discrete_time` |
| Test 1: T₂ ~ τ_p·2π/(ΔE/ħ) (Túnel §12) | ~1e-53 s frente a ~1e-4 s medidos | `test_cergneux_t2_prediction_is_absurdly_short` |
| Túnel = salto discreto sin trayectoria continua (TC p. 55, Túnel §7) | El TDSE continuo reproduce la transmisión analítica | `test_wavepacket_transmission_matches_analytic` |

## Pendiente

- Contrastar el estiramiento de supernovas con datos reales (Pantheon+).
- Retícula discreta tipo Planck para el paquete de ondas (dispersión y violación de Lorentz).
- Contactar al autor.
