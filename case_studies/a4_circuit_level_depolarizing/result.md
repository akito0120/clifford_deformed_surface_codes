# A4: Depolarizing circuit-level threshold

## Prior studies

| Key | Paper | Where | Value | Conditions |
|---|---|---|---|---|
| ORourke2025 | A. R. O'Rourke and S. Devitt, "Compare the Pair: Rotated vs. Unrotated Surface Codes at Equal Logical Error Rates," *Phys. Rev. Research* **7**, 033074 (2025) [arXiv:2409.14765](https://arxiv.org/abs/2409.14765) | Table III (SD, rotated), and the released statistics ([compare_the_pair](https://github.com/wamud/compare_the_pair): `SD_stats.pickle`) | 0.5637 ± 0.0004%, ν = 1.09 ± 0.03 | SD noise, whose round adds two H layers (H, 4 CNOT, H, MR), 3d rounds, memory Z, PyMatching. Fit on d = 8–22 (odd and even) and p = 0.55–0.58% |

- **The plugins [codes.py](codes.py) and [noises.py](noises.py) rebuild ORourke2025's round.** A gate-free step stands in for the first H layer, and the second is folded into the measurement flip, 5p/3 − 4p²/3. What differs: the CNOT order, one extra data idle layer before the first round, and one data qubit per round that the released circuits leave without an idle error during MR (possibly a bug in their idle insertion; the intent is unknown).

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
- p = ORourke2025's nine values near the threshold: 0.49, 0.50, 0.51, 0.52, 0.55, 0.56, 0.57, 0.58, 0.60%
- Decoder: `mwpm`
- Each point ran to 5,000 errors (the 5 × 10⁵-shot limit was never reached)
- Fit: d = 9–21, x_window = 0.014 (covers every point), ν0 = 1.06
- Suppression: required by the schema, not used
- ORourke2025's data: [convert_orourke2025.py](convert_orourke2025.py) converts [SD_stats.pickle](SD_stats.pickle) to [results/orourke2025_samples.csv](results/orourke2025_samples.csv)

## Result

From [results/threshold.csv](results/threshold.csv):

| Code | Basis | p_th (%) | ν | χ²_red | Compare against |
|---|---|---|---|---|---|
| rotated_surface_sd | Z | 0.5644 ± 0.0009 | 1.16 | 1.12 | ORourke2025 (0.5637 ± 0.0004%, ν = 1.09 ± 0.03) |


## Verdict

- **Literature band (0.50–0.82%): pass.**
- **ORourke2025 Table III (0.5637 ± 0.0004%): pass, 0.0007 points (0.13%) above, 0.7σ.**
- **p_L on the 63 points shared with ORourke2025's data: pass, 1.0034 ± 0.0017 times theirs.**
