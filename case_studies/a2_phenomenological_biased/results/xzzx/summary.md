# Summary: a2_phenomenological_biased_xzzx

Written by `cdsc summarize` on 2026-11-05 00:14.

## Setup

- Config: [case_studies/a2_phenomenological_biased/config_xzzx.yaml](../../config_xzzx.yaml)
- Codes: xzzx
- Noise: phenomenological / biased_meas_yz, eta = [0.5, 10, 25, 50, 100], p_meas = same_as_p
- Plugins: [case_studies/a2_phenomenological_biased/noises.py](../../noises.py)
- Sweeps:
  - `threshold_sweep`: d = [11 .. 19] (5), basis X, Z, p = 42 pts [3.55e-02 .. 8.00e-02]
  - `suppression_sweep`: d = [3, 5, 7], basis X, p = 2.00e-02
- Sampling: decoder mwpm, each task until 10,000 errors or 1,000,000 shots, 4 workers
- Run: 2026-10-21 21:42:44, git 4edeb10

## Warnings

- plugins in the config changed after `cdsc run`; samples.csv was made with the config recorded in manifest.json
- xzzx X eta=0.5 p=2.00e-02: d_teraquop=51 is extrapolated far beyond the largest sampled d=7
- xzzx X eta=10 p=2.00e-02: d_teraquop=39 is extrapolated far beyond the largest sampled d=7
- xzzx X eta=25 p=2.00e-02: d_teraquop=37 is extrapolated far beyond the largest sampled d=7
- xzzx X eta=50 p=2.00e-02: d_teraquop=37 is extrapolated far beyond the largest sampled d=7
- xzzx X eta=100 p=2.00e-02: d_teraquop=37 is extrapolated far beyond the largest sampled d=7

## Threshold

Sweep `threshold_sweep`, fit on d = [11, 13, 15, 17, 19], x_window = 0.1, ν0 = 1.0. Data: [threshold.csv](threshold.csv)

| code   | basis   | eta   | p_th              | ν    | χ²_red   | p-value   | figure                                    |
|--------|---------|-------|-------------------|------|----------|-----------|-------------------------------------------|
| xzzx   | X       | 0.5   | 4.3525% ± 0.0069% | 1.10 | 0.96     | 0.529     | [PDF](figures/threshold_xzzx_X_0.5.pdf)   |
| xzzx   | X       | 10    | 5.7843% ± 0.0103% | 1.14 | 1.30     | 0.135     | [PDF](figures/threshold_xzzx_X_10.0.pdf)  |
| xzzx   | X       | 25    | 6.4006% ± 0.0114% | 1.10 | 0.81     | 0.759     | [PDF](figures/threshold_xzzx_X_25.0.pdf)  |
| xzzx   | X       | 50    | 6.8168% ± 0.0156% | 1.26 | 1.42     | 0.067     | [PDF](figures/threshold_xzzx_X_50.0.pdf)  |
| xzzx   | X       | 100   | 7.0810% ± 0.0152% | 1.24 | 1.01     | 0.455     | [PDF](figures/threshold_xzzx_X_100.0.pdf) |
| xzzx   | Z       | 0.5   | 4.3627% ± 0.0069% | 1.10 | 1.14     | 0.280     | [PDF](figures/threshold_xzzx_Z_0.5.pdf)   |
| xzzx   | Z       | 10    | 5.7180% ± 0.0095% | 1.11 | 1.42     | 0.065     | [PDF](figures/threshold_xzzx_Z_10.0.pdf)  |
| xzzx   | Z       | 25    | 6.2878% ± 0.0113% | 1.14 | 1.13     | 0.287     | [PDF](figures/threshold_xzzx_Z_25.0.pdf)  |
| xzzx   | Z       | 50    | 6.6203% ± 0.0130% | 1.17 | 1.17     | 0.240     | [PDF](figures/threshold_xzzx_Z_50.0.pdf)  |
| xzzx   | Z       | 100   | 6.8599% ± 0.0138% | 1.22 | 0.88     | 0.648     | [PDF](figures/threshold_xzzx_Z_100.0.pdf) |

## Teraquop footprint

Sweep `suppression_sweep`, target p_L = 1e-12 per d rounds. Data: [suppression.csv](suppression.csv)

| code   | basis   | eta   | p        | d*   | d_teraquop   | qubits   | figure                                      |
|--------|---------|-------|----------|------|--------------|----------|---------------------------------------------|
| xzzx   | X       | 0.5   | 2.00e-02 | 50.6 | 51           | 5,201    | [PDF](figures/suppression_xzzx_X_0.5.pdf)   |
| xzzx   | X       | 10    | 2.00e-02 | 38.7 | 39           | 3,041    | [PDF](figures/suppression_xzzx_X_10.0.pdf)  |
| xzzx   | X       | 25    | 2.00e-02 | 36.3 | 37           | 2,737    | [PDF](figures/suppression_xzzx_X_25.0.pdf)  |
| xzzx   | X       | 50    | 2.00e-02 | 36.3 | 37           | 2,737    | [PDF](figures/suppression_xzzx_X_50.0.pdf)  |
| xzzx   | X       | 100   | 2.00e-02 | 35.3 | 37           | 2,737    | [PDF](figures/suppression_xzzx_X_100.0.pdf) |

## Sampling

Data: [samples.csv](samples.csv). 465 tasks, 56.8M shots, 4,665,432 errors. Limited by max_errors: 456 tasks; by max_shots: 9 tasks.

| sweep             | code   | basis   | eta   | d              | p                            | tasks   | shots   | min errors   |
|-------------------|--------|---------|-------|----------------|------------------------------|---------|---------|--------------|
| threshold_sweep   | xzzx   | X       | 0.5   | [11 .. 19] (5) | 9 pts [3.55e-02 .. 5.15e-02] | 45      | 7.1M    | 10,000       |
| threshold_sweep   | xzzx   | Z       | 0.5   | [11 .. 19] (5) | 9 pts [3.55e-02 .. 5.15e-02] | 45      | 7.1M    | 10,002       |
| threshold_sweep   | xzzx   | X       | 10    | [11 .. 19] (5) | 9 pts [5.00e-02 .. 6.60e-02] | 45      | 4.2M    | 10,001       |
| threshold_sweep   | xzzx   | Z       | 10    | [11 .. 19] (5) | 9 pts [5.00e-02 .. 6.60e-02] | 45      | 4.4M    | 10,002       |
| threshold_sweep   | xzzx   | X       | 25    | [11 .. 19] (5) | 9 pts [5.50e-02 .. 7.10e-02] | 45      | 3.9M    | 10,000       |
| threshold_sweep   | xzzx   | Z       | 25    | [11 .. 19] (5) | 9 pts [5.40e-02 .. 7.00e-02] | 45      | 4.7M    | 10,000       |
| threshold_sweep   | xzzx   | X       | 50    | [11 .. 19] (5) | 9 pts [5.90e-02 .. 7.50e-02] | 45      | 3.4M    | 10,002       |
| threshold_sweep   | xzzx   | Z       | 50    | [11 .. 19] (5) | 9 pts [5.90e-02 .. 7.50e-02] | 45      | 3.8M    | 10,000       |
| threshold_sweep   | xzzx   | X       | 100   | [11 .. 19] (5) | 9 pts [6.40e-02 .. 8.00e-02] | 45      | 2.7M    | 10,001       |
| threshold_sweep   | xzzx   | Z       | 100   | [11 .. 19] (5) | 9 pts [6.20e-02 .. 7.80e-02] | 45      | 3.4M    | 10,001       |
| suppression_sweep | xzzx   | X       | 0.5   | [3, 5, 7]      | 2.00e-02                     | 3       | 2.3M    | 6,011        |
| suppression_sweep | xzzx   | X       | 10    | [3, 5, 7]      | 2.00e-02                     | 3       | 2.4M    | 2,850        |
| suppression_sweep | xzzx   | X       | 25    | [3, 5, 7]      | 2.00e-02                     | 3       | 2.4M    | 2,378        |
| suppression_sweep | xzzx   | X       | 50    | [3, 5, 7]      | 2.00e-02                     | 3       | 2.4M    | 2,334        |
| suppression_sweep | xzzx   | X       | 100   | [3, 5, 7]      | 2.00e-02                     | 3       | 2.5M    | 2,050        |

## Validation

Data: [validation.json](validation.json). 4 of 4 passed.

## Circuit diagrams

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
