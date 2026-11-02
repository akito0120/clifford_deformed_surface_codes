# A3: Phenomenological threshold against stim's generated circuits

## Prior studies

| Key | Paper | Where | Value | Conditions |
|---|---|---|---|---|
| Gidney2021Stim | C. Gidney, "Stim: a fast stabilizer circuit simulator" [arXiv:2103.02202](https://arxiv.org/abs/2103.02202) | `stim.Circuit.generated`, tasks `surface_code:rotated_memory_x` and `_z` | Reference circuits, sampled at the framework's points | `rounds = d`, `before_round_data_depolarization = p`, `before_measure_flip_probability = p`, `after_clifford_depolarization = 0`, `after_reset_flip_probability = 0` |
| LinLai2025 | T.-H. Lin and C.-Y. Lai, "Union-Intersection Union-Find for Decoding Depolarizing Errors in Topological Codes" [arXiv:2506.14745](https://arxiv.org/abs/2506.14745) | Table V, §V-C | MWPM 3.92% | Rotated code, depolarizing data noise at ε, measurement flips at ε, d noisy rounds and a perfect last round, PyMatching v2, logical X error rate, FSS fit with a low-order polynomial (to ±0.01%), 10⁶ samples per point. The distances are not stated |

- **stim's circuits are the framework's model.**
  - With detectors matched by their coordinates, their detector error models equal the framework's at every simulated distance in both bases, once mechanisms with the same symptoms are merged. So do the decomposed edges PyMatching decodes.
  - So the stim comparison is a differential test of the phenomenological builder, not a reproduction of a published value.
- **LinLai2025 differs only at the top time boundary.**
  - Its last round of data noise flips each memory basis at 2ε/3. In its place, the framework flips the final data readout at ε.
  - It counts logical X errors only, i.e. one basis, as the framework does.

## Setup

- Configs: [config_framework.yaml](config_framework.yaml) and [config_stim.yaml](config_stim.yaml), identical except `experiment.name` and `output.dir`
- The stim side ran through [sample_stim.py](sample_stim.py), with `--reference config_framework.yaml`. It writes samples.csv for `cdsc analyze`, so both sides are fitted the same way.
- Code: `rotated_surface`
- `phenomenological` with `depolarizing` noise and `p_meas: same_as_p`
- Decoder: `mwpm`
- d = 7, 9, 11, 13, 15
- Bases: X and Z
- p = 3.3–4.5% in steps of 0.1%
- Each point ran to at least 20,000 errors

## Result

From [results/framework/threshold.csv](results/framework/threshold.csv) and [results/stim/threshold.csv](results/stim/threshold.csv):

| Basis | Framework p_th (%) | stim p_th (%) | Framework − stim (points) | ν (framework / stim) | χ²_red (framework / stim) |
|---|---|---|---|---|---|
| X | 3.892 ± 0.005 | 3.900 ± 0.005 | −0.008 ± 0.007 (−1.2σ) | 1.09 / 1.10 | 1.25 / 1.39 |
| Z | 3.904 ± 0.005 | 3.902 ± 0.005 | +0.002 ± 0.007 (+0.2σ) | 1.13 / 1.09 | 0.62 / 0.82 |

- Against LinLai2025's 3.92%, the framework is 0.028 points (X) and 0.016 points (Z) lower, i.e. 0.7% and 0.4% (relative).

## Verdict

- **Threshold against stim: pass.** Within 1.2σ in both bases.
- **p_L point by point comparison against stim: pass.** The two samples are statistically indistinguishable.
- **Threshold against LinLai2025 (3.92%): consistent.** Other fits of the same data (d = 7–15 or 11–15, x_window = 0.04–0.08) give 3.88–3.92%, which covers the gap.


## Excerpts

Verbatim from the sources, for text search in the originals. Math is in plain text, and citations are shown as […].

### Gidney2021Stim (stim 1.16.0, the version A3 ran with)

The paper (arXiv v3, published as Quantum 5, 497) does not describe `stim.Circuit.generated`, and the stim v1.3 source in its ancillary files has no generator. The excerpts are from stim at tag [v1.16.0](https://github.com/quantumlib/Stim/tree/v1.16.0) (commit e2fc1ec).

- Code tasks, `rounds` and the noise arguments, from the docstring of `stim.Circuit.generated` ([circuit.pybind.cc L1366–1370, L1378–1397](https://github.com/quantumlib/Stim/blob/e2fc1ec/src/stim/circuit/circuit.pybind.cc#L1366-L1397)):
  ```text
  code_task: A string identifying the type of circuit to generate. Available
      code tasks are:
          - "repetition_code:memory"
          - "surface_code:rotated_memory_x"
          - "surface_code:rotated_memory_z"
  ...
  rounds: How many times the measurement qubits in the generated circuit will
      be measured. Indirectly determines the duration of the generated
      circuit.
  after_clifford_depolarization: Defaults to 0. The probability (p) of
      `DEPOLARIZE1(p)` operations to add after every single-qubit Clifford
      operation and `DEPOLARIZE2(p)` operations to add after every two-qubit
      Clifford operation. The after-Clifford depolarizing operations are only
      included if this probability is not 0.
  before_round_data_depolarization: Defaults to 0. The probability (p) of
      `DEPOLARIZE1(p)` operations to apply to every data qubit at the start of
      a round of stabilizer measurements. The start-of-round depolarizing
      operations are only included if this probability is not 0.
  before_measure_flip_probability: Defaults to 0. The probability (p) of
      `X_ERROR(p)` operations applied to qubits before each measurement (X
      basis measurements use `Z_ERROR(p)` instead). The before-measurement
      flips are only included if this probability is not 0.
  after_reset_flip_probability: Defaults to 0. The probability (p) of
      `X_ERROR(p)` operations applied to qubits after each reset (X basis
      resets use `Z_ERROR(p)` instead). The after-reset flips are only
      included if this probability is not 0.
  ```
- Rounds and the final data readout ([gen_surface_code.cc L124–126, L135, L167–168, L191–192](https://github.com/quantumlib/Stim/blob/e2fc1ec/src/stim/gen/gen_surface_code.cc#L124-L192)):
  ```cpp
  // Build the repeated actions that make up the surface code cycle.
  Circuit cycle_actions;
  params.append_begin_round_tick(cycle_actions, data_qubits);
  ...
  params.append_measure_reset(cycle_actions, measurement_qubits);
  ...
  Circuit tail;
  params.append_measure(tail, data_qubits, "ZX"[is_memory_x]);
  ...
  // Combine to form final circuit.
  Circuit full_circuit = head + body * (params.rounds - 1) + tail;
  ```

### LinLai2025 (arXiv v1, published in IEEE JSAIT, doi:10.1109/JSAIT.2025.3581810)

- Depolarizing errors at ε (§II-B):
  > We assume that each qubit experiences independent depolarizing Pauli errors at a physical error rate of ε, where a qubit undergoes an X, Y, or Z error with probability ε/3.
- Phenomenological model (§II-E, §V):
  > To handle faulty syndrome measurements, we consider the scenario where syndrome extraction is repeated for d rounds for a code of distance d, without employing additional redundant stabilizer measurements […]. During each round of syndrome extraction, data qubits undergo independent depolarizing errors, while measurement outcomes may suffer independent bit-flip errors.

  > For the phenomenological noise model, the data qubits experience depolarizing errors with a physical error rate of ε, and we assume that the measurement outcomes are flipped with probability ε.
- Rounds and the perfect last round (§V-A):
  > All the above observations also hold for the phenomenological noise model, as shown in Figure 10, where d+1 rounds of syndrome extraction are performed for a code of distance d. In this setup, the final round is assumed to have perfect syndromes, which are used to determine whether a logical error occurred in the previous rounds. Note that the logical error rate here is not normalized by the number of rounds.
- Fit and samples (§V-B):
  > The logical error rate p_L is fitted to the form d^(1/ν)(ε − τ) across a range of topological codes using low-order polynomials, where ν is the critical exponent and ε is the physical error rate, and τ is the threshold.

  > The accuracy of ν is ±0.01, and the accuracy of τ is ±0.01%.

  > Figure 11(a) illustrates the decoding performance of UIUF with WG for the [[2d^2, 2, d]] toric codes near the threshold of this code family, where each data point is generated using 10^6 samples.
- Decoder (§V-C):
  > For the MWPM decoder, we use the PyMatching v2 implementation […] in our simulations.
- Value (§I and Table V, row MWPM, column Phen., marked †):
  > Although UIUF’s threshold in the phenomenological noise model (3.47%) is lower than MWPM’s threshold of 3.92%, we demonstrate that UIUF achieves lower logical error rates than MWPM in both the code capacity and phenomenological noise models.

  > Comparison between the MWPM and UIUF decoders in the code capacity and phenomenological noise models.

  > †: Estimate from PyMatching simulations of logical X error rates.
