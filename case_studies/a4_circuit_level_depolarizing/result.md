# A4: Depolarizing circuit-level threshold

## Prior studies

| Key | Paper | Where | Value | Conditions |
|---|---|---|---|---|
| ORourke2025 | A. R. O'Rourke and S. Devitt, "Compare the Pair: Rotated vs. Unrotated Surface Codes at Equal Logical Error Rates" [arXiv:2409.14765](https://arxiv.org/abs/2409.14765) | §IV.B | 0.565%, the same for the rotated and the worst-case unrotated code | SD noise, whose round adds two H layers (H, 4 CNOT, H, MR), 3d rounds, memory Z, PyMatching. Fit on d = 8–22 (odd and even) and p = 0.55–0.58% |

- **A5's plugins rebuild ORourke2025's round.** A gate-free step stands in for the first H layer, and the second is folded into the measurement flip, 5p/3 − 4p²/3. What differs: the CNOT order, one extra data idle layer before the first round, and one data qubit per round that the released circuits leave without an idle error during MR (possibly a bug in their idle insertion; the intent is unknown).

---

The other studies make up the **0.50–0.82%** band:

| Key | Paper | Where | Value | Main difference |
|---|---|---|---|---|
| Fowler2012 | [arXiv:1208.0928](https://arxiv.org/abs/1208.0928) | §VII, Fig. 4 | 0.57% | Depth-8 circuits with H gates; per round, not per d rounds (Stephens2014 Table I) |
| Huang2020 | [arXiv:2004.04693](https://arxiv.org/abs/2004.04693) | §III, Fig. 3, Table I | 0.65% (unweighted), 0.72% (weighted) | Toric code; preparation and measurement at 2p/3; a perfect last round |
| Higgott2023 | [arXiv:2203.04948](https://arxiv.org/abs/2203.04948) | §III.C, Fig. 4 | 0.817(5)% | Preparation and measurement at 2p/3; perfect logical preparation and readout |
| Gidney2021Honeycomb | [arXiv:2108.10457](https://arxiv.org/abs/2108.10457) | §4, Fig. 5 | 0.5–0.7% (SD6) | 8-step cycle with H gates; 3d rounds; correlated MWPM |
| Etxezarreta2025 | [arXiv:2505.17718](https://arxiv.org/abs/2505.17718) | Fig. 2, Tables II–III | about 0.66% (XZZX under SD) | H gates; CZ noise still biased under its SD (η = 1/2); 3d rounds; p_L per round |

## Setup

- Config: [config.yaml](config.yaml)
- Code: `rotated_surface_sd`
- Noise model: `circuit_level`
- Noise: `depolarizing_sd`
- Bases: only Z
- 3d rounds
- d = 9, 11, …, 21.
- p = 0.50–0.62%, 10 points
- Decoder: `mwpm`
- Each point ran to 5,000 errors (the 5 × 10⁵-shot limit was never reached)
- Fit: d = 9–21, x_window = 0.012 (covers every point), ν0 = 1.06
- Suppression: required by the schema, not used

<!-- - Stephens2014:
  - Config: [config.yaml](config.yaml)
  - Code: `rotated_surface`
  - Bases: X and Z
  - p = 0.55–0.85% in steps of 0.025% -->


## Result

From [results/threshold.csv](results/threshold.csv):

| Code | Basis | p_th (%) | ν | χ²_red | Compare against |
|---|---|---|---|---|---|
| rotated_surface_sd | Z | 0.5661 ± 0.0008 | 1.17 | 1.17 | ORourke2025 (0.565%) |


- Other windows (x_window = 0.006–0.02) give 0.5653–0.5661%.
- At the 14 points shared with ORourke2025's data ([SD_stats.pickle](../a5_suppression_circuit_level/SD_stats.pickle)), p_L is 1.007 ± 0.004 times theirs.


## Verdict

- **Literature band (0.50–0.82%): pass.**
- **ORourke2025 (0.565%): pass, 0.19% (0.0011 points) above.**
