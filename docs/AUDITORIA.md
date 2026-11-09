# Auditoría: resultados

> Archivo **generado** con `pytest --audit-report docs/AUDITORIA.md`. No lo edites a mano: cambia los marcadores `@pytest.mark.audit` de los tests o `DOCUMENTAL` en `src/cergneux_audit/report.py`.

«TC» = *Teoría del Tiempo Cuántico* (ene. 2025); «Túnel» = *Reinterpretación del efecto túnel* (dic. 2025).

**Resumen:** ℹ️ Identidad: 2 · ✅ Coincide: 4 · ⚠️ A verificar: 2 · ❌ Discrepa: 10 · 📄 Documental: 2

| # | Afirmación | Página | Veredicto | Detalle | Test |
|---|---|---|---|---|---|
| 1 | c = L_p/T_p confirma el movimiento cuántico | TC p. 5 | ℹ️ Identidad | Identidad por definición de L_p y T_p; no confirma nada | `test_planck_speed_is_c_by_construction` |
| 2 | 1/T_p ≈ 1,85487e43 movimientos por segundo | TC p. 6 | ✅ Coincide | Valor numérico correcto | `test_ticks_per_second_matches_paper` |
| 3 | Gemelos: T₁ = γ·T₂ con v = 0,866 c | TC pp. 12-14 | ✅ Coincide | Es la dilatación temporal estándar con otra notación | `test_twin_gamma_two` |
| 4 | ρ(r) = 1/√(1−r_s/r) da el corrimiento a toda distancia (Figs. 25-29; CMB en r = r_s) | TC pp. 32, 48 | ⚠️ A verificar | Con esa fórmula un ρ pequeño exige r ≫ r_s (ρ = 1,1 ⇒ r ≈ 5,76 r_s). Si solo vale en el límite del CMB, el PDF no da ρ(d) para z intermedios: falta una regla para ΔD(t) | `test_small_redshift_needs_r_far_beyond_rs` |
| 5 | r_s de la masa bariónica = radio del universo observable | TC p. 43 | ℹ️ Identidad | r_s de la masa crítica en la esfera de Hubble es c/H₀ por álgebra, no por coincidencia | `test_rs_equals_hubble_radius_is_an_identity` |
| 6 | Mercurio: 28,8 km de desfase por dilatación temporal | TC pp. 37-38 | ❌ Discrepa | La dilatación da ~8 km; 28,8 km es el desfase geométrico de la precesión de la RG | `test_mercury_paper_shift_is_the_precession_not_the_dilation` |
| 7 | Las supernovas más lejanas duran menos (Tm = Tr/(1+z)) | TC pp. 34, 46-47 | ❌ Discrepa | Datos reales (Blondin et al. 2008, Tabla 3, 35 SN): χ²≈27 para el estándar 1/(1+z) y ≈796 para la Ley de la Fila; exponente b=0,97±0,10 (la Fila exige b=−1) | `test_real_data_contradict_ley_de_la_fila` |
| 8 | Ley de la Energía: ρ fotones por cada fotón emitido | TC pp. 30-31 | ❌ Discrepa | Aplicada a un cuerpo negro da emisividad ρ⁴; FIRAS mide 1 | `test_energy_conservation_claim_gives_rho4_emissivity` |
| 9 | ΔD constante e invariable (p. 10) y ΔD decreciente en el tiempo (p. 51) | TC pp. 10, 51 | 📄 Documental | Contradicción interna del texto | — |
| 10 | dn/dt = (E_J sin φ + F)/ħ | Túnel §4.1 | ❌ Discrepa | Contradice su propia ecuación dn/dt = −(1/ħ)∂H/∂φ: el signo correcto es (F − E_J sin φ)/ħ | `test_hamilton_sign_error_in_paper` |
| 11 | «n entero ⇒ φ discreta» | Túnel §3.3 | 📄 Documental | n entero implica φ periódica (compacta), no discreta | — |
| 12 | La meseta de la tasa de escape a baja T prueba tiempo discreto | Túnel §7 | ❌ Discrepa | La explica el túnel con disipación (Devoret-Martinis-Clarke 1985) | `test_mqt_plateau_below_crossover_without_discrete_time` |
| 13 | Test 1: T₂ ~ τ_p·2π/(ΔE/ħ) | Túnel §12 | ❌ Discrepa | ~1e-53 s frente a ~1e-4 s medidos | `test_cergneux_t2_prediction_is_absurdly_short` |
| 14 | El túnel es un salto discreto sin trayectoria continua | TC p. 55; Túnel §7 | ❌ Discrepa | La evolución continua de Schrödinger reproduce la transmisión analítica; no hace falta el salto | `test_wavepacket_transmission_matches_analytic` |
| 15 | El fotón avanza una celda de Planck por tick (c = ℓ_p/T_p) y las partículas con masa son más lentas | TC pp. 5-6 | ✅ Coincide | Realizable como paseo cuántico discreto 1D: v=1 exacta sin masa, v<1 con masa; el paquete simulado lo confirma | `test_lattice_walk_reproduces_postulated_speeds` |
| 16 | Una retícula de Planck es compatible con la invariancia de Lorentz macroscópica | TC pp. 4-6, 12 | ⚠️ A verificar | Modelo 1D: la desviación escala como (E/E_P)² y es ínfima a energías accesibles; no prueba la anisotropía 3D ni la simultaneidad universal | `test_lattice_lorentz_violation_scales_as_lambda_squared` |
| 17 | La luz avanza una celda de Planck por tick en cualquier dirección de una retícula cúbica (c isótropa) | TC pp. 4-6 | ❌ Discrepa | Literal en retícula cúbica la velocidad varía un 42 % entre ejes y diagonales (1/√3 a 1, o 1 a √3); las pruebas de isotropía de c llegan a ~1e-17 | `test_cubic_lattice_light_is_anisotropic_at_order_one` |
| 18 | Una retícula espacial de Planck es compatible con las cotas de dispersión de la luz | TC pp. 4-6 | ✅ Coincide | Dispersión cuadrática v≈1−(ka)²/8 ⇒ E_QG,2≈3,5 E_P ≈ 4e19 GeV, muy por encima de la cota de Fermi-LAT (1,3e11 GeV): compatible con las cotas y no detectable hoy | `test_spatial_lattice_dispersion_is_far_above_grb_bound` |
| 19 | Las curvas de luz de supernovas lejanas se ven más estrechas (w = s/(1+z)) | TC pp. 34, 46-47 | ❌ Discrepa | Muestra independiente (Goldhaber et al. 2001, 58 SN, curvas de luz): ln w = a + b·ln(1+z) da b≈1,08±0,07; la Fila exige b=−1 (>25σ), χ²≈857 frente a ≈57 | `test_goldhaber_light_curve_widths_contradict_fila` |
| 20 | La Ley del Tiempo (Te = Tr/ρ) y la Ley de la Fila (Tm = Tr/ρ) son coherentes entre sí | TC pp. 31, 34, 47 | ❌ Discrepa | Aplicada a un proceso de duración propia fija, la Ley del Tiempo da Tr = ρ·Te: estiramiento (1+z), como en los datos. Esa lectura coherente no es descartada por las supernovas, que entonces no distinguen la teoría de la expansión | `test_ley_del_tiempo_implies_stretch_not_shortening` |

El veredicto es la tesis del autor del repo; que el test pase significa que la evidencia es reproducible.
