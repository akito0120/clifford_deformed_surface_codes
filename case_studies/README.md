# Case studies

Each case reproduces published results with the framework. Its `result.md` lists the references, the setup, the results and a verdict.

| Case | What it evaluates |
|---|---|
| [A1](a1_code_capacity_depolarizing/result.md) | The depolarizing code-capacity threshold of the rotated surface, XZZX and XY codes with `mwpm`. Checks that the three codes share one threshold (Clifford invariance), against Criger2018 and Campos2026. |
| [A2](a2_phenomenological_biased/result.md) | The phenomenological threshold of the CSS and XZZX codes as the bias η grows, with `mwpm`. Checks that bias lowers the CSS threshold and raises the XZZX one, against Campos2026 and BonillaAtaides2021's CSS reference line. |
| [A3](a3_phenomenological_vs_stim/result.md) | A differential test of the phenomenological builder against stim's generated rotated-code circuits, by threshold and by p_L point by point. The threshold is also compared with LinLai2025. |
| [A4](a4_circuit_level_depolarizing/result.md) | The circuit-level depolarizing threshold of the rotated surface code with `mwpm`, against Stephens2014 and the published band of 0.50–0.82%. |
| [A5](a5_suppression_circuit_level/result.md) | Below-threshold suppression at circuit level under ORourke2025's SD noise, rebuilt with plugins. Compares p_L, Λ and the teraquop footprint at p = 0.1% and 0.2% with the paper's released circuits and data. |
| [B1](b1_decoder_comparison/result.md) | The `bp` and `uf` decoders against `mwpm` at code capacity, under depolarizing noise and independent Z flips. Compares the thresholds and their ratios to MWPM with Criger2018, Delfosse2021, LinLai2025 and the optimal bounds. |
