# A5: Below-threshold suppression and teraquop footprint at circuit level

## Prior study

| Key | Paper | Where | Value | Conditions |
|---|---|---|---|---|
| ORourke2025 | A. R. O'Rourke and S. Devitt, "Compare the Pair: Rotated vs. Unrotated Surface Codes at Equal Logical Error Rates," *Phys. Rev. Research* **7**, 033074 (2025) [arXiv:2409.14765](https://arxiv.org/abs/2409.14765) | Table III (SD, rotated, odd d), §IV.D, and the released circuits and statistics ([compare_the_pair](https://github.com/wamud/compare_the_pair): `src/circuits/SD/z`, `SD_stats.csv`) | Fit p_L = α (p/β)^(γd − δ): α = 0.081 ± 0.014, β = 0.00531 ± 0.00002, γ = 0.577 ± 0.010, δ = 0.24 ± 0.16. Footprint: 1395 ± 18 qubits for p_L = 10⁻¹² at p = 10⁻³ (d* ≈ 26.4; d = 27 gives 1457) | Rotated code, 2d² − 1 qubits. SD noise: two-qubit depolarizing p after each CNOT, depolarizing p after each H and on every idle qubit, reset and measurement errors p. A round has 7 layers: H, CNOT × 4, H, MR. 3d rounds, converted to p_L per d rounds. Memory Z, PyMatching 2. The fit uses p ≤ 0.004 and d ≥ 8. The footprint comes from an unweighted line fit (released code; the figure caption says weighted) of log p_L against √n over d = 8–22 |

- **The plugins reproduce the released circuits.**
  - [codes.py](codes.py) adds one gate-free step before the CNOTs, for the first H layer. [noises.py](noises.py) folds the second H layer into the measurement flip, q = p ⊕ 2p/3 = 5p/3 − 4p²/3. On the final data readout, q stands for the paper's idle error during the last MR plus its readout flip.
  - With the paper's CNOT order put into the code plugin, the DEM on the Z detectors has the same mechanisms as the released circuits' (d = 3–13, p = 0.001 and 0.002, d and 3d rounds). Their probabilities agree within 0.1%, except at the bottom time boundary, where the framework's data idle once more before the first round (19–34% higher), and on one data qubit per round, whose idle error during MR the released circuits omit.
  - The A5 run also differs in its rounds (d instead of 3d) and its CNOT order (the framework's N/Z order). The paper reports that its results hold for every valid order (Fig. 5, §IV.A).
- From the fit, Λ per d rounds is (β/p)^(2γ): 6.87 ± 0.23 at p = 0.001 and 3.09 ± 0.06 at p = 0.002. The paper does not quote these.

## Setup

- Config: [config_suppression.yaml](config_suppression.yaml), with the plugins `rotated_surface_sd` and `depolarizing_sd`.
- `circuit_level`, `p_meas: same_as_p` (keeps q), Z basis, d rounds, decoder `mwpm`.
- d = 7, 9, 11, 13 at p = 0.001 and 0.002.
- Each point ran to 1000 errors or 2 × 10⁸ shots. At p = 0.001, d = 11 (530 errors) and d = 13 (75 errors) stopped at the shot limit.
- `results/suppression/threshold.csv` (0.523%) comes from the placeholder sweep that `cdsc analyze` needs, and is not a result. [config_threshold.yaml](config_threshold.yaml), against the paper's 0.565%, has not been run.

## Result

p_L per d rounds, from [results/suppression/samples.csv](results/suppression/samples.csv) and the paper's `SD_stats.csv`:

| p | d | Framework | Errors | ORourke2025 data | Framework / data | Framework / fit |
|---|---|---|---|---|---|---|
| 0.001 | 7 | 1.005 × 10⁻⁴ | 1002 | 1.179 × 10⁻⁴ | 0.85 ± 0.04 | 0.71 |
| 0.001 | 9 | 1.728 × 10⁻⁵ | 1001 | 1.961 × 10⁻⁵ | 0.88 ± 0.04 | 0.83 |
| 0.001 | 11 | 2.65 × 10⁻⁶ | 530 | 3.04 × 10⁻⁶ | 0.87 ± 0.05 | 0.88 |
| 0.001 | 13 | 3.75 × 10⁻⁷ | 75 | 4.56 × 10⁻⁷ | 0.82 ± 0.10 | 0.85 |
| 0.002 | 7 | 1.614 × 10⁻³ | 1065 | 1.853 × 10⁻³ | 0.87 ± 0.03 | 0.81 |
| 0.002 | 9 | 5.778 × 10⁻⁴ | 1006 | 6.234 × 10⁻⁴ | 0.93 ± 0.04 | 0.90 |
| 0.002 | 11 | 1.859 × 10⁻⁴ | 1003 | 2.278 × 10⁻⁴ | 0.82 ± 0.04 | 0.89 |
| 0.002 | 13 | 6.399 × 10⁻⁵ | 1002 | 7.332 × 10⁻⁵ | 0.87 ± 0.04 | 0.95 |

- The ratio to the data is 0.871 ± 0.014, the same at every point (χ² = 5.2 for 7 degrees of freedom).

Λ per d rounds, p_L(d)/p_L(d + 2), as ORourke2025 data / framework:

| p | (β/p)^(2γ) | 7→9 | 9→11 | 11→13 | Framework, fit on d = 9–13 |
|---|---|---|---|---|---|
| 0.001 | 6.87 ± 0.23 | 6.01 ± 0.26 / 5.82 ± 0.26 | 6.46 ± 0.29 / 6.52 ± 0.35 | 6.66 ± 0.37 / 7.07 ± 0.87 | 6.64 ± 0.28 |
| 0.002 | 3.09 ± 0.06 | 2.97 ± 0.08 / 2.79 ± 0.12 | 2.74 ± 0.11 / 3.11 ± 0.14 | 3.11 ± 0.14 / 2.91 ± 0.13 | 3.01 ± 0.07 |

- Each framework value is within 2.1σ of the data. At 7→9 both lie below (β/p)^(2γ), whose fit starts at d = 8.
- `suppression.csv` reports Λ per round (7.76 and 3.63), a different quantity.

d* for p_L = 10⁻¹² per d rounds. d_teraquop is the smallest odd d ≥ d*, with 2d² − 1 qubits. Ranges are 16–84% of a binomial bootstrap:

| | p = 10⁻³: d* | p = 10⁻³: d_teraquop, qubits | p = 2 × 10⁻³: d* | p = 2 × 10⁻³: d_teraquop |
|---|---|---|---|---|
| ORourke2025 | 26.42 ± 0.17, from 1395 ± 18 qubits (§IV.D) | 27, 1457 (§IV.D) | 45.00, computed from Table III (not quoted) | 45 |
| Framework, `suppression.csv` (d = 7–13) | 26.29 (26.09–26.50) | 27, 1457 | 42.73 (42.36–43.10) | 43 |
| Framework, refit on d = 9–13 | 26.00 (25.67–26.35) | 27, 1457 | 42.82 (42.26–43.42) | 43 |
| Framework data, the paper's method (d = 9–13) | 26.44 | 27, 1457 | 45.71 | 47 |

- The extrapolation models differ: the framework fits log ε per round against d, weighted; the paper fits log p_L per d rounds against √n, unweighted. On the same data, d* moves by 0.44–0.55 at p = 10⁻³ and by 2.9–3.6 at 2 × 10⁻³, where d_teraquop changes from 43 to 47.
- At 2 × 10⁻³, d_teraquop is not robust: the upper ends of the framework ranges give 45, and the Table III d* (44.998) sits on the 45/47 boundary.

## Verdict

- **Equivalent circuit: pass.** Mechanism for mechanism, apart from the bottom time boundary and the idle error the released circuits omit.
- **p_L: 13% below the paper's data at every point.** Lower is the direction expected from d rounds instead of 3d, which gives the time boundaries three times the weight. The size was not tested with a 3d-round run. A constant factor leaves Λ unchanged and lowers d* by about 0.15.
- **Λ: pass.** Within 2.1σ of the paper's data pair by pair, and within 1σ of (β/p)^(2γ) on d = 9–13.
- **Footprint at p = 10⁻³: pass.** d* = 26.0–26.4 against 26.4, with the same d_teraquop (27) and qubit count (1457).
