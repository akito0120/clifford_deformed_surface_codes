# A4: Depolarizing circuit-level threshold

## Prior studies

| Key | Paper | Where | Value | Conditions |
|---|---|---|---|---|
| Stephens2014 | A. M. Stephens, "Fault-tolerant thresholds for quantum error correction with the surface code" [arXiv:1311.5003](https://arxiv.org/abs/1311.5003) | §V.C and Table I, depth-6 circuits, standard noise model | 0.672 ± 0.001% (ν0 = 1.06) | Unrotated planar code, odd d = 3–17 with the fit on d ≥ 9, d rounds, p_L per d rounds, X-error threshold. Preparation, CNOT, measurement and idle (identity-gate) errors all at p. Each ancilla is prepared and measured in its check's basis, without H gates. MWPM (Blossom V) with circuit-derived weights, X and Z decoded separately. About 10⁶ instances and at least 10⁴ logical errors per point |
| ORourke2025 | A. R. O'Rourke and S. Devitt, "Compare the Pair: Rotated vs. Unrotated Surface Codes at Equal Logical Error Rates" [arXiv:2409.14765](https://arxiv.org/abs/2409.14765) | §IV.B | 0.565%, the same for the rotated and the worst-case unrotated code | SD noise, whose round adds two H layers (H, 4 CNOT, H, MR), 3d rounds, memory Z, PyMatching |

- **Stephens2014's depth-6 round is the framework's round.**
  - Reset, four two-qubit gates and measurement, with the same error rates. Idle qubits get identity gates that fail with p, as the framework's idle noise does.
  - Under depolarizing noise, the framework's CZ onto a |+⟩ ancilla is the same as a CNOT onto a |0⟩ ancilla.
  - What differs: the unrotated layout, the decoder implementation, and the time boundaries, which Stephens2014 does not describe. The framework's data preparation and readout fail with p.  
- **The layout should not raise the rotated threshold.** At circuit level, the rotated and the worst-case unrotated code have the same threshold (ORourke2025). At code capacity, the unrotated one is higher (Criger2018: 15.42% against 14.88%).
- **A5's plugins rebuild ORourke2025's round.** A gate-free step stands in for the first H layer, and the second is folded into the measurement flip, 5p/3 − 4p²/3. What differs: d rounds instead of 3d, the CNOT order, and one extra data idle layer before the first round.

The other studies make up the **0.50–0.82%** band:

| Key | Paper | Where | Value | Main difference |
|---|---|---|---|---|
| Fowler2012 | [arXiv:1208.0928](https://arxiv.org/abs/1208.0928) | §VII, Fig. 4 | 0.57% | Depth-8 circuits with H gates; per round, not per d rounds (Stephens2014 Table I) |
| Huang2020 | [arXiv:2004.04693](https://arxiv.org/abs/2004.04693) | §III, Fig. 3, Table I | 0.65% (unweighted), 0.72% (weighted) | Toric code; preparation and measurement at 2p/3; a perfect last round |
| Higgott2023 | [arXiv:2203.04948](https://arxiv.org/abs/2203.04948) | §III.C, Fig. 4 | 0.817(5)% | Preparation and measurement at 2p/3; perfect logical preparation and readout |
| Gidney2021Honeycomb | [arXiv:2108.10457](https://arxiv.org/abs/2108.10457) | §4, Fig. 5 | 0.5–0.7% (SD6) | 8-step cycle with H gates; 3d rounds; correlated MWPM |
| Hetenyi2024 | [arXiv:2306.17786](https://arxiv.org/abs/2306.17786) | §4.4 | 0.65% (isotropic) | Spin-qubit circuits |
| Etxezarreta2025 | [arXiv:2505.17718](https://arxiv.org/abs/2505.17718) | Fig. 2, Tables II–III | about 0.66% (XZZX under SD) | H gates; CZ noise still biased under its SD (η = 1/2); 3d rounds; p_L per round |

## Setup

- Decoder: `mwpm`
- Noise model: `circuit_level`
- Each point ran to 20,000 errors or 10⁶ shots
- d = 7, 9, 11, 13, 15
- Suppression: required by the schema, not used
- Stephens2014:
  - Config: [config.yaml](config.yaml)
  - Code: `rotated_surface`
  - Bases: X and Z
  - p = 0.55–0.85% in steps of 0.025%
- ORourke2025:
  - Config: [config_sd.yaml](config_sd.yaml)
  - Code: `rotated_surface_sd`
  - Noise: `depolarizing_sd`
  - Bases: only Z
  - p = 0.44–0.68% in steps of 0.02%


## Result

From [results/threshold.csv](results/threshold.csv) and [results_sd/threshold.csv](results_sd/threshold.csv):

| Code | Basis | p_th (%) | ν | χ²_red | Compare against |
|---|---|---|---|---|---|
| rotated_surface | X | 0.6937 ± 0.0009 | 1.17 | 0.88 | Stephens2014, (0.672%) |
| rotated_surface | Z | 0.6931 ± 0.0009 | 1.13 | 1.38 | Stephens2014, (0.672%) |
| rotated_surface_sd | Z | 0.5687 ± 0.0007 | 1.14 | 1.12 | ORourke2025 (0.565%) |

- `rotated_surface` X and Z agree: they differ by 0.0006 ± 0.0013 points.
- Other distance sets (d = 7–15, 11–15) and windows (x_window = 0.008–0.02) give:
  - 0.692–0.698% for `rotated_surface`
  - 0.568–0.572% for `rotated_surface_sd`

## Verdict

- **Literature band (0.50–0.82%): both `rotated_surface` and `rotated_surface_sd` pass.**
- **Stephens2014 (0.672%): close, 3.1% (0.021 points) above.**
  - The layout and the time boundaries do not explain it.
  - The cause is not identified. The remaining difference is the decoder implementation, which has not been checked.
- **ORourke2025 (0.565%): pass, 0.7% (0.004 points) above.**


## Excerpts

Verbatim from the sources, for text search in the originals. Math is in plain text, and citations are shown as […].

### Stephens2014 (arXiv v2, published as Phys. Rev. A 89, 022321)

- Code (§II and Fig. 1 caption):
  > The surface code, also known as the planar code, is a variation of Kitaev's toric code […].

  > In general, the number of data qubits is d^2 + (d − 1)^2.
- Circuits (§IV):
  > Depth-eight circuits. First, we assume the gate set consists of the preparation of state |0⟩, the single-qubit Hadamard rotation, the two-qubit controlled-not gate, and measurement in the Z basis. Then, referring to the circuits in Figs. 2 and 3, the overall circuit depth is equal to eight.

  > Depth-six circuits. Second, we assume that the gate set is extended to include the preparation of state |+⟩ and measurement in the X basis. This removes the need for the Hadamard rotations in Fig. 2, and so, the overall circuit depth is reduced to six.

  > In each of these cases, all measurement circuits are performed in parallel and repeated d times where identity gates are inserted whenever qubits are required to be idle. In the first case, we give the Z-error threshold, which is the lower of the two thresholds and, therefore, sets the overall threshold. In all other cases, we give the X-error threshold.
- Standard noise model (§V.C) and idle qubits (§V.D):
  > First, we consider a so-called standard noise model. Erroneous single-qubit gates occur with probability p, acting ideally followed by a single-qubit Pauli error chosen randomly from set {X,Y,Z}. Similarly, erroneous two-qubit gates occur with probability p, acting ideally followed by a two-qubit Pauli error chosen randomly from set {IX,IY,IZ,XI,…,ZZ}. Lastly, erroneous initialization and measurement each occur with probability p, preparing or reporting the incorrect orthogonal eigenstate.

  > The standard noise model is somewhat unreasonable as the qubits involved in two-qubit gates are more reliable than idle qubits.
- Decoder (§III, §IV and §V.F):
  > Here, we use a decoding algorithm that identifies the most likely set of errors consistent with the error syndrome where we consider X and Z errors separately […].

  > Care must be taken to account for correlated errors that arise in the measurement circuits, and edges should be appropriately weighted to account for the fact that different kinds of errors (which cause different pairs of measurement changes) may occur with different probabilities […].

  > In our simulations, minimum-weight perfect matching is performed with Kolmogorov's implementation […] of Edmonds' perfect matching algorithm […], and we use a Mersenne twister pseudo-random number generator […].

  > Following Raussendorf et al. […], our decoding algorithm accounts for the relative probabilities of errors, including correlated errors, that arise in the measurement circuits.
  - The cited implementation is "V. Kolmogorov, Math. Program. Comput. 1, 43 (2009).", the Blossom V paper.
- Rounds, samples and fit (§IV):
  > For noise models in which the error syndrome is unreliable, the measurement circuits are repeated d times before the error syndrome is decoded.

  > For each physical error rate, the logical error rate is an average of approximately 10^6 independent instances, where we ensure that at least 10^4 logical errors are observed per point to limit statistical uncertainty.

  > Allowing for systematic finite-size effects, we fit our data to a quadratic universal scaling function, p_l = A + B(p − p_th)d^(1/ν0) + C(p − p_th)^2 d^(2/ν0), from which we determine p_th and ν0. We perform simulations for odd values of d between d = 3 and d = 17 where p ∼ p_th.

  > To account for this, values of p_th and ν0 are determined from a best fit of the data for d ≥ 9.
- Logical error rate (§VI):
  > We define the logical error rate to be the error rate per d rounds of measurement, following Raussendorf et al. […].
- Value (§V.C):
  > for the depth-six circuits, we find p_th = 0.00672 ± 0.00001, ν0 = 1.06 ± 0.02,
- Table I, row "Depth-six circuits", column "Standard noise model": 0.00672 ± 0.00001. In the same column, the "Depth-eight circuits" row lists 0.0057 […] (Fowler2012) with footnotes a and b. Caption and footnotes:
  > Summary of thresholds for various circuit-based noise models where our results are compared with previous estimates. The values without references are our results. If no uncertainty is given, none was reported in the associated reference.

  > a: Threshold for X errors. For this noise model, the Z-error threshold is lower and, therefore, sets the overall threshold.

  > b: Estimated from the logical error rate per round of measurement, rather than per d rounds of measurement.

### ORourke2025 (arXiv v2, published as Phys. Rev. Research 7, 033074)

- Circuits (§II.B):
  > Each stabiliser generator has its own measurement circuit. The X(Z)-type circuit is in the upper (lower) half of the figure. Including initialisation and measurement of the auxiliary, the circuit's depth is eight (six).
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
- Decoder, rounds and code (§III):
  > Additionally we used the MWPM decoder PyMatching 2 […].

  > We calculated p_L per d rounds but ran 3d rounds of stabiliser measurements to reduce time-boundary edge effects, which arise because the first and last round have less logical errors […].

  > Our generated data, as well as the python code used to generate the circuits, run simulations and render plots, is available at the GitHub repository github.com/wamud/compare_the_pair.
- Memory Z (§IV.A):
  > For specificity we are reporting p_L results for memory Z and the CNOT orders are 32013021 for the rotated code and 10231203 (X_L-aligned inner CNOTs) for the unrotated.
- Value (§IV.B):
  > By inspection the rotated and unrotated p_th are equal. For each noise model they are p_th,SD ≈ 5.65×10^−3, p_th,SI ≈ 5.05×10^−3.

  > While the thresholds were equal for the rotated and worst-case unrotated code, we see a slightly higher threshold for unrotated code, as noted in Ref. […], only if we consider the best-case unrotated code.
- Circuit file: one round of the d = 3 rotated memory-Z circuit at p = 0.0055, from [wamud/compare_the_pair](https://github.com/wamud/compare_the_pair) at commit a051cbe ([src/circuits/SD/z/d=3,p=0.0055,noise=SD,b=z,r=3d,ro=ro,o=10231203,idl=y.stim L62–L67, L69–L70, L74, L79, L84, L89, L94–L96](https://github.com/wamud/compare_the_pair/blob/a051cbe/src/circuits/SD/z/d=3,p=0.0055,noise=SD,b=z,r=3d,ro=ro,o=10231203,idl=y.stim#L62-L96)). The first round precedes the block, so d = 3 runs 9 rounds.
  ```text
  REPEAT 8 {
      TICK
      H 2 11 16 25
      DEPOLARIZE1(0.0055) 2 11 16 25
  I 1 3 5 8 9 10 12 13 14 15 17 18 19
  DEPOLARIZE1(0.0055) 1 3 5 8 9 10 12 13 14 15 17 18 19
  ...
      CX 16 10 11 5 25 19 8 14 3 9 12 18
      DEPOLARIZE2(0.0055) 16 10 11 5 25 19 8 14 3 9 12 18
  ...
      CX 16 8 11 3 25 17 15 14 10 9 19 18
  ...
      CX 2 3 16 17 11 12 1 9 10 18 5 13
  ...
      CX 2 1 16 15 11 10 8 9 17 18 12 13
  ...
      H 2 11 16 25
  ...
      X_ERROR(0.0055) 2 9 11 13 14 16 18 25
      MR 2 9 11 13 14 16 18 25
      X_ERROR(0.0055) 2 9 11 13 14 16 18 25
  ```

### Criger2018 (arXiv v6, published as Quantum 2, 102)

- Boundaries (§2):
  > Specifically, we focus on the rotated surface code, with the boundary conditions from Figure 1. Earlier constructions involve tiling a surface with non-trivial topology, such as a torus […], or using an alternate open boundary condition with smooth and rough boundaries […].
- Fig. 10 (§5), caption:
  > Threshold for the rotated surface code correcting depolarizing errors. Above: Using uniform edge weights, the threshold is 14.88 ± 0.02%, less than the value of 15.5 ± 0.5% obtained using smooth/rough boundary conditions in […].
- Fig. 12 (§6.1), caption:
  > Application of belief propagation/multi-path summation to the decoding of surface codes with smooth/rough boundaries which are subjected to depolarising noise. A similar increase in threshold error rates is observed using these boundary conditions, with a threshold of 15.42 ± 0.01% obtained using a standard MWPM decoder, compatible with the observation of 15.5 ± 0.5% by […].

### Fowler2012 (arXiv v2, published as Phys. Rev. A 86, 032324)

The arXiv submission is a PDF without TeX source, so these excerpts are from the text of that PDF.

- Circuits (Fig. 1 caption):
  > (b) Geometric sequence of operations (left), and quantum circuit (right) for one surface code cycle for a measure-Z qubit, which stabilizes Z_a Z_b Z_c Z_d. (c) Geometry and quantum circuit for a measure-X qubit, which stabilizes X_a X_b X_c X_d. The two identity I operators for the measure-Z process, which are performed by simply waiting, ensure that the timing on the measure-X qubit matches that of the measure-Z qubit, the former undergoing two Hadamard H operations.
- Errors (§VII):
  > The simulations used to generate Fig. 4 include the following types of errors, occurring during the surface code cycle shown in Fig. 1:
  >
  > 1. Attempting to perform a data qubit identity I, but instead performing a single qubit operation X, Y, or Z, each occurring with probability p/3.
  > 2. Attempting to initialize a qubit to |g⟩, but instead preparing |e⟩ with probability p.
  > 3. Attempting to perform a measure qubit Hadamard operation H, but performing in addition one of the single qubit operations X, Y, or Z, each with probability p/3.
  > 4. Performing a measure qubit Z measurement, but reporting the wrong value and projecting to the wrong state with probability p.
  > 5. Attempting to perform a measure qubit-data qubit CNOT, but instead performing one of the two-qubit operations I⊗X, I⊗Y, I⊗Z, X⊗I, X⊗X, X⊗Y, X⊗Z, Y⊗I, Y⊗X, Y⊗Y, Y⊗Z, Z⊗I, Z⊗X, Z⊗Y or Z⊗Z, each with probability p/15.

  > The errors occur randomly during the simulation, with no correlation between errors. The probability p is per step in the surface code cycle (there are eight steps in the cycle used for the simulation (Fig. 1), so the overall rate per cycle of the surface code is approximately 8p, as discussed in more detail in Sect. VII B).
- Logical error rate (§VII and its footnote 14):
  > Edmonds' matching algorithm maps changes detected in the stabilizer outcomes to physical qubit errors; the rate at which the algorithm makes mistakes, meaning it misidentifies the source of a particular error report, is displayed as P_L, the number of X_L errors appearing anywhere in the array, per surface code cycle.

  > There are of course also Z_L errors, occurring at about the same rate as X_L errors; here we are interested in identifying the scaling relation between physical qubit error rate and the resulting logical error rate, a scaling that is very similar for X_L errors and Z_L errors, so we only look at the scaling for X_L errors.
- Value (§VII and Fig. 4 caption):
  > In Fig. 4, which applies to the stabilizer circuits in Fig. 1 simulated with the error sources listed above, the threshold rate is p_th = 0.57%.

  > (a) Numerical simulations of surface code error rates, and how these error rates scale with the distance d of the array. Per-step error rates p less than the per-step threshold error rate of p_th = 0.57% (dashed line) yield surface code logical error rates P_L that vanish rapidly with increasing d. This threshold corresponds to roughly a 4% error rate for the entire surface code measurement cycle.

### Huang2020 (arXiv v1, published as Phys. Rev. A 102, 012419)

- Toric code (§II):
  > This approach straightforwardly generalizes to the open boundaries of the surface code, but we benchmark using periodic boundaries to minimize finite-size effects.
- Noise (§III):
  > In this work, we use a standard depolarizing error model parametrized by a single error parameter p (used e.g. in […]). Our circuits consist of four fundamental noisy gate operations.
  >
  > 1. With probability p, each idling step (identity gate) is followed by a Pauli error drawn uniformly at random from the set {X,Y,Z}.
  > 2. With probability p, each two-qubit CNOT gate is followed by a Pauli error drawn uniformly at random from the set {I,X,Y,Z}^⊗2 ∖ (I ⊗ I).
  > 3. With probability 2p/3, intended preparation of |0⟩ or |+⟩ wrongly prepares |1⟩ or |−⟩, respectively.
  > 4. With probability 2p/3, a measurement outcome in either the Z- or X-basis is flipped.

  > Syndrome extraction for the toric code proceeds in six steps: one preparation step, four two-qubit gates, and a measurement step as shown in Figure 2.
- Rounds and failure (§III):
  > Each trial was decided by performing d rounds of faulty syndrome extraction followed by a terminal perfect round of syndrome extraction. If any nontrivial logical operator was applied to the two encoded qubits, the trial was declared a failure; else, it was declared a success.
- Value (Fig. 3 caption, and Table I, column p_thr: Unweighted MWPM 0.65%, Weighted MWPM 0.72%):
  > Threshold behavior for unweighted (empty) and weighted (filled) decoders using both UF (diamonds) and MWPM (circles). Weighting the UF decoder increases the threshold from ≈0.38% to ≈0.62%, compared with an increase from ≈0.65% to ≈0.72% for MWPM. Each point was obtained from 10^6 trials.

### Higgott2023 (arXiv v5, published as Phys. Rev. X 13, 031007)

- Noise (§III.C and App. D):
  > We compared the performance of belief-matching and belief-find to MWPM and union-find decoders through numerical simulations for the CSS surface code, using a standard circuit-level depolarizing noise model. The details of the noise model are defined in Appendix D (for which we set η = 1 for depolarizing noise).

  > Namely, each two-qubit gate is followed by a two-qubit Pauli channel, for which ZZ, ZI or IZ can occur with probability p/15 each, and the remaining 12 non-trivial two-qubit Paulis can each occur with probability p/(15η). Each single qubit gate location or single qubit idle location of the same duration (a single time step) is followed by a Z error with probability p/3 or an X or Y error each with probability p/(3η). A |+⟩ state is incorrectly prepared as a |−⟩ state with probability 2p/3, and a |0⟩ state is incorrectly prepared as a |1⟩ state with probability 2p/(3η). Each single-qubit X-basis measurement is flipped with probability 2p/3, and each single-qubit Z-basis measurement is flipped with probability 2p/(3η).
- Perfect logical preparation and readout (App. D):
  > Other than for Fig. 13, where we analyse the effect of fragile temporal boundary errors, we assume perfect state preparation and measurement for all other numerical simulations (a perfect round of stabilizer measurements is inserted after perfect initialisation of data qubits, and before perfect logical measurement of the data qubits).
- Value (§III.C and Fig. 4 caption):
  > The MWPM decoder has previously had the highest reported circuit-level threshold for the surface code, which we find to be 0.817(5)% for our noise model.

  > Threshold of the square, CSS surface code using MWPM (left) and belief-matching (right) with η = 1 depolarising noise. The logical failure rate is the probability that a logical X measurement outcome is flipped after preparing in an X eigenstate followed by L rounds of stabilizer measurements.

### Gidney2021Honeycomb (arXiv v2, published as Quantum 5, 605)

- SD6 (§2, Table 2): the SD6 column lists the noisy gate set CX(p), AnyClifford_1(p), Init_Z(p), M_Z(p) and Idle(p). Caption:
  > The three noisy gate sets investigated in this paper. See Table 1 for the exact definitions of the noisy gates.

  > Note that we still call SD6 "SD6" when applying it to the surface code, even though for this model the surface code cycle takes 8 time steps instead of 6.
- Decoder (§3):
  > The second is an in-house minimum-weight perfect-matching decoder that uses correlations to enhance performance […].
- Rounds (Fig. 5 caption):
  > We simulate 3d rounds (but report the error rate per d rounds) to minimize time-boundary effects.
- Value (§4):
  > In the standard circuit model SD6, we observe a threshold within 0.2%−0.3% for the honeycomb code, which compares with a surface code threshold within 0.5%−0.7%.

### Hetenyi2024 (arXiv v2, published as Phys. Rev. A 109, 032433)

- Isotropic noise (§2.3):
  > In that case Eq. (10) implies that the isotropic circuit level noise (p_G = p_T = p_RR = p) threshold can be recovered as p_ic^−1 = (p^th_G)^−1 + (p^th_T)^−1 + (p^th_RR)^−1, whereas the threshold for the phenomenological noise model (p_T = p_RR = p) is p_ph^−1 = (p^th_T)^−1 + (p^th_RR)^−1.
- Value and spin-qubit circuits (§4.4):
  > Finally we make some quantitative comparisons to values found in the literature for the different QEC codes. disregarding the finite idling bias, for the rotated surface code in the presence of isotropic circuit level noise we get p_ic = 0.65% and for the phenomenological noise model p_ph = 3.1% is obtained, which are in line with the expectations […].

  > Some deviations are to be expected for these threshold values due to the differences in the stabilizer measurement protocol, e.g., the use of pair-wise ancilla readout and the additional SWAP gates.

### Etxezarreta2025 (arXiv v1, published as Phys. Rev. Applied 25, 014021)

- Circuits (App. D):
  > For this rotated XZZX code in consideration, we will use sequences of CNOT and CZ gates to measure the stabilisers by means of the check qubits, which will be prepared and measured in the Z-basis and converted to the X-basis by means of Hadamard gates.
- Noise (§III.A and App. E):
  > Note that here we refer to the standard depolarizing circuit-level noise model with an η = 1/2.

  > The hybrid biased-depolarizing circuit-level noise model is defined by the tuple of parameters physical error rate, p, and bias, η, as:
  >
  > - Hadamard gates are followed by single-qubit depolarizing errors at rate p, i.e. each X,Y or Z error occurs with probability p/3.
  > - CNOT (or CY) gates are followed by two-qubit depolarizing errors at rate p, i.e. each error from the set {I,X,Y,Z}^⊗2/I^⊗2 occurs with probability p/15.
  > - CZ gates are followed by two-qubit biased Pauli errors with bias η at rate p. Specifically, each pure dephasing error {ZI,IZ,ZZ} occurs with probability ηp/(3(1+η)), while the rest occur with probability p/(12(1+η)).
  > - Preparing a state in the |0⟩ (|+⟩) state instead results in preparing the orthogonal state |1⟩ (|−⟩) with probability p.
  > - Measurement results in the X or Z basis experience a flip reporting an incorrect outcome with probability p.
  > - Idling steps experience single-qubit biased Pauli errors with bias η at rate p. Specifically, Z errors occur with probability ηp/(1+η), while X and Y errors each occur with probability p/(2(1+η)).
- Metric, rounds and decoder (App. G):
  > The operational figure of merit we use to evaluate the performance is the logical error probability, p_L, per extraction round. We ran 3d rounds of syndrome extraction to reduce time-boundary edge effects coming from the fact that the first and last extraction rounds are less noisy than the ones in the bulk […]. Once the circuits are run to collect the samples, we use the pymatching implementation the minimum-weight perfect-matching (MWPM) decoder in order to aim recovery and determine if a logical error has occurred or not […].
- Value (Fig. 2 caption, and Tables II and III, row "1/2 (SD)": 0.66%):
  > Threshold of the rotated XZZX code as a function of the system bias for the HBD circuit-level noise model with and without bias-preserving CZ gates. a) Bias-preserving CZ gates. The threshold improved from around 0.66% for the SD noise model up to 0.93% when η ≥ 100.

  > Improvement of the threshold as a function of the bias for the HBD circuit-level noise model.

  > Improvement of the threshold as a function of the bias for the HBD circuit-level noise model and CNOT gates exhibiting residual bias as studied in Section II.
