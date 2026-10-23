# A3: Phenomenological threshold against stim's generated circuits

## Prior studies

| Key | Paper | Where | Value | Conditions |
|---|---|---|---|---|
| Gidney2021Stim | C. Gidney, "Stim: a fast stabilizer circuit simulator" [arXiv:2103.02202](https://arxiv.org/abs/2103.02202) | `stim.Circuit.generated`, tasks `surface_code:rotated_memory_x` and `_z` | Reference circuits, sampled at the framework's points | `rounds = d`, `before_round_data_depolarization = p`, `before_measure_flip_probability = p`, `after_clifford_depolarization = 0`, `after_reset_flip_probability = 0` |
| LinLai2025 | T.-H. Lin and C.-Y. Lai, "Union-Intersection Union-Find for Decoding Depolarizing Errors in Topological Codes" [arXiv:2506.14745](https://arxiv.org/abs/2506.14745) | Table V, §V-C | MWPM 3.92% | Rotated code, depolarizing data noise at ε, measurement flips at ε, d noisy rounds and a perfect last round, PyMatching v2, logical X error rate, FSS fit with a low-order polynomial (to ±0.01%), 10⁶ samples per point. The distances are not stated |

- **stim's circuits are the framework's model.**
  - With detectors matched by their coordinates, their detector error models equal the framework's at every simulated distance in both bases, once mechanisms with the same symptoms are merged. So do the decomposed edges PyMatching decodes.
  - So the stim comparison is a differential test of the phenomenological builder, not a reproduction of a published value.
- **LinLai2025 differs only at the top time boundary.**
  - Its last round of data noise flips each memory basis at 2ε/3. In its place, the framework flips the final data readout at ε.
  - It counts logical X errors only, i.e. one basis, as the framework does.

## Setup

- Configs: [config_framework.yaml](config_framework.yaml) and [config_stim.yaml](config_stim.yaml), identical except `experiment.name` and `output.dir`.
- The stim side ran through [sample_stim.py](sample_stim.py), with `--reference config_framework.yaml`. It writes samples.csv for `cdsc analyze`, so both sides are fitted the same way.
- Code: `rotated_surface`.
- `phenomenological` with `depolarizing` noise and `p_meas: same_as_p`.
- Decoder: `mwpm`
- d = 7, 9, 11, 13, 15. Bases X and Z. p = 3.3–4.5% in steps of 0.1%.
- Each point ran to at least 20,000 errors (20,000–25,832).
- Fit: quadratic FSS on d = 9–15, with x_window = 0.06 and ν0 = 1.0. Errors are 1σ from the fit covariance.

## Result

From [results/framework/threshold.csv](results/framework/threshold.csv) and [results/stim/threshold.csv](results/stim/threshold.csv):

| Basis | Framework p_th (%) | stim p_th (%) | Framework − stim (points) | ν (framework / stim) | χ²_red (framework / stim) |
|---|---|---|---|---|---|
| X | 3.892 ± 0.005 | 3.900 ± 0.005 | −0.008 ± 0.007 (−1.2σ) | 1.09 / 1.10 | 1.25 / 1.39 |
| Z | 3.904 ± 0.005 | 3.902 ± 0.005 | +0.002 ± 0.007 (+0.2σ) | 1.13 / 1.09 | 0.62 / 0.82 |

- p_L point by point, by a two-proportion z-test: χ² = 120.1 for 130 points (p = 0.72). No point has |z| > 3.
- Against LinLai2025's 3.92%, the framework is 0.028 points (X) and 0.016 points (Z) lower, i.e. 0.7% and 0.4% (relative).

## Verdict

- **stim, threshold: pass.** Within 1.2σ in both bases.
- **stim, p_L point by point: pass.** The two samples are statistically indistinguishable.
- **LinLai2025 (3.92%): consistent.** Other fits of the same data (d = 7–15 or 11–15, x_window = 0.04–0.08) give 3.88–3.92%, which covers the gap.
