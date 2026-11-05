# Summary: b1_dephasing_mwpm

Written by `cdsc summarize` on 2026-11-05 00:21.

## Setup

- Config: [case_studies/b1_decoder_comparison/config_dephasing_mwpm.yaml](../../config_dephasing_mwpm.yaml)
- Codes: rotated_surface
- Noise: code_capacity / biased, eta = [inf], p_meas = 0.0
- Sweeps:
  - `threshold_sweep`: d = [7 .. 23] (5), basis X, p = 11 pts [9.10e-02 .. 1.11e-01]
  - `suppression_sweep`: d = [3, 5, 7], basis X, p = 5.00e-02
- Sampling: decoder mwpm, each task until 20,000 errors or 1,000,000 shots, 4 workers
- Run: 2026-10-22 09:15:44, git dc039b9 with uncommitted changes

## Warnings

- rotated_surface X eta=inf: poor fit (chi2_red=2.06, p-value=0.000)
- rotated_surface X eta=inf p=5.00e-02: d_teraquop=69 is extrapolated far beyond the largest sampled d=7

## Threshold

Sweep `threshold_sweep`, fit on d = [7, 11, 15, 19, 23], x_window = 0.1, ν0 = 1.46. Data: [threshold.csv](threshold.csv)

| code            | basis   | eta   | p_th              | ν    | χ²_red   | p-value   | figure                                             |
|-----------------|---------|-------|-------------------|------|----------|-----------|----------------------------------------------------|
| rotated_surface | X       | inf   | 9.9716% ± 0.0104% | 1.61 | 2.06     | 0.000     | [PDF](figures/threshold_rotated_surface_X_inf.pdf) |

## Teraquop footprint

Sweep `suppression_sweep`, target p_L = 1e-12 per d rounds. Data: [suppression.csv](suppression.csv)

| code            | basis   | eta   | p        | d*   | d_teraquop   | qubits   | figure                                               |
|-----------------|---------|-------|----------|------|--------------|----------|------------------------------------------------------|
| rotated_surface | X       | inf   | 5.00e-02 | 68.2 | 69           | 9,521    | [PDF](figures/suppression_rotated_surface_X_inf.pdf) |

## Sampling

Data: [samples.csv](samples.csv). 58 tasks, 11.2M shots, 1,175,430 errors. Limited by max_errors: 57 tasks; by max_shots: 1 tasks.

| sweep             | code            | basis   | eta   | d             | p                             | tasks   | shots   | min errors   |
|-------------------|-----------------|---------|-------|---------------|-------------------------------|---------|---------|--------------|
| threshold_sweep   | rotated_surface | X       | inf   | [7 .. 23] (5) | 11 pts [9.10e-02 .. 1.11e-01] | 55      | 8.8M    | 20,000       |
| suppression_sweep | rotated_surface | X       | inf   | [3, 5, 7]     | 5.00e-02                      | 3       | 2.4M    | 16,305       |

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
