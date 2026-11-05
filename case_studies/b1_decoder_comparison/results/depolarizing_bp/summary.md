# Summary: b1_depolarizing_bp

Written by `cdsc summarize` on 2026-11-05 00:21.

## Setup

- Config: [case_studies/b1_decoder_comparison/config_depolarizing_bp.yaml](../../config_depolarizing_bp.yaml)
- Codes: rotated_surface
- Noise: code_capacity / depolarizing, p_meas = 0.0
- Sweeps:
  - `threshold_sweep`: d = [7 .. 23] (5), basis Z, p = 11 pts [1.65e-01 .. 1.85e-01]
  - `suppression_sweep`: d = [3, 5, 7], basis Z, p = 5.00e-02
- Sampling: decoder bp, each task until 10,000 errors or 1,000,000 shots, 4 workers
- Run: 2026-10-22 10:30:14, git dc039b9 with uncommitted changes

## Warnings

- validation.json not found; run `cdsc validate case_studies/b1_decoder_comparison/config_depolarizing_bp.yaml` first
- rotated_surface Z p=5.00e-02: d_teraquop=41 is extrapolated far beyond the largest sampled d=7

## Threshold

Sweep `threshold_sweep`, fit on d = [7, 11, 15, 19, 23], x_window = 0.1, ν0 = 1.5. Data: [threshold.csv](threshold.csv)

| code            | basis   | p_th               | ν    | χ²_red   | p-value   | figure                                         |
|-----------------|---------|--------------------|------|----------|-----------|------------------------------------------------|
| rotated_surface | Z       | 17.6492% ± 0.0249% | 1.67 | 0.94     | 0.598     | [PDF](figures/threshold_rotated_surface_Z.pdf) |

## Teraquop footprint

Sweep `suppression_sweep`, target p_L = 1e-12 per d rounds. Data: [suppression.csv](suppression.csv)

| code            | basis   | p        | d*   | d_teraquop   | qubits   | figure                                           |
|-----------------|---------|----------|------|--------------|----------|--------------------------------------------------|
| rotated_surface | Z       | 5.00e-02 | 39.3 | 41           | 3,361    | [PDF](figures/suppression_rotated_surface_Z.pdf) |

## Sampling

Data: [samples.csv](samples.csv). 58 tasks, 6.6M shots, 573,577 errors. Limited by max_errors: 56 tasks; by max_shots: 2 tasks.

| sweep             | code            | basis   | d             | p                             | tasks   | shots   | min errors   |
|-------------------|-----------------|---------|---------------|-------------------------------|---------|---------|--------------|
| threshold_sweep   | rotated_surface | Z       | [7 .. 23] (5) | 11 pts [1.65e-01 .. 1.85e-01] | 55      | 3.9M    | 10,000       |
| suppression_sweep | rotated_surface | Z       | [3, 5, 7]     | 5.00e-02                      | 3       | 2.6M    | 2,203        |

## Validation

validation.json not found.

## Circuit diagrams

- rotated_surface: [d3 detslice](diagrams/rotated_surface/rotated_surface_d3_detslice.svg) · [d3 timeline](diagrams/rotated_surface/rotated_surface_d3_timeline.svg) · [d5 detslice](diagrams/rotated_surface/rotated_surface_d5_detslice.svg) · [d5 timeline](diagrams/rotated_surface/rotated_surface_d5_timeline.svg) · [d7 detslice](diagrams/rotated_surface/rotated_surface_d7_detslice.svg) · [d7 timeline](diagrams/rotated_surface/rotated_surface_d7_timeline.svg)

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
