# Summary: a4_circuit_level_depolarizing

Written by `cdsc summarize` on 2026-11-05 21:58.

## Setup

- Config: [case_studies/a4_circuit_level_depolarizing/config.yaml](../config.yaml)
- Codes: rotated_surface_sd
- Noise: circuit_level / depolarizing_sd, p_meas = same_as_p
- Plugins: [case_studies/a5_suppression_circuit_level/codes.py](../../a5_suppression_circuit_level/codes.py), [case_studies/a5_suppression_circuit_level/noises.py](../../a5_suppression_circuit_level/noises.py)
- Sweeps:
  - `threshold_sweep`: d = [9 .. 21] (7), rounds = 3 * d, basis Z, p = 10 pts [5.00e-03 .. 6.20e-03]
  - `suppression_sweep`: d = [3, 5, 7], rounds = d, basis Z, p = 3.00e-03
- Sampling: decoder mwpm, each task until 5,000 errors or 500,000 shots, 4 workers
- Run: 2026-11-05 21:12:01 → 21:58:18 (46m 17s), git da1c610 with uncommitted changes

## Warnings

- rotated_surface_sd Z p=3.00e-03: d_teraquop=61 is extrapolated far beyond the largest sampled d=7

## Threshold

Sweep `threshold_sweep`, fit on d = [9, 11, 13, 15, 17, 19, 21], x_window = 0.012, ν0 = 1.06. Data: [threshold.csv](threshold.csv)

| code               | basis   | p_th              | ν    | χ²_red   | p-value   | figure                                            |
|--------------------|---------|-------------------|------|----------|-----------|---------------------------------------------------|
| rotated_surface_sd | Z       | 0.5661% ± 0.0008% | 1.17 | 1.17     | 0.166     | [PDF](figures/threshold_rotated_surface_sd_Z.pdf) |

## Teraquop footprint

Sweep `suppression_sweep`, target p_L = 1e-12 per d rounds. Data: [suppression.csv](suppression.csv)

| code               | basis   | p        | d*   | d_teraquop   | qubits   | figure                                              |
|--------------------|---------|----------|------|--------------|----------|-----------------------------------------------------|
| rotated_surface_sd | Z       | 3.00e-03 | 60.0 | 61           | 7,441    | [PDF](figures/suppression_rotated_surface_sd_Z.pdf) |

## Sampling

Data: [samples.csv](samples.csv). 73 tasks, 3.3M shots, 372,055 errors. Limited by max_errors: 72 tasks; by max_shots: 1 tasks.

| sweep             | code               | basis   | d             | p                             | tasks   | shots   | min errors   |
|-------------------|--------------------|---------|---------------|-------------------------------|---------|---------|--------------|
| threshold_sweep   | rotated_surface_sd | Z       | [9 .. 21] (7) | 10 pts [5.00e-03 .. 6.20e-03] | 70      | 2.1M    | 5,000        |
| suppression_sweep | rotated_surface_sd | Z       | [3, 5, 7]     | 3.00e-03                      | 3       | 1.2M    | 3,769        |

## Validation

Data: [validation.json](validation.json). 4 of 4 passed.

## Circuit diagrams

- rotated_surface_sd: [d3 detslice](diagrams/rotated_surface_sd/rotated_surface_sd_d3_detslice.svg) · [d3 timeline](diagrams/rotated_surface_sd/rotated_surface_sd_d3_timeline.svg) · [d5 detslice](diagrams/rotated_surface_sd/rotated_surface_sd_d5_detslice.svg) · [d5 timeline](diagrams/rotated_surface_sd/rotated_surface_sd_d5_timeline.svg) · [d7 detslice](diagrams/rotated_surface_sd/rotated_surface_sd_d7_detslice.svg) · [d7 timeline](diagrams/rotated_surface_sd/rotated_surface_sd_d7_timeline.svg)

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
