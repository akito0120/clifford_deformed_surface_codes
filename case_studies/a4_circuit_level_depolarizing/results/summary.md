# Summary: a4_circuit_level_depolarizing

Written by `cdsc summarize` on 2026-11-05 00:18.

## Setup

- Config: [case_studies/a4_circuit_level_depolarizing/config.yaml](../config.yaml)
- Codes: rotated_surface
- Noise: circuit_level / depolarizing, p_meas = same_as_p
- Sweeps:
  - `threshold_sweep`: d = [7 .. 15] (5), basis X, Z, p = 13 pts [5.50e-03 .. 8.50e-03]
  - `suppression_sweep`: d = [3, 5, 7], basis X, p = 3.00e-03
- Sampling: decoder mwpm, each task until 20,000 errors or 1,000,000 shots, 4 workers
- Run: 2026-10-20 20:14:27, git e79a96d

## Warnings

- rotated_surface X p=3.00e-03: d_teraquop=51 is extrapolated far beyond the largest sampled d=7

## Threshold

Sweep `threshold_sweep`, fit on d = [9, 11, 13, 15], x_window = 0.015, ν0 = 1.06. Data: [threshold.csv](threshold.csv)

| code            | basis   | p_th              | ν    | χ²_red   | p-value   | figure                                         |
|-----------------|---------|-------------------|------|----------|-----------|------------------------------------------------|
| rotated_surface | X       | 0.6937% ± 0.0009% | 1.17 | 0.88     | 0.685     | [PDF](figures/threshold_rotated_surface_X.pdf) |
| rotated_surface | Z       | 0.6931% ± 0.0009% | 1.13 | 1.38     | 0.053     | [PDF](figures/threshold_rotated_surface_Z.pdf) |

## Teraquop footprint

Sweep `suppression_sweep`, target p_L = 1e-12 per d rounds. Data: [suppression.csv](suppression.csv)

| code            | basis   | p        | d*   | d_teraquop   | qubits   | figure                                           |
|-----------------|---------|----------|------|--------------|----------|--------------------------------------------------|
| rotated_surface | X       | 3.00e-03 | 50.1 | 51           | 5,201    | [PDF](figures/suppression_rotated_surface_X.pdf) |

## Sampling

Data: [samples.csv](samples.csv). 133 tasks, 49.2M shots, 2,630,005 errors. Limited by max_errors: 126 tasks; by max_shots: 7 tasks.

| sweep             | code            | basis   | d             | p                             | tasks   | shots   | min errors   |
|-------------------|-----------------|---------|---------------|-------------------------------|---------|---------|--------------|
| threshold_sweep   | rotated_surface | X       | [7 .. 15] (5) | 13 pts [5.50e-03 .. 8.50e-03] | 65      | 23.0M   | 15,218       |
| threshold_sweep   | rotated_surface | Z       | [7 .. 15] (5) | 13 pts [5.50e-03 .. 8.50e-03] | 65      | 23.1M   | 15,332       |
| suppression_sweep | rotated_surface | X       | [3, 5, 7]     | 3.00e-03                      | 3       | 3.0M    | 3,733        |

## Validation

Data: [validation.json](validation.json). 4 of 4 passed.

## Circuit diagrams

- rotated_surface: [d3 detslice](diagrams/rotated_surface/rotated_surface_d3_detslice.svg) · [d3 timeline](diagrams/rotated_surface/rotated_surface_d3_timeline.svg) · [d5 detslice](diagrams/rotated_surface/rotated_surface_d5_detslice.svg) · [d5 timeline](diagrams/rotated_surface/rotated_surface_d5_timeline.svg) · [d7 detslice](diagrams/rotated_surface/rotated_surface_d7_detslice.svg) · [d7 timeline](diagrams/rotated_surface/rotated_surface_d7_timeline.svg)

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
