# Summary: a1_code_capacity_depolarizing

Written by `cdsc summarize` on 2026-11-05 00:35.

## Setup

- Config: [case_studies/a1_code_capacity_depolarizing/config.yaml](../config.yaml)
- Codes: rotated_surface, xzzx, xy
- Noise: code_capacity / depolarizing, p_meas = 0.0
- Sweeps:
  - `threshold_sweep`: d = [7 .. 23] (5), basis X, Z, p = 15 pts [1.36e-01 .. 1.64e-01]
  - `suppression_sweep`: d = [3, 5, 7], basis X, p = 5.00e-02
- Sampling: decoder mwpm, each task until 20,000 errors or 1,000,000 shots, 4 workers
- Run: 2026-10-20 13:13:49, git 8decad5

## Warnings

- rotated_surface X: poor fit (chi2_red=2.48, p-value=0.000)
- rotated_surface Z: poor fit (chi2_red=2.12, p-value=0.000)
- xy X: poor fit (chi2_red=2.06, p-value=0.000)
- xy Z: poor fit (chi2_red=2.04, p-value=0.000)
- xzzx X: poor fit (chi2_red=1.75, p-value=0.000)
- xzzx Z: poor fit (chi2_red=2.10, p-value=0.000)
- rotated_surface X p=5.00e-02: d_teraquop=47 is extrapolated far beyond the largest sampled d=7
- xy X p=5.00e-02: d_teraquop=47 is extrapolated far beyond the largest sampled d=7
- xzzx X p=5.00e-02: d_teraquop=49 is extrapolated far beyond the largest sampled d=7

## Threshold

Sweep `threshold_sweep`, fit on d = [7, 11, 15, 19, 23], x_window = 0.1, ν0 = 1.5. Data: [threshold.csv](threshold.csv)

| code            | basis   | p_th               | ν    | χ²_red   | p-value   | figure                                         |
|-----------------|---------|--------------------|------|----------|-----------|------------------------------------------------|
| rotated_surface | X       | 14.9619% ± 0.0132% | 1.61 | 2.48     | 0.000     | [PDF](figures/threshold_rotated_surface_X.pdf) |
| rotated_surface | Z       | 14.9734% ± 0.0130% | 1.59 | 2.12     | 0.000     | [PDF](figures/threshold_rotated_surface_Z.pdf) |
| xy              | X       | 14.9622% ± 0.0136% | 1.66 | 2.06     | 0.000     | [PDF](figures/threshold_xy_X.pdf)              |
| xy              | Z       | 14.9550% ± 0.0132% | 1.59 | 2.04     | 0.000     | [PDF](figures/threshold_xy_Z.pdf)              |
| xzzx            | X       | 14.9456% ± 0.0129% | 1.56 | 1.75     | 0.000     | [PDF](figures/threshold_xzzx_X.pdf)            |
| xzzx            | Z       | 14.9652% ± 0.0129% | 1.58 | 2.10     | 0.000     | [PDF](figures/threshold_xzzx_Z.pdf)            |

## Teraquop footprint

Sweep `suppression_sweep`, target p_L = 1e-12 per d rounds. Data: [suppression.csv](suppression.csv)

| code            | basis   | p        | d*   | d_teraquop   | qubits   | figure                                           |
|-----------------|---------|----------|------|--------------|----------|--------------------------------------------------|
| rotated_surface | X       | 5.00e-02 | 46.6 | 47           | 4,417    | [PDF](figures/suppression_rotated_surface_X.pdf) |
| xy              | X       | 5.00e-02 | 46.8 | 47           | 4,417    | [PDF](figures/suppression_xy_X.pdf)              |
| xzzx            | X       | 5.00e-02 | 47.1 | 49           | 4,801    | [PDF](figures/suppression_xzzx_X.pdf)            |

## Sampling

Data: [samples.csv](samples.csv). 459 tasks, 82.7M shots, 9,181,933 errors. Limited by max_errors: 450 tasks; by max_shots: 9 tasks.

| sweep             | code            | basis   | d             | p                             | tasks   | shots   | min errors   |
|-------------------|-----------------|---------|---------------|-------------------------------|---------|---------|--------------|
| threshold_sweep   | rotated_surface | X       | [7 .. 23] (5) | 15 pts [1.36e-01 .. 1.64e-01] | 75      | 12.3M   | 20,001       |
| threshold_sweep   | xzzx            | X       | [7 .. 23] (5) | 15 pts [1.36e-01 .. 1.64e-01] | 75      | 12.3M   | 20,001       |
| threshold_sweep   | xy              | X       | [7 .. 23] (5) | 15 pts [1.36e-01 .. 1.64e-01] | 75      | 12.3M   | 20,000       |
| threshold_sweep   | rotated_surface | Z       | [7 .. 23] (5) | 15 pts [1.36e-01 .. 1.64e-01] | 75      | 12.3M   | 20,000       |
| threshold_sweep   | xzzx            | Z       | [7 .. 23] (5) | 15 pts [1.36e-01 .. 1.64e-01] | 75      | 12.3M   | 20,005       |
| threshold_sweep   | xy              | Z       | [7 .. 23] (5) | 15 pts [1.36e-01 .. 1.64e-01] | 75      | 12.3M   | 20,000       |
| suppression_sweep | rotated_surface | X       | [3, 5, 7]     | 5.00e-02                      | 3       | 3.0M    | 3,842        |
| suppression_sweep | xzzx            | X       | [3, 5, 7]     | 5.00e-02                      | 3       | 3.0M    | 3,931        |
| suppression_sweep | xy              | X       | [3, 5, 7]     | 5.00e-02                      | 3       | 3.0M    | 3,925        |

## Validation

Data: [validation.json](validation.json). 12 of 12 passed.

## Circuit diagrams

- rotated_surface: [d3 detslice](diagrams/rotated_surface/rotated_surface_d3_detslice.svg) · [d3 timeline](diagrams/rotated_surface/rotated_surface_d3_timeline.svg) · [d5 detslice](diagrams/rotated_surface/rotated_surface_d5_detslice.svg) · [d5 timeline](diagrams/rotated_surface/rotated_surface_d5_timeline.svg) · [d7 detslice](diagrams/rotated_surface/rotated_surface_d7_detslice.svg) · [d7 timeline](diagrams/rotated_surface/rotated_surface_d7_timeline.svg)
- xzzx: [d3 detslice](diagrams/xzzx/xzzx_d3_detslice.svg) · [d3 timeline](diagrams/xzzx/xzzx_d3_timeline.svg) · [d5 detslice](diagrams/xzzx/xzzx_d5_detslice.svg) · [d5 timeline](diagrams/xzzx/xzzx_d5_timeline.svg) · [d7 detslice](diagrams/xzzx/xzzx_d7_detslice.svg) · [d7 timeline](diagrams/xzzx/xzzx_d7_timeline.svg)
- xy: [d3 detslice](diagrams/xy/xy_d3_detslice.svg) · [d3 timeline](diagrams/xy/xy_d3_timeline.svg) · [d5 detslice](diagrams/xy/xy_d5_detslice.svg) · [d5 timeline](diagrams/xy/xy_d5_timeline.svg) · [d7 detslice](diagrams/xy/xy_d7_detslice.svg) · [d7 timeline](diagrams/xy/xy_d7_timeline.svg)

## Files

| file                               | contents                                                  | written by           |
|------------------------------------|-----------------------------------------------------------|----------------------|
| [validation.json](validation.json) | check results for each code and distance                  | `cdsc validate`      |
| [plans.json](plans.json)           | sweep plans                                               | `cdsc compile-plans` |
| [samples.csv](samples.csv)         | shots, errors and p_L for each task                       | `cdsc run`           |
| [manifest.json](manifest.json)     | config, environment, git commit, plugin hashes, run times | `cdsc run`           |
| [threshold.csv](threshold.csv)     | threshold fits                                            | `cdsc analyze`       |
| [suppression.csv](suppression.csv) | suppression fits and teraquop footprints                  | `cdsc analyze`       |
| [figures/](figures/)               | threshold and suppression plots (PDF)                     | `cdsc visualize`     |
| [diagrams/](diagrams/)             | circuit diagrams (SVG)                                    | `cdsc visualize`     |
