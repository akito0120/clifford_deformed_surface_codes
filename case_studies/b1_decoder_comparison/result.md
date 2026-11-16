# B1: Decoder comparison at code capacity

## Prior studies

| Key | Paper | Where | Value | Conditions |
|---|---|---|---|---|
| Criger2018 | B. Criger and I. Ashraf, "Multi-path summation for decoding 2D topological codes" [arXiv:1709.02154](https://arxiv.org/abs/1709.02154) | Fig. 7 (§4), Fig. 10 (§5) | Independent flips: MWPM 9.97 ± 0.01%, path-counting MWPM 10.34 ± 0.01%. Depolarizing: MWPM 14.88 ± 0.02%, BP with multi-path summation 17.76 ± 0.02% | Rotated code, d = 7, 11, 15, 19, 23, 25 values of p per figure. BP runs d iterations. A shot fails on either logical |
| LinLai2025 | T.-H. Lin and C.-Y. Lai, "Union-Intersection Union-Find for Decoding Depolarizing Errors in Topological Codes" [arXiv:2506.14745](https://arxiv.org/abs/2506.14745) | Table IV (§V-B), Table V (§V-C) | Rotated code, depolarizing: UF 14.68%, UF with weighted growth 15.03%, MWPM 15.19% | UF (§II-D): every invalid cluster grows by half-edges, then peeling. UF counts any logical error, MWPM the logical X error; the paper calls the two estimates very close. 10⁶ samples per point; distances not stated |
| Delfosse2021 | N. Delfosse and N. H. Nickerson, "Almost-linear time decoding algorithm for topological codes" [arXiv:1709.06218](https://arxiv.org/abs/1709.06218) | Table 1, §5 | Toric code, phase flips: UF 9.2% (uniform growth), 9.9% (smallest cluster first); MWPM 10.3%, cited from Dennis2002 | Half-edge growth and peeling; at least 10⁴ failures per point |
| deMartiIOlius2024 | A. de Martí i Olius et al., "Decoding algorithms for surface codes" [arXiv:2307.14989](https://arxiv.org/abs/2307.14989) | Tables 1 and 2 | Rotated code, η = 0.5: UF 11.6%, MWPM 14.0% | Review. d = 3–11, any logical error, N_runs = 100/P_L. MWPM from QECSIM, UF coded by the authors (App. C) |
| Campos2026 | J. A. Campos and K. R. Brown, "Clifford-deformed compass codes" [arXiv:2412.03808](https://arxiv.org/abs/2412.03808) | Table 1, CSS, η = 100 | MWPM 10.0% | Rotated code (ℓ = 2), d = 11–19, either logical. At η = 100 the Z component flips at 0.995p, i.e. about 9.95% at η = ∞ |

- No decoder may exceed the optimal thresholds: 18.9% for depolarizing noise (Bombin2012) and 10.93% for independent flips (Merz and Chalker, quoted in Wang2003).

## Setup

- Configs, one per noise and decoder:
  - [config_depolarizing_bp.yaml](config_depolarizing_bp.yaml)
  - [config_depolarizing_uf.yaml](config_depolarizing_uf.yaml)
  - [config_dephasing_mwpm.yaml](config_dephasing_mwpm.yaml)
  - [config_dephasing_bp.yaml](config_dephasing_bp.yaml)
  - [config_dephasing_uf.yaml](config_dephasing_uf.yaml)
- `rotated_surface`, `code_capacity`
- Sampled at d = 7, 11, 15, 19, 23; fit on d = 11, 15, 19, 23
- p in steps of 0.2 points around each threshold
- Depolarizing: `depolarizing`, Z basis. The MWPM reference is [A1](../a1_code_capacity_depolarizing/result.md)'s Z-basis samples, refit on d = 11–23 by [stats.py](stats.py).
- Independent Z flips: `biased` with η = inf, X basis
- Each point ran to 10,000 errors (`bp`) or 20,000 (others), with 0.5–3.3 × 10⁵ shots.
- `results/*/suppression.csv` comes from the sweep the config schema requires and is not a result.

## Result

From `results/*/threshold.csv` and [results/stats.txt](results/stats.txt) (A1's refit and the ratios):

| Noise | Decoder | p_th (%) | ν | χ²_red | Ratio to MWPM | Compare against |
|---|---|---|---|---|---|---|
| Depolarizing | `mwpm` (A1) | 15.090 ± 0.019 | 1.58 | 1.23 | — | Criger2018 Fig. 7 (14.952%) and Campos2026 (14.8%) |
| Depolarizing | `bp` | 17.657 ± 0.038 | 1.75 | 1.05 | 1.170 | Criger2018 (1.19 gain) |
| Depolarizing | `uf` | 13.459 ± 0.018 | 1.61 | 1.03 | 0.892 | published range (0.83–0.966 gain) |
| Independent Z | `mwpm` | 10.035 ± 0.015 | 1.59 | 1.21 | — | Criger2018 (9.97%), Campos2026 (10.0%) |
| Independent Z | `bp` | 10.441 ± 0.024 | 1.62 | 1.32 | 1.040 | Criger2018 (1.037 gain) |
| Independent Z | `uf` | 8.878 ± 0.014 | 1.63 | 1.33 | 0.885 | Delfosse2021 (0.893 gain) |

## Verdict

- **`bp`, depolarizing: pass.** Between MWPM and 18.9%. 0.10 points below Criger2018's 17.76%, a different algorithm counting either logical; its gain over MWPM is 1.17 against Criger2018's 1.19.
- **`bp`, independent Z: pass.** 4.0% above MWPM, close to the 3.7% gain of Criger2018's path counting, and below 10.93%. Most of `bp`'s depolarizing gain (+17%) therefore comes from the X–Z correlation of Y errors.
- **`uf`, depolarizing: pass.** Below MWPM, and inside the published range (11.6–14.68%; 0.83–0.966 gain).
- **`uf`, independent Z: pass.** Its ratio to MWPM, 0.885, is within 1% of Delfosse2021's uniform growth (0.893). LinLai2025's uniform-growth UF keeps 0.966, so UF thresholds depend on the implementation.
