# Summary: xzzx_vs_anti3_IVH_circuit_level_v2

Written by `cdsc summarize` on 2026-11-05 00:23.

## Setup

- Config: [case_studies/r1_regular_deformations/config_xzzx_vs_anti3_IVH_circuit_level_v2.yaml](../../config_xzzx_vs_anti3_IVH_circuit_level_v2.yaml)
- Codes: xzzx, anti3_IVH
- Noise: circuit_level / biased, eta = [100], p_meas = same_as_p
- Plugins: [case_studies/r1_regular_deformations/codes.py](../../codes.py)
- Sweeps:
  - `threshold_sweep`: d = [3, 5, 7], basis X, Z, p = 10 pts [1.00e-02 .. 2.00e-02]
  - `suppression_sweep`: d = [3, 5, 7], basis X, Z, p = 1.00e-02
- Sampling: decoder bp, each task until 5,000 errors or 500,000 shots, 4 workers
- Run: 2026-11-03 02:25:31, git f36d3ba

## Warnings

- validation.json not found; run `cdsc validate case_studies/r1_regular_deformations/config_xzzx_vs_anti3_IVH_circuit_level_v2.yaml` first
- xzzx X eta=100: poor fit (chi2_red=2.06, p-value=0.024)
- xzzx Z eta=100: poor fit (chi2_red=6.65, p-value=0.000)
- anti3_IVH X eta=100 p=1.00e-02: d_teraquop=67 is extrapolated far beyond the largest sampled d=7
- anti3_IVH Z eta=100 p=1.00e-02: d_teraquop=65 is extrapolated far beyond the largest sampled d=7
- xzzx X eta=100 p=1.00e-02: d_teraquop=67 is extrapolated far beyond the largest sampled d=7
- xzzx Z eta=100 p=1.00e-02: d_teraquop=83 is extrapolated far beyond the largest sampled d=7

## Threshold

Sweep `threshold_sweep`, fit on d = [3, 5, 7], x_window = 0.01, ν0 = 1.5. Data: [threshold.csv](threshold.csv)

| code      | basis   | eta   | p_th              | ν    | χ²_red   | p-value   | figure                                       |
|-----------|---------|-------|-------------------|------|----------|-----------|----------------------------------------------|
| anti3_IVH | X       | 100   | 1.6039% ± 0.0086% | 1.39 | 0.83     | 0.631     | [PDF](figures/threshold_anti3_IVH_X_100.pdf) |
| anti3_IVH | Z       | 100   | 1.6696% ± 0.0095% | 1.38 | 0.91     | 0.548     | [PDF](figures/threshold_anti3_IVH_Z_100.pdf) |
| xzzx      | X       | 100   | 1.8308% ± 0.0145% | 1.24 | 2.06     | 0.024     | [PDF](figures/threshold_xzzx_X_100.pdf)      |
| xzzx      | Z       | 100   | 1.3786% ± 0.0077% | 1.44 | 6.65     | 0.000     | [PDF](figures/threshold_xzzx_Z_100.pdf)      |

## Teraquop footprint

Sweep `suppression_sweep`, target p_L = 1e-12 per d rounds. Data: [suppression.csv](suppression.csv)

| code      | basis   | eta   | p        | d*   | d_teraquop   | qubits   | figure                                         |
|-----------|---------|-------|----------|------|--------------|----------|------------------------------------------------|
| anti3_IVH | X       | 100   | 1.00e-02 | 66.7 | 67           | 8,977    | [PDF](figures/suppression_anti3_IVH_X_100.pdf) |
| anti3_IVH | Z       | 100   | 1.00e-02 | 64.0 | 65           | 8,449    | [PDF](figures/suppression_anti3_IVH_Z_100.pdf) |
| xzzx      | X       | 100   | 1.00e-02 | 66.0 | 67           | 8,977    | [PDF](figures/suppression_xzzx_X_100.pdf)      |
| xzzx      | Z       | 100   | 1.00e-02 | 81.1 | 83           | 13,777   | [PDF](figures/suppression_xzzx_Z_100.pdf)      |

## Sampling

Data: [samples.csv](samples.csv). 132 tasks, 9.9M shots, 670,211 errors. Limited by max_errors: 132 tasks; by max_shots: 0 tasks.

| sweep             | code      | basis   | eta   | d         | p                             | tasks   | shots   | min errors   |
|-------------------|-----------|---------|-------|-----------|-------------------------------|---------|---------|--------------|
| threshold_sweep   | xzzx      | X       | 100   | [3, 5, 7] | 10 pts [1.00e-02 .. 2.00e-02] | 30      | 1.8M    | 5,000        |
| threshold_sweep   | anti3_IVH | X       | 100   | [3, 5, 7] | 10 pts [1.00e-02 .. 2.00e-02] | 30      | 1.7M    | 5,000        |
| threshold_sweep   | xzzx      | Z       | 100   | [3, 5, 7] | 10 pts [1.00e-02 .. 2.00e-02] | 30      | 3.0M    | 5,000        |
| threshold_sweep   | anti3_IVH | Z       | 100   | [3, 5, 7] | 10 pts [1.00e-02 .. 2.00e-02] | 30      | 1.5M    | 5,000        |
| suppression_sweep | xzzx      | X       | 100   | [3, 5, 7] | 1.00e-02                      | 3       | 422.0k  | 5,073        |
| suppression_sweep | anti3_IVH | X       | 100   | [3, 5, 7] | 1.00e-02                      | 3       | 424.2k  | 5,000        |
| suppression_sweep | xzzx      | Z       | 100   | [3, 5, 7] | 1.00e-02                      | 3       | 705.4k  | 5,029        |
| suppression_sweep | anti3_IVH | Z       | 100   | [3, 5, 7] | 1.00e-02                      | 3       | 385.0k  | 5,144        |

## Validation

validation.json not found.

## Circuit diagrams

- xzzx: [d3 detslice](diagrams/xzzx/xzzx_d3_detslice.svg) · [d3 timeline](diagrams/xzzx/xzzx_d3_timeline.svg) · [d5 detslice](diagrams/xzzx/xzzx_d5_detslice.svg) · [d5 timeline](diagrams/xzzx/xzzx_d5_timeline.svg) · [d7 detslice](diagrams/xzzx/xzzx_d7_detslice.svg) · [d7 timeline](diagrams/xzzx/xzzx_d7_timeline.svg)
- anti3_IVH: [d3 detslice](diagrams/anti3_IVH/anti3_IVH_d3_detslice.svg) · [d3 timeline](diagrams/anti3_IVH/anti3_IVH_d3_timeline.svg) · [d5 detslice](diagrams/anti3_IVH/anti3_IVH_d5_detslice.svg) · [d5 timeline](diagrams/anti3_IVH/anti3_IVH_d5_timeline.svg) · [d7 detslice](diagrams/anti3_IVH/anti3_IVH_d7_detslice.svg) · [d7 timeline](diagrams/anti3_IVH/anti3_IVH_d7_timeline.svg)

## Files

| file                               | contents                                                  | written by           |
|------------------------------------|-----------------------------------------------------------|----------------------|
| validation.json (not found)        | check results for each code and distance                  | `cdsc validate`      |
| plans.json (not found)             | sweep plans                                               | `cdsc compile-plans` |
| [samples.csv](samples.csv)         | shots, errors and p_L for each task                       | `cdsc run`           |
| [manifest.json](manifest.json)     | config, environment, git commit, plugin hashes, run times | `cdsc run`           |
| [threshold.csv](threshold.csv)     | threshold fits                                            | `cdsc analyze`       |
| [suppression.csv](suppression.csv) | suppression fits and teraquop footprints                  | `cdsc analyze`       |
| [figures/](figures/)               | threshold and suppression plots (PDF)                     | `cdsc visualize`     |
| [diagrams/](diagrams/)             | circuit diagrams (SVG)                                    | `cdsc visualize`     |
