# Summary: a4_circuit_level_sd

Written by `cdsc summarize` on 2026-11-05 00:18.

## Setup

- Config: [case_studies/a4_circuit_level_depolarizing/config_sd.yaml](../config_sd.yaml)
- Codes: rotated_surface_sd
- Noise: circuit_level / depolarizing_sd, p_meas = same_as_p
- Plugins: [case_studies/a5_suppression_circuit_level/codes.py](../../a5_suppression_circuit_level/codes.py), [case_studies/a5_suppression_circuit_level/noises.py](../../a5_suppression_circuit_level/noises.py)
- Sweeps:
  - `threshold_sweep`: d = [7 .. 15] (5), basis Z, p = 13 pts [4.40e-03 .. 6.80e-03]
  - `suppression_sweep`: d = [3, 5, 7], basis Z, p = 3.00e-03
- Sampling: decoder mwpm, each task until 20,000 errors or 1,000,000 shots, 4 workers
- Run: 2026-11-01 20:26:10, git f660cb9

## Warnings

- rotated_surface_sd Z p=3.00e-03: d_teraquop=63 is extrapolated far beyond the largest sampled d=7

## Threshold

Sweep `threshold_sweep`, fit on d = [9, 11, 13, 15], x_window = 0.012, ν0 = 1.06. Data: [threshold.csv](threshold.csv)

| code               | basis   | p_th              | ν    | χ²_red   | p-value   | figure                                            |
|--------------------|---------|-------------------|------|----------|-----------|---------------------------------------------------|
| rotated_surface_sd | Z       | 0.5687% ± 0.0007% | 1.14 | 1.12     | 0.279     | [PDF](figures/threshold_rotated_surface_sd_Z.pdf) |

## Teraquop footprint

Sweep `suppression_sweep`, target p_L = 1e-12 per d rounds. Data: [suppression.csv](suppression.csv)

| code               | basis   | p        | d*   | d_teraquop   | qubits   | figure                                              |
|--------------------|---------|----------|------|--------------|----------|-----------------------------------------------------|
| rotated_surface_sd | Z       | 3.00e-03 | 61.0 | 63           | 7,937    | [PDF](figures/suppression_rotated_surface_sd_Z.pdf) |

## Sampling

Data: [samples.csv](samples.csv). 68 tasks, 29.2M shots, 1,332,698 errors. Limited by max_errors: 62 tasks; by max_shots: 6 tasks.

| sweep             | code               | basis   | d             | p                             | tasks   | shots   | min errors   |
|-------------------|--------------------|---------|---------------|-------------------------------|---------|---------|--------------|
| threshold_sweep   | rotated_surface_sd | Z       | [7 .. 15] (5) | 13 pts [4.40e-03 .. 6.80e-03] | 65      | 26.2M   | 12,135       |
| suppression_sweep | rotated_surface_sd | Z       | [3, 5, 7]     | 3.00e-03                      | 3       | 3.0M    | 7,736        |

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
