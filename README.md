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
