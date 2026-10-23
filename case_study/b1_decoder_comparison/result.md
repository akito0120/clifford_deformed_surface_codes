# B1: Decoder comparison at code capacity

## Prior studies

| Key | Paper | Where | Value | Conditions |
|---|---|---|---|---|
| Criger2018 | B. Criger and I. Ashraf, "Multi-path summation for decoding 2D topological codes" [arXiv:1709.02154](https://arxiv.org/abs/1709.02154) | Fig. 7 (§4), Fig. 10 (§5) | Independent flips: MWPM 9.97 ± 0.01%, path-counting MWPM 10.34 ± 0.01%. Depolarizing: MWPM 14.88 ± 0.02%, BP with multi-path summation 17.76 ± 0.02% | Rotated code, d = 7, 11, 15, 19, 23, 25 values of p per figure. BP runs d iterations. A shot fails on either logical |
| LinLai2025 | T.-H. Lin and C.-Y. Lai, "Union-Intersection Union-Find for Decoding Depolarizing Errors in Topological Codes" [arXiv:2506.14745](https://arxiv.org/abs/2506.14745) | Table IV (§V-B), Table V (§V-C) | Rotated code, depolarizing: UF 14.68%, UF with weighted growth 15.03%, MWPM 15.19% | Their own UF: every invalid cluster grows by half-edges, then peeling (§II-D). UF counts any logical error, MWPM the logical X error; the paper calls the two estimates very close. 10⁶ samples per point; distances not stated |
| Delfosse2021 | N. Delfosse and N. H. Nickerson, "Almost-linear time decoding algorithm for topological codes" [arXiv:1709.06218](https://arxiv.org/abs/1709.06218) | Table 1, §5 | Toric code, phase flips: UF 9.2% (uniform growth), 9.9% (smallest cluster first); MWPM 10.3% | Half-edge growth and peeling; at least 10⁴ failures per point |
| deMartiIOlius2024 | A. de Martí i Olius et al., "Decoding algorithms for surface codes" [arXiv:2307.14989](https://arxiv.org/abs/2307.14989) | Tables 1 and 2 | Rotated code, η = 0.5: UF 11.6%, MWPM 14.0% | Review; distances and implementations not stated |
| Campos2026 | J. A. Campos and K. R. Brown, "Clifford-deformed compass codes" [arXiv:2412.03808](https://arxiv.org/abs/2412.03808) | Table 1, CSS, η = 100 | MWPM 10.0% | Rotated code (ℓ = 2), d = 11–19, either logical. At η = 100 the Z component flips at 0.995p, i.e. about 9.95% at η = ∞ |

- No decoder may exceed the optimal thresholds: 18.9% for depolarizing noise (Bombin2012) and 10.93% for independent flips (Wang2003).

## Setup

- Configs, one per noise and decoder: [config_depolarizing_bp.yaml](config_depolarizing_bp.yaml), [config_depolarizing_uf.yaml](config_depolarizing_uf.yaml), [config_dephasing_mwpm.yaml](config_dephasing_mwpm.yaml), [config_dephasing_bp.yaml](config_dephasing_bp.yaml), [config_dephasing_uf.yaml](config_dephasing_uf.yaml).
- `rotated_surface`, `code_capacity`, d = 7, 11, 15, 19, 23, p in steps of 0.2 points around each threshold.
  - Depolarizing: `depolarizing`, Z basis. The MWPM reference is A1's Z basis.
  - Independent Z flips: `biased` with η = ∞, X basis.
- Each point ran to 10,000 errors (`bp`) or 20,000 (others), with 0.5–3.3 × 10⁵ shots.
- Fit: quadratic FSS on d = 7–23 with x_window = 0.1, ν0 = 1.5 (depolarizing) and 1.46 (independent flips).
- `results/*/suppression.csv` comes from the sweep the config schema requires and is not a result.

## Result

From `results/*/threshold.csv` and A1's [results/threshold.csv](../a1_code_capacity_depolarizing/results/threshold.csv):

| Noise | Decoder | p_th (%) | ν | χ²_red | Ratio to MWPM | p_th, d = 11–23 (%) |
|---|---|---|---|---|---|---|
| Depolarizing | `mwpm` (A1) | 14.973 ± 0.013 | 1.59 | 2.12 | — | 15.090 |
| Depolarizing | `bp` | 17.649 ± 0.025 | 1.67 | 0.94 | 1.179 | 17.657 |
| Depolarizing | `uf` | 13.380 ± 0.013 | 1.63 | 1.56 | 0.894 | 13.459 |
| Independent Z | `mwpm` | 9.972 ± 0.010 | 1.61 | 2.06 | — | 10.035 |
| Independent Z | `bp` | 10.311 ± 0.016 | 1.67 | 2.52 | 1.034 | 10.441 |
| Independent Z | `uf` | 8.813 ± 0.010 | 1.62 | 2.15 | 0.884 | 8.878 |

- Without d = 7, χ²_red falls to 1.0–1.3.

## Verdict

- **`mwpm`, independent Z: pass.** 9.972 ± 0.010% against Criger2018's 9.97 ± 0.01%, the equivalent setting, and Campos2026's 10.0%.
- **`bp`, depolarizing: pass.** Between MWPM and 18.9%. 0.11 points below Criger2018's 17.76%, a different algorithm counting either logical, with the same gain over MWPM (1.18 against 1.19).
- **`bp`, independent Z: pass.** 3.4% above MWPM, close to the 3.7% gain of Criger2018's path counting, and below 10.93%. Most of `bp`'s depolarizing gain (+18%) therefore comes from the X–Z correlation of Y errors.
- **`uf`, depolarizing: pass.** Below MWPM, and inside the published UF range (11.6–14.68%; ratios 0.83–0.966).
- **`uf`, independent Z: pass.** Its ratio to MWPM, 0.884, is within 1% of Delfosse2021's uniform growth (0.893). LinLai2025's uniform-growth UF keeps 0.966, so UF thresholds depend on the implementation.
