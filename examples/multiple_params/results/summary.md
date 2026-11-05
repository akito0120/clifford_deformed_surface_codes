# Summary: multiple_params

Written by `cdsc summarize` on 2026-11-05 19:54.

## Setup

- Config: [examples/multiple_params/config.yaml](../config.yaml)
- Codes: rotated_surface, xzzx
- Noise: phenomenological / biased_meas_ratio, eta = [0.5, 10], meas_ratio = [0.5, 1], p_meas = same_as_p
- Plugins: [examples/multiple_params/my_noises.py](../my_noises.py)
- Sweeps:
  - `threshold_sweep`: d = [5, 7, 9], rounds = 2 * d, basis X, p = 15 pts [2.00e-02 .. 9.00e-02]
  - `suppression_sweep`: d = [3, 5, 7, 9], rounds = 2 * d, basis X, p = 2 pts [1.00e-02 .. 1.50e-02]
- Sampling: decoder mwpm, each task until 2,000 errors or 100,000 shots, 4 workers
- Run: 2026-11-05 19:51:12 → 19:53:51 (2m 39s), git 9753b75 with uncommitted changes

## Warnings

- 18 tasks have < 100 errors; their error bars will be wide
- rotated_surface X eta=0.5 meas_ratio=1: poor fit (chi2_red=3.60, p-value=0.000)
- rotated_surface X eta=10 meas_ratio=0.5: poor fit (chi2_red=2.81, p-value=0.001)
- rotated_surface X eta=10 meas_ratio=1: poor fit (chi2_red=6.94, p-value=0.000)
- xzzx X eta=0.5 meas_ratio=1: poor fit (chi2_red=2.92, p-value=0.000)
- rotated_surface X eta=0.5 meas_ratio=0.5 p=1.00e-02: d_teraquop=31 is extrapolated far beyond the largest sampled d=9
- rotated_surface X eta=0.5 meas_ratio=0.5 p=1.50e-02: d_teraquop=41 is extrapolated far beyond the largest sampled d=9
- rotated_surface X eta=0.5 meas_ratio=1 p=1.00e-02: d_teraquop=33 is extrapolated far beyond the largest sampled d=9
- rotated_surface X eta=0.5 meas_ratio=1 p=1.50e-02: d_teraquop=45 is extrapolated far beyond the largest sampled d=9
- rotated_surface X eta=10 meas_ratio=0.5 p=1.00e-02: d_teraquop=37 is extrapolated far beyond the largest sampled d=9
- rotated_surface X eta=10 meas_ratio=0.5 p=1.50e-02: d_teraquop=51 is extrapolated far beyond the largest sampled d=9
- rotated_surface X eta=10 meas_ratio=1 p=1.00e-02: d_teraquop=41 is extrapolated far beyond the largest sampled d=9
- rotated_surface X eta=10 meas_ratio=1 p=1.50e-02: d_teraquop=57 is extrapolated far beyond the largest sampled d=9
- xzzx X eta=0.5 meas_ratio=0.5 p=1.00e-02: d_teraquop=31 is extrapolated far beyond the largest sampled d=9
- xzzx X eta=0.5 meas_ratio=0.5 p=1.50e-02: d_teraquop=41 is extrapolated far beyond the largest sampled d=9
- xzzx X eta=0.5 meas_ratio=1 p=1.00e-02: d_teraquop=33 is extrapolated far beyond the largest sampled d=9
- xzzx X eta=0.5 meas_ratio=1 p=1.50e-02: d_teraquop=43 is extrapolated far beyond the largest sampled d=9
- xzzx X eta=10 meas_ratio=0.5 p=1.00e-02: d_teraquop=23 is extrapolated far beyond the largest sampled d=9
- xzzx X eta=10 meas_ratio=0.5 p=1.50e-02: d_teraquop=29 is extrapolated far beyond the largest sampled d=9
- xzzx X eta=10 meas_ratio=1 p=1.00e-02: d_teraquop=27 is extrapolated far beyond the largest sampled d=9
- xzzx X eta=10 meas_ratio=1 p=1.50e-02: d_teraquop=31 is extrapolated far beyond the largest sampled d=9

## Threshold

Sweep `threshold_sweep`, fit on d = [5, 7, 9], x_window = 0.05, ν0 = 1.5. Data: [threshold.csv](threshold.csv)

| code            | basis   | eta   | meas_ratio   | p_th              | ν    | χ²_red   | p-value   | figure                                                  |
|-----------------|---------|-------|--------------|-------------------|------|----------|-----------|---------------------------------------------------------|
| rotated_surface | X       | 0.5   | 0.5          | 4.6067% ± 0.0429% | 1.16 | 1.11     | 0.346     | [PDF](figures/threshold_rotated_surface_X_0.5_0.5.pdf)  |
| rotated_surface | X       | 0.5   | 1            | 3.7772% ± 0.0315% | 1.18 | 3.60     | 0.000     | [PDF](figures/threshold_rotated_surface_X_0.5_1.0.pdf)  |
| rotated_surface | X       | 10    | 0.5          | 3.4691% ± 0.0368% | 1.37 | 2.81     | 0.001     | [PDF](figures/threshold_rotated_surface_X_10.0_0.5.pdf) |
| rotated_surface | X       | 10    | 1            | 2.8727% ± 0.0307% | 1.37 | 6.94     | 0.000     | [PDF](figures/threshold_rotated_surface_X_10.0_1.0.pdf) |
| xzzx            | X       | 0.5   | 0.5          | 4.4891% ± 0.0433% | 1.25 | 1.26     | 0.235     | [PDF](figures/threshold_xzzx_X_0.5_0.5.pdf)             |
| xzzx            | X       | 0.5   | 1            | 3.7866% ± 0.0327% | 1.24 | 2.92     | 0.000     | [PDF](figures/threshold_xzzx_X_0.5_1.0.pdf)             |
| xzzx            | X       | 10    | 0.5          | 7.4087% ± 0.0778% | 1.25 | 0.99     | 0.462     | [PDF](figures/threshold_xzzx_X_10.0_0.5.pdf)            |
| xzzx            | X       | 10    | 1            | 5.6138% ± 0.0658% | 1.42 | 0.98     | 0.467     | [PDF](figures/threshold_xzzx_X_10.0_1.0.pdf)            |

## Teraquop footprint

Sweep `suppression_sweep`, target p_L = 1e-12 per d rounds. Data: [suppression.csv](suppression.csv)

| code            | basis   | eta   | meas_ratio   | p        | d*   | d_teraquop   | qubits   | figure                                                    |
|-----------------|---------|-------|--------------|----------|------|--------------|----------|-----------------------------------------------------------|
| rotated_surface | X       | 0.5   | 0.5          | 1.00e-02 | 30.2 | 31           | 1,921    | [PDF](figures/suppression_rotated_surface_X_0.5_0.5.pdf)  |
| rotated_surface | X       | 0.5   | 0.5          | 1.50e-02 | 39.9 | 41           | 3,361    | [PDF](figures/suppression_rotated_surface_X_0.5_0.5.pdf)  |
| rotated_surface | X       | 0.5   | 1            | 1.00e-02 | 31.1 | 33           | 2,177    | [PDF](figures/suppression_rotated_surface_X_0.5_1.0.pdf)  |
| rotated_surface | X       | 0.5   | 1            | 1.50e-02 | 43.2 | 45           | 4,049    | [PDF](figures/suppression_rotated_surface_X_0.5_1.0.pdf)  |
| rotated_surface | X       | 10    | 0.5          | 1.00e-02 | 36.6 | 37           | 2,737    | [PDF](figures/suppression_rotated_surface_X_10.0_0.5.pdf) |
| rotated_surface | X       | 10    | 0.5          | 1.50e-02 | 50.2 | 51           | 5,201    | [PDF](figures/suppression_rotated_surface_X_10.0_0.5.pdf) |
| rotated_surface | X       | 10    | 1            | 1.00e-02 | 39.8 | 41           | 3,361    | [PDF](figures/suppression_rotated_surface_X_10.0_1.0.pdf) |
| rotated_surface | X       | 10    | 1            | 1.50e-02 | 56.4 | 57           | 6,497    | [PDF](figures/suppression_rotated_surface_X_10.0_1.0.pdf) |
| xzzx            | X       | 0.5   | 0.5          | 1.00e-02 | 30.1 | 31           | 1,921    | [PDF](figures/suppression_xzzx_X_0.5_0.5.pdf)             |
| xzzx            | X       | 0.5   | 0.5          | 1.50e-02 | 40.2 | 41           | 3,361    | [PDF](figures/suppression_xzzx_X_0.5_0.5.pdf)             |
| xzzx            | X       | 0.5   | 1            | 1.00e-02 | 31.4 | 33           | 2,177    | [PDF](figures/suppression_xzzx_X_0.5_1.0.pdf)             |
| xzzx            | X       | 0.5   | 1            | 1.50e-02 | 42.6 | 43           | 3,697    | [PDF](figures/suppression_xzzx_X_0.5_1.0.pdf)             |
| xzzx            | X       | 10    | 0.5          | 1.00e-02 | 22.7 | 23           | 1,057    | [PDF](figures/suppression_xzzx_X_10.0_0.5.pdf)            |
| xzzx            | X       | 10    | 0.5          | 1.50e-02 | 28.1 | 29           | 1,681    | [PDF](figures/suppression_xzzx_X_10.0_0.5.pdf)            |
| xzzx            | X       | 10    | 1            | 1.00e-02 | 26.1 | 27           | 1,457    | [PDF](figures/suppression_xzzx_X_10.0_1.0.pdf)            |
| xzzx            | X       | 10    | 1            | 1.50e-02 | 29.9 | 31           | 1,921    | [PDF](figures/suppression_xzzx_X_10.0_1.0.pdf)            |

## Sampling

Data: [samples.csv](samples.csv). 424 tasks, 13.9M shots, 798,876 errors. Limited by max_errors: 342 tasks; by max_shots: 82 tasks.

| sweep             | code            | basis   | eta   | meas_ratio   | d            | p                             | tasks   | shots   | min errors   |
|-------------------|-----------------|---------|-------|--------------|--------------|-------------------------------|---------|---------|--------------|
| threshold_sweep   | rotated_surface | X       | 0.5   | 0.5          | [5, 7, 9]    | 15 pts [2.00e-02 .. 9.00e-02] | 45      | 1.0M    | 424          |
| threshold_sweep   | xzzx            | X       | 0.5   | 0.5          | [5, 7, 9]    | 15 pts [2.00e-02 .. 9.00e-02] | 45      | 1.0M    | 389          |
| threshold_sweep   | rotated_surface | X       | 0.5   | 1            | [5, 7, 9]    | 15 pts [2.00e-02 .. 9.00e-02] | 45      | 759.0k  | 850          |
| threshold_sweep   | xzzx            | X       | 0.5   | 1            | [5, 7, 9]    | 15 pts [2.00e-02 .. 9.00e-02] | 45      | 753.7k  | 847          |
| threshold_sweep   | rotated_surface | X       | 10    | 0.5          | [5, 7, 9]    | 15 pts [2.00e-02 .. 9.00e-02] | 45      | 591.0k  | 1,659        |
| threshold_sweep   | xzzx            | X       | 10    | 0.5          | [5, 7, 9]    | 15 pts [2.00e-02 .. 9.00e-02] | 45      | 1.9M    | 52           |
| threshold_sweep   | rotated_surface | X       | 10    | 1            | [5, 7, 9]    | 15 pts [2.00e-02 .. 9.00e-02] | 45      | 420.1k  | 2,007        |
| threshold_sweep   | xzzx            | X       | 10    | 1            | [5, 7, 9]    | 15 pts [2.00e-02 .. 9.00e-02] | 45      | 1.3M    | 169          |
| suppression_sweep | rotated_surface | X       | 0.5   | 0.5          | [3, 5, 7, 9] | 2 pts [1.00e-02 .. 1.50e-02]  | 8       | 791.4k  | 14           |
| suppression_sweep | xzzx            | X       | 0.5   | 0.5          | [3, 5, 7, 9] | 2 pts [1.00e-02 .. 1.50e-02]  | 8       | 791.4k  | 13           |
| suppression_sweep | rotated_surface | X       | 0.5   | 1            | [3, 5, 7, 9] | 2 pts [1.00e-02 .. 1.50e-02]  | 8       | 763.8k  | 27           |
| suppression_sweep | xzzx            | X       | 0.5   | 1            | [3, 5, 7, 9] | 2 pts [1.00e-02 .. 1.50e-02]  | 8       | 762.7k  | 14           |
| suppression_sweep | rotated_surface | X       | 10    | 0.5          | [3, 5, 7, 9] | 2 pts [1.00e-02 .. 1.50e-02]  | 8       | 751.1k  | 40           |
| suppression_sweep | xzzx            | X       | 10    | 0.5          | [3, 5, 7, 9] | 2 pts [1.00e-02 .. 1.50e-02]  | 8       | 800.0k  | 3            |
| suppression_sweep | rotated_surface | X       | 10    | 1            | [3, 5, 7, 9] | 2 pts [1.00e-02 .. 1.50e-02]  | 8       | 687.2k  | 118          |
| suppression_sweep | xzzx            | X       | 10    | 1            | [3, 5, 7, 9] | 2 pts [1.00e-02 .. 1.50e-02]  | 8       | 783.2k  | 9            |

## Validation

Data: [validation.json](validation.json). 8 of 8 passed.

## Circuit diagrams

- rotated_surface: [d3 detslice](diagrams/rotated_surface/rotated_surface_d3_detslice.svg) · [d3 timeline](diagrams/rotated_surface/rotated_surface_d3_timeline.svg) · [d5 detslice](diagrams/rotated_surface/rotated_surface_d5_detslice.svg) · [d5 timeline](diagrams/rotated_surface/rotated_surface_d5_timeline.svg) · [d7 detslice](diagrams/rotated_surface/rotated_surface_d7_detslice.svg) · [d7 timeline](diagrams/rotated_surface/rotated_surface_d7_timeline.svg)
- xzzx: [d3 detslice](diagrams/xzzx/xzzx_d3_detslice.svg) · [d3 timeline](diagrams/xzzx/xzzx_d3_timeline.svg) · [d5 detslice](diagrams/xzzx/xzzx_d5_detslice.svg) · [d5 timeline](diagrams/xzzx/xzzx_d5_timeline.svg) · [d7 detslice](diagrams/xzzx/xzzx_d7_detslice.svg) · [d7 timeline](diagrams/xzzx/xzzx_d7_timeline.svg)

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
