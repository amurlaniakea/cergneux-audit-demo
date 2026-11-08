# Auditoría: resultados

> Archivo **generado** con `pytest --audit-report docs/AUDITORIA.md`. No lo edites a mano: cambia los marcadores `@pytest.mark.audit` de los tests o `DOCUMENTAL` en `src/cergneux_audit/report.py`.

«TC» = *Teoría del Tiempo Cuántico* (ene. 2025); «Túnel» = *Reinterpretación del efecto túnel* (dic. 2025).

**Resumen:** ℹ️ Identidad: 2 · ✅ Coincide: 2 · ❌ Discrepa: 7 · ⚠️ A verificar: 1 · 📄 Documental: 2

| # | Afirmación | Página | Veredicto | Detalle | Test |
|---|---|---|---|---|---|
| 1 | c = L_p/T_p confirma el movimiento cuántico | TC p. 5 | ℹ️ Identidad | Identidad por definición de L_p y T_p; no confirma nada | `test_planck_speed_is_c_by_construction` |
| 2 | 1/T_p ≈ 1,85487e43 movimientos por segundo | TC p. 6 | ✅ Coincide | Valor numérico correcto | `test_ticks_per_second_matches_paper` |
| 3 | Gemelos: T₁ = γ·T₂ con v = 0,866 c | TC pp. 12-14 | ✅ Coincide | Es la dilatación temporal estándar con otra notación | `test_twin_gamma_two` |
| 4 | CMB en r = r_s con ρ → ∞ | TC pp. 32, 48 | ❌ Discrepa | Un ρ pequeño exige r ≫ r_s (ρ = 1,1 ⇒ r ≈ 5,76 r_s); no hay regla distancia → r | `test_small_redshift_needs_r_far_beyond_rs` |
| 5 | r_s de la masa bariónica = radio del universo observable | TC p. 43 | ℹ️ Identidad | r_s de la masa crítica en la esfera de Hubble es c/H₀ por álgebra, no por coincidencia | `test_rs_equals_hubble_radius_is_an_identity` |
| 6 | Mercurio: 28,8 km de desfase por dilatación temporal | TC pp. 37-38 | ❌ Discrepa | La dilatación da ~8 km; 28,8 km es el desfase geométrico de la precesión de la RG | `test_mercury_paper_shift_is_the_precession_not_the_dilation` |
| 7 | Las supernovas más lejanas duran menos (Tm = Tr/(1+z)) | TC pp. 46-47 | ⚠️ A verificar | Opuesto al estiramiento (1+z) de la literatura. Ajuste de exponente listo (b=+1 estándar, b=−1 Fila); faltan datos reales en data/ | `test_sn_stretch_directions_are_opposite` |
| 8 | Ley de la Energía: ρ fotones por cada fotón emitido | TC pp. 30-31 | ❌ Discrepa | Aplicada a un cuerpo negro da emisividad ρ⁴; FIRAS mide 1 | `test_energy_conservation_claim_gives_rho4_emissivity` |
| 9 | ΔD constante e invariable (p. 10) y ΔD decreciente en el tiempo (p. 51) | TC pp. 10, 51 | 📄 Documental | Contradicción interna del texto | — |
| 10 | dn/dt = (E_J sin φ + F)/ħ | Túnel §4.1 | ❌ Discrepa | Contradice su propia ecuación dn/dt = −(1/ħ)∂H/∂φ: el signo correcto es (F − E_J sin φ)/ħ | `test_hamilton_sign_error_in_paper` |
| 11 | «n entero ⇒ φ discreta» | Túnel §3.3 | 📄 Documental | n entero implica φ periódica (compacta), no discreta | — |
| 12 | La meseta de la tasa de escape a baja T prueba tiempo discreto | Túnel §7 | ❌ Discrepa | La explica el túnel con disipación (Devoret-Martinis-Clarke 1985) | `test_mqt_plateau_below_crossover_without_discrete_time` |
| 13 | Test 1: T₂ ~ τ_p·2π/(ΔE/ħ) | Túnel §12 | ❌ Discrepa | ~1e-53 s frente a ~1e-4 s medidos | `test_cergneux_t2_prediction_is_absurdly_short` |
| 14 | El túnel es un salto discreto sin trayectoria continua | TC p. 55; Túnel §7 | ❌ Discrepa | La evolución continua de Schrödinger reproduce la transmisión analítica; no hace falta el salto | `test_wavepacket_transmission_matches_analytic` |

El veredicto es la tesis del autor del repo; que el test pase significa que la evidencia es reproducible.
