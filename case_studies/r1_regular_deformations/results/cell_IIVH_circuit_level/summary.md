# Summary: cell_IIVH_circuit_level

Written by `cdsc summarize` on 2026-11-05 00:22.

## Setup

- Config: [case_studies/r1_regular_deformations/config_cell_IIVH_circuit_level.yaml](../../config_cell_IIVH_circuit_level.yaml)
- Codes: cell_II_VH
- Noise: circuit_level / biased, eta = [100], p_meas = same_as_p
- Plugins: [case_studies/r1_regular_deformations/codes.py](../../codes.py)
- Sweeps:
  - `threshold_sweep`: d = [3, 5, 7], basis X, Z, p = 10 pts [1.00e-02 .. 2.00e-02]
  - `suppression_sweep`: d = [3, 5, 7], basis X, Z, p = 1.00e-02
- Sampling: decoder bp, each task until 5,000 errors or 500,000 shots, 4 workers
- Run: 2026-11-03 17:22:07, git 50ff753

## Warnings

- validation.json not found; run `cdsc validate case_studies/r1_regular_deformations/config_cell_IIVH_circuit_level.yaml` first
- cell_II_VH Z eta=100: poor fit (chi2_red=9.18, p-value=0.000)
- cell_II_VH X eta=100 p=1.00e-02: d_teraquop=73 is extrapolated far beyond the largest sampled d=7
- cell_II_VH Z eta=100 p=1.00e-02: d_teraquop=59 is extrapolated far beyond the largest sampled d=7

## Threshold

Sweep `threshold_sweep`, fit on d = [3, 5, 7], x_window = 0.01, ν0 = 1.5. Data: [threshold.csv](threshold.csv)

| code       | basis   | eta   | p_th              | ν    | χ²_red   | p-value   | figure                                        |
|------------|---------|-------|-------------------|------|----------|-----------|-----------------------------------------------|
| cell_II_VH | X       | 100   | 1.4630% ± 0.0076% | 1.22 | 1.75     | 0.031     | [PDF](figures/threshold_cell_II_VH_X_100.pdf) |
| cell_II_VH | Z       | 100   | 1.5581% ± 0.0056% | 1.15 | 9.18     | 0.000     | [PDF](figures/threshold_cell_II_VH_Z_100.pdf) |

## Teraquop footprint

Sweep `suppression_sweep`, target p_L = 1e-12 per d rounds. Data: [suppression.csv](suppression.csv)

| code       | basis   | eta   | p        | d*   | d_teraquop   | qubits   | figure                                          |
|------------|---------|-------|----------|------|--------------|----------|-------------------------------------------------|
| cell_II_VH | X       | 100   | 1.00e-02 | 72.6 | 73           | 10,657   | [PDF](figures/suppression_cell_II_VH_X_100.pdf) |
| cell_II_VH | Z       | 100   | 1.00e-02 | 58.1 | 59           | 6,961    | [PDF](figures/suppression_cell_II_VH_Z_100.pdf) |

## Sampling

Data: [samples.csv](samples.csv). 66 tasks, 4.8M shots, 336,524 errors. Limited by max_errors: 66 tasks; by max_shots: 0 tasks.

| sweep             | code       | basis   | eta   | d         | p                             | tasks   | shots   | min errors   |
|-------------------|------------|---------|-------|-----------|-------------------------------|---------|---------|--------------|
| threshold_sweep   | cell_II_VH | X       | 100   | [3, 5, 7] | 10 pts [1.00e-02 .. 2.00e-02] | 30      | 963.8k  | 5,000        |
| threshold_sweep   | cell_II_VH | Z       | 100   | [3, 5, 7] | 10 pts [1.00e-02 .. 2.00e-02] | 30      | 2.8M    | 5,000        |
| suppression_sweep | cell_II_VH | X       | 100   | [3, 5, 7] | 1.00e-02                      | 3       | 247.5k  | 5,221        |
| suppression_sweep | cell_II_VH | Z       | 100   | [3, 5, 7] | 1.00e-02                      | 3       | 798.1k  | 5,017        |

## Validation

validation.json not found.

## Circuit diagrams

- cell_II_VH: [d3 detslice](diagrams/cell_II_VH/cell_II_VH_d3_detslice.svg) · [d3 timeline](diagrams/cell_II_VH/cell_II_VH_d3_timeline.svg) · [d5 detslice](diagrams/cell_II_VH/cell_II_VH_d5_detslice.svg) · [d5 timeline](diagrams/cell_II_VH/cell_II_VH_d5_timeline.svg) · [d7 detslice](diagrams/cell_II_VH/cell_II_VH_d7_detslice.svg) · [d7 timeline](diagrams/cell_II_VH/cell_II_VH_d7_timeline.svg)

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
