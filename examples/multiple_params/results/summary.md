# Summary: multiple_params

Written by `cdsc summarize` on 2026-11-05 00:50.

## Setup

- Config: [examples/multiple_params/config.yaml](../config.yaml)
- Codes: rotated_surface, xzzx
- Noise: phenomenological / biased_meas_ratio, eta = [0.5, 10], meas_ratio = [0.5, 1], p_meas = same_as_p
- Plugins: [examples/multiple_params/my_noises.py](../my_noises.py)
- Sweeps:
  - `threshold_sweep`: d = [5, 7, 9], basis X, p = 15 pts [2.00e-02 .. 9.00e-02]
  - `suppression_sweep`: d = [3, 5, 7, 9], basis X, p = 2 pts [1.00e-02 .. 1.50e-02]
- Sampling: decoder mwpm, each task until 2,000 errors or 100,000 shots, 4 workers
- Run: 2026-11-05 00:47:40 → 00:50:22 (2m 42s), git f406ab6

## Warnings

- 25 tasks have < 100 errors; their error bars will be wide
- rotated_surface X eta=0.5 meas_ratio=1: poor fit (chi2_red=2.58, p-value=0.002)
- rotated_surface X eta=10 meas_ratio=0.5: poor fit (chi2_red=2.38, p-value=0.005)
- rotated_surface X eta=10 meas_ratio=1: poor fit (chi2_red=2.93, p-value=0.001)
- xzzx X eta=10 meas_ratio=0.5: poor fit (chi2_red=3.24, p-value=0.000)
- rotated_surface X eta=0.5 meas_ratio=0.5 p=1.00e-02: d_teraquop=31 is extrapolated far beyond the largest sampled d=9
- rotated_surface X eta=0.5 meas_ratio=0.5 p=1.50e-02: d_teraquop=39 is extrapolated far beyond the largest sampled d=9
- rotated_surface X eta=0.5 meas_ratio=1 p=1.00e-02: d_teraquop=33 is extrapolated far beyond the largest sampled d=9
- rotated_surface X eta=0.5 meas_ratio=1 p=1.50e-02: d_teraquop=43 is extrapolated far beyond the largest sampled d=9
- rotated_surface X eta=10 meas_ratio=0.5 p=1.00e-02: d_teraquop=37 is extrapolated far beyond the largest sampled d=9
- rotated_surface X eta=10 meas_ratio=0.5 p=1.50e-02: d_teraquop=51 is extrapolated far beyond the largest sampled d=9
- rotated_surface X eta=10 meas_ratio=1 p=1.00e-02: d_teraquop=41 is extrapolated far beyond the largest sampled d=9
- rotated_surface X eta=10 meas_ratio=1 p=1.50e-02: d_teraquop=57 is extrapolated far beyond the largest sampled d=9
- xzzx X eta=0.5 meas_ratio=0.5 p=1.00e-02: d_teraquop=31 is extrapolated far beyond the largest sampled d=9
- xzzx X eta=0.5 meas_ratio=0.5 p=1.50e-02: d_teraquop=41 is extrapolated far beyond the largest sampled d=9
- xzzx X eta=0.5 meas_ratio=1 p=1.00e-02: d_teraquop=31 is extrapolated far beyond the largest sampled d=9
- xzzx X eta=0.5 meas_ratio=1 p=1.50e-02: d_teraquop=43 is extrapolated far beyond the largest sampled d=9
- xzzx X eta=10 meas_ratio=0.5 p=1.00e-02: d_teraquop=25 is extrapolated far beyond the largest sampled d=9
- xzzx X eta=10 meas_ratio=0.5 p=1.50e-02: d_teraquop=31 is extrapolated far beyond the largest sampled d=9
- xzzx X eta=10 meas_ratio=1 p=1.00e-02: d_teraquop=25 is extrapolated far beyond the largest sampled d=9
- xzzx X eta=10 meas_ratio=1 p=1.50e-02: d_teraquop=33 is extrapolated far beyond the largest sampled d=9

## Threshold

Sweep `threshold_sweep`, fit on d = [5, 7, 9], x_window = 0.05, ν0 = 1.5. Data: [threshold.csv](threshold.csv)

| code            | basis   | eta   | meas_ratio   | p_th              | ν    | χ²_red   | p-value   | figure                                                  |
|-----------------|---------|-------|--------------|-------------------|------|----------|-----------|---------------------------------------------------------|
| rotated_surface | X       | 0.5   | 0.5          | 4.6095% ± 0.0421% | 1.23 | 1.23     | 0.251     | [PDF](figures/threshold_rotated_surface_X_0.5_0.5.pdf)  |
| rotated_surface | X       | 0.5   | 1            | 3.9171% ± 0.0349% | 1.26 | 2.58     | 0.002     | [PDF](figures/threshold_rotated_surface_X_0.5_1.0.pdf)  |
| rotated_surface | X       | 10    | 0.5          | 3.4874% ± 0.0357% | 1.42 | 2.38     | 0.005     | [PDF](figures/threshold_rotated_surface_X_10.0_0.5.pdf) |
| rotated_surface | X       | 10    | 1            | 3.0001% ± 0.0266% | 1.19 | 2.93     | 0.001     | [PDF](figures/threshold_rotated_surface_X_10.0_1.0.pdf) |
| xzzx            | X       | 0.5   | 0.5          | 4.7423% ± 0.0484% | 1.28 | 0.67     | 0.764     | [PDF](figures/threshold_xzzx_X_0.5_0.5.pdf)             |
| xzzx            | X       | 0.5   | 1            | 3.8837% ± 0.0311% | 1.15 | 0.93     | 0.520     | [PDF](figures/threshold_xzzx_X_0.5_1.0.pdf)             |
| xzzx            | X       | 10    | 0.5          | 7.7398% ± 0.0663% | 1.03 | 3.24     | 0.000     | [PDF](figures/threshold_xzzx_X_10.0_0.5.pdf)            |
| xzzx            | X       | 10    | 1            | 5.7293% ± 0.0545% | 1.21 | 1.31     | 0.206     | [PDF](figures/threshold_xzzx_X_10.0_1.0.pdf)            |

## Teraquop footprint

Sweep `suppression_sweep`, target p_L = 1e-12 per d rounds. Data: [suppression.csv](suppression.csv)

| code            | basis   | eta   | meas_ratio   | p        | d*   | d_teraquop   | qubits   | figure                                                    |
|-----------------|---------|-------|--------------|----------|------|--------------|----------|-----------------------------------------------------------|
| rotated_surface | X       | 0.5   | 0.5          | 1.00e-02 | 29.9 | 31           | 1,921    | [PDF](figures/suppression_rotated_surface_X_0.5_0.5.pdf)  |
| rotated_surface | X       | 0.5   | 0.5          | 1.50e-02 | 37.6 | 39           | 3,041    | [PDF](figures/suppression_rotated_surface_X_0.5_0.5.pdf)  |
| rotated_surface | X       | 0.5   | 1            | 1.00e-02 | 31.5 | 33           | 2,177    | [PDF](figures/suppression_rotated_surface_X_0.5_1.0.pdf)  |
| rotated_surface | X       | 0.5   | 1            | 1.50e-02 | 42.6 | 43           | 3,697    | [PDF](figures/suppression_rotated_surface_X_0.5_1.0.pdf)  |
| rotated_surface | X       | 10    | 0.5          | 1.00e-02 | 36.5 | 37           | 2,737    | [PDF](figures/suppression_rotated_surface_X_10.0_0.5.pdf) |
| rotated_surface | X       | 10    | 0.5          | 1.50e-02 | 50.4 | 51           | 5,201    | [PDF](figures/suppression_rotated_surface_X_10.0_0.5.pdf) |
| rotated_surface | X       | 10    | 1            | 1.00e-02 | 39.1 | 41           | 3,361    | [PDF](figures/suppression_rotated_surface_X_10.0_1.0.pdf) |
| rotated_surface | X       | 10    | 1            | 1.50e-02 | 55.8 | 57           | 6,497    | [PDF](figures/suppression_rotated_surface_X_10.0_1.0.pdf) |
| xzzx            | X       | 0.5   | 0.5          | 1.00e-02 | 30.1 | 31           | 1,921    | [PDF](figures/suppression_xzzx_X_0.5_0.5.pdf)             |
| xzzx            | X       | 0.5   | 0.5          | 1.50e-02 | 39.1 | 41           | 3,361    | [PDF](figures/suppression_xzzx_X_0.5_0.5.pdf)             |
| xzzx            | X       | 0.5   | 1            | 1.00e-02 | 30.2 | 31           | 1,921    | [PDF](figures/suppression_xzzx_X_0.5_1.0.pdf)             |
| xzzx            | X       | 0.5   | 1            | 1.50e-02 | 41.3 | 43           | 3,697    | [PDF](figures/suppression_xzzx_X_0.5_1.0.pdf)             |
| xzzx            | X       | 10    | 0.5          | 1.00e-02 | 25.0 | 25           | 1,249    | [PDF](figures/suppression_xzzx_X_10.0_0.5.pdf)            |
| xzzx            | X       | 10    | 0.5          | 1.50e-02 | 29.5 | 31           | 1,921    | [PDF](figures/suppression_xzzx_X_10.0_0.5.pdf)            |
| xzzx            | X       | 10    | 1            | 1.00e-02 | 24.5 | 25           | 1,249    | [PDF](figures/suppression_xzzx_X_10.0_1.0.pdf)            |
| xzzx            | X       | 10    | 1            | 1.50e-02 | 31.3 | 33           | 2,177    | [PDF](figures/suppression_xzzx_X_10.0_1.0.pdf)            |

## Sampling

Data: [samples.csv](samples.csv). 424 tasks, 17.1M shots, 739,934 errors. Limited by max_errors: 313 tasks; by max_shots: 111 tasks.

| sweep             | code            | basis   | eta   | meas_ratio   | d            | p                             | tasks   | shots   | min errors   |
|-------------------|-----------------|---------|-------|--------------|--------------|-------------------------------|---------|---------|--------------|
| threshold_sweep   | rotated_surface | X       | 0.5   | 0.5          | [5, 7, 9]    | 15 pts [2.00e-02 .. 9.00e-02] | 45      | 1.5M    | 164          |
| threshold_sweep   | xzzx            | X       | 0.5   | 0.5          | [5, 7, 9]    | 15 pts [2.00e-02 .. 9.00e-02] | 45      | 1.5M    | 192          |
| threshold_sweep   | rotated_surface | X       | 0.5   | 1            | [5, 7, 9]    | 15 pts [2.00e-02 .. 9.00e-02] | 45      | 1.1M    | 434          |
| threshold_sweep   | xzzx            | X       | 0.5   | 1            | [5, 7, 9]    | 15 pts [2.00e-02 .. 9.00e-02] | 45      | 1.1M    | 406          |
| threshold_sweep   | rotated_surface | X       | 10    | 0.5          | [5, 7, 9]    | 15 pts [2.00e-02 .. 9.00e-02] | 45      | 915.2k  | 754          |
| threshold_sweep   | xzzx            | X       | 10    | 0.5          | [5, 7, 9]    | 15 pts [2.00e-02 .. 9.00e-02] | 45      | 2.4M    | 34           |
| threshold_sweep   | rotated_surface | X       | 10    | 1            | [5, 7, 9]    | 15 pts [2.00e-02 .. 9.00e-02] | 45      | 662.8k  | 1,523        |
| threshold_sweep   | xzzx            | X       | 10    | 1            | [5, 7, 9]    | 15 pts [2.00e-02 .. 9.00e-02] | 45      | 1.6M    | 101          |
| suppression_sweep | rotated_surface | X       | 0.5   | 0.5          | [3, 5, 7, 9] | 2 pts [1.00e-02 .. 1.50e-02]  | 8       | 800.0k  | 7            |
| suppression_sweep | xzzx            | X       | 0.5   | 0.5          | [3, 5, 7, 9] | 2 pts [1.00e-02 .. 1.50e-02]  | 8       | 800.0k  | 6            |
| suppression_sweep | rotated_surface | X       | 0.5   | 1            | [3, 5, 7, 9] | 2 pts [1.00e-02 .. 1.50e-02]  | 8       | 800.0k  | 12           |
| suppression_sweep | xzzx            | X       | 0.5   | 1            | [3, 5, 7, 9] | 2 pts [1.00e-02 .. 1.50e-02]  | 8       | 800.0k  | 8            |
| suppression_sweep | rotated_surface | X       | 10    | 0.5          | [3, 5, 7, 9] | 2 pts [1.00e-02 .. 1.50e-02]  | 8       | 800.0k  | 33           |
| suppression_sweep | xzzx            | X       | 10    | 0.5          | [3, 5, 7, 9] | 2 pts [1.00e-02 .. 1.50e-02]  | 8       | 800.0k  | 1            |
| suppression_sweep | rotated_surface | X       | 10    | 1            | [3, 5, 7, 9] | 2 pts [1.00e-02 .. 1.50e-02]  | 8       | 774.0k  | 50           |
| suppression_sweep | xzzx            | X       | 10    | 1            | [3, 5, 7, 9] | 2 pts [1.00e-02 .. 1.50e-02]  | 8       | 800.0k  | 1            |

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
