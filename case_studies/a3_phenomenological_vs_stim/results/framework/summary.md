# Summary: a3_phenomenological_vs_stim_framework

Written by `cdsc summarize` on 2026-11-05 00:17.

## Setup

- Config: [case_studies/a3_phenomenological_vs_stim/config_framework.yaml](../../config_framework.yaml)
- Codes: rotated_surface
- Noise: phenomenological / depolarizing, p_meas = same_as_p
- Sweeps:
  - `threshold_sweep`: d = [7 .. 15] (5), basis X, Z, p = 13 pts [3.30e-02 .. 4.50e-02]
  - `suppression_sweep`: d = [3, 5, 7], basis X, p = 1.00e-02
- Sampling: decoder mwpm, each task until 20,000 errors or 1,000,000 shots, 4 workers
- Run: 2026-10-20 23:46:17, git 635b189

## Warnings

- rotated_surface X p=1.00e-02: d_teraquop=33 is extrapolated far beyond the largest sampled d=7

## Threshold

Sweep `threshold_sweep`, fit on d = [9, 11, 13, 15], x_window = 0.06, ν0 = 1.0. Data: [threshold.csv](threshold.csv)

| code            | basis   | p_th              | ν    | χ²_red   | p-value   | figure                                         |
|-----------------|---------|-------------------|------|----------|-----------|------------------------------------------------|
| rotated_surface | X       | 3.8923% ± 0.0047% | 1.09 | 1.25     | 0.142     | [PDF](figures/threshold_rotated_surface_X.pdf) |
| rotated_surface | Z       | 3.9036% ± 0.0049% | 1.13 | 0.62     | 0.965     | [PDF](figures/threshold_rotated_surface_Z.pdf) |

## Teraquop footprint

Sweep `suppression_sweep`, target p_L = 1e-12 per d rounds. Data: [suppression.csv](suppression.csv)

| code            | basis   | p        | d*   | d_teraquop   | qubits   | figure                                           |
|-----------------|---------|----------|------|--------------|----------|--------------------------------------------------|
| rotated_surface | X       | 1.00e-02 | 31.3 | 33           | 2,177    | [PDF](figures/suppression_rotated_surface_X.pdf) |

## Sampling

Data: [samples.csv](samples.csv). 133 tasks, 33.9M shots, 2,631,539 errors. Limited by max_errors: 130 tasks; by max_shots: 3 tasks.

| sweep             | code            | basis   | d             | p                             | tasks   | shots   | min errors   |
|-------------------|-----------------|---------|---------------|-------------------------------|---------|---------|--------------|
| threshold_sweep   | rotated_surface | X       | [7 .. 15] (5) | 13 pts [3.30e-02 .. 4.50e-02] | 65      | 15.4M   | 20,000       |
| threshold_sweep   | rotated_surface | Z       | [7 .. 15] (5) | 13 pts [3.30e-02 .. 4.50e-02] | 65      | 15.5M   | 20,000       |
| suppression_sweep | rotated_surface | X       | [3, 5, 7]     | 1.00e-02                      | 3       | 3.0M    | 542          |

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
