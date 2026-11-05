# Summary: a2_phenomenological_biased_css

Written by `cdsc summarize` on 2026-11-05 00:14.

## Setup

- Config: [case_studies/a2_phenomenological_biased/config_css.yaml](../../config_css.yaml)
- Codes: rotated_surface
- Noise: phenomenological / biased_meas_yz, eta = [0.5, 10, 25, 50, 100, inf], p_meas = same_as_p
- Plugins: [case_studies/a2_phenomenological_biased/noises.py](../../noises.py)
- Sweeps:
  - `threshold_sweep`: d = [11 .. 19] (5), basis X, p = 66 pts [2.40e-02 .. 4.85e-02]
  - `suppression_sweep`: d = [3, 5, 7], basis X, p = 1.00e-02
- Sampling: decoder mwpm, each task until 20,000 errors or 1,000,000 shots, 4 workers
- Run: 2026-10-21 16:17:38, git 4edeb10

## Warnings

- plugins in the config changed after `cdsc run`; samples.csv was made with the config recorded in manifest.json
- rotated_surface X eta=50: poor fit (chi2_red=2.28, p-value=0.000)
- rotated_surface X eta=0.5 p=1.00e-02: d_teraquop=31 is extrapolated far beyond the largest sampled d=7
- rotated_surface X eta=10 p=1.00e-02: d_teraquop=39 is extrapolated far beyond the largest sampled d=7
- rotated_surface X eta=25 p=1.00e-02: d_teraquop=41 is extrapolated far beyond the largest sampled d=7
- rotated_surface X eta=50 p=1.00e-02: d_teraquop=41 is extrapolated far beyond the largest sampled d=7
- rotated_surface X eta=100 p=1.00e-02: d_teraquop=41 is extrapolated far beyond the largest sampled d=7
- rotated_surface X eta=inf p=1.00e-02: d_teraquop=41 is extrapolated far beyond the largest sampled d=7

## Threshold

Sweep `threshold_sweep`, fit on d = [11, 13, 15, 17, 19], x_window = 0.06, ν0 = 1.0. Data: [threshold.csv](threshold.csv)

| code            | basis   | eta   | p_th              | ν    | χ²_red   | p-value   | figure                                               |
|-----------------|---------|-------|-------------------|------|----------|-----------|------------------------------------------------------|
| rotated_surface | X       | 0.5   | 4.3648% ± 0.0043% | 1.09 | 1.03     | 0.414     | [PDF](figures/threshold_rotated_surface_X_0.5.pdf)   |
| rotated_surface | X       | 10    | 3.0452% ± 0.0031% | 1.11 | 0.78     | 0.831     | [PDF](figures/threshold_rotated_surface_X_10.0.pdf)  |
| rotated_surface | X       | 25    | 2.9688% ± 0.0030% | 1.10 | 0.99     | 0.490     | [PDF](figures/threshold_rotated_surface_X_25.0.pdf)  |
| rotated_surface | X       | 50    | 2.9377% ± 0.0029% | 1.07 | 2.28     | 0.000     | [PDF](figures/threshold_rotated_surface_X_50.0.pdf)  |
| rotated_surface | X       | 100   | 2.9244% ± 0.0030% | 1.10 | 0.61     | 0.968     | [PDF](figures/threshold_rotated_surface_X_100.0.pdf) |
| rotated_surface | X       | inf   | 2.9112% ± 0.0030% | 1.10 | 0.87     | 0.694     | [PDF](figures/threshold_rotated_surface_X_inf.pdf)   |

## Teraquop footprint

Sweep `suppression_sweep`, target p_L = 1e-12 per d rounds. Data: [suppression.csv](suppression.csv)

| code            | basis   | eta   | p        | d*   | d_teraquop   | qubits   | figure                                                 |
|-----------------|---------|-------|----------|------|--------------|----------|--------------------------------------------------------|
| rotated_surface | X       | 0.5   | 1.00e-02 | 30.2 | 31           | 1,921    | [PDF](figures/suppression_rotated_surface_X_0.5.pdf)   |
| rotated_surface | X       | 10    | 1.00e-02 | 38.2 | 39           | 3,041    | [PDF](figures/suppression_rotated_surface_X_10.0.pdf)  |
| rotated_surface | X       | 25    | 1.00e-02 | 39.9 | 41           | 3,361    | [PDF](figures/suppression_rotated_surface_X_25.0.pdf)  |
| rotated_surface | X       | 50    | 1.00e-02 | 40.0 | 41           | 3,361    | [PDF](figures/suppression_rotated_surface_X_50.0.pdf)  |
| rotated_surface | X       | 100   | 1.00e-02 | 39.7 | 41           | 3,361    | [PDF](figures/suppression_rotated_surface_X_100.0.pdf) |
| rotated_surface | X       | inf   | 1.00e-02 | 39.8 | 41           | 3,361    | [PDF](figures/suppression_rotated_surface_X_inf.pdf)   |

## Sampling

Data: [samples.csv](samples.csv). 348 tasks, 110.6M shots, 6,774,795 errors. Limited by max_errors: 325 tasks; by max_shots: 23 tasks.

| sweep             | code            | basis   | eta   | d              | p                             | tasks   | shots   | min errors   |
|-------------------|-----------------|---------|-------|----------------|-------------------------------|---------|---------|--------------|
| threshold_sweep   | rotated_surface | X       | 0.5   | [11 .. 19] (5) | 11 pts [3.85e-02 .. 4.85e-02] | 55      | 13.3M   | 20,000       |
| threshold_sweep   | rotated_surface | X       | 10    | [11 .. 19] (5) | 11 pts [2.54e-02 .. 3.54e-02] | 55      | 15.5M   | 19,764       |
| threshold_sweep   | rotated_surface | X       | 25    | [11 .. 19] (5) | 11 pts [2.46e-02 .. 3.46e-02] | 55      | 15.7M   | 18,722       |
| threshold_sweep   | rotated_surface | X       | 50    | [11 .. 19] (5) | 11 pts [2.43e-02 .. 3.43e-02] | 55      | 15.9M   | 18,628       |
| threshold_sweep   | rotated_surface | X       | 100   | [11 .. 19] (5) | 11 pts [2.41e-02 .. 3.41e-02] | 55      | 16.1M   | 17,913       |
| threshold_sweep   | rotated_surface | X       | inf   | [11 .. 19] (5) | 11 pts [2.40e-02 .. 3.40e-02] | 55      | 16.1M   | 17,959       |
| suppression_sweep | rotated_surface | X       | 0.5   | [3, 5, 7]      | 1.00e-02                      | 3       | 3.0M    | 402          |
| suppression_sweep | rotated_surface | X       | 10    | [3, 5, 7]      | 1.00e-02                      | 3       | 3.0M    | 1,557        |
| suppression_sweep | rotated_surface | X       | 25    | [3, 5, 7]      | 1.00e-02                      | 3       | 3.0M    | 1,880        |
| suppression_sweep | rotated_surface | X       | 50    | [3, 5, 7]      | 1.00e-02                      | 3       | 3.0M    | 1,968        |
| suppression_sweep | rotated_surface | X       | 100   | [3, 5, 7]      | 1.00e-02                      | 3       | 3.0M    | 1,942        |
| suppression_sweep | rotated_surface | X       | inf   | [3, 5, 7]      | 1.00e-02                      | 3       | 3.0M    | 1,957        |

## Validation

Data: [validation.json](validation.json). 4 of 4 passed.

## Circuit diagrams

- rotated_surface: [d3 detslice](diagrams/rotated_surface/rotated_surface_d3_detslice.svg) · [d3 timeline](diagrams/rotated_surface/rotated_surface_d3_timeline.svg) · [d5 detslice](diagrams/rotated_surface/rotated_surface_d5_detslice.svg) · [d5 timeline](diagrams/rotated_surface/rotated_surface_d5_timeline.svg) · [d7 detslice](diagrams/rotated_surface/rotated_surface_d7_detslice.svg) · [d7 timeline](diagrams/rotated_surface/rotated_surface_d7_timeline.svg)

## Files

| file                               | contents                                                  | written by           |
|------------------------------------|-----------------------------------------------------------|----------------------|
| [validation.json](validation.json) | check results for each code and distance                  | `cdsc validate`      |
| plans.json (not found)             | sweep plans                                               | `cdsc compile-plans` |
| [samples.csv](samples.csv)         | shots, errors and p_L for each task                       | `cdsc run`           |
| [manifest.json](manifest.json)     | config, environment, git commit, plugin hashes, run times | `cdsc run`           |
| [threshold.csv](threshold.csv)     | threshold fits                                            | `cdsc analyze`       |
| [suppression.csv](suppression.csv) | suppression fits and teraquop footprints                  | `cdsc analyze`       |
| [figures/](figures/)               | threshold and suppression plots (PDF)                     | `cdsc visualize`     |
| [diagrams/](diagrams/)             | circuit diagrams (SVG)                                    | `cdsc visualize`     |
