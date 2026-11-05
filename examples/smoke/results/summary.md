# Summary: smoke

Written by `cdsc summarize` on 2026-11-05 00:54.

## Setup

- Config: [examples/smoke/config.yaml](../config.yaml)
- Codes: rotated_surface
- Noise: code_capacity / depolarizing, p_meas = 0.0
- Sweeps:
  - `threshold_sweep`: d = [3, 5, 7, 9], basis X, p = 10 pts [1.35e-01 .. 1.50e-01]
  - `suppression_sweep`: d = [3, 5, 7, 9], basis X, p = 5.00e-02
- Sampling: decoder mwpm, each task until 20,000 errors or 1,000,000 shots, 4 workers
- Run: 2026-11-05 00:54:39 → 00:54:55 (15.8s), git f406ab6 with uncommitted changes

## Warnings

- rotated_surface X p=5.00e-02: d_teraquop=49 is extrapolated far beyond the largest sampled d=9

## Threshold

Sweep `threshold_sweep`, fit on d = [3, 5, 7, 9], x_window = 0.1, ν0 = 1.5. Data: [threshold.csv](threshold.csv)

| code            | basis   | p_th               | ν    | χ²_red   | p-value   | figure                                         |
|-----------------|---------|--------------------|------|----------|-----------|------------------------------------------------|
| rotated_surface | X       | 14.2841% ± 0.0305% | 1.63 | 1.08     | 0.342     | [PDF](figures/threshold_rotated_surface_X.pdf) |

## Teraquop footprint

Sweep `suppression_sweep`, target p_L = 1e-12 per d rounds. Data: [suppression.csv](suppression.csv)

| code            | basis   | p        | d*   | d_teraquop   | qubits   | figure                                           |
|-----------------|---------|----------|------|--------------|----------|--------------------------------------------------|
| rotated_surface | X       | 5.00e-02 | 48.8 | 49           | 4,801    | [PDF](figures/suppression_rotated_surface_X.pdf) |

## Sampling

Data: [samples.csv](samples.csv). 44 tasks, 11.3M shots, 841,305 errors. Limited by max_errors: 40 tasks; by max_shots: 4 tasks.

| sweep             | code            | basis   | d            | p                             | tasks   | shots   | min errors   |
|-------------------|-----------------|---------|--------------|-------------------------------|---------|---------|--------------|
| threshold_sweep   | rotated_surface | X       | [3, 5, 7, 9] | 10 pts [1.35e-01 .. 1.50e-01] | 40      | 7.3M    | 20,000       |
| suppression_sweep | rotated_surface | X       | [3, 5, 7, 9] | 5.00e-02                      | 4       | 4.0M    | 1,805        |

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
