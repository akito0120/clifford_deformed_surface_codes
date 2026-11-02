# A5: Below-threshold suppression and teraquop footprint at circuit level

## Prior study

| Key | Paper | Where | Value | Conditions |
|---|---|---|---|---|
| ORourke2025 | A. R. O'Rourke and S. Devitt, "Compare the Pair: Rotated vs. Unrotated Surface Codes at Equal Logical Error Rates," *Phys. Rev. Research* **7**, 033074 (2025) [arXiv:2409.14765](https://arxiv.org/abs/2409.14765) | Table III (SD, rotated, odd d), §IV.D, and the released circuits and statistics ([compare_the_pair](https://github.com/wamud/compare_the_pair): `src/circuits/SD/z`, `SD_stats.csv`) | Fit p_L = α (p/β)^(γd − δ): α = 0.081 ± 0.014, β = 0.00531 ± 0.00002, γ = 0.577 ± 0.010, δ = 0.24 ± 0.16. Footprint: 1395 ± 18 qubits for p_L = 10⁻¹² at p = 10⁻³ (d* ≈ 26.4; d = 27 gives 1457) | Rotated code, 2d² − 1 qubits. SD noise: two-qubit depolarizing p after each CNOT, depolarizing p after each H and on every idle qubit, reset and measurement errors p. A round has 7 layers: H, CNOT × 4, H, MR. 3d rounds, converted to p_L per d rounds. Memory Z, PyMatching 2. The fit uses p ≤ 0.004 and d ≥ 8. The footprint comes from an unweighted line fit (released code; the Fig. 8 caption says weighted) of log p_L against √n over d = 8–22 |

- **The plugins reproduce the released circuits.**
  - [codes.py](codes.py) adds one gate-free step before the CNOTs, for the first H layer. [noises.py](noises.py) folds the second H layer into the measurement flip, q = p ⊕ 2p/3 = 5p/3 − 4p²/3. On the final data readout, q stands for the paper's idle error during the last MR plus its readout flip.
  - With the paper's CNOT order put into the code plugin, the DEM on the Z detectors has the same mechanisms as the released circuits' (d = 3–13, p = 0.001 and 0.002, d and 3d rounds). Their probabilities agree within 0.1%, except at the bottom time boundary, where the framework's data idle once more before the first round (19–34% higher), and on one data qubit per round, whose idle error during MR the released circuits omit.
  - The A5 run also differs in its rounds (d instead of 3d) and its CNOT order (the framework's N/Z order). The paper reports that its results hold for every valid order (Fig. 5, §IV.A).
- From the fit, Λ per d rounds is (β/p)^(2γ): 6.87 ± 0.23 at p = 0.001 and 3.09 ± 0.06 at p = 0.002. The paper does not quote these.

## Setup

- Config: [config_suppression.yaml](config_suppression.yaml), with the plugins `rotated_surface_sd` and `depolarizing_sd`
- `circuit_level`, `p_meas: same_as_p` (keeps q), Z basis, d rounds, decoder `mwpm`
- d = 7, 9, 11, 13
- p = 0.001 and 0.002
- Each point ran to 1000 errors or 2 × 10⁸ shots. At p = 0.001, d = 11 (530 errors) and d = 13 (75 errors) stopped at the shot limit.
- Threshold: required by the schema, not used. The threshold, against ORourke2025's 0.565%, is in [A4](../a4_circuit_level_depolarizing/result.md).


## Result

p_L per d rounds, from [results/suppression/samples.csv](results/suppression/samples.csv) and ORourke2025's [SD_stats.csv](https://github.com/wamud/compare_the_pair/blob/main/src/collected_stats/SD_stats.csv):

| p | d | Framework's p_L | Framework's Errors | ORourke2025's p_L | Framework / ORourke2025 p_L ratio | Framework / ORourke2025's fit p_L ratio |
|---|---|---|---|---|---|---|
| 0.001 | 7 | 1.005 × 10⁻⁴ | 1002 | 1.179 × 10⁻⁴ | 0.85 ± 0.04 | 0.71 |
| 0.001 | 9 | 1.728 × 10⁻⁵ | 1001 | 1.961 × 10⁻⁵ | 0.88 ± 0.04 | 0.83 |
| 0.001 | 11 | 2.65 × 10⁻⁶ | 530 | 3.04 × 10⁻⁶ | 0.87 ± 0.05 | 0.88 |
| 0.001 | 13 | 3.75 × 10⁻⁷ | 75 | 4.56 × 10⁻⁷ | 0.82 ± 0.10 | 0.85 |
| 0.002 | 7 | 1.614 × 10⁻³ | 1065 | 1.853 × 10⁻³ | 0.87 ± 0.03 | 0.81 |
| 0.002 | 9 | 5.778 × 10⁻⁴ | 1006 | 6.234 × 10⁻⁴ | 0.93 ± 0.04 | 0.90 |
| 0.002 | 11 | 1.859 × 10⁻⁴ | 1003 | 2.278 × 10⁻⁴ | 0.82 ± 0.04 | 0.89 |
| 0.002 | 13 | 6.399 × 10⁻⁵ | 1002 | 7.332 × 10⁻⁵ | 0.87 ± 0.04 | 0.95 |

- The ratio to the ORourke2025's data is 0.871 ± 0.014, the same at every point (χ² = 5.2 for 7 degrees of freedom).

---

Λ per d rounds, p_L(d)/p_L(d + 2), as ORourke2025 data / framework:

| p | ORourke2025 (β/p)^(2γ) | 7→9 | 9→11 | 11→13 | Framework, fit on d = 9–13 |
|---|---|---|---|---|---|
| 0.001 | 6.87 ± 0.23 | 6.01 ± 0.26 / 5.82 ± 0.26 | 6.46 ± 0.29 / 6.52 ± 0.35 | 6.66 ± 0.37 / 7.07 ± 0.87 | 6.64 ± 0.28 |
| 0.002 | 3.09 ± 0.06 | 2.97 ± 0.08 / 2.79 ± 0.12 | 2.74 ± 0.11 / 3.11 ± 0.14 | 3.11 ± 0.14 / 2.91 ± 0.13 | 3.01 ± 0.07 |

- Each framework value is within 2.1σ of the data. At 7→9 both lie below (β/p)^(2γ), whose fit starts at d = 8.
- [suppression.csv](./results/suppression/suppression.csv) reports Λ per round (7.76 and 3.63), a different quantity.

---

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


## Excerpts

Verbatim from the sources, for text search in the originals. Math is in plain text, and citations are shown as […].

### ORourke2025 (arXiv v2, published as Phys. Rev. Research 7, 033074)

- Qubit count: Table I, column "Rotated": Data qubits d^2, Auxiliaries d^2 − 1, Total qubits 2d^2 − 1. Caption:
  > A distance-d logical qubit's physical qubit count.
- Circuits and idling (§II.B):
  > The X(Z)-type circuit is in the upper (lower) half of the figure. Including initialisation and measurement of the auxiliary, the circuit's depth is eight (six). If errors are inserted in the Z-type measurement circuit with the same error probabilities as the Hadamard gates in the X-type circuit, to account for the time in the Z-type circuit that the qubits are idle while the Hadamards are being performed in the X-type circuit, the circuits become effectively equivalent in terms of noise and resultant logical error rates, despite differences in actual depth.

  > Circuit-level noise, on the other hand, models all the operations as faulty, as well as features idling errors, which apply to any qubit not being operated on in a particular time step, that is while an operation is being performed on another qubit.
- SD noise (§III and Table II):
  > In this comparative study we implemented standard depolarising (SD) and superconducting-inspired (SI; […]) circuit-level noise, as applied to our circuits compiled with CNOT gates.

  > We added modifications that enabled the re-ordering of CNOT gates, suggested as the explanation for the difference in the unrotated surface code's p_L between memory X and Z […], and added idling errors on any qubits not being operated on while operations were being applied to other qubits. This included adding idling errors on Z-type stabiliser auxiliaries with the same error probabilities as the Hadamard gate while Hadamard gates were applied to the X-type stabiliser auxiliaries. This renders the two syndrome extraction circuits equivalent in terms of noise.

  Table II, caption and the SD column (the SI column is left out):
  > Standard depolarising (SD) and superconducting-inspired (SI; […]) noise, as applied to the gates in our circuits.

  | Qubit operation | Error | SD |
  |---|---|---|
  | CNOT | Perform CNOT then choose an error uniformly from {𝟙, X, Y, Z}^⊗2 ∖ {𝟙𝟙} | p |
  | Hadamard (H) | Perform H then choose an error uniformly from {X, Y, Z} | p |
  | Reset to \|0⟩ (\|+⟩) | Instead resets to \|1⟩ (\|−⟩) | p |
  | Measurement | Report incorrect result and project to orthogonal eigenstate | p |
  | Idle during gates on other qubits | Choose an error uniformly from {X, Y, Z} | p |
  | Idle during reset or measurement of other qubits | Choose an error uniformly from {X, Y, Z} | p |
- Detectors (§III):
  > To reduce simulation time we enabled the option to exclude detectors in the opposite basis to that of the measured logical observable because PyMatching, being an uncorrelated decoder, does not use these detection events.
- Data idling and MR (Fig. A.1 caption, which shows a d = 2 unrotated circuit):
  > Also depicted is the depolarising errors applied on data qubits before each round of stabiliser measurements, which can equivalently be thought of as idling errors during the Hadamard gates on the X-type stabilisers' auxiliary qubits.

  > MR is a sequential combination of a measure and reset gate in the Z basis. Both the measurement and the reset can be faulty.
- Decoder, rounds and repository (§III):
  > Additionally we used the MWPM decoder PyMatching 2 […].

  > Our generated data, as well as the python code used to generate the circuits, run simulations and render plots, is available at the GitHub repository github.com/wamud/compare_the_pair.

  > We calculated p_L per d rounds but ran 3d rounds of stabiliser measurements to reduce time-boundary edge effects, which arise because the first and last round have less logical errors […]. The p_L per d rounds is hence the XOR of three independent Bernoulli distributions.
- Memory Z and CNOT order (§IV.A, and the captions of Fig. 5 and Fig. A.8):
  > For specificity we are reporting p_L results for memory Z and the CNOT orders are 32013021 for the rotated code and 10231203 (X_L-aligned inner CNOTs) for the unrotated. However, these results reproduce for memory X when also using a worst-case unrotated CNOT ordering (see figures A.8 and A.9) so the choice of valid CNOT orders is arbitrary.

  > Displayed results are from CNOT orders rotated 32013021 and unrotated 10231203, numbering as per Fig. 2, but for all valid CNOT orders these results generalise (see Section IV A).

  > Listed CNOT orders give identical plots up to uncertainty so are grouped.
- Threshold (§IV.B):
  > By inspection the rotated and unrotated p_th are equal. For each noise model they are p_th,SD ≈ 5.65×10^−3, p_th,SI ≈ 5.05×10^−3.
- Fit (§IV.B):
  > We hence instead fit to p_L = α(p/β)^(γd − δ), where we can define the error dimension d_e = γd − δ. Our fits used d ≥ 6 (8) for the unrotated (rotated) code to minimise edge effects that prevent low-distance codes from following the same scaling relationship (see Fig. A.13), and used p ≤ 0.004 because p values closer to p_th were not indicative of sub-threshold scaling.
- Value: Table III, row SD, Rotated, Odd, columns α, β, γ, δ: 0.081 ± 0.014, 0.00531 ± 0.00002, 0.577 ± 0.010, 0.24 ± 0.16. First sentence of the caption:
  > Fits to p_L = α(p/β)^(γd − δ) (Eq. 4) using d ≥ 6 (8) for the unrotated (rotated) code and physical error rates p ≤ 0.004, based on memory Z results but these are equivalent up to uncertainty to memory X (see Section II C).
- Footprint (Fig. 6 caption, §IV.D and Fig. 8 caption):
  > We fit to d ≥ 8 (6) for the rotated (unrotated) code to minimise edge effects. The points of intersection between these least-squares line fits and p_L = 10^−12 are used to generate the 'teraquop' plot in Fig. 8.

  > Projecting the least-squares line fits from Fig. 6 (A.3) to p_L = 10^−12 reveals the teraquop qubit counts for SD (SI) noise.

  > At p = 10^−3, the rotated code uses 1395 ± 18 qubits whereas the unrotated code uses 1847 ± 25 qubits under SD noise.

  > Using these, achieving the teraquop regime at p = 10^−3 under either noise model requires 1457 qubits in the rotated code (d = 27) or 2025 (d = 23) in the unrotated, corresponding to a ratio of 72%.

  > Number of qubits needed to reach the teraquop regime (p_L = 10^−12) under SD noise (see Fig. A.5 for SI noise), calculated using the weighted line fits from Fig. 6, with weights based on the root mean square error (RMSE) of the MLEs for p_L, assuming a binomial distribution.
- Circuit file: the d = 3 rotated memory-Z circuit at p = 0.001, from [wamud/compare_the_pair](https://github.com/wamud/compare_the_pair) at commit a051cbe ([src/circuits/SD/z/d=3,p=0.001,noise=SD,b=z,r=3d,ro=ro,o=10231203,idl=y.stim L18–L33, L37–L38, L42–L43, L47–L55, L60–L62, L104–L106](https://github.com/wamud/compare_the_pair/blob/a051cbe/src/circuits/SD/z/d=3,p=0.001,noise=SD,b=z,r=3d,ro=ro,o=10231203,idl=y.stim#L18-L106)). The first round precedes the block, so d = 3 runs 9 rounds. Data qubit 8 is reset in L18 but missing from the idle lists after MR (L60, and L102 in the block). The circuits at d = 5–13 each leave out one data qubit in the same way.
  ```text
  R 1 3 5 8 10 12 15 17 19
  X_ERROR(0.001) 1 3 5 8 10 12 15 17 19
  R 2 9 11 13 14 16 18 25
  X_ERROR(0.001) 2 9 11 13 14 16 18 25
  TICK
  H 2 11 16 25
  DEPOLARIZE1(0.001) 2 11 16 25
  I 1 3 5 8 9 10 12 13 14 15 17 18 19
  DEPOLARIZE1(0.001) 1 3 5 8 9 10 12 13 14 15 17 18 19
  TICK
  CX 16 10 11 5 25 19 8 14 3 9 12 18
  DEPOLARIZE2(0.001) 16 10 11 5 25 19 8 14 3 9 12 18
  I 1 2 13 15 17
  DEPOLARIZE1(0.001) 1 2 13 15 17
  TICK
  CX 16 8 11 3 25 17 15 14 10 9 19 18
  ...
  TICK
  CX 2 3 16 17 11 12 1 9 10 18 5 13
  ...
  TICK
  CX 2 1 16 15 11 10 8 9 17 18 12 13
  ...
  TICK
  H 2 11 16 25
  DEPOLARIZE1(0.001) 2 11 16 25
  I 1 3 5 8 9 10 12 13 14 15 17 18 19
  DEPOLARIZE1(0.001) 1 3 5 8 9 10 12 13 14 15 17 18 19
  TICK
  X_ERROR(0.001) 2 9 11 13 14 16 18 25
  MR 2 9 11 13 14 16 18 25
  X_ERROR(0.001) 2 9 11 13 14 16 18 25
  ...
  I 1 3 5 10 12 15 17 19
  DEPOLARIZE1(0.001) 1 3 5 10 12 15 17 19
  REPEAT 8 {
  ...
  }
  X_ERROR(0.001) 1 3 5 8 10 12 15 17 19
  M 1 3 5 8 10 12 15 17 19
  ```
- CNOT order label: the repository labels the rotated order 10231203, where the paper says 32013021. It is the only rotated order in `SD_stats.csv`, and [src/paper_data_and_plots.ipynb](https://github.com/wamud/compare_the_pair/blob/a051cbe/src/paper_data_and_plots.ipynb), which "plots the data presented in the paper", prints "Rotated code CNOT orders:" followed by 10231203, and plots that order.
- Teraquop fit, from the cell under "Plot 'teraquop' count" in [src/paper_data_and_plots.ipynb](https://github.com/wamud/compare_the_pair/blob/a051cbe/src/paper_data_and_plots.ipynb), and from [src/functions/com_funcs5.py L1419–L1420, L1439–L1440, L1499–L1502, L1521–L1529, L1552–L1557](https://github.com/wamud/compare_the_pair/blob/a051cbe/src/functions/com_funcs5.py#L1419-L1557). p = 1e-3 is the third entry of `ps`, so the rotated fit runs over d = 8–22:
  ```python
  ps = [5e-4, 7e-4, 1e-3, 1.5e-3, 2e-3, 3e-3, 4e-3, 5e-3]

  funcs.plot_teraquop(mylist, b, roorder, unroorder, ps = ps, teraquop_inset = True, romind = 8, unromind = 6, optional_plot = False, ylims = [4e2,7e7])  # make sure selection of pvalues is below threshold
  ```
  ```python
  # NOte, in function below the maxds are hard-coded to paper max d's (unrot 17, rot 22)
  def plot_teraquop(mylist, b, roorder, unroorder, ps = None,  noise_model = 'SD', romind = 2, unromind = 2, optional_plot = False, teraquop_inset = False, ylims = [None,None]):
  ...
      num_rounds = '3d'
      find_pL_per = 'd rounds'  # Choices are 'round', 'd rounds' or 'shot'
  ...
          if rotation == 'ro':
              # minds = [8 for _ in ps]
              minds = [romind for _ in ps]
              maxds = [17,18] + [22 for _ in range(len(ps)-2)]
  ...
              # GRADIENTS AND INTERCEPTS HERE ARE FITS FOR log10(p_L) = m * d + b
              distances, qubits, gradients_unused, intercepts_unused, pL, log_pL, uncertainties_log_pL, gradient_errors, intercept_errors     =     extract4teraquop(b, noise, mind, maxd, unroorder, roorder, mylist, num_rounds, find_pL_per, pL_estimator, plvsd = True)

              # LET'S INSTEAD GET GRADIENTS AND INTERCEPTS FOR log10(p_L) = m * rt(q) + b WHERE Q IS QUBIT COUNT

              index = 0 if rotation == 'ro' else 1 # pL is a list of list. The first list (at index 0) is for rotated, the second is for unrotated:


              params, pcov = optimize.curve_fit(linear_model, np.sqrt(qubits[index]), log_pL[index])
  ...
              yval = -12 # on a log10 plot this corresponds to a pL of 10^-12

              # d = (yval - b_fit) / m_fit # the teraquop distance
              rtq = (yval - b_fit) / m_fit # the teraquop qubit count

              q = rtq ** 2
  ```
- p_L per d rounds, in `extract4teraquop` ([com_funcs5.py L797–L798, L802–L803, L807–L808](https://github.com/wamud/compare_the_pair/blob/a051cbe/src/functions/com_funcs5.py#L797-L808)):
  ```python
  else: # i.e. if num_rounds is 3d, 10d, etc.
      rounds_multiple = int(num_rounds.strip('d')) # number of rounds taken as multiple of d
  ...
  if find_pL_per == 'd rounds':
      n = rounds_multiple
  ...
  # Updater pL and RMSE(pL) given we are not finding it per shot but per find_pL_per
  pL = sinter.shot_error_rate_to_piece_error_rate(pL, pieces = n)
  ```
- Statistics, from [src/collected_stats/SD_stats.csv](https://github.com/wamud/compare_the_pair/blob/a051cbe/src/collected_stats/SD_stats.csv) (92 MB): line 1, and line 22681, the first row of d = 7 at p = 0.001. Each point of the Result table is spread over 18–136 rows that share one `strong_id`, and their `json_metadata` differs from this row's only in d and p. The "ORourke2025 data" column sums the `shots` and `errors` of those rows and converts them per d rounds as above.
  ```text
       shots,    errors,  discards, seconds,decoder,strong_id,json_metadata,custom_counts
         100,         0,         0,   0.002,pymatching,db39fe684ecd7dccf83a78d686b9d0ecb173a65f7df6b785c0b06f93d5f7ec0a,"{""b"":""z"",""d"":7,""idl"":""y"",""noise"":""SD"",""o"":10231203,""p"":0.001,""r"":""3d"",""ro"":""ro""}",
  ```
