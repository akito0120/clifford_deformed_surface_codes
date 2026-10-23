# A1: Depolarizing code-capacity threshold

## Prior studies

| Key | Paper | Where | Value | Conditions |
|---|---|---|---|---|
| Criger2018 | B. Criger and I. Ashraf, "Multi-path summation for decoding 2D topological codes" [arXiv:1709.02154](https://arxiv.org/abs/1709.02154) | Fig. 7 (top), §4 | 9.97 ± 0.01%, i.e. 14.95 ± 0.02% at p = 1.5q | Rotated code, independent X and Z flips (probability q each), perfect measurement, MWPM with Manhattan-distance (unit) weights, d = 7, 11, 15, 19, 23, q = 0.08–0.13 (25 points) |
| Criger2018 | (same) | Fig. 10 (top), §5 | 14.88 ± 0.02% | The same, with depolarizing noise, p = 0.13–0.18 (25 points) |
| Campos2026 | J. A. Campos and K. R. Brown, "Clifford-deformed compass codes" [arXiv:2412.03808](https://arxiv.org/abs/2412.03808) | Table 1, ℓ = 2, η = 0.5 | 14.8%, one value for CSS and the deformed codes (uncertainty ≤ 0.8%) | Code capacity, PyMatching with weights log((1−p)/p), quadratic FSS fit, d = 11–19 (CSS) and 27–43 (deformed codes) |

- **Both papers count a failure of either logical operator.**
  - A shot fails whenever the residual error is a non-trivial logical, X, Y or Z.
  - Criger2018's code returns I, X, Y or Z for the residual and counts everything but I.
  - Campos2026 checks "whether the residual error is trivial" (§Methods).
- **Fig. 7 is the equivalent reference for one basis.**
  - In one memory basis, the decoder sees one component of each qubit's error: Z for the X basis.
  - Under depolarizing noise, that component appears with probability p_Z + p_Y = 2p/3, independently on each qubit. MWPM decodes it on its own graph with uniform weights. That is Criger2018's independent-flip problem at q = 2p/3.


## Setup

- Config: [config.yaml](config.yaml).
- Codes: `rotated_surface`, `xzzx` and `xy`.
- `code_capacity` with `depolarizing` noise.
- Decoder: `mwpm`
- d = 7, 11, 15, 19, 23. Bases X and Z. p = 0.136–0.164 in steps of 0.002.
- Each point ran to at least 20,000 errors (20,000–26,513).
- Fit: quadratic FSS with x_window = 0.1 and ν0 = 1.5. Errors are 1σ from the fit covariance.

## Result

From [results/threshold.csv](results/threshold.csv):

| Code | Basis | p_th (%) | ν | χ²_red |
|---|---|---|---|---|
| rotated_surface | X | 14.962 ± 0.013 | 1.61 | 2.48 |
| rotated_surface | Z | 14.973 ± 0.013 | 1.59 | 2.12 |
| xzzx | X | 14.946 ± 0.013 | 1.56 | 1.75 |
| xzzx | Z | 14.965 ± 0.013 | 1.58 | 2.10 |
| xy | X | 14.962 ± 0.014 | 1.66 | 2.06 |
| xy | Z | 14.955 ± 0.013 | 1.59 | 2.04 |

- Weighted mean: 14.961 ± 0.005%.
- Spread: 0.028 points.


## Verdict

- **Clifford invariance: pass.** The six series agree point by point and in p_th, and their DEMs have the same structure at every simulated distance.
- **Criger2018 Fig. 7 (1.5 × (9.968 ± 0.012)% = 14.952 ± 0.018%): consistent within its stated uncertainty.**
- **Criger2018 Fig. 10 (14.88%): consistent, with a different metric.**
  - Fig. 10 counts a failure of either logical operator.
  - The 0.08-point difference splits into the failure criterion, the p range and the fit method.
- **Campos2026 (14.8%): consistent within its stated uncertainty.**
