# A2: Phenomenological threshold against bias

## Prior studies

| Key | Paper | Where | Value | Conditions |
|---|---|---|---|---|
| BonillaAtaides2021 | J. P. Bonilla Ataides, D. K. Tuckett, S. D. Bartlett, S. T. Flammia and B. J. Brown, "The XZZX surface code" [arXiv:2009.07851](https://arxiv.org/abs/2009.07851) | Fig. 5(e) | CSS reference line p_hr + p_lr = 2.9%. The XZZX threshold rises with η, to about 10% at high bias | Toric d×d code, d rounds with periodic time, measurement flips q = p_hr + p_lr, MWPM, d = 12–20 at finite bias, 3 × 10⁴ samples per point |
| Campos2026 | J. A. Campos and K. R. Brown, "Clifford-deformed compass codes" [arXiv:2412.03808](https://arxiv.org/abs/2412.03808) | Fig. 6, ℓ = 2 | CSS (a): 4.4, 3.2, 3.0, 2.9, 2.9, 2.9%. XZZX (b): 4.4, 5.1, 5.6, 6.3, 6.9, 7.4%. Both at η = 0.5, 5, 10, 25, 50, 100, each ±0.2 points | Rotated code, measurement flips p_Y + p_Z, a perfect last round, PyMatching, quadratic FSS fit, "distances up to 40" |

- **Both papers count a failure of either logical operator.**
  - Campos2026 checks "whether the residual error is trivial" (§Methods).
  - BonillaAtaides2021 also counts a non-trivial cycle along the time axis.
  - The framework counts one memory basis.
- **The CSS reference line is not a simulation.**
  - It is Wang2003's 2.9% for independent flips, written as p_hr + p_lr = 2.9%.
  - In terms of p it is p_th(η) = 2.9% × 2(η + 1)/(2η + 1). That gives 4.350, 3.038, 2.957, 2.929, 2.914 and 2.900% at η = 0.5, 10, 25, 50, 100 and ∞.
- Campos2026's values were read from the vector PDF of Fig. 6 in its arXiv source (v3) into [Campos2026_fig6_l2.csv](Campos2026_fig6_l2.csv).
- BonillaAtaides2021's XZZX curve is compared in trend only, because of its periodic boundaries.

## Setup

- Configs: [config_css.yaml](config_css.yaml) and [config_xzzx.yaml](config_xzzx.yaml).
- Codes:
  - `rotated_surface` with η = 0.5, 10, 25, 50, 100, ∞.
  - `xzzx` with η = 0.5, 10, 25, 50, 100.
- `phenomenological` noise with the plugin `biased_meas_yz` from [noises.py](noises.py).
  - It is the built-in `biased` noise, with measurement flips at p_Y + p_Z instead of p.
  - d noisy rounds are followed by a data readout flipped at the same rate. Campos2026 makes its last round perfect instead.
- Decoder: `mwpm`
- d = 11, 13, 15, 17, 19.
- p:
  - CSS: 11 points per η around the reference line.
  - XZZX: 9 points per (η, basis) around a pilot crossing.
- Each point has 17,913–26,171 errors (CSS) or 10,000–12,981 errors (XZZX).
- Fit: quadratic FSS with ν0 = 1.0, and x_window = 0.06 (CSS) or 0.1 (XZZX). Errors are 1σ from the fit covariance.
- Bases:
  - CSS: X only. The Z memory sees only X and Y errors, at rate p/(1 + η), so its threshold is far higher.
  - XZZX: X and Z. The lower of the two thresholds is compared.

## Result

From [results/css/threshold.csv](results/css/threshold.csv). Difference is (framework − Campos2026) in units of Campos2026's ±0.2-point error bar.

| η | p_th (%) | Reference line (%) | Campos2026 (%) | Difference (error bars) |
|---|---|---|---|---|
| 0.5 | 4.365 ± 0.004 | 4.350 | 4.4 | −0.2 |
| 10 | 3.045 ± 0.003 | 3.038 | 3.0 | +0.2 |
| 25 | 2.969 ± 0.003 | 2.957 | 2.9 | +0.3 |
| 50 | 2.938 ± 0.003 | 2.929 | 2.9 | +0.2 |
| 100 | 2.924 ± 0.003 | 2.914 | 2.9 | +0.1 |
| ∞ | 2.911 ± 0.003 | 2.900 | — | — |

- Every η is 0.2–0.4% (relative) above the reference line, which is built from the rounded 2.9%.
- In terms of q = p_Y + p_Z, the six thresholds coincide: 2.910 ± 0.001%, with χ² = 1.78 for 5 degrees of freedom.

From [results/xzzx/threshold.csv](results/xzzx/threshold.csv). The difference is that of the lower basis, in the same units.

| η | X basis (%) | Z basis (%) | Campos2026 (%) | Difference (error bars) |
|---|---|---|---|---|
| 0.5 | 4.352 ± 0.007 | 4.363 ± 0.007 | 4.4 | −0.2 |
| 10 | 5.784 ± 0.010 | 5.718 ± 0.009 | 5.6 | +0.6 |
| 25 | 6.401 ± 0.011 | 6.288 ± 0.011 | 6.3 | −0.1 |
| 50 | 6.817 ± 0.016 | 6.620 ± 0.013 | 6.9 | −1.4 |
| 100 | 7.081 ± 0.015 | 6.860 ± 0.014 | 7.4 | −2.7 |

- At η = 0.5 the XZZX code agrees with the CSS code point by point: χ² = 20.7 (X basis) and 26.8 (Z basis) for 25 points.

## Verdict

- **Bias dependence: pass.**
  - The CSS threshold falls with η, from 4.36% to 2.91%. The XZZX threshold rises, from 4.35% to 6.86%.
  - This matches the trend of both papers.
- **Biased noise and deformation: pass.** The CSS thresholds coincide in q, and at η = 0.5 the XZZX and CSS codes agree point by point.
- **CSS against both papers: pass.** At every η, the threshold is within 0.4% (relative) of the reference line and within 0.4 error bars of Campos2026.
- **XZZX against Campos2026: consistent for η ≤ 50 (within 1.4 error bars), low at η = 100.**
  - At η = 100 the threshold is 0.54 points (7%, 2.7 error bars) below 7.4%.
  - Two conditions differ. Campos2026 uses distances up to 40 and counts either logical. Here the distances are d = 11–19, and the lower basis is compared.
  - Counting either logical, with X and Z failures assumed independent, gives 6.97% (−2.2 error bars).
  - A small pilot at d = 19–35 showed the crossing rising with d, toward about 7.2%.
  - Neither effect has been confirmed with a production run.
