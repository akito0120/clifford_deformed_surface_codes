# Summary: half_xzzx

Written by `cdsc summarize` on 2026-11-05 00:56.

## Setup

- Config: [examples/half_xzzx/config.yaml](../config.yaml)
- Codes: rotated_surface, xzzx, half_xzzx
- Noise: circuit_level / dephasing, p_meas = same_as_p
- Plugins: [examples/half_xzzx/my_codes.py](../my_codes.py), [examples/half_xzzx/my_noises.py](../my_noises.py)
- Sweeps:
  - `threshold_sweep`: d = [5, 7, 9], basis X, p = 63 pts [3.20e-03 .. 2.41e-02]
  - `suppression_sweep`: d = [3, 5, 7, 9], basis X, p = 2 pts [3.00e-03 .. 4.00e-03]
- Sampling: decoder mwpm, each task until 2,000 errors or 20,000 shots, 4 workers
- Run: 2026-11-05 00:55:54 → 00:56:43 (48.3s), git f406ab6 with uncommitted changes

## Warnings

- 1 tasks observed 0 errors (suppression_sweep xzzx X d=9 p=3.00e-03)
- 8 tasks have < 100 errors; their error bars will be wide
- half_xzzx X p=3.00e-03: d_teraquop=49 is extrapolated far beyond the largest sampled d=9
- half_xzzx X p=4.00e-03: d_teraquop=67 is extrapolated far beyond the largest sampled d=9
- rotated_surface X p=3.00e-03: d_teraquop=61 is extrapolated far beyond the largest sampled d=9
- rotated_surface X p=4.00e-03: d_teraquop=91 is extrapolated far beyond the largest sampled d=9
- xzzx X p=3.00e-03: d_teraquop=25 is extrapolated far beyond the largest sampled d=9
- xzzx X p=4.00e-03: d_teraquop=31 is extrapolated far beyond the largest sampled d=9

## Threshold

Sweep `threshold_sweep`, fit on d = [5, 7, 9], x_window = 0.012, ν0 = 1.1. Data: [threshold.csv](threshold.csv)

| code            | basis   | p_th              | ν    | χ²_red   | p-value   | figure                                         |
|-----------------|---------|-------------------|------|----------|-----------|------------------------------------------------|
| half_xzzx       | X       | 0.6861% ± 0.0051% | 1.37 | 1.07     | 0.350     | [PDF](figures/threshold_half_xzzx_X.pdf)       |
| rotated_surface | X       | 0.5696% ± 0.0039% | 1.30 | 1.43     | 0.032     | [PDF](figures/threshold_rotated_surface_X.pdf) |
| xzzx            | X       | 2.1671% ± 0.0143% | 1.22 | 0.75     | 0.887     | [PDF](figures/threshold_xzzx_X.pdf)            |

## Teraquop footprint

Sweep `suppression_sweep`, target p_L = 1e-12 per d rounds. Data: [suppression.csv](suppression.csv)

| code            | basis   | p        | d*   | d_teraquop   | qubits   | figure                                           |
|-----------------|---------|----------|------|--------------|----------|--------------------------------------------------|
| half_xzzx       | X       | 3.00e-03 | 48.3 | 49           | 4,801    | [PDF](figures/suppression_half_xzzx_X.pdf)       |
| half_xzzx       | X       | 4.00e-03 | 66.3 | 67           | 8,977    | [PDF](figures/suppression_half_xzzx_X.pdf)       |
| rotated_surface | X       | 3.00e-03 | 60.8 | 61           | 7,441    | [PDF](figures/suppression_rotated_surface_X.pdf) |
| rotated_surface | X       | 4.00e-03 | 90.2 | 91           | 16,561   | [PDF](figures/suppression_rotated_surface_X.pdf) |
| xzzx            | X       | 3.00e-03 | 24.9 | 25           | 1,249    | [PDF](figures/suppression_xzzx_X.pdf)            |
| xzzx            | X       | 4.00e-03 | 29.3 | 31           | 1,921    | [PDF](figures/suppression_xzzx_X.pdf)            |

## Sampling

Data: [samples.csv](samples.csv). 213 tasks, 3.4M shots, 315,739 errors. Limited by max_errors: 109 tasks; by max_shots: 104 tasks.

| sweep             | code            | basis   | d            | p                             | tasks   | shots   | min errors   |
|-------------------|-----------------|---------|--------------|-------------------------------|---------|---------|--------------|
| threshold_sweep   | rotated_surface | X       | [5, 7, 9]    | 21 pts [3.20e-03 .. 8.20e-03] | 63      | 1.1M    | 124          |
| threshold_sweep   | xzzx            | X       | [5, 7, 9]    | 21 pts [1.91e-02 .. 2.41e-02] | 63      | 663.4k  | 2,003        |
| threshold_sweep   | half_xzzx       | X       | [5, 7, 9]    | 21 pts [4.40e-03 .. 9.40e-03] | 63      | 1.2M    | 249          |
| suppression_sweep | rotated_surface | X       | [3, 5, 7, 9] | 2 pts [3.00e-03 .. 4.00e-03]  | 8       | 160.0k  | 96           |
| suppression_sweep | xzzx            | X       | [3, 5, 7, 9] | 2 pts [3.00e-03 .. 4.00e-03]  | 8       | 160.0k  | 0            |
| suppression_sweep | half_xzzx       | X       | [3, 5, 7, 9] | 2 pts [3.00e-03 .. 4.00e-03]  | 8       | 160.0k  | 38           |

## Validation

Data: [validation.json](validation.json). 12 of 12 passed.

## Circuit diagrams

- rotated_surface: [d3 detslice](diagrams/rotated_surface/rotated_surface_d3_detslice.svg) · [d3 timeline](diagrams/rotated_surface/rotated_surface_d3_timeline.svg) · [d5 detslice](diagrams/rotated_surface/rotated_surface_d5_detslice.svg) · [d5 timeline](diagrams/rotated_surface/rotated_surface_d5_timeline.svg) · [d7 detslice](diagrams/rotated_surface/rotated_surface_d7_detslice.svg) · [d7 timeline](diagrams/rotated_surface/rotated_surface_d7_timeline.svg)
- xzzx: [d3 detslice](diagrams/xzzx/xzzx_d3_detslice.svg) · [d3 timeline](diagrams/xzzx/xzzx_d3_timeline.svg) · [d5 detslice](diagrams/xzzx/xzzx_d5_detslice.svg) · [d5 timeline](diagrams/xzzx/xzzx_d5_timeline.svg) · [d7 detslice](diagrams/xzzx/xzzx_d7_detslice.svg) · [d7 timeline](diagrams/xzzx/xzzx_d7_timeline.svg)
- half_xzzx: [d3 detslice](diagrams/half_xzzx/half_xzzx_d3_detslice.svg) · [d3 timeline](diagrams/half_xzzx/half_xzzx_d3_timeline.svg) · [d5 detslice](diagrams/half_xzzx/half_xzzx_d5_detslice.svg) · [d5 timeline](diagrams/half_xzzx/half_xzzx_d5_timeline.svg) · [d7 detslice](diagrams/half_xzzx/half_xzzx_d7_detslice.svg) · [d7 timeline](diagrams/half_xzzx/half_xzzx_d7_timeline.svg)

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
