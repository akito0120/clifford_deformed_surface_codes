# Clifford-Deformed Surface Codes

A simulation framework for clifford-deformed surface codes. Define the code in stabilizer formalism,
and the framework validates it, builds the Stim circuit, runs sampling, decodes, estimates the 
threshold and the suppression factor and visualizes the result.

## Installation

```
pip install -e .
```

## How to use

```
cdsc validate <path-to-config-file>
cdsc see-plans <path-to-config-file>
cdsc run <path-to-config-file>
cdsc analyze <path-to-config-file>
cdsc visualize <path-to-config-file>
```

## Config file

Every command takes one YAML config (schema: [`src/cdsc/config.py`](src/cdsc/config.py)). Example (`configs/smoke.yaml`):

```yaml
experiment:
  name: smoke
  seed: 0

codes: [rotated_surface, xzzx]

noise:
  model: circuit_level        # code_capacity | phenomenological | circuit_level
  definition: biased          # depolarizing | biased | user defined noise
  params:
    eta: [0.5, 10]            # each parameter takes a list of values to sweep
  p_meas: same_as_p           # "same_as_p" or a number

sweeps:
  - id: threshold_sweep
    distances: [7, 9, 11]
    basis: [X]
    p:
      mode: window
      centers: [0.0069, 0.0072, 0.0061, 0.0123]
      half_width: 0.003
      step: 0.00025
  - id: suppression_sweep
    distances: [3, 5, 7, 9, 11]
    basis: [X]
    p:
      mode: list
      values: [0.001, 0.002, 0.003, 0.004]

sampling:
  decoder: mwpm               # mwpm | uf | bp
  max_shots: 100000
  max_errors: 10000
  max_batch_size: 1024
  workers: 4

threshold:
  source_sweep: threshold_sweep
  distances: [7, 9, 11]
  x_window: 0.006
  nu_0: 1.1

suppression:
  source_sweep: suppression_sweep
  target_pl: 1e-12

output:
  dir: results/smoke
```

Notes:

- One sweep plan is created per combination of `noise.params` × `basis` × `codes`. The last key varies fastest, and params keep their YAML order. In `window` mode, `centers` needs one entry per combination, in that order. The example gives (eta, code) = (0.5, rotated_surface), (0.5, xzzx), (10, rotated_surface), (10, xzzx). Check the plans with `cdsc see-plans`.


## Layout

```
.
├── configs                 # Simulation config files
└── src/cdsc
    ├── analysis/           # Threshold and suppression analysis
    ├── circuit_builder/    # Stim circuit builders
    ├── codes/              # Code definition, registry and built-in codes
    ├── noise/              # Noise definition, registry and built-in noises
    ├── sweep/              # Sweep plan builder and sweep runner
    ├── validation/         # Code and circuit validation
    ├── visualization/      # Visualization of sampling and analysis result
    ├── cli.py              # CLI entrypoint and command handlers
    ├── config.py           # YAML config schema definition
    └── decoder.py          # Decoder registry
```
