# Summary: a5_suppression_circuit_level

Written by `cdsc summarize` on 2026-11-05 00:19.

## Setup

- Config: [case_studies/a5_suppression_circuit_level/config_suppression.yaml](../../config_suppression.yaml)
- Codes: rotated_surface_sd
- Noise: circuit_level / depolarizing_sd, p_meas = same_as_p
- Plugins: [case_studies/a5_suppression_circuit_level/codes.py](../../codes.py), [case_studies/a5_suppression_circuit_level/noises.py](../../noises.py)
- Sweeps:
  - `threshold_placeholder`: d = [3, 5, 7], basis Z, p = 7 pts [4.00e-03 .. 7.00e-03]
  - `suppression_sweep`: d = [7, 9, 11, 13], basis Z, p = 2 pts [1.00e-03 .. 2.00e-03]
- Sampling: decoder mwpm, each task until 1,000 errors or 200,000,000 shots, 4 workers
- Run: 2026-10-22 00:33:14, git 84b7c74

## Warnings

- plugins in the config changed after `cdsc run`; samples.csv was made with the config recorded in manifest.json
- 1 tasks have < 100 errors; their error bars will be wide
- rotated_surface_sd Z p=1.00e-03: d_teraquop=27 is extrapolated far beyond the largest sampled d=13
- rotated_surface_sd Z p=2.00e-03: d_teraquop=43 is extrapolated far beyond the largest sampled d=13

## Threshold

Sweep `threshold_placeholder`, fit on d = [3, 5, 7], x_window = 0.01, ν0 = 1.06. Data: [threshold.csv](threshold.csv)

| code               | basis   | p_th              | ν    | χ²_red   | p-value   | figure                                            |
|--------------------|---------|-------------------|------|----------|-----------|---------------------------------------------------|
| rotated_surface_sd | Z       | 0.5233% ± 0.0040% | 1.24 | 1.66     | 0.051     | [PDF](figures/threshold_rotated_surface_sd_Z.pdf) |

## Teraquop footprint

Sweep `suppression_sweep`, target p_L = 1e-12 per d rounds. Data: [suppression.csv](suppression.csv)

| code               | basis   | p        | d*   | d_teraquop   | qubits   | figure                                              |
|--------------------|---------|----------|------|--------------|----------|-----------------------------------------------------|
| rotated_surface_sd | Z       | 1.00e-03 | 26.3 | 27           | 1,457    | [PDF](figures/suppression_rotated_surface_sd_Z.pdf) |
| rotated_surface_sd | Z       | 2.00e-03 | 42.7 | 43           | 3,697    | [PDF](figures/suppression_rotated_surface_sd_Z.pdf) |

## Sampling

Data: [samples.csv](samples.csv). 29 tasks, 492.6M shots, 81,276 errors. Limited by max_errors: 27 tasks; by max_shots: 2 tasks.

| sweep                 | code               | basis   | d              | p                            | tasks   | shots   | min errors   |
|-----------------------|--------------------|---------|----------------|------------------------------|---------|---------|--------------|
| threshold_placeholder | rotated_surface_sd | Z       | [3, 5, 7]      | 7 pts [4.00e-03 .. 7.00e-03] | 21      | 1.2M    | 1,182        |
| suppression_sweep     | rotated_surface_sd | Z       | [7, 9, 11, 13] | 2 pts [1.00e-03 .. 2.00e-03] | 8       | 491.4M  | 75           |

## Validation

Data: [validation.json](validation.json). 4 of 4 passed.

## Circuit diagrams

- rotated_surface_sd: [d3 detslice](diagrams/rotated_surface_sd/rotated_surface_sd_d3_detslice.svg) · [d3 timeline](diagrams/rotated_surface_sd/rotated_surface_sd_d3_timeline.svg) · [d5 detslice](diagrams/rotated_surface_sd/rotated_surface_sd_d5_detslice.svg) · [d5 timeline](diagrams/rotated_surface_sd/rotated_surface_sd_d5_timeline.svg) · [d7 detslice](diagrams/rotated_surface_sd/rotated_surface_sd_d7_detslice.svg) · [d7 timeline](diagrams/rotated_surface_sd/rotated_surface_sd_d7_timeline.svg)

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
