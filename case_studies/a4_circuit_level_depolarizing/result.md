# A4: Depolarizing circuit-level threshold

## Prior studies

| Key | Paper | Where | Value | Conditions |
|---|---|---|---|---|
| ORourke2025 | A. R. O'Rourke and S. Devitt, "Compare the Pair: Rotated vs. Unrotated Surface Codes at Equal Logical Error Rates" [arXiv:2409.14765](https://arxiv.org/abs/2409.14765) | §IV.B | 0.565%, the same for the rotated and the worst-case unrotated code | SD noise, whose round adds two H layers (H, 4 CNOT, H, MR), 3d rounds, memory Z, PyMatching |
<!-- | Stephens2014 | A. M. Stephens, "Fault-tolerant thresholds for quantum error correction with the surface code" [arXiv:1311.5003](https://arxiv.org/abs/1311.5003) | §V.C and Table I, depth-6 circuits, standard noise model | 0.672 ± 0.001% (ν0 = 1.06) | Unrotated planar code, odd d = 3–17 with the fit on d ≥ 9, d rounds, p_L per d rounds, X-error threshold. Preparation, CNOT, measurement and idle (identity-gate) errors all at p. Each ancilla is prepared and measured in its check's basis, without H gates. MWPM (Blossom V) with circuit-derived weights, X and Z decoded separately. About 10⁶ instances and at least 10⁴ logical errors per point | -->

<!-- - **Stephens2014's depth-6 round is the framework's round.**
  - Reset, four two-qubit gates and measurement, with the same error rates. Idle qubits get identity gates that fail with p, as the framework's idle noise does.
  - Under depolarizing noise, the framework's CZ onto a |+⟩ ancilla is the same as a CNOT onto a |0⟩ ancilla.
  - What differs: the unrotated layout, the decoder implementation, and the time boundaries, which Stephens2014 does not describe. The framework's data preparation and readout fail with p.  
- **The layout should not raise the rotated threshold.** At circuit level, the rotated and the worst-case unrotated code have the same threshold (ORourke2025). At code capacity, the unrotated one is higher (Criger2018: 15.42% against 14.88%). -->
- **A5's plugins rebuild ORourke2025's round.** A gate-free step stands in for the first H layer, and the second is folded into the measurement flip, 5p/3 − 4p²/3. What differs: d rounds instead of 3d, the CNOT order, and one extra data idle layer before the first round.

---

The other studies make up the **0.50–0.82%** band:

| Key | Paper | Where | Value | Main difference |
|---|---|---|---|---|
| Fowler2012 | [arXiv:1208.0928](https://arxiv.org/abs/1208.0928) | §VII, Fig. 4 | 0.57% | Depth-8 circuits with H gates; per round, not per d rounds (Stephens2014 Table I) |
| Huang2020 | [arXiv:2004.04693](https://arxiv.org/abs/2004.04693) | §III, Fig. 3, Table I | 0.65% (unweighted), 0.72% (weighted) | Toric code; preparation and measurement at 2p/3; a perfect last round |
| Higgott2023 | [arXiv:2203.04948](https://arxiv.org/abs/2203.04948) | §III.C, Fig. 4 | 0.817(5)% | Preparation and measurement at 2p/3; perfect logical preparation and readout |
| Gidney2021Honeycomb | [arXiv:2108.10457](https://arxiv.org/abs/2108.10457) | §4, Fig. 5 | 0.5–0.7% (SD6) | 8-step cycle with H gates; 3d rounds; correlated MWPM |
| Etxezarreta2025 | [arXiv:2505.17718](https://arxiv.org/abs/2505.17718) | Fig. 2, Tables II–III | about 0.66% (XZZX under SD) | H gates; CZ noise still biased under its SD (η = 1/2); 3d rounds; p_L per round |
<!-- | Hetenyi2024 | [arXiv:2306.17786](https://arxiv.org/abs/2306.17786) | §4.4 | 0.65% (isotropic) | Spin-qubit circuits | -->

## Setup

- Config: [config_sd.yaml](config_sd.yaml)
- Code: `rotated_surface_sd`
- Noise model: `circuit_level`
- Noise: `depolarizing_sd`
- Bases: only Z
- d = 7, 9, 11, 13, 15
- p = 0.44–0.68% in steps of 0.02%
- Decoder: `mwpm`
- Each point ran to 20,000 errors or 10⁶ shots
- Suppression: required by the schema, not used

<!-- - Stephens2014:
  - Config: [config.yaml](config.yaml)
  - Code: `rotated_surface`
  - Bases: X and Z
  - p = 0.55–0.85% in steps of 0.025% -->


## Result

From [results_sd/threshold.csv](results_sd/threshold.csv):

| Code | Basis | p_th (%) | ν | χ²_red | Compare against |
|---|---|---|---|---|---|
| rotated_surface_sd | Z | 0.5687 ± 0.0007 | 1.14 | 1.12 | ORourke2025 (0.565%) |
<!-- | rotated_surface | X | 0.6937 ± 0.0009 | 1.17 | 0.88 | Stephens2014, (0.672%) |
| rotated_surface | Z | 0.6931 ± 0.0009 | 1.13 | 1.38 | Stephens2014, (0.672%) | -->

<!-- - `rotated_surface` X and Z agree: they differ by 0.0006 ± 0.0013 points. -->
- Other distance sets (d = 7–15, 11–15) and windows (x_window = 0.008–0.02) give 0.568–0.572%.
  <!-- - 0.692–0.698% for `rotated_surface`
  - 0.568–0.572% for `rotated_surface_sd` -->

## Verdict

- **Literature band (0.50–0.82%): pass.**
- **ORourke2025 (0.565%): pass, 0.7% (0.004 points) above.**
<!-- - **Stephens2014 (0.672%): close, 3.1% (0.021 points) above.**
  - The layout and the time boundaries do not explain it.
  - The cause is not identified. The remaining difference is the decoder implementation, which has not been checked. -->
