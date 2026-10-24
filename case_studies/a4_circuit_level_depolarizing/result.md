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

The other studies make up the 0.50–0.82% band:

| Key | Paper | Where | Value | Main difference |
|---|---|---|---|---|
| Fowler2012 | [arXiv:1208.0928](https://arxiv.org/abs/1208.0928) | P_L-vs-p figure | 0.57% | Depth-8 circuits with H gates; per round, not per d rounds (Stephens2014 Table I) |
| Huang2020 | [arXiv:2004.04693](https://arxiv.org/abs/2004.04693) | §III, Fig. 3, Table 1 | 0.65% (unweighted), 0.72% (weighted) | Toric code; preparation and measurement at 2p/3; a perfect last round |
| Higgott2023 | [arXiv:2203.04948](https://arxiv.org/abs/2203.04948) | §III.C, Fig. 4 | 0.817(5)% | Preparation and measurement at 2p/3; perfect logical preparation and readout |
| Gidney2021Honeycomb | [arXiv:2108.10457](https://arxiv.org/abs/2108.10457) | §IV, Fig. 5 | 0.5–0.7% (SD6) | 8-step cycle with H gates; 3d rounds; correlated MWPM |
| Hetenyi2024 | [arXiv:2306.17786](https://arxiv.org/abs/2306.17786) | §IV.4 | 0.65% (isotropic) | Spin-qubit circuits |
| Etxezarreta2025 | [arXiv:2505.17718](https://arxiv.org/abs/2505.17718) | Fig. 2, Tables 2–3 | about 0.66% (XZZX under SD, equal to CSS) | H gates; 3d rounds |

## Setup

- Config: [config.yaml](config.yaml).
- Code: `rotated_surface`.
- `circuit_level` with `depolarizing` noise and `p_meas: same_as_p`, over d rounds.
- Decoder: `mwpm`
- d = 7, 9, 11, 13, 15. Bases X and Z. p = 0.55–0.85% in steps of 0.025%.
- Each point ran to 20,000 errors or 10⁶ shots (15,218–23,347 errors).
- Fit: quadratic FSS on d = 9–15, as in Stephens2014, with x_window = 0.015 and ν0 = 1.06. Errors are 1σ from the fit covariance.

## Result

From [results/threshold.csv](results/threshold.csv):

| Code | Basis | p_th (%) | ν | χ²_red |
|---|---|---|---|---|
| rotated_surface | X | 0.6937 ± 0.0009 | 1.17 | 0.88 |
| rotated_surface | Z | 0.6931 ± 0.0009 | 1.13 | 1.38 |

- X and Z agree: they differ by 0.0006 ± 0.0013 points.
- Other distance sets (d = 7–15, 11–15) and windows (x_window = 0.008–0.02) give 0.692–0.698%.

## Verdict

- **Literature band (0.50–0.82%): pass.**
- **Stephens2014 (0.672%): close, 3.1% (0.021 points) above.**
  - The layout and the time boundaries do not explain it.
  - The cause is not identified. The remaining difference is the decoder implementation, which has not been checked.
- **ORourke2025 (0.565%): lower, as expected from the two extra H layers in its round.**
